"""Initial knowledge schema — creates all Knowledge service PostgreSQL tables.

Covers: source_authors, source_books, source_editions, source_rights,
        source_pages, source_passages, source_translations (source.py)
        and ocr_documents, ocr_segments, ocr_corrections,
        knowledge_extractions (ocr.py).

Revision ID: 0001_initial_knowledge
Revises:
Create Date: 2026-09-14 08:00:00.000000
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_knowledge"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------ #
    # source_authors                                                       #
    # ------------------------------------------------------------------ #
    op.create_table(
        "source_authors",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("canonical_name", sa.String(255), nullable=False),
        sa.Column("arabic_name", sa.String(255), nullable=True),
        sa.Column("persian_name", sa.String(255), nullable=True),
        sa.Column("urdu_name", sa.String(255), nullable=True),
        sa.Column("era_hijri", sa.String(64), nullable=True),
        sa.Column("era_ce", sa.String(64), nullable=True),
        sa.Column("biography_summary", sa.Text(), nullable=True),
        sa.Column("is_classical", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_source_authors_canonical_name"), "source_authors", ["canonical_name"])

    # ------------------------------------------------------------------ #
    # source_books                                                         #
    # ------------------------------------------------------------------ #
    op.create_table(
        "source_books",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("primary_author_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_authors.id"), nullable=True),
        sa.Column("canonical_title", sa.String(255), nullable=False),
        sa.Column("original_title", sa.String(255), nullable=False),
        sa.Column("transliterated_title", sa.String(255), nullable=True),
        sa.Column("language_code", sa.String(10), nullable=False),
        sa.Column("discipline", sa.String(64), nullable=False),
        sa.Column("historical_era", sa.String(64), nullable=True),
        sa.Column("source_type", sa.String(64), nullable=False, server_default="CLASSICAL_TREATISE"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_source_books_canonical_title"), "source_books", ["canonical_title"])

    # ------------------------------------------------------------------ #
    # source_editions                                                      #
    # ------------------------------------------------------------------ #
    op.create_table(
        "source_editions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("book_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_books.id"), nullable=False),
        sa.Column("editor_translator", sa.String(255), nullable=True),
        sa.Column("publisher", sa.String(255), nullable=False),
        sa.Column("publication_year", sa.Integer(), nullable=False),
        sa.Column("publication_place", sa.String(128), nullable=True),
        sa.Column("edition_number", sa.String(32), nullable=True),
        sa.Column("volume_number", sa.String(16), nullable=True),
        sa.Column("isbn_issn", sa.String(32), nullable=True),
        sa.Column("total_pages", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("call_number", sa.String(64), nullable=True),
        sa.Column("digital_scan_url", sa.Text(), nullable=True),
        sa.Column("sha256_checksum", sa.String(64), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_source_editions_book_id"), "source_editions", ["book_id"])

    # ------------------------------------------------------------------ #
    # source_rights                                                        #
    # ------------------------------------------------------------------ #
    op.create_table(
        "source_rights",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("edition_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_editions.id"), nullable=False),
        sa.Column("rights_status", sa.String(64), nullable=False, server_default="unknown"),
        sa.Column("clinical_access", sa.String(64), nullable=False, server_default="research_only"),
        sa.Column("license_type", sa.String(64), nullable=False, server_default="PUBLIC_DOMAIN"),
        sa.Column("rights_holder", sa.String(255), nullable=True),
        sa.Column("licensed_to_facility", sa.String(255), nullable=True),
        sa.Column("valid_from", sa.Date(), nullable=True),
        sa.Column("valid_until", sa.Date(), nullable=True),
        sa.Column("commercial_use_permitted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("ai_training_permitted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("verified_by_legal_officer", sa.String(255), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_source_rights_edition_id"), "source_rights", ["edition_id"])

    # ------------------------------------------------------------------ #
    # source_pages                                                         #
    # ------------------------------------------------------------------ #
    op.create_table(
        "source_pages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("edition_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_editions.id"), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=False),
        sa.Column("folio_recto_verso", sa.String(8), nullable=True),
        sa.Column("image_storage_uri", sa.Text(), nullable=False),
        sa.Column("image_mime_type", sa.String(32), nullable=False, server_default="image/tiff"),
        sa.Column("width_px", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("height_px", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("dpi", sa.Integer(), nullable=False, server_default="300"),
        sa.Column("sha256_page_hash", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("edition_id", "page_number", name="uq_edition_page_number"),
    )
    op.create_index(op.f("ix_source_pages_edition_id"), "source_pages", ["edition_id"])

    # ------------------------------------------------------------------ #
    # source_passages                                                      #
    # ------------------------------------------------------------------ #
    op.create_table(
        "source_passages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("page_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_pages.id"), nullable=False),
        sa.Column("passage_order", sa.Integer(), nullable=False),
        sa.Column("chapter", sa.String(255), nullable=True),
        sa.Column("section", sa.String(255), nullable=True),
        sa.Column("original_text", sa.Text(), nullable=False),
        sa.Column("normalized_text", sa.Text(), nullable=False),
        sa.Column("script_code", sa.String(16), nullable=False, server_default="arab"),
        sa.Column("bounding_box", sa.JSON(), nullable=True),
        sa.Column("is_verse", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_recipe", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_margin_note", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_source_passages_page_id"), "source_passages", ["page_id"])

    # ------------------------------------------------------------------ #
    # source_translations                                                  #
    # ------------------------------------------------------------------ #
    op.create_table(
        "source_translations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("passage_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_passages.id"), nullable=False),
        sa.Column("target_language", sa.String(10), nullable=False),
        sa.Column("translated_text", sa.Text(), nullable=False),
        sa.Column("translator_type", sa.String(32), nullable=False, server_default="HUMAN_EXPERT"),
        sa.Column("translator_name", sa.String(255), nullable=True),
        sa.Column("translation_notes", sa.Text(), nullable=True),
        sa.Column("is_canonical", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_source_translations_passage_id"), "source_translations", ["passage_id"])

    # ------------------------------------------------------------------ #
    # ocr_documents  (ocr.py)                                             #
    # ------------------------------------------------------------------ #
    op.create_table(
        "ocr_documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("edition_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_editions.id"), nullable=False),
        sa.Column("engine_name", sa.String(64), nullable=False),
        sa.Column("engine_version", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="QUEUED"),
        sa.Column("target_scripts", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("overall_confidence", sa.Numeric(4, 3), nullable=True),
        sa.Column("total_pages_processed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("needs_review_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("raw_output_uri", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_ocr_documents_edition_id"), "ocr_documents", ["edition_id"])

    # ------------------------------------------------------------------ #
    # ocr_segments                                                         #
    # ------------------------------------------------------------------ #
    op.create_table(
        "ocr_segments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("ocr_document_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("ocr_documents.id"), nullable=False),
        sa.Column("page_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_pages.id"), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("detected_script", sa.String(16), nullable=False, server_default="arab"),
        sa.Column("detected_language", sa.String(10), nullable=False, server_default="ar"),
        sa.Column("segment_text", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Numeric(4, 3), nullable=False),
        sa.Column("bounding_polygon", sa.JSON(), nullable=True),
        sa.Column("needs_review", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_corrected", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_ocr_segments_ocr_document_id"), "ocr_segments", ["ocr_document_id"])
    op.create_index(op.f("ix_ocr_segments_page_id"), "ocr_segments", ["page_id"])

    # ------------------------------------------------------------------ #
    # ocr_corrections                                                      #
    # ------------------------------------------------------------------ #
    op.create_table(
        "ocr_corrections",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("segment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("ocr_segments.id"), nullable=False),
        sa.Column("original_ocr_text", sa.Text(), nullable=False),
        sa.Column("corrected_text", sa.Text(), nullable=False),
        sa.Column("reviewer_user_id", sa.String(64), nullable=False),
        sa.Column("reviewer_name", sa.String(255), nullable=True),
        sa.Column("correction_notes", sa.Text(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_ocr_corrections_segment_id"), "ocr_corrections", ["segment_id"])

    # ------------------------------------------------------------------ #
    # knowledge_extractions                                                #
    # ------------------------------------------------------------------ #
    op.create_table(
        "knowledge_extractions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("passage_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_passages.id"), nullable=False),
        sa.Column("extracted_entities", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("extraction_confidence", sa.Numeric(4, 3), nullable=False),
        sa.Column("extraction_method", sa.String(64), nullable=False, server_default="PATTERN_DICTIONARY_MATCH"),
        sa.Column("review_status", sa.String(32), nullable=False, server_default="NEEDS_EXPERT_REVIEW"),
        sa.Column("reviewer_user_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_knowledge_extractions_passage_id"), "knowledge_extractions", ["passage_id"])


def downgrade() -> None:
    op.drop_table("knowledge_extractions")
    op.drop_table("ocr_corrections")
    op.drop_table("ocr_segments")
    op.drop_table("ocr_documents")
    op.drop_table("source_translations")
    op.drop_table("source_passages")
    op.drop_table("source_pages")
    op.drop_table("source_rights")
    op.drop_table("source_editions")
    op.drop_table("source_books")
    op.drop_table("source_authors")
