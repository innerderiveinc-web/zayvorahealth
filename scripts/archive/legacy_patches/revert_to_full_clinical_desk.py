import os
import re

def revert_index_html():
    path = "index.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Restore header switcher buttons to original Clinic OS & Flagship HQ
    current_switcher = """        <button id="btn-edition-clinic" onclick="setPlatformEdition('clinic')" class="px-2.5 py-1 rounded-lg font-bold text-[11px] flex items-center gap-1.5 transition cursor-pointer bg-emerald-600 text-white shadow-sm ring-1 ring-emerald-400/40" title="ZAYVORA Matab Edition: Aasan OPD, Patient &amp; Prescription Desk">
          <span>🌿</span>
          <span class="hidden sm:inline">Matab (Clinic)</span>
          <span class="sm:hidden">Matab</span>
        </button>
        <button id="btn-edition-enterprise" onclick="setPlatformEdition('enterprise')" class="px-2.5 py-1 rounded-lg font-bold text-[11px] flex items-center gap-1.5 transition cursor-pointer text-slate-400 hover:text-white" title="ZAYVORA Flagship HQ: Full Sovereign R&amp;D, Manufacturing &amp; Clinical Trials">
          <span>🔬</span>
          <span class="hidden sm:inline">Research (HQ)</span>
          <span class="sm:hidden">Research</span>
        </button>"""

    original_switcher = """        <button id="btn-edition-clinic" onclick="setPlatformEdition('clinic')" class="px-2.5 py-1 rounded-lg font-bold text-[11px] flex items-center gap-1.5 transition cursor-pointer bg-emerald-600 text-white shadow-sm ring-1 ring-emerald-400/40" title="ZAYVORA Clinic OS: Simplified for Hospitals, Clinics &amp; Matabs">
          <span>🏥</span>
          <span class="hidden sm:inline">Clinic OS</span>
          <span class="sm:hidden">Clinic</span>
        </button>
        <button id="btn-edition-enterprise" onclick="setPlatformEdition('enterprise')" class="px-2.5 py-1 rounded-lg font-bold text-[11px] flex items-center gap-1.5 transition cursor-pointer text-slate-400 hover:text-white" title="ZAYVORA Flagship HQ: Full Sovereign R&amp;D, Manufacturing &amp; Clinical Trials">
          <span>🏛️</span>
          <span class="hidden sm:inline">Flagship HQ</span>
          <span class="sm:hidden">HQ</span>
        </button>"""

    if current_switcher in html:
        html = html.replace(current_switcher, original_switcher)
        print("[✓] index.html: Restored original Clinic OS & Flagship HQ switcher")
    else:
        # Regex replacement if exact whitespace differed
        html = re.sub(
            r'(<button id="btn-edition-clinic"[^>]*>)\s*<span>.*?</span>\s*<span class="hidden sm:inline">Matab \(Clinic\)</span>\s*<span class="sm:hidden">Matab</span>',
            r'\1\n          <span>🏥</span>\n          <span class="hidden sm:inline">Clinic OS</span>\n          <span class="sm:hidden">Clinic</span>',
            html
        )
        html = re.sub(
            r'(<button id="btn-edition-enterprise"[^>]*>)\s*<span>.*?</span>\s*<span class="hidden sm:inline">Research \(HQ\)</span>\s*<span class="sm:hidden">Research</span>',
            r'\1\n          <span>🏛️</span>\n          <span class="hidden sm:inline">Flagship HQ</span>\n          <span class="sm:hidden">HQ</span>',
            html
        )
        print("[✓] index.html: Restored via regex")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def revert_core_js():
    path = "js/zayvora-core.js"
    with open(path, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. Restore state consultationMode to 'continuum'
    js = js.replace(
        "consultationMode: (function() {\n        try { return localStorage.getItem('zayvora_consultation_mode') || 'fast'; } catch(e) { return 'fast'; }\n      })(),",
        "consultationMode: 'continuum',"
    )
    js = js.replace(
        "try { return localStorage.getItem('zayvora_consultation_mode') || 'fast'; } catch(e) { return 'fast'; }",
        "try { return localStorage.getItem('zayvora_consultation_mode') || 'continuum'; } catch(e) { return 'continuum'; }"
    )

    # 2. Restore badge text in updateEditionUI
    js = js.replace("badge.textContent = 'MATAB CLINIC OS™';", "badge.textContent = 'CLINIC OS™';")
    js = js.replace(
        "sub.textContent = isClinic ? 'Aasan OPD & Prescription Desk (1-Minute Nuskha)' : 'ZAYVORA Sovereign Health OS & R&D Cloud';",
        "sub.textContent = isClinic ? 'Unani OPD & Hospital Management' : 'ZAYVORA Sovereign Health OS & R&D Cloud';"
    )

    # 3. Restore the Omnipresent Clinician Diagnostic Desk (10 Tools Active) in today tab
    today_pattern = re.compile(
        r'\$\{\(state\.platformEdition === \'clinic\'\)\s*\?\s*`[\s\S]*?`\s*:\s*`([\s\S]*?)`\}',
        re.MULTILINE
    )
    m = today_pattern.search(js)
    if m:
        full_original_toolbar = m.group(1).strip()
        js = js[:m.start()] + full_original_toolbar + js[m.end():]
        print("[✓] zayvora-core.js: Restored Omnipresent Clinician Diagnostic Desk in Today tab")

    with open(path, "w", encoding="utf-8") as f:
        f.write(js)
    print("[✓] zayvora-core.js: Written successfully")

if __name__ == "__main__":
    revert_index_html()
    revert_core_js()
