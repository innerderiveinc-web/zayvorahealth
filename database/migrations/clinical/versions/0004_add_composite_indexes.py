"""Add composite performance indexes to clinical tables

Revision ID: 0004_add_composite_indexes
Revises: 0003_enable_row_level_security
Create Date: 2026-09-12 15:40:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0004_add_composite_indexes"
down_revision: Union[str, None] = "0003_enable_row_level_security"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_index("idx_patients_org_mrn", "patients", ["organization_id", "mrn"])
    op.create_index("idx_encounters_org_patient_status", "encounters", ["organization_id", "patient_id", "status"])
    op.create_index("idx_prescriptions_org_patient_status", "prescriptions", ["organization_id", "patient_id", "status"])

def downgrade() -> None:
    op.drop_index("idx_prescriptions_org_patient_status", table_name="prescriptions")
    op.drop_index("idx_encounters_org_patient_status", table_name="encounters")
    op.drop_index("idx_patients_org_mrn", table_name="patients")
