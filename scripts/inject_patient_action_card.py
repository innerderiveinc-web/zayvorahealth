import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_marker = '<!-- Dashboard Action Grid -->'
patient_action_card = """<!-- PRIMARY ACTION CARD: "WHAT DO I DO TODAY?" -->
            <div class="p-6 rounded-2xl bg-gradient-to-r from-emerald-950/70 via-[var(--card)] to-slate-900 border-2 border-emerald-500/40 shadow-xl space-y-4">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-3">
                <div class="flex items-center gap-3">
                  <span class="w-9 h-9 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 flex items-center justify-center font-bold text-base">
                    ☀️
                  </span>
                  <div>
                    <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">TODAY'S CARE • NEXT ACTION</span>
                    <h3 class="text-base font-bold text-white">Morning Regimen: Hab-e-Suranjan (2 pills) + Roghan Massage</h3>
                  </div>
                </div>
                <span class="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-mono font-bold text-xs border border-emerald-500/30">
                  Due: 08:30 AM
                </span>
              </div>

              <p class="text-xs text-[var(--muted)] leading-relaxed">
                Take with lukewarm water after breakfast. Co-apply Roghan-e-Suranjan gently on affected knees in clockwise circular motion. Avoid cold wind exposure.
              </p>

              <!-- Frictionless Adherence Interaction -->
              <div class="flex flex-wrap items-center justify-between gap-3 pt-1 border-t border-[var(--border)]">
                <div class="flex items-center gap-2 text-xs">
                  <span class="text-[var(--muted)] font-medium">Did you take your morning care?</span>
                  <button onclick="trackPatientAdherence('TAKEN', 'Hab-e-Suranjan & Roghan')" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow transition">
                    ✓ Yes, Taken
                  </button>
                  <button onclick="trackPatientAdherence('NOT_YET', 'Hab-e-Suranjan & Roghan')" class="px-3 py-1.5 rounded-lg border border-[var(--border)] text-xs text-[var(--muted)] hover:text-white transition">
                    ⏳ Not Yet
                  </button>
                  <button onclick="trackPatientAdherence('SKIPPED', 'Hab-e-Suranjan & Roghan')" class="px-3 py-1.5 rounded-lg border border-rose-500/30 text-rose-400 hover:bg-rose-500/10 text-xs transition">
                    ✕ Skipped
                  </button>
                </div>
                <div class="flex items-center gap-2 text-xs">
                  <span class="text-emerald-400 font-bold">14-Day Streak!</span>
                  <span class="text-[10px] text-[var(--muted)]">93% Adherence</span>
                </div>
              </div>
            </div>

            <!-- Dashboard Action Grid -->"""

if '<!-- PRIMARY ACTION CARD: "WHAT DO I DO TODAY?" -->' not in html:
    html = html.replace(target_marker, patient_action_card, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Successfully injected Patient 'What do I do today?' Action Card into index.html and docs/index.html")
else:
    print("Action card already present")
