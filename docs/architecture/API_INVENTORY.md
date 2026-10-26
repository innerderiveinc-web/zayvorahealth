# ZAYVORA Health OS — Comprehensive API Inventory & Service Contracts
**Document ID**: `ZAY-AUD-003`  
**Classification**: Technical Architecture Standard  
**Date**: September 2026  
**Status**: AUDITED & OPERATIONAL  

---

## 1. Overview & Dual-Backend Architecture

ZAYVORA Health OS employs a robust dual-backend strategy:

1. **Live REST API Server (`services/live_api_server.py`)**:
   - Zero-dependency, multi-threaded native Python HTTP server listening on port `8000`.
   - Directly backed by `database/zayvora_live.db` (SQLite relational database).
   - Serves critical live production endpoints for authentication, patient registry, appointment booking, prescription authorship with 21 CFR Part 11 signatures, FEFO dispensary management, and Merkle audit logging.
   - Cross-Origin Resource Sharing (CORS) configured for `http://localhost:3000` and all local frontend origins.

2. **Microservice API Fleet (`services/*`)**:
   - 5 domain microservices (Clinical, Therapeutic, Knowledge, AI, Identity) encompassing 42 FastAPI routers and 158 endpoints.
   - Built with Pydantic v2 schemas and SQLAlchemy ORM models for large-scale enterprise deployments.

---

## 2. Live REST API Server Endpoints (`services/live_api_server.py`)

| Method | Route | Description | Auth / Role | DB Tables Involved | Request Payload | Response Schema |
|:---|:---|:---|:---|:---|:---|:---|
| `GET` | `/api/health` | System liveness probe & DB status | Public | `users` (COUNT) | None | `{"ok": true, "database": "connected", "registered_users": int}` |
| `POST` | `/api/v1/auth/register` | Register new user & patient | Public | `users`, `patients` | `{"email", "password", "fullName", "phone", "role"}` | `{"ok": true, "token": str, "user": {...}}` (201 Created) |
| `POST` | `/api/v1/auth/login` | Authenticate user credentials | Public | `users` | `{"email", "password"}` | `{"ok": true, "token": str, "user": {...}}` |
| `GET` | `/api/v1/patients` | List all registered patients | Bearer Token | `patients` | None | `{"ok": true, "count": int, "patients": [...]}` |
| `GET` | `/api/v1/patients/{id}` | Get patient details by ID or MRN | Bearer Token | `patients` | None | `{"ok": true, "patient": {...}}` |
| `POST` | `/api/v1/patients` | Register new patient directly | Staff | `patients` | `{"firstName", "lastName", "dob", "gender", "phone", "mizaj"}` | `{"ok": true, "patient": {...}}` (201 Created) |
| `GET` | `/api/v1/appointments` | List today OPD queue | Bearer Token | `appointments` | None | `{"ok": true, "count": int, "appointments": [...]}` |
| `POST` | `/api/v1/appointments` | Book appointment & issue token | Public / Staff | `appointments` | `{"patientName", "mrn", "doctorName", "date", "timeSlot"}` | `{"ok": true, "appointment": {...}}` (201 Created) |
| `PATCH`| `/api/v1/appointments/{id}/status` | Update consultation status | Staff | `appointments` | `{"status": "IN_CONSULTATION"}` | `{"ok": true, "message": str}` |
| `GET` | `/api/v1/prescriptions` | List clinical prescriptions | Clinician / Staff | `prescriptions` | None | `{"ok": true, "count": int, "prescriptions": [...]}` |
| `POST` | `/api/v1/prescriptions` | Author & cryptographically lock Rx | Doctor | `prescriptions`, `audit_ledger` | `{"patientName", "mrn", "doctorName", "items", "diet"}` | `{"ok": true, "orderNumber": str, "signatureHash": str}` (201) |
| `GET` | `/api/v1/inventory` | List dispensary inventory (FEFO) | Pharmacist | `inventory` | None | `{"ok": true, "count": int, "inventory": [...]}` |
| `POST` | `/api/v1/inventory/dispense` | Dispense medicine & deduct stock | Pharmacist | `inventory` | `{"batchNumber": str, "quantity": int}` | `{"ok": true, "remainingStock": int}` |
| `GET` | `/api/v1/audit/logs` | Inspect Merkle audit trail | Admin | `audit_ledger` | None | `{"ok": true, "count": int, "audit_logs": [...]}` |

