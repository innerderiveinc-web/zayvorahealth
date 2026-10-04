#!/usr/bin/env python3
"""
ZAYVORA Health OS — Comprehensive Bio-Humoral & Functional Health Assessment Engine
Implements:
1. Interactive 8-Pillar Whole-Person Assessment Modal in index.html
2. Full JavaScript State Machine, Scoring Algorithm, and Visual Result Dossier in js/zayvora-core.js
3. Top Header and Hero CTA triggers
4. Downloadable Health Dossier & WhatsApp sharing
"""

import sys

INDEX_FILE = "index.html"
CORE_FILE = "js/zayvora-core.js"

ASSESSMENT_MODAL_HTML = '''
  <!-- ===================================================================== -->
  <!-- MODAL: COMPREHENSIVE 8-PILLAR WHOLE-PERSON HEALTH ASSESSMENT (DOSSIER) -->
  <!-- ===================================================================== -->
  <div id="health-assessment-modal" class="fixed inset-0 z-50 hidden bg-black/90 backdrop-blur-md flex items-center justify-center p-3 sm:p-5">
    <div class="bg-slate-900 border border-emerald-500/50 rounded-3xl max-w-3xl w-full max-h-[94vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
      
      <!-- Modal Header -->
      <div class="px-6 py-4 border-b border-slate-800 bg-slate-950 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white flex items-center justify-center font-bold text-lg shadow-md">🧠</span>
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <span>ZAYVORA Whole-Person Bio-Humoral Health Audit™</span>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Free Clinical Assessment</span>
            </h3>
            <p id="assessment-step-subtitle" class="text-xs text-slate-400">Pillar 1 of 8: Mizaj &amp; Thermal Equilibrium</p>
          </div>
        </div>
        <button onclick="toggleHealthAssessmentModal(false)" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition">✕</button>
      </div>

      <!-- Live Multi-Step Progress Bar -->
      <div class="w-full bg-slate-800 h-1.5 overflow-hidden">
        <div id="assessment-progress-bar" class="bg-gradient-to-r from-emerald-500 via-teal-400 to-cyan-400 h-full w-[12%] transition-all duration-300"></div>
      </div>

      <!-- Modal Body (Dynamic Questions / Dossier Results) -->
      <div id="health-assessment-body" class="p-6 overflow-y-auto flex-1 space-y-5 text-xs">
        <!-- Rendered dynamically by renderAssessmentStep() -->
      </div>

      <!-- Modal Footer Controls -->
      <div id="health-assessment-footer" class="px-6 py-3.5 border-t border-slate-800 bg-slate-950 flex justify-between items-center">
        <button id="assessment-prev-btn" onclick="prevAssessmentStep()" class="px-4 py-2 border border-slate-700 rounded-xl text-slate-400 hover:text-white text-xs font-semibold disabled:opacity-30 disabled:cursor-not-allowed">
          &larr; Previous Pillar
        </button>
        <div class="flex items-center gap-2">
          <span id="assessment-counter-label" class="text-[11px] text-slate-400 font-mono">Pillar 1 / 8</span>
          <button id="assessment-next-btn" onclick="nextAssessmentStep()" class="px-6 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs rounded-xl shadow-lg transition flex items-center gap-1.5 cursor-pointer">
            <span>Continue</span>
            <span>&rarr;</span>
          </button>
        </div>
      </div>

    </div>
  </div>
'''

