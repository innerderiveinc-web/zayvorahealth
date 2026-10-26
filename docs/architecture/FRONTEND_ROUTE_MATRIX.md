# ZAYVORA Health OS™ — FRONTEND ROUTE MATRIX
**Audit Date:** September 15, 2026 | **Framework:** Next.js 14 App Router

---

## Legend
- ✅ Connected to real API  🟡 Partially connected  🔴 Mocked/hardcoded  🔵 Frontend-only  ❌ Missing

---

## App Routes (`apps/web/app/`)

| Route | File | Size (lines) | API Status | Backend Endpoint | Priority Fix |
|---|---|---|---|---|---|
| `/` | `page.tsx` | 575 | 🔵 Static | None | Low |
| `/signup` | `page.tsx` | — | 🔴 Mocked | None | P1 |
| `/settings` | `page.tsx` | 393 | 🔴 Mocked | None | P2 |
| `/dashboard` | `page.tsx` | 931 | 🔴 Mocked | None | P1 |
| `/doctor` | `page.tsx` | 957 | 🔴 Hardcoded patient | `gateway:8000/api/v1/*` (partial) | **P0** |
| `/patient` | `page.tsx` | 1222 | 🟡 3 endpoints wired | `gateway:8000/api/v1/billing,patients,appointments` | P1 |
| `/patient/login` | `page.tsx` | 242 | ✅ Connected | `identity:8001/auth/login` | — |
| `/patient/register` | `page.tsx` | 181 | ✅ Connected | `identity:8001/auth/register` | — |
| `/patient/forgot-password` | `page.tsx` | — | ✅ Connected | `identity:8001/auth/forgot-password` | — |
| `/patient/reset-password` | `page.tsx` | — | ✅ Connected | `identity:8001/auth/reset-password` | — |
| `/receptionist` | `page.tsx` | 798 | 🔵 Zero API calls | None | **P0** |
| `/pharmacy` | `page.tsx` | 765 | 🟡 4 endpoints | `gateway:8000/api/v1/prescriptions,inventory` | P1 |
| `/clinic` | `page.tsx` | 421 | 🔵 Zero API calls | None | P1 |
| `/ai` | `page.tsx` | 308 | 🟡 Demo fallback | `ai:8005` via `hakeemApi.ts` | P1 |
| `/knowledge` | `page.tsx` | 272 | 🔵 Zero API calls | None | **P0** |
| `/research` | `page.tsx` | 254 | 🔵 Zero API calls | None | P1 |
| `/manufacturing` | `page.tsx` | 221 | 🔵 Zero API calls | None | P1 |
| `/maintenance` | `page.tsx` | — | 🔵 Static | None | Low |
| `/admin` | `page.tsx` | 88 | ✅ Connected | `gateway:8000/health` | — |
| `/admin/dashboard` | `page.tsx` | — | ✅ Connected | `gateway:8000` service health | — |
| `/admin/users` | `page.tsx` | — | ✅ Connected | `identity:8001/users` | — |
| `/admin/audit` | `page.tsx` | — | ✅ Connected | `clinical:8002/audit` | — |
| `/admin/health` | `page.tsx` | — | ✅ Connected | All services health probes | — |

---

## Website Routes (`apps/web/app/website/`)

