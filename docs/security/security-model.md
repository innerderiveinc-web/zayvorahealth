# ZAYVORA Health OS™ — Security Model & Data Governance

## 1. Compliance Framework
- **US FDA 21 CFR Part 11:** Electronic records, tamper-evident audit trails, and cryptographically verified digital signatures.
- **India DISHA & DPDP Act 2023:** Stringent data localization, explicit consent management, and pseudonymized research data exports.
- **HIPAA Safe Harbor (45 CFR § 164.514(b)(2)):** Automatic stripping of all 18 direct identifiers before clinical trial ingestion.

## 2. Authentication & Authorization (RBAC)
- Multi-factor authentication (TOTP / SMS OTP) mandatory for all administrative and prescribing roles.
- Role-Based Access Control enforcing tenant isolation across all database queries (`organization_id` foreign keys).
- Revocation blocklist for invalidating JWT tokens upon logout or role reassignment.

## 3. Cryptographic Storage & Transit
- All PHI (Protected Health Information) columns encrypted at rest using AES-256-GCM.
- TLS 1.3 enforced for all microservice intra-cluster and public ingress traffic.
- SHA-256 Merkle tree ledger anchoring every critical clinical action (prescribing, note locking, dispensing, adverse event reporting).
