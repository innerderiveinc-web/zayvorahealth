<div align="center">
  <h1>🌿 ZAYVORA Health OS™</h1>
  <p><strong>ذیورہ</strong> — Enterprise Autonomous AI Operating System for Classical & Integrative Medicine</p>
  <p><em>Ancient Canonical Treatises. Modern Clinical Intelligence. Closed-Loop Agentic Care.</em></p>

  [![CI Matrix](https://img.shields.io/badge/CI%2FCD-Matrix%20Verified-2D6A4F?style=for-the-badge&logo=githubactions)](infrastructure/ci/github-actions-ci.yml)
  [![Quality Gate](https://img.shields.io/badge/Quality%20Gate-Zero%20Defects-2D6A4F?style=for-the-badge&logo=shield)](scripts/quality_gate.py)
  [![Tests](https://img.shields.io/badge/Tests-732%2F732%20Passing-success?style=for-the-badge&logo=checkmarx)](tests/)
  [![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python)](pyproject.toml)
  [![Database](https://img.shields.io/badge/Database-SQLite%20WAL%20%7C%20PostgreSQL-336791?style=for-the-badge&logo=postgresql)](database/adapter.py)
  [![Compliance](https://img.shields.io/badge/Compliance-21%20CFR%20Part%2011%20%7C%20AYUSH%20UPI-blue?style=for-the-badge)](docs/compliance/)
  [![Platform](https://img.shields.io/badge/Platform-Web%20%7C%20Mobile%20APK%20%7C%20Docker-purple?style=for-the-badge)](Dockerfile)
</div>

---

## 📖 Executive Summary

**ZAYVORA Health OS™** is an enterprise-grade healthcare operating system that transforms traditional Unani Tibb and Integrative Medicine from reactive manual dictation into a **closed-loop autonomous agentic clinical platform**.

Built with a **zero-external-dependency Python 3 core**, ZAYVORA runs anywhere—from offline clinic hardware and micro-servers to multi-tenant cloud clusters (Railway, Docker, Kubernetes). It natively embeds:
* **The Classical Canon**: Semantic index across 97 medical treatises (*Al-Qanun fi al-Tibb*, *Kitab al-Hawi*, *Dhakhira Khwarizmshahi*).
* **AYUSH & Unani Pharmacopoeia of India (UPI)**: 250 validated single-drug monographs, compound formulations, posology ceilings, and Schedule E(1) Mudabbar detox firewalls.
* **Closed-Loop Sensory Pipelines**: Chromatic tongue (*Lisan*) analysis, urine (*Qaroorah*) concoction staging, lab OCR extraction, and multi-lingual vernacular voice dictation.

---

## 🤖 The 9 Autonomous Closed-Loop Agentic Pipelines

Unlike conventional healthcare chatbots that rely on reactive prompting, ZAYVORA executes continuous, background **closed-loop agentic loops**:

| # | Agentic Pipeline | Engine Target | Autopilot Clinical Responsibility |
|:---:|---|---|---|
| **1** | **`TriageAgent`** | `services/live_api_server.py` | Automatically ingests patient hemodynamics, BMI, and 10-Ajnas pulse to generate an actionable pre-consult case brief before doctor opens the door. |
| **2** | **`CanonResearchAgent`** | `services/live_api_server.py` | Performs autonomous semantic crosswalk across 38 treatise chapters & 250 UPI monographs, synthesizing print-ready classical evidence dossiers. |
| **3** | **`CareContinuityAgent`** | `services/live_api_server.py` | Closed-loop 5-point *Alamat-e-Nujz* concoction state machine; alerts doctor at 80% concoction for 1-click Phase 2 (Tanqiya / Mushil) evacuation. |
| **4** | **`ReinforcementAgent`** | `services/live_api_server.py` | Analyzes doctor prescription edits to train a dynamic `formulation_preference_matrix` while enforcing fail-closed UPI posology safety ceilings. |
| **5** | **`DeviceSyncEngine`** | `services/live_api_server.py` | Bi-directional offline dirty-queue ingestion (`/api/v1/sync/batch`) and delta synchronization for multi-device clinic operation. |
| **6** | **`PharmacyInventoryAgent`** | `services/live_api_server.py` | Continuous FEFO expiry surveillance, Schedule E(1) Mudabbar poison firewall, and automated candidate purchase order drafting. |
| **7** | **`DiagnosticVisionAgent`** | `services/live_api_server.py` | Multi-modal chromatic feature extraction for Tongue (Lisan coating/moisture), Urine (Qaroorah Rasub), and lab report OCR biomarker indexing. |
| **8** | **`VoiceAgenticScribe`** | `services/live_api_server.py` | Ambient multi-lingual speech recognition (Roman Urdu, Hindi, English) structuring complaints, humoral dyscrasia, and active Nuskhas with zero typing. |
| **9** | **`MobileAppApkBuild`** | `apps/mobile/` | Automated standalone Android `.apk` generation pipeline via EAS Build (`preview` profile) for instant device sideloading. |

---

## 🚀 Quick Start (Running ZAYVORA)

### Method 1: Instant Local Launcher (Zero Dependencies)
Runs natively using only Python standard library:
```bash
# Clone the repository
git clone https://github.com/innerderiveinc-web/zayvorahealth.git
cd zayvorahealth

# Launch the unified server on port 8000
./start.sh
# Open http://localhost:8000 in your browser
```

### Method 2: Docker Container (Multi-Platform OCI)
Deploy on any cloud VM (DigitalOcean, AWS EC2, GCP, Azure, or local Docker Desktop):
```bash
# Build production container image
docker build -t zayvora-health-os .

# Run container with dynamic port mapping
docker run -d -p 8000:8000 --name zayvora zayvora-health-os

# Access application
curl -f http://localhost:8000/api/v1/health
```

### Method 3: Cloud One-Click Deployment (Railway.app)
1. Navigate to [Railway.app](https://railway.app).
2. Select **"New Project"** → **"Deploy from GitHub repo"**.
3. Select `zayvorahealth` (or `zayvorahealthos`).
4. Railway auto-detects `railway.json` and `nixpacks.toml`, launching the container with zero configuration.
5. In Project Settings, click **"Generate Domain"** to get your public SSL URL:
   `https://zayvora-production.up.railway.app`

### Method 4: Mobile Standalone Android APK Build
```bash
# EAS Cloud Build (generates direct .apk download link):
cd apps/mobile && npm run build:apk:cloud

# Or using the build automation script:
./scripts/build_mobile_apk.sh --cloud
```

---

## 🛠️ Developer Make Commands

```bash
make run          # Start local production server on port 8000
make test-all     # Run all 732 automated unit and clinical tests
make quality      # Run zero-defect pre-commit / pre-push Quality Gate
make seed         # Seed database profiles (baseline, demo, pilot, zfie, all)
make bundle-js    # Validate frontend modules and compile production bundle
make sync         # Synchronize canonical HTML and database mirrors
make apk          # Submit standalone Android APK build to EAS Cloud
make package      # Build clean canonical zip release archive
```

---

## 📚 Technical Documentation Hub

Comprehensive, international-standard technical documentation organized according to the **Diátaxis Framework**:
* 🏛️ **[Diátaxis Documentation Hub](docs/README.md)**: Central portal linking all subsystem specifications.
* 📐 **[System Architecture](docs/architecture/FINAL_ARCHITECTURE.md)** & **[Runtime Topology](docs/architecture/SYSTEM_RUNTIME_TOPOLOGY.md)**: Master structural design & dual-profile runtime specification.
* ⚖️ **[Compliance & Statutory Mapping](docs/compliance/STATUTORY_COMPLIANCE_AND_REGULATORY_MAPPING.md)**: 21 CFR Part 11, HIPAA, GDPR, ABDM M1-M3 & DISHA controls.
* 🛡️ **[Security Architecture](docs/security/FINAL_SECURITY_MODEL.md)**: AES-256-GCM authenticated encryption & anti-backdoor shields.
* 📦 **[Frontend Client Architecture](js/README.md)**: 7 domain modules, zero-build PWA, and React/Next.js client topology.

---

## 📁 Repository Directory Structure

```
zayvora-platform/
├── .dockerignore                     # Container build ignore rules
├── .gitignore                        # Git exclusion rules
├── Dockerfile                        # Multi-platform production OCI container
├── Makefile                          # Canonical developer make targets
├── Procfile                          # Cloud PaaS process definition
├── railway.json                      # Railway cloud configuration & health probes
├── README.md                         # Master documentation & system overview
├── CHANGELOG.md                      # Release changelog
│
├── apps/
│   ├── mobile/                       # React Native (Expo 51) Companion App (11 screens)
│   └── web/                          # Production Web Application
│
├── database/                         # Canonical SQLite database & schema migrations
│   └── zayvora_live.db               # Production-grade relational data store
│
├── dist/                             # Pre-compiled static distribution mirror
├── docs/                             # Comprehensive structured documentation
│   ├── ai_doctrine/                  # AI system prompts, doctrine & non-stochastic bounds
│   ├── architecture/                 # System blueprints & architectural decision records
│   ├── clinical/                     # Classical medical treatises & monographs
│   ├── compendiums/                  # Formal BOM & Product Manufacturing PDFs
│   ├── governance/                   # 21 CFR Part 11, HIPAA, Clinical Pilot & Protocols
│   │   ├── clinical_pilot/           # 20 Clinical pilot SOPs, consent forms & KPI charters
│   │   ├── policies/                 # 21 CFR Part 11, HIPAA & Safe-to-Lock enforcement
│   │   └── protocols/                # Clinical governance charter & Mudabbar SOPs
│   └── reports/
│       ├── historical/               # Archived audit reports & certification logs
│       ├── test_runs/                # Verification manifests & XML test reports
│       └── coverage/                 # Code coverage summaries
│
├── js/                               # Frontend core engines (zayvora-core.js)
├── knowledge/                        # Canonical Medical Knowledge & Pharmacopoeia
│   ├── pharmacopoeia/                # UPI monographs, NFUM formulations & Schedule E(1)
│   ├── asbab_sittah_guidelines.json  # Six Essential Lifestyle Principles
│   └── organ_axis_pathways.json      # 12-Organ Axis Physiological Pathways
│
├── scripts/                          # 20 Active operational & CI/CD tools
│   ├── quality_gate.py               # Pre-commit zero-defect syntax & security gate
│   ├── package_production_release.py # Production release packager
│   ├── build_mobile_apk.sh           # Standalone Android APK builder
│   ├── sync_all.py                   # Master static parity & mirror engine
│   ├── production_rollback.py        # Disaster recovery rollback engine
│   └── archive/legacy_patches/       # 150+ Historical migration & patch scripts
│
├── services/                         # Python backend & agentic micro-engines
│   └── live_api_server.py            # High-performance zero-dependency REST server
│
├── start.sh                          # 1-Click platform startup runner
└── tests/                            # 718 Automated unit, clinical & integration tests
```

---

## 🔒 Security, Safety & Statutory Governance

1. **Non-Stochastic Clinical Bounding**: AI agents never autonomously prescribe or dispense medications. All AI recommendations are tagged as **Draft Clinical Recommendations (DCR)** until locked by a licensed practitioner's cryptographic **21 CFR Part 11 Electronic Signature**.
2. **Deterministic Schedule E(1) Firewall**: Highly potent botanical substances (*Aconitum napellus/Bish*, *Strychnos nux-vomica/Azaraqi*, *Cannabis sativa/Qinnab*) cannot be dispensed without verified *Mudabbar* detoxification batch certificates.
3. **Fail-Closed Quality Gate Shield**: Pre-commit and pre-push hooks execute automated syntax validation and anti-backdoor security scanners. Zero commits are accepted without passing all quality checks.

---

## 📜 Intellectual Property & Licensing

Proprietary Software — © 2026 ZAYVORA Healthcare Technologies. All rights reserved.  
Compliant with Central Council for Research in Unani Medicine (CCRUM) & Ministry of AYUSH clinical documentation guidelines.
