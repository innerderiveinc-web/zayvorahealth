# ZAYVORA Health OS™ — Universal UI State Coverage Report

## Executive Summary
This report documents the implementation and audit of the universal **Interactive UI States** (Loading, Empty, Error, Offline, and Permission) across the web and mobile applications of **ZAYVORA Health OS™**. 

Each state has been designed to eliminate cumulative layout shift (CLS), provide empathetic and actionable patient communication, prevent accidental data loss, and maintain transparency regarding data freshness.

---

## 1. UI State Standards & Specifications

### A. Loading States (Skeleton Layouts)
- **Design Rule**: Skeleton pulse placeholders (`.zv-skeleton`) match the exact dimensions and grid layout of the incoming data cards.
- **Implementation**:
  - `LoadingSkeleton` in `design-system/src/components/LoadingSkeleton.tsx`.
  - `PATIENT_LOADING_SKELETON` in `apps/web/app/doctor/page.tsx` preventing layout shift during patient chart resolution.
  - Spinner overlays with localized progress indicators during cryptographic 21 CFR prescription sealing (`"⏳ Sealing Encounter..."`).

### B. Empty States (Action-Oriented & Reassuring)
- **Design Rule**: Never display a blank card or empty table. Explain: (1) what is missing, (2) why it matters, and (3) provide an immediate primary action CTA.
- **Standardized Implementations**:
  - **Appointments**:
    > *“You have no upcoming consultations scheduled. Book your appointment to begin your personalized care journey.”*  
    > `[ + Book Consultation ]`
  - **Prescriptions**:
    > *“No active prescriptions. Once your attending Tabeeb authors your Nuskha, your daily regimen will appear here.”*  
    > `[ View Clinical Programs ]`
  - **Lab Reports**:
    > *“No lab reports uploaded yet. Upload biomarker test results or request a diagnostic panel.”*  
    > `[ Upload Diagnostic Report ]`

### C. Error States (Empathetic & Recoverable)
- **Design Rule**: Never display raw SQL traces, foreign key exceptions, or cryptic HTTP error codes. Clearly indicate: (1) what happened, (2) whether user draft data was preserved, and (3) a clear retry button.
- **Standardized Implementation**:
  - Inline error banners with icon, title, human-friendly explanation, and `[ ↻ Retry ]` / `[ Contact Support ]` actions.
  - React `ErrorBoundary` wrapper (`apps/web/components/ErrorBoundary.tsx`) catching unhandled frontend exceptions.

### D. Offline States (Transparent Freshness & Sync)
- **Design Rule**: Clearly announce cached data state. Never falsely imply offline data is real-time.
- **Standardized Implementation**:
  - Non-intrusive offline banner:
    > *“⚡ Offline Mode: Displaying cached regimen from Sep 16, 14:30. Changes will automatically sync once your connection is restored.”*
  - Destructive actions (e.g. prescription locking, appointment payment) disabled while offline with clear explanatory tooltip.
  - Mobile `OfflineStorageService` asynchronously queues vital sign logs and vitals telemetry for automatic replay.

### E. Permission States
- **Design Rule**: Pre-prompt users before browser/device permission dialogs.
- **Standardized Implementation**:
  - Telemedicine room pre-call check explaining camera and microphone access requirements for pulse visual inspection (*Muayana-e-Nabz*).

---

## 2. Verification Matrix Across Major Screens

| Screen / Workspace | Loading State | Empty State | Error State | Offline Awareness | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Public Homepage** (`/`) | Fast SSR | N/A | Error Boundary | N/A | **VERIFIED** |
| **Patient Dashboard** (`/patient`) | Skeleton | Reassuring CTA | Retry Banner | Cache Notice | **VERIFIED** |
| **Doctor Cockpit** (`/doctor`) | Skeleton | Queue Empty CTA | Auto-Save Alert| Local Draft Lock | **VERIFIED** |
| **Reception Desk** (`/reception`) | Skeleton | Queue Empty | Reconnect Button | Local Token Cache | **VERIFIED** |
| **Pharmacy OS** (`/pharmacy`) | Skeleton | "All Dispensed" | Re-verify Alert | Inventory Lock | **VERIFIED** |
| **Admin Console** (`/admin`) | Skeleton | "No Events" | Service Status | N/A | **VERIFIED** |
| **Mobile Home** (`HomeScreen`) | Native Spinner| Empty Checklist | Toast Notification| AsyncStorage Sync | **VERIFIED** |
