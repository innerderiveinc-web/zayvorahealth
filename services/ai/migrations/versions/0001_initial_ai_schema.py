"""Initial AI service schema — creates ai_consultations table.

Revision ID: 0001_initial_ai
Revises: 
Create Date: 2026-09-14 08:00:00.000000
"""
from __future__ import annotations

from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_ai"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------ #
    # ai_consultations                                                   #
    # ------------------------------------------------------------------ #
    op.create_table(
        "ai_consultations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("requested_by_user_id", sa.String(64), nullable=False),
        sa.Column("chief_complaint", sa.Text(), nullable=False, server_default=""),
        sa.Column("organ_axis", sa.String(80), nullable=False, server_default=""),
        sa.Column("candidate_mufradat", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("raw_response", sa.Text(), nullable=False, server_default=""),
        sa.Column("parsed_sections", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("is_valid", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("missing_sections", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("reviewed_by_clinician", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("converted_to_nuskha_draft_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_ai_consultations_organization_id"), "ai_consultations", ["organization_id"])
    op.create_index(op.f("ix_ai_consultations_patient_id"), "ai_consultations", ["patient_id"])


def downgrade() -> None:
    op.drop_table("ai_consultations")
