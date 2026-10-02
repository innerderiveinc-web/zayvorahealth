"""
ZAYVORA Health OS™ — Canonical Safety Service
============================================
Reference:
  - Blueprint §10 (Safety Firewall - Risk Control)
  - Blueprint §24 (Sample Safety API contract)
  - Checks: identity, eligibility, contraindications, interactions, special populations, organ status, toxicity, regulatory, red flags
  - Contract Output: PASS | CAUTION | BLOCK | REFERRAL
"""

from typing import Dict, Any, List, Optional
import datetime

# High-risk / restricted botanical items
RESTRICTED_INGREDIENTS = {
    "SARPAGANDHA": {"schedule": "E1", "reason": "Schedule E(1) poisonous substance — Rx only; avoid in depression & hypotension"},
    "SURANJAN_TALKH": {"schedule": "E1", "reason": "Schedule E(1) poisonous substance — Colchicum luteum. Rx only; requires Shob-e-Tadbeer"},
    "AQARQARHA": {"schedule": "CONTROLLED", "reason": "4th degree Hot herb — strictly requires Tabasheer + Sandal Safaid and <=200mg/day limit"},
    "JATAMANSI": {"schedule": "CITES", "reason": "CITES Appendix II / WPA Schedule VI — cultivated source documentation required"},
    "KUSHTA_NOSHADER": {"schedule": "HEAVY_MINERAL", "reason": "Requires classical 40-day Tadbeer SOP and ICP-MS assay"}
}

# Special population contraindications
SPECIAL_POP_RESTRICTIONS = {
    "PREGNANCY": ["SURANJAN", "COLCHICUM", "ZAFRAN", "METHI", "GUGGUL", "ASGANDH", "AQARQARHA", "KUSHTA_QALAI"],
    "LACTATION": ["SURANJAN", "AQARQARHA", "KUSHTA_TAMBA"],
    "RENAL_IMPAIRMENT": ["SURANJAN", "KUSHTA_NOSHADER", "KUSHTA_TAMBA", "KUSHTA_HADEED"]
}


class CanonicalSafetyService:
    """Executes deterministic safety evaluations per Blueprint §24 contract."""

    @classmethod
    def evaluate(
        cls,
        patient_id: str,
        candidate_interventions: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        ctx = context or {}
        current_therapies = [t.upper() for t in ctx.get("current_therapies", [])]
        allergies = [a.upper() for a in ctx.get("allergies", [])]
        special_populations = [sp.upper() for sp in ctx.get("special_population", [])]

        evaluated_items = []
        overall_status = "PASS"
        source_refs = ["UPI-PART-1-VOL-VIII", "D&C-ACT-1940-RULE-161", "ZAY-SAFETY-DOCTRINE-2026"]

        for item_id in candidate_interventions:
            key = item_id.upper().replace("-", "_").replace(" ", "_")
            reasons = []
            item_status = "PASS"

            # 1. Check Allergies
            for allergy in allergies:
                if allergy in key or key in allergy:
                    reasons.append("PATIENT_ALLERGY_MATCH")
                    item_status = "BLOCK"

            # 2. Check Special Population Contraindications
            for sp in special_populations:
                restricted_list = SPECIAL_POP_RESTRICTIONS.get(sp, [])
                if any(r in key for r in restricted_list):
                    reasons.append(f"CONTRAINDICATION_{sp}")
                    item_status = "BLOCK"

            # 3. Check Scheduled Toxic / Restricted Ingredients
            for res_name, res_info in RESTRICTED_INGREDIENTS.items():
                if res_name in key:
                    reasons.append(f"SCHEDULE_{res_info['schedule']}_RESTRICTION")
                    if item_status != "BLOCK":
                        item_status = "CAUTION"

            # 4. Check Known Drug-Herb Interactions
            if "GUGGUL" in key and any("THYROXINE" in t or "WARFARIN" in t for t in current_therapies):
                reasons.append("INTERACTION_REVIEW_GUGGUL_DRUG")
                if item_status != "BLOCK":
                    item_status = "CAUTION"

            if "SARPAGANDHA" in key and any("ANTIHYPERTENSIVE" in t or "BETA_BLOCKER" in t for t in current_therapies):
                reasons.append("INTERACTION_REVIEW_HYPOTENSION_POTENTIATION")
                if item_status != "BLOCK":
                    item_status = "CAUTION"

            evaluated_items.append({
                "id": item_id,
                "status": item_status,
                "reason_codes": reasons
            })

            # Elevate overall decision
            if item_status == "BLOCK":
                overall_status = "BLOCK"
            elif item_status == "CAUTION" and overall_status != "BLOCK":
                overall_status = "CAUTION"

        return {
            "decision": overall_status,
            "patient_id": patient_id,
            "items": evaluated_items,
            "engine_version": "safety-1.4.0",
            "source_refs": source_refs,
            "evaluated_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
