from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HakeemConsultRequest(BaseModel):
    patient_id: uuid.UUID
    chief_complaint: str = Field(min_length=1, max_length=2000)
    organ_axis: str | None = None


class HakeemConsultOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    patient_id: uuid.UUID
    chief_complaint: str
    organ_axis: str
    candidate_mufradat: list[dict]
    raw_response: str
    parsed_sections: dict
    is_valid: bool
    missing_sections: list[str]
    reviewed_by_clinician: bool
    converted_to_nuskha_draft_id: str | None
    created_at: datetime


class MarkReviewed(BaseModel):
    converted_to_nuskha_draft_id: str | None = None


class HakeemRefineRequest(BaseModel):
    consultation_id: uuid.UUID
    clinician_feedback: str = Field(min_length=3, max_length=3000)


class HakeemRefineOut(BaseModel):
    consultation_id: uuid.UUID
    valid: bool
    missing_sections: list[str]
    raw_response: str
    sections: dict
    clinician_feedback_applied: str
    zape_personalization: dict
    requires_clinician_review: bool = True


class ZAPEPersonalizeRequest(BaseModel):
    patient_context: dict
    candidate_drugs: list[dict] | None = None
    season: str | None = None


class ZAPEPersonalizeResponse(BaseModel):
    posology: dict
    temperament_modulation: dict
    seasonal_modulation: dict
    overall_summary: str

