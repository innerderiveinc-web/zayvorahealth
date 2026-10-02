# ZAYVORA Health OS™ — PRODUCTION BLOCKER MATRIX
**Audit Date:** September 15, 2026  
**Gate Standard:** Must reach zero P0 blockers before first patient encounter.

---

## P0 — CRITICAL BLOCKERS (Zero Tolerance)
*Must be 100% resolved before any patient encounter or prescription is processed.*

| ID | Blocker | Affected Area | Current State | Fix Required |
|---|---|---|---|---|
| **P0-01** | `SESSION_MOCK_TOKEN` in AI advisory path — prescriptions unsigned | `HakeemReviewDrawer.tsx`, `NuskhaBuilder.tsx` | Hardcoded mock token — no real doctor identity attached to prescription recommendations | Replace with `authService.getToken()` + React auth context |
| **P0-02** | Doctor workspace always loads `DEFAULT_PATIENT` (Hamza Farooqi) — no real patient selection | `app/doctor/page.tsx` | Any doctor opening the workspace would see a demo patient, not their real patient list | Implement patient queue API fetch on workspace load |
| **P0-03** | Encounter ID hardcoded as `ENC-001` — sign action could affect wrong encounter | `app/doctor/page.tsx:108` | Sign action POSTs to `/encounters/ENC-001/sign` regardless of active encounter | Dynamically create encounter on workspace open, use real encounter ID |
| **P0-04** | MFA not enforced for clinical staff login | `services/identity/app/routers/auth.py` | `mfa.py` exists but login flow does not require TOTP step for clinical roles | Add `mfa_required` check in auth router for `role in [hakeem, pharmacist, nurse]` |
| **P0-05** | API calls use `http://` (unencrypted) hardcoded to localhost | `app/doctor/page.tsx`, `app/pharmacy/page.tsx` | Will transmit PHI in plaintext — unacceptable for any deployment beyond a laptop | All API calls must use `NEXT_PUBLIC_GATEWAY_URL` env var + TLS in production |
| **P0-06** | `lang` attribute missing from `<html>` element | `apps/web/app/layout.tsx` | Screen readers and accessibility tools cannot function correctly | Add `lang="en"` to root layout |

---

## P1 — HIGH PRIORITY (Required Before Expanding to Multi-Clinic)

| ID | Blocker | Current State | Fix |
|---|---|---|---|
| **P1-01** | Receptionist workspace — zero backend connections | All actions are UI-only | Wire 6 core workflows: patient registration, queue, appointments to APIs |
| **P1-02** | Knowledge/Research/Manufacturing portals — zero API connections | Frontend-only pages | Connect all 3 portals to their respective backend services |
| **P1-03** | GDPR data export endpoint missing | Endpoint does not exist | Implement `GET /api/v1/gdpr-export` |
| **P1-04** | GDPR data erasure endpoint missing | Endpoint does not exist | Implement `DELETE /api/v1/gdpr-erase` with cascade anonymization |
| **P1-05** | No GDPR consent capture before PHI collection | No consent table, no consent flow | Add `consent_records` table + consent gate on patient registration |
| **P1-06** | Public website booking form has no backend | `/website/book/` submits to nothing | Wire to clinical appointments API |
| **P1-07** | Public website cart has no Stripe integration | `/website/cart/` — no payment processing | Wire to Stripe payment intent + webhook |
| **P1-08** | Mobile app missing push notifications | No FCM/APNs integration | Expo Push + FCM backend in notifications service |
| **P1-09** | mTLS inter-service communication not configured | Plain HTTP between services in cluster | Configure TLS certs + mutual auth in Kubernetes network policies |
| **P1-10** | In-memory task queue — data lost on restart | `clinical/app/workers/` uses in-memory queue | Migrate to Celery + Redis or NATS event bus |
| **P1-11** | No account lockout on failed logins | No brute-force protection on auth | Add `failed_login_attempts` + `locked_until` to user model |
| **P1-12** | Doctor workspace "Afaal/Axis/Assessment" tabs not wired to engines | Tabs navigate to empty UI | Connect tab content to organ_axis, afaal_cascade, differential engine APIs |

---

## P2 — MEDIUM PRIORITY (Pre-Commercial GA)

| ID | Blocker | Fix |
|---|---|---|
| **P2-01** | Prescription PDF generation not implemented | Server-side PDF via WeasyPrint or Playwright |
| **P2-02** | No automated JWT key rotation | Scheduled key rotation daemon |
| **P2-03** | No cookie consent banner on website | GDPR-compliant consent manager |
| **P2-04** | Contact form not wired to email | Wire to `notifications_client.py` |
| **P2-05** | No SEO meta tags / schema.org on website | Add healthcare structured data |
| **P2-06** | Mobile teleconsult screen has no video | WebRTC via Jitsi/Daily.co |
| **P2-07** | No QR barcode scan for pharmacy prescription | Expo Camera + QR decoder |
| **P2-08** | PHI encryption coverage audit needed | Verify AES-GCM on all patient PII fields |
| **P2-09** | BYOK encryption not implemented | AWS KMS / Azure Key Vault integration |
| **P2-10** | Blockchain Merkle root anchoring not implemented | Periodic anchor to public blockchain |
| **P2-11** | Content Security Policy (CSP) headers not set | Next.js middleware CSP configuration |

---

## Blocker Resolution Sequence

```
Phase 1: P0-01 through P0-06 (all critical blockers)
         ↓
Phase 2: Design system consolidation + brand name corrections
         ↓
Phase 3: P1-01 through P1-06 (core workflow connections)
         ↓
Phase 4: P1-07 through P1-12 (security + mobile + infrastructure)
         ↓
Phase 5: P2 items (commercial-grade polish)
         ↓
Phase 6: External audit + pilot readiness review
```

---

## Summary Scorecard

| Priority | Total Blockers | Resolved (Pre-Phase 1) | Remaining |
|---|---|---|---|
| P0 | 6 | 0 | **6** |
| P1 | 12 | 0 | **12** |
| P2 | 11 | 0 | **11** |
| **Total** | **29** | **0** | **29** |
