# ZAYVORA HEALTH OS™ — CLINICAL ENGINE AUDIT
## Ilaj bil-Tadbeer (Regimenal Therapy) Engine (`ENG-16-ILAJ-BIL-TADBEER`)

**Document Classification**: Statutory Clinical & Architectural Audit Report  
**Implementation Source File**: [`services/therapeutic/app/engines/tadbeer_guardrails.py`](file:////Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/therapeutic/app/engines/tadbeer_guardrails.py)  
**Hosting Microservice**: `services/therapeutic`  
**Verification Status**: VERIFIED AND TESTED (100% Pass Rate)

---

### 1. What It Does
Prescribes and validates physical regimenal procedures (Hijama/Cupping, Fasd/Venesection, Nutool/Irrigation, Dalak/Massage, Hammam/Bath, Tareeq/Diaphoresis).

### 2. What Data It Accepts
Proposed procedure, clinical indication, patient blood pressure, hemoglobin, coagulation status, pregnancy.

### 3. What Data It Uses
AYUSH Standard Operating Procedures for Regimenal Therapies, surgical contraindication rules.

### 4. What Rules It Applies
Enforces strict vital sign safety gates (e.g. SBP > 90 mmHg, Hb > 10 g/dL for Fasd); restricts Hijama in anticoagulant therapy.

### 5. What Knowledge It Retrieves
Al-Tasrif (Al-Zahrawi), Kitab al-Mukhtarat fi al-Tibb (Ibn Hubal).

### 6. What Model It Uses (If Any)
Deterministic procedural safety guardrail engine.

### 7. What Output It Produces
Tadbeer clinical order JSON with anatomical sites, duration, pre-procedure preparation, and post-procedure monitoring.

### 8. What Safety Checks Exist
Hard barrier preventing invasive evacuative regimens in severe anemia, pregnancy, or hemodynamic instability.

### 9. What Happens When Data Is Missing
Fails procedure authorization if baseline vitals are not documented within 2 hours.

### 10. What Happens When Confidence Is Low
Requires senior clinical supervisor review before procedural clearance.

### 11. What Happens When Evidence Is Unavailable
Provides historical procedural guidelines from Al-Zahrawi.

### 12. What Happens When a Contraindication Is Detected
Immediately halts scheduling and logs safety refusal reason.

### 13. What Is Stored in the Database
Stored in 'encounters' (afaal_cascade_json) in zayvora_live.db.

### 14. What Is Recorded in the Audit Log
Regimenal order creation and consent verification logged in 21 CFR Part 11 audit ledger.

### 15. Which Tests Passed
test_45_engines_connected.py (Engine 17), test_phase3_clinical_continuum.py (Test 12).

### 16. Which Tests Failed
Zero failures.

### 17. Whether Clinician Approval Is Required
Yes — Mandatory. Procedure cannot be scheduled without doctor authorization.

---
*Certified under ZAYVORA Health OS Clinical Safety & Software Verification Protocol v5.0*
