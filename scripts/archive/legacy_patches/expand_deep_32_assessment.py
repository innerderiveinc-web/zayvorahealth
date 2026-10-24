#!/usr/bin/env python3
"""
ZAYVORA Health OS — 32-Question Deep Clinical Health Assessment Engine
Expands the assessment into a deeply engaging, immersive journey:
- 8 Canonical Pillars
- Exactly 4 fascinating questions per pillar = 32 deep questions
- Classical insight quotes from Ibn Sina (Al-Qanoon) & Al-Razi
- Richer scoring, biological age analysis, and comprehensive health dossier
"""

CORE_FILE = "js/zayvora-core.js"

DEEP_32_PILLARS_JS = '''
    // ── ZAYVORA DEEP 32-QUESTION BIO-HUMORAL HEALTH ASSESSMENT ENGINE ────────
    window.healthAssessmentState = {
      currentStep: 1, // 1 to 8 pillars, step 9 = final dossier
      userAge: 36,
      userName: 'Valued Visitor',
      answers: {
        // Pillar 1: Mizaj
        p1_temp: 'moderate',
        p1_thirst: 'lukewarm_sip',
        p1_skin: 'balanced_skin',
        p1_physique: 'balanced_build',
        // Pillar 2: Digestion
        p2_postmeal: 'mild_bloat',
        p2_bowel: 'regular_daily',
        p2_sensitivity: 'dairy_mucus',
        p2_appetite: 'sharp_hunger',
        // Pillar 3: Mental Strength
        p3_stress: 'moderate_worry',
        p3_memory: 'sharp_retention',
        p3_afternoon: 'mild_afternoon_dip',
        p3_mood: 'stable_calm',
        // Pillar 4: Sleep
        p4_latency: 'falls_asleep_15m',
        p4_waking: 'occasional_waking',
        p4_dreams: 'peaceful_dreams',
        p4_morning: 'moderate_fresh',
        // Pillar 5: Immunity
        p5_shift: 'occasional_seasonal',
        p5_healing: 'normal_healing',
        p5_meds: 'rare_medication',
        p5_vitality: 'good_resilience',
        // Pillar 6: Detox
        p6_sweat: 'natural_sweat',
        p6_tongue: 'thin_white',
        p6_breath: 'fresh_neutral',
        p6_puffiness: 'no_puffiness',
        // Pillar 7: Hormones & Stamina
        p7_stamina: 'good_stamina',
        p7_muscle: 'moderate_tone',
        p7_vitality: 'balanced_drive',
        p7_hair_nails: 'strong_hair',
        // Pillar 8: Lifestyle
        p8_screen: 'moderate_screen',
        p8_movement: 'moderate_walks',
        p8_hydration: 'water_tea',
        p8_peace: 'balanced_peace'
      }
    };

    const healthAssessmentPillars = [
      {
        id: 1,
        title: "Pillar 1: Mizaj & Thermal Equilibrium (مزاجِ بدن)",
        subtitle: "The foundation of all metabolic chemistry: Internal Heat (Hararat) vs Cold & Moisture.",
        classicalQuote: "“When the primary qualities are in equilibrium, the body enjoys optimal health.” — Ibn Sina, Al-Qanoon fi al-Tibb",
        questions: [
          {
            key: "p1_temp",
            label: "How does your body naturally respond to ambient climate and temperature?",
            options: [
              { val: "cold_intolerant", text: "Extremely sensitive to cold; hands & feet are always chilly; craves warm blankets", mizaj: "Balghami", score: 60 },
              { val: "heat_intolerant", text: "Extremely sensitive to heat; easily overheated; agitated and restless during hot summers", mizaj: "Safrawi", score: 65 },
              { val: "dry_wind_cold", text: "Aches easily in dry winter winds; stiff joints, dry throat, and skin tightness", mizaj: "Sawdawi", score: 55 },
              { val: "moderate", text: "Adapts smoothly across all seasons; body maintains steady comfortable warmth", mizaj: "Damawi", score: 95 }
            ]
          },
          {
            key: "p1_thirst",
            label: "What temperature and type of water does your throat naturally crave?",
            options: [
              { val: "ice_cold_gulp", text: "Craves ice-cold refrigerated water; drinks in large gulps to quench burning throat", mizaj: "Safrawi", score: 60 },
              { val: "warm_sip", text: "Prefers warm or room-temperature sips; dislikes cold drinks which cause heaviness", mizaj: "Balghami", score: 75 },
              { val: "rarely_thirsty", text: "Often forgets to drink water for hours; dry mouth but rarely feels intense thirst", mizaj: "Sawdawi", score: 65 },
              { val: "lukewarm_sip", text: "Consistent, natural thirst for clean fresh water; satisfied with normal hydration", mizaj: "Damawi", score: 95 }
            ]
          },
          {
            key: "p1_skin",
            label: "How do your skin, complexion, and body tissues feel naturally?",
            options: [
              { val: "cool_soft_pale", text: "Soft, smooth, cool to touch, pale complexion with tendency to retain fluid", mizaj: "Balghami", score: 65 },
              { val: "warm_flushed_oil", text: "Warm to touch, reddish or yellowish undertone, prone to acne or redness", mizaj: "Safrawi", score: 70 },
              { val: "rough_dry_thin", text: "Dry, rough, thin skin with prominent veins; cracked heels and dry cuticles", mizaj: "Sawdawi", score: 60 },
              { val: "balanced_skin", text: "Firm, healthy pinkish tint, supple moisture, and balanced elasticity", mizaj: "Damawi", score: 95 }
            ]
          },
          {
            key: "p1_physique",
            label: "What best describes your bone structure and weight tendency?",
            options: [
              { val: "broad_soft_gain", text: "Broad bone frame, soft musculature; gains weight very easily, struggles to lose it", mizaj: "Balghami", score: 65 },
              { val: "medium_warm_burn", text: "Medium athletic frame; burns calories quickly; loses weight easily when stressed", mizaj: "Safrawi", score: 75 },
              { val: "slender_light_veins", text: "Slender, light frame; hard to put on weight or muscle mass; prominent joints", mizaj: "Sawdawi", score: 60 },
              { val: "balanced_build", text: "Well-proportioned, strong bone density, stable muscle tone and posture", mizaj: "Damawi", score: 95 }
            ]
          }
        ]
      },
      {
        id: 2,
        title: "Pillar 2: Digestive Fire & Gastric Metabolism (ہضم و قوتِ طبعیہ)",
        subtitle: "Evaluates gastric fire (Hazm-e-Meda), hepatic processing, and intestinal microbiome transit.",
        classicalQuote: "“The stomach is the reservoir of the body; if it is sound, the veins flow with health.” — Hakeem Al-Majusi, Kamil al-Sina'a",
        questions: [
          {
            key: "p2_postmeal",
            label: "1 to 2 hours after having a standard meal, what sensation dominates your gut?",
            options: [
              { val: "stone_bloat", text: "Feels like a heavy stone; severe abdominal bloating, gassiness, and drowsiness", score: 50 },
              { val: "burning_reflux", text: "Heartburn, acidity rising up the throat, sour belching or epigastric heat", score: 55 },
              { val: "mild_bloat", text: "Occasional mild fullness, especially after dining out or eating late at night", score: 75 },
              { val: "light_energy", text: "Completely light and comfortable; feels energized and alert with zero discomfort", score: 95 }
            ]
          },
          {
            key: "p2_bowel",
            label: "How would you describe your daily morning bowel habit (Istifragh)?",
            options: [
              { val: "strained_constipated", text: "Constipated: Hard, dry pellets, strained evacuation, or only once every 2 days", score: 45 },
              { val: "irregular_urgency", text: "Unpredictable: Loose, frequent, or sudden post-meal bathroom urgency", score: 60 },
              { val: "regular_daily", text: "Effortless, complete, well-formed morning evacuation without straining", score: 95 }
            ]
          },
          {
            key: "p2_sensitivity",
            label: "What happens when you consume heavy dairy, sweets, cold curd, or rice?",
            options: [
              { val: "dairy_mucus", text: "Excess throat phlegm, nasal congestion, heavy sluggish gut, and cough", score: 55 },
              { val: "chili_burning", text: "Spicy or fried foods cause acute stomach burning, loose motions, or mouth ulcers", score: 55 },
              { val: "sugar_crash", text: "Refined carbs cause intense afternoon sugar crashes and trembling hunger", score: 65 },
              { val: "clean_digestion", text: "Digests standard wholesome foods smoothly without acute flare-ups", score: 95 }
            ]
          },
          {
            key: "p2_appetite",
            label: "How predictable and sharp is your hunger rhythm throughout the day?",
            options: [
              { val: "hangry_sharp", text: "Must eat on time or becomes irritable ('hangry'), shaky, with gastric burning", score: 65 },
              { val: "sluggish_morning", text: "Zero morning appetite; can go without food until 1:00 PM without feeling hungry", score: 60 },
              { val: "erratic_skipping", text: "Erratic appetite; forgets to eat for long stretches, then binges impulsively", score: 50 },
              { val: "sharp_hunger", text: "Clean, rhythmic appetite: feels genuine wholesome hunger at regular meal times", score: 95 }
            ]
          }
        ]
      },
      {
        id: 3,
        title: "Pillar 3: Mental Strength & Psychosomatic Resilience (قوتِ نفسانیہ و روح)",
        subtitle: "Evaluates nervous system tone, cognitive focus, emotional poise, and mental stamina.",
        classicalQuote: "“Psychic states (Infe'alat-e-Nafsaniyah) alter bodily temperature and humors more swiftly than food.” — Ibn Sina",
        questions: [
          {
            key: "p3_stress",
            label: "When confronted with acute deadline pressure, conflict, or unforeseen stress:",
            options: [
              { val: "anxious_overthink", text: "Spirals into repetitive overthinking, chest tightness, shallow breath, and dread", score: 45 },
              { val: "fiery_anger", text: "Immediate surge of anger, impatience, raised voice, and irritability", score: 60 },
              { val: "shutdown_freeze", text: "Emotional numbness, procrastination, withdrawal, and avoidance of decisions", score: 50 },
              { val: "moderate_worry", text: "Brief anxiety or concern, but regains rational composure within an hour", score: 75 },
              { val: "poised_calm", text: "Remains grounded, mentally clear, patient, and problem-solving oriented", score: 95 }
            ]
          },
          {
            key: "p3_memory",
            label: "How does your memory, learning retention, and mental sharpness operate?",
            options: [
              { val: "brain_fog_forget", text: "Frequent brain fog, forgetfulness, losing track of conversations or tasks", score: 50 },
              { val: "quick_grasp_forget", text: "Learns very quickly on the fly, but forgets details just as quickly later", score: 70 },
              { val: "deep_slow_retention", text: "Takes time to process deeply, but once learned, remembers details for years", score: 85 },
              { val: "sharp_retention", text: "Clear mental agility, excellent working memory, and sharp daily focus", score: 95 }
            ]
          },
          {
            key: "p3_afternoon",
            label: "Around 2:00 PM – 4:00 PM, what typically happens to your mental energy?",
            options: [
              { val: "severe_exhaustion", text: "Heavy cognitive exhaustion; feels like brain shuts down without caffeine/sugar", score: 45 },
              { val: "mild_afternoon_dip", text: "Mild, natural lull that resolves with a walk, fresh air, or glass of water", score: 80 },
              { val: "steady_productivity", text: "Maintains clear, sustained focus and productivity throughout the afternoon", score: 95 }
            ]
          },
          {
            key: "p3_mood",
            label: "What emotional climate most accurately describes your day-to-day inner state?",
            options: [
              { val: "melancholic_low", text: "Tendency toward sadness, quiet worry, self-doubt, and inner heaviness", score: 50 },
              { val: "restless_hurry", text: "Constant inner hurry, racing mind, feeling like there is never enough time", score: 60 },
              { val: "stable_calm", text: "Generally cheerful, content, emotionally balanced, and optimistic", score: 95 }
            ]
          }
        ]
      },
      {
        id: 4,
        title: "Pillar 4: Sleep Architecture & Circadian Restoration (نوم و یقظہ)",
        subtitle: "Measures restorative sleep depth, nocturnal hormone release, and vital spirit replenishment.",
        classicalQuote: "“Deep sleep carries innate heat inward to digest humors and restore the vital faculty.” — Al-Razi, Kitab al-Hawi",
        questions: [
          {
            key: "p4_latency",
            label: "What happens when you lay your head on the pillow at night?",
            options: [
              { val: "racing_insomnia", text: "Tossing and turning for 45+ minutes; racing thoughts, checking phone repeatedly", score: 45 },
              { val: "falls_asleep_15m", text: "Falls asleep peacefully within 15–20 minutes without struggle", score: 95 },
              { val: "passes_out_exhausted", text: "Passes out instantly from sheer exhaustion, but wakes up feeling unrested", score: 65 }
            ]
          },
          {
            key: "p4_waking",
            label: "Do you experience nocturnal awakenings, especially around 2:00 AM – 4:00 AM?",
            options: [
              { val: "liver_hour_awake", text: "Consistently jolts awake between 2:00–4:00 AM with racing mind, heat, or thirst", score: 50 },
              { val: "shallow_tossing", text: "Light sleeper; wakes up at every minor noise, movement, or bathroom trip", score: 60 },
              { val: "occasional_waking", text: "Occasionally wakes once, but falls back asleep smoothly", score: 80 },
              { val: "solid_7hours", text: "Sleeps deeply and uninterrupted for 7 to 8 hours straight", score: 95 }
            ]
          },
          {
            key: "p4_dreams",
            label: "What visual themes appear most prominently in your dream life?",
            options: [
              { val: "falling_dark_fears", text: "Falling, being chased, dark enclosed spaces, anxiety, or heavy nightmares", mizaj: "Sawdawi", score: 55 },
              { val: "fire_heat_quarrel", text: "Fires, hot red scenes, arguments, intense energetic battles, or flying", mizaj: "Safrawi", score: 65 },
              { val: "water_ice_snow", text: "Deep water, oceans, swimming, snow, rain, or calm cloudy skies", mizaj: "Balghami", score: 70 },
              { val: "peaceful_dreams", text: "Pleasant, harmonious, creative, or restful dreams that leave a good feeling", mizaj: "Damawi", score: 95 }
            ]
          },
          {
            key: "p4_morning",
            label: "How do you feel in your body and mind during the first 30 minutes of waking?",
            options: [
              { val: "hit_by_truck", text: "Extremely heavy limbs, stiff joints, brain fog; dreads getting out of bed", score: 45 },
              { val: "moderate_fresh", text: "Needs 10–15 minutes and a wash to fully boot up, then feels ready", score: 80 },
              { val: "naturally_energized", text: "Wakes up before alarm with clear mind, light body, and natural morning energy", score: 95 }
            ]
          }
        ]
      },
      {
        id: 5,
        title: "Pillar 5: Innate Immunity & Healing Resilience (قوتِ مدبرہِ بدن)",
        subtitle: "Measures Tabiyat Mudabbira-e-Badan — your body's intrinsic auto-healing and immunological defence.",
        classicalQuote: "“The physician is but the servant of nature; it is Tabiyat that cures the disease.” — Hippocrates",
        questions: [
          {
            key: "p5_shift",
            label: "How does your body hold up during seasonal weather transitions or travel?",
            options: [
              { val: "catches_everything", text: "Immediately catches sore throat, flu, allergies, or cold at every weather change", score: 45 },
              { val: "occasional_seasonal", text: "Gets sick at most once or twice a year, resolving within 4–5 days", score: 80 },
              { val: "rock_solid", text: "Virtually never falls sick; adapts to varying climates and seasons robustly", score: 95 }
            ]
          },
          {
            key: "p5_healing",
            label: "When you get a cut, skin scrape, bruise, or muscle strain, how fast does it heal?",
            options: [
              { val: "slow_healing", text: "Takes weeks to heal; cuts linger, bruise easily, and scars stay discolored", score: 50 },
              { val: "normal_healing", text: "Standard healing within 5 to 7 days without infection or complication", score: 85 },
              { val: "rapid_healing", text: "Rapid tissue repair; cuts and bruises close cleanly in record time", score: 95 }
            ]
          },
          {
            key: "p5_meds",
            label: "How reliant are you on pharmaceutical interventions (painkillers, antibiotics, antacids)?",
            options: [
              { val: "frequent_meds", text: "Takes pills multiple times a month (Headache pills, acidity antacids, allergy meds)", score: 45 },
              { val: "rare_medication", text: "Only takes conventional medicine in rare emergencies; body resolves issues naturally", score: 95 }
            ]
          },
          {
            key: "p5_vitality",
            label: "If you are forced to miss one meal or sleep late for one night, what happens?",
            options: [
              { val: "complete_crash", text: "Crashes with severe migraine, gastric burning, dizziness, or intense fatigue", score: 45 },
              { val: "good_resilience", text: "Noticeable fatigue, but handles the day smoothly and rebounds with a good night's rest", score: 95 }
            ]
          }
        ]
      },
      {
        id: 6,
        title: "Pillar 6: Toxic Burden & Metabolic Clearance (تنقیہ و فضلات)",
        subtitle: "Evaluates lymphatic drainage, natural perspiration, and elimination of metabolic wastes (Fuzlaat).",
        classicalQuote: "“Retention of that which ought to be evacuated causes the most grievous humoral combustions.” — Ibn Sina",
        questions: [
          {
            key: "p6_sweat",
            label: "How does your body naturally sweat during exertion, exercise, or hot weather?",
            options: [
              { val: "rarely_sweats_dry", text: "Rarely sweats at all; dry tight pores; overheats internally without perspiration", score: 50 },
              { val: "pungent_clammy", text: "Excessive, clammy, sour or pungent sweat that stains clothing or irritates skin", score: 60 },
              { val: "natural_sweat", text: "Clean, natural, odorless sweating that comfortably cools the body down", score: 95 }
            ]
          },
          {
            key: "p6_tongue",
            label: "When you inspect your tongue in the mirror first thing in the morning (Lisan):",
            options: [
              { val: "thick_white", text: "Thick white or greyish coating; sticky saliva; tasteless or sweetish morning mouth", mizaj: "Balghami", score: 50 },
              { val: "yellow_bitter", text: "Yellowish coating; dry mouth; bitter taste; red tip or sides", mizaj: "Safrawi", score: 55 },
              { val: "dark_dry_cracked", text: "Dry, darkish, rough or cracked tongue surface; astringent/sour taste", mizaj: "Sawdawi", score: 50 },
              { val: "thin_white", text: "Clean pink body with a thin healthy translucent white film; fresh mouth", mizaj: "Damawi", score: 95 }
            ]
          },
          {
            key: "p6_breath",
            label: "How would you assess your breath and bodily scent throughout the day?",
            options: [
              { val: "sour_morning_breath", text: "Frequent sour/foul morning breath, tongue halitosis, or metallic taste", score: 55 },
              { val: "fresh_neutral", text: "Clean, fresh, and neutral oral scent with natural hydration", score: 95 }
            ]
          },
          {
            key: "p6_puffiness",
            label: "Do you notice fluid accumulation, under-eye bags, or puffy fingers in the morning?",
            options: [
              { val: "chronic_puffiness", text: "Frequently wakes with puffy eyelids, swollen fingers, or heavy water retention", score: 50 },
              { val: "evening_ankle_swell", text: "Swelling in ankles/feet toward the end of the day after standing or sitting", score: 60 },
              { val: "no_puffiness", text: "Crisp facial contours, light extremities, and zero water retention", score: 95 }
            ]
          }
        ]
      },
      {
        id: 7,
        title: "Pillar 7: Hormonal Stability, Stamina & Vitality (قوتِ حیوانیہ و باہ)",
        subtitle: "Evaluates mitochondrial stamina, endocrine homeostasis, and reproductive vitality.",
        classicalQuote: "“The reproductive essence (Mani) is the quintessence of all digested humors.” — Al-Majusi",
        questions: [
          {
            key: "p7_stamina",
            label: "When climbing 3 flights of stairs or engaging in 20 minutes of brisk activity:",
            options: [
              { val: "severe_breathless", text: "Severe breathlessness, heart pounding in ears, heavy trembling legs", score: 45 },
              { val: "good_stamina", text: "Heart rate elevates naturally, recovers breath smoothly within 2 minutes", score: 95 }
            ]
          },
          {
            key: "p7_muscle",
            label: "How would you describe your muscular recovery and physical tone?",
            options: [
              { val: "sore_for_days", text: "Muscles stay achy, stiff, and sore for 3 to 4 days after modest exertion", score: 50 },
              { val: "moderate_tone", text: "Mild soreness that resolves cleanly within 24 hours; good functional tone", score: 95 }
            ]
          },
          {
            key: "p7_vitality",
            label: "How stable is your natural vitality, reproductive health, and libido drive?",
            options: [
              { val: "chronic_low_drive", text: "Noticeable loss of vitality, chronic hormonal fatigue, low drive and enthusiasm", score: 45 },
              { val: "fluctuating_stress", text: "Fluctuates with work stress and sleep deprivation, but recovers on weekends", score: 75 },
              { val: "balanced_drive", text: "Robust natural vitality, stable hormonal balance, and vigorous physical enthusiasm", score: 95 }
            ]
          },
          {
            key: "p7_hair_nails",
            label: "What is the health status of your hair, scalp, and fingernails?",
            options: [
              { val: "shedding_brittle", text: "Excessive hair fall/thinning, dry brittle nails with ridges, or chronic dandruff", score: 50 },
              { val: "premature_grey", text: "Premature greying or thinning hair accompanied by internal body heat", score: 65 },
              { val: "strong_hair", text: "Thick, lustrous hair, strong smooth nails with healthy pink lunula beds", score: 95 }
            ]
          }
        ]
      },
      {
        id: 8,
        title: "Pillar 8: Environmental, Social & Lifestyle Harmony (اسبابِ ستہ ضروریہ)",
        subtitle: "Evaluates your daily alignment with natural light, movement, air quality, and social peace.",
        classicalQuote: "“Life is maintained by six essential prerequisites (Asbab-e-Sittah الضرورية); neglect of any one unbalances nature.” — Ibn Sina",
        questions: [
          {
            key: "p8_screen",
            label: "What is your daily balance between artificial screen blue-light vs natural sunlight?",
            options: [
              { val: "extreme_screen_nosun", text: "10+ hours staring at digital screens; less than 15 minutes of direct outdoor sunlight", score: 45 },
              { val: "moderate_screen", text: "6–8 hours screen work, but spends 20–30 minutes outdoors during morning/evening", score: 80 },
              { val: "sunlight_priority", text: "Active outdoor habits, daily morning sun exposure, and strict digital sunset curfews", score: 95 }
            ]
          },
          {
            key: "p8_movement",
            label: "How much of your typical working day is spent seated in one stationary posture?",
            options: [
              { val: "sedentary_8hours", text: "Seated continuously for 8+ hours with minimal movement or postural breaks", score: 45 },
              { val: "moderate_walks", text: "Desk work, but takes frequent stretch breaks and clocks 6,000–8,000 daily steps", score: 85 },
              { val: "active_day", text: "Vigorous, active daily routine with 10,000+ steps and physical movement", score: 95 }
            ]
          },
          {
            key: "p8_hydration",
            label: "What is the primary vehicle of your daily fluid and drink intake?",
            options: [
              { val: "caffeine_sodas", text: "Relies heavily on multiple coffees, strong chais, energy drinks, or sweet sodas", score: 50 },
              { val: "water_tea", text: "2.5 to 3 liters of clean water, herbal infusions, and minimal stimulants", score: 95 }
            ]
          },
          {
            key: "p8_peace",
            label: "How would you describe your emotional support network and daily inner peace?",
            options: [
              { val: "isolated_overwhelmed", text: "Isolated, carrying immense pressure alone; constant background anxiety and worry", score: 45 },
              { val: "moderate_support", text: "Busy life with normal family/social bonds, occasional stress that resolves", score: 80 },
              { val: "balanced_peace", text: "Deep inner spiritual serenity, loving family/community support, and clear purpose", score: 95 }
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
        if (counterLabel) counterLabel.innerText = `Pillar ${state.currentStep} of 8 (4 Questions • ${Math.round((state.currentStep / 8) * 100)}%)`;
        if (prevBtn) prevBtn.disabled = (state.currentStep === 1);
        if (nextBtn) {
          nextBtn.innerHTML = state.currentStep === 8 ? '<span>Analyze &amp; Generate Dossier</span> <span>⚡</span>' : '<span>Next Pillar</span> <span>&rarr;</span>';
        }

        body.innerHTML = `
          <div class="space-y-6">
            <!-- Pillar Intro Card with Classical Doctrine Quote -->
            <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-wider">Clinical Diagnostic Pillar 0${pillar.id}</span>
                <span class="text-[10px] text-slate-500 font-mono">4 Diagnostic Nodes</span>
              </div>
              <h4 class="text-sm font-bold text-white">${pillar.title}</h4>
              <p class="text-xs text-slate-300 leading-relaxed">${pillar.subtitle}</p>
              ${pillar.classicalQuote ? `
                <div class="p-2.5 rounded-xl bg-emerald-950/30 border border-emerald-500/20 text-[11px] text-emerald-300 italic font-serif">
                  ${pillar.classicalQuote}
                </div>
              ` : ''}
            </div>

            <!-- 4 Questions for this Pillar -->
            <div class="space-y-5">
              ${pillar.questions.map((q, qIdx) => `
                <div class="space-y-2.5 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
                  <label class="block text-xs font-bold text-slate-200">
                    <span class="text-emerald-400 font-mono mr-1.5">${(pillar.id - 1) * 4 + qIdx + 1}.</span> ${q.label}
                  </label>
                  <div class="grid grid-cols-1 gap-2 pt-1">
                    ${q.options.map(opt => {
                      const isSelected = state.answers[q.key] === opt.val;
                      return `
                        <div onclick="selectAssessmentAnswer('${q.key}', '${opt.val}')" class="p-3 rounded-xl border transition cursor-pointer flex items-center justify-between ${isSelected ? 'border-emerald-500 bg-emerald-950/40 text-white shadow-md ring-1 ring-emerald-500' : 'border-slate-800 bg-slate-900/80 hover:bg-slate-900 hover:border-slate-700 text-slate-300'}">
                          <div class="flex items-center gap-2.5">
                            <span class="w-4 h-4 rounded-full border flex items-center justify-center shrink-0 ${isSelected ? 'border-emerald-500 bg-emerald-500 text-slate-950 font-bold text-[10px]' : 'border-slate-700'}">
                              ${isSelected ? '✓' : ''}
                            </span>
                            <span class="text-xs leading-relaxed">${opt.text}</span>
                          </div>
                          ${opt.mizaj ? `<span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-950 border border-slate-700 text-emerald-300 font-semibold shrink-0 ml-2">${opt.mizaj}</span>` : ''}
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
        // Step 9: Render Comprehensive 32-Point Visual Health Dossier Report
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
      if (footer) footer.classList.add('hidden');
      if (subtitle) subtitle.innerHTML = '<strong>Comprehensive 32-Point Health Dossier Generated</strong> • Verified by Hakeem Dr. Irfan Ashraf';
      if (progressBar) progressBar.style.width = '100%';

      // Calculate Pillar Scores across all 32 questions
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
      let ageDelta = 0;
      if (overallScore < 60) ageDelta = 7;
      else if (overallScore < 70) ageDelta = 4;
      else if (overallScore < 85) ageDelta = 1;
      else ageDelta = -4; // Younger biological vitality!
      const functionalAge = calendarAge + ageDelta;

      // Determine Primary Su-e-Mizaj & Root Cause
      let dominantMizaj = "Balghami (Cold-Moist / Phlegmatic)";
      let rootCause = "Sluggish gastric agni (Hazm-e-Meda), accumulated Phlegm (Khilt-e-Balgham), morning fatigue, and blue-light circadian disruption.";
      let matchedSku = "ZAY-001";
      let matchedProd = "ZAYVORA TensioCalm™";
      let recommendedDiet = "Favor warm carminative teas (Ajwain, Zanjabeel/Ginger, Cumin, Cinnamon). Strictly eliminate iced water, sour curds, and heavy refined starches.";

      if (state.answers.p1_temp === 'heat_intolerant' || state.answers.p2_postmeal === 'burning_reflux' || state.answers.p4_dreams === 'fire_heat_quarrel') {
        dominantMizaj = "Safrawi (Hot-Dry / Bilious)";
        rootCause = "Elevated biliary heat (Khilt-e-Safra), gastric hyperacidity, sympathetic nervous overdrive, and nocturnal liver-hour waking.";
        matchedSku = "ZAY-003";
        matchedProd = "ZAYVORA LiverPrime Core™";
        recommendedDiet = "Favor cooling mucilaginous badraqa (Tukhm-e-Balanga, Arq Shahtarra, Cucumber, Pomegranate, Isabgol). Strictly avoid fried chillies, vinegar, and excessive red meat.";
      } else if (state.answers.p1_temp === 'dry_wind_cold' || state.answers.p3_stress === 'anxious_overthink' || state.answers.p4_dreams === 'falling_dark_fears') {
        dominantMizaj = "Sawdawi (Cold-Dry / Melancholic)";
        rootCause = "Elevated Black Bile combustion (Khilt-e-Sawda), nervous hypersensitivity, dry connective tissue, and prolonged sleep latency.";
        matchedSku = "ZAY-005";
        matchedProd = "ZAYVORA NeuroCalmX™";
        recommendedDiet = "Favor warm almond milk with saffron & honey, stewed apples, and warm foot massage with Roghan Banafsha. Avoid stale reheated foods, excessive lentils, and caffeine.";
      } else if (overallScore >= 85) {
        dominantMizaj = "Motadil Damawi (Balanced Sanguine)";
        rootCause = "Strong physiological equilibrium with minor seasonal adaptations needed to maintain optimal longevity.";
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
                <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400 block">ZAYVORA 32-Node Whole-Person Vitality Score</span>
                <h3 class="text-xl font-black text-white mt-0.5">${overallScore >= 80 ? 'Optimal Humoral Equilibrium' : overallScore >= 65 ? 'Moderate Functional Dyscrasia' : 'Substantial Humoral Imbalance (Needs Tanqiya)'}</h3>
                <p class="text-xs text-slate-300 mt-1">Dominant Temperament: <strong class="text-emerald-300">${dominantMizaj}</strong></p>
              </div>
            </div>

            <!-- Biological Age Card -->
            <div class="p-4 rounded-2xl bg-slate-950/90 border border-slate-800 text-center shrink-0 w-full md:w-auto">
              <span class="text-[10px] text-slate-400 block">Functional Vitality Age:</span>
              <div class="text-2xl font-black font-mono ${ageDelta > 0 ? 'text-amber-400' : 'text-emerald-400'}">${functionalAge} Years</div>
              <span class="text-[10px] text-slate-400">Calendar Age: ${calendarAge} (${ageDelta > 0 ? '+' + ageDelta + ' yrs stress load' : 'Youthful Longevity!'})</span>
            </div>
          </div>

          <!-- 8-Pillar Visual Breakdown -->
          <div class="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
            <h4 class="font-bold text-white text-xs flex items-center justify-between">
              <span>8-Pillar Functional Breakdown (32 Clinical Nodes)</span>
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
'''

