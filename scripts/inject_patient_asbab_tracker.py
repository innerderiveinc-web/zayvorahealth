#!/usr/bin/env python3
"""
Injects the Daily Asbab-e-Sitta (6 Essentials) Equilibrium Companion into js/zayvora-core.js
"""
import re

CORE_FILE = "js/zayvora-core.js"

ASBAB_CARD_HTML = '''
            <!-- DAILY ASBAB-E-SITTA (6 ESSENTIALS) EQUILIBRIUM COMPANION -->
            <div class="bg-[var(--card)] border border-emerald-500/30 rounded-2xl p-6 shadow-xl space-y-4">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-3">
                <div class="flex items-center gap-3">
                  <span class="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 flex items-center justify-center font-bold text-lg">
                    ⚖️
                  </span>
                  <div>
                    <div class="flex items-center gap-2">
                      <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">CANONICAL LIFESTYLE ARCHITECTURE</span>
                      <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-bold">IBN SINA ASBAB-E-SITTA</span>
                    </div>
                    <h3 class="text-base font-bold text-white mt-0.5">Daily Asbab-e-Sitta Equilibrium Companion™ (اسبابِ ستہ ضروریہ)</h3>
                    <p class="text-xs text-[var(--muted)]">6 Daily biological imperatives for constitutional balance, metabolic vitality, and chronic healing.</p>
                  </div>
                </div>
                <div class="flex items-center gap-3">
                  <div class="text-right">
                    <span class="text-xs text-slate-400 block font-mono">Today\'s Equilibrium</span>
                    <span id="patient-mizaj-score-display" class="text-lg font-black text-emerald-400 font-mono">83%</span>
                  </div>
                  <div class="px-3 py-1.5 rounded-xl bg-amber-950/60 border border-amber-500/40 text-amber-300 font-mono text-xs font-bold flex items-center gap-1.5">
                    <span>🔥</span> 14-Day Streak
                  </div>
                </div>
              </div>

              <!-- 6 Essentials Interactive Habit Grid -->
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs" id="asbab-check-grid">
                <!-- 1. Hawa -->
                <div onclick="toggleAsbabPillar(0)" id="asbab-pillar-0" class="cursor-pointer p-3.5 rounded-xl bg-slate-900/90 border border-emerald-500/40 text-white space-y-1.5 transition hover:border-emerald-400 shadow-sm">
                  <div class="flex justify-between items-center">
                    <span class="font-bold text-emerald-300 flex items-center gap-1.5"><span>💨</span> 1. Hawa (Air & Breath)</span>
                    <span class="asbab-check-icon text-xs text-emerald-400 font-bold">✓ DONE</span>
                  </div>
                  <p class="text-[11px] text-slate-300">10 mins deep diaphragmatic oxygenation (*Tarweeh & Tanqiya*). Fresh morning air.</p>
                </div>

                <!-- 2. Makool-o-Mashroob -->
                <div onclick="toggleAsbabPillar(1)" id="asbab-pillar-1" class="cursor-pointer p-3.5 rounded-xl bg-slate-900/90 border border-emerald-500/40 text-white space-y-1.5 transition hover:border-emerald-400 shadow-sm">
                  <div class="flex justify-between items-center">
                    <span class="font-bold text-emerald-300 flex items-center gap-1.5"><span>🥗</span> 2. Makool (Nutrition)</span>
                    <span class="asbab-check-icon text-xs text-emerald-400 font-bold">✓ DONE</span>
                  </div>
                  <p class="text-[11px] text-slate-300">Warm cooked constitutional diet matching your Balghami Mizaj. Avoided ice water.</p>
                </div>

                <!-- 3. Harkat-o-Sukoon Badani -->
                <div onclick="toggleAsbabPillar(2)" id="asbab-pillar-2" class="cursor-pointer p-3.5 rounded-xl bg-slate-900/90 border border-emerald-500/40 text-white space-y-1.5 transition hover:border-emerald-400 shadow-sm">
                  <div class="flex justify-between items-center">
                    <span class="font-bold text-emerald-300 flex items-center gap-1.5"><span>🚶</span> 3. Harkat Badani (Movement)</span>
                    <span class="asbab-check-icon text-xs text-emerald-400 font-bold">✓ DONE</span>
                  </div>
                  <p class="text-[11px] text-slate-300">30 mins brisk walking & knee mobility stretches + morning solar absorption (*Tashmees*).</p>
                </div>

                <!-- 4. Harkat-o-Sukoon Nafsani -->
                <div onclick="toggleAsbabPillar(3)" id="asbab-pillar-3" class="cursor-pointer p-3.5 rounded-xl bg-slate-900/90 border border-emerald-500/40 text-white space-y-1.5 transition hover:border-emerald-400 shadow-sm">
                  <div class="flex justify-between items-center">
                    <span class="font-bold text-emerald-300 flex items-center gap-1.5"><span>🧠</span> 4. Harkat Nafsani (Mind)</span>
                    <span class="asbab-check-icon text-xs text-emerald-400 font-bold">✓ DONE</span>
                  </div>
                  <p class="text-[11px] text-slate-300">Emotional equanimity, stress neutralization, prayer and contemplative pause.</p>
                </div>

                <!-- 5. Naum-o-Yaqzah -->
                <div onclick="toggleAsbabPillar(4)" id="asbab-pillar-4" class="cursor-pointer p-3.5 rounded-xl bg-slate-900/90 border border-emerald-500/40 text-white space-y-1.5 transition hover:border-emerald-400 shadow-sm">
                  <div class="flex justify-between items-center">
                    <span class="font-bold text-emerald-300 flex items-center gap-1.5"><span>🌙</span> 5. Naum (Restorative Sleep)</span>
                    <span class="asbab-check-icon text-xs text-emerald-400 font-bold">✓ DONE</span>
                  </div>
                  <p class="text-[11px] text-slate-300">7.5 hours uninterrupted circadian sleep. Slept before 10:30 PM.</p>
                </div>

                <!-- 6. Ihtibas-o-Istifragh -->
                <div onclick="toggleAsbabPillar(5)" id="asbab-pillar-5" class="cursor-pointer p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 text-slate-400 space-y-1.5 transition hover:border-emerald-400 shadow-sm">
                  <div class="flex justify-between items-center">
                    <span class="font-bold text-slate-300 flex items-center gap-1.5"><span>🔄</span> 6. Istifragh (Elimination)</span>
                    <span class="asbab-check-icon text-xs text-slate-500 font-bold">⏳ PENDING</span>
                  </div>
                  <p class="text-[11px] text-slate-400">Regular morning bowel transit & gentle sweating. Tap when completed today.</p>
                </div>
              </div>

              <!-- Footer with Scientific Crosswalk Link -->
              <div class="pt-2 border-t border-[var(--border)] flex flex-col sm:flex-row justify-between items-center gap-2 text-xs">
                <span class="text-slate-400 text-[11px]">Logged in real time into Dr. Irfan Ashraf\'s clinical review ledger.</span>
                <button onclick="openBotanicalAtlasModal()" class="px-3.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-emerald-500/40 text-emerald-300 text-xs font-bold transition flex items-center gap-1.5">
                  <span>🌿</span> Explore Ibn Sina ⟷ PubMed Molecular Crosswalk &rarr;
                </button>
              </div>
            </div>
'''

