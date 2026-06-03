"""QLoRA fine-tune for the HERA Risk & Safety Copilot baseline.

Reads:
- configs/model.yaml      base model selection
- configs/training.yaml   LoRA hyperparams + training loop config
- data/training/conversations.jsonl  OpenAI-messages format

Produces:
- models/baseline-lora/   adapter weights + tokenizer + training_state.json
- runs/finetune_<ts>/     log file + config snapshot + git SHA

Designed to be run on the external CUDA machine over SSH:

    ssh user@cuda-box
    cd hera-risk-safety-copilot
    uv sync --extra train
    nohup uv run python -m src.baseline.finetune \\
        --config configs/training.yaml \\
        --model-config configs/model.yaml \\
        --model-id qwen2.5-7b-instruct \\
        > finetune.out 2>&1 &
    tail -f finetune.out

Local dry-run (no GPU needed, builds dataset but doesn't load the model):

    uv run python -m src.baseline.finetune --dry-run
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.utils.logging_config import (  # noqa: E402
    configure_logging,
    load_dotenv,
    new_run_dir,
)

log = logging.getLogger("finetune")

DEFAULTS = {
    "model_config": REPO_ROOT / "configs/model.yaml",
    "training_config": REPO_ROOT / "configs/training.yaml",
    "data_path": REPO_ROOT / "data/training/conversations.jsonl",
    "output_dir": REPO_ROOT / "models/baseline-lora",
}


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------


def load_yaml(path: Path) -> dict:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


def select_model(model_config: dict, requested_id: str | None) -> dict:
    """Pick a candidate from configs/model.yaml by id; default to .selected."""
    candidates = {c["name"]: c for c in model_config["candidates"]}
    name = requested_id or model_config.get("selected")
    if name not in candidates:
        raise SystemExit(
            f"Model '{name}' not in configs/model.yaml. "
            f"Available: {sorted(candidates)}"
        )
    return candidates[name]


# ---------------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------------


def load_jsonl(path: Path) -> list[dict]:
    items: list[dict] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        items.append(json.loads(raw))
    return items


def split_dataset(data_path: Path, val_split: float, seed: int) -> tuple[list[dict], list[dict]]:
    """Load JSONL → list of {"messages": ...} dicts, shuffled and split."""
    rows = load_jsonl(data_path)
    if not rows:
        raise SystemExit(f"No examples found in {data_path}")
    log.info("Loaded %d examples from %s", len(rows), data_path.name)

    # Keep only the conversation; drop our metadata (TRL SFTTrainer expects messages-only)
    cleaned = [{"messages": r["messages"]} for r in rows if "messages" in r]
    if len(cleaned) != len(rows):
        log.warning("Dropped %d rows without 'messages'", len(rows) - len(cleaned))

    rng = random.Random(seed)
    rng.shuffle(cleaned)
    n_val = max(1, int(len(cleaned) * val_split))
    train = cleaned[n_val:]
    val = cleaned[:n_val]

    log.info("Train: %d | Val: %d (val_split=%.2f, seed=%d)",
             len(train), len(val), val_split, seed)
    return train, val


def to_hf_datasets(train: list[dict], val: list[dict]):
    """Defer the heavy HF Datasets import until really needed."""
    from datasets import Dataset

    return Dataset.from_list(train), Dataset.from_list(val)


# ---------------------------------------------------------------------------
# Model + tokenizer
# ---------------------------------------------------------------------------


def load_model_and_tokenizer(model_spec: dict, quant_cfg: dict, dry_run: bool):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    hf_id = model_spec["hf_id"]
    log.info("Loading tokenizer: %s", hf_id)
    tokenizer = AutoTokenizer.from_pretrained(hf_id, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Hybrid-reasoning models (Qwen3) inject <think> blocks via their chat template by
    # default. Our HERA dialogues are direct (no chain-of-thought), so we force
    # non-thinking rendering. Wrapping apply_chat_template is version-agnostic: whatever
    # path TRL takes (messages -> template), thinking stays off. The kwarg is silently
    # ignored by templates that don't define it (Mistral / Qwen2.5 / Phi), so this is a
    # no-op there.
    _orig_apply = tokenizer.apply_chat_template

    def _apply_no_think(*a, **k):
        k.setdefault("enable_thinking", False)
        return _orig_apply(*a, **k)

    tokenizer.apply_chat_template = _apply_no_think

    if dry_run:
        log.info("[dry-run] skipping model load")
        return None, tokenizer

    bnb = BitsAndBytesConfig(
        load_in_4bit=quant_cfg["load_in_4bit"],
        bnb_4bit_quant_type=quant_cfg["bnb_4bit_quant_type"],
        bnb_4bit_compute_dtype=getattr(torch, quant_cfg["bnb_4bit_compute_dtype"]),
        bnb_4bit_use_double_quant=quant_cfg["bnb_4bit_use_double_quant"],
    )

    log.info("Loading model (4-bit QLoRA): %s", hf_id)
    model = AutoModelForCausalLM.from_pretrained(
        hf_id,
        quantization_config=bnb,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
    )
    model.config.use_cache = False
    if hasattr(model, "config") and getattr(model.config, "pretraining_tp", 1) != 1:
        model.config.pretraining_tp = 1
    return model, tokenizer


def wrap_with_lora(model, lora_cfg: dict):
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

    model = prepare_model_for_kbit_training(model)
    peft_cfg = LoraConfig(
        r=lora_cfg["r"],
        lora_alpha=lora_cfg["alpha"],
        lora_dropout=lora_cfg["dropout"],
        bias=lora_cfg["bias"],
        target_modules=lora_cfg["target_modules"],
        task_type=lora_cfg["task_type"],
    )
    model = get_peft_model(model, peft_cfg)
    trainable, total = 0, 0
    for p in model.parameters():
        total += p.numel()
        if p.requires_grad:
            trainable += p.numel()
    log.info("LoRA wrapped. Trainable: %s / %s (%.4f%%)",
             f"{trainable:,}", f"{total:,}", 100 * trainable / total)
    return model


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------


def get_git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def snapshot_configs(run_dir: Path, model_cfg: dict, training_cfg: dict, args: argparse.Namespace) -> None:
    import yaml

    (run_dir / "model_config.yaml").write_text(yaml.safe_dump(model_cfg), encoding="utf-8")
    (run_dir / "training_config.yaml").write_text(yaml.safe_dump(training_cfg), encoding="utf-8")
    (run_dir / "args.json").write_text(json.dumps(vars(args), default=str, indent=2), encoding="utf-8")
    (run_dir / "git.txt").write_text(get_git_sha() + "\n", encoding="utf-8")


def build_trainer(model, tokenizer, train_ds, val_ds, training_cfg: dict,
                  output_dir: Path, max_seq_length: int):
    import inspect

    from trl import SFTConfig, SFTTrainer

    tcfg = training_cfg["training"]
    cfg_kwargs = dict(
        output_dir=str(output_dir),
        num_train_epochs=tcfg["num_train_epochs"],
        per_device_train_batch_size=tcfg["per_device_train_batch_size"],
        gradient_accumulation_steps=tcfg["gradient_accumulation_steps"],
        learning_rate=tcfg["learning_rate"],
        lr_scheduler_type=tcfg["lr_scheduler_type"],
        warmup_ratio=tcfg["warmup_ratio"],
        weight_decay=tcfg["weight_decay"],
        max_grad_norm=tcfg["max_grad_norm"],
        optim=tcfg["optim"],
        bf16=tcfg["bf16"],
        gradient_checkpointing=tcfg["gradient_checkpointing"],
        logging_steps=tcfg["logging_steps"],
        eval_strategy=tcfg["eval_strategy"],
        eval_steps=tcfg["eval_steps"],
        save_strategy=tcfg["save_strategy"],
        save_steps=tcfg["save_steps"],
        save_total_limit=tcfg["save_total_limit"],
        load_best_model_at_end=tcfg["load_best_model_at_end"],
        metric_for_best_model=tcfg["metric_for_best_model"],
        report_to="none",
        seed=training_cfg.get("seed", 1337),
    )

    # TRL renamed several args across versions — introspect and pass only what THIS
    # installed version accepts (e.g. max_seq_length -> max_length in recent TRL).
    sft_params = inspect.signature(SFTConfig.__init__).parameters
    if "max_length" in sft_params:
        cfg_kwargs["max_length"] = max_seq_length
    elif "max_seq_length" in sft_params:
        cfg_kwargs["max_seq_length"] = max_seq_length
    if "dataset_kwargs" in sft_params:
        cfg_kwargs["dataset_kwargs"] = {"skip_prepare_dataset": False}

    # SFTTrainer renamed `tokenizer` -> `processing_class` in recent TRL/transformers.
    trainer_params = inspect.signature(SFTTrainer.__init__).parameters
    tok_kw = "processing_class" if "processing_class" in trainer_params else "tokenizer"

    def _make(assistant_only: bool):
        kw = dict(cfg_kwargs)
        if assistant_only and "assistant_only_loss" in sft_params:
            kw["assistant_only_loss"] = True
        kw = {k: v for k, v in kw.items() if k in sft_params}
        return SFTTrainer(
            model=model,
            args=SFTConfig(**kw),
            train_dataset=train_ds,
            eval_dataset=val_ds,
            **{tok_kw: tokenizer},
        )

    # assistant_only_loss computes the loss ONLY on assistant turns (system/user tokens
    # masked) — focuses learning on the HERA answers. It needs both TRL support and a
    # chat template with {% generation %} markers; if either is missing, fall back to
    # full-sequence loss rather than crash the run.
    want_assistant_only = bool(tcfg.get("assistant_only_loss", False))
    if want_assistant_only and "assistant_only_loss" in sft_params:
        try:
            trainer = _make(True)
            log.info("assistant_only_loss: ENABLED (loss computed on assistant turns only)")
            return trainer
        except Exception as exc:  # noqa: BLE001
            log.warning("assistant_only_loss unsupported here (%s) — falling back to full-sequence loss", exc)
    elif want_assistant_only:
        log.warning("assistant_only_loss requested but absent from this TRL version — full-sequence loss")
    return _make(False)


def save_adapter(model, tokenizer, output_dir: Path, run_dir: Path, training_cfg: dict, model_spec: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info("Saving adapter to %s", output_dir)
    model.save_pretrained(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))

    # training_state.json — enough to reproduce the merge later
    state = {
        "base_model_hf_id": model_spec["hf_id"],
        "base_model_name": model_spec["name"],
        "lora_config": training_cfg["lora"],
        "training_config": training_cfg["training"],
        "git_sha": get_git_sha(),
        "run_dir": str(run_dir),
    }
    (output_dir / "training_state.json").write_text(
        json.dumps(state, indent=2), encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, default=DEFAULTS["training_config"])
    ap.add_argument("--model-config", type=Path, default=DEFAULTS["model_config"])
    ap.add_argument("--model-id", default=None,
                    help="Override 'selected' from configs/model.yaml")
    ap.add_argument("--data", type=Path, default=DEFAULTS["data_path"])
    ap.add_argument("--output-dir", type=Path, default=DEFAULTS["output_dir"])
    ap.add_argument("--dry-run", action="store_true",
                    help="Build dataset, snapshot configs, don't load the model.")
    ap.add_argument("--resume", action="store_true",
                    help="Resume from the last checkpoint in --output-dir.")
    args = ap.parse_args(argv)

    run_dir = new_run_dir(prefix="finetune")
    configure_logging(run_dir)
    load_dotenv()
    log.info("Run dir: %s", run_dir)
    log.info("Git SHA: %s", get_git_sha())

    model_cfg = load_yaml(args.model_config)
    training_cfg = load_yaml(args.config)
    model_spec = select_model(model_cfg, args.model_id)
    log.info("Base model: %s (%s, %s B params)",
             model_spec["name"], model_spec["hf_id"], model_spec.get("params_b"))

    seed = training_cfg.get("seed", 1337)
    random.seed(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass
    if not args.dry_run:
        import torch
        torch.manual_seed(seed)

    snapshot_configs(run_dir, model_cfg, training_cfg, args)

    ds_cfg = training_cfg["dataset"]
    train, val = split_dataset(args.data, ds_cfg["val_split"], seed)

    if args.dry_run:
        log.info("[dry-run] dataset OK · configs snapshotted · model load skipped.")
        log.info("[dry-run] First train example has %d messages, roles=%s",
                 len(train[0]["messages"]),
                 [m["role"] for m in train[0]["messages"]])
        return 0

    model, tokenizer = load_model_and_tokenizer(
        model_spec, training_cfg["quantization"], args.dry_run
    )
    model = wrap_with_lora(model, training_cfg["lora"])

    train_ds, val_ds = to_hf_datasets(train, val)
    trainer = build_trainer(
        model, tokenizer, train_ds, val_ds, training_cfg,
        args.output_dir, ds_cfg["max_seq_length"],
    )

    log.info("Starting training…")
    trainer.train(resume_from_checkpoint=args.resume)
    log.info("Training complete.")

    save_adapter(model, tokenizer, args.output_dir, run_dir, training_cfg, model_spec)
    log.info("Done. Adapter saved to %s", args.output_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
