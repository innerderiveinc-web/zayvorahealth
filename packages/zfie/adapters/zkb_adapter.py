"""
ZFIE Knowledge & Safety Adapters
ZKBAdapter: Read-only bridge to ZAYVORA Knowledge Base (cannot overwrite authoritative records).
SafetyFirewallAdapter: Connects ZFIE to the central Clinical Safety Firewall.
"""

from typing import Any, Dict, List, Optional
from packages.zfie.safety.safety_evaluator import ZFIESafetyEvaluator
from packages.zfie.core.enums import SafetyVerdict
from packages.zfie.core.errors import ZFIESafetyBlockError


class ZKBAdapter:
    """
    Read-only adapter querying classical references, Mufradat, Mizaj, Afaal, and Murakkabat.
    ZFIE cannot overwrite authoritative ZKB records.
    """

    @classmethod
    def query_substance(cls, mufrad_id: str) -> Dict[str, Any]:
        catalog = {
            "ZAY-MUF-0001": {
                "name": "Suranjan Shirin",
                "latin": "Colchicum autumnale L.",
                "mizaj": "Hot 2°, Dry 2° (Har Yabis)",
                "afaal": ["Musakkin-e-Waja (Analgesic)", "Mukhrij-e-Mawad (Depurative)", "Muhafiz-e-Mafasil (Joint Protector)"],
                "organ_axis": "Musculoskeletal & Excretory Axis",
                "classical_sources": ["Al-Qanun fi al-Tibb", "Bayaz-e-Kabeer", "Makhzan-al-Adwiya"],
                "authoritative_record": True
            },
            "ZAY-MUF-0002": {
                "name": "Filfil Siyah",
                "latin": "Piper nigrum L.",
                "mizaj": "Hot 3°, Dry 3° (Har Yabis)",
                "afaal": ["Kasir-e-Riyah (Carminative)", "Hazim (Digestive)", "Muqawwi-e-Hazm (Bio-enhancer)"],
                "organ_axis": "Gastrointestinal & Metabolic Axis",
                "classical_sources": ["Kitab al-Hawi", "Al-Qanun"],
                "authoritative_record": True
            }
        }
        return catalog.get(mufrad_id, {"name": "Unspecified Herb", "authoritative_record": True})

    @classmethod
    def attempt_mutation(cls, mufrad_id: str, new_data: Dict[str, Any]) -> None:
        """Explicitly blocks unauthorized writes into authoritative ZKB."""
        raise PermissionError("ZFIE is a computational inference layer and cannot overwrite authoritative ZKB records.")


class SafetyFirewallAdapter:
    """
    Integrates ZFIE with the Clinical Safety Firewall.
    Execution: ZFIE Result -> Safety Firewall -> PASS / CAUTION / BLOCK / UNKNOWN.
    A BLOCK verdict terminates downstream clinical execution.
    """

    @classmethod
    def evaluate_and_enforce(
        cls,
        formulation_id: str,
        ingredients: List[Dict[str, Any]],
        patient_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        result = ZFIESafetyEvaluator.evaluate_formulation(
            formulation_id=formulation_id,
            ingredients=ingredients,
            patient_context=patient_context
        )
        if result["verdict"] == SafetyVerdict.BLOCK.value:
            ZFIESafetyEvaluator.enforce_safety_gate(result)
        return result
