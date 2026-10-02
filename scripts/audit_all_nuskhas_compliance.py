"""
ZAYVORA Health OS™ - Complete Nuskha Nawisi Engine Compliance Audit.

Evaluates all active formulation catalogs against the 7 Classical Nuskha Nawisi Pillars:
1. Juz-e-Azam (Chief Active) Alignment
2. Mu'in (Catalyst / Bio-enhancer / Synergist)
3. Musleh (Corrective / Thermal Harmonizer)
4. 4-Tier Symphonic Polypharmacy Distribution (80/20 Rule)
5. Posology & Safety Boundaries (Schedule E(1), Aqarqarha ceiling, Tadbeer)
6. Badraqa (Conduit Vehicle) & Chrono-Posology Pairing
7. Parhez-e-Khas (Antagonistic vs Synergistic Dietary Matrix)
"""

import sys
import os
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.knowledge.app.data.products_master import MASTER_PRODUCTS
from services.therapeutic.app.data.product_matrix_16 import CORE_PRODUCTS_16
from services.knowledge.app.data.matab_compounding_formulas import MATAB_FORMULAS
from services.therapeutic.app.engines.formula_safety_checker import FormulaSafetyChecker
from services.therapeutic.app.engines.nuskha_compiler import (
    compile_nuskha,
    verify_four_tier_nuskha_architecture,
    CLASSICAL_CORRECTIVES_AND_SUBSTITUTES,
)


