"""
ZAYVORA Knowledge Base — Structured Clinical Knowledge Engine Tests.

Tests for:
  1. Mufradat list (all items returned)
  2. Mufradat poison filter — only E(1) poisons
  3. Mufradat non-poison filter
  4. Mufradat search by Latin name
  5. Mufradat search by English name
  6. Mufradat get by ID — valid
  7. Mufradat get by ID — not found returns None
  8. Murakkabat list
  9. Murakkabat search by dosage form
  10. Murakkabat get by ID — valid
  11. Formulation integrity gate — valid (E1 with mudabbar declared)
  12. Formulation integrity gate — BLOCKED (E1 without mudabbar)
  13. Formulation integrity gate — duplicate ingredient error
  14. Formulation integrity gate — unknown botanical identity
  15. Safety firewall — ALLOWED (safe patient, safe dose)
  16. Safety firewall — BLOCKED (E1 without mudabbar cert)
  17. Safety firewall — BLOCKED (dose ceiling exceeded)
  18. Safety firewall — BLOCKED (pregnant + absolute contraindication)
  19. Safety firewall — BLOCKED (pediatric < 12 + absolute contraindication)
  20. Safety firewall — BLOCKED (severe renal impairment + E1 poison)
  21. Safety firewall — BLOCKED (herb-drug interaction FATAL)
  22. Safety firewall — WARNING only (herb-drug interaction MODERATE)
  23. Mizaj assessment — Damawi (ruddy, hot-moist, fast-broad)
  24. Mizaj assessment — Balghami (pale, cold-moist, slow-broad)
  25. Diseases list — all returned
  26. Diseases get by ID — valid
  27. Engine singleton reuse

"""
from __future__ import annotations

import sys
import os

# Insert service root into sys.path so imports resolve
_SERVICE_ROOT = os.path.join(os.path.dirname(__file__), "..", "app")
if _SERVICE_ROOT not in sys.path:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.structured_knowledge import (
    StructuredKnowledgeEngine,
    get_structured_knowledge,
    CANONICAL_MUFRADAT_DATA,
    CANONICAL_MURAKKABAT_DATA,
    CANONICAL_DISEASES_DATA,
    CANONICAL_HERB_DRUG_INTERACTIONS,
)

PASS = "PASS"
FAIL = "FAIL"
_results: list[tuple[str, str]] = []


def _assert(condition: bool, msg: str):
    if not condition:
        raise AssertionError(msg)


def _run(name: str, fn):
    try:
        fn()
        _results.append((PASS, name))
    except Exception as exc:
        _results.append((FAIL, f"{name}: {exc}"))


def _engine() -> StructuredKnowledgeEngine:
    return StructuredKnowledgeEngine()


# ---------------------------------------------------------------------------
# MUFRADAT TESTS
# ---------------------------------------------------------------------------

def test_mufradat_list_all():
    e = _engine()
    items = e.get_all_mufradat()
    _assert(len(items) == len(CANONICAL_MUFRADAT_DATA), f"Expected {len(CANONICAL_MUFRADAT_DATA)} mufradat, got {len(items)}")


def test_mufradat_filter_poison_true():
    e = _engine()
    items = e.get_all_mufradat(is_poison=True)
    _assert(all(m["is_schedule_e1_poison"] is True for m in items), "Non-poison item leaked into is_poison=True filter")
    _assert(len(items) >= 2, f"Expected ≥2 E(1) poisons, got {len(items)}")


def test_mufradat_filter_poison_false():
    e = _engine()
    items = e.get_all_mufradat(is_poison=False)
    _assert(all(m["is_schedule_e1_poison"] is False for m in items), "Poison item leaked into is_poison=False filter")
    _assert(len(items) >= 2, f"Expected ≥2 non-poison items, got {len(items)}")


def test_mufradat_search_latin():
    e = _engine()
    results = e.get_all_mufradat(search="withania")
    _assert(len(results) == 1, f"Expected 1 match for 'withania', got {len(results)}")
    _assert(results[0]["id"] == "muf-asgandh", f"Wrong match: {results[0]['id']}")


def test_mufradat_search_english():
    e = _engine()
    results = e.get_all_mufradat(search="crocus")
    _assert(len(results) == 1, f"Expected 1 match for 'crocus', got {len(results)}")
    _assert(results[0]["id"] == "muf-zafran", f"Wrong match: {results[0]['id']}")


def test_mufradat_get_by_id_valid():
    e = _engine()
    herb = e.get_mufrad_by_id("muf-kuchla")
    _assert(herb is not None, "muf-kuchla returned None, expected dict")
    _assert(herb["is_schedule_e1_poison"] is True, "Kuchla must be E(1) poison")
    _assert(herb["mandatory_mudabbar"] is True, "Kuchla requires mandatory Mudabbar")


