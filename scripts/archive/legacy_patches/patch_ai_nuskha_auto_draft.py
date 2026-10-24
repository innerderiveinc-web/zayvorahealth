#!/usr/bin/env python3
"""
ZAYVORA Health OS — Automated AI Nuskha Drafting & Clinician Review Gate
Ensures that when a patient diagnosis is made:
1. Hakeem Sahab™ AI automatically formulates the complete Nuskha proposal (Dawaat, Posology, Badraqa, and Parhez).
2. The prescription is marked as a DRAFT proposal under clinical supervision.
3. The clinician (doctor) analyzes, modifies, and holds the sole exclusive authority to finalize/sign it.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_JS = os.path.join(BASE_DIR, "js", "zayvora-core.js")
MODULE_JS = os.path.join(BASE_DIR, "js", "modules", "02-clinical-workspace.js")

def patch_core(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Not found: {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Clean up any leftover fee badge
    content = content.replace(
        '<span id="fast-fee-status-badge" class="text-emerald-400 font-mono text-[10px] font-semibold">✓ Settled: ₹200</span>\n              </div>\n            </div>',
        '</div>'
    )
    content = content.replace(
        '<span id="fast-fee-status-badge" class="text-emerald-400 font-mono text-[10px] font-semibold">✓ Settled: ₹200</span>',
        ''
    )

    # 2. Add Auto-Draft button next to fast-diagnosis-input
    old_diag_box = """              <div class="pt-1">
                <input id="fast-diagnosis-input" type="text" class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-emerald-500 font-semibold" value="Waja-ul-Mafasil (Bilateral Knee Osteoarthritis / وجع المفاصل بلغمی)">
              </div>"""

    new_diag_box = """              <div class="pt-1 flex gap-2">
                <input id="fast-diagnosis-input" type="text" onchange="generateAiNuskhaFromDiagnosis(this.value)" class="flex-1 px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-emerald-500 font-semibold" value="Waja-ul-Mafasil (Bilateral Knee Osteoarthritis / وجع المفاصل بلغمی)">
                <button type="button" onclick="generateAiNuskhaFromDiagnosis(document.getElementById('fast-diagnosis-input').value)" class="px-3 py-2 rounded-xl bg-purple-700 hover:bg-purple-600 text-white font-bold text-xs shadow flex items-center gap-1.5 shrink-0 transition cursor-pointer" title="Hakeem AI drafts complete Nuskha for clinician review">
                  <span>🧠</span> Auto-Draft Nuskha
                </button>
              </div>"""

    if old_diag_box in content:
        content = content.replace(old_diag_box, new_diag_box)
        print(f"[✓] {os.path.basename(filepath)}: Injected Auto-Draft button beside diagnosis input")
    else:
        print(f"[!] {os.path.basename(filepath)}: Old diag box not found, trying regex")
        content = re.sub(
            r'<div class="pt-1">\s*<input id="fast-diagnosis-input"[^>]*>\s*</div>',
            new_diag_box,
            content
        )

    # 3. Add AI Proposed Clinician Review Banner above Active Nuskha Table
    old_rx_header = """            <!-- Active Prescribed Formulations List -->
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-sm space-y-3">"""

    new_rx_header = """            <!-- AI PROPOSED CLINICIAN REVIEW BANNER -->
            <div id="ai-nuskha-proposal-banner" class="p-3 bg-gradient-to-r from-purple-950/80 via-slate-900 to-indigo-950/80 border border-purple-500/40 rounded-2xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 text-xs shadow-sm">
              <div class="flex items-center gap-2.5">
                <span class="w-7 h-7 rounded-lg bg-purple-500/20 text-purple-300 border border-purple-500/30 flex items-center justify-center font-bold text-xs shrink-0">🧠</span>
                <div>
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="font-bold text-white text-xs">Hakeem Sahab™ AI Proposes Nuskha (تجویز کردہ نسخہ)</span>
                    <span class="px-2 py-0.2 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 text-[9px] font-mono font-bold">DRAFT PROPOSAL</span>
                  </div>
                  <span class="text-[10px] text-purple-200 block mt-0.5">AI suggests. Clinician decides. Doctor analyzes &amp; holds sole finalization authority.</span>
                </div>
              </div>
              <div class="text-[10px] text-amber-300 font-bold bg-amber-500/10 border border-amber-500/30 px-2.5 py-1 rounded-lg flex items-center gap-1 shrink-0">
                <span>🛡️</span> Clinician Review &amp; Approval Gate
              </div>
            </div>

            <!-- Active Prescribed Formulations List -->
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-sm space-y-3">"""

    if "id=\"ai-nuskha-proposal-banner\"" not in content:
        if old_rx_header in content:
            content = content.replace(old_rx_header, new_rx_header)
            print(f"[✓] {os.path.basename(filepath)}: Injected AI proposal review banner")
        else:
            print(f"[!] {os.path.basename(filepath)}: Old rx header not matched")

    # 4. Update selectFastComplaint to auto-call generateAiNuskhaFromDiagnosis
    old_select_fast = """  function selectFastComplaint(complaintName, defaultDiag) {
    activeFastComplaint = complaintName;
    const diagInput = document.getElementById('fast-diagnosis-input');
    if (diagInput) diagInput.value = defaultDiag;
    
    // Update active chip UI
    document.querySelectorAll('.fast-complaint-chip').forEach(el => {
      if (el.dataset.complaint === complaintName) {
        el.className = "fast-complaint-chip px-3 py-1.5 rounded-xl bg-emerald-600 text-white font-bold text-xs shadow transition";
      } else {
        el.className = "fast-complaint-chip px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 hover:text-white font-medium text-xs transition";
      }
    });

    calculateIlajBilZidd();
    autoSaveConsultationDraft();
  }"""

    new_select_fast = """  function selectFastComplaint(complaintName, defaultDiag) {
    activeFastComplaint = complaintName;
    const diagInput = document.getElementById('fast-diagnosis-input');
    if (diagInput) diagInput.value = defaultDiag;
    
    // Update active chip UI
    document.querySelectorAll('.fast-complaint-chip').forEach(el => {
      if (el.dataset.complaint === complaintName) {
        el.className = "fast-complaint-chip px-3 py-1.5 rounded-xl bg-emerald-600 text-white font-bold text-xs shadow transition";
      } else {
        el.className = "fast-complaint-chip px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 hover:text-white font-medium text-xs transition";
      }
    });

    // Automatically trigger Hakeem Sahab™ AI Nuskha drafting based on diagnosis
    generateAiNuskhaFromDiagnosis(defaultDiag || complaintName);

    calculateIlajBilZidd();
    autoSaveConsultationDraft();
  }

  function generateAiNuskhaFromDiagnosis(diagText) {
    if (!diagText) {
      const diagInput = document.getElementById('fast-diagnosis-input');
      diagText = diagInput ? diagInput.value : '';
    }
    const txt = (diagText || '').toLowerCase();
    let protocolId = 'arthri'; // Default fallback

    if (txt.includes('waja') || txt.includes('joint') || txt.includes('knee') || txt.includes('osteo') || txt.includes('mafasil') || txt.includes('dard')) {
      protocolId = 'arthri';
    } else if (txt.includes('hazm') || txt.includes('gas') || txt.includes('dyspep') || txt.includes('pet') || txt.includes('kamuni') || txt.includes('stomach') || txt.includes('acid')) {
      protocolId = 'gastro';
    } else if (txt.includes('suda') || txt.includes('migraine') || txt.includes('head') || txt.includes('sir') || txt.includes('shaqeeqa') || txt.includes('tensio')) {
      protocolId = 'ceph';
    } else if (txt.includes('sugar') || txt.includes('diabet') || txt.includes('ziabetus') || txt.includes('gluco') || txt.includes('metabol')) {
      protocolId = 'metabolic';
    } else if (txt.includes('bah') || txt.includes('vitality') || txt.includes('asab') || txt.includes('neuro') || txt.includes('weak') || txt.includes('mardana')) {
      protocolId = 'vitality';
    } else if (txt.includes('nazla') || txt.includes('cold') || txt.includes('cough') || txt.includes('khansi') || txt.includes('sadr') || txt.includes('respir') || txt.includes('banafsha')) {
      protocolId = 'respiratory';
    } else if (txt.includes('jigar') || txt.includes('liver') || txt.includes('kabid') || txt.includes('kasni') || txt.includes('mako') || txt.includes('jaundice')) {
      protocolId = 'liver';
    } else if (txt.includes('skin') || txt.includes('jild') || txt.includes('khujli') || txt.includes('rash') || txt.includes('ushba') || txt.includes('detox')) {
      protocolId = 'skin';
    }

    applyFastProtocol(protocolId);

    // Update banner visibility and status
    const banner = document.getElementById('ai-nuskha-proposal-banner');
    if (banner) {
      banner.classList.remove('hidden');
    }
    
    if (typeof showNotification === 'function') {
      showNotification('✨ Hakeem Sahab™ AI proposed formulation based on diagnosis. Clinician review required before finalizing.', 'info');
    }
  }

  window.generateAiNuskhaFromDiagnosis = generateAiNuskhaFromDiagnosis;"""

    if old_select_fast in content:
        content = content.replace(old_select_fast, new_select_fast)
        print(f"[✓] {os.path.basename(filepath)}: Updated selectFastComplaint and injected generateAiNuskhaFromDiagnosis")
    else:
        print(f"[!] {os.path.basename(filepath)}: Old selectFastComplaint not found exact")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True

if __name__ == "__main__":
    print("=" * 70)
    print(" ZAYVORA Health OS — Patch AI Nuskha Auto-Drafting Engine")
    print("=" * 70)
    patch_core(CORE_JS)
    patch_core(MODULE_JS)
    print("=" * 70)
