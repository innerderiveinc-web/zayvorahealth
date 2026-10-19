// =============================================================================
// ZAYVORA Formulation Intelligence Engine™ (ZFIE)
// Neo4j Graph Model & Cypher Schema Specification
// System: ZAYVORA Health OS™
// Core Chain: Mufrad -> Compound -> Target -> Pathway -> Biological Function -> Phenotype
// =============================================================================

// -----------------------------------------------------------------------------
// 1. CONSTRAINTS & UNIQUENESS
// -----------------------------------------------------------------------------

CREATE CONSTRAINT unique_mufrad_id IF NOT EXISTS
FOR (m:Mufrad) REQUIRE m.canonical_id IS UNIQUE;

CREATE CONSTRAINT unique_formulation_id IF NOT EXISTS
FOR (f:Formulation) REQUIRE f.formulation_code IS UNIQUE;

CREATE CONSTRAINT unique_version_id IF NOT EXISTS
FOR (v:FormulaVersion) REQUIRE v.version_id IS UNIQUE;

CREATE CONSTRAINT unique_batch_id IF NOT EXISTS
FOR (b:Batch) REQUIRE b.batch_id IS UNIQUE;

CREATE CONSTRAINT unique_compound_id IF NOT EXISTS
FOR (c:Compound) REQUIRE c.canonical_id IS UNIQUE;

CREATE CONSTRAINT unique_target_id IF NOT EXISTS
FOR (t:Target) REQUIRE t.canonical_id IS UNIQUE;

CREATE CONSTRAINT unique_pathway_id IF NOT EXISTS
FOR (p:Pathway) REQUIRE p.canonical_id IS UNIQUE;

CREATE CONSTRAINT unique_biostate_id IF NOT EXISTS
FOR (s:BiologicalState) REQUIRE s.state_id IS UNIQUE;

CREATE CONSTRAINT unique_biomarker_id IF NOT EXISTS
FOR (bm:Biomarker) REQUIRE bm.canonical_id IS UNIQUE;

CREATE CONSTRAINT unique_axis_id IF NOT EXISTS
FOR (a:OrganAxis) REQUIRE a.axis_id IS UNIQUE;

CREATE CONSTRAINT unique_evidence_id IF NOT EXISTS
FOR (e:Evidence) REQUIRE e.evidence_id IS UNIQUE;

CREATE CONSTRAINT unique_hypothesis_id IF NOT EXISTS
FOR (h:Hypothesis) REQUIRE h.hypothesis_id IS UNIQUE;

CREATE CONSTRAINT unique_experiment_id IF NOT EXISTS
FOR (x:Experiment) REQUIRE x.experiment_id IS UNIQUE;

CREATE CONSTRAINT unique_outcome_id IF NOT EXISTS
FOR (o:Outcome) REQUIRE o.outcome_id IS UNIQUE;

CREATE CONSTRAINT unique_memory_id IF NOT EXISTS
FOR (sm:ScientificMemory) REQUIRE sm.memory_id IS UNIQUE;

// -----------------------------------------------------------------------------
// 2. NODE LABELS (Section 35)
// -----------------------------------------------------------------------------
// (:Mufrad { canonical_id, name, unani_name, latin_name, plant_part, mizaj_primary, mizaj_secondary, status })
// (:Formulation { formulation_code, canonical_name, traditional_name, status, therapeutic_objective })
// (:FormulaVersion { version_id, version_label, version_number, preparation_method, change_reason, review_status })
// (:Batch { batch_id, batch_number, manufacturer, mfg_date, exp_date, qc_status })
// (:Compound { canonical_id, name, smiles, inchi, inchikey, molecular_weight, chemical_class })
// (:Target { canonical_id, name, organism, target_type, uniprot_id, pdb_id })
// (:Pathway { canonical_id, name, database_name, database_version })
// (:BiologicalState { state_id, name, domain, definition, validated_status })
// (:Biomarker { canonical_id, name, type, unit, normal_range })
// (:Phenotype { phenotype_id, term, icd10_code, namaste_code })
// (:OrganAxis { axis_id, name, primary_organ, associated_humor, classical_concept })
// (:Evidence { evidence_id, level, status, source_type, title, citation, direction })
// (:Hypothesis { hypothesis_id, statement, origin, status, falsification_criteria })
// (:Experiment { experiment_id, protocol_id, laboratory, status, raw_data_uri })
// (:Outcome { outcome_id, outcome_type, baseline_value, followup_value, clinical_context })
// (:ScientificMemory { memory_id, claim_summary, falsification_reason, falsified_by, recorded_at })

