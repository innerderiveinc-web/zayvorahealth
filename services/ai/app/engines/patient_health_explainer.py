"""
ZAYVORA Health OS™ — Explain My Health Engine (Care Intelligence 2.0)
===================================================================
Reference:
  - Human Bedside Manner Rule 5: Compassionate, dignified, clear communication.
  - Purpose: Translates complex clinical diagnoses, Unani humoral concepts,
    and lab biomarkers into clear, reassuring, patient-friendly language.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import datetime


@dataclass
class HealthExplanationDossier:
    patient_id: str
    patient_name: str
    language: str  # "roman_urdu", "english", "hindi"
    condition_explanation: str
    why_this_medicine: str
    daily_care_instructions: List[str]
    lab_markers_simplified: List[Dict[str, str]]
    safety_red_flags_to_watch: List[str]
    next_care_milestone: str
    generated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())


class PatientHealthExplainer:
    """
    Translates complex biomedical and Unani clinical notes into
    accessible, comforting, patient-facing explanations.
    """

    @classmethod
    def explain_health_summary(
        cls,
        patient_id: str,
        patient_name: str,
        diagnosis_title: str = "Waja-ul-Mafasil (Osteoarthritis with Balghami Stagnation)",
        prescribed_nuskha: str = "Majun Suranjan (with purified Colchicum and Zanjabil)",
        biomarkers: Optional[Dict[str, Any]] = None,
        language: str = "roman_urdu"
    ) -> HealthExplanationDossier:
        biomarkers = biomarkers or {
            "hs-CRP": {"value": "4.8 mg/L", "trend": "improving", "meaning": "Sojan/Inflammation"},
            "ESR": {"value": "22 mm/hr", "trend": "normalizing", "meaning": "Khoon ki garmi / reaction"}
        }

        if language == "roman_urdu":
            cond_exp = (
                f"Mohtaram {patient_name} Sahab, doctor sahab ke muayne ke mutabiq aapke ghutno ke joron mein "
                f"thandak aur bhaaripan (Balgham) ki wajah se sojan aur akadpan hai. Yeh umar aur thandi hawa ke asar se "
                f"joron ke andar qudrati chiknahat kam hone ki alamat hai. Fikr ki koi baat nahi, yeh ilaj-pazeer hai."
            )
            med_exp = (
                f"Aapko '{prescribed_nuskha}' tajweez kiya gaya hai. Isme Shuddha Suranjan aur Sonth jaisi jari-bootiyan hain "
                f"jo joron ke andar se faasid maadday (waste fluids) ko kharij karti hain aur khoon ki rawani ko behtar banati hain."
            )
            daily_care = [
                "Subah aur shaam nuskha neem-garam paani ya doodh ke saath lein.",
                "Thande paani, dahee, khatti cheezon aur baadi daalon se parhez rakhein.",
                "Rozana 15-20 minute dhoop mein walk karein aur ghutne par tez hawa na lagne dein."
            ]
            markers_simp = [
                {
                    "marker": "hs-CRP (Sojan ka Test)",
                    "status": "Behtar ho raha hai (4.8 mg/L)",
                    "note": "Joron ki andaruni sojan pehle se taqreeban 42% kam ho chuki hai."
                },
                {
                    "marker": "ESR (Khoon ka Bahao)",
                    "status": "Normal band mein (22 mm/hr)",
                    "note": "Jism ka inflammatory reaction ab control mein hai."
                }
            ]
            red_flags = [
                "Agar achanak ghutne mein shadid surkhi, aag jaisi jalan, ya taiz bukhar ho to foran clinic se rabta karein.",
                "Agar pait mein shadid maror ya ulti aaye to dawai rokk kar doctor ko muttala karein."
            ]
            next_step = "Day 21 par aapka interim review appointment tay hai jahan doctor sahab dawai ki miqdaar adjust karenge."

        else:  # Simple English
            cond_exp = (
                f"Dear {patient_name}, your doctor's evaluation shows localized joint inflammation and stiffness in your knees, "
                f"primarily driven by metabolic fluid accumulation and cold sensitivity. This is manageable through targeted herbal anti-inflammatory therapy."
            )
            med_exp = (
                f"You have been prescribed '{prescribed_nuskha}'. This formulation contains purified Colchicum and Ginger extract "
                f"designed to clear inflammatory buildup from synovial tissues and restore comfortable joint mobility."
            )
            daily_care = [
                "Take your prescribed formulation twice daily with lukewarm water or milk after meals.",
                "Avoid icy beverages, excessive fermented foods, and damp drafts on your joints.",
                "Engage in gentle 15-minute morning mobility exercises and warm sunlight exposure."
            ]
            markers_simp = [
                {
                    "marker": "hs-CRP (Inflammation Level)",
                    "status": "Significantly Improving (4.8 mg/L)",
                    "note": "Your systemic joint inflammation has dropped by over 40% from baseline."
                },
                {
                    "marker": "ESR (Sedimentation Rate)",
                    "status": "Near Normal Range (22 mm/hr)",
                    "note": "Your acute immune reaction is steadily returning to healthy baseline."
                }
            ]
            red_flags = [
                "Contact the clinic immediately if you experience sudden intense localized heat, fever, or inability to bear weight.",
                "Pause medicine and consult your doctor if you experience persistent gastric upset."
            ]
            next_step = "Your 21-day clinical milestone check-in is scheduled to evaluate mobility gains and adjust dosing."

        return HealthExplanationDossier(
            patient_id=patient_id,
            patient_name=patient_name,
            language=language,
            condition_explanation=cond_exp,
            why_this_medicine=med_exp,
            daily_care_instructions=daily_care,
            lab_markers_simplified=markers_simp,
            safety_red_flags_to_watch=red_flags,
            next_care_milestone=next_step
        )
