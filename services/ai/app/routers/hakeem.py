from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.engines.hakeem_sahab import run_hakeem_consultation, run_hakeem_refinement
from app.engines.zape_personalization import run_zape_personalization
from app.models.ai import AiConsultation
from app.schemas.ai import (
    HakeemConsultOut,
    HakeemConsultRequest,
    HakeemRefineOut,
    HakeemRefineRequest,
    MarkReviewed,
    ZAPEPersonalizeRequest,
    ZAPEPersonalizeResponse,
)

router = APIRouter(prefix="/api/v1/hakeem", tags=["hakeem-sahab"])


def _clients(request: Request):
    return request.app.state.clinical_client, request.app.state.knowledge_client, request.app.state.ai_provider


@router.post("/consult", response_model=HakeemConsultOut, status_code=201)
def consult(
    payload: HakeemConsultRequest,
    request: Request,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("hakeem.consult")),
):
    clinical_client, knowledge_client, ai_provider = _clients(request)
    auth_header = request.headers.get("Authorization", "")

    try:
        result = run_hakeem_consultation(
            chief_complaint=payload.chief_complaint,
            organ_axis=payload.organ_axis,
            patient_id=str(payload.patient_id),
            auth_header=auth_header,
            clinical_client=clinical_client,
            knowledge_client=knowledge_client,
            ai_provider=ai_provider,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    record = AiConsultation(
        organization_id=user.organization_id,
        patient_id=payload.patient_id,
        requested_by_user_id=user.user_id,
        chief_complaint=payload.chief_complaint,
        organ_axis=payload.organ_axis or "",
        candidate_mufradat=result["candidateMufradat"],
        raw_response=result["rawResponse"],
        parsed_sections=result["sections"],
        is_valid=result["valid"],
        missing_sections=result["missingSections"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/consultations/{consultation_id}", response_model=HakeemConsultOut)
def get_consultation(
    consultation_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("hakeem.consult")),
):
    record = db.execute(
        select(AiConsultation).where(AiConsultation.id == consultation_id, AiConsultation.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Consultation not found")
    return record


@router.get("/consultations/by-patient/{patient_id}", response_model=list[HakeemConsultOut])
def list_consultations_for_patient(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("hakeem.consult")),
):
    records = db.execute(
        select(AiConsultation)
        .where(AiConsultation.patient_id == patient_id, AiConsultation.organization_id == user.organization_id)
        .order_by(AiConsultation.created_at.desc())
    ).scalars().all()
    return records


@router.post("/consultations/{consultation_id}/mark-reviewed", response_model=HakeemConsultOut)
def mark_reviewed(
    consultation_id: uuid.UUID,
    payload: MarkReviewed,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("hakeem.consult")),
):
    """§50 governance closing the loop: records that a clinician actually
    looked at this consultation, and optionally which Nuskha draft (if
    any) it led to — completing the Patient Data -> ... -> Clinician
    Decision -> Final Action chain."""
    record = db.execute(
        select(AiConsultation).where(AiConsultation.id == consultation_id, AiConsultation.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Consultation not found")
    record.reviewed_by_clinician = True
    if payload.converted_to_nuskha_draft_id:
        record.converted_to_nuskha_draft_id = payload.converted_to_nuskha_draft_id
    db.commit()
    db.refresh(record)
    return record


@router.post("/refine", response_model=HakeemRefineOut)
def refine_consultation(
    payload: HakeemRefineRequest,
    request: Request,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("hakeem.consult")),
):
    """Multi-turn Hakeem Sahab copilot refinement. Incorporates statutory clinician
    feedback, constraints, and critiques to re-evaluate the advisory consultation."""
    clinical_client, knowledge_client, ai_provider = _clients(request)
    auth_header = request.headers.get("Authorization", "")

    record = db.execute(
        select(AiConsultation).where(
            AiConsultation.id == payload.consultation_id,
            AiConsultation.organization_id == user.organization_id,
        )
    ).scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Consultation not found")

    result = run_hakeem_refinement(
        chief_complaint=record.chief_complaint,
        patient_id=str(record.patient_id),
        clinician_feedback=payload.clinician_feedback,
        previous_sections=record.parsed_sections or {},
        auth_header=auth_header,
        clinical_client=clinical_client,
        knowledge_client=knowledge_client,
        ai_provider=ai_provider,
    )

    return HakeemRefineOut(
        consultation_id=record.id,
        valid=result["valid"],
        missing_sections=result["missingSections"],
        raw_response=result["rawResponse"],
        sections=result["sections"],
        clinician_feedback_applied=result["clinicianFeedbackApplied"],
        zape_personalization=result["zapePersonalization"],
        requires_clinician_review=result["requiresClinicianReview"],
    )


@router.post("/personalize", response_model=ZAPEPersonalizeResponse)
def personalize(
    payload: ZAPEPersonalizeRequest,
    user: CurrentUser = Depends(require_permission("hakeem.consult")),
):
    """ZAPE 2.0 (ZAYVORA Adaptive Personalization Engine):
    Performs algorithmic multi-factor posology scaling (Young's/Cowling's rules, eGFR),
    Mizaj constitutional modulation, and seasonal adjustments (Fasl-e-Saal)."""
    result = run_zape_personalization(
        patient_context=payload.patient_context,
        candidate_drugs=payload.candidate_drugs,
        season=payload.season,
    )
    return ZAPEPersonalizeResponse(
        posology=result["posology"],
        temperament_modulation=result["temperament_modulation"],
        seasonal_modulation=result["seasonal_modulation"],
        overall_summary=result["overall_summary"],
    )

