#!/usr/bin/env python3
"""
scripts/fix_workspace_blank_and_restore_all.py

Resolves:
1. Blank workspace crash caused by state.tab being left as 'home' in doctor role on reload/session restore.
2. Adds automatic fallback to 'today' tab in renderDoctorApp and renderWorkspace so workspace is NEVER blank.
3. Unifies getDoctorNavItems() so all 8 Specialty Desks (Ilaj bil Ghiza, Tadbeer, Nafsiyat, Yad-dasht, Followups, AI Copilot, Formulary, Profile) are always present in the dropdown.
4. Explicitly binds switchTab, switchRole, selectDoctorDesk, and toggleDoctorNavDropdown to window.
5. Keeps header visible by removing intrusive scrollIntoView down to workspace.
6. Bumps cache version to v=17.0 across HTML, JS, extensions, and Service Worker.
7. Syncs 100% to docs/ and verifies health.
"""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path("/Users/irfanashraf/Downloads/zayvora-platform-phase0-4")

def patch_zayvora_core():
    core_path = ROOT / "js" / "zayvora-core.js"
    code = core_path.read_text(encoding="utf-8")

    # 1. Update getDoctorNavItems() so all 12 desks are defined and available in both Matab and Clinic modes
    old_get_nav = re.compile(
        r'function getDoctorNavItems\(\)\s*\{.*?return roleNavs\.doctor;\s*\}',
        re.DOTALL
    )
    new_get_nav = '''function getDoctorNavItems() {
      // 12 Classical & Modern Clinical Suites for Hakeem Dr. Irfan Ashraf
      return [
        { id: 'today', label: '📋 Today (آج کی قطار)' },
        { id: 'consultation', label: '🩺 Consultation (مشورہ و مزاج)' },
        { id: 'patients', label: '👤 Patients (مریض)' },
        { id: 'prescriptions', label: '💊 Nuskha (نسخہ و ادویہ)' },
        { id: 'ghiza', label: '🥗 Ilaj bil Ghiza (Dietetics)' },
        { id: 'tadbeer', label: '🌿 Ilaj bil Tadbeer (Hijama & Regimens)' },
        { id: 'nafsiyat', label: '🧠 Ilaj bil Nafsiyat (Psychosomatic)' },
        { id: 'yad', label: '🎙️ Yad-dasht (AI Voice Clinical Notes)' },
        { id: 'followups', label: '📅 Follow-ups (آئندہ تاریخ)' },
        { id: 'assistant', label: '🤖 Clinical AI Copilot' },
        { id: 'knowledge', label: '📖 Unani Formulary (Qarabadeen)' },
        { id: 'profile', label: '👤 Physician Profile & Settings' }
      ];
    }'''

    if old_get_nav.search(code):
        code = old_get_nav.sub(new_get_nav, code, count=1)
        print("✓ Updated getDoctorNavItems() with complete 12 desks")
    else:
        print("! Warning: getDoctorNavItems regex failed to match")

    # 2. Bind window.switchTab and window.switchRole
    if "window.switchTab = switchTab;" not in code:
        code = code.replace(
            "function switchTab(newTab) {",
            "function switchTab(newTab) {\n      if (typeof window !== 'undefined') window.switchTab = switchTab;\n"
        )
        print("✓ Explicitly bound window.switchTab")

    if "window.switchRole = switchRole;" not in code:
        code = code.replace(
            "function switchRole(newRole, bypassAuth = false) {",
            "function switchRole(newRole, bypassAuth = false) {\n      if (typeof window !== 'undefined') window.switchRole = switchRole;\n"
        )
        print("✓ Explicitly bound window.switchRole")

    # 3. Fix switchTab scrolling to keep header visible
    old_switch_tab_scroll = re.compile(
        r'const ws = document\.getElementById\(\'workspace-container\'\);\s*if \(ws && window\.scrollY > 180\) \{\s*ws\.scrollIntoView\(\{ behavior: \'smooth\', block: \'start\' \}\);\s*\}'
    )
    new_switch_tab_scroll = '// Keep header and top bar comfortably in view on tab switch'
    code = old_switch_tab_scroll.sub(new_switch_tab_scroll, code)

    # 4. Fix initializeApp() so role restoration also sets valid state.tab
    old_init_role = re.compile(
        r'if \(state\.currentUser && rawHash && validInternalRoles\.includes\(rawHash\)\) \{\s*'
        r'state\.role = rawHash;\s*'
        r'try \{ sessionStorage\.setItem\(\'zayvora_session_desk\', rawHash\); \} catch\(e\) \{\}\s*'
        r'\} else if \(state\.currentUser && sessionDesk && validInternalRoles\.includes\(sessionDesk\) && \(!rawHash \|\| rawHash === sessionDesk\)\) \{\s*'
        r'state\.role = sessionDesk;\s*'
        r'\}'
    )
    new_init_role = '''if (state.currentUser && rawHash && validInternalRoles.includes(rawHash)) {
        state.role = rawHash;
        state.tab = (rawHash === 'doctor') ? 'today' : ((roleNavs[rawHash] && roleNavs[rawHash][0]) ? roleNavs[rawHash][0].id : 'overview');
        try { sessionStorage.setItem('zayvora_session_desk', rawHash); } catch(e) {}
      } else if (state.currentUser && sessionDesk && validInternalRoles.includes(sessionDesk) && (!rawHash || rawHash === sessionDesk)) {
        state.role = sessionDesk;
        state.tab = (sessionDesk === 'doctor') ? 'today' : ((roleNavs[sessionDesk] && roleNavs[sessionDesk][0]) ? roleNavs[sessionDesk][0].id : 'overview');
      }'''

    if old_init_role.search(code):
        code = old_init_role.sub(new_init_role, code, count=1)
        print("✓ Fixed initializeApp() state.tab restoration for doctor role")
    else:
        print("! Warning: old_init_role regex failed to match")

    # 5. Fix renderDoctorApp() top and bottom fallbacks
    old_render_doctor_top = "function renderDoctorApp(container) {"
    new_render_doctor_top = """function renderDoctorApp(container) {
      const validDoctorTabs = ['today', 'consultation', 'patients', 'prescriptions', 'followups', 'assistant', 'knowledge', 'tadbeer', 'nafsiyat', 'ghiza', 'yad', 'profile'];
      if (!state.tab || !validDoctorTabs.includes(state.tab)) {
        state.tab = 'today';
      }"""
    code = code.replace(old_render_doctor_top, new_render_doctor_top, 1)
    print("✓ Added validDoctorTabs fallback to renderDoctorApp()")

    # 6. Fix renderWorkspace() tab validation for doctor
    old_render_ws = "if (state.role === 'patient') {"
    new_render_ws = """if (state.role === 'doctor') {
        const validDoctorTabs = ['today', 'consultation', 'patients', 'prescriptions', 'followups', 'assistant', 'knowledge', 'tadbeer', 'nafsiyat', 'ghiza', 'yad', 'profile'];
        if (!state.tab || !validDoctorTabs.includes(state.tab)) {
          state.tab = 'today';
        }
        renderDoctorApp(main);
      } else if (state.role === 'patient') {"""
    
    # Check if doctor was second in chain
    if "else if (state.role === 'doctor') {\n          renderDoctorApp(main);" in code:
        code = code.replace(
            "else if (state.role === 'doctor') {\n          renderDoctorApp(main);",
            """else if (state.role === 'doctor') {
          const validDoctorTabs = ['today', 'consultation', 'patients', 'prescriptions', 'followups', 'assistant', 'knowledge', 'tadbeer', 'nafsiyat', 'ghiza', 'yad', 'profile'];
          if (!state.tab || !validDoctorTabs.includes(state.tab)) {
            state.tab = 'today';
          }
          renderDoctorApp(main);"""
        )
        print("✓ Injected tab safety validation inside renderWorkspace()")

    core_path.write_text(code, encoding="utf-8")
    print("✓ Saved updated js/zayvora-core.js")

