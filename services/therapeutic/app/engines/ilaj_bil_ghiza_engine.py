"""
ZAYVORA Health OS™ v5.0 — Ilaj bil Ghiza (Unani Dietotherapy & Nutritional Medicine) Engine
==========================================================================================
Source Authority:
  - Ibn Sina: Al-Qanun fi al-Tibb, Vol II (Kitab al-Adwiya wal-Aghziya)
  - Abu Bakr al-Razi: Kitab al-Hawi fi al-Tibb & Manafi al-Aghziya wa Daf' Madarriha
  - Ibn Zuhr (Avenzoar): Kitab al-Aghziya
  - Mohammad Husain Shirazi: Makhzan-ul-Adwiya
  - CCRUM / Ministry of AYUSH: Guidelines for Dietary Management in Unani Medicine

Invariants:
  1. Treatment by Opposites (Ilaj bil-Zidd): Counteracts pathological Su-e-Mizaj with inverted dietary qualities.
  2. Fourfold Nutrient Hierarchy: Distinguishes Ghiza-e-Mutlaq, Ghiza-e-Dawai, Dawa-e-Ghidhai, and Dawa-e-Mutlaq.
  3. Chyme Quality & Digestibility: Distinguishes Salih-ul-Kaimus (euchymic) vs Radi-ul-Kaimus (dyschymic), and Latif vs Kaseef.
  4. Tanafur-e-Aghziya (Food Antagonisms): Strict deterministic check for incompatible food combinations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# =============================================================================
# 1. CANONICAL CLASSIFICATIONS & TAXONOMY
# =============================================================================

NUTRIENT_CATEGORIES = {
    "GHIZA_E_MUTLAQ": {
        "title": "Ghiza-e-Mutlaq (Absolute Nutrition)",
        "definition": "Substances that become part of body tissues without producing significant alterative/medicinal action.",
        "classical_examples": ["Wheat (Hintah)", "Mutton (Lahm Ghanam)", "Sweet Almonds (Badaam Shirin)", "Egg Yolk"]
    },
    "GHIZA_E_DAWAI": {
        "title": "Ghiza-e-Dawai (Dietary Medicine / Food-Drug)",
        "definition": "Nutritive foods having marked qualitative medicinal properties that gently alter the body temperament.",
        "classical_examples": ["Barley (Sha'eer)", "Garlic (Seer)", "Onion (Basal)", "Lettuce (Kahu)", "Chicory (Kasni)"]
    },
    "DAWA_E_GHIDHAI": {
        "title": "Dawa-e-Ghidhai (Medicinal Food / Drug-Food)",
        "definition": "Medicinal alteratives that possess slight incidental nutritional substance.",
        "classical_examples": ["Ginger (Zanjabeel)", "Cinnamon (Darchini)", "Cumin (Zeera)", "Mint (Pudina)", "Fennel (Badiyan)"]
    },
    "DAWA_E_MUTLAQ": {
        "title": "Dawa-e-Mutlaq (Pure Pharmacology)",
        "definition": "Substances that purely alter body quality without nourishing tissues.",
        "classical_examples": ["Suranjan", "Afsanteen", "Saqmonia", "Ustukhuddus"]
    }
}

DIGESTIBILITY_GRADES = {
    "LATIF": "Light / Easily digested / Rapid metabolic dispersion / Forms thin chyme (e.g. Barley water, Pomegranate, Chicken broth)",
    "MOTADIL": "Balanced / Moderate digestion velocity / Forms normal physiological blood (e.g. Wheat bread, Mutton)",
    "KASEEF": "Dense / Heavy digestion / Slow gastro-intestinal transit / Forms thick viscous chyme (e.g. Beef, Hard cheese, Lentils)"
}

CHYME_QUALITIES = {
    "SALIH_UL_KAIMUS": "Euchymic (Produces pure, healthy sanguine humors with minimal metabolic ash)",
    "RADI_UL_KAIMUS": "Dyschymic (Produces morbid, sluggish humors prone to putrefaction and vascular obstruction)"
}


# =============================================================================
# 2. CANONICAL THERAPEUTIC DIETARY PREPARATIONS (AGHZIYA-E-DAWAIYYAH)
# =============================================================================

CANONICAL_THERAPEUTIC_PREPARATIONS: Dict[str, Dict[str, Any]] = {
    "MAA_UL_SHAEER": {
        "name": "Maa-ul-Sha'eer (Classical Barley Water / Decoctum Hordei)",
        "mizaj": "Barid 1° Yabis 1° (Cooling & Light)",
        "indications": ["Su-e-Mizaj Haar", "Huma (Acute Febrile States)", "Hepatic Inflammatory Heat", "Burning Dysuria"],
        "preparation_protocol": (
            "Boil 1 part pearl barley in 14 parts pure water until grains burst and liquid reduces to 10 parts. "
            "Strain without pressing grains to yield a delicate, translucent liquid."
        ),
        "clinical_benefit": "Supreme cooling febrifuge; quenches cellular dehydration without taxing digestive faculties.",
        "classical_reference": "Al-Qanun fi al-Tibb, Vol II, p. 248"
    },
    "MAA_UL_JUBN": {
        "name": "Maa-ul-Jubn (Medicinal Whey / Serum Lactis)",
        "mizaj": "Barid 1° Ratab 1° (Cooling & Moistening Alterative)",
        "indications": ["Sauda Ghalib (Melancholia)", "Chronic Eczema & Psoriasis", "Visceral Sudad (Obstructions)", "Combusted Bile"],
        "preparation_protocol": (
            "Boil fresh cow or goat milk; curdle gently with a few drops of bitter orange juice or oxymel. "
            "Filter clear yellowish serum through fine muslin. Administer warm in morning fasting."
        ),
        "clinical_benefit": "Unlocks microcapillary stasis; gently concocts and purges burnt black bile without thermal depletion.",
        "classical_reference": "Kitab al-Hawi fi al-Tibb (Al-Razi), Vol XXI"
    },
    "MAA_UL_ASAL": {
        "name": "Maa-ul-Asal (Medicinal Hydromel / Honey Water)",
        "mizaj": "Haar 2° Yabis 1° (Thermogenic & Deobstruent)",
        "indications": ["Su-e-Mizaj Barid", "Phlegmatic Dyspepsia (Su-e-Hazm Balghami)", "Respiratory Mucus Congestion", "Asthenia"],
        "preparation_protocol": (
            "Dissolve 1 part raw unheated honey in 8 parts pure boiled water. "
            "Simmer gently, skimming off surface froth until crystal clear."
        ),
        "clinical_benefit": "Kindles Hararat-e-Ghariziyya, cuts through tenacious thick gastric phlegm, accelerates diuresis.",
        "classical_reference": "Al-Qanun fi al-Tibb, Vol I, Fen 3"
    },
    "KESHK_AB": {
        "name": "Keshk-ab (Barley/Wheat Gruel Water)",
        "mizaj": "Motadil (Equable Nourishment)",
        "indications": ["Post-operative convalescence", "Gastric ulceration", "Exhaustive dysentery"],
        "preparation_protocol": (
            "Crushed hulled barley or wheat steeped in cold water, boiled to thin gruel, and filtered."
        ),
        "clinical_benefit": "Gentlest physiological mucilage; coats gastric and intestinal epithelium.",
        "classical_reference": "Kitab al-Aghziya (Ibn Zuhr)"
    },
    "HARIRAH_E_BADAAM": {
        "name": "Harirah-e-Badaam (Nutritive Almond Emulsion)",
        "mizaj": "Haar 1° Ratab 2° (Warming & Tissue Restorative)",
        "indications": ["Sahar (Insomnia)", "Nisyan (Brain Fog)", "Emaciation (Huzal)", "Cerebral Dryness (Yubusat-e-Dimagh)"],
        "preparation_protocol": (
            "Blanch sweet almonds (Badaam Shirin); grind into micro-fine paste with rose water. "
            "Simmer in fresh milk with a pinch of saffron and a teaspoon of rock sugar candy (Misri)."
        ),
        "clinical_benefit": "Replenishes brain tissue substance, calms limbic tremors, and induces profound natural sleep.",
        "classical_reference": "Makhzan-ul-Adwiya (Shirazi)"
    },
    "SIKANJABEEN": {
        "name": "Sikanjabeen (Classical Oxymel)",
        "mizaj": "Motadil / Barid (Depending on vinegar to honey ratio)",
        "indications": ["Safrawi Cephalea", "Biliary Stagnation", "Splenic & Hepatic Sudad", "Nausea & Anorexia"],
        "preparation_protocol": (
            "Blend 1 part aged grape or date vinegar (Sirka) with 2 parts raw honey and 4 parts pure water. "
            "Simmer gently to rich syrup consistency."
        ),
        "clinical_benefit": "The golden vehicle in Unani medicine: cuts visceral humors, opens bile channels, neutralizes toxic bile.",
        "classical_reference": "Al-Qanun fi al-Tibb, Vol V (Formulary)"
    }
}


# =============================================================================
# 3. FOOD-FOOD INCOMPATIBILITIES (TANAFUR-E-AGHZIYA)
# =============================================================================

CANONICAL_FOOD_ANTAGONISMS = [
    {
        "combination": ["fish", "milk"],
        "arabic_designation": "Samak ma'a Laban",
        "hazard_level": "SEVERE_PROHIBITION",
        "clinical_rationale": (
            "Combining fish (Barid-Ratab 2°) and milk (Barid-Ratab 1°) creates extreme humoral conflict. "
            "Their protein coagulation characteristics differ sharply, producing putrefactive chyme (Radi-ul-Kaimus) "
            "which classical authorities (Ibn Sina, Al-Razi) associate with chronic cutaneous disorders, vitiligo (Bars), and chronic arthralgia."
        ),
        "authority": "Al-Qanun fi al-Tibb, Vol I, p. 198"
    },
    {
        "combination": ["curd", "fish"],
        "arabic_designation": "Mast ma'a Samak",
        "hazard_level": "SEVERE_PROHIBITION",
        "clinical_rationale": "Compounded cold-moist density causes immediate gastric stagnation and deep toxic mucosal coating.",
        "authority": "Makhzan-ul-Adwiya"
    },
    {
        "combination": ["milk", "sour fruits"],
        "arabic_designation": "Laban ma'a Fawakeh Hamiza",
        "hazard_level": "HIGH_PROHIBITION",
        "clinical_rationale": "Acid precipitously curdles milk proteins in the upper stomach, inducing acute nausea, colic, and dysbiosis.",
        "authority": "Kitab al-Hawi, Vol XXI"
    },
    {
        "combination": ["hot solid food", "iced water"],
        "arabic_designation": "Ta'am Haar ma'a Maa Barid",
        "hazard_level": "HIGH_PROHIBITION",
        "clinical_rationale": "Abrupt thermal shock extinguishes gastric innate warmth (Hararat-e-Ghariziyya) and coagulates fatty lipids.",
        "authority": "Al-Qanun fi al-Tibb, Vol I"
    },
    {
        "combination": ["beef", "lentils"],
        "arabic_designation": "Lahm Baqar ma'a Adas",
        "hazard_level": "MODERATE_WARNING",
        "clinical_rationale": "Compounded cold-dry heavy proteins produce excessive black bile (Sauda) and severe bowel obstipation.",
        "authority": "Kitab al-Aghziya (Ibn Zuhr)"
    }
]


# =============================================================================
# 4. ENGINE CORE IMPLEMENTATION
# =============================================================================

@dataclass
class GhizaAssessmentInput:
    patient_id: str
    mizaj: str  # Damwi, Safrawi, Balghami, Saudawi
    su_e_mizaj: Optional[str] = None  # e.g., "Su-e-Mizaj Haar", "Su-e-Mizaj Barid", etc.
    chief_complaint: str = ""
    candidate_foods: List[str] = field(default_factory=list)


class IlajBilGhizaEngine:
    """Certified clinical engine for Unani Dietetics (Ilaj bil Ghiza)."""

    @classmethod
    def check_food_incompatibilities(cls, foods: List[str]) -> List[Dict[str, Any]]:
        """Scans candidate diet list for classical toxic antagonisms (Tanafur-e-Aghziya)."""
        normalized_foods = [f.lower().strip() for f in foods]
        detected_antagonisms = []

        for rule in CANONICAL_FOOD_ANTAGONISMS:
            required_items = rule["combination"]
            # Check if all required antagonistic foods are present
            match = True
            for req in required_items:
                if not any(req in food for food in normalized_foods):
                    match = False
                    break
            if match:
                detected_antagonisms.append(rule)

        return detected_antagonisms

    @classmethod
    def formulate_dietary_regimen(
        cls,
        patient_mizaj: str,
        su_e_mizaj: Optional[str] = None,
        candidate_foods: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Synthesizes an authentic Unani dietary regimen based on Ilaj bil-Zidd."""
        effective_dyscrasia = (su_e_mizaj or patient_mizaj or "Motadil").lower()
        candidate_foods = candidate_foods or []

        # 1. Antagonism Safety Check
        antagonisms = cls.check_food_incompatibilities(candidate_foods)

        # 2. Dietary Rules by Dyscrasia
        if "haar" in effective_dyscrasia or "safrawi" in effective_dyscrasia:
            regimen_quality = "Barid-Ratab (Cooling & Moistening)"
            recommended_foods = [
                {"name": "Barley Water (Maa-ul-Sha'eer)", "role": "Principal Hydration & Febrifuge"},
                {"name": "Cucumber (Khiyar)", "role": "Quenches Hepatic Thirst"},
                {"name": "Zucchini / Gourd (Kadu)", "role": "Latif Cooling Vegetable"},
                {"name": "Sweet Pomegranate (Rumman Shirin)", "role": "Cardiac & Gastric Tonic"},
                {"name": "Purslane (Khurfa)", "role": "Sedates Bilious Irritation"},
                {"name": "Medicinal Whey (Maa-ul-Jubn)", "role": "Purges Combusted Bile"}
            ]
            restricted_foods = [
                "Red meat & Beef", "Deep fried foods", "Garlic & Raw Onions",
                "Black Pepper & Mustard", "Aged Cheese", "Hot Chillies & Pungent Spices"
            ]
            primary_therapeutic_preparation = CANONICAL_THERAPEUTIC_PREPARATIONS["MAA_UL_SHAEER"]
            musleh_advisory = "Incorporate Coriander (Kishneez) and Oxymel (Sikanjabeen) as dietary correctives."

        elif "barid" in effective_dyscrasia or "balghami" in effective_dyscrasia:
            regimen_quality = "Haar-Yabis / Haar-Ratab (Thermogenic & Drying)"
            recommended_foods = [
                {"name": "Medicinal Hydromel (Maa-ul-Asal)", "role": "Gastric Warmth & Phlegm Dissolution"},
                {"name": "Ginger-infused Mutton Broth", "role": "Replenishes Innate Heat"},
                {"name": "Cumin (Zeera Siyah) Seasoning", "role": "Dispels Flatulence & Dries Moisture"},
                {"name": "Fenugreek (Methi) Leaves", "role": "Deobstruent & Phlegm Expellent"},
                {"name": "Dried Figs (Injeer) & Walnuts", "role": "Warming Nutrient Tonic"},
                {"name": "Fresh Garlic (Seer) Boiled", "role": "Visceral Deobstruent"}
            ]
            restricted_foods = [
                "Chilled iced water", "Curd / Yogurt", "Raw cold milk",
                "Cucumber & Watermelon", "Mash lentils & Starchy tubers", "Ice cream & refrigerated food"
            ]
            primary_therapeutic_preparation = CANONICAL_THERAPEUTIC_PREPARATIONS["MAA_UL_ASAL"]
            musleh_advisory = "Incorporate Ginger (Zanjabeel) and Black Pepper (Filfil Siyah) as gastric correctives."

        elif "yabis" in effective_dyscrasia or "saudawi" in effective_dyscrasia:
            regimen_quality = "Haar-Ratab (Warming & Humectant / Moistening)"
            recommended_foods = [
                {"name": "Nutritive Almond Emulsion (Harirah-e-Badaam)", "role": "Brain Tissue & Sleep Restorative"},
                {"name": "Medicinal Whey (Maa-ul-Jubn)", "role": "Purges Burnt Melancholic Humors"},
                {"name": "Fresh Goat Milk with Honey", "role": "Moistens Somatic Tissues"},
                {"name": "Spinach (Isfanakh) with Olive Oil", "role": "Laxative & Humectant"},
                {"name": "Sweet Seedless Grapes", "role": "Produces Euchymic Sanguine Blood"},
                {"name": "Chicken Bone Broth (Shorba Dajaj)", "role": "Gentle Nourishment"}
            ]
            restricted_foods = [
                "Beef (Lahm Baqar)", "Lentils (Adas / Masoor)", "Cabbage & Eggplant (Baingan)",
                "Dry salted fish", "Stale/preserved meat", "Excessive tea & astringent berries"
            ]
            primary_therapeutic_preparation = CANONICAL_THERAPEUTIC_PREPARATIONS["HARIRAH_E_BADAAM"]
            musleh_advisory = "Incorporate Sweet Almond Oil (Roghan Badaam) and Saffron as cardiac and mood correctives."

        else:  # Damwi / Motadil
            regimen_quality = "Motadil Latif (Equable & Light Nutrition)"
            recommended_foods = [
                {"name": "Whole Wheat Bread (Khubz Hintah)", "role": "Equable Body Tissue Sustenance"},
                {"name": "Fresh Apple & Pomegranate Salad", "role": "Cardiac Tonic"},
                {"name": "Light Chicken Soup", "role": "Digestive Maintenance"},
                {"name": "Chicory (Kasni) Infusion", "role": "Hepatic Microvascular Clarity"}
            ]
            restricted_foods = ["Overeating / Gluttony (Imtila)", "Excess red meat", "Heavy pastries"]
            primary_therapeutic_preparation = CANONICAL_THERAPEUTIC_PREPARATIONS["KESHK_AB"]
            musleh_advisory = "Maintain moderation and adhere to circadian meal timing."

        return {
            "status": "APPROVED",
            "effective_mizaj_target": effective_dyscrasia,
            "prescribed_dietary_quality": regimen_quality,
            "recommended_foods": recommended_foods,
            "restricted_foods": restricted_foods,
            "primary_therapeutic_preparation": primary_therapeutic_preparation,
            "musleh_corrective_advisory": musleh_advisory,
            "food_antagonisms_detected": antagonisms,
            "is_safe_for_consumption": len(antagonisms) == 0,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
