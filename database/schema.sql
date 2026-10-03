-- ZAYVORA Health OS — Persistent Relational Database Schema
-- Compatible with SQLite and PostgreSQL

CREATE TABLE IF NOT EXISTS facilities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    facility_type TEXT NOT NULL, -- HOSPITAL, CLINIC, RESEARCH_INSTITUTE, DISPENSARY
    address TEXT,
    city TEXT,
    state TEXT,
    contact_phone TEXT,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    role TEXT NOT NULL DEFAULT "PATIENT",
    mrn TEXT UNIQUE,
    facility_id TEXT DEFAULT "FAC-HQ-01",
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,
    facility_id TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    revoked INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS patients (
    id TEXT PRIMARY KEY,
    mrn TEXT UNIQUE NOT NULL,
    user_id TEXT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth TEXT,
    gender TEXT,
    contact_phone TEXT,
    contact_email TEXT,
    blood_group TEXT DEFAULT "Unknown",
    mizaj_dominant TEXT DEFAULT "Motadil (Balanced)",
    allergies_json TEXT DEFAULT "[]",
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS appointments (
    id TEXT PRIMARY KEY,
    token_number TEXT NOT NULL,
    mrn TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    doctor_reg TEXT,
    department TEXT DEFAULT "Integrative Unani OPD",
    opd_room TEXT DEFAULT "Room 3",
    appointment_date TEXT NOT NULL,
    appointment_time TEXT NOT NULL,
    acuity TEXT DEFAULT "STANDARD",
    chief_complaint TEXT,
    status TEXT DEFAULT "WAITING", -- WAITING, IN_CONSULTATION, COMPLETED, CANCELLED
    fee_amount REAL DEFAULT 800.0,
    payment_status TEXT DEFAULT "PAID", -- PENDING, PAID, REFUNDED
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS prescriptions (
    id TEXT PRIMARY KEY,
    order_number TEXT UNIQUE NOT NULL,
    mrn TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    doctor_reg TEXT NOT NULL,
    items_json TEXT NOT NULL,
    dietary_advice TEXT,
    regimenal_advice TEXT,
    signature_hash TEXT NOT NULL,
    status TEXT DEFAULT "PENDING_VERIFICATION", -- PENDING_VERIFICATION, VERIFIED_READY, DISPENSED
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS inventory (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    batch_number TEXT UNIQUE NOT NULL,
    expiry_date TEXT NOT NULL,
    stock_qty INTEGER NOT NULL DEFAULT 100,
    min_threshold INTEGER DEFAULT 20,
    category TEXT NOT NULL, -- CLINIC_UNANI, RETAIL_UNANI, AYUSH_PROPRIETARY, FSSAI_SUPPLEMENT
    unit_price REAL DEFAULT 150.0,
    is_schedule_e1 INTEGER DEFAULT 0,
    mudabbar_required INTEGER DEFAULT 0,
    mudabbar_cert TEXT,
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS audit_ledger (
    block_number INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    leaf_hash TEXT NOT NULL,
    event_type TEXT NOT NULL,
    signer TEXT NOT NULL,
    status TEXT DEFAULT "ANCHORED",
    facility_id TEXT DEFAULT "FAC-HQ-01",
    details_json TEXT
);

CREATE TABLE IF NOT EXISTS invoices (
    id TEXT PRIMARY KEY,
    invoice_number TEXT UNIQUE NOT NULL,
    mrn TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    amount REAL NOT NULL,
    department TEXT DEFAULT "Integrative Unani OPD",
    payment_method TEXT DEFAULT "UPI",
    status TEXT DEFAULT "PAID",
    prescription_id TEXT,
    items_json TEXT DEFAULT "[]",
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(facility_id) REFERENCES facilities(id),
    FOREIGN KEY(prescription_id) REFERENCES prescriptions(id)
);

CREATE TABLE IF NOT EXISTS encounters (
    id TEXT PRIMARY KEY,
    encounter_number TEXT UNIQUE NOT NULL,
    mrn TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    appointment_id TEXT,
    doctor_name TEXT NOT NULL,
    doctor_reg TEXT NOT NULL,
    facility_id TEXT DEFAULT "FAC-HQ-01",
    chief_complaint TEXT,
    examination_notes TEXT,
    vitals_json TEXT DEFAULT "{}",
    soap_json TEXT DEFAULT "{}",
    mizaj_json TEXT DEFAULT "{}",
    organ_axis_json TEXT DEFAULT "{}",
    afaal_cascade_json TEXT DEFAULT "{}",
    prescription_id TEXT,
    status TEXT DEFAULT "IN_PROGRESS", -- IN_PROGRESS, LOCKED_AND_SIGNED, CANCELLED
    signature_hash TEXT,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    signed_at DATETIME,
    FOREIGN KEY(facility_id) REFERENCES facilities(id),
    FOREIGN KEY(appointment_id) REFERENCES appointments(id),
    FOREIGN KEY(prescription_id) REFERENCES prescriptions(id)
);

CREATE TABLE IF NOT EXISTS ai_consultations (
    id TEXT PRIMARY KEY,
    consultation_id TEXT UNIQUE NOT NULL,
    mrn TEXT NOT NULL,
    patient_name TEXT,
    doctor_name TEXT,
    chief_complaint TEXT NOT NULL,
    organ_axis TEXT,
    mizaj TEXT,
    advisory_sections_json TEXT NOT NULL,
    citations_json TEXT NOT NULL,
    safety_verdict TEXT NOT NULL,
    provider_used TEXT NOT NULL,
    safe_to_lock INTEGER DEFAULT 0,
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS notifications (
    id TEXT PRIMARY KEY,
    notification_id TEXT UNIQUE NOT NULL,
    mrn TEXT,
    recipient TEXT NOT NULL,
    channel TEXT NOT NULL, -- SMS, WHATSAPP, EMAIL, IN_APP
    template_id TEXT NOT NULL,
    message_text TEXT NOT NULL,
    status TEXT DEFAULT "DELIVERED", -- PENDING, DELIVERED, FAILED
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(facility_id) REFERENCES facilities(id)
);

CREATE TABLE IF NOT EXISTS telemedicine_rooms (
    id TEXT PRIMARY KEY,
    room_id TEXT UNIQUE NOT NULL,
    encounter_id TEXT,
    appointment_id TEXT,
    mrn TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    session_token TEXT NOT NULL,
    status TEXT DEFAULT "ACTIVE", -- ACTIVE, CLOSED
    facility_id TEXT DEFAULT "FAC-HQ-01",
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    closed_at DATETIME,
    FOREIGN KEY(facility_id) REFERENCES facilities(id),
    FOREIGN KEY(appointment_id) REFERENCES appointments(id)
);

CREATE INDEX IF NOT EXISTS idx_patients_facility ON patients(facility_id);
CREATE INDEX IF NOT EXISTS idx_appointments_facility ON appointments(facility_id);
CREATE INDEX IF NOT EXISTS idx_prescriptions_facility ON prescriptions(facility_id);
CREATE INDEX IF NOT EXISTS idx_inventory_facility ON inventory(facility_id);
CREATE INDEX IF NOT EXISTS idx_inventory_name ON inventory(name);
CREATE INDEX IF NOT EXISTS idx_invoices_facility ON invoices(facility_id);
CREATE INDEX IF NOT EXISTS idx_invoices_prescription ON invoices(prescription_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token);
CREATE INDEX IF NOT EXISTS idx_encounters_mrn ON encounters(mrn);
CREATE INDEX IF NOT EXISTS idx_encounters_facility ON encounters(facility_id);
CREATE INDEX IF NOT EXISTS idx_encounters_apt ON encounters(appointment_id);
CREATE INDEX IF NOT EXISTS idx_ai_consultations_mrn ON ai_consultations(mrn);
CREATE INDEX IF NOT EXISTS idx_ai_consultations_facility ON ai_consultations(facility_id);
CREATE INDEX IF NOT EXISTS idx_notifications_mrn ON notifications(mrn);
CREATE INDEX IF NOT EXISTS idx_notifications_facility ON notifications(facility_id);
CREATE INDEX IF NOT EXISTS idx_telemedicine_mrn ON telemedicine_rooms(mrn);
CREATE INDEX IF NOT EXISTS idx_telemedicine_facility ON telemedicine_rooms(facility_id);

-- ============================================================================
-- ZKB SOURCE LIBRARY & PROVENANCE SUBSYSTEM (Phase 2)
-- ============================================================================

CREATE TABLE IF NOT EXISTS source_authors (
    id TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    arabic_name TEXT,
    persian_name TEXT,
    urdu_name TEXT,
    era_hijri TEXT,
    era_ce TEXT,
    biography_summary TEXT,
    is_classical BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_books (
    id TEXT PRIMARY KEY,
    primary_author_id TEXT REFERENCES source_authors(id),
    canonical_title TEXT NOT NULL,
    original_title TEXT NOT NULL,
    transliterated_title TEXT,
    language_code TEXT NOT NULL,
    discipline TEXT NOT NULL,
    historical_era TEXT,
    source_type TEXT NOT NULL DEFAULT 'CLASSICAL_TREATISE',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_editions (
    id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES source_books(id),
    editor_translator TEXT,
    publisher TEXT NOT NULL,
    publication_year INTEGER NOT NULL,
    publication_place TEXT,
    edition_number TEXT,
    volume_number TEXT,
    isbn_issn TEXT,
    total_pages INTEGER NOT NULL DEFAULT 0,
    call_number TEXT,
    digital_scan_url TEXT,
    sha256_checksum TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_rights (
    id TEXT PRIMARY KEY,
    edition_id TEXT NOT NULL REFERENCES source_editions(id),
    rights_status TEXT NOT NULL DEFAULT 'unknown',
    clinical_access TEXT NOT NULL DEFAULT 'research_only',
    license_type TEXT NOT NULL DEFAULT 'PUBLIC_DOMAIN',
    rights_holder TEXT,
    licensed_to_facility TEXT,
    valid_from DATE,
    valid_until DATE,
    commercial_use_permitted BOOLEAN NOT NULL DEFAULT 0,
    ai_training_permitted BOOLEAN NOT NULL DEFAULT 0,
    verified_by_legal_officer TEXT,
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_pages (
    id TEXT PRIMARY KEY,
    edition_id TEXT NOT NULL REFERENCES source_editions(id),
    page_number INTEGER NOT NULL,
    folio_recto_verso TEXT,
    image_storage_uri TEXT NOT NULL,
    image_mime_type TEXT NOT NULL DEFAULT 'image/tiff',
    width_px INTEGER NOT NULL DEFAULT 0,
    height_px INTEGER NOT NULL DEFAULT 0,
    dpi INTEGER NOT NULL DEFAULT 300,
    sha256_page_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(edition_id, page_number)
);

CREATE TABLE IF NOT EXISTS source_passages (
    id TEXT PRIMARY KEY,
    page_id TEXT NOT NULL REFERENCES source_pages(id),
    passage_order INTEGER NOT NULL,
    chapter TEXT,
    section TEXT,
    original_text TEXT NOT NULL,
    normalized_text TEXT NOT NULL,
    script_code TEXT NOT NULL DEFAULT 'arab',
    bounding_box TEXT, -- JSON string
    is_verse BOOLEAN NOT NULL DEFAULT 0,
    is_recipe BOOLEAN NOT NULL DEFAULT 0,
    is_margin_note BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_translations (
    id TEXT PRIMARY KEY,
    passage_id TEXT NOT NULL REFERENCES source_passages(id),
    target_language TEXT NOT NULL,
    translated_text TEXT NOT NULL,
    translator_type TEXT NOT NULL DEFAULT 'HUMAN_EXPERT',
    translator_name TEXT,
    translation_notes TEXT,
    is_canonical BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_source_authors_name ON source_authors(canonical_name);
CREATE INDEX IF NOT EXISTS idx_source_books_title ON source_books(canonical_title);
CREATE INDEX IF NOT EXISTS idx_source_editions_book ON source_editions(book_id);
CREATE INDEX IF NOT EXISTS idx_source_rights_edition ON source_rights(edition_id);
CREATE INDEX IF NOT EXISTS idx_source_pages_edition ON source_pages(edition_id);
CREATE INDEX IF NOT EXISTS idx_source_passages_page ON source_passages(page_id);
CREATE INDEX IF NOT EXISTS idx_source_translations_passage ON source_translations(passage_id);

-- ============================================================================
-- ZKB OCR EXTRACTION & HUMAN CORRECTION SUBSYSTEM (Phase 3)
-- ============================================================================

CREATE TABLE IF NOT EXISTS ocr_documents (
    id TEXT PRIMARY KEY,
    edition_id TEXT NOT NULL REFERENCES source_editions(id),
    engine_name TEXT NOT NULL,
    engine_version TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'QUEUED',
    target_scripts TEXT NOT NULL DEFAULT '[]', -- JSON string
    overall_confidence REAL,
    total_pages_processed INTEGER NOT NULL DEFAULT 0,
    needs_review_count INTEGER NOT NULL DEFAULT 0,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    raw_output_uri TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ocr_segments (
    id TEXT PRIMARY KEY,
    ocr_document_id TEXT NOT NULL REFERENCES ocr_documents(id),
    page_id TEXT NOT NULL REFERENCES source_pages(id),
    line_number INTEGER NOT NULL,
    detected_script TEXT NOT NULL DEFAULT 'arab',
    detected_language TEXT NOT NULL DEFAULT 'ar',
    segment_text TEXT NOT NULL,
    confidence REAL NOT NULL,
    bounding_polygon TEXT, -- JSON string
    needs_review BOOLEAN NOT NULL DEFAULT 0,
    is_corrected BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ocr_corrections (
    id TEXT PRIMARY KEY,
    segment_id TEXT NOT NULL REFERENCES ocr_segments(id),
    original_ocr_text TEXT NOT NULL,
    corrected_text TEXT NOT NULL,
    reviewer_user_id TEXT NOT NULL,
    reviewer_name TEXT,
    correction_notes TEXT,
    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS knowledge_extractions (
    id TEXT PRIMARY KEY,
    passage_id TEXT NOT NULL REFERENCES source_passages(id),
    extracted_entities TEXT NOT NULL DEFAULT '{}', -- JSON string
    extraction_confidence REAL NOT NULL,
    extraction_method TEXT NOT NULL DEFAULT 'PATTERN_DICTIONARY_MATCH',
    review_status TEXT NOT NULL DEFAULT 'NEEDS_EXPERT_REVIEW',
    reviewer_user_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_ocr_documents_edition ON ocr_documents(edition_id);
CREATE INDEX IF NOT EXISTS idx_ocr_segments_doc ON ocr_segments(ocr_document_id);
CREATE INDEX IF NOT EXISTS idx_ocr_segments_page ON ocr_segments(page_id);
CREATE INDEX IF NOT EXISTS idx_ocr_segments_needs_review ON ocr_segments(needs_review);
CREATE INDEX IF NOT EXISTS idx_ocr_corrections_segment ON ocr_corrections(segment_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_extractions_passage ON knowledge_extractions(passage_id);

-- ============================================================
-- PHASE 4: Structured Clinical Knowledge Tables
-- ZKB Mufradat, Murakkabat, Diseases, Safety, Drug Interactions
-- ============================================================

CREATE TABLE IF NOT EXISTS zkb_mufradat (
    id TEXT PRIMARY KEY,
    canonical_name_latin TEXT NOT NULL,
    canonical_name_urdu TEXT NOT NULL,
    canonical_name_arabic TEXT,
    canonical_name_english TEXT,
    botanical_name TEXT,
    upi_code TEXT UNIQUE,
    origin_category TEXT NOT NULL DEFAULT 'VEGETABLE',
    plant_part_used TEXT,
    mizaj_primary_quality TEXT,
    mizaj_degree INTEGER NOT NULL DEFAULT 1,
    is_schedule_e1_poison BOOLEAN NOT NULL DEFAULT 0,
    mandatory_mudabbar BOOLEAN NOT NULL DEFAULT 0,
    mudabbar_protocol TEXT,
    historical_dose TEXT,
    approved_single_dose_max_grams REAL NOT NULL DEFAULT 0.0,
    approved_daily_dose_max_grams REAL NOT NULL DEFAULT 0.0,
    therapeutic_actions TEXT NOT NULL DEFAULT '[]', -- JSON array
    badal_substitutes TEXT NOT NULL DEFAULT '[]',   -- JSON array
    musleh_correctives TEXT NOT NULL DEFAULT '[]',  -- JSON array
    pregnancy_status TEXT NOT NULL DEFAULT 'SAFE',
    lactation_status TEXT NOT NULL DEFAULT 'SAFE',
    pediatric_status TEXT NOT NULL DEFAULT 'SAFE',
    geriatric_status TEXT NOT NULL DEFAULT 'SAFE',
    evidence_level TEXT NOT NULL DEFAULT 'E3',
    current_lifecycle_state TEXT NOT NULL DEFAULT 'UNDER_REVIEW',
    safe_for_ai BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS zkb_murakkabat (
    id TEXT PRIMARY KEY,
    canonical_name_urdu TEXT NOT NULL,
    canonical_name_english TEXT NOT NULL,
    dosage_form TEXT NOT NULL,
    nfum_code TEXT UNIQUE,
    primary_organ_axis TEXT,
    therapeutic_objective TEXT,
    overall_mizaj TEXT,
    approved_single_dose_min_grams REAL NOT NULL DEFAULT 0.0,
    approved_single_dose_max_grams REAL NOT NULL DEFAULT 0.0,
    approved_daily_dose_max_grams REAL NOT NULL DEFAULT 0.0,
    anupan_vehicle TEXT,
    shelf_life_months INTEGER NOT NULL DEFAULT 24,
    manufacturing_protocol TEXT,
    evidence_level TEXT NOT NULL DEFAULT 'E3',
    current_lifecycle_state TEXT NOT NULL DEFAULT 'UNDER_REVIEW',
    safe_for_ai BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS zkb_murakkabat_ingredients (
    id TEXT PRIMARY KEY,
    murakkab_id TEXT NOT NULL REFERENCES zkb_murakkabat(id) ON DELETE CASCADE,
    mufradat_id TEXT NOT NULL REFERENCES zkb_mufradat(id),
    ratio REAL NOT NULL DEFAULT 0.0,
    is_chief BOOLEAN NOT NULL DEFAULT 0,
    requires_mudabbar BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS zkb_diseases (
    id TEXT PRIMARY KEY,
    unani_name_arabic TEXT,
    unani_name_urdu TEXT NOT NULL,
    transliterated_name TEXT NOT NULL,
    icd11_code TEXT,
    snomed_ct_id TEXT,
    biomedical_mapping_type TEXT NOT NULL DEFAULT 'phenotypic_cluster',
    primary_organ_axis TEXT,
    pathology_mizaj_derangement TEXT,
    clinical_manifestations TEXT,
    treatment_principles TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS zkb_safety_rules (
    id TEXT PRIMARY KEY,
    rule_code TEXT NOT NULL UNIQUE,
    rule_name TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'WARNING',
    description TEXT NOT NULL,
    applies_to_e1_only BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS zkb_drug_interactions (
    id TEXT PRIMARY KEY,
    mufradat_id TEXT NOT NULL REFERENCES zkb_mufradat(id),
    modern_drug_class TEXT NOT NULL,
    interaction_mechanism TEXT NOT NULL,
    clinical_effect TEXT NOT NULL,
    risk_severity TEXT NOT NULL DEFAULT 'MODERATE',
    recommended_action TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_provenance (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS master_organ_axes (
    id TEXT PRIMARY KEY,
    arabic_name TEXT,
    body_system TEXT,
    governing_power TEXT,
    key_diseases TEXT,
    primary_products TEXT,
    regulatory_track TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS master_protocols (
    id TEXT PRIMARY KEY,
    name TEXT,
    category TEXT,
    organ_axis TEXT,
    icd11_code TEXT,
    primary_humor TEXT,
    phase1 TEXT,
    phase2 TEXT,
    phase3 TEXT,
    product_stack TEXT,
    lab_monitoring TEXT,
    clinical_warnings TEXT
);

CREATE TABLE IF NOT EXISTS master_protocol_kits (
    kit_id TEXT PRIMARY KEY,
    name TEXT,
    protocol_id TEXT,
    category TEXT,
    products TEXT,
    monthly_price REAL
);

CREATE TABLE IF NOT EXISTS master_products (
    sku TEXT PRIMARY KEY,
    name TEXT,
    category TEXT,
    section TEXT,
    organ_axis TEXT,
    is_prescription_required INTEGER DEFAULT 0,
    dosage_form TEXT,
    daily_dose TEXT,
    composition TEXT,
    contraindications TEXT,
    monitoring TEXT,
    citations TEXT,
    mrp REAL,
    b2b_price REAL,
    regulatory_track TEXT,
    unani_name TEXT,
    is_hero_launch INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS master_parhez (
    code TEXT PRIMARY KEY,
    name TEXT,
    classical_principle TEXT,
    target_axes TEXT,
    duration_days INTEGER,
    rules TEXT
);

CREATE INDEX IF NOT EXISTS idx_zkb_mufradat_upi ON zkb_mufradat(upi_code);
CREATE INDEX IF NOT EXISTS idx_zkb_mufradat_e1 ON zkb_mufradat(is_schedule_e1_poison);
CREATE INDEX IF NOT EXISTS idx_zkb_murakkabat_nfum ON zkb_murakkabat(nfum_code);
CREATE INDEX IF NOT EXISTS idx_zkb_murakkabat_ingredients_mur ON zkb_murakkabat_ingredients(murakkab_id);
CREATE INDEX IF NOT EXISTS idx_zkb_murakkabat_ingredients_muf ON zkb_murakkabat_ingredients(mufradat_id);
CREATE INDEX IF NOT EXISTS idx_zkb_diseases_icd ON zkb_diseases(icd11_code);
CREATE INDEX IF NOT EXISTS idx_zkb_drug_interactions_muf ON zkb_drug_interactions(mufradat_id);
CREATE INDEX IF NOT EXISTS idx_zkb_drug_interactions_severity ON zkb_drug_interactions(risk_severity);

-- Password Reset OTPs (Short TTL, Hashed Storage, Rate-Limited)
CREATE TABLE IF NOT EXISTS password_reset_otps (
    id TEXT PRIMARY KEY,
    identifier TEXT NOT NULL,
    otp_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    expires_at DATETIME NOT NULL,
    attempts INTEGER DEFAULT 0,
    used INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_otp_identifier ON password_reset_otps(identifier);

-- Clinical Governance Board Tables (Persistent Relational Storage)
CREATE TABLE IF NOT EXISTS governance_proposals (
    proposal_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    proposed_diff_json TEXT NOT NULL,
    status TEXT NOT NULL,
    created_by TEXT NOT NULL,
    created_at_utc TEXT NOT NULL,
    attestations_json TEXT DEFAULT "[]"
);

CREATE TABLE IF NOT EXISTS governance_change_orders (
    change_order_id TEXT PRIMARY KEY,
    proposal_id TEXT NOT NULL,
    title TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    applied_diff_json TEXT NOT NULL,
    published_at_utc TEXT NOT NULL,
    immutable_sha256_seal TEXT NOT NULL,
    attestations_json TEXT NOT NULL,
    FOREIGN KEY(proposal_id) REFERENCES governance_proposals(proposal_id)
);

-- 12-Gate Evidence Pipeline Tracker Table
CREATE TABLE IF NOT EXISTS mufradat_twelve_gates (
    id TEXT PRIMARY KEY,
    zmf_id TEXT NOT NULL,
    gate_number INTEGER NOT NULL,
    gate_name TEXT NOT NULL,
    signed_by TEXT NOT NULL,
    signed_at TEXT NOT NULL,
    notes TEXT,
    evidence_hash TEXT,
    UNIQUE(zmf_id, gate_number)
);
CREATE INDEX IF NOT EXISTS idx_twelve_gates_zmf ON mufradat_twelve_gates(zmf_id);

-- ============================================================================
-- AUTHORITATIVE CLINICAL PERSISTENCE & HARDENING TABLES (Layers 0, 2, 3, 14, 25, 38)
-- ============================================================================

-- Clinician Credential Registry (Mandatory for clinical prescription approval)
CREATE TABLE IF NOT EXISTS clinician_registry (
    clinician_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    registration_number TEXT NOT NULL UNIQUE,
    registration_body TEXT NOT NULL,          -- e.g. NCISM, State Board of Unani Medicine, Delhi Bharatiya Chikitsa Parishad
    registration_state TEXT NOT NULL,
    registration_type TEXT NOT NULL,          -- PERMANENT, PROVISIONAL, RENEWAL
    specialty TEXT NOT NULL,                  -- UNANI_MEDICINE, ILMUL_ADVIA, MOALAJAT, INTEGRATIVE_MEDICINE
    qualification TEXT NOT NULL,              -- BUMS, MD (Unani), MBBS, MS
    facility_scope TEXT NOT NULL,             -- ALL, or comma-separated facility IDs
    clinical_scope TEXT NOT NULL,             -- GENERAL_PRACTICE, CONSULTANT_TABEEB, PHARMACOLOGY_CHIEF
    issued_at DATE NOT NULL,
    expires_at DATE NOT NULL,
    verification_status TEXT NOT NULL,        -- VERIFIED_ACTIVE, SUSPENDED, EXPIRED, PENDING_REVIEW
    verified_by TEXT NOT NULL,
    verified_at DATETIME NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS idx_clinician_reg_user ON clinician_registry(user_id);
CREATE INDEX IF NOT EXISTS idx_clinician_reg_num ON clinician_registry(registration_number);
CREATE INDEX IF NOT EXISTS idx_clinician_reg_status ON clinician_registry(verification_status);

-- Comprehensive Clinical Assessments (SOAP & Unani Findings)
CREATE TABLE IF NOT EXISTS clinical_assessments (
    assessment_id TEXT PRIMARY KEY,
    encounter_id TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    clinician_id TEXT NOT NULL,
    subjective_narrative TEXT,
    objective_findings_json TEXT,             -- Vitals, Nabz, Lisan, physical examination
    assessment_summary TEXT NOT NULL,
    plan_summary TEXT NOT NULL,
    inputs_reproducibility_json TEXT NOT NULL, -- Raw patient data used to derive scores
    confidence_score REAL NOT NULL DEFAULT 1.0,
    immutable_sha256_hash TEXT NOT NULL,
    signed_at DATETIME NOT NULL,
    FOREIGN KEY(encounter_id) REFERENCES encounters(id),
    FOREIGN KEY(patient_id) REFERENCES patients(id),
    FOREIGN KEY(clinician_id) REFERENCES clinician_registry(clinician_id)
);
CREATE INDEX IF NOT EXISTS idx_clinical_assessments_enc ON clinical_assessments(encounter_id);
CREATE INDEX IF NOT EXISTS idx_clinical_assessments_pat ON clinical_assessments(patient_id);

-- Longitudinal Mizaj Assessments (10-Ajnas Vector & Questionnaire Grounding)
CREATE TABLE IF NOT EXISTS mizaj_assessments (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    encounter_id TEXT,
    ten_ajnas_vectors_json TEXT NOT NULL,      -- Vector scores across Dam, Balgham, Safra, Sauda
    questionnaire_responses_json TEXT,
    dominant_temperament TEXT NOT NULL,       -- DAM, BALGHAM, SAFRA, SAUDA, COMPOUND, or INSUFFICIENT_DATA
    dyscrasia_degree INTEGER DEFAULT 1,       -- 1 to 4
    contradiction_flags_json TEXT DEFAULT "[]",
    clinician_confirmed BOOLEAN DEFAULT 0,
    status TEXT NOT NULL,                     -- COMPLETED, INSUFFICIENT_DATA, CLINICIAN_OVERRIDDEN
    assessed_by TEXT NOT NULL,
    assessed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(patient_id) REFERENCES patients(id)
);
CREATE INDEX IF NOT EXISTS idx_mizaj_assessments_pat ON mizaj_assessments(patient_id);

-- 12 Organ-Axis Diagnostic Scores & Explainability Traces
CREATE TABLE IF NOT EXISTS organ_axis_assessments (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    encounter_id TEXT,
    axis_id TEXT NOT NULL,                    -- e.g. mafasil, jigar_khasiya, dimagh_kuli, etc.
    score REAL NOT NULL,                      -- 0.0 to 100.0
    severity TEXT NOT NULL,                   -- NORMAL, MILD_STAGNATION, MODERATE_IMPAIRMENT, SEVERE_COLLAPSE
    confidence REAL NOT NULL,
    reproducible_inputs_json TEXT NOT NULL,   -- Lab values, symptoms, vitals that generated this score
    explainability_trace TEXT NOT NULL,       -- Clinical rationale explaining why this patient received this score
    assessed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(patient_id) REFERENCES patients(id)
);
CREATE INDEX IF NOT EXISTS idx_organ_axis_pat ON organ_axis_assessments(patient_id);
CREATE INDEX IF NOT EXISTS idx_organ_axis_id ON organ_axis_assessments(axis_id);

-- Canonical Evidence Sources & Study Metadata
CREATE TABLE IF NOT EXISTS evidence_sources (
    source_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    edition TEXT,
    publication_year INTEGER,
    isbn_or_doi TEXT,
    source_type TEXT NOT NULL,                -- PHARMACOPOEIA, CLASSICAL_CANON, PEER_REVIEWED_RCT, META_ANALYSIS, OBSERVATIONAL
    jurisdiction TEXT DEFAULT "INDIA",        -- INDIA, WHO, EMA, US_FDA
    digital_sha256_checksum TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Granular Evidence Claims (Grounding Engine)
CREATE TABLE IF NOT EXISTS evidence_claims (
    claim_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    canonical_substance_id TEXT,
    page_number INTEGER,
    passage_text TEXT NOT NULL,
    evidence_tier TEXT NOT NULL,              -- E0, E1, E2, E3, E4, E5, E6
    study_design TEXT,
    population_size INTEGER,
    confidence_score REAL NOT NULL,
    verified_by TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(source_id) REFERENCES evidence_sources(source_id)
);
CREATE INDEX IF NOT EXISTS idx_evidence_claims_substance ON evidence_claims(canonical_substance_id);
CREATE INDEX IF NOT EXISTS idx_evidence_claims_tier ON evidence_claims(evidence_tier);

-- Immutable Versioned Prescriptions (Nuskha History)
CREATE TABLE IF NOT EXISTS nuskha_versions (
    version_id TEXT PRIMARY KEY,
    prescription_id TEXT NOT NULL,
    version_number INTEGER NOT NULL,
    patient_id TEXT NOT NULL,
    clinician_id TEXT NOT NULL,
    formulation_type TEXT NOT NULL,           -- CLASS_A_CLASSICAL, CLASS_B_ADAPTATION, CLASS_C_RESEARCH, CUSTOM_COMPOUND
    items_json TEXT NOT NULL,
    safety_verdict TEXT NOT NULL,             -- PASS, CAUTION, BLOCK, UNKNOWN
    safety_details_json TEXT NOT NULL,
    clinician_acknowledgement_rationale TEXT, -- Required if safety_verdict == CAUTION
    immutable_digital_signature TEXT NOT NULL,
    signed_at DATETIME NOT NULL,
    FOREIGN KEY(patient_id) REFERENCES patients(id),
    FOREIGN KEY(clinician_id) REFERENCES clinician_registry(clinician_id)
);
CREATE INDEX IF NOT EXISTS idx_nuskha_versions_rx ON nuskha_versions(prescription_id);

-- Standardized Patient-Reported Outcome Measures (PROMs)
CREATE TABLE IF NOT EXISTS patient_prom_responses (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    encounter_id TEXT,
    instrument_id TEXT NOT NULL,              -- VAS_PAIN, KOOS_PS, PHQ_9, Z_VITALITY_INDEX
    instrument_version TEXT NOT NULL,
    language TEXT NOT NULL DEFAULT "en",
    raw_responses_json TEXT NOT NULL,
    calculated_score REAL NOT NULL,
    baseline_score REAL,
    mcid_delta REAL,                          -- Minimal Clinically Important Difference delta
    collection_mode TEXT NOT NULL,            -- PATIENT_PORTAL, CLINIC_TABLET, VOICE_SCRIBE
    collected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(patient_id) REFERENCES patients(id)
);
CREATE INDEX IF NOT EXISTS idx_prom_pat ON patient_prom_responses(patient_id);
CREATE INDEX IF NOT EXISTS idx_prom_instrument ON patient_prom_responses(instrument_id);

-- Patient Treatment Adherence Tracking
CREATE TABLE IF NOT EXISTS patient_adherence_records (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    prescription_id TEXT NOT NULL,
    day_offset INTEGER NOT NULL,
    dose_scheduled_at DATETIME NOT NULL,
    dose_taken_at DATETIME,
    status TEXT NOT NULL,                     -- TAKEN_ON_TIME, TAKEN_LATE, MISSED, ADVERSE_STOP
    patient_notes TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(id),
    FOREIGN KEY(prescription_id) REFERENCES prescriptions(id)
);
CREATE INDEX IF NOT EXISTS idx_adherence_pat ON patient_adherence_records(patient_id);

-- Closed-Loop Learning Healthcare System (Research Staging Partition)
CREATE TABLE IF NOT EXISTS learning_cohorts (
    cohort_id TEXT PRIMARY KEY,
    study_protocol_id TEXT NOT NULL,
    phenotype_cluster_id TEXT NOT NULL,
    target_condition TEXT NOT NULL,
    inclusion_criteria_json TEXT NOT NULL,
    anonymized_subjects_count INTEGER DEFAULT 0,
    status TEXT NOT NULL,                     -- RECRUITING, ANALYZING, COMPLETED, SUSPENDED
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS learning_proposals (
    proposal_id TEXT PRIMARY KEY,
    cohort_id TEXT NOT NULL,
    proposed_clinical_rule TEXT NOT NULL,
    statistical_evidence_json TEXT NOT NULL,   -- Cohen's d, p-value, sample size
    governance_review_status TEXT NOT NULL,    -- PENDING_BOARD, RATIFIED, REJECTED
    board_resolution_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(cohort_id) REFERENCES learning_cohorts(cohort_id)
);

-- Pharmacovigilance Real-Time Signals (ICH E2B / WHO-UMC)
CREATE TABLE IF NOT EXISTS pv_signals (
    signal_id TEXT PRIMARY KEY,
    substance_name TEXT NOT NULL,
    adverse_reaction_term TEXT NOT NULL,      -- MedDRA Preferred Term (PT)
    reports_count INTEGER NOT NULL DEFAULT 1,
    prr_score REAL,                           -- Proportional Reporting Ratio
    who_umc_causality TEXT NOT NULL,          -- CERTAIN, PROBABLE, POSSIBLE, UNLIKELY
    regulatory_alert_status TEXT NOT NULL,    -- MONITORING, ACTION_REQUIRED, CLOSED
    quarantine_recommended BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_pv_substance ON pv_signals(substance_name);



-- Patient Consents (DPDP Act 2023 & Master Blueprint §11)
CREATE TABLE IF NOT EXISTS patient_consents (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    purpose TEXT NOT NULL,
    status TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    notes TEXT
);
CREATE INDEX IF NOT EXISTS idx_patient_consents_pid ON patient_consents(patient_id);
