"""
ZAYVORA Health OS™ — Interactive Clinical Case Simulator Engine
===============================================================
Master Clinical Simulation & Training Engine derived from the 12-Volume Grand
Integrative Medical Library and the 38 Canonical Treatises.

Enables clinicians, postgraduate scholars, and interns to work through
multi-stage clinical decision challenges covering real-world integrative cases:
  Stage 1: Constitutional Mizaj & Humoral Diagnosis
  Stage 2: Bedside Semiology (10-Ajnas Nabz, Qaroorah & Lisaan)
  Stage 3: Phased Integrative Therapeutics (Ghiza, Tadbeer, Dawa, Yad)
  Stage 4: Statutory Pharmacovigilance, Detoxification & Safety Gates
"""

from typing import Dict, Any, List, Optional
import datetime

SIMULATOR_CASES: List[Dict[str, Any]] = [
    {
        "id": "sim-case-01",
        "case_code": "SIM-MET-01",
        "title_en": "Type 2 Diabetes Mellitus with Barid-Balghami Su-e-Mizaj & Metabolic Sluggishness",
        "title_ur": "ذیابیطس شکری نوع دوم — سوء مزاج بارد بلغمى اور میٹابولک انحطاط",
        "category": "Metabolic & Endocrine",
        "difficulty": "Intermediate",
        "volume_id": "vol-01",
        "chapter_ref": "ch-01-03",
        "patient_presentation": {
            "name": "Zafar Iqbal",
            "age": 52,
            "gender": "Male",
            "occupation": "Bank Auditor (Sedentary)",
            "chief_complaint": "Polyuria, postprandial stupor, heavy lethargy, and bilateral lower extremity tingling for 6 months.",
            "vitals": {
                "bp": "138/88 mmHg",
                "pulse": "62 bpm (Nabz-e-Batee, Layyin)",
                "temp": "36.2 °C (Sub-basal)",
                "bmi": "29.4 kg/m²"
            },
            "baseline_investigations": {
                "fasting_blood_glucose": "174 mg/dL",
                "hba1c": "8.6%",
                "fasting_insulin": "22.4 microIU/mL (HOMA-IR: 9.6 - Severe Resistance)",
                "lipid_profile": "Triglycerides: 240 mg/dL, HDL: 36 mg/dL",
                "urine_routine": "Glycosuria 2+, No albuminuria, Specific Gravity 1.028"
            }
        },
        "stages": [
            {
                "stage_number": 1,
                "stage_name": "Constitutional Mizaj & Humoral Diagnosis",
                "clinical_question": "Based on the patient's presentation (cold intolerance, postprandial stupor, pale flabby tongue, and severe insulin resistance), what is the primary pathophysiological Unani diagnostic assessment?",
                "options": [
                    "Su-e-Mizaj Har-Yabis with excessive combustion of Safra",
                    "Su-e-Mizaj Barid-Ratab (Balghami) with deficient innate metabolic fire (Hararat-e-Ghariziyyah)",
                    "Pure Damawi plethora with secondary vascular engorgement",
                    "Su-e-Mizaj Saudawi caused by acute splenic inflammation"
                ],
                "correct_option_index": 1,
                "classical_citation": "Ibn Sina, Al-Qanoon fit-Tibb, Book 3, Fen 19 (On Ziabates): 'Ziabates occurs primarily when the retentive faculty of the kidneys and metabolic transformation of the liver are impaired by coldness (Barudat) leading to rapid transit without concoction.'",
                "biomedical_rationale": "Excess cold-moist dyscrasia correlates with profound downregulation of mitochondrial AMPK phosphorylation and GLUT4 glucose transporter translocation, manifesting as severe cellular insulin resistance."
            },
            {
                "stage_number": 2,
                "stage_name": "Bedside Semiology (Pulse, Urine & Tongue)",
                "clinical_question": "Which specific 10-Ajnas pulse waveform (Nabz) and Qaroorah (urine) characteristics confirm this Barid-Balghami metabolic state?",
                "options": [
                    "Nabz-e-Saree, Azeem, Sulb (Rapid, Large, Hard) with fiery yellow concentrated urine",
                    "Nabz-e-Batee, Saghir, Layyin (Slow, Small, Soft) with pale, voluminous, low-viscosity Qaroorah and white sediment",
                    "Nabz-e-Ghazali (Dicrotic, Bounding) with dark brown smoky urine",
                    "Nabz-e-Munqati (Intermittent) with saffron-tinged foam"
                ],
                "correct_option_index": 1,
                "classical_citation": "Ali ibn al-Abbas al-Majusi, Kamil al-Sina'a al-Tibbiyya, Discourse 2: 'The pulse of Barudat and Balgham is uniformly Batee (slow), Layyin (soft to compression), and Saghir (small volume).'",
                "biomedical_rationale": "Soft and slow pulse reflects diminished sympathetic vascular tone and microvascular sluggishness, while pale copious urine denotes renal clearance of un-metabolized glucose without biliary pigments."
            },
            {
                "stage_number": 3,
                "stage_name": "Phased Integrative Therapeutic Strategy",
                "clinical_question": "What is the most appropriate first-line therapeutic regimen for Phase 1 metabolic harmonization?",
                "options": [
                    "High-dose cold purgatives (Mushil-e-Safra) with ice-cold tamarind sherbet",
                    "Thermogenic posology: Jamun seed + Karela powder with Qurs-e-Ziabates and warm cinnamon infusion, accompanied by 16-hour intermittent fasting (Faqah)",
                    "Heavy meat stews (Yakhni) and bed rest to preserve energy",
                    "Immediate wet cupping (Hijama Ma'a Shart) over the splenic region"
                ],
                "correct_option_index": 1,
                "classical_citation": "Hakim Kabiruddin, Bayaz-e-Kabir, Vol. II: 'Ziabates with cold phlegmatic signs mandates Muharrik-e-Hararat botanicals (Jamun, Karela, Darchini) to awaken innate digestive heat.'",
                "biomedical_rationale": "Cinnamon and bitter charantin upregulate AMPK signaling and enhance peripheral insulin sensitivity, while intermittent fasting induces hepatic autophagy and reduces gluconeogenesis."
            },
            {
                "stage_number": 4,
                "stage_name": "Statutory Pharmacovigilance & Safety Barrier",
                "clinical_question": "If introducing Kushta-e-Baiza-e-Murgh or mineral adjuvants into this diabetic regimen, what statutory clinical governance standard must be verified?",
                "options": [
                    "No verification needed if prescribed by a local traditional healer",
                    "Mandatory 21 CFR Part 11 SHA-256 HMAC electronic signature, heavy-metal safety screening, and renal function (eGFR) monitoring",
                    "Immediate co-administration with high-dose corticosteroids",
                    "Dispensing un-pulverized raw ingredients directly to the patient"
                ],
                "correct_option_index": 1,
                "classical_citation": "ZAYVORA Clinical Governance Framework, Rule 12-E: 'All calcined organo-metallic Kushtajat require verified Certificate of Analysis (COA), atomic absorption spectroscopy, and non-delegable clinician digital seal.'",
                "biomedical_rationale": "Ensures complete bioavailability without nephrotoxic or heavy-metal residues, strictly protecting the patient's baseline renal clearance."
            }
        ]
    },
    {
        "id": "sim-case-02",
        "case_code": "SIM-RHEUM-02",
        "title_en": "Rheumatoid Arthritis (Waja-ul-Mafasil) with Saudawi-Balghami Joint Stagnation",
        "title_ur": "وجع المفاصل بلغمی و سوداوی — سوزشِ مفاصل اور مدافعتی بگاڑ",
        "category": "Musculoskeletal & Immunology",
        "difficulty": "Advanced",
        "volume_id": "vol-08",
        "chapter_ref": "ch-08-02",
        "patient_presentation": {
            "name": "Shabana Begum",
            "age": 46,
            "gender": "Female",
            "occupation": "School Teacher",
            "chief_complaint": "Severe bilateral symmetrical swelling and early morning stiffness (>90 min) in PIP and MCP joints for 8 months.",
            "vitals": {
                "bp": "126/80 mmHg",
                "pulse": "78 bpm (Nabz-e-Sulb, Munshari)",
                "temp": "37.0 °C",
                "bmi": "24.1 kg/m²"
            },
            "baseline_investigations": {
                "rf_titre": "94 IU/mL (Strongly Positive)",
                "anti_ccp": "128 U/mL (Strongly Positive)",
                "hs_crp": "18.4 mg/L (Markedly Elevated)",
                "esr": "54 mm/1st hr",
                "serum_uric_acid": "5.2 mg/dL (Normal)"
            }
        },
        "stages": [
            {
                "stage_number": 1,
                "stage_name": "Humoral Etiology & Diagnostic Synthesis",
                "clinical_question": "What is the classical Unani humoral classification of chronic autoimmune articular erosions with morning stiffness?",
                "options": [
                    "Waja-ul-Mafasil Balghami-Saudawi with accumulation of viscid morbid humors (Akhlat-e-Raddiyya) in joint cavities",
                    "Acute Safrawi arthritis caused by excessive citrus consumption",
                    "Isolated trauma-induced mechanical synoviopathy",
                    "Spontaneous idiopathic neurosis"
                ],
                "correct_option_index": 0,
                "classical_citation": "Al-Razi, Kitab al-Hawi fit-Tibb, Vol. 11 (On Joint Diseases): 'When the joints receive cold, thick humors that the natural faculty fails to resolve, they stagnate and solidify into intractable pain and deformity.'",
                "biomedical_rationale": "Corresponds to chronic immune-complex mediated synovial hyperplasia, pannus formation, and systemic pro-inflammatory cytokine elevation (TNF-alpha, IL-6, IL-1beta)."
            },
            {
                "stage_number": 2,
                "stage_name": "Bedside Tactile Diagnostics & Tongue Examination",
                "clinical_question": "Which tactile joint finding and tongue sign are pathognomonic of Waja-ul-Mafasil with Saudawi-Balghami stagnation?",
                "options": [
                    "Scalding hot erythema with thin bright yellow tongue coat",
                    "Boggy, non-pitting synovial swelling with periarticular coolness and a thick dull white-grey tongue coat with lateral dental indentations",
                    "Dry scaly petechiae with normal clean pink tongue",
                    "Flaccid muscle paresis with completely smooth red tongue"
                ],
                "correct_option_index": 1,
                "classical_citation": "Ibn Sina, Al-Qanoon fit-Tibb, Book 3, Fen 22: 'Cold phlegmatic joint swellings are soft, pale or dusky, lacking acute redness, worsening with cold contact.'",
                "biomedical_rationale": "Boggy coolness reflects chronic proliferative synovitis with stagnant lymphatic drainage, while tongue indentations indicate systemic fluid retention and tissue hypoperfusion."
            },
            {
                "stage_number": 3,
                "stage_name": "Phased Prescribing & Compound Formulation",
                "clinical_question": "What is the classical drug of choice in Unani pharmacopoeia for resolving joint pain and its mandatory Musleh (corrective)?",
                "options": [
                    "Afeem (Opium) alone in large doses without any corrector",
                    "Suranjan Shireen (Colchicum autumnale) paired with Katira / Samagh-e-Arabi and Zanjabeel as Musleh",
                    "Excessive ingestion of vinegar and cold curds",
                    "Continuous dry cold compresses over affected joints"
                ],
                "correct_option_index": 1,
                "classical_citation": "Hakim Najmul Ghani, Khazain-ul-Advia, Vol. 3: 'Suranjan is the sovereign antidote for joints (Dawa-e-Mafasil); its corrector is Katira and Zanjabeel to prevent gastrointestinal griping and mucosal irritation.'",
                "biomedical_rationale": "Suranjan provides bioactive colchicine, which inhibits tubulin polymerization, arrests neutrophil chemotaxis into the synovium, and suppresses the NLRP3 inflammasome."
            },
            {
                "stage_number": 4,
                "stage_name": "Schedule E(1) Statutory Mudabbar Gate",
                "clinical_question": "Suranjan Talkh (Bitter Colchicum) is classified under Schedule E(1) as a statutory poison. What mandatory detoxification SOP is legally and clinically required before dispensing?",
                "options": [
                    "No SOP needed; raw roots can be powdered directly",
                    "Mandatory Mudabbar process: Soaking and boiling in pure cow's milk (Sheer-e-Gao) for 12 hours followed by desiccation and shade-drying",
                    "Washing with alcohol and immediate flame roasting",
                    "Mixing with high-dose synthetic NSAIDs without declaration"
                ],
                "correct_option_index": 1,
                "classical_citation": "NFUM Part-II & Drugs and Cosmetics Rules 1945, Schedule E(1): 'Suranjan Talkh must undergo Shodhana/Tadbeer in cow's milk to eliminate lethal toxic alkaloids while preserving therapeutic colchicosides.'",
                "biomedical_rationale": "Milk lipids and casein bind toxic colchicine degradants, mitigating cardiotoxicity and severe hemorrhagic gastroenteritis while maintaining anti-inflammatory efficacy."
            }
        ]
    },
    {
        "id": "sim-case-03",
        "case_code": "SIM-HEP-03",
        "title_en": "Hepatic Safrawi Dyskinesia & Non-Alcoholic Steatohepatitis (NASH)",
        "title_ur": "سوء مزاج حار کبد — صفراوی سوزش اور جگر پر چربی کا علاج",
        "category": "Gastroenterology & Hepatology",
        "difficulty": "Intermediate",
        "volume_id": "vol-04",
        "chapter_ref": "ch-04-01",
        "patient_presentation": {
            "name": "Hamid Raza",
            "age": 42,
            "gender": "Male",
            "occupation": "Restaurant Manager",
            "chief_complaint": "Right upper quadrant dull heaviness, bitter morning taste, postprandial nausea, and chronic fatigue.",
            "vitals": {
                "bp": "132/84 mmHg",
                "pulse": "82 bpm (Nabz-e-Saree, Sulb)",
                "temp": "37.1 °C",
                "bmi": "31.2 kg/m²"
            },
            "baseline_investigations": {
                "alt": "76 U/L (Elevated)",
                "ast": "58 U/L (Elevated)",
                "gamma_gt": "92 U/L (Elevated)",
                "fibroscan_cap": "314 dB/m (Grade S3 Severe Hepatic Steatosis)",
                "fibroscan_e": "7.8 kPa (Stage F1-F2 Early Fibrosis)"
            }
        },
        "stages": [
            {
                "stage_number": 1,
                "stage_name": "Etiological Synthesis & Organ Mizaj",
                "clinical_question": "What is the primary organ dyscrasia (Su-e-Mizaj Jigar) indicated by elevated transaminases, bitter taste, and Grade S3 steatosis?",
                "options": [
                    "Su-e-Mizaj Barid-Ratab of the liver with secondary Safrawi combustion (Ihtiraq-e-Safra) and hepatic microvascular congestion (Suddah Jigar)",
                    "Isolated splenic atrophy with complete bile deficiency",
                    "Pure neurological migraine with psychosomatic vomiting",
                    "Excessive drying of the lungs with no hepatic involvement"
                ],
                "correct_option_index": 0,
                "classical_citation": "Ibn Sina, Al-Qanoon fit-Tibb, Book 3, Fen 4 (On Diseases of the Liver): 'Obstructions in the hepatic venules (Sudad-e-Jigar) occur when thick nutrient chyme meets burning Safra, culminating in heaviness and functional failure.'",
                "biomedical_rationale": "Hepatic steatosis causes mitochondrial uncoupling and lipid peroxidation, generating reactive oxygen species (ROS) that trigger transaminase leakage and stellate cell fibrogenesis."
            },
            {
                "stage_number": 2,
                "stage_name": "Bedside Physical Signs & Qaroorah Analysis",
                "clinical_question": "Which clinical examination findings confirm active hepatobiliary Safrawi congestion?",
                "options": [
                    "Milky white urine with soft, sunken pulse",
                    "Slight subicteric sclera, tender hepatomegaly on deep inspiration, deep amber-saffron Qaroorah with transient yellow foam, and yellowish tongue dorsum coat",
                    "Completely clear colorless urine with bradycardia 40 bpm",
                    "Severe pitting pedal edema with cyanotic nailbeds"
                ],
                "correct_option_index": 1,
                "classical_citation": "Ali ibn al-Abbas al-Majusi, Kamil al-Sina'a, Discourse 2: 'Yellow-orange urine with foam that stains linen indicates that Safra has overflowed into the bloodstream from hepatic obstruction.'",
                "biomedical_rationale": "Directly correlates with elevated conjugated bilirubin and urinary urobilinogen excretion during active hepatobiliary inflammation."
            },
            {
                "stage_number": 3,
                "stage_name": "Phased Hepatoprotective Formulation",
                "clinical_question": "What is the evidence-based Unani compound formulation pair proven to resolve hepatic steatosis and normalize liver enzymes?",
                "options": [
                    "Heavy animal fats and red wine",
                    "Sharbat-e-Deenar + Arq Mako (Solanum nigrum) and Arq Kasni (Cichorium intybus) with Tukhm-e-Kasni infusion",
                    "High-dose synthetic paracetamol 4g daily",
                    "Strict prolonged water-only fasting for 40 continuous days"
                ],
                "correct_option_index": 1,
                "classical_citation": "Hakim Kabiruddin, Bayaz-e-Kabir, Vol. I: 'For hepatic obstruction and burning dyscrasia, Arq Mako and Arq Kasni serve as the supreme deobstruent (Mufattih) and cooling hepatoprotective.'",
                "biomedical_rationale": "Cichorium intybus and Solanum nigrum contain chicoric acid and solamargine, which activate Nrf2 antioxidant pathways, downregulate SREBP-1c lipogenesis, and reduce hepatic steatosis."
            },
            {
                "stage_number": 4,
                "stage_name": "CYP450 Herb-Drug Safety Governance",
                "clinical_question": "If the patient is concurrently taking prescription Atorvastatin 20mg, what clinical safety caution must be applied regarding herb-drug interaction?",
                "options": [
                    "No caution needed; natural herbs never interact with modern drugs",
                    "Monitor for CYP3A4 inhibition; avoid excessive co-administration of concentrated grapefruit/citrus extracts; schedule liver function testing at 4 weeks",
                    "Immediately triple the statin dose without medical supervision",
                    "Stop all hydration and fluids completely"
                ],
                "correct_option_index": 1,
                "classical_citation": "ZAYVORA Pharmacovigilance Manual §14: 'Herb-Drug Matrix: Concurrent administration of hepatically metabolized pharmaceuticals mandates baseline and 30-day LFT tracking to ensure therapeutic safety.'",
                "biomedical_rationale": "Protects against competitive CYP450 enzyme saturation, ensuring neither statin toxicity (rhabdomyolysis) nor botanical clearance failure occurs."
            }
        ]
    }
]

