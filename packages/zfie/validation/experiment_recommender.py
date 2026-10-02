"""
ZAYVORA Formulation Intelligence Engine™ (ZFIE)
Layer 5D: Next-Best Experiment Recommendation Engine
System: ZAYVORA Health OS™
Scoring Model: (Information Gain * Scientific Value * Uncertainty) / (Cost * Time * Technical Complexity)
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ExperimentRecommendation:
    recommendation_id: str
    hypothesis_id: str
    suggested_assay: str
    target_protein_or_cell_line: str
    expected_information_gain: float   # 0.0 to 1.0
    scientific_value: float            # 0.0 to 1.0 (Clinical relevance)
    uncertainty_level: float           # 0.0 to 1.0 (Higher uncertainty prioritizes experiment)
    estimated_cost_usd: float
    estimated_turnaround_days: int
    technical_feasibility: float       # 0.0 to 1.0
    composite_priority_score: float    # Ranked recommendation score
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ExperimentRecommendationEngine:
    """Ranks and recommends the optimal empirical assay to resolve maximal scientific uncertainty."""

    @classmethod
    def score_and_recommend(
        cls,
        hypothesis_id: str,
        target_name: str,
        proposed_assay: str,
        uncertainty: float = 0.85,
        scientific_value: float = 0.90,
        estimated_cost: float = 2500.0,
        turnaround_days: int = 14,
        feasibility: float = 0.92
    ) -> ExperimentRecommendation:
        """
        Calculates composite priority score:
        Score = (Info Gain * Scientific Value * Uncertainty * Feasibility) / log10(Cost * Turnaround)
        """
        info_gain = round(uncertainty * feasibility, 3)

        # Cost-time penalty factor
        penalty = max(1.0, (estimated_cost / 1000.0) * (turnaround_days / 7.0))
        numerator = info_gain * scientific_value * uncertainty * feasibility * 100.0
        priority_score = round(numerator / penalty, 2)

        rationale = (
            f"High uncertainty ({uncertainty:.2f}) on {target_name} provides maximum information gain ({info_gain:.2f}) "
            f"via {proposed_assay}. Feasibility is {feasibility*100:.0f}% with manageable cost (${estimated_cost:,.0f})."
        )

        return ExperimentRecommendation(
            recommendation_id=f"REC-{abs(hash(hypothesis_id)) % 100000:05d}",
            hypothesis_id=hypothesis_id,
            suggested_assay=proposed_assay,
            target_protein_or_cell_line=target_name,
            expected_information_gain=info_gain,
            scientific_value=scientific_value,
            uncertainty_level=uncertainty,
            estimated_cost_usd=estimated_cost,
            estimated_turnaround_days=turnaround_days,
            technical_feasibility=feasibility,
            composite_priority_score=priority_score,
            rationale=rationale
        )

    @classmethod
    def get_top_recommendations_for_formulation(cls, formulation_id: str) -> List[Dict[str, Any]]:
        """Returns the top prioritized experimental assays for a formulation."""
        recs = [
            cls.score_and_recommend(
                hypothesis_id="ZAY-HYP-001",
                target_name="Beta-tubulin (TUBB)",
                proposed_assay="In-vitro Tubulin Polymerization Fluorescence Kinetic Assay",
                uncertainty=0.75,
                scientific_value=0.95,
                estimated_cost=1800.0,
                turnaround_days=7,
                feasibility=0.96
            ),
            cls.score_and_recommend(
                hypothesis_id="ZAY-HYP-002",
                target_name="CYP3A4 / Intestinal P-gp",
                proposed_assay="Caco-2 Monolayer Bidirectional Permeability & Transport Assay",
                uncertainty=0.82,
                scientific_value=0.88,
                estimated_cost=3200.0,
                turnaround_days=14,
                feasibility=0.90
            ),
            cls.score_and_recommend(
                hypothesis_id="ZAY-HYP-003",
                target_name="NF-kB p65 Nuclear Translocation",
                proposed_assay="RAW 264.7 Macrophage LPS-Stimulated Western Blot & Dual-Luciferase",
                uncertainty=0.68,
                scientific_value=0.85,
                estimated_cost=2100.0,
                turnaround_days=10,
                feasibility=0.94
            )
        ]
        # Sort descending by composite score
        recs.sort(key=lambda r: r.composite_priority_score, reverse=True)
        return [r.to_dict() for r in recs]
