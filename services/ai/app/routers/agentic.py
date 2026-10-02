"""
ZAYVORA AGENTIC CLINICAL AI™ — FastAPI Router
==============================================
Exposes endpoints for:
- Initiating orchestrated agentic workflows
- Clinician Approval Gate (Accept / Modify / Reject / Defer)
- Inspecting active workflow state machine
- Tool registry queries with R0 to R5 risk levels
- Agent observability & audit logging
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

from app.agentic.models import (
    ClinicianDecision,
    AgentRunRecord,
    ToolDeclaration,
)
from app.agentic.orchestrator import HakeemSahabOrchestrator
from app.agentic.tool_registry import ToolRegistry


router = APIRouter(prefix="/api/v1/agentic", tags=["Agentic Clinical AI"])


class WorkflowRunRequest(BaseModel):
    patient_context: Dict[str, Any] = Field(default_factory=dict)
    encounter_context: Dict[str, Any] = Field(default_factory=dict)
    proposed_action: Dict[str, Any] = Field(default_factory=dict)
    actor_id: str = "DOC-01"
    role: str = "DOCTOR"
    organization_id: str = "ORG-ZAYVORA-01"
    facility_id: str = "FACILITY-DELHI-01"


class ApprovalRequest(BaseModel):
    run_id: str
    decision: ClinicianDecision
    clinician_id: str = "DOC-01"
    clinician_role: str = "DOCTOR"
    clinician_notes: Optional[str] = None
    modified_prescription: Optional[Dict[str, Any]] = None


@router.post("/run", response_model=AgentRunRecord)
def run_workflow(req: WorkflowRunRequest):
    """
    Initiates an orchestrated clinical workflow through the 10-state machine.
    Halts automatically at the Human Approval Gate or if blocked by safety firewall.
    """
    try:
        record = HakeemSahabOrchestrator.start_clinical_encounter_workflow(
            patient_context=req.patient_context,
            encounter_context=req.encounter_context,
            proposed_action=req.proposed_action,
            actor_id=req.actor_id,
            role=req.role,
            organization_id=req.organization_id,
            facility_id=req.facility_id,
        )
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/approve", response_model=AgentRunRecord)
def approve_workflow(req: ApprovalRequest):
    """
    Human Approval Gate (§19 & §31).
    Doctor reviews draft nuskha and decides: Accept, Modify, Reject, or Defer.
    Applies SHA-256 HMAC 21 CFR Part 11 electronic signature upon acceptance.
    """
    try:
        record = HakeemSahabOrchestrator.clinician_submit_decision(
            run_id=req.run_id,
            decision=req.decision,
            clinician_id=req.clinician_id,
            clinician_role=req.clinician_role,
            clinician_notes=req.clinician_notes,
            modified_prescription=req.modified_prescription,
        )
        return record
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state/{run_id}", response_model=AgentRunRecord)
def get_workflow_state(run_id: str):
    """Inspects the state of an active or completed agentic workflow."""
    record = HakeemSahabOrchestrator.get_run(run_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")
    return record


@router.get("/tools", response_model=List[ToolDeclaration])
def list_controlled_tools():
    """Lists all tools in the controlled registry with their R0 to R5 risk tiers."""
    return ToolRegistry.list_tools()


@router.get("/audit/logs")
def get_audit_logs(limit: int = Query(50, ge=1, le=200)):
    """Retrieves immutable agent execution event logs for regulatory auditing."""
    return {"audit_events": HakeemSahabOrchestrator.get_audit_logs(limit=limit)}
