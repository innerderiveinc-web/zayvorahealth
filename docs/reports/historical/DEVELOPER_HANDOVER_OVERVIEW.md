# ZAYVORA Health OS™ — Complete Engineering & Architectural Overview
**Document Version:** 5.0.0-Enterprise | **Target Audience:** Engineering Team, Tech Leads, Healthcare Software Architects  
**Official Production Domain:** `https://www.zayvorahealth.com` | **Clinical Intranet:** `https://app.zayvorahealth.com`  
**Repository Location:** `/Users/irfanashraf/Downloads/zayvora-platform-phase0-4`  
**Audit Verification:** 940 / 940 Automated Tests Passed (100% Green, 0 Failures)

---

## 1. Executive Summary & System Philosophy

**ZAYVORA Health OS™** is an enterprise-grade, clinical operating system and patient discovery ecosystem designed to codify, standardize, and scale **Classical Unani Medicine (Tibb-e-Unani)** using modern biomedical informatics, rigorous regulatory safety firewalls, and AI-assisted clinical decision support.

### Key Tenets:
1. **Clinician-in-the-Loop Governance:** AI suggestions (*Hakeem Sahab AI Copilot*) are strictly advisory and non-delegable. Prescriptions require licensed practitioner cryptographic ratification (21 CFR Part 11).
2. **Two-Door Domain Isolation:** 
   - Public Discovery Front-Door: `www.zayvorahealth.com`
   - Clinical Intranet (Hospital OS): `app.zayvorahealth.com` (Zero unauthenticated access, zero search engine indexing).
3. **Evidence-Based Unani Pharmacopoeia:** Codified 336+ UPI (Unani Pharmacopoeia of India) & NFUM monographs, 62 compound Murakkabat, 12-Axis Mizaj Radar, and Schedule E(1) Mudabbar detoxification safety gates.

---

## 2. High-Level Architectural Topology

```
                                  ┌──────────────────────────────────────────────┐
                                  │      ZAYVORA PLATFORM (Unified Monorepo)     │
                                  └──────────────────────┬───────────────────────┘
                                                         │
                        ┌────────────────────────────────┴────────────────────────────────┐
                        ▼                                                                 ▼
           ┌─────────────────────────┐                                       ┌─────────────────────────┐
           │   PUBLIC FRONT-DOOR     │                                       │   ZAYVORA HEALTH OS     │
           │ (www.zayvorahealth.com) │                                       │ (app.zayvorahealth.com) │
           └────────────┬────────────┘                                       └────────────┬────────────┘
                        │                                                                 │
         ┌──────────────┴──────────────┐                                    ┌─────────────┴─────────────┐
         ▼                             ▼                                    ▼                           ▼
  [Patient Portal]           [Staff Gateway]                        [Doctor Clinical Desk]     [Pharmacy & FEFO]
  (Mareez Dashboard)         (Clinician MFA Login)                  [Admin IT Console]         [EMR / Records]
                                                                                  │                           │
                                                                                  └─────────────┬─────────────┘
                                                                                                ▼
                                                                                     [ STRICT SECURITY GATE ]
                                                                                     - Unauthenticated Visitors Blocked
                                                                                     - X-Robots-Tag: noindex, nofollow
                                                                                     - RFC 9309 Crawler Exclusion
```

---

## 3. Technology Stack & Directory Structure

| Layer | Technologies Used | Purpose |
| :--- | :--- | :--- |
| **Frontend Platform** | Next.js 15 (App Router), React 19, TypeScript, TailwindCSS | High-performance responsive web application, interactive clinical cockpits. |
| **Subdomain Middleware** | Next.js Edge Middleware (`apps/web/middleware.ts`) | Subdomain detection (`app.*`, `os.*`), security headers, robots protection. |
| **Backend Microservices** | FastAPI, Starlette, Uvicorn, Python 3.9+ | High-throughput async REST microservices, clinical engines, FHIR serializers. |
| **Unified Live Server** | Python 3 HTTP Server (`services/live_api_server.py`) | Zero-dependency standalone REST backend & multi-facility SQLite/Postgres bridge. |
| **Databases & Caches** | SQLite (Live Local), PostgreSQL (Production), Redis, Neo4j, Qdrant | Relational EMR storage, session locks, Unani Knowledge Graph, Vector RAG. |
| **Audit & Signatures** | NIST SP 800-63B PBKDF2-HMAC-SHA256, Merkle Hash Trees | 21 CFR Part 11 compliant digital signatures and immutable audit trails. |

