#!/usr/bin/env python3
"""
ZAYVORA Health OS — Functional Medicine & Classical Unani Fusion Suite
Injects 5 cutting-edge Functional Medicine features benchmarked against IFM (USA):
1. Hazm-e-Arba'a 4-Stage Digestion & Metabolic Screener (IFM Matrix Core)
2. Functional ATM Timeline (Antecedents, Triggers, Mediators - Saniha-e-Maraz)
3. 24h Circadian Humoral Bio-Clock (Chrono-Therapeutics & Bio-Rhythm)
4. Gut-Brain Axis & Vagus Nerve Screener (Bukharat-e-Meda & Maraq)
5. Toxic Burden & Cellular Tanqiya Readiness Index (Detox & Munzij Protocol)
"""

import sys
import re

def main():
    print("Injecting Functional Medicine Powerhouse Suite into ZAYVORA...")

    # 1. READ HTML
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 2. DEFINE THE 5 FUNCTIONAL MEDICINE HTML MODALS
    functional_modals = '''
  <!-- ===================================================================== -->
  <!-- 6. IFM BENCHMARK: HAZM-E-ARBA'A 4-STAGE DIGESTION & DETOX ANALYZER     -->
  <!-- ===================================================================== -->
  <div id="hazm-arba-modal" class="fixed inset-0 z-50 hidden bg-black/90 backdrop-blur-md flex items-center justify-center p-3 sm:p-5">
    <div class="bg-slate-900 border border-emerald-500/50 rounded-3xl max-w-4xl w-full max-h-[94vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
      <div class="px-6 py-4 border-b border-slate-800 bg-slate-950 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white flex items-center justify-center font-bold text-lg shadow-md">🔄</span>
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <span>Hazm-e-Arba'a™ 4-Stage Metabolic Digestion Screener</span>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">IFM Matrix Benchmark</span>
            </h3>
            <p class="text-xs text-slate-400">Discover which of the 4 metabolic stages (Gastric, Hepatic, Vascular, Cellular) has humoral stasis</p>
          </div>
        </div>
        <button onclick="toggleHazmArbaModal(false)" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition">✕</button>
      </div>
      <div id="hazm-arba-content" class="p-6 overflow-y-auto flex-1 space-y-5 text-xs">
        <!-- Rendered dynamically by renderHazmArba() -->
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- 7. IFM BENCHMARK: FUNCTIONAL ATM ROOT-CAUSE TIMELINE BUILDER           -->
  <!-- ===================================================================== -->
  <div id="atm-timeline-modal" class="fixed inset-0 z-50 hidden bg-black/90 backdrop-blur-md flex items-center justify-center p-3 sm:p-5">
    <div class="bg-slate-900 border border-indigo-500/50 rounded-3xl max-w-4xl w-full max-h-[94vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
      <div class="px-6 py-4 border-b border-slate-800 bg-slate-950 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-500 text-white flex items-center justify-center font-bold text-lg shadow-md">⏳</span>
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <span>Functional ATM Timeline™ (Antecedents • Triggers • Mediators)</span>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Saniha-e-Maraz</span>
            </h3>
            <p class="text-xs text-slate-400">Uncover the congenital roots, inciting events, and ongoing daily mediators of your chronic condition</p>
          </div>
        </div>
        <button onclick="toggleAtmTimelineModal(false)" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition">✕</button>
      </div>
      <div id="atm-timeline-content" class="p-6 overflow-y-auto flex-1 space-y-5 text-xs">
        <!-- Rendered dynamically by renderAtmTimeline() -->
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- 8. CHRONO-THERAPEUTICS: 24-HOUR CIRCADIAN HUMORAL BIO-CLOCK           -->
  <!-- ===================================================================== -->
  <div id="humoral-clock-modal" class="fixed inset-0 z-50 hidden bg-black/90 backdrop-blur-md flex items-center justify-center p-3 sm:p-5">
    <div class="bg-slate-900 border border-amber-500/50 rounded-3xl max-w-4xl w-full max-h-[94vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
      <div class="px-6 py-4 border-b border-slate-800 bg-slate-950 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-600 to-yellow-500 text-slate-950 flex items-center justify-center font-bold text-lg shadow-md">⏱️</span>
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <span>Circadian Humoral Bio-Clock™ (ساعتِ بدن و اخلاط)</span>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">Chrono-Therapeutics</span>
            </h3>
            <p class="text-xs text-slate-400">Real-time biological clock aligning nutrition, botanical posology, and metabolic digestion with daily humoral surges</p>
          </div>
        </div>
        <button onclick="toggleHumoralClockModal(false)" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition">✕</button>
      </div>
      <div id="humoral-clock-content" class="p-6 overflow-y-auto flex-1 space-y-5 text-xs">
        <!-- Rendered dynamically by renderHumoralClock() -->
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- 9. NEURO-GASTROENTEROLOGY: GUT-BRAIN AXIS & VAGUS NERVE SCREENER       -->
  <!-- ===================================================================== -->
  <div id="gut-brain-modal" class="fixed inset-0 z-50 hidden bg-black/90 backdrop-blur-md flex items-center justify-center p-3 sm:p-5">
    <div class="bg-slate-900 border border-rose-500/50 rounded-3xl max-w-4xl w-full max-h-[94vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
      <div class="px-6 py-4 border-b border-slate-800 bg-slate-950 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-600 to-pink-500 text-white flex items-center justify-center font-bold text-lg shadow-md">🧠</span>
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <span>Gut-Brain Axis &amp; Vagus Nerve Correlator™</span>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30">Maraq-e-Meda</span>
            </h3>
            <p class="text-xs text-slate-400">Determine whether your brain fog, anxiety, or insomnia is secondary to gastrointestinal fermentative putrefaction</p>
          </div>
        </div>
        <button onclick="toggleGutBrainModal(false)" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition">✕</button>
      </div>
      <div id="gut-brain-content" class="p-6 overflow-y-auto flex-1 space-y-5 text-xs">
        <!-- Rendered dynamically by renderGutBrain() -->
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- 10. DETOX & MUNZIJ PROTOCOL: CELLULAR TANQIYA READINESS INDEX         -->
  <!-- ===================================================================== -->
  <div id="tanqiya-readiness-modal" class="fixed inset-0 z-50 hidden bg-black/90 backdrop-blur-md flex items-center justify-center p-3 sm:p-5">
    <div class="bg-slate-900 border border-teal-500/50 rounded-3xl max-w-4xl w-full max-h-[94vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
      <div class="px-6 py-4 border-b border-slate-800 bg-slate-950 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-600 to-cyan-500 text-white flex items-center justify-center font-bold text-lg shadow-md">🌿</span>
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <span>Toxic Burden &amp; Cellular Tanqiya Readiness Index™</span>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-teal-500/20 text-teal-300 border border-teal-500/30">Munzij &amp; Mushil Protocol</span>
            </h3>
            <p class="text-xs text-slate-400">Evaluate whether your cellular reserve requires Phase 1 Detoxification (Tanqiya) before taking restorative tonics</p>
          </div>
        </div>
        <button onclick="toggleTanqiyaReadinessModal(false)" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition">✕</button>
      </div>
      <div id="tanqiya-readiness-content" class="p-6 overflow-y-auto flex-1 space-y-5 text-xs">
        <!-- Rendered dynamically by renderTanqiyaReadiness() -->
      </div>
    </div>
  </div>
'''

    if 'id="hazm-arba-modal"' not in html:
        html = html.replace('</body>', functional_modals + '\n</body>')
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ Injected 5 Functional Medicine Modals into index.html")
    else:
        print("• Functional Medicine Modals already exist in index.html")

    # 3. APPEND JAVASCRIPT LOGIC TO JS/ZAYVORA-CORE.JS
    with open("js/zayvora-core.js", "r", encoding="utf-8") as f:
        js = f.read()

    js_suite = r'''
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
              <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-wider">IFM Matrix Assimilation &amp; Biotransformation Engine</span>
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
            <span class="text-[10px] font-mono text-indigo-400 font-bold uppercase tracking-wider">The Functional Medicine Chronological Genesis (IFM Timeline Benchmark)</span>
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
'''

    if 'window.activeHazmStage' not in js:
        js += '\n' + js_suite
        with open("js/zayvora-core.js", "w", encoding="utf-8") as f:
            f.write(js)
        print("✓ Appended 5 Functional Medicine JavaScript modules to js/zayvora-core.js")
    else:
        print("• Functional Medicine JavaScript modules already present in js/zayvora-core.js")

    # 4. INJECT THE GLOBAL BENCHMARKS & FUNCTIONAL MATRIX CARDS INTO THE HERO OF THE LANDING PAGE
    with open("js/zayvora-core.js", "r", encoding="utf-8") as f:
        js_content = f.read()

    # Search for Action Matrix in renderWebsiteApp
    target_needle = r'<!-- Regulatory & Quality Accreditations Strip -->'
    hero_benchmarks_section = r'''
            <!-- ===================================================================== -->
            <!-- GLOBAL CLINICAL BENCHMARKS & FUNCTIONAL MEDICINE SUITE (IFM / MAYO)   -->
            <!-- ===================================================================== -->
            <div class="mt-8 p-6 rounded-3xl bg-slate-900/90 border border-emerald-500/40 shadow-2xl space-y-5 text-left">
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
                <div>
                  <div class="flex items-center gap-2">
                    <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-mono font-bold uppercase">
                      Integrative Clinical Suite
                    </span>
                    <span class="text-xs text-slate-400">Mayo Clinic • Cleveland Clinic • IFM Benchmarks</span>
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
                  <div class="text-[10px] text-slate-400 mt-0.5">Mayo-Style Triage</div>
                </button>

                <!-- 2. Lab Correlator -->
                <button onclick="toggleLabCorrelatorModal(true)" class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 hover:border-teal-500/60 hover:bg-teal-950/20 text-left transition group cursor-pointer">
                  <div class="text-xl mb-1 group-hover:scale-110 transition">🧪</div>
                  <div class="font-bold text-xs text-white">Lab Correlator</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">Cleveland 2nd Opinion</div>
                </button>

                <!-- 3. Food Matrix -->
                <button onclick="toggleFoodCompatibilityModal(true)" class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 hover:border-amber-500/60 hover:bg-amber-950/20 text-left transition group cursor-pointer">
                  <div class="text-xl mb-1 group-hover:scale-110 transition">🥗</div>
                  <div class="font-bold text-xs text-white">Kitchen Matrix</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">ZOE Precision Food</div>
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

'''

    if 'GLOBAL CLINICAL BENCHMARKS & FUNCTIONAL MEDICINE SUITE' not in js_content:
        js_content = js_content.replace(target_needle, hero_benchmarks_section + '\n            ' + target_needle)
        with open("js/zayvora-core.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        print("✓ Injected 10-Tool Diagnostic Suite Grid into Landing Page Hero in js/zayvora-core.js")
    else:
        print("• 10-Tool Diagnostic Suite Grid already present in Landing Page Hero")

if __name__ == '__main__':
    main()
