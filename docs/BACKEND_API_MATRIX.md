# ZAYVORA Health OS™ — BACKEND API MATRIX
**Audit Date:** September 15, 2026 | **Services:** 6 FastAPI microservices

---

## Gateway (port 8000) — Reverse Proxy

| Endpoint Pattern | Routes To | Auth | Status |
|---|---|---|---|
| `/api/v1/auth/*` | identity:8001 | Public | ✅ |
| `/api/v1/users/*` | identity:8001 | JWT | ✅ |
| `/api/v1/patients/*` | clinical:8002 | JWT | ✅ |
| `/api/v1/encounters/*` | clinical:8002 | JWT | ✅ |
| `/api/v1/clinical-notes/*` | clinical:8002 | JWT | ✅ |
| `/api/v1/prescriptions/*` | therapeutic:8004 | JWT | ✅ |
| `/api/v1/inventory/*` | therapeutic:8004 | JWT | ✅ |
| `/api/v1/nuskha/*` | therapeutic:8004 | JWT | ✅ |
| `/api/v1/hakeem/*` | ai:8005 | JWT | ✅ |
| `/api/v1/knowledge/*` | knowledge:8003 | JWT | ✅ |
| `/api/v1/billing/*` | clinical:8002 | JWT | ✅ |
| `/api/v1/appointments/*` | clinical:8002 | JWT | ✅ |
| `/health` | All services | Public | ✅ |
| `/api/v1/gdpr-export` | identity:8001 | JWT+Admin | ❌ NOT IMPLEMENTED |
| `/api/v1/gdpr-erase` | identity:8001 | JWT+Admin | ❌ NOT IMPLEMENTED |

---

## Identity Service (port 8001)

### Authentication Router (`/api/v1/auth`)
| Method | Endpoint | Description | Status |
|---|---|---|---|
| POST | `/login` | Email+password login, returns JWT pair | ✅ |
| POST | `/register` | New user registration | ✅ |
| POST | `/refresh` | Rotate refresh token | ✅ |
| POST | `/logout` | Revoke JTI | ✅ |
| POST | `/forgot-password` | Send reset email | ✅ |
| POST | `/reset-password` | Consume token, set new password | ✅ |
| POST | `/mfa/setup` | Generate TOTP secret | ✅ |
| POST | `/mfa/verify` | Verify TOTP code | ✅ (not enforced on clinical logins) |
| GET | `/.well-known/jwks.json` | Public JWKS endpoint | ✅ |

### Tenancy Router (`/api/v1/tenancy`)
| Method | Endpoint | Description | Status |
|---|---|---|---|
| POST | `/organizations` | Create new organization | ✅ |
| GET | `/organizations/{org_id}` | Get organization | ✅ |
| PATCH | `/organizations/{org_id}` | Update organization | ✅ |

### Missing Identity Endpoints
| Endpoint | Priority |
|---|---|
| `POST /gdpr-export` | P1 |
| `DELETE /gdpr-erase` | P1 |
| `GET /users` (admin) | P1 (admin panel needs this) |
| `POST /users/{id}/activate` | P1 |
| `POST /users/{id}/deactivate` | P1 |

---

## Clinical Service (port 8002)

### 20+ Routers — Key Endpoints

| Router | Prefix | Key Endpoints | Status |
|---|---|---|---|
| patients | `/patients` | CRUD, PHI, Mizaj baseline | ✅ |
| encounters | `/encounters` | Create, lifecycle SM, sign-and-lock | ✅ |
| clinical_notes | `/clinical-notes` | Versioned SOAP, cryptographic lock | ✅ |
| appointments | `/appointments` | Schedule, cancel, reschedule | ✅ |
| mizaj | `/mizaj` | Mizaj assessment via engines | ✅ |
| afaal | `/afaal` | Afaal cascade evaluation | ✅ |
| digital_twin | `/digital-twin` | Patient digital model | ✅ |
| dr | `/dr` | Differential reasoning | ✅ |
| governance | `/governance` | Merkle audit trail | ✅ |
| scribe | `/scribe` | Ambient AI scribe, sign | ✅ |
| tasks | `/tasks` | Clinical task pipeline | ✅ (in-memory queue) |
| timeline | `/timeline` | Unified chronological events | ✅ |
| wearables | `/wearables` | Vitals & sensor data | ✅ |
| interop | `/interop` | FHIR R4 export/import | ✅ |
| patient_portal | `/patient-portal` | Patient-facing portal API | ✅ |
| payments | `/billing` | Invoices, payment intents | ✅ |
| prescriptions | `/prescriptions` | Read prescriptions | ✅ |
| qsura | `/qsura` | QSURA telecom/telemedicine | ✅ |
| research | `/research` | Clinical research module | ✅ |
| predictive | `/predictive` | Predictive risk scoring | ✅ |
| cron | `/cron` | Scheduled tasks | ✅ |

---

## Therapeutic Service (port 8004)

| Router | Prefix | Key Endpoints | Status |
|---|---|---|---|
| nuskha | `/nuskha` | Create, compile, validate prescription | ✅ |
| dispensary | `/dispensary` | Dispense, FEFO inventory pick | ✅ |
| care_plans | `/care-plans` | Structured care plans | ✅ |
| logistics | `/logistics` | Courier, delivery tracking | ✅ |
| tadbeer | `/tadbeer` | Lifestyle/regimen guidelines | ✅ |
| ghiza | `/ghiza` | Dietary guidelines | ✅ |

---

## Knowledge Service (port 8003)

| Router | Prefix | Key Endpoints | Status |
|---|---|---|---|
| mufradat | `/mufradat` | Single herb lookup | ✅ |
| murakkabat | `/murakkabat` | Compound formulas | ✅ |
| pharmacopoeia | `/pharmacopoeia` | UPI-aligned monographs | ✅ |
| taxonomy | `/taxonomy` | Unani classification tree | ✅ |
| hybrid_rag | `/rag` | RAG search over knowledge base | ✅ |
| evidence | `/evidence` | Evidence grading | ✅ |
| ocr | `/ocr` | OCR for prescriptions/docs | ✅ |
| graph | `/graph` | Direct Neo4j graph queries | ✅ |

---

## AI Service (port 8005)

| Router | Prefix | Key Endpoints | Status |
|---|---|---|---|
| hakeem | `/hakeem` | Hakeem Sahab AI™ advisory | ✅ |
| multimodal | `/multimodal` | Lab image analysis, voice | ✅ |
| evaluation | `/evaluation` | AI response evaluation | ✅ |
| security | `/security` | Red-team & prompt injection | ✅ |

---

## API URL Configuration (Critical Gap)

Currently in frontend code, API URLs are hardcoded as:
```
http://localhost:8000
```

Must be changed to:
```
process.env.NEXT_PUBLIC_GATEWAY_URL || 'http://localhost:8000'
```

Files requiring fix:
- `apps/web/app/doctor/page.tsx` (lines 88, 108)
- `apps/web/app/patient/page.tsx`
- `apps/web/app/pharmacy/page.tsx` (lines 143, 144, 240, 260)
- `apps/web/components/NuskhaBuilder.tsx`
- `apps/web/components/HakeemReviewDrawer.tsx`
