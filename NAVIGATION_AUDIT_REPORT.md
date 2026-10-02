# ZAYVORA Health OS™ — Global Navigation Architecture & Audit Report

## Executive Summary
This report documents the architectural consolidation of the global navigation layer across **ZAYVORA Health OS™**. Previously, the sidebar contained an uncurated list of 30+ items exposed indiscriminately across roles. The system now enforces strict, role-bounded navigation hierarchies aligned with clinical workflows and consumer expectations.

---

## 1. Role-Specific Navigation Taxonomies

### A. Patient Navigation (6 Items)
Designed for low cognitive load and clear health actionability:
1. **Home** (`/patient`): Patient orientation cards, health status, next steps.
2. **Care** (`/programs`): Active care protocols, 30/60/90-day Unani wellness programs.
3. **Appointments** (`/patient/appointments`): OPD booking, queue tokens, rescheduling/cancellation.
4. **Reports** (`/patient/labs`): Biomarker history, diagnostic summaries, vital telemetry.
5. **Messages** (`/messages`): Secure clinical communication with attending clinician.
6. **Profile** (`/patient/profile`): Contact information, emergency contacts, consent preferences.

### B. Doctor Navigation (8 Items)
Engineered for rapid OPD throughput and minimal clinical clicks:
1. **Today** (`/doctor`): Active consultation cockpit, primary patient chart.
2. **Patients** (`/doctor/patients`): Searchable roster of registered facility patients.
3. **Queue** (`/doctor/queue`): Real-time OPD triage queue with acuity levels.
4. **Encounters** (`/doctor/encounters`): Clinical consultation history and past notes.
5. **Prescriptions** (`/doctor/nuskha`): 21 CFR Part 11 compliant Nuskha builder and posology engine.
6. **Follow-ups** (`/doctor/follow-ups`): Scheduled recall and longitudinal outcome tracking.
7. **Hakeem Sahab** (`/doctor/hakeem-sahab`): Assistive AI copilot with Accept/Edit/Reject controls.
8. **Reports** (`/doctor/reports`): Clinical audit and diagnostic concordance reports.

### C. Reception Navigation (5 Items)
Optimized for rapid front-desk check-in:
1. **Today** (`/reception`): Front desk dashboard, OPD room statuses.
2. **Appointments** (`/receptionist/appointments`): Multi-doctor OPD calendar.
3. **Queue** (`/receptionist/queue`): Live waiting room queue, token assignment.
4. **Patients** (`/receptionist/patients`): Patient registration and demographics.
5. **Communication** (`/messages`): Patient notifications and appointment SMS alerts.

### D. Pharmacy Navigation (5 Items)
Structured for Good Pharmacy Practice (GPP) and statutory compliance:
1. **Prescriptions** (`/pharmacy`): Incoming signed prescription orders.
2. **Dispensing** (`/pharmacy/dispensing`): FEFO batch allocation and verification.
3. **Inventory** (`/pharmacy/inventory`): Stock levels, expiry alerts, Mudabbar certificates.
4. **Products** (`/products`): Standardized Unani formulations catalog.
5. **Alerts** (`/pharmacy/alerts`): Stockout and recall notifications.

### E. Admin Navigation (7 Items)
Enterprise SaaS governance and audit oversight:
1. **Overview** (`/admin`): Key metrics, active users, clinical throughput.
2. **Users** (`/admin/users`): Staff and clinician user account provisioning.
3. **Clinics** (`/admin/health`): Facility telemetry and microservice health checks.
4. **Roles** (`/admin/users`): Role-based permission assignments.
5. **Configuration** (`/settings`): Global parameters and integration credentials.
6. **Audit Logs** (`/admin/audit`): Tamper-evident Merkle ledger audit viewer.
7. **Reports** (`/admin/reports`): Aggregate operational reports.

---

## 2. Navigation Integrity & Audit Verifications
- **Zero Dead Links**: 100% of links resolve to valid, active application routes; zero `href="#"` or unhandled routes.
- **Active State Highlighting**: Current route actively highlighted with high-contrast emerald indicator (`border-emerald-500/40`, `bg-emerald-950/50`).
- **Keyboard Navigation**: All navigation anchors and collapse buttons support keyboard focus (`Tab`, `Shift+Tab`, `Enter`).
- **ARIA Compliance**: Proper `aria-label`, `aria-current="page"`, and landmark `<nav>` and `<aside>` tags applied.
