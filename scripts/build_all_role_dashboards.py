import re
import os

print("Building all 70 role-tab dashboard implementations...")

# We will read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect the sections we will replace or upgrade
# 1. Add missing helper functions: insertAiRecommendationToPlan, callNextPatientQueue, sendChatMessage, etc.
missing_helpers = '''
    // Missing clinical copilot & queue helpers
    function insertAiRecommendationToPlan() {
      const planInput = document.getElementById('consultation-plan-text');
      const rec = "Standardized Tanqiya Protocol (Day 1-7): Habb-e-Suranjan 2 tab BID + Arq Mako 25ml with warm water. Dietary: Zero cold water, avoid acidic curds.";
      if (planInput) {
        planInput.value = (planInput.value ? planInput.value + "\\n\\n" : "") + "[HAKEEM SAHAB AI RECOMMENDATION]: " + rec;
      }
      showNotification('Hakeem Sahab AI recommendation inserted into Active Encounter Care Plan.', 'success');
      toggleHakeemDrawer(false);
    }

    let currentQueueTokenIndex = 2;
    const queueTokens = [
      { token: "A-12", patient: "Rashid Minhas", room: "201", dr: "Dr. Aisha", status: "IN CONSULTATION" },
      { token: "A-13", patient: "Zubaida Begum", room: "202", dr: "Dr. Akhtar", status: "IN CONSULTATION" },
      { token: "A-14", patient: "Hamza Farooqi", room: "204", dr: "Dr. Irfan", status: "CALLED NOW" },
      { token: "A-15", patient: "Bilal Ahmad", room: "204", dr: "Dr. Irfan", status: "WAITING (NEXT)" },
      { token: "A-16", patient: "Fatima Noor", room: "201", dr: "Dr. Aisha", status: "CHECKED IN" }
    ];

    function callNextPatientQueue() {
      currentQueueTokenIndex = (currentQueueTokenIndex + 1) % queueTokens.length;
      const nextPat = queueTokens[currentQueueTokenIndex];
      showNotification(`🔔 Calling Token #${nextPat.token}: ${nextPat.patient} to Room ${nextPat.room} (${nextPat.dr})`, 'success');
      if (state.role === 'clinic' && state.tab === 'queue') {
        renderClinicApp(document.getElementById('workspace-container'));
      }
    }

    let patientChatMessages = [
      { sender: "doctor", name: "Hakim Dr. Tariq Mansoor", time: "Yesterday 04:30 PM", text: "Salam Hamza, please ensure you take Suranjan after warm milk, not cold water. Report any morning stiffness." },
      { sender: "patient", name: "Hamza Farooqi", time: "Today 09:15 AM", text: "Wa alaykumu s-salam Dr. Sahib. Stiffness has reduced by nearly 40%. Walking is much easier this morning." },
      { sender: "doctor", name: "Hakim Dr. Tariq Mansoor", time: "Today 10:00 AM", text: "Alhamdulillah. Keep following the diet strictly. We will review your knee mobility in Room 204." }
    ];

    function sendPatientChatMessage() {
      const input = document.getElementById('chat-input-field');
      if (!input || !input.value.trim()) return;
      patientChatMessages.push({
        sender: state.role === 'doctor' ? 'doctor' : 'patient',
        name: state.role === 'doctor' ? 'Hakim Dr. Irfan' : 'Hamza Farooqi',
        time: 'Just now',
        text: input.value.trim()
      });
      input.value = '';
      if (state.role === 'patient') {
        renderPatientApp(document.getElementById('workspace-container'));
      } else if (state.role === 'doctor') {
        renderDoctorApp(document.getElementById('workspace-container'));
      }
      showNotification('Clinical message dispatched securely.', 'success');
    }
'''

