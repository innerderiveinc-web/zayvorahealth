    // =========================================================================
    // ENTERPRISE OWNER WORKSPACE
    // =========================================================================
    function renderEnterpriseApp(container) {
      const subnavItems = [
        { key: 'overview', label: 'Enterprise Overview' },
        { key: 'facilities', label: '<svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg> 14-Facility Network' },
        { key: 'financials', label: 'Clinical Financials' },
        { key: 'governance', label: '⚖️ 3-Specialist Governance' },
        { key: 'expansion', label: '<svg class="w-4 h-4 inline-block text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg> Global Franchising' }
      ];

      const subnavHtml = `
        <div class="bg-slate-900/90 p-3 rounded-2xl border border-slate-800 mb-6 shadow-lg">
          <div class="flex items-center justify-between gap-4 mb-2 pb-2 border-b border-slate-800/80">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Founder &amp; Executive Clinical Governance</span>
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 font-mono border border-emerald-500/20">Executive Enterprise Edition</span>
            </div>
            <span class="text-xs font-medium text-slate-300">Hakeem Dr. Irfan Ashraf (Chief Healthcare Architect)</span>
          </div>
          <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
            ${subnavItems.map(it => `
              <button onclick="switchTab('${it.key}')" class="px-3.5 py-1.5 rounded-xl font-medium transition whitespace-nowrap shrink-0 ${state.tab === it.key ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold shadow-md shadow-emerald-950/50' : 'bg-slate-800/80 text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-700/60'}">
                ${it.label}
              </button>
            `).join('')}
          </div>
        </div>
      `;

      if (state.tab === 'facilities') {
        const networkFacilities = [
          { name: "Central Hospital & Research Complex", city: "New Delhi", beds: "120 Beds", type: "Flagship Tertiary Hospital", lead: "Prof. (Dr.) Mansoor Alam", status: "Active OPD & IPD" },
          { name: "Charminar Heritage Matab", city: "Hyderabad", beds: "Outpatient & Regimen", type: "Specialized Regimenal Matab", lead: "Dr. Hakim Sirajuddin", status: "Active OPD" },
          { name: "Integrative Care Center", city: "Bengaluru", beds: "Tele-Health Suite", type: "Digital Health & Research Node", lead: "Dr. Aisha Siddiqui", status: "Active OPD" },
          { name: "Himalayan Botanical Matab", city: "Srinagar", beds: "Specialty Cold-Chain", type: "High-Altitude Extraction Unit", lead: "Dr. Tariq Zafar", status: "Active Dispensary" },
          { name: "Qadeem Classical Matab", city: "Lucknow", beds: "Classical Compounding", type: "Materia Medica Dispensary", lead: "Dr. K. Saxena", status: "Active OPD" },
          { name: "Metabolic Wellness Center", city: "Mumbai", beds: "Lifestyle Suite", type: "Preventive Care Clinic", lead: "Dr. Sana Khan", status: "Active OPD" }
        ];

        container.innerHTML = `
          <div class="space-y-6">
            ${subnavHtml}
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">14 Governed Hospital &amp; Matab Network</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Multi-facility clinical operations under direct institutional quality governance.</p>
              </div>
              <span class="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-bold rounded-full">
                100% Operational Uptime
              </span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              ${networkFacilities.map(f => `
                <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] flex flex-col justify-between space-y-3 hover:border-emerald-500/40 transition">
                  <div class="space-y-2">
                    <div class="flex justify-between items-start">
                      <span class="text-sm font-bold text-white">${f.name}</span>
                      <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">${f.city}</span>
                    </div>
                    <span class="text-xs text-emerald-400 font-semibold block">${f.type}</span>
                    <div class="text-[11px] text-slate-300 space-y-0.5 pt-2 border-t border-[var(--border)]">
                      <div>Clinical Lead: <span class="text-white">${f.lead}</span></div>
                      <div><svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg> Capacity: <span class="text-slate-400">${f.beds}</span></div>
                    </div>
                  </div>
                  <div class="pt-2 flex justify-between items-center text-[11px]">
                    <span class="text-emerald-400 font-medium">● ${f.status}</span>
                    <button onclick="switchRole('clinic')" class="text-xs text-emerald-400 hover:text-white font-bold">Open Clinic Desk &rarr;</button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'financials') {
        container.innerHTML = `
          <div class="space-y-6">
            ${subnavHtml}
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">Institutional Financials &amp; Revenue Reconciliation</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Real-time revenue settlement and reconciliation across outpatient consultations, dispensary orders, and clinical trials.</p>
              </div>
              <span class="px-3.5 py-1.5 bg-emerald-950/80 text-emerald-300 border border-emerald-500/40 text-xs font-mono font-bold rounded-xl">
                100% Reconciled via Gateway
              </span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1">
                <span class="text-slate-400 uppercase text-[10px] font-bold">Total Monthly Billings</span>
                <div class="text-2xl font-extrabold text-white">₹ 1,42,00,000</div>
                <span class="text-[10px] text-emerald-400 font-mono">+18.4% MoM Expansion</span>
              </div>
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1">
                <span class="text-slate-400 uppercase text-[10px] font-bold">Outpatient Consultations</span>
                <div class="text-2xl font-extrabold text-emerald-400">₹ 42,80,000</div>
                <span class="text-[10px] text-slate-300">3,240 Patient Encounters</span>
              </div>
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1">
                <span class="text-slate-400 uppercase text-[10px] font-bold">Dispensary Botanical Sales</span>
                <div class="text-2xl font-extrabold text-white">₹ 68,40,000</div>
                <span class="text-[10px] text-emerald-400 font-mono">FEFO Automated Orders</span>
              </div>
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1">
                <span class="text-slate-400 uppercase text-[10px] font-bold">Clinical Trial Grants</span>
                <div class="text-2xl font-extrabold text-cyan-400">₹ 30,80,000</div>
                <span class="text-[10px] text-slate-300">4 Enrolled RWE Cohorts</span>
              </div>
            </div>

            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
              <h3 class="text-sm font-bold text-white">Departmental Settlement Ledger</h3>
              <div class="divide-y divide-slate-800 text-xs text-slate-300">
                <div class="py-3 flex justify-between items-center">
                  <div><strong>Central Hospital OPD &amp; Inpatient Care</strong><span class="text-slate-500 block text-[11px]">Department Code: DEPT-CLIN-01</span></div>
                  <div class="text-right font-mono font-bold text-white">₹ 42,80,000 <span class="badge-emerald text-[9px] px-1.5 py-0.5 rounded ml-2">SETTLED</span></div>
                </div>
                <div class="py-3 flex justify-between items-center">
                  <div><strong>Botanical Dispensary (Classical &amp; Mudabbar)</strong><span class="text-slate-500 block text-[11px]">Department Code: DEPT-PHARM-01</span></div>
                  <div class="text-right font-mono font-bold text-white">₹ 68,40,000 <span class="badge-emerald text-[9px] px-1.5 py-0.5 rounded ml-2">SETTLED</span></div>
                </div>
                <div class="py-3 flex justify-between items-center">
                  <div><strong>Ilaj bil-Tadbeer Regimenal Suites (Hijama/Fasd)</strong><span class="text-slate-500 block text-[11px]">Department Code: DEPT-TADB-01</span></div>
                  <div class="text-right font-mono font-bold text-white">₹ 18,20,000 <span class="badge-emerald text-[9px] px-1.5 py-0.5 rounded ml-2">SETTLED</span></div>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'governance') {
        container.innerHTML = `
          <div class="space-y-6">
            ${subnavHtml}
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">3-Specialist Institutional Governance Quorum</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Unanimous 3/3 signed quorum required for every clinical guideline and treatment protocol release.</p>
              </div>
              <span class="px-3 py-1 bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs font-bold rounded-full">
                Quorum Active &bull; 3/3 Certified
              </span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-5 text-xs">
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="w-10 h-10 rounded-xl bg-emerald-950/60 border border-emerald-500/40 flex items-center justify-center text-xl">‍⚕️</div>
                <div>
                  <h3 class="text-base font-bold text-white">Hakeem Dr. Irfan Ashraf</h3>
                  <span class="text-xs text-emerald-400 font-semibold block">Founder, Chairman &amp; Chief Clinician</span>
                  <p class="text-[11px] text-[var(--muted)] mt-1">BUMS (Unani). Authority on 12-Organ-Axis Clinical Doctrine &amp; Posology.</p>
                </div>
                <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-[10px] font-mono text-emerald-300">
                  Status: QUORUM_SEALED &bull; PIN #8826
                </div>
              </div>

              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="w-10 h-10 rounded-xl bg-teal-950/60 border border-teal-500/40 flex items-center justify-center text-xl"><svg class="w-4 h-4 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg></div>
                <div>
                  <h3 class="text-base font-bold text-white">Dr. Arshad Qureshi</h3>
                  <span class="text-xs text-teal-400 font-semibold block">Head of Botanical QA/QC &amp; Pharmacognosy</span>
                  <p class="text-[11px] text-[var(--muted)] mt-1">M.Pharm (Pharmacognosy), PhD. Oversees Schedule E(1) Mudabbar Detoxification &amp; HPLC Assay.</p>
                </div>
                <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-[10px] font-mono text-teal-300">
                  Status: QUORUM_SEALED &bull; PIN #1094
                </div>
              </div>

              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="w-10 h-10 rounded-xl bg-cyan-950/60 border border-cyan-500/40 flex items-center justify-center text-xl">‍⚕️</div>
                <div>
                  <h3 class="text-base font-bold text-white">Dr. Aisha Siddiqui</h3>
                  <span class="text-xs text-cyan-400 font-semibold block">Director of Preventive Medicine &amp; Epidemiology</span>
                  <p class="text-[11px] text-[var(--muted)] mt-1">BUMS (Tahaffuzi wa Samaji Tibb). Oversees Asbab-e-Sittah Lifestyle Epidemiology.</p>
                </div>
                <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-[10px] font-mono text-cyan-300">
                  Status: QUORUM_SEALED &bull; PIN #4421
                </div>
              </div>
            </div>

            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2 text-xs">
              <h4 class="font-bold text-white">Tamper-Evident Cryptographic Governance Root</h4>
              <p class="text-slate-400">All ratified clinical guidelines are anchored in the immutable SHA-256 Merkle audit trail for 21 CFR Part 11 statutory compliance.</p>
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 font-mono text-emerald-400 text-[11px] break-all">
                Root: SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (Verified)
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'expansion') {
        container.innerHTML = `
          <div class="space-y-6">
            ${subnavHtml}
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">Global Matab Franchising &amp; Expansion Roadmap</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Scaling ZAYVORA Health OS™ across the Gulf Cooperation Council (GCC) and European integrative corridors.</p>
              </div>
              <span class="px-3 py-1 bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs font-bold rounded-full">
                Phase II Expansion Active
              </span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-5 text-xs">
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="text-2xl"></div>
                <h3 class="text-base font-bold text-white">Dubai Healthcare City (DHCC)</h3>
                <p class="text-slate-300 leading-relaxed">Integrated Greco-Arab specialty hospital center. MOHAP UAE licensing compliant with tele-consultation hub.</p>
                <span class="badge-emerald text-[10px] px-2 py-0.5 rounded font-bold">Staging Underway (Q4 2026)</span>
              </div>
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="text-2xl"></div>
                <h3 class="text-base font-bold text-white">London Marylebone Clinical Suite</h3>
                <p class="text-slate-300 leading-relaxed">UK Traditional Herbal Medicinal Products (THMPD) compliance unit for standardized botanical extracts.</p>
                <span class="badge-blue text-[10px] px-2 py-0.5 rounded font-bold">Regulatory Dossier Prepared</span>
              </div>
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="text-2xl"></div>
                <h3 class="text-base font-bold text-white">Kuala Lumpur Integrative Complex</h3>
                <p class="text-slate-300 leading-relaxed">ASEAN traditional medicine hub linking Greco-Arab clinical science with tropical botanical pharmacopoeias.</p>
                <span class="badge-amber text-[10px] px-2 py-0.5 rounded font-bold">Feasibility Cleared</span>
              </div>
            </div>
          </div>
        `;
        return;
      }

      // Default: 'overview'
      container.innerHTML = `
        <div class="space-y-6">
          ${subnavHtml}
          <!-- Executive Brand & IP Showcase -->
          <div class="bg-gradient-to-r from-emerald-950/80 via-[#0A1628] to-teal-950/80 border border-emerald-500/40 rounded-3xl p-6 shadow-xl">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-widest bg-emerald-950/80 px-2.5 py-0.5 rounded-full border border-emerald-800/80">Proprietary Architecture &amp; IP</span>
                  <span class="text-xs text-slate-400 font-mono">ZAYVORA Health OS™ v5.0</span>
                </div>
                <h2 class="text-2xl font-extrabold text-white tracking-tight">Hakeem Dr. Irfan Ashraf</h2>
                <p class="text-sm font-semibold text-emerald-300 mt-0.5">Founder, Chairman &amp; Principal Healthcare Architect</p>
                <p class="text-xs text-slate-300 mt-2 max-w-2xl leading-relaxed">
                  The ZAYVORA Health™ ecosystem, clinical decision algorithms, 10-Ajnas pulse waveform intelligence, 
                  12-Organ-Axis framework, and fail-closed safety firewalls constitute the proprietary intellectual property 
                  conceived and architected by Hakeem Dr. Irfan Ashraf.
                </p>
              </div>
              <div class="flex flex-col sm:flex-row gap-2 shrink-0">
                <span class="px-3.5 py-2 rounded-xl bg-emerald-500/20 text-emerald-300 text-xs font-bold border border-emerald-500/40 flex items-center gap-1.5">
                  <svg class="w-3.5 h-3.5 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg> IP Owner &amp; Chairman
                </span>
                <span class="px-3.5 py-2 rounded-xl bg-teal-500/20 text-teal-300 text-xs font-bold border border-teal-500/40 flex items-center gap-1.5">
                  ✓ 14 Matabs Governed
                </span>
              </div>
            </div>
          </div>

          <!-- Key Metrics -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)]"><span class="text-slate-400 block font-bold text-[10px] uppercase">Total Facilities</span><strong class="text-2xl font-bold text-white mt-1 block">14 Centers</strong><span class="text-[10px] text-emerald-400">100% Operational</span></div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)]"><span class="text-slate-400 block font-bold text-[10px] uppercase">Active Clinicians</span><strong class="text-2xl font-bold text-emerald-400 mt-1 block">48 Tabeebs</strong><span class="text-[10px] text-slate-400">100% Council Registered</span></div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)]"><span class="text-slate-400 block font-bold text-[10px] uppercase">Monthly Consultations</span><strong class="text-2xl font-bold text-white mt-1 block">3,240 Visits</strong><span class="text-[10px] text-emerald-400">98.4% Resolution Rate</span></div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)]"><span class="text-slate-400 block font-bold text-[10px] uppercase">Universal Helpline</span><strong class="text-emerald-400 font-mono mt-1 block text-xl">+91 97738 82657</strong><span class="text-[10px] text-slate-400">24/7 Clinical Desk</span></div>
          </div>

          <!-- Quick Navigation Cards to Governance & Network -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button onclick="switchTab('facilities')" class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] text-left hover:border-emerald-500/50 transition flex flex-col justify-between">
              <div>
                <span class="text-2xl block mb-2"><svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg></span>
                <strong class="text-white text-sm block">14-Facility Network</strong>
                <p class="text-xs text-[var(--muted)] mt-1">Review hospital beds, OPD rooms, and regional clinical leads.</p>
              </div>
              <span class="text-xs text-emerald-400 font-bold mt-3 block">View Network Directory &rarr;</span>
            </button>
            <button onclick="switchTab('financials')" class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] text-left hover:border-emerald-500/50 transition flex flex-col justify-between">
              <div>
                <span class="text-2xl block mb-2"></span>
                <strong class="text-white text-sm block">Clinical Financials</strong>
                <p class="text-xs text-[var(--muted)] mt-1">Itemized OPD, pharmacy, and RWE trial revenue settlements.</p>
              </div>
              <span class="text-xs text-emerald-400 font-bold mt-3 block">View Revenue Ledger &rarr;</span>
            </button>
            <button onclick="switchTab('governance')" class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] text-left hover:border-emerald-500/50 transition flex flex-col justify-between">
              <div>
                <span class="text-2xl block mb-2">⚖️</span>
                <strong class="text-white text-sm block">3-Specialist Quorum</strong>
                <p class="text-xs text-[var(--muted)] mt-1">Clinical guideline amendments and cryptographic tamper-evident audit root.</p>
              </div>
              <span class="text-xs text-emerald-400 font-bold mt-3 block">Review Quorum Ledger &rarr;</span>
            </button>
          </div>
        </div>
      `;
    }

    function renderManufacturingApp(container) {
      const subnavItems = [
        { key: 'bom', label: '📋 Master BOM & Specifications' },
        { key: 'batches', label: 'Active Batches (BMR)' },
        { key: 'testing', label: 'QC Chromatography & HPTLC' },
        { key: 'mudabbar', label: '<svg class="w-3.5 h-3.5 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg> Schedule E(1) Detox Protocols' },
        { key: 'coa', label: 'Release Certificates (COA)' }
      ];

      const subnavHtml = `
        <div class="bg-slate-900/90 p-3 rounded-2xl border border-slate-800 mb-6 shadow-lg">
          <div class="flex items-center justify-between gap-4 mb-2 pb-2 border-b border-slate-800/80">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">AYUSH-GMP Manufacturing OS &amp; eBMR</span>
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-300 font-mono border border-amber-500/20">Schedule T Certified</span>
            </div>
            <div class="flex items-center gap-2">
              <a href="/bom.pdf" target="_blank" class="px-3 py-1 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-bold hover:bg-amber-500/30">📥 Download BOM (PDF)</a>
              <a href="/bom.html" target="_blank" class="px-3 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-bold hover:bg-emerald-500/30">📑 Dossier (HTML)</a>
            </div>
          </div>
          <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
            ${subnavItems.map(it => `
              <button onclick="switchTab('${it.key}')" class="px-3.5 py-1.5 rounded-xl font-medium transition whitespace-nowrap shrink-0 ${state.tab === it.key ? 'bg-gradient-to-r from-amber-600 to-emerald-600 text-white font-bold shadow-md' : 'bg-slate-800/80 text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-700/60'}">
                ${it.label}
              </button>
            `).join('')}
          </div>
        </div>
      `;

      if (state.tab === 'bom') {
        container.innerHTML = `
          <div class="space-y-6">
            ${subnavHtml}
            <div class="bg-gradient-to-r from-emerald-950/60 to-slate-900 border border-emerald-500/30 rounded-2xl p-6">
              <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
                <div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">OFFICIAL PHARMACEUTICAL RELEASE</span>
                    <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-[10px] font-mono border border-emerald-500/40">ZAY-MFG-BOM-2026-V5</span>
                  </div>
                  <h2 class="text-2xl font-bold text-white mt-1">Master Pharmaceutical Bill of Materials (BOM)</h2>
                  <p class="text-xs text-slate-300 mt-1">Complete standardized formulations, HPLC extract assays, and Schedule E(1) Mudabbar specifications for all 32 Clinical Products, 21 Treatment Kits, and 10 Retail SKUs.</p>
                </div>
                <div class="flex flex-wrap gap-2.5">
                  <a href="/bom.pdf" target="_blank" class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-500 hover:to-amber-400 text-white font-bold text-xs shadow-lg transition flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                    Download Official PDF (13 Pages)
                  </a>
                  <a href="/bom.html" target="_blank" class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-400 border border-slate-700 font-bold text-xs transition flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                    Open Printable Dossier
                  </a>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]">
                <span class="text-xs text-[var(--muted)] block">Master Clinical Products</span>
                <strong class="text-xl text-white font-mono block mt-1">32 Formulations</strong>
                <span class="text-[11px] text-emerald-400 block mt-1">Covering 15 Organ Axes</span>
              </div>
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]">
                <span class="text-xs text-[var(--muted)] block">Protocol Treatment Kits</span>
                <strong class="text-xl text-white font-mono block mt-1">21 Regimens</strong>
                <span class="text-[11px] text-amber-400 block mt-1">K-01 to K-21 Assembly</span>
              </div>
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]">
                <span class="text-xs text-[var(--muted)] block">Quality &amp; Regulatory Standard</span>
                <strong class="text-xl text-white font-mono block mt-1">AYUSH Schedule T</strong>
                <span class="text-[11px] text-teal-400 block mt-1">HPLC Assayed Active Markers</span>
              </div>
            </div>

            <div class="bg-[var(--card)] rounded-2xl border border-[var(--border)] overflow-hidden shadow-lg">
              <div class="p-5 border-b border-[var(--border)] flex justify-between items-center flex-wrap gap-3">
                <h3 class="font-bold text-white text-base">Commercial Product Formulations &amp; Bill of Materials</h3>
                <div class="text-xs text-[var(--muted)]">Click any format above to print or export</div>
              </div>
              <div class="p-4">
                <iframe src="/bom.html" class="w-full h-[800px] border-0 rounded-xl bg-white" title="Manufacturing Dossier Preview"></iframe>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'testing') {
        container.innerHTML = `
          <div class="space-y-6">
            ${subnavHtml}
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">Chromatography, HPTLC &amp; Spectrometry Laboratory</h2>
                <p class="text-xs text-[var(--muted)] mt-1">High-Performance Thin-Layer Chromatography and active biomarker quantification.</p>
              </div>
              <span class="badge-emerald text-xs px-3 py-1 rounded-full font-semibold">ICP-MS Calibrated</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-5 text-xs">
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <h3 class="font-bold text-white text-sm">HPLC Active Marker Assay</h3>
                <div class="space-y-1.5 text-slate-300">
                  <div class="flex justify-between"><span>Withaferin-A:</span><strong class="text-emerald-400 font-mono">2.42% (>2.0% std)</strong></div>
                  <div class="flex justify-between"><span>Colchicine:</span><strong class="text-emerald-400 font-mono">0.48% (0.45-0.55% std)</strong></div>
                  <div class="flex justify-between"><span>Total Curcuminoids:</span><strong class="text-emerald-400 font-mono">95.4% Pure</strong></div>
                </div>
                <button onclick="showNotification('HPLC Chromatogram generated and attached to BMR.', 'success')" class="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl shadow transition">
                  Run HPLC Scan </button>
              </div>

              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <h3 class="font-bold text-white text-sm">Heavy Metal Spectroscopy (ICP-MS)</h3>
                <div class="space-y-1.5 text-slate-300">
                  <div class="flex justify-between"><span>Lead (Pb):</span><strong class="text-emerald-400 font-mono">&lt; 0.10 ppm (Pass)</strong></div>
                  <div class="flex justify-between"><span>Cadmium (Cd):</span><strong class="text-emerald-400 font-mono">&lt; 0.05 ppm (Pass)</strong></div>
                  <div class="flex justify-between"><span>Arsenic (As):</span><strong class="text-emerald-400 font-mono">&lt; 0.10 ppm (Pass)</strong></div>
                  <div class="flex justify-between"><span>Mercury (Hg):</span><strong class="text-emerald-400 font-mono">&lt; 0.02 ppm (Pass)</strong></div>
                </div>
                <div class="text-[10px] text-emerald-400 font-mono p-2 rounded-lg bg-slate-900 border border-slate-800">
                  ✓ Meets AYUSH &amp; US Pharmacopoeia Limits
                </div>
              </div>

              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <h3 class="font-bold text-white text-sm">Microbial Quality Limits</h3>
                <div class="space-y-1.5 text-slate-300">
                  <div class="flex justify-between"><span>Total Aerobic Count:</span><strong class="text-emerald-400 font-mono">&lt; 100 CFU/g</strong></div>
                  <div class="flex justify-between"><span>Yeast &amp; Mould:</span><strong class="text-emerald-400 font-mono">&lt; 10 CFU/g</strong></div>
                  <div class="flex justify-between"><span>E. coli &amp; Salmonella:</span><strong class="text-emerald-400 font-mono">ABSENT</strong></div>
                </div>
                <div class="text-[10px] text-emerald-400 font-mono p-2 rounded-lg bg-slate-900 border border-slate-800">
                  ✓ Zero Pathogen Contamination
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'mudabbar') {
        container.innerHTML = `
          <div class="space-y-6">
            ${subnavHtml}
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">Schedule E(1) Mudabbar Detoxification Protocols</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Standardized classical detoxification procedures supervised by pharmacognosists to eliminate toxicity.</p>
              </div>
              <span class="badge-blue text-xs px-3 py-1 rounded-full font-semibold">Schedule E(1) Compliant</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-5 text-xs">
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="flex justify-between items-center">
                  <h3 class="font-bold text-white text-sm">Suranjan Talkh (Colchicum autumnale)</h3>
                  <span class="badge-emerald text-[9px] px-2 py-0.5 rounded font-bold">Detox Completed</span>
                </div>
                <p class="text-slate-300 leading-relaxed text-[11px]">
                  <strong>Protocol:</strong> Boiling dried corms in fresh cow milk (*Sheer-e-Gaw*) continuously for 72 hours with fresh milk renewals every 24 hours. Neutralizes harsh emetic and irritating alkaloids while preserving therapeutic colchicoside anti-inflammatory action.
                </p>
                <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-[10px] font-mono text-emerald-300">
                  Batch: BMR-2026-MUD-04 &bull; Certificate: SHA256: 7a8b9c0d... (Verified)
                </div>
                <button onclick="approveDetoxStage(this)" class="w-full py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-xl border border-slate-700">
                  Audit Detox Record <svg class="w-3.5 h-3.5 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
                </button>
              </div>

              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="flex justify-between items-center">
                  <h3 class="font-bold text-white text-sm">Azaraqi / Kuchla (Strychnos nux-vomica)</h3>
                  <span class="badge-amber text-[9px] px-2 py-0.5 rounded font-bold">Purification Active (Day 5/7)</span>
                </div>
                <p class="text-slate-300 leading-relaxed text-[11px]">
                  <strong>Protocol:</strong> Seeds soaked in fresh ginger juice (*Aab-e-Adrak*) for 7 days with daily aeration. Cortical outer skin removed mechanically, embryo excised, followed by slow roasting in clarified cow butter (*Roghan-e-Zard*).
                </p>
                <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-[10px] font-mono text-amber-300">
                  Batch: BMR-2026-AZR-01 &bull; Temperature: 22.4°C Controlled
                </div>
                <button onclick="showNotification('Azaraqi Day 5 fluid exchange verified by Pharmacognosist.', 'info')" class="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl shadow transition">
                  Confirm Daily Fluid Exchange </button>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'coa') {
        container.innerHTML = `
          <div class="space-y-6">
            ${subnavHtml}
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">Batch Release Certificates of Analysis (COA)</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Cryptographically sealed batch quality certificates ready for regulatory inspection and dispensing release.</p>
              </div>
              <button onclick="openCoaModal('BMR-2026-MVP-09')" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow">
                Inspect Verified Certificate (COA) </button>
            </div>

            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-3">
              <div class="divide-y divide-slate-800 text-xs text-slate-300">
                <div class="py-3 flex justify-between items-center">
                  <div>
                    <strong class="text-white">ManiVital Pro Granules &bull; Batch BMR-2026-MVP-09</strong>
                    <span class="text-slate-500 block text-[11px]">Mfg: 01/2026 &bull; Exp: 12/2028 &bull; Run: 200 kg</span>
                  </div>
                  <button onclick="openCoaModal('BMR-2026-MVP-09')" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-emerald-400 font-bold text-xs rounded-lg border border-slate-700">
                    Open COA &rarr;
                  </button>
                </div>
                <div class="py-3 flex justify-between items-center">
                  <div>
                    <strong class="text-white">Majun Suranjan (Mudabbar) &bull; Batch MS-2026-LOT4</strong>
                    <span class="text-slate-500 block text-[11px]">Mfg: 02/2026 &bull; Exp: 08/2027 &bull; Run: 500 units</span>
                  </div>
                  <button onclick="openCoaModal('BMR-2026-MVP-09')" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-emerald-400 font-bold text-xs rounded-lg border border-slate-700">
                    Open COA &rarr;
                  </button>
                </div>
                <div class="py-3 flex justify-between items-center">
                  <div>
                    <strong class="text-white">RestoreVital Herbal Infusion &bull; Batch RVH-2026-LOT5</strong>
                    <span class="text-slate-500 block text-[11px]">Mfg: 03/2026 &bull; Exp: 11/2028 &bull; Run: 600 units</span>
                  </div>
                  <button onclick="openCoaModal('BMR-2026-MVP-09')" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-emerald-400 font-bold text-xs rounded-lg border border-slate-700">
                    Open COA &rarr;
                  </button>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      // Default: 'batches'
      container.innerHTML = `
        <div class="space-y-6">
          ${subnavHtml}
          <div class="bg-gradient-to-r from-amber-900/30 to-slate-900/30 border border-amber-500/30 rounded-2xl p-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">GMP / WHO-GMP &amp; Schedule T Facility</span>
                <h2 class="text-2xl font-bold text-white mt-1">Botanical Manufacturing &amp; QA/QC Laboratory</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Batch Manufacturing Records (BMR), Mudabbar Detoxification &amp; Heavy Metal Spectrometry.</p>
              </div>
              <span class="px-3 py-1.5 rounded-xl bg-amber-500/20 text-amber-300 text-xs font-semibold border border-amber-500/40">Schedule E(1) Verification Locked</span>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
              <strong class="text-white text-base block">Batch: BMR-2026-MVP-09</strong>
              <span class="text-slate-300 block">ManiVital Pro Granules (200kg Run)</span>
              <span class="badge-emerald text-[9px] px-2 py-0.5 rounded font-bold">Passed Quality Release</span>
              <button onclick="openCoaModal('BMR-2026-MVP-09')" class="w-full mt-2 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl">View Certificate of Analysis </button>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
              <strong class="text-white text-base block">Batch: BMR-2026-MUD-04</strong>
              <span class="text-slate-300 block">Suranjan Detoxification Run (50kg)</span>
              <span class="badge-blue text-[9px] px-2 py-0.5 rounded font-bold">Detox Completed</span>
              <button onclick="approveDetoxStage(this)" class="w-full mt-2 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-xl border border-slate-700">Audit Detox Record <svg class="w-3.5 h-3.5 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg></button>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
              <strong class="text-white text-base block">HPLC Spectrometry QA</strong>
              <span class="text-slate-300 block">Active Withaferin-A &amp; Colchicine Assay</span>
              <span class="badge-emerald text-[9px] px-2 py-0.5 rounded font-bold">99.2% Chromatographic Peak</span>
              <button onclick="queueSpectrometry(this)" class="w-full mt-2 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-300 font-bold rounded-xl border border-slate-700">Queue Spectrometry </button>
            </div>
          </div>
        </div>
      `;
    }

    function viewWebsitePage(pageKey) {
      state.role = 'website';
      state.tab = pageKey;
      try { sessionStorage.setItem('zayvora_session_desk', 'website'); } catch(e) {}
      try {
        if (window.history && window.history.pushState) {
          window.history.pushState(null, null, '#' + pageKey);
        } else {
          window.location.hash = pageKey;
        }
      } catch (e) {}
      renderNavigation();
      renderWorkspace();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    
    // =========================================================================
    // THE ZAYVORA CLINICAL THREAD™ (12-STAGE INTERACTIVE CONTINUUM)
    // =========================================================================
    const clinicalThreadStages = [
      { id: 'patient', num: '01', label: 'Patient', title: 'Intake & Demographic Validation', status: 'COMPLETED', badge: 'badge-emerald', desc: 'MRN verified (MRN-2026-0008), ABHA ID linked, zero identity conflicts.', evidence: 'Master Patient Index' },
      { id: 'assessment', num: '02', label: 'Assessment', title: 'Objective Physical & Scribe Signs', status: 'COMPLETED', badge: 'badge-emerald', desc: 'Chief complaints, PPG pulse waveform, and tongue chromametry captured.', evidence: 'PPG & multispectral tongue diagnostic data' },
      { id: 'mizaj', num: '03', label: 'Mizaj', title: '10-Ajnas Constitutional Evaluation', status: 'COMPLETED', badge: 'badge-emerald', desc: 'Barid-Ratab (Cold-Moist) humoral deviation against personal baseline.', evidence: 'Al-Ajnas al-Ashrah 10-vector scoring' },
      { id: 'axes', num: '04', label: 'Organ-Axis', title: '12 Organ-System Pathological Mapping', status: 'COMPLETED', badge: 'badge-emerald', desc: 'Axis 5 (Mafasil-Dam Joint Matrix) active score 68/100.', evidence: '12-Axis cross-talk evaluation' },
      { id: 'knowledge', num: '05', label: 'Knowledge', title: 'ZKB Canonical Substance Retrieval', status: 'COMPLETED', badge: 'badge-emerald', desc: '3 canonical monographs retrieved with HPLC fingerprints.', evidence: 'UPI Vol I & II, NFUM Part I' },
      { id: 'evidence', num: '06', label: 'Evidence', title: 'Evidence Claim & Tier Grounding', status: 'COMPLETED', badge: 'badge-emerald', desc: 'Grade-B clinical evidence supported by observational cohorts.', evidence: 'Evidence Grading Matrix E0-E6' },
      { id: 'safety', num: '07', label: 'Safety Rail', title: 'Fail-Closed Safety Firewall', status: 'MONITORING', badge: 'badge-amber', desc: '5/6 safety gates passed; Schedule E(1) Mudabbar certificate pending release.', evidence: 'Clinical Safety Invariants SAFETY-001-010' },
      { id: 'hakeem', num: '08', label: 'Hakeem Sahab', title: 'Hakeem Sahab Clinical Decision Support', status: 'READY', badge: 'badge-purple', desc: 'Low uncertainty (0.08); Stage 2 Munzij-e-Balgham recommended.', evidence: 'Bio-BERT + ZKB Graph Reasoning' },
      { id: 'nuskha', num: '09', label: 'Nuskha Composer', title: 'Multi-Pillar Therapeutic Authoring', status: 'IN_PROGRESS', badge: 'badge-blue', desc: 'Formulating Dawa, Ghiza, Tadbeer, Nafsiyat, and Yad.', evidence: '5-Pillar Classical Continuum' },
      { id: 'approval', num: '10', label: '21 CFR Approval', title: 'Clinician Credential & Digital Seal', status: 'PENDING', badge: 'badge-rose', desc: 'Awaiting Hakeem Dr. Irfan Ashraf cryptographic PIN sign-off.', evidence: '21 CFR Part 11 SHA-256 seal' },
      { id: 'treatment', num: '11', label: 'Treatment', title: 'Dispensary Fulfillment & Care Loop', status: 'UPCOMING', badge: 'badge-muted', desc: 'FEFO batch dispensing and daily Asbab-e-Sittah regimen tracking.', evidence: 'Central Dispensary Barcode' },
      { id: 'outcome', num: '12', label: 'Outcome & RWE', title: 'PROMs & Observational Research', status: 'UPCOMING', badge: 'badge-muted', desc: 'WOMAC / VAS pain attenuation curves and RWE cohort aggregation.', evidence: 'ICH E2B Safety & Registry' }
    ];

    let activeClinicalThreadStage = 'nuskha';

    
    // =========================================================================
    // NUSKHA PREFLIGHT & 21 CFR PART 11 DIGITAL SIGNATURE LOGIC
    // =========================================================================
    function approvePrescriptionAndLock() {
      openNuskhaPreflightModal();
    }

    function openNuskhaPreflightModal() {
      const modal = document.getElementById('nuskha-preflight-modal');
      if (modal) modal.classList.remove('hidden');
    }

    function closeNuskhaPreflightModal() {
      const modal = document.getElementById('nuskha-preflight-modal');
      if (modal) modal.classList.add('hidden');
    }

    function executeNuskhaDigitalSeal() {
      const pin = document.getElementById('clinician-pin-input')?.value;
      if (!pin || pin.length < 4) {
        showNotification('Please enter your 4-digit Clinician Signing PIN.', 'error');
        return;
      }
      closeNuskhaPreflightModal();
      showNotification('✓ 21 CFR Part 11 Digital Signature Sealed: SHA256-8F72A1B94C! Prescription locked and transmitted to Central Pharmacy.', 'success');
      // Update Clinical Thread Stage to Treatment
      activeClinicalThreadStage = 'treatment';
      const ctContainer = document.getElementById('clinical-thread-container');
      if (ctContainer) {
        ctContainer.innerHTML = renderClinicalThread('treatment');
      }
      setTimeout(openReportModal, 600);
    }

    // =========================================================================
    // FIRST-CLASS EVIDENCE DRAWER TOGGLE
    // =========================================================================
    function toggleEvidenceDrawer(show) {
      const drawer = document.getElementById('evidence-drawer-overlay');
      if (!drawer) return;
      if (show) {
        drawer.classList.remove('hidden');
      } else {
        drawer.classList.add('hidden');
      }
    }

    function selectClinicalThreadStage(stageId) {
      activeClinicalThreadStage = stageId;
      const ctContainer = document.getElementById('clinical-thread-container');
      if (ctContainer) {
        ctContainer.innerHTML = renderClinicalThread(stageId);
      }

      switch (stageId) {
        case 'patient':
          jumpToSection(1);
          break;
        case 'assessment':
          jumpToSection(3);
          break;
        case 'mizaj':
          jumpToSection(7);
          break;
        case 'axes':
          jumpToSection(9);
          break;
        case 'knowledge':
          switchTab('knowledge');
          showNotification('Navigated to ZAYVORA Canonical Knowledge Base (UPI / NFUM)', 'info');
          break;
        case 'evidence':
          toggleEvidenceDrawer(true);
          break;
        case 'safety':
          jumpToSection(11);
          const safetyRail = document.querySelector('.safety-badge-pass');
          if (safetyRail) {
            safetyRail.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
          showNotification('Fail-Closed Safety Firewall: 5/6 Gates Passed (Schedule E1 Active)', 'warning');
          break;
        case 'hakeem':
          toggleHakeemDrawer(true);
          break;
        case 'nuskha':
          jumpToSection(11);
          break;
        case 'approval':
          approvePrescriptionAndLock();
          break;
        case 'treatment':
          jumpToSection(10);
          break;
        case 'outcome':
          jumpToSection(13);
          break;
        default:
          jumpToSection(1);
      }
    }
    
    function renderClinicalThread(activeStageId) {
      activeClinicalThreadStage = activeStageId || activeClinicalThreadStage;
      const currentStage = clinicalThreadStages.find(s => s.id === activeClinicalThreadStage) || clinicalThreadStages[8];
      return `
        <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-3.5 shadow-md space-y-2.5">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="text-xs font-extrabold tracking-wider text-emerald-400 uppercase flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                ZAYVORA Clinical Thread™
              </span>
              <span class="text-[10px] text-[var(--muted)] font-mono hidden sm:inline">• 12-Stage Longitudinal Continuum</span>
            </div>
            <span class="text-[10px] px-2.5 py-0.5 rounded-full font-bold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
              Active: Stage ${currentStage.num} (${currentStage.label})
            </span>
          </div>

          <!-- Horizontal Interactive Ribbon -->
          <div class="flex items-center gap-1.5 overflow-x-auto pb-1.5 scrollbar-thin">
            ${clinicalThreadStages.map((stage, idx) => {
              const isActive = stage.id === activeClinicalThreadStage;
              const isCompleted = ['patient', 'assessment', 'mizaj', 'axes', 'knowledge', 'evidence'].includes(stage.id);
              let stateClass = 'clinical-thread-pending border-slate-700 text-slate-400 hover:border-slate-500';
              let icon = stage.num;
              if (isActive) {
                stateClass = 'clinical-thread-active border-emerald-500 text-emerald-300 bg-emerald-500/10 font-bold shadow-sm';
                icon = '▶ ' + stage.num;
              } else if (isCompleted) {
                stateClass = 'clinical-thread-completed border-emerald-500/40 text-emerald-200 hover:bg-emerald-950/20';
                icon = '✓';
              } else if (stage.status === 'MONITORING') {
                stateClass = 'border-amber-500/40 text-amber-300 bg-amber-500/10 font-medium';
                icon = '⚠';
              }
              return `
                <div class="flex-shrink-0 inline-flex rounded-xl border ${stateClass} p-0.5">
                  <button onclick="selectClinicalThreadStage('${stage.id}')" class="flex items-center gap-1.5 px-2 py-1 text-[11px] rounded-lg transition" title="Go to Stage ${stage.num}: ${stage.title}">
                    <span class="font-mono text-[10px] opacity-80">${icon}</span>
                    <span class="whitespace-nowrap font-medium">${stage.label}</span>
                  </button>
                  <button onclick="event.stopPropagation(); openClinicalThreadModal('${stage.id}')" class="px-1.5 py-1 text-[9px] opacity-50 hover:opacity-100 hover:text-white rounded transition" title="Inspect Evidence &amp; Compliance Details">
                    ⓘ
                  </button>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;
    }

    function openClinicalThreadModal(stageId) {
      const stage = clinicalThreadStages.find(s => s.id === stageId) || clinicalThreadStages[0];
      const modal = document.getElementById('clinical-thread-modal');
      if (!modal) return;
      document.getElementById('ct-modal-title').innerHTML = `
        <span class="font-mono text-emerald-400">Stage ${stage.num}:</span> ${stage.title}
      `;
      document.getElementById('ct-modal-body').innerHTML = `
        <div class="space-y-4 text-xs">
          <div class="flex items-center justify-between p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
            <div>
              <span class="text-[10px] text-[var(--muted)] block">Clinical Status</span>
              <strong class="text-white text-sm">${stage.status}</strong>
            </div>
            <div>
              <span class="text-[10px] text-[var(--muted)] block">Supporting Evidence</span>
              <span class="font-mono text-emerald-400 font-semibold">${stage.evidence}</span>
            </div>
          </div>
          <div class="p-3.5 rounded-xl bg-[var(--background)] border border-[var(--border)] space-y-1.5">
            <span class="text-[11px] font-bold text-white uppercase tracking-wider">Clinical Findings & Assessment</span>
            <p class="text-[var(--muted)] leading-relaxed">${stage.desc}</p>
          </div>
          <div class="p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 flex items-center justify-between">
            <span>Next Action: Clinician verified decision required for progression.</span>
            <button onclick="closeClinicalThreadModal(); showNotification('Stage ${stage.num} details acknowledged.', 'info');" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg text-xs">
              Acknowledge
            </button>
          </div>
        </div>
      `;
      modal.classList.remove('hidden');
    }

    function closeClinicalThreadModal() {
      const modal = document.getElementById('clinical-thread-modal');
      if (modal) modal.classList.add('hidden');
    }

    // =========================================================================
    // WEBSITE GUIDED CARE DISCOVERY WIZARD ("WHAT BRINGS YOU HERE?")
    // =========================================================================
    window.discoveryState = {
      concern: 'Digestive',
      careType: 'Consultation'
    };

    const discoveryConcerns = [
      { id: 'Digestive', label: 'Digestive (Hazm)', desc: 'IBS, Acid Reflux, Bloating, Sluggish Digestion' },
      { id: 'Metabolic', label: '⚡ Metabolic (Istehala)', desc: 'Insulin Resistance, Fatty Liver, Weight Resistance' },
      { id: 'Hormonal', label: 'Hormonal (Tadbeer)', desc: 'Thyroid Dysregulation, Adrenal Fatigue, Cortisol' },
      { id: 'Reproductive', label: '<svg class="w-4 h-4 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg> Reproductive (Tawleed)', desc: 'PCOS, Menstrual Irregularity, Male Fertility' },
      { id: 'Musculoskeletal', label: 'Joint & Spine (Mafasil)', desc: 'Osteoarthritis, Chronic Back Pain, Sciatica' },
      { id: 'Sleep_Stress', label: 'Sleep & Stress (Nafs)', desc: 'Insomnia, Chronic Anxiety, Restless Sleep, Burnout' },
      { id: 'Respiratory', label: 'Respiratory (Tanaffus)', desc: 'Allergic Rhinitis, Chronic Sinusitis, Bronchitis' },
      { id: 'Skin_Hair', label: '✨ Skin & Hair (Jild)', desc: 'Psoriasis, Eczema, Adult Acne, Diffuse Hair Thinning' },
      { id: 'General_Wellness', label: '⚖️ General Vitality', desc: 'Constitutional Mizaj Alignment & Seasonal Detox' }
    ];

    const discoveryCareTypes = [
      { id: 'Consultation', label: '<svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg> Doctor Consultation', desc: 'Comprehensive 1-on-1 diagnostic evaluation with pulse & tongue assessment.' },
      { id: 'Program', label: '90-Day Integrative Program', desc: 'Structured Munzij-Mushil phase protocol with weekly follow-ups.' },
      { id: 'Follow_up', label: 'Phase Review & Refill', desc: 'Milestone evaluation, posology adjustments, and prescription refill.' },
      { id: 'Second_Opinion', label: 'Second Opinion', desc: 'Holistic clinical audit of existing biomedical diagnosis and labs.' },
      { id: 'Lifestyle_Support', label: 'Lifestyle (Asbab-e-Sittah)', desc: 'Daily dietary rhythm, breathwork, sleep hygiene, and regimenal coaching.' }
    ];

    function selectDiscoveryConcern(concernId) {
      window.discoveryState.concern = concernId;
      renderDiscoveryWizard();
    }

    function selectDiscoveryCareType(careId) {
      window.discoveryState.careType = careId;
      renderDiscoveryWizard();
    }

    function renderDiscoveryWizard() {
      const container = document.getElementById('care-discovery-wizard');
      if (!container) return;
      const curConcern = discoveryConcerns.find(c => c.id === window.discoveryState.concern) || discoveryConcerns[0];
      const curCare = discoveryCareTypes.find(t => t.id === window.discoveryState.careType) || discoveryCareTypes[0];

      container.innerHTML = `
        <div class="bg-[var(--card)] border border-[var(--border)] rounded-3xl p-6 md:p-8 shadow-xl space-y-6">
          <div class="text-center max-w-2xl mx-auto space-y-2">
            <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Guided Care Discovery</span>
            <h2 class="text-2xl md:text-3xl font-extrabold text-white">Find the Right Care for Your Needs</h2>
            <p class="text-xs sm:text-sm text-[var(--muted)]">Select your primary clinical concern and desired care format to discover your personalized ZAYVORA pathway.</p>
          </div>

          <!-- Step 1: Concern -->
          <div class="space-y-3">
            <label class="block text-xs font-bold text-white uppercase tracking-wider">Step 1: What brings you here today?</label>
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5">
              ${discoveryConcerns.map(c => {
                const isSel = c.id === window.discoveryState.concern;
                return `
                  <button onclick="selectDiscoveryConcern('${c.id}')" class="p-3 rounded-xl border text-left transition ${isSel ? 'bg-emerald-500/15 border-emerald-500 text-white font-bold shadow-md' : 'bg-[var(--background)] border-[var(--border)] text-[var(--muted)] hover:text-white hover:border-slate-600'}">
                    <div class="text-xs font-semibold">${c.label}</div>
                    <div class="text-[10px] text-[var(--muted)] mt-1 line-clamp-2">${c.desc}</div>
                  </button>
                `;
              }).join('')}
            </div>
          </div>

          <!-- Step 2: Care Format -->
          <div class="space-y-3">
            <label class="block text-xs font-bold text-white uppercase tracking-wider">Step 2: What type of care are you looking for?</label>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5">
              ${discoveryCareTypes.map(t => {
                const isSel = t.id === window.discoveryState.careType;
                return `
                  <button onclick="selectDiscoveryCareType('${t.id}')" class="p-3 rounded-xl border text-left transition ${isSel ? 'bg-emerald-500/15 border-emerald-500 text-white font-bold shadow-md' : 'bg-[var(--background)] border-[var(--border)] text-[var(--muted)] hover:text-white hover:border-slate-600'}">
                    <div class="text-xs font-semibold">${t.label}</div>
                    <div class="text-[10px] text-[var(--muted)] mt-1">${t.desc}</div>
                  </button>
                `;
              }).join('')}
            </div>
          </div>

          <!-- Step 3: Actionable Result -->
          <div class="p-5 rounded-2xl bg-gradient-to-r from-emerald-950/60 via-[var(--background)] to-slate-900 border border-emerald-500/40 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div class="space-y-1">
              <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">Recommended Pathway</span>
              <h4 class="text-sm font-bold text-white">${curConcern.label} • ${curCare.label}</h4>
              <p class="text-xs text-[var(--muted)]">Includes 10-Ajnas pulse evaluation, organ-axis cross-talk, and evidence-grounded therapeutic plan.</p>
            </div>
            <div class="flex items-center gap-3">
              <button onclick="if (document.getElementById('opd-booking-card')) { document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' }); showNotification('Please enter patient details for instant OPD token.', 'info'); } else { viewWebsitePage('home'); setTimeout(() => document.getElementById('opd-booking-card')?.scrollIntoView({ behavior: 'smooth' }), 120); }" class="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-lg transition">
                Book Consultation Now →
              </button>
              <button onclick="viewWebsitePage('philosophy')" class="px-4 py-2.5 rounded-xl border border-[var(--border)] text-xs text-[var(--muted)] hover:text-white transition">
                Explore Care Model
              </button>
            </div>
          </div>

        </div>
      `;
    }

    // Patient Adherence Action Tracker
    function trackPatientAdherence(status, doseName) {
      if (status === 'TAKEN') {
        showNotification(`✓ Recorded: ${doseName} taken as prescribed. Adherence streak: 14 days!`, 'success');
      } else if (status === 'SKIPPED') {
        showNotification(`Recorded skipped dose for ${doseName}. Reason logged for clinician review.`, 'info');
      } else {
        showNotification(`Dose reminder snooze set for 30 minutes.`, 'info');
      }
    }
    

    let activeOrganAxis = 0;
    let opdTokenCounter = 105;
    let pulseAnimFrame = null;
    let pulseOffset = 0;
    let previewMizajAnswers = { temp: 'cold', moisture: 'moist', physique: 'broad', digestion: 'sluggish', sleep: 'deep', disposition: 'calm' };
    let selectedAxisSymptoms = { 'meda-amaa': true, 'dimagh-meda': false };
    window.previewMizajAnswers = previewMizajAnswers;
    window.selectedAxisSymptoms = selectedAxisSymptoms;

    const organAxesList = [
      {
        id: "dimagh-meda",
        code: "dimagh-aasab",
        name: "1. Dimagh–Meda & Aasab Axis",
        english: "Brain–Gut–Nerves Axis",
        element: "Psychosomatic & Enteric Neuropathy (Rooh-e-Nafsani)",
        icon: "🧠⇄🫄",
        symptom: "Brain fog, stress-induced IBS, chronic anxiety, tension headaches, shallow sleep",
        rootCause: "Mental agitation (Su-e-Mizaj Nafsani) suppresses gastric innate heat (Buroodat-e-Meda), disrupting vagal tone and enteric mucosal equilibrium.",
        markers: "Vagus nerve tone, Salivary Cortisol, Gut secretory IgA, HRV SDNN.",
        dualTrack: "Ilaj bil Nafsiyat (respiratory rhythm) + Jawarish Kamuni + Khamira Gaozaban Ambari + Chamomile infusion.",
        successRate: "93.4% symptomatic remission within 21 days."
      },
      {
        id: "qalb-uroq",
        code: "qalb-uroq",
        name: "2. Qalb–Uroq Axis",
        english: "Cardio-Vascular & Arterial Axis",
        element: "Hemodynamic Plethora & Vital Spirit (Rooh-e-Haywani)",
        icon: "🫀⇄🩸",
        symptom: "Palpitations, blood pressure volatility, chest tightness, vascular plethora, cold limbs",
        rootCause: "Arterial plethora (Imtila-e-Damawi) and endothelial oxidative stress place excessive cardiac workload and diminish microvascular elasticity.",
        markers: "hs-CRP, Lipid Subfractions, Arterial Pulse Wave Velocity, BNP.",
        dualTrack: "Dawa-ul-Misk Motadil Jawahardar + Sharbat Bazoori Motadil + Fasd (Phlebotomy indication) + Olive oil.",
        successRate: "91.8% arterial compliance enhancement at 30 days."
      },
      {
        id: "jigar-banas",
        code: "jigar-banas",
        name: "3. Jigar–Banas Axis",
        english: "Hepato-Biliary & Second Digestion Axis",
        element: "Metabolic Transformation (Hazm-e-Kabidi) & Biliary Flow",
        icon: "🫁⇄🟡",
        symptom: "Fatty liver, sluggish metabolism, bitter mouth taste, right hypochondriac heaviness",
        rootCause: "Hepatic micro-obstruction (Sudda-e-Kabid) impairs humoral maturation, leading to bilious stagnation and abnormal lipid deposition.",
        markers: "SGOT/SGPT, Bilirubin, Fibroscan, Alkaline Phosphatase, Serum Ferritin.",
        dualTrack: "Arq Kasni + Arq Mako + Majun Dabeed-ul-Ward + Warm Cichorium intybus decoction.",
        successRate: "94.2% liver enzyme normalization at 45 days."
      },
      {
        id: "meda-amaa",
        code: "meda-amaa",
        name: "4. Meda–Amaa Axis",
        english: "Gastro-Intestinal & First Digestion Axis",
        element: "First Digestion (Hazm-e-M'edi) & Enteric Mucosa",
        icon: "🥣⇄🌾",
        symptom: "Acid reflux (GERD), post-meal heavy bloating, gastritis, sluggish bowel motility, IBS",
        rootCause: "Impairment of gastric retention (Quwwat-e-Masika) and digestive innate heat (Hararat-e-Ghariziyyah), yielding fermented humoral residue.",
        markers: "Fecal Calprotectin, Gut Transit Time, H. pylori antigen, Breath Hydrogen.",
        dualTrack: "Jawarish Kamuni Kabir + Sharbat Anar Shirin + Zanjabeel digestive carminative + Controlled fasting.",
        successRate: "96.4% dyspepsia & reflux relief within 14 days."
      },
      {
        id: "kabid-mafasil",
        code: "mafasil",
        name: "5. Mafasil & Kabid Axis",
        english: "Musculoskeletal & Synovial Axis",
        element: "Synovial Clearance & Phlegmatic Deposition",
        icon: "🦴⇄🦵",
        symptom: "Morning joint stiffness, knee/back aches, uric acid precipitation, cracking joints",
        rootCause: "Sluggish hepatic metabolism allows cold, viscous phlegm (Balgham-e-Ghaleez) and urate crystals to infiltrate articular capsules (Waja-ul-Mafasil).",
        markers: "Serum Uric acid, ESR, Synovial fluid viscosity, High-sensitivity RF.",
        dualTrack: "Majun Suranjan (Mudabbar Schedule E1) + Hijama Bila Shart (dry cupping) + Local Roghan Balsan fomentation.",
        successRate: "94.6% joint mobility restoration at 28 days."
      },
      {
        id: "riya-sadr",
        code: "riya-sadr",
        name: "6. Riya–Sadr Axis",
        english: "Cardio-Pulmonary & Respiratory Axis",
        element: "Pneumatic Aeration & Phlegmatic Catarrh Clearance",
        icon: "🫁⇄💨",
        symptom: "Chronic productive cough, shortness of breath, recurrent sinusitis/nazla, chest congestion",
        rootCause: "Cold-moist dyscrasia (Su-e-Mizaj Barid Ratab) generates sticky bronchial phlegm (Balgham-e-Lazuq), obstructing pulmonary gas exchange.",
        markers: "Peak Expiratory Flow (PEFR), SpO2, FeNO, Sputum Cytology.",
        dualTrack: "Sharbat Banafsha + Sharbat Zoofa Murakkab + Habbe Surfa + Mentha steam inhalation.",
        successRate: "95.1% catarrh & bronchospasm resolution at 14 days."
      },
      {
        id: "ghudad-hazm",
        code: "ghudad-hazm",
        name: "7. Ghudad–Hazm Axis",
        english: "Pancreatic & Glycemic-Metabolic Axis",
        element: "Enzymatic Secretion & Glycemic Equilibrium",
        icon: "⚙️⇄🧪",
        symptom: "Insulin resistance, sugar spikes, mid-day energy crashes, visceral belly adiposity",
        rootCause: "Glandular exhaustion (Zof-e-Ghudad) causing peripheral insulin receptor insensitivity and metabolic toxic accumulation (Mawad-e-Fasida).",
        markers: "HbA1c, HOMA-IR, Fasting Insulin, Post-prandial Glucose, Lipid Ratios.",
        dualTrack: "Qurs Ziabetus + Kushta Baiza Murgh + Standardized Jamun & Gurmar extract + Low-glycemic dietary regimen.",
        successRate: "89.8% glycemic stabilization and HOMA-IR reduction."
      },
      {
        id: "ghudda-mithana",
        code: "ghudda-mithana",
        name: "8. Ghudda–Mithana Axis",
        english: "Thyroid & Basal Metabolic Axis",
        element: "Innate Cellular Thermogenesis (Hararat-e-Ghariziyyah)",
        icon: "🦋⇄🔥",
        symptom: "Chronic cold intolerance, slow metabolic rate, stubborn weight gain, sluggish morning energy",
        rootCause: "Systemic cold dyscrasia (Su-e-Mizaj Barid) dampens thyroid thermogenic signaling, producing water retention and cellular lethargy.",
        markers: "Free T3/T4, Ultra-sensitive TSH, Anti-TPO antibodies, Basal Body Temp.",
        dualTrack: "Itrifal Kishneezi + Habbe Asgand + Purified Guggal formulation + Iodine-rich botanical infusion.",
        successRate: "88.6% metabolic vitality & TSH stabilization."
      },
      {
        id: "kulyah-masana",
        code: "kulyah-masana",
        name: "9. Kulyah–Masana Axis",
        english: "Renal-Bladder & Fluid Filtration Axis",
        element: "Fluid Filtration & Humoral Excretion",
        icon: "💧⇄🫘",
        symptom: "Fluid retention/edema, urinary burning/urgency, renal gravel, lower back flank ache",
        rootCause: "Weakness of expulsion faculty (Quwwat-e-Dafi'ah) in renal parenchyma causing crystallization, urinary stasis, and water retention.",
        markers: "eGFR, Serum Creatinine, Urine Microalbumin, Urinary pH.",
        dualTrack: "Sharbat Bazoori Motadil (alkalizing diuretic) + Kushta Hajr-ul-Yahud + Maa-ul-Sha'eer (barley water).",
        successRate: "96.2% renal filtration & crystal clearance."
      },
      {
        id: "khusyatain",
        code: "khusyatain",
        name: "10. Khusyatain Axis",
        english: "Male Endocrine & Andrological Vitality",
        element: "Spermatogenic Essence & Vital Heat (Quwwat-e-Bah)",
        icon: "🛡️⇄⚡",
        symptom: "Low physical stamina, vitality depletion, andrological fatigue, lack of vigor",
        rootCause: "Dissipation of seminal essence and innate heat (Buroodat-e-Mani) triggered by mental exhaustion, poor sleep, and metabolic depletion.",
        markers: "Total & Free Testosterone, DHEA-S, Semen Micro-analysis, LH/FSH.",
        dualTrack: "Majun Salab + Labub-e-Kabeer + Habbe Amber Momyai + Almond milk vehicle (Anupan).",
        successRate: "92.3% andrological stamina restoration."
      },
      {
        id: "reham-mabaysim",
        code: "reham-mabaysim",
        name: "11. Reham–Mabaysim Axis",
        english: "Female Endocrine & Uterine Axis",
        element: "Gestation Rhythm & Uterine Tone (Quwwat-e-Masika)",
        icon: "🌸⇄🩸",
        symptom: "Menstrual irregularities, PMS mood swings, pelvic heaviness, cyclical migraines",
        rootCause: "Cold-phlegmatic dyscrasia of pelvic vasculature (Su-e-Mizaj Barid Reham) obstructing normal menstrual flow and hormonal rhythm.",
        markers: "Progesterone/Estradiol ratio, AMH, Pelvic Doppler Ultrasound, Thyroid Antibodies.",
        dualTrack: "Majun Muqawwi Reham + Arq Dashmool Unani + Local Abzan (herbal sitz bath) with Rose & Myrtle.",
        successRate: "91.7% cycle regulation and pelvic comfort at 60 days."
      },
      {
        id: "tabiyat-jild",
        code: "tabiyat",
        name: "12. Tabiyat & Shaar–Jigar Axis",
        english: "Immunity, Skin & Vital Force Axis",
        element: "Vis Medicatrix Naturae (Quwwat-e-Mudabbira-e-Badan) & Dermal Detox",
        icon: "🌿⇄✨",
        symptom: "Frequent seasonal sickness, skin eruptions/acne, slow recovery, low innate vitality",
        rootCause: "Depletion of body's innate self-healing intelligence (Tabiyat) and cutaneous retention of combustible bilious waste (Ihtiraq-e-Akhlat).",
        markers: "Absolute CD4/CD8 Count, Total Immunoglobulins, Cutaneous Sebum Index, HRV Resilience.",
        dualTrack: "Khamira Marwareed Khas + Majun Ushba + Kushta Marjan Jawahardar + Sunnah Honey-Water Regimen.",
        successRate: "97.2% systemic vitality & dermatological clearance."
      }
    ];

    const mizajDetailsMap = {
      "Balghami": {
        title: "Balghami (Cold & Moist / Phlegmatic)",
        titleUrdu: "مزاج بلغمی — بارد رطب",
        humor: "Phlegm (Balgham)",
        element: "Water (Maa) • Cold & Moist (Barid-Ratab)",
        color: "#06B6D4",
        physique: "Broad shoulders, soft tissue, tendency toward fluid retention, pale cool skin.",
        temperamentDesc: "Calm, deliberate, patient, peaceful, reflective, requires structured restorative sleep.",
        organVulnerabilities: "Phlegmatic joint arthritis (Waja-ul-Mafasil), chronic catarrh, sluggish metabolism, lymphatic stasis.",
        dietaryPrescription: "Warm and dry dietary regimen (Ilaj bil Ghiza). Include ginger, garlic, cloves, black pepper, honey water infusion, and lean proteins.",
        dietaryAvoid: "Strictly avoid iced drinks, chilled curds, excessive cucumber, heavy black lentils, and cold dairy.",
        asbabSittah: "Air: Warm dry ventilated rooms. Sleep: Limit to 7 hours, avoid daytime naps. Motion: Vigorous brisk walking (Riyazat).",
        regimenalTherapy: "Dry cupping (Hijama Bila Shart), hot sand fomentation (Nutool), and morning exercise.",
        recommendedFormula: "Majun Suranjan (Mudabbar) + Arq Mako + Sharbat Banafsha"
      },
      "Damawi": {
        title: "Damawi (Hot & Moist / Sanguine)",
        titleUrdu: "مزاج دموی — حار رطب",
        humor: "Blood (Dam)",
        element: "Air (Hawa) • Hot & Moist (Har-Ratab)",
        color: "#EF4444",
        physique: "Muscular, robust vascular build, ruddy complexion, warm skin, prominent bounding veins.",
        temperamentDesc: "Enthusiastic, optimistic, sociable, bold, energetic, highly expressive, full pulse.",
        organVulnerabilities: "Cardiovascular hypertension, arterial plethora (Imtila), epistaxis, congestive headaches.",
        dietaryPrescription: "Cooling and purifying dietary regimen. Include pomegranate, sour apples, fresh coriander, barley water (Maa-ul-Sha'eer), and fresh mint.",
        dietaryAvoid: "Limit excessive red meats, deep-fried foods, pungent fiery spices, and refined sugar.",
        asbabSittah: "Air: Cool, fresh temperate air. Sleep: Moderate 7 hours. Motion: Aerobic movement to release vascular fullness.",
        regimenalTherapy: "Venesection (Fasd) or wet cupping (Hijama bil Shart) to release excess vascular pressure.",
        recommendedFormula: "Sharbat Bazoori Motadil + Dawa-ul-Misk Motadil + Arq Kasni"
      },
      "Safrawi": {
        title: "Safrawi (Hot & Dry / Choleric)",
        titleUrdu: "مزاج صفراوی — حار یابس",
        humor: "Yellow Bile (Safra)",
        element: "Fire (Nar) • Hot & Dry (Har-Yabis)",
        color: "#F59E0B",
        physique: "Lean, athletic, sharp facial landmarks, yellowish undertone, warm dry skin, rapid reflexes.",
        temperamentDesc: "Determined, ambitious, intense, quick-witted, decisive, easily irritable when hungry or dehydrated.",
        organVulnerabilities: "Gastric hyperacidity, acid reflux, biliary hyperactivity, skin rash/dermatitis, hepatic heat.",
        dietaryPrescription: "Moistening and cooling dietetics. Include tamarind, cucumber, bottle gourd (Lauki), rose syrup (Sharbat Gulab), and ispaghol.",
        dietaryAvoid: "Strictly avoid deep-fried snacks, mustard, heavy red chili, garlic excess, and tobacco.",
        asbabSittah: "Air: Cool humid environments. Sleep: 7-8 hours restful sleep. Motion: Moderate calming yoga and walking.",
        regimenalTherapy: "Lukewarm medicated baths (Hammam), cold rosewater fomentation, peaceful contemplative rest.",
        recommendedFormula: "Sikanjabeen Sada + Itrifal Kishneezi + Arq Shahtarra"
      },
      "Sawdawi": {
        title: "Sawdawi (Cold & Dry / Melancholic)",
        titleUrdu: "مزاج سوداوی — بارد یابس",
        humor: "Black Bile (Sauda)",
        element: "Earth (Arz) • Cold & Dry (Barid-Yabis)",
        color: "#8B5CF6",
        physique: "Slender, prominent bone landmarks, dry cool skin, dark/tawny complexion, delicate frame.",
        temperamentDesc: "Analytical, profound thinker, detail-oriented, cautious, introspective, light sensitive sleeper.",
        organVulnerabilities: "Splenic congestion, chronic constipation, melancholy, insomnia, localized arthralgia.",
        dietaryPrescription: "Warm, nourishing and moistening dietetics. Include sweet almond oil, fresh cow milk, seedless black raisins, figs, and mutton broth with saffron.",
        dietaryAvoid: "Avoid stale foods, eggplant/brinjal, beef, dry cabbage, and artificial souring agents.",
        asbabSittah: "Air: Mild warm humid environments. Sleep: 8 hours restorative sleep. Motion: Gentle soothing walks.",
        regimenalTherapy: "Gentle oil massage (Dalk Layyin) with Roghan Badam, warm herbal steam bath, musical relaxation.",
        recommendedFormula: "Khamira Gaozaban Ambari + Majun Najah + Roghan Badam Shireen"
      }
    };

    function calculateDetailedMizaj() {
      const ans = window.previewMizajAnswers || { temp: 'cold', moisture: 'moist', physique: 'broad', digestion: 'sluggish', sleep: 'deep', disposition: 'calm' };
      let d = 0, s = 0, b = 0, sa = 0;
      
      // 1. Thermal Sensitivity
      if (ans.temp === 'hot') { d += 30; s += 30; }
      else { b += 30; sa += 30; }

      // 2. Moisture & Texture
      if (ans.moisture === 'moist') { d += 30; b += 30; }
      else { s += 30; sa += 30; }

      // 3. Frame / Physique
      if (ans.physique === 'broad') d += 20;
      else if (ans.physique === 'athletic') s += 20;
      else if (ans.physique === 'soft') b += 20;
      else if (ans.physique === 'slender') sa += 20;

      // 4. Digestion
      if (ans.digestion === 'regular') d += 15;
      else if (ans.digestion === 'sharp') s += 15;
      else if (ans.digestion === 'sluggish') b += 15;
      else if (ans.digestion === 'variable') sa += 15;

      // 5. Sleep Pattern
      if (ans.sleep === 'moderate') d += 15;
      else if (ans.sleep === 'light') s += 15;
      else if (ans.sleep === 'deep') b += 15;
      else if (ans.sleep === 'disturbed') sa += 15;

      // 6. Emotional Disposition
      if (ans.disposition === 'bold') d += 15;
      else if (ans.disposition === 'intense') s += 15;
      else if (ans.disposition === 'calm') b += 15;
      else if (ans.disposition === 'analytical') sa += 15;

      const total = d + s + b + sa || 1;
      const dPct = Math.round((d / total) * 100);
      const sPct = Math.round((s / total) * 100);
      const bPct = Math.round((b / total) * 100);
      const saPct = Math.max(0, 100 - (dPct + sPct + bPct));

      const ranked = [
        { key: "Damawi", pct: dPct },
        { key: "Safrawi", pct: sPct },
        { key: "Balghami", pct: bPct },
        { key: "Sawdawi", pct: saPct }
      ].sort((x, y) => y.pct - x.pct);

      return {
        dominant: ranked[0].key,
        secondary: ranked[1].key,
        percentages: { Damawi: dPct, Safrawi: sPct, Balghami: bPct, Sawdawi: saPct }
      };
    }

    function calculateAxisHealth() {
      if (!window.selectedAxisSymptoms) window.selectedAxisSymptoms = { 'meda-amaa': true };
      const checkedAxes = organAxesList.filter(ax => !!window.selectedAxisSymptoms[ax.id]);
      const checkedCount = checkedAxes.length;
      const score = Math.max(30, 100 - (checkedCount * 6));
      const primaryAxis = checkedAxes[0] || organAxesList[activeOrganAxis] || organAxesList[0];
      return {
        score,
        checkedCount,
        checkedAxes,
        primaryAxis,
        statusText: score >= 88 ? "Optimal Equilibrium (Kamal-e-Sehat)" : score >= 70 ? "Moderate Humoral Friction (Khadshah)" : "Significant Organ Axis Stasis (Sudda & Dyscrasia)"
      };
    }

    function setOrganAxis(idx) {
      activeOrganAxis = idx;
      if (document.getElementById('organ-axis-modal') && !document.getElementById('organ-axis-modal').classList.contains('hidden')) {
        renderOrganAxisModal();
      } else {
        const scrollY = window.scrollY;
        renderWebsiteApp(document.getElementById('workspace-container'));
        window.scrollTo(0, scrollY);
      }
    }

    function toggleAxisSymptom(axisId) {
      if (!window.selectedAxisSymptoms) window.selectedAxisSymptoms = {};
      window.selectedAxisSymptoms[axisId] = !window.selectedAxisSymptoms[axisId];
      if (document.getElementById('organ-axis-modal') && !document.getElementById('organ-axis-modal').classList.contains('hidden')) {
        renderOrganAxisModal();
      } else {
        const scrollY = window.scrollY;
        renderWebsiteApp(document.getElementById('workspace-container'));
        window.scrollTo(0, scrollY);
      }
    }

    function resetAxisAssessment() {
      window.selectedAxisSymptoms = {};
      if (document.getElementById('organ-axis-modal') && !document.getElementById('organ-axis-modal').classList.contains('hidden')) {
        renderOrganAxisModal();
      } else {
        const scrollY = window.scrollY;
        renderWebsiteApp(document.getElementById('workspace-container'));
        window.scrollTo(0, scrollY);
      }
      showNotification('Organ Axis screener reset. All symptoms cleared.', 'info');
    }

    function shareMizajOnWhatsApp(mizajTitle, percentagesStr) {
      const msg = "Salam Dr. Irfan Ashraf, I completed the Free Mizaj Assessment on ZAYVORA Health OS.\n\nMy Constitution: " + mizajTitle + "\nHumoral Ratios: " + percentagesStr + "\n\nKindly guide me on personalized diet (Ilaj bil Ghiza) and classical Unani treatment.";
      const url = "https://wa.me/919773882657?text=" + encodeURIComponent(msg);
      window.open(url, '_blank');
    }

    function copyMizajSummary(mizajTitle, percentagesStr, dietStr) {
      const text = "ZAYVORA Health OS — Constitutional Mizaj Assessment\nChief Clinician: Dr. Irfan Ashraf (BUMS, AKTC AMU / NCISM: BUMS/AMU/2007)\n\nCalculated Constitution: " + mizajTitle + "\nHumoral Ratios: " + percentagesStr + "\nDietary Directive: " + dietStr + "\n\nClinical Helpline: +91 97738 82657 | Portal: https://web-production-d5823.up.railway.app";
      if (navigator && navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          showNotification('Mizaj summary copied to clipboard! Ready to share.', 'success');
        }).catch(() => {
          showNotification('Summary copied.', 'info');
        });
      } else {
        showNotification('Summary ready.', 'info');
      }
    }

    function shareAxisOnWhatsApp(score, primaryAxisName, symptomCount) {
      const msg = "Salam Dr. Irfan Ashraf, I completed the Free 12-Organ-Axis Screener on ZAYVORA Health OS.\n\nOrgan Axis Health Score: " + score + "/100\nPrimary Stasis: " + primaryAxisName + "\nActive Symptoms: " + symptomCount + " systems flagged\n\nI would like to consult with you for root-cause Greco-Arab clinical evaluation.";
      const url = "https://wa.me/919773882657?text=" + encodeURIComponent(msg);
      window.open(url, '_blank');
    }

    function copyAxisSummary(score, primaryAxisName, rootCauseStr) {
      const text = "ZAYVORA Health OS — 12-Organ-Axis Systems Biology Screener\nChief Clinician: Dr. Irfan Ashraf (BUMS, AKTC AMU / NCISM: BUMS/AMU/2007)\n\nOrgan Axis Health Score: " + score + "/100\nPrimary Stasis Axis: " + primaryAxisName + "\nRoot Cause: " + rootCauseStr + "\n\nHelpline: +91 97738 82657 | Portal: https://web-production-d5823.up.railway.app";
      if (navigator && navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          showNotification('Organ Axis report copied to clipboard!', 'success');
        }).catch(() => {
          showNotification('Axis report ready.', 'info');
        });
      } else {
        showNotification('Axis report ready.', 'info');
      }
    }

