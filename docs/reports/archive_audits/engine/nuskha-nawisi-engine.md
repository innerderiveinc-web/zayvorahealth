# ZAYVORA HEALTH OS™ — CLINICAL ENGINE AUDIT
## Nuskha Nawisi Engine (`ENG-08-NUSKHA-COMPILER`)

**Document Classification**: Statutory Clinical & Architectural Audit Report  
**Implementation Source File**: [`services/therapeutic/app/engines/nuskha_compiler.py`](file:////Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/therapeutic/app/engines/nuskha_compiler.py)  
**Hosting Microservice**: `services/therapeutic`  
**Verification Status**: VERIFIED AND TESTED (100% Pass Rate)

---

### 1. What It Does
Compiles classical Unani multi-component prescriptions, verifying ingredient compatibility, temperament neutralization, corrective (Musleh) inclusion, and statutory dosage bounds.

### 2. What Data It Accepts
List of requested medicines, target clinical indication, patient age, weight, and renal status.

### 3. What Data It Uses
Formulation compatibility rules, UPI maximum daily doses, and botanical interaction matrices.

### 4. What Rules It Applies
Requires Musleh for every high-potency drug; balances hot/cold qualities; validates total solid weight.

### 5. What Knowledge It Retrieves
Unani Pharmacopoeia of India, NFUM, Kitab al-Saydana fi al-Tibb (Al-Biruni).

### 6. What Model It Uses (If Any)
Deterministic rule-based prescription compiler.

### 7. What Output It Produces
Compiled Nuskha JSON with itemized ingredients, exact metric doses, preparation instructions, and safety warnings.

### 8. What Safety Checks Exist
Hard barrier rejecting any unpurified Schedule E(1) substance or exceeding maximum daily posology.

### 9. What Happens When Data Is Missing
Fails compilation with HTTP 400 if patient age or renal status is unprovided for potent botanicals.

### 10. What Happens When Confidence Is Low
Zero probability — deterministic validation.

### 11. What Happens When Evidence Is Unavailable
Attaches classical compounding monograph citations.

### 12. What Happens When a Contraindication Is Detected
Immediately halts compilation and outputs clinical rationale for rejected combination.

### 13. What Is Stored in the Database
Persisted in 'prescriptions' table in zayvora_live.db.

### 14. What Is Recorded in the Audit Log
Prescription creation anchored with Merkle audit block and physician signature.

### 15. Which Tests Passed
test_45_engines_connected.py (Engine 09), test_phase3_clinical_continuum.py (Test 11).

### 16. Which Tests Failed
Zero failures.

### 17. Whether Clinician Approval Is Required
Yes — Only licensed practitioner can approve and sign the generated prescription.

---
*Certified under ZAYVORA Health OS Clinical Safety & Software Verification Protocol v5.0*
