"""
ZAYVORA Health OS™ - 90-Day Clinical Program Architecture & Value-Stacking Pricing
Reference: Master Clinical System (Part V), Dr. Irfan Ashraf, BUMS.

Implements:
  1. Three-Tier Care Programs (Basic, Advanced, Signature Elite)
  2. Value Stacking: Consultation gating, formula supply, lab mapping, dietary integration
  3. Program-specific pricing matrix across 7 flagship disease clusters
  4. Clinic revenue model calculations
"""

from typing import Dict, Any, List, Optional


PROGRAM_TIER_SPECS: Dict[str, Dict[str, Any]] = {
    "BASIC": {
        "tier_name": "Basic Program",
        "tier_code": "BASIC",
        "price_range_inr": [9500, 12000],
        "product_line": "Core Line Only",
        "formula_packs": "3 Months Supply (Standard Core Line)",
        "diet_plan": "Standardized Unani Mizaj PDF Chart",
        "follow_ups": "Weekly automated WhatsApp health support",
        "lab_support": "Self-directed (baseline review if provided)",
        "documentation": "Digital Health Tracking Sheet",
        "target_segment": "Mass premium / Early-stage prevention"
    },
    "ADVANCED": {
        "tier_name": "Advanced Program",
        "tier_code": "ADVANCED",
        "price_range_inr": [18000, 24000],
        "product_line": "Core Line + 1 Targeted Add-on Product",
        "formula_packs": "3 Months Supply + Phase-specific Support Kit",
        "diet_plan": "Personalized Functional Diet Plan based on Z-MAI",
        "follow_ups": "3 Scheduled Doctor Consultations (Day 0, Day 30, Day 90)",
        "lab_support": "Comprehensive Pre & Post Lab Review",
        "documentation": "Monthly Clinical Progress Reports",
        "target_segment": "Serious chronic illness patients needing structured guidance"
    },
    "SIGNATURE_ELITE": {
        "tier_name": "Signature Elite",
        "tier_code": "SIGNATURE_ELITE",
        "price_range_inr": [32000, 48000],
        "product_line": "Clinical Elite Line (High Density) + 2 Specialized Add-ons",
        "formula_packs": "Full Elite Line + 2 Targeted Add-on Modulators",
        "diet_plan": "Fully customized culinary medicine & glycemic protocol",
        "follow_ups": "Direct Doctor Access + Bi-weekly clinical check-ins",
        "lab_support": "Full Functional Biomarker 360 Mapping (Day 0, Day 45, Day 90)",
        "documentation": "Hardcover Printed Protocol Dossier & Digital Twin Archive",
        "target_segment": "Elite health transformation / Severe treatment-resistant cases"
    }
}

