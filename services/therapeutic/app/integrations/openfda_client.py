"""
OpenFDA Drug Information Client for ZAYVORA Therapeutic Service.

Integrates with the public OpenFDA REST API for drug labels,
adverse events, and interaction checks. Results are cached in Redis.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
from typing import Any

import requests

logger = logging.getLogger(__name__)

OPENFDA_BASE = "https://api.fda.gov/drug"
CACHE_TTL = 3600  # 1 hour


def _cache_key(prefix: str, value: str) -> str:
    h = hashlib.md5(value.encode()).hexdigest()
    return f"openfda:{prefix}:{h}"


def _get_redis():
    try:
        import redis
        url = os.environ.get("ZAYVORA_THERAPEUTIC_REDIS_URL", "")
        return redis.from_url(url) if url else None
    except Exception:
        return None


def _cache_get(key: str) -> Any | None:
    r = _get_redis()
    if not r:
        return None
    try:
        val = r.get(key)
        return json.loads(val) if val else None
    except Exception:
        return None


def _cache_set(key: str, value: Any) -> None:
    r = _get_redis()
    if not r:
        return
    try:
        r.setex(key, CACHE_TTL, json.dumps(value))
    except Exception:
        pass


class OpenFDAClient:
    """Client for the OpenFDA drug endpoint."""

    def __init__(self, api_key: str = "") -> None:
        self.api_key = api_key or os.environ.get("OPENFDA_API_KEY", "")
        self.session = requests.Session()

    def _params(self, extra: dict | None = None) -> dict:
        p: dict = {}
        if self.api_key:
            p["api_key"] = self.api_key
        if extra:
            p.update(extra)
        return p

    def search_drug(self, query: str, limit: int = 10) -> list[dict]:
        """Search drug labels by brand or generic name."""
        cache_key = _cache_key("search", f"{query}:{limit}")
        cached = _cache_get(cache_key)
        if cached is not None:
            return cached

        try:
            resp = self.session.get(
                f"{OPENFDA_BASE}/label.json",
                params=self._params({"search": f"openfda.brand_name:{query}+openfda.generic_name:{query}", "limit": limit}),
                timeout=15,
            )
            if resp.status_code == 404:
                return []
            resp.raise_for_status()
            results = resp.json().get("results", [])
            _cache_set(cache_key, results)
            return results
        except Exception as exc:
            logger.error("OpenFDA search_drug failed: %s", exc)
            return []

    def get_drug_label(self, ndc_code: str) -> dict:
        """Fetch full drug label by NDC code."""
        cache_key = _cache_key("label", ndc_code)
        cached = _cache_get(cache_key)
        if cached is not None:
            return cached

        try:
            resp = self.session.get(
                f"{OPENFDA_BASE}/label.json",
                params=self._params({"search": f"openfda.package_ndc:{ndc_code}", "limit": 1}),
                timeout=15,
            )
            if resp.status_code == 404:
                return {}
            resp.raise_for_status()
            results = resp.json().get("results", [])
            result = results[0] if results else {}
            _cache_set(cache_key, result)
            return result
        except Exception as exc:
            logger.error("OpenFDA get_drug_label failed: %s", exc)
            return {}

    def get_adverse_events(self, drug_name: str, limit: int = 20) -> list[dict]:
        """Fetch adverse event reports for a drug name."""
        cache_key = _cache_key("adverse", f"{drug_name}:{limit}")
        cached = _cache_get(cache_key)
        if cached is not None:
            return cached

        try:
            resp = self.session.get(
                f"{OPENFDA_BASE}/event.json",
                params=self._params({"search": f"patient.drug.medicinalproduct:{drug_name}", "limit": limit}),
                timeout=15,
            )
            if resp.status_code == 404:
                return []
            resp.raise_for_status()
            results = resp.json().get("results", [])
            _cache_set(cache_key, results)
            return results
        except Exception as exc:
            logger.error("OpenFDA get_adverse_events failed: %s", exc)
            return []

    def check_drug_interactions(self, drug_names: list[str]) -> dict:
        """Basic interaction check — returns shared adverse event patterns."""
        if len(drug_names) < 2:
            return {"interactions": [], "note": "At least 2 drugs required."}
        query = "+".join(f"patient.drug.medicinalproduct:{n}" for n in drug_names)
        cache_key = _cache_key("interactions", query)
        cached = _cache_get(cache_key)
        if cached is not None:
            return cached

        try:
            resp = self.session.get(
                f"{OPENFDA_BASE}/event.json",
                params=self._params({"search": query, "count": "patient.reaction.reactionmeddrapt.exact", "limit": 20}),
                timeout=15,
            )
            if resp.status_code == 404:
                result: dict = {"interactions": [], "note": "No co-occurrence data found."}
                _cache_set(cache_key, result)
                return result
            resp.raise_for_status()
            results = resp.json().get("results", [])
            result = {"drug_names": drug_names, "interactions": results, "source": "OpenFDA co-occurrence analysis"}
            _cache_set(cache_key, result)
            return result
        except Exception as exc:
            logger.error("OpenFDA check_drug_interactions failed: %s", exc)
            return {"interactions": [], "error": str(exc)}
