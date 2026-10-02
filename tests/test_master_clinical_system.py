"""
ZAYVORA Health OS™ — Master Clinical Knowledge & Runtime Verification Suite
===========================================================================
Comprehensive automated test suite covering:
1. 12 Canonical Organ Axes & Scoring Engine (0-5 scale, primary/secondary)
2. 21 Clinical Protocols (P-01 to P-21, 3-phase progression)
3. 32 Compliance-Corrected Products (ZAY-001 to ZAY-032, Section A/B/C)
4. 21 Protocol Kits (K-01 to K-21, 3-product stacks & monthly pricing)
5. 8 Parhez Lifestyle Protocols (MF-01 to Resp-01)
6. 30-Point 6-Domain Z-MAI Assessment Tool
7. Drug-Herb Interaction Matrix & Universal Contraindications
8. Four-Tier Nuskha Architecture (80/20 rule & toxic substance safety)
9. Live REST API Server Endpoints for Clinical Knowledge
"""

import unittest
import json
import sqlite3
import os

from services.knowledge.app.data.organ_axes_master import (
    MASTER_ORGAN_AXES,
    score_organ_axes,
    get_all_axes,
    get_axis_by_id
)
from services.knowledge.app.data.protocols_master import (
    MASTER_PROTOCOLS,
    get_all_protocols,
    get_protocol_by_id,
    get_protocols_by_category,
    get_protocol_for_axis
)
from services.knowledge.app.data.products_master import (
    MASTER_PRODUCTS,
    get_all_products,
    get_product_by_sku,
    get_products_by_axis,
    get_rx_products
)
from services.knowledge.app.data.kits_master import (
    MASTER_KITS,
    get_all_kits,
    get_kit_by_id,
    get_kits_by_protocol
)
from services.knowledge.app.data.parhez_master import (
    MASTER_PARHEZ,
    get_all_parhez,
    get_parhez_by_code,
    get_parhez_for_axis
)
from services.knowledge.app.data.drug_interactions_master import (
    MASTER_INTERACTIONS,
    UNIVERSAL_CONTRAINDICATIONS,
    check_drug_herb_interactions,
    get_all_interactions,
    get_universal_contraindications
)
from services.knowledge.app.data.zmai_scoring_tool import (
    DOMAINS,
    calculate_zmai_score,
    get_all_domains
)
from services.clinical.app.engines.organ_axis_engine import score_canonical_12_axes
from services.therapeutic.app.engines.nuskha_compiler import verify_four_tier_nuskha_architecture
from services.therapeutic.app.engines.safety_firewall import run_master_drug_herb_safety_audit
from services.clinical.app.engines.mizaj_assessor import assess_mizaj_zmai_30_point


class TestMasterOrganAxes(unittest.TestCase):
    def test_canonical_axes_count(self):
        self.assertEqual(len(MASTER_ORGAN_AXES), 12, "Must contain exactly 12 canonical organ axes")
        self.assertEqual(len(get_all_axes()), 12)

    def test_axes_data_integrity(self):
        for axis_id, data in MASTER_ORGAN_AXES.items():
            self.assertIn("arabic_name", data)
            self.assertIn("body_system", data)
            self.assertIn("governing_power", data)
            self.assertIn("key_diseases", data)
            self.assertIn("primary_products", data)
            self.assertTrue(len(data["key_diseases"]) > 0)
            self.assertTrue(len(data["primary_products"]) > 0)

    def test_axes_scoring_algorithm(self):
        # Primary axis should be highest score; secondary should be 2nd highest if >= 3
        scores = {
            "Jigar-Banas": 5,
            "Qalb-Uroq": 4,
            "Dimagh-Qalb": 2,
            "Riya-Sadr": 1
        }
        res = score_organ_axes(scores)
        self.assertEqual(res["primary_axis"], "Jigar-Banas")
        self.assertEqual(res["primary_score"], 5)
        self.assertEqual(res["secondary_axis"], "Qalb-Uroq")
        self.assertEqual(res["secondary_score"], 4)
        self.assertEqual(len(res["recommendations"]), 2)

    def test_organ_axis_engine_integration(self):
        res = score_canonical_12_axes({"Qalb-Uroq": 5, "Dimagh-Qalb": 3})
        self.assertEqual(res["primary_axis"], "Qalb-Uroq")
        self.assertEqual(res["secondary_axis"], "Dimagh-Qalb")


