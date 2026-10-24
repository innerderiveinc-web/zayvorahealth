# ZAYVORA Health OS™ — UI/UX Baseline Audit Report

## Executive Summary
This baseline audit inspects the user interface, design tokens, navigation, typography, accessibility, and cognitive load across the entire **ZAYVORA Health OS™** ecosystem prior to the visual transformation.

The evaluation covers:
- The design system tokens (`design-system/`, `apps/web/app/globals.css`)
- Public website routes (`apps/web/app/page.tsx`, `/programs`, `/doctors`, `/knowledge-centre`, etc.)
- Web application dashboards (Patient, Doctor, Receptionist, Pharmacist, Admin)
- Mobile application screens (`apps/mobile/src/screens/`)
- Interactive states (Loading, Empty, Error, Offline)

---

## Comprehensive Baseline Findings & Remediation Plan

| ID | Screen / Route | Current Problem | User Impact | Priority | Recommended Solution | Files Affected | Verification Method |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **AUD-UI-01** | Global CSS / Tokens<br>`globals.css` | Color tokens mismatch: `globals.css` uses dark slate `#0a0f1d` with `#0d9488` teal, while `design-system` specifies Unani green `#2D6A4F` and cream `#FAFAF7`. Admin page uses generic light `#ffffff`. | Visual incoherence; disjointed experience when navigating between public, patient, and admin workspaces. | **P0** | Unify on centralized design tokens supporting a warm clinical cream canvas (`#FAFAF7`) for patient/public and low-eyestrain dark mode (`#0A0F1D`) for clinician cockpits. | `apps/web/app/globals.css`<br>`design-system/src/tokens.css` | Visual theme inspection across light/dark surfaces. |
| **AUD-UI-02** | Doctor Workspace<br>`/doctor` | Sprawling 14-tab horizontal navigation (`overview`, `history`, `examination`, `vitals`, `investigations`, `assessment`, `mizaj`, `afaal`, `axis`, `treatment`, `prescription`, `followup`, `timeline`, `twin`). | High cognitive load for treating physicians; clinical fatigue; excessive scrolling and tab switching during short OPD slots. | **P1** | Compress into a focused 3-area clinical workspace: Primary clinical note/Rx, Collapsible patient history side-drawer, and Hakeem Sahab AI copilot panel. | `apps/web/app/doctor/page.tsx` | Time-to-encounter clinical workflow verification. |
| **AUD-UI-03** | Patient Dashboard<br>`/patient` | Lingering dense technical terminology ("Asbab-e-Sittah Dyscrasia", "Afaal Organ-Axis") in patient-facing secondary tabs. | Medical anxiety for patients; confusion regarding actual medication schedules and daily lifestyle instructions. | **P1** | Adopt plain consumer language: "My Health", "Upcoming Visits", "My Care Plan", "Medicines & Regimen", "Ask Hakeem Sahab", "Daily Habits". Add explanatory tooltips for Unani concepts. | `apps/web/app/patient/page.tsx` | Consumer comprehension testing and text audit. |
| **AUD-UI-04** | Global Navigation<br>`components/Sidebar.tsx` | Sprawling 30+ item sidebar showing links irrelevant to active role (e.g. patients seeing manufacturing and clinical analytics). | Confusion; security ambiguity; cluttered interface. | **P1** | Implement strict role-based navigation hierarchy: Patient (6 items), Doctor (8 items), Receptionist (5 items), Pharmacist (5 items), Admin (7 items). | `apps/web/components/Sidebar.tsx`<br>`apps/web/components/PlatformHeader.tsx` | Multi-role login visual verification. |
| **AUD-UI-05** | Mobile App Navigation<br>`apps/mobile/AppNavigator.tsx` | Mobile app has 6 emoji-based bottom tabs (`Home`, `Appointments`, `Prescriptions`, `Labs`, `Notifications`, `Profile`) causing tab crowding on small screens (<375px). | Cramped touch targets; high risk of mis-taps; unprofessional emoji aesthetic. | **P1** | Simplify to canonical 5-tab structure: `Home`, `Care`, `Appointments`, `Messages`, `Profile` with clean SVG icons and safe-area padding. | `apps/mobile/src/navigation/AppNavigator.tsx` | Responsive mobile screen testing at 320px–390px. |
| **AUD-UI-06** | Mobile Screens<br>`apps/mobile/HomeScreen.tsx` | Dense tabular layouts and desktop card grids used on mobile screens. | Horizontal clipping; tiny unreadable text; poor touch interaction. | **P1** | Transform tables into mobile cards, list rows, and expandable bottom sheets with large touch targets (>48px). | `apps/mobile/src/screens/HomeScreen.tsx`<br>`AppointmentsScreen.tsx` | Viewport rendering check on mobile emulators. |
| **AUD-UI-07** | Admin Console<br>`apps/web/app/admin/` | Uses default Tailwind gray palette (`bg-gray-100`, `text-gray-800`) completely disconnected from the ZAYVORA Unani brand. | Looks like a third-party boilerplate admin template rather than part of ZAYVORA Health OS™. | **P2** | Restyle admin layout and pages using ZAYVORA brand tokens (`#2D6A4F`, `#1B4332`, `#FAFAF7`). | `apps/web/app/admin/layout.tsx`<br>`apps/web/app/admin/page.tsx` | Visual consistency check with global design tokens. |
| **AUD-UI-08** | Universal UI States<br>All Routes | Several secondary routes lack dedicated loading skeletons, resulting in cumulative layout shifts (CLS) when data loads. | Jarring layout shifts; user frustration during slow network connections. | **P1** | Implement reusable skeleton layouts (`LoadingSkeleton`), helpful empty states with action CTAs, and offline banners. | `design-system/src/components/`<br>`apps/web/components/ui/` | Simulated high-latency network testing. |
| **AUD-UI-09** | Accessibility (a11y)<br>Web & Mobile | Some icon-only action buttons lack `aria-label`; focus states are subtle or default browser outlines. | Violates WCAG 2.2 AA accessibility; impairs screen-reader and keyboard-only navigation users. | **P1** | Enforce accessible focus rings (`--shadow-focus-ring`), explicit ARIA labels on all icon buttons, and high-contrast status badges (>4.5:1). | `design-system/src/tokens.css`<br>`apps/web/components/` | Keyboard tab navigation & accessibility audit. |
| **AUD-UI-10** | Microcopy & Error Messages<br>All Routes | Technical errors ("Encounter payload invalid", "Database foreign key exception") occasionally displayed in alert banners. | Patient confusion; loss of institutional trust. | **P1** | Rewrite all error microcopy into human-centered, reassuring language with clear retry and support paths. | `apps/web/app/`<br>`apps/mobile/` | Automated text search for technical error strings. |

---

## Baseline Scorecard & Target State

| Dimension | Baseline Score (Pre-Transformation) | Target Score (Post-Transformation) |
| :--- | :---: | :---: |
| **Visual Consistency & Branding** | 6.5 / 10 | 9.8 / 10 |
| **Patient Consumer Friendliness** | 7.0 / 10 | 9.9 / 10 |
| **Clinician Ergonomics & Density**| 6.0 / 10 | 9.5 / 10 |
| **Mobile Native Feel** | 6.8 / 10 | 9.6 / 10 |
| **WCAG 2.2 AA Accessibility** | 7.5 / 10 | 9.8 / 10 |
| **UI State Completeness (Empty/Load/Error)** | 6.5 / 10 | 9.7 / 10 |

---

## Approved Execution Plan
Proceed directly to **Stage 1 (Design System)**, then **Stage 2 (Global Navigation)**, **Stage 3 (Public Website)**, **Stage 4 (Patient Portal)**, **Stage 5 (Mobile App)**, **Stage 6 (Doctor Workspace)**, **Stage 7 (Operations)**, **Stage 8 (UI States)**, **Stage 9 (Accessibility & Performance)**, and **Stage 10 (Verification)**.
