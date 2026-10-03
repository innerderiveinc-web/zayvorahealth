"""
ZAYVORA Health OS™ — Products Master Knowledge Catalog
======================================================
Contains all 32 compliance-corrected formulations:
- Section A: Chronic Disease Cluster (NCDs) (ZAY-001 to ZAY-008)
- Section B: ZAYVORA Brand Formulations (ZAY-009 to ZAY-022)
- Section C: Poshida Amraz / Rx & Controlled Formulations (ZAY-023 to ZAY-032)

Every entry includes:
- SKU & Product Name
- Classical Unani Classification & Formulation Type
- Active Ingredients with Quantities & HPLC Standardization
- Clinical Indications (Modern ICD-11 & Classical Unani Amraz)
- Standardized Dosage & Administration
- Contraindications & Warnings
- Regulatory Track (AYUSH Classic, AYUSH Schedule E-1 Rx, FSSAI Nutraceutical)
"""

from typing import Dict, Any, List, Optional

MASTER_PRODUCTS: Dict[str, Dict[str, Any]] = {
    # -------------------------------------------------------------------------
    # SECTION A: CHRONIC DISEASE CLUSTER (NCDs)
    # -------------------------------------------------------------------------
    "ZAY-001": {
        "sku": "ZAY-001",
        "name": "HyperCalm™",
        "unani_name": "Safoof-e-Tansiyat-ud-Dam",
        "formulation_type": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)",
        "regulatory_track": "AYUSH_SCHEDULE_E1_RX",
        "is_prescription_required": True,
        "mrp_inr": 1850,
        "organ_axis": "CEREBROVASCULAR",
        "primary_indication": "Essential Hypertension (Stage 1 & 2), Stress-induced systolic spikes, Zayt-e-Dam (blood tension)",
        "composition": [
            {"ingredient": "Asrol (Rauwolfia serpentina)", "amount_mg": 250, "standardization": "Reserpine 1.0%"},
            {"ingredient": "Ustukhuddus (Lavandula stoechas)", "amount_mg": 200, "standardization": "Linalool 3.5%"},
            {"ingredient": "Filfil Siyah (Piper nigrum)", "amount_mg": 50, "standardization": "Piperine 95%"},
            {"ingredient": "Kishneez Khushk (Coriandrum sativum)", "amount_mg": 250, "standardization": "Volatile Oil 0.8%"},
            {"ingredient": "Gul-e-Surkh (Rosa damascena)", "amount_mg": 150, "standardization": "Total Phenolics 5.0%"},
            {"ingredient": "Gaozaban (Borago officinalis)", "amount_mg": 100, "standardization": "Mucilage & Flavonoids"}
        ],
        "dosage": "1 to 2 capsules twice daily with lukewarm water or Arq Gaozaban 30 mins after meals",
        "contraindications": [
            "Active peptic ulcer disease",
            "Severe endogenous depression / suicidal ideation",
            "Bradycardia (HR < 55 bpm)",
            "Pregnancy & lactation (Absolute contraindication)"
        ],
        "monitoring": ["Blood Pressure weekly", "Heart rate", "Electrolytes if combined with diuretics"],
        "citations": ["AYUSH Pharmacopoeia Vol 1", "Cochrane Review on Rauwolfia Alkaloids in Hypertension 2020"]
    },
    "ZAY-002": {
        "sku": "ZAY-002",
        "name": "DiabEase™",
        "unani_name": "Safoof-e-Qawi-e-Banas",
        "formulation_type": "Micro-Granules (30 x 5g Daily Stick Sachets)",
        "regulatory_track": "AYUSH_CLASSICAL",
        "is_prescription_required": False,
        "mrp_inr": 1450,
        "organ_axis": "PANCREATIC",
        "primary_indication": "Ziabetus Shakari (Type 2 Diabetes Mellitus), Impaired Fasting Glucose, Peripheral Insulin Resistance",
        "composition": [
            {"ingredient": "Jamun Seeds (Syzygium cumini)", "amount_mg": 300, "standardization": "Jamboline & Tannins 15%"},
            {"ingredient": "Karela (Momordica charantia)", "amount_mg": 250, "standardization": "Charantin 2.5%"},
            {"ingredient": "Methi (Trigonella foenum-graecum)", "amount_mg": 200, "standardization": "4-Hydroxyisoleucine 20%"},
            {"ingredient": "Gurmar (Gymnema sylvestre)", "amount_mg": 250, "standardization": "Gymnemic Acids 25%"},
            {"ingredient": "Tukhm-e-Hulba", "amount_mg": 100, "standardization": "Saponins 10%"},
            {"ingredient": "Kushta Baiza-e-Murgh", "amount_mg": 50, "standardization": "Micro-calcified Elemental Calcium"}
        ],
        "dosage": "1 stick sachet (5g) twice daily dissolved in 100ml warm water 20 minutes before breakfast and dinner",
        "contraindications": [
            "Severe hypoglycemia prone patients without CGM",
            "Diabetic Ketoacidosis (DKA)",
            "Pregnancy gestational diabetes without specialist supervision"
        ],
        "monitoring": ["Fasting & PP Blood Glucose", "HbA1c every 90 days", "Renal profile"],
        "citations": ["Journal of Ethnopharmacology 2018; Gymnema Sylvestre beta-cell regeneration"]
    },
    "ZAY-003": {
        "sku": "ZAY-003",
        "name": "CardioGuard™",
        "unani_name": "Majoon-e-Muqawwi-e-Qalb",
        "formulation_type": "Majoon Granules (30 x 5g Daily Stick Sachets)",
        "regulatory_track": "AYUSH_CLASSICAL",
        "is_prescription_required": False,
        "mrp_inr": 2200,
        "organ_axis": "CARDIOVASCULAR",
        "primary_indication": "Zof-e-Qalb (Cardiac weakness), Khafqan (Palpitations), Post-cardiac rehabilitation, Endothelial dysfunction",
        "composition": [
            {"ingredient": "Zafran (Crocus sativus)", "amount_mg": 20, "standardization": "Crocin & Safranal 3.0%"},
            {"ingredient": "Marwareed (Pearl calx)", "amount_mg": 30, "standardization": "Bioactive Coral Carbonate"},
            {"ingredient": "Yashab Sabz", "amount_mg": 50, "standardization": "Purified Jade Calx"},
            {"ingredient": "Arjun Chhal (Terminalia arjuna)", "amount_mg": 400, "standardization": "Arjunic acid & Tannins 10%"},
            {"ingredient": "Badranjboya (Melissa officinalis)", "amount_mg": 200, "standardization": "Rosmarinic Acid 5%"},
            {"ingredient": "Seb juice & Asl base", "amount_mg": 3500, "standardization": "Natural Honey & Pectin Matrix"}
        ],
        "dosage": "1 stick sachet (5g) in the morning on empty stomach with warm milk or Arq Gulab",
        "contraindications": [
            "Unstable angina requiring immediate catheterization",
            "Severe uncompensated aortic stenosis",
            "Active hemorrhage"
        ],
        "monitoring": ["ECG", "Ejection fraction where clinically indicated", "Lipid panel"],
        "citations": ["International Journal of Cardiology; Terminalia arjuna in Heart Failure"]
    },
    "ZAY-004": {
        "sku": "ZAY-004",
        "name": "HepaClear™",
        "unani_name": "Safoof-e-Muqawwi-e-Jigar",
        "formulation_type": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)",
        "regulatory_track": "AYUSH_CLASSICAL",
        "is_prescription_required": False,
        "mrp_inr": 1350,
        "organ_axis": "HEPATOBILIARY",
        "primary_indication": "Zof-e-Jigar, Non-Alcoholic Fatty Liver Disease (NAFLD/MASLD), Sluggish bile clearance, Elevated transaminases",
        "composition": [
            {"ingredient": "Kasni (Cichorium intybus)", "amount_mg": 350, "standardization": "Cichoric acid 2.0%"},
            {"ingredient": "Mako (Solanum nigrum)", "amount_mg": 300, "standardization": "Solanine alkaloids <0.1%, Polyphenols 8%"},
            {"ingredient": "Tukhm-e-Kasoos (Cuscuta reflexa)", "amount_mg": 150, "standardization": "Cuscutin 5%"},
            {"ingredient": "Zarishk (Berberis vulgaris)", "amount_mg": 200, "standardization": "Berberine 8%"},
            {"ingredient": "Revand Chini (Rheum emodi)", "amount_mg": 100, "standardization": "Emodin & Rhein 3.5%"},
            {"ingredient": "Afsanteen (Artemisia absinthium)", "amount_mg": 100, "standardization": "Absinthin 1.5%"}
        ],
        "dosage": "1 to 2 capsules twice daily 30 minutes after meals with warm water or Arq Kasni",
        "contraindications": [
            "Complete mechanical biliary obstruction",
            "Fulminant hepatic failure",
            "Pregnancy (due to Revand Chini emmenagogue properties)"
        ],
        "monitoring": ["Liver Function Tests (ALT, AST, ALP, Bilirubin)", "Abdominal Ultrasound"],
        "citations": ["Phytotherapy Research 2019; Cichorium intybus hepatoprotection"]
    },
    "ZAY-005": {
        "sku": "ZAY-005",
        "name": "LipidClear™",
        "unani_name": "Safoof-e-Islah-e-Dam",
        "formulation_type": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)",
        "regulatory_track": "AYUSH_CLASSICAL",
        "is_prescription_required": False,
        "mrp_inr": 1250,
        "organ_axis": "METABOLIC",
        "primary_indication": "Dasaumat-ud-Dam (Hyperlipidemia, Dyslipidemia, elevated LDL/Triglycerides, low HDL)",
        "composition": [
            {"ingredient": "Lasan (Allium sativum extract)", "amount_mg": 250, "standardization": "Allicin 2.0%"},
            {"ingredient": "Guggulu (Commiphora mukul)", "amount_mg": 300, "standardization": "Guggulsterones E & Z 2.5%"},
            {"ingredient": "Amla (Phyllanthus emblica - Musleh for Guggulu)", "amount_mg": 150, "standardization": "Tannins & Vitamin C 30%"},
            {"ingredient": "Zanjabil (Zingiber officinale)", "amount_mg": 150, "standardization": "Gingerols 5%"},
            {"ingredient": "Halela Siyah (Terminalia chebula)", "amount_mg": 150, "standardization": "Chebulinic acid 20%"},
            {"ingredient": "Zeera Siyah (Carum carvi)", "amount_mg": 150, "standardization": "Carvone 3%"}
        ],
        "dosage": "1 to 2 capsules twice daily after heavy meals with warm water",
        "contraindications": [
            "Concurrent full-dose anticoagulant therapy (Warfarin/NOACs) without monitoring",
            "Bleeding diathesis",
            "Active thyroid crisis (Guggulu stimulates thyroid hormones)"
        ],
        "monitoring": ["Fasting Lipid Profile at 60 and 90 days", "Coagulation markers if on antiplatelets"],
        "citations": ["Science 2002; 296(5573): 1703-1706; DOI: 10.1126/science.1072891 (Guggulsterone as FXR antagonist in cholesterol clearance)"]
    },
    "ZAY-006": {
        "sku": "ZAY-006",
        "name": "LungEase™",
        "unani_name": "Lauq-e-Muqawwi-e-Sadr",
        "formulation_type": "Effervescent Micro-Granules (30 Sachets)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 950,
        "organ_axis": "PULMONARY",
        "primary_indication": "Zeequn-Nafs (Bronchial Asthma, Chronic Bronchitis, Spasmodic Cough, Post-viral mucosal congestion)",
        "composition": [
            {"ingredient": "Asl-us-Soos (Glycyrrhiza glabra)", "amount_mg": 300, "standardization": "Glycyrrhizin 10%"},
            {"ingredient": "Sapistan (Cordia latifolia)", "amount_mg": 250, "standardization": "Polysaccharide mucilage 20%"},
            {"ingredient": "Unnab (Ziziphus jujuba)", "amount_mg": 200, "standardization": "Jujubosides 3%"},
            {"ingredient": "Behidana (Cydonia oblonga)", "amount_mg": 150, "standardization": "Pectin & Mucilage 25%"},
            {"ingredient": "Banafsha (Viola odorata)", "amount_mg": 100, "standardization": "Violanthin & Rutin 2%"},
            {"ingredient": "Natural Honey Base", "amount_mg": 4000, "standardization": "Pure Forest Flora"}
        ],
        "dosage": "1 sachet dissolved in 100ml warm water, sip slowly twice daily, followed by warm water or fennel tea",
        "contraindications": [
            "Severe uncontrolled hypertension (due to licorice mineralocorticoid activity in excessive doses)",
            "Uncontrolled diabetes (requires Safoof dry form alternative)",
            "Hypokalemia"
        ],
        "monitoring": ["Peak Expiratory Flow Rate (PEFR)", "Symptom frequency diary"],
        "citations": ["Pulmonary Pharmacology & Therapeutics 2021; Glycyrrhizin anti-inflammatory in airway hyperresponsiveness"]
    },
    "ZAY-007": {
        "sku": "ZAY-007",
        "name": "JointFree™",
        "unani_name": "Safoof-e-Muhallil-e-Mafasil",
        "formulation_type": "Micro-Granules (30 x 5g Daily Stick Sachets)",
        "regulatory_track": "AYUSH_PROPRIETARY",
        "is_prescription_required": False,
        "mrp_inr": 1650,
        "organ_axis": "MUSCULOSKELETAL",
        "primary_indication": "Waja-ul-Mafasil (Osteoarthritis, Rheumatoid stiffness, Joint inflammation, Cartilage degradation)",
        "composition": [
            {"ingredient": "Suranjan Shirin (Colchicum autumnale - purified)", "amount_mg": 150, "standardization": "Colchicine < 0.2%"},
            {"ingredient": "Asgandh (Withania somnifera)", "amount_mg": 300, "standardization": "Withanolides 5.0%"},
            {"ingredient": "Zanjabil (Zingiber officinale)", "amount_mg": 200, "standardization": "Gingerols 5%"},
            {"ingredient": "Kundur (Boswellia serrata)", "amount_mg": 250, "standardization": "AKBA (3-O-acetyl-11-keto-beta-boswellic acid) 30%"},
            {"ingredient": "Filfil Daraz (Piper longum)", "amount_mg": 100, "standardization": "Piperine 95%"}
        ],
        "dosage": "1 stick sachet (5g) twice daily with warm milk or lukewarm water after breakfast and dinner",
        "contraindications": [
            "Severe renal impairment (eGFR < 30 mL/min)",
            "Pregnancy & lactation",
            "Severe diarrhea or acute gastroenteritis"
        ],
        "monitoring": ["ESR, CRP", "WOMAC Osteoarthritis score", "Serum Creatinine"],
        "citations": ["Arthritis & Rheumatism 2014; Boswellia serrata AKBA in knee osteoarthritis"]
    },
    "ZAY-008": {
        "sku": "ZAY-008",
        "name": "MindBalance™",
        "unani_name": "Majoon-e-Mufarrih-e-Arwah",
        "formulation_type": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)",
        "regulatory_track": "AYUSH_CLASSICAL",
        "is_prescription_required": False,
        "mrp_inr": 1750,
        "organ_axis": "NEUROPSYCHIATRIC",
        "primary_indication": "Malikhuliya (Anxiety, Neurosis, Chronic Cortisol Dysregulation, Mental Burnout, Cognitive Fatigue)",
        "composition": [
            {"ingredient": "Brahmi (Bacopa monnieri)", "amount_mg": 350, "standardization": "Bacosides A & B 20%"},
            {"ingredient": "Shankhpushpi (Convolvulus pluricaulis)", "amount_mg": 300, "standardization": "Total Alkaloids 2.5%"},
            {"ingredient": "Ustukhuddus (Lavandula stoechas)", "amount_mg": 200, "standardization": "Linalool 3.5%"},
            {"ingredient": "Gaozaban (Borago officinalis)", "amount_mg": 150, "standardization": "Flavonoids 2%"},
            {"ingredient": "Badranjboya (Melissa officinalis)", "amount_mg": 150, "standardization": "Rosmarinic acid 5%"},
            {"ingredient": "Jadwar (Delphinium denudatum)", "amount_mg": 50, "standardization": "Denudatine alkaloids 1%"}
        ],
        "dosage": "1 to 2 capsules twice daily (in the morning and 1 hour before sleep) with warm milk",
        "contraindications": [
            "Concomitant MAO-inhibitor therapy without clinical taper",
            "Severe bipolar mania",
            "Heavy daytime machinery operation until tolerance established"
        ],
        "monitoring": ["GAD-7 Anxiety Scale", "Sleep quality score", "Cortisol diurnal curve where indicated"],
        "citations": ["Neuropsychopharmacology 2018; Bacopa monnieri synaptic plasticity"]
    },

    # -------------------------------------------------------------------------
    # SECTION B: ZAYVORA BRAND FORMULATIONS
    # -------------------------------------------------------------------------
    "ZAY-009": {
        "sku": "ZAY-009",
        "name": "Night-One X™",
        "unani_name": "Qurs-e-Taqwiyat-e-Quwwat-e-Baah",
        "formulation_type": "Habb / Coated Micro-Tablets (60 Tabs)",
        "regulatory_track": "AYUSH_SCHEDULE_E1_RX",
        "is_prescription_required": True,
        "mrp_inr": 3400,
        "organ_axis": "ANDROLOGICAL",
        "primary_indication": "Severe Neuro-Vascular Erectile Dysfunction (Zof-e-Baah Shadeed), Loss of Penile Tumescence",
        "composition": [
            {"ingredient": "Zafran (Crocus sativus)", "amount_mg": 30, "standardization": "Crocin 3%"},
            {"ingredient": "Jund Bedastar (Castoreum)", "amount_mg": 50, "standardization": "Purified Castorin Complex"},
            {"ingredient": "Regmahi (Scincus officinalis)", "amount_mg": 50, "standardization": "Calcified Bio-Peptides"},
            {"ingredient": "Kuchla Mudabbar (Purified Strychnos nux-vomica)", "amount_mg": 15, "standardization": "Strychnine 1.15%"},
            {"ingredient": "Salab Misri (Orchis mascula)", "amount_mg": 300, "standardization": "Glucomannan 15%"},
            {"ingredient": "Amber (Ambra grisea)", "amount_mg": 10, "standardization": "Ambrein 25%"}
        ],
        "dosage": "1 tablet at night with 250ml warm saffron milk 2 hours after meal (Maximum 3 tablets per week; Rx restricted)",
        "contraindications": [
            "Severe uncontrolled hypertension (>180/110 mmHg)",
            "Concurrent Nitrate therapy (Nitroglycerin, Isosorbide mononitrate)",
            "History of ventricular arrhythmias or recent myocardial infarction (<6 months)",
            "Pediatric age or female usage"
        ],
        "monitoring": ["IIEF-5 Score", "Resting BP & Pulse", "Safety check every 30 days"],
        "citations": ["AYUSH Schedule E-1 Mandatory Monitoring Standard 2021"]
    },
    "ZAY-010": {
        "sku": "ZAY-010",
        "name": "Fertility PRO™",
        "unani_name": "Majoon-e-Taqwiyat-e-Mani-Shadeed",
        "formulation_type": "Majoon / Oral Paste (30 x 10g Sachets)",
        "regulatory_track": "AYUSH_CLASSICAL",
        "is_prescription_required": False,
        "mrp_inr": 3800,
        "organ_axis": "ANDROLOGICAL",
        "primary_indication": "Severe Oligospermia (<10 million/ml), Asthenozoospermia, Teratozoospermia, Semen Viscosity & Volume Deficit",
        "composition": [
            {"ingredient": "Salab Panja (Dactylorhiza hatagirea)", "amount_mg": 300, "standardization": "Mucilaginous Glycoproteins 18%"},
            {"ingredient": "Khulanjan (Alpinia galanga)", "amount_mg": 200, "standardization": "Galangin 3%"},
            {"ingredient": "Behman Surkh (Salvia haematodes)", "amount_mg": 200, "standardization": "Salvianolic Acids 5%"},
            {"ingredient": "Behman Safed (Centaurea behen)", "amount_mg": 200, "standardization": "Total Sterols 2%"},
            {"ingredient": "Maghz-e-Badam (Prunus amygdalus)", "amount_mg": 400, "standardization": "Oleic & Linoleic Essential Lipids"},
            {"ingredient": "Maghz-e-Pista (Pistacia vera)", "amount_mg": 200, "standardization": "Phytosterols & Tocopherols"},
            {"ingredient": "Zafran (Crocus sativus)", "amount_mg": 15, "standardization": "Safranal 2%"},
            {"ingredient": "Kushta Nuqra (Silver Calx)", "amount_mg": 30, "standardization": "Sub-micron Silver Nanoparticles"}
        ],
        "dosage": "1 sachet (10g) in the morning on empty stomach with 250ml full-fat lukewarm milk for 90 days minimum",
        "contraindications": [
            "Non-obstructive Azoospermia with elevated FSH (>30 mIU/mL) - requires genetic karyotyping first",
            "Severe untreated varicocele Grade 3 (requires urological ligation evaluation)"
        ],
        "monitoring": ["Semen Analysis (WHO 6th Edition) at baseline, 60 days, and 90 days", "Serum Testosterone, LH, FSH"],
        "citations": ["Andrologia 2020; Classical Unani spermatogenic formulation in idiopathic oligoasthenozoospermia"]
    },
    "ZAY-011": {
        "sku": "ZAY-011",
        "name": "Men Daily™",
        "unani_name": "Safoof-e-Taqwiyat-e-Umumi-Lil-Rijal",
        "formulation_type": "Standardized Micro-Granules (30 x 3g Sachets)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 1150,
        "organ_axis": "ANDROLOGICAL",
        "primary_indication": "General male vitality, everyday physical endurance, mild fatigue, micronutrient repletion",
        "composition": [
            {"ingredient": "Ashwagandha (Withania somnifera)", "amount_mg": 300, "standardization": "Withanolides 5%"},
            {"ingredient": "Gokshura (Tribulus terrestris)", "amount_mg": 300, "standardization": "Protodioscin 40%"},
            {"ingredient": "Safed Musli (Chlorophytum borivilianum)", "amount_mg": 200, "standardization": "Saponins 20%"},
            {"ingredient": "Shatavari (Asparagus racemosus)", "amount_mg": 200, "standardization": "Shatavarins 10%"},
            {"ingredient": "Shilajit (purified asphaltum)", "amount_mg": 150, "standardization": "Fulvic Acid 60%"},
            {"ingredient": "Akarkara (Anacyclus pyrethrum)", "amount_mg": 100, "standardization": "Pellitorine 1.5%"}
        ],
        "dosage": "1 sachet (3g) daily in the morning with warm water or milk",
        "contraindications": ["None reported at recommended dietary levels"],
        "monitoring": ["Energy visual analogue scale", "Annual biochemistry"],
        "citations": ["Journal of the International Society of Sports Nutrition 2015; Withania somnifera ergogenic outcomes"]
    },
    "ZAY-012": {
        "sku": "ZAY-012",
        "name": "Sleep+Stress™",
        "unani_name": "Safoof-e-Taskeen-e-Dimagh",
        "formulation_type": "Herbal Infusion / Decoction Elixir (200ml Bottle)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 1250,
        "organ_axis": "NEUROPSYCHIATRIC",
        "primary_indication": "Sahar (Insomnia), Disrupted sleep architecture, Elevated evening cortisol, Nocturnal restlessness",
        "composition": [
            {"ingredient": "Ashwagandha (Withania somnifera)", "amount_mg": 400, "standardization": "Withanolides 5% (high withanolide-A)"},
            {"ingredient": "Tagar (Valeriana wallichii)", "amount_mg": 300, "standardization": "Valerenic Acids 0.8%"},
            {"ingredient": "Jatamansi (Nardostachys jatamansi)", "amount_mg": 250, "standardization": "Jatamansone 2%"},
            {"ingredient": "Chamomile Extract", "amount_mg": 150, "standardization": "Apigenin 1.2%"},
            {"ingredient": "Tukhm-e-Khashkhash (Poppy seeds - purified)", "amount_mg": 200, "standardization": "Nutritional Lipid & Tryptophan Matrix"}
        ],
        "dosage": "10ml to 15ml with warm milk or chamomile infusion 45 minutes before bedtime",
        "contraindications": [
            "Concurrent use with high-dose benzodiazepines or z-drugs without doctor taper",
            "Sleep apnea requiring nocturnal CPAP (must continue CPAP)"
        ],
        "monitoring": ["Pittsburgh Sleep Quality Index (PSQI)", "Morning alertness score"],
        "citations": ["Sleep Medicine 2021; Valeriana wallichii and Withania in primary insomnia"]
    },
    "ZAY-013": {
        "sku": "ZAY-013",
        "name": "Fertility Moderate™",
        "unani_name": "Safoof-e-Muwalid-e-Mani-Mutawassit",
        "formulation_type": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 1850,
        "organ_axis": "ANDROLOGICAL",
        "primary_indication": "Moderate Oligospermia (10-15 million/ml), Decreased seminal volume, Semen liquefaction delay",
        "composition": [
            {"ingredient": "Safed Musli (Chlorophytum borivilianum)", "amount_mg": 350, "standardization": "Saponins 25%"},
            {"ingredient": "Kaunch Beej (Mucuna pruriens)", "amount_mg": 300, "standardization": "L-Dopa 10%"},
            {"ingredient": "Talmakhana (Asteracantha longifolia)", "amount_mg": 250, "standardization": "Mucilaginous Sterols 5%"},
            {"ingredient": "Tukhm-e-Utangan (Blepharis edulis)", "amount_mg": 200, "standardization": "Total Glycosides 4%"},
            {"ingredient": "Gond Katira (Astragalus gummifer)", "amount_mg": 150, "standardization": "Tragacanthin Polysaccharide"}
        ],
        "dosage": "1 to 2 capsules twice daily with warm milk",
        "contraindications": ["None major; avoid in severe acute prostatitis until resolved"],
        "monitoring": ["Semen analysis at 60 days"],
        "citations": ["Fertility and Sterility 2011; Mucuna pruriens improves male fertility"]
    },
    "ZAY-014": {
        "sku": "ZAY-014",
        "name": "HairRoot-X™",
        "unani_name": "Safoof-e-Munbit-e-Sha'r",
        "formulation_type": "Micro-Granules (30 x 5g Daily Stick Sachets)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 1100,
        "organ_axis": "DERMATOLOGICAL",
        "primary_indication": "Intisaar-ush-Sha'r (Hair thinning, Telogen Effluvium, Early Greying, Scalp follicular weakness)",
        "composition": [
            {"ingredient": "Amla (Emblica officinalis)", "amount_mg": 400, "standardization": "Tannins 30%, Vitamin C natural"},
            {"ingredient": "Bhringraj (Eclipta alba)", "amount_mg": 350, "standardization": "Wedelolactone 2%"},
            {"ingredient": "Shikakai (Acacia concinna)", "amount_mg": 150, "standardization": "Saponins 15%"},
            {"ingredient": "Halela Siyah (Terminalia chebula)", "amount_mg": 150, "standardization": "Polyphenols 20%"},
            {"ingredient": "Tukhm-e-Kahu (Lactuca sativa seeds)", "amount_mg": 100, "standardization": "Lactucin & Flavonoids"}
        ],
        "dosage": "1 stick sachet (5g) daily in the morning with water; optionally paired with topical Roghan Baiza-e-Murgh",
        "contraindications": ["None reported"],
        "monitoring": ["Hair pull test", "Trichoscopy / Follicular density"],
        "citations": ["Archives of Dermatological Research 2019; Eclipta alba follicular stimulation"]
    },
    "ZAY-015": {
        "sku": "ZAY-015",
        "name": "UroClear™",
        "unani_name": "Safoof-e-Mufattit-e-Hisat",
        "formulation_type": "Targeted Micro-Granules (30 x 5g Daily Sachets)",
        "regulatory_track": "AYUSH_PROPRIETARY",
        "is_prescription_required": False,
        "mrp_inr": 1350,
        "organ_axis": "UROLOGICAL",
        "primary_indication": "Hisat-e-Kulya wa Masana (Kidney and bladder calculi <8mm), Crystalluria, Burning micturition (Sozish-e-Baul)",
        "composition": [
            {"ingredient": "Kulthi (Macrotyloma uniflorum)", "amount_mg": 400, "standardization": "Phytic Acid & Flavonoids 5%"},
            {"ingredient": "Gokshura (Tribulus terrestris)", "amount_mg": 350, "standardization": "Saponins 40%"},
            {"ingredient": "Pashanbhed (Bergenia ligulata)", "amount_mg": 300, "standardization": "Bergenin 8%"},
            {"ingredient": "Hajr-ul-Yahood Bhasma (Lapis judaicus)", "amount_mg": 150, "standardization": "Natural Calcium Silicate complex"},
            {"ingredient": "Javakhar (Potassium carbonate from barley ash)", "amount_mg": 100, "standardization": "Potassium Carbonate 80%"}
        ],
        "dosage": "1 stick sachet (5g) twice daily dissolved in a full glass of water (maintain minimum 3 liters daily fluid intake)",
        "contraindications": [
            "Obstructive uropathy with hydronephrosis",
            "Stone diameter > 9mm (requires urological intervention)",
            "Renal failure (eGFR < 30 mL/min)"
        ],
        "monitoring": ["NCCT KUB or USG KUB at 30 and 60 days", "Urine routine/microscopy for crystals"],
        "citations": ["Urological Research 2018; Bergenia ligulata and Macrotyloma in calcium oxalate dissolution"]
    },
    "ZAY-016": {
        "sku": "ZAY-016",
        "name": "FemCare-L™",
        "unani_name": "Safoof-e-Qabiz-e-Reham",
        "formulation_type": "Micro-Calcified Tablets (60 Tabs)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 1150,
        "organ_axis": "GYNECOLOGICAL",
        "primary_indication": "Sailan-ur-Reham (Non-infective Leucorrhoea, Vaginal Discharge, Pelvic Congestion)",
        "composition": [
            {"ingredient": "Lodhra (Symplocos racemosa)", "amount_mg": 350, "standardization": "Total Alkaloids (Loturine) 1.5%"},
            {"ingredient": "Mochras (Bombax ceiba gum)", "amount_mg": 300, "standardization": "Tannins & Mucilage 20%"},
            {"ingredient": "Ashok Chhal (Saraca asoca)", "amount_mg": 350, "standardization": "Catechin & Tannins 10%"},
            {"ingredient": "Gond Dhak (Butea monosperma gum)", "amount_mg": 150, "standardization": "Butein & Tannic Acid 15%"},
            {"ingredient": "Phitkari Biryan (Purified roasted alum)", "amount_mg": 50, "standardization": "Purified Potash Alum"}
        ],
        "dosage": "1 to 2 tablets twice daily with rice water (Maa-ul-Arz) or lukewarm water after meals",
        "contraindications": [
            "Trichomoniasis or bacterial vaginosis requiring immediate antimicrobial therapy",
            "Suspected cervical intraepithelial neoplasia (CIN) without Pap smear",
            "Pregnancy first trimester"
        ],
        "monitoring": ["Discharge characteristics", "Pelvic examination if chronic"],
        "citations": ["Journal of Pharmacognosy and Phytochemistry 2017; Symplocos racemosa gynecological utility"]
    },
    "ZAY-017": {
        "sku": "ZAY-017",
        "name": "MetaboBurn-M™",
        "unani_name": "Safoof-e-Tahleel-e-Shahm",
        "formulation_type": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 1450,
        "organ_axis": "METABOLIC",
        "primary_indication": "Shahm-e-Mufrit (Central Obesity, Slow Basal Metabolic Rate, Visceral Adipose Tissue Excess)",
        "composition": [
            {"ingredient": "Garcinia cambogia", "amount_mg": 350, "standardization": "Hydroxycitric Acid (HCA) 60%"},
            {"ingredient": "Green Coffee Bean", "amount_mg": 250, "standardization": "Chlorogenic Acid (CGA) 50%"},
            {"ingredient": "Zeera Siyah (Carum carvi)", "amount_mg": 200, "standardization": "Carvone 3%"},
            {"ingredient": "Ajwain (Trachyspermum ammi)", "amount_mg": 200, "standardization": "Thymol 2.5%"},
            {"ingredient": "Filfil Siyah (Piper nigrum)", "amount_mg": 100, "standardization": "Piperine 95%"}
        ],
        "dosage": "1 to 2 capsules twice daily 30 minutes before major meals with warm water",
        "contraindications": [
            "Anorexia nervosa or underweight status (BMI < 18.5)",
            "Pregnancy & lactation",
            "Severe gastritis / peptic ulcer"
        ],
        "monitoring": ["Waist circumference", "Body Mass Index (BMI)", "Visceral fat score"],
        "citations": ["Obesity Reviews 2016; Hydroxycitric acid and chlorogenic acid in lipid metabolism"]
    },
    "ZAY-018": {
        "sku": "ZAY-018",
        "name": "ThyroMet-W™",
        "unani_name": "Safoof-e-Islah-e-Ghudda-e-Darqiya",
        "formulation_type": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 1550,
        "organ_axis": "ENDOCRINE",
        "primary_indication": "Ghudda-e-Darqiya sluggishness (Subclinical Hypothyroidism, Cold intolerance, Myxedematous sluggishness)",
        "composition": [
            {"ingredient": "Kanchnar Chhal (Bauhinia variegata)", "amount_mg": 400, "standardization": "Flavonoids 5%"},
            {"ingredient": "Guggulu (Commiphora mukul)", "amount_mg": 300, "standardization": "Guggulsterones 2.5%"},
            {"ingredient": "Triphala (Terminalia chebula, bellerica, Emblica officinalis)", "amount_mg": 250, "standardization": "Tannins 35%"},
            {"ingredient": "Trikatu (Zingiber, Piper nigrum, Piper longum)", "amount_mg": 150, "standardization": "Piperine & Gingerols 10%"},
            {"ingredient": "Varuna (Crataeva nurvala)", "amount_mg": 150, "standardization": "Lupeol 1.5%"}
        ],
        "dosage": "1 to 2 capsules twice daily with warm ginger infusion or lukewarm water",
        "contraindications": [
            "Overt Hyperthyroidism / Thyrotoxicosis",
            "Autoimmune Graves disease",
            "Pregnancy"
        ],
        "monitoring": ["Serum TSH, Free T3, Free T4 every 60-90 days"],
        "citations": ["Phytomedicine 2018; Guggulu regulation of thyroidal hormone synthesis"]
    },
    "ZAY-019": {
        "sku": "ZAY-019",
        "name": "Women Daily™",
        "unani_name": "Safoof-e-Nisa",
        "formulation_type": "Compressed Tablets (60 Tabs)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 1150,
        "organ_axis": "GYNECOLOGICAL",
        "primary_indication": "General female vitality, nutritional anemia, premenstrual fatigue, hormonal equilibrium",
        "composition": [
            {"ingredient": "Shatavari (Asparagus racemosus)", "amount_mg": 400, "standardization": "Shatavarins 10%"},
            {"ingredient": "Ashok Chhal (Saraca asoca)", "amount_mg": 300, "standardization": "Tannins 10%"},
            {"ingredient": "Lodhra (Symplocos racemosa)", "amount_mg": 250, "standardization": "Loturine 1.5%"},
            {"ingredient": "Giloy (Tinospora cordifolia)", "amount_mg": 200, "standardization": "Bitters 3%"},
            {"ingredient": "Iron Bhasma (Kushta Khabs-ul-Hadeed)", "amount_mg": 50, "standardization": "Micro-calcified Elemental Iron"}
        ],
        "dosage": "1 to 2 tablets daily in the morning with milk or warm water",
        "contraindications": ["Hemochromatosis (iron overload)"],
        "monitoring": ["Hemoglobin & Ferritin", "Menstrual regularity diary"],
        "citations": ["Journal of Herbal Medicine 2020; Asparagus racemosus in female endocrine homeostasis"]
    },
    "ZAY-020": {
        "sku": "ZAY-020",
        "name": "Sugar Care™",
        "unani_name": "Safoof-e-Daf-e-Ziabetus-Mutawassit",
        "formulation_type": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 1250,
        "organ_axis": "PANCREATIC",
        "primary_indication": "Prediabetes (HbA1c 5.7–6.4%), Impaired fasting glucose, Postprandial glucose surges",
        "composition": [
            {"ingredient": "Vijaysar (Pterocarpus marsupium)", "amount_mg": 350, "standardization": "Marsupsin & Pterosupin 5%"},
            {"ingredient": "Gurmar (Gymnema sylvestre)", "amount_mg": 300, "standardization": "Gymnemic acids 25%"},
            {"ingredient": "Methi (Trigonella foenum-graecum)", "amount_mg": 250, "standardization": "Galactomannan 30%"},
            {"ingredient": "Jamun (Syzygium cumini)", "amount_mg": 200, "standardization": "Jamboline 10%"},
            {"ingredient": "Dalchini (Cinnamomum verum)", "amount_mg": 150, "standardization": "Polyphenols 10%"}
        ],
        "dosage": "1 to 2 capsules twice daily 15 minutes before lunch and dinner with water",
        "contraindications": ["None major; monitor glucose when combined with prescription oral hypoglycemics"],
        "monitoring": ["Fasting blood glucose, HbA1c at 90 days"],
        "citations": ["Diabetes Care 2017; Pterocarpus marsupium in glycemic moderation"]
    },
    "ZAY-021": {
        "sku": "ZAY-021",
        "name": "Immunity™",
        "unani_name": "Safoof-e-Muqawwi-e-Tabiyat",
        "formulation_type": "Purified Herbal Granules (30 x 3g Sachets)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 950,
        "organ_axis": "IMMUNOLOGICAL",
        "primary_indication": "Tabiyat Mudabbira-e-Badan enhancer, Recurrent seasonal infections, Post-infectious asthenia",
        "composition": [
            {"ingredient": "Giloy (Tinospora cordifolia)", "amount_mg": 400, "standardization": "Tinosporaside & Cordifolioside 3%"},
            {"ingredient": "Tulsi (Ocimum sanctum)", "amount_mg": 250, "standardization": "Ursolic acid 2.5%"},
            {"ingredient": "Kalmegh (Andrographis paniculata)", "amount_mg": 200, "standardization": "Andrographolide 10%"},
            {"ingredient": "Amla (Emblica officinalis)", "amount_mg": 300, "standardization": "Vitamin C & Tannins 30%"},
            {"ingredient": "Haldi (Curcuma longa)", "amount_mg": 150, "standardization": "Curcuminoids 95%"},
            {"ingredient": "Filfil Siyah (Piper nigrum - Bio-enhancer Mu'in)", "amount_mg": 20, "standardization": "Piperine 95%"}
        ],
        "dosage": "1 sachet (3g) once or twice daily dissolved in warm water or green tea",
        "contraindications": ["Autoimmune flare states (active multiple sclerosis) without specialist review"],
        "monitoring": ["Absolute lymphocyte count", "Infection incidence log"],
        "citations": ["Frontiers in Pharmacology 2021; Tinospora cordifolia immunomodulatory cascades"]
    },
    "ZAY-022": {
        "sku": "ZAY-022",
        "name": "GutEase-IBS™",
        "unani_name": "Safoof-e-Islah-e-Amaa",
        "formulation_type": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 1150,
        "organ_axis": "GASTROINTESTINAL",
        "primary_indication": "Zalaq-ul-Amaa / Nafkh-e-Shikam (Irritable Bowel Syndrome, Gut Dysbiosis, Postprandial Cramping & Flatulence)",
        "composition": [
            {"ingredient": "Bilva (Aegle marmelos)", "amount_mg": 400, "standardization": "Marmelosin & Tannins 10%"},
            {"ingredient": "Ispaghul Husk (Plantago ovata)", "amount_mg": 350, "standardization": "Soluble dietary fiber 85%"},
            {"ingredient": "Saunf (Foeniculum vulgare)", "amount_mg": 200, "standardization": "Anethole 2%"},
            {"ingredient": "Pudina (Mentha piperita)", "amount_mg": 150, "standardization": "Menthol 1.5%"},
            {"ingredient": "Zeera Safed (Cuminum cyminum)", "amount_mg": 150, "standardization": "Cuminaldehyde 2%"}
        ],
        "dosage": "1 to 2 capsules twice daily 20 minutes after food with fresh buttermilk or water",
        "contraindications": ["Acute bowel obstruction", "Appendicitis symptoms", "Fecal impaction"],
        "monitoring": ["Bristol Stool Form Scale", "Abdominal pain visual analogue score"],
        "citations": ["Digestive Diseases and Sciences 2019; Aegle marmelos in irritable bowel syndrome"]
    },

    # -------------------------------------------------------------------------
    # SECTION C: POSHIDA AMRAZ (Rx ONLY & SPECIALIST CONTROLLED)
    # -------------------------------------------------------------------------
    "ZAY-023": {
        "sku": "ZAY-023",
        "name": "NeuroVigor-Rx™",
        "unani_name": "Habb-e-Azaraqi Mudabbar (Majoon-e-Muhrik-e-Baah)",
        "formulation_type": "Coated Micro-Tablets (Alu-Alu Blister, 60 Tabs)",
        "regulatory_track": "AYUSH_SCHEDULE_E1_RX",
        "is_prescription_required": True,
        "mrp_inr": 1850,
        "organ_axis": "ANDROLOGICAL",
        "primary_indication": "Refractory Erectile Dysfunction, Severe Loss of Libido, Chronic Neuro-vascular Impotence",
        "composition": [
            {"ingredient": "Zafran (Crocus sativus)", "amount_mg": 35, "standardization": "Crocin 3%"},
            {"ingredient": "Kuchla Mudabbar (Purified Nux-vomica)", "amount_mg": 20, "standardization": "Strychnine 1.15%"},
            {"ingredient": "Salab Panja (Dactylorhiza hatagirea)", "amount_mg": 350, "standardization": "Mucilaginous Glycoproteins 18%"},
            {"ingredient": "Shingraf Mudabbar (Purified Cinnabar)", "amount_mg": 15, "standardization": "Traditional detoxified mercuric sulfide compound"},
            {"ingredient": "Darchini (Cinnamomum zeylanicum)", "amount_mg": 100, "standardization": "Cinnamaldehyde 5%"},
            {"ingredient": "Asgandh (Withania somnifera)", "amount_mg": 250, "standardization": "Withanolides 5%"}
        ],
        "dosage": "1 tablet at bedtime with 250ml full-cream milk (Maximum 3 times weekly; strictly requires registered AYUSH practitioner prescription)",
        "contraindications": [
            "Severe cardiovascular disease, unstable angina, heart failure NYHA III/IV",
            "Concurrent phosphodiesterase-5 inhibitors (Sildenafil, Tadalafil) without 24-hr washout",
            "Uncontrolled hypertension (>170/105 mmHg)",
            "Renal or hepatic failure"
        ],
        "monitoring": ["IIEF-15 Score", "Blood Pressure at every refill", "Renal and Liver Function at 60 days"],
        "citations": ["AYUSH Schedule E-1 Mandate; Classical Unani Formulary of India (NFUM)"]
    },
    "ZAY-024": {
        "sku": "ZAY-024",
        "name": "SpermoVora™",
        "unani_name": "Safoof-e-Mujaddid-e-Nutfa-Shadeed",
        "formulation_type": "Single-Serve Paste Sachets (30 x 7g)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 2250,
        "organ_axis": "ANDROLOGICAL",
        "primary_indication": "Severe Oligo-Astheno-Teratozoospermia (OAT Syndrome), Elevated DNA Fragmentation Index (DFI > 25%)",
        "composition": [
            {"ingredient": "Coenzyme Q10", "amount_mg": 200, "standardization": "Pure Ubiquinone 99%"},
            {"ingredient": "L-Carnitine L-Tartrate", "amount_mg": 500, "standardization": "Pure L-Carnitine 68%"},
            {"ingredient": "Lycopene 10%", "amount_mg": 25, "standardization": "Natural Tomato Lycopene Extract"},
            {"ingredient": "Salab Misri (Orchis mascula)", "amount_mg": 350, "standardization": "Glucomannan 15%"},
            {"ingredient": "Safed Musli (Chlorophytum borivilianum)", "amount_mg": 300, "standardization": "Saponins 20%"},
            {"ingredient": "Zinc Monomethionine", "amount_mg": 50, "standardization": "Elemental Zinc 10mg"},
            {"ingredient": "Selenium Yeast", "amount_mg": 40, "standardization": "Elemental Selenium 40mcg"}
        ],
        "dosage": "1 sachet (7g paste) twice daily with milk or fresh pomegranate juice for 90 to 120 days",
        "contraindications": [
            "Hypercalcemia / Hypercalciuria",
            "Severe renal disease"
        ],
        "monitoring": ["Semen Analysis at Day 45 and Day 90", "DNA Fragmentation Index (SCSA/TUNEL)", "ROS Seminal Fluid assay"],
        "citations": ["Human Reproduction Update 2021; Antioxidant therapy in male idiopathic infertility"]
    },
    "ZAY-025": {
        "sku": "ZAY-025",
        "name": "SemenGuard™",
        "unani_name": "Safoof-e-Mumsik-e-Mani-Shadeed",
        "formulation_type": "Micro-Granules (30 x 5g Daily Stick Sachets)",
        "regulatory_track": "AYUSH_PROPRIETARY",
        "is_prescription_required": False,
        "mrp_inr": 1950,
        "organ_axis": "ANDROLOGICAL",
        "primary_indication": "Surat-e-Inzal (Premature Ejaculation, IELT < 1 minute), Riqat-e-Mani (Seminal hyperviscosity/thinness)",
        "composition": [
            {"ingredient": "Tukhm-e-Kahu (Lactuca sativa seeds)", "amount_mg": 250, "standardization": "Lactucopicrin 1.5%"},
            {"ingredient": "Tukhm-e-Khashkhash (Purified poppy seeds)", "amount_mg": 250, "standardization": "Total Lipids & Alkaloids"},
            {"ingredient": "Gond Kikar (Acacia arabica gum)", "amount_mg": 300, "standardization": "Arabinogalactan 35%"},
            {"ingredient": "Mochras (Bombax ceiba gum)", "amount_mg": 200, "standardization": "Tannins 20%"},
            {"ingredient": "Kushta Qalai (Tin calx)", "amount_mg": 50, "standardization": "Purified Stannic Oxide complex"}
        ],
        "dosage": "1 stick sachet (5g) twice daily with lukewarm milk 1 hour before sleep",
        "contraindications": ["None major; avoid combining with heavy CNS depressants"],
        "monitoring": ["Intravaginal Ejaculatory Latency Time (IELT)", "Premature Ejaculation Diagnostic Tool (PEDT)"],
        "citations": ["Journal of Sexual Medicine 2019; Herbal neuro-modulators in premature ejaculation"]
    },
    "ZAY-026": {
        "sku": "ZAY-026",
        "name": "ProstaGuard™",
        "unani_name": "Safoof-e-Mulayyim-e-Ghudda-e-Baristeht",
        "formulation_type": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 1850,
        "organ_axis": "UROLOGICAL",
        "primary_indication": "Waram-e-Ghudda-e-Baristeht (Benign Prostatic Hyperplasia - BPH Grade 1 & 2, Nocturia, Urinary Hesitancy)",
        "composition": [
            {"ingredient": "Saw Palmetto Extract (Serenoa repens)", "amount_mg": 320, "standardization": "Fatty Acids 45%"},
            {"ingredient": "Nettle Root (Urtica dioica)", "amount_mg": 250, "standardization": "Beta-Sitosterol 0.8%"},
            {"ingredient": "Gokshura (Tribulus terrestris)", "amount_mg": 300, "standardization": "Saponins 40%"},
            {"ingredient": "Varuna (Crataeva nurvala)", "amount_mg": 250, "standardization": "Lupeol 1.5%"},
            {"ingredient": "Pumpkin Seed Extract (Cucurbita pepo)", "amount_mg": 200, "standardization": "Phytosterols 20%"}
        ],
        "dosage": "1 to 2 capsules twice daily after meals with water",
        "contraindications": [
            "Prostate Cancer (mandatory PSA check prior to therapy)",
            "Acute urinary retention requiring Foley catheterization"
        ],
        "monitoring": ["Serum PSA (Prostate Specific Antigen)", "IPSS (International Prostate Symptom Score)", "Post-void residual volume (PVR)"],
        "citations": ["Cochrane Database of Systematic Reviews; Serenoa repens and Urtica dioica in benign prostatic hyperplasia"]
    },
    "ZAY-027": {
        "sku": "ZAY-027",
        "name": "TestoVital Classic™",
        "unani_name": "Majoon-e-Muqawwi-e-Khusyatain",
        "formulation_type": "Targeted HPMC Veg Capsules (60 Caps)",
        "regulatory_track": "AYUSH_CLASSICAL",
        "is_prescription_required": False,
        "mrp_inr": 3600,
        "organ_axis": "ANDROLOGICAL",
        "primary_indication": "Late-onset Hypogonadism, Andropause, Sarcopenia, Testicular Axis Fatigue, Low Free Testosterone",
        "composition": [
            {"ingredient": "Salab Gatta (Orchis latifolia)", "amount_mg": 300, "standardization": "Bioactive Mucilage 20%"},
            {"ingredient": "Khusyat-us-Salab (Testicular Bio-Extract)", "amount_mg": 250, "standardization": "Standardized Peptide Fraction"},
            {"ingredient": "Zafran (Crocus sativus)", "amount_mg": 20, "standardization": "Crocin 3%"},
            {"ingredient": "Asgandh (Withania somnifera)", "amount_mg": 300, "standardization": "Withanolides 5%"},
            {"ingredient": "Kushta Nuqra (Silver calx)", "amount_mg": 30, "standardization": "Sub-micron Silver Particles"},
            {"ingredient": "Maghz-e-Chilgoza (Pinus gerardiana)", "amount_mg": 250, "standardization": "Pinolenic Acid 15%"}
        ],
        "dosage": "1 to 2 capsules in the morning on empty stomach with warm milk",
        "contraindications": [
            "Active or suspected prostate carcinoma",
            "Severe sleep apnea",
            "Polycythemia (Hematocrit > 52%)"
        ],
        "monitoring": ["Total and Free Testosterone", "PSA", "Hematocrit at baseline and 90 days"],
        "citations": ["American Journal of Men's Health 2021; Withania somnifera and orchid extracts in male endocrine renewal"]
    },
    "ZAY-028": {
        "sku": "ZAY-028",
        "name": "LeucoClear™",
        "unani_name": "Safoof-e-Daf-e-Sailan-ur-Reham-Shadeed",
        "formulation_type": "Micro-Granules (30 x 3g Daily Stick Sachets)",
        "regulatory_track": "AYUSH_PROPRIETARY",
        "is_prescription_required": False,
        "mrp_inr": 1650,
        "organ_axis": "GYNECOLOGICAL",
        "primary_indication": "Intractable Chronic Leucorrhoea, Cervical Erosion, Sacral backache associated with vaginal discharge",
        "composition": [
            {"ingredient": "Lodhra (Symplocos racemosa)", "amount_mg": 400, "standardization": "Loturine 1.5%"},
            {"ingredient": "Ashok Chhal (Saraca asoca)", "amount_mg": 350, "standardization": "Tannins 10%"},
            {"ingredient": "Mochras (Bombax ceiba gum)", "amount_mg": 300, "standardization": "Tannins & Mucilage 20%"},
            {"ingredient": "Kushta Baiza-e-Murgh", "amount_mg": 100, "standardization": "Egg Shell Micro-Calcified Calcium"},
            {"ingredient": "Phitkari Biryan (Roasted alum)", "amount_mg": 100, "standardization": "Purified Potash Alum"}
        ],
        "dosage": "1 stick sachet (3g) twice daily with rice water (Maa-ul-Arz) 30 minutes before meals",
        "contraindications": ["Undiagnosed irregular genital bleeding", "Malignancy of genital tract"],
        "monitoring": ["Discharge culture and sensitivity if foul smelling", "Speculum exam"],
        "citations": ["AYUSH Clinical Protocols on Sailan-ur-Reham"]
    },
    "ZAY-029": {
        "sku": "ZAY-029",
        "name": "CycloCare-PCOS™",
        "unani_name": "Safoof-e-Munazzim-e-Haiz",
        "formulation_type": "Micro-Granules (30 x 5g Daily Stick Sachets)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 2400,
        "organ_axis": "GYNECOLOGICAL",
        "primary_indication": "Ehtebas-e-Tams / Marz-e-Keesa-tul-Khusyatur-Reham (PCOS/PCOD, Anovulatory Cycles, Hyperandrogenism, Insulin Resistance)",
        "composition": [
            {"ingredient": "Myo-Inositol", "amount_mg": 2000, "standardization": "Pure USP Grade (40:1 ratio match)"},
            {"ingredient": "D-Chiro-Inositol", "amount_mg": 50, "standardization": "Pure USP Grade (40:1 ratio match)"},
            {"ingredient": "Kanchnar Chhal (Bauhinia variegata)", "amount_mg": 350, "standardization": "Flavonoids 5%"},
            {"ingredient": "Methi (Trigonella foenum-graecum)", "amount_mg": 300, "standardization": "4-Hydroxyisoleucine 20%"},
            {"ingredient": "Haldi (Curcuma longa)", "amount_mg": 200, "standardization": "Curcuminoids 95%"},
            {"ingredient": "Dalchini (Cinnamomum verum)", "amount_mg": 150, "standardization": "Polyphenols 10%"},
            {"ingredient": "Filfil Siyah (Piper nigrum - Bio-enhancer Mu'in)", "amount_mg": 15, "standardization": "Piperine 95%"}
        ],
        "dosage": "1 stick sachet (5g) twice daily dissolved in 150ml water 20 minutes before meals for 3 to 6 consecutive cycles",
        "contraindications": [
            "Pregnancy (once conception confirmed, switch to prenatal protocol)",
            "Active ovarian cyst torsion requiring surgery"
        ],
        "monitoring": ["Pelvic USG (antral follicle count, ovarian volume)", "LH:FSH ratio", "Free Testosterone", "Fasting Insulin"],
        "citations": ["European Review for Medical and Pharmacological Sciences; Myo-inositol + D-chiro-inositol in PCOS"]
    },
    "ZAY-030": {
        "sku": "ZAY-030",
        "name": "UterTone™",
        "unani_name": "Majoon-e-Muqawwi-e-Reham-Shadeed",
        "formulation_type": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 1850,
        "organ_axis": "GYNECOLOGICAL",
        "primary_indication": "Zof-e-Reham (Uterine Atony, Pelvic Floor Laxity, Dysmenorrhea, Luteal Phase Inadequacy)",
        "composition": [
            {"ingredient": "Ashok Chhal (Saraca asoca)", "amount_mg": 400, "standardization": "Catechins 10%"},
            {"ingredient": "Shatavari (Asparagus racemosus)", "amount_mg": 350, "standardization": "Shatavarins 10%"},
            {"ingredient": "Supari Mudabbar (Purified Areca catechu)", "amount_mg": 150, "standardization": "Arecoline detoxified <0.05%"},
            {"ingredient": "Gond Katira (Astragalus gummifer)", "amount_mg": 200, "standardization": "Tragacanthin 40%"},
            {"ingredient": "Asl-us-Soos (Glycyrrhiza glabra)", "amount_mg": 150, "standardization": "Glycyrrhizin 10%"}
        ],
        "dosage": "1 to 2 capsules twice daily with warm milk",
        "contraindications": ["Acute active heavy bleeding (menorrhagia) during menstruation (pause during peak flow)"],
        "monitoring": ["Menstrual duration and pain visual analog score"],
        "citations": ["International Journal of Pharmaceutical Sciences and Research 2018; Saraca asoca uterine tonicity"]
    },
    "ZAY-031": {
        "sku": "ZAY-031",
        "name": "MenoPease™",
        "unani_name": "Safoof-e-Daf-e-Araz-e-Yas",
        "formulation_type": "Micro-Granules (30 x 3g Daily Stick Sachets)",
        "regulatory_track": "AYUSH_PROPRIETARY",
        "is_prescription_required": False,
        "mrp_inr": 1750,
        "organ_axis": "GYNECOLOGICAL",
        "primary_indication": "Sinn-e-Yas (Menopausal Syndrome, Vasomotor Hot Flashes, Night Sweats, Mood Swings, Accelerated Bone Demineralization)",
        "composition": [
            {"ingredient": "Shatavari (Asparagus racemosus)", "amount_mg": 400, "standardization": "Shatavarins 10%"},
            {"ingredient": "Black Cohosh (Actaea racemosa extract)", "amount_mg": 100, "standardization": "Triterpene Glycosides 2.5%"},
            {"ingredient": "Shankhpushpi (Convolvulus pluricaulis)", "amount_mg": 300, "standardization": "Total Alkaloids 2.5%"},
            {"ingredient": "Badranjboya (Melissa officinalis)", "amount_mg": 200, "standardization": "Rosmarinic Acid 5%"},
            {"ingredient": "Praval Pishti (Purified Coral Calx)", "amount_mg": 150, "standardization": "Bioactive Calcium & Trace Minerals"}
        ],
        "dosage": "1 stick sachet (3g) twice daily with lukewarm water after breakfast and dinner",
        "contraindications": [
            "Estrogen receptor-positive breast cancer history without oncologist clearance",
            "Severe active hepatic impairment"
        ],
        "monitoring": ["Greene Climacteric Scale", "Bone Mineral Density (DEXA) annually", "Liver enzymes"],
        "citations": ["Maturitas 2020; Actaea racemosa and phytoestrogenic botanicals in vasomotor symptoms"]
    },
    "ZAY-032": {
        "sku": "ZAY-032",
        "name": "FertiliWomen™",
        "unani_name": "Safoof-e-Mualijat-e-Uqr-e-Nisa",
        "formulation_type": "Compressed Tablets (60 Tabs)",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "is_prescription_required": False,
        "mrp_inr": 3800,
        "organ_axis": "GYNECOLOGICAL",
        "primary_indication": "Uqr-e-Nisa (Female Infertility, Diminished Ovarian Reserve, Poor Oocyte Quality, Thin Endometrial Lining)",
        "composition": [
            {"ingredient": "Shatavari (Asparagus racemosus)", "amount_mg": 400, "standardization": "Shatavarins 10%"},
            {"ingredient": "Shivlingi (Bryonia laciniosa seeds)", "amount_mg": 250, "standardization": "Bryonin 2%"},
            {"ingredient": "Putranjiva (Putranjiva roxburghii)", "amount_mg": 250, "standardization": "Total Glycosides 3%"},
            {"ingredient": "Ashok Chhal (Saraca asoca)", "amount_mg": 300, "standardization": "Tannins 10%"},
            {"ingredient": "Coenzyme Q10", "amount_mg": 100, "standardization": "Pure Ubiquinone 99%"},
            {"ingredient": "L-Methylfolate (Active Folate)", "amount_mg": 0.5, "standardization": "Pure Active L-5-MTHF"}
        ],
        "dosage": "1 to 2 tablets twice daily with warm milk starting on Day 5 of menstrual cycle continuously for 90 days",
        "contraindications": [
            "Confirmed pregnancy (pause upon positive hCG, transition to maternal regimen)",
            "Bilateral complete fallopian tube occlusion (tubal factor requires surgical or IVF resolution)"
        ],
        "monitoring": ["Follicular study (Transvaginal USG) for ovulation & endometrial thickness", "Serum Progesterone at Day 21", "AMH"],
        "citations": ["Reproductive BioMedicine Online 2020; CoQ10 and ovarian response in subfertile women"]
    }
}


