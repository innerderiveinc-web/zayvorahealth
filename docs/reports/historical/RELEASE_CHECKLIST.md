# ZAYVORA Health OS™ — Production & Pilot Release Checklist

**Document Reference:** `RELEASE_CHECKLIST.md`  
**Classification:** Operational Release Gate Procedure  
**Target Release:** v1.0.0-pilot (Controlled Clinical Pilot) -> v1.0.0 (General Commercial)  

---

## 1. Controlled Clinical Pilot Release Gates (v1.0.0-pilot)

- [x] **Secret Hygiene**: Zero unencrypted `.env` files or credentials in git tracking or workspace root.
- [x] **Development Secret Rotation**: All development keys rotated and verified with live regression tests.
- [x] **Master Test Regression**: 319 / 319 master system tests passing deterministically.
- [x] **Database Backup & Restoration Drill**: Verified point-in-time recovery with zero data loss (`DRILL-BF8845A0`).
- [x] **Deterministic AI Safety**: Mandatory `safe_to_lock: false` and red-flag emergency referrals verified.
- [x] **Schedule E(1) Mudabbar Gate**: Toxic botanical dispensing hard-blocked without detox batch certificate.
- [x] **21 CFR Part 11 Audit Ledger**: SHA-256 Merkle chain non-repudiation verified on all clinical records.
- [x] **Mobile Source Integrity**: 11 production screens and offline storage service verified.
- [x] **Clinical Pilot Governance Package**: 18 protocol, SOP, and consent documents prepared in `clinical-pilot/`.
- [ ] **Site Institutional Review Board Approval**: Submission of `CLINICAL_PILOT_PROTOCOL.md` to hospital IEC.
- [ ] **Site Pharmacy License Verification**: Verification of on-site dispensary Form 20/20-B state drug license.

---

## 2. Unrestricted Public Commercial Release Gates (v1.0.0)

- [ ] **External Penetration Testing**: Engagement completed with signed CREST penetration testing report.
- [ ] **NHA ABDM Production Sign-Off**: Milestones M1, M2, and M3 certified by National Health Authority.
- [ ] **Commercial Payment & SMS Gateways**: Live merchant credentials provisioned in Vault/KMS.
- [ ] **Managed PostgreSQL Cluster Cutover**: Managed PostgreSQL 16 provisioned with Multi-AZ redundancy.
- [ ] **Mobile Binary Distribution**: Signed Android APK/AAB and iOS IPA generated and approved on Google Play / Apple App Store.
- [ ] **Legal & Compliance Sign-Off**: Final review of Terms of Service, Privacy Policy, and Medical Disclaimers.
