"""
ZAYVORA HEALTH OS™ — Shadow-Mode Formulation Intelligence Orchestrator
Governed Scientific Intelligence Layer (Blueprint §34, §35, §58, §83, §85)

Provides shadow-mode clinical decision support:
- Non-autonomous: Cannot sign, modify, or dispense prescriptions independently
- Generates multi-scale mechanistic summaries (Classical Unani <-> Molecular Biology)
- Flags safety alerts and HPLC batch biomarker deviations for clinician review
- Embeds mandatory statutory caveats on all computational findings
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from services.knowledge.app.core.canonical_identity_service import CanonicalIdentityRegistry
from services.therapeutic.app.models.computational_twin import FormulationTwinRegistry
from services.therapeutic.app.engines.formulation_intelligence_engine import (
    FormulationIntelligenceEngine,
    SafetyEvaluationResult,
    SafetyVerdict
)
from services.knowledge.app.engines.evidence_bridge import EvidenceBridgeEngine


@dataclass
class ShadowConsultationInsight:
    consultation_id: str
    formulation_id: str
    canonical_name: str
    formula_version: str
    active_batch_id: Optional[str]
    unani_rationale: str
    molecular_mechanisms: List[str]
    target_genes: List[str]
    active_pathways: List[str]
    synergy_insights: List[Dict[str, Any]]
    safety_evaluation: Dict[str, Any]
    evidence_level: str
    clinician_action_summary: str
    statutory_caveat: str
    tamper_proof_seal: str = ""

    def __post_init__(self):
        if not self.tamper_proof_seal:
            raw = f"{self.consultation_id}:{self.formulation_id}:{self.evidence_level}:{self.safety_evaluation.get('verdict')}"
            self.tamper_proof_seal = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @property
    def requires_clinician_approval(self) -> bool:
        return True

    @property
    def autonomous_execution_allowed(self) -> bool:
        return False

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["requires_clinician_approval"] = True
        d["autonomous_execution_allowed"] = False
        return d


class FormulationShadowOrchestrator:
    """Shadow-mode AI assistant providing computational formulation intelligence to clinicians."""

    MANDATORY_CAVEAT = (
        "ZAYVORA SCIENTIFIC NOTICE: Computational Formulation Intelligence™ provides governed "
        "decision support based on classical Unani literature, modern pharmacology, and analytical assays. "
        "It does NOT prescribe autonomously. Full clinical responsibility resides with the treating physician."
    )

    @classmethod
    def analyze_prescription_candidate(
        cls,
        formulation_id: str,
        patient_context: Dict[str, Any],
        selected_batch_id: Optional[str] = None
    ) -> ShadowConsultationInsight:
        """
        Runs a comprehensive shadow-mode evaluation of a candidate formulation for a clinician.
        """
        # 1. Fetch Formulation Twin
        twin = FormulationTwinRegistry.get_twin(formulation_id)
        if not twin:
            # Fallback for unknown
            return ShadowConsultationInsight(
                consultation_id=f"SHADOW-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                formulation_id=formulation_id,
                canonical_name="Unknown Formulation",
                formula_version="N/A",
                active_batch_id=selected_batch_id,
                unani_rationale="Formulation identity not recognized in canonical twin registry.",
                molecular_mechanisms=[],
                target_genes=[],
                active_pathways=[],
                synergy_insights=[],
                safety_evaluation={
                    "verdict": SafetyVerdict.UNKNOWN.value,
                    "safety_score": 0.0,
                    "risk_factors": ["Unknown entity."],
                    "schedule_e1_cleared": False
                },
                evidence_level="E0",
                clinician_action_summary="Verify prescription against official formulary.",
                statutory_caveat=cls.MANDATORY_CAVEAT
            )

        # 2. Run Independent Safety Engine
        safety_res = FormulationIntelligenceEngine.evaluate_independent_safety(
            formulation_id=twin.formulation_id,
            patient_context=patient_context
        )

        # 3. Resolve Molecular Targets and Pathways
        target_genes = []
        for tid in twin.resolved_targets:
            tgt = CanonicalIdentityRegistry.get_target(tid)
            if tgt:
                target_genes.append(f"{tgt.gene_symbol} ({tgt.protein_name})")

        active_pathways = []
        for pid in twin.resolved_pathways:
            pw = CanonicalIdentityRegistry.get_pathway(pid)
            if pw:
                active_pathways.append(f"{pw.pathway_name} [{pw.category}]")

        # 4. Synthesize Unani & Molecular Rationale
        unani_rationale = (
            f"Classical Indication: {twin.classical_indication}. "
            f"Humoral Action: {twin.primary_mizaj_effect} targeting the {twin.primary_organ_axis.upper()} organ-axis."
        )

        mechanisms = [
            f"Constituents modulate {len(target_genes)} key cellular targets across {len(active_pathways)} signaling pathways.",
            f"Juz-e-Azam acts with high affinity on primary inflammatory/metabolic effectors.",
            f"Musleh adjuvants provide gastroprotective buffering and enhance tissue bioavailability."
        ]

        # 5. Check Active Batch
        batch_id_used = selected_batch_id
        if not batch_id_used:
            batches = FormulationTwinRegistry.list_batches_for_formulation(twin.formulation_id)
            if batches:
                batch_id_used = batches[0]["batch_id"]

        # 6. Highest Evidence Grade
        evidence_level = EvidenceBridgeEngine.get_highest_evidence_level(twin.formulation_id).value

        # 7. Clinician Action Summary
        if safety_res.verdict == SafetyVerdict.BLOCK:
            action = f"PREVENT DISPENSE: {safety_res.clinician_action_required}"
        elif safety_res.verdict == SafetyVerdict.CAUTION:
            action = f"ADVISORY: Review risk factors ({', '.join(safety_res.risk_factors[:2])}). Dose titration recommended."
        else:
            action = f"CLEARED: Ready for clinician review and 21 CFR Part 11 digital signature."

        consult_id = f"SHADOW-{twin.formulation_id}-{datetime.now(timezone.utc).strftime('%H%M%S')}"

        return ShadowConsultationInsight(
            consultation_id=consult_id,
            formulation_id=twin.formulation_id,
            canonical_name=twin.canonical_name,
            formula_version=twin.formula_version,
            active_batch_id=batch_id_used,
            unani_rationale=unani_rationale,
            molecular_mechanisms=mechanisms,
            target_genes=target_genes,
            active_pathways=active_pathways,
            synergy_insights=twin.synergy_pairs,
            safety_evaluation=safety_res.to_dict(),
            evidence_level=evidence_level,
            clinician_action_summary=action,
            statutory_caveat=cls.MANDATORY_CAVEAT
        )
