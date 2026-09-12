"""Initial AI schema (ai_consultations audit trail)

Revision ID: 0001_initial_ai
Revises: 
Create Date: 2026-09-11 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_ai"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ai_consultations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("requested_by_user_id", sa.String(length=64), nullable=False),
        sa.Column("chief_complaint", sa.Text(), nullable=False, server_default=""),
        sa.Column("organ_axis", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("candidate_mufradat", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("raw_response", sa.Text(), nullable=False, server_default=""),
        sa.Column("parsed_sections", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("is_valid", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("missing_sections", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("reviewed_by_clinician", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("converted_to_nuskha_draft_id", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("ai_consultations")
