"""
ZAYVORA Health OS™ - Dual-Tier Product Catalog & 80/20 Formulation Engine
Reference: Master Clinical System (Chapter 1 & 2) & Book 1 (Part VI),
Author: Dr. Irfan Ashraf, BUMS.

Codifies:
  1. Core Line (Mass Premium / Franchise) vs Clinical Elite Line (Doctor-supervised)
  2. 80/20 Formulation Architecture Verification (80% Unani Core + 20% Modern Precision)
  3. Dosing, density, capsule specifications, and regulatory pathways.
"""

from typing import Dict, Any, List, Optional


DUAL_TIER_CATALOG: Dict[str, Dict[str, Any]] = {
    "ZAY-PROD-01": {
        "sku": "ZAY-PROD-01",
        "name": "ZAYVORA Fertility+",
        "clinical_indication": "Female Infertility & Ovarian Priming",
        "primary_axis": "Ovary (Mabaysim)",
        "secondary_axis": "Liver + Stress",
        "program_duration_days": 90,
        "core_line": {
            "tier": "CORE",
            "capsule_fill_mg": 500,
            "dosing": "2 capsules twice daily",
            "mrp_inr": 1600,
            "cogs_inr": 520,
            "distribution": "Retail + Doctor",
            "extract_type": "Quality botanical extracts (10:1)",
            "mineral_forms": "Standard bioavailable minerals",
            "composition": [
                {"name": "Shatavari Extract", "amount_mg": 140, "category": "80% Core", "role": "Ovarian follicular nourishment"},
                {"name": "Lodhra Extract", "amount_mg": 80, "category": "80% Core", "role": "Uterine astringent & anti-inflammatory"},
                {"name": "Ashoka Extract", "amount_mg": 80, "category": "80% Core", "role": "Endometrial receptor sensitization"},
                {"name": "Behman Safaid", "amount_mg": 50, "category": "80% Core", "role": "Cardio-ovarian Muqawwi"},
                {"name": "Gaozaban Extract", "amount_mg": 50, "category": "80% Core", "role": "Mufarrih, neuroendocrine calming"},
                {"name": "Zinc (Chelated)", "amount_mg": 10, "category": "20% Precision", "role": "Enzyme cofactor for follicular maturation"},
                {"name": "Selenium", "amount_mcg": 40, "amount_mg": 0.04, "category": "20% Precision", "role": "Antioxidant protection"},
                {"name": "CoQ10", "amount_mg": 30, "category": "20% Precision", "role": "Mitochondrial oocyte ATP"},
                {"name": "Vitamin B6", "amount_mg": 5, "category": "20% Precision", "role": "Progesterone phase cofactor"}
            ],
            "unani_core_weight_mg": 400.0,
            "precision_weight_mg": 45.04,
            "unani_core_percentage": 89.87,
            "positioning": "Hormonal rhythm support + ovarian nourishment"
        },
        "elite_line": {
            "tier": "CLINICAL_ELITE",
            "capsule_fill_mg": 700,
            "dosing": "1 capsule twice daily",
            "mrp_inr": 3200,
            "cogs_inr": 1150,
            "distribution": "Doctor-Only Prescription",
            "extract_type": "Standardized extracts with HPLC marker verification",
            "mineral_forms": "Premium bisglycinate chelates & phytosomes",
            "composition": [
                {"name": "Shatavari Extract (40% saponins)", "amount_mg": 200, "category": "80% Core", "role": "High-potency follistimulation"},
                {"name": "Ashoka Extract (10% tannins)", "amount_mg": 120, "category": "80% Core", "role": "Selective estrogen receptor modulator"},
                {"name": "Lodhra Extract", "amount_mg": 100, "category": "80% Core", "role": "Pelvic anti-fibrinolytic & anti-inflammatory"},
                {"name": "Behman Safaid", "amount_mg": 80, "category": "80% Core", "role": "Endothelial nitric oxide support"},
                {"name": "Gaozaban Extract", "amount_mg": 80, "category": "80% Core", "role": "GLA neuroendocrine modulator"},
                {"name": "Zinc Bisglycinate", "amount_mg": 15, "category": "20% Precision", "role": "High-absorption sterol synthesis"},
                {"name": "Selenium (L-Selenomethionine)", "amount_mcg": 50, "amount_mg": 0.05, "category": "20% Precision", "role": "Glutathione peroxidase cofactor"},
                {"name": "CoQ10 (Ubiquinol form)", "amount_mg": 60, "category": "20% Precision", "role": "Active reduced mitochondrial electron donor"},
                {"name": "Myo-Inositol", "amount_mg": 150, "category": "20% Precision", "role": "Ovarian insulin sensitizer"},
                {"name": "Piperine", "amount_mg": 3, "category": "20% Precision", "role": "Bioavailability enhancer (2,000% cascade)"}
            ],
            "unani_core_weight_mg": 580.0,
            "precision_weight_mg": 228.05,
            "unani_core_percentage": 71.78,
            "positioning": "Clinical-grade ovarian support with enhanced bioavailability"
        }
    },
    "ZAY-PROD-02": {
        "sku": "ZAY-PROD-02",
        "name": "ZAYVORA TestoMax / NightOne",
        "clinical_indication": "Male Infertility, Low Testosterone & Andropause",
        "primary_axis": "Testicular (Khusyatain)",
        "secondary_axis": "Liver + Adrenal",
        "program_duration_days": 120,
        "core_line": {
            "tier": "CORE",
            "capsule_fill_mg": 550,
            "dosing": "2 capsules twice daily",
            "mrp_inr": 1750,
            "cogs_inr": 550,
            "distribution": "Retail + Doctor",
            "extract_type": "Standardized extracts",
            "mineral_forms": "Chelated zinc, purified shilajit",
            "composition": [
                {"name": "Asgandh (Withania somnifera)", "amount_mg": 150, "category": "80% Core", "role": "Cortisol reduction & LH support"},
                {"name": "Safed Musli (Chlorophytum borivilianum)", "amount_mg": 120, "category": "80% Core", "role": "Spermatogenic precursor"},
                {"name": "Kaunch Beej Shuddha", "amount_mg": 100, "category": "80% Core", "role": "Dopaminergic LH pulse stimulant"},
                {"name": "Gokhru (Tribulus terrestris)", "amount_mg": 80, "category": "80% Core", "role": "Protodioscin nitric oxide release"},
                {"name": "Shilajit Shuddha", "amount_mg": 40, "category": "20% Precision", "role": "Mitochondrial ATP & fulvic delivery"},
                {"name": "Zinc Monomethionine", "amount_mg": 12, "category": "20% Precision", "role": "Leydig cell testosterone synthesis"},
                {"name": "Selenium", "amount_mcg": 50, "amount_mg": 0.05, "category": "20% Precision", "role": "Sperm flagella motility structural protein"},
                {"name": "Piperine", "amount_mg": 2.5, "category": "20% Precision", "role": "Bioavailability enhancer"}
            ],
            "unani_core_weight_mg": 450.0,
            "precision_weight_mg": 54.55,
            "unani_core_percentage": 89.19,
            "positioning": "Endogenous testosterone and sperm motility support"
        },
        "elite_line": {
            "tier": "CLINICAL_ELITE",
            "capsule_fill_mg": 750,
            "dosing": "1 capsule twice daily",
            "mrp_inr": 3400,
            "cogs_inr": 1200,
            "distribution": "Doctor-Only Prescription",
            "extract_type": "High-density extracts (KSM-66, 40% protodioscin)",
            "mineral_forms": "Zinc Bisglycinate, Ubiquinol, L-Carnitine L-Tartrate",
            "composition": [
                {"name": "Asgandh KSM-66 (5% Withanolides)", "amount_mg": 200, "category": "80% Core", "role": "Testosterone +17% (RCT validated)"},
                {"name": "Safed Musli (30% saponins)", "amount_mg": 150, "category": "80% Core", "role": "Leydig receptor stimulation"},
                {"name": "Kaunch Beej Shuddha (L-DOPA >3.5%)", "amount_mg": 120, "category": "80% Core", "role": "Dopaminergic prolactin suppression"},
                {"name": "Salab Misri Extract", "amount_mg": 100, "category": "80% Core", "role": "Muwalid-e-Mani substrate"},
                {"name": "Shilajit (Fulvic >=60% ICP-MS)", "amount_mg": 50, "category": "20% Precision", "role": "Free testosterone enhancement"},
                {"name": "Zinc Bisglycinate", "amount_mg": 15, "category": "20% Precision", "role": "90% cellular absorption zinc"},
                {"name": "CoQ10 (Ubiquinol)", "amount_mg": 50, "category": "20% Precision", "role": "Mitochondrial triad (motility boost)"},
                {"name": "L-Carnitine L-Tartrate", "amount_mg": 60, "category": "20% Precision", "role": "Epididymal sperm energy shuttle"},
                {"name": "Piperine (95%)", "amount_mg": 5, "category": "20% Precision", "role": "Absorption amplifier"}
            ],
            "unani_core_weight_mg": 570.0,
            "precision_weight_mg": 180.0,
            "unani_core_percentage": 76.0,
            "positioning": "Clinical-grade spermatogenic regeneration for severe oligospermia"
        }
    },
    "ZAY-PROD-03": {
        "sku": "ZAY-PROD-03",
        "name": "ZAYVORA MetaReset / DiabEase",
        "clinical_indication": "Metabolic Syndrome, Type 2 Diabetes, Insulin Resistance",
        "primary_axis": "Insulin-Metabolic (Jigar-Banas)",
        "secondary_axis": "Liver + Thyroid",
        "program_duration_days": 90,
        "core_line": {
            "tier": "CORE",
            "capsule_fill_mg": 500,
            "dosing": "2 capsules twice daily before meals",
            "mrp_inr": 1400,
            "cogs_inr": 460,
            "distribution": "Retail + Doctor",
            "extract_type": "Standard aqueous/ethanolic extracts",
            "mineral_forms": "Chromium picolinate, Alpha Lipoic Acid",
            "composition": [
                {"name": "Gurmar (Gymnema sylvestre)", "amount_mg": 120, "category": "80% Core", "role": "Intestinal glucose absorption block"},
                {"name": "Jamun Beej (Syzygium cumini)", "amount_mg": 100, "category": "80% Core", "role": "Alpha-glucosidase inhibition"},
                {"name": "Karela (Momordica charantia)", "amount_mg": 80, "category": "80% Core", "role": "Polypeptide-P insulin mimetic"},
                {"name": "Methi Dana (Trigonella)", "amount_mg": 80, "category": "80% Core", "role": "4-OH-Isoleucine secretagogue"},
                {"name": "Daruhaldi (Berberis aristata)", "amount_mg": 60, "category": "80% Core", "role": "AMPK activation"},
                {"name": "Alpha Lipoic Acid", "amount_mg": 30, "category": "20% Precision", "role": "Insulin receptor antioxidant"},
                {"name": "Chromium Picolinate", "amount_mcg": 200, "amount_mg": 0.2, "category": "20% Precision", "role": "Glucose tolerance factor"},
                {"name": "Zinc Bisglycinate", "amount_mg": 10, "category": "20% Precision", "role": "Pancreatic beta cell insulin storage"}
            ],
            "unani_core_weight_mg": 440.0,
            "precision_weight_mg": 40.2,
            "unani_core_percentage": 91.63,
            "positioning": "Postprandial glycemic stabilization & glucose uptake"
        },
        "elite_line": {
            "tier": "CLINICAL_ELITE",
            "capsule_fill_mg": 700,
            "dosing": "1 capsule twice daily",
            "mrp_inr": 2900,
            "cogs_inr": 1050,
            "distribution": "Doctor-Only Prescription",
            "extract_type": "Standardized marker extracts (25% gymnemic acids, 20% ellagic)",
            "mineral_forms": "Berberine phytosome, R-ALA, Vanadyl sulfate",
            "composition": [
                {"name": "Gurmar Extract (25% Gymnemic acids)", "amount_mg": 160, "category": "80% Core", "role": "Beta-cell regenerative signalling"},
                {"name": "Tukhm Jamun (20% Ellagic acid)", "amount_mg": 140, "category": "80% Core", "role": "Hepatic gluconeogenesis suppression"},
                {"name": "Daruhaldi Extract (Berberis aristata)", "amount_mg": 120, "category": "80% Core", "role": "AMPK phosphorylation & GLUT4"},
                {"name": "Karela (1% Bitter peptides)", "amount_mg": 100, "category": "80% Core", "role": "Peripheral insulin sensitivity"},
                {"name": "R-Alpha Lipoic Acid", "amount_mg": 60, "category": "20% Precision", "role": "Endothelial & mitochondrial protection"},
                {"name": "Myo-Inositol", "amount_mg": 100, "category": "20% Precision", "role": "Inositol second messenger activation"},
                {"name": "Chromium Picolinate", "amount_mcg": 400, "amount_mg": 0.4, "category": "20% Precision", "role": "Chromodulin insulin amplification"},
                {"name": "Piperine (95%)", "amount_mg": 5, "category": "20% Precision", "role": "Bioavailability enhancer"}
            ],
            "unani_core_weight_mg": 520.0,
            "precision_weight_mg": 165.4,
            "unani_core_percentage": 75.87,
            "positioning": "Clinical reversal protocol for severe insulin resistance and HOMA-IR >3.5"
        }
    }
}


