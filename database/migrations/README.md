# ZAYVORA Database Migrations Framework

This directory contains the database schema migration infrastructure for ZAYVORA HEALTH.

## Multi-Service Database Architecture

Per ZAYVORA Clinical Architecture Specification v4.0 §49, ZAYVORA employs domain-isolated relational databases on PostgreSQL 16:

1. **`zayvora_identity`**: Tenants (`organizations`), `users`, `roles`, `permissions`, `audit_logs`.
2. **`zayvora_clinical`**: `patients`, `encounters`, `clinical_notes` (versioned), `prescriptions`, `appointments`.
3. **`zayvora_therapeutic`**: `nuskha_drafts`, `tadbeer_plans`, `ghiza_plans`.
4. **`zayvora_ai`**: `ai_consultations` (AI Governance audit trail).

## Schema Evolution Rules

1. **Never Auto-Generate in Production**: `init_db()` is restricted to development/testing runtimes (`environment != 'production'`). Production schema changes must be applied via forward-only, idempotent migration scripts.
2. **Never Delete Historical Clinical Data**: Tables recording clinical interactions (`clinical_notes`, `prescriptions`, `nuskha_drafts`, `audit_logs`, `ai_consultations`) are append-only by architectural mandate. Never issue `DROP COLUMN` or destructive mutations on historical record versions.
3. **Tenant Isolation Foreign Keys**: Every clinically-scoped table must include a non-nullable `organization_id` foreign key indexed for partition queries.

## Running Migrations (Alembic)

```bash
# Set target database URL
export DATABASE_URL="postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_clinical"

# Generate a new migration
alembic revision --autogenerate -m "add_pregnancy_status_to_patients"

# Apply pending migrations
alembic upgrade head
```
