import os
import unittest

class TestMobileApplicationWorkflows(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.mobile_dir = os.path.join(self.base_dir, "apps", "mobile")
        self.screens_dir = os.path.join(self.mobile_dir, "src", "screens")
        self.services_dir = os.path.join(self.mobile_dir, "src", "services")
        self.nav_dir = os.path.join(self.mobile_dir, "src", "navigation")

    def test_all_11_screens_exist(self):
        """Verify all 11 production mobile screens exist."""
        required_screens = [
            "HomeScreen.tsx",
            "AuthScreen.tsx",
            "AppointmentsScreen.tsx",
            "PrescriptionsScreen.tsx",
            "LabResultsScreen.tsx",
            "NotificationsScreen.tsx",
            "ProfileScreen.tsx",
            "MizajAssessmentScreen.tsx",
            "TeleConsultRoom.tsx",
            "LifestyleTrackerScreen.tsx",
            "ClinicianCompanionScreen.tsx",
        ]
        for screen in required_screens:
            p = os.path.join(self.screens_dir, screen)
            self.assertTrue(os.path.exists(p), f"Mobile screen missing: {screen} at {p}")

    def test_app_navigator_exists_and_routes_screens(self):
        """Verify AppNavigator routes exist and handle auth state."""
        nav_file = os.path.join(self.nav_dir, "AppNavigator.tsx")
        self.assertTrue(os.path.exists(nav_file), "AppNavigator.tsx missing")
        with open(nav_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("AuthScreen", content)
        self.assertIn("HomeScreen", content)
        self.assertIn("AppointmentsScreen", content)
        self.assertIn("PrescriptionsScreen", content)
        self.assertIn("LabResultsScreen", content)
        self.assertIn("NotificationsScreen", content)
        self.assertIn("ProfileScreen", content)
        self.assertIn("MizajAssessmentScreen", content)
        self.assertIn("TeleConsultRoom", content)
        self.assertIn("LifestyleTrackerScreen", content)
        self.assertIn("getStoredToken", content)

    def test_mobile_services_exist(self):
        """Verify mobile API and storage services exist."""
        services = [
            "auth.service.ts",
            "api.service.ts",
            "notifications.service.ts",
            "OfflineStorageService.ts",
        ]
        for s in services:
            p = os.path.join(self.services_dir, s)
            self.assertTrue(os.path.exists(p), f"Mobile service missing: {s}")

    def test_mobile_shared_components_exist(self):
        """Verify mobile shared UI components exist."""
        comp_dir = os.path.join(self.mobile_dir, "src", "components")
        expected = [
            "Card.tsx",
            "Button.tsx",
            "Badge.tsx",
            "LoadingSkeleton.tsx",
            "EmptyState.tsx",
            "index.ts",
        ]
        for comp in expected:
            p = os.path.join(comp_dir, comp)
            self.assertTrue(os.path.exists(p), f"Mobile shared component missing: {comp}")

    def test_mobile_zero_external_branding(self):
        """Verify no accidental external university ownership claims in mobile code."""
        banned = ["ZAYVORA Healthcare System", "Hamdard Hospital", "Majeedia Hospital", "AMU Hospital"]
        for root, _, files in os.walk(self.mobile_dir):
            for f in files:
                if f.endswith(".tsx") or f.endswith(".ts"):
                    path = os.path.join(root, f)
                    with open(path, "r", encoding="utf-8") as file:
                        c = file.read()
                    for ban in banned:
                        self.assertNotIn(ban, c, f"Found banned term '{ban}' in mobile file {path}")

    def test_patient_action_first_regimen_and_adherence(self):
        """Verify Patient Mobile features action-first regimen and 1-tap adherence tracking."""
        app_file = os.path.join(self.mobile_dir, "App.tsx")
        home_file = os.path.join(self.screens_dir, "HomeScreen.tsx")

        with open(app_file, "r", encoding="utf-8") as f:
            app_src = f.read()
        self.assertIn("TODAY'S CARE • NEXT ACTION", app_src)
        self.assertIn("What do I do today?", app_src)
        self.assertIn("patientAdherence", app_src)
        self.assertIn("✓ Taken", app_src)
        self.assertIn("⏳ Not Yet", app_src)
        self.assertIn("✕ Skipped", app_src)

        with open(home_file, "r", encoding="utf-8") as f:
            home_src = f.read()
        self.assertIn("TODAY'S CARE • NEXT ACTION", home_src)
        self.assertIn("What do I do today?", home_src)
        self.assertIn("adherence", home_src)
        self.assertIn("✓ Taken", home_src)
        self.assertIn("⏳ Not Yet", home_src)
        self.assertIn("✕ Skipped", home_src)

    def test_eas_standalone_apk_configuration(self):
        """Verify eas.json configures Android standalone APK build type."""
        import json
        eas_path = os.path.join(self.mobile_dir, "eas.json")
        self.assertTrue(os.path.exists(eas_path), "eas.json must exist")
        with open(eas_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("build", data)
        self.assertIn("preview", data["build"])
        self.assertEqual(data["build"]["preview"]["android"]["buildType"], "apk")

    def test_package_json_build_scripts(self):
        """Verify package.json contains standalone APK build scripts."""
        import json
        pkg_path = os.path.join(self.mobile_dir, "package.json")
        self.assertTrue(os.path.exists(pkg_path), "package.json must exist")
        with open(pkg_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        scripts = data.get("scripts", {})
        self.assertIn("build:apk", scripts)
        self.assertIn("build:apk:cloud", scripts)
        self.assertIn("build:aab", scripts)

    def test_mobile_apk_build_script_executable(self):
        """Verify scripts/build_mobile_apk.sh exists and is executable."""
        script_path = os.path.join(self.base_dir, "scripts", "build_mobile_apk.sh")
        self.assertTrue(os.path.exists(script_path), "build_mobile_apk.sh must exist")
        self.assertTrue(os.access(script_path, os.X_OK), "build_mobile_apk.sh must be executable")

if __name__ == "__main__":
    unittest.main()
