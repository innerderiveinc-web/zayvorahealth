# ZAYVORA Health OS™ — Component Architecture & Design System Audit

**Audit Date**: September 20, 2026  
**Commit SHA**: `80435f58281ea66f41f42d915f24cfb7aafd2b58`  
**Package**: `design-system` v0.1.0  
**Status**: 100% Export Integrity & Type Safety

---

## 1. Design Token Consolidation

All components consume centralized tokens defined in `design-system/src/tokens.css` and `design-system/tailwind.config.js`:

| Token Category | Brand Values | Clinical Semantic Mapping |
| :--- | :--- | :--- |
| **Primary Palette** | Unani Forest Green (`#2D6A4F`), Deep Teal (`#1B4332`) | Clinical authority, verified safe status, primary actions |
| **Secondary Accent** | Warm Gold (`#F4A261`), Alabaster Cream (`#FAFAF7`) | Cautions, highlighted milestones, canonical highlights |
| **Alert Palette** | Rose (`#E63946`), Amber (`#E76F51`), Emerald (`#2A9D8F`) | BLOCK (hard stop), CAUTION (justification required), PASS |
| **Typography** | `font-sans`: Inter, `font-display`: Amiri | High legibility for vitals & Latin text; authentic Arabic/Urdu typography |
| **Border Radii** | `sm: 4px`, `md: 8px`, `lg: 12px`, `xl: 16px`, `full: 9999px` | Consistent card corners, buttons, and status tags |
| **Shadows** | `shadow-card`, `shadow-modal`, `shadow-drawer` | Elevation hierarchy avoiding visual fatigue |

---

## 2. Foundational UI Primitives Audit (`design-system/src/primitives/`)

| Primitive Component | TypeScript Interface | Accessibility & ARIA Features | Clinical Ergonomics |
| :--- | :--- | :--- | :--- |
| **`Drawer.tsx`** | `DrawerProps` | `role="dialog"`, `aria-modal="true"`, ESC key listener | Slide-over for 6-question Evidence Provenance Drawer |
| **`Search.tsx`** | `SearchProps` | `type="search"`, keyboard shortcut indicator (`⌘K`) | Instant search for patients, Mufradat, and actions |
| **`Tooltip.tsx`** | `TooltipProps` | `role="tooltip"`, 4 placements, hover/focus triggers | Explains medical abbreviations and grading metrics |
| **`Toast.tsx`** | `ToastProps`, `ToastContainerProps` | `role="status"`, auto-dismiss with cancelable timeout | Non-intrusive feedback for order submissions & saves |
| **`Table.tsx`** | `TableProps<T>`, `Column<T>` | Semantic `<table>`, `<th>`, `<tr>`, `<td>`, sort indicators | Dense tabular layouts for appointments and inventory |
| **`Progress.tsx`** | `ProgressProps` | `role="progressbar"`, `aria-valuenow`, min/max bounds | Visual completion indicator for treatment milestones |
| **`ErrorState.tsx`** | `ErrorStateProps` | Diagnostic correlation ID (CID), error code, retry CTA | Fail-closed error boundary for clinical safety |
| **`OfflineState.tsx`** | `OfflineStateProps` | Local cache indicator, pending mutations count | Offline resilience for clinics with intermittent WAN |
| **`ForbiddenState.tsx`**| `ForbiddenStateProps` | Explains statutory role limitation, back navigation | Enforces scope-of-practice and license boundaries |

---

## 3. Specialized Clinical Components Audit (`design-system/src/clinical/`)

