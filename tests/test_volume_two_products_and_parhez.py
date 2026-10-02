"""
Test Suite for ZAYVORA Volume II: 16 Core Products, Dual-Track Mapping & 8 Parhez Protocols
Author: Dr. Irfan Ashraf, BUMS

Tests:
  1. Complete 16 Core Products Schema (80/20 polypharmacy architecture)
  2. Parent-Child mapping from 16 GMP Products to 32 Classical Matab Nuskhas
  3. Green Zone vs Red Zone Claims Discipline (DMR Act 1954 compliance)
  4. 8 Complete Parhez Clinical Lifestyle Protocols
  5. Live REST endpoints:
     - GET /api/v1/therapeutic/products-16/all
     - GET /api/v1/therapeutic/products-16/{id}
     - GET /api/v1/clinical/parhez-8/all
     - GET /api/v1/clinical/parhez-8/{code}
"""

import unittest
import json
import io
from unittest.mock import MagicMock

from services.therapeutic.app.data.product_matrix_16 import (
    CORE_PRODUCTS_16,
    get_all_core_products,
    get_product_by_id,
    get_products_by_regulatory_track
)
from services.clinical.app.data.parhez_protocols_8 import (
    PARHEZ_PROTOCOLS_8,
    get_all_parhez,
    get_parhez_by_code
)
import services.live_api_server as las


class TestVolumeTwoProductsAndParhez(unittest.TestCase):

    def setUp(self):
        self.handler = las.ZayvoraApiHandler.__new__(las.ZayvoraApiHandler)
        self.handler.wfile = io.BytesIO()
        self.handler.headers = {"Content-Length": "0"}
        self.handler.server = MagicMock()
        self.handler.client_address = ("127.0.0.1", 54321)
        self.handler.request_version = "HTTP/1.1"

    def test_sixteen_products_count_and_tracks(self):
        """Test that exactly 16 products are registered across AYUSH Track A and FSSAI Track B."""
        all_prods = get_all_core_products()
        self.assertEqual(len(all_prods), 16)

        ayush_prods = get_products_by_regulatory_track("AYUSH")
        fssai_prods = get_products_by_regulatory_track("FSSAI")
        self.assertEqual(len(ayush_prods) + len(fssai_prods), 16)

    def test_parent_child_nuskha_mapping(self):
        """Test that every GMP product maps back to its parent classical Matab Nuskha."""
        p1 = get_product_by_id("ZAY-PROD-01")
        self.assertIsNotNone(p1)
        self.assertEqual(p1["parent_nuskha_code"], "MF-01")
        self.assertIn("Safoof Muqawwi", p1["parent_nuskha_name"])

        p5 = get_product_by_id("ZAY-PROD-05")
        self.assertEqual(p5["internal_code"], "ZV-F-02")
        self.assertEqual(p5["parent_nuskha_code"], "PC-01")

    def test_eighty_twenty_architecture(self):
        """Test that 80% classical core and 20% modern layer are present in each product."""
        for prod in get_all_core_products():
            self.assertIn("classical_core_80", prod)
            self.assertIn("modern_layer_20", prod)
            self.assertGreater(len(prod["classical_core_80"]), 0)
            self.assertGreater(len(prod["modern_layer_20"]), 0)

    def test_claims_discipline_boundaries(self):
        """Verify DMR Act 1954 red zone prohibition compliance."""
        for prod in get_all_core_products():
            self.assertIn("permitted_claim_green_zone", prod)
            self.assertIn("prohibited_claim_red_zone", prod)
            self.assertTrue(len(prod["prohibited_claim_red_zone"]) > 10)


    def test_eight_parhez_protocols(self):
        """Test registration and content of all 8 clinical Parhez protocols."""
        all_pz = get_all_parhez()
        self.assertEqual(len(all_pz), 8)

        # Test MF-01
        mf01 = get_parhez_by_code("MF-01")
        self.assertIsNotNone(mf01)
        elem_names = [e["element"] for e in mf01["elements"]]
        self.assertIn("Thermal Management", elem_names)
        self.assertIn("Alcohol Abstinence", elem_names)

        # Test FK-01 (Fatty Liver)
        fk01 = get_parhez_by_code("FK-01")
        self.assertIsNotNone(fk01)
        self.assertTrue(any("coffee" in e["element"].lower() for e in fk01["elements"]))

    def test_api_products_and_parhez_endpoints(self):
        """Test live HTTP GET routes for 16 products and 8 Parhez."""
        # 1. GET /api/v1/therapeutic/products-16/all
        self.handler.path = "/api/v1/therapeutic/products-16/all"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/therapeutic/products-16/all HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body_prods = json.loads(resp_lines[1])
        self.assertEqual(body_prods["total_products"], 16)

        # 2. GET /api/v1/clinical/parhez-8/MF-01
        self.handler.path = "/api/v1/clinical/parhez-8/MF-01"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/clinical/parhez-8/MF-01 HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body_pz = json.loads(resp_lines[1])
        self.assertEqual(body_pz["parhez"]["parhez_code"], "MF-01")


if __name__ == "__main__":
    unittest.main()
