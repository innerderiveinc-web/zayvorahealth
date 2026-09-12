from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.engines.tadbeer_guardrails import run_tadbeer_guardrails
from app.models.therapeutic import TadbeerPlan
from app.schemas.therapeutic import TadbeerPlanCreate, TadbeerPlanOut

router = APIRouter(prefix="/api/v1/tadbeer-plans", tags=["tadbeer"])


@router.post("", response_model=TadbeerPlanOut, status_code=201)
def create_tadbeer_plan(
    payload: TadbeerPlanCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("tadbeer.create")),
):
    data = payload.model_dump()
    safety_context = data.pop("patient_safety_context", None) or {}
    safety_result = run_tadbeer_guardrails(
        patient_context=safety_context,
        plan=data,
    )
    plan = TadbeerPlan(
        organization_id=user.organization_id,
        created_by_user_id=user.user_id,
        safety_verdict=safety_result["verdict"],
        safety_reasons=safety_result["reasons"],
        **data,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.get("/by-patient/{patient_id}", response_model=list[TadbeerPlanOut])
def list_tadbeer_plans_for_patient(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("tadbeer.read")),
):
    plans = db.execute(
        select(TadbeerPlan)
        .where(TadbeerPlan.patient_id == patient_id, TadbeerPlan.organization_id == user.organization_id)
        .order_by(TadbeerPlan.created_at.desc())
    ).scalars().all()
    return plans
