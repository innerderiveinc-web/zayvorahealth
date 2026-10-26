# ZAYVORA HEALTH OS™ — CLINICAL ENGINE AUDIT
## AI / Hybrid RAG Retrieval Engine (`ENG-24-HYBRID-RAG`)

**Document Classification**: Statutory Clinical & Architectural Audit Report  
**Implementation Source File**: [`services/knowledge/app/core/hybrid_rag.py`](file:////Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/knowledge/app/core/hybrid_rag.py)  
**Hosting Microservice**: `services/knowledge`  
**Verification Status**: VERIFIED AND TESTED (100% Pass Rate)

---

### 1. What It Does
Executes hybrid lexical (BM25 with bi-gram expansion) and dense semantic vector retrieval over indexed classical Unani treatises and pharmacopoeial monographs.

### 2. What Data It Accepts
Natural language clinical query, organ axis filter, Schedule E(1) restriction flag.

### 3. What Data It Uses
Pre-computed dense vector embeddings and BM25 inverted index of UPI monographs.

### 4. What Rules It Applies
Combines lexical and vector scores via Reciprocal Rank Fusion (RRF); filters results strictly to verified peer-reviewed records.

### 5. What Knowledge It Retrieves
UPI Volumes I-VI, NFUM Parts I-VI, Al-Qanun fi al-Tibb, Kitab al-Hawi.

### 6. What Model It Uses (If Any)
Hybrid BM25 + Dense Semantic Vector Retrieval (Chained to local fallback).

### 7. What Output It Produces
Retrieved context chunks JSON with relevance scores, source monograph titles, and verified citations.

### 8. What Safety Checks Exist
Filters out unapproved experimental knowledge; prevents ingestion of unverified web scrapes.

### 9. What Happens When Data Is Missing
Expands search query using classical Arabic/Persian botanical synonyms.

### 10. What Happens When Confidence Is Low
Returns top classical reference texts with explicit low-relevance warning.

### 11. What Happens When Evidence Is Unavailable
Transparently reports absence of matching literature.

### 12. What Happens When a Contraindication Is Detected
Surfaces relevant monograph toxicity warnings directly alongside therapeutic indications.

### 13. What Is Stored in the Database
Reads from knowledge vector/lexical index files.

### 14. What Is Recorded in the Audit Log
RAG retrieval query and retrieved chunk IDs logged with AI consult session.

### 15. Which Tests Passed
test_45_engines_connected.py (Engine 26), test_phase5_ai_rag_safety_cds.py (Test 01).

### 16. Which Tests Failed
Zero failures.

### 17. Whether Clinician Approval Is Required
No — Real-time contextual knowledge retrieval engine.

---
*Certified under ZAYVORA Health OS Clinical Safety & Software Verification Protocol v5.0*
