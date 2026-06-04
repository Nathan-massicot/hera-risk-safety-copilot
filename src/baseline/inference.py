"""Prompt-only and fine-tuned baseline Copilots — both via Ollama HTTP.

The only difference between the two:
- prompt-only → model = `mistral:7b-instruct-v0.3-q4_K_M` (or whatever vanilla model)
- fine-tuned  → model = `hera-baseline:latest` (after Task #10 — adapter merged + GGUF q4)

Same code, different model id. Both implement `Copilot`.
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any

import requests

from src.copilot_base import ChatTurn, Copilot, default_system_prompt

log = logging.getLogger("copilot.baseline")

DEFAULT_OLLAMA_URL = os.environ.get("HERA_OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("HERA_OLLAMA_MODEL", "mistral:7b-instruct-v0.3-q4_K_M")


class OllamaCopilot:
    """Generic Ollama-backed Copilot used by prompt-only and fine-tuned approaches."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        ollama_url: str = DEFAULT_OLLAMA_URL,
        system_prompt: str | None = None,
        name: str | None = None,
        temperature: float = 0.7,
        num_predict: int = 1024,
        timeout_s: int = 120,
    ) -> None:
        self.model = model
        self.ollama_url = ollama_url.rstrip("/")
        self.system_prompt = system_prompt or default_system_prompt()
        self.name = name or f"ollama:{model}"
        self.temperature = temperature
        # Decoding knobs — env-overridable so we can tune anti-repetition without
        # editing code. Defaults match the hera-baseline Modelfile.
        self.num_predict = int(os.environ.get("HERA_NUM_PREDICT", num_predict))
        self.top_p = float(os.environ.get("HERA_TOP_P", "0.8"))
        self.top_k = int(os.environ.get("HERA_TOP_K", "20"))
        self.repeat_penalty = float(os.environ.get("HERA_REPEAT_PENALTY", "1.3"))
        self.repeat_last_n = int(os.environ.get("HERA_REPEAT_LAST_N", "64"))
        self.timeout_s = timeout_s

    def chat(self, messages: list[dict]) -> ChatTurn:
        # Prepend system prompt if not already present
        if not messages or messages[0].get("role") != "system":
            messages = [{"role": "system", "content": self.system_prompt}, *messages]

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            # Disable Qwen3's <think> block so transcripts are clean & comparable
            # (no-op for non-thinking models). Sampling matches the fine-tuned
            # hera-baseline so the ONLY difference across approaches is the
            # model/architecture, not the decoding params.
            "think": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.num_predict,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "repeat_penalty": self.repeat_penalty,
                "repeat_last_n": self.repeat_last_n,
            },
        }

        t0 = time.time()
        try:
            r = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=self.timeout_s,
            )
            r.raise_for_status()
            body = r.json()
        except requests.RequestException as exc:
            log.error("Ollama call failed: %s", exc)
            return ChatTurn(content=f"[Ollama error: {exc}]", latency_s=time.time() - t0)

        content = body.get("message", {}).get("content", "")
        return ChatTurn(
            content=content,
            latency_s=time.time() - t0,
            prompt_tokens=body.get("prompt_eval_count", 0),
            completion_tokens=body.get("eval_count", 0),
        )

    def reset(self) -> None:
        # Stateless; nothing to reset.
        return None


# Convenience factories used by the eval runner
def prompt_only_copilot() -> OllamaCopilot:
    return OllamaCopilot(
        model=os.environ.get("HERA_PROMPT_ONLY_MODEL", "qwen3:8b"),
        name="prompt-only",
    )


def fine_tuned_copilot() -> OllamaCopilot:
    return OllamaCopilot(
        model=os.environ.get("HERA_FINETUNED_MODEL", "hera-baseline:latest"),
        name="fine-tuned",
    )
