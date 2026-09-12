# ZAYVORA HEALTH OS v5.0 — ENTERPRISE CLINICAL DESIGN SYSTEM
**Document ID**: `ZAY-DOC-V5-DS-01`  
**Version**: Design System v5.0  
**Classification**: Enterprise UI/UX Standard  

---

## 1. DESIGN PHILOSOPHY

The ZAYVORA Design System v5.0 provides a distraction-free, high-contrast, clinical-grade interface for high-stakes healthcare workflows. It balances classical Unani heritage with contemporary biomedical informatics.

---

## 2. COLOR TOKEN SYSTEM

### 2.1 Foundation Tokens (Navy & Slate)
| Token | Hex | Role |
|:---|:---|:---|
| `--color-bg-base` | `#0A0F1D` | Deep canvas background |
| `--color-bg-surface` | `#0F172A` | Primary container / AppShell background |
| `--color-bg-card` | `#1E293B` | Interactive cards, modal dialogs, data tables |
| `--color-bg-elevated`| `#334155` | Elevated tooltips, dropdowns, hovered items |
| `--color-border-subtle` | `#1E293B` | Structural dividers |
| `--color-border-default`| `#334155` | Card borders, table grid lines |
| `--color-border-focus` | `#0D9488` | Keyboard focus ring |

### 2.2 Semantic & Clinical Accent Tokens
| Token | Hex | Clinical Usage |
|:---|:---|:---|
| `--color-primary` | `#0D9488` | Primary clinical actions, active tabs |
| `--color-primary-light` | `#14B8A6` | Interactive hover states |
| `--color-success` | `#10B981` | Safe, verified, Mudabbar certified, locked |
| `--color-warning` | `#F59E0B` | Pending review, dosage warning, precaution |
| `--color-danger` | `#EF4444` | Clinical hold, toxic botanical, contraindication |
| `--color-info` | `#3B82F6` | General clinical information, standard vitals |
| `--color-research` | `#8B5CF6` | Clinical research cohorts, trial protocols |

---

## 3. TYPOGRAPHY & DATA DENSITY

- **Clinical Body**: System font stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`) with tabular numbers (`font-variant-numeric: tabular-nums`) for vitals and lab values.
- **Hierarchy**:
  - Page Title: `24px / 32px`, font-weight 700.
  - Section Header: `16px / 24px`, font-weight 600, uppercase tracking.
  - Body Text: `14px / 20px`, font-weight 400.
  - Micro / Meta: `12px / 16px`, font-weight 500.

---

## 4. STANDARD COMPONENT INVENTORY

1. **`AppShell`**: Responsive container with header, role navigation sidebar, and main view.
2. **`TopHeader`**: Facility selector, role indicator, active user profile, alert badge.
3. **`Breadcrumbs`**: Contextual path hierarchy (`Clinic > Doctor > Consultation`).
4. **`StatCard`**: Compact clinical KPI cards with status accents.
5. **`DataTable`**: Dense clinical records table with sort, filter, empty, and loading states.
6. **`StatusBadge`**: Pill badges for prescription, appointment, and batch statuses.
7. **`ConfirmDialog`**: Mandatory two-step confirmation for destructive clinical actions.
8. **`HakeemReviewDrawer`**: Side drawer for AI clinical reasoning with mandatory human doctor sign-off.
9. **`ApprovalBanner`**: Non-delegable clinician signature and Mudabbar status banner.

---
**Approved By**: Clinical UX Director, ZAYVORA HEALTH OS™