def get_dual_tier_product(sku: str) -> Optional[Dict[str, Any]]:
    """Retrieves dual-tier product data by SKU."""
    return DUAL_TIER_CATALOG.get(sku.upper())


def get_all_dual_tier_products() -> List[Dict[str, Any]]:
    """Returns all cataloged dual-tier products."""
    return list(DUAL_TIER_CATALOG.values())


def validate_80_20_compliance(formula_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validates that any ZAYVORA formulation satisfies the rigid 80-20 principle:
      - At least 70-80% Unani Core herbs
      - No more than 20-30% Modern Precision Bioactives
      - Modern ingredients CANNOT be the dominant hero ingredient
    """
    total_weight = sum(float(item.get("amount_mg", 1.0)) for item in formula_items)
    if total_weight == 0:
        return {"compliant": False, "reason": "Formula has 0 total weight."}

    unani_weight = sum(float(item.get("amount_mg", 0.0)) for item in formula_items if "Core" in item.get("category", ""))
    precision_weight = sum(float(item.get("amount_mg", 0.0)) for item in formula_items if "Precision" in item.get("category", ""))

    unani_pct = round((unani_weight / total_weight) * 100.0, 2)
    precision_pct = round((precision_weight / total_weight) * 100.0, 2)

    # Check that highest single ingredient is not a modern nutraceutical overriding Unani herbs
    sorted_items = sorted(formula_items, key=lambda x: float(x.get("amount_mg", 0.0)), reverse=True)
    top_ingredient = sorted_items[0] if sorted_items else {}
    is_hero_modern = "Precision" in top_ingredient.get("category", "")

    compliant = unani_pct >= 70.0 and not is_hero_modern

    return {
        "compliant": compliant,
        "unani_core_percentage": unani_pct,
        "precision_percentage": precision_pct,
        "top_ingredient": top_ingredient.get("name", "N/A"),
        "hero_ingredient_category": top_ingredient.get("category", "N/A"),
        "violation": "Modern ingredient dominates or Unani core <70%" if not compliant else None
    }
