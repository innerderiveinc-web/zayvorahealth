from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.models.therapeutic import GhizaPlan
from app.schemas.therapeutic import GhizaPlanCreate, GhizaPlanOut

router = APIRouter(prefix="/api/v1/ghiza-plans", tags=["ghiza"])


@router.post("", response_model=GhizaPlanOut, status_code=201)
def create_ghiza_plan(
    payload: GhizaPlanCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("ghiza.create")),
):
    plan = GhizaPlan(
        organization_id=user.organization_id,
        created_by_user_id=user.user_id,
        **payload.model_dump(),
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.get("/by-patient/{patient_id}", response_model=list[GhizaPlanOut])
def list_ghiza_plans_for_patient(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("ghiza.read")),
):
    plans = db.execute(
        select(GhizaPlan)
        .where(GhizaPlan.patient_id == patient_id, GhizaPlan.organization_id == user.organization_id)
        .order_by(GhizaPlan.created_at.desc())
    ).scalars().all()
    return plans
