def get_clinic_app_code():
    return '''    function renderClinicApp(container) {
      if (state.tab === 'overview' || !state.tab) {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">Clinic Operations & Reception Overview</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Receptionist: <span class="text-white font-medium">Sana Khan</span> • Central Integrative OPD & Diagnostic Wing</p>
              </div>
              <div class="flex items-center gap-2">
                <button onclick="openAddPatientModal()" class="px-4 py-2 rounded-xl bg-emerald-600 text-white text-xs font-semibold hover:bg-emerald-500 shadow">
                  + Register Walk-In Patient
                </button>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]">
                <span class="text-[var(--muted)] block">Today's Total Check-Ins</span>
                <span class="text-2xl font-bold text-white mt-1 block">18</span>
                <span class="text-[10px] text-emerald-400">14 Completed • 4 In-Waiting</span>
              </div>
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]">
                <span class="text-[var(--muted)] block">Active Consultation Rooms</span>
                <span class="text-2xl font-bold text-white mt-1 block">3 / 4</span>
                <span class="text-[10px] text-blue-400">Rooms 201, 202, 204 Occupied</span>
              </div>
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]">
                <span class="text-[var(--muted)] block">Today's Revenue Collected</span>
                <span class="text-2xl font-bold text-emerald-400 mt-1 block">₹ 14,250</span>
                <span class="text-[10px] text-[var(--muted)]">100% Settled via Gateway</span>
              </div>
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]">
                <span class="text-[var(--muted)] block">Average Wait Time</span>
                <span class="text-2xl font-bold text-amber-300 mt-1 block">12 Mins</span>
                <span class="text-[10px] text-emerald-400">-4 mins from target</span>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3">
                <div class="flex justify-between items-center border-b border-[var(--border)] pb-2">
                  <h3 class="text-sm font-bold text-white">Live OPD Room Allocation</h3>
                  <button onclick="switchTab('queue')" class="text-xs text-emerald-400 hover:underline font-bold">Open Queue Board →</button>
                </div>
                <div class="space-y-2 text-xs">
                  <div class="flex justify-between items-center p-3 rounded-xl bg-slate-900 border border-slate-800">
                    <div>
                      <span class="font-bold text-white block">Room 201 • General Integrative OPD</span>
                      <span class="text-[10px] text-slate-400">Attending: Dr. Aisha Siddiqui</span>
                    </div>
                    <span class="badge-emerald text-[9px] px-2 py-0.5 rounded font-bold">Consulting (Token #A-12)</span>
                  </div>
                  <div class="flex justify-between items-center p-3 rounded-xl bg-slate-900 border border-slate-800">
                    <div>
                      <span class="font-bold text-white block">Room 204 • Senior Rheumatology Suite</span>
                      <span class="text-[10px] text-slate-400">Attending: Dr. Irfan Ashraf</span>
                    </div>
                    <span class="badge-blue text-[9px] px-2 py-0.5 rounded font-bold">Calling Next (Token #A-14)</span>
                  </div>
                </div>
              </div>

              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3">
                <div class="flex justify-between items-center border-b border-[var(--border)] pb-2">
                  <h3 class="text-sm font-bold text-white">Emergency Casualty Status</h3>
                  <span class="badge-emerald text-[9px] px-2 py-0.5 rounded font-bold">Casualty Bed Ready</span>
                </div>
                <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs space-y-1.5">
                  <div class="flex justify-between"><span>24/7 Helpline:</span><strong class="text-emerald-400 font-mono">+91 97738 82657</strong></div>
                  <div class="flex justify-between"><span>On-Call Tabeeb:</span><strong class="text-white">Hakim Syed M. Akhtar</strong></div>
                  <div class="flex justify-between"><span>ABDM Gateway Sync:</span><strong class="text-emerald-400">Connected (M1, M2, M3)</strong></div>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'appointments') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">OPD Central Appointment Ledger</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Multi-physician schedule, slot allocation, and booking status.</p>
              </div>
              <button onclick="openAddPatientModal()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow">
                + Register Walk-In
              </button>
            </div>

            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-4">
              <div class="overflow-x-auto">
                <table class="w-full text-xs text-left">
                  <thead class="text-[10px] uppercase text-slate-400 bg-slate-900/50 border-b border-[var(--border)]">
                    <tr>
                      <th class="p-3">Time</th>
                      <th class="p-3">Patient Name</th>
                      <th class="p-3">MRN</th>
                      <th class="p-3">Attending Doctor</th>
                      <th class="p-3">Room</th>
                      <th class="p-3">Status</th>
                      <th class="p-3 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-[var(--border)] text-slate-300">
                    <tr>
                      <td class="p-3 font-mono font-bold text-white">10:30 AM</td>
                      <td class="p-3 font-bold text-white">Hamza Farooqi</td>
                      <td class="p-3 font-mono text-[11px]">MRN-2026-0814</td>
                      <td class="p-3">Dr. Irfan Ashraf</td>
                      <td class="p-3">Room 204</td>
                      <td class="p-3"><span class="badge-blue text-[9px] px-2 py-0.5 rounded font-bold">Checked In</span></td>
                      <td class="p-3 text-right"><button onclick="handleNotifyPatientAppointment(this)" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-emerald-400 font-bold rounded-lg text-xs">Notify SMS</button></td>
                    </tr>
                    <tr>
                      <td class="p-3 font-mono font-bold text-white">11:15 AM</td>
                      <td class="p-3 font-bold text-white">Bilal Ahmad</td>
                      <td class="p-3 font-mono text-[11px]">MRN-2026-0744</td>
                      <td class="p-3">Dr. Irfan Ashraf</td>
                      <td class="p-3">Room 204</td>
                      <td class="p-3"><span class="badge-emerald text-[9px] px-2 py-0.5 rounded font-bold">Confirmed</span></td>
                      <td class="p-3 text-right"><button onclick="handleNotifyPatientAppointment(this)" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-emerald-400 font-bold rounded-lg text-xs">Notify SMS</button></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'patients') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Clinic Patient Census & ABDM Register</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Institutional demographic records and national health locker linkage.</p>
              </div>
              <button onclick="openAddPatientModal()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow">
                + Register New Patient
              </button>
            </div>

            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-4">
              <input type="text" placeholder="Search census by name, MRN, mobile or ABHA..." class="w-full px-4 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-emerald-500">
              <div class="overflow-x-auto text-xs text-slate-300">
                <table class="w-full text-left">
                  <thead class="text-[10px] uppercase text-slate-400 bg-slate-900/50 border-b border-[var(--border)]">
                    <tr><th class="p-3">MRN</th><th class="p-3">Name</th><th class="p-3">Phone</th><th class="p-3">ABHA Address</th><th class="p-3">Status</th></tr>
                  </thead>
                  <tbody class="divide-y divide-[var(--border)]">
                    <tr><td class="p-3 font-mono font-bold text-emerald-400">MRN-2026-0814</td><td class="p-3 font-bold text-white">Hamza Farooqi</td><td class="p-3 font-mono">+91 97738 82657</td><td class="p-3 font-mono text-emerald-400">hamza@abdm</td><td class="p-3"><span class="badge-emerald text-[9px] px-2 py-0.5 rounded">Active In-Care</span></td></tr>
                    <tr><td class="p-3 font-mono font-bold text-emerald-400">MRN-2026-0744</td><td class="p-3 font-bold text-white">Bilal Ahmad</td><td class="p-3 font-mono">+91 97738 82657</td><td class="p-3 font-mono text-emerald-400">bilal@abdm</td><td class="p-3"><span class="badge-emerald text-[9px] px-2 py-0.5 rounded">Active In-Care</span></td></tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'queue') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">Live OPD Token Queue Manager</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Real-time room allocation, token progression, and waiting lobby announcements.</p>
              </div>
              <button onclick="callNextPatientQueue()" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition">
                🔔 Call Next Patient (Advance Token)
              </button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="md:col-span-2 bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-4">
                <h3 class="text-sm font-bold text-white">Active Queue Tokens</h3>
                <div class="space-y-2 text-xs">
                  ${queueTokens.map((t, idx) => `
                    <div class="p-4 rounded-xl ${idx === currentQueueTokenIndex ? 'bg-emerald-500/10 border-2 border-emerald-400' : 'bg-slate-900 border border-slate-800'} flex justify-between items-center">
                      <div>
                        <div class="flex items-center gap-2">
                          <span class="font-mono text-base font-extrabold ${idx === currentQueueTokenIndex ? 'text-emerald-400' : 'text-white'}">Token #${t.token}</span>
                          <span class="font-bold text-white">${t.patient}</span>
                        </div>
                        <span class="text-[11px] text-slate-400">Assigned: Room ${t.room} (${t.dr})</span>
                      </div>
                      <span class="${idx === currentQueueTokenIndex ? 'badge-emerald' : 'badge-blue'} text-[10px] px-2.5 py-1 rounded font-bold">${t.status}</span>
                    </div>
                  `).join('')}
                </div>
              </div>

              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3 text-xs">
                <h3 class="text-sm font-bold text-white">Lobby Display Status</h3>
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2 text-center">
                  <span class="text-slate-400 block text-[10px] uppercase tracking-wider">Now Serving</span>
                  <span class="text-4xl font-extrabold text-emerald-400 font-mono block">Token #${queueTokens[currentQueueTokenIndex].token}</span>
                  <span class="text-sm font-bold text-white block">${queueTokens[currentQueueTokenIndex].patient}</span>
                  <span class="text-xs text-cyan-300 block">Proceed to Room ${queueTokens[currentQueueTokenIndex].room}</span>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'doctors') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Hospital Medical Faculty & Duty Roster</h2>
                <p class="text-xs text-[var(--muted)] mt-1">On-duty Senior Tabeebs, OPD timings, and consultation room allocations.</p>
              </div>
              <span class="badge-emerald text-xs px-3 py-1 rounded-full font-semibold">3 Doctors On Duty</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <span class="text-[10px] text-emerald-400 font-bold uppercase">Room 204 • On Duty</span>
                <h4 class="font-bold text-white text-base">Hakim Dr. Irfan Ashraf</h4>
                <p class="text-slate-300">BUMS, MD (Unani Clinical Medicine)</p>
                <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 space-y-1">
                  <div>Shift: <strong class="text-white">09:00 AM – 06:00 PM</strong></div>
                  <div>OPD: <strong class="text-emerald-400">Active (4 in Queue)</strong></div>
                </div>
              </div>
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <span class="text-[10px] text-emerald-400 font-bold uppercase">Room 201 • On Duty</span>
                <h4 class="font-bold text-white text-base">Dr. Aisha Siddiqui</h4>
                <p class="text-slate-300">BUMS, MD, Fellowship in Gynecology</p>
                <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 space-y-1">
                  <div>Shift: <strong class="text-white">09:00 AM – 05:00 PM</strong></div>
                  <div>OPD: <strong class="text-emerald-400">Active (2 in Queue)</strong></div>
                </div>
              </div>
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3">
                <span class="text-[10px] text-emerald-400 font-bold uppercase">Room 202 • On Duty</span>
                <h4 class="font-bold text-white text-base">Hakim Syed M. Akhtar</h4>
                <p class="text-slate-300">BUMS, Senior Regimenal Specialist</p>
                <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 space-y-1">
                  <div>Shift: <strong class="text-white">10:00 AM – 07:00 PM</strong></div>
                  <div>OPD: <strong class="text-emerald-400">Active (Hijama Wing)</strong></div>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'billing') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">OPD Cashier & Billing Desk</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Consultation fee collections, digital receipt generation, and UPI settlement ledger.</p>
              </div>
              <button onclick="showNotification('Daily revenue settlement batch generated.', 'success')" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow">
                Generate Daily Settlement
              </button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]">
                <span class="text-slate-400 block">Today's Collections</span>
                <span class="text-2xl font-bold text-emerald-400 font-mono mt-1 block">₹ 14,250</span>
                <span class="text-[10px] text-slate-400">18 Invoices Paid</span>
              </div>
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]">
                <span class="text-slate-400 block">UPI / Card Ratio</span>
                <span class="text-2xl font-bold text-white font-mono mt-1 block">84% Digital</span>
                <span class="text-[10px] text-emerald-400">Direct Gateway Settle</span>
              </div>
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)]">
                <span class="text-slate-400 block">Dispensary Sales</span>
                <span class="text-2xl font-bold text-cyan-300 font-mono mt-1 block">₹ 9,800</span>
                <span class="text-[10px] text-slate-400">FEFO Dispensary counter</span>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'settings') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Clinic Configuration & Operational Parameters</h2>
                <p class="text-xs text-[var(--muted)] mt-1">OPD hours, casualty contacts, and ABDM facility credentials.</p>
              </div>
              <button onclick="showNotification('Clinic settings updated.', 'success')" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow">
                Save Settings
              </button>
            </div>

            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3 text-xs">
              <div class="flex justify-between p-3 rounded-lg bg-slate-900 border border-slate-800"><span>Facility Name:</span><strong class="text-white">ZAYVORA Healthcare System - Central Hospital</strong></div>
              <div class="flex justify-between p-3 rounded-lg bg-slate-900 border border-slate-800"><span>Universal Helpline:</span><strong class="text-emerald-400 font-mono">+91 97738 82657</strong></div>
              <div class="flex justify-between p-3 rounded-lg bg-slate-900 border border-slate-800"><span>Location:</span><strong class="text-white">New Delhi Institutional Complex</strong></div>
              <div class="flex justify-between p-3 rounded-lg bg-slate-900 border border-slate-800"><span>ABDM HFR Facility ID:</span><strong class="text-emerald-400 font-mono">IN0710008412</strong></div>
            </div>
          </div>
        `;
        return;
      }
    }'''
