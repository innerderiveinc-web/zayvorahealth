"""
ZAYVORA Health OS™ — Drug-Herb Interaction & Safety Firewall Knowledge Catalog
==============================================================================
Contains the comprehensive clinical interaction matrix between classical Unani
and standardized botanical actives and modern pharmaceutical drug classes,
alongside universal absolute contraindications and pre-operative washout protocols.
"""

from typing import Dict, Any, List, Optional

MASTER_INTERACTIONS: List[Dict[str, Any]] = [
    {
        "interaction_id": "DHI-001",
        "herb_active": "Asrol (Rauwolfia serpentina / Reserpine)",
        "allopathic_drug_class": "Antihypertensives (ACE inhibitors, ARBs, Beta-blockers, CCBs)",
        "severity": "CRITICAL",
        "clinical_effect": "Profound synergistic hypotension and bradycardia",
        "mechanism": "Reserpine depletes vesicular catecholamines in postganglionic sympathetic terminals, compounding pharmaceutical afterload reduction.",
        "management": "Prescription Only (Schedule E-1). Mandatory baseline BP check. Daily home BP monitoring. Titrate pharmaceutical antihypertensives under physician supervision."
    },
    {
        "interaction_id": "DHI-002",
        "herb_active": "Asrol (Rauwolfia serpentina / Reserpine)",
        "allopathic_drug_class": "CNS Depressants (Benzodiazepines, Alcohol, Barbiturates)",
        "severity": "CRITICAL",
        "clinical_effect": "Excessive central nervous system depression, profound sedation, exacerbation of depressive disorders",
        "mechanism": "Additive central monoamine depletion and GABA-A potentiation.",
        "management": "Absolute contraindication with high-dose sedative regimens. Screen for clinical depression before initiating."
    },
    {
        "interaction_id": "DHI-003",
        "herb_active": "Guggulu (Commiphora mukul / Guggulsterones)",
        "allopathic_drug_class": "Anticoagulants (Warfarin, Heparin, NOACs - Apixaban, Rivaroxaban) & Antiplatelets (Aspirin, Clopidogrel)",
        "severity": "CRITICAL",
        "clinical_effect": "Significantly heightened risk of severe systemic hemorrhage and hematoma",
        "mechanism": "Guggulsterones inhibit platelet aggregation factor (PAF) and possess mild intrinsic fibrinolytic activity.",
        "management": "INR monitoring mandatory every 7 days if co-administered with Warfarin. Discontinue 7 days before any surgical or dental procedure."
    },
    {
        "interaction_id": "DHI-004",
        "herb_active": "Guggulu (Commiphora mukul / Guggulsterones)",
        "allopathic_drug_class": "Thyroid Hormone Replacements (Levothyroxine, Liothyronine)",
        "severity": "MODERATE",
        "clinical_effect": "Potential drug-induced hyperthyroidism or erratic TSH fluctuations",
        "mechanism": "Guggulsterones upregulate peripheral monodeiodinase conversion of T4 to bioactive T3.",
        "management": "Check serum TSH and free T3/T4 at 30 days and 60 days. Adjust synthetic levothyroxine dosage accordingly."
    },
    {
        "interaction_id": "DHI-005",
        "herb_active": "Asl-us-Soos (Glycyrrhiza glabra / Glycyrrhizin)",
        "allopathic_drug_class": "Loop & Thiazide Diuretics (Furosemide, Hydrochlorothiazide) & Cardiac Glycosides (Digoxin)",
        "severity": "CRITICAL",
        "clinical_effect": "Severe hypokalemia, cardiac dysrhythmias, fatal digoxin toxicity",
        "mechanism": "Glycyrrhetinic acid reversibly inhibits renal 11-beta-hydroxysteroid dehydrogenase type 2 (11-beta-HSD2), allowing cortisol to hyper-activate mineralocorticoid receptors.",
        "management": "Do not co-administer high-dose licorice formulations (ZAY-006) with potassium-wasting diuretics or digoxin without serum potassium monitoring. Use DGL (deglycyrrhizinated) form if indicated."
    },
    {
        "interaction_id": "DHI-006",
        "herb_active": "Asl-us-Soos (Glycyrrhiza glabra / Glycyrrhizin)",
        "allopathic_drug_class": "Antihypertensive medications",
        "severity": "MODERATE",
        "clinical_effect": "Loss of blood pressure control; hypertensive rebound",
        "mechanism": "Sodium retention and fluid expansion mediated by mineralocorticoid excess.",
        "management": "Limit glycyrrhizin intake to < 100mg daily in hypertensive patients; monitor BP weekly."
    },
    {
        "interaction_id": "DHI-007",
        "herb_active": "Filfil Siyah / Filfil Daraz (Piperine)",
        "allopathic_drug_class": "CYP3A4 & P-Glycoprotein Substrates (Phenytoin, Carbamazepine, Cyclosporine, Atorvastatin, Theophylline)",
        "severity": "HIGH",
        "clinical_effect": "Elevated pharmaceutical plasma concentrations and unexpected drug toxicity",
        "mechanism": "Piperine is a potent non-competitive inhibitor of hepatic Cytochrome P450 3A4 and intestinal P-glycoprotein efflux pumps, dramatically boosting oral bioavailability.",
        "management": "Therapeutic drug monitoring (TDM) recommended for narrow therapeutic index drugs (Phenytoin, Cyclosporine). Consider pharmaceutical dose reduction."
    },
    {
        "interaction_id": "DHI-008",
        "herb_active": "Kalonji (Nigella sativa / Thymoquinone) & Gurmar (Gymnema sylvestre)",
        "allopathic_drug_class": "Oral Hypoglycemic Agents (Sulfonylureas, Meglitinides) & Insulin",
        "severity": "HIGH",
        "clinical_effect": "Acute symptomatic hypoglycemia (diaphoresis, tremors, syncope)",
        "mechanism": "Additive pancreatic beta-cell insulin secretion and peripheral glucose uptake.",
        "management": "Advise continuous glucose monitoring (CGM) or fingerstick testing 4x daily. Anticipate lowering pharmaceutical secretagogue doses by 25-50%."
    },
    {
        "interaction_id": "DHI-009",
        "herb_active": "Asgandh (Withania somnifera / Withanolides)",
        "allopathic_drug_class": "Immunosuppressants (Cyclosporine, Tacrolimus, Azathioprine, Mycophenolate)",
        "severity": "HIGH",
        "clinical_effect": "Risk of allograft rejection or relapse of autoimmune flares",
        "mechanism": "Withanolides stimulate Th1 cell-mediated immunity and natural killer (NK) cell cytotoxicity, directly counteracting pharmacologic immunosuppression.",
        "management": "Strictly avoid in post-solid organ transplant recipients."
    },
    {
        "interaction_id": "DHI-010",
        "herb_active": "Kuchla Mudabbar (Strychnos nux-vomica / Strychnine)",
        "allopathic_drug_class": "CNS Stimulants (Amphetamines, Methylphenidate) & MAO Inhibitors",
        "severity": "CRITICAL",
        "clinical_effect": "Hyperreflexia, tetanic spasms, severe neurotoxicity, hypertensive crisis",
        "mechanism": "Competitive glycine receptor antagonism combined with sympathomimetic amine accumulation.",
        "management": "Strictly Schedule E-1 prescription only. Absolute contraindication with stimulants or MAOIs."
    },
    {
        "interaction_id": "DHI-011",
        "herb_active": "Suranjan Shirin (Colchicum autumnale / Colchicine)",
        "allopathic_drug_class": "Strong CYP3A4 / P-gp Inhibitors (Clarithromycin, Ketoconazole) & Statins",
        "severity": "CRITICAL",
        "clinical_effect": "Severe colchicine toxicity, fatal bone marrow suppression, rhabdomyolysis",
        "mechanism": "Inhibition of colchicine elimination pathway.",
        "management": "Purified pharmaceutical-standard botanical only. Contraindicated with macrolide antibiotics or severe renal failure."
    }
]

