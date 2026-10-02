"""
ZAYVORA Health OS™ - Clinical Decision Support (CDS) Extension
Reference: Book 2: ZAYVORA Clinical Handbook (Part IV, Chapters 1 & 2),
Author: Dr. Irfan Ashraf, BUMS.

Implements:
  1. Plateau Management Engine (detects 3+ weeks stagnation, suggests botanical rotation & compliance checks)
  2. Mixed Mizaj Resolution Engine (resolves multi-axis temperamental conflicts, e.g., Hot Liver / Cold Kidneys)
"""

from typing import Dict, Any, List, Optional


# Botanical rotation map for breaking receptor tolerance
HERB_ROTATION_MAP: Dict[str, Dict[str, Any]] = {
    "ASGANDH": {
        "primary_action": "Muqawwi-e-Aam, Cortisol reduction",
        "rotation_alternative": "BEHMAN_SAFAID",
        "alternative_name": "Behman Safaid (Centaurea behen)",
        "rationale": "Provides nervine and anabolic support with cooling-moistening quality, preventing excessive thermal buildup."
    },
    "GUGGUL": {
        "primary_action": "Muhallil, Lipid lowering, Thyroid deiodinase activation",
        "rotation_alternative": "METHI",
        "alternative_name": "Methi Dana (Trigonella foenum-graecum)",
        "rationale": "Maintains metabolic and insulin-sensitizing action without gastric heating."
    },
    "SHILAJIT": {
        "primary_action": "Mitochondrial ATP, fulvic delivery",
        "rotation_alternative": "SALAB_MISRI",
        "alternative_name": "Salab Misri (Orchis mascula)",
        "rationale": "Sustains tissue-nourishing Muwalid-e-Mani substrate without high mineral load."
    },
    "KASNI": {
        "primary_action": "Hepatoprotective, inulin prebiotic",
        "rotation_alternative": "MAKOH",
        "alternative_name": "Makoh (Solanum nigrum aerial)",
        "rationale": "Provides gentle hepatic decongestion and bile-thinning."
    },
    "GOKHRU": {
        "primary_action": "Diuretic, protodioscin nitric oxide release",
        "rotation_alternative": "PUNARNAVA",
        "alternative_name": "Punarnava (Boerhavia diffusa)",
        "rationale": "Provides renal filtration and microvascular support via neutral temperamental balance."
    }
}


