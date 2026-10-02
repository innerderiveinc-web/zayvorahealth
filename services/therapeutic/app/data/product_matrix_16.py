"""
ZAYVORA Health OS™ - 16 Core Product Matrix & Dual-Track Mapping
Reference: Chapters 31, 32, 33, 38,
ZAYVORA Clinical System — Volume II (2026), Dr. Irfan Ashraf, BUMS.

Establishes:
  1. The 16 Commercial GMP Products across AYUSH Track A & FSSAI Track B.
  2. Direct Parent-Child Mapping linking the 16 Products to the 32 Classical Matab Nuskhas.
  3. The 4-Tier Polypharmacy Architecture (80% Classical Core + 20% Modern Layer).
  4. Packaging, Pricing (MRP), Dose Forms, and Claims Boundaries (Green vs Red Zone).
"""

from typing import Dict, Any, List, Optional

CORE_PRODUCTS_16: Dict[str, Dict[str, Any]] = {
    "ZAY-PROD-01": {
        "product_id": "ZAY-PROD-01",
        "internal_code": "ZV-M-01",
        "name": "Qurs-e-Taqwiyat-e-Mani PRO (ViriMax-M)",
        "clinical_axis": "Male Reproductive Axis",
        "parent_nuskha_code": "MF-01",
        "parent_nuskha_name": "Safoof Muqawwi-e-Khasiya wa Mani",
        "regulatory_track": "AYUSH Track A (Schedule T GMP)",
        "launch_priority": "Priority 1 (Anchor Product)",
        "dosage_form": "60 Vegetarian Capsules",
        "mrp_target_inr": 2500,
        "daily_dose": "2 capsules twice daily with warm full-fat milk after food",
        "classical_core_80": [
            {"ingredient": "Asgandh (Withania somnifera)", "standardisation": "5% Withanolides (KSM-66)", "mg_per_cap": 300},
            {"ingredient": "Salab Misri (Orchis mascula)", "standardisation": "1:1 concentrated extract", "mg_per_cap": 150},
            {"ingredient": "Behman Combination (Safaid + Surkh 1:1)", "standardisation": "4:1 extract", "mg_per_cap": 100},
            {"ingredient": "Tabasheer Purified (Bambusa arundinacea)", "standardisation": "SiO2 >= 85%", "mg_per_cap": 500}
        ],
        "modern_layer_20": [
            {"ingredient": "CoQ10 Ubiquinol", "purpose": "Sperm flagellar mitochondrial ATP", "mg_per_cap": 50},
            {"ingredient": "L-Carnitine Tartrate", "purpose": "Fatty acid beta-oxidation for motility", "mg_per_cap": 250},
            {"ingredient": "Zinc Bisglycinate", "purpose": "Sertoli DNA polymerase cofactor", "mg_per_cap": 15},
            {"ingredient": "Selenium L-Selenomethionine", "purpose": "GPx4 sperm membrane protection", "mcg_per_cap": 100},
            {"ingredient": "Piperine (Filfil Siyah 95%)", "purpose": "Bioavailability enhancer (P-gp/CYP3A4 inhibitor)", "mg_per_cap": 5}
        ],
        "permitted_claim_green_zone": "Traditionally used in Unani medicine to support male vitality, healthy sperm parameters, and reproductive stamina.",
        "prohibited_claim_red_zone": "Cures male infertility or treats azoospermia (Prohibited under DMR Act 1954)."
    },
    "ZAY-PROD-02": {
        "product_id": "ZAY-PROD-02",
        "internal_code": "ZV-M-02",
        "name": "NightOne X (Bah-Catalyst Formula)",
        "clinical_axis": "Male Performance / Neuro-Stress Axis",
        "parent_nuskha_code": "MF-02",
        "parent_nuskha_name": "Nuskha Muharrik-e-Bah wa Mufarrih",
        "regulatory_track": "FSSAI Track B (Nutraceutical)",
        "launch_priority": "Priority 2",
        "dosage_form": "30 Capsules",
        "mrp_target_inr": 1999,
        "daily_dose": "1 capsule 1 hour before sleep or as advised by clinician",
        "classical_core_80": [
            {"ingredient": "Salab Misri extract", "standardisation": "1:1 extract", "mg_per_cap": 150},
            {"ingredient": "Asgandh extract", "standardisation": "5% Withanolides", "mg_per_cap": 200},
            {"ingredient": "Behman Combination (Safaid + Surkh 1:1)", "standardisation": "4:1 extract", "mg_per_cap": 100},
            {"ingredient": "Sandal Safaid + Tabasheer (Thermal Correctors)", "standardisation": "Pure refined", "mg_per_cap": 400}
        ],
        "modern_layer_20": [
            {"ingredient": "Aqarqarha extract (Anacyclus pyrethrum)", "purpose": "Pellitorine eNOS cavernosal activation", "mg_per_cap": 50},
            {"ingredient": "Zinc Bisglycinate", "purpose": "17b-HSD testosterone enzyme cofactor", "mg_per_cap": 10},
            {"ingredient": "Piperine", "purpose": "Alkylamide bioavailability catalyst", "mg_per_cap": 5}
        ],
        "permitted_claim_green_zone": "Nutraceutical formulation supporting male vigor, stamina, and healthy microcirculation.",
        "prohibited_claim_red_zone": "Treats erectile dysfunction or guarantees instant performance."
    },
    "ZAY-PROD-03": {
        "product_id": "ZAY-PROD-03",
        "internal_code": "ZV-F-01",
        "name": "ThyroMet-W (Thyroid-Metabolic)",
        "clinical_axis": "Thyroid-Metabolic Axis",
        "parent_nuskha_code": "TM-01",
        "parent_nuskha_name": "Nuskha Muhallil-e-Balgham Jigar-Darqiya",
        "regulatory_track": "AYUSH Track A (Schedule T GMP)",
        "launch_priority": "Priority 3",
        "dosage_form": "60 Capsules",
        "mrp_target_inr": 2200,
        "daily_dose": "2 capsules daily with food",
        "classical_core_80": [
            {"ingredient": "Guggul Shudh (Commiphora wightii)", "standardisation": "10% Guggulsterones (E+Z)", "mg_per_cap": 300},
            {"ingredient": "Punarnava extract (Boerhavia diffusa)", "standardisation": "2.5% Boeravinones", "mg_per_cap": 200},
            {"ingredient": "Methi seed extract (Trigonella)", "standardisation": "50% 4-Hydroxyisoleucine", "mg_per_cap": 200},
            {"ingredient": "Tabasheer + Amla Musleh", "standardisation": "Mandatory thermal corrector", "mg_per_cap": 500}
        ],
        "modern_layer_20": [
            {"ingredient": "Selenium L-Selenomethionine", "purpose": "Deiodinase D1/D2 enzyme cofactor (T4 to T3)", "mcg_per_cap": 100},
            {"ingredient": "Zinc Bisglycinate", "purpose": "TSH receptor binding affinity", "mg_per_cap": 10},
            {"ingredient": "Piperine", "purpose": "Guggulsterone absorption enhancement", "mg_per_cap": 5}
        ],
        "permitted_claim_green_zone": "Traditionally used to support healthy metabolic rate and optimal thyroid function.",
        "prohibited_claim_red_zone": "Replaces levothyroxine or cures Hashimoto's thyroiditis."
    },
    "ZAY-PROD-04": {
        "product_id": "ZAY-PROD-04",
        "internal_code": "ZV-M-03",
        "name": "Sleep+Stress PRO (NeuroCalm-S)",
        "clinical_axis": "Neuro-Psychological / Stress-Insomnia Axis",
        "parent_nuskha_code": "NE-01",
        "parent_nuskha_name": "Nuskha Musakkin-e-Rooh wa Dimagh",
        "regulatory_track": "FSSAI Track B (Nutraceutical)",
        "launch_priority": "Priority 4",
        "dosage_form": "60 Capsules",
        "mrp_target_inr": 1999,
        "daily_dose": "2 capsules 30-45 minutes before bedtime",
        "classical_core_80": [
            {"ingredient": "Jatamansi extract (Nardostachys)", "standardisation": "3% Jatamansone / Nardosinone", "mg_per_cap": 150},
            {"ingredient": "Asgandh KSM-66", "standardisation": "5% Withanolides", "mg_per_cap": 250},
            {"ingredient": "Khus root (Vetiver)", "standardisation": "Mubarrid-e-Dimagh", "mg_per_cap": 100},
            {"ingredient": "Gul Banafsha (Viola odorata)", "standardisation": "Gentle neural resolvent", "mg_per_cap": 100}
        ],
        "modern_layer_20": [
            {"ingredient": "L-Theanine", "purpose": "Alpha-wave brain state induction", "mg_per_cap": 100},
            {"ingredient": "Magnesium Glycinate", "purpose": "GABA synthesis cofactor", "mg_per_cap": 200},
            {"ingredient": "Zafran (Saffron extract)", "purpose": "Serotonin reuptake modulation", "mg_per_cap": 15}
        ],
        "permitted_claim_green_zone": "Supports restful sleep, healthy stress adaptation, and emotional equilibrium.",
        "prohibited_claim_red_zone": "Treats clinical depression or cures clinical anxiety disorder."
    },
    "ZAY-PROD-05": {
        "product_id": "ZAY-PROD-05",
        "internal_code": "ZV-F-02",
        "name": "OvaBalance PRO (Female Hormonal)",
        "clinical_axis": "Female Reproductive / PCOS Axis",
        "parent_nuskha_code": "PC-01",
        "parent_nuskha_name": "Nuskha Mudirr-e-Tams wa Muqawwi-e-Rahim",
        "regulatory_track": "AYUSH Track A (Schedule T GMP)",
        "launch_priority": "Secondary",
        "dosage_form": "60 Capsules",
        "mrp_target_inr": 2500,
        "daily_dose": "2 capsules twice daily with meals",
        "classical_core_80": [
            {"ingredient": "Methi standardised extract", "standardisation": "50% 4-HI & galactomannan", "mg_per_cap": 250},
            {"ingredient": "Guggul Shudh", "standardisation": "2.5% Guggulsterones", "mg_per_cap": 150},
            {"ingredient": "Chiraita (Swertia chirayita)", "standardisation": "Hepatic Tanqiya & aromatase support", "mg_per_cap": 100},
            {"ingredient": "Shatavari extract (Asparagus racemosus)", "standardisation": "20% Saponins (Muqawwi-e-Rahim)", "mg_per_cap": 150},
            {"ingredient": "Amla Musleh", "standardisation": "40% Tannins", "mg_per_cap": 100}
        ],
        "modern_layer_20": [
            {"ingredient": "Myo-Inositol + D-Chiro-Inositol", "purpose": "40:1 ratio second messenger insulin/FSH signalling", "mg_per_cap": 500},
            {"ingredient": "N-Acetyl Cysteine (NAC)", "purpose": "Follicular glutathione antioxidant", "mg_per_cap": 150},
            {"ingredient": "Zinc Bisglycinate", "purpose": "5-alpha reductase down-regulation for acne/hirsutism", "mg_per_cap": 15}
        ],
        "permitted_claim_green_zone": "Traditionally used to support regular menstrual cycles and female hormonal balance.",
        "prohibited_claim_red_zone": "Cures PCOS or guarantees pregnancy."
    },
    "ZAY-PROD-06": {
        "product_id": "ZAY-PROD-06",
        "internal_code": "ZV-G-01",
        "name": "LivClear PRO (JigarOne)",
        "clinical_axis": "Fatty Liver / Hepatic Axis",
        "parent_nuskha_code": "FK-01",
        "parent_nuskha_name": "Joshanda Muqawwi-e-Jigar wa Muhallil",
        "regulatory_track": "FSSAI Track B (Nutraceutical)",
        "launch_priority": "Secondary",
        "dosage_form": "60 Capsules",
        "mrp_target_inr": 2200,
        "daily_dose": "1 capsule twice daily before meals",
        "classical_core_80": [
            {"ingredient": "Kasni root extract (Cichorium intybus)", "standardisation": "Choleretic sesquiterpenes", "mg_per_cap": 250},
            {"ingredient": "Kutki extract (Picrorhiza kurroa)", "standardisation": "2% Picrosides I+II", "mg_per_cap": 150},
            {"ingredient": "Bhumi Amla (Phyllanthus niruri)", "standardisation": "Hepatic cytoprotective", "mg_per_cap": 150}
        ],
        "modern_layer_20": [
            {"ingredient": "Milk Thistle (Silymarin 80%)", "purpose": "Hepatocyte membrane stabilization & Nrf2 activation", "mg_per_cap": 140},
            {"ingredient": "CoQ10 Ubiquinol", "purpose": "Hepatic mitochondrial bioenergetics", "mg_per_cap": 50},
            {"ingredient": "Piperine", "purpose": "Bioavailability catalyst", "mg_per_cap": 5}
        ],
        "permitted_claim_green_zone": "Supports liver health, healthy hepatic enzyme levels, and detoxification processes.",
        "prohibited_claim_red_zone": "Reverses cirrhosis or cures hepatitis."
    },
    "ZAY-PROD-07": {
        "product_id": "ZAY-PROD-07",
        "internal_code": "ZV-M-04",
        "name": "MetaReset (Metabolic Weight & Glucose)",
        "clinical_axis": "Insulin Resistance / Metabolic Axis",
        "parent_nuskha_code": "WM-01",
        "parent_nuskha_name": "Nuskha Muhallil-e-Balgham wa Samn",
        "regulatory_track": "FSSAI Track B (Nutraceutical)",
        "launch_priority": "Secondary",
        "dosage_form": "60 Capsules",
        "mrp_target_inr": 2500,
        "daily_dose": "2 capsules daily with main meal",
        "classical_core_80": [
            {"ingredient": "Gurmar extract (Gymnema sylvestre)", "standardisation": "25% Gymnemic acids", "mg_per_cap": 250},
            {"ingredient": "Guggul Shudh", "standardisation": "10% Guggulsterones", "mg_per_cap": 150},
            {"ingredient": "Amla extract (Phyllanthus emblica - Musleh for Guggul)", "standardisation": "30% Tannins & Vit C", "mg_per_cap": 100},
            {"ingredient": "Zeera Siyah", "standardisation": "3% Thymoquinone", "mg_per_cap": 100}
        ],
        "modern_layer_20": [
            {"ingredient": "Berberine HCl (97%)", "purpose": "AMPK master metabolic switch activation", "mg_per_cap": 250},
            {"ingredient": "Alpha-Lipoic Acid (R-form)", "purpose": "GLUT4 translocation enhancement", "mg_per_cap": 100},
            {"ingredient": "Chromium Picolinate", "purpose": "Insulin receptor tyrosine kinase amplification", "mcg_per_cap": 200}
        ],
        "permitted_claim_green_zone": "Helps maintain healthy blood sugar levels already within normal range and supports metabolic vitality.",
        "prohibited_claim_red_zone": "Replaces insulin or cures Type 2 Diabetes."
    },
    "ZAY-PROD-08": {
        "product_id": "ZAY-PROD-08",
        "internal_code": "ZV-R-01",
        "name": "StoneGuard (Urolithiasis & Renal Support)",
        "clinical_axis": "Renal-Urinary Axis",
        "parent_nuskha_code": "ST-01",
        "parent_nuskha_name": "Joshanda Mufattit-e-Hasat Kulya",
        "regulatory_track": "AYUSH Track A (Schedule T GMP)",
        "launch_priority": "Secondary",
        "dosage_form": "60 Capsules + 100g Kulthi Powder",
        "mrp_target_inr": 1800,
        "daily_dose": "2 capsules twice daily + 10g Kulthi morning decoction",
        "classical_core_80": [
            {"ingredient": "Kulthi extract (Macrotyloma uniflorum)", "standardisation": "Calculus dissolvent (Mufattit)", "mg_per_cap": 300},
            {"ingredient": "Punarnava extract", "standardisation": "2.5% Boeravinones (Mudirr)", "mg_per_cap": 150},
            {"ingredient": "Sandal Safaid + Unnab", "standardisation": "Cooling urothelial protector", "mg_per_cap": 100}
        ],
        "modern_layer_20": [
            {"ingredient": "Potassium Magnesium Citrate", "purpose": "Urinary alkalinization & calcium oxalate crystal inhibition", "mg_per_cap": 250},
            {"ingredient": "Vitamin B6 (Pyridoxine)", "purpose": "Reduces endogenous hepatic oxalate synthesis", "mg_per_cap": 25}
        ],
        "permitted_claim_green_zone": "Traditionally used to support urinary tract flushing and renal physiological comfort.",
        "prohibited_claim_red_zone": "Dissolves staghorn calculi or replaces emergency urological surgery."
    },
    "ZAY-PROD-09": {
        "product_id": "ZAY-PROD-09",
        "internal_code": "ZV-C-01",
        "name": "CardioCalm (Neuro-Cardiac Integration)",
        "clinical_axis": "Cardio-Vascular Axis",
        "parent_nuskha_code": "CV-01",
        "parent_nuskha_name": "Nuskha Muqawwi-e-Qalb wa Khafqan",
        "regulatory_track": "FSSAI Track B (Nutraceutical)",
        "launch_priority": "Secondary",
        "dosage_form": "60 Capsules",
        "mrp_target_inr": 2200,
        "daily_dose": "1 capsule twice daily with meals",
        "classical_core_80": [
            {"ingredient": "Arjuna bark extract (Terminalia arjuna)", "standardisation": "1% Arjunosides (Muqawwi-e-Qalb)", "mg_per_cap": 300},
            {"ingredient": "Kalonji seed extract", "standardisation": "2.5% Thymoquinone", "mg_per_cap": 150},
            {"ingredient": "Gul-e-Gaozaban", "standardisation": "Cardiac demulcent & Mufarrih", "mg_per_cap": 100}
        ],
        "modern_layer_20": [
            {"ingredient": "CoQ10 Ubiquinol", "purpose": "Myocardial ATP support", "mg_per_cap": 50},
            {"ingredient": "Magnesium Glycinate", "purpose": "Vascular smooth muscle relaxation", "mg_per_cap": 150},
            {"ingredient": "Hibiscus sabdariffa extract", "purpose": "Anthocyanin ACE inhibition", "mg_per_cap": 100}
        ],
        "permitted_claim_green_zone": "Promotes cardiovascular resilience, normal arterial tone, and emotional calm.",
        "prohibited_claim_red_zone": "Treats angina or replaces prescription beta-blockers/ACE inhibitors."
    },
    "ZAY-PROD-10": {
        "product_id": "ZAY-PROD-10",
        "internal_code": "ZV-AI-01",
        "name": "JointEase PRO (JointResolve-K)",
        "clinical_axis": "Musculo-Skeletal / Inflammatory Joint Axis",
        "parent_nuskha_code": "JT-01",
        "parent_nuskha_name": "Nuskha Waja-ul-Mafasil wa Muhallil",
        "regulatory_track": "AYUSH Track A (Schedule T GMP)",
        "launch_priority": "Secondary",
        "dosage_form": "90 Capsules",
        "mrp_target_inr": 2500,
        "daily_dose": "1 capsule three times daily with meals",
        "classical_core_80": [
            {"ingredient": "Kundur (Boswellia serrata)", "standardisation": "65% Total Boswellic Acids (min 25% AKBA)", "mg_per_cap": 250},
            {"ingredient": "Guggul Shudh", "standardisation": "10% Guggulsterones", "mg_per_cap": 150},
            {"ingredient": "Amla extract (Phyllanthus emblica - Musleh for Guggul)", "standardisation": "30% Tannins & Vit C", "mg_per_cap": 100},
            {"ingredient": "Suranjan Shireen (Colchicum autumnale purified)", "standardisation": "Classical joint resolvent", "mg_per_cap": 50},
            {"ingredient": "Sonth (Zingiber officinale)", "standardisation": "5% Gingerols", "mg_per_cap": 50}
        ],
        "modern_layer_20": [
            {"ingredient": "Curcumin Phytosome (Meriva)", "purpose": "29x bioavailability NF-kB joint anti-inflammatory", "mg_per_cap": 200},
            {"ingredient": "Collagen Type II (UC-II Undenatured)", "purpose": "Cartilage extracellular matrix protection", "mg_per_cap": 20},
            {"ingredient": "Vitamin D3", "purpose": "Bone-joint immune homeostasis", "IU_per_cap": 1000}
        ],
        "permitted_claim_green_zone": "Traditionally used to support joint mobility, cartilage integrity, and ease morning stiffness.",
        "prohibited_claim_red_zone": "Cures osteoarthritis or reverses severe rheumatoid joint deformity."
    },
    "ZAY-PROD-11": {
        "product_id": "ZAY-PROD-11",
        "internal_code": "ZV-D-01",
        "name": "HairRevive System",
        "clinical_axis": "Dermato-Hair Axis",
        "parent_nuskha_code": "HR-01",
        "parent_nuskha_name": "Roghan Bhringraj wa Nuskha Sha'r",
        "regulatory_track": "FSSAI Track B (Nutraceutical + Cosmetic Oil)",
        "launch_priority": "Secondary",
        "dosage_form": "60 Capsules + 100mL Roghan Bhringraj",
        "mrp_target_inr": 1999,
        "daily_dose": "1 capsule twice daily + scalp massage 3x/week",
        "classical_core_80": [
            {"ingredient": "Bhringraj extract (Eclipta alba)", "standardisation": "0.5% Wedelolactone (5AR-II inhibition)", "mg_per_cap": 200},
            {"ingredient": "Amla extract", "standardisation": "40% Tannins & Vitamin C", "mg_per_cap": 150},
            {"ingredient": "Brahmi extract", "standardisation": "20% Bacosides", "mg_per_cap": 100}
        ],
        "modern_layer_20": [
            {"ingredient": "Saw Palmetto extract (85% fatty acids)", "purpose": "DHT follicular down-regulation", "mg_per_cap": 160},
            {"ingredient": "Pumpkin Seed Oil extract", "purpose": "Phytosterol 5AR inhibition", "mg_per_cap": 100},
            {"ingredient": "Biotin (Vitamin B7)", "purpose": "Keratin matrix synthesis", "mcg_per_cap": 5000},
            {"ingredient": "Zinc Bisglycinate", "purpose": "Follicular cellular division", "mg_per_cap": 15}
        ],
        "permitted_claim_green_zone": "Supports hair follicle nourishment, reduces stress-related hair fall, and promotes hair strength.",
        "prohibited_claim_red_zone": "Cures baldness or regrows hair on cicatricial fibrosed scalp."
    },
    "ZAY-PROD-12": {
        "product_id": "ZAY-PROD-12",
        "internal_code": "ZV-R-02",
        "name": "LungClear (Respiratory & Balgham)",
        "clinical_axis": "Respiratory Axis",
        "parent_nuskha_code": "RS-01",
        "parent_nuskha_name": "Joshanda Zeequn-Nafs wa Munaffis",
        "regulatory_track": "AYUSH Track A (Schedule T GMP)",
        "launch_priority": "Secondary",
        "dosage_form": "60 Capsules",
        "mrp_target_inr": 1800,
        "daily_dose": "1 capsule twice daily with warm water",
        "classical_core_80": [
            {"ingredient": "Vasaka (Adhatoda vasica)", "standardisation": "0.5% Vasicine & vasicinone (Bronchodilator)", "mg_per_cap": 250},
            {"ingredient": "Mulathi (Glycyrrhiza glabra)", "standardisation": "20% Glycyrrhizin (Mucolytic)", "mg_per_cap": 150},
            {"ingredient": "Tulsi (Ocimum sanctum)", "standardisation": "2.5% Ursolic acid", "mg_per_cap": 100},
            {"ingredient": "Sonth (Dry Ginger)", "standardisation": "5% Gingerols", "mg_per_cap": 50}
        ],
        "modern_layer_20": [
            {"ingredient": "N-Acetyl Cysteine (NAC)", "purpose": "Disulphide mucus bond cleavage (mucolytic gold standard)", "mg_per_cap": 300},
            {"ingredient": "Quercetin Phytosome", "purpose": "Airway mast cell stabilization", "mg_per_cap": 100}
        ],
        "permitted_claim_green_zone": "Traditionally used to support clear bronchial airways and healthy respiratory comfort.",
        "prohibited_claim_red_zone": "Replaces emergency asthma inhalers or cures chronic obstructive pulmonary disease."
    },
    "ZAY-PROD-13": {
        "product_id": "ZAY-PROD-13",
        "internal_code": "ZV-I-01",
        "name": "ImmunoGuard (Immune-Inflammatory)",
        "clinical_axis": "Immune-Inflammatory Axis",
        "parent_nuskha_code": "IM-01",
        "parent_nuskha_name": "Nuskha Musaffi-e-Dam wa Muqawwi-e-Tabiyat",
        "regulatory_track": "FSSAI Track B (Nutraceutical)",
        "launch_priority": "Year 2",
        "dosage_form": "60 Capsules",
        "mrp_target_inr": 2200,
        "daily_dose": "1 capsule twice daily with food",
        "classical_core_80": [
            {"ingredient": "Giloy extract (Tinospora cordifolia)", "standardisation": "3% Bitter principles", "mg_per_cap": 300},
            {"ingredient": "Chiraita extract", "standardisation": "Xanthone glycosides", "mg_per_cap": 100},
            {"ingredient": "Neem bark extract", "standardisation": "Blood purification", "mg_per_cap": 100}
        ],
        "modern_layer_20": [
            {"ingredient": "Zinc Bisglycinate", "purpose": "T-cell proliferation & immune defense", "mg_per_cap": 15},
            {"ingredient": "Vitamin D3 + K2", "purpose": "Treg regulatory tolerance", "IU_per_cap": 2000}
        ],
        "permitted_claim_green_zone": "Helps strengthen natural immune defenses and supports immune cell homeostasis.",
        "prohibited_claim_red_zone": "Treats autoimmune disorders or cures systemic lupus erythematosus."
    },
    "ZAY-PROD-14": {
        "product_id": "ZAY-PROD-14",
        "internal_code": "ZV-G-02",
        "name": "GutBalance (Digestive Microbiome)",
        "clinical_axis": "Gut-Digestive Axis",
        "parent_nuskha_code": "GI-01",
        "parent_nuskha_name": "Safoof Muqawwi-e-Meda wa Hazim",
        "regulatory_track": "FSSAI Track B (Nutraceutical)",
        "launch_priority": "Year 2",
        "dosage_form": "60 Capsules",
        "mrp_target_inr": 1800,
        "daily_dose": "1 capsule twice daily before meals",
        "classical_core_80": [
            {"ingredient": "Zeera Siyah", "standardisation": "3% TQ", "mg_per_cap": 200},
            {"ingredient": "Ajwain extract", "standardisation": "Carminative thymol", "mg_per_cap": 150},
            {"ingredient": "Saunf extract", "standardisation": "Trans-anethole", "mg_per_cap": 150}
        ],
        "modern_layer_20": [
            {"ingredient": "L-Glutamine", "purpose": "Enterocyte mucosal barrier fuel", "mg_per_cap": 300},
            {"ingredient": "Prebiotic FOS", "purpose": "Selective Bifidobacterium nourishment", "mg_per_cap": 100}
        ],
        "permitted_claim_green_zone": "Supports gut microbiome health, relieves occasional bloating, and aids natural digestion.",
        "prohibited_claim_red_zone": "Treats Crohn's disease or cures ulcerative colitis."
    },
    "ZAY-PROD-15": {
        "product_id": "ZAY-PROD-15",
        "internal_code": "ZV-N-02",
        "name": "NeuroClear (Cognitive-Memory)",
        "clinical_axis": "Cognitive-Memory Axis",
        "parent_nuskha_code": "NE-02",
        "parent_nuskha_name": "Majoon Muqawwi-e-Hafiza wa Dimagh",
        "regulatory_track": "FSSAI Track B (Nutraceutical)",
        "launch_priority": "Year 2",
        "dosage_form": "60 Capsules",
        "mrp_target_inr": 2500,
        "daily_dose": "1 capsule twice daily with breakfast and lunch",
        "classical_core_80": [
            {"ingredient": "Brahmi extract (Bacopa monnieri)", "standardisation": "20% Bacosides (BDNF upregulation)", "mg_per_cap": 250},
            {"ingredient": "Shankhpushpi (Convolvulus pluricaulis)", "standardisation": "Neuroprotective flavonoids", "mg_per_cap": 150},
            {"ingredient": "Jatamansi", "standardisation": "GABAergic modulation", "mg_per_cap": 100}
        ],
        "modern_layer_20": [
            {"ingredient": "Alpha-GPC (Choline precursor)", "purpose": "Acetylcholine synthesis for memory encoding", "mg_per_cap": 150},
            {"ingredient": "Phosphatidylserine", "purpose": "Neuronal membrane fluidity", "mg_per_cap": 100}
        ],
        "permitted_claim_green_zone": "Supports mental focus, cognitive clarity, memory recall, and neural resilience.",
        "prohibited_claim_red_zone": "Cures Alzheimer's disease or treats dementia."
    },
    "ZAY-PROD-16": {
        "product_id": "ZAY-PROD-16",
        "internal_code": "ZV-F-03",
        "name": "WomanVitality (Menopause & Vitality)",
        "clinical_axis": "Female Vitality / Menopause Axis",
        "parent_nuskha_code": "PC-02",
        "parent_nuskha_name": "Majoon Muqawwi-e-Rahim wa Mubahhi Niswan",
        "regulatory_track": "AYUSH Track A (Schedule T GMP)",
        "launch_priority": "Year 2",
        "dosage_form": "60 Capsules",
        "mrp_target_inr": 2200,
        "daily_dose": "1 capsule twice daily with meals",
        "classical_core_80": [
            {"ingredient": "Shatavari extract", "standardisation": "20% Saponins (Phytoestrogenic)", "mg_per_cap": 300},
            {"ingredient": "Asgandh extract", "standardisation": "5% Withanolides", "mg_per_cap": 150},
            {"ingredient": "Zafran (Saffron)", "standardisation": "Mood and hot flash relief", "mg_per_cap": 15}
        ],
        "modern_layer_20": [
            {"ingredient": "Black Cohosh (Cimicifuga racemosa)", "purpose": "Neuroendocrine thermoregulatory stabilization", "mg_per_cap": 40},
            {"ingredient": "Calcium Citrate Malate + D3", "purpose": "Postmenopausal bone density support", "mg_per_cap": 250}
        ],
        "permitted_claim_green_zone": "Traditionally used to ease menopausal transitions, hot flushes, and female vitality.",
        "prohibited_claim_red_zone": "Replaces hormone replacement therapy or cures menopausal syndrome."
    }
}


