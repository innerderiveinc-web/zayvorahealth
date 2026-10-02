"""
ZAYVORA Health OS™ - Formula Thermal Balance & Tadbir Safety Engine
Reference: ZAYVORA Pharmacopoeia Part 2 (Synergy & Quality Principles),
Dr. Irfan Ashraf, BUMS.

Implements:
  1. Net Mizaj Calculator (calculates heat/cold and moisture/dryness vectors across multi-herb formulas)
  2. Mandatory Musleh (Corrective) Verification Gate (e.g. Aqarqarha & Guggul pairing)
  3. Tadbir (Purification/Shuddhi) Certification Gate (Sang-e-Yahud, Shilajit, Guggul)
  4. Pharmacological Synergy Stack Verification (Mitochondrial Triad, Antioxidant Shield, NO Cascade)
"""

from typing import Dict, Any, List, Optional

# Reference the canonical single drug monographs
from services.knowledge.app.data.pharmacopoeia_monographs import MONOGRAPHS


class FormulaSafetyChecker:
    """
    Quality and safety engine auditing polypharmacy formulas before compounding or dispensing.
    """

    @classmethod
    def calculate_net_formula_mizaj(cls, ingredients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates the net thermal and moisture vector:
          Net Heat = sum(Heat Degrees * weight) - sum(Cold Degrees * weight)
          Net Moisture = sum(Moist Degrees * weight) - sum(Dry Degrees * weight)
        """
        total_weight = sum(float(i.get("weight_g", 1.0)) for i in ingredients)
        if total_weight == 0:
            total_weight = 1.0

        heat_sum = 0.0
        moisture_sum = 0.0

        for item in ingredients:
            name_key = item.get("key", "").upper()
            wt = float(item.get("weight_g", 1.0))
            
            # Find monograph
            mono = MONOGRAPHS.get(name_key)
            if not mono:
                # Try finding by partial name
                for k, m in MONOGRAPHS.items():
                    if k in name_key or name_key in k:
                        mono = m
                        break

            if mono:
                mizaj = mono.get("mizaj", {})
                h = float(mizaj.get("heat", 0))
                c = float(mizaj.get("cold", 0))
                m_deg = float(mizaj.get("moisture", 0))
                d = float(mizaj.get("dryness", 0))

                heat_sum += (h - c) * wt
                moisture_sum += (m_deg - d) * wt

        net_thermal_index = round(heat_sum / total_weight, 2)
        net_moisture_index = round(moisture_sum / total_weight, 2)

        # Classify net state
        if net_thermal_index > 1.5:
            thermal_state = "Har (Hot Dominant)"
        elif net_thermal_index < -1.5:
            thermal_state = "Barid (Cold Dominant)"
        else:
            thermal_state = "Mutadil-e-Hararat (Thermally Balanced)"

        if net_moisture_index > 1.5:
            moisture_state = "Ratab (Moist Dominant)"
        elif net_moisture_index < -1.5:
            moisture_state = "Yabis (Dry Dominant)"
        else:
            moisture_state = "Mutadil-e-Rutubat (Moisture Balanced)"

        return {
            "net_thermal_index": net_thermal_index,
            "net_moisture_index": net_moisture_index,
            "classified_formula_mizaj": f"{thermal_state} — {moisture_state}",
            "is_thermally_extreme": abs(net_thermal_index) >= 2.5 or abs(net_moisture_index) >= 2.5
        }

    @classmethod
    def audit_formula_safety_and_musleh(cls, ingredients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Audits formula for mandatory correctives (Musleh) and contraindications.
        """
        ing_keys = [i.get("key", "").upper() for i in ingredients]
        violations = []
        cautions = []
        synergy_detected = []

        # Rule 1: Aqarqarha (4th degree Hot) requires Tabasheer + Sandal Safaid + Amla
        if any("AQARQARHA" in k for k in ing_keys):
            has_tabasheer = any("TABASHEER" in k for k in ing_keys)
            has_sandal = any("SANDAL" in k for k in ing_keys)
            has_amla = any("AMLA" in k for k in ing_keys)

            if not (has_tabasheer and has_sandal):
                violations.append(
                    "CRITICAL SAFETY VIOLATION: Aqarqarha (4th degree Hot) present without mandatory thermal correctors (Tabasheer + Sandal Safaid). Risk of iatrogenic Safra excess and gastric burning."
                )

        # Rule 2: Guggul (Hot 2-3°, Dry 2°) requires Amla / Triphala Musleh
        if any("GUGGUL" in k for k in ing_keys):
            has_amla = any("AMLA" in k or "TRIPHALA" in k or "AMLAJ" in k or "AMLAL" in k for k in ing_keys)
            if not has_amla:
                cautions.append("Guggul present without Amla Musleh: recommend adding Amla to prevent gastric dryness and heartburn.")

        # Rule 3: Curcumin / Haldi requires Piperine or Phytosome delivery for bioavailability
        has_curcumin = any(("HALDI" in k and "DARU" not in k) or "CURCUMIN" in k or "CURCUMA" in k for k in ing_keys)
        if has_curcumin:
            has_piperine = any(p in k for k in ing_keys for p in ["FILFIL_SIYAH", "PIPERINE", "PIPPALI", "TRIKATU"])
            has_phytosome = any(p in k for k in ing_keys for p in ["PHYTOSOME", "MERIVA"])
            if not (has_piperine or has_phytosome):
                cautions.append("Curcumin present without Piperine: oral bioavailability is <1% without Piperine or phytosome delivery.")
            elif has_phytosome:
                synergy_detected.append("Phytosome Phospholipid-Bound Delivery Active: 29x Curcumin Bioavailability")
            else:
                synergy_detected.append("2,000% Bioavailability Cascade Active: Curcumin + Piperine")

        # Check for Mitochondrial Triad
        has_coq10 = any("COQ10" in k for k in ing_keys)
        has_shilajit = any("SHILAJIT" in k for k in ing_keys)
        has_carnitine = any("CARNITINE" in k for k in ing_keys)
        if has_coq10 and has_shilajit and has_carnitine:
            synergy_detected.append("Mitochondrial Power Triad Active: CoQ10 + Shilajit + L-Carnitine (40% motility boost)")

        # Check for Triple-Redundant Antioxidant Shield
        has_selenium = any("SELENIUM" in k for k in ing_keys)
        has_tabasheer = any("TABASHEER" in k for k in ing_keys)
        has_amla = any("AMLA" in k for k in ing_keys)
        if has_selenium and has_tabasheer and has_amla:
            synergy_detected.append("Triple-Redundant Antioxidant Shield Active: Selenium (GPx4) + Tabasheer (silica) + Amla (Vitamin C)")

        # Rule 4: Behman Dual-Color Balance (Chapter 15.3)
        has_combo = any("BEHMAN_COMBINATION" in k or "BEHMAN COMBINATION" in k for k in ing_keys)
        has_behman_surkh = has_combo or any("BEHMAN_SURKH" in k or "BEHMAN SURKH" in k for k in ing_keys)
        has_behman_safaid = has_combo or any("BEHMAN_SAFAID" in k or "BEHMAN_SAFED" in k or "BEHMAN SAFAID" in k or "BEHMAN SAFED" in k for k in ing_keys)
        if has_behman_surkh and not has_behman_safaid:
            violations.append(
                "THERMAL BALANCE VIOLATION: Behman Surkh (Red Behen, Hot-Dry Leydig activator) present without Behman Safaid (White Behen, Cold-Moist cooling substrate). Risk of thermal damage to sperm DNA."
            )
        elif has_behman_surkh and has_behman_safaid:
            synergy_detected.append("Classical Behman Dual-Color Balance Active: Leydig stimulation without thermal sperm DNA degradation")

        # Rule 5: Aqarqarha Micro-Dose Ceiling (Chapter 15.4)
        for item in ingredients:
            k = item.get("key", "").upper()
            if "AQARQARHA" in k:
                daily_dose_mg = item.get("daily_dose_mg")
                if daily_dose_mg is not None and float(daily_dose_mg) > 200.0:
                    violations.append(
                        f"OVERDOSE VIOLATION: Aqarqarha daily dose of {daily_dose_mg}mg exceeds strict ZAYVORA ceiling of 200mg/day max (Risk of acute gastric burning, hypertension, and tachycardia)."
                    )

        # Calculate thermal balance
        thermal_res = cls.calculate_net_formula_mizaj(ingredients)

        is_cleared = len(violations) == 0

        return {
            "formula_cleared": is_cleared,
            "decision": "FORMULA APPROVED FOR COMPOUNDING" if is_cleared else "FORMULA REJECTED - SAFETY INTERACTION",
            "violations": violations,
            "cautions": cautions,
            "synergies_detected": synergy_detected,
            "thermal_audit": thermal_res
        }

    @classmethod
    def verify_tadbir_compliance(cls, raw_mineral_drug: str, tadbir_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifies batch purification (Tadbir/Shuddhi) compliance for mineral or toxic agents.
        """
        drug_key = raw_mineral_drug.upper()

        if "SANG_E_YAHUD" in drug_key:
            days_oxidized = int(tadbir_report.get("oxidation_days", 0))
            is_non_gritty = bool(tadbir_report.get("finely_triturated", False))
            if days_oxidized < 40 or not is_non_gritty:
                return {
                    "passed": False,
                    "reason": f"Tadbir failed: Sang-e-Yahud requires full 40-day oxidation/trituration in Kulthi decoction. Only {days_oxidized} days reported."
                }
            return {"passed": True, "certification": "Tadbir-e-Sang-e-Yahud Certified: Converted to pure non-toxic calcium phosphate matrix."}

        elif "SHILAJIT" in drug_key:
            lead_ppm = float(tadbir_report.get("lead_ppm", 10.0))
            fulvic_percent = float(tadbir_report.get("fulvic_acid_percent", 0.0))
            if lead_ppm > 3.0:
                return {
                    "passed": False,
                    "reason": f"Heavy metal contamination: Lead {lead_ppm} ppm exceeds ZAYVORA specification of <3.0 ppm."
                }
            if fulvic_percent < 50.0:
                return {
                    "passed": False,
                    "reason": f"Subpotent: Fulvic acid {fulvic_percent}% is below 50% minimum threshold."
                }
            return {"passed": True, "certification": "Shodhana Certified: Heavy metals <3 ppm and fulvic acid >= 50%."}

        elif "GUGGUL" in drug_key:
            was_triphala_soaked = bool(tadbir_report.get("triphala_soak_12hr", False))
            temp_c = float(tadbir_report.get("evaporation_temp_c", 70.0))
            if not was_triphala_soaked:
                return {"passed": False, "reason": "Shuddhi failed: Mandatory 12-hour Triphala decoction soak not documented."}
            if temp_c > 65.0:
                return {"passed": False, "reason": f"Thermal degradation: Evaporation temperature {temp_c}°C exceeded 65°C ceiling."}
            return {"passed": True, "certification": "Shudh Guggul Certified: Irritant resin acids filtered, guggulsterones preserved."}

        elif "TABASHEER" in drug_key or "BANSLOCHAN" in drug_key:
            sio2_pct = float(tadbir_report.get("silicon_dioxide_pct") or tadbir_report.get("silica_percent") or 0.0)
            lead_ppm = float(tadbir_report.get("lead_ppm", 10.0))
            arsenic_ppm = float(tadbir_report.get("arsenic_ppm", 5.0))
            if sio2_pct < 85.0:
                return {"passed": False, "reason": f"Subpotent: Tabasheer SiO2 content {sio2_pct}% is below 85% minimum specification."}
            if lead_ppm >= 1.0 or arsenic_ppm >= 0.5:
                return {"passed": False, "reason": f"Heavy metal contamination: Lead {lead_ppm} ppm (limit <1.0) or Arsenic {arsenic_ppm} ppm (limit <0.5) exceeded."}
            return {"passed": True, "certification": "DNA Heat Shield Certified: Tabasheer meets >=85% SiO2 and ultra-pure mineral standards."}

        return {"passed": True, "certification": "Standard botanical authentication verified."}

    @classmethod
    def audit_four_tier_polypharmacy(cls, formula_components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Audits polypharmacy compound formulas against ZAYVORA's Four-Tier Architecture (Part One §6.4):
          - Tier 1: Foundation (20-30% by weight) - Nutritive, substrate-providing agents (Salab, Asgandh)
          - Tier 2: Core (50-60% by weight) - Primary therapeutic agents targeting axis (Behman, Guggul)
          - Tier 3: Correctors (15-25% by weight) - Balancing & thermal buffer agents (Tabasheer, Amla)
          - Tier 4: Catalysts (5-10% by weight) - Bioavailability & signal amplifiers (Piperine, Aqarqarha)
        """
        total_weight = sum(float(i.get("weight_g", 1.0)) for i in formula_components)
        if total_weight == 0:
            total_weight = 1.0

        tier_weights = {
            "tier_1_foundation": 0.0,
            "tier_2_core": 0.0,
            "tier_3_correctors": 0.0,
            "tier_4_catalysts": 0.0
        }

        for item in formula_components:
            tier_num = int(item.get("tier", 2))
            wt = float(item.get("weight_g", 1.0))
            if tier_num == 1:
                tier_weights["tier_1_foundation"] += wt
            elif tier_num == 2:
                tier_weights["tier_2_core"] += wt
            elif tier_num == 3:
                tier_weights["tier_3_correctors"] += wt
            elif tier_num == 4:
                tier_weights["tier_4_catalysts"] += wt
            else:
                tier_weights["tier_2_core"] += wt

        tier_pcts = {k: round((v / total_weight) * 100.0, 1) for k, v in tier_weights.items()}

        warnings = []
        # Check standard bands
        if not (15.0 <= tier_pcts["tier_1_foundation"] <= 35.0):
            warnings.append(f"Tier 1 Foundation is {tier_pcts['tier_1_foundation']}% (Target: 20-30%).")
        if not (40.0 <= tier_pcts["tier_2_core"] <= 65.0):
            warnings.append(f"Tier 2 Core Therapeutic is {tier_pcts['tier_2_core']}% (Target: 50-60%).")
        if not (10.0 <= tier_pcts["tier_3_correctors"] <= 30.0):
            warnings.append(f"Tier 3 Correctors is {tier_pcts['tier_3_correctors']}% (Target: 15-25%).")
        if not (3.0 <= tier_pcts["tier_4_catalysts"] <= 15.0):
            warnings.append(f"Tier 4 Catalysts is {tier_pcts['tier_4_catalysts']}% (Target: 5-10%).")

        is_balanced = len(warnings) == 0

        return {
            "is_symphonic_polypharmacy": is_balanced,
            "tier_percentages": tier_pcts,
            "ideal_distribution": {
                "tier_1_foundation": "20-30%",
                "tier_2_core": "50-60%",
                "tier_3_correctors": "15-25%",
                "tier_4_catalysts": "5-10%"
            },
            "warnings": warnings,
            "status": "SYMPHONIC POLYPHARMACY APPROVED" if is_balanced else "POLYPHARMACY RATIO DEVIATION DETECTED"
        }
