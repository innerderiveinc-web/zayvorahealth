"""
ZAYVORA Health OS™ - Patient Education & Vernacular Health Literacy Modules
Reference: Understanding Your Health Through the Lens of Unani Medicine,
Author: Dr. Irfan Ashraf, BUMS.

Transforms complex clinical biochemistry and Unani concepts into accessible,
empowering patient educational modules.
"""

from typing import Dict, Any, List, Optional


PATIENT_EDUCATION_CHAPTERS: Dict[str, Dict[str, Any]] = {
    "THREE_HEALTH_CRISES": {
        "slug": "three-health-crises",
        "title": "The Three Health Crises of the Modern Era",
        "target_audience": "Patients, Families & Health-Conscious Individuals",
        "summary": "Why modern urban life is causing homeostatic failure across reproductive, hormonal, and metabolic systems.",
        "crises": [
            {
                "name": "The Male Reproductive Crisis",
                "statistics": "Average sperm counts in industrialised nations have fallen by >50% over the past 50 years. Clinically low testosterone ('andropause') is now routinely diagnosed in men in their late 20s and 30s.",
                "root_drivers": [
                    "Chronic occupational stress causing persistent cortisol suppression of GnRH/LH pulses",
                    "Circadian disruption: missing the 10 PM - 2 AM deep sleep window where 70% of testosterone is synthesized",
                    "Environmental xenoestrogens: microplastics, bisphenols, phthalates, pesticides",
                    "Scrotal hyperthermia from sedentary desk work, synthetic tight clothing, and laptops on laps",
                    "Nutritional deficiencies: zinc, selenium, CoQ10, omega-3 fatty acids"
                ],
                "biological_timeline": "Spermatogenesis takes 74 days; clinical turnaround requires a minimum 90 to 120-day committed cycle."
            },
            {
                "name": "The Female Metabolic Chaos (PCOS & Thyroid)",
                "statistics": "PCOS affects 1 in 5 Indian women of reproductive age. Hashimoto's thyroiditis is the leading cause of female hypothyroidism.",
                "root_drivers": [
                    "Insulin resistance driving ovarian theca cells to overproduce androgens",
                    "The oral contraceptive pill suppresses symptoms but leaves underlying metabolic driver untouched",
                    "Low T3 syndrome: normal TSH while active cellular T3 remains depleted",
                    "Chronic gut permeability and gluten-associated molecular mimicry in thyroid autoimmunity"
                ],
                "biological_timeline": "Requires 3 full menstrual cycles for follicular recruitment and metabolic insulin sensitisation."
            },
            {
                "name": "The Urban Lifestyle Epidemic (Fatty Liver & Burnout)",
                "statistics": "NAFLD affects 25-30% of adults globally. Over 537 million people live with metabolic syndrome.",
                "root_drivers": [
                    "Sustained mismatch between human evolutionary design (movement, natural light, seasonal eating) and modern knowledge economy (10 hours sitting, screens at midnight, ultra-processed food)",
                    "Fructose and refined carbohydrates driving de novo hepatic lipogenesis",
                    "Burnout (Inzibaab-e-Rooh) characterized by glymphatic brain congestion and HPA axis exhaustion"
                ],
                "biological_timeline": "Grades I-II NAFLD are completely reversible within 12-16 weeks of structured lifestyle and botanical care."
            }
        ]
    },
    "TSH_VS_FREE_T3": {
        "slug": "tsh-vs-free-t3",
        "title": "The Thyroid Trap: Why 'Normal' TSH Still Leaves You Exhausted",
        "key_concept": "TSH is a pituitary messenger hormone, NOT a thyroid hormone. Measuring TSH alone fails to see what your body's cells are receiving.",
        "pathophysiology": {
            "inactive_storage": "T4 (Thyroxine) is produced by the thyroid gland as an inactive storage hormone.",
            "active_metabolic_driver": "T3 (Triiodothyronine) is the active hormone that enters mitochondria and drives basal metabolic rate.",
            "the_liver_connection": "Approximately 60% of all T4-to-T3 conversion occurs in the LIVER via 5'-deiodinase enzymes. When NAFLD or hepatic inflammation is present, conversion stalls.",
            "low_t3_syndrome": "A patient can have a completely normal TSH (e.g. 2.1 mIU/L) and normal T4, yet have low Free T3 and high Reverse T3 (rT3), causing severe fatigue, cold intolerance, and weight loss resistance."
        },
        "functional_biomarkers": [
            {"test": "TSH", "conventional_range": "0.5 - 4.5 mIU/L", "functional_optimal": "1.0 - 2.0 mIU/L"},
            {"test": "Free T3", "conventional_range": "2.0 - 4.4 pg/mL", "functional_optimal": "3.2 - 4.0 pg/mL"},
            {"test": "Free T4", "conventional_range": "0.8 - 1.8 ng/dL", "functional_optimal": "1.1 - 1.4 ng/dL"},
            {"test": "Reverse T3 (rT3)", "conventional_range": "<24 ng/dL", "functional_optimal": "<15 ng/dL"}
        ]
    },
    "HOMA_IR_EXPLAINED": {
        "slug": "homa-ir-explained",
        "title": "Insulin Resistance: The Invisible Upstream Driver",
        "explanation": "Fasting blood sugar can remain completely normal for 10-15 years while the pancreas produces 5x to 10x more insulin to force glucose into resistant muscle and liver cells.",
        "formula": "HOMA-IR = (Fasting Glucose [mg/dL] * Fasting Insulin [uIU/mL]) / 405",
        "interpretation": [
            {"score_range": "<1.5", "status": "Optimal Insulin Sensitivity", "risk": "Minimal"},
            {"score_range": "1.5 - 2.5", "status": "Early / Borderline Insulin Resistance", "risk": "Moderate (Early metabolic syndrome)"},
            {"score_range": ">2.5 - 3.5", "status": "Established Insulin Resistance", "risk": "High (PCOS, NAFLD driver)"},
            {"score_range": ">3.5", "status": "Severe Insulin Resistance", "risk": "Critical (Pre-diabetic state requiring immediate protocol)"}
        ]
    },
    "THE_SIX_ESSENTIALS": {
        "slug": "the-six-essentials",
        "title": "The Six Non-Negotiable Essentials (Asbab-e-Sitta-e-Zaruriya)",
        "prescriptions": [
            {
                "pillar": "Sleep & Wakefulness (Nawm wa Yaqzah)",
                "rules": [
                    "In bed by 10:30 PM: Growth hormone and 70% of testosterone are produced during deep sleep between 10 PM and 2 AM.",
                    "Screens off by 9:00 PM: 460-490nm blue light delays melatonin onset by 90 minutes.",
                    "Morning sunlight within 10 minutes of waking: Calibrates the cortisol awakening response (CAR)."
                ]
            },
            {
                "pillar": "Psychological State (Nafsaniyat) & 4-7-8 Breathing",
                "rules": [
                    "Diaphragmatic breathing with prolonged exhalation directly stimulates the cardiac vagal nerve.",
                    "Practice 4-7-8 technique (Inhale 4s, Hold 7s, Exhale 8s) for 10 minutes daily to shift autonomic tone within 4 days."
                ]
            },
            {
                "pillar": "Food & Drink (Makool wa Mashroob) & Glycemic Swaps",
                "rules": [
                    "Replace white rice with millets (jowar, bajra, ragi) or quinoa.",
                    "Replace refined maida with whole-grain chickpea flour (besan).",
                    "Eliminate refined vegetable seed oils (sunflower, soya); switch to cold-pressed sesame, mustard, or extra virgin olive oil.",
                    "Post-meal walking: A 15-20 minute walk after lunch and dinner blunts the blood glucose peak by 20-30%."
                ]
            }
        ]
    }
}


def get_patient_education_module(slug: str) -> Optional[Dict[str, Any]]:
    for mod in PATIENT_EDUCATION_CHAPTERS.values():
        if mod.get("slug") == slug:
            return mod
    return None


def get_all_patient_education_modules() -> List[Dict[str, Any]]:
    return list(PATIENT_EDUCATION_CHAPTERS.values())
