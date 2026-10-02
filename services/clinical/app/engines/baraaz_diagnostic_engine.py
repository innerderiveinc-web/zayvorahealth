"""
ZAYVORA Health OS™ v5.0 — Classical Baraaz (Stool & Alimentary) Diagnostic Engine
================================================================================
References:
  - Ibn Sina: Al-Qanoon fit-Tibb (Section on Ahwal-e-Baraaz wa Alamat-e-Hazm)
  - Al-Razi: Kitab al-Mansuri fit-Tibb (Diagnosis of Gastric & Intestinal Humors)
  - Modern Gastroenterology: Bristol Stool Form Scale (BSFS Types 1-7)

Evaluates the Classical Dimensions of Baraaz:
  1. Lawn (Color):
     - Asfar (Normal yellowish-brown)
     - Abyad / Jasiy (Chalky white - Sadad-e-Majari-e-Safra / Obstructive Jaundice)
     - Aswad (Black tarry - Ghait-e-Aswad / Upper GI Bleed / Melena or Saudawi stasis)
     - Ahmar (Overt hematochezia - Bleeding fissures/hemorrhoids/colitis)
     - Akhdar (Green - rapid transit / raw bilious overflow)
  2. Qiwam (Consistency & Bristol Correlation):
     - Yabis shadeed (Bristol 1-2: Severe dryness / Sawda-Balgham yabis)
     - Motadil (Bristol 3-4: Optimal digestion & transit)
     - Raqeeq / Mai (Bristol 5-7: Zalaq-ul-Amaa / Diarrhea / Balgham-e-Mufarrat)
  3. Istihala (State of Alimentary Digestion):
     - Mustahil Sahih (Well-digested, homogeneous)
     - Ghair Mustahil (Undigested food residues - Dha'f-e-Hazm-e-Meda)
  4. Riyah wa Nufukh (Flatulence & Fermentation):
     - Nafakh shadeed (Excessive borborygmi, fermentation dysbiosis)
  5. Boo (Odor):
     - Motadil (Natural)
     - Hiddat-e-Boo (Sour / Acidic fermentation)
     - Ufunat-e-Shadeedah (Putrid colonic putrefaction)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class BaraazInspectionInput:
    lawn: str = "Asfar Tabiyi"     # "Asfar Tabiyi" | "Abyad Chalky" | "Aswad Melena" | "Ahmar Bloody" | "Akhdar"
    bristol_type: int = 4          # 1 to 7
    istihala: str = "Mustahil"     # "Mustahil" (Fully digested) | "Ghair_Mustahil" (Undigested particles)
    riyah: str = "Qaleel"          # "Qaleel" (Normal) | "Katheer" (Severe gas/bloating)
    boo: str = "Motadil"           # "Motadil" | "Hamid" (Sour) | "Muntan" (Putrid)
    khurooj_ease: str = "Sahal"    # "Sahal" (Effortless) | "Usr" (Straining/Tenesmus) | "Ajil" (Urgency)


class BaraazDiagnosticEngine:
    """Clinical reasoning engine for alimentary diagnostics via classical Baraaz & modern gastroenterology."""

    @classmethod
    def analyze_baraaz(
        cls,
        patient_id: str,
        data: BaraazInspectionInput,
        clinical_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        clinical_context = clinical_context or {}

        humoral_burden: Dict[str, int] = {
            "Dam": 0,
            "Safra": 0,
            "Balgham": 0,
            "Sawda": 0,
        }
        alimentary_status: List[str] = []
        pathological_alerts: List[str] = []
        red_flags: List[str] = []
        recommended_tadbeer: List[str] = []

        # 1. Color (Lawn) Assessment
        c_lawn = data.lawn.lower()
        if "aswad" in c_lawn or "melena" in c_lawn or "black" in c_lawn:
            red_flags.append("Ghait-e-Aswad (Melena) detected: Upper GI bleeding must be excluded STAT.")
            humoral_burden["Sawda"] += 4
        elif "ahmar" in c_lawn or "blood" in c_lawn or "red" in c_lawn:
            red_flags.append("Nazf-e-Mevi (Overt Hematochezia): Lower GI bleed or severe proctitis.")
            humoral_burden["Dam"] += 4
        elif "abyad" in c_lawn or "chalk" in c_lawn or "pale" in c_lawn or "white" in c_lawn:
            red_flags.append("Sadad-e-Majari-e-Safra (Biliary duct obstruction / Cholestasis).")
            alimentary_status.append("Absence of stercobilin indicates impaired bile secretion into duodenum")
            humoral_burden["Safra"] += 3
        elif "akhdar" in c_lawn or "green" in c_lawn:
            humoral_burden["Safra"] += 2
            alimentary_status.append("Sura'at-e-Nafuz (Rapid colonic transit bypassing biliverdin reduction)")
        else:
            humoral_burden["Safra"] += 1  # Physiological presence of bile

        # 2. Consistency & Bristol Scale
        if data.bristol_type in [1, 2]:
            humoral_burden["Sawda"] += 3
            alimentary_status.append("Qabz-e-Yabis (Spastic/Dry Constipation with delayed colonic transit)")
            recommended_tadbeer.extend([
                "Roghan-e-Badam Shireen (Sweet Almond Oil 10ml in warm milk HS)",
                "Lu'ab-e-Isabgol (Ispaghula husk steeped with warm water)",
                "Dalak-e-Batn (Clockwise gentle abdominal massage with warm sesame oil)"
            ])
        elif data.bristol_type in [3, 4]:
            alimentary_status.append("Qiwam-e-Motadil (Optimal alimentary hydration and mucosal transit)")
        elif data.bristol_type in [5, 6, 7]:
            humoral_burden["Balgham"] += 3
            alimentary_status.append("Zalaq-ul-Amaa / Ishaal (Mucosal Hyper-motility & Malabsorption)")
            recommended_tadbeer.extend([
                "Habis-e-Amaa astringents (Belgiri, Post-e-Anar decoction)",
                "Taskeen-e-Meda (Infusion of Kishneez and Podina)",
                "Avoid cold, raw, and mucilaginous foods"
            ])

        # 3. Istihala (Digestive Completeness)
        if data.istihala == "Ghair_Mustahil":
            alimentary_status.append("Dha'f-e-Hazm-e-Meda (Impaired gastric peptic and churning capacity)")
            recommended_tadbeer.append("Jawarish Kamuni or Zanjabeel extract 15 mins prior to main meals")

        # 4. Riyah wa Nufukh
        if data.riyah == "Katheer":
            alimentary_status.append("Nafakh-e-Shadeed (Dysbiotic gaseous distension & fermentation)")
            recommended_tadbeer.append("Kasir-e-Riyah carminatives (Ajwain Desi + Zeera Siyah)")

        # 5. Odor (Boo)
        if data.boo == "Muntan":
            alimentary_status.append("Ufunat-e-Meviyah (Putrefactive dysbiosis in colonic lumen)")
        elif data.boo == "Hamid":
            alimentary_status.append("Tahammuz (Acidic carbohydrate malfermentation)")

        # Primary Humoral Imbalance
        sorted_h = sorted(humoral_burden.items(), key=lambda x: x[1], reverse=True)
        dominant_dyscrasia = sorted_h[0][0] if sorted_h[0][1] > 0 else "Motadil"

        return {
            "patient_id": patient_id,
            "modality": "Classical Baraaz & Bristol Form Clinical Synthesis",
            "bristol_type": data.bristol_type,
            "dominant_humoral_burden": dominant_dyscrasia,
            "humoral_scores": humoral_burden,
            "alimentary_syndromes": alimentary_status,
            "critical_red_flags": red_flags,
            "recommended_regimenal_tadbeer": recommended_tadbeer,
            "requires_urgent_endoscopy": len(red_flags) > 0,
            "safe_for_routine_matab": len(red_flags) == 0,
        }
