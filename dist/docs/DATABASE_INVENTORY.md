# ZAYVORA Health OS — Database Inventory & Relational Architecture
**Document ID**: `ZAY-AUD-004`  
**Classification**: Database Architecture & Storage Standard  
**Date**: September 2026  
**Status**: ACTIVE & PERSISTENT  

---

## 1. Storage Strategy: Dual-Tier Persistence Architecture

To guarantee zero operational downtime, seamless local setup, and massive enterprise scalability, ZAYVORA Health OS implements a dual-tier database strategy:

1. **Tier 1 (Active Local Production & Staging)**:
   - **Engine**: SQLite 3 relational database (`database/zayvora_live.db`).
   - **Schema**: DDL defined in `database/schema.sql`.
   - **Persistence**: Writes directly to disk with WAL (Write-Ahead Logging) compatibility and ACID transaction guarantees.
   - **Seed Engine**: `database/init_live_db.py` pre-populates verified clinician accounts, patient records, queue tokens, and FEFO inventory.

2. **Tier 2 (Enterprise Cloud Cluster Microservices)**:
   - **Engine**: PostgreSQL 15+ relational database.
   - **ORM**: SQLAlchemy declarative models partitioned across 6 microservice domains.
   - **Migrations**: Alembic versioned migrations located in `database/migrations/*`.

---

## 2. Active Relational Schema (`database/schema.sql`)

### 2.1 Table: `users`
Stores authenticated users across all 9 roles with salted SHA-256 password hashes.

| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | `TEXT` | `PRIMARY KEY` | Unique user identifier (`USR-ADMIN-01`, `USR-DOC-01`, etc.) |
| `email` | `TEXT` | `UNIQUE NOT NULL` | Verified login email address |
| `password_hash` | `TEXT` | `NOT NULL` | Hex-encoded SHA-256 hash of password + salt |
| `salt` | `TEXT` | `NOT NULL` | Cryptographically random per-user salt (16-character hex) |
| `full_name` | `TEXT` | `NOT NULL` | Official legal/clinical name |
| `phone` | `TEXT` | None | Contact telephone number |
| `role` | `TEXT` | `NOT NULL DEFAULT "PATIENT"` | User role (`SUPER_ADMIN`, `DOCTOR`, `PATIENT`, etc.) |
| `mrn` | `TEXT` | `UNIQUE` | Medical Record Number for patients (`MRN-2026-xxxx`) |
| `facility_id` | `TEXT` | `DEFAULT "FAC-HQ-01"` | Associated clinic or hospital facility identifier |
| `is_active` | `INTEGER`| `DEFAULT 1` | Account status flag (1=active, 0=suspended) |
| `created_at` | `DATETIME`| `DEFAULT CURRENT_TIMESTAMP` | Timestamp of account creation |

### 2.2 Table: `patients`
Core patient demographic and clinical baseline profile.

| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | `TEXT` | `PRIMARY KEY` | Internal patient identifier (`PAT-0814`) |
| `mrn` | `TEXT` | `UNIQUE NOT NULL` | Official Medical Record Number (`MRN-2026-0814`) |
| `user_id` | `TEXT` | `FOREIGN KEY (users.id)` | Linked authenticated user account (nullable for walk-ins) |
| `first_name` | `TEXT` | `NOT NULL` | Patient given name |
| `last_name` | `TEXT` | `NOT NULL` | Patient family name |
| `date_of_birth` | `TEXT` | None | ISO-8601 date of birth (`YYYY-MM-DD`) |
| `gender` | `TEXT` | None | Biological sex / gender |
| `contact_phone` | `TEXT` | None | Primary mobile contact phone |
| `contact_email` | `TEXT` | None | Primary notification email |
| `blood_group` | `TEXT` | `DEFAULT "Unknown"` | ABO and Rh blood group (`B+`, `O+`, etc.) |
| `mizaj_dominant` | `TEXT` | `DEFAULT "Motadil"` | Baseline temperament (`Balghami`, `Safrawi`, `Damawi`, `Sawdawi`) |
| `allergies_json` | `TEXT` | `DEFAULT "[]"` | JSON array of known allergies and contraindications |
| `created_at` | `DATETIME`| `DEFAULT CURRENT_TIMESTAMP` | Registration timestamp |

### 2.3 Table: `appointments`
Outpatient department (OPD) appointments, walk-in tokens, and consultation tracking.

| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | `TEXT` | `PRIMARY KEY` | Appointment ID (`APT-104`) |
| `token_number` | `TEXT` | `NOT NULL` | Daily sequential queue token (`T-104`, `T-105`) |
| `mrn` | `TEXT` | `NOT NULL` | Linked patient Medical Record Number |
| `patient_name` | `TEXT` | `NOT NULL` | Full patient name |
| `doctor_name` | `TEXT` | `NOT NULL` | Assigned clinician |
| `doctor_reg` | `TEXT` | None | Council registration number of attending clinician |
| `department` | `TEXT` | `DEFAULT "Integrative Unani OPD"` | Clinical specialty department |
| `opd_room` | `TEXT` | `DEFAULT "Room 3"` | Physical consultation room |
| `appointment_date`| `TEXT` | `NOT NULL` | Consultation date (`YYYY-MM-DD`) |
| `appointment_time`| `TEXT` | `NOT NULL` | Scheduled time slot (`10:15 AM`) |
| `acuity` | `TEXT` | `DEFAULT "STANDARD"` | Triage priority (`STANDARD`, `URGENT`, `FOLLOWUP`) |
| `chief_complaint` | `TEXT` | None | Patient primary presenting symptom |
| `status` | `TEXT` | `DEFAULT "WAITING"` | `WAITING`, `IN_CONSULTATION`, `COMPLETED`, `CANCELLED` |
| `fee_amount` | `REAL` | `DEFAULT 800.0` | Consultation fee in currency units (INR) |
| `payment_status` | `TEXT` | `DEFAULT "PAID"` | Billing status (`PENDING`, `PAID`, `REFUNDED`) |
| `created_at` | `DATETIME`| `DEFAULT CURRENT_TIMESTAMP` | Creation timestamp |