// -----------------------------------------------------------------------------
// 3. CORE RELATIONSHIPS & PROPERTY RULES (Sections 36 & 37)
// Mandatory properties for every relationship:
// - evidence_id: string
// - provenance_id: string
// - claim_origin: 'OBSERVED' | 'CURATED' | 'CALCULATED' | 'PREDICTED' | 'INFERRED' | 'UNKNOWN'
// - source_version: string
// - created_at: datetime
// - algorithm_version: string
// -----------------------------------------------------------------------------

// (1) Mufrad -> Formulation
// (Mufrad)-[:COMPONENT_OF { ratio, plant_part, preparation_state, evidence_id, provenance_id, claim_origin }]->(Formulation)

// (2) Formulation -> FormulaVersion
// (Formulation)-[:HAS_VERSION { effective_from, review_status, evidence_id, provenance_id }]->(FormulaVersion)

// (3) FormulaVersion -> Batch
// (FormulaVersion)-[:HAS_BATCH { release_date, qc_status, evidence_id, provenance_id }]->(Batch)

// (4) Batch -> Compound (Measured / Fingerprinted)
// (Batch)-[:CONTAINS_COMPOUND { abundance, abundance_unit, measurement_method, evidence_id, provenance_id, claim_origin: 'OBSERVED' }]->(Compound)

// (5) FormulaVersion -> Compound (Predicted / Nominal)
// (FormulaVersion)-[:HAS_COMPOUND { expected_range, extraction_efficiency, evidence_id, provenance_id, claim_origin: 'CALCULATED' }]->(Compound)

// (6) Compound -> Target
// (Compound)-[:ASSOCIATED_WITH_TARGET { binding_affinity_kd, ic50_nm, docking_score_kcal_mol, activity_type, evidence_id, provenance_id, claim_origin }]->(Target)

// (7) Target -> Pathway
// (Target)-[:PART_OF_PATHWAY { role, impact_factor, evidence_id, provenance_id, claim_origin }]->(Pathway)

// (8) Pathway -> BiologicalState
// (Pathway)-[:ASSOCIATED_WITH_STATE { correlation, modulation_direction, evidence_id, provenance_id, claim_origin }]->(BiologicalState)

// (9) BiologicalState -> OrganAxis
// (BiologicalState)-[:RELEVANT_TO_AXIS { axis_relevance_score, evidence_id, provenance_id, claim_origin }]->(OrganAxis)

// (10) Biomarker -> BiologicalState
// (Biomarker)-[:ASSOCIATED_WITH_STATE { sensitivity, specificity, evidence_id, provenance_id, claim_origin }]->(BiologicalState)

// (11) Formulation -> Evidence
// (Formulation)-[:SUPPORTED_BY { evidence_level, study_type, evidence_id, provenance_id }]->(Evidence)

// (12) Compound -> Evidence
// (Compound)-[:SUPPORTED_BY { evidence_level, assay_type, evidence_id, provenance_id }]->(Evidence)

// (13) Target -> Evidence
// (Target)-[:SUPPORTED_BY { validation_method, evidence_id, provenance_id }]->(Evidence)

// (14) Hypothesis -> Experiment
// (Hypothesis)-[:TESTED_BY { experiment_role, protocol_reference, created_at }]->(Experiment)

// (15) Experiment -> Evidence
// (Experiment)-[:GENERATES { p_value, effect_size, replicates, evidence_id, provenance_id }]->(Evidence)

// (16) Formulation -> Outcome
// (Formulation)-[:OBSERVED_WITH { cohort_size, effect_delta, evidence_id, provenance_id }]->(Outcome)

// (17) Formulation -> ScientificMemory (Negative Knowledge)
// (Formulation)-[:REFUTED_BY { falsification_reason, evidence_id, recorded_at }]->(ScientificMemory)

// -----------------------------------------------------------------------------
// 4. REPRESENTATIVE CYPHER SEED (Suranjan Shirin / Colchicine Subgraph)
// -----------------------------------------------------------------------------

MERGE (m:Mufrad { canonical_id: 'ZAY-MUF-0001' })
ON CREATE SET
  m.name = 'Suranjan Shirin',
  m.unani_name = 'سورنجان شیریں',
  m.latin_name = 'Colchicum autumnale L.',
  m.plant_part = 'Corm',
  m.mizaj_primary = 'Cold',
  m.mizaj_secondary = 'Dry',
  m.status = 'ACTIVE';

