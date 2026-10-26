# ZAYVORA Knowledge Base™ (ZKB) — Data Model & Schema Specification

**Document Identifier**: `ZKB-DATA-003`  
**Classification**: Enterprise Clinical Data Architecture  
**Status**: DRAFT / UNDER REVIEW (Phase 1 Deliverable)  
**Target RDBMS**: PostgreSQL 16 (Relational & Temporal Ledger)  
**Target Graph DB**: Neo4j 5.x Enterprise (Multi-Hop Knowledge Graph)

---

## 1. Relational Data Model Architecture

The ZKB relational model provides an immutable, auditable, source-of-record substrate. It supports temporal versioning, cryptographic provenance, multilingual translations, multi-clinician quorum reviews, and regulatory pharmacopoeial compliance.

---

### 1.1 Source Library & Provenance Subsystem

#### 1. `source_authors`
Stores canonical historical scholars, translators, and modern editorial committees.
```sql
CREATE TABLE source_authors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    canonical_name VARCHAR(255) NOT NULL,
    arabic_name VARCHAR(255),
    persian_name VARCHAR(255),
    urdu_name VARCHAR(255),
    era_hijri VARCHAR(64),
    era_ce VARCHAR(64),
    biography_summary TEXT,
    is_classical BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_source_authors_canonical ON source_authors(canonical_name);
```

#### 2. `source_books`
Master registry of classical treatises, modern pharmacopoeias, and research compendiums.
```sql
CREATE TABLE source_books (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    primary_author_id UUID REFERENCES source_authors(id) ON DELETE RESTRICT_OR_CASCADE,
    canonical_title VARCHAR(255) NOT NULL,
    original_title VARCHAR(255) NOT NULL,
    transliterated_title VARCHAR(255),
    language_code VARCHAR(10) NOT NULL, -- ar, ur, fa, hi, en
    discipline VARCHAR(64) NOT NULL, -- Kulliyat, Mufradat, Murakkabat, Moalajat, Jarahat
    historical_era VARCHAR(64),
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_source_books_title ON source_books(canonical_title);
```

#### 3. `source_editions`
Physical and digital print editions, critical recensions, and translations.
```sql
CREATE TABLE source_editions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id UUID NOT NULL REFERENCES source_books(id) ON DELETE RESTRICT,
    editor_translator VARCHAR(255),
    publisher VARCHAR(255) NOT NULL,
    publication_year INTEGER NOT NULL,
    publication_place VARCHAR(128),
    edition_number VARCHAR(32),
    volume_number VARCHAR(16),
    isbn_issn VARCHAR(32),
    total_pages INTEGER NOT NULL,
    call_number VARCHAR(64),
    digital_scan_url TEXT,
    sha256_checksum VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_source_editions_book ON source_editions(book_id);
CREATE UNIQUE INDEX uq_source_edition_checksum ON source_editions(sha256_checksum);
```

#### 4. `source_rights`
Legal copyright, public domain clearance, and institutional licensing limits.
```sql
CREATE TABLE source_rights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    edition_id UUID NOT NULL REFERENCES source_editions(id) ON DELETE CASCADE,
    license_type VARCHAR(64) NOT NULL, -- PUBLIC_DOMAIN, CC_BY_SA, INSTITUTIONAL_SUBSCRIPTION, ALL_RIGHTS_RESERVED
    rights_holder VARCHAR(255),
    licensed_to_facility VARCHAR(255),
    valid_from DATE NOT NULL,
    valid_until DATE,
    commercial_use_permitted BOOLEAN NOT NULL DEFAULT FALSE,
    ai_training_permitted BOOLEAN NOT NULL DEFAULT FALSE,
    verified_by_legal_officer VARCHAR(255) NOT NULL,
    verified_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_source_rights_edition ON source_rights(edition_id);
```

#### 5. `source_pages`
High-resolution page scans, dimensional metadata, and orientation records.
```sql
CREATE TABLE source_pages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    edition_id UUID NOT NULL REFERENCES source_editions(id) ON DELETE RESTRICT,
    page_number INTEGER NOT NULL,
    folio_recto_verso VARCHAR(8), -- 12a, 12b, 1r, 1v
    image_storage_uri TEXT NOT NULL,
    image_mime_type VARCHAR(32) NOT NULL DEFAULT 'image/tiff',
    width_px INTEGER NOT NULL,
    height_px INTEGER NOT NULL,
    dpi INTEGER NOT NULL DEFAULT 300,
    sha256_page_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_edition_page UNIQUE (edition_id, page_number)
);
CREATE INDEX idx_source_pages_edition ON source_pages(edition_id, page_number);
```

