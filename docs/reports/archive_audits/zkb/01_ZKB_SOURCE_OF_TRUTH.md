# ZAYVORA KNOWLEDGE BASE™ (ZKB) — SOURCE OF TRUTH & ARCHITECTURAL INVARIANTS
## Foundational Clinical, Epistemological & Engineering Rules

**Document Reference**: `/docs/knowledge-base/01_ZKB_SOURCE_OF_TRUTH.md`  
**Version**: 1.0.0 (Immutable Reference Specification)  
**Date**: September 14, 2026  
**Brand Philosophy**: *Ancient Wisdom. Modern Science. Intelligent Care.*  
**Regulatory Frameworks**: Unani Pharmacopoeia of India (UPI), Drugs & Cosmetics Rules 1945 (Schedule E1), US FDA 21 CFR Part 11, CDSCO GCP Guidelines.

---

## 1. System Invariants & Non-Negotiable Directives

The **ZAYVORA Knowledge Base™ (ZKB)** is not a document library, chatbot database, static JSON repository, or vector-only search cache. It is a **versioned, searchable, multilingual, evidence-linked, safety-governed, and clinician-reviewed Knowledge Operating System**.

The following 10 architectural invariants are permanent and unbreakable:

1. **Strict 9-Tier Knowledge State Machine**:
   Every piece of medical data must pass sequentially through the 9 validated lifecycle stages. No raw, unverified, or automatically parsed text may enter clinical recommendations or prescriptions.
2. **Non-Delegable Human Prescribing Invariant (`safe_to_lock = False`)**:
   AI algorithms, machine learning models, and autonomous copilots are strictly decision-support tools. They cannot approve clinical knowledge, cannot author final prescriptions, and cannot bypass licensed human practitioner review.
3. **Mandatory Page-Level Provenance**:
   Every clinical assertion, drug indication, botanical posology, or safety warning must link cryptographically to a verified source edition, chapter, section, and page number with preserved original text.
4. **Historical vs. Modern Dose Separation**:
   Historical dosages recorded in classical manuscripts (*Dirham*, *Mithqal*, *Masha*, *Ratti*) must never be presented as validated modern clinical dosages. Modern posology requires pharmacopoeial standardization and clinical trial verification.
5. **Botanical Identity Verification**:
   No botanical entity may enter the active clinical formulary without unambiguous taxonomic verification linking classical vernacular names (*Urdu*, *Arabic*, *Persian*) to accepted botanical binominals verified against Plants of the World Online (POWO) and World Flora Online (WFO).
6. **Humoral-Biomedical Epistemological Distinction**:
   Unani pathological concepts (e.g. *Su-e-Mizaj*, *Ghalba-e-Dam*, *Ihtibas-e-Tams*) must never be equated to modern biomedical diagnoses (e.g. Hypertension, Amenorrhea) as identical equivalents without an approved, expert-reviewed cross-walk label (`clinical_analogy`, `probable_mapping`, `expert_verified_mapping`, `not_equivalent`).
7. **Schedule E(1) Statutory Mudabbar Gate**:
   All toxic botanicals, heavy metals, and Schedule E(1) substances must enforce mandatory Mudabbar (detoxification) protocols. Unpurified forms are locked from clinical dispensing.
8. **GRADE Certainty & Evidence Tier Integrity**:
   Classical textual evidence (Tier E0) must never be automatically upgraded to empirical clinical trial evidence (Tier E3–E6) by an AI model without peer-reviewed human validation.
9. **Fail-Closed Safety Firewall**:
   In any scenario involving ambiguous botanical identity, unverified detoxification, patient pregnancy, pediatric use, or severe renal/hepatic impairment, the safety firewall must evaluate to `DO_NOT_RECOMMEND` or `CLINICIAN_REVIEW_REQUIRED`.
10. **Zero Developer Jargon in Clinical Frontends**:
    All patient-, doctor-, and pharmacist-facing interfaces must render purely clinical, empathetic, and human-readable terminology. System traces, database codes, or raw JSON errors are prohibited.

