"""
ZAYVORA Safety Firewall (ZAYVORA Clinical Architecture Specification v4.0 §13).

Runs BEFORE any Nuskha draft can be approved. Pure, deterministic function
— no LLM involved, no randomness, same input always gives same output.
That determinism is the whole point: a clinician needs to be able to
predict and trust exactly why a verdict fired.

Output verdict, in escalating order of severity:
    SAFE_TO_CONSIDER < CAUTION < MODIFY < DO_NOT_RECOMMEND < REFER

Enforces:
1. Red flag symptom screening for biomedical emergency referral.
2. Age, pregnancy, lactation, allergy, and comorbidity guardrails.
3. Statutory Schedule E(1) poisons verification: mandatory Mudabbar (detoxification)
   protocol compliance and statutory dosage ceilings.
4. Comprehensive clinical Drug-Herb and Herb-Herb interaction matrix (>30 rules).
5. Classical Unani Tazaad-e-Mizaj (temperamental conflict) evaluation.
"""
from __future__ import annotations

import re
import sys
import os
from typing import Any

# ── Mufradat 250 Registry Hard-Block Integration ─────────────────────────────
try:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../..")))
    from services.knowledge.app.data.mufradat_250_registry import (
        is_high_risk_blocked,
        get_mufrad_by_id,
        get_high_risk_28_registry,
    )
    _MUFRADAT_REGISTRY_AVAILABLE = True
except ImportError:
    _MUFRADAT_REGISTRY_AVAILABLE = False
    def is_high_risk_blocked(zmf_id: str) -> bool:
        return False
    def get_mufrad_by_id(zmf_id: str) -> dict | None:
        return None
    def get_high_risk_28_registry() -> dict:
        return {}
# ─────────────────────────────────────────────────────────────────────────────

VERDICT_ORDER = ["SAFE_TO_CONSIDER", "CAUTION", "MODIFY", "DO_NOT_RECOMMEND", "REFER"]

RED_FLAG_KEYWORDS = [
    "chest pain",
    "difficulty breathing",
    "severe bleeding",
    "suicidal",
    "loss of consciousness",
    "sudden weakness",
    "severe abdominal pain",
]

# ============================================================================
# 1. SCHEDULE E(1) STATUTORY POISONS DIRECTORY (DRUGS & COSMETICS RULES 1945)
# ============================================================================
SCHEDULE_E1_POISONS: dict[str, dict[str, Any]] = {
    "suranjan_talkh": {
        "canonical_name": "Suranjan Talkh",
        "synonyms": ["suranjan talkh", "suranjan-e-talkh", "bitter colchicum", "colchicum luteum", "colchicum autumnale", "suranjan"],
        "max_single_dose_mg": 250.0,
        "max_daily_dose_mg": 750.0,
        "mudabbar_protocol": "boiled in cow's milk (Sheer-e-Gao), skin peeled, embryo excised, and lightly fried in Almond Oil",
        "statutory_warning": "SCHEDULE E(1) POISON: Mitotic spindle poison (colchicine). Strict Mudabbar certification required.",
    },
    "kuchla": {
        "canonical_name": "Kuchla",
        "synonyms": ["kuchla", "azaraqi", "strychnos nux-vomica", "nux vomica", "kupilu"],
        "max_single_dose_mg": 65.0,
        "max_daily_dose_mg": 125.0,
        "mudabbar_protocol": "soaked in milk/Triphala, outer seed coat and embryo removed, fried in cow's ghee",
        "statutory_warning": "SCHEDULE E(1) POISON: Spinal neurotoxin (strychnine). Fatal convulsions if unpurified.",
    },
    "bhilawa": {
        "canonical_name": "Bhilawa",
        "synonyms": ["bhilawa", "hab-ul-fahm", "marking nut", "semecarpus anacardium", "bhallataka"],
        "max_single_dose_mg": 125.0,
        "max_daily_dose_mg": 250.0,
        "mudabbar_protocol": "thalamus removed, treated with brick powder (Surkhi) to absorb corrosive phenolic resins, washed and boiled in milk",
        "statutory_warning": "SCHEDULE E(1) POISON: Corrosive vesicant (bhilawanol). Must undergo brick-dust Shodhana.",
    },
    "afeem": {
        "canonical_name": "Afeem",
        "synonyms": ["afeem", "afyoon", "opium", "papaver somniferum", "taryaaq"],
        "max_single_dose_mg": 30.0,
        "max_daily_dose_mg": 65.0,
        "mudabbar_protocol": "purified in Arq-e-Gulab (rose water) and filtered 7 times",
        "statutory_warning": "SCHEDULE E(1) / NDPS NARCOTIC: Controlled narcotic. High respiratory depression and addiction hazard.",
    },
    "bhang": {
        "canonical_name": "Bhang",
        "synonyms": ["bhang", "qinnab", "cannabis sativa", "vijaya", "indian hemp"],
        "max_single_dose_mg": 250.0,
        "max_daily_dose_mg": 500.0,
        "mudabbar_protocol": "washed in cold water 21 times and fried with cow's ghee",
        "statutory_warning": "SCHEDULE E(1) POISON: Psychotropic cannabinoid. Use only Mudabbar processed leaves.",
    },
    "dhatura": {
        "canonical_name": "Dhatura",
        "synonyms": ["dhatura", "jauz-e-masir", "datura metel", "datura stramonium", "thorn apple"],
        "max_single_dose_mg": 30.0,
        "max_daily_dose_mg": 60.0,
        "mudabbar_protocol": "seeds steeped and boiled in cow's milk, seed coat removed",
        "statutory_warning": "SCHEDULE E(1) POISON: Potent anticholinergic deliriant (scopolamine/atropine).",
    },
    "jamalgota": {
        "canonical_name": "Jamalgota",
        "synonyms": ["jamalgota", "habb-us-salateen", "croton tiglium", "jayapala"],
        "max_single_dose_mg": 30.0,
        "max_daily_dose_mg": 60.0,
        "mudabbar_protocol": "cotyledonary embryo excised and boiled in milk between cloth bundle",
        "statutory_warning": "SCHEDULE E(1) POISON: Drastic hydragogue cathartic. Severe dehydration risk if unpurified.",
    },
    "bish": {
        "canonical_name": "Bish",
        "synonyms": ["bish", "meetha teeliya", "aconitum ferox", "aconitum chasmanthum", "vatsanabha", "monkshood"],
        "max_single_dose_mg": 15.0,
        "max_daily_dose_mg": 30.0,
        "mudabbar_protocol": "processed in Gomutra and cow's milk for 3 days until softened",
        "statutory_warning": "SCHEDULE E(1) POISON: Lethal cardiotoxin (aconitine). Raw root is strictly banned.",
    },
    "samm_ul_far": {
        "canonical_name": "Samm-ul-Far",
        "synonyms": ["samm-ul-far", "sankhiya", "arsenic trioxide", "white arsenic"],
        "max_single_dose_mg": 2.0,
        "max_daily_dose_mg": 5.0,
        "mudabbar_protocol": "calcined with plant juices as certified classical Kushta",
        "statutory_warning": "SCHEDULE E(1) POISON: Heavy metal arsenic. Prohibited except in standardized Kushta.",
    },
    "seemab": {
        "canonical_name": "Seemab",
        "synonyms": ["seemab", "para", "elemental mercury", "quicksilver", "rasendra"],
        "max_single_dose_mg": 15.0,
        "max_daily_dose_mg": 30.0,
        "mudabbar_protocol": "triturated with sulphur for 72 hours into non-metallic Kajli/Kushta",
        "statutory_warning": "SCHEDULE E(1) POISON: Mercury. Strictly prohibited except in certified Kajli.",
    },
    "kaner": {
        "canonical_name": "Kaner",
        "synonyms": ["kaner", "kharzahra", "nerium indicum", "nerium oleander"],
        "max_single_dose_mg": 30.0,
        "max_daily_dose_mg": 60.0,
        "mudabbar_protocol": "boiled in milk before classical formulation",
        "statutory_warning": "SCHEDULE E(1) POISON: Cardiac glycoside toxin. High arrhythmia risk.",
    },
}

