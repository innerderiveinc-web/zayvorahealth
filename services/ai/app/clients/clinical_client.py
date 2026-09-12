"""
Client for services/clinical. This is Phase 4's resolution of the
"deliberate simplification" noted in docs/PHASE3-THERAPEUTIC-CORE.md —
Hakeem Sahab is the orchestrator that now actually fetches patient
context from services/clinical, rather than trusting a caller to supply
it.

Two implementations: HttpClinicalClient (real, forwards the caller's
Authorization header so RBAC is enforced by services/clinical itself —
this service never gets broader access than the calling user has) and
FakeClinicalClient (tests).
"""
from __future__ import annotations

from typing import Protocol
from typing import Any

try:
    import httpx
except ImportError:
    httpx = None


class ClinicalClient(Protocol):
    def get_patient_safety_context(self, *, patient_id: str, auth_header: str) -> dict: ...


class HttpClinicalClient:
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")

    def get_patient_safety_context(self, *, patient_id: str, auth_header: str) -> dict:
        if httpx is None:
            raise RuntimeError("httpx is required for HttpClinicalClient")
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(
                f"{self._base_url}/api/v1/patients/{patient_id}",
                headers={"Authorization": auth_header},
            )

            resp.raise_for_status()
            patient = resp.json()
        return {
            "age": _age_from_dob(patient.get("date_of_birth")),
            "pregnancy_status": patient.get("pregnancy_status", "not_applicable"),
            "lactation_status": "no",
            "allergies": patient.get("allergies", []),
            "current_medications": patient.get("current_medications", []),
            "comorbidities": patient.get("comorbidities", []),
            "full_name": patient.get("full_name", ""),
        }


class FakeClinicalClient:
    def __init__(self, patients: dict[str, dict] | None = None):
        self._patients = patients or {}

    def get_patient_safety_context(self, *, patient_id: str, auth_header: str) -> dict:
        if patient_id not in self._patients:
            raise ValueError(f"Patient {patient_id} not found")
        return self._patients[patient_id]


def _age_from_dob(date_of_birth: str | None) -> int | None:
    if not date_of_birth:
        return None
    from datetime import date

    try:
        year, month, day = (int(p) for p in date_of_birth.split("-"))
        born = date(year, month, day)
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    except (ValueError, TypeError):
        return None
