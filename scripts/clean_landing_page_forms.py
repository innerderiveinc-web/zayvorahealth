#!/usr/bin/env python3
"""
ZAYVORA Health OS — Landing Page De-Cluttering & Questionnaire Modalization
Directly cuts out the 350+ lines of raw form questions on the landing page
and replaces them with two sleek, high-converting gateway cards.
"""

import sys

def main():
    print("De-cluttering landing page: modalizing Mizaj and Organ-Axis assessments...")

    with open("js/zayvora-core.js", "r", encoding="utf-8") as f:
        js = f.read()

    start_needle = "<!-- 5. FREE COMPREHENSIVE MIZAJ ASSESSMENT (AL-AJNAS AL-ASHRAH) -->"
    end_needle = '<div id="opd-booking-card"'

    if start_needle not in js:
        print(f"Error: start needle not found in js/zayvora-core.js")
        sys.exit(1)
    if end_needle not in js:
        print(f"Error: end needle not found in js/zayvora-core.js")
        sys.exit(1)

    start_idx = js.find(start_needle)
    end_idx = js.find(end_needle)

    print(f"Found block to replace from index {start_idx} to {end_idx} ({end_idx - start_idx} chars)")

    sleek_replacement = '''<!-- ===================================================================== -->
          <!-- 5. FREE CLINICAL SELF-ASSESSMENT SUITE (STREAMLINED MODAL LAUNCHERS)  -->
          <!-- ===================================================================== -->
          <div class="space-y-6">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-2 border-b border-slate-800 pb-3">
              <div>
                <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-wider block">CLINICAL SELF-ASSESSMENT GATEWAYS</span>
                <h3 class="text-xl sm:text-2xl font-extrabold text-white">Free Constitutional &amp; Organ-Axis Screeners</h3>
                <p class="text-xs text-slate-300 mt-0.5">Instant, non-invasive bio-humoral diagnostics based on classical Greco-Arab doctrines.</p>
              </div>
              <span class="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-bold">100% FREE • NO LOGIN REQUIRED</span>
            </div>

            <!-- Two High-Impact Diagnostic Cards Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Card 1: Mizaj Assessment -->
              <div id="mizaj-assessment-section" class="p-6 rounded-3xl bg-gradient-to-br from-[#0F172A] to-[#1E293B] border-2 border-emerald-500/40 shadow-xl space-y-4 flex flex-col justify-between">
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <span class="w-10 h-10 rounded-2xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-xl font-bold">🩺</span>
                    <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-bold">AL-AJNAS AL-ASHRAH</span>
                  </div>
                  <div>
                    <h4 class="text-lg font-bold text-white">Free Assessment of Mizaj (Temperament)</h4>
                    <p class="text-xs text-slate-300 mt-1 leading-relaxed">
                      Discover your constitutional bio-humoral archetype (Damawi, Safrawi, Balghami, Sawdawi) and receive personalized dietary directives (Ilaj bil-Ghiza).
                    </p>
                  </div>
                </div>
                <div class="pt-2">
                  <button onclick="toggleMizajAssessmentModal(true)" class="w-full py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition flex items-center justify-center gap-2 cursor-pointer">
                    <span>Take 60-Second Mizaj Audit</span> <span>&rarr;</span>
                  </button>
                </div>
              </div>

              <!-- Card 2: 12-Organ-Axis Screener -->
              <div id="organ-axis-assessment-section" class="p-6 rounded-3xl bg-gradient-to-br from-[#0F172A] to-[#1E293B] border-2 border-teal-500/40 shadow-xl space-y-4 flex flex-col justify-between">
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <span class="w-10 h-10 rounded-2xl bg-teal-500/20 text-teal-400 flex items-center justify-center text-xl font-bold">🔬</span>
                    <span class="px-2.5 py-0.5 rounded-full bg-teal-500/20 text-teal-300 font-mono text-[10px] font-bold">SYSTEMS BIOLOGY</span>
                  </div>
                  <div>
                    <h4 class="text-lg font-bold text-white">Free 12-Organ-Axis Clinical Screener</h4>
                    <p class="text-xs text-slate-300 mt-1 leading-relaxed">
                      Screen for humoral stasis across 12 organ networks (Brain-Gut, Cardio-Vascular, Hepato-Biliary, Renal-Detox) and calculate your systemic balance score.
                    </p>
                  </div>
                </div>
                <div class="pt-2">
                  <button onclick="toggleOrganAxisModal(true)" class="w-full py-3 bg-gradient-to-r from-teal-600 to-cyan-600 hover:from-teal-500 text-white font-bold text-xs rounded-xl shadow-lg transition flex items-center justify-center gap-2 cursor-pointer">
                    <span>Launch 12-Organ-Axis Screener</span> <span>&rarr;</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          '''

    js = js[:start_idx] + sleek_replacement + js[end_idx:]

    with open("js/zayvora-core.js", "w", encoding="utf-8") as f:
        f.write(js)

    print("✓ Successfully replaced inline forms with sleek modal gateways in js/zayvora-core.js")

if __name__ == '__main__':
    main()
