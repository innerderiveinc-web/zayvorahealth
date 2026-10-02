"""
ZAYVORA Health OS™ — Clinician Multi-Sign-Off & Legal Audit Engine
===================================================================
Implements Phase 10 (Clinician Review & Multi-Disciplinary Governance).

A drug monograph or compound prescription CANNOT achieve autonomous
AI authorization without all mandatory digital sign-offs:
  1. Source Reviewer (Classical Text Transcription & Page Citations)
  2. Pharmacognosist (Botanical Identity, Microscopy, Adulterants)
  3. Toxicologist / Safety Officer (Schedule E(1), Shodhana, Ceilings)
  4. Regulatory Officer (UPI, NFUM, PCIM&H compliance)
  5. Chief Senior Hakeem (Clinical Authority Sign-off)

Generates tamper-evident SHA-256 cryptographic audit certificates.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
import hashlib
import json
from datetime import datetime, timezone

SIGN_OFF_ROLES = [
    "CLASSICAL_SOURCE_SCHOLAR",
    "PHARMACOGNOSIST_BOTANIST",
    "TOXICOLOGIST_SAFETY_OFFICER",
    "REGULATORY_COMPLIANCE_OFFICER",
    "CHIEF_UNANI_CLINICIAN",
]

# In-memory certificate ledger (replaces with DB table in production)
_SIGN_OFF_LEDGER: Dict[str, Dict[str, Any]] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _generate_audit_hash(payload: Dict[str, Any]) -> str:
    """Generates deterministic SHA-256 hash for legal tamper-evidence."""
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class ClinicalMultiSignoffEngine:
    """
    Multi-Disciplinary Sign-Off & Audit Certificate Generator.
    """

    @classmethod
    def record_expert_signoff(
        cls,
        target_id: str,
        target_type: str,
        role: str,
        expert_name: str,
        expert_credentials: str,
        comments: str = "",
        passed: bool = True
    ) -> Dict[str, Any]:
        """
        Records an individual expert sign-off for a drug or nuskha.
        """
        tid = target_id.strip().upper()
        r_upper = role.strip().upper()

        if r_upper not in SIGN_OFF_ROLES:
            return {
                "success": False,
                "error": f"Invalid role '{role}'. Must be one of: {', '.join(SIGN_OFF_ROLES)}"
            }

        if not expert_name:
            return {"success": False, "error": "expert_name is mandatory."}

        record = _SIGN_OFF_LEDGER.setdefault(tid, {
            "target_id": tid,
            "target_type": target_type,
            "signoffs": {},
            "is_fully_certified": False,
            "certificate_hash": None,
            "created_at": _now_iso()
        })

        signoff_entry = {
            "role": r_upper,
            "expert_name": expert_name,
            "expert_credentials": expert_credentials,
            "timestamp": _now_iso(),
            "comments": comments,
            "passed": passed
        }
        record["signoffs"][r_upper] = signoff_entry

        # Check if all 5 roles have signed off and passed
        all_passed = (
            len(record["signoffs"]) == len(SIGN_OFF_ROLES)
            and all(s["passed"] for s in record["signoffs"].values())
        )

        record["is_fully_certified"] = all_passed
        if all_passed:
            record["certified_at"] = _now_iso()
            record["certificate_hash"] = _generate_audit_hash(record)

        return {
            "success": True,
            "target_id": tid,
            "role": r_upper,
            "expert_name": expert_name,
            "completed_signoffs": len(record["signoffs"]),
            "required_signoffs": len(SIGN_OFF_ROLES),
            "is_fully_certified": all_passed,
            "certificate_hash": record["certificate_hash"],
            "message": "Sign-off recorded successfully."
        }

    @classmethod
    def get_audit_certificate(cls, target_id: str) -> Dict[str, Any]:
        """
        Returns full legal audit certificate and sign-off status.
        """
        tid = target_id.strip().upper()
        record = _SIGN_OFF_LEDGER.get(tid)

        if not record:
            return {
                "target_id": tid,
                "certified": False,
                "status": "NO_SIGNOFF_RECORD_FOUND",
                "completed_roles": [],
                "pending_roles": SIGN_OFF_ROLES,
                "certificate_hash": None,
                "governance_rule": "AI prescription strictly prohibited without full 5-role clinical certification."
            }

        signed_roles = set(record["signoffs"].keys())
        pending = [r for r in SIGN_OFF_ROLES if r not in signed_roles]

        return {
            "target_id": tid,
            "target_type": record["target_type"],
            "certified": record["is_fully_certified"],
            "completed_signoff_count": len(signed_roles),
            "total_required": len(SIGN_OFF_ROLES),
            "completed_roles": list(signed_roles),
            "pending_roles": pending,
            "signoffs_detail": record["signoffs"],
            "certificate_hash": record["certificate_hash"],
            "certified_at": record.get("certified_at"),
            "legal_authority": (
                "ZAYVORA Health OS™ Certified Clinical Sign-off — Validated under Drugs & Cosmetics Act 1940 / CCRUM Research Standards."
                if record["is_fully_certified"]
                else "INCOMPLETE CERTIFICATION: AI autonomy blocked."
            )
        }
