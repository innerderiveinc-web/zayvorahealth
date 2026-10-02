"""
ZAYVORA Health OS™ v5.0 — CYP450 Pharmacokinetic Drug-Herb Interaction Engine
==============================================================================
Evaluates molecular Phase I hepatic cytochrome P450 (CYP) metabolism and
Phase III efflux transporter (P-glycoprotein / ABCB1) pharmacokinetic conflicts
between botanical phytochemicals and modern allopathic medications.

Botanical Actives & Pharmacokinetic Vectors:
  - Piperine: Potent inhibitor of CYP3A4 and P-glycoprotein (increases Cmax of co-administered drugs).
  - Curcumin: Moderate inhibitor of CYP3A4, CYP2C9, and P-gp.
  - Guggulsterones: Activator of Pregnane X Receptor (PXR) -> induces CYP3A4 (accelerates drug clearance).
  - Berberine: Potent inhibitor of CYP2D6 and CYP3A4, alters intestinal P-gp.
  - Glycyrrhizin (Asl-us-Soos): Inhibits renal 11-beta-HSD2 (mineralocorticoid excess) and mild CYP3A4.
  - Withanolides (Asgandh): Mild GABAergic synergy with sedatives/benzodiazepines, thyroid T4 stimulation.

Classical Equivalence:
  Maps pharmacokinetic bio-accumulation / accelerated clearance to Unani
  'Tanafur-e-Advia' (mutual incompatibility) and 'Ibtal-e-Quwa' (annulment of medicinal efficacy).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


DRUG_METABOLIC_PATHWAYS = {
    "warfarin": {
        "class": "Anticoagulant",
        "primary_enzymes": ["CYP2C9", "CYP3A4"],
        "critical_risk": "Hemorrhage or loss of anticoagulation. INR instability.",
        "prohibited_herbs": ["guggul", "piperine", "curcumin", "ginger", "garlic", "zafran"]
    },
    "atorvastatin": {
        "class": "Statin (HMG-CoA Reductase Inhibitor)",
        "primary_enzymes": ["CYP3A4", "P-gp"],
        "critical_risk": "Elevated statin plasma concentrations -> Rhabdomyolysis / hepatotoxicity.",
        "prohibited_herbs": ["piperine > 15mg", "berberine > 1000mg"]
    },
    "simvastatin": {
        "class": "Statin (HMG-CoA Reductase Inhibitor)",
        "primary_enzymes": ["CYP3A4", "P-gp"],
        "critical_risk": "Significant Cmax surge -> Severe myopathy and myoglobinuria.",
        "prohibited_herbs": ["piperine > 10mg", "berberine"]
    },
    "levothyroxine": {
        "class": "Thyroid Hormone Replacement",
        "primary_enzymes": ["Intestinal Absorption / Hepatic Deiodinases"],
        "critical_risk": "Chelation and blocked intestinal absorption if taken concurrently with minerals or fiber.",
        "prohibited_herbs": ["calcium", "iron", "isabgol", "guggul concurrent"]
    },
    "metformin": {
        "class": "Biguanide Antidiabetic",
        "primary_enzymes": ["OCT1", "OCT2 Renal Transporters"],
        "critical_risk": "Additive hypoglycemia when combined with high-potency berberine without dose titration.",
        "prohibited_herbs": ["berberine > 1500mg"]
    },
    "amlodipine": {
        "class": "Dihydropyridine Calcium Channel Blocker",
        "primary_enzymes": ["CYP3A4"],
        "critical_risk": "Excessive vasodilation and orthostatic hypotension if CYP3A4 clearance is inhibited.",
        "prohibited_herbs": ["high_dose_piperine"]
    },
    "digoxin": {
        "class": "Cardiac Glycoside (Narrow Therapeutic Index)",
        "primary_enzymes": ["P-gp"],
        "critical_risk": "P-gp inhibition causes toxic digoxin accumulation -> Fatal ventricular arrhythmias.",
        "prohibited_herbs": ["piperine", "licorice", "berberine"]
    }
}

HERBAL_CYP_PROFILES = {
    "piperine": {
        "inhibits": ["CYP3A4", "P-gp", "CYP2C9"],
        "induces": [],
        "clinical_effect": "Increases systemic bioavailability of co-administered CYP3A4/P-gp substrates by up to 200-2,000%."
    },
    "curcumin": {
        "inhibits": ["CYP3A4", "CYP2C9", "P-gp"],
        "induces": [],
        "clinical_effect": "Inhibits platelet aggregation and delays clearance of CYP2C9 substrates."
    },
    "guggul": {
        "inhibits": [],
        "induces": ["CYP3A4", "PXR"],
        "clinical_effect": "Accelerates clearance of prescription drugs metabolized by CYP3A4, reducing efficacy."
    },
    "berberine": {
        "inhibits": ["CYP2D6", "CYP3A4", "CYP2C9"],
        "induces": [],
        "clinical_effect": "Inhibits multi-drug clearance and displays additive AMPK activation with Metformin."
    },
    "licorice": {
        "inhibits": ["11-beta-HSD2", "CYP3A4"],
        "induces": [],
        "clinical_effect": "Inhibits cortisol-cortisone breakdown, causing pseudoaldosteronism & potassium wasting."
    }
}


class CYP450InteractionEngine:
    """Evaluates CYP450 and P-gp mediated pharmacokinetic interactions."""

    @classmethod
    def evaluate_pharmacokinetic_risk(
        cls,
        current_allopathic_medications: List[str],
        candidate_herbs: List[str]
    ) -> Dict[str, Any]:
        conflicts = []
        cautions = []
        cyps_affected = set()
        highest_verdict = "PASS"

        meds_lower = [m.lower().strip() for m in current_allopathic_medications]
        herbs_lower = [h.lower().strip() for h in candidate_herbs]

        for med in meds_lower:
            for d_name, d_profile in DRUG_METABOLIC_PATHWAYS.items():
                if d_name in med:
                    for h in herbs_lower:
                        for p_herb in d_profile["prohibited_herbs"]:
                            clean_p = p_herb.split()[0]
                            if clean_p in h:
                                conflicts.append({
                                    "medication": med,
                                    "herb": h,
                                    "pathway": d_profile["primary_enzymes"],
                                    "severity": "CRITICAL_CONTRAINDICATION" if "warfarin" in d_name or "digoxin" in d_name else "SIGNIFICANT_CAUTION",
                                    "clinical_risk": d_profile["critical_risk"],
                                    "action_required": f"Do not combine {h} with {med}. Maintain a minimum 4-hour spacing or substitute herb."
                                })
                                highest_verdict = "BLOCK" if "warfarin" in d_name or "digoxin" in d_name else "CAUTION"

        # Check general enzyme inhibition
        for h in herbs_lower:
            for herb_key, profile in HERBAL_CYP_PROFILES.items():
                if herb_key in h:
                    cyps_affected.update(profile["inhibits"])
                    if profile["induces"]:
                        cyps_affected.update([f"{i} (Induction)" for i in profile["induces"]])

        return {
            "evaluation": highest_verdict,
            "conflicts_detected_count": len(conflicts),
            "conflicts": conflicts,
            "enzymes_and_transporters_modulated": sorted(list(cyps_affected)),
            "safe_to_administer_simultaneously": len(conflicts) == 0,
            "chrono_spacing_guideline": "When mild/moderate CYP competition exists, separate herbal doses by at least 3 hours from allopathic medications."
        }