def get_all_products() -> List[Dict[str, Any]]:
    """Returns list of all 32 products."""
    return list(MASTER_PRODUCTS.values())


def get_product_by_sku(sku: str) -> Optional[Dict[str, Any]]:
    """Finds product by SKU."""
    return MASTER_PRODUCTS.get(sku)


def get_products_by_axis(axis_code: str) -> List[Dict[str, Any]]:
    """Finds all products mapped to a specific organ axis."""
    axis_upper = axis_code.upper()
    return [p for p in MASTER_PRODUCTS.values() if p.get("organ_axis", "").upper() == axis_upper]


def get_rx_products() -> List[Dict[str, Any]]:
    """Returns products that strictly require clinical prescription (AYUSH Schedule E-1)."""
    return [p for p in MASTER_PRODUCTS.values() if p.get("is_prescription_required") is True]


def enrich_master_products_with_seven_pillars():
    """Enriches all 32 Master Products with Badraqa conduit, Chrono posology, and Dietary Parhez."""
    try:
        from services.therapeutic.app.engines.master_nuskha_architect import (
            ORGAN_BADRAQA_CONDUIT_REGISTRY,
            ORGAN_PARHEZ_MATRIX,
            CHRONO_SCHEDULES
        )
        for sku, prod in MASTER_PRODUCTS.items():
            axis = prod.get("organ_axis", "METABOLIC").upper()
            axis_map = {
                "CEREBROVASCULAR": "CEREBROVASCULAR",
                "METABOLIC": "METABOLIC",
                "CARDIOVASCULAR": "CARDIOVASCULAR",
                "HEPATIC": "HEPATO_BILIARY",
                "PULMONARY": "PULMONARY",
                "MUSCULOSKELETAL": "MUSCULOSKELETAL",
                "NEUROPSYCHIATRIC": "NEURO_PSYCHOLOGICAL",
                "REPRODUCTIVE_MALE": "MALE_REPRODUCTIVE",
                "REPRODUCTIVE_FEMALE": "FEMALE_REPRODUCTIVE",
                "DERMATOLOGICAL": "METABOLIC",
                "RENAL": "RENAL_URINARY",
                "GYNECOLOGICAL": "FEMALE_REPRODUCTIVE",
                "ENDOCRINE": "METABOLIC",
                "IMMUNOLOGICAL": "IMMUNOLOGICAL",
                "GASTROINTESTINAL": "GASTROINTESTINAL"
            }
            target_key = axis_map.get(axis, "METABOLIC")
            badraqa = ORGAN_BADRAQA_CONDUIT_REGISTRY.get(target_key, ORGAN_BADRAQA_CONDUIT_REGISTRY["MALE_REPRODUCTIVE"])
            parhez = ORGAN_PARHEZ_MATRIX.get(target_key, ORGAN_PARHEZ_MATRIX["MALE_REPRODUCTIVE"])

            prod["badraqa_vehicle"] = badraqa["primary_conduit"]
            prod["badraqa_action_vector"] = badraqa["action_vector"]
            prod["chrono_timing"] = CHRONO_SCHEDULES["bad_az_ghiza"]["time_window"]
            prod["parhez_prohibited_foods"] = parhez["prohibited_antagonistic"]
            prod["parhez_synergistic_foods"] = parhez["accelerating_synergistic"]
    except Exception:
        pass

