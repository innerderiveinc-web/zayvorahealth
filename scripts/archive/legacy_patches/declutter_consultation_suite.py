#!/usr/bin/env python3
"""
ZAYVORA Health OS — Consultation Suite De-Clutter & Clinician Experience Upgrade
1. Simplifies Consultation Topbar: Groups academic/research tools (Core Theory, Medical Library,
   Case Practicum, Botanical Crosswalk, Safety Architecture, Bedside Mode) into a clean, dignified
   "📚 Clinical Tools & Doctrine ▾" dropdown menu.
2. In Tab 11 (Prescription Studio): Separates formulation actions into:
   - Primary Prescribing Actions: Classical Qarabadeen, ZAYVORA Products, Self-Nuskha, Dispatch.
   - Advanced Molecular/Safety Tools: Computational Twin™ and CYP450 Screener cleanly grouped.
3. Streamlines visual noise while keeping 100% of the underlying backend, APIs, and tests working.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_JS = os.path.join(BASE_DIR, "js", "zayvora-core.js")

def declutter_consultation():
    with open(CORE_JS, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. Top Bar Buttons De-clutter
    old_top_buttons = """            <div class="flex items-center gap-2 flex-wrap">
              <div class="flex items-center bg-slate-900 border border-slate-700 rounded-xl p-1 shadow-sm">
                <button onclick="setConsultationMode('fast')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition text-amber-400 hover:text-white" title="Switch to 60-Sec Fast Matab (Alt+M)">
                  ⚡ 60-Sec Fast Matab™
                </button>
                <button onclick="setConsultationMode('continuum')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition bg-emerald-600 text-white shadow" title="Current: 13-Step Continuum">
                  🔬 13-Step Detailed Continuum
                </button>
              </div>
              <button onclick="toggleHakeemDrawer(true)" class="px-3.5 py-2 rounded-xl bg-purple-600/20 border border-purple-500/40 text-purple-300 text-xs font-bold hover:bg-purple-600/30 flex items-center gap-1.5 transition">
                <svg class="w-4 h-4 inline-block text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg> Hakeem Sahab Clinical Assistant
              </button>
              <button onclick="openAgenticAiModal()" class="px-3.5 py-2 rounded-xl bg-indigo-600/20 border border-indigo-500/40 text-indigo-300 text-xs font-bold hover:bg-indigo-600/30 flex items-center gap-1.5 transition" title="ZAYVORA Clinical Governance & Safety Architecture">
                <span>⚖️</span> Clinical Safety Architecture
              </button>
              <button onclick="openCoreTheoryModal()" class="px-3.5 py-2 rounded-xl bg-amber-500/20 border border-amber-400/40 text-amber-300 text-xs font-bold hover:bg-amber-500/30 flex items-center gap-1.5 transition" title="ZAYVORA Core Medical Theory & Doctrine">
                <span>💡</span> Core Theory
              </button>
              <button onclick="openMedicalDoctrineModal()" class="px-3.5 py-2 rounded-xl bg-emerald-600/20 border border-emerald-500/40 text-emerald-300 text-xs font-bold hover:bg-emerald-600/30 flex items-center gap-1.5 transition" title="12-Volume Classical & Modern Integrative Medical Library">
                <svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg> 📖 Medical Doctrine Library
              </button>
              <button onclick="openCaseSimulatorModal()" class="px-3 py-2 rounded-xl bg-blue-600/20 border border-blue-500/40 text-blue-300 text-xs font-bold hover:bg-blue-600/30 flex items-center gap-1.5 transition" title="Accredited Clinical Case Practicum & Training">
                <span>🎓</span> Clinical Case Practicum
              </button>
              <button onclick="openBotanicalAtlasModal()" class="px-3 py-2 rounded-xl bg-amber-600/20 border border-amber-500/40 text-amber-300 text-xs font-bold hover:bg-amber-600/30 flex items-center gap-1.5 transition" title="Ibn Sina ⟷ PubMed: Integrative Molecular &amp; Classical Herb Crosswalk Engine">
                <span>🌿</span> Ibn Sina ⟷ PubMed Crosswalk
              </button>
              <button onclick="toggleMobileClinicMode()" id="btn-mobile-clinic-toggle" class="px-3 py-2 rounded-xl bg-teal-600/20 border border-teal-500/40 text-teal-300 text-xs font-bold hover:bg-teal-600/30 flex items-center gap-1.5 transition" title="Touch-Optimized Bedside Consultation Mode">
                <span>📱</span> Bedside Mode
              </button>
              <button onclick="openEmergencyRedFlagModal()" id="btn-emergency-guard" class="px-3 py-2 rounded-xl bg-rose-600/20 border border-rose-500/40 text-rose-300 text-xs font-bold hover:bg-rose-600/30 flex items-center gap-1.5 transition" title="Statutory Emergency Referral & Clinical Red-Flag Triage">
                <span>🚨</span> Red-Flag Guard
              </button>
              <button onclick="saveConsultationDraft()" class="px-3 py-2 rounded-xl border border-[var(--border)] text-xs text-[var(--muted)] hover:text-white transition">
                Save Draft
              </button>
              <button onclick="completeConsultation()" id="btn-complete-consultation" class="px-5 py-2 rounded-xl bg-emerald-600 text-white text-xs font-bold hover:bg-emerald-500 shadow-md transition">
                Sign & Lock Prescription (21 CFR 11)
              </button>
            </div>"""

    new_top_buttons = """            <div class="flex items-center gap-2 flex-wrap">
              <!-- Mode Switcher: 60-Sec Quick Matab vs Detailed (13-Step) -->
              <div class="flex items-center bg-slate-900 border border-slate-700 rounded-xl p-1 shadow-sm">
                <button onclick="setConsultationMode('fast')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition text-amber-400 hover:text-white" title="Switch to 60-Sec Fast Matab (Alt+M)">
                  ⚡ 60-Sec Fast Matab™
                </button>
                <button onclick="setConsultationMode('continuum')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition bg-emerald-600 text-white shadow" title="Current: 13-Step Continuum">
                  🔬 13-Step Detailed Continuum
                </button>
              </div>

              <!-- Core Doctor Clinical Actions -->
              <button onclick="saveConsultationDraft()" class="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-bold text-slate-200 hover:text-white transition shadow-sm flex items-center gap-1.5">
                <span>💾</span> <span>Save Draft</span>
              </button>
              <button onclick="completeConsultation()" id="btn-complete-consultation" class="px-4 py-2 rounded-xl bg-emerald-600 text-white text-xs font-bold hover:bg-emerald-500 shadow-md transition flex items-center gap-1.5">
                <span>🔒</span> <span>Sign &amp; Lock Prescription (21 CFR 11)</span>
              </button>

              <!-- Hakeem Sahab Assistant Pill -->
              <button onclick="toggleHakeemDrawer(true)" class="px-3.5 py-2 rounded-xl bg-purple-950/60 hover:bg-purple-900/80 border border-purple-500/40 text-purple-300 text-xs font-bold flex items-center gap-1.5 transition shadow-sm">
                <svg class="w-3.5 h-3.5 inline-block text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                <span>Hakeem Sahab™ Assistant</span>
              </button>

              <!-- Emergency Red-Flag Guard -->
              <button onclick="openEmergencyRedFlagModal()" id="btn-emergency-guard" class="px-3 py-2 rounded-xl bg-rose-950/40 hover:bg-rose-900/60 border border-rose-600/40 text-rose-300 text-xs font-bold flex items-center gap-1.5 transition">
                <span>🚨</span> <span>Red-Flag Guard</span>
              </button>

              <!-- Unified Clinical Tools & Doctrine Dropdown -->
              <div class="relative">
                <button onclick="toggleConsultationToolsDropdown()" class="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 hover:text-white text-xs font-bold flex items-center gap-1.5 transition shadow-sm cursor-pointer" title="Classical Doctrine, Practicum & Research Tools">
                  <span>📚</span>
                  <span>Clinical Tools &amp; Doctrine</span>
                  <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                </button>
                <div id="consultation-tools-dropdown" class="hidden absolute right-0 mt-2 w-64 bg-[#0F172A] border border-emerald-500/30 rounded-2xl p-2.5 shadow-2xl z-50 space-y-1 backdrop-blur-xl text-left">
                  <div class="px-2 py-1 text-[10px] font-mono uppercase text-slate-400 font-bold border-b border-slate-800">Knowledge &amp; Governance</div>
                  <button onclick="openMedicalDoctrineModal(); toggleConsultationToolsDropdown(false);" class="w-full text-left px-2.5 py-1.5 rounded-lg text-xs font-semibold text-slate-200 hover:bg-slate-800 hover:text-emerald-300 flex items-center gap-2 transition">
                    <span>📖</span> <span>Medical Doctrine Library</span>
                  </button>
                  <button onclick="openCoreTheoryModal(); toggleConsultationToolsDropdown(false);" class="w-full text-left px-2.5 py-1.5 rounded-lg text-xs font-semibold text-slate-200 hover:bg-slate-800 hover:text-amber-300 flex items-center gap-2 transition">
                    <span>💡</span> <span>Core Theory</span>
                  </button>
                  <button onclick="openBotanicalAtlasModal(); toggleConsultationToolsDropdown(false);" class="w-full text-left px-2.5 py-1.5 rounded-lg text-xs font-semibold text-slate-200 hover:bg-slate-800 hover:text-emerald-300 flex items-center gap-2 transition">
                    <span>🌿</span> <span>Ibn Sina ⟷ PubMed Crosswalk</span>
                  </button>
                  <button onclick="openCaseSimulatorModal(); toggleConsultationToolsDropdown(false);" class="w-full text-left px-2.5 py-1.5 rounded-lg text-xs font-semibold text-slate-200 hover:bg-slate-800 hover:text-blue-300 flex items-center gap-2 transition">
                    <span>🎓</span> <span>Clinical Case Practicum</span>
                  </button>
                  <button onclick="openAgenticAiModal(); toggleConsultationToolsDropdown(false);" class="w-full text-left px-2.5 py-1.5 rounded-lg text-xs font-semibold text-slate-200 hover:bg-slate-800 hover:text-indigo-300 flex items-center gap-2 transition">
                    <span>⚖️</span> <span>Clinical Safety Architecture</span>
                  </button>
                  <button onclick="toggleMobileClinicMode(); toggleConsultationToolsDropdown(false);" id="btn-mobile-clinic-toggle" class="w-full text-left px-2.5 py-1.5 rounded-lg text-xs font-semibold text-slate-200 hover:bg-slate-800 hover:text-teal-300 flex items-center gap-2 border-t border-slate-800 pt-1.5 transition">
                    <span>📱</span> <span>Bedside Mode</span>
                  </button>
                </div>
              </div>
            </div>"""

    if old_top_buttons in js:
        js = js.replace(old_top_buttons, new_top_buttons, 1)
        print("✓ Successfully streamlined Consultation Suite top bar with Clinical Tools dropdown")
    else:
        print("! Warning: Could not locate exact old_top_buttons in js/zayvora-core.js")

    # 2. Add toggleConsultationToolsDropdown helper if not present
    if "function toggleConsultationToolsDropdown" not in js:
        dropdown_fn = """
    function toggleConsultationToolsDropdown(force) {
      const p = document.getElementById('consultation-tools-dropdown');
      if (!p) return;
      if (typeof force === 'boolean') {
        if (force) p.classList.remove('hidden'); else p.classList.add('hidden');
      } else {
        p.classList.toggle('hidden');
      }
    }
    window.toggleConsultationToolsDropdown = toggleConsultationToolsDropdown;
