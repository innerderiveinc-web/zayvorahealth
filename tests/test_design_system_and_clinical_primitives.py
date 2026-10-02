import os
import re
import unittest

class TestDesignSystemAndClinicalPrimitives(unittest.TestCase):
    """
    Validates the Design System package expansion:
    - 9 Foundational Primitives (Drawer, Search, Tooltip, Toast, Table, Progress, ErrorState, OfflineState, ForbiddenState)
    - 22 Specialized Clinical Components
    - Complete index.ts barrel exports and TypeScript typings
    - Zero-mock data discipline & fail-closed safety assertions
    """

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ds_dir = os.path.join(self.base_dir, "design-system")
        self.src_dir = os.path.join(self.ds_dir, "src")
        self.primitives_dir = os.path.join(self.src_dir, "primitives")
        self.clinical_dir = os.path.join(self.src_dir, "clinical")
        self.index_path = os.path.join(self.src_dir, "index.ts")

    def test_primitives_files_exist(self):
        """Verify all 9 foundational primitives exist as .tsx files."""
        expected_primitives = [
            "Drawer.tsx", "Search.tsx", "Tooltip.tsx", "Toast.tsx",
            "Table.tsx", "Progress.tsx", "ErrorState.tsx",
            "OfflineState.tsx", "ForbiddenState.tsx"
        ]
        for prim in expected_primitives:
            p = os.path.join(self.primitives_dir, prim)
            self.assertTrue(os.path.exists(p), f"Primitive {prim} must exist in {self.primitives_dir}")
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("export ", content, f"{prim} must export its component")

    def test_clinical_components_files_exist(self):
        """Verify all 22 specialized clinical components exist as .tsx files."""
        expected_clinical = [
            "PatientHeader.tsx", "ClinicalThread.tsx", "AttentionFeed.tsx", "MizajStatus.tsx",
            "AxisRow.tsx", "AxisDetail.tsx", "EvidenceCard.tsx", "EvidenceDrawer.tsx",
            "SafetyRail.tsx", "SafetyDecision.tsx", "HakeemInsight.tsx", "KnowledgeProvenance.tsx",
            "TrustLedger.tsx", "NuskhaComposer.tsx", "NuskhaPreflight.tsx", "ApprovalPanel.tsx",
            "SignatureSummary.tsx", "CareProgressRibbon.tsx", "OutcomeCard.tsx", "AdherenceCard.tsx",
            "DataFreshness.tsx", "ConsentStatus.tsx"
        ]
        self.assertEqual(len(expected_clinical), 22, "Must test exactly 22 clinical components")
        for comp in expected_clinical:
            p = os.path.join(self.clinical_dir, comp)
            self.assertTrue(os.path.exists(p), f"Clinical component {comp} must exist in {self.clinical_dir}")
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("export ", content, f"{comp} must export its component")

    def test_index_barrel_exports(self):
        """Verify design-system/src/index.ts exports all components and types."""
        with open(self.index_path, "r", encoding="utf-8") as f:
            idx = f.read()

        # Check primitive exports
        primitives = [
            "Drawer", "Search", "Tooltip", "Toast", "ToastContainer",
            "Table", "Progress", "ErrorState", "OfflineState", "ForbiddenState"
        ]
        for p in primitives:
            self.assertTrue(re.search(r'\bexport\s*\{[^}]*\b' + p + r'\b[^}]*\}', idx), f"Index must export primitive {p}")

        # Check clinical exports
        clinical = [
            "PatientHeader", "ClinicalThread", "AttentionFeed", "MizajStatus",
            "AxisRow", "AxisDetail", "EvidenceCard", "EvidenceDrawer",
            "SafetyRail", "SafetyDecision", "HakeemInsight", "KnowledgeProvenance",
            "TrustLedger", "NuskhaComposer", "NuskhaPreflight", "ApprovalPanel",
            "SignatureSummary", "CareProgressRibbon", "OutcomeCard", "AdherenceCard",
            "DataFreshness", "ConsentStatus"
        ]
        for c in clinical:
            self.assertTrue(re.search(r'\bexport\s*\{[^}]*\b' + c + r'\b[^}]*\}', idx), f"Index must export clinical component {c}")

    def test_zero_mock_data_discipline(self):
        """Ensure clinical components default to unassessed/insufficient data instead of fabricated values."""
        # PatientHeader must fallback to Needs Assessment when dominantMizaj is null
        with open(os.path.join(self.clinical_dir, "PatientHeader.tsx"), "r", encoding="utf-8") as f:
            header_src = f.read()
            self.assertIn("Needs Assessment", header_src)

        # MizajStatus must handle Pending
        with open(os.path.join(self.clinical_dir, "MizajStatus.tsx"), "r", encoding="utf-8") as f:
            mizaj_src = f.read()
            self.assertIn("Needs Assessment", mizaj_src)
            self.assertIn("Pending", mizaj_src)

        # DataFreshness must have INSUFFICIENT_DATA state
        with open(os.path.join(self.clinical_dir, "DataFreshness.tsx"), "r", encoding="utf-8") as f:
            freshness_src = f.read()
            self.assertIn("INSUFFICIENT_DATA", freshness_src)

    def test_safety_fail_closed_guarantees(self):
        """Verify fail-closed safety assertions in SafetyRail, SafetyDecision, and NuskhaPreflight."""
        with open(os.path.join(self.clinical_dir, "SafetyRail.tsx"), "r", encoding="utf-8") as f:
            rail_src = f.read()
            self.assertIn("HARD BLOCK ENFORCED", rail_src)
            self.assertIn("CAUTION: JUSTIFICATION REQ", rail_src)

        with open(os.path.join(self.clinical_dir, "SafetyDecision.tsx"), "r", encoding="utf-8") as f:
            decision_src = f.read()
            self.assertIn("Safety Invariant Violation (Hard Block)", decision_src)
            self.assertIn("Prescription Formulation Blocked", decision_src)

        with open(os.path.join(self.clinical_dir, "NuskhaPreflight.tsx"), "r", encoding="utf-8") as f:
            preflight_src = f.read()
            self.assertIn("GATE FAILED", preflight_src)
            self.assertIn("Schedule E(1) Detoxification", preflight_src)

    def test_cfr_part_11_digital_signature_integrity(self):
        """Verify 21 CFR Part 11 requirements in approval and trust components."""
        with open(os.path.join(self.clinical_dir, "ApprovalPanel.tsx"), "r", encoding="utf-8") as f:
            appr_src = f.read()
            self.assertIn("21 CFR Part 11 Electronic Signature Authority", appr_src)
            self.assertIn("Signing PIN", appr_src)

        with open(os.path.join(self.clinical_dir, "SignatureSummary.tsx"), "r", encoding="utf-8") as f:
            summary_src = f.read()
            self.assertIn("21 CFR Part 11 Digital Signature Seal Verified", summary_src)
            self.assertIn("SHA-256 Seal", summary_src)

        with open(os.path.join(self.clinical_dir, "TrustLedger.tsx"), "r", encoding="utf-8") as f:
            ledger_src = f.read()
            self.assertIn("Merkle Root", ledger_src)
            self.assertIn("sha256Seal", ledger_src)

    def test_hakeem_sahab_disclaimer_and_evidence_provenance(self):
        """Verify AI copilot disclaimer and evidence drawer 6 questions."""
        with open(os.path.join(self.clinical_dir, "HakeemInsight.tsx"), "r", encoding="utf-8") as f:
            hakeem_src = f.read()
            self.assertIn("AI suggests. Clinician decides.", hakeem_src)
            self.assertIn("uncertaintyScore", hakeem_src)

        with open(os.path.join(self.clinical_dir, "EvidenceDrawer.tsx"), "r", encoding="utf-8") as f:
            drawer_src = f.read()
            self.assertIn("1. What is the Clinical Claim?", drawer_src)
            self.assertIn("2. What is the Authoritative Source?", drawer_src)
            self.assertIn("3. How Strong is the Evidence?", drawer_src)
            self.assertIn("4. Who Reviewed and Approved It?", drawer_src)
            self.assertIn("5. When Was the Review Certified?", drawer_src)
            self.assertIn("6. What are the Clinical Limitations?", drawer_src)

if __name__ == '__main__':
    unittest.main()
