"""Unit tests for the simulated developer — focus on the no-repeat behavior that
stops the harness from manufacturing conversation loops."""

from __future__ import annotations

from src.evaluation.simulator import simulate_answer

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
    assert "haven't pinned that down" in out


def test_stateless_call_is_backward_compatible():
    # used_keys omitted → legacy behavior: still returns the matching answer.
    out = simulate_answer(SCN, "What data do you store?")
    assert out == SCN["simulated_answers"]["data_collected"]


def test_no_simulated_answers_returns_safe_default():
    out = simulate_answer({}, "anything", set())
    assert "discuss what would help" in out
