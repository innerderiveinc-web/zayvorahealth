# ZAYVORA Health OS — Backend Services & Subsystem Architecture

This directory houses the backend business logic, clinical engines, domain micro-routers, and runtime profiles for **ZAYVORA Health OS (V5.0.0-Enterprise)**.

---

## 🏛️ Dual-Runtime Architectural Topology

To satisfy both **Edge-First Offline Clinics** (single-doctor practices, remote field hospitals without reliable internet or cloud infrastructure) and **Cloud-Scale Enterprise Hospitals** (multi-tenant health systems with millions of records), ZAYVORA employs a **Dual-Profile Packaging Architecture**:

```
                                  ┌─────────────────────────────┐
                                  │   ZAYVORA Health OS Client   │
                                  │  (Web / PWA / Mobile / API) │
                                  └──────────────┬──────────────┘
                                                 │
                                                 ▼
                        ┌─────────────────────────────────────────────────┐
                        │              HTTP Request Ingestion             │
                        └────────┬───────────────────────────────┬────────┘
                                 │                               │
                [PROFILE: MONOLITH (Default)]         [PROFILE: DISTRIBUTED]
                                 │                               │
                                 ▼                               ▼
                     ┌───────────────────────┐       ┌───────────────────────┐
                     │  live_api_server.py   │       │   API Gateway Proxy   │
                     │  (Standard HTTP Core) │       │   (services/gateway)  │
                     └───────────┬───────────┘       └───────────┬───────────┘
                                 │                               │
                                 ▼                               ▼
                     ┌───────────────────────┐       ┌───────────────────────┐
                     │   12 Domain Routers   │       │  6 FastAPI Containers │
                     │   (services/routes/)  │       │  (Clinical, Identity, │
                     └───────────┬───────────┘       │   Therapeutic, AI...) │
                                 │                   └───────────┬───────────┘
                                 ▼                               │
                     ┌───────────────────────┐                   │
                     │  engine_registry.py   │◄──────────────────┘
                     │  (In-Memory Engine    │   (Shared Domain Engines)
                     │       Facade)         │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Core Domain Engines   │
                     │  - agentic_core.py    │
                     │  - auth_core.py       │
                     │  - prescription_core  │
                     │  - patient_core.py    │
                     └───────────────────────┘
```

---

## 📂 Subsystem Directory Layout

### 1. Unified Dispatcher & Cores
- **`live_api_server.py`**: Ultra-lean, zero-dependency standard-library HTTP dispatcher (1,074 lines) supporting both standalone execution and containerized deployment.
- **`agentic_core.py`**: Pure domain implementation for the 8 autonomous clinical and research AI agents (Hakeem Case Brief, Autonomous Scribe, Dynamic Triage, etc.).
- **`auth_core.py`**: 21 CFR Part 11 compliant cryptographic authentication, token minting, Argon2/PBKDF2 password hashing, and OTP validation.
- **`prescription_core.py`**: Invariant safety engine for Unani prescriptions, posology thresholds, drug-drug interaction matrix, and printable slips.
- **`patient_core.py`**: AES-256-GCM authenticated encryption for PHI, Patient 360 master data graph, and audit records.
- **`engine_registry.py`**: Microservice facade that dynamically loads domain algorithms in-process with graceful fallback handling.
- **`ai_provider_chain.py`**: Multi-tier chained failover LLM provider (Ollama -> Anthropic -> OpenAI -> Deterministic Local Rule Engine).

### 2. Domain Micro-Routers (`services/routes/`)
1. **`agentic_routes.py`**: Autonomous clinical AI copilot, case briefs, scribe, and triage endpoints.
2. **`auth_routes.py`**: Login, registration, token refresh, OTP dispatch, and RBAC authorization.
3. **`pharmacy_routes.py`**: Classical formulation monographs (UPI Part 2 Vol 4), classical weights converter, and FEFO inventory.
4. **`clinical_routes.py`**: 12-Organ Axis, Qaroorah, Baraaz, and Asbab-e-Sittah scoring engines.
5. **`computational_routes.py`**: Canonical Identity substances, molecular twins, evidence matrices, and ZFIE endpoints.
6. **`telemedicine_routes.py`**: Appointments booking, live queue transitions, QSURA video sessions, and WebRTC signaling.
7. **`patient_routes.py`**: Patient directory, encrypted demographics, Patient 360 view, and EHR timeline.
8. **`encounter_routes.py`**: Encounters lifecycle, Merkle hash seals, Hakeem copilot, and Deep RAG.
9. **`billing_prescription_routes.py`**: Prescriptions authoring, barcode-verified dispensing, and billing invoices.
10. **`diagnostics_operations_routes.py`**: Tasks queue, care plans, lab diagnostics, facilities, and immutable audit ledger.
11. **`continuum_trials_routes.py`**: Doctor continuum, pragmatic clinical trials OS, and digital twin cohorts.
12. **`governance_protocols_routes.py`**: 12-Gate clinical governance, treatment regimens, CDSS protocols, and Tadbeer-e-Adviyah SOPs.

### 3. Distributed Microservice Containers
The directories below contain individual microservices equipped with their own `Dockerfile`, Alembic migrations, and FastAPI routers for distributed Kubernetes deployments:
- **`clinical/`**: Electronic Health Records, clinical continuum, encounter management.
- **`therapeutic/`**: Posology calculation, formulary inventory, compounding, eBMR manufacturing.
- **`identity/`**: OAuth2/OIDC provider, federated identity, biometric credentials.
- **`knowledge/`**: Classical Unani pharmacopoeia, UPI monographs, Kulliyat-e-Adwiyah corpus.
- **`ai/`**: Heavy multimodal AI models, RAG vector index, biomedical embeddings.
- **`gateway/`**: High-throughput reverse-proxy API Gateway for distributed deployments.

---

## ⚙️ Runtime Profile Configuration

Set the environment variable `ZAYVORA_RUNTIME_PROFILE` to select the operational mode:

```bash
# Modular Monolith Profile (Default - recommended for clinics, offline nodes, standalone servers)
export ZAYVORA_RUNTIME_PROFILE=monolith
python3 services/live_api_server.py

# Distributed Microservices Profile (For cloud Kubernetes clusters)
export ZAYVORA_RUNTIME_PROFILE=distributed
docker compose up -d
# or: helm install zayvora infrastructure/helm/zayvora
```