# ============================================================================
# 2. CLINICAL DRUG-HERB & HERB-HERB INTERACTION RULES (>30 RULES)
# ============================================================================
INTERACTION_RULES: list[dict[str, Any]] = [
    # --- Anticoagulants / Antiplatelets ---
    {
        "medication_keyword": "warfarin",
        "ingredient_keyword": "",
        "verdict": "CAUTION",
        "reason": "Patient is on an anticoagulant (warfarin) — many botanicals affect bleeding risk; verify each ingredient individually before finalizing.",
    },
    {
        "medication_keyword": "anticoagulant",
        "ingredient_keyword": "",
        "verdict": "CAUTION",
        "reason": "Patient is on anticoagulant therapy — risk of hemostatic interference; review bleeding parameters.",
    },
    {
        "medication_keyword": "warfarin",
        "ingredient_keyword": "garlic",
        "verdict": "MODIFY",
        "reason": "High-dose garlic can potentiate anticoagulant effect — reduce dose or substitute (Badal) before proceeding.",
    },
    {
        "medication_keyword": "anticoagulant",
        "ingredient_keyword": "garlic",
        "verdict": "MODIFY",
        "reason": "Garlic possesses antiplatelet properties and synergizes with anticoagulants, elevating major hemorrhage risk.",
    },
    {
        "medication_keyword": "warfarin",
        "ingredient_keyword": "ginger",
        "verdict": "MODIFY",
        "reason": "Ginger (Zanjabeel) inhibits thromboxane synthetase and synergizes with warfarin, increasing bleeding risk.",
    },
    {
        "medication_keyword": "warfarin",
        "ingredient_keyword": "zanjabeel",
        "verdict": "MODIFY",
        "reason": "Zanjabeel (Ginger) inhibits thromboxane synthetase and synergizes with warfarin, increasing bleeding risk.",
    },
    {
        "medication_keyword": "warfarin",
        "ingredient_keyword": "ginkgo",
        "verdict": "MODIFY",
        "reason": "Ginkgo biloba inhibits platelet activating factor (PAF), compounding warfarin anticoagulation; risk of spontaneous hemorrhage.",
    },
    {
        "medication_keyword": "warfarin",
        "ingredient_keyword": "guggul",
        "verdict": "MODIFY",
        "reason": "Guggul exhibits hypoprothrombinemic activity that potentiates warfarin; requires INR monitoring and dose titration.",
    },
    {
        "medication_keyword": "aspirin",
        "ingredient_keyword": "asal-us-soos",
        "verdict": "MODIFY",
        "reason": "Asal-us-Soos (Licorice) combined with Aspirin increases gastrointestinal mucosal ulceration and bleeding hazard.",
    },
    {
        "medication_keyword": "aspirin",
        "ingredient_keyword": "licorice",
        "verdict": "MODIFY",
        "reason": "Licorice combined with Aspirin increases gastrointestinal mucosal ulceration and bleeding hazard.",
    },
    {
        "medication_keyword": "clopidogrel",
        "ingredient_keyword": "ginkgo",
        "verdict": "MODIFY",
        "reason": "Dual antiplatelet inhibition from Clopidogrel and Ginkgo biloba markedly elevates intracranial/GI bleeding risk.",
    },
    {
        "medication_keyword": "anticoagulant",
        "ingredient_keyword": "curcumin",
        "verdict": "CAUTION",
        "reason": "High-dose curcumin exhibits mild antiplatelet effects; monitor coagulation indices.",
    },

    # --- Antidiabetics ---
    {
        "medication_keyword": "insulin",
        "ingredient_keyword": "",
        "verdict": "CAUTION",
        "reason": "Patient is on insulin — hypoglycemia-potentiating ingredients could compound blood-glucose lowering.",
    },
    {
        "medication_keyword": "metformin",
        "ingredient_keyword": "karela",
        "verdict": "MODIFY",
        "reason": "Karela (Momordica charantia) contains charantin and vicine which synergize with Metformin, risking severe hypoglycemia.",
    },
    {
        "medication_keyword": "insulin",
        "ingredient_keyword": "karela",
        "verdict": "MODIFY",
        "reason": "Karela possesses insulin-mimetic polypeptide-p; combined with exogenous insulin, this poses acute hypoglycemic shock risk.",
    },
    {
        "medication_keyword": "metformin",
        "ingredient_keyword": "gurmar",
        "verdict": "MODIFY",
        "reason": "Gurmar (Gymnema sylvestre) stimulates endogenous islet secretion and compounds Metformin; blood glucose titration mandatory.",
    },
    {
        "medication_keyword": "antidiabetic",
        "ingredient_keyword": "methi",
        "verdict": "MODIFY",
        "reason": "Methi (Fenugreek) delays gastrointestinal carbohydrate absorption and compounds antidiabetic therapy.",
    },

    # --- Cardiovascular & Antihypertensives ---
    {
        "medication_keyword": "antihypertensive",
        "ingredient_keyword": "asal-us-soos",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Asal-us-Soos (Licorice) causes pseudoaldosteronism, fluid retention, and severe hypertension, directly counteracting antihypertensive therapy.",
    },
    {
        "medication_keyword": "antihypertensive",
        "ingredient_keyword": "licorice",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Licorice causes pseudoaldosteronism, sodium retention, and hypokalemia, directly antagonizing blood pressure control.",
    },
    {
        "medication_keyword": "amlodipine",
        "ingredient_keyword": "asal-us-soos",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Asal-us-Soos inhibits 11-beta-HSD2, causing mineralocorticoid excess that overcomes calcium channel blockade.",
    },
    {
        "medication_keyword": "lisinopril",
        "ingredient_keyword": "asal-us-soos",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Licorice antagonizes ACE inhibitor action via volume overload and systemic vascular resistance elevation.",
    },
    {
        "medication_keyword": "digoxin",
        "ingredient_keyword": "asal-us-soos",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Licorice-induced hypokalemia severely sensitizes myocardium to Digoxin, risking fatal ventricular arrhythmias.",
    },
    {
        "medication_keyword": "digoxin",
        "ingredient_keyword": "licorice",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Licorice-induced hypokalemia severely sensitizes myocardium to Digoxin, risking fatal ventricular arrhythmias.",
    },
    {
        "medication_keyword": "digoxin",
        "ingredient_keyword": "sana",
        "verdict": "MODIFY",
        "reason": "Sana Makki (Senna) anthraquinones induce colonic potassium loss; hypokalemia dramatically compounds Digoxin toxicity.",
    },

    # --- Neuropsychiatric / Antidepressants / Sedatives ---
    {
        "medication_keyword": "fluoxetine",
        "ingredient_keyword": "harmal",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Harmal (Peganum harmala) harmaline is a potent reversible MAO-A inhibitor; combination with SSRIs precipitates fatal Serotonin Syndrome.",
    },
    {
        "medication_keyword": "ssri",
        "ingredient_keyword": "harmal",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Harmal MAO-A inhibition combined with SSRI therapy triggers severe hyperthermia, clonus, and Serotonin Syndrome.",
    },
    {
        "medication_keyword": "antidepressant",
        "ingredient_keyword": "st. john's wort",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "St. John's Wort combined with antidepressants carries high risk of Serotonin Syndrome and CYP3A4 pharmacokinetic induction.",
    },
    {
        "medication_keyword": "lithium",
        "ingredient_keyword": "gokhru",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Gokhru (Tribulus terrestris) natriuretic diuresis reduces renal clearance of Lithium, leading to acute lithium neurotoxicity.",
    },
    {
        "medication_keyword": "sedative",
        "ingredient_keyword": "afeem",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Synergistic central nervous system and respiratory depression between prescription sedatives and Afeem (Opium); risk of fatal apnea.",
    },
    {
        "medication_keyword": "sedative",
        "ingredient_keyword": "bhang",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Additive psychoactive sedation, severe psychomotor impairment, and postural hypotension.",
    },
    {
        "medication_keyword": "sedative",
        "ingredient_keyword": "valerian",
        "verdict": "CAUTION",
        "reason": "Additive GABAergic sedation; advise patient against operating machinery or driving.",
    },

    # --- Statins ---
    {
        "medication_keyword": "statin",
        "ingredient_keyword": "grapefruit",
        "verdict": "MODIFY",
        "reason": "Grapefruit / Naranj furanocoumarins irreversibly inhibit intestinal CYP3A4, causing massive statin accumulation and rhabdomyolysis.",
    },
    {
        "medication_keyword": "atorvastatin",
        "ingredient_keyword": "naranj",
        "verdict": "MODIFY",
        "reason": "Naranj (Citrus aurantium) inhibits CYP3A4-mediated statin clearance, increasing risk of myopathy and acute renal injury.",
    },

    # --- Endocrine / Thyroid ---
    {
        "medication_keyword": "levothyroxine",
        "ingredient_keyword": "asgandh",
        "verdict": "CAUTION",
        "reason": "Asgandh (Ashwagandha) stimulates thyroid gland activity and increases serum T3/T4 levels; monitor thyroid profile.",
    },
    {
        "medication_keyword": "levothyroxine",
        "ingredient_keyword": "ashwagandha",
        "verdict": "CAUTION",
        "reason": "Ashwagandha increases thyroid hormone production, risking additive hyperthyroid symptoms in patients on Levothyroxine.",
    },

    # --- Chelation / Mineral Binding ---
    {
        "medication_keyword": "iron",
        "ingredient_keyword": "amla",
        "verdict": "MODIFY",
        "reason": "Tannins in Amla form unabsorbable iron-tannate chelates; separate administration times by at least 2 hours.",
    },
    {
        "medication_keyword": "iron",
        "ingredient_keyword": "triphala",
        "verdict": "MODIFY",
        "reason": "Triphala hydrolyzable tannins bind oral iron supplements, completely abrogating intestinal iron bioavailability.",
    },
    {
        "medication_keyword": "ciprofloxacin",
        "ingredient_keyword": "kushta",
        "verdict": "MODIFY",
        "reason": "Multivalent cations in classical Kushtas chelate fluoroquinolones, preventing antibacterial absorption; separate doses by 3 hours.",
    },

    # --- Immunosuppressants ---
    {
        "medication_keyword": "immunosuppressant",
        "ingredient_keyword": "",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Patient is on immunosuppressant therapy — immunomodulatory botanicals risk interfering with treatment; specialist review required first.",
    },
    {
        "medication_keyword": "tacrolimus",
        "ingredient_keyword": "kalonji",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Kalonji (Nigella sativa) thymoquinone stimulates T-helper cell responses, directly opposing Tacrolimus graft protection.",
    },
    {
        "medication_keyword": "cyclosporine",
        "ingredient_keyword": "giloy",
        "verdict": "DO_NOT_RECOMMEND",
        "reason": "Giloy (Tinospora cordifolia) stimulates macrophages and cytokine secretion, creating high risk of acute organ transplant rejection.",
    },

    # --- NSAIDs ---
    {
        "medication_keyword": "diclofenac",
        "ingredient_keyword": "garlic",
        "verdict": "MODIFY",
        "reason": "Concomitant NSAID and garlic therapy impairs platelet function while compromising gastric mucosal protection; elevated ulcer risk.",
    },
    {
        "medication_keyword": "ibuprofen",
        "ingredient_keyword": "ginkgo",
        "verdict": "MODIFY",
        "reason": "Synergistic antiplatelet action increases risk of gastrointestinal hemorrhage.",
    },
]


