"""
ZAYVORA Health OS™ — Nuskha Approval Lifecycle State Machine
===========================================================
Reference:
  - Blueprint §40 (Nuskha Approval State Machine)
  - Lifecycle: DRAFT -> SAFETY CHECK -> CLINICIAN REVIEW -> APPROVED -> DISPENSED -> MONITORING -> COMPLETED
  - Branch States: REJECTED, MODIFIED, REFERRED
  - Core Rule: Every transition stores actor, role, timestamp, reason, previous_version, new_version, evidence/safety references.
  - Invariants:
      1. AI Copilot can NEVER approve prescriptions or dispense medications.
      2. SUPER_ADMIN / IT Administrator is STRICTLY barred from medical prescribing.
      3. Only verified active clinicians (CCIM/NCISM registered) can transition to APPROVED.
      4. Safety BLOCK or UNKNOWN hard-stops approval (fails closed).
      5. Safety CAUTION requires mandatory signed clinician acknowledgement rationale.
      6. Prescriptions generate immutable cryptographic digital signatures (SHA-256).
"""

from __future__ import annotations

import datetime
import hashlib
import json
import uuid
from typing import Any, Dict, List, Optional


class UnverifiedClinicianException(Exception):
    """Raised when an actor without verified active clinician credentials attempts approval."""
    pass


class SafetyBlockException(Exception):
    """Raised when an attempt is made to approve a prescription with safety status BLOCK."""
    pass


class SafetyIncompleteException(Exception):
    """Raised when an attempt is made to approve a prescription with UNKNOWN safety status."""
    pass


class MissingClinicianRationaleException(Exception):
    """Raised when safety status is CAUTION but clinician signed justification is missing."""
    pass


class AdministrativePrescriptionForbiddenException(Exception):
    """Raised when an administrative or IT role attempts to prescribe or approve medication."""
    pass


# Valid Nuskha Lifecycle States
NUSKHA_STATES = [
    "DRAFT",
    "SAFETY_CHECK",
    "CLINICIAN_REVIEW",
    "APPROVED",
    "DISPENSED",
    "MONITORING",
    "COMPLETED",
    "REJECTED",
    "MODIFIED",
    "REFERRED"
]

# State transition matrix
PERMITTED_NUSKHA_TRANSITIONS = {
    "DRAFT": ["SAFETY_CHECK", "REJECTED"],
    "SAFETY_CHECK": ["CLINICIAN_REVIEW", "REJECTED"],
    "CLINICIAN_REVIEW": ["APPROVED", "MODIFIED", "REJECTED", "REFERRED"],
    "APPROVED": ["DISPENSED", "MODIFIED", "REJECTED"],
    "DISPENSED": ["MONITORING"],
    "MONITORING": ["COMPLETED", "MODIFIED", "REFERRED"],
    "MODIFIED": ["DRAFT", "SAFETY_CHECK"],
    "REJECTED": ["DRAFT"],
    "REFERRED": ["MONITORING", "COMPLETED"],
    "COMPLETED": []
}

# Strict role permissions per transition target:
# SUPER_ADMIN is an IT/administrative role and is STRICTLY BARRED from APPROVED and DISPENSED.
TARGET_STATE_ROLE_GATES = {
    "APPROVED": ["DOCTOR", "HAKEEM", "CLINICIAN"],
    "DISPENSED": ["PHARMACIST", "DISPENSARY_OPERATOR"],
    "CLINICIAN_REVIEW": ["DOCTOR", "HAKEEM", "CLINICIAN", "SYSTEM", "SUPER_ADMIN"],
    "COMPLETED": ["DOCTOR", "HAKEEM", "CLINICIAN"],
    "REFERRED": ["DOCTOR", "HAKEEM", "CLINICIAN", "SUPER_ADMIN"]
}

# Strictly forbidden actors for clinical execution
FORBIDDEN_ACTOR_ROLES = ["AI", "AI_COPILOT", "HAKEEM_SAHAB_AI", "BOT", "UNAUTHENTICATED"]


