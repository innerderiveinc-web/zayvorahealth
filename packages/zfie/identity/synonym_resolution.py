"""
ZFIE Synonym Resolution & Entity Matching
Resolves vernacular names (Urdu, Arabic, Sanskrit, Hindi, Trade names) to Canonical IDs.
"""

from typing import Any, Dict, List, Optional, Tuple
from packages.zfie.identity.canonical_identity import CanonicalIdentityRegistry
from packages.zfie.core.enums import EntityType


class SynonymResolver:
    """Multi-lingual synonym dictionary resolving names to authoritative canonical IDs."""

    _SYNONYM_MAP: Dict[str, str] = {
        # Suranjan
        "suranjan": "ZAY-MUF-0001",
        "suranjan shirin": "ZAY-MUF-0001",
        "sweet meadow saffron": "ZAY-MUF-0001",
        "colchicum autumnale": "ZAY-MUF-0001",
        "colchicum luteum": "ZAY-MUF-0001",
        "autumn crocus": "ZAY-MUF-0001",
        # Filfil Siyah
        "filfil siyah": "ZAY-MUF-0002",
        "black pepper": "ZAY-MUF-0002",
        "piper nigrum": "ZAY-MUF-0002",
        "kali mirch": "ZAY-MUF-0002",
        "maricha": "ZAY-MUF-0002",
        # Muqil
        "muqil": "ZAY-MUF-0003",
        "guggul": "ZAY-MUF-0003",
        "guggulu": "ZAY-MUF-0003",
        "commiphora mukul": "ZAY-MUF-0003",
        "commiphora wightii": "ZAY-MUF-0003",
        "indian bdellium": "ZAY-MUF-0003",
        # Asgandh
        "asgandh": "ZAY-MUF-0004",
        "asgandh nagori": "ZAY-MUF-0004",
        "ashwagandha": "ZAY-MUF-0004",
        "withania somnifera": "ZAY-MUF-0004",
        "indian ginseng": "ZAY-MUF-0004",
        # Zanjabeel
        "zanjabeel": "ZAY-MUF-0005",
        "ginger": "ZAY-MUF-0005",
        "adrak": "ZAY-MUF-0005",
        "sonth": "ZAY-MUF-0005",
        "zingiber officinale": "ZAY-MUF-0005",
    }

    @classmethod
    def resolve_to_canonical_id(cls, raw_name: str) -> Optional[str]:
        if not raw_name:
            return None
        cleaned = raw_name.strip().lower()
        if cleaned in cls._SYNONYM_MAP:
            return cls._SYNONYM_MAP[cleaned]
        # Partial containment search
        for syn, cid in cls._SYNONYM_MAP.items():
            if syn in cleaned or cleaned in syn:
                return cid
        return None

    @classmethod
    def match_entity(cls, query: str) -> Dict[str, Any]:
        cid = cls.resolve_to_canonical_id(query)
        if not cid:
            return {"match_found": False, "query": query, "canonical_id": None, "confidence": 0.0}
        record = CanonicalIdentityRegistry.get(cid)
        return {
            "match_found": True,
            "query": query,
            "canonical_id": cid,
            "confidence": 0.98 if query.strip().lower() in cls._SYNONYM_MAP else 0.82,
            "entity": record
        }
