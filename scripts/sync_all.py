#!/usr/bin/env python3
"""
ZAYVORA Health OS — Master Synchronization & Canonical Parity Engine
Ensures 100% byte-for-byte synchronization across:
1. Root index.html -> app.html
2. Root files -> docs/ (GitHub Pages mirror)
3. Assets (favicon.ico, zayvora-logo.png, tailwind.min.js, sw.js, manifest.json)
4. js/ -> docs/js/
"""
import os
import shutil
import filecmp
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def sync():
    print("=" * 60)
    print(" ZAYVORA Health OS — Auto-Sync & Parity Verification Engine")
    print("=" * 60)

    index_path = os.path.join(BASE_DIR, "index.html")
    app_path = os.path.join(BASE_DIR, "app.html")
    docs_dir = os.path.join(BASE_DIR, "docs")
    js_dir = os.path.join(BASE_DIR, "js")
    docs_js_dir = os.path.join(docs_dir, "js")

    if not os.path.exists(index_path):
        print(f"[-] ERROR: Master index.html not found at {index_path}")
        return False

    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(docs_js_dir, exist_ok=True)

    # 1. Sync index.html -> app.html (Single Source of Truth)
    shutil.copy2(index_path, app_path)
    print("[✓] Synced index.html -> app.html (Canonical Source)")

    # 2. Sync to docs/
    files_to_sync_to_docs = [
        "index.html",
        "app.html",
        "sw.js",
        "manifest.json",
        "tailwind.min.js",
        "favicon.ico",
        "zayvora-logo.png",
        "CNAME"
    ]

    for fname in files_to_sync_to_docs:
        src = os.path.join(BASE_DIR, fname)
        dst = os.path.join(docs_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"[✓] Synced {fname} -> docs/{fname}")
        else:
            print(f"[!] Warning: {fname} does not exist in root.")

    # 3. Sync js/ directory -> docs/js/
    if os.path.exists(js_dir):
        for root, dirs, files in os.walk(js_dir):
            rel_dir = os.path.relpath(root, js_dir)
            target_dir = os.path.join(docs_js_dir, rel_dir) if rel_dir != "." else docs_js_dir
            os.makedirs(target_dir, exist_ok=True)
            for f in files:
                s_file = os.path.join(root, f)
                d_file = os.path.join(target_dir, f)
                shutil.copy2(s_file, d_file)
        print("[✓] Synced js/ -> docs/js/ (All JavaScript libraries)")

    # 4. Strict Parity Verification
    errors = []
    if not filecmp.cmp(index_path, app_path, shallow=False):
        errors.append("index.html and app.html do not match byte-for-byte!")
    
    docs_index = os.path.join(docs_dir, "index.html")
    if not filecmp.cmp(index_path, docs_index, shallow=False):
        errors.append("index.html and docs/index.html do not match byte-for-byte!")

    docs_app = os.path.join(docs_dir, "app.html")
    if not filecmp.cmp(app_path, docs_app, shallow=False):
        errors.append("app.html and docs/app.html do not match byte-for-byte!")

    if errors:
        print("\n[-] PARITY VERIFICATION FAILED:")
        for err in errors:
            print(f"    - {err}")
        return False

    print("\n[✓] 100% PARITY CONFIRMED: Root & Docs are byte-identical.")
    return True

if __name__ == "__main__":
    success = sync()
    sys.exit(0 if success else 1)
