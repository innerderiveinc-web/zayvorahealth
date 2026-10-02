"""
ZAYVORA Health OS™ - Statutory Red-Flag & Emergency Referral Guard
Reference: Book 2: ZAYVORA Clinical Handbook (Part IV, Chapter 3),
Author: Dr. Irfan Ashraf, BUMS.

Absolute clinical safety triage: knowing when NOT to treat is as important as knowing how to treat.
Triggers immediate HARD STOP in Unani prescribing and auto-generates allopathic emergency referral.
"""

from typing import Dict, Any, List, Optional


RED_FLAG_CRITERIA: Dict[str, Dict[str, Any]] = {
    "CARDIAC": {
        "system": "Cardiac",
        "triggers": ["chest pain", "angina", "shortness of breath", "sob", "irregular heartbeat", "arrhythmia", "syncope"],
        "action": "Immediate cardiology referral; do NOT wait. Transfer to nearest cardiac emergency facility.",
        "urgency": "EMERGENCY_STAT",
        "hard_stop": True
    },
    "NEUROLOGICAL": {
        "system": "Neurological",
        "triggers": ["severe sudden headache", "vision changes", "diplopia", "seizures", "unilateral weakness", "slurred speech"],
        "action": "Emergency room referral for acute neuroimaging (CT/MRI stroke/aneurysm screen).",
        "urgency": "EMERGENCY_STAT",
        "hard_stop": True
    },
    "HEPATIC": {
        "system": "Hepatic",
        "triggers": ["jaundice", "scleral icterus", "alt > 300", "sgpt > 300", "ascites", "hepatic encephalopathy", "asterixis"],
        "action": "Immediate hepatologist referral. STOP all hepatotoxic and metabolically demanding herbs immediately.",
        "urgency": "HIGH_URGENT",
        "hard_stop": True
    },
    "RENAL": {
        "system": "Renal",
        "triggers": ["creatinine > 2.0", "oliguria", "anuria", "severe facial/pedal edema", "gross hematuria"],
        "action": "Urgent nephrologist referral. Stop all mineral preparations, Kushtas, and high-potassium herbs.",
        "urgency": "HIGH_URGENT",
        "hard_stop": True
    },
    "ENDOCRINE": {
        "system": "Endocrine",
        "triggers": ["uncontrolled diabetes", "fbs > 250", "hba1c > 11", "diabetic ketoacidosis", "thyroid crisis", "thyroid storm"],
        "action": "Immediate endocrinologist co-management. Insulin or antithyroid drug therapy mandatory.",
        "urgency": "HIGH_URGENT",
        "hard_stop": True
    },
    "PSYCHIATRIC": {
        "system": "Psychiatric",
        "triggers": ["suicidal ideation", "suicidal thoughts", "intent to self harm", "active psychosis", "hallucinations", "phq-9 >= 20"],
        "action": "Emergency psychiatric evaluation. Ensure 24-hour family observation. Contact suicide prevention hotline.",
        "urgency": "EMERGENCY_STAT",
        "hard_stop": True
    },
    "ONCOLOGICAL": {
        "system": "Oncological",
        "triggers": ["unexplained rapid weight loss", "palpable breast mass", "testicular mass", "postmenopausal bleeding", "hemoptysis"],
        "action": "Immediate oncology workup (biopsy, PET-CT, specialist consultation). Unani cannot treat undiagnosed masses.",
        "urgency": "HIGH_URGENT",
        "hard_stop": True
    },
    "SURGICAL_ABDOMINAL": {
        "system": "Surgical Gastrointestinal",
        "triggers": ["rebound tenderness", "rigid abdomen", "board-like abdomen", "hematemesis", "vomiting blood", "melena", "black tarry stool", "qai-ud-dam", "ghait-e-aswad", "acute appendicitis", "bowel obstruction"],
        "action": "Emergency surgical evaluation. Suspected acute peritonitis, active upper GI hemorrhage, or obstruction. Nil per os (NPO) STAT.",
        "urgency": "EMERGENCY_STAT",
        "hard_stop": True
    },
    "RESPIRATORY_CRITICAL": {
        "system": "Respiratory Emergency",
        "triggers": ["spo2 < 90", "severe hypoxemia", "stridor", "massive hemoptysis", "nafs-ud-dam", "cyanosis", "respiratory distress"],
        "action": "Immediate emergency room transfer for supplemental oxygen, airway stabilization, and emergency pulmonary assessment.",
        "urgency": "EMERGENCY_STAT",
        "hard_stop": True
    },
    "SEPSIS_ANAPHYLAXIS": {
        "system": "Sepsis & Anaphylaxis",
        "triggers": ["anaphylaxis", "angioedema", "stridor with hives", "septic shock", "fever with rigors and hypotension", "altered mental state with high fever"],
        "action": "Emergency resuscitation pathway (STAT Epinephrine for anaphylaxis / IV fluids and broad-spectrum therapy for septic shock).",
        "urgency": "EMERGENCY_STAT",
        "hard_stop": True
    }
}


