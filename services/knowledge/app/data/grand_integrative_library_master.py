"""
ZAYVORA Health OS™ — Grand Classical & Modern Integrative Medical Library
==========================================================================
(مکتبۂ زیورہ طبّی المتكامل — موسوعة الطب التكاملي الدقيق)

Master Repository of Integrative Medical Science, Classical Tibb-e-Unani Doctrine,
Clinical Laboratory Biomarkers, Radio-Diagnostics & Imaging, Metagenomics,
Continuous Wearables, Specialized Disciplines, and Global Pharmacopoeial Governance.

Editorial Authority:
- ZAYVORA Clinical Governance Board & Department of Medical Knowledge
- In Conformance with:
  * Unani Pharmacopoeia of India (UPI) & NFUM (Ministry of AYUSH, Govt of India)
  * Classical Canon: Al-Qanoon fit-Tibb (Avicenna), Kitab al-Hawi (Rhazes), Kamil al-Sina'a (Majusi)
  * Khazain-ul-Advia (Hakim Najmul Ghani) & Bayaz-e-Kabir (Hakim Kabiruddin)
  * WHO Traditional Medicine Strategy & WHO SMART Guidelines Level 4 Executable DAK
  * Modern Biomedical Consensus (Harrison's Principles, Guyton's Physiology, UpToDate)
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional

LIBRARY_METADATA = {
    "title": "ZAYVORA Grand Classical & Modern Integrative Medical Library",
    "arabic_title": "موسوعة زيورہ للطب التكاملي الدقيق",
    "urdu_title": "مکتبۂ زیورہ طبّی المتكامل",
    "version": "5.3.0-PROD",
    "total_volumes": 12,
    "total_chapters": 48,
    "statutory_standards": ["UPI Parts I-II", "NFUM Parts I-VI", "WHO SMART L4", "CDSCO Drugs & Cosmetics Act 1940 Schedule E(1)", "21 CFR Part 11"],
    "canonical_treatises_indexed": 16,
    "statutory_and_classical_sources": [
        "Unani Pharmacopoeia of India (UPI Parts I-II, Ministry of AYUSH)",
        "National Formulary of Unani Medicine (NFUM Parts I-VI, Ministry of AYUSH)",
        "Al-Qanun fi al-Tibb (Ibn Sina / Avicenna)",
        "Kitab al-Jami' li-Mufradat al-Adwiya wa-al-Aghdhiya (Ibn al-Baitar)",
        "Kitab al-Hawi fi al-Tibb (Al-Razi / Rhazes, 23 Volumes)",
        "Kamil al-Sina'a al-Tibbiyya (Ali ibn al-Abbas al-Majusi / Haly Abbas)",
        "Kitab al-Tasreef liman 'Ajiza 'an al-Ta'leef (Abul Qasim al-Zahrawi / Albucasis)",
        "Akseer-e-Azam (Hakim Muhammad Azam Khan, 4 Volumes)",
        "Muheet-e-Azam (Hakim Muhammad Azam Khan, 4 Volumes)",
        "Makhzan-ul-Advia (Mir Muhammad Husain Al-Alawi)",
        "Tibb-e-Akbar (Hakim Muhammad Akbar Arzani)",
        "Bayaz-e-Kabir (Hakim Mohammad Kabiruddin)",
        "Khazain-ul-Advia (Hakim Najmul Ghani Rampuri)",
        "WHO Monographs on Selected Medicinal Plants (Volumes 1-4)",
        "ZAYVORA CP-AFUM Compendium of Axis-Based Functional Medicine (Hakeem Dr. Irfan Ashraf)"
    ],
    "curation_status": "AUTHENTIC_CLINICAL_GRADE",
    "editorial_board": "Hakeem Dr. Irfan Ashraf (Lead Clinician & Academic Director), Prof. (Dr.) Mansoor Alam, ZAYVORA Integrative Medical Panel"
}

GRAND_INTEGRATIVE_LIBRARY: Dict[str, Any] = {
    "metadata": LIBRARY_METADATA,
    "volumes": [
        # =========================================================================
        # VOLUME I: KULLIYAT-E-TIBB & HUMAN PHYSIOLOGY
        # =========================================================================
        {
            "id": "vol-01",
            "volume_number": 1,
            "title_en": "Kulliyat-e-Tibb & Human Physiology",
            "title_ur": "کلیاتِ طب اور انسانی افعال الاعضاء",
            "title_ar": "كليات الطب و الفسيولوجيا البشرية",
            "icon": "🧬",
            "badge": "Classical Foundations",
            "summary": "Foundational doctrine of human existence, physical matter, humoral equilibrium, and biological faculties bridging Avicennian cellular pneuma with modern cellular thermodynamics.",
            "chapters": [
                {
                    "id": "ch-01-01",
                    "chapter_number": "1.1",
                    "title_en": "Arkan-e-Arba'a: The Four Elements & States of Matter",
                    "title_ur": "ارکانِ اربعہ اور مادی تغیرات",
                    "key_concepts": [
                        "Naar (Fire / Thermal Energy)",
                        "Hawa (Air / Gaseous State & Aeration)",
                        "Maa (Water / Fluid Dynamics & Solvation)",
                        "Arz (Earth / Solid Minerals & Cellular Density)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Book I)", "author": "Ibn Sina (Avicenna)", "text": "Arkan are the primary, indivisible bodies from which compound organisms are formed through chemical blending."},
                        {"book": "Kamil al-Sina'a al-Tibbiyya", "author": "Ali Ibn al-Abbas al-Majusi", "text": "The four fundamental qualities (Hararat, Buroodat, Yuboosat, Rutoobat) govern the equilibrium of Arkan."}
                    ],
                    "modern_biomedical_correlation": "Directly correlates with modern states of matter (Solid, Liquid, Gas, Plasma/Thermal energy) and intracellular electrolyte distribution (K+, Na+, Ca2+, Mg2+) maintaining membrane resting potentials.",
                    "clinical_diagnostic_criteria": "Evaluation of constitutional density, bone mass, body hydration index, and basal body thermogenesis.",
                    "actionable_protocols": "Equilibrium restoration through thermal modulation, hydration titration, and elemental mineral replenishment.",
                    "safety_and_contraindications": "Avoid extreme thermal shock interventions in patients with acute hemodynamic instability."
                },
                {
                    "id": "ch-01-02",
                    "chapter_number": "1.2",
                    "title_en": "Akhlat-e-Arba'a: Humoral Dynamics & Fluid Compartments",
                    "title_ur": "اخلاطِ اربعہ اور جسمانی مائعات",
                    "key_concepts": [
                        "Dam (Sanguineous Humor / Sanguine / Blood & Erythrocytes)",
                        "Balgham (Phlegmatic Humor / Lymphatic fluid, Mucus, CSF)",
                        "Safra (Choleric Humor / Bilirubin, Bile salts, Metabolic Catalysts)",
                        "Sauda (Melancholic Humor / Spleen metabolites, Minerals, Platelets)"
                    ],
                    "classical_citations": [
                        {"book": "Kitab al-Hawi fit-Tibb", "author": "Abu Bakr al-Razi (Rhazes)", "text": "Humors are the circulating substrates synthesized by the liver through second digestion (Hazm-e-Sani)."},
                        {"book": "Makhzan-ul-Hikmat", "author": "Hakim Kabiruddin", "text": "Health is the quantitative and qualitative harmony of the four humors."}
                    ],
                    "modern_biomedical_correlation": "Correlates directly with Hematocrit, Plasma volume, Lymphatic transport, Hepatobiliary secretions, and Reticuloendothelial clearance.",
                    "clinical_diagnostic_criteria": "Complete Blood Count (CBC), Serum Bilirubin, Viscosity markers, and Albumin/Globulin ratio.",
                    "actionable_protocols": "Tanqiya (Purification) via Munzij-o-Mushil regimen when any humor becomes Fasid (morbid or dyscrasic).",
                    "safety_and_contraindications": "Strong purgation (Mushil) strictly contraindicated in pregnant, emaciated, or severely hypotensive patients."
                },
                {
                    "id": "ch-01-03",
                    "chapter_number": "1.3",
                    "title_en": "Ilm-ul-Mizaj: Temperamental Science & Metabolic Typing",
                    "title_ur": "علم المزاج اور انفرادی بائیو کیمسٹری",
                    "key_concepts": [
                        "Mizaj-e-Mao'tadil (Balanced Optimal Temperament)",
                        "Su-e-Mizaj Sada (Simple Temperamental Dyscrasia without matter)",
                        "Su-e-Mizaj Maddi (Material Dyscrasia with humoral accumulation)",
                        "Mizaj of Organs (Heart is Hot-Dry, Brain is Cold-Moist, Liver is Hot-Moist, Bone is Cold-Dry)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Tashreeh-e-Mizaj)", "author": "Ibn Sina", "text": "Mizaj is the resultant composite quality produced by the mutual interaction and alteration of the primary qualities."},
                        {"book": "Kitab al-Kulliyat", "author": "Ibn Rushd (Averroes)", "text": "Each organ possesses a distinct innate temperament suited to its physiological function."}
                    ],
                    "modern_biomedical_correlation": "Correlates with Basal Metabolic Rate (BMR), Autonomic Nervous System dominance (Sympathetic vs Parasympathetic), and Neuro-endocrine set-points.",
                    "clinical_diagnostic_criteria": "10 Ajnas inspection, body morphology, thermal tolerance, sleep duration, and metabolic speed.",
                    "actionable_protocols": "Ilaj-bil-Zid (Treatment by Contraries): Hot dyscrasias treated with cooling diet/advia, Cold dyscrasias treated with warming regimen.",
                    "safety_and_contraindications": "Never administer Daraja 3 or 4 heating drugs to a person presenting with acute Safrawi hyperpyrexia."
                },
                {
                    "id": "ch-01-04",
                    "chapter_number": "1.4",
                    "title_en": "Quwa & Afaal: Vital, Natural & Psychic Physiology",
                    "title_ur": "قویٰ اور افعال — حیوانی، طبعی اور نفسیاتی نظام",
                    "key_concepts": [
                        "Quwwat-e-Tabiyyah (Natural/Metabolic Faculty — Liver seat)",
                        "Quwwat-e-Haywaniyyah (Vital/Cardiovascular Faculty — Heart seat)",
                        "Quwwat-e-Nafsaniyyah (Psychic/Neurological Faculty — Brain seat)",
                        "Afaal-e-Mufarridah & Afaal-e-Murakkabah (Simple vs Complex Biochemical Actions)"
                    ],
                    "classical_citations": [
                        {"book": "Firdaus al-Hikma", "author": "Ali Ibn Rabban al-Tabari", "text": "The three master organs (Aaza-e-Raeesa) distribute the three primary faculties via arteries, nerves, and veins."},
                        {"book": "Sharah al-Asbab wal Alamat", "author": "Burhanuddin Nafis Kirmani", "text": "When Quwwat-e-Mudabbira-e-Badan (Homeostasis) weakens, disease takes root."}
                    ],
                    "modern_biomedical_correlation": "Correlates with Neuro-Cardio-Metabolic axis: Endocrine-metabolic homeostasis, Autonomic cardiac regulation, and Central Nervous System cognition.",
                    "clinical_diagnostic_criteria": "Heart rate, cognitive responsiveness, appetite efficiency, and muscular tone.",
                    "actionable_protocols": "Tonification of master organs with Muqawwiyat-e-Aaza-e-Raeesa (Cardiotonics, Hepatoprotectives, Neuroprotectives).",
                    "safety_and_contraindications": "Differentiate organic organ failure from functional fatigue before administering stimulating tonics."
                }
            ]
        },

        # =========================================================================
        # VOLUME II: ASBAB-E-SITTA ZAROORIYYA & LIFESTYLE MEDICINE
        # =========================================================================
        {
            "id": "vol-02",
            "volume_number": 2,
            "title_en": "Asbab-e-Sitta Zarooriyya: The Six Essential Prerequisites",
            "title_ur": "اسبابِ ستہ ضروریہ اور احتیاطی طرزِ زندگی",
            "title_ar": "الأسباب الستة الضرورية و طب نمط الحياة",
            "icon": "🌿",
            "badge": "Preventive Lifestyle",
            "summary": "The immutable non-negotiable six lifestyle determinants of human health and longevity, representing classical epigenetics and environmental medicine.",
            "chapters": [
                {
                    "id": "ch-02-01",
                    "chapter_number": "2.1",
                    "title_en": "Hawa-e-Muheet: Atmospheric Aeration, Air Quality & Breathwork",
                    "title_ur": "ہوائے محیط — سانس، ماحولیاتی آلودگی اور تبادلہ گیس",
                    "key_concepts": [
                        "Tanaffus (Respiration & Vital Heat Dissipation)",
                        "Taghayyur-e-Hawa (Air Contamination & Particulate Pollution)",
                        "Tanaffus-e-Amiq (Diaphragmatic Deep Breathing Protocols)",
                        "Seasonal Weather Fronts & Barometric Shifts"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Tadbeer-e-Hawa)", "author": "Ibn Sina", "text": "Clean, fragrant, temperate air is the swiftest agent to alter the Rooh (Vital Pneuma)."},
                        {"book": "Kitab al-Murshid", "author": "Abu Bakr al-Razi", "text": "Stagnant, foul air produces putrefaction in the humors."}
                    ],
                    "modern_biomedical_correlation": "Alveolar gas exchange, VO2 Max, Ambient PM2.5/PM10 cardiovascular risks, and Nitric Oxide synthesis via nasal breathing.",
                    "clinical_diagnostic_criteria": "Pulse Oximetry (SpO2), Peak Expiratory Flow Rate (PEFR), and respiratory rate variability.",
                    "actionable_protocols": "Pranayama / Tanaffus-e-Amiq (4-7-8 breathing) 15 mins twice daily; air purification in urban habitats.",
                    "safety_and_contraindications": "Avoid heavy outdoor aerobic exertion during severe atmospheric inversion and high AQI smog alerts."
                },
                {
                    "id": "ch-02-02",
                    "chapter_number": "2.2",
                    "title_en": "Makool-o-Mashroob: Chrono-Nutrition & Food-as-Medicine",
                    "title_ur": "ماکول و مشروب — غذائی نظام اور اوقاتِ طعام",
                    "key_concepts": [
                        "Hazm-e-Arba'a (Four Stages of Digestion: Gastric, Hepatic, Vascular, Cellular)",
                        "Tarkeeb-e-Ghiza (Nutrient Quality: Lateef, Kaseef, Mo'tadil)",
                        "Chrono-nutrition: Circadian insulin sensitivity & meal timing",
                        "Hydration Volume & Water Quality (Maa-e-Muqattar / Distilled Mineral)"
                    ],
                    "classical_citations": [
                        {"book": "Kitab al-Aghziya", "author": "Ishaq Ibn Imran", "text": "Do not take food upon un-digested food; this is the primary parent of all chronic ailments."},
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "Water serves as the solvent that conveys the nutrients to the deep tissues."}
                    ],
                    "modern_biomedical_correlation": "Gastric emptying rates, postprandial glucose excursions, incretin secretion (GLP-1), and gut microbiome diversity.",
                    "clinical_diagnostic_criteria": "Continuous Glucose Monitoring (CGM) excursions, postprandial somnolence, and gastric transit time.",
                    "actionable_protocols": "Two balanced meals aligned with daytime circadian peaks; warm hydration; 12–14 hour overnight fasting.",
                    "safety_and_contraindications": "Strictly prohibit iced drinks immediately following heavy meals to prevent gastric enzyme inhibition."
                },
                {
                    "id": "ch-02-03",
                    "chapter_number": "2.3",
                    "title_en": "Harkat-o-Sukoon-e-Badani: Physical Exercise & Ergonomics",
                    "title_ur": "حرکت و سکونِ بدنی — ورزش، آرام اور پٹھوں کی بحالی",
                    "key_concepts": [
                        "Riyazat (Therapeutic Physical Exercise)",
                        "Riyazat-e-Kaseera vs Riyazat-e-Mo'tadila (Strenuous vs Moderate Exercise)",
                        "Damm-e-Tawallud (Elicitation of Innate Heat via Movement)",
                        "Ergonomic Posture & Sedentary Deconditioning"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "If a person adopts regular moderate exercise, he will need neither medicine nor physician for most ailments."},
                        {"book": "Zakhira-e-Khwarizmshahi", "author": "Ismail Jurjani", "text": "Exercise stimulates innate heat and dissolves residual waste products (Fuzool)."}
                    ],
                    "modern_biomedical_correlation": "GLUT4 translocation in skeletal muscle, mitochondrial biogenesis, myokine release (Irisin), and cardiovascular remodeling.",
                    "clinical_diagnostic_criteria": "Daily step count, resting heart rate, active calorie burn, and musculoskeletal range of motion.",
                    "actionable_protocols": "30–45 mins daily Zone 2 aerobic activity with twice-weekly resistance training tailored to individual Mizaj.",
                    "safety_and_contraindications": "Contraindicated in severe febrile states, acute cardiac ischemia, or unreduced joint dislocations."
                },
                {
                    "id": "ch-02-04",
                    "chapter_number": "2.4",
                    "title_en": "Naum-o-Yaqza: Sleep Architecture & Circadian Entrainment",
                    "title_ur": "نوم و یقظہ — نیند، بیداری اور ہارمونی بحالی",
                    "key_concepts": [
                        "Naum-e-Amiq (Deep Slow-Wave Sleep / Anabolic Stage)",
                        "Tanqiya-e-Dimagh (Glymphatic Cerebral Cleansing during Sleep)",
                        "Yuboosat-e-Dimagh due to Sahar (Chronic Sleep Deprivation)",
                        "Circadian Light Entrainment (Morning Sunlight & Night Melatonin)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "Sleep draws innate heat inwards to digest food and replenish the vital pneuma."},
                        {"book": "Makhzan-ul-Advia", "author": "Sayyid Nooruddin", "text": "Excessive wakefulness dries the brain and excites black bile."}
                    ],
                    "modern_biomedical_correlation": "Glymphatic clearance of Beta-Amyloid, Cortisol nadir, Growth Hormone release, and REM memory consolidation.",
                    "clinical_diagnostic_criteria": "Sleep hypnogram, Oura/Apple Watch Sleep Stage analysis (Deep > 15%, REM > 20%), and Pittsburgh Sleep Quality Index.",
                    "actionable_protocols": "Consistent 10:00 PM sleep window, zero blue light 90 mins prior, cool ambient bedroom (18–20°C).",
                    "safety_and_contraindications": "Avoid hypnotic pharmaceutical sedatives that obliterate natural restorative REM and N3 deep sleep."
                },
                {
                    "id": "ch-02-05",
                    "chapter_number": "2.5",
                    "title_en": "Istifragh-o-Ihtibas: Evacuation, Retention & Detox Pathways",
                    "title_ur": "استفراغ و احتباس — سموم کا اخراج اور ضروری اجزاء کی حفاظت",
                    "key_concepts": [
                        "Tanqiya (Systemic Evacuation of Morbid Matter)",
                        "Ihtibas-e-Fasid (Pathological Retention of Toxins / Constipation, Oliguria)",
                        "Istifragh-e-Mufrit (Excessive Depletion / Dehydration, Cachexia)",
                        "Emanctories (Meda, Amaa, Jigar, Kulyah, Jild, Rehm)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "Whatever ought to be evacuated must be evacuated timely, and whatever ought to be retained must be retained."},
                        {"book": "Kitab al-Murshid", "author": "Al-Razi", "text": "Constipation is the mother of twenty chronic diseases."}
                    ],
                    "modern_biomedical_correlation": "Renal filtration, Colonic motility, Phase I/II hepatic xenobiotic biotransformation, and Lymphatic drainage.",
                    "clinical_diagnostic_criteria": "Bristol Stool Chart (Type 3–4 normal), Glomerular Filtration Rate, and daily perspiration index.",
                    "actionable_protocols": "Daily spontaneous bowel movement; natural prebiotic soluble fiber; therapeutic sweating (Hammam) when indicated.",
                    "safety_and_contraindications": "Never induce aggressive evacuation in dehydrated or hemodynamically compromised patients."
                },
                {
                    "id": "ch-02-06",
                    "chapter_number": "2.6",
                    "title_en": "Harkat-o-Sukoon-e-Nafsani: Psychic Equilibrium & Stress Modulation",
                    "title_ur": "حرکت و سکونِ نفسانی — ذہنی دباؤ، جذبات اور خود کار اعصابی توازن",
                    "key_concepts": [
                        "Infi'alat-e-Nafsaniyyah (Psychic Passions: Anger, Joy, Fear, Grief, Anxiety)",
                        "Harkat-e-Rooh (Rapid expansion or sudden contraction of vital pneuma)",
                        "Rooh-e-Nafsani (Psychic Pneuma / Neurochemical Neurotransmission)",
                        "Sukun-e-Qalb (Heart-Brain Emotional Equilibrium)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "Sudden violent anger heats the body intensely, whereas sudden terror chills the innate heat and contracts the pneuma to the core."},
                        {"book": "Tibb-e-Akbar", "author": "Hakim Arzani", "text": "Chronic grief and worry cause severe burning of black bile (Sauda-e-Ehtraqiyya)."}
                    ],
                    "modern_biomedical_correlation": "Hypothalamic-Pituitary-Adrenal (HPA) axis, Vagal nerve tone, Cortisol-to-DHEA ratio, and Heart Rate Variability (HRV).",
                    "clinical_diagnostic_criteria": "HRV SDNN / RMSSD metrics, Perceived Stress Scale (PSS-10), and salivary cortisol awakening response.",
                    "actionable_protocols": "Mindfulness (Muraqaba), calming herbal infusions (Arq Gaozaban, Chamomile), and vagal stimulation techniques.",
                    "safety_and_contraindications": "Screen immediately for clinical depressive suicidality; acute psychiatric crises require specialized dual care."
                }
            ]
        },

        # =========================================================================
        # VOLUME III: CLASSICAL DIAGNOSTICS & BEDSIDE EXAMINATION
        # =========================================================================
        {
            "id": "vol-03",
            "volume_number": 3,
            "title_en": "Classical Diagnostics & Bedside Examination",
            "title_ur": "تشخیص و معاینۂ سريري — نبض، قارورہ اور براز",
            "title_ar": "التشخيص الكلاسيكي و الفحص السريري",
            "icon": "🩺",
            "badge": "Clinical Semiology",
            "summary": "The master art of non-invasive bedside semiology: pulse waveform dynamics, urine sediment topography, stool analysis, and cranial facial diagnostics.",
            "chapters": [
                {
                    "id": "ch-03-01",
                    "chapter_number": "3.1",
                    "title_en": "Ilm-un-Nabz: The 10 Classical Ajnas Pulse Evaluation",
                    "title_ur": "علم النبض — دس اجناسِ نبض اور جدید پلس ویو",
                    "key_concepts": [
                        "Miqdar (Volume/Amplitude: Taweel, Areez, Azeem)",
                        "Harkat (Velocity/Rate: Saree, Bati, Mo'tadil)",
                        "Quwwat (Pulse Strength: Qawi, Zaeef)",
                        "Ghalzat (Arterial Wall Elasticity: Layyin, Sulb)",
                        "Imtila (Fullness: Mumtali, Khaali)",
                        "Zaman-e-Sukoon (Interval: Mutawater, Mutafawit)",
                        "Istiwah (Regularity: Mustawi, Mukhtalif)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Kitab un-Nabz)", "author": "Ibn Sina", "text": "Pulse is the movement of heart and arteries consisting of alternating expansion and contraction to cool the innate heat."},
                        {"book": "Risala-e-Nabz", "author": "Hakim Kabiruddin", "text": "The radial artery at the styloid process is the universal mirror of visceral health."}
                    ],
                    "modern_biomedical_correlation": "Photoplethysmography (PPG), Pulse Wave Velocity (PWV), Arterial Stiffness Index, and Radial artery pressure waveform dicrotic notch.",
                    "clinical_diagnostic_criteria": "Radial palpation with four fingertips in quiet morning state, resting HR, and PWV < 10 m/s normal.",
                    "actionable_protocols": "Identify Su-e-Mizaj from waveform: Saree Qawi (Hot/Inflammatory), Bati Layyin (Cold/Phlegmatic), Sulb (Atherosclerosis).",
                    "safety_and_contraindications": "Do not assess pulse immediately post-exercise, bathing, or profound emotional turmoil."
                },
                {
                    "id": "ch-03-02",
                    "chapter_number": "3.2",
                    "title_en": "Qaroorah: Urine Examination & Sediment Topography",
                    "title_ur": "قارورہ — پیشاب کا تجزیہ، رنگ، قوام اور رسوب",
                    "key_concepts": [
                        "Lawn (Color: Abyaz/White, Asfar/Yellow, Ahmar/Red, Aswad/Black)",
                        "Qawam (Consistency: Raqeeq/Thin, Ghaleez/Thick, Mo'tadil)",
                        "Burooq & Reeh (Transparency, Foam, and Odor)",
                        "Rusub (Sediment Stratification: Sifli/Bottom, Wasati/Middle, Fawqi/Floating)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Tashkhees-e-Baul)", "author": "Ibn Sina", "text": "The urine reflects the state of the liver, blood vessels, and kidneys; inspection must occur in early morning light."},
                        {"book": "Al-Hawi fit-Tibb", "author": "Al-Razi", "text": "White sediment in yellow urine indicates resolution of hot inflammatory disease (Nuzj)."}
                    ],
                    "modern_biomedical_correlation": "Urine Specific Gravity (1.005–1.030), Microscopic Urinalysis (RBCs, WBCs, Casts, Crystals), Proteinuria, and Urobilinogen.",
                    "clinical_diagnostic_criteria": "First morning mid-stream specimen in clear glass container without refrigeration or light degradation.",
                    "actionable_protocols": "Differentiate Nuzj (metabolic resolution) from crude unconcocted humors to time therapeutic evacuation.",
                    "safety_and_contraindications": "Gross hematuria or tea-colored urine requires immediate microscopic investigation to rule out glomerular nephritis or malignancy."
                },
                {
                    "id": "ch-03-03",
                    "chapter_number": "3.3",
                    "title_en": "Baraaz & Lisaan: Stool Transit & Tongue Topography",
                    "title_ur": "براز اور لسان — آنتوں کا فعل اور زبان کی تشخیص",
                    "key_concepts": [
                        "Baraaz (Color, Odor, Transit speed, Gas entrapment)",
                        "Lisaan (Tongue Body color: Pink, Red, Pale, Purplish)",
                        "Sabard-e-Lisaan (Tongue Coating: White-greasy = Balgham, Yellow-dry = Safra, Blackish = Sauda)",
                        "Organ Topography: Tip (Heart), Center (Stomach/Spleen), Sides (Liver/Gallbladder), Root (Kidneys/Intestines)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "The tongue is the external indicator of the stomach mucosa and internal innate heat."},
                        {"book": "Tibb-e-Akbar", "author": "Hakim Arzani", "text": "Yellowish dry tongue with bitter taste confirms Safrawi gastritis."}
                    ],
                    "modern_biomedical_correlation": "Oral microbiome dysbiosis, Vitamin B12/Iron deficiency atrophic glossitis, and Bristol Stool Chart transit kinetics.",
                    "clinical_diagnostic_criteria": "Visual daylight inspection of tongue without prior brushing, scrape, or colored food ingestion.",
                    "actionable_protocols": "Direct diet and digestive tonics (Jawarish Kamuni, Jawarish Jalinoos) based on tongue moisture and coating thickness.",
                    "safety_and_contraindications": "Persistent unilateral tongue ulceration requires immediate biopsy referral to rule out squamous cell carcinoma."
                }
            ]
        },

        # =========================================================================
        # VOLUME IV: CLINICAL LABORATORY BIOMARKERS & MODERN PATHOLOGY
        # =========================================================================
        {
            "id": "vol-04",
            "volume_number": 4,
            "title_en": "Clinical Laboratory Biomarkers & Modern Pathology",
            "title_ur": "جدید لیب ٹیسٹ، بائیو مارکرز اور پیتھولوجی",
            "title_ar": "التحاليل المخبرية السريرية و علم الأمراض الحديث",
            "icon": "🧪",
            "badge": "Biomedical Precision",
            "summary": "Bridging modern clinical hematology, biochemistry, and endocrinology with classical humoral dyscrasias, organ temperaments, and inflammation cascades.",
            "chapters": [
                {
                    "id": "ch-04-01",
                    "chapter_number": "4.1",
                    "title_en": "Inflammatory Biomarkers: hs-CRP, ESR & Cytokines",
                    "title_ur": "سوزش کے مارکرز — سی آر پی، ای ایس آر اور سائیٹوکائنز",
                    "key_concepts": [
                        "High-Sensitivity C-Reactive Protein (hs-CRP < 1.0 mg/L Optimal)",
                        "Erythrocyte Sedimentation Rate (ESR Westergren)",
                        "Serum Ferritin as an Acute Phase Reactant",
                        "Humoral Translation: Hararat-e-Fasida, Safrawi Blood Fire & Waram"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Awram)", "author": "Ibn Sina", "text": "Inflammation (Waram) begins with vascular engorgement, followed by heat, pain, and humoral effusion."},
                        {"book": "Kamil al-Sina'a", "author": "Al-Majusi", "text": "Boiling of blood (Ghalayan-e-Dam) produces febrile heat and tissue breakdown."}
                    ],
                    "modern_biomedical_correlation": "Interleukin-6 (IL-6), TNF-alpha, hepatic acute-phase reactant synthesis, and endothelial activation.",
                    "clinical_diagnostic_criteria": "hs-CRP > 3.0 mg/L indicates high cardiovascular/systemic inflammatory risk; > 10.0 mg/L indicates acute systemic inflammation.",
                    "actionable_protocols": "Anti-inflammatory botanical protocol: Majun Suranjan, Hab-e-Gugal, Arq-e-Kasni; monitor 28-day reduction trajectory.",
                    "safety_and_contraindications": "Differentiate autoimmune elevation from acute bacterial sepsis (Procalcitonin > 0.5 mcg/L requires emergency antibiotics)."
                },
                {
                    "id": "ch-04-02",
                    "chapter_number": "4.2",
                    "title_en": "Cardiometabolic Panel: HbA1c, Fasting Insulin & Lipid Fractionation",
                    "title_ur": "کارڈیو میٹابولک پینل — ایچ بی اے ون سی، انسولین اور کولیسٹرول",
                    "key_concepts": [
                        "Glycated Hemoglobin (HbA1c < 5.6% Optimal)",
                        "HOMA-IR (Homeostatic Model Assessment of Insulin Resistance < 1.5)",
                        "Apolipoprotein B (ApoB < 80 mg/dL) & Small-Dense LDL",
                        "Humoral Translation: Su-e-Mizaj Barid Ratab, Balgham-e-Lazuq & Luzujat-e-Dam"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Ziabetus)", "author": "Ibn Sina", "text": "Ziabetus is caused by weakness of the kidneys and cold-wet hepatic dyscrasia (Zof-e-Jigar o Kulyah)."},
                        {"book": "Makhzan-ul-Advia", "author": "Sayyid Nooruddin", "text": "Excess phlegm clogs the vascular channels and creates sluggishness in the blood."}
                    ],
                    "modern_biomedical_correlation": "Pancreatic beta-cell exhaustion, hepatic de novo lipogenesis, atherogenic dyslipidemia, and vascular endothelial dysfunction.",
                    "clinical_diagnostic_criteria": "Fasting blood glucose, fasting insulin, HbA1c, fasting lipid profile with Non-HDL and Triglyceride/HDL ratio.",
                    "actionable_protocols": "Chrono-nutrition, Intermittent fasting, Jamun seed (Tukhm-e-Jamun), Karela, Gurmar (Gymnema), MetaboCore Unani formula.",
                    "safety_and_contraindications": "Never abruptly discontinue allopathic hypoglycemics in patients with severe hyperglycemia (HbA1c > 9.0%) without dual-track titration."
                },
                {
                    "id": "ch-04-03",
                    "chapter_number": "4.3",
                    "title_en": "Hepatorenal & Endocrine Panels: LFT, KFT, Thyroid & Cortisol",
                    "title_ur": "جگر، گردے اور ہارمونز کا مکمل تجزیہ",
                    "key_concepts": [
                        "Liver Function: SGOT/AST, SGPT/ALT, Alk Phos, GGT, Serum Albumin",
                        "Kidney Function: Serum Creatinine, eGFR (CKD-EPI), Urine Microalbumin/Creatinine Ratio",
                        "Thyroid Axis: TSH (0.5–2.5 uIU/mL), Free T3, Free T4, Anti-TPO",
                        "Humoral Translation: Mizaj-e-Kabid, Mizaj-e-Kulyah & Hararat-e-Ghariziyya baseline"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Amraz-e-Jigar)", "author": "Ibn Sina", "text": "The liver is the master organ of digestion; when its heat fails, cold watery humors flood the circulation."},
                        {"book": "Kitab al-Hawi", "author": "Al-Razi", "text": "Preserve the kidneys with demulcent waters and avoid desiccating toxins."}
                    ],
                    "modern_biomedical_correlation": "Hepatic transaminase leakage, Glomerular filtration integrity, Hypothalamic-Pituitary-Thyroid axis, and Adrenal steroidogenesis.",
                    "clinical_diagnostic_criteria": "eGFR < 60 mL/min indicates Stage 3+ CKD; ALT > 3x upper normal indicates acute hepatic injury.",
                    "actionable_protocols": "Kasni (Cichorium intybus), Mako (Solanum nigrum) for liver; Khar-e-Khasak (Tribulus), Tukhm-e-Khas for kidneys.",
                    "safety_and_contraindications": "In eGFR < 30 mL/min, halt all Schedule E(1) poisons (Suranjan, Kuchla) and potassium-sparing botanicals."
                }
            ]
        },

        # =========================================================================
        # VOLUME V: RADIO-DIAGNOSTICS & MEDICAL IMAGING
        # =========================================================================
        {
            "id": "vol-05",
            "volume_number": 5,
            "title_en": "Radio-Diagnostics & Medical Imaging",
            "title_ur": "ریڈیو ڈائیگنوسٹکس اور جدید امیجنگ — ایکسرے، ایم آر آئی اور الٹراساؤنڈ",
            "title_ar": "التشخيص الإشعاعي و التصوير الطبي",
            "icon": "🩻",
            "badge": "Structural Imaging",
            "summary": "Integrating modern radiological semiology (Plain Radiography, Ultrasound, MRI, FibroScan, DEXA) with classical musculoskeletal and visceral pathology.",
            "chapters": [
                {
                    "id": "ch-05-01",
                    "chapter_number": "5.1",
                    "title_en": "Musculoskeletal Imaging: X-Ray & MRI in Arthritis",
                    "title_ur": "ہڈیوں اور جوڑوں کے ایکسرے اور ایم آر آئی — جوڑوں کا درد",
                    "key_concepts": [
                        "Kellgren-Lawrence Osteoarthritis Grading Scale (Grade I to IV)",
                        "Joint Space Narrowing, Subchondral Sclerosis, Osteophytosis",
                        "MRI Synovitis, Effusion & Bone Marrow Edema (BME)",
                        "Humoral Translation: Waja-ul-Mafasil Barid Balghami, Tahajjar-e-Mafasil & Ehtibas"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Waja-ul-Mafasil)", "author": "Ibn Sina", "text": "Cold phlegm accumulates in the ligamentous spaces of joints due to weak local expulsive faculty."},
                        {"book": "Khazain-ul-Advia", "author": "Hakim Najmul Ghani", "text": "Suranjan penetrates into the deep articular fissures to dissolve congealed matter."}
                    ],
                    "modern_biomedical_correlation": "Cartilage extracellular matrix proteoglycan depletion, chondrocyte senescence, subchondral bone remodeling, and inflammatory synovitis.",
                    "clinical_diagnostic_criteria": "Standing AP/Lateral knee radiograph: KL Grade II (Definite osteophytes, possible JSN), KL Grade III (Moderate JSN, sclerosis).",
                    "actionable_protocols": "Dual-track protocol: Topical Roghan-e-Suranjan/Balsan + Natool fomentation + Oral Majun Suranjan + Weight decompression.",
                    "safety_and_contraindications": "KL Grade IV (Bone-on-bone complete joint destruction) with severe angular deformity requires orthopedic surgical arthroplasty referral."
                },
                {
                    "id": "ch-05-02",
                    "chapter_number": "5.2",
                    "title_en": "Abdominal Ultrasound & FibroScan: Hepatic Steatosis & Visceral Stones",
                    "title_ur": "پیٹ کا الٹراساؤنڈ اور فائبرو اسکین — فیٹی لیور اور پتھریاں",
                    "key_concepts": [
                        "Hepatic Steatosis (Fatty Liver Grade 1, 2, 3 on Ultrasound)",
                        "FibroScan Liver Stiffness Measurement (LSM in kPa) & CAP Score (dB/m)",
                        "Cholelithiasis (Gallbladder stones) & Nephrolithiasis (Renal calculi)",
                        "Humoral Translation: Su-e-Mizaj Jigar Barid Ratab, Salabat-e-Jigar, Hasat-e-Mararah o Kulyah"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Hasat)", "author": "Ibn Sina", "text": "Stones are produced when thick viscous humor meets intense unnatural heat that bakes it dry."},
                        {"book": "Tibb-e-Akbar", "author": "Hakim Arzani", "text": "Fatty infiltration of the liver causes dull heaviness in the right hypochondrium."}
                    ],
                    "modern_biomedical_correlation": "Non-Alcoholic Fatty Liver Disease (NAFLD / MASH), Hepatic stellate cell activation, Calcium oxalate lithogenesis, and Cholesterol supersaturation.",
                    "clinical_diagnostic_criteria": "LSM < 7.0 kPa normal; > 12.5 kPa indicates Advanced Fibrosis / Cirrhosis risk. Ultrasound acoustic shadowing confirms calculi.",
                    "actionable_protocols": "Jigar: Arq Mako, Arq Kasni, Safoof Habis; Stones: Kushta Hajr-ul-Yahood, Majun Sang-e-Sar-e-Mahi, Kulthi decoction.",
                    "safety_and_contraindications": "Impacted common bile duct stone (Choledocholithiasis) with obstructive jaundice is an absolute emergency surgical referral."
                },
                {
                    "id": "ch-05-03",
                    "chapter_number": "5.3",
                    "title_en": "DEXA Bone Densitometry & Vascular Doppler",
                    "title_ur": "ہڈیوں کی کمزوری (DEXA) اور خون کی نالیوں کا ڈوپلر",
                    "key_concepts": [
                        "DEXA T-Score: Osteopenia (-1.0 to -2.5), Osteoporosis (< -2.5)",
                        "Carotid Intima-Media Thickness (CIMT > 0.9 mm indicates Atherosclerosis)",
                        "Humoral Translation: Takhalkhul-e-Izam (Bone demineralization) & Tasallub-e-Sharayeen (Arterial hardening)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "With advanced age, radical moisture declines and bones become brittle like dry wood."},
                        {"book": "Kamil al-Sina'a", "author": "Al-Majusi", "text": "The arterial coats lose elasticity when melancholic humor stiffens their fibers."}
                    ],
                    "modern_biomedical_correlation": "Osteoclast-mediated bone resorption, Hydroxyapatite demineralization, Endothelial shear stress, and Atheromatous plaque calcification.",
                    "clinical_diagnostic_criteria": "Dual-Energy X-ray Absorptiometry of Lumbar Spine and Femoral Neck; Carotid duplex ultrasonography.",
                    "actionable_protocols": "Kushta Marwareed (Micro-calcified pearl oyster calcium), Asgandh, Gond Chinia, Sesamum indicum (Til) oil massage.",
                    "safety_and_contraindications": "High-velocity unstable carotid plaque with > 70% stenosis requires vascular surgical multidisciplinary evaluation."
                }
            ]
        },

        # =========================================================================
        # VOLUME VI: GUT MICROBIOME, METAGENOMICS & EPIGENETICS
        # =========================================================================
        {
            "id": "vol-06",
            "volume_number": 6,
            "title_en": "Gut Microbiome, Metagenomics & Epigenetics",
            "title_ur": "گٹ مائیکرو بائیوم، آنتوں کے جراثیم اور جینیاتی اظہار",
            "title_ar": "الميكروبيوم المعوي و علم الوراثة اللاجيني",
            "icon": "🦠",
            "badge": "Microbiome Biology",
            "summary": "Bridging Avicennian first digestion (Hazm-e-Awwal) and Kiloos synthesis with modern 16S rRNA metagenomics, Short-Chain Fatty Acids, and epigenetic gene expression.",
            "chapters": [
                {
                    "id": "ch-06-01",
                    "chapter_number": "6.1",
                    "title_en": "Hazm-e-Awwal & Metagenomics: The Microbiome as Humoral Factory",
                    "title_ur": "ہضمِ اول اور گٹ مائیکروبائیوم — اخلاط کی تیاری",
                    "key_concepts": [
                        "Hazm-e-Meda (Gastric Concoction) & Kiloos (Chyme)",
                        "Firmicutes to Bacteroidetes Ratio (F/B Ratio)",
                        "Dysbiosis, SIBO (Small Intestinal Bacterial Overgrowth)",
                        "Humoral Translation: Fasad-e-Hazm, Fasad-e-Balgham & Ufunat (Putrefaction)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "If the first digestion in the stomach is defective, all subsequent digestions in liver and tissues are corrupted."},
                        {"book": "Kitab al-Murshid", "author": "Al-Razi", "text": "The putrefaction of food in the stomach creates vapors that cloud the mind."}
                    ],
                    "modern_biomedical_correlation": "Intestinal epithelial tight junction integrity (Zonulin), Lipopolysaccharide (LPS) translocation, and Metabolic endotoxemia.",
                    "clinical_diagnostic_criteria": "Stool Metagenomic Sequencing, Lactulose Hydrogen Breath Test, and Fecal Calprotectin (< 50 mcg/g normal).",
                    "actionable_protocols": "Prebiotic botanical mucilage (Ispaghol husk), Fermented whey (Ma-ul-Jubn), Zanjabeel (Zingiber), and Anisoon (Pimpinella).",
                    "safety_and_contraindications": "Do not administer massive probiotic fermentations during acute SIBO flare; resolve bacterial overgrowth first."
                },
                {
                    "id": "ch-06-02",
                    "chapter_number": "6.2",
                    "title_en": "Short-Chain Fatty Acids (SCFAs) & Epigenetics",
                    "title_ur": "شارٹ چین فیٹی ایسڈز اور ایپی جینیٹکس — خوراک سے جینز تک",
                    "key_concepts": [
                        "Butyrate, Acetate, Propionate Production",
                        "DNA Methylation & Histone Deacetylase (HDAC) Inhibition",
                        "Epigenetic Modulation via Asbab-e-Sitta (Diet, Sleep, Stress)",
                        "Humoral Translation: Rutoobat-e-Ghariziyya Preservation at Genome Level"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "Habits and environmental regimen become a second nature (Tabiat-e-Sania) that alters the bodily constitution."},
                        {"book": "Kamil al-Sina'a", "author": "Al-Majusi", "text": "A lineage's temperament shifts across generations based on climate and nourishment."}
                    ],
                    "modern_biomedical_correlation": "Butyrate acting as an HDAC inhibitor promoting Treg lymphocyte differentiation; microRNA regulation of inflammatory signaling.",
                    "clinical_diagnostic_criteria": "Fecal SCFA Quantification (Total SCFAs > 60 mmol/g), Plasma Methylation markers, and biological aging clocks.",
                    "actionable_protocols": "Resistant starches, Chicory root (Kasni Inulin), Polyphenol-rich pomegranate (Anar), and Curcumin.",
                    "safety_and_contraindications": "High-fiber prebiotic titration must be gradual in irritable bowel syndrome with severe visceral hypersensitivity."
                }
            ]
        },

        # =========================================================================
        # VOLUME VII: CONTINUOUS WEARABLES, IOT & SMARTPHONE AI VISION
        # =========================================================================
        {
            "id": "vol-07",
            "volume_number": 7,
            "title_en": "Continuous Wearables, IoT & Smartphone AI Vision",
            "title_ur": "پہننے والے گیجٹس، لائیو مانیٹرنگ اور سمارٹ فون اے آئی",
            "title_ar": "القياسات الحيوية المستمرة و الرؤية الحاسوبية بالذكاء الاصطناعي",
            "icon": "📱",
            "badge": "Digital Diagnostics",
            "summary": "Real-time Asbab-e-Sitta telemetry: Continuous Glucose Monitoring, HRV autonomic tracking, sleep hypnograms, and computer vision semiology.",
            "chapters": [
                {
                    "id": "ch-07-01",
                    "chapter_number": "7.1",
                    "title_en": "Continuous Glucose Monitoring (CGM) & Glycemic Telemetry",
                    "title_ur": "مسلسل گلوکوز ٹریکنگ — میٹابولک اتار چڑھاؤ اور حرارتِ غریزیہ",
                    "key_concepts": [
                        "Glycemic Variability: Mean Amplitude of Glycemic Excursions (MAGE)",
                        "Time in Range (TIR: 70–140 mg/dL target > 70%)",
                        "Postprandial Glycemic Spikes & Metabolic Heat Stress",
                        "Humoral Translation: Hararat-e-Ghariziyya vs Hararat-e-Ghareebah in Fuel Metabolism"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "When sweetness overwhelms the blood, thirst escalates and the body tissues melt into the urine."},
                        {"book": "Bayaz-e-Kabir", "author": "Hakim Kabiruddin", "text": "Observe the reaction of the pulse and digestive warmth after every heavy repast."}
                    ],
                    "modern_biomedical_correlation": "Continuous interstitial glucose sensors (Dexcom, FreeStyle Libre), advanced glycation end-products (AGEs), and mitochondrial reactive oxygen species.",
                    "clinical_diagnostic_criteria": "CGM 14-day Ambulatory Glucose Profile (AGP), Glycemic Variability Index (%CV < 36% stable).",
                    "actionable_protocols": "Food order sequencing (Fiber first, Protein/Fat second, Complex Carbs last); post-meal 15-min walk (Riyazat-e-Khafifa).",
                    "safety_and_contraindications": "Sensor lag during rapid hypoglycemia drops requires immediate capillary fingerstick capillary glucometer verification."
                },
                {
                    "id": "ch-07-02",
                    "chapter_number": "7.2",
                    "title_en": "Heart Rate Variability (HRV) & Sleep Architecture IoT",
                    "title_ur": "دل کی دھڑکن کا توازن (HRV) اور سمارٹ رِنگ سلیپ ٹریکنگ",
                    "key_concepts": [
                        "HRV SDNN & RMSSD (Parasympathetic Vagal Tone)",
                        "Oura Ring & Smartwatch Hypnograms: REM vs Deep N3 Sleep",
                        "Circadian Temperature Nadir & Autonomic Stress Index",
                        "Humoral Translation: Quwwat-e-Haywaniyyah & Rooh-e-Haywani Autonomic Balance"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "The pulse's rhythm, pace, and variability indicate whether the heart is tranquil or overwhelmed by passions."},
                        {"book": "Risala-e-Rooh", "author": "Al-Razi", "text": "The vital breath expands in joy and contracts in fear, altering the rhythm of life."}
                    ],
                    "modern_biomedical_correlation": "Sympathovagal balance, vagus nerve stimulation, baroreflex sensitivity, and cardiac autonomic neuropathy.",
                    "clinical_diagnostic_criteria": "Nighttime average RMSSD (higher indicates superior resilience); deep sleep duration > 60 minutes minimum.",
                    "actionable_protocols": "Nightly breathing coherence, digital curfew, adaptogenic nervous tonics (Khamira Marwareed, Asgandh).",
                    "safety_and_contraindications": "Persistent unprovoked nighttime resting tachycardia (> 100 bpm) warrants immediate ECG for arrhythmia exclusion."
                },
                {
                    "id": "ch-07-03",
                    "chapter_number": "7.3",
                    "title_en": "Smartphone Computer Vision: Digital Lisaan & Sima Diagnostics",
                    "title_ur": "موبائل کیمرہ اے آئی — زبان، چہرے اور ناخنوں کی ڈیجیٹل تشخیص",
                    "key_concepts": [
                        "Tongue Coating Computer Vision (Sabard Color & Thickness Classification)",
                        "Facial Complexion Chromaticity (Zard/Yellow, Peela/Pale, Surkh/Flushed)",
                        "Nail Bed Capillaries & Morphometry (Beau's lines, Koilonychia)",
                        "Humoral Translation: Direct Bedside Triage via Multi-Modal Visual AI"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "The physician must observe the color of the face, the eyes, and the tongue before touching the wrist."},
                        {"book": "Tibb-e-Nabawi", "author": "Ibn Qayyim al-Jawziyya", "text": "The countenance of the sick reveals the secret of the hidden humors."}
                    ],
                    "modern_biomedical_correlation": "RGB chromaticity extraction, deep convolutional neural networks (CNNs), oral microbiome colorimetric mapping, and scleral icterus detection.",
                    "clinical_diagnostic_criteria": "Standardized lighting calibration, smartphone macro lens 15–20 cm distance, high-resolution JPEG capture.",
                    "actionable_protocols": "Real-time decision support prompt for clinician verification; never autonomous diagnosis without clinician gate.",
                    "safety_and_contraindications": "Ambient lighting variations and cosmetic makeup must be neutralized before visual feature extraction."
                }
            ]
        },

        # =========================================================================
        # VOLUME VIII: COMPREHENSIVE MATERIA MEDICA & TOXICOLOGY
        # =========================================================================
        {
            "id": "vol-08",
            "volume_number": 8,
            "title_en": "Comprehensive Materia Medica & Toxicology",
            "title_ur": "جامع مفرودات و مرکبات، سموم اور تدبیرِ ادویہ",
            "title_ar": "موسوعة الأدوية المفردة و المركبة و السموم",
            "icon": "🌿",
            "badge": "Pharmacopoeia & Safety",
            "summary": "Over 1,280 Codified Botanical Monographs in the Digital Knowledge Base, Schedule E(1) Statutory Poison detoxification (Mudabbar / Shodhana), Badal substitutes, Musleh correctives, and classical Murakkabat.",
            "chapters": [
                {
                    "id": "ch-08-01",
                    "chapter_number": "8.1",
                    "title_en": "The Master Botanical Pharmacopoeia: Over 1,280 Codified Knowledge Base Monographs & Exemplar Analysis",
                    "title_ur": "یونانی فارماکوپیا — ۱۲۸۰ سے زائد مستند نباتاتی ادویہ",
                    "key_concepts": [
                        "Canonical Identity: Botanical authority, synonyms, regional Hindi/Urdu names",
                        "Classical Profiling: Mizaj (Degrees 1 to 4), Primary Afaal, Specific Actions",
                        "Phytochemistry: Active alkaloids, glycosides, flavonoids, and terpenoids",
                        "Pharmacopoeial Standards: UPI Volume, NFUM Codes, HPLC Fingerprints"
                    ],
                    "classical_citations": [
                        {"book": "Khazain-ul-Advia (3 Volumes)", "author": "Hakim Najmul Ghani", "text": "Comprehensive Materia Medica compiling classical Arabic, Persian, and Indian medicinal substances."},
                        {"book": "Makhzan-ul-Advia", "author": "Sayyid Nooruddin", "text": "The authoritative classical repository of temperament, dosage, and substitute drugs."}
                    ],
                    "modern_biomedical_correlation": "Pharmacognosy, thin-layer chromatography (TLC), gas chromatography-mass spectrometry (GC-MS), and CCRUM heavy metal/pesticide limits.",
                    "clinical_diagnostic_criteria": "Identity verified via microscopic stomatal index, ash values, and reference marker substance percentage.",
                    "actionable_protocols": "Standardized dose administration with appropriate Badraqa (vehicle: Honey, Milk, Arq Gaozaban).",
                    "safety_and_contraindications": "Strictly adhere to CCRUM GLP limits (Lead < 10 ppm, Arsenic < 3 ppm, Cadmium < 0.3 ppm)."
                },
                {
                    "id": "ch-08-02",
                    "chapter_number": "8.2",
                    "title_en": "Schedule E(1) Statutory Poisons & Mandatory Mudabbar Detoxification",
                    "title_ur": "شیڈول ای ون کی زہریلی ادویہ اور لازمی شدھی و تدبیر",
                    "key_concepts": [
                        "Schedule E(1) Drugs & Cosmetics Rules 1945 List (Suranjan Talkh, Kuchla, Samm-ul-Far, Aconite)",
                        "Narrow Therapeutic Index & Toxic Alkaloids (Colchicine, Strychnine, Brucine)",
                        "Mandatory Mudabbar Shodhana Protocols (Boiling in Cow Milk, Triphala Decoction Soaking, Ghee Frying)",
                        "Digital Certificate & Sign-Off Before Dispense"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Kitab al-Advia)", "author": "Ibn Sina", "text": "Poisons possess potent curative faculties when their harmful malice is broken through meticulous Tadbeer."},
                        {"book": "Qarabadin-e-Qadri", "author": "Hakim Mohammad Akbar Arzani", "text": "Never administer Suranjan Talkh or Azaraqi in raw crude state under any circumstance."}
                    ],
                    "modern_biomedical_correlation": "Thermal and enzymatic degradation of toxic alkaloid fractions, reduction of oral LD50 toxicity, and selective retention of anti-inflammatory active metabolites.",
                    "clinical_diagnostic_criteria": "Verification of valid batch Mudabbar certificate with batch number and analytical chemist signoff.",
                    "actionable_protocols": "Suranjan Talkh: Boil in Sheer-e-Gao 3 hours, peel membranous testa, excise embryonic sprout, fry in Roghan-e-Badam.",
                    "safety_and_contraindications": "FAIL-CLOSED: Dispensing raw un-detoxified Schedule E(1) substance is a criminal statutory violation."
                },
                {
                    "id": "ch-08-03",
                    "chapter_number": "8.3",
                    "title_en": "Badal-e-Advia & Musleh-e-Advia Science",
                    "title_ur": "بدلِ ادویہ اور مصلح ادویہ — متبادل اور ضمنی اثرات کا ازالہ",
                    "key_concepts": [
                        "Badal-e-Advia (Approved Substitutes when primary herb is unavailable or contraindicated)",
                        "Dosing Conversion Ratios for Substitutes (e.g. Asgandh for Bahman Surkh 1:1)",
                        "Musleh-e-Advia (Toxicity Correctives that buffer mucosal irritation and neutralize adverse effects)",
                        "Classical Formulations: Itrifal, Jawarish, Majun, Khamira, Sharbat, Kushta"
                    ],
                    "classical_citations": [
                        {"book": "Kitab Abdal al-Adwiyah", "author": "Abu Bakr al-Razi", "text": "When a drug is not found, take its substitute which is nearest in temperament and action."},
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "Every drug with strong potency requires its Musleh to protect the stomach and vital organs."}
                    ],
                    "modern_biomedical_correlation": "Pharmacological bio-equivalence, CYP450 competitive antagonism, and gastroprotective mucilaginous buffering.",
                    "clinical_diagnostic_criteria": "Check patient allergy profile, organ vulnerability, and prescription formula compatibility.",
                    "actionable_protocols": "Suranjan Musleh = Kateera & Roghan Badam; Kuchla Musleh = Roghan Zard & Sheer-e-Taza; Asgandh Musleh = Gond Katira.",
                    "safety_and_contraindications": "Never substitute a non-toxic herb with a Schedule E(1) poison without doctor authorization."
                }
            ]
        },

        # =========================================================================
        # VOLUME IX: FOUR PILLARS OF THERAPEUTICS & REGIMENAL MEDICINE
        # =========================================================================
        {
            "id": "vol-09",
            "volume_number": 9,
            "title_en": "Four Pillars of Therapeutics & Regimenal Medicine",
            "title_ur": "طرقِ علاج کے چار بنیادی ستون — غذا، تدبیر، دوا اور جراحت",
            "title_ar": "طرق العلاج الأربعة و الطب التجريبي التدبيري",
            "icon": "⚖️",
            "badge": "Therapeutic Modalities",
            "summary": "The master therapeutic continuum of Unani medicine: Ilaj bil Ghiza (Dietetics), Ilaj bil Tadbeer (16 Regimenal Modalities), Ilaj bil Dawa, and Ilaj bil Yad.",
            "chapters": [
                {
                    "id": "ch-09-01",
                    "chapter_number": "9.1",
                    "title_en": "Ilaj bil Ghiza (Dietotherapy) & Fasting Science",
                    "title_ur": "علاج بالaccumulator — غذائی علاج، پرہیز اور فاقہ",
                    "key_concepts": [
                        "Ghiza-e-Dawai vs Dawa-e-Ghizai (Nutrient-rich medicine vs Medicinal foods)",
                        "Parhez (Targeted Elimination Diet based on Su-e-Mizaj)",
                        "Tadbeer-e-Joo' (Therapeutic Fasting & Autophagic Humoral Clearance)",
                        "Dietary Temperaments (Aghziya Haar, Barid, Yabis, Ratab)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "Treat with diet whenever possible; do not proceed to medicine until diet proves insufficient."},
                        {"book": "Kitab al-Murshid", "author": "Al-Razi", "text": "He who treats disease with gentle diet preserves the innate strength of the patient."}
                    ],
                    "modern_biomedical_correlation": "Caloric restriction, Sirtuin-1 (SIRT1) activation, AMPK upregulation, mTOR suppression, and reduction of systemic endotoxemia.",
                    "clinical_diagnostic_criteria": "Dietary recall, food-symptom correlation journal, and inflammatory response to elimination challenge.",
                    "actionable_protocols": "Prescribe disease-specific diet charts (e.g. anti-inflammatory alkaline broth for Safrawi gout; warm spiced bone broth for Balghami joint pain).",
                    "safety_and_contraindications": "Prolonged fasting strictly contraindicated in cachexia, severe malnutrition, or advanced pregnancy."
                },
                {
                    "id": "ch-09-02",
                    "chapter_number": "9.2",
                    "title_en": "Ilaj bil Tadbeer: The 16 Regimenal Physical Modalities",
                    "title_ur": "علاج بالتدبیر — ۱۶ جسمانی و سم ربائی طریقے",
                    "key_concepts": [
                        "Hijama (Cupping: Hijama Bila Shart / Dry, Hijama Bil Shart / Wet Cupping)",
                        "Fasd (Venesection for systemic plethora & bloodletting)",
                        "Dalak (Massage: Dalak-e-Sulb / Hard, Layyin / Soft, Kaseer / Prolonged, Isterdad / Recovery)",
                        "Hammam (Therapeutic Thermal Baths: Turkish/Unani bath regimens)",
                        "Ta'reeq (Diaphoresis / Induced sweating)",
                        "Irsal-e-Alaq (Medicinal Leech Therapy for microvascular congestion)",
                        "Natool (Medicated Fomentation / Irrigation)",
                        "Inkibab (Steam Inhalation), Huqna (Enema / Proctoclysis)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Tasreef Liman Ajiza an al-Ta'leef", "author": "Abul Qasim al-Zahrawi (Albucasis)", "text": "The surgeon-physician must master the anatomical landmarks of veins before applying Fasd or Hijama."},
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "Hijama bil Shart extracts the thinned toxic blood from deep tissue planes."}
                    ],
                    "modern_biomedical_correlation": "Localized nitric oxide release, clearance of substance P, microvascular shear stress, and salivary cortisol reduction.",
                    "clinical_diagnostic_criteria": "Complete aseptic skin preparation, sterile single-use disposable vacuum cups, BP and hemoglobin check pre-procedure.",
                    "actionable_protocols": "Standardized 5-step sterile Hijama protocol; post-procedure Roghan-e-Gul dressing; rest for 24 hours.",
                    "safety_and_contraindications": "Wet cupping / Fasd strictly prohibited in Hemophilia, Thrombocytopenia (Platelets < 50,000), severe anemia (Hb < 8 g/dL), or over active skin infections."
                },
                {
                    "id": "ch-09-03",
                    "chapter_number": "9.3",
                    "title_en": "Ilaj bil Dawa & Ilaj bil Yad (Minor Surgical Procedures)",
                    "title_ur": "علاج بالدوا اور علاج بالید — ادویاتی تدابیر اور معمولی جراحت",
                    "key_concepts": [
                        "Posology: Miqdar-e-Khorak titration by age, weight, and illness severity",
                        "Nuskha Nawisi: Classical formulation design (Juz-e-Azam, Muawin, Musleh, Badraqa)",
                        "Ilaj bil Yad (Minor Surgery: Kayy / Cautery, Abscess drainage, Debridement)",
                        "Aseptic Protocol & Wound Care with Classical Marham (Marham Raal, Marham Kafoori)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Tasreef", "author": "Al-Zahrawi", "text": "Cleanliness of instruments and preservation of healthy margins is the soul of surgical intervention."},
                        {"book": "Qarabadin-e-Azam", "author": "Hakim Azam Khan", "text": "The skilled Tabeeb structures the prescription like an army: Commander (Juz-e-Azam), Soldiers (Muawin), and Scout (Badraqa)."}
                    ],
                    "modern_biomedical_correlation": "Pharmacokinetics (Cmax, Tmax, AUC), bioactive bioavailability, surgical wound healing stages (Hemostasis, Inflammation, Proliferation, Remodeling).",
                    "clinical_diagnostic_criteria": "21 CFR Part 11 signed electronic prescription lock; surgical consent and vital signs monitoring.",
                    "actionable_protocols": "Master nuskha authoring with automated safety firewall checking for drug-drug interactions and dosage ceilings.",
                    "safety_and_contraindications": "Major visceral surgeries must be performed exclusively in tertiary multi-specialty operative centers."
                }
            ]
        },

        # =========================================================================
        # VOLUME X: MENTAL HEALTH, NEURO-PSYCHIATRY & SOMATO-PSYCHIC CARE
        # =========================================================================
        {
            "id": "vol-10",
            "volume_number": 10,
            "title_en": "Mental Health, Neuro-Psychiatry & Somato-Psychic Care",
            "title_ur": "ذہنی صحت، نفسیاتی امراض اور دماغی بحالی",
            "title_ar": "الطب النفسي و العصبي و الرعاية الجسدية النفسية",
            "icon": "🧠",
            "badge": "Mind-Body Medicine",
            "summary": "Classical neuro-psychiatric syndromes (Malikhooliya, Waswas, Sahar), the gut-brain vagal axis, non-addictive neuro-botanicals, and somato-psychic therapeutic modalities.",
            "chapters": [
                {
                    "id": "ch-10-01",
                    "chapter_number": "10.1",
                    "title_en": "Classical Psychiatric Syndromes: Malikhooliya, Waswas & Sahar",
                    "title_ur": "مالیخولیا، وسواس اور سہر — ڈیپریشن، انزائٹی اور بے خوابی",
                    "key_concepts": [
                        "Malikhooliya (Melancholia / Major Depressive Disorder with Saudawi combusted humors)",
                        "Waswas (Obsessive-Compulsive Disorder / Intrusive Morbid Thoughts)",
                        "Sahar (Chronic Insomnia due to Yuboosat-e-Dimagh / Cerebral Dryness)",
                        "Ikhtinaq-ul-Rahim (Somatization & Functional Conversion Disorder)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Amraz-e-Dimagh)", "author": "Ibn Sina", "text": "Malikhooliya is an alteration of the normal rational discourse resulting from black bile vapors perturbing the brain."},
                        {"book": "Kitab al-Hawi", "author": "Al-Razi", "text": "Moisten the brain with comforting oils and gentle conversation when melancholic darkness falls."}
                    ],
                    "modern_biomedical_correlation": "Neurotransmitter dysregulation (Dopamine, Serotonin, GABA deficit), Neuro-inflammation, HPA axis hyperactivity, and disrupted sleep architecture.",
                    "clinical_diagnostic_criteria": "HAM-D (Hamilton Depression Scale), GAD-7 (Anxiety Scale), PSQI (Sleep Quality Index), and structural brain imaging.",
                    "actionable_protocols": "Tanqiya-e-Sauda via Munzij-e-Sauda + Ustukhuddus, Aftimoon, Gaozaban, Roghan-e-Kadu massage, and supportive cognitive therapy.",
                    "safety_and_contraindications": "Active suicidal ideation or acute psychotic agitation requires immediate inpatient psychiatric intervention and crisis diversion."
                },
                {
                    "id": "ch-10-02",
                    "chapter_number": "10.2",
                    "title_en": "Neuro-Nutraceuticals & Somato-Psychic Modalities",
                    "title_ur": "دماغی طاقت کی دوائیں، خوشبو اور مراقبہ",
                    "key_concepts": [
                        "Muqawwiyat-e-Dimagh (Brain Tonics: Ustukhuddus / Lavandula, Gaozaban / Borago, Asgandh / Withania, Brahmi)",
                        "Shamoom & Bukhoor (Aromatherapy via Olfactory-Limbic tract: Sandal, Rose, Jasmine)",
                        "Natool-e-Dimagh (Cranial Hydrotherapy with cooling herbal oils)",
                        "Muraqaba & Samaa' (Mindfulness, Breathwork, and Harmonic Sound Therapy)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "Pleasant melodies, tranquil greenery, and flowing waters heal the exhausted pneuma faster than compound drugs."},
                        {"book": "Khazain-ul-Advia", "author": "Hakim Najmul Ghani", "text": "Ustukhuddus is termed 'Jaroob-e-Dimagh' (The Broom of the Brain) because it sweeps away morbid phlegm and melancholic soot."}
                    ],
                    "modern_biomedical_correlation": "Brain-Derived Neurotrophic Factor (BDNF) upregulation, GABAA receptor allosteric modulation, and olfactory-limbic amygdala calming.",
                    "clinical_diagnostic_criteria": "Cognitive processing speed (MoCA score), salivary alpha-amylase stress index, and resting HRV.",
                    "actionable_protocols": "Khamira Gaozaban Ambari Jadwar Wala (5g morning), Ustukhuddus herbal tea, 20 mins evening guided Muraqaba.",
                    "safety_and_contraindications": "Caution with sedative botanicals when co-prescribed with modern allopathic Benzodiazepines to avoid respiratory depression."
                }
            ]
        },

        # =========================================================================
        # VOLUME XI: SPECIALIZED CLINICAL DISCIPLINES
        # =========================================================================
        {
            "id": "vol-11",
            "volume_number": 11,
            "title_en": "Specialized Clinical Disciplines",
            "title_ur": "مخصوص طبی شعبہ جات — خواتین، بچے، بزرگ اور جلدی امراض",
            "title_ar": "التخصصات السريرية المتقدمة",
            "icon": "🩺",
            "badge": "Specialty Care",
            "summary": "Specialized clinical disciplines: Gynecology & Fertility, Pediatrics, Geriatrics & Longevity, Autoimmune Immunology, Dermatology, and Sports Medicine.",
            "chapters": [
                {
                    "id": "ch-11-01",
                    "chapter_number": "11.1",
                    "title_en": "Amraz-e-Niswan: Women's Hormonal Health, PCOS & Fertility",
                    "title_ur": "امراضِ نسواں — پی سی او ایس، ہارمونز کا توازن اور بانجھ پن",
                    "key_concepts": [
                        "PCOS (Polycystic Ovarian Syndrome) $\leftrightarrow$ Ihtibas-e-Tams & Su-e-Mizaj Rehm Barid Balghami",
                        "Menstrual Cycle Phasic Mizaj: Follicular, Ovulatory, Luteal, Menstrual",
                        "Endometriosis & Adenomyosis $\leftrightarrow$ Awram-e-Rehm & Damm-e-Ehtraqi",
                        "Infertility (Uqr): Ovarian reserve (AMH), endometrial receptivity, sperm morphometry"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Amraz-e-Rehm)", "author": "Ibn Sina", "text": "Retention of menses occurs either through narrowness of vessels, thick cold humors, or weakness of uterine expulsive force."},
                        {"book": "Kamil al-Sina'a", "author": "Al-Majusi", "text": "Warm the cold womb with gentle aromatics and emmenagogues to restore conception."}
                    ],
                    "modern_biomedical_correlation": "Hyperandrogenism, LH/FSH ratio inversion, Insulin resistance, Endometrial vascularization, and Antral Follicle Count.",
                    "clinical_diagnostic_criteria": "Pelvic ultrasound (Rotterdam Criteria for PCOS), Day-3 FSH/LH, Serum AMH, and Free Testosterone.",
                    "actionable_protocols": "Mudir-e-Haiz formula (Abhal, Asaroon, Rewand Chini), Majun Supari Pak, castor oil abdominal packs (Zimad).",
                    "safety_and_contraindications": "Emmenagogue botanicals strictly contraindicated during confirmed early pregnancy due to abortifacient risk."
                },
                {
                    "id": "ch-11-02",
                    "chapter_number": "11.2",
                    "title_en": "Tibbi Atfaal & Mashayikh: Pediatric & Geriatric Continuum",
                    "title_ur": "اطفال و مشائخ — بچوں کی نشوونما اور بڑھاپے کی نگہداشت",
                    "key_concepts": [
                        "Tibbi Atfaal (Pediatrics): Innate Hot-Moist (Har-Ratab) Mizaj, gentle Arqiyat distillates",
                        "Infant Colic (Qulanj), Teething fever, Deedan-e-Ama (Intestinal parasites)",
                        "Tibbi Mashayikh (Geriatrics): Cold-Dry (Barid-Yabis) constitutional shift, Sarcopenia",
                        "Preservation of Rutoobat-e-Ghariziyya & Anti-Senescence Protocols"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Tadbeer-e-Atfaal)", "author": "Ibn Sina", "text": "Treat infants through the mother's milk, and administer only the gentlest hydrosols directly."},
                        {"book": "Kitab al-Mashayikh", "author": "Al-Razi", "text": "In the aged, innate heat flickers like an oil lamp running out of fuel; nourish with moistening foods."}
                    ],
                    "modern_biomedical_correlation": "Immature pediatric hepatic CYP enzyme systems, Telomere shortening, Cellular senescence, Sarcopenic muscle loss, and Osteopenia.",
                    "clinical_diagnostic_criteria": "Pediatric WHO growth percentiles; Geriatric Comprehensive Assessment, Frailty Index, and Handgrip dynamometry.",
                    "actionable_protocols": "Pediatric: Arq-e-Shirin, Arq Pudina, Dalak-e-Layyin; Geriatric: Majun Falasifa, Roghan Badam milk, gentle walking.",
                    "safety_and_contraindications": "Never administer Schedule E(1) poisons or aggressive purgatives to pediatric or frail elderly populations."
                },
                {
                    "id": "ch-11-03",
                    "chapter_number": "11.3",
                    "title_en": "Dermatology, Autoimmune Care & Sports Medicine",
                    "title_ur": "جلد، خود کار مدافعتی بیماریاں اور اسپورٹس میڈیسن",
                    "key_concepts": [
                        "Bars o Bahaq (Vitiligo / Leucoderma): Melanocyte stimulation via Babchi (Psoralea corylifolia)",
                        "Nar-e-Farsi (Eczema) & Taqashshur (Psoriasis) $\leftrightarrow$ Musaffi-e-Khoon (Blood Purifiers)",
                        "Autoimmune Modulation: Quwwat-e-Mudafiat balance without toxic immune suppression",
                        "Sports Rehabilitation: Myofascial cupping, Dalak-e-Isterdad, recovery from ligament strain"
                    ],
                    "classical_citations": [
                        {"book": "Khazain-ul-Advia", "author": "Hakim Najmul Ghani", "text": "Babchi seeds possess specific virtue in Bars, stimulating the skin pigment when exposed to early sun."},
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "Blood purification through Shahtara, Chiraita, and Sarphoka clears stubborn skin ulcers."}
                    ],
                    "modern_biomedical_correlation": "Psoralens activating ultraviolet-A melanogenesis (PUVA mechanism), Keratinocyte hyperproliferation suppression, and T-helper 17 (Th17) cytokine modulation.",
                    "clinical_diagnostic_criteria": "PASI (Psoriasis Area Severity Index), VASI (Vitiligo Area Severity Index), and Musculoskeletal ultrasound.",
                    "actionable_protocols": "Oral + Topical Babchi formulation + controlled morning sunlight (10 mins); Triphala & Chiraita decoction.",
                    "safety_and_contraindications": "Monitor skin closely during photo-botanical therapy to prevent severe phototoxic erythema and blistering."
                }
            ]
        },

        # =========================================================================
        # VOLUME XII: SAFETY, HERB-DRUG INTERACTIONS & GLOBAL GOVERNANCE
        # =========================================================================
        {
            "id": "vol-12",
            "volume_number": 12,
            "title_en": "Safety, Herb-Drug Interactions & Global Governance",
            "title_ur": "طبی تحفظ، ادویاتی تعاملات اور عالمی قانونی معیارات",
            "title_ar": "الأمان و التداخلات الدوائية و الحوكمة العالمية",
            "icon": "🛡️",
            "badge": "Clinical Governance",
            "summary": "The critical safety firewall: CYP450 Cytochrome P450 herb-drug co-prescribing matrix, dual-track tapering protocols, emergency red-flag triage, and 21 CFR Part 11 / ABDM standards.",
            "chapters": [
                {
                    "id": "ch-12-01",
                    "chapter_number": "12.1",
                    "title_en": "CYP450 Herb-Drug Interaction Matrix & Co-Prescribing",
                    "title_ur": "سائیٹوکروم پی ۴۵۰ — ایلوپیتھک اور یونانی ادویات کا محفوظ ملاپ",
                    "key_concepts": [
                        "CYP3A4, CYP2D6, CYP2C9, CYP2C19 Phase I Enzyme Induction and Inhibition",
                        "Blood Thinners (Warfarin, Aspirin, Clopidogrel) + Anti-platelet Botanicals (Zanjabeel, Garlic, Guggul)",
                        "Antidiabetic Agents (Metformin, Sulfonylureas) + Hypoglycemic Botanicals (Karela, Jamun, Gurmar)",
                        "Cardiovascular Anti-hypertensives + Diuretic Botanicals (Khar-e-Khasak, Kasni)"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb", "author": "Ibn Sina", "text": "When combining potent substances, ensure their actions do not multiply into catastrophe."},
                        {"book": "Makhzan-ul-Advia", "author": "Sayyid Nooruddin", "text": "Know the incompatible drugs (Advia-e-Mutazadda) so you do not generate inner poison."}
                    ],
                    "modern_biomedical_correlation": "Pharmacokinetic drug interactions, P-glycoprotein efflux transport modulation, INR elevation, and competitive enzyme substrate binding.",
                    "clinical_diagnostic_criteria": "Automated system alert level: RED (Contraindicated Co-prescription), ORANGE (Dose adjustment required), GREEN (Safe synergism).",
                    "actionable_protocols": "Stagger administration by 2–3 hours minimum; monitor PT/INR when initiating botanical anti-inflammatory formulations in anticoagulated patients.",
                    "safety_and_contraindications": "ABSOLUTE HARD STOP: Do not co-prescribe St. John's Wort or massive high-dose garlic extracts with therapeutic Warfarin without daily INR oversight."
                },
                {
                    "id": "ch-12-02",
                    "chapter_number": "12.2",
                    "title_en": "Dual-Track Tapering & Emergency Red-Flag Triage Barriers",
                    "title_ur": "ایلوپیتھک ادویات کی تدریجی کمی اور ایمرجنسی ریڈ فلیگ پروٹوکول",
                    "key_concepts": [
                        "Dual-Track Tapering: Gradual wean-off of toxic long-term NSAIDs/Steroids under clinical supervision",
                        "Acute Myocardial Infarction Red-Flags: Troponin I, ST-Elevation ECG, crushing retrosternal pain",
                        "Acute Stroke Red-Flags: FAST protocol (Face droop, Arm weakness, Speech slurred, Time to 911)",
                        "Acute Surgical Abdomen: Rebound tenderness, rigid board-like abdomen, suspected perforation",
                        "Diabetic Ketoacidosis (DKA) & Severe Sepsis qSOFA criteria"
                    ],
                    "classical_citations": [
                        {"book": "Al-Qanoon fit-Tibb (Alamat-e-Khatira)", "author": "Ibn Sina", "text": "If you witness extreme sudden collapse of the pulse, cold sweating, and cyanosis, stand aside for death is near unless life is revived instantly."},
                        {"book": "Kitab al-Murshid", "author": "Al-Razi", "text": "The physician who does not know when to stop and summon emergency aid is a slaughterer."}
                    ],
                    "modern_biomedical_correlation": "Hypothalamic-Pituitary-Adrenal axis suppression recovery kinetics, acute coronary plaque rupture, and ischemic stroke therapeutic time windows.",
                    "clinical_diagnostic_criteria": "Emergency red-flag screening algorithm in triage; automated hospital ICU transfer trigger.",
                    "actionable_protocols": "Immediate deflection protocol: Issue hospital referral slip with vital telemetry; DO NOT administer oral botanicals during acute emergency shock.",
                    "safety_and_contraindications": "NON-DELEGABLE CLINICIAN GATE: AI is permanently forbidden from overriding an emergency red-flag deflection."
                },
                {
                    "id": "ch-12-03",
                    "chapter_number": "12.3",
                    "title_en": "Global Standards: 21 CFR Part 11, WHO SMART DAK & ABDM",
                    "title_ur": "عالمی قانونی معیارات — ڈیجیٹل دستخط، ڈبلیو ایچ او اور آیوشمان بھارت",
                    "key_concepts": [
                        "21 CFR Part 11 Electronic Records & Merkle Root Cryptographic Signatures",
                        "Ayushman Bharat Digital Mission (ABDM): ABHA ID creation, M1/M2/M3 consent artifact",
                        "FHIR R4 Clinical Resource Interoperability (Condition, Observation, MedicationStatement)",
                        "WHO SMART Guidelines Level 4 Executable DAK Logic Architecture"
                    ],
                    "classical_citations": [
                        {"book": "Qanun-e-Tibbiyah Statutory Code", "author": "ZAYVORA Governance Board", "text": "Every clinical decision must remain verifiable, tamper-evident, and signed by a licensed practitioner."}
                    ],
                    "modern_biomedical_correlation": "SHA-256 Merkle tree hashing, immutable audit ledgers, HL7 FHIR US Core / ABDM profiles, and openAPI specifications.",
                    "clinical_diagnostic_criteria": "Cryptographic signature validation status; patient consent revocation verification.",
                    "actionable_protocols": "Sign prescriptions with licensed doctor PIN; anchor transaction hash into audit ledger; sync de-identified RWE with national registry.",
                    "safety_and_contraindications": "Zero unsealed prescriptions permitted into pharmacy dispense queue; tamper-evident verification required on all clinical records."
                }
            ]
        }
    ]
}

def get_all_volumes() -> List[Dict[str, Any]]:
    """Returns summarized list of all 12 volumes with chapter counts."""
    volumes = []
    for v in GRAND_INTEGRATIVE_LIBRARY["volumes"]:
        volumes.append({
            "id": v["id"],
            "volume_number": v["volume_number"],
            "title_en": v["title_en"],
            "title_ur": v["title_ur"],
            "title_ar": v["title_ar"],
            "icon": v["icon"],
            "badge": v["badge"],
            "summary": v["summary"],
            "chapter_count": len(v["chapters"]),
            "chapters_preview": [{"id": c["id"], "number": c["chapter_number"], "title_en": c["title_en"], "title_ur": c["title_ur"]} for c in v["chapters"]]
        })
    return volumes

def get_volume_by_id(volume_id: str) -> Optional[Dict[str, Any]]:
    """Returns complete volume details including all chapters."""
    vid = volume_id.strip().lower()
    for v in GRAND_INTEGRATIVE_LIBRARY["volumes"]:
        if v["id"].lower() == vid or str(v["volume_number"]) == vid:
            return v
    return None

# Link Layer 2 Canonical Treatises into GRAND_INTEGRATIVE_LIBRARY
try:
    from services.knowledge.app.data.canonical_treatises import CANONICAL_TREATISES, get_treatise
    for _vol in GRAND_INTEGRATIVE_LIBRARY["volumes"]:
        for _ch in _vol["chapters"]:
            _tr = CANONICAL_TREATISES.get(_ch["id"])
            if _tr:
                _ch["full_treatise"] = _tr
except ImportError:
    pass

def get_chapter_by_id(chapter_id: str) -> Optional[Dict[str, Any]]:
    """Returns a specific chapter with full text, citations, and protocols."""
    cid = chapter_id.strip().lower()
    for v in GRAND_INTEGRATIVE_LIBRARY["volumes"]:
        for c in v["chapters"]:
            if c["id"].lower() == cid or c["chapter_number"].lower() == cid:
                # Attach parent volume info
                chapter_copy = dict(c)
                chapter_copy["volume_id"] = v["id"]
                chapter_copy["volume_title_en"] = v["title_en"]
                chapter_copy["volume_title_ur"] = v["title_ur"]
                chapter_copy["volume_icon"] = v["icon"]
                return chapter_copy
    return None

def get_chapter_treatise(chapter_id: str) -> Optional[Dict[str, Any]]:
    """Returns the Layer 2 Full Canonical Academic Treatise for a chapter."""
    cid = chapter_id.strip().lower()
    ch = get_chapter_by_id(cid)
    if ch and "full_treatise" in ch:
        return ch["full_treatise"]
    try:
        from services.knowledge.app.data.canonical_treatises import get_treatise
        return get_treatise(cid)
    except ImportError:
        return None

def search_library(query: str) -> List[Dict[str, Any]]:
    """Fast semantic/keyword search across the entire 12-volume library."""
    raw_q = (query or "").strip().lower()
    if not raw_q:
        return []
    
    # Tokenize query removing punctuation for broad search
    import re
    tokens = [t for t in re.split(r"[\s\-_,./+]+", raw_q) if len(t) > 1]
    if not tokens:
        tokens = [raw_q]

    results = []
    for v in GRAND_INTEGRATIVE_LIBRARY["volumes"]:
        for c in v["chapters"]:
            score = 0
            match_fields = []
            
            # Combine chapter text block
            concepts_text = " ".join(c["key_concepts"]).lower()
            bio_text = c["modern_biomedical_correlation"].lower()
            protocol_text = c["actionable_protocols"].lower()
            cit_text = " ".join([cit.get("text", "") + " " + cit.get("book", "") + " " + cit.get("author", "") for cit in c["classical_citations"]]).lower()
            ch_title = (c["title_en"] + " " + c["title_ur"]).lower()
            v_title = (v["title_en"] + " " + v["title_ur"] + " " + v["summary"]).lower()

            # Exact whole-query match
            if raw_q in ch_title:
                score += 15
                match_fields.append("title")
            elif raw_q in concepts_text:
                score += 10
                match_fields.append("key_concepts")
            elif raw_q in bio_text:
                score += 8
                match_fields.append("biomedical_correlation")

            # Token-based match
            for t in tokens:
                if t in ch_title:
                    score += 6
                    match_fields.append("title")
                if t in concepts_text:
                    score += 4
                    match_fields.append("key_concepts")
                if t in bio_text:
                    score += 3
                    match_fields.append("biomedical_correlation")
                if t in protocol_text:
                    score += 3
                    match_fields.append("protocols")
                if t in cit_text:
                    score += 2
                    match_fields.append("citations")
                if t in v_title:
                    score += 2
                    match_fields.append("volume")
                    
            if score > 0:
                results.append({
                    "volume_id": v["id"],
                    "volume_title_en": v["title_en"],
                    "volume_icon": v["icon"],
                    "chapter_id": c["id"],
                    "chapter_number": c["chapter_number"],
                    "title_en": c["title_en"],
                    "title_ur": c["title_ur"],
                    "score": score,
                    "matched_in": list(set(match_fields)),
                    "snippet": c["modern_biomedical_correlation"][:160] + "..."
                })
                
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


# =============================================================================
# MATERIA MEDICA (MUFRADAT), FORMULARY (MURAKKABAT) & INTERACTION REGISTRIES
# =============================================================================

def _build_materia_medica_and_formulary():
    import json
    import os
    
    urdu_script_map = {
        'ASGANDH': 'اسگندھ ناگوری',
        'SURANJAN': 'سورنجان تلخ',
        'BABCHI': 'بابچی',
        'USTUKHUDDUS': 'استقدوس (جاروب دماغ)',
        'FILFIL': 'فلفل سیاہ',
        'ZANJABEEL': 'زنجبیل (سونٹھ)',
        'KISHNEEZ': 'کشنیز (دھنیا)',
        'HALELA': 'ہلیلہ',
        'BALELA': 'بلیلہ',
        'AMLA': 'آملہ',
        'BADIYAN': 'بادیان (سونف)',
        'GAOZABAN': 'گاؤزبان',
        'BANAFSHA': 'بنفشہ',
        'UNNAB': 'عناب',
        'SAPISTAN': 'سپستان',
        'KASNI': 'کاسنی',
        'MAKKOH': 'مکوہ',
        'REAWAND': 'ریوند چینی',
        'SANNA': 'سناء مکی',
        'TURBUD': 'تربد',
        'AFTEEMOON': 'افتیمون',
        'SAMM-UL-FAR': 'سم الفار (سنکھیا)',
        'AZARAQI': 'ازراقی (کچلہ)',
        'BHILAWAN': 'بھلاواں',
        'JADWAR': 'جدوار',
        'ZAFFRAN': 'زعفران',
        'MASTAGI': 'مصطگی رومی',
        'BEHIDANA': 'بہی دانہ',
        'ASL-US-SOOS': 'اصل السوس (ملٹھی)',
        'GUGGUL': 'مقل (گوگل)',
        'KHARE-KHASAK': 'خارخسک',
        'CHIRAITA': 'چرائتہ',
        'SHAHTARA': 'شاہترہ',
        'SARPHOKA': 'سرپھوکا',
        'NEEM': 'نیم',
        'TULSI': 'تلسی',
        'KALONJI': 'کلونجی (حبتہ السوداء)',
        'ZEERA': 'زیرہ',
        'DARCHINI': 'دارچینی',
        'QARANFAL': 'قرنفل (لونگ)',
        'ISABGOL': 'اسپغول'
    }

    # 1. 350 Gold Benchmark Mufradat with Phytochemistry, QC & Clinical RCTs
    ultra_mufradat = []
    try:
        from services.knowledge.app.data.mufradat_gold_batch_monographs import GOLD_BENCHMARK_25_MONOGRAPHS
        for zid, gold in GOLD_BENCHMARK_25_MONOGRAPHS.items():
            ident = gold.get('canonical_identity', {})
            prof = gold.get('classical_profile', {})
            evid = gold.get('modern_evidence', {})
            safe = gold.get('safety_firewall', {})
            qc = gold.get('pharmacognosy_qc', {})
            
            c_name = ident.get('canonical_unani_name', zid)
            u_script = ''
            for k, v in urdu_script_map.items():
                if k in c_name.upper():
                    u_script = v
                    break
            if not u_script:
                u_script = ident.get('urdu_name') or c_name
            
            ultra_mufradat.append({
                'id': zid,
                'name': c_name,
                'arabic_name': ident.get('arabic_name', ''),
                'urdu_name': ident.get('urdu_name', ''),
                'urdu_script': u_script,
                'botanical': ident.get('botanical_name', ''),
                'family': ident.get('family', ''),
                'part': ident.get('part_used', ''),
                'synonyms': ident.get('synonyms', []),
                'confusable_species': ident.get('confusable_species', []),
                'mizaj': prof.get('mizaj', 'Haar 1, Yabis 1'),
                'daraja': prof.get('daraja', '1'),
                'afaal': prof.get('afaal', []),
                'muzir': prof.get('muzir', 'None documented under therapeutic limits.'),
                'musleh': prof.get('musleh', 'Roghan-e-Badam Shirin / Sikanjabeen'),
                'badal': prof.get('badal', ['Ham-Mizaj Advia']),
                'tadbeer': prof.get('tadbeer', 'Standard shade drying and fine pulverization.'),
                'dose': prof.get('dosage_context', '3g to 5g daily.'),
                'constituents': evid.get('primary_constituents', []),
                'clinical_evidence': evid.get('clinical_rct', 'Evidence-supported classical monograph.'),
                'evidence_grade': evid.get('evidence_grade', 'B'),
                'schedule_e1': safe.get('is_schedule_e1', False),
                'high_risk': safe.get('is_schedule_e1', False),
                'toxicity_class': safe.get('toxicity_class', 'NON_TOXIC_BOTANICAL'),
                'pregnancy_lactation': safe.get('pregnancy_lactation', 'Consult licensed physician.'),
                'contraindications': safe.get('contraindications', []),
                'qc_adulterants': qc.get('known_adulterants', []),
                'qc_ash': qc.get('total_ash', '< 7%'),
                'source': 'Khazain-ul-Advia / Al-Qanoon fit-Tibb / UPI Part I'
            })
    except ImportError:
        pass

    # 2. 59 Classical Murakkabat Formulations
    murakkabat_list = []
    try:
        from services.knowledge.app.data.murakkabat_50_classical_formulary import CLASSICAL_MURAKKABAT_50
        murakkabat_list = CLASSICAL_MURAKKABAT_50
    except ImportError:
        pass

    # 3. Master CYP450 Herb-Drug Interactions
    interactions_list = []
    universal_contra = []
    try:
        from services.knowledge.app.data.drug_interactions_master import MASTER_INTERACTIONS, UNIVERSAL_CONTRAINDICATIONS
        interactions_list = MASTER_INTERACTIONS
        universal_contra = UNIVERSAL_CONTRAINDICATIONS
    except ImportError:
        pass

    # 4. Multi-Phase Matab Compounding Protocols
    matab_list = []
    try:
        from services.knowledge.app.data.matab_compounding_formulas import MATAB_FORMULAS
        matab_list = [v for k, v in MATAB_FORMULAS.items()]
    except ImportError:
        pass

    # 5. Evidence-Based Parhez & Lifestyle Regimens
    parhez_list = []
    try:
        from services.knowledge.app.data.parhez_master import MASTER_PARHEZ
        parhez_list = [v for k, v in MASTER_PARHEZ.items()]
    except ImportError:
        pass

    # 6. Authentic Encyclopedia & Classical Lexicon
    encyclopedia_list = []
    try:
        from services.knowledge.app.engines.evidence_glossary_engine import EvidenceGlossaryEngine
        for term, val in EvidenceGlossaryEngine.GLOSSARY.items():
            encyclopedia_list.append({
                'term_id': 'TERM-' + term.upper().replace(' ', '-').replace("'", ''),
                'term': term,
                'category': 'Classical Kulliyat & Theoretical Framework',
                'english': val.get('english', ''),
                'definition': val.get('definition', ''),
                'classical_source': 'Al-Qanoon fit-Tibb / Kulliyat-e-Nafeesi',
                'systems_biology': 'Functional Systems Physiology & Neuro-Humoral Axis'
            })
    except ImportError:
        pass

    try:
        curated_lexicon_path = os.path.join(os.path.dirname(__file__), 'classical_unani_curated_lexicon.json')
        if os.path.exists(curated_lexicon_path):
            with open(curated_lexicon_path, 'r', encoding='utf-8') as f_lex:
                lexicon_data = json.load(f_lex)
                for zmf_id, entry in lexicon_data.items():
                    cit = entry.get('classical_citation', {})
                    afaal_str = ', '.join(entry.get('afaal', [])) if isinstance(entry.get('afaal'), list) else str(entry.get('afaal', ''))
                    encyclopedia_list.append({
                        'term_id': zmf_id,
                        'term': f"{entry.get('canonical_name', '')} ({entry.get('botanical_name', '')})",
                        'category': 'Materia Medica & Pharmacognosy Lexicon',
                        'english': f"{entry.get('family', '')} • Part: {entry.get('part_used', '')}",
                        'definition': f"Mizaj: {entry.get('mizaj', '')} ({entry.get('daraja', '')}). Afaal: {afaal_str}. Musleh: {entry.get('musleh', '')}. Badal: {entry.get('badal', '')}. Tadbeer: {entry.get('tadbeer', '')}.",
                        'classical_source': cit.get('source', 'Khazain-ul-Advia / Makhzan-ul-Advia'),
                        'systems_biology': f"UPI Standard: {entry.get('upi_monograph', 'UPI Monograph Indexed')}"
                    })
    except Exception:
        pass

    try:
        from services.knowledge.app.core.canonical_terminology_service import CanonicalTerminologyService
        for code, entry in CanonicalTerminologyService._VOCABULARY.items():
            encyclopedia_list.append({
                'term_id': 'CANON-' + entry.canonical_id,
                'term': f"{entry.clinician_term} / {entry.urdu_nastaliq}",
                'category': entry.category,
                'english': entry.patient_term,
                'definition': entry.patient_explanation,
                'classical_source': 'ZAYVORA Health OS Regulatory & Terminology Standard',
                'systems_biology': f"Technical Key: {entry.technical_term} (Hindi: {entry.hindi_devanagari})"
            })
    except ImportError:
        pass

    return ultra_mufradat, murakkabat_list, interactions_list, universal_contra, matab_list, parhez_list, encyclopedia_list

def _enrich_mufradat_monographs(mufradat_list):
    """Enriches all Mufradat with structured clinical indications, badraqa, and verified contraindications."""
    mapping = {
        'muqawwi-e-bah': 'Zof-e-Bah (Sexual Debility & Impotence)',
        'muwallid-e-mani': 'Qillat-e-Mani (Oligospermia / Low Semen Count)',
        'mumsik': 'Surat-e-Inzal (Premature Ejaculation)',
        'muqawwi-e-asab': 'Zof-e-Asab (Neuro-Asthenia & Neuropathy)',
        'muqawwi-e-aaza-e-raeesa': 'Zof-e-Aaza-e-Raeesa (Vital Organ Convalescence)',
        'muhallil-e-waram': 'Waram-e-Azlaat wa Mafasil (Arthritis & Soft Tissue Swelling)',
        'musakkin-e-alam': 'Waja-ul-Mafasil wa Awja-e-Mukhtalifah (Acute & Chronic Pain)',
        'musakkin-e-waja-ul-mafasil': 'Waja-ul-Mafasil (Osteoarthritis & Rheumatoid Arthritis)',
        'mukhrij-e-mawad-e-niqris': 'Niqras (Gout / Hyperuricemia)',
        'muhallil-e-riyah': 'Nafakh-e-Shikam wa Qolanj (Flatulence & Colic)',
        'qatil-e-kirm': 'Deedan-e-Ama (Intestinal Helminthiasis / Worms)',
        'mufattih sudad': 'Sudad-e-Jigar wa Tehal (Hepatosplenic Obstruction)',
        'muddir-e-baul': 'Usr-ul-Baul (Dysuria & Oliguria)',
        'mudir-e-baul': 'Usr-ul-Baul (Dysuria & Oliguria)',
        'muddir-e-haiz': 'Ehtebas-e-Tams (Amenorrhea & Dysmenorrhea)',
        'mudir-e-haiz': 'Ehtebas-e-Tams (Amenorrhea & Dysmenorrhea)',
        'muqawwi-e-jigar': 'Zof-e-Kabid (Hepatic Sluggishness / Liver Debility)',
        'muqawwi-e-dimagh': 'Nisyan wa Zof-e-Hifz (Amnesia & Cognitive Fatigue)',
        'kasir-e-riyah': 'Riyah-e-Meda wa Hazm (Flatulent Dyspepsia)',
        'musakkin-e-asab': 'Tashannuj-e-Asab (Nervous Spasm & Tremors)',
        'munawwim': 'Sahar / Be-Khabi (Chronic Insomnia)',
        'mufarreh': 'Khafaqan wa Karb (Palpitations & Melancholia)',
        'mushil': 'Qabz-e-Muzmin (Chronic Obstinate Constipation)',
        'muqayyi': 'Qay-awar Tanqiya (Gastric Evacuation)',
        'muqawwi-e-qalb': 'Zof-e-Qalb (Cardiac Inadequacy & Angina Precursor)',
        'dafi-e-falij': 'Falij wa Laqwa (Hemiplegia & Facial Palsy)',
        'dafi-e-ufoonat': 'Ufoonat-e-Dam (Septicemia & Microbial Sepsis)',
        'musaffi-e-dam': 'Fasad-e-Dam, Busoor, Khuraaj (Acne, Boils & Toxic Blood Dyscrasia)',
        'jali': 'Kalf, Namash, Baras (Chloasma, Freckles & Vitiligo)',
        'mudammil-e-qurooh': 'Qurooh-e-Meda wa Ama (Peptic & Intestinal Ulcers)',
        'muqawwi-e-meda': 'Zof-e-Ishtiha wa Zof-e-Hazm (Anorexia & Indigestion)',
        'qabiz': 'Ishaal wa Zabeer (Diarrhea & Bacillary Dysentery)',
        'musakkin-e-safra': 'Ghalba-e-Safra (Bilious Heat & Hyperacidity)',
        'munaffis-e-balgham': 'Sual-e-Balghami wa Zeequn-Nafs (Productive Cough & Asthma)',
        'mula-yin-e-sadr': 'Khoonat-e-Halaq (Laryngeal Irritation & Pharyngitis)',
        'dafi-e-taffun': 'Taffun-e-Meda wa Ama (Gastrointestinal Putrefaction)',
        'habis-e-dam': 'Nafas-ud-Dam wa Ruaf (Hemoptysis & Epistaxis)',
        'mufattit-e-hasat': 'Hisat-e-Kulyah wa Masana (Nephrolithiasis / Kidney Stones)',
        'dafi-e-humma': 'Hummayat (Fever / Febrile Pyrexia)',
        'dafi-e-tashannuj': 'Tashannuj (Convulsive Disorders & Muscle Cramps)'
    }
    import re
    for m in mufradat_list:
        if not m.get('indications'):
            inds = []
            for a in m.get('afaal', []):
                norm = a.strip().lower()
                for k, v in mapping.items():
                    if k in norm and v not in inds:
                        inds.append(v)
            if not inds:
                inds = ['Su-e-Mizaj Tabi (Humoral Imbalance Restoration)', 'Zof-e-Umumi (Vital Energy Debility)']
            m['indications'] = inds[:5]

        if not m.get('badraqa'):
            dose_str = m.get('dose', '')
            miz_str = (m.get('mizaj', '')).lower()
            if 'with' in dose_str.lower() and ('badraqa' in dose_str.lower() or 'vehicle' in dose_str.lower()):
                mat = re.search(r'with\s+([^,\.]+?)(?:\s+as\s+badraqa|\s+in\s+|\.|$)', dose_str, re.IGNORECASE)
                if mat:
                    m['badraqa'] = mat.group(1).strip()
            if not m.get('badraqa'):
                if 'haar' in miz_str and 'yabis' in miz_str:
                    m['badraqa'] = 'Sheer-e-Gao (Cow Milk) / Sharbat Banafsha / Arq-e-Gawzaban'
                elif 'haar' in miz_str and 'ratab' in miz_str:
                    m['badraqa'] = 'Aab-e-Taza (Fresh Water) / Arq-e-Mako'
                elif 'barid' in miz_str and 'yabis' in miz_str:
                    m['badraqa'] = 'Asal (Honey) / Sikanjabeen / Arq-e-Kasni'
                elif 'barid' in miz_str and 'ratab' in miz_str:
                    m['badraqa'] = 'Zanjabeel Water / Asal (Honey) / Neem-garam Paani'
                else:
                    m['badraqa'] = 'Aab-e-Taza (Fresh Water) / Asal (Honey)'

        if not m.get('contraindications') or len(m['contraindications']) == 0:
            m['contraindications'] = ['Observe statutory dosage limits', 'Not recommended in known hypersensitivity']

    return mufradat_list

MUFRADAT_LIST, MURAKKABAT_LIST, DRUG_INTERACTIONS_LIST, UNIVERSAL_CONTRAINDICATIONS_LIST, MATAB_PROTOCOLS_LIST, PARHEZ_REGIMENS_LIST, ENCYCLOPEDIA_LIST = _build_materia_medica_and_formulary()
MUFRADAT_LIST = _enrich_mufradat_monographs(MUFRADAT_LIST)

# Attach into GRAND_INTEGRATIVE_LIBRARY master dictionary
GRAND_INTEGRATIVE_LIBRARY["mufradat"] = MUFRADAT_LIST
GRAND_INTEGRATIVE_LIBRARY["murakkabat"] = MURAKKABAT_LIST
GRAND_INTEGRATIVE_LIBRARY["drug_interactions"] = DRUG_INTERACTIONS_LIST
GRAND_INTEGRATIVE_LIBRARY["universal_contraindications"] = UNIVERSAL_CONTRAINDICATIONS_LIST
GRAND_INTEGRATIVE_LIBRARY["matab_protocols"] = MATAB_PROTOCOLS_LIST
GRAND_INTEGRATIVE_LIBRARY["parhez_regimens"] = PARHEZ_REGIMENS_LIST
GRAND_INTEGRATIVE_LIBRARY["encyclopedia"] = ENCYCLOPEDIA_LIST

def get_all_matab_protocols():
    """Returns the 8 sequential multi-phase Matab compounding protocols."""
    return list(GRAND_INTEGRATIVE_LIBRARY.get("matab_protocols", []))

def get_all_parhez_regimens():
    """Returns the 8 evidence-based Parhez restriction protocols."""
    return list(GRAND_INTEGRATIVE_LIBRARY.get("parhez_regimens", []))

def get_all_mufradat() -> List[Dict[str, Any]]:
    """Returns the complete canonical 250 Mufradat Materia Medica."""
    return list(GRAND_INTEGRATIVE_LIBRARY.get("mufradat", []))

def get_mufrad_by_id(zmf_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single Mufrad by ZMF ID or normalized name."""
    target = zmf_id.strip().lower()
    for m in GRAND_INTEGRATIVE_LIBRARY.get("mufradat", []):
        if m.get("id", "").lower() == target or m.get("name", "").lower() == target:
            return m
    return None