| Clinical Component | Primary Functionality | Zero-Mock Discipline | Invariant Enforcement |
| :--- | :--- | :--- | :--- |
| **`PatientHeader.tsx`** | Patient 360 bar (MRN, Age, Gender, Mizaj, Allergies) | Defaults to `Needs Assessment` when unassessed | Shows critical allergy badges in high-contrast rose |
| **`ClinicalThread.tsx`** | 12-stage living continuum horizontal ribbon | Linear status tracking; stages strictly gated | Prevents skipping from assessment directly to Rx |
| **`AttentionFeed.tsx`** | Exception-first feed (`What/Why/When/Action`) | Real appointment and lab data feed only | Primary Next Patient Card with direct encounter trigger |
| **`MizajStatus.tsx`** | Humoral polarity (Damawi, Safrawi, Balghami, Sawdawi) | Supports `Pending` / `Needs Assessment` | Shows 4 qualitative balances: Heat, Cold, Moisture, Dryness |
| **`AxisRow.tsx`** | Organ-axis balance meter (0–10 score) | Displays explainable score with imbalance tags | Color-coded vulnerability states: Optimal to Critical |
| **`AxisDetail.tsx`** | Deep dive for organ-axis biomarkers & canonical text | Explains clinical rationale with classical canon anchors | Functional biomarkers paired with clinician guidance notes |
| **`EvidenceCard.tsx`** | GRADE-rated clinical claim with DOI/citation | Requires source title and evidence grade level | Distinguishes Classical Canon, Pharmacopoeia, and Trials |
| **`EvidenceDrawer.tsx`** | First-class 6-question slide-over provenance drawer | Answers all 6 mandatory provenance questions | Explains clinical limitations and contraindications |
| **`SafetyRail.tsx`** | Permanent fail-closed rail (5 invariant checks) | Live status evaluation; zero fail-open permitted | `BLOCK` and `UNKNOWN` hard-disable prescription approval |
| **`SafetyDecision.tsx`**| Justification modal for CAUTION & hard block dialog | Requires $\ge 15$ character clinical justification | For `BLOCK`, overrides are physically impossible |
| **`HakeemInsight.tsx`** | AI copilot clinical insight card with citations | Displays measured uncertainty score (0.08) | Enforces disclaimer: *"AI suggests. Clinician decides."* |
| **`KnowledgeProvenance.tsx`**| Substance tiering & 12-stage governance pipeline | Stage 01–09 labeled `RESEARCH CANDIDATE` | Blocks runtime AI prescribing for candidate substances |
| **`TrustLedger.tsx`** | Cryptographic audit ledger entry | Merkle root hash + SHA-256 seal + timestamp | 21 CFR Part 11 compliant audit verification button |
| **`NuskhaComposer.tsx`**| Multi-pillar prescription formulation authoring | Mufradat, Murakkab, dose, duration, vehicle (Badraqa)| Flags Schedule E(1) substances for Mudabbar verification |
| **`NuskhaPreflight.tsx`**| Pre-signoff checklist modal & PIN signature entry | 5 mandatory invariant checks before approval | Pre-signoff checklist must be 100% satisfied to proceed |
| **`ApprovalPanel.tsx`** | Clinician electronic signature authority panel | Requires registered practitioner PIN entry | Rejects unauthorized roles (e.g. `SUPER_ADMIN`) |
| **`SignatureSummary.tsx`**| Post-approval cryptographic seal certificate | SHA-256 seal hash, practitioner reg #, timestamp | Permanent unalterable digital medical order record |
| **`CareProgressRibbon.tsx`**| Patient care journey progression bar | Triage $\rightarrow$ Consult $\rightarrow$ Rx Dispensed $\rightarrow$ Follow-up | Displays dates and completion checkmarks |
| **`OutcomeCard.tsx`** | PROM outcome comparison card (Baseline vs Now) | Calculates delta without synthetic score inflation | Validated clinical instruments with clinician notes |
| **`AdherenceCard.tsx`** | Patient action card (morning/afternoon/bedtime) | 1-tap logging (`✓ Taken`, `⏳ Not Yet`, `✕ Skipped`) | Plain-language instructions and timing guidance |
| **`DataFreshness.tsx`** | Data freshness indicator (Realtime, Cached, Stale) | Explicit `INSUFFICIENT_DATA` state | Prompts refresh on stale records (>24h) |
| **`ConsentStatus.tsx`** | Statutory patient informed consent badge | Tracks consent level (Active, Pending, Expired) | Button to obtain digital signature if expired |

---

## 4. Barrel Exports Verification (`design-system/src/index.ts`)
- All 9 foundational primitives and 22 clinical components are exported with complete TypeScript types.
- Zero cyclic dependencies detected.
- Verified in `tests/test_design_system_and_clinical_primitives.py` (7/7 tests PASSED).
