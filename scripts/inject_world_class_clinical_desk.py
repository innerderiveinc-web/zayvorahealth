import re
import sys

def run():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # -------------------------------------------------------------
    # 1. Inject JavaScript helpers for Clinical Thread & Care Discovery
    # -------------------------------------------------------------
    js_helpers = """
    // =========================================================================
    // THE ZAYVORA CLINICAL THREAD™ (12-STAGE INTERACTIVE CONTINUUM)
    // =========================================================================
    const clinicalThreadStages = [
      { id: 'patient', num: '01', label: 'Patient', title: 'Intake & Demographic Validation', status: 'COMPLETED', badge: 'badge-emerald', desc: 'MRN verified (MRN-2026-0008), ABHA ID linked, zero identity conflicts.', evidence: 'Master Patient Index' },
      { id: 'assessment', num: '02', label: 'Assessment', title: 'Objective Physical & Scribe Signs', status: 'COMPLETED', badge: 'badge-emerald', desc: 'Chief complaints, PPG pulse waveform, and tongue chromametry captured.', evidence: 'PPG & multispectral tongue telemetry' },
      { id: 'mizaj', num: '03', label: 'Mizaj', title: '10-Ajnas Constitutional Evaluation', status: 'COMPLETED', badge: 'badge-emerald', desc: 'Barid-Ratab (Cold-Moist) humoral deviation against personal baseline.', evidence: 'Al-Ajnas al-Ashrah 10-vector scoring' },
      { id: 'axes', num: '04', label: 'Organ-Axis', title: '12 Organ-System Pathological Mapping', status: 'COMPLETED', badge: 'badge-emerald', desc: 'Axis 5 (Mafasil-Dam Joint Matrix) active score 68/100.', evidence: '12-Axis cross-talk evaluation' },
      { id: 'knowledge', num: '05', label: 'Knowledge', title: 'ZKB Canonical Substance Retrieval', status: 'COMPLETED', badge: 'badge-emerald', desc: '3 canonical monographs retrieved with HPLC fingerprints.', evidence: 'UPI Vol I & II, NFUM Part I' },
      { id: 'evidence', num: '06', label: 'Evidence', title: 'Evidence Claim & Tier Grounding', status: 'COMPLETED', badge: 'badge-emerald', desc: 'Grade-B clinical evidence supported by observational cohorts.', evidence: 'Evidence Grading Matrix E0-E6' },
      { id: 'safety', num: '07', label: 'Safety Rail', title: 'Fail-Closed Safety Firewall', status: 'MONITORING', badge: 'badge-amber', desc: '5/6 safety gates passed; Schedule E(1) Mudabbar certificate pending release.', evidence: 'Clinical Safety Invariants SAFETY-001-010' },
      { id: 'hakeem', num: '08', label: 'Hakeem Sahab', title: 'Contextual AI Copilot Decision Support', status: 'READY', badge: 'badge-purple', desc: 'Low uncertainty (0.08); Stage 2 Munzij-e-Balgham recommended.', evidence: 'Bio-BERT + ZKB Graph Reasoning' },
      { id: 'nuskha', num: '09', label: 'Nuskha Composer', title: 'Multi-Pillar Therapeutic Authoring', status: 'IN_PROGRESS', badge: 'badge-blue', desc: 'Formulating Dawa, Ghiza, Tadbeer, Nafsiyat, and Yad.', evidence: '5-Pillar Classical Continuum' },
      { id: 'approval', num: '10', label: '21 CFR Approval', title: 'Clinician Credential & Digital Seal', status: 'PENDING', badge: 'badge-rose', desc: 'Awaiting Dr. Tariq Mansoor cryptographic PIN sign-off.', evidence: '21 CFR Part 11 SHA-256 seal' },
      { id: 'treatment', num: '11', label: 'Treatment', title: 'Dispensary Fulfillment & Care Loop', status: 'UPCOMING', badge: 'badge-muted', desc: 'FEFO batch dispensing and daily Asbab-e-Sittah regimen tracking.', evidence: 'Central Dispensary Barcode' },
      { id: 'outcome', num: '12', label: 'Outcome & RWE', title: 'PROMs & Observational Research', status: 'UPCOMING', badge: 'badge-muted', desc: 'WOMAC / VAS pain attenuation curves and RWE cohort aggregation.', evidence: 'ICH E2B Safety & Registry' }
    ];

    let activeClinicalThreadStage = 'nuskha';

    function renderClinicalThread(activeStageId) {
      activeClinicalThreadStage = activeStageId || activeClinicalThreadStage;
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
            <span class="text-[10px] px-2 py-0.5 rounded-full font-bold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
              Active: Stage 09 (Nuskha)
            </span>
          </div>

          <!-- Horizontal Interactive Ribbon -->
          <div class="flex items-center gap-1.5 overflow-x-auto pb-1.5 scrollbar-thin">
            ${clinicalThreadStages.map((stage, idx) => {
              const isActive = stage.id === activeClinicalThreadStage;
              const isCompleted = ['patient', 'assessment', 'mizaj', 'axes', 'knowledge', 'evidence'].includes(stage.id);
              let stateClass = 'clinical-thread-pending border-slate-700 text-slate-400';
              let icon = stage.num;
              if (isActive) {
                stateClass = 'clinical-thread-active border-emerald-500 text-emerald-300 font-bold';
                icon = '▶ ' + stage.num;
              } else if (isCompleted) {
                stateClass = 'clinical-thread-completed border-emerald-500/40 text-emerald-200';
                icon = '✓';
              } else if (stage.status === 'MONITORING') {
                stateClass = 'border-amber-500/40 text-amber-300 bg-amber-500/10 font-medium';
                icon = '⚠';
              }
              return `
                <button onclick="openClinicalThreadModal('${stage.id}')" class="clinical-thread-item flex-shrink-0 flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl border text-[11px] ${stateClass}" title="${stage.title} (Click to inspect evidence)">
                  <span class="font-mono text-[10px] opacity-80">${icon}</span>
                  <span class="whitespace-nowrap">${stage.label}</span>
                </button>
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
      { id: 'Digestive', label: '🥗 Digestive (Hazm)', desc: 'IBS, Acid Reflux, Bloating, Sluggish Digestion' },
      { id: 'Metabolic', label: '⚡ Metabolic (Istehala)', desc: 'Insulin Resistance, Fatty Liver, Weight Resistance' },
      { id: 'Hormonal', label: '🔄 Hormonal (Tadbeer)', desc: 'Thyroid Dysregulation, Adrenal Fatigue, Cortisol' },
      { id: 'Reproductive', label: '🌿 Reproductive (Tawleed)', desc: 'PCOS, Menstrual Irregularity, Male Fertility' },
      { id: 'Musculoskeletal', label: '🦴 Joint & Spine (Mafasil)', desc: 'Osteoarthritis, Chronic Back Pain, Sciatica' },
      { id: 'Sleep_Stress', label: '🌙 Sleep & Stress (Nafs)', desc: 'Insomnia, Chronic Anxiety, Restless Sleep, Burnout' },
      { id: 'Respiratory', label: '🫁 Respiratory (Tanaffus)', desc: 'Allergic Rhinitis, Chronic Sinusitis, Bronchitis' },
      { id: 'Skin_Hair', label: '✨ Skin & Hair (Jild)', desc: 'Psoriasis, Eczema, Adult Acne, Diffuse Hair Thinning' },
      { id: 'General_Wellness', label: '⚖️ General Vitality', desc: 'Constitutional Mizaj Alignment & Seasonal Detox' }
    ];

    const discoveryCareTypes = [
      { id: 'Consultation', label: '🩺 Doctor Consultation', desc: 'Comprehensive 1-on-1 diagnostic evaluation with pulse & tongue assessment.' },
      { id: 'Program', label: '📆 90-Day Integrative Program', desc: 'Structured Munzij-Mushil phase protocol with weekly follow-ups.' },
      { id: 'Follow_up', label: '🔄 Phase Review & Refill', desc: 'Milestone evaluation, posology adjustments, and prescription refill.' },
      { id: 'Second_Opinion', label: '📋 Second Opinion', desc: 'Holistic clinical audit of existing biomedical diagnosis and labs.' },
      { id: 'Lifestyle_Support', label: '🌱 Lifestyle (Asbab-e-Sittah)', desc: 'Daily dietary rhythm, breathwork, sleep hygiene, and regimenal coaching.' }
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
            <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Guided Care Discovery</span>
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
              <button onclick="switchRole('clinic'); showNotification('Opening In-Clinic Consultation Booking...', 'info');" class="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-lg transition">
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
    """

    if '// THE ZAYVORA CLINICAL THREAD™ (12-STAGE INTERACTIVE CONTINUUM)' not in html:
        # Insert right before function renderWebsiteApp
        html = html.replace('function renderWebsiteApp(', js_helpers + '\n    function renderWebsiteApp(', 1)
        print("✓ Injected Clinical Thread, Care Discovery Wizard, and Adherence functions")

    # -------------------------------------------------------------
    # 2. Add Clinical Thread Modal HTML to body
    # -------------------------------------------------------------
    modal_html = """
  <!-- CLINICAL THREAD STAGE INSPECTION MODAL -->
  <div id="clinical-thread-modal" class="hidden fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
      <div class="flex justify-between items-center border-b border-[var(--border)] pb-3">
        <h3 id="ct-modal-title" class="font-bold text-base text-white">Stage Details</h3>
        <button onclick="closeClinicalThreadModal()" class="text-[var(--muted)] hover:text-white font-bold text-base">✕</button>
      </div>
      <div id="ct-modal-body"></div>
    </div>
  </div>
    """
    if 'id="clinical-thread-modal"' not in html:
        html = html.replace('</body>', modal_html + '\n</body>', 1)
        print("✓ Injected Clinical Thread Modal into HTML")

    # -------------------------------------------------------------
    # 3. Inject Care Discovery Wizard into Website Home
    # -------------------------------------------------------------
    wizard_placeholder = """
          <!-- Guided Care Discovery Wizard ("What Brings You Here?") -->
          <div id="care-discovery-wizard"></div>
    """
    if 'id="care-discovery-wizard"' not in html:
        # Place right after the hero banner in renderWebsiteApp
        hero_end = '<!-- 6 Clinical Care Areas -->'
        if hero_end in html:
            html = html.replace(hero_end, wizard_placeholder + '\n          ' + hero_end, 1)
            print("✓ Injected Care Discovery Wizard placeholder into website home")

        # Also make sure renderDiscoveryWizard() is called in initWebsiteWaveform or at end of renderWebsiteApp
        init_wave = 'initWebsiteWaveform();'
        if init_wave in html and 'renderDiscoveryWizard();' not in html:
            html = html.replace(init_wave, init_wave + '\n      renderDiscoveryWizard();', 1)
            print("✓ Bound renderDiscoveryWizard() call in renderWebsiteApp")

    # -------------------------------------------------------------
    # 4. Upgrade Clinician "Today" Screen: Exception-First Attention Feed
    # -------------------------------------------------------------
    # Find doctor Today screen and inject the Next Patient Card + Attention Feed
    today_pattern = re.compile(r"if\s*\(state\.tab\s*===\s*'today'\)\s*\{([\s\S]*?)container\.innerHTML\s*=\s*`([\s\S]*?)`;\s*return;\s*\}", re.MULTILINE)
    match = today_pattern.search(html)
    if match:
        today_replacement = """if (state.tab === 'today') {
        container.innerHTML = `
          <div class="space-y-6 pb-10">
            <!-- Welcome Header -->
            <div class="bg-gradient-to-r from-[#1E293B] via-[var(--card)] to-[#0F172A] border border-[var(--border)] rounded-2xl p-5 shadow-lg flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <div class="flex items-center gap-2">
                  <span class="text-xl">🩺</span>
                  <h2 class="text-xl font-extrabold text-white">Hakim Dr. Tariq Mansoor</h2>
                  <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-bold border border-emerald-500/30">OPD Session Active</span>
                </div>
                <p class="text-xs text-[var(--muted)] mt-1">ZAYVORA Integrative Healthcare & Research Centre • Facility ID: <span class="font-mono text-white">ZAY-DEL-01</span></p>
              </div>
              <div class="flex items-center gap-2">
                <button onclick="switchTab('consultation')" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-md transition">
                  Open Clinical Desk™ →
                </button>
              </div>
            </div>

            <!-- PRIMARY CARD: NEXT PATIENT IN QUEUE -->
            <div class="p-6 rounded-2xl bg-gradient-to-r from-emerald-950/60 via-[var(--card)] to-slate-900 border-2 border-emerald-500/50 shadow-xl space-y-4">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-3">
                <div class="flex items-center gap-3">
                  <span class="w-9 h-9 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 flex items-center justify-center font-bold text-sm">
                    01
                  </span>
                  <div>
                    <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">NEXT PATIENT • TOKEN #T-104</span>
                    <h3 class="text-lg font-bold text-white">Hamza Farooqi (42y Male)</h3>
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <span class="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-mono font-bold text-xs border border-emerald-500/30">
                    Ready in Sub-Waiting
                  </span>
                  <span class="text-xs text-[var(--muted)] font-mono">Appt: 10:30 AM</span>
                </div>
              </div>

              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span class="text-[10px] text-[var(--muted)] block">MRN & ABHA</span>
                  <strong class="font-mono text-white">MRN-2026-0008</strong>
                </div>
                <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span class="text-[10px] text-[var(--muted)] block">Chief Concern</span>
                  <strong class="text-white">Knee Osteoarthritis</strong>
                </div>
                <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span class="text-[10px] text-[var(--muted)] block">Baseline Mizaj</span>
                  <strong class="text-emerald-400 font-medium">Barid-Ratab (Cold-Moist)</strong>
                </div>
                <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span class="text-[10px] text-[var(--muted)] block">Triage Priority</span>
                  <span class="text-emerald-400 font-bold">Standard OPD</span>
                </div>
              </div>

              <div class="flex items-center justify-between pt-1">
                <span class="text-xs text-[var(--muted)]">Patient intake vitals and tongue multispectral preview synced from IoT reception desk.</span>
                <button onclick="switchTab('consultation')" class="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-lg transition flex items-center gap-2">
                  <span>Start Consultation</span>
                  <span>→</span>
                </button>
              </div>
            </div>

            <!-- EXCEPTION-FIRST ATTENTION FEED -->
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <span class="text-base">⚠️</span>
                  <h3 class="text-base font-bold text-white">Clinical Attention Feed</h3>
                  <span class="text-[10px] px-2 py-0.5 rounded-full font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">4 Items Requiring Action</span>
                </div>
                <span class="text-xs text-[var(--muted)]">Exception-driven clinical workflow</span>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <!-- Attention Item 1: Lab Result Available -->
                <div class="p-4 rounded-2xl bg-[var(--card)] border border-blue-500/30 space-y-3 shadow-sm">
                  <div class="flex justify-between items-start">
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/15 text-blue-400 border border-blue-500/30">LAB RESULT AVAILABLE</span>
                    <span class="text-[10px] text-[var(--muted)] font-mono">24 mins ago</span>
                  </div>
                  <div>
                    <h4 class="text-sm font-bold text-white">HbA1c & LFT Panel Uploaded — Zaid Khan (MRN-2026-0004)</h4>
                    <p class="text-xs text-[var(--muted)] mt-1"><strong>WHY:</strong> Clinician review required before continuing Phase 2 Munzij-e-Balgham regimen.</p>
                  </div>
                  <div class="flex items-center justify-between pt-1 border-t border-[var(--border)] text-xs">
                    <span class="text-[var(--muted)]">WHEN: Due before 11:00 AM</span>
                    <button onclick="switchTab('patients'); showNotification('Opening investigations panel for Zaid Khan...', 'info');" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg text-xs">
                      Review Labs
                    </button>
                  </div>
                </div>

                <!-- Attention Item 2: Follow-up Due -->
                <div class="p-4 rounded-2xl bg-[var(--card)] border border-emerald-500/30 space-y-3 shadow-sm">
                  <div class="flex justify-between items-start">
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">PHASE MILESTONE DUE</span>
                    <span class="text-[10px] text-[var(--muted)] font-mono">Today 11:45 AM</span>
                  </div>
                  <div>
                    <h4 class="text-sm font-bold text-white">Day 14 Munzij-to-Mushil Transition — Fatima Bi (MRN-2026-0005)</h4>
                    <p class="text-xs text-[var(--muted)] mt-1"><strong>WHY:</strong> Humoral coction (Nujd) achieved in urine sample; verify readiness for purgative expulsion.</p>
                  </div>
                  <div class="flex items-center justify-between pt-1 border-t border-[var(--border)] text-xs">
                    <span class="text-[var(--muted)]">WHEN: Encounter Slot #3</span>
                    <button onclick="switchTab('followups'); showNotification('Opening Day 14 milestone transition note...', 'info');" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg text-xs">
                      Evaluate Nujd
                    </button>
                  </div>
                </div>

                <!-- Attention Item 3: Safety Alert -->
                <div class="p-4 rounded-2xl bg-[var(--card)] border border-amber-500/30 space-y-3 shadow-sm">
                  <div class="flex justify-between items-start">
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/15 text-amber-400 border border-amber-500/30">SCHEDULE E(1) DETOXIFICATION GATE</span>
                    <span class="text-[10px] text-amber-400 font-mono font-bold">High Priority</span>
                  </div>
                  <div>
                    <h4 class="text-sm font-bold text-white">Mudabbar Certificate Release — Suranjan Shirin (Batch #MS-2026-LOT5)</h4>
                    <p class="text-xs text-[var(--muted)] mt-1"><strong>WHY:</strong> Dispensary dispense blocked until chief physician digital signature verifies detoxification certificate.</p>
                  </div>
                  <div class="flex items-center justify-between pt-1 border-t border-[var(--border)] text-xs">
                    <span class="text-[var(--muted)]">WHEN: Immediate (Dispensary Blocked)</span>
                    <button onclick="switchRole('pharmacy'); switchTab('detox');" class="px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white font-bold rounded-lg text-xs">
                      Audit Certificate
                    </button>
                  </div>
                </div>

                <!-- Attention Item 4: Unsigned Encounter -->
                <div class="p-4 rounded-2xl bg-[var(--card)] border border-purple-500/30 space-y-3 shadow-sm">
                  <div class="flex justify-between items-start">
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-purple-500/15 text-purple-400 border border-purple-500/30">21 CFR PART 11 SIGNATURE REQUIRED</span>
                    <span class="text-[10px] text-[var(--muted)] font-mono">Yesterday 17:30</span>
                  </div>
                  <div>
                    <h4 class="text-sm font-bold text-white">Unsealed Encounter #ENC-2026-8941 — Dr. Mansoor</h4>
                    <p class="text-xs text-[var(--muted)] mt-1"><strong>WHY:</strong> Nuskha locked but cryptographic SHA-256 physician PIN seal not yet committed to Merkle ledger.</p>
                  </div>
                  <div class="flex items-center justify-between pt-1 border-t border-[var(--border)] text-xs">
                    <span class="text-[var(--muted)]">WHEN: Statutory 24-hr Deadline</span>
                    <button onclick="switchTab('prescriptions'); showNotification('Opening unsealed prescription for cryptographic signature...', 'info');" class="px-3 py-1.5 bg-purple-600 hover:bg-purple-500 text-white font-bold rounded-lg text-xs">
                      Sign & Seal
                    </button>
                  </div>
                </div>
              </div>
            </div>

          </div>
        `;
        return;
      }"""
        html = html[:match.start()] + today_replacement + html[match.end():]
        print("✓ Upgraded Doctor 'Today' screen to Exception-First Attention Feed")

    # -------------------------------------------------------------
    # 5. Upgrade renderSingleConsultationWorkspace to Clinical Desk™ 3-Zone
    # -------------------------------------------------------------
    # Let's inspect where renderSingleConsultationWorkspace layout starts:
    # <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
    pattern_cw = re.compile(r'<div class="grid grid-cols-1 lg:grid-cols-4 gap-6">([\s\S]*?)<!-- Right Dynamic Clinical Workspace Container -->\s*<div class="lg:col-span-3 space-y-6" id="consultation-section-content">', re.MULTILINE)
    m_cw = pattern_cw.search(html)
    if m_cw:
        new_3zone_head = """<!-- CLINICAL DESK™ 3-ZONE LAYOUT -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
            
            <!-- ZONE 1 (Left 3 cols): Queue, Patient & Canonical Tabs -->
            <div class="lg:col-span-3 space-y-4 text-xs">
              <!-- Mini Patient Card -->
              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-sm space-y-2">
                <div class="flex items-center justify-between border-b border-[var(--border)] pb-2">
                  <span class="text-[10px] font-bold text-emerald-400 uppercase">Active Patient</span>
                  <span class="font-mono text-[10px] text-white px-2 py-0.5 rounded bg-[var(--background)]">#T-104</span>
                </div>
                <div class="space-y-0.5">
                  <h3 class="font-bold text-sm text-white">${state.patient.name}</h3>
                  <p class="text-[11px] text-[var(--muted)]">${state.patient.age}y ${state.patient.gender} • <span class="text-emerald-400">${state.patient.mizaj}</span></p>
                  <p class="text-[10px] font-mono text-[var(--muted)]">MRN: ${state.patient.mrn}</p>
                </div>
              </div>

              <!-- 13 Canonical Navigation Tabs -->
              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-3.5 shadow-sm space-y-1">
                <span class="text-[10px] font-bold text-[var(--muted)] uppercase tracking-wider block px-2 pb-1 border-b border-[var(--border)]">Consultation Steps (13)</span>
                <button onclick="jumpToSection(1)" id="c-step-1" class="consultation-step active w-full text-left px-2.5 py-1.5 rounded-lg border border-transparent">1. Overview</button>
                <button onclick="jumpToSection(2)" id="c-step-2" class="consultation-step w-full text-left px-2.5 py-1.5 rounded-lg border border-transparent text-[var(--muted)] hover:text-white">2. History</button>
                <button onclick="jumpToSection(3)" id="c-step-3" class="consultation-step w-full text-left px-2.5 py-1.5 rounded-lg border border-transparent text-[var(--muted)] hover:text-white">3. Examination</button>
                <button onclick="jumpToSection(4)" id="c-step-4" class="consultation-step w-full text-left px-2.5 py-1.5 rounded-lg border border-transparent text-[var(--muted)] hover:text-white">4. Vitals</button>
                <button onclick="jumpToSection(5)" id="c-step-5" class="consultation-step w-full text-left px-2.5 py-1.5 rounded-lg border border-transparent text-[var(--muted)] hover:text-white">5. Investigations</button>
                <button onclick="jumpToSection(6)" id="c-step-6" class="consultation-step w-full text-left px-2.5 py-1.5 rounded-lg border border-transparent text-[var(--muted)] hover:text-white">6. Assessment</button>
                <button onclick="jumpToSection(7)" id="c-step-7" class="consultation-step w-full text-left px-2.5 py-1.5 rounded-lg border border-transparent text-[var(--muted)] hover:text-white">7. Mizaj</button>
                <button onclick="jumpToSection(8)" id="c-step-8" class="consultation-step w-full text-left px-2.5 py-1.5 rounded-lg border border-transparent text-[var(--muted)] hover:text-white flex items-center justify-between">
                  <span>8. Afaal Cascade</span>
                  <span class="text-[8px] px-1 py-0.2 rounded bg-emerald-500/20 text-emerald-400 font-mono">4-STAGE</span>
                </button>
                <button onclick="jumpToSection(9)" id="c-step-9" class="consultation-step w-full text-left px-2.5 py-1.5 rounded-lg border border-transparent text-[var(--muted)] hover:text-white">9. Axis Mapping</button>
                <button onclick="jumpToSection(10)" id="c-step-10" class="consultation-step w-full text-left px-2.5 py-1.5 rounded-lg border border-transparent text-[var(--muted)] hover:text-white">10. Treatment Plan</button>
                <button onclick="jumpToSection(11)" id="c-step-11" class="consultation-step w-full text-left px-2.5 py-1.5 rounded-lg border border-transparent text-[var(--muted)] hover:text-white">11. Prescription</button>
                <button onclick="jumpToSection(12)" id="c-step-12" class="consultation-step w-full text-left px-2.5 py-1.5 rounded-lg border border-transparent text-[var(--muted)] hover:text-white">12. Follow-up</button>
                <button onclick="jumpToSection(13)" id="c-step-13" class="consultation-step w-full text-left px-2.5 py-1.5 rounded-lg border border-transparent text-[var(--muted)] hover:text-white">13. Timeline</button>
              </div>

              <div class="space-y-2 pt-1">
                <button onclick="saveConsultationDraft()" class="w-full px-3 py-2 rounded-xl border border-[var(--border)] text-xs text-white hover:bg-[var(--background)] transition">
                  💾 Save Draft Note
                </button>
                <button onclick="approvePrescriptionAndLock()" class="w-full px-3 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md transition">
                  🔒 Lock & Sign (21 CFR)
                </button>
              </div>
            </div>

            <!-- ZONE 2 (Center 6 cols): Persistent Clinical Thread™ + Encounter Surface -->
            <div class="lg:col-span-6 space-y-4">
              <!-- Persistent Clinical Thread Ribbon -->
              ${renderClinicalThread('nuskha')}
              
              <!-- Dynamic Clinical Section Surface -->
              <div id="consultation-section-content" class="space-y-6">"""
        
        html = html[:m_cw.start()] + new_3zone_head + html[m_cw.end():]
        print("✓ Upgraded Clinical Desk to 3-Zone structure (Zone 1 & 2)")

        # Now close Zone 2 and insert Zone 3 (Right 3 cols)
        # Search for closing tag of consultation-section-content
        # In old layout: </div> </div> <!-- 5-LAYER HAKEEM SAHAB...
        zone3_html = """</div>
            </div>

            <!-- ZONE 3 (Right 3 cols): Intelligence, Evidence & Permanent Safety Rail -->
            <div class="lg:col-span-3 space-y-4 text-xs">
              
              <!-- PERMANENT SAFETY RAIL -->
              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b border-[var(--border)] pb-2.5">
                  <div class="flex items-center gap-2">
                    <span class="text-sm">🛡️</span>
                    <span class="font-extrabold text-white text-xs tracking-wide">Permanent Safety Rail</span>
                  </div>
                  <span class="px-2 py-0.5 rounded-full text-[9px] font-bold safety-badge-pass">ACTIVE</span>
                </div>

                <div class="space-y-2">
                  <div class="p-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] flex items-center justify-between">
                    <div>
                      <span class="font-semibold text-white block text-[11px]">Allergies & Hypersensitivity</span>
                      <span class="text-[9px] text-[var(--muted)]">No Asteraceae conflicts</span>
                    </div>
                    <span class="px-1.5 py-0.5 rounded text-[9px] font-bold safety-badge-pass">PASS</span>
                  </div>

                  <div class="p-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] flex items-center justify-between">
                    <div>
                      <span class="font-semibold text-white block text-[11px]">CYP450 Herb-Drug Interxn</span>
                      <span class="text-[9px] text-[var(--muted)]">No active enzyme blocks</span>
                    </div>
                    <span class="px-1.5 py-0.5 rounded text-[9px] font-bold safety-badge-pass">PASS</span>
                  </div>

                  <div class="p-2.5 rounded-xl bg-[var(--background)] border border-amber-500/30 flex items-center justify-between">
                    <div>
                      <span class="font-semibold text-white block text-[11px]">Schedule E(1) Mudabbar</span>
                      <span class="text-[9px] text-amber-400">Suranjan requires cert</span>
                    </div>
                    <span class="px-1.5 py-0.5 rounded text-[9px] font-bold safety-badge-caution">CAUTION</span>
                  </div>

                  <div class="p-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] flex items-center justify-between">
                    <div>
                      <span class="font-semibold text-white block text-[11px]">Food Antagonism (Tanafur)</span>
                      <span class="text-[9px] text-[var(--muted)]">No Samak + Laban block</span>
                    </div>
                    <span class="px-1.5 py-0.5 rounded text-[9px] font-bold safety-badge-pass">PASS</span>
                  </div>

                  <div class="p-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] flex items-center justify-between">
                    <div>
                      <span class="font-semibold text-white block text-[11px]">Hemodynamic Pre-req</span>
                      <span class="text-[9px] text-[var(--muted)]">BP 128/82 mmHg ≥ 100</span>
                    </div>
                    <span class="px-1.5 py-0.5 rounded text-[9px] font-bold safety-badge-pass">PASS</span>
                  </div>
                </div>

                <button onclick="showNotification('Safety rails re-evaluated across all 10 clinical safety invariants (SAFETY-001 - 010): 0 BLOCK, 1 CAUTION.', 'info');" class="w-full py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-[10px] text-slate-300 font-semibold transition border border-slate-700">
                  ⚡ Re-evaluate Safety Rails
                </button>
              </div>

              <!-- HAKEEM SAHAB AI DECISION SUPPORT CARD -->
              <div class="bg-[var(--card)] border border-purple-500/30 rounded-2xl p-4 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b border-[var(--border)] pb-2">
                  <div class="flex items-center gap-1.5">
                    <span class="text-sm">🤖</span>
                    <span class="font-bold text-white text-xs">Hakeem Sahab™ AI</span>
                  </div>
                  <span class="px-2 py-0.5 rounded text-[9px] font-mono bg-purple-500/20 text-purple-300 border border-purple-500/30">Uncertainty: 0.08</span>
                </div>
                <div class="p-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] space-y-1">
                  <span class="text-[10px] font-bold text-purple-300 uppercase">Contextual Recommendation</span>
                  <p class="text-[11px] text-[var(--muted)] leading-relaxed">
                    Phase 2 Munzij-e-Balgham indicated. Formulate Hab-e-Suranjan with co-prescribed Roghan-e-Banafsha scalp friction for nocturnal tension.
                  </p>
                </div>
                <div class="flex items-center gap-2">
                  <button onclick="applyHakeemRecommendation()" class="flex-1 py-1.5 bg-purple-600 hover:bg-purple-500 text-white rounded-lg font-bold text-[10px] transition">
                    + Apply to Nuskha
                  </button>
                  <button onclick="toggleHakeemDrawer(true)" class="px-2.5 py-1.5 border border-[var(--border)] text-[var(--muted)] hover:text-white rounded-lg text-[10px] transition">
                    Expand
                  </button>
                </div>
                <span class="text-[9px] text-[var(--muted)] block text-center italic">AI suggests. Clinician decides.</span>
              </div>

              <!-- EVIDENCE & PROVENANCE CARD -->
              <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b border-[var(--border)] pb-2">
                  <div class="flex items-center gap-1.5">
                    <span class="text-sm">📚</span>
                    <span class="font-bold text-white text-xs">Evidence Provenance</span>
                  </div>
                  <span class="text-[9px] font-bold text-emerald-400">Grade A/B</span>
                </div>
                <div class="space-y-1.5 text-[10px] text-[var(--muted)]">
                  <div class="flex justify-between p-1.5 rounded bg-[var(--background)]">
                    <span class="text-white font-medium">Suranjan Shirin</span>
                    <span class="font-mono text-emerald-400">UPI Vol I, p.112</span>
                  </div>
                  <div class="flex justify-between p-1.5 rounded bg-[var(--background)]">
                    <span class="text-white font-medium">Asgandh Nagori</span>
                    <span class="font-mono text-emerald-400">UPI Vol I, p.15</span>
                  </div>
                  <div class="flex justify-between p-1.5 rounded bg-[var(--background)]">
                    <span class="text-white font-medium">Kitab al-Aghziya</span>
                    <span class="font-mono text-emerald-400">Ibn Zuhr, 1162 AD</span>
                  </div>
                </div>
                <button onclick="switchRole('website'); switchTab('knowledge');" class="w-full py-1.5 border border-[var(--border)] rounded-lg text-[10px] text-slate-300 hover:text-white hover:bg-[var(--background)] transition">
                  Browse ZKB Pharmacopoeia →
                </button>
              </div>

            </div>

          </div>"""

        # In old html, find the end of consultation-section-content div
        # It was: <!-- 5-LAYER HAKEEM SAHAB AI COPILOT DRAWER -->
        old_drawer_marker = '<!-- 5-LAYER HAKEEM SAHAB AI COPILOT DRAWER -->'
        idx_dm = html.find(old_drawer_marker)
        # Search backward for the two closing </div></div>
        idx_close = html.rfind('</div>', 0, idx_dm)
        idx_close2 = html.rfind('</div>', 0, idx_close)
        html = html[:idx_close2] + zone3_html + '\n\n          ' + html[idx_dm:]
        print("✓ Injected Zone 3 (Safety Rail, Hakeem, Evidence) into Clinical Desk")

    # -------------------------------------------------------------
    # 6. Save updated index.html & sync docs/index.html
    # -------------------------------------------------------------
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Successfully updated index.html and docs/index.html")

if __name__ == '__main__':
    run()
