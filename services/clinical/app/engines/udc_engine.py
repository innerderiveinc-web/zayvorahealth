"""
ZAYVORA Health OS™ — Unani Diagnosis Code (UDC) Engine
Source: Dr. Irfan Ashraf — The Organ-Axis Clinical System (Chapter 5)
Standardized format: [Mizaj] — [Dominant Khilt] — [Primary Organ-Axis] — [Afaal Phase]
Example: Balghami-Sawdawi — Balgham Ghalib — Jigar-Kulya — Phase 1 (Tanqiya)
"""
from typing import Dict, Any, List, Optional
import re

VALID_MIZAJ = [
    "Damvi", "Damawi",
    "Safravi", "Safrawi",
    "Balghami",
    "Saudavi", "Sawdawi",
    "Damvi-Balghami", "Damawi-Balghami",
    "Safravi-Saudavi", "Safrawi-Sawdawi",
    "Balghami-Saudavi", "Balghami-Sawdawi",
    "Damvi-Safravi", "Damawi-Safrawi",
    "Mu'tadil"
]

VALID_AKHLAT = [
    "Dam Ghalib", "Dam",
    "Safra Ghalib", "Safra",
    "Balgham Ghalib", "Balgham",
    "Sauda Ghalib", "Sauda",
    "Balgham/Sauda Ghalib", "Safra/Sauda mixed", "Safra/Balgham alternating",
    "Fasad-e-Balgham", "Fasad-e-Safra", "Fasad-e-Sauda", "Fasad-e-Dam"
]

VALID_AXES = [
    "Gut-Liver", "Jigar-Kulya", "Meda-Amaa",
    "Liver-Pancreas", "Jigar-Banas",
    "Gut-Ovarian", "Reham-Mabaysim", "Quwwat-e-Tanasul (F)",
    "Liver-Testicular", "Khusyatain-Dam", "Quwwat-e-Tanasul (M)",
    "Thyroid-Neuro", "Tihal-Ghudad", "Ghudad-Hazm",
    "HPA Axis", "Dimagh-Qalb", "Dimagh-Aasab"
]

VALID_PHASES = [
    "Phase 1 (Tanqiya)", "Phase 1 (Stabilization)", "Tanqiya",
    "Phase 2 (Tahleel)", "Phase 2 (Axis Correction)", "Tahleel",
    "Phase 3 (Taqwiyaat)", "Phase 3 (Consolidation)", "Taqwiyaat",
    "Phase 4 (Hifz)", "Phase 4 (Preservation)", "Hifz"
]

PROTOCOL_MAP = {
    "Quwwat-e-Tanasul (M)": "MF-01",
    "Liver-Testicular": "MF-01",
    "Khusyatain-Dam": "MF-01",
    "Quwwat-e-Tanasul (F)": "PC-01",
    "Gut-Ovarian": "PC-01",
    "Reham-Mabaysim": "PC-01",
    "HPA Axis": "NE-01",
    "Dimagh-Qalb": "NE-01",
    "Dimagh-Aasab": "NE-01",
    "Jigar-Kulya": "WM-01",
    "Liver-Pancreas": "WM-01",
    "Gut-Liver": "WM-01",
    "Meda-Amaa": "GI-01",
    "Tihal-Ghudad": "TG-01",
    "Thyroid-Neuro": "TG-01",
    "Riya-Qasba": "RS-01"
}


def generate_udc(mizaj: str, dominant_khilt: str, primary_axis: str, afaal_phase: str) -> str:
    """
    Generates a canonical Unani Diagnosis Code (UDC) string.
    Format: [Mizaj] — [Dominant Khilt] — [Primary Organ-Axis] — [Afaal Phase]
    """
    m = mizaj.strip()
    k = dominant_khilt.strip()
    a = primary_axis.strip()
    p = afaal_phase.strip()
    return f"{m} — {k} — {a} — {p}"


def parse_udc(udc_str: str) -> Dict[str, Any]:
    """
    Parses a UDC string into its constitutional, humoral, organ-axis, and phase components.
    Validates clinical constraints (e.g. Phase 1 Tanqiya constraints).
    """
    parts = [part.strip() for part in re.split(r'\s+[—–-]\s+|\s*[—–]\s*', udc_str) if part.strip()]
    if len(parts) < 4:
        return {
            "valid": False,
            "error": "UDC must contain 4 parts: [Mizaj] — [Dominant Khilt] — [Primary Organ-Axis] — [Afaal Phase]",
            "raw": udc_str
        }

    mizaj, khilt, axis, phase = parts[0], parts[1], parts[2], parts[3]
    
    # Clinical Constraints Engine
    is_tanqiya = "Tanqiya" in phase or "Phase 1" in phase or "Stabilization" in phase
    is_tahleel = "Tahleel" in phase or "Phase 2" in phase or "Correction" in phase
    is_taqwiyat = "Taqwiyaat" in phase or "Phase 3" in phase or "Consolidation" in phase
    is_hifz = "Hifz" in phase or "Phase 4" in phase or "Preservation" in phase

    # Constraints
    constraints = []
    if is_tanqiya:
        constraints.append("PHASE 1 CONSTRAINT: Absolutely no heavy Muqawwi (tonifying/strengthening) herbs. Elimination and clearing agents only.")
        constraints.append("RULE: Isaal (humoral evacuation) must precede Taghdiya (nourishment).")
    elif is_tahleel:
        constraints.append("PHASE 2 CONSTRAINT: Muhallilat (anti-inflammatory resolvents) active. Maintain hepatic support.")
    elif is_taqwiyat:
        constraints.append("PHASE 3 CONSTRAINT: Tissue rebuilding active. Full Muqawwi tonics permitted. Monitor organ capacity recovery.")
    elif is_hifz:
        constraints.append("PHASE 4 CONSTRAINT: Lifestyle lock-in (Asbab-e-Sitta) and seasonal Tanqiya maintenance.")

    recommended_protocol = PROTOCOL_MAP.get(axis, "Custom-Axis-Protocol")

    return {
        "valid": True,
        "udc_code": f"{mizaj} — {khilt} — {axis} — {phase}",
        "mizaj": mizaj,
        "dominant_khilt": khilt,
        "primary_axis": axis,
        "afaal_phase": phase,
        "phase_category": "Tanqiya" if is_tanqiya else "Tahleel" if is_tahleel else "Taqwiyaat" if is_taqwiyat else "Hifz",
        "recommended_protocol": recommended_protocol,
        "clinical_constraints": constraints
    }