print("--- Updating js/zayvora-core.js with 32-Question Engine ---")
with open(CORE_FILE, "r", encoding="utf-8") as f:
    js = f.read()

# Replace the older healthAssessmentPillars block with the expanded 32-question block
start_marker = "// ── ZAYVORA COMPREHENSIVE 8-PILLAR WHOLE-PERSON HEALTH ASSESSMENT ENGINE ──"
end_marker = "function shareHealthDossierWhatsApp(score, mizaj) {"

if start_marker in js:
    pre = js.split(start_marker)[0]
    remainder = js.split(start_marker)[1]
    # find where shareHealthDossierWhatsApp ends
    post = remainder.split(end_marker)[1]
    # find closing brace of shareHealthDossierWhatsApp
    post_clean = post.split("}", 1)[1]

    new_js = pre + DEEP_32_PILLARS_JS.strip() + "\n\n    function shareHealthDossierWhatsApp(score, mizaj) {" + post.split("}", 1)[0] + "}\n" + post_clean
    with open(CORE_FILE, "w", encoding="utf-8") as f:
        f.write(new_js)
    print("✓ Successfully replaced with 32-Question Deep Clinical Engine in js/zayvora-core.js")
else:
    print("! Marker not found in js/zayvora-core.js")

print("Script finished.")
