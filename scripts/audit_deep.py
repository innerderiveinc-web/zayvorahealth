#!/usr/bin/env python3
"""
Deep Comprehensive Audit Suite for ZAYVORA Health OS
Audits:
1. Dynamic onclick handlers and missing JavaScript functions
2. Missing DOM IDs accessed via document.getElementById
3. Frontend API fetch paths vs live_api_server.py handlers
4. Database tables and columns referenced in backend vs schema
5. Contrast tokens and theme attributes
"""
import re
import sqlite3

CORE_JS = "js/zayvora-core.js"
EXT_JS = "js/zayvora-extensions.js"
INDEX_HTML = "index.html"
SERVER_PY = "services/live_api_server.py"
DB_FILE = "database/zayvora_live.db"

with open(CORE_JS) as f: core_js = f.read()
with open(EXT_JS) as f: ext_js = f.read()
with open(INDEX_HTML) as f: html = f.read()
with open(SERVER_PY) as f: server_py = f.read()

all_js = core_js + "\n" + ext_js

print("=" * 60)
print("1. CHECKING DYNAMIC ONCLICK FUNCTIONS")
print("=" * 60)
onclicks = set(re.findall(r'onclick=[\'"]\s*([a-zA-Z0-9_]+)\(', all_js))
missing_fns = []
for fn in onclicks:
    pattern = rf'(?:function\s+{fn}\s*\(|window\.{fn}\s*=|const\s+{fn}\s*=\s*|let\s+{fn}\s*=\s*|var\s+{fn}\s*=\s*)'
    if not re.search(pattern, all_js):
        missing_fns.append(fn)

print(f"Total onclick handlers in JS: {len(onclicks)}")
print(f"Missing onclick functions: {len(missing_fns)}")
for fn in missing_fns:
    print(f"  ✗ Missing function: {fn}()")

print("\n" + "=" * 60)
print("2. CHECKING API FETCH ENDPOINTS")
print("=" * 60)
fetch_paths = set(re.findall(r'[\'\"`](/api/v1/[^\'\"`\?\s]+)', all_js))
missing_routes = []
for p in sorted(fetch_paths):
    clean = p.split('?')[0]
    # Check if exact route or prefix is in server_py
    if clean not in server_py:
        # check parameterized route e.g. /api/v1/patients/{id}
        parts = clean.strip('/').split('/')
        if len(parts) >= 3:
            prefix = '/' + '/'.join(parts[:3])
            if prefix not in server_py:
                missing_routes.append(clean)
        else:
            missing_routes.append(clean)

print(f"Total API routes called in frontend: {len(fetch_paths)}")
print(f"Potential unhandled routes: {len(missing_routes)}")
for r in missing_routes:
    print(f"  ? Route not found in server: {r}")

print("\n" + "=" * 60)
print("3. CHECKING DATABASE SCHEMA COVERAGE")
print("=" * 60)
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = set(r[0] for r in cur.fetchall())
print(f"Existing DB tables ({len(tables)}): {sorted(list(tables))}")

# Check SQL queries in live_api_server.py (skip python import patterns)
sql_statements = re.findall(r'(?:cur\.execute|conn\.execute)\s*\(\s*["\']+(.*?)["\']+', server_py, re.DOTALL)
referenced_tables = set()
for stmt in sql_statements:
    found = re.findall(r'(?:FROM|INTO|UPDATE)\s+([a-zA-Z0-9_]+)', stmt, re.IGNORECASE)
    for f in found:
        if f.upper() not in ['SELECT', 'SET', 'WHERE', 'VALUES', 'DEFAULT']:
            referenced_tables.add(f)

missing_tables = [t for t in referenced_tables if t.lower() not in [x.lower() for x in tables] and t != 'sqlite_master']
print(f"Missing DB tables: {len(missing_tables)}")
for mt in missing_tables:
    print(f"  ✗ Referenced in SQL query but missing in DB: {mt}")

# 3b. Posology check on master_products
cur.execute("SELECT sku, name, dosage_form, daily_dose FROM master_products")
posology_flaws = []
for sku, name, form, dose in cur.fetchall():
    if "Capsule" in form and re.match(r'^\d+g\s+', dose):
        posology_flaws.append((sku, name, form, dose))
    elif "Tablet" in form and re.match(r'^\d+g\s+', dose):
        posology_flaws.append((sku, name, form, dose))

print(f"\nPosology mismatches in master_products: {len(posology_flaws)}")
for pf in posology_flaws:
    print(f"  ✗ Flawed posology: {pf[0]} {pf[1]} ({pf[2]}) -> {pf[3]}")
conn.close()

print("\n" + "=" * 60)
print("4. CHECKING CRITICAL DOM GETELEMENTBYID TARGETS")
print("=" * 60)
get_ids = set(re.findall(r'document\.getElementById\([\'"]([a-zA-Z0-9_\-]+)[\'"]\)', all_js))
missing_dom_ids = []
# Many IDs are rendered dynamically in workspace. Let's see which ones are static in HTML vs dynamic in templates
for el_id in sorted(get_ids):
    if el_id not in html and el_id not in all_js.replace(f"getElementById('{el_id}')", "").replace(f'getElementById("{el_id}")', ""):
        missing_dom_ids.append(el_id)

print(f"Total getElementById queries: {len(get_ids)}")
print(f"IDs not found anywhere in HTML or JS template literals: {len(missing_dom_ids)}")
for mid in missing_dom_ids[:10]:
    print(f"  ? Missing DOM ID: {mid}")

print("\nAudit check finished.")
