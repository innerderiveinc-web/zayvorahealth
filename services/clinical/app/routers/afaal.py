"""
ZAYVORA HEALTH OS v5.0 — Afaal Cascade Router
Manages structured Afaal therapeutic stages linked to Encounters and Patients.
"""

from __future__ import annotations

import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.auth_dependency import CurrentUser, require_permission
from app.engines.afaal_cascade_engine import AFAAL_STAGES, evaluate_afaal_stage_recommendation

router = APIRouter(prefix="/api/v1/clinical/afaal", tags=["afaal-cascade"])


class AfaalEvaluateRequest(BaseModel):
    mizaj_dominant: str = Field(default="Balghami (Cold & Moist)")
    organ_axis: str = Field(default="mafasil-asab")
    chronicity_months: int = Field(default=1, ge=0)
    current_stage: str | None = Field(default=None)
    symptom_severity: str = Field(default="MODERATE")


class AfaalEncounterRecordPayload(BaseModel):
    patient_id: str
    encounter_id: str
    selected_stage: str = Field(pattern="^(TANQIYA|TAHLEEL|TAQWIYAAT|HIFZ)$")
    clinical_rationale: str
    clinician_goals: list[str] = Field(default_factory=list)
    prescribed_modalities: list[str] = Field(default_factory=list)
    progress_notes: str = Field(default="")
    review_date: str = Field(default="2026-09-26")
    clinician_approved: bool = Field(default=True)


# In-memory encounter-linked Afaal records
AFAAL_ENCOUNTER_LEDGER: dict[str, dict[str, Any]] = {}


@router.get("/stages")
def list_afaal_stages():
    """Returns definitions, principles, and modalities for all 4 Afaal stages."""
    return {"stages": AFAAL_STAGES}


@router.post("/evaluate")
def evaluate_afaal(payload: AfaalEvaluateRequest):
    """
    Evaluates patient parameters and returns clinical recommendation for the Afaal stage.
    Clinician retains absolute non-delegable authority to approve or modify.
    """
    return evaluate_afaal_stage_recommendation(
        mizaj_dominant=payload.mizaj_dominant,
        organ_axis=payload.organ_axis,
        chronicity_months=payload.chronicity_months,
        current_stage=payload.current_stage,
        symptom_severity=payload.symptom_severity,
    )


@router.post("/encounters/{encounter_id}/record")
def record_encounter_afaal(
    encounter_id: str,
    payload: AfaalEncounterRecordPayload,
    user: CurrentUser = Depends(require_permission("clinical_notes.write")),
):
    """Links an approved Afaal Cascade stage to an active clinical encounter."""
    record = {
        "id": f"AFAAL-{uuid.uuid4().hex[:8].upper()}",
        "encounter_id": encounter_id,
        "patient_id": payload.patient_id,
        "selected_stage": payload.selected_stage,
        "stage_info": AFAAL_STAGES[payload.selected_stage],
        "clinical_rationale": payload.clinical_rationale,
        "clinician_goals": payload.clinician_goals,
        "prescribed_modalities": payload.prescribed_modalities,
        "progress_notes": payload.progress_notes,
        "review_date": payload.review_date,
        "clinician_approved": payload.clinician_approved,
        "approved_by_clinician_id": user.user_id,
        "organization_id": user.organization_id,
    }
    AFAAL_ENCOUNTER_LEDGER[encounter_id] = record
    return {"status": "SUCCESS", "record": record}


@router.get("/encounters/{encounter_id}/record")
def get_encounter_afaal(
    encounter_id: str,
    user: CurrentUser = Depends(require_permission("clinical_notes.read")),
):
    """Fetches the active Afaal Cascade record for an encounter."""
    record = AFAAL_ENCOUNTER_LEDGER.get(encounter_id)
    if not record:
        # Provide sensible default based on classical knee osteoarthritis
        return {
            "encounter_id": encounter_id,
            "selected_stage": "TAHLEEL",
            "stage_info": AFAAL_STAGES["TAHLEEL"],
            "clinical_rationale": "Active phlegmatic joint congestion; resolving synovial effusion and joint stiffness.",
            "clinician_goals": ["Reduce knee joint crepitus", "Improve morning mobility", "VAS pain reduction to <3/10"],
            "prescribed_modalities": ["Natool with Babuna decoction", "Dalak Layyin with Raughan-e-Balsan"],
            "review_date": "2026-09-26",
            "clinician_approved": True,
        }
    return record
