"""OCR Extraction and Scholarly Correction Schema

Revision ID: 0002_ocr_and_extraction
Revises: 0001_initial_source_library
Create Date: 2026-09-14 00:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0002_ocr_and_extraction"
down_revision: Union[str, None] = "0001_initial_source_library"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. ocr_documents
    op.create_table(
        "ocr_documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("edition_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_editions.id"), nullable=False, index=True),
        sa.Column("engine_name", sa.String(length=64), nullable=False),
        sa.Column("engine_version", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="QUEUED"),
        sa.Column("target_scripts", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("overall_confidence", sa.Numeric(precision=4, scale=3), nullable=True),
        sa.Column("total_pages_processed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("needs_review_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("raw_output_uri", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 2. ocr_segments
    op.create_table(
        "ocr_segments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("ocr_document_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("ocr_documents.id"), nullable=False, index=True),
        sa.Column("page_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_pages.id"), nullable=False, index=True),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("detected_script", sa.String(length=16), nullable=False, server_default="arab"),
        sa.Column("detected_language", sa.String(length=10), nullable=False, server_default="ar"),
        sa.Column("segment_text", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Numeric(precision=4, scale=3), nullable=False),
        sa.Column("bounding_polygon", sa.JSON(), nullable=True),
        sa.Column("needs_review", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_corrected", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 3. ocr_corrections
    op.create_table(
        "ocr_corrections",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("segment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("ocr_segments.id"), nullable=False, index=True),
        sa.Column("original_ocr_text", sa.Text(), nullable=False),
        sa.Column("corrected_text", sa.Text(), nullable=False),
        sa.Column("reviewer_user_id", sa.String(length=64), nullable=False),
        sa.Column("reviewer_name", sa.String(length=255), nullable=True),
        sa.Column("correction_notes", sa.Text(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 4. knowledge_extractions
    op.create_table(
        "knowledge_extractions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("passage_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_passages.id"), nullable=False, index=True),
        sa.Column("extracted_entities", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("extraction_confidence", sa.Numeric(precision=4, scale=3), nullable=False),
        sa.Column("extraction_method", sa.String(length=64), nullable=False, server_default="PATTERN_DICTIONARY_MATCH"),
        sa.Column("review_status", sa.String(length=32), nullable=False, server_default="NEEDS_EXPERT_REVIEW"),
        sa.Column("reviewer_user_id", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("knowledge_extractions")
    op.drop_table("ocr_corrections")
    op.drop_table("ocr_segments")
    op.drop_table("ocr_documents")
