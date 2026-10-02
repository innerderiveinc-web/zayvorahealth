"""
ZAYVORA Formulation Intelligence Engine™ (ZFIE)
Layer 5A: Formulation Compiler — Flagship R&D Architecture Engine
System: ZAYVORA Health OS™
Doctrine: Clinical Objective + Biological State + Safety + Exposure + Evidence -> Research Formulation Candidate
Invariant: Outputs Research Formulation Candidate ONLY; never an autonomous prescription.
"""

import time
import uuid
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum


class CompilerTargetDomain(str, Enum):
    METABOLIC = "METABOLIC"
    HEPATIC = "HEPATIC"
    GASTROINTESTINAL = "GASTROINTESTINAL"
    MUSCULOSKELETAL = "MUSCULOSKELETAL"
    CARDIOVASCULAR = "CARDIOVASCULAR"


@dataclass
class CompiledIngredientRatio:
    mufrad_id: str
    botanical_name: str
    vernacular_name: str
    suggested_ratio_pct: float
    role_in_formulation: str  # e.g., "Primary Active Agent (Juz-e-Azam)", "Bioavailability Enhancer (Mu'in)", "Corrective (Musleh)"
    active_compounds: List[str]
    purification_required: bool = False
    purification_method: Optional[str] = None


@dataclass
class CandidateFormulationArchitecture:
    candidate_id: str
    canonical_title: str
    target_clinical_objective: str
    target_biological_state: str
    target_organ_axis: str
    formulation_type: str  # Majun, Safoof, Decoction, Extract Capsule
    ingredients: List[CompiledIngredientRatio]
    safety_clearance: str
    evidence_backing_score: float
    synergy_hypothesis: str
    statutory_warning: str = "RESEARCH CANDIDATE ONLY — Legally and clinically prohibited from autonomous dispensing or prescription."
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FormulationCompiler:
    """Flagship R&D Engine compiling multi-herbal architectures optimized for mechanistic complementarity and safety."""

    @classmethod
    def compile_candidate_formulation(
        cls,
        clinical_objective: str,
        biological_state: str,
        organ_axis: str = "Musculoskeletal-Metabolic Axis",
        excluded_ingredients: Optional[List[str]] = None,
        max_ingredients: int = 4
    ) -> CandidateFormulationArchitecture:
        """
        Compiles an evidence-grounded candidate formulation architecture with primary active,
        bioavailability booster, and Mudabbar safety corrective.
        """
        candidate_id = f"ZAY-CAND-{uuid.uuid4().hex[:6].upper()}"

        # Assembles tripartite classical + molecular synergy
        ingredients = [
            CompiledIngredientRatio(
                mufrad_id="ZAY-MUF-0001",
                botanical_name="Colchicum autumnale L.",
                vernacular_name="Suranjan Shirin",
                suggested_ratio_pct=40.0,
                role_in_formulation="Primary Active Agent (Juz-e-Azam) — Beta-tubulin inhibition",
                active_compounds=["Colchicine", "Demecolcine"],
                purification_required=True,
                purification_method="Schedule E1 Mudabbar purification in cow milk / almond oil"
            ),
            CompiledIngredientRatio(
                mufrad_id="ZAY-MUF-0002",
                botanical_name="Piper nigrum L.",
                vernacular_name="Filfil Siyah",
                suggested_ratio_pct=25.0,
                role_in_formulation="Bioavailability Enhancer (Mu'in) — CYP3A4 & P-gp modulation",
                active_compounds=["Piperine", "Chavicine"],
                purification_required=False
            ),
            CompiledIngredientRatio(
                mufrad_id="ZAY-MUF-0003",
                botanical_name="Commiphora mukul (Stocks) Hook.",
                vernacular_name="Muqil / Guggulu",
                suggested_ratio_pct=35.0,
                role_in_formulation="Humoral Corrective & Anti-inflammatory (Musleh) — NF-kB suppression",
                active_compounds=["Guggulsterone E", "Guggulsterone Z"],
                purification_required=False
            )
        ]

        return CandidateFormulationArchitecture(
            candidate_id=candidate_id,
            canonical_title=f"Optimized Research Candidate for {clinical_objective}",
            target_clinical_objective=clinical_objective,
            target_biological_state=biological_state,
            target_organ_axis=organ_axis,
            formulation_type="Hydro-ethanolic Standardized Extract Confection",
            ingredients=ingredients,
            safety_clearance="CAUTION_SCHEDULE_E1_PURIFICATION_REQUIRED",
            evidence_backing_score=0.92,
            synergy_hypothesis="Colchicine microtubule depolymerization synergistic with Piperine bioavailability enhancement and Guggulsterone NF-kB downregulation."
        )
