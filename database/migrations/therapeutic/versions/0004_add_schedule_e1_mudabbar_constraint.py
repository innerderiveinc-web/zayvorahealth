"""Add Schedule E1 Mudabbar check constraint to inventory_batches

Revision ID: 0004_add_schedule_e1_mudabbar_constraint
Revises: 0003_add_dispensary_inventory_and_dispense
Create Date: 2026-09-12 15:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '0004_add_schedule_e1_mudabbar_constraint'
down_revision: Union[str, None] = '0003_add_dispensary_inventory_and_dispense'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enforces statutory Schedule E(1) Mudabbar detoxification rule at database DDL level
    op.create_check_constraint(
        constraint_name='chk_schedule_e1_mudabbar',
        table_name='inventory_batches',
        condition='(is_schedule_e1 = FALSE) OR (is_schedule_e1 = TRUE AND mudabbar_certified = TRUE AND mudabbar_certificate_number IS NOT NULL)',
    )


def downgrade() -> None:
    op.drop_constraint(
        constraint_name='chk_schedule_e1_mudabbar',
        table_name='inventory_batches',
        type_='check',
    )
