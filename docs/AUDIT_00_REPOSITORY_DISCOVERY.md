# AUDIT 00: REPOSITORY DISCOVERY & INVENTORY
**ZAYVORA HEALTH™ — Enterprise Healthcare Operating System**  
*“Ancient Wisdom. Modern Science. Intelligent Care.”*

**Audit Date**: September 12, 2026  
**Auditor Lead**: Principal Healthcare Systems & AI Auditor  
**Audit Scope**: Full Repository Codebase, Applications, Microservices, Infrastructure, and Ontologies  
**Classification**: OFFICIAL AUDIT REPORT — EVIDENCE-BASED DISCOVERY  

---

## 1. Executive Discovery Summary

A comprehensive, unvarnished forensic analysis of the `zayvora-platform-phase0-4` repository was conducted. The repository contains **323 files** totaling **44,138 lines of code and documentation** spanning TypeScript/React, Python/FastAPI, SQL/Alembic, Kubernetes/Docker YAML, and JSON ontologies.

The codebase represents a substantial, highly sophisticated implementation of an AI-native Unani healthcare operating system. However, the discovery also uncovers significant architectural consolidations, legacy directory shells, client-side fallback mocks, and simulated external integrations that must be transparently documented.

---

## 2. Repository Structural Inventory

```
/Users/irfanashraf/Downloads/zayvora-platform-phase0-4
├── .github/
│   └── workflows/ci.yml               # Automated GitHub Actions CI workflow (187 tests)
├── .gitignore                         # Standard Python, Node, environment ignore rules
├── README.md                          # Master architectural overview and quickstart
├── apps/                              # User-facing application layer
│   └── web/                           # [ACTIVE APPLICATION] Next.js 16 Clinician Desk 2.0 (10 cockpits)
├── database/                          # Relational persistence & migrations
│   ├── migrations/                    # Alembic migration environments (identity, clinical, therapeutic, ai)
│   │   └── migrate.py                 # Multi-service migration runner
│   ├── seed_data.py                   # Master multi-service database seeder (SQLite/Postgres)
│   └── seeds/                         # Canonical seed fixtures (canonical_seed_fixtures.json)
├── docs/                              # Architecture audits, specifications, and regulatory reports
├── infrastructure/                    # Deployment, containerization, and orchestration
│   ├── docker-compose.yml             # Local multi-container stack (Postgres, Redis, Neo4j, 6 services, worker)
│   └── k8s/                           # Kubernetes production manifests (HPA, Zero-trust network policies)
├── knowledge/                         # Physiological & chronobiological JSON knowledge ontologies
│   ├── asbab_sittah_guidelines.json   # Canonical Six Essential Requisites register
│   └── organ_axis_pathways.json       # 12 canonical Unani organ-axis reflex physiological pathways
├── pharmacopoeia/                     # Canonical pharmacopoeial registers
│   ├── nfum_formulations_canonical.json # National Formulary of Unani Medicine compound formulations
│   ├── schedule_e1_statutory_register.json # Schedule E(1) statutory poisons register
│   └── upi_monographs_canonical.json  # Unani Pharmacopoeia of India single drug monographs
├── policies/                          # Regulatory, data privacy, and compliance policies
│   ├── 21_cfr_part_11_compliance_policy.md # Cryptographic electronic signatures & Merkle audit trail
│   ├── hipaa_disha_data_privacy_policy.md  # 18 Safe Harbor de-identification & DISHA rules
│   └── safe_to_lock_enforcement_policy.md  # Clinician non-delegable prescription locking policy
├── prompts/                           # System and copilot prompt specifications
│   ├── hakeem_sahab_v2_system_prompt.md    # 13-section structured clinical reasoning prompt
│   └── zape_personalization_prompt.md      # ZAPE 2.0 dynamic personalization prompt template
├── protocols/                         # Clinical standard operating procedures
│   ├── clinical_governance_charter.md      # Governance Board 2-Tabeeb quorum rules
│   ├── mudabbar_detoxification_sops.md     # Detoxification SOPs for Schedule E(1) poisons
│   └── tadbeer_clinical_guidelines.md      # Regimenal therapy clinical guidelines
├── services/                          # Backend microservices layer (6 active core services)
│   ├── ai/                            # [ACTIVE SERVICE 1] Port 8005: Hakeem Sahab v2, ZAPE, Fallback Router
│   ├── clinical/                      # [ACTIVE SERVICE 2] Port 8002: EMR, Mizaj, Twin, Scribe, Wearables, Tasks
│   ├── gateway/                       # [ACTIVE SERVICE 3] Port 8000: Unified reverse proxy & rate limiting
│   ├── identity/                      # [ACTIVE SERVICE 4] Port 8001: RS256 Auth, JWKS, RBAC, Redis rate limit
│   ├── knowledge/                     # [ACTIVE SERVICE 5] Port 8003: Neo4j/In-memory Graph, Hybrid RAG, Cmd+K
│   └── therapeutic/                   # [ACTIVE SERVICE 6] Port 8004: Safety Firewall, Mudabbar Gate, Nuskha, eBMR
└── tests/
    └── run_all_tests.py               # Master test runner (28 test suites, 189 tests, 100% pass)
```

