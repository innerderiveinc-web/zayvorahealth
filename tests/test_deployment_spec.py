import os
import json
import unittest

class TestDeploymentSpecifications(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def test_procfile_exists_and_configured(self):
        """Verify Procfile routes to live_api_server with dynamic port."""
        procfile_path = os.path.join(self.base_dir, "Procfile")
        self.assertTrue(os.path.exists(procfile_path), "Procfile must exist")
        with open(procfile_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("web: python3 services/live_api_server.py", content)

    def test_railway_json_valid_and_has_healthcheck(self):
        """Verify railway.json configuration schema and health probe."""
        railway_path = os.path.join(self.base_dir, "railway.json")
        self.assertTrue(os.path.exists(railway_path), "railway.json must exist")
        with open(railway_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        self.assertIn("deploy", cfg)
        self.assertEqual(cfg["deploy"]["healthcheckPath"], "/api/v1/health")
        self.assertIn("startCommand", cfg["deploy"])

    def test_nixpacks_toml_configured(self):
        """Verify nixpacks.toml exists and specifies python."""
        nixpacks_path = os.path.join(self.base_dir, "nixpacks.toml")
        self.assertTrue(os.path.exists(nixpacks_path), "nixpacks.toml must exist")
        with open(nixpacks_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("python", content)
        self.assertIn("services/live_api_server.py", content)

    def test_dockerfile_and_dockerignore_configured(self):
        """Verify standard container Dockerfile and .dockerignore."""
        dockerfile_path = os.path.join(self.base_dir, "Dockerfile")
        dockerignore_path = os.path.join(self.base_dir, ".dockerignore")
        self.assertTrue(os.path.exists(dockerfile_path), "Dockerfile must exist")
        self.assertTrue(os.path.exists(dockerignore_path), ".dockerignore must exist")

        with open(dockerfile_path, "r", encoding="utf-8") as f:
            df = f.read()
        self.assertIn("python:3.11-slim", df)
        self.assertIn("HEALTHCHECK", df)
        self.assertIn("/api/v1/health", df)
        self.assertIn("live_api_server.py", df)

        with open(dockerignore_path, "r", encoding="utf-8") as f:
            di = f.read()
        self.assertIn(".git", di)
        self.assertIn(".env", di)

if __name__ == "__main__":
    unittest.main()
