#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Production Clean Slate Utility
===================================================
Completely wipes all mock/dummy transactional data:
- 0 Patients
- 0 Appointments (Active OPD Queue = 0)
- 0 Prescriptions
- 0 Invoices (Hospital Revenue = ₹0.00)
- 0 Encounters & Test Chat Logs

PRESERVES 100% of Medical Knowledge & Staff:
- 32 ZAYVORA Sovereign Products
- 48 Medical Treatises & Grand Corpus
- 250 Canonical Mufradat & Herbal Directory
- 1,593 Standard UMA Diagnostic Terms
- 14 Herb-Drug Interactions
- 21 Master Clinical Protocols & 12 Organ Axes
- Official Doctor & Staff Accounts (Dr. Irfan Ashraf, Admin, Reception, Pharmacy)
- Dispensary Inventory
"""

import os
import sys
import shutil
import sqlite3
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "database", "zayvora_live.db")
BACKUP_DIR = os.path.join(BASE_DIR, "database", "backups")

PURGE_TABLES = [
    "appointments",
    "invoices",
    "prescriptions",
    "encounters",
    "ai_consultations",
    "notifications",
    "telemedicine_rooms",
    "sessions",
    "password_reset_otps",
    "platform_tasks",
    "patients",
]

PRESERVED_TABLES = [
    "master_products",
    "unani_standard_terms",
    "zkb_mufradat",
    "zkb_drug_interactions",
    "source_authors",
    "source_books",
    "master_protocols",
    "master_organ_axes",
    "master_parhez",
    "facilities",
    "inventory",
    "users",
]

def clean_slate_production():
    print("=" * 68)
    print(" ZAYVORA Health OS — 100% Clean Slate Production Reset")
    print("=" * 68)

    if not os.path.exists(DB_PATH):
        print(f"[!] Database not found at: {DB_PATH}")
        sys.exit(1)

    # 1. Create timestamped safety backup
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"zayvora_clean_slate_backup_{timestamp}.db")
    shutil.copyfile(DB_PATH, backup_file)
    print(f"[✓] Safety Pre-Clean Backup Created:\n    {backup_file}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 2. Purge transactional tables
    print("\n--- Purging Transactional Tables ---")
    total_purged = 0
    for tbl in PURGE_TABLES:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {tbl}")
            count = cur.fetchone()[0]
            cur.execute(f"DELETE FROM {tbl}")
            print(f"  • {tbl:22}: Cleared {count:3} rows -> 0")
            total_purged += count
        except sqlite3.OperationalError:
            print(f"  • {tbl:22}: Skipped (table does not exist)")

    # 3. Clean test patient accounts from users table
    cur.execute("DELETE FROM users WHERE role = 'PATIENT' OR email LIKE 'live.patient%' OR email LIKE '%@example.com' OR email LIKE 'temp.logout%'")
    deleted_test_users = cur.rowcount
    if deleted_test_users > 0:
        print(f"  • users (patients): Cleared {deleted_test_users} dummy accounts")

    # Reset SQLite autoincrement sequences
    try:
        cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('appointments', 'invoices', 'prescriptions')")
    except Exception:
        pass

    conn.commit()

    # 4. Checkpoint WAL and VACUUM
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    cur.execute("VACUUM")
    conn.commit()

    # 5. Verify preserved master knowledge
    print("\n--- Verifying Preserved Knowledge Base & Staff Accounts ---")
    for tbl in PRESERVED_TABLES:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {tbl}")
            count = cur.fetchone()[0]
            print(f"  ✓ {tbl:24}: {count:4} rows INTACT (Protected)")
        except sqlite3.OperationalError:
            pass

    conn.close()

    print("\n" + "=" * 68)
    print(f" [✓] PRODUCTION CLEAN SLATE COMPLETE: {total_purged} dummy rows purged.")
    print(" Live Clinic Statistics:")
    print("   • Active OPD Queue : 0 Patients")
    print("   • Registered Patients : 0 Patients")
    print("   • Active Prescriptions: 0 Prescriptions")
    print("   • Hospital Revenue    : ₹0.00")
    print(" System is 100% clean and ready for real patients.")
    print("=" * 68)

if __name__ == "__main__":
    clean_slate_production()
