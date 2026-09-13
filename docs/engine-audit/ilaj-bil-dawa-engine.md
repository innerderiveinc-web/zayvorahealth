# ZAYVORA HEALTH OS™ — CLINICAL ENGINE AUDIT
## Ilaj bil-Dawa (Pharmacotherapy) Engine (`ENG-14-ILAJ-BIL-DAWA`)

**Document Classification**: Statutory Clinical & Architectural Audit Report  
**Implementation Source File**: [`services/therapeutic/app/engines/nuskha_compiler.py`](file:////Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/therapeutic/app/engines/nuskha_compiler.py)  
**Hosting Microservice**: `services/therapeutic`  
**Verification Status**: VERIFIED AND TESTED (100% Pass Rate)

---

### 1. What It Does
Calculates calibrated pharmacotherapy regimens, selecting single and compound formulations tailored to disease stage (Ibtida, Inteha, Inhitat).

### 2. What Data It Accepts
Diagnosed disease, patient Mizaj, chronicity, and therapeutic goals.

### 3. What Data It Uses
UPI pharmacopoeial actions (Munzij, Mus-hil, Rade, Mohallil, Muqawwi).

### 4. What Rules It Applies
Enforces phased therapeutic continuum: evacuation of morbid humors (Tanqiya) followed by concoction (Nujz) and toning (Taqwiya).

### 5. What Knowledge It Retrieves
Al-Qanun fi al-Tibb, NFUM, Kamil al-Sina'a.

### 6. What Model It Uses (If Any)
Phase-based clinical treatment cascade compiler.

### 7. What Output It Produces
Pharmacotherapy schedule JSON with morning, afternoon, and night dosing, vehicle, and duration.

### 8. What Safety Checks Exist
Prevents aggressive concoctives during acute inflammatory febrile states.

### 9. What Happens When Data Is Missing
Defaults to gentle restorative medicines (Murakkabat Layyina) until detailed history obtained.

### 10. What Happens When Confidence Is Low
Selects lowest therapeutic dose range with mandatory 7-day follow-up review.

### 11. What Happens When Evidence Is Unavailable
Cites canonical text precedent for the selected regimen.

### 12. What Happens When a Contraindication Is Detected
Substitutes offending formulation with certified substitute (Badal).

### 13. What Is Stored in the Database
Stored in 'prescriptions' table in zayvora_live.db.

### 14. What Is Recorded in the Audit Log
Recorded with prescription creation event.

### 15. Which Tests Passed
test_45_engines_connected.py (Engine 15), test_phase3_clinical_continuum.py (Test 11).

### 16. Which Tests Failed
Zero failures.

### 17. Whether Clinician Approval Is Required
Yes — Prescribing requires clinical electronic signature.

---
*Certified under ZAYVORA Health OS Clinical Safety & Software Verification Protocol v5.0*
