"""
Real Anthropic Messages API provider.

IMPORTANT: this class has not been exercised against the live Anthropic
API in this repository's own test suite or during this build session —
there is no ANTHROPIC_API_KEY available in the sandbox this was built in.
See docs/PHASE4-AI-CORE.md for exactly what that means and how to verify
this yourself (it's a much smaller gap to close than Phase 2's Neo4j one
— you likely already have an API key).

The code below follows the standard Anthropic Python SDK usage pattern
and was reviewed carefully, but "reviewed carefully" is not "tested" —
same honesty standard applied to graph/neo4j_repository.py in Phase 2.
"""
from __future__ import annotations

import anthropic


class AnthropicProvider:
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6", max_tokens: int = 2000):
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model
        self._max_tokens = max_tokens

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text_blocks = [block.text for block in response.content if block.type == "text"]
        return "\n".join(text_blocks)
