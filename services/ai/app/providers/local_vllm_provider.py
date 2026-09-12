"""
Local / Self-Hosted LLM Provider (vLLM, Ollama, LocalAI).

Provides on-premise, HIPAA/GDPR-compliant offline AI runtime for hospital
networks and sovereign clinical deployments using standard OpenAI-compatible API.
"""
from __future__ import annotations

import json
import urllib.request
import urllib.error


class LocalVLLMProvider:
    def __init__(
        self,
        base_url: str = "http://localhost:8000/v1",
        model: str = "meta-llama/Meta-Llama-3-70B-Instruct",
        max_tokens: int = 2000,
        timeout: float = 45.0,
    ):
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._max_tokens = max_tokens
        self._timeout = timeout

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        url = f"{self._base_url}/chat/completions"
        payload = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                return body["choices"][0]["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Local vLLM Provider request failed: {e}") from e
