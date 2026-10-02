# ZAYVORA Health OS™ — MASTER IMPLEMENTATION PLAN
## Phase 1 → Phase 8 Execution Roadmap
**Document Date:** September 15, 2026  
**Based On:** Phase 0 Full Repository Audit  
**Status:** APPROVED FOR EXECUTION

---

## Phase 1 — Critical Blocker Resolution & Design System Consolidation
**Goal:** Zero P0 blockers. Real auth tokens everywhere. Brand names corrected.  
**Estimated Effort:** 3–5 days

### 1.1 Fix P0 Security Blockers

| Task | File | Change |
|---|---|---|
| Replace `SESSION_MOCK_TOKEN` | `HakeemReviewDrawer.tsx:698`, `NuskhaBuilder.tsx:949` | Use `authService.getToken()` via React context |
| Fix hardcoded patient | `app/doctor/page.tsx:43` | Fetch patient list from `/api/v1/patients` on load |
| Fix hardcoded encounter | `app/doctor/page.tsx:108` | Create encounter dynamically on workspace open |
| Replace hardcoded API URLs | All `.tsx` with `http://localhost:8000` | Use `process.env.NEXT_PUBLIC_GATEWAY_URL` |
| Add `lang="en"` | `apps/web/app/layout.tsx` | Root HTML element |
| Enforce MFA on clinical login | `services/identity/app/routers/auth.py` | Add TOTP verification step for clinical roles |

### 1.2 Brand Name Corrections

| From | To | Files |
|---|---|---|
| "Hakeem Sahab" | "Hakeem Sahab AI™" | All UI components, page titles |
| "Knowledge Service" | "ZAYVORA Knowledge Intelligence™" | `/knowledge` page |
| "Clinical AI" | "Hakeem Sahab AI™" | AI-related UI |
| "Clinic" / "Matab" | "ZAYVORA Matab™" | Clinic route, booking |
| "Health OS" | "ZAYVORA Health OS™" | Header, meta tags |

### 1.3 Design System Integration
- Wire `design-system/` components into all pages (replace ad-hoc Tailwind)
- Add Toast/notification system globally
- Implement global loading indicator (route transitions)
- Standardize error message display (no raw API errors to users)

---

## Phase 2 — Public Website Completion
**Goal:** Full public website — booking, cart/checkout, contact all functional  
**Estimated Effort:** 3–4 days

| Task | Detail |
|---|---|
| Wire `/website/book` to clinical appointments API | Create appointment on submit, send confirmation SMS/email |
| Wire `/website/cart` to Stripe | `stripe_client.py` already exists — connect checkout flow |
| Wire `/website/contact` to notifications service | Send email via `notifications_client.py` |
| Add SEO meta tags + schema.org | Healthcare provider schema on all pages |
| Add GDPR cookie consent banner | Before any analytics or tracking |
| CMS → Database migration path | Plan how to move `programsData.ts` etc. to proper CMS/DB |
| Add `care-system` page to website nav | Not currently in nav menu |

---

## Phase 3 — Core Healthcare Workflows
**Goal:** Doctor, Receptionist, Pharmacy fully operational end-to-end  
**Estimated Effort:** 5–7 days

### 3.1 Doctor Workspace
- Patient queue sidebar with API-loaded patient list
- Dynamic encounter creation on workspace open
- Wire "Mizaj" tab to `mizaj_assessor.py` engine output
- Wire "Afaal" tab to `afaal_cascade_engine.py` output
- Wire "Axis" tab to `organ_axis_engine.py` output
- Wire "Assessment" tab to `differential_engine.py` output
- Real-time clinical notes auto-save (debounced API calls)
- Prescription PDF generation (server-side)
- Add `/doctor/[patient-id]` dynamic route

### 3.2 Receptionist Workspace
- Patient registration form → identity + clinical APIs
- Live queue management (WebSocket)
- Appointment scheduling with conflict detection
- Walk-in vs. pre-booked flow
- Add `/receptionist/queue` and `/receptionist/appointments` sub-routes

### 3.3 Pharmacy Workspace
- Safety Firewall error display (clear clinical language)
- FEFO expiry warnings in inventory
- QR/barcode prescription scan
- Add `/pharmacy/inventory` and `/pharmacy/dispensing` sub-routes

---

## Phase 4 — Intelligence Layer Full Activation
**Goal:** Hakeem Sahab AI™, ZAPE, Multimodal all fully operational  
**Estimated Effort:** 3–4 days

| Task | Detail |
|---|---|
| Connect Hakeem Sahab AI™ with real auth | Replace mock token, test 5-layer advisory |
| Remove `NEXT_PUBLIC_DEMO_MODE` fallback | `multimodalApi.ts` — real API only |
| Expose ZAPE personalization in doctor UI | Show personalized reasoning explanation |
| Connect Pharmacovigilance to doctor workspace | Surface adverse event warnings |
| Wire Digital Twin Cockpit fully | Connect all engine outputs to `DigitalTwinCockpit.tsx` |
| Knowledge portal full connection | Wire `/knowledge` page to knowledge service RAG |
| AI evaluation dashboard | Surface AI accuracy scores in admin |

