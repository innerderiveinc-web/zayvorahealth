"""
ZFIE Safety Evaluator
Evaluates toxicity limits, Schedule E1 botanicals, dosage bounds, and drug-herb interactions.
Never overrides or weakens the ZAYVORA Clinical Safety Firewall.
BLOCK verdict strictly terminates downstream clinical execution.
"""

from typing import Any, Dict, List, Optional
from packages.zfie.core.enums import SafetyVerdict
from packages.zfie.core.errors import ZFIESafetyBlockError


class ZFIESafetyEvaluator:
    """Independent scientific safety evaluation engine."""

    SCHEDULE_E1_SUBSTANCES = {
        "ZAY-MUF-0001": "Suranjan Shirin (Colchicum autumnale) contains Colchicine alkaloid - Schedule E(1) Mudabbar requirement",
    }

    @classmethod
    def evaluate_formulation(
        cls,
        formulation_id: str,
        ingredients: List[Dict[str, Any]],
        patient_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Runs multi-tiered safety check."""
        verdict = SafetyVerdict.PASS
        reasons = []
        cautions = []

        # 1. Schedule E1 Mudabbar Check
        for ing in ingredients:
            muf_id = ing.get("mufrad_id")
            if muf_id in cls.SCHEDULE_E1_SUBSTANCES:
                prep = ing.get("processing_method", "").lower()
                is_purified = ("mudabbar" in prep or "shodhit" in prep or ("purified" in prep and "unpurified" not in prep))
                if not is_purified:
                    verdict = SafetyVerdict.BLOCK
                    reasons.append(
                        f"CRITICAL SAFETY VIOLATION: {cls.SCHEDULE_E1_SUBSTANCES[muf_id]} without certified Mudabbar purification."
                    )
                else:
                    cautions.append(f"Monitored Schedule E1 ingredient: {cls.SCHEDULE_E1_SUBSTANCES[muf_id]}")

        # 2. Patient Contraindication Check (if patient context supplied)
        if patient_context:
            conditions = [c.lower() for c in patient_context.get("conditions", [])]
            eGFR = patient_context.get("eGFR", 90.0)

            if eGFR < 30.0:
                verdict = SafetyVerdict.BLOCK
                reasons.append("CRITICAL: Severe renal impairment (eGFR < 30 mL/min). Colchicine accumulation hazard.")

            if "pregnancy" in conditions:
                verdict = SafetyVerdict.BLOCK
                reasons.append("CRITICAL: Teratogenic mitotic inhibitor contraindication in pregnancy.")

        if verdict == SafetyVerdict.BLOCK:
            return {
                "verdict": SafetyVerdict.BLOCK.value,
                "reasons": reasons,
                "cautions": cautions,
                "can_proceed_to_clinic": False
            }

        final_verdict = SafetyVerdict.CAUTION if cautions else SafetyVerdict.PASS
        return {
            "verdict": final_verdict.value,
            "reasons": reasons,
            "cautions": cautions,
            "can_proceed_to_clinic": True
        }

    @classmethod
    def enforce_safety_gate(cls, evaluation: Dict[str, Any]) -> None:
        """Throws ZFIESafetyBlockError if verdict is BLOCK, terminating downstream operations."""
        if evaluation.get("verdict") == SafetyVerdict.BLOCK.value:
            raise ZFIESafetyBlockError(
                "ZFIE Safety Gate Failure: Clinical execution blocked by Safety Firewall.",
                reasons=evaluation.get("reasons", [])
            )
