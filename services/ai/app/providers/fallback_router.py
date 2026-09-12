"""
Chained Fallback AI Router (Phase 16 - Model-Agnostic Runtime).

Ensures zero clinical downtime during cloud provider outages, API rate limits,
or network partitions by dynamically failing over through a prioritized chain
of providers: [Primary Cloud LLM -> Secondary LLM -> Local vLLM -> Deterministic Fallback].
"""
from __future__ import annotations

import logging
from typing import Any
from app.providers.base import AIProvider

logger = logging.getLogger(__name__)


class ChainedFallbackRouter:
    def __init__(self, providers: list[tuple[str, AIProvider] | AIProvider]):
        if not providers:
            raise ValueError("ChainedFallbackRouter requires at least one provider")
        normalized: list[tuple[str, AIProvider]] = []
        for p in providers:
            if isinstance(p, tuple):
                normalized.append(p)
            else:
                name = getattr(p, "name", p.__class__.__name__)
                normalized.append((str(name), p))
        self._providers = normalized
        self.last_used_provider_name: str | None = None
        self.degradation_logs: list[dict[str, Any]] = []

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        last_error = None
        self.degradation_logs.clear()

        for name, provider in self._providers:
            try:
                result = provider.generate(system_prompt=system_prompt, user_prompt=user_prompt)
                self.last_used_provider_name = name
                return result
            except Exception as exc:
                logger.warning("AI Provider '%s' failed: %s. Failing over to next provider.", name, exc)
                self.degradation_logs.append({
                    "provider": name,
                    "status": "failed",
                    "error": str(exc),
                })
                last_error = exc
                continue

        raise RuntimeError(
            f"All AI providers in fallback chain failed! Last error: {last_error}. "
            f"Providers attempted: {[name for name, _ in self._providers]}"
        )