def _escalate(current: str, candidate: str) -> str:
    return candidate if VERDICT_ORDER.index(candidate) > VERDICT_ORDER.index(current) else current


def _parse_dose_mg(ingredient: dict[str, Any]) -> float | None:
    """Extract dose in milligrams from either structured dose_mg or miqdaar string."""
    if ingredient.get("dose_mg") is not None:
        try:
            return float(ingredient["dose_mg"])
        except (ValueError, TypeError):
            pass

    miqdaar = (ingredient.get("miqdaar") or "").strip().lower()
    if not miqdaar:
        return None

    # Match patterns like '250mg', '250 mg', '0.5g', '1g', '1 masha'
    mg_match = re.search(r"(\d+(?:\.\d+)?)\s*mg", miqdaar)
    if mg_match:
        return float(mg_match.group(1))

    g_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:g|gm|gram)", miqdaar)
    if g_match:
        return float(g_match.group(1)) * 1000.0

    masha_match = re.search(r"(\d+(?:\.\d+)?)\s*masha", miqdaar)
    if masha_match:
        return float(masha_match.group(1)) * 970.0

    ratti_match = re.search(r"(\d+(?:\.\d+)?)\s*ratti", miqdaar)
    if ratti_match:
        return float(ratti_match.group(1)) * 120.0

    return None