class TestMasterClinicalProtocols(unittest.TestCase):
    def test_protocols_count(self):
        self.assertEqual(len(MASTER_PROTOCOLS), 21, "Must contain exactly 21 clinical protocols (P-01 to P-21)")
        self.assertEqual(len(get_all_protocols()), 21)

    def test_protocols_three_phase_structure(self):
        for pid in [f"P-{i:02d}" for i in range(1, 22)]:
            proto = get_protocol_by_id(pid)
            self.assertIsNotNone(proto, f"Protocol {pid} must exist")
            self.assertIn("phase1", proto, f"{pid} must contain phase1")
            self.assertIn("phase2", proto, f"{pid} must contain phase2")
            self.assertIn("phase3", proto, f"{pid} must contain phase3")
            self.assertIn("lab_monitoring", proto)
            self.assertIn("clinical_warnings", proto)
            self.assertIn("protocol_kit_id", proto)

    def test_category_and_axis_queries(self):
        metabolic_protocols = get_protocols_by_category("METABOLIC")
        self.assertTrue(len(metabolic_protocols) >= 2)
        jigar_protocols = get_protocol_for_axis("Jigar-Banas")
        self.assertTrue(len(jigar_protocols) >= 1)


class TestMasterProductsCatalog(unittest.TestCase):
    def test_products_count(self):
        self.assertEqual(len(MASTER_PRODUCTS), 32, "Must contain all 32 compliance-corrected formulations")
        self.assertEqual(len(get_all_products()), 32)

    def test_sections_and_skus(self):
        for i in range(1, 33):
            sku = f"ZAY-{i:03d}"
            prod = get_product_by_sku(sku)
            self.assertIsNotNone(prod, f"Product {sku} must exist")
            self.assertTrue(len(prod["composition"]) >= 4, f"{sku} must have at least 4 active ingredients")
            self.assertTrue(prod["mrp_inr"] > 0)
            self.assertIn("regulatory_track", prod)

    def test_rx_products(self):
        rx_list = get_rx_products()
        rx_skus = [p["sku"] for p in rx_list]
        # HyperCalm, Night-One X, VigorX-ED require Rx
        self.assertIn("ZAY-001", rx_skus)
        self.assertIn("ZAY-009", rx_skus)
        self.assertIn("ZAY-023", rx_skus)


class TestMasterProtocolKits(unittest.TestCase):
    def test_kits_count(self):
        self.assertEqual(len(MASTER_KITS), 21, "Must contain exactly 21 protocol kits (K-01 to K-21)")
        self.assertEqual(len(get_all_kits()), 21)

    def test_kit_pricing_and_products(self):
        for i in range(1, 22):
            kid = f"K-{i:02d}"
            kit = get_kit_by_id(kid)
            self.assertIsNotNone(kit, f"Kit {kid} must exist")
            self.assertTrue(kit["monthly_price_inr"] >= 2000, f"{kid} price should be realistic")
            self.assertTrue(len(kit["products"]) >= 2, f"{kid} should have 2-3 product stack")


class TestMasterParhezProtocols(unittest.TestCase):
    def test_parhez_count(self):
        self.assertEqual(len(MASTER_PARHEZ), 8, "Must contain 8 canonical Parhez protocols")
        self.assertEqual(len(get_all_parhez()), 8)

    def test_specific_parhez_codes(self):
        codes = ["MF-01", "PC-01", "TM-01", "NE-01", "WM-01", "FK-01", "ST-01", "Resp-01"]
        for c in codes:
            pz = get_parhez_by_code(c)
            self.assertIsNotNone(pz, f"Parhez {c} must exist")
            self.assertTrue(len(pz["rules"]) >= 4, f"{c} must contain detailed clinical rules")


