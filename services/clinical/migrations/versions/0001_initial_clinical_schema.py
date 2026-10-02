"""Initial clinical schema — creates all Clinical service tables.

Revision ID: 0001_initial_clinical
Revises:
Create Date: 2026-09-14 08:00:00.000000
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_clinical"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------ #
    # patients                                                             #
    # ------------------------------------------------------------------ #
    op.create_table(
        "patients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("mrn", sa.String(40), nullable=False),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("date_of_birth", sa.String(10), nullable=True),
        sa.Column("sex", sa.String(20), nullable=False),
        sa.Column("contact_phone", sa.String(40), nullable=False, server_default=""),
        sa.Column("contact_email", sa.String(255), nullable=False, server_default=""),
        sa.Column("emergency_contact", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("allergies", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("current_medications", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("current_supplements", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("medical_history", sa.Text(), nullable=False, server_default=""),
        sa.Column("surgical_history", sa.Text(), nullable=False, server_default=""),
        sa.Column("family_history", sa.Text(), nullable=False, server_default=""),
        sa.Column("patient_goals", sa.Text(), nullable=False, server_default=""),
        sa.Column("patient_preferences", sa.Text(), nullable=False, server_default=""),
        sa.Column("pregnancy_status", sa.String(30), nullable=False, server_default="not_applicable"),
        sa.Column("comorbidities", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("consent_given", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_by_user_id", sa.String(64), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_patients_org_mrn", "patients", ["organization_id", "mrn"])
    op.create_index(op.f("ix_patients_organization_id"), "patients", ["organization_id"])

    # ------------------------------------------------------------------ #
    # encounters                                                           #
    # ------------------------------------------------------------------ #
    op.create_table(
        "encounters",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("clinician_user_id", sa.String(64), nullable=False),
        sa.Column("encounter_type", sa.String(40), nullable=False, server_default="consultation"),
        sa.Column("chief_complaint", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(20), nullable=False, server_default="open"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("idx_encounters_org_patient_status", "encounters", ["organization_id", "patient_id", "status"])
    op.create_index(op.f("ix_encounters_organization_id"), "encounters", ["organization_id"])
    op.create_index(op.f("ix_encounters_patient_id"), "encounters", ["patient_id"])

    # ------------------------------------------------------------------ #
    # clinical_notes                                                       #
    # ------------------------------------------------------------------ #
    op.create_table(
        "clinical_notes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("encounters.id"), nullable=False),
        sa.Column("author_user_id", sa.String(64), nullable=False),
        sa.Column("subjective", sa.Text(), nullable=False, server_default=""),
        sa.Column("objective", sa.Text(), nullable=False, server_default=""),
        sa.Column("assessment", sa.Text(), nullable=False, server_default=""),
        sa.Column("plan", sa.Text(), nullable=False, server_default=""),
        sa.Column("amends_note_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("clinical_notes.id"), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_clinical_notes_organization_id"), "clinical_notes", ["organization_id"])
    op.create_index(op.f("ix_clinical_notes_patient_id"), "clinical_notes", ["patient_id"])
    op.create_index(op.f("ix_clinical_notes_encounter_id"), "clinical_notes", ["encounter_id"])

    # ------------------------------------------------------------------ #
    # prescriptions                                                        #
    # ------------------------------------------------------------------ #
    op.create_table(
        "prescriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("encounters.id"), nullable=False),
        sa.Column("prescribed_by_user_id", sa.String(64), nullable=False),
        sa.Column("medication_name", sa.String(200), nullable=False),
        sa.Column("dose", sa.String(100), nullable=False, server_default=""),
        sa.Column("frequency", sa.String(100), nullable=False, server_default=""),
        sa.Column("duration", sa.String(100), nullable=False, server_default=""),
        sa.Column("instructions", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("discontinued_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("discontinued_reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_prescriptions_org_patient_status", "prescriptions", ["organization_id", "patient_id", "status"])
    op.create_index(op.f("ix_prescriptions_organization_id"), "prescriptions", ["organization_id"])
    op.create_index(op.f("ix_prescriptions_patient_id"), "prescriptions", ["patient_id"])

    # ------------------------------------------------------------------ #
    # appointments                                                         #
    # ------------------------------------------------------------------ #
    op.create_table(
        "appointments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("clinician_user_id", sa.String(64), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("status", sa.String(20), nullable=False, server_default="scheduled"),
        sa.Column("reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_appointments_organization_id"), "appointments", ["organization_id"])
    op.create_index(op.f("ix_appointments_patient_id"), "appointments", ["patient_id"])

    # ------------------------------------------------------------------ #
    # mizaj_assessments                                                    #
    # ------------------------------------------------------------------ #
    op.create_table(
        "mizaj_assessments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("encounters.id"), nullable=True),
        sa.Column("assessed_by_user_id", sa.String(64), nullable=False),
        sa.Column("primary_temperament", sa.String(30), nullable=False),
        sa.Column("secondary_temperament", sa.String(30), nullable=False),
        sa.Column("distribution_percentages", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("su_e_mizaj", sa.String(100), nullable=False, server_default="None (Motadil)"),
        sa.Column("dyscrasia_degree", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("raw_scores", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("answers_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_mizaj_assessments_organization_id"), "mizaj_assessments", ["organization_id"])
    op.create_index(op.f("ix_mizaj_assessments_patient_id"), "mizaj_assessments", ["patient_id"])

    # ------------------------------------------------------------------ #
    # wearable_samples                                                     #
    # ------------------------------------------------------------------ #
    op.create_table(
        "wearable_samples",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("patient_id", sa.String(64), nullable=False),
        sa.Column("sample_id", sa.String(64), nullable=False, unique=True),
        sa.Column("timestamp_utc", sa.String(40), nullable=False),
        sa.Column("source_device", sa.String(100), nullable=False, server_default="Wearable"),
        sa.Column("hrv_rmssd_ms", sa.Float(), nullable=False, server_default="45.0"),
        sa.Column("hrv_sdnn_ms", sa.Float(), nullable=False, server_default="50.0"),
        sa.Column("resting_heart_rate_bpm", sa.Integer(), nullable=False, server_default="70"),
        sa.Column("sleep_hours_total", sa.Float(), nullable=False, server_default="7.0"),
        sa.Column("deep_sleep_hours", sa.Float(), nullable=False, server_default="1.5"),
        sa.Column("rem_sleep_hours", sa.Float(), nullable=False, server_default="1.8"),
        sa.Column("spo2_average_pct", sa.Float(), nullable=False, server_default="98.0"),
        sa.Column("spo2_lowest_pct", sa.Float(), nullable=False, server_default="95.0"),
        sa.Column("respiratory_rate_bpm", sa.Float(), nullable=False, server_default="15.0"),
        sa.Column("daily_steps", sa.Integer(), nullable=False, server_default="6000"),
        sa.Column("active_energy_kcal", sa.Float(), nullable=False, server_default="350.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_wearable_samples_patient_id"), "wearable_samples", ["patient_id"])
    op.create_index(op.f("ix_wearable_samples_sample_id"), "wearable_samples", ["sample_id"])

    # ------------------------------------------------------------------ #
    # qsura_dispatch_logs                                                  #
    # ------------------------------------------------------------------ #
    op.create_table(
        "qsura_dispatch_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("message_id", sa.String(64), nullable=False, unique=True),
        sa.Column("organization_id", sa.String(64), nullable=True),
        sa.Column("channel", sa.String(20), nullable=False),
        sa.Column("recipient", sa.String(100), nullable=False),
        sa.Column("message_type", sa.String(50), nullable=False),
        sa.Column("rendered_content", sa.Text(), nullable=False),
        sa.Column("delivery_status", sa.String(20), nullable=False, server_default="DELIVERED"),
        sa.Column("dispatched_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("regulatory_compliance", sa.String(100), nullable=False, server_default="DISHA / HIPAA / TRAI DLT Compliant"),
    )
    op.create_index(op.f("ix_qsura_dispatch_logs_message_id"), "qsura_dispatch_logs", ["message_id"])
    op.create_index(op.f("ix_qsura_dispatch_logs_organization_id"), "qsura_dispatch_logs", ["organization_id"])

    # ------------------------------------------------------------------ #
    # payment_transactions  (billing.py)                                  #
    # ------------------------------------------------------------------ #
    op.create_table(
        "payment_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("appointment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("appointments.id"), nullable=True),
        sa.Column("prescription_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("prescriptions.id"), nullable=True),
        sa.Column("amount_in_cents", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(10), nullable=False, server_default="INR"),
        sa.Column("gateway_provider", sa.String(30), nullable=False),
        sa.Column("gateway_transaction_id", sa.String(100), nullable=False, unique=True),
        sa.Column("gateway_order_id", sa.String(100), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="created"),
        sa.Column("idempotency_key", sa.String(128), nullable=False, unique=True),
        sa.Column("signature_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("payment_method", sa.String(50), nullable=False, server_default="card"),
        sa.Column("receipt_email", sa.String(255), nullable=True),
        sa.Column("payload_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_payments_org_status", "payment_transactions", ["organization_id", "status"])
    op.create_index("idx_payments_gateway_tx", "payment_transactions", ["gateway_provider", "gateway_transaction_id"])
    op.create_index(op.f("ix_payment_transactions_organization_id"), "payment_transactions", ["organization_id"])
    op.create_index(op.f("ix_payment_transactions_patient_id"), "payment_transactions", ["patient_id"])
    op.create_index(op.f("ix_payment_transactions_gateway_order_id"), "payment_transactions", ["gateway_order_id"])
    op.create_index(op.f("ix_payment_transactions_status"), "payment_transactions", ["status"])

    # ------------------------------------------------------------------ #
    # invoices  (billing.py)                                              #
    # ------------------------------------------------------------------ #
    op.create_table(
        "invoices",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("invoice_number", sa.String(64), nullable=False, unique=True),
        sa.Column("total_amount_in_cents", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(10), nullable=False, server_default="INR"),
        sa.Column("status", sa.String(30), nullable=False, server_default="issued"),
        sa.Column("line_items", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(op.f("ix_invoices_organization_id"), "invoices", ["organization_id"])
    op.create_index(op.f("ix_invoices_patient_id"), "invoices", ["patient_id"])
    op.create_index(op.f("ix_invoices_invoice_number"), "invoices", ["invoice_number"])


def downgrade() -> None:
    op.drop_table("invoices")
    op.drop_table("payment_transactions")
    op.drop_table("qsura_dispatch_logs")
    op.drop_table("wearable_samples")
    op.drop_table("mizaj_assessments")
    op.drop_table("appointments")
    op.drop_table("prescriptions")
    op.drop_table("clinical_notes")
    op.drop_table("encounters")
    op.drop_table("patients")
