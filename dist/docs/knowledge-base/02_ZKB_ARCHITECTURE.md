# ZAYVORA Knowledge Base™ (ZKB) — System Architecture Specification

**Document Identifier**: `ZKB-ARCH-002`  
**Classification**: Enterprise Clinical Knowledge Architecture  
**Status**: DRAFT / UNDER REVIEW (Phase 1 Deliverable)  
**Brand Philosophy**: *Ancient Wisdom. Modern Science. Intelligent Care.*

---

## 1. Executive Architectural Overview

The **ZAYVORA Knowledge Base™ (ZKB)** is not a static document repository, naive vector index, or disconnected chatbot prompt layer. It is an authoritative, multi-tiered, source-grounded **Clinical Knowledge Operating System**. 

ZKB sits at the exact intersection of:
1. **Classical Unani Medicine**: Preserving canonical epistemology (*Kulliyat*, *Mizaj*, *Akhlat*, *Arwah*, *Aza*, *Quwa*, *Af'al*), textual authenticity, and traditional compounding methodologies (*Ilaj bil-Dawa*, *Ilaj bil-Ghiza*, *Ilaj bil-Tadbeer*).
2. **Modern Biomedical Science**: Incorporating clinical pharmacology, botanical taxonomy (POWO/WFO), pharmacognosy, toxicological limits, and contemporary disease taxonomies (ICD-11, SNOMED-CT).
3. **Evidence-Based Governance**: Applying formal E0–E6 evidence grading, GRADE certainty scoring, human-in-the-loop expert quorums, and cryptographic audit trails.

### Architectural Core Invariant
> **The Clinical Provenance Invariant**: No medical fact, dosage, formulation, or therapeutic claim may be served to a clinician, patient, or artificial intelligence inference model without an unbroken, cryptographically verified chain of custody tracing directly to an authenticated source edition, volume, and page number.

---

## 2. End-to-End System Topology

The ZKB platform is structured across six decoupled yet tightly integrated architectural layers:

```
+---------------------------------------------------------------------------------------------------+
|                                 1. SOURCE ACQUISITION & INGESTION LAYER                           |
|  [Manuscripts / Rare Editions] --> [Digital Scans (TIFF/PDF)] --> [Rights & Provenance Registry] |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+-------------------------------------------------+-------------------------------------------------+
|                                    2. MULTILINGUAL OCR & SEGMENTATION                             |
|  [Arabic / Urdu Nastaliq Engine] --> [Segment Bounding Boxes] --> [Human Transcription Desk]     |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+-------------------------------------------------+-------------------------------------------------+
|                                 3. RELATIONAL PROVENANCE REPOSITORY                               |
|  [Source Books] -> [Editions] -> [Pages] -> [Passages] -> [Translations] -> [Entity Linkages]     |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                         +------------------------+------------------------+
                         |                                                 |
                         v                                                 v
+------------------------+------------------------+  +---------------------+------------------------+
|           4. MULTI-HOP KNOWLEDGE GRAPH          |  |         5. SOURCE-GROUNDED HYBRID RAG        |
|  (Neo4j Enterprise / In-Memory Core Engine)     |  |  - Multilingual BM25 Lexical Stemmer         |
|  - Nodes: Herbs, Compounds, Mizaj, Organ-Axes   |  |  - Dense Clinical Embeddings (BioBERT/Custom)|
|  - Edges: Detoxified_By, Treats, Contraindicated|  |  - Reciprocal Rank Fusion (RRF @ k=60)       |
+------------------------+------------------------+  +---------------------+------------------------+
                         |                                                 |
                         +------------------------+------------------------+
                                                  |
                                                  v
+-------------------------------------------------+-------------------------------------------------+
|                       6. DETERMINISTIC CLINICAL SAFETY FIREWALL & GATEWAY                         |
|  - Statutory Schedule E(1) Poison Hard Stop     - Pregnancy / Renal / Hepatic Contraindication    |
|  - Mandatory Mudabbar Detoxification Gate       - Multi-Clinician Quorum Attestation Gate         |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+-------------------------------------------------+-------------------------------------------------+
|                             7. ROLE-BASED CONSUMPTION INTERFACES                                  |
|  [Curator Desk]  [Unani Scholar Desk]  [Clinician Desk]  [Hakeem Sahab AI]  [Pharmacy / eBMR]     |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Layer-by-Layer Architectural Specification

### 3.1 Layer 1: Source Acquisition & Rights Governance
- **Purpose**: Ingestion of historical classical manuscripts, authoritative pharmacopoeias (UPI, NFUM, IP, BHP), and modern clinical trials.
- **Components**:
  - `SourceDocumentIngestionPipeline`: Accepts multi-page high-resolution TIFF, PDF, and image containers.
  - `RightsVerificationEngine`: Enforces Public Domain vs. Copyrighted status before ingestion. For commercial texts, it stores licensing expiration dates and usage quotas.
  - `CryptographicHasher`: Generates SHA-256 digests for raw uploaded assets to guarantee tamper-proof bitstream provenance.

### 3.2 Layer 2: Multilingual OCR, Segmentation & Correction Desk
- **Purpose**: High-fidelity extraction of non-Latin, cursive, and calligraphic medical literature.
- **Supported Scripts**:
  - Arabic (*Naskh*, *Muhaqqaq* classical medical manuscripts).
  - Urdu (*Nastaliq* calligraphy, Persian-Arabic ligature joins).
  - Persian (*Farsi* historical treatises such as *Zakhira-i Khwarizmshahi*).
  - Hindi / Sanskrit (*Devanagari* references for cross-system pharmacognosy).
  - Latin / English (Modern pharmacological publications, UPI English editions).
- **Architecture**:
  - Layout Analysis: Identifies margins, headers, marginalia (*hashiya*), footnotes, and tabular compounding recipes.
  - Line and Word Bounding Box Generation: Every extracted word retains `[x_min, y_min, x_max, y_max]` relative coordinates on the parent page scan.
  - Confidence Scoring: Each token receives a confidence score (0.00 to 1.00). Any passage with an aggregate confidence below 0.95 is automatically routed to the **Human Transcription Correction Desk**.
  - No unverified OCR text may transition to `STRUCTURED_KNOWLEDGE` without human scholar validation.

### 3.3 Layer 3: Relational Provenance Repository (PostgreSQL)
- **Purpose**: The immutable database of record for all normalized knowledge structures.
- **Relational Integrity**:
  - Strict Foreign Key hierarchies: `source_books` -> `source_editions` -> `source_pages` -> `source_passages` -> `source_translations`.
  - Versioning: Append-only ledger using temporal timestamps (`valid_from`, `valid_to`) and audit IDs. Records are never deleted in place; superseding entries increment minor/major version counters.
  - Granular Evidence Leveling: Every structured passage assigns an initial evidence tier ($E_0$ to $E_6$).

### 3.4 Layer 4: Multi-Hop Knowledge Graph (Neo4j & In-Memory Engine)
- **Purpose**: Contextual, non-linear reasoning across multi-dimensional traditional and modern clinical concepts.
- **Domain Topology**:
  - **Node Labels**:
    - `Herb` (Botanical name, UPI ID, canonical Arabic/Urdu name).
    - `PlantPart` (Root, leaf, gum-resin, bark, seeds).
    - `Formulation` (Classical compound, e.g., Majun, Khamira, Sharbat).
    - `Mizaj` (Heat, Cold, Moisture, Dryness degrees 1 through 4).
    - `OrganAxis` (The 12 physiological axes: Neuro-Cerebral, Hepato-Digestive, etc.).
    - `Disease` (Unani *Marad* linked to modern ICD-11 / SNOMED-CT).
    - `ActivePhytochemical` (Thymol, Glycyrrhizin, Strychnine, Curcumin).
    - `ModernDrug` (Warfarin, Metformin, Digoxin, Aspirin).
  - **Edge Semantics**:
    - `(:Herb)-[:HAS_MIZAJ {degree: 2}]->(:Mizaj)`
    - `(:Herb)-[:AFFECTS_AXIS {action: 'Muqawwi'}]->(:OrganAxis)`
    - `(:Formulation)-[:CONTAINS_INGREDIENT {ratio: 0.15}]->(:Herb)`
    - `(:Herb)-[:DETOXIFIED_BY]->(:MudabbarProtocol)`
    - `(:Herb)-[:INTERACTS_WITH {severity: 'CRITICAL'}]->(:ModernDrug)`
    - `(:Herb)-[:TREATS {evidence_tier: 'E2'}]->(:Disease)`

### 3.5 Layer 5: Source-Grounded Hybrid RAG & Vector Engine
- **Purpose**: Context retrieval for clinician search and AI clinical copilots that eliminates hallucinations.
- **Hybrid Retrieval Architecture**:
  - **Lexical BM25 Channel**: Tokenizes medical query terms using specialized Arabic/Urdu morphology stemmers and botanical synonyms. Essential for exact classical entity matches (e.g., searching for *Ustukhuddus* or *Lavandula stoechas*).
  - **Dense Vector Channel**: Generates 1536-dimensional embeddings for passages using clinical language models. Captures semantic symptoms, therapeutic actions, and patient narratives.
  - **Reciprocal Rank Fusion (RRF)**: Merges rank positions from lexical and dense pipelines:
    $$RRF\_Score(d) = \sum_{m \in \{lexical, dense\}} \frac{1}{k + rank_m(d)} \quad (k = 60)$$
  - **Negative Evidence & Restriction Filter**: Post-fusion filter strictly strips any candidate passage that has status `RESTRICTED_OR_RETIRED` or lacks `safe_for_ai = True`.
  - **Citation Grounding Layer**: Formats extracted chunks with verified cryptographic citation headers:
    `[Source: UPI Vol 1, Ed. 2007, Page 42, ISBN: 978-81-901151-4-8, Digest: a3f9...]`.

### 3.6 Layer 6: Deterministic Clinical Safety Firewall
- **Purpose**: Non-bypassable rule engine that acts as a gatekeeper before any knowledge record, recommendation, or formula is rendered to a physician or patient.
- **Invariants Enforced**:
  1. **Schedule E(1) Statutory Poison Interceptor**: Any herb listed in the statutory poison register (e.g., *Azaraqi* / Strychnos nux-vomica, *Aconite*, *Afiyun*) requires verified proof of *Mudabbar* (detoxification) processing.
  2. **Maximum Single & Daily Dose Ceilings**: Strict numeric ceiling checks. If a formula or prescription exceeds the modern pharmacopoeial limit, it throws a blocking exception (`ExceededTherapeuticLimitException`).
  3. **Vulnerable Population Gates**: Automatic contraindication flags for pregnancy, lactation, pediatric (under 12 years), and geriatric (65 years and older) cohorts.
  4. **Organ Impairment Interceptor**: Blocks nephrotoxic or hepatotoxic herbs if patient lab records indicate renal or hepatic dysfunction.

### 3.7 Layer 7: Five Role-Based Operational Frontends
1. **Curator Workbench**: Document ingestion, scan quality control, metadata tagging, and rights ledger management.
2. **Unani Scholar Workbench**: Parallel layout viewer for bilingual translation, classical concept tagging (*Af'al*, *Khas Parwarish*), and OCR correction.
3. **Clinical Reviewer Desk**: Comparative analysis of historical dosage versus approved modern pharmacopoeial thresholds, toxicological verification, and evidence tier grading.
4. **Research & Analytics Portal**: High-throughput population queries, phytochemistry correlations, cross-system drug-herb interaction matrices.
5. **Governance & Audit Console**: Quorum voting on change orders, cryptographic sealing of monographs, revision history, and compliance logging.

---

## 4. Hardware & Deployment Topology

```
+---------------------------------------------------------------------------------------------------+
|                                  KUBERNETES / CONTAINER CLUSTER                                   |
|                                                                                                   |
|  +--------------------------------+   +---------------------------------+                         |
|  |  apps/web (Next.js 14 Frontend)|   |  services/knowledge (FastAPI)   |                         |
|  |  - Node.js 20 LTS Engine       |   |  - Python 3.11 ASGI Engine      |                         |
|  |  - Port 3000                   |   |  - Port 8002                    |                         |
|  +---------------+----------------+   +----------------+----------------+                         |
|                  |                                     |                                          |
|                  v                                     v                                          |
|  +--------------------------------+   +----------------+----------------+                         |
|  |  services/api (Live Gateway)   |   |  services/ai (Clinical Engine)  |                         |
|  |  - Python 3.11 ASGI Engine     |   |  - LangChain / RAG Pipeline     |                         |
|  |  - Port 8000                   |   |  - Port 8001                    |                         |
|  +---------------+----------------+   +----------------+----------------+                         |
|                  |                                     |                                          |
|                  +------------------+------------------+                                          |
|                                     |                                                             |
|                                     v                                                             |
|  +---------------------------------------------------------------------+                          |
|  |                          PERSISTENCE TIER                           |                          |
|  |  - Relational: PostgreSQL 16 (Source of Record, RBAC, Ledger)       |                          |
|  |  - Graph: Neo4j 5.x Enterprise (Knowledge & Formulation Graph)       |                          |
|  |  - Vector: pgvector / Qdrant (Clinical & Classical Embeddings)      |                          |
|  |  - Cache & Bus: Redis 7.x (Session, Invalidation, Quorum Events)   |                          |
|  +---------------------------------------------------------------------+                          |
+---------------------------------------------------------------------------------------------------+
```

---

## 5. Security, Tenancy & Compliance Boundaries

1. **Multi-Tenancy Isolation**:
   - Master knowledge records are globally shared and immutable.
   - Clinic-specific custom formulations or proprietary research notes are partitioned using strict PostgreSQL Row-Level Security (`clinic_id` scoping).
2. **Access Control (RBAC)**:
   - `KNOWLEDGE_CURATOR`: Can ingest documents and submit OCR corrections.
   - `UNANI_SCHOLAR`: Can edit classical concepts and draft translations.
   - `CLINICAL_REVIEWER`: Can modify modern approved dosages and certify evidence tiers.
   - `CHIEF_MEDICAL_OFFICER`: Can cast final quorum votes to unlock `AI_AVAILABLE` status.
3. **Data Loss Prevention**:
   - Point-in-time recovery (PITR) enabled on relational stores.
   - All OCR correction transactions recorded in append-only audit ledgers.

---

## 6. Verification and Validation Criteria

- **Latency Budgets**:
  - Relational lookup by UPI monograph ID: < 15 ms (p95).
  - Multi-hop graph path resolution (up to 3 hops): < 45 ms (p95).
  - Hybrid RAG retrieval + RRF fusion: < 120 ms (p95).
  - Deterministic Safety Firewall pass-through: < 5 ms (p99).
- **Correctness Guarantees**:
  - Zero hallucination rate: Any clinical AI response without a direct citation link fails safety evaluation.
  - Zero unverified toxic release: Schedule E(1) ingredients lacking verified Mudabbar certification throw non-recoverable pipeline errors.

---
*Signed and Approved for Architecture Baseline:*  
**Principal Healthcare Software Architect & Lead Clinical Safety Engineer**