### Repository Structure:
```
zayvora-platform-phase0-4/
├── apps/
│   └── web/                         # Next.js 15 Full-Stack Web Application
│       ├── app/                     # App Router: /doctor, /patient, /pharmacy, /admin, /book, etc.
│       ├── components/              # Design System: PublicHeader, PlatformHeader, AppShell, etc.
│       ├── lib/                     # Client APIs, Session Store, SEO metadata, SiteConfig
│       ├── middleware.ts            # Subdomain Router & Crawler Shield Middleware
│       └── public/robots.txt        # RFC 9309 Private Intranet Crawler Barrier
├── services/                        # Backend Microservices & Clinical Engines
│   ├── identity/                    # Authentication, RBAC, TOTP MFA, NIST Password Hashing
│   ├── clinical/                    # Encounter Engine, SOAP Notes, 12-Axis Mizaj, ABDM FHIR
│   ├── therapeutic/                 # 4-Tier Nuskha Nawisi, Drug-Herb Checker, FEFO Inventory
│   ├── knowledge/                   # Pharmacopoeia (UPI), Neo4j Graph, Hybrid RAG, Bio-BERT
│   ├── ai/                          # Hakeem Sahab AI Copilot v2, Prompt Guardrails, DAK Level 3
│   ├── gateway/                     # Reverse Proxy & API Gateway (Port 8000)
│   └── live_api_server.py           # Unified Production REST API Server & SQLite/Postgres Bridge
├── database/                        # Database Provisioning Scripts & Seed Data
│   └── zayvora_live.db              # Active SQLite Ledger (9 Patients, 9 Batches, 44 Audits)
├── dist/                            # Production Distribution Archives
│   ├── zayvora-health-os-full.zip   # Clean production bundle (13.79 MB)
│   └── zayvora-health-os-complete-with-git.zip # Full bundle with Git history (34.38 MB)
├── scripts/
│   ├── launch_zayvora_os.py         # Production Web & API Server Launcher (Port 8080)
│   └── verify_live_stack.py         # 9-Pillar Master Verification Suite
├── tests/                           # Master Automated Test Suite
│   └── run_all_tests.py             # Master Test Runner (940/940 Tests Passing)
└── launch.sh                        # One-Click Unified Local & Server Startup Script
```

---

## 4. The 9 Core Architectural Pillars

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ZAYVORA HEALTH OS™ — 9-PILLAR DOCTRINE                          │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. 350-Drug Materia Medica │ 2. 50+ Classical Compounds │ 3. Sehat Sahab & Parhez      │
│    UPI monographs, 12-Axis │    Schedule E(1) Mudabbar  │    14-Day PROMs, 8-Tier Diet │
│    Constitutional Radar    │    Detoxification Gate     │    Patient Health 360 App    │
├────────────────────────────┼────────────────────────────┼──────────────────────────────┤
│ 4. Knowledge Graph & RAG   │ 5. Clinical Continuum      │ 6. ABDM FHIR Federation      │
│    Neo4j Graph (386 nodes) │    WHO SMART DAK Level 3/4 │    M1/M2/M3 HIP Envelope     │
│    Hakeem Copilot v2       │    21 CFR Part 11 Merkle   │    4-Facility Stock Balance  │
├────────────────────────────┼────────────────────────────┼──────────────────────────────┤
│ 7. Adaptive Precision Med  │ 8. Digital Biomarkers      │ 9. Clinical Trial OS & RWE   │
│    Phenotypic Subtyping    │    Single-Subject N-of-1   │    Federated Learning, Twin  │
│    Adherent-Non-Responder  │    Bayesian Response Est.  │    Global Crosswalk (WHO/FDA)│
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

---

## 5. Security, Compliance & Invariant Enforcement

