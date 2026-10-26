# ZAYVORA HEALTH OS™ — PHASE 4 DELIVERY REPORT
## Pharmacy FEFO Allocation, Schedule E(1) Mudabbar Gate, Atomic Dispensing & Billing Settlement

**Author**: Principal Software Architect & Clinical Safety Officer  
**Date**: September 13, 2026  
**Status**: COMPLETE & PRODUCTION-VERIFIED (15/15 Automated Integration Tests Passing)  
**Classification**: Regulated Ayurvedic, Siddha, and Unani (ASU) Digital Pharmacy & Billing Subsystem  

---

### 1. Executive Summary

Phase 4 establishes the clinical dispensary and automated billing continuum for ZAYVORA HEALTH OS™. Under classical Unani and statutory AYUSH regulations (Drugs & Cosmetics Act 1940, Rule 161 and Schedule E(1)), medication dispensing is subject to strict legal and clinical safety constraints:
1. **First-Expired, First-Out (FEFO)**: Dispensary lots must be allocated strictly in order of chronological expiration date (`expiry_date ASC`) to prevent stock obsolescence and ensure maximum therapeutic potency.
2. **Schedule E(1) Mudabbar Gate**: Toxic or irritant botanical and mineral ingredients (e.g., *Colchicum luteum* / *Suranjan Talkh*, *Strychnos nux-vomica* / *Azaraqi*) must never be dispensed in raw, unpurified states. Dispensation requires an audited, non-null `mudabbar_cert` purification lot certificate.
3. **Statutory Expiry Protection**: Expired inventory batches are blocked at the database and API layer with immediate clinical alerts.
4. **Atomic Prescription Dispensation**: Multi-formulation prescriptions are fulfilled as an atomic database transaction. All prescribed batches are decremented simultaneously, the prescription status updates to `DISPENSED`, an itemized invoice is created in the billing ledger, and an immutable leaf hash is anchored into the 21 CFR Part 11 Merkle audit trail.
5. **Multi-Tenancy & RBAC**: Only licensed pharmacy staff (`ROLE_PHARMACIST`, `SUPER_ADMIN`) are permitted to dispense stock. Cross-facility inventory tampering is cryptographically blocked.

---

### 2. Implemented Schema & Architecture Extensions

#### A. Database Schema (`database/schema.sql` & `database/init_live_db.py`)
- **Inventory Table Enhancement**: Added `unit_price REAL DEFAULT 150.0` and performance index `idx_inventory_name` on `(name, expiry_date)`.
- **Invoices Table Enhancement**: Added `prescription_id TEXT` and `items_json TEXT DEFAULT '[]'` with performance index `idx_invoices_prescription` on `(prescription_id)`.
- **Statutory Test Seeding**:
  - `MS-2026-LOT5`: *Majun Suranjan (Mudabbar)*, Exp: `2027-05-15`, Stock: 45, Cert: `MUD-2026-0881` (Earliest active lot).
  - `MS-2026-LOT4`: *Majun Suranjan (Mudabbar)*, Exp: `2027-08-30`, Stock: 130, Cert: `MUD-2026-0412` (Secondary lot).
  - `MS-2026-RAW`: *Majun Suranjan (Unpurified)*, Exp: `2027-10-01`, Stock: 50, Cert: `NULL` (Schedule E(1) unpurified test lot).
  - `RB-2024-EXP`: *Roghane Badam Shirin*, Exp: `2024-12-31`, Stock: 15, Cert: `NULL` (Statutory expired test lot).

---

### 3. API Endpoints Delivered

| Endpoint | Method | Role | Description |
| :--- | :--- | :--- | :--- |
| `/api/v1/inventory/allocate-fefo` | POST | Pharmacist, Doctor, Staff | Algorithmic FEFO batch allocation. Sorts available batches chronologically, excludes expired lots, enforces Mudabbar checks for Schedule E(1), and splits quantities greedily across tiers. |
| `/api/v1/inventory/dispense` | POST | Pharmacist, Super Admin | Single-batch dispensary deduction. Validates stock sufficiency, checks expiry, enforces Mudabbar certification, isolates facility tenant, and logs Merkle audit block. |
| `/api/v1/prescriptions/{id}/dispense` | POST | Pharmacist, Super Admin | Atomic fulfillment of complete prescription. Allocates all items via FEFO, decrements inventory stock, transitions prescription to `DISPENSED`, generates settled pharmacy invoice (`RCPT-PHARM-xxxx`), and anchors audit event. |
| `/api/v1/inventory` | GET | Authenticated Staff | Fetches facility inventory sorted by `expiry_date ASC`. |
| `/api/v1/prescriptions` | GET | Authenticated Staff | Enhanced with `?status=...` and `?mrn=...` filtering. |
| `/api/v1/billing/invoices` | GET | Authenticated Staff | Enhanced with `?prescriptionId=...` filtering for instant reconciliation. |

---

### 4. Safety Gates & Algorithmic Guardrails

#### 1. FEFO Allocation Engine
```python
# Algorithmic sorting and greedy allocation
cur.execute("""
    SELECT * FROM inventory 
    WHERE LOWER(name) = ? AND facility_id = ? AND stock_qty > 0 AND expiry_date > ?
    ORDER BY expiry_date ASC
""", (med_name.lower(), target_facility, today_str))
```
- Multi-batch quantities are split cleanly across lots (e.g. allocating 60 units from a 45-unit earliest lot and 15 units from a 130-unit secondary lot).
- If available stock cannot satisfy the requested quantity, the endpoint returns an allocation plan with `fullyAllocated: false` and a transparent stock shortfall message.

