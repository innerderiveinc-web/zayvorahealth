"""
ZAYVORA HEALTH™ — Global Command Center (Cmd+K) Unified Omni-Search Engine
Indexes cross-domain clinical entities: Mufradat, Murakkabat, Amraz/ICD-11, Tadbeer Regimens, and Navigation actions.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import re
from .pharmacopoeia import UPI_MUFRADAT_REGISTRY, NFUM_COMPOUND_REGISTRY


@dataclass
class SearchResultItem:
    id: str
    category: str        # "mufradat", "murakkabat", "amraz", "tadbeer", "navigation"
    title: str
    subtitle: str
    badge: Optional[str] = None
    route: str = "/"
    metadata: Dict[str, Any] = field(default_factory=dict)


# Canonical Unani Amraz & ICD-11 Reference Table
AMRAZ_INDEX = [
    {"id": "AMR-001", "name": "Niqras (Podagra / Gout)", "icd11": "FA20", "system": "Articular / Metabolic", "mizaj": "Damawi-Safrawi"},
    {"id": "AMR-002", "name": "Waja-ul-Mafasil (Polyarthritis)", "icd11": "FA20.Z", "system": "Musculoskeletal", "mizaj": "Balghami"},
    {"id": "AMR-003", "name": "Su-i-Mizaj Meda Haar (Bilious Gastritis)", "icd11": "DA42", "system": "Gastrointestinal", "mizaj": "Safrawi"},
    {"id": "AMR-004", "name": "Zia-e-Baitus Shakari (Type 2 Diabetes)", "icd11": "5A11", "system": "Endocrine / Renal", "mizaj": "Barid Yabis"},
    {"id": "AMR-005", "name": "Bars (Vitiligo / Leukoderma)", "icd11": "EB90", "system": "Dermatological", "mizaj": "Barid Ratab"},
    {"id": "AMR-006", "name": "Sual-e-Muzmin (Chronic Bronchitis)", "icd11": "CA20", "system": "Respiratory", "mizaj": "Balghami"},
    {"id": "AMR-007", "name": "Zof-e-Meda (Atonic Dyspepsia)", "icd11": "DA44", "system": "Gastrointestinal", "mizaj": "Barid"},
    {"id": "AMR-008", "name": "Irq-un-Nasa (Sciatica)", "icd11": "ME84.1", "system": "Neurological", "mizaj": "Balghami-Saudawi"},
    {"id": "AMR-009", "name": "Khafaqan (Cardiac Palpitations)", "icd11": "MB40.0", "system": "Cardiovascular", "mizaj": "Saudawi"},
    {"id": "AMR-010", "name": "Dawali (Varicose Veins)", "icd11": "BD71", "system": "Vascular", "mizaj": "Saudawi"},
]

# Canonical Tadbeer Regimens
TADBEER_INDEX = [
    {"id": "TDB-001", "name": "Hijama (Wet / Dry Cupping)", "type": "Istifragh (Evacuation)", "indication": "Tanqiya-e-Dam, local stasis"},
    {"id": "TDB-002", "name": "Fasd (Venesection)", "type": "Istifragh (Evacuation)", "indication": "Ghalba-e-Dam, acute plethora"},
    {"id": "TDB-003", "name": "Dalak (Therapeutic Massage)", "type": "Tahleel / Tanweem", "indication": "Muscular spasm, fatigue, insomnia"},
    {"id": "TDB-004", "name": "Hammam (Therapeutic Bathing)", "type": "Tahleel / Tareeq", "indication": "Diaphoresis, Su-e-Mizaj Yabis"},
    {"id": "TDB-005", "name": "Natool (Irrigation / Pouring)", "type": "Taskeen / Tabreed", "indication": "Cephalic heat, localized inflammation"},
    {"id": "TDB-006", "name": "Huqna (Enema)", "type": "Istifragh", "indication": "Colonic evacuation, Qoolanj"},
]

# Navigation Shortcuts
NAV_SHORTCUTS = [
    {"id": "NAV-001", "title": "Clinical Digital Twin (12 Axes)", "subtitle": "Inspect multi-organ functional trajectory", "route": "digital_twin"},
    {"id": "NAV-002", "title": "Ambient Clinical Scribe", "subtitle": "Polyglot voice consultation & SOAP note synthesizer", "route": "ambient_scribe"},
    {"id": "NAV-003", "title": "Nuskha Nawisi Studio", "subtitle": "Formulation compiler with Mudabbar safety gates", "route": "nuskha"},
    {"id": "NAV-004", "title": "Ilaj bil-Tadbeer Regimens", "subtitle": "Regimenal therapy safety protocols & execution", "route": "tadbeer"},
    {"id": "NAV-005", "title": "UPI Pharmacopoeia Reference", "subtitle": "Single botanical monographs & Schedule E(1) rules", "route": "pharmacopoeia"},
]


class CommandSearchEngine:
    """Unified cross-domain search index for ZAYVORA Command Center (Cmd+K)."""

    @classmethod
    def search(cls, query: str, limit: int = 20) -> List[SearchResultItem]:
        q = query.strip().lower()
        if not q:
            # Return popular navigation shortcuts and top items
            results = []
            for n in NAV_SHORTCUTS:
                results.append(SearchResultItem(
                    id=n["id"],
                    category="navigation",
                    title=n["title"],
                    subtitle=n["subtitle"],
                    badge="Shortcut",
                    route=n["route"],
                ))
            return results

        results: List[SearchResultItem] = []

        # 1. Search Navigation
        for n in NAV_SHORTCUTS:
            if q in n["title"].lower() or q in n["subtitle"].lower():
                results.append(SearchResultItem(
                    id=n["id"],
                    category="navigation",
                    title=n["title"],
                    subtitle=n["subtitle"],
                    badge="Shortcut",
                    route=n["route"],
                ))

        # 2. Search Mufradat (UPI)
        for m in UPI_MUFRADAT_REGISTRY:
            drug_id = m.get("id", "")
            name_en = m.get("name", "")
            botanical = m.get("botanical_name", "")
            synonyms = " ".join(m.get("synonyms", []))
            mizaj_info = m.get("mizaj", {})
            mizaj_str = f"{mizaj_info.get('quality', '')} ({mizaj_info.get('temperament', '')})"
            sched_e1 = m.get("is_schedule_e1", False)

            match_score = 0
            if q in name_en.lower(): match_score += 3
            if q in botanical.lower(): match_score += 2
            if q in synonyms.lower(): match_score += 2
            if q in mizaj_str.lower(): match_score += 1

            if match_score > 0:
                results.append(SearchResultItem(
                    id=drug_id,
                    category="mufradat",
                    title=name_en,
                    subtitle=f"{botanical} • Mizaj: {mizaj_str}",
                    badge="Schedule E(1)" if sched_e1 else "UPI Mufrad",
                    route="pharmacopoeia",
                    metadata={"is_schedule_e1": sched_e1, "botanical": botanical},
                ))

        # 3. Search Murakkabat (NFUM)
        for f in NFUM_COMPOUND_REGISTRY:
            form_id = f.get("id", "")
            fname = f.get("name", "")
            urdu_f = f.get("urdu_name", "")
            cat = f.get("category", "")
            indication = f.get("classical_indication", "")
            sched_e1 = f.get("schedule_e1_warning", False)

            if q in fname.lower() or q in urdu_f or q in cat.lower() or q in indication.lower():
                results.append(SearchResultItem(
                    id=form_id,
                    category="murakkabat",
                    title=fname,
                    subtitle=f"{cat} • Indication: {indication[:40]}...",
                    badge="Contains E(1)" if sched_e1 else "NFUM Compound",
                    route="nuskha",
                    metadata={"contains_schedule_e1": sched_e1},
                ))

        # 4. Search Amraz & ICD-11
        for a in AMRAZ_INDEX:
            if q in a["name"].lower() or q in a["icd11"].lower() or q in a["system"].lower():
                results.append(SearchResultItem(
                    id=a["id"],
                    category="amraz",
                    title=a["name"],
                    subtitle=f"ICD-11: {a['icd11']} • System: {a['system']} • {a['mizaj']}",
                    badge=a["icd11"],
                    route="timeline",
                ))

        # 5. Search Tadbeer
        for t in TADBEER_INDEX:
            if q in t["name"].lower() or q in t["indication"].lower() or q in t["type"].lower():
                results.append(SearchResultItem(
                    id=t["id"],
                    category="tadbeer",
                    title=t["name"],
                    subtitle=f"{t['type']} • {t['indication']}",
                    badge="Tadbeer",
                    route="tadbeer",
                ))

        # Deduplicate and limit
        return results[:limit]
