def get_pharmacy_app_code():
    return '''    function renderPharmacyApp(container) {
      if (state.tab === 'dispensing' || !state.tab) {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">Botanical Dispensary & Dispensing Counter</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Chief Pharmacist: <span class="text-white font-medium">Zubair Ahmad</span> • Central Hospital FEFO Compound Dispensary</p>
              </div>
              <div class="flex items-center gap-2">
                <span class="px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-300 text-xs font-bold border border-emerald-500/40">✓ Barcode Scanning Ready</span>
              </div>
            </div>

            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 space-y-4">
              <div class="flex justify-between items-center border-b border-[var(--border)] pb-3">
                <div>
                  <span class="text-[10px] text-amber-400 font-bold uppercase tracking-wider block">Order Awaiting Dispensing</span>
                  <h3 class="text-base font-bold text-white mt-0.5">Prescription RX-2026-09-0814</h3>
                </div>
                <span class="badge-emerald text-xs px-2.5 py-1 rounded-full font-bold">21 CFR 11 Cryptographically Locked</span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                <div class="p-3.5 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span class="text-[var(--muted)] block">Patient:</span>
                  <strong class="text-white block mt-0.5">Hamza Farooqi (MRN-2026-0814)</strong>
                  <span class="text-[10px] text-[var(--muted)]">48M • Su-e-Mizaj Barid Balghami</span>
                </div>
                <div class="p-3.5 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span class="text-[var(--muted)] block">Prescribing Physician:</span>
                  <strong class="text-white block mt-0.5">Hakim Dr. Irfan Ashraf</strong>
                  <span class="text-[10px] text-emerald-400">CCIM / DMC-UN-88412</span>
                </div>
                <div class="p-3.5 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span class="text-[var(--muted)] block">Detox Safety Gate:</span>
                  <strong class="text-emerald-400 block mt-0.5">Schedule E(1) Mudabbar Certified</strong>
                  <span class="text-[10px] text-emerald-300 font-mono">BMR-2026-MUD-04 (Passed)</span>
                </div>
              </div>

              <div class="space-y-3">
                <h4 class="text-xs font-bold text-white uppercase tracking-wider">Compound Formulation Items (FEFO Allocation)</h4>
                <div class="space-y-2 text-xs">
                  <div class="p-3.5 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                    <div>
                      <strong class="text-white">ManiVital Pro (Vitality & Seminal Viscosity Formulation)</strong>
                      <div class="text-[11px] text-[var(--muted)] mt-0.5">5g twice daily with lukewarm milk • Qty: 200g Granules</div>
                    </div>
                    <div class="text-right">
                      <span class="text-xs font-mono text-emerald-400 font-bold block">Batch: BMR-2026-MVP-09</span>
                      <span class="text-[10px] text-slate-400">FEFO Expiry: Aug 2028</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="pt-3 border-t border-[var(--border)] flex flex-col sm:flex-row justify-between items-center gap-4">
                <div class="text-xs text-[var(--muted)]">
                  Dispensing will auto-decrement warehouse stock in Postgres & emit an ABDM M3 MedicationDispense event.
                </div>
                <button onclick="dispensePharmacyOrder()" class="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-lg transition">
                  ✓ Dispense & Deduct Stock
                </button>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'inventory') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">FEFO Botanical Warehouse Inventory</h2>
                <p class="text-xs text-[var(--muted)] mt-1">First-Expiry-First-Out automated stock allocation and real-time inventory ledger.</p>
              </div>
              <button onclick="showNotification('Warehouse stock audit refreshed.', 'info')" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-700">
                🔄 Refresh Inventory
              </button>
            </div>

            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-4">
              <div class="overflow-x-auto text-xs text-slate-300">
                <table class="w-full text-left">
                  <thead class="text-[10px] uppercase text-slate-400 bg-slate-900/50 border-b border-[var(--border)]">
                    <tr><th class="p-3">Item Name</th><th class="p-3">Batch</th><th class="p-3">Stock</th><th class="p-3">Expiry</th><th class="p-3">Storage Temp</th><th class="p-3 text-right">Action</th></tr>
                  </thead>
                  <tbody class="divide-y divide-[var(--border)]">
                    <tr>
                      <td class="p-3 font-bold text-white">ManiVital Pro (200g)</td>
                      <td class="p-3 font-mono text-emerald-400">BMR-2026-MVP-09</td>
                      <td class="p-3 font-mono font-bold text-white">412 Units</td>
                      <td class="p-3 font-mono text-slate-300">Aug 2028</td>
                      <td class="p-3 text-cyan-300">15 - 25°C</td>
                      <td class="p-3 text-right"><button onclick="openCoaModal('BMR-2026-MVP-09')" class="text-emerald-400 font-bold hover:underline">View COA ↗</button></td>
                    </tr>
                    <tr>
                      <td class="p-3 font-bold text-white">Qurs-e-Taqwiyat-e-Mani (60 Tab)</td>
                      <td class="p-3 font-mono text-emerald-400">BMR-2026-QTM-04</td>
                      <td class="p-3 font-mono font-bold text-white">280 Bottles</td>
                      <td class="p-3 font-mono text-slate-300">Jul 2028</td>
                      <td class="p-3 text-cyan-300">15 - 25°C</td>
                      <td class="p-3 text-right"><button onclick="openCoaModal('BMR-2026-MVP-09')" class="text-emerald-400 font-bold hover:underline">View COA ↗</button></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'detox') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Mudabbar Schedule E(1) Detoxification Gate</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Verification of botanical toxic alkaloid neutralization before dispensary release.</p>
              </div>
              <span class="badge-emerald text-xs px-3 py-1 rounded-full font-semibold">100% Detox Batches Cleared</span>
            </div>

            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-4 text-xs">
              <h3 class="text-sm font-bold text-white">Active Detoxification Log: Suranjan (*Colchicum autumnale*)</h3>
              <div class="space-y-2">
                <div class="flex justify-between p-3 rounded-lg bg-slate-900 border border-slate-800"><span>Process:</span><strong class="text-white">Boiling in Cow's Milk (*Tadbeer bi-Haleeb*)</strong></div>
                <div class="flex justify-between p-3 rounded-lg bg-slate-900 border border-slate-800"><span>Duration:</span><strong class="text-white">24 Hours continuous maceration</strong></div>
                <div class="flex justify-between p-3 rounded-lg bg-slate-900 border border-slate-800"><span>Colchicine Concentration:</span><strong class="text-emerald-400">Reduced to 0.18% (Safe Window)</strong></div>
                <div class="flex justify-between p-3 rounded-lg bg-slate-900 border border-slate-800"><span>Supervising Clinician:</span><strong class="text-white">Hakim Dr. Irfan Ashraf</strong></div>
              </div>
              <button onclick="approveDetoxStage(this)" class="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition">
                ✓ Approve & Sign Detox Clearance (21 CFR Part 11)
              </button>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'orders') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Dispensed Orders & Logistics Tracking</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Fulfilled pharmacy orders, dispatch timestamps, and cold-chain courier tracking.</p>
              </div>
              <button onclick="showNotification('Cold-chain telemetry stream online.', 'success')" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-700">
                🌡️ Check Cold Chain
              </button>
            </div>

            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3 text-xs text-slate-300">
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm block">Order #ORD-2026-9041 — Hamza Farooqi</strong>
                  <span class="text-[11px] text-slate-400">ManiVital Pro (200g) • Dispatched via Central Express</span>
                </div>
                <div class="text-right">
                  <span class="badge-emerald text-[9px] px-2 py-0.5 rounded font-bold block">In Transit (2-8°C OK)</span>
                  <span class="text-[10px] text-slate-400 font-mono">AWB: ZAY-9941-EXP</span>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }
    }'''

