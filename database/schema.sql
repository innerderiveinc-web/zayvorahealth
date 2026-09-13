-- ZAYVORA Health OS — Persistent Relational Database Schema
-- Compatible with SQLite and PostgreSQL

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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inventory (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    batch_number TEXT UNIQUE NOT NULL,
    expiry_date TEXT NOT NULL,
    stock_qty INTEGER NOT NULL DEFAULT 100,
    min_threshold INTEGER DEFAULT 20,
    category TEXT NOT NULL, -- CLINIC_UNANI, RETAIL_UNANI, AYUSH_PROPRIETARY, FSSAI_SUPPLEMENT
    is_schedule_e1 INTEGER DEFAULT 0,
    mudabbar_required INTEGER DEFAULT 0,
    mudabbar_cert TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_ledger (
    block_number INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    leaf_hash TEXT NOT NULL,
    event_type TEXT NOT NULL,
    signer TEXT NOT NULL,
    status TEXT DEFAULT "ANCHORED",
    details_json TEXT
);
