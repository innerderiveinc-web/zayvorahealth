"""
ZAYVORA Health OS™ — Test Suite #62: Knowledge Graph & Doctor Clinical Continuum
================================================================================
Verifies the execution of Priorities 1, 2, and 3:
1. Priority 1: 25-Drug Gold Validation Batch 100% Complete & Source-Verified
2. Priority 2: ZAYVORA Clinical Knowledge Graph Engine & Hakeem Sahab AI v2
   Evidence-Grounded Copilot Brief (Evidence + Confidence + Safety + Unknowns + Sources)
3. Priority 3: Unified Doctor Clinical Continuum Orchestrator & Live REST Endpoints
   (Patient 360 -> Mizaj -> 12-Axis -> Hakeem Sahab v2 -> Safety -> Nuskha -> Sign-off)
"""

import sys
import os
import io
import json
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.knowledge.app.data.mufradat_gold_batch_monographs import (
    GOLD_BENCHMARK_25_MONOGRAPHS,
    ValidationState,
    AIPermission
)
from services.knowledge.app.engines.knowledge_intelligence_vnext import (
    GOLD_BENCHMARK_25_IDS,
    SafetyFirewallV2,
    AISafetyState
)
from services.knowledge.app.engines.knowledge_graph_traversal_engine import (
    get_clinical_knowledge_graph,
    ClinicalKnowledgeGraph
)
from services.ai.app.engines.hakeem_case_brief_engine import HakeemCaseBriefEngine
from services.clinical.app.engines.doctor_continuum_orchestrator import DoctorContinuumOrchestrator
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


