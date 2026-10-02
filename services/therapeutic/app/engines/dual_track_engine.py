"""
ZAYVORA Health OS™ — Dual-Track Delivery Engine (Track 1 Matab vs Track 2 GMP)
Source: Dr. Irfan Ashraf — CP-AFUM Textbook Chapter 5 & The Organ-Axis Clinical System (Chapter 13)
Encodes:
- Track 1 (Matab Custom Nuskha Compounding): Individualized, complex multi-axis, Grade 3 depletion
- Track 2 (Standardized GMP Hero Capsules): Scale, telemedicine, single/dual axis, maintenance
- The 6 ZAYVORA Core GMP Products & their standardized active matrices
- The Matab Nuskha Base Batch recipes
"""
from typing import Dict, Any, List, Optional

GMP_PRODUCTS_MASTER = {
    "LiverPrime Core": {
        "sku": "ZV-G-01",
        "axis": "Gut-Liver",
        "phase_use": "Phase 1: Mandatory ALL cases; Phase 2: 50% maintenance; Phase 3: taper",
        "standardized_actives": [
            {"name": "Silymarin", "spec": "70-80% standardized extract", "dose": "140mg TID"},
            {"name": "NAC (N-Acetylcysteine)", "spec": "Pure grade", "dose": "600mg/day"},
            {"name": "Phosphatidylcholine", "spec": "Lipid-active", "dose": "Standard therapeutic"},
            {"name": "Artichoke extract", "spec": "Cynarin standardized", "dose": "320mg/day"}
        ],
        "monitoring": "SGPT (ALT), hs-CRP every 4 weeks in Phase 1"
    },
    "MetaboCore Elite": {
        "sku": "ZV-M-02",
        "axis": "Liver-Pancreas",
        "phase_use": "Phase 2 hero: T2DM / Metabolic Syndrome / PCOS-IR; Phase 3: 50% dose",
        "standardized_actives": [
            {"name": "Berberine HCl", "spec": "≥95% standardized (plant metformin)", "dose": "500mg BID Wk1 -> 1000mg BID Wk2+"},
            {"name": "Alpha-Lipoic Acid (R-form)", "spec": "Mitochondrial antioxidant", "dose": "600mg/day"},
            {"name": "Chromium Picolinate", "spec": "Insulin receptor cofactor", "dose": "400mcg/day"},
            {"name": "Fenugreek extract", "spec": "40% saponins / 4-HI", "dose": "Standard therapeutic"}
        ],
        "monitoring": "HbA1c (12-weekly), Fasting Insulin (8-weekly), TG/HDL ratio"
    },
    "OvaSync": {
        "sku": "ZV-F-01",
        "axis": "Gut-Ovarian",
        "phase_use": "Phase 2 hero: PCOS / anovulatory infertility; Phase 3: maintenance",
        "standardized_actives": [
            {"name": "Myo-Inositol + D-Chiro-Inositol", "spec": "40:1 physiological ratio", "dose": "MI 2g + DCI 50mg BID"},
            {"name": "Vitex agnus-castus", "spec": "Dopaminergic LH-modulating", "dose": "Standard extract"},
            {"name": "Shatavari extract", "spec": "5:1 extract (Shatavarins)", "dose": "Cooling uterine tonic"},
            {"name": "Folic Acid / 5-MTHF", "spec": "Active methylfolate", "dose": "400-800mcg/day"}
        ],
        "monitoring": "AMH trend (12-weekly), LH:FSH ratio (8-weekly), Menstrual cycle regularity"
    },
    "ManiVital Pro": {
        "sku": "ZV-M-01",
        "axis": "Liver-Testicular",
        "phase_use": "Phase 2 hero: male factor infertility / oligospermia; Phase 3: 50% dose",
        "standardized_actives": [
            {"name": "Ashwagandha (KSM-66)", "spec": "≥5% Withanolides (HPLC)", "dose": "300mg BD"},
            {"name": "CoQ10 (Ubiquinol)", "spec": "Mitochondrial ATP flagellar motor", "dose": "200-300mg/day"},
            {"name": "Zinc Bisglycinate", "spec": "Sertoli cell structural cofactor", "dose": "30mg elemental/day"},
            {"name": "Selenium (L-Selenomethionine)", "spec": "GPx4 sperm membrane protector", "dose": "200mcg/day"},
            {"name": "L-Carnitine + Acetyl-L-Carnitine", "spec": "Sperm motility beta-oxidation", "dose": "1500mg/day total"}
        ],
        "monitoring": "Semen Analysis at 12 weeks (full 72-74 day spermatogenesis cycle)"
    },
    "ThyroMet Axis": {
        "sku": "ZV-T-01",
        "axis": "Thyroid-Neuro",
        "phase_use": "Phase 2 hero: hypothyroid / low T3 conversion failure; Phase 3: 50% dose",
        "standardized_actives": [
            {"name": "Selenium (L-Selenomethionine)", "spec": "Rate-limiting deiodinase cofactor", "dose": "200mcg/day"},
            {"name": "Zinc Bisglycinate", "spec": "T3 nuclear binding cofactor", "dose": "30mg/day"},
            {"name": "Guggulsterones (E+Z)", "spec": "2.5% HPLC / FXR antagonist", "dose": "Standardized extract"},
            {"name": "Ashwagandha", "spec": "HPA cortisol normalizer", "dose": "300mg bedtime"},
            {"name": "L-Tyrosine", "spec": "Substrate for T4 synthesis", "dose": "500mg fasting"}
        ],
        "monitoring": "TSH + Free T3 at 8 weeks (TSH lags 6-8 weeks); Anti-TPO at 12 weeks"
    },
    "NeuroCalmX": {
        "sku": "ZV-N-01",
        "axis": "HPA Axis",
        "phase_use": "Phase 1: HPA-compromised cases; Phase 2 hero: anxiety / burnout; Phase 3: 50% dose",
        "standardized_actives": [
            {"name": "Valerian root extract", "spec": "0.8% Valerenic acid (GABA-A agonist)", "dose": "Standard night dose"},
            {"name": "L-Theanine", "spec": "Alpha-wave promoter", "dose": "200mg before bed"},
            {"name": "Magnesium Glycinate", "spec": "NMDA receptor antagonist", "dose": "400mg at night"},
            {"name": "Ashwagandha (KSM-66)", "spec": "Bidirectional cortisol normalizer", "dose": "300mg"}
        ],
        "monitoring": "Cortisol AM/PM at 8 weeks; PHQ-9 and GAD-7 at 4 and 8 weeks"
    }
}