MERGE (f:Formulation { formulation_code: 'ZAY-FORM-0001' })
ON CREATE SET
  f.canonical_name = 'Majun Suranjan',
  f.traditional_name = 'معجون سورنجان',
  f.status = 'APPROVED',
  f.therapeutic_objective = 'Arthritis, Gout, Joint Inflammation (Waja-ul-Mafasil)';

MERGE (v:FormulaVersion { version_id: 'ZAY-FORM-0001-v1.1' })
ON CREATE SET
  v.version_label = 'v1.1',
  v.version_number = 1,
  v.preparation_method = 'Classical Decoction & Honey Confection',
  v.review_status = 'APPROVED';

MERGE (c:Compound { canonical_id: 'ZAY-CMP-0001' })
ON CREATE SET
  c.name = 'Colchicine',
  c.smiles = 'CC(=O)NC1CCC2=CC(=O)C(=C(C2=C3C1=CC(=C(C3=O)OC)OC)OC)OC',
  c.chemical_class = 'Tropolone Alkaloid',
  c.molecular_weight = 399.44;

MERGE (t:Target { canonical_id: 'ZAY-TGT-0001' })
ON CREATE SET
  t.name = 'Tubulin beta chain',
  t.canonical_identifier = 'TUBB_HUMAN',
  t.organism = 'Homo sapiens',
  t.target_type = 'Structural Protein';

MERGE (p:Pathway { canonical_id: 'ZAY-PATH-0001' })
ON CREATE SET
  p.name = 'Microtubule Cytoskeleton Dynamics & Neutrophil Extravasation',
  p.database_name = 'Reactome',
  p.database_version = 'v84';

MERGE (s:BiologicalState { state_id: 'ZAY-BIO-0001' })
ON CREATE SET
  s.name = 'Acute Crystal-Induced Synovial Inflammation',
  s.domain = 'Rheumatology / Waja-ul-Mafasil',
  s.validated_status = 'EXPERIMENTALLY_SUPPORTED';

MERGE (a:OrganAxis { axis_id: 'ZAY-AXIS-0007' })
ON CREATE SET
  a.name = 'Musculoskeletal-Metabolic Axis',
  a.primary_organ = 'Joints / Synovium / Kidney',
  a.associated_humor = 'Balgham-e-Fasid / Khilt-e-Ghaliz';

MERGE (e:Evidence { evidence_id: 'ZAY-EVD-91' })
ON CREATE SET
  e.level = 'E5',
  e.status = 'ESTABLISHED',
  e.source_type = 'CLINICAL_TRIAL',
  e.title = 'Colchicine in the Treatment and Prophylaxis of Acute Gout Flares',
  e.direction = 'INHIBITORY';

// Link nodes with typed, auditable property schema
MERGE (m)-[:COMPONENT_OF { ratio: 0.35, plant_part: 'Purified Corm', claim_origin: 'CURATED' }]->(f);
MERGE (f)-[:HAS_VERSION { review_status: 'APPROVED', claim_origin: 'CURATED' }]->(v);
MERGE (v)-[:HAS_COMPOUND { abundance_mg_per_g: 1.2, claim_origin: 'CURATED' }]->(c);
MERGE (c)-[:ASSOCIATED_WITH_TARGET {
  activity_type: 'Inhibition',
  ic50_nm: 3.2,
  docking_score_kcal_mol: -8.9,
  evidence_id: 'ZAY-EVD-91',
  provenance_id: 'ZAY-PROV-PDB-1SA0',
  claim_origin: 'PREDICTED',
  algorithm_version: 'AutoDock-Vina-1.2.5'
}]->(t);
MERGE (t)-[:PART_OF_PATHWAY { role: 'Direct Subunit Binding', claim_origin: 'CURATED' }]->(p);
MERGE (p)-[:ASSOCIATED_WITH_STATE { modulation_direction: 'DOWNREGULATION', claim_origin: 'CURATED' }]->(s);
MERGE (s)-[:RELEVANT_TO_AXIS { axis_relevance_score: 0.94, claim_origin: 'CURATED' }]->(a);
MERGE (f)-[:SUPPORTED_BY { evidence_level: 'E5', evidence_id: 'ZAY-EVD-91' }]->(e);
MERGE (c)-[:SUPPORTED_BY { evidence_level: 'E5', evidence_id: 'ZAY-EVD-91' }]->(e);
MERGE (t)-[:SUPPORTED_BY { evidence_level: 'E5', evidence_id: 'ZAY-EVD-91' }]->(e);
