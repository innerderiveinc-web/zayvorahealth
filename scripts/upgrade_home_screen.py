import re

def build_home_html():
    return '''      // DEFAULT TAB: 'home' - The Official Landing Page
      const st = clinicalStages[activeWebsiteStage];
      const activeAxis = organAxesList[activeOrganAxis] || organAxesList[0];
      
      const calcKey = (previewMizajAnswers.temp === 'cold' && previewMizajAnswers.moisture === 'moist') ? "Balghami" :
                      (previewMizajAnswers.temp === 'hot' && previewMizajAnswers.moisture === 'moist') ? "Damawi" :
                      (previewMizajAnswers.temp === 'hot' && previewMizajAnswers.moisture === 'dry') ? "Safrawi" : "Sawdawi";
      
      const mizajInfo = mizajDetailsMap[calcKey] || mizajDetailsMap["Balghami"];

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

            <h1 class="text-3xl sm:text-4xl md:text-6xl font-extrabold text-white max-w-5xl mx-auto leading-tight tracking-tight">
              Ancient Wisdom. Modern Science. <br class="hidden sm:inline" />
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#2DD4BF] via-emerald-300 to-teal-200">
                Intelligent Healthcare.
              </span>
            </h1>

            <p class="text-xs sm:text-sm md:text-base text-[#94A3B8] max-w-3xl mx-auto leading-relaxed">
              ZAYVORA Health OS™ unites 1,000 years of codified Greco-Arab Unani clinical doctrine with multi-omics diagnostic precision, 
              100 Hz arterial PPG pulse telemetry, longitudinal Mizaj profiling, and fail-closed 21 CFR Part 11 clinician governance.
            </p>

            <!-- Action Matrix -->
            <div class="flex flex-wrap items-center justify-center gap-3 pt-2">
              <button onclick="document.getElementById('opd-booking-card').scrollIntoView({ behavior: 'smooth' });" class="px-6 py-3.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs shadow-xl shadow-emerald-950/50 transition flex items-center gap-2">
                <span>🎫</span> Generate Instant OPD Token
              </button>
              <button onclick="document.getElementById('mizaj-assessment-section').scrollIntoView({ behavior: 'smooth' });" class="px-6 py-3.5 rounded-xl border border-emerald-500/40 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 font-semibold text-xs transition flex items-center gap-2">
                <span>🧬</span> 60-Sec Mizaj Assessment
              </button>
              <button onclick="viewWebsitePage('products')" class="px-6 py-3.5 rounded-xl border border-[#334155] bg-[#1E293B]/70 hover:bg-[#1E293B] text-slate-300 hover:text-white font-semibold text-xs transition">
                🌿 View 10-Product Store
              </button>
            </div>

            <!-- Regulatory & Quality Accreditations Strip -->
            <div class="flex flex-wrap items-center justify-center gap-6 pt-4 text-[11px] text-[#94A3B8] border-t border-slate-800/80">
              <span class="flex items-center gap-1.5"><span class="text-emerald-400">✓</span> Ministry of AYUSH Aligned</span>
              <span class="flex items-center gap-1.5"><span class="text-emerald-400">✓</span> NCISM Clinical Standards</span>
              <span class="flex items-center gap-1.5"><span class="text-emerald-400">✓</span> 21 CFR Part 11 Digital Seal</span>
              <span class="flex items-center gap-1.5"><span class="text-emerald-400">✓</span> ABDM &amp; FHIR R4 Ready</span>
              <span class="flex items-center gap-1.5"><span class="text-emerald-400">✓</span> Schedule E(1) Mudabbar Verified</span>
            </div>
          </div>

          <!-- ===================================================================== -->
          <!-- 2. INSTITUTIONAL METRICS COUNTER MARQUEE -->
          <!-- ===================================================================== -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1">
              <span class="text-slate-400 uppercase text-[10px] font-bold tracking-wider">Governed Facilities</span>
              <div class="text-2xl font-extrabold text-white">14 Centers</div>
              <span class="text-[10px] text-emerald-400 font-mono">Central Hospital &amp; Matabs</span>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1">
              <span class="text-slate-400 uppercase text-[10px] font-bold tracking-wider">Board Tabeebs &amp; Clinicians</span>
              <div class="text-2xl font-extrabold text-emerald-400">48 Specialists</div>
              <span class="text-[10px] text-slate-400 font-mono">100% Council Registered</span>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1">
              <span class="text-slate-400 uppercase text-[10px] font-bold tracking-wider">Monthly Consultations</span>
              <div class="text-2xl font-extrabold text-white">3,240 Visits</div>
              <span class="text-[10px] text-teal-300 font-mono">98.4% Resolution Rate</span>
            </div>
            <div class="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] space-y-1">
              <span class="text-slate-400 uppercase text-[10px] font-bold tracking-wider">Standardized Pharmacopoeia</span>
              <div class="text-2xl font-extrabold text-white">250+ Monographs</div>
              <span class="text-[10px] text-emerald-400 font-mono">Verified HPLC Fingerprints</span>
            </div>
          </div>

          <!-- Guided Care Discovery Wizard ("What Brings You Here?") -->
          <div id="care-discovery-wizard"></div>

          <!-- ===================================================================== -->
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
                <h2 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Hakeem Dr. Irfan Ashraf</h2>
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
                  <div class="text-white font-semibold">BUMS, MD (Unani), PhD</div>
                  <div class="text-[10px] text-slate-400">Moalajat &amp; Waja-ul-Mafasil Authority</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 space-y-1">
                  <span class="text-[10px] text-teal-400 font-bold uppercase">Academic Leadership</span>
                  <div class="text-white font-semibold">Director, CP-AFUM Curriculum</div>
                  <div class="text-[10px] text-slate-400">96 Lectures &bull; 6 Clinical Modules</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 space-y-1">
                  <span class="text-[10px] text-amber-400 font-bold uppercase">Statutory Registration</span>
                  <div class="text-white font-semibold">NCISM / CCIM Certified</div>
                  <div class="text-[10px] text-slate-400 font-mono">Reg. No: #CCIM-BUMS-DL-0881</div>
                </div>
              </div>
            </div>
          </div>

          <!-- ===================================================================== -->
          <!-- 4. LIVE DIAGNOSTIC HARDWARE & ARTERIAL NABZ PULSE CANVAS -->
          <!-- ===================================================================== -->
          <div class="p-6 md:p-8 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-5 shadow-lg">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-[#1E293B] pb-3">
              <div class="flex items-center gap-2.5">
                <span class="w-3 h-3 rounded-full bg-emerald-400 animate-pulse"></span>
                <div>
                  <h3 class="text-sm font-bold text-white">Live Clinical Diagnostic Hardware &amp; DSP Waveform Streams</h3>
                  <span class="text-[10px] text-slate-400">Real-time physiological arterial pulse capture &amp; multispectral telemetry</span>
                </div>
              </div>
              <span class="px-3 py-1 rounded-lg bg-[#1E293B] text-emerald-400 font-mono font-bold text-[10px] border border-emerald-500/30">
                100 Hz Streaming DSP &bull; 12ms Telemetry Latency
              </span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 items-center">
              <div class="lg:col-span-5 p-4 rounded-2xl bg-[#0A0F1D] border border-[#1E293B] space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-white flex items-center gap-1.5">
                    <span class="text-emerald-400 text-base">🩺</span> Arterial Nabz PPG Waveform
                  </span>
                  <span class="font-mono text-emerald-400 font-bold">72 BPM (Bat&apos;ee)</span>
                </div>
                
                <!-- Live Continuous Waveform Canvas -->
                <canvas id="preview-pulse-canvas" width="340" height="90" class="w-full h-24 rounded-lg bg-[#0F172A] border border-[#1E293B]"></canvas>

                <div class="grid grid-cols-3 gap-2 text-[10px] text-[#94A3B8] font-mono text-center">
                  <div class="p-1.5 rounded bg-[#1E293B] border border-slate-800"><strong class="text-white block">Kayfiyat</strong>Layyin (Soft)</div>
                  <div class="p-1.5 rounded bg-[#1E293B] border border-slate-800"><strong class="text-white block">Miqdar</strong>Azeem (High Amp)</div>
                  <div class="p-1.5 rounded bg-[#1E293B] border border-slate-800"><strong class="text-white block">Zamanah</strong>Bat&apos;ee (Slow)</div>
                </div>
              </div>

              <div class="lg:col-span-7 grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div class="p-4 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-1.5 text-xs">
                  <div class="flex justify-between items-center"><span class="text-xl">👅</span><span class="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-300">LISAN</span></div>
                  <h4 class="font-bold text-white text-xs">Tongue Chromametry</h4>
                  <div class="text-[10px] text-[#94A3B8] space-y-0.5">
                    <div>Saburra: <strong class="text-white">White (Phlegm)</strong></div>
                    <div>Moisture: <strong class="text-emerald-400">68% Rutubat</strong></div>
                    <div>Humoral: <strong class="text-amber-400">Balghami Shift</strong></div>
                  </div>
                </div>

                <div class="p-4 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-1.5 text-xs">
                  <div class="flex justify-between items-center"><span class="text-xl">❄️</span><span class="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300">COLD-CHAIN</span></div>
                  <h4 class="font-bold text-white text-xs">Dispensary IoT</h4>
                  <div class="text-[10px] text-[#94A3B8] space-y-0.5">
                    <div>Temp: <strong class="text-emerald-400">19.4&deg;C Safe</strong></div>
                    <div>Humidity: <strong class="text-white">42% RH</strong></div>
                    <div>FEFO Lock: <strong class="text-emerald-400">Active</strong></div>
                  </div>
                </div>

                <div class="p-4 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-1.5 text-xs">
                  <div class="flex justify-between items-center"><span class="text-xl">📡</span><span class="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-300">BLE MESH</span></div>
                  <h4 class="font-bold text-white text-xs">Wearables Gateway</h4>
                  <div class="text-[10px] text-[#94A3B8] space-y-0.5">
                    <div>Sensor Nodes: <strong class="text-purple-300">4 Active</strong></div>
                    <div>SpO2 Telemetry: <strong class="text-emerald-400">98% Normal</strong></div>
                    <div>Relapse Risk: <strong class="text-emerald-400">0.04 (Minimal)</strong></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ===================================================================== -->
          <!-- 5. INTERACTIVE 60-SECOND MIZAJ CONSTITUTIONAL ASSESSMENT -->
          <!-- ===================================================================== -->
          <div id="mizaj-assessment-section" class="p-6 md:p-8 rounded-3xl bg-[#0F172A] border border-emerald-500/30 space-y-6 shadow-xl">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-[#334155] pb-4">
              <div>
                <span class="text-xs font-bold text-[#2DD4BF] uppercase tracking-wider">Precision Constitutional Diagnostics</span>
                <h3 class="text-xl sm:text-2xl font-extrabold text-white mt-0.5">60-Second Interactive Mizaj Assessment</h3>
                <p class="text-xs text-[#94A3B8]">Select your parameters below to compute your classical temperament and tailored dietetics.</p>
              </div>
              <span class="px-3 py-1 bg-emerald-500/20 text-emerald-300 font-mono font-bold text-xs rounded-full border border-emerald-500/40">
                Al-Ajnas al-Ashrah Logic
              </span>
            </div>

            <!-- Quiz Questions Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
              <div class="p-3.5 bg-[#1E293B] rounded-2xl border border-[#334155] space-y-2">
                <span class="text-[10px] font-bold text-teal-400 block uppercase">1. Thermal Sensitivity</span>
                <div class="grid grid-cols-2 gap-1.5">
                  <button onclick="setPreviewMizaj('temp', 'hot')" class="py-2 rounded-xl text-xs font-semibold transition ${previewMizajAnswers.temp === 'hot' ? 'bg-[#0D9488] text-white shadow' : 'bg-[#0F172A] text-slate-400 hover:text-white'}">🔥 Warm / Heat</button>
                  <button onclick="setPreviewMizaj('temp', 'cold')" class="py-2 rounded-xl text-xs font-semibold transition ${previewMizajAnswers.temp === 'cold' ? 'bg-[#0D9488] text-white shadow' : 'bg-[#0F172A] text-slate-400 hover:text-white'}">❄️ Cold / Chills</button>
                </div>
              </div>
              <div class="p-3.5 bg-[#1E293B] rounded-2xl border border-[#334155] space-y-2">
                <span class="text-[10px] font-bold text-teal-400 block uppercase">2. Moisture &amp; Skin Texture</span>
                <div class="grid grid-cols-2 gap-1.5">
                  <button onclick="setPreviewMizaj('moisture', 'moist')" class="py-2 rounded-xl text-xs font-semibold transition ${previewMizajAnswers.moisture === 'moist' ? 'bg-[#0D9488] text-white shadow' : 'bg-[#0F172A] text-slate-400 hover:text-white'}">💧 Moist / Hydrated</button>
                  <button onclick="setPreviewMizaj('moisture', 'dry')" class="py-2 rounded-xl text-xs font-semibold transition ${previewMizajAnswers.moisture === 'dry' ? 'bg-[#0D9488] text-white shadow' : 'bg-[#0F172A] text-slate-400 hover:text-white'}">🍂 Dry / Rough</button>
                </div>
              </div>
              <div class="p-3.5 bg-[#1E293B] rounded-2xl border border-[#334155] space-y-2">
                <span class="text-[10px] font-bold text-teal-400 block uppercase">3. Skeletal Frame &amp; Bone</span>
                <div class="grid grid-cols-2 gap-1.5">
                  <button onclick="setPreviewMizaj('physique', 'broad')" class="py-2 rounded-xl text-xs font-semibold transition ${previewMizajAnswers.physique === 'broad' ? 'bg-[#0D9488] text-white shadow' : 'bg-[#0F172A] text-slate-400 hover:text-white'}">🛡️ Broad Frame</button>
                  <button onclick="setPreviewMizaj('physique', 'slender')" class="py-2 rounded-xl text-xs font-semibold transition ${previewMizajAnswers.physique === 'slender' ? 'bg-[#0D9488] text-white shadow' : 'bg-[#0F172A] text-slate-400 hover:text-white'}">⚡ Slender / Agile</button>
                </div>
              </div>
              <div class="p-3.5 bg-[#1E293B] rounded-2xl border border-[#334155] space-y-2">
                <span class="text-[10px] font-bold text-teal-400 block uppercase">4. Sleep &amp; Digestion Depth</span>
                <div class="grid grid-cols-2 gap-1.5">
                  <button onclick="setPreviewMizaj('sleep', 'deep')" class="py-2 rounded-xl text-xs font-semibold transition ${previewMizajAnswers.sleep === 'deep' ? 'bg-[#0D9488] text-white shadow' : 'bg-[#0F172A] text-slate-400 hover:text-white'}">😴 Deep Rest</button>
                  <button onclick="setPreviewMizaj('sleep', 'light')" class="py-2 rounded-xl text-xs font-semibold transition ${previewMizajAnswers.sleep === 'light' ? 'bg-[#0D9488] text-white shadow' : 'bg-[#0F172A] text-slate-400 hover:text-white'}">🌙 Light / Agile</button>
                </div>
              </div>
            </div>

            <!-- Calculated Mizaj Dynamic Clinical Profile Output -->
            <div class="p-6 rounded-2xl bg-gradient-to-r from-[#1E293B] via-[#0F172A] to-[#1E293B] border border-emerald-500/40 space-y-4">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-[#334155] pb-3">
                <div>
                  <span class="text-[10px] font-mono uppercase text-emerald-400 font-bold">Calculated Constitutional Type</span>
                  <h4 class="text-xl font-extrabold text-white">${mizajInfo.title}</h4>
                  <span class="text-xs text-[#2DD4BF] font-mono">${mizajInfo.element}</span>
                </div>
                <button onclick="switchRole('doctor'); switchTab('consultation');" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-xl shadow transition">
                  Consult Hakeem Dr. Irfan Ashraf →
                </button>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                <div class="p-3.5 rounded-xl bg-[#0A0F1D] border border-slate-800 space-y-1">
                  <strong class="text-slate-400 block uppercase text-[10px]">Organ Vulnerabilities</strong>
                  <p class="text-slate-300 leading-relaxed">${mizajInfo.organVulnerabilities}</p>
                </div>
                <div class="p-3.5 rounded-xl bg-[#0A0F1D] border border-slate-800 space-y-1">
                  <strong class="text-teal-400 block uppercase text-[10px]">Tailored Dietetics (Ilaj bil Ghiza)</strong>
                  <p class="text-slate-300 leading-relaxed">${mizajInfo.dietaryPrescription}</p>
                </div>
                <div class="p-3.5 rounded-xl bg-[#0A0F1D] border border-slate-800 space-y-1">
                  <strong class="text-emerald-400 block uppercase text-[10px]">Recommended Formula &amp; Regimen</strong>
                  <p class="text-slate-300 leading-relaxed font-mono text-[11px]">${mizajInfo.recommendedFormula}</p>
                  <p class="text-[10px] text-slate-400 mt-1">${mizajInfo.regimenalTherapy}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- ===================================================================== -->
          <!-- 6. INTERACTIVE 12-ORGAN-AXIS CROSS-TALK DIAGNOSTIC EXPLORER -->
          <!-- ===================================================================== -->
          <div class="p-6 md:p-8 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-6 shadow-xl">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-[#334155] pb-4">
              <div>
                <span class="text-xs font-bold text-[#2DD4BF] uppercase tracking-wider">Systems Biology Framework</span>
                <h3 class="text-xl sm:text-2xl font-extrabold text-white mt-0.5">The 12-Organ-Axis Clinical Diagnostic Explorer</h3>
                <p class="text-xs text-[#94A3B8]">Click an organ axis below to examine root-cause humoral cross-talk and targeted interventions.</p>
              </div>
              <span class="px-3 py-1 rounded-full bg-[#0D9488]/20 text-[#2DD4BF] font-mono text-xs font-semibold">
                Proprietary Axis Engine
              </span>
            </div>

            <!-- Axis Selection Tabs -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5">
              ${organAxesList.map((axis, idx) => `
                <button onclick="setOrganAxis(${idx})" class="p-3.5 rounded-2xl text-left border transition-all ${idx === activeOrganAxis ? 'bg-emerald-500/20 border-emerald-400 shadow-lg text-white' : 'bg-[#1E293B] border-[#334155] text-slate-400 hover:border-emerald-500/40 hover:text-white'}">
                  <div class="text-xl mb-1">${axis.icon}</div>
                  <div class="text-xs font-bold text-white leading-snug">${axis.name}</div>
                  <span class="text-[10px] text-[#2DD4BF] font-mono mt-1 block">${axis.element}</span>
                </button>
              `).join('')}
            </div>

            <!-- Active Axis Deep Clinical Breakdown -->
            <div class="p-6 rounded-2xl bg-[#1E293B] border border-emerald-500/30 space-y-4">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-[#334155] pb-3">
                <div class="flex items-center gap-3">
                  <span class="text-3xl">${activeAxis.icon}</span>
                  <div>
                    <h4 class="text-base font-bold text-white">${activeAxis.name}</h4>
                    <span class="text-xs text-emerald-400 font-mono">${activeAxis.element}</span>
                  </div>
                </div>
                <span class="px-3 py-1 bg-emerald-500/20 text-emerald-300 font-mono text-xs font-bold rounded-lg border border-emerald-500/30">
                  ${activeAxis.successRate}
                </span>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div class="p-4 rounded-xl bg-[#0A0F1D] border border-slate-800 space-y-1.5">
                  <strong class="text-slate-400 block uppercase text-[10px]">Root Cause Pathophysiology</strong>
                  <p class="text-slate-300 leading-relaxed">${activeAxis.rootCause}</p>
                  <div class="pt-2 text-[11px] text-slate-400">
                    <span class="text-emerald-400 font-semibold">Objective Biomarkers:</span> ${activeAxis.markers}
                  </div>
                </div>

                <div class="p-4 rounded-xl bg-[#0A0F1D] border border-slate-800 space-y-1.5">
                  <strong class="text-teal-400 block uppercase text-[10px]">Dual-Track Therapeutic Intervention</strong>
                  <p class="text-slate-300 leading-relaxed">${activeAxis.dualTrack}</p>
                  <div class="pt-2">
                    <button onclick="switchRole('doctor'); switchTab('tadbeer');" class="text-xs text-emerald-400 hover:underline font-semibold">
                      Explore Full 16-Modality Tadbeer Protocols &rarr;
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ===================================================================== -->
          <!-- 7. INSTANT OPD QUEUE TOKEN GENERATOR CARD -->
          <!-- ===================================================================== -->
          <div id="opd-booking-card" class="p-6 md:p-8 rounded-3xl bg-gradient-to-r from-[#0F172A] via-[#1E293B] to-[#0F172A] border border-emerald-500/40 space-y-5 shadow-2xl">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-[#334155] pb-3">
              <div>
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Fast-Track Patient Admission</span>
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
          <!-- 8. THE 12-STAGE CLOSED-LOOP CLINICAL CONTINUUM -->
          <!-- ===================================================================== -->
          <div class="space-y-6">
            <div class="text-center space-y-1">
              <span class="text-xs font-bold text-[#2DD4BF] uppercase tracking-wider">Clinical Framework</span>
              <h2 class="text-2xl font-bold text-white">The 12-Stage Closed-Loop Clinical Continuum</h2>
              <p class="text-xs text-[#94A3B8]">Click any stage below to inspect the verified clinical mechanics.</p>
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
              ${clinicalStages.map((stage, idx) => `
                <button onclick="setWebsiteStage(${idx})" class="p-3 rounded-xl text-left border transition-all ${idx === activeWebsiteStage ? 'bg-[#0D9488]/20 border-[#2DD4BF] shadow-lg' : 'bg-[#1E293B] border-[#334155] hover:border-[#0D9488]/50'}">
                  <div class="flex justify-between items-center text-[10px] font-mono font-bold">
                    <span class="${idx === activeWebsiteStage ? 'text-[#2DD4BF]' : 'text-slate-500'}">${stage.num}.</span>
                    <span class="${idx === activeWebsiteStage ? 'text-white' : 'text-slate-400'}">${stage.name}</span>
                  </div>
                  <div class="text-[10px] text-slate-200 mt-1 truncate font-semibold">${stage.title}</div>
                </button>
              `).join('')}
            </div>

            <div class="p-6 rounded-2xl bg-gradient-to-r from-[#1E293B] via-[#0F172A] to-[#1E293B] border border-[#2DD4BF]/40 space-y-3">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-[#334155] pb-3">
                <div>
                  <span class="text-[10px] font-mono font-bold text-[#2DD4BF]">STAGE ${st.num} OF 12</span>
                  <h3 class="text-lg font-bold text-white">${st.name}: ${st.title}</h3>
                  <span class="text-xs text-emerald-400 italic">${st.latin}</span>
                </div>
                <span class="px-3 py-1 rounded-full bg-[#0D9488]/20 border border-[#0D9488]/40 text-[#2DD4BF] text-[10px] font-semibold">
                  Verified Protocol
                </span>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div>
                  <strong class="text-slate-400 block mb-1 uppercase text-[10px]">Clinical Mechanism</strong>
                  <p class="text-slate-300 leading-relaxed">${st.desc}</p>
                </div>
                <div class="bg-[#0A0F1D] p-3 rounded-xl border border-[#334155]">
                  <strong class="text-teal-400 block mb-1 uppercase text-[10px]">Clinical Execution &amp; Safety Output</strong>
                  <p class="text-slate-400 font-mono text-[11px]">${st.action}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- ===================================================================== -->
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
          <!-- 10. 10 FORMULATIONS STORE SHOWCASE -->
          <!-- ===================================================================== -->
          <div class="space-y-6">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-2 border-b border-[#334155] pb-3">
              <div>
                <span class="text-xs font-bold text-[#2DD4BF] uppercase tracking-wider">Botanical Therapeutics</span>
                <h3 class="text-2xl font-bold text-white">ZAYVORA Herbals Portfolio</h3>
                <p class="text-xs text-[#94A3B8]">GMP manufactured, HPLC verified, Schedule E(1) Mudabbar purified.</p>
              </div>
              <button onclick="viewWebsitePage('products')" class="px-4 py-2 border border-[#334155] text-xs font-bold text-[#2DD4BF] hover:bg-[#1E293B] rounded-xl">
                Open Cart &amp; Dispensary (${herbalsCart.length} items) &rarr;
              </button>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3">
              ${herbalsProducts.map(p => `
                <div class="p-4 rounded-2xl bg-[#1E293B] border border-[#334155] flex flex-col justify-between space-y-3 hover:border-teal-500/50 transition">
                  <div class="space-y-1.5">
                    <div class="flex justify-between items-center">
                      <span class="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-[#0D9488]/20 text-[#2DD4BF]">${p.category}</span>
                      <span class="text-xs font-bold text-white">₹${p.price}</span>
                    </div>
                    <h4 class="text-xs font-bold text-white">${p.name}</h4>
                    <p class="text-[10px] text-[#94A3B8] line-clamp-2">${p.desc}</p>
                  </div>
                  <div class="pt-2 border-t border-[#334155] flex justify-between items-center">
                    <button onclick="viewWebsitePage('knowledge')" class="text-[10px] text-slate-400 hover:text-white">Monograph</button>
                    <button onclick="addToHerbalsCart('${p.id}')" class="px-2.5 py-1 bg-[#0D9488] hover:bg-[#14B8A6] text-white text-[10px] font-bold rounded-lg transition">
                      + Add
                    </button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- ===================================================================== -->
          <!-- 11. VERNACULAR AUDIO POSOLOGY & SCRIPTURE GUIDANCE -->
          <!-- ===================================================================== -->
          <div class="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-4">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-[#1E293B] pb-3">
              <div class="flex items-center gap-2">
                <span class="text-2xl">🔊</span>
                <div>
                  <h4 class="font-bold text-white text-sm">Vernacular Audio Posology Guidance</h4>
                  <p class="text-[11px] text-[#94A3B8]">Listen to verified dosage instructions in Urdu, Hindi, or English.</p>
                </div>
              </div>
              <div class="flex gap-1.5">
                <button onclick="setAudioLanguage('ur')" class="px-3 py-1 rounded-lg text-xs font-semibold ${audioPosologyLang === 'ur' ? 'bg-emerald-600 text-white' : 'bg-slate-800 text-slate-400'}">اردو (Urdu)</button>
                <button onclick="setAudioLanguage('hi')" class="px-3 py-1 rounded-lg text-xs font-semibold ${audioPosologyLang === 'hi' ? 'bg-emerald-600 text-white' : 'bg-slate-800 text-slate-400'}">हिन्दी (Hindi)</button>
                <button onclick="setAudioLanguage('en')" class="px-3 py-1 rounded-lg text-xs font-semibold ${audioPosologyLang === 'en' ? 'bg-emerald-600 text-white' : 'bg-slate-800 text-slate-400'}">English</button>
              </div>
            </div>

            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 flex flex-col sm:flex-row justify-between items-center gap-3">
              <p class="text-xs text-slate-200" id="audio-posology-text">
                ایک چمچ صبح اور شام کھانے کے بعد نیم گرم دودھ کے ساتھ لیں۔ ٹھنڈے مشروبات اور کھٹی چیزوں سے پرہیز کریں۔
              </p>
              <button onclick="toggleAudioPosology()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl transition flex items-center gap-2 shrink-0">
                <span>▶</span> Play Audio Posology
              </button>
            </div>
          </div>

          <!-- ===================================================================== -->
          <!-- 12. BOTTOM DIRECTORY TO ALL 25 PAGES -->
          <!-- ===================================================================== -->
          <div class="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] flex flex-col sm:flex-row justify-between items-center gap-4">
            <div>
              <h4 class="font-bold text-white text-sm">Explore All 25 Canonical Web Pages</h4>
              <p class="text-xs text-[#94A3B8]">Browse the complete public site structure including clinical programs, conditions, research, and ethics.</p>
            </div>
            <button onclick="viewWebsitePage('pages25')" class="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-600 transition">
              View 25 Canonical Pages Directory &rarr;
            </button>
          </div>

        </div>
      `;

      if (typeof renderDiscoveryWizard === 'function') renderDiscoveryWizard();
      if (typeof initWebsiteWaveform === 'function') initWebsiteWaveform();
    }'''

def upgrade_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Locate start of DEFAULT TAB: 'home'
    marker_start = "      // DEFAULT TAB: 'home' - The Official Landing Page"
    idx_start = content.find(marker_start)
    if idx_start == -1:
        print(f"Could not find marker in {filepath}")
        return False

    marker_end = "      if (typeof renderDiscoveryWizard === 'function') renderDiscoveryWizard();
      if (typeof initWebsiteWaveform === 'function') initWebsiteWaveform();\n    }"
    idx_end = content.find(marker_end, idx_start)
    if idx_end == -1:
        print(f"Could not find end marker in {filepath}")
        return False

    new_home = build_home_html()
    new_content = content[:idx_start] + new_home + content[idx_end + len(marker_end):]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Successfully upgraded {filepath}")
    return True

for p in ['index.html', 'docs/index.html']:
    upgrade_file(p)
