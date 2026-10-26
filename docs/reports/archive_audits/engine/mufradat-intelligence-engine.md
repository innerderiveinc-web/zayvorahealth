# ZAYVORA HEALTH OS™ — CLINICAL ENGINE AUDIT
## Mufradat Intelligence Engine (`ENG-04-MUFRADAT-INTEL`)

**Document Classification**: Statutory Clinical & Architectural Audit Report  
**Implementation Source File**: [`services/knowledge/app/core/pharmacopoeia.py`](file:////Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/knowledge/app/core/pharmacopoeia.py)  
**Hosting Microservice**: `services/knowledge`  
**Verification Status**: VERIFIED AND TESTED (100% Pass Rate)

---

### 1. What It Does
Analyzes single botanical drugs, validating binomial nomenclature, part used, temperament degrees (Darja-e-Mizaj), therapeutic actions, and toxicity profiles.

### 2. What Data It Accepts
Botanical name, vernacular synonym, or Latin binomial.

### 3. What Data It Uses
UPI Mufradat Registry (UPI_MUFRADAT_REGISTRY) comprising 100+ fully vetted classical herbs.

### 4. What Rules It Applies
Validates exact botanical part (corm, root, leaf, seed); rejects ambiguous common names.

### 5. What Knowledge It Retrieves
Unani Pharmacopoeia of India Vol I-VI, Makhzan-ul-Mufradat.

### 6. What Model It Uses (If Any)
Deterministic ontology mapping engine.

### 7. What Output It Produces
Mufrad profile JSON with canonical name, temperament, therapeutic actions, daily posology, and Schedule E(1) status.

### 8. What Safety Checks Exist
Flags Schedule E(1) poisons (Suranjan Talkh, Kuchla, Afiyun, Samm-ul-Far); requires Mudabbar verification.

### 9. What Happens When Data Is Missing
Rejects unrecognized herbs with HTTP 404; provides phonetic canonical search suggestions.

### 10. What Happens When Confidence Is Low
Returns ranked list of closest botanical matches requiring explicit clinician disambiguation.

### 11. What Happens When Evidence Is Unavailable
Marks contemporary pharmacological evidence as 'TRADITIONAL_USE_ONLY'.

### 12. What Happens When a Contraindication Is Detected
Triggers DO_NOT_RECOMMEND flag if single herb is contraindicated for patient's physiological state.

### 13. What Is Stored in the Database
Referenced in 'prescriptions' table items_json in zayvora_live.db.

### 14. What Is Recorded in the Audit Log
Logged on prescription compilation in 21 CFR Part 11 audit ledger.

### 15. Which Tests Passed
test_45_engines_connected.py (Engine 05), test_phase5_ai_rag_safety_cds.py (Test 02).

### 16. Which Tests Failed
Zero failures.

### 17. Whether Clinician Approval Is Required
Yes — Selection and administration requires licensed physician authorization.

---
*Certified under ZAYVORA Health OS Clinical Safety & Software Verification Protocol v5.0*
