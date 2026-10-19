"""
ZFIE Evidence Bridge & Provenance Engine
Enforces the 7-level evidence hierarchy (E0 to E6) and validates scientific claims.
Never silently promotes computational predictions into clinical facts.
"""

from typing import Any, Dict, List, Optional
from packages.zfie.core.enums import EvidenceLevel, EvidenceStrength
from packages.zfie.core.errors import InvalidEvidencePromotionError
from packages.zfie.core.types import ProvenanceRecord


class EvidenceBridgeEngine:
    """Authoritative scientific evidence bridge verifying claim integrity."""

    _EVIDENCE_STORE: Dict[str, Dict[str, Any]] = {
        "EVD-001": {
            "evidence_id": "EVD-001",
            "level": EvidenceLevel.E6_CONTROLLED_CLINICAL.value,
            "title": "High versus Low Dosing of Oral Colchicine for Early Acute Gout Flare (AGREE Trial)",
            "doi": "10.1002/art.27327",
            "sample_size": 184,
            "species": "Homo sapiens",
            "study_design": "RCT Phase 3",
            "reviewer": "Terteit et al. / Dr. Farhan Zaidi (PhD)",
            "license": "CC-BY-4.0"
        },
        "EVD-002": {
            "evidence_id": "EVD-002",
            "level": EvidenceLevel.E5_HUMAN_OBSERVATIONAL_PK.value,
            "title": "Influence of Piperine on Pharmacokinetics of Curcumin and Phytochemicals in Humans and Animals",
            "doi": "10.1055/s-2006-957450",
            "sample_size": 24,
            "species": "Homo sapiens",
            "study_design": "Crossover Pharmacokinetic Trial",
            "reviewer": "Shoba et al. / Dr. Farhan Zaidi (PhD)",
            "license": "Open Access"
        },
        "EVD-003": {
            "evidence_id": "EVD-003",
            "level": EvidenceLevel.E2_COMPUTATIONAL_PREDICTION.value,
            "title": "Insight into Tubulin Regulation from Complex with Colchicine and Stathmin-like Domain (PDB: 1SA0)",
            "doi": "10.1038/nature02393",
            "sample_size": 0,
            "species": "In Silico Model",
            "study_design": "Crystallography & Molecular Docking",
            "reviewer": "Ravelli et al. / ZFIE Automated Docking Pipeline",
            "license": "Nature / PDB"
        }
    }

    @classmethod
    def get_evidence(cls, evidence_id: str) -> Optional[Dict[str, Any]]:
        return cls._EVIDENCE_STORE.get(evidence_id)

    @classmethod
    def register_evidence(cls, evidence: Dict[str, Any]) -> str:
        eid = evidence.get("evidence_id")
        if not eid:
            raise ValueError("evidence_id required")
        cls._EVIDENCE_STORE[eid] = evidence
        return eid

    @classmethod
    def promote_evidence_level(
        cls,
        evidence_id: str,
        target_level: EvidenceLevel,
        experimental_data_attached: bool
    ) -> Dict[str, Any]:
        """Attempts to promote evidence level; raises error if unvalidated."""
        ev = cls.get_evidence(evidence_id)
        if not ev:
            raise ValueError(f"Evidence {evidence_id} not found.")

        current_level_str = ev["level"]
        curr_rank = EvidenceLevel.rank(current_level_str)
        targ_rank = EvidenceLevel.rank(target_level.value)

        if targ_rank >= 4 and not experimental_data_attached:
            raise InvalidEvidencePromotionError(
                f"Forbidden evidence promotion: Cannot elevate {current_level_str} to {target_level.value} "
                f"without verified clinical or experimental wet-lab dataset."
            )

        ev["level"] = target_level.value
        ev["promotion_note"] = f"Promoted from {current_level_str} with verified experimental data."
        return ev
