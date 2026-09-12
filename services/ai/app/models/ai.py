"""
Master Build Prompt v4.0 §50 AI Governance: every AI recommendation
needs an audit trail (Patient Data -> Retrieved Knowledge -> Reasoning ->
Safety -> Recommendation -> Clinician Decision -> Final Action). This
table is that trail's storage — every Hakeem Sahab consultation is
recorded here, valid or not, before it's returned to the caller.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def _now() -> datetime:
    return datetime.now(timezone.utc)


class AiConsultation(Base):
    __tablename__ = "ai_consultations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    requested_by_user_id: Mapped[str] = mapped_column(String(64), nullable=False)

    chief_complaint: Mapped[str] = mapped_column(Text, default="")
    organ_axis: Mapped[str] = mapped_column(String(80), default="")
    candidate_mufradat: Mapped[list] = mapped_column(JSON, default=list)

    raw_response: Mapped[str] = mapped_column(Text, default="")
    parsed_sections: Mapped[dict] = mapped_column(JSON, default=dict)
    is_valid: Mapped[bool] = mapped_column(Boolean, default=False)
    missing_sections: Mapped[list] = mapped_column(JSON, default=list)

    reviewed_by_clinician: Mapped[bool] = mapped_column(Boolean, default=False)
    converted_to_nuskha_draft_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
