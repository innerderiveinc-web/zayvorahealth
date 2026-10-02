"""
ZAYVORA Health OS™ — Patient 360 Time-Aware Aggregate Engine
============================================================
Reference:
  - Blueprint §13 (Patient 360 Implementation)
  - 10 Enterprise Panels:
      1. Identity + Consent
      2. Problems
      3. Mizaj
      4. 12-Axis Map
      5. Investigations
      6. Care Plan
      7. Nuskha (Versioned)
      8. Pharmacy
      9. Outcomes
      10. AI Activity
"""

from typing import Dict, Any, List, Optional
import datetime

class Patient360Engine:
    """Generates the canonical 10-panel time-aware Patient 360 record."""

    @classmethod
    def build_patient_360(
        cls,
        patient_id: str,
        patient_demographics: Optional[Dict[str, Any]] = None,
        clinical_history: Optional[Dict[str, Any]] = None,
        labs: Optional[Dict[str, Any]] = None,
        mizaj_data: Optional[Dict[str, Any]] = None,
        axis_scores: Optional[Dict[str, Any]] = None,
        active_nuskha: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        demo = patient_demographics or {
            "patient_id": patient_id,
            "name": "Tariq Mahmood",
            "age": 38,
            "gender": "Male",
            "blood_group": "B+",
            "contact": "+91-9876543210",
            "emergency_contact": {"name": "Ayesha Mahmood", "relation": "Spouse", "phone": "+91-9876543211"}
        }

        mizaj = mizaj_data or {
            "current_mizaj": "Balghami (Cold & Moist)",
            "dominant_score": 17,
            "max_score": 18,
            "category": "SIGNIFICANT_DOMINANCE",
            "assessment_instrument": "Z-MAI 6-Domain Quantitative Matrix v2.0",
            "assessment_date": "2026-09-18",
            "clinician_reviewer": "Dr. Irfan Ashraf, BUMS",
            "override_history": []
        }

        # 10 Panels per Blueprint §13
        return {
            "patient_id": patient_id,
            "assembled_at": datetime.datetime.utcnow().isoformat() + "Z",
            "panels": {
                "identity_and_consent": {
                    "demographics": demo,
                    "consent_status": "ACTIVE_INFORMED_CONSENT",
                    "consent_date": "2026-09-18",
                    "consent_version": "DPDP-2025-V1.2",
                    "privacy_controls": {"research_opt_in": True, "telemedicine_opt_in": True, "abdm_linking": True}
                },
                "problems": [
                    {"code": "ICD11-5A11", "name": "Insulin Resistance (HOMA-IR 5.12)", "status": "ACTIVE", "severity": "MODERATE", "identified_on": "2026-09-18"},
                    {"code": "ICD11-5B81", "name": "Subclinical Hypothyroidism (TSH 3.9)", "status": "ACTIVE", "severity": "MILD", "identified_on": "2026-09-18"},
                    {"code": "ICD11-GB04", "name": "Oligoasthenospermia (Zof-e-Mani)", "status": "ACTIVE", "severity": "MODERATE", "identified_on": "2026-09-18"}
                ],
                "mizaj": mizaj,
                "axis_map": axis_scores or {
                    "Jigar-Banas (Hepato-Metabolic)": {"score": 4, "status": "Clinician Review", "trend": "WORSENING", "primary_concern": "Elevated HOMA-IR & LDL"},
                    "Khusyatain-Dam (Male Reproductive)": {"score": 3, "status": "Clinician Review", "trend": "STABLE", "primary_concern": "Asthenospermia"},
                    "Dimagh-Aasab (Neuro-Psychological)": {"score": 2, "status": "Monitoring", "trend": "STABLE", "primary_concern": "Mid-day lethargy"}
                },
                "investigations": labs or {
                    "fasting_glucose": {"value": 114, "unit": "mg/dL", "status": "ABNORMAL_HIGH"},
                    "fasting_insulin": {"value": 18.2, "unit": "uIU/mL", "status": "ABNORMAL_HIGH"},
                    "homa_ir": {"value": 5.12, "unit": "index", "status": "PATHOLOGICAL"},
                    "tsh": {"value": 3.9, "unit": "mIU/L", "status": "SUBCLINICAL_ELEVATED"},
                    "sperm_count": {"value": 11.2, "unit": "M/mL", "status": "SUBOPTIMAL"},
                    "motility": {"value": 28.0, "unit": "%", "status": "SUBOPTIMAL"}
                },
                "care_plan": {
                    "current_phase": "Phase 1: Tanqiya & Istifragh (Cleansing & Evacuation)",
                    "planned_duration_weeks": 4,
                    "target_goals": ["HOMA-IR reduction to <3.0", "TSH stabilization <2.5", "Resolution of daytime lethargy"],
                    "next_scheduled_review": "2026-10-16"
                },
                "nuskha": active_nuskha or {
                    "nuskha_id": f"NSK-{patient_id}-01",
                    "version": 1,
                    "status": "APPROVED",
                    "approved_by": "Dr. Irfan Ashraf, BUMS",
                    "approved_at": "2026-09-18T10:30:00Z",
                    "items": [
                        {"name": "Custom Compounded Safoof (Tanqiya Formula)", "dose": "5g twice daily with warm water", "role": "Core Cleansing"},
                        {"name": "DiabEase™ (Core Line)", "dose": "1 capsule 30 min before lunch & dinner", "role": "Metabolic Reset"}
                    ],
                    "parhez": "MF-01 Balgham Restrictive Protocol (No cold dairy, sugar, or refined carbs)"
                },
                "pharmacy": {
                    "dispensed_batches": [
                        {"item": "Custom Compounded Safoof", "lot_number": "SAF-2026-09-B12", "dispensed_by": "Pharm. Zaid Khan", "date": "2026-09-18", "status": "DISPENSED"},
                        {"item": "DiabEase™", "lot_number": "DBE-2026-08-04", "dispensed_by": "Pharm. Zaid Khan", "date": "2026-09-18", "status": "DISPENSED"}
                    ],
                    "substitutions": []
                },
                "outcomes": {
                    "patient_reported": {"energy_score_baseline": 3, "sleep_quality_baseline": 4, "digestive_comfort": 5},
                    "clinical_improvements": [],
                    "safety_adverse_events": []
                },
                "ai_activity": {
                    "copilot_invocations_count": 2,
                    "case_brief_generated": True,
                    "safety_firewall_status": "PASS_CLEARED",
                    "clinician_override_recorded": False
                }
            }
        }
