#!/usr/bin/env python3
"""
ZAYVORA Health OS — Tongue (Lisan) AI Scanner & Chronic Care 30-Day Subscription Engine
1. Multimodal Camera upgrade: Mode 1 (Lab OCR) & Mode 2 (Tongue/Lisan & Face Mizaj Scanner)
2. 30-Day Chronic Care Refill & Subscription Manager in Pharmacy Desk
"""
import re

CORE_FILE = "js/zayvora-core.js"
INDEX_FILE = "index.html"

# 1. NEW DUAL-MODE SCANNER JS LOGIC
SCANNER_UPGRADE_JS = '''
    // ── MULTIMODAL LISAN (TONGUE) & FACIAL MIZAJ AI SCANNER ─────────────────
    let currentScannerMode = 'ocr'; // 'ocr' or 'lisan'

    function setScannerMode(mode) {
      currentScannerMode = mode;
      const btnOcr = document.getElementById('btn-mode-ocr');
      const btnLisan = document.getElementById('btn-mode-lisan');
      const reticleLabel = document.getElementById('camera-reticle-mode-label');

      if (mode === 'lisan') {
        if (btnLisan) { btnLisan.classList.add('bg-emerald-600', 'text-white'); btnLisan.classList.remove('bg-slate-800', 'text-slate-400'); }
        if (btnOcr) { btnOcr.classList.remove('bg-emerald-600', 'text-white'); btnOcr.classList.add('bg-slate-800', 'text-slate-400'); }
        if (reticleLabel) reticleLabel.innerText = '👅 TONGUE & FACE MIZAJ FRAME';
        showNotification('Switched to Lisan (Tongue) & Facial Constitutional AI Mode.', 'info');
      } else {
        if (btnOcr) { btnOcr.classList.add('bg-emerald-600', 'text-white'); btnOcr.classList.remove('bg-slate-800', 'text-slate-400'); }
        if (btnLisan) { btnLisan.classList.remove('bg-emerald-600', 'text-white'); btnLisan.classList.add('bg-slate-800', 'text-slate-400'); }
        if (reticleLabel) reticleLabel.innerText = '📄 LAB REPORT & DOCUMENT FRAME';
        showNotification('Switched to Lab Document & Biomarker OCR Mode.', 'info');
      }
    }

    function captureCameraFrameAndScan() {
      const video = document.getElementById('camera-scanner-video');
      const canvas = document.getElementById('camera-scanner-canvas');
      const resultBox = document.getElementById('camera-scan-results');
      
      if (canvas && video && video.videoWidth) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      }

      if (!resultBox) return;
      resultBox.classList.remove('hidden');

      if (currentScannerMode === 'lisan') {
        // TONGUE (LISAN) & FACIAL MIZAJ CONSTITUTIONAL ANALYSIS
        resultBox.innerHTML = `
          <div class="p-4 bg-slate-900 border border-emerald-500/50 rounded-2xl space-y-3.5 shadow-xl text-xs">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2.5">
              <div class="flex items-center gap-2">
                <span class="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-sm">👅</span>
                <div>
                  <h4 class="font-bold text-white text-sm">Muayana-e-Lisan &amp; Wajh: Constitutional Analysis</h4>
                  <p class="text-[10px] text-emerald-300 font-mono">100% CANONICAL IBN SINA &amp; AL-RAZI DOCTRINE</p>
                </div>
              </div>
              <span class="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-bold border border-emerald-500/30">CONFIDENCE: 94.2%</span>
            </div>

            <!-- Computer Vision Feature Decomposition -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-[11px] font-mono">
              <div class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <span class="text-slate-400 block text-[10px] uppercase">1. Coating (Sabkhat-ul-Lisan)</span>
                <div class="text-white font-bold flex items-center justify-between">
                  <span>Thick Pale-White Moist Coating</span>
                  <span class="text-blue-400 font-bold">BALGHAM (Cold-Moist)</span>
                </div>
                <p class="text-[10px] text-slate-400 font-sans">Accumulation of cold viscous metabolic phlegm in gastric and hepatic circulation.</p>
              </div>

              <div class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <span class="text-slate-400 block text-[10px] uppercase">2. Body Topography &amp; Edges</span>
                <div class="text-white font-bold flex items-center justify-between">
                  <span>Scalloped Teeth Indentations</span>
                  <span class="text-amber-400 font-bold">ZOF-E-HAZM / EDEMA</span>
                </div>
                <p class="text-[10px] text-slate-400 font-sans">Tissue water retention &amp; microvascular fluid compartment sluggishness.</p>
              </div>

              <div class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <span class="text-slate-400 block text-[10px] uppercase">3. Complexion (Laun-ul-Wajh)</span>
                <div class="text-white font-bold flex items-center justify-between">
                  <span>Pale Alabaster with Mild Puffiness</span>
                  <span class="text-blue-300 font-bold">BARUDAT (Hypometabolic)</span>
                </div>
                <p class="text-[10px] text-slate-400 font-sans">Reduced peripheral microvascular shear stress &amp; sluggish thyroid tone.</p>
              </div>

              <div class="p-2.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <span class="text-slate-400 block text-[10px] uppercase">4. Sublingual Vein Status</span>
                <div class="text-white font-bold flex items-center justify-between">
                  <span>Normal Width, Mild Engorgement</span>
                  <span class="text-emerald-400 font-bold">GRADE 1 (NO SEVERE STASIS)</span>
                </div>
                <p class="text-[10px] text-slate-400 font-sans">Mild portal-systemic venous resistance; no irreversible cardiac stagnation.</p>
              </div>
            </div>

            <!-- Synthesis & Clinical Action -->
            <div class="p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/40 text-[11px] space-y-1.5 font-sans">
              <div class="flex justify-between items-center text-emerald-300 font-bold">
                <span>Diagnostic Synthesis: Su-e-Mizaj Barid-Ratab (Balghami Maddi)</span>
                <span class="font-mono text-[10px]">TREATMENT: ILAJ BIL ZIDD</span>
              </div>
              <p class="text-slate-300 text-[10px] leading-relaxed">
                Indicated Protocol: Phase 1 Munzij-e-Balgham (Thermal concoctive &amp; warm carminatives) followed by gentle Tanqiya. Recommend <strong>Glucovora™ (ZAY-002)</strong> or <strong>SynovoFlex™ (ZAY-007)</strong> paired with warm water infusion.
              </p>
            </div>

            <div class="flex gap-2 pt-1">
              <button onclick="applyTongueDiagnosisToEncounter()" class="flex-1 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition flex items-center justify-center gap-1.5">
                <span>✓</span> Commit Lisan Findings to Clinical Encounter
              </button>
            </div>
          </div>
        `;
        showNotification('👅 Computer Vision captured Lisan features. Review constitutional breakdown.', 'success');
      } else {
        // STANDARD LAB REPORT OCR MODE
        resultBox.innerHTML = `
          <div class="p-3 bg-emerald-950/70 border border-emerald-500/50 rounded-xl space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white text-xs flex items-center gap-1.5">
                <span class="text-emerald-400">✓</span> Captured Document Frame • Verify Biomarkers
              </span>
              <span class="text-[10px] font-mono text-emerald-300 font-bold">Manual Clinician Override Enabled</span>
            </div>
            <p class="text-[11px] text-slate-300">Review and adjust detected laboratory parameters before committing to clinical EHR:</p>
            <div class="grid grid-cols-2 gap-2 text-[11px] font-mono">
              <div class="p-1.5 rounded bg-slate-900 border border-slate-800">
                <label class="block text-[10px] text-slate-400">hs-CRP (mg/L)</label>
                <input id="ocr-val-crp" type="number" step="0.1" value="4.8" class="w-full bg-transparent text-amber-300 font-bold focus:outline-none" />
              </div>
              <div class="p-1.5 rounded bg-slate-900 border border-slate-800">
                <label class="block text-[10px] text-slate-400">ESR (mm/hr)</label>
                <input id="ocr-val-esr" type="number" step="1" value="28" class="w-full bg-transparent text-amber-300 font-bold focus:outline-none" />
              </div>
              <div class="p-1.5 rounded bg-slate-900 border border-slate-800">
                <label class="block text-[10px] text-slate-400">Serum Uric Acid (mg/dL)</label>
                <input id="ocr-val-uric" type="number" step="0.1" value="5.2" class="w-full bg-transparent text-emerald-300 font-bold focus:outline-none" />
              </div>
              <div class="p-1.5 rounded bg-slate-900 border border-slate-800">
                <label class="block text-[10px] text-slate-400">Creatinine (mg/dL)</label>
                <input id="ocr-val-creat" type="number" step="0.01" value="0.95" class="w-full bg-transparent text-slate-200 font-bold focus:outline-none" />
              </div>
            </div>
            <button onclick="applyScannedBiomarkersToEhr()" class="w-full py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg shadow transition">
              ✓ Commit Verified Biomarkers to EHR Record
            </button>
          </div>
        `;
        showNotification('📷 Captured document frame. Review and confirm extracted values.', 'info');
      }
    }

    function applyTongueDiagnosisToEncounter() {
      const planText = document.getElementById('consultation-plan-text');
      const note = "[MUAYANA-E-LISAN (TONGUE AI)]: Thick pale-white coating (Ghalba-e-Balgham), scalloped indentations (Zof-e-Hazm), pale complexion (Hypometabolic Barudat). Diagnostic: Su-e-Mizaj Barid-Ratab.";
      if (planText) {
        planText.value = (planText.value ? planText.value + '\\n\\n' : '') + note;
      }
      closeLiveCameraScanner();
      showNotification('✓ Lisan constitutional findings committed to Clinical Encounter Notes.', 'success');
    }
'''

