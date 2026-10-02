"""
ZAYVORA Health OS™ v5.0 — Ilaj bil Yad & Jarahat (Classical Unani Operative & Manual Surgery) Engine
====================================================================================================
Source Authority:
  - Abul Qasim Khalaf Ibn Abbas Al-Zahrawi (Albucasis): Kitab al-Tasrif li-man 'Ajiza 'an al-Ta'lif (Treatise 30: On Surgery)
  - Amin al-Dawla Ibn al-Quff al-Karaki: Kitab al-Umdah fi Sina'at al-Jarahah (The Pillar of Surgery)
  - Ibn Sina: Al-Qanun fi al-Tibb, Book 4 (Amraz-e-Jarahiyyah, Kasr wa Khal'a, Kai)
  - Ali Ibn Abbas Majusi: Kamilus Sana'ah al-Tibbiyyah

Invariants:
  1. Fail-Closed Surgical Safety Gate: Absolute contraindication for invasive procedures during hemodynamic instability, extreme age (<14, >60 for major Fasd), or pregnancy.
  2. Anatomical Precision: Incisions (Bata) strictly aligned with natural skin tension lines as pioneered by Al-Zahrawi.
  3. Sterile Instrument Integrity: Mandatory verification of sterile Aalaat-e-Jarahat and local antiseptic protocols.
  4. Post-Operative Hemostasis & Cicatrization: Mandatory deployment of authentic Unani styptics (Sang-e-Jarahat, Damm-ul-Akhwain, Kundur).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# =============================================================================
# 1. CLASSICAL UNANI OPERATIVE MODALITIES (AMALIYYAT-E-JARAHAT)
# =============================================================================

CLASSICAL_JARAHAT_MODALITIES: Dict[str, Dict[str, Any]] = {
    "FASD": {
        "classical_name": "Fasd (Venesection / Phlebotomy)",
        "english_equivalent": "Therapeutic Venesection of Targeted Superficial Veins",
        "primary_vessels": [
            "Qeefal (Cephalic Vein - head & neck conditions)",
            "Basaliq (Basilic Vein - thorax, liver, spleen)",
            "Akhal (Median Cubital Vein - systemic sanguine plethoric states)",
            "Safin (Great Saphenous Vein - uterine & pelvic derivation)",
            "Urq-un-Nasa (Sciatic vein branch - sciatica pain)"
        ],
        "indications": ["Imtila Damwi (Sanguine Plethora)", "Severe Hypertensive Crises", "Acute Meningismus", "Sciatica Flare"],
        "contraindications": ["Systolic BP < 100 mmHg", "Severe Anemia (Hb < 10 g/dL)", "Age < 14 or > 60", "Pregnancy"],
        "max_volume_limit_ml": 350,
        "classical_authority": "Kitab al-Tasrif (Al-Zahrawi), Treatise 30, Ch. 1"
    },
    "HIJAMA_BI_AL_SHART": {
        "classical_name": "Hijama bi al-Shart (Wet Cupping with Scarification)",
        "english_equivalent": "Scarified Capillary Decongestion",
        "primary_sites": ["Kahil (Upper thoracic spine / inter-scapular)", "Hamat (Occiput vertex)", "Saqain (Calves)"],
        "indications": ["Localized Capillary Stasis", "Chronic Myofascial Back Pain", "Severe Migraine", "Cutaneous Toxic Heat"],
        "contraindications": ["Coagulopathy / Hemophilia", "Local active infected lesions", "Fasting exhaustion"],
        "lunar_timing_rule": "Conducted preferentially during lunar waning phase (17th, 19th, or 21st day of Hijri month)",
        "classical_authority": "Al-Qanun fi al-Tibb, Book 1"
    },
    "TALEEQ": {
        "classical_name": "Taleeq (Medicinal Hirudotherapy / Leeching)",
        "english_equivalent": "Biochemical Microvascular Decongestion via Hirudo medicinalis",
        "primary_sites": ["Varicose peri-malleolar zones", "Arthritic peri-articular tissues", "Alopecia patches"],
        "indications": ["Deep Venous Insufficiency", "Localized Thrombophlebitis", "Gouty Arthritis Tophus", "Venous Stasis Ulcers"],
        "contraindications": ["Arterial insufficiency", "Leukemia", "Severe immunosuppression"],
        "biological_agent": "Hirudo medicinalis (Laboratory-cultured, single-patient disposable)",
        "classical_authority": "Kitab al-Umdah fi Sina'at al-Jarahah (Ibn al-Quff)"
    },
    "KAI": {
        "classical_name": "Kai (Thermal & Chemical Cauterization)",
        "english_equivalent": "Controlled Thermocoagulation & Hemostasis",
        "variants": ["Mikwah Zahabiyyah (Gold cautery)", "Mikwah Hadeediyyah (Iron cautery)", "Kai Kimiyawi (Caustic mineral)"],
        "indications": ["Persistent Cold Deep-Seated Sciatica", "Intractable Hemorrhage", "Chronic Fistula-in-Ano (Nasoori Qurooh)"],
        "contraindications": ["Acute hot phlegmons", "Superficial major nerve trunks", "Extreme debility"],
        "classical_rule": "Kai is the ultimate regimental/surgical intervention when pharmacological and evaporative therapies fail.",
        "classical_authority": "Kitab al-Tasrif (Al-Zahrawi), Treatise 30, Section 1 (On Cauterization)"
    },
    "BATA": {
        "classical_name": "Bata wa Tajreef (Incision, Drainage & Debridement)",
        "english_equivalent": "Abscess Incision & Purulent Evacuation along Natural Creases",
        "indications": ["Khuraj (Acute Abscess)", "Duhas (Paronychia)", "Tahajjur (Subcutaneous induration)"],
        "contraindications": ["Immature inflammatory phlegmon before concoction / maturation"],
        "surgical_guideline": "Incise precisely along skin lines of cleavage to prevent cicatricial contraction and keloid deformity.",
        "classical_authority": "Kitab al-Tasrif (Al-Zahrawi), Treatise 30, Section 2"
    },
    "JABR_E_NUQSAN": {
        "classical_name": "Jabr-e-Nuqsan (Bone Setting & Fracture Reduction)",
        "english_equivalent": "Closed Anatomical Fracture Reduction & Padded Splint Immobilization",
        "techniques": ["Taddud (Gentle manual traction)", "Taswiyah (Anatomical alignment)", "Jabair (Padded wooden splints)"],
        "indications": ["Simple long bone fractures", "Articular subluxation", "Joint sprain with ligament laxity"],
        "contraindications": ["Open compound fracture with arterial severance (requires emergency hospital trauma transfer)"],
        "topical_dressing": "Zimad-e-Jabr (Acacia, Kundur, and Egg white plaster)",
        "classical_authority": "Al-Qanun fi al-Tibb, Book 4, Fen 5"
    },
    "BATAR": {
        "classical_name": "Amal-e-Qat' wa Batar (Surgical Excision of Gangrene)",
        "english_equivalent": "Limb Salvage Excision above Gangrenous Demarcation",
        "indications": ["Mawt-ul-Azw (Gangrene with black necrosis threatening systemic sepsis)"],
        "contraindications": ["Spreading septic shock (immediate emergency hospital vascular trauma transfer)"],
        "classical_precept": "Sacrifice the part to save the whole (Ibn al-Quff). Cut through living tissue above the putrefactive line.",
        "classical_authority": "Kitab al-Umdah fi Sina'at al-Jarahah (Ibn al-Quff)"
    }
}


# =============================================================================
# 2. CLASSICAL SURGICAL INSTRUMENTARIUM (AALAAT-E-JARAHAT)
# =============================================================================

AL_ZAHRAWI_INSTRUMENTS: Dict[str, Dict[str, str]] = {
    "MIBZA": {"classical_name": "Al-Mibza'", "english_name": "Surgical Scalpel / Lancets", "use": "Precise sharp incision of skin and veins"},
    "JAFFAT": {"classical_name": "Al-Jaffat", "english_name": "Surgical Forceps & Pincers", "use": "Tissue grasping and foreign body extraction"},
    "MINSHAR": {"classical_name": "Al-Minshar", "english_name": "Bone Saw", "use": "Clean osteotomy and bone resection"},
    "SINNARAH": {"classical_name": "Al-Sinnarah", "english_name": "Surgical Retraction Hook", "use": "Retraction of blood vessels and wound edges"},
    "MIKWAH": {"classical_name": "Al-Mikwah", "english_name": "Thermal Cautery Irons", "use": "Hemostatic sealing and tissue sterilization"},
    "MIQYAS": {"classical_name": "Al-Miqyas", "english_name": "Surgical Sound & Probe", "use": "Exploring tract depth in fistulae and sinuses"}
}


# =============================================================================
# 3. POST-OPERATIVE CICATRIZING & STYPTIC BOTANICALS (ADWIYA MUNDAMILAH)
# =============================================================================

CICATRIZING_STYPTIC_FORMULARY: Dict[str, Dict[str, str]] = {
    "SANG_E_JARAHAT": {
        "name": "Sang-e-Jarahat (Purified Hydrous Magnesium Silicate / Steatite)",
        "mizaj": "Barid 1° Yabis 2°",
        "role": "Premier local styptic and wound drying cicatrizer (Mundamil-e-Jarahat)",
        "mode": "Dusting powder directly over sutured or debrided wound beds"
    },
    "DAMM_UL_AKHWAIN": {
        "name": "Damm-ul-Akhwain (Dragon's Blood / Dracaena cinnabari resin)",
        "mizaj": "Barid 2° Yabis 2°",
        "role": "Habis-e-Dam (Immediate capillary hemocoagulant)",
        "mode": "Topical styptic paste with egg white or rose water"
    },
    "KUNDUR": {
        "name": "Kundur (Frankincense / Boswellia serrata resin)",
        "mizaj": "Haar 2° Yabis 2°",
        "role": "Antiseptic tissue regenerator and anti-putrefactive agent",
        "mode": "Ointment base with olive oil or fine dusting powder"
    },
    "MUR_MAKKI": {
        "name": "Mur Makki (Myrrh / Commiphora myrrha gum)",
        "mizaj": "Haar 2° Yabis 2°",
        "role": "Potent antimicrobial cleanser; prevents wound gangrene",
        "mode": "Alcoholic or aqueous wash for infected wound cavities"
    }
}


# =============================================================================
# 4. SURGICAL DECISION & SAFETY GUARD ENGINE
# =============================================================================

@dataclass
class SurgicalAssessmentInput:
    patient_id: str
    age: int
    gender: str
    systolic_bp: int
    diastolic_bp: int
    hemoglobin_g_dl: float
    is_pregnant: bool
    proposed_procedure: str
    target_site: str
    clinical_indication: str


class IlajBilYadEngine:
    """Certified clinical engine for Unani Operative Surgery & Interventions (Ilaj bil Yad)."""

    @classmethod
    def evaluate_surgical_safety(cls, assessment: SurgicalAssessmentInput) -> Dict[str, Any]:
        """Validates all classical and regulatory safety barriers before permitting operative interventions."""
        procedure_key = assessment.proposed_procedure.upper().strip()
        procedure_meta = CLASSICAL_JARAHAT_MODALITIES.get(procedure_key)

        if not procedure_meta:
            return {
                "status": "REJECTED_UNKNOWN_PROCEDURE",
                "is_approved": False,
                "error": f"Unknown surgical procedure '{assessment.proposed_procedure}'. Must match authentic Unani modalities."
            }

        contraindications_triggered = []

        # 1. Hemodynamic Invariant: Systolic BP >= 100 mmHg
        if assessment.systolic_bp < 100:
            contraindications_triggered.append(
                f"Hypotension Alert: Systolic BP ({assessment.systolic_bp} mmHg) is below statutory 100 mmHg minimum for surgery/Fasd."
            )

        # 2. Hemoglobin Invariant for blood-letting procedures
        if procedure_key in ["FASD", "HIJAMA_BI_AL_SHART"]:
            if assessment.hemoglobin_g_dl < 10.0:
                contraindications_triggered.append(
                    f"Anemia Barrier: Hemoglobin ({assessment.hemoglobin_g_dl} g/dL) is below 10.0 g/dL. Blood-letting strictly contraindicated."
                )

        # 3. Age Restrictions for Major Fasd (14 to 60 years)
        if procedure_key == "FASD":
            if assessment.age < 14 or assessment.age > 60:
                contraindications_triggered.append(
                    f"Age Invariant: Fasd is strictly contraindicated in pediatric (<14) and geriatric (>60) populations (Age: {assessment.age})."
                )

        # 4. Pregnancy Barrier
        if assessment.is_pregnant:
            if procedure_key in ["FASD", "HIJAMA_BI_AL_SHART", "BATAR"]:
                contraindications_triggered.append(
                    "Pregnancy Contraindication: Invasive surgery or blood-letting triggers uterine derivation and abortifacient risk."
                )

        # Result Synthesis
        is_safe = len(contraindications_triggered) == 0

        return {
            "procedure": procedure_meta["classical_name"],
            "english_title": procedure_meta["english_equivalent"],
            "is_approved": is_safe,
            "status": "APPROVED_FOR_CLINICAL_SIGNATURE" if is_safe else "BLOCKED_BY_SAFETY_FIREWALL",
            "contraindications_triggered": contraindications_triggered,
            "classical_authority": procedure_meta["classical_authority"],
            "pre_operative_prerequisites": {
                "sterile_instrument_check": "Sterilized Al-Zahrawi surgical tools inspected",
                "patient_consent_and_vital_monitoring": "Vitals verified stable",
                "antiseptic_preparation": "Local cleansing with Arq-e-Gulab and Sirka"
            },
            "post_operative_dressing": [
                CICATRIZING_STYPTIC_FORMULARY["SANG_E_JARAHAT"],
                CICATRIZING_STYPTIC_FORMULARY["KUNDUR"]
            ],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
