#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Complete Patient Clinical Continuum Simulation
===================================================================
Executes a full end-to-end patient encounter across all 6 converged publications:
  1. Patient Intake & Chief Complaints
  2. Z-MAI 6-Domain Quantitative Scoring Matrix & Dosage Form Selection
  3. Closed-Loop Biomarker Confirmation Algorithm
  4. Red-Flag Emergency Guard & 12-Axis Scoring
  5. Symphonic 4-Tier Polypharmacy Formulation & Safety Audit (Behman + Aqarqarha)
  6. 90-Day Clinical Program Stacking, Parhez Assignment & Prescription Generation
"""

import json
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.knowledge.app.data.zmai_scoring_tool import calculate_mizaj_2_matrix, MIZAJ_2_DOMAINS
from services.clinical.app.engines.functional_lab_engine import (
    calculate_homa_ir,
    verify_humoral_biomarker_correlation,
    evaluate_five_non_negotiable_lab_trigger_rules
)
from services.clinical.app.engines.emergency_red_flag_guard import EmergencyRedFlagGuard
from services.therapeutic.app.engines.formula_safety_checker import FormulaSafetyChecker
from services.knowledge.app.data.dual_tier_product_catalog import get_dual_tier_product
from services.knowledge.app.data.program_packages_pricing import get_program_pricing
from services.clinical.app.engines.udc_engine import generate_udc

def run_simulation():
    print("=" * 78)
    print(" ZAYVORA HEALTH OS™ — PRECISION UNANI CLINICAL CONTINUUM SIMULATION")
    print(" Reference: Foundations, Framework & Pharmacopoeia (Dr. Irfan Ashraf, BUMS)")
    print("=" * 78)

    # -------------------------------------------------------------------------
    # 1. Patient Intake & Chief Complaints
    # -------------------------------------------------------------------------
    patient = {
        "mrn": "MRN-2026-TARIQ",
        "name": "Tariq Mahmood",
        "age": 38,
        "gender": "Male",
        "weight_kg": 92.5,
        "height_cm": 176,
        "chief_complaints": [
            "Severe mid-day fatigue and sluggishness",
            "Weight gain of 14 kg over 24 months (visceral)",
            "Low libido and morning erectile softening",
            "Cold hands and feet with heavy unrefreshing sleep"
        ]
    }
    print(f"\n[1] PATIENT INTAKE RECORD: {patient['name']} (Age: {patient['age']} | BMI: {round(patient['weight_kg'] / ((patient['height_cm']/100)**2), 1)})")
    for cc in patient["chief_complaints"]:
        print(f"    • {cc}")

    # -------------------------------------------------------------------------
    # 2. Z-MAI 6-Domain Quantitative Scoring Matrix (Part One Ch 9)
    # -------------------------------------------------------------------------
    print("\n[2] Z-MAI 6-DOMAIN QUANTITATIVE MIZAJ MATRIX EVALUATION:")
    domain_scores = {
        "body_build_weight": {"balgham": 3, "safra": 0, "sauda": 0, "dam": 1},
        "skin_complexion": {"balgham": 3, "safra": 0, "sauda": 0, "dam": 0},
        "psychological_profile": {"balgham": 2, "safra": 1, "sauda": 0, "dam": 1},
        "digestion_appetite": {"balgham": 3, "safra": 0, "sauda": 1, "dam": 0},
        "sleep_quality": {"balgham": 3, "safra": 0, "sauda": 0, "dam": 1},
        "tongue_pulse": {"balgham": 3, "safra": 0, "sauda": 1, "dam": 0}
    }
    zmai_eval = calculate_mizaj_2_matrix(domain_scores)
    scores = zmai_eval["mizaj_scores"]
    print(f"    Humor Scores (Max 18): Balgham={scores['balgham']}, Safra={scores['safra']}, Sauda={scores['sauda']}, Dam={scores['dam']}")
    print(f"    Dominant Mizaj: {zmai_eval['primary_dominant_humor'].upper()} (Score: {zmai_eval['primary_score']}/18 -> {zmai_eval['primary_category']})")
    print(f"    Dosage Form Mandate: {zmai_eval['clinical_adjustment_logic']['recommended_dosage_form']}")
    print(f"    Contraindicated Form: {zmai_eval['clinical_adjustment_logic']['contraindicated_dosage_form']}")
    print(f"    Pharmacological Strategy: {zmai_eval['clinical_adjustment_logic']['pharmacological_strategy']}")

    # -------------------------------------------------------------------------
    # 3. Objective Biomarker Validation (Part One Ch 8)
    # -------------------------------------------------------------------------
    print("\n[3] CLOSED-LOOP OBJECTIVE BIOMARKER MAPPING:")
    labs = {
        "fasting_glucose": 114,
        "fasting_insulin": 18.2,
        "tsh": 3.9,
        "ldl": 148,
        "bmi": 29.8,
        "total_testosterone": 340,
        "sperm_count": 11.2,
        "motility": 28.0
    }
    homa_res = calculate_homa_ir(labs["fasting_glucose"], labs["fasting_insulin"])
    labs["homa_ir"] = homa_res["homa_ir"]

    bio_corr_balgham = verify_humoral_biomarker_correlation("BALGHAM", labs)
    bio_corr_sperm = verify_humoral_biomarker_correlation("SPERM", labs)

    print(f"    Calculated HOMA-IR: {homa_res['homa_ir']} ({homa_res['status']})")
    print(f"    Balgham Correlation: {bio_corr_balgham['correlation_status']}")
    for conf in bio_corr_balgham["confirmations"]:
        print(f"      ✓ {conf}")
    print(f"    Spermatogenic Axis Correlation: {bio_corr_sperm['correlation_status']}")
    for conf in bio_corr_sperm["confirmations"]:
        print(f"      ✓ {conf}")

    # -------------------------------------------------------------------------
    # 4. Emergency Triage & Non-Negotiable Lab Trigger Rules
    # -------------------------------------------------------------------------
    print("\n[4] EMERGENCY RED-FLAG & CLINICAL SAFETY TRIAGE:")
    triage = EmergencyRedFlagGuard.screen_patient_for_red_flags(patient["chief_complaints"], labs)
    print(f"    Safe for Unani Outpatient Care: {triage['is_safe_for_unani_care']} (Red Flags Detected: {len(triage['detected_red_flags'])})")

    triggers = evaluate_five_non_negotiable_lab_trigger_rules(labs, patient["chief_complaints"])
    print(f"    Mandatory Lab Trigger Actions Detected: {len(triggers['triggered_rules'])}")
    for tr in triggers["triggered_rules"]:
        print(f"      • [{tr['rule']}]: {tr['finding']} -> {tr['action']}")

    # -------------------------------------------------------------------------
    # 5. Symphonic 4-Tier Formula Formulation & Safety Verification
    # -------------------------------------------------------------------------
    print("\n[5] 4-TIER SYMPHONIC POLYPHARMACY FORMULA & SAFETY AUDIT:")
    formula_100g = [
        # Tier 1: Foundation (Target: 20-30%) -> 25g (25%)
        {"key": "ASGANDH", "name": "Asgandh Nagauri", "tier": 1, "weight_g": 15.0},
        {"key": "SALAB_MISRI", "name": "Salab Misri", "tier": 1, "weight_g": 10.0},
        # Tier 2: Core Therapeutic (Target: 50-60%) -> 55g (55%)
        {"key": "GUGGUL", "name": "Guggul Shuddha", "tier": 2, "weight_g": 20.0},
        {"key": "BEHMAN_SURKH", "name": "Behman Surkh (Leydig Activator)", "tier": 2, "weight_g": 15.0},
        {"key": "BEHMAN_SAFAID", "name": "Behman Safaid (Cooling DNA Substrate)", "tier": 2, "weight_g": 15.0},
        {"key": "TUKHM_JAMUN", "name": "Tukhm Jamun", "tier": 2, "weight_g": 5.0},
        # Tier 3: Correctors / Musleh (Target: 15-25%) -> 15g (15%)
        {"key": "TABASHEER", "name": "Tabasheer (DNA Heat Shield)", "tier": 3, "weight_g": 5.0},
        {"key": "SANDAL_SAFAID", "name": "Sandal Safaid (Thermal Musleh)", "tier": 3, "weight_g": 5.0},
        {"key": "AMLA", "name": "Amla Khushk (Musleh)", "tier": 3, "weight_g": 5.0},
        # Tier 4: Catalysts (Target: 5-10%) -> 5g (5%)
        {"key": "AQARQARHA", "name": "Aqarqarha Micro-dose", "tier": 4, "weight_g": 2.0, "daily_dose_mg": 66.0},
        {"key": "PIPERINE", "name": "Sat Filfil Siyah (Bioenhancer)", "tier": 4, "weight_g": 3.0}
    ]

    tier_audit = FormulaSafetyChecker.audit_four_tier_polypharmacy(formula_100g)
    print(f"    Symphonic Weight Audit: {tier_audit['status']}")
    for tier, pct in tier_audit["tier_percentages"].items():
        print(f"      • {tier.replace('_', ' ').title()}: {pct}% (Target: {tier_audit['ideal_distribution'][tier]})")

    safety_res = FormulaSafetyChecker.audit_formula_safety_and_musleh(formula_100g)
    print(f"    Formula Safety Decision: {safety_res['decision']}")
    print(f"    Violations Count: {len(safety_res['violations'])}")
    for syn in safety_res["synergies_detected"]:
        print(f"      ★ Synergy Active: {syn}")

    # -------------------------------------------------------------------------
    # 6. Program Stacking, UDC Coding & Electronic Prescription
    # -------------------------------------------------------------------------
    print("\n[6] 90-DAY CLINICAL PROGRAM & PRESCRIPTION ENCOUNTER:")
    udc = generate_udc(
        mizaj="Balghami",
        dominant_khilt="Balgham Ghalib",
        primary_axis="Liver-Testicular",
        afaal_phase="Phase 1 (Tanqiya)"
    )
    print(f"    Assigned Unified Diagnostic Code (UDC): {udc}")
    
    pricing = get_program_pricing("SIGNATURE_ELITE", "MALE_METABOLIC_REBUILD")
    if pricing:
        print(f"    90-Day Package: {pricing['name']} — {pricing['duration_days']} Days ({pricing['mrp_inr']})")
    
    print("    Prescription Dispensing Plan:")
    print("      1. Custom Compounded Safoof (100g batch): 5g twice daily with lukewarm water.")
    print("         (Strictly dry powder form per Z-MAI Balgham guideline; Majoon forbidden).")
    print("      2. DiabEase™ (Core Line): 1 capsule 30 minutes before meals.")
    print("      3. Dietary Parhez (MF-01 Balgham Restrictive):")
    print("         - Zero cold dairy, ice cream, sugar, or saturated animal fats.")
    print("         - Warm infused water with Ginger & Cumin; 4-7-8 vagal breathing twice daily.")
    print("=" * 78)
    print(" ✓ END-TO-END CLINICAL CONTINUUM SIMULATION COMPLETED SUCCESSFULLY")
    print("=" * 78)

if __name__ == "__main__":
    run_simulation()
