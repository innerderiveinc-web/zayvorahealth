import os

path = "js/zayvora-core.js"
with open(path, "r", encoding="utf-8") as f:
    js = f.read()

old_toolbar = """            <!-- CLINICIAN DIAGNOSTIC & FUNCTIONAL TIBB SUITE (OMNIPRESENT TOOLBAR) -->
            <div class="p-4 rounded-2xl bg-gradient-to-r from-slate-900 to-slate-950 border border-emerald-500/40 space-y-2.5 shadow-md">
              <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs">🧠</span>
                  <h4 class="text-xs font-bold text-white uppercase tracking-wider">Clinician Diagnostic Desk • ZAYVORA Diagnostic &amp; Clinical Engines</h4>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-[10px] font-mono text-emerald-400">10 Tools Active</span>
                  <button onclick="toggleGlobalToolsModal(true)" class="text-[10px] text-slate-400 hover:text-white font-mono underline">View All →</button>
                </div>
              </div>
              <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2 text-xs">
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
            </div>"""

new_toolbar = """            ${(state.platformEdition === 'clinic') ? `
            <!-- AASAN MATAB DESK HEADER (CLEAN & MINIMALIST FOR CLINIC) -->
            <div class="p-4 rounded-2xl bg-gradient-to-r from-emerald-950/70 via-slate-900 to-slate-950 border border-emerald-500/40 shadow-md flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
              <div class="flex items-center gap-3">
                <span class="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 flex items-center justify-center font-bold text-lg">🌿</span>
                <div>
                  <h4 class="text-sm font-bold text-white flex items-center gap-2">
                    Aasan Matab Desk Active
                    <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-[10px] font-mono font-bold border border-emerald-500/30">⚡ 1-Minute OPD</span>
                  </h4>
                  <p class="text-xs text-slate-300">Tez OPD, Nabz/Mizaj Tashkhees, Qarabadeen Nuskha aur 1-Click Parchi Print</p>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <button onclick="setConsultationMode('fast'); switchTab('consultation');" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md transition flex items-center gap-1.5 cursor-pointer">
                  <span>⚡</span> Start 1-Minute Consultation →
                </button>
                <button onclick="toggleGlobalToolsModal(true)" class="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs border border-slate-700 transition flex items-center gap-1.5 cursor-pointer" title="Access All 10 Global Diagnostic Engines">
                  <span>🧠</span> Research Tools (10) ▾
                </button>
              </div>
            </div>
            ` : `
            <!-- CLINICIAN DIAGNOSTIC & FUNCTIONAL TIBB SUITE (OMNIPRESENT TOOLBAR) -->
            <div class="p-4 rounded-2xl bg-gradient-to-r from-slate-900 to-slate-950 border border-emerald-500/40 space-y-2.5 shadow-md">
              <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs">🧠</span>
                  <h4 class="text-xs font-bold text-white uppercase tracking-wider">Clinician Diagnostic Desk • ZAYVORA Diagnostic &amp; Clinical Engines</h4>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-[10px] font-mono text-emerald-400">10 Tools Active</span>
                  <button onclick="toggleGlobalToolsModal(true)" class="text-[10px] text-slate-400 hover:text-white font-mono underline">View All →</button>
                </div>
              </div>
              <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2 text-xs">
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
            `}"""

if old_toolbar in js:
    js = js.replace(old_toolbar, new_toolbar)
    with open(path, "w", encoding="utf-8") as f:
        f.write(js)
    print("SUCCESS: Collapsed today tab diagnostic toolbar for Clinic Mode!")
else:
    print("Old toolbar not found")
