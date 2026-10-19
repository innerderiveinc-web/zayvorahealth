// =========================================================================
// ZAYVORA FUNCTIONAL MEDICINE & TIBB-E-UNANI FUSION SUITE
// 1. Hazm-e-Arba'a (4-Stage Digestion & Detox Analyzer)
// 2. Functional ATM Timeline (Antecedents, Triggers, Mediators)
// 3. Circadian Humoral Bio-Clock (24h Chrono-Therapeutics)
// 4. Gut-Brain Axis & Vagus Nerve Correlator (Maraq-e-Meda)
// 5. Toxic Burden & Cellular Tanqiya Readiness Index
// =========================================================================

    // ── 1. HAZM-E-ARBA'A (4-STAGE METABOLIC DIGESTION ANALYZER) ────────────
    window.activeHazmStage = 'medi';
    window.hazmStagesData = [
      {
        id: 'medi',
        stageNumber: 'Stage 1',
        name: 'Hazm-e-M\'edi (Gastric & Upper Gut Digestion)',
        arabic: 'ہضمِ معدی — کائلوس (Chyme)',
        biologicalRole: 'Acidification, enzymatic cleaving of peptides, and transformation of food bolus into Chyme (Kailoos).',
        stasisSigns: ['Post-prandial heaviness & early satiety', 'Acid regurgitation / sour belching (Hamuzat)', 'Epigastric bloating within 30 min of eating', 'Undigested food residues in stool'],
        underlyingDyscrasia: 'Zo\'af-e-Meda & Su-e-Mizaj Barid (Hypochlorhydria & Cold Gastric Weakness)',
        correctionRoadmap: 'Chew 1 slice fresh Ginger with rock salt 10 min prior to meals. Sip warm cumin water; strictly avoid iced water with meals.',
        recommendedSku: 'ZAY-003',
        recommendedProduct: 'ZAYVORA LiverPrime Core™ (with Jawarish formulation)'
      },
      {
        id: 'kabidi',
        stageNumber: 'Stage 2',
        name: 'Hazm-e-Kabidi (Hepatic Transamination & Humoral Genesis)',
        arabic: 'ہضمِ کبدی — پیدائشِ اخلاط و کائموس (Chyle)',
        biologicalRole: 'Portal venous nutrient uptake, Phase-I & II biotransformation, and synthesis of the 4 humors (Dam, Balgham, Safra, Sawda).',
        stasisSigns: ['Right upper quadrant fullness / sluggishness', 'Elevated ALT/SGPT or bilirubin', 'Bitter morning taste & yellowish tongue fur', 'Nausea after fatty or heavy foods'],
        underlyingDyscrasia: 'Sudda-e-Kabid & Su-e-Mizaj Har Safrawi (Hepato-Biliary Stasis & Bilious Inflammation)',
        correctionRoadmap: 'Drink Chicory seed infusion (Bekh-e-Kasni) and Revand Chini decoction. Replace refined oils with extra virgin cold-pressed olive oil.',
        recommendedSku: 'ZAY-003',
        recommendedProduct: 'ZAYVORA LiverPrime Core™'
      },
      {
        id: 'uroogi',
        stageNumber: 'Stage 3',
        name: 'Hazm-e-Uroogi (Vascular & Microvascular Digestion)',
        arabic: 'ہضمِ عروقی — انتقال و تغذیہ بذریعہ شریان',
        biologicalRole: 'Endothelial transport, capillary nutrient exchange, and removal of nitrogenous waste across the macro/micro-vasculature.',
        stasisSigns: ['Elevated triglycerides or LDL cholesterol', 'Sluggish capillary refill & cold extremities', 'Heavy legs with dependent evening edema', 'Elevated arterial stiffness / pulse tension'],
        underlyingDyscrasia: 'Lazoojat-e-Dam & Ihtibas-e-Balgham (Vascular Viscosity & Endothelial Stasis)',
        correctionRoadmap: 'Consume Allium sativum (Seer/Garlic) with lukewarm water. Daily 30 min brisk metabolic walk to stimulate vascular shear stress.',
        recommendedSku: 'ZAY-001',
        recommendedProduct: 'ZAYVORA TensioCalm™'
      },
      {
        id: 'uzwi',
        stageNumber: 'Stage 4',
        name: 'Hazm-e-Uzwi (Cellular, Mitochondrial & Tissue Assimilation)',
        arabic: 'ہضمِ عضوی — جزوِ بدن بننا اور فضلات کا اخراج',
        biologicalRole: 'Mitochondrial ATP synthesis, cellular repair, synthesis of intracellular matrix, and micro-waste (Fuzlaat-e-Uzwiyah) clearance.',
        stasisSigns: ['Unrelenting cellular fatigue despite 8 hrs sleep', 'Elevated serum uric acid / joint stiffness', 'Brain fog and delayed cognitive processing', 'Poor tissue healing and chronic muscular soreness'],
        underlyingDyscrasia: 'Ihtibas-e-Fuzlaat-e-Uzwiyah & Nuqs-e-Hararat-e-Ghariziyah (Cellular Toxin Congestion & Mitochondrial Weakness)',
        correctionRoadmap: 'Fasting intervals (14-hour intermittent sawm) to induce autophagy. Administer Withania somnifera (Asgandh) and Curcuma longa.',
        recommendedSku: 'ZAY-007',
        recommendedProduct: 'ZAYVORA VitaMani Max™'
      }
    ];

    function toggleHazmArbaModal(show = true) {
      const modal = document.getElementById('hazm-arba-modal');
      if (!modal) return;
      if (show) {
        renderHazmArba();
        modal.classList.remove('hidden');
      } else {
        modal.classList.add('hidden');
      }
    }

    function renderHazmArba() {
      const container = document.getElementById('hazm-arba-content');
      if (!container) return;
      const stage = window.hazmStagesData.find(s => s.id === window.activeHazmStage) || window.hazmStagesData[0];

      container.innerHTML = `
        <div class="space-y-6">
          <!-- Intro Banner -->
          <div class="p-4 rounded-2xl bg-emerald-950/30 border border-emerald-500/30 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
            <div>
              <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-wider">ZAYVORA Metabolic Assimilation &amp; Biotransformation Engine</span>
              <h4 class="text-sm font-bold text-white">Hazm-e-Arba'a: The 4 Cascades of Greco-Arab Metabolism</h4>
              <p class="text-[11px] text-slate-300">In Tibb-e-Unani, disease begins when metabolic waste (Fuzlaat) is halted at one of the four stages of digestion.</p>
            </div>
            <span class="px-3 py-1 rounded-xl bg-emerald-500/20 text-emerald-300 font-mono text-xs font-bold whitespace-nowrap">
              Active: ${stage.stageNumber}
            </span>
          </div>

          <!-- Stage Selection Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
            ${window.hazmStagesData.map(s => `
              <button onclick="window.activeHazmStage='${s.id}'; renderHazmArba();" class="p-3 rounded-2xl border text-left transition flex flex-col justify-between ${s.id === stage.id ? 'bg-emerald-600 text-white border-emerald-400 shadow-lg ring-2 ring-emerald-500/50' : 'bg-slate-800/80 hover:bg-slate-800 text-slate-300 border-slate-700'}">
                <span class="text-[10px] font-mono font-bold opacity-80 uppercase">${s.stageNumber}</span>
                <span class="text-xs font-bold mt-1 line-clamp-1">${s.name.split(' ')[0]}</span>
                <span class="text-[10px] opacity-75 mt-0.5">${s.arabic.split('—')[0]}</span>
              </button>
            `).join('')}
          </div>

          <!-- Active Stage Clinical Deep-Dive -->
          <div class="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-4">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
              <div>
                <h3 class="text-base font-bold text-white flex items-center gap-2">
                  <span>${stage.name}</span>
                </h3>
                <span class="text-xs text-emerald-400 font-serif">${stage.arabic}</span>
              </div>
              <span class="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 font-mono text-[11px]">
                ${stage.stageNumber} of 4
              </span>
            </div>

            <div>
              <span class="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-wider block mb-1">Biological &amp; Physiological Function:</span>
              <p class="text-xs text-slate-200 leading-relaxed">${stage.biologicalRole}</p>
            </div>

            <!-- Stasis Symptoms -->
            <div>
              <span class="text-[10px] font-mono font-bold text-rose-400 uppercase tracking-wider block mb-2">Hallmark Clinical Signs of Stasis (Impaired Hazm):</span>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                ${stage.stasisSigns.map(sign => `
                  <div class="p-2.5 rounded-xl bg-rose-950/20 border border-rose-500/30 text-rose-200 text-xs flex items-center gap-2">
                    <span class="text-rose-400">⚠️</span>
                    <span>${sign}</span>
                  </div>
                `).join('')}
              </div>
            </div>

            <!-- Root Cause & Correction -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span class="text-[10px] font-mono text-cyan-400 font-bold uppercase tracking-wider block">Greco-Arab Etiology (Su-e-Mizaj):</span>
                <p class="text-xs text-slate-200 font-medium">${stage.underlyingDyscrasia}</p>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-900 border border-emerald-500/30 space-y-1">
                <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-wider block">Dietary &amp; Lifestyle Correction:</span>
                <p class="text-xs text-slate-200">${stage.correctionRoadmap}</p>
              </div>
            </div>

            <!-- Matched Formulation -->
            <div class="p-4 rounded-xl bg-emerald-950/30 border border-emerald-500/40 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
              <div>
                <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-wider block">Standardized Integrative Formulation:</span>
                <span class="text-sm font-bold text-white">${stage.recommendedProduct}</span>
              </div>
              <div class="flex gap-2 w-full sm:w-auto">
                <button onclick="addToHerbalsCart('${stage.recommendedSku.toLowerCase()}'); toggleHazmArbaModal(false); toggleCheckoutModal();" class="flex-1 sm:flex-initial px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition">
                  Order Protocol
                </button>
                <button onclick="openProductQuickView('${stage.recommendedSku}')" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs rounded-xl border border-slate-700 transition">
                  View Monograph
                </button>
              </div>
            </div>

          </div>
        </div>
      `;
    }
    window.toggleHazmArbaModal = toggleHazmArbaModal;
    window.renderHazmArba = renderHazmArba;


    // ── 2. FUNCTIONAL ATM TIMELINE BUILDER (SANIHA-E-MARAZ) ────────────────
    window.atmSelectedAntecedent = 'mizaj_barid';
    window.atmSelectedTrigger = 'antibiotics';
    window.atmSelectedMediator = 'stress_sleep';

    const atmAntecedents = [
      { id: 'mizaj_barid', label: 'Congenital Cold/Moist Mizaj (Balghami Constitution)', detail: 'Sluggish baseline metabolic rate, prone to fluid accumulation, weak digestion.' },
      { id: 'mizaj_har', label: 'Congenital Hot/Dry Mizaj (Safrawi Constitution)', detail: 'Rapid burn-out, prone to systemic acidity, gastritis, and bile overheating.' },
      { id: 'family_metabolic', label: 'Familial Diathesis (Cardio-Metabolic Lineage)', detail: 'Transgenerational tendency toward insulin resistance, hypertension, and hyperuricemia.' }
    ];

    const atmTriggers = [
      { id: 'antibiotics', label: 'Severe Infection / Prolonged Antibiotic Course', detail: 'Eradicated commensal microflora, provoked Leaky Gut, and precipitated secondary Zo\'af-e-Meda.' },
      { id: 'psychic_grief', label: 'Severe Psychic Shock / Grief (Sadma-e-Nafsani)', detail: 'Depleted innate vital energy (Hararat-e-Ghariziyah), causing hypothalamic-pituitary dysregulation.' },
      { id: 'viral_insult', label: 'Post-Viral Fatigue / Endothelial Inflammatory Spike', detail: 'Left lingering latent heat (Hararat-e-Ghariba) and microvascular stasis.' }
    ];

    const atmMediators = [
      { id: 'stress_sleep', label: 'Circadian Disruption & High Cortisol (Naum wa Yaqza Disrupted)', detail: 'Sleeping after midnight prevents nocturnal glymphatic cleansing and surges morning inflammatory cytokines.' },
      { id: 'diet_mixing', label: 'Improper Food Combining (Taqfeem & Processed Sugars)', detail: 'Consuming cold liquids with heavy meals paralyzes gastric pepsins and promotes fermentation.' },
      { id: 'sedentary', label: 'Sedentary Lifestyle (Qillat-e-Harkat-e-Badani)', detail: 'Absence of muscular contraction stops lymphatic clearance, perpetuating morbid humoral stagnation.' }
    ];

    function toggleAtmTimelineModal(show = true) {
      const modal = document.getElementById('atm-timeline-modal');
      if (!modal) return;
      if (show) {
        renderAtmTimeline();
        modal.classList.remove('hidden');
      } else {
        modal.classList.add('hidden');
      }
    }

    function renderAtmTimeline() {
      const container = document.getElementById('atm-timeline-content');
      if (!container) return;

      const curA = atmAntecedents.find(a => a.id === window.atmSelectedAntecedent) || atmAntecedents[0];
      const curT = atmTriggers.find(t => t.id === window.atmSelectedTrigger) || atmTriggers[0];
      const curM = atmMediators.find(m => m.id === window.atmSelectedMediator) || atmMediators[0];

      container.innerHTML = `
        <div class="space-y-6">
          <div class="p-4 rounded-2xl bg-indigo-950/30 border border-indigo-500/30">
            <span class="text-[10px] font-mono text-indigo-400 font-bold uppercase tracking-wider">ZAYVORA Chronological Genesis Timeline (Saniha-e-Maraz Standard)</span>
            <h4 class="text-sm font-bold text-white">Saniha-e-Maraz: Antecedents, Triggers &amp; Mediators</h4>
            <p class="text-[11px] text-slate-300">Map how your illness evolved over decades from predisposing genetics to the trigger event and ongoing daily mediators.</p>
          </div>

          <!-- Step 1: Antecedents -->
          <div class="space-y-2">
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded-full bg-indigo-600 text-white font-bold text-xs flex items-center justify-center">1</span>
              <h5 class="text-xs font-bold text-white uppercase tracking-wider">Antecedent (Your Predisposition / Mizaj-e-Asli)</h5>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
              ${atmAntecedents.map(a => `
                <button onclick="window.atmSelectedAntecedent='${a.id}'; renderAtmTimeline();" class="p-3 rounded-xl border text-left transition ${a.id === curA.id ? 'bg-indigo-600 text-white border-indigo-400 ring-2 ring-indigo-500/50' : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-750'}">
                  <div class="font-bold text-xs">${a.label}</div>
                  <div class="text-[10px] opacity-80 mt-1">${a.detail}</div>
                </button>
              `).join('')}
            </div>
          </div>

          <!-- Step 2: Triggers -->
          <div class="space-y-2">
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded-full bg-rose-600 text-white font-bold text-xs flex items-center justify-center">2</span>
              <h5 class="text-xs font-bold text-white uppercase tracking-wider">Trigger (The Inciting Shock / Asbab-e-Badi'ah)</h5>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
              ${atmTriggers.map(t => `
                <button onclick="window.atmSelectedTrigger='${t.id}'; renderAtmTimeline();" class="p-3 rounded-xl border text-left transition ${t.id === curT.id ? 'bg-rose-600 text-white border-rose-400 ring-2 ring-rose-500/50' : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-750'}">
                  <div class="font-bold text-xs">${t.label}</div>
                  <div class="text-[10px] opacity-80 mt-1">${t.detail}</div>
                </button>
              `).join('')}
            </div>
          </div>

          <!-- Step 3: Mediators -->
          <div class="space-y-2">
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded-full bg-amber-600 text-white font-bold text-xs flex items-center justify-center">3</span>
              <h5 class="text-xs font-bold text-white uppercase tracking-wider">Mediator (The Daily Perpetuating Insult / Asbab-e-Wasita)</h5>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
              ${atmMediators.map(m => `
                <button onclick="window.atmSelectedMediator='${m.id}'; renderAtmTimeline();" class="p-3 rounded-xl border text-left transition ${m.id === curM.id ? 'bg-amber-600 text-white border-amber-400 ring-2 ring-amber-500/50' : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-750'}">
                  <div class="font-bold text-xs">${m.label}</div>
                  <div class="text-[10px] opacity-80 mt-1">${m.detail}</div>
                </button>
              `).join('')}
            </div>
          </div>

          <!-- Clinical Synthesis Card -->
          <div class="p-5 rounded-2xl bg-slate-950 border border-indigo-500/40 space-y-3">
            <div class="flex justify-between items-center border-b border-slate-800 pb-2">
              <span class="text-xs font-bold text-indigo-300">Synthesized Clinical Illness Trajectory</span>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300">READY FOR CONSULTATION</span>
            </div>
            <p class="text-xs text-slate-200 leading-relaxed">
              Your chronic presentation originated from a <strong>${curA.label}</strong>, was precipitated by a <strong>${curT.label}</strong>, and is currently locked into chronic low-grade inflammation by <strong>${curM.label}</strong>.
            </p>
            <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-[11px] text-slate-300">
              <strong class="text-emerald-400">Dr. Irfan Ashraf's Reversal Strategy:</strong> To break this chronicity loop, modern pharmacology merely masks symptoms. In classical Tibb, we immediately dismantle the <em>Mediator</em> through targeted Asbab-e-Sitta lifestyle modifications, neutralize the cellular residue of the <em>Trigger</em>, and reinforce your constitutional <em>Antecedent</em>.
            </div>
            <div class="pt-2 flex flex-col sm:flex-row gap-2">
              <a href="https://wa.me/919773882657?text=${encodeURIComponent(`Salam Dr. Irfan Ashraf, I created my ATM Functional Timeline on ZAYVORA Health OS. Antecedent: ${curA.label}, Trigger: ${curT.label}, Mediator: ${curM.label}. Please review my clinical trajectory.`)}" target="_blank" class="flex-1 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition text-center">
                Send Timeline to Dr. Irfan Ashraf on WhatsApp
              </a>
              <button onclick="toggleAtmTimelineModal(false); toggleCheckoutModal();" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs rounded-xl border border-slate-700 transition">
                Order Protocol
              </button>
            </div>
          </div>

        </div>
      `;
    }
    window.toggleAtmTimelineModal = toggleAtmTimelineModal;
    window.renderAtmTimeline = renderAtmTimeline;


    // ── 3. CIRCADIAN HUMORAL BIO-CLOCK (CHRONO-THERAPEUTICS) ───────────────
    function getActiveHumoralHourData() {
      const hour = new Date().getHours();
      if (hour >= 6 && hour < 12) {
        return {
          windowName: 'Morning Phase (06:00 – 12:00)',
          humor: 'Khilt-e-Dam (Sanguine / Blood)',
          element: 'Air (Hawa) — Hot & Moist (Har Ratab)',
          color: 'rose',
          peakPower: 'Optimal Physical Energy & Arterial Circulation',
          dietDirective: 'Hearty protein-rich breakfast, warm herbal teas with Saffron or Cardamom. Avoid excess dry cooling foods.',
          bestMedicationTime: 'Cardio-protective tonics, vital adaptogens (Asgandh), and vitalizing infusions.',
          caution: 'Avoid intense hot arguments or acute physical exhaustion; blood pressure naturally ascends during this window.'
        };
      } else if (hour >= 12 && hour < 18) {
        return {
          windowName: 'Afternoon Phase (12:00 – 18:00)',
          humor: 'Khilt-e-Safra (Bilious / Yellow Bile)',
          element: 'Fire (Aag) — Hot & Dry (Har Yabis)',
          color: 'amber',
          peakPower: 'Peak Digestive Fire (Hararat-e-Ghariziyah) & Gastric Breakdown',
          dietDirective: 'Consume the main substantial meal of the day now. Digestion operates at maximum enzymic potency.',
          bestMedicationTime: 'Hepato-protective bitters, LiverPrime Core™, and digestive carminatives (Jawarish Kamuni).',
          caution: 'Avoid spicy, oily, deep-fried snacks; excess chili now over-ignites bile and triggers acid reflux.'
        };
      } else if (hour >= 18 && hour < 24) {
        return {
          windowName: 'Evening Phase (18:00 – 24:00)',
          humor: 'Khilt-e-Sawda (Melancholic / Black Bile)',
          element: 'Earth (Matti) — Cold & Dry (Barid Yabis)',
          color: 'indigo',
          peakPower: 'Sensory Wind-Down, Splenic Filtration & Structural Solidification',
          dietDirective: 'Light warm dinner before 20:00 (Warm soups, steamed squash, barley porridge). Avoid heavy beef or lentils.',
          bestMedicationTime: 'Nervine sedatives, NeuroCalmX™, chamomile or lavender infusions to subdue melancholy and cortisol.',
          caution: 'Cease digital screens and intense mental rumination; Sawda surges provoke over-thinking and insomnia.'
        };
      } else {
        return {
          windowName: 'Night / Dawn Phase (00:00 – 06:00)',
          humor: 'Khilt-e-Balgham (Phlegmatic / Phlegm)',
          element: 'Water (Pani) — Cold & Moist (Barid Ratab)',
          color: 'cyan',
          peakPower: 'Deep Cellular Restoration, Lymphatic Glymphatic Cleansing & Tissue Hydration',
          dietDirective: 'Zero ingestion during this regenerative circadian fast. Allow gastric mucosa complete reparative rest.',
          bestMedicationTime: 'Uninterrupted deep restorative sleep (Naum) allowing natural innate intelligence (Tabi\'at) to govern.',
          caution: 'Waking or eating at 02:00 paralyzes lymphatic clearance and causes heavy morning puffiness.'
        };
      }
    }

    function toggleHumoralClockModal(show = true) {
      const modal = document.getElementById('humoral-clock-modal');
      if (!modal) return;
      if (show) {
        renderHumoralClock();
        modal.classList.remove('hidden');
      } else {
        modal.classList.add('hidden');
      }
    }

    function renderHumoralClock() {
      const container = document.getElementById('humoral-clock-content');
      if (!container) return;

      const active = getActiveHumoralHourData();
      const now = new Date();
      const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      container.innerHTML = `
        <div class="space-y-6">
          <!-- Live Time Display -->
          <div class="p-5 rounded-2xl bg-gradient-to-r from-amber-950/40 to-slate-900 border border-amber-500/40 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-emerald-400 animate-ping"></span>
                <span class="text-xs font-mono font-bold text-amber-300 uppercase tracking-wider">LIVE CHRONO-THERAPEUTICS ENGINE</span>
              </div>
              <h4 class="text-lg font-bold text-white mt-1">Current Active Window: ${active.windowName}</h4>
              <p class="text-xs text-slate-300">Local Time: <span class="font-mono text-emerald-400 font-bold">${timeStr}</span> • Diurnal Humoral Cycle</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 text-center">
              <span class="text-[10px] font-mono text-slate-400 block uppercase">DOMINANT HUMOR</span>
              <span class="text-sm font-extrabold text-white">${active.humor.split(' ')[0]}</span>
            </div>
          </div>

          <!-- 4 Diurnal Quadrants Visualizer -->
          <div class="grid grid-cols-1 sm:grid-cols-4 gap-2.5">
            <div class="p-3 rounded-xl border ${new Date().getHours() >= 6 && new Date().getHours() < 12 ? 'bg-rose-950/60 border-rose-500 ring-2 ring-rose-500/50' : 'bg-slate-900 border-slate-800 opacity-60'}">
              <span class="text-[10px] font-mono text-rose-400 font-bold block">06:00 – 12:00</span>
              <div class="font-bold text-xs text-white mt-0.5">Khilt-e-Dam</div>
              <div class="text-[10px] text-slate-400">Blood / Circulation</div>
            </div>
            <div class="p-3 rounded-xl border ${new Date().getHours() >= 12 && new Date().getHours() < 18 ? 'bg-amber-950/60 border-amber-500 ring-2 ring-amber-500/50' : 'bg-slate-900 border-slate-800 opacity-60'}">
              <span class="text-[10px] font-mono text-amber-400 font-bold block">12:00 – 18:00</span>
              <div class="font-bold text-xs text-white mt-0.5">Khilt-e-Safra</div>
              <div class="text-[10px] text-slate-400">Bile / Digestion</div>
            </div>
            <div class="p-3 rounded-xl border ${new Date().getHours() >= 18 && new Date().getHours() < 24 ? 'bg-indigo-950/60 border-indigo-500 ring-2 ring-indigo-500/50' : 'bg-slate-900 border-slate-800 opacity-60'}">
              <span class="text-[10px] font-mono text-indigo-400 font-bold block">18:00 – 24:00</span>
              <div class="font-bold text-xs text-white mt-0.5">Khilt-e-Sawda</div>
              <div class="text-[10px] text-slate-400">Nervous / Calm</div>
            </div>
            <div class="p-3 rounded-xl border ${new Date().getHours() >= 0 && new Date().getHours() < 6 ? 'bg-cyan-950/60 border-cyan-500 ring-2 ring-cyan-500/50' : 'bg-slate-900 border-slate-800 opacity-60'}">
              <span class="text-[10px] font-mono text-cyan-400 font-bold block">00:00 – 06:00</span>
              <div class="font-bold text-xs text-white mt-0.5">Khilt-e-Balgham</div>
              <div class="text-[10px] text-slate-400">Lymphatic Detox</div>
            </div>
          </div>

          <!-- Real-Time Clinical Directives -->
          <div class="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-4">
            <h5 class="text-xs font-bold text-white uppercase tracking-wider border-b border-slate-800 pb-2">
              Action Directives for This Exact Hour
            </h5>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-wider block">🍽️ Nutritional Timing Right Now:</span>
                <p class="text-xs text-slate-200">${active.dietDirective}</p>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span class="text-[10px] font-mono text-cyan-400 font-bold uppercase tracking-wider block">💊 Optimal Botanical Bio-Availability:</span>
                <p class="text-xs text-slate-200">${active.bestMedicationTime}</p>
              </div>
            </div>

            <div class="p-3.5 rounded-xl bg-rose-950/20 border border-rose-500/30 text-rose-200 text-xs flex items-center gap-2">
              <span class="text-rose-400 text-base">⚠️</span>
              <div>
                <strong>Circadian Contraindication:</strong> ${active.caution}
              </div>
            </div>
          </div>

        </div>
      `;
    }
    window.toggleHumoralClockModal = toggleHumoralClockModal;
    window.renderHumoralClock = renderHumoralClock;


    // ── 4. GUT-BRAIN AXIS & VAGUS NERVE SCREENER (MARAQ-E-MEDA) ─────────────
    window.gutBrainAnswers = { q1: false, q2: false, q3: false, q4: false, q5: false };

    function toggleGutBrainModal(show = true) {
      const modal = document.getElementById('gut-brain-modal');
      if (!modal) return;
      if (show) {
        renderGutBrain();
        modal.classList.remove('hidden');
      } else {
        modal.classList.add('hidden');
      }
    }

    function renderGutBrain() {
      const container = document.getElementById('gut-brain-content');
      if (!container) return;

      const questions = [
        { key: 'q1', text: 'Do you experience brain fog, grogginess, or loss of mental sharpness 30–60 minutes after meals?' },
        { key: 'q2', text: 'Does abdominal bloating, distension, or gas coincide with heightened anxiety or racing thoughts?' },
        { key: 'q3', text: 'Do you wake up between 02:00 and 04:00 AM with abdominal discomfort, heart pounding, or tension?' },
        { key: 'q4', text: 'Does persistent constipation or sluggish bowels make you feel irritable, gloomy, or emotionally flat?' },
        { key: 'q5', text: 'Do you suffer from cold extremities, epigastric spasms, or sudden sour belches during stressful periods?' }
      ];

      const yesCount = Object.values(window.gutBrainAnswers).filter(Boolean).length;
      const score = Math.round((yesCount / 5) * 100);

      container.innerHTML = `
        <div class="space-y-6">
          <div class="p-4 rounded-2xl bg-rose-950/30 border border-rose-500/30">
            <span class="text-[10px] font-mono text-rose-400 font-bold uppercase tracking-wider">Functional Neuro-Gastroenterology &amp; Classical Tibb</span>
            <h4 class="text-sm font-bold text-white">Maraq-e-Meda: The Gut-Brain Vagus Nerve Axis</h4>
            <p class="text-[11px] text-slate-300">Discover whether your mood swings, brain fog, or panic sensations are caused by toxic vapors (Bukharat-e-Meda) ascending via the vagus nerve.</p>
          </div>

          <!-- Question Checklist -->
          <div class="space-y-2.5">
            ${questions.map((q, idx) => `
              <div onclick="window.gutBrainAnswers['${q.key}'] = !window.gutBrainAnswers['${q.key}']; renderGutBrain();" class="p-3.5 rounded-xl border transition flex items-center justify-between cursor-pointer ${window.gutBrainAnswers[q.key] ? 'bg-rose-950/40 border-rose-500 text-white' : 'bg-slate-900 border-slate-800 text-slate-300 hover:bg-slate-850'}">
                <div class="flex items-center gap-3">
                  <span class="w-6 h-6 rounded-full bg-slate-800 text-slate-300 font-mono text-xs flex items-center justify-center font-bold">${idx + 1}</span>
                  <span class="text-xs">${q.text}</span>
                </div>
                <span class="text-base">${window.gutBrainAnswers[q.key] ? '✅' : '⚪'}</span>
              </div>
            `).join('')}
          </div>

          <!-- Result Evaluation -->
          <div class="p-5 rounded-2xl bg-slate-950 border border-rose-500/40 space-y-3">
            <div class="flex justify-between items-center border-b border-slate-800 pb-2">
              <span class="text-xs font-bold text-white">Vagal-Gut Fermentation Score: <strong class="text-rose-400">${score}%</strong></span>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded ${score >= 60 ? 'bg-rose-500/20 text-rose-300' : 'bg-emerald-500/20 text-emerald-300'} font-bold">
                ${score >= 60 ? 'HIGH GUT-BRAIN DYSBIOSIS' : 'MILD / BALANCED'}
              </span>
            </div>

            <p class="text-xs text-slate-200 leading-relaxed">
              ${score >= 60 
                ? 'Your responses confirm classical <strong>Maraq-e-Meda</strong> (Gut-Induced Neurosis). Microbial fermentation and putrefaction in your gastrointestinal tract release endotoxins and inflammatory metabolites that ascend via the vagus nerve (Aasab) to trigger cerebral neuro-inflammation.'
                : 'Your enteric nervous system and gastric vagal tone are relatively stable. Minor digestive bloating is unlikely to be driving significant cognitive or neurological symptoms.'}
            </p>

            <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-[11px] text-slate-300">
              <strong class="text-cyan-400">Classical Treatment Protocol:</strong> Carminative gastric carminatives (Jawarish Kamuni / GastroNorm) + Aniseed &amp; Ajwain decoction. Eliminate fermentable dairy and ultra-processed seed oils for 21 days.
            </div>

            <div class="pt-2 flex flex-col sm:flex-row gap-2">
              <button onclick="addToHerbalsCart('zay-003'); toggleGutBrainModal(false); toggleCheckoutModal();" class="flex-1 py-2.5 bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs rounded-xl shadow transition">
                Order Gastro-Vagal Protocol (ZAY-003)
              </button>
              <button onclick="toggleGutBrainModal(false); toggleLabCorrelatorModal(true);" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs rounded-xl border border-slate-700 transition">
                Correlate with Blood Labs
              </button>
            </div>
          </div>

        </div>
      `;
    }
    window.toggleGutBrainModal = toggleGutBrainModal;
    window.renderGutBrain = renderGutBrain;


    // ── 5. TOXIC BURDEN & CELLULAR TANQIYA READINESS INDEX ──────────────────
    window.tanqiyaAnswers = { t1: false, t2: false, t3: false, t4: false, t5: false };

    function toggleTanqiyaReadinessModal(show = true) {
      const modal = document.getElementById('tanqiya-readiness-modal');
      if (!modal) return;
      if (show) {
        renderTanqiyaReadiness();
        modal.classList.remove('hidden');
      } else {
        modal.classList.add('hidden');
      }
    }

    function renderTanqiyaReadiness() {
      const container = document.getElementById('tanqiya-readiness-content');
      if (!container) return;

      const checks = [
        { key: 't1', title: 'Incomplete Bowel Evacuation (Ihtibas)', desc: 'Infrequent, hard, or incomplete daily stool evacuation.' },
        { key: 't2', title: 'Thick Tongue Coating (Saburrah)', desc: 'White, yellow, or grey pasty film on the dorsal surface of the tongue upon waking.' },
        { key: 't3', title: 'Turbid / Pungent Urine (Taffun-e-Bawl)', desc: 'Dark amber or cloudy urine with noticeable strong odor despite hydration.' },
        { key: 't4', title: 'Environmental / Chemical Exposure', desc: 'Frequent intake of commercial pharmaceuticals, pesticide residues, or city pollution.' },
        { key: 't5', title: 'Post-Meal Sluggishness & Heaviness', desc: 'Feeling weighed down, mentally dull, or physically heavy throughout the day.' }
      ];

      const count = Object.values(window.tanqiyaAnswers).filter(Boolean).length;
      const requiresTanqiya = count >= 3;

      container.innerHTML = `
        <div class="space-y-6">
          <div class="p-4 rounded-2xl bg-teal-950/30 border border-teal-500/30">
            <span class="text-[10px] font-mono text-teal-400 font-bold uppercase tracking-wider">Unani Toxicology &amp; Phase-II Detoxification</span>
            <h4 class="text-sm font-bold text-white">Tanqiya Readiness: Do You Need Cleansing Before Tonics?</h4>
            <p class="text-[11px] text-slate-300">The classical doctrine warns: <em>"Administering restorative tonics to a toxic, congested body only feeds the morbid humors."</em> Check your symptoms below.</p>
          </div>

          <!-- Checks -->
          <div class="space-y-2.5">
            ${checks.map((c, idx) => `
              <div onclick="window.tanqiyaAnswers['${c.key}'] = !window.tanqiyaAnswers['${c.key}']; renderTanqiyaReadiness();" class="p-3.5 rounded-xl border transition flex items-center justify-between cursor-pointer ${window.tanqiyaAnswers[c.key] ? 'bg-teal-950/40 border-teal-500 text-white' : 'bg-slate-900 border-slate-800 text-slate-300 hover:bg-slate-850'}">
                <div class="flex items-center gap-3">
                  <span class="w-6 h-6 rounded-full bg-slate-800 text-slate-300 font-mono text-xs flex items-center justify-center font-bold">${idx + 1}</span>
                  <div>
                    <div class="font-bold text-xs">${c.title}</div>
                    <div class="text-[10px] text-slate-400">${c.desc}</div>
                  </div>
                </div>
                <span class="text-base">${window.tanqiyaAnswers[c.key] ? '✅' : '⚪'}</span>
              </div>
            `).join('')}
          </div>

          <!-- Diagnostic Outcome -->
          <div class="p-5 rounded-2xl bg-slate-950 border border-teal-500/40 space-y-3">
            <div class="flex justify-between items-center border-b border-slate-800 pb-2">
              <span class="text-xs font-bold text-white">Phase Readiness: <strong class="text-teal-400">${requiresTanqiya ? 'PHASE 1: TANQIYA (DETOX)' : 'PHASE 2: TAQWIYAT (NOURISHMENT)'}</strong></span>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded ${requiresTanqiya ? 'bg-amber-500/20 text-amber-300' : 'bg-emerald-500/20 text-emerald-300'} font-bold">
                ${count} / 5 SIGNS PRESENT
              </span>
            </div>

            <p class="text-xs text-slate-200 leading-relaxed">
              ${requiresTanqiya
                ? 'Your biological system exhibits significant <strong>Imtila (Humoral Overload &amp; Toxin Retention)</strong>. Starting high-potency tonics right now is counterproductive. You must first undertake a 7-day <strong>Munzij-wa-Mushil (Humoral Concoction &amp; Gentle Elimination)</strong> protocol to clear metabolic endotoxins.'
                : 'Your eliminative organs (liver, bowel, renal bed) are functioning with adequate clearance. You are ready to safely initiate restorative constitutional tonics and adaptogenic herbal regimens.'}
            </p>

            <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-[11px] text-slate-300">
              <strong class="text-teal-400">Prescribed Regimen:</strong> ${requiresTanqiya ? 'NephroPure Ultra™ (ZAY-004) + Senna-Mallow decoction + 2.5L structured water with barley water (Ma-ul-Sha\'eer).' : 'VitaMani Max™ (ZAY-007) or TensioCalm™ (ZAY-001) for vitality and longevity.'}
            </div>

            <div class="pt-2 flex flex-col sm:flex-row gap-2">
              <button onclick="addToHerbalsCart('${requiresTanqiya ? 'zay-004' : 'zay-007'}'); toggleTanqiyaReadinessModal(false); toggleCheckoutModal();" class="flex-1 py-2.5 bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs rounded-xl shadow transition">
                Order Protocol (${requiresTanqiya ? 'ZAY-004 Detox' : 'ZAY-007 Rejuvenation'})
              </button>
              <button onclick="toggleTanqiyaReadinessModal(false); toggleAsbabChallengeModal(true);" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs rounded-xl border border-slate-700 transition">
                14-Day Reset Challenge
              </button>
            </div>
          </div>

        </div>
      `;
    }
    window.toggleTanqiyaReadinessModal = toggleTanqiyaReadinessModal;
    window.renderTanqiyaReadiness = renderTanqiyaReadiness;


    function toggleGlobalToolsModal(show = true) {
      const modal = document.getElementById('global-tools-modal');
      if (!modal) return;
      if (show) {
        modal.classList.remove('hidden');
      } else {
        modal.classList.add('hidden');
      }
    }
    window.toggleGlobalToolsModal = toggleGlobalToolsModal;


    // ── DEDICATED MIZAJ & ORGAN-AXIS MODAL CONTROLLERS ───────────────────────
    function toggleMizajAssessmentModal(show = true) {
      const modal = document.getElementById('mizaj-assessment-modal');
      if (!modal) return;
      if (show) {
        renderMizajAssessmentModal();
        modal.classList.remove('hidden');
      } else {
        modal.classList.add('hidden');
      }
    }
    window.toggleMizajAssessmentModal = toggleMizajAssessmentModal;

    function renderMizajAssessmentModal() {
      const container = document.getElementById('mizaj-modal-content');
      if (!container) return;
      if (typeof window.previewMizajAnswers === 'undefined') {
        window.previewMizajAnswers = { temp: 'cold', moisture: 'moist', physique: 'broad', digestion: 'sluggish', sleep: 'deep', disposition: 'calm' };
      }
      const ans = window.previewMizajAnswers;
      const mizajRes = calculateDetailedMizaj();

      container.innerHTML = `
        <div class="space-y-6">
          <div class="flex justify-between items-center border-b border-slate-800 pb-3">
            <div>
              <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-wider block">AL-AJNAS AL-ASHRAH CANONICAL MATRIX</span>
              <h4 class="text-sm font-bold text-white">6-Point Constitutional Temperament Questionnaire</h4>
            </div>
            <button onclick="resetMizajAssessment()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-xl border border-slate-700 transition">
              🔄 Reset to Default
            </button>
          </div>

          <!-- 6 Diagnostic Questions Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
            <!-- Q1: Thermal Profile -->
            <div class="p-3.5 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-[11px] font-bold text-teal-400 uppercase">1. Thermal Sensitivity</span>
                <span class="text-[10px] text-slate-400 font-mono">Malmas</span>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="setPreviewMizaj('temp', 'hot')" class="py-2 px-2.5 rounded-xl text-xs font-semibold transition ${ans.temp === 'hot' ? 'bg-gradient-to-r from-red-600 to-amber-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🔥 Warm / Hot
                </button>
                <button onclick="setPreviewMizaj('temp', 'cold')" class="py-2 px-2.5 rounded-xl text-xs font-semibold transition ${ans.temp === 'cold' ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  ❄️ Cold Sensitive
                </button>
              </div>
            </div>

            <!-- Q2: Moisture & Skin Texture -->
            <div class="p-3.5 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-[11px] font-bold text-teal-400 uppercase">2. Moisture &amp; Skin</span>
                <span class="text-[10px] text-slate-400 font-mono">Jild</span>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="setPreviewMizaj('moisture', 'moist')" class="py-2 px-2.5 rounded-xl text-xs font-semibold transition ${ans.moisture === 'moist' ? 'bg-teal-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  💧 Soft / Moist
                </button>
                <button onclick="setPreviewMizaj('moisture', 'dry')" class="py-2 px-2.5 rounded-xl text-xs font-semibold transition ${ans.moisture === 'dry' ? 'bg-teal-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🌵 Dry / Rough
                </button>
              </div>
            </div>

            <!-- Q3: Skeletal Frame & Musculature -->
            <div class="p-3.5 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-[11px] font-bold text-teal-400 uppercase">3. Body Build</span>
                <span class="text-[10px] text-slate-400 font-mono">Binyah</span>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="setPreviewMizaj('physique', 'broad')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.physique === 'broad' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  💪 Broad
                </button>
                <button onclick="setPreviewMizaj('physique', 'athletic')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.physique === 'athletic' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  ⚡ Athletic
                </button>
                <button onclick="setPreviewMizaj('physique', 'soft')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.physique === 'soft' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🫧 Soft
                </button>
                <button onclick="setPreviewMizaj('physique', 'slender')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.physique === 'slender' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🦴 Slender
                </button>
              </div>
            </div>

            <!-- Q4: Appetite & Digestion -->
            <div class="p-3.5 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-[11px] font-bold text-teal-400 uppercase">4. Digestion &amp; Thirst</span>
                <span class="text-[10px] text-slate-400 font-mono">Meda</span>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="setPreviewMizaj('digestion', 'sharp')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.digestion === 'sharp' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🔥 Sharp / High Thirst
                </button>
                <button onclick="setPreviewMizaj('digestion', 'sluggish')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.digestion === 'sluggish' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🐢 Sluggish / Low Thirst
                </button>
                <button onclick="setPreviewMizaj('digestion', 'regular')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.digestion === 'regular' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  ⚖️ Strong / Regular
                </button>
                <button onclick="setPreviewMizaj('digestion', 'variable')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.digestion === 'variable' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🌪️ Irregular / Gas
                </button>
              </div>
            </div>

            <!-- Q5: Sleep Architecture -->
            <div class="p-3.5 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-[11px] font-bold text-teal-400 uppercase">5. Sleep Architecture</span>
                <span class="text-[10px] text-slate-400 font-mono">Naum</span>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="setPreviewMizaj('sleep', 'deep')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.sleep === 'deep' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  💤 Heavy / Excessive
                </button>
                <button onclick="setPreviewMizaj('sleep', 'light')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.sleep === 'light' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  ⚡ Light / Short
                </button>
                <button onclick="setPreviewMizaj('sleep', 'moderate')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.sleep === 'moderate' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🌙 Balanced (7h)
                </button>
                <button onclick="setPreviewMizaj('sleep', 'disturbed')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.sleep === 'disturbed' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🦉 Insomnia / Active Mind
                </button>
              </div>
            </div>

            <!-- Q6: Emotional Temperament -->
            <div class="p-3.5 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-[11px] font-bold text-teal-400 uppercase">6. Mind &amp; Emotion</span>
                <span class="text-[10px] text-slate-400 font-mono">Nafs</span>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button onclick="setPreviewMizaj('disposition', 'calm')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.disposition === 'calm' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🌊 Patient / Easygoing
                </button>
                <button onclick="setPreviewMizaj('disposition', 'intense')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.disposition === 'intense' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  ⚡ Quick-tempered / Driven
                </button>
                <button onclick="setPreviewMizaj('disposition', 'bold')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.disposition === 'bold' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  ☀️ Cheerful / Social
                </button>
                <button onclick="setPreviewMizaj('disposition', 'analytical')" class="py-1.5 rounded-xl text-[11px] font-semibold transition ${ans.disposition === 'analytical' ? 'bg-emerald-600 text-white shadow font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'}">
                  🧐 Reflective / Overthinking
                </button>
              </div>
            </div>
          </div>

          <!-- Real-Time Diagnostic Result Card -->
          <div class="p-5 rounded-2xl bg-slate-950 border border-emerald-500/40 space-y-4">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
              <div>
                <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase">CALCULATED BIO-HUMORAL ARCHETYPE:</span>
                <h4 class="text-base font-extrabold text-white">${mizajRes.title}</h4>
              </div>
              <span class="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-xs font-bold border border-emerald-500/30">
                Dominant: ${mizajRes.primary}
              </span>
            </div>

            <!-- Percentage Bars -->
            <div class="space-y-2">
              <div class="flex justify-between text-[11px] text-slate-300">
                <span>Damawi (Sanguine): <strong>${mizajRes.percentages.damawi}%</strong></span>
                <span>Safrawi (Bilious): <strong>${mizajRes.percentages.safrawi}%</strong></span>
                <span>Balghami (Phlegmatic): <strong>${mizajRes.percentages.balghami}%</strong></span>
                <span>Sawdawi (Melancholic): <strong>${mizajRes.percentages.sawdawi}%</strong></span>
              </div>
              <div class="w-full h-3 rounded-full bg-slate-900 flex overflow-hidden border border-slate-800">
                <div style="width: ${mizajRes.percentages.damawi}%; background-color: #ef4444;" title="Damawi: ${mizajRes.percentages.damawi}%"></div>
                <div style="width: ${mizajRes.percentages.safrawi}%; background-color: #f59e0b;" title="Safrawi: ${mizajRes.percentages.safrawi}%"></div>
                <div style="width: ${mizajRes.percentages.balghami}%; background-color: #06b6d4;" title="Balghami: ${mizajRes.percentages.balghami}%"></div>
                <div style="width: ${mizajRes.percentages.sawdawi}%; background-color: #8b5cf6;" title="Sawdawi: ${mizajRes.percentages.sawdawi}%"></div>
              </div>
            </div>

            <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300">
              <strong class="text-emerald-400">Dietary Directive (Ilaj bil-Ghiza):</strong> ${mizajRes.dietaryDirective}
            </div>

            <!-- Sharing & Action Controls -->
            <div class="flex flex-col sm:flex-row gap-2 pt-1">
              <button onclick="shareMizajOnWhatsApp('${mizajRes.title}', 'Damawi: ${mizajRes.percentages.damawi}%, Safrawi: ${mizajRes.percentages.safrawi}%, Balghami: ${mizajRes.percentages.balghami}%, Sawdawi: ${mizajRes.percentages.sawdawi}%')" class="flex-1 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition flex items-center justify-center gap-2">
                <span>💬</span> WhatsApp Result to Dr. Irfan Ashraf
              </button>
              <button onclick="copyMizajSummary('${mizajRes.title}', 'Damawi: ${mizajRes.percentages.damawi}%, Safrawi: ${mizajRes.percentages.safrawi}%, Balghami: ${mizajRes.percentages.balghami}%, Sawdawi: ${mizajRes.percentages.sawdawi}%', '${mizajRes.dietaryDirective}')" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs rounded-xl border border-slate-700 transition">
                Copy Summary
              </button>
            </div>
          </div>
        </div>
      `;
    }
    window.renderMizajAssessmentModal = renderMizajAssessmentModal;


    function toggleOrganAxisModal(show = true) {
      const modal = document.getElementById('organ-axis-modal');
      if (!modal) return;
      if (show) {
        renderOrganAxisModal();
        modal.classList.remove('hidden');
      } else {
        modal.classList.add('hidden');
      }
    }
    window.toggleOrganAxisModal = toggleOrganAxisModal;

    function renderOrganAxisModal() {
      const container = document.getElementById('organ-axis-modal-content');
      if (!container) return;

      const axisRes = calculateAxisHealth();

      container.innerHTML = `
        <div class="space-y-6">
          <div class="flex justify-between items-center border-b border-slate-800 pb-3">
            <div>
              <span class="text-[10px] font-mono text-teal-400 font-bold uppercase tracking-wider block">SYSTEMS BIOLOGY &amp; ORGAN-AXIS EQUILIBRIUM</span>
              <h4 class="text-sm font-bold text-white">12 Vital Organ Networks • Objective Screener</h4>
            </div>
            <button onclick="resetAxisAssessment()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-xl border border-slate-700 transition">
              🔄 Clear All Checkmarks
            </button>
          </div>

          <!-- Overall Health Score Bar -->
          <div class="p-4 rounded-2xl bg-slate-950 border border-teal-500/40 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
            <div>
              <span class="text-[10px] font-mono text-slate-400 uppercase">CALCULATED ORGAN-AXIS EQUILIBRIUM:</span>
              <div class="text-2xl font-black text-teal-300">${axisRes.score} <span class="text-xs text-slate-500">/ 100</span></div>
              <span class="text-xs text-slate-300">${axisRes.summary}</span>
            </div>
            <div class="text-left sm:text-right">
              <span class="text-[10px] font-mono text-rose-400 block uppercase">PRIMARY FLAGGED STASIS:</span>
              <span class="text-xs font-bold text-white">${axisRes.primaryAxis.name}</span>
              <span class="text-[10px] text-teal-400 block">${axisRes.primaryAxis.english}</span>
            </div>
          </div>

          <!-- 12-Axis Interactive Check Grid -->
          <div class="space-y-3">
            <div class="flex justify-between items-center">
              <span class="text-xs font-bold text-slate-300 uppercase tracking-wider">Tap Any Symptoms You Currently Experience:</span>
              <span class="text-xs font-mono text-teal-400">${axisRes.checkedCount} of 12 Flagged</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
              ${organAxesList.map((ax, idx) => {
                const isChecked = !!(window.selectedAxisSymptoms && window.selectedAxisSymptoms[ax.id]);
                return `
                  <div onclick="toggleAxisSymptom('${ax.id}')" class="p-3 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between ${isChecked ? 'bg-teal-950/50 border-teal-400 shadow-md ring-1 ring-teal-400' : 'bg-slate-950 border-slate-800 hover:border-slate-700'}">
                    <div class="flex items-start justify-between gap-2">
                      <div class="flex items-center gap-2">
                        <span class="text-lg">${ax.icon}</span>
                        <div>
                          <div class="text-xs font-bold text-white">${ax.name}</div>
                          <span class="text-[10px] text-teal-400 font-mono">${ax.english}</span>
                        </div>
                      </div>
                      <span class="w-5 h-5 rounded-md flex items-center justify-center text-xs font-bold ${isChecked ? 'bg-teal-500 text-slate-950' : 'border border-slate-700 text-transparent'}">
                        ✓
                      </span>
                    </div>
                    <p class="text-[11px] text-slate-300 mt-2 leading-relaxed">${ax.symptom}</p>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          <!-- Deep Diagnostic Root Cause Card -->
          <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
            <div class="border-b border-slate-800 pb-2">
              <span class="text-[10px] font-mono uppercase text-teal-400 font-bold block">PRIMARY COMPROMISED SYSTEM ANALYSIS:</span>
              <h5 class="text-sm font-bold text-white">${axisRes.primaryAxis.name} (${axisRes.primaryAxis.english})</h5>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-slate-400 block uppercase text-[10px]">Root Cause Pathophysiology (Su-e-Mizaj):</strong>
                <p class="text-slate-300 leading-relaxed">${axisRes.primaryAxis.rootCause}</p>
                <div class="pt-1.5 text-[11px] text-emerald-400 font-mono">Biomarkers: ${axisRes.primaryAxis.markers}</div>
              </div>
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-teal-400 block uppercase text-[10px]">Targeted Intervention (Afaal &amp; Regimen):</strong>
                <p class="text-slate-300 leading-relaxed">${axisRes.primaryAxis.dualTrack}</p>
                <div class="pt-1.5 text-[11px] text-cyan-400 font-mono">Clinical Efficacy: ${axisRes.primaryAxis.successRate}</div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="pt-1 flex flex-col sm:flex-row gap-2">
            <button onclick="shareAxisOnWhatsApp('${axisRes.score}', '${axisRes.primaryAxis.name.replace(/'/g, "\\'")}', '${axisRes.checkedCount}')" class="flex-1 py-2.5 bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs rounded-xl shadow transition flex items-center justify-center gap-2">
              <span>💬</span> WhatsApp Organ-Axis Report to Dr. Irfan Ashraf
            </button>
            <button onclick="copyAxisSummary('${axisRes.score}', '${axisRes.primaryAxis.name.replace(/'/g, "\\'")}', '${axisRes.primaryAxis.rootCause.replace(/'/g, "\\'")}')" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs rounded-xl border border-slate-700 transition">
              Copy Report
            </button>
          </div>

        </div>
      `;
    }
    window.renderOrganAxisModal = renderOrganAxisModal;