def evaluate_clinical_delivery_track(
    is_remote: bool,
    active_axes_count: int,
    quwwat_grade: int,
    patient_prefers_convenience: bool
) -> Dict[str, Any]:
    """
    Determines whether Track 1 (Matab Nuskha) or Track 2 (GMP Capsules) is indicated
    based on the Chapter 13 Decision Framework.
    """
    if quwwat_grade >= 3:
        return {
            "recommended_track": "TRACK 1 (Matab Custom Nuskha)",
            "mandatory": True,
            "rationale": "Grade 3 critical organ depletion requires high therapeutic density (5-10g/day) and bespoke compounding under direct Hakim supervision.",
            "delivery_mode": "In-clinic Matab compounding with weekly or bi-weekly reviews."
        }
    
    if active_axes_count >= 3:
        return {
            "recommended_track": "TRACK 1 (Matab Custom Nuskha)",
            "mandatory": True,
            "rationale": "Complex multi-axis presentation (3+ dysfunctional axes) requires individualized thermal calibration beyond fixed GMP capsule architecture.",
            "delivery_mode": "Bespoke Nuskha compounding with GMP micronutrient co-administration."
        }

    if is_remote or patient_prefers_convenience:
        return {
            "recommended_track": "TRACK 2 (Standardized GMP Hero Capsules)",
            "mandatory": False,
            "rationale": "Remote / telemedicine patient or preference for travel-friendly, fixed-dose standardized capsules with documented stability.",
            "delivery_mode": "Direct dispatch of WHO-GMP certified bottles with digital monitoring protocol."
        }

    return {
        "recommended_track": "HYBRID DUAL-TRACK (Matab Acute + GMP Maintenance)",
        "mandatory": False,
        "rationale": "Track 1 custom Nuskha in acute Phase 1-2 for rapid clinical response, transitioning to Track 2 GMP capsules for Phase 3 consolidation.",
        "delivery_mode": "Matab Nuskha 5g BD + Track 2 complementary micronutrient capsules."
    }
