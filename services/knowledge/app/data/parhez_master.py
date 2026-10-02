"""
ZAYVORA Health OS™ — Parhez (Lifestyle & Dietary) Master Knowledge Catalog
=========================================================================
Contains all 8 Canonical Parhez Protocols rooted in Classical Unani Asbab-e-Sitta
Zarooriya (Six Essential Prerequisites of Life) cross-referenced with modern
chronobiology, metabolic endocrinology, and nutritional science:
- MF-01: Male Fertility Parhez
- PC-01: PCOS Lifestyle & Insulin Reset
- TM-01: Thyroid-Metabolic Circadian Reset
- NE-01: Neuro-Sleep & Cortisol Reset
- WM-01: Metabolic Reset & Weight Optimization
- FK-01: Hepatobiliary Reset & Fatty Liver Protocol
- ST-01: Nephrolithiasis & Urological StoneGuard
- Resp-01: Pulmonary & Respiratory Decongestion
"""

from typing import Dict, Any, List, Optional

MASTER_PARHEZ: Dict[str, Dict[str, Any]] = {
    "MF-01": {
        "code": "MF-01",
        "name": "Male Fertility & Spermatogenesis Parhez",
        "classical_principle": "Hifz-e-Mani & Taskeen-e-Hararat-e-Khusyatain (Preservation of Semen & Testicular Cooling)",
        "target_axes": ["ANDROLOGICAL"],
        "duration_days": 90,
        "rules": [
            {
                "category": "Thermal Regulation",
                "instruction": "Strict testicular cooling: Wear 100% loose breathable cotton boxer shorts. Strictly avoid hot tubs, thermal baths, saunas, and resting laptop directly on lap.",
                "scientific_rationale": "Spermatogenic enzymes undergo denaturation at temperatures above 34.5°C; elevated scrotal heat directly increases DNA fragmentation index."
            },
            {
                "category": "Circadian & Sleep",
                "instruction": "Sleep strictly between 10:00 PM and 6:00 AM (8 continuous hours in total darkness).",
                "scientific_rationale": "Peak nocturnal melatonin secretion scavenges reactive oxygen species in testicular Leydig and Sertoli cells."
            },
            {
                "category": "Toxicology & Abstinence",
                "instruction": "Zero alcohol, zero cigarette/tobacco/vape nicotine, zero recreational drugs for minimum 90-120 days.",
                "scientific_rationale": "Nicotine and ethanol induce testicular microvascular ischemia and profound teratozoospermia."
            },
            {
                "category": "Nutritional Additions",
                "instruction": "Consume 30g raw walnuts daily and wild oily fish (or flaxseed + algae DHA) 3 times weekly.",
                "scientific_rationale": "Alpha-linolenic acid (ALA) and DHA integrate into sperm plasma membrane, restoring vital membrane fluidity and progressive motility."
            },
            {
                "category": "Autonomic Nervous System",
                "instruction": "Perform 4-7-8 breathing exercises (Inhale 4s, Hold 7s, Exhale 8s) for 10 minutes twice daily.",
                "scientific_rationale": "Vagal nerve stimulation reduces sympathetic vasoconstriction to internal pudendal and testicular arteries."
            }
        ]
    },
    "PC-01": {
        "code": "PC-01",
        "name": "PCOS Lifestyle & Insulin Reset Parhez",
        "classical_principle": "Tanqia-e-Balgham & Fath-e-Sudad-e-Reham (Phlegm Decongestion & Uterine De-obstruction)",
        "target_axes": ["GYNECOLOGICAL", "METABOLIC"],
        "duration_days": 180,
        "rules": [
            {
                "category": "Carbohydrate Architecture",
                "instruction": "Eliminate all refined sugars, white flour, fruit juices, and high-glycemic starches (daily glycemic load < 45).",
                "scientific_rationale": "Hyperinsulinemia directly stimulates the ovarian theca cells to overproduce androgens and suppresses hepatic SHBG."
            },
            {
                "category": "Dairy Modulation",
                "instruction": "Restrict conventional dairy to <= 1 serving per day of A2 fermented kefir or sheep/goat yogurt.",
                "scientific_rationale": "Insulin-like growth factor-1 (IGF-1) present in commercial bovine dairy exacerbates follicular arrest and cystic transformation."
            },
            {
                "category": "Physical Resistance",
                "instruction": "Perform 3 sessions weekly of progressive strength resistance training (compound multi-joint exercises).",
                "scientific_rationale": "Skeletal muscle GLUT-4 translocation occurs independently of insulin during resistance contraction, dramatically reducing systemic insulin resistance."
            },
            {
                "category": "Postprandial Protocol",
                "instruction": "Undertake a 15-20 minute brisk walk immediately following the two main meals of the day.",
                "scientific_rationale": "Post-meal light ambulation attenuates peak postprandial glucose excursions by up to 35%."
            },
            {
                "category": "Pelvic Circulation",
                "instruction": "Apply warm castor oil packs over the lower abdomen for 45 minutes, 3 times weekly (strictly outside of menstrual bleeding days).",
                "scientific_rationale": "Ricinoleic acid promotes local lymphatic drainage and softens congested pelvic adhesions."
            }
        ]
    },
    "TM-01": {
        "code": "TM-01",
        "name": "Thyroid-Metabolic Circadian Reset Parhez",
        "classical_principle": "In'ash-e-Hararat-e-Ghariziya (Revival of Innate Metabolic Heat)",
        "target_axes": ["ENDOCRINE", "METABOLIC"],
        "duration_days": 120,
        "rules": [
            {
                "category": "Morning Photobiology",
                "instruction": "Expose eyes and face to outdoor natural sunlight within 30 minutes of waking for 10-15 minutes.",
                "scientific_rationale": "Photonic entrainment of the suprachiasmatic nucleus (SCN) coordinates the hypothalamic TRH and pituitary TSH pulsatility."
            },
            {
                "category": "Thermal Dietetics",
                "instruction": "Consume exclusively warm, cooked, aromatic foods; avoid raw refrigerated meals and ice-cold water.",
                "scientific_rationale": "Conserves digestive enzymatic energy (*Hararat-e-Ghariziya*) and prevents gastrointestinal transit sluggishness."
            },
            {
                "category": "Goitrogen Deactivation",
                "instruction": "All cruciferous vegetables (broccoli, cabbage, cauliflower, kale) must be thoroughly steamed or boiled before consumption.",
                "scientific_rationale": "Thermal cooking deactivates myrosinase enzymes, preventing the release of goitrin which competitively inhibits thyroidal iodide uptake."
            },
            {
                "category": "Trace Mineral Fortification",
                "instruction": "Eat exactly 2 Brazil nuts daily (provides 100-200 mcg organic selenomethionine).",
                "scientific_rationale": "Selenium is the essential cofactor for iodothyronine deiodinase enzymes responsible for converting inactive T4 to bioactive T3."
            },
            {
                "category": "Supplement Caution",
                "instruction": "Do not consume high-dose iodine or kelp supplements unless specifically prescribed by a physician.",
                "scientific_rationale": "Excessive iodine can precipitate the Wolff-Chaikoff effect or trigger severe autoimmune thyroid flares in Hashimoto's patients."
            }
        ]
    },
    "NE-01": {
        "code": "NE-01",
        "name": "Neuro-Sleep & Cortisol Reset Parhez",
        "classical_principle": "Taskeen-e-Ruh & Ta'deel-e-Khafqan (Calming of Vital Spirit & Nervous Equilibrium)",
        "target_axes": ["NEUROPSYCHIATRIC"],
        "duration_days": 60,
        "rules": [
            {
                "category": "Digital Sunset",
                "instruction": "Implement strict digital curfew at 9:00 PM: All LED screens, phones, laptops, and bright overhead blue lighting powered off.",
                "scientific_rationale": "Short-wavelength 480nm blue light suppresses pineal melatonin secretion and maintains evening cortisol elevation."
            },
            {
                "category": "Circadian Consistency",
                "instruction": "Maintain an identical bedtime and wake time 7 days a week within a maximum variance of +/- 30 minutes.",
                "scientific_rationale": "Consistent sleep schedules stabilize the central circadian pacemaker and consolidate restorative slow-wave delta sleep."
            },
            {
                "category": "Adenosine Clearance & Caffeine",
                "instruction": "Absolute zero caffeine (coffee, black tea, energy drinks, colas) after 12:00 PM noon.",
                "scientific_rationale": "Caffeine has a 5-7 hour half-life; competitive blockade of adenosine A1 receptors in the ventrolateral preoptic nucleus impedes sleep architecture."
            },
            {
                "category": "Thermal Pre-Sleep Protocol",
                "instruction": "Take a warm shower or foot soak with Epsom salts (magnesium sulfate) 60 minutes before bed.",
                "scientific_rationale": "Peripheral vasodilation causes rapid core body temperature cooling, which is the physiological trigger for sleep onset."
            }
        ]
    },
    "WM-01": {
        "code": "WM-01",
        "name": "Metabolic Reset & Weight Optimization Parhez",
        "classical_principle": "Qat-e-Shahm & Taqlil-e-Ghiza (Adipose Dissolution & Caloric Restraint)",
        "target_axes": ["METABOLIC", "HEPATOBILIARY"],
        "duration_days": 90,
        "rules": [
            {
                "category": "Time-Restricted Feeding",
                "instruction": "Adopt a 16:8 Intermittent Fasting schedule with daily eating window strictly from 12:00 PM to 8:00 PM.",
                "scientific_rationale": "16 hours of daily fasting lowers circulating insulin, triggers hepatic autophagy, and upregulates fatty acid beta-oxidation."
            },
            {
                "category": "Refined Calorie Elimination",
                "instruction": "Strictly eliminate all refined grains, seed oils (sunflower, soybean, corn), and commercial snacks.",
                "scientific_rationale": "High omega-6 to omega-3 ratios promote chronic macrophage infiltration of visceral adipose tissue and systemic inflammation."
            },
            {
                "category": "Daily Non-Exercise Physical Activity",
                "instruction": "Achieve a minimum of 10,000 steps daily distributed across morning, afternoon, and evening.",
                "scientific_rationale": "Non-Exercise Activity Thermogenesis (NEAT) accounts for the largest fraction of variable daily energy expenditure."
            },
            {
                "category": "Hydration Volume",
                "instruction": "Drink 35 ml per kg body weight of warm or ambient temperature water throughout daylight hours.",
                "scientific_rationale": "Adequate cellular hydration prevents misinterpretation of thirst as hunger and assists renal elimination of metabolic end-products."
            }
        ]
    },
    "FK-01": {
        "code": "FK-01",
        "name": "Hepatobiliary Reset & Fatty Liver Parhez",
        "classical_principle": "Tanqia-e-Jigar & Daf-e-Dasaumat (Hepatic Decontamination & Lipid Washout)",
        "target_axes": ["HEPATOBILIARY", "METABOLIC"],
        "duration_days": 180,
        "rules": [
            {
                "category": "Fructose Abstinence",
                "instruction": "Strictly eliminate all industrial high-fructose corn syrup, sweetened beverages, honey in large amounts, and fruit juices.",
                "scientific_rationale": "Hepatic fructokinase metabolizes fructose unrestrained by ATP negative feedback, converting it directly into toxic intrahepatic triglycerides via de novo lipogenesis."
            },
            {
                "category": "Absolute Alcohol Abstinence",
                "instruction": "Zero alcohol intake for a minimum of 180 days.",
                "scientific_rationale": "Ethanol induces mitochondrial reactive oxygen species in hepatocytes and accelerates progression from steatosis to steatohepatitis (MASH)."
            },
            {
                "category": "Bioactive Coffee Consumption",
                "instruction": "Consume 2 cups of unsweetened black filtered coffee daily (unless contraindicated by severe cardiac arrhythmia).",
                "scientific_rationale": "Caffeine and chlorogenic acid stimulate hepatic autophagy and are clinically demonstrated to reduce liver stiffness and fibrosis scores."
            },
            {
                "category": "Bitter Botanical Dietetics",
                "instruction": "Incorporate daily bitter greens: Cichorium (Kasni), dandelion greens, mustard greens, arugula, or fresh radish.",
                "scientific_rationale": "Bitters stimulate cholecystokinin release, enhance bile acid excretion, and decongest intrahepatic biliary canaliculi."
            },
            {
                "category": "Protein Sourcing",
                "instruction": "Limit red meat to <= 1 serving every 2 weeks; prioritize wild fish, lentils, and sprouted pulses.",
                "scientific_rationale": "High intake of saturated fat and heme iron in red meat increases hepatic oxidative stress and worsens insulin resistance."
            }
        ]
    },
    "ST-01": {
        "code": "ST-01",
        "name": "Nephrolithiasis (StoneGuard) Parhez",
        "classical_principle": "Taflis-e-Hisat & Tanqia-e-Majari-e-Baul (Stone Fragmentation & Urinary Tract Cleansing)",
        "target_axes": ["UROLOGICAL"],
        "duration_days": 90,
        "rules": [
            {
                "category": "Hydration Target",
                "instruction": "Drink at least 2.5 to 3.0 Liters of water daily to maintain a 24-hour urine output exceeding 2.0 Liters.",
                "scientific_rationale": "Dilution decreases urinary supersaturation of calcium oxalate, uric acid, and calcium phosphate below crystallization thresholds."
            },
            {
                "category": "Citrate Alkalinization",
                "instruction": "Drink freshly squeezed lemon juice (from 2 whole lemons) in warm water twice daily.",
                "scientific_rationale": "Citrate binds free calcium in the urinary lumen, forming a soluble calcium citrate complex and inhibiting crystal nucleation and agglomeration."
            },
            {
                "category": "Oxalate Modulation",
                "instruction": "Restrict high-oxalate foods: Avoid spinach, Swiss chard, rhubarb, beets, dark chocolate, and excessive almonds.",
                "scientific_rationale": "Hyperoxaluria is a potent driver of calcium oxalate monohydrate (whewellite) stone precipitation."
            },
            {
                "category": "Calcium Maintenance",
                "instruction": "Do NOT restrict dietary calcium; consume normal dietary calcium (yogurt, paneer, sesame) with meals.",
                "scientific_rationale": "Dietary calcium binds free oxalate in the gastrointestinal tract, forming insoluble calcium oxalate that is excreted in feces rather than absorbed into circulation."
            },
            {
                "category": "Sodium Restriction",
                "instruction": "Limit dietary sodium intake to < 2000 mg/day (under 1 level teaspoon of table salt).",
                "scientific_rationale": "High proximal tubular sodium reabsorption is linked to calcium excretion; reducing sodium decreases urinary calcium excretion."
            }
        ]
    },
    "Resp-01": {
        "code": "Resp-01",
        "name": "Pulmonary & Airway Decongestion Parhez",
        "classical_principle": "Tanqiya-e-Sadr & Tahleel-e-Balgham (Chest Clearance & Phlegm Liquefaction)",
        "target_axes": ["PULMONARY"],
        "duration_days": 60,
        "rules": [
            {
                "category": "Mucogenic Food Avoidance",
                "instruction": "Eliminate cold milk, ice cream, aged cheeses, deep-fried snacks, and heavy sour curds.",
                "scientific_rationale": "Cold temperature and dairy casein increase oropharyngeal and tracheobronchial mucus viscosity in susceptible individuals."
            },
            {
                "category": "Warm Demulcent Hydration",
                "instruction": "Sip warm water infused with fresh ginger, tulsi leaves, and licorice throughout the day.",
                "scientific_rationale": "Warm fluids enhance tracheobronchial ciliary beat frequency and promote mucociliary clearance."
            },
            {
                "category": "Inhalational Aromatherapy",
                "instruction": "Perform steam inhalation with 2 drops of eucalyptus oil or mint extract for 10 minutes each evening before sleep.",
                "scientific_rationale": "Volatile cineole and menthol act on TRPM8 sensory receptors to produce subjective airway patency and antibacterial action."
            },
            {
                "category": "Upper Airway Cleansing",
                "instruction": "Practice morning nasal saline irrigation (Jal Neti) using isotonic lukewarm sterile saline.",
                "scientific_rationale": "Removes entrapped particulate matter, allergens, and inflammatory cytokines from the sinonasal mucosa."
            }
        ]
    }
}


def get_all_parhez() -> List[Dict[str, Any]]:
    """Returns list of all 8 Parhez protocols."""
    return list(MASTER_PARHEZ.values())


def get_parhez_by_code(code: str) -> Optional[Dict[str, Any]]:
    """Returns specific Parhez protocol by code (e.g., MF-01)."""
    c = code.lower().strip()
    for k, v in MASTER_PARHEZ.items():
        if k.lower() == c or v.get("code", "").lower() == c:
            return v
    return None


def get_parhez_for_axis(axis_code: str) -> List[Dict[str, Any]]:
    """Finds all Parhez protocols applicable to a given organ axis."""
    axis_upper = axis_code.upper()
    return [p for p in MASTER_PARHEZ.values() if axis_upper in [a.upper() for a in p.get("target_axes", [])]]
