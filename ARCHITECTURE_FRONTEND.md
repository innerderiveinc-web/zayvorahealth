# ZAYVORA Health OS™ — Frontend Architecture & Developer Guide

## 1. Overview & Architecture Philosophy

ZAYVORA Health OS is architected to provide an instant, zero-dependency, ultra-fast clinical runtime that requires **no `npm install`**, **no node_modules bloat**, and **zero client-side compilation steps** at browser load time.

To achieve this without sacrificing modularity, the frontend employs a **Dual-Tier Modular Structure**:
1. **Source Code Tier (`js/modules/`)**: Individual, decoupled, highly focused ES6 modules organized by functional clinical domain.
2. **Distribution & Runtime Tier (`js/zayvora-core.js`)**: A deterministic, bundled distribution payload compiled by `scripts/bundle_frontend.py` with zero external dependencies.

> [!IMPORTANT]
> **DEVELOPER RULE**: NEVER edit `js/zayvora-core.js` directly! All functional edits, new features, and bug fixes must be authored in the respective module under `js/modules/`, followed by running `python3 scripts/bundle_frontend.py && python3 scripts/sync_all.py`.

---

## 2. Directory Structure & Domain Modules

```
js/
├── modules/
│   ├── 01-core-kernel.js                    # State store, event bus, reactive signals, auth session lifecycle
│   ├── 02-clinical-workspace.js             # Doctor cockpit, 10-Ajnas Mizaj, 9 Organ-Axis, SOAP notes, encounters
│   ├── 03-governance-admin.js               # Executive analytics, Merkle audit trail, user RBAC, facility settings
│   ├── 04-pharmacy-dispensary.js            # FEFO inventory, batch POS, checkout, preferences & currency engine
│   ├── 05-grand-library.js                  # 97 Classical treatises, Ibn Sina / Razi compendia, Qarabadeen
│   ├── 06-functional-suite.js               # Mathematical scoring engines, Afaal cascade, humoral balance
│   └── 07-interactive-modals-and-hardware.js # Camera scanner, optical nabz sensor, IoMT telemetry listeners
├── zayvora-core.js                          # Canonical bundled production distribution (Auto-generated)
└── zayvora-extensions.js                    # Supplementary helper plugins & experimental widgets
```

---

## 3. Developer Workflow: Adding Features or Modifying Logic

### Step 1: Locate the Domain Module
* **Doctor consultation, SOAP notes, clinical prescriptions, Mizaj calculator:**
  👉 Edit [`js/modules/02-clinical-workspace.js`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/js/modules/02-clinical-workspace.js)
* **Dispensary inventory, billing, language & currency switcher:**
  👉 Edit [`js/modules/04-pharmacy-dispensary.js`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/js/modules/04-pharmacy-dispensary.js)
* **User roles, permission gates, facility onboarding:**
  👉 Edit [`js/modules/03-governance-admin.js`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/js/modules/03-governance-admin.js)
* **Classical formulations & medical doctrine library:**
  👉 Edit [`js/modules/05-grand-library.js`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/js/modules/05-grand-library.js)

### Step 2: Bundle and Verify Frontend
Run the automated bundle compiler:
```bash
python3 scripts/bundle_frontend.py
```
This utility:
- Concatenates the 7 domain modules in strict dependency sequence.
- Validates JavaScript syntax natively using Node.js / JavaScript engines.
- Updates `js/zayvora-core.js` and reports line counts and bundle sizes.

### Step 3: Synchronize Deployment Targets
Propagate changes to `app.html`, `dist/`, and `docs/`:
```bash
python3 scripts/sync_all.py
python3 scripts/build_dist.py
```

### Step 4: Run Quality Gates & Tests
Ensure zero regressions or syntax defects:
```bash
python3 scripts/quality_gate.py
python3 tests/run_all_tests.py
```

---

## 4. UI Layout & View Separation

### 🏥 Clinic Edition (Matab Mode) vs 🏛️ Flagship HQ (Enterprise Mode)
The application shell features a built-in edition toggle:
* **Clinic OS (`clinic` mode)**: Stripped-down, distraction-free environment for daily Matabs and outpatient clinics. Focuses exclusively on:
  1. `📋 Reception / OPD Queue`
  2. `🩺 Doctor Cockpit (Consultation & Rx)`
  3. `💊 Pharmacy & Dispensary POS`
  4. `👤 Patient 360 Record`
* **Flagship HQ (`enterprise` mode)**: Full sovereign view exposing R&D formulation suites, eBMR manufacturing batch traceability, IoMT sensor telemetry, and observational clinical registry tools.

---

## 5. Coding Standards & Integrity Guards
1. **Zero Hallucination AI Rule**: AI suggestions must always pass through the Deterministic Safety Firewall (`services/therapeutic/app/routers/safety_firewall.py`).
2. **Preserve Comments & Docstrings**: Never remove clinical attribution or pharmacological contraindication comments.
3. **Responsive & Accessible**: All modals must support `Escape` key dismissal and mobile-responsive viewport scaling.
