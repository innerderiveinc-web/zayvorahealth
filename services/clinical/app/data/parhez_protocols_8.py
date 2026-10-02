"""
ZAYVORA Health OS™ - 8 Complete Clinical Parhez Protocols
Reference: Parhez Compendium & Chapters 20-27,
ZAYVORA Clinical System — Volume II (2026), Dr. Irfan Ashraf, BUMS.

Implements the 8 verified clinical lifestyle prescriptions:
  1. MF-01: Male Fertility & Sexual Performance (Scrotal thermal, zero alcohol, 30g walnuts, 10PM sleep)
  2. PC-01: Female Hormonal / PCOS (Refined carb elimination, dairy limit, post-meal walk, Takmid)
  3. TM-01: Thyroid-Metabolic (Morning cortisol window exercise, warm food rule, cooked cruciferous only)
  4. NE-01: Neuro-Sleep / Stress Axis (Digital sunset 9:00 PM, fixed sleep/wake, morning sunlight 5 min)
  5. WM-01: Metabolic Weight Reset (16:8 IF 12PM-8PM, 10,000 steps/day, zero refined sugar for 90 days)
  6. FK-01: Fatty Liver / Hepatic Restoration (Absolute fructose elimination, 2 cups black coffee, cruciferous)
  7. ST-01: StoneGuard / Urolithiasis Metaphylaxis (2.5L fluid volume titration, lemon juice citrate, dietary calcium)
  8. RS-01: Respiratory & Balgham Clearance (Dairy elimination, warm fluids only, steam inhalation, HEPA air)
"""

from typing import Dict, Any, List, Optional

