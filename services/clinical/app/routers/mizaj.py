from __future__ import annotations

import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.engines.differential_engine import match_differential_considerations
from app.engines.mizaj_assessor import calculate_mizaj_assessment
from app.engines.organ_axis_engine import run_complete_organ_axis_analysis
from app.models.clinical import MizajAssessment, Patient
from app.schemas.clinical import (
    MizajAssessmentCreate,
    MizajAssessmentOut,
    OrganAxisAnalysisRequest,
    OrganAxisAnalysisResponse,
)

router = APIRouter(tags=["mizaj-and-diagnostics"])


class DifferentialQuery(BaseModel):
    chief_complaint: str = Field(min_length=1, max_length=2000)
    organ_axis: str | None = None
    dominant_mizaj: str | None = None


@router.post("/api/v1/patients/{patient_id}/mizaj-assessment", response_model=MizajAssessmentOut, status_code=201)
def create_mizaj_assessment(
    patient_id: uuid.UUID,
    payload: MizajAssessmentCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("clinical_notes.write")),
):
    # Verify patient belongs to user organization
    patient = db.execute(
        select(Patient).where(Patient.id == patient_id, Patient.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    result = calculate_mizaj_assessment(payload.answers)

    record = MizajAssessment(
        organization_id=user.organization_id,
        patient_id=patient_id,
        encounter_id=payload.encounter_id,
        assessed_by_user_id=user.user_id,
        primary_temperament=result["primary_temperament"],
        secondary_temperament=result["secondary_temperament"],
        distribution_percentages=result["distribution_percentages"],
        su_e_mizaj=result["su_e_mizaj"],
        dyscrasia_degree=result["dyscrasia_degree"],
        raw_scores=result["raw_scores"],
        answers_json=payload.answers,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/api/v1/patients/{patient_id}/mizaj-assessment/latest", response_model=MizajAssessmentOut)
def get_latest_mizaj_assessment(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("clinical_notes.read")),
):
    record = db.execute(
        select(MizajAssessment)
        .where(MizajAssessment.patient_id == patient_id, MizajAssessment.organization_id == user.organization_id)
        .order_by(MizajAssessment.created_at.desc())
    ).scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="No Mizaj assessment on file for patient")
    return record


@router.get("/api/v1/patients/{patient_id}/mizaj-assessment/history", response_model=list[MizajAssessmentOut])
def list_mizaj_assessments(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("clinical_notes.read")),
):
    records = db.execute(
        select(MizajAssessment)
        .where(MizajAssessment.patient_id == patient_id, MizajAssessment.organization_id == user.organization_id)
        .order_by(MizajAssessment.created_at.desc())
    ).scalars().all()
    return records


@router.post("/api/v1/diagnostics/differential")
def get_differential_diagnoses(
    query: DifferentialQuery,
    user: CurrentUser = Depends(require_permission("clinical_notes.read")),
):
    """Integrative differential diagnosis engine mapping symptoms to Unani Amraz & ICD-11."""
    return match_differential_considerations(
        chief_complaint=query.chief_complaint,
        organ_axis=query.organ_axis,
        dominant_mizaj=query.dominant_mizaj,
    )


@router.post("/api/v1/diagnostics/organ-axis/analyze", response_model=OrganAxisAnalysisResponse)
def analyze_organ_axis_endpoint(
    payload: OrganAxisAnalysisRequest,
    user: CurrentUser = Depends(require_permission("clinical_notes.read")),
):
    """Analyzes primary/secondary organ axes, detects reflex sympathies (Mushaarakat),
    deduces the Four Classical Causes (Asbab-e-Arba'a), and stages Dawr-e-Marad.
    """
    return run_complete_organ_axis_analysis(
        complaint=payload.complaint,
        associated_symptoms=payload.associated_symptoms,
        duration_days=payload.duration_days,
        symptom_acuity=payload.symptom_acuity,
        inflammatory_signs=payload.inflammatory_signs,
        temperament_context=payload.temperament_context,
    )

