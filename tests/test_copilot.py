"""Tests for the HERA Risk & Safety Copilot baseline."""

from unittest.mock import patch, MagicMock

from src.baseline.copilot import (
    build_system_prompt,
    check_ollama,
    chat_with_ollama,
    create_app,
    load_taxonomy,
)


# ---------------------------------------------------------------------------
# Taxonomy loading
# ---------------------------------------------------------------------------


def test_load_taxonomy():
    taxonomy = load_taxonomy()
    assert taxonomy["name"] == "HERA"
    assert len(taxonomy["pillars"]) == 7


def test_taxonomy_pillars_have_dimensions():
    taxonomy = load_taxonomy()
    for pillar in taxonomy["pillars"]:
        assert "id" in pillar
        assert "name" in pillar
        assert len(pillar["dimensions"]) > 0


def test_taxonomy_dimensions_have_reflection_questions():
    taxonomy = load_taxonomy()
    for pillar in taxonomy["pillars"]:
        for dim in pillar["dimensions"]:
            assert "id" in dim
            assert "name" in dim
            assert len(dim["reflection_questions"]) > 0


def test_taxonomy_has_38_dimensions():
    # Canonical count: 6+6+5+5+4+5+7 = 38. CLAUDE.md/README intro text
    # historically said "37" but the per-pillar breakdown sums to 38.
    taxonomy = load_taxonomy()
    total = sum(len(p["dimensions"]) for p in taxonomy["pillars"])
    assert total == 38


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------


def test_build_system_prompt_contains_all_pillars():
    taxonomy = load_taxonomy()
    prompt = build_system_prompt(taxonomy)
    for pillar in taxonomy["pillars"]:
        assert pillar["name"] in prompt


def test_build_system_prompt_contains_dimension_ids():
    taxonomy = load_taxonomy()
    prompt = build_system_prompt(taxonomy)
    for pillar in taxonomy["pillars"]:
        for dim in pillar["dimensions"]:
            assert dim["id"] in prompt


# ---------------------------------------------------------------------------
# Ollama interaction (mocked)
# ---------------------------------------------------------------------------


def test_check_ollama_connection_error():
    import requests

    with patch(
        "src.baseline.copilot.requests.get",
        side_effect=requests.ConnectionError("conn"),
    ):
        ok, msg = check_ollama()
    assert not ok


def test_check_ollama_model_found():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"models": [{"name": "mistral:7b-instruct-v0.3-q4_K_M"}]}
    with patch("src.baseline.copilot.requests.get", return_value=mock_resp):
        ok, msg = check_ollama()
    assert ok
    assert "Connected" in msg


def test_check_ollama_model_not_found():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"models": [{"name": "llama3:8b"}]}
    with patch("src.baseline.copilot.requests.get", return_value=mock_resp):
        ok, msg = check_ollama()
    assert not ok
    assert "not found" in msg


def test_chat_with_ollama_success():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"message": {"content": "Hello!"}}
    mock_resp.raise_for_status = MagicMock()
    with patch("src.baseline.copilot.requests.post", return_value=mock_resp):
        result = chat_with_ollama([{"role": "user", "content": "Hi"}])
    assert result == "Hello!"


def test_chat_with_ollama_connection_error():
    import requests

    with patch(
        "src.baseline.copilot.requests.post",
        side_effect=requests.ConnectionError("fail"),
    ):
        result = chat_with_ollama([{"role": "user", "content": "Hi"}])
    assert "Error" in result


def test_chat_with_ollama_timeout():
    import requests

    with patch(
        "src.baseline.copilot.requests.post",
        side_effect=requests.Timeout("timeout"),
    ):
        result = chat_with_ollama([{"role": "user", "content": "Hi"}])
    assert "timed out" in result


# ---------------------------------------------------------------------------
# Gradio app creation
# ---------------------------------------------------------------------------


def test_create_app_returns_blocks():
    import gradio as gr

    app = create_app()
    assert isinstance(app, gr.Blocks)
