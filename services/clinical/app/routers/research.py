from __future__ import annotations

import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.models.clinical import Encounter, Patient, Prescription
from app.research.deidentifier import anonymize_patient_for_research, classify_therapeutic_outcome

router = APIRouter(prefix="/api/v1/research", tags=["research-cloud-rwe"])


class OutcomeClassificationRequest(BaseModel):
    baseline_severity_score: float = Field(gt=0, description="Baseline symptom severity scale 1-10 or 1-100")
    followup_severity_score: float = Field(ge=0, description="Post-treatment symptom severity scale")
    mizaj_equilibrium_restored: bool = Field(default=False)


@router.get("/patients/{patient_id}/deidentified")
def get_deidentified_research_record(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    """Exports patient clinical trajectory stripped of all 18 HIPAA/DISHA direct
    identifiers and mapped to relative study days for observational cohort studies."""
    patient = db.execute(
        select(Patient).where(Patient.id == patient_id, Patient.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    encounters = db.execute(
        select(Encounter)
        .where(Encounter.patient_id == patient.id, Encounter.organization_id == user.organization_id)
        .order_by(Encounter.started_at.asc())
    ).scalars().all()

    prescriptions = db.execute(
        select(Prescription)
        .where(Prescription.patient_id == patient.id, Prescription.organization_id == user.organization_id)
        .order_by(Prescription.created_at.asc())
    ).scalars().all()

    pat_dict = {
        "id": str(patient.id),
        "age": patient.age,
        "gender": patient.gender,
        "mizaj_temperament": patient.mizaj_temperament,
    }

    enc_dicts = [
        {
            "started_at": e.started_at.isoformat() if e.started_at else None,
            "encounter_type": e.encounter_type,
            "vital_signs": e.vital_signs,
            "chief_complaint": e.chief_complaint,
        }
        for e in encounters
    ]

    rx_dicts = [
        {
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "medication_name": p.medication_name,
            "dose": p.dose,
            "is_schedule_e1": False,
            "verified_mudabbar": True,
        }
        for p in prescriptions
    ]

    return anonymize_patient_for_research(
        patient=pat_dict,
        encounters=enc_dicts,
        prescriptions=rx_dicts,
    )


@router.post("/outcomes/classify")
def classify_outcome_endpoint(
    payload: OutcomeClassificationRequest,
    user: CurrentUser = Depends(require_permission("clinical_notes.read")),
):
    """Classifies patient response into validated Unani outcome categories
    (Kamil, Juz'i, Ghair Mu'athir, Intikas)."""
    try:
        return classify_therapeutic_outcome(
            baseline_severity_score=payload.baseline_severity_score,
            followup_severity_score=payload.followup_severity_score,
            mizaj_equilibrium_restored=payload.mizaj_equilibrium_restored,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
