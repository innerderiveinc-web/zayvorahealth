"""
Client for services/knowledge. Same pattern as clinical_client.py.
"""
from __future__ import annotations

from typing import Protocol

try:
    import httpx
except ImportError:
    httpx = None


class KnowledgeClient(Protocol):
    def find_mufradat(self, *, organ_axis: str | None, auth_header: str) -> list[dict]: ...

    def get_rag_context(self, *, organ_axis: str | None, symptoms: list[str], temperament: str | None, auth_header: str) -> str: ...


class HttpKnowledgeClient:
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")

    def find_mufradat(self, *, organ_axis: str | None, auth_header: str) -> list[dict]:
        if httpx is None:
            raise RuntimeError("httpx is required for HttpKnowledgeClient")
        params = {"organ_axis": organ_axis} if organ_axis else {}
        with httpx.Client(timeout=10.0) as client:

            resp = client.get(
                f"{self._base_url}/api/v1/mufradat",
                params=params,
                headers={"Authorization": auth_header},
            )
            resp.raise_for_status()
            return resp.json()

    def get_rag_context(self, *, organ_axis: str | None, symptoms: list[str], temperament: str | None, auth_header: str) -> str:
        try:
            with httpx.Client(timeout=10.0) as client:
                resp = client.post(
                    f"{self._base_url}/api/v1/graph/rag-context",
                    json={"organ_axis": organ_axis, "symptoms": symptoms, "temperament": temperament},
                    headers={"Authorization": auth_header},
                )
                if resp.status_code == 200:
                    return resp.json().get("rag_context_text", "")
        except Exception:
            pass
        return ""


class FakeKnowledgeClient:
    def __init__(self, mufradat_by_axis: dict[str, list[dict]] | None = None, rag_context: str = ""):
        self._mufradat_by_axis = mufradat_by_axis or {}
        self._rag_context = rag_context

    def find_mufradat(self, *, organ_axis: str | None, auth_header: str) -> list[dict]:
        if organ_axis is None:
            return [m for entries in self._mufradat_by_axis.values() for m in entries]
        return self._mufradat_by_axis.get(organ_axis, [])

    def get_rag_context(self, *, organ_axis: str | None, symptoms: list[str], temperament: str | None, auth_header: str) -> str:
        return self._rag_context
