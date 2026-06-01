# Fine-tune workflow — external CUDA machine

The Mac M4 Pro can't fine-tune a 7B model in any reasonable time. The plan:
push the repo + data to a CUDA box over SSH, run training in tmux, rsync the
adapter back, then re-quantize for Ollama (Task #10).

## One-time setup on the CUDA box

```bash
# SSH in
ssh <user>@<cuda-host>

# Clone the repo (or pull if already there)
git clone https://github.com/Nathan-massicot/hera-risk-safety-copilot.git
cd hera-risk-safety-copilot

# Install uv if missing
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Install Python deps (this pulls torch+cuda variants automatically)
uv sync --extra train

# Optional sanity check
uv run python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

## Every training run — local Mac side

You generated `data/training/conversations.jsonl` via the Claude.ai workflow.
Now push it + the latest code to the CUDA box.

Set the host once per shell:

```bash
export CUDA_HOST=user@cuda-box.example.com
export CUDA_PATH=~/hera-risk-safety-copilot
```

Sync code + data + configs (excluding the bulky `.venv/`, `models/`, `runs/`,
`node_modules/`, …):

```bash
rsync -av --delete \
    --exclude='.venv' --exclude='__pycache__' --exclude='.pytest_cache' \
    --exclude='node_modules' --exclude='dist' \
    --exclude='runs/' --exclude='models/' \
    --exclude='document/' \
    --exclude='.git/' \
    ./ "$CUDA_HOST:$CUDA_PATH/"
```

(The `--delete` flag mirrors deletions; remove it if you want safer behavior.)

## Launch training — on the CUDA box

```bash
ssh "$CUDA_HOST"
cd "$CUDA_PATH"

# Optional: refresh deps if pyproject changed
uv sync --extra train

# Pick the model id matching your VRAM
# Use `nvidia-smi` first to confirm VRAM
nvidia-smi

# 7B QLoRA fits in 24 GB VRAM. 14B needs ~32 GB. Mistral 7B is the safe default.
# Override the 'selected' model with --model-id if you want.
tmux new -s finetune
uv run python -m src.baseline.finetune \
    --model-id mistral-7b-instruct-v0.3 \
    --config configs/training.yaml \
    --model-config configs/model.yaml \
    --output-dir models/baseline-lora \
    2>&1 | tee finetune.out
# Ctrl-B then D to detach
```

Reattach later: `tmux attach -t finetune`.

A 7B QLoRA on ~250 dialogues with the default 3 epochs typically takes
30–90 min on a single A100 / 4090 / RTX 6000. Watch `eval_loss` decrease in
the logs; should stabilize after epoch 2.

## Pull the adapter back — local Mac side

When training finishes, pull `models/baseline-lora/` back:

```bash
rsync -av "$CUDA_HOST:$CUDA_PATH/models/baseline-lora/" ./models/baseline-lora/
rsync -av "$CUDA_HOST:$CUDA_PATH/runs/finetune_*" ./runs/
```

You now have:
- `models/baseline-lora/adapter_model.safetensors`
- `models/baseline-lora/adapter_config.json`
- `models/baseline-lora/tokenizer*`
- `models/baseline-lora/training_state.json`
- `runs/finetune_<ts>/` — training log + config snapshot + git SHA

Both `models/` and `runs/` are gitignored — they stay local.

## Next step

Continue with Task #10: merge adapter + base model, convert to GGUF q4_K_M,
import into Ollama as `hera-baseline:latest`. See `scripts/ollama_workflow/`
(written at J4).

## Troubleshooting

- **OOM at load**: drop `per_device_train_batch_size` to 1 (already is) and
  `max_seq_length` from 4096 to 2048 in `configs/training.yaml`.
- **bitsandbytes errors**: usually a CUDA version mismatch. `pip show bitsandbytes`
  and check `bitsandbytes.cuda_version()`.
- **flash-attn not available**: optional, just remove `attn_implementation` if
  added; PyTorch SDPA will be used.
- **Slow training**: enable `gradient_checkpointing=true` (already on) and
  increase `gradient_accumulation_steps` to compensate batch size.
- **Eval metric stuck**: too few samples for `eval_steps=50`. Drop to 25 or
  set `eval_strategy=epoch`.
