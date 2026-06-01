"""Merge a PEFT/LoRA adapter into its base model and save the result in HF format.

This is step 1/3 of the post-training pipeline:
    1. merge_adapter.py     (this script)   LoRA adapter + base → merged HF model
    2. llama.cpp convert    (shell command) HF model → GGUF f16
    3. llama.cpp quantize   (shell command) GGUF f16 → GGUF q4_K_M
    4. ollama create        (shell command) GGUF q4 + Modelfile → ollama tag

Usage:
    uv run --extra train python scripts/ollama_workflow/merge_adapter.py \\
        --adapter models/baseline-lora \\
        --out    models/baseline-merged

Reads:
- adapter_config.json + adapter weights from --adapter
- training_state.json next to it (records the base model HF id)
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.utils.logging_config import configure_logging, new_run_dir  # noqa: E402

log = logging.getLogger("merge")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", type=Path, required=True,
                    help="Path to LoRA adapter dir (e.g., models/baseline-lora)")
    ap.add_argument("--out", type=Path, required=True,
                    help="Where to write the merged HF model")
    ap.add_argument("--base-model", default=None,
                    help="Override base model HF id (default: read training_state.json)")
    args = ap.parse_args(argv)

    run_dir = new_run_dir(prefix="merge")
    configure_logging(run_dir)

    if not args.adapter.exists():
        log.error("Adapter dir not found: %s", args.adapter)
        return 1

    state_path = args.adapter / "training_state.json"
    if args.base_model:
        base_id = args.base_model
    elif state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        base_id = state["base_model_hf_id"]
    else:
        log.error("No --base-model given and no training_state.json at %s", state_path)
        return 1
    log.info("Base model HF id: %s", base_id)
    log.info("Adapter dir: %s", args.adapter)

    # Import torch lazily so --help works without GPU deps installed
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    log.info("Loading tokenizer…")
    tokenizer = AutoTokenizer.from_pretrained(base_id, trust_remote_code=True)

    log.info("Loading base model in bfloat16 (full precision merge)…")
    base = AutoModelForCausalLM.from_pretrained(
        base_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )

    log.info("Loading LoRA adapter…")
    model = PeftModel.from_pretrained(base, str(args.adapter))

    log.info("Merging adapter into base weights…")
    merged = model.merge_and_unload()

    args.out.mkdir(parents=True, exist_ok=True)
    log.info("Saving merged model to %s", args.out)
    merged.save_pretrained(str(args.out), safe_serialization=True)
    tokenizer.save_pretrained(str(args.out))

    # Re-emit training_state for downstream tooling
    if state_path.exists():
        (args.out / "training_state.json").write_text(
            state_path.read_text(encoding="utf-8"), encoding="utf-8"
        )

    log.info("Done. Next step:")
    log.info("  # 2/3 — convert to GGUF f16")
    log.info("  python ~/llama.cpp/convert_hf_to_gguf.py %s --outtype f16 --outfile %s/hera-baseline.f16.gguf",
             args.out, args.out)
    log.info("  # 3/3 — quantize to q4_K_M")
    log.info("  ~/llama.cpp/build/bin/llama-quantize %s/hera-baseline.f16.gguf %s/hera-baseline.q4_K_M.gguf q4_K_M",
             args.out, args.out)
    log.info("  # 4/4 — create Ollama tag (see scripts/ollama_workflow/README.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