ASSESSMENT_JS_ENGINE = '''
    // ── ZAYVORA COMPREHENSIVE 8-PILLAR WHOLE-PERSON HEALTH ASSESSMENT ENGINE ──
    window.healthAssessmentState = {
      currentStep: 1, // 1 to 8 pillars, step 9 = final dossier
      userAge: 36,
      userName: 'Valued Visitor',
      answers: {
        // Pillar 1
        p1_temp: 'moderate',
        p1_physique: 'balanced',
        // Pillar 2
        p2_digestion: 'mild_bloating',
        p2_bowel: 'regular',
        // Pillar 3
        p3_stress: 'moderate_anxiety',
        p3_energy: 'afternoon_slump',
        // Pillar 4
        p4_sleep_depth: 'interrupted',
        p4_morning_feel: 'groggy',
        // Pillar 5
        p5_illness: 'occasional_seasonal',
        p5_recovery: 'medium_recovery',
        // Pillar 6
        p6_sweat: 'normal_sweat',
        p6_tongue: 'mild_coating',
        // Pillar 7
        p7_stamina: 'average_stamina',
        p7_hormones: 'mild_swings',
        // Pillar 8
        p8_screen: 'high_screen',
        p8_support: 'moderate_support'
      }
    };

    const healthAssessmentPillars = [
      {
        id: 1,
        title: "Pillar 1: Mizaj & Thermal Equilibrium (مزاجِ بدن)",
        subtitle: "Evaluates the balance of internal metabolic heat (Hararat) and moisture (Ratoobat).",
        questions: [
          {
            key: "p1_temp",
            label: "How does your body typically react to climatic temperature?",
            options: [
              { val: "cold_intolerant", text: "Very sensitive to cold (Hands/feet cold, loves warmth)", mizaj: "Balghami", score: 60 },
              { val: "heat_intolerant", text: "Very sensitive to heat (Sweats easily, agitated in summer)", mizaj: "Safrawi", score: 65 },
              { val: "dry_cold", text: "Intolerant of dry winds & winter (Prone to aches/stiffness)", mizaj: "Sawdawi", score: 55 },
              { val: "moderate", text: "Comfortable across seasons, adapts smoothly", mizaj: "Damawi", score: 95 }
            ]
          },
          {
            key: "p1_physique",
            label: "What best describes your body build and skin texture?",
            options: [
              { val: "broad_soft", text: "Broad build, soft/cool skin, tendency to gain weight easily", mizaj: "Balghami", score: 65 },
              { val: "lean_warm", text: "Lean/medium build, warm skin, sharp appetite and quick metabolism", mizaj: "Safrawi", score: 70 },
              { val: "slender_dry", text: "Slender frame, dry skin, prominent veins and light bones", mizaj: "Sawdawi", score: 60 },
              { val: "balanced", text: "Well-proportioned, warm & firm skin, robust posture", mizaj: "Damawi", score: 95 }
            ]
          }
        ]
      },
      {
        id: 2,
        title: "Pillar 2: Digestive Fire & Metabolism (ہضم و قوتِ طبعیہ)",
        subtitle: "Assesses gastric fire (Hazm-e-Meda), hepatic processing, and intestinal microbiome transit.",
        questions: [
          {
            key: "p2_digestion",
            label: "How do you feel 1–2 hours after having a standard meal?",
            options: [
              { val: "severe_bloat", text: "Heavy, sluggish, bloated with gas and brain fog", score: 50 },
              { val: "burning_acid", text: "Acid reflux, burning sensation in chest/stomach", score: 55 },
              { val: "mild_bloating", text: "Occasional heaviness, especially after heavy foods", score: 75 },
              { val: "light_active", text: "Light, energetic, clean digestion with zero discomfort", score: 95 }
            ]
          },
          {
            key: "p2_bowel",
            label: "What is your typical daily bowel evacuation pattern (Istifragh)?",
            options: [
              { val: "constipated", text: "Constipated (Incomplete, strained, or every 2 days)", score: 45 },
              { val: "irregular_loose", text: "Irregular, loose stools or sudden urgency", score: 60 },
              { val: "regular", text: "Daily clean morning bowel movement without straining", score: 95 }
            ]
          }
        ]
      },
      {
        id: 3,
        title: "Pillar 3: Mental Strength & Psychosomatic Resilience (قوتِ نفسانیہ)",
        subtitle: "Evaluates nervous system tone, cognitive focus, and emotional equilibrium.",
        questions: [
          {
            key: "p3_stress",
            label: "When confronted with high work or emotional pressure, what is your reaction?",
            options: [
              { val: "severe_anxiety", text: "Overthinking, tight chest, insomnia, overwhelming anxiety", score: 45 },
              { val: "quick_anger", text: "Sudden irritation, anger, restlessness and impatience", score: 60 },
              { val: "moderate_anxiety", text: "Mild stress and distraction, but manage to recover", score: 75 },
              { val: "calm_focused", text: "Calm, grounded, rational focus with emotional poise", score: 95 }
            ]
          },
          {
            key: "p3_energy",
            label: "How is your mental clarity and concentration through the day?",
            options: [
              { val: "chronic_fog", text: "Frequent brain fog, forgetfulness, and fatigue", score: 50 },
              { val: "afternoon_slump", text: "Good in the morning, but heavy crash around 2–4 PM", score: 70 },
              { val: "sharp_steady", text: "Sharp, steady focus and clear mental agility all day", score: 95 }
            ]
          }
        ]
      },
      {
        id: 4,
        title: "Pillar 4: Sleep Architecture & Circadian Restoration (نوم و یقظہ)",
        subtitle: "Measures restorative sleep depth, nocturnal hormone release, and vital spirit (Ruh) replenishment.",
        questions: [
          {
            key: "p4_sleep_depth",
            label: "How would you describe your typical night of sleep?",
            options: [
              { val: "insomnia", text: "Difficulty falling asleep (Tossing 45+ mins, racing thoughts)", score: 45 },
              { val: "interrupted", text: "Wake up 2–3 times during the night, shallow sleep", score: 60 },
              { val: "deep_restorative", text: "7–8 hours uninterrupted, deep restorative sleep", score: 95 }
            ]
          },
          {
            key: "p4_morning_feel",
            label: "How do you feel upon waking up in the morning?",
            options: [
              { val: "exhausted", text: "Exhausted, stiff limbs, needing stimulants (Tea/Coffee) to function", score: 45 },
              { val: "groggy", text: "A bit slow for the first 30 mins, then gradually pick up", score: 70 },
              { val: "refreshed", text: "Wake up energized, clear-headed, and eager for the day", score: 95 }
            ]
          }
        ]
      },
      {
        id: 5,
        title: "Pillar 5: Innate Healing Resilience & Immunity (قوتِ مدبرہِ بدن)",
        subtitle: "Measures Tabiyat Mudabbira-e-Badan — your body's intrinsic auto-healing and immunological defence.",
        questions: [
          {
            key: "p5_illness",
            label: "How frequently do you experience colds, seasonal allergies, or infections?",
            options: [
              { val: "very_frequent", text: "Every weather change / 4+ times a year (Catches infections fast)", score: 50 },
              { val: "occasional_seasonal", text: "1–2 times a year, usually resolving within a week", score: 75 },
              { val: "rarely_ill", text: "Rarely ever fall sick; robust natural immunological resistance", score: 95 }
            ]
          },
          {
            key: "p5_recovery",
            label: "When you get injured, fatigued, or sick, how fast does your body bounce back?",
            options: [
              { val: "slow_recovery", text: "Very slow recovery; lingering fatigue and prolonged symptoms", score: 50 },
              { val: "medium_recovery", text: "Moderate recovery; needs 4–7 days of rest to feel normal", score: 75 },
              { val: "rapid_recovery", text: "Rapid rebound; body heals cleanly with minimal medication", score: 95 }
            ]
          }
        ]
      },
      {
        id: 6,
        title: "Pillar 6: Toxic Burden & Metabolic Clearance (تنقیہ و فضلات)",
        subtitle: "Evaluates lymphatic drainage, natural perspiration, and elimination of metabolic wastes (Fuzlaat).",
        questions: [
          {
            key: "p6_sweat",
            label: "How is your natural perspiration (sweating) during physical activity or heat?",
            options: [
              { val: "no_sweat", text: "Rarely sweat even during exercise; dry or dull skin", score: 50 },
              { val: "excessive_pungent", text: "Profuse, clammy, pungent or irritating sweat", score: 60 },
              { val: "normal_sweat", text: "Clean, natural sweating during exertion; skin feels fresh", score: 95 }
            ]
          },
          {
            key: "p6_tongue",
            label: "When you look at your tongue in the mirror first thing in the morning:",
            options: [
              { val: "thick_white", text: "Thick white coating, slimy feeling, tastelessness (Balghami load)", score: 50 },
              { val: "yellow_bitter", text: "Yellowish coating, dry mouth, bitter taste (Safrawi load)", score: 55 },
              { val: "dark_dry", text: "Darker/rough coating, astringent taste (Sawdawi load)", score: 50 },
              { val: "mild_coating", text: "Thin translucent coating, pink moist surface (Healthy baseline)", score: 95 }
            ]
          }
        ]
      },
      {
        id: 7,
        title: "Pillar 7: Hormonal Stability & Physical Stamina (قوتِ حیوانیہ و باہ)",
        subtitle: "Evaluates mitochondrial stamina, endocrine homeostasis, and reproductive vitality.",
        questions: [
          {
            key: "p7_stamina",
            label: "What is your physical endurance and muscular energy level?",
            options: [
              { val: "poor_stamina", text: "Exhausted easily; climbing 2 flights of stairs causes breathlessness", score: 45 },
              { val: "average_stamina", text: "Can perform daily routines, but completely drained by evening", score: 70 },
              { val: "high_stamina", text: "Strong physical endurance, good muscle recovery and stamina", score: 95 }
            ]
          },
          {
            key: "p7_hormones",
            label: "How stable are your hormones, vitality, and mood drive?",
            options: [
              { val: "low_vitality", text: "Low vitality, loss of drive, frequent mood dips / hormonal imbalance", score: 50 },
              { val: "mild_swings", text: "Occasional fatigue and fluctuations with stress", score: 75 },
              { val: "optimal_vitality", text: "Strong vitality, balanced hormones, steady drive and enthusiasm", score: 95 }
            ]
          }
        ]
      },
      {
        id: 8,
        title: "Pillar 8: Environmental & Lifestyle Harmony (اسبابِ ستہ ضروریہ)",
        subtitle: "Evaluates your daily alignment with natural light, movement, air quality, and social peace.",
        questions: [
          {
            key: "p8_screen",
            label: "What is your daily exposure to artificial blue light (screens) vs natural outdoor sunlight?",
            options: [
              { val: "extreme_screen", text: "10+ hours screen time, virtually zero direct morning sunlight", score: 45 },
              { val: "high_screen", text: "6–9 hours screen time, 10–15 mins occasional sunlight", score: 65 },
              { val: "balanced_sun", text: "Regular daily outdoor natural sunlight (20+ mins), screen curfews", score: 95 }
            ]
          },
          {
            key: "p8_support",
            label: "How would you rate your daily inner peace and emotional environment?",
            options: [
              { val: "high_lonely", text: "High chronic stress, feeling isolated, little work-life boundary", score: 45 },
              { val: "moderate_support", text: "Busy routine, moderate stress, fair support from family/friends", score: 75 },
              { val: "peaceful_connected", text: "Emotionally fulfilled, supportive community, regular moments of peace", score: 95 }
            ]
          }
        ]
      }
    ];

    function openHealthAssessmentModal() {
      const modal = document.getElementById('health-assessment-modal');
      if (!modal) return;
      window.healthAssessmentState.currentStep = 1;
      renderAssessmentStep();
      modal.classList.remove('hidden');
    }

    function toggleHealthAssessmentModal(show = true) {
      const modal = document.getElementById('health-assessment-modal');
      if (!modal) return;
      if (show) openHealthAssessmentModal();
      else modal.classList.add('hidden');
    }

    function renderAssessmentStep() {
      const state = window.healthAssessmentState;
      const body = document.getElementById('health-assessment-body');
      const subtitle = document.getElementById('assessment-step-subtitle');
      const progressBar = document.getElementById('assessment-progress-bar');
      const prevBtn = document.getElementById('assessment-prev-btn');
      const nextBtn = document.getElementById('assessment-next-btn');
      const counterLabel = document.getElementById('assessment-counter-label');
      const footer = document.getElementById('health-assessment-footer');

      if (!body) return;

      if (state.currentStep <= 8) {
        if (footer) footer.classList.remove('hidden');
        const pillar = healthAssessmentPillars.find(p => p.id === state.currentStep) || healthAssessmentPillars[0];
        
        if (subtitle) subtitle.innerHTML = `<strong>${pillar.title}</strong> — ${pillar.subtitle}`;
        if (progressBar) progressBar.style.width = `${Math.round((state.currentStep / 8) * 100)}%`;
        if (counterLabel) counterLabel.innerText = `Pillar ${state.currentStep} of 8 (${Math.round((state.currentStep / 8) * 100)}%)`;
        if (prevBtn) prevBtn.disabled = (state.currentStep === 1);
        if (nextBtn) {
          nextBtn.innerHTML = state.currentStep === 8 ? '<span>Calculate Health Dossier</span> <span>⚡</span>' : '<span>Next Pillar</span> <span>&rarr;</span>';
        }

        body.innerHTML = `
          <div class="space-y-6">
            <!-- Pillar Intro Card -->
            <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-1">
              <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-wider">Clinical Diagnostic Screener</span>
              <h4 class="text-sm font-bold text-white">${pillar.title}</h4>
              <p class="text-xs text-slate-400 leading-relaxed">${pillar.subtitle}</p>
            </div>

            <!-- Questions for this Pillar -->
            <div class="space-y-5">
              ${pillar.questions.map((q, qIdx) => `
                <div class="space-y-2.5">
                  <label class="block text-xs font-bold text-slate-200">
                    <span class="text-emerald-400 font-mono mr-1.5">${qIdx + 1}.</span> ${q.label}
                  </label>
                  <div class="grid grid-cols-1 gap-2">
                    ${q.options.map(opt => {
                      const isSelected = state.answers[q.key] === opt.val;
                      return `
                        <div onclick="selectAssessmentAnswer('${q.key}', '${opt.val}')" class="p-3 rounded-xl border transition cursor-pointer flex items-center justify-between ${isSelected ? 'border-emerald-500 bg-emerald-950/40 text-white shadow-md ring-1 ring-emerald-500' : 'border-slate-800 bg-slate-950/80 hover:bg-slate-950 hover:border-slate-700 text-slate-300'}">
                          <div class="flex items-center gap-2.5">
                            <span class="w-4 h-4 rounded-full border flex items-center justify-center shrink-0 ${isSelected ? 'border-emerald-500 bg-emerald-500 text-slate-950 font-bold text-[10px]' : 'border-slate-700'}">
                              ${isSelected ? '✓' : ''}
                            </span>
                            <span class="text-xs">${opt.text}</span>
                          </div>
                          ${opt.mizaj ? `<span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-900 border border-slate-700 text-emerald-300 font-semibold">${opt.mizaj}</span>` : ''}
                        </div>
                      `;
                    }).join('')}
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      } else {
        // Step 9: Render the Comprehensive Visual Health Dossier Report
        calculateAndRenderHealthDossier();
      }
    }

    function selectAssessmentAnswer(key, val) {
      window.healthAssessmentState.answers[key] = val;
      renderAssessmentStep();
    }

    function nextAssessmentStep() {
      if (window.healthAssessmentState.currentStep < 8) {
        window.healthAssessmentState.currentStep++;
        renderAssessmentStep();
      } else {
        // Proceed to Dossier
        window.healthAssessmentState.currentStep = 9;
        renderAssessmentStep();
      }
    }

    function prevAssessmentStep() {
      if (window.healthAssessmentState.currentStep > 1) {
        window.healthAssessmentState.currentStep--;
        renderAssessmentStep();
      }
    }

    function calculateAndRenderHealthDossier() {
      const state = window.healthAssessmentState;
      const body = document.getElementById('health-assessment-body');
      const subtitle = document.getElementById('assessment-step-subtitle');
      const progressBar = document.getElementById('assessment-progress-bar');
      const footer = document.getElementById('health-assessment-footer');

      if (!body) return;
      if (footer) footer.classList.add('hidden'); // Custom action buttons inside dossier
      if (subtitle) subtitle.innerHTML = '<strong>Comprehensive Health Dossier Generated</strong> • Verified by Hakeem Dr. Irfan Ashraf';
      if (progressBar) progressBar.style.width = '100%';

      // Calculate Pillar Scores
      const pillarScores = [];
      let totalWeightedScore = 0;

      healthAssessmentPillars.forEach(pil => {
        let pilSum = 0;
        pil.questions.forEach(q => {
          const ansKey = state.answers[q.key];
          const matchedOpt = q.options.find(o => o.val === ansKey) || q.options[0];
          pilSum += matchedOpt.score;
        });
        const avgScore = Math.round(pilSum / pil.questions.length);
        pillarScores.push({ id: pil.id, name: pil.title.split(':')[1].trim(), score: avgScore });
        totalWeightedScore += avgScore;
      });

      const overallScore = Math.round(totalWeightedScore / 8);
      const calendarAge = state.userAge || 36;
      // Functional Vitality Age formula
      let ageDelta = 0;
      if (overallScore < 60) ageDelta = 7;
      else if (overallScore < 70) ageDelta = 4;
      else if (overallScore < 85) ageDelta = 1;
      else ageDelta = -4; // Younger vitality!
      const functionalAge = calendarAge + ageDelta;

      // Determine Primary Su-e-Mizaj & Root Cause
      let dominantMizaj = "Balghami (Cold-Moist)";
      let rootCause = "Sluggish gastric agni (Hazm-e-Meda), accumulated Phlegm, and blue-light circadian stress.";
      let matchedSku = "ZAY-001";
      let matchedProd = "ZAYVORA TensioCalm™";
      let recommendedDiet = "Favor warm carminative teas (Ajwain, Zanjabeel/Ginger, Cumin). Strictly eliminate iced water, sour curds, and heavy refined starches.";

      if (state.answers.p1_temp === 'heat_intolerant' || state.answers.p2_digestion === 'burning_acid') {
        dominantMizaj = "Safrawi (Hot-Dry / Bilious)";
        rootCause = "Elevated biliary heat, gastric hyperacidity, and sympathetic nervous overdrive.";
        matchedSku = "ZAY-003";
        matchedProd = "ZAYVORA LiverPrime Core™";
        recommendedDiet = "Favor cooling mucilaginous badraqa (Tukhm-e-Balanga, Arq Shahtarra, Cucumber, Pomegranate). Strictly avoid fried chillies, vinegar, and excessive red meat.";
      } else if (state.answers.p1_temp === 'dry_cold' || state.answers.p3_stress === 'severe_anxiety') {
        dominantMizaj = "Sawdawi (Cold-Dry / Melancholic)";
        rootCause = "Elevated Black Bile combustion, nervous hypersensitivity, and nocturnal sleep latency.";
        matchedSku = "ZAY-005";
        matchedProd = "ZAYVORA NeuroCalmX™";
        recommendedDiet = "Favor warm almond milk with saffron, honey, stewed apples, and warm foot baths with Roghan Banafsha. Avoid stale foods, excessive lentils, and caffeine.";
      } else if (overallScore >= 85) {
        dominantMizaj = "Motadil Damawi (Balanced Sanguine)";
        rootCause = "Strong physiological equilibrium with minor lifestyle adaptations required to preserve vitality.";
        matchedSku = "ZAY-007";
        matchedProd = "ZAYVORA VitaMani Max™";
        recommendedDiet = "Maintain current balanced seasonal dietary regimen with 2.5L daily hydration and fresh seasonal greens.";
      }

      body.innerHTML = `
        <div class="space-y-6 text-xs pb-4">
          
          <!-- Master Scorecard Header Banner -->
          <div class="p-6 rounded-3xl bg-gradient-to-r from-emerald-950/90 via-slate-900 to-teal-950/90 border border-emerald-500/50 flex flex-col md:flex-row justify-between items-center gap-6 shadow-2xl">
            <div class="flex items-center gap-5">
              <!-- Radial Dial Badge -->
              <div class="w-24 h-24 rounded-full border-4 ${overallScore >= 80 ? 'border-emerald-400 bg-emerald-950/80 text-emerald-300' : overallScore >= 65 ? 'border-amber-400 bg-amber-950/80 text-amber-300' : 'border-rose-400 bg-rose-950/80 text-rose-300'} flex flex-col items-center justify-center font-mono font-black shadow-lg shrink-0">
                <span class="text-3xl leading-none">${overallScore}</span>
                <span class="text-[9px] uppercase tracking-wider text-slate-400 mt-1">out of 100</span>
              </div>
              <div>
                <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400 block">ZAYVORA Whole-Person Vitality Score</span>
                <h3 class="text-xl font-black text-white mt-0.5">${overallScore >= 80 ? 'Optimal Humoral Equilibrium' : overallScore >= 65 ? 'Moderate Functional Dyscrasia' : 'Substantial Humoral Imbalance (Needs Tanqiya)'}</h3>
                <p class="text-xs text-slate-300 mt-1">Dominant Temperament: <strong class="text-emerald-300">${dominantMizaj}</strong></p>
              </div>
            </div>

            <!-- Biological Age Card -->
            <div class="p-4 rounded-2xl bg-slate-950/90 border border-slate-800 text-center shrink-0 w-full md:w-auto">
              <span class="text-[10px] text-slate-400 block">Functional Vitality Age:</span>
              <div class="text-2xl font-black font-mono ${ageDelta > 0 ? 'text-amber-400' : 'text-emerald-400'}">${functionalAge} Years</div>
              <span class="text-[10px] text-slate-400">Calendar Age: ${calendarAge} (${ageDelta > 0 ? '+' + ageDelta + ' yrs stress load' : 'Youthful Vitality!'})</span>
            </div>
          </div>

          <!-- 8-Pillar Visual Breakdown -->
          <div class="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
            <h4 class="font-bold text-white text-xs flex items-center justify-between">
              <span>8-Pillar Functional Breakdown</span>
              <span class="text-[10px] text-slate-400 font-normal">Scores &gt;80 indicates optimal harmony</span>
            </h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              ${pillarScores.map(p => `
                <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1.5">
                  <div class="flex justify-between items-center">
                    <strong class="text-slate-200 text-[11px] truncate">${p.name}</strong>
                    <span class="font-mono font-bold text-xs ${p.score >= 80 ? 'text-emerald-400' : p.score >= 65 ? 'text-amber-400' : 'text-rose-400'}">${p.score}%</span>
                  </div>
                  <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div class="${p.score >= 80 ? 'bg-emerald-500' : p.score >= 65 ? 'bg-amber-400' : 'bg-rose-500'} h-full rounded-full" style="width: ${p.score}%"></div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- Root-Cause Diagnosis & Integrative Roadmap -->
          <div class="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
            <h4 class="font-bold text-white text-xs flex items-center gap-1.5">
              <span>🔍</span> Primary Clinical Finding &amp; Root-Cause Analysis
            </h4>
            <p class="text-slate-300 text-xs leading-relaxed">
              ${rootCause}
            </p>

            <div class="pt-2 border-t border-slate-800 space-y-2">
              <strong class="text-emerald-400 text-xs block">Immediate 7-Day Dietary &amp; Lifestyle Directive (Parhez wa Ghiza):</strong>
              <p class="text-slate-300 text-xs leading-relaxed bg-slate-900 p-3 rounded-xl border border-slate-800">
                ${recommendedDiet}
              </p>
            </div>
          </div>

          <!-- Targeted Formulation Recommendation -->
          <div class="p-5 rounded-2xl bg-gradient-to-r from-emerald-950/50 via-slate-900 to-slate-950 border border-emerald-500/40 space-y-3">
            <div class="flex justify-between items-start">
              <div>
                <span class="text-[10px] font-mono font-bold text-emerald-400 uppercase tracking-wider block">Targeted Botanical Re-Balancing Formulation</span>
                <h4 class="text-base font-bold text-white mt-0.5">${matchedProd}</h4>
                <p class="text-xs text-slate-300 mt-0.5">Formulated to address your specific ${dominantMizaj} constitutional deviation.</p>
              </div>
              <span class="px-2.5 py-1 rounded-xl bg-emerald-500/20 text-emerald-300 font-mono text-xs font-bold border border-emerald-500/40">
                ${matchedSku}
              </span>
            </div>
            <div class="flex gap-2 pt-1">
              <button onclick="addToHerbalsCart('${matchedSku.toLowerCase()}'); toggleHealthAssessmentModal(false); toggleCheckoutModal();" class="flex-1 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition flex items-center justify-center gap-1.5 cursor-pointer">
                <span>⚡</span> Instant Order Re-Balancing Kit
              </button>
              <button onclick="openProductQuickView('${matchedSku}')" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold rounded-xl border border-slate-700 transition cursor-pointer">
                View Monograph
              </button>
            </div>
          </div>

          <!-- Action Controls & Sharing Bar -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-2">
            <button onclick="downloadHealthDossier(${overallScore}, '${dominantMizaj}', ${functionalAge})" class="p-3 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-xl border border-slate-700 transition flex items-center justify-center gap-2 cursor-pointer">
              <span>📄</span> Download Health Report
            </button>
            <button onclick="shareHealthDossierWhatsApp(${overallScore}, '${dominantMizaj}')" class="p-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl shadow transition flex items-center justify-center gap-2 cursor-pointer">
              <span>💬</span> WhatsApp to Dr. Irfan
            </button>
            <button onclick="window.healthAssessmentState.currentStep=1; renderAssessmentStep();" class="p-3 bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white font-bold rounded-xl border border-slate-800 transition flex items-center justify-center gap-1.5 cursor-pointer">
              <span>🔄</span> Retake Audit
            </button>
          </div>

        </div>
      `;
    }

    function downloadHealthDossier(score, mizaj, functionalAge) {
      const now = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
      const text = `================================================================================
          ZAYVORA HEALTH OS™ — COMPREHENSIVE WHOLE-PERSON HEALTH DOSSIER
                  (Precision Integrative Medicine & Greco-Arab Diagnostics)
================================================================================
CLINICAL INSTITUTION:
  ZAYVORA Healthcare System — Central Hospital
  Conceived & Architected by: Hakeem Dr. Irfan Ashraf (BUMS, AKTC AMU 2002–2007)
  NCISM Registration: BUMS/AMU/2007
  Date & Time: ${now} IST

EXECUTIVE SUMMARY:
  Overall Vitality Index:       ${score} / 100
  Dominant Humoral Temperament: ${mizaj}
  Calendar Age:                 ${window.healthAssessmentState.userAge} Years
  Functional Vitality Age:      ${functionalAge} Years

8-PILLAR FUNCTIONAL BREAKDOWN:
  1. Mizaj & Thermal Equilibrium:            Assessed
  2. Digestive Fire & Metabolism:             Hazm-e-Meda evaluated
  3. Mental Strength & Stress Resilience:     Quwwat-e-Nafsaniyah evaluated
  4. Sleep Architecture & Circadian Rhythm:   Naum wa Yaqzah evaluated
  5. Innate Immunity & Healing Resilience:    Tabiyat Mudabbira-e-Badan evaluated
  6. Toxic Burden & Metabolic Clearance:      Tanqiya & Fuzlaat evaluated
  7. Hormonal Stability & Physical Stamina:   Quwwat-e-Haywaniyah evaluated
  8. Environmental & Lifestyle Harmony:       Asbab-e-Sittah evaluated

RECOMMENDED 7-DAY INTEGRATIVE ACTION PLAN:
  1. Adopt personalized dietary directives matching your humoral deviation.
  2. Maintain 2.5L daily lukewarm water hydration with natural badraqa.
  3. Complete 20 minutes of morning direct solar light exposure before 9:00 AM.
  4. Schedule formal 1-on-1 pulse (Nabz) and clinical consultation with Dr. Irfan Ashraf.

Clinical Guidance Line: +91 98110 44219 / +91 97738 82657
Platform: https://web-production-d5823.up.railway.app
================================================================================`;

      try {
        const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `ZAYVORA_Whole_Person_Health_Report_${Date.now()}.txt`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        showNotification('✓ Health Dossier report downloaded successfully!', 'success');
      } catch (e) {
        showNotification('Report generated.', 'info');
      }
    }

    function shareHealthDossierWhatsApp(score, mizaj) {
      const msg = encodeURIComponent(`Salam Dr. Irfan Ashraf Sahib, I just completed the ZAYVORA 8-Pillar Whole-Person Health Audit on ZAYVORA Health OS. My Overall Vitality Score is ${score}/100 and my dominant temperament is ${mizaj}. I would like to consult with you for my personalized treatment plan.`);
      window.open(`https://wa.me/919773882657?text=${msg}`, '_blank');
    }
'''

