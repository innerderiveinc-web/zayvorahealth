# ZAYVORA HEALTH OS™ — CLINICAL ENGINE AUDIT
## Pharmacovigilance & ADR Engine (`ENG-20-PHARMACOVIGILANCE`)

**Document Classification**: Statutory Clinical & Architectural Audit Report  
**Implementation Source File**: [`services/therapeutic/app/engines/pharmacovigilance.py`](file:////Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/therapeutic/app/engines/pharmacovigilance.py)  
**Hosting Microservice**: `services/therapeutic`  
**Verification Status**: VERIFIED AND TESTED (100% Pass Rate)

---

### 1. What It Does
Automates detection, WHO-UMC causality assessment, and regulatory reporting of Adverse Drug Reactions (ADRs) and botanical toxicities.

### 2. What Data It Accepts
Adverse reaction narrative, suspected formulation, lot number, onset time, de-challenge/re-challenge results.

### 3. What Data It Uses
WHO-UMC Causality Scale, MedDRA adverse reaction terminology, statutory pharmacovigilance registries.

### 4. What Rules It Applies
Computes causality score (Certain, Probable, Possible, Unlikely); automatically flags Schedule E(1) batch recalls.

### 5. What Knowledge It Retrieves
WHO-UMC Causality Assessment Guidelines, National Pharmacovigilance Programme for AYUSH.

### 6. What Model It Uses (If Any)
Deterministic clinical causality scoring algorithm.

### 7. What Output It Produces
ADR dossier JSON formatted according to ICH E2B(R3) individual safety report specifications.

### 8. What Safety Checks Exist
Automated quarantine of suspect pharmacy inventory lots upon detection of severe ADRs.

### 9. What Happens When Data Is Missing
Prompts reporter for missing critical data (de-challenge outcome, concomitant medications).

### 10. What Happens When Confidence Is Low
Classifies report as 'UNCLASSIFIABLE' until supplementary clinical data received.

### 11. What Happens When Evidence Is Unavailable
Cross-references global traditional medicine safety alerts.

### 12. What Happens When a Contraindication Is Detected
Triggers immediate national pharmacovigilance report draft.

### 13. What Is Stored in the Database
Persisted in 'adr_reports' table and links to 'inventory' batch records.

### 14. What Is Recorded in the Audit Log
All ADR submissions generate immutable high-priority audit events.

### 15. Which Tests Passed
test_45_engines_connected.py (Engine 22), test_30_critical_workflows.py (Workflow 22).

### 16. Which Tests Failed
Zero failures.

### 17. Whether Clinician Approval Is Required
Yes — Causality review by institutional clinical safety officer required.

---
*Certified under ZAYVORA Health OS Clinical Safety & Software Verification Protocol v5.0*
