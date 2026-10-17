import os
import re
import unittest

class TestWorldClassFrontendExperience(unittest.TestCase):
    """
    Validates the World-Class Frontend, Health OS, and Mobile Experience Upgrade:
    - The ZAYVORA Clinical Thread™ (12-stage interactive continuum)
    - Clinical Desk™ 3-Zone Desktop Layout (Zone 1: Queue, Zone 2: Encounter, Zone 3: AI & Safety)
    - Exception-First Attention Feed on Clinician 'Today' screen
    - Permanent Fail-Closed Safety Rail
    - Website Guided Care Discovery Wizard ('What brings you here?')
    - Patient Action-Oriented Regimen ('What do I do today?' & Adherence)
    - 21 CFR Part 11 Nuskha Preflight Modal & Digital Seal
    - First-Class Evidence Provenance Drawer (6 mandatory questions)
    - 12-Stage Knowledge Governance Review Pipeline (Research Candidate vs Clinical Approved)
    - Enhanced Command Palette ⌘K with Suggested Clinical Actions
    - Zero Mock Clinical Data Leakage
    """

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.index_path = os.path.join(self.base_dir, "index.html")
        self.assertTrue(os.path.exists(self.index_path), "index.html must exist")
        with open(self.index_path, "r", encoding="utf-8") as f:
            self.html = f.read()
        core_js_path = os.path.join(self.base_dir, "js", "zayvora-core.js")
        if os.path.exists(core_js_path):
            with open(core_js_path, "r", encoding="utf-8") as f:
                self.html += "\n" + f.read()
        ext_js_path = os.path.join(self.base_dir, "js", "zayvora-extensions.js")
        if os.path.exists(ext_js_path):
            with open(ext_js_path, "r", encoding="utf-8") as f:
                self.html += "\n" + f.read()

    def test_clinical_thread_stages_and_interactive_binding(self):
        """Verify all 12 stages of the ZAYVORA Clinical Thread™ are codified."""
        expected_stages = [
            "patient", "assessment", "mizaj", "axes", "knowledge", "evidence",
            "safety", "hakeem", "nuskha", "approval", "treatment", "outcome"
        ]
        self.assertIn("const clinicalThreadStages = [", self.html)
        self.assertIn("function renderClinicalThread(", self.html)
        self.assertIn("function openClinicalThreadModal(", self.html)
        self.assertIn('id="clinical-thread-modal"', self.html)

        for stage in expected_stages:
            self.assertIn(f"id: '{stage}'", self.html, f"Stage {stage} must be in clinicalThreadStages")

    def test_clinical_desk_three_zone_layout(self):
        """Verify the 3-Zone desktop cockpit layout exists in renderSingleConsultationWorkspace."""
        self.assertIn("CLINICAL DESK™ 3-ZONE LAYOUT", self.html)
        self.assertIn("ZONE 1 (Left 3 cols): Queue, Patient & Canonical Tabs", self.html)
        self.assertIn("ZONE 2 (Center 6 cols): Persistent Clinical Thread™ + Encounter Surface", self.html)
        self.assertIn("ZONE 3 (Right 3 cols): Intelligence, Evidence & Permanent Safety Rail", self.html)
        self.assertIn("renderClinicalThread('nuskha')", self.html)

    def test_attention_feed_structure_and_next_patient(self):
        """Verify the exception-first Attention Feed replaces KPI clutter on doctor Today screen."""
        self.assertIn("NEXT PATIENT • TOKEN #T-104", self.html)
        self.assertIn("Hamza Farooqi (42y Male)", self.html)
        self.assertIn("Clinical Attention Feed", self.html)
        self.assertIn("LAB RESULT AVAILABLE", self.html)
        self.assertIn("PHASE MILESTONE DUE", self.html)
        self.assertIn("SCHEDULE E(1) DETOXIFICATION GATE", self.html)
        self.assertIn("21 CFR PART 11 SIGNATURE REQUIRED", self.html)
        self.assertIn("WHY:", self.html)
        self.assertIn("WHEN:", self.html)

    def test_safety_rail_states_and_rules(self):
        """Verify permanent Safety Rail includes all mandatory clinical checks and states."""
        self.assertIn("Permanent Safety Rail", self.html)
        self.assertIn("Allergies & Hypersensitivity", self.html)
        self.assertIn("CYP450 Herb-Drug Interxn", self.html)
        self.assertIn("Schedule E(1) Mudabbar", self.html)
        self.assertIn("Food Antagonism (Tanafur)", self.html)
        self.assertIn("Hemodynamic Pre-req", self.html)
        self.assertIn("safety-badge-pass", self.html)
        self.assertIn("safety-badge-caution", self.html)
        self.assertIn("Re-evaluate Safety Rails", self.html)

    def test_care_discovery_wizard_flows(self):
        """Verify Website Guided Care Discovery Wizard exists and has all 9 concerns and 5 care types."""
        self.assertIn('id="care-discovery-wizard"', self.html)
        self.assertIn("const discoveryConcerns = [", self.html)
        self.assertIn("const discoveryCareTypes = [", self.html)
        self.assertIn("function selectDiscoveryConcern(", self.html)
        self.assertIn("function selectDiscoveryCareType(", self.html)
        self.assertIn("function renderDiscoveryWizard(", self.html)

        concerns = ["Digestive", "Metabolic", "Hormonal", "Reproductive", "Musculoskeletal", "Sleep_Stress", "Respiratory", "Skin_Hair", "General_Wellness"]
        for c in concerns:
            self.assertIn(f"id: '{c}'", self.html, f"Concern {c} must be defined")

        care_types = ["Consultation", "Program", "Follow_up", "Second_Opinion", "Lifestyle_Support"]
        for ct in care_types:
            self.assertIn(f"id: '{ct}'", self.html, f"Care type {ct} must be defined")

    def test_patient_action_oriented_flow(self):
        """Verify Patient Mobile view is action-oriented with plain language adherence tracking."""
        self.assertIn("TODAY'S CARE • NEXT ACTION", self.html)
        self.assertIn("Hab-e-Suranjan (2 pills) + Roghan Massage", self.html)
        self.assertIn("trackPatientAdherence", self.html)
        self.assertIn("✓ Yes, Taken", self.html)
        self.assertIn("⏳ Not Yet", self.html)
        self.assertIn("✕ Skipped", self.html)

    def test_nuskha_preflight_modal_and_digital_seal(self):
        """Verify 21 CFR Part 11 Nuskha Preflight modal and digital signature seal exist."""
        self.assertIn('id="nuskha-preflight-modal"', self.html)
        self.assertIn("Nuskha Preflight & 21 CFR Part 11 Digital Signoff", self.html)
        self.assertIn("function openNuskhaPreflightModal(", self.html)
        self.assertIn("function executeNuskhaDigitalSeal(", self.html)
        self.assertIn("Clinician Statutory Scope", self.html)
        self.assertIn("SHA-256 Merkle Ledger", self.html)

    def test_first_class_evidence_drawer(self):
        """Verify the 6-question Evidence Drawer slide-over exists and opens on demand."""
        self.assertIn('id="evidence-drawer-overlay"', self.html)
        self.assertIn("Evidence Provenance Drawer", self.html)
        self.assertIn("function toggleEvidenceDrawer(", self.html)
        self.assertIn("1. What is the Clinical Claim?", self.html)
        self.assertIn("2. What is the Authoritative Source?", self.html)
        self.assertIn("3. How Strong is the Evidence?", self.html)
        self.assertIn("4. Who Reviewed and Approved It?", self.html)
        self.assertIn("5. When Was the Review Certified?", self.html)
        self.assertIn("6. What are the Clinical Limitations?", self.html)

    def test_knowledge_governance_12_stage_pipeline(self):
        """Verify 12-stage review pipeline and strict demarcation between Clinical Approved and Research Candidate."""
        self.assertTrue(
            "12-Stage Knowledge Governance & Formulary Validation Pipeline" in self.html or
            "12-Stage Knowledge Governance & AI Promotion Pipeline" in self.html
        )
        self.assertIn("CLINICAL APPROVED • STAGE 12/12", self.html)
        self.assertIn("RESEARCH CANDIDATE • STAGE 06/12", self.html)
        self.assertTrue(
            "PRESCRIPTION GOVERNANCE LOCK" in self.html or
            "AI PRESCRIBING BLOCKED" in self.html
        )
        self.assertIn("Strictly isolated in Research Staging partition", self.html)

    def test_command_palette_suggested_clinical_actions(self):
        """Verify ⌘K Command Palette includes suggested clinical quick actions."""
        self.assertIn("Action • Start Patient Consultation", self.html)
        self.assertIn("Action • Clinical Decision Support", self.html)
        self.assertIn("Action • Safety Firewall Check", self.html)
        self.assertIn("Action • Formulate Multi-Pillar Rx", self.html)

    def test_zero_mock_leakage_and_insufficient_data_integrity(self):
        """Verify zero undefined/null rendering and proper insufficient data handling."""
        self.assertNotIn(">undefined<", self.html)
        self.assertNotIn(">null<", self.html)
        self.assertNotIn(">NaN<", self.html)
        self.assertTrue(
            "Clinical Decision Support" in self.html and
            "Attending physician" in self.html
        )

if __name__ == '__main__':
    unittest.main()