"""
        js = dropdown_fn + js
        print("✓ Injected toggleConsultationToolsDropdown helper")

    # 3. Tab 11 (Prescription Studio) Formulation Bar De-clutter
    old_formulation_bar = """              <div class="grid grid-cols-2 sm:grid-cols-3 2xl:grid-cols-6 gap-2.5 pt-1">
                <button onclick="openQarabadeenCatalogModal()" class="p-2.5 bg-emerald-700/90 hover:bg-emerald-600 text-white rounded-xl font-bold text-xs shadow-sm transition flex items-center gap-2.5 text-left w-full min-w-0 overflow-hidden active:scale-[0.98]">
                  <span class="w-8 h-8 rounded-lg bg-black/20 flex items-center justify-center text-sm shrink-0">🏛️</span>
                  <div class="min-w-0 flex-1">
                    <span class="block font-bold text-xs leading-tight truncate text-white">+ Classical Qarabadeen</span>
                    <span class="text-[9px] font-normal text-white/80 block truncate">NFUM Pharmacopoeia</span>
                  </div>
                </button>

                <button onclick="openSelfNuskhaModal()" class="p-2.5 bg-purple-700/90 hover:bg-purple-600 text-white rounded-xl font-bold text-xs shadow-sm transition flex items-center gap-2.5 text-left w-full min-w-0 overflow-hidden active:scale-[0.98]">
                  <span class="w-8 h-8 rounded-lg bg-black/20 flex items-center justify-center text-sm shrink-0">🧪</span>
                  <div class="min-w-0 flex-1">
                    <span class="block font-bold text-xs leading-tight truncate text-white">+ Self-Nuskha Compound</span>
                    <span class="text-[9px] font-normal text-white/80 block truncate">Bespoke Matab Track 1</span>
                  </div>
                </button>

                <button onclick="openZayvoraProductsModal()" class="p-2.5 bg-amber-700/90 hover:bg-amber-600 text-white rounded-xl font-bold text-xs shadow-sm transition flex items-center gap-2.5 text-left w-full min-w-0 overflow-hidden active:scale-[0.98]">
                  <span class="w-8 h-8 rounded-lg bg-black/20 flex items-center justify-center text-sm shrink-0">🌿</span>
                  <div class="min-w-0 flex-1">
                    <span class="block font-bold text-xs leading-tight truncate text-white">+ ZAYVORA Products</span>
                    <span class="text-[9px] font-normal text-white/80 block truncate">32 Master SKUs (5 Launch)</span>
                  </div>
                </button>

                <button onclick="openComputationalIntelligenceModal()" class="p-2.5 bg-indigo-700/90 hover:bg-indigo-600 text-white rounded-xl font-bold text-xs shadow-sm transition flex items-center gap-2.5 text-left w-full min-w-0 overflow-hidden active:scale-[0.98]">
                  <span class="w-8 h-8 rounded-lg bg-black/20 flex items-center justify-center text-sm shrink-0">🧬</span>
                  <div class="min-w-0 flex-1">
                    <span class="block font-bold text-xs leading-tight truncate text-white">Computational Twin™</span>
                    <span class="text-[9px] font-normal text-white/80 block truncate">Molecular &amp; Evidence</span>
                  </div>
                </button>

                <button onclick="openCyp450ScreenerModal()" class="p-2.5 bg-cyan-700/90 hover:bg-cyan-600 text-white rounded-xl font-bold text-xs shadow-sm transition flex items-center gap-2.5 text-left w-full min-w-0 overflow-hidden active:scale-[0.98]">
                  <span class="w-8 h-8 rounded-lg bg-black/20 flex items-center justify-center text-sm shrink-0">🔬</span>
                  <div class="min-w-0 flex-1">
                    <span class="block font-bold text-xs leading-tight truncate text-white">CYP450 Safety Screen</span>
                    <span class="text-[9px] font-normal text-white/80 block truncate">Herb-Drug Interactions</span>
                  </div>
                </button>

                <button onclick="openQsuraDispatchModal()" class="p-2.5 bg-teal-700/90 hover:bg-teal-600 text-white rounded-xl font-bold text-xs shadow-sm transition flex items-center gap-2.5 text-left w-full min-w-0 overflow-hidden active:scale-[0.98]">
                  <span class="w-8 h-8 rounded-lg bg-black/20 flex items-center justify-center text-sm shrink-0">📱</span>
                  <div class="min-w-0 flex-1">
                    <span class="block font-bold text-xs leading-tight truncate text-white">Dispatch Center</span>
                    <span class="text-[9px] font-normal text-white/80 block truncate">WhatsApp / SMS / PDF</span>
                  </div>
                </button>
              </div>"""

    new_formulation_bar = """              <!-- Primary Prescribing Formulation Actions (What the Doctor Prescribes) -->
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5 pt-1">
                <button onclick="openQarabadeenCatalogModal()" class="p-3 bg-emerald-700 hover:bg-emerald-600 text-white rounded-xl font-bold text-xs shadow-sm transition flex items-center gap-3 text-left w-full active:scale-[0.98]">
                  <span class="w-9 h-9 rounded-xl bg-black/20 flex items-center justify-center text-base shrink-0">🏛️</span>
                  <div class="min-w-0 flex-1">
                    <span class="block font-bold text-xs leading-tight truncate text-white">+ Classical Qarabadeen</span>
                    <span class="text-[10px] font-normal text-white/80 block truncate">NFUM Pharmacopoeia Murakkabat</span>
                  </div>
                </button>

                <button onclick="openZayvoraProductsModal()" class="p-3 bg-amber-700 hover:bg-amber-600 text-white rounded-xl font-bold text-xs shadow-sm transition flex items-center gap-3 text-left w-full active:scale-[0.98]">
                  <span class="w-9 h-9 rounded-xl bg-black/20 flex items-center justify-center text-base shrink-0">🌿</span>
                  <div class="min-w-0 flex-1">
                    <span class="block font-bold text-xs leading-tight truncate text-white">+ ZAYVORA Products</span>
                    <span class="text-[10px] font-normal text-white/80 block truncate">32 Standardized Sovereign SKUs</span>
                  </div>
                </button>

                <button onclick="openSelfNuskhaModal()" class="p-3 bg-purple-700 hover:bg-purple-600 text-white rounded-xl font-bold text-xs shadow-sm transition flex items-center gap-3 text-left w-full active:scale-[0.98]">
                  <span class="w-9 h-9 rounded-xl bg-black/20 flex items-center justify-center text-base shrink-0">🧪</span>
                  <div class="min-w-0 flex-1">
                    <span class="block font-bold text-xs leading-tight truncate text-white">+ Custom / Self-Nuskha</span>
                    <span class="text-[10px] font-normal text-white/80 block truncate">Bespoke Matab Compounding</span>
                  </div>
                </button>

                <button onclick="openQsuraDispatchModal()" class="p-3 bg-teal-700 hover:bg-teal-600 text-white rounded-xl font-bold text-xs shadow-sm transition flex items-center gap-3 text-left w-full active:scale-[0.98]">
                  <span class="w-9 h-9 rounded-xl bg-black/20 flex items-center justify-center text-base shrink-0">📱</span>
                  <div class="min-w-0 flex-1">
                    <span class="block font-bold text-xs leading-tight truncate text-white">Dispatch Prescription</span>
                    <span class="text-[10px] font-normal text-white/80 block truncate">WhatsApp / SMS / PDF Slip</span>
                  </div>
                </button>
              </div>

              <!-- Secondary Research & Safety Screener Utilities (Quiet Background Controls) -->
              <div class="pt-2 border-t border-slate-700/60 flex items-center justify-between text-xs">
                <span class="text-[10px] text-slate-400 font-medium flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  Background Safety Gates: Active
                </span>
                <div class="flex items-center gap-2">
                  <button onclick="openComputationalIntelligenceModal()" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 border border-indigo-500/30 text-indigo-300 rounded-lg text-[10px] font-bold transition flex items-center gap-1.5" title="Inspect Computational Evidence & Molecular Profile">
                    <span>🧬</span> <span>Computational Twin™</span>
                  </button>
                  <button onclick="openCyp450ScreenerModal()" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 border border-cyan-500/30 text-cyan-300 rounded-lg text-[10px] font-bold transition flex items-center gap-1.5" title="Inspect CYP450 Herb-Drug Interactions">
                    <span>🔬</span> <span>CYP450 Safety Screen</span>
                  </button>
                </div>
              </div>"""

    if old_formulation_bar in js:
        js = js.replace(old_formulation_bar, new_formulation_bar, 1)
        print("✓ Successfully organized Prescription Formulation Bar into primary clinical actions and background utilities")
    else:
        print("! Warning: Could not locate exact old_formulation_bar in js/zayvora-core.js")

    with open(CORE_JS, "w", encoding="utf-8") as f:
        f.write(js)
    print("Done decluttering consultation suite.")

if __name__ == "__main__":
    declutter_consultation()
