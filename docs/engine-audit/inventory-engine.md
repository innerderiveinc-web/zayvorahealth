# ZAYVORA HEALTH OS™ — CLINICAL ENGINE AUDIT
## FEFO Inventory Allocation Engine (`ENG-22-INVENTORY-FEFO`)

**Document Classification**: Statutory Clinical & Architectural Audit Report  
**Implementation Source File**: [`services/therapeutic/app/engines/dispensary_engine.py`](file:////Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/therapeutic/app/engines/dispensary_engine.py)  
**Hosting Microservice**: `services/therapeutic`  
**Verification Status**: VERIFIED AND TESTED (100% Pass Rate)

---

### 1. What It Does
Enforces First-Expired, First-Out (FEFO) stock rotation across multi-location dispensary warehouses, managing batch lots, expiration dates, and Mudabbar certificates.

### 2. What Data It Accepts
Requested formulation name, quantity required, facility ID.

### 3. What Data It Uses
Inventory table in zayvora_live.db with fields lot_number, expiry_date, mudabbar_cert, quantity_on_hand.

### 4. What Rules It Applies
Sorts lots by expiry_date ASC; excludes expired stock (expiry_date <= today); requires valid Mudabbar cert for Schedule E(1).

### 5. What Knowledge It Retrieves
WHO Good Storage and Distribution Practices for Medical Products.

### 6. What Model It Uses (If Any)
Greedy multi-batch allocation algorithm.

### 7. What Output It Produces
FEFO allocation JSON detailing allocated batch lot numbers, quantities picked per lot, and remaining warehouse stock.

### 8. What Safety Checks Exist
Blocks expired stock with HTTP 400 (EXPIRED_STOCK_ERROR); blocks unpurified Schedule E(1) (MUDABBAR_CERTIFICATE_REQUIRED).

### 9. What Happens When Data Is Missing
Fails allocation if total available unexpired stock < requested quantity.

### 10. What Happens When Confidence Is Low
Not applicable — exact inventory ledger accounting.

### 11. What Happens When Evidence Is Unavailable
Not applicable.

### 12. What Happens When a Contraindication Is Detected
Quarantined lots are immediately excluded from allocation algorithm.

### 13. What Is Stored in the Database
Updates 'inventory' table quantity_on_hand atomically within database transaction.

### 14. What Is Recorded in the Audit Log
Every inventory movement recorded in audit ledger.

### 15. Which Tests Passed
test_45_engines_connected.py (Engine 24), test_phase4_pharmacy_fefo_billing.py (Tests 01, 02, 03, 04).

### 16. Which Tests Failed
Zero failures.

### 17. Whether Clinician Approval Is Required
No — Automated warehouse logistics execution.

---
*Certified under ZAYVORA Health OS Clinical Safety & Software Verification Protocol v5.0*
