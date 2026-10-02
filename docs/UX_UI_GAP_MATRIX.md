# ZAYVORA Health OS™ — UX/UI GAP MATRIX
**Audit Date:** September 15, 2026

---

## 1. Design System Status

| Component | Location | Status |
|---|---|---|
| Brand tokens (colors, typography) | `design-system/tokens.css` | ✅ Implemented — #2D6A4F primary, #1B4332 secondary, #F4A261 accent |
| Tailwind config | `design-system/tailwind.config.js` | ✅ |
| Button component | `design-system/components/Button.tsx` | ✅ |
| Card component | `design-system/components/Card.tsx` | ✅ |
| Badge/StatusBadge | `design-system/components/Badge.tsx` + `components/StatusBadge.tsx` | ✅ |
| Input component | `design-system/components/Input.tsx` | ✅ |
| Modal component | `design-system/components/Modal.tsx` | ✅ |
| Spinner/Loading | `design-system/components/Spinner.tsx` + `components/ui/LoadingSpinner.tsx` | ✅ |
| DataTable | `components/ui/DataTable.tsx` | ✅ |
| PageHeader | `components/ui/PageHeader.tsx` | ✅ |
| EmptyState | `components/ui/EmptyState.tsx` | ✅ |
| Toast/Notification system | ❌ Not found | Missing |
| Form validation feedback | ❌ Not standardized | Missing |
| Error boundary | `components/ErrorBoundary.tsx` | ✅ |
| Command palette | `components/GlobalCommandPalette.tsx` | 🔵 UI exists, not fully wired |

---

## 2. UX Gaps by Portal

### Doctor Workspace (`/doctor`)
| Gap | Severity | Action |
|---|---|---|
| Patient must be hardcoded — no patient selection UI | Critical | Add patient search/select flow at workspace entry |
| No patient list sidebar to switch between patients | High | Implement patient queue sidebar |
| `SESSION_MOCK_TOKEN` — AI drawer never uses real auth | Critical | Replace with `authService.getToken()` |
| "Afaal", "Axis", "Assessment" tabs not wired | High | Connect to backend engine endpoints |
| Prescription print is UI-only (no PDF) | Medium | Server-side PDF generation (WeasyPrint/Playwright) |
| No unsaved-changes warning on navigation | Medium | Implement `beforeunload` guard |
| No keyboard shortcuts for power users | Low | Integrate `GlobalCommandPalette.tsx` |

### Patient Portal (`/patient`)
| Gap | Severity | Action |
|---|---|---|
| No real-time appointment status updates | Medium | WebSocket or SSE from clinical service |
| Lab results not linked to contextual AI explanation | High | Integrate Hakeem Sahab AI™ for lab interpretation |
| No e-consent flow | Critical (GDPR) | Implement consent recording before data capture |
| Telemedicine button present but no WebRTC | High | Implement video consultation |
| No medication adherence tracker | Medium | Connect to care plans + notifications |

### Receptionist (`/receptionist`)
| Gap | Severity | Action |
|---|---|---|
| Entire workspace is frontend-only | Critical | Wire all 6 key workflows to backend APIs |
| No live patient queue view | Critical | WebSocket queue management |
| No appointment conflict detection | High | Backend validation on schedule overlap |
| No walk-in registration form that saves to DB | Critical | Wire patient registration to identity + clinical APIs |

### Pharmacy (`/pharmacy`)
| Gap | Severity | Action |
|---|---|---|
| Safety firewall errors not displayed in UI | Critical | Show `MudabbarDispenseBlockError` clearly |
| No QR barcode scan for prescription input | High | Camera-based QR scan |
| Stock expiry alerts not shown | High | Surface FEFO warnings from inventory |
| No batch/LOT number tracking UI | Medium | Extend inventory display |

### Public Website
| Gap | Severity | Action |
|---|---|---|
| Booking form (`/website/book`) has no backend | Critical | Wire to clinical appointments API |
| Cart (`/website/cart`) has no Stripe integration | Critical | Wire to Stripe payment flow |
| Contact form not wired to email service | High | Wire to `notifications_client.py` |
| No SEO optimization (meta tags, structured data) | High | Add healthcare schema.org markup |
| No cookie consent banner | Critical (GDPR) | Implement before any analytics |

---

## 3. Brand Consistency Gaps

| Issue | Location | Fix |
|---|---|---|
| "Hakeem Sahab" without "AI™" suffix | Multiple components | Global replace → "Hakeem Sahab AI™" |
| "Knowledge Service" in UI | `/knowledge` page | Replace → "ZAYVORA Knowledge Intelligence™" |
| "Clinical AI" references | AI-related UI | Replace → "Hakeem Sahab AI™" |
| Clinic referred to as "Clinic" | `/clinic` route | Replace → "ZAYVORA Matab™" |
| No trademark ™/® marks in HTML meta | `layout.tsx` | Add to title/description |

---

## 4. Accessibility Gaps

| Gap | WCAG Level | Priority |
|---|---|---|
| No `aria-label` on icon-only buttons | A | P1 |
| Color contrast not verified against WCAG 2.1 AA | AA | P1 |
| No skip-navigation links | A | P1 |
| Form inputs missing associated `<label>` in some pages | A | P1 |
| No focus indicator styling | AA | P1 |
| No keyboard navigation for modal dialogs | A | P1 |
| Mobile: tap targets < 44px | A | P1 |
| No `lang` attribute on HTML element | A | P0 |
| No `alt` text audit on images | A | P1 |

---

## 5. Responsive Design Gaps

| Gap | Severity |
|---|---|
| Doctor workspace not mobile-responsive (13 tabs) | High |
| Patient portal not tablet-optimized | Medium |
| Admin console not mobile-friendly | Low |
| Website navigation menu on mobile | Medium (functional but needs audit) |

---

## 6. Loading & Error State Gaps

| Gap | Priority |
|---|---|
| No global loading indicator (route transitions) | P1 |
| No retry mechanism on API failure | P1 |
| No offline mode indicator on web | P2 |
| Error messages show raw API errors (not user-friendly) | P0 |
| No empty state illustrations for new users | P2 |
