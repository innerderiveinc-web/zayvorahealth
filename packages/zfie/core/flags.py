"""
ZAYVORA Formulation Intelligence Engine™ (ZFIE)
Section 68 — Feature Flag Governance Module
System: ZAYVORA Health OS™

Initial Deployment Configuration:
ZFIE_ENABLED=true
ZFIE_RESEARCH_ENABLED=true
ZFIE_SHADOW_MODE=true
ZFIE_CLINICAL_CDS_ENABLED=false
ZFIE_SYNERGY_ENABLED=false
ZFIE_BIOLOGICAL_STATE_ENABLED=false
ZFIE_EXPERIMENT_PLANNER_ENABLED=false

Principle: Shadow Mode only. Clinical workflows continue unchanged.
"""

import os
from typing import Dict, Any


def _parse_bool(val: Any, default: bool = False) -> bool:
    if val is None:
        return default
    if isinstance(val, bool):
        return val
    str_val = str(val).strip().lower()
    return str_val in ("true", "1", "t", "yes", "y", "enabled")


class ZFIESettings:
    """Manages active runtime flags for ZFIE."""

    @classmethod
    def is_zfie_enabled(cls) -> bool:
        return _parse_bool(os.environ.get("ZFIE_ENABLED", "true"), default=True)

    @classmethod
    def is_research_enabled(cls) -> bool:
        return _parse_bool(os.environ.get("ZFIE_RESEARCH_ENABLED", "true"), default=True)

    @classmethod
    def is_shadow_mode(cls) -> bool:
        return _parse_bool(os.environ.get("ZFIE_SHADOW_MODE", "true"), default=True)

    @classmethod
    def is_clinical_cds_enabled(cls) -> bool:
        # Default false per Section 68
        return _parse_bool(os.environ.get("ZFIE_CLINICAL_CDS_ENABLED", "false"), default=False)

    @classmethod
    def is_synergy_enabled(cls) -> bool:
        # Default false per Section 68
        return _parse_bool(os.environ.get("ZFIE_SYNERGY_ENABLED", "false"), default=False)

    @classmethod
    def is_biological_state_enabled(cls) -> bool:
        # Default false per Section 68
        return _parse_bool(os.environ.get("ZFIE_BIOLOGICAL_STATE_ENABLED", "false"), default=False)

    @classmethod
    def is_experiment_planner_enabled(cls) -> bool:
        # Default false per Section 68
        return _parse_bool(os.environ.get("ZFIE_EXPERIMENT_PLANNER_ENABLED", "false"), default=False)

    @classmethod
    def get_flags(cls) -> Dict[str, bool]:
        return {
            "ZFIE_ENABLED": cls.is_zfie_enabled(),
            "ZFIE_RESEARCH_ENABLED": cls.is_research_enabled(),
            "ZFIE_SHADOW_MODE": cls.is_shadow_mode(),
            "ZFIE_CLINICAL_CDS_ENABLED": cls.is_clinical_cds_enabled(),
            "ZFIE_SYNERGY_ENABLED": cls.is_synergy_enabled(),
            "ZFIE_BIOLOGICAL_STATE_ENABLED": cls.is_biological_state_enabled(),
            "ZFIE_EXPERIMENT_PLANNER_ENABLED": cls.is_experiment_planner_enabled(),
        }
