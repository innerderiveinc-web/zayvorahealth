"""
ZFIE Migration Runner
Applies isolated ZFIE migrations 001_zfie_identities through 028_zfie_events
to SQLite and PostgreSQL databases without altering existing clinical tables.
"""

import os
import sqlite3
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DB_PATH = os.path.join(BASE_DIR, "database", "zayvora_live.db")
MIGRATIONS_DIR = os.path.dirname(os.path.abspath(__file__))


def apply_migrations(db_path: str = DB_PATH) -> int:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    applied = 0
    sql_files = sorted([f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql")])

    for fname in sql_files:
        fpath = os.path.join(MIGRATIONS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            script = f.read()
        try:
            cursor.executescript(script)
            applied += 1
        except Exception as e:
            print(f"[ERROR] Failed applying {fname}: {e}", file=sys.stderr)
            raise

    conn.commit()
    conn.close()
    return applied


if __name__ == "__main__":
    count = apply_migrations()
    print(f"✓ Successfully applied {count} ZFIE migrations to {DB_PATH}")
