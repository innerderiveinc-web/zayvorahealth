def get_doctor_app_code():
    return '''    function renderDoctorApp(container) {
      if (state.tab === 'today') {
        container.innerHTML = `
          <div class="space-y-8 pb-10">
            <!-- SECTION 3: Welcome Section & Quick Actions -->
            <div class="bg-gradient-to-r from-[#1E293B] via-[var(--card)] to-[#0F172A] border border-[var(--border)] rounded-3xl p-6 shadow-xl space-y-5">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-[var(--border)] pb-4">
                <div>
                  <div class="flex items-center gap-2">
                    <span class="text-2xl">☀️</span>
                    <h2 class="text-2xl font-extrabold text-white">Good Morning, Dr. Irfan</h2>
                    <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-bold border border-emerald-500/30">Clinic Open</span>
                  </div>
                  <p class="text-xs sm:text-sm text-[var(--muted)] mt-1">Here is your clinical and operational overview for today.</p>
                </div>
                <div class="flex flex-wrap items-center gap-3 text-xs">
                  <div class="px-3 py-1.5 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                    <span class="text-[10px] text-[var(--muted)] block">Date</span>
                    <strong class="text-white font-mono">Sunday, 13 Sep 2026</strong>
                  </div>
                  <div class="px-3 py-1.5 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                    <span class="text-[10px] text-[var(--muted)] block">Clinic Timing</span>
                    <strong class="text-[#2DD4BF] font-mono">09:00 AM – 06:00 PM</strong>
                  </div>
                  <div class="px-3 py-1.5 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                    <span class="text-[10px] text-[var(--muted)] block">Current Shift</span>
                    <strong class="text-amber-300 font-mono">Morning OPD (General)</strong>
                  </div>
                </div>
              </div>

              <!-- Metrics Grid -->
              <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
                <div class="p-3 rounded-2xl bg-[var(--background)] border border-[var(--border)]">
                  <span class="text-[10px] text-[var(--muted)] block font-medium">Scheduled</span>
                  <span class="text-xl font-bold text-white font-mono mt-1 block">18</span>
                  <span class="text-[9px] text-[#2DD4BF]">Total Bookings</span>
                </div>
                <div class="p-3 rounded-2xl bg-[var(--background)] border border-[var(--border)]">
                  <span class="text-[10px] text-[var(--muted)] block font-medium">Completed</span>
                  <span class="text-xl font-bold text-emerald-400 font-mono mt-1 block">12</span>
                  <span class="text-[9px] text-emerald-400">Consultations Done</span>
                </div>
                <div class="p-3 rounded-2xl bg-[var(--background)] border border-[var(--border)]">
                  <span class="text-[10px] text-[var(--muted)] block font-medium">Waiting Room</span>
                  <span class="text-xl font-bold text-amber-300 font-mono mt-1 block">4</span>
                  <span class="text-[9px] text-amber-300">Avg Wait: 12m</span>
                </div>
                <div class="p-3 rounded-2xl bg-[var(--background)] border border-[var(--border)]">
                  <span class="text-[10px] text-[var(--muted)] block font-medium">Critical / Triage</span>
                  <span class="text-xl font-bold text-rose-400 font-mono mt-1 block">1</span>
                  <span class="text-[9px] text-rose-400">High Blood Pressure</span>
                </div>
                <div class="p-3 rounded-2xl bg-[var(--background)] border border-[var(--border)]">
                  <span class="text-[10px] text-[var(--muted)] block font-medium">Rx Issued</span>
                  <span class="text-xl font-bold text-purple-400 font-mono mt-1 block">11</span>
                  <span class="text-[9px] text-purple-300">All Signed 21 CFR</span>
                </div>
                <div class="p-3 rounded-2xl bg-[var(--background)] border border-[var(--border)]">
                  <span class="text-[10px] text-[var(--muted)] block font-medium">Follow-ups</span>
                  <span class="text-xl font-bold text-blue-400 font-mono mt-1 block">5</span>
                  <span class="text-[9px] text-blue-300">Due This Week</span>
                </div>
              </div>

              <!-- Quick Action Toolbar -->
              <div class="flex flex-wrap items-center gap-3 pt-2">
                <button onclick="switchTab('consultation')" class="px-5 py-2.5 rounded-2xl bg-gradient-to-r from-emerald-600 to-[#2DD4BF] text-white text-xs font-bold shadow-lg hover:brightness-110 transition">
                  🩺 Open Consultation Suite
                </button>
                <button onclick="openAddPatientModal()" class="px-4 py-2.5 rounded-2xl bg-[var(--background)] border border-[var(--border)] text-xs text-white font-bold hover:bg-slate-800 transition">
                  + Add New Patient
                </button>
                <button onclick="switchTab('patients')" class="px-4 py-2.5 rounded-2xl bg-[var(--background)] border border-[var(--border)] text-xs text-white font-bold hover:bg-slate-800 transition">
                  👥 Patient 360 Registry
                </button>
                <button onclick="switchTab('assistant')" class="px-4 py-2.5 rounded-2xl bg-[var(--background)] border border-[var(--border)] text-xs text-emerald-400 font-bold hover:bg-slate-800 transition">
                  🤖 Hakeem AI Assistant
                </button>
              </div>
            </div>

            <!-- Active OPD Queue Table -->
            <div class="bg-[var(--card)] rounded-3xl border border-[var(--border)] p-6 space-y-4">
              <div class="flex justify-between items-center border-b border-[var(--border)] pb-3">
                <h3 class="font-bold text-white text-base">Active Waiting Patients (OPD Queue)</h3>
                <span class="text-xs text-emerald-400 font-mono font-bold">Room 204 Active</span>
              </div>
              <div class="overflow-x-auto">
                <table class="w-full text-xs text-left">
                  <thead class="text-[10px] uppercase text-slate-400 bg-slate-900/50 border-b border-[var(--border)]">
                    <tr>
                      <th class="p-3">Token</th>
                      <th class="p-3">Patient Name</th>
                      <th class="p-3">MRN</th>
                      <th class="p-3">Chief Complaint</th>
                      <th class="p-3">Mizaj Baseline</th>
                      <th class="p-3">Status</th>
                      <th class="p-3 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-[var(--border)] text-slate-300">
                    <tr class="bg-emerald-500/5">
                      <td class="p-3 font-mono font-bold text-emerald-400">#A-14</td>
                      <td class="p-3 font-bold text-white">Hamza Farooqi (48M)</td>
                      <td class="p-3 font-mono text-[11px]">MRN-2026-0814</td>
                      <td class="p-3">Bilateral Knee Stiffness & Pain (Worse in Cold)</td>
                      <td class="p-3 text-cyan-300 font-semibold">Barid Balghami</td>
                      <td class="p-3"><span class="badge-blue text-[9px] px-2 py-0.5 rounded font-bold">Next in Line</span></td>
                      <td class="p-3 text-right"><button onclick="switchTab('consultation')" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg text-xs shadow">Start Encounter →</button></td>
                    </tr>
                    <tr>
                      <td class="p-3 font-mono font-bold text-slate-400">#A-15</td>
                      <td class="p-3 font-bold text-white">Bilal Ahmad (52M)</td>
                      <td class="p-3 font-mono text-[11px]">MRN-2026-0744</td>
                      <td class="p-3">Metabolic Syndrome, Post-prandial heaviness</td>
                      <td class="p-3 text-amber-300 font-semibold">Damawi Safrawi</td>
                      <td class="p-3"><span class="badge-emerald text-[9px] px-2 py-0.5 rounded">Checked In</span></td>
                      <td class="p-3 text-right"><button onclick="switchTab('consultation')" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold rounded-lg text-xs">Prepare File</button></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'consultation') {
        renderSingleConsultationWorkspace(container);
        return;
      }

      if (state.tab === 'patients') {
        container.innerHTML = `
          <div class="space-y-6 pb-10">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">Patient 360 & Longitudinal Ledger</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Institutional patient records, baseline Mizaj profiles, and active encounters.</p>
              </div>
              <button onclick="openAddPatientModal()" class="px-4 py-2 rounded-xl bg-emerald-600 text-white text-xs font-semibold hover:bg-emerald-500 shadow">
                + Register New Patient
              </button>
            </div>

            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-4">
              <div class="flex flex-col sm:flex-row justify-between gap-3">
                <input type="text" placeholder="Search by name, MRN, phone or ABHA ID..." class="px-4 py-2 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white flex-1 focus:outline-none focus:border-emerald-500">
                <select class="px-3 py-2 bg-slate-900 border border-slate-700 rounded-xl text-xs text-slate-300">
                  <option>All Mizaj Categories</option>
                  <option>Damawi (Sanguine)</option>
                  <option>Safrawi (Choleric)</option>
                  <option>Balghami (Phlegmatic)</option>
                  <option>Sawdawi (Melancholic)</option>
                </select>
              </div>

              <div class="overflow-x-auto">
                <table class="w-full text-xs text-left">
                  <thead class="text-[10px] uppercase text-slate-400 bg-slate-900/50 border-b border-[var(--border)]">
                    <tr>
                      <th class="p-3">MRN</th>
                      <th class="p-3">Patient Name</th>
                      <th class="p-3">Age/Sex</th>
                      <th class="p-3">Diagnosis</th>
                      <th class="p-3">Mizaj Baseline</th>
                      <th class="p-3">Last Visit</th>
                      <th class="p-3 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-[var(--border)] text-slate-300">
                    <tr class="hover:bg-slate-800/40">
                      <td class="p-3 font-mono font-bold text-emerald-400">MRN-2026-0814</td>
                      <td class="p-3 font-bold text-white">Hamza Farooqi</td>
                      <td class="p-3">48 / M</td>
                      <td class="p-3 text-cyan-300">Osteoarthritis (Knee)</td>
                      <td class="p-3">Barid Balghami</td>
                      <td class="p-3 font-mono">Today (Waiting)</td>
                      <td class="p-3 text-right"><button onclick="switchTab('consultation')" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg text-xs">Consult 🩺</button></td>
                    </tr>
                    <tr class="hover:bg-slate-800/40">
                      <td class="p-3 font-mono font-bold text-emerald-400">MRN-2026-0744</td>
                      <td class="p-3 font-bold text-white">Bilal Ahmad</td>
                      <td class="p-3">52 / M</td>
                      <td class="p-3">Metabolic Syndrome</td>
                      <td class="p-3">Damawi Safrawi</td>
                      <td class="p-3 font-mono">Sep 10, 2026</td>
                      <td class="p-3 text-right"><button onclick="switchTab('consultation')" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-lg text-xs">Open Chart</button></td>
                    </tr>
                    <tr class="hover:bg-slate-800/40">
                      <td class="p-3 font-mono font-bold text-emerald-400">MRN-2026-0612</td>
                      <td class="p-3 font-bold text-white">Ayesha Siddiqui</td>
                      <td class="p-3">34 / F</td>
                      <td class="p-3">PCOS & Anovulatory Cycles</td>
                      <td class="p-3">Barid Yabis</td>
                      <td class="p-3 font-mono">Sep 08, 2026</td>
                      <td class="p-3 text-right"><button onclick="switchTab('consultation')" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-lg text-xs">Open Chart</button></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'prescriptions') {
        container.innerHTML = `
          <div class="space-y-6 pb-10">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">Prescription & Nuskha Central Registry</h2>
                <p class="text-xs text-[var(--muted)] mt-1">21 CFR Part 11 signed prescriptions, FEFO dispensary dispatch status, and authorization logs.</p>
              </div>
              <button onclick="openReportModal()" class="px-4 py-2 rounded-xl bg-emerald-600 text-white text-xs font-semibold hover:bg-emerald-500 shadow">
                📑 Generate Summary PDF
              </button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)] space-y-1">
                <span class="text-slate-400 block">Total Issued Today</span>
                <span class="text-2xl font-bold text-white font-mono block">11 Nuskhas</span>
                <span class="text-[10px] text-emerald-400">100% Signed with 21 CFR Token</span>
              </div>
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)] space-y-1">
                <span class="text-slate-400 block">FEFO Dispensary Queue</span>
                <span class="text-2xl font-bold text-amber-300 font-mono block">3 Orders Pending</span>
                <span class="text-[10px] text-slate-400">Automated stock decrement active</span>
              </div>
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)] space-y-1">
                <span class="text-slate-400 block">Schedule E(1) Mudabbar Verified</span>
                <span class="text-2xl font-bold text-emerald-400 font-mono block">100% Compliant</span>
                <span class="text-[10px] text-emerald-400">Suranjan & Semecarpus certified</span>
              </div>
            </div>

            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-4">
              <h3 class="text-sm font-bold text-white">Recent Prescriptions</h3>
              <div class="space-y-3 text-xs">
                ${state.prescriptions.map(rx => `
                  <div class="p-4 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
                    <div class="space-y-1">
                      <div class="flex items-center gap-2">
                        <strong class="text-white text-sm">${rx.id} — Hamza Farooqi (MRN-2026-0814)</strong>
                        <span class="badge-emerald text-[9px] px-2 py-0.5 rounded font-bold">${rx.status}</span>
                      </div>
                      <p class="text-slate-300">Items: ManiVital Pro, Qurs-e-Taqwiyat-e-Mani, Arq Mako • Prescribed on ${rx.date}</p>
                      <span class="text-[10px] text-emerald-400 font-mono">${rx.signature}</span>
                    </div>
                    <div class="flex gap-2">
                      <button onclick="openReportModal()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold">Print Rx 🖨️</button>
                      <button onclick="showNotification('Prescription re-verified in dispensary queue.', 'info')" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold">Verify FEFO</button>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'followups') {
        container.innerHTML = `
          <div class="space-y-6 pb-10">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Longitudinal Follow-up & Relapse Guard</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Patient Reported Outcomes (WOMAC / VAS), Humoral Stability, and QSURA Outbound Alerts.</p>
              </div>
              <span class="badge-emerald text-xs px-3 py-1 rounded-full font-semibold">5 Follow-ups Due This Week</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="md:col-span-2 bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-4">
                <h3 class="text-sm font-bold text-white">Hamza Farooqi — Knee Mobility Trajectory (WOMAC)</h3>
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2 text-xs">
                  <div class="flex justify-between"><span class="text-slate-400">Baseline Pain Score (VAS):</span><strong class="text-rose-400 font-mono">7.8 / 10</strong></div>
                  <div class="flex justify-between"><span class="text-slate-400">Current Pain Score (Day 24):</span><strong class="text-emerald-400 font-mono">3.2 / 10 (-59%)</strong></div>
                  <div class="flex justify-between"><span class="text-slate-400">Joint Stiffness Duration:</span><strong class="text-white font-mono">15 mins (Down from 75 mins)</strong></div>
                  <div class="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden mt-2"><div class="bg-emerald-500 h-full rounded-full" style="width: 76%"></div></div>
                </div>
                <div class="flex justify-between items-center pt-2">
                  <span class="text-xs text-slate-300">Next Scheduled Milestone: <strong class="text-white">Sep 20, 2026</strong></span>
                  <button onclick="handleSendWhatsAppFollowup(this)" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition">
                    💬 Dispatch WhatsApp Adherence Ping
                  </button>
                </div>
              </div>

              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3 text-xs">
                <h3 class="text-sm font-bold text-white">Relapse Risk Assessment</h3>
                <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                  <span class="text-slate-400 block">Current Risk Level</span>
                  <strong class="text-emerald-400 text-base block font-mono">LOW (12% Risk)</strong>
                  <p class="text-[10px] text-slate-400">Stable barid ratab temperament without acute exacerbations.</p>
                </div>
                <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                  <span class="text-slate-400 block">Season (Fasl) Adjustment</span>
                  <strong class="text-amber-300 block">Autumn (Kharif) Transition</strong>
                  <p class="text-[10px] text-slate-400">Increase warm anupan; prepare for winter barid aggravation.</p>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'assistant') {
        container.innerHTML = `
          <div class="space-y-6 pb-10">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Hakeem Sahab™ AI Clinical Reasoning Assistant</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Classical Tibb-e-Unani multi-hop knowledge graph cross-referenced with modern biomedical evidence.</p>
              </div>
              <span class="px-3 py-1 bg-amber-500/10 text-amber-300 border border-amber-500/30 rounded-full text-xs font-bold font-mono">21 CFR 11 Barrier Active</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="md:col-span-2 bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-4">
                <h3 class="text-sm font-bold text-white">Interactive Clinical Copilot Query</h3>
                <div class="flex gap-2">
                  <input id="hakeem-direct-query-input" type="text" placeholder="e.g. Suranjan dosage in elderly patient with elevated uric acid..." class="flex-1 px-4 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-emerald-500">
                  <button onclick="askHakeemAI(document.getElementById('hakeem-direct-query-input').value)" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition">
                    Consult AI ⚡
                  </button>
                </div>

                <div class="flex flex-wrap gap-2 text-[11px]">
                  <span class="text-slate-400">Sample Inquiries:</span>
                  <button onclick="askHakeemAI('Analyze Hamza Farooqi knee dyscrasia')" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-emerald-400 font-mono">Knee Dyscrasia</button>
                  <button onclick="askHakeemAI('Check Suranjan and Colchicum interaction')" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-emerald-400 font-mono">Suranjan Interaction</button>
                  <button onclick="askHakeemAI('Suggest Tanqiya Stage 1 protocol')" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-emerald-400 font-mono">Tanqiya Stage 1</button>
                </div>

                <div id="hakeem-assistant-result" class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2 text-xs text-slate-200">
                  <div class="flex justify-between items-center text-[10px] text-slate-400 border-b border-slate-800 pb-1.5">
                    <span>Evidence Source: <strong class="text-emerald-400">Unani Pharmacopoeia of India (UPI Vol II) & PubMed</strong></span>
                    <span>Concordance: <strong class="text-emerald-400">96.4%</strong></span>
                  </div>
                  <p class="leading-relaxed">
                    <strong>Recommended Protocol:</strong> Su-e-Mizaj Barid Balghami with chronic knee joint effusion indicates a primary 7-day <em>Munzij-e-Balgham</em> preparation followed by gentle evacuation (<em>Tanqiya</em>). Prescribe Habb-e-Suranjan (2 tabs BID) with warm water, supported by Arq Mako (25ml). Prohibit sour and cold foods.
                  </p>
                  <div class="pt-2 flex justify-end">
                    <button onclick="insertAiRecommendationToPlan()" class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg shadow">
                      + Insert to Active Encounter Plan
                    </button>
                  </div>
                </div>
              </div>

              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3 text-xs">
                <h3 class="text-sm font-bold text-white">AI Safety Guardrails</h3>
                <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                  <strong class="text-emerald-400 block">Zero Autonomous Prescribing</strong>
                  <p class="text-slate-400 text-[11px]">AI outputs remain advisory recommendations until explicitly cryptographically signed by the attending Tabeeb.</p>
                </div>
                <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                  <strong class="text-cyan-300 block">Contraindication Interceptor</strong>
                  <p class="text-slate-400 text-[11px]">Suranjan (Colchicum autumnale) dose locked to maximum 2g/day with mandatory Musleh (Kateera/Gond).</p>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'knowledge') {
        container.innerHTML = `
          <div class="space-y-6 pb-10">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">ZKB Clinical Knowledge & Pharmacopoeia Graph</h2>
                <p class="text-xs text-[var(--muted)] mt-1">1,280+ Canonical Botanical Monographs, Temperament Classifications, and Badal/Musleh Traversal.</p>
              </div>
              <button onclick="showNotification('Knowledge Graph cache refreshed.', 'info')" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-700">
                🔄 Sync Graph
              </button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3 text-xs">
                <span class="text-[10px] text-emerald-400 font-bold uppercase tracking-wider block">Mufradat (Single Drug)</span>
                <h4 class="font-bold text-white text-base">Suranjan Shireen (*Colchicum autumnale*)</h4>
                <div class="space-y-1 text-slate-300">
                  <div>Mizaj: <strong class="text-amber-300">Garm 2° / Khushk 2°</strong></div>
                  <div>Primary Action: <strong class="text-white">Musakkin-e-Waja (Analgesic) & Mukhrij-e-Mawad</strong></div>
                  <div>Musleh (Corrective): <strong class="text-emerald-400">Samagh-e-Arabi / Kateera</strong></div>
                  <div>Badal (Substitute): <strong class="text-cyan-300">Asgandh (Withania somnifera)</strong></div>
                </div>
              </div>

              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3 text-xs">
                <span class="text-[10px] text-emerald-400 font-bold uppercase tracking-wider block">Mufradat (Single Drug)</span>
                <h4 class="font-bold text-white text-base">Asgandh Nagori (*Withania somnifera*)</h4>
                <div class="space-y-1 text-slate-300">
                  <div>Mizaj: <strong class="text-amber-300">Garm 1° / Khushk 2°</strong></div>
                  <div>Primary Action: <strong class="text-white">Muqawwi-e-Aam (Vital Restorer) & Muallid-e-Mani</strong></div>
                  <div>Musleh (Corrective): <strong class="text-emerald-400">Ghee / Shakar Safaid</strong></div>
                  <div>HPLC Marker: <strong class="text-cyan-300">Withaferin-A (>1.5%)</strong></div>
                </div>
              </div>

              <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-3 text-xs">
                <span class="text-[10px] text-emerald-400 font-bold uppercase tracking-wider block">Murakkabat (Compound)</span>
                <h4 class="font-bold text-white text-base">Majun Dabeed-ul-Ward</h4>
                <div class="space-y-1 text-slate-300">
                  <div>Mizaj: <strong class="text-amber-300">Garm 2° / Khushk 2°</strong></div>
                  <div>Target Organ: <strong class="text-white">Kabid (Liver) & Mida (Stomach)</strong></div>
                  <div>Indication: <strong class="text-emerald-400">Sluggish Hepatobiliary Flow, Jaundice</strong></div>
                  <div>Standard: <strong class="text-cyan-300">NFUM Part I, Page 112</strong></div>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'profile') {
        container.innerHTML = `
          <div class="space-y-6 pb-10">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Physician Credentials & 21 CFR Signature</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Medical council registration, institutional tenure, and cryptographic key status.</p>
              </div>
              <span class="badge-emerald text-xs px-3 py-1 rounded-full font-semibold">Active & Licensed</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3">
                <h3 class="text-sm font-bold text-white">Clinician Details</h3>
                <div class="space-y-2">
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Name:</span><strong class="text-white">Hakim Dr. Irfan Ashraf</strong></div>
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Academic Degrees:</span><strong class="text-emerald-400 font-bold">BUMS, MD (Unani Clinical Medicine)</strong></div>
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Medical Registration:</span><strong class="text-white font-mono">CCIM / DMC-UN-88412</strong></div>
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Department:</span><strong class="text-white">Integrative OPD & Clinical Rheumatology</strong></div>
                </div>
              </div>

              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3">
                <h3 class="text-sm font-bold text-white">Cryptographic Signature Token</h3>
                <div class="space-y-2">
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>21 CFR Token:</span><strong class="text-emerald-400 font-mono">HMAC-SHA256 (HARDWARE HSM)</strong></div>
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Facility Key:</span><strong class="text-white">ZAYVORA-CENTRAL-DELHI-01</strong></div>
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Emergency Helpline:</span><strong class="text-emerald-400 font-mono">+91 97738 82657</strong></div>
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Audit Trail Status:</span><strong class="text-emerald-400">Merkle Root Verified</strong></div>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }
    }'''
