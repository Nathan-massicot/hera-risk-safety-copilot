"""Unit tests for src/evaluation/metrics.py — pure-function golden inputs."""

from __future__ import annotations

from src.evaluation.metrics import (
    accuracy_f1,
    coverage,
    extract_assistant_questions,
    extract_dimensions,
    extract_named_risks,
    latency,
    relevance,
)


def test_extract_dimensions_simple():
    assert extract_dimensions("see [P1.D2] and P3.D11") == {"P1.D2", "P3.D11"}


def test_extract_dimensions_handles_garbage():
    assert extract_dimensions("no dims here, just text") == set()
    assert extract_dimensions("") == set()


def test_extract_assistant_questions_only_assistant():
    transcript = [
        {"role": "user", "content": "Is this safe?"},
        {"role": "assistant", "content": "Tell me about your data. What types? Got a DPO?"},
        {"role": "user", "content": "Mostly logs."},
        {"role": "assistant", "content": "Got it. Any GDPR mapping?"},
    ]
    qs = extract_assistant_questions(transcript)
    assert qs == ["What types?", "Got a DPO?", "Any GDPR mapping?"]


def test_extract_named_risks_requires_hint_word():
    transcript = [
        {"role": "assistant", "content": "Citing P2.D3 just for reference."},
        {"role": "assistant", "content": "There is a serious risk on [P1.D4]."},
        {"role": "assistant", "content": "I see a concern with [P7.D1] classification."},
    ]
    risks = extract_named_risks(transcript)
    assert sorted(r[0] for r in risks) == ["P1.D4", "P7.D1"]


def test_coverage_perfect_recall():
    scenario = {"gold_standard": {"relevant_dimensions": ["P1.D1", "P2.D3"]}}
    transcript = [{"role": "assistant", "content": "[P1.D1] and [P2.D3] matter here."}]
    out = coverage(scenario, transcript)
    assert out["recall"] == 1.0
    assert out["missed"] == []


def test_coverage_partial_recall_and_extras():
    scenario = {"gold_standard": {"relevant_dimensions": ["P1.D1", "P2.D3", "P7.D2"]}}
    transcript = [{"role": "assistant", "content": "[P1.D1] only, but also [P6.D5]"}]
    out = coverage(scenario, transcript)
    assert out["recall"] == 1 / 3
    assert out["missed"] == ["P2.D3", "P7.D2"]
    assert out["extra"] == ["P6.D5"]


def test_relevance_precision():
    scenario = {"gold_standard": {"relevant_dimensions": ["P1.D1", "P2.D3"]}}
    transcript = [
        {"role": "assistant",
         "content": "Are you tracking [P1.D1] adherence? Have you mapped [P2.D3] storage? What is your colour theme?"},
    ]
    out = relevance(scenario, transcript)
    assert out["n_total_questions"] == 3
    assert out["n_relevant_questions"] == 2
    assert abs(out["precision"] - 2 / 3) < 1e-9


def test_relevance_no_questions():
    out = relevance({"gold_standard": {"relevant_dimensions": ["P1.D1"]}}, [])
    assert out["n_total_questions"] == 0
    assert out["precision"] == 0.0


def test_accuracy_f1_perfect():
    scenario = {"gold_standard": {"expected_risks": [
        {"dimension": "P1.D1", "risk": "x", "severity": "high"},
        {"dimension": "P2.D3", "risk": "y", "severity": "low"},
    ]}}
    transcript = [
        {"role": "assistant", "content": "Real risk on [P1.D1]."},
        {"role": "assistant", "content": "Privacy concern on [P2.D3]."},
    ]
    out = accuracy_f1(scenario, transcript)
    assert out["tp"] == 2 and out["fp"] == 0 and out["fn"] == 0
    assert out["f1"] == 1.0


def test_accuracy_f1_partial_and_extras():
    scenario = {"gold_standard": {"expected_risks": [
        {"dimension": "P1.D1", "risk": "x", "severity": "high"},
        {"dimension": "P2.D3", "risk": "y", "severity": "low"},
    ]}}
    transcript = [
        {"role": "assistant", "content": "Risk on [P1.D1]."},
        {"role": "assistant", "content": "Hazard on [P6.D5]."},  # extra
    ]
    out = accuracy_f1(scenario, transcript)
    assert out["tp"] == 1 and out["fp"] == 1 and out["fn"] == 1
    # precision = 0.5, recall = 0.5, f1 = 0.5
    assert abs(out["f1"] - 0.5) < 1e-9


def test_latency_aggregates():
    out = latency([{"latency_s": 1.0}, {"latency_s": 2.0}, {"latency_s": 4.0}, {"latency_s": 5.0}])
    assert out["mean"] == 3.0
    assert out["n_turns"] == 4
    assert out["median"] == 4.0  # sorted[2] for n=4


def test_latency_empty():
    out = latency([])
    assert out["mean"] == 0.0
    assert out["n_turns"] == 0
