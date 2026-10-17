#!/usr/bin/env python3
"""
ZAYVORA Health OS — Consultation Desk Declutter & Simplification Engine
Streamlines the consultation experience into an elegant, doctor-first workspace:
1. Replaces cluttered header with clean patient summary (MRN, Mizaj, Allergies, Attending Doctor).
2. Removes redundant 'Change Mareez' dropdown from the active consultation header.
3. Replaces 8 giant colored protocol cards with a sleek, compact, 1-row pill selector.
4. Adds clean Hakeem Sahab™ CDSS advisory integration.
5. Removes irrelevant cash fee buttons from the clinical prescription pad.
6. Consolidates action buttons (Print Slip, WhatsApp Rx, Follow-up Reminder, Sign & Lock).
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_JS = os.path.join(BASE_DIR, "js", "zayvora-core.js")
MODULE_JS = os.path.join(BASE_DIR, "js", "modules", "02-clinical-workspace.js")

def declutter_file(filepath):
    if not os.path.exists(filepath):
        print(f"[-] File not found: {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Header declutter
    old_header_pattern = re.compile(
        r'<!-- FAST MATAB WORKSPACE HEADER -->\s*<div class="bg-\[var\(--card\)\] border border-\[var\(--border\)\] rounded-2xl p-5 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">[\s\S]*?<!-- 2-COLUMN FAST MATAB WORKDESK -->',
        re.MULTILINE
    )

    new_header = """<!-- FAST MATAB WORKSPACE HEADER -->
        <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div class="flex items-center gap-2 flex-wrap">
              <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold border border-emerald-500/40 flex items-center gap-1.5">
                <span>🩺</span> Consultation Desk
              </span>
              <span class="text-xs font-mono text-[var(--muted)] px-2 py-0.5 rounded bg-[var(--background)] border border-[var(--border)]">${state.encounterId}</span>
              <h2 class="text-lg font-bold text-white">${state.patient.name} (${state.patient.age}y, ${state.patient.gender})</h2>
              <span class="text-[10px] font-mono text-emerald-400 px-2 py-0.5 rounded bg-[var(--background)] border border-[var(--border)]">MRN: ${state.patient.mrn}</span>
            </div>
            <div class="flex items-center gap-2 mt-1.5 flex-wrap text-xs text-[var(--muted)]">
              <span>Baseline Mizaj: <strong id="fast-patient-mizaj-display" class="text-emerald-400 font-semibold">${state.patient.mizaj}</strong></span>
              <span>•</span>
              <span>Allergies: <strong class="text-rose-400 font-medium">${state.patient.allergies || 'None reported'}</strong></span>
              <span>•</span>
              <span>Physician: <strong class="text-slate-200">Hakeem Dr. Irfan Ashraf</strong></span>
            </div>
          </div>
          
          <!-- Mode Switcher & Top Action Buttons -->
          <div class="flex items-center gap-2 flex-wrap">
            <div class="flex items-center bg-slate-900 border border-slate-700 rounded-xl p-1">
              <button onclick="setConsultationMode('fast')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition bg-emerald-600 text-white shadow">
                ⚡ Simple Desk
              </button>
              <button onclick="setConsultationMode('continuum')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-400 hover:text-white" title="Switch to Full 13-Step Clinical Continuum">
                🔬 13-Step Detailed
              </button>
            </div>
            
            <button onclick="openBilingualPrescriptionSlipModal()" class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white font-bold text-xs shadow-sm transition flex items-center gap-1.5">
              <span>🖨️</span> Patient Slip
            </button>
            <button onclick="completeConsultation()" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md transition flex items-center gap-1.5">
              <span>🔒</span> Sign &amp; Lock (21 CFR 11)
            </button>
          </div>
        </div>

        <!-- 2-COLUMN FAST MATAB WORKDESK -->"""

    if old_header_pattern.search(content):
        content = old_header_pattern.sub(new_header, content)
        print(f"[✓] {os.path.basename(filepath)}: Decluttered header successfully")
    else:
        print(f"[!] {os.path.basename(filepath)}: Old header pattern not found, trying partial")

    # 2. Protocols bar declutter (replace 8 giant colored buttons with compact clean bar)
    old_proto_pattern = re.compile(
        r'<!-- 1-Click Classical Protocols Bar -->\s*<div class="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-slate-700 rounded-2xl p-4 shadow-sm space-y-2\.5">[\s\S]*?</div>\s*</div>\s*<!-- DYNAMIC "ILAJ BIL-ZIDD"',
        re.MULTILINE
    )

    new_proto = """<!-- 1-Click Classical Protocols Bar (Compact & Clean) -->
            <div class="bg-[var(--card)] border border-purple-500/30 rounded-2xl p-3.5 shadow-sm space-y-2.5">
              <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-lg bg-purple-500/20 text-purple-300 flex items-center justify-center font-bold text-xs">🧠</span>
                  <span class="font-bold text-white text-xs">Hakeem Sahab™ Clinical CDSS &bull; Master Protocols</span>
                </div>
                <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30 font-semibold">1-Click Auto-Fill</span>
              </div>
              
              <div class="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar text-xs">
                <button onclick="applyFastProtocol('arthri')" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-emerald-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700 transition" title="Suranjan + SynovoFlex (وجع المفاصل)">🦵 ArthriCare</button>
                <button onclick="applyFastProtocol('gastro')" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-teal-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700 transition" title="Kamuni + Bazoori (سوء ہضم)">🧪 GastroBalance</button>
                <button onclick="applyFastProtocol('ceph')" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-purple-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700 transition" title="Itrifal + TensioCalm (صداع مزمن)">🧠 Cephalic</button>
                <button onclick="applyFastProtocol('metabolic')" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-amber-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700 transition" title="Khabsul Hadeed + Glucovora (ذیابیطس)">🍯 Metabolic</button>
                <button onclick="applyFastProtocol('respiratory')" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-blue-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700 transition" title="Banafsha + Sapistan (نزلہ و سعال)">🫁 Respiratory</button>
                <button onclick="applyFastProtocol('liver')" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-cyan-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700 transition" title="Kasni + Arq Mako (کبد و استسقاء)">🩺 Hepato</button>
                <button onclick="applyFastProtocol('vitality')" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-indigo-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700 transition" title="Arad Khurma + Jadwar (ضعف باہ)">⚡ Vitality</button>
                <button onclick="applyFastProtocol('skin')" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-rose-800 hover:text-white text-slate-300 font-medium whitespace-nowrap border border-slate-700 transition" title="Majun Ushba + Unnab (مصفی خون)">🌿 Skin Detox</button>
              </div>
            </div>

            <!-- DYNAMIC "ILAJ BIL-ZIDD" """

    if old_proto_pattern.search(content):
        content = old_proto_pattern.sub(new_proto, content)
        print(f"[✓] {os.path.basename(filepath)}: Compacted protocols bar successfully")
    else:
        print(f"[!] {os.path.basename(filepath)}: Old protocols bar pattern not found")

    # 3. Remove fee settlement bar
    old_fee_pattern = re.compile(
        r'<!-- Matab Consultation Fee Settler \(Discreet Bar\) -->\s*<div class="p-2 bg-slate-950/60 rounded-xl border border-slate-800/80 flex items-center justify-between text-xs">[\s\S]*?</div>',
        re.MULTILINE
    )
    if old_fee_pattern.search(content):
        content = old_fee_pattern.sub('', content)
        print(f"[✓] {os.path.basename(filepath)}: Removed cash fee buttons from prescription pad")

    # 4. Consolidate bottom actions bar
    old_bottom_pattern = re.compile(
        r'<!-- Bottom Master Actions Bar -->\s*<div class="p-4 bg-slate-900 rounded-2xl border border-slate-800 flex flex-col sm:flex-row justify-between items-center gap-3">[\s\S]*?</div>\s*</div>\s*</div>\s*</div>\s*`;\s*// Initialize list and balance indicator',
        re.MULTILINE
    )

    new_bottom = """<!-- Bottom Master Actions Bar -->
            <div class="p-4 bg-slate-900 rounded-2xl border border-slate-800 flex flex-col sm:flex-row justify-between items-center gap-3">
              <div class="text-[11px] text-slate-400">
                <span class="text-emerald-400 font-bold">✓ Ready for Dispense:</span> 21 CFR Part 11 Validated Prescription
              </div>
              <div class="flex items-center gap-2 w-full sm:w-auto flex-wrap">
                <button onclick="openBilingualPrescriptionSlipModal()" class="flex-1 sm:flex-none px-3.5 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white rounded-xl font-bold text-xs shadow-sm transition flex items-center justify-center gap-1.5">
                  <span>🖨️</span> Print Slip (Urdu/Eng)
                </button>
                <button onclick="sendRxViaWhatsApp()" class="flex-1 sm:flex-none px-3.5 py-2.5 bg-emerald-700 hover:bg-emerald-600 text-white rounded-xl font-bold text-xs shadow-sm transition flex items-center justify-center gap-1.5">
                  <span>📲</span> WhatsApp Rx
                </button>
                <button onclick="sendFollowupReminderViaWhatsApp()" class="flex-1 sm:flex-none px-3.5 py-2.5 bg-blue-700 hover:bg-blue-600 text-white rounded-xl font-bold text-xs shadow-sm transition flex items-center justify-center gap-1.5" title="Send 14-day follow-up appointment reminder via WhatsApp">
                  <span>📅</span> Reminder
                </button>
                <button onclick="completeConsultation()" class="flex-1 sm:flex-none px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-bold text-xs shadow-md transition flex items-center justify-center gap-1.5">
                  <span>🔒</span> Sign &amp; Lock (21 CFR 11)
                </button>
              </div>
            </div>

          </div>

        </div>

      </div>
    `;

    // Initialize list and balance indicator"""

    if old_bottom_pattern.search(content):
        content = old_bottom_pattern.sub(new_bottom, content)
        print(f"[✓] {os.path.basename(filepath)}: Upgraded bottom actions bar successfully")
    else:
        print(f"[!] {os.path.basename(filepath)}: Old bottom bar pattern not found")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True

if __name__ == "__main__":
    print("=" * 70)
    print(" ZAYVORA Health OS — Declutter Consultation Desk")
    print("=" * 70)
    declutter_file(CORE_JS)
    declutter_file(MODULE_JS)
    print("=" * 70)
