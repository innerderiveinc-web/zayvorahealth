#!/usr/bin/env python3
"""
ZAYVORA Health OS — Omnipresent OS Diagnostic Integration
Embeds the 10 Global Diagnostic & Functional Medicine Engines into:
1. Top Global Navigation Header (persistent launcher across all roles)
2. #global-tools-modal (universal 10-tool command center)
3. Doctor Clinical Cockpit (renderDoctorApp)
4. Patient Health 360 Dashboard (renderPatientApp)
"""

import sys

def main():
    print("Making all diagnostic and functional medicine upgrades visible across the OS...")

    # 1. UPDATE INDEX.HTML
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Add header launcher button right before #platform-currency-select
    header_btn = '''        <!-- Global Diagnostic & Functional Medicine Hub Launcher (Omnipresent in OS) -->
        <button onclick="toggleGlobalToolsModal(true)" class="bg-slate-900 border border-emerald-500/40 hover:border-emerald-400 text-emerald-300 hover:text-white font-bold text-[11px] rounded-xl px-2.5 py-1.5 focus:outline-none cursor-pointer transition shadow-sm flex items-center gap-1.5" title="Access All 10 Global Diagnostic & Functional Medicine Engines">
          <span>🧠</span>
          <span class="hidden sm:inline">Diagnostic Tools</span>
          <span class="px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-300 font-mono text-[9px]">10</span>
        </button>

'''

    if 'toggleGlobalToolsModal(true)' not in html:
        target_currency = '<select id="platform-currency-select"'
        html = html.replace(target_currency, header_btn + '        ' + target_currency)
        print("✓ Injected Diagnostic Tools launcher button into Top Header in index.html")

    # Add #global-tools-modal right before </body>
    global_tools_modal = '''
  <!-- ===================================================================== -->
  <!-- UNIVERSAL OS COMMAND CENTER: ALL 10 CLINICAL & FUNCTIONAL ENGINES    -->
  <!-- ===================================================================== -->
  <div id="global-tools-modal" class="fixed inset-0 z-50 hidden bg-black/90 backdrop-blur-md flex items-center justify-center p-3 sm:p-5">
    <div class="bg-slate-900 border border-emerald-500/50 rounded-3xl max-w-4xl w-full max-h-[94vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
      <div class="px-6 py-4 border-b border-slate-800 bg-slate-950 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 via-teal-600 to-cyan-600 text-white flex items-center justify-center font-bold text-lg shadow-md">🧠</span>
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <span>ZAYVORA Diagnostic &amp; Functional Medicine Suite™</span>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">10 Clinical Engines</span>
            </h3>
            <p class="text-xs text-slate-400">Mayo Clinic • Cleveland Clinic • IFM Functional Medicine Benchmarks</p>
          </div>
        </div>
        <button onclick="toggleGlobalToolsModal(false)" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition">✕</button>
      </div>
      <div class="p-6 overflow-y-auto flex-1 space-y-5 text-xs">
        
        <div class="p-3.5 rounded-2xl bg-emerald-950/30 border border-emerald-500/30 flex justify-between items-center">
          <div>
            <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-wider">OMNIPRESENT CLINICAL INTELLIGENCE</span>
            <p class="text-xs text-slate-200">Access any diagnostic engine directly from anywhere in ZAYVORA Health OS.</p>
          </div>
          <span class="text-xs font-mono text-emerald-400 font-bold">100% OPERATIONAL</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          
          <!-- 1. Body Navigator -->
          <div onclick="toggleGlobalToolsModal(false); toggleBodyNavigatorModal(true);" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 hover:border-cyan-500 hover:bg-cyan-950/20 transition cursor-pointer space-y-1.5 group">
            <div class="flex justify-between items-center">
              <span class="text-2xl group-hover:scale-110 transition">🗺️</span>
              <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-bold">MAYO CLINIC</span>
            </div>
            <h4 class="text-xs font-bold text-white group-hover:text-cyan-300 transition">Body Symptom Navigator</h4>
            <p class="text-[11px] text-slate-400">Interactive organ-by-organ visual triage with classical Unani roots and home remedies.</p>
          </div>

          <!-- 2. Lab Correlator -->
          <div onclick="toggleGlobalToolsModal(false); toggleLabCorrelatorModal(true);" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 hover:border-teal-500 hover:bg-teal-950/20 transition cursor-pointer space-y-1.5 group">
            <div class="flex justify-between items-center">
              <span class="text-2xl group-hover:scale-110 transition">🧪</span>
              <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-teal-500/20 text-teal-300 font-bold">CLEVELAND CLINIC</span>
            </div>
            <h4 class="text-xs font-bold text-white group-hover:text-teal-300 transition">Lab Report Correlator</h4>
            <p class="text-[11px] text-slate-400">Correlate allopathic blood panels (HbA1c, Uric Acid, TSH, SGPT) with Greco-Arab root causes.</p>
          </div>

          <!-- 3. Food Matrix -->
          <div onclick="toggleGlobalToolsModal(false); toggleFoodCompatibilityModal(true);" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 hover:border-amber-500 hover:bg-amber-950/20 transition cursor-pointer space-y-1.5 group">
            <div class="flex justify-between items-center">
              <span class="text-2xl group-hover:scale-110 transition">🥗</span>
              <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold">ZOE / THORNE</span>
            </div>
            <h4 class="text-xs font-bold text-white group-hover:text-amber-300 transition">Kitchen Food Matrix</h4>
            <p class="text-[11px] text-slate-400">Mizaj-aligned food scanner, dietary incompatibilities, and traditional correctives (Musleh).</p>
          </div>

          <!-- 4. Hazm-e-Arba'a -->
          <div onclick="toggleGlobalToolsModal(false); toggleHazmArbaModal(true);" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 hover:border-emerald-500 hover:bg-emerald-950/20 transition cursor-pointer space-y-1.5 group">
            <div class="flex justify-between items-center">
              <span class="text-2xl group-hover:scale-110 transition">🔄</span>
              <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">IFM MATRIX</span>
            </div>
            <h4 class="text-xs font-bold text-white group-hover:text-emerald-300 transition">Hazm-e-Arba'a Digestion</h4>
            <p class="text-[11px] text-slate-400">4-Stage digestion analyzer: Gastric, Hepatic, Vascular, and Cellular/Mitochondrial stages.</p>
          </div>

          <!-- 5. ATM Timeline -->
          <div onclick="toggleGlobalToolsModal(false); toggleAtmTimelineModal(true);" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 hover:border-indigo-500 hover:bg-indigo-950/20 transition cursor-pointer space-y-1.5 group">
            <div class="flex justify-between items-center">
              <span class="text-2xl group-hover:scale-110 transition">⏳</span>
              <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-bold">SANIHA-E-MARAZ</span>
            </div>
            <h4 class="text-xs font-bold text-white group-hover:text-indigo-300 transition">Functional ATM Timeline</h4>
            <p class="text-[11px] text-slate-400">Map your Antecedents (genetics), Triggers (infections/shocks), and ongoing Mediators.</p>
          </div>

          <!-- 6. Humoral Bio-Clock -->
          <div onclick="toggleGlobalToolsModal(false); toggleHumoralClockModal(true);" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 hover:border-yellow-500 hover:bg-yellow-950/20 transition cursor-pointer space-y-1.5 group">
            <div class="flex justify-between items-center">
              <span class="text-2xl group-hover:scale-110 transition">⏱️</span>
              <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-yellow-500/20 text-yellow-300 font-bold">CHRONO-BIOLOGY</span>
            </div>
            <h4 class="text-xs font-bold text-white group-hover:text-yellow-300 transition">24h Humoral Bio-Clock</h4>
            <p class="text-[11px] text-slate-400">Real-time biological clock aligning nutrition and botanical posology with diurnal humoral surges.</p>
          </div>

          <!-- 7. Gut-Brain Vagus -->
          <div onclick="toggleGlobalToolsModal(false); toggleGutBrainModal(true);" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 hover:border-rose-500 hover:bg-rose-950/20 transition cursor-pointer space-y-1.5 group">
            <div class="flex justify-between items-center">
              <span class="text-2xl group-hover:scale-110 transition">🧠</span>
              <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold">MARAQ-E-MEDA</span>
            </div>
            <h4 class="text-xs font-bold text-white group-hover:text-rose-300 transition">Gut-Brain Vagus Screener</h4>
            <p class="text-[11px] text-slate-400">Detect whether brain fog and anxiety are driven by gastrointestinal fermentation.</p>
          </div>

          <!-- 8. Tanqiya Detox -->
          <div onclick="toggleGlobalToolsModal(false); toggleTanqiyaReadinessModal(true);" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 hover:border-teal-500 hover:bg-teal-950/20 transition cursor-pointer space-y-1.5 group">
            <div class="flex justify-between items-center">
              <span class="text-2xl group-hover:scale-110 transition">🌿</span>
              <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-teal-500/20 text-teal-300 font-bold">MUNZIJ &amp; MUSHIL</span>
            </div>
            <h4 class="text-xs font-bold text-white group-hover:text-teal-300 transition">Tanqiya Readiness Index</h4>
            <p class="text-[11px] text-slate-400">Determine whether your body requires Phase 1 Detoxification before taking restorative tonics.</p>
          </div>

          <!-- 9. 14-Day Reset Challenge -->
          <div onclick="toggleGlobalToolsModal(false); toggleAsbabChallengeModal(true);" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 hover:border-purple-500 hover:bg-purple-950/20 transition cursor-pointer space-y-1.5 group">
            <div class="flex justify-between items-center">
              <span class="text-2xl group-hover:scale-110 transition">🏆</span>
              <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 font-bold">DIGITAL Rx</span>
            </div>
            <h4 class="text-xs font-bold text-white group-hover:text-purple-300 transition">14-Day Asbab-e-Sitta Reset</h4>
            <p class="text-[11px] text-slate-400">Daily habit tracking across the six essential pillars of health to restore natural homeostasis.</p>
          </div>

          <!-- 10. Clinical Outcomes & PROMs -->
          <div onclick="toggleGlobalToolsModal(false); toggleClinicalOutcomesModal(true);" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 hover:border-blue-500 hover:bg-blue-950/20 transition cursor-pointer space-y-1.5 group">
            <div class="flex justify-between items-center">
              <span class="text-2xl group-hover:scale-110 transition">📈</span>
              <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 font-bold">EVIDENCE RWE</span>
            </div>
            <h4 class="text-xs font-bold text-white group-hover:text-blue-300 transition">PROMs Clinical Outcomes</h4>
            <p class="text-[11px] text-slate-400">Real-world registry of 1,240+ multi-center subjects with objective biochemical verification.</p>
          </div>

        </div>
      </div>
    </div>
  </div>
'''

    if 'id="global-tools-modal"' not in html:
        html = html.replace('</body>', global_tools_modal + '\n</body>')
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("✓ Injected #global-tools-modal into index.html")

    # 2. UPDATE JS/ZAYVORA-CORE.JS
    with open("js/zayvora-core.js", "r", encoding="utf-8") as f:
        js = f.read()

    # Add toggleGlobalToolsModal function
    js_modal_fn = '''
    function toggleGlobalToolsModal(show = true) {
      const modal = document.getElementById('global-tools-modal');
      if (!modal) return;
      if (show) {
        modal.classList.remove('hidden');
      } else {
        modal.classList.add('hidden');
      }
    }
    window.toggleGlobalToolsModal = toggleGlobalToolsModal;
'''
    if 'window.toggleGlobalToolsModal' not in js:
        js += '\n' + js_modal_fn
        print("✓ Appended toggleGlobalToolsModal to js/zayvora-core.js")

    # Inject Clinician Diagnostic Suite Bar into renderDoctorApp
    doctor_target = '<!-- Welcome Header -->'
    doctor_bar = '''<!-- CLINICIAN DIAGNOSTIC & FUNCTIONAL TIBB SUITE (OMNIPRESENT TOOLBAR) -->
            <div class="p-4 rounded-2xl bg-gradient-to-r from-slate-900 to-slate-950 border border-emerald-500/40 space-y-2.5 shadow-md">
              <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs">🧠</span>
                  <h4 class="text-xs font-bold text-white uppercase tracking-wider">Clinician Diagnostic Desk • Functional &amp; Mayo Engines</h4>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-[10px] font-mono text-emerald-400">10 Tools Active</span>
                  <button onclick="toggleGlobalToolsModal(true)" class="text-[10px] text-slate-400 hover:text-white font-mono underline">View All →</button>
                </div>
              </div>
              <div class="grid grid-cols-2 sm:grid-cols-5 gap-2 text-xs">
                <button onclick="toggleBodyNavigatorModal(true)" class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-cyan-500 hover:bg-cyan-950/20 text-slate-200 hover:text-white flex items-center gap-2 transition cursor-pointer text-left">
                  <span>🗺️</span> <span class="font-medium text-[11px]">Body Navigator</span>
                </button>
                <button onclick="toggleLabCorrelatorModal(true)" class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-teal-500 hover:bg-teal-950/20 text-slate-200 hover:text-white flex items-center gap-2 transition cursor-pointer text-left">
                  <span>🧪</span> <span class="font-medium text-[11px]">Lab Correlator</span>
                </button>
                <button onclick="toggleHazmArbaModal(true)" class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-emerald-500 hover:bg-emerald-950/20 text-slate-200 hover:text-white flex items-center gap-2 transition cursor-pointer text-left">
                  <span>🔄</span> <span class="font-medium text-[11px]">Hazm-e-Arba'a</span>
                </button>
                <button onclick="toggleAtmTimelineModal(true)" class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-indigo-500 hover:bg-indigo-950/20 text-slate-200 hover:text-white flex items-center gap-2 transition cursor-pointer text-left">
                  <span>⏳</span> <span class="font-medium text-[11px]">ATM Timeline</span>
                </button>
                <button onclick="toggleHumoralClockModal(true)" class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-yellow-500 hover:bg-yellow-950/20 text-slate-200 hover:text-white flex items-center gap-2 transition cursor-pointer text-left">
                  <span>⏱️</span> <span class="font-medium text-[11px]">Humoral Clock</span>
                </button>
                <button onclick="toggleGutBrainModal(true)" class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-rose-500 hover:bg-rose-950/20 text-slate-200 hover:text-white flex items-center gap-2 transition cursor-pointer text-left">
                  <span>🧠</span> <span class="font-medium text-[11px]">Gut-Brain Vagus</span>
                </button>
                <button onclick="toggleTanqiyaReadinessModal(true)" class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-teal-500 hover:bg-teal-950/20 text-slate-200 hover:text-white flex items-center gap-2 transition cursor-pointer text-left">
                  <span>🌿</span> <span class="font-medium text-[11px]">Tanqiya Detox</span>
                </button>
                <button onclick="toggleFoodCompatibilityModal(true)" class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-amber-500 hover:bg-amber-950/20 text-slate-200 hover:text-white flex items-center gap-2 transition cursor-pointer text-left">
                  <span>🥗</span> <span class="font-medium text-[11px]">Kitchen Matrix</span>
                </button>
                <button onclick="toggleAsbabChallengeModal(true)" class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-purple-500 hover:bg-purple-950/20 text-slate-200 hover:text-white flex items-center gap-2 transition cursor-pointer text-left">
                  <span>🏆</span> <span class="font-medium text-[11px]">14-Day Reset</span>
                </button>
                <button onclick="toggleClinicalOutcomesModal(true)" class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-blue-500 hover:bg-blue-950/20 text-slate-200 hover:text-white flex items-center gap-2 transition cursor-pointer text-left">
                  <span>📈</span> <span class="font-medium text-[11px]">PROMs Registry</span>
                </button>
              </div>
            </div>

            '''

    if 'CLINICIAN DIAGNOSTIC & FUNCTIONAL TIBB SUITE' not in js:
        js = js.replace(doctor_target, doctor_bar + doctor_target, 1)
        print("✓ Injected Clinician Diagnostic Desk Toolbar into renderDoctorApp")

    # Inject Patient Diagnostic & Self-Care Tools into renderPatientApp
    patient_target = '<!-- PRIMARY ACTION CARD: "WHAT DO I DO TODAY?" -->'
    patient_bar = '''<!-- PATIENT HEALTH 360 INTEGRATIVE FUNCTIONAL ENGINES -->
            <div class="p-5 rounded-2xl bg-gradient-to-r from-slate-900 to-slate-950 border border-emerald-500/30 space-y-3 shadow-md">
              <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs">🌟</span>
                  <h4 class="text-xs font-bold text-white uppercase tracking-wider">Patient Health Discovery • Functional Self-Care Tools</h4>
                </div>
                <button onclick="toggleGlobalToolsModal(true)" class="text-[10px] text-emerald-400 hover:underline font-mono">View All 10 Tools →</button>
              </div>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
                <button onclick="toggleHumoralClockModal(true)" class="p-3 rounded-xl bg-slate-900/90 border border-amber-500/30 hover:border-amber-400 hover:bg-amber-950/20 text-left transition cursor-pointer">
                  <div class="text-lg">⏱️</div>
                  <div class="font-bold text-white text-[11px] mt-1">Humoral Bio-Clock</div>
                  <div class="text-[10px] text-slate-400">Right food &amp; medicine time</div>
                </button>
                <button onclick="toggleFoodCompatibilityModal(true)" class="p-3 rounded-xl bg-slate-900/90 border border-amber-500/30 hover:border-amber-400 hover:bg-amber-950/20 text-left transition cursor-pointer">
                  <div class="text-lg">🥗</div>
                  <div class="font-bold text-white text-[11px] mt-1">Kitchen Food Matrix</div>
                  <div class="text-[10px] text-slate-400">ZOE Precision nutrition</div>
                </button>
                <button onclick="toggleGutBrainModal(true)" class="p-3 rounded-xl bg-slate-900/90 border border-rose-500/30 hover:border-rose-400 hover:bg-rose-950/20 text-left transition cursor-pointer">
                  <div class="text-lg">🧠</div>
                  <div class="font-bold text-white text-[11px] mt-1">Gut-Brain Screener</div>
                  <div class="text-[10px] text-slate-400">Check vagal fermentation</div>
                </button>
                <button onclick="toggleHazmArbaModal(true)" class="p-3 rounded-xl bg-slate-900/90 border border-emerald-500/30 hover:border-emerald-400 hover:bg-emerald-950/20 text-left transition cursor-pointer">
                  <div class="text-lg">🔄</div>
                  <div class="font-bold text-white text-[11px] mt-1">4-Stage Digestion</div>
                  <div class="text-[10px] text-slate-400">Locate metabolic stasis</div>
                </button>
              </div>
            </div>

            '''

    if 'PATIENT HEALTH 360 INTEGRATIVE FUNCTIONAL ENGINES' not in js:
        js = js.replace(patient_target, patient_bar + patient_target, 1)
        print("✓ Injected Patient Health Discovery Tools into renderPatientApp")

    with open("js/zayvora-core.js", "w", encoding="utf-8") as f:
        f.write(js)

if __name__ == '__main__':
    main()
