# GDPR Compliance Gap Analysis — ZAYVORA Health OS™

**Date:** 2026-09-14
**Scope:** All patient-facing services
**Standard:** EU General Data Protection Regulation (GDPR) 2016/679

---

## Summary Status

| Article | Requirement | Status |
|---------|-------------|--------|
| Art. 5 | Data minimisation & purpose limitation | ⚠️ Partial |
| Art. 6 | Lawful basis for processing | ✅ Consent tracked |
| Art. 13/14 | Transparency / privacy notice | 🔲 Required |
| Art. 15 | Right of access | 🔲 Not implemented |
| Art. 17 | Right to erasure ("right to be forgotten") | 🔲 Not implemented |
| Art. 20 | Data portability | 🔲 Not implemented |
| Art. 25 | Data protection by design and default | ✅ RBAC, encryption |
| Art. 32 | Security of processing | ✅ Encryption, access controls |
| Art. 33 | Breach notification (72h) | ⚠️ Manual process only |
| Art. 35 | DPIA (Data Protection Impact Assessment) | 🔲 Required |
| Art. 37 | Data Protection Officer (DPO) | 🔲 Appointment needed |

---

## Art. 15 — Right of Access

Patients must be able to request a copy of all personal data held.

**Required endpoint:** `GET /api/v1/patients/{id}/gdpr-export`

Response must include:
- Personal demographics
- Clinical encounters and notes
- Prescriptions and medication history
- Lab results
- Mizaj assessments
- Appointment history
- Audit log entries for their data

**Status:** 🔲 Not implemented — implement as P0 before EU launch.

---

## Art. 17 — Right to Erasure

Patients must be able to request deletion of their data, except where retention is legally required (e.g., medical records).

**Required endpoint:** `DELETE /api/v1/patients/{id}/gdpr-erase`

Logic:
1. Anonymize PII fields (name, email, phone, DOB → hash/null)
2. Retain clinical records (required by law, typically 10 years)
3. Delete non-clinical personal data (preferences, device tokens)
4. Issue deletion confirmation email

**Status:** 🔲 Not implemented — implement as P0 before EU launch.

---

## Art. 20 — Data Portability

Export in machine-readable format (JSON, FHIR R4 Bundle recommended).

**Required endpoint:** `GET /api/v1/patients/{id}/fhir-export`

**Status:** 🔲 Not implemented. FHIR client exists — can generate Bundle from existing data.

---

## Art. 33 — Breach Notification Procedure

GDPR requires notifying the supervisory authority within 72 hours of discovering a personal data breach.

**Current state:** Manual process only. No automated breach detection.

**Actions:**
1. Integrate anomaly detection on audit logs (unusual access patterns)
2. Create breach incident report template (`docs/compliance/BREACH_REPORT_TEMPLATE.md`)
3. Document Data Protection Authority (DPA) contact for each operating country

---

## Data Processing Records (Art. 30)

| Processing Activity | Lawful Basis | Data Subjects | Retention |
|--------------------|-------------|---------------|-----------|
| User authentication | Legitimate interest | All users | 7 years |
| Clinical encounters | Medical treatment (Art. 9(2)(h)) | Patients | 10 years |
| Prescriptions | Medical treatment | Patients | 10 years |
| AI inference (Hakeem) | Legitimate interest + consent | Patients | Session only |
| Notifications (SMS/email) | Legitimate interest | All users | 30 days |
| Audit logs | Legal obligation | All users | 6 years |
| Payment data | Contractual | Paying users | 7 years |

---

## Privacy by Design Checklist

- [x] Encryption at rest (AES-256 for PHI fields)
- [x] Encryption in transit (TLS 1.3)
- [x] RBAC — minimum necessary access
- [x] Audit logging of all PHI access
- [x] Pseudonymisation of patient IDs in logs
- [ ] Data retention policies enforced by automated purge jobs
- [ ] Consent management UI in patient portal
- [ ] Cookie consent banner on web app
- [ ] Privacy policy page accessible without login

---

## Priority Actions for EU Launch

| Priority | Action | Owner |
|----------|--------|-------|
| P0 | Appoint a Data Protection Officer (DPO) | Legal |
| P0 | Conduct Data Protection Impact Assessment (DPIA) | Tech + Legal |
| P0 | Implement GDPR data export endpoint | Engineering |
| P0 | Implement GDPR erasure endpoint | Engineering |
| P0 | Publish privacy policy and cookie notice | Legal + Design |
| P1 | Implement consent management in patient portal | Engineering |
| P1 | Automated audit log retention and purge jobs | Engineering |
| P1 | Document breach notification procedure | Legal |
| P2 | Register with local DPA if required | Legal |
