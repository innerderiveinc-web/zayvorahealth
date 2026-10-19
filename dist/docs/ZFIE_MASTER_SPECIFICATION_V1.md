# ZAYVORA Formulation Intelligence Engine™ (ZFIE)
## Technical PRD, Data Architecture, API Contract & Production Integration Blueprint

### Document Status
**Classification:** Production Architecture Proposal & Enterprise Master Specification  
**System:** ZAYVORA Health OS™  
**Scientific Layer:** ZAYVORA Formulation Intelligence Engine™ (ZFIE)  
**Primary AI Interface:** Hakeem Sahab AI™  
**Authority:** Clinician-controlled (Non-Autonomous)  
**Execution Mode:** Research → Shadow → Controlled Clinical Decision Support  
**Version:** 1.0.0-RELEASE (Canonical)

---

# 1. Product Definition

ZFIE is the computational scientific layer of ZAYVORA Health OS™ responsible for modelling, analysing, comparing and validating multi-component formulations.

It is **not** an autonomous prescribing engine.

Its job is to transform:

**Mufradat → Composition → Constituents → Molecular Targets → Pathways → Biological Context → Exposure → Safety → Evidence → Validation → Clinical Consideration**

while maintaining provenance and uncertainty throughout the chain.

The source architecture explicitly defines formulation as a first-class computational object and introduces the Computational Formulation Twin for this purpose.

---

# 2. Strategic Position

ZFIE should not replace:
* ZAYVORA Knowledge Intelligence™
* Mizaj framework
* Afaal reasoning
* Organ-Axis reasoning
* Clinical protocols
* Nuskha workflow
* Safety Firewall
* Clinician approval

Instead:

```text
ZKB
  ↓
authoritative knowledge

ZFIE
  ↓
computational inference

Validation Engine
  ↓
experimental truth

Clinical Intelligence
  ↓
clinically relevant interpretation

Clinician
  ↓
final decision
```

---

# 3. Product Objectives

## Primary Objectives
* **O1 — Computational formulation representation:** Represent every formulation as a versioned computational object.
* **O2 — Molecular traceability:** Trace relationships from Mufrad → constituent → target → pathway → biological function.
* **O3 — Evidence-grounded inference:** Every meaningful inference must be traceable to evidence, data, method and version.
* **O4 — Batch intelligence:** Distinguish Formula from Batch and permit comparison of measured batch fingerprints.
* **O5 — Scientific uncertainty:** Never collapse heterogeneous evidence into a misleading single confidence score.
* **O6 — Experimental learning:** Allow hypotheses to move through controlled validation.
* **O7 — Clinical integration:** Give clinicians useful mechanistic and safety context without autonomous treatment decisions.
* **O8 — Proprietary knowledge moat:** Capture ZAYVORA's formulation, manufacturing, experimental and longitudinal outcome relationships.

---

# 4. Non-Goals

The initial system must not attempt to build:
* autonomous diagnosis
* autonomous prescribing
* automatic Nuskha approval
* uncontrolled patient-data model training
* generic chatbot-only experience
* docking-only efficacy claims
* a giant disease encyclopedia before core validation
* unsupported biomarker → Mizaj equivalence
* unvalidated "synergy confirmed" claims

---

# 5. System Architecture

```text
                         ZAYVORA HEALTH OS
                                │
 ┌──────────────────────────────┼─────────────────────────────┐
 │                              │                             │
 ▼                              ▼                             ▼
KNOWLEDGE                  CLINICAL                     OPERATIONS
INTELLIGENCE              INTELLIGENCE                  INTELLIGENCE
 │                              │                             │
 └───────────────┬──────────────┘                             │
                 ▼                                            │
      FORMULATION INTELLIGENCE ENGINE                          │
                 │                                             │
 ┌───────────────┼────────────────────────────────────────────┐│
 │               │                 │                           ││
 ▼               ▼                 ▼                           ▼│
Identity      Chemistry        Molecular                  Batch/QC
Engine        Engine           Intelligence               Intelligence
 │               │                 │                           │
 └───────────────┼─────────────────┼───────────────────────────┘
                 ▼
          Network Pharmacology
                 │
                 ▼
          Biological State
                 │
        ┌────────┴─────────┐
        ▼                  ▼
     Exposure            Safety
        │                  │
        └────────┬─────────┘
                 ▼
             Evidence
                 │
        ┌────────┴─────────┐
        ▼                  ▼
 Contradiction          Synergy
    Engine              Engine
        │                  │
        └────────┬─────────┘
                 ▼
          Validation Engine
                 │
                 ▼
        Experiment Planner
                 │
                 ▼
         Hakeem Sahab AI™
                 │
                 ▼
        Clinician Review
                 │
                 ▼
        Existing Nuskha Flow
                 │
                 ▼
             Patient
                 │
                 ▼
        Follow-up / Outcomes
                 │
                 ▼
          Research Dataset
```