enrich_master_products_with_seven_pillars()


COMMERCIAL_UPGRADE_REGISTRY = {
    "ZAY-001": {"name": "TensioCalm™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-002": {"name": "Glucovora™", "form": "Micro-Granules (30 x 5g Daily Stick Sachets)", "hero": True},
    "ZAY-003": {"name": "CardioVora™", "form": "Majoon Granules (30 x 5g Daily Stick Sachets)", "hero": False},
    "ZAY-004": {"name": "LiverPrime™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": True},
    "ZAY-005": {"name": "LipidoVora™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-006": {"name": "PulmoVora™", "form": "Effervescent Micro-Granules (30 Sachets)", "hero": False},
    "ZAY-007": {"name": "SynovoFlex™", "form": "Micro-Granules (30 x 5g Daily Stick Sachets)", "hero": True},
    "ZAY-008": {"name": "NeuroVora™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-009": {"name": "NeuroShield-Rx™", "form": "Habb / Coated Micro-Tablets (60 Tabs)", "hero": False},
    "ZAY-010": {"name": "SpermoPro™", "form": "Majoon / Oral Paste (30 Sachets)", "hero": False},
    "ZAY-011": {"name": "VigorVora™", "form": "Standardized Micro-Granules (30 Sachets)", "hero": False},
    "ZAY-012": {"name": "SomnoVora™", "form": "Herbal Infusion / Decoction Elixir (200ml)", "hero": False},
    "ZAY-013": {"name": "VitalMani™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-014": {"name": "DermaVora-Hair™", "form": "Micro-Granules (30 x 5g Daily Stick Sachets)", "hero": False},
    "ZAY-015": {"name": "LithoVora™", "form": "Targeted Micro-Granules (30 x 5g Daily Sachets)", "hero": False},
    "ZAY-016": {"name": "GynaeVora-L™", "form": "Micro-Calcified Tablets (60 Tabs)", "hero": False},
    "ZAY-017": {"name": "MetaboBurn-M™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-018": {"name": "ThyroMet-W™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-019": {"name": "FemmeDaily™", "form": "Compressed Tablets (60 Tabs)", "hero": False},
    "ZAY-020": {"name": "GlucoBalance™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-021": {"name": "ImmunoVora™", "form": "Purified Herbal Granules (30 Sachets)", "hero": False},
    "ZAY-022": {"name": "GastroVora™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-023": {"name": "NeuroVigor-Rx™", "form": "Coated Micro-Tablets (Alu-Alu Blister, 60 Tabs)", "hero": False, "mrp": 1850},
    "ZAY-024": {"name": "SpermoVora™", "form": "Single-Serve Paste Sachets (30 x 7g)", "hero": False, "mrp": 2250},
    "ZAY-025": {"name": "ManiVital Pro™", "form": "Micro-Granules (30 x 5g Daily Stick Sachets)", "hero": True},
    "ZAY-026": {"name": "ProstaVora™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-027": {"name": "AndroVora™", "form": "Targeted HPMC Veg Capsules (60 Caps)", "hero": False},
    "ZAY-028": {"name": "LeucoVora™", "form": "Micro-Granules (30 x 3g Daily Stick Sachets)", "hero": False},
    "ZAY-029": {"name": "OvaSync-PCOS™", "form": "Micro-Granules (30 x 5g Daily Stick Sachets)", "hero": True},
    "ZAY-030": {"name": "MensoCalm™", "form": "HPMC Veg Capsules (Alu-Alu Blister, 60 Caps)", "hero": False},
    "ZAY-031": {"name": "MenoVora™", "form": "Micro-Granules (30 x 3g Daily Stick Sachets)", "hero": False},
    "ZAY-032": {"name": "ConceiveVora™", "form": "Compressed Tablets (60 Tabs)", "hero": False},
}


def apply_commercial_brand_upgrades():
    """Applies modern coined names, packaging formats, Phase-1 hero designations, and rationalized pricing."""
    for sku, info in COMMERCIAL_UPGRADE_REGISTRY.items():
        if sku in MASTER_PRODUCTS:
            MASTER_PRODUCTS[sku]["name"] = info["name"]
            MASTER_PRODUCTS[sku]["formulation_type"] = info["form"]
            MASTER_PRODUCTS[sku]["is_hero_launch"] = info["hero"]
            if "mrp" in info:
                MASTER_PRODUCTS[sku]["mrp_inr"] = info["mrp"]


apply_commercial_brand_upgrades()

