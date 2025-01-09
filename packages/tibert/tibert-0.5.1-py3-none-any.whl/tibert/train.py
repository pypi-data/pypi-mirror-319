import pickle
from typing import List, Optional, Tuple, Type, Union, Literal
import traceback, copy, os
from statistics import mean
import torch
from torch.utils.data.dataloader import DataLoader
from transformers import BertTokenizerFast, CamembertTokenizerFast  # type: ignore
from tqdm import tqdm
from tibert.bertcoref import (
    BertForCoreferenceResolution,
    CamembertForCoreferenceResolution,
    CoreferenceDataset,
    CoreferenceDocument,
    DataCollatorForSpanClassification,
)
from tibert.score import score_coref_predictions, score_mention_detection
from tibert.predict import predict_coref, predict_coref_simple
from tibert.utils import gpu_memory_usage


def _save_train_checkpoint(
    path: str,
    model: Union[BertForCoreferenceResolution, CamembertForCoreferenceResolution],
    epoch: int,
    optimizer: torch.optim.AdamW,
    bert_lr: float,
    task_lr: float,
):
    checkpoint = {
        "model": model.state_dict(),
        "model_config": vars(model.config),
        "epoch": epoch,
        "optimizer": optimizer.state_dict(),
        "bert_lr": bert_lr,
        "task_lr": task_lr,
    }
    torch.save(checkpoint, path)


def load_train_checkpoint(
    checkpoint_path: str,
    model_class: Union[
        Type[BertForCoreferenceResolution], Type[CamembertForCoreferenceResolution]
    ],
) -> Tuple[
    Union[BertForCoreferenceResolution, CamembertForCoreferenceResolution],
    torch.optim.AdamW,
]:
    config_class = model_class.config_class

    checkpoint = torch.load(checkpoint_path, weights_only=True)

    model_config = config_class(**checkpoint["model_config"])
    model = model_class(model_config)
    model.load_state_dict(checkpoint["model"], strict=False)

    optimizer = torch.optim.AdamW(
        [
            {"params": model.bert_parameters(), "lr": checkpoint["bert_lr"]},
            {
                "params": model.task_parameters(),
                "lr": checkpoint["task_lr"],
            },
        ],
        lr=checkpoint["task_lr"],
    )
    optimizer.load_state_dict(checkpoint["optimizer"])

    return model, optimizer


def _optimizer_to_(
    optimizer: torch.optim.AdamW, device: torch.device
) -> torch.optim.AdamW:
    """From https://github.com/pytorch/pytorch/issues/2830"""
    for state in optimizer.state.values():
        for k, v in state.items():
            if isinstance(v, torch.Tensor):
                state[k] = v.to(device)
    return optimizer


def _save_append_example_pred(
    path: str,
    model: Union[BertForCoreferenceResolution, CamembertForCoreferenceResolution],
    tokenizer: Union[BertTokenizerFast, CamembertTokenizerFast],
    example_doc: CoreferenceDocument,
):
    """
    Save an example and its prediction to a file, keeping previous
    predictions.  Useful to follow the evolution of predictions for an
    example.
    """
    pred = predict_coref_simple(example_doc.tokens, model, tokenizer)

    if os.path.exists(path):
        with open(path, "rb") as f:
            ex_dict = pickle.load(f)
        ex_dict["preds"] = ex_dict.get("preds", []) + [pred]
    else:
        ex_dict = {"ref": example_doc, "preds": [pred]}

    with open(path, "wb") as f:
        pickle.dump(ex_dict, f)


