# ZAYVORA Health OS™ — Release Notes

## v2.0.0 — 2026-09-15 (Pre-staging / Pilot Candidate)

### New in This Release

#### Phase 1 — Architecture & Design System
- Design System v5.0 with full CSS token set (`--bg-base`, `--bg-surface`, `--bg-card`, etc.)
- Role-aware `Sidebar` component with navigation for all 7 workspaces
- `PlatformFooter` with brand hierarchy and legal links
- `AppShell` upgraded with role detection from URL path

#### Phase 2 — Public Website
- 30+ public marketing routes under `/website/`
- Dynamic routes: `/website/blog/[slug]`, `/website/programs/[slug]`, `/website/herbals/[slug]`
- New pages: academy, teleconsultation, modern-science, ai-healthcare, clinical-care

#### Phase 3 — Clinical Workspaces
- **Doctor workspace:** queue, calendar, patients, encounters, mizaj, organ-axis, hakeem-sahab, nuskha, follow-ups, reports
- **Patient portal:** appointments, book, prescriptions, medications, labs, documents, symptoms, lifestyle, messages, care-plan, payments, notifications, consent, settings, help, doctors, clinics, teleconsultation, mizaj

#### Phase 4 — Intelligence Layer
- Hakeem Sahab AI™ clinical reasoning interface with safety invariant display
- Mizaj Engine documentation and assessment entry point
- Organ-Axis Mapper with 6 axes and engine status badges
- ZKI Safety Validator status (Partially Automated — 72%)

#### Phase 5 — Enterprise Modules
- Admin: roles, security, clinics, integrations, billing, subscriptions, system-health, backups, compliance, feature-flags
- Engine Observability dashboard (all 25 engines with status, coverage, safety flag)
- Manufacturing: batches (eBMR), QC lab, CoA modal with 21 CFR Part 11 HMAC
- Admin users and organisations connected to live identity service endpoints

#### Phase 6 — Mobile
- Mizaj Assessment Screen (10-question Ajnas-e-Ashrah)
- Notification Service (push token registration, dosage reminders)
- AppNavigator updated with MizajAssessment, TeleConsult, LifestyleTracker

#### Phase 7 — Hardening
- 300/300 unit tests passing (41 suites)
- Zero Python syntax errors across 262 files
- Zero TSX brace imbalances across 91 files
- Helm chart v2.0.0 with Vault agent and security contexts

#### Phase 8 — Documentation
- 17 `FINAL_*.md` documents covering all aspects of the platform

### Breaking Changes
- None (no live production system yet)

### Known Issues
- Live database not provisioned
- Neo4j ZKB not provisioned
- Vault not live
- No E2E test suite
- Security audit pending