PARHEZ_PROTOCOLS_8: Dict[str, Dict[str, Any]] = {
    "MF-01": {
        "parhez_code": "MF-01",
        "name": "Male Fertility & Sexual Performance Parhez",
        "target_condition": "Oligospermia, Asthenospermia, Male Infertility, Psychogenic ED",
        "core_philosophy": "Parhez is a medical co-prescription. In spermatogenesis, thermal and oxidative hygiene accounts for 50% of treatment response.",
        "elements": [
            {
                "element": "Thermal Management",
                "prescription": "100% loose cotton underwear only. Cold water scrotal splash after shower (10 sec). No laptop on lap. No sauna/hot tub for 90 days.",
                "mechanism": "Spermatogenesis optimal at 34-35°C (2-3°C below core body temperature). 1°C sustained elevation reduces sperm count measurably."
            },
            {
                "element": "Sleep Architecture",
                "prescription": "Lights out by 10:30 PM. Wake at 6:00 AM. No screens after 9:30 PM. 7 days/week without weekend exceptions.",
                "mechanism": "70% of daily testosterone secretion occurs during slow-wave sleep (10 PM - 2 AM). 1 night of 5-hour sleep drops testosterone 10-15%."
            },
            {
                "element": "Alcohol Abstinence",
                "prescription": "Zero alcohol for 90 days minimum. Beer, wine, spirits all prohibited.",
                "mechanism": "Ethanol is a direct Leydig cell toxin. Acetaldehyde causes mitochondrial dysfunction and spikes Sperm DNA Fragmentation Index (DFI)."
            },
            {
                "element": "Dietary Foundation",
                "prescription": "30g walnuts daily (2 tablespoons). Oily fish 3x/week. 5-6 eggs/week. Eliminate all ultra-processed foods.",
                "mechanism": "DHA is incorporated into sperm plasma membrane for motility. Walnuts provide omega-3 ALA and antioxidant polyphenols."
            },
            {
                "element": "Exercise Prescription",
                "prescription": "35 min moderate aerobic exercise (brisk walk, cycling) 5 days/week. No anabolic steroids. No extreme marathon endurance.",
                "mechanism": "Moderate exercise improves testicular blood flow via nitric oxide without the cortisol-induced HPG suppression of extreme endurance."
            },
            {
                "element": "Stress Management",
                "prescription": "10-minute daily diaphragmatic breathing (4-in, 4-hold, 8-out). 1 full day/week without occupational cognitive demands.",
                "mechanism": "Cortisol is an HPG-axis chemical castrator. Prolonged exhale stimulates vagal brake on sympathetic overdrive."
            },
            {
                "element": "Sexual Activity Timing",
                "prescription": "Regular sexual activity every 2-4 days. Avoid prolonged abstinence beyond 7 days.",
                "mechanism": "Abstinence > 7 days increases epididymal sperm senescence and DNA fragmentation."
            }
        ]
    },
    "PC-01": {
        "parhez_code": "PC-01",
        "name": "Female Hormonal & PCOS Parhez",
        "target_condition": "PCOS, Anovulation, Menstrual Irregularity, Female Insulin Resistance",
        "core_philosophy": "Targeting the insulin-androgen-inflammatory triad. Every refined carbohydrate spike produces a proportional theca-cell androgen surge.",
        "elements": [
            {
                "element": "Carbohydrate Quality",
                "prescription": "Eliminate refined carbohydrates (white rice, white flour, added sugars, packaged snacks). Zero fruit juices — whole fruit only (1-2/day).",
                "mechanism": "Reduces postprandial insulin surges, downregulates ovarian theca-cell androgen synthesis, and elevates hepatic SHBG."
            },
            {
                "element": "Dairy Reduction",
                "prescription": "Maximum 1 serving/day. Eliminate cow's milk and whey protein. Favor fermented goat milk or curd.",
                "mechanism": "Bovine IGF-1 and insulinotropic dairy peptides cross-react with insulin receptors, worsening PCOS insulin resistance."
            },
            {
                "element": "Resistance Training",
                "prescription": "Minimum 3 sessions/week (30-40 min) of bodyweight or resistance training + 30 min brisk walking on other days.",
                "mechanism": "Upregulates skeletal muscle GLUT4 expression, creating an insulin-independent glucose sink."
            },
            {
                "element": "Post-Meal Walk",
                "prescription": "15-20 minute brisk walk after each main meal (especially lunch).",
                "mechanism": "Blunts postprandial glucose peaks by 20-30% via muscle contraction glucose uptake."
            },
            {
                "element": "Pelvic Circulation (Takmid)",
                "prescription": "Warm castor oil pack on lower abdomen for 20-30 min, 3x/week during non-menstrual phase.",
                "mechanism": "Classical Unani warm fomentation to enhance local microcirculation and resolve pelvic Balgham congestion."
            }
        ]
    },
    "TM-01": {
        "parhez_code": "TM-01",
        "name": "Thyroid-Metabolic Parhez",
        "target_condition": "Subclinical Hypothyroidism, Low T3 Syndrome, Hashimoto's Thyroiditis",
        "core_philosophy": "Supports hepatic T4-to-T3 deiodinase conversion and shields the thyroid gland from autoimmune and goitrogenic triggers.",
        "elements": [
            {
                "element": "Morning Exercise Timing",
                "prescription": "Moderate exercise (brisk walk, yoga Sun Salutations) within 90 minutes of waking (7-9 AM cortisol peak).",
                "mechanism": "Morning cortisol combined with light movement amplifies hepatic deiodinase enzyme activity converting T4 to active T3."
            },
            {
                "element": "Food Temperature Rule",
                "prescription": "No cold or iced food/beverages. Warm or room temperature only. Morning warm water with lemon and raw ginger.",
                "mechanism": "Cold suppresses Hararat-e-Ghariziya in the Jigar and reduces cytochrome P450 and deiodinase enzymatic velocity."
            },
            {
                "element": "Cruciferous Vegetable Preparation",
                "prescription": "Cook all cruciferous vegetables (broccoli, cabbage, cauliflower) at >70°C for 5+ min. Never consume raw in large amounts.",
                "mechanism": "Heat deactivates goitrogenic glucosinolates and thiocyanates that competitively inhibit thyroid iodine uptake."
            },
            {
                "element": "Selenium Food Source",
                "prescription": "3-4 Brazil nuts daily + sunflower seeds 2 tbsp/day.",
                "mechanism": "Saturates all three deiodinase isoforms (D1, D2, D3) and protects thyroid peroxidase from H2O2 oxidative damage."
            },
            {
                "element": "Iodine Strategy",
                "prescription": "Use iodized salt in cooking. DO NOT take supplemental high-dose iodine (especially if Anti-TPO positive).",
                "mechanism": "High-dose supplemental iodine triggers the Wolff-Chaikoff effect and accelerates thyroid autoimmune destruction in Hashimoto's."
            }
        ]
    },
    "NE-01": {
        "parhez_code": "NE-01",
        "name": "Neuro-Sleep & Circadian Hygiene Parhez",
        "target_condition": "Chronic Insomnia, HPA Axis Burnout, GAD, Performance Anxiety",
        "core_philosophy": "Circadian entrainment is non-negotiable biology. Melatonin cannot rise in the presence of evening blue light and elevated cortisol.",
        "elements": [
            {
                "element": "The Digital Sunset",
                "prescription": "All screens completely off by 9:00 PM. Phone kept outside bedroom. Paper reading or gentle music only.",
                "mechanism": "460-490 nm blue light suppresses pineal melatonin synthesis via retinal melanopsin ganglion cells."
            },
            {
                "element": "Fixed Sleep/Wake Rhythm",
                "prescription": "Same bedtime (10:00-10:30 PM) and wake time (6:00-6:30 AM) daily, including weekends.",
                "mechanism": "Varying sleep times by 2 hours produces social jet lag, impairs HPA negative feedback, and blunts the cortisol awakening response."
            },
            {
                "element": "Sunrise Exposure",
                "prescription": "Stand outside in morning sunlight for 10-15 minutes within 30 minutes of waking (no sunglasses).",
                "mechanism": "Direct photic input to the SCN anchors the cortisol peak, setting the biological timer for melatonin release 14-16 hours later."
            },
            {
                "element": "Afternoon Caffeine Cutoff",
                "prescription": "Zero caffeine (tea, coffee, cola) after 12:00 PM noon.",
                "mechanism": "Caffeine has a 5-7 hour half-life and competitively blocks adenosine receptors, fragmenting restorative slow-wave sleep."
            }
        ]
    },
    "WM-01": {
        "parhez_code": "WM-01",
        "name": "Metabolic Weight Reset Parhez",
        "target_condition": "Obesity, Insulin Resistance, Metabolic Syndrome, Central Adiposity",
        "core_philosophy": "Thawing the frozen metabolism. Insulin must reach true baseline to allow adipose tissue lipolysis.",
        "elements": [
            {
                "element": "16:8 Intermittent Fasting",
                "prescription": "Consistent eating window 12:00 PM to 8:00 PM. Fasting window: water, green tea, black coffee only.",
                "mechanism": "Fasting reduces 24-hr insulin area-under-the-curve by 20-30% and activates autophagic clearance of damaged organelles."
            },
            {
                "element": "The Elimination List",
                "prescription": "Zero refined sugar, white flour, packaged snacks, fruit juices, or commercial seed oils (sunflower, palm) for 90 days.",
                "mechanism": "Eliminates substrate for hepatic de novo lipogenesis and prevents trans-fat endotoxemic inflammation."
            },
            {
                "element": "Daily Movement Metric",
                "prescription": "10,000 steps daily minimum (tracked by pedometer/smartwatch).",
                "mechanism": "Frequent non-exercise physical activity keeps skeletal muscle GLUT4 transporters active independent of insulin."
            }
        ]
    },
    "FK-01": {
        "parhez_code": "FK-01",
        "name": "Fatty Liver & Hepatic Restoration Parhez",
        "target_condition": "NAFLD Grade I-III, NASH, Elevated Transaminases (ALT/AST)",
        "core_philosophy": "Removing the hepatic burden. Fructose is metabolized exclusively by the liver into fat.",
        "elements": [
            {
                "element": "Fructose Elimination",
                "prescription": "Absolute zero added sugar, high-fructose corn syrup, packaged juices, and sodas. Whole fresh fruit limited to 1-2 pieces/day.",
                "mechanism": "Fructose bypasses phosphofructokinase regulation, driving uninhibited hepatic de novo lipogenesis."
            },
            {
                "element": "Zero Alcohol",
                "prescription": "Complete alcohol abstinence for the duration of liver restoration.",
                "mechanism": "Ethanol and NAFLD share identical toxic oxidative pathways; even low doses accelerate fibrosis progression."
            },
            {
                "element": "Therapeutic Coffee",
                "prescription": "2 cups of black coffee daily (no sugar, no milk).",
                "mechanism": "Chlorogenic acid in coffee activates Nrf2 and stimulates hepatic autophagy, reducing NAFLD progression risk by 40%."
            },
            {
                "element": "Daily Cruciferous Greens",
                "prescription": "Cooked broccoli, cauliflower, or Brussels sprouts daily (minimum 150g).",
                "mechanism": "Sulforaphane acts as a potent Nrf2 activator, working synergistically with Silymarin."
            }
        ]
    },
    "ST-01": {
        "parhez_code": "ST-01",
        "name": "StoneGuard Urolithiasis Metaphylaxis Parhez",
        "target_condition": "Renal Calculi (Calcium Oxalate, Uric Acid), Recurrent Nephrolithiasis",
        "core_philosophy": "Dilution, diversion, and metabolic crystal inhibition to break the 50% 5-year stone recurrence cycle.",
        "elements": [
            {
                "element": "Fluid Volume Titration",
                "prescription": "Minimum 2.5L fluid daily. Target: pale yellow to clear urine. Distribute in five 500mL servings across the day.",
                "mechanism": "Decreases urinary mineral concentrations below the supersaturation crystallization threshold."
            },
            {
                "element": "Fresh Lemon Juice Citrate Strategy",
                "prescription": "Fresh lemon juice in water (2-3 tablespoons daily).",
                "mechanism": "Increases urinary citrate, which chelates free calcium and directly inhibits calcium oxalate nucleation."
            },
            {
                "element": "Dietary Oxalate Management",
                "prescription": "Reduce high-oxalate foods (spinach, beets, chocolate, peanuts, strong tea). DO NOT restrict dietary calcium.",
                "mechanism": "Dietary calcium binds oxalate in the intestine, excreting it in stool rather than absorbing it into urine."
            }
        ]
    },
    "RS-01": {
        "parhez_code": "RS-01",
        "name": "Respiratory & Balgham Clearance Parhez",
        "target_condition": "Allergic Rhinitis, Chronic Sinusitis, Productive Cough, Mild-Moderate Asthma",
        "core_philosophy": "Eliminates mucosal Balgham congestion and stabilizes airway immune mast cells.",
        "elements": [
            {
                "element": "Dairy & Cold Food Elimination",
                "prescription": "Zero cold dairy, ice cream, or refrigerated drinks. All fluids room temperature or warm.",
                "mechanism": "Cold dairy increases mucus viscosity and stimulates goblet cell hyperplasia in Balgham constitutions."
            },
            {
                "element": "Steam Inhalation (Bukhūr)",
                "prescription": "Steam inhalation with 2 drops eucalyptus/Nilgiri oil for 2 minutes twice daily.",
                "mechanism": "Liquefies bronchial mucus polymers and improves mucociliary escalator clearance velocity."
            },
            {
                "element": "Nasal Hygiene (Jal Neti)",
                "prescription": "Isotonic saline nasal rinse morning and evening.",
                "mechanism": "Flushes aeroallergens and inflammatory cytokines directly from the sinonasal mucosa."
            }
        ]
    }
}


def get_all_parhez() -> List[Dict[str, Any]]:
    return list(PARHEZ_PROTOCOLS_8.values())


def get_parhez_by_code(code: str) -> Optional[Dict[str, Any]]:
    return PARHEZ_PROTOCOLS_8.get(code.upper())