class NuskhaStateMachine:
    """Manages the state transitions and immutable audit events for patient prescriptions."""

    @classmethod
    def transition(
        cls,
        nuskha_id: str,
        current_state: str,
        target_state: str,
        actor_id: str,
        actor_role: str,
        reason: str,
        current_version: int = 1,
        evidence_refs: Optional[List[str]] = None,
        safety_refs: Optional[List[str]] = None,
        safety_status: Optional[str] = "CLEAR",
        safety_score: Optional[float] = None,
        clinician_acknowledgement_rationale: Optional[str] = None,
        target_axis: Optional[str] = None,
        prescription_payload: Optional[Dict[str, Any]] = None,
        raise_on_error: bool = False
    ) -> Dict[str, Any]:
        """
        Executes a formal state transition on a Nuskha with role validation,
        statutory clinician verification, deterministic safety hard-gating,
        and immutable SHA-256 audit logging.
        """
        curr = current_state.upper()
        tgt = target_state.upper()
        role = actor_role.upper()

        # Check state validity
        if curr not in NUSKHA_STATES:
            err = f"Invalid current state '{curr}'"
            return {"success": False, "error": err, "code": "INVALID_CURRENT_STATE"}
        if tgt not in NUSKHA_STATES:
            err = f"Invalid target state '{tgt}'"
            return {"success": False, "error": err, "code": "INVALID_TARGET_STATE"}

        # Invariant 1: AI cannot transition to clinical execution states
        if role in FORBIDDEN_ACTOR_ROLES:
            if tgt in ["APPROVED", "DISPENSED", "COMPLETED"]:
                err = f"Security Violation: Actor role '{role}' is legally and architecturally barred from setting state to '{tgt}'. Clinician approval is mandatory."
                return {
                    "success": False,
                    "error": err,
                    "code": "AI_PRESCRIPTION_AUTHORITY_VIOLATION"
                }

        # Check transition legality
        allowed = PERMITTED_NUSKHA_TRANSITIONS.get(curr, [])
        if tgt not in allowed:
            err = f"Illegal state transition from '{curr}' to '{tgt}'. Permitted next states: {allowed}"
            return {
                "success": False,
                "error": err,
                "code": "ILLEGAL_STATE_TRANSITION"
            }

        # Check role permission for target state
        required_roles = TARGET_STATE_ROLE_GATES.get(tgt)
        if required_roles and role not in required_roles:
            err = f"Access Denied: Role '{role}' does not have authority to transition Nuskha to '{tgt}'. Required roles: {required_roles}"
            if role in ["SUPER_ADMIN", "ADMIN"] and tgt in ["APPROVED", "DISPENSED"]:
                err = f"Clinical Safety Violation: Administrative role '{role}' cannot prescribe, approve, or dispense medications. Licensed clinician signature required."
                if raise_on_error:
                    raise AdministrativePrescriptionForbiddenException(err)
            return {
                "success": False,
                "error": err,
                "code": "INSUFFICIENT_ROLE_AUTHORITY"
            }

        # Clinical Approval Hard-Gating (when transitioning to APPROVED)
        verified_clinician_info: Dict[str, Any] = {}
        if tgt == "APPROVED":
            # 1. Deterministic Safety Hard-Gating
            norm_safety = (safety_status or "CLEAR").upper()
            if norm_safety == "BLOCK":
                err = "Safety Hard-Gating Violation: Prescription contains BLOCK-level contraindication or critical toxicity. Clinical approval is prohibited."
                if raise_on_error:
                    raise SafetyBlockException(err)
                return {"success": False, "error": err, "code": "SAFETY_BLOCK_CONTRAINDICATION"}

            if norm_safety == "UNKNOWN":
                err = "Safety Hard-Gating Violation: Prescription safety evaluation is UNKNOWN. System fails closed."
                if raise_on_error:
                    raise SafetyIncompleteException(err)
                return {"success": False, "error": err, "code": "SAFETY_EVALUATION_INCOMPLETE"}

            if norm_safety == "CAUTION":
                if not clinician_acknowledgement_rationale or not clinician_acknowledgement_rationale.strip():
                    err = "Prescription has safety CAUTION; signed clinician justification rationale is mandatory."
                    if raise_on_error:
                        raise MissingClinicianRationaleException(err)
                    return {"success": False, "error": err, "code": "MISSING_CLINICIAN_RATIONALE"}

            # 2. Statutory Clinician Credential Verification
            try:
                from services.identity.app.core.clinician_registry_service import ClinicianRegistryService
                clinician_res = ClinicianRegistryService.verify_clinician(actor_id, target_axis)
                if not clinician_res.get("verified"):
                    err = f"Statutory Credential Violation: {clinician_res.get('error')}"
                    if raise_on_error:
                        raise UnverifiedClinicianException(err)
                    return {
                        "success": False,
                        "error": err,
                        "code": clinician_res.get("code", "CLINICIAN_NOT_VERIFIED")
                    }
                verified_clinician_info = clinician_res
            except Exception as e:
                if raise_on_error:
                    raise UnverifiedClinicianException(f"Clinician registry service error: {str(e)}")
                return {
                    "success": False,
                    "error": f"Clinician verification error: {str(e)}",
                    "code": "CLINICIAN_VERIFICATION_FAILED"
                }

        # Calculate version increment
        new_version = current_version + 1 if tgt in ["APPROVED", "MODIFIED"] else current_version

        # Cryptographic Digital Signature for Prescription
        sig_basis = f"{nuskha_id}:{tgt}:{new_version}:{actor_id}:{reason}:{clinician_acknowledgement_rationale or ''}"
        if prescription_payload:
            sig_basis += ":" + json.dumps(prescription_payload, sort_keys=True)
        digital_sig = hashlib.sha256(sig_basis.encode("utf-8")).hexdigest()

        # Build immutable audit event
        audit_event = {
            "event_id": f"AUD-NSK-{uuid.uuid4().hex[:10].upper()}",
            "nuskha_id": nuskha_id,
            "previous_state": curr,
            "new_state": tgt,
            "previous_version": current_version,
            "new_version": new_version,
            "actor_id": actor_id,
            "actor_role": role,
            "reason": reason,
            "evidence_refs": evidence_refs or [],
            "safety_refs": safety_refs or [],
            "safety_status": safety_status,
            "clinician_acknowledgement_rationale": clinician_acknowledgement_rationale,
            "verified_clinician_id": verified_clinician_info.get("clinician_id"),
            "registration_number": verified_clinician_info.get("registration_number"),
            "digital_signature_sha256": digital_sig,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }

        return {
            "success": True,
            "nuskha_id": nuskha_id,
            "current_state": tgt,
            "version": new_version,
            "digital_signature": digital_sig,
            "verified_clinician": verified_clinician_info,
            "audit_event": audit_event
        }
