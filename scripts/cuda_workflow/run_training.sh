#!/usr/bin/env bash
# HERA QLoRA fine-tune — end-to-end on the CUDA/WSL box.
#
# Steps: (1) sanity checks  (2) dry-run  (3) train Qwen3-8B (non-thinking SFT)
#        (4) markdown recap  (5) stage adapter + recap on git (LFS) — push is left to YOU.
#
# Run it DETACHED so it survives an SSH/laptop disconnect (see the README notes):
#   tmux new -s hera
#   bash scripts/cuda_workflow/run_training.sh 2>&1 | tee run_console.log
#   #  Ctrl-b  then  d   to detach  ·  tmux attach -t hera   to come back
#
# NOTE: WSL keeps running only while the Windows workstation stays powered & awake.
#       Set Windows power plan to "never sleep" (plugged in) before leaving.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
MODEL_ID="qwen3-8b"
OUT="models/baseline-lora"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
REPORT_DIR="training_reports/${TS}_${MODEL_ID}"

echo "================ [1/5] Sanity checks ================"
uv run python - <<'PY'
import sys
import transformers
from packaging import version
v = transformers.__version__
print("transformers:", v)
if version.parse(v) < version.parse("4.51.0"):
    sys.exit("ERROR: Qwen3 requires transformers >= 4.51.0 — run: uv add 'transformers>=4.51' && uv sync --extra train")
import torch
assert torch.cuda.is_available(), "ERROR: no CUDA GPU visible in this (WSL) environment"
print("GPU:", torch.cuda.get_device_name(0),
      f"| {torch.cuda.get_device_properties(0).total_memory/1e9:.1f} GB")
PY

echo "================ [2/5] Dry-run (validate data + config) ================"
uv run python -m src.baseline.finetune --model-id "$MODEL_ID" --dry-run

echo "================ [3/5] Training (Qwen3-8B, non-thinking) ================"
echo ">>> First run downloads ~16 GB of weights from HF, then trains. Watch the FIRST"
echo ">>> optimizer step succeed (no OOM) before walking away."
uv run python -m src.baseline.finetune \
    --model-id "$MODEL_ID" \
    --config configs/training.yaml \
    --output-dir "$OUT"

echo "================ [4/5] Training recap ================"
mkdir -p "$REPORT_DIR"
uv run python scripts/cuda_workflow/training_recap.py --out "$REPORT_DIR/recap.md"

echo "================ [5/5] Stage adapter + recap on git ================"
if command -v git-lfs >/dev/null 2>&1; then
    git lfs install --local
    git lfs track "*.safetensors" >/dev/null
    cp "$OUT/adapter_model.safetensors" "$OUT/adapter_config.json" "$REPORT_DIR/" 2>/dev/null || \
        echo "(adapter files not found in $OUT — skipping copy)"
    git add .gitattributes "$REPORT_DIR"
    git commit -m "Fine-tune ${MODEL_ID} @ ${TS} — adapter (LFS) + recap" || echo "(nothing to commit)"
    echo ">>> Committed. Review, then PUSH yourself:   git push"
else
    echo ">>> git-lfs not installed — committing the RECAP only (weights stay local in $OUT)."
    echo ">>> For the weights, either:  sudo apt-get install git-lfs  then re-run step 5,"
    echo ">>>                         or push the adapter to the HF Hub (recommended for model weights)."
    git add "$REPORT_DIR"
    git commit -m "Fine-tune ${MODEL_ID} @ ${TS} — recap" || echo "(nothing to commit)"
    echo ">>> Committed recap. PUSH yourself:   git push"
fi

echo "================ DONE ================"