---

## 2. The 9-Tier Knowledge Progression Lifecycle

Every knowledge entity in ZKB transitions through the following formal state machine:

```text
+----------------------------------------------------------------------------------------------------+
|                               THE 9-TIER KNOWLEDGE PROGRESSION ENUM                                |
+----------------------------------------------------------------------------------------------------+
|  1. ORIGINAL_SOURCE         Original physical manuscript, book edition, or regulatory gazette      |
|         |                                                                                          |
|         v                                                                                          |
|  2. EXTRACTED_TEXT          Raw digital capture, scanned page image, or raw PDF text stream        |
|         |                                                                                          |
|         v                                                                                          |
|  3. OCR_TEXT                Algorithmic OCR text with character confidence score & word boundaries |
|         |                                                                                          |
|         v                                                                                          |
|  4. TRANSLATION             Verified multi-lingual translation (Arabic/Urdu/Persian -> English)    |
|         |                                                                                          |
|         v                                                                                          |
|  5. STRUCTURED_KNOWLEDGE    Parsed entities (Mufrad, Murakkab, Mizaj, Af'al, Indications, Dosing)  |
|         |                                                                                          |
|         v                                                                                          |
|  6. EXPERT_REVIEWED         Attested by Unani Philologist and Biomedical Subject-Matter Expert     |
|         |                                                                                          |
|         v                                                                                          |
|  7. CLINICALLY_APPROVED     Signed by Senior Clinical Specialist with 21 CFR Part 11 Digital Seal  |
|         |                                                                                          |
|         v                                                                                          |
|  8. AI_AVAILABLE            Indexed for Hybrid RAG, Hakeem Sahab™ copilot, and CDS prompting      |
|         |                                                                                          |
|         v (If contradicted, unsafe, or superseded)                                                 |
|  9. RESTRICTED_OR_RETIRED   Locked from clinical recommendations; retained for audit & research    |
+----------------------------------------------------------------------------------------------------+
```

### Stage Transition Criteria & Authorization Gates

| State | Definition | Entry Criteria | Authorized Roles | Access Scope |
| :--- | :--- | :--- | :--- | :--- |
| **1. ORIGINAL_SOURCE** | Primary manuscript, printed edition, or pharmacopoeia. | Physical acquisition, bibliographical cataloging, rights status verification. | Knowledge Curator | Internal Archivists |
| **2. EXTRACTED_TEXT** | Raw file storage and page segmentation. | High-resolution image scan (>= 300 DPI) or validated digital text. | Ingestion Pipeline | Ingestion Workers |
| **3. OCR_TEXT** | Machine-read textual layer. | Multilingual OCR run (Tesseract / EasyOCR / Vision model); confidence recorded. | OCR Worker | Curators |
| **4. TRANSLATION** | Human- or MT-assisted translation with verification. | Dual-column original script and English/Hindi target translation. | Language Expert | Reviewers |
| **5. STRUCTURED_KNOWLEDGE** | Entity-attribute extraction. | Normalized fields: canonical name, botanical binominal, Mizaj, Af'al, doses. | Knowledge Engineer | Curators |
| **6. EXPERT_REVIEWED** | Unani classical & biomedical validation. | Verified by BUMS/MD Unani specialist; botanical identity confirmed. | Unani Expert | Reviewers |
| **7. CLINICALLY_APPROVED** | Formal clinical governance sign-off. | Quorum approval by Governance Board (>= 2 Senior Clinicians). | Clinical Board | Clinical Staff |
| **8. AI_AVAILABLE** | Active for clinical decision support. | Embedded into vector store, BM25 index, and knowledge graph. | AI Engine | Doctors, Copilot |
| **9. RESTRICTED_OR_RETIRED** | Decommissioned or safety-quarantined. | Toxic alert, regulatory withdrawal, or historical contradiction. | Governance Lead | Research Only |

---

## 3. Source Rights and Provenance Framework

ZKB strictly enforces legal rights verification before ingestion:

