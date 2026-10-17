"""
ZAYVORA Health OS™ V2 — Evidence-Governed Clinical Intelligence Test Suite
==========================================================================
Verifies the complete 17-point prioritized blueprint:
P0-1:  ZMIE Evidence & Provenance Layer
P0-2:  Clinical Truth Firewall (Fail-Closed Engine)
P0-3:  Tripartite Separation (Classical vs Modern vs Interpretation vs Status)
P0-4:  Scientifically Honest Mizaj Research Engine
P0-5:  Patient 360 as Center of the OS
P0-6:  Longitudinal Clinical Timeline
P0-7:  Hakeem Sahab V2 Clinical Copilot (Advisory Only)
P0-8:  Explicit Uncertainty Engine
P0-9:  7-Tier Formulation Evidence Ladder (E0-E6)
P0-10: First-Class Pharmacovigilance Longitudinal Registry
P0-11: Regulatory Claim Defensibility
P0-12: Clear Demo Sandbox Presentation
P0-13: Permissions Architecture & Clinical Audit Ledger
P0-14: Full Consent Engine
P0-15: Real-World Evidence & Clinical Outcomes Engine
P0-16: Clinical Validation Benchmarks (BM-001 - BM-005)
P0-17: 9-Hub Master Navigation Architecture
"""

import unittest
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.knowledge.app.engines.zmie_provenance_firewall import (
    EVIDENCE_LADDER_TIERS,
    EvidenceProvenanceClaim,
    TripartiteKnowledgeUnit,
    UncertaintyAssessment,
    ScientificMizajEvaluation,
    ClinicalCopilotAdvisory,
    ClinicalTruthFirewall
)
from services.live_api_server import (
    get_db,
    _build_patient_360_v2,
    _decrypt_phi
)


