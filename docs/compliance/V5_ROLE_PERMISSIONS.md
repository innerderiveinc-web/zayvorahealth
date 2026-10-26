# ZAYVORA HEALTH OS v5.0 — ROLE-BASED ACCESS CONTROL (RBAC) MATRIX
**Document ID**: `ZAY-DOC-V5-RBAC-01`  
**Version**: Enterprise Clinical OS v5.0  
**Classification**: Enterprise Security Standard  

---

## 1. ENTERPRISE ROLES

ZAYVORA Health OS v5.0 enforces strict principle-of-least-privilege across 6 defined enterprise roles:

1. `ROLE_SENIOR_TABEEB` (Doctor / Clinician)
2. `ROLE_PATIENT` (Healthcare Consumer)
3. `ROLE_CLINIC_ADMIN` (Receptionist / OPD Manager)
4. `ROLE_PHARMACIST` (Dispensary Lead)
5. `ROLE_RESEARCHER` (Clinical Trial Investigator)
6. `ROLE_PLATFORM_ADMIN` (System & IT Administrator)

---

## 2. GRANULAR PERMISSION MATRIX

| Permission Code | Description | Doctor | Patient | Reception | Pharmacy | Research | Admin |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| `patient:read` | View patient clinical records | Full | Self Only | Demographics Only | Rx Only | De-ID Only | Audit Only |
| `patient:create` | Register new walk-in patient | Yes | No | Yes | No | No | Yes |
| `encounter:manage` | Conduct consultation & write SOAP | Yes | No | No | No | No | No |
| `rx:create_draft` | Author draft prescription | Yes | No | No | No | No | No |
| `rx:approve_lock` | 21 CFR Part 11 signature & lock | Yes (Verified) | No | No | No | No | No |
| `dispense:verify` | Verify Mudabbar & FEFO batch | No | No | No | Yes | No | No |
| `dispense:execute` | Release medicines & decrement stock | No | No | No | Yes | No | No |
| `billing:charge` | Issue bill & record payment | No | Pay Only | Yes | Yes | No | Yes |
| `trials:manage` | Manage clinical trial protocols | Read | No | No | No | Full | Audit Only |
| `adr:report` | Submit WHO-UMC adverse event | Yes | Yes | No | Yes | Yes | Full |
| `audit:inspect` | Inspect 21 CFR Part 11 Merkle logs | No | No | No | No | No | Full |

---

## 3. ENFORCEMENT PROTOCOLS

- **Backend Enforcement**: Evaluated in FastAPI dependency injection (`get_current_active_user`) at the microservice route level.
- **Frontend Isolation**: Contextual navigation filters routes, preventing unauthorized users from accessing sensitive workspaces.
- **Audit Logging**: Any attempt to access unauthorized resources triggers an immutable security audit event logged in the Merkle ledger.

---
**Approved By**: Principal Cybersecurity Architect, ZAYVORA HEALTH OS™