def _check_schedule_e1_poisons(ingredients: list[dict[str, Any]]) -> tuple[str, list[str]]:
    verdict = "SAFE_TO_CONSIDER"
    reasons: list[str] = []

    # ── GATE 0: Mufradat 250 Hard-Block (ZMF Registry Integration) ────────────
    # Any ingredient carrying a ZMF ID that is in the HIGH_RISK_28 list
    # receives an automatic DO_NOT_RECOMMEND regardless of Mudabbar status.
    if _MUFRADAT_REGISTRY_AVAILABLE:
        hr_registry = get_high_risk_28_registry()
        for ing in ingredients:
            zmf_id = (ing.get("zmf_id") or ing.get("id") or "").strip().upper()
            ing_name = ing.get("name", "").strip()

            is_purified = (
                ing.get("shodhana_certified") is True
                or ing.get("is_mudabbar") is True
                or "shodhana" in ing_name.lower()
                or "mudabbar" in ing_name.lower()
            )

            # Check by explicit ZMF ID
            if zmf_id and is_high_risk_blocked(zmf_id):
                rec = hr_registry.get(zmf_id, {})
                target_verdict = "CAUTION" if is_purified else "DO_NOT_RECOMMEND"
                verdict = _escalate(verdict, target_verdict)
                reasons.append(
                    f"🚫 MUFRADAT-250 HARD BLOCK [{zmf_id}]: '{ing_name or rec.get('name', zmf_id)}' "
                    f"is classified HIGH_RISK in the ZMF Canonical Registry. "
                    f"Primary toxin: {rec.get('primary_toxin', 'N/A')}. "
                    f"Clinical risk: {rec.get('clinical_risk', 'See registry.')} "
                    f"Restriction: {rec.get('restriction', 'AI_BLOCKED — clinician specialist sign-off required.')} "
                    f"[Category: {rec.get('category', 'Restricted Substance')}]"
                )
                # Suranjan Talkh (ZMF-002) requires explicit Shodhana certificate
                if zmf_id == "ZMF-002" and not is_purified:
                    reasons.append(
                        "⛔ SURANJAN SHODHANA ENFORCEMENT [ZMF-002]: Suranjan Talkh (Colchicum luteum Baker) "
                        "requires a verified classical Shodhana certificate — soaked in vinegar (Sirka) for "
                        "3 days, then boiled in cow's milk (Sheer-e-Gao) — before any dispensing. "
                        "Set ingredient field 'shodhana_certified': true to acknowledge compliance. "
                        "Without this, the formulation MUST NOT BE DISPENSED under PCIM&H / CDSCO norms."
                    )
            else:
                # Also name-based scan against hr_registry for untagged ingredients
                for zmf_key, rec in hr_registry.items():
                    rec_name_lower = rec.get("name", "").lower()
                    if rec_name_lower and rec_name_lower in ing_name.lower():
                        target_verdict = "CAUTION" if is_purified else "DO_NOT_RECOMMEND"
                        verdict = _escalate(verdict, target_verdict)
                        reasons.append(
                            f"🚫 MUFRADAT-250 HARD BLOCK (name match) [{zmf_key}]: "
                            f"'{ing_name}' matches HIGH_RISK substance '{rec.get('name')}'. "
                            f"Primary toxin: {rec.get('primary_toxin', 'N/A')}. "
                            f"Restriction: {rec.get('restriction', 'AI_BLOCKED.')}"
                        )
                        break
    # ─────────────────────────────────────────────────────────────────────────

    for ing in ingredients:
        name = ing.get("name", "").strip().lower()
        if not name:
            continue

        matched_spec = None
        for key, spec in SCHEDULE_E1_POISONS.items():
            if any(syn in name for syn in spec["synonyms"]):
                matched_spec = spec
                break

        if not matched_spec:
            continue

        # 1. Detoxification check (Mandatory Mudabbar)
        is_mudabbar = (
            ing.get("is_mudabbar") is True
            or "mudabbar" in name
            or "shodhit" in name
            or "purified" in name
        )

        if not is_mudabbar:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append(
                f"SCHEDULE E(1) POISON: '{ing.get('name')}' is strictly contraindicated in unpurified (Kham) state. "
                f"It MUST be certified Mudabbar ({matched_spec['mudabbar_protocol']}) before clinical dispensing "
                f"under Drugs & Cosmetics Rules 1945."
            )
        else:
            # Marked Mudabbar, still requires statutory vigilance
            verdict = _escalate(verdict, "CAUTION")
            reasons.append(
                f"SCHEDULE E(1) Controlled Substance: '{ing.get('name')}' certified Mudabbar. "
                f"{matched_spec['statutory_warning']}"
            )

        # 2. Statutory dose ceiling checks
        dose_mg = _parse_dose_mg(ing)
        if dose_mg is not None:
            if dose_mg > matched_spec["max_single_dose_mg"]:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append(
                    f"SCHEDULE E(1) DOSE CEILING EXCEEDED: '{ing.get('name')}' dose ({dose_mg:.1f} mg) exceeds "
                    f"statutory maximum single safe dose of {matched_spec['max_single_dose_mg']:.1f} mg."
                )
            if dose_mg > matched_spec["max_daily_dose_mg"]:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append(
                    f"SCHEDULE E(1) DOSE CEILING EXCEEDED: '{ing.get('name')}' dose ({dose_mg:.1f} mg) exceeds "
                    f"statutory maximum daily safe dose of {matched_spec['max_daily_dose_mg']:.1f} mg."
                )

    return verdict, reasons


