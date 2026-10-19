# ZAYVORA Health OS™ — DATABASE MODEL MATRIX
**Audit Date:** September 15, 2026

---

## 1. PostgreSQL — Primary Relational Database

**Connection:** `postgresql+asyncpg://zayvora:${POSTGRES_PASSWORD}@postgres:5432/zayvora`  
**Total Tables:** ~36 across 4 service schemas  
**ORM:** SQLAlchemy 2.x (async)  
**Migrations:** Alembic per service (`services/{service}/migrations/`)

### Identity Service Models (`services/identity/app/models/identity.py` — 142 lines)

| Table | Key Columns | Status |
|---|---|---|
| `organizations` | id (UUID), name, slug, settings JSONB, created_at | ✅ |
| `users` | id (UUID), email, password_hash, org_id FK, role_id FK, is_active, mfa_secret | ✅ |
| `roles` | id (UUID), name, org_id FK, description | ✅ |
| `permissions` | id (UUID), code, description, resource, action | ✅ |
| `role_permissions` | role_id FK, permission_id FK (M2M) | ✅ |
| `audit_logs` | id (UUID), user_id FK, action, resource, ip_addr, created_at | ✅ |
| `refresh_tokens` | jti (UUID), user_id FK, expires_at, revoked | ✅ |

### Clinical Service Models (`services/clinical/app/models/clinical.py` — 224 lines)

| Table | Key Columns | Status |
|---|---|---|
| `patients` | id (UUID), org_id FK, name_encrypted, dob_encrypted, mizaj_dominant, allergies[], comorbidities[], blood_group | ✅ |
| `encounters` | id (UUID), patient_id FK, doctor_id FK, status (Enum: draft/active/signed/locked), chief_complaint, encounter_date | ✅ |
| `clinical_notes` | id (UUID), encounter_id FK, version INT, soap_text_encrypted, hash SHA-256, is_locked | ✅ |
| `vitals` | id (UUID), encounter_id FK, bp, pulse_rate, spo2, temperature, weight, recorded_at | ✅ |
| `lab_results` | id (UUID), patient_id FK, test_name, value, unit, reference_range, is_flagged, collected_at | ✅ |
| `appointments` | id (UUID), patient_id FK, doctor_id FK, org_id FK, scheduled_at, duration_mins, status, modality | ✅ |
| `digital_twins` | id (UUID), patient_id FK, mizaj_vector JSONB, organ_reserve JSONB, risk_scores JSONB, last_updated | ✅ |
| `audit_merkle_blocks` | id (UUID), org_id FK, block_hash, parent_hash, events JSONB, created_at | ✅ |
| `wearable_readings` | id (UUID), patient_id FK, device_type, metrics JSONB, recorded_at | ✅ |
| `research_records` | id (UUID), patient_id FK, study_id FK, consent_date, data JSONB | ✅ |

### Billing Models (`services/clinical/app/models/billing.py` — 111 lines)

| Table | Key Columns | Status |
|---|---|---|
| `invoices` | id (UUID), patient_id FK, org_id FK, amount, currency, status, stripe_id | ✅ |
| `invoice_items` | id (UUID), invoice_id FK, description, quantity, unit_price | ✅ |
| `payments` | id (UUID), invoice_id FK, stripe_payment_intent_id, amount_paid, paid_at | ✅ |
| `subscriptions` | id (UUID), org_id FK, plan_name, stripe_subscription_id, status, current_period_end | ✅ |

### Therapeutic Service Models (`services/therapeutic/app/models/therapeutic.py` — 240 lines)

| Table | Key Columns | Status |
|---|---|---|
| `nuskhaat` (prescriptions) | id (UUID), patient_id FK, encounter_id FK, doctor_id FK, status, safe_to_lock, signature_hash | ✅ |
| `nuskha_items` | id (UUID), nuskha_id FK, herb_id, compound_name, dose, frequency, duration, route | ✅ |
| `care_plans` | id (UUID), patient_id FK, title, goals JSONB, interventions JSONB, review_date | ✅ |
| `care_plan_milestones` | id (UUID), care_plan_id FK, milestone, target_date, is_achieved | ✅ |
| `inventory` | id (UUID), org_id FK, herb_code, herb_name, batch_no, quantity_g, expiry_date, unit_cost | ✅ |
| `dispense_records` | id (UUID), nuskha_id FK, inventory_id FK, quantity_dispensed, dispensed_at, dispensed_by | ✅ |
| `tadbeer_plans` | id (UUID), patient_id FK, lifestyle_interventions JSONB, ghiza_plan JSONB | ✅ |

