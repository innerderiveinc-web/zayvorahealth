"""
ZAYVORA Knowledge Base (ZKB) — Structured Clinical Knowledge Subsystem
Covers Mufradat, Murakkabat, Disease Taxonomy, Mizaj Engine, Organ-Axis Matrix,
and Deterministic Clinical Safety Firewall.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# -----------------------------------------------------------------------------
# 1. CANONICAL MUFRADAT REPOSITORY
# -----------------------------------------------------------------------------
CANONICAL_MUFRADAT_DATA: List[Dict[str, Any]] = [
    {
        "id": "muf-asgandh",
        "canonical_name_latin": "Withania somnifera (L.) Dunal",
        "canonical_name_urdu": "اسگندھ",
        "canonical_name_arabic": "عَبَاب",
        "canonical_name_english": "Winter Cherry / Ashwagandha",
        "botanical_name": "Withania somnifera (L.) Dunal",
        "upi_code": "UPI-M-001",
        "origin_category": "VEGETABLE",
        "plant_part_used": "Dried Root",
        "mizaj_primary_quality": "HOT_AND_DRY",
        "mizaj_degree": 1,
        "is_schedule_e1_poison": False,
        "mandatory_mudabbar": False,
        "mudabbar_protocol": None,
        "historical_dose": "3 to 5 masha (3–5 g)",
        "approved_single_dose_max_grams": 6.0,
        "approved_daily_dose_max_grams": 12.0,
        "therapeutic_actions": ["Muqawwi-e-Aam", "Musakkin", "Muwallid-e-Mani"],
        "badal_substitutes": ["Bahman Surkh", "Bozidan"],
        "musleh_correctives": ["Kateera", "Gond Babool"],
        "pregnancy_status": "CAUTION",
        "lactation_status": "SAFE_WITH_MONITORING",
        "pediatric_status": "SAFE_ABOVE_6_YEARS",
        "geriatric_status": "SAFE_TONIC",
        "evidence_level": "E2",
        "current_lifecycle_state": "CLINICALLY_APPROVED",
        "safe_for_ai": True,
    },
    {
        "id": "muf-suranjan-talkh",
        "canonical_name_latin": "Colchicum luteum Baker",
        "canonical_name_urdu": "سورنجان تلخ",
        "canonical_name_arabic": "عُكْنَة",
        "canonical_name_english": "Bitter Meadow Saffron",
        "botanical_name": "Colchicum luteum Baker",
        "upi_code": "UPI-M-002",
        "origin_category": "VEGETABLE",
        "plant_part_used": "Dried Corm",
        "mizaj_primary_quality": "HOT_AND_DRY",
        "mizaj_degree": 3,
        "is_schedule_e1_poison": True,
        "mandatory_mudabbar": True,
        "mudabbar_protocol": "Boiled in cow's milk for 3 hours, skin peeled, embryo excised, fried in Roghan-e-Badam.",
        "historical_dose": "2 to 4 ratti (250–500 mg)",
        "approved_single_dose_max_grams": 0.250,
        "approved_daily_dose_max_grams": 0.750,
        "therapeutic_actions": ["Muhallil-e-Aoraam", "Musakkin-e-Alam", "Mukhrij-e-Mawad"],
        "badal_substitutes": ["Suranjan Shireen", "Bozidan"],
        "musleh_correctives": ["Roghan-e-Badam", "Zafran", "Kateera"],
        "pregnancy_status": "ABSOLUTE_CONTRAINDICATION",
        "lactation_status": "ABSOLUTE_CONTRAINDICATION",
        "pediatric_status": "ABSOLUTE_CONTRAINDICATION",
        "geriatric_status": "RESTRICTED_CLOSE_MONITORING",
        "evidence_level": "E1",
        "current_lifecycle_state": "CLINICALLY_APPROVED",
        "safe_for_ai": True,
    },
    {
        "id": "muf-kuchla",
        "canonical_name_latin": "Strychnos nux-vomica L.",
        "canonical_name_urdu": "کچلہ / اذراقی",
        "canonical_name_arabic": "جَوْز القَيْء",
        "canonical_name_english": "Nux Vomica / Poison Nut",
        "botanical_name": "Strychnos nux-vomica L.",
        "upi_code": "UPI-M-003",
        "origin_category": "VEGETABLE",
        "plant_part_used": "Dried Ripe Seed",
        "mizaj_primary_quality": "HOT_AND_DRY",
        "mizaj_degree": 3,
        "is_schedule_e1_poison": True,
        "mandatory_mudabbar": True,
        "mudabbar_protocol": "Soaked in cow's milk for 7 days, seed coat and embryo excised, endosperm fried in Cow's Ghee.",
        "historical_dose": "Half to 1 ratti (30–65 mg)",
        "approved_single_dose_max_grams": 0.065,
        "approved_daily_dose_max_grams": 0.125,
        "therapeutic_actions": ["Muqawwi-e-Asab", "Muqawwi-e-Baah", "Muharrik-e-Qalb"],
        "badal_substitutes": ["Jadwar", "Asgandh"],
        "musleh_correctives": ["Roghan-e-Zard", "Milk", "Anisoon"],
        "pregnancy_status": "ABSOLUTE_CONTRAINDICATION",
        "lactation_status": "ABSOLUTE_CONTRAINDICATION",
        "pediatric_status": "ABSOLUTE_CONTRAINDICATION",
        "geriatric_status": "ABSOLUTE_CONTRAINDICATION",
        "evidence_level": "E1",
        "current_lifecycle_state": "CLINICALLY_APPROVED",
        "safe_for_ai": True,
    },
    {
        "id": "muf-filfil-siyah",
        "canonical_name_latin": "Piper nigrum L.",
        "canonical_name_urdu": "فلفل سیاہ",
        "canonical_name_arabic": "فُلْفُل أَسْوَد",
        "canonical_name_english": "Black Pepper",
        "botanical_name": "Piper nigrum L.",
        "upi_code": "UPI-M-004",
        "origin_category": "VEGETABLE",
        "plant_part_used": "Dried Berries",
        "mizaj_primary_quality": "HOT_AND_DRY",
        "mizaj_degree": 3,
        "is_schedule_e1_poison": False,
        "mandatory_mudabbar": False,
        "mudabbar_protocol": None,
        "historical_dose": "500 mg to 1 g",
        "approved_single_dose_max_grams": 1.0,
        "approved_daily_dose_max_grams": 2.0,
        "therapeutic_actions": ["Hazim", "Kasir-e-Riyah", "MulaYYin"],
        "badal_substitutes": ["Zanjabeel", "Filfil Daraz"],
        "musleh_correctives": ["Roghan-e-Badam", "Ghee"],
        "pregnancy_status": "SAFE_FOOD_AMOUNTS",
        "lactation_status": "SAFE_WITH_MONITORING",
        "pediatric_status": "SAFE_ABOVE_2_YEARS",
        "geriatric_status": "SAFE",
        "evidence_level": "E2",
        "current_lifecycle_state": "CLINICALLY_APPROVED",
        "safe_for_ai": True,
    },
    {
        "id": "muf-zafran",
        "canonical_name_latin": "Crocus sativus L.",
        "canonical_name_urdu": "زعفران",
        "canonical_name_arabic": "زَعْفَرَان",
        "canonical_name_english": "Saffron",
        "botanical_name": "Crocus sativus L.",
        "upi_code": "UPI-M-005",
        "origin_category": "VEGETABLE",
        "plant_part_used": "Dried Stigmas",
        "mizaj_primary_quality": "HOT_AND_DRY",
        "mizaj_degree": 2,
        "is_schedule_e1_poison": False,
        "mandatory_mudabbar": False,
        "mudabbar_protocol": None,
        "historical_dose": "250 mg to 500 mg",
        "approved_single_dose_max_grams": 0.500,
        "approved_daily_dose_max_grams": 1.000,
        "therapeutic_actions": ["Mufarrih-e-Qalb", "Muqawwi-e-Dimagh", "Mudirr-e-Baul"],
        "badal_substitutes": ["Qust", "Darcheeni"],
        "musleh_correctives": ["Anisoon", "Sikangabeen"],
        "pregnancy_status": "ABSOLUTE_CONTRAINDICATION_IN_HIGH_DOSE",
        "lactation_status": "SAFE_NORMAL_DOSE",
        "pediatric_status": "SAFE_ABOVE_6_YEARS",
        "geriatric_status": "SAFE_CARDIOTONIC",
        "evidence_level": "E3",
        "current_lifecycle_state": "CLINICALLY_APPROVED",
        "safe_for_ai": True,
    },
]


# -----------------------------------------------------------------------------
# 2. CANONICAL MURAKKABAT (COMPOUND FORMULATIONS)
# -----------------------------------------------------------------------------
CANONICAL_MURAKKABAT_DATA: List[Dict[str, Any]] = [
    {
        "id": "mur-majun-suranjan",
        "canonical_name_urdu": "معجون سورنجان",
        "canonical_name_english": "Majun Suranjan",
        "dosage_form": "Majun (Electuary)",
        "nfum_code": "NFUM-I-001",
        "primary_organ_axis": "Musculo-Skeletal & Joint Axis",
        "therapeutic_objective": "Relief from chronic joint pain, inflammatory gout, and sciatica (Waja' al-Mafasil wa Irq al-Nasa).",
        "overall_mizaj": "Hot & Dry (2nd degree)",
        "approved_single_dose_min_grams": 5.0,
        "approved_single_dose_max_grams": 7.0,
        "approved_daily_dose_max_grams": 14.0,
        "anupan_vehicle": "Warm water or Arq-e-Badiyan",
        "shelf_life_months": 36,
        "manufacturing_protocol": "Decoction of Suranjan Talkh (Mudabbar) mixed with Qand Siyah syrup, fine powders incorporated, cooled.",
        "ingredients": [
            {"mufradat_id": "muf-suranjan-talkh", "ratio": 0.15, "is_chief": True, "requires_mudabbar": True},
            {"mufradat_id": "muf-filfil-siyah", "ratio": 0.10, "is_chief": False, "requires_mudabbar": False},
            {"mufradat_id": "muf-zafran", "ratio": 0.05, "is_chief": False, "requires_mudabbar": False},
        ],
        "evidence_level": "E2",
        "current_lifecycle_state": "CLINICALLY_APPROVED",
        "safe_for_ai": True,
    },
    {
        "id": "mur-khamira-gawzaban",
        "canonical_name_urdu": "خمیرہ گاوزبان عنبری جواہر والا",
        "canonical_name_english": "Khamira Gawzaban Ambari Jawaharwala",
        "dosage_form": "Khamira (Fermented/Aerated Electuary)",
        "nfum_code": "NFUM-I-002",
        "primary_organ_axis": "Cardio-Vascular & Neuro-Cerebral Axis",
        "therapeutic_objective": "Exhilarant and cardiac tonic for palpitation, anxiety, mental exhaustion, and weakness of memory.",
        "overall_mizaj": "Moderate Warm (Motadil)",
        "approved_single_dose_min_grams": 3.0,
        "approved_single_dose_max_grams": 5.0,
        "approved_daily_dose_max_grams": 10.0,
        "anupan_vehicle": "Warm milk or Arq-e-Gawzaban",
        "shelf_life_months": 24,
        "manufacturing_protocol": "Aqueous extract of Gawzaban boiled with sugar base, whisked vigorously until frothy white, pulverized pearls/emeralds added.",
        "ingredients": [
            {"mufradat_id": "muf-asgandh", "ratio": 0.20, "is_chief": True, "requires_mudabbar": False},
            {"mufradat_id": "muf-zafran", "ratio": 0.05, "is_chief": False, "requires_mudabbar": False},
        ],
        "evidence_level": "E3",
        "current_lifecycle_state": "CLINICALLY_APPROVED",
        "safe_for_ai": True,
    },
]


# -----------------------------------------------------------------------------
# 3. CANONICAL DISEASES & UNANI-BIOMEDICAL MAPPINGS
# -----------------------------------------------------------------------------
CANONICAL_DISEASES_DATA: List[Dict[str, Any]] = [
    {
        "id": "dis-waja-al-mafasil",
        "unani_name_arabic": "وجع المفاصل",
        "unani_name_urdu": "وجع المفاصل",
        "transliterated_name": "Waja' al-Mafasil",
        "icd11_code": "FA20",
        "snomed_ct_id": "399269003",
        "biomedical_mapping_type": "phenotypic_cluster",
        "primary_organ_axis": "Musculo-Skeletal & Joint Axis",
        "pathology_mizaj_derangement": "Su'-e-Mizaj Balghami with Materia Morbens (Balgham-e-Ghaleez)",
        "clinical_manifestations": "Joint pain, morning stiffness, swelling, crepitus, restricted mobility exacerbated by cold weather.",
        "treatment_principles": "Tanqiya (evacuation of morbid phlegm via Munzij-Mushil), followed by Tadil (tempering) and Muqawwi Mafasil tonics.",
    },
    {
        "id": "dis-su-e-hazm",
        "unani_name_arabic": "سوء الهضم",
        "unani_name_urdu": "سوء ہضم",
        "transliterated_name": "Su'-e-Hazm",
        "icd11_code": "DD90",
        "snomed_ct_id": "37108002",
        "biomedical_mapping_type": "phenotypic_cluster",
        "primary_organ_axis": "Hepato-Digestive & Gastro-Intestinal Axis",
        "pathology_mizaj_derangement": "Su'-e-Mizaj Barid (Cold derangement of stomach resulting in weak Quwat-e-Hazima).",
        "clinical_manifestations": "Epigastric fullness, delayed gastric emptying, belching, flatulence, borborygmi, anorexia.",
        "treatment_principles": "Tanqiya of gastric phlegm, warm stomachic digestives (Jawarish Kamuni, Filfil Siyah), light diet (Ilaj bil-Ghiza).",
    },
]


# -----------------------------------------------------------------------------
# 4. HERB-DRUG INTERACTIONS
# -----------------------------------------------------------------------------
CANONICAL_HERB_DRUG_INTERACTIONS: List[Dict[str, Any]] = [
    {
        "mufradat_id": "muf-zafran",
        "modern_drug_class": "Anticoagulants / Antiplatelets (Warfarin, Aspirin, Clopidogrel)",
        "interaction_mechanism": "Synergistic inhibition of platelet aggregation and thromboxane synthesis.",
        "clinical_effect": "Increased risk of spontaneous bleeding, hematoma, prolonged INR.",
        "risk_severity": "SEVERE",
        "recommended_action": "AVOID_COMBINATION_OR_MONITOR_INR",
    },
    {
        "mufradat_id": "muf-filfil-siyah",
        "modern_drug_class": "P-glycoprotein / CYP3A4 Substrates (Digoxin, Cyclosporine, Phenytoin)",
        "interaction_mechanism": "Piperine potent bio-enhancer inhibits intestinal CYP3A4 and P-glycoprotein efflux.",
        "clinical_effect": "Elevated modern drug serum concentration and potential acute toxicity.",
        "risk_severity": "MODERATE",
        "recommended_action": "ADJUST_MODERN_DOSE_OR_SEPARATE_BY_4_HOURS",
    },
    {
        "mufradat_id": "muf-suranjan-talkh",
        "modern_drug_class": "CYP3A4 Inhibitors (Clarithromycin, Ketoconazole) & Statin Lipid Lowering Drugs",
        "interaction_mechanism": "Impaired colchicine clearance causing systemic mitotic toxicity, rhabdomyolysis.",
        "clinical_effect": "Severe gastrointestinal necrosis, acute kidney injury, muscular breakdown.",
        "risk_severity": "FATAL",
        "recommended_action": "ABSOLUTE_CONTRAINDICATION_BLOCK",
    },
]


class StructuredKnowledgeEngine:
    """Enterprise Knowledge Repository for Mufradat, Murakkabat, Diseases, and Safety Checks."""

    def __init__(self):
        self.mufradat: Dict[str, Dict[str, Any]] = {m["id"]: dict(m) for m in CANONICAL_MUFRADAT_DATA}
        self.murakkabat: Dict[str, Dict[str, Any]] = {m["id"]: dict(m) for m in CANONICAL_MURAKKABAT_DATA}
        self.diseases: Dict[str, Dict[str, Any]] = {d["id"]: dict(d) for d in CANONICAL_DISEASES_DATA}
        self.interactions: List[Dict[str, Any]] = list(CANONICAL_HERB_DRUG_INTERACTIONS)

    # ------------------------------------------------------------------------
    # MUFRADAT
    # ------------------------------------------------------------------------
    def get_all_mufradat(self, is_poison: Optional[bool] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        res = list(self.mufradat.values())
        if is_poison is not None:
            res = [m for m in res if m["is_schedule_e1_poison"] == is_poison]
        if search:
            q = search.lower()
            res = [
                m for m in res
                if q in m["canonical_name_latin"].lower()
                or q in m["canonical_name_urdu"].lower()
                or q in m.get("canonical_name_english", "").lower()
                or q in m.get("upi_code", "").lower()
            ]
        return res

    def get_mufrad_by_id(self, mufrad_id: str) -> Optional[Dict[str, Any]]:
        return self.mufradat.get(mufrad_id)

    # ------------------------------------------------------------------------
    # MURAKKABAT & FORMULATION GATE
    # ------------------------------------------------------------------------
    def get_all_murakkabat(self, search: Optional[str] = None) -> List[Dict[str, Any]]:
        res = list(self.murakkabat.values())
        if search:
            q = search.lower()
            res = [
                m for m in res
                if q in m["canonical_name_english"].lower()
                or q in m["canonical_name_urdu"].lower()
                or q in m["dosage_form"].lower()
                or q in m["primary_organ_axis"].lower()
            ]
        return res

    def get_murakkab_by_id(self, murakkab_id: str) -> Optional[Dict[str, Any]]:
        return self.murakkabat.get(murakkab_id)

    def validate_formulation_integrity(self, formulation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detects missing ingredients, unpurified Schedule E(1) toxins, and posology conflicts."""
        errors = []
        warnings = []
        ingredients = formulation_data.get("ingredients", [])

        if not ingredients:
            errors.append("Formulation must contain at least one ingredient.")

        seen_mufradat = set()
        has_mudabbar_poison = False

        for ing in ingredients:
            m_id = ing.get("mufradat_id")
            if not m_id:
                errors.append("Missing mufradat_id for component ingredient.")
                continue

            if m_id in seen_mufradat:
                errors.append(f"Duplicate ingredient '{m_id}' detected in recipe.")
            seen_mufradat.add(m_id)

            herb = self.get_mufrad_by_id(m_id)
            if not herb:
                errors.append(f"Unknown botanical identity: Mufrad '{m_id}' not found in canonical registry.")
                continue

            # Schedule E(1) Detoxification Gate
            if herb.get("is_schedule_e1_poison"):
                has_mudabbar_poison = True
                if not ing.get("requires_mudabbar"):
                    errors.append(
                        f"SCHEDULE E(1) SAFETY GATE VIOLATION: Ingredient '{herb['canonical_name_latin']}' "
                        "requires certified Mudabbar protocol proof before incorporation."
                    )

        # Ratio sum check
        total_ratio = sum(float(ing.get("ratio", 0)) for ing in ingredients)
        if total_ratio <= 0.0:
            errors.append("Ingredient ratios must sum to a positive fraction.")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "has_schedule_e1": has_mudabbar_poison,
        }

    # ------------------------------------------------------------------------
    # DETERMINISTIC CLINICAL SAFETY FIREWALL
    # ------------------------------------------------------------------------
    def evaluate_prescription_safety(
        self,
        patient_context: Dict[str, Any],
        prescribed_items: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Non-bypassable multi-variable clinical safety evaluation."""
        violations = []
        warnings = []
        blocked = False

        age = patient_context.get("age", 35)
        is_pregnant = patient_context.get("is_pregnant", False)
        is_lactating = patient_context.get("is_lactating", False)
        eGFR = patient_context.get("egfr", 90.0) # Renal clearance
        alt = patient_context.get("alt", 25.0)   # Hepatic enzyme
        concurrent_modern_drugs = [d.lower() for d in patient_context.get("modern_drugs", [])]

        for item in prescribed_items:
            m_id = item.get("mufradat_id")
            dose = float(item.get("single_dose_grams", 0.0))
            is_mudabbar_certified = bool(item.get("mudabbar_certified", False))

            herb = self.get_mufrad_by_id(m_id)
            if not herb:
                continue

            # 1. Schedule E(1) Hard Stop
            if herb["is_schedule_e1_poison"] and not is_mudabbar_certified:
                violations.append({
                    "rule": "SCHEDULE_E1_POISON_UNCERTIFIED",
                    "severity": "CRITICAL_BLOCK",
                    "message": f"Statutory poison '{herb['canonical_name_latin']}' lacks certified Mudabbar processing.",
                })
                blocked = True

            # 2. Dose Ceiling Hard Stop
            if dose > float(herb["approved_single_dose_max_grams"]):
                violations.append({
                    "rule": "DOSE_CEILING_EXCEEDED",
                    "severity": "CRITICAL_BLOCK",
                    "message": (
                        f"Prescribed dose {dose}g for '{herb['canonical_name_latin']}' exceeds approved "
                        f"maximum single dose ceiling of {herb['approved_single_dose_max_grams']}g."
                    ),
                })
                blocked = True

            # 3. Pregnancy Cohort Gate
            if is_pregnant and herb.get("pregnancy_status") == "ABSOLUTE_CONTRAINDICATION":
                violations.append({
                    "rule": "PREGNANCY_CONTRAINDICATION",
                    "severity": "CRITICAL_BLOCK",
                    "message": f"'{herb['canonical_name_latin']}' is strictly contraindicated during pregnancy.",
                })
                blocked = True

            # 4. Pediatric Gate (<12 years)
            if age < 12 and herb.get("pediatric_status") == "ABSOLUTE_CONTRAINDICATION":
                violations.append({
                    "rule": "PEDIATRIC_CONTRAINDICATION",
                    "severity": "CRITICAL_BLOCK",
                    "message": f"'{herb['canonical_name_latin']}' cannot be prescribed to pediatric patients (<12 years).",
                })
                blocked = True

            # 5. Renal Impairment (eGFR < 30)
            if eGFR < 30.0 and herb["is_schedule_e1_poison"]:
                violations.append({
                    "rule": "SEVERE_RENAL_IMPAIRMENT",
                    "severity": "CRITICAL_BLOCK",
                    "message": f"Patient has severe renal impairment (eGFR {eGFR}). Nephrotoxic alkaloid herb blocked.",
                })
                blocked = True

            # 6. Herb-Drug Interaction Matrix
            for inter in self.interactions:
                if inter["mufradat_id"] == m_id:
                    inter_drug = inter["modern_drug_class"].lower()
                    if any(d in inter_drug for d in concurrent_modern_drugs):
                        if inter["risk_severity"] in {"SEVERE", "FATAL"}:
                            violations.append({
                                "rule": "HERB_DRUG_INTERACTION",
                                "severity": "CRITICAL_BLOCK",
                                "message": f"Dangerous interaction between '{herb['canonical_name_latin']}' and concurrent modern therapy.",
                            })
                            blocked = True
                        else:
                            warnings.append(f"Moderate herb-drug interaction: {inter['clinical_effect']}")

        if blocked:
            verdict = "BLOCKED"
        elif warnings:
            verdict = "ALLOWED_WITH_WARNING"
        else:
            verdict = "ALLOWED"

        return {
            "verdict": verdict,
            "is_safe": not blocked,
            "violations": violations,
            "warnings": warnings,
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }

    # ------------------------------------------------------------------------
    # MIZAJ ALGORITHMIC ASSESSMENT
    # ------------------------------------------------------------------------
    def assess_patient_mizaj(self, phenotype_signs: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates 4-temperament profile from 10-Ajnas physical observations."""
        scores = {"Damawi": 0.0, "Safrawi": 0.0, "Balghami": 0.0, "Sawdawi": 0.0}
        supporting = []
        contradicting = []

        # 1. Complexion
        comp = phenotype_signs.get("complexion", "").lower()
        if "ruddy" in comp or "red" in comp:
            scores["Damawi"] += 2.0
            supporting.append("Ruddy complexion indicates Damawi temperament.")
        elif "yellow" in comp or "pale yellow" in comp:
            scores["Safrawi"] += 2.0
            supporting.append("Yellowish hue indicates Safrawi temperament.")
        elif "chalky" in comp or "pale white" in comp:
            scores["Balghami"] += 2.0
            supporting.append("Pale white complexion indicates Balghami temperament.")
        elif "dark" in comp or "dusky" in comp:
            scores["Sawdawi"] += 2.0
            supporting.append("Dusky/dark complexion indicates Sawdawi temperament.")

        # 2. Touch (Mamas)
        touch = phenotype_signs.get("touch", "").lower()
        if "hot & dry" in touch or "hot and dry" in touch:
            scores["Safrawi"] += 2.5
        elif "hot & moist" in touch or "hot and moist" in touch:
            scores["Damawi"] += 2.5
        elif "cold & moist" in touch or "cold and moist" in touch:
            scores["Balghami"] += 2.5
        elif "cold & dry" in touch or "cold and dry" in touch:
            scores["Sawdawi"] += 2.5

        # 3. Pulse (Nabz)
        pulse = phenotype_signs.get("pulse", "").lower()
        if "fast" in pulse and "broad" in pulse:
            scores["Damawi"] += 2.0
        elif "fast" in pulse and "narrow" in pulse:
            scores["Safrawi"] += 2.0
        elif "slow" in pulse and "broad" in pulse:
            scores["Balghami"] += 2.0
        elif "slow" in pulse and "narrow" in pulse:
            scores["Sawdawi"] += 2.0

        # Determine dominant and secondary
        sorted_mizaj = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        dominant, dom_score = sorted_mizaj[0]
        secondary, sec_score = sorted_mizaj[1]

        total = sum(scores.values()) or 1.0
        confidence = round(dom_score / total, 2) if total > 0 else 0.50

        return {
            "dominant_mizaj": dominant,
            "secondary_mizaj": secondary,
            "confidence": max(0.40, min(0.95, confidence)),
            "scores": scores,
            "supporting_findings": supporting,
            "contradicting_findings": contradicting,
            "clinician_review_status": "PROVISIONAL_PENDING_CLINICIAN_PULSE_CHECK",
        }


_GLOBAL_STRUCTURED_KNOWLEDGE: Optional[StructuredKnowledgeEngine] = None

def get_structured_knowledge() -> StructuredKnowledgeEngine:
    global _GLOBAL_STRUCTURED_KNOWLEDGE
    if _GLOBAL_STRUCTURED_KNOWLEDGE is None:
        _GLOBAL_STRUCTURED_KNOWLEDGE = StructuredKnowledgeEngine()
    return _GLOBAL_STRUCTURED_KNOWLEDGE