def _check_tazaad_e_mizaj(patient_context: dict, ingredients: list[dict[str, Any]]) -> tuple[str, list[str]]:
    """
    Classical Unani Tazaad-e-Mizaj (Temperamental Conflict) Engine:
    1. Detects pairings of extreme Hot (Degree 3-4) and extreme Cold (Degree 3-4) botanicals without Musleh.
    2. Evaluates patient's pathological acute dyscrasia vs ingredient Mizaj.
    """
    verdict = "SAFE_TO_CONSIDER"
    reasons: list[str] = []

    hot_extremes: list[dict[str, Any]] = []
    cold_extremes: list[dict[str, Any]] = []

    for ing in ingredients:
        name = ing.get("name", "").lower()
        temp = (ing.get("mizaj_temperament") or "").capitalize()
        hc = ing.get("mizaj_degree_hc")

        # Inherent classification for known high-degree ingredients
        if not hc:
            if any(k in name for k in ["suranjan", "kuchla", "filfil siyah", "zanjabeel", "bhilawa", "bish"]):
                hc = 3
                temp = "Safrawi"
            elif any(k in name for k in ["afeem", "dhatura", "sandal safed", "kahu"]):
                hc = 3
                temp = "Saudawi"

        if hc and hc >= 3:
            if temp in ("Safrawi", "Damwi"):
                hot_extremes.append({"name": ing.get("name"), "degree": hc, "musleh": ing.get("musleh")})
            elif temp in ("Saudawi", "Balghami"):
                cold_extremes.append({"name": ing.get("name"), "degree": hc, "musleh": ing.get("musleh")})

    # Rule A: Extreme Hot vs Extreme Cold in the same formula without an explicit harmonizing Musleh
    if hot_extremes and cold_extremes:
        has_musleh = any(i.get("musleh") for i in ingredients)
        if not has_musleh:
            verdict = _escalate(verdict, "CAUTION")
            h_names = ", ".join(h["name"] for h in hot_extremes)
            c_names = ", ".join(c["name"] for c in cold_extremes)
            reasons.append(
                f"Tazaad-e-Mizaj (Temperamental Conflict): Extreme Hot ingredients ({h_names}) combined with "
                f"Extreme Cold ingredients ({c_names}) without a balancing Musleh (corrective harmonizer)."
            )

    # Rule B: Extreme Hot drug in acute hot dyscrasia (Su-e-Mizaj Haar / active fever)
    complaint = (patient_context.get("chief_complaint") or "").lower()
    comorbidities = " ".join(patient_context.get("comorbidities") or []).lower()
    has_hot_dyscrasia = any(k in complaint or k in comorbidities for k in ["fever", "bukhar", "humma", "safra", "su-e-mizaj haar"])

    if has_hot_dyscrasia and hot_extremes:
        for h in hot_extremes:
            if not h.get("musleh"):
                verdict = _escalate(verdict, "MODIFY")
                reasons.append(
                    f"Mizaj Contraindication: Extreme Hot (Degree {h['degree']}) ingredient '{h['name']}' prescribed in "
                    f"acute hot dyscrasia (Su-e-Mizaj Haar / fever) without a cooling Musleh."
                )

    return verdict, reasons


