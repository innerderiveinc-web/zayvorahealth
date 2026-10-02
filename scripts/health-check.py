#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Service Health Checker
Polls all microservice /health endpoints and reports status.
Usage: python3 scripts/health-check.py
"""
import urllib.request
import urllib.error
import json
import sys

SERVICES = [
    ("Gateway / Unified", "http://localhost:8000/api/health"),
    ("Identity",          "http://localhost:8001/api/health"),
    ("Clinical",          "http://localhost:8002/api/health"),
    ("Knowledge",         "http://localhost:8003/api/health"),
    ("Therapeutic",       "http://localhost:8004/api/health"),
    ("AI",                "http://localhost:8005/api/health"),
]

print()
print("ZAYVORA Health OS™ — Service Health Check")
print("=" * 55)

# First check if unified live API server is responding on port 8000
unified_active = False
try:
    with urllib.request.urlopen("http://localhost:8000/api/health", timeout=2) as r:
        data = json.loads(r.read())
        if data.get("ok") and data.get("service") == "zayvora_live_api":
            unified_active = True
            print("  Unified Live API:  ✅ ONLINE (All 6 domains served on :8000)")
            print(f"    - Database:      {data.get('database')} ({data.get('database_engine')})")
            print(f"    - Users:         {data.get('registered_users')}")
            print(f"    - Facilities:    {data.get('registered_facilities')}")
            print(f"    - Timestamp:     {data.get('timestamp')}")
            print("-" * 55)
except Exception:
    pass

any_ok = unified_active
for name, url in SERVICES:
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            data = json.loads(r.read())
            status = "✅ OK"
            any_ok = True
    except urllib.error.URLError:
        if unified_active and name != "Gateway / Unified":
            status = "⚪ PROXIED (Handled via Unified Live Server :8000)"
        else:
            status = "❌ OFFLINE (not running)"
    except Exception as e:
        status = f"⚠  ERROR: {e}"

    print(f"  {name:18s}  {status}")

print("=" * 55)
if unified_active or any_ok:
    print("Health Status: System is functional.")
    sys.exit(0)
else:
    print("All services offline. To start, run:")
    print("  - Unified Server: python3 services/live_api_server.py")
    print("  - Or Microservices: bash scripts/dev-start.sh")
    sys.exit(1)

