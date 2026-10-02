# ZAYVORA Health OS™ — ARCHITECTURE SOURCE OF TRUTH
**Document ID:** ZAY-ARCH-SOT-001  
**Version:** Phase 0 Baseline  
**Date:** September 15, 2026  
**Status:** AUTHORITATIVE — Do not modify without Engineering Lead sign-off

---

## 1. System Topology

```
┌──────────────────────────────────────────────────────────────────────┐
│                    ZAYVORA Health OS™ Platform                       │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                     Public Clients                          │    │
│  │  Browser (Next.js 14)    Mobile (Expo ~51 / RN 0.74.5)    │    │
│  └────────────────────────┬────────────────────────────────────┘    │
│                           │ HTTPS                                   │
│  ┌────────────────────────▼────────────────────────────────────┐    │
│  │           API Gateway  (FastAPI, port 8000)                 │    │
│  │  Rate Limiting · CORS · JWT Verification · Path Routing     │    │
│  └──┬─────────────┬──────────────┬──────────────┬─────────────┘    │
│     │             │              │              │                   │
│  ┌──▼──┐  ┌──────▼────┐  ┌─────▼──────┐  ┌──▼─────────────────┐  │
│  │ ID  │  │ Clinical  │  │ Knowledge  │  │ Therapeutic         │  │
│  │:8001│  │  :8002    │  │  :8003     │  │  :8004              │  │
│  │     │  │           │  │            │  │                     │  │
│  │Auth │  │20+ Routers│  │Neo4j Graph │  │7 Engines            │  │
│  │RBAC │  │5 Engines  │  │RAG Pipeline│  │Nuskha Compiler      │  │
│  │MFA  │  │Digital    │  │UPI Monogr. │  │Safety Firewall      │  │
│  │JWKS │  │Twin       │  │FHIR/ABDM   │  │Dispensary FEFO      │  │
│  └──┬──┘  └──────┬────┘  └─────┬──────┘  └──┬─────────────────┘  │
│     │             │              │             │                   │
│  ┌──▼─────────────▼──────────────▼─────────────▼──────────────┐    │
│  │         AI Service  (FastAPI, port 8005)                    │    │
│  │  Hakeem Sahab AI™ · ZAPE · Multimodal · Red-team Security   │    │
│  └──────────────────────────┬───────────────────────────────────┘  │
│                             │                                       │
│  ┌──────────────────────────▼───────────────────────────────────┐  │
│  │                  Persistence Layer                            │  │
│  │  PostgreSQL 16 (single DB, schema-isolated per service)      │  │
│  │  Neo4j 5 (knowledge graph, bolt://neo4j:7687)                │  │
│  │  Redis 7 (sessions, rate limiting, OpenFDA cache)            │  │
│  └───────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Service Contracts

| Service | Port | Framework | DB | Auth | Key Responsibility |
|---|---|---|---|---|---|
| **gateway** | 8000 | FastAPI | — | Validates JWT | Reverse proxy, rate limit, CORS |
| **identity** | 8001 | FastAPI | PostgreSQL | Issues JWT | Auth, RBAC, MFA, tenancy |
| **clinical** | 8002 | FastAPI | PostgreSQL | JWT required | Encounters, patients, EHR, engines |
| **knowledge** | 8003 | FastAPI | Neo4j | JWT required | Unani KG, RAG, UPI, pharmacopoeia |
| **therapeutic** | 8004 | FastAPI | PostgreSQL | JWT required | Prescriptions, dispensary, safety |
| **ai** | 8005 | FastAPI | PostgreSQL | JWT required | Hakeem Sahab AI™, ZAPE, multimodal |

---

## 3. Data Model Summary

### PostgreSQL Tables (36 total across 4 schemas)

**identity schema:**
- `organizations` — multi-tenant root
- `users` — UUID PK, bcrypt hash, org FK, role FK
- `roles` — role definitions
- `permissions` — permission catalogue
- `role_permissions` — M2M
- `audit_logs` — immutable event log

**clinical schema:**
- `patients` — PHI, Mizaj baseline, allergies, AES-GCM encrypted fields
- `encounters` — lifecycle state machine
- `clinical_notes` — versioned, cryptographically locked
- `vitals` — timestamped measurements
- `lab_results` — FHIR-aligned
- `appointments` — scheduling
- `digital_twins` — patient digital model
- `audit_merkle_blocks` — Merkle chain

**therapeutic schema:**
- `nuskhaat` — prescriptions
- `nuskha_items` — prescription line items
- `inventory` — herb/compound stock (FEFO)
- `care_plans` — structured plans
- `dispensary_logs` — dispense records

**ai schema:**
- `ai_sessions` — Hakeem conversation sessions
- `ai_recommendations` — advisory records with citations

### Neo4j Graph (knowledge service)
- Nodes: `Herb`, `Compound`, `Disease`, `Mizaj`, `OrganAxis`, `Formula`, `Evidence`
- Relationships: `TREATS`, `CONTAINS`, `CONTRAINDICATED_FOR`, `DERIVED_FROM`, `CLASSIFIED_AS`

---

## 4. Authentication Flow

```
1. POST /api/v1/auth/login → identity:8001
2. Returns: { access_token (15m), refresh_token (7d), user, role }
3. All subsequent requests: Authorization: Bearer <access_token>
4. Gateway verifies JWT signature using JWKS from identity service
5. On 401: POST /api/v1/auth/refresh → new access_token
6. Clinical MFA path: POST /api/v1/auth/mfa/verify (TOTP) → clinical token
```

---

## 5. Brand Hierarchy (Canonical Names)

| Brand Entity | Canonical Name | Usage |
|---|---|---|
| Master brand | **ZAYVORA Health™** | All public-facing contexts |
| Digital OS | **ZAYVORA Health OS™** | Platform/product references |
| Clinic brand | **ZAYVORA Matab™** | Clinician workspace, appointment booking |
| AI Copilot | **Hakeem Sahab AI™** | All AI advisory UI elements |
| Knowledge layer | **ZAYVORA Knowledge Intelligence™** | Knowledge/RAG UI, docs |
| Products | **ZAYVORA Health Products™** | Product catalog, pharmacy |
| R&D | **ZAYVORA Research & Manufacturing™** | Research/manufacturing portals |

> ⚠️ All existing UI references to bare "Hakeem Sahab", "Knowledge Service", "Clinical AI" must be updated to canonical brand names above during Phase 1.

---

## 6. Infrastructure

| Component | Tool | Config File |
|---|---|---|
| Local dev orchestration | Docker Compose | `docker-compose.yml` (5269 bytes) |
| Dev overrides (hot reload + tools) | Docker Compose override | `docker-compose.override.yml` |
| Production Kubernetes | Helm | `infrastructure/helm/zayvora/` |
| CI/CD | GitHub Actions | `.github/workflows/ci.yml`, `release.yml` |
| DB migrations | Alembic | `services/{service}/migrations/` |
| Secrets management | `.env` / K8s Secrets | `.env.example` (40+ vars) |

---

## 7. External Integrations Status

| Integration | Client File | Status |
|---|---|---|
| FHIR R4 + SMART OAuth2 | `clinical/app/integrations/fhir_client.py` | ✅ Client implemented |
| OpenFDA (drug search) | `therapeutic/app/integrations/openfda_client.py` | ✅ Client + Redis cache |
| Stripe (subscriptions) | `identity/app/integrations/stripe_client.py` | ✅ Client implemented |
| Twilio SMS | `identity/app/integrations/notifications_client.py` | ✅ Client implemented |
| SendGrid Email | Same as above | ✅ Client implemented |
| Qdrant Vector Store | `ai/app/integrations/vector_store.py` | ✅ Client implemented |
| ABDM (Indian health stack) | `clinical/app/interop/` | 🟡 Framework exists, credentials needed |
| Google Gemini / LLM | `ai/app/providers/` | 🟡 Provider abstraction exists |