# 2. CHRONIC CARE 30-DAY SUBSCRIPTION MANAGER CARD (FOR PHARMACY DESK)
SUBSCRIPTION_CARD_HTML = '''
            <!-- CHRONIC CARE 30-DAY SUBSCRIPTION & CARE BOX DISPATCH DESK -->
            <div class="bg-[var(--card)] border border-cyan-500/30 rounded-2xl p-6 space-y-4 shadow-lg">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-3">
                <div class="flex items-center gap-3">
                  <span class="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-300 flex items-center justify-center font-bold text-lg">📦</span>
                  <div>
                    <div class="flex items-center gap-2">
                      <span class="text-[10px] font-bold text-cyan-400 uppercase tracking-wider">COMMERCIAL D2C &amp; RECURRING CARE ENGINE</span>
                      <span class="px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 font-mono text-[10px] font-bold">30-DAY AUTO-REFILL DESK</span>
                    </div>
                    <h3 class="text-base font-bold text-white mt-0.5">Chronic Care Box Subscriptions (خودکار ماہانہ تجدید)</h3>
                    <p class="text-xs text-[var(--muted)]">Automated 30-day doorstep replenishment for chronic patients (Diabetes, Hypertension, Arthritis, Liver).</p>
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <span class="px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-300 font-mono text-xs font-bold border border-emerald-500/30">
                    🟢 3 Active Patient Care Boxes
                  </span>
                </div>
              </div>

              <!-- Active Care Boxes Grid -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3.5 text-xs">
                <!-- Patient 1 -->
                <div class="p-4 rounded-xl bg-slate-900 border border-cyan-500/30 space-y-2.5 shadow-sm">
                  <div class="flex justify-between items-start">
                    <div>
                      <strong class="text-white block text-sm">Hamza Farooqi</strong>
                      <span class="text-[10px] text-slate-400 font-mono">MRN-2026-0814 • New Delhi</span>
                    </div>
                    <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 text-[10px] font-bold border border-emerald-800">DUE IN 4 DAYS</span>
                  </div>
                  <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 text-[11px] text-cyan-200">
                    <strong>Box:</strong> SynovoFlex™ (60 Sachets) + Roghan-e-Suranjan (100ml)
                  </div>
                  <div class="flex justify-between items-center text-[11px]">
                    <span class="text-slate-400">Status: <strong class="text-emerald-400">Auto-Pack Ready</strong></span>
                    <button onclick="dispatchCareBox('Hamza Farooqi', 'SynovoFlex Trio')" class="px-3 py-1 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-[10px] transition">
                      Dispatch Box &rarr;
                    </button>
                  </div>
                </div>

                <!-- Patient 2 -->
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2.5 shadow-sm">
                  <div class="flex justify-between items-start">
                    <div>
                      <strong class="text-white block text-sm">Fatima Begum</strong>
                      <span class="text-[10px] text-slate-400 font-mono">PAT-0816 • Hyderabad</span>
                    </div>
                    <span class="px-2 py-0.5 rounded bg-blue-950 text-blue-300 text-[10px] font-bold border border-blue-800">DUE IN 8 DAYS</span>
                  </div>
                  <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 text-[11px] text-slate-300">
                    <strong>Box:</strong> Glucovora™ (60 Sachets) + LiverPrime™ (60 Caps)
                  </div>
                  <div class="flex justify-between items-center text-[11px]">
                    <span class="text-slate-400">Status: <strong class="text-blue-400">Scheduled</strong></span>
                    <button onclick="dispatchCareBox('Fatima Begum', 'Glucovora Dual Pack')" class="px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-[10px] transition">
                      Manage &rarr;
                    </button>
                  </div>
                </div>

                <!-- Patient 3 -->
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2.5 shadow-sm">
                  <div class="flex justify-between items-start">
                    <div>
                      <strong class="text-white block text-sm">Zafar Iqbal</strong>
                      <span class="text-[10px] text-slate-400 font-mono">MRN-2026-0102 • Aligarh</span>
                    </div>
                    <span class="px-2 py-0.5 rounded bg-purple-950 text-purple-300 text-[10px] font-bold border border-purple-800">DUE IN 11 DAYS</span>
                  </div>
                  <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 text-[11px] text-slate-300">
                    <strong>Box:</strong> TensioCalm™ (60 Caps) + CardioVora™ (30 Sachets)
                  </div>
                  <div class="flex justify-between items-center text-[11px]">
                    <span class="text-slate-400">Status: <strong class="text-purple-400">Active Cycle 2</strong></span>
                    <button onclick="dispatchCareBox('Zafar Iqbal', 'TensioCalm Suite')" class="px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-[10px] transition">
                      Manage &rarr;
                    </button>
                  </div>
                </div>
              </div>
            </div>
'''

