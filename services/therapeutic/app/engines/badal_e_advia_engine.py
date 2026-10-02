"""
ZAYVORA Health OS™ — Badal-e-Advia (Botanical Substitute Advisory) Engine
==========================================================================
Classical Unani concept of Badal (Badeel / Khalaf): When a prescribed
Mufrad is unavailable, restricted (HIGH_RISK_28), or contraindicated,
the Hakeem selects a pharmacologically equivalent substitute sharing
the same Mizaj, primary Afaal, and organ affinity.

Sources: Ibn Sina's Qanoon, Kabeeruddin's Makhzan-ul-Advia,
         ZAYVORA Mufradat 250 Canonical Registry.

Rules for Badal selection:
  1. Same Temperament (Mizaj) as original — Hot/Cold/Moist/Dry match.
  2. Same primary therapeutic action (Amal/Fail).
  3. Same or lower Daraja (strength degree) — never escalate potency.
  4. Absent from HIGH_RISK_28 registry (safe substitutes only).
  5. Prefer same organ system affinity.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
import sys, os

try:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../..")))
    from services.knowledge.app.data.mufradat_250_registry import (
        get_all_mufradat_250,
        get_mufrad_by_id,
        is_high_risk_blocked,
        get_high_risk_28_registry,
    )
    _REGISTRY_AVAILABLE = True
except ImportError:
    _REGISTRY_AVAILABLE = False

# ── Classical Badal (Substitute) Knowledge Base ───────────────────────────────
# Format: original_drug_lower → list of substitute dicts
# Each substitute: name, zmf_id, mizaj, afaal, notes, daraja_equivalence
CLASSICAL_BADAL_MAP: Dict[str, List[Dict[str, Any]]] = {
    # High-Risk Substitutions (blocked substances → safe alternatives)
    "suranjan talkh": [
        {"name": "Haldi (Curcuma longa)", "zmf_id": "ZMF-057", "mizaj": "Haar Yabis Daraja 2",
         "afaal": "Anti-inflammatory, Musakkil-e-Waram",
         "notes": "For joint inflammation: Haldi with Methi provides anti-inflammatory action without colchicine toxicity.",
         "daraja_equivalence": "LOWER_SAFER", "organ_affinity": "Joints, Liver"},
        {"name": "Ajwain (Trachyspermum ammi)", "zmf_id": "ZMF-012", "mizaj": "Haar Yabis Daraja 3",
         "afaal": "Mudir-e-Baul, Qatil-e-Kirm, Muharrik",
         "notes": "For gouty conditions: Ajwain with Kalonji addresses uric acid pathway safely.",
         "daraja_equivalence": "EQUIVALENT", "organ_affinity": "Joints, Kidney, GI"},
    ],
    "jamalgota": [
        {"name": "Sana Makki (Cassia senna)", "zmf_id": "ZMF-088", "mizaj": "Haar Yabis Daraja 2",
         "afaal": "Mushil-e-Safra, Laxative",
         "notes": "For purgation: Sana Makki provides safe anthraquinone-based catharsis without Jamalgota toxicity.",
         "daraja_equivalence": "LOWER_SAFER", "organ_affinity": "Colon, Liver"},
        {"name": "Isabgol (Plantago ovata)", "zmf_id": "ZMF-083", "mizaj": "Barid Ratab Daraja 1",
         "afaal": "Mulayyin, Musakkin, Mudir-e-Baul",
         "notes": "For constipation: Isabgol offers gentle bulk laxation, completely safe.",
         "daraja_equivalence": "LOWER_SAFER", "organ_affinity": "Colon, GI"},
    ],
    "ajwain khurasani": [
        {"name": "Ustukhuddus (Lavandula stoechas)", "zmf_id": "ZMF-004", "mizaj": "Haar Ratab Daraja 2",
         "afaal": "Musakkin-e-Alam, Muqawwi-e-Dimagh, Munawwim",
         "notes": "For neurological calm and sleep: Ustukhuddus lacks anticholinergic toxicity.",
         "daraja_equivalence": "EQUIVALENT", "organ_affinity": "Brain, Nerves"},
        {"name": "Gaozaban (Borago officinalis)", "zmf_id": "ZMF-006", "mizaj": "Haar Ratab Daraja 2",
         "afaal": "Mufarrih-e-Qalb, Muqawwi-e-Dimagh, Munawwim",
         "notes": "For anxiety, palpitation, and insomnia.",
         "daraja_equivalence": "LOWER_SAFER", "organ_affinity": "Heart, Brain"},
    ],
    "afeem": [
        {"name": "Kahu (Lactuca virosa)", "zmf_id": "ZMF-092", "mizaj": "Barid Ratab Daraja 2",
         "afaal": "Munawwim, Musakkin-e-Alam, Muqil-e-Hararat",
         "notes": "For pain and insomnia: Kahu provides mild sedation without opiate dependency risk.",
         "daraja_equivalence": "LOWER_SAFER", "organ_affinity": "Brain, Nerves"},
        {"name": "Asgandh (Withania somnifera)", "zmf_id": "ZMF-001", "mizaj": "Haar Ratab Daraja 2",
         "afaal": "Muqawwi-e-Bah, Muqawwi-e-Asab, Munawwim (adaptogenic)",
         "notes": "For pain-fatigue complex: Ashwagandha addresses central sensitization safely.",
         "daraja_equivalence": "LOWER_SAFER", "organ_affinity": "Nerves, Adrenals, Reproductive"},
    ],
    "bhang": [
        {"name": "Asgandh (Withania somnifera)", "zmf_id": "ZMF-001", "mizaj": "Haar Ratab Daraja 2",
         "afaal": "Muqawwi-e-Asab, Musakkin, Adaptogenic",
         "notes": "For anxiety and stress: Ashwagandha modulates HPA axis without psychotropic risks.",
         "daraja_equivalence": "LOWER_SAFER", "organ_affinity": "Nerves, Adrenals"},
        {"name": "Babchi (Psoralea corylifolia)", "zmf_id": "ZMF-003", "mizaj": "Haar Yabis Daraja 3",
         "afaal": "Muqawwi-e-Asab, Muhallil-e-Waram",
         "notes": "For skin and nerve conditions where Bhang was classically used.",
         "daraja_equivalence": "DIFFERENT_ACTION", "organ_affinity": "Skin, Nerves"},
    ],
    "dhatura": [
        {"name": "Ustukhuddus (Lavandula stoechas)", "zmf_id": "ZMF-004", "mizaj": "Haar Ratab Daraja 2",
         "afaal": "Musakkin-e-Alam, Muqawwi-e-Dimagh",
         "notes": "For antispasmodic effect without anticholinergic toxicity.",
         "daraja_equivalence": "LOWER_SAFER", "organ_affinity": "Brain, Nerves, GI"},
    ],
    "bish": [
        {"name": "Asgandh (Withania somnifera)", "zmf_id": "ZMF-001", "mizaj": "Haar Ratab Daraja 2",
         "afaal": "Muqawwi, Musakkin-e-Alam (adaptogenic pain modulation)",
         "notes": "For neuralgic pain: Ashwagandha modulates pain centrally without cardiotoxicity.",
         "daraja_equivalence": "LOWER_SAFER", "organ_affinity": "Nerves, Joints"},
    ],
    "kuchla": [
        {"name": "Filfil Siyah (Piper nigrum)", "zmf_id": "ZMF-005", "mizaj": "Haar Yabis Daraja 3",
         "afaal": "Muharrik-e-Asab, Mudir, Muqawwi",
         "notes": "For nerve stimulation: Piperine enhances bioavailability and neuronal activity safely.",
         "daraja_equivalence": "LOWER_SAFER", "organ_affinity": "Nerves, GI, Circulation"},
    ],
    # Common safe-drug substitutions (for unavailability, not toxicity)
    "babchi": [
        {"name": "Asgandh (Withania somnifera)", "zmf_id": "ZMF-001", "mizaj": "Haar Ratab Daraja 2",
         "afaal": "Muqawwi-e-Asab, Anti-inflammatory",
         "notes": "If Babchi unavailable for skin conditions, Asgandh provides adaptogenic anti-inflammatory support.",
         "daraja_equivalence": "DIFFERENT_INDICATION", "organ_affinity": "Skin, Nerves"},
    ],
    "ustukhuddus": [
        {"name": "Gaozaban (Borago officinalis)", "zmf_id": "ZMF-006", "mizaj": "Haar Ratab Daraja 2",
         "afaal": "Mufarrih-e-Qalb, Muqawwi-e-Dimagh",
         "notes": "For neurological and cardiac indications of Lavandula, Gaozaban is the classical Badal.",
         "daraja_equivalence": "EQUIVALENT", "organ_affinity": "Heart, Brain, Nerves"},
    ],
}

# Mizaj-based fallback matching
MIZAJ_BADAL_POOL: List[Dict[str, Any]] = [
    {"name": "Asgandh",      "zmf_id": "ZMF-001", "mizaj_class": "HAAR_RATAB",  "daraja": 2},
    {"name": "Ustukhuddus",  "zmf_id": "ZMF-004", "mizaj_class": "HAAR_RATAB",  "daraja": 2},
    {"name": "Gaozaban",     "zmf_id": "ZMF-006", "mizaj_class": "HAAR_RATAB",  "daraja": 2},
    {"name": "Babchi",       "zmf_id": "ZMF-003", "mizaj_class": "HAAR_YABIS",  "daraja": 3},
    {"name": "Filfil Siyah", "zmf_id": "ZMF-005", "mizaj_class": "HAAR_YABIS",  "daraja": 3},
    {"name": "Sana Makki",   "zmf_id": "ZMF-088", "mizaj_class": "HAAR_YABIS",  "daraja": 2},
    {"name": "Isabgol",      "zmf_id": "ZMF-083", "mizaj_class": "BARID_RATAB", "daraja": 1},
    {"name": "Kahu",         "zmf_id": "ZMF-092", "mizaj_class": "BARID_RATAB", "daraja": 2},
]


class BadalEAdviaEngine:
    """
    Badal-e-Advia (Classical Botanical Substitute Advisory) Engine.

    For any requested Mufrad — especially HIGH_RISK_28 blocked substances —
    provides classical substitution recommendations with Mizaj, Afaal,
    and safety profile matching.
    """

    @classmethod
    def get_badal_recommendations(
        cls,
        ingredient_name: str,
        zmf_id: str = "",
        indication: str = "",
        patient_mizaj: str = ""
    ) -> Dict[str, Any]:
        """
        Return classical Badal-e-Advia recommendations for a given ingredient.

        Args:
            ingredient_name: Name of the ingredient to substitute.
            zmf_id:          ZMF identifier if known.
            indication:      Clinical indication for context.
            patient_mizaj:   Patient's Mizaj for personalized matching.
        """
        name_lower = ingredient_name.strip().lower()
        zmf_upper = zmf_id.strip().upper() if zmf_id else ""

        # Determine if original is blocked
        is_blocked = False
        block_reason = ""
        if zmf_upper and _REGISTRY_AVAILABLE:
            is_blocked = is_high_risk_blocked(zmf_upper)
            if is_blocked:
                hr = get_high_risk_28_registry().get(zmf_upper, {})
                block_reason = (
                    f"{hr.get('category', 'HIGH_RISK')} — "
                    f"Primary toxin: {hr.get('primary_toxin', 'N/A')}. "
                    f"{hr.get('restriction', 'AI_BLOCKED.')}"
                )

        # Look up in classical Badal map
        substitutes = []
        for key, subs in CLASSICAL_BADAL_MAP.items():
            if key in name_lower or (zmf_upper and any(s.get("zmf_id") == zmf_upper for s in subs)):
                substitutes = subs
                break

        # Mizaj-based fallback if no direct Badal found
        mizaj_fallback = []
        if not substitutes and patient_mizaj:
            mz_lower = patient_mizaj.lower()
            if "haar" in mz_lower and "ratab" in mz_lower:
                mizaj_fallback = [x for x in MIZAJ_BADAL_POOL if x["mizaj_class"] == "HAAR_RATAB"]
            elif "haar" in mz_lower and "yabis" in mz_lower:
                mizaj_fallback = [x for x in MIZAJ_BADAL_POOL if x["mizaj_class"] == "HAAR_YABIS"]
            elif "barid" in mz_lower and "ratab" in mz_lower:
                mizaj_fallback = [x for x in MIZAJ_BADAL_POOL if x["mizaj_class"] == "BARID_RATAB"]

        classical_doctrine = (
            "Badal-e-Advia Principle (Ibn Sina, Qanoon fil-Tibb): A substitute must match "
            "the original in Mizaj, primary Amal, Daraja, and organ affinity. "
            "A Badal of lower Daraja is always preferred over one of higher Daraja. "
            "The Hakeem must verify equivalence in clinical context before dispensing."
        )

        return {
            "original_ingredient": ingredient_name,
            "zmf_id": zmf_upper or "UNTAGGED",
            "is_high_risk_blocked": is_blocked,
            "block_reason": block_reason if is_blocked else None,
            "indication": indication or "Not specified",
            "patient_mizaj": patient_mizaj or "Not specified",
            "classical_substitutes": substitutes,
            "mizaj_based_fallback": mizaj_fallback,
            "total_recommendations": len(substitutes) + len(mizaj_fallback),
            "classical_doctrine": classical_doctrine,
            "governance_note": (
                "All Badal recommendations require Hakeem clinical judgment. "
                "Substitutes provided are classical equivalents — not pharmaceutical bioequivalents. "
                "Final selection must consider patient Mizaj, disease state, and drug availability."
            )
        }

    @classmethod
    def get_all_badal_entries(cls) -> Dict[str, Any]:
        """Return the complete classical Badal-e-Advia knowledge base."""
        return {
            "total_entries": len(CLASSICAL_BADAL_MAP),
            "total_substitutes": sum(len(v) for v in CLASSICAL_BADAL_MAP.values()),
            "entries": {
                orig: {
                    "original": orig,
                    "substitutes": subs,
                    "count": len(subs)
                }
                for orig, subs in CLASSICAL_BADAL_MAP.items()
            },
            "governance_note": "Classical Badal knowledge base — not exhaustive. Expands with each drug monograph review."
        }