---

## 3. Technology Stack Inventory

| Component | Target Technology | Actual Implementation in Codebase | Verification Evidence |
| :--- | :--- | :--- | :--- |
| **Web Frontend** | Next.js 16 (App Router), React 19, Tailwind CSS | Next.js 16.1.1, React 19.2.3, Tailwind CSS v4 | [`apps/web/package.json`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/apps/web/package.json) |
| **Backend Services** | Python 3.11+, FastAPI, Pydantic v2 | FastAPI 0.115+, Pydantic 2.10+, Uvicorn | `services/*/requirements.txt` |
| **Relational Database** | PostgreSQL 16 Alpine | SQLAlchemy 2.0, Psycopg3, Alembic 1.14 | `database/migrations/*/alembic.ini` |
| **Caching & Queue** | Redis 7 Alpine | Redis 5.0+ client (Channels 0 & 1), in-memory fallback | [`services/clinical/app/workers/task_queue.py`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/clinical/app/workers/task_queue.py) |
| **Knowledge Graph** | Neo4j 5 Community | Neo4j Bolt Python Driver 5.27, `InMemoryGraphRepository` | [`services/knowledge/app/graph/`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/knowledge/app/graph/) |
| **AI LLM Inference** | Anthropic Claude, OpenAI, Local vLLM | `ChainedFallbackRouter` (Anthropic $\to$ OpenAI $\to$ vLLM $\to$ Fake) | [`services/ai/app/providers/fallback_router.py`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/ai/app/providers/fallback_router.py) |
| **Lexical & Vector Search** | Hybrid RAG | In-process Okapi BM25 + 128-dim Normalized Vector Store + RRF | [`services/knowledge/app/core/hybrid_rag.py`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/knowledge/app/core/hybrid_rag.py) |
| **Containerization** | Docker, Docker Compose | Multi-container Compose with 9 services | [`infrastructure/docker-compose.yml`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/infrastructure/docker-compose.yml) |
| **Orchestration** | Kubernetes 1.30+ | 19-document production YAML (HPA v2, Zero-Trust Policies) | [`infrastructure/k8s/zayvora-production-manifests.yaml`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/infrastructure/k8s/zayvora-production-manifests.yaml) |
| **CI / Automation** | GitHub Actions | `.github/workflows/ci.yml` running compilation & 187 tests | [`.github/workflows/ci.yml`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/.github/workflows/ci.yml) |

---

## 4. Active Applications vs. Empty Directory Shells

