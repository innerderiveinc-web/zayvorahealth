# ZAYVORA Health OS™ — Security Model

**Status: Pre-staging · Independent audit NOT yet conducted**

> ⚠️ CAUTION: Do not deploy with live patient data until an independent security audit
> is complete and all findings are remediated.

## Authentication

- **JWT RS256** — Asymmetric signing; private key never leaves identity service
- **JWKS endpoint** — `/api/v1/auth/jwks.json` for public key distribution
- **Session timeout** — 15 minutes inactivity auto-logout
- **Refresh tokens** — Short-lived (1h access, 7d refresh)

## Multi-Factor Authentication

- **TOTP-based** (RFC 6238) for all clinical roles
- Setup via `/auth/mfa/setup` + `/auth/mfa/verify-setup`
- Mandatory for: doctor, receptionist, pharmacy, admin, manufacturing

## Role-Based Access Control (RBAC)

Roles: super_admin, doctor, receptionist, pharmacy, research_analyst, manufacturing, patient

Each role maps to a permission set. Permissions are checked at the API gateway level.

## 21 CFR Part 11 Compliance

- All eBMR (prescription) sign events generate a **SHA-256 HMAC** signature
- Signature stored in `prescriptions.hmac_sha256`
- Audit trail: every write operation logged to `identity.audit_log`
- Electronic signatures include: user_id, timestamp, action, resource_id, ip_address

## Schedule E(1) Safety Gate

Herb classes listed under Schedule E(1) of the Drugs and Cosmetics Act require:
1. Mudabbar (detoxification/purification) certification
2. ICP-MS heavy metal verification
3. Microbial limits confirmation

The Safety Gate at the therapeutic service **blocks** dispensing of Schedule E(1) herbs
without a valid Mudabbar certificate in the QC system.

## GDPR Compliance

- Right to export: `GET /api/v1/auth/gdpr-export`
- Right to erasure: `DELETE /api/v1/auth/gdpr-erase`
- Data minimisation applied to all patient records

## Known Security Gaps (Must Fix Before Production)

1. HashiCorp Vault not provisioned (secrets currently in environment variables)
2. No independent penetration test conducted
3. Rate limiting not implemented at API gateway
4. CORS configuration requires hardening for production domains
5. Container images not scanned for CVEs
