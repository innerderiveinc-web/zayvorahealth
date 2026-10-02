"""
ZAYVORA Health OS™ - Regimental Therapy & Thermoregulation Engine
Reference: Chapters 9, 10, 11, 12, 13, 26,
ZAYVORA Global Edition (Second Edition 2026), Dr. Irfan Ashraf, BUMS.

Implements clinical protocols for:
  1. Hammam 3-Phase Graduated Heat Sequence (HSP70/90 induction, GLUT4 upregulation)
  2. ZAYVORA Daily Home Contrast Shower Protocol
  3. Dalak (Therapeutic Massage) Taxonomy & Directional Colonic Protocols
  4. Hijama (Wet Cupping) Safety Verification & Anatomical Site Selection
  5. Seasonal Regimen (Fasl-i-Ilaj) Scheduling
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class RegimentalHydrotherapyEngine:
    """
    Therapeutic engine for non-pharmacological regimental interventions (Ilaj bil Tadbeer).
    Enforces temperature safety thresholds, anatomical mapping, and contraindications.
    """

    # ------------------- 1. HAMMAM PROTOCOLS -------------------
    @classmethod
    def generate_hammam_prescription(
        cls,
        mizaj: str,
        condition: str,
        has_cvd_history: bool = False,
        is_pregnant: bool = False,
        neuropathy_present: bool = False
    ) -> Dict[str, Any]:
        """
        Prescribes 3-Room Classical Unani Hammam thermal sequence.
        Absolute safety checks enforced.
        """
        # Safety screening
        if is_pregnant:
            return {
                "eligible": False,
                "reason": "Absolute contraindication: Hot bath/Hammam contraindicated in pregnancy (hyperthermia teratogenicity risk)."
            }
        if neuropathy_present:
            return {
                "eligible": False,
                "reason": "Absolute contraindication: Severe peripheral neuropathy (burn risk from impaired thermal sensation)."
            }

        max_temp = 38.0 if has_cvd_history else 41.0

        sequence = [
            {
                "phase": 1,
                "chamber": "Bayt al-Awwal (Cool Outer Chamber)",
                "target_temp_c": 22.0,
                "duration_min": 5,
                "action": "Acclimatization, gentle hydration with room temperature electrolyte water"
            },
            {
                "phase": 2,
                "chamber": "Bayt al-Wastani (Warm Intermediate Chamber)",
                "target_temp_c": 32.0,
                "duration_min": 10,
                "action": "Pores dilate, mild perspiration initiation, pre-bath preparatory Dalak (Muaddil)"
            },
            {
                "phase": 3,
                "chamber": "Bayt al-Harara (Hot Inner Steam Chamber)",
                "target_temp_c": max_temp,
                "duration_min": 15 if has_cvd_history else 20,
                "action": "Intense sweating (Istifragh), Heat Shock Protein (HSP70/90) induction, peripheral vasodilation"
            },
            {
                "phase": 4,
                "chamber": "Restorative Cool Down (Return to Bayt al-Wastani)",
                "target_temp_c": 24.0,
                "duration_min": 10,
                "action": "Restorative Dalak (Murieh) with cooling aromatics (rose/sandalwood), rehydration with Kasni/mint tea"
            }
        ]

        return {
            "eligible": True,
            "condition": condition,
            "mizaj": mizaj,
            "max_safe_temperature_c": max_temp,
            "therapeutic_objective": "HSP70-mediated insulin sensitization, lymphatic clearance, and autonomic rebalancing",
            "sequence": sequence,
            "clinical_notes": "Continuous hydration mandatory. Terminate immediately if lightheadedness or palpitations occur."
        }

    # ------------------- 2. HOME CONTRAST SHOWER -------------------
    @classmethod
    def generate_home_contrast_shower_protocol(
        cls,
        mizaj: str,
        is_raynauds: bool = False
    ) -> Dict[str, Any]:
        """
        Chapter 12.10: Home-Based Hydrotherapy - The ZAYVORA Daily Shower Protocol.
        Trains vascular reactivity and norepinephrine release without extreme hypothermia.
        """
        if is_raynauds:
            return {
                "eligible": False,
                "reason": "Contraindicated: Raynaud's phenomenon (risk of severe peripheral vasospasm)."
            }

        cold_temp_target = "18-20°C" if mizaj in ["Bard-Yabis", "Bard-Ratab"] else "15-18°C"
        cold_duration_sec = 30 if mizaj == "Bard-Yabis" else 60

        return {
            "protocol_name": "ZAYVORA Daily Morning Contrast Shower",
            "frequency": "Daily upon morning waking (prior to 9:00 AM)",
            "cycles": [
                {
                    "step": 1,
                    "phase": "Warm Immersion / Flow",
                    "temp": "39-40°C",
                    "duration": "3-4 minutes",
                    "objective": "Vasodilation, muscle relaxation, parasympathetic priming"
                },
                {
                    "step": 2,
                    "phase": "Graduated Cool Transition",
                    "temp": "Ramp down over 60 seconds",
                    "duration": "60 seconds",
                    "objective": "Prepare autonomic nervous system"
                },
                {
                    "step": 3,
                    "phase": "Cold Shock Pulse",
                    "temp": cold_temp_target,
                    "duration": f"{cold_duration_sec} seconds",
                    "objective": "Norepinephrine release (300-500% surge), brown adipose tissue activation, vagal rebound"
                },
                {
                    "step": 4,
                    "phase": "Repeat Cycle",
                    "instruction": "Repeat Steps 1-3 for 2 to 3 total rounds",
                    "conclusion": "Always conclude with 1 minute of comfortable warm water to prevent prolonged hypothermic vasoconstriction"
                }
            ],
            "mizaj_adjustment": f"Adjusted for {mizaj}: cold phase calibrated to {cold_temp_target} for {cold_duration_sec}s."
        }

    # ------------------- 3. DALAK (THERAPEUTIC MASSAGE) -------------------
    @classmethod
    def prescribe_dalak(
        cls,
        mizaj: str,
        presentation: str,
        has_dvt_history: bool = False,
        recent_surgery_weeks: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Chapter 11: Dalak Classification & Protocols.
        Intensity: Layyeen (gentle), Shadeed (vigorous), Mutawassit (moderate).
        """
        if has_dvt_history:
            return {
                "eligible": False,
                "reason": "Absolute contraindication: Active or past Deep Vein Thrombosis (thromboembolism risk)."
            }
        if recent_surgery_weeks is not None and recent_surgery_weeks < 6:
            return {
                "eligible": False,
                "reason": f"Contraindication: Recent surgery within 6 weeks ({recent_surgery_weeks} weeks reported)."
            }

        # Determine technique based on presentation & Mizaj
        if "ibs" in presentation.lower() or "constipation" in presentation.lower() or "suoo-e-hazm" in presentation.lower():
            dalak_type = "Dalak-e-Batin (Colonic Abdominal Massage)"
            intensity = "Mutawassit (Moderate depth)"
            direction = "Strictly Clockwise along ascending, transverse, and descending colon"
            duration = "15-20 minutes daily or 3x/week"
            oils = "Warm Sesame oil infused with Ajwain (Trachyspermum ammi) and Cumin"
            objective = "Normalize gut peristalsis, relieve visceral hypersensitivity, release gaseous distension"

        elif mizaj == "Bard-Ratab" or "obesity" in presentation.lower() or "metabolic" in presentation.lower():
            dalak_type = "Dalak-e-Shadeed (Deep Vigorous Massage)"
            intensity = "Shadeed (Firm kneading / Pétrissage & tapotement)"
            direction = "Centripetal (toward the heart) on limbs, firm circular on abdomen"
            duration = "45-60 minutes, 2-3x weekly"
            oils = "Mustard seed oil with warming black pepper and ginger extracts"
            objective = "Stimulate Hararat-e-Ghariziya, promote lymphatic return, mobilize stubborn Balgham"

        elif mizaj == "Bard-Yabis" or "burnout" in presentation.lower() or "chronic stress" in presentation.lower():
            dalak_type = "Dalak-e-Layyeen wa Murieh (Gentle Restorative Nervine Massage)"
            intensity = "Layyeen (Slow, rhythmic effleurage)"
            direction = "Craniocaudal and parasympathetic spine alignment (neck, shoulders, paraspinal)"
            duration = "45-60 minutes, 2x weekly"
            oils = "Sweet almond oil or cold-pressed sesame with Lavender and Jatamansi"
            objective = "Reduce salivary cortisol by 24-31%, upregulate serotonin & dopamine, restore vagal tone"

        elif mizaj == "Harr-Yabis" or "hypertension" in presentation.lower():
            dalak_type = "Dalak-e-Murateb (Cooling & Calming Massage)"
            intensity = "Mutawassit to Layyeen (Slow, rhythmic gliding)"
            direction = "Downward soothing strokes along spine and extremities"
            duration = "30-45 minutes, 2x weekly"
            oils = "Coconut oil or Olive oil infused with Sandalwood and Coriander"
            objective = "Sedate sympathetic overdrive, induce nitric oxide vasodilation, drop systolic BP 6-10 mmHg"

        else:
            dalak_type = "Dalak-e-Mutadil (General Balanced Regimental Massage)"
            intensity = "Mutawassit"
            direction = "Centripetal"
            duration = "30-45 minutes weekly"
            oils = "Olive oil"
            objective = "Constitutional maintenance and myofascial relaxation"

        return {
            "eligible": True,
            "dalak_type": dalak_type,
            "intensity": intensity,
            "direction": direction,
            "duration": duration,
            "recommended_oils": oils,
            "physiological_objective": objective,
            "practitioner_level_required": "Clinical Dalak Practitioner (Certified minimum)"
        }

    # ------------------- 4. HIJAMA (WET CUPPING) -------------------
    @classmethod
    def verify_hijama_safety(
        cls,
        platelet_count: int,
        hemoglobin_g_dl: float,
        is_anticoagulated: bool,
        is_pregnant: bool,
        active_infection_at_site: bool
    ) -> Dict[str, Any]:
        """
        Chapter 10.7: Absolute & Relative Contraindications for Hijama Bil Shurt.
        """
        rejection_reasons = []

        if is_anticoagulated:
            rejection_reasons.append("Patient on oral anticoagulant therapy (Warfarin, NOACs, Heparin)")
        if platelet_count < 50000:
            rejection_reasons.append(f"Severe thrombocytopenia: Platelet count {platelet_count} < 50,000/mcL")
        if hemoglobin_g_dl < 10.0:
            rejection_reasons.append(f"Severe anemia: Hemoglobin {hemoglobin_g_dl} g/dL < 10.0 g/dL")
        if is_pregnant:
            rejection_reasons.append("Pregnancy (risk of uterine reflex stimulation on lumbosacral/abdominal sites)")
        if active_infection_at_site:
            rejection_reasons.append("Active localized skin infection, cellulitis, or open abscess")

        if rejection_reasons:
            return {
                "cleared": False,
                "decision": "REJECTED - HIJAMA CONTRAINDICATED",
                "reasons": rejection_reasons
            }

        caution_flags = []
        if 10.0 <= hemoglobin_g_dl < 12.0:
            caution_flags.append(f"Mild anemia (Hb {hemoglobin_g_dl} g/dL): Limit extraction to <20 mL total")

        return {
            "cleared": True,
            "decision": "CLEARED FOR REGIMENTAL WET CUPPING",
            "max_extraction_volume_ml": 20 if caution_flags else 50,
            "cautions": caution_flags,
            "protocol_specifications": {
                "incision_depth": "Superficial epidermal scarification only (1-2 mm, no deep dermal penetration)",
                "equipment": "Sterile single-use disposable cups and surgical blades only",
                "post_care": "Antiseptic dressing, avoid water immersion for 24 hours, monitor vitals"
            }
        }
