"""
ZAYVORA Health OS™ — Hakeem Sahab AI Copilot Permission Guard
============================================================
Reference:
  - Blueprint §11 (Hakeem Sahab AI Clinician Copilot)
  - Blueprint §41 (Hakeem Sahab Tool Permission Model)
  - Doctrine: Autonomous Diagnosis != Autonomous Prescription != Autonomous Treatment Decision
  - Hard Guardrails: AI cannot finalize prescriptions, dispense drugs, change approved nuskhas, or alter safety rules.
"""

from typing import Dict, Any, List, Optional
import sys
import os

# ── Mufradat 250 Hard-Block Integration ──────────────────────────────────────
try:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../..")))
    from services.knowledge.app.data.mufradat_250_registry import (
        is_high_risk_blocked,
        get_high_risk_28_registry,
    )
    _MUFRADAT_GUARD_AVAILABLE = True
except ImportError:
    _MUFRADAT_GUARD_AVAILABLE = False
    def is_high_risk_blocked(zmf_id: str) -> bool:
        return False
    def get_high_risk_28_registry() -> dict:
        return {}
# ─────────────────────────────────────────────────────────────────────────────


COPILOT_PERMISSIONS_TABLE: Dict[str, Dict[str, Any]] = {
    "read_patient_chart": {
        "ai_default": "ALLOWED",
        "clinician_override": True,
        "description": "Read authorized patient history, labs, observations, and previous encounters."
    },
    "retrieve_knowledge": {
        "ai_default": "ALLOWED",
        "clinician_override": True,
        "description": "Query approved Mufradat, Murakkabat, Organ-Axis monographs and literature."
    },
    "summarize_evidence": {
        "ai_default": "ALLOWED",
        "clinician_override": True,
        "description": "Synthesize clinical literature with explicit evidence tier (E0-E6) and citations."
    },
    "flag_safety_issue": {
        "ai_default": "ALLOWED",
        "clinician_override": True,
        "description": "Identify red flags, drug interactions, contraindications, and dosage violations."
    },
    "draft_questions": {
        "ai_default": "ALLOWED",
        "clinician_override": True,
        "description": "Suggest diagnostic follow-up questions for the consulting clinician."
    },
    "draft_plan": {
        "ai_default": "ALLOWED_DRAFT_ONLY",
        "clinician_override": True,
        "description": "Draft preliminary therapeutic options clearly labeled as non-binding suggestions."
    },
    "change_approved_nuskha": {
        "ai_default": "BLOCKED",
        "clinician_override": True,
        "description": "Modifying an approved patient prescription requires explicit clinician action."
    },
    "finalize_prescription": {
        "ai_default": "BLOCKED",
        "clinician_override": False,
        "description": "Legally restricted to registered human clinicians (BUMS/Ayush/MD)."
    },
    "dispense_medication": {
        "ai_default": "BLOCKED",
        "clinician_override": False,
        "description": "Physically and legally restricted to licensed pharmacy dispensing workflow."
    },
    "change_safety_rules": {
        "ai_default": "BLOCKED",
        "clinician_override": False,
        "description": "Restricted to Clinical Knowledge Governance Board release cycles."
    }
}


