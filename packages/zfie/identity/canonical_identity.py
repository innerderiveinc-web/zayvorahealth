"""
ZFIE Canonical Identity Service
Enforces immutable, canonical identifiers for all biological, chemical,
and pharmaceutical entities across ZAYVORA.
Names & synonyms are attributes, never primary keys.
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional
from packages.zfie.core.enums import EntityType


class CanonicalIdentityRegistry:
    """Registry maintaining authoritative mappings from canonical IDs to entity definitions."""

    _PREFIXES = {
        EntityType.MUFRAD: "ZAY-MUF-",
        EntityType.MURAKKAB: "ZAY-MUR-",
        EntityType.FORMULATION: "ZAY-FORM-",
        EntityType.FORMULA_VERSION: "FORM-VER-",
        EntityType.BATCH: "ZAY-BATCH-",
        EntityType.COMPOUND: "ZAY-CMP-",
        EntityType.TARGET: "ZAY-TGT-",
        EntityType.PATHWAY: "ZAY-PWY-",
        EntityType.BIOMARKER: "ZAY-BMK-",
        EntityType.EVIDENCE: "ZAY-EVD-",
        EntityType.HYPOTHESIS: "ZAY-HYP-",
        EntityType.EXPERIMENT: "ZAY-EXP-",
        EntityType.OUTCOME: "ZAY-OUT-",
    }

    _ENTITIES: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def generate_id(cls, entity_type: EntityType, unique_seed: str) -> str:
        """Generates deterministic, collision-resistant canonical ID from seed."""
        prefix = cls._PREFIXES.get(entity_type, "ZAY-ENT-")
        clean_seed = unique_seed.strip().lower()
        hash_suffix = hashlib.sha256(clean_seed.encode("utf-8")).hexdigest()[:8].upper()
        return f"{prefix}{hash_suffix}"

    @classmethod
    def register(cls, canonical_id: str, entity_type: EntityType, metadata: Dict[str, Any]) -> str:
        cls._ENTITIES[canonical_id] = {
            "canonical_id": canonical_id,
            "entity_type": entity_type.value,
            "metadata": metadata
        }
        return canonical_id

    @classmethod
    def get(cls, canonical_id: str) -> Optional[Dict[str, Any]]:
        return cls._ENTITIES.get(canonical_id)

    @classmethod
    def list_by_type(cls, entity_type: EntityType) -> List[Dict[str, Any]]:
        return [
            v for v in cls._ENTITIES.values()
            if v.get("entity_type") == entity_type.value
        ]


# Seed foundational canonical entries
_DEFAULT_SUBSTANCES = [
    ("ZAY-MUF-0001", "Colchicum autumnale", "Suranjan Shirin", "Colchicum luteum Baker"),
    ("ZAY-MUF-0002", "Piper nigrum", "Filfil Siyah", "Black Pepper"),
    ("ZAY-MUF-0003", "Commiphora mukul", "Muqil", "Guggulu"),
    ("ZAY-MUF-0004", "Withania somnifera", "Asgandh", "Ashwagandha"),
    ("ZAY-MUF-0005", "Zingiber officinale", "Zanjabeel", "Ginger")
]

for cid, latin, urdu, english in _DEFAULT_SUBSTANCES:
    CanonicalIdentityRegistry.register(
        cid,
        EntityType.MUFRAD,
        {"latin_name": latin, "urdu_name": urdu, "english_name": english}
    )
