"""
ZAYVORA Health OS™ — Grand Integrative Medical Canon & Evidence Hierarchy Master
================================================================================
Definitive 6-Level Scholarly Evidence Hierarchy, Classical Canons, Qarabadeen Formularies,
Official AYUSH Standards, and Modern Biomedical Textbooks.

Editorial Mandate:
- Zero Fabricated / Synthetic Records. 100% Peer-Reviewed, Ministry-Standard & Classical Treatises.
- 19-Point Standard Drug Monograph Architecture.
- Strict Tiered Hierarchy for AI Clinical Decision Support (Hakeem Sahab™ CDS).
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional

# =============================================================================
# THE 19-POINT CANONICAL DRUG MONOGRAPH ARCHITECTURE
# =============================================================================
CANONICAL_MONOGRAPH_SCHEMA_19_POINTS = [
    {"point": 1, "field": "arabic_persian_urdu_name", "title": "Arabic / Persian / Urdu Canonical Nomenclature (الاسم العربي والفارسي والأردي)"},
    {"point": 2, "field": "botanical_identity_and_taxonomy", "title": "Botanical Identity, Family & Binomial Taxonomy"},
    {"point": 3, "field": "synonyms_and_regional_names", "title": "Synonyms, Classical Cognates & Vernacular Regional Names"},
    {"point": 4, "field": "mizaj_temperament_and_degree", "title": "Mizaj (Temperament & Qualitative Degrees: Har, Barid, Ratab, Yabis)"},
    {"point": 5, "field": "afaal_primary_actions", "title": "Afaal (Primary Physiological & Pharmacological Actions)"},
    {"point": 6, "field": "therapeutic_actions_and_properties", "title": "Therapeutic Actions & Pharmacodynamic Properties"},
    {"point": 7, "field": "clinical_indications_amraz", "title": "Clinical Indications & Disease Target Systems (Mahall-e-Amraz)"},
    {"point": 8, "field": "dosage_miqdar_e_khoorak", "title": "Posology & Dosage (Miqdar-e-Khoorak by Age, Route, Form)"},
    {"point": 9, "field": "method_of_preparation_and_purification", "title": "Method of Preparation & Detoxification (Tadbeer / Mudabbar SOPs)"},
    {"point": 10, "field": "musleh_corrective_agents", "title": "Musleh (Corrective & Antidotal Agents for Mitigating Side-Effects)"},
    {"point": 11, "field": "badal_substitutes", "title": "Badal (Canonical Pharmacological Substitutes & Therapeutic Alternates)"},
    {"point": 12, "field": "contraindications", "title": "Contraindications (Mawane-e-Istemal: Pregnancy, Hepatorenal, Pediatric)"},
    {"point": 13, "field": "adverse_effects_and_toxicity", "title": "Muzirrat (Adverse Effects, Toxicological Warnings & Target Organs)"},
    {"point": 14, "field": "compound_formulations_murakkabat", "title": "Compound Formulations (Major Murakkabat in which Drug is Key Ingredient)"},
    {"point": 15, "field": "classical_canonical_references", "title": "Classical Canonical Citations (Volume, Discourse & Chapter References)"},
    {"point": 16, "field": "modern_pharmacology_and_mechanism", "title": "Modern Phytochemistry, Active Constituents & Molecular Mechanism of Action"},
    {"point": 17, "field": "clinical_evidence_and_trials", "title": "Modern Clinical Evidence, Human In-Vivo Trials & Systematic Reviews"},
    {"point": 18, "field": "toxicology_and_safety_limits", "title": "Toxicology, LD50, Heavy Metal Limits & Teratogenic Assessment"},
    {"point": 19, "field": "pharmacopoeial_quality_standards", "title": "Statutory Pharmacopoeial Standards (TLC/HPTLC Fingerprints, Extractive Values)"}
]


# =============================================================================
# THE 6-LEVEL ZAYVORA EVIDENCE HIERARCHY
# =============================================================================
ZAYVORA_EVIDENCE_HIERARCHY: Dict[str, Dict[str, Any]] = {
    # -------------------------------------------------------------------------
    # LEVEL 1: ORIGINAL CLASSICAL SOURCES
    # -------------------------------------------------------------------------
    "LEVEL_1": {
        "tier_name": "Original Classical Canon Sources (الأمهات والكتب الطبية الكبرى)",
        "priority_rank": 1,
        "description": "Foundational doctrinal authorities establishing the core principles of human physiology, humoral balance, etiology, and internal clinical medicine.",
        "authorities": [
            {
                "title": "Al-Qanun fi al-Tibb (The Canon of Medicine)",
                "arabic_title": "القانون في الطب",
                "author": "Ibn Sina (Avicenna, 980–1037 CE)",
                "scope": "Foundational medical theory, Mizaj (temperaments), Akhlat (humors), Afaal (functions), systemic diseases (head to toe), simples (Mufradat) and compounds (Aqrabadhin).",
                "canonical_editions": ["Rome Medici Press (1593)", "Bulaq Cairo Edition (1877)", "CCRUM Urdu Translation (Govt of India, 5 Volumes)"],
                "jurisdiction": "GLOBAL_CLASSICAL"
            },
            {
                "title": "Al-Hawi fi al-Tibb (Continens Liber)",
                "arabic_title": "الحاوي في الطب",
                "author": "Abu Bakr Muhammad ibn Zakariyya al-Razi (Rhazes, 865–925 CE)",
                "scope": "Exhaustive 23-volume clinical compilation of bedside case observations, original hospital records, differential diagnosis, and experimental therapeutic reasoning.",
                "canonical_editions": ["Dairat-ul-Ma'arif al-Osmania, Hyderabad Edition (1955–1971, 23 Volumes)"],
                "jurisdiction": "GLOBAL_CLASSICAL"
            },
            {
                "title": "Kamil al-Sina'a al-Tibbiyya (Al-Kitab al-Maliki / Liber Regius)",
                "arabic_title": "کامل الصناعة الطبية (الكتاب الملكي)",
                "author": "Ali ibn al-Abbas al-Majusi (Haly Abbas, c. 930–994 CE)",
                "scope": "Major early comprehensive medical manual dividing medical science into 10 discourses on theoretical principles and 10 discourses on applied clinical therapeutics.",
                "canonical_editions": ["Bulaq Cairo Classical Edition (1877, 2 Volumes)"],
                "jurisdiction": "GLOBAL_CLASSICAL"
            },
            {
                "title": "Zakhira-i Khwarazm Shahi",
                "persian_title": "ذخیره خوارزمشاهی",
                "author": "Sayyid Ismail Jurjani (1042–1136 CE)",
                "scope": "One of the greatest Persian Unani medical encyclopedias in 10 books covering anatomy, hygiene, diagnosis, fevers, surgery, pharmacology, and poisons.",
                "canonical_editions": ["Bonyad-e Farhang-e Iran Edition (Tehran)", "Idara Kitab-us-Shifa New Delhi (Urdu Translation)"],
                "jurisdiction": "PERSIAN_CLASSICAL"
            },
            {
                "title": "Sharh al-Asbab wa'l-Alamat",
                "arabic_title": "شرح الأسباب والعلامات",
                "author": "Burhan-ud-Din Nafis ibn Awad al-Kirmani (d. 1449 CE)",
                "scope": "Masterwork on special pathology, clinical signs, cardinal symptoms, etiology, and therapeutic management commenting on Samarqandi's Asbab.",
                "canonical_editions": ["Munshi Nawal Kishore Press (Lucknow, 1879)", "CCRUM Urdu Edition (New Delhi)"],
                "jurisdiction": "CLASSICAL_PATHOLOGY"
            },
            {
                "title": "Kitab al-Tasreef liman 'Ajiza 'an al-Ta'leef",
                "arabic_title": "كتاب التصريف لمن عجز عن التأليف",
                "author": "Abul Qasim Khalaf ibn al-Abbas al-Zahrawi (Albucasis, 936–1013 CE)",
                "scope": "Monumental 30-volume medical encyclopedia famous for Treatise 30 on Ilaj bil Tadbeer (Hijama/cupping, Fasd/venesection, Kai/cautery, and 200+ surgical instruments).",
                "canonical_editions": ["Dar al-Kitab al-Lubnani Edition", "John Channing Oxford Latin/Arabic Edition (1778)"],
                "jurisdiction": "CLASSICAL_SURGERY_TADBEER"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # LEVEL 2: CLASSICAL UNANI MATERIA MEDICA & MUFRADAT
    # -------------------------------------------------------------------------
    "LEVEL_2": {
        "tier_name": "Classical Unani Materia Medica & Mufradat (كتب المفردات وعلم الأدوية الكلاسيكي)",
        "priority_rank": 2,
        "description": "Comprehensive monographs on medicinal plants, animal substances, and minerals, detailing temperamental degrees, primary actions, correctives (Musleh), and substitutes (Badal).",
        "authorities": [
            {
                "title": "Makhzan al-Adwiya / Makhzan-ul-Advia",
                "persian_title": "مخزن الادویہ",
                "author": "Mir Muhammad Husain Al-Alawi Shirazi (1771 CE)",
                "scope": "The supreme classical Indo-Persian Materia Medica. Comprehensive repository of single drugs, precise temperaments, degrees, specific actions, correctives (Musleh), and substitutes (Badal).",
                "canonical_editions": ["Munshi Nawal Kishore Press (Lucknow, 1874)", "CCRUM Edition (New Delhi)"]
            },
            {
                "title": "Ikhtiyarat-i Badi'i",
                "persian_title": "اختیارات بدیعی",
                "author": "Zain al-Din Ali ibn al-Husain al-Ansari (Haji Zain al-Attar, 1329–1404 CE)",
                "scope": "Authoritative Persian Materia Medica in two parts: Part 1 cataloging simple drugs alphabetically; Part 2 detailing compound formulations and antidotes.",
                "canonical_editions": ["Tehran University Medical Manuscripts Edition (1992)", "Calcutta Manuscript Press"]
            },
            {
                "title": "Kitab al-Jami' li-Mufradat al-Adwiya wa-al-Aghdhiya",
                "arabic_title": "الجامع لمفردات الأدوية والأغذية",
                "author": "Allama Ibn al-Baitar (Diya al-Din al-Malaqi, 1197–1248 CE)",
                "scope": "The most comprehensive botanical and pharmaceutical encyclopedia of classical antiquity, citing 150+ classical authors across 1,400+ medicinal substances.",
                "canonical_editions": ["Bulaq Cairo Edition (1874, 4 Volumes)", "Dar al-Kutub al-Ilmiyyah (Beirut, 1992)"]
            },
            {
                "title": "Muheet-e-Azam",
                "persian_title": "محیط اعظم",
                "author": "Hakim Muhammad Azam Khan (Nazim-e-Jahan, 1814–1902 CE)",
                "scope": "Monumental 4-volume compendium of single drugs synthesizing Arabic, Persian, Ayurvedic, and vernacular Indian botanical scholarship.",
                "canonical_editions": ["Munshi Nawal Kishore Press (Lucknow, 1896, 4 Volumes)", "CCRUM Urdu Edition (New Delhi)"]
            },
            {
                "title": "Khazain-ul-Advia",
                "urdu_title": "خزائن الادویہ",
                "author": "Hakim Najmul Ghani Rampuri (1859–1932 CE)",
                "scope": "Exhaustive 3-volume Urdu encyclopedia of single drugs with multilingual synonyms (Arabic, Persian, Hindi, Latin), degrees of temperament, and posology.",
                "canonical_editions": ["Munshi Nawal Kishore Press (Lucknow, 1926, 3 Volumes)", "Idara Kitab-us-Shifa (New Delhi)"]
            }
        ]
    },

    # -------------------------------------------------------------------------
    # LEVEL 3: CLASSICAL FORMULARIES (QARABADEEN LITERATURE)
    # -------------------------------------------------------------------------
    "LEVEL_3": {
        "tier_name": "Classical Formularies (Qarabadeen Literature / کتب قرابادین ومصنفات تراکیب)",
        "priority_rank": 3,
        "description": "Essential compound formulation manuals (Murakkabat) providing authentic compounding methods, weights, dosage, and therapeutic indications.",
        "authorities": [
            {
                "title": "Qarabadeen-e-Azam",
                "urdu_title": "قرابادین اعظم",
                "author": "Hakim Muhammad Azam Khan (Nazim-e-Jahan, 1814–1902 CE)",
                "scope": "Grand master formulary detailing thousands of classical compound formulations, specific clinical actions, dosage variations, and preparation methods.",
                "canonical_editions": ["Munshi Nawal Kishore Press (Lucknow, 1895)", "CCRUM Edition (New Delhi)"]
            },
            {
                "title": "Qarabadeen-e-Qadri",
                "persian_title": "قرابادین قادری",
                "author": "Hakim Muhammad Akbar Arzani (d. 1722 CE)",
                "scope": "Celebrated practical clinical formulary organized by anatomical disease sections, documenting tried-and-tested prescriptions.",
                "canonical_editions": ["Munshi Nawal Kishore Press (Lucknow, 1875)", "CCRUM Edition (New Delhi)"]
            },
            {
                "title": "Qarabadeen-e-Jadid",
                "urdu_title": "قرابادین جدید",
                "author": "Hakim Mohammad Kabiruddin",
                "scope": "Modern standardized formulary reconciling classical recipes with metric weights, modern pharmaceutical standards, and dispensary practice.",
                "canonical_editions": ["Idara Kitab-us-Shifa (New Delhi, 1935)", "Hikmat Book Depot (Lahore)"]
            },
            {
                "title": "Qarabadeen-e-Najm-ul-Ghani",
                "urdu_title": "قرابادین نجم الغنی",
                "author": "Hakim Najmul Ghani Rampuri (1859–1932 CE)",
                "scope": "Comprehensive Urdu pharmaceutical formulary covering syrups (Ashriba), electuaries (Majun/Jawarish/Khamira), pills (Habb), and powders (Sufuf).",
                "canonical_editions": ["Munshi Nawal Kishore Press (Lucknow, 1928)", "Idara Kitab-us-Shifa Edition"]
            },
            {
                "title": "Qarabadeen-e-Shifa'i",
                "persian_title": "قرابادین شفائی",
                "author": "Muzaffar ibn Muhammad al-Husaini al-Shifa'i (d. 1556 CE)",
                "scope": "Classical Persian formulary that served as the primary basis for the Pharmacopoeia Persica (first printed pharmacopoeia in the Middle East).",
                "canonical_editions": ["Lucknow Edition (1878)", "Tehran University Manuscripts (1970)"]
            },
            {
                "title": "Bayaz-e-Kabir (Vol I & II)",
                "urdu_title": "بیاض کبیر",
                "author": "Hakim Mohammad Kabiruddin",
                "scope": "Standard formulary used across Indian Unani colleges and manufacturing pharmacies, specifying authentic recipes and clinical dosages.",
                "canonical_editions": ["Idara Kitab-us-Shifa (New Delhi, 1938, 2 Volumes)"]
            }
        ]
    },

    # -------------------------------------------------------------------------
    # LEVEL 4: OFFICIAL INDIAN UNANI STANDARDS & STATUTORY PHARMACOPOEIAS
    # -------------------------------------------------------------------------
    "LEVEL_4": {
        "tier_name": "Official Indian Unani Standards & Statutory Pharmacopoeias (معاییر دستور الادویہ)",
        "priority_rank": 4,
        "description": "Statutory regulatory standards bridging classical literature with contemporary pharmaceutical quality, safety, and legal compliance.",
        "authorities": [
            {
                "title": "The Unani Pharmacopoeia of India (UPI, Parts I & II)",
                "authority": "Pharmacopoeia Commission for Indian Medicine & Homeopathy (PCIM&H), Ministry of AYUSH, Govt of India",
                "scope": "Statutory standards for single drugs (Part I, multiple volumes) and compound formulations (Part II), defining botanical identity, TLC fingerprints, and purity.",
                "regulatory_status": "STATUTORY_BINDING (Drugs & Cosmetics Act, 1940, Second Schedule)",
                "volumes": ["Part I: Vol I to VI (Single Drugs)", "Part II: Vol I to IV (Compound Formulations)"]
            },
            {
                "title": "National Formulary of Unani Medicine (NFUM, Parts I to VI)",
                "authority": "Ministry of AYUSH, Government of India",
                "scope": "Official standardized manufacturing formulas, proportions of ingredients, therapeutic indications, and legal dosage limits for classical formulations.",
                "regulatory_status": "STATUTORY_BINDING (Drugs & Cosmetics Rules, 1945)",
                "volumes": ["Parts I, II, III, IV, V, VI"]
            },
            {
                "title": "Central Council for Research in Unani Medicine (CCRUM) Publications",
                "authority": "CCRUM, Ministry of AYUSH, Government of India",
                "scope": "Standardization monographs, ethnobotanical survey reports, clinical research trial monographs, and verified safety reviews.",
                "regulatory_status": "OFFICIAL_GOVERNMENT_RESEARCH"
            },
            {
                "title": "Unani Pharmacopoeia Committee (UPC) Monographs & Gazette Notifications",
                "authority": "Ministry of AYUSH, Government of India",
                "scope": "Official pharmacopoeial amendments, Schedule E(1) poisonous botanical purification requirements, and heavy metal permissible limits.",
                "regulatory_status": "STATUTORY_GAZETTE"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # LEVEL 5: MODERN BIOMEDICAL SCIENCES (STANDARD MEDICAL TEXTBOOKS)
    # -------------------------------------------------------------------------
    "LEVEL_5": {
        "tier_name": "Modern Biomedical Sciences (Gold-Standard Clinical Medical Textbooks)",
        "priority_rank": 5,
        "description": "Standard authoritative clinical references across all major medical specialties to ground integrative diagnoses, laboratory testing, and pathology.",
        "disciplines": {
            "Anatomy": [
                {"book": "Gray's Anatomy: The Anatomical Basis of Clinical Practice", "authors": "Susan Standring (Editor-in-Chief)", "edition": "42nd Edition (Elsevier)", "standard": "GOLD_STANDARD"},
                {"book": "Atlas of Human Anatomy", "authors": "Frank H. Netter, MD", "edition": "8th Edition (Elsevier)", "standard": "CLINICAL_ATLAS"},
                {"book": "Snell's Clinical Anatomy by Regions", "authors": "Lawrence E. Wineski", "edition": "10th Edition (Wolters Kluwer)", "standard": "REGIONAL_CLINICAL"}
            ],
            "Physiology": [
                {"book": "Guyton and Hall Textbook of Medical Physiology", "authors": "John E. Hall, Michael E. Hall", "edition": "14th Edition (Elsevier)", "standard": "GOLD_STANDARD"},
                {"book": "Ganong's Review of Medical Physiology", "authors": "Kim E. Barrett, Susan M. Barman et al.", "edition": "26th Edition (McGraw-Hill)", "standard": "CELLULAR_INTEGRATIVE"},
                {"book": "Costanzo Physiology", "authors": "Linda S. Costanzo", "edition": "7th Edition (Elsevier)", "standard": "SYSTEMS_PHYSIOLOGY"}
            ],
            "Pathology": [
                {"book": "Robbins & Cotran Pathologic Basis of Disease", "authors": "Vinay Kumar, Abul K. Abbas, Jon C. Aster", "edition": "10th Edition (Elsevier)", "standard": "GOLD_STANDARD"},
                {"book": "Textbook of Pathology", "authors": "Harsh Mohan", "edition": "8th Edition (Jaypee Brothers)", "standard": "CLINICAL_HISTOPATHOLOGY"}
            ],
            "Pharmacology": [
                {"book": "Goodman & Gilman's: The Pharmacological Basis of Therapeutics", "authors": "Laurence L. Brunton, Björn C. Knollmann", "edition": "14th Edition (McGraw-Hill)", "standard": "GOLD_STANDARD"},
                {"book": "Basic & Clinical Pharmacology", "authors": "Bertram G. Katzung, Todd W. Vanderah", "edition": "15th Edition (McGraw-Hill)", "standard": "MECHANISTIC_CLINICAL"},
                {"book": "Essentials of Medical Pharmacology", "authors": "K.D. Tripathi", "edition": "8th Edition (Jaypee Brothers)", "standard": "THERAPEUTIC_CLINICAL"}
            ],
            "Internal Medicine": [
                {"book": "Harrison's Principles of Internal Medicine", "authors": "Joseph Loscalzo, Anthony S. Fauci, Dennis L. Kasper et al.", "edition": "21st Edition (McGraw-Hill, 2 Volumes)", "standard": "GOLD_STANDARD"},
                {"book": "Davidson's Principles and Practice of Medicine", "authors": "Ian D. Penman, Stuart H. Ralston et al.", "edition": "24th Edition (Elsevier)", "standard": "CLINICAL_BEDSIDE"}
            ],
            "General Surgery": [
                {"book": "Bailey & Love's Short Practice of Surgery", "authors": "P. Ronan O'Connell, Andrew W. McCaskie, Robert D. Sayers", "edition": "28th Edition (CRC Press)", "standard": "GOLD_STANDARD"},
                {"book": "Sabiston Textbook of Surgery: The Biological Basis of Modern Surgical Practice", "authors": "Courtney M. Townsend Jr. et al.", "edition": "21st Edition (Elsevier)", "standard": "BIOLOGICAL_SURGICAL"},
                {"book": "Schwartz's Principles of Surgery", "authors": "F. Charles Brunicardi et al.", "edition": "11th Edition (McGraw-Hill)", "standard": "OPERATIVE_CLINICAL"}
            ],
            "Pediatrics": [
                {"book": "Nelson Textbook of Pediatrics", "authors": "Robert M. Kliegman, Joseph W. St. Geme III et al.", "edition": "21st Edition (Elsevier, 2 Volumes)", "standard": "GOLD_STANDARD"},
                {"book": "Ghai Essential Pediatrics", "authors": "Vinod K. Paul, Arvind Bagga", "edition": "10th Edition (CBS Publishers)", "standard": "REGIONAL_PEDIATRIC"}
            ],
            "Dermatology": [
                {"book": "Fitzpatrick's Dermatology", "authors": "Sewon Kang, Masayuki Amagai, Anna L. Bruckner et al.", "edition": "9th Edition (McGraw-Hill, 2 Volumes)", "standard": "GOLD_STANDARD"},
                {"book": "Rook's Textbook of Dermatology", "authors": "Christopher Griffiths, Jonathan Barker et al.", "edition": "9th Edition (Wiley-Blackwell, 4 Volumes)", "standard": "ENCYCLOPEDIC_DERM"}
            ],
            "Preventive & Social Medicine (PSM) / Public Health": [
                {"book": "Park's Textbook of Preventive and Social Medicine", "authors": "K. Park", "edition": "27th Edition (M/s Banarsidas Bhanot)", "standard": "EPIDEMIOLOGICAL_GOLD"},
                {"book": "Maxcy-Rosenau-Last Public Health & Preventive Medicine", "authors": "Matthew L. Boulton, Robert B. Wallace", "edition": "16th Edition (McGraw-Hill)", "standard": "GLOBAL_PUBLIC_HEALTH"}
            ],
            "Radiology & Imaging": [
                {"book": "Grainger & Allison's Diagnostic Radiology: A Textbook of Medical Imaging", "authors": "Andy Adam, Adrian K. Dixon et al.", "edition": "7th Edition (Elsevier, 2 Volumes)", "standard": "GOLD_STANDARD"},
                {"book": "Brant and Helms' Fundamentals of Diagnostic Radiology", "authors": "Clyde A. Helms et al.", "edition": "5th Edition (Wolters Kluwer, 4 Volumes)", "standard": "COMPREHENSIVE_IMAGING"}
            ],
            "Obstetrics & Gynecology": [
                {"book": "Williams Obstetrics", "authors": "F. Gary Cunningham, Kenneth J. Leveno et al.", "edition": "26th Edition (McGraw-Hill)", "standard": "GOLD_STANDARD_OBSTETRICS"},
                {"book": "DC Dutta's Textbook of Obstetrics & Gynecology", "authors": "Hiralal Konar", "edition": "9th Edition (Jaypee Brothers)", "standard": "CLINICAL_OBGYN"},
                {"book": "Shaw's Textbook of Gynaecology", "authors": "V.G. Padubidri, Shirish N. Daftary", "edition": "17th Edition (Elsevier)", "standard": "GYNAECOLOGICAL_PATHOLOGY"}
            ],
            "Microbiology & Infectious Diseases": [
                {"book": "Jawetz, Melnick & Adelberg's Medical Microbiology", "authors": "Stefan Riedel, Stephen A. Morse et al.", "edition": "28th Edition (McGraw-Hill)", "standard": "GOLD_STANDARD"},
                {"book": "Ananthanarayan and Paniker's Textbook of Microbiology", "authors": "Reba Kanungo", "edition": "12th Edition (Universities Press)", "standard": "CLINICAL_BACTERIOLOGY"},
                {"book": "Mandell, Douglas, and Bennett's Principles and Practice of Infectious Diseases", "authors": "John E. Bennett, Raphael Dolin, Martin J. Blaser", "edition": "9th Edition (Elsevier, 2 Volumes)", "standard": "ENCYCLOPEDIC_INFECTIOUS"}
            ],
            "Biochemistry & Genetics": [
                {"book": "Harper's Illustrated Biochemistry", "authors": "Peter J. Kennelly, Kathleen M. Botham et al.", "edition": "32nd Edition (McGraw-Hill)", "standard": "GOLD_STANDARD"},
                {"book": "Lehninger Principles of Biochemistry", "authors": "David L. Nelson, Michael M. Cox", "edition": "8th Edition (Macmillan Learning)", "standard": "MOLECULAR_BIOCHEMISTRY"}
            ],
            "Forensic Medicine & Toxicology": [
                {"book": "Parikh's Textbook of Medical Jurisprudence, Forensic Medicine and Toxicology", "authors": "C.K. Parikh", "edition": "8th Edition (CBS Publishers)", "standard": "JURISPRUDENCE_TOXICOLOGY"},
                {"book": "The Essentials of Forensic Medicine and Toxicology", "authors": "K.S. Narayan Reddy, O.P. Murty", "edition": "35th Edition (Jaypee Brothers)", "standard": "MEDICOLEGAL_STATUTORY"},
                {"book": "Goldfrank's Toxicologic Emergencies", "authors": "Lewis S. Nelson, Mary Ann Howland et al.", "edition": "11th Edition (McGraw-Hill)", "standard": "CLINICAL_TOXICOLOGY"}
            ]
        }
    },

    # -------------------------------------------------------------------------
    # LEVEL 6: MODERN UNANI REFERENCE LITERATURE & CONTEMPORARY TEXTBOOKS
    # -------------------------------------------------------------------------
    "LEVEL_6": {
        "tier_name": "Modern Unani Reference Literature & Institutional Textbooks (الكتب المرجعية الحديثة)",
        "priority_rank": 6,
        "description": "Contemporary academic textbooks, institutional compendia, and modern research literature serving as secondary interpretive aids.",
        "authorities": [
            {
                "title": "Hamdard Pharmacopoeia (Qarabadin-e-Hamdard)",
                "authority": "Hamdard Laboratories (India / Pakistan)",
                "scope": "Comprehensive industrial compounding specifications, commercial product standards, batch ratios, and clinical indications for patented and classical products.",
                "category": "INDUSTRIAL_INSTITUTIONAL"
            },
            {
                "title": "Institutional Academic Curriculum Textbooks (NCISM / BUMS / MD Unani)",
                "subjects": [
                    "Kulliyat Umoor-e-Tabi'iyyah (Basic Principles & Human Biology)",
                    "Tashreeh-ul-Badan (Unani Human Anatomy)",
                    "Munafe-ul-Aaza (Unani Human Physiology)",
                    "Ilmul Advia (Pharmacology & Materia Medica)",
                    "Saidla wa Murakkabat (Unani Pharmacy & Compounding)",
                    "Mahiyat-ul-Amraz (Pathology & Etiology)",
                    "Moalajat (Medicine & Systemic Therapeutics)",
                    "Ilaj bil Tadbeer (Regimenal & Physical Medicine)",
                    "Amraz-e-Niswan wa Qabalat (Obstetrics & Gynecology)",
                    "Amraz-e-Atfal (Pediatrics)",
                    "Jarahat (Unani Surgery & Minor Operative Procedures)",
                    "Ain-Uzn-Anaf-Halaq (ENT & Ophthalmology)"
                ],
                "category": "ACADEMIC_CURRICULUM"
            },
            {
                "title": "WHO Monographs on Selected Medicinal Plants (Volumes 1–4)",
                "authority": "World Health Organization (WHO), Geneva",
                "scope": "Global regulatory monographs establishing botanical identity, purity criteria, clinical trials, pharmacology, and adverse contraindications.",
                "category": "GLOBAL_PHYTOTHERAPY"
            },
            {
                "title": "ZAYVORA CP-AFUM Compendium of Axis-Based Functional Medicine",
                "author": "Hakeem Dr. Irfan Ashraf, BUMS (AKTC AMU Aligarh)",
                "scope": "Integrative curriculum textbook synthesizing classical temperament science with modern functional diagnostics and the 12 Organ-Axes.",
                "category": "INTEGRATIVE_AXIS_COMPENDIUM"
            }
        ]
    }
}


def get_evidence_hierarchy() -> Dict[str, Dict[str, Any]]:
    """Returns the full 6-level scholarly evidence hierarchy."""
    return ZAYVORA_EVIDENCE_HIERARCHY

def get_monograph_schema() -> List[Dict[str, Any]]:
    """Returns the 19-point canonical drug monograph architecture."""
    return CANONICAL_MONOGRAPH_SCHEMA_19_POINTS
