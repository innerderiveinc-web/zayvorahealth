#!/usr/bin/env python3
"""
ZAYVORA Health OS — Automated SQLite to PostgreSQL Live Migration Tool
Reads all 82 tables from SQLite (database/zayvora_live.db) and creates/populates PostgreSQL database.
Usage:
  DATABASE_URL="postgresql://user:pass@host:5432/dbname" python3 scripts/migrate_sqlite_to_pg.py
"""

import os
import sys
import sqlite3
import json

def migrate():
    pg_url = os.environ.get("DATABASE_URL")
    if not pg_url:
        print("ERROR: DATABASE_URL environment variable is required.")
        print("Example: DATABASE_URL='postgresql://postgres:password@localhost:5432/zayvora' python3 scripts/migrate_sqlite_to_pg.py")
        sys.exit(1)

    try:
        import psycopg2
        import psycopg2.extras
    except ImportError:
        print("ERROR: psycopg2 is not installed. Run: pip install psycopg2-binary")
        sys.exit(1)

    sqlite_path = os.path.join(os.path.dirname(__file__), "..", "database", "zayvora_live.db")
    if not os.path.exists(sqlite_path):
        print(f"ERROR: SQLite database not found at {sqlite_path}")
        sys.exit(1)

    print(f"Connecting to SQLite: {sqlite_path}")
    s_conn = sqlite3.connect(sqlite_path)
    s_cur = s_conn.cursor()

    if pg_url.startswith("postgres://"):
        pg_url = "postgresql://" + pg_url[len("postgres://"):]

    print(f"Connecting to PostgreSQL...")
    p_conn = psycopg2.connect(pg_url)
    p_cur = p_conn.cursor()

    # Get list of tables
    s_cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [r[0] for r in s_cur.fetchall()]
    print(f"Discovered {len(tables)} tables to migrate.")

    type_mapping = {
        "INTEGER": "BIGINT",
        "INT": "INTEGER",
        "TEXT": "TEXT",
        "REAL": "DOUBLE PRECISION",
        "FLOAT": "DOUBLE PRECISION",
        "BLOB": "BYTEA",
        "BOOLEAN": "BOOLEAN",
        "DATETIME": "TIMESTAMP",
        "VARCHAR": "VARCHAR",
    }

    success_count = 0
    total_rows = 0

    for table in tables:
        # Get column schema
        s_cur.execute(f"PRAGMA table_info(\"{table}\")")
        columns = s_cur.fetchall()
        
        col_defs = []
        col_names = []
        for col in columns:
            cid, name, col_type, notnull, dflt_value, pk = col
            col_names.append(f'"{name}"')
            base_type = col_type.split("(")[0].upper() if col_type else "TEXT"
            pg_type = type_mapping.get(base_type, "TEXT")
            if "(" in col_type:
                pg_type = col_type # preserve varchar length if any
            
            definition = f'"{name}" {pg_type}'
            if pk:
                definition += " PRIMARY KEY"
            if notnull and not pk:
                definition += " NOT NULL"
            col_defs.append(definition)

        create_sql = f'CREATE TABLE IF NOT EXISTS "{table}" ({", ".join(col_defs)});'
        try:
            p_cur.execute(create_sql)
            p_conn.commit()
        except Exception as e:
            print(f"  [Warning] Table '{table}' creation notice: {e}")
            p_conn.rollback()

        # Migrate rows
        s_cur.execute(f'SELECT * FROM "{table}"')
        rows = s_cur.fetchall()
        if rows:
            placeholders = ", ".join(["%s"] * len(col_names))
            insert_sql = f'INSERT INTO "{table}" ({", ".join(col_names)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;'
            try:
                psycopg2.extras.execute_batch(p_cur, insert_sql, rows, page_size=200)
                p_conn.commit()
                total_rows += len(rows)
                print(f"  ✓ {table}: {len(rows)} rows migrated")
            except Exception as e:
                print(f"  ✗ {table} row insert failed: {e}")
                p_conn.rollback()
        else:
            print(f"  - {table}: 0 rows (schema ready)")
        success_count += 1

    print(f"\n=======================================================")
    print(f"✓ MIGRATION COMPLETE: {success_count}/{len(tables)} tables processed ({total_rows} total rows).")
    print(f"=======================================================")
    s_conn.close()
    p_conn.close()

if __name__ == "__main__":
    migrate()
