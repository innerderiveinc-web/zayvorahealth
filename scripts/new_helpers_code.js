
    // =========================================================================
    // PRODUCTION INTERACTIVE MODAL CONTROLLERS & LOGIC
    // =========================================================================

    // 1. Global Search Modal (⌘K)
    function toggleSearchModal() {
      const m = document.getElementById('search-modal');
      m.classList.toggle('hidden');
      if (!m.classList.contains('hidden')) {
        setTimeout(() => document.getElementById('global-search-input').focus(), 50);
        handleGlobalSearch('');
      }
    }

    function handleGlobalSearch(query) {
      const q = (query || '').toLowerCase().trim();
      const resContainer = document.getElementById('global-search-results');
      
      const searchItems = [
        { title: 'Hamza Farooqi', category: 'Patient (MRN-2026-0814)', type: 'patient', action: () => { switchRole('doctor'); switchTab('today'); toggleSearchModal(); } },
        { title: 'Ayesha Siddiqui', category: 'Patient (MRN-2026-0819)', type: 'patient', action: () => { switchRole('doctor'); switchTab('today'); toggleSearchModal(); } },
        { title: 'Majun Suranjan (Mudabbar)', category: 'Medication (Schedule E1)', type: 'medicine', action: () => { switchRole('pharmacy'); switchTab('fefo'); toggleSearchModal(); } },
        { title: 'Raughan-e-Balsan', category: 'Medication (Analgesic Oil)', type: 'medicine', action: () => { switchRole('pharmacy'); switchTab('fefo'); toggleSearchModal(); } },
        { title: 'MetaboCore Elite', category: 'Product (Glycemic Regulator)', type: 'medicine', action: () => { viewWebsitePage('products'); toggleSearchModal(); } },
        { title: '12-Stage Closed-Loop Continuum', category: 'Clinical Protocol', type: 'protocol', action: () => { viewWebsitePage('care_journey'); toggleSearchModal(); } },
        { title: '4-Stage Afaal Treatment Cascade', category: 'Humoral Protocol', type: 'protocol', action: () => { viewWebsitePage('philosophy'); toggleSearchModal(); } },
        { title: 'ZAYVORA Healthcare System - Central Hospital', category: 'Facility Location', type: 'page', action: () => { viewWebsitePage('clinics'); toggleSearchModal(); } },
        { title: 'About ZAYVORA Health OS', category: 'Public Page', type: 'page', action: () => { viewWebsitePage('about'); toggleSearchModal(); } },
        { title: 'Clinical Services', category: 'Public Page', type: 'page', action: () => { viewWebsitePage('services'); toggleSearchModal(); } },
        { title: 'Research & RWE Evidence', category: 'Public Page', type: 'page', action: () => { viewWebsitePage('research'); toggleSearchModal(); } },
        { title: 'Contact & Concierge (+91 97738 82657)', category: 'Public Page', type: 'page', action: () => { viewWebsitePage('contact'); toggleSearchModal(); } },
        { title: 'Patient FAQs & ABHA Guide', category: 'Public Page', type: 'page', action: () => { viewWebsitePage('faqs'); toggleSearchModal(); } }
      ];

      const matches = q ? searchItems.filter(i => i.title.toLowerCase().includes(q) || i.category.toLowerCase().includes(q)) : searchItems.slice(0, 7);

      if (matches.length === 0) {
        resContainer.innerHTML = '<p class="text-slate-500 text-center py-4">No matching records found.</p>';
        return;
      }

      resContainer.innerHTML = matches.map((m, idx) => `
        <div onclick="window.__searchActions[${idx}]()" class="p-2.5 rounded-xl bg-[var(--background)] hover:bg-slate-800 border border-[var(--border)] cursor-pointer flex justify-between items-center transition">
          <div>
            <span class="font-bold text-white text-xs">${m.title}</span>
            <span class="text-[10px] text-[var(--muted)] block">${m.category}</span>
          </div>
          <span class="text-[10px] text-emerald-400 font-mono">Jump ↗</span>
        </div>
      `).join('');

      window.__searchActions = matches.map(m => m.action);
    }

    // 2. Clinical Notifications Center
    function toggleNotificationsModal() {
      const m = document.getElementById('notifications-modal');
      m.classList.toggle('hidden');
      if (!m.classList.contains('hidden')) {
        renderDrawerAlerts();
      }
    }

    function renderDrawerAlerts() {
      const c = document.getElementById('drawer-alerts-list');
      const countBadge = document.getElementById('drawer-notif-count');
      const headerBadge = document.getElementById('header-notif-badge');
      
      const unread = state.alerts.filter(a => !a.acknowledged);
      if (countBadge) countBadge.innerText = `${unread.length} Active`;
      if (headerBadge) {
        headerBadge.innerText = unread.length;
        if (unread.length === 0) headerBadge.classList.add('hidden');
        else headerBadge.classList.remove('hidden');
      }

      if (state.alerts.length === 0) {
        c.innerHTML = '<p class="text-slate-500 text-center py-4 text-xs">No alerts.</p>';
        return;
      }

      c.innerHTML = state.alerts.map(a => `
        <div class="p-3 rounded-xl border text-xs space-y-1.5 ${a.acknowledged ? 'bg-slate-900/40 border-[var(--border)] opacity-60' : 'bg-rose-950/20 border-rose-500/30'}">
          <div class="flex justify-between items-center">
            <span class="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded ${a.level === 'CRITICAL' ? 'bg-rose-500/20 text-rose-300' : a.level === 'LAB' ? 'bg-amber-500/20 text-amber-300' : 'bg-blue-500/20 text-blue-300'}">${a.level}</span>
            ${!a.acknowledged ? `<button onclick="acknowledgeAlert('${a.id}')" class="px-2 py-0.5 rounded bg-emerald-600/30 hover:bg-emerald-600 text-emerald-300 text-[10px] font-bold transition">Acknowledge</button>` : `<span class="text-[9px] text-emerald-400 font-bold">✓ Signed</span>`}
          </div>
          <h4 class="font-bold text-white text-xs">${a.title}</h4>
          <p class="text-[10px] text-slate-300 leading-relaxed">${a.desc}</p>
        </div>
      `).join('');
    }

    function acknowledgeAlert(id) {
      const a = state.alerts.find(item => item.id === id);
      if (a) a.acknowledged = true;
      renderDrawerAlerts();
      showNotification(`Alert ${id} acknowledged and logged to clinical audit trail.`, 'success');
    }

    function markAllAlertsRead() {
      state.alerts.forEach(a => a.acknowledged = true);
      renderDrawerAlerts();
      showNotification('All clinical alerts acknowledged.', 'success');
    }

    // 3. Register New Patient Modal
    function toggleAddPatientModal() {
      const m = document.getElementById('add-patient-modal');
      m.classList.toggle('hidden');
    }
    function openAddPatientModal() {
      toggleAddPatientModal();
    }

    function handleRegisterNewPatient(e) {
      e.preventDefault();
      const name = document.getElementById('new-pat-name').value;
      const age = document.getElementById('new-pat-age').value;
      const gender = document.getElementById('new-pat-gender').value;
      const phone = document.getElementById('new-pat-phone').value;
      const complaint = document.getElementById('new-pat-complaint').value;
      const mizaj = document.getElementById('new-pat-mizaj').value;

      const mrn = `MRN-2026-${Math.floor(1000 + Math.random() * 9000)}`;
      const token = `T-${100 + state.appointments.length + 1}`;

      state.patient = {
        id: `PAT-${Date.now().toString().slice(-6)}`,
        mrn,
        name,
        age: parseInt(age),
        gender,
        phone,
        email: `${name.toLowerCase().replace(/\s+/g, '.')}@patient.zayvora.com`,
        allergies: 'None recorded',
        mizaj,
        primaryComplaint: complaint
      };

      state.appointments.push({
        id: `APT-${Date.now().toString().slice(-4)}`,
        token,
        patientName: name,
        mrn,
        doctorName: 'Hakim Dr. Tariq Mansoor',
        scheduledTime: 'Today, OPD Queue',
        type: 'General Integrative OPD',
        complaint,
        status: `Waiting with Token ${token}`
      });

      toggleAddPatientModal();
      showNotification(`Patient ${name} registered! Token ${token} issued. Admitted to Room 204.`, 'success');
      switchRole('doctor');
      switchTab('today');
    }

    // 4. Clinical Report & COA Modal
    function toggleReportModal() {
      const m = document.getElementById('report-modal');
      m.classList.toggle('hidden');
    }

    function openReportModal() {
      const c = document.getElementById('report-modal-content');
      c.innerHTML = `
        <div class="space-y-4">
          <div class="border-b border-[var(--border)] pb-3 flex justify-between items-start">
            <div>
              <h2 class="text-base font-bold text-white">ZAYVORA Healthcare System - Central Hospital</h2>
              <p class="text-[10px] text-[var(--muted)]">National Institute of Integrative Greco-Arab Medicine • New Delhi Institutional Area</p>
              <p class="text-[10px] text-emerald-400 font-mono">Emergency & Concierge: +91 97738 82657</p>
            </div>
            <div class="text-right text-[10px] font-mono text-slate-400">
              <div>Encounter: <strong class="text-white">${state.encounterId}</strong></div>
              <div>Date: ${new Date().toLocaleDateString('en-GB')}</div>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2 text-[11px] p-3 rounded-lg bg-slate-900 border border-[var(--border)]">
            <div><strong class="text-slate-400">Patient:</strong> <span class="text-white font-semibold">${state.patient.name}</span> (${state.patient.age}y / ${state.patient.gender})</div>
            <div><strong class="text-slate-400">MRN:</strong> <span class="text-emerald-400 font-mono">${state.patient.mrn}</span></div>
            <div><strong class="text-slate-400">Constitutional Mizaj:</strong> <span class="text-white">${state.patient.mizaj}</span></div>
            <div><strong class="text-slate-400">Active Afaal Stage:</strong> <span class="text-teal-400 font-bold">${state.afaalStage} (${state.afaalDays} Days)</span></div>
          </div>

          <div class="space-y-2">
            <h4 class="font-bold text-white text-xs">Prescribed Unani Formulations</h4>
            <div class="p-3 rounded-lg bg-slate-900 border border-[var(--border)] space-y-1.5 text-[11px]">
              <div>1. <strong>Majun Suranjan</strong> — 5g twice daily with warm water (Schedule E1 Mudabbar)</div>
              <div>2. <strong>Raughan-e-Balsan</strong> — Bedtime local application with warm fomentation</div>
            </div>
          </div>

          <div class="p-3 rounded-lg bg-emerald-950/40 border border-emerald-500/40 text-[10px] space-y-1">
            <div class="flex justify-between items-center text-emerald-400 font-mono font-bold">
              <span>🔒 21 CFR Part 11 Electronic Signature Verified</span>
              <span>HMAC-SHA256: e8b94a02c...</span>
            </div>
            <div class="text-slate-300">Signatory: Hakim Dr. Tariq Mansoor (Senior Tabeeb, Reg. AYUSH-DL-0881)</div>
          </div>
        </div>
      `;
      toggleReportModal();
    }

    function openCoaModal(batchId) {
      const c = document.getElementById('report-modal-content');
      c.innerHTML = `
        <div class="space-y-4">
          <div class="border-b border-[var(--border)] pb-3 flex justify-between items-start">
            <div>
              <h2 class="text-base font-bold text-white">Certificate of Analysis (COA)</h2>
              <p class="text-[10px] text-[var(--muted)]">ZAYVORA AYUSH GMP Certified Botanical Manufacturing Facility</p>
            </div>
            <span class="px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-300 font-mono font-bold text-xs">PASSED & RELEASED</span>
          </div>

          <div class="grid grid-cols-2 gap-2 text-[11px] p-3 rounded-lg bg-slate-900 border border-[var(--border)]">
            <div><strong class="text-slate-400">Batch Number:</strong> <span class="text-white font-mono font-bold">${batchId || 'BMR-2026-MVP-09'}</span></div>
            <div><strong class="text-slate-400">Product:</strong> ManiVital Pro Granules (150g)</div>
            <div><strong class="text-slate-400">Manufacture Date:</strong> 2026-08-20</div>
            <div><strong class="text-slate-400">Expiry Date (FEFO):</strong> 2028-08-19</div>
          </div>

          <div class="space-y-2 text-[11px]">
            <h4 class="font-bold text-white text-xs">Standardized Physicochemical Specifications</h4>
            <div class="divide-y divide-[var(--border)] bg-slate-900 p-3 rounded-lg border border-[var(--border)]">
              <div class="py-1 flex justify-between"><span>Withanolide Content (HPLC):</span><strong class="text-emerald-400">2.82% (Spec: &gt;2.5%)</strong></div>
              <div class="py-1 flex justify-between"><span>Heavy Metals (Pb, Cd, As, Hg):</span><strong class="text-emerald-400">&lt; 0.05 ppm (Passed)</strong></div>
              <div class="py-1 flex justify-between"><span>Microbial Limits (Total Viable Count):</span><strong class="text-emerald-400">&lt; 10 CFU/g (Sterile)</strong></div>
              <div class="py-1 flex justify-between"><span>Pesticide Residue (GC-MS):</span><strong class="text-emerald-400">Not Detected (Safe)</strong></div>
            </div>
          </div>

          <div class="p-3 rounded-lg bg-emerald-950/40 border border-emerald-500/40 text-[10px] space-y-1">
            <div class="flex justify-between items-center text-emerald-400 font-mono font-bold">
              <span>Authorized Quality Release</span>
              <span>Dr. Arshad Qureshi, Head QC</span>
            </div>
          </div>
        </div>
      `;
      toggleReportModal();
    }

    // 5. Language Switcher
    function switchLanguage(lang) {
      state.lang = lang;
      ['en', 'hi', 'ur'].forEach(l => {
        const btn = document.getElementById(`lang-btn-${l}`);
        if (btn) {
          if (l === lang) {
            btn.className = 'px-2 py-0.5 rounded-lg bg-[var(--card)] text-[#2DD4BF]';
          } else {
            btn.className = 'px-2 py-0.5 rounded-lg text-[var(--muted)] hover:text-white';
          }
        }
      });
      const greetings = {
        en: 'Language set to English (EN)',
        hi: 'भाषा बदलकर हिन्दी कर दी गई (HI)',
        ur: 'زبان اردو منتخب کی گئی (UR)'
      };
      showNotification(greetings[lang] || 'Language updated', 'info');
    }

    // 6. Live Hakeem Sahab AI Copilot
    function focusAiCopilot() {
      const input = document.getElementById('ai-quick-input');
      if (input) {
        input.focus();
        input.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else {
        switchTab('today');
      }
    }

    function askHakeemAI(promptQuery) {
      const inputEl = document.getElementById('ai-quick-input');
      const query = (promptQuery || (inputEl ? inputEl.value : '')).trim();
      const resBox = document.getElementById('hakeem-ai-response-box');
      if (!query) {
        if (inputEl) inputEl.focus();
        return;
      }

      let answer = "";
      if (query.toLowerCase().includes('hamza') || query.toLowerCase().includes('dyscrasia')) {
        answer = "Patient Hamza Farooqi presents with Barid Balghami Su-e-Mizaj affecting the bilateral knee articular axis. Recommended protocol: 14-day Tanqiya with Munzij-e-Balgham decoction, warm fomentation (Natool), and Majun Suranjan Mudabbar. Avoid cold/moist dietary intake.";
      } else if (query.toLowerCase().includes('protocol') || query.toLowerCase().includes('tanqiya')) {
        answer = "Tanqiya Protocol Stage 1: Munzij-e-Balgham (Gul-e-Banafsha 5g, Tukhm-e-Khatmi 5g, Mavez Munaqqa 7 nos.) boiled in 250ml water until reduced to 100ml. Administer for 7 days followed by Hijama Bila Shart on day 8.";
      } else if (query.toLowerCase().includes('suranjan') || query.toLowerCase().includes('interaction')) {
        answer = "Colchicum autumnale (Suranjan Talkh) interaction profile: Safe when detoxified (Mudabbar) in cow milk. Potential potentiation with loop diuretics. Mandatory corrective (Musleh): Kateera (Astragalus gummifer) or Shakar Safaid.";
      } else {
        answer = `Clinical reasoning for "${query}": Correlated with UPI Vol. II codified botanical monograph. Humoral equilibrium requires targeting primary organ-axis. Note: Clinician electronic signature required before locking Rx (21 CFR Part 11).`;
      }

      if (resBox) {
        resBox.classList.remove('hidden');
        resBox.innerHTML = `
          <div class="p-3 rounded-xl bg-teal-950/50 border border-teal-500/40 space-y-2 mt-2">
            <div class="flex justify-between items-center text-xs">
              <span class="font-bold text-teal-300 flex items-center gap-1">🤖 Hakeem Sahab AI Copilot</span>
              <span class="text-[10px] font-mono text-emerald-400">UPI Vol. 1 Citations</span>
            </div>
            <p class="text-xs text-slate-200 leading-relaxed">${answer}</p>
            <div class="flex justify-between items-center text-[10px] pt-1 border-t border-teal-500/20 text-slate-400">
              <span>Non-autonomous: Licensed Clinician Sign-off Enforced</span>
              <button onclick="insertAiRecommendationToPlan()" class="text-emerald-400 hover:text-white font-bold">+ Insert to Care Plan</button>
            </div>
          </div>
        `;
      }
      if (inputEl) inputEl.value = '';
    }

    function approveDetoxStage(btn) {
      if (btn) {
        const badge = btn.parentElement.querySelector('.bg-amber-500\\/20') || btn.parentElement.querySelector('[class*="amber"]');
        if (badge) badge.className = 'px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 text-[10px] font-bold';
        btn.outerHTML = '<span class="text-emerald-400 font-bold text-xs block text-center py-2 bg-emerald-950/40 rounded-lg border border-emerald-500/30">✓ Stage Approved by Dr. A. Qureshi</span>';
      }
      showNotification('Mudabbar detox stage approved and logged to BMR-2026-MUD-04 batch record.', 'success');
    }

    function queueSpectrometry(btn) {
      if (btn) {
        btn.outerHTML = '<span class="text-blue-400 font-bold text-xs block text-center py-2 bg-blue-950/40 rounded-lg border border-blue-500/30">✓ In Spectrometry Queue (Slot #4)</span>';
      }
      showNotification('Sample dispatched to HPLC Spectrometry Lab.', 'info');
    }

    // Keyboard Shortcuts (⌘K for Search, Escape to Close)
    window.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        toggleSearchModal();
      }
      if (e.key === 'Escape') {
        const searchM = document.getElementById('search-modal');
        if (searchM && !searchM.classList.contains('hidden')) searchM.classList.add('hidden');
        const notifM = document.getElementById('notifications-modal');
        if (notifM && !notifM.classList.contains('hidden')) notifM.classList.add('hidden');
        const patM = document.getElementById('add-patient-modal');
        if (patM && !patM.classList.contains('hidden')) patM.classList.add('hidden');
        const repM = document.getElementById('report-modal');
        if (repM && !repM.classList.contains('hidden')) repM.classList.add('hidden');
      }
    });