def test_mufradat_get_by_id_not_found():
    e = _engine()
    herb = e.get_mufrad_by_id("muf-does-not-exist")
    _assert(herb is None, "Expected None for unknown mufrad_id")


# ---------------------------------------------------------------------------
# MURAKKABAT TESTS
# ---------------------------------------------------------------------------

def test_murakkabat_list_all():
    e = _engine()
    items = e.get_all_murakkabat()
    _assert(len(items) == len(CANONICAL_MURAKKABAT_DATA), f"Expected {len(CANONICAL_MURAKKABAT_DATA)} murakkabat, got {len(items)}")


def test_murakkabat_search_dosage_form():
    e = _engine()
    results = e.get_all_murakkabat(search="majun")
    _assert(len(results) == 1, f"Expected 1 match for 'majun', got {len(results)}")
    _assert(results[0]["id"] == "mur-majun-suranjan", f"Wrong match: {results[0]['id']}")


def test_murakkabat_get_by_id_valid():
    e = _engine()
    formula = e.get_murakkab_by_id("mur-khamira-gawzaban")
    _assert(formula is not None, "mur-khamira-gawzaban returned None")
    _assert(formula["nfum_code"] == "NFUM-I-002", "Wrong NFUM code")
    _assert(len(formula["ingredients"]) == 2, f"Expected 2 ingredients, got {len(formula['ingredients'])}")


# ---------------------------------------------------------------------------
# FORMULATION INTEGRITY GATE
# ---------------------------------------------------------------------------

def test_formulation_gate_valid():
    """Valid formulation: E1 ingredient WITH mudabbar declared."""
    e = _engine()
    payload = {
        "name": "Test Majun",
        "ingredients": [
            {"mufradat_id": "muf-suranjan-talkh", "ratio": 0.15, "is_chief": True, "requires_mudabbar": True},
            {"mufradat_id": "muf-filfil-siyah", "ratio": 0.10, "is_chief": False, "requires_mudabbar": False},
        ],
    }
    result = e.validate_formulation_integrity(payload)
    _assert(result["is_valid"] is True, f"Expected valid, got errors: {result['errors']}")
    _assert(result["has_schedule_e1"] is True, "E1 flag should be True since Suranjan Talkh is present")


def test_formulation_gate_e1_without_mudabbar():
    """Formulation integrity gate must BLOCK E1 poison without mudabbar declaration."""
    e = _engine()
    payload = {
        "name": "Unsafe Majun",
        "ingredients": [
            {"mufradat_id": "muf-suranjan-talkh", "ratio": 0.15, "is_chief": True, "requires_mudabbar": False},
        ],
    }
    result = e.validate_formulation_integrity(payload)
    _assert(result["is_valid"] is False, "Should be INVALID — E1 poison without mudabbar flag")
    _assert(any("SCHEDULE E(1)" in err for err in result["errors"]), f"Expected E1 safety gate error, got: {result['errors']}")


def test_formulation_gate_duplicate_ingredient():
    """Duplicate ingredient in recipe must produce an error."""
    e = _engine()
    payload = {
        "name": "Bad Formulation",
        "ingredients": [
            {"mufradat_id": "muf-asgandh", "ratio": 0.20, "is_chief": True, "requires_mudabbar": False},
            {"mufradat_id": "muf-asgandh", "ratio": 0.10, "is_chief": False, "requires_mudabbar": False},
        ],
    }
    result = e.validate_formulation_integrity(payload)
    _assert(result["is_valid"] is False, "Should be INVALID — duplicate ingredient")
    _assert(any("Duplicate" in err for err in result["errors"]), f"Expected duplicate error, got: {result['errors']}")


def test_formulation_gate_unknown_botanical():
    """Unknown mufradat_id must produce a botanical identity error."""
    e = _engine()
    payload = {
        "name": "Ghost Formulation",
        "ingredients": [
            {"mufradat_id": "muf-nonexistent-herb", "ratio": 0.30, "is_chief": True, "requires_mudabbar": False},
        ],
    }
    result = e.validate_formulation_integrity(payload)
    _assert(result["is_valid"] is False, "Should be INVALID — unknown botanical identity")
    _assert(any("not found" in err for err in result["errors"]), f"Expected botanical identity error, got: {result['errors']}")


# ---------------------------------------------------------------------------
# CLINICAL SAFETY FIREWALL
# ---------------------------------------------------------------------------

def _safe_patient():
    return {"age": 35, "is_pregnant": False, "is_lactating": False, "egfr": 90.0, "alt": 25.0, "modern_drugs": []}


