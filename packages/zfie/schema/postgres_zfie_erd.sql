-- =============================================================================
-- ZAYVORA Formulation Intelligence Engine™ (ZFIE)
-- Full Production PostgreSQL ERD & DDL Schema
-- System: ZAYVORA Health OS™
-- Doctrine: KNOWLEDGE -> INFERENCE -> EVIDENCE -> SAFETY -> VALIDATION -> CLINICIAN -> ACTION -> OUTCOME
-- =============================================================================

-- Enable UUID extension if not present
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- 1. ENUMS (Section 4)
-- =============================================================================

DO $$ BEGIN
    CREATE TYPE zfie_status AS ENUM (
      'DRAFT',
      'PENDING_REVIEW',
      'APPROVED',
      'REJECTED',
      'BLOCKED',
      'ACTIVE',
      'SUPERSEDED',
      'EXPIRED',
      'ARCHIVED'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE evidence_status AS ENUM (
      'ESTABLISHED',
      'SUPPORTED',
      'COMPUTATIONALLY_PREDICTED',
      'TRADITIONAL_CLAIM',
      'CONFLICTING',
      'UNKNOWN'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE evidence_level AS ENUM (
      'E0',
      'E1',
      'E2',
      'E3',
      'E4',
      'E5',
      'E6'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE safety_state AS ENUM (
      'PASS',
      'CAUTION',
      'BLOCK',
      'UNKNOWN'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE claim_origin AS ENUM (
      'OBSERVED',
      'CURATED',
      'CALCULATED',
      'PREDICTED',
      'INFERRED',
      'UNKNOWN'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE analysis_mode AS ENUM (
      'RESEARCH',
      'SHADOW',
      'CLINICAL_CDS'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE validation_state AS ENUM (
      'NOT_VALIDATED',
      'IN_PROGRESS',
      'PARTIALLY_SUPPORTED',
      'EXPERIMENTALLY_SUPPORTED',
      'REPLICATED',
      'CONTRADICTED',
      'RETIRED'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- =============================================================================
-- 2. CORE MASTER TABLES (Sections 5 - 10)
-- =============================================================================

-- Table 1: Mufradat (Section 5)
CREATE TABLE IF NOT EXISTS zfie_mufradat (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    canonical_name TEXT NOT NULL,
    unani_name TEXT,
    latin_name TEXT,
    common_names JSONB NOT NULL DEFAULT '[]',
    synonyms JSONB NOT NULL DEFAULT '[]',
    plant_part TEXT,
    traditional_description TEXT,
    classical_reference_ids UUID[] DEFAULT '{}',
    status zfie_status NOT NULL DEFAULT 'DRAFT',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 2: Formulations (Section 6)
CREATE TABLE IF NOT EXISTS zfie_formulations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    canonical_name TEXT NOT NULL,
    formulation_code TEXT UNIQUE NOT NULL,
    formulation_type TEXT,
    traditional_system TEXT,
    classical_source TEXT,
    therapeutic_objective TEXT,
    current_version_id UUID NULL,
    status zfie_status NOT NULL DEFAULT 'DRAFT',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by UUID NULL
);

-- Table 3: Formulation Versions (Section 7)
CREATE TABLE IF NOT EXISTS zfie_formulation_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    formulation_id UUID NOT NULL
        REFERENCES zfie_formulations(id) ON DELETE RESTRICT,

    version_label TEXT NOT NULL,
    version_number INTEGER NOT NULL,

    preparation_method TEXT,
    dosage_definition JSONB,
    route TEXT,

    change_reason TEXT,
    supersedes_version_id UUID NULL
        REFERENCES zfie_formulation_versions(id) ON DELETE SET NULL,

    effective_from TIMESTAMPTZ,
    effective_to TIMESTAMPTZ,

    review_status zfie_status NOT NULL DEFAULT 'DRAFT',

    knowledge_snapshot_id UUID NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE(formulation_id, version_number)
);

-- Circular FK link back to current_version_id
DO $$ BEGIN
    ALTER TABLE zfie_formulations
    ADD CONSTRAINT fk_formulation_current_version
    FOREIGN KEY (current_version_id)
    REFERENCES zfie_formulation_versions(id) ON DELETE SET NULL;
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Table 4: Formulation Ingredients (Section 8)
CREATE TABLE IF NOT EXISTS zfie_formulation_ingredients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    formulation_version_id UUID NOT NULL
        REFERENCES zfie_formulation_versions(id) ON DELETE CASCADE,

    mufrad_id UUID NOT NULL
        REFERENCES zfie_mufradat(id) ON DELETE RESTRICT,

    quantity NUMERIC,
    unit TEXT,
    ratio NUMERIC,

    plant_part TEXT,
    preparation_state TEXT,
    sequence INTEGER,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 5: Batch Model (Section 9) - Formula != Batch Invariant
CREATE TABLE IF NOT EXISTS zfie_batches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    formulation_version_id UUID NOT NULL
        REFERENCES zfie_formulation_versions(id) ON DELETE RESTRICT,

    batch_number TEXT NOT NULL,
    manufacturer TEXT,
    supplier TEXT,

    manufacturing_date DATE,
    expiry_date DATE,

    manufacturing_process_version TEXT,

    qc_status TEXT,
    release_status TEXT,

    metadata JSONB NOT NULL DEFAULT '{}',

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE(manufacturer, batch_number)
);

-- Table 6: Chemical Fingerprint (Section 10)
CREATE TABLE IF NOT EXISTS zfie_chemical_fingerprints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    batch_id UUID NOT NULL
        REFERENCES zfie_batches(id) ON DELETE CASCADE,

    method TEXT NOT NULL,
    instrument TEXT,

    algorithm_name TEXT,
    algorithm_version TEXT,

    fingerprint_hash TEXT,

    marker_compounds JSONB NOT NULL DEFAULT '[]',
    measured_compounds JSONB NOT NULL DEFAULT '[]',

    raw_data_uri TEXT,

    quality_status TEXT,

    measured_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- 3. PROVENANCE, LICENSES & EVIDENCE (Sections 21 - 23)
-- =============================================================================

-- Table 7: Provenance (Section 22)
CREATE TABLE IF NOT EXISTS zfie_provenance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    source_name TEXT NOT NULL,
    source_version TEXT,

    source_uri TEXT,

    retrieved_at TIMESTAMPTZ,

    transformation TEXT,

    transformation_version TEXT,

    checksum TEXT,

    notes TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 8: License Registry (Section 23)
CREATE TABLE IF NOT EXISTS zfie_licenses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    source_name TEXT NOT NULL,

    license_name TEXT,
    commercial_use_allowed BOOLEAN,
    derivative_use_allowed BOOLEAN,
    redistribution_allowed BOOLEAN,

    attribution_required BOOLEAN,

    restrictions TEXT,

    source_version TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 9: Evidence Bridge (Section 21)
CREATE TABLE IF NOT EXISTS zfie_evidence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    level evidence_level NOT NULL,
    status evidence_status NOT NULL,

    source_type TEXT NOT NULL,
    source_identifier TEXT,

    title TEXT,
    citation TEXT,

    study_design TEXT,
    population TEXT,
    species TEXT,
    tissue TEXT,

    dose TEXT,
    route TEXT,
    method TEXT,
    direction TEXT,

    publication_date DATE,

    reviewer_id UUID,

    provenance_id UUID REFERENCES zfie_provenance(id) ON DELETE SET NULL,
    license_id UUID REFERENCES zfie_licenses(id) ON DELETE SET NULL,

    limitations TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- 4. CHEMISTRY & MOLECULAR MAPPING (Sections 11 - 16)
-- =============================================================================

-- Table 10: Compounds (Section 11)
CREATE TABLE IF NOT EXISTS zfie_compounds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    canonical_name TEXT NOT NULL,

    canonical_smiles TEXT,
    inchi TEXT,
    inchikey TEXT,

    molecular_formula TEXT,
    molecular_weight NUMERIC,

    chemical_class TEXT,

    external_identifiers JSONB NOT NULL DEFAULT '{}',

    provenance_id UUID REFERENCES zfie_provenance(id) ON DELETE SET NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 11: Formulation -> Compound (Section 12)
CREATE TABLE IF NOT EXISTS zfie_formulation_compounds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    formulation_version_id UUID
        REFERENCES zfie_formulation_versions(id) ON DELETE CASCADE,

    batch_id UUID NULL
        REFERENCES zfie_batches(id) ON DELETE SET NULL,

    compound_id UUID NOT NULL
        REFERENCES zfie_compounds(id) ON DELETE RESTRICT,

    relationship_type TEXT NOT NULL,

    abundance NUMERIC,
    abundance_unit TEXT,

    measurement_method TEXT,

    evidence_id UUID NULL REFERENCES zfie_evidence(id) ON DELETE SET NULL,

    provenance_id UUID NULL REFERENCES zfie_provenance(id) ON DELETE SET NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 12: Targets (Section 13)
CREATE TABLE IF NOT EXISTS zfie_targets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    canonical_identifier TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,

    organism TEXT,
    target_type TEXT,

    external_identifiers JSONB NOT NULL DEFAULT '{}',

    provenance_id UUID REFERENCES zfie_provenance(id) ON DELETE SET NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 13: Compound -> Target (Section 14)
CREATE TABLE IF NOT EXISTS zfie_compound_targets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    compound_id UUID NOT NULL
        REFERENCES zfie_compounds(id) ON DELETE CASCADE,

    target_id UUID NOT NULL
        REFERENCES zfie_targets(id) ON DELETE CASCADE,

    relationship_type TEXT,
    activity_type TEXT,

    activity_value NUMERIC,
    activity_unit TEXT,

    assay_type TEXT,

    source_id TEXT,
    evidence_id UUID REFERENCES zfie_evidence(id) ON DELETE SET NULL,

    claim_origin claim_origin NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 14: Pathways (Section 15)
CREATE TABLE IF NOT EXISTS zfie_pathways (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    canonical_identifier TEXT NOT NULL,
    name TEXT NOT NULL,

    database_name TEXT,
    database_version TEXT,

    description TEXT,

    provenance_id UUID REFERENCES zfie_provenance(id) ON DELETE SET NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE(database_name, canonical_identifier, database_version)
);

-- Table 15: Target -> Pathway (Section 16)
CREATE TABLE IF NOT EXISTS zfie_target_pathways (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    target_id UUID NOT NULL
        REFERENCES zfie_targets(id) ON DELETE CASCADE,

    pathway_id UUID NOT NULL
        REFERENCES zfie_pathways(id) ON DELETE CASCADE,

    relationship_type TEXT,

    evidence_id UUID REFERENCES zfie_evidence(id) ON DELETE SET NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- 5. BIOLOGICAL STATES & ORGAN AXES (Sections 17 - 20)
-- =============================================================================

-- Table 16: Biological State (Section 17)
CREATE TABLE IF NOT EXISTS zfie_biological_states (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    name TEXT NOT NULL,
    domain TEXT NOT NULL,

    definition TEXT NOT NULL,

    criteria JSONB NOT NULL DEFAULT '{}',

    validated_status TEXT,

    version TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 17: Organ-Axis Link (Section 18)
CREATE TABLE IF NOT EXISTS zfie_biological_state_axes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    biological_state_id UUID NOT NULL
        REFERENCES zfie_biological_states(id) ON DELETE CASCADE,

    organ_axis_id UUID NOT NULL,

    relationship_type TEXT NOT NULL,

    evidence_id UUID REFERENCES zfie_evidence(id) ON DELETE SET NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 18: Biomarkers (Section 19)
CREATE TABLE IF NOT EXISTS zfie_biomarkers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    canonical_name TEXT NOT NULL,
    type TEXT,

    unit TEXT,

    normal_range JSONB,

    external_identifiers JSONB NOT NULL DEFAULT '{}',

    provenance_id UUID REFERENCES zfie_provenance(id) ON DELETE SET NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 19: Biomarker -> Biological State (Section 20)
CREATE TABLE IF NOT EXISTS zfie_biomarker_states (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    biomarker_id UUID NOT NULL
        REFERENCES zfie_biomarkers(id) ON DELETE CASCADE,

    biological_state_id UUID NOT NULL
        REFERENCES zfie_biological_states(id) ON DELETE CASCADE,

    relationship_type TEXT,

    evidence_id UUID REFERENCES zfie_evidence(id) ON DELETE SET NULL,

    claim_origin claim_origin NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- 6. HYPOTHESES, EXPERIMENTS & VALIDATION (Sections 24 - 27)
-- =============================================================================

-- Table 20: Hypotheses (Section 24)
CREATE TABLE IF NOT EXISTS zfie_hypotheses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    subject_type TEXT NOT NULL,
    subject_id UUID NOT NULL,

    statement TEXT NOT NULL,

    origin claim_origin NOT NULL,

    model_version TEXT,
    knowledge_version TEXT,

    status TEXT NOT NULL,

    created_by UUID,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 21: Experiments (Section 25)
CREATE TABLE IF NOT EXISTS zfie_experiments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    hypothesis_id UUID NOT NULL
        REFERENCES zfie_hypotheses(id) ON DELETE CASCADE,

    protocol_id TEXT,

    laboratory TEXT,
    operator_id UUID,

    planned_start TIMESTAMPTZ,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,

    status TEXT NOT NULL,

    raw_data_uri TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 22: Experiment Results (Section 26)
CREATE TABLE IF NOT EXISTS zfie_experiment_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    experiment_id UUID NOT NULL
        REFERENCES zfie_experiments(id) ON DELETE CASCADE,

    endpoint TEXT NOT NULL,

    value NUMERIC,
    unit TEXT,

    statistical_method TEXT,

    raw_data_uri TEXT,
    analysis_version TEXT,

    result_status TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 23: Validation Records (Section 27)
CREATE TABLE IF NOT EXISTS zfie_validation_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    hypothesis_id UUID NOT NULL
        REFERENCES zfie_hypotheses(id) ON DELETE CASCADE,

    experiment_id UUID NULL
        REFERENCES zfie_experiments(id) ON DELETE SET NULL,

    validation_state validation_state NOT NULL,

    evidence_level evidence_level NOT NULL,

    rationale TEXT,

    reviewer_id UUID,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- 7. CONTRADICTIONS, SYNERGY & SCIENTIFIC MEMORY (Sections 28 - 29)
-- =============================================================================

-- Table 24: Contradictions (Section 28) - First-Class Immutability Rule
CREATE TABLE IF NOT EXISTS zfie_contradictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    subject_type TEXT NOT NULL,
    subject_id UUID NOT NULL,

    evidence_a_id UUID NOT NULL
        REFERENCES zfie_evidence(id) ON DELETE RESTRICT,

    evidence_b_id UUID NOT NULL
        REFERENCES zfie_evidence(id) ON DELETE RESTRICT,

    contradiction_type TEXT,

    possible_explanations JSONB NOT NULL DEFAULT '[]',

    status TEXT NOT NULL DEFAULT 'OPEN',

    resolution TEXT,

    reviewer_id UUID,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 25: Synergy (Section 29)
CREATE TABLE IF NOT EXISTS zfie_synergy_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    formulation_version_id UUID
        REFERENCES zfie_formulation_versions(id) ON DELETE CASCADE,

    model TEXT NOT NULL,

    endpoint TEXT,

    dose_response_available BOOLEAN NOT NULL DEFAULT false,

    components JSONB NOT NULL DEFAULT '[]',

    result JSONB NOT NULL DEFAULT '{}',

    status TEXT NOT NULL DEFAULT 'SYNERGY_CANDIDATE',

    evidence_id UUID REFERENCES zfie_evidence(id) ON DELETE SET NULL,

    analysis_version TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- 8. REPRODUCIBILITY: ANALYSIS RUNS, MODELS & SNAPSHOTS (Sections 30 - 32)
-- =============================================================================

-- Table 26: Analysis Run (Section 30) - Master Reproducibility Object
CREATE TABLE IF NOT EXISTS zfie_analysis_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    analysis_code TEXT UNIQUE NOT NULL,

    subject_type TEXT NOT NULL,
    subject_id UUID NOT NULL,

    subject_version TEXT,

    mode analysis_mode NOT NULL,

    model_versions JSONB NOT NULL DEFAULT '{}',
    knowledge_version TEXT,

    safety_rule_version TEXT,

    input_snapshot JSONB NOT NULL DEFAULT '{}',
    output_snapshot JSONB NOT NULL DEFAULT '{}',

    status TEXT NOT NULL,

    error_details TEXT,

    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,

    created_by UUID
);

-- Table 27: Model Registry (Section 31)
CREATE TABLE IF NOT EXISTS zfie_models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    model_code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,

    version TEXT NOT NULL,

    intended_use TEXT,
    excluded_use TEXT,

    training_dataset TEXT,
    evaluation_dataset TEXT,

    limitations TEXT,

    release_status TEXT,

    approved_for_clinical_cds BOOLEAN NOT NULL DEFAULT false,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 28: Knowledge Snapshot (Section 32)
CREATE TABLE IF NOT EXISTS zfie_knowledge_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    snapshot_code TEXT UNIQUE NOT NULL,

    zkb_version TEXT,

    external_sources JSONB NOT NULL DEFAULT '{}',

    mapping_versions JSONB NOT NULL DEFAULT '{}',

    safety_version TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- 9. CLINICAL & OUTCOME LINKS (Sections 33 - 34)
-- =============================================================================

-- Table 29: Clinical Link (Section 33)
CREATE TABLE IF NOT EXISTS zfie_clinical_analysis_links (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    analysis_run_id UUID NOT NULL
        REFERENCES zfie_analysis_runs(id) ON DELETE CASCADE,

    patient_id UUID NOT NULL,
    encounter_id UUID NOT NULL,

    formulation_id UUID,

    review_status TEXT NOT NULL DEFAULT 'PENDING',

    clinician_id UUID,

    clinician_decision TEXT,

    reviewed_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 30: Outcome Link (Section 34)
CREATE TABLE IF NOT EXISTS zfie_outcome_links (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    formulation_id UUID,
    formulation_version_id UUID,
    batch_id UUID,

    patient_id UUID NULL,
    cohort_id UUID NULL,

    clinical_context JSONB,

    outcome_type TEXT NOT NULL,

    baseline_value JSONB,
    followup_value JSONB,

    measurement_time TIMESTAMPTZ,

    provenance_id UUID REFERENCES zfie_provenance(id) ON DELETE SET NULL,

    governance_status TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- 10. SAFETY & AUDIT EVENT ARCHITECTURE (Sections 22, 54, 55)
-- =============================================================================

-- Table 31: Safety Rules
CREATE TABLE IF NOT EXISTS zfie_safety_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_code TEXT UNIQUE NOT NULL,
    rule_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    severity safety_state NOT NULL DEFAULT 'CAUTION',
    condition_expression JSONB NOT NULL,
    remediation_text TEXT,
    active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 32: Negative Knowledge (Scientific Memory)
CREATE TABLE IF NOT EXISTS zfie_negative_knowledge (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject_type TEXT NOT NULL,
    subject_id UUID NOT NULL,
    claim_summary TEXT NOT NULL,
    falsification_reason TEXT NOT NULL,
    evidence_id UUID REFERENCES zfie_evidence(id) ON DELETE RESTRICT,
    falsified_by TEXT NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 33: Canonical Substance Identity (ZAY-MUF / ZAY-CMP Registry)
CREATE TABLE IF NOT EXISTS zfie_canonical_identities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    canonical_id TEXT UNIQUE NOT NULL,
    entity_type TEXT NOT NULL,
    primary_name TEXT NOT NULL,
    alternate_names JSONB NOT NULL DEFAULT '[]',
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 34: Immutable Audit Events Ledger (Section 54 - 55)
CREATE TABLE IF NOT EXISTS zfie_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id TEXT UNIQUE NOT NULL,
    event_type TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    entity_version TEXT,
    actor_id TEXT NOT NULL,
    actor_type TEXT NOT NULL CHECK (actor_type IN ('USER', 'SYSTEM', 'AI_AGENT')),
    model_version TEXT,
    knowledge_version TEXT,
    correlation_id TEXT NOT NULL,
    payload_hash TEXT,
    details JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- 11. DATABASE INDEXES (Section 62)
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_formulation_versions_formulation
    ON zfie_formulation_versions(formulation_id);

CREATE INDEX IF NOT EXISTS idx_ingredients_formulation_version
    ON zfie_formulation_ingredients(formulation_version_id);

CREATE INDEX IF NOT EXISTS idx_batches_formulation_version
    ON zfie_batches(formulation_version_id);

CREATE INDEX IF NOT EXISTS idx_formulation_compounds_formula
    ON zfie_formulation_compounds(formulation_version_id);

CREATE INDEX IF NOT EXISTS idx_compound_targets_compound
    ON zfie_compound_targets(compound_id);

CREATE INDEX IF NOT EXISTS idx_compound_targets_target
    ON zfie_compound_targets(target_id);

CREATE INDEX IF NOT EXISTS idx_target_pathways_target
    ON zfie_target_pathways(target_id);

CREATE INDEX IF NOT EXISTS idx_target_pathways_pathway
    ON zfie_target_pathways(pathway_id);

CREATE INDEX IF NOT EXISTS idx_evidence_level
    ON zfie_evidence(level);

CREATE INDEX IF NOT EXISTS idx_analysis_subject
    ON zfie_analysis_runs(subject_type, subject_id);

CREATE INDEX IF NOT EXISTS idx_contradictions_subject
    ON zfie_contradictions(subject_type, subject_id);

CREATE INDEX IF NOT EXISTS idx_events_correlation
    ON zfie_events(correlation_id);

CREATE INDEX IF NOT EXISTS idx_events_actor
    ON zfie_events(actor_type, actor_id);
