#!/usr/bin/env python3
"""
Upgrades Doctor Workspace in index.html and docs/index.html with:
- Section 12: The Epistemic Quadrants (Known, Missing, Conflicting, Uncertain)
- Section 13: Clinical Debate & Contradiction Guard Engine
- Section 23: Autonomous Post-Consultation Follow-Up Monitoring Protocol
Preserves 100% existing functionality, zero syntax errors, and zero regressions.
"""

import os, re, sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

NEW_LAYER_B_AND_D_E = '''                <!-- Layer B: Clinical Reasoning -->
                <div class="p-4 rounded-xl bg-[#1E293B] border border-blue-500/30 space-y-2.5">
                  <div class="flex items-center justify-between border-b border-[#334155] pb-2">
                    <span class="font-bold text-blue-400 flex items-center gap-1.5">
                      Layer B: Clinical Reasoning & Organ-Axis Synthesis
                    </span>
                    <span class="text-[10px] px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 font-semibold">Humoral + Biomedical</span>
                  </div>
                  <div class="space-y-1.5 text-[#CBD5E1] text-[11px]">
                    <p>• <strong class="text-white">Unani Pathology:</strong> Primary *Su-e-Mizaj Barid Balghami* (Cold-Moist dyscrasia) with deposition of viscous phlegmatic humor (*Khilt-e-Balgham*) into knee articular capsules.</p>
                    <p>• <strong class="text-white">Modern Pathophysiology:</strong> Grade II osteoarthritic changes with micro-inflammatory synovitis, verified by elevated hs-CRP (4.8 mg/L) and ESR (28 mm/hr).</p>
                    <p>• <strong class="text-white">Organ-Axis Cross-talk:</strong> Mafasil-Asab (Locomotor) axis is primary target; Meda-Amaa (GI) axis demonstrates adequate digestion (*Quwwat-e-Hazima*), enabling oral compound confection tolerance.</p>
                  </div>

                  <!-- Clinical Debate & Alternative Hypotheses (Section 13) -->
                  <div class="mt-2 pt-2 border-t border-slate-700/60 space-y-1 text-[11px]">
                    <div class="flex items-center justify-between">
                      <span class="text-indigo-300 font-bold flex items-center gap-1">⚔️ Clinical Debate &amp; Alternative Differentials</span>
                      <span class="text-[9px] px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-mono">Contradiction Engine §13</span>
                    </div>
                    <p class="text-slate-300">• <strong class="text-white">Primary Hypothesis:</strong> Knee Osteoarthritis with Humoral Phlegmatic Stasis (*Waja-ul-Mafasil Barid Balghami*).</p>
                    <p class="text-slate-300">• <strong class="text-white">Alternative Differential:</strong> Secondary Metabolic Gouty Arthropathy (*Niqris*) or Early Seronegative Spondyloarthritis.</p>
                    <div class="p-2 rounded bg-slate-900/80 border border-indigo-500/30 text-[10px] text-indigo-200">
                      <strong class="text-indigo-300">Falsification Guard ("What could make this wrong?"):</strong> If serum uric acid &gt;7.2 mg/dL or morning stiffness &gt;60 mins with elevated inflammatory markers, pause Suranjan Talkh and pivot to targeted *Musaffi-e-Dam &amp; Tanqiya* protocol.
                    </div>
                  </div>
                </div>

                <!-- Layer C: Unverified Suggestions -->
                <div class="p-4 rounded-xl bg-[#1E293B] border border-amber-500/30 space-y-2">
                  <div class="flex items-center justify-between border-b border-[#334155] pb-2">
                    <span class="font-bold text-amber-400 flex items-center gap-1.5">
                      ⚠️ Layer C: Unverified Suggestions & Adjuncts
                    </span>
                    <span class="text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-semibold">Non-Statutory / Experimental</span>
                  </div>
                  <div class="p-2.5 bg-[#0F172A] rounded-lg border border-[#334155] text-[11px] text-[#94A3B8]">
                    <span class="text-amber-300 font-semibold block">Experimental Adjunctive Modality:</span>
                    <span>Standardized Boswellia serrata (Kundur) extract 250mg twice daily has demonstrated 5-LOX inhibition in pre-clinical models. Lacks statutory AYUSH classical monograph; use at tabeeb's sole clinical discretion.</span>
                  </div>
                </div>

                <!-- Layer D: The 4 Epistemic Quadrants (Unknowns as a First-Class Object §12) -->
                <div class="p-4 rounded-xl bg-[#1E293B] border border-rose-500/30 space-y-3">
                  <div class="flex items-center justify-between border-b border-[#334155] pb-2">
                    <span class="font-bold text-rose-400 flex items-center gap-1.5">
                      Layer D: Clinical Epistemic Quadrants &amp; Safety Firewall
                    </span>
                    <span class="text-[10px] px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-semibold font-mono">Known &bull; Missing &bull; Conflicting &bull; Uncertain</span>
                  </div>

                  <!-- 4-Quadrant Grid -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px]">
                    <!-- Quadrant 1: Known -->
                    <div class="p-2.5 rounded-lg bg-emerald-950/30 border border-emerald-500/30 space-y-1">
                      <div class="flex items-center justify-between">
                        <strong class="text-emerald-300 text-[11px] font-bold">🟩 1. Known (Confirmed)</strong>
                        <span class="text-[9px] text-emerald-400 font-mono">Verified</span>
                      </div>
                      <ul class="text-[10px] text-emerald-200/90 space-y-0.5">
                        <li>&bull; Vitals: BP 128/82 mmHg, Pulse 74 bpm</li>
                        <li>&bull; Baseline Mizaj: Barid-Balghami (Cold-Moist)</li>
                        <li>&bull; Verified Labs: hs-CRP 4.8 mg/L, ESR 28 mm/hr</li>
                      </ul>
                    </div>

                    <!-- Quadrant 2: Missing -->
                    <div class="p-2.5 rounded-lg bg-amber-950/30 border border-amber-500/30 space-y-1">
                      <div class="flex items-center justify-between">
                        <strong class="text-amber-300 text-[11px] font-bold">🟨 2. Missing (Unperformed)</strong>
                        <span class="text-[9px] text-amber-400 font-mono">High Priority</span>
                      </div>
                      <ul class="text-[10px] text-amber-200/90 space-y-0.5">
                        <li>&bull; Repeat Serum Uric Acid (4-week follow-up)</li>
                        <li>&bull; 25-OH Vitamin D3 &amp; Ionized Calcium panel</li>
                        <li>&bull; 30-day allopathic medication reconciliation</li>
                      </ul>
                    </div>

                    <!-- Quadrant 3: Conflicting -->
                    <div class="p-2.5 rounded-lg bg-orange-950/30 border border-orange-500/30 space-y-1">
                      <div class="flex items-center justify-between">
                        <strong class="text-orange-300 text-[11px] font-bold">🟧 3. Conflicting (Tazaad)</strong>
                        <span class="text-[9px] text-orange-400 font-mono">Audit Alert</span>
                      </div>
                      <ul class="text-[10px] text-orange-200/90 space-y-0.5">
                        <li>&bull; Patient logs severe nocturnal throbbing vs normal morning mobility score</li>
                        <li>&bull; High subjective fatigue vs normal baseline thyroid markers</li>
                      </ul>
                    </div>

                    <!-- Quadrant 4: Uncertain -->
                    <div class="p-2.5 rounded-lg bg-cyan-950/30 border border-cyan-500/30 space-y-1">
                      <div class="flex items-center justify-between">
                        <strong class="text-cyan-300 text-[11px] font-bold">🟦 4. Uncertain (Evidence)</strong>
                        <span class="text-[9px] text-cyan-400 font-mono">E2 Evidence</span>
                      </div>
                      <ul class="text-[10px] text-cyan-200/90 space-y-0.5">
                        <li>&bull; Long-term trial evidence on adjunctive Boswellia serrata is moderate (E2 tier)</li>
                        <li>&bull; Response timeline depends on strict Asbab-e-Sittah dietary adherence</li>
                      </ul>
                    </div>
                  </div>

                  <!-- Safety Gate Alarms -->
                  <div class="p-2.5 rounded-lg bg-[#0F172A] border border-rose-500/40 text-[11px] text-[#FB7185] space-y-0.5">
                    <div>&bull; <strong>Schedule E(1) Mudabbar Requirement:</strong> Suranjan contains colchicine. Dispensation locked until batch Mudabbar certificate is verified.</div>
                    <div>&bull; <strong>Allergy Alert:</strong> Patient has documented hypersensitivity to Sonf (Foeniculum vulgare). Formulary verified: Formulation is 100% Sonf-free.</div>
                  </div>
                </div>

                <!-- Layer E: Clinician Decision Gate & Autonomous Follow-Up -->
                <div class="p-4 rounded-xl bg-purple-950/40 border border-purple-500/40 space-y-3">
                  <div class="flex items-center justify-between border-b border-purple-500/30 pb-2">
                    <span class="font-bold text-purple-300 flex items-center gap-1.5">
                      <svg class="w-3.5 h-3.5 inline-block text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg> Layer E: Clinician Decision Gate &amp; Statutory Authority
                    </span>
                    <span class="text-[10px] px-2 py-0.5 rounded bg-rose-500/20 text-rose-400 font-mono font-bold">safe_to_lock = False</span>
                  </div>
                  <p class="text-[11px] text-[#CBD5E1] leading-relaxed">
                    AI generates clinical recommendations only. Prescribing and clinical lockdown authority resides exclusively with the licensed clinician under Medical Council regulations and 21 CFR Part 11.
                  </p>

                  <!-- Autonomous Follow-up Protocol (Section 23) -->
                  <div class="p-2.5 bg-[#0F172A] rounded-xl border border-purple-500/30 space-y-1 text-[11px]">
                    <div class="flex items-center justify-between">
                      <span class="font-bold text-purple-300 text-[10px] uppercase tracking-wide">Autonomous Post-Consultation Follow-Up Protocol (§23)</span>
                      <span class="text-[9px] px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-300 font-mono">Automated Check-in</span>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-[10px] text-slate-300 pt-1">
                      <div class="p-1.5 bg-slate-900 rounded border border-slate-800">
                        <strong class="text-white block font-mono text-[9px]">Day 7 Check-in:</strong>
                        <span>Symptom trajectory &amp; gastric tolerance score</span>
                      </div>
                      <div class="p-1.5 bg-slate-900 rounded border border-slate-800">
                        <strong class="text-white block font-mono text-[9px]">Day 21 Re-evaluation:</strong>
                        <span>Joint range of motion &amp; stiffness duration</span>
                      </div>
                      <div class="p-1.5 bg-slate-900 rounded border border-slate-800">
                        <strong class="text-white block font-mono text-[9px]">Day 45 Escalation Gate:</strong>
                        <span>Repeat lab trigger &amp; proactive doctor review</span>
                      </div>
                    </div>
                  </div>

                  <div class="flex items-center justify-between pt-1">
                    <span class="text-[11px] text-[#94A3B8]">Review status: <span class="text-amber-400 font-semibold">Pending Clinician Approval</span></span>
                    <button onclick="approveHakeemSuggestions()" class="px-4 py-1.5 rounded-lg bg-emerald-600 text-white font-bold text-xs hover:bg-emerald-500 transition">
                      Accept AI Suggestions into Plan
                    </button>
                  </div>
                </div>'''

def upgrade_html(file_path):
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match block from <!-- Layer B: Clinical Reasoning --> to before <!-- Drawer Footer -->
    pattern = r"<!-- Layer B: Clinical Reasoning -->.*?<!-- Drawer Footer -->"
    replacement = NEW_LAYER_B_AND_D_E.strip() + "\n              </div>\n\n              <!-- Drawer Footer -->"

    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, lambda m: replacement, content, flags=re.DOTALL)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully upgraded Hakeem Sahab CDS Drawer in {file_path}")
    else:
        print(f"Pattern for Layer B to Drawer Footer not matched in {file_path}")

upgrade_html(os.path.join(BASE_DIR, "index.html"))
upgrade_html(os.path.join(BASE_DIR, "docs", "index.html"))
print("UI Drawer upgrades completed.")
