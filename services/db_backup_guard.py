#!/usr/bin/env python3
"""
ZAYVORA Health OS — Autonomous Database Safety & Auto-Backup Daemon
Runs automated integrity checks and creates rotating snapshot backups.
Can be triggered manually, on startup, or scheduled via cron.
"""

import os
import sys
import sqlite3
import shutil
import time
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "zayvora_live.db")
BACKUP_DIR = os.path.join(BASE_DIR, "database", "backups")

def run_integrity_and_backup(max_backups=7):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    if not os.path.exists(DB_PATH):
        print(f"[Backup] Database not found at {DB_PATH}")
        return False

    # 1. Run PRAGMA integrity check
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cur = conn.cursor()
        cur.execute("PRAGMA integrity_check")
        status = cur.fetchone()[0]
        conn.close()
        if status != "ok":
            print(f"[CRITICAL ALERT] Database integrity failed: {status}")
            return False
    except Exception as e:
        print(f"[CRITICAL ALERT] Error inspecting database: {e}")
        return False

    # 2. Create online non-blocking vacuum snapshot backup
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"zayvora_backup_{timestamp}.db")
    try:
        source_conn = sqlite3.connect(DB_PATH, timeout=20.0)
        dest_conn = sqlite3.connect(backup_path)
        source_conn.backup(dest_conn)
        dest_conn.close()
        source_conn.close()
        size_kb = os.path.getsize(backup_path) / 1024
        print(f"[✓ Backup OK] Snapshot created: {os.path.basename(backup_path)} ({size_kb:.1f} KB)")
    except Exception as e:
        print(f"[Backup Error] Failed to create backup: {e}")
        return False

    # 3. Clean up oldest backups beyond retention limit
    existing_backups = sorted(glob.glob(os.path.join(BACKUP_DIR, "zayvora_backup_*.db")))
    if len(existing_backups) > max_backups:
        for old in existing_backups[:-max_backups]:
            try:
                os.remove(old)
                for ext in ["-wal", "-shm"]:
                    companion = old + ext
                    if os.path.exists(companion):
                        os.remove(companion)
                print(f"[Backup Prune] Removed stale backup: {os.path.basename(old)}")
            except Exception:
                pass

    return True

if __name__ == "__main__":
    success = run_integrity_and_backup()
    sys.exit(0 if success else 1)
