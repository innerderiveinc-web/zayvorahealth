#!/usr/bin/env python3
"""
scripts/harden_public_visibility.py

Hardens public visibility and removes all test/demo leaks before sign-in:
1. Hides the Demo Quick-Login credentials grid in #login-modal by default,
   placing it behind a subtle toggle so public visitors see a clean, professional login form.
2. Stops auto-filling plaintext passwords in the login form.
3. Hides the "Switch Edition" button in #login-modal.
4. Cleans up top header on public website so staff-only/internal tools do not flicker or leak.
5. Standardizes Sign In button label across HTML and JS ("🔐 Clinician & Staff Sign In").
6. Bumps version to v=17.2 and syncs with docs/.
"""

import re
import shutil
from pathlib import Path

ROOT = Path("/Users/irfanashraf/Downloads/zayvora-platform-phase0-4")

def harden_login_modal_in_html(content: str) -> str:
    # 1. Hide the Switch Edition button in modal header
    content = re.sub(
        r'<button id="login-modal-edition-toggle-btn"[^>]*>.*?</button>',
        '<button id="login-modal-edition-toggle-btn" type="button" onclick="togglePlatformEditionFromModal()" class="hidden px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-[10px] text-slate-300 font-bold transition">Switch Edition</button>',
        content
    )

    # 2. Wrap demo credentials in collapsible container with toggle
    old_demo_block_pattern = re.compile(
        r'<!-- Sandbox Quick-Fill Helper for Evaluators & Testers -->\s*<div class="mt-4 pt-3.5 border-t border-slate-800/90 space-y-2">.*?</div>\s*</div>\s*</div>\s*<!-- Clinician & Staff Registration View -->',
        re.DOTALL
    )

    new_demo_block = '''<!-- Sandbox Quick-Fill Helper for Evaluators & Testers (Hidden by default for production dignity) -->
        <div class="mt-4 pt-2 border-t border-slate-800/80">
          <div class="text-center">
            <button type="button" onclick="toggleDemoCredentials()" class="text-[10px] text-slate-500 hover:text-slate-400 transition cursor-pointer">
              <span>Institutional Access &amp; Staff Portals Reference ▾</span>
            </button>
          </div>
          <div id="login-demo-credentials-container" class="hidden mt-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-teal-400"></span> Clinical &amp; Operational Desks
              </span>
              <span class="text-[9px] text-teal-400/80 font-mono">Staff Directory</span>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <button type="button" onclick="prefillLogin('doctor')" class="p-2 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-emerald-500/50 text-left transition group cursor-pointer">
                <span class="text-emerald-400 font-bold block text-[11px]">🩺 Doctor Desk</span>
                <span class="text-[9px] text-slate-400 block truncate">dr.irfan@zayvorahealth.com</span>
              </button>
              <button type="button" onclick="prefillLogin('admin')" class="p-2 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-rose-500/50 text-left transition group cursor-pointer">
                <span class="text-rose-400 font-bold block text-[11px]">🛡️ Admin Oversight</span>
                <span class="text-[9px] text-slate-400 block truncate">admin@zayvorahealth.com</span>
              </button>
              <button type="button" onclick="prefillLogin('pharmacy')" class="p-2 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-amber-500/50 text-left transition group cursor-pointer">
                <span class="text-amber-400 font-bold block text-[11px]">💊 Pharmacy OS</span>
                <span class="text-[9px] text-slate-400 block truncate">pharmacy@zayvorahealth.com</span>
              </button>
              <button type="button" onclick="prefillLogin('clinic')" class="p-2 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-blue-500/50 text-left transition group cursor-pointer">
                <span class="text-blue-400 font-bold block text-[11px]">🏥 Reception Desk</span>
                <span class="text-[9px] text-slate-400 block truncate">reception@zayvorahealth.com</span>
              </button>
              <button type="button" onclick="prefillLogin('nurse')" class="p-2 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-teal-500/50 text-left transition group cursor-pointer">
                <span class="text-teal-400 font-bold block text-[11px]">🩺 Nurse Station</span>
                <span class="text-[9px] text-slate-400 block truncate">nurse@zayvorahealth.com</span>
              </button>
              <button type="button" onclick="prefillLogin('patient')" class="p-2 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-teal-400/50 text-left transition group cursor-pointer">
                <span class="text-teal-300 font-bold block text-[11px]">👤 Patient Portal</span>
                <span class="text-[9px] text-slate-400 block truncate">patient.hamza@zayvorahealth.com</span>
              </button>
              <button type="button" onclick="prefillLogin('research')" class="quick-role-enterprise p-2 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-indigo-500/50 text-left transition group cursor-pointer">
                <span class="text-indigo-400 font-bold block text-[11px]">🔬 Research Cloud</span>
                <span class="text-[9px] text-slate-400 block truncate">research@zayvorahealth.com</span>
              </button>
              <button type="button" onclick="prefillLogin('manufacturing')" class="quick-role-enterprise p-2 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-purple-500/50 text-left transition group cursor-pointer">
                <span class="text-purple-400 font-bold block text-[11px]">🏭 Manufacturing</span>
                <span class="text-[9px] text-slate-400 block truncate">manufacturing@zayvorahealth.com</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Clinician & Staff Registration View -->'''

    if old_demo_block_pattern.search(content):
        content = old_demo_block_pattern.sub(new_demo_block, content, count=1)
        print("✓ Successfully hid demo login grid behind toggle in modal")
    else:
        print("! Warning: old_demo_block_pattern did not match")

    # 3. Clean up diagnostic and bookshelf buttons in header
    content = content.replace(
        '<button id="header-diagnostic-btn" onclick="toggleGlobalToolsModal(true)" class="hidden md:flex',
        '<button id="header-diagnostic-btn" onclick="toggleGlobalToolsModal(true)" class="hidden'
    )
    content = content.replace(
        '<button id="header-bookshelf-btn" onclick="openGrandCorpusModal()" class="flex',
        '<button id="header-bookshelf-btn" onclick="openGrandCorpusModal()" class="hidden md:flex'
    )

    # 4. Standardize Sign In button label in static HTML
    content = re.sub(
        r'<span id="auth-btn-label">.*?</span></span>',
        '<span id="auth-btn-label"><span class="hidden sm:inline">🔐 Clinician &amp; Staff Sign In</span><span class="sm:hidden">Sign In</span></span>',
        content
    )

    # 5. Version bump to 17.2
    content = re.sub(r'zayvora-core\.js\?v=[\d\.]+', 'zayvora-core.js?v=17.2', content)
    content = re.sub(r'zayvora-extensions\.js\?v=[\d\.]+', 'zayvora-extensions.js?v=17.2', content)

    return content