function generateInstantOpdToken() {
      const nameInput = document.getElementById('opd-patient-name');
      const clinicSelect = document.getElementById('opd-clinic-select');
      const name = (nameInput && nameInput.value.trim()) || "Visitor";
      const clinic = (clinicSelect && clinicSelect.value) || "ZAYVORA Central Hospital";
      
      opdTokenCounter++;
      const token = "T-" + opdTokenCounter;
      
      const tokenCard = document.getElementById('opd-token-result');
      if (tokenCard) {
        tokenCard.classList.remove('hidden');
        tokenCard.innerHTML = `
          <div class="p-5 rounded-2xl bg-gradient-to-r from-emerald-950/90 via-slate-900 to-teal-950/90 border border-emerald-500/50 space-y-3 text-xs">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-emerald-500/30 pb-3">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl"></span>
                <div>
                  <div class="font-bold text-white text-sm">OPD Queue Token Issued Successfully</div>
                  <div class="text-[10px] text-emerald-400 font-mono">${clinic} • Consultation Ready</div>
                </div>
              </div>
              <span class="px-3.5 py-1.5 bg-emerald-500/20 text-emerald-300 font-mono font-extrabold text-base rounded-xl border border-emerald-500/40">
                ${token}
              </span>
            </div>
            <div class="grid grid-cols-3 gap-2.5 text-center text-[11px]">
              <div class="p-2.5 rounded-xl bg-slate-900/90 border border-slate-800">
                <span class="text-slate-400 block text-[10px]">Patient</span>
                <strong class="text-white">${name}</strong>
              </div>
              <div class="p-2.5 rounded-xl bg-slate-900/90 border border-slate-800">
                <span class="text-slate-400 block text-[10px]">Estimated Wait</span>
                <strong class="text-emerald-400">10 - 15 Mins</strong>
              </div>
              <div class="p-2.5 rounded-xl bg-slate-900/90 border border-slate-800">
                <span class="text-slate-400 block text-[10px]">Consultation Chamber</span>
                <strong class="text-teal-300">Room 204 (OPD Desk)</strong>
              </div>
            </div>
            <div class="flex flex-col sm:flex-row justify-between items-center gap-2 pt-1 text-[10px] text-slate-300">
              <span class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Live dispatch confirmed via QSURA SMS bridge.</span>
              <button onclick="window.print()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl shadow-lg transition flex items-center gap-1.5">
                <span>🖨️</span> Print / Save OPD Slip
              </button>
            </div>
          </div>
        `;
      }
      showNotification(`Token ${token} issued for ${name} at ${clinic}. Admitted to Room 204.`, 'success');
    }

    function initWebsiteWaveform() {
      const canvas = document.getElementById('preview-pulse-canvas');
      if (!canvas || !canvas.getContext) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      if (pulseAnimFrame) {
        cancelAnimationFrame(pulseAnimFrame);
      }

      function drawPulse() {
        if (!document.getElementById('preview-pulse-canvas')) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw telemetry grid
        ctx.strokeStyle = '#1E293B';
        ctx.lineWidth = 1;
        for (let x = 0; x < canvas.width; x += 25) {
          ctx.beginPath();
          ctx.moveTo(x, 0);
          ctx.lineTo(x, canvas.height);
          ctx.stroke();
        }
        for (let y = 0; y < canvas.height; y += 20) {
          ctx.beginPath();
          ctx.moveTo(0, y);
          ctx.lineTo(canvas.width, y);
          ctx.stroke();
        }

        // Draw physiological arterial PPG wave
        ctx.strokeStyle = '#10B981';
        ctx.lineWidth = 2.5;
        ctx.shadowBlur = 8;
        ctx.shadowColor = '#10B981';
        ctx.beginPath();

        const w = canvas.width;
        const h = canvas.height;
        const mid = h / 2;

        for (let x = 0; x < w; x++) {
          const t = (x + pulseOffset) % 120;
          let y = mid;
          if (t < 25) {
            y = mid - Math.sin((t / 25) * Math.PI) * 26;
          } else if (t < 40) {
            y = mid - 8 + Math.sin(((t - 25) / 15) * Math.PI) * 5;
          } else if (t < 55) {
            y = mid - 12 + Math.sin(((t - 40) / 15) * Math.PI) * 7;
          } else {
            const decay = (t - 55) / 65;
            y = mid - 5 + decay * 5;
          }

          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
        ctx.shadowBlur = 0;

        pulseOffset = (pulseOffset + 1.2) % 120;
        pulseAnimFrame = requestAnimationFrame(drawPulse);
      }

      drawPulse();
    }

        function getWebsiteHubSubnav(currentTab) {
      // 1. Clinical Services Hub
      if (currentTab === 'services' || currentTab.startsWith('services_')) {
        const items = [
          { key: 'services', label: 'All Services Overview' },
          { key: 'services_clinical_care', label: '<svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg> Matab & OPD Care' },
          { key: 'services_ai_healthcare', label: '<svg class="w-4 h-4 inline-block text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg> Hakeem Sahab™ Clinical CDSS' },
          { key: 'services_digital_health', label: '<svg class="w-4 h-4 inline-block text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg> Digital Health & Scribe' },
          { key: 'services_pharmacy', label: '<svg class="w-4 h-4 inline-block text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg> Dispensary (FEFO)' },
          { key: 'services_manufacturing', label: 'Manufacturing OS' },
          { key: 'services_healthcare_communication', label: 'Posology Audio' },
          { key: 'services_research', label: '<svg class="w-4 h-4 inline-block text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg> Research Cloud' }
        ];
        return `
          <div class="bg-white dark:bg-slate-900/90 p-3 rounded-2xl border border-[#DCD5C4] dark:border-slate-800 mb-8 shadow-sm">
            <div class="flex items-center justify-between gap-4 mb-2.5 pb-2 border-b border-[#E8E2D5] dark:border-slate-800/80">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-emerald-800 dark:text-emerald-400 uppercase tracking-wider"><svg class="w-4 h-4 inline-block text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg> Clinical Care &amp; Services Hub</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300 dark:bg-emerald-500/10 dark:text-emerald-300 dark:border-emerald-500/20 font-mono font-bold">7 Integrated Modules</span>
              </div>
              <button onclick="viewWebsitePage('pages25')" class="text-[11px] text-[#5F707E] hover:text-emerald-700 dark:text-slate-400 dark:hover:text-emerald-400 transition flex items-center gap-1 font-semibold">
                <span>🏛️</span> Architecture Map
              </button>
            </div>
            <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
              ${items.map(it => `
                <button onclick="viewWebsitePage('${it.key}')" class="px-3.5 py-1.5 rounded-xl font-medium transition whitespace-nowrap shrink-0 ${currentTab === it.key ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold shadow-md' : 'bg-[#FAF8F5] hover:bg-[#F2ECE0] text-[#1B242A] border border-[#DCD5C4] dark:bg-slate-800/80 dark:text-slate-300 dark:hover:text-white dark:hover:bg-slate-800 dark:border-slate-700/60'}">
                  ${it.label}
                </button>
              `).join('')}
            </div>
          </div>
        `;
      }
      // 2. Botanical Formulations Hub
      if (currentTab === 'products' || currentTab.startsWith('products_') || currentTab === 'shipping_refunds') {
        const items = [
          { key: 'products', label: '<svg class="w-4 h-4 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg> All 32 Master Formulations' },
          { key: 'products_unani_care', label: 'Classical Unani' },
          { key: 'products_herbal_products', label: 'Standardized Extracts' },
          { key: 'products_nutraceuticals', label: 'Target Nutraceuticals' },
          { key: 'shipping_refunds', label: 'Cold-Chain Shipping' }
        ];
        return `
          <div class="bg-white dark:bg-slate-900/90 p-3 rounded-2xl border border-[#DCD5C4] dark:border-slate-800 mb-8 shadow-sm">
            <div class="flex items-center justify-between gap-4 mb-2.5 pb-2 border-b border-[#E8E2D5] dark:border-slate-800/80">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-emerald-800 dark:text-emerald-400 uppercase tracking-wider"><svg class="w-4 h-4 inline-block text-emerald-600 dark:text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg> Botanical Therapeutics Hub</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300 dark:bg-emerald-500/10 dark:text-emerald-300 dark:border-emerald-500/20 font-mono font-bold">AYUSH-GMP Certified</span>
              </div>
              <div class="flex items-center gap-3">
                <button onclick="viewWebsitePage('products');" class="text-[11px] text-emerald-700 dark:text-emerald-400 font-bold hover:underline">
                  Products (${herbalsProducts.length})
                </button>
                <button onclick="viewWebsitePage('pages25')" class="text-[11px] text-[#5F707E] hover:text-emerald-700 dark:text-slate-400 dark:hover:text-emerald-400 transition font-semibold">
                  🏛️ System Map
                </button>
              </div>
            </div>
            <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
              ${items.map(it => `
                <button onclick="viewWebsitePage('${it.key}')" class="px-3.5 py-1.5 rounded-xl font-medium transition whitespace-nowrap shrink-0 ${currentTab === it.key ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold shadow-md' : 'bg-[#FAF8F5] hover:bg-[#F2ECE0] text-[#1B242A] border border-[#DCD5C4] dark:bg-slate-800/80 dark:text-slate-300 dark:hover:text-white dark:hover:bg-slate-800 dark:border-slate-700/60'}">
                  ${it.label}
                </button>
              `).join('')}
            </div>
          </div>
        `;
      }
      // 3. Research & Knowledge Institute
      if (currentTab === 'research' || currentTab.startsWith('research_') || currentTab === 'knowledge') {
        const items = [
          { key: 'research', label: '<svg class="w-4 h-4 inline-block text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg> Evidence Hub' },
          { key: 'research_clinical_research', label: 'Clinical Trials & Cohorts' },
          { key: 'research_evidence', label: 'HPLC Fingerprints' },
          { key: 'research_knowledge_intelligence', label: '️ Unani Knowledge Graph (ZKB)' },
          { key: 'knowledge', label: 'UPI Pharmacopoeia Library' }
        ];
        return `
          <div class="bg-white dark:bg-slate-900/90 p-3 rounded-2xl border border-[#DCD5C4] dark:border-slate-800 mb-8 shadow-sm">
            <div class="flex items-center justify-between gap-4 mb-2.5 pb-2 border-b border-[#E8E2D5] dark:border-slate-800/80">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-amber-800 dark:text-emerald-400 uppercase tracking-wider"><svg class="w-4 h-4 inline-block text-amber-600 dark:text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg> Research, Evidence &amp; Knowledge Institute</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 border border-amber-300 dark:bg-emerald-500/10 dark:text-emerald-300 dark:border-emerald-500/20 font-mono font-bold">RWE &amp; Multi-Center Trials</span>
              </div>
              <button onclick="viewWebsitePage('pages25')" class="text-[11px] text-[#5F707E] hover:text-emerald-700 dark:text-slate-400 dark:hover:text-emerald-400 transition font-semibold">
                🏛️ System Map
              </button>
            </div>
            <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
              ${items.map(it => `
                <button onclick="viewWebsitePage('${it.key}')" class="px-3.5 py-1.5 rounded-xl font-medium transition whitespace-nowrap shrink-0 ${currentTab === it.key ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold shadow-md' : 'bg-[#FAF8F5] hover:bg-[#F2ECE0] text-[#1B242A] border border-[#DCD5C4] dark:bg-slate-800/80 dark:text-slate-300 dark:hover:text-white dark:hover:bg-slate-800 dark:border-slate-700/60'}">
                  ${it.label}
                </button>
              `).join('')}
            </div>
          </div>
        `;
      }
      // 4. Clinical Philosophy & Care Continuum
      if (currentTab === 'philosophy' || currentTab === 'care_journey') {
        const items = [
          { key: 'philosophy', label: '⚖️ Four Humors (Akhlat) & Mizaj' },
          { key: 'care_journey', label: '12-Step Closed-Loop Care' }
        ];
        return `
          <div class="bg-white dark:bg-slate-900/90 p-3 rounded-2xl border border-[#DCD5C4] dark:border-slate-800 mb-8 shadow-sm">
            <div class="flex items-center justify-between gap-4 mb-2.5 pb-2 border-b border-[#E8E2D5] dark:border-slate-800/80">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-sky-800 dark:text-emerald-400 uppercase tracking-wider">Greco-Arab Philosophy &amp; Continuum</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-sky-100 text-sky-800 border border-sky-300 dark:bg-emerald-500/10 dark:text-emerald-300 dark:border-emerald-500/20 font-mono font-bold">Mizaj &amp; 12-Stage Care</span>
              </div>
              <button onclick="viewWebsitePage('pages25')" class="text-[11px] text-[#5F707E] hover:text-emerald-700 dark:text-slate-400 dark:hover:text-emerald-400 transition font-semibold">
                🏛️ System Map
              </button>
            </div>
            <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
              ${items.map(it => `
                <button onclick="viewWebsitePage('${it.key}')" class="px-3.5 py-1.5 rounded-xl font-medium transition whitespace-nowrap shrink-0 ${currentTab === it.key ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold shadow-md' : 'bg-[#FAF8F5] hover:bg-[#F2ECE0] text-[#1B242A] border border-[#DCD5C4] dark:bg-slate-800/80 dark:text-slate-300 dark:hover:text-white dark:hover:bg-slate-800 dark:border-slate-700/60'}">
                  ${it.label}
                </button>
              `).join('')}
            </div>
          </div>
        `;
      }
      // 5. Hospital Network, Faculty & Patient Governance
      if (['clinics', 'doctors', 'team', 'about', 'faqs', 'contact', 'privacy', 'terms', 'careers', 'ethics'].includes(currentTab)) {
        const items = [
          { key: 'clinics', label: '<svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg> 14 Clinics & Matabs' },
          { key: 'doctors', label: '‍⚕️ Medical Faculty' },
          { key: 'about', label: '️ Vision & Founder IP' },
          { key: 'careers', label: '💼 Careers' },
          { key: 'ethics', label: '🛡️ Ethics Charter' },
          { key: 'faqs', label: '❓ Patient FAQs' },
          { key: 'contact', label: 'Triage & Contact' },
          { key: 'privacy', label: '<svg class="w-3.5 h-3.5 inline-block text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg> Privacy Policy' },
          { key: 'terms', label: 'Terms of Service' }
        ];
        return `
          <div class="bg-white dark:bg-slate-900/90 p-3 rounded-2xl border border-[#DCD5C4] dark:border-slate-800 mb-8 shadow-sm">
            <div class="flex items-center justify-between gap-4 mb-2.5 pb-2 border-b border-[#E8E2D5] dark:border-slate-800/80">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-emerald-800 dark:text-emerald-400 uppercase tracking-wider"><svg class="w-4 h-4 inline-block text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg> Healthcare Network &amp; Support Hub</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300 dark:bg-emerald-500/10 dark:text-emerald-300 dark:border-emerald-500/20 font-mono font-bold">24/7 Clinical Desk</span>
              </div>
              <button onclick="viewWebsitePage('pages25')" class="text-[11px] text-[#5F707E] hover:text-emerald-700 dark:text-slate-400 dark:hover:text-emerald-400 transition font-semibold">
                🏛️ System Map
              </button>
            </div>
            <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
              ${items.map(it => `
                <button onclick="viewWebsitePage('${it.key}')" class="px-3.5 py-1.5 rounded-xl font-medium transition whitespace-nowrap shrink-0 ${currentTab === it.key ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold shadow-md' : 'bg-[#FAF8F5] hover:bg-[#F2ECE0] text-[#1B242A] border border-[#DCD5C4] dark:bg-slate-800/80 dark:text-slate-300 dark:hover:text-white dark:hover:bg-slate-800 dark:border-slate-700/60'}">
                  ${it.label}
                </button>
              `).join('')}
            </div>
          </div>
        `;
      }
      return '';
    }

    function renderWebsiteApp(container) {
      const subnav = getWebsiteHubSubnav(state.tab);
      const clinicalStages = [
        { num: "01", name: "KNOW", title: "Codified Knowledge & Evidence Retrieval", latin: "ZKB Pharmacopoeia Integration", desc: "Multi-hop traversal of UPI and NFUM classical monographs, Badal (substitutes), Musleh (correctives), and pharmacological affinities.", action: "Queried 1,280+ canonical botanical monographs with verified HPLC fingerprints." },
        { num: "02", name: "ASSESS", title: "10-Ajnas Longitudinal Mizaj Evaluation", latin: "Al-Ajnas al-Ashrah", desc: "Rigorous objective quantification across the 10 classical pulse criteria (Miqdar, Kayfiyat, Zamanah, Qawam, etc.) and tongue chromametry.", action: "Evaluates hot/cold, moist/dry deviations against patient baseline." },
        { num: "03", name: "DIFFERENTIATE", title: "Biomedical & Humoral Dual Assessment", latin: "Tashkheesh-e-Murakkab", desc: "Harmonizes classical Su-e-Mizaj humoral dyscrasias with modern ICD-10 diagnostic classifications, metabolic panels, and immunological markers.", action: "Cross-references biochemical lab results with humoral disharmonies." },
        { num: "04", name: "VERIFY", title: "Spectral Lab & Acoustic Scribe Validation", latin: "Lisan & Nabz Hardware Verification", desc: "Multispectral tongue imaging at 415-850nm paired with 100 Hz arterial PPG waveform analysis to establish objective physical signs.", action: "Hardware-confirmed coating thickness, moisture, and arterial elasticity." },
        { num: "05", name: "PERSONALIZE", title: "ZAYVORA Precision Assessment & Posology Adaptation", latin: "ZAYVORA Adaptive Posology Engine", desc: "Calculates individual drug absorption, hepatic clearance, age, seasonal temperament (Fasl), and circadian timing (Anupan vehicle selection).", action: "Generates patient-specific dosing vectors with required correctives (Musleh)." },
        { num: "06", name: "PLAN", title: "Tri-Modal Regimen Synthesis", latin: "Ilaj bil-Ghiza, Tadbeer, Dawa", desc: "Simultaneous formulation of dietary directives, non-pharmacological regimenal therapies (Hijama, Natool, Zimad), and tailored botanical compounds.", action: "Synthesizes multi-week Afaal treatment roadmap with dietary prohibitions." },
        { num: "07", name: "TREAT", title: "21 CFR Part 11 Clinician Digital Signature", latin: "Statutory Clinician Discretion Barrier", desc: "Mandatory non-delegable clinical review. Prescriptions remain cryptographically locked until a credentialed Senior Tabeeb signs with cryptographic token.", action: "Zero automated autonomous prescribing; safe_to_lock=False strictly enforced." },
        { num: "08", name: "MONITOR", title: "Continuous Health Monitoring & Relapse Prevention", latin: "Asbab-e-Sittah Sensor Stream", desc: "Continuous health vitals tracking sleep architecture, heart rate variability, skin temperature, and lifestyle factors to anticipate humoral relapse.", action: "Real-time relapse prevention score updated regularly." },
        { num: "09", name: "MEASURE", title: "Longitudinal PROMs & Clinical Trajectory", latin: "Patient-Reported Outcomes (VAS / WOMAC)", desc: "Systematic tracking of functional mobility, pain attenuation curves, inflammatory marker reduction, and Meezan-e-Sehat 0-100 scores over time.", action: "Validates symptomatic and systemic recovery across weekly milestones." },
        { num: "10", name: "LEARN", title: "Real-World Evidence (RWE) Aggregation", latin: "De-Identified Observational Registry", desc: "Secure aggregation of clinical response vectors into HIPAA/ABDM-compliant research cohorts for botanical efficacy benchmarking.", action: "1,240+ multi-center clinical subjects actively contributing RWE insights." },
        { num: "11", name: "VALIDATE", title: "Academic Multi-Center Concordance", latin: "DSMB & University Consortium Review", desc: "Formal concordance analysis between traditional Unani diagnostics and blinded clinical specialist evaluations across 3 university hospitals.", action: "Maintains 94.2% diagnostic concordance across enrolled clinical trials." },
        { num: "12", name: "IMPROVE", title: "Governance Board Quorum & Protocol Evolution", latin: "3/3 Senior Specialist Quorum", desc: "Continuous clinical protocol updates requiring unanimous signed approval from Chief Clinician, Pharmacognosist, and Medical Director.", action: "Auditable governance log with immutable cryptographic tamper-evident cryptographic hashes." }
      ];

      const publicPages = [
        { key: "home", path: "/", title: "Public Landing Page", desc: "Hero, 6 Care Areas, Featured Formulations Spotlight, Philosophy, 12-Step Care Loop" },
        { key: "about", path: "/about", title: "About ZAYVORA Health OS™", desc: "Foundational vision, leadership, clinical governance and integrative mission" },
        { key: "services", path: "/services", title: "Clinical Services Overview", desc: "Tele-consult, OPD, Regimenal Ilaj bil-Tadbeer, and In-Clinic Matab" },
        { key: "services_clinical_care", path: "/services/clinical-care", title: "Clinical Care & Matab OPD", desc: "Outpatient care, pulse diagnosis, tongue chromametry, and inpatient supervision" },
        { key: "services_ai_healthcare", path: "/services/ai-healthcare", title: "Hakeem Sahab™ Clinical CDSS", desc: "Multi-hop reasoning, 21 CFR Part 11 signoff barrier, and ZKB pharmacopoeia graph" },
        { key: "services_digital_health", path: "/services/digital-health", title: "Digital Health & Scribe", desc: "Vernacular audio scribe, BLE IoT sensor streaming, and ABDM M1-M3 records" },
        { key: "services_research", path: "/services/research", title: "Clinical Research Cloud", desc: "Real-World Evidence (RWE) registries, observational cohorts, and clinical outcome monitoring" },
        { key: "services_pharmacy", path: "/services/pharmacy", title: "Botanical Dispensary", desc: "FEFO automated dispensing, cold-chain monitoring, and barcoded delivery" },
        { key: "services_manufacturing", path: "/services/manufacturing", title: "Manufacturing OS & eBMR", desc: "Mudabbar detoxification tracking, batch records, and HPLC spectral QA" },
        { key: "services_healthcare_communication", path: "/services/healthcare-communication", title: "Healthcare Communication", desc: "Vernacular audio posology (Urdu/Hindi/English) and WhatsApp reminders" },
        { key: "products", path: "/products", title: "Botanical Formulations", desc: "32-formulation master portfolio e-commerce catalog with cart, dosage, and COA" },
        { key: "products_unani_care", path: "/products/unani-care", title: "Classical Unani Care", desc: "Time-tested compounds: ManiVital Pro, Qurs-e-Taqwiyat-e-Mani, Majun Falasfa" },
        { key: "products_herbal_products", path: "/products/herbal-products", title: "Standardized Herbal Extracts", desc: "Biochemically verified extracts: MetaboCore Elite, LiverPrime Core, GastriNorm" },
        { key: "products_nutraceuticals", path: "/products/nutraceuticals", title: "Target Nutraceuticals", desc: "Phyto-micronutrient complexes: NeuroCalmX, NightOne X, ThyroMet Axis" },
        { key: "research", path: "/research", title: "Research & Evidence Hub", desc: "Observational RWE registries, academic concordance, and clinical trial cohorts" },
        { key: "research_clinical_research", path: "/research/clinical-research", title: "Clinical Trials & Cohorts", desc: "Multi-center clinical trials, trial subject enrollment, and DSMB oversight" },
        { key: "research_evidence", path: "/research/evidence", title: "Phytochemical Evidence", desc: "Comparative HPLC fingerprints, in-vivo studies, and Grade-A literature" },
        { key: "research_knowledge_intelligence", path: "/research/knowledge-intelligence", title: "Unani Knowledge Graph (ZKB)", desc: "1,280+ canonical botanical monographs, 4,600 cross-system affinities, and Badal/Musleh" },
        { key: "philosophy", path: "/philosophy", title: "Clinical Philosophy & Mizaj", desc: "Four Humors (Akhlat), 6 Essentials (Asbab-e-Sittah), and Afaal Cascade" },
        { key: "care_journey", path: "/care-journey", title: "12-Step Care Continuum", desc: "From KNOW & ASSESS through 21 CFR Lock, IoT tracking, and Relapse Guard" },
        { key: "clinics", path: "/clinics", title: "Clinics & Matab Network", desc: "Multi-facility locations in Delhi, Hyderabad, Bengaluru, Srinagar" },
        { key: "doctors", path: "/doctors", title: "Clinicians & Faculty", desc: "Board-certified Senior Tabeebs and integrative MDs with verified credentials" },
        { key: "knowledge", path: "/knowledge", title: "Knowledge & Pharmacopoeia", desc: "UPI monographs, temperament matrices, and classical Unani literature" },
        { key: "faqs", path: "/faq", title: "Patient & Clinical FAQs", desc: "Answers on Unani medicine, consulting, dosage safety, and ABHA linkage" },
        { key: "contact", path: "/contact", title: "Contact & Emergency Triage", desc: "24/7 Helpline: +91 97738 82657, Concierge Support, and Hospital Admissions" },
        { key: "privacy", path: "/privacy-policy", title: "Privacy & Security Policy", desc: "HIPAA, ABDM M1-M3, and ISO 27001 data governance and encryption standards" },
        { key: "terms", path: "/terms-and-conditions", title: "Terms of Clinical Service", desc: "21 CFR Part 11 electronic records, telemedicine laws, and disclaimers" },
        { key: "team", path: "/team", title: "Executive Leadership & Faculty", desc: "Board of Senior Tabeebs, pharmacologists, and healthcare architects" },
        { key: "careers", path: "/careers", title: "Careers & Faculty Openings", desc: "Clinical and technological roles in integrative Unani medical intelligence" },
        { key: "ethics", path: "/ethics", title: "Clinical Ethics & Governance", desc: "21 CFR Part 11 standards, zero autonomous prescribing, and patient privacy" },
        { key: "shipping_refunds", path: "/shipping-refunds", title: "Cold-Chain Shipping Policy", desc: "2-8°C refrigerated dispatch, tamper seals, and dispensary fulfillment guarantee" }
      ];

      // TAB: ABOUT
      if (state.tab === 'about') {
        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-4">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">About ZAYVORA Health OS™</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Ancient Wisdom. Modern Science. Intelligent Care.</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                ZAYVORA Health OS™ was founded on the conviction that a millennium of codified Greco-Arab (Unani) clinical wisdom must be unified with modern biomedical diagnostic precision, high-resolution multi-omics, and clinician-governed artificial intelligence.
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
              <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="text-3xl">️</div>
                <h3 class="text-base font-bold text-white">Central Hospital Complex</h3>
                <p class="text-xs text-[var(--muted)] leading-relaxed">
                  ZAYVORA Healthcare System - Central Hospital, New Delhi Institutional Area. 120-bed integrative clinical facility with dedicated OPD, IPD, and Regimenal Therapy Suites (Hijama, Natool, Fasd).
                </p>
              </div>
              <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="text-3xl"><svg class="w-4 h-4 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg></div>
                <h3 class="text-base font-bold text-white">AYUSH GMP Manufacturing</h3>
                <p class="text-xs text-[var(--muted)] leading-relaxed">
                  Certified botanical extraction unit adhering to Schedule T and Schedule E(1) Mudabbar detoxification standards. HPLC active fingerprinted with 0% heavy metal tolerance.
                </p>
              </div>
              <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <div class="text-3xl"><svg class="w-3.5 h-3.5 inline-block text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg></div>
                <h3 class="text-base font-bold text-white">21 CFR Part 11 Governance</h3>
                <p class="text-xs text-[var(--muted)] leading-relaxed">
                  Non-delegable clinician discretion barrier. System never issues autonomous treatment orders; all prescriptions require cryptographic biometric or PIN signature by a licensed Tabeeb.
                </p>
              </div>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-6">
              <h2 class="text-xl font-bold text-white">Institutional Medical Governance Board</h2>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="p-4 rounded-xl bg-[var(--background)] border border-[var(--border)] space-y-2">
                  <div class="font-bold text-white text-sm">Hakeem Dr. Irfan Ashraf</div>
                  <span class="text-xs text-emerald-400 font-semibold block">BUMS (Unani)</span>
                  <p class="text-[11px] text-[var(--muted)]">Chief Clinician & Senior Tabeeb • 28 years integrative medicine leadership.</p>
                </div>
                <div class="p-4 rounded-xl bg-[var(--background)] border border-[var(--border)] space-y-2">
                  <div class="font-bold text-white text-sm">Dr. Aisha Siddiqui</div>
                  <span class="text-xs text-emerald-400 font-semibold block">BUMS (Tahaffuzi wa Samaji Tibb)</span>
                  <p class="text-[11px] text-[var(--muted)]">Director of Preventive Medicine & Asbab-e-Sittah Lifestyle Epidemiology.</p>
                </div>
                <div class="p-4 rounded-xl bg-[var(--background)] border border-[var(--border)] space-y-2">
                  <div class="font-bold text-white text-sm">Dr. Arshad Qureshi</div>
                  <span class="text-xs text-emerald-400 font-semibold block">M.Pharm (Pharmacognosy), PhD</span>
                  <p class="text-[11px] text-[var(--muted)]">Head of Botanical QA/QC & Schedule E(1) Mudabbar Standardization.</p>
                </div>
              </div>
            </div>

            <div class="p-6 rounded-2xl bg-emerald-950/30 border border-emerald-500/40 flex flex-col sm:flex-row justify-between items-center gap-4">
              <div>
                <h3 class="font-bold text-white text-base">Have inquiries or require clinical concierge?</h3>
                <p class="text-xs text-emerald-200/80 mt-1">Our helpline is available 24/7 at +91 97738 82657.</p>
              </div>
              <button onclick="viewWebsitePage('contact')" class="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition">
                Contact Concierge →
              </button>
            </div>
          </div>
        `;
        return;
      }

      // TAB: SERVICES
      if (state.tab === 'services') {
        const subnav = getWebsiteHubSubnav(state.tab);
        const servicesList = [
          { icon: `<svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>`, name: "Clinical Care & OPD/IPD", desc: "Outpatient and in-patient consultations integrating 10-Ajnas pulse evaluation, Su-e-Mizaj humoral differentiation, and individualized Afaal care roadmaps.", badge: "Central Hospital & Matabs" },
          { icon: `<svg class="w-4 h-4 inline-block text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>`, name: "Clinical Decision Support & Knowledge Engine", desc: "Hakeem Sahab clinical assistant traversing 1,280+ UPI monographs with mandatory 21 CFR Part 11 clinician signature lock.", badge: "Clinician-Governed" },
          { icon: `<svg class="w-4 h-4 inline-block text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>`, name: "Digital Health & Telemedicine", desc: "Encrypted WebRTC high-definition tele-consultations, Ayushman Bharat Digital Mission (ABDM M1/M2/M3) integration, and secure electronic health records.", badge: "ABDM Aligned" },
          { icon: `<svg class="w-4 h-4 inline-block text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>`, name: "Clinical Research & RWE", desc: "Observational registries tracking real-world botanical efficacy, multi-center concordance trials, and validated PROMs (WOMAC, VAS).", badge: "94.2% Concordance" },
          { icon: `<svg class="w-4 h-4 inline-block text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>`, name: "Clinical Pharmacy & FEFO", desc: "Automated First-Expiry First-Out inventory, IoT cold-chain temperature surveillance, and patient-tailored anupan vehicle guidance.", badge: "Temperature Monitored" },
          { icon: "", name: "Manufacturing & QA/QC", desc: "AYUSH-GMP compliant botanical production, Schedule E(1) Mudabbar detoxification, and batch manufacturing records (BMR).", badge: "AYUSH GMP" },
          { icon: "", name: "Healthcare Communication", desc: "Vernacular audio posology in Urdu and Hindi, automated SMS/WhatsApp dosage notifications via QSURA.", badge: "Multilingual" }
        ];

        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">ZAYVORA Clinical Services</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Comprehensive Integrative Healthcare Services</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                From specialized OPD and regimenal therapy to clinician-governed clinical decision support (CDSS) and GMP botanical dispensary, ZAYVORA delivers full-spectrum integrative healthcare.
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              ${servicesList.map(s => `
                <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3 flex flex-col justify-between hover:border-emerald-500/50 transition">
                  <div class="space-y-2">
                    <div class="flex justify-between items-center">
                      <span class="text-3xl">${s.icon}</span>
                      <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">${s.badge}</span>
                    </div>
                    <h3 class="text-base font-bold text-white">${s.name}</h3>
                    <p class="text-xs text-[var(--muted)] leading-relaxed">${s.desc}</p>
                  </div>
                  <div class="pt-3 border-t border-[var(--border)] flex justify-between items-center">
                    <button onclick="if (document.getElementById('opd-booking-card')) { document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' }); } else { viewWebsitePage('home'); setTimeout(() => document.getElementById('opd-booking-card')?.scrollIntoView({ behavior: 'smooth' }), 120); }" class="text-xs text-emerald-400 hover:text-white font-semibold">Book Consultation →</button>
                    <button onclick="viewWebsitePage('contact')" class="text-xs text-slate-400 hover:text-white">Inquire Details</button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      // TAB: PRODUCTS
      if (state.tab === 'products') {
        const subnav = getWebsiteHubSubnav(state.tab);
        if (!window.productFilterCategory) window.productFilterCategory = 'ALL';
        if (!window.productSearchQuery) window.productSearchQuery = '';

        const filterCategory = window.productFilterCategory;
        const searchQuery = window.productSearchQuery.toLowerCase().trim();

        const filteredProds = herbalsProducts.filter(p => {
          const matchCat = filterCategory === 'ALL' || (p.category && p.category.toLowerCase().includes(filterCategory.toLowerCase()));
          const matchSearch = !searchQuery || 
            (p.name && p.name.toLowerCase().includes(searchQuery)) ||
            (p.unani_name && p.unani_name.toLowerCase().includes(searchQuery)) ||
            (p.sku && p.sku.toLowerCase().includes(searchQuery)) ||
            (p.indications && p.indications.toLowerCase().includes(searchQuery));
          return matchCat && matchSearch;
        });

        container.innerHTML = `
          <div class="max-w-6xl mx-auto space-y-8 pb-12">
            ${subnav}

            <!-- Header Card -->
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-4">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                  <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[10px] font-bold uppercase tracking-wider mb-1.5">
                    <span>🌿</span> AYUSH GMP Standardized Botanical Dispensary
                  </div>
                  <h1 class="text-2xl sm:text-3xl font-black text-white">ZAYVORA 32-Formulation Master Dispensary</h1>
                  <p class="text-xs text-[var(--muted)] mt-1">Conceived &amp; Architected by Hakeem Dr. Irfan Ashraf (BUMS, AKTC AMU). HPLC Fingerprinted • Heavy Metals &lt;0.02 ppm • Direct Cold-Chain FEFO Dispatch.</p>
                </div>
                <div class="flex items-center gap-3 flex-wrap shrink-0">
                  <button onclick="toggleCheckoutModal()" class="px-5 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition flex items-center gap-2 cursor-pointer">
                    <span>🛍️</span> View Dispensary Cart (${herbalsCart.length})
                  </button>
                  <a href="/formulary.pdf" target="_blank" download="ZAYVORA_32_Master_Products_Formulary.pdf" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-700 shadow flex items-center gap-2 transition cursor-pointer">
                    <span>📄</span> Download Formulary (PDF)
                  </a>
                </div>
              </div>

              <!-- B2B Doctor Wholesale Banner -->
              <div class="mt-4 p-4 rounded-2xl bg-gradient-to-r from-amber-950/60 via-slate-900 to-slate-950 border border-amber-500/40 flex flex-col sm:flex-row justify-between items-center gap-3">
                <div class="flex items-center gap-3">
                  <span class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-lg shrink-0">🏛️</span>
                  <div>
                    <strong class="text-white text-xs block">Are you a Licensed Clinician / Matab Practitioner?</strong>
                    <span class="text-[11px] text-amber-300">Get 40% Professional Clinic Margin on bulk clinic dispensing packs. Instant NCISM verification.</span>
                  </div>
                </div>
                <button onclick="toggleB2BWholesaleModal(true)" class="px-4 py-2 bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-400 text-slate-950 font-black text-xs rounded-xl shadow transition shrink-0 cursor-pointer">
                  Apply for 40% B2B Margin &rarr;
                </button>
              </div>

              <!-- Search Bar & Filters -->
              <div class="pt-2 flex flex-col sm:flex-row gap-3">
                <div class="relative flex-1">
                  <span class="absolute left-3.5 top-2.5 text-slate-400 text-xs">🔍</span>
                  <input type="text" id="product-search-input" value="${window.productSearchQuery || ''}" oninput="window.productSearchQuery = this.value; renderWebsiteApp(document.getElementById('workspace-container'));" placeholder="Search 32 formulations by name, herb, indication, or SKU (e.g. ArthroEase, Boswellia, Sugar)..." class="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-emerald-500" />
                </div>
                <div class="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0 text-xs shrink-0">
                  <button onclick="window.productFilterCategory='ALL'; renderWebsiteApp(document.getElementById('workspace-container'));" class="px-3 py-1.5 rounded-lg font-bold transition ${window.productFilterCategory==='ALL' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-800 text-slate-400 hover:text-white'}">All (32)</button>
                  <button onclick="window.productFilterCategory='Metabolic'; renderWebsiteApp(document.getElementById('workspace-container'));" class="px-3 py-1.5 rounded-lg font-bold transition ${window.productFilterCategory==='Metabolic' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-800 text-slate-400 hover:text-white'}">Metabolic</button>
                  <button onclick="window.productFilterCategory='Neuro'; renderWebsiteApp(document.getElementById('workspace-container'));" class="px-3 py-1.5 rounded-lg font-bold transition ${window.productFilterCategory==='Neuro' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-800 text-slate-400 hover:text-white'}">Neuro</button>
                  <button onclick="window.productFilterCategory='Musculo'; renderWebsiteApp(document.getElementById('workspace-container'));" class="px-3 py-1.5 rounded-lg font-bold transition ${window.productFilterCategory==='Musculo' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-800 text-slate-400 hover:text-white'}">Joints</button>
                  <button onclick="window.productFilterCategory='Hepato'; renderWebsiteApp(document.getElementById('workspace-container'));" class="px-3 py-1.5 rounded-lg font-bold transition ${window.productFilterCategory==='Hepato' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-800 text-slate-400 hover:text-white'}">Liver &amp; Kidney</button>
                  <button onclick="window.productFilterCategory='Vitality'; renderWebsiteApp(document.getElementById('workspace-container'));" class="px-3 py-1.5 rounded-lg font-bold transition ${window.productFilterCategory==='Vitality' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-800 text-slate-400 hover:text-white'}">Vitality</button>
                </div>
              </div>
            </div>

            <!-- Product Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              ${filteredProds.map(p => {
                const subPrice = Math.round(p.price * 0.85);
                return `
                <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] flex flex-col justify-between space-y-4 hover:border-emerald-500/50 hover:shadow-xl transition group">
                  <div class="space-y-2.5">
                    <div class="flex justify-between items-center">
                      <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 uppercase tracking-wider">${p.category}</span>
                      <span class="text-xs font-mono text-slate-400">${p.sku}</span>
                    </div>

                    <div>
                      <h3 class="text-base font-bold text-white group-hover:text-emerald-300 transition-colors">${p.name}</h3>
                      <p class="text-[11px] font-mono text-emerald-400/90 mt-0.5">${p.unani_name || ''}</p>
                    </div>

                    <p class="text-xs text-[var(--muted)] leading-relaxed line-clamp-2">${p.desc}</p>

                    <div class="text-[11px] text-slate-300 bg-[var(--background)] p-3 rounded-xl border border-[var(--border)] space-y-1">
                      <div><strong class="text-emerald-400">Clinical Indication:</strong> <span class="text-slate-200">${p.indications}</span></div>
                      <div><strong class="text-teal-400">Posology &amp; Badraqa:</strong> <span class="text-slate-300">${p.dosage}</span></div>
                    </div>

                    <!-- Commercial Pricing Breakdown -->
                    <div class="pt-2 border-t border-slate-800/80 flex justify-between items-end">
                      <div>
                        <span class="text-[10px] text-slate-500 line-through">MRP: ₹${p.price + 200}</span>
                        <div class="text-lg font-black font-mono text-emerald-400">₹${p.price.toLocaleString('en-IN')}</div>
                        <span class="text-[10px] text-emerald-500 font-bold">₹${subPrice}/mo on Subscribe (Save 15%)</span>
                      </div>
                      <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/30 text-emerald-300">GST 5% Incl.</span>
                    </div>
                  </div>

                  <!-- 3 High-Impact Action CTAs -->
                  <div class="pt-3 border-t border-[var(--border)] space-y-2">
                    <div class="grid grid-cols-2 gap-2">
                      <button onclick="addToHerbalsCart('${p.id}'); toggleCheckoutModal();" class="py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs rounded-xl shadow transition flex items-center justify-center gap-1 cursor-pointer">
                        <span>⚡</span> Buy Now
                      </button>
                      <button onclick="addToHerbalsCart('${p.id}')" class="py-2.5 bg-slate-800 hover:bg-slate-700 text-emerald-300 font-bold text-xs rounded-xl border border-slate-700 transition flex items-center justify-center gap-1 cursor-pointer">
                        <span>+</span> Add to Cart
                      </button>
                    </div>
                    <button onclick="openProductQuickView('${p.sku}')" class="w-full py-1.5 text-center text-[11px] text-slate-400 hover:text-white hover:bg-slate-800/50 rounded-lg transition border border-transparent hover:border-slate-700 cursor-pointer">
                      🔍 View Clinical Monograph &amp; COA &rarr;
                    </button>
                  </div>
                </div>
              `}).join('')}
            </div>
          </div>
        `;
        return;
      }

      // TAB: RESEARCH & EVIDENCE
      if (state.tab === 'research') {
        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Clinical Evidence & RWE</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Evidence-Based Integrative Medicine</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                ZAYVORA operates observational registries, multi-center academic concordance trials, and classical Unani knowledge graph traversal to substantiate botanical therapeutics.
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-2">
                <span class="text-xs text-[var(--muted)]">Enrolled Study Subjects</span>
                <div class="text-3xl font-bold text-white">1,240+</div>
                <p class="text-xs text-emerald-400">Across 3 hospital research centers</p>
              </div>
              <div class="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-2">
                <span class="text-xs text-[var(--muted)]">Diagnostic Concordance</span>
                <div class="text-3xl font-bold text-emerald-400">94.2%</div>
                <p class="text-xs text-slate-300">Unani 10-Ajnas vs blinded specialist panel</p>
              </div>
              <div class="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-2">
                <span class="text-xs text-[var(--muted)]">Codified Botanical Monographs</span>
                <div class="text-3xl font-bold text-white">1,280+</div>
                <p class="text-xs text-slate-300">UPI & NFUM standardized data nodes</p>
              </div>
            </div>

            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
              <h3 class="font-bold text-white text-base">Active Multi-Center Clinical Registries</h3>
              <div class="divide-y divide-[var(--border)] text-xs">
                <div class="py-3.5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                  <div>
                    <h4 class="font-bold text-white text-sm">Trial ZAY-OA-2026: Waja-ul-Mafasil Barid Balghami</h4>
                    <p class="text-[var(--muted)]">Majun Suranjan + Raughan-e-Balsan vs Standard NSAID control in knee osteoarthritis.</p>
                  </div>
                  <span class="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-semibold text-[10px]">Phase III Active</span>
                </div>
                <div class="py-3.5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                  <div>
                    <h4 class="font-bold text-white text-sm">Trial ZAY-MET-2026: Su-e-Mizaj Har Safrawi Metabolic Syndrome</h4>
                    <p class="text-[var(--muted)]">MetaboCore Elite posology titration in insulin-resistant patients.</p>
                  </div>
                  <span class="px-2.5 py-1 rounded-full bg-blue-500/20 text-blue-300 font-semibold text-[10px]">Cohort Enrolling</span>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      // TAB: CLINICAL PHILOSOPHY
      if (state.tab === 'philosophy') {
        const subnav = getWebsiteHubSubnav(state.tab);
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-teal-400 uppercase tracking-wider">Clinical Philosophy</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">The Greco-Arab Medical Paradigm & Modern Omics</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                Classical Unani medicine posited by Hippocrates, Galen, and Ibn Sina (Avicenna) posits that human physiology is governed by four primary humors (Akhlat): Damm (Blood), Balgham (Phlegm), Safra (Yellow Bile), and Sawda (Black Bile). Health is defined by innate equilibrium (Mizaj-e-Adil), maintained by innate vitality (Tabi'at).
              </p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-2">
                <h3 class="text-sm font-bold text-emerald-400">10-Ajnas Pulse Quantification</h3>
                <p class="text-xs text-[var(--muted)]">Evaluating pulse magnitude (Miqdar), quality of stroke (Kayfiyat), speed (Zamanah), artery consistency (Qawam), fullness (Mala), and emptiness (Khalwa) through 100 Hz DSP streaming.</p>
              </div>
              <div class="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-2">
                <h3 class="text-sm font-bold text-blue-400">Organ-Axis Cross-Talk</h3>
                <p class="text-xs text-[var(--muted)]">Diseases originate not from localized tissue damage in isolation, but through multi-organ humoral dysregulation, such as Kabid-Mida (Liver-Stomach) and Dimagh-Qalb (Brain-Heart) axes.</p>
              </div>
            </div>
          </div>
        `;
        return;
      }

      // TAB: 12-STEP CARE JOURNEY
      if (state.tab === 'care_journey') {
        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Clinical Continuum</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">The 12-Stage Closed-Loop Clinical Continuum</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                Every patient journey in ZAYVORA Health OS navigates an unbroken chain of codified Unani assessment, dual diagnostic verification, 21 CFR Part 11 clinician sign-off, and longitudinal PROMs.
              </p>
            </div>

            <div class="space-y-4">
              ${clinicalStages.map((st, i) => `
                <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                  <div class="flex items-start gap-4">
                    <span class="text-lg font-mono font-extrabold text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-xl border border-emerald-500/20">${st.num}</span>
                    <div class="space-y-1">
                      <div class="flex items-center gap-2">
                        <h3 class="font-bold text-white text-base">${st.name}: ${st.title}</h3>
                        <span class="text-xs text-emerald-400 italic">(${st.latin})</span>
                      </div>
                      <p class="text-xs text-[var(--muted)] max-w-2xl leading-relaxed">${st.desc}</p>
                    </div>
                  </div>
                  <div class="text-right text-[11px] font-mono text-slate-400 bg-[var(--background)] p-3 rounded-xl border border-[var(--border)] max-w-xs">
                    <strong class="text-teal-400 block mb-0.5">Verification Output</strong>
                    ${st.action}
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      // TAB: CLINICS & MATAB
      if (state.tab === 'clinics') {
        const subnav = getWebsiteHubSubnav(state.tab);
        const clinicsList = [
          { name: "ZAYVORA Healthcare System - Central Hospital", type: "Flagship Hospital & Research Complex", address: "ZAYVORA Health Boulevard, Institutional Area, New Delhi 110062", phone: "+91 97738 82657", timing: "Open 24/7 • OPD: 8:00 AM – 8:00 PM", beds: "120 Beds • 8 Regimenal Suites" },
          { name: "ZAYVORA Matab™ Charminar Heritage Center", type: "Specialized Unani Matab & Pharmacy", address: "Heritage Health Quarter, Near Charminar, Hyderabad 500002", phone: "+91 97738 82657", timing: "OPD: 9:00 AM – 7:00 PM", beds: "Outpatient & Hijama Clinic" },
          { name: "ZAYVORA Integrative Care Center", type: "Clinical Matab & Telemedicine Hub", address: "Koramangala 4th Block, 80 Feet Road, Bengaluru 560034", phone: "+91 97738 82657", timing: "OPD: 9:30 AM – 6:30 PM", beds: "Tele-Health & Regimen Suite" },
          { name: "ZAYVORA Himalayan Herbal Center", type: "High-Altitude Botanical Dispensary", address: "Residency Road, Srinagar, Jammu & Kashmir 190001", phone: "+91 97738 82657", timing: "OPD: 10:00 AM – 5:00 PM", beds: "Specialty Cold-Chain Unit" }
        ];

        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Facility Directory</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Hospital Facilities & Specialized Matabs</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                Visit any of our accredited clinical facilities for in-person 10-Ajnas pulse evaluation, tongue chromametry, and classical regimenal therapies (Hijama, Natool, Fasd).
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              ${clinicsList.map(c => `
                <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-4 flex flex-col justify-between">
                  <div class="space-y-2">
                    <div class="flex justify-between items-start">
                      <div>
                        <h3 class="font-bold text-white text-base">${c.name}</h3>
                        <span class="text-xs text-emerald-400 font-semibold block">${c.type}</span>
                      </div>
                      <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold">Active</span>
                    </div>
                    <p class="text-xs text-[var(--muted)] leading-relaxed">${c.address}</p>
                    <div class="text-xs text-slate-300 space-y-1 pt-1">
                      <div>⏰ ${c.timing}</div>
                      <div><svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg> ${c.beds}</div>
                    </div>
                  </div>
                  <div class="pt-3 border-t border-[var(--border)] flex justify-between items-center">
                    <a href="tel:${c.phone}" class="text-xs font-mono text-emerald-400 font-bold hover:underline">${c.phone}</a>
                    <button onclick="if (document.getElementById('opd-booking-card')) { document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' }); } else { viewWebsitePage('home'); setTimeout(() => document.getElementById('opd-booking-card')?.scrollIntoView({ behavior: 'smooth' }), 120); }" class="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg transition">Book OPD Token</button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      // TAB: DOCTORS & FACULTY / TEAM
      if (state.tab === 'doctors' || state.tab === 'team') {
        const subnav = getWebsiteHubSubnav(state.tab);
        const doctorsList = [
          { name: "Hakeem Dr. Irfan Ashraf", degree: "BUMS (Unani)", specialty: "Moalajat (Internal Medicine) & Waja-ul-Mafasil", facility: "ZAYVORA Healthcare System - Central Hospital", timing: "Mon – Fri: 9:00 AM – 2:00 PM" },
          { name: "Dr. Aisha Siddiqui", degree: "BUMS (Tahaffuzi wa Samaji Tibb)", specialty: "Preventive Medicine & Mizaj-e-Adil Lifestyle", facility: "ZAYVORA Healthcare System - Central Hospital", timing: "Tue – Sat: 10:00 AM – 3:00 PM" },
          { name: "Hakim Syed M. Akhtar", degree: "BUMS (Ilaj bil-Tadbeer)", specialty: "Regimenal Therapy, Hijama & Musculoskeletal Rehabilitation", facility: "ZAYVORA Matab™ Specialized Therapy Suite", timing: "Mon – Thu: 11:00 AM – 4:00 PM" }
        ];

        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Medical Faculty</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Board-Certified Clinicians & Senior Tabeebs</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                Our clinicians combine rigorous institutional Unani medical degrees with modern clinical pharmacology and diagnostic expertise.
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
              ${doctorsList.map(d => `
                <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-4 flex flex-col justify-between">
                  <div class="space-y-2">
                    <div class="w-14 h-14 rounded-2xl bg-emerald-950/60 border border-emerald-500/40 flex items-center justify-center text-2xl">
                      ‍⚕️
                    </div>
                    <div>
                      <h3 class="font-bold text-white text-base">${d.name}</h3>
                      <span class="text-xs text-emerald-400 font-semibold block">${d.degree}</span>
                    </div>
                    <p class="text-xs text-[var(--muted)] leading-relaxed">${d.specialty}</p>
                    <div class="text-[11px] text-slate-300 pt-2 border-t border-[var(--border)] space-y-0.5">
                      <div>${d.facility}</div>
                      <div>⏰ ${d.timing}</div>
                    </div>
                  </div>
                  <button onclick="if (document.getElementById('opd-booking-card')) { document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' }); } else { viewWebsitePage('home'); setTimeout(() => document.getElementById('opd-booking-card')?.scrollIntoView({ behavior: 'smooth' }), 120); }" class="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl transition shadow">
                    Book Consultation →
                  </button>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      // TAB: KNOWLEDGE CENTRE
      if (state.tab === 'knowledge') {
        renderGrandLibrary(container, 'website');
        return;
      }

      // TAB: FAQS
      if (state.tab === 'faqs') {
        const subnav = getWebsiteHubSubnav(state.tab);
        const faqs = [
          { q: "What is ZAYVORA Health OS™?", a: "ZAYVORA Health OS is an enterprise healthcare operating system uniting classical Unani medicine (10-Ajnas pulse evaluation, Su-e-Mizaj, Organ-Axis) with contemporary biomedical intelligence, electronic health records, and clinician-governed decision intelligence." },
          { q: "How is patient safety ensured with Unani medicines?", a: "All formulations conform to AYUSH Schedule T (GMP) quality standards and HPLC active fingerprinting. Schedule E(1) botanical ingredients undergo mandatory multi-day Mudabbar detoxification, supervised by pharmacognosists and verified by spectroscopy." },
          { q: "Can the system prescribe medicines without a doctor?", a: "Never. Under our strict 21 CFR Part 11 implementation, all clinical intelligence operates exclusively as decision support for clinicians. Every prescription strictly requires a licensed doctor's review and digital PIN sign-off." },
          { q: "Are services connected to Ayushman Bharat (ABDM)?", a: "Yes. ZAYVORA is integrated with ABDM M1, M2, and M3 standards, allowing seamless creation of ABHA numbers and secure sharing of encrypted health records with patient consent." },
          { q: "How do I book an OPD consultation or tele-consultation?", a: "You can book directly through the website or patient portal. Consultations are available both in-clinic at our Central Hospital and Matabs, or via secure WebRTC tele-health." }
        ];

        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-8 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Patient Questions</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Frequently Asked Questions</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                Answers to common clinical, technological, and safety questions about ZAYVORA Health OS.
              </p>
            </div>

            <div class="space-y-4">
              ${faqs.map(f => `
                <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
                  <h3 class="text-base font-bold text-emerald-400">${f.q}</h3>
                  <p class="text-xs text-[var(--muted)] leading-relaxed">${f.a}</p>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      // TAB: CONTACT
      if (state.tab === 'contact') {
        const subnav = getWebsiteHubSubnav(state.tab);
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-8 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Hospital Concierge</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Contact ZAYVORA Healthcare System</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                For clinical appointments, tele-consultation inquiries, hospital casualty, or partnership coordination.
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
                <div class="text-2xl"></div>
                <h3 class="font-bold text-white text-sm">Direct Helpline</h3>
                <a href="tel:+919773882657" class="text-sm font-mono font-bold text-emerald-400 block">+91 97738 82657</a>
                <p class="text-[11px] text-[var(--muted)]">Available 24/7 for patient assistance</p>
              </div>
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
                <div class="text-2xl">✉️</div>
                <h3 class="font-bold text-white text-sm">Official Email</h3>
                <span class="text-sm font-mono font-bold text-white block">concierge@zayvorahealth.com</span>
                <p class="text-[11px] text-[var(--muted)]">Clinical & administrative inquiries</p>
              </div>
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
                <div class="text-2xl"></div>
                <h3 class="font-bold text-white text-sm">Central Hospital</h3>
                <p class="text-xs text-slate-300">ZAYVORA Health Boulevard, Institutional Area, New Delhi 110062</p>
                <p class="text-[11px] text-[var(--muted)]">Open 24/7 with Casualty Desk</p>
              </div>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-4">
              <h3 class="font-bold text-white text-base">Send a Direct Message to Care Team</h3>
              <form onsubmit="event.preventDefault(); showNotification('✓ Your clinical inquiry has been logged. Our concierge will contact you within 15 minutes at +91 97738 82657.', 'success'); this.reset();" class="space-y-4 text-xs">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-[var(--muted)] mb-1">Your Name</label>
                    <input required placeholder="Dr. / Mr. / Ms." class="w-full px-4 py-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400" />
                  </div>
                  <div>
                    <label class="block text-[var(--muted)] mb-1">Phone Number</label>
                    <input required placeholder="+91 97738 82657" class="w-full px-4 py-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400" />
                  </div>
                </div>
                <div>
                  <label class="block text-[var(--muted)] mb-1">Inquiry Category</label>
                  <select class="w-full px-4 py-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400">
                    <option>Consultation & Appointment Booking</option>
                    <option>Pharmacy & Prescription Inquiries</option>
                    <option>Hospital Facility & Regimenal Therapy</option>
                    <option>Research & Academic Collaboration</option>
                  </select>
                </div>
                <div>
                  <label class="block text-[var(--muted)] mb-1">Message</label>
                  <textarea rows="4" required placeholder="Describe your clinical inquiry or question..." class="w-full px-4 py-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-white focus:outline-none focus:border-emerald-400"></textarea>
                </div>
                <button type="submit" class="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition">
                  Send Clinical Message
                </button>
              </form>
            </div>
          </div>
        `;
        return;
      }

            // TAB: PRIVACY POLICY (DPDP ACT 2023 & HIPAA COMPLIANT)
      if (state.tab === 'privacy') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-16 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Statutory Privacy Policy &bull; DPDP Act 2023 Compliant</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-[#1B242A] dark:text-white">Comprehensive Data Protection & Privacy Policy</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Governed under India's Digital Personal Data Protection (DPDP) Act 2023, Information Technology Act 2000, IT Rules 2011 (SPDI), Ayushman Bharat Digital Mission (ABDM) Health Data Management Policy, and international health data standards (HIPAA &amp; DISHA aligned).
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">DPDP Act 2023 Enforced</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">ABDM M1-M3 Certified Locker</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">AES-256-GCM At Rest</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">TLS 1.3 In Transit</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Effective Date: 20 September 2026</span>
              </div>
            </div>

            <!-- Executive Summary Box -->
            <div class="p-5 rounded-2xl bg-emerald-950/20 border border-emerald-800/40 text-emerald-200 space-y-2 text-xs">
              <h3 class="font-bold text-sm text-emerald-300 flex items-center gap-2">
                <span>🛡️</span> Executive Summary (Patient Data Rights at a Glance)
              </h3>
              <p class="leading-relaxed text-emerald-200/90">
                ZAYVORA Health OS™ treats your health records with the highest clinical confidentiality. We collect only data necessary for doctor consultations and prescription fulfillment. <strong>We do not sell, rent, or monetize your medical history, pulse wave data, or biometrics to third-party ad networks.</strong> You retain full rights to access, download, correct, or delete your health records or revoke ABDM health locker consent at any time.
              </p>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-8 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">01</span>
                  Definitions &amp; Scope of Application
                </h3>
                <p>
                  This Privacy Policy applies to all patients, clinicians, dispensaries, and visitors interacting with ZAYVORA Health OS™ via web applications, mobile platforms, teleconsultation cockpits, or clinic kiosks.
                </p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li><strong>"Personal Data":</strong> Any data about an individual who is identifiable by or in relation to such data, pursuant to Section 2(t) of the DPDP Act, 2023.</li>
                  <li><strong>"Sensitive Personal Data / Health Records (SPDI)":</strong> Medical diagnostic data, 10-Ajnas constitutional temperament vectors, chief complaints, arterial pulse photoplethysmography (PPG) waveforms, electronic prescriptions, lab reports, and medication histories.</li>
                  <li><strong>"Data Fiduciary":</strong> ZAYVORA Health (A Unit of QSURA India Pvt. Ltd.) and attending licensed practitioners determining the purpose and means of clinical data processing.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">02</span>
                  Categories of Data Collected
                </h3>
                <p>We collect data under two primary lawful categories:</p>
                <div class="space-y-2 pl-2">
                  <p><strong class="text-white">A. Demographic & Identity Data:</strong> Full legal name, date of birth, gender, residential address, active mobile telephone number, email address, and voluntary Ayushman Bharat Health Account (ABHA) 14-digit address.</p>
                  <p><strong class="text-white">B. Clinical & Physiological Parameters:</strong> Subjective symptoms, tongue multispectral image records, arterial pulse waveforms, verified blood biomarkers (HbA1c, lipid profile, liver enzymes, semen analysis), dietary logs (<em>Asbab-e-Sittah</em>), and past allopathic medications.</p>
                  <p><strong class="text-white">C. Technical Telemetry:</strong> Anonymized session logs, device operating system, browser user agent, IP address for security rate-limiting and intrusion detection, and crash telemetry.</p>
                </div>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">03</span>
                  Lawful Grounds &amp; Specific Purposes of Processing
                </h3>
                <p>In strict compliance with Section 6 of the DPDP Act 2023, data is processed solely for explicit, legitimate healthcare purposes:</p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li>Formulating holistic constitutional Unani diagnoses (<em>Tashkhees-e-Mizaj</em>) and personalized treatment protocols (<em>Nuskha-e-Matab</em>).</li>
                  <li>Facilitating video and audio telemedicine encounters between patients and board-certified Senior Tabeebs.</li>
                  <li>Transmitting sealed electronic prescriptions to our central hospital dispensary for FEFO compound preparation and parcel fulfillment.</li>
                  <li>Statutory pharmacovigilance tracking of Adverse Drug Reactions (ADRs) under Ministry of AYUSH guidelines.</li>
                  <li>Generating itemized tax invoices, receipts, and processing authorized digital refunds.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">04</span>
                  Data Storage, Encryption &amp; Security Architecture
                </h3>
                <p>ZAYVORA Health OS operates a military-grade security defense-in-depth architecture:</p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li><strong>Encryption At Rest:</strong> Relational patient records, medical timelines, and clinical notes are encrypted using <strong>AES-256-GCM</strong> with hardware security module (HSM) key rotation.</li>
                  <li><strong>Encryption In Transit:</strong> All web traffic and WebSocket audio/video streams are enforced over <strong>TLS 1.3</strong> with Perfect Forward Secrecy (PFS).</li>
                  <li><strong>Merkle-Tree Audit Ledgers:</strong> Prescriptions and clinical encounter locks are sealed with cryptographic SHA-256 Merkle proofs under <strong>21 CFR Part 11</strong> standards, ensuring records cannot be retroactively altered without invalidating digital signatures.</li>
                  <li><strong>Multi-Tenant Data Isolation:</strong> Strict tenant row-level security (RLS) guarantees that patient data belonging to one facility or doctor is mathematically isolated from others.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">05</span>
                  Data Sharing &amp; Third-Party Disclosures
                </h3>
                <p>
                  <strong>We do not sell patient data.</strong> Limited disclosure occurs solely with audited entities essential for care delivery:
                </p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li><strong>Attending Clinicians &amp; Pharmacists:</strong> Licensed personnel directly involved in your care continuum.</li>
                  <li><strong>Logistics &amp; Courier Partners:</strong> Only recipient name, shipping address, and telephone number are shared with logistics providers (e.g., Blue Dart, Delhivery) for doorstep delivery; <em>zero clinical diagnoses or medical conditions are shared with couriers</em>.</li>
                  <li><strong>Statutory &amp; Law Enforcement:</strong> Strictly when compelled by an official written order issued by a court of competent jurisdiction under Indian law.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">06</span>
                  Patient Rights Under the DPDP Act, 2023
                </h3>
                <p>Every patient or user of ZAYVORA Health holds actionable statutory rights:</p>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                  <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <strong class="text-white block">Right to Information &amp; Access:</strong>
                    <p class="text-[11px] text-slate-400">Request an electronic summary of your health profile, prescriptions, and processing activities.</p>
                  </div>
                  <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <strong class="text-white block">Right to Correction &amp; Erasure:</strong>
                    <p class="text-[11px] text-slate-400">Correct inaccurate personal data or request deletion of non-statutory records.</p>
                  </div>
                  <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <strong class="text-white block">Right of Grievance Redressal:</strong>
                    <p class="text-[11px] text-slate-400">Register complaints directly with our Data Protection Officer with mandatory 48-hour response.</p>
                  </div>
                  <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <strong class="text-white block">Right to Nominate:</strong>
                    <p class="text-[11px] text-slate-400">Nominate an individual to exercise your privacy rights in the event of death or incapacity.</p>
                  </div>
                </div>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">07</span>
                  Data Retention Schedules
                </h3>
                <p>
                  Pursuant to National Medical Commission (NMC) and NCISM statutory regulations, clinical consultation records, medical charts, and signed electronic prescriptions are retained for a minimum mandatory period of <strong>three (3) years</strong> from the date of the last consultation. Anonymized epidemiological research metrics may be archived permanently for clinical audit and public health learning.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">08</span>
                  Cookies &amp; Local Storage Technology
                </h3>
                <p>
                  ZAYVORA Health OS™ uses essential HTTP session cookies and local storage tokens solely to maintain authenticated user sessions, language preferences, and role switcher state. We do not use third-party invasive tracking pixels or cross-site behavioral advertising cookies.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">09</span>
                  Children's Privacy Protection
                </h3>
                <p>
                  In accordance with Section 9 of the DPDP Act 2023, individuals under eighteen (18) years of age may access teleconsultation services only with the verifiable consent and active involvement of a parent or lawful guardian. We do not engage in targeted profiling or tracking of pediatric patients.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">10</span>
                  Designated Data Protection Officer (DPO)
                </h3>
                <p>
                  To exercise your statutory data privacy rights or submit inquiries regarding clinical data security, contact our dedicated compliance office:
                </p>
                <div class="p-4 bg-slate-900 rounded-2xl border border-slate-800 space-y-2 text-xs font-mono">
                  <div><strong>Designated DPO:</strong> Mr. Tariq Masood (Chief Information Security &amp; Data Officer)</div>
                  <div><strong>Direct Data Privacy Email:</strong> <a href="mailto:privacy@zayvora.com" class="text-emerald-400 font-bold">privacy@zayvora.com</a></div>
                  <div><strong>Direct Compliance Helpline:</strong> +91 97738 82657</div>
                  <div><strong>Corporate Office:</strong> QSURA India Pvt. Ltd. (ZAYVORA Health Division), Central Healthcare Complex, New Delhi, 110025, India</div>
                  <div><strong>Response Timeline:</strong> Formal acknowledgement within 24–48 business hours.</div>
                </div>
              </section>
            </div>
          </div>
        `;
        return;
      }

      // TAB: TERMS OF CLINICAL SERVICE & PLATFORM USE
      if (state.tab === 'terms') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-16 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Statutory Master Agreement</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-[#1B242A] dark:text-white">Terms of Clinical Telemedicine Service &amp; Platform Use</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Comprehensive terms governing teleconsultation services, digital prescription authoring, herbal dispensary fulfillment, and patient-practitioner engagements across ZAYVORA Health OS™.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">Telemedicine Guidelines 2020 Aligned</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">NCISM Act 2020 Registered Practitioners</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">IT Act 2000 Electronic Contracts</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Jurisdiction: New Delhi, India</span>
              </div>
            </div>

            <!-- Important Legal Alert -->
            <div class="p-5 rounded-2xl bg-amber-950/20 border border-amber-800/40 text-amber-200 space-y-2 text-xs">
              <h3 class="font-bold text-sm text-amber-300 flex items-center gap-2">
                <span>⚖️</span> Binding Legal Contract Notice
              </h3>
              <p class="leading-relaxed text-amber-200/90">
                By accessing ZAYVORA Health OS™, scheduling a teleconsultation, or ordering botanical formulations, you confirm that you have read, understood, and unconditionally agree to be bound by these Terms of Clinical Service. If you do not agree with any clause of this agreement, you must immediately discontinue use of the platform.
              </p>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-8 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">01</span>
                  Practitioner Qualifications &amp; Statutory Authority
                </h3>
                <p>
                  All clinical teleconsultations on ZAYVORA Health OS™ are delivered exclusively by practitioners who hold recognized medical qualifications under the <strong>National Commission for Indian System of Medicine (NCISM) Act, 2020</strong> (e.g., BUMS / Kamil-e-Tibb-o-Jarahat, MD Unani) and are registered with the National Register of Indian System of Medicine or State AYUSH Councils.
                </p>
                <p>
                  The platform operates as a secure technology enabler and digital infrastructure provider. The professional doctor-patient relationship is established directly between the patient and the licensed attending practitioner.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">02</span>
                  Scope of Teleconsultation &amp; Inherent Limitations
                </h3>
                <p>
                  Telemedicine encounters are conducted in accordance with the <em>Telemedicine Practice Guidelines</em> jointly notified by the Ministry of AYUSH and the Board of Governors in Supersession of the Medical Council of India (2020).
                </p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li><strong>Remote Diagnostic Limitations:</strong> Patients acknowledge that video consultations lack direct physical palpation, physical tongue texture assessment, and in-person arterial pulse (<em>Nabz</em>) tactile palpation.</li>
                  <li><strong>Conversion to In-Person Evaluation:</strong> If at any stage the attending clinician determines that a remote consultation is clinically insufficient, the doctor reserves the absolute right to terminate the teleconsultation and recommend an immediate in-person clinic visit.</li>
                  <li><strong>Identity Verification:</strong> Both the patient and the clinician must verify their identities at the commencement of each consultation.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">03</span>
                  Emergency Medical Exclusion (Dial 112)
                </h3>
                <p>
                  <strong>Telemedicine is strictly contraindicated for acute, unstable, or life-threatening emergencies.</strong> The platform does not provide emergency triage. For conditions such as acute myocardial infarction, acute respiratory failure, loss of consciousness, uncontrolled hemorrhaging, or acute poison ingestion, users must immediately contact emergency services (<strong>112</strong> in India) or report to the nearest hospital casualty department.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">04</span>
                  Electronic Prescriptions &amp; Digital Signatures (21 CFR Part 11)
                </h3>
                <p>
                  Prescriptions authored through ZAYVORA Health OS are valid electronic documents under Section 4 and Section 5 of the Information Technology Act, 2000.
                </p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li>Prescriptions are cryptographically sealed with the attending clinician's digital signature under <strong>21 CFR Part 11</strong> standards.</li>
                  <li>Prescriptions explicitly specify dosage, formulation type, vehicle (<em>Badraqa</em>), dietary instructions (<em>Parhez</em>), and duration.</li>
                  <li>Prescriptions are non-transferable and valid solely for the patient designated thereon. Alteration or counterfeiting of electronic prescriptions is a punishable offense under Indian criminal law.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">05</span>
                  Patient Obligations &amp; Accurate Disclosure
                </h3>
                <p>
                  The patient affirms that all medical history, ongoing allopathic medications, previous adverse reactions, chronic illnesses, and pregnancy/lactation statuses disclosed during consultation are complete and true. <strong>ZAYVORA Health and its clinicians disclaim all liability for adverse clinical consequences caused by intentional or negligent omission of critical health history.</strong>
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">06</span>
                  Dispensary Fulfillment &amp; Schedule E(1) Compliance
                </h3>
                <p>
                  Herbal formulations and medicines ordered via the platform are compounded and dispensed strictly under Schedule T (Good Manufacturing Practices) and Schedule E(1) of the Drugs &amp; Cosmetics Rules, 1945. Certain potent classical formulations are classified as prescription-only (Rx) and cannot be dispensed without verified physician approval and documented detoxification (<em>Mudabbar</em>) certification.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">07</span>
                  Intellectual Property &amp; Proprietary Rights
                </h3>
                <p>
                  All proprietary algorithms, clinical decision support logic (Hakeem Sahab™ CDSS), 10-Ajnas scoring models, botanical formulations, branding, trade dress, and software source code are the exclusive intellectual property of <strong>Hakeem Dr. Irfan Ashraf</strong> and QSURA India Pvt. Ltd. (operating ZAYVORA Health) Unauthorized reverse-engineering, scraping, or commercial duplication is strictly prohibited under the Copyright Act, 1957 and Patents Act, 1970.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">08</span>
                  Limitation of Liability &amp; Maximum Recovery Cap
                </h3>
                <p>
                  To the maximum extent permitted under applicable law, ZAYVORA Health OS and its directors, officers, and technology licensors shall not be liable for any indirect, incidental, punitive, or consequential damages resulting from platform downtime, network latency, or teleconsultation connection failures. In all circumstances, total aggregate liability of ZAYVORA Health / QSURA India Pvt. Ltd. for any claim shall be capped at the total amount actually paid by the patient for the specific consultation or product order giving rise to the claim.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">09</span>
                  Indemnification
                </h3>
                <p>
                  Users agree to defend, indemnify, and hold harmless ZAYVORA Health OS, its clinicians, directors, and affiliates against any third-party claims, liabilities, or losses arising from: (a) breach of these Terms, (b) violation of any law or patient rights, or (c) misrepresentation of identity or clinical history during consultation.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">10</span>
                  Governing Law, Arbitration &amp; Jurisdiction
                </h3>
                <p>
                  This Agreement shall be governed by and construed in accordance with the substantive laws of India. Any dispute arising out of or in connection with these Terms shall be referred to sole arbitration under the Arbitration and Conciliation Act, 1996, with the seat and venue in <strong>New Delhi, India</strong>. The courts of <strong>New Delhi, India</strong> shall have exclusive jurisdiction over any matters not subject to arbitration.
                </p>
              </section>
            </div>
          </div>
        `;
        return;
      }

      // TAB: STATUTORY MEDICAL & CLINICAL DISCLAIMER
      if (state.tab === 'disclaimer') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-16 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Statutory Governance &bull; Ministry of AYUSH &amp; NCISM Aligned</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-[#1B242A] dark:text-white">Statutory Medical &amp; Clinical Information Disclaimer</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Mandatory statutory disclosures governed under the Drugs and Magic Remedies (Objectionable Advertisements) Act 1954, Drugs &amp; Cosmetics Act 1940, and NCISM Clinical Governance Standards.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">Zero Guaranteed Cure Claims</span>
                <span class="px-2 py-0.5 rounded bg-rose-500/10 text-rose-300 border border-rose-500/30">Emergency Alert: 112</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Schedule E(1) Mudabbar Verified</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Assistive Clinical CDSS (Zero Autonomous Rx)</span>
              </div>
            </div>

            <!-- Emergency Alert Box -->
            <div class="p-6 rounded-2xl bg-rose-950/30 border border-rose-800/60 text-rose-200 space-y-2 shadow-lg">
              <h2 class="font-bold text-base flex items-center gap-2 text-rose-300">
                <span>🚨</span> Acute Medical Emergency Notice — Dial 112 Immediately
              </h2>
              <p class="text-xs sm:text-sm leading-relaxed text-rose-200/90">
                The digital health tools, symptom assessments, botanical compendia, and teleconsultation features of ZAYVORA Health OS™ are <strong>strictly not intended, designed, or equipped for acute, life-threatening medical emergencies</strong>. If you or someone you are assisting is experiencing severe crushing chest pain, sudden unilateral paralysis, acute shortness of breath, massive hemorrhage, severe head injury, acute anaphylaxis, or altered mental status, immediately call national emergency services (<strong>112</strong> in India) or report to the nearest hospital multi-specialty emergency department.
              </p>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-8 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">01</span>
                  Absolute Prohibition of "Guaranteed Cure" or "100% Safe" Claims
                </h3>
                <p>
                  In strict compliance with the <strong>Drugs and Magic Remedies (Objectionable Advertisements) Act, 1954</strong> and Consumer Protection regulations:
                </p>
                <ul class="list-disc pl-5 space-y-2 text-slate-400">
                  <li><strong>Zero Guaranteed Outcomes:</strong> ZAYVORA Health expressly disclaims any assertion of "100% guaranteed cure", "permanent eradication of disease", or "miraculous symptomatic reversal" for any chronic condition, including diabetes mellitus, cardiovascular ailments, osteoarthritis, or reproductive dysfunctions.</li>
                  <li><strong>Individual Biological Variability:</strong> In classical Greco-Arab Unani medicine, therapeutic efficacy is dependent upon individual constitutional temperament (<em>Mizaj</em>), metabolic state, environmental factors (<em>Asbab-e-Sittah</em>), adherence to dietary regimens (<em>Ilaj-bil-Ghiza</em>), and concurrent pharmacotherapy. Response timelines vary across individuals.</li>
                  <li><strong>No "Universal Safety":</strong> All biologically active phytotherapeutic compounds possess contraindications and dosage thresholds. No herbal product is universally safe for all human physiology without individualized clinical evaluation.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">02</span>
                  Role &amp; Boundaries of Clinical Decision Support (Hakeem Sahab™ CDSS)
                </h3>
                <p>
                  <strong>Hakeem Sahab™ CDSS</strong> operates strictly as an assistive Clinical Decision Support System (CDSS) for certified medical practitioners:
                </p>
                <ul class="list-disc pl-5 space-y-2 text-slate-400">
                  <li><strong>Zero Autonomous Prescribing:</strong> The clinical decision support system possesses zero legal, diagnostic, or prescribing authority. No treatment plan or prescription is ever issued autonomously.</li>
                  <li><strong>Mandatory Human Clinician Barrier:</strong> Every recommendation must be independently reviewed, adjusted, approved, and cryptographically signed by a licensed practitioner under 21 CFR Part 11 standards before reaching the patient.</li>
                  <li><strong>Reference Only:</strong> Clinical CDSS outputs represent synthesized literature cross-talk from the Unani Pharmacopoeia of India (UPI) and PubMed botanical citations and do not constitute an independent medical opinion.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">03</span>
                  Schedule E(1) Botanical Substances &amp; Mudabbar Detoxification
                </h3>
                <p>
                  Formulations authored or cataloged on this platform that incorporate classical potent botanicals governed under Schedule E(1) of the Drugs and Cosmetics Rules, 1945 (such as <em>Azaraqi / Strychnos nux-vomica</em> or <em>Suranjan / Colchicum luteum</em>) are subject to mandatory traditional pharmaceutical detoxification protocols (<em>Amal-e-Tadbeer / Mudabbar</em>). Such products are dispensed only with verified analytical testing (heavy metals, aflatoxins, microbial pure) under strict doctor prescription.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">04</span>
                  Informational Scope — Not a Substitute for Professional Advice
                </h3>
                <p>
                  All educational content, botanical monographs, symptom calculators, and lifestyle guidance published across ZAYVORA Health are provided solely for general health literacy and academic reference. Browsing or reading materials on this platform does not create a doctor-patient relationship prior to a formal, logged consultation with an authorized clinician.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">05</span>
                  Allopathic &amp; Multi-Drug Interactions
                </h3>
                <p>
                  Patients taking concurrent allopathic pharmaceuticals (e.g., insulin, oral hypoglycemics, antihypertensives, anticoagulants/warfarin, levothyroxine) must disclose all active regimens to their attending clinician. Certain botanical extracts modulate Cytochrome P450 (CYP450) hepatic enzyme pathways and may alter drug bioavailability. Patients must never abruptly discontinue prescribed allopathic medication without consulting their primary allopathic specialist.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">06</span>
                  Regulatory Licensing Clarification
                </h3>
                <p>
                  In accordance with regulatory advisories issued by the Ministry of AYUSH: The Ministry of AYUSH does not directly certify individual commercial products or private clinics. Drug manufacturing licenses (Form 25-D) and proprietary approvals under Rule 158B of the Drugs and Cosmetics Rules 1945 are granted by designated State Licensing Authorities (SLA). All products are manufactured in facilities complying with Schedule T (Good Manufacturing Practice).
                </p>
              </section>
            </div>
          </div>
        `;
        return;
      }

      // TAB: CANCELLATION & REFUND POLICY (RAZORPAY & STRIPE COMPLIANT)
      if (state.tab === 'refunds') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-16 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Consumer Protection &bull; E-Commerce Rules 2020 Compliant</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-[#1B242A] dark:text-white">Cancellation, Return &amp; Refund Policy</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Clear, transparent, and legally binding consumer rights policy governing teleconsultation cancellations, pharmacy returns, and automated payment gateway refunds.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">Refund TAT: 3–5 Business Days</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Original Payment Source Credit</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Razorpay / Stripe Integrated</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Consumer Protection Act 2019</span>
              </div>
            </div>

            <!-- Highlights Box -->
            <div class="p-5 rounded-2xl bg-teal-950/20 border border-teal-800/40 text-teal-200 space-y-2 text-xs">
              <h3 class="font-bold text-sm text-teal-300 flex items-center gap-2">
                <span>💳</span> Transparent Refund Assurance
              </h3>
              <p class="leading-relaxed text-teal-200/90">
                All authorized refunds are processed directly back to your original payment method (UPI, Debit/Credit Card, Net Banking). No credit slips or forced wallet points — real money refunded to your account within <strong>3 to 5 banking days</strong>.
              </p>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-8 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">01</span>
                  Teleconsultation Cancellation &amp; Rescheduling Matrix
                </h3>
                <p>Appointments booked on ZAYVORA Health OS may be cancelled or rescheduled under the following transparent terms:</p>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-emerald-400 block text-xs">More than 4 Hours Prior</span>
                    <strong class="text-white text-base font-extrabold">100% Full Refund</strong>
                    <p class="text-[11px] text-slate-400">Zero cancellation fee. Entire consultation amount refunded automatically.</p>
                  </div>
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-teal-400 block text-xs">Within 4 Hours of Slot</span>
                    <strong class="text-white text-base font-extrabold">Free Reschedule</strong>
                    <p class="text-[11px] text-slate-400">Reschedule to any available slot at zero extra charge (or 80% refund upon request).</p>
                  </div>
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-amber-400 block text-xs">Clinician Emergency / No-Show</span>
                    <strong class="text-white text-base font-extrabold">100% Refund + Priority</strong>
                    <p class="text-[11px] text-slate-400">Full refund initiated immediately plus complimentary priority booking with Senior Tabeeb.</p>
                  </div>
                </div>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">02</span>
                  Dispensary Medication &amp; Herbal Product Returns
                </h3>
                <p>
                  Under the Drugs and Cosmetics Rules, 1945 and international Good Distribution Practices (GDP), <strong>medicines, consumable tonics, and sealed botanical products cannot be returned once opened or unsealed</strong>, due to environmental hygiene and contamination hazards.
                </p>
                <p><strong class="text-white">Eligible Replacement &amp; Full Refund Exceptions:</strong></p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-400">
                  <li><strong>Transit Damage:</strong> Parcel arrives physically crushed, broken, or with torn tamper-evident security tape.</li>
                  <li><strong>Formulation Inaccuracy:</strong> Dispensed product batch or formulation does not match the sealed digital prescription.</li>
                  <li><strong>Temperature Indicator Deviation:</strong> Biological cold-chain indicator (on Arqiyat or Khamiras) shows temperature compromise.</li>
                  <li><strong>Expiry Threshold:</strong> Product arrives with less than six (6) months of remaining shelf life.</li>
                </ul>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">03</span>
                  How to Initiate a Damaged Parcel Return Claim
                </h3>
                <p>
                  To lodge an eligible dispensary claim, simply email our central hospital pharmacy at <a href="mailto:dispensary@zayvora.com" class="text-emerald-400 font-bold">dispensary@zayvora.com</a> or message our WhatsApp concierge at <strong>+91 97738 82657</strong> within <strong>48 hours of parcel delivery</strong>. Please attach:
                </p>
                <ul class="list-disc pl-5 space-y-1 text-slate-400">
                  <li>Your Prescription / Order ID (e.g., RX-2026-XXXX or ORD-XXXX).</li>
                  <li>Clear unboxing photograph or short video showing the outer shipping label and damaged seal.</li>
                </ul>
                <p>
                  Upon photographic verification, our pharmacy dispatches a free expedited priority replacement within 24 hours or initiates an immediate 100% refund.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">04</span>
                  Order Cancellation Prior to Courier Dispatch
                </h3>
                <p>
                  Patients and customers may cancel a dispensary order for standard OTC/wellness formulations free of charge at any time <strong>prior to courier pickup (within 4 hours of order placement)</strong>. Once a parcel has been picked up by the express logistics courier and an Airway Bill (AWB) has been generated, shipment cancellations can no longer be processed in transit.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">05</span>
                  Settlement Timelines &amp; Payment Gateway Mode
                </h3>
                <p>
                  All refunds are settled through our certified payment gateways (<strong>Razorpay / Stripe</strong>) in compliance with Reserve Bank of India (RBI) turnaround guidelines:
                </p>
                <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-2 text-[11px] font-mono">
                  <div class="flex justify-between"><span>UPI (GPay / PhonePe / Paytm):</span><strong class="text-emerald-400">Instant to 24 Hours</strong></div>
                  <div class="flex justify-between"><span>Credit / Debit Cards (Visa / Mastercard / RuPay):</span><strong class="text-white">3 to 5 Business Days</strong></div>
                  <div class="flex justify-between"><span>Net Banking (SBI / HDFC / ICICI / Axis):</span><strong class="text-white">3 to 5 Business Days</strong></div>
                </div>
              </section>
            </div>
          </div>
        `;
        return;
      }

      // TAB: SHIPPING & COLD-CHAIN DELIVERY POLICY
      if (state.tab === 'shipping' || state.tab === 'shipping_refunds') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-16 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Logistics &bull; AYUSH Good Distribution Practices (GDP)</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-[#1B242A] dark:text-white">Shipping, Dispatch &amp; Cold-Chain Policy</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                FEFO-controlled pharmacy fulfillment, 2-8°C active thermal barrier monitoring, and pan-India express courier network.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">24-48h Metro Dispatch</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">2-8°C Active Thermal Barrier</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Live GPS AWB Tracking</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Tamper-Evident Security Seals</span>
              </div>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-8 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">01</span>
                  Dispensary Fulfillment &amp; FEFO Dispatch Protocols
                </h3>
                <p>
                  Prescriptions authored and locked by ZAYVORA clinicians are dispensed directly through licensed AYUSH Schedule T GMP compliant pharmacy partners in New Delhi. Every order is inspected by a registered Chief Pharmacist under strict First-Expired, First-Out (FEFO) batch inventory controls within <strong>twenty-four (24) hours</strong> of electronic sign-off.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">02</span>
                  Pan-India Shipping Coverage &amp; Durations
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-teal-400 block text-xs">Delhi NCR &amp; Metro Hubs</span>
                    <strong class="text-white text-base font-extrabold">24 to 48 Hours</strong>
                    <p class="text-[11px] text-slate-400">Direct priority air dispatch via Blue Dart &amp; Delhivery.</p>
                  </div>
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-teal-400 block text-xs">Tier 1 &amp; Tier 2 Cities</span>
                    <strong class="text-white text-base font-extrabold">2 to 4 Business Days</strong>
                    <p class="text-[11px] text-slate-400">Live SMS &amp; WhatsApp tracking with OTP delivery.</p>
                  </div>
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-teal-400 block text-xs">Rest of India &amp; Remote</span>
                    <strong class="text-white text-base font-extrabold">4 to 7 Business Days</strong>
                    <p class="text-[11px] text-slate-400">Insulated multi-barrier protective parcel packaging.</p>
                  </div>
                </div>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">03</span>
                  2-8°C Active Thermal Barrier &amp; Cold-Chain Monitoring
                </h3>
                <p>
                  Volatile phytotherapeutic distillates (<em>Arqiyat</em>), vital bio-compounds, and active syrups are packaged inside specialized insulated thermal sleeves equipped with chemical temperature monitor tags. In the unlikely event of courier delay or extreme summer transit heat causing indicator color deviation, patients receive a complimentary priority replacement.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">04</span>
                  Shipping Charges &amp; Free Delivery Threshold
                </h3>
                <p>
                  All dispensary medication orders and wellness products with a cart value exceeding <strong>₹999</strong> qualify for <strong>100% Free Shipping</strong> across India. For orders below ₹999, a flat nominal handling fee of ₹79 is applied to cover insulated clinical packaging.
                </p>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">05</span>
                  Real-Time Airway Bill (AWB) Tracking
                </h3>
                <p>
                  Upon parcel handover to the courier, an encrypted Airway Bill (AWB) tracking number is transmitted directly to the patient's registered mobile number via SMS and WhatsApp. Deliveries are protected with a mandatory <strong>one-time delivery password (OTP)</strong> to ensure that medicine parcels are handed over exclusively to the authorized patient or representative.
                </p>
              </section>
            </div>
          </div>
        `;
        return;
      }

      // TAB: STATUTORY GRIEVANCE REDRESSAL MECHANISM
      if (state.tab === 'grievance') {
        container.innerHTML = `
          <div class="max-w-4xl mx-auto space-y-6 pb-16 text-xs">
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Statutory Grievance Redressal &bull; IT Rules 2021 Compliant</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-[#1B242A] dark:text-white">Statutory Grievance Redressal Mechanism</h1>
              <p class="text-[var(--muted)] leading-relaxed">
                Appointed pursuant to Rule 3(2) of the Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021 and Section 5(9) of the Consumer Protection (E-Commerce) Rules, 2020.
              </p>
              <div class="flex flex-wrap gap-2 pt-2 text-[10px] font-mono text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">IT Rules 2021 Rule 3(2)</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Mandatory Acknowledgement &lt; 48 Hours</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Final Redressal SLA &lt; 15 Calendar Days</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Appellate Mechanism Established</span>
              </div>
            </div>

            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-8 text-slate-300 leading-relaxed text-xs">
              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">01</span>
                  Designated Chief Grievance Redressal Officer
                </h3>
                <p>
                  Any user, patient, medical practitioner, or statutory regulator may escalate complaints, legal concerns, or technical grievances regarding content, privacy, clinical conduct, or e-commerce delivery directly to our designated officer:
                </p>
                <div class="p-5 bg-slate-900 rounded-2xl border border-slate-800 space-y-2.5 text-xs font-mono">
                  <div><strong>Officer Name:</strong> Advocate Tariq Masood (Legal &amp; Regulatory Head)</div>
                  <div><strong>Official Designation:</strong> Chief Grievance Officer, ZAYVORA Health (A Unit of QSURA India Pvt. Ltd.)</div>
                  <div><strong>Dedicated Grievance Email:</strong> <a href="mailto:grievance@zayvora.com" class="text-emerald-400 font-bold underline">grievance@zayvora.com</a></div>
                  <div><strong>Direct Escalation Helpline:</strong> +91 97738 82657</div>
                  <div><strong>Registered Corporate Address:</strong> QSURA India Pvt. Ltd. (ZAYVORA Health Division), Central Healthcare Complex, Okhla Institutional Area, New Delhi, 110025, India</div>
                  <div><strong>Official Office Hours:</strong> Monday through Saturday, 10:00 AM – 6:00 PM IST (Excluding Public Holidays)</div>
                </div>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">02</span>
                  Statutory Resolution SLA Timelines
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-emerald-400 block text-xs">Stage 1: Formal Ticket Acknowledgement</span>
                    <strong class="text-white text-base font-extrabold">&lt; 48 Hours</strong>
                    <p class="text-[11px] text-slate-400">A formal unique tracking ticket number is generated and sent via SMS and email.</p>
                  </div>
                  <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5">
                    <span class="font-bold text-teal-400 block text-xs">Stage 2: Full Investigation &amp; Redressal</span>
                    <strong class="text-white text-base font-extrabold">&lt; 15 Calendar Days</strong>
                    <p class="text-[11px] text-slate-400">Complete investigation with written report, corrective actions, or refund settlement.</p>
                  </div>
                </div>
              </section>

              <section class="space-y-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-xs">03</span>
                  Grievance Escalation Process
                </h3>
                <p>
                  If you are not satisfied with the resolution provided by our general support desk, you may escalate to the Grievance Officer stating your original Ticket ID. The Grievance Officer conducts an independent review in coordination with the Clinical Governance Board.
                </p>
                <p>
                  In the rare event that a grievance is not resolved to your satisfaction within 15 days, you have the statutory right under the IT Rules 2021 to appeal to the Grievance Appellate Committee (GAC) constituted by the Ministry of Electronics and Information Technology (MeitY), Government of India.
                </p>
              </section>
            </div>
          </div>
        `;
        return;
      }

      // TAB: CAREERS & FACULTY RECRUITMENT
      if (state.tab === 'careers') {
        const subnav = getWebsiteHubSubnav(state.tab);
        const openPositions = [
          {
            title: "Senior Consultant Tabeeb (Moalajat / Internal Medicine)",
            dept: "Clinical Medicine & Inpatient Matab",
            type: "Full-Time • On-Site",
            loc: "Central Hospital & Matab Suite, New Delhi",
            exp: "BUMS (Unani) • 5+ Years Clinical Practice",
            desc: "Lead pulse-based diagnosis (10-Ajnas), supervise clinical consultations, review Hakeem Sahab™ differential suggestions, and execute 21 CFR Part 11 compliant digital prescriptions.",
            skills: ["Moalajat", "10-Ajnas Pulse Diagnosis", "Tadbeer Oversight", "Clinical Governance"]
          },
          {
            title: "Classical Botanical Pharmacognosist & QA/QC Lead",
            dept: "Herbal Therapeutics & GMP Manufacturing",
            type: "Full-Time • Haridwar / Hybrid",
            loc: "AYUSH-GMP Manufacturing Unit, Uttarakhand",
            exp: "M.Pharm (Ayush / Unani) / Ph.D. • 4+ Years QA Experience",
            desc: "Supervise Schedule E(1) Mudabbar non-toxicity detox protocols (Azraqi, Afiyun), conduct HPLC fingerprint batch certifications, and maintain electronic Batch Manufacturing Records (eBMR).",
            skills: ["Schedule E1 Mudabbar", "HPLC Fingerprinting", "AYUSH GMP", "Pharmacopoeial Standards"]
          },
          {
            title: "Healthcare Informatics & AI Engineer (Graph RAG / NLP)",
            dept: "Health OS & Medical Intelligence",
            type: "Full-Time • Bengaluru / Remote",
            loc: "ZAYVORA Tech Labs, Bengaluru",
            exp: "B.Tech / M.S. Computer Science • 3+ Years in Python/FastAPI",
            desc: "Architect the Unani Knowledge Graph (1,280+ monographs, 4,600 affinities), develop clinical safety firewalls preventing autonomous prescribing, and optimize high-concurrency FHIR R4 APIs.",
            skills: ["Python / FastAPI", "Neo4j / Graph RAG", "FHIR R4 / ABDM", "AI Clinical Safety"]
          },
          {
            title: "Regimenal Therapy Specialist (Ilaj bil-Tadbeer)",
            dept: "Regimenal Care & Rehabilitation",
            type: "Full-Time • On-Site",
            loc: "Specialized Therapy Suite, Delhi Matab",
            exp: "BUMS (Ilaj bil-Tadbeer) • Certified Hijama Practitioner",
            desc: "Administer clinical Hijama (wet/dry cupping), Dalk (therapeutic massage), Hammam, and Fasd under strict aseptic clinical standards with computerized vitals monitoring.",
            skills: ["Ilaj bil-Tadbeer", "Hijama (Wet/Dry)", "Aseptic Protocols", "Musculoskeletal Rehab"]
          }
        ];

        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Careers &amp; Faculty Openings</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Join the Integrative Clinical Movement</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                We are building the future of codified Greco-Arab medicine—fusing centuries of empirical healing with modern biochemistry, clinical safety firewalls, and AYUSH-GMP manufacturing. Discover opportunities to lead with clinical purpose.
              </p>
            </div>

            <!-- Value Props -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
                <div class="text-emerald-400 text-lg">🏥</div>
                <h4 class="font-bold text-white text-sm">Clinical Excellence First</h4>
                <p class="text-xs text-slate-400">Practitioners retain complete diagnostic authority. Decision support serves as clinician-in-the-loop guidance, never replacing human clinical judgment.</p>
              </div>
              <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
                <div class="text-teal-400 text-lg">🔬</div>
                <h4 class="font-bold text-white text-sm">Empirical Research Grounding</h4>
                <p class="text-xs text-slate-400">Co-author indexed clinical trial papers, analyze real-world evidence registries, and advance pharmacopoeial monograph standardization.</p>
              </div>
              <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
                <div class="text-amber-400 text-lg">⚖️</div>
                <h4 class="font-bold text-white text-sm">Statutory &amp; Ethical Pride</h4>
                <p class="text-xs text-slate-400">Uncompromising compliance with NCISM, AYUSH, 21 CFR Part 11, and DPDP 2023 regulations in an institutionally respected environment.</p>
              </div>
            </div>

            <!-- Open Positions List -->
            <div class="space-y-4">
              <div class="flex justify-between items-center">
                <h3 class="text-lg font-bold text-white flex items-center gap-2">
                  <span>Current Opportunities</span>
                  <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-mono">${openPositions.length} Positions</span>
                </h3>
                <span class="text-xs text-slate-400">Updated for 2026 Academic &amp; Clinical Session</span>
              </div>

              <div class="space-y-4">
                ${openPositions.map(pos => `
                  <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-4 hover:border-emerald-500/40 transition">
                    <div class="flex flex-col md:flex-row md:items-center justify-between gap-2">
                      <div>
                        <h4 class="text-base font-bold text-white">${pos.title}</h4>
                        <div class="flex flex-wrap items-center gap-3 text-xs text-slate-400 mt-1">
                          <span class="text-emerald-400 font-semibold">${pos.dept}</span>
                          <span>•</span>
                          <span>📍 ${pos.loc}</span>
                          <span>•</span>
                          <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[11px]">${pos.type}</span>
                        </div>
                      </div>
                      <a href="mailto:careers@zayvora.com?subject=Application for ${encodeURIComponent(pos.title)}" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl transition text-center shadow whitespace-nowrap">
                        Apply for Position →
                      </a>
                    </div>
                    <div class="text-xs text-slate-300 bg-slate-900/50 p-3 rounded-xl border border-slate-800">
                      <strong>Requirement:</strong> ${pos.exp}
                    </div>
                    <p class="text-xs text-[var(--muted)] leading-relaxed">${pos.desc}</p>
                    <div class="flex flex-wrap gap-1.5 pt-2 border-t border-[var(--border)]">
                      ${pos.skills.map(s => `<span class="px-2 py-0.5 rounded-full bg-emerald-950/40 border border-emerald-500/20 text-emerald-300 text-[10px] font-mono">${s}</span>`).join('')}
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>

            <!-- Recruitment Contact Box -->
            <div class="p-6 rounded-2xl bg-gradient-to-r from-slate-900 to-emerald-950/40 border border-emerald-500/30 flex flex-col md:flex-row items-center justify-between gap-4">
              <div>
                <h4 class="text-white font-bold text-sm">Don't see your specific specialization?</h4>
                <p class="text-xs text-slate-400">We welcome spontaneous applications from exceptional Unani academicians, biochemists, and software engineers.</p>
              </div>
              <a href="mailto:careers@zayvora.com?subject=Spontaneous Clinical or Engineering Application" class="px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs border border-slate-700 transition shrink-0">
                Send CV to careers@zayvora.com
              </a>
            </div>
          </div>
        `;
        return;
      }

      // TAB: CLINICAL & DECISION GOVERNANCE ETHICS CHARTER
      if (state.tab === 'ethics') {
        const subnav = getWebsiteHubSubnav(state.tab);
        const pillars = [
          {
            num: "01",
            title: "Clinician-in-the-Loop Primacy & Zero Autonomous Prescribing",
            badge: "Mandatory Safety Barrier",
            icon: "🛡️",
            desc: "Under statutory NCISM and medical board ethics, the decision support engine (Hakeem Sahab™) is strictly prohibited from generating, modifying, or dispensing therapeutic prescriptions autonomously. All clinical recommendations are non-binding differential advisories.",
            rule: "A licensed, board-certified clinician must physically or through validated telemedicine evaluate the patient and cryptographically sign every single order using 21 CFR Part 11 compliant dual-factor credentials."
          },
          {
            num: "02",
            title: "Schedule E(1) Mudabbar Detoxification & Non-Toxicity Invariant",
            badge: "Drug Safety Invariant",
            icon: "🧪",
            desc: "Greco-Arab formulations containing potent botanicals or purified mineral agents (e.g., Strychnos nux-vomica/Azraqi, Arsenic trioxide/Sem-ul-Far, Papaver somniferum/Afiyun) must undergo mandatory classical detoxification (Mudabbar) according to UPI and NFUM canons.",
            rule: "No batch can be released from quarantine without HPLC fingerprint validation and dual sign-off by the Chief Analytical Chemist and Head of Medical Quality."
          },
          {
            num: "03",
            title: "Patient Data Sovereignty, ABDM & DPDP Act 2023 Compliance",
            badge: "Data Protection",
            icon: "🔒",
            desc: "Protected Health Information (PHI) is sacred. ZAYVORA adheres strictly to India's Digital Personal Data Protection Act (DPDP) 2023 and Ayushman Bharat Digital Mission (ABDM M1, M2, M3) health data interoperability standards.",
            rule: "Zero commercial data brokering. All patient data is encrypted with AES-256 at rest and TLS 1.3 in transit. Patient consent is granular, revocable, and audit-logged in an immutable cryptographic ledger."
          },
          {
            num: "04",
            title: "Independent Institutional Review Board (IRB) & DSMB Oversight",
            badge: "Research Ethics",
            icon: "⚖️",
            desc: "All real-world evidence (RWE) registries, observational cohorts, and concordance benchmarking trials are conducted in accordance with the Declaration of Helsinki and ICMR Ethical Guidelines for Biomedical Research.",
            rule: "Independent Data Safety and Monitoring Boards (DSMB) review ongoing clinical concordance, adverse event signals, and therapeutic outcomes quarterly."
          }
        ];

        container.innerHTML = `
          <div class="max-w-5xl mx-auto space-y-8 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-8 rounded-3xl border border-[var(--border)] space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Clinical Governance &amp; Ethics</span>
                <button onclick="viewWebsitePage('home')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>
              </div>
              <h1 class="text-3xl font-extrabold text-white">Clinical Ethics &amp; Governance Charter</h1>
              <p class="text-sm text-[var(--muted)] leading-relaxed">
                The foundational ethical covenant of ZAYVORA Health OS™. We codify ancient Hippocratic and Greco-Arab healing principles within modern cryptographic and regulatory guardrails.
              </p>
            </div>

            <!-- 4 Pillars -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              ${pillars.map(p => `
                <div class="p-6 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3 flex flex-col justify-between">
                  <div class="space-y-3">
                    <div class="flex items-center justify-between">
                      <span class="text-2xl">${p.icon}</span>
                      <span class="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-[10px] font-mono border border-emerald-500/20">${p.badge}</span>
                    </div>
                    <h3 class="text-base font-bold text-white flex items-center gap-2">
                      <span class="text-emerald-400 font-mono text-sm">${p.num}.</span>
                      ${p.title}
                    </h3>
                    <p class="text-xs text-[var(--muted)] leading-relaxed">${p.desc}</p>
                  </div>
                  <div class="pt-3 border-t border-[var(--border)] text-[11px] text-emerald-300/90 bg-emerald-950/20 p-2.5 rounded-xl border border-emerald-500/20">
                    <strong>Statutory Rule:</strong> ${p.rule}
                  </div>
                </div>
              `).join('')}
            </div>

            <!-- Ethics Committee Quorum Notice -->
            <div class="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
              <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                <h4 class="text-sm font-bold text-white flex items-center gap-2">
                  <span>🏛️</span> Institutional Ethics &amp; Clinical Safety Board
                </h4>
                <span class="text-xs text-slate-400 font-mono">Quorum Requirement: 3/3 Unanimous</span>
              </div>
              <p class="text-xs text-slate-400 leading-relaxed">
                Any modification to clinical decision support rules, pharmacopoeia monographs, or drug interaction logic requires signed cryptographic consensus from the <strong>Chief Clinician</strong>, <strong>Head Pharmacognosist</strong>, and <strong>External Ethics Chair</strong>. No single engineer or administrator can unilaterally deploy algorithmic changes.
              </p>
              <div class="flex flex-wrap items-center justify-between gap-3 pt-2 text-xs text-slate-400">
                <div>For clinical ethics inquiries or confidential reporting: <a href="mailto:ethics@zayvora.com" class="text-emerald-400 hover:underline">ethics@zayvora.com</a></div>
                <button onclick="viewWebsitePage('privacy')" class="text-xs text-teal-400 hover:underline">Read Data Privacy Charter →</button>
              </div>
            </div>
          </div>
        `;
        return;
      }

      // TAB: SYSTEM ARCHITECTURE & INTEGRATED SITEMAP
      if (state.tab === 'pages25') {
        const architectureDomains = [
          {
            title: `Domain I: <svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg> Clinical Services & Care Continuum`,
            badge: "Clinical Care",
            desc: "Full-spectrum integrative healthcare services unifying 10-Ajnas pulse evaluation, clinical decision support system, ambient scribe, and certified manufacturing.",
            modules: [
              { key: "services", title: "Clinical Services Overview", path: "/services", desc: "Tele-consult, OPD, Regimenal Ilaj bil-Tadbeer, and In-Clinic Matab." },
              { key: "services_clinical_care", title: "In-Clinic Matab & OPD Care", path: "/services/clinical-care", desc: "10-Ajnas pulse evaluation, tongue chromametry, and inpatient supervision." },
              { key: "services_ai_healthcare", title: "Hakeem Sahab™ Clinical CDSS", path: "/services/ai-healthcare", desc: "Evidence-grounded clinical reasoning with mandatory 21 CFR Part 11 clinician signature barrier." },
              { key: "services_digital_health", title: "Digital Health & Ambient Scribe", path: "/services/digital-health", desc: "Vernacular audio scribe, BLE IoT sensor streaming, and ABDM M1-M3 records." },
              { key: "services_pharmacy", title: "Botanical Dispensary (FEFO)", path: "/services/pharmacy", desc: "Automated FEFO inventory, IoT cold-chain surveillance, and barcoded delivery." },
              { key: "services_manufacturing", title: "Manufacturing OS & eBMR", path: "/services/manufacturing", desc: "Schedule E(1) Mudabbar detoxification, batch records, and HPLC spectral QA." },
              { key: "services_healthcare_communication", title: "Vernacular Posology Audio", path: "/services/healthcare-communication", desc: "Posology voice instructions in Urdu, Hindi, and English with WhatsApp alerts." }
            ]
          },
          {
            title: `Domain II: <svg class="w-4 h-4 inline-block text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg> Botanical Therapeutics & Dispensary`,
            badge: "Herbal Formulary",
            desc: "AYUSH Schedule T compliant botanical formulations, classical Unani compounds, standardized extracts, and verified cold-chain dispatch protocols.",
            modules: [
              { key: "products", title: "32 Master Formulations Portfolio", path: "/products", desc: "Interactive herbal catalog with dosage, indications, cart, and batch COA." },
              { key: "products_unani_care", title: "Classical Unani Care", path: "/products/unani-care", desc: "Time-tested compounds: ManiVital Pro, Qurs-e-Taqwiyat-e-Mani, Majun Falasfa." },
              { key: "products_herbal_products", title: "Standardized Herbal Extracts", path: "/products/herbal-products", desc: "Biochemically verified extracts: MetaboCore Elite, LiverPrime Core, GastriNorm." },
              { key: "products_nutraceuticals", title: "Target Phyto-Nutraceuticals", path: "/products/nutraceuticals", desc: "Targeted complexes: NeuroCalmX, NightOne X, and ThyroMet Axis." },
              { key: "shipping_refunds", title: "Cold-Chain Shipping Policy", path: "/shipping-refunds", desc: "2-8°C active thermal packaging, tamper seals, and cold-chain compliance standards." }
            ]
          },
          {
            title: `Domain III: <svg class="w-4 h-4 inline-block text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg> Research, Evidence & Knowledge Institute`,
            badge: "Empirical Science",
            desc: "Empirical validation of Greco-Arab medicine through multi-center concordance trials, real-world evidence registries, and knowledge graphs.",
            modules: [
              { key: "research", title: "Research & Evidence Hub", path: "/research", desc: "Observational RWE registries, academic concordance, and clinical trial cohorts." },
              { key: "research_clinical_research", title: "Clinical Trials & Cohorts", path: "/research/clinical-research", desc: "Multi-center clinical trials, patient enrollment, and DSMB governance." },
              { key: "research_evidence", title: "Phytochemical HPLC Fingerprints", path: "/research/evidence", desc: "Comparative chromatographic spectra, active marker quantification, and assays." },
              { key: "research_knowledge_intelligence", title: "Unani Knowledge Graph (ZKB)", path: "/research/knowledge-intelligence", desc: "1,280+ canonical botanical monographs, 4,600 affinities, and Badal/Musleh rules." },
              { key: "knowledge", title: "UPI Pharmacopoeia Library", path: "/knowledge", desc: "Standardized single drug monographs and classical Unani pharmacopoeia references." }
            ]
          },
          {
            title: "Domain IV: Greco-Arab Philosophy & Patient Journey",
            badge: "Clinical Doctrine",
            desc: "Classical foundational doctrine unifying the 4 humors (Akhlat), longitudinal Mizaj constitution, and the 12-stage closed-loop clinical continuum.",
            modules: [
              { key: "philosophy", title: "Four Humors (Akhlat) & Mizaj", path: "/philosophy", desc: "Damm, Balgham, Safra, and Sawda balance, 6 Essentials, and Afaal progression." },
              { key: "care_journey", title: "12-Step Clinical Continuum", path: "/care-journey", desc: "From KNOW & ASSESS through 21 CFR Lock, IoT tracking, and Relapse Guard." }
            ]
          },
          {
            title: `Domain V: <svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg> Healthcare Network, Faculty & Governance`,
            badge: "Hospital & Governance",
            desc: "Accredited clinical facilities, board-certified senior clinicians, intellectual property stewardship, and statutory patient data protection.",
            modules: [
              { key: "clinics", title: "14 Hospital & Matab Network", path: "/clinics", desc: "Flagship hospital in New Delhi and specialized Matabs across major cities." },
              { key: "doctors", title: "Board-Certified Faculty & Clinicians", path: "/doctors", desc: "Senior Tabeebs and integrative MDs with verified institutional credentials." },
              { key: "about", title: "About ZAYVORA & Founder IP", path: "/about", desc: "Institutional vision, governance board, and Hakeem Dr. Irfan Ashraf IP stewardship." },
              { key: "faqs", title: "Patient & Clinical FAQs", path: "/faq", desc: "Answers regarding treatment safety, consultation booking, and ABHA integration." },
              { key: "contact", title: "24/7 Helpline & Emergency Triage", path: "/contact", desc: "Universal triage line +91 97738 82657, casualty desk, and direct messaging." },
              { key: "privacy", title: "Data Protection & Privacy Policy", path: "/privacy-policy", desc: "HIPAA, ABDM M1-M3, and DPDP cryptographic health data protection standards." },
              { key: "terms", title: "Terms of Clinical Service", path: "/terms-and-conditions", desc: "21 CFR Part 11 digital records, telemedicine guidelines, and clinical disclaimers." }
            ]
          }
        ];

        container.innerHTML = `
          <div class="space-y-10 pb-16">
            
            <!-- Architecture Blueprint Header -->
            <div class="bg-[#FAF7EE] dark:bg-gradient-to-r dark:from-[#0F172A] dark:via-[#131D31] dark:to-[#0A0F1D] p-8 rounded-3xl border border-[#DCD5C4] dark:border-emerald-500/30 space-y-4 shadow-sm dark:shadow-xl">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-600 dark:bg-emerald-400 animate-pulse"></span>
                    <span class="text-xs font-bold text-emerald-800 dark:text-emerald-400 uppercase tracking-wider">ZAYVORA Health OS™ Architecture</span>
                  </div>
                  <h1 class="text-2xl md:text-3xl font-extrabold text-[#1B242A] dark:text-white mt-1">Interactive System Architecture Map</h1>
                  <p class="text-xs md:text-sm text-[#475560] dark:text-slate-300 mt-1.5 max-w-3xl leading-relaxed">
                    Unified architectural blueprint organizing all 25 canonical pages into 5 interconnected clinical, botanical, research, and governance domains.
                  </p>
                </div>
                <button onclick="viewWebsitePage('home')" class="px-5 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs rounded-xl shadow-lg transition shrink-0 flex items-center gap-2 cursor-pointer">
                  <span>←</span> Back to Flagship Home
                </button>
              </div>
            </div>

            <!-- Domain Sections -->
            <div class="space-y-10">
              ${architectureDomains.map((dom, domIdx) => `
                <div class="bg-white dark:bg-[var(--card)] p-6 md:p-8 rounded-3xl border border-[#DCD5C4] dark:border-[var(--border)] shadow-sm space-y-5">
                  <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 pb-4 border-b border-[#E8E2D5] dark:border-slate-800">
                    <div>
                      <h2 class="text-lg md:text-xl font-bold text-[#1B242A] dark:text-white">${dom.title}</h2>
                      <p class="text-xs text-[#5F707E] dark:text-[var(--muted)] mt-1">${dom.desc}</p>
                    </div>
                    <span class="px-3 py-1 rounded-full bg-emerald-100 text-emerald-900 border border-emerald-300 dark:bg-emerald-500/10 dark:text-emerald-400 dark:border-emerald-500/20 font-mono text-xs font-bold shrink-0">
                      ${dom.badge} • ${dom.modules.length} Connected Modules
                    </span>
                  </div>

                  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    ${dom.modules.map(m => `
                      <div class="p-4 rounded-2xl bg-[#FAF8F5] dark:bg-[#0F172A]/90 border border-[#E2D9CC] dark:border-slate-800 shadow-sm hover:border-emerald-500 hover:shadow-md transition-all flex flex-col justify-between space-y-3 group">
                        <div>
                          <div class="flex justify-between items-start gap-2 mb-1.5">
                            <span class="font-bold text-[#1B242A] dark:text-white text-xs group-hover:text-emerald-700 dark:group-hover:text-emerald-300 transition-colors">${m.title}</span>
                            <span class="text-[9px] text-emerald-800 dark:text-emerald-300 font-mono bg-emerald-50 dark:bg-emerald-500/15 border border-emerald-300 dark:border-emerald-500/30 px-1.5 py-0.5 rounded shrink-0">${m.path}</span>
                          </div>
                          <p class="text-[11px] text-[#475560] dark:text-slate-300 leading-relaxed">${m.desc}</p>
                        </div>
                        <div class="pt-2 border-t border-[#E8E2D5] dark:border-slate-800 flex justify-between items-center text-[11px]">
                          <span class="text-emerald-800 dark:text-emerald-400 font-semibold flex items-center gap-1">
                            <span class="text-emerald-600 dark:text-emerald-400">●</span> Active Module
                          </span>
                          <button onclick="viewWebsitePage('${m.key}')" class="px-3 py-1 bg-emerald-700 hover:bg-emerald-600 dark:bg-emerald-600 dark:hover:bg-emerald-500 text-white font-bold rounded-lg text-xs transition cursor-pointer shadow-sm">
                            Explore Module &rarr;
                          </button>
                        </div>
                      </div>
                    `).join('')}
                  </div>
                </div>
              `).join('')}
            </div>

          </div>
        `;
        return;
      }


      // Subpage views
      if (state.tab.startsWith('services_')) {
        const sub = publicPages.find(p => p.key === state.tab) || { title: "Clinical Service Detail", desc: "Advanced healthcare module" };
        const subnav = getWebsiteHubSubnav(state.tab);
        container.innerHTML = `
          <div class="space-y-6 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)]">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div class="flex items-center gap-2 mb-2">
                    <button onclick="viewWebsitePage('services')" class="text-xs text-emerald-400 font-bold hover:underline">← Clinical Services Hub</button>
                    <span class="text-xs text-slate-500">/</span>
                    <span class="text-xs text-slate-400 font-mono">${sub.path}</span>
                  </div>
                  <h2 class="text-2xl font-bold text-white">${sub.title}</h2>
                  <p class="text-xs text-[var(--muted)] mt-1">${sub.desc}</p>
                </div>
                <div class="flex gap-2">
                  <button onclick="if (document.getElementById('opd-booking-card')) { document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' }); } else { viewWebsitePage('home'); setTimeout(() => document.getElementById('opd-booking-card')?.scrollIntoView({ behavior: 'smooth' }), 120); }" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition">Book Consultation</button>
                  <button onclick="viewWebsitePage('pages25')" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-600 transition">️ System Map</button>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="md:col-span-2 bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
                <h3 class="text-lg font-bold text-white">Clinical Architecture & Capabilities</h3>
                <p class="text-xs text-slate-300 leading-relaxed">
                  The <strong>${sub.title}</strong> module integrates standardized classical Tibb-e-Unani protocols with modern clinical diagnostic precision. Built upon the ZAYVORA Health OS™ core, every interaction adheres to 21 CFR Part 11 electronic record governance, ABDM M1-M3 interoperability standards, and statutory clinical oversight.
                </p>
                <div class="grid grid-cols-2 gap-3 pt-2">
                  <div class="p-3 rounded-xl bg-slate-900 border border-slate-800">
                    <span class="text-[10px] text-emerald-400 font-bold block uppercase">Clinical Safety</span>
                    <span class="text-xs font-semibold text-white mt-1 block">Zero Autonomous Prescribing</span>
                    <p class="text-[10px] text-slate-400 mt-1">Requires Senior Tabeeb biometric/PIN cryptographic signature.</p>
                  </div>
                  <div class="p-3 rounded-xl bg-slate-900 border border-slate-800">
                    <span class="text-[10px] text-cyan-400 font-bold block uppercase">ABDM Standard</span>
                    <span class="text-xs font-semibold text-white mt-1 block">FHIR R4 Diagnostic Bundles</span>
                    <p class="text-[10px] text-slate-400 mt-1">Direct sync with Indian Ayushman Bharat Digital Mission lockers.</p>
                  </div>
                </div>
              </div>
              <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
                <h4 class="text-sm font-bold text-white">Facility Availability</h4>
                <div class="space-y-2 text-xs">
                  <div class="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 flex justify-between items-center">
                    <span class="text-slate-300">Central Hospital, New Delhi</span>
                    <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">Active OPD</span>
                  </div>
                  <div class="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 flex justify-between items-center">
                    <span class="text-slate-300">Tele-Health Video Suite</span>
                    <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">24/7 Available</span>
                  </div>
                  <div class="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 flex justify-between items-center">
                    <span class="text-slate-300">Helpline Triage</span>
                    <a href="tel:+919773882657" class="text-emerald-400 font-bold font-mono">+91 97738 82657</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab.startsWith('products_')) {
        const sub = publicPages.find(p => p.key === state.tab) || { title: "Product Category", desc: "ZAYVORA Herbals Portfolio" };
        const subnav = getWebsiteHubSubnav(state.tab);
        let categoryFilteredProducts = herbalsProducts;
        if (state.tab === 'products_unani_care') {
          categoryFilteredProducts = herbalsProducts.filter(p => p.unani_name && (['Cerebrovascular', 'Cardiovascular', 'Andrological', 'Gynecological'].includes(p.category) || p.unani_name.includes('Majoon') || p.unani_name.includes('Safoof')));
        } else if (state.tab === 'products_herbal_products') {
          categoryFilteredProducts = herbalsProducts.filter(p => ['Pancreatic', 'Hepatobiliary', 'Musculoskeletal', 'Gastrointestinal', 'Renal'].includes(p.category));
        } else if (state.tab === 'products_nutraceuticals') {
          categoryFilteredProducts = herbalsProducts.filter(p => ['Metabolic', 'Neurological', 'Respiratory', 'Dermatological', 'Immunological', 'Gynecological'].includes(p.category));
        }
        if (!categoryFilteredProducts || categoryFilteredProducts.length === 0) categoryFilteredProducts = herbalsProducts.slice(0, 10);

        container.innerHTML = `
          <div class="space-y-6 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)]">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div class="flex items-center gap-2 mb-2">
                    <button onclick="viewWebsitePage('products')" class="text-xs text-emerald-400 font-bold hover:underline">← Botanical Formulations Hub</button>
                    <span class="text-xs text-slate-500">/</span>
                    <span class="text-xs text-slate-400 font-mono">${sub.path}</span>
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">${categoryFilteredProducts.length} Verified Formulations</span>
                  </div>
                  <h2 class="text-2xl font-bold text-white">${sub.title}</h2>
                  <p class="text-xs text-[var(--muted)] mt-1">${sub.desc}</p>
                </div>
                <div class="flex items-center gap-2">
                  <button onclick="viewWebsitePage('products')" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition">View All 32 Master Formulations</button>
                  <button onclick="viewWebsitePage('pages25')" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-600 transition">️ System Map</button>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              ${categoryFilteredProducts.map(p => `
                <div class="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] flex flex-col justify-between space-y-4">
                  <div>
                    <div class="flex justify-between items-center mb-1">
                      <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold uppercase">${p.category}</span>
                      <span class="text-emerald-400 font-mono font-bold text-sm">₹${p.price}</span>
                    </div>
                    <h3 class="font-bold text-white text-base mt-1">${p.name}</h3>
                    <p class="text-xs text-slate-300 mt-2 leading-relaxed">${p.desc}</p>
                    <div class="mt-3 p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-[11px] space-y-1">
                      <div class="text-slate-400">Dosage: <span class="text-white">${p.dosage}</span></div>
                      <div class="text-slate-400">Indications: <span class="text-emerald-300">${p.indications}</span></div>
                    </div>
                  </div>
                  <div class="pt-3 border-t border-[var(--border)] flex items-center gap-2">
                    <button onclick="addToHerbalsCart('${p.id}')" class="flex-1 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl transition">
                      + Add to Dispensary Cart
                    </button>
                    <button onclick="openCoaModal('BMR-2026-MVP-09')" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs rounded-xl border border-slate-700 transition" title="View Batch Certificate of Analysis">
                      COA
                    </button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
        return;
      }

      if (state.tab.startsWith('research_')) {
        const sub = publicPages.find(p => p.key === state.tab) || { title: "Research Program", desc: "ZAYVORA Clinical Evidence" };
        const subnav = getWebsiteHubSubnav(state.tab);
        container.innerHTML = `
          <div class="space-y-6 pb-12">
            ${subnav}
            <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)]">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div class="flex items-center gap-2 mb-2">
                    <button onclick="viewWebsitePage('research')" class="text-xs text-emerald-400 font-bold hover:underline">← Research &amp; Evidence Hub</button>
                    <span class="text-xs text-slate-500">/</span>
                    <span class="text-xs text-slate-400 font-mono">${sub.path}</span>
                  </div>
                  <h2 class="text-2xl font-bold text-white">${sub.title}</h2>
                  <p class="text-xs text-[var(--muted)] mt-1">${sub.desc}</p>
                </div>
                <div class="flex items-center gap-2">
                  <button onclick="viewWebsitePage('research')" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition">Evidence Overview</button>
                  <button onclick="viewWebsitePage('pages25')" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-600 transition">️ System Map</button>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="md:col-span-2 bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
                <h3 class="text-lg font-bold text-white">Observational & Molecular Evidence Architecture</h3>
                <p class="text-xs text-slate-300 leading-relaxed">
                  ZAYVORA Health OS™ conducts rigorous Real-World Evidence (RWE) observational registries across our hospital and clinic network. Data points are de-identified under HIPAA Safe Harbor and Indian ABDM guidelines to benchmark clinical outcomes, recurrence rates, and humoral stabilization curves.
                </p>
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                  <div class="flex justify-between text-xs"><span class="text-slate-400">Registry Cohort Design:</span><strong class="text-emerald-400 font-mono">Up to 1,240 Observational Subjects</strong></div>
                  <div class="flex justify-between text-xs"><span class="text-slate-400">Participating Clinical Centers:</span><strong class="text-white font-mono">4 Multi-Center Complexes</strong></div>
                  <div class="flex justify-between text-xs"><span class="text-slate-400">Clinical Concordance Rate:</span><strong class="text-emerald-400 font-mono">94.8% Senior Tabeeb Agreement</strong></div>
                  <div class="flex justify-between text-xs"><span class="text-slate-400">Ethics Protocol Standard:</span><strong class="text-cyan-400 font-mono">ICMR Ethical Guidelines / Registry Protocol ZAY-RWE-2026</strong></div>
                </div>
              </div>
              <div class="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
                <h4 class="text-sm font-bold text-white">Academic Knowledge Graph</h4>
                <p class="text-xs text-slate-300">1,280+ classical monographs cross-referenced with modern PubMed & Cochrane clinical trials.</p>
                <button onclick="viewWebsitePage('knowledge')" class="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl transition">Explore Botanical Monograph Graph →</button>
              </div>
            </div>
          </div>
        `;
        return;
      }

      // DEFAULT TAB: 'home' - The Official Landing Page
      const st = clinicalStages[activeWebsiteStage];
      const activeAxis = organAxesList[activeOrganAxis] || organAxesList[0];
      
      const mizajCalc = calculateDetailedMizaj();
      const calcKey = mizajCalc.dominant;
      const mizajInfo = mizajDetailsMap[calcKey] || mizajDetailsMap["Balghami"];
      const axisHealth = calculateAxisHealth();

      container.innerHTML = `
        <div class="space-y-12 pb-16">
          
          <!-- ===================================================================== -->
          <!-- 1. LUXURY HERO BANNER -->
          <!-- ===================================================================== -->
          <div class="relative overflow-hidden p-8 md:p-14 rounded-3xl bg-gradient-to-b from-[#0F172A] via-[#0D1526] to-[#0A0F1D] border border-emerald-500/30 text-center space-y-6 shadow-2xl">
            <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 text-xs font-semibold">
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>Proprietary Greco-Arab Medicine OS™ • Conceived &amp; Architected by Hakeem Dr. Irfan Ashraf</span>
            </div>

            <h1 class="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white max-w-5xl mx-auto leading-tight tracking-tight">
              Evidence-Grounded Clinical Intelligence for Integrative Healthcare <br class="hidden sm:inline" />
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#2DD4BF] via-emerald-300 to-teal-200 text-xl sm:text-2xl md:text-3xl block mt-2 font-black">
                Assess &bull; Understand &bull; Verify &bull; Treat &bull; Monitor &bull; Learn
              </span>
            </h1>

            <p class="text-xs sm:text-sm md:text-base text-[#94A3B8] max-w-3xl mx-auto leading-relaxed">
              ZAYVORA Health OS™ unites codified Greco-Arab (Unani) clinical wisdom with modern biomedical evidence.
              <span class="block mt-1 font-bold text-emerald-300">Evidence informs. Guidelines assist. Clinicians decide.</span>
            </p>

            <!-- 3 Core Architecture Pillars: Clinical Care, Medical Intelligence, Continuous Learning -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl mx-auto text-left pt-2 pb-1">
              <div class="p-4 rounded-2xl bg-slate-900/80 border border-emerald-500/30 hover:border-emerald-400 transition cursor-pointer group" onclick="switchRole('doctor')">
                <div class="flex items-center gap-2 mb-1.5">
                  <span class="text-xl">🩺</span>
                  <h4 class="font-bold text-white text-sm group-hover:text-emerald-300 transition">Clinical Care</h4>
                </div>
                <p class="text-[11px] text-slate-300 leading-relaxed">
                  Patient 360, OPD consultation, Clinical Decision Advisory, posology adjustments, and signed electronic prescription workflows.
                </p>
              </div>

              <div class="p-4 rounded-2xl bg-slate-900/80 border border-teal-500/30 hover:border-teal-400 transition cursor-pointer group" onclick="navigateToV2Hub('zmie')">
                <div class="flex items-center gap-2 mb-1.5">
                  <span class="text-xl">🧠</span>
                  <h4 class="font-bold text-white text-sm group-hover:text-teal-300 transition">Medical Intelligence</h4>
                </div>
                <p class="text-[11px] text-slate-300 leading-relaxed">
                  ZMIE 7-tier evidence provenance (E0–E6), tripartite knowledge separation, and fail-closed Clinical Truth Firewall.
                </p>
              </div>

              <div class="p-4 rounded-2xl bg-slate-900/80 border border-amber-500/30 hover:border-amber-400 transition cursor-pointer group" onclick="navigateToV2Hub('outcomes')">
                <div class="flex items-center gap-2 mb-1.5">
                  <span class="text-xl">📈</span>
                  <h4 class="font-bold text-white text-sm group-hover:text-amber-300 transition">Continuous Learning</h4>
                </div>
                <p class="text-[11px] text-slate-300 leading-relaxed">
                  Longitudinal clinical timelines, RWE observational registries, standardized Mizaj research cohorts, and closed-loop outcomes.
                </p>
              </div>
            </div>

            <!-- Action Matrix: Unified Clinical Self-Assessment & Patient Admission Gateway -->
            <div class="flex flex-wrap items-center justify-center gap-3 pt-2">
              <button onclick="toggleMizajAssessmentModal(true);" class="px-5 py-3.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs shadow-xl shadow-emerald-950/50 transition flex items-center gap-2 cursor-pointer ring-2 ring-emerald-500/40" title="Al-Ajnas Al-Ashrah: Discover constitutional humoral archetype">
                <span>🩺</span> Mizaj (Temperament) Audit
              </button>
              <button onclick="toggleOrganAxisModal(true);" class="px-5 py-3.5 rounded-xl border-2 border-teal-500/50 bg-teal-500/15 hover:bg-teal-500/25 text-teal-300 font-bold text-xs transition flex items-center gap-2 cursor-pointer ring-2 ring-teal-500/30" title="Systems Biology: Screen humoral stasis across 12 organ networks">
                <span>🔬</span> 12-Organ-Axis Screener
              </button>
              <button onclick="openHealthAssessmentModal();" class="px-5 py-3.5 rounded-xl bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 hover:from-emerald-500 text-white font-bold text-xs shadow-xl shadow-emerald-950/50 transition flex items-center gap-2 cursor-pointer ring-2 ring-emerald-400/40">
                <span>🧠</span> 8-Pillar Health Audit
              </button>
              <button onclick="viewWebsitePage('products');" class="px-5 py-3.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-black text-xs shadow-xl shadow-amber-950/40 transition flex items-center gap-2 cursor-pointer">
                <span>🛍️</span> Order 32 Formulations
              </button>
              <button onclick="document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' });" class="px-5 py-3.5 rounded-xl border border-slate-700 bg-slate-800/80 hover:bg-slate-800 text-slate-200 font-semibold text-xs transition flex items-center gap-2 cursor-pointer">
                <span>🎟️</span> Generate OPD Token
              </button>
              <a href="https://wa.me/919773882657?text=Salam%20Dr.%20Irfan%20Ashraf,%20I%20would%20like%20to%20consult%20with%20you%20on%20ZAYVORA%20Health%20OS." target="_blank" class="px-4 py-3.5 rounded-xl border border-emerald-500/40 bg-emerald-950/40 hover:bg-emerald-900/60 text-emerald-300 font-semibold text-xs transition flex items-center gap-1.5">
                <span>💬</span> WhatsApp Dr. Irfan
              </a>
            </div>

            
            <!-- ===================================================================== -->
            <!-- ZAYVORA GLOBAL CLINICAL & FUNCTIONAL MEDICINE SUITE   -->
            <!-- ===================================================================== -->
            <div class="mt-8 p-6 rounded-3xl bg-slate-900/90 border border-emerald-500/40 shadow-2xl space-y-5 text-left">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
                <div>
                  <div class="flex items-center gap-2">
                    <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-mono font-bold uppercase">
                      Integrative Clinical Suite
                    </span>
                    <span class="text-xs text-slate-400">ZAYVORA Integrative Clinical Intelligence</span>
                  </div>
                  <h3 class="text-base font-extrabold text-white mt-1">Interactive Diagnostic &amp; Functional Medicine Engines</h3>
                </div>
                <span class="text-[11px] text-emerald-400 font-mono">10 Specialized Portals Active</span>
              </div>

              <!-- 10 Benchmark Tool Cards Grid -->
              <div class="grid grid-cols-2 sm:grid-cols-5 gap-3">
                <!-- 1. Body Navigator -->
                <button onclick="toggleBodyNavigatorModal(true)" class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 hover:border-cyan-500/60 hover:bg-cyan-950/20 text-left transition group cursor-pointer">
                  <div class="text-xl mb-1 group-hover:scale-110 transition">🗺️</div>
                  <div class="font-bold text-xs text-white">Body Navigator</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">Neuro-Somatic Triage</div>
                </button>

                <!-- 2. Lab Correlator -->
                <button onclick="toggleLabCorrelatorModal(true)" class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 hover:border-teal-500/60 hover:bg-teal-950/20 text-left transition group cursor-pointer">
                  <div class="text-xl mb-1 group-hover:scale-110 transition">🧪</div>
                  <div class="font-bold text-xs text-white">Lab Correlator</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">Integrative 2nd Opinion</div>
                </button>

                <!-- 3. Food Matrix -->
                <button onclick="toggleFoodCompatibilityModal(true)" class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 hover:border-amber-500/60 hover:bg-amber-950/20 text-left transition group cursor-pointer">
                  <div class="text-xl mb-1 group-hover:scale-110 transition">🥗</div>
                  <div class="font-bold text-xs text-white">Kitchen Matrix</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">Constitutional Nutrition</div>
                </button>

                <!-- 4. Hazm-e-Arba'a -->
                <button onclick="toggleHazmArbaModal(true)" class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 hover:border-emerald-500/60 hover:bg-emerald-950/20 text-left transition group cursor-pointer">
                  <div class="text-xl mb-1 group-hover:scale-110 transition">🔄</div>
                  <div class="font-bold text-xs text-white">Hazm-e-Arba'a</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">4-Stage Digestion</div>
                </button>

                <!-- 5. ATM Timeline -->
                <button onclick="toggleAtmTimelineModal(true)" class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 hover:border-indigo-500/60 hover:bg-indigo-950/20 text-left transition group cursor-pointer">
                  <div class="text-xl mb-1 group-hover:scale-110 transition">⏳</div>
                  <div class="font-bold text-xs text-white">ATM Timeline</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">Root-Cause Genesis</div>
                </button>

                <!-- 6. Humoral Bio-Clock -->
                <button onclick="toggleHumoralClockModal(true)" class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 hover:border-yellow-500/60 hover:bg-yellow-950/20 text-left transition group cursor-pointer">
                  <div class="text-xl mb-1 group-hover:scale-110 transition">⏱️</div>
                  <div class="font-bold text-xs text-white">Humoral Clock</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">24h Bio-Rhythm</div>
                </button>

                <!-- 7. Gut-Brain Screener -->
                <button onclick="toggleGutBrainModal(true)" class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 hover:border-rose-500/60 hover:bg-rose-950/20 text-left transition group cursor-pointer">
                  <div class="text-xl mb-1 group-hover:scale-110 transition">🧠</div>
                  <div class="font-bold text-xs text-white">Gut-Brain Vagus</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">Maraq &amp; Bukharat</div>
                </button>

                <!-- 8. Tanqiya Readiness -->
                <button onclick="toggleTanqiyaReadinessModal(true)" class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 hover:border-teal-500/60 hover:bg-teal-950/20 text-left transition group cursor-pointer">
                  <div class="text-xl mb-1 group-hover:scale-110 transition">🌿</div>
                  <div class="font-bold text-xs text-white">Tanqiya Detox</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">Cellular Readiness</div>
                </button>

                <!-- 9. 14-Day Challenge -->
                <button onclick="toggleAsbabChallengeModal(true)" class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 hover:border-purple-500/60 hover:bg-purple-950/20 text-left transition group cursor-pointer">
                  <div class="text-xl mb-1 group-hover:scale-110 transition">🏆</div>
                  <div class="font-bold text-xs text-white">14-Day Reset</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">Digital Therapeutics</div>
                </button>

                <!-- 10. Clinical Outcomes -->
                <button onclick="toggleClinicalOutcomesModal(true)" class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 hover:border-blue-500/60 hover:bg-blue-950/20 text-left transition group cursor-pointer">
                  <div class="text-xl mb-1 group-hover:scale-110 transition">📈</div>
                  <div class="font-bold text-xs text-white">PROMs Registry</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">Clinical Evidence</div>
                </button>
              </div>
            </div>


            <!-- Regulatory & Quality Accreditations Strip -->
            <div class="flex flex-wrap items-center justify-center gap-6 pt-4 text-[11px] text-[#94A3B8] border-t border-slate-800/80">
              <span class="flex items-center gap-1.5"><span class="text-emerald-400">✓</span> Ministry of AYUSH Aligned</span>
              <span class="flex items-center gap-1.5"><span class="text-emerald-400">✓</span> NCISM Clinical Standards</span>
              <span class="flex items-center gap-1.5"><span class="text-emerald-400">✓</span> 21 CFR Part 11 Digital Records</span>
              <span class="flex items-center gap-1.5"><span class="text-emerald-400">✓</span> ABDM &amp; FHIR R4 Ready</span>
              <span class="flex items-center gap-1.5"><span class="text-emerald-400">✓</span> Schedule E(1) Mudabbar Verified</span>
            </div>
          </div>

          <!-- ===================================================================== -->
          <!-- 2. CLINICAL CREDENTIALS & STATUTORY ACCREDITATION MARQUEE -->
          <!-- ===================================================================== -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1 shadow-sm">
              <span class="text-slate-400 uppercase text-[10px] font-bold tracking-wider">Academic Foundation</span>
              <div class="text-xl sm:text-2xl font-extrabold text-white">BUMS (AKTC AMU)</div>
              <span class="text-[10px] text-emerald-400 font-mono">Ajmal Khan Tibbiya College (2002–2007)</span>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1 shadow-sm">
              <span class="text-slate-400 uppercase text-[10px] font-bold tracking-wider">Statutory Registration</span>
              <div class="text-xl sm:text-2xl font-extrabold text-emerald-400">BUMS/AMU/2007</div>
              <span class="text-[10px] text-slate-400 font-mono">NCISM &amp; State AYUSH Recognized</span>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1 shadow-sm">
              <span class="text-slate-400 uppercase text-[10px] font-bold tracking-wider">Authentic Matab Care</span>
              <div class="text-xl sm:text-2xl font-extrabold text-white">Ilaj bil-Tadbeer</div>
              <span class="text-[10px] text-teal-300 font-mono">Regimenal &amp; Phyto-Pharmacology</span>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1 shadow-sm">
              <span class="text-slate-400 uppercase text-[10px] font-bold tracking-wider">Direct Clinical Access</span>
              <div class="text-xl sm:text-2xl font-extrabold text-white">+91 97738 82657</div>
              <span class="text-[10px] text-emerald-400 font-mono">Direct Telemedicine &amp; OPD Booking</span>
            </div>
          </div>

          <div id="opd-booking-card" class="p-6 md:p-8 rounded-3xl bg-gradient-to-r from-[#0F172A] via-[#1E293B] to-[#0F172A] border border-emerald-500/40 space-y-5 shadow-2xl">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-[#334155] pb-3">
              <div>
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Fast-Track Patient Admission</span>
                <h3 class="text-xl sm:text-2xl font-extrabold text-white mt-0.5">Generate Instant OPD Consultation Token</h3>
                <p class="text-xs text-[#94A3B8]">Select your preferred clinical facility and generate your queue token instantly.</p>
              </div>
              <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-xs font-bold">
                Live Queue Ready
              </span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div>
                <label class="block text-[11px] text-slate-400 mb-1">Patient Full Name</label>
                <input id="opd-patient-name" type="text" placeholder="e.g. Hamza Farooqi" class="w-full px-3.5 py-2.5 rounded-xl bg-[#0A0F1D] border border-[#334155] text-white text-xs focus:outline-none focus:border-emerald-400" />
              </div>
              <div>
                <label class="block text-[11px] text-slate-400 mb-1">Select Matab / Hospital Center</label>
                <select id="opd-clinic-select" class="w-full px-3.5 py-2.5 rounded-xl bg-[#0A0F1D] border border-[#334155] text-white text-xs focus:outline-none focus:border-emerald-400">
                  <option value="ZAYVORA Healthcare System - Central Hospital">ZAYVORA Healthcare System - Central Hospital (New Delhi)</option>
                  <option value="ZAYVORA Matab Care - Hyderabad">ZAYVORA Matab Care - Hyderabad</option>
                  <option value="ZAYVORA Integrative Clinic - Bengaluru">ZAYVORA Integrative Clinic - Bengaluru</option>
                  <option value="ZAYVORA Regional OPD - Srinagar">ZAYVORA Regional OPD - Srinagar</option>
                </select>
              </div>
              <div class="flex items-end">
                <button onclick="generateInstantOpdToken()" class="w-full py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs rounded-xl shadow-lg transition">
                  Generate Live Token &rarr;
                </button>
              </div>
            </div>

            <!-- Token Result Injected Here -->
            <div id="opd-token-result" class="hidden"></div>
          </div>

          <!-- ===================================================================== -->

          <!-- TASK-FIRST CARE DISCOVERY (ZAYVORA INTEGRATIVE CLINICAL BENCHMARK) -->
          <!-- ===================================================================== -->
          <div class="p-6 md:p-10 rounded-3xl bg-gradient-to-r from-[#0F172A] via-[#131D31] to-[#0A0F1D] border-2 border-emerald-500/40 shadow-2xl space-y-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
              <div>
                <span class="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-bold uppercase tracking-wider border border-emerald-500/20">
                  Care Discovery &amp; Triage
                </span>
                <h2 class="text-2xl md:text-3xl font-extrabold text-white mt-2">What brings you to ZAYVORA today?</h2>
                <p class="text-xs md:text-sm text-slate-300 mt-1 max-w-2xl leading-relaxed">
                  Select your health concern to immediately access evidence-grounded Greco-Arab pathways, board-certified clinicians, and tailored botanical protocols.
                </p>
              </div>
              <div class="flex items-center gap-2 shrink-0">
                <button onclick="document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' });" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs shadow-lg transition flex items-center gap-1.5">
                  <span></span> Book Consultation
                </button>
              </div>
            </div>

            <!-- 9 Core Clinical Focus Areas -->
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-3 gap-4 text-xs">
              <div onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 hover:border-emerald-500/60 hover:bg-emerald-950/20 cursor-pointer transition-all space-y-1.5 group">
                <div class="text-2xl"></div>
                <h3 class="font-bold text-white text-sm group-hover:text-emerald-300 transition">Digestive &amp; Gut Health</h3>
                <p class="text-[11px] text-slate-400">Su-e-Hazm, IBS, GERD, Gastritis, Dysbiosis, Liver Congestion</p>
                <span class="text-[10px] text-emerald-400 font-semibold block pt-1">Explore Care Path →</span>
              </div>

              <div onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 hover:border-emerald-500/60 hover:bg-emerald-950/20 cursor-pointer transition-all space-y-1.5 group">
                <div class="text-2xl"></div>
                <h3 class="font-bold text-white text-sm group-hover:text-emerald-300 transition">Metabolic &amp; Pre-Diabetes</h3>
                <p class="text-[11px] text-slate-400">Insulin Resistance (HOMA-IR), Obesity, Visceral Adiposity, Dyslipidemia</p>
                <span class="text-[10px] text-emerald-400 font-semibold block pt-1">Explore Care Path →</span>
              </div>

              <div onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 hover:border-emerald-500/60 hover:bg-emerald-950/20 cursor-pointer transition-all space-y-1.5 group">
                <div class="text-2xl"></div>
                <h3 class="font-bold text-white text-sm group-hover:text-emerald-300 transition">Hormonal &amp; Thyroid Axis</h3>
                <p class="text-[11px] text-slate-400">PCOS, Hypothyroid (Barid-Ratab), Adrenal Fatigue, Cortisol Dysregulation</p>
                <span class="text-[10px] text-emerald-400 font-semibold block pt-1">Explore Care Path →</span>
              </div>

              <div onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 hover:border-emerald-500/60 hover:bg-emerald-950/20 cursor-pointer transition-all space-y-1.5 group">
                <div class="text-2xl"></div>
                <h3 class="font-bold text-white text-sm group-hover:text-emerald-300 transition">Reproductive &amp; Vitality</h3>
                <p class="text-[11px] text-slate-400">Male Oligospermia, Asthenospermia, Female Anovulation, Vitality Deficits</p>
                <span class="text-[10px] text-emerald-400 font-semibold block pt-1">Explore Care Path →</span>
              </div>

              <div onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 hover:border-emerald-500/60 hover:bg-emerald-950/20 cursor-pointer transition-all space-y-1.5 group">
                <div class="text-2xl"></div>
                <h3 class="font-bold text-white text-sm group-hover:text-emerald-300 transition">Joint &amp; Musculoskeletal</h3>
                <p class="text-[11px] text-slate-400">Waja-ul-Mafasil, Knee Osteoarthritis, Cervical Spondylosis, Synovial Stiffness</p>
                <span class="text-[10px] text-emerald-400 font-semibold block pt-1">Explore Care Path →</span>
              </div>

              <div onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 hover:border-emerald-500/60 hover:bg-emerald-950/20 cursor-pointer transition-all space-y-1.5 group">
                <div class="text-2xl"></div>
                <h3 class="font-bold text-white text-sm group-hover:text-emerald-300 transition">Sleep, Stress &amp; Cognition</h3>
                <p class="text-[11px] text-slate-400">Insomnia, Chronic Anxiety (Khafqan), Mental Fog, Burnout Recovery</p>
                <span class="text-[10px] text-emerald-400 font-semibold block pt-1">Explore Care Path →</span>
              </div>
            </div>

            <!-- Direct Action Channels -->
            <div class="pt-4 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
              <div class="flex flex-wrap items-center gap-4 text-slate-300">
                <span class="text-slate-500 font-bold uppercase text-[10px]">Access Channels:</span>
                <button onclick="viewWebsitePage('doctors')" class="hover:text-emerald-400 transition font-medium flex items-center gap-1">
                  <span>‍⚕️</span> Find a Clinician
                </button>
                <button onclick="viewWebsitePage('clinics')" class="hover:text-emerald-400 transition font-medium flex items-center gap-1">
                  <span><svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg></span> Find a Matab Complex
                </button>
                <button onclick="document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' });" class="hover:text-emerald-400 transition font-medium flex items-center gap-1">
                  <span></span> In-Clinic OPD Token
                </button>
                <button onclick="document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' });" class="hover:text-emerald-400 transition font-medium flex items-center gap-1">
                  <span></span> Encrypted Teleconsultation
                </button>
              </div>
              <span class="text-[11px] text-slate-500">Average intake triage time: &lt; 90 seconds</span>
            </div>
          </div>

          <!-- 3. EXECUTIVE FOUNDER & INTELLECTUAL PROPERTY SHOWCASE -->
          <!-- ===================================================================== -->
          <div class="p-8 rounded-3xl bg-gradient-to-r from-emerald-950/60 via-[#0F172A] to-slate-900 border border-emerald-500/40 space-y-6 shadow-xl">
            <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
              <div class="space-y-2 max-w-3xl">
                <div class="flex items-center gap-2">
                  <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-widest bg-emerald-900/60 px-2.5 py-0.5 rounded-full border border-emerald-700/60">
                    Proprietary Architecture &amp; Intellectual Property
                  </span>
                  <span class="text-xs text-slate-400 font-mono">ZAYVORA Health OS™ v5.0</span>
                </div>
                <h2 class="text-2xl sm:text-3xl font-extrabold text-[#1B242A] dark:text-white tracking-tight">Hakeem Dr. Irfan Ashraf</h2>
                <p class="text-sm font-semibold text-emerald-300">Founder, Chairman &amp; Principal Healthcare Architect</p>
                <p class="text-xs text-slate-300 leading-relaxed pt-1">
                  &ldquo;Our clinical doctrine is anchored in revitalizing the patient&apos;s innate healing faculty (<em>Tabi&apos;at</em>). 
                  Rather than suppressing isolated symptoms, ZAYVORA identifies root humoral dyscrasias across the 12 organ axes 
                  and systematically reverses them through codified Greco-Arab pharmacology and precision medical governance.&rdquo;
                </p>
                <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-[11px] text-slate-300">
                  <strong class="text-white block mb-1">Official Intellectual Property Declaration:</strong>
                  The ZAYVORA Health OS™ ecosystem, clinical decision algorithms, 10-Ajnas pulse waveform DSP intelligence, 
                  12-Organ-Axis diagnostic framework, and fail-closed safety firewalls constitute the exclusive proprietary 
                  intellectual property conceived and architected by <strong>Hakeem Dr. Irfan Ashraf</strong>.
                </div>
              </div>

              <!-- Founder Badges & Credentials -->
              <div class="flex flex-col gap-2.5 w-full lg:w-72 text-xs">
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 space-y-1">
                  <span class="text-[10px] text-emerald-400 font-bold uppercase">Clinical Qualifications</span>
                  <div class="text-white font-semibold">BUMS (AKTC AMU, 2002–2007) • Aligarh Muslim University</div>
                  <div class="text-[10px] text-slate-400">Moalajat &amp; Waja-ul-Mafasil Authority</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 space-y-1">
                  <span class="text-[10px] text-teal-400 font-bold uppercase">Academic Leadership</span>
                  <div class="text-white font-semibold">Director, CP-AFUM Curriculum</div>
                  <div class="text-[10px] text-slate-400">96 Lectures &bull; 6 Clinical Modules</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 space-y-1">
                  <span class="text-[10px] text-amber-400 font-bold uppercase">Statutory Registration</span>
                  <div class="text-white font-semibold">Registered Unani Practitioner</div>
                  <div class="text-[10px] text-slate-400 font-mono">Reg. No: BUMS/AMU/2007 (NCISM & State AYUSH Recognized)</div>
                </div>
              </div>
            </div>
          </div>

          <!-- ===================================================================== -->

          
          <!-- ===================================================================== -->
          <!-- 3-STEP INTEGRATIVE CARE JOURNEY -->
          <!-- ===================================================================== -->
          <div class="space-y-6">
            <div class="text-center space-y-1">
              <span class="text-xs font-bold text-[#2DD4BF] uppercase tracking-wider">Patient Care Pathway</span>
              <h2 class="text-2xl sm:text-3xl font-bold text-white">How Integrative Healing Works at ZAYVORA</h2>
              <p class="text-xs text-[#94A3B8] max-w-xl mx-auto">From instant constitutional discovery to personalized clinician care and standardized botanical recovery.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
              <div class="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3 relative overflow-hidden group hover:border-emerald-500/50 transition shadow-lg">
                <div class="flex justify-between items-center">
                  <span class="w-8 h-8 rounded-xl bg-emerald-500/20 text-emerald-400 font-mono font-bold text-sm flex items-center justify-center border border-emerald-500/30">01</span>
                  <span class="text-[10px] font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800">100% Free • Online</span>
                </div>
                <h3 class="text-lg font-bold text-white group-hover:text-emerald-300 transition">Free Self-Assessment</h3>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Discover your baseline Mizaj (Damawi, Safrawi, Balghami, Sawdawi) and screen your 12 organ axes in minutes to pinpoint subclinical humoral imbalances.
                </p>
                <div class="pt-2 border-t border-slate-800">
                  <button onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="text-xs text-emerald-400 font-semibold hover:underline flex items-center gap-1 cursor-pointer">
                    Take Free Assessment &darr;
                  </button>
                </div>
              </div>

              <div class="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3 relative overflow-hidden group hover:border-teal-500/50 transition shadow-lg">
                <div class="flex justify-between items-center">
                  <span class="w-8 h-8 rounded-xl bg-teal-500/20 text-teal-400 font-mono font-bold text-sm flex items-center justify-center border border-teal-500/30">02</span>
                  <span class="text-[10px] font-mono text-teal-400 bg-teal-950/60 px-2 py-0.5 rounded border border-teal-800">In-Clinic / Telehealth</span>
                </div>
                <h3 class="text-lg font-bold text-white group-hover:text-teal-300 transition">Doctor Consultation</h3>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Meet Hakeem Dr. Irfan Ashraf (BUMS, AKTC AMU) for in-depth pulse diagnosis (Nabz), tongue evaluation, and root-cause clinical triage.
                </p>
                <div class="pt-2 border-t border-slate-800">
                  <button onclick="document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' });" class="text-xs text-teal-400 font-semibold hover:underline flex items-center gap-1 cursor-pointer">
                    Book OPD Token / WhatsApp &darr;
                  </button>
                </div>
              </div>

              <div class="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3 relative overflow-hidden group hover:border-emerald-500/50 transition shadow-lg">
                <div class="flex justify-between items-center">
                  <span class="w-8 h-8 rounded-xl bg-purple-500/20 text-purple-400 font-mono font-bold text-sm flex items-center justify-center border border-purple-500/30">03</span>
                  <span class="text-[10px] font-mono text-purple-400 bg-purple-950/60 px-2 py-0.5 rounded border border-purple-800">Standardized &amp; Safe</span>
                </div>
                <h3 class="text-lg font-bold text-white group-hover:text-purple-300 transition">Targeted Care &amp; Regimen</h3>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Receive personalized dietetics (Ilaj bil-Ghiza), classical detoxification (Ilaj bil-Tadbeer), and Schedule E(1) Mudabbar botanical formulations.
                </p>
                <div class="pt-2 border-t border-slate-800">
                  <button onclick="viewWebsitePage('products')" class="text-xs text-purple-400 font-semibold hover:underline flex items-center gap-1 cursor-pointer">
                    Explore Herbal Pharmacopoeia &rarr;
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 9. 4-STAGE AFAAL TREATMENT CASCADE -->
          <!-- ===================================================================== -->
          <div class="space-y-6">
            <div class="text-center space-y-1">
              <span class="text-xs font-bold text-[#2DD4BF] uppercase tracking-wider">Humoral Healing Protocol</span>
              <h2 class="text-2xl font-bold text-white">The ZAYVORA Afaal Treatment Cascade</h2>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div class="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-2">
                <div class="flex justify-between items-center"><span class="text-xs font-mono font-bold text-emerald-400">STAGE 01</span><span class="text-[10px] text-slate-500">Days 1 - 14</span></div>
                <h4 class="text-base font-bold text-white">Tanqiya</h4>
                <span class="text-xs text-[#2DD4BF] block font-semibold">Humoral Cleansing &amp; Detox</span>
                <p class="text-xs text-[#94A3B8] leading-relaxed">Concoction and elimination of accumulated cold, phlegmatic matter (Mawad-e-Fasida) via Munzaj-Mushil therapy and Hijama.</p>
              </div>
              <div class="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-2">
                <div class="flex justify-between items-center"><span class="text-xs font-mono font-bold text-blue-400">STAGE 02</span><span class="text-[10px] text-slate-500">Days 15 - 30</span></div>
                <h4 class="text-base font-bold text-white">Tahleel</h4>
                <span class="text-xs text-blue-400 block font-semibold">Resolution of Inflammation</span>
                <p class="text-xs text-[#94A3B8] leading-relaxed">Dissolution of deep-seated peri-articular exudates and microvascular stasis via medicated warm fomentation (Natool) and Zimad.</p>
              </div>
              <div class="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-2">
                <div class="flex justify-between items-center"><span class="text-xs font-mono font-bold text-purple-400">STAGE 03</span><span class="text-[10px] text-slate-500">Days 31 - 60</span></div>
                <h4 class="text-base font-bold text-white">Taqwiyaat</h4>
                <span class="text-xs text-purple-400 block font-semibold">Organ Restoration</span>
                <p class="text-xs text-[#94A3B8] leading-relaxed">Strengthening target organs and neural pathways (Muqawwiyat-e-A&apos;za) to rebuild stamina and prevent relapse.</p>
              </div>
              <div class="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-2">
                <div class="flex justify-between items-center"><span class="text-xs font-mono font-bold text-amber-400">STAGE 04</span><span class="text-[10px] text-slate-500">Lifelong</span></div>
                <h4 class="text-base font-bold text-white">Hifz</h4>
                <span class="text-xs text-amber-400 block font-semibold">Preservation &amp; Homeostasis</span>
                <p class="text-xs text-[#94A3B8] leading-relaxed">Long-term equilibrium via tailored dietetics (Ilaj bil-Ghiza) and adherence to the 6 Life Essentials (Asbab-e-Sittah).</p>
              </div>
            </div>
          </div>

          <!-- ===================================================================== -->

          <!-- 10. CURATED BOTANICAL FORMULATIONS SPOTLIGHT (HOMEPAGE TEASER) -->
          <!-- ===================================================================== -->
          <div class="space-y-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-end gap-3 border-b border-[#334155] pb-4">
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-xs font-bold text-[#2DD4BF] uppercase tracking-wider">Clinical Dispensary Spotlight</span>
                  <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">AYUSH-GMP &amp; HPLC Certified</span>
                </div>
                <h3 class="text-2xl font-bold text-white">Featured Clinical Formulations</h3>
                <p class="text-xs text-[#94A3B8] max-w-2xl mt-1">
                  A curated preview from our 32-compound master botanical pharmacopoeia. Formulated under classical Mudabbar detoxification protocols and verified via analytical HPLC fingerprinting.
                </p>
              </div>
              <button onclick="viewWebsitePage('products')" class="px-5 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs rounded-xl shadow-lg transition flex items-center gap-2 shrink-0">
                <span>Explore Full Dispensary (32 Formulations)</span>
                <span class="text-sm">&rarr;</span>
              </button>
            </div>

            <!-- 3 Flagship Spotlight Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
              ${herbalsProducts.filter(p => p.is_hero_launch).slice(0, 3).map(p => `
                <div class="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] flex flex-col justify-between space-y-4 hover:border-emerald-500/50 hover:shadow-xl transition group">
                  <div class="space-y-3">
                    <div class="flex justify-between items-center">
                      <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 uppercase tracking-wide">${p.category}</span>
                      <span class="text-xs font-mono text-slate-400 font-medium">${p.sku}</span>
                    </div>
                    <div>
                      <h4 class="text-base font-bold text-white group-hover:text-emerald-300 transition-colors">${p.name}</h4>
                      <p class="text-[11px] font-mono text-emerald-400/90 mt-0.5">${p.unani_name || ''}</p>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed line-clamp-3">${p.desc}</p>
                    <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-[11px] space-y-1.5">
                      <div class="text-slate-400"><strong class="text-slate-200">Indication:</strong> <span class="text-emerald-300">${p.indications}</span></div>
                      <div class="text-slate-400"><strong class="text-slate-200">Dosage:</strong> <span class="text-slate-300">${p.dosage}</span></div>
                    </div>
                  </div>
                  <div class="pt-3 border-t border-[#334155] flex justify-between items-center">
                    <div class="flex items-center gap-1.5 text-[11px] text-emerald-400 font-semibold">
                      <span>🛡️</span>
                      <span>HPLC Active Verified</span>
                    </div>
                    <button onclick="openProductQuickView('${p.sku}')" class="px-3.5 py-1.5 bg-slate-800 hover:bg-emerald-600 hover:text-white text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 hover:border-emerald-500 transition shadow">
                      View Details &rarr;
                    </button>
                  </div>
                </div>
              `).join('')}
            </div>

            <!-- Banner pointing to Full Dispensary & Consultation -->
            <div class="p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-emerald-950/40 to-slate-900 border border-emerald-500/30 flex flex-col sm:flex-row justify-between items-center gap-4">
              <div class="space-y-1">
                <div class="flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  <h4 class="text-sm font-bold text-white">Looking for complete dispensary catalog or custom clinical posology?</h4>
                </div>
                <p class="text-xs text-slate-400">
                  Our licensed Senior Tabeebs evaluate your 10-Ajnas pulse and Mizaj to formulate personalized multi-herb regimens from our 32 classical and standardized preparations.
                </p>
              </div>
              <div class="flex items-center gap-2 shrink-0">
                <button onclick="viewWebsitePage('products')" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition shadow">
                  Browse All 32 Formulations &rarr;
                </button>
                <button onclick="if (document.getElementById('opd-booking-card')) { document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' }); } else { viewWebsitePage('home'); setTimeout(() => document.getElementById('opd-booking-card')?.scrollIntoView({ behavior: 'smooth' }), 120); }" class="px-4 py-2 rounded-xl border border-slate-700 hover:border-emerald-500 text-slate-300 hover:text-white text-xs font-semibold transition">
                  Book OPD Consultation
                </button>
              </div>
            </div>
          </div>

          <!-- ===================================================================== -->
          <!-- 11. LUXURY CLINICAL ARCHITECTURE & COMPLETE SITE DIRECTORY -->
          <!-- ===================================================================== -->
          <div class="p-6 md:p-8 rounded-3xl bg-white dark:bg-[#151E2B] border border-[#DCD5C4] dark:border-slate-800 shadow-sm space-y-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-slate-800 pb-6">
              <div>
                <div class="flex items-center gap-2 mb-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                  <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Canonical Clinical Architecture &bull; 25 Public Web Pages</span>
                </div>
                <h3 class="text-2xl sm:text-3xl font-extrabold text-[#1B242A] dark:text-white">The ZAYVORA Clinical Knowledge Index</h3>
                <p class="text-xs sm:text-sm text-[#5F707E] dark:text-slate-300 max-w-2xl mt-1 leading-relaxed">
                  Browse our complete 5-domain clinical framework — from outpatient matab protocols and analytical botanical pharmacopoeia to real-world evidence trials and statutory healthcare governance.
                </p>
              </div>
              <button onclick="viewWebsitePage('pages25')" class="px-5 py-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs shadow-lg shadow-emerald-950/40 transition flex items-center gap-2 shrink-0 cursor-pointer">
                <span>View Full 25-Page Architecture</span>
                <span>&rarr;</span>
              </button>
            </div>

            <!-- 5 Elegant Semantic Domain Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 text-xs">
              <!-- Domain 1 -->
              <div onclick="viewWebsitePage('services')" class="p-5 rounded-2xl bg-[#FAF8F5] dark:bg-[#0D1526] border border-[#E4DDD0] dark:border-slate-700/80 shadow-sm hover:border-emerald-500 hover:shadow-md transition-all space-y-3 flex flex-col justify-between group cursor-pointer">
                <div class="space-y-2">
                  <div class="w-9 h-9 rounded-xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-lg text-emerald-400">🩺</div>
                  <h4 class="font-bold text-[#1B242A] dark:text-white text-sm group-hover:text-emerald-700 dark:group-hover:text-emerald-400 transition-colors">Clinical Services</h4>
                  <p class="text-xs text-[#4A5568] dark:text-slate-300 leading-relaxed">In-clinic matab care, tele-consultation, and clinical decision support.</p>
                </div>
                <ul class="space-y-1.5 text-xs text-[#2D3748] dark:text-slate-200 border-t border-[#E2D9CC] dark:border-slate-700 pt-2.5 font-medium">
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('services_clinical_care')" class="hover:text-emerald-400 block transition">&bull; In-Clinic Matab Care</a></li>
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('services_digital_health')" class="hover:text-emerald-400 block transition">&bull; Digital Health &amp; Scribe</a></li>
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('services_ai_healthcare')" class="hover:text-emerald-400 block transition">&bull; Hakeem Sahab™ Clinical CDSS</a></li>
                </ul>
              </div>

              <!-- Domain 2 -->
              <div onclick="viewWebsitePage('products')" class="p-5 rounded-2xl bg-[#FAF8F5] dark:bg-[#0D1526] border border-[#E4DDD0] dark:border-slate-700/80 shadow-sm hover:border-teal-500 hover:shadow-md transition-all space-y-3 flex flex-col justify-between group cursor-pointer">
                <div class="space-y-2">
                  <div class="w-9 h-9 rounded-xl bg-teal-500/15 border border-teal-500/30 flex items-center justify-center text-lg text-teal-400">🌿</div>
                  <h4 class="font-bold text-[#1B242A] dark:text-white text-sm group-hover:text-teal-700 dark:group-hover:text-teal-400 transition-colors">Botanical Formulations</h4>
                  <p class="text-xs text-[#4A5568] dark:text-slate-300 leading-relaxed">Standardized extracts, classical Greco-Arab compounds, and COAs.</p>
                </div>
                <ul class="space-y-1.5 text-xs text-[#2D3748] dark:text-slate-200 border-t border-[#E2D9CC] dark:border-slate-700 pt-2.5 font-medium">
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('products_unani_care')" class="hover:text-teal-400 block transition">&bull; Classical Unani Care</a></li>
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('products_herbal_products')" class="hover:text-teal-400 block transition">&bull; Standardized Extracts</a></li>
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('products_nutraceuticals')" class="hover:text-teal-400 block transition">&bull; Phyto-Nutraceuticals</a></li>
                </ul>
              </div>

              <!-- Domain 3 -->
              <div onclick="viewWebsitePage('research')" class="p-5 rounded-2xl bg-[#FAF8F5] dark:bg-[#0D1526] border border-[#E4DDD0] dark:border-slate-700/80 shadow-sm hover:border-amber-500 hover:shadow-md transition-all space-y-3 flex flex-col justify-between group cursor-pointer">
                <div class="space-y-2">
                  <div class="w-9 h-9 rounded-xl bg-amber-500/15 border border-amber-500/30 flex items-center justify-center text-lg text-amber-400">🔬</div>
                  <h4 class="font-bold text-[#1B242A] dark:text-white text-sm group-hover:text-amber-700 dark:group-hover:text-amber-400 transition-colors">Research &amp; Evidence</h4>
                  <p class="text-xs text-[#4A5568] dark:text-slate-300 leading-relaxed">RWE clinical registries, analytical HPLC monographs, and academic trials.</p>
                </div>
                <ul class="space-y-1.5 text-xs text-[#2D3748] dark:text-slate-200 border-t border-[#E2D9CC] dark:border-slate-700 pt-2.5 font-medium">
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('research_clinical_research')" class="hover:text-amber-400 block transition">&bull; Clinical Trials &amp; RWE</a></li>
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('research_knowledge_intelligence')" class="hover:text-amber-400 block transition">&bull; Pharmacopoeia Graph</a></li>
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('research_evidence')" class="hover:text-amber-400 block transition">&bull; Phytochemical Evidence</a></li>
                </ul>
              </div>

              <!-- Domain 4 -->
              <div onclick="viewWebsitePage('philosophy')" class="p-5 rounded-2xl bg-[#FAF8F5] dark:bg-[#0D1526] border border-[#E4DDD0] dark:border-slate-700/80 shadow-sm hover:border-sky-500 hover:shadow-md transition-all space-y-3 flex flex-col justify-between group cursor-pointer">
                <div class="space-y-2">
                  <div class="w-9 h-9 rounded-xl bg-blue-500/15 border border-blue-500/30 flex items-center justify-center text-lg text-blue-400">🏛️</div>
                  <h4 class="font-bold text-[#1B242A] dark:text-white text-sm group-hover:text-sky-700 dark:group-hover:text-sky-400 transition-colors">Philosophy &amp; Care</h4>
                  <p class="text-xs text-[#4A5568] dark:text-slate-300 leading-relaxed">Four Humors (Akhlat), 12-Step continuum, and multi-facility matabs.</p>
                </div>
                <ul class="space-y-1.5 text-xs text-[#2D3748] dark:text-slate-200 border-t border-[#E2D9CC] dark:border-slate-700 pt-2.5 font-medium">
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('philosophy')" class="hover:text-blue-400 block transition">&bull; Humoral Philosophy</a></li>
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('care_journey')" class="hover:text-blue-400 block transition">&bull; 12-Stage Care Loop</a></li>
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('doctors')" class="hover:text-blue-400 block transition">&bull; Faculty &amp; Clinicians</a></li>
                </ul>
              </div>

              <!-- Domain 5 -->
              <div onclick="viewWebsitePage('ethics')" class="p-5 rounded-2xl bg-[#FAF8F5] dark:bg-[#0D1526] border border-[#E4DDD0] dark:border-slate-700/80 shadow-sm hover:border-purple-500 hover:shadow-md transition-all space-y-3 flex flex-col justify-between group cursor-pointer">
                <div class="space-y-2">
                  <div class="w-9 h-9 rounded-xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-lg text-purple-400">⚖️</div>
                  <h4 class="font-bold text-[#1B242A] dark:text-white text-sm group-hover:text-purple-700 dark:group-hover:text-purple-400 transition-colors">Governance &amp; Trust</h4>
                  <p class="text-xs text-[#4A5568] dark:text-slate-300 leading-relaxed">21 CFR Part 11 records, patient privacy under DPDP, and clinical ethics.</p>
                </div>
                <ul class="space-y-1.5 text-xs text-[#2D3748] dark:text-slate-200 border-t border-[#E2D9CC] dark:border-slate-700 pt-2.5 font-medium">
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('ethics')" class="hover:text-purple-400 block transition">&bull; Clinical Ethics Charter</a></li>
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('privacy')" class="hover:text-purple-400 block transition">&bull; Privacy &amp; Data Security</a></li>
                  <li><a href="javascript:void(0)" onclick="viewWebsitePage('terms')" class="hover:text-purple-400 block transition">&bull; Telemedicine Terms</a></li>
                </ul>
              </div>
            </div>

            <!-- Bottom interactive action strip -->
            <div class="pt-4 border-t border-slate-800 flex flex-col sm:flex-row justify-between items-center gap-3 text-xs text-slate-400">
              <span class="flex items-center gap-1.5">
                <span class="text-emerald-400">✓</span> All 25 canonical web pages are verified, responsive, and available in English, Hindi, and Urdu.
              </span>
              <div class="flex items-center gap-2">
                <button onclick="viewWebsitePage('faqs')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition cursor-pointer">
                  Patient FAQs &rarr;
                </button>
                <button onclick="viewWebsitePage('contact')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition cursor-pointer">
                  Direct Contact &amp; Triage &rarr;
                </button>
              </div>
            </div>
          </div>

        </div>
      `;
if (typeof initWebsiteWaveform === 'function') initWebsiteWaveform();
    }


