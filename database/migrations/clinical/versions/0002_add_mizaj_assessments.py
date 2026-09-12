"""Add mizaj_assessments table

Revision ID: 0002_add_mizaj_assessments
Revises: 0001_initial_clinical
Create Date: 2026-09-11 16:42:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0002_add_mizaj_assessments"
down_revision: Union[str, None] = "0001_initial_clinical"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "mizaj_assessments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False, index=True),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("encounters.id"), nullable=True),
        sa.Column("assessed_by_user_id", sa.String(length=64), nullable=False),
        sa.Column("primary_temperament", sa.String(length=30), nullable=False),
        sa.Column("secondary_temperament", sa.String(length=30), nullable=False),
        sa.Column("distribution_percentages", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("su_e_mizaj", sa.String(length=100), nullable=False, server_default="None (Motadil)"),
        sa.Column("dyscrasia_degree", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("raw_scores", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("answers_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("mizaj_assessments")
