# ZAYVORA Health OS™ — Centralized Design System Documentation

## 1. Design Philosophy & Aesthetic Core
ZAYVORA Health OS™ marries **ancient healing wisdom with modern evidence-based clinical rigor**. The visual system reflects this convergence:
- **Calm & Reassuring**: Soothing forest greens and alabaster creams reduce clinical anxiety for patients.
- **High-Density Clinical Efficiency**: Precise spacing, high-contrast badges, and low-cognitive-load layouts empower practitioners during rapid OPD encounters.
- **Trustworthy & Transparent**: Clear status signifiers, explicit consent notices, and visible 21 CFR Part 11 seals.

---

## 2. Foundations & Design Tokens

### Brand Palette
| Token | Value | Semantic Role | Usage |
| :--- | :--- | :--- | :--- |
| `--color-brand-primary` | `#2D6A4F` | Unani Forest Green | Primary actions, brand headers, active tab indicators |
| `--color-brand-secondary` | `#1B4332` | Deep Anatolian Teal | Structural borders, secondary surfaces, active states |
| `--color-brand-accent` | `#F4A261` | Warm Herbal Gold | Key focus rings, badges, special callouts, review buttons |
| `--color-bg-base` (Light) | `#FAFAF7` | Warm Alabaster Cream | Public website, patient portal, consumer forms |
| `--color-bg-base` (Dark) | `#0A0F1D` | Obsidian Deep Navy | Doctor cockpit, surgical/OPD ambient viewing |
| `--color-text` (Light) | `#1A1A1A` | Charcoal Black | Primary text on cream/white surfaces |
| `--color-text` (Dark) | `#F8FAFC` | Crisp White | Primary text on dark obsidian surfaces |

### Status Colors (WCAG 2.2 AA Compliant)
- **Success / Normal**: `#2D6A4F` (Light: `rgba(45, 106, 79, 0.16)`)
- **Warning / Moderate**: `#D97706` (Light: `rgba(217, 119, 6, 0.16)`)
- **Danger / Critical**: `#DC2626` (Light: `rgba(220, 38, 38, 0.16)`)
- **Info / Ongoing**: `#2563EB` (Light: `rgba(37, 99, 235, 0.16)`)
- **Research / Genomic**: `#7C3AED` (Light: `rgba(124, 58, 237, 0.16)`)

### Typography Scale
- **Display Typeface**: `'Amiri', Georgia, serif` (Evokes classical Unani treatises, elegant Arabic/Urdu ligature support).
- **Body & Interface**: `'Inter', system-ui, -apple-system, sans-serif` (Optimal legibility on high-DPI screens and mobile viewports).

---

## 3. Component Library Inventory

All components are centralized in `design-system/src/components/` and re-exported from `design-system`:

### Primitive Components
- **`Button`**: Supports `primary`, `secondary`, `accent`, `ghost`, and `danger` variants with loading spinner, icon slot, and disabled states.
- **`Card`**: Structured container with customizable header, body, footer, and interactive hover elevation.
- **`Badge`**: Status signifiers supporting `success`, `warning`, `error`, `info`, `gold`, and `neutral`.
- **`Input` & `Textarea`**: Accessible text entry with floating/static labels, validation error text, and keyboard focus rings.
- **`Select`**: Accessible dropdown selector with grouped options.
- **`Modal` & `ConfirmationDialog`**: Focus-trapped dialogs with accessible backdrop and keyboard `Escape` dismissal.
- **`Tabs`**: ARIA-compliant tabbed navigation for complex clinical views.
- **`Alert`**: Inline dismissible callout for clinical red flags, system warnings, and success notices.
- **`LoadingSkeleton`**: Animated placeholder reducing cumulative layout shift during API fetching.
- **`EmptyState`**: Human-centered placeholder explaining missing data with a clear action button.
- **`Breadcrumb`**: Hierarchical pathway navigation for nested clinical modules.
- **`Stepper`**: Multi-stage progress indicator for patient onboarding and consultation flows.
- **`Timeline`**: Chronological event tracker for patient medical history and audit trails.
- **`Avatar`**: User initials or image with online status indicator.
- **`Switch`**: Accessible toggle switch for preferences and feature flags.

### Specialized Clinical Components
- **`ClinicalStatus`**: Formats classical Unani Mizaj temperaments (Damawi, Safrawi, Balghami, Sawdawi, Motadil) and clinical acuity (CRITICAL, URGENT, STANDARD).
- **`PrescriptionItem`**: Renders classical Nuskha items with Schedule E(1) warnings, posology instructions, and Mudabbar purification certificates.
- **`AppointmentItem`**: Displays OPD queue appointments with token numbers, doctor/patient information, consultation mode (OPD / Video), and reschedule/cancel actions.
