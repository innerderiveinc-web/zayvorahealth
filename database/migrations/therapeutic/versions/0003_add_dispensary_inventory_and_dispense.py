"""Add inventory_batches and dispense_records tables

Revision ID: 0003_add_dispensary_inventory_and_dispense
Revises: 0002_add_unified_care_plans
Create Date: 2026-09-11 17:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0003_add_dispensary_inventory_and_dispense"
down_revision: Union[str, None] = "0002_add_unified_care_plans"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "inventory_batches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("medication_name", sa.String(length=255), nullable=False, index=True),
        sa.Column("formulation_type", sa.String(length=50), nullable=False, server_default="murakkab"),
        sa.Column("batch_number", sa.String(length=100), nullable=False, index=True),
        sa.Column("manufacturer", sa.String(length=255), nullable=False, server_default="ZAYVORA GMP Dispensary"),
        sa.Column("manufacturing_date", sa.String(length=50), nullable=False),
        sa.Column("expiry_date", sa.String(length=50), nullable=False, index=True),
        sa.Column("initial_quantity", sa.Float(), nullable=False),
        sa.Column("available_quantity", sa.Float(), nullable=False),
        sa.Column("unit", sa.String(length=30), nullable=False, server_default="g"),
        sa.Column("is_schedule_e1", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("mudabbar_certified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("mudabbar_certificate_number", sa.String(length=100), nullable=True),
        sa.Column("qc_release_status", sa.String(length=30), nullable=False, server_default="released"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "dispense_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("prescription_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("batch_number", sa.String(length=100), nullable=False),
        sa.Column("quantity_dispensed", sa.Float(), nullable=False),
        sa.Column("dispensed_by_pharmacist_id", sa.String(length=64), nullable=False),
        sa.Column("pharmacist_license_number", sa.String(length=100), nullable=False),
        sa.Column("patient_counseling_notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("mudabbar_verified_at_dispense", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("dispensed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("dispense_records")
    op.drop_table("inventory_batches")
