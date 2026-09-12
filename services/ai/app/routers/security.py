"""
ZAYVORA HEALTH™ — Clinical AI Security & Guardrails Router
Provides endpoints for prompt sanitization, input validation, and defensive robustness audits.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from ..security.safety_guardrails import ClinicalPromptGuardrail
from ..security.robustness_suite import RobustnessEvaluator

router = APIRouter(prefix="/api/v1/security", tags=["AI Security & Guardrails"])


class PromptValidationRequest(BaseModel):
    prompt: str = Field(..., description="User or clinician prompt text to validate")


class OutputValidationRequest(BaseModel):
    response_text: str = Field(..., description="Copilot generated response text to verify")


@router.post("/guardrail/validate-input", summary="Validate input prompt against clinical AI guardrails")
async def validate_input(payload: PromptValidationRequest):
    result = ClinicalPromptGuardrail.validate_input_prompt(payload.prompt)
    return {
        "is_safe": result.is_safe,
        "risk_level": result.risk_level,
        "flags": result.flags,
        "violation_reason": result.violation_reason,
        "sanitized_text": result.sanitized_text,
    }


@router.post("/guardrail/validate-output", summary="Verify output response maintains safety invariants")
async def validate_output(payload: OutputValidationRequest):
    result = ClinicalPromptGuardrail.validate_output_response(payload.response_text)
    return {
        "is_safe": result.is_safe,
        "risk_level": result.risk_level,
        "flags": result.flags,
        "violation_reason": result.violation_reason,
    }


@router.post("/robustness/audit", summary="Run automated security and robustness audit across test vectors")
async def run_robustness_audit():
    audit_report = RobustnessEvaluator.run_audit()
    return audit_report
