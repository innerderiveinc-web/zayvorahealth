"""Initial Source Library and Provenance Schema

Revision ID: 0001_initial_source_library
Revises: 
Create Date: 2026-09-14 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_source_library"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. source_authors
    op.create_table(
        "source_authors",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("canonical_name", sa.String(length=255), nullable=False, index=True),
        sa.Column("arabic_name", sa.String(length=255), nullable=True),
        sa.Column("persian_name", sa.String(length=255), nullable=True),
        sa.Column("urdu_name", sa.String(length=255), nullable=True),
        sa.Column("era_hijri", sa.String(length=64), nullable=True),
        sa.Column("era_ce", sa.String(length=64), nullable=True),
        sa.Column("biography_summary", sa.Text(), nullable=True),
        sa.Column("is_classical", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 2. source_books
    op.create_table(
        "source_books",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("primary_author_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_authors.id"), nullable=True),
        sa.Column("canonical_title", sa.String(length=255), nullable=False, index=True),
        sa.Column("original_title", sa.String(length=255), nullable=False),
        sa.Column("transliterated_title", sa.String(length=255), nullable=True),
        sa.Column("language_code", sa.String(length=10), nullable=False),
        sa.Column("discipline", sa.String(length=64), nullable=False),
        sa.Column("historical_era", sa.String(length=64), nullable=True),
        sa.Column("source_type", sa.String(length=64), nullable=False, server_default="CLASSICAL_TREATISE"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 3. source_editions
    op.create_table(
        "source_editions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("book_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_books.id"), nullable=False, index=True),
        sa.Column("editor_translator", sa.String(length=255), nullable=True),
        sa.Column("publisher", sa.String(length=255), nullable=False),
        sa.Column("publication_year", sa.Integer(), nullable=False),
        sa.Column("publication_place", sa.String(length=128), nullable=True),
        sa.Column("edition_number", sa.String(length=32), nullable=True),
        sa.Column("volume_number", sa.String(length=16), nullable=True),
        sa.Column("isbn_issn", sa.String(length=32), nullable=True),
        sa.Column("total_pages", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("call_number", sa.String(length=64), nullable=True),
        sa.Column("digital_scan_url", sa.Text(), nullable=True),
        sa.Column("sha256_checksum", sa.String(length=64), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 4. source_rights
    op.create_table(
        "source_rights",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("edition_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_editions.id"), nullable=False, index=True),
        sa.Column("rights_status", sa.String(length=64), nullable=False, server_default="unknown"),
        sa.Column("clinical_access", sa.String(length=64), nullable=False, server_default="research_only"),
        sa.Column("license_type", sa.String(length=64), nullable=False, server_default="PUBLIC_DOMAIN"),
        sa.Column("rights_holder", sa.String(length=255), nullable=True),
        sa.Column("licensed_to_facility", sa.String(length=255), nullable=True),
        sa.Column("valid_from", sa.Date(), nullable=True),
        sa.Column("valid_until", sa.Date(), nullable=True),
        sa.Column("commercial_use_permitted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("ai_training_permitted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("verified_by_legal_officer", sa.String(length=255), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 5. source_pages
    op.create_table(
        "source_pages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("edition_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_editions.id"), nullable=False, index=True),
        sa.Column("page_number", sa.Integer(), nullable=False),
        sa.Column("folio_recto_verso", sa.String(length=8), nullable=True),
        sa.Column("image_storage_uri", sa.Text(), nullable=False),
        sa.Column("image_mime_type", sa.String(length=32), nullable=False, server_default="image/tiff"),
        sa.Column("width_px", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("height_px", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("dpi", sa.Integer(), nullable=False, server_default="300"),
        sa.Column("sha256_page_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("edition_id", "page_number", name="uq_edition_page_number"),
    )

    # 6. source_passages
    op.create_table(
        "source_passages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("page_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_pages.id"), nullable=False, index=True),
        sa.Column("passage_order", sa.Integer(), nullable=False),
        sa.Column("chapter", sa.String(length=255), nullable=True),
        sa.Column("section", sa.String(length=255), nullable=True),
        sa.Column("original_text", sa.Text(), nullable=False),
        sa.Column("normalized_text", sa.Text(), nullable=False),
        sa.Column("script_code", sa.String(length=16), nullable=False, server_default="arab"),
        sa.Column("bounding_box", sa.JSON(), nullable=True),
        sa.Column("is_verse", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_recipe", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_margin_note", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 7. source_translations
    op.create_table(
        "source_translations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("passage_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("source_passages.id"), nullable=False, index=True),
        sa.Column("target_language", sa.String(length=10), nullable=False),
        sa.Column("translated_text", sa.Text(), nullable=False),
        sa.Column("translator_type", sa.String(length=32), nullable=False, server_default="HUMAN_EXPERT"),
        sa.Column("translator_name", sa.String(length=255), nullable=True),
        sa.Column("translation_notes", sa.Text(), nullable=True),
        sa.Column("is_canonical", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("source_translations")
    op.drop_table("source_passages")
    op.drop_table("source_pages")
    op.drop_table("source_rights")
    op.drop_table("source_editions")
    op.drop_table("source_books")
    op.drop_table("source_authors")
