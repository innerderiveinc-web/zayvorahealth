# ZAYVORA Health OS — Client-Side Architecture & Modular Script Engine

This directory contains the client-side JavaScript architecture for **ZAYVORA Health OS (V5.0.0-Enterprise)**.

---

## 🏛️ Tri-Tier Client Architecture Overview

ZAYVORA provides three distinct frontend targets tailored for different operational environments:

1. **Edge/Offline PWA Client (`/index.html` + `js/zayvora-core.js`):**
   - Zero-build, standard-compliant browser client designed for offline field clinics, local laptops, and rapid low-latency clinical desks.
   - Requires zero Node.js server runtime; boots instantly from static file hosting or local HTTP daemon.
2. **Enterprise Cloud Web Application (`apps/web/`):**
   - Full Next.js 14 / TypeScript React web application equipped with server-side rendering (SSR), advanced dashboard charting, and enterprise identity federation.
3. **Mobile Clinician & Patient Application (`apps/mobile/`):**
   - Native cross-platform application built on React Native & Expo (iOS / Android) for bedside rounds, remote tele-consults, and offline biometric capture.

---

## 📂 JavaScript Directory Structure

```
js/
├── README.md                               # This architectural specification
├── zayvora-core.js                         # Production distribution bundle (Edge PWA)
├── zayvora-extensions.js                   # Extended telemetry & specialized clinical tools
├── grand-corpus-vault-data.js              # Canonical 97-Treatise offline bibliography vault
└── modules/                                # Domain-Separated Modular Controllers
    ├── 01-core-kernel.js                   # Theme switcher, state store, event bus, base utils
    ├── 02-clinical-workspace.js            # Doctor consult desk, patient intake, EHR charts, Nuskha
    ├── 03-governance-admin.js              # 21 CFR Part 11 Auth, RBAC, session tokens, security
    ├── 04-pharmacy-dispensary.js           # Posology converter, FEFO inventory, B2B wholesale
    ├── 05-grand-library.js                 # 12 Volumes Unani pharmacopoeia, UPI monographs
    ├── 06-functional-suite.js              # Mizaj assessment modal, 12-Organ Axis, Asbab-e-Sittah
    └── 07-interactive-modals-and-hardware.js # 3D Molecular Docking, Webcam rPPG Nabz Scanner
```

---

## 🛠️ Build & Verification Pipeline

Run the automated bundler and syntax verifier to validate all domain modules:

```bash
python3 scripts/bundle_frontend.py
```

This pipeline automatically:
1. Validates native JavaScript syntax (`node --check`) across all 7 domain modules.
2. Asserts bundle integrity of `zayvora-core.js` and `zayvora-extensions.js`.
3. Synchronizes verified assets to the `docs/js/` GitHub Pages hosting mirror.
