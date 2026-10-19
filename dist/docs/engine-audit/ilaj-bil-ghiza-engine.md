# ZAYVORA HEALTH OS™ — CLINICAL ENGINE AUDIT
## Ilaj bil-Ghiza (Dietotherapy) Engine (`ENG-15-ILAJ-BIL-GHIZA`)

**Document Classification**: Statutory Clinical & Architectural Audit Report  
**Implementation Source File**: [`services/therapeutic/app/routers/ghiza.py`](file:////Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/therapeutic/app/routers/ghiza.py)  
**Hosting Microservice**: `services/therapeutic`  
**Verification Status**: VERIFIED AND TESTED (100% Pass Rate)

---

### 1. What It Does
Generates customized clinical dietotherapy and dietary restriction (Parhez) protocols, harmonizing food temperament against pathological dyscrasia.

### 2. What Data It Accepts
Patient dominant Mizaj, presenting pathology, food allergies, and comorbidities (diabetes, hypertension).

### 3. What Data It Uses
Unani Food Temperament Matrix (Ghiza-e-Mutlaq, Ghiza-e-Dawai, Dawa-e-Ghidhai).

### 4. What Rules It Applies
Prescribes foods opposing the pathological humor (Ilaj bil-Zid); enforces low glycemic index for metabolic disease.

### 5. What Knowledge It Retrieves
Kitab al-Aghdhiya (Ibn Zuhr / Avenzoar), Al-Qanun fi al-Tibb Book II.

### 6. What Model It Uses (If Any)
Nutritional balancing rule engine.

### 7. What Output It Produces
Dietary prescription JSON detailing recommended foods, strictly prohibited foods (Parhez), and meal timings.

### 8. What Safety Checks Exist
Validates food-allergen conflicts; blocks high-sodium foods in hypertensive/renal patients.

### 9. What Happens When Data Is Missing
Emits standard balanced diet (Ghiza-e-Motadila) pending metabolic labs.

### 10. What Happens When Confidence Is Low
Recommends light, easily digestible broths (Maa-ul-Jubn, Maa-ul-Asl).

### 11. What Happens When Evidence Is Unavailable
Cites Ibn Zuhr classical dietetics references.

### 12. What Happens When a Contraindication Is Detected
Strictly excludes hot/pungent foods in active gastric ulceration or bleeding disorders.

### 13. What Is Stored in the Database
Persisted in 'encounters' (afaal_cascade_json) and printed on A4 prescription letterhead.

### 14. What Is Recorded in the Audit Log
Included in clinical consultation audit record.

### 15. Which Tests Passed
test_45_engines_connected.py (Engine 16), test_phase3_clinical_continuum.py (Test 12).

### 16. Which Tests Failed
Zero failures.

### 17. Whether Clinician Approval Is Required
Yes — Review and approval by attending clinician or clinical nutritionist.

---
*Certified under ZAYVORA Health OS Clinical Safety & Software Verification Protocol v5.0*
