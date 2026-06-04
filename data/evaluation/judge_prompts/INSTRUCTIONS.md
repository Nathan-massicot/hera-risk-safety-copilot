# Manual judging via Claude.ai

1. In Claude.ai, create a project `HERA judge` and paste
   `src/evaluation/llm_judge_system_prompt.md` as its instructions.
2. For each `<case>.md` file in this directory, open a new chat
   in that project and paste the file's content.
3. Copy the JSON response and save as `<same-name>.json` in
   `judge_responses/`.
4. When done, run:
   `uv run python -m src.evaluation.llm_judge --mode import`