1. **21 CFR Part 11 Digital Signatures:**
   - Every locked prescription receives a cryptographic signature containing: Signer Name, Medical Council Reg No, UTC Timestamp, and SHA-256 Merkle leaf hash.
   - Any tampering with prescription parameters invalidates the chain.

2. **Schedule E(1) Mudabbar Detoxification Gate:**
   - Classical potent botanicals (e.g. *Suranjan Talkh / Colchicum autumnale*, *Aconitum napellus*) cannot be dispensed unless linked to a validated Mudabbar Certificate Hash (`CERT-E1-MUDABBAR-SHA256-VALIDATED`).
   - Raw/unpurified batches are hard-locked by the inventory state machine.

3. **FEFO (First-Expiry-First-Out) Automated Batch Allocation:**
   - Dispensary stock allocations automatically select the earliest expiring compliant lot. Expired batches (`RB-2024-EXP`) are quarantined immediately.

4. **Zero Unauthenticated Access on Clinical OS:**
   - Visiting `/doctor`, `/pharmacy`, `/admin`, `/patient` without a session renders the **ZAYVORA Health OS — Clinician & Staff Gateway** modal. Direct access to charts or records is cryptographically impossible without a valid token.

5. **Hardware Integration Transparency:**
   - Standard invariant: UI displays **`Hardware Integration Architecture`** and **`Connected Devices: 0`** until physical telemetry nodes are clinically paired and verified. No mock telemetry is rendered as "Live".

---

## 6. API Reference & Key Endpoints

| Endpoint | Method | Role / Auth | Description |
| :--- | :--- | :--- | :--- |
| `/api/v1/auth/register` | `POST` | Public / Open | Patient registration & PBKDF2 password hashing. |
| `/api/v1/auth/login` | `POST` | Public / Open | Generates access token & cryptographic refresh token. |
| `/api/v1/auth/refresh` | `POST` | Bearer Token | Cryptographic session rotation without relogin. |
| `/api/v1/patients` | `GET` | Clinician / Staff | Master Patient Index (MPI) search with filters. |
| `/api/v1/appointments` | `POST` | Patient / Staff | Creates real clinical appointment & issues queue token. |
| `/api/v1/prescriptions` | `POST` | Doctor / Hakeem | Authors draft Nuskha, triggers safety firewall check. |
| `/api/v1/prescriptions/lock` | `POST` | Doctor (Only) | 21 CFR Part 11 digital signature sealing. |
| `/api/v1/inventory` | `GET` | Pharmacy / Staff | Returns FEFO sorted inventory with Mudabbar status. |
| `/api/v1/inventory/dispense`| `POST` | Pharmacist | Verifies Mudabbar cert & decrements batch stock. |
| `/api/v1/audit/logs` | `GET` | Administrator | Merkle-anchored immutable audit ledger blocks. |
| `/api/v1/health` | `GET` | Any | Microservice health check and DB connectivity status. |

---

## 7. How to Run Locally & Deploy

### Quick Local Start (Unified Launcher):
```bash
# Clone or navigate to the repository
cd /Users/irfanashraf/Downloads/zayvora-platform-phase0-4

# Run the single one-click startup script
./launch.sh
```
This automatically boots:
- **Live REST API & SQL Database Bridge:** `http://localhost:8000`
- **ZAYVORA Web Cockpit & All 10 Workspaces:** `http://localhost:8080`

### Full Next.js & Microservices Stack (Dev Mode):
```bash
# Terminal 1: Start Microservices Gateway & Engines
bash scripts/dev-start.sh

# Terminal 2: Start Next.js Frontend
cd apps/web
npm install
npm run dev
# Running on http://localhost:3000
```

### Running the Automated Test Battery:
```bash
python3 tests/run_all_tests.py
# Output:
# ======================================================================
# ✓ MASTER SUITE PASSED: 940 tests passed with ZERO failures.
# ======================================================================
```

### Production DNS & Deployment Mapping:
| Hostname | Destination | Environment |
| :--- | :--- | :--- |
| `www.zayvorahealth.com` | Production Web Cluster | Public Discovery Front-Door |
| `app.zayvorahealth.com` | Production Web Cluster | ZAYVORA Health OS (Intranet) |
| `api.zayvorahealth.com` | FastAPI Gateway / Port 8000 | Core Transactional API |
