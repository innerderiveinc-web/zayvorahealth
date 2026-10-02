import os
import unittest

class TestMultiPageWebsiteArchitecture(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.web_app_dir = os.path.join(self.base_dir, "apps", "web", "app")
        self.data_dir = os.path.join(self.base_dir, "apps", "web", "lib", "data")
        self.components_dir = os.path.join(self.base_dir, "apps", "web", "components", "website")

    def test_required_routes_exist(self):
        """Verify all 25+ required public and auth routes exist with page.tsx."""
        required_routes = [
            "",  # /
            "about",
            "services",
            "services/clinical-care",
            "services/ai-healthcare",
            "services/digital-health",
            "services/research",
            "services/pharmacy",
            "services/manufacturing",
            "services/healthcare-communication",
            "products",
            "products/unani-care",
            "products/herbal-products",
            "products/nutraceuticals",
            "research",
            "research/clinical-research",
            "research/evidence",
            "research/knowledge-intelligence",
            "team",
            "contact",
            "faq",
            "privacy-policy",
            "terms-and-conditions",
            "careers",
            "login",
            "forgot-password",
            "reset-password",
            "reception",
            "research/workspace",
        ]

        for route in required_routes:
            page_path = os.path.join(self.web_app_dir, route, "page.tsx")
            self.assertTrue(
                os.path.exists(page_path),
                f"Required route page missing: {route} (expected at {page_path})"
            )

    def test_shared_data_layer_files_exist(self):
        """Verify centralized shared data layer files exist."""
        required_files = [
            "types.ts",
            "siteConfig.ts",
            "navigation.ts",
            "services.ts",
            "products.ts",
            "research.ts",
            "team.ts",
            "faqs.ts",
            "legal.ts",
            "seo.ts",
            "index.ts",
        ]
        for f in required_files:
            p = os.path.join(self.data_dir, f)
            self.assertTrue(os.path.exists(p), f"Missing data module: {f}")

    def test_shared_components_exist(self):
        """Verify reusable website components exist."""
        required_components = [
            "PageHeader.tsx",
            "ServiceCard.tsx",
            "ProductCard.tsx",
            "ResearchCard.tsx",
            "TeamCard.tsx",
            "FaqAccordion.tsx",
            "ContactForm.tsx",
        ]
        for comp in required_components:
            p = os.path.join(self.components_dir, comp)
            self.assertTrue(os.path.exists(p), f"Missing website component: {comp}")

    def test_site_config_values(self):
        """Verify siteConfig has official ZAYVORA proprietary identity."""
        p = os.path.join(self.data_dir, "siteConfig.ts")
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('"ZAYVORA Health™"', content)
        self.assertIn('"ZAYVORA Health OS™"', content)
        self.assertIn('"Ancient Wisdom. Modern Science. Intelligent Care."', content)
        self.assertIn("+91 97738 82657", content)

    def test_header_navigation_dropdowns(self):
        """Verify navigation contains dropdowns for Services (7), Products (3), Research (3)."""
        p = os.path.join(self.data_dir, "navigation.ts")
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        # Check all 7 services are present
        self.assertIn("/services/clinical-care", content)
        self.assertIn("/services/ai-healthcare", content)
        self.assertIn("/services/digital-health", content)
        self.assertIn("/services/research", content)
        self.assertIn("/services/pharmacy", content)
        self.assertIn("/services/manufacturing", content)
        self.assertIn("/services/healthcare-communication", content)
        # Check all 3 products are present
        self.assertIn("/products/unani-care", content)
        self.assertIn("/products/herbal-products", content)
        self.assertIn("/products/nutraceuticals", content)
        # Check all 3 research areas are present
        self.assertIn("/research/clinical-research", content)
        self.assertIn("/research/evidence", content)
        self.assertIn("/research/knowledge-intelligence", content)

    def test_design_system_components_exist(self):
        """Verify expanded shared design system components exist."""
        ds_dir = os.path.join(self.base_dir, "design-system", "src", "components")
        expected = [
            "Button.tsx",
            "Card.tsx",
            "Badge.tsx",
            "Input.tsx",
            "Modal.tsx",
            "Spinner.tsx",
            "Textarea.tsx",
            "Select.tsx",
            "Tabs.tsx",
            "Alert.tsx",
            "LoadingSkeleton.tsx",
            "EmptyState.tsx",
            "ConfirmationDialog.tsx",
        ]
        for comp in expected:
            p = os.path.join(ds_dir, comp)
            self.assertTrue(os.path.exists(p), f"Design system component missing: {comp}")

    def test_zero_accidental_external_branding_in_new_routes(self):
        """Verify no accidental external university ownership claims appear in new routes."""
        banned = ["Hamdard Hospital", "HIMSR Hospital", "Majeedia Hospital", "AMU Hospital", "AKTC Hospital"]
        for root, _, files in os.walk(self.web_app_dir):
            # Exclude website/ legacy routes if any
            for f in files:
                if f.endswith(".tsx"):
                    path = os.path.join(root, f)
                    with open(path, "r", encoding="utf-8") as file:
                        c = file.read()
                    for ban in banned:
                        self.assertNotIn(ban, c, f"Found banned term '{ban}' in {path}")

if __name__ == "__main__":
    unittest.main()