#### 6. `source_passages`
Segmented textual passages with coordinate-level bounding box grounding.
```sql
CREATE TABLE source_passages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    page_id UUID NOT NULL REFERENCES source_pages(id) ON DELETE RESTRICT,
    passage_order INTEGER NOT NULL,
    original_text TEXT NOT NULL,
    normalized_text TEXT NOT NULL,
    script_code VARCHAR(16) NOT NULL, -- arab, nastaliq, farsi, deva, latn
    bounding_box JSONB, -- {x_min, y_min, x_max, y_max}
    is_verse BOOLEAN NOT NULL DEFAULT FALSE,
    is_recipe BOOLEAN NOT NULL DEFAULT FALSE,
    is_margin_note BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_source_passages_page ON source_passages(page_id);
```

#### 7. `source_translations`
Authoritative scholarly translations with multi-linguistic alignment.
```sql
CREATE TABLE source_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    passage_id UUID NOT NULL REFERENCES source_passages(id) ON DELETE RESTRICT,
    target_language VARCHAR(10) NOT NULL, -- en, ur, hi, ar
    translated_text TEXT NOT NULL,
    translator_type VARCHAR(32) NOT NULL, -- HUMAN_EXPERT, AI_DRAFT_VERIFIED
    translator_id UUID,
    translation_notes TEXT,
    is_canonical BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_source_translations_passage ON source_translations(passage_id);
```

---

### 1.2 OCR Extraction Subsystem

#### 8. `ocr_documents`
Jobs representing bulk automated processing of digital editions.
```sql
CREATE TABLE ocr_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    edition_id UUID NOT NULL REFERENCES source_editions(id),
    engine_name VARCHAR(64) NOT NULL, -- Tesseract-Urdu, Kraken-Arabic, Google-Vision-OCR
    engine_version VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL, -- QUEUED, PROCESSING, COMPLETED, FAILED
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    overall_confidence NUMERIC(4,3),
    raw_output_uri TEXT
);
```

#### 9. `ocr_segments`
Word-level and line-level extracted tokens with spatial anchors.
```sql
CREATE TABLE ocr_segments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ocr_document_id UUID NOT NULL REFERENCES ocr_documents(id) ON DELETE CASCADE,
    page_id UUID NOT NULL REFERENCES source_pages(id),
    line_number INTEGER NOT NULL,
    segment_text TEXT NOT NULL,
    confidence NUMERIC(4,3) NOT NULL,
    bounding_polygon JSONB NOT NULL,
    needs_review BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE INDEX idx_ocr_segments_page ON ocr_segments(page_id);
CREATE INDEX idx_ocr_segments_needs_review ON ocr_segments(needs_review) WHERE needs_review = TRUE;
```

#### 10. `ocr_corrections`
Scholarly human-in-the-loop review audit ledger.
```sql
CREATE TABLE ocr_corrections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    segment_id UUID NOT NULL REFERENCES ocr_segments(id),
    original_ocr_text TEXT NOT NULL,
    corrected_text TEXT NOT NULL,
    reviewer_user_id UUID NOT NULL,
    correction_notes TEXT,
    reviewed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_ocr_corrections_segment ON ocr_corrections(segment_id);
```

---

### 1.3 Structured Clinical Knowledge Subsystem

#### 11. `zkb_mufradat` (Single Unani Drugs / Materia Medica)
```sql
CREATE TABLE zkb_mufradat (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    canonical_name_latin VARCHAR(255) NOT NULL, -- Botanical / Zoological / Mineral
    canonical_name_urdu VARCHAR(255) NOT NULL,
    canonical_name_arabic VARCHAR(255) NOT NULL,
    canonical_name_english VARCHAR(255),
    upi_code VARCHAR(64) UNIQUE, -- Unani Pharmacopoeia of India Monograph ID
    origin_category VARCHAR(32) NOT NULL, -- VEGETABLE (Nabati), ANIMAL (Haiwani), MINERAL (Madani)
    plant_part_used VARCHAR(128),
    mizaj_primary_quality VARCHAR(32) NOT NULL, -- HOT_AND_DRY, COLD_AND_MOIST, etc.
    mizaj_degree INTEGER NOT NULL CHECK (mizaj_degree BETWEEN 1 AND 4),
    mizaj_secondary_quality VARCHAR(32),
    mizaj_secondary_degree INTEGER CHECK (mizaj_secondary_degree BETWEEN 1 AND 4),
    is_schedule_e1_poison BOOLEAN NOT NULL DEFAULT FALSE,
    mudabbar_required BOOLEAN NOT NULL DEFAULT FALSE,
    mudabbar_protocol_summary TEXT,
    historical_single_dose_min_grams NUMERIC(6,3),
    historical_single_dose_max_grams NUMERIC(6,3),
    approved_single_dose_max_grams NUMERIC(6,3) NOT NULL,
    approved_daily_dose_max_grams NUMERIC(6,3) NOT NULL,
    therapeutic_actions TEXT[] NOT NULL, -- Array of classical actions: Muhallil, Muqawwi, etc.
    badal_substitutes TEXT[],
    musleh_correctives TEXT[],
    current_lifecycle_state VARCHAR(32) NOT NULL DEFAULT 'ORIGINAL_SOURCE',
    safe_for_ai BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_zkb_mufradat_latin ON zkb_mufradat(canonical_name_latin);
CREATE INDEX idx_zkb_mufradat_upi ON zkb_mufradat(upi_code);
CREATE INDEX idx_zkb_mufradat_e1 ON zkb_mufradat(is_schedule_e1_poison);
```

