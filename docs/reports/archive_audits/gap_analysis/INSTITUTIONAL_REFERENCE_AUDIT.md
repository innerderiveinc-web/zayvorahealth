# ZAYVORA Health OS™ — Institutional Reference Audit

**Status:** Completed & Enforced  
**Audit Scope:** Full codebase scan across all file extensions (`.py`, `.ts`, `.tsx`, `.sql`, `.md`, `.json`, `.yaml`)  
**Author:** DevSecOps Lead & Quality Assurance Lead  

---

## 1. Audit Policy & Source Categories

Under the ZAYVORA Source Attribution Policy, external institutional names may only be retained if they fall under one of 8 legitimate source categories:

1. `HISTORICAL_REFERENCE` — Classical history of Greco-Arab / Unani medicine.
2. `ACADEMIC_REFERENCE` — Verified degree or alma mater of a licensed practitioner.
3. `EVIDENCE_SOURCE` — Published peer-reviewed research or clinical trial citation.
4. `PUBLICATION_SOURCE` — Official textbook, monograph, or gazette publication.
5. `REGULATORY_SOURCE` — AYUSH Ministry, WHO, FSSAI, or pharmacopoeia commission citations.
6. `EXAMPLE_ONLY` — Academic benchmark in multi-center research simulation harness.
7. `VERIFIED_COLLABORATION` — Active legal partnership (None currently active).
8. `VERIFIED_AFFILIATION` — Active legal affiliation (None currently active).

**Any occurrence in operational UI, clinical appointments, prescriptions, dispensaries, or demo tenants that does not satisfy these categories has been expunged.**

---

## 2. Forensic Register of Retained References

| Institution | File / Path | Category | Reason for Retention | Endorsement Implied? | Legal Status | Approval |
|:---|:---|:---:|:---|:---:|:---:|:---:|
| **A&U Tibbia College, University of Delhi** | `apps/web/lib/cms/doctorsData.ts` | `ACADEMIC_REFERENCE` | Medical qualification of Prof. Dr. Mansoor Alam (BUMS degree) | No | Verified academic degree | Approved |
| **Faculty of Medicine (Unani), Jamia Hamdard** | `apps/web/lib/cms/doctorsData.ts` | `ACADEMIC_REFERENCE` | Medical qualification of Dr. Hakim Sirajuddin (BUMS degree) | No | Verified academic degree | Approved |
| **Aligarh Muslim University (AMU)** | `apps/web/lib/cms/doctorsData.ts` | `ACADEMIC_REFERENCE` | Post-graduate MD (Kulliyat) credential of Dr. Hakim Sirajuddin | No | Verified academic degree | Approved |
| **Government Nizamia Tibbi College, Hyderabad** | `apps/web/lib/cms/doctorsData.ts` | `ACADEMIC_REFERENCE` | Medical qualification of Dr. Yasmeen Zehra (BUMS degree) | No | Verified academic degree | Approved |
| **Jamia Hamdard (PhD Pharmacology)** | `apps/web/lib/cms/doctorsData.ts` | `ACADEMIC_REFERENCE` | Doctorate credential in Ilmul Advia of Dr. Tariq Zafar | No | Verified academic degree | Approved |
| **AUTC, Jamia Hamdard, AMU AKTC** | `database/seed_pilot_tenants.py` | `EXAMPLE_ONLY` | Multi-center synthetic research cohort benchmarking in clinical concordance test | No | Synthetic test harness fixture | Approved |
| **AUTC, Jamia Hamdard, AMU AKTC** | `tests/test_clinical_pilot_concordance.py`| `EXAMPLE_ONLY` | Multi-site test assertions validating university concordance simulation | No | CI test harness | Approved |