---

# 6. Bounded Contexts

* **Context A — Identity:** Canonical identities and entity resolution (`Mufrad`, `Murakkab`, `Formulation`, `FormulaVersion`, `Batch`, `Compound`, `Target`, `Pathway`, `Biomarker`, `Evidence`, `Experiment`, `Outcome`).
* **Context B — Formulation:** Composition, ingredient ratios, preparation method, formula versioning, formulation status, manufacturing links.
* **Context C — Molecular:** Chemical structures, constituent mapping, target associations, bioactivity, molecular similarity, computational predictions.
* **Context D — Network:** Formulation → compound → target → pathway → biological system → Organ-Axis relationships.
* **Context E — Exposure:** Dose assumptions, route, bioavailability, metabolism, PK/PD evidence, exposure uncertainty.
* **Context F — Safety:** Toxicity signals, interaction risks, contraindications, organ-specific risks, dose-related concerns, patient-level safety checks.
* **Context G — Evidence:** Evidence Bridge attaching source, study, methodology, species, tissue, dose, direction, evidence level, date and reviewer.
* **Context H — Validation:** Hypotheses, experiment plans, experiments, measurements, results, replication, validation state.
* **Context I — Clinical Intelligence:** Transforming scientific outputs into clinician-readable considerations.

---

# 7. Canonical Identity Model

Authoritative persistent IDs:
```text
MUF-000421         (Mufrad Botanical)
FORM-000018        (Formulation Twin)
FORM-000018-V1.2   (Formula Version)
BATCH-2026-0041    (Physical Lot)
CMP-009871         (Phytochemical)
TGT-002187         (Protein Target)
PATH-001104        (Biological Pathway)
BIO-000087         (Biomarker)
EVD-004812         (Evidence Record)
EXP-001203         (Validation Experiment)
OUT-000893         (Clinical Outcome)
```

---

# 8. Computational Formulation Twin

**Entity:** `computational_formulation_twin`
- **Core fields:** `id`, `formulation_id`, `formula_version_id`, `traditional_system`, `classical_definition`, `clinical_objective`, `status`, `created_at`, `updated_at`, `created_by`, `reviewed_by`, `knowledge_version`.
- **Nested domains:** `identity`, `ingredients`, `preparation`, `manufacturing`, `batch`, `chemistry`, `biology`, `pharmacology`, `exposure`, `safety`, `evidence`, `validation`, `clinical_links`, `outcomes`.

---

# 9. PostgreSQL Data Model

Authoritative tables:
* `mufradat`: Botanical substances, taxonomy, classical references.
* `formulations`: Multi-component formulation entities.
* `formulation_versions`: Immutable formula versioning with change tracking.
* `formulation_ingredients`: Quantities, parts, ratios, and preparation states.
* `batches`: Physical manufacturing records linked to formula versions.
* `chemical_fingerprints`: HPLC/GC/MS assays, raw data URIs, fingerprint hashes.
* `compounds`: IUPAC, SMILES, InChIKey, molecular formula, weight.
* `compound_formulation_links`: Constituent abundance and measurement type.
* `targets`: Gene symbols, UniProt accessions, ChEMBL target IDs.
* `compound_target_links`: Binding activities, assay types, and evidence links.
* `pathways`: Reactome/KEGG identifiers and descriptions.
* `target_pathway_links`: Target involvement in cellular cascades.
* `biological_states`: Metabolic, inflammatory, hepatic, oxidative criteria.
* `evidence_records`: E0–E6 levels, study design, citations, and reviews.
* `hypotheses`: Scientific assertions with model and knowledge provenance.
* `experiments`: Laboratory protocols, operators, and statuses.
* `experiment_results`: Endpoints, values, and raw spectrum references.
* `safety_rules`: Risk severity, contraindications, and condition predicates.
* `outcomes`: Longitudinal patient biomarker deltas and batch correlations.

