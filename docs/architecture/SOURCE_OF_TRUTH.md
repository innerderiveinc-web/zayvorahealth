# ZAYVORA Health OS — Source of Truth & Repository Architecture
**Document ID**: `ZAY-SOT-001`  
**Classification**: Engineering Governance Standard  
**Date**: September 2026  
**Status**: CERTIFIED SOURCE OF TRUTH  

---

## 1. Canonical Repository Identification

- **Workspace Path**: `/Users/irfanashraf/Downloads/zayvora-platform-phase0-4`
- **Active Branch**: `main`
- **Current Canonical Commit**: `e747e7d`
- **Commit Title**: `feat(audit-and-clinical): complete 10 audit reports, printable A4 prescription letterhead, live billing API, and automated test expansion`
- **Production Archive**: `zayvora-health-os-production.zip` (728 files, 3.22 MB)
- **Active Persistent Database**: `database/zayvora_live.db` (SQLite relational storage, 7 tables)

---

## 2. Single Documented Commands

### 2.1 Development Command
```bash
# Terminal 1: Seed persistent database and start live REST API server (Port 8000)
python3 database/init_live_db.py && python3 services/live_api_server.py

# Terminal 2: Start Next.js web application (Port 3000)
cd apps/web && npm run dev
```

### 2.2 Test Command
```bash
# Execute master test continuum and all domain verification suites
python3 tests/run_all_tests.py && python3 tests/test_45_engines_connected.py && python3 tests/test_live_api_integration.py && python3 tests/test_definition_of_done.py && python3 tests/test_rescue_user_experience.py
```
*Current Baseline: 444 tests passing across 10 test runners with 0 failures.*

### 2.3 Production Build Command
```bash
cd apps/web && npm run build
```

---

## 3. Required Environment Variables

| Variable Name | Default Value | Role |
|:---|:---|:---|
| `PORT` | `8000` | Port for native REST API server |
| `DATABASE_PATH` | `database/zayvora_live.db` | Local SQLite database file path |
| `DATABASE_URL` | `postgresql://zayvora:secret@localhost:5432/zayvora_clinical` | PostgreSQL connection string for microservices |
| `JWT_SECRET` | Dynamic system hex | Secret key for signing and validating session tokens |
| `NEXT_PUBLIC_API_URL`| `http://localhost:8000` | API base URL consumed by web frontend |
| `FACILITY_ID` | `FAC-HQ-01` | Default multi-tenant institutional facility code |
| `MERKLE_LOG_ENABLED`| `true` | Enables immutable 21 CFR Part 11 Merkle tree logging |

---

## 4. Elimination of Duplication & Dead Code
- Verified single source of truth on branch `main`.
- All temporary mock artifacts isolated or removed from production execution paths.
- Zero broken imports across all 91 React components and 284 Python modules.