---

## 3. Microservice Endpoints Overview (158 Endpoints across 42 Routers)

### 3.1 Clinical Service (`services/clinical` — 81 Endpoints)
- **Patients & Encounters**: `/api/v1/patients/*`, `/api/v1/encounters/*`, `/api/v1/clinical_notes/*`
- **Mizaj & Diagnostics**: `/api/v1/mizaj/assess`, `/api/v1/mizaj/history`, `/api/v1/afaal/analyze`
- **Physiological Twins**: `/api/v1/digital_twin/trajectory`, `/api/v1/timeline/events`
- **Clinical Governance**: `/api/v1/governance/dsbm`, `/api/v1/governance/concordance`
- **Ambient Scribe**: `/api/v1/scribe/transcribe`, `/api/v1/scribe/soap_generate`
- **Wearables & Predictive**: `/api/v1/wearables/stream`, `/api/v1/predictive/relapse_risk`
- **Interoperability & ABDM**: `/api/v1/interop/fhir/bundle`, `/api/v1/interop/abdm/m1_link`
- **Communication & Billing**: `/api/v1/qsura/send`, `/api/v1/payments/checkout`, `/api/v1/payments/webhook`
- **Background Workers**: `/api/v1/tasks/dispatch`, `/api/v1/cron/scanners`

### 3.2 Therapeutic Service (`services/therapeutic` — 24 Endpoints)
- **Nuskha Formulation**: `/api/v1/nuskha/compile`, `/api/v1/nuskha/validate_posology`, `/api/v1/nuskha/lock`
- **Dispensary & Inventory**: `/api/v1/dispensary/fefo_pick`, `/api/v1/dispensary/mudabbar_verify`
- **Regimenal & Dietetics**: `/api/v1/tadbeer/protocols`, `/api/v1/ghiza/parhez_plan`
- **Care Plans & Safety**: `/api/v1/care_plans/build`, `/api/v1/pharmacovigilance/adr_report`
- **Logistics & Shipments**: `/api/v1/logistics/courier_dispatch`, `/api/v1/logistics/tracking`

### 3.3 Knowledge Service (`services/knowledge` — 30 Endpoints)
- **Mufradat Taxonomy**: `/api/v1/mufradat/catalog`, `/api/v1/mufradat/lookup/{name}`
- **Pharmacopoeia Registry**: `/api/v1/pharmacopoeia/formulas`, `/api/v1/pharmacopoeia/schedule_e1`
- **Knowledge Graph**: `/api/v1/graph/traverse`, `/api/v1/graph/triples`
- **RAG & Search**: `/api/v1/rag/retrieve`, `/api/v1/search/command_k`
- **Evidence & Governance**: `/api/v1/evidence/citations`, `/api/v1/governance_board/quorum`

### 3.4 AI Service (`services/ai` — 15 Endpoints)
- **Hakeem Sahab Assistant**: `/api/v1/hakeem/consult`, `/api/v1/hakeem/differential`
- **AI Safety & Firewall**: `/api/v1/security/guardrail_check`, `/api/v1/security/sanitization`
- **Multimodal Clinical Labs**: `/api/v1/multimodal/ocr_lab_report`, `/api/v1/multimodal/physical_signs`
- **Evaluation Lab**: `/api/v1/evaluation/benchmark`, `/api/v1/evaluation/hallucination_score`

### 3.5 Identity Service (`services/identity` — 8 Endpoints)
- **Authentication**: `/api/v1/auth/token`, `/api/v1/auth/refresh`, `/api/v1/auth/mfa`
- **Tenancy & RBAC**: `/api/v1/tenancy/organizations`, `/api/v1/tenancy/roles`, `/api/v1/tenancy/users`

---

## 4. Client Integration & Frontend Connectivity Status

- **Web Client API Bridge**: `apps/web/lib/services/apiClient.ts` handles communication with `http://localhost:8000`.
- **Authentication Service**: `apps/web/lib/services/authService.ts` implements `loginAsync` and `registerAsync` connected directly to the live server.
- **Appointment Service**: `apps/web/lib/services/appointmentService.ts` submits live booking requests and retrieves OPD queues.
- **Graceful Offline Fallback**: If the live backend is temporarily unreachable, client services fall back to verified offline mock state without crashing or freezing.