UNIVERSAL_CONTRAINDICATIONS: Dict[str, List[str]] = {
    "PREGNANCY": [
        "ZAY-001 (HyperCalm™ - contains Asrol / Reserpine - teratogenic risk)",
        "ZAY-004 (HepaClear™ - contains Revand Chini / emmenagogue anthraquinones)",
        "ZAY-007 (JointFree™ - contains Suranjan / Colchicine - antimitotic / teratogenic)",
        "ZAY-009 (Night-One X™ - contains Kuchla & animal derivatives)",
        "ZAY-017 (MetaboBurn-M™ - thermogenic metabolic modulation inappropriate in pregnancy)",
        "ZAY-018 (ThyroMet-W™ - thyroid stimulating guggulu)",
        "ZAY-023 (VigorX-ED™ - contains heavy metals Shingraf & Kuchla Mudabbar)"
    ],
    "LACTATION": [
        "ZAY-001 (Reserpine excreted in breast milk; causes neonatal nasal congestion & bradycardia)",
        "ZAY-007 (Colchicine passes into human milk)",
        "ZAY-023 (High potency heavy metal calxes contraindicated in nursing mothers)"
    ],
    "SEVERE_RENAL_IMPAIRMENT_EGFR_UNDER_30": [
        "ZAY-007 (JointFree™ - Colchicine accumulation risk)",
        "ZAY-015 (UroClear™ - mineral load / silicate clearance failure)",
        "ZAY-023 (VigorX-ED™ - cinnabar / mercurial trace excretion impaired)",
        "ZAY-024 (FertiMax-M™ - amino acid nitrogenous load)"
    ],
    "PRE_OPERATIVE_WASHOUT_7_DAYS": [
        "ZAY-003 (CardioGuard™ - contains high-dose Arjuna & Zafran)",
        "ZAY-005 (LipidClear™ - contains high-dose Allium sativum / Guggulu)",
        "ZAY-007 (JointFree™ - contains Boswellia serrata & Zingiber)",
        "ZAY-011 (Men Daily™ - contains Shilajit & Gokshura)"
    ]
}


