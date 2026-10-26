# ZAYVORA Health OS™ — Final Architecture

**Status: Pre-staging / Pilot Candidate**
**Version: 2.0.0**
**Last Updated: 2026-09-15**

## System Overview

ZAYVORA Health OS™ is a multi-tenant, microservice-based digital healthcare operating system
integrating classical Unani medicine with modern biomedical intelligence.

## Brand Hierarchy

| Brand | Role |
|:---|:---|
| ZAYVORA Health™ | Complete healthcare ecosystem |
| ZAYVORA Health OS™ | Digital healthcare operating system |
| ZAYVORA Matab™ | Clinician-led Unani care delivery |
| Hakeem Sahab AI™ | Clinical reasoning AI (safe_to_lock=False) |
| ZAYVORA Knowledge Intelligence™ | Knowledge, evidence, and safety governance |
| ZAYVORA Health Products™ | Standardised Unani, herbal, nutraceutical solutions |
| ZAYVORA Research & Manufacturing™ | Research, formulation, quality, production |

## Architecture Stack

```
┌─────────────────────────────────────────────────────────────────┐
│  ZAYVORA Health OS™  —  Web Frontend (Next.js 15 App Router)   │
│  118 routes · Design System v5.0 · Role-aware AppShell         │
├─────────────────────────────────────────────────────────────────┤
│                 API Gateway (FastAPI · Port 8000)               │
│          Path-prefix routing → downstream microservices         │
├──────────┬──────────┬──────────┬──────────┬────────────────────┤
│ Identity │ Clinical │Knowledge │Therapeutic│     AI Service     │
│  :8001   │  :8002   │  :8003   │   :8004   │      :8005         │
│ Auth/MFA │ Patient  │ ZKB/ZKI  │ Nuskha    │ Hakeem Sahab AI™  │
│ RBAC     │ Encounter│ Neo4j    │ Safety    │ Multimodal LLM    │
│ GDPR     │ eBMR     │ Evidence │ Herb DB   │ RAG pipeline      │
├──────────┴──────────┴──────────┴──────────┴────────────────────┤
│  PostgreSQL (zayvora DB)  │  Neo4j (ZKB)  │  Redis (cache)     │
│  pgvector extension       │  Knowledge    │  Session store     │
│  Schema-per-service       │  Graph        │  Queue             │
├──────────────────────────────────────────────────────────────────┤
│  HashiCorp Vault  │  Kubernetes / Helm v2.0.0  │  Prometheus    │
└─────────────────────────────────────────────────────────────────┘
```

## Microservice Ports

| Service | Port | Prefix | Technology |
|:---|:---|:---|:---|
| API Gateway | 8000 | / | FastAPI |
| Identity | 8001 | /api/v1/auth, /api/v1 | FastAPI + SQLAlchemy |
| Clinical | 8002 | /api/v1/clinical | FastAPI |
| Knowledge | 8003 | /api/v1/knowledge | FastAPI + Neo4j |
| Therapeutic | 8004 | /api/v1/therapeutic | FastAPI |
| AI | 8005 | /api/v1/multimodal | FastAPI |

## Safety Invariants (Non-negotiable)

1. `safe_to_lock=False` — All AI-assisted prescriptions; human sign-off mandatory
2. Schedule E(1) Mudabbar Gate — Toxic herbs blocked without purification cert
3. 21 CFR Part 11 — SHA-256 HMAC on all eBMR and prescription locks
4. No unsupported medical claims in any UI or documentation
