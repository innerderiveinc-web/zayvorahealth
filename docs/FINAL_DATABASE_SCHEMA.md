# ZAYVORA Health OS™ — Database Schema

**Database: PostgreSQL (`zayvora`) + Neo4j (ZKB)**
**Status: Pre-staging · Schema defined · No live instance verified**

## Schema Isolation

Each microservice owns its schema:

| Service | Schema | Key Tables |
|:---|:---|:---|
| Identity | `identity` | users, organizations, roles, permissions, audit_log |
| Clinical | `clinical` | patients, encounters, prescriptions, symptoms, vitals |
| Knowledge | `knowledge` | herbs, formulations, contraindications, evidence |
| Therapeutic | `therapeutic` | nuskha, herb_drug_interactions, dosage_rules |
| AI | `ai` | inference_log, model_metadata, feedback |
| Manufacturing | `manufacturing` | batches, qc_results, coa_records, mudabbar_certs |
| Pharmacy | `pharmacy` | inventory, dispensing_records, stock_alerts |

## Core Tables

### identity.users
| Column | Type | Constraints |
|:---|:---|:---|
| id | UUID | PK |
| email | VARCHAR(255) | UNIQUE NOT NULL |
| hashed_password | VARCHAR | NOT NULL |
| role | VARCHAR | NOT NULL |
| org_id | UUID | FK → organizations |
| mfa_enabled | BOOLEAN | DEFAULT false |
| created_at | TIMESTAMPTZ | NOT NULL |

### clinical.patients
| Column | Type | Constraints |
|:---|:---|:---|
| id | UUID | PK |
| mrn | VARCHAR | UNIQUE (Medical Record Number) |
| name | VARCHAR | NOT NULL |
| dob | DATE | NOT NULL |
| gender | VARCHAR | NOT NULL |
| mizaj | VARCHAR | Damawi/Safrawi/Balghami/Sawdawi |
| org_id | UUID | FK → identity.organizations |
| created_at | TIMESTAMPTZ | NOT NULL |

### clinical.prescriptions
| Column | Type | Constraints |
|:---|:---|:---|
| id | UUID | PK |
| patient_id | UUID | FK → patients |
| doctor_id | UUID | FK → identity.users |
| herbs | JSONB | Array of herb + dose |
| instructions | TEXT | |
| safe_to_lock | BOOLEAN | DEFAULT false (AI invariant) |
| hmac_sha256 | VARCHAR | 21 CFR Part 11 signature |
| signed_at | TIMESTAMPTZ | NULL until clinician signs |
| status | VARCHAR | draft/signed/dispensed |

## Neo4j — ZAYVORA Knowledge Base (ZKB)

Nodes: `Herb`, `Disease`, `Symptom`, `Mizaj`, `Organ`, `Formulation`
Relationships: `TREATS`, `CONTRAINDICATED_WITH`, `BELONGS_TO_MIZAJ`, `COMPONENT_OF`

**Status: Schema designed · Live Neo4j instance not yet provisioned**
