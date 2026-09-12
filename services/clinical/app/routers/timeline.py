from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.models.clinical import Appointment, ClinicalNote, Encounter, Patient, Prescription
from app.schemas.clinical import TimelineEvent

router = APIRouter(prefix="/api/v1/patients", tags=["timeline"])


@router.get("/{patient_id}/timeline", response_model=list[TimelineEvent])
def get_patient_timeline(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    """Master Build Prompt v4.0 §6: a chronological, machine-readable view
    of everything that has happened to this patient — encounters, notes,
    prescriptions, appointments — so a clinician can understand the
    patient's journey quickly. Only current (non-superseded) note versions
    appear here; use /clinical-notes/{id}/history for the full amendment
    trail of a specific note.
    """
    patient = db.execute(
        select(Patient).where(Patient.id == patient_id, Patient.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    events: list[TimelineEvent] = []

    encounters = db.execute(
        select(Encounter).where(Encounter.patient_id == patient_id, Encounter.organization_id == user.organization_id)
    ).scalars().all()
    for e in encounters:
        label = e.encounter_type.replace("_", " ").title()
        summary = f"{label} encounter" + (f" — {e.chief_complaint}" if e.chief_complaint else "")
        events.append(TimelineEvent(event_type="encounter", event_id=e.id, occurred_at=e.started_at, summary=summary))

    notes = db.execute(
        select(ClinicalNote).where(
            ClinicalNote.patient_id == patient_id,
            ClinicalNote.organization_id == user.organization_id,
            ClinicalNote.is_current.is_(True),
        )
    ).scalars().all()
    for n in notes:
        snippet = (n.assessment or n.subjective or "")[:80]
        events.append(
            TimelineEvent(event_type="clinical_note", event_id=n.id, occurred_at=n.created_at, summary=f"Clinical note — {snippet}" if snippet else "Clinical note")
        )

    prescriptions = db.execute(
        select(Prescription).where(Prescription.patient_id == patient_id, Prescription.organization_id == user.organization_id)
    ).scalars().all()
    for p in prescriptions:
        summary = f"Prescribed {p.medication_name}" + (f" {p.dose}" if p.dose else "")
        events.append(TimelineEvent(event_type="prescription", event_id=p.id, occurred_at=p.created_at, summary=summary))
        if p.status == "discontinued" and p.discontinued_at:
            events.append(
                TimelineEvent(
                    event_type="prescription",
                    event_id=p.id,
                    occurred_at=p.discontinued_at,
                    summary=f"Discontinued {p.medication_name}" + (f" — {p.discontinued_reason}" if p.discontinued_reason else ""),
                )
            )

    appointments = db.execute(
        select(Appointment).where(Appointment.patient_id == patient_id, Appointment.organization_id == user.organization_id)
    ).scalars().all()
    for a in appointments:
        events.append(
            TimelineEvent(event_type="appointment", event_id=a.id, occurred_at=a.scheduled_at, summary=f"Appointment ({a.status})" + (f" — {a.reason}" if a.reason else ""))
        )

    events.sort(key=lambda ev: ev.occurred_at)
    return events
