"""
ZAYVORA Health OS™ — Functional Diagnostics & Lab Integration Engine
Source: Dr. Irfan Ashraf — CP-AFUM Textbook Chapter 3 & Table 3.1
Encodes:
- 3-tier functional lab interpretation: Optimal vs. Suboptimal vs. Pathological
- The 5 Non-Negotiable Lab Trigger Rules
- Table 3.3 Semen Analysis Reference (WHO 6th Edition vs ZAYVORA Functional Optimal)
- Table 6.1 Mandatory Referral Thresholds (Red Flags)
"""
from typing import Dict, Any, List, Optional

FUNCTIONAL_LAB_RANGES = {
    "TSH": {
        "unit": "mIU/L",
        "standard_range": (0.4, 4.5),
        "functional_optimal": (0.5, 2.5),
        "action_threshold": 2.5,
        "trigger_message": "TSH >2.5 in symptomatic patient = subclinical hypothyroid. Trigger: ThyroMet Axis protocol."
    },
    "Free_T3": {
        "unit": "pg/mL",
        "standard_range": (2.3, 4.2),
        "functional_optimal": (3.0, 4.0),
        "action_threshold_low": 3.0,
        "trigger_message": "Free T3 <3.0 indicates peripheral T4->T3 conversion failure (hepatic deiodinase impairment)."
    },
    "Free_T4": {
        "unit": "ng/dL",
        "standard_range": (0.8, 1.8),
        "functional_optimal": (1.0, 1.5),
        "trigger_message": "Free T4 assesses gland output vs peripheral conversion."
    },
    "Anti_TPO": {
        "unit": "IU/mL",
        "standard_range": (0, 35),
        "functional_optimal": (0, 20),
        "action_threshold": 35,
        "referral_threshold": 300,
        "trigger_message": "Anti-TPO >35 indicates Hashimoto's autoimmune thyroiditis (add Selenium 200mcg). >300 requires endocrinology referral."
    },
    "HbA1c": {
        "unit": "%",
        "standard_range": (4.0, 5.6),
        "functional_optimal": (4.0, 5.4),
        "action_threshold": 5.4,
        "referral_threshold": 10.0,
        "trigger_message": "HbA1c 5.4-5.7% is ZAYVORA pre-diabetic action zone."
    },
    "Fasting_Insulin": {
        "unit": "uIU/mL",
        "standard_range": (2, 25),
        "functional_optimal": (3, 8),
        "action_threshold": 10,
        "trigger_message": "Fasting Insulin >10 uIU/mL indicates early/hidden insulin resistance. Trigger: MetaboCore Elite."
    },
    "SGPT_ALT": {
        "unit": "U/L",
        "standard_range": (7, 56),
        "functional_optimal": (0, 25),
        "action_threshold": 45,
        "referral_threshold": 100,
        "trigger_message": "SGPT >45 U/L mandates Phase 1 (LiverPrime Core) before any axis-specific correction. >100 requires hepatology referral."
    },
    "hs_CRP": {
        "unit": "mg/L",
        "standard_range": (0, 3.0),
        "functional_optimal": (0, 1.0),
        "action_threshold": 3.0,
        "trigger_message": "hs-CRP >3 mg/L mandates Phase 1 systemic anti-inflammatory protocol."
    },
    "AMH": {
        "unit": "ng/mL",
        "standard_range": (1.0, 3.5),
        "functional_optimal": (1.5, 3.5),
        "action_threshold_low": 1.0,
        "referral_threshold_low": 0.3,
        "action_threshold_high": 3.5,
        "trigger_message": "AMH <1.0 indicates diminished reserve (<0.3 reproductive referral). AMH >3.5 indicates PCOS follicle arrest."
    },
    "Serum_Creatinine": {
        "unit": "mg/dL",
        "standard_range": (0.7, 1.3),
        "functional_optimal": (0.8, 1.1),
        "action_threshold": 1.3,
        "referral_threshold": 2.0,
        "trigger_message": "Creatinine >1.3 mg/dL indicates impaired glomerular clearance. Trigger: UroClear renal axis."
    },
    "Uric_Acid": {
        "unit": "mg/dL",
        "standard_range": (3.5, 7.2),
        "functional_optimal": (3.5, 5.5),
        "action_threshold": 6.5,
        "referral_threshold": 9.0,
        "trigger_message": "Uric acid >6.5 mg/dL indicates hyperuricemia / Niqris (gout) risk. Trigger: JointEase & Mudirr-e-Baul."
    },
    "Triglycerides": {
        "unit": "mg/dL",
        "standard_range": (0, 150),
        "functional_optimal": (50, 100),
        "action_threshold": 150,
        "referral_threshold": 500,
        "trigger_message": "Triglycerides >150 mg/dL indicates hepatic de novo lipogenesis & Balgham-e-Dasami. Trigger: LipidClear."
    },
    "LDL_Cholesterol": {
        "unit": "mg/dL",
        "standard_range": (0, 100),
        "functional_optimal": (50, 90),
        "action_threshold": 130,
        "referral_threshold": 190,
        "trigger_message": "LDL-C >130 mg/dL mandates cardiovascular vascular endothelium protection. Trigger: CardioGuard."
    },
    "Hemoglobin": {
        "unit": "g/dL",
        "standard_range": (12.0, 16.5),
        "functional_optimal": (13.0, 15.5),
        "action_threshold_low": 11.5,
        "referral_threshold_low": 8.0,
        "trigger_message": "Hb <11.5 g/dL indicates Faqr-ud-Dam / Anemia. Trigger: Kushta Faulad & nutritive iron co-factors."
    },
    "Serum_Ferritin": {
        "unit": "ng/mL",
        "standard_range": (15, 200),
        "functional_optimal": (50, 120),
        "action_threshold_low": 30,
        "trigger_message": "Ferritin <30 ng/mL indicates depleted marrow iron stores (Su-ul-Qinya)."
    },
    "Total_Bilirubin": {
        "unit": "mg/dL",
        "standard_range": (0.2, 1.2),
        "functional_optimal": (0.4, 0.9),
        "action_threshold": 1.5,
        "referral_threshold": 3.0,
        "trigger_message": "Total Bilirubin >1.5 mg/dL indicates impaired biliary excretion (Yarqan). Phase 1 LiverPrime mandatory."
    }
}


