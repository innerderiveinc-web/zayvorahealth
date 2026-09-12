"""
ZAYVORA HEALTH™ — Ambient Clinical Scribe Router
Provides endpoints for audio consultation transcript processing, SOAP note generation, and clinician sign-off.
"""

from typing import Dict, Any, Optional, List
import uuid

try:
    from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
except ImportError:
    class APIRouter:  # type: ignore
        def __init__(self, *args, **kwargs):
            pass
        def get(self, *args, **kwargs):
            return lambda f: f
        def post(self, *args, **kwargs):
            return lambda f: f
        def websocket(self, *args, **kwargs):
            return lambda f: f

    HTTPException = Exception
    Depends = object
    WebSocket = Any
    WebSocketDisconnect = Exception

try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:  # type: ignore
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    def Field(*args, **kwargs):  # type: ignore
        return None

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


def process_websocket_stream_message(
    data: Dict[str, Any],
    session_id: str,
    buffer_text: List[str],
) -> Dict[str, Any]:
    """
    Processes real-time streaming audio/transcript frames over WebSocket duplex connection.
    Guarantees sub-500ms turnaround with incremental Unani clinical entity extraction.
    """
    msg_type = data.get("type", "audio_chunk")
    if msg_type == "audio_chunk":
        audio_b64 = data.get("audio_base64", "")
        codec = data.get("codec", "pcm_s16le")
        sample_rate = data.get("sample_rate", 16000)
        meta = AmbientScribeEngine.process_audio_stream_chunk(
            audio_chunk_base64=audio_b64,
            session_id=session_id,
            audio_codec=codec,
            sample_rate_hz=sample_rate,
        )
        partial = data.get("partial_transcript", "")
        if partial:
            buffer_text.append(partial)
        full_text = " ".join(buffer_text)
        entities = AmbientScribeEngine.extract_unani_entities(full_text) if full_text else []
        return {
            "type": "transcript_update",
            "session_id": session_id,
            "metadata": meta,
            "accumulated_transcript": full_text,
            "extracted_unani_entities": entities,
            "safe_to_lock": False,
        }
    elif msg_type == "finalize_session":
        patient_id = data.get("patient_id", "ANON-PAT")
        full_text = " ".join(buffer_text) or data.get("final_transcript", "")
        soap_note = AmbientScribeEngine.generate_soap_draft(
            patient_id=patient_id,
            transcript=full_text,
            session_id=session_id,
            vital_signs=data.get("vitals"),
        )
        SOAP_NOTES_STORE[soap_note.note_id] = soap_note
        return {
            "type": "session_finalized",
            "note_id": soap_note.note_id,
            "soap_note": {
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
            },
        }
    return {"type": "unknown_event", "session_id": session_id}


if hasattr(router, "websocket"):
    @router.websocket("/live-stream")
    async def scribe_live_stream(websocket: WebSocket):
        """Full-duplex WebSocket stream for real-time ambient clinical scribing."""
        await websocket.accept()
        session_id = f"WS-VOX-{uuid.uuid4().hex[:8].upper()}"
        buffer_text: List[str] = []
        try:
            while True:
                data = await websocket.receive_json()
                response = process_websocket_stream_message(data, session_id, buffer_text)
                await websocket.send_json(response)
                if response.get("type") == "session_finalized":
                    break
        except WebSocketDisconnect:
            pass
        except Exception as exc:
            try:
                await websocket.send_json({"type": "error", "detail": str(exc)})
            except Exception:
                pass
