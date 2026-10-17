import os
import re
import unittest

class TestPracticalClinicalEnhancements(unittest.TestCase):
    """
    Practical verification for all newly added clinical and patient-friendly features:
    1. Dual Platform Edition Switcher (Clinic Mode vs Flagship HQ)
    2. 8 One-Click Fast Matab Classical Protocols with Vernacular Scripts (Urdu & Hindi)
    3. Dedicated 1-Page A4 Prescription Print Layout
    4. 1-Click WhatsApp Sharing for OPD Tokens and Prescriptions
    5. Visual Graphic Mizaj Report Card Modal with Elemental & Akhlat Meters
    """

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.index_path = os.path.join(self.base_dir, "index.html")
        self.core_js_path = os.path.join(self.base_dir, "js", "zayvora-core.js")
        
        with open(self.index_path, "r", encoding="utf-8") as f:
            self.index_html = f.read()
            
        with open(self.core_js_path, "r", encoding="utf-8") as f:
            self.core_js = f.read()

    def test_01_dual_platform_edition_switcher(self):
        """Test Dual Edition switcher UI elements, state and functions."""
        # 1. HTML elements in header
        self.assertIn('id="header-edition-badge"', self.index_html, "Header edition badge must exist in DOM")
        self.assertIn('id="btn-edition-clinic"', self.index_html, "Clinic edition button must exist")
        self.assertIn('id="btn-edition-enterprise"', self.index_html, "Enterprise edition button must exist")
        
        # 2. State & functions in JS
        self.assertIn("platformEdition:", self.core_js, "platformEdition property must exist in state")
        self.assertIn("function setPlatformEdition(", self.core_js, "setPlatformEdition function must exist")
        self.assertIn("function togglePlatformEditionFromModal(", self.core_js, "togglePlatformEditionFromModal function must exist")
        self.assertIn("function updateEditionUI(", self.core_js, "updateEditionUI function must exist")
        self.assertIn("function getDoctorNavItems(", self.core_js, "getDoctorNavItems function must exist")
        
        # 3. Mode filter validation in getDoctorNavItems
        self.assertIn("state.platformEdition === 'clinic'", self.core_js, "getDoctorNavItems must filter based on clinic edition")

    def test_02_all_8_master_protocols_in_fast_matab(self):
        """Test that all 8 master disease protocols exist in both applyFastProtocol logic and Fast Matab UI."""
        protocols = [
            'arthri', 'gastro', 'ceph', 'metabolic',
            'respiratory', 'liver', 'vitality', 'skin'
        ]
        
        # Check function exists
        self.assertIn("function applyFastProtocol(protocolId)", self.core_js)
        
        # Check each protocol branch in applyFastProtocol
        for p in protocols:
            self.assertIn(f"protocolId === '{p}'", self.core_js, f"Protocol '{p}' must be handled in applyFastProtocol")
            self.assertIn(f"applyFastProtocol('{p}')", self.core_js, f"Protocol button '{p}' must exist in Fast Matab UI")
            
        # Check that vernacular scripts (Urdu & Hindi) are present in formulations
        self.assertIn("معجون سرنجان", self.core_js, "Urdu script for Majun Suranjan must be present")
        self.assertIn("माजून सुरंजान", self.core_js, "Hindi script for Majun Suranjan must be present")
        self.assertIn("جوارش کمونی", self.core_js, "Urdu script for Jawarish Kamuni must be present")
        self.assertIn("شربت بنفشہ", self.core_js, "Urdu script for Sharbat Banafsha must be present")
        self.assertIn("شربت عناب", self.core_js, "Urdu script for Sharbat Unnab must be present")
        
        # Check that parhez text input is populated
        self.assertIn("parhezInput.value =", self.core_js, "applyFastProtocol must auto-fill dietary restrictions")

    def test_03_prescription_slip_and_a4_print_styling(self):
        """Test bilingual prescription slip modal and print layout."""
        self.assertIn('id="bilingual-rx-slip-modal"', self.index_html, "Bilingual Rx slip modal must exist")
        self.assertIn("BUMS/AMU", self.index_html, "Doctor registration must be rendered on Rx slip")
        self.assertIn("21 CFR Part 11", self.index_html, "Prescription must have statutory audit signature")
        
        # Check print CSS rules
        self.assertIn("@media print", self.index_html, "Dedicated print stylesheet must exist")
        self.assertIn("#bilingual-rx-slip-modal", self.index_html, "Print CSS must specifically target Rx slip modal")

    def test_04_whatsapp_sharing_for_tokens_and_prescriptions(self):
        """Test WhatsApp sharing function and presence of action buttons."""
        # 1. Functions exist
        self.assertIn("function sendTokenViaWhatsApp(", self.core_js, "sendTokenViaWhatsApp function must exist")
        self.assertIn("function sendRxViaWhatsApp(", self.core_js, "sendRxViaWhatsApp function must exist")
        
        # 2. Correct wa.me URL formation
        self.assertIn("https://wa.me/", self.core_js, "WhatsApp functions must target official https://wa.me/ API")
        self.assertIn("encodeURIComponent", self.core_js, "WhatsApp text must be properly URL-encoded")
        
        # 3. Action buttons in Queue and Appointments
        self.assertIn("sendTokenViaWhatsApp('A-12', 'Hamza Farooqi'", self.core_js, "Appointments table must have WhatsApp token button")
        self.assertIn("sendTokenViaWhatsApp('${t.token}'", self.core_js, "Queue token cards must have WhatsApp token button")

    def test_05_visual_mizaj_report_card(self):
        """Test Visual Graphic Mizaj Report Card modal and computational engine."""
        # 1. Modal in HTML
        self.assertIn('id="visual-mizaj-card-modal"', self.index_html, "Visual Mizaj Card Modal container must exist")
        self.assertIn('id="visual-mizaj-card-content"', self.index_html, "Visual Mizaj Card Content container must exist")
        
        # 2. Calculation logic
        self.assertIn("function calculateDetailedMizaj(", self.core_js, "calculateDetailedMizaj function must exist")
        self.assertIn("percentages.damawi", self.core_js, "calculateDetailedMizaj must compute Damawi percentage")
        self.assertIn("percentages.balghami", self.core_js, "calculateDetailedMizaj must compute Balghami percentage")
        self.assertIn("percentages.safrawi", self.core_js, "calculateDetailedMizaj must compute Safrawi percentage")
        self.assertIn("percentages.sawdawi", self.core_js, "calculateDetailedMizaj must compute Sawdawi percentage")
        
        # 3. Rendering and sharing functions
        self.assertIn("function renderVisualMizajCard(", self.core_js, "renderVisualMizajCard function must exist")
        self.assertIn("function openVisualMizajCardModal(", self.core_js, "openVisualMizajCardModal function must exist")
        self.assertIn("function shareVisualMizajCardWhatsApp(", self.core_js, "shareVisualMizajCardWhatsApp function must exist")

if __name__ == "__main__":
    unittest.main()
