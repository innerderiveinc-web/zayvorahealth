# ZAYVORA HEALTH™ — Enterprise Policy: Data Privacy, HIPAA & DISHA Compliance
*Longitudinal PHI Protection, Cryptographic Tenancy & Safe Harbor De-identification*

---

## 1. Statutory Governance Framework

ZAYVORA HEALTH™ adheres strictly to:
1. **DISHA (Digital Information Security in Healthcare Act)**: Indian healthcare data protection standard governing electronic health records, consent frameworks, and patient data autonomy.
2. **HIPAA (Health Insurance Portability and Accountability Act)**: Privacy Rule, Security Rule, and Breach Notification Rule.
3. **ABDM (Ayushman Bharat Digital Mission)**: Guidelines for ABHA onboarding, consent artifacts, and FHIR R4 interoperability.

---

## 2. Multi-Tenant Architectural Isolation

- **Tenant Boundary Invariant**: Every patient, clinical encounter, note, prescription, and audit record is strictly partitioned by `tenant_id` (Clinic / Health System).
- **Row-Level Security (RLS)**: Enforced at the PostgreSQL database engine layer.
- **Neo4j Graph Partitioning**: Patient Graph nodes (`:Patient`, `:Encounter`) are physically separated from universal knowledge nodes (`:Mufrad`, `:Disease`, `:Evidence`). Patient graph queries unconditionally require `WHERE p.tenant_id = $tenant_id`.

---

## 3. Real-World Evidence (RWE) 18 Safe Harbor De-Identification Protocol

Before any patient data can be ingested into the ZAYVORA Research Cloud for observational clinical studies or epidemiological modeling, it must pass through the automated de-identification engine:
1. **Names**: Scrubbed and replaced with a cryptographic salted hash (`SUBJ-XXXXXX`).
2. **Geographic Data**: All geographic subdivisions smaller than state truncated.
3. **Dates**: All clinical dates transformed into relative study timelines ($t - t_0$ in elapsed days).
4. **Phone Numbers & Faxes**: Zeroed out.
5. **Electronic Mail Addresses**: Zeroed out.
6. **Social Security / Aadhaar / National ID Numbers**: Removed.
7. **Medical Record Numbers (MRN)**: Salted SHA-256 pseudonymized.
8. **Health Plan Beneficiary Numbers**: Removed.
9. **Account Numbers**: Removed.
10. **Certificate / License Numbers**: Removed.
11. **Vehicle Identifiers**: Removed.
12. **Device Identifiers & Serial Numbers**: Stripped.
13. **Web Universal Resource Locators (URLs)**: Stripped.
14. **Internet Protocol (IP) Addresses**: Masked to /24 CIDR or eliminated.
15. **Biometric Identifiers**: Retinal and fingerprint scans strictly excluded.
16. **Full-Face Photographs**: Dermatological images must be tightly cropped to the lesion margin, with all facial features completely obscured.
17. **Any Other Unique Identifying Characteristic**: Redacted.
18. **Ages over 89**: Aggregated into a single category of age 90+.

---

## 4. Encryption Standards

- **Data in Transit**: Mandatory TLS 1.3 with mTLS between internal Kubernetes microservice pods.
- **Data at Rest**: AES-256 encryption at the storage layer; column-level encryption for critical PHI fields (patient national IDs, phone numbers, addresses).