# Known drug classes and representative active molecules
DRUG_SYNONYMS = {
    "antihypertensive": ["metoprolol", "atenolol", "amlodipine", "losartan", "telmisartan", "enalapril", "ramipril", "lisinopril", "hydrochlorothiazide", "propranolol", "diltiazem", "verapamil"],
    "anticoagulant": ["warfarin", "heparin", "apixaban", "rivaroxaban", "dabigatran", "aspirin", "clopidogrel", "ticagrelor"],
    "antidiabetic": ["metformin", "glimepiride", "glipizide", "gliclazide", "insulin", "sitagliptin", "vildagliptin", "dapagliflozin", "empagliflozin"],
    "cns_depressant": ["diazepam", "alprazolam", "lorazepam", "clonazepam", "zolpidem", "phenobarbital", "alcohol"],
    "immunosuppressant": ["cyclosporine", "tacrolimus", "azathioprine", "mycophenolate", "methotrexate", "prednisone"],
    "thyroid": ["levothyroxine", "eltroxin", "thyronorm", "liothyronine"]
}

SKU_TO_HERBS = {
    "ZAY-001": ["asrol", "rauwolfia", "reserpine", "filfil siyah", "piperine"],
    "ZAY-002": ["gurmar", "gymnema", "karela", "jamun"],
    "ZAY-003": ["zafran", "arjun", "terminalia"],
    "ZAY-004": ["kasni", "revand chini", "afsanteen"],
    "ZAY-005": ["guggulu", "lasan", "allium", "garlic", "zanjabil", "ginger"],
    "ZAY-006": ["asl-us-soos", "licorice", "glycyrrhiza"],
    "ZAY-007": ["suranjan", "colchicum", "colchicine", "kundur", "boswellia", "asgandh", "withania"],
    "ZAY-008": ["brahmi", "bacopa", "shankhpushpi"],
    "ZAY-009": ["kuchla", "strychnine", "zafran"],
    "ZAY-018": ["guggulu", "kanchnar"],
    "ZAY-023": ["kuchla", "strychnine", "shingraf", "zafran"]
}

def check_drug_herb_interactions(active_herbs_or_skus: List[str], medications: List[str]) -> List[Dict[str, Any]]:
    """
    Scans patient medication list against active herbs / SKUs.
    Returns matched interactions with clinical severity and management rules.
    """
    flagged = []
    meds_lower = [m.lower().strip() for m in medications]
    
    # Expand SKUs to their active herbs
    expanded_herbs = set()
    for item in active_herbs_or_skus:
        item_clean = item.strip().upper()
        if item_clean in SKU_TO_HERBS:
            for h in SKU_TO_HERBS[item_clean]:
                expanded_herbs.add(h.lower())
        else:
            expanded_herbs.add(item.lower())

    for item in MASTER_INTERACTIONS:
        herb_str = item["herb_active"].lower()
        drug_class_str = item["allopathic_drug_class"].lower()
        
        # Check if herb matches
        matched_herb = any(h in herb_str for h in expanded_herbs)
        if not matched_herb:
            continue
            
        # Check if drug matches directly or via drug class synonym
        matched_drug = False
        for med in meds_lower:
            if med in drug_class_str or any(w in drug_class_str for w in med.split()):
                matched_drug = True
                break
            # Check synonyms
            for cat, drug_list in DRUG_SYNONYMS.items():
                if any(syn in med for syn in drug_list) and cat in drug_class_str:
                    matched_drug = True
                    break
            if matched_drug:
                break
                
        if matched_herb and matched_drug:
            flagged.append(item)
            
    return flagged


def get_all_interactions() -> List[Dict[str, Any]]:
    """Returns complete drug-herb interaction registry."""
    return MASTER_INTERACTIONS


def get_universal_contraindications() -> Dict[str, List[str]]:
    """Returns universal contraindications by medical category."""
    return UNIVERSAL_CONTRAINDICATIONS
