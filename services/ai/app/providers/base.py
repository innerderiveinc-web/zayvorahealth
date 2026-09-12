"""
Model-agnostic AI provider interface (Master Build Prompt v4.0 §52:
"Never hard-code the application to a single model provider").

Two implementations:
- AnthropicProvider (providers/anthropic_provider.py) — real, calls the
  Anthropic Messages API. NOT exercised live in this repo's own test
  suite — see docs/PHASE4-AI-CORE.md for why (no API key available in the
  sandbox this was built in) and how to verify it yourself.
- ScriptedFakeProvider (providers/fake_provider.py) — deterministic,
  used only in tests, returns a pre-scripted response so orchestration
  logic (prompt assembly, response validation, storage) can be tested
  without hitting a real LLM.
"""
from __future__ import annotations

from typing import Protocol


class AIProvider(Protocol):
    def generate(self, *, system_prompt: str, user_prompt: str) -> str: ...
