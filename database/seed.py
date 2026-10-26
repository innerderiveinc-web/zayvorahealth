#!/usr/bin/env python3
"""
ZAYVORA Health OS — Unified Database Seeder CLI
================================================
Canonical unified seeder supporting multiple profiles:
- baseline: Core organizations, facilities, users, and clinical terms
- demo: Synthetic patient records, encounters, and active prescriptions
- pilot: Multi-tenant pilot clinical centers and doctor accounts
- zfie: ZAYVORA Formulation Intelligence Engine compounds and evidence
- all: Executes all seed profiles in topological dependency order

Usage:
    python3 database/seed.py --profile=all
    python3 database/seed.py --profile=baseline
    python3 database/seed.py --profile=demo
    python3 database/seed.py --profile=pilot
    python3 database/seed.py --profile=zfie
"""

import argparse
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "zayvora_live.db")


def run_baseline(db_path: str = DB_PATH):
    """Seed baseline schema, users, organizations, and terminology."""
    from database.seed_data import seed_sqlite_standard
    print(f"[Seed:Baseline] Seeding core structures into {os.path.basename(db_path)}...")
    seed_sqlite_standard(db_path)
    print("  ✓ Baseline seed complete.")


def run_demo(db_path: str = DB_PATH):
    """Seed demonstration clinical patients and prescriptions."""
    from database.seed_demo_data import seed
    print(f"[Seed:Demo] Seeding clinical demo fixtures into {os.path.basename(db_path)}...")
    seed()
    print("  ✓ Demo seed complete.")


def run_pilot(db_path: str = DB_PATH):
    """Seed institutional pilot tenants and physician credentials."""
    from database.seed_pilot_tenants import seed_pilot_tenants
    print(f"[Seed:Pilot] Seeding pilot tenant organizations into {os.path.basename(db_path)}...")
    res = seed_pilot_tenants(db_path)
    print(f"  ✓ Pilot seed complete ({res.get('organizations', 0)} orgs, {res.get('facilities', 0)} facilities).")


def run_zfie(db_path: str = DB_PATH):
    """Seed ZFIE formulation intelligence and evidence matrix."""
    from database.seed_zfie_live import seed_zfie_database
    print(f"[Seed:ZFIE] Seeding computational formulation library into {os.path.basename(db_path)}...")
    seed_zfie_database(db_path)
    print("  ✓ ZFIE seed complete.")


def main():
    parser = argparse.ArgumentParser(
        description="ZAYVORA Health OS — Unified Database Seeder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--profile",
        choices=["all", "baseline", "demo", "pilot", "zfie"],
        default="all",
        help="Seed profile to apply (default: all)",
    )
    parser.add_argument(
        "--db",
        default=DB_PATH,
        help="Target SQLite database path (default: database/zayvora_live.db)",
    )
    args = parser.parse_args()

    print("=================================================================")
    print(f" ZAYVORA Health OS — Database Seeding: Profile [{args.profile.upper()}]")
    print("=================================================================")

    if args.profile in ("baseline", "all"):
        run_baseline(args.db)

    if args.profile in ("pilot", "all"):
        run_pilot(args.db)

    if args.profile in ("zfie", "all"):
        run_zfie(args.db)

    if args.profile in ("demo", "all"):
        run_demo(args.db)

    print("=================================================================")
    print("✓ All requested seed operations completed successfully.")
    print("=================================================================")


if __name__ == "__main__":
    main()
