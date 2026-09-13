# ZAYVORA Health OS — Frontend Gap Report & UI/UX Audit
**Document ID**: `ZAY-AUD-005`  
**Classification**: Frontend Quality & User Experience Standard  
**Date**: September 2026  
**Status**: AUDITED & VERIFIED  

---

## 1. Architectural Overview of `apps/web`

The ZAYVORA web frontend is built on **Next.js 16** leveraging the modern **App Router** architecture with server-side rendering (SSR), static optimization, and modular client-side React components.

- **Total Canonical Web Pages**: 52 pages (`page.tsx`)
- **Shared Clinical Shells**: 9 specialized role-based layouts (`DoctorShell`, `PatientShell`, `AdminShell`, `ReceptionistShell`, `PharmacistShell`, `ResearcherShell`, `EnterpriseOwnerShell`, `PublicWebsiteShell`, `AppShell`)
- **Reusable Domain Components**: 23 components (`NuskhaBuilder`, `PatientTimeline`, `MizajAssessmentModal`, `AmbientScribeGovernanceCockpit`, `DigitalTwinCockpit`, `HakeemReviewDrawer`, `MultimodalLabCockpit`, `PlatformHeader`, `PlatformFooter`, `PublicHeader`, `PublicFooter`, `StatCard`, `StatusBadge`, `EmptyState`, `ErrorBoundary`, etc.)
- **Shared Architecture Tokens**: `designTokens.ts`, `statusEnums.ts`, `routeMatrix.ts`, `dataContracts.ts`

---

## 2. Mandatory UI State Audit (Loading, Empty, Error, Permission)

In accordance with Section 4 of the Master Specification, every screen must gracefully render four fundamental UI states:

| Route / Module | Loading State | Empty State | Error State | Permission Denied State |
|:---|:---:|:---:|:---:|:---:|
| `/website` (Institutional Home) | Skeleton Banner | Contextual Banner | Fallback Error View | Public (Unrestricted) |
| `/website/programs` | Program Card Skeleton | "No programs match your filter" | Error Retry Alert | Public (Unrestricted) |
| `/website/herbals` | Grid Card Shimmer | "No botanical remedies found" | Network Retry Card | Public (Unrestricted) |
| `/website/doctors` | Clinician Avatar Shimmer | "No specialists currently listed" | Error Retry Alert | Public (Unrestricted) |
| `/website/book` | Calendar Slot Skeleton | "No open consultation slots" | Booking Failure Modal | Public (Unrestricted) |
| `/patient` (Patient Portal) | 13-Section Shimmer | "No active treatments found" | Portal Error Boundary | Auth Redirect Guard |
| `/doctor` & `/dashboard` (Doctor OS) | Queue Token Shimmer | "No patients in today OPD queue" | Clinical Alert Banner | Role Guard (`DOCTOR`) |
| `/receptionist` (OPD Queue) | Table Row Skeleton | "Waiting room is currently empty" | Action Failure Toast | Role Guard (`RECEPTIONIST`) |
| `/pharmacy` (Dispensary) | Inventory Row Shimmer| "All stock levels within threshold" | Dispense Blocked Card| Role Guard (`PHARMACIST`) |
| `/admin` (Enterprise IT) | Telemetry Card Shimmer| "No pending audit alerts" | DR Health Alert | Role Guard (`SUPER_ADMIN`) |
| `/ai` (Hakeem Sahab Studio) | Reasoning Pulse | "Select patient to start AI analysis" | Fallback Safe Notice | Clinician Role Guard |
| `/settings` (Settings Workspace) | Key Vault Shimmer | "No 2FA devices configured" | Update Failed Alert | Session Required Guard |

---

## 3. Developer Jargon Elimination Verification

A comprehensive audit was executed across all user-facing templates to ensure complete eradication of internal engineering terminology:

| Raw Developer Term (Forbidden in Clinical UI) | User-Facing Healthcare Replacement (Implemented) | Status |
|:---|:---|:---:|
| `GET /api/v1/clinical/patients` | "Patient Directory & Records" | **Resolved** |
| `tenant_id: 001` | "Facility: Jamia Hamdard AUTC - Main Hospital" | **Resolved** |
| `No data found` | "No patients have been registered yet. Add your first patient to begin." | **Resolved** |
| `safe_to_lock = False` | "Pending Licensed Clinician Review & Digital Signature" | **Resolved** |
| `25-Engine Live Matrix` | "Integrated Clinical Specialty Services" | **Resolved** |
| `Vector Store / RAG Retrieval` | "Validated Classical Literature & Pharmacopoeia Reference" | **Resolved** |
| `P95 Latency 1.2ms` | "System Status: Real-time Operational" | **Resolved** |
| `P0/P1 Blockers: 0` | "Clinical Quality & Safety Standards Verified" | **Resolved** |
| `Internal Error 500: Stack Trace` | "Secure clinical service encountered a temporary delay. Please refresh." | **Resolved** |

---

## 4. Frontend Gap Analysis & Remaining Refinements

1. **Prescription PDF Print Layout**:
   - *Current State*: Prescription modal displays formatted summary with digital signature hash and QR code placeholder.
   - *Target State*: Native browser print stylesheet (`@media print`) for standardized A4 medical prescription letterhead.
2. **Offline Local Storage Cache**:
   - *Current State*: Direct fetch to `http://localhost:8000` with in-memory fallback.
   - *Target State*: IndexedDB / ServiceWorker local cache for intermittent clinic network outages.
3. **Multi-lingual Toggle Integration**:
   - *Current State*: Vernacular audio posology supports Urdu, Hindi, and English; UI labels currently English-first.
   - *Target State*: Full RTL (Right-to-Left) Nastaliq typography support for Urdu clinical interfaces.

