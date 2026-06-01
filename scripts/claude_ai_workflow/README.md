# Training-set generation via Claude.ai (no API calls)

Manual but zero-cost workflow: you paste each batch prompt into a Claude.ai
**Project**, copy the JSON response into a file, then run the parser to merge
everything into the canonical training JSONL.

## Why this exists

The HERA fine-tune needs ~80–250 multi-turn (developer ↔ copilot) dialogues.
The default `scripts/build_training_set.py` uses the Anthropic API. This
alternative lets you produce the same data through the Claude.ai chat UI —
no key, no cost, and the conversation history doubles as your provenance trail.

## One-time setup

1. Open https://claude.ai → **Projects** → **New project**, name it
   `HERA training-data generator`.
2. In the project's **Instructions**, paste the entire content of
   [`system_prompt.md`](system_prompt.md). Save.
3. Optional: pin the project so you can find it quickly.

## Per-batch loop

For each batch listed in [`batches/`](batches/):

1. Open the project, start a **new chat**.
2. Paste the batch prompt verbatim (one file = one prompt).
3. Wait for Claude to produce the JSON. It will be a single object
   `{"dialogues": [...]}` containing 5 dialogues.
4. Copy Claude's response **only** (not your prompt). Save it as
   `responses/batch_NN.json` (same number as the batch).
5. Repeat for the next batch.

Tips:
- If Claude truncates near the end, type `continue` and append.
- If Claude wraps the JSON in ``` fences, leave them — the parser strips them.
- If Claude refuses to output one of the dialogues, just delete that one
  from the JSON and move on.

## Import into the training set

Once you have any number of `responses/batch_NN.json` files:

```bash
uv run --extra datagen python scripts/claude_ai_workflow/import_batches.py
```

This:
- Reads every file in `scripts/claude_ai_workflow/responses/`
- Strips code fences, parses, validates each dialogue against the schema
- Appends valid ones to `data/training/conversations.jsonl`
- Writes a report to `runs/claude_import_<ts>/transcript.jsonl`

Re-runs are idempotent — already-imported dialogues are skipped via
`(archetype_id, batch_id, idx)` deduplication.

## Recommended ramp

| Phase | Batches | Dialogues | Time |
|------|---------|-----------|------|
| Smoke test | 1   | 5   | 5 min |
| Minimum viable LoRA | 1–8  | 40   | 1h |
| Comfortable training set | 1–14 | ~70  | 2h |
| Full target | 1–14 + manual augmentation (20) | ~90 | 2h + 1h |

70 high-quality curated dialogues + 20 manual diverse ones outperforms 280
noisy synthetic ones for a small-LoRA fine-tune. Don't feel obligated to
hit 250 — finish J2 deliverables first, augment if there's time.
