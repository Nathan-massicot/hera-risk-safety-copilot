"""Smoke tests for RLM agent JSON parsing (no Ollama call required)."""

from __future__ import annotations

from src.rlm.agents import _argmax_combined, _get_score, extract_json


def test_extract_json_unfenced():
    payload = '{"a": 1, "b": [2, 3]}'
    assert extract_json(payload) == {"a": 1, "b": [2, 3]}


def test_extract_json_fenced():
    payload = '```json\n{"x": "y"}\n```'
    assert extract_json(payload) == {"x": "y"}


def test_extract_json_fenced_no_lang():
    payload = '```\n{"k": 7}\n```'
    assert extract_json(payload) == {"k": 7}


def test_get_score_lookup():
    scores = [
        {"index": 0, "relevance": 4, "depth": 3, "novelty": 2},
        {"index": 1, "relevance": 5, "depth": 5, "novelty": 5},
    ]
    assert _get_score(scores, 1, "relevance") == 5
    assert _get_score(scores, 0, "novelty") == 2
    assert _get_score(scores, 9, "relevance") == 0


def test_argmax_combined_picks_highest_sum():
    scores = [
        {"index": 0, "relevance": 4, "depth": 4, "novelty": 4},  # sum 12
        {"index": 1, "relevance": 5, "depth": 5, "novelty": 5},  # sum 15  ← best
        {"index": 2, "relevance": 3, "depth": 3, "novelty": 3},  # sum 9
    ]
    assert _argmax_combined(scores) == 1


def test_argmax_combined_handles_missing_fields():
    scores = [
        {"index": 0, "relevance": 5},
        {"index": 1, "relevance": 4, "depth": 4, "novelty": 4},  # sum 12
    ]
    assert _argmax_combined(scores) == 1
