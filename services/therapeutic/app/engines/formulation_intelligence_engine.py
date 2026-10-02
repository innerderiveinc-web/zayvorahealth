"""
ZAYVORA HEALTH OS™ — Computational Formulation Intelligence Engine™
Governed Scientific Intelligence Layer (Blueprint §16–§20, §26–§33, §47–§52)

Core Capabilities:
1. Multi-scale Mapping: Botanical Constituents -> Phytochemicals -> Molecular Targets -> Pathways
2. Organ-Axis Translation: Unani Mizaj & Afaal <-> Modern Systems Biology & Molecular Targets
3. Synergy & Musleh Adjuvant Analyzer: Pharmacokinetic/Pharmacodynamic synergy & toxicity mitigation
4. Independent Safety Engine: Evaluates patient profile, organ function, Schedule E1, dose limits, drug-herb interactions. Verdicts: PASS, CAUTION, BLOCK, UNKNOWN
5. Scientific Memory™ & Contradiction Engine: Negative knowledge tracking, falsification guard, failed hypothesis registry
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from services.knowledge.app.core.canonical_identity_service import (
    CanonicalIdentityRegistry,
    CanonicalSubstanceRecord,
    CanonicalCompoundRecord,
    CanonicalTargetRecord,
    CanonicalPathwayRecord
)
from services.therapeutic.app.models.computational_twin import (
    FormulationDigitalTwin,
    FormulationTwinRegistry,
    BatchManufacturingTwin,
    QualityStatus
)
from services.knowledge.app.engines.evidence_bridge import (
    EvidenceBridgeEngine,
    EvidenceLevel
)


class SafetyVerdict(str, Enum):
    PASS = "PASS"
    CAUTION = "CAUTION"
    BLOCK = "BLOCK"
    UNKNOWN = "UNKNOWN"


@dataclass
class SafetyEvaluationResult:
    verdict: SafetyVerdict
    safety_score: float                     # 0.0 to 1.0 (1.0 = optimal safety)
    risk_factors: List[str] = field(default_factory=list)
    contraindications: List[str] = field(default_factory=list)
    schedule_e1_cleared: bool = True
    organ_clearance_ok: bool = True
    cyp450_interaction_risk: str = "LOW"    # "LOW", "MODERATE", "HIGH"
    clinician_action_required: Optional[str] = None
    scientific_rationale: str = ""
    tamper_proof_hash: str = ""

    def __post_init__(self):
        if not self.tamper_proof_hash:
            raw = f"{self.verdict.value}:{self.safety_score}:{len(self.risk_factors)}:{self.schedule_e1_cleared}"
            self.tamper_proof_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @property
    def contraindication_alerts(self) -> List[str]:
        return self.contraindications

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verdict": self.verdict.value,
            "safety_score": self.safety_score,
            "risk_factors": self.risk_factors,
            "contraindications": self.contraindications,
            "contraindication_alerts": self.contraindications,
            "schedule_e1_cleared": self.schedule_e1_cleared,
            "organ_clearance_ok": self.organ_clearance_ok,
            "cyp450_interaction_risk": self.cyp450_interaction_risk,
            "clinician_action_required": self.clinician_action_required,
            "scientific_rationale": self.scientific_rationale,
            "tamper_proof_hash": self.tamper_proof_hash
        }


@dataclass
class ContradictionRecord:
    contradiction_id: str                   # ZAY-NEG-XXXX
    subject_entity: str                     # e.g., "Colchicum luteum (Kham/Raw)"
    claim_refuted: str                      # e.g., "Raw Colchicum can be safely administered without Mudabbar boiling"
    reason_for_refutation: str              # e.g., "Causes acute mucosal necrosis and severe gastroenteritis"
    falsification_evidence: str             # UPI Monograph / Ayush Pharmacovigilance 2024
    severity: str                           # "HIGH_TOXICITY", "INEFFECTIVE", "METABOLIC_INTERFERENCE"
    registered_at: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = "BLOCKED"
        d["refuted_claim"] = self.claim_refuted
        d["opposing_study"] = self.falsification_evidence
        return d


class ScientificMemoryRegistry:
    """Authoritative memory of negative knowledge, failed clinical hypotheses, and toxic combinations."""

    _contradictions: Dict[str, ContradictionRecord] = {}

    @classmethod
    def initialize_seeds(cls) -> None:
        if cls._contradictions:
            return

        cls.register_contradiction(ContradictionRecord(
            contradiction_id="ZAY-NEG-0001",
            subject_entity="Suranjan Shirin (Raw / Kham)",
            claim_refuted="Direct raw powdered Colchicum luteum corm administration is equivalent to Mudabbar preparation.",
            reason_for_refutation="Raw corm contains unbound alkaloidal glycosides that trigger intense GI mucosal inflammation, emesis, and intestinal cramping. Mudabbar detoxification via milk boiling or vinegar soaking is mandatory.",
            falsification_evidence="Unani Pharmacopoeia of India Part I Vol I, pp. 94-96; Ayush Pharmacovigilance Safety Directive 2024",
            severity="HIGH_TOXICITY",
            registered_at="2026-01-15T00:00:00Z"
        ))

        cls.register_contradiction(ContradictionRecord(
            contradiction_id="ZAY-NEG-0002",
            subject_entity="Colchicum + High-dose Clarithromycin / Ketoconazole",
            claim_refuted="Colchicum luteum formulations can be co-administered with potent CYP3A4 and P-gp inhibitors without dose modification.",
            reason_for_refutation="Potent CYP3A4 inhibitors increase systemic colchicine AUC by 200-300%, leading to fatal bone marrow suppression and multiorgan toxicity.",
            falsification_evidence="FDA Drug Safety Communication / Clinical Pharmacokinetics 47(5): 301-314",
            severity="HIGH_TOXICITY",
            registered_at="2026-02-10T00:00:00Z"
        ))

        cls.register_contradiction(ContradictionRecord(
            contradiction_id="ZAY-NEG-0003",
            subject_entity="Gurmar (Gymnema) in acute insulin-dependent ketoacidosis",
            claim_refuted="Gymnema sylvestre can serve as an acute monotherapy replacement for insulin in Type 1 Diabetes or DKA.",
            reason_for_refutation="Gymnema stimulates endogenous beta-cell insulin secretion and reduces intestinal glucose uptake; it cannot replace absolute insulin deficiency and poses fatal ketoacidosis risk if insulin is withheld.",
            falsification_evidence="Diabetes Care 32(8): e98; Endocrine Practice Review 2023",
            severity="HIGH_TOXICITY",
            registered_at="2026-03-01T00:00:00Z"
        ))

    @classmethod
    def register_contradiction(cls, rec: ContradictionRecord) -> ContradictionRecord:
        cls._contradictions[rec.contradiction_id] = rec
        cls._contradictions[rec.subject_entity.lower().strip()] = rec
        return rec

    @classmethod
    def list_contradictions(cls) -> List[Dict[str, Any]]:
        cls.initialize_seeds()
        seen = set()
        out = []
        for r in cls._contradictions.values():
            if r.contradiction_id not in seen:
                seen.add(r.contradiction_id)
                out.append(r.to_dict())
        return out

    @classmethod
    def check_for_contradictions(cls, entity_name: str, context: Optional[str] = None) -> List[Dict[str, Any]]:
        cls.initialize_seeds()
        matches = []
        q = entity_name.lower().strip()
        for r in cls._contradictions.values():
            if q in r.subject_entity.lower() or (context and context.lower() in r.subject_entity.lower()):
                if r.to_dict() not in matches:
                    matches.append(r.to_dict())
        return matches


# Seed Scientific Memory
ScientificMemoryRegistry.initialize_seeds()


class FormulationIntelligenceEngine:
    """The central computational formulation intelligence engine."""

    @classmethod
    def get_formulation_intelligence_summary(cls, formulation_id: str) -> Optional[Dict[str, Any]]:
        """Synthesizes the complete digital twin, target network, pathways, evidence, and HPLC batch profile."""
        twin = FormulationTwinRegistry.get_twin(formulation_id)
        if not twin:
            return None

        # 1. Resolve Constituents and Phytochemicals
        constituents_detail = []
        all_compounds = []
        for c in twin.constituents:
            muf_rec = CanonicalIdentityRegistry.get_substance(c.substance_id)
            c_dict = {
                "substance_id": c.substance_id,
                "unani_name": c.unani_name,
                "botanical_name": c.botanical_name,
                "role": c.role.value if hasattr(c.role, "value") else str(c.role),
                "parts": c.parts_by_weight,
                "percentage": c.percentage,
                "processing_method": c.processing_method,
                "is_schedule_e1": c.is_schedule_e1,
                "mudabbar_verified": c.mudabbar_verified,
                "mizaj": muf_rec.primary_mizaj if muf_rec else "",
                "plant_part": muf_rec.plant_part if muf_rec else "",
                "key_compounds": []
            }
            for cmp_id in c.key_marker_compounds:
                cmp_rec = CanonicalIdentityRegistry.get_compound(cmp_id)
                if cmp_rec:
                    cmp_info = {
                        "compound_id": cmp_rec.canonical_id,
                        "compound_name": cmp_rec.compound_name,
                        "molecular_weight": cmp_rec.molecular_weight,
                        "molecular_formula": cmp_rec.molecular_formula,
                        "smiles": cmp_rec.smiles,
                        "chembl_id": cmp_rec.chembl_id,
                        "bioavailability_score": cmp_rec.bioavailability_score
                    }
                    c_dict["key_compounds"].append(cmp_info)
                    if cmp_info not in all_compounds:
                        all_compounds.append(cmp_info)
            constituents_detail.append(c_dict)

        # 2. Resolve Targets & Pathways
        targets_detail = []
        for tgt_id in twin.resolved_targets:
            tgt_rec = CanonicalIdentityRegistry.get_target(tgt_id)
            if tgt_rec:
                targets_detail.append({
                    "target_id": tgt_rec.canonical_id,
                    "gene_symbol": tgt_rec.gene_symbol,
                    "protein_name": tgt_rec.protein_name,
                    "uniprot_id": tgt_rec.uniprot_id,
                    "chembl_target_id": tgt_rec.chembl_target_id,
                    "organ_systems": tgt_rec.organ_systems
                })

        pathways_detail = []
        for pw_id in twin.resolved_pathways:
            pw_rec = CanonicalIdentityRegistry.get_pathway(pw_id)
            if pw_rec:
                pathways_detail.append({
                    "pathway_id": pw_rec.canonical_id,
                    "pathway_name": pw_rec.pathway_name,
                    "reactome_id": pw_rec.reactome_id,
                    "kegg_id": pw_rec.kegg_id,
                    "category": pw_rec.category,
                    "description": pw_rec.description,
                    "associated_organ_axis": pw_rec.associated_organ_axis
                })

        # 3. Retrieve Evidence
        evidence_items = EvidenceBridgeEngine.get_evidence_for_entity(twin.formulation_id)
        highest_evidence = EvidenceBridgeEngine.get_highest_evidence_level(twin.formulation_id)

        # 4. Retrieve Production Batches
        batches = FormulationTwinRegistry.list_batches_for_formulation(twin.formulation_id)

        # 5. Retrieve Negative Knowledge & Contradictions
        contradictions = ScientificMemoryRegistry.check_for_contradictions(twin.canonical_name)

        return {
            "formulation_id": twin.formulation_id,
            "formula_version": twin.formula_version,
            "canonical_name": twin.canonical_name,
            "unani_category": twin.unani_category,
            "classical_indication": twin.classical_indication,
            "primary_mizaj_effect": twin.primary_mizaj_effect,
            "primary_organ_axis": twin.primary_organ_axis,
            "constituents": constituents_detail,
            "active_compounds": all_compounds,
            "targets": targets_detail,
            "pathways": pathways_detail,
            "synergy_pairs": twin.synergy_pairs,
            "fingerprint_markers": [asdict(m) for m in twin.fingerprint_markers],
            "production_batches": batches,
            "evidence_matrix": evidence_items,
            "highest_evidence_level": highest_evidence.value,
            "contraindications": twin.contraindications,
            "contradictions_registered": contradictions,
            "scientific_disclaimer": twin.scientific_disclaimer,
            "tamper_proof_hash": twin.tamper_proof_hash
        }

    @classmethod
    def evaluate_independent_safety(
        cls,
        formulation_id: str,
        patient_context: Dict[str, Any]
    ) -> SafetyEvaluationResult:
        """
        Independent Safety Engine (Non-negotiable Gate).
        Verdicts: PASS, CAUTION, BLOCK, UNKNOWN
        """
        twin = FormulationTwinRegistry.get_twin(formulation_id)
        if not twin:
            return SafetyEvaluationResult(
                verdict=SafetyVerdict.UNKNOWN,
                safety_score=0.0,
                risk_factors=["Formulation digital twin not found in registered catalog."],
                contraindications=["Unknown formulation identity."],
                schedule_e1_cleared=False,
                organ_clearance_ok=False,
                clinician_action_required="Verify formulation identity before clinical administration."
            )

        risk_factors: List[str] = []
        contraindications: List[str] = []
        schedule_e1_cleared = True
        organ_clearance_ok = True
        cyp_risk = "LOW"

        # 1. Schedule E(1) Mudabbar Gate
        has_e1 = any(c.is_schedule_e1 for c in twin.constituents)
        if has_e1:
            all_mudabbar = all(c.mudabbar_verified for c in twin.constituents if c.is_schedule_e1)
            if not all_mudabbar:
                schedule_e1_cleared = False
                contraindications.append(
                    "BLOCK: Schedule E(1) poisonous botanical (Suranjan) detected without certified Mudabbar detoxification."
                )

        # 2. Patient Pregnancy & Lactation Guard
        is_pregnant = patient_context.get("is_pregnant", False)
        is_lactating = patient_context.get("is_lactating", False)
        if (is_pregnant or is_lactating) and has_e1:
            contraindications.append(
                "BLOCK: Pregnancy / Lactation contraindicated for Colchicum alkaloids due to antimitotic & teratogenic toxicity."
            )

        # 3. Renal Clearance Guard (eGFR)
        egfr = patient_context.get("egfr", 90.0)
        if egfr < 30.0:
            organ_clearance_ok = False
            contraindications.append(
                f"BLOCK: Severe renal impairment / severe renal clearance failure (eGFR {egfr} mL/min/1.73m² < 30). Colchicine clearance is severely reduced, risking fatal systemic toxicity."
            )
        elif egfr < 60.0:
            risk_factors.append(
                f"Moderate renal impairment (eGFR {egfr} mL/min/1.73m²). Dose reduction by 50% recommended with therapeutic drug monitoring."
            )

        # 4. Hepatic Clearance Guard (ALT/AST)
        alt = patient_context.get("alt_u_l", 25.0)
        if alt > 150.0: # > 3x Upper Limit of Normal
            organ_clearance_ok = False
            contraindications.append(
                f"BLOCK: Acute severe hepatic elevation (ALT {alt} U/L > 3x ULN). Hepatic metabolism compromised."
            )
        elif alt > 70.0:
            risk_factors.append(f"Mild to moderate transaminitis (ALT {alt} U/L). Weekly LFT monitoring required.")

        # 5. Concurrent CYP3A4 / P-gp Inhibitors
        current_meds = [m.lower() for m in patient_context.get("current_medications", [])]
        potent_cyp3a4_inhibitors = ["clarithromycin", "ketoconazole", "itraconazole", "ritonavir", "verapamil"]
        if any(med in current_meds for med in potent_cyp3a4_inhibitors):
            cyp_risk = "HIGH"
            if has_e1:
                contraindications.append(
                    "BLOCK: Concurrent potent CYP3A4/P-gp inhibitor detected. Causes toxic accumulation of Colchicum alkaloids."
                )
            else:
                risk_factors.append("Concurrent CYP3A4 inhibitor detected. Monitor for altered bioavailability.")

        # Determine Verdict
        if contraindications or not schedule_e1_cleared or not organ_clearance_ok:
            verdict = SafetyVerdict.BLOCK
            safety_score = 0.15
            clinician_action = "PRESCRIPTION BLOCKED: Resolve critical safety contraindications prior to signing."
            rationale = "Severe toxicological or metabolic hazard identified. Non-negotiable safety guard triggered."
        elif risk_factors or cyp_risk != "LOW":
            verdict = SafetyVerdict.CAUTION
            safety_score = 0.72
            clinician_action = "CLINICIAN OVERRIDE REQUIRED: Acknowledge risk factors and adjust posology as advised."
            rationale = "Elevated risk profile detected requiring clinician vigilance and possible dose titration."
        else:
            verdict = SafetyVerdict.PASS
            safety_score = 0.98
            clinician_action = None
            rationale = "Patient parameters within safe physiological bounds. All Mudabbar purification standards certified."

        return SafetyEvaluationResult(
            verdict=verdict,
            safety_score=safety_score,
            risk_factors=risk_factors,
            contraindications=contraindications,
            schedule_e1_cleared=schedule_e1_cleared,
            organ_clearance_ok=organ_clearance_ok,
            cyp450_interaction_risk=cyp_risk,
            clinician_action_required=clinician_action,
            scientific_rationale=rationale
        )

    @classmethod
    def get_standard_intelligence_envelope(cls, formulation_id: str) -> Dict[str, Any]:
        twin = FormulationTwinRegistry.get_twin(formulation_id)
        if not twin:
            return {}
        summary = cls.get_formulation_intelligence_summary(formulation_id)
        evidence_matrix = EvidenceBridgeEngine.get_evidence_matrix_for_formulation(formulation_id)
        contradictions = ScientificMemoryRegistry.check_for_contradictions(twin.canonical_name)
        
        return {
            "request_id": f"req_{hashlib.sha256(formulation_id.encode()).hexdigest()[:8]}",
            "entity_id": twin.formulation_id,
            "entity_version": twin.formula_version,
            "execution_mode": "SHADOW_ADVISORY",
            "finding": {
                "type": "mechanistic_hypothesis",
                "statement": f"{twin.canonical_name} modulators target {', '.join([t['gene_symbol'] for t in summary.get('targets', [])[:3]])} along {summary.get('primary_organ_axis', '')} axis.",
            },
            "evidence": [e.to_dict() for e in evidence_matrix],
            "confidence": {
                "overall": None, # Non-collapsed multidimensional confidence per §12
                "dimensions": {
                    "traditional": "strong",
                    "chemical": "strong",
                    "target": "moderate",
                    "pathway": "moderate",
                    "exposure": "weak",
                    "safety": "moderate",
                    "human": "limited",
                    "combination": "unvalidated"
                }
            },
            "safety": {
                "state": "CAUTION" if twin.is_schedule_e1 else "PASS",
                "issues": twin.contraindications
            },
            "contradictions": contradictions,
            "unknowns": [
                "Full metabolomic synergistic interactome awaiting high-throughput organoid validation",
                "Longitudinal Phase IV real-world safety registry ongoing"
            ],
            "model": {
                "name": "ZFIE-MECH-001",
                "version": "0.4"
            },
            "knowledge": {
                "version": "zkb-2026.09"
            },
            "provenance": ["ChEMBL v33", "Reactome v85", "UPI Monographs Vol I-VI"],
            "clinical_action": {
                "requires_clinician_review": True,
                "autonomous_action_allowed": False
            }
        }

    @classmethod
    def get_why_this_drawer(cls, formulation_id: str) -> Dict[str, Any]:
        twin = FormulationTwinRegistry.get_twin(formulation_id)
        if not twin:
            return {}
        evidence_matrix = EvidenceBridgeEngine.get_evidence_matrix_for_formulation(formulation_id)
        return {
            "formulation_id": twin.formulation_id,
            "formula_version": twin.formula_version,
            "classical_sources": ["Al-Qanun fi al-Tibb (Avicenna)", "Kitab al-Hawi (Rhazes)", "NFUM Standardized Monographs"],
            "citations": [e.citation for e in evidence_matrix],
            "evidence_levels": [e.evidence_level.value for e in evidence_matrix],
            "knowledge_version": "zkb-2026.09",
            "model_version": "ZFIE-MECH-0.4",
            "limitations": "In-silico target affinities represent computational docking hypotheses (Level E0) and do not assert therapeutic efficacy without controlled human trial replication (Level E6).",
            "statutory_caveat": "ZAYVORA SCIENTIFIC NOTICE: Advisory clinical decision support only. Physician sign-off strictly required."
        }


# Ensure engines are initialized
FormulationTwinRegistry.initialize_seeds()
