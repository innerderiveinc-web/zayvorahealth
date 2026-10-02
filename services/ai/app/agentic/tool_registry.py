"""
ZAYVORA AGENTIC CLINICAL AI™ — Controlled Tool Registry
========================================================
Implements Section 17 & 18:
- Controlled tool registration with explicit risk tiers (R0 to R5).
- Role-based authorization & data scoping.
- Prevention of autonomous privilege escalation.
"""

from typing import Dict, Any, List, Optional, Callable
from app.agentic.models import ToolDeclaration, RiskLevel


class ToolSecurityViolation(Exception):
    """Raised when an agent or user attempts an unauthorized or unapproved tool execution."""
    pass


class ToolRegistry:
    """Central registry of all authorized tools usable by agents in the clinical runtime."""

    _tools: Dict[str, ToolDeclaration] = {}
    _handlers: Dict[str, Callable] = {}

    @classmethod
    def register_tool(cls, declaration: ToolDeclaration, handler: Optional[Callable] = None):
        cls._tools[declaration.tool_id] = declaration
        if handler:
            cls._handlers[declaration.tool_id] = handler

    @classmethod
    def get_tool(cls, tool_id: str) -> Optional[ToolDeclaration]:
        return cls._tools.get(tool_id)

    @classmethod
    def list_tools(cls) -> List[ToolDeclaration]:
        return list(cls._tools.values())

    @classmethod
    def authorize_execution(
        cls,
        tool_id: str,
        actor_role: str,
        is_autonomous_ai: bool = True,
        is_clinician_approved: bool = False,
    ) -> ToolDeclaration:
        """
        Validates authorization boundaries before any tool is executed (§18).
        """
        tool = cls._tools.get(tool_id)
        if not tool:
            raise ToolSecurityViolation(f"Unknown tool ID '{tool_id}' is not registered in ZAYVORA Tool Registry.")

        # Check role permissions
        if "*" not in tool.allowed_roles and actor_role not in tool.allowed_roles:
            raise ToolSecurityViolation(
                f"Role '{actor_role}' is not authorized to invoke tool '{tool_id}'. Allowed roles: {tool.allowed_roles}"
            )

        # Invariant: Autonomous AI can NEVER execute R4 (High-Impact Clinical) or R5 (Privileged) tools
        if is_autonomous_ai and tool.risk_level in [RiskLevel.R4_HIGH_IMPACT_CLINICAL, RiskLevel.R5_PRIVILEGED_SYSTEM]:
            raise ToolSecurityViolation(
                f"Autonomous AI is strictly prohibited from executing {tool.risk_level.value} tool '{tool_id}'. "
                "This action requires explicit human clinician/admin execution."
            )

        # Invariant: Tools requiring approval cannot execute without verified clinician sign-off
        if tool.approval_required and not is_clinician_approved:
            raise ToolSecurityViolation(
                f"Tool '{tool_id}' requires explicit clinician approval before execution. "
                "Action held at Human Approval Gate."
            )

        return tool


# ── Canonical System Tool Registration ────────────────────────────────────────

