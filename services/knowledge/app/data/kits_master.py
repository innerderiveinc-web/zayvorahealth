"""
ZAYVORA Health OS™ — Protocol Kits Master Knowledge Catalog
===========================================================
Contains all 21 Protocol Kits (K-01 to K-21) aligned with Clinical Protocols P-01 to P-21:
- 3-product clinical stacks
- Monthly pricing tiers (₹2,200 to ₹10,000/month)
- Target clinical indication and organ axis
- Regulatory composition (FSSAI Nutraceutical, AYUSH Classic, AYUSH Rx)
"""

from typing import Dict, Any, List, Optional

MASTER_KITS: Dict[str, Dict[str, Any]] = {
    "K-01": {
        "kit_id": "K-01",
        "name": "Diabetes Control Kit",
        "protocol_id": "P-01",
        "organ_axis": "PANCREATIC",
        "primary_indication": "Type 2 Diabetes Mellitus, Glycemic Dysregulation, Insulin Resistance",
        "products": [
            {"sku": "ZAY-004", "name": "HepaClear™", "role": "Hepatic insulin sensitization"},
            {"sku": "ZAY-002", "name": "DiabEase™", "role": "Beta-cell support & carbohydrate enzyme inhibition"},
            {"sku": "ZAY-008", "name": "MindBalance™", "role": "Cortisol dampening & stress hyperglycemia control"}
        ],
        "monthly_price_inr": 4500,
        "price_range_inr": "₹3,800 – ₹5,500",
        "regulatory_track": "AYUSH_CLASSICAL",
        "duration_weeks": 24,
        "is_prescription_required": False
    },
    "K-02": {
        "kit_id": "K-02",
        "name": "Metabolic Burn Kit",
        "protocol_id": "P-02",
        "organ_axis": "METABOLIC",
        "primary_indication": "Metabolic Syndrome, Visceral Adiposity, Sarcopenic Obesity",
        "products": [
            {"sku": "ZAY-004", "name": "HepaClear™", "role": "Hepatic detox & bile flow optimization"},
            {"sku": "ZAY-017", "name": "MetaboBurn-M™", "role": "Thermogenic lipolysis & ATP-citrate lyase inhibition"},
            {"sku": "ZAY-005", "name": "LipidClear™", "role": "Circulating atherogenic lipid clearance"}
        ],
        "monthly_price_inr": 4800,
        "price_range_inr": "₹4,000 – ₹6,000",
        "regulatory_track": "FSSAI_AYUSH_HYBRID",
        "duration_weeks": 24,
        "is_prescription_required": False
    },
    "K-03": {
        "kit_id": "K-03",
        "name": "Lipid Management Kit",
        "protocol_id": "P-03",
        "organ_axis": "METABOLIC",
        "primary_indication": "Atherogenic Dyslipidemia, Elevated LDL-C, Hypertriglyceridemia",
        "products": [
            {"sku": "ZAY-005", "name": "LipidClear™", "role": "HMG-CoA reductase modulation & reverse cholesterol transport"},
            {"sku": "ZAY-004", "name": "HepaClear™", "role": "Biliary excretion of cholesterol metabolites"},
            {"sku": "ZAY-003", "name": "CardioGuard™", "role": "Endothelial nitric oxide enhancement & antioxidant protection"}
        ],
        "monthly_price_inr": 4200,
        "price_range_inr": "₹3,500 – ₹5,000",
        "regulatory_track": "AYUSH_CLASSICAL",
        "duration_weeks": 24,
        "is_prescription_required": False
    },
    "K-04": {
        "kit_id": "K-04",
        "name": "Blood Pressure Kit (Rx)",
        "protocol_id": "P-04",
        "organ_axis": "CEREBROVASCULAR",
        "primary_indication": "Essential Hypertension, Vascular Resistance, Sympathetic Vasoconstriction",
        "products": [
            {"sku": "ZAY-001", "name": "HyperCalm™", "role": "Central sympatholytic & peripheral vasodilator (Rx Asrol)"},
            {"sku": "ZAY-003", "name": "CardioGuard™", "role": "Arterial compliance & inotropic support"},
            {"sku": "ZAY-008", "name": "MindBalance™", "role": "Baroreflex sensitivity & neuro-calmative balance"}
        ],
        "monthly_price_inr": 5500,
        "price_range_inr": "₹4,500 – ₹7,000",
        "regulatory_track": "AYUSH_SCHEDULE_E1_RX",
        "duration_weeks": 24,
        "is_prescription_required": True
    },
    "K-05": {
        "kit_id": "K-05",
        "name": "Cardiac Protection Kit",
        "protocol_id": "P-05",
        "organ_axis": "CARDIOVASCULAR",
        "primary_indication": "Post-MI Rehabilitation, Coronary Microvascular Dysfunction, Angina pectoris support",
        "products": [
            {"sku": "ZAY-003", "name": "CardioGuard™", "role": "Myocardial tonic & antioxidant preservation"},
            {"sku": "ZAY-005", "name": "LipidClear™", "role": "Plaque stabilization & lipid profile optimization"},
            {"sku": "ZAY-001", "name": "HyperCalm™", "role": "Afterload reduction & hemodynamic soothing"}
        ],
        "monthly_price_inr": 6800,
        "price_range_inr": "₹5,500 – ₹8,000",
        "regulatory_track": "AYUSH_SCHEDULE_E1_RX",
        "duration_weeks": 24,
        "is_prescription_required": True
    },
    "K-06": {
        "kit_id": "K-06",
        "name": "Stress-Anxiety Kit",
        "protocol_id": "P-06",
        "organ_axis": "NEUROPSYCHIATRIC",
        "primary_indication": "Generalized Anxiety Disorder, Chronic Burnout, Sympathetic Overactivity",
        "products": [
            {"sku": "ZAY-008", "name": "MindBalance™", "role": "HPA axis balancing & GABAergic neuroprotection"},
            {"sku": "ZAY-012", "name": "Sleep+Stress™", "role": "Somatic stress relief & evening relaxation"}
        ],
        "monthly_price_inr": 3000,
        "price_range_inr": "₹2,500 – ₹3,800",
        "regulatory_track": "FSSAI_AYUSH_HYBRID",
        "duration_weeks": 16,
        "is_prescription_required": False
    },
    "K-07": {
        "kit_id": "K-07",
        "name": "Sleep Restore Kit",
        "protocol_id": "P-07",
        "organ_axis": "NEUROPSYCHIATRIC",
        "primary_indication": "Chronic Primary Insomnia, Sleep Onset Latency, Fragmented Sleep Architecture",
        "products": [
            {"sku": "ZAY-012", "name": "Sleep+Stress™", "role": "Slow-wave sleep induction & GABA-A potentiation"},
            {"sku": "ZAY-008", "name": "MindBalance™", "role": "Daytime emotional stabilizing & circadian entrainment"}
        ],
        "monthly_price_inr": 2800,
        "price_range_inr": "₹2,200 – ₹3,500",
        "regulatory_track": "FSSAI_AYUSH_HYBRID",
        "duration_weeks": 12,
        "is_prescription_required": False
    },
    "K-08": {
        "kit_id": "K-08",
        "name": "Respiratory Care Kit",
        "protocol_id": "P-08",
        "organ_axis": "PULMONARY",
        "primary_indication": "Bronchial Asthma, Chronic Bronchitis, Post-Viral Airway Reactivity",
        "products": [
            {"sku": "ZAY-006", "name": "LungEase™", "role": "Bronchodilation, mucosal soothing & phlegm expectoration"},
            {"sku": "ZAY-021", "name": "Immunity™", "role": "Immunomodulation & systemic anti-inflammatory protection"}
        ],
        "monthly_price_inr": 3200,
        "price_range_inr": "₹2,800 – ₹4,000",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "duration_weeks": 16,
        "is_prescription_required": False
    },
    "K-09": {
        "kit_id": "K-09",
        "name": "Joint Care Kit",
        "protocol_id": "P-09",
        "organ_axis": "MUSCULOSKELETAL",
        "primary_indication": "Osteoarthritis, Degenerative Joint Disease, Cartilage Breakdown",
        "products": [
            {"sku": "ZAY-007", "name": "JointFree™", "role": "5-LOX inhibition, synovial decongestion & joint cushioning"},
            {"sku": "ZAY-021", "name": "Immunity™", "role": "Systemic antioxidant & matrix metalloproteinase reduction"}
        ],
        "monthly_price_inr": 3600,
        "price_range_inr": "₹3,000 – ₹4,500",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "duration_weeks": 24,
        "is_prescription_required": False
    },
    "K-10": {
        "kit_id": "K-10",
        "name": "ED Restore Kit (Rx)",
        "protocol_id": "P-10",
        "organ_axis": "ANDROLOGICAL",
        "primary_indication": "Severe Arteriogenic / Neurogenic Erectile Dysfunction, Impotence",
        "products": [
            {"sku": "ZAY-023", "name": "NeuroVigor-Rx™", "role": "Potent PDE5-independent pelvic perfusion & spinal reflex excitation (Rx)"},
            {"sku": "ZAY-027", "name": "AndroVora™", "role": "Leydig cell trophic support & free testosterone amplification"},
            {"sku": "ZAY-008", "name": "NeuroVora™", "role": "Performance anxiety mitigation & central dopaminergic tone"}
        ],
        "monthly_price_inr": 5450,
        "price_range_inr": "₹5,000 – ₹6,500",
        "regulatory_track": "AYUSH_SCHEDULE_E1_RX",
        "duration_weeks": 16,
        "is_prescription_required": True
    },
    "K-11": {
        "kit_id": "K-11",
        "name": "Male Fertility Kit",
        "protocol_id": "P-11",
        "organ_axis": "ANDROLOGICAL",
        "primary_indication": "Severe Oligo-Astheno-Teratozoospermia (OAT Syndrome), Sperm DNA Fragmentation",
        "products": [
            {"sku": "ZAY-024", "name": "SpermoVora™", "role": "Mitochondrial bioenergetics (CoQ10/L-Carnitine) & DNA integrity"},
            {"sku": "ZAY-010", "name": "NephroVora™", "role": "Spermatogenic epithelium nourishment & volume boost"},
            {"sku": "ZAY-025", "name": "ManiVital Pro™", "role": "Seminal plasma antioxidant buffer & liquefaction normalizing"}
        ],
        "monthly_price_inr": 5850,
        "price_range_inr": "₹5,000 – ₹7,000",
        "regulatory_track": "FSSAI_AYUSH_HYBRID",
        "duration_weeks": 24,
        "is_prescription_required": False
    },
    "K-12": {
        "kit_id": "K-12",
        "name": "Testosterone Restore Kit",
        "protocol_id": "P-12",
        "organ_axis": "ANDROLOGICAL",
        "primary_indication": "Late-Onset Hypogonadism, Andropause, Loss of Muscle Tone & Libido",
        "products": [
            {"sku": "ZAY-027", "name": "TestoVital Classic™", "role": "Gonadal steroidogenesis upregulation"},
            {"sku": "ZAY-011", "name": "Men Daily™", "role": "DHEA/testosterone precursor micro-nutrients & vigor"}
        ],
        "monthly_price_inr": 5800,
        "price_range_inr": "₹5,000 – ₹7,500",
        "regulatory_track": "AYUSH_CLASSICAL",
        "duration_weeks": 16,
        "is_prescription_required": False
    },
    "K-13": {
        "kit_id": "K-13",
        "name": "Prostate Health Kit",
        "protocol_id": "P-13",
        "organ_axis": "UROLOGICAL",
        "primary_indication": "Benign Prostatic Hyperplasia (Grade 1-2), Urinary Hesitancy, Nocturia",
        "products": [
            {"sku": "ZAY-026", "name": "ProstaGuard™", "role": "5-alpha reductase inhibition & stromal remodeling"},
            {"sku": "ZAY-015", "name": "UroClear™", "role": "Bladder neck spasmolytic & anti-crystalluria clearance"},
            {"sku": "ZAY-011", "name": "Men Daily™", "role": "Cellular antioxidant & systemic vitality"}
        ],
        "monthly_price_inr": 4200,
        "price_range_inr": "₹3,500 – ₹5,000",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "duration_weeks": 24,
        "is_prescription_required": False
    },
    "K-14": {
        "kit_id": "K-14",
        "name": "PCOS Kit",
        "protocol_id": "P-14",
        "organ_axis": "GYNECOLOGICAL",
        "primary_indication": "Polycystic Ovary Syndrome (PCOS/PCOD), Oligomenorrhea, Hyperandrogenism",
        "products": [
            {"sku": "ZAY-029", "name": "CycloCare-PCOS™", "role": "40:1 Inositol insulin sensitization & ovarian steroidogenesis"},
            {"sku": "ZAY-004", "name": "HepaClear™", "role": "Hepatic SHBG production & excess androgen clearance"},
            {"sku": "ZAY-008", "name": "MindBalance™", "role": "HPA axis moderating & stress cortisol suppression"}
        ],
        "monthly_price_inr": 5200,
        "price_range_inr": "₹4,500 – ₹6,500",
        "regulatory_track": "FSSAI_AYUSH_HYBRID",
        "duration_weeks": 24,
        "is_prescription_required": False
    },
    "K-15": {
        "kit_id": "K-15",
        "name": "Leucorrhoea Kit",
        "protocol_id": "P-15",
        "organ_axis": "GYNECOLOGICAL",
        "primary_indication": "Intractable Chronic Non-infective Leucorrhoea, Cervical Congestion",
        "products": [
            {"sku": "ZAY-028", "name": "LeucoClear™", "role": "Endocervical astringency, moisture control & tissue repair"},
            {"sku": "ZAY-016", "name": "FemCare-L™", "role": "Pelvic decongestion & vaginal barrier defense"},
            {"sku": "ZAY-019", "name": "Women Daily™", "role": "Hematinic & systemic mucosal rejuvenation"}
        ],
        "monthly_price_inr": 3800,
        "price_range_inr": "₹3,500 – ₹5,000",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "duration_weeks": 12,
        "is_prescription_required": False
    },
    "K-16": {
        "kit_id": "K-16",
        "name": "Cycle Care Kit",
        "protocol_id": "P-16",
        "organ_axis": "GYNECOLOGICAL",
        "primary_indication": "Dysmenorrhea, Irregular Menstrual Cycle, Pelvic Floor Cramping",
        "products": [
            {"sku": "ZAY-030", "name": "UterTone™", "role": "Myometrial spasmolytic tonic & luteal phase support"},
            {"sku": "ZAY-016", "name": "FemCare-L™", "role": "Pelvic circulatory rhythm"},
            {"sku": "ZAY-019", "name": "Women Daily™", "role": "Nutritional replenishment & hormonal balancing"}
        ],
        "monthly_price_inr": 3900,
        "price_range_inr": "₹3,200 – ₹4,800",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "duration_weeks": 16,
        "is_prescription_required": False
    },
    "K-17": {
        "kit_id": "K-17",
        "name": "Menopause Kit",
        "protocol_id": "P-17",
        "organ_axis": "GYNECOLOGICAL",
        "primary_indication": "Climacteric Syndrome, Vasomotor Flashes, Night Sweats, Osteopenia risk",
        "products": [
            {"sku": "ZAY-031", "name": "MenoPease™", "role": "Phytoestrogenic hypothalamic modulation & bone calcium"},
            {"sku": "ZAY-019", "name": "Women Daily™", "role": "General female vitality & adrenal adaptogen"},
            {"sku": "ZAY-003", "name": "CardioGuard™", "role": "Post-menopausal vascular endothelial preservation"}
        ],
        "monthly_price_inr": 5400,
        "price_range_inr": "₹4,500 – ₹7,000",
        "regulatory_track": "FSSAI_AYUSH_HYBRID",
        "duration_weeks": 24,
        "is_prescription_required": False
    },
    "K-18": {
        "kit_id": "K-18",
        "name": "Female Fertility Kit",
        "protocol_id": "P-18",
        "organ_axis": "GYNECOLOGICAL",
        "primary_indication": "Unexplained Female Subfertility, Oocyte Mitochondrial Deficit, Luteal Insufficiency",
        "products": [
            {"sku": "ZAY-032", "name": "FertiliWomen™", "role": "Oocyte bioenergetics (CoQ10/Folate) & follicular recruitment"},
            {"sku": "ZAY-029", "name": "CycloCare-PCOS™", "role": "Insulin-mediated ovulatory regularisation"},
            {"sku": "ZAY-030", "name": "UterTone™", "role": "Endometrial receptivity & implantation optimization"}
        ],
        "monthly_price_inr": 7600,
        "price_range_inr": "₹6,000 – ₹9,000",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "duration_weeks": 24,
        "is_prescription_required": False
    },
    "K-19": {
        "kit_id": "K-19",
        "name": "Immunity Shield Kit",
        "protocol_id": "P-19",
        "organ_axis": "IMMUNOLOGICAL",
        "primary_indication": "Recurrent Seasonal Viral Infections, Chronic Fatigue, Sluggish Immunity",
        "products": [
            {"sku": "ZAY-021", "name": "Immunity™", "role": "Natural killer cell activation & antioxidant shield"},
            {"sku": "ZAY-006", "name": "LungEase™", "role": "Respiratory tract epithelial barrier enhancement"}
        ],
        "monthly_price_inr": 2900,
        "price_range_inr": "₹2,500 – ₹3,500",
        "regulatory_track": "FSSAI_NUTRACEUTICAL",
        "duration_weeks": 12,
        "is_prescription_required": False
    },
    "K-20": {
        "kit_id": "K-20",
        "name": "Gut Restore Kit",
        "protocol_id": "P-20",
        "organ_axis": "GASTROINTESTINAL",
        "primary_indication": "Irritable Bowel Syndrome, Intestinal Dysbiosis, Post-Antibiotic Leaky Gut",
        "products": [
            {"sku": "ZAY-022", "name": "GutEase-IBS™", "role": "Mucosal barrier restoration & motility normalization"},
            {"sku": "ZAY-004", "name": "HepaClear™", "role": "Bile acid flow & digestive enzymatic stimulation"},
            {"sku": "ZAY-008", "name": "MindBalance™", "role": "Gut-brain axis signaling & visceral hypersensitivity reduction"}
        ],
        "monthly_price_inr": 3800,
        "price_range_inr": "₹3,000 – ₹4,500",
        "regulatory_track": "FSSAI_AYUSH_HYBRID",
        "duration_weeks": 16,
        "is_prescription_required": False
    },
    "K-21": {
        "kit_id": "K-21",
        "name": "Hair Restore Kit",
        "protocol_id": "P-21",
        "organ_axis": "DERMATOLOGICAL",
        "primary_indication": "Telogen Effluvium, Androgenetic Thinning, Follicular Dormancy",
        "products": [
            {"sku": "ZAY-014", "name": "HairRoot-X™", "role": "Anagen phase elongation & micro-circulation"},
            {"sku": "ZAY-019", "name": "Women Daily™", "role": "Nutritional ferritin & mineral fortification"},
            {"sku": "ZAY-008", "name": "MindBalance™", "role": "Stress-induced telogen shed prevention"}
        ],
        "monthly_price_inr": 3400,
        "price_range_inr": "₹2,800 – ₹4,000",
        "regulatory_track": "FSSAI_AYUSH_HYBRID",
        "duration_weeks": 24,
        "is_prescription_required": False
    }
}


def get_all_kits() -> List[Dict[str, Any]]:
    """Returns list of all 21 kits."""
    return list(MASTER_KITS.values())


def get_kit_by_id(kit_id: str) -> Optional[Dict[str, Any]]:
    """Returns specific kit by ID (e.g., K-01)."""
    return MASTER_KITS.get(kit_id.upper())


def get_kits_by_protocol(protocol_id: str) -> List[Dict[str, Any]]:
    """Finds kit matching protocol ID (e.g. P-01)."""
    p_id = protocol_id.upper()
    return [k for k in MASTER_KITS.values() if k.get("protocol_id", "").upper() == p_id]


def sync_kit_product_names():
    """Syncs product names within all kits to match master product branding."""
    try:
        from services.knowledge.app.data.products_master import MASTER_PRODUCTS
        for kit in MASTER_KITS.values():
            for p in kit.get("products", []):
                sku = p.get("sku")
                if sku in MASTER_PRODUCTS:
                    p["name"] = MASTER_PRODUCTS[sku]["name"]
    except Exception:
        pass


sync_kit_product_names()