def get_research_app_code():
    return '''    function renderResearchApp(container) {
      if (state.tab === 'studies' || !state.tab) {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Clinical Research & Outcomes Platform</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Lead Investigator: <span class="text-white font-medium">Dr. K. Saxena, MD, PhD</span> • Protocol: ZAY-RCT-OSTEO-01</p>
              </div>
              <span class="badge-emerald text-xs px-3 py-1 rounded-full font-semibold">IRB Approved</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
                <span class="text-[var(--muted)] block">Enrolled Trial Cohort</span>
                <span class="text-2xl font-bold text-white">148 Subjects</span>
                <span class="text-[10px] text-emerald-400">100% Retained at Week 3</span>
              </div>
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
                <span class="text-[var(--muted)] block">Primary Clinical Endpoint</span>
                <span class="text-2xl font-bold text-emerald-400">-58% WOMAC</span>
                <span class="text-[10px] text-[var(--muted)]">Pain & Stiffness Reduction</span>
              </div>
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
                <span class="text-[var(--muted)] block">GCP Safety Compliance</span>
                <span class="text-2xl font-bold text-[#2DD4BF]">Zero SAEs</span>
                <span class="text-[10px] text-emerald-400">Audited by DSMB Committee</span>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'outcomes') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Patient-Reported Outcomes (PROMs)</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Longitudinal tracking of WOMAC and Visual Analog Scale pain attenuation curves.</p>
              </div>
            </div>
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3 text-xs">
              <h3 class="text-sm font-bold text-white">Cohort Aggregate Analysis</h3>
              <p class="text-slate-300">Mean WOMAC total score dropped from 64.2 at baseline to 26.8 at Week 4 across 148 trial participants.</p>
              <div class="w-full bg-slate-900 h-3 rounded-full overflow-hidden mt-2"><div class="bg-emerald-500 h-full rounded-full" style="width: 72%"></div></div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'adverse') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">ICH E2B Pharmacovigilance Ledger</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Automated adverse event reporting, severity scoring, and DSMB committee oversight.</p>
              </div>
              <span class="badge-emerald text-xs px-3 py-1 rounded-full font-semibold">0 Critical Adverse Events</span>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] text-xs text-slate-300 space-y-2">
              <p>No unexpected serious adverse reactions (SUSAR) detected. Mild transient dyspepsia reported in 2 subjects, resolved spontaneously without dose reduction.</p>
            </div>
          </div>
        `;
        return;
      }
    }'''

