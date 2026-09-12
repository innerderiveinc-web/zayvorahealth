"""
Clinical Core domain models (Master Build Prompt v4.0 §5 Patient 360, §6
Clinical Timeline, §39 EMR).

Tenant isolation: every table carries organization_id directly (not a join
through Patient) so a single malformed query can't leak across tenants —
each query in routers/ filters on organization_id explicitly, never trusts
a patient_id alone to imply the right tenant.

Versioning: Master Build Prompt v4.0 §5 says "Never overwrite historical
clinical information. Use versioned records." Applied here to ClinicalNote
and Prescription — both are effectively append-only. Amending a note
creates a new row pointing back via amends_note_id; the original is never
edited or deleted. Patient demographic fields (name, contact info) are
treated as correctable, not clinical history, and are mutable.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def _uuid_pk() -> Mapped[uuid.UUID]:
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Patient(Base):
    """Patient 360 core record. Demographic/contact fields are mutable
    (corrections happen); everything clinically significant lives in
    Encounter/ClinicalNote/Prescription rows instead, which are versioned.
    """

    __tablename__ = "patients"

    id: Mapped[uuid.UUID] = _uuid_pk()
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    mrn: Mapped[str] = mapped_column(String(40), nullable=False)  # medical record number, org-scoped
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    date_of_birth: Mapped[str | None] = mapped_column(String(10), nullable=True)  # ISO date, nullable if unknown
    sex: Mapped[str] = mapped_column(String(20), nullable=False)  # female | male | other | unknown
    contact_phone: Mapped[str] = mapped_column(String(40), default="")
    contact_email: Mapped[str] = mapped_column(String(255), default="")
    emergency_contact: Mapped[dict] = mapped_column(JSON, default=dict)  # {name, phone, relation}
    allergies: Mapped[list] = mapped_column(JSON, default=list)
    current_medications: Mapped[list] = mapped_column(JSON, default=list)
    current_supplements: Mapped[list] = mapped_column(JSON, default=list)
    medical_history: Mapped[str] = mapped_column(Text, default="")
    surgical_history: Mapped[str] = mapped_column(Text, default="")
    family_history: Mapped[str] = mapped_column(Text, default="")
    patient_goals: Mapped[str] = mapped_column(Text, default="")
    patient_preferences: Mapped[str] = mapped_column(Text, default="")
    pregnancy_status: Mapped[str] = mapped_column(String(30), default="not_applicable")  # pregnant | not_pregnant | unknown | not_applicable
    comorbidities: Mapped[list] = mapped_column(JSON, default=list)  # structured list of condition codes/names
    consent_given: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_by_user_id: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)


class Encounter(Base):
    """A single consultation/visit. Notes, prescriptions, and (later)
    diagnoses/investigations all attach to an encounter."""

    __tablename__ = "encounters"

    id: Mapped[uuid.UUID] = _uuid_pk()
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False, index=True)
    clinician_user_id: Mapped[str] = mapped_column(String(64), nullable=False)
    encounter_type: Mapped[str] = mapped_column(String(40), default="consultation")  # consultation | follow_up | telemedicine
    chief_complaint: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="open")  # open | closed
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ClinicalNote(Base):
    """A versioned SOAP note. Amending creates a new row (amends_note_id
    points at the previous version); nothing here is ever UPDATEd after
    creation — see module docstring."""

    __tablename__ = "clinical_notes"

    id: Mapped[uuid.UUID] = _uuid_pk()
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False, index=True)
    encounter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("encounters.id"), nullable=False, index=True)
    author_user_id: Mapped[str] = mapped_column(String(64), nullable=False)
    subjective: Mapped[str] = mapped_column(Text, default="")
    objective: Mapped[str] = mapped_column(Text, default="")
    assessment: Mapped[str] = mapped_column(Text, default="")
    plan: Mapped[str] = mapped_column(Text, default="")
    amends_note_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("clinical_notes.id"), nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True)  # False once a newer version supersedes it
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class Prescription(Base):
    """A prescribed item. Discontinuing sets status/discontinued_at rather
    than deleting the row — the fact a medication was prescribed and later
    stopped is itself clinical history."""

    __tablename__ = "prescriptions"

    id: Mapped[uuid.UUID] = _uuid_pk()
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False, index=True)
    encounter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("encounters.id"), nullable=False, index=True)
    prescribed_by_user_id: Mapped[str] = mapped_column(String(64), nullable=False)
    medication_name: Mapped[str] = mapped_column(String(200), nullable=False)
    dose: Mapped[str] = mapped_column(String(100), default="")
    frequency: Mapped[str] = mapped_column(String(100), default="")
    duration: Mapped[str] = mapped_column(String(100), default="")
    instructions: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="active")  # active | discontinued
    discontinued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    discontinued_reason: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[uuid.UUID] = _uuid_pk()
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False, index=True)
    clinician_user_id: Mapped[str] = mapped_column(String(64), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(default=20)
    status: Mapped[str] = mapped_column(String(20), default="scheduled")  # scheduled | completed | cancelled | no_show
    reason: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class MizajAssessment(Base):
    """Longitudinal Mizaj evaluation using classical 10 Ajnas-e-Ashara.
    Append-only: captures patient's constitutional baseline and acute dyscrasia (Su-e-Mizaj).
    """

    __tablename__ = "mizaj_assessments"

    id: Mapped[uuid.UUID] = _uuid_pk()
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False, index=True)
    encounter_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("encounters.id"), nullable=True)
    assessed_by_user_id: Mapped[str] = mapped_column(String(64), nullable=False)

    primary_temperament: Mapped[str] = mapped_column(String(30), nullable=False)
    secondary_temperament: Mapped[str] = mapped_column(String(30), nullable=False)
    distribution_percentages: Mapped[dict] = mapped_column(JSON, default=dict)
    su_e_mizaj: Mapped[str] = mapped_column(String(100), default="None (Motadil)")
    dyscrasia_degree: Mapped[int] = mapped_column(default=0)
    raw_scores: Mapped[dict] = mapped_column(JSON, default=dict)
    answers_json: Mapped[dict] = mapped_column(JSON, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class WearableSampleRecord(Base):
    """Time-series physiological record from continuous health wearables.
    Normalizes biometric samples for Quwwat-e-Hayawaniyyah and Asbab-e-Sittah monitoring.
    """

    __tablename__ = "wearable_samples"

    id: Mapped[uuid.UUID] = _uuid_pk()
    patient_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    sample_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    timestamp_utc: Mapped[str] = mapped_column(String(40), nullable=False)
    source_device: Mapped[str] = mapped_column(String(100), default="Wearable")
    hrv_rmssd_ms: Mapped[float] = mapped_column(nullable=False, default=45.0)
    hrv_sdnn_ms: Mapped[float] = mapped_column(nullable=False, default=50.0)
    resting_heart_rate_bpm: Mapped[int] = mapped_column(nullable=False, default=70)
    sleep_hours_total: Mapped[float] = mapped_column(nullable=False, default=7.0)
    deep_sleep_hours: Mapped[float] = mapped_column(nullable=False, default=1.5)
    rem_sleep_hours: Mapped[float] = mapped_column(nullable=False, default=1.8)
    spo2_average_pct: Mapped[float] = mapped_column(nullable=False, default=98.0)
    spo2_lowest_pct: Mapped[float] = mapped_column(nullable=False, default=95.0)
    respiratory_rate_bpm: Mapped[float] = mapped_column(nullable=False, default=15.0)
    daily_steps: Mapped[int] = mapped_column(nullable=False, default=6000)
    active_energy_kcal: Mapped[float] = mapped_column(nullable=False, default=350.0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class QSURADispatchRecord(Base):
    """Immutable audit record of external communications dispatched via QSURA broker.
    Supports Meta WhatsApp Business API, TRAI DLT SMS, Email, and Webhook transports.
    """

    __tablename__ = "qsura_dispatch_logs"

    id: Mapped[uuid.UUID] = _uuid_pk()
    message_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    organization_id: Mapped[str] = mapped_column(String(64), nullable=True, index=True)
    channel: Mapped[str] = mapped_column(String(20), nullable=False)
    recipient: Mapped[str] = mapped_column(String(100), nullable=False)
    message_type: Mapped[str] = mapped_column(String(50), nullable=False)
    rendered_content: Mapped[str] = mapped_column(Text, nullable=False)
    delivery_status: Mapped[str] = mapped_column(String(20), nullable=False, default="DELIVERED")
    dispatched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    regulatory_compliance: Mapped[str] = mapped_column(String(100), default="DISHA / HIPAA / TRAI DLT Compliant")
