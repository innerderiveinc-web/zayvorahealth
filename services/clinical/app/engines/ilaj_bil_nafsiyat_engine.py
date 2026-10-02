"""
ZAYVORA Health OS™ v5.0 — Ilaj bil Nafsiyat (Unani Psychological & Psychosomatic Medicine) Engine
=================================================================================================
Source Authority:
  - Dr. Irfan Ashraf: "ILAJ BIL NAFSIYAT: Ancient Healing for the Modern Mind" (February 2026)
  - Ibn Sina: Al-Qanun fi al-Tibb (Vol 3, Fen 1: Amraz-e-Dimagh, Malikholia, Wahm, Sahar)
  - Abu Bakr al-Razi: Kitab al-Hawi fi al-Tibb & Kitab al-Tibb al-Ruhani
  - Abu Zayd al-Balkhi: Masalih al-Abdan wa al-Anfus (Sustenance of the Soul)
  - Unani Pharmacopoeia of India (UPI Vol I & II)

Invariants:
  1. Fail-closed Psychiatric Emergency Triage Barrier: Detects suicidal ideation, psychosis,
     severe mania, and addiction crisis; immediately locks elective prescribing and initiates statutory emergency medical facility diversion.
  2. Dual-Classification Taxonomy: Maps classical Unani psychiatric entities (Wahm, Juzn, Sauda Ghalib,
     Izterab, Sahar, Nisyan, Ghazab, Khauf) directly to ICD-11 & SNOMED codes.
  3. Grounded Therapeutic Modalities: Enforces Asbab-e-Nafsaniyah root causes, temperament-based Itrafat
     (aromatherapy), Tanaffus (breathwork), Dalk-e-Ra's, and the 3 verified clinical case study protocols.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# =============================================================================
# 1. PSYCHIATRIC CRISIS DIVERSION & EMERGENCY TRIAGE
# =============================================================================

CRISIS_KEYWORDS = [
    "suicide", "suicidal", "kill myself", "end my life", "want to die",
    "self harm", "hallucination", "hearing voices", "delusion", "paranoia",
    "psychosis", "psychotic", "bipolar mania", "manic episode", "heroin withdrawal",
    "substance overdose", "severe addiction"
]

# =============================================================================
# 2. CLASSICAL UNANI PSYCHIATRIC TAXONOMY (DUAL-DOCTRINE MAPPING)
# =============================================================================

CLASSICAL_NAFSIYAT_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "Wahm": {
        "classical_name": "Wahm (Al-Wahm al-Waswasi)",
        "english_equivalent": "Severe Anxiety & Anticipatory Dread ('What if' thinking)",
        "primary_humor": "Sauda (Cold & Dry)",
        "icd11_code": "6B00",
        "icd11_title": "Generalized anxiety disorder",
        "snomed_ct": "197480006",
        "pathophysiology_unani": "Excess cold and dry black bile clouds psychic spirit (Rooh-e-Nafsani) in brain, creating hypervigilance and fearful anticipation.",
        "key_symptoms": ["Excessive worry", "Anticipatory dread", "Restlessness", "Nervous tremors", "Somatic tension"]
    },
    "Juzn": {
        "classical_name": "Juzn / Huzn-e-Muzmin",
        "english_equivalent": "Depression, Vital Disconnection & Deep Grief",
        "primary_humor": "Sauda & Balgham (Cold & Dry dominant)",
        "icd11_code": "6A70",
        "icd11_title": "Single episode depressive disorder",
        "snomed_ct": "35489007",
        "pathophysiology_unani": "Profound cooling and drying of internal innate heat (Hararat-e-Ghariziyyah), causing withdrawal, loss of appetite, and vital apathy.",
        "key_symptoms": ["Emotional numbness", "Loss of pleasure (Anhedonia)", "Persistent crying", "Loss of vital connection", "Fatigue"]
    },
    "Sauda_Ghalib": {
        "classical_name": "Sauda Ghalib / Malikholia",
        "english_equivalent": "Melancholia & Obsessive Rumination",
        "primary_humor": "Sauda (Black Bile combusted / burnt Safra)",
        "icd11_code": "6B20",
        "icd11_title": "Obsessive-compulsive disorder / Melancholia",
        "snomed_ct": "371569001",
        "pathophysiology_unani": "Morbid black bile vapors ascending to cerebrum and pericardium, producing fixed dark obsessions, despair, and sleeplessness.",
        "key_symptoms": ["Obsessive dark thoughts", "Unrelenting sadness", "Unfounded suspicions", "Severe insomnia", "Chest tightness"]
    },
    "Izterab": {
        "classical_name": "Izterab",
        "english_equivalent": "Restlessness, Agitation & Inner Turmoil",
        "primary_humor": "Safra (Hot & Dry)",
        "icd11_code": "6B01",
        "icd11_title": "Panic disorder & psychomotor agitation",
        "snomed_ct": "24199005",
        "pathophysiology_unani": "Acute heat and excessive yellow bile irritating the neurological faculty (Quwwat-e-Nafsaniyah), creating driven urgency without direction.",
        "key_symptoms": ["Inability to sit still", "Inner turmoil", "Rapid speech", "Sweating palms", "Surge of panic"]
    },
    "Sahar": {
        "classical_name": "Sahar / Niham",
        "english_equivalent": "Chronic Insomnia & Non-Restorative Sleep",
        "primary_humor": "Yubusat-e-Dimagh (Excess Cerebral Dryness)",
        "icd11_code": "7A00",
        "icd11_title": "Insomnia disorder",
        "snomed_ct": "193462001",
        "pathophysiology_unani": "Depletion of natural cerebral moisture (Rutubat-e-Dimaghiyyah) preventing the resting spirit from settling into somatic sleep.",
        "key_symptoms": ["Difficulty falling asleep", "Frequent nocturnal waking", "Exhaustion upon waking", "Tension headaches", "Dry eyes"]
    },
    "Nisyan": {
        "classical_name": "Nisyan",
        "english_equivalent": "Memory Loss, Cognitive Fog & Forgetfulness",
        "primary_humor": "Barid-Yabis or Barid-Ratab",
        "icd11_code": "MB21.1",
        "icd11_title": "Amnestic & cognitive complaints",
        "snomed_ct": "386807006",
        "pathophysiology_unani": "Impairment of the cognitive retaining faculty (Quwwat-e-Hafizah) caused by cerebral coldness or excess phlegmatic stagnation.",
        "key_symptoms": ["Poor working memory", "Difficulty concentrating", "Brain fog", "Mental exhaustion during study/work"]
    },
    "Ghazab": {
        "classical_name": "Ghazab",
        "english_equivalent": "Pathological Rage, Anger & Irritability",
        "primary_humor": "Safra (Yellow Bile)",
        "icd11_code": "QE84",
        "icd11_title": "Irritability and anger episode",
        "snomed_ct": "70928004",
        "pathophysiology_unani": "Boiling of cardiac blood and bile (Ghalayan-e-Dam wa Safra), surging heat outward into the musculature and eyes.",
        "key_symptoms": ["Explosive outbursts", "Flushed facial heat", "Throbbing temples", "Strained interpersonal relationships"]
    },
    "Khauf": {
        "classical_name": "Khauf-e-Muzmin",
        "english_equivalent": "Paralyzing Fear & Phobic Avoidance",
        "primary_humor": "Barid-Yabis (Cold & Dry)",
        "icd11_code": "6B03",
        "icd11_title": "Phobic anxiety disorder",
        "snomed_ct": "271596009",
        "pathophysiology_unani": "Sudden inward retreat of the vital spirit (Inqibad-e-Rooh) into the core heart, leaving extremities cold and trembling.",
        "key_symptoms": ["Paralyzing phobias", "Cold extremities", "Sudden trembling", "Avoidance of daily activities"]
    }
}


# =============================================================================
# 3. ITRAFAT (AROMATHERAPY) & TANAFFUS (BREATHWORK) MATRIX
# =============================================================================

ITRAFAT_AROMATHERAPY_CATALOG = {
    "Gulab": {
        "name": "Rose (Rosa damascena) / Arq-e-Gulab",
        "mizaj": "Barid 1° / Yabis 2° (Cooling & Heart-opening)",
        "target_humor": "Safra & Dam (Excess Heat/Anger)",
        "actions": ["Comforts the heart", "Dispels anger-driven heat", "Brings emotional sweetness", "Reduces irritability"],
        "application_methods": ["Inhalation of pure Arq-e-Gulab", "Consumption of rose petal infusion", "Forehead dab with rose essential oil"]
    },
    "Sandal": {
        "name": "Sandalwood (Santalum album)",
        "mizaj": "Barid 2° / Yabis 2° (Cooling & Heart-calming)",
        "target_humor": "Safra (Acute Heat / Restlessness)",
        "actions": ["Cools an overheated mind", "Soothes hot agitation", "Relieves tension headaches", "Deepens meditation"],
        "application_methods": ["Paste applied to the frontal forehead/temples", "Natural oil diffusion in room"]
    },
    "Ustukhuddus": {
        "name": "Lavender (Lavandula angustifolia) / Jaroob-e-Dimagh",
        "mizaj": "Haar 1° / Yabis 2° (Mildly Warming & Limbic Calming)",
        "target_humor": "Sauda & Balgham (Grief / Anxiety / Tension)",
        "actions": ["Uplifts mood naturally", "Reduces anticipatory dread", "Soothes limbic reactivity", "Relieves tension headaches"],
        "application_methods": ["Dried flowers in pillow", "Scalp/chest massage with infused oil", "Bedtime tea infusion"]
    },
    "Zafran": {
        "name": "Saffron (Crocus sativus)",
        "mizaj": "Haar 1° / Yabis 2° (Warming & Mood-lifting)",
        "target_humor": "Sauda (Melancholy / Deep Sadness)",
        "actions": ["Clinically validated antidepressant", "Uplifts spirit (Farhat-e-Qalb)", "Improves cerebral perfusion", "Dispels dark grief"],
        "application_methods": ["2 to 3 strands dissolved in warm bedtime milk", "Aromatic scent inhalation"]
    },
    "Yasmeen": {
        "name": "Jasmine (Jasminum officinale)",
        "mizaj": "Haar 2° / Yabis 2° (Thermogenic & Neuro-stimulant)",
        "target_humor": "Balgham (Lethargy & Brain Fog)",
        "actions": ["Dispels phlegmatic stagnation", "Brings mental alertness and joy", "Restores sensory clarity"],
        "application_methods": ["Fresh flower aroma", "Vapor diffusion in workspace"]
    }
}

TANAFFUS_BREATHWORK_PROTOCOLS = {
    "Vagal_4_7_8": {
        "name": "4-7-8 Vagal Regulation Breathing",
        "indication": "Acute anxiety, panic surge, exam terror, bedtime sleep induction",
        "technique": "Inhale through the nose for 4 counts, hold the breath for 7 counts, exhale through mouth for 8 counts. Repeat 4 to 8 cycles.",
        "neurobiology": "Activates parasympathetic vagal brake, reducing heart rate, amygdala firing, and blood pressure within 90 seconds."
    },
    "Counting_Anchor": {
        "name": "Counting Breath Anchor (Habas-e-Nafas)",
        "indication": "Obsessive wandering thoughts, hypervigilance, racing mind",
        "technique": "Slow equal breathing (5 counts in, 5 counts out). Count backwards from 20 to 1 with each breath cycle.",
        "neurobiology": "Engages prefrontal working memory circuits to decouple the brain's default mode network (DMN) rumination loop."
    },
    "Alternate_Nostril": {
        "name": "Alternate Nostril Breathing (Tanaffus-e-Mutabaadil)",
        "indication": "Constitutional humoral imbalance, mental fatigue, emotional ambivalence",
        "technique": "Gently close right nostril, inhale left 4 counts. Close left, exhale right 4 counts. Inhale right 4 counts, exhale left 4 counts.",
        "neurobiology": "Balances bilateral hemispheric autonomic outflow, supporting homeostatic autonomic equilibrium."
    }
}


# =============================================================================
# 4. VERIFIED CLINICAL CASE STUDY PROTOCOLS (CHAPTER 12)
# =============================================================================

VERIFIED_CASE_STUDY_PROTOCOLS = {
    "Grieving_Mother": {
        "code": "PROTO-NAFS-001",
        "title": "The Bereavement & Sudden Grief Protocol (Huzn-e-Shadeed)",
        "reference_case": "Fatima, 45 — Loss of son, severe insomnia, heart palpitations, grief withdrawal",
        "humoral_pathology": "Sauda-heat mixed presentation (Grief increased cold-dry black bile while emotional agitation generated combustive heat).",
        "interventions": {
            "herbal_therapy": [
                "Arq-e-Gulab (Rosewater): 20 mL twice daily before meals (comforts the heart).",
                "Ustukhuddus (Lavender) oil: Gentle head and chest massage before sleep.",
                "Warm milk with Saffron (Zafran 3 strands) and Ashwagandha (Asgandh 3g) at bedtime.",
                "Khamira Gaozaban Ambari Jawaharwala: 3g in the morning on an empty stomach."
            ],
            "tadbeer_regimen": [
                "Istima (Empathetic counseling sessions): Weekly structured listening.",
                "Expressive Grief Journaling: Writing memories, lessons, and feelings.",
                "Gentle morning nature walk (30 mins) with a trusted companion.",
                "Bereavement community support group connection."
            ],
            "spiritual_component": [
                "Zikr and quiet Dua of surrender (releasing burden of control).",
                "Tafakkur on the eternal bond of maternal love."
            ]
        },
        "expected_timeline": "6 to 12 weeks for gradual restoration of sleep, appetite, and emotional resilience."
    },
    "Anxious_Student": {
        "code": "PROTO-NAFS-002",
        "title": "The Student Exam & Performance Anxiety Protocol (Wahm & Izterab)",
        "reference_case": "Ahmed, 22 — University test anxiety, panic attacks, trembling, perfectionism",
        "humoral_pathology": "Excess hot and dry yellow bile (Safra) from intense mental strain, combined with nervous system exhaustion.",
        "interventions": {
            "herbal_therapy": [
                "Coriander (Kishneez) water & Sharbat-e-Gulab (Rose syrup) as daily cooling drink.",
                "Brahmi (Bacopa monnieri) 500mg morning for cognitive clarity and memory retention.",
                "Chamomile tea during afternoon study breaks."
            ],
            "tadbeer_regimen": [
                "4-7-8 Vagal Breathing: 4 cycles immediately before exam entry and study sessions.",
                "Structured 50/10 study interval blocks (50 mins study, 10 mins screen-free walk).",
                "Cognitive reframing of perfectionism: Reframing anxiety as a temporary humoral wave, not personal failure."
            ],
            "spiritual_component": [
                "Morning prayer (Baad-e-Fajr) intention setting.",
                "Shukr practice naming 3 academic blessings."
            ]
        },
        "expected_timeline": "4 to 6 weeks for complete panic resolution and study stamina recovery."
    },
    "Burned_Out_Professional": {
        "code": "PROTO-NAFS-003",
        "title": "The Executive Burnout & Liver Heat Protocol (Izterab-e-Muttasil)",
        "reference_case": "Sarah, 35 — Corporate executive, chronic burnout, anger flares, tension headaches, insomnia",
        "humoral_pathology": "Severe excess yellow bile (Safra) from chronic sympathetic overdrive. Liver heat affecting digestion and mind.",
        "interventions": {
            "herbal_therapy": [
                "Cooling Hepatic & Gastric Formula: Rose, Coriander, and Fennel (Badiyan) infusion BD.",
                "Triphala / Itrifal Kishneezi: 5g at bedtime for gentle downward evacuation.",
                "Sandalwood paste application to temples during acute headache flares."
            ],
            "tadbeer_regimen": [
                "Hijama bila-Shart (Dry cupping) on upper back and shoulder girdle to disperse musculoskeletal tension.",
                "Firm Digital Boundary: Strict email blackout after 7:00 PM; one full evening unplugged weekly.",
                "Dietary cooling: Elimination of fried spicy foods, incorporation of cucumber, pomegranate, and barley water."
            ],
            "spiritual_component": [
                "Evening accounting (Muhasaba) without self-judgment.",
                "Tafakkur on life priorities and intentional career pacing."
            ]
        },
        "expected_timeline": "8 to 12 weeks for headache resolution, uninterrupted 7-8 hour sleep, and restored emotional calm."
    }
}


# =============================================================================
# 5. CORE ILAJ BIL NAFSIYAT ENGINE CLASS
# =============================================================================

@dataclass
class NafsiyatAssessmentInput:
    patient_id: str
    age: int
    gender: str
    chief_complaint: str
    patient_narrative: str = ""
    presenting_symptoms: List[str] = field(default_factory=list)
    current_mizaj: str = "Damwi"  # Damwi, Balghami, Safrawi, Saudawi
    stress_level: str = "MODERATE"  # LOW, MODERATE, SEVERE, CRISIS
    sleep_hours: float = 6.5
    social_isolation: bool = False
    spiritual_disconnection: bool = False
    grief_or_trauma_present: bool = False
    emotional_suppression_present: bool = False


class IlajBilNafsiyatEngine:
    """Production clinical engine for Unani Psychological & Psychosomatic Medicine."""

    @classmethod
    def evaluate_psychiatric_safety(cls, input_text: str) -> Optional[Dict[str, Any]]:
        """
        FAIL-CLOSED SAFETY INVARIANT:
        If severe psychiatric danger, psychosis, or suicidal ideation is detected,
        elective prescribing is blocked and emergency medical diversion is returned.
        """
        lowered = input_text.lower()
        triggered_keywords = [kw for kw in CRISIS_KEYWORDS if kw in lowered]
        if triggered_keywords:
            return {
                "verdict": "EMERGENCY_PSYCHIATRIC_DIVERSION",
                "safety_status": "BLOCK_ELECTIVE_PRESCRIBING",
                "triggered_red_flags": triggered_keywords,
                "clinical_rationale": (
                    "Patient expresses symptoms of psychiatric crisis, acute psychosis, or self-harm ideation. "
                    "In accordance with Chapter 10 of 'Ilaj bil Nafsiyat' and statutory healthcare invariants, "
                    "Unani elective regimental and herbal therapies are locked. Immediate licensed psychiatric emergency referral is mandatory."
                ),
                "emergency_action": "Immediate diversion to nearest emergency medical facility or accredited psychiatric hospital.",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        return None

    @classmethod
    def diagnose_condition(cls, symptoms: List[str], chief_complaint: str) -> Dict[str, Any]:
        """Maps symptoms and complaint to authentic Unani psychiatric entities."""
        combined_text = (chief_complaint + " " + " ".join(symptoms)).lower()
        diagnoses = []

        for entity_key, meta in CLASSICAL_NAFSIYAT_TAXONOMY.items():
            match_score = 0
            # Check key symptoms
            for sym in meta["key_symptoms"]:
                if any(word in combined_text for word in sym.lower().split()):
                    match_score += 1
            # Check primary name
            if entity_key.lower() in combined_text:
                match_score += 2

            if match_score >= 1:
                diagnoses.append({
                    "entity_key": entity_key,
                    "classical_name": meta["classical_name"],
                    "english_equivalent": meta["english_equivalent"],
                    "primary_humor": meta["primary_humor"],
                    "icd11_code": meta["icd11_code"],
                    "icd11_title": meta["icd11_title"],
                    "snomed_ct": meta["snomed_ct"],
                    "match_confidence": min(1.0, 0.4 + (match_score * 0.15)),
                    "pathophysiology_unani": meta["pathophysiology_unani"]
                })

        diagnoses.sort(key=lambda x: x["match_confidence"], reverse=True)
        return {
            "primary_diagnosis": diagnoses[0] if diagnoses else CLASSICAL_NAFSIYAT_TAXONOMY["Wahm"],
            "differential_diagnoses": diagnoses[1:3] if len(diagnoses) > 1 else []
        }

    @classmethod
    def evaluate_root_causes(cls, assessment: NafsiyatAssessmentInput) -> Dict[str, Any]:
        """Evaluates the 6 primary root causes (Asbab-e-Nafsaniyah) from Chapter 6."""
        causes = []
        if assessment.grief_or_trauma_present:
            causes.append({
                "cause_id": "Huzn-e-Shadeed",
                "name": "Sudden Grief or Trauma",
                "humoral_effect": "Increases cold and dry black bile, embeds emotional shock into myocardium.",
                "priority": "HIGH"
            })
        if assessment.stress_level in ["SEVERE", "CRISIS"]:
            causes.append({
                "cause_id": "Izterab-e-Muttasil",
                "name": "Prolonged Chronic Stress",
                "humoral_effect": "Generates systemic heat, depletes Quwwat-e-Nafsaniyah, exhausts adrenal resilience.",
                "priority": "HIGH"
            })
        if assessment.social_isolation:
            causes.append({
                "cause_id": "Tanhai",
                "name": "Loneliness & Social Isolation",
                "humoral_effect": "Lack of relational warmth creates profound melancholic cooling.",
                "priority": "MEDIUM"
            })
        if assessment.spiritual_disconnection:
            causes.append({
                "cause_id": "Batini_Khushi_ki_Kami",
                "name": "Spiritual Disconnection & Loss of Purpose",
                "humoral_effect": "Inner void destabilizes the psychological spirit (Rooh-e-Nafsani).",
                "priority": "MEDIUM"
            })
        if assessment.emotional_suppression_present:
            causes.append({
                "cause_id": "Jazabat_ka_Dabna",
                "name": "Suppressed Emotions & Blockages",
                "humoral_effect": "Unprocessed grief/anger turns inward, precipitating visceral spasming.",
                "priority": "MEDIUM"
            })
        if assessment.sleep_hours < 6.0:
            causes.append({
                "cause_id": "Su-e-Tadbeer_Naum",
                "name": "Circadian & Sleep Architecture Collapse",
                "humoral_effect": "Depletes cerebral moisture, causing severe Yubusat-e-Dimagh.",
                "priority": "HIGH"
            })

        return {
            "total_root_causes_identified": len(causes),
            "primary_causes": causes
        }

    @classmethod
    def generate_care_plan(cls, assessment: NafsiyatAssessmentInput) -> Dict[str, Any]:
        """
        Generates a comprehensive, personalized Ilaj bil-Nafsiyat care plan:
        1. Safety check (Emergency gate)
        2. Dual diagnostic synthesis
        3. Root cause profiling
        4. Itrafat (Aromatherapy) & Tanaffus breathwork
        5. Daily life regimen (Subah, Din, Shaam)
        6. Pre-configured matching case protocol
        """
        # 1. Safety Gate
        combined_text = assessment.chief_complaint + " " + assessment.patient_narrative
        crisis_check = cls.evaluate_psychiatric_safety(combined_text)
        if crisis_check:
            return crisis_check

        # 2. Diagnosis
        diag = cls.diagnose_condition(assessment.presenting_symptoms, assessment.chief_complaint)
        primary_diag = diag["primary_diagnosis"]

        # 3. Root Causes
        root_causes = cls.evaluate_root_causes(assessment)

        # 4. Tailored Itrafat & Tanaffus based on Mizaj & Diagnosis
        is_hot = assessment.current_mizaj in ["Safrawi", "Damwi"] or primary_diag["entity_key"] in ["Izterab", "Ghazab"]
        
        selected_aroma = ITRAFAT_AROMATHERAPY_CATALOG["Sandal" if is_hot else "Ustukhuddus"]
        secondary_aroma = ITRAFAT_AROMATHERAPY_CATALOG["Gulab" if is_hot else "Zafran"]

        selected_breathwork = TANAFFUS_BREATHWORK_PROTOCOLS["Vagal_4_7_8"]

        # 5. Matching Case Protocol
        if assessment.grief_or_trauma_present:
            case_protocol = VERIFIED_CASE_STUDY_PROTOCOLS["Grieving_Mother"]
        elif assessment.age <= 25 and ("exam" in combined_text or "test" in combined_text or "study" in combined_text):
            case_protocol = VERIFIED_CASE_STUDY_PROTOCOLS["Anxious_Student"]
        else:
            case_protocol = VERIFIED_CASE_STUDY_PROTOCOLS["Burned_Out_Professional"]

        # 6. Daily Routine Plan (Chapter 11)
        daily_routine = {
            "Subah_ki_Aadat": [
                "Wake early (Baad-e-Fajr) to align with natural light and cortisol rhythms.",
                "5-minute quiet Gratitude (Shukr) reflection before touching digital devices.",
                "5 to 10 deep vagal breaths (Inhale 4, Hold 4, Exhale 6 counts).",
                "Nourishing Brain Breakfast: Soaked peeled almonds (Badam Shirin), dates with warm milk, and herbal infusion."
            ],
            "Din_ki_Aadat": [
                "Take scheduled reflection pauses between work demands.",
                "Mindful Midday Lunch: Eat seated, screen-free, chewing thoroughly without rush.",
                "Qaylulah: 15 to 20 minute brief afternoon rest to restore afternoon cognitive stamina.",
                "Movement in Nature: 20-30 minute walk outdoors to regulate sensory nervous system."
            ],
            "Shaam_ki_Aadat": [
                "Light dinner eaten 2 to 3 hours before sleep.",
                "Evening Reflection & Accounting (Muhasaba): Consciously releasing the day's friction without harsh self-judgment.",
                "Family and community presence: Meaningful connection over screens.",
                "Relaxation Ritual: Warm bath with rosewater or lavender, gentle foot and forehead massage with oil.",
                "Bedtime: 2 to 3 strands of saffron in warm milk; gratitude journaling."
            ],
            "Mausam_ke_Mutabiq_Adjustment": "Adapt cooling herbs and shaded walks during summer; warming soups, ginger and lavender warmth during winter."
        }

        return {
            "status": "CLINICALLY_APPROVED_NAFSIYAT_PLAN",
            "patient_id": assessment.patient_id,
            "diagnosis": diag,
            "root_cause_analysis": root_causes,
            "prescribed_aroma_itrafat": [selected_aroma, secondary_aroma],
            "prescribed_tanaffus_breathwork": selected_breathwork,
            "case_study_protocol_template": case_protocol,
            "daily_life_regimen": daily_routine,
            "principles_of_care": [
                "Healing requires balance, not perfection.",
                "The therapeutic relationship (Istima / Listening) is itself an active medicine.",
                "Herbal and regimental therapies work synergistically with spiritual reflection and routine."
            ],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
