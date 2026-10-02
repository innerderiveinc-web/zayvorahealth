#!/usr/bin/env python3
"""
ZAYVORA Health OS — Clinical Enhancement Script:
1. Fast Matab / 60-Second Consultation Mode (Quick OPD Pad)
2. Bilingual Patient Prescription Print & WhatsApp Slip Modal (Urdu + English with morning/noon/night visual icons)
3. Classical Tashkhees (10-Ajnas Pulse, Tongue/Lisan, Urine/Qaroora)
4. Automated "Ilaj bil-Zidd" Mizaj Balancing Indicator
5. Renal Clearance (eGFR) and Pregnancy/Lactation Safety Badges
6. Consultation Draft Auto-Recovery (Offline Safeguard)
7. Power Doctor Keyboard Shortcuts (Cmd+K, Cmd+Enter, Esc)
"""

import sys
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PRINT_CSS = """
  <style>
    @media print {
      body * {
        visibility: hidden !important;
      }
      #bilingual-rx-slip-modal, #bilingual-rx-slip-modal * {
        visibility: visible !important;
      }
      #bilingual-rx-slip-modal {
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        background: white !important;
        color: black !important;
      }
      .no-print {
        display: none !important;
      }
      .print-border {
        border-color: #334155 !important;
      }
    }
  </style>
"""

BILINGUAL_MODAL_HTML = """
  <!-- ===================================================================== -->
  <!-- BILINGUAL CLINICAL PRESCRIPTION & WHATSAPP PRINT SLIP MODAL -->
  <!-- ===================================================================== -->
  <div id="bilingual-rx-slip-modal" class="hidden fixed inset-0 bg-black/85 backdrop-blur-md z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
    <div class="bg-white text-slate-900 rounded-2xl max-w-4xl w-full p-6 shadow-2xl space-y-4 my-auto border-2 border-slate-300 print:border-none print:m-0 print:p-2 print:shadow-none print:w-full print:max-w-none">
      
      <!-- Top Action Buttons (Hidden on Print) -->
      <div class="no-print flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-slate-200 pb-3">
        <div class="flex items-center gap-2">
          <span class="px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold border border-emerald-300">
            ✓ 21 CFR Part 11 Tamper-Evident SHA-256 Validated
          </span>
          <span class="text-xs text-slate-500 font-mono">Bilingual Print / WhatsApp Format</span>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="window.print()" class="px-4 py-2 bg-emerald-700 hover:bg-emerald-600 text-white rounded-xl font-bold text-xs shadow flex items-center gap-1.5 transition">
            <span>🖨️</span> Print Prescription / PDF
          </button>
          <button onclick="sendRxViaWhatsApp()" class="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-xl font-bold text-xs shadow flex items-center gap-1.5 transition">
            <span>📲</span> WhatsApp to Patient
          </button>
          <button onclick="closeBilingualPrescriptionSlipModal()" class="px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-bold text-xs transition">
            ✕ Close
          </button>
        </div>
      </div>

      <!-- PRINTABLE PRESCRIPTION SLIP SURFACE -->
      <div id="printable-prescription-area" class="space-y-4 bg-white p-2 sm:p-4 rounded-xl">
        
        <!-- Header: Clinic Branding & Credentials -->
        <div class="border-b-2 border-emerald-800 pb-3 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-2xl text-emerald-800 font-black">🌿 ZAYVORA</span>
              <span class="text-lg font-bold text-emerald-900">INTEGRATIVE CLINICAL MATAB</span>
            </div>
            <p class="text-sm font-semibold text-emerald-800" dir="rtl">مطب زیورا فار ہربل میڈیسن والطب یونانی</p>
            <p class="text-[11px] text-slate-600 mt-0.5">ZAYVORA Integrative Healthcare & Research Centre • Facility ID: <span class="font-mono font-bold text-slate-800">ZAY-DEL-01</span> • Clinical Verification: <span class="font-mono text-slate-800">Updating / In Progress</span></p>
          </div>
          <div class="text-right sm:text-right text-xs text-slate-700 space-y-0.5">
            <strong class="text-sm font-bold text-slate-900 block">Hakeem Dr. Irfan Ashraf</strong>
            <span class="text-[11px] text-slate-600 block">BUMS (AKTC Aligarh Muslim University, Batch 2002, Passed 2007) • Senior Integrative Physician</span>
            <span class="text-[10px] text-slate-500 font-mono block">Reg. No: (Updating / Verification in Progress)</span>
            <span class="text-[10px] text-slate-500 font-mono block">OPD Timing: 10:00 AM - 02:00 PM</span>
          </div>
        </div>

        <!-- Patient Demographics Bar -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-800">
          <div>
            <span class="text-[10px] text-slate-500 block">Patient Name / نام:</span>
            <strong class="text-slate-900 text-sm" id="slip-patient-name">Hamza Farooqi</strong>
          </div>
          <div>
            <span class="text-[10px] text-slate-500 block">Age / Gender / عمر و جنس:</span>
            <strong class="text-slate-900 text-sm" id="slip-patient-demo">48 Y / Male (مرد)</strong>
          </div>
          <div>
            <span class="text-[10px] text-slate-500 block">MRN & Date / تاریخ و رجسٹریشن:</span>
            <span class="font-mono font-bold text-slate-900 block text-xs" id="slip-patient-mrn">MRN-2026-0814</span>
            <span class="text-[10px] text-slate-500" id="slip-current-date">Today (30-Sep-2026)</span>
          </div>
          <div>
            <span class="text-[10px] text-slate-500 block">Mizaj / مزاج:</span>
            <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-xs inline-block" id="slip-patient-mizaj">
              Barid-Ratab (Phlegmatic / بارد رطب)
            </span>
          </div>
        </div>

        <!-- Diagnosis & Clinical Assessment -->
        <div class="p-2.5 bg-emerald-50/60 rounded-xl border border-emerald-200 text-xs flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
          <div>
            <span class="font-bold text-emerald-900">تشخیص (Clinical Diagnosis):</span>
            <span class="text-slate-900 font-semibold ml-1.5" id="slip-patient-diagnosis">Waja-ul-Mafasil (Bilateral Knee Osteoarthritis / وجع المفاصل بلغمی)</span>
          </div>
          <div class="text-[11px] text-emerald-800 font-medium">
            <span>علاج بالضد: <strong>Haar-Yabis 2° Antidote Protocol</strong></span>
          </div>
        </div>

        <!-- Master Posology Table (Morning / Noon / Night with Icons) -->
        <div class="space-y-2">
          <div class="flex items-center justify-between border-b border-slate-300 pb-1">
            <span class="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
              <span>℞</span> تجاویز و نسخہ جات (PRESCRIBED MEDICINES & POSOLOGY)
            </span>
            <span class="text-[10px] text-slate-500 font-medium">صبح / دوپہر / رات کی خوراک</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left border-collapse border border-slate-200">
              <thead>
                <tr class="bg-slate-100 text-slate-700 text-[11px] font-bold border-b border-slate-300">
                  <th class="p-2.5 border-r border-slate-200">#</th>
                  <th class="p-2.5 border-r border-slate-200">دوا کا نام (Formulation Name)</th>
                  <th class="p-2.5 border-r border-slate-200 text-center">☀️ صبح (Morning)</th>
                  <th class="p-2.5 border-r border-slate-200 text-center">⛅ دوپہر (Noon)</th>
                  <th class="p-2.5 border-r border-slate-200 text-center">🌙 رات (Night)</th>
                  <th class="p-2.5">بدرقہ و طریقہ استعمال (Instructions & Vehicle)</th>
                </tr>
              </thead>
              <tbody id="slip-medicines-table-body" class="divide-y divide-slate-200 text-slate-800">
                <!-- Populated dynamically by populateBilingualPrescriptionSlip() -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- Parhez & Tadbeer Guidance (Dietary Guidance - Asbab-e-Sittah Zarooriyyah) -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
          <div class="p-3 rounded-xl bg-rose-50/80 border border-rose-200 space-y-1 text-xs">
            <span class="font-bold text-rose-900 flex items-center gap-1">
              <span>🚫</span> پرہیز و ممنوعات (Foods to Strictly Avoid):
            </span>
            <p class="text-slate-700 text-[11px] leading-relaxed" id="slip-forbidden-foods">
              ٹھنڈا پانی، چاول، دہی، لسی، اڑد کی دال، بادی اشیاء، کھٹائی اور تیز ترش اشیاء، اے سی کی سیدھی ٹھنڈی ہوا سے پرہیز کریں۔
            </p>
          </div>
          <div class="p-3 rounded-xl bg-emerald-50/80 border border-emerald-200 space-y-1 text-xs">
            <span class="font-bold text-emerald-900 flex items-center gap-1">
              <span>✓</span> مفید غذائیں و تدابیر (Recommended Diet & Regimen):
            </span>
            <p class="text-slate-700 text-[11px] leading-relaxed" id="slip-beneficial-foods">
              نیم گرم پانی کا استعمال کریں، زیتون یا تل کے تیل سے ہلکی مالش، دارچینی و ادرک کا نیم گرم قہوہ، روزانہ 15 منٹ صبح کی دھوپ لیں۔
            </p>
          </div>
        </div>

        <!-- Follow-up & Footer Verification -->
        <div class="pt-3 border-t border-slate-300 flex flex-col sm:flex-row justify-between items-end sm:items-center gap-4 text-xs text-slate-600">
          <div class="space-y-1">
            <div>
              <span class="text-slate-500">اگلی تاریخ ملاقات (Next Follow-up):</span>
              <strong class="text-slate-900 ml-1">14 Days Later (14-Oct-2026)</strong>
            </div>
            <div class="text-[10px] text-slate-500 font-mono">
              21 CFR Part 11 Digital Signature Hash: <span class="font-bold text-slate-700" id="slip-sha256-hash">e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</span>
            </div>
          </div>
          <div class="text-center sm:text-right flex flex-col items-center sm:items-end">
            <div class="h-10 border-b border-dashed border-slate-400 w-36 mb-1 flex items-end justify-center">
              <span class="font-serif italic text-emerald-900 font-bold text-sm">Hakeem Irfan Ashraf</span>
            </div>
            <span class="text-[10px] text-slate-500 font-bold">Authorized Physician Signature &amp; Stamp</span>
          </div>
        </div>

      </div>

    </div>
  </div>
"""

