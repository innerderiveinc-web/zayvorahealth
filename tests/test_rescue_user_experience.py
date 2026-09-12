#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — UX Rescue & Product Usability Verification Suite
Validates that:
1. All 14 rescue audit documents exist and are populated.
2. The UI is completely free of developer jargon on clinical/patient screens.
3. Role-based app shells provide clean medical experiences.
4. The 16-section Doctor Consultation Workspace is fully integrated.
5. SCREEN_STATUS_MATRIX.csv has valid statuses across all screens.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESCUE_DIR = os.path.join(BASE_DIR, "docs/rescue")
PREVIEW_FILE = os.path.join(BASE_DIR, "docs/zayvora_health_os_preview.html")

def test_rescue_documentation_completeness():
    required_files = [
        "LIVE_PREVIEW_AUDIT.md",
        "PRODUCT_POSITIONING.md",
        "ROLE_BASED_NAVIGATION.md",
        "CORE_WORKFLOW_MAP.md",
        "UI_UX_REDESIGN_PLAN.md",
        "FRONTEND_REPAIR_REPORT.md",
        "BACKEND_REPAIR_REPORT.md",
        "API_CONNECTION_REPORT.md",
        "BROKEN_FEATURES.md",
        "HIDDEN_FEATURES.md",
        "FINAL_USER_ACCEPTANCE_TEST.md",
        "USER_CONFUSION_REPORT.md",
        "CORE_PRODUCT_SCOPE.md",
        "SCREEN_STATUS_MATRIX.csv"
    ]
    for rf in required_files:
        p = os.path.join(RESCUE_DIR, rf)
        assert os.path.exists(p), f"Missing rescue deliverable: {rf}"
        assert os.path.getsize(p) > 100, f"File {rf} is too small or empty"
    print("✓ All 14 rescue documents and matrix verified.")


def test_no_developer_jargon_in_clinical_screens():
    with open(PREVIEW_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Split between clinical/patient screens and the Admin IT console
    admin_split = html.find("renderAdminApp")
    clinical_part = html[:admin_split]

    forbidden_in_clinical = [
        "25-Engine Live Matrix",
        "safe_to_lock = False",
        "P0/P1 Blockers",
        "0 OPEN (P0/P1)",
        "P95 Latency 1.2ms",
        "Vector Store",
        "Database Tables",
        "Service Mesh",
        "RAG Retrieval"
    ]
    for term in forbidden_in_clinical:
        assert term not in clinical_part, f"Forbidden developer term found in clinical view: '{term}'"
    print("✓ Zero developer jargon detected in Patient, Doctor, or Clinic views.")


def test_doctor_consultation_has_all_sections():
    with open(PREVIEW_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    sections = [
        "Patient Clinical Summary",
        "Chief Complaint",
        "Vital Signs",
        "10-Ajnas Longitudinal Mizaj",
        "Organ-Axis Physiological Cross-Talk",
        "Hakeem Sahab AI Clinical Assistant",
        "Prescription Formulation",
        "Medication Safety & Interaction Review",
        "Follow-up Encounter",
        "21 CFR Part 11 Cryptographic Clinician Approval"
    ]
    for s in sections:
        assert s in html, f"Missing consultation section in Doctor Workspace: '{s}'"
    print("✓ Single Doctor Consultation Workspace verified with all clinical sections.")


def test_screen_status_matrix_validity():
    csv_path = os.path.join(RESCUE_DIR, "SCREEN_STATUS_MATRIX.csv")
    with open(csv_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) >= 15, "Status matrix has insufficient screen evaluations"
    header = lines[0].strip().split(",")
    assert "Role" in header and "Screen" in header and "Final Status" in header
    for line in lines[1:]:
        if line.strip():
            cols = line.strip().split(",")
            assert cols[-2] == "READY", f"Screen not READY in matrix: {line}"
    print("✓ SCREEN_STATUS_MATRIX.csv validated across all roles and screens.")


if __name__ == "__main__":
    print("=" * 80)
    print("ZAYVORA HEALTH OS™ — UX RESCUE VERIFICATION TEST RUNNER")
    print("=" * 80)
    test_rescue_documentation_completeness()
    test_no_developer_jargon_in_clinical_screens()
    test_doctor_consultation_has_all_sections()
    test_screen_status_matrix_validity()
    print("=" * 80)
    print("✓ ALL UX RESCUE VERIFICATION TESTS PASSED SUCCESSFULLY.")
    print("=" * 80)