def calculate_homa_ir(fasting_glucose_mg_dl: float, fasting_insulin_miu_l: float) -> Dict[str, Any]:
    """
    Computes HOMA-IR = (Glucose * Insulin) / 405.
    Optimal: <1.5
    Early Resistance: >2.0
    Moderate Resistance: >3.0
    Severe Resistance: >5.0 (Physician co-management)
    """
    homa = round((fasting_glucose_mg_dl * fasting_insulin_miu_l) / 405.0, 2)
    if homa < 1.5:
        status = "OPTIMAL"
        rec = "Excellent insulin sensitivity."
    elif homa <= 2.0:
        status = "BORDERLINE"
        rec = "Monitor glycaemic markers and dietary carbohydrate quality."
    elif homa <= 3.0:
        status = "EARLY_RESISTANCE"
        rec = "Stage 1 Insulin Resistance: initiate MetaboCore Elite + 16:8 IF lifestyle."
    elif homa <= 5.0:
        status = "MODERATE_RESISTANCE"
        rec = "Stage 2 Insulin Resistance: intensive MetaboCore + Berberine protocol."
    else:
        status = "SEVERE_RESISTANCE"
        rec = "Stage 3 Severe IR: physician co-management required."

    return {
        "homa_ir": homa,
        "status": status,
        "clinical_recommendation": rec
    }


def calculate_tg_hdl_ratio(triglycerides: float, hdl: float) -> Dict[str, Any]:
    """
    TG/HDL ratio as non-fasting insulin resistance surrogate marker.
    Optimal: <2.0
    Insulin resistance marker: >3.5
    Severe insulin resistance / atherogenic: >5.0
    """
    if hdl <= 0:
        return {"ratio": None, "status": "INVALID_HDL"}
    ratio = round(triglycerides / hdl, 2)
    if ratio < 2.0:
        status = "OPTIMAL"
        note = "Low atherogenic particle density."
    elif ratio <= 3.5:
        status = "MODERATE"
        note = "Monitor lipid particle size and hepatic VLDL output."
    else:
        status = "INSULIN_RESISTANCE"
        note = "Strong non-fasting surrogate marker for small dense LDL and hepatic insulin resistance."

    return {
        "tg_hdl_ratio": ratio,
        "status": status,
        "clinical_note": note
    }


