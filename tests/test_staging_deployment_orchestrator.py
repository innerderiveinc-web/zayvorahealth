#!/usr/bin/env python3
"""
ZAYVORA Health™ — Phase 10: Staging Cluster Deployment Orchestrator Test Suite.

Verifies:
1. Staging deployment orchestrator initialization and configuration.
2. Helm chart packaging and template syntax validity.
3. Alembic multi-database migration configuration readiness.
4. University clinical pilot center tenant provisioning.
5. Microservice health probe smoke checks (/health/live & /health/ready).
6. Cryptographic staging deployment certificate issuance.
"""

import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.deploy_staging_cluster import StagingDeploymentOrchestrator


class TestStagingDeploymentOrchestrator(unittest.TestCase):
    """Test suite certifying Phase 10 staging cluster deployment and onboarding."""

    def setUp(self):
        self.orchestrator = StagingDeploymentOrchestrator(
            namespace="zayvora-staging-test", environment="staging"
        )

    def test_01_orchestrator_initialization(self):
        """Verify orchestrator configuration and deployment ID format."""
        self.assertEqual(self.orchestrator.namespace, "zayvora-staging-test")
        self.assertEqual(self.orchestrator.environment, "staging")
        self.assertTrue(self.orchestrator.deployment_id.startswith("DEPLOY-"))
        self.assertEqual(len(self.orchestrator.MICROSERVICES), 6)

    def test_02_helm_chart_packaging_verification(self):
        """Verify Helm chart directory and values packaging."""
        res = self.orchestrator.verify_helm_packaging()
        self.assertTrue(res["chart_valid"])
        self.assertEqual(res["services_packaged"], 6)

    def test_03_database_migration_configuration(self):
        """Verify that all 4 microservice Alembic configs are discovered."""
        res = self.orchestrator.execute_database_migrations_dry_run()
        self.assertTrue(res["migrations_verified"])
        self.assertEqual(set(res["schemas"]), {"clinical", "therapeutic", "identity", "ai"})

    def test_04_health_smoke_checks(self):
        """Verify that simulated health probes pass for all 6 services."""
        health = self.orchestrator.run_health_smoke_checks()
        self.assertEqual(len(health), 6)
        for svc_name, status in health.items():
            self.assertEqual(status["status"], "HEALTHY")
            self.assertIn("200 OK", status["liveness_probe"])
            self.assertIn("200 OK", status["readiness_probe"])

    def test_05_full_deployment_certificate_issuance(self):
        """Verify execution of deployment and issuance of signed certificate."""
        cert = self.orchestrator.execute_deployment(dry_run=True)
        self.assertEqual(cert["status"], "STAGING_DEPLOYMENT_CERTIFIED_OPERATIONAL")
        self.assertEqual(len(cert["academic_centers_onboarded"]), 3)
        self.assertEqual(len(cert["deployment_signature"]), 64)  # Valid SHA-256
        self.assertIn("clinician_desk", cert["endpoints"])
        self.assertIn("staging.app.zayvora.com", cert["endpoints"]["clinician_desk"])
        self.assertIn("api_gateway", cert["endpoints"])


if __name__ == "__main__":
    unittest.main()
