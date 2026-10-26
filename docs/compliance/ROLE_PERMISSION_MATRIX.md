# ZAYVORA Health OS — Enterprise Role-Based Access Control (RBAC) Matrix
**Document ID**: `ZAY-AUD-007`  
**Classification**: Cybersecurity & Governance Standard  
**Date**: September 2026  
**Status**: AUDITED & ACTIVE  

---

## 1. Enterprise User Roles

ZAYVORA Health OS implements the principle of least privilege across 9 enterprise user roles:

1. `SUPER_ADMIN`: Master platform architect and multi-tenant infrastructure custodian.
2. `ENTERPRISE_ADMIN`: Hospital director or clinic franchise administrator.
3. `DOCTOR`: Licensed Unani physician / Tabeeb with prescribing and signing authority.
4. `HAKEEM`: Senior traditional Unani consultant and formulation specialist.
5. `RECEPTIONIST`: Front desk coordinator, OPD queue manager, and fee collector.
6. `PHARMACIST`: Licensed dispensary lead, Mudabbar verifier, and FEFO stock manager.
7. `PATIENT`: Healthcare consumer and registered medical beneficiary.
8. `RESEARCHER`: Clinical trial investigator and real-world evidence (RWE) analyst.
9. `LAB_TECHNICIAN`: Diagnostic laboratory personnel and physical sign extractor.

---

## 2. Comprehensive 42-Permission Matrix

| # | Permission Code | Scope Description | Admin | Doctor | Hakeem | Reception | Pharmacy | Patient | Research | Lab |
|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | `patient:read_full` | View complete clinical history and PHI | Yes | Yes | Yes | No | No | Self | De-ID | No |
| 2 | `patient:read_demographics`| View name, age, phone, and emergency contact | Yes | Yes | Yes | Yes | Yes | Self | De-ID | Yes |
| 3 | `patient:create` | Register new patient record and MRN | Yes | Yes | Yes | Yes | No | Self Reg| No | No |
| 4 | `patient:update` | Update address, contact, and preferences | Yes | Yes | Yes | Yes | No | Self | No | No |
| 5 | `patient:delete` | GDPR / DISHA statutory right-to-erasure | Yes | No | No | No | No | No | No | No |
| 6 | `encounter:create` | Initiate new clinical consultation | No | Yes | Yes | No | No | No | No | No |
| 7 | `encounter:write_soap` | Author subjective, objective, SOAP notes | No | Yes | Yes | No | No | No | No | No |
| 8 | `encounter:close` | Complete and archive clinical encounter | No | Yes | Yes | No | No | No | No | No |
| 9 | `vitals:record` | Enter BP, pulse, temp, SpO2, Nabz | Yes | Yes | Yes | Yes | No | Self | No | Yes |
| 10| `mizaj:assess` | Conduct 10-Ajnas Mizaj examination | No | Yes | Yes | No | No | Survey | Read | No |
| 11| `mizaj:override` | Clinician override of AI/self Mizaj score | No | Yes | Yes | No | No | No | No | No |
| 12| `organ_axis:map` | Calculate 9-axis physiological cross-talk | No | Yes | Yes | No | No | Read | Read | No |
| 13| `rx:draft` | Formulate botanical Nuskha draft | No | Yes | Yes | No | No | No | No | No |
| 14| `rx:sign_21cfr11` | Cryptographically seal prescription | No | Yes | Yes | No | No | No | No | No |
| 15| `rx:cancel` | Revoke issued prescription | No | Yes | Yes | No | No | No | No | No |
| 16| `rx:read_patient` | View active and past prescriptions | Yes | Yes | Yes | No | Yes | Self | De-ID | No |
| 17| `dispense:verify_fefo` | Validate batch expiry and stock priority | No | No | No | No | Yes | No | No | No |
| 18| `dispense:verify_mudabbar`| Check Schedule E(1) purification certificate| No | No | No | No | Yes | No | No | No |
| 19| `dispense:execute` | Release medicines and deduct inventory | No | No | No | No | Yes | No | No | No |
| 20| `inventory:read` | Inspect pharmacy stock levels | Yes | Read | Read | No | Yes | No | No | No |
| 21| `inventory:adjust` | Log damaged, expired, or returned stock | Yes | No | No | No | Yes | No | No | No |
| 22| `inventory:purchase` | Create supplier purchase order | Yes | No | No | No | Yes | No | No | No |
| 23| `opd:queue_read` | View daily OPD consultation queue | Yes | Yes | Yes | Yes | Read | Self Pos| No | No |
| 24| `opd:token_issue` | Issue sequential queue token (`T-10x`) | Yes | No | No | Yes | No | No | No | No |
| 25| `opd:token_advance` | Transition token status to In Consultation | No | Yes | Yes | Yes | No | No | No | No |
| 26| `appointment:book` | Book scheduled appointment slot | Yes | Yes | Yes | Yes | No | Self | No | No |
| 27| `appointment:cancel` | Cancel or mark no-show appointment | Yes | Yes | Yes | Yes | No | Self | No | No |
| 28| `billing:create_invoice`| Generate OPD or pharmacy invoice | Yes | No | No | Yes | Yes | No | No | No |
| 29| `billing:collect_payment`| Record cash, UPI, or card payment | Yes | No | No | Yes | Yes | Self Pay| No | No |
| 30| `billing:refund` | Authorize consultation fee refund | Yes | No | No | No | No | No | No | No |
| 31| `ai:query_hakeem` | Query Hakeem Sahab clinical assistant | No | Yes | Yes | No | No | No | Yes | No |
| 32| `ai:override_safety` | Force override of non-blocking safety flag| No | Yes | Yes | No | No | No | No | No |
| 33| `scribe:record` | Activate ambient clinical scribe | No | Yes | Yes | No | No | No | No | No |
| 34| `scribe:approve_notes` | Review and merge transcribed SOAP notes | No | Yes | Yes | No | No | No | No | No |
| 35| `lab:upload_report` | Upload diagnostic PDF or image | Yes | Yes | Yes | Yes | No | Self | No | Yes |
| 36| `lab:extract_signs` | Execute multimodal OCR lab extraction | No | Yes | Yes | No | No | No | No | Yes |
| 37| `trial:create_protocol`| Design clinical research protocol | Yes | No | No | No | No | No | Yes | No |
| 38| `trial:view_rwe` | Inspect real-world evidence analytics | Yes | Read | Read | No | No | No | Yes | No |
| 39| `audit:inspect_ledger`| Verify 21 CFR Part 11 Merkle tree | Yes | No | No | No | No | No | Audit | No |
| 40| `tenant:configure` | Manage organization branches and settings | Yes | No | No | No | No | No | No | No |
| 41| `user:provision` | Create staff accounts and assign roles | Yes | No | No | No | No | No | No | No |
| 42| `security:export_keys` | Rotate PKI signing keys and credentials | Yes | No | No | No | No | No | No | No |

---

## 3. Enforcement Mechanisms

- **FastAPI Dependency Injection**: `get_current_active_user` validates JWT tokens and asserts required permissions before handler execution.
- **Frontend Route Protection**: `routeMatrix.ts` cross-checks user role against `allowedRoles`, redirecting unauthorized users to `/login` or displaying a permission denied banner.
- **Database Row-Level Isolation**: All clinical and operational queries strictly filter by `facility_id` and patient MRN.

