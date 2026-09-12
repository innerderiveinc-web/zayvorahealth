"""Add unified_care_plans table

Revision ID: 0002_add_unified_care_plans
Revises: 0001_initial_therapeutic
Create Date: 2026-09-11 16:40:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0002_add_unified_care_plans"
down_revision: Union[str, None] = "0001_initial_therapeutic"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "unified_care_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("created_by_user_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("horizon", sa.String(length=30), nullable=False, server_default="stabilization"),
        sa.Column("duration_days", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("mizaj_context", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("usool_e_ilaj", sa.Text(), nullable=False, server_default=""),
        sa.Column("primary_indication", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("ilaj_bid_dawa", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("ilaj_bit_tadbeer", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("ilaj_bil_ghiza", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("asbab_sittah", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("review_milestones", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("prognosis_notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("safe_to_lock", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("signed_by_clinician_id", sa.String(length=64), nullable=True),
        sa.Column("clinician_registration_number", sa.String(length=100), nullable=False, server_default=""),
        sa.Column("signed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("unified_care_plans")
