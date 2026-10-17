import os
import re

def update_index_html():
    path = "index.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Top banner: Change from amber DEMONSTRATION to emerald PRODUCTION
    banner_old = """  <!-- ===================================================================== -->
  <!-- DEMONSTRATION & SYNTHETIC DATA ENVIRONMENT NOTICE BANNER -->
  <!-- ===================================================================== -->
  <div id="demo-environment-banner" class="w-full bg-amber-950/90 border-b border-amber-500/40 px-3 py-1.5 text-center text-[11px] font-mono font-bold text-amber-300 tracking-wider flex items-center justify-center gap-2 z-50">
    <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse shrink-0"></span>
    <span>DEMONSTRATION ENVIRONMENT &mdash; ALL PATIENT, CLINICAL, REGULATORY AND TRANSACTION DATA IS SYNTHETIC.</span>
  </div>"""

    banner_new = """  <!-- ===================================================================== -->
  <!-- PRODUCTION ENVIRONMENT STATUS BANNER -->
  <!-- ===================================================================== -->
  <div id="demo-environment-banner" class="w-full bg-emerald-950/90 border-b border-emerald-500/40 px-3 py-1 text-center text-[11px] font-mono font-bold text-emerald-300 tracking-wider flex items-center justify-center gap-2 z-50">
    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse shrink-0"></span>
    <span>ZAYVORA HEALTH OS &bull; LIVE CLINICAL PRODUCTION ENVIRONMENT &bull; SECURE HOSPITAL INSTANCE</span>
  </div>"""

    if banner_old in html:
        html = html.replace(banner_old, banner_new)
        print("[✓] index.html: Updated top banner to Production")
    else:
        print("[!] index.html: banner_old not found by exact string, checking regex")
        html = re.sub(
            r'<div id="demo-environment-banner"[^>]*>[\s\S]*?DEMONSTRATION ENVIRONMENT[\s\S]*?<\/div>',
            banner_new.strip(),
            html
        )

    # 2. Right header pill: Remove "DEMO SANDBOX"
    hub_old = """      <div class="hidden lg:flex items-center gap-2 pl-3 border-l border-slate-800 shrink-0">
        <span class="px-2 py-0.5 text-[9px] font-mono font-bold rounded bg-amber-500/10 text-amber-300 border border-amber-500/30">DEMO SANDBOX — NOT REAL PATIENT INFORMATION</span>
        <span class="px-2 py-0.5 text-[9px] font-mono font-bold rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">EVIDENCE V2</span>
      </div>"""

    hub_new = """      <div class="hidden lg:flex items-center gap-2 pl-3 border-l border-slate-800 shrink-0">
        <span class="px-2 py-0.5 text-[9px] font-mono font-bold rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">CLINICAL PRODUCTION LIVE</span>
        <span class="px-2 py-0.5 text-[9px] font-mono font-bold rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">EVIDENCE V2</span>
      </div>"""

    if hub_old in html:
        html = html.replace(hub_old, hub_new)
        print("[✓] index.html: Updated right header pill to Production")

    # 3. Footer badge: Remove "EVALUATION SANDBOX • DEMO ENVIRONMENT"
    footer_old = """        <div class="shrink-0 flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-[10px] font-mono">
          <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
          <span>EVALUATION SANDBOX &bull; DEMO ENVIRONMENT</span>
        </div>"""

    footer_new = """        <div class="shrink-0 flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-[10px] font-mono">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>ENTERPRISE PRODUCTION &bull; CLINICAL OPERATING SYSTEM</span>
        </div>"""

    if footer_old in html:
        html = html.replace(footer_old, footer_new)
        print("[✓] index.html: Updated footer badge to Production")

    # 4. Prescription slip demo badge
    slip_old = """            <strong class="text-slate-900 text-sm flex items-center gap-1.5" id="slip-patient-name">
              <span>Hamza Farooqi</span>
              <span class="px-1.5 py-0.2 rounded text-[8px] font-bold bg-amber-100 text-amber-800 border border-amber-300">DEMO SANDBOX</span>
            </strong>"""

    slip_new = """            <strong class="text-slate-900 text-sm flex items-center gap-1.5" id="slip-patient-name">
              <span>Hamza Farooqi</span>
              <span class="px-1.5 py-0.2 rounded text-[8px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">VERIFIED PATIENT</span>
            </strong>"""

    if slip_old in html:
        html = html.replace(slip_old, slip_new)
        print("[✓] index.html: Updated prescription slip patient badge")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("[✓] index.html updated successfully")

def update_core_js():
    path = "js/zayvora-core.js"
    with open(path, "r", encoding="utf-8") as f:
        js = f.read()

    # Clean patient demo profile
    p_old = "patient: { name: 'Hamza Farooqi [TEST]', title: 'Patient (MRN-2026-0814) • DEMO SANDBOX', email: 'demo.patient@sandbox.zayvora.internal' },"
    p_new = "patient: { name: 'Hamza Farooqi', title: 'Patient (MRN-2026-0814) • Verified Record', email: 'patient.hamza@zayvorahealth.com' },"

    if p_old in js:
        js = js.replace(p_old, p_new)
        print("[✓] zayvora-core.js: Updated patient profile from test to verified")

    with open(path, "w", encoding="utf-8") as f:
        f.write(js)
    print("[✓] zayvora-core.js updated successfully")

if __name__ == "__main__":
    update_index_html()
    update_core_js()
