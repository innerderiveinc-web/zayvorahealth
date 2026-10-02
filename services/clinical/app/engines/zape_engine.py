"""
ZAYVORA Health OS™ - ZAPE (ZAYVORA AI Personalisation Engine)
Reference: Chapter 28, 'AI Personalisation Framework (ZAPE)',
ZAYVORA Global Edition (Second Edition 2026), Dr. Irfan Ashraf, BUMS.

Implements the 4-Layer Clinical Engine:
  Layer 1: Multimodal Data Ingestion (questionnaires, vitals, labs, wearables, lifestyle)
  Layer 2: 6-Axis Disease Model Activation Scoring (Metabolic, Inflammatory, Gut-Digestive,
           Neuro-Hormonal, Cardiovascular-Renal, Detoxification-Elimination)
  Layer 3: Constitutional (Mizaj) Moderation
  Layer 4: Protocol Adaptation & Longitudinal Response Tuning
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class ZAPEEngine:
    """
    Core AI Personalisation Engine for ZAYVORA Health OS™.
    Operates strictly as an advisory clinical decision support system (SaMD Tier IIa)
    with human-clinician-in-the-loop governance.
    """

    AXES = [
        "Metabolic Axis",
        "Inflammatory Axis",
        "Gut-Digestive Axis",
        "Neuro-Hormonal Axis",
        "Cardiovascular-Renal Axis",
        "Detoxification-Elimination Axis"
    ]

    MIZAJ_TYPES = [
        "Harr-Yabis",    # Hot-Dry (Safrawi dominant)
        "Harr-Ratab",    # Hot-Wet (Damawi dominant)
        "Bard-Ratab",    # Cold-Wet (Balghami dominant)
        "Bard-Yabis",    # Cold-Dry (Sawdawi dominant)
        "Mutadil"        # Balanced / Temperate
    ]

    @classmethod
    def ingest_patient_data(cls, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Layer 1: Multimodal Data Ingestion & Sanitization.
        Extracts demographics, vitals, questionnaires (PSS, PHQ9, GAD7, PSQI),
        biomarkers, and constitutional indicators.
        """
        patient_profile = {
            "patient_id": raw_input.get("patient_id", "ANON-001"),
            "age": raw_input.get("age", 40),
            "sex": raw_input.get("sex", "unknown"),
            "bmi": float(raw_input.get("bmi", 25.0)),
            "waist_cm": float(raw_input.get("waist_cm", 85.0)),
            "mizaj": raw_input.get("mizaj", "Mutadil"),
            "questionnaires": {
                "pss_10": int(raw_input.get("pss_10", 12)),
                "phq_9": int(raw_input.get("phq_9", 4)),
                "gad_7": int(raw_input.get("gad_7", 3)),
                "psqi": int(raw_input.get("psqi", 5)),
            },
            "vitals": {
                "sbp": int(raw_input.get("sbp", 120)),
                "dbp": int(raw_input.get("dbp", 80)),
                "hrv_ms": float(raw_input.get("hrv_ms", 45.0)),
                "resting_hr": int(raw_input.get("resting_hr", 72))
            },
            "biomarkers": {
                "fbg": float(raw_input.get("fbg", 95.0)),
                "hba1c": float(raw_input.get("hba1c", 5.4)),
                "fasting_insulin": float(raw_input.get("fasting_insulin", 6.0)),
                "hs_crp": float(raw_input.get("hs_crp", 0.8)),
                "alt": float(raw_input.get("alt", 22.0)),
                "ast": float(raw_input.get("ast", 20.0)),
                "ggt": float(raw_input.get("ggt", 25.0)),
                "triglycerides": float(raw_input.get("triglycerides", 120.0)),
                "hdl": float(raw_input.get("hdl", 50.0)),
                "tsh": float(raw_input.get("tsh", 2.1)),
                "ferritin": float(raw_input.get("ferritin", 65.0)),
                "morning_cortisol": float(raw_input.get("morning_cortisol", 14.0)),
                "vitamin_d": float(raw_input.get("vitamin_d", 35.0))
            },
            "symptoms": raw_input.get("symptoms", []),
            "current_medications": raw_input.get("current_medications", [])
        }
        return patient_profile

    @classmethod
    def calculate_axis_activations(cls, profile: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Layer 2: Axis Mapping.
        Computes numerical activation scores (0-100) and severity categorizations
        for each of the 6 core clinical axes based on objective biomarkers and scores.
        """
        bm = profile["biomarkers"]
        vitals = profile["vitals"]
        q = profile["questionnaires"]
        bmi = profile["bmi"]
        symptoms = [s.lower() for s in profile.get("symptoms", [])]

        activations = {}

        # 1. Metabolic Axis (Insulin resistance, mitochondrial failure, dyslipidemia)
        homa_ir = (bm["fbg"] * bm["fasting_insulin"]) / 405.0
        met_score = 0
        if bm["hba1c"] >= 6.5 or bm["fbg"] >= 126 or homa_ir >= 3.5:
            met_score += 45
        elif bm["hba1c"] >= 5.7 or bm["fbg"] >= 100 or homa_ir >= 2.5:
            met_score += 25
        if bmi >= 30.0:
            met_score += 25
        elif bmi >= 25.0:
            met_score += 15
        if bm["triglycerides"] >= 150 or bm["hdl"] < 40:
            met_score += 20
        if "fatigue" in symptoms or "lethargy" in symptoms:
            met_score += 10
        met_score = min(met_score, 100)
        activations["Metabolic Axis"] = {
            "score": met_score,
            "homa_ir": round(homa_ir, 2),
            "severity": cls._score_to_severity(met_score),
            "key_drivers": ["Insulin Resistance" if homa_ir > 2.5 else "None", "Elevated HbA1c" if bm["hba1c"] >= 5.7 else "Optimal Glycemia"]
        }

        # 2. Inflammatory Axis (hs-CRP, visceral adiposity, endothelial damage)
        inf_score = 0
        if bm["hs_crp"] >= 3.0:
            inf_score += 50
        elif bm["hs_crp"] >= 1.0:
            inf_score += 25
        if vitals["sbp"] >= 140 or vitals["dbp"] >= 90:
            inf_score += 20
        if any(s in symptoms for s in ["joint pain", "morning stiffness", "skin eruption", "acne"]):
            inf_score += 25
        inf_score = min(inf_score, 100)
        activations["Inflammatory Axis"] = {
            "score": inf_score,
            "hs_crp": bm["hs_crp"],
            "severity": cls._score_to_severity(inf_score),
            "key_drivers": ["Systemic Inflammation" if bm["hs_crp"] >= 1.0 else "Quiet Terrain"]
        }

        # 3. Gut-Digestive Axis (Dysbiosis, permeability, Su-e-Hazm)
        gut_score = 0
        if any(s in symptoms for s in ["bloating", "gas", "constipation", "diarrhea", "acid reflux"]):
            gut_score += 40
        if "mucus in stool" in symptoms or "irregular bowels" in symptoms:
            gut_score += 25
        if bm["alt"] > 45 or bm["ggt"] > 50:
            gut_score += 20
        if q["psqi"] > 8:
            gut_score += 15
        gut_score = min(gut_score, 100)
        activations["Gut-Digestive Axis"] = {
            "score": gut_score,
            "severity": cls._score_to_severity(gut_score),
            "key_drivers": ["Gastrointestinal Dysmotility" if gut_score > 30 else "Balanced Gut"]
        }

        # 4. Neuro-Hormonal Axis (HPA axis, PSS, PHQ-9, GAD-7, TSH, Cortisol)
        neuro_score = 0
        if q["pss_10"] >= 20 or q["phq_9"] >= 10 or q["gad_7"] >= 10:
            neuro_score += 45
        elif q["pss_10"] >= 14 or q["phq_9"] >= 5 or q["gad_7"] >= 5:
            neuro_score += 25
        if bm["tsh"] > 4.5 or bm["tsh"] < 0.4:
            neuro_score += 25
        elif bm["tsh"] > 2.5:
            neuro_score += 15
        if bm["morning_cortisol"] < 8.0:  # Adrenal burnout flat curve
            neuro_score += 20
        elif bm["morning_cortisol"] > 22.0:  # Acute hypercortisolemia
            neuro_score += 15
        if vitals["hrv_ms"] < 30.0:  # Low HRV = sympathetic dominance
            neuro_score += 15
        neuro_score = min(neuro_score, 100)
        activations["Neuro-Hormonal Axis"] = {
            "score": neuro_score,
            "severity": cls._score_to_severity(neuro_score),
            "key_drivers": ["HPA Dysregulation" if q["pss_10"] >= 14 else "Autonomic Balance"]
        }

        # 5. Cardiovascular-Renal Axis (Vascular fullness, BP, arterial compliance)
        cv_score = 0
        if vitals["sbp"] >= 140 or vitals["dbp"] >= 90:
            cv_score += 50
        elif vitals["sbp"] >= 130 or vitals["dbp"] >= 80:
            cv_score += 30
        if bm["triglycerides"] >= 150:
            cv_score += 20
        if "palpitations" in symptoms or "headache" in symptoms:
            cv_score += 15
        if bm["hs_crp"] >= 2.0:
            cv_score += 15
        cv_score = min(cv_score, 100)
        activations["Cardiovascular-Renal Axis"] = {
            "score": cv_score,
            "severity": cls._score_to_severity(cv_score),
            "key_drivers": ["Vascular Tension" if vitals["sbp"] >= 130 else "Normotensive"]
        }

        # 6. Detoxification-Elimination Axis (Hepatic enzymes, bowel transit, skin clearance)
        detox_score = 0
        if bm["alt"] > 45 or bm["ast"] > 40 or bm["ggt"] > 50:
            detox_score += 45
        if any(s in symptoms for s in ["constipation", "sluggish bowels", "skin eruptions", "chemical sensitivity"]):
            detox_score += 30
        if bm["fasting_insulin"] > 15:
            detox_score += 15
        if q["psqi"] > 8:
            detox_score += 10
        detox_score = min(detox_score, 100)
        activations["Detoxification-Elimination Axis"] = {
            "score": detox_score,
            "severity": cls._score_to_severity(detox_score),
            "key_drivers": ["Hepatic/Bowel Congestion" if detox_score > 30 else "Clear Elimination"]
        }

        return activations

    @classmethod
    def apply_mizaj_moderation(
        cls,
        mizaj: str,
        activations: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Layer 3: Constitutional (Mizaj) Moderation.
        Translates raw activation scores into personalized, temperament-calibrated
        guidance according to Chapter 6 & Chapter 25 principles.
        """
        mizaj_clean = mizaj if mizaj in cls.MIZAJ_TYPES else "Mutadil"

        modifiers = {
            "mizaj": mizaj_clean,
            "qualities": cls._get_mizaj_qualities(mizaj_clean),
            "dietary_orientation": {},
            "botanical_orientation": {},
            "regimental_orientation": {}
        }

        if mizaj_clean == "Harr-Yabis":  # Hot-Dry (Safrawi)
            modifiers["dietary_orientation"] = {
                "principle": "Cooling and moistening (Barid-Ratab)",
                "foods_to_favor": ["Cucumber", "Yogurt", "Barley water", "Pomegranate", "Leafy greens", "Mint", "Coriander"],
                "foods_to_avoid": ["Hot spices (chili, clove)", "Fried foods", "Red meat", "Excess coffee", "Alcohol"],
                "hydration_guideline": "High volume cool water, rose water infusions, avoid excessive dry heat"
            }
            modifiers["botanical_orientation"] = {
                "cooling_agents": ["Licorice (DGL)", "Coriander seed", "Aloe vera", "Sandalwood"],
                "dose_adjustment": "Heating herbs reduced by 25-30%; avoid potent thermogenics"
            }
            modifiers["regimental_orientation"] = {
                "dalak_style": "Slow, deep, gentle effleurage (sedative, cooling)",
                "hydrotherapy": "Moderate warm to cool finish; avoid extreme prolonged heat",
                "exercise": "Swimming, gentle yoga, early morning/evening workouts (avoid midday sun)"
            }

        elif mizaj_clean == "Bard-Ratab":  # Cold-Wet (Balghami)
            modifiers["dietary_orientation"] = {
                "principle": "Warming and drying (Harr-Yabis)",
                "foods_to_favor": ["Ginger", "Cinnamon", "Black pepper", "Garlic", "Roasted grains", "Lean poultry", "Green tea"],
                "foods_to_avoid": ["Dairy products", "Cold beverages", "Ice cream", "Excess sweets", "Raw heavy salads"],
                "eating_window": "Compressed Time-Restricted Eating (8-10 hour daylight window)"
            }
            modifiers["botanical_orientation"] = {
                "warming_agents": ["Cinnamon", "Ginger", "Guggul", "Fenugreek", "Gymnema sylvestre"],
                "dose_adjustment": "Full therapeutic warming dose (100% to +10%)"
            }
            modifiers["regimental_orientation"] = {
                "dalak_style": "Vigorous, stimulating, deep kneading (Pétrissage & tapotement to stimulate metabolism)",
                "hydrotherapy": "Hammam steam & warm immersion (39-40°C) with Epsom salts to dry phlegmatic excess",
                "exercise": "Vigorous aerobic + progressive resistance training in the morning"
            }

        elif mizaj_clean == "Harr-Ratab":  # Hot-Wet (Damawi)
            modifiers["dietary_orientation"] = {
                "principle": "Cooling, drying, and reducing (Barid-Yabis)",
                "foods_to_favor": ["Bitter vegetables (bitter gourd, dandelion)", "Whole barley", "Fish", "Pomegranate", "Hibiscus tea"],
                "foods_to_avoid": ["Red meat", "Excess salt", "Alcohol", "Heavy sweets", "Rich saturated fats"],
                "eating_window": "Moderate Mediterranean DASH-aligned pattern with strict sodium <2g/day"
            }
            modifiers["botanical_orientation"] = {
                "toning_agents": ["Arjuna bark", "Kalonji", "Hibiscus sabdariffa", "Garlic extract"],
                "dose_adjustment": "Heating herbs reduced by 15-20%"
            }
            modifiers["regimental_orientation"] = {
                "dalak_style": "Moderate pressure, circulatory drainage toward the heart",
                "hydrotherapy": "Contrast hydrotherapy (3 min warm / 30-60 sec cool) to train vascular compliance",
                "exercise": "Swimming, brisk walking, moderate cycling (avoid excessive thermal strain)"
            }

        elif mizaj_clean == "Bard-Yabis":  # Cold-Dry (Sawdawi)
            modifiers["dietary_orientation"] = {
                "principle": "Warming, moistening, and nourishing (Harr-Ratab)",
                "foods_to_favor": ["Bone broths", "Ghee", "Dates", "Warm milk with saffron", "Cooked root vegetables", "Oily fish"],
                "foods_to_avoid": ["Cold/raw dry foods (chips, crackers)", "Excess caffeine", "Strict long fasting"],
                "eating_window": "Regular frequent nourishing meals; do not skip breakfast"
            }
            modifiers["botanical_orientation"] = {
                "nervine_agents": ["Ashwagandha KSM-66", "Saffron", "Jatamansi", "Brahmi"],
                "dose_adjustment": "Moistening and adaptogenic emphasis; support HPA axis and gut motility"
            }
            modifiers["regimental_orientation"] = {
                "dalak_style": "Warm nourishing oil massage (sesame or almond oil with warming aromatics)",
                "hydrotherapy": "Gentle warm bath with magnesium; avoid extreme cold plunge",
                "exercise": "Gentle restorative yoga, mindful walking in sunlight, diaphragmatic breathing"
            }

        else:  # Mutadil (Balanced)
            modifiers["dietary_orientation"] = {
                "principle": "Equilibrium maintenance",
                "foods_to_favor": ["Diverse Mediterranean diet with 30+ plant species/week", "Clean hydration"],
                "foods_to_avoid": ["Ultra-processed foods", "Excess refined sugars", "Trans fats"],
                "eating_window": "10-hour daytime eating window"
            }
            modifiers["botanical_orientation"] = {
                "wellness_agents": ["Triphala", "Green tea", "Turmeric"],
                "dose_adjustment": "Standard reference posology"
            }
            modifiers["regimental_orientation"] = {
                "dalak_style": "Balanced full-body restorative massage",
                "hydrotherapy": "Morning contrast shower",
                "exercise": "Balanced aerobic and resistance training 150 min/week"
            }

        return modifiers

    @classmethod
    def generate_zape_decision_support(
        cls,
        raw_patient_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Layer 4: Protocol Adaptation & Decision Generation.
        Synthesizes Layers 1-3 to output an actionable, 4-tier clinical protocol.
        """
        profile = cls.ingest_patient_data(raw_patient_input)
        activations = cls.calculate_axis_activations(profile)
        mizaj_mods = cls.apply_mizaj_moderation(profile["mizaj"], activations)

        ranked_axes = sorted(
            [{"axis": k, **v} for k, v in activations.items()],
            key=lambda x: x["score"],
            reverse=True
        )

        primary_axis = ranked_axes[0]["axis"]
        secondary_axis = ranked_axes[1]["axis"] if len(ranked_axes) > 1 else None

        tier_1_lifestyle = {
            "nutrition": mizaj_mods["dietary_orientation"],
            "exercise": mizaj_mods["regimental_orientation"]["exercise"],
            "sleep_target": "7-8 hours in dark room (18-20°C); morning bright light (10,000 lux)",
            "stress_management": "Resonance frequency slow breathing at 6 cycles/min + MBSR"
        }

        tier_2_botanicals = cls._select_tier_2_botanicals(primary_axis, profile["mizaj"])
        if secondary_axis and activations[secondary_axis]["score"] >= 60:
            secondary_botanicals = cls._select_tier_2_botanicals(secondary_axis, profile["mizaj"])
            for sb in secondary_botanicals:
                if not any(b["botanical"] == sb["botanical"] for b in tier_2_botanicals):
                    tier_2_botanicals.append(sb)

        tier_3_pharmacotherapy = {
            "guideline": "Advisory oversight only. Prescribed only by licensed medical doctor.",
            "indications_flagged": cls._flag_pharmacotherapy_needs(profile, primary_axis)
        }


        tier_4_regimental = {
            "dalak": mizaj_mods["regimental_orientation"]["dalak_style"],
            "hydrotherapy": mizaj_mods["regimental_orientation"]["hydrotherapy"],
            "hijama_evaluation": cls._evaluate_hijama_eligibility(profile, primary_axis)
        }

        return {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "patient_id": profile["patient_id"],
            "mizaj": profile["mizaj"],
            "axis_priority_ranking": [a["axis"] for a in ranked_axes],
            "axis_activations": activations,
            "primary_axis": primary_axis,
            "secondary_axis": secondary_axis,
            "constitutional_modifiers": mizaj_mods,
            "recommendations": {
                "tier_1_lifestyle": tier_1_lifestyle,
                "tier_2_botanicals": tier_2_botanicals,
                "tier_3_pharmacotherapy": tier_3_pharmacotherapy,
                "tier_4_regimental": tier_4_regimental
            },
            "clinical_safety_notice": "ZAPE recommendations are advisory clinical decision support. All final prescriptions and diagnostic conclusions remain the sole responsibility of the licensed treating physician."
        }

    @staticmethod
    def _score_to_severity(score: int) -> str:
        if score >= 65:
            return "Severe"
        elif score >= 35:
            return "Moderate"
        elif score >= 15:
            return "Mild"
        return "Normal"

    @staticmethod
    def _get_mizaj_qualities(mizaj: str) -> str:
        qualities_map = {
            "Harr-Yabis": "Hot & Dry (Fire element / Safra)",
            "Harr-Ratab": "Hot & Wet (Air element / Dam)",
            "Bard-Ratab": "Cold & Wet (Water element / Balgham)",
            "Bard-Yabis": "Cold & Dry (Earth element / Sauda)",
            "Mutadil": "Temperate & Balanced"
        }
        return qualities_map.get(mizaj, "Balanced")

    @classmethod
    def _select_tier_2_botanicals(cls, primary_axis: str, mizaj: str) -> List[Dict[str, Any]]:
        botanicals = []
        if primary_axis == "Metabolic Axis":
            botanicals.append({"botanical": "Berberine", "dose": "500 mg tid before meals", "evidence_level": "1b", "mechanism": "AMPK activation, GLUT4 upregulation"})
            botanicals.append({"botanical": "Cinnamon (C. verum)", "dose": "1-3g powder daily", "evidence_level": "1b", "mechanism": "Insulin receptor sensitisation"})
            if mizaj in ["Bard-Ratab", "Bard-Yabis"]:
                botanicals.append({"botanical": "Gurmar (Gymnema sylvestre)", "dose": "400 mg extract before meals", "evidence_level": "1b", "mechanism": "Sweet receptor blockade, glucose absorption reduction"})
            else:
                botanicals.append({"botanical": "Jamun seed (Syzygium cumini)", "dose": "1-2g daily", "evidence_level": "2b", "mechanism": "Cooling metabolic modulator"})

        elif primary_axis == "Cardiovascular-Renal Axis":
            botanicals.append({"botanical": "Arjuna bark (Terminalia arjuna)", "dose": "500 mg bd", "evidence_level": "1b", "mechanism": "Cardiotonic, calcium channel modulation"})
            botanicals.append({"botanical": "Kalonji (Nigella sativa)", "dose": "2-3g/day oil or powder", "evidence_level": "1b", "mechanism": "Thymoquinone ACE inhibition, vasodilation"})
            botanicals.append({"botanical": "Hibiscus sabdariffa tea", "dose": "240 mL bd", "evidence_level": "1b", "mechanism": "ACE inhibitory anthocyanins, mild diuresis"})

        elif primary_axis == "Gut-Digestive Axis":
            botanicals.append({"botanical": "Isabgol (Psyllium husk)", "dose": "5-10g with warm water", "evidence_level": "1a", "mechanism": "Bifunctional bowel regulation, prebiotic"})
            botanicals.append({"botanical": "Peppermint oil (enteric-coated)", "dose": "0.2-0.4 mL tid", "evidence_level": "1a", "mechanism": "Smooth muscle calcium antagonism, spasmolysis"})
            botanicals.append({"botanical": "Triphala", "dose": "1g before bed", "evidence_level": "1b", "mechanism": "Mild prokinetic, microbiome diversity"})

        elif primary_axis == "Neuro-Hormonal Axis":
            botanicals.append({"botanical": "Ashwagandha (KSM-66)", "dose": "300-600 mg daily", "evidence_level": "1b", "mechanism": "HPA axis normalisation, cortisol reduction 15-30%"})
            botanicals.append({"botanical": "Jatamansi (Nardostachys jatamansi)", "dose": "300-500 mg at bedtime", "evidence_level": "2b", "mechanism": "GABA-A modulation, sleep consolidation"})
            botanicals.append({"botanical": "Saffron (Crocus sativus)", "dose": "30 mg bd", "evidence_level": "1a", "mechanism": "Monoamine reuptake inhibition, neuroprotection"})

        elif primary_axis == "Inflammatory Axis":
            botanicals.append({"botanical": "Curcumin + Piperine", "dose": "500-1000 mg bd", "evidence_level": "1a", "mechanism": "NF-kB inhibition, TNF-alpha suppression"})
            botanicals.append({"botanical": "Boswellia serrata", "dose": "300-500 mg tid", "evidence_level": "1b", "mechanism": "5-LOX inflammatory pathway inhibition"})
            botanicals.append({"botanical": "Omega-3 (EPA/DHA)", "dose": "2-4g daily", "evidence_level": "1a", "mechanism": "Pro-resolving lipid mediator synthesis"})

        else:  # Detoxification-Elimination Axis
            botanicals.append({"botanical": "Milk Thistle (Silymarin)", "dose": "140 mg tid (70-80% extract)", "evidence_level": "1b", "mechanism": "Hepatic membrane stabilisation, glutathione protection"})
            botanicals.append({"botanical": "Kasni (Cichorium intybus)", "dose": "500 mg extract daily", "evidence_level": "2b", "mechanism": "Choleretic, PPAR-alpha hepatic lipid mobilization"})

        return botanicals

    @classmethod
    def _flag_pharmacotherapy_needs(cls, profile: Dict[str, Any], primary_axis: str) -> List[str]:
        flags = []
        bm = profile["biomarkers"]
        v = profile["vitals"]

        if bm["hba1c"] >= 9.0:
            flags.append("Urgent Metformin/conventional pharmacotherapy required (HbA1c >= 9.0%). Do not delay for lifestyle alone.")
        if v["sbp"] >= 180 or v["dbp"] >= 120:
            flags.append("Hypertensive Crisis (BP >= 180/120). Immediate medical emergency evaluation required.")
        elif v["sbp"] >= 140 or v["dbp"] >= 90:
            flags.append("Stage 2 Hypertension: Dual-agent pharmacotherapy recommended alongside lifestyle.")
        if bm["alt"] > 100:
            flags.append("Severe transaminitis (ALT > 100 U/L): Hepatology referral required for acute pathology screening.")
        if bm["tsh"] > 10.0:
            flags.append("Overt Hypothyroidism (TSH > 10.0 mIU/L): Levothyroxine indication under endocrine care.")

        if not flags:
            flags.append("Patient in Tier 1/2 preventive window; conventional prescription standby pending 12-week review.")
        return flags

    @classmethod
    def _evaluate_hijama_eligibility(cls, profile: Dict[str, Any], primary_axis: str) -> Dict[str, Any]:
        meds = [m.lower() for m in profile.get("current_medications", [])]
        is_anticoagulated = any(a in m for m in meds for a in ["warfarin", "heparin", "eliquis", "xarelto", "apixaban", "rivaroxaban"])

        if is_anticoagulated:
            return {"eligible": False, "reason": "Absolute contraindication: Active oral anticoagulation"}
        if profile["biomarkers"]["ferritin"] < 20.0:
            return {"eligible": False, "reason": "Caution: Low ferritin stores (<20 ng/mL)"}

        if primary_axis in ["Cardiovascular-Renal Axis", "Inflammatory Axis"] or profile["mizaj"] in ["Harr-Ratab", "Harr-Yabis"]:
            return {
                "eligible": True,
                "recommended_sites": ["L3-L5 paraspinal area", "Interscapular (between shoulder blades)", "Cervical base"],
                "protocol": "Superficial scarification (1-2 mm), sterile disposable equipment, 30-50 mL total extraction",
                "frequency": "Monthly for 3-4 sessions, then maintenance at seasonal transitions (Spring/Autumn)"
            }

        return {
            "eligible": True,
            "recommended_sites": ["Interscapular region"],
            "protocol": "Maintenance detox cupping once every 3-6 months",
            "frequency": "Seasonal maintenance"
        }
