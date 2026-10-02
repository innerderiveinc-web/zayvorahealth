#!/usr/bin/env python3
"""
Unified Migration Orchestrator for ZAYVORA Multi-Service Relational Databases.

Usage:
  python3 database/migrations/migrate.py [upgrade|downgrade] [all|identity|clinical|therapeutic|ai]
"""
import os
import sys
import argparse
import subprocess

SERVICES = ["identity", "clinical", "therapeutic", "ai", "knowledge"]

def run_service_migration(service: str, action: str = "upgrade", revision: str = "head") -> int:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    ini_path = os.path.join(base_dir, f"database/migrations/{service}/alembic.ini")
    
    cmd = ["alembic", "-c", ini_path, action, revision]
    print(f"===> [{service.upper()}] Running: {' '.join(cmd)}")
    
    env = os.environ.copy()
    proc = subprocess.run(cmd, cwd=base_dir, env=env)
    return proc.returncode

def main():
    parser = argparse.ArgumentParser(description="ZAYVORA Multi-Database Migration Runner")
    parser.add_argument("action", choices=["upgrade", "downgrade", "current", "history"], default="upgrade", nargs="?")
    parser.add_argument("target", choices=["all", "identity", "clinical", "therapeutic", "ai", "knowledge"], default="all", nargs="?")
    parser.add_argument("--revision", default="head", help="Revision target (default: head)")

    args = parser.parse_args()

    targets = SERVICES if args.target == "all" else [args.target]

    failed = []
    for s in targets:
        code = run_service_migration(s, args.action, args.revision)
        if code != 0:
            failed.append(s)

    if failed:
        print(f"\n[ERROR] Migration failed for services: {', '.join(failed)}")
        sys.exit(1)
    else:
        print(f"\n[SUCCESS] Migrations {args.action} completed successfully for: {', '.join(targets)}")

if __name__ == "__main__":
    main()
