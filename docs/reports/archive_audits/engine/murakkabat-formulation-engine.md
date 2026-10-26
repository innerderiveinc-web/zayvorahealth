# ZAYVORA HEALTH OS™ — CLINICAL ENGINE AUDIT
## Murakkabat / Formulation Engine (`ENG-05-MURAKKABAT-INTEL`)

**Document Classification**: Statutory Clinical & Architectural Audit Report  
**Implementation Source File**: [`services/knowledge/app/core/pharmacopoeia.py`](file:////Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/knowledge/app/core/pharmacopoeia.py)  
**Hosting Microservice**: `services/knowledge`  
**Verification Status**: VERIFIED AND TESTED (100% Pass Rate)

---

### 1. What It Does
Validates classical compound formulations (Majun, Itrifal, Jawarish, Habb, Roghan, Sharbat), asserting component ratios, chief drugs (Juz-e-Azam), and correct vehicles.

### 2. What Data It Accepts
Formulation name, desired dosage form, and clinical indication.

### 3. What Data It Uses
National Formulary of Unani Medicine (NFUM) Parts I-VI and classical Qarabadeen registries.

### 4. What Rules It Applies
Verifies that constituent herbs balance the compound temperament; ensures inclusion of correct corrective (Musleh).

### 5. What Knowledge It Retrieves
NFUM, Qarabadeen-e-Qadri, Qarabadeen-e-Azam.

### 6. What Model It Uses (If Any)
Deterministic formula matrix compiler.

### 7. What Output It Produces
Murakkab formula JSON with standard dosage, vehicle (Anupana / Sheer-e-Gao / Arq), and Mudabbar requirements.

### 8. What Safety Checks Exist
Enforces batch-level Mudabbar certificate validation for all compound formulations containing Schedule E(1) ingredients.

### 9. What Happens When Data Is Missing
Rejects incomplete formulations; requires full specification of excipients and preservation base (Asl / Qand).

### 10. What Happens When Confidence Is Low
Zero probability — strictly matches codified NFUM recipes.

### 11. What Happens When Evidence Is Unavailable
Identifies classical empirical formulations lacking modern randomized controlled trial evidence.

### 12. What Happens When a Contraindication Is Detected
Blocks sugar-based confections (Majun, Jawarish) in diabetic patients (HbA1c > 7.0%).

### 13. What Is Stored in the Database
Persisted in 'prescriptions' and 'inventory' tables in zayvora_live.db.

### 14. What Is Recorded in the Audit Log
Prescription and dispensing events recorded in Merkle audit ledger.

### 15. Which Tests Passed
test_45_engines_connected.py (Engine 06), test_phase4_pharmacy_fefo_billing.py (Test 05).

### 16. Which Tests Failed
Zero failures.

### 17. Whether Clinician Approval Is Required
Yes — Mandatory physician review and digital signature.

---
*Certified under ZAYVORA Health OS Clinical Safety & Software Verification Protocol v5.0*
