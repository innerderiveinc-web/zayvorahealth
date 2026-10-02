"""
ZAYVORA Knowledge Base (ZKB) — OCR Extraction & Scholarly Correction Models
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional

try:
    from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, Numeric, String, Text
    from sqlalchemy.dialects.postgresql import UUID
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
    from app.models.source import Base
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False
    class Base:
        pass


def _now() -> datetime:
    return datetime.now(timezone.utc)


if HAS_SQLALCHEMY:
    class OcrDocument(Base):
        __tablename__ = "ocr_documents"

        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        edition_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("source_editions.id"), nullable=False, index=True)
        engine_name: Mapped[str] = mapped_column(String(64), nullable=False)
        engine_version: Mapped[str] = mapped_column(String(32), nullable=False)
        status: Mapped[str] = mapped_column(String(32), default="QUEUED", nullable=False)
        target_scripts: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
        overall_confidence: Mapped[Optional[float]] = mapped_column(Numeric(4, 3), nullable=True)
        total_pages_processed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
        needs_review_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
        started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
        completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
        raw_output_uri: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)

        segments = relationship("OcrSegment", back_populates="document", cascade="all, delete-orphan")

    class OcrSegment(Base):
        __tablename__ = "ocr_segments"

        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        ocr_document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ocr_documents.id"), nullable=False, index=True)
        page_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("source_pages.id"), nullable=False, index=True)
        line_number: Mapped[int] = mapped_column(Integer, nullable=False)
        detected_script: Mapped[str] = mapped_column(String(16), default="arab", nullable=False)
        detected_language: Mapped[str] = mapped_column(String(10), default="ar", nullable=False)
        segment_text: Mapped[str] = mapped_column(Text, nullable=False)
        confidence: Mapped[float] = mapped_column(Numeric(4, 3), nullable=False)
        bounding_polygon: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
        needs_review: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
        is_corrected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)

        document = relationship("OcrDocument", back_populates="segments")
        corrections = relationship("OcrCorrection", back_populates="segment", cascade="all, delete-orphan")

    class OcrCorrection(Base):
        __tablename__ = "ocr_corrections"

        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        segment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ocr_segments.id"), nullable=False, index=True)
        original_ocr_text: Mapped[str] = mapped_column(Text, nullable=False)
        corrected_text: Mapped[str] = mapped_column(Text, nullable=False)
        reviewer_user_id: Mapped[str] = mapped_column(String(64), nullable=False)
        reviewer_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        correction_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
        reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)

        segment = relationship("OcrSegment", back_populates="corrections")

    class KnowledgeExtraction(Base):
        __tablename__ = "knowledge_extractions"

        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        passage_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("source_passages.id"), nullable=False, index=True)
        extracted_entities: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
        extraction_confidence: Mapped[float] = mapped_column(Numeric(4, 3), nullable=False)
        extraction_method: Mapped[str] = mapped_column(String(64), default="PATTERN_DICTIONARY_MATCH", nullable=False)
        review_status: Mapped[str] = mapped_column(String(32), default="NEEDS_EXPERT_REVIEW", nullable=False)
        reviewer_user_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
