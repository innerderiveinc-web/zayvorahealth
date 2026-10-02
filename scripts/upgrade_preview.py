import re
import os

with open("docs/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update phone numbers
html = html.replace("+91 1800-ZAYVORA", "+91 97738 82657")
html = html.replace("1800-ZAYVORA", "+91 97738 82657")

# 2. Update role-selector default in HTML
old_selector_part = """<select id="role-selector" onchange="switchRole(this.value)" class="bg-transparent text-xs font-semibold text-emerald-400 focus:outline-none cursor-pointer">
            <option value="doctor" selected>🩺 Hakim Dr. Tariq Mansoor (Doctor / Senior Tabeeb)</option>
            <option value="patient">👤 Hamza Farooqi (Patient Health 360)</option>
            <option value="clinic">🏥 Sana Khan (Clinic Receptionist & OPD)</option>
            <option value="pharmacy">💊 Zainab Ali (Clinical Pharmacist & FEFO)</option>
            <option value="manufacturing">🏭 Dr. Arshad Qureshi (Manufacturing QA/QC & BMR)</option>
            <option value="research">🔬 Dr. K. Saxena (Clinical Researcher & RWE)</option>
            <option value="enterprise">🏢 Hakeem Abdul Majeed (Enterprise Owner / Chairman)</option>
            <option value="admin">🛡️ Platform Administrator (System Admin & IT)</option>
            <option value="website">🌐 Public Website (25 Canonical Pages)</option>
            <option value="herbals">🌿 ZAYVORA Herbals (10 Formulations Store & Cart)</option>
            <option value="mobile">📱 ZAYVORA Mobile App (React Native / Expo Simulator)</option>
            <option value="hardware">🔬 Clinical Hardware & IoT Lab (Nabz, Lisan, Cold-Chain)</option>
          </select>"""

new_selector_part = """<select id="role-selector" onchange="switchRole(this.value)" class="bg-transparent text-xs font-semibold text-emerald-400 focus:outline-none cursor-pointer">
            <option value="website" selected>🌐 ZAYVORA Health™ Public Website (Official Landing Page)</option>
            <option value="doctor">🩺 Hakim Dr. Tariq Mansoor (Doctor Consultation Cockpit)</option>
            <option value="patient">👤 Hamza Farooqi (Patient Health 360 & Regimen)</option>
            <option value="clinic">🏥 Sana Khan (Clinic Receptionist & OPD Queue)</option>
            <option value="pharmacy">💊 Zainab Ali (Clinical Pharmacist & FEFO Dispensary)</option>
            <option value="manufacturing">🏭 Dr. Arshad Qureshi (Manufacturing QA/QC & BMR)</option>
            <option value="research">🔬 Dr. K. Saxena (Clinical Researcher & RWE Registry)</option>
            <option value="enterprise">🏢 Hakeem Abdul Majeed (Enterprise Owner / Chairman)</option>
            <option value="admin">🛡️ Platform Administrator (System Admin & IT)</option>
            <option value="herbals">🌿 ZAYVORA Herbals (10 Formulations Store & Cart)</option>
            <option value="mobile">📱 ZAYVORA Mobile App (React Native / Expo Simulator)</option>
            <option value="hardware">🔬 Clinical Hardware & IoT Lab (Nabz, Lisan, Cold-Chain)</option>
          </select>"""

if old_selector_part in html:
    html = html.replace(old_selector_part, new_selector_part)
    print("✓ Role selector updated")
else:
    print("! Role selector not matched exactly, trying regex")
    html = re.sub(
        r'<select id="role-selector".*?</select>',
        new_selector_part,
        html,
        flags=re.DOTALL
    )

# 3. Update top search, notifications, and language buttons
old_search_btn = """<button onclick="showNotification('Global search active: Type Ctrl+K to search Patients, Rx, Protocols, Medicines.')" class="px-2.5 py-1 rounded-xl bg-[var(--background)] border border-[var(--border)] text-xs text-[var(--muted)] hover:border-[#2DD4BF] flex items-center gap-1.5 transition">
            <span>🔍</span> <span class="hidden sm:inline">Search...</span> <kbd class="px-1 py-0.2 rounded bg-[var(--card)] text-[9px] font-mono">⌘K</kbd>
          </button>"""
new_search_btn = """<button onclick="toggleSearchModal()" class="px-2.5 py-1 rounded-xl bg-[var(--background)] border border-[var(--border)] text-xs text-[var(--muted)] hover:border-[#2DD4BF] flex items-center gap-1.5 transition" title="Search Patients, Rx, Protocols (⌘K)">
            <span>🔍</span> <span class="hidden sm:inline">Search...</span> <kbd class="px-1 py-0.2 rounded bg-[var(--card)] text-[9px] font-mono">⌘K</kbd>
          </button>"""
html = html.replace(old_search_btn, new_search_btn)

old_notif_btn = """<button onclick="showNotification('3 Clinical & System Alerts Pending: 1 Drug Interaction, 1 Lab Value, 1 Refill.')" class="relative p-1.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-xs hover:border-[#2DD4BF] transition" title="Notifications">
            🔔<span class="absolute -top-1 -right-1 w-3.5 h-3.5 rounded-full bg-rose-500 text-white font-bold text-[8px] flex items-center justify-center">3</span>
          </button>"""
new_notif_btn = """<button onclick="toggleNotificationsModal()" class="relative p-1.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-xs hover:border-[#2DD4BF] transition" title="Notifications">
            🔔<span id="header-notif-badge" class="absolute -top-1 -right-1 w-3.5 h-3.5 rounded-full bg-rose-500 text-white font-bold text-[8px] flex items-center justify-center">3</span>
          </button>"""
html = html.replace(old_notif_btn, new_notif_btn)

old_lang_box = """<div class="flex items-center bg-[var(--background)] rounded-xl border border-[var(--border)] p-0.5 text-[10px] font-bold">
            <button onclick="showNotification('Language: English')" class="px-2 py-0.5 rounded-lg bg-[var(--card)] text-[#2DD4BF]">EN</button>
            <button onclick="showNotification('Language: Hindi (हिन्दी)')" class="px-2 py-0.5 rounded-lg text-[var(--muted)] hover:text-white">HI</button>
            <button onclick="showNotification('Language: Urdu (اردو)')" class="px-2 py-0.5 rounded-lg text-[var(--muted)] hover:text-white">UR</button>
          </div>"""
new_lang_box = """<div class="flex items-center bg-[var(--background)] rounded-xl border border-[var(--border)] p-0.5 text-[10px] font-bold">
            <button id="lang-btn-en" onclick="switchLanguage('en')" class="px-2 py-0.5 rounded-lg bg-[var(--card)] text-[#2DD4BF]">EN</button>
            <button id="lang-btn-hi" onclick="switchLanguage('hi')" class="px-2 py-0.5 rounded-lg text-[var(--muted)] hover:text-white">HI</button>
            <button id="lang-btn-ur" onclick="switchLanguage('ur')" class="px-2 py-0.5 rounded-lg text-[var(--muted)] hover:text-white">UR</button>
          </div>"""
html = html.replace(old_lang_box, new_lang_box)

# 4. Update initial state to role: 'website', tab: 'home'
html = html.replace("role: 'doctor',", "role: 'website',")
html = html.replace("tab: 'today',", "tab: 'home',")

print("Upgraded base HTML tokens")
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html)