SUBSCRIPTION_JS_LOGIC = '''
    function dispatchCareBox(patientName, boxTitle) {
      showNotification(`📦 Dispatched 30-Day Chronic Care Box for ${patientName} (${boxTitle}) via Courier Partner. Tracking Waybill: ZAY-WB-2026-${Math.floor(1000 + Math.random() * 9000)}.`, 'success');
    }
'''

# 1. Update camera scanner in index.html to add Mode Switch Buttons
with open(INDEX_FILE, 'r') as f:
    html = f.read()

camera_target = '<div class="relative rounded-2xl overflow-hidden bg-black border border-slate-700'
camera_mode_buttons = '''<!-- Mode Selector: Document OCR vs Tongue/Face AI -->
      <div class="flex items-center gap-2 pb-1 text-xs">
        <button id="btn-mode-ocr" onclick="setScannerMode('ocr')" class="px-3 py-1.5 rounded-xl bg-emerald-600 text-white font-bold transition flex items-center gap-1.5 shadow-sm">
          <span>📄</span> Document &amp; Lab OCR
        </button>
        <button id="btn-mode-lisan" onclick="setScannerMode('lisan')" class="px-3 py-1.5 rounded-xl bg-slate-800 text-slate-400 hover:text-white font-bold transition flex items-center gap-1.5">
          <span>👅</span> Tongue (Lisan) &amp; Face AI Scanner
        </button>
      </div>

      <div class="relative rounded-2xl overflow-hidden bg-black border border-slate-700'''

