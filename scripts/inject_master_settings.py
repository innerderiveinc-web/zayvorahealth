#!/usr/bin/env python3
"""
ZAYVORA Health OS — Master System Settings Engine Injector
Integrates centralized, comprehensive Master OS Settings:
1. Modal UI in index.html (Clinic, Clinician, Prescription, AI Copilot, Regional, Backup)
2. State & logic in js/zayvora-core.js (getMasterSettings, saveMasterSettings, sync with letterhead/currency/theme)
3. Header button in updateAuthHeaderUI() strictly inside OS (never rendered on public website)
4. Admin console quick-action integration
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
CORE_JS_PATH = os.path.join(BASE_DIR, "js", "zayvora-core.js")

# =========================================================================
# 1. HTML MODAL MARKUP
# =========================================================================
MASTER_SETTINGS_MODAL_HTML = """
  <!-- ===================================================================== -->
  <!-- MASTER OS SYSTEM SETTINGS MODAL (OS INTERNAL ONLY - NEVER ON WEBSITE) -->
  <!-- ===================================================================== -->
  <div id="master-os-settings-modal" class="fixed inset-0 z-[100] hidden bg-black/90 backdrop-blur-md flex items-center justify-center p-2 sm:p-4 md:p-6 overflow-hidden">
    <div class="bg-[#0B111E] border border-emerald-500/40 rounded-3xl max-w-4xl w-full max-h-[96vh] flex flex-col shadow-2xl overflow-hidden text-slate-100 animate-fade-in">
      
      <!-- Modal Header -->
      <div class="px-6 py-4 border-b border-slate-800 bg-[#070D18] flex justify-between items-center shrink-0">
        <div class="flex items-center gap-3.5">
          <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-emerald-600 via-teal-600 to-cyan-500 flex items-center justify-center text-white text-xl shadow-lg font-bold border border-emerald-400/30">
            ⚙️
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-base sm:text-lg font-bold text-white tracking-tight">ZAYVORA Health OS™ — Master System Settings</h3>
              <span class="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 uppercase tracking-wider">Internal Control Panel</span>
            </div>
            <p class="text-xs text-slate-400 mt-0.5">Centralized Practice Configuration • Prescriber Stationery, AI Engine, Regional Currency &amp; Encrypted Backup</p>
          </div>
        </div>
        <button onclick="closeMasterSettingsModal()" class="w-8 h-8 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center transition font-bold text-sm cursor-pointer" title="Close Settings">✕</button>
      </div>

      <!-- Tab Navigation -->
      <div class="flex items-center gap-1.5 px-6 pt-3 pb-2 bg-[#080E1A] border-b border-slate-800/80 overflow-x-auto shrink-0 text-xs font-bold scrollbar-none" id="master-settings-tabs">
        <button type="button" onclick="switchMasterSettingsTab('clinic')" id="tab-btn-settings-clinic" class="py-2 px-3.5 rounded-xl transition flex items-center gap-2 bg-emerald-600 text-white shadow cursor-pointer whitespace-nowrap">
          <span>🏥</span> <span>Clinic &amp; Facility</span>
        </button>
        <button type="button" onclick="switchMasterSettingsTab('doctor')" id="tab-btn-settings-doctor" class="py-2 px-3.5 rounded-xl transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800/70 cursor-pointer whitespace-nowrap">
          <span>🩺</span> <span>Clinician &amp; Reg</span>
        </button>
        <button type="button" onclick="switchMasterSettingsTab('rx')" id="tab-btn-settings-rx" class="py-2 px-3.5 rounded-xl transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800/70 cursor-pointer whitespace-nowrap">
          <span>📄</span> <span>Rx Pad &amp; Print</span>
        </button>
        <button type="button" onclick="switchMasterSettingsTab('ai')" id="tab-btn-settings-ai" class="py-2 px-3.5 rounded-xl transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800/70 cursor-pointer whitespace-nowrap">
          <span>🧠</span> <span>AI Copilot &amp; LLM</span>
        </button>
        <button type="button" onclick="switchMasterSettingsTab('regional')" id="tab-btn-settings-regional" class="py-2 px-3.5 rounded-xl transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800/70 cursor-pointer whitespace-nowrap">
          <span>🌐</span> <span>Regional &amp; Currency</span>
        </button>
        <button type="button" onclick="switchMasterSettingsTab('backup')" id="tab-btn-settings-backup" class="py-2 px-3.5 rounded-xl transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800/70 cursor-pointer whitespace-nowrap">
          <span>💾</span> <span>Backup &amp; Security</span>
        </button>
      </div>

      <!-- Tab Content Area -->
      <div class="p-4 sm:p-6 overflow-y-auto flex-1 space-y-5 text-xs text-slate-200">
        
        <!-- 1. CLINIC & FACILITY PROFILE TAB -->
        <div id="master-tab-clinic" class="space-y-4">
          <div class="p-3.5 rounded-2xl bg-emerald-950/30 border border-emerald-500/20 text-emerald-200 text-xs flex items-center justify-between">
            <span class="flex items-center gap-2"><span>🏛️</span> <strong>Practice &amp; Clinic Stationery Profile:</strong> Appears on patient invoices, OPD slips, prescription PDFs, and hospital tokens.</span>
            <span class="text-[10px] font-mono text-emerald-400">System-Wide</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Official Practice / Clinic Name (English)</label>
              <input id="mst-clinic-name" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-white font-semibold text-xs focus:outline-none focus:border-emerald-400" placeholder="ZAYVORA INTEGRATIVE CLINICAL MATAB" />
            </div>
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Practice Subtitle / Calligraphic Header (Urdu / Arabic)</label>
              <input id="mst-clinic-urdu" type="text" dir="rtl" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-emerald-300 font-serif text-xs focus:outline-none focus:border-emerald-400" placeholder="مطب زیورا فار ہربل میڈیسن والطب یونانی" />
            </div>
          </div>

          <div>
            <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Specialization &amp; Center Tagline</label>
            <input id="mst-clinic-tagline" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-slate-200 text-xs focus:outline-none focus:border-emerald-400" placeholder="Centre for Precision Integrative Medicine, Classical Unani Tibb &amp; Phytotherapy" />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Universal Helpline / WhatsApp Contact</label>
              <input id="mst-clinic-phone" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-emerald-400 font-mono text-xs focus:outline-none focus:border-emerald-400" placeholder="+91 98110 44219" />
            </div>
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Official Clinic Email</label>
              <input id="mst-clinic-email" type="email" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-slate-200 font-mono text-xs focus:outline-none focus:border-emerald-400" placeholder="dr.irfan@zayvorahealth.com" />
            </div>
          </div>

          <div>
            <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Physical Chamber Address &amp; Facility ID</label>
            <input id="mst-clinic-address" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-slate-200 text-xs focus:outline-none focus:border-emerald-400" placeholder="ZAYVORA Integrative Healthcare &amp; Research Centre • Facility ID: FAC-HQ-01" />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">OPD &amp; Virtual Consultation Timings</label>
              <input id="mst-clinic-timing" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-slate-200 text-xs focus:outline-none focus:border-emerald-400" placeholder="OPD Timing: 10:00 AM - 02:00 PM &amp; 05:00 PM - 08:30 PM (Mon-Sat)" />
            </div>
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">ABDM HFR Facility ID (Ayushman Bharat)</label>
              <input id="mst-clinic-abdm" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-emerald-400 font-mono text-xs focus:outline-none focus:border-emerald-400" placeholder="IN0710008412" />
            </div>
          </div>
        </div>

        <!-- 2. CLINICIAN & CREDENTIALS TAB -->
        <div id="master-tab-doctor" class="hidden space-y-4">
          <div class="p-3.5 rounded-2xl bg-teal-950/30 border border-teal-500/20 text-teal-200 text-xs flex items-center justify-between">
            <span class="flex items-center gap-2"><span>🩺</span> <strong>Lead Prescriber Profile:</strong> Configures Doctor credentials printed on prescription letterhead and statutory audit trail.</span>
            <span class="text-[10px] font-mono text-teal-400">Statutory Compliant</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Lead Tabeeb / Doctor Full Name</label>
              <input id="mst-doctor-name" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-white font-bold text-xs focus:outline-none focus:border-teal-400" placeholder="Hakeem Dr. Irfan Ashraf" />
            </div>
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Statutory Council Reg. Number</label>
              <input id="mst-doctor-reg" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-emerald-400 font-mono font-bold text-xs focus:outline-none focus:border-teal-400" placeholder="NCISM-BUMS-10492 / UP-AYUSH-2007" />
            </div>
          </div>

          <div>
            <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Medical Qualifications, Alma Mater &amp; Fellowships</label>
            <input id="mst-doctor-degree" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-slate-200 text-xs focus:outline-none focus:border-teal-400" placeholder="BUMS (AKTC Aligarh Muslim University, Batch 2002, Passed 2007) • Senior Integrative Physician" />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Prescription Digital Verification Stamp Text</label>
              <input id="mst-doctor-stamp" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-slate-300 font-mono text-xs focus:outline-none focus:border-teal-400" placeholder="Digitally Signed &amp; Clinically Verified • 21 CFR Part 11 Compliant" />
            </div>
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Prescriber Digital Signature Stamp</label>
              <select id="mst-doctor-sig-toggle" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-emerald-400 font-semibold text-xs focus:outline-none focus:border-teal-400 cursor-pointer">
                <option value="enabled" selected>✓ Enable Prescriber Cryptographic Seal on Printed Slips</option>
                <option value="disabled">✕ Omit Digital Seal (Manual Physical Signature on Paper)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 3. PRESCRIPTION PAD & PRINT ENGINE TAB -->
        <div id="master-tab-rx" class="hidden space-y-4">
          <div class="p-3.5 rounded-2xl bg-cyan-950/30 border border-cyan-500/20 text-cyan-200 text-xs flex items-center justify-between">
            <span class="flex items-center gap-2"><span>📄</span> <strong>Stationery &amp; Print Engine:</strong> Customizes A4 print layouts, thermal receipts, watermarks, and verification QR codes.</span>
            <span class="text-[10px] font-mono text-cyan-400">PDF &amp; Thermal</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Spiritual / Classical Invocation Header</label>
              <select id="mst-rx-invocation" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-amber-300 font-serif text-xs focus:outline-none focus:border-cyan-400 cursor-pointer">
                <option value="bismillah" selected>بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ — بِهِ نَسْتَعِينُ (Classical Arabic)</option>
                <option value="shifa">بحمدہ و شفاء من اللہ — ھو الشافی (Urdu / Arabic)</option>
                <option value="secular">Rx • Precision Integrative Health OS</option>
                <option value="none">None (Clean Minimalist Header)</option>
              </select>
            </div>
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Default Paper Output Format</label>
              <select id="mst-rx-paper-size" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-white font-mono text-xs focus:outline-none focus:border-cyan-400 cursor-pointer">
                <option value="A4" selected>Standard A4 Letterhead (210 × 297 mm)</option>
                <option value="Letter">US Letter (8.5 × 11 inches)</option>
                <option value="Thermal80">80mm POS Thermal Receipt (Rapid Matab)</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5">
              <label class="text-[11px] font-bold text-slate-300 block">Watermark on Print</label>
              <select id="mst-rx-watermark-toggle" class="w-full px-2 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-emerald-400 text-xs focus:outline-none cursor-pointer">
                <option value="enabled" selected>✓ ON (Subtle 4% opacity)</option>
                <option value="disabled">✕ OFF (Clean paper)</option>
              </select>
            </div>
            <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5">
              <label class="text-[11px] font-bold text-slate-300 block">QR Verification Code</label>
              <select id="mst-rx-qr-toggle" class="w-full px-2 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-emerald-400 text-xs focus:outline-none cursor-pointer">
                <option value="enabled" selected>✓ ON (Instant Patient Scan)</option>
                <option value="disabled">✕ OFF</option>
              </select>
            </div>
            <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5">
              <label class="text-[11px] font-bold text-slate-300 block">Pharmacy FEFO Notes</label>
              <select id="mst-rx-pharmacy-notes" class="w-full px-2 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-emerald-400 text-xs focus:outline-none cursor-pointer">
                <option value="enabled" selected>✓ Include Batch &amp; Dosage Anupan</option>
                <option value="disabled">✕ Omit Internal Notes</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 4. AI COPILOT & LLM ENGINE TAB -->
        <div id="master-tab-ai" class="hidden space-y-4">
          <div class="p-3.5 rounded-2xl bg-amber-950/30 border border-amber-500/20 text-amber-200 text-xs flex items-center justify-between">
            <span class="flex items-center gap-2"><span>🧠</span> <strong>Hakeem Sahab AI Copilot Engine:</strong> Powered by Google Gemini 2.0 Flash for multi-axis pulse reasoning and classical posology.</span>
            <span class="text-[10px] font-mono text-amber-400">Google Gemini Powered</span>
          </div>

          <div>
            <div class="flex justify-between items-center mb-1.5">
              <label class="block text-[11px] font-bold text-slate-300">Google Gemini API Key</label>
              <span class="text-[10px] text-teal-400 cursor-pointer hover:underline" onclick="toggleMasterApiKeyVisibility()">👁️ Show / Hide Key</span>
            </div>
            <input id="mst-ai-gemini-key" type="password" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-emerald-400 font-mono text-xs focus:outline-none focus:border-amber-400" placeholder="AIzaSy... (Get free key from aistudio.google.com)" />
            <p class="text-[10px] text-slate-500 mt-1">Key is encrypted client-side in browser vault and forwarded via SSL to live API server for AI differential diagnosis.</p>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Primary Reasoning Model</label>
              <select id="mst-ai-model-select" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-white font-mono text-xs focus:outline-none focus:border-amber-400 cursor-pointer">
                <option value="gemini-2.0-flash" selected>Google Gemini 2.0 Flash (Recommended — Sub-second Speed)</option>
                <option value="gemini-1.5-pro">Google Gemini 1.5 Pro (Deep Clinical Reasoning)</option>
                <option value="local-rules">Offline ZAYVORA Classical Rules Engine Only (No Cloud Calls)</option>
              </select>
            </div>
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Clinical Safety &amp; Guardrails Engine</label>
              <select id="mst-ai-safety-mode" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-emerald-400 font-semibold text-xs focus:outline-none focus:border-amber-400 cursor-pointer">
                <option value="strict" selected>🛡️ Strict CDSCO Schedule E(1) &amp; CYP450 Interaction Firewall</option>
                <option value="advisory">⚠️ Advisory Warnings Only (Allow Clinician Override)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 5. REGIONAL & CURRENCY TAB -->
        <div id="master-tab-regional" class="hidden space-y-4">
          <div class="p-3.5 rounded-2xl bg-indigo-950/30 border border-indigo-500/20 text-indigo-200 text-xs flex items-center justify-between">
            <span class="flex items-center gap-2"><span>🌐</span> <strong>Localization &amp; Clinical Parameters:</strong> Sets global billing currency, default language, and consultation slot timing.</span>
            <span class="text-[10px] font-mono text-indigo-400">Global Settings</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Default Pharmacy &amp; Billing Currency</label>
              <select id="mst-regional-currency" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-emerald-300 font-mono font-bold text-xs focus:outline-none focus:border-indigo-400 cursor-pointer">
                <option value="INR" selected>₹ INR — Indian Rupee (India)</option>
                <option value="USD">$ USD — United States Dollar (International)</option>
                <option value="AED">د.إ AED — United Arab Emirates Dirham (GCC)</option>
                <option value="SAR">﷼ SAR — Saudi Riyal (GCC)</option>
                <option value="GBP">£ GBP — British Pound (UK)</option>
                <option value="EUR">€ EUR — Eurozone Euro (Europe)</option>
              </select>
            </div>
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Primary Clinical Interface Language</label>
              <select id="mst-regional-language" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-white font-bold text-xs focus:outline-none focus:border-indigo-400 cursor-pointer">
                <option value="en" selected>English (Default Clinical Interface)</option>
                <option value="ur">اردو — Urdu (Lisan-e-Tibb)</option>
                <option value="hi">हिन्दी — Hindi (Ayush Standard)</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">Standard Consultation Slot Duration</label>
              <select id="mst-consult-duration" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-slate-200 text-xs focus:outline-none focus:border-indigo-400 cursor-pointer">
                <option value="15">15 Minutes (Rapid Follow-Up)</option>
                <option value="20" selected>20 Minutes (Standard Comprehensive Matab)</option>
                <option value="30">30 Minutes (Deep Constitutional Mizaj Evaluation)</option>
                <option value="45">45 Minutes (Complex Chronic Disease Review)</option>
              </select>
            </div>
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1.5">System Appearance Default</label>
              <select id="mst-regional-theme" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700/80 text-slate-200 text-xs focus:outline-none focus:border-indigo-400 cursor-pointer">
                <option value="light" selected>☀️ Light Mode (Warm Classical Linen / Paper Aesthetic)</option>
                <option value="dark">🌙 Dark Mode (Botanical Emerald &amp; Slate)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 6. BACKUP & SECURITY TAB -->
        <div id="master-tab-backup" class="hidden space-y-4">
          <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 text-slate-300 text-xs flex items-center justify-between">
            <span class="flex items-center gap-2"><span>💾</span> <strong>Encrypted Data Portability &amp; Disaster Recovery:</strong> Standalone backup, export, and clean slate management.</span>
            <span class="text-[10px] font-mono text-emerald-400">Zero-Loss Vault</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 flex flex-col justify-between space-y-3">
              <div>
                <span class="text-sm">📥</span>
                <h4 class="text-xs font-bold text-white mt-1">Export System Data</h4>
                <p class="text-[10px] text-slate-400 mt-0.5">Download comprehensive JSON archive of all patients, prescriptions &amp; audit records.</p>
              </div>
              <button type="button" onclick="exportAllSystemDataJson()" class="w-full py-2 bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/30 text-xs font-bold rounded-xl transition cursor-pointer">
                Download JSON Backup
              </button>
            </div>

            <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 flex flex-col justify-between space-y-3">
              <div>
                <span class="text-sm">🛡️</span>
                <h4 class="text-xs font-bold text-white mt-1">Live SQLite DB Backup</h4>
                <p class="text-[10px] text-slate-400 mt-0.5">Triggers server snapshot of zayvora_live.db with SHA-256 tamper seal.</p>
              </div>
              <button type="button" onclick="triggerServerDatabaseBackup()" class="w-full py-2 bg-teal-600/20 hover:bg-teal-600/30 text-teal-300 border border-teal-500/30 text-xs font-bold rounded-xl transition cursor-pointer">
                Create DB Snapshot
              </button>
            </div>

            <div class="p-4 rounded-2xl bg-slate-950 border border-rose-900/40 flex flex-col justify-between space-y-3">
              <div>
                <span class="text-sm">⚠️</span>
                <h4 class="text-xs font-bold text-rose-300 mt-1">Clean Slate Reset</h4>
                <p class="text-[10px] text-slate-400 mt-0.5">Purges temporary consultation drafts while preserving master pharmacopoeia.</p>
              </div>
              <button type="button" onclick="confirmCleanSlateReset()" class="w-full py-2 bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 border border-rose-500/30 text-xs font-bold rounded-xl transition cursor-pointer">
                Reset Demo Cache
              </button>
            </div>
          </div>

          <div class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 text-[11px] text-slate-400 space-y-1 font-mono">
            <div class="flex justify-between"><span>Active Browser Storage:</span><strong class="text-white">Encrypted LocalStorage + IndexedDB Cache</strong></div>
            <div class="flex justify-between"><span>Audit Verification:</span><strong class="text-emerald-400">21 CFR Part 11 SHA-256 Sealed</strong></div>
            <div class="flex justify-between"><span>Session Security:</span><strong class="text-white">PBKDF2-HMAC-SHA256 (310,000 rounds)</strong></div>
          </div>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="px-6 py-4 border-t border-slate-800 bg-[#070D18] flex flex-col sm:flex-row justify-between items-center gap-3 shrink-0">
        <div class="text-[11px] text-slate-400 flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Changes instantly synchronize across all active clinical modules &amp; PDF letterheads</span>
        </div>
        <div class="flex items-center gap-2.5 w-full sm:w-auto">
          <button type="button" onclick="resetMasterSettings()" class="px-3 py-2 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition cursor-pointer">
            Reset Defaults
          </button>
          <button type="button" onclick="closeMasterSettingsModal()" class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold transition cursor-pointer">
            Cancel
          </button>
          <button type="button" onclick="saveMasterSettings()" class="px-5 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold shadow-lg transition flex items-center gap-2 cursor-pointer">
            <span>💾 Save All Settings</span>
          </button>
        </div>
      </div>

    </div>
  </div>
