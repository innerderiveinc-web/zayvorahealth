"""
ZAYVORA Health OS™ — Test Suite #60: End-to-End Matab Clinical Simulation
==========================================================================
Simulates the complete patient consultation and governance flow:
  1. Complete 250-Drug Master Monograph Matrix coverage & integrity.
  2. Multi-Disciplinary 5-Role Clinician Sign-Off & Legal Certificate generation.
  3. Real-World Matab Clinical Case Simulation:
     - Patient: Mohd. Zubair (52M), Acute Gout / Waja-ul-Mafasil.
     - Intercept Schedule E(1) toxic request (Suranjan Talkh).
     - Advisory suggests classical Badal (Chob Zard / Haldi + Ajwain Desi).
     - Custom Nuskha formulated & audited against 60 Core Monographs.
     - 5-expert multi-sign-off recorded -> Legal SHA-256 Certificate generated.
     - Bilingual Patient Monograph Card generated with governance disclaimer.
  4. Live REST API verification.
"""
import sys
import os
import io
import json
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.knowledge.app.data.mufradat_250_monograph_matrix import Master250MonographMatrix
from services.clinical.app.engines.clinical_multisignoff_engine import ClinicalMultiSignoffEngine, SIGN_OFF_ROLES
from services.therapeutic.app.engines.safety_firewall import run_safety_firewall
from services.therapeutic.app.engines.badal_e_advia_engine import BadalEAdviaEngine
from services.therapeutic.app.engines.validated_murakkab_compiler import ValidatedMurakkabCompiler
from services.knowledge.app.engines.mufradat_card_generator import MufradatCardGenerator
from services.live_api_server import ZayvoraApiHandler


def _call_get(path):
    req = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
    req.path = path
    req.headers = {}
    req.request_version = "HTTP/1.1"
    req.wfile = io.BytesIO()
    req.log_request = lambda *a, **k: None
    req.do_GET()
    raw = req.wfile.getvalue().decode()
    body = raw.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in raw else raw
    return json.loads(body)


def _call_post(path, payload):
    data = json.dumps(payload).encode()
    req = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
    req.path = path
    req.headers = {"Content-Length": str(len(data))}
    req.request_version = "HTTP/1.1"
    req.rfile = io.BytesIO(data)
    req.wfile = io.BytesIO()
    req.log_request = lambda *a, **k: None
    req.do_POST()
    raw = req.wfile.getvalue().decode()
    body = raw.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in raw else raw
    return json.loads(body)


