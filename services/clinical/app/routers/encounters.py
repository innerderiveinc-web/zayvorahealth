from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.models.clinical import Encounter, Patient
from app.schemas.clinical import EncounterCreate, EncounterOut

router = APIRouter(prefix="/api/v1/encounters", tags=["encounters"])


@router.post("", response_model=EncounterOut, status_code=201)
def create_encounter(
    payload: EncounterCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("encounter.create")),
):
    patient = db.execute(
        select(Patient).where(Patient.id == payload.patient_id, Patient.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    encounter = Encounter(
        organization_id=user.organization_id,
        patient_id=payload.patient_id,
        clinician_user_id=user.user_id,
        encounter_type=payload.encounter_type,
        chief_complaint=payload.chief_complaint,
    )
    db.add(encounter)
    db.commit()
    db.refresh(encounter)
    return encounter


@router.get("/{encounter_id}", response_model=EncounterOut)
def get_encounter(
    encounter_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("encounter.read")),
):
    encounter = db.execute(
        select(Encounter).where(Encounter.id == encounter_id, Encounter.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found")
    return encounter


@router.post("/{encounter_id}/close", response_model=EncounterOut)
def close_encounter(
    encounter_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("encounter.close")),
):
    encounter = db.execute(
        select(Encounter).where(Encounter.id == encounter_id, Encounter.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found")
    if encounter.status == "closed":
        raise HTTPException(status_code=409, detail="Encounter is already closed")
    encounter.status = "closed"
    encounter.closed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(encounter)
    return encounter


@router.get("/by-patient/{patient_id}", response_model=list[EncounterOut])
def list_encounters_for_patient(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("encounter.read")),
):
    encounters = db.execute(
        select(Encounter)
        .where(Encounter.patient_id == patient_id, Encounter.organization_id == user.organization_id)
        .order_by(Encounter.started_at.desc())
    ).scalars().all()
    return encounters