```text
rights_status:
- VERIFIED_PUBLIC_DOMAIN   (Pre-1928 classical texts, government pharmacopoeias)
- LICENSED                 (Explicit publisher contract with active agreement ID)
- PERMISSION_REQUIRED      (Copyrighted contemporary translation awaiting clearance)
- RESTRICTED               (Confidential clinical trial or internal institutional data)
- UNKNOWN                  (Default state on upload; blocks clinical indexing)
- REJECTED                 (Copyright infringement or unverified origin; purge queue)

clinical_access:
- RESEARCH_ONLY            (Accessible solely to academic researchers; blocked from CDS)
- EXPERT_REVIEW_REQUIRED   (Pending philological or botanical authentication)
- CLINICAL_REVIEW_REQUIRED (Pending senior physician safety review)
- CLINICALLY_APPROVED      (Fully approved for doctor consultation & prescription support)
- BLOCKED                  (Hard safety firewall lock; completely excluded from retrieval)
```

---

## 4. Multi-World Epistemological Model

ZKB structures all health knowledge across **Four Intersecting Worlds**:

1. **World A: Classical Unani Epistemology**
   - Foundation: *Al-Qanoon fit-Tibb*, *Kitab al-Hawi*, *Makhzan-ul-Adwiya*, *Kamil-us-Sana'a*.
   - Concepts: *Mizaj* (temperaments), *Akhlat* (humors), *Quwa* (faculties), *Arwah* (pneuma), *Asbab-e-Sittah Zarooriyyah* (six essential lifestyle factors).
   - Evidence Tier: E0 (Classical Literature).
2. **World B: Contemporary Pharmacopoeial & Regulatory Standards**
   - Foundation: Unani Pharmacopoeia of India (UPI), National Formulary of Unani Medicine (NFUM), Schedule E(1) Drugs & Cosmetics Rules 1945.
   - Concepts: Physico-chemical TLC/HPLC fingerprints, ash values, Mudabbar certification, statutory posology limits.
   - Evidence Tier: E1 (Official Pharmacopoeial Standards).
3. **World C: Empirical Biomedical & Clinical Trial Literature**
   - Foundation: PubMed/MEDLINE peer-reviewed studies, randomized controlled trials, Cochrane systematic reviews, in-vitro bioassays.
   - Concepts: Pharmacokinetics, receptor affinities, anti-inflammatory cytokine assays (TNF-alpha, IL-6), toxicology.
   - Evidence Tier: E2 through E6.
4. **World D: Real-World Evidence & Practice Data (RWE/RWD)**
   - Foundation: ZAYVORA longitudinal patient registry, de-identified electronic health records, post-marketing pharmacovigilance (ICH E2B).
   - Concepts: Real-world patient response trajectories, longitudinal PROMs, adverse event monitoring.

---

## 5. Provenance Traceability Requirement for AI Decision Support

Every response generated by the Hakeem Sahab™ clinical copilot must satisfy the **ZKB Grounding Contract**:

```json
{
  "claim": "Suranjan Talkh (Colchicum luteum) is effective in acute podagra (Niqras) but requires mandatory Mudabbar boiling in cow's milk.",
  "provenance": {
    "source_id": "SRC-UPI-VOL1",
    "source_title": "Unani Pharmacopoeia of India, Part I, Volume I",
    "edition": "First Edition, 2007",
    "page_number": 80,
    "chapter": "Monographs: Single Drugs of Plant Origin",
    "original_text_snippet": "Suranjan Talkh consists of dried corm of Colchicum luteum Baker... It is poisonous and must be purified before use.",
    "original_language": "en",
    "rights_status": "VERIFIED_PUBLIC_DOMAIN",
    "knowledge_world": "B",
    "evidence_level": "E1",
    "reviewer_id": "REV-CCIM-2004",
    "clinical_status": "CLINICALLY_APPROVED",
    "digital_seal_sha256": "4adc67c8947932f9e1b1a2..."
  }
}
```

If an AI assertion cannot produce an unbroken provenance trail linking to an approved source, the assertion is discarded by the Response Validator prior to rendering.