def get_admin_app_code():
    return '''    function renderAdminApp(container) {
      if (state.tab === 'organizations' || !state.tab) {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Hospital Facilities & Institutional Centers</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Multi-facility clinical seats, hospital tiers, and license quotas.</p>
              </div>
              <span class="badge-emerald text-xs px-3 py-1 rounded-full font-semibold">4 Facilities Active</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span class="font-bold text-white text-sm block">Central Hospital, New Delhi</span>
                <span class="text-emerald-400 block font-mono">24 Doctor Seats • Enterprise Flagship</span>
                <span class="text-[10px] text-slate-400">ABDM HFR: IN0710008412 • 21 CFR Part 11 Enabled</span>
              </div>
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span class="font-bold text-white text-sm block">ZAYVORA Matab™, Hyderabad</span>
                <span class="text-emerald-400 block font-mono">12 Doctor Seats • Regional Matab</span>
                <span class="text-[10px] text-slate-400">Charminar Clinical Wing • Active OPD</span>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'users') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">User Permissions & RBAC Matrix</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Role-based access control, biometric MFA tokens, and privilege segregation.</p>
              </div>
              <button onclick="showNotification('User directory synchronized.', 'info')" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-700">
                Sync RBAC
              </button>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] text-xs text-slate-300 space-y-2">
              <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Hakim Dr. Irfan Ashraf:</span><strong class="text-emerald-400">Senior Clinician (21 CFR Signer)</strong></div>
              <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Zubair Ahmad:</span><strong class="text-cyan-300">Chief Pharmacist (Dispensary Dispense)</strong></div>
              <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Sana Khan:</span><strong class="text-amber-300">Receptionist (OPD Queue Intake)</strong></div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'audit') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Merkle Cryptographic Audit Trail</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Immutable SHA-256 chained transaction logs satisfying 21 CFR Part 11 requirements.</p>
              </div>
              <span class="badge-emerald text-xs px-3 py-1 rounded-full font-semibold">Ledger Validated</span>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] text-xs space-y-2 font-mono text-slate-300">
              <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">Block #9102: Prescription RX-0814 signed by Dr. Irfan Ashraf (SHA256: 8f2c...41b0)</div>
              <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">Block #9101: Mudabbar batch BMR-MUD-04 released by Quality Assurance (SHA256: 7d1a...09ac)</div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'safety') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Clinical Safety Firewall Rules</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Schedule E(1) posology limits, contraindication interlock, and non-delegable clinician barriers.</p>
              </div>
              <span class="badge-emerald text-xs px-3 py-1 rounded-full font-semibold">14 Active Interceptors</span>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] text-xs text-slate-300 space-y-2">
              <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">RULE-01: Zero autonomous AI prescription issuance (Enforced: STRICT)</div>
              <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">RULE-02: Colchicum autumnale max daily dose ceiling: 2.0g (Enforced: STRICT)</div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'engines') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Platform Microservices Health</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Identity, Clinical, Knowledge, Therapeutic, and AI RPC engines status.</p>
              </div>
              <span class="badge-emerald text-xs px-3 py-1 rounded-full font-semibold">All 6 Services Healthy</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-xs">
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800"><strong class="text-white block">Identity Service</strong><span class="text-emerald-400 font-mono">Status: Healthy (18ms)</span></div>
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800"><strong class="text-white block">Clinical Engine</strong><span class="text-emerald-400 font-mono">Status: Healthy (24ms)</span></div>
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800"><strong class="text-white block">Knowledge Graph</strong><span class="text-emerald-400 font-mono">Status: Healthy (31ms)</span></div>
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800"><strong class="text-white block">Therapeutic OS</strong><span class="text-emerald-400 font-mono">Status: Healthy (19ms)</span></div>
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800"><strong class="text-white block">Hakeem AI Copilot</strong><span class="text-emerald-400 font-mono">Status: Healthy (82ms)</span></div>
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800"><strong class="text-white block">API Gateway</strong><span class="text-emerald-400 font-mono">Status: Healthy (9ms)</span></div>
            </div>
          </div>
        `;
        return;
      }
    }'''

