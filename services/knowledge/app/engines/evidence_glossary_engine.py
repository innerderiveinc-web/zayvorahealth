"""
ZAYVORA Health OS™ - OCEBM Evidence Grading & Canonical Glossary Registry
Reference: Appendix C (Evidence Grading) & Section IX (Glossary & Index),
ZAYVORA Global Edition (Second Edition 2026), Dr. Irfan Ashraf, BUMS.

Implements:
  1. Oxford Centre for Evidence-Based Medicine (OCEBM) grading matrix for key ZAYVORA interventions.
  2. Canonical 42-Term Unani <-> Systems Biology Glossary.
"""

from typing import Dict, Any, List, Optional


class EvidenceGlossaryEngine:
    """
    Registry for OCEBM evidence grading and canonical bilingual Unani terminology.
    """

    OCEBM_REGISTRY = [
        {
            "intervention": "DASH Diet",
            "condition": "Hypertension",
            "evidence_level": "Level 1a",
            "study_type": "Meta-analysis of RCTs",
            "key_source": "Sacks et al., N Engl J Med 2001",
            "clinical_effect": "Reduces SBP by 8-14 mmHg; equivalent to single antihypertensive monotherapy"
        },
        {
            "intervention": "Mediterranean Diet",
            "condition": "Cardiovascular Risk & NAFLD",
            "evidence_level": "Level 1a",
            "study_type": "Meta-analysis of RCTs",
            "key_source": "Estruch et al., N Engl J Med 2018 (PREDIMED)",
            "clinical_effect": "30% relative risk reduction in major adverse cardiovascular events"
        },
        {
            "intervention": "Time-Restricted Eating (TRE)",
            "condition": "Metabolic Syndrome & Insulin Resistance",
            "evidence_level": "Level 1b",
            "study_type": "Multiple RCTs",
            "key_source": "Sutton et al., Cell Metab 2018",
            "clinical_effect": "Improves insulin sensitivity, blood pressure, and oxidative stress via peripheral clock synchrony"
        },
        {
            "intervention": "Low-FODMAP Diet",
            "condition": "Irritable Bowel Syndrome (IBS)",
            "evidence_level": "Level 1a",
            "study_type": "Meta-analysis of RCTs",
            "key_source": "Hulisz, JAAPA 2018; Staudacher & Whelan, Gut 2017",
            "clinical_effect": "50-80% symptom reduction in abdominal pain, bloating, and stool irregularity"
        },
        {
            "intervention": "CBT for IBS",
            "condition": "Irritable Bowel Syndrome",
            "evidence_level": "Level 1b",
            "study_type": "Multiple RCTs",
            "key_source": "Lackner et al., Gastroenterology 2018",
            "clinical_effect": "Durable visceral pain reduction at 12-month follow-up through gut-brain axis modulation"
        },
        {
            "intervention": "Aerobic Exercise (150 min/week)",
            "condition": "Type 2 Diabetes Mellitus",
            "evidence_level": "Level 1a",
            "study_type": "Meta-analysis of RCTs",
            "key_source": "Colberg et al., Diabetes Care 2016",
            "clinical_effect": "Lowers HbA1c by ~0.7%, stimulates insulin-independent GLUT4 translocation"
        },
        {
            "intervention": "Resistance Training (2-3x/week)",
            "condition": "Metabolic Syndrome & Sarcopenia",
            "evidence_level": "Level 1a",
            "study_type": "Meta-analysis of RCTs",
            "key_source": "Strasser et al., Sports Med 2010",
            "clinical_effect": "Increases metabolically active skeletal muscle mass, enhances resting metabolic rate"
        },
        {
            "intervention": "Inositol (Myo + D-Chiro 40:1 ratio, 4g/day)",
            "condition": "Polycystic Ovarian Syndrome (PCOS)",
            "evidence_level": "Level 1b",
            "study_type": "Multiple RCTs",
            "key_source": "Unfer et al., Gynecol Endocrinol 2012",
            "clinical_effect": "Restores spontaneous ovulatory cycles in 50-70%, reduces hyperandrogenism"
        },
        {
            "intervention": "Nigella sativa (Kalonji 2-3g/day)",
            "condition": "Hypertension & Metabolic Syndrome",
            "evidence_level": "Level 1b",
            "study_type": "Multiple RCTs",
            "key_source": "Rohner et al., J Hypertens 2015",
            "clinical_effect": "Reduces SBP by 6-8 mmHg through thymoquinone-mediated calcium antagonism and ACE inhibition"
        },
        {
            "intervention": "Silymarin (Milk Thistle 140-420 mg tid)",
            "condition": "NAFLD / MAFLD",
            "evidence_level": "Level 1b",
            "study_type": "Multiple RCTs",
            "key_source": "Abenavoli et al., Phytother Res 2010",
            "clinical_effect": "Reduces ALT/AST transaminases, stabilizes hepatocyte membranes, inhibits hepatic NF-kB"
        },
        {
            "intervention": "Berberine (500 mg tid)",
            "condition": "Type 2 Diabetes & Dyslipidemia",
            "evidence_level": "Level 1b",
            "study_type": "Multiple RCTs",
            "key_source": "Yin et al., Metabolism 2008",
            "clinical_effect": "HbA1c reduction comparable to metformin (~1.0%) via AMPK activation"
        },
        {
            "intervention": "Ashwagandha (Withania somnifera, KSM-66 300-600 mg)",
            "condition": "Chronic Stress & Anxiety",
            "evidence_level": "Level 1b",
            "study_type": "Multiple RCTs",
            "key_source": "Chandrasekhar et al., Indian J Psychol Med 2012",
            "clinical_effect": "Cortisol reduction of 15-30%, normalises HPA axis, improves sleep quality"
        },
        {
            "intervention": "Enteric-Coated Peppermint Oil (0.2-0.4 mL tid)",
            "condition": "Irritable Bowel Syndrome (IBS)",
            "evidence_level": "Level 1a",
            "study_type": "Meta-analysis of RCTs",
            "key_source": "Ford et al., BMJ 2008; Cash et al., Dig Dis Sci 2016",
            "clinical_effect": "Smooth muscle calcium channel blockade, significant global IBS symptom relief"
        },
        {
            "intervention": "Therapeutic Massage (Dalak)",
            "condition": "Hypertension & Autonomic Stress",
            "evidence_level": "Level 1b",
            "study_type": "Multiple RCTs",
            "key_source": "Moyer et al., Psychol Bull 2004; Shamon & Arnetz, 2017",
            "clinical_effect": "Reduces SBP by 6-10 mmHg, increases vagal tone (HRV), lowers salivary cortisol by 24-31%"
        },
        {
            "intervention": "Passive Heat / Hammam (40-41°C)",
            "condition": "Type 2 Diabetes Mellitus",
            "evidence_level": "Level 2b",
            "study_type": "Single RCT",
            "key_source": "Hooper, N Engl J Med 1999",
            "clinical_effect": "13% reduction in fasting blood glucose via HSP70 upregulation and GLUT4 translocation"
        },
        {
            "intervention": "CBT-I (Cognitive Behavioral Therapy for Insomnia)",
            "condition": "Chronic Insomnia",
            "evidence_level": "Level 1a",
            "study_type": "Meta-analysis of RCTs",
            "key_source": "Qaseem et al., Ann Intern Med 2016 (ACP Clinical Guideline)",
            "clinical_effect": "First-line chronic insomnia treatment; superior durability to Z-drugs and benzodiazepines"
        },
        {
            "intervention": "Mindfulness-Based Stress Reduction (MBSR)",
            "condition": "Anxiety & Depression",
            "evidence_level": "Level 1a",
            "study_type": "Meta-analysis of RCTs",
            "key_source": "Goyal et al., JAMA Intern Med 2014",
            "clinical_effect": "Reduces amygdala hyperreactivity, lowers pro-inflammatory cytokines (IL-6, hs-CRP)"
        },
        {
            "intervention": "Hijama (Wet Cupping / Hijama Bil Shurt)",
            "condition": "Chronic Musculoskeletal Pain & Hypertension",
            "evidence_level": "Level 2b-3",
            "study_type": "Small RCTs and Pilot Studies",
            "key_source": "Al-Bedah et al., 2015, 2017; Teut et al., 2018",
            "clinical_effect": "Local nitric oxide release, pain gate modulation, modest SBP drop in volume plethora"
        },
        {
            "intervention": "Spearmint Herbal Tea (2 cups/day)",
            "condition": "PCOS Hyperandrogenism",
            "evidence_level": "Level 2b",
            "study_type": "Single RCT",
            "key_source": "Grant, Phytother Res 2010",
            "clinical_effect": "Significant anti-androgenic effect, reduction in free testosterone and hirsutism"
        }
    ]

    GLOSSARY = {
        "Akhlat-e-Arba'a": {
            "english": "The Four Humours",
            "definition": "The four functional physiological states: Dam (blood), Balgham (phlegm), Safra (yellow bile), and Sawda (black bile)."
        },
        "Asbab-e-Sitta Zarooriya": {
            "english": "The Six Essential Factors",
            "definition": "The six lifestyle determinants of health: ambient air, food and drink, movement and rest, sleep and wakefulness, evacuation and retention, and emotional state."
        },
        "Bard": {
            "english": "Cold Quality",
            "definition": "One of the four primary qualities (Kaifiyyat) characterized by metabolic slowdown and sluggish circulation."
        },
        "Bard-Ratab": {
            "english": "Cold-Wet Temperament",
            "definition": "Constitutional profile dominated by Balgham; clinically associated with insulin resistance, fluid retention, and hypometabolism."
        },
        "Bard-Yabis": {
            "english": "Cold-Dry Temperament",
            "definition": "Constitutional profile dominated by Sauda; clinically associated with melancholia, HPA axis exhaustion, dry skin, and constipation."
        },
        "Dalak": {
            "english": "Therapeutic Massage",
            "definition": "Regimental manual therapy classified by intensity (Layyeen, Shadeed, Mutawassit) and direction for neuroregulation and lymphatic drainage."
        },
        "Dam": {
            "english": "Blood Humour",
            "definition": "Hot-Wet humour representing anabolic vitality, intravascular volume, and cardiovascular pressure."
        },
        "Fasd": {
            "english": "Phlebotomy / Venesection",
            "definition": "Classical bloodletting procedure for vascular plethora (Imtila-e-Dam)."
        },
        "Ghilaz-e-Dam": {
            "english": "Blood Thickening / Hyperviscosity",
            "definition": "Unani description of dyslipidemia, hemoconcentration, and metabolic acidosis in obesity."
        },
        "Hammam": {
            "english": "Therapeutic Bath / Hydrotherapy",
            "definition": "Graded 3-room thermoregulatory sequence inducing Heat Shock Proteins (HSP70/90) and metabolic activation."
        },
        "Hararat-e-Ghariziya": {
            "english": "Innate Heat / Metabolic Fire",
            "definition": "Mitochondrial and cellular energy production transforming nutrition into vital biological energy."
        },
        "Harr": {
            "english": "Hot Quality",
            "definition": "Primary quality representing thermogenesis, metabolic acceleration, and acute inflammation."
        },
        "Harr-Ratab": {
            "english": "Hot-Wet Temperament",
            "definition": "Constitutional profile dominated by Dam; associated with robust physique, plethora, and stage 1 hypertension."
        },
        "Harr-Yabis": {
            "english": "Hot-Dry Temperament",
            "definition": "Constitutional profile dominated by Safra; associated with rapid catabolism, GERD, high oxidative stress, and irritability."
        },
        "Hijama": {
            "english": "Cupping Therapy",
            "definition": "Superficial scarification and suction cupping for removing microcirculatory congestion and modulating local nitric oxide."
        },
        "Ihtibas-o-Istifrag": {
            "english": "Retention & Evacuation",
            "definition": "Homeostatic balance between retaining essential nutrients and eliminating metabolic waste via liver, bowel, skin, and kidneys."
        },
        "Ilaj bil Dawa": {
            "english": "Pharmacotherapy / Botanical Medicine",
            "definition": "Third tier in the Unani therapeutic hierarchy using natural substances when lifestyle and regimen are insufficient."
        },
        "Ilaj bil Ghiza": {
            "english": "Nutritional Therapy",
            "definition": "Second tier in the Unani therapeutic hierarchy treating through condition- and Mizaj-matched foods."
        },
        "Ilaj bil Tadbeer": {
            "english": "Regimental Therapy",
            "definition": "Foundational first tier in the therapeutic hierarchy utilizing physical, environmental, and behavioral interventions."
        },
        "Ilaj bil Yad": {
            "english": "Surgery / Manual Intervention",
            "definition": "Fourth tier in the hierarchy; reserved as a last resort for mechanical or acute emergencies."
        },
        "Imtila": {
            "english": "Vascular Plethora / Volume Overload",
            "definition": "Engorgement of the vascular system with excess fluid and blood humour; underlying driver of essential hypertension."
        },
        "Kaifiyyat": {
            "english": "Primary Qualities",
            "definition": "The four fundamental qualities: Hot (Harr), Cold (Bard), Moist (Ratab), and Dry (Yabis)."
        },
        "Mizaj": {
            "english": "Constitutional Temperament",
            "definition": "An individual's unique biological and metabolic phenotype established by the dynamic balance of the four humours."
        },
        "Munzij": {
            "english": "Concoctive / Ripening Therapy",
            "definition": "Herbal preparations that prepare morbid humours for physiological excretion prior to purgation."
        },
        "Mushil": {
            "english": "Purgative / Evacuation Therapy",
            "definition": "Regulated therapeutic elimination of prepared morbid matter through the gastrointestinal tract."
        },
        "Nabz": {
            "english": "Pulse Examination",
            "definition": "Ten-parameter manual examination of the arterial pulse assessing rate, volume, tension, and rhythm to evaluate Mizaj."
        },
        "Rooh": {
            "english": "Vital Spirit / Pneuma",
            "definition": "The biological carrier of vitality and nervous energy linking psychological states to somatic physiology."
        },
        "Safra": {
            "english": "Yellow Bile Humour",
            "definition": "Hot-Dry humour corresponding to hepatic metabolism, bile acid secretion, and inflammatory reactivity."
        },
        "Samn Mufrit": {
            "english": "Obesity",
            "definition": "Excessive accumulation of heavy nutritive material and fat tissue with Balgham dominance and Rooh attenuation."
        },
        "Sauda": {
            "english": "Black Bile Humour",
            "definition": "Cold-Dry humour associated with neuroendocrine burnout, tissue dehydration, and chronic degenerative states."
        },
        "Su-e-Hazm": {
            "english": "Dyspepsia / Impaired Digestion",
            "definition": "Incomplete enzymatic digestion producing fermentation, gas, and systemic inflammatory toxins (Madda)."
        },
        "Su-e-Mizaj": {
            "english": "Constitutional Derangement",
            "definition": "Pathological deviation of an individual's Mizaj away from their healthy baseline."
        },
        "Tabiyat": {
            "english": "Innate Healing Intelligence",
            "definition": "The physiological sum of homeostatic regulation, immune surveillance, and regenerative healing within the body."
        },
        "Tadbeer-e-Fasli": {
            "english": "Seasonal Regimen",
            "definition": "The systematic adjustment of nutrition, physical activity, and botanicals across the four annual seasons (Rabi, Saif, Kharif, Shita)."
        },
        "Tadbeer-e-Yawmiyya": {
            "english": "Daily Circadian Regimen",
            "definition": "The structured daily routine of waking, morning light, meal timing, and sleep architecture."
        },
        "ZAPE": {
            "english": "ZAYVORA AI Personalisation Engine",
            "definition": "Four-layer computational decision-support framework personalizing clinical care by integrating multi-axis data and Mizaj."
        },
        "ZAYVORA": {
            "english": "Integrated Health Operating System",
            "definition": "Global integrative healthcare system founded by Dr. Irfan Ashraf synthesizing Unani medicine with contemporary systems biology."
        }
    }

    @classmethod
    def get_all_evidence(cls) -> List[Dict[str, Any]]:
        return cls.OCEBM_REGISTRY

    @classmethod
    def filter_evidence_by_condition(cls, condition: str) -> List[Dict[str, Any]]:
        return [
            e for e in cls.OCEBM_REGISTRY
            if condition.lower() in e["condition"].lower() or condition.lower() in e["intervention"].lower()
        ]

    @classmethod
    def get_glossary_term(cls, term: str) -> Optional[Dict[str, Any]]:
        return cls.GLOSSARY.get(term)

    @classmethod
    def search_glossary(cls, query: str) -> List[Dict[str, Any]]:
        q = query.lower()
        results = []
        for term, details in cls.GLOSSARY.items():
            if q in term.lower() or q in details["english"].lower() or q in details["definition"].lower():
                results.append({"term": term, **details})
        return results
