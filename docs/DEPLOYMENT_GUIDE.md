# ZAYVORA Health OS — Enterprise Deployment Guide
**Document ID**: `ZAY-OPS-001`  
**Classification**: DevOps & Infrastructure Standard  
**Date**: September 2026  

---

## 1. Deployment Architectures

ZAYVORA Health OS supports two primary deployment topologies:

### 1.1 Local Clinic / Standalone Server (Zero-Dependency)
Ideal for individual Matabs, specialized clinics, and off-grid healthcare facilities:
- **Backend**: Native Python 3 multi-threaded HTTP server (`services/live_api_server.py`)
- **Database**: SQLite persistent relational store (`database/zayvora_live.db`)
- **Frontend**: Node.js 18+ Next.js 16 App Router server (`apps/web`)

```bash
# Setup steps
python3 database/init_live_db.py
python3 services/live_api_server.py &
cd apps/web && npm install && npm run build && npm run start
```

### 1.2 Enterprise Hospital Cluster (Kubernetes / Cloud Native)
Designed for tertiary teaching hospitals, multi-center healthcare systems, and regional health authorities:
- **Service Mesh**: 5 microservices deployed via Helm chart (`infrastructure/helm/zayvora`)
- **Database**: High-Availability PostgreSQL 15 cluster with primary/replica streaming
- **Cache & Queue**: Redis 7 cluster for asynchronous tasks and ABDM pipelines
- **Gateway**: Traefik / NGINX reverse proxy with TLS termination and rate limiting

---

## 2. Environment Variables Configuration

| Variable Name | Default Value | Description |
|:---|:---|:---|
| `PORT` | `8000` | Port for the live REST API server |
| `DATABASE_PATH` | `database/zayvora_live.db` | Absolute or relative path to SQLite database |
| `JWT_SECRET` | System-generated random hex | 256-bit secret key for JWT session tokens |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | URL exposed to frontend browser clients |
| `FACILITY_ID` | `FAC-HQ-01` | Institutional facility code for multi-tenancy |
| `MERKLE_LOG_ENABLED` | `true` | Enables immutable block chaining in audit ledger |

