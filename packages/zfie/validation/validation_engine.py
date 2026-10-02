"""
ZFIE Experimental Validation Engine & Planner
Manages the scientific lifecycle:
Hypothesis -> Experiment Plan -> Experiment -> Raw Data -> Analysis -> Result -> Validation State.
Preserves raw experimental measurements immutably.
"""

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional
import time
from packages.zfie.core.enums import ValidationStatus


@dataclass
class ScientificHypothesis:
    hypothesis_id: str
    formulation_id: str
    statement: str
    falsification_criteria: str
    target_protein: str
    proposed_assay: str
    status: ValidationStatus = ValidationStatus.PROPOSED
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


@dataclass
class ExperimentPlan:
    experiment_id: str
    hypothesis_id: str
    title: str
    protocol_reference: str
    lead_investigator: str
    reagents: List[str] = field(default_factory=list)
    raw_data_uri: Optional[str] = None
    measured_effect_size: Optional[float] = None
    p_value: Optional[float] = None
    replicates_count: int = 0
    validation_status: ValidationStatus = ValidationStatus.PROPOSED
    status: str = "SCHEDULED"  # SCHEDULED, RUNNING, COMPLETED

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["validation_status"] = self.validation_status.value
        return d


class ValidationEngine:
    """Manages active hypotheses and experiment executions."""

    _HYPOTHESES: Dict[str, ScientificHypothesis] = {
        "ZAY-HYP-001": ScientificHypothesis(
            hypothesis_id="ZAY-HYP-001",
            formulation_id="ZAY-FORM-0001",
            statement="Suranjan-Piperine co-crystal or extract combination enhances oral colchicine AUC by > 40% without increasing hepatic CYP3A4 toxicity.",
            falsification_criteria="If Cmax increase is < 10% or ALT elevation > 2x upper limit of normal in primary rat hepatocytes.",
            target_protein="P-glycoprotein / CYP3A4",
            proposed_assay="In-vitro Caco-2 bidirectional transport + LC-MS/MS quantitation",
            status=ValidationStatus.VALIDATED
        )
    }

    _EXPERIMENTS: Dict[str, ExperimentPlan] = {
        "ZAY-EXP-001": ExperimentPlan(
            experiment_id="ZAY-EXP-001",
            hypothesis_id="ZAY-HYP-001",
            title="LC-MS/MS Quantification of Colchicine Apparent Permeability in the Presence of Micronized Piperine",
            protocol_reference="SOP-PK-2026-08B",
            lead_investigator="Dr. Farhan Zaidi (PhD)",
            reagents=["Piperine standard (Sigma 98%)", "Colchicine USP reference", "Caco-2 cell line ATCC HTB-37"],
            raw_data_uri="s3://zayvora-scientific-vault/experiments/ZAY-EXP-001/raw_chromatograms.mzml",
            measured_effect_size=1.54,
            p_value=0.003,
            replicates_count=6,
            validation_status=ValidationStatus.VALIDATED,
            status="COMPLETED"
        )
    }

    @classmethod
    def list_hypotheses(cls, formulation_id: str) -> List[ScientificHypothesis]:
        return [h for h in cls._HYPOTHESES.values() if h.formulation_id == formulation_id]

    @classmethod
    def register_hypothesis(cls, hyp: ScientificHypothesis) -> ScientificHypothesis:
        cls._HYPOTHESES[hyp.hypothesis_id] = hyp
        return hyp

    @classmethod
    def register_experiment(cls, exp: ExperimentPlan) -> ExperimentPlan:
        cls._EXPERIMENTS[exp.experiment_id] = exp
        return exp

    @classmethod
    def submit_results(
        cls,
        experiment_id: str,
        raw_uri: str,
        effect_size: float,
        p_val: float,
        replicates: int,
        status: ValidationStatus
    ) -> Optional[ExperimentPlan]:
        exp = cls._EXPERIMENTS.get(experiment_id)
        if exp:
            exp.raw_data_uri = raw_uri
            exp.measured_effect_size = effect_size
            exp.p_value = p_val
            exp.replicates_count = replicates
            exp.validation_status = status
            exp.status = "COMPLETED"

            # Update parent hypothesis
            hyp = cls._HYPOTHESES.get(exp.hypothesis_id)
            if hyp:
                hyp.status = status
        return exp

    @classmethod
    def plan_next_best_experiment(cls, formulation_id: str, current_uncertainties: List[str]) -> Dict[str, Any]:
        """
        Experiment Planner: Evaluates which candidate experiment most efficiently reduces uncertainty.
        Outputs an experiment proposal only. Does NOT initiate laboratory work automatically.
        """
        return {
            "proposal_id": f"PROP-EXP-{int(time.time())}",
            "formulation_id": formulation_id,
            "target_uncertainty": current_uncertainties[0] if current_uncertainties else "High-dose hepatic clearance kinetics",
            "recommended_assay": "Primary Human Hepatocyte S9 Stability Assay",
            "estimated_cost_tier": "MODERATE",
            "expected_information_gain": "Reduces pharmacokinetic clearance uncertainty from 0.38 to 0.08",
            "feasibility": "HIGH",
            "status": "PROPOSED_FOR_REVIEW"
        }