def get_enterprise_app_code():
    return '''    function renderEnterpriseApp(container) {
      container.innerHTML = `
        <div class="space-y-6">
          <div class="bg-gradient-to-r from-emerald-900/30 to-teal-900/30 border border-emerald-500/30 rounded-2xl p-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">ZAYVORA Health OS™ v2.0 Enterprise</span>
                <h2 class="text-2xl font-bold text-white mt-1">Enterprise Multi-Facility Operations</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Governing 14 Integrative Hospitals & Matabs across 4 National Clusters.</p>
              </div>
              <div class="flex gap-2">
                <span class="px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-300 text-xs font-semibold border border-emerald-500/40">✓ All Facilities Compliant</span>
              </div>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
            <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]"><span class="text-slate-400 block">Total Facilities</span><strong class="text-2xl font-bold text-white mt-1 block">14 Centers</strong></div>
            <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]"><span class="text-slate-400 block">Active Clinicians</span><strong class="text-2xl font-bold text-emerald-400 mt-1 block">48 Tabeebs</strong></div>
            <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]"><span class="text-slate-400 block">Monthly Consultations</span><strong class="text-2xl font-bold text-white mt-1 block">3,240 Visits</strong></div>
            <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]"><span class="text-slate-400 block">Universal Helpline</span><strong class="text-emerald-400 font-mono mt-1 block">+91 97738 82657</strong></div>
          </div>
        </div>
      `;
    }'''

def get_manufacturing_app_code():
    return '''    function renderManufacturingApp(container) {
      container.innerHTML = `
        <div class="space-y-6">
          <div class="bg-gradient-to-r from-amber-900/30 to-slate-900/30 border border-amber-500/30 rounded-2xl p-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">GMP / WHO-GMP & Schedule T Facility</span>
                <h2 class="text-2xl font-bold text-white mt-1">Botanical Manufacturing & QA/QC Laboratory</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Batch Manufacturing Records (BMR), Mudabbar Detoxification & Heavy Metal Spectrometry.</p>
              </div>
              <span class="px-3 py-1.5 rounded-xl bg-amber-500/20 text-amber-300 text-xs font-semibold border border-amber-500/40">Schedule E(1) Verification Locked</span>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
              <strong class="text-white text-base block">Batch: BMR-2026-MVP-09</strong>
              <span class="text-slate-300 block">ManiVital Pro Granules (200kg Run)</span>
              <span class="badge-emerald text-[9px] px-2 py-0.5 rounded font-bold">Passed Quality Release</span>
              <button onclick="openCoaModal('BMR-2026-MVP-09')" class="w-full mt-2 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl">View Certificate of Analysis 📜</button>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
              <strong class="text-white text-base block">Batch: BMR-2026-MUD-04</strong>
              <span class="text-slate-300 block">Suranjan Detoxification Run (50kg)</span>
              <span class="badge-blue text-[9px] px-2 py-0.5 rounded font-bold">Detox Completed</span>
              <button onclick="approveDetoxStage(this)" class="w-full mt-2 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-xl border border-slate-700">Audit Detox Record 🛡️</button>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-2">
              <strong class="text-white text-base block">HPLC Spectrometry QA</strong>
              <span class="text-slate-300 block">Active Withaferin-A & Colchicine Assay</span>
              <span class="badge-emerald text-[9px] px-2 py-0.5 rounded font-bold">99.2% Chromatographic Peak</span>
              <button onclick="queueSpectrometry(this)" class="w-full mt-2 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-300 font-bold rounded-xl border border-slate-700">Queue Spectrometry 🧪</button>
            </div>
          </div>
        </div>
      `;
    }'''