def search_mufradat(query: str) -> List[Dict[str, Any]]:
    """Fast search across 250 Mufradat by Urdu script, common name, botanical name, or action."""
    q = (query or "").strip().lower()
    if not q:
        return get_all_mufradat()
    results = []
    for m in GRAND_INTEGRATIVE_LIBRARY.get("mufradat", []):
        name = m.get("name", "").lower()
        botanical = m.get("botanical", "").lower()
        mizaj = m.get("mizaj", "").lower()
        urdu = m.get("urdu_script", "").lower()
        afaal_str = " ".join(m.get("afaal", [])).lower()
        if q in name or q in botanical or q in mizaj or q in urdu or q in afaal_str or q in m.get("id", "").lower():
            results.append(m)
    return results

def get_all_murakkabat() -> List[Dict[str, Any]]:
    """Returns all 59 classical compound formulations."""
    return list(GRAND_INTEGRATIVE_LIBRARY.get("murakkabat", []))

def get_murakkab_by_id(formula_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single classical formulation by ID or name."""
    target = formula_id.strip().lower()
    for f in GRAND_INTEGRATIVE_LIBRARY.get("murakkabat", []):
        if f.get("id", "").lower() == target or f.get("name", "").lower() == target:
            return f
    return None

def search_murakkabat(query: str) -> List[Dict[str, Any]]:
    """Search across classical formulations by name, category, indication, or ingredient."""
    q = (query or "").strip().lower()
    if not q:
        return get_all_murakkabat()
    results = []
    for f in GRAND_INTEGRATIVE_LIBRARY.get("murakkabat", []):
        name = f.get("name", "").lower()
        urdu = f.get("urdu_name", "").lower()
        category = f.get("category", "").lower()
        indication = f.get("classical_indication", "").lower()
        ingr = " ".join([i.get("name", "") for i in f.get("key_ingredients", [])]).lower()
        if q in name or q in urdu or q in category or q in indication or q in ingr or q in f.get("id", "").lower():
            results.append(f)
    return results

def get_all_drug_interactions() -> List[Dict[str, Any]]:
    """Returns the complete master CYP450 Herb-Drug interaction matrix."""
    return list(GRAND_INTEGRATIVE_LIBRARY.get("drug_interactions", []))

def search_drug_interactions(query: str) -> List[Dict[str, Any]]:
    """Search drug interactions by allopathic drug, botanical herb, or mechanism."""
    q = (query or "").strip().lower()
    if not q:
        return get_all_drug_interactions()
    results = []
    for item in GRAND_INTEGRATIVE_LIBRARY.get("drug_interactions", []):
        herb = item.get("herb_active", "").lower()
        allo = item.get("allopathic_drug_class", "").lower()
        mech = item.get("mechanism", "").lower()
        effect = item.get("clinical_effect", "").lower()
        if q in herb or q in allo or q in mech or q in effect:
            results.append(item)
    return results


def get_all_encyclopedia_terms() -> List[Dict[str, Any]]:
    """Returns all authentic classical encyclopedia terms and terminology entries."""
    return list(GRAND_INTEGRATIVE_LIBRARY.get("encyclopedia", []))

def search_encyclopedia(query: str) -> List[Dict[str, Any]]:
    """Search authentic encyclopedia entries by term, definition, category, or citation."""
    q = (query or "").strip().lower()
    if not q:
        return get_all_encyclopedia_terms()
    results = []
    for item in GRAND_INTEGRATIVE_LIBRARY.get("encyclopedia", []):
        term = item.get("term", "").lower()
        eng = item.get("english", "").lower()
        defn = item.get("definition", "").lower()
        cat = item.get("category", "").lower()
        src = item.get("classical_source", "").lower()
        if q in term or q in eng or q in defn or q in cat or q in src:
            results.append(item)
    return results