def test_safety_allowed():
    """Safe patient, safe dose → ALLOWED."""
    e = _engine()
    result = e.evaluate_prescription_safety(
        patient_context=_safe_patient(),
        prescribed_items=[{"mufradat_id": "muf-asgandh", "single_dose_grams": 3.0, "mudabbar_certified": False}],
    )
    _assert(result["verdict"] == "ALLOWED", f"Expected ALLOWED, got {result['verdict']}")
    _assert(result["is_safe"] is True, "Should be safe")
    _assert(len(result["violations"]) == 0, f"Expected no violations, got {result['violations']}")


def test_safety_blocked_e1_uncertified():
    """E1 poison without mudabbar certification must be BLOCKED."""
    e = _engine()
    result = e.evaluate_prescription_safety(
        patient_context=_safe_patient(),
        prescribed_items=[{"mufradat_id": "muf-suranjan-talkh", "single_dose_grams": 0.25, "mudabbar_certified": False}],
    )
    _assert(result["verdict"] == "BLOCKED", f"Expected BLOCKED, got {result['verdict']}")
    rules = [v["rule"] for v in result["violations"]]
    _assert("SCHEDULE_E1_POISON_UNCERTIFIED" in rules, f"Expected E1 rule, got rules: {rules}")


def test_safety_blocked_dose_ceiling():
    """Dose exceeding approved ceiling must be BLOCKED."""
    e = _engine()
    result = e.evaluate_prescription_safety(
        patient_context=_safe_patient(),
        # Asgandh max single dose = 6g; prescribing 10g
        prescribed_items=[{"mufradat_id": "muf-asgandh", "single_dose_grams": 10.0, "mudabbar_certified": False}],
    )
    _assert(result["verdict"] == "BLOCKED", f"Expected BLOCKED, got {result['verdict']}")
    rules = [v["rule"] for v in result["violations"]]
    _assert("DOSE_CEILING_EXCEEDED" in rules, f"Expected DOSE_CEILING_EXCEEDED, got {rules}")


def test_safety_blocked_pregnancy():
    """Prescribing Suranjan Talkh to a pregnant patient must be BLOCKED."""
    e = _engine()
    patient = {**_safe_patient(), "is_pregnant": True}
    result = e.evaluate_prescription_safety(
        patient_context=patient,
        prescribed_items=[{"mufradat_id": "muf-suranjan-talkh", "single_dose_grams": 0.20, "mudabbar_certified": True}],
    )
    _assert(result["verdict"] == "BLOCKED", f"Expected BLOCKED for pregnancy, got {result['verdict']}")
    rules = [v["rule"] for v in result["violations"]]
    _assert("PREGNANCY_CONTRAINDICATION" in rules, f"Expected pregnancy rule, got {rules}")


def test_safety_blocked_pediatric():
    """Prescribing Kuchla to a child < 12 must be BLOCKED."""
    e = _engine()
    patient = {**_safe_patient(), "age": 8}
    result = e.evaluate_prescription_safety(
        patient_context=patient,
        prescribed_items=[{"mufradat_id": "muf-kuchla", "single_dose_grams": 0.06, "mudabbar_certified": True}],
    )
    _assert(result["verdict"] == "BLOCKED", f"Expected BLOCKED for pediatric, got {result['verdict']}")
    rules = [v["rule"] for v in result["violations"]]
    _assert("PEDIATRIC_CONTRAINDICATION" in rules, f"Expected pediatric rule, got {rules}")


def test_safety_blocked_renal_impairment():
    """E1 poison with eGFR < 30 must be BLOCKED regardless of mudabbar cert."""
    e = _engine()
    patient = {**_safe_patient(), "egfr": 18.0}
    result = e.evaluate_prescription_safety(
        patient_context=patient,
        prescribed_items=[{"mufradat_id": "muf-suranjan-talkh", "single_dose_grams": 0.20, "mudabbar_certified": True}],
    )
    _assert(result["verdict"] == "BLOCKED", f"Expected BLOCKED for renal impairment, got {result['verdict']}")
    rules = [v["rule"] for v in result["violations"]]
    _assert("SEVERE_RENAL_IMPAIRMENT" in rules, f"Expected renal rule, got {rules}")


def test_safety_blocked_herb_drug_fatal():
    """Suranjan Talkh + statin (CYP3A4) → FATAL → must BLOCK."""
    e = _engine()
    patient = {**_safe_patient(), "modern_drugs": ["statin"]}
    result = e.evaluate_prescription_safety(
        patient_context=patient,
        prescribed_items=[{"mufradat_id": "muf-suranjan-talkh", "single_dose_grams": 0.20, "mudabbar_certified": True}],
    )
    _assert(result["verdict"] == "BLOCKED", f"Expected BLOCKED for fatal herb-drug interaction, got {result['verdict']}")
    rules = [v["rule"] for v in result["violations"]]
    _assert("HERB_DRUG_INTERACTION" in rules, f"Expected HERB_DRUG_INTERACTION rule, got {rules}")