def run_safety_firewall(*, patient_context: dict, ingredients: list[dict]) -> dict:
    """
    patient_context: {
        "age": int | None,
        "pregnancy_status": "pregnant" | "not_pregnant" | "unknown" | "not_applicable",
        "lactation_status": "yes" | "no",
        "allergies": list[str],
        "current_medications": list[str],
        "comorbidities": list[str],
        "chief_complaint": str,  # screened for red-flag keywords
    }
    ingredients: [
        {
            "name": str,
            "is_mudabbar": bool | None,
            "mudabbar_process": str | None,
            "dose_mg": float | None,
            "miqdaar": str | None,
            "musleh": str | None,
            "badal": str | None,
            "mizaj_temperament": str | None,
            "mizaj_degree_hc": int | None,
            "mizaj_degree_wd": int | None,
        },
        ...
    ]
    """
    verdict = "SAFE_TO_CONSIDER"
    reasons: list[str] = []

    # 1. Red flag symptoms screening
    complaint = (patient_context.get("chief_complaint") or "").lower()
    for kw in RED_FLAG_KEYWORDS:
        if kw in complaint:
            verdict = _escalate(verdict, "REFER")
            reasons.append(f"Red flag in presenting complaint: '{kw}' — biomedical emergency evaluation takes priority.")

    # 2. Age checks
    age = patient_context.get("age")
    if age is not None:
        if age < 12:
            verdict = _escalate(verdict, "CAUTION")
            reasons.append("Pediatric patient (<12) — dosing and formulation require pediatric-specific review.")
        if age >= 70:
            verdict = _escalate(verdict, "CAUTION")
            reasons.append("Elderly patient (≥70) — increased sensitivity to dosing and higher interaction risk.")

    # 3. Pregnancy & Lactation
    if patient_context.get("pregnancy_status") == "pregnant":
        verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
        reasons.append("Patient is pregnant — most Ilaj bil-Dawa formulations are contraindicated pending ingredient-specific safety review.")

    if patient_context.get("lactation_status") == "yes":
        verdict = _escalate(verdict, "CAUTION")
        reasons.append("Patient is lactating — verify every ingredient for lactation safety before finalizing.")

    # 4. Allergy matching
    allergies = [a.lower() for a in (patient_context.get("allergies") or [])]
    ingredient_names = [i.get("name", "").lower() for i in ingredients]
    for allergy in allergies:
        for ing_name in ingredient_names:
            if allergy and allergy in ing_name:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append(f"Proposed ingredient '{ing_name}' conflicts with a documented allergy ('{allergy}').")

    # 5. Drug-herb & drug-drug interactions
    medications = [m.lower() for m in (patient_context.get("current_medications") or [])]
    for rule in INTERACTION_RULES:
        med_hit = any(rule["medication_keyword"] in med for med in medications)
        if not med_hit:
            continue
        if rule["ingredient_keyword"] == "":
            verdict = _escalate(verdict, rule["verdict"])
            reasons.append(rule["reason"])
        else:
            ing_hit = any(rule["ingredient_keyword"] in name for name in ingredient_names)
            if ing_hit:
                verdict = _escalate(verdict, rule["verdict"])
                reasons.append(rule["reason"])

    # 6. Comorbidities check
    comorbidities = [c.lower() for c in (patient_context.get("comorbidities") or [])]
    renal_hepatic = [c for c in comorbidities if "renal" in c or "kidney" in c or "hepatic" in c or "liver" in c]
    if renal_hepatic:
        verdict = _escalate(verdict, "CAUTION")
        reasons.append(f"Renal/hepatic comorbidity noted ({', '.join(renal_hepatic)}) — dose adjustment and ingredient clearance review required.")

    # 7. Schedule E(1) Statutory Poison & Mudabbar checks
    e1_verdict, e1_reasons = _check_schedule_e1_poisons(ingredients)
    verdict = _escalate(verdict, e1_verdict)
    reasons.extend(e1_reasons)

    # 8. Classical Unani Tazaad-e-Mizaj (Temperamental Conflict) check
    mizaj_verdict, mizaj_reasons = _check_tazaad_e_mizaj(patient_context, ingredients)
    verdict = _escalate(verdict, mizaj_verdict)
    reasons.extend(mizaj_reasons)

    if not reasons:
        reasons.append("No safety concerns identified from structured data on file. Practitioner clinical judgment remains required regardless.")

    return {
        "verdict": verdict,
        "reasons": reasons,
        "requiresPractitionerSignoff": True,
    }


# -----------------------------------------------------------------------------
# Master Drug-Herb Interaction & Universal Contraindication Checker
# -----------------------------------------------------------------------------
try:
    from services.knowledge.app.data.drug_interactions_master import (
        check_drug_herb_interactions as master_check_interactions,
        get_universal_contraindications as master_get_universal_contraindications,
    )
