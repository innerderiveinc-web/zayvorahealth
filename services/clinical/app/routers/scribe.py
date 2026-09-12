"""
ZAYVORA HEALTH™ — Ambient Clinical Scribe Router
Provides endpoints for audio consultation transcript processing, SOAP note generation, and clinician sign-off.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from ..scribe.ambient_scribe import AmbientScribeEngine, UnaniSOAPNote

router = APIRouter(prefix="/api/v1/scribe", tags=["Ambient Clinical Scribe"])

# In-memory store for SOAP notes during consultation session
SOAP_NOTES_STORE: Dict[str, UnaniSOAPNote] = {}


class TranscriptProcessRequest(BaseModel):
    patient_id: str = Field(..., description="UUID or ID of the patient")
    transcript: str = Field(..., description="Audio consultation transcript in English, Urdu, Hindi, or mixed Roman script")
    session_id: Optional[str] = Field(None, description="Optional session or consultation ID")
    vitals: Optional[Dict[str, Any]] = Field(None, description="Optional vital signs recorded during session")


class ClinicianSignOffRequest(BaseModel):
    note_id: str = Field(..., description="ID of the draft SOAP note")
    clinician_id: str = Field(..., description="Accredited Clinician ID")
    clinician_name: str = Field(..., description="Clinician full name")
    clinician_role: str = Field(..., description="Role e.g. clinician, hakeem, doctor")
    clinical_amendments: Optional[Dict[str, Any]] = Field(None, description="Any amendments to subjective, assessment, or plan")
    clinician_notes: Optional[str] = Field(None, description="Clinician's attestation or additional instructions")


@router.post("/process-transcript", summary="Process dialogue transcript into structured Unani SOAP draft")
async def process_transcript(payload: TranscriptProcessRequest):
    if not payload.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript cannot be empty.")

    soap_note = AmbientScribeEngine.generate_soap_draft(
        patient_id=payload.patient_id,
        transcript=payload.transcript,
        session_id=payload.session_id,
        vital_signs=payload.vitals,
    )
    SOAP_NOTES_STORE[soap_note.note_id] = soap_note

    return {
        "note_id": soap_note.note_id,
        "patient_id": soap_note.patient_id,
        "session_id": soap_note.session_id,
        "created_at": soap_note.created_at,
        "detected_languages": soap_note.detected_languages,
        "subjective": soap_note.subjective,
        "objective": soap_note.objective,
        "assessment": soap_note.assessment,
        "plan": soap_note.plan,
        "safe_to_lock": soap_note.safe_to_lock,
        "status": soap_note.status,
    }


@router.get("/notes/{note_id}", summary="Retrieve a SOAP note by ID")
async def get_soap_note(note_id: str):
    note = SOAP_NOTES_STORE.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"SOAP note '{note_id}' not found.")
    return note


@router.post("/sign-and-lock", summary="Clinician reviews, verifies, and locks a SOAP note")
async def sign_and_lock_soap_note(payload: ClinicianSignOffRequest):
    note = SOAP_NOTES_STORE.get(payload.note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"SOAP note '{payload.note_id}' not found.")

    try:
        updated_note = AmbientScribeEngine.clinician_sign_and_lock(
            soap_note=note,
            clinician_id=payload.clinician_id,
            clinician_name=payload.clinician_name,
            clinician_role=payload.clinician_role,
            clinical_amendments=payload.clinical_amendments,
            clinician_notes=payload.clinician_notes,
        )
        SOAP_NOTES_STORE[payload.note_id] = updated_note
        return {
            "note_id": updated_note.note_id,
            "status": updated_note.status,
            "safe_to_lock": updated_note.safe_to_lock,
            "signed_by": updated_note.signed_by,
            "signed_at": updated_note.signed_at,
            "clinician_notes": updated_note.clinician_notes,
            "assessment": updated_note.assessment,
            "plan": updated_note.plan,
        }
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