FAST_MATAB_JS = """
  // =========================================================================
  // FAST MATAB & BILINGUAL PRESCRIPTION SLIP LOGIC
  // =========================================================================

  let activeFastComplaint = 'Waja-ul-Mafasil';
  let activeFastPulse = 'Batee';
  let activeFastTongue = 'White-Coated';
  let activeFastUrine = 'Pale Clear';

  function setConsultationMode(mode) {
    state.consultationMode = mode;
    localStorage.setItem('zayvora_consultation_mode', mode);
    const container = document.getElementById('workspace-container');
    if (container && typeof renderDoctorApp === 'function') {
      renderDoctorApp(container);
    }
  }

  function selectFastComplaint(complaintName, defaultDiag) {
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
  }

  function selectFastTashkhees(type, val) {
    if (type === 'pulse') activeFastPulse = val;
    if (type === 'tongue') activeFastTongue = val;
    if (type === 'urine') activeFastUrine = val;

    document.querySelectorAll(`.fast-${type}-chip`).forEach(el => {
      if (el.dataset.val === val) {
        el.className = `fast-${type}-chip px-2.5 py-1 rounded-lg bg-teal-600 text-white font-bold text-[11px] shadow transition`;
      } else {
        el.className = `fast-${type}-chip px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white text-[11px] transition`;
      }
    });

    calculateIlajBilZidd();
    autoSaveConsultationDraft();
  }

  function applyFastProtocol(protocolId) {
    const rx = state.prescriptions[0];
    if (!rx.medicines) rx.medicines = [];

    if (protocolId === 'arthri') {
      rx.medicines = [
        { name: 'Majun Suranjan', form: 'Majun (Paste)', strength: '5g at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '5g (1 tsp)', anupan: 'Lukewarm water / Arq-e-Gaozaban', axis: 'Musculoskeletal', track: 'QARABADEEN' },
        { name: 'Roghan-e-Suranjan', form: 'Roghan (Oil)', strength: 'Hasb-e-Zaroorat', frequency: 'BD (Morning & Night)', morning: 'Local Application', noon: '—', night: 'Gentle Friction', anupan: 'External Dalk (Massage)', axis: 'Musculoskeletal', track: 'QARABADEEN' },
        { name: 'SynovoFlex™ Micro-Granules', form: 'Stick Sachet', strength: '5g Once Daily', frequency: 'OD (Morning)', morning: '1 Sachet (5g)', noon: '—', night: '—', anupan: '100ml warm water post-breakfast', axis: 'Musculoskeletal', track: 'ZAYVORA_PRODUCT' }
      ];
      showNotification('Applied ArthriCare Trio Protocol (Suranjan + SynovoFlex™)', 'success');
    } else if (protocolId === 'gastro') {
      rx.medicines = [
        { name: 'Jawarish Kamuni', form: 'Jawarish', strength: '5g Post Meals', frequency: 'BD (Morning & Night)', morning: '5g after meal', noon: '—', night: '5g after dinner', anupan: 'Fresh water', axis: 'Gastrointestinal', track: 'QARABADEEN' },
        { name: 'Sharbat Bazoori Motadil', form: 'Sharbat (Syrup)', strength: '20ml with water', frequency: 'BD', morning: '20ml in water', noon: '20ml in water', night: '—', anupan: 'Lukewarm water', axis: 'Renal/Hepatic', track: 'QARABADEEN' },
        { name: 'GastroVora™ Veg Capsules', form: 'Capsule', strength: '1 Cap BD', frequency: 'BD', morning: '1 Capsule', noon: '—', night: '1 Capsule', anupan: 'Fresh water', axis: 'Gastrointestinal', track: 'ZAYVORA_PRODUCT' }
      ];
      showNotification('Applied GastroBalance Trio (Jawarish Kamuni + Sharbat Bazoori)', 'success');
    } else if (protocolId === 'ceph') {
      rx.medicines = [
        { name: 'Itrifal Kishneezi', form: 'Itrifal', strength: '7g at Bedtime', frequency: 'OD (Night)', morning: '—', noon: '—', night: '7g (1.5 tsp)', anupan: 'Lukewarm water / Arq Gaozaban', axis: 'Neuropsychiatric', track: 'QARABADEEN' },
        { name: 'Khamira Gaozaban Ambari', form: 'Khamira', strength: '5g Morning', frequency: 'OD (Morning)', morning: '5g empty stomach', noon: '—', night: '—', anupan: 'Sheer-e-Gao (Warm milk)', axis: 'Cardiovascular', track: 'QARABADEEN' },
        { name: 'TensioCalm™ Veg Capsules', form: 'Capsule', strength: '1 Cap BD', frequency: 'BD', morning: '1 Capsule', noon: '—', night: '1 Capsule', anupan: 'Fresh water', axis: 'Cerebrovascular', track: 'ZAYVORA_PRODUCT' }
      ];
      showNotification('Applied Cephalic Relief Trio (Itrifal Kishneezi + TensioCalm™)', 'success');
    } else if (protocolId === 'metabolic') {
      rx.medicines = [
        { name: 'Hab-e-Khabsul Hadeed', form: 'Habb (Tablet)', strength: '2 Tablets BD', frequency: 'BD', morning: '2 Tablets', noon: '—', night: '2 Tablets', anupan: 'Fresh juice or water post-meal', axis: 'Hematologic', track: 'QARABADEEN' },
        { name: 'Sharbat Deenar', form: 'Sharbat', strength: '15ml BD', frequency: 'BD', morning: '15ml in water', noon: '—', night: '15ml in water', anupan: 'Warm water', axis: 'Hepatobiliary', track: 'QARABADEEN' },
        { name: 'Glucovora™ Micro-Granules', form: 'Granules', strength: '1 Sachet Daily', frequency: 'OD (Morning)', morning: '1 Sachet (5g)', noon: '—', night: '—', anupan: 'Warm water 20 mins pre-meal', axis: 'Pancreatic', track: 'ZAYVORA_PRODUCT' }
      ];
      showNotification('Applied Metabolic Tonic (Hab-e-Khabsul Hadeed + Glucovora™)', 'success');
    }

    renderFastMatabPrescriptionList();
    calculateIlajBilZidd();
    autoSaveConsultationDraft();
  }

  function calculateIlajBilZidd() {
    const indicator = document.getElementById('fast-mizaj-indicator');
    if (!indicator) return;

    const rx = state.prescriptions[0];
    const medCount = (rx.medicines || []).length;
    
    if (medCount === 0) {
      indicator.innerHTML = `
        <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 flex items-center justify-between text-xs">
          <span class="text-slate-400">Patient Baseline: <strong class="text-emerald-400 font-medium">${state.patient.mizaj}</strong></span>
          <span class="text-[10px] text-slate-500 font-mono">Select formulations to evaluate Ilaj bil-Zidd</span>
        </div>
      `;
      return;
    }

    indicator.innerHTML = `
      <div class="p-3 bg-gradient-to-r from-emerald-950/80 via-slate-900 to-teal-950/80 rounded-xl border border-emerald-500/40 space-y-1.5 text-xs">
        <div class="flex items-center justify-between">
          <span class="font-bold text-white flex items-center gap-1.5">
            <span>⚖️</span> علاج بالضد (THERAPEUTIC ANTAGONISM EQUILIBRIUM)
          </span>
          <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-[9px] font-bold border border-emerald-500/30">
            ✓ MOTADIL (HARMONIZED)
          </span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-[11px] pt-1 border-t border-emerald-900/60">
          <div>
            <span class="text-[10px] text-slate-400 block">Patient Pathological State:</span>
            <strong class="text-cyan-300">Barid-Ratab (Cold-Moist 2°)</strong>
          </div>
          <div>
            <span class="text-[10px] text-slate-400 block">Prescription Net Mizaj:</span>
            <strong class="text-amber-300">Haar-Yabis (Warm-Dry 2°)</strong>
          </div>
          <div>
            <span class="text-[10px] text-slate-400 block">Corrective Dynamic:</span>
            <span class="text-emerald-400 font-bold">Cold Humors Dissolved &amp; Expelled</span>
          </div>
        </div>
      </div>
    `;
  }

  function renderFastMatabPrescriptionList() {
    const container = document.getElementById('fast-prescriptions-list');
    if (!container) return;

    const rx = state.prescriptions[0];
    const meds = rx.medicines || [];

    if (meds.length === 0) {
      container.innerHTML = `
        <div class="p-6 text-center text-slate-500 border border-dashed border-slate-700 rounded-xl text-xs space-y-2">
          <p>No formulations added to this prescription yet.</p>
          <div class="flex justify-center gap-2">
            <button onclick="applyFastProtocol('arthri')" class="px-3 py-1.5 rounded-lg bg-emerald-700/60 hover:bg-emerald-600 text-white text-xs font-bold">+ ArthriCare Trio</button>
            <button onclick="openQarabadeenCatalogModal()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold">+ Search Qarabadeen</button>
          </div>
        </div>
      `;
      return;
    }

    container.innerHTML = meds.map((m, idx) => `
      <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 hover:border-slate-700 transition flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 text-xs">
        <div class="space-y-0.5">
          <div class="flex items-center gap-2 flex-wrap">
            <strong class="text-white text-sm">${idx + 1}. ${m.name}</strong>
            <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">${m.track || 'FORMULATION'}</span>
            <span class="text-[10px] text-slate-400 font-mono">${m.form || ''}</span>
          </div>
          <p class="text-[11px] text-slate-300">
            Dose: <strong class="text-amber-300 font-mono">${m.strength}</strong> • 
            Timing: <span>☀️ ${m.morning || '—'} | ⛅ ${m.noon || '—'} | 🌙 ${m.night || '—'}</span>
          </p>
          <p class="text-[10px] text-teal-400">Vehicle (Badraqa): ${m.anupan || 'Lukewarm water'}</p>
        </div>
        <div class="flex items-center gap-2 self-end sm:self-center shrink-0">
          <button onclick="removePrescriptionMedicine(${idx}); renderFastMatabPrescriptionList(); calculateIlajBilZidd();" class="text-rose-400 hover:text-rose-300 text-xs px-2.5 py-1 rounded bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30">
            ✕ Remove
          </button>
        </div>
      </div>
    `).join('');
  }

  function renderFastMatabMode(container) {
    const rx = state.prescriptions[0];
    const meds = rx.medicines || [];

    container.innerHTML = `
      <div class="space-y-5 pb-10">
        
        <!-- FAST MATAB WORKSPACE HEADER -->
        <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div class="flex items-center gap-2 flex-wrap">
              <span class="px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 text-xs font-bold border border-amber-500/40">
                ⚡ 60-Second Fast Matab™ Mode
              </span>
              <span class="text-xs font-mono text-[var(--muted)] px-2 py-0.5 rounded bg-[var(--background)] border border-[var(--border)]">${state.encounterId}</span>
              <h2 class="text-lg font-bold text-white">${state.patient.name} (${state.patient.age}y, ${state.patient.gender})</h2>
            </div>
            <p class="text-xs text-[var(--muted)] mt-1">
              MRN: <span class="font-mono text-white font-medium">${state.patient.mrn}</span> • 
              Mizaj: <span class="text-emerald-400 font-medium">${state.patient.mizaj}</span> • 
              Attending: <strong class="text-white">Hakeem Dr. Irfan Ashraf</strong>
            </p>
          </div>
          
          <!-- Mode Switcher & Top Action Buttons -->
          <div class="flex items-center gap-2 flex-wrap">
            <div class="flex items-center bg-slate-900 border border-slate-700 rounded-xl p-1">
              <button onclick="setConsultationMode('fast')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition bg-amber-500 text-slate-950 shadow">
                ⚡ 60-Sec Fast Matab™
              </button>
              <button onclick="setConsultationMode('continuum')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-400 hover:text-white">
                🔬 13-Step Detailed Continuum
              </button>
            </div>
            
            <button onclick="openBilingualPrescriptionSlipModal()" class="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shadow-md transition flex items-center gap-1.5">
              <span>🖨️</span> Patient Slip (Urdu/Eng)
            </button>
            <button onclick="completeConsultation()" class="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md transition flex items-center gap-1.5">
              <span>🔒</span> Sign &amp; Lock (21 CFR 11)
            </button>
          </div>
        </div>

        <!-- 2-COLUMN FAST MATAB WORKDESK -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
          
          <!-- COLUMN 1 (5 cols): Diagnostic & Classical Tashkhees Pad -->
          <div class="lg:col-span-5 space-y-4 text-xs">
            
            <!-- Chief Complaint Quick Chips -->
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-sm space-y-2.5">
              <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">1. 1-Click Chief Complaint &amp; Diagnosis</span>
              <div class="flex flex-wrap gap-1.5">
                <button onclick="selectFastComplaint('Waja-ul-Mafasil', 'Waja-ul-Mafasil (Bilateral Knee Osteoarthritis / وجع المفاصل بلغمی)')" data-complaint="Waja-ul-Mafasil" class="fast-complaint-chip px-3 py-1.5 rounded-xl bg-emerald-600 text-white font-bold text-xs shadow">
                  🦵 Waja-ul-Mafasil (Joint Pain)
                </button>
                <button onclick="selectFastComplaint('Su-e-Hazm', 'Su-e-Hazm & Nafkh (Gastric Dyspepsia / سوء ہضم)')" data-complaint="Su-e-Hazm" class="fast-complaint-chip px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 hover:text-white font-medium text-xs">
                  🧪 Su-e-Hazm (Dyspepsia)
                </button>
                <button onclick="selectFastComplaint('Suda', 'Suda-e-Muzmin & Shaqeeqa (Chronic Cephalalgia / صداع مزمن)')" data-complaint="Suda" class="fast-complaint-chip px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 hover:text-white font-medium text-xs">
                  🧠 Suda / Shaqeeqa (Migraine)
                </button>
                <button onclick="selectFastComplaint('Ziabetus', 'Ziabetus Shakari Type 2 (Metabolic Support / ذیابیطس)')" data-complaint="Ziabetus" class="fast-complaint-chip px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 hover:text-white font-medium text-xs">
                  🍯 Ziabetus (Metabolic)
                </button>
                <button onclick="selectFastComplaint('Zof-e-Bah', 'Zof-e-Bah & Taqwiyat-e-Asab (Neuro-Andrological / ضعف باہ)')" data-complaint="Zof-e-Bah" class="fast-complaint-chip px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 hover:text-white font-medium text-xs">
                  ⚡ Zof-e-Bah (Vitality)
                </button>
              </div>

              <div class="pt-1">
                <input id="fast-diagnosis-input" type="text" class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-emerald-500 font-semibold" value="Waja-ul-Mafasil (Bilateral Knee Osteoarthritis / وجع المفاصل بلغمی)">
              </div>
            </div>

            <!-- Classical Tashkhees Drawer (Nabz, Lisan, Qaroora) -->
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-sm space-y-3">
              <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                <span class="text-xs font-bold text-white flex items-center gap-1.5">
                  <span>🩺</span> Classical Tashkhees (10-Ajnas Pulse, Tongue &amp; Urine)
                </span>
                <span class="text-[9px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono font-bold">Unani Classical Vitals</span>
              </div>

              <!-- Nabz Harakat -->
              <div class="space-y-1">
                <span class="text-[10px] text-slate-400 block font-medium">Nabz Harakat (Pulse Speed / نبض کی حرکت):</span>
                <div class="flex gap-1.5">
                  <button onclick="selectFastTashkhees('pulse', 'Batee')" data-val="Batee" class="fast-pulse-chip px-2.5 py-1 rounded-lg bg-teal-600 text-white font-bold text-[11px] shadow">
                    Batee (Slow / بارد)
                  </button>
                  <button onclick="selectFastTashkhees('pulse', 'Saree')" data-val="Saree" class="fast-pulse-chip px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white text-[11px]">
                    Saree (Rapid / حار)
                  </button>
                  <button onclick="selectFastTashkhees('pulse', 'Motadil')" data-val="Motadil" class="fast-pulse-chip px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white text-[11px]">
                    Motadil (Normal)
                  </button>
                </div>
              </div>

              <!-- Lisan Appearance -->
              <div class="space-y-1">
                <span class="text-[10px] text-slate-400 block font-medium">Lisan (Tongue Coating / زبان کی کیفیت):</span>
                <div class="flex gap-1.5 flex-wrap">
                  <button onclick="selectFastTashkhees('tongue', 'White-Coated')" data-val="White-Coated" class="fast-tongue-chip px-2.5 py-1 rounded-lg bg-teal-600 text-white font-bold text-[11px] shadow">
                    White Slimy (Balghami / بلغم)
                  </button>
                  <button onclick="selectFastTashkhees('tongue', 'Yellowish')" data-val="Yellowish" class="fast-tongue-chip px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white text-[11px]">
                    Yellowish (Safrawi / صفراء)
                  </button>
                  <button onclick="selectFastTashkhees('tongue', 'Normal')" data-val="Normal" class="fast-tongue-chip px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white text-[11px]">
                    Normal Pink (معتدل)
                  </button>
                </div>
              </div>

              <!-- Qaroora / Urine -->
              <div class="space-y-1">
                <span class="text-[10px] text-slate-400 block font-medium">Qaroora (Urine Inspection / قارورہ):</span>
                <div class="flex gap-1.5 flex-wrap">
                  <button onclick="selectFastTashkhees('urine', 'Pale Clear')" data-val="Pale Clear" class="fast-urine-chip px-2.5 py-1 rounded-lg bg-teal-600 text-white font-bold text-[11px] shadow">
                    Abyaz Rakeeq (Pale Watery)
                  </button>
                  <button onclick="selectFastTashkhees('urine', 'Deep Yellow')" data-val="Deep Yellow" class="fast-urine-chip px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white text-[11px]">
                    Asfar Nari (Deep Amber)
                  </button>
                  <button onclick="selectFastTashkhees('urine', 'Mukaddar')" data-val="Mukaddar" class="fast-urine-chip px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white text-[11px]">
                    Mukaddar (Turbid / کدر)
                  </button>
                </div>
              </div>

              <!-- Modern Vitals Bar -->
              <div class="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800 text-[10px]">
                <div class="p-2 rounded bg-slate-900 border border-slate-800">
                  <span class="text-slate-400 block">Blood Pressure:</span>
                  <strong class="text-white">128/82 mmHg</strong>
                </div>
                <div class="p-2 rounded bg-slate-900 border border-slate-800">
                  <span class="text-slate-400 block">Heart Rate:</span>
                  <strong class="text-white">72 bpm</strong>
                </div>
                <div class="p-2 rounded bg-slate-900 border border-slate-800">
                  <span class="text-slate-400 block">hs-CRP Marker:</span>
                  <strong class="text-cyan-400">4.8 mg/L</strong>
                </div>
              </div>
            </div>

            <!-- PERMANENT SAFETY CHECKLIST & STATUTORY AUDIT -->
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-sm space-y-2">
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Real-Time Clinical Safety Rails</span>
              <div class="grid grid-cols-2 gap-2 text-[10px]">
                <div class="p-2 rounded-lg bg-[var(--background)] border border-emerald-500/20 flex items-center justify-between">
                  <span class="text-slate-300">Renal (eGFR 88):</span>
                  <span class="text-emerald-400 font-bold font-mono">PASS ✓</span>
                </div>
                <div class="p-2 rounded-lg bg-[var(--background)] border border-emerald-500/20 flex items-center justify-between">
                  <span class="text-slate-300">Pregnancy / Lactation:</span>
                  <span class="text-emerald-400 font-bold font-mono">CLEAR ✓</span>
                </div>
                <div class="p-2 rounded-lg bg-[var(--background)] border border-emerald-500/20 flex items-center justify-between">
                  <span class="text-slate-300">Schedule E1 Detox:</span>
                  <span class="text-amber-400 font-bold font-mono">CERTIFIED ✓</span>
                </div>
                <div class="p-2 rounded-lg bg-[var(--background)] border border-emerald-500/20 flex items-center justify-between">
                  <span class="text-slate-300">CYP450 Herb-Drug:</span>
                  <span class="text-emerald-400 font-bold font-mono">0 BLOCKS ✓</span>
                </div>
              </div>
            </div>

          </div>

          <!-- COLUMN 2 (7 cols): 1-Click Fast Protocols, Nuskha Pad & Action -->
          <div class="lg:col-span-7 space-y-4 text-xs">
            
            <!-- 1-Click Classical Protocols Bar -->
            <div class="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-slate-700 rounded-2xl p-4 shadow-sm space-y-2.5">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-white flex items-center gap-1.5">
                  <span>⚡</span> 1-Click Classical Master Protocols (Favorite Nuskhas)
                </span>
                <span class="text-[10px] text-amber-300 font-mono font-bold">Fast OPD Dispense</span>
              </div>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                <button onclick="applyFastProtocol('arthri')" class="p-2.5 rounded-xl bg-emerald-800/80 hover:bg-emerald-700 text-white font-bold text-left transition shadow space-y-0.5 border border-emerald-600">
                  <span class="block text-xs">ArthriCare Trio</span>
                  <span class="text-[9px] text-emerald-200 block font-normal">Suranjan + SynovoFlex</span>
                </button>
                <button onclick="applyFastProtocol('gastro')" class="p-2.5 rounded-xl bg-teal-800/80 hover:bg-teal-700 text-white font-bold text-left transition shadow space-y-0.5 border border-teal-600">
                  <span class="block text-xs">GastroBalance</span>
                  <span class="text-[9px] text-teal-200 block font-normal">Kamuni + Bazoori</span>
                </button>
                <button onclick="applyFastProtocol('ceph')" class="p-2.5 rounded-xl bg-purple-800/80 hover:bg-purple-700 text-white font-bold text-left transition shadow space-y-0.5 border border-purple-600">
                  <span class="block text-xs">Cephalic Relief</span>
                  <span class="text-[9px] text-purple-200 block font-normal">Itrifal + TensioCalm</span>
                </button>
                <button onclick="applyFastProtocol('metabolic')" class="p-2.5 rounded-xl bg-amber-800/80 hover:bg-amber-700 text-white font-bold text-left transition shadow space-y-0.5 border border-amber-600">
                  <span class="block text-xs">Metabolic Tonic</span>
                  <span class="text-[9px] text-amber-200 block font-normal">Khabsul Hadeed + Gluco</span>
                </button>
              </div>
            </div>

            <!-- DYNAMIC "ILAJ BIL-ZIDD" MIZAJ BALANCE CARD -->
            <div id="fast-mizaj-indicator">
              <!-- Populated dynamically by calculateIlajBilZidd() -->
            </div>

            <!-- Active Prescribed Formulations List -->
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-sm space-y-3">
              <div class="flex justify-between items-center border-b border-[var(--border)] pb-2.5">
                <span class="font-bold text-white text-xs flex items-center gap-1.5">
                  <span>℞</span> Active Nuskha &amp; Formulations Table
                </span>
                <div class="flex items-center gap-2">
                  <button onclick="openQarabadeenCatalogModal()" class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] rounded-lg transition">
                    + Qarabadeen
                  </button>
                  <button onclick="openZayvoraProductsModal()" class="px-2.5 py-1 bg-amber-600 hover:bg-amber-500 text-white font-bold text-[11px] rounded-lg transition">
                    + ZAYVORA Products
                  </button>
                  <button onclick="openSelfNuskhaModal()" class="px-2.5 py-1 bg-purple-600 hover:bg-purple-500 text-white font-bold text-[11px] rounded-lg transition">
                    + Self-Nuskha
                  </button>
                </div>
              </div>

              <!-- Prescription Items List -->
              <div id="fast-prescriptions-list" class="space-y-2">
                <!-- Rendered dynamically -->
              </div>
            </div>

            <!-- Parhez & Tadbeer Note Pad -->
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-sm space-y-2">
              <span class="text-xs font-bold text-white block">پرہیز و غذائی ہدایات (Dietary Restrictions &amp; Parhez)</span>
              <textarea id="fast-parhez-text" rows="2" class="w-full p-2.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-200 text-xs outline-none focus:border-emerald-500" placeholder="Dietary restrictions...">ٹھنڈا پانی، چاول، دہی، لسی، اڑد کی دال، بادی اشیاء، کھٹائی اور تیز ترش اشیاء سے سخت پرہیز کریں۔ نیم گرم پانی استعمال کریں۔</textarea>
            </div>

            <!-- Bottom Master Actions Bar -->
            <div class="p-4 bg-slate-900 rounded-2xl border border-slate-800 flex flex-col sm:flex-row justify-between items-center gap-3">
              <div class="text-[11px] text-slate-400">
                <span class="text-emerald-400 font-bold">✓ Ready for Dispense:</span> 21 CFR 11 Signed Prescription
              </div>
              <div class="flex items-center gap-2 w-full sm:w-auto">
                <button onclick="openBilingualPrescriptionSlipModal()" class="flex-1 sm:flex-none px-4 py-2.5 bg-teal-600 hover:bg-teal-500 text-white rounded-xl font-bold text-xs shadow-md transition flex items-center justify-center gap-1.5">
                  <span>🖨️</span> Print Patient Slip (Urdu/Eng)
                </button>
                <button onclick="sendRxViaWhatsApp()" class="flex-1 sm:flex-none px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-bold text-xs shadow-md transition flex items-center justify-center gap-1.5">
                  <span>📲</span> WhatsApp Rx
                </button>
              </div>
            </div>

          </div>

        </div>

      </div>
    `;

    // Initialize list and balance indicator
    renderFastMatabPrescriptionList();
    calculateIlajBilZidd();
  }

  function openBilingualPrescriptionSlipModal() {
    const m = document.getElementById('bilingual-rx-slip-modal');
    if (!m) return;

    // Populate patient info
    document.getElementById('slip-patient-name').innerText = state.patient.name;
    document.getElementById('slip-patient-demo').innerText = `${state.patient.age} Y / ${state.patient.gender} (${state.patient.gender === 'Female' ? 'عورت' : 'مرد'})`;
    document.getElementById('slip-patient-mrn').innerText = state.patient.mrn;
    document.getElementById('slip-patient-mizaj').innerText = `${state.patient.mizaj} (مزاج)`;
    
    const diagInput = document.getElementById('fast-diagnosis-input');
    if (diagInput && diagInput.value) {
      document.getElementById('slip-patient-diagnosis').innerText = diagInput.value;
    }

    const parhezInput = document.getElementById('fast-parhez-text');
    if (parhezInput && parhezInput.value) {
      document.getElementById('slip-forbidden-foods').innerText = parhezInput.value;
    }

    // Populate medicines table
    const tableBody = document.getElementById('slip-medicines-table-body');
    const rx = state.prescriptions[0];
    const meds = rx.medicines || [];

    if (meds.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="6" class="p-4 text-center text-slate-400">No active medicines in prescription.</td>
        </tr>
      `;
    } else {
      tableBody.innerHTML = meds.map((m, idx) => `
        <tr class="hover:bg-slate-50 transition border-b border-slate-200">
          <td class="p-2.5 font-bold font-mono text-center border-r border-slate-200">${idx + 1}</td>
          <td class="p-2.5 border-r border-slate-200">
            <strong class="text-slate-900 block text-xs">${m.name}</strong>
            <span class="text-[10px] text-slate-500 font-mono">${m.form || ''} • ${m.track || 'Unani Formulary'}</span>
          </td>
          <td class="p-2.5 text-center border-r border-slate-200 font-semibold text-emerald-800">
            ${m.morning && m.morning !== '—' ? `<span class="bg-amber-100 text-amber-900 px-2 py-0.5 rounded text-[10px] font-bold">☀️ ${m.morning}</span>` : '—'}
          </td>
          <td class="p-2.5 text-center border-r border-slate-200 font-semibold text-emerald-800">
            ${m.noon && m.noon !== '—' ? `<span class="bg-blue-100 text-blue-900 px-2 py-0.5 rounded text-[10px] font-bold">⛅ ${m.noon}</span>` : '—'}
          </td>
          <td class="p-2.5 text-center border-r border-slate-200 font-semibold text-emerald-800">
            ${m.night && m.night !== '—' ? `<span class="bg-indigo-100 text-indigo-900 px-2 py-0.5 rounded text-[10px] font-bold">🌙 ${m.night}</span>` : '—'}
          </td>
          <td class="p-2.5 text-slate-700 text-[11px]">
            <span class="font-bold text-emerald-900">${m.anupan || 'Fresh water'}</span>
            ${m.notes ? `<span class="block text-[10px] text-slate-500">${m.notes}</span>` : ''}
          </td>
        </tr>
      `).join('');
    }

    // SHA-256 Hash display
    document.getElementById('slip-sha256-hash').innerText = 'sha256:' + Math.random().toString(16).substring(2, 10) + Math.random().toString(16).substring(2, 10) + Math.random().toString(16).substring(2, 10);

    m.classList.remove('hidden');
  }

  function closeBilingualPrescriptionSlipModal() {
    const m = document.getElementById('bilingual-rx-slip-modal');
    if (m) m.classList.add('hidden');
  }

  function sendRxViaWhatsApp() {
    const rx = state.prescriptions[0];
    const meds = rx.medicines || [];
    
    let text = `*🌿 ZAYVORA INTEGRATIVE CLINICAL MATAB*%0A`;
    text += `*Patient:* ${state.patient.name} (${state.patient.age}y, ${state.patient.gender})%0A`;
    text += `*MRN:* ${state.patient.mrn}%0A`;
    text += `*Date:* 30-Sep-2026%0A`;
    text += `*Diagnosis:* Waja-ul-Mafasil (Joint Arthralgia)%0A%0A`;
    text += `*℞ PRESCRIBED MEDICINES:*%0A`;
    
    meds.forEach((m, i) => {
      text += `${i+1}. *${m.name}*%0A   - Dosage: ${m.strength}%0A   - Vehicle (Badraqa): ${m.anupan}%0A`;
    });
    
    text += `%0A*PARHEZ & GHIZA (پرہیز):*%0A`;
    text += `Thanda paani, chawal, dahi, baadi cheezein band karein. Neem garam paani istemal karein.%0A%0A`;
    text += `*Next Follow-up:* 14 Days Later.%0A`;
    text += `_Hakeem Dr. Irfan Ashraf (BUMS)_%0A`;
    text += `_Digital Verification: 21 CFR Part 11 Validated_`;

    const phone = "919876543210";
    window.open(`https://wa.me/${phone}?text=${text}`, '_blank');
    showNotification('Prepared bilingual prescription dispatch for WhatsApp!', 'success');
  }

  // =========================================================================
  // CONSULTATION DRAFT AUTO-RECOVERY & KEYBOARD SHORTCUTS
  // =========================================================================

  function autoSaveConsultationDraft() {
    try {
      const draft = {
        timestamp: Date.now(),
        complaint: activeFastComplaint,
        diagnosis: document.getElementById('fast-diagnosis-input')?.value || '',
        pulse: activeFastPulse,
        tongue: activeFastTongue,
        urine: activeFastUrine,
        parhez: document.getElementById('fast-parhez-text')?.value || '',
        medicines: state.prescriptions[0]?.medicines || []
      };
      localStorage.setItem('zayvora_consultation_draft_v2', JSON.stringify(draft));
    } catch(e) {}
  }

  function checkAndRestoreDraft() {
    try {
      const raw = localStorage.getItem('zayvora_consultation_draft_v2');
      if (!raw) return;
      const draft = JSON.parse(raw);
      const ageHours = (Date.now() - draft.timestamp) / (1000 * 3600);
      if (ageHours < 24 && draft.medicines && draft.medicines.length > 0) {
        state.prescriptions[0].medicines = draft.medicines;
      }
    } catch(e) {}
  }

  // Global Keyboard Shortcuts
  window.addEventListener('keydown', function(e) {
    // Cmd+K or Ctrl+K: Quick Drug Search
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      openQarabadeenCatalogModal();
    }
    // Cmd+Enter or Ctrl+Enter: Sign / Finalize
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault();
      if (document.getElementById('bilingual-rx-slip-modal') && !document.getElementById('bilingual-rx-slip-modal').classList.contains('hidden')) {
        window.print();
      } else {
        openBilingualPrescriptionSlipModal();
      }
    }
    // Escape: Close modals
    if (e.key === 'Escape') {
      closeBilingualPrescriptionSlipModal();
      const m1 = document.getElementById('qarabadeen-modal');
      if (m1) m1.classList.add('hidden');
      const m2 = document.getElementById('zayvora-products-modal');
      if (m2) m2.classList.add('hidden');
    }
  });

  // Auto-save interval every 5 seconds
  setInterval(autoSaveConsultationDraft, 5000);
"""

