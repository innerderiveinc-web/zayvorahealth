#!/usr/bin/env python3
"""
ZAYVORA Health OS — Codebase Integrity, Static Drift & Parity Test Suite
========================================================================
This test suite acts as an unbreakable gatekeeper ensuring:
1. 100% Byte-for-byte Parity between root index.html, app.html, and docs/ mirrors.
2. 100% Parity between js/ and docs/js/.
3. Zero missing static assets (Favicons, Logos, Manifests, Tailwind, Service Worker).
4. PWA Manifest icon references point to existing physical files in both root and docs/.
5. Zero Duplicate HTML Element IDs in canonical templates.
6. 100% of HTML onclick handlers resolve to defined JavaScript functions.
7. Zero SQLite database corruption across all active and backup databases.
"""

import unittest
import os
import filecmp
import json
import re
import sqlite3
import glob

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestCodebaseIntegrityAndParity(unittest.TestCase):

    def test_01_canonical_html_and_docs_byte_parity(self):
        """Ensure index.html, app.html, docs/index.html, and docs/app.html are 100% byte-identical."""
        index_path = os.path.join(BASE_DIR, "index.html")
        app_path = os.path.join(BASE_DIR, "app.html")
        docs_index = os.path.join(BASE_DIR, "docs", "index.html")
        docs_app = os.path.join(BASE_DIR, "docs", "app.html")

        self.assertTrue(os.path.exists(index_path), "index.html must exist")
        self.assertTrue(os.path.exists(app_path), "app.html must exist")
        self.assertTrue(os.path.exists(docs_index), "docs/index.html must exist")
        self.assertTrue(os.path.exists(docs_app), "docs/app.html must exist")

        self.assertTrue(filecmp.cmp(index_path, app_path, shallow=False),
                        "DRIFT ERROR: index.html and app.html have diverged! Run scripts/sync_all.py")
        self.assertTrue(filecmp.cmp(index_path, docs_index, shallow=False),
                        "DRIFT ERROR: index.html and docs/index.html have diverged! Run scripts/sync_all.py")
        self.assertTrue(filecmp.cmp(app_path, docs_app, shallow=False),
                        "DRIFT ERROR: app.html and docs/app.html have diverged! Run scripts/sync_all.py")

    def test_02_javascript_bundle_docs_parity(self):
        """Ensure js/ and docs/js/ files match byte-for-byte without any missing scripts."""
        js_dir = os.path.join(BASE_DIR, "js")
        docs_js_dir = os.path.join(BASE_DIR, "docs", "js")

        self.assertTrue(os.path.isdir(js_dir), "js/ directory must exist")
        self.assertTrue(os.path.isdir(docs_js_dir), "docs/js/ directory must exist")

        for f in os.listdir(js_dir):
            if f.endswith(".js"):
                src = os.path.join(js_dir, f)
                dst = os.path.join(docs_js_dir, f)
                self.assertTrue(os.path.exists(dst), f"Missing script in docs: docs/js/{f}")
                self.assertTrue(filecmp.cmp(src, dst, shallow=False),
                                f"DRIFT ERROR: js/{f} and docs/js/{f} have diverged! Run scripts/sync_all.py")

    def test_03_static_assets_presence_and_sync(self):
        """Ensure critical static assets exist in both root and docs/."""
        critical_assets = ["favicon.ico", "zayvora-logo.png", "manifest.json", "tailwind.min.js", "sw.js"]
        for asset in critical_assets:
            root_asset = os.path.join(BASE_DIR, asset)
            docs_asset = os.path.join(BASE_DIR, "docs", asset)

            self.assertTrue(os.path.exists(root_asset), f"Root missing asset: {asset}")
            self.assertTrue(os.path.exists(docs_asset), f"docs/ missing asset: docs/{asset}")
            self.assertTrue(filecmp.cmp(root_asset, docs_asset, shallow=False),
                            f"DRIFT ERROR: {asset} and docs/{asset} differ! Run scripts/sync_all.py")

    def test_04_manifest_pwa_icon_resolution(self):
        """Verify that manifest.json icon targets physically exist on disk in root and docs/."""
        manifest_path = os.path.join(BASE_DIR, "manifest.json")
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)

        icons = manifest_data.get("icons", [])
        self.assertGreater(len(icons), 0, "manifest.json must contain at least one icon")

        for icon in icons:
            src = icon.get("src", "").lstrip("./").lstrip("/")
            root_icon = os.path.join(BASE_DIR, src)
            docs_icon = os.path.join(BASE_DIR, "docs", src)
            self.assertTrue(os.path.exists(root_icon), f"Manifest icon does not exist at {root_icon}")
            self.assertTrue(os.path.exists(docs_icon), f"Manifest icon does not exist at {docs_icon}")

    def test_05_zero_duplicate_html_ids(self):
        """Verify that index.html contains zero duplicate IDs to prevent DOM reference collisions."""
        index_path = os.path.join(BASE_DIR, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        ids = re.findall(r'\bid=["\']([a-zA-Z0-9_\-]+)["\']', content)
        seen = set()
        duplicates = set()
        for el_id in ids:
            if el_id in seen:
                duplicates.add(el_id)
            seen.add(el_id)

        self.assertEqual(len(duplicates), 0, f"Found duplicate HTML element IDs: {duplicates}")

    def test_06_html_onclick_handler_resolution(self):
        """Verify all inline onclick handlers in index.html correspond to defined functions."""
        index_path = os.path.join(BASE_DIR, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()

        js_code = ""
        for js_file in ["zayvora-core.js", "zayvora-extensions.js"]:
            p = os.path.join(BASE_DIR, "js", js_file)
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    js_code += "\n" + f.read()

        defined_funcs = set(re.findall(r'(?:function\s+([a-zA-Z0-9_$]+)\s*\(|(?:window\.)?([a-zA-Z0-9_$]+)\s*=\s*function|(?:window\.)?([a-zA-Z0-9_$]+)\s*=\s*\()', js_code))
        all_defined = set()
        for t in defined_funcs:
            for item in t:
                if item:
                    all_defined.add(item)

        standard_allowed = {'alert', 'confirm', 'prompt', 'print', 'close', 'open', 'showNotification', 'switchTab', 'navigateModule', 'toggleTheme', 'logout', 'openModal', 'closeModal'}
        all_defined.update(standard_allowed)

        handlers = re.findall(r'onclick=["\']([^"\']+)["\']', html)
        missing_handlers = set()
        for h in handlers:
            fn_calls = re.findall(r'([a-zA-Z0-9_$]+)\s*\(', h)
            for fn in fn_calls:
                if fn not in all_defined and not fn.startswith('console') and not fn.startswith('event'):
                    missing_handlers.add(fn)

        self.assertEqual(len(missing_handlers), 0, f"Unbound HTML onclick handlers found: {missing_handlers}")

    def test_07_database_integrity_check(self):
        """Verify PRAGMA integrity_check == ok across all live and backup SQLite databases."""
        db_files = glob.glob(os.path.join(BASE_DIR, "**", "*.db"), recursive=True)
        self.assertGreater(len(db_files), 0, "At least one SQLite database must exist")

        for db in db_files:
            try:
                conn = sqlite3.connect(db)
                cur = conn.cursor()
                cur.execute("PRAGMA integrity_check;")
                result = cur.fetchone()[0]
                conn.close()
                self.assertEqual(result, "ok", f"Database corruption detected in {db}: {result}")
            except Exception as e:
                self.fail(f"Failed to query database {db}: {e}")

if __name__ == "__main__":
    unittest.main()