class EmergencyRedFlagGuard:
    """Triage safety engine evaluating patient records for mandatory specialist referral."""

    @classmethod
    def screen_patient_for_red_flags(
        cls,
        symptoms: List[str],
        labs: Optional[Dict[str, Any]] = None,
        notes: str = ""
    ) -> Dict[str, Any]:
        """
        Screens presenting symptoms, laboratory biomarkers, and clinical notes for red flags.
        """
        detected_flags = []
        full_text = (" ".join(symptoms) + " " + notes).lower()
        labs = labs or {}

        # 1. Check Symptom & Text Triggers
        for sys_key, crit in RED_FLAG_CRITERIA.items():
            for trig in crit["triggers"]:
                if trig in full_text:
                    detected_flags.append({
                        "system": crit["system"],
                        "triggered_by": f"Keyword '{trig}' in clinical presentation",
                        "action_required": crit["action"],
                        "urgency": crit["urgency"]
                    })
                    break

        # 2. Check Objective Lab Triggers
        alt = labs.get("alt") or labs.get("sgpt")
        if alt is not None:
            try:
                if float(alt) > 300.0:
                    detected_flags.append({
                        "system": "Hepatic",
                        "triggered_by": f"Objective ALT/SGPT = {alt} U/L (>300 U/L threshold)",
                        "action_required": "Hepatologist referral. Discontinue all oral Unani preparations.",
                        "urgency": "HIGH_URGENT"
                    })
            except ValueError:
                pass

        creat = labs.get("creatinine") or labs.get("serum_creatinine")
        if creat is not None:
            try:
                if float(creat) > 2.0:
                    detected_flags.append({
                        "system": "Renal",
                        "triggered_by": f"Objective Serum Creatinine = {creat} mg/dL (>2.0 mg/dL threshold)",
                        "action_required": "Urgent nephrologist referral. Rule out acute kidney injury or chronic renal failure.",
                        "urgency": "HIGH_URGENT"
                    })
            except ValueError:
                pass

        fbs = labs.get("fbs") or labs.get("fasting_glucose")
        if fbs is not None:
            try:
                if float(fbs) > 250.0:
                    detected_flags.append({
                        "system": "Endocrine",
                        "triggered_by": f"Objective Fasting Blood Sugar = {fbs} mg/dL (>250 mg/dL critical limit)",
                        "action_required": "Endocrinologist referral for emergency glycemic control.",
                        "urgency": "HIGH_URGENT"
                    })
            except ValueError:
                pass

        phq9 = labs.get("phq9") or labs.get("phq_9")
        if phq9 is not None:
            try:
                if float(phq9) >= 20.0:
                    detected_flags.append({
                        "system": "Psychiatric",
                        "triggered_by": f"PHQ-9 score = {phq9} (Severe Depression / Self-harm risk)",
                        "action_required": "Psychiatric emergency evaluation. Unani nervines cannot replace emergency crisis care.",
                        "urgency": "EMERGENCY_STAT"
                    })
            except ValueError:
                pass

        spo2 = labs.get("spo2") or labs.get("oxygen_saturation")
        if spo2 is not None:
            try:
                if float(spo2) < 90.0:
                    detected_flags.append({
                        "system": "Respiratory Emergency",
                        "triggered_by": f"Objective SpO2 = {spo2}% (<90% Critical Hypoxemia)",
                        "action_required": "Immediate oxygen therapy and emergency pulmonary/ER transfer.",
                        "urgency": "EMERGENCY_STAT"
                    })
            except ValueError:
                pass

        hb = labs.get("hemoglobin") or labs.get("hb")
        if hb is not None:
            try:
                if float(hb) < 7.0:
                    detected_flags.append({
                        "system": "Hematological Emergency",
                        "triggered_by": f"Objective Hemoglobin = {hb} g/dL (<7.0 g/dL Severe Anemia / Hemorrhage threshold)",
                        "action_required": "Immediate transfusion medicine & hematology evaluation. STOP all outpatient herbal trials.",
                        "urgency": "EMERGENCY_STAT"
                    })
            except ValueError:
                pass

        has_hard_stop = len(detected_flags) > 0

        return {
            "is_safe_for_unani_care": not has_hard_stop,
            "decision": "PROCEED WITH CLINICAL CONTINUUM" if not has_hard_stop else "EMERGENCY HARD STOP - REFERRAL MANDATORY",
            "detected_red_flags": detected_flags,
            "referral_dossier_required": has_hard_stop,
            "statutory_note": "Per ZAYVORA Clinical Handbook Book 2 Chapter 3: In the presence of red flags, treatment must not be initiated or continued without specialist allopathic co-management."
        }