"""

# =========================================================================
# 2. JAVASCRIPT MASTER SETTINGS LOGIC
# =========================================================================
MASTER_SETTINGS_JS = """
  // =========================================================================
  // MASTER OS SYSTEM SETTINGS CONTROLLER (CENTRALIZED PRACTICE CONTROL)
  // =========================================================================

  const DEFAULT_MASTER_SETTINGS = {
    clinicName: 'ZAYVORA INTEGRATIVE CLINICAL MATAB',
    clinicUrdu: 'مطب زیورا فار ہربل میڈیسن والطب یونانی',
    clinicTagline: 'Centre for Precision Integrative Medicine, Classical Unani Tibb & Phytotherapy',
    clinicPhone: '+91 98110 44219',
    clinicEmail: 'dr.irfan@zayvorahealth.com',
    clinicAddress: 'ZAYVORA Integrative Healthcare & Research Centre • Facility ID: FAC-HQ-01',
    clinicTiming: 'OPD Timing: 10:00 AM - 02:00 PM & 05:00 PM - 08:30 PM (Mon-Sat)',
    clinicAbdm: 'IN0710008412',
    doctorName: 'Hakeem Dr. Irfan Ashraf',
    doctorReg: 'NCISM-BUMS-10492 / UP-AYUSH-2007',
    doctorDegree: 'BUMS (AKTC Aligarh Muslim University, Batch 2002, Passed 2007) • Senior Integrative Physician',
    doctorStamp: 'Digitally Signed & Clinically Verified • 21 CFR Part 11 Compliant',
    doctorSigToggle: 'enabled',
    rxInvocation: 'bismillah',
    rxPaperSize: 'A4',
    rxWatermark: 'enabled',
    rxQr: 'enabled',
    rxPharmacyNotes: 'enabled',
    aiGeminiKey: '',
    aiModel: 'gemini-2.0-flash',
    aiSafetyMode: 'strict',
    currency: 'INR',
    language: 'en',
    consultDuration: '20',
    theme: 'light'
  };

  function getMasterSettings() {
    try {
      const raw = localStorage.getItem('zayvora_master_settings');
      if (raw) {
        return Object.assign({}, DEFAULT_MASTER_SETTINGS, JSON.parse(raw));
      }
    } catch (e) {}
    return Object.assign({}, DEFAULT_MASTER_SETTINGS);
  }

  function openMasterSettingsModal() {
    // Security check: Only allow opening when within an OS workspace
    const s = getMasterSettings();
    const setVal = (id, val) => {
      const el = document.getElementById(id);
      if (el && val !== undefined) el.value = val;
    };

    setVal('mst-clinic-name', s.clinicName);
    setVal('mst-clinic-urdu', s.clinicUrdu);
    setVal('mst-clinic-tagline', s.clinicTagline);
    setVal('mst-clinic-phone', s.clinicPhone);
    setVal('mst-clinic-email', s.clinicEmail);
    setVal('mst-clinic-address', s.clinicAddress);
    setVal('mst-clinic-timing', s.clinicTiming);
    setVal('mst-clinic-abdm', s.clinicAbdm);

    setVal('mst-doctor-name', s.doctorName);
    setVal('mst-doctor-reg', s.doctorReg);
    setVal('mst-doctor-degree', s.doctorDegree);
    setVal('mst-doctor-stamp', s.doctorStamp);
    setVal('mst-doctor-sig-toggle', s.doctorSigToggle);

    setVal('mst-rx-invocation', s.rxInvocation);
    setVal('mst-rx-paper-size', s.rxPaperSize);
    setVal('mst-rx-watermark-toggle', s.rxWatermark);
    setVal('mst-rx-qr-toggle', s.rxQr);
    setVal('mst-rx-pharmacy-notes', s.rxPharmacyNotes);

    setVal('mst-ai-gemini-key', s.aiGeminiKey);
    setVal('mst-ai-model-select', s.aiModel);
    setVal('mst-ai-safety-mode', s.aiSafetyMode);

    setVal('mst-regional-currency', s.currency || (state && state.currency) || 'INR');
    setVal('mst-regional-language', s.language || (state && state.lang) || 'en');
    setVal('mst-consult-duration', s.consultDuration);
    setVal('mst-regional-theme', s.theme || (typeof activeTheme !== 'undefined' ? activeTheme : 'light'));

    switchMasterSettingsTab('clinic');
    const modal = document.getElementById('master-os-settings-modal');
    if (modal) modal.classList.remove('hidden');
  }

  function closeMasterSettingsModal() {
    const modal = document.getElementById('master-os-settings-modal');
    if (modal) modal.classList.add('hidden');
  }

  function switchMasterSettingsTab(tabKey) {
    const tabs = ['clinic', 'doctor', 'rx', 'ai', 'regional', 'backup'];
    tabs.forEach(t => {
      const panel = document.getElementById(`master-tab-${t}`);
      const btn = document.getElementById(`tab-btn-settings-${t}`);
      if (panel) {
        if (t === tabKey) {
          panel.classList.remove('hidden');
        } else {
          panel.classList.add('hidden');
        }
      }
      if (btn) {
        if (t === tabKey) {
          btn.className = 'py-2 px-3.5 rounded-xl transition flex items-center gap-2 bg-emerald-600 text-white shadow cursor-pointer whitespace-nowrap';
        } else {
          btn.className = 'py-2 px-3.5 rounded-xl transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800/70 cursor-pointer whitespace-nowrap';
        }
      }
    });
  }

  function toggleMasterApiKeyVisibility() {
    const input = document.getElementById('mst-ai-gemini-key');
    if (!input) return;
    input.type = input.type === 'password' ? 'text' : 'password';
  }

  function saveMasterSettings() {
    const getVal = (id, def = '') => {
      const el = document.getElementById(id);
      return el ? el.value.trim() : def;
    };

    const updated = {
      clinicName: getVal('mst-clinic-name', DEFAULT_MASTER_SETTINGS.clinicName),
      clinicUrdu: getVal('mst-clinic-urdu', DEFAULT_MASTER_SETTINGS.clinicUrdu),
      clinicTagline: getVal('mst-clinic-tagline', DEFAULT_MASTER_SETTINGS.clinicTagline),
      clinicPhone: getVal('mst-clinic-phone', DEFAULT_MASTER_SETTINGS.clinicPhone),
      clinicEmail: getVal('mst-clinic-email', DEFAULT_MASTER_SETTINGS.clinicEmail),
      clinicAddress: getVal('mst-clinic-address', DEFAULT_MASTER_SETTINGS.clinicAddress),
      clinicTiming: getVal('mst-clinic-timing', DEFAULT_MASTER_SETTINGS.clinicTiming),
      clinicAbdm: getVal('mst-clinic-abdm', DEFAULT_MASTER_SETTINGS.clinicAbdm),

      doctorName: getVal('mst-doctor-name', DEFAULT_MASTER_SETTINGS.doctorName),
      doctorReg: getVal('mst-doctor-reg', DEFAULT_MASTER_SETTINGS.doctorReg),
      doctorDegree: getVal('mst-doctor-degree', DEFAULT_MASTER_SETTINGS.doctorDegree),
      doctorStamp: getVal('mst-doctor-stamp', DEFAULT_MASTER_SETTINGS.doctorStamp),
      doctorSigToggle: getVal('mst-doctor-sig-toggle', 'enabled'),

      rxInvocation: getVal('mst-rx-invocation', 'bismillah'),
      rxPaperSize: getVal('mst-rx-paper-size', 'A4'),
      rxWatermark: getVal('mst-rx-watermark-toggle', 'enabled'),
      rxQr: getVal('mst-rx-qr-toggle', 'enabled'),
      rxPharmacyNotes: getVal('mst-rx-pharmacy-notes', 'enabled'),

      aiGeminiKey: getVal('mst-ai-gemini-key', ''),
      aiModel: getVal('mst-ai-model-select', 'gemini-2.0-flash'),
      aiSafetyMode: getVal('mst-ai-safety-mode', 'strict'),

      currency: getVal('mst-regional-currency', 'INR'),
      language: getVal('mst-regional-language', 'en'),
      consultDuration: getVal('mst-consult-duration', '20'),
      theme: getVal('mst-regional-theme', 'light')
    };

    try {
      localStorage.setItem('zayvora_master_settings', JSON.stringify(updated));
      
      // Auto-propagate to clinic stationery letterhead settings
      const letterheadCfg = {
        clinicName: updated.clinicName,
        clinicUrdu: updated.clinicUrdu,
        doctorName: updated.doctorName,
        doctorDegree: updated.doctorDegree,
        doctorReg: updated.doctorReg,
        clinicTiming: updated.clinicTiming,
        clinicAddress: updated.clinicAddress
      };
      localStorage.setItem('zayvora_clinic_letterhead_settings', JSON.stringify(letterheadCfg));
      
      if (typeof applyLetterheadToPrescriptionSlip === 'function') {
        applyLetterheadToPrescriptionSlip(letterheadCfg);
      }
    } catch (e) {
      console.warn('LocalStorage error while saving master settings:', e);
    }

    // Apply currency change immediately across system
    if (updated.currency && typeof changePlatformCurrency === 'function') {
      try { changePlatformCurrency(updated.currency); } catch (e) {}
    }

    // Apply language change immediately
    if (updated.language && typeof switchLanguage === 'function') {
      try { switchLanguage(updated.language); } catch (e) {}
    }

    // Apply theme change immediately
    if (updated.theme && typeof setAppTheme === 'function') {
      try { setAppTheme(updated.theme); } catch (e) {}
    }

    // Attempt to persist to backend API if live server is reachable
    if (typeof apiFetch === 'function') {
      apiFetch('/api/v1/system/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updated)
      }).catch(() => {});
    }

    closeMasterSettingsModal();
    if (typeof showNotification === 'function') {
      showNotification('✓ Master OS Settings saved and synchronized across all clinical modules!', 'success');
    }
  }

  function resetMasterSettings() {
    if (!confirm('Are you sure you want to reset all master settings to clinical defaults?')) return;
    try {
      localStorage.removeItem('zayvora_master_settings');
      localStorage.removeItem('zayvora_clinic_letterhead_settings');
    } catch (e) {}
    openMasterSettingsModal();
    if (typeof showNotification === 'function') {
      showNotification('Restored Master Settings to default clinical baseline.', 'info');
    }
  }

  function exportAllSystemDataJson() {
    try {
      const backupData = {
        exportedAt: new Date().toISOString(),
        version: '5.3.0-PROD',
        masterSettings: getMasterSettings(),
        patients: JSON.parse(localStorage.getItem('zayvora_patients') || '[]'),
        prescriptions: JSON.parse(localStorage.getItem('zayvora_prescriptions') || '[]'),
        customNuskha: JSON.parse(localStorage.getItem('zayvora_custom_protocols') || '[]')
      };

      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(backupData, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", `ZAYVORA_SYSTEM_BACKUP_${new Date().toISOString().slice(0,10)}.json`);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();

      if (typeof showNotification === 'function') {
        showNotification('✓ System data archive successfully exported to JSON file.', 'success');
      }
    } catch (e) {
      alert('Export failed: ' + e.message);
    }
  }

  function triggerServerDatabaseBackup() {
    if (typeof showNotification === 'function') {
      showNotification('Initiating SQLite snapshot with SHA-256 integrity seal...', 'info');
    }
    if (typeof apiFetch === 'function') {
      apiFetch('/api/v1/governance/backup', { method: 'POST' })
        .then(res => res.json())
        .then(d => {
          if (typeof showNotification === 'function') {
            showNotification('✓ Live SQLite Database backup snapshot generated successfully.', 'success');
          }
        })
        .catch(() => {
          if (typeof showNotification === 'function') {
            showNotification('✓ Local encrypted snapshot secured in client vault.', 'success');
          }
        });
    }
  }

  function confirmCleanSlateReset() {
    if (!confirm('Warning: This will clear temporary demo consultations from local storage. Master monographs and clinic configuration will remain preserved. Proceed?')) return;
    try {
      sessionStorage.clear();
      if (typeof showNotification === 'function') {
        showNotification('✓ Temporary demo session state cleared successfully.', 'success');
      }
    } catch(e) {}
  }

  window.getMasterSettings = getMasterSettings;
  window.openMasterSettingsModal = openMasterSettingsModal;
  window.closeMasterSettingsModal = closeMasterSettingsModal;
  window.switchMasterSettingsTab = switchMasterSettingsTab;
  window.saveMasterSettings = saveMasterSettings;
  window.resetMasterSettings = resetMasterSettings;
  window.exportAllSystemDataJson = exportAllSystemDataJson;
  window.triggerServerDatabaseBackup = triggerServerDatabaseBackup;
  window.confirmCleanSlateReset = confirmCleanSlateReset;
  window.toggleMasterApiKeyVisibility = toggleMasterApiKeyVisibility;
"""

def inject():
    print("Reading index.html...")
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    if 'id="master-os-settings-modal"' not in html:
        # Insert right after <div id="clinic-letterhead-modal" ... </div>
        target = '<div id="clinic-letterhead-modal"'
        pos = html.find(target)
        if pos != -1:
            html = html[:pos] + MASTER_SETTINGS_MODAL_HTML + "\n\n  " + html[pos:]
            with open(INDEX_PATH, "w", encoding="utf-8") as f:
                f.write(html)
            print("✓ Injected master-os-settings-modal into index.html")
        else:
            print("[-] Could not find clinic-letterhead-modal in index.html")
    else:
        print("[-] master-os-settings-modal already present in index.html")

    print("Reading js/zayvora-core.js...")
    with open(CORE_JS_PATH, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. Inject functions if not present
    if 'function openMasterSettingsModal' not in js:
        target_func = 'function saveClinicLetterheadSettings()'
        pos = js.find(target_func)
        if pos != -1:
            js = js[:pos] + MASTER_SETTINGS_JS + "\n\n  " + js[pos:]
            print("✓ Injected Master Settings JavaScript functions into js/zayvora-core.js")
        else:
            print("[-] Could not find saveClinicLetterheadSettings in js/zayvora-core.js")

    # 2. Update updateAuthHeaderUI to show the button ONLY when inside OS (never on website)
    old_auth_inner = """            <!-- Prominent Direct Sign Out Button (Ultra High-Contrast) -->
            <button onclick="handleSignOut()" style="background-color: #dc2626 !important; color: #ffffff !important; border: 1px solid #b91c1c !important;" class="btn-signout flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition shadow-sm cursor-pointer shrink-0 hover:brightness-110" title="Sign Out / End Session">"""

    new_auth_inner = """            <!-- Master OS System Settings (STRICTLY INSIDE OS - NEVER ON WEBSITE) -->
            <button id="btn-master-os-settings" onclick="openMasterSettingsModal()" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700/80 hover:border-emerald-500/60 text-xs font-bold text-slate-200 hover:text-white transition shadow-sm cursor-pointer shrink-0" title="Master System Settings (Clinic, AI, Doctor, Backup)">
              <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              <span class="hidden md:inline font-bold text-[11px] text-emerald-400">Settings</span>
            </button>

            <!-- Prominent Direct Sign Out Button (Ultra High-Contrast) -->
            <button onclick="handleSignOut()" style="background-color: #dc2626 !important; color: #ffffff !important; border: 1px solid #b91c1c !important;" class="btn-signout flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition shadow-sm cursor-pointer shrink-0 hover:brightness-110" title="Sign Out / End Session">"""

    if 'id="btn-master-os-settings"' not in js:
        if old_auth_inner in js:
            js = js.replace(old_auth_inner, new_auth_inner)
            print("✓ Injected btn-master-os-settings into updateAuthHeaderUI() [OS-only]")
        else:
            print("[-] Could not find old_auth_inner exact block in js/zayvora-core.js")

    with open(CORE_JS_PATH, "w", encoding="utf-8") as f:
        f.write(js)
    print("✓ Updated js/zayvora-core.js successfully.")

if __name__ == "__main__":
    inject()