class CaseSimulatorEngine:
    """Clinical Case Simulator & Medical Competency Grading Engine."""

    @classmethod
    def get_all_cases(cls) -> List[Dict[str, Any]]:
        """Returns catalog of all available interactive clinical cases."""
        catalog = []
        for c in SIMULATOR_CASES:
            catalog.append({
                "id": c["id"],
                "case_code": c["case_code"],
                "title_en": c["title_en"],
                "title_ur": c["title_ur"],
                "category": c["category"],
                "difficulty": c["difficulty"],
                "total_stages": len(c["stages"]),
                "patient_name": c["patient_presentation"]["name"],
                "patient_age": c["patient_presentation"]["age"],
                "chief_complaint": c["patient_presentation"]["chief_complaint"]
            })
        return catalog

    @classmethod
    def get_case_by_id(cls, case_id: str, sanitize_answers: bool = True) -> Optional[Dict[str, Any]]:
        """
        Returns full case challenge details.
        If sanitize_answers is True, strips out correct_option_index and rationale
        so students/doctors cannot inspect answers before submitting.
        """
        case_match = None
        for c in SIMULATOR_CASES:
            if c["id"].lower() == case_id.strip().lower() or c["case_code"].lower() == case_id.strip().lower():
                case_match = c
                break

        if not case_match:
            return None

        if not sanitize_answers:
            return case_match

        sanitized_stages = []
        for s in case_match["stages"]:
            sanitized_stages.append({
                "stage_number": s["stage_number"],
                "stage_name": s["stage_name"],
                "clinical_question": s["clinical_question"],
                "options": s["options"]
            })

        return {
            "id": case_match["id"],
            "case_code": case_match["case_code"],
            "title_en": case_match["title_en"],
            "title_ur": case_match["title_ur"],
            "category": case_match["category"],
            "difficulty": case_match["difficulty"],
            "volume_id": case_match.get("volume_id"),
            "chapter_ref": case_match.get("chapter_ref"),
            "patient_presentation": case_match["patient_presentation"],
            "stages": sanitized_stages
        }

    @classmethod
    def evaluate_case_submission(
        cls,
        case_id: str,
        user_answers: Dict[int, int],
        clinician_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluates submitted stage answers, calculates competency score (0-100%),
        and provides comprehensive academic explanations and classical citations.
        """
        case_full = cls.get_case_by_id(case_id, sanitize_answers=False)
        if not case_full:
            return {"ok": False, "error": f"Case '{case_id}' not found."}

        total_stages = len(case_full["stages"])
        correct_count = 0
        stage_evaluations = []

        for stage in case_full["stages"]:
            st_num = stage["stage_number"]
            user_choice = user_answers.get(st_num)
            correct_choice = stage["correct_option_index"]
            is_correct = (user_choice == correct_choice)

            if is_correct:
                correct_count += 1

            stage_evaluations.append({
                "stage_number": st_num,
                "stage_name": stage["stage_name"],
                "clinical_question": stage["clinical_question"],
                "user_selected_index": user_choice,
                "user_selected_text": stage["options"][user_choice] if user_choice is not None and 0 <= user_choice < len(stage["options"]) else "None / Unanswered",
                "correct_option_index": correct_choice,
                "correct_option_text": stage["options"][correct_choice],
                "is_correct": is_correct,
                "classical_citation": stage.get("classical_citation", ""),
                "biomedical_rationale": stage.get("biomedical_rationale", "")
            })

        score_pct = round((correct_count / total_stages) * 100, 1) if total_stages > 0 else 0

        if score_pct >= 90:
            rank = "Master Integrative Physician (Tabeeb-e-Haziq)"
            badge_color = "#2D6A4F"
        elif score_pct >= 75:
            rank = "Senior Clinical Resident (Tabeeb-e-Mahir)"
            badge_color = "#3A86FF"
        elif score_pct >= 50:
            rank = "Junior Practitioner (Tabeeb-e-Muta'allim)"
            badge_color = "#F4A261"
        else:
            rank = "Requires Remedial Doctrinal Study"
            badge_color = "#E63946"

        return {
            "ok": True,
            "case_id": case_full["id"],
            "case_title": case_full["title_en"],
            "clinician_id": clinician_id or "CLINICIAN-GUEST",
            "score_percentage": score_pct,
            "correct_stages": correct_count,
            "total_stages": total_stages,
            "clinical_competency_rank": rank,
            "rank_badge_color": badge_color,
            "stage_evaluations": stage_evaluations,
            "recommended_study": [
                f"Grand Library Volume: {case_full.get('volume_id', 'vol-01').upper()}",
                f"Canonical Chapter: {case_full.get('chapter_ref', 'ch-01-01')}",
                "Review Bedside Tactile Semiology manual and Schedule E(1) Mudabbar SOPs"
            ],
            "evaluated_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