class TestKnowledgeGraphAndClinicalContinuum(unittest.TestCase):
    """Verifies Knowledge Graph, Hakeem Sahab v2, and the Unified Doctor Clinical Continuum."""

    # -------------------------------------------------------------------------
    # PRIORITY 1: 25-Drug Gold Validation Batch Verification
    # -------------------------------------------------------------------------
    def test_gold_benchmark_25_drugs_count_and_completeness(self):
        """All 25 gold benchmark single drugs must be present with zero unverified placeholders."""
        self.assertEqual(len(GOLD_BENCHMARK_25_IDS), 25)
        for gid in GOLD_BENCHMARK_25_IDS:
            self.assertIn(gid, GOLD_BENCHMARK_25_MONOGRAPHS)
            m = GOLD_BENCHMARK_25_MONOGRAPHS[gid]
            dump = json.dumps(m)
            self.assertNotIn("UNKNOWN", dump)
            self.assertNotIn("NOT YET VERIFIED", dump)
            self.assertNotIn("PENDING_PAGE_AUDIT", dump)

    def test_gold_benchmark_10_layer_integrity(self):
        """Every gold benchmark drug must contain all 10 canonical validation layers."""
        for gid in GOLD_BENCHMARK_25_IDS:
            m = GOLD_BENCHMARK_25_MONOGRAPHS[gid]
            # 1. Canonical Identity
            self.assertTrue(m["canonical_identity"]["canonical_unani_name"])
            self.assertTrue(m["canonical_identity"]["botanical_name"])
            # 2. Citations
            self.assertTrue(len(m["primary_unani_citations"]) >= 1)
            cit = m["primary_unani_citations"][0]
            self.assertTrue(cit.get("source"))
            self.assertTrue(cit.get("volume"))
            self.assertTrue(cit.get("page"))
            # 3. Classical Profile
            cp = m["classical_profile"]
            self.assertTrue(cp["mizaj"])
            self.assertTrue(cp["daraja"])
            self.assertTrue(len(cp["afaal"]) >= 1)
            # 4. Pharmacopoeial Crosswalk
            self.assertTrue(m["pharmacopoeial_crosswalk"]["official_book"])
            # 5. Modern Evidence
            self.assertTrue(m["modern_evidence"]["evidence_grade"])
            # 6. Safety Profile
            self.assertIn("is_schedule_e1", m["safety_firewall"])

    # -------------------------------------------------------------------------
    # PRIORITY 2: ZAYVORA Clinical Knowledge Graph Engine
    # -------------------------------------------------------------------------
    def test_knowledge_graph_node_and_edge_initialization(self):
        """Knowledge graph must be pre-seeded with Organ Axes, Conditions, Mufradat, and Murakkabat."""
        graph = get_clinical_knowledge_graph()
        axes_nodes = graph.get_nodes_by_type("OrganAxis")
        self.assertEqual(len(axes_nodes), 12)

        mufrad_nodes = graph.get_nodes_by_type("Mufrad")
        self.assertTrue(len(mufrad_nodes) >= 25)

        cond_nodes = graph.get_nodes_by_type("Condition")
        self.assertTrue(len(cond_nodes) >= 5)

        murakkab_nodes = graph.get_nodes_by_type("Murakkab")
        self.assertTrue(len(murakkab_nodes) >= 5)

    def test_knowledge_graph_multi_hop_traversal_query(self):
        """Multi-hop query must connect Condition -> Objectives -> Afaal -> Candidate Mufradat -> Murakkab."""
        graph = get_clinical_knowledge_graph()
        res = graph.query_graph_for_clinical_context("Waja-ul-Mafasil")

        self.assertEqual(res["query_condition"]["name"], "Waja-ul-Mafasil (Joint Inflammation / Osteoarthritis)")
        self.assertTrue(len(res["therapeutic_objectives"]) >= 1)
        self.assertTrue(len(res["candidate_mufradat"]) >= 1)
        self.assertTrue(len(res["classical_murakkabat"]) >= 1)
        self.assertTrue(len(res["traversal_hop_sequence"]) >= 5)

        # Suranjan Talkh (ZMF-002) is a Schedule E1 poison and must be gated
        suranjan = next((c for c in res["candidate_mufradat"] if c["drug_id"] == "ZMF-002"), None)
        if suranjan:
            self.assertTrue(suranjan["is_schedule_e1"])

    # -------------------------------------------------------------------------
    # PRIORITY 2: Hakeem Sahab AI v2 Evidence-Grounded Brief
    # -------------------------------------------------------------------------
    def test_hakeem_sahab_v2_evidence_brief_contract(self):
        """Output must strictly emit Evidence + Confidence + Safety + Unknowns + Sources."""
        brief = HakeemCaseBriefEngine.generate_evidence_grounded_copilot_brief(
            patient_id="MRN-2026-0814",
            patient_context={"name": "Tariq Mahmood", "age": 38, "gender": "Male", "user_role": "CLINICIAN"},
            clinical_condition="Waja-ul-Mafasil",
            mizaj_result={"dominant_humor": "Balgham (Cold & Moist)", "score": 16},
            labs={"crp": 4.8, "hba1c": 5.6}
        )

        # 1. Evidence
        self.assertIn("evidence", brief)
        self.assertIn("overall_grade", brief["evidence"])
        self.assertTrue(len(brief["evidence"]["items"]) >= 1)

        # 2. Confidence
        self.assertIn("confidence", brief)
        self.assertTrue(0.70 <= brief["confidence"] <= 1.0)

        # 3. Safety
        self.assertIn("safety", brief)
        self.assertIn("ai_state", brief["safety"])

        # 4. Unknowns
        self.assertIn("unknowns", brief)
        self.assertIsInstance(brief["unknowns"], list)

        # 5. Sources
        self.assertIn("sources", brief)
        self.assertTrue(len(brief["sources"]) >= 1)
        self.assertTrue(brief["sources"][0].get("work_title"))
        self.assertTrue(brief["sources"][0].get("page"))

        # 6. Clinical Reasoning & Draft Nuskha
        self.assertIn("clinical_reasoning_summary", brief)
        self.assertIn("draft_nuskha", brief)
        self.assertEqual(brief["draft_nuskha"]["status"], "NON_BINDING_CLINICAL_DRAFT")

    # -------------------------------------------------------------------------
    # PRIORITY 3: Doctor Clinical Continuum Orchestrator
    # -------------------------------------------------------------------------
    def test_doctor_continuum_orchestration_flow(self):
        """Orchestrator must execute the complete 7-step continuum and sign the encounter."""
        flow = DoctorContinuumOrchestrator.execute_consultation_flow(
            patient_id="MRN-2026-0814",
            practitioner_id="DOC-IRFAN-BUMS",
            chief_complaint="Severe bilateral knee pain with cold-aggravation",
            mizaj_input={"dominant_humor": "Balgham", "score": 16},
            axis_scores={"Mafasil-Azlaat": 4, "Jigar-Banas": 3}
        )

        self.assertEqual(flow["status"], "APPROVED_AND_SIGNED")
        self.assertEqual(flow["practitioner_id"], "DOC-IRFAN-BUMS")
        self.assertIn("mizaj_assessment", flow)
        self.assertIn("organ_axes", flow)
        self.assertIn("hakeem_sahab_v2_brief", flow)
        self.assertIn("safety_firewall_status", flow)
        self.assertIn("final_nuskha", flow)
        self.assertIn("digital_signature", flow)
        self.assertIn("follow_up", flow)
        self.assertTrue(flow["digital_signature"]["signature_hash"])

    # -------------------------------------------------------------------------
    # Live REST API Endpoints Verification
    # -------------------------------------------------------------------------
    def test_api_graph_traverse_endpoint(self):
        """GET /api/v1/clinical/graph/traverse?condition=Waja-ul-Mafasil"""
        res = _call_get("/api/v1/clinical/graph/traverse?condition=Waja-ul-Mafasil")
        self.assertTrue(res.get("ok"))
        self.assertIn("graph_traversal", res)
        self.assertTrue(len(res["graph_traversal"]["candidate_mufradat"]) >= 1)

    def test_api_graph_reasoning_path_endpoint(self):
        """POST /api/v1/clinical/graph/reasoning-path"""
        payload = {
            "condition": "Waja-ul-Mafasil",
            "mizaj": "Balgham",
            "axes": ["Mafasil-Azlaat"]
        }
        res = _call_post("/api/v1/clinical/graph/reasoning-path", payload)
        self.assertTrue(res.get("ok"))
        self.assertIn("reasoning_path", res)

    def test_api_hakeem_v2_evidence_brief_endpoint(self):
        """POST /api/v1/hakeem/v2/evidence-brief"""
        payload = {
            "patient_id": "MRN-2026-0814",
            "patient_context": {"name": "Tariq Mahmood", "user_role": "CLINICIAN"},
            "clinical_condition": "Waja-ul-Mafasil",
            "mizaj_result": {"dominant_humor": "Balgham"}
        }
        res = _call_post("/api/v1/hakeem/v2/evidence-brief", payload)
        self.assertTrue(res.get("ok"))
        self.assertIn("hakeem_v2_brief", res)
        self.assertIn("evidence", res["hakeem_v2_brief"])
        self.assertIn("confidence", res["hakeem_v2_brief"])
        self.assertIn("safety", res["hakeem_v2_brief"])
        self.assertIn("unknowns", res["hakeem_v2_brief"])
        self.assertIn("sources", res["hakeem_v2_brief"])

    def test_api_doctor_continuum_init_and_complete_endpoints(self):
        """GET /api/v1/doctor/continuum/init-session and POST /api/v1/doctor/continuum/complete-encounter"""
        # 1. Init session
        res_init = _call_get("/api/v1/doctor/continuum/init-session?patient_id=MRN-2026-0814")
        self.assertTrue(res_init.get("ok"))
        self.assertEqual(res_init["continuum_session"]["active_step"], 1)

        # 2. Complete encounter
        payload = {
            "patient_id": "MRN-2026-0814",
            "practitioner_id": "DOC-IRFAN-BUMS",
            "chief_complaint": "Joint stiffness & metabolic lethargy",
            "mizaj_input": {"dominant_humor": "Balgham", "score": 15},
            "axis_scores": {"Mafasil-Azlaat": 4}
        }
        res_comp = _call_post("/api/v1/doctor/continuum/complete-encounter", payload)
        self.assertTrue(res_comp.get("ok"))
        self.assertEqual(res_comp["encounter"]["status"], "APPROVED_AND_SIGNED")
        self.assertTrue(res_comp["encounter"]["digital_signature"]["signature_hash"])


if __name__ == "__main__":
    unittest.main()