def train_coref_model(
    model: Union[BertForCoreferenceResolution, CamembertForCoreferenceResolution],
    train_dataset: CoreferenceDataset,
    valid_dataset: CoreferenceDataset,
    tokenizer: Union[BertTokenizerFast, CamembertTokenizerFast],
    batch_size: int = 1,
    epochs_nb: int = 30,
    bert_lr: float = 1e-5,
    task_lr: float = 2e-4,
    model_save_dir: Optional[str] = None,
    device_str: Literal["cpu", "cuda", "auto"] = "auto",
    _run: Optional["sacred.run.Run"] = None,
    optimizer: Optional[torch.optim.AdamW] = None,
    example_tracking_path: Optional[str] = None,
) -> BertForCoreferenceResolution:
    """
    :param model: model to train
    :param dataset: dataset to train on.  90% of that dataset will be
        used for training, 10% for testing
    :param tokenizer: tokenizer associated with ``model``
    :param batch_size: batch_size during training and testing
    :param epochs_nb: number of epochs to train for
    :param sents_per_documents_train: max number of sentences in each
        train document
    :param bert_lr: learning rate of the BERT encoder
    :param task_lr: learning rate for other parts of the network
    :param model_save_dir: directory in which to save the final model
        (under 'model') and checkpoints ('checkpoint.pth')
    :param device_str:
    :param _run: sacred run, used to log metrics
    :param optimizer: a torch optimizer to use.  Can be useful to
        resume training.
    :param example_tracking_path: if given, path to a file where an
        example and its prediction will be dumped each epoch.  Usefull
        to track the evolution of predictions.

    :return: the best trained model, according to CoNLL-F1 on the test
             set
    """
    # Get torch device and send model to it
    # -------------------------------------
    if device_str == "auto":
        device_str = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(device_str)
    model = model.to(device)

    data_collator = DataCollatorForSpanClassification(
        tokenizer, model.config.max_span_size, device_str
    )
    train_dataloader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, collate_fn=data_collator
    )

    # Optimizer initialization
    # ------------------------
    if optimizer is None:
        optimizer = torch.optim.AdamW(
            [
                {"params": model.bert_parameters(), "lr": bert_lr},
                {
                    "params": model.task_parameters(),
                    "lr": task_lr,
                },
            ],
            lr=task_lr,
        )
    optimizer = _optimizer_to_(optimizer, device)

    # -----------------
    best_f1 = 0
    best_model = model

    # Training loop
    # -------------
    for epoch_i in range(epochs_nb):
        model = model.train()

        epoch_losses = []

        data_tqdm = tqdm(train_dataloader)
        for batch in data_tqdm:
            optimizer.zero_grad()

            try:
                out = model(**batch)
            except Exception as e:
                print(e)
                traceback.print_exc()
                continue

            assert not out.loss is None
            out.loss.backward()
            optimizer.step()

            if device_str == "cuda":
                _ = _run and _run.log_scalar("gpu_usage", gpu_memory_usage())

            data_tqdm.set_description(f"loss : {out.loss.item()}")
            epoch_losses.append(out.loss.item())
            if _run:
                _run.log_scalar("loss", out.loss.item())

        if _run:
            _run.log_scalar("epoch_mean_loss", mean(epoch_losses))

        # Metrics Computation
        # -------------------
        preds = predict_coref(
            [doc.tokens for doc in valid_dataset.documents],
            model,
            tokenizer,
            batch_size=batch_size,
            device_str=device_str,
        )
        metrics = score_coref_predictions(preds, valid_dataset.documents)

        conll_f1 = mean(
            [metrics["MUC"]["f1"], metrics["B3"]["f1"], metrics["CEAF"]["f1"]]
        )
        if _run:
            _run.log_scalar("validation.muc_precision", metrics["MUC"]["precision"])
            _run.log_scalar("validation.muc_recall", metrics["MUC"]["recall"])
            _run.log_scalar("validation.muc_f1", metrics["MUC"]["f1"])
            _run.log_scalar("validation.b3_precision", metrics["B3"]["precision"])
            _run.log_scalar("validation.b3_recall", metrics["B3"]["recall"])
            _run.log_scalar("validation.b3_f1", metrics["B3"]["f1"])
            _run.log_scalar("validation.ceaf_precision", metrics["CEAF"]["precision"])
            _run.log_scalar("validation.ceaf_recall", metrics["CEAF"]["recall"])
            _run.log_scalar("validation.ceaf_f1", metrics["CEAF"]["f1"])
            _run.log_scalar("validation.conll_f1", conll_f1)
        print(metrics)

        m_precision, m_recall, m_f1 = score_mention_detection(
            preds, valid_dataset.documents
        )
        if _run:
            _run.log_scalar("validation.mention_detection_precision", m_precision)
            _run.log_scalar("validation.mention_detection_recall", m_recall)
            _run.log_scalar("validation.mention_detection_f1", m_f1)
        print(
            f"mention detection metrics: (precision: {m_precision}, recall: {m_recall}, f1: {m_f1})"
        )

        # Example evolution tracking
        # --------------------------
        if not example_tracking_path is None:
            _save_append_example_pred(
                example_tracking_path, model, tokenizer, valid_dataset.documents[1]
            )

        # Model saving
        # ------------
        if not model_save_dir is None:
            os.makedirs(model_save_dir, exist_ok=True)
            _save_train_checkpoint(
                os.path.join(model_save_dir, "checkpoint.pth"),
                model,
                epoch_i,
                optimizer,
                bert_lr,
                task_lr,
            )
        if conll_f1 > best_f1 or best_f1 == 0:
            best_model = copy.deepcopy(model).to("cpu")
            best_f1 = conll_f1
            if not model_save_dir is None:
                model.save_pretrained(os.path.join(model_save_dir, "model"))

    return best_model