def get_all_core_products() -> List[Dict[str, Any]]:
    """Returns all 16 core GMP products."""
    return list(CORE_PRODUCTS_16.values())


def get_product_by_id(prod_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves product by ID (e.g. 'ZAY-PROD-01') or internal code (e.g. 'ZV-M-01')."""
    p_id = prod_id.upper()
    if p_id in CORE_PRODUCTS_16:
        return CORE_PRODUCTS_16[p_id]
    for p in CORE_PRODUCTS_16.values():
        if p["internal_code"].upper() == p_id:
            return p
    return None


def get_products_by_axis(axis_name: str) -> List[Dict[str, Any]]:
    """Filters products by target clinical axis."""
    return [
        p for p in CORE_PRODUCTS_16.values()
        if axis_name.lower() in p["clinical_axis"].lower()
    ]


def get_products_by_regulatory_track(track: str) -> List[Dict[str, Any]]:
    """Filters products by AYUSH Track A vs FSSAI Track B."""
    t_clean = track.upper()
    return [
        p for p in CORE_PRODUCTS_16.values()
        if t_clean in p["regulatory_track"].upper()
    ]


def get_classical_prescribing_metadata(clinical_axis: str) -> Dict[str, Any]:
    """
    Returns the 7-Pillar Classical Prescribing Bundle:
    Badraqa (Carrier Fluid), Chrono-Posology, and 3-Column Parhez Matrix.
    """
    from services.therapeutic.app.engines.master_nuskha_architect import (
        ORGAN_BADRAQA_CONDUIT_REGISTRY,
        ORGAN_PARHEZ_MATRIX,
        CHRONO_SCHEDULES
    )
    ax_upper = clinical_axis.upper()
    matched_axis = "MALE_REPRODUCTIVE"
    if "FEMALE" in ax_upper or "GYNEC" in ax_upper or "HORMONAL" in ax_upper:
        matched_axis = "FEMALE_REPRODUCTIVE"
    elif "NEURO" in ax_upper or "STRESS" in ax_upper or "MEMORY" in ax_upper:
        matched_axis = "NEURO_PSYCHOLOGICAL"
    elif "CARDIO" in ax_upper or "VASCULAR" in ax_upper:
        matched_axis = "CARDIOVASCULAR"
    elif "LIVER" in ax_upper or "JIGAR" in ax_upper:
        matched_axis = "HEPATO_BILIARY"
    elif "GUT" in ax_upper or "DIGESTIVE" in ax_upper:
        matched_axis = "GASTROINTESTINAL"
    elif "LUNG" in ax_upper or "RESPIRATORY" in ax_upper:
        matched_axis = "PULMONARY"
    elif "RENAL" in ax_upper or "STONE" in ax_upper:
        matched_axis = "RENAL_URINARY"
    elif "JOINT" in ax_upper or "SKELETAL" in ax_upper or "INFLAMMATORY" in ax_upper:
        matched_axis = "MUSCULOSKELETAL"
    elif "METABOLIC" in ax_upper or "WEIGHT" in ax_upper:
        matched_axis = "METABOLIC"
    elif "IMMUNE" in ax_upper:
        matched_axis = "IMMUNOLOGICAL"

    badraqa = ORGAN_BADRAQA_CONDUIT_REGISTRY.get(matched_axis, ORGAN_BADRAQA_CONDUIT_REGISTRY["MALE_REPRODUCTIVE"])
    parhez = ORGAN_PARHEZ_MATRIX.get(matched_axis, ORGAN_PARHEZ_MATRIX["MALE_REPRODUCTIVE"])

    return {
        "matched_organ_axis": matched_axis,
        "badraqa_conduit_vehicle": badraqa,
        "chrono_posology": CHRONO_SCHEDULES["bad_az_ghiza"],
        "parhez_dietary_matrix": parhez,
        "galenical_processing": "GMP Standardized micro-granulation with active bio-enhancer synergy."
    }


# Automatically attach 7-Pillars classical metadata to each core product
for _prod_id, _prod in CORE_PRODUCTS_16.items():
    _meta = get_classical_prescribing_metadata(_prod.get("clinical_axis", ""))
    _prod["badraqa_vehicle"] = _meta["badraqa_conduit_vehicle"]["primary_conduit"]
    _prod["badraqa_action_vector"] = _meta["badraqa_conduit_vehicle"]["action_vector"]
    _prod["chrono_timing"] = _meta["chrono_posology"]["time_window"]
    _prod["parhez_prohibited_foods"] = _meta["parhez_dietary_matrix"]["prohibited_antagonistic"]
    _prod["parhez_synergistic_foods"] = _meta["parhez_dietary_matrix"]["accelerating_synergistic"]

