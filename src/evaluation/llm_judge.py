"""Depth & Actionability LLM-as-judge for HERA Copilot transcripts.

Two run modes:
- **API mode** (--mode api) → calls Anthropic Claude (needs ANTHROPIC_API_KEY).
- **Manual mode** (--mode manual) → emits one `judge_prompts/<scenario>_<approach>.md`
  per case, ready to paste into Claude.ai. The user pastes each prompt, saves the
  JSON response in `judge_responses/<scenario>_<approach>.json`, and re-runs this
  script with --mode import to consolidate the ratings.

Output: `runs/<ts>/judge_ratings.jsonl` with one row per (scenario, approach).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.utils.logging_config import (  # noqa: E402
    JsonlSink,
    configure_logging,
    load_dotenv,
    new_run_dir,
)

log = logging.getLogger("eval.judge")


JUDGE_SYSTEM = """You are an expert rater for the HERA Risk & Safety Copilot — a conversational AI helping mHealth app developers identify ethical and regulatory risks.

For each transcript you receive, score on two 1–5 scales:

**Depth** — how specifically did the copilot drill into the developer's actual app?
- 1 = entirely generic, copy-pastable to any health app
- 3 = some specifics (named features, regulations) but mostly templated
- 5 = laser-focused; questions and risks reference THIS developer's choices, data flows, target users, and the precise regulation/article that applies

**Actionability** — could a competent developer take the copilot's suggestions and implement them tomorrow?
- 1 = vague platitudes ("ensure compliance")
- 3 = directional advice ("do a DPIA")
- 5 = concrete recipes ("Implement a layered consent UI with a 1-paragraph summary + an expandable detail section; document the lawful basis under GDPR Art. 9(2)(a) in your privacy notice")

Output STRICTLY a single JSON object:

```json
{
  "depth": <int 1-5>,
  "depth_justification": "<1-2 sentences>",
  "actionability": <int 1-5>,
  "actionability_justification": "<1-2 sentences>",
  "salient_examples": ["<short snippets from the transcript that drove your scores>"]
}
```

No commentary, no markdown headers, just the JSON object.
"""


def build_user_prompt(scenario: dict, transcript: list[dict], approach: str) -> str:
    transcript_text = "\n\n".join(
        f"### {m['role'].upper()}\n{m['content']}" for m in transcript
    )
    return f"""APPROACH UNDER REVIEW: `{approach}`

SCENARIO ID: {scenario['id']}
APP DESCRIPTION: {scenario['app_description']}

DEVELOPER PERSONA: {scenario.get('developer_persona', 'n/a')}

EXPECTED HERA DIMENSIONS (gold standard): {', '.join(scenario['gold_standard']['relevant_dimensions'])}

TRANSCRIPT:
{transcript_text}

