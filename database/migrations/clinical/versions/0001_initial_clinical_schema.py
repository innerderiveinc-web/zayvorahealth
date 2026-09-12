"""Initial clinical schema (patients, encounters, clinical_notes, prescriptions, appointments)

Revision ID: 0001_initial_clinical
Revises: 
Create Date: 2026-09-11 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_clinical"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. patients
    op.create_table(
        "patients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("mrn", sa.String(length=40), nullable=False),
        sa.Column("full_name", sa.String(length=200), nullable=False),
        sa.Column("date_of_birth", sa.String(length=10), nullable=True),
        sa.Column("sex", sa.String(length=20), nullable=False),
        sa.Column("contact_phone", sa.String(length=40), nullable=False, server_default=""),
        sa.Column("contact_email", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("emergency_contact", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("allergies", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("current_medications", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("current_supplements", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("medical_history", sa.Text(), nullable=False, server_default=""),
        sa.Column("surgical_history", sa.Text(), nullable=False, server_default=""),
        sa.Column("family_history", sa.Text(), nullable=False, server_default=""),
        sa.Column("patient_goals", sa.Text(), nullable=False, server_default=""),
        sa.Column("patient_preferences", sa.Text(), nullable=False, server_default=""),
        sa.Column("pregnancy_status", sa.String(length=30), nullable=False, server_default="not_applicable"),
        sa.Column("comorbidities", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("consent_given", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_by_user_id", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 2. encounters
    op.create_table(
        "encounters",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False, index=True),
        sa.Column("clinician_user_id", sa.String(length=64), nullable=False),
        sa.Column("encounter_type", sa.String(length=40), nullable=False, server_default="consultation"),
        sa.Column("chief_complaint", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="open"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 3. clinical_notes
    op.create_table(
        "clinical_notes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False, index=True),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("encounters.id"), nullable=False, index=True),
        sa.Column("author_user_id", sa.String(length=64), nullable=False),
        sa.Column("subjective", sa.Text(), nullable=False, server_default=""),
        sa.Column("objective", sa.Text(), nullable=False, server_default=""),
        sa.Column("assessment", sa.Text(), nullable=False, server_default=""),
        sa.Column("plan", sa.Text(), nullable=False, server_default=""),
        sa.Column("amends_note_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("clinical_notes.id"), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 4. prescriptions
    op.create_table(
        "prescriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False, index=True),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("encounters.id"), nullable=False, index=True),
        sa.Column("prescribed_by_user_id", sa.String(length=64), nullable=False),
        sa.Column("medication_name", sa.String(length=200), nullable=False),
        sa.Column("dose", sa.String(length=100), nullable=False, server_default=""),
        sa.Column("frequency", sa.String(length=100), nullable=False, server_default=""),
        sa.Column("duration", sa.String(length=100), nullable=False, server_default=""),
        sa.Column("instructions", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("discontinued_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("discontinued_reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 5. appointments
    op.create_table(
        "appointments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False, index=True),
        sa.Column("clinician_user_id", sa.String(length=64), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="scheduled"),
        sa.Column("reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("appointments")
    op.drop_table("prescriptions")
    op.drop_table("clinical_notes")
    op.drop_table("encounters")
    op.drop_table("patients")