# 2. Complete renderPatientApp supporting all 8 tabs:
# ['home', 'appointments', 'health', 'treatment', 'medicines', 'reports', 'messages', 'profile']
new_renderPatientApp = '''    function renderPatientApp(container) {
      if (state.tab === 'home') {
        container.innerHTML = `
          <div class="space-y-6">
            <!-- Greeting Header -->
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">Good Morning, Hamza</h2>
                <p class="text-xs text-[var(--muted)] mt-1">MRN: <span class="font-mono text-emerald-400 font-semibold">${state.patient.mrn}</span> • Active Care Plan: <span class="text-white font-medium">Osteoarthritis & Knee Stiffness</span></p>
              </div>
              <div class="flex items-center gap-2">
                <button onclick="switchTab('appointments')" class="px-4 py-2 rounded-xl bg-emerald-600 text-white text-xs font-semibold hover:bg-emerald-500 transition-colors shadow-md">
                  + Book Appointment
                </button>
                <button onclick="switchTab('medicines')" class="px-4 py-2 rounded-xl border border-[var(--border)] text-xs text-[var(--muted)] hover:text-white transition-colors">
                  View Prescriptions
                </button>
              </div>
            </div>

            <!-- Dashboard Action Grid -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              
              <!-- Card 1: Upcoming Appointment -->
              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b border-[var(--border)] pb-2.5">
                  <span class="text-xs font-bold text-white flex items-center gap-1.5">
                    📅 Next Scheduled Visit
                  </span>
                  <span class="badge-blue text-[10px] px-2 py-0.5 rounded font-semibold">Today</span>
                </div>
                <div class="space-y-1">
                  <p class="text-sm font-bold text-white">${state.patient.nextAppointment.time}</p>
                  <p class="text-xs text-[var(--muted)]">${state.patient.nextAppointment.doctor}</p>
                  <p class="text-[11px] text-emerald-400 font-medium">${state.patient.nextAppointment.facility} • Room 204</p>
                </div>
                <div class="pt-2 border-t border-[var(--border)] flex items-center justify-between">
                  <span id="patient-status-badge" class="badge-blue text-[10px] px-2 py-0.5 rounded font-bold">Confirmed</span>
                  <button onclick="handlePatientOnlineCheckIn(this)" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded-lg font-semibold transition">
                    Check In Online
                  </button>
                </div>
              </div>

              <!-- Card 2: Today's Medicine Reminders -->
              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b border-[var(--border)] pb-2.5">
                  <span class="text-xs font-bold text-white flex items-center gap-1.5">
                    💊 Today's Regimen
                  </span>
                  <span class="badge-emerald text-[10px] px-2 py-0.5 rounded font-semibold">2 of 3 Taken</span>
                </div>
                <div class="space-y-2 text-xs">
                  <div class="flex items-center justify-between p-2 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                    <div>
                      <strong class="text-white block">ManiVital Pro</strong>
                      <span class="text-[10px] text-[var(--muted)]">5g Morning with Warm Milk</span>
                    </div>
                    <span class="badge-emerald text-[10px] px-2 py-0.5 rounded font-bold">Taken ✓</span>
                  </div>
                  <div class="flex items-center justify-between p-2 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                    <div>
                      <strong class="text-white block">Qurs-e-Taqwiyat-e-Mani</strong>
                      <span class="text-[10px] text-[var(--muted)]">2 tabs Bedtime</span>
                    </div>
                    <button onclick="this.textContent='Taken ✓'; this.className='badge-emerald text-[10px] px-2 py-1 rounded font-bold';" class="px-2 py-1 bg-slate-800 hover:bg-emerald-600 text-white text-[10px] rounded font-semibold transition">
                      Mark Taken
                    </button>
                  </div>
                </div>
              </div>

              <!-- Card 3: Health Score & Mizaj -->
              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b border-[var(--border)] pb-2.5">
                  <span class="text-xs font-bold text-white flex items-center gap-1.5">
                    ⚖️ Meezan-e-Sehat Score
                  </span>
                  <span class="text-xs text-emerald-400 font-mono font-bold">84 / 100</span>
                </div>
                <div class="space-y-1 text-xs">
                  <div class="flex justify-between text-[11px]"><span class="text-slate-400">Current Mizaj:</span><strong class="text-cyan-300">Barid Balghami (Cold/Moist)</strong></div>
                  <div class="flex justify-between text-[11px]"><span class="text-slate-400">Baseline Target:</span><strong class="text-white">Mo'tadil (Equable)</strong></div>
                  <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden mt-2"><div class="bg-emerald-500 h-full rounded-full" style="width: 84%"></div></div>
                </div>
                <div class="pt-2 border-t border-[var(--border)] flex justify-between items-center text-[11px]">
                  <span class="text-slate-400">Stage: <strong class="text-white">Tahleel (Resolution)</strong></span>
                  <button onclick="switchTab('treatment')" class="text-emerald-400 hover:underline font-bold">View Plan →</button>
                </div>
              </div>

            </div>

            <!-- Quick Links -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
              <button onclick="switchTab('health')" class="p-3.5 rounded-xl bg-[var(--card)] border border-[var(--border)] hover:border-emerald-500/50 text-left transition space-y-1">
                <span class="text-base block">🩺</span>
                <strong class="text-white block">My Health & Vitals</strong>
                <span class="text-[10px] text-[var(--muted)]">10-Ajnas & Lab Markers</span>
              </button>
              <button onclick="switchTab('treatment')" class="p-3.5 rounded-xl bg-[var(--card)] border border-[var(--border)] hover:border-emerald-500/50 text-left transition space-y-1">
                <span class="text-base block">🌿</span>
                <strong class="text-white block">Treatment Roadmap</strong>
                <span class="text-[10px] text-[var(--muted)]">4-Stage Afaal Protocol</span>
              </button>
              <button onclick="switchTab('reports')" class="p-3.5 rounded-xl bg-[var(--card)] border border-[var(--border)] hover:border-emerald-500/50 text-left transition space-y-1">
                <span class="text-base block">📑</span>
                <strong class="text-white block">Lab & Radiology Reports</strong>
                <span class="text-[10px] text-[var(--muted)]">hs-CRP & X-Ray PDFs</span>
              </button>
              <button onclick="switchTab('messages')" class="p-3.5 rounded-xl bg-[var(--card)] border border-[var(--border)] hover:border-emerald-500/50 text-left transition space-y-1">
                <span class="text-base block">💬</span>
                <strong class="text-white block">Care Team Channel</strong>
                <span class="text-[10px] text-[var(--muted)]">Chat with Dr. Tariq</span>
              </button>
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
                <h2 class="text-xl font-bold text-white">Consultation Appointments</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Manage scheduled in-person visits and tele-health video consultations.</p>
              </div>
              <button onclick="openAddPatientModal()" class="px-4 py-2 rounded-xl bg-emerald-600 text-white text-xs font-semibold hover:bg-emerald-500 shadow">
                + Book New Slot
              </button>
            </div>

            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-4">
              <h3 class="text-sm font-bold text-white flex items-center gap-2">
                <span>🗓️</span> Upcoming Visit
              </h3>
              <div class="p-4 rounded-xl bg-[var(--background)] border border-emerald-500/30 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div class="space-y-1">
                  <div class="flex items-center gap-2">
                    <strong class="text-white text-base">Hakim Dr. Tariq Mansoor</strong>
                    <span class="badge-emerald text-[10px] px-2 py-0.5 rounded font-bold">Confirmed</span>
                  </div>
                  <p class="text-xs text-slate-300">Senior Tabeeb • ZAYVORA Central Hospital (Room 204)</p>
                  <p class="text-xs text-emerald-400 font-mono">Tomorrow 10:30 AM • Knee Joint Follow-up & Pulse Evaluation</p>
                </div>
                <div class="flex gap-2">
                  <button onclick="handleConfirmMobileVideo(this)" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-xl shadow">Join WebRTC Room</button>
                  <button onclick="showNotification('Appointment rescheduled request logged.', 'info')" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold rounded-xl border border-slate-700">Reschedule</button>
                </div>
              </div>
            </div>

            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-4">
              <h3 class="text-sm font-bold text-white">Past Encounter History</h3>
              <div class="overflow-x-auto">
                <table class="w-full text-xs text-left">
                  <thead class="text-[10px] uppercase text-slate-400 bg-slate-900/50 border-b border-[var(--border)]">
                    <tr>
                      <th class="p-3">Date</th>
                      <th class="p-3">Attending Physician</th>
                      <th class="p-3">Type</th>
                      <th class="p-3">Diagnosis</th>
                      <th class="p-3">Status</th>
                      <th class="p-3 text-right">Summary</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-[var(--border)] text-slate-300">
                    <tr>
                      <td class="p-3 font-mono">Sep 10, 2026</td>
                      <td class="p-3 font-semibold text-white">Dr. Irfan Ashraf</td>
                      <td class="p-3">In-Person OPD</td>
                      <td class="p-3 text-cyan-300">Su-e-Mizaj Barid Balghami</td>
                      <td class="p-3"><span class="badge-emerald text-[9px] px-2 py-0.5 rounded">Completed</span></td>
                      <td class="p-3 text-right"><button onclick="openReportModal()" class="text-emerald-400 font-bold hover:underline">View PDF ↗</button></td>
                    </tr>
                    <tr>
                      <td class="p-3 font-mono">Aug 28, 2026</td>
                      <td class="p-3 font-semibold text-white">Dr. Aisha Siddiqui</td>
                      <td class="p-3">Tele-Health Video</td>
                      <td class="p-3">Tanqiya Stage 1 Review</td>
                      <td class="p-3"><span class="badge-emerald text-[9px] px-2 py-0.5 rounded">Completed</span></td>
                      <td class="p-3 text-right"><button onclick="openReportModal()" class="text-emerald-400 font-bold hover:underline">View PDF ↗</button></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'health') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">My Health & Classical Vitals</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Longitudinal 10-Ajnas Pulse, Tongue Chromametry, and Clinical Biomarkers.</p>
              </div>
              <button onclick="triggerNabzPulseTest()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow">
                ⚡ Calibrate Pulse Sensor
              </button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)] space-y-1">
                <span class="text-slate-400 block">Blood Pressure</span>
                <span class="text-2xl font-bold text-white font-mono block">120/78</span>
                <span class="text-[10px] text-emerald-400">Optimal Normotensive</span>
              </div>
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)] space-y-1">
                <span class="text-slate-400 block">Resting Heart Rate</span>
                <span class="text-2xl font-bold text-emerald-400 font-mono block">72 BPM</span>
                <span class="text-[10px] text-slate-400">PPG Waveform Regular</span>
              </div>
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)] space-y-1">
                <span class="text-slate-400 block">Inflammatory hs-CRP</span>
                <span class="text-2xl font-bold text-white font-mono block">2.1 mg/L</span>
                <span class="text-[10px] text-emerald-400">Down from 4.8 mg/L (-56%)</span>
              </div>
              <div class="p-4 rounded-xl bg-[var(--card)] border border-[var(--border)] space-y-1">
                <span class="text-slate-400 block">Meezan Equilibrium</span>
                <span class="text-2xl font-bold text-cyan-300 font-mono block">84 / 100</span>
                <span class="text-[10px] text-emerald-400">Humoral Balance Restoring</span>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3">
                <h3 class="text-sm font-bold text-white">Al-Ajnas al-Ashrah (10 Classical Pulse Metrics)</h3>
                <div class="space-y-2 text-xs">
                  <div class="flex justify-between p-2 rounded-lg bg-slate-900 border border-slate-800"><span>1. Miqdar (Magnitude):</span><strong class="text-white">Azeem (Large/Full)</strong></div>
                  <div class="flex justify-between p-2 rounded-lg bg-slate-900 border border-slate-800"><span>2. Kayfiyat (Stroke Strength):</span><strong class="text-white">Qawi (Strong)</strong></div>
                  <div class="flex justify-between p-2 rounded-lg bg-slate-900 border border-slate-800"><span>3. Zamanah (Speed):</span><strong class="text-white">Batee (Slow/Cold)</strong></div>
                  <div class="flex justify-between p-2 rounded-lg bg-slate-900 border border-slate-800"><span>4. Qawam (Arterial Elasticity):</span><strong class="text-emerald-400">Layyin (Soft/Supple)</strong></div>
                </div>
              </div>
              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3">
                <h3 class="text-sm font-bold text-white">Multispectral Lisan (Tongue Chromametry)</h3>
                <div class="space-y-2 text-xs">
                  <div class="flex justify-between p-2 rounded-lg bg-slate-900 border border-slate-800"><span>Sub-Lingual Venous Stasis:</span><strong class="text-emerald-400">None (Grade 0)</strong></div>
                  <div class="flex justify-between p-2 rounded-lg bg-slate-900 border border-slate-800"><span>Saburra Coating Thickness:</span><strong class="text-white">0.42 mm (Normal Thin)</strong></div>
                  <div class="flex justify-between p-2 rounded-lg bg-slate-900 border border-slate-800"><span>Dorsal Surface Moisture:</span><strong class="text-cyan-300">68% Hydration (Barid Ratab)</strong></div>
                  <div class="flex justify-between p-2 rounded-lg bg-slate-900 border border-slate-800"><span>Optical Sensor Status:</span><strong class="text-emerald-400">Calibrated at 415-850nm</strong></div>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'treatment') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">4-Stage Afaal Treatment Roadmap</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Systematic detoxification, humoral resolution, organ strengthening, and health preservation.</p>
              </div>
              <span class="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-full text-xs font-bold font-mono">Stage 2 Active</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
              <div class="p-4 rounded-xl bg-slate-900/60 border border-emerald-500/40 space-y-2">
                <span class="text-[10px] text-emerald-400 font-bold block uppercase">Stage 01 • Finished</span>
                <h4 class="font-bold text-white text-sm">Tanqiya (Evacuation)</h4>
                <p class="text-[11px] text-slate-400">Purging of morbid phlegm (Balgham) and metabolic toxins via mild concoctions.</p>
                <span class="badge-emerald text-[9px] px-2 py-0.5 rounded font-bold">7 Days Completed ✓</span>
              </div>
              <div class="p-4 rounded-xl bg-slate-900 border-2 border-emerald-400 space-y-2 shadow-lg">
                <span class="text-[10px] text-emerald-400 font-bold block uppercase">Stage 02 • ACTIVE</span>
                <h4 class="font-bold text-white text-sm">Tahleel (Resolution)</h4>
                <p class="text-[11px] text-slate-300">Dissolving localized joint congestion using warm Natool fomentation & Suranjan.</p>
                <span class="badge-blue text-[9px] px-2 py-0.5 rounded font-bold">Day 9 of 14</span>
              </div>
              <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2 opacity-70">
                <span class="text-[10px] text-slate-400 font-bold block uppercase">Stage 03 • Next</span>
                <h4 class="font-bold text-white text-sm">Taqwiyaat (Restoration)</h4>
                <p class="text-[11px] text-slate-400">Strengthening knee cartilage matrix and vital organs (Muqawwi-e-Aza).</p>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[9px] font-bold">28 Days Duration</span>
              </div>
              <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2 opacity-70">
                <span class="text-[10px] text-slate-400 font-bold block uppercase">Stage 04 • Planned</span>
                <h4 class="font-bold text-white text-sm">Hifz (Preservation)</h4>
                <p class="text-[11px] text-slate-400">Permanent lifestyle harmony (Asbab-e-Sittah) to prevent relapse.</p>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[9px] font-bold">60 Days Maintenance</span>
              </div>
            </div>

            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3">
              <h3 class="text-sm font-bold text-white">Dietary Directives (*Ilaj bil-Ghiza*)</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div class="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 space-y-1">
                  <strong class="text-rose-300 block">Prohibited Foods (Maniyat):</strong>
                  <p class="text-slate-300">Cold drinks, refrigerated water, sour curds, red meat, excessive lentils (Maash), and nightshades.</p>
                </div>
                <div class="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 space-y-1">
                  <strong class="text-emerald-300 block">Recommended Foods (Mufeedat):</strong>
                  <p class="text-slate-300">Warm sheep bone broth seasoned with saffron, ginger, black pepper, and cumin; soaked almonds and figs.</p>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'medicines') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 class="text-xl font-bold text-white">My Prescriptions & Posology</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Standardized dosage schedules, vehicles (*Anupan*), and spoken audio guidance.</p>
              </div>
              <button onclick="handleRequestMobileRefill(this)" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow">
                Request Dispensary Refill
              </button>
            </div>

            <!-- Vernacular Audio Scribe Player -->
            <div class="bg-gradient-to-r from-emerald-900/30 to-slate-900 border border-emerald-500/30 p-5 rounded-2xl space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-emerald-400 flex items-center gap-2">
                  <span>🔊</span> Vernacular Audio Posology Player
                </span>
                <div class="flex gap-2">
                  <button onclick="setAudioLanguage('ur')" class="px-2.5 py-1 rounded bg-slate-800 text-[10px] text-white font-bold">اردو</button>
                  <button onclick="setAudioLanguage('hi')" class="px-2.5 py-1 rounded bg-slate-800 text-[10px] text-white font-bold">हिंदी</button>
                  <button onclick="setAudioLanguage('en')" class="px-2.5 py-1 rounded bg-slate-800 text-[10px] text-white font-bold">English</button>
                </div>
              </div>
              <div class="p-3 bg-slate-900/80 rounded-xl border border-slate-800 text-xs text-slate-200">
                <p id="audio-spoken-text">Take one teaspoon twice daily after breakfast and dinner with lukewarm milk. Strictly avoid cold drinks.</p>
              </div>
              <button onclick="toggleAudioPlayback()" class="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl transition">
                ▶ Listen to Audio Posology
              </button>
            </div>

            <!-- Prescriptions Cards -->
            <div class="space-y-4">
              ${state.prescriptions.map(rx => `
                <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-4">
                  <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-[var(--border)] pb-3">
                    <div>
                      <div class="flex items-center gap-2">
                        <span class="font-bold text-white text-base">${rx.id}</span>
                        <span class="badge-emerald text-[10px] px-2 py-0.5 rounded font-bold">${rx.status}</span>
                      </div>
                      <span class="text-xs text-[var(--muted)]">Prescribed by ${rx.prescriber} on ${rx.date}</span>
                    </div>
                    <span class="font-mono text-[10px] text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded border border-emerald-500/20">
                      ${rx.signature}
                    </span>
                  </div>

                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    ${rx.medicines.map(m => `
                      <div class="p-3.5 rounded-xl bg-[var(--background)] border border-[var(--border)] space-y-1.5 text-xs">
                        <div class="flex justify-between items-start">
                          <div>
                            <strong class="text-white text-sm block">${m.name}</strong>
                            <span class="text-[11px] text-emerald-400 font-mono">${m.form} • ${m.strength}</span>
                          </div>
                          <span class="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-bold">${m.frequency}</span>
                        </div>
                        <div class="text-[11px] text-slate-300">Vehicle (*Anupan*): <span class="text-white font-medium">${m.anupan}</span></div>
                        <div class="text-[11px] text-slate-400">Duration: <span class="text-white font-mono">${m.duration}</span></div>
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

      if (state.tab === 'reports') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Diagnostic & Clinical Reports</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Digitally signed diagnostic lab sheets, radiograph summaries, and encrypted PDF downloads.</p>
              </div>
              <button onclick="openReportModal()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow">
                📑 Generate Summary PDF
              </button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3">
                <div class="flex justify-between items-center">
                  <span class="font-bold text-white text-sm">Comprehensive Metabolic & Inflammatory Panel</span>
                  <span class="badge-emerald text-[9px] px-2 py-0.5 rounded font-bold">Verified</span>
                </div>
                <p class="text-xs text-slate-300">hs-CRP, ESR, Serum Uric Acid, Fasting Blood Glucose, and LFT enzymes.</p>
                <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs space-y-1">
                  <div class="flex justify-between"><span>Test Date:</span><strong class="text-white font-mono">Sep 10, 2026</strong></div>
                  <div class="flex justify-between"><span>Lab Facility:</span><strong class="text-white">Central Hospital Pathology Wing</strong></div>
                </div>
                <button onclick="openReportModal()" class="w-full py-2 bg-slate-800 hover:bg-slate-700 text-emerald-400 font-bold text-xs rounded-xl border border-slate-700 transition">
                  Download Encrypted PDF 📥
                </button>
              </div>

              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3">
                <div class="flex justify-between items-center">
                  <span class="font-bold text-white text-sm">Multispectral Tongue Chromametry (4,096 Px)</span>
                  <span class="badge-blue text-[9px] px-2 py-0.5 rounded font-bold">Instrument Log</span>
                </div>
                <p class="text-xs text-slate-300">High-resolution chromametric spectrum confirming Su-e-Mizaj Barid Balghami moisture patterns.</p>
                <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs space-y-1">
                  <div class="flex justify-between"><span>Wavelength:</span><strong class="text-white font-mono">415 - 850 nm</strong></div>
                  <div class="flex justify-between"><span>Integrity Hash:</span><strong class="text-emerald-400 font-mono">SHA256: 4a9f...b012</strong></div>
                </div>
                <button onclick="openReportModal()" class="w-full py-2 bg-slate-800 hover:bg-slate-700 text-emerald-400 font-bold text-xs rounded-xl border border-slate-700 transition">
                  Download Encrypted PDF 📥
                </button>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'messages') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Direct Care Team Channel</h2>
                <p class="text-xs text-[var(--muted)] mt-1">End-to-end encrypted medical messaging with attending Senior Tabeeb.</p>
              </div>
              <span class="badge-emerald text-xs px-3 py-1 rounded-full font-semibold">Attending: Hakim Dr. Tariq Mansoor</span>
            </div>

            <!-- Chat Window -->
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 flex flex-col h-[420px] justify-between">
              <div class="space-y-3 overflow-y-auto pr-2">
                ${patientChatMessages.map(msg => `
                  <div class="flex flex-col ${msg.sender === 'doctor' ? 'items-start' : 'items-end'}">
                    <span class="text-[10px] text-slate-400 mb-0.5">${msg.name} • ${msg.time}</span>
                    <div class="p-3 rounded-2xl max-w-[80%] text-xs ${msg.sender === 'doctor' ? 'bg-slate-800 text-white rounded-tl-none border border-slate-700' : 'bg-emerald-600 text-white rounded-tr-none'}">
                      ${msg.text}
                    </div>
                  </div>
                `).join('')}
              </div>

              <div class="pt-3 border-t border-[var(--border)] flex gap-2">
                <input id="chat-input-field" type="text" placeholder="Type your clinical update or question here..." class="flex-1 px-4 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-emerald-500">
                <button onclick="sendPatientChatMessage()" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition">
                  Send
                </button>
              </div>
            </div>
          </div>
        `;
        return;
      }

      if (state.tab === 'profile') {
        container.innerHTML = `
          <div class="space-y-6">
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-white">Patient Profile & ABHA Identity</h2>
                <p class="text-xs text-[var(--muted)] mt-1">Demographics, emergency triage contact, and national health locker linkage.</p>
              </div>
              <button onclick="showNotification('Profile updates saved to EHR.', 'success')" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow">
                Save Changes
              </button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3">
                <h3 class="text-sm font-bold text-white">Demographics</h3>
                <div class="space-y-2">
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Full Name:</span><strong class="text-white">Hamza Farooqi</strong></div>
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>MRN (Medical Record Number):</span><strong class="text-emerald-400 font-mono">${state.patient.mrn}</strong></div>
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Age & Sex:</span><strong class="text-white">48 Years / Male</strong></div>
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Blood Group:</span><strong class="text-white">O+ (Rh Positive)</strong></div>
                </div>
              </div>

              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 space-y-3">
                <h3 class="text-sm font-bold text-white">Health System Linkage</h3>
                <div class="space-y-2">
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>ABHA Address:</span><strong class="text-emerald-400 font-mono">hamza.farooqi@abdm</strong></div>
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Primary Matab:</span><strong class="text-white">Central Hospital, New Delhi</strong></div>
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>Emergency Helpline:</span><strong class="text-emerald-400 font-mono">+91 97738 82657</strong></div>
                  <div class="flex justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800"><span>21 CFR Electronic Consent:</span><strong class="text-emerald-400">Granted (HIPAA / DISHA)</strong></div>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }
    }
'''

