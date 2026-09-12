"""
Unit test verifying Helm Chart packaging and configuration integrity (DEP-01).
"""
import os
import unittest


class TestHelmChartPackaging(unittest.TestCase):
    def setUp(self):
        self.helm_dir = os.path.abspath("infrastructure/helm/zayvora")

    def test_chart_yaml_structure(self):
        chart_path = os.path.join(self.helm_dir, "Chart.yaml")
        self.assertTrue(os.path.exists(chart_path), "Chart.yaml must exist")
        with open(chart_path, "r") as f:
            content = f.read()
        self.assertIn("apiVersion: v2", content)
        self.assertIn("name: zayvora", content)
        self.assertIn("version: 2.0.0", content)

    def test_values_yaml_covers_all_microservices(self):
        values_path = os.path.join(self.helm_dir, "values.yaml")
        self.assertTrue(os.path.exists(values_path), "values.yaml must exist")
        with open(values_path, "r") as f:
            content = f.read()
        for svc in ["gateway", "identity", "clinical", "knowledge", "therapeutic", "ai"]:
            self.assertIn(f"{svc}:", content, f"values.yaml must configure service: {svc}")
        self.assertIn("vaultAgent:", content)
        self.assertIn("runAsNonRoot: true", content)
        self.assertIn("readOnlyRootFilesystem: true", content)
        self.assertIn("ingress:", content)

    def test_template_files_present(self):
        tpl_dir = os.path.join(self.helm_dir, "templates")
        expected_templates = [
            "_helpers.tpl",
            "configmap.yaml",
            "secret.yaml",
            "deployments.yaml",
            "services.yaml",
            "ingress.yaml",
        ]
        for tpl in expected_templates:
            tpl_path = os.path.join(tpl_dir, tpl)
            self.assertTrue(os.path.exists(tpl_path), f"Template {tpl} must exist in {tpl_dir}")


if __name__ == "__main__":
    unittest.main()