### Logistics Models (`services/therapeutic/app/models/logistics.py` — 80 lines)

| Table | Key Columns | Status |
|---|---|---|
| `delivery_orders` | id (UUID), nuskha_id FK, patient_id FK, address JSONB, courier_ref, status, expected_at | ✅ |
| `delivery_events` | id (UUID), order_id FK, event_type, timestamp, notes | ✅ |

### AI Service Models (`services/ai/app/models/ai.py` — 46 lines)

| Table | Key Columns | Status |
|---|---|---|
| `ai_sessions` | id (UUID), patient_id FK, doctor_id FK, session_type, started_at | ✅ |
| `ai_recommendations` | id (UUID), session_id FK, content, citations JSONB, confidence, reviewed_by, is_approved | ✅ |
| `ai_evaluations` | id (UUID), recommendation_id FK, safety_score, accuracy_score, evaluator, evaluated_at | ✅ |

---

## 2. Neo4j — Knowledge Graph Database

**Connection:** `bolt://neo4j:7687`  
**Auth:** `${NEO4J_USER}/${NEO4J_PASSWORD}`  
**Models:** `services/knowledge/app/models/source.py` (169 lines) + `ocr.py` (89 lines)  
**Migrations:** Cypher constraints applied at service startup (no Alembic)

### Graph Schema

**Node Labels:**
| Label | Key Properties | Description |
|---|---|---|
| `Herb` (Mufradat) | id, upi_code, arabic_name, latin_name, mizaj, organ_affinity[], schedule_e1 | Single herb monograph |
| `Compound` (Murakkab) | id, upi_code, arabic_name, latin_name, ingredients[], classical_source | Multi-ingredient formula |
| `Disease` | id, icd11_code, namaste_code, arabic_name, organ_system | Dual-paradigm disease classification |
| `Mizaj` | id, type (sanguine/bilious/phlegmatic/melancholic), humoral_balance | Constitutional type |
| `OrganAxis` | id, organ_name, classical_name, functions[], pathological_signs[] | Classical organ system |
| `Evidence` | id, study_ref, evidence_grade (A/B/C/D), pub_year, conclusion | Clinical evidence record |
| `Formula` | id, nfum_code, name, components[], indications[], contraindications[] | NFUM formulation |

**Relationship Types:**
| Relationship | From | To | Properties |
|---|---|---|---|
| `TREATS` | Herb/Compound | Disease | dose_range, evidence_grade, classical_ref |
| `CONTAINS` | Compound/Formula | Herb | quantity, proportion |
| `CONTRAINDICATED_FOR` | Herb/Compound | Disease/Condition | severity, mechanism |
| `CLASSIFIED_AS` | Herb | Mizaj | strength, quality |
| `AFFECTS` | Herb/Compound | OrganAxis | action_type |
| `SUPPORTED_BY` | TREATS rel | Evidence | — |
| `DERIVED_FROM` | Formula | Compound | classical_source |

---

## 3. Redis — Cache & Session Store

**Connection:** `redis://redis:6379`  
**Uses:**
- JWT JTI revocation list (TTL = token expiry)
- Rate limit counters per IP/user
- OpenFDA drug search cache (TTL = 1 hour)
- Session tokens (identity service)
- Clinical query result cache (configurable TTL)

---

## 4. Migration Status

| Service | Alembic Config | Current Status |
|---|---|---|
| identity | `services/identity/migrations/` | ✅ Working, has initial migration |
| clinical | `services/clinical/migrations/` | ✅ Config created this session |
| therapeutic | `services/therapeutic/migrations/` | ✅ Config created this session |
| ai | `services/ai/migrations/` | ✅ Config created this session |
| gateway | N/A (no DB) | — |
| knowledge | Neo4j startup constraints | ✅ Cypher-based |

---

## 5. Known Data Model Gaps

| Gap | Priority | Action Required |
|---|---|---|
| No GDPR consent tracking table | P1 | Add `consent_records` table to identity schema |
| No audit log for AI recommendations (immutable) | P1 | Extend `ai_recommendations` with Merkle chaining |
| `users` table lacks `failed_login_attempts`, `locked_until` | P1 | Add brute-force lockout fields |
| `patients` PHI encryption not applied to all fields | P1 | Audit AES-GCM coverage of `name`, `dob`, `phone` |
| No soft-delete pattern consistently applied | P2 | Add `deleted_at` to all critical tables |
| No `updated_by` audit trail on record mutations | P2 | Add `updated_by` FK to key tables |
