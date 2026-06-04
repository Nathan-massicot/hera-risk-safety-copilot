"""Unit tests for the simulated developer — focus on the no-repeat behavior that
stops the harness from manufacturing conversation loops."""

from __future__ import annotations

from src.evaluation.simulator import (
    LexicalDeveloper,
    SemanticDeveloper,
    best_probe_key,
    simulate_answer,
)

SCN = {
    "simulated_answers": {
        "data_collected": "We store chat transcripts, mood scores and session timestamps.",
        "consent_flow": "There's a single 'I agree to the terms' checkbox at signup.",
        "regulatory_status": "We market it as a wellness app, not a medical device.",
    }
}


def test_matches_the_asked_topic():
    out = simulate_answer(SCN, "What data do you collect and store?", set())
    assert out == SCN["simulated_answers"]["data_collected"]


def test_never_serves_the_same_answer_twice():
    used: set[str] = set()
    a1 = simulate_answer(SCN, "What data do you collect and store?", used)
    a2 = simulate_answer(SCN, "Remind me — what data do you store?", used)
    assert a1 == SCN["simulated_answers"]["data_collected"]
    assert a2 != a1  # re-asking an answered topic must NOT replay the block
    assert "data_collected" in used


def test_advances_through_distinct_topics():
    used: set[str] = set()
    a1 = simulate_answer(SCN, "What data do you collect?", used)
    a2 = simulate_answer(SCN, "How do you obtain user consent?", used)
    a3 = simulate_answer(SCN, "Is it a regulated medical device or wellness app?", used)
    assert a1 == SCN["simulated_answers"]["data_collected"]
    assert a2 == SCN["simulated_answers"]["consent_flow"]
    assert a3 == SCN["simulated_answers"]["regulatory_status"]
    assert used == {"data_collected", "consent_flow", "regulatory_status"}


def test_exhausted_topics_nudge_toward_summary():
    used = {"data_collected", "consent_flow", "regulatory_status"}
    out = simulate_answer(SCN, "What data do you store?", used)
    assert "summary" in out.lower() or "covered" in out.lower()


def test_unscripted_question_returns_fallback_not_an_answer():
    out = simulate_answer(SCN, "What's your favourite colour scheme?", set())
    assert out not in SCN["simulated_answers"].values()
    assert "haven't worked that out" in out
    # The fallback must NOT invite a "what would good look like?" meta-loop.
    assert "good" not in out.lower()


def test_matching_tolerates_plurals_and_suffixes():
    # Focused single questions must still route to the right probe key even when the
    # keyword appears as a plural/suffixed form (the bug a one-question prompt exposed).
    keys = {"safety_validation", "accessibility", "consent_flow", "data_collected", "user_research"}
    assert best_probe_key("How do you avoid false positives and false negatives?", keys) == "safety_validation"
    assert best_probe_key("Is the app accessible for screen readers and low-literacy users?", keys) == "accessibility"
    assert best_probe_key("Is consent freely given and informed at signup?", keys) == "consent_flow"


def test_matching_short_token_does_not_overmatch():
    # "ai" must stay a strict word — it must NOT fire on "aid".
    assert best_probe_key("Do you provide first aid information to users?", {"ai_or_algorithm"}) is None


def test_runner_wraps_up_when_developer_runs_dry():
    from src.copilot_base import ChatTurn
    from src.evaluation.runner import run_scenario

    class DryCopilot:
        name = "stub"

        def reset(self):
            pass

        def chat(self, messages):
            # A question that matches no probe key → the developer always stalls.
            return ChatTurn(content="What's your favourite colour scheme this week?")

    scenario = {
        "id": "stub",
        "app_description": "An app.",
        "simulated_answers": {"data_collected": "We store logs."},
        "gold_standard": {"relevant_dimensions": ["P1.D1"], "expected_risks": []},
    }
    out = run_scenario(DryCopilot(), scenario, max_turns=10, request_report=False,
                       developer=LexicalDeveloper())
    asst = [m for m in out["transcript"] if m["role"] == "assistant"]
    # Early-stop after 3 consecutive stalls → far fewer than the 10 max turns.
    assert len(asst) <= 4


def test_semantic_developer_routes_dedups_and_thresholds():
    import numpy as np

    # Hand-crafted vectors: each question aligns with one fact; off-topic = zero vector.
    vec = {
        "FACT_consent": [1.0, 0.0, 0.0],
        "FACT_data": [0.0, 1.0, 0.0],
        "FACT_safety": [0.0, 0.0, 1.0],
        "How is consent obtained?": [0.9, 0.1, 0.0],
        "What data is stored?": [0.1, 0.9, 0.0],
        "Off-topic question": [0.0, 0.0, 0.0],
    }

    class FakeEmbedder:
        def encode(self, texts, normalize_embeddings=False):
            a = np.asarray([vec[t] for t in texts], dtype="float32")
            if normalize_embeddings:
                n = np.linalg.norm(a, axis=1, keepdims=True)
                a = a / np.clip(n, 1e-9, None)
            return a

    scenario = {
        "id": "t",
        "simulated_answers": {},
        "dev_facts": [
            {"dimension": "P1.D3", "fact": "FACT_consent"},
            {"dimension": "P2.D1", "fact": "FACT_data"},
            {"dimension": "P4.D2", "fact": "FACT_safety"},
        ],
    }
    dev = SemanticDeveloper(embedder=FakeEmbedder(), threshold=0.5)
    dev.reset()

    r1 = dev.answer(scenario, "How is consent obtained?")
    assert r1.matched and r1.text == "FACT_consent"
    # Re-asking the same topic must NOT replay it (dedup) → an unmatched non-answer.
    r2 = dev.answer(scenario, "How is consent obtained?")
    assert not r2.matched and r2.text != "FACT_consent"
    # A different topic still routes correctly.
    r3 = dev.answer(scenario, "What data is stored?")
    assert r3.matched and r3.text == "FACT_data"
    # Below-threshold (orthogonal) question → fallback, not a forced wrong answer.
    r4 = dev.answer(scenario, "Off-topic question")
    assert not r4.matched


def test_stateless_call_is_backward_compatible():
    # used_keys omitted → legacy behavior: still returns the matching answer.
    out = simulate_answer(SCN, "What data do you store?")
    assert out == SCN["simulated_answers"]["data_collected"]


def test_no_simulated_answers_returns_safe_default():
    out = simulate_answer({}, "anything", set())
    assert "discuss what would help" in out
