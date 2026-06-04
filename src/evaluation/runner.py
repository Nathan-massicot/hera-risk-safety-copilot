"""Run one Copilot against the 25 evaluation scenarios.

For each scenario:
1. Start a fresh conversation with the app_description as the user's opening message
2. Loop up to `max_turns`: copilot responds, simulator returns the closest canned answer
3. Compute auto-metrics (coverage / relevance / F1 / latency)
4. Append the scenario result to `runs/<ts>/results.jsonl`

Usage:
    uv run --extra rag python -m src.evaluation.runner --approach prompt-only
    uv run --extra rag python -m src.evaluation.runner --approach rag --limit 5
    uv run --extra rag python -m src.evaluation.runner --approach fine-tuned --max-turns 8
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.copilot_base import Copilot  # noqa: E402
from src.evaluation.metrics import all_metrics  # noqa: E402
from src.evaluation.simulator import simulate_answer  # noqa: E402
from src.utils.logging_config import (  # noqa: E402
    JsonlSink,
    configure_logging,
    load_dotenv,
    new_run_dir,
)

log = logging.getLogger("eval.runner")

SCENARIOS_PATH = REPO_ROOT / "data/evaluation/scenarios.json"


# ---------------------------------------------------------------------------
# Approach factories — kept here so the runner has zero hard dependency on each
# ---------------------------------------------------------------------------


def build_copilot(approach: str) -> Copilot:
    if approach == "prompt-only":
        from src.baseline.inference import prompt_only_copilot
        return prompt_only_copilot()
    if approach == "fine-tuned":
        from src.baseline.inference import fine_tuned_copilot
        return fine_tuned_copilot()
    if approach == "rag":
        from src.rag.copilot import RAGCopilot
        return RAGCopilot()
    if approach == "rlm":
        from src.rlm.copilot import RLMCopilot  # written at J4
        return RLMCopilot()
    raise SystemExit(f"Unknown approach: {approach}")


# ---------------------------------------------------------------------------
# Single-scenario driver
# ---------------------------------------------------------------------------


REPORT_REQUEST = (
    "Thanks for the conversation. Could you produce a brief structured risk "
    "report now? Use HERA dimension IDs (e.g. [P1.D2]) and group risks by "
    "severity. End the report with a list of dimensions you didn't get to cover."
)


def run_scenario(
    copilot: Copilot,
    scenario: dict,
    max_turns: int,
    request_report: bool,
) -> dict:
    """Simulate one developer ↔ copilot conversation."""
    copilot.reset() if hasattr(copilot, "reset") else None

    messages: list[dict] = [
        {"role": "user", "content": scenario["app_description"]},
    ]
    turn_records: list[dict] = []
    # Track which probe categories the simulated developer has already answered so we
    # never replay the same canned answer (otherwise the harness manufactures looping).
    used_keys: set[str] = set()

    for turn in range(max_turns):
        chat = copilot.chat(messages)
        messages.append({"role": "assistant", "content": chat.content})
        turn_records.append({
            "turn": turn,
            "latency_s": chat.latency_s,
            "prompt_tokens": chat.prompt_tokens,
            "completion_tokens": chat.completion_tokens,
            "retrieved_n": chat.extra.get("retrieved_n", 0) if chat.extra else 0,
        })

        # If the copilot doesn't end with a question, we still continue but
        # the simulator may give a generic answer.
        dev_answer = simulate_answer(scenario, chat.content, used_keys)
        messages.append({"role": "user", "content": dev_answer})

    if request_report:
        messages.append({"role": "user", "content": REPORT_REQUEST})
        # Prefer a dedicated synthesis path (RLM bypasses its question loop here to
        # actually write the report); fall back to a normal turn otherwise.
        final_report = getattr(copilot, "final_report", None)
        report_turn = final_report(messages) if callable(final_report) else copilot.chat(messages)
        messages.append({"role": "assistant", "content": report_turn.content})
        turn_records.append({
            "turn": max_turns,
            "latency_s": report_turn.latency_s,
            "prompt_tokens": report_turn.prompt_tokens,
            "completion_tokens": report_turn.completion_tokens,
            "is_report": True,
        })

    metrics = all_metrics(scenario, messages, turn_records)
    return {
        "scenario_id": scenario["id"],
        "transcript": messages,
        "turn_records": turn_records,
        "metrics": metrics,
    }


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--approach", required=True,
                    choices=["prompt-only", "fine-tuned", "rag", "rlm"])
    ap.add_argument("--scenarios", type=Path, default=SCENARIOS_PATH)
    ap.add_argument("--limit", type=int, default=None,
                    help="Run only the first N scenarios (smoke testing)")
    ap.add_argument("--max-turns", type=int, default=10,
                    help="Max alternating turns per scenario (excluding the final report)")
    ap.add_argument("--no-report", action="store_true",
                    help="Skip the final 'produce a risk report' request")
    args = ap.parse_args(argv)

    run_dir = new_run_dir(prefix=f"eval_{args.approach}")
    configure_logging(run_dir)
    load_dotenv()

    log.info("Approach: %s", args.approach)
    copilot = build_copilot(args.approach)
    log.info("Copilot ready: %s", copilot.name)

    scenarios = json.loads(args.scenarios.read_text(encoding="utf-8"))
    if args.limit:
        scenarios = scenarios[: args.limit]
    log.info("Scenarios: %d", len(scenarios))

    results_path = run_dir / "results.jsonl"
    summary: list[dict] = []

    with JsonlSink(results_path) as sink:
        for i, scenario in enumerate(scenarios, 1):
            t0 = time.time()
            try:
                result = run_scenario(
                    copilot, scenario,
                    max_turns=args.max_turns,
                    request_report=not args.no_report,
                )
            except KeyboardInterrupt:
                log.warning("Interrupted on scenario %s", scenario["id"])
                raise
            except Exception as exc:
                log.exception("Scenario %s failed: %s", scenario["id"], exc)
                sink.write({"scenario_id": scenario["id"], "error": str(exc)})
                continue
            dt = time.time() - t0
            sink.write(result)

            m = result["metrics"]
            summary.append({
                "scenario_id": scenario["id"],
                "coverage_recall": m["coverage"]["recall"],
                "relevance_precision": m["relevance"]["precision"],
                "accuracy_f1": m["accuracy_f1"]["f1"],
                "latency_mean_s": m["latency"]["mean"],
                "elapsed_s": dt,
            })
            log.info(
                "[%d/%d] %s · cov=%.2f rel=%.2f f1=%.2f · %.1fs",
                i, len(scenarios), scenario["id"],
                m["coverage"]["recall"], m["relevance"]["precision"],
                m["accuracy_f1"]["f1"], dt,
            )

    # Aggregate summary
    def mean(key: str) -> float:
        vals = [s[key] for s in summary if s.get(key) is not None]
        return sum(vals) / len(vals) if vals else 0.0

    agg = {
        "approach": args.approach,
        "copilot_name": copilot.name,
        "n_scenarios": len(summary),
        "macro_coverage_recall": mean("coverage_recall"),
        "macro_relevance_precision": mean("relevance_precision"),
        "macro_accuracy_f1": mean("accuracy_f1"),
        "macro_latency_mean_s": mean("latency_mean_s"),
        "per_scenario": summary,
    }
    (run_dir / "summary.json").write_text(
        json.dumps(agg, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    log.info("\n=== Summary (%s) ===", args.approach)
    log.info("  coverage (macro recall)     %.3f", agg["macro_coverage_recall"])
    log.info("  relevance (macro precision) %.3f", agg["macro_relevance_precision"])
    log.info("  accuracy  (macro F1)        %.3f", agg["macro_accuracy_f1"])
    log.info("  latency   (macro mean s)    %.2f", agg["macro_latency_mean_s"])
    log.info("Results: %s", results_path.relative_to(REPO_ROOT))
    log.info("Summary: %s", (run_dir / "summary.json").relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
