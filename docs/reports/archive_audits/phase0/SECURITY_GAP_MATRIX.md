# ZAYVORA Health OS™ — SECURITY GAP MATRIX
**Audit Date:** September 15, 2026  
**Classification:** CONFIDENTIAL — Engineering & Security Review Only

---

## 1. Critical Security Gaps (P0 — Block Any Patient Encounter)

| ID | Gap | Location | Risk | Remediation |
|---|---|---|---|---|
| **SEC-P0-01** | `SESSION_MOCK_TOKEN` hardcoded in production-path components | `HakeemReviewDrawer.tsx:698`, `NuskhaBuilder.tsx:949` | All AI recommendations would route without real auth context — prescriptions could be generated without doctor identity | Replace with `authService.getToken()` — auth context from React context/hook |
| **SEC-P0-02** | API URLs hardcoded as `http://localhost:8000` (HTTP, not HTTPS) | `app/doctor/page.tsx:88,108`, `app/pharmacy/page.tsx:143,144` | In production, data transmitted unencrypted; localhost URL will fail in any non-local environment | Use `process.env.NEXT_PUBLIC_GATEWAY_URL` + enforce HTTPS |
| **SEC-P0-03** | MFA not enforced for clinical staff login | `services/identity/app/routers/auth.py` | Clinical roles (Hakeem, Pharmacist) can access PHI without MFA — HIPAA/GDPR violation | Enforce `mfa_required=True` for roles with PHI access in login flow |
| **SEC-P0-04** | `lang` attribute missing from HTML root | `apps/web/app/layout.tsx` | Screen readers cannot determine language — accessibility + potential XSS vector | Add `lang="en"` (or `"ur"` for Urdu) to `<html>` element |

---

## 2. High Priority Security Gaps (P1 — Required Before GA)

| ID | Gap | Location | Risk | Remediation |
|---|---|---|---|---|
| **SEC-P1-01** | GDPR export endpoint missing | Gateway + Identity | Non-compliant with GDPR Article 20 (right to data portability) | Implement `GET /api/v1/gdpr-export` returning all patient data |
| **SEC-P1-02** | GDPR erasure endpoint missing | Gateway + Identity | Non-compliant with GDPR Article 17 (right to be forgotten) | Implement `DELETE /api/v1/gdpr-erase` with cascade anonymization |
| **SEC-P1-03** | mTLS inter-service communication not configured | `docker-compose.yml`, Helm | Internal service calls use plain HTTP — MITM possible in shared cluster | Configure TLS certs per service + mutual verification in Kubernetes |
| **SEC-P1-04** | No rate limiting on auth endpoints | `services/identity/app/routers/auth.py` | Brute-force attacks on login/reset-password possible | Add Slowapi/Redis-backed rate limiter: 5 attempts per 15 min per IP |
| **SEC-P1-05** | `users` table lacks failed_login_attempts / account lockout | `services/identity/app/models/identity.py` | No protection against brute-force credential stuffing | Add `failed_login_attempts` INT, `locked_until` TIMESTAMP |
| **SEC-P1-06** | No GDPR consent table | DB schema | Cannot prove informed consent for PHI collection — GDPR violation | Add `consent_records` table with consent_type, granted_at, withdrawn_at |
| **SEC-P1-07** | RabbitMQ/NATS event bus absent — in-memory queue | `clinical/app/workers/` | In-memory task queue data lost on process restart — audit trail gaps | Implement Celery + Redis or NATS for durable async tasks |
| **SEC-P1-08** | Automated JWT key rotation not implemented | `services/identity/app/core/security.py` | Long-lived signing keys increase breach impact window | Implement scheduled key rotation daemon with graceful key rollover |
| **SEC-P1-09** | PHI encryption coverage not verified | `clinical/app/models/clinical.py` | Some patient fields (phone, address) may not be AES-GCM encrypted | Audit all `patients` columns — apply `EncryptedString` type to PHI |

---

## 3. Medium Priority (P2 — Pre-Pilot)

| ID | Gap | Remediation |
|---|---|---|
| **SEC-P2-01** | BYOK (Bring Your Own Key) org encryption not implemented | AWS KMS / Azure Key Vault per-org key management |
| **SEC-P2-02** | No Content Security Policy (CSP) headers | Add strict CSP via Next.js middleware / Nginx |
| **SEC-P2-03** | No Subresource Integrity (SRI) on external scripts | Add integrity hashes to CDN resources |
| **SEC-P2-04** | Docker containers not verified to run as non-root | Audit all Dockerfiles for `USER nonroot` directive |
| **SEC-P2-05** | No automated dependency vulnerability scanning in CI | Trivy scan exists in CI but not blocking — make it blocking |
| **SEC-P2-06** | Blockchain Merkle root anchoring not implemented | Periodic anchor to public blockchain / consortium ledger |
| **SEC-P2-07** | No WAF (Web Application Firewall) configuration | Add Cloudflare WAF rules or Nginx ModSecurity |
| **SEC-P2-08** | AI prompt injection protection not tested | Red-team `ai/app/security/` against adversarial prompts |

---

## 4. Security Controls Already Implemented ✅

| Control | Implementation | Evidence |
|---|---|---|
| JWT RS256 asymmetric signing | `security.py` — JWKS endpoint | ✅ |
| Argon2id / bcrypt password hashing | `security.py` | ✅ |
| JTI token revocation (instant logout) | Redis JTI blacklist | ✅ |
| RBAC with permission catalogue | `permissions_catalogue.py` | ✅ |
| Multi-tenant data isolation | Org ID scoped on all DB queries | ✅ |
| 21 CFR Part 11 electronic signatures | `scribe.py` sign-and-lock | ✅ |
| Tamper-evident Merkle audit trail | `audit_trail_engine.py` | ✅ |
| AES-256-GCM PHI encryption | Applied to key patient fields | ✅ (coverage audit needed) |
| SQL injection protection | SQLAlchemy ORM — parameterized | ✅ |
| HMAC constant-time comparison | `hmac.compare_digest` in security.py | ✅ |
| Non-root container execution | Helm values | 🟡 Configured in Helm, not verified in all Dockerfiles |
| Safety Firewall — Schedule E(1) block | `safety_firewall.py` | ✅ |
| `safe_to_lock = False` AI invariant | `hakeem_sahab.py` | ✅ |
| Penetration test scenarios | Test suite — SQL inject, HMAC forge, cross-tenant | ✅ |
| CORS configuration | Gateway middleware | ✅ |
| Security headers | `security_headers.py` | ✅ |
| Rate limiting | `rate_limit.py` (Redis-backed) | ✅ (auth endpoints need stricter limits) |

---

## 5. Compliance Readiness

| Regulation | Status | Key Gaps |
|---|---|---|
| **HIPAA** | 🟡 75% | MFA enforcement, audit log completeness, BA agreements |
| **GDPR** | 🔴 50% | Consent table, export/erase endpoints, cookie banner |
| **AYUSH/CDSCO** | ✅ 90% | Schedule E(1) firewall, 21 CFR Part 11 signatures in place |
| **21 CFR Part 11** | ✅ 85% | eSign bridge to e-Mudhra/Aadhaar needed for Indian legal validity |
| **ISO 27001** | 🟡 60% | Policy documentation exists, certification process not started |
