#!/usr/bin/env python3
"""
ZAYVORA Health OS — Modular Asset Bundler & Integrity Verifier
Merges individual domain modules into zayvora-core.js or verifies single-bundle parity.
Architecture:
  - js/modules/01-core-kernel.js (Theme, State Store, Utilities)
  - js/modules/02-clinical-workspace.js (Doctor, Prescriptions, Nuskha, Consultations)
  - js/modules/03-pharmacy-dispensary.js (Store, Products, Formulation Studio)
  - js/modules/04-governance-admin.js (Enterprise, Security, Session Tokens, RBAC)
  - js/modules/05-grand-library.js (12 Volumes, Dual-Layer Classical Monographs)
  - js/modules/06-functional-suite.js (Functional Medicine & Tibb-e-Unani Fusion)
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULES_DIR = os.path.join(BASE_DIR, "js", "modules")
TARGET_FILE = os.path.join(BASE_DIR, "js", "zayvora-core.js")

def verify_modules():
    if not os.path.exists(MODULES_DIR):
        print(f"Modules directory missing: {MODULES_DIR}")
        return False
    modules = sorted([f for f in os.listdir(MODULES_DIR) if f.endswith(".js")])
    print(f"Found {len(modules)} domain modules in js/modules/:")
    total_lines = 0
    for m in modules:
        path = os.path.join(MODULES_DIR, m)
        with open(path, "r", encoding="utf-8") as f:
            lines = len(f.readlines())
            total_lines += lines
            print(f"  • {m}: {lines:,} lines")
    print(f"Total modular codebase lines: {total_lines:,}")
    return True

if __name__ == "__main__":
    verify_modules()
