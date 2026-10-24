# ZAYVORA Health OS™ — Remaining Blockers Matrix

**Document Reference:** `REMAINING_BLOCKERS.md`  
**Classification:** Enterprise Healthcare Release & Deployment Governance  
**Generated At:** 2026-09-16T16:14:45+05:30  

---

## 1. Release Blocker Classification

Blockers are categorized into:
- **Pilot Blockers**: Must be resolved before the controlled clinical pilot begins.
- **Commercial Public Release Blockers**: Must be resolved before open general-public launch.

---

## 2. Detailed Blocker Inventory

| Blocker ID | Domain | Severity | Description | Pilot Blocker? | Public Release Blocker? | Remediation Roadmap / Owner |
|---|---|---|---|---|---|---|
| **BLK-01** | Regulatory | **Critical** | Physical Pilot Site Pharmacy Retail License (State Drug Authority Form 20/20-B). | **YES** | **YES** | Site Clinical Director to provide attested copy of pharmacy retail license prior to patient enrollment. |
| **BLK-02** | Governance | **High** | Institutional Ethics Committee (IEC) / IRB approval of `CLINICAL_PILOT_PROTOCOL.md`. | **YES** | **YES** | Submit clinical pilot protocol and consent forms to institutional review board. |
| **BLK-03** | Interoperability | **High** | Official National Health Authority (NHA) ABDM Milestone 1–3 Production Certification. | **NO** (Sandbox OK) | **YES** | Schedule NHA milestone demonstration and complete production security audit. |
| **BLK-04** | Security | **High** | External CREST / CHECK certified third-party penetration testing engagement. | **NO** (Internal OK) | **YES** | Execute external pen test under `PENTEST_RULES_OF_ENGAGEMENT_TEMPLATE.md`. |
| **BLK-05** | Infrastructure | **Medium** | Provision live commercial SMS aggregator (Twilio/SendGrid) and payment gateway keys. | **NO** (Fallback OK) | **YES** | Securely provision live API keys into production HashiCorp Vault / Kubernetes secrets. |
| **BLK-06** | Mobile DevOps | **Medium** | Automated Android APK/AAB and iOS IPA binary compilation in dedicated build farm. | **NO** (Local test OK) | **YES** | Set up GitHub Actions macOS runner with Xcode and Android SDK to generate signed app store binaries. |
| **BLK-07** | Infrastructure | **Medium** | Live multi-AZ PostgreSQL 16 cluster provisioning and DNS cutover. | **NO** (SQLite OK) | **YES** | Run `psql -f database/postgres_setup.sql` and `make migrate` on managed PostgreSQL cluster. |

---

## 3. Blockers Resolution Timeline
- **Pilot Phase (Month 0)**: BLK-01 (Pharmacy license) and BLK-02 (IEC approval) scheduled for completion during pre-pilot institutional onboarding.
- **Pre-Commercial Phase (Month 4–6)**: BLK-03 (ABDM sign-off), BLK-04 (CREST pen test), BLK-05 (Cloud credentials), BLK-06 (Mobile binaries), and BLK-07 (PostgreSQL cluster) scheduled for commercial launch preparation.