---

# 10. Graph Model — Neo4j

Core nodes: `Mufrad`, `Formulation`, `FormulaVersion`, `Batch`, `Compound`, `Target`, `Pathway`, `BiologicalState`, `Biomarker`, `Phenotype`, `Evidence`, `Experiment`, `Outcome`, `OrganAxis`.

Key traversals:
```cypher
(:Mufrad)-[:CONTAINS]->(:Compound)
(:Formulation)-[:HAS_VERSION]->(:FormulaVersion)-[:PRODUCED_AS]->(:Batch)
(:Compound)-[:ASSOCIATED_WITH]->(:Target)-[:PART_OF]->(:Pathway)
(:Pathway)-[:RELEVANT_TO]->(:BiologicalState)-[:MAPS_TO]->(:OrganAxis)
(:Biomarker)-[:INDICATES]->(:BiologicalState)
(:Hypothesis)-[:VALIDATED_BY]->(:Experiment)-[:GENERATED]->(:Evidence)
(:Formulation)-[:OBSERVED_WITH]->(:Outcome)
```

---

# 11. Evidence Bridge & Scientific Evidence Ladder

**Hierarchy:**
* **E0:** AI Hypothesis
* **E1:** Literature Association
* **E2:** Computational Prediction (Docking / In-Silico Energetics)
* **E3:** In-Vitro Cellular / Enzymatic Assays
* **E4:** In-Vivo Animal Disease Models
* **E5:** Human Observational / Pharmacokinetic (PK) Cohorts
* **E6:** Controlled Multi-Center Clinical Evidence (RCT)

**State Vocabulary:** `ESTABLISHED`, `SUPPORTED`, `COMPUTATIONALLY_PREDICTED`, `TRADITIONAL_CLAIM`, `CONFLICTING`, `UNKNOWN`.

---

# 12. Scientific Confidence Model

Never collapse heterogeneous evidence into a single misleading score. Maintain independent multidimensional confidence:
```json
{
  "traditional": "strong",
  "chemical": "strong",
  "target": "moderate",
  "pathway": "moderate",
  "exposure": "weak",
  "safety": "moderate",
  "human": "limited",
  "combination": "unvalidated"
}
```

---

# 13. Provenance & License Registry

Every dataset and reference tracks `source_name`, `source_version`, `source_url`, `download_date`, `license`, `commercial_use`, and field-level restrictions.

---

# 14. API Architecture

Base URI: `/api/v1`
* `/formulations`, `/formulations/:id/versions`, `/formulations/:id/twin`, `/formulations/:id/analyze`
* `/compounds/:id`, `/formulations/:id/compounds`, `/batches/:id/fingerprint`
* `/compounds/:id/targets`, `/targets/:id/pathways`, `/molecular/analysis`
* `/network/analyze`, `/formulations/:id/network`, `/targets/:id/network`
* `/evidence/:id`, `/formulations/:id/evidence`
* `/safety/check`, `/formulations/:id/safety`
* `/hypotheses`, `/experiments`, `/experiments/:id/results`, `/validation/assess`
* `/clinical/formulation-intelligence`, `/encounters/:id/formulation-intelligence`

---

# 15. Standard Intelligence Response Contract

```json
{
  "request_id": "req_123",
  "entity_id": "FORM-000018",
  "entity_version": "1.2",
  "finding": {
    "type": "mechanistic_hypothesis",
    "statement": "Colchicine inhibits tubulin polymerization and NLRP3 inflammasome"
  },
  "evidence": [
    {
      "evidence_id": "EVD-004812",
      "level": "E2",
      "status": "COMPUTATIONALLY_PREDICTED"
    }
  ],
  "confidence": {
    "overall": null,
    "dimensions": {
      "traditional": "strong",
      "chemical": "strong",
      "target": "moderate",
      "human": "limited"
    }
  },
  "safety": {
    "state": "CAUTION",
    "issues": []
  },
  "contradictions": [],
  "unknowns": [],
  "model": {
    "name": "ZFIE-MECH-001",
    "version": "0.4"
  },
  "knowledge": {
    "version": "zkb-2026.09"
  },
  "clinical_action": {
    "requires_clinician_review": true,
    "autonomous_action_allowed": false
  }
}
```