class TestZMAIScoringTool(unittest.TestCase):
    def test_domains_structure(self):
        self.assertEqual(len(DOMAINS), 6, "Must contain 6 clinical domains")
        total_q = sum(len(d["questions"]) for d in DOMAINS.values())
        self.assertEqual(total_q, 30, "Must contain exactly 30 validated questions")

    def test_zmai_scoring_calculation(self):
        # 30 damawi answers -> 100% Damawi
        responses = {f"q{i}_test": "damawi" for i in range(1, 31)}
        # Map to actual question IDs
        real_responses = {}
        for dom in DOMAINS.values():
            for q in dom["questions"]:
                real_responses[q["id"]] = "damawi"
        
        result = calculate_zmai_score(real_responses)
        self.assertEqual(result["dominant_mizaj"], "damawi")
        self.assertEqual(result["percentages"]["damawi"], 100.0)
        self.assertIsNotNone(result["dyscrasia"])

    def test_mizaj_assessor_engine_integration(self):
        real_responses = {}
        for dom in DOMAINS.values():
            for q in dom["questions"]:
                real_responses[q["id"]] = "safrawi"
        res = assess_mizaj_zmai_30_point(real_responses)
        self.assertEqual(res["dominant_mizaj"], "safrawi")


class TestDrugHerbInteractionsAndSafety(unittest.TestCase):
    def test_interactions_count(self):
        self.assertTrue(len(MASTER_INTERACTIONS) >= 10)

    def test_critical_interactions_detection(self):
        # Asrol + Metoprolol -> Critical hypotension
        hits = check_drug_herb_interactions(["ZAY-001"], ["Metoprolol 50mg"])
        self.assertTrue(len(hits) >= 1)
        self.assertEqual(hits[0]["severity"], "CRITICAL")

        # Guggulu + Warfarin -> Critical hemorrhage
        hits2 = check_drug_herb_interactions(["Guggulu"], ["Warfarin 5mg"])
        self.assertTrue(len(hits2) >= 1)
        self.assertEqual(hits2[0]["severity"], "CRITICAL")

    def test_safety_firewall_audit(self):
        # Pregnancy contraindication check
        audit = run_master_drug_herb_safety_audit(["ZAY-001"], ["Paracetamol"], is_pregnant=True)
        self.assertFalse(audit["is_safe"])
        self.assertEqual(audit["severity"], "CRITICAL")
        self.assertTrue(audit["requires_clinician_override"])


class TestFourTierNuskhaArchitecture(unittest.TestCase):
    def test_balanced_four_tier_nuskha(self):
        ingredients = [
            {"name": "Jamun Seed Extract", "role": "asl", "dose_mg": 400},
            {"name": "Gurmar Extract", "role": "muawwid", "dose_mg": 400},
            {"name": "Methi", "role": "musleh", "dose_mg": 100},
            {"name": "Gond Kateera", "role": "muhsin", "dose_mg": 100}
        ]
        res = verify_four_tier_nuskha_architecture(ingredients)
        self.assertEqual(res["status"], "passed")
        self.assertTrue(res["is_four_tier_complete"])
        self.assertEqual(res["therapeutic_core_pct"], 80.0)
        self.assertEqual(res["protective_buffer_pct"], 20.0)
        self.assertTrue(res["rule_80_20_compliant"])

    def test_unpurified_toxic_substance_rejection(self):
        ingredients = [
            {"name": "Raw Kuchla Seed", "role": "asl", "dose_mg": 50, "is_mudabbar": False}
        ]
        res = verify_four_tier_nuskha_architecture(ingredients)
        self.assertEqual(res["status"], "failed_safety")
        self.assertTrue(len(res["toxic_alerts"]) >= 1)


