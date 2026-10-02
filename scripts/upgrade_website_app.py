import re

with open("docs/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update roleNavs.website
old_role_nav_website = """      website: [
        { id: 'home', label: '🌐 Public Home' },
        { id: 'pages25', label: '📑 25 Canonical Pages Directory' },
        { id: 'philosophy', label: '🌿 Clinical Philosophy' },
        { id: 'care_journey', label: '🗺️ 12-Step Care Journey' },
        { id: 'knowledge', label: '📚 Knowledge Centre' }
      ],"""

new_role_nav_website = """      website: [
        { id: 'home', label: '🌐 Home' },
        { id: 'about', label: '🏛️ About' },
        { id: 'services', label: '🩺 Services' },
        { id: 'products', label: '🌿 Products' },
        { id: 'research', label: '🔬 Research & RWE' },
        { id: 'philosophy', label: '📜 Clinical Philosophy' },
        { id: 'care_journey', label: '🗺️ 12-Step Continuum' },
        { id: 'clinics', label: '🏥 Clinics & Matab' },
        { id: 'doctors', label: '👨‍⚕️ Clinicians' },
        { id: 'knowledge', label: '📚 Knowledge Centre' },
        { id: 'faqs', label: '❓ FAQs' },
        { id: 'contact', label: '📞 Contact' },
        { id: 'pages25', label: '📑 All 25 Pages Directory' }
      ],"""

if old_role_nav_website in html:
    html = html.replace(old_role_nav_website, new_role_nav_website)
    print("✓ roleNavs.website updated")
else:
    print("! roleNavs.website exact match failed")

# 2. Add state.alerts and state.unreadAlerts
if "const state = {" in html:
    html = html.replace(
        "const state = {",
        """const state = {
      lang: 'en',
      unreadAlerts: 3,
      alerts: [
        { id: 'ALT-1', level: 'CRITICAL', title: 'Azaraqi (Mudabbar) + CNS Sedative Warning', desc: 'Patient Hamza Farooqi: Must not co-administer without 6h spacing and Kateera corrective.', acknowledged: false },
        { id: 'ALT-2', level: 'LAB', title: 'Elevated Fasting Blood Glucose (118 mg/dL)', desc: 'Patient Hamza Farooqi: Su-e-Mizaj Barid Balghami correlation noted. Dietary parhez issued.', acknowledged: false },
        { id: 'ALT-3', level: 'INVENTORY', title: 'Batch Expiring in 60 Days: Majun Suranjan', desc: 'Dispensary Batch BATCH-MS-2026-0441 has 142 units remaining. Prioritize FEFO dispatch.', acknowledged: false }
      ],"""
    )
    print("✓ state.alerts initialized")

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html)
