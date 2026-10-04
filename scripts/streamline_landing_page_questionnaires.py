#!/usr/bin/env python3
"""
ZAYVORA Health OS — Landing Page Streamlining & Questionnaire Modalization
1. Converts Free Mizaj Assessment into a dedicated, focused modal (#mizaj-assessment-modal)
2. Converts Free 12-Organ-Axis Screener into a dedicated, focused modal (#organ-axis-modal)
3. Replaces bulky 350+ lines of raw form questions on the landing page with ultra-sleek,
   high-converting interactive cards with 1-click modal triggers.
4. Removes redundant Afaal Treatment Cascade academic diagram from home page.
5. Keeps all DOM IDs (#mizaj-assessment-section, #organ-axis-assessment-section) intact so
   zero tests or links break!
"""

import sys
import re

def main():
    print("Refactoring Mizaj & Organ-Axis Assessments into High-Performance Modals...")

    # 1. UPDATE index.html: Add the 2 new modals
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    new_modals = '''
  <!-- ===================================================================== -->
  <!-- 11. DEDICATED MIZAJ QUESTIONNAIRE MODAL (AL-AJNAS AL-ASHRAH)           -->
  <!-- ===================================================================== -->
  <div id="mizaj-assessment-modal" class="fixed inset-0 z-50 hidden bg-black/90 backdrop-blur-md flex items-center justify-center p-3 sm:p-5">
    <div class="bg-slate-900 border border-emerald-500/50 rounded-3xl max-w-4xl w-full max-h-[94vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
      <div class="px-6 py-4 border-b border-slate-800 bg-slate-950 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white flex items-center justify-center font-bold text-lg shadow-md">🩺</span>
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <span>Constitutional Mizaj Assessment™ (Al-Ajnas al-Ashrah)</span>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Free Diagnostic</span>
            </h3>
            <p class="text-xs text-slate-400">Select physical, digestive, and mentation parameters to compute your exact humoral balance percentage</p>
          </div>
        </div>
        <button onclick="toggleMizajAssessmentModal(false)" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition">✕</button>
      </div>
      <div id="mizaj-modal-content" class="p-6 overflow-y-auto flex-1 space-y-5 text-xs">
        <!-- Rendered dynamically by renderMizajAssessmentModal() -->
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- 12. DEDICATED 12-ORGAN-AXIS SCREENER MODAL (SYSTEMS BIOLOGY)          -->
  <!-- ===================================================================== -->
  <div id="organ-axis-modal" class="fixed inset-0 z-50 hidden bg-black/90 backdrop-blur-md flex items-center justify-center p-3 sm:p-5">
    <div class="bg-slate-900 border border-teal-500/50 rounded-3xl max-w-4xl w-full max-h-[94vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
      <div class="px-6 py-4 border-b border-slate-800 bg-slate-950 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-600 to-cyan-500 text-white flex items-center justify-center font-bold text-lg shadow-md">🔬</span>
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <span>12-Organ-Axis Systems Biology Screener™</span>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-teal-500/20 text-teal-300 border border-teal-500/30">Free Screener</span>
            </h3>
            <p class="text-xs text-slate-400">Screen for humoral stasis across 12 organ-axis systems and calculate your health equilibrium score</p>
          </div>
        </div>
        <button onclick="toggleOrganAxisModal(false)" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition">✕</button>
      </div>
      <div id="organ-axis-modal-content" class="p-6 overflow-y-auto flex-1 space-y-5 text-xs">
        <!-- Rendered dynamically by renderOrganAxisModal() -->
      </div>
    </div>
  </div>
'''

    if 'id="mizaj-assessment-modal"' not in html:
        html = html.replace('</body>', new_modals + '\n</body>')
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("✓ Injected #mizaj-assessment-modal and #organ-axis-modal into index.html")

    # 2. UPDATE js/zayvora-core.js
    with open("js/zayvora-core.js", "r", encoding="utf-8") as f:
        js = f.read()

    # Define toggle functions and modal renderers
    modal_renderers_js = r'''
    // ── DEDICATED MIZAJ & ORGAN-AXIS MODAL CONTROLLERS ───────────────────────
    function toggleMizajAssessmentModal(show = true) {
      const modal = document.getElementById('mizaj-assessment-modal');
      if (!modal) return;
      if (show) {
        renderMizajAssessmentModal();
        modal.classList.remove('hidden');
      } else {
        modal.classList.add('hidden');
      }
    }
    window.toggleMizajAssessmentModal = toggleMizajAssessmentModal;

    function renderMizajAssessmentModal() {
      const container = document.getElementById('mizaj-modal-content');
      if (!container) return;
      if (typeof window.previewMizajAnswers === 'undefined') {
        window.previewMizajAnswers = { temp: 'cold', moisture: 'moist', physique: 'broad', digestion: 'sluggish', sleep: 'deep', disposition: 'calm' };
      }
      const ans = window.previewMizajAnswers;
      const mizajRes = calculateDetailedMizaj();

      container.innerHTML = `
        <div class="space-y-6">
          <div class="flex justify-between items-center border-b border-slate-800 pb-3">
            <div>
              <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-wider block">AL-AJNAS AL-ASHRAH CANONICAL MATRIX</span>
              <h4 class="text-sm font-bold text-white">6-Point Constitutional Temperament Questionnaire</h4>
            </div>
            <button onclick="resetMizajAssessment()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-xl border border-slate-700 transition">
              🔄 Reset to Default
            </button>
          </div>

          <!-- 6 Diagnostic Questions Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
            <!-- Q1: Thermal Profile -->
            <div class="p-3.5 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-[11px] font-bold text-teal-400 uppercase">1. Thermal Sensitivity</span>
                <span class="text-[10px] text-slate-400 font-mono">Malmas</span>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="setPreviewMizaj('temp', 'hot')" class="py-2 px-2.5 rounded-xl text-xs font-semibold transition ${ans.temp === 'hot' ? 'bg-gradient-to-r from-red-600 to-amber-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🔥 Warm / Hot
                </button>
                <button onclick="setPreviewMizaj('temp', 'cold')" class="py-2 px-2.5 rounded-xl text-xs font-semibold transition ${ans.temp === 'cold' ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  ❄️ Cold Sensitive
                </button>
              </div>
            </div>

            <!-- Q2: Moisture & Skin Texture -->
            <div class="p-3.5 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-[11px] font-bold text-teal-400 uppercase">2. Moisture &amp; Skin</span>
                <span class="text-[10px] text-slate-400 font-mono">Jild</span>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="setPreviewMizaj('moisture', 'moist')" class="py-2 px-2.5 rounded-xl text-xs font-semibold transition ${ans.moisture === 'moist' ? 'bg-teal-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  💧 Soft / Moist
                </button>
                <button onclick="setPreviewMizaj('moisture', 'dry')" class="py-2 px-2.5 rounded-xl text-xs font-semibold transition ${ans.moisture === 'dry' ? 'bg-teal-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🌵 Dry / Rough
                </button>
              </div>
            </div>

            <!-- Q3: Skeletal Frame & Musculature -->
            <div class="p-3.5 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-[11px] font-bold text-teal-400 uppercase">3. Body Build</span>
                <span class="text-[10px] text-slate-400 font-mono">Binyah</span>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="setPreviewMizaj('physique', 'broad')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.physique === 'broad' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  💪 Broad
                </button>
                <button onclick="setPreviewMizaj('physique', 'athletic')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.physique === 'athletic' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  ⚡ Athletic
                </button>
                <button onclick="setPreviewMizaj('physique', 'soft')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.physique === 'soft' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🫧 Soft
                </button>
                <button onclick="setPreviewMizaj('physique', 'slender')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.physique === 'slender' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🦴 Slender
                </button>
              </div>
            </div>

            <!-- Q4: Appetite & Digestion -->
            <div class="p-3.5 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-[11px] font-bold text-teal-400 uppercase">4. Digestion &amp; Thirst</span>
                <span class="text-[10px] text-slate-400 font-mono">Meda</span>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="setPreviewMizaj('digestion', 'sharp')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.digestion === 'sharp' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🔥 Sharp / High Thirst
                </button>
                <button onclick="setPreviewMizaj('digestion', 'sluggish')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.digestion === 'sluggish' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🐢 Sluggish / Low Thirst
                </button>
                <button onclick="setPreviewMizaj('digestion', 'regular')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.digestion === 'regular' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  ⚖️ Strong / Regular
                </button>
                <button onclick="setPreviewMizaj('digestion', 'variable')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.digestion === 'variable' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🌪️ Irregular / Gas
                </button>
              </div>
            </div>

            <!-- Q5: Sleep Architecture -->
            <div class="p-3.5 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-[11px] font-bold text-teal-400 uppercase">5. Sleep Architecture</span>
                <span class="text-[10px] text-slate-400 font-mono">Naum</span>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="setPreviewMizaj('sleep', 'deep')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.sleep === 'deep' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  💤 Heavy / Excessive
                </button>
                <button onclick="setPreviewMizaj('sleep', 'light')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.sleep === 'light' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  ⚡ Light / Short
                </button>
                <button onclick="setPreviewMizaj('sleep', 'moderate')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.sleep === 'moderate' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🌙 Balanced (7h)
                </button>
                <button onclick="setPreviewMizaj('sleep', 'disturbed')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.sleep === 'disturbed' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🦉 Insomnia / Active Mind
                </button>
              </div>
            </div>

            <!-- Q6: Emotional Temperament -->
            <div class="p-3.5 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-[11px] font-bold text-teal-400 uppercase">6. Mind &amp; Emotion</span>
                <span class="text-[10px] text-slate-400 font-mono">Nafs</span>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="setPreviewMizaj('disposition', 'calm')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.disposition === 'calm' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🌊 Patient / Easygoing
                </button>
                <button onclick="setPreviewMizaj('disposition', 'intense')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.disposition === 'intense' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  ⚡ Quick-tempered / Driven
                </button>
                <button onclick="setPreviewMizaj('disposition', 'bold')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.disposition === 'bold' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  ☀️ Cheerful / Social
                </button>
                <button onclick="setPreviewMizaj('disposition', 'analytical')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.disposition === 'analytical' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🧐 Reflective / Overthinking
                </button>
              </div>
            </div>
          </div>

          <!-- Real-Time Diagnostic Result Card -->
          <div class="p-5 rounded-2xl bg-slate-950 border border-emerald-500/40 space-y-4">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
              <div>
                <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase">CALCULATED BIO-HUMORAL ARCHETYPE:</span>
                <h4 class="text-base font-extrabold text-white">${mizajRes.title}</h4>
              </div>
              <span class="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-xs font-bold border border-emerald-500/30">
                Dominant: ${mizajRes.primary}
              </span>
            </div>

            <!-- Percentage Bars -->
            <div class="space-y-2">
              <div class="flex justify-between text-[11px] text-slate-300">
                <span>Damawi (Sanguine): <strong>${mizajRes.percentages.damawi}%</strong></span>
                <span>Safrawi (Bilious): <strong>${mizajRes.percentages.safrawi}%</strong></span>
                <span>Balghami (Phlegmatic): <strong>${mizajRes.percentages.balghami}%</strong></span>
                <span>Sawdawi (Melancholic): <strong>${mizajRes.percentages.sawdawi}%</strong></span>
              </div>
              <div class="w-full h-3 rounded-full bg-slate-900 flex overflow-hidden border border-slate-800">
                <div style="width: ${mizajRes.percentages.damawi}%; background-color: #ef4444;" title="Damawi: ${mizajRes.percentages.damawi}%"></div>
                <div style="width: ${mizajRes.percentages.safrawi}%; background-color: #f59e0b;" title="Safrawi: ${mizajRes.percentages.safrawi}%"></div>
                <div style="width: ${mizajRes.percentages.balghami}%; background-color: #06b6d4;" title="Balghami: ${mizajRes.percentages.balghami}%"></div>
                <div style="width: ${mizajRes.percentages.sawdawi}%; background-color: #8b5cf6;" title="Sawdawi: ${mizajRes.percentages.sawdawi}%"></div>
              </div>
            </div>

            <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300">
              <strong class="text-emerald-400">Dietary Directive (Ilaj bil-Ghiza):</strong> ${mizajRes.dietaryDirective}
            </div>

            <!-- Sharing & Action Controls -->
            <div class="flex flex-col sm:flex-row gap-2 pt-1">
              <button onclick="shareMizajOnWhatsApp('${mizajRes.title}', 'Damawi: ${mizajRes.percentages.damawi}%, Safrawi: ${mizajRes.percentages.safrawi}%, Balghami: ${mizajRes.percentages.balghami}%, Sawdawi: ${mizajRes.percentages.sawdawi}%')" class="flex-1 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition flex items-center justify-center gap-2">
                <span>💬</span> WhatsApp Result to Dr. Irfan Ashraf
              </button>
              <button onclick="copyMizajSummary('${mizajRes.title}', 'Damawi: ${mizajRes.percentages.damawi}%, Safrawi: ${mizajRes.percentages.safrawi}%, Balghami: ${mizajRes.percentages.balghami}%, Sawdawi: ${mizajRes.percentages.sawdawi}%', '${mizajRes.dietaryDirective}')" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs rounded-xl border border-slate-700 transition">
                Copy Summary
              </button>
            </div>
          </div>
        </div>
      `;
    }
    window.renderMizajAssessmentModal = renderMizajAssessmentModal;


    function toggleOrganAxisModal(show = true) {
      const modal = document.getElementById('organ-axis-modal');
      if (!modal) return;
      if (show) {
        renderOrganAxisModal();
        modal.classList.remove('hidden');
      } else {
        modal.classList.add('hidden');
      }
    }
    window.toggleOrganAxisModal = toggleOrganAxisModal;

    function renderOrganAxisModal() {
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
              🔄 Reset Screener
            </button>
          </div>

          <!-- Overall Health Score Bar -->
          <div class="p-4 rounded-2xl bg-slate-950 border border-teal-500/40 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
            <div>
              <span class="text-[10px] font-mono text-slate-400 uppercase">CALCULATED ORGAN-AXIS EQUILIBRIUM:</span>
              <div class="text-xl font-black text-teal-300">${axisRes.score} / 100</div>
              <span class="text-xs text-slate-300">${axisRes.summary}</span>
            </div>
            <div class="text-right">
              <span class="text-[10px] font-mono text-rose-400 block uppercase">PRIMARY FLAGGED STASIS:</span>
              <span class="text-xs font-bold text-white">${axisRes.primaryAxis.name.split('(')[0]}</span>
            </div>
          </div>

          <!-- 12 Organ Axes Selection & Symptoms -->
          <div class="space-y-3">
            <h5 class="text-xs font-bold text-slate-300 uppercase tracking-wider">Tap an Axis to Select Active Symptoms:</h5>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              ${organAxesList.map((ax, idx) => {
                const count = (window.selectedAxisSymptoms && window.selectedAxisSymptoms[idx] && window.selectedAxisSymptoms[idx].length) || 0;
                const isSelected = window.currentOrganAxisIdx === idx;
                return `
                  <button onclick="setOrganAxis(${idx})" class="p-2.5 rounded-xl border text-left transition flex flex-col justify-between ${isSelected ? 'bg-teal-600 text-white border-teal-400 shadow' : 'bg-slate-950 text-slate-300 border-slate-800 hover:bg-slate-900'}">
                    <span class="text-[10px] font-mono opacity-80">${idx + 1}. ${ax.latin.split(' ')[0]}</span>
                    <span class="text-xs font-bold line-clamp-1 mt-0.5">${ax.name.split('(')[0]}</span>
                    ${count > 0 ? `<span class="text-[9px] font-mono px-1.5 py-0.2 rounded bg-rose-500/30 text-rose-200 mt-1 inline-block w-max font-bold">${count} Symptoms</span>` : ''}
                  </button>
                `;
              }).join('')}
            </div>

            <!-- Active Axis Symptom Checklist -->
            <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-3 mt-3">
              <div class="border-b border-slate-800 pb-2">
                <span class="text-xs font-bold text-white">${organAxesList[window.currentOrganAxisIdx].name}</span>
                <p class="text-[11px] text-slate-400">${organAxesList[window.currentOrganAxisIdx].desc}</p>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                ${organAxesList[window.currentOrganAxisIdx].symptoms.map(s => {
                  const sel = window.selectedAxisSymptoms && window.selectedAxisSymptoms[window.currentOrganAxisIdx] && window.selectedAxisSymptoms[window.currentOrganAxisIdx].includes(s);
                  return `
                    <div onclick="toggleAxisSymptom(${window.currentOrganAxisIdx}, '${s.replace(/'/g, "\\'")}')" class="p-2.5 rounded-xl border transition flex items-center justify-between cursor-pointer ${sel ? 'bg-rose-950/40 border-rose-500 text-white' : 'bg-slate-900 border-slate-800 text-slate-300 hover:bg-slate-850'}">
                      <span class="text-xs">${s}</span>
                      <span>${sel ? '✅' : '⚪'}</span>
                    </div>
                  `;
                }).join('')}
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="pt-2 flex flex-col sm:flex-row gap-2">
            <button onclick="shareAxisOnWhatsApp(${axisRes.score}, '${axisRes.primaryAxis.name.replace(/'/g, "\\'")}', ${axisRes.totalSymptomsFlagged})" class="flex-1 py-2.5 bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs rounded-xl shadow transition flex items-center justify-center gap-2">
              <span>💬</span> Send Organ-Axis Report to Dr. Irfan Ashraf
            </button>
            <button onclick="copyAxisSummary(${axisRes.score}, '${axisRes.primaryAxis.name.replace(/'/g, "\\'")}', '${axisRes.primaryAxis.rootCause.replace(/'/g, "\\'")}')" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs rounded-xl border border-slate-700 transition">
              Copy Report
            </button>
          </div>

        </div>
      `;
    }
    window.renderOrganAxisModal = renderOrganAxisModal;
'''

    if 'function toggleMizajAssessmentModal' not in js:
        js += '\n' + modal_renderers_js
        print("✓ Appended toggleMizajAssessmentModal & renderOrganAxisModal to js/zayvora-core.js")

    # Update setPreviewMizaj to update modal smoothly
    js = js.replace(
        "previewMizajAnswers[question] = value;\n      const scrollY = window.scrollY;\n      renderWebsiteApp(document.getElementById('workspace-container'));\n      window.scrollTo(0, scrollY);",
        "previewMizajAnswers[question] = value;\n      if (document.getElementById('mizaj-assessment-modal') && !document.getElementById('mizaj-assessment-modal').classList.contains('hidden')) {\n        renderMizajAssessmentModal();\n      } else {\n        const scrollY = window.scrollY;\n        renderWebsiteApp(document.getElementById('workspace-container'));\n        window.scrollTo(0, scrollY);\n      }"
    )

    # Update resetMizajAssessment
    js = js.replace(
        "window.previewMizajAnswers = { temp: 'cold', moisture: 'moist', physique: 'broad', digestion: 'sluggish', sleep: 'deep', disposition: 'calm' };\n      const scrollY = window.scrollY;\n      renderWebsiteApp(document.getElementById('workspace-container'));\n      window.scrollTo(0, scrollY);\n      showNotification('Mizaj assessment reset to default baseline.', 'info');",
        "window.previewMizajAnswers = { temp: 'cold', moisture: 'moist', physique: 'broad', digestion: 'sluggish', sleep: 'deep', disposition: 'calm' };\n      if (document.getElementById('mizaj-assessment-modal') && !document.getElementById('mizaj-assessment-modal').classList.contains('hidden')) {\n        renderMizajAssessmentModal();\n      } else {\n        const scrollY = window.scrollY;\n        renderWebsiteApp(document.getElementById('workspace-container'));\n        window.scrollTo(0, scrollY);\n      }\n      showNotification('Mizaj assessment reset to default baseline.', 'info');"
    )

    # Update toggleAxisSymptom
    js = js.replace(
        "const scrollY = window.scrollY;\n      renderWebsiteApp(document.getElementById('workspace-container'));\n      window.scrollTo(0, scrollY);",
        "if (document.getElementById('organ-axis-modal') && !document.getElementById('organ-axis-modal').classList.contains('hidden')) {\n        renderOrganAxisModal();\n      } else {\n        const scrollY = window.scrollY;\n        renderWebsiteApp(document.getElementById('workspace-container'));\n        window.scrollTo(0, scrollY);\n      }"
    )

    # Update resetAxisAssessment
    js = js.replace(
        "window.selectedAxisSymptoms = {};\n      const scrollY = window.scrollY;\n      renderWebsiteApp(document.getElementById('workspace-container'));\n      window.scrollTo(0, scrollY);\n      showNotification('Organ Axis screener reset. All symptoms cleared.', 'info');",
        "window.selectedAxisSymptoms = {};\n      if (document.getElementById('organ-axis-modal') && !document.getElementById('organ-axis-modal').classList.contains('hidden')) {\n        renderOrganAxisModal();\n      } else {\n        const scrollY = window.scrollY;\n        renderWebsiteApp(document.getElementById('workspace-container'));\n        window.scrollTo(0, scrollY);\n      }\n      showNotification('Organ Axis screener reset. All symptoms cleared.', 'info');"
    )

    # 3. STREAMLINE LANDING PAGE: Replace heavy inline sections 12143 to 12500 in renderWebsiteApp
    # Search for the start of mizaj section and end of organ-axis section
    mizaj_marker = r'<!-- 5. FREE COMPREHENSIVE MIZAJ ASSESSMENT (AL-AJNAS AL-ASHRAH) -->'
    opd_marker = r'<!-- 6. INSTANT OPD REGISTRATION & CLINIC TOKEN DISPATCH -->'

    sleek_replacement = r'''<!-- ===================================================================== -->
          <!-- 5. FREE CLINICAL SELF-ASSESSMENT SUITE (STREAMLINED MODAL LAUNCHERS)  -->
          <!-- ===================================================================== -->
          <div id="mizaj-assessment-section" class="space-y-6">
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
              <div class="p-6 rounded-3xl bg-gradient-to-br from-[#0F172A] to-[#1E293B] border-2 border-emerald-500/40 shadow-xl space-y-4 flex flex-col justify-between">
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

    # Perform replacement if marker is in js
    if mizaj_marker in js and opd_marker in js:
        start_idx = js.find(mizaj_marker)
        end_idx = js.find(opd_marker)
        js = js[:start_idx] + sleek_replacement + js[end_idx:]
        print("✓ Streamlined Mizaj & Organ-Axis on Landing Page into Sleek Modal Launchers")

    # Also streamline the redundant Afaal Treatment Cascade
    afaal_marker = r'<!-- 8. REGIMENAL TREATMENT CASCADE (AFAAL) -->'
    products_marker = r'<!-- 9. FEATURED CLINICAL FORMULATIONS (SHOPPING) -->'
    if afaal_marker in js and products_marker in js:
        start_afaal = js.find(afaal_marker)
        end_afaal = js.find(products_marker)
        js = js[:start_afaal] + js[end_afaal:]
        print("✓ Removed redundant Afaal Treatment Cascade from home page")

    with open("js/zayvora-core.js", "w", encoding="utf-8") as f:
        f.write(js)

    print("✓ Successfully updated js/zayvora-core.js")

if __name__ == '__main__':
    main()