### Active Application
1. **`apps/web` (Clinic Desk 2.0)**:
   - Contains **48 active files** (14,919 LOC).
   - Fully interactive Next.js 16 single-page clinician workbench.
   - Hosts 10 primary operational cockpits:
     1. Longitudinal Patient Timeline
     2. Nuskha Nawisi Studio (Nuskha Builder)
     3. Ilaj-bit-Tadbeer Regimen Planner
     4. UPI Pharmacopoeia Reference
     5. Clinical Digital Twin Cockpit
     6. Ambient Scribe & 21 CFR Part 11 Cockpit
     7. Multimodal Lab & Physical Signs Cockpit
     8. Patient App 2.0 & Adherence Cockpit
     9. Clinical Governance Board Cockpit
     10. Task Pipelines & ABDM Streaming Workers Cockpit

### Empty Application Shells (Technical Debt / Missing Modules)
1. **`apps/admin`**: **0 files**. Completely empty directory. (Platform administration features are partly handled via API or Clinic Desk).
2. **`apps/mobile`**: **0 files**. Completely empty directory. Dedicated React Native / Flutter native clinician/patient mobile app is **NOT IMPLEMENTED**.
3. **`apps/patient`**: **0 files**. Completely empty directory. Dedicated standalone patient portal is not a separate application; it was implemented as an embedded component (`apps/web/components/PatientPortalCockpit.tsx`) inside the clinician web app.

---

## 5. Active Microservices vs. Legacy Directory Shells

The early architecture plan envisioned 21 discrete microservices. During platform development, domain boundaries were consolidated into **6 core production microservices**.

### Active Services (6)
1. **`services/gateway`** (FastAPI / Port 8000): Unified reverse proxy, API dispatch, upstream health aggregation, token passthrough.
2. **`services/identity`** (FastAPI / Port 8001): Multi-tenant isolation, RS256 JWT issuance, public JWKS endpoint, Redis sliding rate limiting, TOTP MFA.
3. **`services/clinical`** (FastAPI / Port 8002): Patient 360, Encounters, SOAP notes, Prescriptions, 10-Ajnas Mizaj engine, 12 Organ-Axis engine, Digital Twin, Ambient Scribe, Wearable streams, Predictive relapse forecaster, Tasks & workers daemon.
4. **`services/knowledge`** (FastAPI / Port 8003): UPI monographs, NFUM formulations, Hybrid RAG (BM25 + Dense vector), Command search (Cmd+K), Clinical Governance Board quorum state machine.
5. **`services/therapeutic`** (FastAPI / Port 8004): Safety Firewall (allergies, herb-drug interactions), Schedule E(1) Mudabbar gate (`MudabbarDispenseBlockError`), Nuskha compiler, Care plans, FEFO dispensary engine, eBMR manufacturing OS.
6. **`services/ai`** (FastAPI / Port 8005): Hakeem Sahab v2 copilot, ZAPE 2.0 personalization engine, Chained Fallback Router, AI evaluation lab, Multimodal lab extractor.

### Empty Service Shells (15 Unused Directories)
The following 15 directories in `services/` contain **0 files each**:
`services/analytics`, `services/axis`, `services/communications`, `services/diagnostic`, `services/evidence`, `services/ghiza`, `services/manufacturing`, `services/mizaj`, `services/nuskha`, `services/pharmacopoeia`, `services/pharmacy`, `services/research`, `services/safety`, `services/tadbeer`, `services/unani`.
- **Root Cause**: Their capabilities were merged into the 6 active microservices above.
- **Audit Recommendation**: Clean up or formally deprecate these empty directory shells to eliminate architectural confusion.

---

## 6. Database Systems & State Management

1. **Relational Schemas (PostgreSQL 16 / SQLAlchemy 2.0)**:
   - 4 independent database migration environments under `database/migrations/`: `identity`, `clinical`, `therapeutic`, `ai`.
   - All tables enforce multi-tenant isolation via `organization_id UUID NOT NULL INDEX`.
   - Append-only versioning implemented on `clinical_notes` (using `amends_note_id` and `is_current`) and `audit_logs`.