### 2.4 Table: `prescriptions`
Clinically authored, 21 CFR Part 11 signed, and tamper-evident medical prescriptions.

| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | `TEXT` | `PRIMARY KEY` | Unique prescription ID (`RX-B201`) |
| `order_number` | `TEXT` | `UNIQUE NOT NULL` | Pharmacy order number (`RX-2026-LOT4`) |
| `mrn` | `TEXT` | `NOT NULL` | Patient MRN |
| `patient_name` | `TEXT` | `NOT NULL` | Patient name |
| `doctor_name` | `TEXT` | `NOT NULL` | Prescribing doctor name |
| `doctor_reg` | `TEXT` | `NOT NULL` | Doctor council registration number |
| `items_json` | `TEXT` | `NOT NULL` | JSON array of prescribed medicines, dosages, and posology |
| `dietary_advice` | `TEXT` | None | Specific Unani Parhez / dietary restrictions |
| `regimenal_advice`| `TEXT` | None | Recommended Tadbeer (Hijama, Fasd, Nutool, etc.) |
| `signature_hash` | `TEXT` | `NOT NULL` | Cryptographic SHA-256 hash sealing author, date, and items |
| `status` | `TEXT` | `DEFAULT "PENDING_VERIFICATION"` | `PENDING_VERIFICATION`, `VERIFIED_READY`, `DISPENSED` |
| `created_at` | `DATETIME`| `DEFAULT CURRENT_TIMESTAMP` | Authoring timestamp |

### 2.5 Table: `inventory`
Dispensary stock management with First-Expired First-Out (FEFO) picking and Schedule E(1) controls.

| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | `TEXT` | `PRIMARY KEY` | Stock item ID (`INV-001`) |
| `name` | `TEXT` | `NOT NULL` | Medicine or formulation name |
| `batch_number` | `TEXT` | `UNIQUE NOT NULL` | Manufacturing batch identifier (`MS-2026-LOT4`) |
| `expiry_date` | `TEXT` | `NOT NULL` | Expiration date (`YYYY-MM-DD`) for FEFO sorting |
| `stock_qty` | `INTEGER`| `NOT NULL DEFAULT 100` | Current available physical quantity in units |
| `min_threshold` | `INTEGER`| `DEFAULT 20` | Reorder threshold triggering automated low-stock alert |
| `category` | `TEXT` | `NOT NULL` | `CLINIC_UNANI`, `RETAIL_UNANI`, `AYUSH_PROPRIETARY`, `FSSAI` |
| `is_schedule_e1`| `INTEGER`| `DEFAULT 0` | 1 if item contains regulated poisonous plant, else 0 |
| `mudabbar_required`| `INTEGER`| `DEFAULT 0` | 1 if Mudabbar purification certificate is mandatory |
| `mudabbar_cert` | `TEXT` | None | Certificate hash verifying completed Mudabbar protocol |
| `created_at` | `DATETIME`| `DEFAULT CURRENT_TIMESTAMP` | Batch registration timestamp |

### 2.6 Table: `audit_ledger`
Immutable, tamper-evident cryptographic block ledger compliant with 21 CFR Part 11 and HIPAA.

| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `block_number` | `INTEGER`| `PRIMARY KEY AUTOINCREMENT` | Monotonically increasing block index |
| `timestamp` | `DATETIME`| `DEFAULT CURRENT_TIMESTAMP` | Immutable block timestamp |
| `leaf_hash` | `TEXT` | `NOT NULL` | SHA-256 hash of the sealed event payload |
| `event_type` | `TEXT` | `NOT NULL` | `PRESCRIPTION_LOCKED_21CFR11`, `DISPENSE_EXECUTED`, etc. |
| `signer` | `TEXT` | `NOT NULL` | Entity or clinician who authorized the action |
| `status` | `TEXT` | `DEFAULT "ANCHORED"` | Cryptographic state (`ANCHORED`, `VERIFIED`) |
| `details_json` | `TEXT` | None | Associated contextual metadata |

---

## 3. Microservice SQLAlchemy ORM Models (25 Tables)

- **Identity Service**: `organizations`, `roles`, `permissions`, `users`, `audit_logs`
- **Clinical Service**: `patients`, `encounters`, `clinical_notes`, `prescriptions`, `appointments`, `mizaj_assessments`, `wearable_samples`, `qsura_dispatch_logs`
- **Therapeutic Service**: `nuskha_drafts`, `tadbeer_plans`, `ghiza_plans`, `unified_care_plans`, `inventory_batches`, `dispense_records`
- **Billing Service**: `payment_transactions`, `invoices`
- **Logistics Service**: `courier_shipments`
- **AI Service**: `ai_consultations`

---

## 4. Disaster Recovery & Backup Integrity (`database/dr_backup_restore.py`)

- **Backup Automation**: Generates timestamped, compressed SQLite snapshots into `backups/`.
- **Integrity Validation**: Computes SHA-256 hash of database before and after snapshot restoration.
- **Recovery Point Objective (RPO)**: < 15 minutes.
- **Recovery Time Objective (RTO)**: < 30 seconds.
- **Automated Verification**: Verified in `tests/run_all_tests.py` (Phase 7 Production Readiness Gate).

