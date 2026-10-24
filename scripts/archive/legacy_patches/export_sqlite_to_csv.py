#!/usr/bin/env python3
"""Export all tables from the SQLite development database to CSV files.
Usage:
  python3 export_sqlite_to_csv.py --db-path <path-to-sqlite> --out-dir <output-directory>
The script creates one CSV file per table in the output directory.
"""
import argparse
import os
import sqlite3
import csv

def export_table(conn, table, out_dir):
    cursor = conn.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{table}.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)
    print(f"Exported {table} -> {out_path} ({len(rows)} rows)")

def main():
    parser = argparse.ArgumentParser(description="Export SQLite DB tables to CSV")
    parser.add_argument("--db-path", required=True, help="Path to SQLite .db file")
    parser.add_argument("--out-dir", default="database/export", help="Directory to place CSVs")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        export_table(conn, table, args.out_dir)
    conn.close()

if __name__ == "__main__":
    main()