class ClinicalDecisionSupportExt:
    """Advanced decision support engine for stalled cases and mixed temperaments."""

    @classmethod
    def evaluate_treatment_plateau(
        cls,
        weeks_on_protocol: int,
        reported_compliance_pct: float,
        subjective_improvement_pct: float,
        lab_markers_stagnant: bool,
        patient_frustration: bool = False,
        current_herbs: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluates whether a patient has entered a treatment plateau (Book 2 Ch 1)
        and outputs a systematic modification protocol.
        """
        is_plateau = (weeks_on_protocol >= 3) and (
            subjective_improvement_pct < 15.0 or lab_markers_stagnant or patient_frustration
        )

        if not is_plateau:
            return {
                "plateau_detected": False,
                "status": "PROTOCOL ON TRACK",
                "recommendation": "Continue current Afaal Cascade phase. Reassess at scheduled milestone."
            }

        # Generate 6-step modification protocol
        action_steps = [
            {
                "step": 1,
                "action": "Verify Compliance",
                "detail": f"Reported compliance is {reported_compliance_pct}%. Non-judgmentally review pill counts, dose timing, and dietary Parhez consistency."
            },
            {
                "step": 2,
                "action": "Screen for Hidden Stressors",
                "detail": "Audit sleep architecture (bedtime after 11 PM), acute occupational stress, or covert alcohol/sugar intake blocking hepatic response."
            },
            {
                "step": 3,
                "action": "Reassess Mizaj Drift",
                "detail": "Re-run Z-MAI assessment. Determine if initial treatment shifted constitutional balance (e.g. from Cold-Damp to excessive Dryness)."
            }
        ]

        # Check botanical rotation
        rotations = []
        if current_herbs:
            for herb in current_herbs:
                h_key = herb.upper().replace("-", "_").replace(" ", "_")
                for k, v in HERB_ROTATION_MAP.items():
                    if k in h_key:
                        rotations.append({
                            "current_herb": herb,
                            "switch_to": v["alternative_name"],
                            "rationale": v["rationale"]
                        })

        action_steps.append({
            "step": 4,
            "action": "Rotate Botanicals (Tolerance Break)",
            "detail": "Switch primary herbs to alternatives with identical Afaal to reset receptor sensitivity.",
            "suggested_rotations": rotations
        })

        action_steps.append({
            "step": 5,
            "action": "Add Catalytic Synergists (Tier 4)",
            "detail": "Introduce 5-10% bioavailability amplifiers (e.g., Piperine 5mg or Zanjabeel 500mg) to enhance tissue uptake."
        })

        action_steps.append({
            "step": 6,
            "action": "Consider Allopathic Co-Management",
            "detail": "If patient fails to progress after 4 weeks of modified regimen, initiate collaborative specialist evaluation."
        })

        return {
            "plateau_detected": True,
            "status": "PLATEAU DETECTED - PROTOCOL MODIFICATION REQUIRED",
            "weeks_on_protocol": weeks_on_protocol,
            "modification_protocol": action_steps,
            "suggested_rotations": rotations
        }

    @classmethod
    def resolve_mixed_mizaj_conflict(
        cls,
        organ_1: str,
        mizaj_1: str,
        organ_2: str,
        mizaj_2: str,
        primary_symptom: str
    ) -> Dict[str, Any]:
        """
        Resolves diametrically opposed organ temperaments (Book 2 Ch 2).
        Canonical example: Hot Liver (Safravi Jigar) + Cold Kidneys (Barid Kulya).
        """
        o1 = organ_1.upper()
        o2 = organ_2.upper()
        m1 = mizaj_1.upper()
        m2 = mizaj_2.upper()

        if ("LIVER" in o1 or "JIGAR" in o1) and ("HOT" in m1 or "SAFRAVI" in m1) and ("KIDNEY" in o2 or "KULYA" in o2) and ("COLD" in m2 or "BARID" in m2):
            return {
                "clinical_pattern": "Hot Liver / Cold Kidneys (Safravi Jigar with Barid Kulya)",
                "pathophysiology": "Hepatic inflammation and elevated enzymes alongside renal-genital weakness (low libido, edema, fatigue).",
                "sequenced_solution": [
                    {
                        "stage": "Stage A (Weeks 1-4): Cool and Clear the Liver First",
                        "herbs": ["Kutki (Picrorhiza kurroa) 500-1000mg", "Amla (Phyllanthus emblica) 1000-1500mg"],
                        "clinical_rule": "NEVER administer hot aphrodisiacs or potent kidney tonics while hepatic inflammation is active. Cool liver first."
                    },
                    {
                        "stage": "Stage B (Weeks 5-8): Introduce Gentle Kidney Tonics",
                        "herbs": ["Gokhru (Tribulus terrestris) 1500mg", "Shilajit Shuddha 300mg"],
                        "clinical_rule": "Avoid highly heating 3rd/4th degree agents like Aqarqarha or heavy hot spices."
                    },
                    {
                        "stage": "Stage C (Continuous): Neutral Bridge Modulator",
                        "herbs": ["Punarnava (Boerhavia diffusa) 1000mg"],
                        "clinical_rule": "Punarnava provides balanced diuresis and hepatoprotection without skewing heat or cold."
                    }
                ],
                "monitoring_rule": "Track ALT/AST at week 4. Only proceed to Stage B when liver enzymes stabilize."
            }

        # Generic opposing resolver
        return {
            "clinical_pattern": f"Mixed Constitutional Conflict: {organ_1} ({mizaj_1}) vs {organ_2} ({mizaj_2})",
            "pathophysiology": "Conflicting humoral demands require phased sequencing rather than simultaneous antagonistic compounding.",
            "sequenced_solution": [
                {
                    "stage": "Phase 1: Clear the dominant inflammatory or hot organ first (Tanqiya)",
                    "clinical_rule": "Address whichever organ presents with active heat, swelling, or acute laboratory deviation."
                },
                {
                    "stage": "Phase 2: Nourish the depleted or cold organ with neutral vehicle tonics",
                    "clinical_rule": "Introduce tonics with cooling Musleh correctives to protect the first organ."
                }
            ],
            "monitoring_rule": "Re-evaluate Mizaj every 21 days."
        }