CANONICAL_TOOLS = [
    # R0 — Informational
    ToolDeclaration(
        tool_id="Appointment.findSlots",
        description="Query OPD slot availability and clinic schedule.",
        required_permission="appointment:read",
        allowed_roles=["PATIENT", "DOCTOR", "STAFF", "ADMIN", "AI_AGENT"],
        data_scope="FACILITY_SCHEDULE",
        risk_level=RiskLevel.R0_INFORMATIONAL,
        approval_required=False,
    ),
    ToolDeclaration(
        tool_id="Knowledge.search",
        description="Query canonical Mufradat, Murakkabat, and 12-volume integrative library.",
        required_permission="knowledge:read",
        allowed_roles=["DOCTOR", "RESEARCHER", "STAFF", "AI_AGENT"],
        data_scope="PUBLIC_KNOWLEDGE",
        risk_level=RiskLevel.R0_INFORMATIONAL,
        approval_required=False,
    ),
    ToolDeclaration(
        tool_id="Evidence.search",
        description="Surface pharmacological trials, safety records, and evidence tiers.",
        required_permission="evidence:read",
        allowed_roles=["DOCTOR", "RESEARCHER", "AI_AGENT"],
        data_scope="EVIDENCE_REPOSITORY",
        risk_level=RiskLevel.R0_INFORMATIONAL,
        approval_required=False,
    ),

    # R1 — Low-Risk Operational
    ToolDeclaration(
        tool_id="Appointment.create",
        description="Book a confirmed patient appointment token.",
        required_permission="appointment:write",
        allowed_roles=["PATIENT", "STAFF", "DOCTOR", "ADMIN", "AI_AGENT"],
        data_scope="APPOINTMENT_DATA",
        risk_level=RiskLevel.R1_LOW_RISK_OPERATIONAL,
        approval_required=False,
    ),
    ToolDeclaration(
        tool_id="Message.sendReminder",
        description="Queue an appointment or adherence reminder to patient with delivery confirmation.",
        required_permission="communication:send",
        allowed_roles=["STAFF", "DOCTOR", "AI_AGENT"],
        data_scope="COMMUNICATION_OUTBOX",
        risk_level=RiskLevel.R1_LOW_RISK_OPERATIONAL,
        approval_required=False,
    ),

    # R2 — Sensitive Patient Data
    ToolDeclaration(
        tool_id="PatientRecord.read",
        description="Read patient demographics, vitals, allergy profile, and historical encounters.",
        required_permission="patient:read",
        allowed_roles=["DOCTOR", "STAFF", "AI_AGENT"],
        data_scope="PATIENT_PHI",
        risk_level=RiskLevel.R2_SENSITIVE,
        approval_required=False,
    ),
    ToolDeclaration(
        tool_id="LabResult.read",
        description="Access diagnostic laboratory reports and biomarkers.",
        required_permission="lab:read",
        allowed_roles=["DOCTOR", "AI_AGENT"],
        data_scope="PATIENT_LABS",
        risk_level=RiskLevel.R2_SENSITIVE,
        approval_required=False,
    ),

    # R3 — Clinically Meaningful (AI Proposes / Drafts Only)
    ToolDeclaration(
        tool_id="Nuskha.createDraft",
        description="Draft a 4-tier structured Nuskha formulation for clinician review.",
        required_permission="clinical:draft",
        allowed_roles=["DOCTOR", "AI_AGENT"],
        data_scope="ENCOUNTER_DRAFT",
        risk_level=RiskLevel.R3_CLINICALLY_MEANINGFUL,
        approval_required=True,
    ),
    ToolDeclaration(
        tool_id="ClinicalConsideration.surface",
        description="Highlight potential differential diagnoses, red flags, or missing investigations.",
        required_permission="clinical:suggest",
        allowed_roles=["DOCTOR", "AI_AGENT"],
        data_scope="ENCOUNTER_ANALYSIS",
        risk_level=RiskLevel.R3_CLINICALLY_MEANINGFUL,
        approval_required=True,
    ),

    # R4 — High-Impact Clinical (Human Clinician Execution ONLY)
    ToolDeclaration(
        tool_id="Prescription.signAndLock",
        description="Finalize, digitally sign with SHA-256 HMAC (21 CFR Part 11), and lock prescription.",
        required_permission="clinical:prescribe",
        allowed_roles=["DOCTOR"],  # AI_AGENT explicitly excluded!
        data_scope="PERMANENT_HEALTH_RECORD",
        risk_level=RiskLevel.R4_HIGH_IMPACT_CLINICAL,
        approval_required=True,
    ),
    ToolDeclaration(
        tool_id="Pharmacy.dispenseMedication",
        description="Deduct inventory and dispense verified formulation to patient.",
        required_permission="pharmacy:dispense",
        allowed_roles=["PHARMACIST"],  # AI_AGENT explicitly excluded!
        data_scope="DISPENSARY_INVENTORY",
        risk_level=RiskLevel.R4_HIGH_IMPACT_CLINICAL,
        approval_required=True,
    ),

    # R5 — Privileged System Administration
    ToolDeclaration(
        tool_id="Governance.updateSafetyPolicy",
        description="Update institutional contraindication rules or Mudabbar detoxification requirements.",
        required_permission="admin:governance",
        allowed_roles=["ADMIN"],  # AI_AGENT explicitly excluded!
        data_scope="SYSTEM_POLICIES",
        risk_level=RiskLevel.R5_PRIVILEGED_SYSTEM,
        approval_required=True,
    ),
]

for t in CANONICAL_TOOLS:
    ToolRegistry.register_tool(t)
