#!/usr/bin/env python3
"""
ZAYVORA Health™ — Phase 9: Statutory Regulatory Clearances & Traceability Test Suite.

Verifies:
1. IEC 62304:2006/Amd 1:2015 Bidirectional Traceability Matrix completeness (100% coverage).
2. Zero orphaned statutory requirements across CDSCO, AYUSH, ABDM, and 21 CFR Part 11.
3. Regulatory inspection pack integrity signature and standards conformance list.
4. Statutory Schedule E(1) and NCISM non-delegable prescribing authority alignment.
"""

import hashlib
import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.clinical.app.governance.regulatory_dossier_engine import (
    RegulatoryDossierEngine,
    TraceabilityEntry,
)


class TestRegulatoryDossier(unittest.TestCase):
    """Test suite certifying Phase 9 regulatory dossier and technical file integrity."""

    def test_01_traceability_matrix_100_percent_coverage(self):
        """Verify that all statutory requirements have 100% verified status."""
        metrics = RegulatoryDossierEngine.verify_traceability_matrix()
        self.assertEqual(metrics["status"], "100_PERCENT_TRACEABILITY_VERIFIED")
        self.assertEqual(metrics["traceability_coverage_pct"], 100.0)
        self.assertEqual(metrics["unverified_requirements"], 0)
        self.assertGreaterEqual(metrics["total_statutory_requirements"], 10)

    def test_02_zero_orphaned_requirements(self):
        """Verify that every requirement has a valid code artifact, DB constraint, and test."""
        for entry in RegulatoryDossierEngine.TRACEABILITY_REGISTER:
            self.assertTrue(entry.requirement_id.startswith("REQ-"))
            self.assertTrue(len(entry.code_artifact) > 0, f"Empty code artifact in {entry.requirement_id}")
            self.assertTrue(len(entry.database_constraint) > 0, f"Empty DB constraint in {entry.requirement_id}")
            self.assertTrue(len(entry.verification_test) > 0, f"Empty test in {entry.requirement_id}")
            self.assertEqual(entry.verification_status, "VERIFIED_PASSING")

    def test_03_regulatory_inspection_pack_generation(self):
        """Verify that the official inspection pack is generated with valid integrity signature."""
        pack = RegulatoryDossierEngine.generate_inspection_pack()
        self.assertEqual(pack["document_id"], "CDSCO-AYUSH-DOSSIER-2026-V1")
        self.assertEqual(pack["regulatory_verdict"], "READY_FOR_STATUTORY_CDSCO_AYUSH_FILING")
        self.assertTrue(len(pack["integrity_signature"]) == 64)  # Valid SHA-256

        standards = pack["standards_conformance"]
        self.assertTrue(any("IEC 62304" in s for s in standards))
        self.assertTrue(any("ISO 13485" in s for s in standards))
        self.assertTrue(any("Schedule E(1)" in s for s in standards))
        self.assertTrue(any("NCISM" in s for s in standards))
        self.assertTrue(any("21 CFR Part 11" in s for s in standards))

    def test_04_statutory_poison_and_prescribing_traceability(self):
        """Verify specific traceability for SAF-01 (Mudabbar) and SAF-02 (Prescribing)."""
        reg = {e.requirement_id: e for e in RegulatoryDossierEngine.TRACEABILITY_REGISTER}
        
        self.assertIn("REQ-SAF-01", reg)
        e1 = reg["REQ-SAF-01"]
        self.assertIn("chk_schedule_e1_mudabbar", e1.database_constraint)
        self.assertIn("allocate_fefo_batches", e1.code_artifact)

        self.assertIn("REQ-SAF-02", reg)
        e2 = reg["REQ-SAF-02"]
        self.assertIn("chk_nuskha_draft_status", e2.database_constraint)
        self.assertIn("NCISM Act 2020", e2.standard_reference)

    def test_05_dossier_document_exists_and_complete(self):
        """Verify that the formal technical dossier markdown document is intact."""
        dossier_path = os.path.join(BASE_DIR, "docs/zayvora-audit/PHASE9_STATUTORY_REGULATORY_DOSSIER.md")
        self.assertTrue(os.path.exists(dossier_path))
        with open(dossier_path, "r") as f:
            content = f.read()
        self.assertIn("Central Drugs Standard Control Organisation (CDSCO)", content)
        self.assertIn("Essential Principles of Safety & Performance", content)
        self.assertIn("IEC 62304 / ISO 14971 Bidirectional Traceability Matrix", content)


if __name__ == "__main__":
    unittest.main()
