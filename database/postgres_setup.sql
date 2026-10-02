-- ============================================================
--  ZAYVORA Health OS™ — PostgreSQL Provisioning Script
--  Database: zayvora (Single database with per-service schema isolation)
--  Status: Pre-staging / Pilot Candidate
-- ============================================================

-- 1. Create application role if it does not exist
DO $$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'zayvora') THEN
    CREATE ROLE zayvora LOGIN PASSWORD 'zayvora';
  END IF;
END $$;

-- 2. Ensure main zayvora database exists
SELECT 'CREATE DATABASE zayvora OWNER zayvora ENCODING ''UTF8'''
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'zayvora')\gexec

-- 3. Connect to zayvora database and configure extensions and schemas
\c zayvora

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
-- vector extension for embeddings if pgvector is installed:
-- CREATE EXTENSION IF NOT EXISTS "vector";

-- 4. Create isolated schemas per service
CREATE SCHEMA IF NOT EXISTS identity AUTHORIZATION zayvora;
CREATE SCHEMA IF NOT EXISTS clinical AUTHORIZATION zayvora;
CREATE SCHEMA IF NOT EXISTS therapeutic AUTHORIZATION zayvora;
CREATE SCHEMA IF NOT EXISTS ai AUTHORIZATION zayvora;
CREATE SCHEMA IF NOT EXISTS manufacturing AUTHORIZATION zayvora;
CREATE SCHEMA IF NOT EXISTS pharmacy AUTHORIZATION zayvora;
CREATE SCHEMA IF NOT EXISTS audit AUTHORIZATION zayvora;

-- 5. Grant permissions
GRANT ALL PRIVILEGES ON DATABASE zayvora TO zayvora;
GRANT ALL PRIVILEGES ON ALL SCHEMAS IN DATABASE zayvora TO zayvora;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA identity TO zayvora;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA clinical TO zayvora;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA therapeutic TO zayvora;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA ai TO zayvora;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA manufacturing TO zayvora;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA pharmacy TO zayvora;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA audit TO zayvora;

ALTER DEFAULT PRIVILEGES IN SCHEMA identity GRANT ALL ON TABLES TO zayvora;
ALTER DEFAULT PRIVILEGES IN SCHEMA clinical GRANT ALL ON TABLES TO zayvora;
ALTER DEFAULT PRIVILEGES IN SCHEMA therapeutic GRANT ALL ON TABLES TO zayvora;
ALTER DEFAULT PRIVILEGES IN SCHEMA ai GRANT ALL ON TABLES TO zayvora;
ALTER DEFAULT PRIVILEGES IN SCHEMA manufacturing GRANT ALL ON TABLES TO zayvora;
ALTER DEFAULT PRIVILEGES IN SCHEMA pharmacy GRANT ALL ON TABLES TO zayvora;
ALTER DEFAULT PRIVILEGES IN SCHEMA audit GRANT ALL ON TABLES TO zayvora;

-- 6. Verification
SELECT schema_name FROM information_schema.schemata 
WHERE schema_name IN ('identity', 'clinical', 'therapeutic', 'ai', 'manufacturing', 'pharmacy', 'audit');
