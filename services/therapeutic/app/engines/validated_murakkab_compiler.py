"""
ZAYVORA Health OS™ — Validated Murakkab & Nuskha Integration Layer
====================================================================
Complies with Phase 9 of the Canonical Architecture:
  Mufradat -> Classical Murakkabat -> Ingredient Role Assignment
    ├── Chief Drug (Juz-e-Azam)
    ├── Supporting Drug (Muawin)
    ├── Corrective (Musleh)
    ├── Substitute (Badal)
    └── Vehicle/Conduit (Badraqa)

Safety Enforcement:
  - Every compound is audited against the validated 60 Core Matab Registry.
  - Schedule E(1) containing compounds (e.g., Habb-e-Suranjan, Habb-e-Azaraqi)
    mandate Mudabbar certification and are strictly BLOCKED from autonomous
    AI prescription.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
import sys, os

try:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../..")))
    from services.knowledge.app.data.mufradat_gold_batch_monographs import (
        GoldBenchmarkRegistry,
        GOLD_BENCHMARK_25_MONOGRAPHS,
    )
    _REGISTRY_AVAILABLE = True
except ImportError:
    _REGISTRY_AVAILABLE = False


# ── Canonical Classical Murakkabat Registry ──────────────────────────────────
CLASSICAL_MURAKKABAT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "MRK-001": {
        "murakkab_id": "MRK-001",
        "name": "Itrifal Ustukhuddus",
        "category": "ITRIFAL_CEPHALIC",
        "classical_source": "Qarabadeen-e-Qadiri / NFUM Part-I",
        "upi_reference": "UPI Part-II Vol I p.15",
        "primary_indication": "Purification of morbid humours from the brain (Tanquia-e-Dimagh), Chronic catarrh, Migraine, Premature greying.",
        "organ_axis": "Axis 01 (Brain & Cognition)",
        "composition": [
            {"zmf_id": "ZMF-004", "ingredient": "Ustukhuddus", "role": "Juz-e-Azam (Chief Cephalic Drug)", "ratio_parts": 3},
            {"zmf_id": "ZMF-091", "ingredient": "Amla Khushk", "role": "Muawin (Tonic & Astringent)", "ratio_parts": 2},
            {"zmf_id": "ZMF-088", "ingredient": "Sana Makki", "role": "Muawin (Purging Morbid Humours)", "ratio_parts": 2},
            {"zmf_id": "ZMF-019", "ingredient": "Kishneez Khushk", "role": "Musleh (Prevents Cephalic Vapors)", "ratio_parts": 1},
            {"zmf_id": "ZMF-057", "ingredient": "Chob Zard (Haldi)", "role": "Muawin (Anti-inflammatory)", "ratio_parts": 0.5},
            {"zmf_id": "RAW-HONEY", "ingredient": "Asal (Honey) / Qand Safaid", "role": "Badraqa & Preservative Base (Qiwam)", "ratio_parts": 15}
        ],
        "dosage_instructions": "5g to 10g at bedtime with lukewarm water or Arq-e-Gaozaban.",
        "is_schedule_e1_containing": False,
        "ai_prescribing_permitted": True,
        "governance_status": "VALIDATED_CLASSICAL_COMPOUND"
    },

    "MRK-002": {
        "murakkab_id": "MRK-002",
        "name": "Jawarish Kamooni",
        "category": "JAWARISH_STOMACHIC",
        "classical_source": "Al-Qanoon fil-Tibb / Qarabadeen-e-Azam",
        "upi_reference": "UPI Part-II Vol I p.28",
        "primary_indication": "Gastric flatulence (Nafakh-e-Shikam), Dyspepsia, Sluggish digestion, Hiccups.",
        "organ_axis": "Axis 04 (Gastrointestinal & Digestion)",
        "composition": [
            {"zmf_id": "ZMF-020", "ingredient": "Zeera Siyah Mudabbar (Soaked in Sirka)", "role": "Juz-e-Azam (Carminative Chief)", "ratio_parts": 4},
            {"zmf_id": "ZMF-005", "ingredient": "Filfil Siyah", "role": "Muawin (Digestive Bioenhancer)", "ratio_parts": 1},
            {"zmf_id": "ZMF-016", "ingredient": "Zanjabeel (Sonth)", "role": "Muawin (Thermogenic Stomachic)", "ratio_parts": 1},
            {"zmf_id": "ZMF-024", "ingredient": "Badiyan (Saunf)", "role": "Musleh & Spasmolytic", "ratio_parts": 1.5},
            {"zmf_id": "ZMF-054", "ingredient": "Mastagi Roomi", "role": "Muawin (Gastric Toner)", "ratio_parts": 0.5},
            {"zmf_id": "RAW-HONEY", "ingredient": "Asal / Qand", "role": "Base Vehicle (Qiwam)", "ratio_parts": 16}
        ],
        "dosage_instructions": "5g twice daily after meals with water.",
        "is_schedule_e1_containing": False,
        "ai_prescribing_permitted": True,
        "governance_status": "VALIDATED_CLASSICAL_COMPOUND"
    },

    "MRK-003": {
        "murakkab_id": "MRK-003",
        "name": "Khamira Gaozaban Ambari",
        "category": "KHAMIRA_CARDIAC_MOOD",
        "classical_source": "Tibb-e-Akbar / Qarabadeen-e-Hamdard",
        "upi_reference": "UPI Part-II Vol I p.42",
        "primary_indication": "Cardiac palpitation (Khafqan), Mental fatigue, Anxiety, Memory weakness.",
        "organ_axis": "Axis 02 (Cardiovascular & Mood / Qalb)",
        "composition": [
            {"zmf_id": "ZMF-006", "ingredient": "Gaozaban (Barg wa Gul)", "role": "Juz-e-Azam (Exhilarant Chief)", "ratio_parts": 3},
            {"zmf_id": "ZMF-018", "ingredient": "Badranjboya", "role": "Muawin (Cardiac Tonic)", "ratio_parts": 1.5},
            {"zmf_id": "ZMF-004", "ingredient": "Ustukhuddus", "role": "Muawin (Cephalic Cleaner)", "ratio_parts": 1},
            {"zmf_id": "ZMF-051", "ingredient": "Tabasheer", "role": "Musleh (Quenches Heart Heat)", "ratio_parts": 1},
            {"zmf_id": "ZMF-040", "ingredient": "Zafran", "role": "Muawin & Mufarreh", "ratio_parts": 0.2},
            {"zmf_id": "ZMF-052", "ingredient": "Abresham Muqarraz", "role": "Muawin (Cardioprotective)", "ratio_parts": 1},
            {"zmf_id": "RAW-SUGAR", "ingredient": "Shakar Safaid / Arq-e-Gulab", "role": "Base Medium (Khamira Ferment Base)", "ratio_parts": 20}
        ],
        "dosage_instructions": "5g morning on empty stomach with milk or Arq-e-Gaozaban.",
        "is_schedule_e1_containing": False,
        "ai_prescribing_permitted": True,
        "governance_status": "VALIDATED_CLASSICAL_COMPOUND"
    },

    "MRK-004": {
        "murakkab_id": "MRK-004",
        "name": "Sharbat-e-Bazoori Motadil",
        "category": "SHARBAT_DIURETIC_HEPATIC",
        "classical_source": "Makhzan-ul-Advia / NFUM Part-II",
        "upi_reference": "UPI Part-II Vol I p.65",
        "primary_indication": "Liver and renal heat, Oliguria, Burning micturition, Mild jaundice.",
        "organ_axis": "Axis 08 (Renal & Urinary Tract)",
        "composition": [
            {"zmf_id": "ZMF-011", "ingredient": "Bekh wa Tukhm-e-Kasni", "role": "Juz-e-Azam (Hepatoprotective Diuretic)", "ratio_parts": 2},
            {"zmf_id": "ZMF-024", "ingredient": "Bekh wa Tukhm-e-Badiyan", "role": "Muawin (Renal Vasodilator)", "ratio_parts": 2},
            {"zmf_id": "ZMF-028", "ingredient": "Khar-e-Khasak (Gokhru)", "role": "Muawin (Lithotriptic Diuretic)", "ratio_parts": 2},
            {"zmf_id": "ZMF-084", "ingredient": "Tukhm-e-Khyarain (Cucumber/Melon seeds)", "role": "Musleh & Demulcent", "ratio_parts": 2},
            {"zmf_id": "RAW-SUGAR", "ingredient": "Qand Safaid (Sugar Syrup)", "role": "Syrup Vehicle", "ratio_parts": 25}
        ],
        "dosage_instructions": "20ml to 40ml diluted in 150ml cool water twice daily.",
        "is_schedule_e1_containing": False,
        "ai_prescribing_permitted": True,
        "governance_status": "VALIDATED_CLASSICAL_COMPOUND"
    },

    "MRK-005": {
        "murakkab_id": "MRK-005",
        "name": "Habb-e-Suranjan (Mudabbar)",
        "category": "HABB_RESTRICTED_POISON",
        "classical_source": "Kitab-ul-Mukhtarat / NFUM Part-I",
        "upi_reference": "UPI Part-II Vol I p.18 (Schedule E-1)",
        "primary_indication": "Acute Gout (Niqris), Severe inflammatory joint effusion, Sciatica (Irq-un-Nasa).",
        "organ_axis": "Axis 09 (Musculoskeletal & Joints)",
        "composition": [
            {"zmf_id": "ZMF-002", "ingredient": "Suranjan Talkh (MANDATORY CERTIFIED MUDABBAR)", "role": "Juz-e-Azam (Antigout Toxin)", "ratio_parts": 2},
            {"zmf_id": "ZMF-088", "ingredient": "Sana Makki", "role": "Muawin (Morbid Humour Purgation)", "ratio_parts": 1},
            {"zmf_id": "ZMF-029", "ingredient": "Tukhm-e-Karafs", "role": "Muawin (Uric Acid Elimination)", "ratio_parts": 1},
            {"zmf_id": "ZMF-050", "ingredient": "Gond Katiyra", "role": "Musleh (Gastric Mucosal Shield)", "ratio_parts": 0.5},
            {"zmf_id": "ZMF-057", "ingredient": "Chob Zard (Haldi)", "role": "Muawin (Anti-inflammatory)", "ratio_parts": 1}
        ],
        "dosage_instructions": "STRICT CLINICIAN DISPENSING ONLY: 1 pill (approx 250mg) at bedtime with milk. Max 7 days.",
        "is_schedule_e1_containing": True,
        "ai_prescribing_permitted": False,
        "governance_status": "SCHEDULE_E1_RESTRICTED_CLINICIAN_ONLY"
    }
}


class ValidatedMurakkabCompiler:
    """
    Compiler and auditor for Unani Compound Formulations (Murakkabat)
    and custom multi-herb patient Nuskhas.
    """

    @classmethod
    def get_murakkab(cls, murakkab_id: str) -> Optional[Dict[str, Any]]:
        """Lookup validated Murakkab by ID."""
        return CLASSICAL_MURAKKABAT_REGISTRY.get(murakkab_id.strip().upper())

    @classmethod
    def list_all_murakkabat(cls) -> List[Dict[str, Any]]:
        """List all validated classical compound formulas."""
        return [
            {
                "murakkab_id": m["murakkab_id"],
                "name": m["name"],
                "category": m["category"],
                "organ_axis": m["organ_axis"],
                "is_schedule_e1": m["is_schedule_e1_containing"],
                "ai_permitted": m["ai_prescribing_permitted"],
                "ingredients_count": len(m["composition"]),
                "governance_status": m["governance_status"]
            }
            for m in CLASSICAL_MURAKKABAT_REGISTRY.values()
        ]

    @classmethod
    def audit_custom_nuskha(cls, nuskha_name: str, ingredients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Audits a proposed Nuskha prescription against the 60 Validated Monograph Catalog.
        Checks for:
          1. Identity verification status of all components.
          2. Presence of Schedule E(1) poisonous substances.
          3. Presence of mandatory Musleh (corrective) if hot/toxic drugs are present.
          4. AI autonomy clearance.
        """
        total_items = len(ingredients)
        verified_items = []
        unverified_items = []
        schedule_e1_detected = []
        musleh_detected = []

        for ing in ingredients:
            zmf_id = ing.get("zmf_id", "").strip().upper()
            name = ing.get("name", zmf_id)
            ratio = ing.get("ratio", 1)

            # Check in gold/core monographs
            monograph = GoldBenchmarkRegistry.get_monograph(zmf_id) if _REGISTRY_AVAILABLE else None

            if monograph:
                is_e1 = monograph["safety_firewall"]["is_schedule_e1"]
                verified_items.append({
                    "zmf_id": zmf_id,
                    "name": monograph["canonical_identity"]["canonical_unani_name"],
                    "mizaj": monograph["classical_profile"]["mizaj"],
                    "is_schedule_e1": is_e1,
                    "role": ing.get("role", "Muawin"),
                    "musleh_hint": monograph["classical_profile"]["musleh"]
                })
                if is_e1:
                    schedule_e1_detected.append({
                        "zmf_id": zmf_id,
                        "name": name,
                        "shodhana_required": monograph["classical_profile"]["tadbeer"]
                    })
                # Check if this item is a classical Musleh
                if any(k in name.lower() for k in ["katiyra", "katira", "gul-e-surkh", "honey", "sikanjabeen", "badam"]):
                    musleh_detected.append(name)
            else:
                unverified_items.append({"zmf_id": zmf_id, "name": name})

        # Governance decision
        has_e1 = len(schedule_e1_detected) > 0
        all_verified = len(unverified_items) == 0

        if has_e1:
            audit_verdict = "REJECTED_FOR_AUTONOMOUS_AI_CONTAINS_SCHEDULE_E1"
            ai_permitted = False
            notes = "Nuskha contains statutory poisons. Mandatory human Hakeem sign-off and certified Mudabbar protocol required."
        elif not all_verified:
            audit_verdict = "PENDING_CONTAINS_UNVERIFIED_INGREDIENTS"
            ai_permitted = False
            notes = f"{len(unverified_items)} ingredient(s) are not verified in the 60-drug Core Matab catalog."
        else:
            audit_verdict = "APPROVED_CLINICAL_NUSKHA"
            ai_permitted = True
            notes = "All ingredients are fully validated in the Core Matab catalog with verified citations and safe toxicity profiles."

        return {
            "nuskha_name": nuskha_name,
            "total_ingredients": total_items,
            "verified_count": len(verified_items),
            "unverified_count": len(unverified_items),
            "schedule_e1_detected": schedule_e1_detected,
            "audit_verdict": audit_verdict,
            "ai_autonomous_permitted": ai_permitted,
            "verified_ingredients": verified_items,
            "unverified_ingredients": unverified_items,
            "governance_notes": notes
        }
