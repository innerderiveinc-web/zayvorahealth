# 🌿 ZAYVORA Health OS™ — Developer Quickstart Guide

Welcome to **ZAYVORA Health OS™** (Integrative Clinical Operating System & Pharmacopoeia Engine).

---

## ⚡ 1. Prerequisites
- **Python 3.9+** (Zero external dependencies needed for the live standalone clinical server).
- **Modern Web Browser** (Chrome / Safari / Edge / Firefox) with webcam access for optical scanning.

---

## 🚀 2. Run the Platform in 5 Seconds

### Step 1: Start the Local Backend REST Server
```bash
python3 services/live_api_server.py 8088
```
*Server will start listening at `http://localhost:8088` connected to SQLite database.*

### Step 2: Open the Web Application
Open your browser and navigate to:
```
http://localhost:8088
```
*(Or simply double-click `index.html` or `docs/index.html` in your browser).*

---

## 🧪 3. Run the Verification Test Suite
To verify the entire ecosystem (all 45 clinical engines, safety firewalls, and regulatory protocols):
```bash
python3 tests/run_all_tests.py
```
*Expected Result: `✓ MASTER SUITE PASSED: 981 tests passed with ZERO failures.`*

---

## 👥 4. Demo Login Credentials (Outpatient Matab)

| Role | Email | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Clinician (Doctor)** | `doctor@zayvora.com` | `Password123!` | Full Clinical Desk, 13-Tab Consultation, 21 CFR 11 Prescription Locking |
| **Central Pharmacist** | `pharmacist@zayvora.com` | `Password123!` | FEFO Dispensary Queue, Barcode Scanner, Batch Audit |
| **Clinic Receptionist**| `reception@zayvora.com` | `Password123!` | OPD Token Generation, Patient Registration, ABHA Linking |
| **Patient (Hamza)**    | `patient@zayvora.com` | `Password123!` | Vernacular Audio Posology, Active Formulations, Dietary Parhez |
| **Super Admin**        | `admin@zayvora.com` | `Password123!` | Multi-Facility Registry, 21 CFR Merkle Ledger, System Health |

---

## 📂 5. Architecture Directory Map

```
zayvora-platform/
├── index.html              # Canonical Single-Page Unified Clinical Desk & Discovery Engine
├── docs/                   # GitHub Pages & Production Documentation Bundle
├── database/               # SQLite & Schema Seeds (zayvora_live.db)
├── services/               # Modular FastAPI & Zero-Dependency Microservices
│   ├── clinical/           # Encounter, SOAP, 10-Ajnas Mizaj & Organ-Axis Engines
│   ├── therapeutic/        # Master Nuskha Builder, CYP450 Screener, Mudabbar Gate
│   ├── knowledge/          # 250+ UPI Mufradat, Murakkabat, Classical Unani Library
│   ├── ai/                 # Hakeem Sahab Agentic AI Copilot & Safety Guardrails
│   └── live_api_server.py  # Production Monolith REST Server
├── tests/                  # Complete 981-Test Suite (tests/run_all_tests.py)
├── apps/                   # Next.js Web App & React Native Mobile App
└── infrastructure/         # Docker Compose, Helm Charts & K8s Manifests
```

For full architecture details, refer to `DEVELOPER_HANDOVER_OVERVIEW.md`.