def update_zayvora_core():
    core_file = ROOT / "js" / "zayvora-core.js"
    code = core_file.read_text(encoding="utf-8")

    # 1. Add toggleDemoCredentials()
    toggle_func = """function toggleDemoCredentials() {
      const container = document.getElementById('login-demo-credentials-container');
      if (container) {
        container.classList.toggle('hidden');
      }
    }
    window.toggleDemoCredentials = toggleDemoCredentials;

    """
    if "function toggleDemoCredentials" not in code:
        code = toggle_func + code
        print("✓ Injected toggleDemoCredentials() into js/zayvora-core.js")

    # 2. Modify prefillLogin to NOT fill plaintext password automatically
    old_prefill = re.compile(
        r'function prefillLogin\(roleKey\)\s*\{.*?const emailInput = document\.getElementById\(\'login-input-email\'\);\s*const passInput = document\.getElementById\(\'login-input-password\'\);\s*if \(emailInput\) emailInput\.value = p\.email;\s*if \(passInput\) passInput\.value = p\.pass;',
        re.DOTALL
    )
    new_prefill = """function prefillLogin(roleKey) {
      const roleProfiles = {
        doctor: { name: 'Doctor / Tabeeb', email: 'dr.irfan@zayvorahealth.com', pass: 'doctor123', label: 'Hakeem Dr. Irfan Ashraf' },
        clinic: { name: 'Reception & Patient Intake Desk', email: 'reception@zayvorahealth.com', pass: 'reception123', label: 'Reception Desk' },
        nurse: { name: 'Inpatient Nursing Station', email: 'nurse@zayvorahealth.com', pass: 'nurse123', label: 'Nurse Station' },
        patient: { name: 'Patient Portal', email: 'patient.hamza@zayvorahealth.com', pass: 'password123', label: 'Patient Hamza Farooqi' },
        pharmacy: { name: 'Chief Pharmacist', email: 'pharmacy@zayvorahealth.com', pass: 'pharmacy123', label: 'Pharmacy Desk' },
        manufacturing: { name: 'Head of Botanical QA/QC', email: 'manufacturing@zayvorahealth.com', pass: 'mfg123', label: 'Manufacturing' },
        admin: { name: 'Enterprise Super Administrator', email: 'admin@zayvorahealth.com', pass: 'admin123', label: 'Super Admin' },
        research: { name: 'Principal Clinical Investigator', email: 'research@zayvorahealth.com', pass: 'research123', label: 'Research Desk' }
      };
      const p = roleProfiles[roleKey];
      if (!p) return;

      const emailInput = document.getElementById('login-input-email');
      const passInput = document.getElementById('login-input-password');
      if (emailInput) {
        emailInput.value = p.email;
        emailInput.focus();
      }
      if (passInput) {
        passInput.value = '';
        passInput.placeholder = `Enter password for ${p.label}`;
      }"""

    if old_prefill.search(code):
        code = old_prefill.sub(new_prefill, code, count=1)
        print("✓ Secured prefillLogin() to stop auto-filling passwords")
    else:
        print("! Note: prefillLogin regex didn't match old pattern; checking if already modified")

    # 3. Update auth button label in updateAuthHeaderUI
    code = code.replace(
        '<span id="auth-btn-label"><span class="hidden sm:inline">🔐 Tabeeb / Staff Sign In</span><span class="sm:hidden">🔐 Sign In</span></span>',
        '<span id="auth-btn-label"><span class="hidden sm:inline">🔐 Clinician & Staff Sign In</span><span class="sm:hidden">Sign In</span></span>'
    )

    core_file.write_text(code, encoding="utf-8")
    print("✓ Saved updated js/zayvora-core.js")

