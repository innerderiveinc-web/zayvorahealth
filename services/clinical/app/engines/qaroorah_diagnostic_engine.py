"""
ZAYVORA Health OS™ v5.0 — Classical Qaroorah (Urine / Tafsirah) Diagnostic Engine
================================================================================
References:
  - Ibn Sina: Al-Qanoon fit-Tibb (Book 1, Section on Ahwal-e-Baul)
  - Al-Razi: Kitab al-Hawi fit-Tibb
  - Ismail Jurjani: Dhakhira-e-Khwarizmshahi
  - Modern Clinical Urinalysis (NCCLS/CLSI GP16-A3 Standards)

Codifies the 7 Classical Dimensions of Qaroorah (Ajnas-e-Sab'a):
  1. Lawn (Color): Abyad (White), Asfar (Straw/Yellow), Ahmar (Red/Flaming), Asawad/Akhdar (Dark/Green).
  2. Qiwam (Consistency): Raqeeq (Thin), Ghaleez (Thick/Viscous), Motadil (Equable).
  3. Safa wa Kudurat (Transparency & Clarity): Safi (Clear), Kadeer (Turbid/Cloudy).
  4. Rusoob (Sediment): Rasub-e-Mahmoof (Equable/Physiological), Qaihi (Purulent),
                         Rameeli (Sandy/Lithic), Mukhati (Mucoid/Phlegmatic).
  5. Miqdar (Volume): Katheer (Copious/Polyuria), Qaleel (Oliguria), Motadil.
  6. Boo (Odor): Bira'ihah (Inoffensive/Normal), Hiddat-e-Boo (Pungent/Safrawi),
                 Mutanaffan (Fetid/Putrid infection).
  7. Zabd (Foam/Bubbles): Katheer-uz-Zabd (Persistent froth - Proteinuria/Balgham-e-Lazuq),
                          Qaleel-uz-Zabd (Transient/Normal).

Integrated Dual-Stream Diagnostic Reasoning:
  Combines classical inspection with modern Dipstick & Microscopic urinalysis
  (Specific Gravity, pH, Protein, Glucose, Ketones, Nitrites, Leuko-esterase,
   Crystals, Casts, Microscopic Hematuria).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class QaroorahPhysicalInspection:
    lawn: str = "Asfar Qashiy"       # "Abyad" | "Asfar Qashiy" | "Asfar Na'i" | "Ahmar Nari" | "Asawad" | "Akhdar"
    qiwam: str = "Motadil"           # "Raqeeq" (Thin) | "Ghaleez" (Thick) | "Motadil" (Equable)
    safa: str = "Safi"               # "Safi" (Clear) | "Kadeer" (Turbid)
    rusoob: str = "Mahmoof"          # "Mahmoof" (Normal) | "Rameeli" (Sandy) | "Qaihi" (Purulent) | "Mukhati" (Mucoid) | "None"
    miqdar: str = "Motadil"          # "Katheer" (Excess) | "Qaleel" (Scanty) | "Motadil" (Normal)
    boo: str = "Bira'ihah"           # "Bira'ihah" (Normal) | "Hadd" (Pungent) | "Mutanaffan" (Fetid)
    zabd: str = "Qaleel"             # "Qaleel" (Transient) | "Katheer_Daim" (Persistent froth)


@dataclass
class ModernUrinalysisData:
    specific_gravity: Optional[float] = None     # 1.005 - 1.030
    ph: Optional[float] = None                   # 4.5 - 8.0
    protein_mg_dl: Optional[float] = None        # 0 (Negative), 30 (1+), 100 (2+), 300 (3+)
    glucose_mg_dl: Optional[float] = None        # 0 (Negative), >100 (Glycosuria)
    ketones: Optional[str] = None                # "Negative" | "Trace" | "Moderate" | "Large"
    nitrite: Optional[str] = None                # "Negative" | "Positive"
    leukocyte_esterase: Optional[str] = None     # "Negative" | "Trace" | "Positive"
    microscopic_rbc_hpf: Optional[float] = None  # 0 - 2 (Normal)
    microscopic_wbc_hpf: Optional[float] = None  # 0 - 5 (Normal)
    crystals: Optional[str] = None               # "None" | "Calcium Oxalate" | "Uric Acid" | "Triple Phosphate"
    casts: Optional[str] = None                  # "None" | "Hyaline" | "Granular" | "RBC Casts" | "WBC Casts"


class QaroorahDiagnosticEngine:
    """Clinical reasoning engine for classical Qaroorah and modern urinalysis."""

    @classmethod
    def analyze_qaroorah(
        cls,
        patient_id: str,
        inspection: QaroorahPhysicalInspection,
        modern_labs: Optional[ModernUrinalysisData] = None,
        clinical_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        modern_labs = modern_labs or ModernUrinalysisData()
        clinical_context = clinical_context or {}

        humoral_indicators: Dict[str, int] = {
            "Dam": 0,
            "Safra": 0,
            "Balgham": 0,
            "Sawda": 0,
        }
        involved_organs: List[str] = []
        pathological_syndromes: List[str] = []
        critical_red_flags: List[str] = []
        modern_correlations: List[str] = []

        # -------------------------------------------------------------
        # 1. Lawn (Color) Interpretation
        # -------------------------------------------------------------
        c_lawn = inspection.lawn.lower()
        if "abyad" in c_lawn or "white" in c_lawn or "pale" in c_lawn:
            humoral_indicators["Balgham"] += 3
            pathological_syndromes.append("Buroodat-e-Mizaj (Excessive Constitutional Coldness)")
            if inspection.qiwam.lower() == "raqeeq":
                pathological_syndromes.append("Adam-e-Nujz (Unconcocted, immature humoral stasis)")
        elif "asfar na" in c_lawn or "deep yellow" in c_lawn or "bright yellow" in c_lawn:
            humoral_indicators["Safra"] += 3
            pathological_syndromes.append("Ghalba-e-Safra (Bilious Heat & Hepato-biliary excitation)")
        elif "ahmar" in c_lawn or "red" in c_lawn or "nari" in c_lawn:
            humoral_indicators["Dam"] += 3
            involved_organs.append("Urooqe / Majari-e-Baul")
            pathological_syndromes.append("Imtila-e-Damwi (Sanguineous Plethora / Hematuria)")
        elif "asawad" in c_lawn or "black" in c_lawn or "dark" in c_lawn:
            humoral_indicators["Sawda"] += 3
            pathological_syndromes.append("Ihtiraq-e-Akhlat (Humoral Combustion / Melancholic stasis)")

        # -------------------------------------------------------------
        # 2. Qiwam (Consistency) & Safa (Clarity)
        # -------------------------------------------------------------
        c_qiwam = inspection.qiwam.lower()
        c_safa = inspection.safa.lower()
        if "ghaleez" in c_qiwam or "thick" in c_qiwam:
            humoral_indicators["Balgham"] += 2
            pathological_syndromes.append("Ghilzat-e-Akhlat (Viscous Humoral Congestion)")
        if "kadeer" in c_safa or "turbid" in c_safa or "cloudy" in c_safa:
            involved_organs.append("Kulyah wa Masana (Kidneys & Bladder)")
            pathological_syndromes.append("Kudurat-ul-Baul (Urinary Tract Stasis / Infection risk)")

        # -------------------------------------------------------------
        # 3. Rusoob (Sediment) Analysis
        # -------------------------------------------------------------
        c_rusoob = inspection.rusoob.lower()
        if "rameeli" in c_rusoob or "sand" in c_rusoob:
            involved_organs.append("Kulyah (Kidneys)")
            pathological_syndromes.append("Raml-e-Kulya (Renal Gravel / Nephrolithiasis Risk)")
            modern_correlations.append("High probability of microscopic or macroscopic crystalluria")
        elif "qaihi" in c_rusoob or "purulent" in c_rusoob:
            involved_organs.append("Majari-e-Baul")
            pathological_syndromes.append("Hurqat-ul-Baul wa Quruh (Pyuria / Mucosal Ulceration)")
            modern_correlations.append("Probable pyuria / leukocyturia indicative of active infection")
        elif "mukhati" in c_rusoob or "mucoid" in c_rusoob:
            humoral_indicators["Balgham"] += 2
            pathological_syndromes.append("Balgham-e-Kham (Unripe Phlegmatic Exudate)")
        elif "mahmoof" in c_rusoob:
            pathological_syndromes.append("Rasub-e-Mahmoof (Favourable Physiological Clearance / Nujz marker)")

        # -------------------------------------------------------------
        # 4. Boo (Odor) & Zabd (Foam)
        # -------------------------------------------------------------
        c_boo = inspection.boo.lower()
        if "mutanaffan" in c_boo or "fetid" in c_boo:
            pathological_syndromes.append("Ufunat-e-Baul (Septic Putrefaction in Urinary Pathway)")
            involved_organs.append("Majari-e-Baul")
        elif "hadd" in c_boo or "pungent" in c_boo:
            humoral_indicators["Safra"] += 2

        c_zabd = inspection.zabd.lower()
        if "katheer" in c_zabd or "froth" in c_zabd:
            humoral_indicators["Balgham"] += 2
            pathological_syndromes.append("Riyah-e-Ghaleezah wa Rutoobat-e-Lazuqah (Viscous protein stasis)")
            modern_correlations.append("Significant persistent frothing correlates with macro-proteinuria")

        # -------------------------------------------------------------
        # 5. Modern Laboratory Data Synthesis
        # -------------------------------------------------------------
        if modern_labs.protein_mg_dl is not None and modern_labs.protein_mg_dl >= 100:
            critical_red_flags.append(f"Significant Proteinuria ({modern_labs.protein_mg_dl} mg/dL) detected.")
            involved_organs.append("Kulyah (Glomerular Barrier)")
            modern_correlations.append("Glomerulopathy or advanced nephrotic/nephritic condition.")

        if modern_labs.glucose_mg_dl is not None and modern_labs.glucose_mg_dl > 0:
            pathological_syndromes.append("Zia-e-Baitus Shakri (Diabetes / Glycosuria)")
            modern_correlations.append(f"Glycosuria detected ({modern_labs.glucose_mg_dl} mg/dL)")

        if modern_labs.nitrite == "Positive" or modern_labs.leukocyte_esterase == "Positive":
            pathological_syndromes.append("Warm-e-Majari-e-Baul Haad (Acute Bacterial Cystitis / UTI)")
            modern_correlations.append("Positive Leukocyte Esterase/Nitrite indicates active bacterial colonization")

        if modern_labs.microscopic_rbc_hpf is not None and modern_labs.microscopic_rbc_hpf > 3:
            critical_red_flags.append(f"Microscopic Hematuria ({modern_labs.microscopic_rbc_hpf} RBC/hpf).")
            pathological_syndromes.append("Nazf-e-Baul (Urinary Bleeding)")

        if modern_labs.crystals and modern_labs.crystals != "None":
            modern_correlations.append(f"Urinary Crystals Present: {modern_labs.crystals}")
            pathological_syndromes.append("Istidad-e-Hisat (Active Crystalluria / Calculogenesis)")

        # Determine Dominant Humoral Dyscrasia from Qaroorah
        sorted_humors = sorted(humoral_indicators.items(), key=lambda x: x[1], reverse=True)
        dominant_humor = sorted_humors[0][0] if sorted_humors[0][1] > 0 else "Motadil (Balanced)"

        # Target Afaal Recommendation
        afaal_strategy = []
        if dominant_humor == "Safra":
            afaal_strategy.extend(["Tabreed (Cooling)", "Taskeen (Sedating bile)", "Idrar-e-Baul (Mild Diuresis)"])
        elif dominant_humor == "Balgham":
            afaal_strategy.extend(["Tasgheen (Warming)", "Nujz-e-Balgham (Concoction of phlegm)", "Tahleel-e-Riyah"])
        elif dominant_humor == "Sawda":
            afaal_strategy.extend(["Tanziyah (Cleansing)", "Tarteeb (Hydration/Moistening)", "Tanqiya-e-Sawda"])
        elif dominant_humor == "Dam":
            afaal_strategy.extend(["Tanqiya-e-Dam (Blood letting / Fasd consideration)", "Tabreed-e-Dam"])
        else:
            afaal_strategy.append("Hifz-e-Sihhat (Health preservation)")

        return {
            "patient_id": patient_id,
            "diagnostic_modality": "Classical Qaroorah wa Modern Urinalysis Integration",
            "dominant_humor_inferred": dominant_humor,
            "humoral_scores": humoral_indicators,
            "involved_organs": list(set(involved_organs)),
            "pathological_syndromes": list(set(pathological_syndromes)),
            "modern_correlations": modern_correlations,
            "critical_red_flags": critical_red_flags,
            "recommended_afaal_strategy": afaal_strategy,
            "safe_to_proceed_with_herbal": len(critical_red_flags) == 0,
            "clinical_governance_note": "Tafsirah-e-Baul is a decision-support semiotic tool; requires confirmation via standard clinical microscopy where red flags appear."
        }