class TestDatabaseMasterTables(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(os.getcwd(), "database", "zayvora_live.db")
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_tables_populated(self):
        expected_counts = {
            "master_organ_axes": 12,
            "master_protocols": 21,
            "master_products": 32,
            "master_protocol_kits": 21,
            "master_parhez": 8
        }
        for table, expected in expected_counts.items():
            self.cur.execute(f"SELECT COUNT(*) FROM {table}")
            cnt = self.cur.fetchone()[0]
            self.assertEqual(cnt, expected, f"Table {table} must have {expected} rows, found {cnt}")



class TestLiveApiServerMasterEndpoints(unittest.TestCase):
    def setUp(self):
        from unittest.mock import MagicMock
        from services.live_api_server import ZayvoraApiHandler
        self.HandlerClass = ZayvoraApiHandler

    def _invoke(self, method, path, body=None):
        import io
        from unittest.mock import MagicMock
        if body is not None:
            raw_body = json.dumps(body).encode("utf-8")
            headers = {"Content-Length": str(len(raw_body))}
            rfile = io.BytesIO(raw_body)
        else:
            headers = {}
            rfile = io.BytesIO()

        wfile = io.BytesIO()
        handler = self.HandlerClass.__new__(self.HandlerClass)
        handler.rfile = rfile
        handler.wfile = wfile
        handler.requestline = f"{method} {path} HTTP/1.1"
        handler.command = method
        handler.path = path
        handler.request_version = "HTTP/1.1"
        handler.headers = headers
        handler.client_address = ("127.0.0.1", 12345)
        handler.server = MagicMock()
        handler.close_connection = False

        if method == "GET":
            handler.do_GET()
        elif method == "POST":
            handler.do_POST()

        output = wfile.getvalue()
        header_end = output.find(b"\r\n\r\n")
        if header_end != -1:
            raw_body = output[header_end+4:].decode()
            return json.loads(raw_body) if raw_body else {}
        return {}

    def test_get_axes_endpoint(self):
        res = self._invoke("GET", "/api/v1/clinical/axes")
        self.assertTrue(res.get("ok"))
        self.assertEqual(res.get("count"), 12)

    def test_post_axes_score_endpoint(self):
        res = self._invoke("POST", "/api/v1/clinical/axes/score", {"scores": {"Jigar-Banas": 5, "Qalb-Uroq": 4}})
        self.assertTrue(res.get("ok"))
        self.assertEqual(res.get("result", {}).get("primary_axis"), "Jigar-Banas")

    def test_get_protocols_endpoint(self):
        res = self._invoke("GET", "/api/v1/clinical/protocols")
        self.assertTrue(res.get("ok"))
        self.assertEqual(res.get("count"), 21)

    def test_get_single_protocol_endpoint(self):
        res = self._invoke("GET", "/api/v1/clinical/protocols/P-01")
        self.assertTrue(res.get("ok"))
        self.assertIn("Diabetes", res.get("protocol", {}).get("name", ""))

    def test_get_kits_endpoint(self):
        res = self._invoke("GET", "/api/v1/clinical/kits")
        self.assertTrue(res.get("ok"))
        self.assertEqual(res.get("count"), 21)

    def test_get_products_endpoint(self):
        res = self._invoke("GET", "/api/v1/therapeutic/products")
        self.assertTrue(res.get("ok"))
        self.assertEqual(res.get("count"), 32)

    def test_get_single_product_endpoint(self):
        res = self._invoke("GET", "/api/v1/therapeutic/products/ZAY-001")
        self.assertTrue(res.get("ok"))
        self.assertEqual(res.get("product", {}).get("sku"), "ZAY-001")

    def test_get_parhez_endpoint(self):
        res = self._invoke("GET", "/api/v1/therapeutic/parhez")
        self.assertTrue(res.get("ok"))
        self.assertEqual(res.get("count"), 8)

    def test_post_zmai_calculate_endpoint(self):
        res = self._invoke("POST", "/api/v1/clinical/zmai/calculate", {"responses": {"q1_build": "damawi"}})
        self.assertTrue(res.get("ok"))
        self.assertEqual(res.get("assessment", {}).get("dominant_mizaj"), "damawi")

    def test_post_safety_check_endpoint(self):
        res = self._invoke("POST", "/api/v1/therapeutic/interactions/check", {
            "products": ["ZAY-001"],
            "medications": ["Metoprolol 50mg"],
            "is_pregnant": True
        })
        self.assertTrue(res.get("ok"))
        self.assertFalse(res.get("is_safe"))
        self.assertEqual(res.get("severity"), "CRITICAL")


if __name__ == "__main__":
    unittest.main()
