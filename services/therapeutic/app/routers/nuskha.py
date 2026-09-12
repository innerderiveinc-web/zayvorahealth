from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.engines.nuskha_compiler import compile_nuskha
from app.engines.safety_firewall import run_safety_firewall
from app.models.therapeutic import NuskhaDraft
from app.schemas.therapeutic import (
    NuskhaApprove,
    NuskhaCompileRequest,
    NuskhaCompileResponse,
    NuskhaDraftCreate,
    NuskhaDraftOut,
    NuskhaReject,
)

router = APIRouter(prefix="/api/v1/nuskha-drafts", tags=["nuskha"])

BLOCKING_VERDICTS = {"DO_NOT_RECOMMEND", "REFER"}


@router.post("/compile", response_model=NuskhaCompileResponse)
def compile_nuskha_endpoint(
    payload: NuskhaCompileRequest,
    user: CurrentUser = Depends(require_permission("nuskha.create")),
):
    """Classical Unani Nuskha Compiler: assigns formulation roles (Juz-e-Azam,
    Muin, Musleh, Badal), validates target organ-axis alignment, adjusts
    pediatric/geriatric/renal posology, and verifies temperamental balance.
    """
    result = compile_nuskha(
        target_organ_axes=payload.target_organ_axes,
        therapeutic_objective=payload.therapeutic_objective,
        ingredients=[i.model_dump() for i in payload.ingredients],
        patient_context=payload.patient_safety_context.model_dump(),
    )
    return result


@router.post("", response_model=NuskhaDraftOut, status_code=201)
def create_nuskha_draft(
    payload: NuskhaDraftCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("nuskha.create")),
):
    """Master Build Prompt v4.0 §19: 'Never automatically convert an
    AI-generated candidate into a final prescription.' Every draft is
    created with status='draft' — there is no code path that creates one
    pre-approved. The Safety Firewall runs here, once, and its result is
    stored immutably alongside the draft; it is never silently recomputed.
    """
    safety_result = run_safety_firewall(
        patient_context=payload.patient_safety_context.model_dump(),
        ingredients=[i.model_dump() for i in payload.ingredients],
    )

    draft = NuskhaDraft(
        organization_id=user.organization_id,
        patient_id=payload.patient_id,
        encounter_id=payload.encounter_id,
        created_by_user_id=user.user_id,
        mizaj_context=payload.mizaj_context,
        asbab=payload.asbab,
        tashkhis=payload.tashkhis,
        organ_axis_context=payload.organ_axis_context,
        usool_e_ilaj=payload.usool_e_ilaj,
        therapeutic_objective=payload.therapeutic_objective,
        ingredients=[i.model_dump() for i in payload.ingredients],
        dosage_form=payload.dosage_form,
        dose=payload.dose,
        timing=payload.timing,
        duration=payload.duration,
        parhez=payload.parhez,
        safety_verdict=safety_result["verdict"],
        safety_reasons=safety_result["reasons"],
        status="draft",
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft


def _get_draft_or_404(db: Session, draft_id: uuid.UUID, organization_id: str) -> NuskhaDraft:
    draft = db.execute(
        select(NuskhaDraft).where(NuskhaDraft.id == draft_id, NuskhaDraft.organization_id == organization_id)
    ).scalar_one_or_none()
    if not draft:
        raise HTTPException(status_code=404, detail="Nuskha draft not found")
    return draft


@router.get("/{draft_id}", response_model=NuskhaDraftOut)
def get_nuskha_draft(
    draft_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("nuskha.read")),
):
    return _get_draft_or_404(db, draft_id, user.organization_id)


@router.get("/by-patient/{patient_id}", response_model=list[NuskhaDraftOut])
def list_drafts_for_patient(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("nuskha.read")),
):
    drafts = db.execute(
        select(NuskhaDraft)
        .where(NuskhaDraft.patient_id == patient_id, NuskhaDraft.organization_id == user.organization_id)
        .order_by(NuskhaDraft.created_at.desc())
    ).scalars().all()
    return drafts


@router.post("/{draft_id}/approve", response_model=NuskhaDraftOut)
def approve_nuskha_draft(
    draft_id: uuid.UUID,
    payload: NuskhaApprove,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("nuskha.approve")),
):
    """Clinical Authority Guardrail (§2, §19): if the stored Safety
    Firewall verdict is DO_NOT_RECOMMEND or REFER, approval is blocked
    UNLESS the approver also holds safety_firewall.override AND supplies
    a non-empty justification — which is stored permanently on the draft,
    not just accepted and discarded. This is the one place in the whole
    therapeutic service where a human can override a safety hold, and it
    is logged every time it happens.
    """
    draft = _get_draft_or_404(db, draft_id, user.organization_id)
    if draft.status != "draft":
        raise HTTPException(status_code=409, detail=f"Draft is already '{draft.status}' — cannot approve again")

    if draft.safety_verdict in BLOCKING_VERDICTS:
        if "safety_firewall.override" not in user.permissions:
            raise HTTPException(
                status_code=403,
                detail=f"Safety Firewall verdict is '{draft.safety_verdict}' — approval requires safety_firewall.override permission and a justification.",
            )
        if not payload.safety_override_justification.strip():
            raise HTTPException(
                status_code=422,
                detail="safety_override_justification is required to approve a draft with a blocking Safety Firewall verdict.",
            )
        draft.safety_override_justification = payload.safety_override_justification

    draft.status = "approved"
    draft.reviewed_by_user_id = user.user_id
    if payload.clinician_registration_number:
        draft.clinician_registration_number = payload.clinician_registration_number
    draft.reviewed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(draft)
    return draft


@router.post("/{draft_id}/reject", response_model=NuskhaDraftOut)
def reject_nuskha_draft(
    draft_id: uuid.UUID,
    payload: NuskhaReject,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("nuskha.approve")),
):
    draft = _get_draft_or_404(db, draft_id, user.organization_id)
    if draft.status != "draft":
        raise HTTPException(status_code=409, detail=f"Draft is already '{draft.status}' — cannot reject again")

    draft.status = "rejected"
    draft.rejection_reason = payload.rejection_reason
    draft.reviewed_by_user_id = user.user_id
    draft.reviewed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(draft)
    return draft
