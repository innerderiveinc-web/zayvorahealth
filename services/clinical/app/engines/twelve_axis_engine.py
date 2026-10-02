"""
ZAYVORA Health OS™ - 12-Axis Clinical Intelligence Engine™
Proposed Proprietary Clinical Architecture; advisory decision-support layer,
not a replacement for clinician-validated diagnosis.

Implements:
  1. Axis Activity Index Weighted Formula:
     Score = (0.25 * Symptoms) + (0.20 * History) + (0.30 * Labs) + (0.10 * Lifestyle) + (0.15 * Clinician)
  2. Safe Clinical Status Labels:
     - Not Assessed
     - Low Concern (Routine wellness monitoring)
     - Moderate Concern (Clinician review recommended)
     - High Concern (Priority assessment)
     - Red Flag (Immediate referral/urgent care pathway)
  3. Patient 360 12-Axis Health Map Generation
  4. Hakeem Sahab AI Copilot Draft Summary (strictly advisory, clinician-in-the-loop)
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

# Reference the canonical 12-Axis knowledge schema
from services.knowledge.app.data.organ_axes_12_schema import ORGAN_AXES_12


class TwelveAxisEngine:
    """
    Runtime operational engine evaluating and monitoring the 12 Organ-Axis systems
    for patient profiles and doctor cockpits.
    """

    STATUS_NOT_ASSESSED = "Not Assessed"
    STATUS_LOW = "Low Concern"
    STATUS_MODERATE = "Moderate Concern"
    STATUS_HIGH = "High Concern"
    STATUS_RED_FLAG = "Red Flag"

    @classmethod
    def calculate_single_axis_activity(
        cls,
        axis_id: str,
        symptoms_score: float,       # 0 - 100
        history_score: float,        # 0 - 100
        investigations_score: float, # 0 - 100
        lifestyle_score: float,      # 0 - 100
        clinician_assessment: Optional[float] = None, # 0 - 100
        has_red_flags: bool = False
    ) -> Dict[str, Any]:
        """
        Calculates the safe Axis Activity Index according to the defined formula:
          Index = (0.25 * Symptoms) + (0.20 * History) + (0.30 * Labs) + (0.10 * Lifestyle) + (0.15 * Clinician)
        """
        axis_def = ORGAN_AXES_12.get(axis_id.upper())
        axis_name = axis_def["axis_name"] if axis_def else axis_id

        # If clinician assessment is not provided yet, scale the other weights to 1.0
        if clinician_assessment is None:
            raw_score = (
                (0.25 * symptoms_score) +
                (0.20 * history_score) +
                (0.30 * investigations_score) +
                (0.10 * lifestyle_score)
            ) / 0.85
            clinician_status = "Pending Clinician Review"
        else:
            raw_score = (
                (0.25 * symptoms_score) +
                (0.20 * history_score) +
                (0.30 * investigations_score) +
                (0.10 * lifestyle_score) +
                (0.15 * clinician_assessment)
            )
            clinician_status = "Clinician Validated"

        activity_index = round(min(max(raw_score, 0.0), 100.0), 1)

        # Status categorization
        if has_red_flags:
            status = cls.STATUS_RED_FLAG
            ui_meaning = "Immediate referral / urgent care pathway"
        elif activity_index >= 65.0:
            status = cls.STATUS_HIGH
            ui_meaning = "Priority clinical assessment indicated"
        elif activity_index >= 35.0:
            status = cls.STATUS_MODERATE
            ui_meaning = "Clinician review recommended"
        elif activity_index >= 10.0:
            status = cls.STATUS_LOW
            ui_meaning = "Routine wellness monitoring"
        else:
            status = cls.STATUS_NOT_ASSESSED
            ui_meaning = "Baseline / data collection in progress"

        return {
            "axis_id": axis_id.upper(),
            "axis_name": axis_name,
            "activity_index": activity_index,
            "status": status,
            "ui_meaning": ui_meaning,
            "clinician_status": clinician_status,
            "breakdown": {
                "symptoms_weight_25": round(0.25 * symptoms_score, 1),
                "history_weight_20": round(0.20 * history_score, 1),
                "investigations_weight_30": round(0.30 * investigations_score, 1),
                "lifestyle_weight_10": round(0.10 * lifestyle_score, 1),
                "clinician_weight_15": round(0.15 * (clinician_assessment or 0.0), 1)
            },
            "foundational_core_links": axis_def.get("foundational_core_links", []) if axis_def else []
        }

    @classmethod
    def generate_patient_360_axis_map(
        cls,
        patient_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generates the complete 12-Axis Health Map for Patient 360 view.
        Ensures all 12 axes are accounted for without false disease diagnoses.
        """
        patient_id = patient_data.get("patient_id", "ANON-001")
        mizaj = patient_data.get("mizaj", "Mutadil")
        axis_inputs = patient_data.get("axes", {})

        evaluated_axes = []
        high_concern_axes = []
        red_flag_axes = []

        for axis_id, axis_meta in ORGAN_AXES_12.items():
            input_val = axis_inputs.get(axis_id, {})
            if input_val:
                res = cls.calculate_single_axis_activity(
                    axis_id=axis_id,
                    symptoms_score=float(input_val.get("symptoms_score", 0)),
                    history_score=float(input_val.get("history_score", 0)),
                    investigations_score=float(input_val.get("investigations_score", 0)),
                    lifestyle_score=float(input_val.get("lifestyle_score", 0)),
                    clinician_assessment=input_val.get("clinician_assessment"),
                    has_red_flags=bool(input_val.get("has_red_flags", False))
                )
            else:
                res = {
                    "axis_id": axis_id,
                    "axis_name": axis_meta["axis_name"],
                    "activity_index": 0.0,
                    "status": cls.STATUS_NOT_ASSESSED,
                    "ui_meaning": "Data missing / not assessed",
                    "clinician_status": "Not Assessed",
                    "breakdown": {},
                    "foundational_core_links": axis_meta.get("foundational_core_links", [])
                }

            evaluated_axes.append(res)
            if res["status"] == cls.STATUS_RED_FLAG:
                red_flag_axes.append(res["axis_name"])
            elif res["status"] in [cls.STATUS_HIGH, cls.STATUS_MODERATE]:
                high_concern_axes.append(res["axis_name"])

        return {
            "patient_id": patient_id,
            "mizaj": mizaj,
            "evaluation_timestamp": datetime.utcnow().isoformat() + "Z",
            "framework_notice": "ZAYVORA 12-Axis Clinical Intelligence Framework™ — Proposed Proprietary Clinical Architecture; advisory decision-support layer, not a replacement for clinician-validated diagnosis.",
            "total_axes_evaluated": len([a for a in evaluated_axes if a["status"] != cls.STATUS_NOT_ASSESSED]),
            "red_flags_present": len(red_flag_axes) > 0,
            "red_flag_axes": red_flag_axes,
            "priority_axes": high_concern_axes,
            "axes": evaluated_axes
        }

    @classmethod
    def generate_hakeem_sahab_ai_draft(
        cls,
        patient_summary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generates an advisory AI copilot draft for the clinician.
        Strictly observes ethical boundaries: NO autonomous prescriptions or final diagnoses.
        """
        symptoms = patient_summary.get("reported_symptoms", [])
        biomarkers = patient_summary.get("biomarkers", {})
        mizaj = patient_summary.get("mizaj", "Mutadil")

        relevant_axes = []
        supporting_observations = []
        missing_info = []
        red_flags_flagged = []

        # Analyze symptoms for Gut-Liver
        if any(s in [sym.lower() for sym in symptoms] for s in ["bloating", "constipation", "acidity", "indigestion", "gas"]):
            relevant_axes.append({"axis": "Gut–Liver Axis", "recommendation": "Assessment indicated based on reported digestive discomfort"})
            supporting_observations.append("Digestive symptoms matching Su-e-Hazm pattern")

        # Analyze biomarkers for Metabolic-Pancreatic
        fbg = biomarkers.get("fbg", 0)
        hba1c = biomarkers.get("hba1c", 0)
        if hba1c >= 5.7 or fbg >= 100:
            relevant_axes.append({"axis": "Metabolic–Pancreatic Axis", "recommendation": "Further investigation indicated (Elevated glycemic indicators)"})
            supporting_observations.append(f"Fasting glucose {fbg} mg/dL, HbA1c {hba1c}%")

        # Check for missing data
        if "medication_history" not in patient_summary:
            missing_info.append("Complete current medication and herbal supplement history")
        if not biomarkers:
            missing_info.append("Relevant baseline laboratory reports (CBC, LFT, Metabolic panel)")
        if "symptom_duration" not in patient_summary:
            missing_info.append("Exact symptom duration and progression trajectory")

        return {
            "ai_copilot": "Hakeem Sahab AI Draft Generator",
            "clinical_status": "DRAFT - Requires Clinician Review & Edit",
            "possible_relevant_axes": relevant_axes,
            "supporting_observations": supporting_observations,
            "missing_information": missing_info,
            "safety_summary": {
                "clinician_review_required": True,
                "autonomous_prescription_prevented": True,
                "red_flags": red_flags_flagged
            },
            "advisory_notice": "This draft is generated by Hakeem Sahab AI as clinical decision support. The licensed treating physician must independently confirm all findings and approve any care plan."
        }
