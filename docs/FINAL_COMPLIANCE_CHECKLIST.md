# ZAYVORA Health OS™ — Compliance Checklist

**Status: Pre-staging / Pilot Candidate**

## 21 CFR Part 11 — Electronic Records & Signatures

| Requirement | Status | Evidence |
|:---|:---|:---|
| Electronic signatures on eBMR | ✅ Implemented | SHA-256 HMAC in `prescriptions.hmac_sha256` |
| Audit trail for all write ops | ✅ Implemented | `identity.audit_log` table |
| User authentication before signing | ✅ Implemented | JWT + MFA required |
| Tamper-evident record storage | ⚠️ Partial | HMAC generated; append-only DB not enforced |
| System access controls | ✅ Implemented | RBAC + JWT |
| System validation | ❌ Not done | IQ/OQ/PQ protocol not conducted |

## GDPR / Data Protection

| Requirement | Status | Evidence |
|:---|:---|:---|
| Right to data portability | ✅ Implemented | `GET /auth/gdpr-export` |
| Right to erasure | ✅ Implemented | `DELETE /auth/gdpr-erase` |
| Data minimisation | ✅ Applied | Only required fields collected |
| Consent management | ⚠️ Partial | UI exists; backend consent log pending |
| Privacy policy | ✅ Published | `/website/privacy` |
| DPA / Data Processing Agreement | ❌ Not drafted | Required before live use |

## Schedule E(1) — Drugs and Cosmetics Act

| Requirement | Status | Evidence |
|:---|:---|:---|
| Herb classification database | ✅ Implemented | ZKB classification |
| Mudabbar gate | ✅ Implemented | QC lab workflow + cert check |
| ICP-MS heavy metal testing | ✅ Workflow | Manufacturing/lab page |
| Microbial limits | ✅ Workflow | Manufacturing/lab page |
| HPTLC authentication | ✅ Workflow | Manufacturing/lab page |

## Clinical Safety

| Requirement | Status | Notes |
|:---|:---|:---|
| safe_to_lock=False invariant | ✅ Active | All AI prescriptions require human sign-off |
| No false efficacy claims | ✅ Enforced | Medical disclaimer on all patient-facing pages |
| Independent clinical review | ❌ Not done | Required before pilot launch |
| IRB/Ethics committee approval | ❌ Not done | Required for research features |

## Overall Compliance Verdict

**System is NOT compliant for live patient data.**
All items marked ❌ must be resolved before the pilot launch.
