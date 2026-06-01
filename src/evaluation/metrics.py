"""Pure-function metrics for comparing one approach against a scenario's gold standard.

Each metric takes:
- `scenario`: one scenario dict from data/evaluation/scenarios.json
- `transcript`: list[dict] in the same shape as OpenAI messages

…and returns a float (or a small dict) that the runner aggregates.

All metrics are deterministic, stdlib-only, and unit-testable on golden inputs.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any

# Pattern matching HERA dimension IDs like P1.D2 or [P7.D11]
DIM_RE = re.compile(r"\bP(\d)\.D(\d+)\b")
RISK_HINT_RE = re.compile(r"\b(risk|issue|concern|problem|hazard|liability|exposure|gap)\b", re.IGNORECASE)
QUESTION_RE = re.compile(r"\?")


# ---------------------------------------------------------------------------
# Extractors (also reused by the LLM-judge)
# ---------------------------------------------------------------------------


def extract_dimensions(text: str) -> set[str]:
    """All HERA dimension IDs cited in `text`, normalized to 'Pn.Dm'."""
    return {f"P{a}.D{b}" for a, b in DIM_RE.findall(text)}


def extract_dimensions_from_transcript(messages: Iterable[dict]) -> set[str]:
    """Union of all dimensions cited by the assistant across the transcript."""
    found: set[str] = set()
    for m in messages:
        if m["role"] == "assistant":
            found |= extract_dimensions(m["content"])
    return found


def extract_assistant_questions(messages: Iterable[dict]) -> list[str]:
    """One-line entries: each assistant sentence ending with '?' becomes a question."""
    out: list[str] = []
    for m in messages:
        if m["role"] != "assistant":
            continue
        # Naive sentence split on . ! ? followed by space or EOL
        for sent in re.split(r"(?<=[.!?])\s+", m["content"]):
            sent = sent.strip()
            if QUESTION_RE.search(sent):
                out.append(sent)
    return out


def extract_named_risks(messages: Iterable[dict]) -> list[tuple[str, str]]:
    """List of (dim_id, sentence) for each assistant sentence that names a HERA dim
    AND uses risk-hint language. Returns the dim id alongside the originating sentence."""
    risks: list[tuple[str, str]] = []
    for m in messages:
        if m["role"] != "assistant":
            continue
        for sent in re.split(r"(?<=[.!?])\s+", m["content"]):
            dims = extract_dimensions(sent)
            if dims and RISK_HINT_RE.search(sent):
                for d in dims:
                    risks.append((d, sent.strip()))
    return risks


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------


def coverage(scenario: dict, transcript: list[dict]) -> dict:
    """Recall over relevant_dimensions: hit / total_expected."""
    expected: set[str] = set(scenario["gold_standard"]["relevant_dimensions"])
    found = extract_dimensions_from_transcript(transcript)
    hit = expected & found
    return {
        "found": sorted(found),
        "expected": sorted(expected),
        "hit": sorted(hit),
        "missed": sorted(expected - found),
        "extra": sorted(found - expected),  # off-target dims cited
        "recall": (len(hit) / len(expected)) if expected else 0.0,
    }


def relevance(scenario: dict, transcript: list[dict]) -> dict:
    """Precision-like: of all questions asked, how many touch a relevant dimension?"""
    relevant: set[str] = set(scenario["gold_standard"]["relevant_dimensions"])
    questions = extract_assistant_questions(transcript)
    n_total = len(questions)
    n_relevant = 0
    for q in questions:
        if extract_dimensions(q) & relevant:
            n_relevant += 1
    return {
        "n_total_questions": n_total,
        "n_relevant_questions": n_relevant,
        "precision": (n_relevant / n_total) if n_total else 0.0,
    }


def accuracy_f1(scenario: dict, transcript: list[dict]) -> dict:
    """F1 on identified risks vs gold standard, matched by HERA dimension id.

    True positive: copilot raised a risk in a dim where the gold standard also expected one.
    False positive: copilot raised a risk in a dim NOT in the gold standard's expected risks.
    False negative: gold standard expected a risk in a dim the copilot did not raise.
    """
    expected_dims: set[str] = {r["dimension"] for r in scenario["gold_standard"]["expected_risks"]}
    raised_dims: set[str] = {d for d, _ in extract_named_risks(transcript)}

    tp = len(expected_dims & raised_dims)
    fp = len(raised_dims - expected_dims)
    fn = len(expected_dims - raised_dims)

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def latency(turn_records: list[dict]) -> dict:
    """Mean / median / p95 latency over assistant turns."""
    lats = [t.get("latency_s", 0.0) for t in turn_records if t.get("latency_s")]
    if not lats:
        return {"mean": 0.0, "median": 0.0, "p95": 0.0, "n_turns": 0}
    lats_sorted = sorted(lats)
    p95_idx = max(0, int(0.95 * len(lats_sorted)) - 1)
    return {
        "mean": sum(lats) / len(lats),
        "median": lats_sorted[len(lats_sorted) // 2],
        "p95": lats_sorted[p95_idx],
        "n_turns": len(lats),
    }


def all_metrics(scenario: dict, transcript: list[dict], turn_records: list[dict]) -> dict:
    """One-shot helper called by the runner per scenario."""
    return {
        "coverage": coverage(scenario, transcript),
        "relevance": relevance(scenario, transcript),
        "accuracy_f1": accuracy_f1(scenario, transcript),
        "latency": latency(turn_records),
    }
