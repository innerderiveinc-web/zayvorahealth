# ZAYVORA Health OS™ — All Pages and Routes Inventory

| Route | Application Shell | Primary Purpose | Authorization Role |
| :--- | :--- | :--- | :--- |
| `/` | Public Web | Platform overview, care philosophy, directory | Public |
| `/auth/login` | Identity | Unified secure login with MFA challenge | Public / Registered |
| `/auth/register` | Identity | Patient self-registration & credentialing | Public |
| `/patient/dashboard` | Patient App | Daily health schedule, upcoming visits, alerts | `ROLE_PATIENT` |
| `/patient/prescriptions`| Patient App | Active herbal medications, posology voice prompts | `ROLE_PATIENT` |
| `/patient/proms` | Patient App | Symptom severity & outcome tracking | `ROLE_PATIENT` |
| `/patient/timeline` | Patient App | Longitudinal chronological care history | `ROLE_PATIENT` |
| `/doctor/workspace` | Clinical Workspace| 16-section unified consultation desk | `ROLE_SENIOR_TABEEB` |
| `/doctor/patients` | Clinical Workspace| Patient roster, search, and MRN directory | `ROLE_SENIOR_TABEEB` |
| `/doctor/appointments`| Clinical Workspace| Today appointments, queue, and triage status | `ROLE_SENIOR_TABEEB` |
| `/clinic/operations` | Clinic Ops | Front-desk queue, check-ins, bed management | `ROLE_CLINIC_ADMIN` |
| `/clinic/billing` | Clinic Ops | Invoices, payment gateway reconciliations | `ROLE_CLINIC_ADMIN` |
| `/pharmacy/queue` | Pharmacy OS | Real-time prescription queue & verification | `ROLE_PHARMACIST` |
| `/pharmacy/inventory` | Pharmacy OS | FEFO stock, expiry monitoring, Mudabbar gate | `ROLE_PHARMACIST` |
| `/pharmacy/ebmr` | Manufacturing OS | Master Formula Records (MFR) & batch assays | `ROLE_PHARMACIST` |
| `/research/trials` | Research Cloud | Clinical trial cohorts & RWE observational studies| `ROLE_RESEARCHER` |
| `/research/adr` | Research Cloud | WHO-UMC / ICH E2B pharmacovigilance reports | `ROLE_RESEARCHER` |
| `/admin/governance` | Platform Admin | 3/3 Specialist quorum change orders & review | `ROLE_ADMIN` |
| `/admin/audit` | Platform Admin | SHA-256 Merkle tree immutable audit viewer | `ROLE_ADMIN` |
| `/admin/interop` | Interop Hub | ABDM gateway status & HL7 FHIR R4 bundles | `ROLE_ADMIN` |
