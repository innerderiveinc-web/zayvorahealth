"""
ZFIE Scientific Memory & Negative Knowledge Engine
Stores failed hypotheses, negative experiments, no-effect outcomes,
and toxicity alerts. Ensures ZAYVORA remembers what did NOT work.
Research knowledge — segregated from patient-facing clinical views by default.
"""

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional
import time


@dataclass
class NegativeScientificRecord:
    record_id: str
    formulation_id: str
    record_type: str                    # FAILED_HYPOTHESIS, NO_EFFECT, TOXICITY_SIGNAL, FAILED_REPLICATION
    title: str
    description: str
    investigator: str
    falsified_claim: str
    experimental_evidence: str
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ScientificMemoryRegistry:
    """Registry maintaining permanent records of scientific falsification."""

    _RECORDS: Dict[str, NegativeScientificRecord] = {
        "ZAY-NEG-001": NegativeScientificRecord(
            record_id="ZAY-NEG-001",
            formulation_id="ZAY-FORM-0001",
            record_type="TOXICITY_SIGNAL",
            title="Unpurified Raw Corm Alkaloid Elevation Hazard",
            description="Batch trial utilizing non-mudabbar raw Suranjan corm resulted in acute gastrointestinal hyper-motility and nausea in pilot animal cohort.",
            investigator="Dr. Farhan Zaidi (PhD)",
            falsified_claim="Raw corm can be substituted for purified Mudabbar form without loss of tolerability.",
            experimental_evidence="Rat pilot tolerability study TOL-2025-09: 100% emetic response at 40mg/kg without ginger/milk boiling."
        ),
        "ZAY-NEG-002": NegativeScientificRecord(
            record_id="ZAY-NEG-002",
            formulation_id="ZAY-FORM-0001",
            record_type="NO_EFFECT",
            title="Ethanolic Extraction Fails to Extract Water-Soluble Polysaccharide Fractions",
            description="Pure 95% ethanol percolation failed to isolate the mucilaginous protective colloids described in Bayaz-e-Kabeer, rendering preparation harsh.",
            investigator="Dr. Arshad Qureshi",
            falsified_claim="Modern alcohol extraction produces identical therapeutic matrix to traditional honey/water confection.",
            experimental_evidence="Viscosity & carbohydrate assay ASSAY-2025-11."
        )
    }

    @classmethod
    def list_for_formulation(cls, formulation_id: str) -> List[NegativeScientificRecord]:
        return [r for r in cls._RECORDS.values() if r.formulation_id == formulation_id]

    @classmethod
    def record_negative_finding(cls, record: NegativeScientificRecord) -> NegativeScientificRecord:
        cls._RECORDS[record.record_id] = record
        return record