| Route | File | API Status | CMS / Backend | Priority |
|---|---|---|---|---|
| `/website` | `page.tsx` | ✅ CMS-driven | `programsData.ts`, `productsData.ts` | — |
| `/website/about` | `page.tsx` | ✅ Static | None | — |
| `/website/philosophy` | `page.tsx` | ✅ Static | None | — |
| `/website/modern-unani` | `page.tsx` | ✅ Static | None | — |
| `/website/care-journey` | `page.tsx` | ✅ Static | None | — |
| `/website/care-system` | `page.tsx` | ✅ Static | None | — |
| `/website/programs` | `page.tsx` | ✅ CMS | `programsData.ts` | — |
| `/website/program` | `page.tsx` | ✅ CMS | `programsData.ts` | — |
| `/website/herbals` | `page.tsx` | ✅ CMS | `productsData.ts` | — |
| `/website/product` | `page.tsx` | ✅ CMS | `productsData.ts` | — |
| `/website/doctors` | `page.tsx` | ✅ CMS | `doctorsData.ts` | — |
| `/website/doctor` | `page.tsx` | ✅ CMS | `doctorsData.ts` | — |
| `/website/clinics` | `page.tsx` | ✅ Static | None | — |
| `/website/matab` | `page.tsx` | ✅ Static | None | — |
| `/website/knowledge-centre` | `page.tsx` | ✅ CMS | `articlesData.ts` | — |
| `/website/blog` | `page.tsx` | ✅ CMS | `articlesData.ts` | — |
| `/website/article` | `page.tsx` | ✅ CMS | `articlesData.ts` | — |
| `/website/book` | `page.tsx` | 🔵 No backend | Should call clinical booking API | **P0** |
| `/website/cart` | `page.tsx` | 🔵 No backend | Should call Stripe/order API | P1 |
| `/website/conditions` | `page.tsx` | ✅ Static | None | — |
| `/website/research` | `page.tsx` | ✅ Static | None | — |
| `/website/portfolio` | `page.tsx` | ✅ Static | None | — |
| `/website/faqs` | `page.tsx` | ✅ CMS | `faqsData.ts` | — |
| `/website/contact` | `page.tsx` | 🔵 No backend | Should send email via notifications | P1 |
| `/website/careers` | `page.tsx` | ✅ Static | None | — |
| `/website/partner` | `page.tsx` | 🔵 No backend | None | P2 |
| `/website/privacy` | `page.tsx` | ✅ Static | None | — |
| `/website/terms` | `page.tsx` | ✅ Static | None | — |
| `/website/medical-disclaimer` | `page.tsx` | ✅ Static | None | — |
| `/website/refund-policy` | `page.tsx` | ✅ Static | None | — |
| `/website/shipping-policy` | `page.tsx` | ✅ Static | None | — |
| `/website/shipping-refunds` | `page.tsx` | ✅ Static | None | — |
| `/website/accessibility` | `page.tsx` | ✅ Static | None | — |

---

## Missing Routes (Required by Master Directive)

| Required Route | Status | Phase to Build |
|---|---|---|
| `/doctor/[patient-id]` | ❌ Missing | Phase 3 |
| `/doctor/schedule` | ❌ Missing | Phase 3 |
| `/patient/[id]/timeline` | ❌ Missing | Phase 3 |
| `/pharmacy/inventory` | ❌ Missing | Phase 3 |
| `/pharmacy/dispensing` | ❌ Missing | Phase 3 |
| `/receptionist/queue` | ❌ Missing | Phase 3 |
| `/receptionist/appointments` | ❌ Missing | Phase 3 |
| `/admin/billing` | ❌ Missing | Phase 5 |
| `/admin/tenancy` | ❌ Missing | Phase 5 |
| `/research/trials` | ❌ Missing | Phase 5 |
| `/manufacturing/batch` | ❌ Missing | Phase 5 |

---

## Component Inventory

| Component | Size | Purpose | API-Connected |
|---|---|---|---|
| `AppShell.tsx` | — | Authenticated layout shell | — |
| `NuskhaBuilder.tsx` | 30KB | Prescription builder | 🔴 SESSION_MOCK_TOKEN |
| `HakeemReviewDrawer.tsx` | 19KB | AI advisory panel | 🔴 SESSION_MOCK_TOKEN |
| `PatientPortalCockpit.tsx` | 16KB | Patient dashboard widget | 🟡 Partial |
| `MultimodalLabCockpit.tsx` | 17KB | Lab AI analysis | ⚫ Demo mode |
| `MizajAssessmentModal.tsx` | 12KB | Mizaj assessment form | 🟡 Partial |
| `DigitalTwinCockpit.tsx` | — | Patient digital twin viz | 🟡 FHIR-connected |
| `GovernanceBoardCockpit.tsx` | — | Clinical governance | 🟡 Partial |
| `AmbientScribeGovernanceCockpit.tsx` | — | Scribe AI + governance | 🟡 Partial |
| `PatientTimeline.tsx` | — | Clinical timeline | 🟡 Partial |
| `TaskPipelineCockpit.tsx` | — | Clinical task queue | 🟡 Partial |
| `GlobalCommandPalette.tsx` | — | Keyboard command palette | 🔵 UI only |
| `PlatformHeader.tsx` | — | Authenticated header | — |
| `PlatformFooter.tsx` | — | Authenticated footer | — |
| `PublicHeader.tsx` | — | Website header | — |
| `PublicFooter.tsx` | — | Website footer | — |

### Shell Components (`components/shells/`)
| Shell | Purpose |
|---|---|
| `AdminShell.tsx` | Admin console layout |
| `DoctorShell.tsx` | Doctor workspace layout |
| `PatientShell.tsx` | Patient portal layout |
| `PharmacistShell.tsx` | Pharmacy layout |
| `ReceptionistShell.tsx` | Receptionist layout |
| `PublicWebsiteShell.tsx` | Public marketing layout |
| `EnterpriseOwnerShell.tsx` | Enterprise admin layout |
| `ResearcherShell.tsx` | Research portal layout |