class CopilotPermissionGuard:
    """Enforces strict capability boundaries on AI copilot actions."""

    @classmethod
    def evaluate_permission(
        cls,
        action_name: str,
        actor_role: str = "HAKEEM_SAHAB_AI",
        is_clinician_present: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluates whether an intended action is permitted under the ZAYVORA
        Hakeem Sahab Tool Permission Model.
        """
        action = action_name.lower().strip()
        role = actor_role.upper().strip()

        if action not in COPILOT_PERMISSIONS_TABLE:
            return {
                "allowed": False,
                "action": action,
                "status": "BLOCKED",
                "reason": f"Unknown or unmapped action '{action}'. All autonomous actions default to BLOCKED.",
                "legal_authority": "GOVERNANCE_ZERO_TRUST"
            }

        spec = COPILOT_PERMISSIONS_TABLE[action]
        ai_default = spec["ai_default"]

        # Human Clinicians are never blocked by the AI permission table
        if role in ["DOCTOR", "HAKEEM", "CLINICIAN", "SUPER_ADMIN"]:
            return {
                "allowed": True,
                "action": action,
                "status": "ALLOWED_CLINICIAN_AUTHORITY",
                "reason": f"Action allowed under qualified clinician authority ({role}).",
                "legal_authority": "REGISTERED_CLINICIAN"
            }

        # Handle AI Copilot roles
        if ai_default == "ALLOWED":
            return {
                "allowed": True,
                "action": action,
                "status": "ALLOWED",
                "reason": spec["description"],
                "legal_authority": "COPILOT_SAFE_RETRIEVAL"
            }
        elif ai_default == "ALLOWED_DRAFT_ONLY":
            return {
                "allowed": True,
                "action": action,
                "status": "ALLOWED_DRAFT_ONLY",
                "reason": "Permitted to create draft proposals only; cannot execute or bind care.",
                "legal_authority": "COPILOT_DRAFT_MODE"
            }
        else: # BLOCKED
            return {
                "allowed": False,
                "action": action,
                "status": "BLOCKED",
                "reason": f"HARD STOP: Action '{action}' is strictly prohibited for AI. {spec['description']}",
                "legal_authority": "STATUTORY_RULE_161_DOCTRINE_INVARIANT"
            }

    @classmethod
    def get_permission_matrix(cls) -> Dict[str, Any]:
        """Returns the full tool permissions specification."""
        return COPILOT_PERMISSIONS_TABLE

    @classmethod
    def evaluate_ingredient_access(
        cls,
        zmf_id: str,
        ingredient_name: str = "",
        actor_role: str = "HAKEEM_SAHAB_AI",
        context: str = "retrieve_knowledge"
    ) -> Dict[str, Any]:
        """
        ZMF Mufradat 250 Hard-Block Gate for AI Copilot.

        Evaluates whether the AI copilot may access, retrieve, draft, or
        reference information about a specific Mufrad identified by ZMF ID.

        HIGH_RISK_28 substances are HARD BLOCKED for all AI actions —
        the AI cannot suggest, draft, retrieve clinical data, or reference
        these substances without explicit clinician-initiated override.

        Args:
            zmf_id:          The ZMF identifier (e.g. "ZMF-002").
            ingredient_name: Human-readable name (for error messages).
            actor_role:      Role of the requesting actor.
            context:         The action context (e.g. "retrieve_knowledge").

        Returns:
            Dict with keys: allowed, zmf_id, status, reason, legal_authority
        """
        zmf_upper = zmf_id.strip().upper()
        display = ingredient_name or zmf_upper

        # Human clinicians bypass the AI ingredient gate
        if actor_role.upper() in ["DOCTOR", "HAKEEM", "CLINICIAN", "SUPER_ADMIN"]:
            return {
                "allowed": True,
                "zmf_id": zmf_upper,
                "status": "ALLOWED_CLINICIAN_AUTHORITY",
                "reason": f"Clinician ({actor_role}) access granted to {display}.",
                "legal_authority": "REGISTERED_CLINICIAN"
            }

        # ZMF Hard-Block check
        if _MUFRADAT_GUARD_AVAILABLE and is_high_risk_blocked(zmf_upper):
            hr_registry = get_high_risk_28_registry()
            rec = hr_registry.get(zmf_upper, {})
            return {
                "allowed": False,
                "zmf_id": zmf_upper,
                "status": "HARD_BLOCKED_ZMF_HIGH_RISK_28",
                "reason": (
                    f"🚫 AI HARD BLOCK: '{display}' [{zmf_upper}] is in the HIGH_RISK_28 registry. "
                    f"Category: {rec.get('category', 'Restricted Substance')}. "
                    f"Primary toxin: {rec.get('primary_toxin', 'N/A')}. "
                    f"Restriction: {rec.get('restriction', 'AI_BLOCKED — specialist sign-off required.')} "
                    f"The AI copilot may NOT retrieve, draft, or reference this substance. "
                    f"Only a registered clinician with explicit specialist authority may proceed."
                ),
                "legal_authority": "MUFRADAT_250_REGISTRY_HARD_BLOCK"
            }

        return {
            "allowed": True,
            "zmf_id": zmf_upper,
            "status": "ALLOWED_RESEARCH_ONLY",
            "reason": f"'{display}' is not in HIGH_RISK_28 registry. AI access permitted for research/draft context only.",
            "legal_authority": "COPILOT_RESEARCH_ONLY"
        }

