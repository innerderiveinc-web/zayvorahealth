#!/usr/bin/env python3
"""Import CSV files (exported from SQLite) into a PostgreSQL database using psycopg2.
Usage:
  python3 import_csv_to_postgres.py \
      --postgres-url postgresql+psycopg://user:pass@host:5432/dbname \
      --csv-dir <directory-with-csv-files>
The script expects one CSV per table, with a header row matching column names.
"""
import argparse
import os
from pathlib import Path
import psycopg2
from psycopg2 import sql

def import_table(conn, table_name, csv_path):
    with open(csv_path, "r", encoding="utf-8") as f:
        # Build COPY command with header
        copy_sql = sql.SQL("COPY {} ({}) FROM STDIN WITH CSV HEADER").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join([sql.Identifier(col) for col in next(csv_reader(f))])
        )
    # Re-open file for COPY (psycopg2 needs file pointer at start)
    with open(csv_path, "r", encoding="utf-8") as f:
        cur = conn.cursor()
        cur.copy_expert(copy_sql.as_string(conn), f)
        conn.commit()
        print(f"Imported {table_name} from {csv_path}")

def csv_reader(file_obj):
    import csv
    return csv.reader(file_obj)

def main():
    parser = argparse.ArgumentParser(description="Import CSV files into PostgreSQL")
    parser.add_argument("--postgres-url", required=True, help="SQLAlchemy‑style PostgreSQL URL")
    parser.add_argument("--csv-dir", required=True, help="Directory containing CSV files")
    args = parser.parse_args()

    # Convert SQLAlchemy URL to psycopg2 DSN (remove +psycopg)
    dsn = args.postgres_url.replace("postgresql+psycopg://", "postgresql://")
    conn = psycopg2.connect(dsn)

    csv_dir = Path(args.csv_dir)
    for csv_path in csv_dir.glob("*.csv"):
        table_name = csv_path.stem
        import_table(conn, table_name, csv_path)

    conn.close()

if __name__ == "__main__":
    main()
