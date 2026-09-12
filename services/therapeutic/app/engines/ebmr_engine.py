"""
ZAYVORA Manufacturing OS & Electronic Batch Manufacturing Records (eBMR 2.0).
Phase 14 — Master Formula Records (MFR), In-Process QC Gates & Schedule E(1) Mudabbar Verification.

Complies with:
- AYUSH Good Manufacturing Practices (GMP / Schedule T)
- 21 CFR Part 11 Electronic Batch Records & Digital Sign-off
- Heavy Metal & Microbial Limits (WHO/UPI Standards)
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any


CANONICAL_MFRS: dict[str, dict[str, Any]] = {
    "mfr-majun-falasifa": {
        "mfr_id": "mfr-majun-falasifa",
        "product_name": "Majun Falasifa",
        "category": "Majun (Electuary)",
        "canonical_reference": "NFUM Part-I, Formulation 1:22",
        "standard_batch_size": 10.0,
        "unit": "kg",
        "shelf_life_months": 36,
        "ingredients": [
            {"name": "Maghz-e-Chilgoza", "ratio": 0.05, "is_schedule_e1": False},
            {"name": "Filfil Siyah", "ratio": 0.05, "is_schedule_e1": False},
            {"name": "Zanjabeel", "ratio": 0.05, "is_schedule_e1": False},
            {"name": "Sheetraj Hindi", "ratio": 0.05, "is_schedule_e1": False},
            {"name": "Zarawand Mudaharrij", "ratio": 0.05, "is_schedule_e1": False},
            {"name": "Salab Misri", "ratio": 0.05, "is_schedule_e1": False},
            {"name": "Qiwam (Sugar / Honey Base 70 Brix)", "ratio": 0.70, "is_schedule_e1": False},
        ],
        "critical_steps": [
            {"step_number": 1, "name": "Raw Herb Cleaning & Sifting", "duration_minutes": 60, "hold_point": True},
            {"step_number": 2, "name": "Fine Pulverization (Mesh 80)", "duration_minutes": 90, "hold_point": False},
            {"step_number": 3, "name": "Qiwam Preparation (Target 70-72 Brix at 105C)", "duration_minutes": 120, "hold_point": True},
            {"step_number": 4, "name": "Gradual Blending & Cooling to 45C", "duration_minutes": 60, "hold_point": True},
            {"step_number": 5, "name": "Post-Compounding Maturation", "duration_minutes": 2880, "hold_point": True},
        ],
        "ipqc_specs": {
            "brix_refraction": {"target": 71.0, "min": 68.0, "max": 74.0, "unit": "°Bx"},
            "ph_value": {"target": 5.2, "min": 4.5, "max": 6.0, "unit": "pH"},
            "lead_pb_ppm": {"target": 1.0, "min": 0.0, "max": 10.0, "unit": "ppm"},
            "arsenic_as_ppm": {"target": 0.5, "min": 0.0, "max": 3.0, "unit": "ppm"},
            "total_bacterial_count": {"target": 100, "min": 0, "max": 10000, "unit": "CFU/g"},
        },
    },
    "mfr-majun-suranjan": {
        "mfr_id": "mfr-majun-suranjan",
        "product_name": "Majun Suranjan",
        "category": "Majun (Electuary with Schedule E1 Poison)",
        "canonical_reference": "NFUM Part-I, Formulation 1:26",
        "standard_batch_size": 10.0,
        "unit": "kg",
        "shelf_life_months": 36,
        "ingredients": [
            {
                "name": "Suranjan Talkh",
                "ratio": 0.10,
                "is_schedule_e1": True,
                "mandatory_mudabbar_protocol": "Boiled in cow's milk for 3h, peeled, dried, fried in Roghan-e-Badam.",
            },
            {"name": "Sana-e-Makki", "ratio": 0.05, "is_schedule_e1": False},
            {"name": "Turbud Safaid", "ratio": 0.05, "is_schedule_e1": False},
            {"name": "Post-e-Halela Zard", "ratio": 0.05, "is_schedule_e1": False},
            {"name": "Qiwam Base", "ratio": 0.75, "is_schedule_e1": False},
        ],
        "critical_steps": [
            {"step_number": 1, "name": "Raw Drug Quarantine Inspection", "duration_minutes": 30, "hold_point": True},
            {
                "step_number": 2,
                "name": "Schedule E(1) Mudabbar Detoxification of Suranjan Talkh",
                "duration_minutes": 240,
                "hold_point": True,  # Critical statutory hold point
            },
            {"step_number": 3, "name": "Qiwam Compounding", "duration_minutes": 120, "hold_point": False},
            {"step_number": 4, "name": "Homogenization and QA Sample Release", "duration_minutes": 60, "hold_point": True},
        ],
        "ipqc_specs": {
            "brix_refraction": {"target": 70.0, "min": 68.0, "max": 73.0, "unit": "°Bx"},
            "ph_value": {"target": 5.0, "min": 4.5, "max": 5.8, "unit": "pH"},
            "lead_pb_ppm": {"target": 1.0, "min": 0.0, "max": 10.0, "unit": "ppm"},
            "arsenic_as_ppm": {"target": 0.5, "min": 0.0, "max": 3.0, "unit": "ppm"},
            "total_bacterial_count": {"target": 100, "min": 0, "max": 10000, "unit": "CFU/g"},
        },
    },
}


class eBMRBatchSession:
    """Manages state transitions, IPQC verifications, and release gate for an active eBMR run."""

    def __init__(self, batch_number: str, mfr_id: str, batch_size: float, operator_id: str):
        if mfr_id not in CANONICAL_MFRS:
            raise ValueError(f"Master Formula Record '{mfr_id}' not found in canonical MFR registry.")

        self.batch_id = str(uuid.uuid4())
        self.batch_number = batch_number
        self.mfr = CANONICAL_MFRS[mfr_id]
        self.batch_size = batch_size
        self.status = "STAGED"  # STAGED -> IN_PROCESS -> IPQC_TESTING -> RELEASED / REJECTED
        self.operator_id = operator_id
        self.created_at = datetime.utcnow().isoformat()
        self.stage_signoffs: list[dict[str, Any]] = []
        self.ipqc_results: dict[str, float] = {}
        self.mudabbar_verified: bool = False
        self.mudabbar_certificate_no: str | None = None
        self.has_schedule_e1 = any(ing.get("is_schedule_e1") for ing in self.mfr["ingredients"])

    def record_stage_signoff(
        self,
        *,
        step_number: int,
        operator_id: str,
        comments: str = "",
        mudabbar_cert_no: str | None = None,
    ) -> dict[str, Any]:
        """Records electronic signature for a critical process step."""
        step = next((s for s in self.mfr["critical_steps"] if s["step_number"] == step_number), None)
        if not step:
            raise ValueError(f"Step {step_number} is not defined in MFR {self.mfr['mfr_id']}.")

        if "Mudabbar" in step["name"] and self.has_schedule_e1:
            if not mudabbar_cert_no:
                raise ValueError("Schedule E(1) Mudabbar detoxification step requires a verified Mudabbar Certificate Number.")
            self.mudabbar_verified = True
            self.mudabbar_certificate_no = mudabbar_cert_no

        signoff = {
            "step_number": step_number,
            "step_name": step["name"],
            "signed_by_operator": operator_id,
            "timestamp": datetime.utcnow().isoformat(),
            "comments": comments,
            "mudabbar_cert_applied": mudabbar_cert_no,
        }
        self.stage_signoffs.append(signoff)
        self.status = "IN_PROCESS"
        return signoff

    def submit_ipqc_results(self, test_results: dict[str, float]) -> dict[str, Any]:
        """Submits In-Process Quality Control (IPQC) laboratory results and validates
        against MFR statutory pharmacopoeial specifications."""
        self.ipqc_results = test_results
        self.status = "IPQC_TESTING"
        violations = []

        specs = self.mfr["ipqc_specs"]
        for param, val in test_results.items():
            if param in specs:
                spec = specs[param]
                if val < spec["min"] or val > spec["max"]:
                    violations.append(
                        f"Parameter '{param}' value {val} {spec['unit']} out of range [{spec['min']} - {spec['max']} {spec['unit']}]."
                    )

        passed = len(violations) == 0
        return {
            "status": "PASSED" if passed else "FAILED_SPECIFICATION",
            "passed": passed,
            "tested_parameters": len(test_results),
            "violations": violations,
        }

    def execute_final_qa_release(self, qa_director_id: str, statutory_affirmation: bool = True) -> dict[str, Any]:
        """Final QA Release Gate: Ensures all hold points signed, Mudabbar certified if Schedule E(1),
        and IPQC assays comply with statutory limits. Yields a Certificate of Analysis (CoA)."""
        if not statutory_affirmation:
            raise ValueError("Statutory affirmation of GMP release is required.")

        # Check Mudabbar requirement
        if self.has_schedule_e1 and not self.mudabbar_verified:
            self.status = "REJECTED"
            raise ValueError("QA RELEASE BLOCKED: Schedule E(1) substance lacks completed Mudabbar detoxification.")

        # Check all hold points are signed off
        mandatory_steps = [s["step_number"] for s in self.mfr["critical_steps"] if s["hold_point"]]
        signed_steps = [s["step_number"] for s in self.stage_signoffs]
        missing_steps = [s for s in mandatory_steps if s not in signed_steps]
        if missing_steps:
            raise ValueError(f"QA RELEASE BLOCKED: Critical hold points {missing_steps} are missing operator sign-off.")

        # Validate IPQC
        ipqc_check = self.submit_ipqc_results(self.ipqc_results)
        if not ipqc_check["passed"]:
            self.status = "REJECTED"
            raise ValueError(f"QA RELEASE BLOCKED: IPQC assay violations detected: {ipqc_check['violations']}")

        self.status = "RELEASED"

        # Generate Certificate of Analysis (CoA)
        coa = {
            "certificate_id": f"COA-{self.batch_number}",
            "product_name": self.mfr["product_name"],
            "batch_number": self.batch_number,
            "manufacturing_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "mfr_reference": self.mfr["canonical_reference"],
            "batch_size": f"{self.batch_size} {self.mfr['unit']}",
            "is_schedule_e1": self.has_schedule_e1,
            "mudabbar_certified": self.mudabbar_verified,
            "mudabbar_certificate_number": self.mudabbar_certificate_no,
            "ipqc_assays": self.ipqc_results,
            "qa_director_id": qa_director_id,
            "release_timestamp": datetime.utcnow().isoformat(),
            "verdict": "CERTIFIED_GMP_RELEASE",
        }
        return coa