#### 12. `zkb_mufradat_synonyms`
Multilingual synonyms, regional vernaculars, and botanical basionyms.
```sql
CREATE TABLE zkb_mufradat_synonyms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mufradat_id UUID NOT NULL REFERENCES zkb_mufradat(id) ON DELETE CASCADE,
    synonym_name VARCHAR(255) NOT NULL,
    language_or_dialect VARCHAR(32) NOT NULL, -- Persian, Sanskrit, Tamil, Bengali, Turkish
    is_standard_commercial_name BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE INDEX idx_zkb_synonyms_lookup ON zkb_mufradat_synonyms(synonym_name);
```

#### 13. `zkb_murakkabat` (Compound Formulations)
```sql
CREATE TABLE zkb_murakkabat (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    canonical_name_urdu VARCHAR(255) NOT NULL,
    canonical_name_english VARCHAR(255) NOT NULL,
    dosage_form VARCHAR(64) NOT NULL, -- Majun, Khamira, Sharbat, Safuf, Habb, Qurs, Kushta, Itrifal
    nfum_code VARCHAR(64), -- National Formulary of Unani Medicine identifier
    primary_organ_axis VARCHAR(64) NOT NULL, -- Neuro-Cerebral, Hepato-Digestive, etc.
    overall_mizaj VARCHAR(64) NOT NULL,
    approved_single_dose_min_grams NUMERIC(6,3) NOT NULL,
    approved_single_dose_max_grams NUMERIC(6,3) NOT NULL,
    approved_daily_dose_max_grams NUMERIC(6,3) NOT NULL,
    anupan_vehicle VARCHAR(128) NOT NULL, -- Water, Milk, Arq-e-Gawzaban
    shelf_life_months INTEGER NOT NULL,
    manufacturing_protocol TEXT NOT NULL,
    current_lifecycle_state VARCHAR(32) NOT NULL DEFAULT 'ORIGINAL_SOURCE',
    safe_for_ai BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_zkb_murakkabat_name ON zkb_murakkabat(canonical_name_english);
CREATE INDEX idx_zkb_murakkabat_form ON zkb_murakkabat(dosage_form);
```

#### 14. `zkb_murakkabat_ingredients`
Component herbs, minerals, ratios, and detoxification verifications.
```sql
CREATE TABLE zkb_murakkabat_ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    murakkab_id UUID NOT NULL REFERENCES zkb_murakkabat(id) ON DELETE CASCADE,
    mufradat_id UUID NOT NULL REFERENCES zkb_mufradat(id) ON DELETE RESTRICT,
    quantity_ratio NUMERIC(7,4) NOT NULL, -- Fraction of total batch
    processing_stage VARCHAR(64) NOT NULL, -- Decoction, Fine Powder, Base Syrup, Trituration
    is_chief_active_ingredient BOOLEAN NOT NULL DEFAULT FALSE,
    requires_mudabbar_proof BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE INDEX idx_zkb_ingredients_formula ON zkb_murakkabat_ingredients(murakkab_id);
```

#### 15. `zkb_diseases`
Unani disease entities with ICD-11 & SNOMED-CT cross-references.
```sql
CREATE TABLE zkb_diseases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    unani_name_arabic VARCHAR(255) NOT NULL,
    unani_name_urdu VARCHAR(255) NOT NULL,
    transliterated_name VARCHAR(255) NOT NULL,
    icd11_code VARCHAR(32),
    snomed_ct_id VARCHAR(64),
    primary_organ_axis VARCHAR(64) NOT NULL,
    pathology_mizaj_derangement VARCHAR(64) NOT NULL, -- Su'-e-Mizaj Damawi, Safrawi, Balghami, Sawdawi
    predominant_maddah VARCHAR(64), -- Matter involvement
    clinical_manifestations TEXT NOT NULL,
    treatment_principles TEXT NOT NULL -- Usul-e-Ilaj
);
CREATE INDEX idx_zkb_diseases_icd11 ON zkb_diseases(icd11_code);
CREATE INDEX idx_zkb_diseases_axis ON zkb_diseases(primary_organ_axis);
```

