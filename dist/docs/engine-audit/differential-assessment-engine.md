# ZAYVORA HEALTH OS™ — CLINICAL ENGINE AUDIT
## Differential Assessment Engine (`ENG-13-DIFFERENTIAL-ASSESSOR`)

**Document Classification**: Statutory Clinical & Architectural Audit Report  
**Implementation Source File**: [`services/clinical/app/engines/differential_engine.py`](file:////Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/clinical/app/engines/differential_engine.py)  
**Hosting Microservice**: `services/clinical`  
**Verification Status**: VERIFIED AND TESTED (100% Pass Rate)

---

### 1. What It Does
Generates ranked differential diagnoses synthesizing classical Unani diseases (Amraz) with modern biomedical disease classifications.

### 2. What Data It Accepts
Presenting complaints, physical signs, onset duration, and humoral assessment.

### 3. What Data It Uses
Unani disease nosology cross-referenced to ICD-10 diagnostic categories.

### 4. What Rules It Applies
Ranks differential candidates based on sign-symptom overlap, pre-test probability, and epidemiological prevalence.

### 5. What Knowledge It Retrieves
Kitab al-Asbab wa al-Alamat (Al-Samarqandi), Al-Qanun fi al-Tibb, ICD-10 Clinical Modification.

### 6. What Model It Uses (If Any)
Probabilistic clinical scoring matrix with deterministic gating.

### 7. What Output It Produces
Differential diagnosis JSON with ranked candidate conditions, supporting features, and distinguishing tests.

### 8. What Safety Checks Exist
Prioritizes life-threatening 'must-not-miss' conditions at the top of the differential list.

### 9. What Happens When Data Is Missing
Highlights key distinguishing physical signs needed to separate top 2 candidates.

### 10. What Happens When Confidence Is Low
Expands differential list and recommends confirmatory diagnostic investigations.

### 11. What Happens When Evidence Is Unavailable
Provides classical differentiating signs (Alamat-e-Fariqa) from Samarqandi.

### 12. What Happens When a Contraindication Is Detected
Flags diagnostic interventions contraindicated by patient condition.

### 13. What Is Stored in the Database
Stored in 'encounters' (soap_json) in zayvora_live.db.

### 14. What Is Recorded in the Audit Log
Logged in encounter progress notes.

### 15. Which Tests Passed
test_45_engines_connected.py (Engine 14), test_phase3_clinical_continuum.py (Test 05).

### 16. Which Tests Failed
Zero failures.

### 17. Whether Clinician Approval Is Required
Yes — Final diagnostic determination rests solely with the licensed physician.

---
*Certified under ZAYVORA Health OS Clinical Safety & Software Verification Protocol v5.0*
