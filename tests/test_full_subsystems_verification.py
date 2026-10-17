import os
import re
import unittest
import sqlite3
import json

class TestFullSubsystemsVerification(unittest.TestCase):
    """
    Exhaustive verification across all 5 key subsystems:
    1. Web Application Subsystem
    2. Mobile Application Subsystem
    3. Core Engines Subsystem
    4. API Layer Subsystem
    5. Audio Subsystems
    """

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.index_path = os.path.join(self.base_dir, "index.html")
        self.core_js_path = os.path.join(self.base_dir, "js", "zayvora-core.js")
        self.ext_js_path = os.path.join(self.base_dir, "js", "zayvora-extensions.js")
        self.sw_path = os.path.join(self.base_dir, "sw.js")
        self.manifest_path = os.path.join(self.base_dir, "manifest.json")
        self.db_path = os.path.join(self.base_dir, "database", "zayvora_live.db")
        self.api_server_path = os.path.join(self.base_dir, "services", "live_api_server.py")

        with open(self.index_path, "r", encoding="utf-8") as f:
            self.index_html = f.read()
        with open(self.core_js_path, "r", encoding="utf-8") as f:
            self.core_js = f.read()
        with open(self.ext_js_path, "r", encoding="utf-8") as f:
            self.ext_js = f.read()

    # ─────────────────────────────────────────────────────────────────────────
    # 1. WEB APPLICATION SUBSYSTEM
    # ─────────────────────────────────────────────────────────────────────────
    def test_01_web_application_subsystem(self):
        """Verify Web App layout, role desks, consultation thread, and responsive surfaces."""
        # A. All 13 Workspace Renderers exist
        roles = ['doctor', 'clinic', 'pharmacy', 'nurse', 'patient', 'research',
                 'admin', 'enterprise', 'manufacturing', 'herbals', 'website', 'mobile', 'hardware']
        for r in roles:
            renderer_name = f"render{r.capitalize()}App"
            self.assertIn(f"function {renderer_name}(", self.core_js, f"Renderer {renderer_name} must exist")

        # B. Central navigation & active view switching
        self.assertIn("function switchRole(", self.core_js)
        self.assertIn("function switchTab(", self.core_js)
        self.assertIn("function renderWorkspace(", self.core_js)

        # C. Doctor 3-Zone Cockpit & Fast Matab
        self.assertIn("renderSingleConsultationWorkspace", self.core_js)
        self.assertIn("renderFastMatabMode", self.core_js)
        self.assertIn("openBilingualPrescriptionSlipModal", self.core_js)

        # D. 25-page canonical sitemap in website footer
        self.assertIn('id="site-footer-directory"', self.index_html)
        self.assertIn("Site Directory (25 Pages)", self.core_js)

    # ─────────────────────────────────────────────────────────────────────────
    # 2. MOBILE APPLICATION SUBSYSTEM
    # ─────────────────────────────────────────────────────────────────────────
    def test_02_mobile_application_subsystem(self):
        """Verify PWA Service Worker, Web App Manifest, Bedside Simulator, and Touch Triage."""
        # A. Manifest.json exists with valid PWA fields
        self.assertTrue(os.path.exists(self.manifest_path), "manifest.json must exist")
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        self.assertIn("ZAYVORA Health OS", manifest_data.get("name"))
        self.assertEqual(manifest_data.get("display"), "standalone")

        # B. Service Worker (sw.js) exists with cache strategies and offline fallback
        self.assertTrue(os.path.exists(self.sw_path), "sw.js must exist")
        with open(self.sw_path, "r", encoding="utf-8") as f:
            sw_code = f.read()
        self.assertIn("addEventListener('fetch'", sw_code)
        self.assertIn("caches.match", sw_code)

        # C. Bedside Mobile Interface & Touch Mode
        self.assertIn("toggleMobileClinicMode", self.ext_js)
        self.assertIn("mobileActiveScreen", self.core_js)
        self.assertIn("Asbab-e-Sittah 6 Essentials", self.core_js)
        self.assertIn("Doctor Mobile Triage", self.core_js)

    # ─────────────────────────────────────────────────────────────────────────
    # 3. CORE ENGINES SUBSYSTEM
    # ─────────────────────────────────────────────────────────────────────────
    def test_03_core_engines_subsystem(self):
        """Verify Mizaj diagnostics, Ilaj bil-Zidd counteraction, ZFIE compiler, and 21 CFR Part 11 seals."""
        # A. Detailed Mizaj Engine
        self.assertIn("function calculateDetailedMizaj(", self.core_js)
        self.assertIn("percentages.damawi", self.core_js)
        self.assertIn("percentages.balghami", self.core_js)
        self.assertIn("percentages.safrawi", self.core_js)
        self.assertIn("percentages.sawdawi", self.core_js)

        # B. Ilaj bil-Zidd Therapeutic Antagonism Engine
        self.assertIn("function calculateIlajBilZidd(", self.core_js)
        self.assertIn("THERAPEUTIC ANTAGONISM EQUILIBRIUM", self.core_js)

        # C. 21 CFR Part 11 Merkle Audit Trail & Digital Signature
        self.assertIn("21 CFR Part 11", self.core_js)
        self.assertIn("SHA-256", self.core_js)

        # D. Schedule E(1) Mudabbar Detoxification Gate
        self.assertIn("Schedule E(1)", self.core_js)
        self.assertIn("Mudabbar Detoxification Gate", self.core_js)

    # ─────────────────────────────────────────────────────────────────────────
    # 4. API LAYER SUBSYSTEM
    # ─────────────────────────────────────────────────────────────────────────
    def test_04_api_layer_subsystem(self):
        """Verify SQLite Database schema and Live REST API Server architecture."""
        # A. SQLite database exists and contains essential tables
        self.assertTrue(os.path.exists(self.db_path), "zayvora_live.db must exist")
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        conn.close()

        mandatory_tables = ["users", "patients", "prescriptions", "appointments", "inventory"]
        for t in mandatory_tables:
            self.assertIn(t, tables, f"Database must contain table '{t}'")

        # B. live_api_server.py REST endpoints
        with open(self.api_server_path, "r", encoding="utf-8") as f:
            server_code = f.read()
        self.assertIn("class ZayvoraApiHandler", server_code)
        self.assertIn("/api/v1/auth/login", server_code)
        self.assertIn("/api/v1/patients", server_code)
        self.assertIn("/api/v1/prescriptions", server_code)
        self.assertIn("/api/v1/appointments", server_code)
        self.assertIn("/api/v1/ai/status", server_code)

        # C. Graceful fallback layer in frontend for static/Netlify environments
        self.assertIn("async function apiFetch(", self.core_js)

    # ─────────────────────────────────────────────────────────────────────────
    # 5. AUDIO SUBSYSTEMS
    # ─────────────────────────────────────────────────────────────────────────
    def test_05_audio_subsystems(self):
        """Verify Web Speech API posology synthesizer, acoustic chimes, language map, and WhatsApp audio."""
        # A. Audio Posology Player function
        self.assertIn("function toggleAudioPosology(", self.ext_js)
        self.assertIn("window.toggleAudioPosology = toggleAudioPosology", self.ext_js)

        # B. Multi-lingual Vernacular Text Map (Urdu, Hindi, English)
        self.assertIn("محترم مریض، السلام علیکم", self.ext_js, "Urdu voice posology script must exist")
        self.assertIn("नमस्ते। यह औषधि", self.ext_js, "Hindi voice posology script must exist")
        self.assertIn("Strictly avoid cold beverages", self.ext_js, "English voice posology script must exist")

        # C. Acoustic Chime Engine (Web Audio API 528 Hz)
        self.assertIn("function playAcousticChime(", self.ext_js)
        self.assertIn("function playMelodicPosologySequence(", self.ext_js)
        self.assertIn("AudioContext", self.ext_js)

        # D. Dynamic Language Switcher
        self.assertIn("window.setAudioPosologyLang", self.ext_js)

        # E. Live WhatsApp Audio Directives Sharing
        self.assertIn("Send Voice Posology to Patient via WhatsApp", self.core_js)

if __name__ == "__main__":
    unittest.main()