def get_herbals_app_code():
    return '''    function renderHerbalsApp(container) {
      const totalAmount = herbalsCart.reduce((sum, item) => sum + item.price, 0);

      container.innerHTML = `
        <div class="space-y-6">
          <div class="bg-gradient-to-r from-teal-900/30 to-emerald-900/30 border border-teal-500/30 rounded-2xl p-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <span class="text-xs font-bold text-teal-400 uppercase tracking-wider">ZAYVORA Herbals™ Direct Store</span>
                <h2 class="text-2xl font-bold text-white mt-1">10 Clinical Botanical Formulations</h2>
                <p class="text-xs text-[var(--muted)] mt-1">GMP-certified, heavy-metal tested, standardized botanicals delivered with FEFO batch transparency.</p>
              </div>
              <div class="flex items-center gap-3">
                <span class="px-3 py-1.5 rounded-xl bg-teal-500/20 text-teal-300 text-xs font-bold border border-teal-500/40">
                  🛒 Cart (${herbalsCart.length} items — ₹${totalAmount.toLocaleString('en-IN')})
                </span>
                ${herbalsCart.length > 0 ? `
                  <button onclick="checkoutHerbalsCart()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow">
                    Checkout Now →
                  </button>
                ` : ''}
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            ${herbalsProducts.map(p => `
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
                    + Add to Cart
                  </button>
                  <button onclick="openCoaModal('BMR-2026-MVP-09')" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs rounded-xl border border-slate-700 transition">
                    📑 COA
                  </button>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }'''

