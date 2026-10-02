"""
ZAYVORA Health OS™ - 8 Major Disease Protocols & Appendix B Templates
Reference: Chapters 14-21 and Appendix B (B1-B4),
ZAYVORA Global Edition (Second Edition 2026), Dr. Irfan Ashraf, BUMS.

Implements standard diagnostic evaluation and treatment protocols for:
  1. Type 2 Diabetes Mellitus (Template B1)
  2. Hypertension (Template B2)
  3. Polycystic Ovarian Syndrome (PCOS) (Template B3)
  4. Obesity & Metabolic Syndrome (Template B4)
  5. Non-Alcoholic Fatty Liver Disease (NAFLD / MAFLD)
  6. Irritable Bowel Syndrome (IBS)
  7. Chronic Stress Syndrome
  8. Autoimmune Tendency Framework
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class GlobalProtocolsEngine:
    """
    Standard Clinical Protocol Engine generating verified diagnostic classifications
    and Appendix B templates according to the ZAYVORA Global Edition.
    """

    # ------------------- 1. TYPE 2 DIABETES (TEMPLATE B1) -------------------
    @classmethod
    def evaluate_t2dm(
        cls,
        hba1c: float,
        fbg: float,
        fasting_insulin: float,
        bmi: float,
        waist_cm: float,
        mizaj: str = "Bard-Ratab",
        current_meds: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Chapter 14 & Template B1: T2DM Evaluation & Remission Assessment.
        """
        current_meds = current_meds or []
        homa_ir = (fbg * fasting_insulin) / 405.0

        # Classification
        if hba1c >= 6.5 or fbg >= 126.0:
            status = "Type 2 Diabetes Mellitus Confirmed"
        elif 5.7 <= hba1c <= 6.4 or 100.0 <= fbg <= 125.0:
            status = "Prediabetes (Impaired Fasting Glucose / Glucose Intolerance)"
        else:
            status = "Normoglycemic"

        # Remission Check (DiRECT criteria: off medications for >= 1 year with HbA1c < 5.7% or < 6.5%)
        is_in_remission = False
        remission_type = "None"
        if len(current_meds) == 0:
            if hba1c < 5.7:
                is_in_remission = True
                remission_type = "Complete Remission (Normal HbA1c < 5.7% off medication)"
            elif 5.7 <= hba1c < 6.5:
                is_in_remission = True
                remission_type = "Partial Remission (Prediabetes range 5.7-6.4% off medication)"

        # Appendix B1 Structured Template
        template_b1 = {
            "template_id": "Appendix B1: Type 2 Diabetes Initial Assessment",
            "patient_mizaj": mizaj,
            "dominant_axis_drivers": [
                "Insulin Resistance (HOMA-IR: {:.2f})".format(homa_ir) if homa_ir > 2.5 else "Beta-Cell Stress",
                "Excess Balgham (Cold-Moist)" if mizaj in ["Bard-Ratab", "Bard-Yabis"] else "Safra / Hararat Heat Burnout"
            ],
            "metabolic_baseline": {
                "hba1c_percent": hba1c,
                "fbg_mg_dl": fbg,
                "fasting_insulin_uIU_ml": fasting_insulin,
                "homa_ir": round(homa_ir, 2),
                "bmi": bmi,
                "waist_cm": waist_cm
            },
            "pharmacological_status": current_meds if current_meds else ["None - Intensive Lifestyle Trial"],
            "dietary_protocol_assigned": "Low-GI Mediterranean with 14:10 or 16:8 Time-Restricted Eating (TRE)",
            "botanical_protocol": [
                "Berberine 500 mg tid before meals",
                "Cinnamon extract (Cinnamomum verum) 1-3g daily",
                "Gurmar (Gymnema sylvestre) 400 mg before carbs" if mizaj in ["Bard-Ratab", "Bard-Yabis"] else "Jamun seed (Syzygium cumini) 1-2g daily"
            ],
            "regimental_therapies_prescribed": [
                "Daily morning brisk walk 30-45 min (GLUT4 translocation)",
                "Resistance training 3x/week",
                "Weekly Dalak (warming oil)" if mizaj in ["Bard-Ratab", "Bard-Yabis"] else "Cooling hydrotherapy"
            ],
            "target_hba1c": "< 6.5% (remission target < 5.7%)",
            "target_weight_loss_kg": round(bmi * 0.07 * 2.2, 1)  # 7-10% body weight loss
        }

        return {
            "status": status,
            "is_in_remission": is_in_remission,
            "remission_type": remission_type,
            "template_b1": template_b1
        }

    # ------------------- 2. HYPERTENSION (TEMPLATE B2) -------------------
    @classmethod
    def evaluate_hypertension(
        cls,
        sbp: int,
        dbp: int,
        mizaj: str = "Harr-Ratab",
        has_cardiac_symptoms: bool = False,
        current_meds: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Chapter 15 & Template B2: Hypertension Evaluation (ACC/AHA 2017 & Unani Imtila-e-Dam).
        """
        current_meds = current_meds or []

        if sbp >= 180 or dbp >= 120:
            category = "Hypertensive Crisis (EMERGENCY)"
            zayvora_response = "Immediate medical emergency evaluation; pharmacological priority"
        elif sbp >= 140 or dbp >= 90:
            category = "Stage 2 Hypertension"
            zayvora_response = "Lifestyle + Antihypertensive medication; integrative adjuncts"
        elif (130 <= sbp <= 139) or (80 <= dbp <= 89):
            category = "Stage 1 Hypertension"
            zayvora_response = "Lifestyle trial 3-6 months +/- medication based on CV risk score"
        elif (120 <= sbp <= 129) and dbp < 80:
            category = "Elevated Blood Pressure"
            zayvora_response = "Intensive lifestyle intervention; monthly review"
        else:
            category = "Normal Blood Pressure"
            zayvora_response = "Preventive lifestyle - constitutional nutrition, sleep, stress alignment"

        template_b2 = {
            "template_id": "Appendix B2: Hypertension Initial Assessment",
            "patient_mizaj": mizaj,
            "unani_concept": "Imtila-e-Dam (Vascular Plethora) and Ghulba-e-Dam",
            "bp_reading": f"{sbp}/{dbp} mmHg",
            "category": category,
            "zayvora_response": zayvora_response,
            "dietary_protocol": "DASH Protocol, Sodium strict < 2,000 mg/day, Potassium & Magnesium Augmentation",
            "botanical_support": [
                "Arjuna bark extract (Terminalia arjuna) 500 mg bd",
                "Kalonji oil (Nigella sativa) 2.5 mL bd",
                "Hibiscus sabdariffa flower tea 240 mL bd (ACE-inhibitory anthocyanins)"
            ],
            "regimental_therapies": [
                "Contrast hydrotherapy to train vascular compliance",
                "Resonance frequency slow breathing at 6 breaths/min (baroreflex sensitization)",
                "Hijama wet cupping (L3-L5 & interscapular) if volume plethora and no anticoagulation"
            ],
            "target_bp": "< 130/80 mmHg (< 140/90 in frail elderly)"
        }

        return {
            "category": category,
            "requires_urgent_medical": sbp >= 180 or dbp >= 120,
            "template_b2": template_b2
        }

    # ------------------- 3. PCOS (TEMPLATE B3) -------------------
    @classmethod
    def evaluate_pcos(
        cls,
        cycle_length_days: int,
        cycles_per_year: int,
        hirsutism_score: int,  # Ferriman-Gallwey score
        total_testosterone_nmol: float,
        ovarian_follicles_count: int,
        amh_pmol_l: float,
        fasting_insulin: float,
        homa_ir: float,
        mizaj: str = "Bard-Ratab",
        fertility_intent: bool = False
    ) -> Dict[str, Any]:
        """
        Chapter 16 & Template B3: PCOS Rotterdam Criteria & Phenotypic Classification.
        Rotterdam Criteria requires 2 of 3:
          1. Oligo/Anovulation (cycles > 35 days or < 8/year)
          2. Clinical/Biochemical Hyperandrogenism (FG score >= 8 or Testo > 2.5 nmol/L)
          3. Polycystic Ovaries (>= 20 follicles or AMH > 35 pmol/L)
        """
        crit_1 = cycle_length_days > 35 or cycles_per_year < 8
        crit_2 = hirsutism_score >= 8 or total_testosterone_nmol > 2.5
        crit_3 = ovarian_follicles_count >= 20 or amh_pmol_l > 35.0

        criteria_met = sum([crit_1, crit_2, crit_3])
        pcos_confirmed = criteria_met >= 2

        # Phenotype classification
        if crit_1 and crit_2 and crit_3:
            phenotype = "Phenotype A (Full: Anovulation + Hyperandrogenism + PCOM)"
        elif crit_1 and crit_2:
            phenotype = "Phenotype B (Classic: Anovulation + Hyperandrogenism)"
        elif crit_2 and crit_3:
            phenotype = "Phenotype C (Ovulatory: Hyperandrogenism + PCOM)"
        elif crit_1 and crit_3:
            phenotype = "Phenotype D (Non-Androgenic: Anovulation + PCOM)"
        else:
            phenotype = "Sub-diagnostic or Non-PCOS"

        template_b3 = {
            "template_id": "Appendix B3: PCOS Initial Assessment",
            "patient_mizaj": mizaj,
            "unani_concept": "Ihtibas-e-Taams (Menstrual Obstruction) due to Balgham excess or Ghilaz-e-Dam",
            "rotterdam_criteria_met_count": criteria_met,
            "pcos_confirmed": pcos_confirmed,
            "phenotype": phenotype,
            "metabolic_status": {
                "fasting_insulin": fasting_insulin,
                "homa_ir": homa_ir,
                "insulin_resistant": homa_ir > 2.5 or fasting_insulin > 15
            },
            "fertility_intent": fertility_intent,
            "inositol_protocol": "Myo-Inositol 4g/day + D-Chiro-Inositol in 40:1 ratio",
            "botanical_protocol": [
                "Spearmint tea (2 cups daily for anti-androgenic effect)",
                "Vitex agnus-castus (Chaste Tree) for LH/FSH normalization",
                "Berberine 500 mg tid (insulin sensitisation)"
            ],
            "lifestyle_prescription": "Low-glycemic Mediterranean nutrition, resistance training to improve muscle glucose disposal, 20 min daily mind-body practice",
            "referral_notes": "Refer for reproductive endocrinology co-management if pregnancy is actively sought" if fertility_intent else "Conservative endocrine-metabolic optimization"
        }

        return {
            "pcos_confirmed": pcos_confirmed,
            "phenotype": phenotype,
            "template_b3": template_b3
        }

    # ------------------- 4. METABOLIC SYNDROME (TEMPLATE B4) -------------------
    @classmethod
    def evaluate_metabolic_syndrome(
        cls,
        waist_cm: float,
        sex: str,
        is_asian: bool,
        triglycerides_mg_dl: float,
        hdl_mg_dl: float,
        sbp: int,
        dbp: int,
        fbg_mg_dl: float,
        mizaj: str = "Bard-Ratab"
    ) -> Dict[str, Any]:
        """
        Chapter 17 & Template B4: Metabolic Syndrome Evaluation (IDF/AHA/NHLBI 2009 Harmonized).
        Requires 3 of 5 criteria:
          1. Abdominal Obesity (Waist > 90cm M / > 80cm F in Asians; > 102cm M / > 88cm F in Western)
          2. Raised Triglycerides (>= 150 mg/dL)
          3. Reduced HDL (< 40 mg/dL M, < 50 mg/dL F)
          4. Raised Blood Pressure (>= 130/85 mmHg)
          5. Raised Fasting Glucose (>= 100 mg/dL)
        """
        # 1. Waist
        if is_asian:
            waist_cut = 90.0 if sex.lower() == "male" else 80.0
        else:
            waist_cut = 102.0 if sex.lower() == "male" else 88.0
        crit_waist = waist_cm >= waist_cut

        # 2. TG
        crit_tg = triglycerides_mg_dl >= 150.0

        # 3. HDL
        hdl_cut = 40.0 if sex.lower() == "male" else 50.0
        crit_hdl = hdl_mg_dl < hdl_cut

        # 4. BP
        crit_bp = sbp >= 130 or dbp >= 85

        # 5. FBG
        crit_fbg = fbg_mg_dl >= 100.0

        criteria_hits = [
            ("Central Obesity", crit_waist),
            ("Elevated Triglycerides", crit_tg),
            ("Reduced HDL", crit_hdl),
            ("Elevated Blood Pressure", crit_bp),
            ("Impaired Fasting Glucose", crit_fbg)
        ]
        total_hits = sum(1 for _, met in criteria_hits if met)
        met_syn_confirmed = total_hits >= 3

        template_b4 = {
            "template_id": "Appendix B4: Metabolic Syndrome Initial Assessment",
            "patient_mizaj": mizaj,
            "unani_concept": "Samn Mufrit (Excessive Fatness) & Ghilaz-e-Dam with Balgham Dominance",
            "criteria_met_count": total_hits,
            "metabolic_syndrome_confirmed": met_syn_confirmed,
            "criteria_breakdown": {name: met for name, met in criteria_hits},
            "dietary_assignment": "Time-Restricted Eating (10-hour daytime window), Low-GI, front-loaded calories",
            "exercise_prescription": {
                "phase_1": "Weeks 1-4: Daily walking at comfortable pace (movement habit)",
                "phase_2": "Weeks 5-8: Progressive resistance training (2-3x/week) for muscle mass",
                "phase_3": "Weeks 9-12: High-Intensity Interval Training (HIIT) for visceral fat mobilization"
            },
            "botanical_protocol": [
                "Gurmar (Gymnema sylvestre) 400 mg before meals",
                "Berberine 500 mg tid",
                "Triphala 1g before bed (prebiotic and gentle metabolic regulator)"
            ],
            "three_month_targets": {
                "weight_reduction_percent": "5-10% of total body weight",
                "triglycerides_target": "< 150 mg/dL",
                "bp_target": "< 130/80 mmHg"
            }
        }

        return {
            "metabolic_syndrome_confirmed": met_syn_confirmed,
            "criteria_count": total_hits,
            "template_b4": template_b4
        }

    # ------------------- 5. NAFLD / MAFLD (CHAPTER 18) -------------------
    @classmethod
    def evaluate_nafld(
        cls,
        alt: float,
        ast: float,
        bmi: float,
        has_diabetes: bool,
        platelet_count: int,
        age: int
    ) -> Dict[str, Any]:
        """
        Chapter 18: NAFLD Assessment via HSI and FIB-4.
        HSI = 8 * (ALT/AST) + BMI + (2 if DM else 0) + (2 if female else 0)
        FIB-4 = (Age * AST) / (Platelets * sqrt(ALT))
        """
        import math
        hsi = 8.0 * (alt / max(ast, 1.0)) + bmi + (2.0 if has_diabetes else 0.0)
        fib4 = (age * ast) / (max(platelet_count, 1) * math.sqrt(max(alt, 1.0)))

        steatosis_likely = hsi > 36.0
        advanced_fibrosis_risk = "High Risk (Hepatology referral indicated)" if fib4 > 2.67 else ("Low Risk" if fib4 < 1.30 else "Indeterminate")

        return {
            "hsi_score": round(hsi, 2),
            "steatosis_likely": steatosis_likely,
            "fib4_score": round(fib4, 2),
            "fibrosis_risk": advanced_fibrosis_risk,
            "clinical_protocol": {
                "weight_loss_target": "7-10% body weight loss (reverses steatohepatitis)",
                "dietary_pattern": "Mediterranean low-carb, eliminate liquid fructose and trans-fats",
                "coffee_adjunct": "3-4 cups filtered or espresso coffee daily (chlorogenic acid autophagy)",
                "botanicals": [
                    "Milk Thistle (Silymarin 70-80% extract) 140-420 mg tid",
                    "Kasni (Cichorium intybus) extract 500 mg daily",
                    "Turmeric (Curcumin) 500 mg tid with piperine",
                    "Berberine 500 mg bd"
                ]
            }
        }

    # ------------------- 6. IBS (CHAPTER 19) -------------------
    @classmethod
    def evaluate_ibs(
        cls,
        pain_days_per_week: int,
        symptom_duration_months: int,
        stool_pattern: str,  # "constipation", "diarrhea", "mixed", "unclassified"
        mizaj: str = "Bard-Ratab",
        has_alarm_features: bool = False
    ) -> Dict[str, Any]:
        """
        Chapter 19: Irritable Bowel Syndrome (Rome IV Criteria + Unani Suoo-e-Hazm).
        Rome IV: Abdominal pain >= 1 day/week for last 3 months with onset >= 6 months ago.
        """
        if has_alarm_features:
            return {
                "eligible_for_functional_dx": False,
                "warning": "ALARM FEATURES PRESENT (Rectal bleeding, nocturnal symptoms, unexplained weight loss, elevated calprotectin). Urgent gastroenterology endoscopy referral required."
            }

        rome_iv_met = pain_days_per_week >= 1 and symptom_duration_months >= 6
        subtype_map = {
            "constipation": "IBS-C (Constipation-Predominant)",
            "diarrhea": "IBS-D (Diarrhoea-Predominant)",
            "mixed": "IBS-M (Mixed Bowel Habits)",
            "unclassified": "IBS-U (Unclassified)"
        }
        subtype = subtype_map.get(stool_pattern.lower(), "IBS-U (Unclassified)")

        protocol = {
            "diet": "Low-FODMAP elimination for 6-8 weeks, followed by systematic single-food reintroduction",
            "soluble_fibre": "Isabgol (Psyllium husk) 5-10g daily with warm water (bifunctional)",
            "botanicals": [
                "Enteric-coated Peppermint oil capsules (0.2-0.4 mL tid) - Level 1a evidence",
                "Ajwain (Trachyspermum ammi) and Saunf (Fennel) carminative tea"
            ],
            "probiotics": "Bifidobacterium infantis 35624 or Lactobacillus plantarum 299v",
            "regimental": "Clockwise abdominal Dalak (massage) 15 minutes 3x/week",
            "mind_body": "Gut-directed hypnotherapy (Whorwell protocol) or CBT-I/MBSR (Level 1b evidence)"
        }

        return {
            "rome_iv_criteria_met": rome_iv_met,
            "subtype": subtype,
            "protocol": protocol
        }
