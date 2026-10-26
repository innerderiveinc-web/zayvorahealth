# ZAYVORA Health OS™ — UI/UX & Design System Audit
**Document ID**: `AUDIT-UI-08`  
**Target**: ZAYVORA Design System & Accessibility  
**Standard**: WCAG 2.1 AA, Clinical Ergonomics, Multilingual Support  

---

## 1. Design Token Specifications

| Token Category | Specification & Value | Clinical Rationale |
|---|---|---|
| **Primary Palette** | Deep Emerald (`#065f46`), Gold-Soft (`#d97706`), Forest (`#047857`) | Evokes botanical heritage, healing, trust, and precision. |
| **Neutral Palette** | Slate-900 (`#0f172a`), Slate-100 (`#f1f5f9`), White (`#ffffff`) | High-contrast clinical readability, prevents visual fatigue. |
| **Semantic Alerts** | Success Green (`#10b981`), Warning Amber (`#f59e0b`), Danger Red (`#ef4444`) | Immediate triaging of safety firewall results and red flags. |
| **Typography** | Inter, Plus Jakarta Sans, Arabic/Urdu Noto Nastaliq | Clean tabular numbers for vitals; native RTL font for Urdu. |
| **Border Radius** | `0.75rem` (12px) for cards, `0.5rem` (8px) for buttons/inputs | Calm, human, modern enterprise software feel. |

---

## 2. Accessibility & Usability Verifications
- **Contrast Ratios**: All text elements exceed WCAG AA 4.5:1 ratio against backgrounds.
- **Keyboard Navigation**: Full tab ordering, focus rings (`focus:ring-2 focus:ring-emerald-500`), and escape key handlers on all modals.
- **Screen Reader Support**: Comprehensive ARIA attributes (`aria-expanded`, `aria-haspopup`, `aria-live="polite"`).
- **Multilingual RTL Architecture**: CSS logical properties (`margin-inline-start`) to support native Urdu rendering without layout breakage.