---

# 16. Safety Firewall Contract

Enforces authoritative verdicts:
* `PASS`: Permitted to continue to next workflow stage.
* `CAUTION`: Requires explicit clinician acknowledgment.
* `BLOCK`: Strictly prohibits downstream clinical execution.
* `UNKNOWN`: Insufficient evidence to proceed.

---

# 17–19. Hakeem Sahab AI™ Orchestration & Multi-Agent Architecture

Multi-Agent Ensemble:
1. Literature Curator
2. Entity Resolution Agent
3. Evidence Auditor
4. Mechanism Analyst
5. Synergy Analyst
6. Safety Analyst
7. Formulation Scientist Copilot
8. Validation Planner

**Strict Agent Rule:** Agents emit *proposal objects*, never authorized clinical orders.

---

# 20–24. Validation, Batch Intelligence & Versioning

* **Experiment Planner:** Recommends experiments based on maximum uncertainty reduction per unit cost/time.
* **Research / Clinical Separation:** Clinical patient PHI is isolated from de-identified research datasets.
* **Formula ≠ Batch:** Multiple manufacturing lots with distinct measured fingerprints link to a single formula version.

---

# 25–31. Clinical Desk & UI Experience

* **Doctor Desk:** Simple 8-tab panel with "Why this?" evidence drawer; non-blocking decision support.
* **Research Workspace:** Deep network topology, in-silico docking energetics, and raw spectra inspection.
* **Synergy UX:** Labeled as `SYNERGY CANDIDATE`, never "Confirmed Synergy" without wet-lab assay.
* **Biological State UX:** Assessed as multi-system physiological pattern, not reductionist disease label.

---

# 32–35. Permissions, Security & Shadow Mode

* RBAC roles: `SUPER_ADMIN`, `DOCTOR`, `HAKEEM_AI`, `RESEARCHER`, `PHARMACIST`, `QC_SCIENTIST`, `AUDITOR`.
* Strict invariant: `HAKEEM_AI` cannot prescribe, approve, or bypass safety firewalls.
* Shadow Mode: ZFIE executes alongside existing clinical logic, recording comparisons without modifying patient care.

---

# 36–45. Architecture, Audit & Outcome Loop

* Modular monolith structure (`services/knowledge`, `services/therapeutic`, `services/clinical`, `services/ai`).
* Deterministic logic (safety, permissions, units) separated from probabilistic inference (docking, text mining).
* Longitudinal closed-loop connects batch potencies with biomarker trajectories.

---

# 46–48. Initial Pilot & MVP Scope

* **Pilot Domains:** Metabolic (Glucovora) + Liver (LiverPrime) + Gut/Joints (Majun Suranjan).
* **MVP Scope:** One verified formulation + version + batch generating traceable targets, pathways, evidence, safety, and validation state.

---

# 49. The 12 MVP Acceptance Tests (AT-01 to AT-12)

* **AT-01:** Create formulation → create version → create batch.
* **AT-02:** Modify ingredient ratio → new formula version automatically created.
* **AT-03:** Run analysis → result contains model and knowledge versions.
* **AT-04:** Every molecular relationship has evidence/provenance.
* **AT-05:** Computational prediction is labelled E2 / E0.
* **AT-06:** No E2 output can be represented as E5/E6.
* **AT-07:** Safety BLOCK prevents downstream clinical execution.
* **AT-08:** AI cannot approve its own recommendation.
* **AT-09:** Contradictory evidence remains visible.
* **AT-10:** Research data cannot silently enter production training.
* **AT-11:** Old analysis remains reproducible after knowledge update.
* **AT-12:** Clinician can inspect "Why this?"

---

# 50–53. Final Invariants & Product Moat

**The Definitive Core Principle:**
> **"Knowledge informs. Computation infers. Evidence qualifies. Safety constrains. Validation verifies. AI explains. Tools execute only authorized actions. The clinician decides. Governance learns."**
