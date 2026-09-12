"""Enable PostgreSQL Row-Level Security (RLS) for multi-tenant isolation

Revision ID: 0003_enable_row_level_security
Revises: 0002_add_mizaj_assessments
Create Date: 2026-09-12 15:35:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0003_enable_row_level_security"
down_revision: Union[str, None] = "0002_add_mizaj_assessments"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TENANT_TABLES = [
    "patients",
    "encounters",
    "clinical_notes",
    "prescriptions",
    "appointments",
    "mizaj_assessments",
]

def upgrade() -> None:
    for table in TENANT_TABLES:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY;")
        policy_sql = (
            f"CREATE POLICY {table}_tenant_isolation_policy ON {table} "
            f"FOR ALL "
            f"USING (organization_id = NULLIF(current_setting('app.current_org_id', true), '')::uuid) "
            f"WITH CHECK (organization_id = NULLIF(current_setting('app.current_org_id', true), '')::uuid);"
        )
        op.execute(policy_sql)

def downgrade() -> None:
    for table in TENANT_TABLES:
        op.execute(f"DROP POLICY IF EXISTS {table}_tenant_isolation_policy ON {table};")
        op.execute(f"ALTER TABLE {table} NO FORCE ROW LEVEL SECURITY;")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;")