def test_safety_warning_herb_drug_moderate():
    """Filfil Siyah + digoxin → MODERATE → ALLOWED_WITH_WARNING, not blocked."""
    e = _engine()
    patient = {**_safe_patient(), "modern_drugs": ["digoxin"]}
    result = e.evaluate_prescription_safety(
        patient_context=patient,
        prescribed_items=[{"mufradat_id": "muf-filfil-siyah", "single_dose_grams": 0.5, "mudabbar_certified": False}],
    )
    _assert(result["verdict"] == "ALLOWED_WITH_WARNING", f"Expected ALLOWED_WITH_WARNING, got {result['verdict']}")
    _assert(result["is_safe"] is True, "Should still be safe (not blocked)")
    _assert(len(result["warnings"]) > 0, "Expected at least one warning")


# ---------------------------------------------------------------------------
# MIZAJ ASSESSMENT
# ---------------------------------------------------------------------------

def test_mizaj_damawi():
    """Ruddy complexion + hot&moist + fast&broad pulse → Damawi."""
    e = _engine()
    result = e.assess_patient_mizaj({
        "complexion": "ruddy red skin",
        "touch": "hot and moist",
        "pulse": "fast and broad",
    })
    _assert(result["dominant_mizaj"] == "Damawi", f"Expected Damawi, got {result['dominant_mizaj']}")
    _assert(0.40 <= result["confidence"] <= 0.95, f"Confidence out of range: {result['confidence']}")
    _assert(result["clinician_review_status"] == "PROVISIONAL_PENDING_CLINICIAN_PULSE_CHECK",
            "Clinician review status must be PROVISIONAL")


def test_mizaj_balghami():
    """Pale white + cold&moist + slow&broad pulse → Balghami."""
    e = _engine()
    result = e.assess_patient_mizaj({
        "complexion": "pale white chalky",
        "touch": "cold and moist",
        "pulse": "slow and broad",
    })
    _assert(result["dominant_mizaj"] == "Balghami", f"Expected Balghami, got {result['dominant_mizaj']}")


# ---------------------------------------------------------------------------
# DISEASE TESTS
# ---------------------------------------------------------------------------

def test_diseases_list():
    e = _engine()
    items = list(e.diseases.values())
    _assert(len(items) == len(CANONICAL_DISEASES_DATA), f"Expected {len(CANONICAL_DISEASES_DATA)} diseases, got {len(items)}")


def test_diseases_get_by_id():
    e = _engine()
    disease = e.diseases.get("dis-waja-al-mafasil")
    _assert(disease is not None, "dis-waja-al-mafasil not found")
    _assert(disease["icd11_code"] == "FA20", f"Wrong ICD-11 code: {disease['icd11_code']}")


# ---------------------------------------------------------------------------
# SINGLETON TEST
# ---------------------------------------------------------------------------

def test_engine_singleton():
    e1 = get_structured_knowledge()
    e2 = get_structured_knowledge()
    _assert(e1 is e2, "get_structured_knowledge() must return same singleton instance")


# ===========================================================================
# TEST RUNNER — compatible with run_all_tests.py loader
# ===========================================================================

TEST_FUNCTIONS = [
    test_mufradat_list_all,
    test_mufradat_filter_poison_true,
    test_mufradat_filter_poison_false,
    test_mufradat_search_latin,
    test_mufradat_search_english,
    test_mufradat_get_by_id_valid,
    test_mufradat_get_by_id_not_found,
    test_murakkabat_list_all,
    test_murakkabat_search_dosage_form,
    test_murakkabat_get_by_id_valid,
    test_formulation_gate_valid,
    test_formulation_gate_e1_without_mudabbar,
    test_formulation_gate_duplicate_ingredient,
    test_formulation_gate_unknown_botanical,
    test_safety_allowed,
    test_safety_blocked_e1_uncertified,
    test_safety_blocked_dose_ceiling,
    test_safety_blocked_pregnancy,
    test_safety_blocked_pediatric,
    test_safety_blocked_renal_impairment,
    test_safety_blocked_herb_drug_fatal,
    test_safety_warning_herb_drug_moderate,
    test_mizaj_damawi,
    test_mizaj_balghami,
    test_diseases_list,
    test_diseases_get_by_id,
    test_engine_singleton,
]


def run_tests():
    passed = 0
    failed = 0
    for fn in TEST_FUNCTIONS:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
            passed += 1
        except Exception as exc:
            print(f"  FAIL  {fn.__name__}: {exc}")
            failed += 1
    return passed, failed


if __name__ == "__main__":
    p, f = run_tests()
    print(f"\n{p} passed, {f} failed")
    sys.exit(0 if f == 0 else 1)