---

## Phase 5 — Enterprise Modules
**Goal:** Research, Manufacturing, Knowledge Management fully operational  
**Estimated Effort:** 4–5 days

| Task | Detail |
|---|---|
| Research portal (`/research`) | Wire to `clinical/app/research/` backend |
| Manufacturing portal (`/manufacturing`) | Wire to `therapeutic/app/logistics/` + `courier_engine.py` |
| Enterprise admin (`/admin/billing`) | Multi-org billing management |
| Multi-tenant management (`/admin/tenancy`) | Org creation, quota management |
| Knowledge ingestion pipeline | Upload + OCR + Neo4j ingest workflow |
| GDPR export + erasure endpoints | Implement `GET/DELETE /api/v1/gdpr-export|erase` |
| e-Mudhra/Aadhaar eSign bridge | Legal digital signature for Indian context |

---

## Phase 6 — Mobile App Completion
**Goal:** Full patient + clinician mobile experience  
**Estimated Effort:** 4–5 days

| Task | Detail |
|---|---|
| Push notifications | Expo Push + FCM/APNs in `notifications_client.py` |
| Deep linking | Configure Expo Linking + React Navigation |
| Biometric auth | Expo LocalAuthentication |
| `AIChatScreen` | Hakeem Sahab AI™ mobile chat |
| `MizajAssessmentScreen` | Mobile Mizaj self-assessment |
| `BookAppointmentScreen` | Full booking flow |
| `VitalEntryScreen` | Manual vital entry |
| `EmergencyScreen` | Red flag detection + emergency protocols |
| Teleconsult video | WebRTC via Daily.co Expo SDK |
| Wearable sync | Apple HealthKit + Google Fit |
| Offline prescription caching | Extend `OfflineStorageService.ts` |
| RTL / Urdu language support | i18n + RTL layout |
| EAS Build configuration | App signing for App Store + Play Store |

---

## Phase 7 — Hardening, Security & Compliance
**Goal:** Production-grade security, full compliance, performance  
**Estimated Effort:** 4–5 days

| Task | Detail |
|---|---|
| mTLS inter-service communication | Kubernetes network policy + TLS certs |
| RabbitMQ/NATS event bus | Replace in-memory queue, wire durable async tasks |
| Account lockout brute-force protection | `failed_login_attempts` + `locked_until` |
| Automated JWT key rotation | Scheduled key rotation daemon |
| GDPR consent table | `consent_records` — type, granted_at, withdrawn_at |
| PHI encryption coverage audit | All patient PII fields verified AES-GCM |
| CSP + Security headers full audit | Strict CSP via Next.js middleware |
| WAF configuration | Cloudflare rules / Nginx ModSecurity |
| Trivy scan as blocking CI gate | Currently non-blocking — must block on HIGH/CRITICAL |
| Load testing | k6 stress tests on all critical paths |
| Accessibility full audit | WCAG 2.1 AA compliance |
| HIPAA documentation | Complete Business Associate Agreements |
| GDPR DPA documentation | Data Processing Agreements |

---

## Phase 8 — Pilot Readiness
**Goal:** Ready for first closed pilot with ZAYVORA Matab™ clinic  
**Estimated Effort:** 2–3 days

| Task | Detail |
|---|---|
| Staging environment deployment | Docker Compose on VPS or cloud VM |
| Seed data for pilot clinic | Realistic Unani clinical data |
| Staff onboarding documentation | Hakeem training guide, pharmacist guide |
| Runbook + incident response | Escalation paths, rollback procedure |
| Monitoring + alerting | Prometheus + Grafana dashboards |
| Final go/no-go checklist | 0 P0 blockers verified by QA |
| Pilot clinic user accounts | Create org + staff + test patients |
| 72-hour soak test | Simulated clinical load before go-live |

---

## Recommended Implementation Sequence

```
Week 1:  Phase 1 (blockers) → Phase 2 (website)
Week 2:  Phase 3 (healthcare workflows)
Week 3:  Phase 4 (intelligence) → Phase 5 (enterprise)
Week 4:  Phase 6 (mobile)
Week 5:  Phase 7 (hardening)
Week 6:  Phase 8 (pilot)
```

---

## Success Criteria

| Criterion | Metric |
|---|---|
| Zero P0 blockers | 0/6 remaining |
| Real auth everywhere | `SESSION_MOCK_TOKEN` count = 0 |
| API connection coverage | ≥ 90% of UI actions have real backend |
| Test coverage | ≥ 80% on critical clinical paths |
| WCAG 2.1 AA | 0 Level A violations |
| Security scan | 0 HIGH/CRITICAL CVEs in container images |
| Load test | P95 response time < 500ms at 100 concurrent users |
| Brand consistency | All brand names match canonical names (100%) |
