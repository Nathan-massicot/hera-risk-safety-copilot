# Adapter → Ollama-ready local model

End-to-end: take the LoRA adapter trained on the CUDA box and turn it into a
local `hera-baseline:latest` tag in Ollama, suitable for both the eval runner
and the web app demo.

```
                                          ┌──────────────────┐
                                          │ hera-baseline:   │
  models/baseline-lora/                    │   latest         │
  (LoRA adapter from CUDA)                 │ in Ollama        │
       │                                   └──────────────────┘
       │                                            ▲
       ▼                                            │
  merge_adapter.py        convert         quantize  │   ollama create
  ┌─────────────┐  ────►  ┌─────────────┐ ────►   ┌─┴────────────┐
  │ merged HF   │         │ gguf f16    │         │ gguf q4_K_M  │
  └─────────────┘         └─────────────┘         └──────────────┘
```

## Prerequisites

- LoRA adapter at `models/baseline-lora/` — synced back from the CUDA box.
  Should contain `adapter_model.safetensors`, `adapter_config.json`,
  `training_state.json`, and tokenizer files.
- Ollama running locally (`ollama serve`).
- llama.cpp built locally for the GGUF tooling:
  ```bash
  git clone https://github.com/ggerganov/llama.cpp ~/llama.cpp
  cd ~/llama.cpp
  cmake -B build -DGGML_METAL=ON         # Apple Silicon
  cmake --build build --config Release
  pip install -r requirements.txt        # for convert_hf_to_gguf.py
  ```

## Step 1 — Merge adapter into base weights

```bash
uv sync --extra train
uv run --extra train python scripts/ollama_workflow/merge_adapter.py \
    --adapter models/baseline-lora \
    --out    models/baseline-merged
```

The base model id is read from `models/baseline-lora/training_state.json`
(written by `src/baseline/finetune.py` at training time). Override with
`--base-model mistralai/Mistral-7B-Instruct-v0.3` if needed.

Result: `models/baseline-merged/` contains a full HF-format checkpoint, ~14 GB
in bf16.

## Step 2 — Convert HF → GGUF f16

```bash
python ~/llama.cpp/convert_hf_to_gguf.py \
    models/baseline-merged \
    --outtype f16 \
    --outfile models/baseline-merged/hera-baseline.f16.gguf
```

## Step 3 — Quantize to q4_K_M

```bash
~/llama.cpp/build/bin/llama-quantize \
    models/baseline-merged/hera-baseline.f16.gguf \
    models/baseline-merged/hera-baseline.q4_K_M.gguf \
    q4_K_M
```

The q4_K_M file should be ~4-5 GB for a 7B base, ~9-10 GB for a 14B.

## Step 4 — Build Modelfile + import into Ollama

```bash
uv run python scripts/ollama_workflow/build_modelfile.py \
    --merged-dir models/baseline-merged \
    --gguf-name  hera-baseline.q4_K_M.gguf

cd models/baseline-merged
ollama create hera-baseline -f Modelfile

# Sanity check
ollama run hera-baseline "I am building a teleconsultation app for mental health. What HERA risks should I think about first?"
```

You should see the model cite HERA dimension IDs (e.g., `[P3.D3]`) — a sign the
fine-tune internalized the taxonomy.

## Step 5 — Switch the eval + web app to the fine-tuned model

```bash
# For the eval runner — already uses HERA_OLLAMA_MODEL via env
HERA_FINETUNED_MODEL=hera-baseline:latest \
    uv run --extra rag python -m src.evaluation.runner --approach fine-tuned --limit 3

# For the web app — set in .env
echo "HERA_OLLAMA_MODEL=hera-baseline:latest" >> .env
```

## Troubleshooting

- **convert_hf_to_gguf.py errors on tokenizer**: usually means the tokenizer
  files are missing from the merged dir. Re-run `merge_adapter.py` — it copies
  the tokenizer.
- **llama-quantize: unknown ftype 'q4_K_M'**: build llama.cpp from a recent
  commit (post-Sept 2024).
- **Ollama: '*.gguf' not found**: paths in the Modelfile are *relative to the
  Modelfile's directory*. The template uses `./{GGUF_FILENAME}` and assumes
  you `cd models/baseline-merged` before `ollama create`.
- **Smoke test gives generic answers**: the fine-tune may not have converged.
  Check `runs/finetune_<ts>/run.log` — `eval_loss` should be < 1.5 by epoch 3.
  If not, increase epochs or check training data quality.
