from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.models.clinical import Encounter, Prescription
from app.schemas.clinical import PrescriptionCreate, PrescriptionDiscontinue, PrescriptionOut

router = APIRouter(prefix="/api/v1/prescriptions", tags=["prescriptions"])


@router.post("", response_model=PrescriptionOut, status_code=201)
def create_prescription(
    payload: PrescriptionCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("prescription.create")),
):
    encounter = db.execute(
        select(Encounter).where(Encounter.id == payload.encounter_id, Encounter.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found")

    prescription = Prescription(
        organization_id=user.organization_id,
        patient_id=encounter.patient_id,
        encounter_id=encounter.id,
        prescribed_by_user_id=user.user_id,
        medication_name=payload.medication_name,
        dose=payload.dose,
        frequency=payload.frequency,
        duration=payload.duration,
        instructions=payload.instructions,
    )
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return prescription


@router.post("/{prescription_id}/discontinue", response_model=PrescriptionOut)
def discontinue_prescription(
    prescription_id: uuid.UUID,
    payload: PrescriptionDiscontinue,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("prescription.discontinue")),
):
    prescription = db.execute(
        select(Prescription).where(Prescription.id == prescription_id, Prescription.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    if prescription.status == "discontinued":
        raise HTTPException(status_code=409, detail="Prescription is already discontinued")

    prescription.status = "discontinued"
    prescription.discontinued_at = datetime.now(timezone.utc)
    prescription.discontinued_reason = payload.reason
    db.commit()
    db.refresh(prescription)
    return prescription


@router.get("/by-patient/{patient_id}", response_model=list[PrescriptionOut])
def list_prescriptions_for_patient(
    patient_id: uuid.UUID,
    active_only: bool = False,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("prescription.read")),
):
    query = select(Prescription).where(
        Prescription.patient_id == patient_id, Prescription.organization_id == user.organization_id
    )
    if active_only:
        query = query.where(Prescription.status == "active")
    prescriptions = db.execute(query.order_by(Prescription.created_at.desc())).scalars().all()
    return prescriptions
