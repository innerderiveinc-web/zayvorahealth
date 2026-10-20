#!/usr/bin/env python3
"""
ZAYVORA Health OS — Release Packaging Engine
Builds the canonical zayvora-health-os-production-latest.zip excluding cache and ephemeral logs.
"""

import os
import zipfile
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_ZIP = os.path.join(BASE_DIR, "zayvora-health-os-production-latest.zip")

EXCLUDE_DIR_NAMES = {
    ".git", "__pycache__", ".pytest_cache", ".system_generated",
    "node_modules", ".vscode", ".idea", "venv", ".venv",
    "backups", "scratch"
}

EXCLUDE_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".DS_Store", ".db-shm", ".db-wal", ".pid", ".lock"
}

EXCLUDE_FILES = {
    ".env",
    ".env.local",
    ".env.production",
    "zayvora-health-os-production-latest.zip",
    "zayvora-platform-phase0-4.zip",
    "zayvora-website.zip"
}


def should_exclude_dir(rel_path: str) -> bool:
    parts = rel_path.split(os.sep)
    for part in parts:
        if part in EXCLUDE_DIR_NAMES:
            return True
        if part.startswith("venv") or part.startswith(".venv"):
            return True
    return False


def should_exclude_file(filename: str, rel_path: str) -> bool:
    if filename in EXCLUDE_FILES:
        return True
    if filename.startswith(".env") and filename != ".env.example" and filename != ".env.test.example":
        return True
    if filename.startswith("scratch_") or filename.startswith(".DS_Store"):
        return True
    ext = os.path.splitext(filename)[1]
    if ext in EXCLUDE_EXTENSIONS:
        return True
    # Exclude ad-hoc database backups while retaining canonical database/zayvora_live.db
    if "backups" in rel_path.split(os.sep):
        return True
    if "backup" in filename.lower() and ext == ".db":
        return True
    return False


def sanitize_databases_for_release():
    """Sanitizes local databases before packaging: removes transient sessions and active OTPs (OS-010)."""
    import sqlite3
    db_file = os.path.join(BASE_DIR, "database", "zayvora_live.db")
    if os.path.isfile(db_file):
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = set(r[0] for r in c.fetchall())
            if "sessions" in tables:
                c.execute("DELETE FROM sessions")
            if "password_reset_otps" in tables:
                c.execute("DELETE FROM password_reset_otps")
            conn.commit()
            c.execute("VACUUM")
            conn.close()
            print("✓ Database hygiene: purged transient session state and OTPs from zayvora_live.db.")
        except Exception as e:
            print(f"[WARN] Database sanitation notice: {e}")


def package_release():
    print(f"Building canonical production release: {OUTPUT_ZIP}...")
    sanitize_databases_for_release()
    total_files = 0
    total_bytes = 0

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for root, dirs, files in os.walk(BASE_DIR):
            rel_dir = os.path.relpath(root, BASE_DIR)
            
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if not should_exclude_dir(os.path.join(rel_dir, d) if rel_dir != "." else d)]

            for file in sorted(files):
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, BASE_DIR)

                if should_exclude_file(file, rel_path):
                    continue

                zipf.write(abs_path, rel_path)
                total_files += 1
                total_bytes += os.path.getsize(abs_path)

    zip_size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"✓ Packaged {total_files} clean production files ({zip_size_mb:.2f} MB) into {os.path.basename(OUTPUT_ZIP)}.")

    # Also sync to artifact directory if available
    artifact_dir = "/Users/irfanashraf/.gemini/antigravity/brain/aef53974-5787-48a1-b0a4-20feaf895e12"
    if os.path.isdir(artifact_dir):
        import shutil
        dest = os.path.join(artifact_dir, os.path.basename(OUTPUT_ZIP))
        shutil.copy2(OUTPUT_ZIP, dest)
        print(f"✓ Copied release archive to artifact directory: {dest}")


if __name__ == "__main__":
    package_release()