#### 16. `zkb_mizaj_rules`
Algorithmic rules for patient temperament assessment and corrective balancing.
```sql
CREATE TABLE zkb_mizaj_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phenotype_factor VARCHAR(64) NOT NULL, -- Complexion, Build, Touch, Pulse, Sleep, Appetite, Emotional
    observation_value VARCHAR(128) NOT NULL,
    damawi_weight NUMERIC(4,2) NOT NULL DEFAULT 0.0,
    safrawi_weight NUMERIC(4,2) NOT NULL DEFAULT 0.0,
    balghami_weight NUMERIC(4,2) NOT NULL DEFAULT 0.0,
    sawdawi_weight NUMERIC(4,2) NOT NULL DEFAULT 0.0,
    clinical_notes TEXT
);
```

#### 17. `zkb_organ_axis_rules`
Functional interconnectivity rules across the 12 Organ-Axes.
```sql
CREATE TABLE zkb_organ_axis_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_axis VARCHAR(64) NOT NULL,
    target_axis VARCHAR(64) NOT NULL,
    interaction_type VARCHAR(64) NOT NULL, -- Synergistic, Antagonistic, Modulatory, Reflected (Bil-Irak)
    pathological_transmission_pattern TEXT NOT NULL,
    treatment_coordination_guideline TEXT NOT NULL
);
CREATE INDEX idx_zkb_axis_rules ON zkb_organ_axis_rules(source_axis, target_axis);
```

---

### 1.4 Evidence, Safety & Clinical Risk Subsystem

#### 18. `zkb_evidence_records`
Structured empirical grounding, trials, and E0–E6 grading.
```sql
CREATE TABLE zkb_evidence_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_entity_type VARCHAR(32) NOT NULL, -- MUFRADAT, MURAKKABAT, TREATMENT_PLAN
    target_entity_id UUID NOT NULL,
    evidence_tier VARCHAR(8) NOT NULL CHECK (evidence_tier IN ('E0','E1','E2','E3','E4','E5','E6')),
    grade_certainty VARCHAR(16) NOT NULL CHECK (grade_certainty IN ('VERY_LOW','LOW','MODERATE','HIGH')),
    pub_med_id VARCHAR(32),
    doi VARCHAR(128),
    study_design VARCHAR(64) NOT NULL, -- RCT, InVitro, Animal, Cohort, CaseSeries, ClassicalAuthority
    sample_size INTEGER,
    outcome_summary TEXT NOT NULL,
    adverse_events_noted TEXT,
    passage_provenance_id UUID REFERENCES source_passages(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_zkb_evidence_target ON zkb_evidence_records(target_entity_type, target_entity_id);
```

#### 19. `zkb_safety_rules`
Deterministic checks executed by the Clinical Safety Firewall.
```sql
CREATE TABLE zkb_safety_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_code VARCHAR(64) UNIQUE NOT NULL,
    entity_type VARCHAR(32) NOT NULL, -- HERB, FORMULATION, CLASS
    entity_id UUID,
    contraindication_cohort VARCHAR(64) NOT NULL, -- PREGNANCY, LACTATION, PEDIATRIC_LT_12, GERIATRIC_GT_65, RENAL_IMPAIRMENT, HEPATIC_IMPAIRMENT
    severity_level VARCHAR(16) NOT NULL CHECK (severity_level IN ('WARNING','CRITICAL_BLOCK','ABSOLUTE_HAZARD')),
    clinical_rationale TEXT NOT NULL,
    regulatory_source VARCHAR(128) NOT NULL, -- Schedule E(1), EMA HMPC, UPI
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE INDEX idx_zkb_safety_entity ON zkb_safety_rules(entity_type, entity_id);
```