ASBAB_JS_LOGIC = '''
    // ── ASBAB-E-SITTA INTERACTIVE EQUILIBRIUM TRACKER ────────────────────────
    window.asbabStates = [true, true, true, true, true, false];
    function toggleAsbabPillar(index) {
      if (!window.asbabStates) window.asbabStates = [true, true, true, true, true, false];
      window.asbabStates[index] = !window.asbabStates[index];
      const el = document.getElementById(`asbab-pillar-${index}`);
      if (!el) return;
      const isDone = window.asbabStates[index];
      const checkIcon = el.querySelector('.asbab-check-icon');
      if (isDone) {
        el.classList.remove('border-slate-800', 'text-slate-400');
        el.classList.add('border-emerald-500/40', 'text-white');
        if (checkIcon) {
          checkIcon.classList.remove('text-slate-500');
          checkIcon.classList.add('text-emerald-400');
          checkIcon.innerText = '✓ DONE';
        }
      } else {
        el.classList.remove('border-emerald-500/40', 'text-white');
        el.classList.add('border-slate-800', 'text-slate-400');
        if (checkIcon) {
          checkIcon.classList.remove('text-emerald-400');
          checkIcon.classList.add('text-slate-500');
          checkIcon.innerText = '⏳ PENDING';
        }
      }
      const doneCount = window.asbabStates.filter(Boolean).length;
      const score = Math.round((doneCount / 6) * 100);
      const scoreEl = document.getElementById('patient-mizaj-score-display');
      if (scoreEl) scoreEl.innerText = `${score}%`;
      showNotification(`✓ Updated Asbab-e-Sitta Equilibrium Score: ${score}% (${doneCount}/6 Pillars Completed)`, 'success');
    }
'''

with open(CORE_FILE, "r") as f:
    core_code = f.read()

target_str = '<!-- LIVE OPD TOKEN & QUEUE PROGRESS TRACKER (#T-104) -->'
if target_str in core_code and '<!-- DAILY ASBAB-E-SITTA (6 ESSENTIALS) EQUILIBRIUM COMPANION -->' not in core_code:
    new_core_code = core_code.replace(target_str, ASBAB_CARD_HTML.strip() + '\n\n            ' + target_str)
    # Also append JS logic at end
    new_core_code += '\n' + ASBAB_JS_LOGIC.strip() + '\n'
    with open(CORE_FILE, "w") as f:
        f.write(new_core_code)
    print("✓ Successfully injected Asbab-e-Sitta Companion into js/zayvora-core.js")
else:
    print("Notice: Target already injected or not found.")
