#!/usr/bin/env python3
"""
ZAYVORA Health OS — Qualification Accuracy Correction:
Accurately reflect Hakeem Dr. Irfan Ashraf's credentials as:
BUMS (Unani) — strictly removing any unintended 'MD' references across all files.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPLACEMENTS = [
    ("Hakeem Dr. Irfan Ashraf (BUMS, MD Unani)", "Hakeem Dr. Irfan Ashraf (BUMS)"),
    ("Hakeem Dr. Irfan Ashraf (BUMS, MD)", "Hakeem Dr. Irfan Ashraf (BUMS)"),
    ("BUMS, MD (Unani), Senior Integrative Physician", "BUMS (Unani), Senior Integrative Physician"),
    ("BUMS, MD (Unani), Senior Integrative Clinician", "BUMS (Unani), Senior Integrative Clinician"),
    ("BUMS, MD (Unani)", "BUMS (Unani)"),
    ("BUMS, MD", "BUMS"),
]

def correct_file(fpath):
    if not os.path.exists(fpath):
        return
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    for old_str, new_str in REPLACEMENTS:
        if old_str in content:
            content = content.replace(old_str, new_str)
            modified = True

    if modified:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Corrected credentials in {fpath}")

def main():
    target_files = [
        os.path.join(BASE_DIR, "app.html"),
        os.path.join(BASE_DIR, "docs", "app.html"),
        os.path.join(BASE_DIR, "index.html"),
        os.path.join(BASE_DIR, "docs", "index.html"),
        os.path.join(BASE_DIR, "website.html"),
        os.path.join(BASE_DIR, "docs", "website.html"),
        os.path.join(BASE_DIR, "scripts", "inject_fast_matab_and_bilingual_slip.py"),
        os.path.join(BASE_DIR, "scripts", "compile_zayvora_master_book.py"),
        os.path.join(BASE_DIR, "docs", "THE_ZAYVORA_DOCTRINE_MASTER_BOOK.md"),
        os.path.join(BASE_DIR, "docs", "THE_ZAYVORA_DOCTRINE_MASTER_BOOK.html"),
    ]
    for tf in target_files:
        correct_file(tf)

    # Re-run compile_zayvora_master_book.py
    os.system(f"python3 {os.path.join(BASE_DIR, 'scripts', 'compile_zayvora_master_book.py')}")

if __name__ == "__main__":
    main()