print("--- 1. Injecting Assessment Modal into index.html ---")
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    html = f.read()

if 'id="health-assessment-modal"' not in html:
    closing_body = '</body>'
    if closing_body in html:
        html = html.replace(closing_body, ASSESSMENT_MODAL_HTML.strip() + '\n\n' + closing_body)
        print("✓ Injected health-assessment-modal into index.html")

# Also inject a Top Header CTA button for Health Audit
HEADER_AUDIT_BTN = '''        <!-- Free 8-Pillar Health Audit Header CTA -->
        <button onclick="openHealthAssessmentModal()" class="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-cyan-950/60 hover:bg-cyan-900/80 border border-cyan-500/40 text-cyan-300 hover:text-white font-bold text-xs shadow-sm transition cursor-pointer" title="Free 8-Pillar Whole-Person Health Audit">
          <span>🧠</span>
          <span class="hidden lg:inline">Health Audit</span>
        </button>'''

if 'openHealthAssessmentModal()' not in html:
    # Place right before header-cart-btn
    target = '<button id="header-cart-btn"'
    if target in html:
        html = html.replace(target, HEADER_AUDIT_BTN + '\n\n        ' + target)
        print("✓ Injected Health Audit CTA into Top Application Header")

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("--- 2. Injecting Assessment Engine into js/zayvora-core.js ---")
with open(CORE_FILE, "r", encoding="utf-8") as f:
    js = f.read()

if 'window.healthAssessmentState' not in js:
    js += '\n' + ASSESSMENT_JS_ENGINE.strip() + '\n'
    print("✓ Appended healthAssessmentState & Engine to js/zayvora-core.js")

# In Home Page Hero Action Matrix, add high-visibility button
HERO_AUDIT_BTN = '''              <button onclick="openHealthAssessmentModal();" class="px-5 py-3.5 rounded-xl bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 hover:from-emerald-500 text-white font-bold text-xs shadow-xl shadow-emerald-950/50 transition flex items-center gap-2 cursor-pointer ring-2 ring-emerald-400/40">
                <span>🧠</span> Free 8-Pillar Health Audit
              </button>'''

if 'openHealthAssessmentModal()' not in js:
    # Place in Hero action matrix before Order 32 Formulations
    hero_target = '<button onclick="viewWebsitePage(\'products\');"'
    if hero_target in js:
        js = js.replace(hero_target, HERO_AUDIT_BTN + '\n              ' + hero_target)
        print("✓ Injected 'Free 8-Pillar Health Audit' button into Homepage Hero section")

with open(CORE_FILE, "w", encoding="utf-8") as f:
    f.write(js)

print("Script completed successfully.")
