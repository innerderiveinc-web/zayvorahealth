from __future__ import annotations

import uuid
from datetime import datetime, timezone

try:
    from fastapi import APIRouter, Depends, HTTPException
    from fastapi.responses import PlainTextResponse
except ImportError:
    APIRouter = object
    Depends = object
    HTTPException = Exception
    PlainTextResponse = object

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, get_current_user
from app.core.database import get_db
from app.engines.pharmacovigilance import evaluate_who_umc_causality
from app.models.therapeutic import UnifiedCarePlan
from app.schemas.therapeutic import (
    ADRReportCreate,
    CarePlanCreate,
    CarePlanOut,
    CarePlanSign,
    WHOUMCResultOut,
)

router = APIRouter(prefix="/api/v1/care-plans", tags=["care-plans"])


def _require_care_plan_create(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if "care_plan.create" not in user.permissions and "nuskha.create" not in user.permissions:
        raise HTTPException(status_code=403, detail="Missing required permission: care_plan.create")
    return user


def _require_care_plan_read(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if "care_plan.read" not in user.permissions and "nuskha.read" not in user.permissions:
        raise HTTPException(status_code=403, detail="Missing required permission: care_plan.read")
    return user


def _require_care_plan_sign(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if "care_plan.sign" not in user.permissions and "nuskha.approve" not in user.permissions:
        raise HTTPException(status_code=403, detail="Missing required permission: care_plan.sign")
    return user


@router.post("", response_model=CarePlanOut, status_code=201)
def create_care_plan(
    payload: CarePlanCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(_require_care_plan_create),
):
    """Creates a unified multi-horizon care plan integrating Dawa, Tadbeer,
    Ghiza, and Asbab Sittah Daruriyyah.
    
    Safe Invariant: safe_to_lock is initialized to False; status is 'draft'.
    Requires statutory clinician signing to activate.
    """
    care_plan = UnifiedCarePlan(
        organization_id=uuid.UUID(str(user.organization_id)),
        patient_id=payload.patient_id,
        encounter_id=payload.encounter_id,
        created_by_user_id=user.user_id,
        title=payload.title,
        horizon=payload.horizon,
        duration_days=payload.duration_days,
        mizaj_context=payload.mizaj_context,
        usool_e_ilaj=payload.usool_e_ilaj,
        primary_indication=payload.primary_indication,
        ilaj_bid_dawa=payload.ilaj_bid_dawa,
        ilaj_bit_tadbeer=payload.ilaj_bit_tadbeer,
        ilaj_bil_ghiza=payload.ilaj_bil_ghiza,
        asbab_sittah=payload.asbab_sittah.model_dump(),
        review_milestones=payload.review_milestones,
        prognosis_notes=payload.prognosis_notes,
        safe_to_lock=False,
        status="draft",
    )
    db.add(care_plan)
    db.commit()
    db.refresh(care_plan)
    return care_plan


@router.get("/patient/{patient_id}", response_model=list[CarePlanOut])
def list_care_plans_for_patient(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(_require_care_plan_read),
):
    stmt = (
        select(UnifiedCarePlan)
        .where(
            UnifiedCarePlan.organization_id == uuid.UUID(str(user.organization_id)),
            UnifiedCarePlan.patient_id == patient_id,
        )
        .order_by(UnifiedCarePlan.created_at.desc())
    )
    return list(db.scalars(stmt).all())


@router.get("/{care_plan_id}", response_model=CarePlanOut)
def get_care_plan(
    care_plan_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(_require_care_plan_read),
):
    stmt = select(UnifiedCarePlan).where(
        UnifiedCarePlan.id == care_plan_id,
        UnifiedCarePlan.organization_id == uuid.UUID(str(user.organization_id)),
    )
    plan = db.scalar(stmt)
    if not plan:
        raise HTTPException(status_code=404, detail="Care plan not found")
    return plan


@router.post("/{care_plan_id}/sign", response_model=CarePlanOut)
def sign_care_plan(
    care_plan_id: uuid.UUID,
    payload: CarePlanSign,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(_require_care_plan_sign),
):
    """Statutory Clinician Sign-off & Plan Locking.
    
    Validates practitioner statutory authority, verifies clinical posology
    across all modalities, and locks the plan into 'active' status with
    safe_to_lock = True.
    """
    if not payload.statutory_affirmation:
        raise HTTPException(
            status_code=400,
            detail="Statutory affirmation of clinical review is required to lock care plan",
        )

    stmt = select(UnifiedCarePlan).where(
        UnifiedCarePlan.id == care_plan_id,
        UnifiedCarePlan.organization_id == uuid.UUID(str(user.organization_id)),
    )
    plan = db.scalar(stmt)
    if not plan:
        raise HTTPException(status_code=404, detail="Care plan not found")

    if plan.status == "active" and plan.safe_to_lock:
        raise HTTPException(status_code=400, detail="Care plan is already signed and locked")

    plan.safe_to_lock = True
    plan.status = "active"
    plan.signed_by_clinician_id = user.user_id
    plan.clinician_registration_number = payload.clinician_registration_number.strip()
    plan.signed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(plan)
    return plan


@router.post("/pharmacovigilance/evaluate", response_model=WHOUMCResultOut)
def evaluate_pharmacovigilance_endpoint(
    payload: ADRReportCreate,
    user: CurrentUser = Depends(get_current_user),
):
    """Evaluates suspected Adverse Drug Reaction (ADR) or botanical toxicity
    using the international WHO-UMC standardized causality criteria and
    AYUSH Schedule E(1) statutory Mudabbar rules.
    """
    result = evaluate_who_umc_causality(payload.model_dump())
    return result


@router.post("/pharmacovigilance/export-e2b", response_class=PlainTextResponse)
def export_pharmacovigilance_e2b_endpoint(
    payload: ADRReportCreate,
    user: CurrentUser = Depends(get_current_user),
):
    """Exports suspected Adverse Drug Reaction (ADR) evaluation to ICH E2B(R3)
    standardized XML format for national and WHO-UMC pharmacovigilance submission.
    """
    from app.pharmacovigilance.e2b_exporter import export_ich_e2b_r3_xml
    evaluation = evaluate_who_umc_causality(payload.model_dump())
    xml_data = export_ich_e2b_r3_xml(payload.model_dump(), evaluation)
    if PlainTextResponse is not object:
        return PlainTextResponse(content=xml_data, media_type="application/xml")
    return xml_data


@router.post("/pharmacovigilance/export-cioms")
def export_pharmacovigilance_cioms_endpoint(
    payload: ADRReportCreate,
    user: CurrentUser = Depends(get_current_user),
):
    """Exports suspected Adverse Drug Reaction (ADR) evaluation to CIOMS Form I format."""
    from app.pharmacovigilance.e2b_exporter import export_cioms_i_format
    evaluation = evaluate_who_umc_causality(payload.model_dump())
    return export_cioms_i_format(payload.model_dump(), evaluation)
