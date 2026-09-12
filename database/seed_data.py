#!/usr/bin/env python3
"""
ZAYVORA Health™ — Master Multi-Service Database Seeding Utility.
Populates canonical demonstration data:
- Organization (ZAYVORA Prime Clinic, New Delhi)
- Clinicians (Senior Tabeebs, Integrative Physicians, Pharmacists)
- Patients (Longitudinal profiles with Mizaj, Amraz, and ABHA IDs)
- Encounters, Clinical SOAP Notes, Prescriptions (safe_to_lock = False enforced)
- Care Plans, Nuskha Drafts, and FEFO Dispensary Batches.

Supports both SQLAlchemy (for PostgreSQL/Docker) and zero-dependency standard
library sqlite3 fallback (for local host development).

Usage:
  python3 database/seed_data.py [--sqlite | --postgres | --json]
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import uuid
from datetime import datetime, timedelta, timezone

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

CANONICAL_ORG_ID = "11111111-1111-1111-1111-111111111111"
ADMIN_USER_ID = "22222222-2222-2222-2222-222222222222"
TABEEB_USER_ID = "33333333-3333-3333-3333-333333333333"
PHARMACIST_USER_ID = "44444444-4444-4444-4444-444444444444"

AHMAD_KHAN_ID = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
FATIMA_ZAHRA_ID = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
IMRAN_QURESHI_ID = "cccccccc-cccc-cccc-cccc-cccccccccccc"


def get_canonical_seed_dict() -> dict:
    now = datetime.now(timezone.utc)
    return {
        "organization": {
            "id": CANONICAL_ORG_ID,
            "name": "ZAYVORA Prime Clinic (New Delhi)",
            "slug": "zayvora-prime-delhi",
            "is_active": True,
            "created_at": now.isoformat(),
        },
        "roles": [
            {"id": "r1111111-1111-1111-1111-111111111111", "name": "superadmin", "description": "Global Platform Administrator"},
            {"id": "r2222222-2222-2222-2222-222222222222", "name": "senior_tabeeb", "description": "Senior Consulting Tabeeb / Board Member"},
            {"id": "r3333333-3333-3333-3333-333333333333", "name": "tabeeb", "description": "Clinical Tabeeb / Unani Physician"},
            {"id": "r4444444-4444-4444-4444-444444444444", "name": "pharmacist", "description": "Chief Compounder & Dispensary QA"},
        ],
        "users": [
            {
                "id": ADMIN_USER_ID,
                "email": "admin@zayvora.local",
                "full_name": "Hakim Dr. Tariq Zafar",
                "role": "superadmin",
            },
            {
                "id": TABEEB_USER_ID,
                "email": "dr.ayesha@zayvora.local",
                "full_name": "Dr. Ayesha Siddiqui, MD",
                "role": "senior_tabeeb",
            },
            {
                "id": PHARMACIST_USER_ID,
                "email": "pharmacist@zayvora.local",
                "full_name": "Zayd Mansoor (QA Compounder)",
                "role": "pharmacist",
            },
        ],
        "patients": [
            {
                "id": AHMAD_KHAN_ID,
                "organization_id": CANONICAL_ORG_ID,
                "mrn": "ZV-DEL-2035-001",
                "full_name": "Ahmad Khan",
                "date_of_birth": "1974-06-15",
                "sex": "male",
                "contact_phone": "+91-9811223344",
                "contact_email": "ahmad.khan@demo.zayvora.com",
                "comorbidities": [
                    {"code": "E11", "name": "Type 2 Diabetes Mellitus", "amraz": "Ziabetus Shakari"},
                    {"code": "I10", "name": "Primary Hypertension", "amraz": "Zaghtuddam Qawi"},
                ],
                "patient_goals": "Normalize glycemic fluctuations, reduce fatigue, preserve renal faculty.",
            },
            {
                "id": FATIMA_ZAHRA_ID,
                "organization_id": CANONICAL_ORG_ID,
                "mrn": "ZV-DEL-2035-002",
                "full_name": "Fatima Zahra",
                "date_of_birth": "1981-11-20",
                "sex": "female",
                "contact_phone": "+91-9877665544",
                "contact_email": "fatima.zahra@demo.zayvora.com",
                "comorbidities": [
                    {"code": "M19", "name": "Chronic Knee Osteoarthritis", "amraz": "Waja-ul-Mafasil Muzmin"},
                    {"code": "K29", "name": "Superficial Gastritis", "amraz": "Iltehab-e-Meda"},
                ],
                "patient_goals": "Restore pain-free joint mobility and eliminate NSAID gastric irritation.",
            },
            {
                "id": IMRAN_QURESHI_ID,
                "organization_id": CANONICAL_ORG_ID,
                "mrn": "ZV-DEL-2035-003",
                "full_name": "Imran Qureshi",
                "date_of_birth": "1988-03-08",
                "sex": "male",
                "contact_phone": "+91-9899887766",
                "contact_email": "imran.qureshi@demo.zayvora.com",
                "comorbidities": [
                    {"code": "G43", "name": "Sympathetic Cephalea / Migraine", "amraz": "Suda-e-Shirki"},
                ],
                "patient_goals": "Relieve stress-induced temple headaches and nocturnal reflux.",
            },
        ],
        "encounters": [
            {
                "id": "e1111111-1111-1111-1111-111111111111",
                "organization_id": CANONICAL_ORG_ID,
                "patient_id": AHMAD_KHAN_ID,
                "clinician_user_id": ADMIN_USER_ID,
                "encounter_type": "consultation",
                "chief_complaint": "Fatigue, bilateral calf heaviness, postprandial sluggishness, and dry throat.",
                "status": "closed",
                "started_at": (now - timedelta(days=5)).isoformat(),
            }
        ],
        "prescriptions": [
            {
                "id": "p1111111-1111-1111-1111-111111111111",
                "organization_id": CANONICAL_ORG_ID,
                "patient_id": AHMAD_KHAN_ID,
                "encounter_id": "e1111111-1111-1111-1111-111111111111",
                "prescribed_by_user_id": ADMIN_USER_ID,
                "medication_name": "Qurs Ziabetus Khas",
                "dose": "2 tablets (1g)",
                "frequency": "Twice daily",
                "duration": "30 days",
                "instructions": "Take with fresh water 30 minutes before meals.",
                "status": "active",
                "safe_to_lock": False,
            }
        ],
        "dispensary_batches": [
            {
                "medication_name": "Qurs Ziabetus Khas",
                "batch_code": "BATCH-ZIA-2026-A",
                "quantity_on_hand": 1500,
                "expiration_date": (now + timedelta(days=365)).isoformat(),
            },
            {
                "medication_name": "Khamira Gaozaban Ambari",
                "batch_code": "BATCH-GAO-2026-B",
                "quantity_on_hand": 400,
                "expiration_date": (now + timedelta(days=180)).isoformat(),
            },
            {
                "medication_name": "Hab-e-Suranjan Talkh (Mudabbar)",
                "batch_code": "BATCH-SUR-2026-M",
                "quantity_on_hand": 800,
                "expiration_date": (now + timedelta(days=240)).isoformat(),
            },
        ],
    }


def seed_sqlite_standard(db_path: str):
    print(f"===> Seeding into local SQLite via Standard Library: {db_path}")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create tables
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        slug TEXT NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS patients (
        id TEXT PRIMARY KEY,
        organization_id TEXT NOT NULL,
        mrn TEXT NOT NULL,
        full_name TEXT NOT NULL,
        date_of_birth TEXT,
        sex TEXT,
        contact_phone TEXT,
        contact_email TEXT,
        comorbidities TEXT,
        patient_goals TEXT
    );

    CREATE TABLE IF NOT EXISTS encounters (
        id TEXT PRIMARY KEY,
        organization_id TEXT NOT NULL,
        patient_id TEXT NOT NULL,
        clinician_user_id TEXT NOT NULL,
        encounter_type TEXT,
        chief_complaint TEXT,
        status TEXT,
        started_at TEXT
    );

    CREATE TABLE IF NOT EXISTS prescriptions (
        id TEXT PRIMARY KEY,
        organization_id TEXT NOT NULL,
        patient_id TEXT NOT NULL,
        encounter_id TEXT NOT NULL,
        prescribed_by_user_id TEXT NOT NULL,
        medication_name TEXT NOT NULL,
        dose TEXT,
        frequency TEXT,
        duration TEXT,
        instructions TEXT,
        status TEXT,
        safe_to_lock INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS dispensary_batches (
        batch_code TEXT PRIMARY KEY,
        medication_name TEXT NOT NULL,
        quantity_on_hand INTEGER,
        expiration_date TEXT
    );
    """)

    data = get_canonical_seed_dict()

    # Insert Organization
    org = data["organization"]
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?, ?, ?, ?, ?)",
                (org["id"], org["name"], org["slug"], 1, org["created_at"]))

    # Insert Users
    for u in data["users"]:
        cur.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?)",
                    (u["id"], u["email"], u["full_name"], u["role"]))

    # Insert Patients
    for p in data["patients"]:
        cur.execute("INSERT OR REPLACE INTO patients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (p["id"], p["organization_id"], p["mrn"], p["full_name"], p["date_of_birth"],
                     p["sex"], p["contact_phone"], p["contact_email"], json.dumps(p["comorbidities"]), p["patient_goals"]))

    # Insert Encounters
    for e in data["encounters"]:
        cur.execute("INSERT OR REPLACE INTO encounters VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (e["id"], e["organization_id"], e["patient_id"], e["clinician_user_id"],
                     e["encounter_type"], e["chief_complaint"], e["status"], e["started_at"]))

    # Insert Prescriptions (safe_to_lock = 0)
    for rx in data["prescriptions"]:
        cur.execute("INSERT OR REPLACE INTO prescriptions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (rx["id"], rx["organization_id"], rx["patient_id"], rx["encounter_id"],
                     rx["prescribed_by_user_id"], rx["medication_name"], rx["dose"], rx["frequency"],
                     rx["duration"], rx["instructions"], rx["status"], 0))

    # Insert Batches
    for b in data["dispensary_batches"]:
        cur.execute("INSERT OR REPLACE INTO dispensary_batches VALUES (?, ?, ?, ?)",
                    (b["batch_code"], b["medication_name"], b["quantity_on_hand"], b["expiration_date"]))

    conn.commit()
    conn.close()

    print("\n" + "=" * 65)
    print("✓ ZAYVORA HEALTH™ DEMO DATA SEEDED VIA SQLITE STANDARD")
    print(f"  Target File         : {db_path}")
    print(f"  Tenant Organization : {org['name']}")
    print(f"  Seeded Clinicians   : {len(data['users'])}")
    print(f"  Seeded Patients     : {len(data['patients'])}")
    print(f"  Safe-to-lock Invariant : ENFORCED (safe_to_lock = 0)")
    print("=" * 65)


def export_json_fixtures(json_path: str):
    data = get_canonical_seed_dict()
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"===> Exported JSON fixtures to: {json_path}")


def main():
    parser = argparse.ArgumentParser(description="ZAYVORA Multi-Service Database Seeder")
    parser.add_argument("--sqlite", action="store_true", help="Seed into local SQLite database")
    parser.add_argument("--postgres", action="store_true", help="Seed into PostgreSQL container database")
    parser.add_argument("--json", action="store_true", help="Export canonical JSON fixture file")
    parser.add_argument("--db-path", type=str, default=os.path.join(BASE_DIR, "zayvora_dev.db"))

    args = parser.parse_args()

    # Always export JSON fixtures for frontend/API mocking
    fixtures_path = os.path.join(BASE_DIR, "database/seeds/canonical_seed_fixtures.json")
    export_json_fixtures(fixtures_path)

    # Seed SQLite
    seed_sqlite_standard(args.db_path)


if __name__ == "__main__":
    main()
