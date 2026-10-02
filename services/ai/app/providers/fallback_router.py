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
    def __init__(
        self,
        providers: list[tuple[str, AIProvider] | AIProvider],
        deterministic_fallback: AIProvider | None = None
    ):
        if not providers and not deterministic_fallback:
            raise ValueError("ChainedFallbackRouter requires at least one provider")
        normalized: list[tuple[str, AIProvider]] = []
        for p in (providers or []):
            if isinstance(p, tuple):
                normalized.append(p)
            else:
                name = getattr(p, "name", p.__class__.__name__)
                normalized.append((str(name), p))
        self._providers = normalized
        self._deterministic_fallback = deterministic_fallback
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

        if self._deterministic_fallback is not None:
            fallback_name = getattr(self._deterministic_fallback, "name", "DeterministicSafeFallbackProvider")
            logger.warning("All AI providers failed. Invoking deterministic safe fallback provider '%s'.", fallback_name)
            self.degradation_logs.append({
                "provider": fallback_name,
                "status": "safe_fallback_activated",
                "prior_error": str(last_error),
            })
            self.last_used_provider_name = fallback_name
            return self._deterministic_fallback.generate(system_prompt=system_prompt, user_prompt=user_prompt)

        raise RuntimeError(
            f"All AI providers in fallback chain failed! Last error: {last_error}. "
            f"Providers attempted: {[name for name, _ in self._providers]}"
        )