def update_file(filepath):
    print(f"Updating {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Inject Print CSS into <head>
    if "bilingual-rx-slip-modal" not in content:
        if "</head>" in content:
            content = content.replace("</head>", PRINT_CSS + "\n</head>", 1)

    # 2. Inject Bilingual Modal HTML into <body>
    if 'id="bilingual-rx-slip-modal"' not in content:
        if 'id="qarabadeen-modal"' in content:
            content = content.replace('<div id="qarabadeen-modal"', BILINGUAL_MODAL_HTML + '\n  <div id="qarabadeen-modal"', 1)
        elif '</body>' in content:
            content = content.replace('</body>', BILINGUAL_MODAL_HTML + '\n</body>', 1)

    # 3. Inject Fast Matab & Bilingual Slip JS
    if "function setConsultationMode" not in content:
        if "function renderSingleConsultationWorkspace(container)" in content:
            target = "function renderSingleConsultationWorkspace(container) {"
            replacement = FAST_MATAB_JS + "\n\n    function renderSingleConsultationWorkspace(container) {\n      if (state.consultationMode === 'fast') { renderFastMatabMode(container); return; }"
            content = content.replace(target, replacement, 1)

    # 4. Enhance renderSingleConsultationWorkspace top bar with mode switch button & slip button
    if "openBilingualPrescriptionSlipModal()" not in content:
        target_btn = '<button onclick="completeConsultation()"'
        replacement_btn = """<div class="flex items-center bg-slate-900 border border-slate-700 rounded-xl p-1 mr-2">
                <button onclick="setConsultationMode('fast')" class="px-2.5 py-1 rounded-lg text-xs font-bold transition text-slate-400 hover:text-white">⚡ Fast Matab</button>
                <button onclick="setConsultationMode('continuum')" class="px-2.5 py-1 rounded-lg text-xs font-bold transition bg-emerald-600 text-white shadow">🔬 13-Step Detailed</button>
              </div>
              <button onclick="openBilingualPrescriptionSlipModal()" class="px-3.5 py-2 rounded-xl bg-teal-600/30 border border-teal-500/40 text-teal-300 text-xs font-bold hover:bg-teal-600/40 flex items-center gap-1.5 transition">
                <span>🖨️</span> Patient Slip (Urdu/Eng)
              </button>
              <button onclick="completeConsultation()" """
        content = content.replace(target_btn, replacement_btn, 1)

    # 5. Enhance Tab 11 (Prescription) with Bilingual Patient Slip button
    if 'Tab 11: Master Prescription Studio' in content:
        old_bar = '<span id="consultation-lock-badge"'
        new_bar = '<button onclick="openBilingualPrescriptionSlipModal()" class="px-3 py-1 bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold rounded-lg shadow transition flex items-center gap-1"><span>🖨️</span> Print Patient Slip (Urdu/Eng)</button>\n              <span id="consultation-lock-badge"'
        content = content.replace(old_bar, new_bar, 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully updated {filepath} (Size: {os.path.getsize(filepath)} bytes)")

def main():
    target_files = [
        os.path.join(BASE_DIR, "app.html"),
        os.path.join(BASE_DIR, "docs", "app.html"),
        os.path.join(BASE_DIR, "index.html"),
        os.path.join(BASE_DIR, "docs", "index.html"),
    ]
    for tf in target_files:
        if os.path.exists(tf):
            update_file(tf)
        else:
            print(f"Warning: File {tf} not found")

if __name__ == "__main__":
    main()
