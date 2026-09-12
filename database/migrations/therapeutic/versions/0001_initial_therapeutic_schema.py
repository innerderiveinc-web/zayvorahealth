"""Initial therapeutic schema (nuskha_drafts, tadbeer_plans, ghiza_plans)

Revision ID: 0001_initial_therapeutic
Revises: 
Create Date: 2026-09-11 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_therapeutic"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. nuskha_drafts
    op.create_table(
        "nuskha_drafts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("created_by_user_id", sa.String(length=64), nullable=False),
        sa.Column("mizaj_context", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("asbab", sa.Text(), nullable=False, server_default=""),
        sa.Column("tashkhis", sa.Text(), nullable=False, server_default=""),
        sa.Column("organ_axis_context", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("usool_e_ilaj", sa.Text(), nullable=False, server_default=""),
        sa.Column("therapeutic_objective", sa.Text(), nullable=False, server_default=""),
        sa.Column("ingredients", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("dosage_form", sa.String(length=100), nullable=False, server_default=""),
        sa.Column("dose", sa.String(length=200), nullable=False, server_default=""),
        sa.Column("timing", sa.String(length=200), nullable=False, server_default=""),
        sa.Column("duration", sa.String(length=200), nullable=False, server_default=""),
        sa.Column("parhez", sa.Text(), nullable=False, server_default=""),
        sa.Column("safety_verdict", sa.String(length=30), nullable=False),
        sa.Column("safety_reasons", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="draft"),
        sa.Column("reviewed_by_user_id", sa.String(length=64), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rejection_reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("safety_override_justification", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 2. tadbeer_plans
    op.create_table(
        "tadbeer_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("created_by_user_id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("category", sa.String(length=40), nullable=False),
        sa.Column("indication", sa.Text(), nullable=False, server_default=""),
        sa.Column("method", sa.Text(), nullable=False, server_default=""),
        sa.Column("frequency", sa.String(length=100), nullable=False, server_default=""),
        sa.Column("duration", sa.String(length=100), nullable=False, server_default=""),
        sa.Column("contraindications", sa.Text(), nullable=False, server_default=""),
        sa.Column("practitioner_requirements", sa.Text(), nullable=False, server_default=""),
        sa.Column("safety_verdict", sa.String(length=30), nullable=False, server_default="SAFE_TO_CONSIDER"),
        sa.Column("safety_reasons", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 3. ghiza_plans
    op.create_table(
        "ghiza_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("created_by_user_id", sa.String(length=64), nullable=False),
        sa.Column("dietary_goals", sa.Text(), nullable=False, server_default=""),
        sa.Column("meal_structure", sa.Text(), nullable=False, server_default=""),
        sa.Column("foods_recommended", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("foods_to_limit", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("hydration_guidance", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("ghiza_plans")
    op.drop_table("tadbeer_plans")
    op.drop_table("nuskha_drafts")
