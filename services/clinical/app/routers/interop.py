from __future__ import annotations

import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.interop.abdm_gateway import ABDMGateway
from app.interop.fhir_converter import build_abdm_op_consult_bundle
from app.models.clinical import ClinicalNote, Encounter, MizajAssessment, Patient, Prescription

router = APIRouter(prefix="/api/v1/interop", tags=["interoperability-abdm-fhir"])

_ABDM_GATEWAY = ABDMGateway()


class VerifyABHARequest(BaseModel):
    abha_id: str = Field(min_length=5, max_length=50, description="14-digit ABHA number or username@abdm")


class RequestConsentPayload(BaseModel):
    patient_abha: str = Field(min_length=5, max_length=50)
    purpose_code: str = Field(default="CAREMGT")
    hi_types: list[str] | None = None
    date_range_days: int = Field(default=180, ge=1, le=730)


@router.get("/patients/{patient_id}/fhir/op-consult")
def export_fhir_op_consult(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    """Exports the patient's holistic Unani health record as an ABDM-compliant
    HL7 FHIR R4 Document Bundle (OPConsultRecord)."""
    patient = db.execute(
        select(Patient).where(Patient.id == patient_id, Patient.organization_id == user.organization_id)
    ).scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Fetch latest encounter
    encounter = db.execute(
        select(Encounter)
        .where(Encounter.patient_id == patient.id, Encounter.organization_id == user.organization_id)
        .order_by(Encounter.started_at.desc())
    ).scalars().first()

    # Fetch active prescriptions
    prescriptions = db.execute(
        select(Prescription)
        .where(Prescription.patient_id == patient.id, Prescription.organization_id == user.organization_id)
        .order_by(Prescription.created_at.desc())
    ).scalars().all()

    # Fetch latest mizaj assessment
    mizaj = db.execute(
        select(MizajAssessment)
        .where(MizajAssessment.patient_id == patient.id, MizajAssessment.organization_id == user.organization_id)
        .order_by(MizajAssessment.created_at.desc())
    ).scalars().first()

    # Conditions from clinical notes
    notes = db.execute(
        select(ClinicalNote)
        .where(ClinicalNote.patient_id == patient.id, ClinicalNote.organization_id == user.organization_id, ClinicalNote.is_current.is_(True))
    ).scalars().all()

    conditions = []
    for n in notes:
        if n.assessment:
            conditions.append({
                "diagnosis_name": n.assessment[:80],
                "unani_amraz_code": "amraz-general",
            })

    pat_dict = {
        "id": str(patient.id),
        "full_name": patient.full_name,
        "gender": patient.gender,
        "date_of_birth": patient.date_of_birth.isoformat() if patient.date_of_birth else None,
        "abha_number": getattr(patient, "abha_number", None),
        "abha_address": getattr(patient, "abha_address", None),
    }

    rx_list = [
        {
            "medication_name": p.medication_name,
            "dose": p.dose or "Standard posology",
            "instructions": p.instructions,
            "is_schedule_e1": False,
        }
        for p in prescriptions
    ]

    mizaj_dict = None
    if mizaj:
        mizaj_dict = {
            "primary_temperament": mizaj.primary_temperament,
            "heat_cold_score": mizaj.heat_cold_score,
            "wet_dry_score": mizaj.wet_dry_score,
        }

    return build_abdm_op_consult_bundle(
        patient=pat_dict,
        encounter={"id": str(encounter.id)} if encounter else None,
        conditions=conditions,
        prescriptions=rx_list,
        mizaj_assessment=mizaj_dict,
        organization_id=user.organization_id,
    )


@router.post("/abdm/verify-abha")
def verify_abha_endpoint(
    payload: VerifyABHARequest,
    user: CurrentUser = Depends(require_permission("patient.write")),
):
    """ABDM Milestone 1: Verifies an ABHA ID or PHR Address."""
    return _ABDM_GATEWAY.verify_abha(payload.abha_id)


@router.post("/abdm/consent/request")
def request_consent_endpoint(
    payload: RequestConsentPayload,
    user: CurrentUser = Depends(require_permission("patient.write")),
):
    """ABDM Milestone 2: Initiates a Consent Manager request to the patient's ABHA account."""
    return _ABDM_GATEWAY.request_consent(
        patient_abha=payload.patient_abha,
        purpose_code=payload.purpose_code,
        hi_types=payload.hi_types,
        date_range_days=payload.date_range_days,
    )


@router.get("/abdm/consent/{consent_request_id}")
def get_consent_status_endpoint(
    consent_request_id: str,
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    """Checks the status of an ABDM Consent Request."""
    record = _ABDM_GATEWAY.get_consent_status(consent_request_id)
    if not record:
        raise HTTPException(status_code=404, detail="Consent request not found")
    return record


@router.post("/abdm/consent/{consent_request_id}/grant")
def grant_consent_endpoint(
    consent_request_id: str,
    user: CurrentUser = Depends(require_permission("patient.write")),
):
    """Simulates consent approval callback from the patient's ABHA app."""
    record = _ABDM_GATEWAY.grant_consent_mock(consent_request_id)
    if not record:
        raise HTTPException(status_code=404, detail="Consent request not found")
    return record