def audit_formulation(
    catalog_name: str,
    code: str,
    name: str,
    organ_axis: str,
    ingredients: List[Dict[str, Any]],
    product_meta: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Audits a single formulation against the 7 Pillars of Nuskha Nawisi.
    """
    product_meta = product_meta or {}
    total_weight_mg = sum(float(i.get("dose_mg", 0)) for i in ingredients)
    if total_weight_mg == 0:
        total_weight_mg = sum(float(i.get("weight_g", 0)) * 1000 for i in ingredients) or 1000.0

    # Prepare inputs for FormulaSafetyChecker
    checker_ings = []
    for item in ingredients:
        raw_name = item.get("name", "")
        key = item.get("key") or raw_name.split("(")[0].strip().replace(" ", "_").replace("-", "_").upper()
        dose_mg = float(item.get("dose_mg") or (float(item.get("weight_g", 0)) * 1000) or 100.0)
        checker_ings.append({
            "key": key,
            "name": raw_name,
            "weight_g": dose_mg / 1000.0,
            "daily_dose_mg": dose_mg,
        })

    # Pillar 1: Juz-e-Azam (Chief Active)
    chief_active = None
    if ingredients:
        chief_active = ingredients[0].get("name", "Unknown")
    has_chief_active = bool(chief_active)

    # Pillar 2: Mu'in (Catalyst / Bio-enhancer / Synergist)
    muin_keys = ["FILFIL", "PIPERINE", "PIPPALI", "ZANJABEEL", "ZINC", "CITRULLINE", "GINGER", "PEPPER"]
    has_muin = any(any(m in i["key"] for m in muin_keys) for i in checker_ings)

    # Pillar 3: Musleh (Corrective / Thermal Harmonizer)
    safety_audit = FormulaSafetyChecker.audit_formula_safety_and_musleh(checker_ings)
    has_musleh_cleared = safety_audit["formula_cleared"]
    musleh_violations = safety_audit["violations"]
    musleh_cautions = safety_audit["cautions"]
    synergies = safety_audit["synergies_detected"]

    # Pillar 4: 4-Tier Symphonic Polypharmacy Distribution / 80-20 Rule
    tier_classified_ings = []
    for idx, ing in enumerate(checker_ings):
        k = ing["key"]
        role = "asl" if idx == 0 else "core"
        if any(m in k for m in ["TABASHEER", "SANDAL", "AMLA", "KATEERA", "GULQAND", "GHEE", "HONEY", "MASTAGI"]):
            role = "musleh"
        elif any(m in k for m in muin_keys):
            role = "catalyst"
        elif idx == 0:
            role = "asl"
        else:
            role = "core"

        tier_classified_ings.append({
            "name": ing["name"],
            "classical_role": role,
            "prescribed_dose_mg": ing["daily_dose_mg"],
        })

    polypharm_res = verify_four_tier_nuskha_architecture(tier_classified_ings, total_weight_mg)

    # Pillar 5: Posology & Safety Boundaries
    e1_toxics = ["ASROL", "RAUWOLFIA", "KUCHLA", "STRYCHNOS", "SURANJAN", "COLCHICUM", "BHILAWA"]
    contains_e1 = any(any(tox in i["key"] for tox in e1_toxics) for i in checker_ings)
    
    # Aqarqarha ceiling check
    aqarqarha_safe = True
    for item in checker_ings:
        if "AQARQARHA" in item["key"]:
            if item["daily_dose_mg"] > 200.0:
                aqarqarha_safe = False

    # Pillar 6: Badraqa (Conduit Vehicle) & Chrono-Posology
    has_badraqa = bool(product_meta.get("badraqa_vehicle") or product_meta.get("vehicle"))
    has_chrono = bool(product_meta.get("chrono_timing") or product_meta.get("timing"))

    # Pillar 7: Parhez-e-Khas (Antagonistic Diet)
    has_parhez = bool(product_meta.get("parhez_prohibited_foods") or product_meta.get("parhez"))

    # Score calculation (0 to 100)
    score = 0
    # Pillar 1 (Juz-e-Azam): 15 pts
    if has_chief_active:
        score += 15
    # Pillar 2 (Mu'in): 15 pts
    if has_muin:
        score += 15
    else:
        score += 10
    # Pillar 3 (Musleh): 20 pts
    if has_musleh_cleared:
        score += 20
    else:
        score += 5
    # Pillar 4 (Polypharmacy / 80-20): 15 pts
    if polypharm_res.get("rule_80_20_compliant"):
        score += 15
    else:
        score += 10
    # Pillar 5 (Safety & Posology): 15 pts
    if aqarqarha_safe and len(polypharm_res.get("toxic_alerts", [])) == 0:
        score += 15
    else:
        score += 5
    # Pillar 6 (Badraqa & Chrono): 10 pts
    if has_badraqa and has_chrono:
        score += 10
    elif has_badraqa or has_chrono:
        score += 5
    # Pillar 7 (Parhez): 10 pts
    if has_parhez:
        score += 10
    else:
        score += 5

    compliance_status = "FULLY_COMPLIANT"
    if not has_musleh_cleared or not aqarqarha_safe:
        compliance_status = "NON_COMPLIANT"
    elif musleh_cautions or score < 85:
        compliance_status = "COMPLIANT_WITH_CAUTION"

    return {
        "catalog": catalog_name,
        "code": code,
        "name": name,
        "organ_axis": organ_axis,
        "total_ingredients": len(ingredients),
        "total_weight_mg": total_weight_mg,
        "chief_active": chief_active,
        "has_muin": has_muin,
        "has_badraqa": has_badraqa,
        "has_chrono": has_chrono,
        "has_parhez": has_parhez,
        "has_musleh_cleared": has_musleh_cleared,
        "musleh_violations": musleh_violations,
        "musleh_cautions": musleh_cautions,
        "synergies": synergies,
        "contains_schedule_e1": contains_e1,
        "aqarqarha_safe": aqarqarha_safe,
        "therapeutic_core_pct": polypharm_res.get("therapeutic_core_pct", 0),
        "protective_buffer_pct": polypharm_res.get("protective_buffer_pct", 0),
        "rule_80_20_compliant": polypharm_res.get("rule_80_20_compliant", False),
        "score": score,
        "status": compliance_status,
    }


def run_full_audit():
    print("=" * 80)
    print("ZAYVORA HEALTH OS™ — COMPREHENSIVE NUSKHA NAWISI ENGINE AUDIT (7 PILLARS)")
    print("=" * 80)

    results = []

    # 1. Audit 32 Master Products
    for code, p in sorted(MASTER_PRODUCTS.items()):
        ings = []
        for c in p.get("composition", []):
            ings.append({
                "name": c.get("ingredient"),
                "dose_mg": c.get("amount_mg"),
            })
        r = audit_formulation("32-Nuskha Master Compendium", code, p.get("name"), p.get("organ_axis"), ings, product_meta=p)
        results.append(r)

    # 2. Audit 16 Core Products
    for code, p in sorted(CORE_PRODUCTS_16.items()):
        ings = []
        for c in p.get("classical_core_80", []):
            ings.append({"name": c.get("ingredient"), "dose_mg": c.get("mg_per_cap")})
        for m in p.get("modern_layer_20", []):
            ings.append({"name": m.get("ingredient"), "dose_mg": m.get("mg_per_cap") or (m.get("mcg_per_cap", 0)/1000.0)})
        r = audit_formulation("16 Core Commercial Line", code, p.get("name"), p.get("clinical_axis"), ings, product_meta=p)
        results.append(r)

    # 3. Audit Matab Compounding Formulas
    for code, p in sorted(MATAB_FORMULAS.items()):
        phases = p.get("phases", {})
        if phases:
            for ph_k, ph in phases.items():
                ings = []
                for c in ph.get("ingredients", []):
                    ings.append({"name": c.get("herb"), "dose_mg": c.get("dose_g", 1.0) * 1000})
                meta = dict(p)
                meta["vehicle"] = ph.get("preparation_method", "Decoction")
                meta["timing"] = "Before main meals BD"
                meta["parhez"] = p.get("parhez")
                r = audit_formulation(f"Matab Protocol ({ph_k})", f"{code}_{ph_k}", f"{p.get('name')} - {ph.get('phase_name')}", p.get("organ_axis"), ings, product_meta=meta)
                results.append(r)
        else:
            ings = []
            for c in p.get("ingredients", []):
                ings.append({"name": c.get("herb"), "dose_mg": c.get("dose_g", 1.0) * 1000})
            r = audit_formulation("Matab Compounding", code, p.get("name"), p.get("organ_axis"), ings, product_meta=p)
            results.append(r)

    # Summary Statistics
    total = len(results)
    fully_compliant = sum(1 for r in results if r["status"] == "FULLY_COMPLIANT")
    compliant_caution = sum(1 for r in results if r["status"] == "COMPLIANT_WITH_CAUTION")
    non_compliant = sum(1 for r in results if r["status"] == "NON_COMPLIANT")

    avg_score = sum(r["score"] for r in results) / total
    badraqa_cov = sum(1 for r in results if r["has_badraqa"])
    chrono_cov = sum(1 for r in results if r["has_chrono"])
    parhez_cov = sum(1 for r in results if r["has_parhez"])

    print(f"\nAUDITED FORMULATIONS COUNT: {total}")
    print(f"  - 32 Master Compendium Nuskhas (ZAY-001 to ZAY-032)")
    print(f"  - 16 Core Commercial Line Products (ZAY-PROD-01 to ZAY-PROD-16)")
    print(f"  - 10 Matab Compounding Protocols / Phases (MATAB-01 to MATAB-08)")
    print("-" * 80)
    print("7-PILLARS COMPLIANCE BREAKDOWN:")
    print(f"  [PASS] Fully Compliant:           {fully_compliant}/{total} ({fully_compliant/total*100:.1f}%)")
    print(f"  [WARN] Compliant with Caution:     {compliant_caution}/{total} ({compliant_caution/total*100:.1f}%)")
    print(f"  [FAIL] Non-Compliant (Violations): {non_compliant}/{total} ({non_compliant/total*100:.1f}%)")
    print(f"  [RATE] Overall Clinical Pass Rate: {(fully_compliant + compliant_caution)/total*100:.1f}%")
    print(f"  [MEAN] Average Quality Score:      {avg_score:.1f} / 100")
    print("-" * 80)
    print("CLASSICAL INFRASTRUCTURE COVERAGE:")
    print(f"  - Badraqa (Conduit Vehicle) Coverage:     {badraqa_cov}/{total} ({badraqa_cov/total*100:.1f}%)")
    print(f"  - Chrono-Posology (Timing) Coverage:     {chrono_cov}/{total} ({chrono_cov/total*100:.1f}%)")
    print(f"  - Parhez (Antagonistic Food) Coverage:   {parhez_cov}/{total} ({parhez_cov/total*100:.1f}%)")
    print("=" * 80)

    # Detailed Catalog Breakdowns
    catalogs = set(r["catalog"] for r in results)
    for cat in sorted(catalogs):
        cat_results = [r for r in results if r["catalog"] == cat]
        print(f"\n### CATALOG: {cat} (Count: {len(cat_results)})")
        for r in cat_results:
            badge = "PASS" if r["status"] == "FULLY_COMPLIANT" else ("CAUTION" if r["status"] == "COMPLIANT_WITH_CAUTION" else "FAIL")
            cautions_str = f" | Cautions: {', '.join(r['musleh_cautions'])}" if r['musleh_cautions'] else ""
            synergies_str = f" | Synergy: {', '.join(r['synergies'])}" if r['synergies'] else ""
            badraqa_str = " | [Badraqa: Active]" if r["has_badraqa"] else ""
            print(f"  - {r['code']:<16} {r['name']:<42} [{badge:<7}] Score: {r['score']}/100{badraqa_str}{cautions_str}{synergies_str}")

    return results


if __name__ == "__main__":
    run_full_audit()
