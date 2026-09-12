"""
ZAYVORA HEALTH™ — Patient Portal Router
Provides endpoints for patient daily schedule ("Today" view), posology adherence logging, and secure messaging.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from ..patient_portal.portal_engine import (
    PatientPortalEngine,
    DailyDoseItem,
    PatientDailySchedule,
    PatientMessage,
)

router = APIRouter(prefix="/api/v1/patient-portal", tags=["Patient App 2.0 & Adherence"])


class LogAdherenceRequest(BaseModel):
    patient_id: str = Field(..., description="UUID of the patient")
    dose_id: str = Field(..., description="Dose identifier")
    status: str = Field(..., description="TAKEN, MISSED, or SKIPPED")
    skip_reason: Optional[str] = Field(None, description="Optional reason if skipped")


class SendMessageRequest(BaseModel):
    patient_id: str = Field(..., description="UUID of the patient")
    sender_type: str = Field("PATIENT", description="PATIENT or CLINICIAN")
    sender_name: str = Field(..., description="Name of sender")
    content: str = Field(..., description="Message text content")


@router.get("/{patient_id}/today", summary="Retrieve personalized daily clinical schedule ('Today' view)")
async def get_patient_today(patient_id: str, date: Optional[str] = None):
    schedule = PatientPortalEngine.get_daily_schedule(patient_id, date)
    return {
        "patient_id": schedule.patient_id,
        "date": schedule.date_str,
        "doses": [
            {
                "dose_id": d.dose_id,
                "medication_name": d.medication_name,
                "dosage_form": d.dosage_form,
                "quantity_display": d.quantity_display,
                "timing_slot": d.timing_slot,
                "intake_vehicle": d.intake_vehicle,
                "instructions": d.instructions,
                "status": d.status,
                "logged_at_utc": d.logged_at_utc,
                "skip_reason": d.skip_reason,
            }
            for d in schedule.doses
        ],
        "tadbeer_reminders": schedule.tadbeer_reminders,
        "ghiza_dietary_rules": schedule.ghiza_dietary_rules,
        "compliance_score_7d": schedule.compliance_score_7d,
        "overall_status": schedule.overall_status,
    }


@router.post("/adherence", summary="Log medication intake adherence")
async def log_adherence(payload: LogAdherenceRequest):
    try:
        item = PatientPortalEngine.log_adherence(
            patient_id=payload.patient_id,
            dose_id=payload.dose_id,
            status=payload.status,
            skip_reason=payload.skip_reason,
        )
        return {
            "dose_id": item.dose_id,
            "status": item.status,
            "logged_at_utc": item.logged_at_utc,
            "skip_reason": item.skip_reason,
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.post("/messages/send", summary="Send asynchronous message between patient and clinician")
async def send_message(payload: SendMessageRequest):
    msg = PatientPortalEngine.send_message(
        patient_id=payload.patient_id,
        sender_type=payload.sender_type,
        sender_name=payload.sender_name,
        content=payload.content,
    )
    return {
        "message_id": msg.message_id,
        "patient_id": msg.patient_id,
        "sender_type": msg.sender_type,
        "sender_name": msg.sender_name,
        "content": msg.content,
        "urgency": msg.urgency,
        "timestamp_utc": msg.timestamp_utc,
    }


@router.get("/{patient_id}/messages", summary="Get message thread for patient")
async def get_patient_messages(patient_id: str):
    messages = PatientPortalEngine.get_messages(patient_id)
    return [
        {
            "message_id": m.message_id,
            "sender_type": m.sender_type,
            "sender_name": m.sender_name,
            "content": m.content,
            "urgency": m.urgency,
            "timestamp_utc": m.timestamp_utc,
        }
        for m in messages
    ]


class VoiceSynthesisRequest(BaseModel):
    patient_id: str = Field(..., description="UUID of the patient")
    medication_name: Optional[str] = Field("Jawarish Kamuni", description="Name of prescribed formulation")
    dosage_display: Optional[str] = Field("5g (1 teaspoon)", description="Dosage quantity")
    timing_slot: Optional[str] = Field("Morning", description="Timing slot (Morning, Afternoon, Evening, Bedtime)")
    intake_vehicle: Optional[str] = Field("Lukewarm water", description="Anupana / intake vehicle (Lukewarm water, Milk, Honey)")
    language: str = Field("ur", description="Target language: ur (Urdu), hi (Hindi), te (Telugu), en (English)")
    dose_id: Optional[str] = Field(None, description="Optional dose ID from today's schedule")


@router.post("/voice/synthesize", summary="Synthesize localized audio instructions via Bhashini / Indic TTS engine (Issue ENH-02)")
async def synthesize_medication_voice_prompt(payload: VoiceSynthesisRequest):
    from ..patient_portal.voice_synthesizer import BhashiniVoiceSynthesizer

    med_name = payload.medication_name or "Prescribed Medication"
    dose_disp = payload.dosage_display or "as directed"
    timing = payload.timing_slot or "Morning"
    vehicle = payload.intake_vehicle or "lukewarm water"

    # If dose_id provided, look up from verified daily schedule to guarantee clinical accuracy
    if payload.dose_id:
        schedule = PatientPortalEngine.get_daily_schedule(payload.patient_id)
        for d in schedule.doses:
            if d.dose_id == payload.dose_id:
                med_name = d.medication_name
                dose_disp = d.quantity_display
                timing = d.timing_slot
                vehicle = d.intake_vehicle
                break

    result = BhashiniVoiceSynthesizer.synthesize_medication_prompt(
        patient_id=payload.patient_id,
        medication_name=med_name,
        dosage_display=dose_disp,
        timing_slot=timing,
        intake_vehicle=vehicle,
        language=payload.language,
    )
    return result

