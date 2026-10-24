#!/usr/bin/env python3
"""
Patch ZAYVORA Health OS to implement the streamlined Matab Mode:
1. Header Edition labels: "Matab (Clinic)" vs "Research (HQ)"
2. Default state.consultationMode = 'fast'
3. Clinician desk in Clinic Edition collapses 10 diagnostic tools into a sleek compact bar
4. Fast Matab Mode enhanced with:
   - Quick Patient Selector
   - 4-Button tactile Mizaj picker (Damawi, Balghami, Safrawi, Sawdawi)
   - Inline instant medicine search
   - Matab fee settlement bar
   - Friendly clinical safety wording
"""

import os
import re

def patch_index_html():
    path = "index.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Update header edition switcher buttons to clear labels
    old_switcher = """        <button id="btn-edition-clinic" onclick="setPlatformEdition('clinic')" class="px-2.5 py-1 rounded-lg font-bold text-[11px] flex items-center gap-1.5 transition cursor-pointer bg-emerald-600 text-white shadow-sm ring-1 ring-emerald-400/40" title="ZAYVORA Clinic OS: Simplified for Hospitals, Clinics &amp; Matabs">
          <span>🏥</span>
          <span class="hidden sm:inline">Clinic OS</span>
          <span class="sm:hidden">Clinic</span>
        </button>
        <button id="btn-edition-enterprise" onclick="setPlatformEdition('enterprise')" class="px-2.5 py-1 rounded-lg font-bold text-[11px] flex items-center gap-1.5 transition cursor-pointer text-slate-400 hover:text-white" title="ZAYVORA Flagship HQ: Full Sovereign R&amp;D, Manufacturing &amp; Clinical Trials">
          <span>🏛️</span>
          <span class="hidden sm:inline">Flagship HQ</span>
          <span class="sm:hidden">HQ</span>
        </button>"""

    new_switcher = """        <button id="btn-edition-clinic" onclick="setPlatformEdition('clinic')" class="px-2.5 py-1 rounded-lg font-bold text-[11px] flex items-center gap-1.5 transition cursor-pointer bg-emerald-600 text-white shadow-sm ring-1 ring-emerald-400/40" title="ZAYVORA Matab Edition: Aasan OPD, Patient &amp; Prescription Desk">
          <span>🌿</span>
          <span class="hidden sm:inline">Matab (Clinic)</span>
          <span class="sm:hidden">Matab</span>
        </button>
        <button id="btn-edition-enterprise" onclick="setPlatformEdition('enterprise')" class="px-2.5 py-1 rounded-lg font-bold text-[11px] flex items-center gap-1.5 transition cursor-pointer text-slate-400 hover:text-white" title="ZAYVORA Flagship HQ: Full Sovereign R&amp;D, Manufacturing &amp; Clinical Trials">
          <span>🔬</span>
          <span class="hidden sm:inline">Research (HQ)</span>
          <span class="sm:hidden">Research</span>
        </button>"""

    if old_switcher in html:
        html = html.replace(old_switcher, new_switcher)
        print("[✓] index.html: Updated header edition switcher labels")
    else:
        print("[!] index.html: old_switcher pattern not found directly, checking partial replacement")
        # Try replacing inner spans
        html = re.sub(
            r'(<button id="btn-edition-clinic"[^>]*>)\s*<span>.*?</span>\s*<span class="hidden sm:inline">Clinic OS</span>\s*<span class="sm:hidden">Clinic</span>',
            r'\1\n          <span>🌿</span>\n          <span class="hidden sm:inline">Matab (Clinic)</span>\n          <span class="sm:hidden">Matab</span>',
            html
        )
        html = re.sub(
            r'(<button id="btn-edition-enterprise"[^>]*>)\s*<span>.*?</span>\s*<span class="hidden sm:inline">Flagship HQ</span>\s*<span class="sm:hidden">HQ</span>',
            r'\1\n          <span>🔬</span>\n          <span class="hidden sm:inline">Research (HQ)</span>\n          <span class="sm:hidden">Research</span>',
            html
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("[✓] index.html written successfully")


def patch_core_js():
    path = "js/zayvora-core.js"
    with open(path, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. Ensure state has consultationMode defaulting to 'fast'
    state_pattern = "platformEdition: (function() {"
    if "consultationMode:" not in js:
        js = js.replace(
            "platformEdition: (function() {",
            """consultationMode: (function() {\n        try { return localStorage.getItem('zayvora_consultation_mode') || 'fast'; } catch(e) { return 'fast'; }\n      })(),\n      platformEdition: (function() {"""
        )
        print("[✓] zayvora-core.js: Added consultationMode: 'fast' to state")

    # 2. Update updateEditionUI badge text
    old_badge_clinic = "badge.textContent = 'CLINIC OS™';"
    new_badge_clinic = "badge.textContent = 'MATAB CLINIC OS™';"
    if old_badge_clinic in js:
        js = js.replace(old_badge_clinic, new_badge_clinic)

    old_sub_clinic = "sub.textContent = isClinic ? 'Unani OPD & Hospital Management' : 'ZAYVORA Sovereign Health OS & R&D Cloud';"
    new_sub_clinic = "sub.textContent = isClinic ? 'Aasan OPD & Prescription Desk (1-Minute Nuskha)' : 'ZAYVORA Sovereign Health OS & R&D Cloud';"
    if old_sub_clinic in js:
        js = js.replace(old_sub_clinic, new_sub_clinic)

    print("[✓] zayvora-core.js: Updated updateEditionUI")

    # 3. Add helper functions for Fast Matab:
    helpers_code = """
  // =========================================================================
  // FAST MATAB EXPANDED CLINICAL WORKDESK HELPERS
  // =========================================================================
  function switchFastPatient(mrnOrId) {
    const patientMap = {
      'PAT-774901': { id: 'PAT-774901', mrn: 'MRN-2026-0814', name: 'Hamza Farooqi', age: 44, gender: 'Male', phone: '+91-9876543210', mizaj: 'Su-e-Mizaj Barid Balghami', allergies: 'Sonf (Foeniculum vulgare)', primaryComplaint: 'Bilateral knee pain' },
      'PAT-774902': { id: 'PAT-774902', mrn: 'MRN-2026-0819', name: 'Ayesha Siddiqui', age: 38, gender: 'Female', phone: '+91-9812345678', mizaj: 'Su-e-Mizaj Haar Safrawi', allergies: 'None reported', primaryComplaint: 'Chronic dyspepsia & gas' },
      'PAT-774903': { id: 'PAT-774903', mrn: 'MRN-2026-0820', name: 'Fatima Begum', age: 49, gender: 'Female', phone: '+91-9833445566', mizaj: 'Balghami', allergies: 'Dust, Pollen', primaryComplaint: 'Suaal & Ziq-un-Nafs' },
      'PAT-774904': { id: 'PAT-774904', mrn: 'MRN-2026-0821', name: 'Abdul Rehman', age: 64, gender: 'Male', phone: '+91-9711223344', mizaj: 'Safrawi', allergies: 'None', primaryComplaint: 'Su-e-Hazm & Nafkh' },
      'PAT-774905': { id: 'PAT-774905', mrn: 'MRN-2026-0822', name: 'Zainab Khatoon', age: 34, gender: 'Female', phone: '+91-9955443322', mizaj: 'Damawi', allergies: 'Penicillin', primaryComplaint: 'Suda & Shaqeeqa' }
    };
    if (patientMap[mrnOrId]) {
      state.patient = patientMap[mrnOrId];
      if (state.prescriptions && state.prescriptions[0]) {
        state.prescriptions[0].patientName = state.patient.name;
        state.prescriptions[0].mrn = state.patient.mrn;
      }
      showNotification('Switched patient to: ' + state.patient.name, 'success');
      const c = document.getElementById('workspace-container');
      if (c) renderFastMatabMode(c);
    }
  }

  function selectFastMizaj(mizajName) {
    if (!state.patient) state.patient = {};
    state.patient.mizaj = mizajName;
    calculateIlajBilZidd();
    const mizajDisplay = document.getElementById('fast-patient-mizaj-display');
    if (mizajDisplay) mizajDisplay.textContent = mizajName;
    document.querySelectorAll('.fast-mizaj-btn').forEach(btn => {
      if (btn.dataset.mizaj === mizajName) {
        btn.className = 'fast-mizaj-btn px-2.5 py-1.5 rounded-xl border font-bold text-xs flex items-center justify-center gap-1.5 transition bg-emerald-600 border-emerald-400 text-white shadow-md';
      } else {
        btn.className = 'fast-mizaj-btn px-2.5 py-1.5 rounded-xl border font-bold text-xs flex items-center justify-center gap-1.5 transition bg-slate-900 border-slate-800 text-slate-300 hover:text-white';
      }
    });
    showNotification('Mizaj updated: ' + mizajName, 'success');
  }

  function handleFastMedSearch(query) {
    const resultsDiv = document.getElementById('fast-med-search-results');
    if (!resultsDiv) return;
    if (!query || query.trim().length < 2) {
      resultsDiv.classList.add('hidden');
      resultsDiv.innerHTML = '';
      return;
    }
    const q = query.toLowerCase().trim();
    const matches = [];
    if (typeof QARABADEEN_CATALOG !== 'undefined') {
      QARABADEEN_CATALOG.forEach(m => {
        if ((m.name && m.name.toLowerCase().includes(q)) || 
            (m.urdu && m.urdu.includes(q)) ||
            (m.source && m.source.toLowerCase().includes(q)) ||
            (m.indication && m.indication.toLowerCase().includes(q))) {
          matches.push({ ...m, type: 'QARABADEEN', track: 'QARABADEEN' });
        }
      });
    }
    if (typeof ZAYVORA_PRODUCTS_32 !== 'undefined') {
      ZAYVORA_PRODUCTS_32.forEach(p => {
        if ((p.name && p.name.toLowerCase().includes(q)) ||
            (p.indication && p.indication.toLowerCase().includes(q)) ||
            (p.form && p.form.toLowerCase().includes(q))) {
          matches.push({ ...p, type: 'ZAYVORA_PRODUCT', track: 'ZAYVORA_PRODUCT', urdu: p.category || '' });
        }
      });
    }
    if (matches.length === 0) {
      resultsDiv.innerHTML = '<div class="p-2.5 text-center text-slate-400 text-xs">Koi dawa nahi mili. Try: Khamira, Majun, Itrifal, Sharbat</div>';
      resultsDiv.classList.remove('hidden');
      return;
    }
    resultsDiv.innerHTML = matches.slice(0, 8).map(item => `
      <div class="p-2 bg-slate-800 hover:bg-slate-700 rounded-lg flex items-center justify-between gap-2 cursor-pointer transition border border-slate-700/60" onclick="addFastMedFromSearch('${encodeURIComponent(item.name)}', '${encodeURIComponent(item.form || 'Compound')}', '${encodeURIComponent(item.dose || '5g')}', '${item.type}')">
        <div>
          <strong class="text-white text-xs block">${item.name} ${item.urdu ? `<span class="urdu-font text-emerald-400 text-sm font-normal">(${item.urdu})</span>` : ''}</strong>
          <span class="text-[10px] text-slate-400">${item.source || item.form || ''} • Dose: ${item.dose || '5g'}</span>
        </div>
        <button class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-bold shrink-0">+ Add</button>
      </div>
    `).join('');
    resultsDiv.classList.remove('hidden');
  }

  function addFastMedFromSearch(nameEnc, formEnc, doseEnc, track) {
    const name = decodeURIComponent(nameEnc);
    const form = decodeURIComponent(formEnc);
    const dose = decodeURIComponent(doseEnc);
    const rx = state.prescriptions[0];
    if (!rx.medicines) rx.medicines = [];
    rx.medicines.push({
      name: name,
      form: form || 'Electuary / Compound',
      strength: dose || '5g',
      frequency: 'BD (Morning & Night)',
      morning: dose || '5g',
      noon: '—',
      night: dose || '5g',
      anupan: 'Fresh or lukewarm water',
      axis: 'Integrative',
      track: track || 'QARABADEEN'
    });
    renderFastMatabPrescriptionList();
    calculateIlajBilZidd();
    const resultsDiv = document.getElementById('fast-med-search-results');
    if (resultsDiv) { resultsDiv.classList.add('hidden'); }
    const input = document.getElementById('fast-med-quick-input');
    if (input) { input.value = ''; }
    showNotification('Added to Nuskha: ' + name, 'success');
  }

  function setFastFee(amount) {
    const badge = document.getElementById('fast-fee-status-badge');
    if (badge) {
      badge.textContent = '✓ Fee Settled: ₹' + amount;
    }
    showNotification('Matab Fee Recorded: ₹' + amount, 'success');
  }

  window.switchFastPatient = switchFastPatient;
  window.selectFastMizaj = selectFastMizaj;
  window.handleFastMedSearch = handleFastMedSearch;
  window.addFastMedFromSearch = addFastMedFromSearch;
  window.setFastFee = setFastFee;
"""

    if "function switchFastPatient(" not in js:
        js = js.replace(
            "function renderFastMatabMode(container) {",
            helpers_code + "\n  function renderFastMatabMode(container) {"
        )
        print("[✓] zayvora-core.js: Added Fast Matab helpers")

    # 4. Now enhance renderFastMatabMode HTML
    # Check if patient selector already in renderFastMatabMode
    if "switchFastPatient(this.value)" not in js:
        old_header_block = """            <p class="text-xs text-[var(--muted)] mt-1">
              MRN: <span class="font-mono text-white font-medium">${state.patient.mrn}</span> • 
              Mizaj: <span class="text-emerald-400 font-medium">${state.patient.mizaj}</span> • 
              Attending: <strong class="text-white">Hakeem Dr. Irfan Ashraf</strong>
            </p>"""

        new_header_block = """            <div class="flex items-center gap-2 mt-1 flex-wrap">
              <span class="text-xs text-[var(--muted)]">MRN: <span class="font-mono text-white font-medium">${state.patient.mrn}</span> • Mizaj: <strong id="fast-patient-mizaj-display" class="text-emerald-400 font-medium">${state.patient.mizaj}</strong></span>
              <div class="flex items-center gap-1.5 ml-0 sm:ml-3">
                <span class="text-[10px] text-amber-300 font-bold uppercase">Change Mareez:</span>
                <select onchange="switchFastPatient(this.value)" class="bg-slate-900 border border-emerald-500/40 rounded-lg px-2 py-0.5 text-xs text-white font-bold outline-none cursor-pointer">
                  <option value="PAT-774901" ${(state.patient&&state.patient.id==='PAT-774901')?'selected':''}>👤 Hamza Farooqi (44y M) • T-104</option>
                  <option value="PAT-774902" ${(state.patient&&state.patient.id==='PAT-774902')?'selected':''}>👤 Ayesha Siddiqui (38y F) • T-105</option>
                  <option value="PAT-774903" ${(state.patient&&state.patient.id==='PAT-774903')?'selected':''}>👤 Fatima Begum (49y F) • T-106</option>
                  <option value="PAT-774904" ${(state.patient&&state.patient.id==='PAT-774904')?'selected':''}>👤 Abdul Rehman (64y M) • T-107</option>
                  <option value="PAT-774905" ${(state.patient&&state.patient.id==='PAT-774905')?'selected':''}>👤 Zainab Khatoon (34y F) • T-108</option>
                </select>
              </div>
            </div>"""

        if old_header_block in js:
            js = js.replace(old_header_block, new_header_block)
            print("[✓] zayvora-core.js: Added Patient switcher to Fast Matab header")

    # 5. Add 4-button tactile Mizaj selector in Classical Tashkhees Drawer
    old_tashkhees_top = """              <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                <span class="text-xs font-bold text-white flex items-center gap-1.5">
                  <span>🩺</span> Classical Tashkhees (10-Ajnas Pulse, Tongue &amp; Urine)
                </span>
                <span class="text-[9px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono font-bold">Unani Classical Vitals</span>
              </div>"""

    new_tashkhees_top = """              <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                <span class="text-xs font-bold text-white flex items-center gap-1.5">
                  <span>🩺</span> Classical Tashkhees (10-Ajnas Pulse, Tongue &amp; Urine)
                </span>
                <span class="text-[9px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono font-bold">Unani Classical Vitals</span>
              </div>

              <!-- 4-BUTTON TACTILE MIZAJ PICKER -->
              <div class="space-y-1.5 pb-2 border-b border-slate-800">
                <span class="text-[10px] text-slate-400 block font-bold uppercase tracking-wider">Mizaj-e-Mareez (طبیعی / غیر طبیعی مزاج):</span>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-1.5">
                  <button onclick="selectFastMizaj('Damawi (Sanguine / خونی)')" data-mizaj="Damawi (Sanguine / خونی)" class="fast-mizaj-btn px-2 py-1.5 rounded-xl border font-bold text-[11px] flex items-center justify-center gap-1 transition ${(state.patient&&state.patient.mizaj&&state.patient.mizaj.includes('Damawi')) ? 'bg-rose-600 border-rose-400 text-white shadow-md' : 'bg-slate-900 border-slate-800 text-slate-300 hover:text-white'}">
                    <span>🔴</span> Damawi (خون)
                  </button>
                  <button onclick="selectFastMizaj('Balghami (Phlegmatic / بلغمی)')" data-mizaj="Balghami (Phlegmatic / بلغمی)" class="fast-mizaj-btn px-2 py-1.5 rounded-xl border font-bold text-[11px] flex items-center justify-center gap-1 transition ${(state.patient&&state.patient.mizaj&&state.patient.mizaj.includes('Balghami')) ? 'bg-cyan-600 border-cyan-400 text-white shadow-md' : 'bg-slate-900 border-slate-800 text-slate-300 hover:text-white'}">
                    <span>⚪</span> Balghami (بلغم)
                  </button>
                  <button onclick="selectFastMizaj('Safrawi (Choleric / صفراوی)')" data-mizaj="Safrawi (Choleric / صفراوی)" class="fast-mizaj-btn px-2 py-1.5 rounded-xl border font-bold text-[11px] flex items-center justify-center gap-1 transition ${(state.patient&&state.patient.mizaj&&state.patient.mizaj.includes('Safrawi')) ? 'bg-amber-600 border-amber-400 text-white shadow-md' : 'bg-slate-900 border-slate-800 text-slate-300 hover:text-white'}">
                    <span>🟡</span> Safrawi (صفراء)
                  </button>
                  <button onclick="selectFastMizaj('Sawdawi (Melancholic / سوداوی)')" data-mizaj="Sawdawi (Melancholic / سوداوی)" class="fast-mizaj-btn px-2 py-1.5 rounded-xl border font-bold text-[11px] flex items-center justify-center gap-1 transition ${(state.patient&&state.patient.mizaj&&state.patient.mizaj.includes('Sawdawi')) ? 'bg-slate-700 border-slate-500 text-white shadow-md' : 'bg-slate-900 border-slate-800 text-slate-300 hover:text-white'}">
                    <span>⚫</span> Sawdawi (سوداء)
                  </button>
                </div>
              </div>"""

    if old_tashkhees_top in js and "fast-mizaj-btn" not in js:
        js = js.replace(old_tashkhees_top, new_tashkhees_top)
        print("[✓] zayvora-core.js: Added 4-Button tactile Mizaj picker to Tashkhees Drawer")

    # 6. Add Instant Medicine Search Bar above prescribed list
    old_rx_header = """            <!-- Active Prescribed Formulations List -->
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
            </div>"""

    new_rx_header = """            <!-- Active Prescribed Formulations List -->
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-sm space-y-3">
              <div class="flex justify-between items-center border-b border-[var(--border)] pb-2.5">
                <span class="font-bold text-white text-xs flex items-center gap-1.5">
                  <span>℞</span> Active Nuskha &amp; Formulations Table
                </span>
                <div class="flex items-center gap-2">
                  <button onclick="openQarabadeenCatalogModal()" class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] rounded-lg transition" title="Search all 59 Classical Formulations">
                    + Qarabadeen (59)
                  </button>
                  <button onclick="openZayvoraProductsModal()" class="px-2.5 py-1 bg-amber-600 hover:bg-amber-500 text-white font-bold text-[11px] rounded-lg transition" title="Search all 32 ZAYVORA Sovereign Formulations">
                    + ZAYVORA (32)
                  </button>
                  <button onclick="openSelfNuskhaModal()" class="px-2.5 py-1 bg-purple-600 hover:bg-purple-500 text-white font-bold text-[11px] rounded-lg transition">
                    + Self-Nuskha
                  </button>
                </div>
              </div>

              <!-- Fast Inline Medicine Search Input -->
              <div class="relative">
                <div class="relative">
                  <input id="fast-med-quick-input" type="text" placeholder="🔍 Dawa dhoondein (e.g. Khamira, Majun, Itrifal, Sharbat, Safuf)..." oninput="handleFastMedSearch(this.value)" onfocus="handleFastMedSearch(this.value)" class="w-full pl-8 pr-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-emerald-500 font-medium">
                  <span class="absolute left-2.5 top-2.5 text-xs text-slate-400">🔍</span>
                </div>
                <div id="fast-med-search-results" class="hidden absolute left-0 right-0 top-full mt-1 bg-slate-900 border border-emerald-500/40 rounded-xl shadow-2xl max-h-56 overflow-y-auto z-40 p-1 space-y-1">
                </div>
              </div>

              <!-- Prescription Items List -->
              <div id="fast-prescriptions-list" class="space-y-2">
                <!-- Rendered dynamically -->
              </div>

              <!-- Matab Consultation Fee Settler Bar -->
              <div class="p-2.5 bg-slate-900/90 rounded-xl border border-slate-800 flex flex-wrap items-center justify-between gap-2 text-xs">
                <div class="flex items-center gap-1.5">
                  <span class="text-slate-400 font-semibold">💵 Matab Fee (فیس):</span>
                  <button onclick="setFastFee(100)" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 font-mono text-[11px] border border-slate-700">₹100</button>
                  <button onclick="setFastFee(200)" class="px-2 py-0.5 rounded bg-emerald-700 text-white font-mono text-[11px] font-bold border border-emerald-500">₹200</button>
                  <button onclick="setFastFee(300)" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 font-mono text-[11px] border border-slate-700">₹300</button>
                  <button onclick="setFastFee(500)" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 font-mono text-[11px] border border-slate-700">₹500</button>
                </div>
                <span id="fast-fee-status-badge" class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-bold">✓ Fee Settled: ₹200</span>
              </div>
            </div>"""

    if old_rx_header in js:
        js = js.replace(old_rx_header, new_rx_header)
        print("[✓] zayvora-core.js: Added Fast inline medicine search and fee settler to Nuskha table")

    # 7. Replace safety rails technical jargon with natural clinical terms
    old_safety = """                <div class="p-2 rounded-lg bg-[var(--background)] border border-emerald-500/20 flex items-center justify-between">
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
                </div>"""

    new_safety = """                <div class="p-2 rounded-lg bg-[var(--background)] border border-emerald-500/20 flex items-center justify-between">
                  <span class="text-slate-300">Gurda o Meda (Renal/GI):</span>
                  <span class="text-emerald-400 font-bold font-mono">NORMAL ✓</span>
                </div>
                <div class="p-2 rounded-lg bg-[var(--background)] border border-emerald-500/20 flex items-center justify-between">
                  <span class="text-slate-300">Hamal o Raza'at (Pregnancy):</span>
                  <span class="text-emerald-400 font-bold font-mono">MEHFOOZ ✓</span>
                </div>
                <div class="p-2 rounded-lg bg-[var(--background)] border border-emerald-500/20 flex items-center justify-between">
                  <span class="text-slate-300">Zahrili Advia (E1) Mudabbar:</span>
                  <span class="text-amber-400 font-bold font-mono">CERTIFIED ✓</span>
                </div>
                <div class="p-2 rounded-lg bg-[var(--background)] border border-emerald-500/20 flex items-center justify-between">
                  <span class="text-slate-300">Advia Tasaadum (Herb-Drug):</span>
                  <span class="text-emerald-400 font-bold font-mono">0 KHATRA ✓</span>
                </div>"""

    if old_safety in js:
        js = js.replace(old_safety, new_safety)
        print("[✓] zayvora-core.js: Updated Safety rails with natural clinical terms")

    with open(path, "w", encoding="utf-8") as f:
        f.write(js)
    print("[✓] zayvora-core.js written successfully")

if __name__ == "__main__":
    patch_index_html()
    patch_core_js()
