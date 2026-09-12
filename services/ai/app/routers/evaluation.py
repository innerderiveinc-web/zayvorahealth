"""
ZAYVORA HEALTH™ — Clinical AI Evaluation Lab Router
Exposes endpoints for running Hakeem Sahab benchmarks and inspection of gold-standard cases.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from ..evaluation.benchmark_cases import GOLD_STANDARD_BENCHMARK_CASES
from ..evaluation.eval_engine import EvaluationEngine

router = APIRouter(prefix="/api/v1/hakeem/eval", tags=["AI Evaluation Lab"])


class SingleCaseEvalRequest(BaseModel):
    case_id: str = Field(..., description="Benchmark case ID (e.g. UBM-001)")
    response_text: str = Field(..., description="The AI copilot generated clinical response text")


class SuiteEvalRequest(BaseModel):
    responses_by_case_id: Dict[str, str] = Field(
        ..., description="Map of case_id to copilot generated response text"
    )


@router.get("/cases", summary="List gold-standard classical Unani benchmark cases")
async def list_benchmark_cases(category: Optional[str] = None):
    cases = GOLD_STANDARD_BENCHMARK_CASES
    if category:
        cases = [c for c in cases if category.lower() in c.category.lower()]

    return [
        {
            "case_id": c.case_id,
            "title": c.title,
            "category": c.category,
            "patient_profile": c.patient_profile,
            "expected_mizaj": {
                "dominant": c.expected_mizaj_dominant,
                "secondary": c.expected_mizaj_secondary,
            },
            "expected_amraz": {
                "icd11": c.expected_amraz_icd11,
                "unani": c.expected_amraz_unani,
            },
            "expected_canonical_formulations": c.expected_canonical_formulations,
            "schedule_e1_substances": c.schedule_e1_substances,
            "requires_mudabbar": c.requires_mudabbar,
            "mandatory_citations": c.mandatory_citations,
        }
        for c in cases
    ]


@router.get("/cases/{case_id}", summary="Get specific benchmark case by ID")
async def get_benchmark_case(case_id: str):
    case = next((c for c in GOLD_STANDARD_BENCHMARK_CASES if c.case_id == case_id), None)
    if not case:
        raise HTTPException(status_code=404, detail=f"Benchmark case '{case_id}' not found.")
    return {
        "case_id": case.case_id,
        "title": case.title,
        "category": case.category,
        "patient_profile": case.patient_profile,
        "expected_mizaj_dominant": case.expected_mizaj_dominant,
        "expected_mizaj_secondary": case.expected_mizaj_secondary,
        "expected_amraz_icd11": case.expected_amraz_icd11,
        "expected_amraz_unani": case.expected_amraz_unani,
        "expected_canonical_formulations": case.expected_canonical_formulations,
        "contraindicated_substances": case.contraindicated_substances,
        "schedule_e1_substances": case.schedule_e1_substances,
        "requires_mudabbar": case.requires_mudabbar,
        "mandatory_citations": case.mandatory_citations,
        "posology_rules": case.posology_rules,
    }


@router.post("/evaluate-case", summary="Evaluate a candidate clinical response against a benchmark case")
async def evaluate_single_case(payload: SingleCaseEvalRequest):
    case = next((c for c in GOLD_STANDARD_BENCHMARK_CASES if c.case_id == payload.case_id), None)
    if not case:
        raise HTTPException(status_code=404, detail=f"Benchmark case '{payload.case_id}' not found.")

    report = EvaluationEngine.evaluate_case(payload.response_text, case)
    return {
        "case_id": report.case_id,
        "case_title": report.case_title,
        "overall_score": report.overall_score,
        "grade": report.grade,
        "critical_safety_pass": report.critical_safety_pass,
        "summary": report.summary,
        "section_completeness": {
            "found_count": report.section_completeness.found_count,
            "total_expected": report.section_completeness.total_expected,
            "missing_sections": report.section_completeness.missing_sections,
            "score": report.section_completeness.score,
        },
        "citation_eval": {
            "precision_score": report.citation_eval.precision_score,
            "found_citations": report.citation_eval.found_citations,
            "missing_mandatory": report.citation_eval.missing_mandatory,
        },
        "hallucination_eval": {
            "hallucination_index": report.hallucination_eval.hallucination_index,
            "contraindications_detected": report.hallucination_eval.contraindications_detected,
            "unauthorized_claims": report.hallucination_eval.unauthorized_claims,
            "is_acceptable": report.hallucination_eval.is_acceptable,
        },
        "safety_eval": {
            "passed": report.safety_eval.passed,
            "safety_score": report.safety_eval.safety_score,
            "schedule_e1_detected": report.safety_eval.schedule_e1_detected,
            "mudabbar_protocol_present": report.safety_eval.mudabbar_protocol_present,
        },
        "invariant_eval": {
            "passed": report.invariant_eval.passed,
            "safe_to_lock_preserved_false": report.invariant_eval.safe_to_lock_preserved_false,
            "clinician_review_demanded": report.invariant_eval.clinician_review_demanded,
        },
    }


@router.post("/evaluate-suite", summary="Evaluate a candidate response suite across all benchmark cases")
async def evaluate_suite(payload: SuiteEvalRequest):
    results = EvaluationEngine.evaluate_suite(payload.responses_by_case_id)
    return results
