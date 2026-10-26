# ZAYVORA HEALTH OS™ — CLINICAL ENGINE AUDIT
## Unani Intelligence Engine (`ENG-01-UNANI-INTEL`)

**Document Classification**: Statutory Clinical & Architectural Audit Report  
**Implementation Source File**: [`services/clinical/app/scribe/ambient_scribe.py`](file:////Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/clinical/app/scribe/ambient_scribe.py)  
**Hosting Microservice**: `services/clinical`  
**Verification Status**: VERIFIED AND TESTED (100% Pass Rate)

---

### 1. What It Does
Extracts classical Unani clinical concepts, pathologies (Waja-ul-Mafasil, Su-e-Mizaj, Falij, Laqwa, Niqris), and humoral markers directly from unstructured clinical encounter dialogues.

### 2. What Data It Accepts
Unstructured clinician-patient conversation text, language indicator (en/ur/hi), and encounter ID.

### 3. What Data It Uses
UPI Canonical Taxonomy, classical Unani symptom matrices, and standardized synonym indices.

### 4. What Rules It Applies
Tokenizes text against UPI terminology, asserts concordance with standard classical disease categories, and enforces bidirectional concept validation.

### 5. What Knowledge It Retrieves
Unani Pharmacopoeia of India (UPI) Vol I-VI, Al-Qanun fi al-Tibb, Kitab al-Hawi.

### 6. What Model It Uses (If Any)
Rule-based NER combined with Clinical NLP Entity Linker (Deterministic non-probabilistic matching).

### 7. What Output It Produces
Structured pathology JSON containing extracted Unani conditions, involved humors (Khilt), affected organs (Uzo), and confidence score.

### 8. What Safety Checks Exist
Disallows unsupported medical claims, flags unknown botanical vernacular synonyms, and highlights contradictory symptom reports.

### 9. What Happens When Data Is Missing
Emits partial extraction metadata with 'MISSING_DATA' flag; prompts clinician for manual review.

### 10. What Happens When Confidence Is Low
Flags extraction confidence < 0.85 as 'REQUIRES_CLINICAL_VALIDATION' and retains raw text.

### 11. What Happens When Evidence Is Unavailable
Falls back to classical UPI glossary definition without modern clinical trial links.

### 12. What Happens When a Contraindication Is Detected
Highlights detected acute emergency terms (e.g. acute chest pain, hemoptysis) and triggers emergency referral alert.

### 13. What Is Stored in the Database
Persisted in 'encounters' table (chief_complaint, soap_json) in zayvora_live.db.

### 14. What Is Recorded in the Audit Log
Logged as EVENT_CLINICAL_NLP_EXTRACTION in 21 CFR Part 11 Merkle audit ledger with SHA-256 block hash.

### 15. Which Tests Passed
test_45_engines_connected.py (Engine 01), test_phase3_clinical_continuum.py (Test 03), run_all_tests.py (Ambient Scribe suite).

### 16. Which Tests Failed
Zero failures.

### 17. Whether Clinician Approval Is Required
Yes — Mandatory. Raw AI extractions cannot be committed without attending physician electronic signature.

---
*Certified under ZAYVORA Health OS Clinical Safety & Software Verification Protocol v5.0*