def evaluate_semen_analysis(params: Dict[str, float]) -> Dict[str, Any]:
    """
    Evaluates semen analysis parameters according to Table 3.3:
    WHO 6th Edition lower limits vs ZAYVORA Functional Optimal Targets.
    """
    findings = []
    actions = []

    vol = params.get("volume_ml")
    if vol is not None:
        if vol < 1.4:
            findings.append("Low volume (<1.4 mL): investigate ejaculatory duct / seminal vesicle.")
        elif vol >= 2.0:
            findings.append("Volume optimal (≥2.0 mL).")

    mot = params.get("total_motility_pct")
    if mot is not None:
        if mot < 42:
            findings.append("Asthenozoospermia (total motility <42%): mitochondrial energy failure.")
            actions.append("Full ManiVital Pro Phase 2 protocol (CoQ10 Ubiquinol 200-300mg + L-Carnitine 1.5g).")
        elif mot >= 55:
            findings.append("Total motility in ZAYVORA optimal range (≥55%).")

    conc = params.get("concentration_million_ml")
    if conc is not None:
        if conc == 0:
            findings.append("Azoospermia (0 sperm): IMMEDIATE urology / reproductive medicine referral.")
            actions.append("RED FLAG: Azoospermia requires structural/genetic investigation. Not a ZAYVORA solo case.")
        elif conc < 16:
            findings.append("Oligozoospermia (<16 M/mL): suppressed spermatogenesis.")
            actions.append("Full Liver-Testicular Axis protocol (ManiVital Pro + LiverPrime Core Phase 1).")
        elif conc >= 40:
            findings.append("Concentration in ZAYVORA optimal fertility range (≥40 M/mL).")

    morph = params.get("morphology_kruger_pct")
    if morph is not None:
        if morph < 4:
            findings.append("Teratozoospermia (morphology <4% Kruger strict): high oxidative sperm burden.")
            actions.append("Antioxidant priority: Selenium 200mcg + CoQ10 + Tabasheer silica buffering.")

    dfi = params.get("dfi_pct")
    if dfi is not None:
        if dfi > 25:
            findings.append("High DNA Fragmentation Index (>25%): sperm DNA integrity compromised.")
            actions.append("Intense 90-day Muhafiz Stack + thermal management (no hot baths/laptops) + zero alcohol.")
        elif dfi < 15:
            findings.append("DFI optimal (<15%): high natural conception integrity.")

    return {
        "parameters_analyzed": params,
        "findings": findings,
        "protocol_actions": actions
    }


