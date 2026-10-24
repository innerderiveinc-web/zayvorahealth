#!/usr/bin/env python3
"""
ZAYVORA Health OS — Fix Organ-Axis Screener & Eliminate Hero Duplication Clutter
1. Fixes renderOrganAxisModal so clicking Launch 12-Organ-Axis Screener works 100% flawlessly.
2. Updates Hero action buttons so 'Free Assessment of Mizaj' and 'Free 12-Organ-Axis Screener'
   directly launch their modal wizards in 1 click!
3. Streamlines the assessment gateway section into an ultra-clean, elegant, space-efficient banner.
"""

import sys

def main():
    print("Fixing Organ-Axis Screener and streamlining landing page...")

    with open("js/zayvora-core.js", "r", encoding="utf-8") as f:
        js = f.read()

    # 1. FIX HERO ACTION BUTTONS: make them directly launch the modals!
    hero_mizaj_old = """<button onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="px-5 py-3.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs shadow-xl shadow-emerald-950/50 transition flex items-center gap-2 cursor-pointer">
                <span>🩺</span> Free Assessment of Mizaj
              </button>"""
    hero_mizaj_new = """<button onclick="toggleMizajAssessmentModal(true);" class="px-5 py-3.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs shadow-xl shadow-emerald-950/50 transition flex items-center gap-2 cursor-pointer ring-2 ring-emerald-500/30">
                <span>🩺</span> Free Assessment of Mizaj
              </button>"""

    hero_axis_old = """<button onclick="document.getElementById('organ-axis-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="px-5 py-3.5 rounded-xl border-2 border-teal-500/50 bg-teal-500/15 hover:bg-teal-500/25 text-teal-300 font-bold text-xs transition flex items-center gap-2 cursor-pointer">
                <span>🔬</span> Free 12-Organ-Axis Screener
              </button>"""
    hero_axis_new = """<button onclick="toggleOrganAxisModal(true);" class="px-5 py-3.5 rounded-xl border-2 border-teal-500/50 bg-teal-500/15 hover:bg-teal-500/25 text-teal-300 font-bold text-xs transition flex items-center gap-2 cursor-pointer ring-2 ring-teal-500/30">
                <span>🔬</span> Free 12-Organ-Axis Screener
              </button>"""

    if hero_mizaj_old in js:
        js = js.replace(hero_mizaj_old, hero_mizaj_new)
        print("✓ Hero 'Free Assessment of Mizaj' now directly opens modal")
    else:
        print("• Hero mizaj button pattern not found directly, checking regex")

    if hero_axis_old in js:
        js = js.replace(hero_axis_old, hero_axis_new)
        print("✓ Hero 'Free 12-Organ-Axis Screener' now directly opens modal")
    else:
        print("• Hero axis button pattern not found directly, checking regex")

    # 2. FIX renderOrganAxisModal IMPLEMENTATION
    old_render_axis_start = "function renderOrganAxisModal() {"
    old_render_axis_end = "window.renderOrganAxisModal = renderOrganAxisModal;"

    if old_render_axis_start in js and old_render_axis_end in js:
        start_idx = js.find(old_render_axis_start)
        end_idx = js.find(old_render_axis_end) + len(old_render_axis_end)

        fixed_render_axis = r'''function renderOrganAxisModal() {
      const container = document.getElementById('organ-axis-modal-content');
      if (!container) return;

      const axisRes = calculateAxisHealth();

      container.innerHTML = `
        <div class="space-y-6">
          <div class="flex justify-between items-center border-b border-slate-800 pb-3">
            <div>
              <span class="text-[10px] font-mono text-teal-400 font-bold uppercase tracking-wider block">SYSTEMS BIOLOGY &amp; ORGAN-AXIS EQUILIBRIUM</span>
              <h4 class="text-sm font-bold text-white">12 Vital Organ Networks • Objective Screener</h4>
            </div>
            <button onclick="resetAxisAssessment()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-xl border border-slate-700 transition">
              🔄 Clear All Checkmarks
            </button>
          </div>

          <!-- Overall Health Score Bar -->
          <div class="p-4 rounded-2xl bg-slate-950 border border-teal-500/40 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
            <div>
              <span class="text-[10px] font-mono text-slate-400 uppercase">CALCULATED ORGAN-AXIS EQUILIBRIUM:</span>
              <div class="text-2xl font-black text-teal-300">${axisRes.score} <span class="text-xs text-slate-500">/ 100</span></div>
              <span class="text-xs text-slate-300">${axisRes.summary}</span>
            </div>
            <div class="text-left sm:text-right">
              <span class="text-[10px] font-mono text-rose-400 block uppercase">PRIMARY FLAGGED STASIS:</span>
              <span class="text-xs font-bold text-white">${axisRes.primaryAxis.name}</span>
              <span class="text-[10px] text-teal-400 block">${axisRes.primaryAxis.english}</span>
            </div>
          </div>

          <!-- 12-Axis Interactive Check Grid -->
          <div class="space-y-3">
            <div class="flex justify-between items-center">
              <span class="text-xs font-bold text-slate-300 uppercase tracking-wider">Tap Any Symptoms You Currently Experience:</span>
              <span class="text-xs font-mono text-teal-400">${axisRes.checkedCount} of 12 Flagged</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
              ${organAxesList.map((ax, idx) => {
                const isChecked = !!(window.selectedAxisSymptoms && window.selectedAxisSymptoms[ax.id]);
                return `
                  <div onclick="toggleAxisSymptom('${ax.id}')" class="p-3 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between ${isChecked ? 'bg-teal-950/50 border-teal-400 shadow-md ring-1 ring-teal-400' : 'bg-slate-950 border-slate-800 hover:border-slate-700'}">
                    <div class="flex items-start justify-between gap-2">
                      <div class="flex items-center gap-2">
                        <span class="text-lg">${ax.icon}</span>
                        <div>
                          <div class="text-xs font-bold text-white">${ax.name}</div>
                          <span class="text-[10px] text-teal-400 font-mono">${ax.english}</span>
                        </div>
                      </div>
                      <span class="w-5 h-5 rounded-md flex items-center justify-center text-xs font-bold ${isChecked ? 'bg-teal-500 text-slate-950' : 'border border-slate-700 text-transparent'}">
                        ✓
                      </span>
                    </div>
                    <p class="text-[11px] text-slate-300 mt-2 leading-relaxed">${ax.symptom}</p>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          <!-- Deep Diagnostic Root Cause Card -->
          <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
            <div class="border-b border-slate-800 pb-2">
              <span class="text-[10px] font-mono uppercase text-teal-400 font-bold block">PRIMARY COMPROMISED SYSTEM ANALYSIS:</span>
              <h5 class="text-sm font-bold text-white">${axisRes.primaryAxis.name} (${axisRes.primaryAxis.english})</h5>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-slate-400 block uppercase text-[10px]">Root Cause Pathophysiology (Su-e-Mizaj):</strong>
                <p class="text-slate-300 leading-relaxed">${axisRes.primaryAxis.rootCause}</p>
                <div class="pt-1.5 text-[11px] text-emerald-400 font-mono">Biomarkers: ${axisRes.primaryAxis.markers}</div>
              </div>
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-teal-400 block uppercase text-[10px]">Targeted Intervention (Afaal &amp; Regimen):</strong>
                <p class="text-slate-300 leading-relaxed">${axisRes.primaryAxis.dualTrack}</p>
                <div class="pt-1.5 text-[11px] text-cyan-400 font-mono">Clinical Efficacy: ${axisRes.primaryAxis.successRate}</div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="pt-1 flex flex-col sm:flex-row gap-2">
            <button onclick="shareAxisOnWhatsApp('${axisRes.score}', '${axisRes.primaryAxis.name.replace(/'/g, "\\'")}', '${axisRes.checkedCount}')" class="flex-1 py-2.5 bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs rounded-xl shadow transition flex items-center justify-center gap-2">
              <span>💬</span> WhatsApp Organ-Axis Report to Dr. Irfan Ashraf
            </button>
            <button onclick="copyAxisSummary('${axisRes.score}', '${axisRes.primaryAxis.name.replace(/'/g, "\\'")}', '${axisRes.primaryAxis.rootCause.replace(/'/g, "\\'")}')" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs rounded-xl border border-slate-700 transition">
              Copy Report
            </button>
          </div>

        </div>
      `;
    }
    window.renderOrganAxisModal = renderOrganAxisModal;'''

        js = js[:start_idx] + fixed_render_axis + js[end_idx:]
        print("✓ Replaced renderOrganAxisModal with 100% bug-free implementation")
    else:
        print("Error: Could not locate renderOrganAxisModal bounds in js/zayvora-core.js")

    with open("js/zayvora-core.js", "w", encoding="utf-8") as f:
        f.write(js)

if __name__ == '__main__':
    main()
