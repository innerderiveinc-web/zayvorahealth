from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.models.clinical import Appointment, Patient
from app.schemas.clinical import AppointmentCreate, AppointmentOut, AppointmentUpdate

router = APIRouter(prefix="/api/v1/appointments", tags=["appointments"])


@router.post("", response_model=AppointmentOut, status_code=201)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("appointment.create")),
):
    patient = db.execute(
        select(Patient).where(Patient.id == payload.patient_id, Patient.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    appointment = Appointment(
        organization_id=user.organization_id,
        patient_id=payload.patient_id,
        clinician_user_id=user.user_id,
        scheduled_at=payload.scheduled_at,
        duration_minutes=payload.duration_minutes,
        reason=payload.reason,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.patch("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(
    appointment_id: uuid.UUID,
    payload: AppointmentUpdate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("appointment.update")),
):
    appointment = db.execute(
        select(Appointment).where(Appointment.id == appointment_id, Appointment.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(appointment, field, value)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.get("/by-patient/{patient_id}", response_model=list[AppointmentOut])
def list_appointments_for_patient(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("appointment.read")),
):
    appointments = db.execute(
        select(Appointment)
        .where(Appointment.patient_id == patient_id, Appointment.organization_id == user.organization_id)
        .order_by(Appointment.scheduled_at.asc())
    ).scalars().all()
    return appointments