#### 2. Statutory Schedule E(1) Mudabbar Gate
- Unani botanical and mineral toxins under Schedule E(1) (e.g., Suranjan Talkh / *Colchicum luteum*) must have a verified detoxification record (`mudabbar_cert`).
- Any attempt to allocate or dispense an unpurified batch returns:
  `HTTP 403 Forbidden`  
  `code: "MUDABBAR_CERTIFICATE_REQUIRED"`  
  `error: "DISPENSE BLOCKED: Schedule E(1) item requires validated Mudabbar Certificate."`

#### 3. Statutory Expiry Gate
- Stock items where `expiry_date <= today_str` are strictly blocked:
  `HTTP 400 Bad Request`  
  `code: "EXPIRED_STOCK_ERROR"`  
  `error: "Dispensing blocked: This medication batch has passed its expiration date."`

#### 4. Dispense Idempotency Guard
- Once a prescription is fulfilled, its status transitions to `DISPENSED`. Subsequent duplicate dispense attempts are rejected:
  `HTTP 400 Bad Request`  
  `code: "PRESCRIPTION_ALREADY_DISPENSED"`  
  `error: "This prescription has already been dispensed and cannot be fulfilled again."`

#### 5. Cross-Tenant Pharmacy Guard
- Pharmacists can only allocate and dispense inventory belonging to their assigned healthcare facility (`facility_id`). Cross-tenant requests without Super Admin credentials return:
  `HTTP 403 Forbidden`  
  `code: "CROSS_TENANT_ACCESS_DENIED"`  
  `error: "Access denied: You do not have authorization to dispense inventory from a different healthcare facility."`

---

### 5. Automated Test Suite Verification

Test Suite: `tests/test_phase4_pharmacy_fefo_billing.py`  
Status: **15/15 PASSED (100%)**

```
============================================================================
 ZAYVORA HEALTH OS™ — PHASE 4 PHARMACY FEFO, DISPENSING & BILLING TEST SUITE
============================================================================
[PASS] Test 01: FEFO Inventory Retrieval - Retrieved 8 inventory items ordered by expiry_date ASC
[PASS] Test 02: FEFO Lot Prioritization - Allocated earliest lot MS-2026-LOT5 (Exp: 2027-05-15)
[PASS] Test 03: Multi-Batch Split Allocation - Split 60 units across LOT5 (45.0) and LOT4 (15.0)
[PASS] Test 04: Statutory Expiry Gate - Blocked expired stock RB-2024-EXP: 'Dispensing blocked: This medication batch has passed its expiration date.'
[PASS] Test 05: Schedule E(1) Mudabbar Gate - Blocked raw botanical MS-2026-RAW: 'DISPENSE BLOCKED: Schedule E(1) item requires validated Mudabbar Certificate.'
[PASS] Test 06: Certified Mudabbar Dispensation - Successfully dispensed MS-2026-LOT4 (Remaining: 127)
[PASS] Test 07: Stock Sufficiency Guardrail - Rejected excess quantity: 'Insufficient stock for batch RB-2026-LOT1. Available: 87, Requested: 9999.'
[PASS] Test 08: RBAC Patient Dispensing Barrier - Patient blocked from dispensing: 'Access restricted: Only licensed pharmacy personnel are authorized to dispense medications.'
[PASS] Test 09: RBAC Receptionist Dispensing Barrier - Receptionist blocked from dispensing: 'Access restricted: Only licensed pharmacy personnel are authorized to dispense medications.'
[PASS] Test 10: Atomic Prescription Dispensation - Prescription RX-2026-E6F6 fulfilled, Invoice RCPT-PHARM-4039 settled (₹420.0)
[PASS] Test 11: Dispense Idempotency Guard - Duplicate dispense rejected: 'This prescription has already been dispensed and cannot be fulfilled again.'
[PASS] Test 12: Billing Reconciliation - Retrieved pharmacy invoice RCPT-PHARM-4039 linked to RX-2026-E6F6 (Dept: Central Dispensary)
[PASS] Test 13: Cross-Tenant Pharmacy Guard - Cross-facility dispense blocked: 'Access denied: You do not have authorization to dispense inventory from a different healthcare facility.'
[PASS] Test 14: Merkle Audit Trail - Dispense anchored in Merkle block #19 (Hash: 221daf915a4c9f2e...)
[PASS] Test 15: Zero Developer Jargon Audit - All pharmacy payloads, error codes and clinical responses contain zero developer terminology
============================================================================
PHASE 4 VERIFICATION SUMMARY: 15 PASSED | 0 FAILED (TOTAL 15)
============================================================================
```

---

### 6. Frontend Pharmacy Integration (`apps/web/app/pharmacy/page.tsx`)

1. **Live Data Binding**:
   - Prescription dispensing queue connects to `GET /api/v1/prescriptions?status=PENDING_VERIFICATION`.
   - Inventory levels connect to `GET /api/v1/inventory`.
2. **Interactive Dispensing Flow**:
   - Pharmacist verifies prescribed formulations against active FEFO batches.
   - Click on "Confirm & Dispense All Formulations" executes `POST /api/v1/prescriptions/{id}/dispense`.
   - On success, displays real-time settled billing receipt with receipt ID, total amount (₹), and 21 CFR Part 11 Merkle leaf hash.
   - Automatically refreshes inventory stock and prescription queue.
3. **Zero Developer Jargon**:
   - All modal notices, error alerts, and receipt summaries use clean clinical nomenclature.
