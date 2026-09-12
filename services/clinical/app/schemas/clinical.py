from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PatientCreate(BaseModel):
    mrn: str = Field(min_length=1, max_length=40)
    full_name: str = Field(min_length=1, max_length=200)
    date_of_birth: str | None = Field(default=None, description="ISO date, e.g. 1990-05-14")
    sex: str = Field(pattern="^(female|male|other|unknown)$")
    contact_phone: str = Field(default="", max_length=40)
    contact_email: str = Field(default="", max_length=255)
    emergency_contact: dict = Field(default_factory=dict)
    allergies: list[str] = Field(default_factory=list)
    current_medications: list[str] = Field(default_factory=list)
    current_supplements: list[str] = Field(default_factory=list)
    medical_history: str = Field(default="", max_length=5000)
    surgical_history: str = Field(default="", max_length=5000)
    family_history: str = Field(default="", max_length=5000)
    patient_goals: str = Field(default="", max_length=2000)
    patient_preferences: str = Field(default="", max_length=2000)
    pregnancy_status: str = Field(default="not_applicable", pattern="^(pregnant|not_pregnant|unknown|not_applicable)$")
    comorbidities: list[str] = Field(default_factory=list)
    consent_given: bool = False


class PatientUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    contact_phone: str | None = Field(default=None, max_length=40)
    contact_email: str | None = Field(default=None, max_length=255)
    emergency_contact: dict | None = None
    allergies: list[str] | None = None
    current_medications: list[str] | None = None
    current_supplements: list[str] | None = None
    medical_history: str | None = Field(default=None, max_length=5000)
    surgical_history: str | None = Field(default=None, max_length=5000)
    family_history: str | None = Field(default=None, max_length=5000)
    patient_goals: str | None = Field(default=None, max_length=2000)
    patient_preferences: str | None = Field(default=None, max_length=2000)
    pregnancy_status: str | None = Field(default=None, pattern="^(pregnant|not_pregnant|unknown|not_applicable)$")
    comorbidities: list[str] | None = None
    consent_given: bool | None = None
    is_active: bool | None = None


class PatientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    mrn: str
    full_name: str
    date_of_birth: str | None
    sex: str
    contact_phone: str
    contact_email: str
    emergency_contact: dict
    allergies: list[str]
    current_medications: list[str]
    current_supplements: list[str]
    medical_history: str
    surgical_history: str
    family_history: str
    patient_goals: str
    patient_preferences: str
    pregnancy_status: str
    comorbidities: list[str]
    consent_given: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


class EncounterCreate(BaseModel):
    patient_id: uuid.UUID
    encounter_type: str = Field(default="consultation", pattern="^(consultation|follow_up|telemedicine)$")
    chief_complaint: str = Field(default="", max_length=2000)


class EncounterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    patient_id: uuid.UUID
    clinician_user_id: str
    encounter_type: str
    chief_complaint: str
    status: str
    started_at: datetime
    closed_at: datetime | None


class ClinicalNoteCreate(BaseModel):
    encounter_id: uuid.UUID
    subjective: str = Field(default="", max_length=5000)
    objective: str = Field(default="", max_length=5000)
    assessment: str = Field(default="", max_length=5000)
    plan: str = Field(default="", max_length=5000)


class ClinicalNoteAmend(BaseModel):
    subjective: str = Field(default="", max_length=5000)
    objective: str = Field(default="", max_length=5000)
    assessment: str = Field(default="", max_length=5000)
    plan: str = Field(default="", max_length=5000)


class ClinicalNoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    patient_id: uuid.UUID
    encounter_id: uuid.UUID
    author_user_id: str
    subjective: str
    objective: str
    assessment: str
    plan: str
    amends_note_id: uuid.UUID | None
    is_current: bool
    created_at: datetime


class PrescriptionCreate(BaseModel):
    encounter_id: uuid.UUID
    medication_name: str = Field(min_length=1, max_length=200)
    dose: str = Field(default="", max_length=100)
    frequency: str = Field(default="", max_length=100)
    duration: str = Field(default="", max_length=100)
    instructions: str = Field(default="", max_length=2000)


class PrescriptionDiscontinue(BaseModel):
    reason: str = Field(default="", max_length=1000)


class PrescriptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    patient_id: uuid.UUID
    encounter_id: uuid.UUID
    prescribed_by_user_id: str
    medication_name: str
    dose: str
    frequency: str
    duration: str
    instructions: str
    status: str
    discontinued_at: datetime | None
    discontinued_reason: str
    created_at: datetime


class AppointmentCreate(BaseModel):
    patient_id: uuid.UUID
    scheduled_at: datetime
    duration_minutes: int = Field(default=20, ge=5, le=240)
    reason: str = Field(default="", max_length=1000)


class AppointmentUpdate(BaseModel):
    status: str | None = Field(default=None, pattern="^(scheduled|completed|cancelled|no_show)$")
    scheduled_at: datetime | None = None
    reason: str | None = Field(default=None, max_length=1000)


class AppointmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    patient_id: uuid.UUID
    clinician_user_id: str
    scheduled_at: datetime
    duration_minutes: int
    status: str
    reason: str
    created_at: datetime


class TimelineEvent(BaseModel):
    event_type: str  # encounter | clinical_note | prescription | appointment
    event_id: uuid.UUID
    occurred_at: datetime
    summary: str


class MizajAssessmentCreate(BaseModel):
    encounter_id: uuid.UUID | None = None
    answers: dict[str, str] = Field(
        ...,
        description="10-Ajnas responses (malmas, lahm_shahm, ashar, laun, hayat_aza, kayfiyyat_infial, naum_yaqzah, harkat_sukoon, fuzalaat, afal_aza)",
    )


class MizajAssessmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    patient_id: uuid.UUID
    encounter_id: uuid.UUID | None
    assessed_by_user_id: str
    primary_temperament: str
    secondary_temperament: str
    distribution_percentages: dict
    su_e_mizaj: str
    dyscrasia_degree: int
    raw_scores: dict
    answers_json: dict
    created_at: datetime


class OrganAxisAnalysisRequest(BaseModel):
    complaint: str = Field(min_length=2, max_length=1000)
    associated_symptoms: list[str] = Field(default_factory=list)
    duration_days: int | None = Field(default=None, ge=1, le=3650)
    symptom_acuity: str = Field(default="moderate", pattern="^(mild|moderate|severe)$")
    inflammatory_signs: bool = Field(default=False)
    temperament_context: dict = Field(default_factory=dict)


class OrganAxisAnalysisResponse(BaseModel):
    complaint: str
    organ_axes: dict
    asbab_e_arbaa: dict
    dawr_e_marad: dict