def evaluate_five_non_negotiable_lab_trigger_rules(labs: Dict[str, float], symptoms: List[str] = None) -> Dict[str, Any]:
    """
    Executes the 5 Non-Negotiable Lab Trigger Rules from CP-AFUM Textbook Section 3.5.
    Returns mandatory actions, phase mandates, and referral flags.
    """
    symptoms = symptoms or []
    triggers = []
    referrals = []
    phase_1_mandatory = False

    sgpt = labs.get("sgpt", labs.get("alt", labs.get("SGPT", labs.get("ALT"))))
    crp = labs.get("hs_crp", labs.get("crp", labs.get("hsCRP", labs.get("CRP"))))
    tsh = labs.get("tsh", labs.get("TSH"))
    insulin = labs.get("fasting_insulin", labs.get("insulin", labs.get("Fasting_Insulin")))
    anti_tpo = labs.get("anti_tpo", labs.get("antiTPO", labs.get("Anti_TPO")))
    amh = labs.get("amh", labs.get("AMH"))
    hba1c = labs.get("hba1c", labs.get("HbA1c"))

    # Rule 1: SGPT > 45 U/L
    if sgpt is not None:
        if sgpt > 100:
            referrals.append("MANDATORY REFERRAL: SGPT >100 U/L indicates acute hepatopathy or severe hepatitis. Hepatology referral mandatory — do not solo-manage.")
        elif sgpt > 45:
            phase_1_mandatory = True
            triggers.append({
                "rule": "Rule 1 (SGPT Trigger)",
                "finding": f"SGPT = {sgpt} U/L (>45 U/L)",
                "action": "Phase 1 (LiverPrime Core) is MANDATORY before any axis-specific correction. No exceptions."
            })

    # Rule 2: hs-CRP > 3 mg/L
    if crp is not None and crp > 3.0:
        phase_1_mandatory = True
        triggers.append({
            "rule": "Rule 2 (hs-CRP Trigger)",
            "finding": f"hs-CRP = {crp} mg/L (>3.0 mg/L)",
            "action": "Phase 1 mandatory — systemic inflammation impairs receptor sensitivity for herbal actives."
        })

    # Rule 3: TSH > 2.5 mIU/L (symptomatic)
    if tsh is not None:
        if tsh > 10.0:
            referrals.append("MANDATORY REFERRAL: TSH >10 mIU/L indicates overt hypothyroidism. Endocrinology co-management required.")
        elif tsh > 2.5 and any(s.lower() in ["fatigue", "cold", "weight", "constipation", "brain fog"] for s in symptoms):
            triggers.append({
                "rule": "Rule 3 (TSH Subclinical Trigger)",
                "finding": f"TSH = {tsh} mIU/L (>2.5) with hypothyroid symptoms",
                "action": "Initiate ThyroMet Axis protocol immediately — do not watchfully wait in symptomatic patients."
            })

    # Rule 4: Fasting Insulin > 10 uIU/mL
    if insulin is not None and insulin > 10.0:
        triggers.append({
            "rule": "Rule 4 (Fasting Insulin IR Trigger)",
            "finding": f"Fasting Insulin = {insulin} uIU/mL (>10 uIU/mL)",
            "action": "Initiate MetaboCore Elite protocol — Stage 1 early insulin resistance detected before HbA1c elevation."
        })

    # Rule 5: Anti-TPO > 300 IU/mL or SGPT > 100
    if anti_tpo is not None:
        if anti_tpo > 300:
            referrals.append("MANDATORY REFERRAL: Anti-TPO >300 IU/mL indicates aggressive Hashimoto's autoimmune thyroiditis. Endocrinology specialist referral required.")
        elif anti_tpo > 35:
            triggers.append({
                "rule": "Rule 5A (Hashimoto Immune Modulation)",
                "finding": f"Anti-TPO = {anti_tpo} IU/mL (>35 IU/mL)",
                "action": "Add Selenium 200mcg/day to reduce Anti-TPO titers. Do NOT supplement iodine."
            })

    # Red Flag: AMH < 0.3
    if amh is not None and amh < 0.3:
        referrals.append("REFERRAL RECOMMENDED: AMH <0.3 ng/mL indicates critically diminished ovarian reserve. Reproductive endocrinology / IVF pathway discussion required.")

    # Red Flag: HbA1c > 10%
    if hba1c is not None and hba1c > 10.0:
        referrals.append("MANDATORY REFERRAL: HbA1c >10% indicates uncontrolled severe diabetes. Endocrinology co-management required.")

    return {
        "phase_1_mandatory": phase_1_mandatory,
        "triggered_rules": triggers,
        "specialist_referrals": referrals,
        "requires_referral": len(referrals) > 0
    }


