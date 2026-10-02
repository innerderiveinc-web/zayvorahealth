"""
ZAYVORA Health OS™ — Mufradat Patient Monograph Card Generator
===============================================================
Generates patient-friendly information cards from the 250 Mufradat
canonical registry records. Cards are bilingual (Urdu/English names)
and structured for safe patient education — clinical decisions remain
exclusively with the Hakeem.

Card Sections:
  1. Identity   — Arabic/Urdu name, English name, botanical name
  2. Mizaj      — Classical temperament (plain language)
  3. Key Uses   — Patient-friendly Afaal summary (max 3 points)
  4. Safety     — Contraindications and cautions (simplified)
  5. Dose Hint  — Classical dosage range (informational only)
  6. Governance — Mandatory governance footer (AI/patient disclaimer)
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

# ── Mizaj Plain-Language Map ──────────────────────────────────────────────────
MIZAJ_PLAIN: Dict[str, str] = {
    "Haar Ratab":         "Warm & Moist — supports vitality, circulation, and flexibility.",
    "Haar Yabis":         "Warm & Dry — stimulating, toning, and drying in nature.",
    "Barid Ratab":        "Cool & Moist — calming, soothing, and hydrating in nature.",
    "Barid Yabis":        "Cool & Dry — consolidating, astringent, and grounding in nature.",
    "Muaddil":            "Balanced — gently corrective, suits most constitutional types.",
    "Haar Ratab Daraja 1": "Mildly Warm & Moist — very gentle; suitable for most adults.",
    "Haar Ratab Daraja 2": "Moderately Warm & Moist — energizing and circulatory supportive.",
    "Haar Ratab Daraja 3": "Strongly Warm & Moist — potent; use with Hakeem guidance.",
    "Haar Yabis Daraja 2": "Moderately Warm & Dry — stimulating; avoid in hot constitutions.",
    "Haar Yabis Daraja 3": "Strongly Warm & Dry — very stimulating; specialist supervision.",
    "Barid Ratab Daraja 1": "Mildly Cool & Moist — soothing; safe for most adults.",
    "Barid Ratab Daraja 2": "Moderately Cool & Moist — cooling; reduces heat and inflammation.",
}

# ── Afaal Plain-Language Simplifier ──────────────────────────────────────────
AFAAL_PLAIN: Dict[str, str] = {
    "Muqawwi-e-Bah":      "Supports reproductive health",
    "Muqawwi-e-Asab":     "Supports nervous system strength",
    "Muqawwi-e-Dimagh":   "Supports brain function and memory",
    "Muqawwi-e-Qalb":     "Supports heart health",
    "Muqawwi-e-Jigar":    "Supports liver function",
    "Muqawwi-e-Meda":     "Supports digestive health",
    "Mufarrih-e-Qalb":    "Uplifts mood and heart",
    "Musakkin-e-Alam":    "Relieves pain naturally",
    "Muhallil-e-Waram":   "Reduces inflammation and swelling",
    "Munawwim":           "Promotes healthy sleep",
    "Mudir-e-Baul":       "Supports healthy urinary flow",
    "Mudir-e-Haiz":       "Supports healthy menstrual cycle",
    "Mushil":             "Gentle digestive cleansing",
    "Mulayyin":           "Gentle laxative action",
    "Muqil-e-Hararat":    "Reduces excess body heat",
    "Dafi-e-Tashannuj":   "Reduces muscle spasms",
    "Qatil-e-Kirm":       "Supports against intestinal parasites",
    "Muharrik":           "Energizing and stimulating",
    "Hafiz-e-Sehat":      "Overall health maintenance",
    "Hifz-e-Sehat":       "Overall health maintenance",
}

GOVERNANCE_FOOTER = (
    "⚕ IMPORTANT — Patient Education Card Only: This card provides general "
    "traditional information. It is NOT a prescription, medical advice, or "
    "treatment recommendation. Always consult your Hakeem or physician before "
    "using any herb or remedy. Self-medication is NOT permitted. "
    "ZAYVORA Health OS™ — all clinical decisions are made exclusively "
    "by your registered healthcare provider."
)

HIGH_RISK_PATIENT_NOTICE = (
    "🚫 RESTRICTED SUBSTANCE: This herb is classified as a high-risk substance "
    "under Indian drug regulations (Schedule E(1) or equivalent). It is NOT "
    "available for general use and requires specialist Hakeem prescription "
    "with certified Tadbeer (purification). Do NOT attempt to obtain or use "
    "this substance without your healthcare provider's explicit direction."
)


def _simplify_afaal(afaal_string: str) -> List[str]:
    """Convert comma-separated classical Afaal to patient-friendly points (max 3)."""
    if not afaal_string:
        return ["Traditional remedy — consult your Hakeem for specific uses."]
    parts = [p.strip() for p in afaal_string.replace(";", ",").split(",") if p.strip()]
    simplified = []
    for part in parts[:4]:
        for key, val in AFAAL_PLAIN.items():
            if key.lower() in part.lower():
                if val not in simplified:
                    simplified.append(val)
                break
        else:
            # Keep original but clean it
            clean = part.replace("-e-", " of ").replace("-ul-", " of ").strip()
            if clean and clean not in simplified:
                simplified.append(clean)
    return simplified[:3] if simplified else ["Traditional health support — consult your Hakeem."]


def _mizaj_plain(mizaj_str: str) -> str:
    """Return plain-language Mizaj description."""
    if not mizaj_str:
        return "Temperament not specified — your Hakeem will assess."
    for key, val in MIZAJ_PLAIN.items():
        if key.lower() in mizaj_str.lower():
            return val
    return f"Classical temperament: {mizaj_str}. Your Hakeem will explain."


class MufradatCardGenerator:
    """
    Patient Monograph Card Generator for ZAYVORA Mufradat 250.
    """

    @classmethod
    def generate_card(cls, zmf_id: str) -> Dict[str, Any]:
        """
        Generate a patient-friendly information card for a single Mufrad.

        Args:
            zmf_id: ZMF identifier (e.g. "ZMF-001") or common name.

        Returns:
            Dict containing structured patient card data.
        """
        if not _REGISTRY_AVAILABLE:
            return {"error": "Mufradat registry not available.", "zmf_id": zmf_id}

        record = get_mufrad_by_id(zmf_id)
        if not record:
            return {
                "error": f"No registry record found for '{zmf_id}'.",
                "zmf_id": zmf_id,
                "suggestion": "Verify ZMF ID or common name. Use /api/v1/knowledge/mufradat-250/all to list all records."
            }

        zmf_upper = record.get("id", zmf_id).upper()
        is_blocked = is_high_risk_blocked(zmf_upper)

        # Build key uses
        afaal_raw = record.get("afaal") or record.get("primary_afaal") or ""
        key_uses = _simplify_afaal(afaal_raw)

        # Mizaj plain language
        mizaj_raw = record.get("mizaj") or ""
        mizaj_description = _mizaj_plain(mizaj_raw)

        # Safety notice
        safety_notices = []
        if is_blocked:
            safety_notices.append(HIGH_RISK_PATIENT_NOTICE)
        contraindications = record.get("contraindications") or []
        if isinstance(contraindications, list):
            for ci in contraindications[:3]:
                safety_notices.append(f"Caution: {ci}")
        elif isinstance(contraindications, str) and contraindications:
            safety_notices.append(f"Caution: {contraindications}")

        # Dose hint (for registered Hakeem dispensing context only)
        dose_hint = record.get("dose_range") or record.get("classical_dose") or "Dose determined by your Hakeem based on clinical assessment."

        # Canonical group
        canonical_group = record.get("canonical_group") or "Not classified"

        card = {
            "card_type": "MUFRAD_PATIENT_MONOGRAPH",
            "zmf_id": zmf_upper,
            "identity": {
                "urdu_arabic_name": record.get("name") or zmf_upper,
                "english_name": record.get("english_name") or record.get("common_english") or "See Hakeem",
                "botanical_name": record.get("botanical") or record.get("botanical_name") or "Botanical identity in registry",
                "canonical_group": canonical_group,
                "part_used": record.get("part_used") or "Not specified",
            },
            "temperament": {
                "classical_mizaj": mizaj_raw or "See your Hakeem",
                "plain_description": mizaj_description,
            },
            "key_traditional_uses": key_uses,
            "safety": {
                "is_high_risk_restricted": is_blocked,
                "safety_notices": safety_notices if safety_notices else ["No specific patient-level cautions noted. Always consult your Hakeem."],
            },
            "dose_information": {
                "classical_dose_range": dose_hint,
                "dose_note": "Dosage is ALWAYS determined by your registered Hakeem. Never self-administer.",
            },
            "governance": {
                "ai_permission_state": record.get("ai_permission_state") or "RESEARCH_ONLY",
                "clinical_use_state": record.get("clinical_use_state") or "NOT_APPROVED",
                "patient_self_care": record.get("patient_self_care") or "NOT_ALLOWED",
                "footer": GOVERNANCE_FOOTER,
            }
        }
        return card

    @classmethod
    def generate_batch_cards(cls, zmf_ids: List[str]) -> Dict[str, Any]:
        """Generate patient cards for multiple Mufradat."""
        cards = {}
        errors = []
        for zmf_id in zmf_ids:
            result = cls.generate_card(zmf_id)
            if "error" in result:
                errors.append({"zmf_id": zmf_id, "error": result["error"]})
            else:
                cards[zmf_id.upper()] = result
        return {
            "total_requested": len(zmf_ids),
            "cards_generated": len(cards),
            "errors": errors,
            "cards": cards
        }

    @classmethod
    def generate_seed_cards(cls) -> Dict[str, Any]:
        """Generate patient cards for the 6 Internal Seed Mufradat."""
        seed_ids = ["ZMF-001", "ZMF-003", "ZMF-004", "ZMF-005", "ZMF-006"]
        return cls.generate_batch_cards(seed_ids)
