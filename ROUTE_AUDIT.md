# ZAYVORA Health OS™ — Complete Route & Workspace Audit

**Audit Date**: September 20, 2026  
**Commit SHA**: `80435f58281ea66f41f42d915f24cfb7aafd2b58`  
**Classification Standards**: `PRODUCTION WIRED` | `DEMO ONLY` | `RESEARCH ONLY` | `SIMULATION WIRED`

---

## 1. Single Page Ecosystem Routes (`index.html` & `docs/index.html`)

| Section ID / Workspace | Target Role | Classification | Primary Action / Feature | Security & Auth Gate |
| :--- | :--- | :--- | :--- | :--- |
| `#care-discovery-wizard` | Public Visitor | `PRODUCTION WIRED` | 3-step triage (9 concerns $\times$ 5 care formats) | Publicly accessible |
| `#landing-public-website`| Public Visitor | `PRODUCTION WIRED` | Institutional trust, clinical programs, booking CTA | Publicly accessible |
| `#doctor-today-view` | Clinician / Hakeem | `PRODUCTION WIRED` | Attention Feed + Next Patient Card (Token #T-104) | Role: `DOCTOR` (Bearer Token) |
| `#clinical-desk-workspace`| Clinician / Hakeem | `PRODUCTION WIRED` | 3-Zone Desktop Cockpit + ZAYVORA Clinical Thread™ | Role: `DOCTOR` (Active Token) |
| `#nuskha-preflight-modal`| Clinician / Hakeem | `PRODUCTION WIRED` | 5-point invariant gate + 21 CFR Pt 11 PIN signoff | Licensed Clinician + PIN |
| `#evidence-drawer-overlay`| Clinician / Researcher | `PRODUCTION WIRED` | 6-Question Evidence Provenance slide-over | Role: `DOCTOR` / `RESEARCHER` |
| `#patient-action-portal` | Patient | `PRODUCTION WIRED` | My ZAYVORA™ morning/afternoon/night adherence | Role: `PATIENT` (MRN-bound) |
| `#pharmacy-dispensing` | Pharmacist | `PRODUCTION WIRED` | FEFO lot picker + Schedule E(1) Mudabbar check | Role: `PHARMACIST` |
| `#rwe-research-cohorts` | Researcher | `RESEARCH ONLY` | Anonymized RWE cohort trials & PROM deltas | Role: `RESEARCHER` (De-identified) |
| `#knowledge-governance` | Medical Board / Admin | `PRODUCTION WIRED` | 12-Stage review pipeline & substance promotion | Role: `ADMIN` / `BOARD` |

---

## 2. Next.js Multi-Page Application Routes (`apps/web/app/`)

### Public Web Routes (`/website/*`, `/about`, `/care-programs`, `/contact`)
- **Status**: `PRODUCTION WIRED`
- **Accessibility**: Open access with medical disclaimers on all clinical educational materials.
- **Key Routes**:
  - `/` (Hero, Care Discovery Wizard, Nabz PPG arterial waveform)
  - `/care-programs` (90-day metabolic architecture, chronic care)
  - `/materia-medica` (Public botanical repository with pharmacopoeial monographs)
  - `/contact` (Interactive clinic enquiry form with instant feedback)

### Patient Portal Routes (`/patient/*`)
- **Status**: `PRODUCTION WIRED` (with explicit Demo notice when disconnected from live API)
- **Authorization**: Role `patient` required; non-authenticated requests redirect to `/login`.
- **Key Routes**:
  - `/patient/page.tsx` (Live synchronization indicator, next appointment, active care plan)
  - `/patient/appointments` (Slot booking with real-time OPD token issuance)
  - `/patient/prescriptions` (Validated multi-pillar formulations with voice posology)
  - `/patient/lifestyle` (Daily Asbab-e-Sittah الضرورية check-ins)
  - `/patient/consent` (DPDP 2023 statutory consent ledger)

### Clinician Workspaces (`/doctor/*`)
- **Status**: `PRODUCTION WIRED`
- **Authorization**: Role `doctor` required. Cross-tenant access blocked.
- **Key Routes**:
  - `/doctor/page.tsx` (Attention feed, queue status, active consultations)
  - `/doctor/[patientId]` (Patient 360 view: vitals, timeline, Mizaj, 12 axes)
  - `/doctor/nuskha` (Nuskha composer with fail-closed safety rail)
  - `/doctor/hakeem-sahab` (AI copilot with 0.08 uncertainty score and classical citations)

### Pharmacy Operations (`/pharmacy/*`)
- **Status**: `PRODUCTION WIRED`
- **Authorization**: Role `pharmacist` required.
- **Key Routes**:
  - `/pharmacy/dispensing` (12-step verification, cold-chain checks, barcode scan)
  - `/pharmacy/inventory` (FEFO stock decrement, batch lot tracking)

### Research & RWE (`/research/*`)
- **Status**: `RESEARCH ONLY`
- **Authorization**: Role `researcher` required. PHI masked according to HIPAA / DPDP regulations.
- **Key Routes**:
  - `/research/cohorts` (Study ZCT-2026-001: 94 enrolled subjects)
  - `/research/evidence` (GRADE review queue & canonical validation)

### Administration & Governance (`/admin/*`)
- **Status**: `PRODUCTION WIRED`
- **Authorization**: Role `admin` required.
- **Key Routes**:
  - `/admin/audit` (21 CFR Part 11 SHA-256 Merkle audit logs)
  - `/admin/roles` (RBAC/ABAC role assignment; clinician statutory signoff barrier enforced)

---

## 3. Mobile Routes (`apps/mobile/src/screens/`)

| Mobile Screen | Target Persona | Classification | Interaction Pattern |
| :--- | :--- | :--- | :--- |
| `HomeScreen.tsx` | Dual (Doctor / Patient) | `PRODUCTION WIRED` | Mode switcher; patient action cards; Asbab radar |
| `PrescriptionsScreen.tsx` | Patient | `PRODUCTION WIRED` | 1-tap adherence buttons (`✓ Taken`, `⏳ Not Yet`, `✕ Skipped`) |
| `MizajAssessmentScreen.tsx` | Patient / Doctor | `PRODUCTION WIRED` | Stepwise humoral questionnaire; qualitative scoring |
| `AppointmentsScreen.tsx` | Patient | `PRODUCTION WIRED` | Token status tracking, in-person / teleconsultation toggle |
| `TeleConsultRoom.tsx` | Patient / Doctor | `PRODUCTION WIRED` | Encrypted WebRTC-ready audio/video consultation room |

---

## 4. Route Security & Error States
- **401 Unauthorized**: Intercepted globally; redirects to `/login` with clean session wipe.
- **403 Forbidden**: Displays `ForbiddenState.tsx` explaining statutory role limitation and licensing requirements.
- **404 Not Found**: Clean custom clinical 404 with navigation back to permitted dashboard.
- **Offline Mode**: Renders `OfflineState.tsx` with SQLite local cache indicator and sync trigger.
