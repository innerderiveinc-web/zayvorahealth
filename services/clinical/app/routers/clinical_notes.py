from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.models.clinical import ClinicalNote, Encounter
from app.schemas.clinical import ClinicalNoteAmend, ClinicalNoteCreate, ClinicalNoteOut

router = APIRouter(prefix="/api/v1/clinical-notes", tags=["clinical-notes"])


@router.post("", response_model=ClinicalNoteOut, status_code=201)
def create_note(
    payload: ClinicalNoteCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("clinical_note.create")),
):
    encounter = db.execute(
        select(Encounter).where(Encounter.id == payload.encounter_id, Encounter.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found")

    note = ClinicalNote(
        organization_id=user.organization_id,
        patient_id=encounter.patient_id,
        encounter_id=encounter.id,
        author_user_id=user.user_id,
        subjective=payload.subjective,
        objective=payload.objective,
        assessment=payload.assessment,
        plan=payload.plan,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.post("/{note_id}/amend", response_model=ClinicalNoteOut, status_code=201)
def amend_note(
    note_id: uuid.UUID,
    payload: ClinicalNoteAmend,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("clinical_note.amend")),
):
    """Amending never edits the original row — see models/clinical.py
    module docstring on versioning. This creates a new ClinicalNote row
    pointing back at the original via amends_note_id, and flips the
    original's is_current to False. Both rows remain queryable forever."""
    original = db.execute(
        select(ClinicalNote).where(ClinicalNote.id == note_id, ClinicalNote.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not original:
        raise HTTPException(status_code=404, detail="Clinical note not found")
    if not original.is_current:
        raise HTTPException(status_code=409, detail="This note has already been superseded by a later amendment")

    amended = ClinicalNote(
        organization_id=user.organization_id,
        patient_id=original.patient_id,
        encounter_id=original.encounter_id,
        author_user_id=user.user_id,
        subjective=payload.subjective,
        objective=payload.objective,
        assessment=payload.assessment,
        plan=payload.plan,
        amends_note_id=original.id,
    )
    original.is_current = False
    db.add(amended)
    db.commit()
    db.refresh(amended)
    return amended


@router.get("/by-patient/{patient_id}", response_model=list[ClinicalNoteOut])
def list_notes_for_patient(
    patient_id: uuid.UUID,
    include_superseded: bool = False,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("clinical_note.read")),
):
    query = select(ClinicalNote).where(
        ClinicalNote.patient_id == patient_id, ClinicalNote.organization_id == user.organization_id
    )
    if not include_superseded:
        query = query.where(ClinicalNote.is_current.is_(True))
    notes = db.execute(query.order_by(ClinicalNote.created_at.desc())).scalars().all()
    return notes


@router.get("/{note_id}/history", response_model=list[ClinicalNoteOut])
def note_history(
    note_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("clinical_note.read")),
):
    """Walk the amends_note_id chain to return every version of a note,
    oldest first — the full audit trail for that piece of documentation."""
    chain: list[ClinicalNote] = []
    current = db.execute(
        select(ClinicalNote).where(ClinicalNote.id == note_id, ClinicalNote.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not current:
        raise HTTPException(status_code=404, detail="Clinical note not found")

    # Walk forward to the latest version first, in case note_id points at
    # an old, superseded version.
    while True:
        newer = db.execute(
            select(ClinicalNote).where(
                ClinicalNote.amends_note_id == current.id, ClinicalNote.organization_id == user.organization_id
            )
        ).scalar_one_or_none()
        if not newer:
            break
        current = newer

    chain.append(current)
    while current.amends_note_id is not None:
        current = db.execute(select(ClinicalNote).where(ClinicalNote.id == current.amends_note_id)).scalar_one()
        chain.append(current)

    return list(reversed(chain))
