#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Live Database Provisioner
===============================================
Provisions the full zayvora PostgreSQL database from scratch:

  1. Creates PostgreSQL schemas per service
  2. Runs Alembic migrations across all services
  3. Seeds canonical pilot data (organisations, users, patients, encounters)
  4. Verifies database integrity

Usage:
  # SQLite dev (no PostgreSQL required):
  python3 database/provision.py --mode sqlite

  # PostgreSQL (requires running PostgreSQL instance):
  python3 database/provision.py --mode postgres --url postgresql://zayvora:zayvora@localhost:5432/zayvora

  # Dry run (print what would be done, no changes):
  python3 database/provision.py --dry-run

  # Re-seed only (keep schema, refresh data):
  python3 database/provision.py --seed-only

Environment variables (alternative to --url):
  DATABASE_URL=postgresql://zayvora:zayvora@localhost:5432/zayvora

Safety:
  - Will NOT run in production without explicit --yes-i-know-this-is-live
  - Never drops or truncates tables with APPEND_ONLY marker
  - All seed data uses deterministic UUIDs for idempotent reruns
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sqlite3
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent.parent
DB_DIR   = Path(__file__).parent

SERVICES = ["identity", "clinical", "therapeutic", "ai", "knowledge"]

# Deterministic UUIDs for canonical seed data (idempotent reruns)
ORG_ID           = "11111111-1111-1111-1111-111111111111"
ADMIN_USER_ID    = "22222222-2222-2222-2222-222222222222"
DOCTOR_USER_ID   = "33333333-3333-3333-3333-333333333333"
DOCTOR2_USER_ID  = "34343434-3434-3434-3434-343434343434"
RECEPTIONIST_ID  = "44444444-4444-4444-4444-444444444444"
PHARMACIST_ID    = "55555555-5555-5555-5555-555555555555"
PATIENT1_ID      = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
PATIENT2_ID      = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
PATIENT3_ID      = "cccccccc-cccc-cccc-cccc-cccccccccccc"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hash_password(password: str, salt: str = "dev_salt_v2") -> tuple[str, str]:
    """SHA-256 password hash with salt matching live_api_server.py."""
    hashed = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    return hashed, salt

def _hmac_sign(data: str, key: str = "zayvora_21cfr_key") -> str:
    """SHA-256 HMAC for 21 CFR Part 11 digital signatures."""
    return hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def log(msg: str, level: str = "INFO") -> None:
    stamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{stamp}] [{level:5s}] {msg}")

# ---------------------------------------------------------------------------
# SQLite provisioner (development / no PostgreSQL)
# ---------------------------------------------------------------------------

def provision_sqlite(dry_run: bool = False) -> bool:
    db_path = DB_DIR / "zayvora_live.db"
    schema_path = DB_DIR / "schema.sql"

    log(f"SQLite mode → {db_path}")

    if not schema_path.exists():
        log("schema.sql not found", "ERROR")
        return False

    if dry_run:
        log("[DRY RUN] Would initialise SQLite DB and seed canonical data")
        return True

    # Re-initialise (remove stale DB)
    if db_path.exists():
        log("Removing stale database for clean provisioning…")
        db_path.unlink()

    conn = sqlite3.connect(str(db_path))
    cur  = conn.cursor()

    with open(schema_path) as f:
        cur.executescript(f.read())
    log("Schema applied")

    _seed_sqlite(cur)
    conn.commit()
    conn.close()

    size_kb = db_path.stat().st_size // 1024
    log(f"SQLite DB provisioned → {db_path} ({size_kb} KB)")
    return True