class TestEndToEndMatabSimulation(unittest.TestCase):
    """End-to-End Clinical Verification & Realistic Patient Journey."""

    def test_complete_250_monograph_matrix_statistics(self):
        """350 catalog must report 100% coverage with zero unindexed gaps."""
        stats = Master250MonographMatrix.get_catalog_statistics()
        self.assertEqual(stats["total_monographs"], 350)
        self.assertEqual(stats["coverage_percent"], 100.0)
        self.assertGreaterEqual(stats["schedule_e1_hard_blocked"], 26)

    def test_multi_disciplinary_signoff_lifecycle(self):
        """Full 5-role sign-off produces tamper-evident certificate."""
        rx_id = "RX-2026-TEST-99"
        # Initial status: not certified
        initial_cert = ClinicalMultiSignoffEngine.get_audit_certificate(rx_id)
        self.assertFalse(initial_cert["certified"])
        self.assertEqual(len(initial_cert["pending_roles"]), 5)

        # Record 4 roles -> still incomplete
        for role in SIGN_OFF_ROLES[:4]:
            ClinicalMultiSignoffEngine.record_expert_signoff(
                target_id=rx_id, target_type="PRESCRIPTION",
                role=role, expert_name=f"Expert {role}",
                expert_credentials="BUMS / MD"
            )
        mid_cert = ClinicalMultiSignoffEngine.get_audit_certificate(rx_id)
        self.assertFalse(mid_cert["certified"])

        # Record final 5th role (Chief Unani Clinician) -> certified!
        final_res = ClinicalMultiSignoffEngine.record_expert_signoff(
            target_id=rx_id, target_type="PRESCRIPTION",
            role=SIGN_OFF_ROLES[4], expert_name="Hakeem M. Tariq",
            expert_credentials="Senior Professor & Chief Clinician"
        )
        self.assertTrue(final_res["is_fully_certified"])
        self.assertIsNotNone(final_res["certificate_hash"])

        final_cert = ClinicalMultiSignoffEngine.get_audit_certificate(rx_id)
        self.assertTrue(final_cert["certified"])
        self.assertIn("ZAYVORA Health OS™ Certified", final_cert["legal_authority"])

    def test_clinical_case_study_acute_gout_pipeline(self):
        """
        Complete Patient Consultation Flow:
        Mohd. Zubair (52M) - Acute Gout & Joint Inflammation.
        """
        # Step 1: Doctor attempts to add raw Suranjan Talkh (ZMF-002)
        patient_ctx = {
            "patient_id": "PT-MZ-52M",
            "age": 52,
            "gender": "male",
            "chief_complaint": "Severe 1st MTP joint pain & swelling, hyperuricemia",
            "diagnosis": "Waja-ul-Mafasil / Niqris (Acute Gout)",
            "selected_ingredients": [
                {"name": "Suranjan Talkh", "zmf_id": "ZMF-002", "shodhana_certified": False}
            ]
        }
        # Run Safety Firewall
        fw_verdict = run_safety_firewall(
            patient_context=patient_ctx,
            ingredients=patient_ctx["selected_ingredients"]
        )
        self.assertEqual(fw_verdict["verdict"], "DO_NOT_RECOMMEND")
        self.assertTrue(any("ZMF-002" in r for r in fw_verdict["reasons"]))

        # Step 2: System queries Badal-e-Advia for non-toxic substitute
        badal_res = BadalEAdviaEngine.get_badal_recommendations(
            ingredient_name="Suranjan Talkh",
            zmf_id="ZMF-002",
            indication="Niqris",
            patient_mizaj="Haar"
        )
        self.assertTrue(badal_res["is_high_risk_blocked"])
        self.assertGreater(len(badal_res["classical_substitutes"]), 0)
        top_substitute = badal_res["classical_substitutes"][0]["name"]
        self.assertIn("Haldi", top_substitute)

        # Step 3: Clinician formulates safe replacement nuskha
        safe_nuskha = [
            {"zmf_id": "ZMF-057", "name": "Chob Zard (Haldi)", "role": "Juz-e-Azam"},
            {"zmf_id": "ZMF-001", "name": "Asgandh", "role": "Muawin"},
            {"zmf_id": "ZMF-016", "name": "Zanjabeel", "role": "Muawin"},
            {"zmf_id": "ZMF-024", "name": "Badiyan", "role": "Musleh"}
        ]
        audit_res = ValidatedMurakkabCompiler.audit_custom_nuskha(
            "Nuskha-e-Mafasil Motadil (Patient Mohd. Zubair)",
            safe_nuskha
        )
        self.assertEqual(audit_res["audit_verdict"], "APPROVED_CLINICAL_NUSKHA")
        self.assertTrue(audit_res["ai_autonomous_permitted"])

        # Step 4: Multi-sign-off certificate recorded
        for role in SIGN_OFF_ROLES:
            ClinicalMultiSignoffEngine.record_expert_signoff(
                target_id="PT-MZ-52M-RX01", target_type="PRESCRIPTION",
                role=role, expert_name=f"Consultant {role}",
                expert_credentials="MD / BUMS"
            )
        rx_cert = ClinicalMultiSignoffEngine.get_audit_certificate("PT-MZ-52M-RX01")
        self.assertTrue(rx_cert["certified"])

        # Step 5: Generate patient education card for Asgandh (ZMF-001)
        asgandh_card = MufradatCardGenerator.generate_card("ZMF-001")
        self.assertEqual(asgandh_card["zmf_id"], "ZMF-001")
        self.assertIn("governance", asgandh_card)
        self.assertIn("footer", asgandh_card["governance"])

    def test_api_catalog_stats_endpoint(self):
        """GET /api/v1/knowledge/mufradat-250/catalog-stats returns 350 stats."""
        resp = _call_get("/api/v1/knowledge/mufradat-250/catalog-stats")
        self.assertTrue(resp.get("ok"))
        self.assertEqual(resp["stats"]["total_monographs"], 350)

    def test_api_signoff_certificate_endpoint(self):
        """GET /api/v1/governance/signoff/certificate/{target_id} returns certificate."""
        resp = _call_get("/api/v1/governance/signoff/certificate/ZMF-001")
        self.assertTrue(resp.get("ok"))
        self.assertIn("audit_certificate", resp)

    def test_api_signoff_record_post_endpoint(self):
        """POST /api/v1/governance/signoff/record records expert sign-off."""
        payload = {
            "target_id": "API-TEST-PRESCRIPTION-01",
            "target_type": "PRESCRIPTION",
            "role": "TOXICOLOGIST_SAFETY_OFFICER",
            "expert_name": "Dr. A. Qadir",
            "expert_credentials": "PhD Toxicology",
            "comments": "No toxic substances found."
        }
        resp = _call_post("/api/v1/governance/signoff/record", payload)
        self.assertTrue(resp.get("ok"))
        self.assertEqual(resp["signoff_result"]["role"], "TOXICOLOGIST_SAFETY_OFFICER")

    def test_system_provenance_and_data_truth_endpoint(self):
        """GET /api/v1/system/provenance returns honest environment metadata and zero-mock guarantee."""
        resp = _call_get("/api/v1/system/provenance")
        self.assertTrue(resp.get("ok"))
        self.assertIn("provenance_metadata", resp)
        self.assertIn("environment", resp["provenance_metadata"])
        self.assertEqual(resp["provenance_metadata"]["environment"]["value"], "DEVELOPMENT_DEMO_FIXTURES")
        self.assertIn("Zero hallucinated citations", resp["data_truth_guarantee"])


    def test_classical_unani_research_coverage_across_all_250_drugs(self):
        """All 350 drugs have verified classical citations, Mizaj, Afaal, Musleh, and Badal with zero unverified placeholders."""
        from services.knowledge.app.data.mufradat_250_monograph_matrix import _MASTER_250_CATALOG
        self.assertEqual(len(_MASTER_250_CATALOG), 350)

        for did, mono in _MASTER_250_CATALOG.items():
            citations = mono.get("primary_unani_citations", [])
            self.assertGreaterEqual(len(citations), 1, f"Missing citation for {did}")
            
            # Check citations have authentic references and no raw placeholders
            for c in citations:
                self.assertNotIn("UNKNOWN / NOT YET VERIFIED", str(c))
                self.assertNotIn("PENDING_PAGE_AUDIT", str(c))
                self.assertNotIn("Prof. Hakeem M. Tariq", c.get("reviewer", ""))
                self.assertTrue(any(src in c.get("source", "") for src in ["Khazain-ul-Advia", "Makhzan", "Bustan", "Al-Qanoon", "Kitab", "Ibn", "Al-Hawi"]))

            # Verify classical profile integrity
            cp = mono.get("classical_profile", {})
            self.assertTrue(cp.get("mizaj"), f"Missing mizaj for {did}")
            self.assertTrue(cp.get("afaal"), f"Missing afaal for {did}")
            self.assertTrue(cp.get("musleh"), f"Missing musleh for {did}")
            self.assertTrue(cp.get("badal"), f"Missing badal for {did}")

        # Ensure candidate queue is completely cleared
        stats = Master250MonographMatrix.get_catalog_statistics()
        self.assertEqual(stats["tier_3_candidate_queue"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

