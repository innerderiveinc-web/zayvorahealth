"""Initial therapeutic schema — creates all Therapeutic service tables.

Covers: nuskha_drafts, tadbeer_plans, ghiza_plans, unified_care_plans,
        inventory_batches, dispense_records (therapeutic.py)
        and courier_shipments (logistics.py).

Revision ID: 0001_initial_therapeutic
Revises:
Create Date: 2026-09-14 08:00:00.000000
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_therapeutic"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------ #
    # nuskha_drafts                                                        #
    # ------------------------------------------------------------------ #
    op.create_table(
        "nuskha_drafts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_by_user_id", sa.String(64), nullable=False),
        sa.Column("mizaj_context", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("asbab", sa.Text(), nullable=False, server_default=""),
        sa.Column("tashkhis", sa.Text(), nullable=False, server_default=""),
        sa.Column("organ_axis_context", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("usool_e_ilaj", sa.Text(), nullable=False, server_default=""),
        sa.Column("therapeutic_objective", sa.Text(), nullable=False, server_default=""),
        sa.Column("ingredients", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("dosage_form", sa.String(100), nullable=False, server_default=""),
        sa.Column("dose", sa.String(200), nullable=False, server_default=""),
        sa.Column("timing", sa.String(200), nullable=False, server_default=""),
        sa.Column("duration", sa.String(200), nullable=False, server_default=""),
        sa.Column("parhez", sa.Text(), nullable=False, server_default=""),
        sa.Column("safety_verdict", sa.String(30), nullable=False),
        sa.Column("safety_reasons", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("reviewed_by_user_id", sa.String(64), nullable=True),
        sa.Column("clinician_registration_number", sa.String(100), nullable=False, server_default=""),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rejection_reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("safety_override_justification", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "status IN ('draft', 'approved', 'rejected')",
            name="chk_nuskha_draft_status",
        ),
        sa.CheckConstraint(
            "(status != 'approved') OR (status = 'approved' AND reviewed_by_user_id IS NOT NULL)",
            name="chk_nuskha_approved_reviewer",
        ),
    )
    op.create_index(op.f("ix_nuskha_drafts_organization_id"), "nuskha_drafts", ["organization_id"])
    op.create_index(op.f("ix_nuskha_drafts_patient_id"), "nuskha_drafts", ["patient_id"])
    op.create_index(op.f("ix_nuskha_drafts_encounter_id"), "nuskha_drafts", ["encounter_id"])

    # ------------------------------------------------------------------ #
    # tadbeer_plans                                                        #
    # ------------------------------------------------------------------ #
    op.create_table(
        "tadbeer_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_by_user_id", sa.String(64), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("category", sa.String(40), nullable=False),
        sa.Column("indication", sa.Text(), nullable=False, server_default=""),
        sa.Column("method", sa.Text(), nullable=False, server_default=""),
        sa.Column("frequency", sa.String(100), nullable=False, server_default=""),
        sa.Column("duration", sa.String(100), nullable=False, server_default=""),
        sa.Column("contraindications", sa.Text(), nullable=False, server_default=""),
        sa.Column("practitioner_requirements", sa.Text(), nullable=False, server_default=""),
        sa.Column("safety_verdict", sa.String(30), nullable=False, server_default="SAFE_TO_CONSIDER"),
        sa.Column("safety_reasons", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_tadbeer_plans_organization_id"), "tadbeer_plans", ["organization_id"])
    op.create_index(op.f("ix_tadbeer_plans_patient_id"), "tadbeer_plans", ["patient_id"])
    op.create_index(op.f("ix_tadbeer_plans_encounter_id"), "tadbeer_plans", ["encounter_id"])

    # ------------------------------------------------------------------ #
    # ghiza_plans                                                          #
    # ------------------------------------------------------------------ #
    op.create_table(
        "ghiza_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_by_user_id", sa.String(64), nullable=False),
        sa.Column("dietary_goals", sa.Text(), nullable=False, server_default=""),
        sa.Column("meal_structure", sa.Text(), nullable=False, server_default=""),
        sa.Column("foods_recommended", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("foods_to_limit", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("hydration_guidance", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_ghiza_plans_organization_id"), "ghiza_plans", ["organization_id"])
    op.create_index(op.f("ix_ghiza_plans_patient_id"), "ghiza_plans", ["patient_id"])
    op.create_index(op.f("ix_ghiza_plans_encounter_id"), "ghiza_plans", ["encounter_id"])

    # ------------------------------------------------------------------ #
    # unified_care_plans                                                   #
    # ------------------------------------------------------------------ #
    op.create_table(
        "unified_care_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_by_user_id", sa.String(64), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("horizon", sa.String(30), nullable=False, server_default="stabilization"),
        sa.Column("duration_days", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("mizaj_context", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("usool_e_ilaj", sa.Text(), nullable=False, server_default=""),
        sa.Column("primary_indication", sa.String(255), nullable=False, server_default=""),
        sa.Column("ilaj_bid_dawa", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("ilaj_bit_tadbeer", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("ilaj_bil_ghiza", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("asbab_sittah", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("review_milestones", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("prognosis_notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("safe_to_lock", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("signed_by_clinician_id", sa.String(64), nullable=True),
        sa.Column("clinician_registration_number", sa.String(100), nullable=False, server_default=""),
        sa.Column("signed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_unified_care_plans_organization_id"), "unified_care_plans", ["organization_id"])
    op.create_index(op.f("ix_unified_care_plans_patient_id"), "unified_care_plans", ["patient_id"])
    op.create_index(op.f("ix_unified_care_plans_encounter_id"), "unified_care_plans", ["encounter_id"])

    # ------------------------------------------------------------------ #
    # inventory_batches                                                    #
    # ------------------------------------------------------------------ #
    op.create_table(
        "inventory_batches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("medication_name", sa.String(255), nullable=False),
        sa.Column("formulation_type", sa.String(50), nullable=False, server_default="murakkab"),
        sa.Column("batch_number", sa.String(100), nullable=False),
        sa.Column("manufacturer", sa.String(255), nullable=False, server_default="ZAYVORA GMP Dispensary"),
        sa.Column("manufacturing_date", sa.String(50), nullable=False),
        sa.Column("expiry_date", sa.String(50), nullable=False),
        sa.Column("initial_quantity", sa.Float(), nullable=False),
        sa.Column("available_quantity", sa.Float(), nullable=False),
        sa.Column("unit", sa.String(30), nullable=False, server_default="g"),
        sa.Column("is_schedule_e1", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("mudabbar_certified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("mudabbar_certificate_number", sa.String(100), nullable=True),
        sa.Column("qc_release_status", sa.String(30), nullable=False, server_default="released"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "(is_schedule_e1 = FALSE) OR (is_schedule_e1 = TRUE AND mudabbar_certified = TRUE AND mudabbar_certificate_number IS NOT NULL)",
            name="chk_schedule_e1_mudabbar",
        ),
    )
    op.create_index(op.f("ix_inventory_batches_organization_id"), "inventory_batches", ["organization_id"])
    op.create_index(op.f("ix_inventory_batches_medication_name"), "inventory_batches", ["medication_name"])
    op.create_index(op.f("ix_inventory_batches_batch_number"), "inventory_batches", ["batch_number"])
    op.create_index(op.f("ix_inventory_batches_expiry_date"), "inventory_batches", ["expiry_date"])

    # ------------------------------------------------------------------ #
    # dispense_records                                                     #
    # ------------------------------------------------------------------ #
    op.create_table(
        "dispense_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("prescription_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("batch_number", sa.String(100), nullable=False),
        sa.Column("quantity_dispensed", sa.Float(), nullable=False),
        sa.Column("dispensed_by_pharmacist_id", sa.String(64), nullable=False),
        sa.Column("pharmacist_license_number", sa.String(100), nullable=False),
        sa.Column("patient_counseling_notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("mudabbar_verified_at_dispense", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("dispensed_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_dispense_records_organization_id"), "dispense_records", ["organization_id"])
    op.create_index(op.f("ix_dispense_records_prescription_id"), "dispense_records", ["prescription_id"])
    op.create_index(op.f("ix_dispense_records_patient_id"), "dispense_records", ["patient_id"])
    op.create_index(op.f("ix_dispense_records_batch_id"), "dispense_records", ["batch_id"])

    # ------------------------------------------------------------------ #
    # courier_shipments  (logistics.py)                                   #
    # ------------------------------------------------------------------ #
    op.create_table(
        "courier_shipments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("prescription_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("carrier", sa.String(50), nullable=False),
        sa.Column("awb_tracking_number", sa.String(100), nullable=False, unique=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="MANIFESTED"),
        sa.Column("destination_pincode", sa.String(20), nullable=False),
        sa.Column("shipping_address", sa.Text(), nullable=False),
        sa.Column("temperature_controlled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("temperature_range_celsius", sa.String(50), nullable=False, server_default="15C - 25C (Ambient Controlled)"),
        sa.Column("manifest_generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("tracking_history", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("courier_payload_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_shipments_org_status", "courier_shipments", ["organization_id", "status"])
    op.create_index("idx_shipments_awb", "courier_shipments", ["carrier", "awb_tracking_number"])
    op.create_index(op.f("ix_courier_shipments_organization_id"), "courier_shipments", ["organization_id"])
    op.create_index(op.f("ix_courier_shipments_prescription_id"), "courier_shipments", ["prescription_id"])
    op.create_index(op.f("ix_courier_shipments_patient_id"), "courier_shipments", ["patient_id"])
    op.create_index(op.f("ix_courier_shipments_status"), "courier_shipments", ["status"])
    op.create_index(op.f("ix_courier_shipments_awb_tracking_number"), "courier_shipments", ["awb_tracking_number"])


def downgrade() -> None:
    op.drop_table("courier_shipments")
    op.drop_table("dispense_records")
    op.drop_table("inventory_batches")
    op.drop_table("unified_care_plans")
    op.drop_table("ghiza_plans")
    op.drop_table("tadbeer_plans")
    op.drop_table("nuskha_drafts")