def get_mobile_app_code():
    return '''    let mobileActiveScreen = 'home';
    let isPlayingAudio = false;

    function setMobileScreen(screen) {
      mobileActiveScreen = screen;
      renderMobileApp(document.getElementById('workspace-container'));
    }

    function renderMobileApp(container) {
      const audioTexts = {
        ur: "ایک چمچ صبح اور شام کھانے کے بعد نیم گرم دودھ کے ساتھ لیں۔ ٹھنڈے مشروبات اور کھٹی چیزوں سے پرہیز کریں۔",
        hi: "एक चम्मच सुबह और शाम खाना खाने کے बाद गुनगुने दूध के साथ लें। ठंडी चीजों और खट्टी चीजों से परहेज करें।",
        en: "Take one teaspoon twice daily after breakfast and dinner with lukewarm milk. Avoid cold drinks."
      };

      container.innerHTML = `
        <div class="flex flex-col lg:flex-row gap-8 items-center justify-center py-4">
          <!-- Mobile Device Frame -->
          <div class="w-[360px] h-[720px] bg-[#0A0F1D] border-4 border-slate-700 rounded-[40px] shadow-2xl overflow-hidden flex flex-col relative">
            <!-- Mobile Notch / Top Status -->
            <div class="bg-[#0F172A] px-5 py-3 flex items-center justify-between border-b border-slate-800 text-[11px]">
              <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span class="font-bold text-white tracking-wider">ZAYVORA Mobile</span>
              </div>
              <span class="font-mono text-emerald-400 font-bold">09:41 AM</span>
            </div>

            <!-- Mobile Screen Body -->
            <div class="flex-1 p-4 overflow-y-auto space-y-4">
              ${mobileActiveScreen === 'home' ? `
                <div class="space-y-4">
                  <div class="bg-gradient-to-br from-emerald-800/40 to-slate-900 p-4 rounded-2xl border border-emerald-500/30">
                    <span class="text-[10px] text-emerald-400 font-mono block">Hamza Farooqi (MRN-8819)</span>
                    <h3 class="font-bold text-white text-base mt-1">Meezan-e-Sehat: 84/100</h3>
                    <p class="text-xs text-slate-300 mt-1">Su-e-Mizaj Barid Balghami (Tahleel Phase)</p>
                  </div>

                  <div class="grid grid-cols-2 gap-2 text-xs">
                    <button onclick="setMobileScreen('rx')" class="p-3 bg-[#1E293B] border border-slate-700 rounded-xl text-left hover:border-emerald-500">
                      <span class="text-base block">💊</span>
                      <strong class="text-white block mt-1">My Medicines</strong>
                      <span class="text-[10px] text-slate-400">Voice Posology</span>
                    </button>
                    <button onclick="setMobileScreen('lifestyle')" class="p-3 bg-[#1E293B] border border-slate-700 rounded-xl text-left hover:border-emerald-500">
                      <span class="text-base block">🌿</span>
                      <strong class="text-white block mt-1">6 Essentials</strong>
                      <span class="text-[10px] text-slate-400">Asbab-e-Sittah</span>
                    </button>
                    <button onclick="setMobileScreen('consult')" class="p-3 bg-[#1E293B] border border-slate-700 rounded-xl text-left hover:border-emerald-500">
                      <span class="text-base block">🩺</span>
                      <strong class="text-white block mt-1">Tele-OPD</strong>
                      <span class="text-[10px] text-slate-400">Join Video Room</span>
                    </button>
                    <button onclick="setMobileScreen('doctor')" class="p-3 bg-[#1E293B] border border-slate-700 rounded-xl text-left hover:border-emerald-500">
                      <span class="text-base block">👨‍⚕️</span>
                      <strong class="text-white block mt-1">Dr. Companion</strong>
                      <span class="text-[10px] text-slate-400">21 CFR Sign-off</span>
                    </button>
                  </div>
                </div>
              ` : mobileActiveScreen === 'rx' ? `
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <button onclick="setMobileScreen('home')" class="text-xs text-emerald-400 font-bold">← Back</button>
                    <span class="text-xs font-bold text-white">Active Prescriptions</span>
                  </div>
                  <div class="bg-[#1E293B] p-3 rounded-xl border border-slate-700 space-y-2 text-xs">
                    <strong class="text-white block">ManiVital Pro Granules</strong>
                    <p class="text-slate-300 text-[11px]">5g twice daily with lukewarm milk.</p>
                    <button onclick="handleRequestMobileRefill(this)" class="w-full py-1.5 border border-emerald-500/50 text-emerald-400 rounded-lg text-[10px] font-bold">
                      Request Dispensary Refill
                    </button>
                  </div>
                </div>
              ` : mobileActiveScreen === 'lifestyle' ? `
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <button onclick="setMobileScreen('home')" class="text-xs text-emerald-400 font-bold">← Back</button>
                    <span class="text-xs font-bold text-white">Asbab-e-Sittah</span>
                  </div>
                  <div class="bg-[#1E293B] p-3 rounded-xl border border-slate-700 space-y-1 text-[11px]">
                    <span class="font-bold text-emerald-400 block">Sleep & Rest Adherence</span>
                    <span class="text-slate-300">7.5 hours continuous restorative sleep</span>
                  </div>
                  <button onclick="handleSaveMobileAdherence(this)" class="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl">
                    ✓ Save Today's Adherence
                  </button>
                </div>
              ` : mobileActiveScreen === 'consult' ? `
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <button onclick="setMobileScreen('home')" class="text-xs text-emerald-400 font-bold">← Back</button>
                    <span class="text-xs font-bold text-white">Integrative Tele-OPD</span>
                  </div>
                  <div class="bg-[#1E293B] p-3 rounded-xl border border-slate-700 space-y-1 text-xs">
                    <span class="text-white font-bold block">Hakim Dr. Tariq Mansoor</span>
                    <span class="text-emerald-400">Central Hospital Suite</span>
                  </div>
                  <button onclick="handleConfirmMobileVideo(this)" class="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl">
                    Confirm Video Room Appointment
                  </button>
                </div>
              ` : `
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <button onclick="setMobileScreen('home')" class="text-xs text-emerald-400 font-bold">← Back</button>
                    <span class="text-xs font-bold text-white">Doctor Mobile Triage</span>
                  </div>
                  <div class="bg-[#1E293B] p-3 rounded-xl border border-slate-700 text-[11px] space-y-2">
                    <span class="font-bold text-white block">Mohammad Tariq (MRN-8819)</span>
                    <button onclick="handleSignLockMobileRx(this)" class="w-full py-1.5 bg-emerald-600 text-white font-bold text-[10px] rounded-lg">
                      🔒 Sign & Lock Prescription
                    </button>
                  </div>
                </div>
              `}
            </div>

            <!-- Mobile Bottom Bar -->
            <div class="bg-[#0F172A] border-t border-slate-800 p-2 flex justify-around text-[10px]">
              <button onclick="setMobileScreen('home')" class="${mobileActiveScreen === 'home' ? 'text-emerald-400 font-bold' : 'text-slate-400'}">Home</button>
              <button onclick="setMobileScreen('rx')" class="${mobileActiveScreen === 'rx' ? 'text-emerald-400 font-bold' : 'text-slate-400'}">Rx</button>
              <button onclick="setMobileScreen('lifestyle')" class="${mobileActiveScreen === 'lifestyle' ? 'text-emerald-400 font-bold' : 'text-slate-400'}">Lifestyle</button>
              <button onclick="setMobileScreen('consult')" class="${mobileActiveScreen === 'consult' ? 'text-emerald-400 font-bold' : 'text-slate-400'}">Consult</button>
              <button onclick="setMobileScreen('doctor')" class="${mobileActiveScreen === 'doctor' ? 'text-emerald-400 font-bold' : 'text-slate-400'}">Doctor</button>
            </div>
          </div>
        </div>
      `;
    }'''