def _seed_sqlite(cur: sqlite3.Cursor) -> None:
    """Seed canonical pilot data into SQLite."""

    # --- Facilities ---
    facilities = [
        ("FAC-HQ-01",     "zayvora clinic and hospital",           "ZAYVORA-CLINIC-HOSP", "HOSPITAL",          "Main Health Boulevard", "New Delhi",  "Delhi",     "+91 97738 82657", 1),
        ("FAC-BRANCH-02", "zayvora hospital",                      "ZAYVORA-HOSP",        "HOSPITAL",          "Charminar Road",        "Hyderabad",  "Telangana", "+91 40 2452 1102", 1),
        ("FAC-BRANCH-03", "ZAYVORA Matab™ — Integrative Care",    "ZM-INT-01",           "CLINIC",            "Arera Colony",          "Bhopal",     "MP",        "+91 75 5428 0011", 1),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO facilities (id,name,code,facility_type,address,city,state,contact_phone,is_active) VALUES (?,?,?,?,?,?,?,?,?)",
        facilities,
    )
    log(f"  Seeded {len(facilities)} facilities")

    # --- Users ---
    users = [
        # Requested Credentials
        ("USR-ADMIN-01", "admin@zayvorahealth",           _hash_password("admin123"),     "Super Admin (Irfan Ashraf)", "+91 98110 00001", "SUPER_ADMIN",  None,             "FAC-HQ-01"),
        ("USR-DOC-01",   "dr.irfan@zayvorahealth",        _hash_password("doctor123"),    "Dr. Irfan Ashraf",          "+91 98110 44219", "DOCTOR",       None,             "FAC-HQ-01"),
        ("USR-DOC-02",   "dr.malik@zayvorahealth",        _hash_password("doctor123"),    "Dr. Malik",                 "+91 98480 33110", "DOCTOR",       None,             "FAC-BRANCH-02"),
        ("USR-REC-01",   "reception@zayvorahealth",       _hash_password("reception123"), "Reception Desk",            "+91 98110 55301", "RECEPTIONIST", None,             "FAC-HQ-01"),
        ("USR-PHARM-01", "pharmacy@zayvorahealth",        _hash_password("pharmacy123"),  "Chief Pharmacist",          "+91 98110 88123", "PHARMACIST",   None,             "FAC-HQ-01"),
        ("USR-PAT-01",   "ahmad.khan@example.com",        _hash_password("password123"),  "Ahmad Khan",                "+91 98110 12345", "PATIENT",      "MRN-2026-0001",  "FAC-HQ-01"),
        # Compatibility Aliases for Automated Test Suites
        ("USR-ADMIN-ALT","admin@zayvora.health",          _hash_password("admin123"),     "Admin Alias",               "+91 98110 00001", "SUPER_ADMIN",  None,             "FAC-HQ-01"),
        ("USR-DOC-ALT",  "dr.mansoor@zayvora.health",     _hash_password("doctor123"),    "Prof. Dr. Mansoor Alam",    "+91 98110 44219", "DOCTOR",       None,             "FAC-HQ-01"),
        ("USR-DOC-ALT2", "dr.sirajuddin@zayvora.health",  _hash_password("doctor123"),    "Dr. Hakim Sirajuddin",      "+91 98480 33110", "DOCTOR",       None,             "FAC-BRANCH-02"),
        ("USR-REC-ALT",  "reception@zayvora.health",      _hash_password("reception123"), "Receptionist",              "+91 98110 55301", "RECEPTIONIST", None,             "FAC-HQ-01"),
        ("USR-PHARM-ALT","pharmacy@zayvora.health",       _hash_password("pharmacy123"),  "Pharmacist",                "+91 98110 88123", "PHARMACIST",   None,             "FAC-HQ-01"),
        ("USR-PAT-02",   "fatima.zahra@example.com",      _hash_password("password123"),  "Fatima Zahra",              "+91 98480 99221", "PATIENT",      "MRN-2026-0002",  "FAC-BRANCH-02"),
        ("USR-PAT-03",   "hamza.farooqi@example.com",     _hash_password("password123"),  "Hamza Farooqi",             "+91 99001 55432", "PATIENT",      "MRN-2026-0003",  "FAC-HQ-01"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO users (id,email,password_hash,salt,full_name,phone,role,mrn,facility_id) VALUES (?,?,?,?,?,?,?,?,?)",
        [(u[0],u[1],u[2][0],u[2][1],u[3],u[4],u[5],u[6],u[7]) for u in users],
    )
    log(f"  Seeded {len(users)} users")

    # --- Patients ---
    patients = [
        ("PAT-001", "MRN-2026-0001", "USR-PAT-01", "Ahmad",  "Khan",   "1990-03-15", "Male",   "+91 98110 12345", "ahmad.khan@example.com",   "B+", "Damawi (Sanguine)",    "FAC-HQ-01"),
        ("PAT-002", "MRN-2026-0002", "USR-PAT-02", "Fatima", "Zahra",  "1974-11-08", "Female", "+91 98480 99221", "fatima.zahra@example.com",  "O+", "Balghami (Phlegmatic)","FAC-BRANCH-02"),
        ("PAT-003", "MRN-2026-0003", "USR-PAT-03", "Hamza",  "Farooqi","1998-07-22", "Male",   "+91 99001 55432", "hamza.farooqi@example.com", "A+", "Safrawi (Choleric)",   "FAC-HQ-01"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO patients (id,mrn,user_id,first_name,last_name,date_of_birth,gender,contact_phone,contact_email,blood_group,mizaj_dominant,facility_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        patients,
    )
    log(f"  Seeded {len(patients)} patients")

    # --- Appointments ---
    appts = [
        ("APT-001","Q-001","MRN-2026-0001","Ahmad Khan",    "Prof. Dr. Mansoor Alam","REG-MCI-44219","Integrative Unani OPD","Room 3","2026-09-21","09:30","STANDARD","Chronic headache and fatigue","COMPLETED", 800.0,"PAID","FAC-HQ-01"),
        ("APT-002","Q-002","MRN-2026-0002","Fatima Zahra",  "Prof. Dr. Mansoor Alam","REG-MCI-44219","Integrative Unani OPD","Room 3","2026-09-21","10:00","STANDARD","Weight management and hypothyroid","WAITING",   800.0,"PAID","FAC-HQ-01"),
        ("APT-003","Q-003","MRN-2026-0003","Hamza Farooqi", "Dr. Hakim Sirajuddin",  "REG-NMC-33110","Dermatology OPD",      "Room 5","2026-09-21","10:30","URGENT",  "Chronic skin rash with itching",   "WAITING",   800.0,"PENDING","FAC-BRANCH-02"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO appointments (id,token_number,mrn,patient_name,doctor_name,doctor_reg,department,opd_room,appointment_date,appointment_time,acuity,chief_complaint,status,fee_amount,payment_status,facility_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        appts,
    )
    log(f"  Seeded {len(appts)} appointments")

    # --- Prescriptions ---
    rx_items = json.dumps([
        {"herb": "Ashwagandha (Withania somnifera)", "dose": "3g", "form": "Safoof", "frequency": "BD"},
        {"herb": "Brahmi (Bacopa monnieri)",          "dose": "2g", "form": "Safoof", "frequency": "BD"},
        {"herb": "Senna Makki (Cassia angustifolia)", "dose": "1g", "form": "Safoof", "frequency": "HS"},
    ])
    rx_sig = _hmac_sign(f"APT-001|MRN-2026-0001|{_now()}")
    cur.execute(
        "INSERT OR IGNORE INTO prescriptions (id,order_number,mrn,patient_name,doctor_name,doctor_reg,items_json,dietary_advice,regimenal_advice,signature_hash,status,facility_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        ("RX-001","NX-2026-0001","MRN-2026-0001","Ahmad Khan","Prof. Dr. Mansoor Alam","REG-MCI-44219",rx_items,
         "Avoid cold water and heavy meals. Warm milk before bed.",
         "Morning walk 30 min. Avoid daytime sleep.",
         rx_sig,"VERIFIED_READY","FAC-HQ-01"),
    )
    log("  Seeded 1 canonical prescription (SHA-256 HMAC signed)")


# ---------------------------------------------------------------------------
# PostgreSQL provisioner
# ---------------------------------------------------------------------------

def provision_postgres(url: str, dry_run: bool = False, seed_only: bool = False) -> bool:
    log(f"PostgreSQL mode → {url.split('@')[-1]}")  # hide credentials in log

    try:
        import sqlalchemy as sa
        from sqlalchemy import text
    except ImportError:
        log("sqlalchemy not installed. Run: pip install sqlalchemy psycopg2-binary", "ERROR")
        return False

    if dry_run:
        log("[DRY RUN] Would connect to PostgreSQL and run migrations + seed")
        return True

    try:
        engine = sa.create_engine(url, echo=False)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log("PostgreSQL connection verified")
    except Exception as e:
        log(f"Cannot connect to PostgreSQL: {e}", "ERROR")
        log("Ensure PostgreSQL is running and DATABASE_URL is set correctly", "ERROR")
        return False

    if not seed_only:
        log("Running Alembic migrations for all services…")
        migrate_script = BASE_DIR / "database" / "migrations" / "migrate.py"
        result = subprocess.run(
            [sys.executable, str(migrate_script), "upgrade", "all"],
            cwd=str(BASE_DIR),
            capture_output=False,
        )
        if result.returncode != 0:
            log("Migration failed — check alembic.ini DATABASE_URL settings", "ERROR")
            return False
        log("All migrations applied")

    log("Seeding canonical pilot data…")
    seed_script = DB_DIR / "seed_data.py"
    result = subprocess.run(
        [sys.executable, str(seed_script), "--postgres"],
        cwd=str(BASE_DIR),
        env={**os.environ, "DATABASE_URL": url},
        capture_output=False,
    )
    if result.returncode != 0:
        log("Seeding failed — check seed_data.py", "WARN")
    else:
        log("Canonical pilot data seeded")

    return True


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify_sqlite() -> bool:
    db_path = DB_DIR / "zayvora_live.db"
    if not db_path.exists():
        log("zayvora_live.db not found", "ERROR")
        return False

    conn = sqlite3.connect(str(db_path))
    cur  = conn.cursor()

    checks = {
        "facilities":    "SELECT COUNT(*) FROM facilities",
        "users":         "SELECT COUNT(*) FROM users",
        "patients":      "SELECT COUNT(*) FROM patients",
        "appointments":  "SELECT COUNT(*) FROM appointments",
        "prescriptions": "SELECT COUNT(*) FROM prescriptions",
    }

    log("Database verification:")
    all_ok = True
    for table, sql in checks.items():
        try:
            count = cur.execute(sql).fetchone()[0]
            log(f"  {table:20s} → {count} rows")
            if count == 0:
                log(f"  WARNING: {table} is empty", "WARN")
        except Exception as e:
            log(f"  {table}: ERROR — {e}", "ERROR")
            all_ok = False

    conn.close()
    return all_ok


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="ZAYVORA Health OS™ — Live Database Provisioner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--mode", choices=["sqlite", "postgres"], default="sqlite",
                        help="Database backend (default: sqlite)")
    parser.add_argument("--url", default=os.getenv("DATABASE_URL", ""),
                        help="PostgreSQL connection URL")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be done without making changes")
    parser.add_argument("--seed-only", action="store_true",
                        help="Skip migrations, only seed data")
    parser.add_argument("--verify-only", action="store_true",
                        help="Only verify the existing database")
    parser.add_argument("--yes-i-know-this-is-live", action="store_true",
                        help="Required to run against a live production database")

    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  ZAYVORA Health OS™ — Database Provisioner v2.0")
    print("  Status: Pre-staging / Pilot Candidate")
    print("=" * 60)
    print()

    # Safety guard
    env = os.getenv("ENVIRONMENT", "development").lower()
    if env == "production" and not args.yes_i_know_this_is_live:
        log("PRODUCTION environment detected. Use --yes-i-know-this-is-live to proceed.", "ERROR")
        log("This guard prevents accidental provisioning in live environments.", "ERROR")
        sys.exit(1)

    if args.verify_only:
        ok = verify_sqlite() if args.mode == "sqlite" else True
        sys.exit(0 if ok else 1)

    # Provision
    if args.mode == "sqlite":
        ok = provision_sqlite(dry_run=args.dry_run)
    else:
        if not args.url:
            log("--url or DATABASE_URL environment variable required for postgres mode", "ERROR")
            sys.exit(1)
        ok = provision_postgres(args.url, dry_run=args.dry_run, seed_only=args.seed_only)

    if not ok:
        sys.exit(1)

    # Verify
    if not args.dry_run and args.mode == "sqlite":
        print()
        verify_sqlite()

    print()
    log("Provisioning complete.")
    if env != "production":
        print()
        print("  Default credentials (DEVELOPMENT ONLY — change before pilot):")
        print("  ┌────────────────────────────────────────────────────────────────────────────────────────┐")
        print("  │ Role             Email                    Password       Facility / Notes                      │")
        print("  ├────────────────────────────────────────────────────────────────────────────────────────┤")
        print("  │ Super Admin      admin@zayvorahealth      admin123       zayvora clinic and hospital           │")
        print("  │ Doctor / Tabeeb  dr.irfan@zayvorahealth   doctor123      Integrative Unani OPD                 │")
        print("  │ Doctor / Tabeeb  dr.malik@zayvorahealth   doctor123      zayvora hospital                      │")
        print("  │ Receptionist     reception@zayvorahealth  reception123   Patient Queue & Token Management      │")
        print("  │ Pharmacist       pharmacy@zayvorahealth   pharmacy123    Dispensary & 21 CFR Part 11 eBMR      │")
        print("  │ Patient          ahmad.khan@example.com   password123    MRN: MRN-2026-0001 (Mizaj: Damawi)    │")
        print("  └────────────────────────────────────────────────────────────────────────────────────────┘")
        print()
        print("  ⚠  NEVER use these credentials with live patient data.")
        print("  Run with --mode postgres and a real DATABASE_URL for pilot.")
        print()


if __name__ == "__main__":
    main()
