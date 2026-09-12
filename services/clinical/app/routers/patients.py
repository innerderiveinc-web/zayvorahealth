from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.models.clinical import Patient
from app.schemas.clinical import PatientCreate, PatientOut, PatientUpdate

router = APIRouter(prefix="/api/v1/patients", tags=["patients"])


def _get_patient_or_404(db: Session, patient_id: uuid.UUID, organization_id: str) -> Patient:
    patient = db.execute(
        select(Patient).where(Patient.id == patient_id, Patient.organization_id == organization_id)
    ).scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("", response_model=PatientOut, status_code=201)
def create_patient(
    payload: PatientCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("patient.create")),
):
    existing = db.execute(
        select(Patient).where(Patient.organization_id == user.organization_id, Patient.mrn == payload.mrn)
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail=f"A patient with MRN '{payload.mrn}' already exists")

    patient = Patient(
        organization_id=user.organization_id,
        created_by_user_id=user.user_id,
        **payload.model_dump(),
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("", response_model=list[PatientOut])
def list_patients(
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    patients = db.execute(
        select(Patient).where(Patient.organization_id == user.organization_id).order_by(Patient.created_at.desc())
    ).scalars().all()
    return patients


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    return _get_patient_or_404(db, patient_id, user.organization_id)


@router.patch("/{patient_id}", response_model=PatientOut)
def update_patient(
    patient_id: uuid.UUID,
    payload: PatientUpdate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("patient.update")),
):
    patient = _get_patient_or_404(db, patient_id, user.organization_id)
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(patient, field, value)
    db.commit()
    db.refresh(patient)
    return patient