Now produce the JSON judgement object."""


# ---------------------------------------------------------------------------
# API mode
# ---------------------------------------------------------------------------


def call_claude_api(client, model: str, system: str, user: str) -> str:
    msg = client.messages.create(
        model=model,
        max_tokens=1500,
        temperature=0.2,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return msg.content[0].text


# ---------------------------------------------------------------------------
# Manual (Claude.ai) mode
# ---------------------------------------------------------------------------


def write_manual_prompts(cases: list[dict], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "INSTRUCTIONS.md").write_text(
        "# Manual judging via Claude.ai\n\n"
        "1. In Claude.ai, create a project `HERA judge` and paste\n"
        "   `src/evaluation/llm_judge_system_prompt.md` as its instructions.\n"
        "2. For each `<case>.md` file in this directory, open a new chat\n"
        "   in that project and paste the file's content.\n"
        "3. Copy the JSON response and save as `<same-name>.json` in\n"
        "   `judge_responses/`.\n"
        "4. When done, run:\n"
        "   `uv run python -m src.evaluation.llm_judge --mode import`\n",
        encoding="utf-8",
    )
    for case in cases:
        name = f"{case['scenario_id']}__{case['approach']}.md"
        (out_dir / name).write_text(case["prompt"], encoding="utf-8")


def import_manual_responses(in_dir: Path, sink: JsonlSink) -> int:
    n = 0
    for p in sorted(in_dir.glob("*.json")):
        scenario_id, approach = p.stem.split("__", 1)
        try:
            payload = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            log.warning("%s: parse failed (%s)", p.name, exc)
            continue
        sink.write({"scenario_id": scenario_id, "approach": approach, "judgement": payload,
                    "source": "manual-claude-ai"})
        n += 1
    return n


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", choices=["api", "manual", "import"], default="manual")
    ap.add_argument("--results-glob",
                    default="runs/eval_*/results.jsonl",
                    help="Glob to discover results.jsonl files to judge")
    ap.add_argument("--model", default="claude-opus-4-7",
                    help="(api mode) Anthropic model id")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args(argv)

    run_dir = new_run_dir(prefix="judge")
    configure_logging(run_dir)
    load_dotenv()

    # Save system prompt next to the cases for convenience
    sys_prompt_path = REPO_ROOT / "src/evaluation/llm_judge_system_prompt.md"
    if not sys_prompt_path.exists():
        sys_prompt_path.write_text(JUDGE_SYSTEM, encoding="utf-8")

    out_jsonl = run_dir / "judge_ratings.jsonl"
    sink = JsonlSink(out_jsonl)

    if args.mode == "import":
        in_dir = REPO_ROOT / "data/evaluation/judge_responses"
        if not in_dir.exists():
            log.error("No judge_responses directory at %s", in_dir)
            return 1
        n = import_manual_responses(in_dir, sink)
        log.info("Imported %d manual ratings → %s", n, out_jsonl.relative_to(REPO_ROOT))
        return 0

    # Gather cases from the matching results.jsonl files
    cases: list[dict] = []
    for results in sorted(REPO_ROOT.glob(args.results_glob)):
        approach_tag = results.parent.name  # e.g. eval_rag_20260601T... → approach inferred
        # Extract approach from prefix `eval_<approach>_<ts>_<short>`
        approach = approach_tag.split("_", 2)[1] if approach_tag.startswith("eval_") else "unknown"
        for raw in results.read_text(encoding="utf-8").splitlines():
            if not raw.strip():
                continue
            row = json.loads(raw)
            if "transcript" not in row:
                continue
            scenarios_path = REPO_ROOT / "data/evaluation/scenarios.json"
            scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))
            scn_by_id = {s["id"]: s for s in scenarios}
            scn = scn_by_id.get(row["scenario_id"])
            if not scn:
                continue
            cases.append({
                "scenario_id": row["scenario_id"],
                "approach": approach,
                "prompt": build_user_prompt(scn, row["transcript"], approach),
            })

    if args.limit:
        cases = cases[: args.limit]
    log.info("Discovered %d (scenario × approach) cases to judge", len(cases))

    if args.mode == "manual":
        out_dir = REPO_ROOT / "data/evaluation/judge_prompts"
        write_manual_prompts(cases, out_dir)
        log.info("Wrote %d manual prompts to %s", len(cases), out_dir.relative_to(REPO_ROOT))
        return 0

    # API mode
    try:
        from anthropic import Anthropic
    except ImportError:
        log.error("anthropic not installed. Run: uv sync --extra datagen")
        return 2
    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("ANTHROPIC_API_KEY missing. Copy .env.example to .env.")
        return 2
    client = Anthropic()

    for i, case in enumerate(cases, 1):
        t0 = time.time()
        try:
            raw = call_claude_api(client, args.model, JUDGE_SYSTEM, case["prompt"])
        except Exception as exc:
            log.warning("[%d/%d] API error on %s/%s: %s",
                        i, len(cases), case["scenario_id"], case["approach"], exc)
            time.sleep(2.0)
            continue
        try:
            judgement = json.loads(raw.strip().lstrip("`json\n").rstrip("`"))
        except json.JSONDecodeError as exc:
            log.warning("[%d/%d] JSON parse failed on %s/%s: %s",
                        i, len(cases), case["scenario_id"], case["approach"], exc)
            continue
        sink.write({
            "scenario_id": case["scenario_id"],
            "approach": case["approach"],
            "judgement": judgement,
            "source": f"anthropic-{args.model}",
            "elapsed_s": time.time() - t0,
        })
        log.info("[%d/%d] %s/%s → depth=%d action=%d (%.1fs)",
                 i, len(cases), case["scenario_id"], case["approach"],
                 judgement.get("depth", 0), judgement.get("actionability", 0),
                 time.time() - t0)

    sink.close()
    log.info("Done. Ratings → %s", out_jsonl.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