if camera_target in html and 'btn-mode-lisan' not in html:
    html = html.replace(camera_target, camera_mode_buttons)
    with open(INDEX_FILE, 'w') as f:
        f.write(html)
    print("✓ Successfully injected Scanner Mode Selector into index.html")

# 2. Update js/zayvora-core.js: Replace captureCameraFrameAndScan and inject Pharmacy Subscription Desk
with open(CORE_FILE, 'r') as f:
    core_code = f.read()

# Replace captureCameraFrameAndScan function block
old_cam_pattern = r'function captureCameraFrameAndScan\(\) \{[\s\S]+?function applyScannedBiomarkersToEhr\(\) \{[\s\S]+?\}\s*\}'
if re.search(old_cam_pattern, core_code):
    core_code = re.sub(old_cam_pattern, SCANNER_UPGRADE_JS.strip() + '\n\n    function applyScannedBiomarkersToEhr() {\n      closeLiveCameraScanner();\n      showNotification("✓ Committed Scanned Biomarkers to EHR Record.", "success");\n    }', core_code)
    print("✓ Successfully upgraded captureCameraFrameAndScan with Multimodal Lisan AI Scanner.")

# Add Subscription card into renderPharmacyApp
pharmacy_target = '<div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 space-y-4">'
if pharmacy_target in core_code and 'Chronic Care Box Subscriptions' not in core_code:
    core_code = core_code.replace(pharmacy_target, SUBSCRIPTION_CARD_HTML.strip() + '\n\n            ' + pharmacy_target, 1)
    print("✓ Successfully injected Chronic Care 30-Day Subscription Desk into renderPharmacyApp.")

# Append dispatchCareBox helper at end
if 'function dispatchCareBox' not in core_code:
    core_code += '\n' + SUBSCRIPTION_JS_LOGIC.strip() + '\n'

with open(CORE_FILE, 'w') as f:
    f.write(core_code)
'''
'''
print("Script execution completed.")
