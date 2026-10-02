#!/usr/bin/env python3
"""Validate that SQLite and PostgreSQL tables contain identical data.
It compares row counts and an MD5 checksum of each table's CSV dump.
Usage:
  python3 validate_migration.py \
      --sqlite-db path/to/sqlite.db \
      --postgres-url postgresql+psycopg://user:pass@host:5432/dbname
The script prints a markdown table with the results.
"""
import argparse
import sqlite3
import csv
import hashlib
import sys
from pathlib import Path
import psycopg2

def dump_table_sqlite(conn, table):
    cur = conn.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    cols = [description[0] for description in cur.description]
    return cols, rows

def dump_table_postgres(conn, table):
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        cols = [desc.name for desc in cur.description]
    return cols, rows

def md5_of_rows(cols, rows):
    # deterministic ordering: sort rows by all columns
    sorted_rows = sorted(rows)
    hasher = hashlib.md5()
    # write header
    header = ",".join(cols).encode()
    hasher.update(header)
    for row in sorted_rows:
        line = ",".join(str(v) if v is not None else "" for v in row).encode()
        hasher.update(line)
    return hasher.hexdigest()

def list_sqlite_tables(conn):
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    return [row[0] for row in cur.fetchall()]

def list_postgres_tables(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public';")
        return [row[0] for row in cur.fetchall()]

def main():
    parser = argparse.ArgumentParser(description='Validate SQLite → PostgreSQL migration')
    parser.add_argument('--sqlite-db', required=True, help='Path to SQLite .db file')
    parser.add_argument('--postgres-url', required=True, help='SQLAlchemy style PostgreSQL URL')
    args = parser.parse_args()

    # Connect to SQLite
    sqlite_conn = sqlite3.connect(args.sqlite_db)
    # Convert SQLAlchemy URL to psycopg2 DSN
    dsn = args.postgres_url.replace('postgresql+psycopg://', 'postgresql://')
    pg_conn = psycopg2.connect(dsn)

    sqlite_tables = set(list_sqlite_tables(sqlite_conn))
    pg_tables = set(list_postgres_tables(pg_conn))
    common = sqlite_tables.intersection(pg_tables)

    print("| Table | SQLite rows | Postgres rows | SHA256 match |")
    print("|-------|------------|---------------|--------------|")
    for table in sorted(common):
        s_cols, s_rows = dump_table_sqlite(sqlite_conn, table)
        p_cols, p_rows = dump_table_postgres(pg_conn, table)
        s_md5 = md5_of_rows(s_cols, s_rows)
        p_md5 = md5_of_rows(p_cols, p_rows)
        match = "✅" if s_md5 == p_md5 else "❌"
        print(f"| {table} | {len(s_rows)} | {len(p_rows)} | {match} |")

    # Report missing tables
    if sqlite_tables - pg_tables:
        print("\nTables only in SQLite:", ", ".join(sorted(sqlite_tables - pg_tables)))
    if pg_tables - sqlite_tables:
        print("\nTables only in PostgreSQL:", ", ".join(sorted(pg_tables - sqlite_tables)))

    sqlite_conn.close()
    pg_conn.close()

if __name__ == "__main__":
    main()