#### 20. `zkb_contraindications` & `zkb_drug_interactions`
Herb-drug and herb-condition conflict matrices.
```sql
CREATE TABLE zkb_drug_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mufradat_id UUID NOT NULL REFERENCES zkb_mufradat(id),
    modern_drug_class VARCHAR(128) NOT NULL, -- Anticoagulants, Antidiabetics, Cardiac Glycosides, Sedatives
    interaction_mechanism VARCHAR(255) NOT NULL,
    clinical_effect TEXT NOT NULL,
    risk_severity VARCHAR(16) NOT NULL CHECK (risk_severity IN ('MILD','MODERATE','SEVERE','FATAL')),
    recommended_action VARCHAR(64) NOT NULL -- AVOID, MONITOR_INR, ADJUST_TIMING, SEPARATE_BY_4_HOURS
);
CREATE INDEX idx_zkb_interactions_herb ON zkb_drug_interactions(mufradat_id);
```

---

### 1.5 Governance, Versioning & Audit Subsystem

#### 21. `zkb_knowledge_reviews` & `zkb_clinical_approvals`
```sql
CREATE TABLE zkb_knowledge_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type VARCHAR(32) NOT NULL,
    entity_id UUID NOT NULL,
    reviewer_user_id UUID NOT NULL,
    reviewer_role VARCHAR(64) NOT NULL, -- UNANI_SCHOLAR, CLINICAL_PHARMACOLOGIST, TOXICOLOGIST, CHIEF_MEDICAL_OFFICER
    decision VARCHAR(32) NOT NULL, -- APPROVED, REJECTED, REVISIONS_REQUESTED
    review_comments TEXT NOT NULL,
    digital_signature_hash VARCHAR(128) NOT NULL,
    reviewed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE zkb_clinical_approvals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type VARCHAR(32) NOT NULL,
    entity_id UUID NOT NULL,
    lifecycle_state VARCHAR(32) NOT NULL,
    quorum_met BOOLEAN NOT NULL DEFAULT FALSE,
    required_votes INTEGER NOT NULL DEFAULT 3,
    affirmed_votes INTEGER NOT NULL DEFAULT 0,
    quorum_seal_hash VARCHAR(128),
    effective_from TIMESTAMPTZ,
    approved_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_zkb_approvals_target ON zkb_clinical_approvals(entity_type, entity_id);
```

#### 22. `zkb_audit_logs`
Cryptographically chained, immutable transaction logs.
```sql
CREATE TABLE zkb_audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action_type VARCHAR(64) NOT NULL,
    actor_id UUID NOT NULL,
    actor_role VARCHAR(64) NOT NULL,
    resource_type VARCHAR(64) NOT NULL,
    resource_id UUID NOT NULL,
    state_before JSONB,
    state_after JSONB,
    client_ip VARCHAR(64) NOT NULL,
    prev_entry_hash VARCHAR(64) NOT NULL,
    entry_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_zkb_audit_resource ON zkb_audit_logs(resource_type, resource_id);
```

---

## 2. Graph Schema Specification (Neo4j Enterprise)

### 2.1 Graph Node Definitions
- `Herb`: `id`, `name_latin`, `name_urdu`, `upi_code`, `is_poison`
- `Compound`: `id`, `name_urdu`, `name_english`, `dosage_form`
- `Phytochemical`: `id`, `name`, `chemical_formula`, `pubchem_cid`
- `OrganAxis`: `id`, `axis_code`, `axis_name`
- `Mizaj`: `id`, `primary_quality`, `degree`
- `Disease`: `id`, `icd11_code`, `unani_name`
- `ModernDrug`: `id`, `drug_name`, `pharmacological_class`

### 2.2 Graph Relationships & Constraints
```cypher
// Graph Constraints
CREATE CONSTRAINT uq_herb_upi IF NOT EXISTS FOR (h:Herb) REQUIRE h.upi_code IS UNIQUE;
CREATE CONSTRAINT uq_compound_id IF NOT EXISTS FOR (c:Compound) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT uq_disease_icd IF NOT EXISTS FOR (d:Disease) REQUIRE d.icd11_code IS UNIQUE;

// Relationship Schemas
(:Herb)-[:HAS_TEMPERAMENT {degree: 2}]->(:Mizaj)
(:Herb)-[:TARGETS_AXIS {action_type: 'Muqawwi', confidence: 0.98}]->(:OrganAxis)
(:Herb)-[:CONTAINS_ACTIVE_PRINCIPLE]->(:Phytochemical)
(:Herb)-[:REQUIRES_DETOXIFICATION]->(:MudabbarProtocol)
(:Compound)-[:COMPOSED_OF {ratio_percentage: 12.5}]->(:Herb)
(:Compound)-[:INDICATED_FOR {evidence_level: 'E2'}]->(:Disease)
(:Herb)-[:INTERACTS_WITH {severity: 'CRITICAL', action: 'BLOCK'}]->(:ModernDrug)
```

---
*Signed and Certified by:*  
**Principal Healthcare Database Architect & Clinical Governance Specialist**
