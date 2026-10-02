"""
ZAYVORA Health OS™ v5.0 — Classical Munzij & Mushil (Nujz & Tanqiya) Protocol Engine
====================================================================================
References:
  - Ibn Sina: Al-Qanoon fit-Tibb (Principles of Evacuation & Concoction)
  - Al-Razi: Kitab al-Hawi (Treatment of Su-e-Mizaj Maddi)
  - National Formulary of Unani Medicine (NFUM Vol I-VI)

The Inviolable 3-Stage Classical Law for Su-e-Mizaj Maddi (Chronic Morbid Matter):
  "Never purge an unconcocted humor (Lā tushil al-khilt mā lam yandaj).
   First ripen with Munzij, second evacuate with Mushil, third restore with Muqawwi."

Stage 1: NUJZ (Concoction Phase):
  - Munzij-e-Safra: 3 to 5 days.
  - Munzij-e-Balgham: 7 to 10 days.
  - Munzij-e-Sawda: 14 to 21 days.
  Monitors Alamat-e-Nujz in Qaroorah (sediment settles, clarity changes) and Baraaz.

Stage 2: TANQIYA (Targeted Humoral Evacuation):
  - Mushil / Munaqqi formulated precisely for the ripened humor.

Stage 3: TABREED WA TAQWIYAT (Post-Evacuation Restoration):
  - Cooling, soothing, and restoring target and master organ tone.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


MUNZIJ_FORMULATIONS = {
    "Safra": {
        "formula_name": "Joshanda Munzij-e-Safra Standard",
        "standard_duration_days": 4,
        "ingredients": [
            {"herb": "Gaozaban", "role": "Mufarrih & Thermal Modulator", "dose_g": 5.0},
            {"herb": "Shahtarah", "role": "Musaffi-e-Dam & Safra corrector", "dose_g": 5.0},
            {"herb": "Unnab", "role": "Muskin-e-Hararat & Emollient", "dose_g": 5.0},
            {"herb": "Sapistan", "role": "Mulayyin & Demulcent", "dose_g": 5.0},
            {"herb": "Tukhm-e-Kasni", "role": "Mufattih Sudad-e-Kabid", "dose_g": 5.0}
        ],
        "signs_of_nujz": [
            "Urine color moderates from dark flaming yellow to light straw (Asfar Qashiy)",
            "Disappearance of burning micturition (Taskeen-e-Sozish)",
            "Sediment in Qaroorah becomes uniformly settled (Rasub-e-Mahmoof)",
            "Relief from bitter taste in mouth (Talkhi-e-Dahan) and thirst"
        ],
        "mushil_pairing": {
            "name": "Joshanda Mushil-e-Safra",
            "evacuant_actives": ["Maghz-e-Faloos Khiyarshambar (Cassia fistula) 20g", "Taranjabeen (Manna) 15g", "Sana-e-Makki 3g"],
            "timing": "Morning fasting (Nihaar Munh) on final day"
        },
        "post_evacuation_taqwiyaat": "Sharbat-e-Bazoori Motadil 25ml with Arq-e-Kasni BD for 7 days"
    },
    "Balgham": {
        "formula_name": "Joshanda Munzij-e-Balgham Standard",
        "standard_duration_days": 8,
        "ingredients": [
            {"herb": "Asl-us-Soos (Licorice)", "role": "Munajjiz & Muqatta-e-Balgham", "dose_g": 7.0},
            {"herb": "Badiyan (Fennel)", "role": "Kasir-e-Riyah & Munzij", "dose_g": 5.0},
            {"herb": "Bekh-e-Kasni", "role": "Deobstruent hepatic conduit", "dose_g": 5.0},
            {"herb": "Gul-e-Gaozaban", "role": "Muqawwi-e-Qalb wa Dimagh", "dose_g": 5.0},
            {"herb": "Zufa Khushk (Hyssop)", "role": "Muhallil & Balgham thinner", "dose_g": 3.0}
        ],
        "signs_of_nujz": [
            "Urine shifts from thin watery pale (Abyad Raqeeq) to thicker with distinct sediment",
            "Resolution of heavy morning lethargy and limb stiffness",
            "Clearing of thick white tongue coating (Lisan Abyad Ghaleez)",
            "Easy expectoration and digestive lightness"
        ],
        "mushil_pairing": {
            "name": "Itrifal / Decoction Mushil-e-Balgham",
            "evacuant_actives": ["Sana-e-Makki 5g", "Turbud Safaid Mudabbar 3g", "Roghan-e-Badam 10ml"],
            "timing": "Bedtime or early morning after confirmed Nujz"
        },
        "post_evacuation_taqwiyaat": "Jawarish Kamuni 5g post meals + Khamira Gaozaban Ambari 5g at bedtime"
    },
    "Sawda": {
        "formula_name": "Joshanda Munzij-e-Sawda Standard",
        "standard_duration_days": 15,
        "ingredients": [
            {"herb": "Aftimoon Wilayati (Cuscuta)", "role": "Specific Munzij & Mushil-e-Sawda", "dose_g": 5.0},
            {"herb": "Ustukhuddus (French Lavender)", "role": "Jarub-e-Dimagh (Broom of the brain)", "dose_g": 5.0},
            {"herb": "Badiyan (Fennel seed)", "role": "Carminative & Concoctive", "dose_g": 5.0},
            {"herb": "Gul-e-Surkh (Rose petals)", "role": "Mulayyin & Cardiotonic", "dose_g": 5.0},
            {"herb": "Shahtarah (Fumaria)", "role": "Blood purifier & alterative", "dose_g": 5.0}
        ],
        "signs_of_nujz": [
            "Urine darkness and leaden cloudiness clarifies with healthy bottom sediment",
            "Alleviation of somatic brooding, melancholy, and insomnia",
            "Softening of hard skin dryness (Yuboosat-e-Jild)",
            "Restoration of natural pulse amplitude and elasticity"
        ],
        "mushil_pairing": {
            "name": "Itrifal Ustukhuddus with Aftimoon Extract",
            "evacuant_actives": ["Ayarij Faiqra 3g", "Post-e-Halela Zard 5g", "Aftimoon 5g"],
            "timing": "Night time with warm lukewarm milk"
        },
        "post_evacuation_taqwiyaat": "Mufarrih Yaqooti Motadil 3g + Sheer-e-Gao Taaza with Roghan-e-Badam"
    }
}


class MunzijMushilProtocolEngine:
    """Clinical engine structuring safe 3-phase Munzij-Mushil interventions."""

    @classmethod
    def synthesize_protocol(
        cls,
        patient_id: str,
        target_humor: str,
        chronicity_level: str = "CHRONIC",
        has_active_nujz: bool = False,
    ) -> Dict[str, Any]:
        h_key = "Balgham"
        for k in MUNZIJ_FORMULATIONS.keys():
            if k.lower() in target_humor.lower():
                h_key = k
                break

        spec = MUNZIJ_FORMULATIONS[h_key]
        duration = spec["standard_duration_days"]
        if chronicity_level == "LONGSTANDING_SEVERE":
            duration = int(duration * 1.5)

        current_phase = "PHASE_1_NUJZ_CONCOCTION" if not has_active_nujz else "PHASE_2_TANQIYA_EVACUATION"

        return {
            "patient_id": patient_id,
            "target_pathological_humor": h_key,
            "classical_rule": "Lā tushil al-khilt mā lam yandaj (Do not purge until concocted)",
            "current_recommended_phase": current_phase,
            "nujz_phase": {
                "phase_name": "Stage 1: Nujz (Humoral Concoction)",
                "formula_name": spec["formula_name"],
                "prescribed_duration_days": duration,
                "ingredients": spec["ingredients"],
                "preparation_method": "Soak overnight in 250ml water, boil down to 100ml in morning, strain and drink warm.",
                "monitoring_signs_of_nujz": spec["signs_of_nujz"]
            },
            "tanqiya_phase": {
                "phase_name": "Stage 2: Tanqiya / Mushil (Targeted Evacuation)",
                "mushil_formula": spec["mushil_pairing"]["name"],
                "actives": spec["mushil_pairing"]["evacuant_actives"],
                "administration_timing": spec["mushil_pairing"]["timing"],
                "safety_precondition": "Administer ONLY when clinician observes at least 2 Alamat-e-Nujz."
            },
            "taqwiyaat_phase": {
                "phase_name": "Stage 3: Tabreed & Taqwiyat (Restoration)",
                "prescription": spec["post_evacuation_taqwiyaat"],
                "duration_days": 14
            },
            "clinician_signoff_required": True
        }
