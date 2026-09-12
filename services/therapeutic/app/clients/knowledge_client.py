"""
Knowledge Client for services/therapeutic.

Enables the Therapeutic service to query live UPI/NFUM pharmacopoeia monographs,
statutory Schedule E(1) poison data, and evidence levels from services/knowledge.
Includes both HttpKnowledgeClient and LocalKnowledgeClient for test/standalone environments.
"""
from __future__ import annotations

from typing import Any, Protocol

import httpx


class KnowledgeClient(Protocol):
    def get_schedule_e1_substance(self, name: str, *, auth_header: str | None = None) -> dict[str, Any] | None: ...
    def get_monograph(self, name: str, *, auth_header: str | None = None) -> dict[str, Any] | None: ...
    def get_compound(self, name: str, *, auth_header: str | None = None) -> dict[str, Any] | None: ...


class HttpKnowledgeClient:
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")

    def get_schedule_e1_substance(self, name: str, *, auth_header: str | None = None) -> dict[str, Any] | None:
        headers = {"Authorization": auth_header} if auth_header else {}
        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.get(f"{self._base_url}/api/v1/pharmacopoeia/schedule-e1/{name}", headers=headers)
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        return None

    def get_monograph(self, name: str, *, auth_header: str | None = None) -> dict[str, Any] | None:
        headers = {"Authorization": auth_header} if auth_header else {}
        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.get(f"{self._base_url}/api/v1/pharmacopoeia/monographs/{name}", headers=headers)
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        return None

    def get_compound(self, name: str, *, auth_header: str | None = None) -> dict[str, Any] | None:
        headers = {"Authorization": auth_header} if auth_header else {}
        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.get(f"{self._base_url}/api/v1/pharmacopoeia/compounds/{name}", headers=headers)
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        return None


class LocalKnowledgeClient:
    """Standalone / fallback client using local pharmacopoeia datasets."""

    def __init__(self, schedule_e1_data: dict[str, Any] | None = None):
        self._schedule_e1 = schedule_e1_data or {}

    def get_schedule_e1_substance(self, name: str, *, auth_header: str | None = None) -> dict[str, Any] | None:
        target = name.lower()
        for k, v in self._schedule_e1.items():
            if target == k or target in v.get("synonyms", []):
                return v
        return None

    def get_monograph(self, name: str, *, auth_header: str | None = None) -> dict[str, Any] | None:
        return None

    def get_compound(self, name: str, *, auth_header: str | None = None) -> dict[str, Any] | None:
        return None