class TestV2EvidenceGovernedClinicalIntelligence(unittest.TestCase):

    def test_01_evidence_ladder_and_provenance_specification(self):
        """P0-1 & P0-9: 7-Tier Evidence Ladder (E0-E6) and Strict Provenance Schema"""
        self.assertEqual(len(EVIDENCE_LADDER_TIERS), 7)
        self.assertIn("E0", EVIDENCE_LADDER_TIERS)
        self.assertIn("E6", EVIDENCE_LADDER_TIERS)
        self.assertEqual(EVIDENCE_LADDER_TIERS["E0"]["rigor_rank"], 0)
        self.assertEqual(EVIDENCE_LADDER_TIERS["E6"]["rigor_rank"], 6)
        self.assertTrue(EVIDENCE_LADDER_TIERS["E6"]["human_evidence"])
        self.assertFalse(EVIDENCE_LADDER_TIERS["E0"]["human_evidence"])

        # Check provenance registry has required fields
        asg_claims = ClinicalTruthFirewall.PROVENANCE_REGISTRY.get("ASGANDH_CYP3A4")
        self.assertIsNotNone(asg_claims)
        c = asg_claims[0]
        self.assertEqual(c.evidence_level, "E2")
        self.assertIn("Savai et al.", c.source_citation)
        self.assertIn("HepG2", c.exact_passage)
        self.assertEqual(c.applicability, "IN_VITRO_ONLY")
        self.assertGreater(c.confidence_score, 0.5)

    def test_02_clinical_truth_firewall_fail_closed_and_safety(self):
        """P0-2: Clinical Truth Firewall Fail-Closed Gate & Contraindication Defense"""
        # Unknown claim -> MUST fail-closed
        res_unknown = ClinicalTruthFirewall.evaluate_claim("NON_EXISTENT_HERB_CLAIM")
        self.assertFalse(res_unknown["firewall_pass"])
        self.assertEqual(res_unknown["status"], "INSUFFICIENT_EVIDENCE")
        self.assertIn("Insufficient verified evidence", res_unknown["verdict_statement"])
        self.assertFalse(res_unknown["action_permitted"])
        self.assertTrue(res_unknown["requires_human_clinician_signoff"])

        # Verified claim with pregnant patient context -> Contraindication block
        res_preg = ClinicalTruthFirewall.evaluate_claim("ASGANDH_CYP3A4", {"is_pregnant": True})
        self.assertFalse(res_preg["firewall_pass"])
        self.assertEqual(res_preg["status"], "SAFETY_CONTRAINDICATION_PREGNANCY")
        self.assertIn("CONTRAINDICATED IN PREGNANCY", res_preg["verdict_statement"])

        # Verified standard claim -> Advisory permitted
        res_ok = ClinicalTruthFirewall.evaluate_claim("ASGANDH_CYP3A4", {"is_pregnant": False})
        self.assertTrue(res_ok["firewall_pass"])
        self.assertEqual(res_ok["status"], "EVIDENCE_VERIFIED_ADVISORY_ONLY")
        self.assertTrue(res_ok["requires_human_clinician_signoff"])

    def test_03_tripartite_separation_architecture(self):
        """P0-3: Classical vs Modern Evidence vs ZAYVORA Interpretation vs Clinical Status"""
        unit = ClinicalTruthFirewall.get_tripartite_separation("Asgandh Nagori")
        self.assertIsInstance(unit, TripartiteKnowledgeUnit)
        self.assertIn("Muqawwi-e-Aam", unit.classical_unani["indication"])
        self.assertIn("Makhzan al-Adwiya", unit.classical_unani["canonical_sources"][0])
        self.assertIn("E5", unit.modern_evidence["evidence_tier"])
        self.assertIn("cortisol", unit.modern_evidence["established_findings"])
        self.assertIn("Neuro-Endocrine-Immune", unit.zayvora_interpretation["axis_hypothesis"])
        self.assertIn("SUFFICIENT_FOR_ADJUNCTIVE_CARE", unit.clinical_status["evidence_sufficiency"])

    def test_04_scientifically_honest_mizaj_framework(self):
        """P0-4: Traditional construct distinguished from Modern biomarkers and Hypothesis"""
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM mizaj_research_cohorts WHERE patient_id = 'PAT-0814'")
            row = cur.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row["patient_clinical_phenotype"], "Balghami Barid-Ratb Phenotype with Chronic Hyperuricemic Joint Arthropathy")
            self.assertGreaterEqual(row["inter_rater_reliability_kappa"], 0.85)

            trad = json.loads(row["traditional_construct_json"])
            self.assertEqual(trad["mizaj_type"], "Balghami")
            self.assertIn("Batee", trad["nabz"]["type"])

            labs = json.loads(row["lab_variables_json"])
            self.assertIn("hs_crp", labs)
            self.assertIn("uric_acid", labs)

            # Hypothesis status verified
            self.assertEqual(row["validation_status"], "PROSPECTIVE_COHORT_OBSERVATION")
            self.assertIn("correlates with", row["statistical_association_hypothesis"])

    def test_05_patient_360_center_of_gravity(self):
        """P0-5: Patient 360 integrates identity, consent, timeline, outcomes, mizaj, and evidence"""
        p360 = _build_patient_360_v2("PAT-0814")
        self.assertEqual(p360["center_of_gravity"], "PATIENT_CENTRIC_OS_V2")
        self.assertEqual(p360["identity"]["mrn"], "MRN-2026-0814")
        self.assertTrue(p360["is_demo_patient"])
        self.assertEqual(p360["demo_sandbox_badge"], "DEMO SANDBOX — NOT REAL PATIENT INFORMATION")

        # Longitudinal timeline linked
        self.assertGreaterEqual(len(p360["longitudinal_timeline"]), 8)
        # Consent engine linked
        self.assertGreaterEqual(len(p360["consent_engine"]), 3)
        # Clinical outcomes linked
        self.assertGreaterEqual(len(p360["clinical_outcomes"]), 4)
        # Mizaj research linked
        self.assertIn("Balghami", p360["mizaj_research_profile"]["traditional_construct"]["dominant_mizaj"])
        # Evidence used citations linked
        self.assertGreaterEqual(len(p360["evidence_provenance_used"]), 1)
        self.assertEqual(p360["evidence_provenance_used"][0]["claim_id"], "PRV-SUR-001")

    def test_06_longitudinal_clinical_timeline_progression(self):
        """P0-6: Chronological event progression from OPD to 12-week RWE milestone"""
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT event_timestamp, event_type, title, clinical_summary, metrics_json 
                FROM longitudinal_clinical_timeline 
                WHERE patient_id = 'PAT-0814' 
                ORDER BY event_timestamp ASC
            """)
            events = cur.fetchall()
            self.assertEqual(len(events), 8)
            types = [e["event_type"] for e in events]
            self.assertEqual(types, [
                "OPD_INITIAL", "MIZAJ_ASSESSMENT", "LAB_DIAGNOSTICS", "EVIDENCE_REVIEW",
                "PRESCRIPTION_SIGNED", "FOLLOW_UP_OPD", "LAB_UPDATE", "OUTCOME_MILESTONE"
            ])

            # Check outcome milestone metrics
            last_metric = json.loads(events[-1]["metrics_json"])
            self.assertEqual(last_metric["vas_pain"], 3.0)
            self.assertEqual(last_metric["rwe_grade"], "RWE_E4")

    def test_07_hakeem_sahab_v2_clinical_copilot_advisory(self):
        """P0-7: Copilot generates advisory only; zero autonomous prescription authoring"""
        ctx = {
            "primary_complaint": "Bilateral knee arthralgia",
            "current_medications": ["Aspirin 75mg"],
            "allergies": "Penicillin",
            "egfr": None  # Missing renal function!
        }
        advisory = ClinicalTruthFirewall.generate_clinical_copilot_advisory(ctx, "What should I prescribe?")
        self.assertIsInstance(advisory, ClinicalCopilotAdvisory)
        self.assertFalse(advisory.prescription_generated)
        self.assertTrue(advisory.doctor_decision_required)
        self.assertGreaterEqual(len(advisory.evidence_sources_found), 3)
        self.assertGreaterEqual(len(advisory.safety_considerations_identified), 2)
        self.assertGreaterEqual(len(advisory.potential_herb_drug_interactions), 1)
        self.assertTrue(any("Serum Creatinine" in m for m in advisory.missing_clinical_information))
        self.assertTrue(any("NO PRESCRIPTION IS GENERATED BY AI" in s for s in advisory.suggested_next_steps))

    def test_08_explicit_uncertainty_engine(self):
        """P0-8: Uncertainty evaluation with confidence %, evidence strength, completeness, contradictions"""
        eval_res = ClinicalTruthFirewall.evaluate_claim("ASGANDH_CYP3A4", {"renal_function_egfr": 90})
        unc = eval_res["uncertainty"]
        self.assertIn("overall_confidence_pct", unc)
        self.assertIn("evidence_strength", unc)
        self.assertIn("data_completeness", unc)
        self.assertIn("patient_uncertainty", unc)
        self.assertEqual(unc["final_authority"], "LICENSED_CLINICIAN")

    def test_09_longitudinal_pharmacovigilance_registry(self):
        """P0-10: First-class Pharmacovigilance tracking exposure, symptoms, causality, action, outcome"""
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM pharmacovigilance_longitudinal_registry WHERE patient_id = 'PAT-0814'")
            row = cur.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row["substance_or_pair"], "Majun Suranjan + Aspirin 75mg")
            self.assertEqual(row["interaction_category"], "DRUG_HERB_PHARMACODYNAMIC")
            self.assertEqual(row["causality_assessment"], "POSSIBLE_ADDITIVE_GASTRIC_IRRITATION")
            self.assertEqual(row["outcome"], "SYMPTOM_COMPLETELY_RESOLVED")

    def test_10_consent_engine_and_audit_ledger(self):
        """P0-13 & P0-14: Granular Consent Engine and Cryptographic Audit Ledger"""
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM consent_engine_records WHERE patient_id = 'PAT-0814'")
            consents = cur.fetchall()
            self.assertEqual(len(consents), 3)
            for c in consents:
                self.assertIsNotNone(c["signature_hash"])
                self.assertIn(c["consent_type"], ("CLINICAL_TREATMENT", "AI_PROCESSING", "RWE_RESEARCH_REGISTRY"))

    def test_11_real_world_evidence_and_outcomes_engine(self):
        """P0-15: Longitudinal outcomes measuring VAS, adherence, QoL, and RWE grade"""
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM clinical_outcomes_registry WHERE patient_id = 'PAT-0814' ORDER BY recorded_at ASC")
            outcomes = cur.fetchall()
            self.assertEqual(len(outcomes), 4)

            # Week 0 baseline vs Week 12 milestone
            baseline = outcomes[0]
            milestone = outcomes[-1]
            self.assertEqual(baseline["symptom_vas_score"], 8.0)
            self.assertEqual(milestone["symptom_vas_score"], 3.0)
            self.assertEqual(baseline["quality_of_life_score"], 38.0)
            self.assertEqual(milestone["quality_of_life_score"], 82.0)
            self.assertEqual(milestone["evidence_grade_generated"], "RWE_E4")

    def test_12_clinical_validation_benchmarks(self):
        """P0-16: 5 Gold-Standard Benchmark Cases (BM-001 - BM-005)"""
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT case_id, domain, gold_standard_answer_json FROM clinical_validation_benchmarks ORDER BY case_id ASC")
            benchmarks = cur.fetchall()
            self.assertEqual(len(benchmarks), 5)
            ids = [b["case_id"] for b in benchmarks]
            self.assertEqual(ids, ["BM-001", "BM-002", "BM-003", "BM-004", "BM-005"])

            bm2 = json.loads(benchmarks[1]["gold_standard_answer_json"])
            self.assertFalse(bm2["autonomous_prescription_allowed"])

            bm5 = json.loads(benchmarks[4]["gold_standard_answer_json"])
            self.assertFalse(bm5["prescription_generated"])
            self.assertTrue(bm5["doctor_decision_required"])

    def test_13_defensible_regulatory_language_in_html(self):
        """P0-11: No unvalidated compliance claims in user-facing templates"""
        html_path = os.path.join(BASE_DIR, "app.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Overclaims must NOT exist
        self.assertNotIn("DPDP Act 2023 &amp; ABDM Compliant", html)
        self.assertNotIn("21 CFR Part 11 Certified", html)

        # Defensible language MUST exist
        self.assertIn("DPDP-ready architecture &amp; ABDM integration-ready", html)
        self.assertIn("21 CFR Part 11–aligned controls", html)

    def test_14_9_hub_navigation_structure(self):
        """P0-17: 9-Hub UI Architecture Navigation present in HTML and JS"""
        html_path = os.path.join(BASE_DIR, "app.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn('id="zayvora-v2-master-nav"', html)
        self.assertIn('navigateToV2Hub(\'command_center\')', html)
        self.assertIn('navigateToV2Hub(\'patients\')', html)
        self.assertIn('navigateToV2Hub(\'clinical\')', html)
        self.assertIn('navigateToV2Hub(\'zmie\')', html)
        self.assertIn('navigateToV2Hub(\'pharmacy\')', html)
        self.assertIn('navigateToV2Hub(\'formulation\')', html)
        self.assertIn('navigateToV2Hub(\'outcomes\')', html)
        self.assertIn('navigateToV2Hub(\'research\')', html)
        self.assertIn('navigateToV2Hub(\'admin\')', html)

        js_path = os.path.join(BASE_DIR, "js", "zayvora-core.js")
        with open(js_path, "r", encoding="utf-8") as f:
            js = f.read()
        self.assertIn("function navigateToV2Hub(hub)", js)


if __name__ == "__main__":
    unittest.main()