PROGRAM_SPECIFIC_PRICING: Dict[str, Dict[str, Any]] = {
    "FEMALE_FERTILITY": {
        "code": "FEMALE_FERTILITY",
        "program_title": "90-Day Female Fertility & Ovarian Restoration",
        "primary_axis": "Ovary (Mabaysim)",
        "pricing": {
            "BASIC": 12000,
            "ADVANCED": 22000,
            "SIGNATURE_ELITE": 42000
        },
        "biological_rationale": "Requires 3 full menstrual cycles for follicular recruitment and endometrial receptor restoration."
    },
    "MALE_FERTILITY": {
        "code": "MALE_FERTILITY",
        "program_title": "90-Day Male Fertility & Spermatogenic Rebuild",
        "primary_axis": "Testicular (Khusyatain)",
        "pricing": {
            "BASIC": 11000,
            "ADVANCED": 21000,
            "SIGNATURE_ELITE": 38000
        },
        "biological_rationale": "Human spermatogenesis cycle requires 74 days; clinical impact on morphology & DNA fragmentation manifests at 90-120 days."
    },
    "METABOLIC_RESET": {
        "code": "METABOLIC_RESET",
        "program_title": "90-Day Metabolic & Insulin Sensitivity Reset",
        "primary_axis": "Hepato-Metabolic (Jigar-Banas)",
        "pricing": {
            "BASIC": 10000,
            "ADVANCED": 20000,
            "SIGNATURE_ELITE": 35000
        },
        "biological_rationale": "12 weeks of liver de-steatosis and cellular insulin sensitisation required for verifiable HbA1c normalisation."
    },
    "PCOS_BALANCE": {
        "code": "PCOS_BALANCE",
        "program_title": "90-Day PCOS & Hormonal Rhythm Restoration",
        "primary_axis": "Insulin-Ovary Axis (Reham-Mabaysim)",
        "pricing": {
            "BASIC": 12000,
            "ADVANCED": 24000,
            "SIGNATURE_ELITE": 45000
        },
        "biological_rationale": "Reverses hyperinsulinemia-driven ovarian androgen excess across 3 consecutive ovulatory cycles."
    },
    "NEURO_CARDIAC": {
        "code": "NEURO_CARDIAC",
        "program_title": "90-Day Neuro-Cardiac & Autonomic Recovery",
        "primary_axis": "Neural-Cardiac (Dimagh-Qalb)",
        "pricing": {
            "BASIC": 9000,
            "ADVANCED": 18000,
            "SIGNATURE_ELITE": 32000
        },
        "biological_rationale": "Restores sympathetic-vagal autonomic balance and reduces sustained catecholamine endothelial injury."
    },
    "MALE_REBUILD": {
        "code": "MALE_REBUILD",
        "program_title": "90-Day Male Andropause & Vitality Rebuild",
        "primary_axis": "Hormone-Nerve-Adrenal",
        "pricing": {
            "BASIC": 12000,
            "ADVANCED": 25000,
            "SIGNATURE_ELITE": 48000
        },
        "biological_rationale": "Restores Leydig cell responsiveness and clears cortisol-mediated gonadotropin suppression."
    },
    "FEMALE_REBALANCE": {
        "code": "FEMALE_REBALANCE",
        "program_title": "90-Day Peri-Menopausal & Bone-Vitality Rebalance",
        "primary_axis": "Hormone-Mood-Liver",
        "pricing": {
            "BASIC": 12000,
            "ADVANCED": 24000,
            "SIGNATURE_ELITE": 45000
        },
        "biological_rationale": "Modulates estrogen decline via phytoestrogens and supports adrenal DHEA backup production."
    }
}


def get_program_pricing(program_code: str, tier: str) -> Optional[Dict[str, Any]]:
    """Calculates package breakdown, pricing, and deliverables for a patient."""
    p_data = PROGRAM_SPECIFIC_PRICING.get(program_code.upper())
    t_data = PROGRAM_TIER_SPECS.get(tier.upper())
    if not p_data or not t_data:
        return None

    price = p_data["pricing"].get(tier.upper(), 0)
    return {
        "program_code": program_code.upper(),
        "program_title": p_data["program_title"],
        "tier": tier.upper(),
        "tier_name": t_data["tier_name"],
        "price_inr": price,
        "product_line": t_data["product_line"],
        "formula_packs": t_data["formula_packs"],
        "diet_plan": t_data["diet_plan"],
        "consultations": t_data["follow_ups"],
        "lab_support": t_data["lab_support"],
        "documentation": t_data["documentation"],
        "biological_duration_days": 90,
        "biological_rationale": p_data["biological_rationale"]
    }


def calculate_clinic_revenue_projection(basic_count: int = 20, advanced_count: int = 15, signature_count: int = 5) -> Dict[str, Any]:
    """Projects monthly and annual revenue for a single or multi-clinic deployment."""
    monthly_basic = basic_count * 10000
    monthly_advanced = advanced_count * 22000
    monthly_signature = signature_count * 40000
    total_monthly = monthly_basic + monthly_advanced + monthly_signature
    total_annual = total_monthly * 12

    return {
        "monthly_breakdown": {
            "basic_revenue_inr": monthly_basic,
            "advanced_revenue_inr": monthly_advanced,
            "signature_revenue_inr": monthly_signature,
            "total_monthly_revenue_inr": total_monthly
        },
        "single_clinic_annual_inr": total_annual,
        "three_clinics_annual_inr": total_annual * 3,
        "projected_label": f"₹{round(total_annual / 100000, 1)} Lakhs (Single Clinic) / ₹{round((total_annual * 3) / 10000000, 2)} Crores (3 Clinics)"
    }