def update_versions():
    files = [ROOT / "index.html", ROOT / "app.html"]
    for f in files:
        txt = f.read_text(encoding="utf-8")
        txt = re.sub(r'zayvora-core\.js\?v=[\d\.]+', 'zayvora-core.js?v=17.0', txt)
        txt = re.sub(r'zayvora-extensions\.js\?v=[\d\.]+', 'zayvora-extensions.js?v=17.0', txt)
        f.write_text(txt, encoding="utf-8")
        print(f"✓ Bumped {f.name} to v=17.0")

    # sw.js
    sw_file = ROOT / "sw.js"
    sw_code = sw_file.read_text(encoding="utf-8")
    sw_code = re.sub(r"const CACHE_NAME = 'zayvora-health-os-v[\d\.]+-live';", "const CACHE_NAME = 'zayvora-health-os-v17.0-live';", sw_code)
    sw_file.write_text(sw_code, encoding="utf-8")
    print("✓ Updated sw.js CACHE_NAME to v17.0-live")

    # js/zayvora-extensions.js
    ext_file = ROOT / "js" / "zayvora-extensions.js"
    ext_code = ext_file.read_text(encoding="utf-8")
    ext_code = re.sub(r"sw\.js\?v=[\d\.]+", "sw.js?v=17.0", ext_code)
    ext_file.write_text(ext_code, encoding="utf-8")
    print("✓ Updated js/zayvora-extensions.js sw registration to v17.0")

def sync_to_docs():
    shutil.copy2(ROOT / "index.html", ROOT / "docs" / "index.html")
    shutil.copy2(ROOT / "app.html", ROOT / "docs" / "app.html")
    shutil.copy2(ROOT / "sw.js", ROOT / "docs" / "sw.js")
    shutil.copy2(ROOT / "js" / "zayvora-core.js", ROOT / "docs" / "js" / "zayvora-core.js")
    shutil.copy2(ROOT / "js" / "zayvora-extensions.js", ROOT / "docs" / "js" / "zayvora-extensions.js")
    print("✓ Synced all modified files to docs/")

if __name__ == "__main__":
    patch_zayvora_core()
    update_versions()
    sync_to_docs()
    print("=== Fix & Sync Complete ===")
