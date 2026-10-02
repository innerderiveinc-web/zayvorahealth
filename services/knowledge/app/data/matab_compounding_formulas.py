"""
ZAYVORA Health OS™ - Matab Clinical Compounding Formulations
Reference: Master Clinical System (Part III), Dr. Irfan Ashraf, BUMS.

High-potency, gram-based raw powder & decoction formulas for internal dispensary use (Matab).
These formulations are NOT for open retail distribution and represent the authentic clinical
application of ZAYVORA protocols administered directly by qualified Hakeems.
"""

from typing import Dict, Any, List, Optional


MATAB_FORMULAS: Dict[str, Dict[str, Any]] = {
    "MATAB-01": {
        "protocol_id": "MATAB-01",
        "name": "Female Infertility Matab Protocol",
        "organ_axis": "Ovary (Mabaysim) / Jigar-Reham",
        "description": "Sequential 3-phase high-potency decoction & milk-vehicle clinical formula.",
        "phases": {
            "phase_1": {
                "phase_name": "Phase 1: Gut-Liver Priming",
                "duration_days": 30,
                "ingredients": [
                    {"herb": "Kasni (Cichorium intybus) root", "dose_g": 5.0, "role": "Hepatoprotective & inulin prebiotic"},
                    {"herb": "Triphala Churna", "dose_g": 5.0, "role": "Humoral concoction (Nujz) & bowel clearance"},
                    {"herb": "Daruhaldi (Berberis aristata)", "dose_g": 3.0, "role": "AMPK activation & pelvic anti-inflammatory"},
                    {"herb": "Mastagi Rumi (Pistacia lentiscus)", "dose_g": 2.0, "role": "Gastric mucosa protection (if IBS tendency)"}
                ],
                "preparation_method": "Decoction: boil in 400ml water down to 150ml. Drink BD before meals."
            },
            "phase_2": {
                "phase_name": "Phase 2: Follicular Activation",
                "duration_cycle_days": "Day 5 to Day 14 of menstrual cycle",
                "ingredients": [
                    {"herb": "Shatavari (Asparagus racemosus)", "dose_g": 6.0, "role": "Follicular stimulation & steroidal saponins"},
                    {"herb": "Lodhra (Symplocos racemosa)", "dose_g": 4.0, "role": "Ovarian microcirculation & LH modulation"},
                    {"herb": "Ashoka (Saraca asoca) bark", "dose_g": 4.0, "role": "Endometrial receptor sensitization"},
                    {"herb": "Behman Safaid (Centaurea behen)", "dose_g": 3.0, "role": "Uterine Muqawwi & vital spirit tonic"},
                    {"herb": "Tukhm-e-Karafs (Celery seed)", "dose_g": 2.0, "role": "Emmenagogue catalyst & pelvic blood flow"}
                ],
                "preparation_method": "Coarsely ground powder taken with 250ml warm grass-fed cow milk at bedtime."
            },
            "phase_3": {
                "phase_name": "Phase 3: Luteal Stabilization",
                "duration_cycle_days": "Day 15 to Day 28 of menstrual cycle",
                "ingredients": [
                    {"herb": "Gaozaban (Borago officinalis)", "dose_g": 5.0, "role": "Neuroendocrine calming & GLA prostaglandin balance"},
                    {"herb": "Amla (Phyllanthus emblica)", "dose_g": 5.0, "role": "Corpus luteum antioxidant shield (high Vit C)"},
                    {"herb": "Gul-e-Surkh (Rosa damascena)", "dose_g": 3.0, "role": "Mufarrih-e-Qalb, reduces luteal anxiety"},
                    {"herb": "Jatamansi (Nardostachys jatamansi)", "dose_g": 2.0, "role": "GABAergic progesterone support"}
                ],
                "preparation_method": "Infusion in warm water, strained and taken at 8:00 PM."
            }
        },
        "parhez": ["Avoid cold sour foods, vinegar, refrigerated curd, and unpasteurized soft cheeses", "Emphasize warm grass-fed cow milk with soaked almonds and saffron, and bone broths"]
    },
    "MATAB-02": {
        "protocol_id": "MATAB-02",
        "name": "Male Infertility & Oligospermia Matab Formula",
        "organ_axis": "Testicular (Khusyatain) / Jigar-Khusyatain",
        "description": "Potent spermatogenic and Leydig cell activation formula.",
        "ingredients": [
            {"herb": "Asgandh Nagauri (Withania somnifera)", "dose_g": 6.0, "role": "LH stimulation & testicular ROS reduction"},
            {"herb": "Salab Misri (Orchis mascula)", "dose_g": 5.0, "role": "#1 Muwalid-e-Mani biological substrate"},
            {"herb": "Safed Musli (Chlorophytum borivilianum)", "dose_g": 5.0, "role": "Sperm motility & volume enhancement"},
            {"herb": "Gokhru (Tribulus terrestris)", "dose_g": 5.0, "role": "Protodioscin nitric oxide release"},
            {"herb": "Behman Safaid", "dose_g": 4.0, "role": "Cardio-seminal vascular conduit"},
            {"herb": "Tabasheer (Bambusa arundinacea)", "dose_g": 4.0, "role": "Scrotal cooling (maintains 34°C testicular environment)"}
        ],
        "vehicle": "Warm full-fat milk with 1 tsp raw honey",
        "timing": "Twice daily: morning fasting and night before sleep",
        "parhez": ["Avoid excessive sour foods (Imli, pickles), trans-fats, tight nylon underwear, and hot saunas", "Emphasize grass-fed cow milk, dates, soaked almonds, and roasted pumpkin seeds"]
    },
    "MATAB-03": {
        "protocol_id": "MATAB-03",
        "name": "PCOS Metabolic-Ovarian Balance Matab Formula",
        "organ_axis": "Insulin-Ovary Axis (Reham-Mabaysim)",
        "ingredients": [
            {"herb": "Shatavari", "dose_g": 5.0, "role": "FSH/LH pulsatility restore"},
            {"herb": "Lodhra", "dose_g": 3.0, "role": "Anti-androgenic on ovarian theca cells"},
            {"herb": "Ashoka", "dose_g": 3.0, "role": "Menstrual regulation"},
            {"herb": "Kasni", "dose_g": 5.0, "role": "Hepatic insulin clearance"},
            {"herb": "Methi Dana", "dose_g": 3.0, "role": "4-OH-Isoleucine insulin sensitiser"},
            {"herb": "Gaozaban", "dose_g": 4.0, "role": "Mufarrih, cortisol-driven androgen suppression"}
        ],
        "vehicle": "Lukewarm water with 10 drops fresh lemon juice",
        "timing": "Morning 30 mins before breakfast and evening 6:00 PM",
        "parhez": ["Avoid refined sugar, bakery, white flour, and dairy fats", "Emphasize high-fiber fenugreek and soaked seeds"]
    },
    "MATAB-04": {
        "protocol_id": "MATAB-04",
        "name": "Metabolic Reset & Insulin Sensitivity Formula",
        "organ_axis": "Hepato-Metabolic (Jigar-Banas)",
        "ingredients": [
            {"herb": "Kasni root", "dose_g": 6.0, "role": "Prebiotic & hepatoprotective"},
            {"herb": "Makoh aerial", "dose_g": 6.0, "role": "Bile acid secretion & anti-steatotic"},
            {"herb": "Methi Dana", "dose_g": 5.0, "role": "Slows intestinal glucose uptake"},
            {"herb": "Zeera Siyah", "dose_g": 3.0, "role": "Digestive carminative"},
            {"herb": "Punarnava root", "dose_g": 4.0, "role": "Renal metabolic clearance"},
            {"herb": "Triphala", "dose_g": 5.0, "role": "Eliminates toxic humoral congestion"}
        ],
        "vehicle": "Boiled warm decoction BD before main meals",
        "timing": "Twice daily: 30 minutes before main meals (12:30 PM & 8:00 PM)",
        "parhez": ["Avoid deep fried food, high glycemic index fruits, and direct post-meal sleep", "Include radish, bitter gourd, and barley"]
    },
    "MATAB-05": {
        "protocol_id": "MATAB-05",
        "name": "Liver-Gut Clearance Matab Formula",
        "organ_axis": "Gut-Digestive (Meda-Amaa)",
        "ingredients": [
            {"herb": "Kasni", "dose_g": 5.0, "role": "Bile flow"},
            {"herb": "Makoh", "dose_g": 5.0, "role": "Liver detox"},
            {"herb": "Daruhaldi", "dose_g": 3.0, "role": "Anti-microbial & AMPK"},
            {"herb": "Triphala", "dose_g": 5.0, "role": "Mild laxative"},
            {"herb": "Isabgol husk", "dose_g": 5.0, "role": "Binds bile acids & fecal bulk"}
        ],
        "vehicle": "Full glass (250ml) warm water at bedtime",
        "timing": "Bedtime (09:30 PM) with 250ml warm water",
        "parhez": ["Avoid heavy red meat, oily curries, and alcohol", "Drink warm water only"]
    },
    "MATAB-06": {
        "protocol_id": "MATAB-06",
        "name": "StoneCare Mufattit-e-Hisat Formula",
        "organ_axis": "Renal (Kulya-Mithana)",
        "ingredients": [
            {"herb": "Gokhru", "dose_g": 6.0, "role": "Diuretic & ureteral smooth muscle relaxant"},
            {"herb": "Punarnava", "dose_g": 6.0, "role": "Uric acid clearance & renal repair"},
            {"herb": "Hajrul Yahood Shuddha", "dose_g": 3.0, "role": "Mineral lithotriptic (14-21 days maximum)"},
            {"herb": "Kasni", "dose_g": 5.0, "role": "Urinary alkalinisation"}
        ],
        "vehicle": "3 litres daily water with fresh lemon juice",
        "timing": "Three times daily with high volume hydration (07:00 AM, 01:00 PM, 07:00 PM)",
        "parhez": ["Strictly avoid spinach, tomato seeds, chocolates, excess calcium supplements", "Drink minimum 3L water daily"]
    },
    "MATAB-07": {
        "protocol_id": "MATAB-07",
        "name": "NeuroCalm & HPA Axis Reset Formula",
        "organ_axis": "Neural-Cardiac (Dimagh-Qalb)",
        "ingredients": [
            {"herb": "Jatamansi", "dose_g": 2.0, "role": "GABA-A positive allosteric modulation"},
            {"herb": "Brahmi", "dose_g": 3.0, "role": "Bacosides serotonin & memory support"},
            {"herb": "Gaozaban", "dose_g": 4.0, "role": "Mufarrih-e-Qalb, neuro-anti-inflammatory"},
            {"herb": "Arjun bark", "dose_g": 5.0, "role": "Vagal tone & cardiotonic"},
            {"herb": "Unnab", "dose_g": 4.0, "role": "Sedative cAMP anxiolytic"}
        ],
        "vehicle": "Warm milk with a pinch of nutmeg at 9:00 PM",
        "timing": "Bedtime (09:30 PM) in calm quiet setting",
        "parhez": ["Avoid coffee, energy drinks, late screen exposure, and heated arguments", "Practice 10 mins cooling nasal breathing"]
    },
    "MATAB-08": {
        "protocol_id": "MATAB-08",
        "name": "JointRestore & Muhallil-e-Mafasil Formula",
        "organ_axis": "Musculo-Skeletal (Mafasil)",
        "ingredients": [
            {"herb": "Suranjan Shireen", "dose_g": 3.0, "role": "Colchicine anti-inflammatory (30 days max)"},
            {"herb": "Asgandh", "dose_g": 5.0, "role": "Muscle protection & cortisol suppression"},
            {"herb": "Daruhaldi", "dose_g": 5.0, "role": "5-LOX and COX-2 inhibition"},
            {"herb": "Gokhru", "dose_g": 4.0, "role": "Uric acid excretion"},
            {"herb": "Punarnava", "dose_g": 4.0, "role": "Synovial edema resolution"}
        ],
        "vehicle": "Taken after meals + warm Roghan massage on joints",
        "timing": "Twice daily after meals (02:00 PM & 08:30 PM)",
        "parhez": ["Avoid cold sour curd, eggplant, tomato, and direct cold drafts on joints", "Take warm mutton bone broth"]
    }
}


def get_matab_formula(protocol_id: str) -> Optional[Dict[str, Any]]:
    return MATAB_FORMULAS.get(protocol_id.upper())


def get_all_matab_formulas() -> List[Dict[str, Any]]:
    return list(MATAB_FORMULAS.values())
