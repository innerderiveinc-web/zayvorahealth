"""
Standard Unani Medical Terminology Engine (CCRUM / AYUSH UMA Codification)
==========================================================================
Codifies and indexes the 1,593+ Standard Unani Medical Terms (UMA-0001 to UMA-1640)
from the statutory/canonical publication of the Central Council for Research in
Unani Medicine (CCRUM), Ministry of AYUSH, Government of India.

Provides bi-directional translation between classical Greco-Arab Unani medical
terminology (Mufarradat, Murakkabat, Ilm al-Amrad, Tashkhees, Jarahat) and
modern ICD/biomedical diagnostics.
"""

import json
import os
import re
from typing import Dict, List, Optional, Any

_DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "standard_unani_terminology_uma.json"
)

class StandardUnaniTerminologyEngine:
    _instance = None

    def __init__(self, data_file: Optional[str] = None):
        self.data_file = data_file or _DATA_FILE
        self.terms: List[Dict[str, Any]] = []
        self.by_code: Dict[str, Dict[str, Any]] = {}
        self.by_unani_lower: Dict[str, List[Dict[str, Any]]] = {}
        self.by_english_lower: Dict[str, List[Dict[str, Any]]] = {}
        self._load_data()

    def _load_data(self):
        if not os.path.exists(self.data_file):
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                self.terms = json.load(f)
            
            for item in self.terms:
                code = item.get("uma_code", "").strip().upper()
                if code:
                    self.by_code[code] = item
                
                u_term = item.get("unani_term", "").strip().lower()
                if u_term:
                    if u_term not in self.by_unani_lower:
                        self.by_unani_lower[u_term] = []
                    self.by_unani_lower[u_term].append(item)
                
                eng_eq = item.get("english_equivalent", "").strip().lower()
                if eng_eq:
                    if eng_eq not in self.by_english_lower:
                        self.by_english_lower[eng_eq] = []
                    self.by_english_lower[eng_eq].append(item)
        except Exception as e:
            print(f"[StandardUnaniTerminologyEngine] Error loading data: {e}")

    def get_term_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Lookup by UMA code (e.g. 'UMA-0002' or 'uma-1640')"""
        clean_code = code.strip().upper()
        if not clean_code.startswith("UMA-"):
            # If user passed just digits or UMA digits
            digits = re.findall(r"\d+", clean_code)
            if digits:
                clean_code = f"UMA-{int(digits[0]):04d}"
        return self.by_code.get(clean_code)

    def search_terms(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search across code, Unani name, English equivalent, and definition text."""
        q = (query or "").strip().lower()
        if not q:
            return self.terms[:limit]

        # Exact code match prioritized
        if q.upper() in self.by_code:
            return [self.by_code[q.upper()]]

        results = []
        for item in self.terms:
            code = item.get("uma_code", "").lower()
            unani = item.get("unani_term", "").lower()
            eng = item.get("english_equivalent", "").lower()
            defn = item.get("definition", "").lower()

            score = 0
            if q == unani or q == eng or q == code:
                score += 100
            elif unani.startswith(q) or eng.startswith(q):
                score += 50
            elif q in unani or q in eng:
                score += 30
            elif q in defn:
                score += 10

            if score > 0:
                results.append((score, item))

        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:limit]]

    def lookup_unani_to_biomedical(self, unani_name: str) -> List[Dict[str, Any]]:
        """Return matches for an Unani term giving modern clinical equivalents."""
        q = (unani_name or "").strip().lower()
        if not q:
            return []
        if q in self.by_unani_lower:
            return self.by_unani_lower[q]
        # Partial match
        return [t for t in self.terms if q in t.get("unani_term", "").lower()]

    def lookup_biomedical_to_unani(self, biomedical_term: str) -> List[Dict[str, Any]]:
        """Return matches for modern clinical disease/symptom pointing to Unani classification."""
        q = (biomedical_term or "").strip().lower()
        if not q:
            return []
        if q in self.by_english_lower:
            return self.by_english_lower[q]
        # Partial match
        return [t for t in self.terms if q in t.get("english_equivalent", "").lower() or q in t.get("definition", "").lower()]

    def get_statistics(self) -> Dict[str, Any]:
        """Return summary statistics of the standardized terminology registry."""
        with_eng = sum(1 for t in self.terms if t.get("english_equivalent"))
        return {
            "total_terms": len(self.terms),
            "terms_with_biomedical_equivalents": with_eng,
            "coverage_percentage": round((with_eng / len(self.terms) * 100), 1) if self.terms else 0,
            "statutory_authority": "CCRUM / Ministry of AYUSH, Government of India",
            "source_standard": "Standard Unani Medical Terminology (1,430/1,640 terms)",
            "highest_code": self.terms[-1]["uma_code"] if self.terms else None
        }

# Global Singleton
_global_engine: Optional[StandardUnaniTerminologyEngine] = None

def get_terminology_engine() -> StandardUnaniTerminologyEngine:
    global _global_engine
    if _global_engine is None:
        _global_engine = StandardUnaniTerminologyEngine()
    return _global_engine
