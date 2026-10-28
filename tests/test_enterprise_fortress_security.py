#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Enterprise Fortress Security & DR Verification Suite
=============================================================================
Verifies the 3 core pillars of the Enterprise Fortress Roadmap:
1. Multi-Dimensional Token-Bucket Rate Limiter (IP & Token, Auth Barrier, 429 Retry-After).
2. Defense-in-Depth HTTP Security Headers (Strict CSP, HSTS, X-Frame-Options, Permissions-Policy).
3. Litestream-Compatible Continuous WAL Replication (Near-Zero RPO < 1.0s, RTO < 5.0s, SHA-256 seal).
4. System Security & Replication Telemetry Endpoints (/api/v1/system/*).
=============================================================================
"""

import unittest
import os
import sys
import json
import time
import shutil
from io import BytesIO

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.security_shield import (
    check_rate_limit,
    get_rate_limit_headers,
    inspect_payload_safety,
    apply_enterprise_security_headers,
    RATE_LIMIT_BURST,
    AUTH_RATE_LIMIT_BURST,
)
from database.continuous_replication_daemon import ContinuousReplicationEngine, get_replication_engine
from services.live_api_server import ZayvoraApiHandler


class DummyResponseHandler:
    """Mock HTTP handler to capture sent headers."""
    def __init__(self):
        self.headers_sent = {}

    def send_header(self, keyword, value):
        self.headers_sent[keyword] = value


class TestEnterpriseFortressSecurity(unittest.TestCase):

    def test_01_token_bucket_rate_limiting_barrier(self):
        """Verifies Token Bucket rate limiting: allows burst, rejects excess, returns 429."""
        test_ip = "198.51.100.42"

        # 1. First request must be allowed
        self.assertTrue(check_rate_limit(test_ip))

        # 2. Exhaust burst capacity for this test IP
        for _ in range(int(RATE_LIMIT_BURST)):
            check_rate_limit(test_ip)

        # 3. Next immediate request must be blocked
        is_allowed = check_rate_limit(test_ip)
        self.assertFalse(is_allowed, "Rate limiter must block traffic exceeding burst capacity")

        # 4. Standard IETF / OWASP 429 headers must be generated
        headers = get_rate_limit_headers(test_ip)
        self.assertIn("Retry-After", headers)
        self.assertIn("X-RateLimit-Limit", headers)
        self.assertIn("X-RateLimit-Remaining", headers)
        self.assertEqual(headers["X-RateLimit-Remaining"], "0")
        self.assertGreaterEqual(int(headers["Retry-After"]), 1)

    def test_02_auth_login_stricter_rate_limiting(self):
        """Verifies stricter brute-force rate limit on login / auth endpoints."""
        auth_attacker_ip = "203.0.113.99"

        # Exhaust strict auth capacity (15 attempts)
        for _ in range(int(AUTH_RATE_LIMIT_BURST)):
            check_rate_limit(auth_attacker_ip, is_auth_endpoint=True)

        # 16th attempt on login must be blocked
        is_blocked = not check_rate_limit(auth_attacker_ip, is_auth_endpoint=True)
        self.assertTrue(is_blocked, "Brute force attempts on auth endpoints must be blocked")

        headers = get_rate_limit_headers(auth_attacker_ip, is_auth_endpoint=True)
        self.assertEqual(headers["X-RateLimit-Limit"], str(int(AUTH_RATE_LIMIT_BURST)))
        self.assertIn("Retry-After", headers)

    def test_03_enterprise_http_security_headers_and_csp(self):
        """Verifies presence of OWASP Top 10, HIPAA & ISO 27001 HTTP response headers."""
        handler = DummyResponseHandler()
        apply_enterprise_security_headers(handler)

        h = handler.headers_sent
        self.assertIn("Content-Security-Policy", h)
        self.assertIn("default-src 'self'", h["Content-Security-Policy"])
        self.assertIn("object-src 'none'", h["Content-Security-Policy"])
        self.assertIn("frame-ancestors 'self'", h["Content-Security-Policy"])

        self.assertEqual(h.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertEqual(h.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(h.get("X-XSS-Protection"), "1; mode=block")
        self.assertEqual(h.get("Referrer-Policy"), "strict-origin-when-cross-origin")
        self.assertIn("max-age=31536000", h.get("Strict-Transport-Security", ""))
        self.assertEqual(h.get("Cross-Origin-Opener-Policy"), "same-origin")

    def test_04_continuous_wal_replication_engine(self):
        """Verifies real-time continuous WAL replication, RPO < 1s, and SHA-256 seal."""
        test_replica_dir = os.path.join(BASE_DIR, "backups", "wal_replica_test")
        os.makedirs(test_replica_dir, exist_ok=True)

        engine = ContinuousReplicationEngine(
            db_path=os.path.join(BASE_DIR, "database", "zayvora_live.db"),
            replica_dir=test_replica_dir
        )

        manifest = engine.sync_once()
        self.assertEqual(manifest["status"], "ACTIVE_STREAMING")
        self.assertLess(manifest["rpo_seconds"], 1.0, "Continuous replication must guarantee RPO < 1.0 second")
        self.assertLessEqual(manifest["rto_seconds"], 5.0, "Recovery Time Objective must be < 5.0 seconds")
        self.assertTrue(len(manifest["sha256_integrity_seal"]) == 64, "Replicated state must have valid SHA-256 seal")
        self.assertTrue(os.path.exists(manifest["replica_database"]), "Physical replicated database file must exist on disk")

        # Cleanup test replica dir
        try:
            shutil.rmtree(test_replica_dir)
        except Exception:
            pass

    def test_05_system_replication_and_security_endpoints(self):
        """Verifies in-memory live execution of /api/v1/system/replication-status and /api/v1/system/security-status."""
        class DummySocket:
            def __init__(self, rfile, wfile):
                self.rfile = rfile
                self.wfile = wfile
            def makefile(self, mode, *args, **kwargs):
                return self.rfile if "r" in mode else self.wfile
            def sendall(self, b):
                self.wfile.write(b)

        # 1. Test simulated GET /api/v1/system/replication-status
        raw_headers = "GET /api/v1/system/replication-status HTTP/1.1\r\nHost: localhost:8000\r\n\r\n"
        input_stream = BytesIO(raw_headers.encode("utf-8"))
        output_stream = BytesIO()

        dummy_sock = DummySocket(input_stream, output_stream)
        handler = ZayvoraApiHandler(dummy_sock, ("127.0.0.1", 8000), None)
        output = output_stream.getvalue().decode("utf-8")
        self.assertIn("200 OK", output)
        self.assertIn("replication", output)
        self.assertIn("rpo_seconds", output)

        # 2. Test simulated GET /api/v1/system/security-status
        raw_headers2 = "GET /api/v1/system/security-status HTTP/1.1\r\nHost: localhost:8000\r\n\r\n"
        input_stream2 = BytesIO(raw_headers2.encode("utf-8"))
        output_stream2 = BytesIO()

        dummy_sock2 = DummySocket(input_stream2, output_stream2)
        handler2 = ZayvoraApiHandler(dummy_sock2, ("127.0.0.1", 8000), None)
        output2 = output_stream2.getvalue().decode("utf-8")
        self.assertIn("200 OK", output2)
        self.assertIn("security_architecture", output2)
        self.assertIn("Token-Bucket", output2)


if __name__ == "__main__":
    unittest.main()
