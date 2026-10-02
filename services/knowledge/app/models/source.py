"""
ZAYVORA Knowledge Base (ZKB) — Source Library & Provenance Models
Supports Classical Treatises, Pharmacopoeias, Manuscripts, Rights Management,
Page Scans, Passage Segmentation, and Scholarly Translations.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone, date
from typing import Any, Optional

try:
    from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint, func
    from sqlalchemy.dialects.postgresql import UUID
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

    class Base(DeclarativeBase):
        pass

    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False
    class Base:
        pass


def _uuid_str() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


if HAS_SQLALCHEMY:
    class SourceAuthor(Base):
        __tablename__ = "source_authors"

        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        canonical_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
        arabic_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        persian_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        urdu_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        era_hijri: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
        era_ce: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
        biography_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
        is_classical: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now, nullable=False)

        books = relationship("SourceBook", back_populates="author")

    class SourceBook(Base):
        __tablename__ = "source_books"

        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        primary_author_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("source_authors.id"), nullable=True)
        canonical_title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
        original_title: Mapped[str] = mapped_column(String(255), nullable=False)
        transliterated_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        language_code: Mapped[str] = mapped_column(String(10), nullable=False) # ar, ur, fa, hi, en
        discipline: Mapped[str] = mapped_column(String(64), nullable=False) # Kulliyat, Mufradat, Murakkabat, Moalajat
        historical_era: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
        source_type: Mapped[str] = mapped_column(String(64), default="CLASSICAL_TREATISE", nullable=False)
        description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now, nullable=False)

        author = relationship("SourceAuthor", back_populates="books")
        editions = relationship("SourceEdition", back_populates="book", cascade="all, delete-orphan")

    class SourceEdition(Base):
        __tablename__ = "source_editions"

        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        book_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("source_books.id"), nullable=False, index=True)
        editor_translator: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        publisher: Mapped[str] = mapped_column(String(255), nullable=False)
        publication_year: Mapped[int] = mapped_column(Integer, nullable=False)
        publication_place: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
        edition_number: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
        volume_number: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
        isbn_issn: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
        total_pages: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
        call_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
        digital_scan_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
        sha256_checksum: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now, nullable=False)

        book = relationship("SourceBook", back_populates="editions")
        rights = relationship("SourceRights", back_populates="edition", uselist=False, cascade="all, delete-orphan")
        pages = relationship("SourcePage", back_populates="edition", cascade="all, delete-orphan")

    class SourceRights(Base):
        __tablename__ = "source_rights"

        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        edition_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("source_editions.id"), nullable=False, index=True)
        rights_status: Mapped[str] = mapped_column(String(64), default="unknown", nullable=False)
        clinical_access: Mapped[str] = mapped_column(String(64), default="research_only", nullable=False)
        license_type: Mapped[str] = mapped_column(String(64), default="PUBLIC_DOMAIN", nullable=False)
        rights_holder: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        licensed_to_facility: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        valid_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
        valid_until: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
        commercial_use_permitted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
        ai_training_permitted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
        verified_by_legal_officer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)

        edition = relationship("SourceEdition", back_populates="rights")

    class SourcePage(Base):
        __tablename__ = "source_pages"
        __table_args__ = (
            UniqueConstraint("edition_id", "page_number", name="uq_edition_page_number"),
        )

        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        edition_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("source_editions.id"), nullable=False, index=True)
        page_number: Mapped[int] = mapped_column(Integer, nullable=False)
        folio_recto_verso: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
        image_storage_uri: Mapped[str] = mapped_column(Text, nullable=False)
        image_mime_type: Mapped[str] = mapped_column(String(32), default="image/tiff", nullable=False)
        width_px: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
        height_px: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
        dpi: Mapped[int] = mapped_column(Integer, default=300, nullable=False)
        sha256_page_hash: Mapped[str] = mapped_column(String(64), nullable=False)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)

        edition = relationship("SourceEdition", back_populates="pages")
        passages = relationship("SourcePassage", back_populates="page", cascade="all, delete-orphan")

    class SourcePassage(Base):
        __tablename__ = "source_passages"

        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        page_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("source_pages.id"), nullable=False, index=True)
        passage_order: Mapped[int] = mapped_column(Integer, nullable=False)
        chapter: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        section: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        original_text: Mapped[str] = mapped_column(Text, nullable=False)
        normalized_text: Mapped[str] = mapped_column(Text, nullable=False)
        script_code: Mapped[str] = mapped_column(String(16), default="arab", nullable=False)
        bounding_box: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
        is_verse: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
        is_recipe: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
        is_margin_note: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)

        page = relationship("SourcePage", back_populates="passages")
        translations = relationship("SourceTranslation", back_populates="passage", cascade="all, delete-orphan")

    class SourceTranslation(Base):
        __tablename__ = "source_translations"

        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        passage_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("source_passages.id"), nullable=False, index=True)
        target_language: Mapped[str] = mapped_column(String(10), nullable=False) # en, ur, hi, ar
        translated_text: Mapped[str] = mapped_column(Text, nullable=False)
        translator_type: Mapped[str] = mapped_column(String(32), default="HUMAN_EXPERT", nullable=False)
        translator_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        translation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
        is_canonical: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)

        passage = relationship("SourcePassage", back_populates="translations")