def get_hardware_app_code():
    return '''    function renderHardwareApp(container) {
      container.innerHTML = `
        <div class="space-y-6">
          <div class="bg-gradient-to-r from-cyan-900/30 to-blue-900/30 border border-cyan-500/30 rounded-2xl p-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider">ZAYVORA Health OS™ Hardware Integration Architecture</span>
                <h2 class="text-2xl font-bold text-white mt-1">Hardware Integration Architecture & Sensory Instrumentation Lab</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Digital signal processing specifications integrating classical Unani diagnostics with clinical sensors. (Architecture Spec-Ready • Awaiting verified physical device pairing)</p>
              </div>
              <div class="flex flex-wrap gap-2">
                <span class="px-3 py-1.5 rounded-xl bg-slate-800/80 text-slate-300 text-xs font-semibold border border-slate-700">Hardware Integration Architecture</span>
                <span class="px-3 py-1.5 rounded-xl bg-slate-900 text-slate-400 text-xs font-mono font-semibold border border-slate-700">Connected Devices: 0</span>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-[var(--card)] rounded-2xl border border-[var(--border)] p-6 space-y-4">
              <h3 class="font-bold text-white text-base">10-Ajnas Nabz (Arterial Pulse) Sensor</h3>
              <canvas id="nabz-canvas" width="400" height="120" class="w-full bg-[#050B14] rounded-xl border border-cyan-500/30"></canvas>
              <button onclick="triggerNabzPulseTest()" class="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow">
                ⚡ Calibrate Pulse Sensor (100 Hz PPG)
              </button>
            </div>

            <div class="bg-[var(--card)] rounded-2xl border border-[var(--border)] p-6 space-y-4">
              <h3 class="font-bold text-white text-base">Multispectral Lisan (Tongue) Camera</h3>
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 text-xs space-y-1">
                <div>Optical Wavelength: <strong class="text-white font-mono">415 - 850 nm</strong></div>
                <div>Saburra Coating Thickness: <strong class="text-emerald-400 font-mono">0.42 mm</strong></div>
              </div>
              <button onclick="handleCaptureTongueSpectrum(this)" class="w-full py-2.5 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-700">
                📸 Capture Multispectral Spectrum
              </button>
            </div>
          </div>
        </div>
      `;
      setTimeout(initNabzPulseCanvas, 50);
    }'''
