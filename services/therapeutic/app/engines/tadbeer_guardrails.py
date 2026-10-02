"""
ZAYVORA Health OS™ v5.0 — Ilaj bil-Tadbeer (Unani Regimental Therapy) Engine
=============================================================================
Source Authority:
  - Dr. Irfan Ashraf: "Ilaj Bil Tadbeer: The Game Changer in Modern Healthcare" (Feb 2026)
  - Dr. Irfan Ashraf: "Ilaj bil Tadbeer: A Beginner's Guide to Unani Healing" (Feb 2026)
  - Ibn Sina: Al-Qanun fi al-Tibb (Book 1 & 3: Regimen, Massage, Exercise, Baths, Evacuations)
  - Abu Bakr al-Razi: Kitab al-Hawi fi al-Tibb & Kitab al-Mansuri
  - Abul Qasim al-Zahrawi: Kitab al-Tasrif (Surgical & Regimental Instruments)
  - NCISM / CCIM BUMS Official Syllabus (Kulliyat-e-Ilaj & Ilaj bit-Tadbeer)
  - Central Council for Research in Unani Medicine (CCRUM) Regimental SOP Guidelines

Covers:
  1. The 16 Classical Regimental Modalities (Al-Tadabeer Al-Sittata Ashar)
  2. The 7 Therapeutic Principles (Usool-e-Tadbeer)
  3. Condition-Specific Multi-Modal Regimen Protocols (Low Back Pain, IBS, Osteoarthritis, Headaches)
  4. Home-Based Self-Care Protocols & Basic Kit (< ₹500)
  5. Deterministic Safety Guardrails & Acute Medical Red-Flag Triage Barrier
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

VERDICT_ORDER = ["SAFE_TO_CONSIDER", "CAUTION", "MODIFY", "DO_NOT_RECOMMEND", "REFER"]


def _escalate(current: str, candidate: str) -> str:
    return candidate if VERDICT_ORDER.index(candidate) > VERDICT_ORDER.index(current) else current


# =============================================================================
# 1. THE 16 CLASSICAL REGIMENTAL MODALITIES (FULL CATALOG)
# =============================================================================

TADBEER_MODALITIES_16: Dict[str, Dict[str, Any]] = {
    "Riyazat": {
        "name": "Riyazat (Physical Exercise & Activity)",
        "classical_description": "Voluntary physical movement performed with intention to accelerate Hararat-e-Ghariziyyah and expel wastes through perspiration.",
        "types": ["Light (Brisk walking)", "Moderate (Swimming, jogging)", "Vigorous (Competitive exertion)"],
        "indications": ["Obesity", "Metabolic syndrome", "Type 2 Diabetes", "Depression", "Cardiovascular tone"],
        "mizaj_guidelines": {
            "Damwi": "Tolerates high-intensity well; regular vigorous sweating beneficial.",
            "Balghami": "Sustained vigorous thermogenic exercise essential to melt cold-moist stagnation.",
            "Safrawi": "Moderate non-competitive cooling movement (e.g. swimming in cool water); avoid overheating.",
            "Saudawi": "Gentle restorative movement (nature walking, gentle yoga); strictly avoid exhaustion."
        },
        "contraindications": ["Acute high fever", "Immediately postprandial (<2h)", "Extreme physical exhaustion", "Active acute infection"],
        "evidence_grade": "A (RCT & Meta-analyses)"
    },
    "Dalak": {
        "name": "Dalak (Medical & Therapeutic Massage)",
        "classical_description": "Mechanical manipulation of soft tissues categorized by pressure, duration, and medium.",
        "types": [
            "Dalak-e-Layyin (Soft/Gentle: Sedative, sleep-inducing, vagal stimulation)",
            "Dalak-e-Sulb (Firm/Vigorous: Muscle tone, deobstruent, increases circulation)",
            "Dalak-e-Duhni (Oil Massage: Nourishment, skin softening, anti-dryness)"
        ],
        "indications": ["Musculoskeletal pain", "Post-stroke rehabilitation", "Insomnia", "Anxiety", "Chronic constipation (clockwise abdominal)"],
        "contraindications": ["Documented or suspected DVT (Deep Vein Thrombosis) — FATAL RISK", "Active skin cellulitis / open wounds", "Acute unreduced fractures"],
        "evidence_grade": "A (Meta-analyses)"
    },
    "Hijama": {
        "name": "Hijama (Cupping Therapy — Wet & Dry)",
        "classical_description": "Creation of therapeutic negative pressure on specific visceral reflex zones to extract morbid congestion or redirect humors.",
        "types": ["Hijama bila-Shart (Dry / Suction alone)", "Hijama bil-Shart (Wet / Scarification & capillary extraction)"],
        "indications": ["Chronic low back pain", "Knee osteoarthritis", "Hypertension", "Sciatica", "Musculoskeletal tension"],
        "contraindications": [
            "Anticoagulant therapy (Warfarin, Heparin, NOACs)",
            "Active bleeding disorders / severe coagulopathy",
            "Moderate-to-severe anemia (Hb < 9 g/dL)",
            "Acute hypotension / hemodynamic instability",
            "Pregnancy: strictly contraindicated on abdominal and lumbosacral regions"
        ],
        "evidence_grade": "A/B (Systematic Reviews & RCTs)"
    },
    "Fasd": {
        "name": "Fasd (Venesection / Phlebotomy)",
        "classical_description": "Controlled incisive evacuation of vitiated blood from specific peripheral veins (Basilic, Cephalic, Median).",
        "indications": ["Plethora (Imtila bi Hasb al-Aw'iyah)", "Polycythemia vera", "Acute hypertensive emergencies in resource-limited settings"],
        "contraindications": [
            "Pediatric age < 14 years (Ibn Sina Canon Rule)",
            "Geriatric age > 60 years (Failure of Tabiyat recovery)",
            "Pregnancy (Absolute contraindication)",
            "Severe anemia, hypotension, heart failure, bleeding diathesis"
        ],
        "evidence_grade": "B (Controlled Clinical Trials)"
    },
    "Taleeq": {
        "name": "Taleeq / Irsal-e-Alaq (Medicinal Leech Therapy / Hirudotherapy)",
        "classical_description": "Application of medicinal leeches (Hirudo medicinalis) to inject bioactive salivary secretions (hirudin, calin, hyaluronidase).",
        "indications": ["Venous congestion post-reconstructive flap surgery (FDA-cleared medical device indication)", "Diabetic non-healing ulcers", "Varicose micro-thrombosis", "Severe localized inflammation"],
        "contraindications": ["Severe anemia (Hb < 8 g/dL)", "Active leukemia / immunosuppression", "Arterial insufficiency", "Hemophilia / Anticoagulants"],
        "evidence_grade": "A (FDA-Cleared Medical Device Modality & Clinical RCTs)"
    },
    "Kai": {
        "name": "Kai (Therapeutic Cauterization / Thermocautery)",
        "classical_description": "Thermal application using heated instruments to arrest necrosis, resolve deep intractable joint pathology, or create counter-irritation.",
        "indications": ["Refractory sciatica", "Chronic non-responsive arthralgia", "Arresting gangrenous spread", "Cold chronic joint deformity"],
        "contraindications": ["Uncontrolled diabetes (extreme gangrene risk)", "Peripheral diabetic neuropathy", "Over major vascular trunks", "Cosmetic facial zones"],
        "evidence_grade": "B (Specialist Clinical Interventions)"
    },
    "Hammam": {
        "name": "Hammam (Medicated Baths & Hydrotherapy)",
        "classical_description": "Immersion in thermal water or steam rooms infused with medicinal herbs to induce sweating or muscular relaxation.",
        "types": ["Hammam Haar (Hot: Muscle relaxant, toxin purge)", "Hammam Barid (Cold: Toning, fever management)", "Contrast Hammam (Alternating hot/cold: Circulatory booster)"],
        "indications": ["Fibromyalgia", "Rheumatoid arthritis", "Chronic fatigue", "Stress & insomnia"],
        "contraindications": ["Acute febrile illness (Humma-e-Hadda)", "Severe decompensated heart failure", "Uncontrolled angina"],
        "evidence_grade": "A (RCTs in Hydrotherapy)"
    },
    "Takmeed": {
        "name": "Takmeed (Fomentation & Compress Therapy)",
        "classical_description": "Local application of moist/dry heat or cold compresses to relieve pain, soften indurations, or arrest acute swelling.",
        "types": ["Hot Fomentation (Takmeed Haar: Castor oil pack in PCOS/joint stiffness)", "Cold Compress (Takmeed Barid: Acute sprains, epistaxis)"],
        "indications": ["Acute musculoskeletal sprains", "Pelvic congestion (PCOS)", "Boil maturation", "Tension headaches"],
        "contraindications": ["Open bleeding wounds (for hot)", "Sensory nerve loss / frostbite risk (for cold)"],
        "evidence_grade": "A (Physical Therapy Evidence)"
    },
    "Nutool": {
        "name": "Nutool (Irrigation & Pouring Therapy)",
        "classical_description": "Pouring a continuous steady stream of warm or cold medicated decoction onto the scalp or specific affected organ.",
        "indications": ["Sahar (Chronic insomnia)", "Sudaa (Headache/Migraine)", "Meningeal tension", "Cerebral hyperthermia"],
        "contraindications": ["Active open scalp infections", "Acute cranial trauma"],
        "evidence_grade": "B (Clinical Unani Studies)"
    },
    "Inkebab": {
        "name": "Inkebab (Steam Inhalation & Fumigation)",
        "classical_description": "Breathing in herbal aromatic vapors (Mint, Eucalyptus, Camphor, Ajwain) to clear respiratory conduits.",
        "indications": ["Sinusitis", "Bronchitis", "Allergic rhinitis", "Facial pore cleansing"],
        "contraindications": ["Severe active hemoptysis", "Facial burn risk in unattended pediatric patients"],
        "evidence_grade": "B (Respiratory Regimenal Evidence)"
    },
    "Ishal": {
        "name": "Ishal (Therapeutic Purgation / Tanqiya)",
        "classical_description": "Evacuation of morbid gastrointestinal humors using calibrated herbal purgatives after concoction (Nujz).",
        "indications": ["Su-e-Mizaj Maddi", "Chronic constipation", "Systemic humoral plethora"],
        "contraindications": ["Acute intestinal obstruction", "Acute appendicitis / peritonitis", "Pregnancy (labor induction risk)", "Severe electrolyte collapse"],
        "evidence_grade": "B (Classical Protocol Validated)"
    },
    "Qai": {
        "name": "Qai (Therapeutic Emesis)",
        "classical_description": "Induced therapeutic vomiting to evacuate toxic phlegmatic or bilious matter from the upper stomach.",
        "indications": ["Acute non-corrosive ingestion poisoning", "Severe gastric phlegmatic burden", "Chronic dyspepsia"],
        "contraindications": ["Esophageal varices (catastrophic bleed risk)", "Intracranial hypertension", "Late pregnancy", "Ingestion of petroleum/caustics"],
        "evidence_grade": "B (Classical Gastro-Emergency)"
    },
    "Huqna": {
        "name": "Huqna (Enema Therapy — Cleansing, Nutritive, Medicinal)",
        "classical_description": "Colonic administration of warm herbal decoctions or oils for lower bowel cleansing, local absorption, or systemic nourishment.",
        "types": ["Cleansing (Huqna Munaqqiya)", "Nutritive (Huqna Mughazziya)", "Soothing Demulcent (Huqna Mulayyina)"],
        "indications": ["Chronic refractory constipation", "IBS (Irritable Bowel Syndrome)", "Sciatic nerve compression from colonic gas", "Paralytic ileus recovery"],
        "contraindications": ["Acute gastrointestinal perforation", "Severe active ulcerative colitis bleeding"],
        "evidence_grade": "A/B (PubMed 2025 Clinical Evidence)"
    },
    "Tareeq": {
        "name": "Tareeq (Diaphoresis / Therapeutic Sweating)",
        "classical_description": "Induction of active sweating via exercise, steam chambers, hot baths, or diaphoretic infusions to purge metabolic wastes.",
        "indications": ["Dermatological clearing", "Fever resolution (defervescence)", "Microvascular drainage"],
        "contraindications": ["Severe hypovolemia", "Heat stroke / anhidrosis"],
        "evidence_grade": "B"
    },
    "Idrar": {
        "name": "Idrar (Therapeutic Diuresis)",
        "classical_description": "Promoting urinary excretion of serous waste and renal sediment using gentle herbal diuretics (Bazoori, Kasni, Khar-e-Khasak).",
        "indications": ["Mild fluid retention", "Crystalluria / renal gravel", "Urinary tract irritation"],
        "contraindications": ["Complete anuria from structural obstruction", "End-stage renal disease without dialysis"],
        "evidence_grade": "B"
    },
    "Aabzan": {
        "name": "Aabzan (Medicated Sitz Bath & Hydration Therapy)",
        "classical_description": "Immersion of pelvic and perineal region in a tub containing warm decoctions of chamomile, rose, or neem.",
        "indications": ["Hemorrhoids (Bawaseer)", "Anal fissures", "Post-partum pelvic toning", "Prostatitis / Pelvic floor spasm"],
        "contraindications": ["Active acute pelvic hemorrhage", "Unexplained mass"],
        "evidence_grade": "A (Standard Proctological Regimen)"
    }
}


# =============================================================================
# 2. THE 7 CORE THERAPEUTIC PRINCIPLES (USOOL-E-TADBEER)
# =============================================================================

USOOL_E_TADBEER_PRINCIPLES = {
    "Tanqiya": "Evacuation: Removing excess or morbid matter (Mawad-e-Fasida) via Hijama, Fasd, Huqna, Ishal, or Qai.",
    "Ta'deel": "Moderation: Restoring balance in temperament and humors through lifestyle and gentle regimen.",
    "Tahleel": "Resolution: Dissolving and dispersing accumulated pathological inflammatory substances via Dalak, Takmeed, or Hammam.",
    "Taqwiyat": "Strengthening: Enhancing organ function and vital force (Quwwat-e-Mudabbira-e-Badan) via Riyazat and nourishing Dalak.",
    "Tabreed_Taskheen": "Thermal Alteration: Modifying local or systemic temperature through hot or cold hydrotherapy/compresses.",
    "Tarteeb": "Moistening: Addressing pathological dryness through oil massage (Dalak-e-Duhni) and warm baths.",
    "Tabyees": "Drying: Managing excess morbid moisture through thermogenic sweating (Tareeq) and vigorous exercise."
}


# =============================================================================
# 3. CONDITION-SPECIFIC MULTI-MODAL PROTOCOLS (CHAPTER 3 & APPENDIX C)
# =============================================================================

MULTI_MODAL_TREATMENT_TRAJECTORIES: Dict[str, Dict[str, Any]] = {
    "Chronic_Low_Back_Pain": {
        "protocol_id": "PROTO-TADB-001",
        "title": "Chronic Lower Back Pain Multi-Modal Trajectory",
        "phases": {
            "Week_1_to_2": "Dalak-e-Layyin (Massage with Roghan-e-Baqla/Badam) + Takmeed Haar (Hot compress) + Gentle Riyazat walking.",
            "Week_3_to_4": "Introduce Hijama bila-Shart on bilateral lumbar musculature; progress to graduated spinal stability exercises.",
            "Ongoing": "Daily 20-min brisk walk, ergonomic sitting adjustments, core strengthening Riyazat."
        },
        "target_outcome": "50-70% pain score reduction and restored lumbar range of motion."
    },
    "IBS_Mizaj_Divergent": {
        "protocol_id": "PROTO-TADB-002",
        "title": "Irritable Bowel Syndrome (IBS) Temperament-Divergent Protocol",
        "clinical_pearl": "Balghami IBS requires warming & drying; Safrawi IBS requires cooling & moistening. Same diagnosis, opposite regimens.",
        "sub_protocols": {
            "Balghami_IBS": {
                "mizaj_type": "Cold & Moist (Phlegmatic)",
                "regimen": [
                    "Warming Riyazat (brisk cardiovascular walking)",
                    "Dalak-e-Batan (Abdominal massage) clockwise with warm Roghan-e-Zaitoon or ginger oil",
                    "Ginger-infused warm Huqna (enema) for colonic mucus clearance",
                    "Elimination of cold dairy and raw refrigerated foods"
                ]
            },
            "Safrawi_IBS": {
                "mizaj_type": "Hot & Dry (Choleric)",
                "regimen": [
                    "Gentle cooling exercise (swimming in ambient water)",
                    "Abdominal massage with soothing Rose or Almond oil",
                    "Soothing demulcent Huqna (Ispaghol husk decoction / Arq-e-Gulab)",
                    "Elimination of chillies, fried spices, and high-heat cooking"
                ]
            }
        },
        "clinical_evidence": "75% sustained symptom relief and PPI discontinuation within 30 days (Dr. Ashraf Clinical Cohort)."
    },
    "Knee_Osteoarthritis": {
        "protocol_id": "PROTO-TADB-003",
        "title": "Knee Osteoarthritis / Waja-ul-Mafasil Multi-Modal Protocol",
        "regimen": [
            "Dalak around joint margins with warming oils (Roghan-e-Suranjan)",
            "Takmeed Haar with castor oil compress for 20 mins daily",
            "Hijama bila-Shart over peri-patellar tender zones once every 2 weeks",
            "Low-impact cycling or water aerobics to preserve cartilage"
        ],
        "refractory_escalation": "Cauterization (Kai) by certified Unani surgeon if chronic intractable pain persists without surgical fracture."
    },
    "Tension_Headache_Migraine": {
        "protocol_id": "PROTO-TADB-004",
        "title": "Tension Headache & Sudaa Regimental Protocol",
        "regimen": [
            "Cold compress (Takmeed Barid) across forehead and temporal arteries",
            "Gentle scalp and cranial massage (Dalk-e-Ra's) with oil of violet (Roghan-e-Banafsha)",
            "Inkebab (Steam inhalation) with peppermint/mint leaves",
            "Rest in dark, quiet environment; hydration with 500 mL water."
        ]
    }
}


# =============================================================================
# 4. HOME-BASED SELF-CARE KITS & PRACTICES (PART 2 & 4 OF HANDBOOK)
# =============================================================================

HOME_SELF_CARE_SPEC = {
    "basic_kit_under_500_inr": [
        {"item": "Coconut or Olive Oil", "cost_est": 100, "use": "Self-massage of belly, feet, or scalp"},
        {"item": "Hot Water Bag", "cost_est": 150, "use": "Warm compress on abdomen, back, or stiff joints"},
        {"item": "Clean Towels (2)", "cost_est": 0, "use": "Moist fomentation or steam tenting"},
        {"item": "Small Steaming Pot", "cost_est": 0, "use": "Herbal steam inhalation (Inkebab)"}
    ],
    "clockwise_belly_massage_protocol": {
        "purpose": "Stimulates colonic motility along ascending, transverse, and descending colon; relieves cramps and constipation.",
        "duration_minutes": 10,
        "instructions": [
            "Warm a small amount of coconut or olive oil between palms.",
            "Lie comfortably on your back with knees slightly bent.",
            "Place palm on lower right abdomen, move upwards to right ribcage, across to left ribcage, and down to lower left pelvis.",
            "Repeat circular clockwise motion gently for 5 to 10 minutes before bedtime."
        ]
    },
    "contrast_bath_protocol": {
        "purpose": "Vascular pumping mechanism to relieve peripheral edema, foot ache, and autonomic fatigue.",
        "instructions": [
            "Prepare two basins: One warm water (38-40°C), one cool water (15-20°C).",
            "Immerse feet in warm water for 3 minutes.",
            "Switch to cool water for 1 minute.",
            "Repeat cycle 3 times, always ending on cool water."
        ]
    }
}


# =============================================================================
# 5. ACUTE MEDICAL RED-FLAGS TRIAGE GUARD (PART 5)
# =============================================================================

ACUTE_MEDICAL_RED_FLAGS = [
    "chest pain", "difficulty breathing", "shortness of breath", "severe sudden onset pain",
    "fever over 102", "fever > 102", "high fever persisting", "fever persisting >3 days",
    "vomiting blood", "severe headache with vision problems", "loss of consciousness",
    "sudden weakness", "sudden numbness", "severe abdominal pain", "coughing blood"
]


# =============================================================================
# 6. CORE GUARDRAIL EXECUTION FUNCTION
# =============================================================================

def run_tadbeer_guardrails(
    *,
    patient_context: dict[str, Any],
    plan: dict[str, Any],
) -> dict[str, Any]:
    """
    Evaluates safety of a proposed Tadbeer (regimenal therapy) plan against
    the patient's clinical safety context, checking both general contraindications
    and modality-specific physiological thresholds.
    """
    verdict = "SAFE_TO_CONSIDER"
    reasons: list[str] = []

    procedure_name = (plan.get("name") or "").lower()
    category = (plan.get("category") or "").lower()
    method = (plan.get("method") or "").lower()
    indication = (plan.get("indication") or "").lower()

    age = patient_context.get("age")
    pregnancy = patient_context.get("pregnancy_status") == "pregnant"
    lactation = patient_context.get("lactation_status") == "yes"
    medications = [m.lower() for m in (patient_context.get("current_medications") or [])]
    comorbidities = [c.lower() for c in (patient_context.get("comorbidities") or [])]
    complaint = (patient_context.get("chief_complaint") or "").lower()

    # -------------------------------------------------------------------------
    # Red-Flag Emergency Triage Screening
    # -------------------------------------------------------------------------
    combined_clinical_notes = complaint + " " + " ".join(comorbidities)
    for rf in ACUTE_MEDICAL_RED_FLAGS:
        if rf in combined_clinical_notes:
            verdict = "REFER"
            reasons.append(
                f"ACUTE MEDICAL RED FLAG DETECTED: '{rf}'. In accordance with Part 5 of Ilaj bil Tadbeer guidelines, "
                "elective regimental therapy is halted. Patient requires immediate emergency allopathic medical evaluation."
            )
            return {
                "verdict": "REFER",
                "reasons": reasons,
                "emergency_red_flag_triggered": True,
                "requiresImmediateMedicalAttention": True
            }

    has_anticoagulant = any(
        kw in med
        for med in medications
        for kw in ["warfarin", "heparin", "apixaban", "rivaroxaban", "dabigatran", "clopidogrel", "anticoagulant", "aspirin"]
    )
    has_bleeding_disorder = any(
        kw in c
        for c in comorbidities + [complaint]
        for kw in ["hemophilia", "thrombocytopenia", "bleeding disorder", "itp", "purpura"]
    )
    has_anemia = any("anemia" in c or "low hemoglobin" in c or "anaemia" in c for c in comorbidities + [complaint])
    has_hypotension = any("hypotension" in c or "low blood pressure" in c or "shock" in c for c in comorbidities + [complaint])
    has_fever = any("fever" in c or "bukhar" in c or "humma" in c for c in comorbidities + [complaint])
    has_dvt = any("dvt" in c or "deep vein thrombosis" in c or "thrombophlebitis" in c or "clot in leg" in c for c in comorbidities + [complaint])
    has_uncontrolled_diabetes = any("uncontrolled diabetes" in c or "diabetic neuropathy" in c for c in comorbidities)

    # 1. HIJAMA (CUPPING THERAPY)
    if "hijama" in procedure_name or "cupping" in procedure_name:
        is_wet = "wet" in procedure_name or "wet" in method or "shart" in procedure_name or "shart" in method
        if is_wet:
            if has_bleeding_disorder or has_anticoagulant:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append("Hijama bil-Shart (Wet Cupping) is strictly contraindicated in patients on anticoagulants or with active coagulopathies.")
            if has_anemia:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append("Hijama bil-Shart (Wet Cupping) is contraindicated in moderate-to-severe anemia; risks precipitating hypovolemic crisis.")
            if has_hypotension:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append("Wet Cupping is contraindicated during acute hypotension or hemodynamic instability.")
        if pregnancy:
            is_pelvic = any(k in method or k in indication for k in ["abdomen", "sacral", "lumbar", "pelvic", "back"])
            if is_pelvic:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append("Hijama over abdominal or lumbosacral regions is contraindicated in pregnancy due to reflex uterine hyperstimulation.")
            else:
                verdict = _escalate(verdict, "CAUTION")
                reasons.append("Pregnancy precaution: Hijama requires strict vital monitoring and non-invasive application.")

    # 2. FASD (VENESECTION)
    if "fasd" in procedure_name or "venesection" in procedure_name or "phlebotomy" in procedure_name:
        if age is not None:
            if age < 14:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append("Fasd is strictly contraindicated in pediatric patients under 14 years of age (Canon of Medicine §Fasd Rules).")
            elif age > 60:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append("Fasd is contraindicated in elderly patients exceeding 60 years of age due to failure of Tabiyat recovery.")
        if pregnancy:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Fasd is absolutely contraindicated during pregnancy.")
        if has_anemia or has_hypotension or has_bleeding_disorder:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Fasd is contraindicated in anemia, hypotension, or coagulopathy.")

    # 3. HAMMAM (MEDICATED BATHS)
    if "hammam" in procedure_name or "bath" in procedure_name or category == "bathing":
        if has_fever:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Hot Hammam is contraindicated in acute febrile illness (Humma-e-Hadda); exacerbates core hyperthermia.")
        if any("cardiac" in c or "heart failure" in c or "angina" in c for c in comorbidities):
            verdict = _escalate(verdict, "CAUTION")
            reasons.append("Hammam causes peripheral vasodilation; requires monitoring in cardiovascular disease.")

    # 4. DALAK (MEDICAL MASSAGE)
    if "dalak" in procedure_name or "massage" in procedure_name or category == "massage":
        if has_dvt:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Medical massage is STRICTLY CONTRAINDICATED in suspected or documented Deep Vein Thrombosis (DVT); extreme risk of fatal pulmonary embolism.")

    # 5. QAI (THERAPEUTIC EMESIS)
    if "qai" in procedure_name or "emesis" in procedure_name:
        has_severe_htn = any("hypertension" in c or "high blood pressure" in c for c in comorbidities)
        has_hernia = any("hernia" in c for c in comorbidities)
        if has_severe_htn or has_hernia or pregnancy:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Therapeutic emesis (Qai) is contraindicated in hypertension, hernia, or pregnancy due to severe acute intra-abdominal/cranial pressure elevation.")

    # 6. ISHAAL (THERAPEUTIC PURGATION)
    if "ishaal" in procedure_name or "purgation" in procedure_name:
        if pregnancy:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Drastic purgation (Ishaal) is contraindicated in pregnancy due to risk of inducing premature labor.")
        if any("obstruction" in c or "appendicitis" in c for c in comorbidities):
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Purgation is contraindicated in acute bowel obstruction or surgical abdomen.")

    # 7. KAI (CAUTERIZATION)
    if "kai" in procedure_name or "cauterization" in procedure_name:
        if has_uncontrolled_diabetes:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Cauterization (Kai) is contraindicated in uncontrolled diabetes or peripheral neuropathy due to risk of non-healing ulcer and gangrene.")

    # 8. TALEEQ / ZALO (LEECH THERAPY)
    if "zalo" in procedure_name or "leech" in procedure_name or "alaq" in procedure_name or "taleeq" in procedure_name:
        if has_bleeding_disorder or has_anticoagulant or has_anemia:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Leech therapy (Taleeq / Irsal-e-Alaq) is contraindicated in coagulopathy, anticoagulant use, or severe anemia due to prolonged bleeding from hirudin.")

    # 9. AABZAN (SITZ BATH)
    if "aabzan" in procedure_name or "sitz" in procedure_name:
        if any("pelvic hemorrhage" in c or "active uterine bleeding" in c for c in comorbidities):
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Aabzan (Sitz bath) is contraindicated during active acute pelvic or rectal hemorrhage.")

    # 10. RIYAZAT (EXERCISE)
    if "riyazat" in procedure_name or "exercise" in procedure_name:
        if has_fever:
            verdict = _escalate(verdict, "MODIFY")
            reasons.append("Riyazat must be suspended during acute febrile illness to conserve Tabiyat.")

    if not reasons:
        reasons.append("No contraindications identified for proposed regimenal therapy. Ensure clinical asepsis and practitioner certification.")

    return {
        "verdict": verdict,
        "reasons": reasons,
        "requiresPractitionerCertification": True,
        "evaluated_at": datetime.now(timezone.utc).isoformat()
    }
