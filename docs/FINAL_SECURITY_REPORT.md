# ZAYVORA Health OS™ — Final Security & Cryptography Report

**Status:** Pre-staging / Pilot Candidate  
**Standard:** OWASP Top 10, 21 CFR Part 11, HIPAA Security Rule, DPDP Act 2023  
**Author:** DevSecOps Lead & Information Security Architect  

---

## 1. Authentication & Session Architecture

- **Token Scheme:** Asymmetric RS256 JWT with public key distribution via `/.well-known/jwks.json`.
- **Session Duration:** 15-minute access token lifespan with automatic refresh token rotation.
- **Token Invalidation:** Token reuse detection revokes all downstream tokens upon replay attempt.
- **Lockout Manager:** Tracks failed authentication attempts per identifier; locks account for 15 minutes after 5 consecutive failures.
- **Password Security:** Minimum 12 characters, requiring uppercase, lowercase, digit, and special character. Salted SHA-256 hashing.

---

## 2. Multi-Factor Authentication (MFA)

- Implements TOTP (RFC 6238) via `pyotp`.
- Mandatory for all clinical, pharmacy, manufacturing, and administrative roles.
- Provisioning endpoint: `POST /api/v1/auth/mfa/setup` with QR code generation.
- Verification endpoint: `POST /api/v1/auth/mfa/verify-setup`.

---

## 3. Role-Based Access Control (RBAC) & Tenancy

Seven clinical and operational roles enforce granular endpoint permissions:

| Role | Scope & Permissions | Gating Enforcement |
|:---|:---|:---:|
| `SUPER_ADMIN` | Global platform administration, Merkle audit inspection | Gateway + Service |
| `CLINIC_ADMIN`| Facility management, staff assignment, billing audit | Gateway + Service |
| `DOCTOR` | Clinical encounters, diagnosis, Nuskha authoring, AI copilot | Gateway + Service |
| `HAKEEM` | Unani consultations, Mizaj diagnostics, Tadbeer planning | Gateway + Service |
| `RECEPTIONIST`| Patient registration, appointment booking, queue management | Gateway + Service |
| `PHARMACIST` | Prescription verification, FEFO inventory dispensing | Gateway + Service |
| `PATIENT` | Self-record view, appointment booking, prescription access | Gateway + Service |

### Multi-Tenancy & Cross-Tenant Data Isolation
- Every query is partitioned by `facility_id` / `organization_id`.
- Verified in automated test suites: cross-tenant access attempts return `HTTP 403 FORBIDDEN` (`CROSS_TENANT_ACCESS_DENIED`).

---

## 4. 21 CFR Part 11 Compliance & Audit Ledger

- **Electronic Signatures:** All prescription releases, encounter locks, and Certificate of Analysis (CoA) sign-offs generate a SHA-256 HMAC digital signature.
- **Signature Payload:** Combines Order Number, Patient MRN, Doctor Registration Number, Formulation Payload, and Timestamp.
- **Audit Ledger:** Append-only ledger table (`audit_ledger`) anchors every state change with leaf hash, signer identity, facility ID, and timestamp.
- **Immutability:** Modifying historical prescription or encounter records is programmatically blocked.

---

## 5. Security Gaps & Pre-Pilot Hardening Checklist

| Security Requirement | Status | Pre-Pilot Action Required |
|:---|:---:|:---|
| Independent Penetration Testing | ❌ Pending | Engage external CREST-accredited firm for grey-box audit |
| HashiCorp Vault Secrets Storage | ⚠️ Configured | Provision live Vault agent in staging cluster |
| Container Image Scanning | ✅ Configured | Trivy vulnerability scan configured in CI pipeline |
| Rate Limiting | ✅ Active | Sliding-window IP and per-user limits on API Gateway |
| Security Response Headers | ✅ Active | OWASP headers (CSP, HSTS, X-Frame-Options) injected |
