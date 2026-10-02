"""
ZAYVORA Health OS™ — 12-Gate Evidence Pipeline Status Tracker Engine
=====================================================================
Source: ZAYVORA Mufradat 250 Validation-Controlled Master v2
        (12-Gate Evidence Pipeline — Gates 1 through 12)

The 12-Gate Pipeline governs the clinical promotion pathway for all
250 Mufradat. A drug may NOT be promoted beyond its current gate
without documented expert sign-off at the preceding gate.

Gates:
  Gate 01 — Classical Textual Evidence (Kutub-e-Unani)
  Gate 02 — Botanical / Mineralogical Identity Verification
  Gate 03 — Quality Control & Pharmacognosy (IS/API/AFI compliance)
  Gate 04 — Toxicological Safety Profile (LD50, sub-acute, chronic)
  Gate 05 — Standardized Phytochemical Profiling (HPLC/TLC marker)
  Gate 06 — In-vitro Pharmacological Screening (cell lines, enzyme)
  Gate 07 — In-vivo Animal Efficacy Studies (GLP / CPCSEA-compliant)
  Gate 08 — Clinical Phase I — Safety (Healthy Volunteers, Dose Escalation)
  Gate 09 — Clinical Phase II — Efficacy (Pilot RCT, n>=30)
  Gate 10 — Clinical Phase III — Confirmatory (Multi-Center RCT)
  Gate 11 — Regulatory Dossier Submission (CDSCO / PCIM&H / AYUSH)
  Gate 12 — Post-Market Surveillance & Pharmacovigilance
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

GATE_DEFINITIONS: Dict[int, Dict[str, str]] = {
    1:  {"name": "Classical Textual Evidence",          "authority": "Classical Scholar / Muallif",       "abbrev": "G01-CTE"},
    2:  {"name": "Botanical / Mineralogical Identity",  "authority": "Botanist / Pharmacognosist",         "abbrev": "G02-BMI"},
    3:  {"name": "Quality Control & Pharmacognosy",     "authority": "QC Lab / API/AFI Officer",           "abbrev": "G03-QCP"},
    4:  {"name": "Toxicological Safety Profile",        "authority": "Toxicologist / CPCSEA Lab",          "abbrev": "G04-TSP"},
    5:  {"name": "Phytochemical Profiling",             "authority": "Analytical Chemist / HPLC Lab",      "abbrev": "G05-PCH"},
    6:  {"name": "In-vitro Pharmacological Screening",  "authority": "Pharmacologist / Cell Biology Lab",  "abbrev": "G06-IVS"},
    7:  {"name": "In-vivo Animal Efficacy",             "authority": "GLP Lab / CPCSEA Committee",         "abbrev": "G07-IVV"},
    8:  {"name": "Clinical Phase I Safety",             "authority": "CDSCO IEC / Principal Investigator", "abbrev": "G08-CP1"},
    9:  {"name": "Clinical Phase II Efficacy",          "authority": "CDSCO / Site Investigator",          "abbrev": "G09-CP2"},
    10: {"name": "Clinical Phase III Confirmatory",     "authority": "CDSCO / Multi-Center PI",            "abbrev": "G10-CP3"},
    11: {"name": "Regulatory Dossier Submission",       "authority": "CDSCO / PCIM and H / AYUSH",        "abbrev": "G11-REG"},
    12: {"name": "Post-Market Surveillance",            "authority": "ZAYVORA PV Cell / MvP Unit",         "abbrev": "G12-PMS"},
}

import os
import sqlite3
import hashlib

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
_DB_PATH = os.path.join(_BASE_DIR, "database", "zayvora_live.db")

def _get_gates_db():
    if os.path.exists(_DB_PATH):
        try:
            conn = sqlite3.connect(_DB_PATH)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception:
            return None
    return None

_GATE_STATUS_STORE: Dict[str, Dict[int, Dict[str, Any]]] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class TwelveGateTrackerEngine:
    """12-Gate Evidence Pipeline Tracker for ZAYVORA Mufradat 250 with persistent SQL backing."""

    @classmethod
    def get_gate_status(cls, zmf_id: str) -> Dict[str, Any]:
        zmf = zmf_id.strip().upper()
        record = _GATE_STATUS_STORE.setdefault(zmf, {})

        conn = _get_gates_db()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute("SELECT gate_number, signed_by, signed_at, notes FROM mufradat_twelve_gates WHERE zmf_id = ?", (zmf,))
                    for r in cur.fetchall():
                        g_num = r["gate_number"]
                        if g_num not in record:
                            record[g_num] = {
                                "signed_by": r["signed_by"],
                                "signed_at": r["signed_at"],
                                "notes": r["notes"],
                                "gate_number": g_num
                            }
            except Exception:
                pass
        gates_detail = []
        highest_completed = 0
        for gate_num in range(1, 13):
            gdef = GATE_DEFINITIONS[gate_num]
            signoff = record.get(gate_num)
            if signoff:
                highest_completed = gate_num
                status = "COMPLETED"
            elif gate_num == max(record.keys(), default=0) + 1:
                status = "NEXT"
            else:
                status = "PENDING"
            gates_detail.append({
                "gate_number": gate_num,
                "gate_abbrev": gdef["abbrev"],
                "gate_name": gdef["name"],
                "required_authority": gdef["authority"],
                "status": status,
                "signoff_by": signoff.get("signed_by") if signoff else None,
                "signoff_at": signoff.get("signed_at") if signoff else None,
                "notes": signoff.get("notes") if signoff else None,
            })
        return {
            "zmf_id": zmf,
            "current_gate_completed": highest_completed,
            "next_gate_required": min(highest_completed + 1, 12) if highest_completed < 12 else None,
            "pipeline_complete": highest_completed == 12,
            "clinical_promotion_allowed": highest_completed >= 10,
            "ai_internal_allowed": highest_completed >= 1,
            "gates": gates_detail,
            "governance_note": (
                "Gates 1-7 establish pre-clinical safety. Gates 8-10 = human clinical evidence. "
                "Gate 11 = regulatory approval. Gate 12 = pharmacovigilance. "
                "AI clinical promotion requires Gate 10+ completion."
            )
        }

    @classmethod
    def record_gate_signoff(
        cls,
        zmf_id: str,
        gate_number: int,
        signed_by: str,
        notes: str = "",
        override_incomplete_prior: bool = False
    ) -> Dict[str, Any]:
        zmf = zmf_id.strip().upper()
        if gate_number < 1 or gate_number > 12:
            return {"success": False, "error": f"Invalid gate number {gate_number}. Must be 1-12."}
        if not signed_by or not signed_by.strip():
            return {"success": False, "error": "signed_by must be provided."}
        record = _GATE_STATUS_STORE.setdefault(zmf, {})
        if gate_number > 1 and (gate_number - 1) not in record and not override_incomplete_prior:
            prev_gate = GATE_DEFINITIONS[gate_number - 1]
            return {
                "success": False,
                "error": (
                    f"Cannot sign off Gate {gate_number} — Gate {gate_number - 1} "
                    f"('{prev_gate['name']}') has not been completed. "
                    f"Set override_incomplete_prior=true with documented justification."
                )
            }
        record[gate_number] = {
            "signed_by": signed_by.strip(),
            "signed_at": _now_iso(),
            "notes": notes.strip(),
            "gate_number": gate_number,
        }

        conn = _get_gates_db()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute("""
                    INSERT OR REPLACE INTO mufradat_twelve_gates 
                    (id, zmf_id, gate_number, gate_name, signed_by, signed_at, notes, evidence_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        f"GTRK-{zmf}-{gate_number}",
                        zmf,
                        gate_number,
                        GATE_DEFINITIONS[gate_number]["name"],
                        signed_by.strip(),
                        record[gate_number]["signed_at"],
                        notes.strip(),
                        hashlib.sha256(f"{zmf}:{gate_number}:{signed_by}:{notes}".encode()).hexdigest()
                    ))
            except Exception:
                pass

        highest = max(record.keys()) if record else 0
        return {
            "success": True,
            "zmf_id": zmf,
            "gate_number": gate_number,
            "gate_name": GATE_DEFINITIONS[gate_number]["name"],
            "signed_by": signed_by.strip(),
            "signed_at": record[gate_number]["signed_at"],
            "highest_gate_completed": highest,
            "clinical_promotion_allowed": highest >= 10,
            "pipeline_complete": highest == 12,
            "message": f"Gate {gate_number} sign-off recorded for {zmf}."
        }

    @classmethod
    def get_dashboard_summary(cls) -> Dict[str, Any]:
        conn = _get_gates_db()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute("SELECT zmf_id, gate_number, signed_by, signed_at, notes FROM mufradat_twelve_gates")
                    for r in cur.fetchall():
                        rec = _GATE_STATUS_STORE.setdefault(r["zmf_id"], {})
                        rec[r["gate_number"]] = {
                            "signed_by": r["signed_by"],
                            "signed_at": r["signed_at"],
                            "notes": r["notes"],
                            "gate_number": r["gate_number"]
                        }
            except Exception:
                pass

        total_tracked = len(_GATE_STATUS_STORE)
        gate_distribution: Dict[int, int] = {i: 0 for i in range(0, 13)}
        clinical_promotion_ready = []
        pipeline_complete = []
        for zmf_id, record in _GATE_STATUS_STORE.items():
            highest = max(record.keys()) if record else 0
            gate_distribution[highest] = gate_distribution.get(highest, 0) + 1
            if highest >= 10:
                clinical_promotion_ready.append(zmf_id)
            if highest == 12:
                pipeline_complete.append(zmf_id)
        return {
            "total_mufradat_tracked": total_tracked,
            "total_mufradat_catalog": 250,
            "untracked_mufradat": 250 - total_tracked,
            "gate_distribution": gate_distribution,
            "clinical_promotion_ready_count": len(clinical_promotion_ready),
            "clinical_promotion_ready_zmf_ids": clinical_promotion_ready,
            "pipeline_complete_count": len(pipeline_complete),
            "pipeline_complete_zmf_ids": pipeline_complete,
            "governance_summary": (
                f"{total_tracked}/250 Mufradat have any gate record. "
                f"{250 - total_tracked} remain at Gate 0 (untracked / pre-submission). "
                f"{len(clinical_promotion_ready)} eligible for clinical AI promotion (Gate 10+). "
                f"{len(pipeline_complete)} have completed all 12 gates."
            )
        }

    @classmethod
    def get_all_gate_definitions(cls) -> List[Dict[str, Any]]:
        return [
            {
                "gate_number": num,
                "gate_abbrev": gdef["abbrev"],
                "gate_name": gdef["name"],
                "required_authority": gdef["authority"],
            }
            for num, gdef in sorted(GATE_DEFINITIONS.items())
        ]
