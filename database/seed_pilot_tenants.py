#!/usr/bin/env python3
"""
ZAYVORA Health™ — Phase 8 Clinical Pilot University Tenant Seeding Utility.

Provisions multi-tenant academic medical centers:
1. ZAYVORA Healthcare System - Central Hospital (Delhi)
2. ZAYVORA Healthcare System - Research Wing (SUMER, New Delhi)
3. ZAYVORA Healthcare System - Clinical Center (AKTC, Aligarh)
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PILOT_CENTERS = [
    {
        "id": "org-autc-delhi-001",
        "name": "ZAYVORA Healthcare System - Central Clinical Hub (Delhi)",
        "slug": "autc-delhi",
        "pi_name": "Hakeem Dr. Irfan Ashraf (BUMS, Chief Clinical Lead)",
        "pi_email": "clinical.lead@zayvora.clinical",
        "reg_no": "Facility ID: ZAY-DEL-01",
    },
    {
        "id": "org-jh-sumer-002",
        "name": "ZAYVORA Healthcare System - Academic Research Node (Simulation-1)",
        "slug": "jh-sumer",
        "pi_name": "Dr. Tariq Mahmood (BUMS, Academic Research Lead)",
        "pi_email": "research.sim1@zayvora.clinical",
        "reg_no": "Facility ID: ZAY-RES-02",
    },
    {
        "id": "org-amu-aktc-003",
        "name": "ZAYVORA Healthcare System - Collaborative Clinical Node (Simulation-2)",
        "slug": "amu-aktc",
        "pi_name": "Dr. Rehan Qureshi (BUMS, Clinical Specialist)",
        "pi_email": "clinic.sim2@zayvora.clinical",
        "reg_no": "Facility ID: ZAY-COL-03",
    },
]


def seed_pilot_tenants(target_db: str | None = None) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    db_file = target_db or os.path.join(BASE_DIR, "zayvora_pilot_tenants.db")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS pilot_organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            pi_name TEXT NOT NULL,
            pi_email TEXT NOT NULL,
            reg_no TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS pilot_cohort_subjects (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            pseudonym TEXT NOT NULL,
            age INTEGER NOT NULL,
            mizaj_cohort TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (org_id) REFERENCES pilot_organizations(id)
        );
    """)

    seeded_orgs = 0
    seeded_subjects = 0

    for center in PILOT_CENTERS:
        cur.execute(
            "INSERT OR REPLACE INTO pilot_organizations VALUES (?, ?, ?, ?, ?, ?, ?)",
            (center["id"], center["name"], center["slug"], center["pi_name"], center["pi_email"], center["reg_no"], now),
        )
        seeded_orgs += 1

        # Seed sample trial subjects for each center (10 per center for verification)
        for i in range(1, 11):
            subj_id = f"SUBJ-{center['slug'].upper()}-{i:03d}"
            cohort = ["Damwi", "Safrawi", "Balghami", "Saudawi"][i % 4]
            cur.execute(
                "INSERT OR REPLACE INTO pilot_cohort_subjects VALUES (?, ?, ?, ?, ?, ?)",
                (subj_id, center["id"], f"PSEUDO-{center['slug'].upper()}-{i:03d}", 20 + i * 4, cohort, now),
            )
            seeded_subjects += 1

    conn.commit()
    conn.close()

    return {
        "status": "PILOT_TENANTS_SEEDED",
        "database_file": db_file,
        "centers_seeded": seeded_orgs,
        "trial_subjects_seeded": seeded_subjects,
        "timestamp_utc": now,
    }


def main():
    parser = argparse.ArgumentParser(description="ZAYVORA Pilot Tenant Seeder")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    res = seed_pilot_tenants()
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("=================================================================")
        print(" ZAYVORA HEALTH™ — PHASE 8 CLINICAL PILOT TENANT SEEDER")
        print("=================================================================")
        print(f" Status          : {res['status']}")
        print(f" Database Target : {res['database_file']}")
        print(f" Centers Seeded  : {res['centers_seeded']}")
        print(f" Subjects Seeded : {res['trial_subjects_seeded']}")
        print("=================================================================")


if __name__ == "__main__":
    main()
