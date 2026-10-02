"""
ZAYVORA 12-Axis Clinical Intelligence Framework™
Proposed Proprietary Clinical Architecture; advisory decision-support layer,
not a replacement for clinician-validated diagnosis.

This canonical schema models the 12 Organ-Axis Systems and explicitly maps
them back to Book 1's 3 Foundational Core Axes:
  1. Jigar–Khasiya (Liver–Gonadal)
  2. Jigar–Rahim (Liver–Uterine/Ovarian)
  3. Dimagh–Kuli (Brain–Adrenal/HPA)
"""

from typing import Dict, Any, List

ORGAN_AXES_12: Dict[str, Dict[str, Any]] = {
    "AXIS_01": {
        "axis_id": "AXIS_01",
        "axis_name": "Gut–Liver Axis",
        "classical_nodes": ["Mida (Stomach)", "Amaa (Intestines)", "Jigar (Liver)"],
        "modern_nodes": ["Gastrointestinal tract", "Hepatic portal system", "Gut microbiome", "Mucosal barrier"],
        "clinical_domains": ["Digestion", "Bowel transit", "Hepatic biotransformation", "Bile acid metabolism", "Nutrient absorption"],
        "symptoms": ["Bloating", "Constipation", "Diarrhea", "Acid reflux / Heartburn", "Post-prandial fatigue", "Abdominal discomfort"],
        "investigations": ["LFT (ALT, AST, GGT, Bilirubin)", "Stool analysis / Calprotectin", "CBC", "Abdominal Ultrasound when indicated"],
        "unani_mapping": {
            "mizaj_tendency": ["Balghami (Cold-Moist)", "Safrawi (Hot-Dry)"],
            "akhlat_pattern": ["Balgham excess in Meda/Amaa", "Safra irritation in mucosa"],
            "afaal": ["Quwwat-e-Hazima (Digestive faculty)", "Quwwat-e-Masika (Retentive faculty)", "Quwwat-e-Dafi'a (Expulsive faculty)"],
            "usoole_ilaj": ["Tadbeer-e-Ghiza (Low-FODMAP / easily digestible warm food)", "Munzij wa Mushil if humoral stagnation", "Carminative & hepatoprotective botanicals"]
        },
        "safety": {
            "red_flags": ["Unexplained weight loss", "Gastrointestinal bleeding / Melena", "Nocturnal bowel symptoms", "Persistent vomiting"],
            "contraindications": ["Avoid strong purgatives (Mushil-e-Qawi) during acute bowel inflammation or obstruction"],
            "referral_rules": ["Gastroenterology referral if alarm features present or calprotectin significantly elevated"]
        },
        "foundational_core_links": ["Jigar–Khasiya", "Jigar–Rahim"],
        "evidence_status": "proposed_proprietary",
        "clinician_approval_required": True
    },
    "AXIS_02": {
        "axis_id": "AXIS_02",
        "axis_name": "Metabolic–Pancreatic Axis",
        "classical_nodes": ["Jigar (Liver)", "Banka (Pancreas)", "Shareen (Vascular/Adipose)"],
        "modern_nodes": ["Pancreatic beta-cells", "Adipose tissue", "Skeletal muscle", "Hepatic gluconeogenesis"],
        "clinical_domains": ["Glucose homeostasis", "Insulin sensitivity", "Adipokine signaling", "Lipid partitioning"],
        "symptoms": ["Weight gain / Central adiposity", "Postprandial lethargy", "Sugar cravings", "Polydipsia", "Acanthosis nigricans"],
        "investigations": ["HbA1c", "Fasting Plasma Glucose", "Fasting Insulin (HOMA-IR)", "Lipid Profile (TG, HDL)"],
        "unani_mapping": {
            "mizaj_tendency": ["Bard-Ratab (Cold-Moist / Balghami)", "Harr-Yabis (Hot-Dry / Safrawi)"],
            "akhlat_pattern": ["Samn Mufrit with Balgham accumulation", "Hararat exhaustion in beta-cells"],
            "afaal": ["Quwwat-e-Ghazia (Nutritive faculty)", "Hararat-e-Ghariziya"],
            "usoole_ilaj": ["Time-Restricted Eating (TRE)", "Low-GI whole food diet", "Insulin-sensitizing herbs (Berberine, Gurmar, Cinnamon)"]
        },
        "safety": {
            "red_flags": ["HbA1c >= 10.0%", "Ketonuria / Diabetic Ketoacidosis symptoms", "Rapid unintentional weight loss"],
            "contraindications": ["Do not discontinue prescribed insulin or oral hypoglycemics without medical supervision"],
            "referral_rules": ["Immediate endocrinology referral for severe hyperglycemia or suspicion of Type 1/LADA"]
        },
        "foundational_core_links": ["Jigar–Khasiya", "Jigar–Rahim", "Dimagh–Kuli"],
        "evidence_status": "proposed_proprietary",
        "clinician_approval_required": True
    },
    "AXIS_03": {
        "axis_id": "AXIS_03",
        "axis_name": "Thyroid–Adrenal Axis",
        "classical_nodes": ["Ghuda Darqiya (Thyroid)", "Kuliya / Ghuda Fawq-al-Kuliya (Adrenal)", "Rooh (Vital Force)"],
        "modern_nodes": ["HPT axis (Hypothalamic-Pituitary-Thyroid)", "HPA axis (Hypothalamic-Pituitary-Adrenal)", "Cellular thermogenesis"],
        "clinical_domains": ["Basal metabolic rate", "Cortisol awakening response", "Thermoregulation", "Mitochondrial energy"],
        "symptoms": ["Chronic fatigue", "Cold intolerance", "Brain fog", "Afternoon energy crash", "Difficulty waking", "Weight resistance"],
        "investigations": ["TSH", "Free T3", "Free T4", "Anti-TPO", "Salivary Diurnal Cortisol", "DHEA-S"],
        "unani_mapping": {
            "mizaj_tendency": ["Bard-Yabis (Cold-Dry / Sauda)", "Bard-Ratab (Cold-Wet / Balgham)"],
            "akhlat_pattern": ["Weak Hararat-e-Ghariziya", "Sauda-Balgham cold depression"],
            "afaal": ["Quwwat-e-Haywaniya (Vital faculty)", "Hararat maintenance"],
            "usoole_ilaj": ["Warming adaptogenic botanicals (Ashwagandha, Shilajit)", "Morning light circadian alignment", "Avoid fasting overload in HPA burnout"]
        },
        "safety": {
            "red_flags": ["TSH > 10.0 mIU/L", "Severe adrenal insufficiency (Addisonian crisis risk)", "Anti-TPO > 300 IU/mL with rapid enlargement"],
            "contraindications": ["Do not administer heavy thermogenics in thyrotoxicosis or acute hyperthyroid flares"],
            "referral_rules": ["Endocrinology evaluation required for overt hypothyroidism or abnormal thyroid nodule"]
        },
        "foundational_core_links": ["Dimagh–Kuli", "Jigar–Rahim"],
        "evidence_status": "proposed_proprietary",
        "clinician_approval_required": True
    },
    "AXIS_04": {
        "axis_id": "AXIS_04",
        "axis_name": "Male Reproductive Axis",
        "classical_nodes": ["Khasiya (Testes)", "Jigar (Liver)", "Qalb (Heart)", "Dimagh (Brain)"],
        "modern_nodes": ["HPG axis (Hypothalamic-Pituitary-Gonadal)", "Leydig cells", "Sertoli cells", "Hepatic SHBG regulation"],
        "clinical_domains": ["Spermatogenesis", "Testosterone synthesis", "Mitochondrial motility", "Erectile hemodynamics", "Libido"],
        "symptoms": ["Low libido", "Erectile weakness", "Oligospermia / Asthenospermia", "Low vitality", "Muscle loss"],
        "investigations": ["Semen Analysis (WHO 2021 criteria)", "Total & Free Testosterone", "LH", "FSH", "Prolactin", "Scrotal Ultrasound"],
        "unani_mapping": {
            "mizaj_tendency": ["Bard-Ratab (Sluggish)", "Harr-Yabis (Seminal heat/viscosity)"],
            "akhlat_pattern": ["Nuqs-e-Mani (Seminal depletion)", "Burudat in Khasiya"],
            "afaal": ["Quwwat-e-Tawallud (Generative faculty)", "Quwwat-e-Bah (Reproductive energy)"],
            "usoole_ilaj": ["Muqawwiyat-e-Bah (Constitutional reproductive tonics)", "Phase 1 Tanqiya followed by Phase 2 Muqawwi", "Antioxidant cellular support"]
        },
        "safety": {
            "red_flags": ["Testicular mass or persistent pain", "Azoospermia (complete absence of sperm)", "Severe hypogonadism"],
            "contraindications": ["Do not administer heavy tonics (Muqawwi) during active seminal or urinary tract infection"],
            "referral_rules": ["Urology / Andrology co-management required for azoospermia, varicocele grade III, or genital anomalies"]
        },
        "foundational_core_links": ["Jigar–Khasiya", "Dimagh–Kuli"],
        "evidence_status": "proposed_proprietary",
        "clinician_approval_required": True
    },
    "AXIS_05": {
        "axis_id": "AXIS_05",
        "axis_name": "Female Reproductive Axis",
        "classical_nodes": ["Rahim (Uterus)", "Khusyatur-Rahim (Ovaries)", "Jigar (Liver)", "Dimagh (Brain)"],
        "modern_nodes": ["Ovarian theca/granulosa cells", "Endometrium", "Hypothalamic GnRH pulse generator", "Hepatic estrogen clearance"],
        "clinical_domains": ["Ovulatory cycle", "Endometrial receptivity", "Follicular maturation", "Estrogen-progesterone balance", "Pelvic circulation"],
        "symptoms": ["Irregular menses / Amenorrhea", "Hirsutism / Acne", "Dysmenorrhea", "Pelvic heaviness", "Ovulatory pain", "Infertility"],
        "investigations": ["Pelvic Ultrasound (PCOM / Endometrial thickness)", "LH/FSH ratio", "Day 21 Progesterone", "Total Testosterone", "AMH"],
        "unani_mapping": {
            "mizaj_tendency": ["Bard-Ratab (Balghami phlegmatic obstruction)", "Harr-Yabis (Hyperandrogenic Safra)"],
            "akhlat_pattern": ["Ihtibas-e-Taams (Menstrual obstruction)", "Ghilaz-e-Dam"],
            "afaal": ["Quwwat-e-Nafisa (Menstrual regulatory faculty)", "Quwwat-e-Tawallud"],
            "usoole_ilaj": ["Mudirr-e-Haiz (Emmenagogues)", "Inositol 40:1 ratio & Spearmint", "Low-GI anti-inflammatory nutrition"]
        },
        "safety": {
            "red_flags": ["Abnormal uterine bleeding / Post-coital bleeding", "AMH < 0.3 ng/mL (critically diminished reserve)", "Severe pelvic mass"],
            "contraindications": ["Contraindicated: Emmenagogic or uterine contracting herbs during pregnancy"],
            "referral_rules": ["Gynecologic oncology referral for postmenopausal bleeding or suspicious ovarian cyst morphology"]
        },
        "foundational_core_links": ["Jigar–Rahim", "Dimagh–Kuli"],
        "evidence_status": "proposed_proprietary",
        "clinician_approval_required": True
    },
    "AXIS_06": {
        "axis_id": "AXIS_06",
        "axis_name": "Neuro–Psychological Axis",
        "classical_nodes": ["Dimagh (Brain)", "Qalb (Heart)", "Rooh-e-Nafsani (Psychic Spirit)"],
        "modern_nodes": ["Prefrontal cortex", "Amygdala", "Vagus nerve", "Default mode network", "Enteric-brain neurotransmitters"],
        "clinical_domains": ["Emotional regulation", "Autonomic tone (HRV)", "Sleep architecture", "Cognitive stamina", "Stress resilience"],
        "symptoms": ["Anxiety / Nervous tension", "Ruminative sadness (Huzn)", "Sleep-onset insomnia", "Brain fatigue", "Palpitations (Khalajan)"],
        "investigations": ["PSS-10", "PHQ-9", "GAD-7", "PSQI (Sleep Index)", "Heart Rate Variability (HRV)", "Salivary Cortisol"],
        "unani_mapping": {
            "mizaj_tendency": ["Saudavi (Cold-Dry)", "Safrawi (Hot-Dry acute anxiety)"],
            "akhlat_pattern": ["Ghalba-e-Sauda in Dimagh", "Combustion of Safra into Sauda Ihtiraqiya"],
            "afaal": ["Quwwat-e-Mudrika (Perceptive faculty)", "Quwwat-e-Hafiza (Memory)"],
            "usoole_ilaj": ["Ilaj bil Nafsiyat (Mind-body therapy, Dhikr, CBT)", "Nervine tonics (Jatamansi, Saffron, Brahmi)", "Resonant slow breathing at 6 cycles/min"]
        },
        "safety": {
            "red_flags": ["Active suicidal ideation or intent", "Psychotic symptoms / Hallucinations", "Severe depressive stupor"],
            "contraindications": ["Do not replace psychiatric medications abruptly; avoid St. John's Wort with SSRIs/SNRIs (serotonin syndrome)"],
            "referral_rules": ["Immediate emergency psychiatric escalation if suicide risk or acute psychotic episode detected"]
        },
        "foundational_core_links": ["Dimagh–Kuli", "Jigar–Khasiya", "Jigar–Rahim"],
        "evidence_status": "proposed_proprietary",
        "clinician_approval_required": True
    },
    "AXIS_07": {
        "axis_id": "AXIS_07",
        "axis_name": "Cardio–Vascular Axis",
        "classical_nodes": ["Qalb (Heart)", "Shareen (Arteries)", "Dam (Blood Humour)"],
        "modern_nodes": ["Myocardium", "Vascular endothelium", "Renin-Angiotensin-Aldosterone System (RAAS)", "Baroreceptors"],
        "clinical_domains": ["Arterial blood pressure", "Endothelial nitric oxide bioavailability", "Vascular stiffness", "Myocardial performance"],
        "symptoms": ["Elevated blood pressure", "Exertional dyspnea", "Throbbing headache", "Facial flushing", "Chest tightness"],
        "investigations": ["Ambulatory BP Monitoring", "ECG", "Lipid Subfractions (ApoB, Lp(a))", "hs-CRP", "Coronary Artery Calcium (CAC) when indicated"],
        "unani_mapping": {
            "mizaj_tendency": ["Harr-Ratab (Damawi plethora)", "Harr-Yabis (Arterial dryness/stiffness)"],
            "akhlat_pattern": ["Imtila-e-Dam (Vascular plethora)", "Ghulba-e-Dam"],
            "afaal": ["Quwwat-e-Haywaniya (Vital cardiovascular faculty)", "Nabz rhythm"],
            "usoole_ilaj": ["DASH diet / Sodium < 2g/day", "Cardiotonic botanicals (Arjuna, Kalonji, Hibiscus)", "Contrast hydrotherapy to train vascular reactivity"]
        },
        "safety": {
            "red_flags": ["BP >= 180/120 mmHg (Hypertensive Crisis)", "Acute chest pain radiating to left arm/jaw", "Acute neurological deficit / Stroke signs"],
            "contraindications": ["Do not withhold emergency antihypertensives during stage 2 crisis; avoid vigorous regimental therapy in unstable angina"],
            "referral_rules": ["Immediate emergency department escalation for acute coronary syndrome or hypertensive emergency"]
        },
        "foundational_core_links": ["Jigar–Khasiya", "Jigar–Rahim"],
        "evidence_status": "proposed_proprietary",
        "clinician_approval_required": True
    },
    "AXIS_08": {
        "axis_id": "AXIS_08",
        "axis_name": "Renal–Urinary Axis",
        "classical_nodes": ["Kuliya (Kidneys)", "Masana (Bladder)", "Majra-e-Bawl (Urinary Tract)"],
        "modern_nodes": ["Glomerular filtration barrier", "Renal tubules", "Electrolyte transport", "Urothelium"],
        "clinical_domains": ["Fluid and electrolyte homeostasis", "Renal clearance", "Acid-base balance", "Urinary pH and crystallization"],
        "symptoms": ["Fluid retention / Periorbital edema", "Dysuria", "Nocturia", "Flank pain", "Foamy urine"],
        "investigations": ["Serum Creatinine & eGFR", "Urine Albumin:Creatinine Ratio (UACR)", "Urinalysis / Microscopy", "Renal Ultrasound"],
        "unani_mapping": {
            "mizaj_tendency": ["Bard-Ratab (Cold-wet fluid stagnation)", "Harr-Yabis (Renal heat / stone tendency)"],
            "akhlat_pattern": ["Su-e-Mizaj Kuliya", "Hasat-e-Kuliya (Calculus formation)"],
            "afaal": ["Quwwat-e-Mumayyiza (Filtration faculty)", "Quwwat-e-Dafi'a Bawliya"],
            "usoole_ilaj": ["Mudirr-e-Bawl (Gentle herbal diuretics: Dandelion, Parsley root)", "Alkalinizing hydration", "Low-oxalate dietary adjustment"]
        },
        "safety": {
            "red_flags": ["eGFR < 30 mL/min/1.73m² (Severe CKD)", "Gross hematuria", "Anuria / Acute kidney injury", "Uremic symptoms"],
            "contraindications": ["Avoid nephrotoxic substances; strict contraindication for potassium-sparing or heavy botanicals in advanced renal failure"],
            "referral_rules": ["Nephrology referral required for eGFR < 60 with persistent proteinuria or unexplained hematuria"]
        },
        "foundational_core_links": ["Dimagh–Kuli"],
        "evidence_status": "proposed_proprietary",
        "clinician_approval_required": True
    },
    "AXIS_09": {
        "axis_id": "AXIS_09",
        "axis_name": "Respiratory Axis",
        "classical_nodes": ["Riya (Lungs)", "Qasbat al-Riya (Trachea/Bronchi)", "Rooh (Vital Breath)"],
        "modern_nodes": ["Bronchial tree", "Alveolar-capillary membrane", "Thoracic diaphragm", "Mucociliary clearance"],
        "clinical_domains": ["Gas exchange", "Airway hyperreactivity", "Mucus rheology", "Respiratory immune surveillance"],
        "symptoms": ["Chronic cough", "Wheezing / Dyspnea", "Excessive sputum production", "Sinus congestion", "Chest constriction"],
        "investigations": ["Spirometry / PFT", "Chest X-ray / CT when indicated", "Pulse Oximetry (SpO2)", "Eosinophil count / IgE"],
        "unani_mapping": {
            "mizaj_tendency": ["Bard-Ratab (Balgham excess in lungs)", "Harr-Yabis (Airway dryness / spasmodic)"],
            "akhlat_pattern": ["Ghalba-e-Balgham in Riya", "Zeequn-Nafs (Asthma)"],
            "afaal": ["Quwwat-e-Tanaffus (Respiratory faculty)", "Tanaffus-e-Tabi'i"],
            "usoole_ilaj": ["Munaffis-e-Balgham (Expectorants: Licorice, Adhatoda vasica)", "Steam therapy with Eucalyptus", "Diaphragmatic breath training"]
        },
        "safety": {
            "red_flags": ["SpO2 < 92% on room air", "Acute severe bronchospasm unresponsive to bronchodilators", "Hemoptysis"],
            "contraindications": ["Do not discontinue rescue inhalers in asthma; avoid respiratory irritants and smoke exposure"],
            "referral_rules": ["Pulmonology referral for persistent abnormal spirometry or suspicious pulmonary infiltrate"]
        },
        "foundational_core_links": ["Jigar–Khasiya", "Dimagh–Kuli"],
        "evidence_status": "proposed_proprietary",
        "clinician_approval_required": True
    },
    "AXIS_10": {
        "axis_id": "AXIS_10",
        "axis_name": "Immune–Inflammatory Axis",
        "classical_nodes": ["Tabiyat (Innate Intelligence)", "Tihal (Spleen)", "Dam (Blood Humour)"],
        "modern_nodes": ["Innate and adaptive immunity", "T-regulatory cells (Tregs)", "NF-kB / Inflammatory cascade", "Gut lymphoid tissue (GALT)"],
        "clinical_domains": ["Self-tolerance", "Pathogen surveillance", "Chronic low-grade inflammation", "Lymphatic drainage"],
        "symptoms": ["Joint pain / Arthralgia", "Recurrent infections", "Allergic flares", "Low-grade malaise", "Skin rashes"],
        "investigations": ["hs-CRP", "ESR", "ANA / Autoantibody panels", "Serum Vitamin D (25-OH)", "Immunoglobulin levels"],
        "unani_mapping": {
            "mizaj_tendency": ["Saudavi-Safrawi (Chronic inflammatory combustion)", "Balghami (Immune sluggishness)"],
            "akhlat_pattern": ["Fasad-e-Dam (Blood dyscrasia)", "Su-e-Mizaj Mukhtalif"],
            "afaal": ["Quwwat-e-Mudafi'a (Defense faculty)", "Tabiyat self-repair"],
            "usoole_ilaj": ["Anti-inflammatory Mediterranean / AIP diet", "Curcumin, Boswellia, Omega-3 fatty acids", "Vitamin D optimization to 40-60 ng/mL"]
        },
        "safety": {
            "red_flags": ["High-titer systemic autoimmune disease activity (Lupus nephritis, severe RA vasculitis)", "Unexplained lymphadenopathy", "High fever with constitutional collapse"],
            "contraindications": ["Do not administer strong immune stimulants (Echinacea, high-dose astragalus) in active autoimmune flares"],
            "referral_rules": ["Rheumatology / Clinical Immunology referral for multisystem autoimmune disease or biologic therapy"]
        },
        "foundational_core_links": ["Dimagh–Kuli", "Jigar–Rahim"],
        "evidence_status": "proposed_proprietary",
        "clinician_approval_required": True
    },
    "AXIS_11": {
        "axis_id": "AXIS_11",
        "axis_name": "Musculo–Skeletal Axis",
        "classical_nodes": ["Azam (Bones)", "Azlat (Muscles)", "Mafasil (Joints)", "Asab (Tendons/Ligaments)"],
        "modern_nodes": ["Skeletal muscle myofibrils", "Articular cartilage", "Synovial membrane", "Bone trabeculae"],
        "clinical_domains": ["Myofascial tone", "Joint mobility and lubrication", "Bone mineral density", "Postural stability"],
        "symptoms": ["Joint stiffness", "Chronic low back pain", "Muscle cramping / Myalgia", "Postural fatigue", "Reduced range of motion"],
        "investigations": ["Joint Radiographs / MRI", "Serum Calcium, Magnesium, Alkaline Phosphatase", "DEXA scan", "Uric Acid"],
        "unani_mapping": {
            "mizaj_tendency": ["Bard-Yabis (Sauda degeneration/stiffness)", "Bard-Ratab (Joint effusion/Balgham)"],
            "akhlat_pattern": ["Waja-ul-Mafasil (Arthritis)", "Rikhwat (Muscle flaccidity)"],
            "afaal": ["Quwwat-e-Muharrika (Locomotor faculty)", "Skeletal integrity"],
            "usoole_ilaj": ["Dalak (Structured therapeutic massage)", "Warming topical liniments (Roghan-e-Suranjan, Roghan-e-Balsan)", "Targeted resistance training"]
        },
        "safety": {
            "red_flags": ["Cauda equina syndrome signs (saddle anesthesia, bowel/bladder dysfunction)", "Acute septic arthritis (hot, red, swollen joint with fever)", "Pathological fracture"],
            "contraindications": ["Contraindicated: Deep tissue manipulation or vigorous regimental therapy over acute fractures, septic joints, or severe osteoporosis"],
            "referral_rules": ["Orthopedic / Spine surgery referral for acute neurological compression or progressive structural instability"]
        },
        "foundational_core_links": ["Jigar–Khasiya", "Dimagh–Kuli"],
        "evidence_status": "proposed_proprietary",
        "clinician_approval_required": True
    },
    "AXIS_12": {
        "axis_id": "AXIS_12",
        "axis_name": "Dermato–Hair Axis",
        "classical_nodes": ["Jild (Skin)", "Sha'r (Hair)", "Masan (Pores)", "Jigar (Liver)"],
        "modern_nodes": ["Stratum corneum epidermal barrier", "Dermal fibroblasts / Collagen", "Pilosebaceous unit", "Sebaceous lipid homeostasis"],
        "clinical_domains": ["Cutaneous barrier integrity", "Follicular cycling", "Sebum regulation", "Microvascular skin perfusion", "Peripheral detox"],
        "symptoms": ["Acne vulgaris", "Telogen effluvium / Hair thinning", "Dry eczema / Pruritus", "Skin hyperpigmentation (Melasma)", "Premature hair graying"],
        "investigations": ["Ferritin", "Zinc", "Thyroid panel", "Biotin / Vitamin D", "Dermatoscopy when indicated"],
        "unani_mapping": {
            "mizaj_tendency": ["Harr-Yabis (Safrawi acne/rashes)", "Bard-Yabis (Sauda dry pruritus/alopecia)"],
            "akhlat_pattern": ["Fasad-e-Akhlat in cutaneous capillaries", "Ihtibaas of sweat pores"],
            "afaal": ["Quwwat-e-Jildiya (Dermal protective faculty)", "Tanqiya via cutaneous sweat"],
            "usoole_ilaj": ["Musaffi-e-Dam (Blood purifiers: Neem, Chiraita, Kasni)", "Topical soothing oils (Almond, Rose oil)", "Hammam steam to open cutaneous pores"]
        },
        "safety": {
            "red_flags": ["Malignant melanoma warning signs (ABCDE rule)", "Erythroderma covering > 90% body surface area", "Stevens-Johnson syndrome / Toxic epidermal necrolysis signs"],
            "contraindications": ["Do not apply abrasive regimental therapies over active open eczematous lesions, severe bullae, or infected dermatoses"],
            "referral_rules": ["Dermatology referral for non-healing ulcers, suspicious pigmented lesions, or severe unresponsive dermatoses"]
        },
        "foundational_core_links": ["Jigar–Rahim", "Jigar–Khasiya"],
        "evidence_status": "proposed_proprietary",
        "clinician_approval_required": True
    }
}


def get_all_organ_axes() -> List[Dict[str, Any]]:
    """Returns the full list of all 12 Organ-Axis schemas."""
    return list(ORGAN_AXES_12.values())


def get_axis_by_id(axis_id: str) -> Dict[str, Any]:
    """Retrieves single axis schema by ID (e.g. 'AXIS_01')."""
    return ORGAN_AXES_12.get(axis_id.upper())


def get_axes_by_foundational_core(core_axis_name: str) -> List[Dict[str, Any]]:
    """Filters axes connected to one of the 3 Foundational Core Axes (Jigar-Khasiya, Jigar-Rahim, Dimagh-Kuli)."""
    return [
        axis for axis in ORGAN_AXES_12.values()
        if core_axis_name in axis.get("foundational_core_links", [])
    ]