def verify_humoral_biomarker_correlation(
    suspected_humor_or_condition: str,
    labs: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Closed-Loop Biomarker Integration Algorithm (Part One Chapter 8).
    Maps classical Unani clinical assessment directly to modern laboratory panels,
    creating an objective validation and monitoring loop.
    """
    query = suspected_humor_or_condition.upper()
    confirmations = []
    contradictions = []

    # 1. Ghalba-e-Balgham (Phlegm Dominance / Cold-Moist Metabolic Sluggishness)
    if "BALGHAM" in query:
        insulin = labs.get("fasting_insulin") or labs.get("insulin")
        tsh = labs.get("tsh") or labs.get("TSH")
        ldl = labs.get("ldl") or labs.get("LDL")
        bmi = labs.get("bmi") or labs.get("BMI")
        homa_ir = labs.get("homa_ir")

        if insulin and float(insulin) > 12.0:
            confirmations.append(f"Fasting insulin {insulin} uIU/mL >12 confirms Balghami metabolic congestion.")
        if tsh and float(tsh) > 2.5:
            confirmations.append(f"TSH {tsh} mIU/L >2.5 confirms hypothyroid metabolic slowing (Barid-Ratab).")
        if ldl and float(ldl) > 100.0:
            confirmations.append(f"LDL {ldl} mg/dL >100 confirms lipid accumulation.")
        if homa_ir and float(homa_ir) > 2.0:
            confirmations.append(f"HOMA-IR {homa_ir} >2.0 confirms cellular insulin resistance.")
        if bmi and float(bmi) > 25.0:
            confirmations.append(f"BMI {bmi} indicates phlegmatic tissue accumulation.")

    # 2. Ghalba-e-Safra (Bile / Inflammatory Overdrive)
    elif "SAFRA" in query:
        crp = labs.get("hs_crp") or labs.get("crp") or labs.get("hsCRP")
        alt = labs.get("alt") or labs.get("sgpt")
        ast = labs.get("ast") or labs.get("sgot")
        bili = labs.get("bilirubin") or labs.get("total_bilirubin")

        if crp and float(crp) > 1.0:
            confirmations.append(f"hsCRP {crp} mg/L >1.0 confirms Safravi inflammatory overdrive.")
        if alt and float(alt) > 30.0:
            confirmations.append(f"ALT/SGPT {alt} U/L >30 confirms hepatic inflammatory stress.")
        if ast and float(ast) > 30.0:
            confirmations.append(f"AST/SGOT {ast} U/L >30 confirms cellular heat damage.")
        if bili and float(bili) > 1.0:
            confirmations.append(f"Bilirubin {bili} mg/dL confirms biliary congestion.")

    # 3. Ghalba-e-Sauda (Black Bile / Oxidative Stress & Neuro-Adrenal)
    elif "SAUDA" in query:
        cortisol = labs.get("cortisol") or labs.get("morning_cortisol")
        homocysteine = labs.get("homocysteine")
        dhea = labs.get("dhea_s") or labs.get("dhea")

        if cortisol and float(cortisol) > 18.0:
            confirmations.append(f"Morning Cortisol {cortisol} mcg/dL confirms hyperactive HPA Sauda axis.")
        if homocysteine and float(homocysteine) > 11.0:
            confirmations.append(f"Homocysteine {homocysteine} umol/L confirms methylation/oxidative strain.")
        if dhea and float(dhea) < 120.0:
            confirmations.append(f"DHEA-S {dhea} confirms adrenal reserve depletion.")
        mda = labs.get("mda") or labs.get("malondialdehyde")
        if mda and float(mda) > 2.5:
            confirmations.append(f"MDA {mda} nmol/mL confirms lipid peroxidation and oxidative sawdawi cellular damage.")

    # 4. Ghalba-e-Dam (Blood Plethora / Vascular Congestion)
    elif "DAM" in query:
        hct = labs.get("hematocrit") or labs.get("pcv")
        plt = labs.get("platelets")
        sbp = labs.get("systolic_bp") or labs.get("bp_systolic")

        if hct and float(hct) > 48.0:
            confirmations.append(f"Hematocrit {hct}% >48% confirms Damawi plethora.")
        if plt and float(plt) > 350.0:
            confirmations.append(f"Platelets {plt}k indicates hypercoagulable vascular state.")
        if sbp and float(sbp) > 130.0:
            confirmations.append(f"Blood pressure {sbp} mmHg indicates vascular volume tension.")

    # 5. Zof-e-Quwwat-e-Mani (Male Reproductive / Seminal Depletion)
    elif "MANI" in query or "SPERM" in query or "TESTIS" in query:
        sperm_count = labs.get("sperm_count")
        motility = labs.get("motility") or labs.get("progressive_motility")
        testo = labs.get("testosterone") or labs.get("total_testosterone")

        if sperm_count and float(sperm_count) < 15.0:
            confirmations.append(f"Sperm count {sperm_count} M/mL (<15 M/mL) confirms Zof-e-Quwwat-e-Mani.")
        if motility and float(motility) < 40.0:
            confirmations.append(f"Progressive motility {motility}% (<40%) confirms mitochondrial asthenospermia.")
        if testo and float(testo) < 400.0:
            confirmations.append(f"Total testosterone {testo} ng/dL (<400) confirms Leydig Quwwat deficit.")

    is_confirmed = len(confirmations) >= 1

    return {
        "humor_evaluated": suspected_humor_or_condition,
        "is_biomarker_confirmed": is_confirmed,
        "correlation_status": "CONFIRMED_BY_BIOMARKERS" if len(confirmations) >= 2 else ("PARTIALLY_CORRELATED" if len(confirmations) == 1 else "UNCONFIRMED_OR_DISCORDANT"),
        "confirmations": confirmations,
        "contradictions": contradictions,
        "closed_loop_recommendation": "PROCEED WITH PHASED AFAAL CASCADE" if is_confirmed else "FURTHER FUNCTIONAL LAB MAPPING RECOMMENDED"
    }
