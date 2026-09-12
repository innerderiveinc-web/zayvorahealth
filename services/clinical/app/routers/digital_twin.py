from __future__ import annotations

import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.engines.digital_twin import (
    build_digital_twin_state,
    compute_mizaj_trajectory,
    simulate_treatment_projection,
)
from app.models.clinical import Encounter, MizajAssessment, Patient

router = APIRouter(prefix="/api/v1/patients", tags=["digital-twin"])


class DigitalTwinSimulationRequest(BaseModel):
    dominant_humor: str = Field(default="Dam", pattern="^(Dam|Safra|Balgham|Sauda)$")
    treatment_modalities: list[str] = Field(default_factory=lambda: ["Ilaj bil-Dawa", "Ilaj bil-Ghiza"])
    weeks: int = Field(default=4, ge=2, le=12)


def _get_patient_or_404(patient_id: uuid.UUID, organization_id: str, db: Session) -> Patient:
    patient = db.execute(
        select(Patient).where(Patient.id == patient_id, Patient.organization_id == organization_id)
    ).scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


def _assemble_twin(patient: Patient, db: Session) -> dict[str, Any]:
    # Fetch latest encounter with vitals if available
    latest_enc = db.execute(
        select(Encounter)
        .where(Encounter.patient_id == patient.id, Encounter.organization_id == patient.organization_id)
        .order_by(Encounter.started_at.desc())
    ).scalars().first()

    vitals = latest_enc.vital_signs if latest_enc and latest_enc.vital_signs else {}

    # Fetch latest mizaj assessment
    latest_mizaj = db.execute(
        select(MizajAssessment)
        .where(MizajAssessment.patient_id == patient.id, MizajAssessment.organization_id == patient.organization_id)
        .order_by(MizajAssessment.created_at.desc())
    ).scalars().first()

    mizaj_data = {}
    if latest_mizaj:
        mizaj_data = {
            "primary_temperament": latest_mizaj.primary_temperament,
            "heat_cold_score": latest_mizaj.heat_cold_score,
            "wet_dry_score": latest_mizaj.wet_dry_score,
        }

    return build_digital_twin_state(
        patient_id=str(patient.id),
        vital_signs=vitals,
        mizaj_assessment=mizaj_data,
        active_diagnoses=[],
        lab_biomarkers={},
        age=patient.age,
    )


@router.get("/{patient_id}/digital-twin")
def get_patient_digital_twin(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    """Retrieves the physiological state vector and organ axis integrity matrix
    for the patient's Clinical Digital Twin."""
    patient = _get_patient_or_404(patient_id, user.organization_id, db)
    return _assemble_twin(patient, db)


@router.post("/{patient_id}/digital-twin/simulate")
def simulate_patient_trajectory(
    patient_id: uuid.UUID,
    payload: DigitalTwinSimulationRequest,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    """Simulates treatment trajectory, organ axis recovery, and Nujz (concoction) schedule
    over 2 to 12 weeks for predictive clinical scenario modeling."""
    patient = _get_patient_or_404(patient_id, user.organization_id, db)
    twin = _assemble_twin(patient, db)

    return simulate_treatment_projection(
        digital_twin=twin,
        dominant_humor=payload.dominant_humor,
        treatment_modalities=payload.treatment_modalities,
        weeks=payload.weeks,
    )


@router.get("/{patient_id}/digital-twin/trajectory")
def get_patient_mizaj_trajectory(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    """Calculates longitudinal Mizaj drift velocity and healing trend across
    all historical 10-Ajnas evaluations for the patient."""
    patient = _get_patient_or_404(patient_id, user.organization_id, db)

    records = db.execute(
        select(MizajAssessment)
        .where(MizajAssessment.patient_id == patient.id, MizajAssessment.organization_id == user.organization_id)
        .order_by(MizajAssessment.created_at.asc())
    ).scalars().all()

    history = []
    for r in records:
        history.append({
            "created_at": r.created_at.isoformat() if r.created_at else "",
            "mizaj_state": {
                "primary_temperament": r.primary_temperament,
                "heat_cold_deviation": r.heat_cold_score,
                "wet_dry_deviation": r.wet_dry_score,
                "drift_magnitude": round((r.heat_cold_score**2 + r.wet_dry_score**2) ** 0.5, 2),
            },
        })

    return compute_mizaj_trajectory(history)