except ImportError:
    master_check_interactions = None
    master_get_universal_contraindications = None


def run_master_drug_herb_safety_audit(
    ingredients: list[Any],
    current_medications: list[str],
    is_pregnant: bool = False,
    is_lactating: bool = False,
    egfr: float | None = None
) -> dict[str, Any]:
    """
    Direct audit against the 11 Master Drug-Herb Interactions and Universal Contraindications.
    Accepts SKU strings, ingredient names, or ingredient dicts.
    """
    raw_names = []
    for item in ingredients:
        if isinstance(item, str):
            raw_names.append(item)
        elif isinstance(item, dict):
            raw_names.append(item.get("name") or item.get("sku") or "")
            
    detected_interactions = []
    if master_check_interactions:
        detected_interactions = master_check_interactions(raw_names, current_medications)

    contraindication_alerts = []
    if master_get_universal_contraindications:
        u_map = master_get_universal_contraindications()
        if is_pregnant:
            for item in u_map.get("PREGNANCY", []):
                for ing in raw_names:
                    sku = item.split()[0]
                    if sku.lower() in ing.lower() or any(w.lower() in item.lower() for w in ing.split()):
                        contraindication_alerts.append(f"PREGNANCY CONTRAINDICATION: {item}")
        if is_lactating:
            for item in u_map.get("LACTATION", []):
                for ing in raw_names:
                    sku = item.split()[0]
                    if sku.lower() in ing.lower() or any(w.lower() in item.lower() for w in ing.split()):
                        contraindication_alerts.append(f"LACTATION CONTRAINDICATION: {item}")
        if egfr is not None and egfr < 30.0:
            for item in u_map.get("SEVERE_RENAL_IMPAIRMENT_EGFR_UNDER_30", []):
                for ing in raw_names:
                    sku = item.split()[0]
                    if sku.lower() in ing.lower() or any(w.lower() in item.lower() for w in ing.split()):
                        contraindication_alerts.append(f"SEVERE RENAL CONTRAINDICATION (eGFR < 30): {item}")

    is_safe = len(detected_interactions) == 0 and len(contraindication_alerts) == 0
    severity = "SAFE"
    if detected_interactions:
        max_sev = max(i.get("severity", "LOW") for i in detected_interactions)
        severity = max_sev
    if contraindication_alerts:
        severity = "CRITICAL"

    return {
        "is_safe": is_safe,
        "severity": severity,
        "interactions_count": len(detected_interactions),
        "interactions": detected_interactions,
        "contraindications_count": len(contraindication_alerts),
        "contraindications": contraindication_alerts,
        "requires_clinician_override": not is_safe
    }


# =====================================================================
# CP-AFUM / AFUF RED FLAGS, FORBIDDEN LIST & HERB-DRUG MATRIX
# Source: Dr. Irfan Ashraf — CP-AFUM Textbook Chapters 5 & 6, Table 6.1
# =====================================================================

CP_AFUM_RED_FLAGS = [
    {
        "name": "Elevated SGPT / Acute Hepatopathy",
        "threshold": "SGPT > 100 U/L",
        "check_fn": lambda d: d.get("sgpt", 0) > 100 or d.get("alt", 0) > 100,
        "referral": "Hepatology — rule out viral hepatitis, NASH, or hepatocellular carcinoma.",
        "zayvora_role": "Adjunctive liver support only — do not prescribe Phase 2 independently."
    },
    {
        "name": "Severe Autoimmune Thyroiditis",
        "threshold": "Anti-TPO > 300 IU/mL",
        "check_fn": lambda d: d.get("anti_tpo", 0) > 300,
        "referral": "Endocrinology — aggressive Hashimoto requiring specialist immunotherapy assessment.",
        "zayvora_role": "ThyroMet Axis adjunctive only under specialist guidance."
    },
    {
        "name": "Critically Diminished Ovarian Reserve",
        "threshold": "AMH < 0.3 ng/mL",
        "check_fn": lambda d: 0 < d.get("amh", 999) < 0.3,
        "referral": "Reproductive Endocrinology — IVF pathway discussion required.",
        "zayvora_role": "OvaSync may support but primary management is specialist-led."
    },
    {
        "name": "Azoospermia",
        "threshold": "Zero sperm on semen analysis",
        "check_fn": lambda d: d.get("sperm_count", 999) == 0 or d.get("azoospermia", False),
        "referral": "Urology / Reproductive Medicine — structural/genetic investigation (biopsy, ICSI candidacy).",
        "zayvora_role": "Not a ZAYVORA solo case — ManiVital Pro as adjunct only."
    },
    {
        "name": "Severe Uncontrolled Diabetes",
        "threshold": "HbA1c > 10%",
        "check_fn": lambda d: d.get("hba1c", 0) > 10.0,
        "referral": "Endocrinology — severe T2DM requires insulin or multi-drug management.",
        "zayvora_role": "MetaboCore adjunctive — do not solo manage severe T2DM."
    },
    {
        "name": "Overt Primary Hypothyroidism",
        "threshold": "TSH > 10 mIU/L",
        "check_fn": lambda d: d.get("tsh", 0) > 10.0,
        "referral": "General Medicine / Endocrinology — conventional levothyroxine co-prescription.",
        "zayvora_role": "ThyroMet Axis adjunctive to conventional thyroid replacement."
    },
    {
        "name": "Psychiatric Emergency",
        "threshold": "Suicidal ideation, severe psychosis, acute mania",
        "check_fn": lambda d: d.get("suicidal_ideation", False) or d.get("psychiatric_emergency", False),
        "referral": "IMMEDIATE psychiatric referral — same day or emergency services.",
        "zayvora_role": "No ZAYVORA role in acute psychiatric emergency management."
    },
    {
        "name": "Unexplained Significant Weight Loss",
        "threshold": ">10% body weight unintentional loss over 3 months",
        "check_fn": lambda d: d.get("unexplained_weight_loss_pct", 0) > 10.0,
        "referral": "Oncological screen mandatory before any protocol — exclude malignancy.",
        "zayvora_role": "No ZAYVORA protocol until red flag cause excluded."
    }
]