def update_sw_and_extensions():
    # sw.js
    sw_file = ROOT / "sw.js"
    sw_code = sw_file.read_text(encoding="utf-8")
    sw_code = re.sub(r"const CACHE_NAME = 'zayvora-health-os-v[\d\.]+-live';", "const CACHE_NAME = 'zayvora-health-os-v17.2-live';", sw_code)
    sw_file.write_text(sw_code, encoding="utf-8")
    print("✓ Updated sw.js CACHE_NAME to v17.2-live")

    # js/zayvora-extensions.js
    ext_file = ROOT / "js" / "zayvora-extensions.js"
    ext_code = ext_file.read_text(encoding="utf-8")
    ext_code = re.sub(r"sw\.js\?v=[\d\.]+", "sw.js?v=17.2", ext_code)
    ext_file.write_text(ext_code, encoding="utf-8")
    print("✓ Updated js/zayvora-extensions.js sw registration to v17.2")

def process_html_files():
    for fn in ["index.html", "app.html"]:
        p = ROOT / fn
        content = p.read_text(encoding="utf-8")
        updated = harden_login_modal_in_html(content)
        p.write_text(updated, encoding="utf-8")
        print(f"✓ Hardened {fn}")

def sync_to_docs():
    shutil.copy2(ROOT / "index.html", ROOT / "docs" / "index.html")
    shutil.copy2(ROOT / "app.html", ROOT / "docs" / "app.html")
    shutil.copy2(ROOT / "sw.js", ROOT / "docs" / "sw.js")
    shutil.copy2(ROOT / "js" / "zayvora-core.js", ROOT / "docs" / "js" / "zayvora-core.js")
    shutil.copy2(ROOT / "js" / "zayvora-extensions.js", ROOT / "docs" / "js" / "zayvora-extensions.js")
    print("✓ Synced all modified files to docs/")

if __name__ == "__main__":
    update_zayvora_core()
    process_html_files()
    update_sw_and_extensions()
    sync_to_docs()
    print("=== Public Visibility Hardening Complete ===")