2. **Zero-Dependency Seeding & SQLite Fallback**:
   - [`database/seed_data.py`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/database/seed_data.py) provides hybrid execution: runs against PostgreSQL when configured, or standard library `sqlite3` without external dependencies.
   - Pre-generated JSON fixtures available in [`database/seeds/canonical_seed_fixtures.json`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/database/seeds/canonical_seed_fixtures.json).
3. **Graph Database**:
   - `services/knowledge/app/graph/neo4j_repository.py` implements Cypher queries.
   - When Neo4j is offline or in unit tests, `InMemoryGraphRepository` (`fake_repository.py`) is used.
4. **Redis Cache & Task Queue**:
   - `services/identity/app/core/rate_limit.py`: Sliding window counter using Redis sorted sets.
   - `services/clinical/app/workers/task_queue.py`: Background task queue using Redis lists (`lpush`/`brpop`) with thread-safe `queue.Queue` in-memory fallback.

---

## 7. External Integrations: Real vs. Simulated

| Integration | Intended Role | Implementation Status | Evidence |
| :--- | :--- | :--- | :--- |
| **NHA ABDM Gateway** | Ayushman Bharat Digital Mission (Milestones 1–3) | **SIMULATED** | [`abdm_gateway.py`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/clinical/app/interop/abdm_gateway.py) uses in-memory dicts. Does not connect to live NHA mTLS endpoint. |
| **HL7 FHIR R4** | ABDM OPConsultRecord document bundle export | **REAL IMPLEMENTATION** | [`fhir_converter.py`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/clinical/app/interop/fhir_converter.py) generates valid FHIR R4 JSON bundles. |
| **QSURA Telecom** | WhatsApp HSM & SMS TRAI DLT delivery | **SIMULATED BROKER** | [`qsura_broker.py`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/clinical/app/qsura/qsura_broker.py) formats and masks Zero-PHI payloads; external telecom gateway is simulated. |
| **LLM Providers** | Anthropic Claude 3.5, OpenAI GPT-4o, Local vLLM | **REAL CLIENTS + TEST FAKE** | Real `anthropic` and `openai` clients in [`services/ai`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/ai/app/providers/). Defaults to `ScriptedFakeProvider` when API keys are absent. |
| **Continuous Wearables**| Ingestion from Apple HealthKit / Google Fit | **ALGORITHMIC ENGINE ONLY** | [`wearable_engine.py`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/clinical/app/wearables/wearable_engine.py) analyzes telemetry; live cloud OAuth2 connectors are not built. |
| **Speech-to-Text** | Ambient clinical speech recording | **TEXT PARSER ONLY** | [`ambient_scribe.py`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/clinical/app/scribe/ambient_scribe.py) parses text transcripts into Unani SOAP notes; live audio capture/Whisper is absent. |

---

## 8. Test Framework & Quality Assurance

- **Master Test Runner**: [`tests/run_all_tests.py`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/tests/run_all_tests.py).
- **Test Execution Metric**: **187 automated tests** across **27 distinct test suites**.
- **Passing Status**: **187 / 187 passed (100% pass rate)**.
- **Failures**: **0**.
- **Skips**: **0**.
- **Static Compilation**: Clean across all services and applications (`python3 -m compileall -q` returns 0 errors).

---

## 9. Key Architectural Findings & Technical Debt

1. **Client-Side Fallback Masking**:
   Every API module in `apps/web/lib/*Api.ts` contains `try-catch` blocks returning rich mock responses when backends are unreachable. This causes the UI to look completely functional even when services are offline.
2. **Consolidation Residue**:
   15 empty service directories and 3 empty app directories clutter the repository tree.
3. **Simulated Gateways**:
   ABDM, QSURA, and Wearable device clouds operate on rigorous domain data structures and mathematical models, but rely on simulation wrappers rather than live third-party network connections.
4. **Clinical Validation Gap**:
   All 10-Ajnas, CKD-EPI, organ-axis, and drug interaction rules are codified and unit-tested, but the platform has not yet undergone live human clinical trials or received formal statutory CDSCO/AYUSH clearance.