FORBIDDEN_FORMULATION_LIST = [
    "DHEA", "pregnenolone", "synthetic testosterone", "synthetic estrogen", "anabolic steroid",
    "Ephedra", "Ephedrine", "Yohimbine", "Aristolochia", "Kava-Kava", "Kava", "Raw Kuchla",
    "Raw Shingraf", "Raw Suranjan", "Raw Jamalgota"
]

AFUF_HERB_DRUG_RULES = [
    {
        "herb": "Berberine",
        "drug": "Metformin",
        "severity": "SAFE_WITH_MONITORING",
        "mechanism": "Additive AMPK activation — enhanced glucose-lowering.",
        "action": "Safe combination; monitor for hypoglycemia if metformin dose is high."
    },
    {
        "herb": "Berberine",
        "drug": "Insulin",
        "severity": "HIGH_CAUTION",
        "mechanism": "Additive glucose lowering — cumulative hypoglycemia risk.",
        "action": "CAUTION: Monitor glucose weekly; coordinate dose reduction with physician."
    },
    {
        "herb": "Berberine",
        "drug": "Statins",
        "severity": "MODERATE_CAUTION",
        "mechanism": "Berberine inhibits CYP3A4 -> increased statin plasma concentration.",
        "action": "CAUTION: Monitor for myopathy (muscle pain, CK elevation); use lowest effective statin dose."
    },
    {
        "herb": "Valerian",
        "drug": "Benzodiazepines",
        "severity": "CONTRAINDICATED",
        "mechanism": "Additive GABAergic CNS depression -> excessive sedation risk.",
        "action": "AVOID COMBINATION: Taper benzodiazepine first, then initiate Valerian after 2-week washout."
    },
    {
        "herb": "Ashwagandha",
        "drug": "Levothyroxine",
        "severity": "MODERATE_MONITOR",
        "mechanism": "Ashwagandha enhances deiodinase activity -> increased T4-to-T3 conversion.",
        "action": "MONITOR: Recheck TSH + Free T3 every 4 weeks; patient may require Levothyroxine dose reduction."
    },
    {
        "herb": "Guggul",
        "drug": "Warfarin",
        "severity": "HIGH_CAUTION",
        "mechanism": "CYP modulation and antiplatelet additive effect alters INR.",
        "action": "AVOID unless monitored weekly: inform anticoagulation clinic; check INR at 2 and 4 weeks."
    },
    {
        "herb": "Silymarin",
        "drug": "Cyclosporine",
        "severity": "CONTRAINDICATED",
        "mechanism": "CYP3A4 inhibition -> elevated immunosuppressant levels -> nephrotoxicity.",
        "action": "AVOID in transplant patients: absolutely contraindicated without specialist transplant nephrologist review."
    },
    {
        "herb": "NAC",
        "drug": "Nitroglycerin",
        "severity": "CONTRAINDICATED",
        "mechanism": "NAC potentiates vasodilatory effect of nitrates -> severe hypotension risk.",
        "action": "AVOID: Contraindicated combination. Screen for nitrate use in all cardiac patients."
    }
]


def evaluate_cp_afum_clinical_safety(
    patient_data: dict[str, Any],
    ingredients: list[Any],
    current_medications: list[str]
) -> dict[str, Any]:
    """
    Comprehensive CP-AFUM Safety Screen:
    1. Checks all Table 6.1 Red Flag referral criteria
    2. Checks Chapter 19 Forbidden List violations
    3. Checks Table 5.1 / Table R.2 Herb-Drug interaction rules
    """
    red_flag_triggers = []
    for rf in CP_AFUM_RED_FLAGS:
        try:
            if rf["check_fn"](patient_data):
                red_flag_triggers.append({
                    "red_flag": rf["name"],
                    "threshold": rf["threshold"],
                    "referral": rf["referral"],
                    "zayvora_role": rf["zayvora_role"]
                })
        except Exception:
            pass

    ing_names = []
    for it in ingredients:
        if isinstance(it, str):
            ing_names.append(it)
        elif isinstance(it, dict):
            ing_names.append(it.get("name") or "")

    forbidden_found = []
    for ing in ing_names:
        for f in FORBIDDEN_FORMULATION_LIST:
            if f.lower() in ing.lower():
                forbidden_found.append(f"FORBIDDEN INGREDIENT DETECTED: '{ing}' contains excluded agent '{f}'.")

    # Check AFUF Herb-Drug rules
    herb_drug_alerts = []
    meds_str = " ".join(current_medications).lower()
    for rule in AFUF_HERB_DRUG_RULES:
        herb_hit = any(rule["herb"].lower() in ing.lower() for ing in ing_names)
        drug_hit = rule["drug"].lower() in meds_str
        if herb_hit and drug_hit:
            herb_drug_alerts.append(rule)

    is_safe = (len(red_flag_triggers) == 0 and len(forbidden_found) == 0 and 
               all(a["severity"] != "CONTRAINDICATED" for a in herb_drug_alerts))

    return {
        "is_safe": is_safe,
        "red_flag_referrals": red_flag_triggers,
        "forbidden_ingredients": forbidden_found,
        "herb_drug_interactions": herb_drug_alerts,
        "requires_specialist_referral": len(red_flag_triggers) > 0,
        "verdict": "SAFE" if is_safe else "REFER_OR_MODIFY"
    }
