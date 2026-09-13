-- ZAYVORA Health OS — Persistent Relational Database Schema
-- Compatible with SQLite and PostgreSQL

CREATE TABLE IF NOT EXISTS facilities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    facility_type TEXT NOT NULL, -- HOSPITAL, CLINIC, RESEARCH_INSTITUTE, DISPENSARY
    address TEXT,
    city TEXT,
    state TEXT,
    contact_phone TEXT,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    role TEXT NOT NULL DEFAULT "PATIENT",
    mrn TEXT UNIQUE,
    facility_id TEXT DEFAULT "FAC-HQ-01",
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,
    facility_id TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    revoked INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS patients (
    id TEXT PRIMARY KEY,
    mrn TEXT UNIQUE NOT NULL,
    user_id TEXT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth TEXT,
    gender TEXT,
    contact_phone TEXT,
    contact_email TEXT,
    blood_group TEXT DEFAULT "Unknown",
    mizaj_dominant TEXT DEFAULT "Motadil (Balanced)",
    allergies_json TEXT DEFAULT "[]",
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS appointments (
    id TEXT PRIMARY KEY,
    token_number TEXT NOT NULL,
    mrn TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    doctor_reg TEXT,
    department TEXT DEFAULT "Integrative Unani OPD",
    opd_room TEXT DEFAULT "Room 3",
    appointment_date TEXT NOT NULL,
    appointment_time TEXT NOT NULL,
    acuity TEXT DEFAULT "STANDARD",
    chief_complaint TEXT,
    status TEXT DEFAULT "WAITING", -- WAITING, IN_CONSULTATION, COMPLETED, CANCELLED
    fee_amount REAL DEFAULT 800.0,
    payment_status TEXT DEFAULT "PAID", -- PENDING, PAID, REFUNDED
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS prescriptions (
    id TEXT PRIMARY KEY,
    order_number TEXT UNIQUE NOT NULL,
    mrn TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    doctor_reg TEXT NOT NULL,
    items_json TEXT NOT NULL,
    dietary_advice TEXT,
    regimenal_advice TEXT,
    signature_hash TEXT NOT NULL,
    status TEXT DEFAULT "PENDING_VERIFICATION", -- PENDING_VERIFICATION, VERIFIED_READY, DISPENSED
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS inventory (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    batch_number TEXT UNIQUE NOT NULL,
    expiry_date TEXT NOT NULL,
    stock_qty INTEGER NOT NULL DEFAULT 100,
    min_threshold INTEGER DEFAULT 20,
    category TEXT NOT NULL, -- CLINIC_UNANI, RETAIL_UNANI, AYUSH_PROPRIETARY, FSSAI_SUPPLEMENT
    unit_price REAL DEFAULT 150.0,
    is_schedule_e1 INTEGER DEFAULT 0,
    mudabbar_required INTEGER DEFAULT 0,
    mudabbar_cert TEXT,
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS audit_ledger (
    block_number INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    leaf_hash TEXT NOT NULL,
    event_type TEXT NOT NULL,
    signer TEXT NOT NULL,
    status TEXT DEFAULT "ANCHORED",
    facility_id TEXT DEFAULT "FAC-HQ-01",
    details_json TEXT
);

CREATE TABLE IF NOT EXISTS invoices (
    id TEXT PRIMARY KEY,
    invoice_number TEXT UNIQUE NOT NULL,
    mrn TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    amount REAL NOT NULL,
    department TEXT DEFAULT "Integrative Unani OPD",
    payment_method TEXT DEFAULT "UPI",
    status TEXT DEFAULT "PAID",
    prescription_id TEXT,
    items_json TEXT DEFAULT "[]",
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(facility_id) REFERENCES facilities(id),
    FOREIGN KEY(prescription_id) REFERENCES prescriptions(id)
);

CREATE TABLE IF NOT EXISTS encounters (
    id TEXT PRIMARY KEY,
    encounter_number TEXT UNIQUE NOT NULL,
    mrn TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    appointment_id TEXT,
    doctor_name TEXT NOT NULL,
    doctor_reg TEXT NOT NULL,
    facility_id TEXT DEFAULT "FAC-HQ-01",
    chief_complaint TEXT,
    examination_notes TEXT,
    vitals_json TEXT DEFAULT "{}",
    soap_json TEXT DEFAULT "{}",
    mizaj_json TEXT DEFAULT "{}",
    organ_axis_json TEXT DEFAULT "{}",
    afaal_cascade_json TEXT DEFAULT "{}",
    prescription_id TEXT,
    status TEXT DEFAULT "IN_PROGRESS", -- IN_PROGRESS, LOCKED_AND_SIGNED, CANCELLED
    signature_hash TEXT,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    signed_at DATETIME,
    FOREIGN KEY(facility_id) REFERENCES facilities(id),
    FOREIGN KEY(appointment_id) REFERENCES appointments(id),
    FOREIGN KEY(prescription_id) REFERENCES prescriptions(id)
);

CREATE TABLE IF NOT EXISTS ai_consultations (
    id TEXT PRIMARY KEY,
    consultation_id TEXT UNIQUE NOT NULL,
    mrn TEXT NOT NULL,
    patient_name TEXT,
    doctor_name TEXT,
    chief_complaint TEXT NOT NULL,
    organ_axis TEXT,
    mizaj TEXT,
    advisory_sections_json TEXT NOT NULL,
    citations_json TEXT NOT NULL,
    safety_verdict TEXT NOT NULL,
    provider_used TEXT NOT NULL,
    safe_to_lock INTEGER DEFAULT 0,
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE INDEX IF NOT EXISTS idx_patients_facility ON patients(facility_id);
CREATE INDEX IF NOT EXISTS idx_appointments_facility ON appointments(facility_id);
CREATE INDEX IF NOT EXISTS idx_prescriptions_facility ON prescriptions(facility_id);
CREATE INDEX IF NOT EXISTS idx_inventory_facility ON inventory(facility_id);
CREATE INDEX IF NOT EXISTS idx_inventory_name ON inventory(name);
CREATE INDEX IF NOT EXISTS idx_invoices_facility ON invoices(facility_id);
CREATE INDEX IF NOT EXISTS idx_invoices_prescription ON invoices(prescription_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token);
CREATE INDEX IF NOT EXISTS idx_encounters_mrn ON encounters(mrn);
CREATE INDEX IF NOT EXISTS idx_encounters_facility ON encounters(facility_id);
CREATE INDEX IF NOT EXISTS idx_encounters_apt ON encounters(appointment_id);
CREATE INDEX IF NOT EXISTS idx_ai_consultations_mrn ON ai_consultations(mrn);
CREATE INDEX IF NOT EXISTS idx_ai_consultations_facility ON ai_consultations(facility_id);



