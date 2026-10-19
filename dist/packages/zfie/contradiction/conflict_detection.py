"""
ZFIE Contradiction Engine
Treats contradictions as first-class scientific objects.
Never deletes or suppresses conflicting evidence.
"""

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional
from packages.zfie.core.enums import ContradictionStatus


@dataclass
class ContradictionObject:
    contradiction_id: str
    formulation_id: str
    claim_a: str
    source_a: str
    claim_b: str
    source_b: str
    methodological_differences: str
    dose_differences: str
    species_differences: str
    extraction_differences: str
    status: ContradictionStatus = ContradictionStatus.OPEN
    resolution_notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


class ContradictionRegistry:
    """Maintains active contradictions without silently dropping any conflicting study."""

    _CONTRADICTIONS: Dict[str, ContradictionObject] = {
        "ZAY-CONTRA-001": ContradictionObject(
            contradiction_id="ZAY-CONTRA-001",
            formulation_id="ZAY-FORM-0001",
            claim_a="Suranjan (Colchicum) promotes uric acid clearance rapidly in healthy volunteers.",
            source_a="Tibb-e-Unani Pharmacopoeia / J. Ethnopharmacol 2018 (aqueous extract 250mg)",
            claim_b="Colchicum extract exhibits negligible uricosuric action in hyperuricemic rodent models.",
            source_b="Biochem Pharmacol 2021 (methanolic crude extract 50mg/kg in Sprague-Dawley rats)",
            methodological_differences="In-vivo human healthy cohort vs Rodent chemically-induced hyperuricemia model.",
            dose_differences="Human therapeutic dose (250mg) vs Supraphysiological rodent dosage (50mg/kg).",
            species_differences="Homo sapiens renal organic anion transporters (hURAT1) differ from rodent rUrat1.",
            extraction_differences="Classical aqueous boiling extraction (Joshanda) vs 100% methanol laboratory extraction.",
            status=ContradictionStatus.EXPLAINED,
            resolution_notes="Discrepancy explained by interspecies differences in urate transporter kinetics and extraction solvent polarity."
        )
    }

    @classmethod
    def list_for_formulation(cls, formulation_id: str) -> List[ContradictionObject]:
        return [
            c for c in cls._CONTRADICTIONS.values()
            if c.formulation_id == formulation_id
        ]

    @classmethod
    def register_contradiction(cls, contra: ContradictionObject) -> ContradictionObject:
        cls._CONTRADICTIONS[contra.contradiction_id] = contra
        return contra

    @classmethod
    def update_status(cls, contra_id: str, new_status: ContradictionStatus, notes: str) -> Optional[ContradictionObject]:
        c = cls._CONTRADICTIONS.get(contra_id)
        if c:
            c.status = new_status
            c.resolution_notes = notes
        return c
