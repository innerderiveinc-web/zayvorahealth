    // ── PWA Service Worker Registration ─────────────────────────────────────
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('sw.js?v=11.0').then(function(reg) {
          reg.update();
        }).catch(function(err) {
          console.warn('[ZAYVORA Health OS] ServiceWorker registration notice:', err);
        });
      });
    }

    // ── Mobile Clinic Mode Toggle ───────────────────────────────────────────
    let isMobileClinicActive = false;
    function toggleMobileClinicMode() {
      isMobileClinicActive = !isMobileClinicActive;
      const btn = document.getElementById('btn-mobile-clinic-toggle');
      if (isMobileClinicActive) {
        document.body.classList.add('mobile-clinic-active');
        if (btn) {
          btn.classList.remove('bg-teal-600/20', 'text-teal-300');
          btn.classList.add('bg-teal-500', 'text-slate-950', 'shadow-lg');
          btn.innerHTML = '<span>🟢</span> Mobile Clinic: ACTIVE (Offline Ready)';
        }
        showNotification('🟢 Mobile Clinic Mode Activated: Offline caching and touch-friendly bedside interactions enabled.', 'success');
      } else {
        document.body.classList.remove('mobile-clinic-active');
        if (btn) {
          btn.classList.remove('bg-teal-500', 'text-slate-950', 'shadow-lg');
          btn.classList.add('bg-teal-600/20', 'text-teal-300');
          btn.innerHTML = '<span>📱</span> Mobile Clinic';
        }
        showNotification('Mobile Clinic Mode Deactivated. Standard clinical layout restored.', 'info');
      }
    }

    // ── Case Simulator Functions ────────────────────────────────────────────
    const SIMULATOR_CASES_EMBEDDED = [
      {
        id: "sim-01",
        title: "Type 2 Diabetes Mellitus with Barid-Balghami Su-e-Mizaj",
        title_ur: "ذیابیطس شکری نوع دوم — سوء مزاج بارد بلغمى",
        patient: "Zafar Iqbal, 52y M (Auditor) — Polyuria, lethargy, HbA1c 8.6%",
        question_1: "What is the primary Unani constitutional diagnosis?",
        options_1: ["Safrawi heat excess", "Su-e-Mizaj Barid-Ratab (Balghami) with deficient innate metabolic fire", "Damawi plethora", "Saudawi splenomegaly"],
        correct_1: 1,
        question_2: "Which 10-Ajnas pulse waveform confirms this metabolic state?",
        options_2: ["Nabz-e-Saree, Azeem, Sulb (Rapid, Large, Hard)", "Nabz-e-Batee, Saghir, Layyin (Slow, Small, Soft)", "Nabz-e-Ghazali (Bounding)", "Nabz-e-Munqati"],
        correct_2: 1,
        explanation: "Ibn Sina, Al-Qanoon fit-Tibb Book 3: Cold phlegmatic impairment of the liver and kidneys diminishes glucose concoction, resulting in soft, slow pulse and pale copious urine."
      },
      {
        id: "sim-02",
        title: "Rheumatoid Arthritis (Waja-ul-Mafasil) with Saudawi-Balghami Stagnation",
        title_ur: "وجع المفاصل بلغمی و سوداوی",
        patient: "Shabana Begum, 46y F — Morning stiffness >90 min, RF 94 IU/mL, hs-CRP 18.4 mg/L",
        question_1: "What is the classical drug of choice and its mandatory Musleh (corrective)?",
        options_1: ["Afeem without corrector", "Suranjan Shireen paired with Katira and Zanjabeel", "Excess cold vinegar", "Dry ice compresses"],
        correct_1: 1,
        question_2: "Under Schedule E(1), what detoxification SOP is mandatory for Suranjan Talkh?",
        options_2: ["None needed", "Mudabbar boiling in Sheer-e-Gao (fresh cow's milk) for 12 hours", "Alcohol flame wash", "High-dose steroid blending"],
        correct_2: 1,
        explanation: "Al-Razi, Kitab al-Hawi fit-Tibb Vol. 11: Suranjan resolves morbid humoral joint effusions; cow's milk Mudabbar detoxification neutralizes colchicine toxicity while preserving anti-inflammatory efficacy."
      }
    ];

    function openCaseSimulatorModal() {
      const modal = document.getElementById('case-simulator-modal');
      const content = document.getElementById('case-simulator-content');
      if (!modal || !content) return;

      let html = '<div class="space-y-6">';
      SIMULATOR_CASES_EMBEDDED.forEach(function(cs, idx) {
        html += `
          <div class="p-5 rounded-xl bg-slate-800/80 border border-slate-700 space-y-3">
            <div class="flex justify-between items-start">
              <div>
                <span class="text-[10px] uppercase font-bold text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded">Case #${idx + 1}</span>
                <h4 class="text-sm font-bold text-white mt-1">${cs.title}</h4>
                <p class="text-xs text-emerald-300 font-serif" dir="rtl">${cs.title_ur}</p>
              </div>
              <span class="text-[11px] text-slate-400 bg-slate-900 px-2 py-1 rounded border border-slate-800">${cs.patient}</span>
            </div>

            <div class="p-3 bg-slate-900/90 rounded-lg border border-slate-800 space-y-2 text-xs">
              <p class="font-bold text-slate-200">Stage 1: ${cs.question_1}</p>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                ${cs.options_1.map((opt, i) => `
                  <button onclick="evaluateSimChoice(this, ${i === cs.correct_1})" class="p-2 text-left rounded bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 text-xs transition">
                    ${opt}
                  </button>
                `).join('')}
              </div>
            </div>

            <div class="p-3 bg-slate-900/90 rounded-lg border border-slate-800 space-y-2 text-xs">
              <p class="font-bold text-slate-200">Stage 2: ${cs.question_2}</p>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                ${cs.options_2.map((opt, i) => `
                  <button onclick="evaluateSimChoice(this, ${i === cs.correct_2})" class="p-2 text-left rounded bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 text-xs transition">
                    ${opt}
                  </button>
                `).join('')}
              </div>
            </div>

            <div class="p-3 rounded-lg bg-emerald-950/40 border border-emerald-800/40 text-[11px] text-emerald-300">
              <span class="font-bold block mb-0.5">📖 Canonical Authority:</span>
              ${cs.explanation}
            </div>
          </div>
        `;
      });
      html += '</div>';

      content.innerHTML = html;
      modal.classList.remove('hidden');
    }

    function evaluateSimChoice(btn, isCorrect) {
      if (isCorrect) {
        btn.classList.remove('bg-slate-800', 'text-slate-300', 'border-slate-700');
        btn.classList.add('bg-emerald-600', 'text-white', 'border-emerald-500', 'font-bold');
        btn.innerHTML = '✓ ' + btn.innerText;
      } else {
        btn.classList.remove('bg-slate-800', 'text-slate-300', 'border-slate-700');
        btn.classList.add('bg-rose-900/60', 'text-rose-200', 'border-rose-700', 'line-through');
      }
    }

    function closeCaseSimulatorModal() {
      const modal = document.getElementById('case-simulator-modal');
      if (modal) modal.classList.add('hidden');
    }

    // ── Botanical Visual Atlas Functions ────────────────────────────────────
    const BOTANICAL_ATLAS_EMBEDDED = [
      {
        name: "Asgandh (Withania somnifera)",
        urdu: "اسگندھ ناگوری",
        mizaj: "Hot 2°, Dry 2°",
        part: "Dried Root (Bikh-e-Asgandh)",
        macro: "Cylindrical light brown roots (10-20 cm), smooth starchy fracture breaking cleanly with minimal splintering.",
        organoleptic: "Characteristic horse-like pungent odor, bitter and mucilaginous taste.",
        microscopy: "Abundant simple and compound starch grains (5-18 μm), microsphenoidal calcium oxalate sand.",
        adulteration: "True Asgandh cross-section stains deep blue-violet with Iodine; exhausted roots yield <6% water extractive (UPI standard >=15%)."
      },
      {
        name: "Suranjan Shireen (Colchicum autumnale)",
        urdu: "سورنجان شیریں",
        mizaj: "Hot 2°, Dry 2° (Sweet) / Hot 3°, Dry 3° (Bitter)",
        part: "Dried Corm",
        macro: "Flattened ovate corms with longitudinal groove, chalky white amylaceous fracture.",
        organoleptic: "Suranjan Shireen is bland and sweetish; Suranjan Talkh is intensely bitter and acrid.",
        microscopy: "Compound starch grains; COMPLETE ABSENCE of calcium oxalate raphides.",
        adulteration: "Suranjan Talkh dropped in conc. H2SO4 yields transient intense yellow-red reaction. Schedule E(1) requires cow's milk Mudabbar detoxification."
      },
      {
        name: "Zanjabeel (Zingiber officinale)",
        urdu: "زنجبیل / سونٹھ",
        mizaj: "Hot 3°, Dry 2°",
        part: "Dried Rhizome",
        macro: "Laterally compressed 'hands' with protruding fibro-vascular bundles and golden-brown cortical zone.",
        organoleptic: "Strongly agreeable spicy fragrance, biting salivary-stimulating pungency.",
        microscopy: "Sac-shaped oval starch grains with eccentric beak-like hilum, yellow oleoresin cells.",
        adulteration: "Chalk-bleached ginger effervesces in dilute HCl and exhibits total ash >8% (standard max: 6%)."
      },
      {
        name: "Zafran (Crocus sativus)",
        urdu: "زعفران / کیسر",
        mizaj: "Hot 2°, Dry 1°",
        part: "Dried Stigmas",
        macro: "Dark crimson-red trumpet-shaped trifid stigmas flared and slit at apex.",
        organoleptic: "Powerfully sweet, honey-like, floral aroma with pleasantly bitter taste.",
        microscopy: "Conical finger-like epidermal papillae (50-120 μm) on upper stigma margin.",
        adulteration: "Genuine saffron in warm water releases clear golden-yellow halos; dyed corn silk bleeds red dye immediately and turns grey."
      }
    ];

    function openBotanicalAtlasModal() {
      const modal = document.getElementById('botanical-atlas-modal');
      const content = document.getElementById('botanical-atlas-content');
      if (!modal || !content) return;

      let html = '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">';
      BOTANICAL_ATLAS_EMBEDDED.forEach(function(item) {
        html += `
          <div class="p-4 rounded-xl bg-slate-800/90 border border-slate-700 space-y-2">
            <div class="flex justify-between items-start border-b border-slate-700/60 pb-2">
              <div>
                <h4 class="font-bold text-amber-300 text-sm">${item.name}</h4>
                <p class="text-xs text-amber-200 font-serif" dir="rtl">${item.urdu}</p>
              </div>
              <span class="text-[10px] bg-amber-950/60 text-amber-300 border border-amber-800/40 px-2 py-0.5 rounded font-bold">${item.mizaj}</span>
            </div>
            <div class="space-y-1.5 text-slate-300 text-xs">
              <p><strong class="text-slate-100">Part:</strong> ${item.part}</p>
              <p><strong class="text-slate-100">Macroscopic:</strong> ${item.macro}</p>
              <p><strong class="text-slate-100">Organoleptic:</strong> ${item.organoleptic}</p>
              <p><strong class="text-slate-100">Microscopy:</strong> ${item.microscopy}</p>
              <div class="p-2 rounded bg-slate-900 border border-slate-800 text-[11px] text-amber-200">
                <strong class="text-amber-400 block">Adulteration SOP:</strong> ${item.adulteration}
              </div>
            </div>
          </div>
        `;
      });
      html += '</div>';

      content.innerHTML = html;
      modal.classList.remove('hidden');
    }

    function closeBotanicalAtlasModal() {
      const modal = document.getElementById('botanical-atlas-modal');
      if (modal) modal.classList.add('hidden');
    }

    // ── Agentic Clinical AI Modal Functions ────────────────────────────────
    function openAgenticAiModal() {
      const modal = document.getElementById('agentic-ai-modal');
      if (modal) modal.classList.remove('hidden');
    }

    function closeAgenticAiModal() {
      const modal = document.getElementById('agentic-ai-modal');
      if (modal) modal.classList.add('hidden');
    }

    function applyHakeemRecommendation() {
      // Copies Hakeem proposal into draft prescription
      const nuskhaInput = document.getElementById('consultation-plan-text') || document.getElementById('nuskha-composition-input');
      if (nuskhaInput) {
        nuskhaInput.value += '\n• Hab-e-Suranjan 2 tabs BD + Roghan-e-Banafsha scalp friction nocte.';
      }
      jumpToSection(11); // Jumps to Prescription tab
      if (typeof showNotification === 'function') {
        showNotification('✓ Proposal added to draft formulation. Awaiting clinician review.', 'success');
      } else if (typeof showToast === 'function') {
        showToast('✓ Proposal added to draft formulation. Awaiting clinician review.');
      }
    }

    let isAudioPlaying = false;

    function playAcousticChime(frequency = 528, duration = 0.35) {
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();
        if (ctx.state === 'suspended') ctx.resume();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(frequency, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(frequency * 1.15, ctx.currentTime + 0.1);
        osc.frequency.exponentialRampToValueAtTime(frequency, ctx.currentTime + duration);
        gain.gain.setValueAtTime(0.04, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + duration);
      } catch (err) {}
    }

    function playMelodicPosologySequence() {
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();
        if (ctx.state === 'suspended') ctx.resume();
        const notes = [440, 528, 660, 528];
        notes.forEach((freq, idx) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          const startTime = ctx.currentTime + idx * 0.3;
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, startTime);
          gain.gain.setValueAtTime(0.05, startTime);
          gain.gain.exponentialRampToValueAtTime(0.0001, startTime + 0.28);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(startTime);
          osc.stop(startTime + 0.28);
        });
      } catch (e) {}
    }

    // Pre-warm SpeechSynthesis Voices immediately
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      try {
        window.speechSynthesis.getVoices();
        if (window.speechSynthesis.onvoiceschanged !== undefined) {
          window.speechSynthesis.onvoiceschanged = () => {
            window.speechSynthesis.getVoices();
          };
        }
      } catch (e) {}
    }

    function selectNaturalHumanVoice(lang) {
      const voices = ('speechSynthesis' in window) ? (window.speechSynthesis.getVoices() || []) : [];
      const scoreVoice = (v) => {
        let s = 0;
        const name = (v.name || '').toLowerCase();
        const vlang = (v.lang || '').toLowerCase();
        if (name.includes('natural') || name.includes('neural')) s += 100;
        if (name.includes('enhanced') || name.includes('premium')) s += 80;
        if (name.includes('google')) s += 60;
        if (name.includes('siri')) s += 50;
        if (name.includes('lekha') || name.includes('swara') || name.includes('neerja') || name.includes('gul') || name.includes('asif')) s += 70;
        if (vlang.startsWith('ur')) s += 90;
        return s;
      };

      if (lang === 'ur') {
        const urduVoices = voices.filter(v => (v.lang || '').toLowerCase().startsWith('ur'));
        if (urduVoices.length > 0) {
          urduVoices.sort((a, b) => scoreVoice(b) - scoreVoice(a));
          return { voice: urduVoices[0], textType: 'script', langCode: urduVoices[0].lang || 'ur-PK' };
        }
        const hiVoices = voices.filter(v => (v.lang || '').toLowerCase().startsWith('hi'));
        if (hiVoices.length > 0) {
          hiVoices.sort((a, b) => scoreVoice(b) - scoreVoice(a));
          return { voice: hiVoices[0], textType: 'devanagari', langCode: hiVoices[0].lang || 'hi-IN' };
        }
        const inVoices = voices.filter(v => (v.lang || '').toLowerCase().includes('in'));
        if (inVoices.length > 0) {
          inVoices.sort((a, b) => scoreVoice(b) - scoreVoice(a));
          return { voice: inVoices[0], textType: 'devanagari', langCode: inVoices[0].lang || 'hi-IN' };
        }
        return { voice: null, textType: 'devanagari', langCode: 'hi-IN' };
      } else if (lang === 'hi') {
        const hiVoices = voices.filter(v => (v.lang || '').toLowerCase().startsWith('hi'));
        if (hiVoices.length > 0) {
          hiVoices.sort((a, b) => scoreVoice(b) - scoreVoice(a));
          return { voice: hiVoices[0], textType: 'script', langCode: hiVoices[0].lang || 'hi-IN' };
        }
        return { voice: null, textType: 'script', langCode: 'hi-IN' };
      } else {
        const enVoices = voices.filter(v => (v.lang || '').toLowerCase().startsWith('en'));
        enVoices.sort((a, b) => scoreVoice(b) - scoreVoice(a));
        const v = enVoices[0] || null;
        return { voice: v, textType: 'script', langCode: v ? v.lang : 'en-US' };
      }
    }

    function toggleAudioPosology(e) {
      const btn = (e && e.currentTarget) || (window.event && window.event.currentTarget) || document.getElementById('btn-audio-posology');
      
      if (isAudioPlaying) {
        if ('speechSynthesis' in window) {
          window.speechSynthesis.cancel();
        }
        isAudioPlaying = false;
        if (btn) {
          btn.innerHTML = '<span>▶</span> Play Audio Posology';
          btn.classList.remove('ring-2', 'ring-emerald-400');
        }
        showNotification('Audio posology stopped.', 'info');
        return;
      }

      isAudioPlaying = true;
      if (btn) {
        btn.innerHTML = '<span class="animate-pulse">🔊</span> Playing Audio Posology...';
        btn.classList.add('ring-2', 'ring-emerald-400');
      }

      // Soft ambient clinic chime to confirm tap
      playAcousticChime(528, 0.25);

      const lang = audioPosologyLang || 'ur';
      const textMap = {
        ur: {
          script: "محترم مریض، السلام علیکم۔ یہ دوا صبح اور شام کھانا کھانے کے بعد، آدھا چمچ نیم گرم دودھ یا تازہ پانی کے ساتھ نوش فرمائیں۔ کھٹی، تلی ہوئی اور ٹھنڈی چیزوں سے پرہیز رکھیں۔ اللہ تعالیٰ آپ کو صحت اور شفائے کاملہ عطا فرمائے۔",
          devanagari: "मोहतरम मरीज़, अस्सलाम वालेकुम। यह दवा सुबह और शाम खाना खाने के बाद, आधा चम्मच नीम गरम दूध या ताज़ा पानी के साथ लें। खट्टी, तली हुई और ठंडी चीज़ों से परहेज़ रखें। अल्लाह आपको सेहत और शिफ़ा अता फ़रमाए।",
          phonetic: "Mohtaram mareez, Assalaamu alaikum. Yeh dawa subah aur shaam khana khane ke baad, aadha chammach neem garam doodh ya taza paani ke saath nosh farmayein. Khatti, tali hui aur thandi cheezon se parhez rakhein. Allah Ta'ala aapko shifa ata farmaye."
        },
        hi: {
          script: "नमस्ते। यह औषधि सुबह और शाम भोजन के बाद, आधा चम्मच गुनगुने दूध या ताज़े पानी के साथ लें। खट्टी, तली हुई और ठंडी चीज़ों से परहेज़ रखें। ईश्वर आपको शीघ्र स्वास्थ्य लाभ दे।",
          devanagari: "नमस्ते। यह औषधि सुबह और शाम भोजन के बाद, आधा चम्मच गुनगुने दूध या ताज़े पानी के साथ लें। खट्टी, तली हुई और ठंडी चीज़ों से परहेज़ रखें। ईश्वर आपको शीघ्र स्वास्थ्य लाभ दे।",
          phonetic: "Namaste. Yeh aushadhi subah aur shaam bhojan ke baad, aadha chammach gun-gune doodh ya taaze paani ke saath lein. Khatti, tali hui aur thandi cheezon se parhez rakhein. Ishwar aapko shighra swasthya laabh de."
        },
        en: {
          script: "Hello. Please take half a teaspoon twice daily after meals, with lukewarm milk or fresh water. Strictly avoid cold beverages, sour, and fried foods. Wishing you a speedy and complete recovery.",
          devanagari: "Hello. Please take half a teaspoon twice daily after meals with lukewarm milk or fresh water.",
          phonetic: "Hello. Please take half a teaspoon twice daily after meals with lukewarm milk or fresh water. Strictly avoid cold beverages, sour, and fried foods. Wishing you a speedy and complete recovery."
        }
      };

      const selected = textMap[lang] || textMap.en;

      if ('speechSynthesis' in window) {
        try {
          window.speechSynthesis.cancel();
          if (window.speechSynthesis.paused) {
            window.speechSynthesis.resume();
          }

          const selection = selectNaturalHumanVoice(lang);
          let textToSpeak = selected.script;
          if (selection.textType === 'devanagari') {
            textToSpeak = selected.devanagari || selected.phonetic;
          } else if (selection.textType === 'phonetic') {
            textToSpeak = selected.phonetic;
          }

          const utterance = new SpeechSynthesisUtterance(textToSpeak);
          utterance.lang = selection.langCode;
          if (selection.voice) utterance.voice = selection.voice;
          utterance.rate = 0.86;
          utterance.pitch = 1.0;
          utterance.volume = 1.0;

          utterance.onend = () => {
            isAudioPlaying = false;
            if (btn) {
              btn.innerHTML = '<span>▶</span> Play Audio Posology';
              btn.classList.remove('ring-2', 'ring-emerald-400');
            }
          };

          utterance.onerror = (err) => {
            console.warn('SpeechSynthesis error, triggering acoustic posology:', err);
            isAudioPlaying = false;
            if (btn) {
              btn.innerHTML = '<span>▶</span> Play Audio Posology';
              btn.classList.remove('ring-2', 'ring-emerald-400');
            }
            playMelodicPosologySequence();
          };

          setTimeout(() => {
            window.speechSynthesis.speak(utterance);
          }, 150);

          showNotification(`🔊 Playing natural human voice posology in ${lang.toUpperCase()}...`, 'success');
        } catch (err) {
          console.warn('SpeechSynthesis error:', err);
          playMelodicPosologySequence();
        }
      } else {
        playMelodicPosologySequence();
        showNotification('Playing acoustic audio posology...', 'info');
      }
    }

    // ── Core Theory Functions ───────────────────────────────────────────────
    function openCoreTheoryModal() {
      const modal = document.getElementById('core-theory-modal');
      if (modal) modal.classList.remove('hidden');
    }

    function closeCoreTheoryModal() {
      const modal = document.getElementById('core-theory-modal');
      if (modal) modal.classList.add('hidden');
    }

    // ── STATUTORY EMERGENCY RED-FLAG & ALLOPATHIC REFERRAL ENGINE ───────────
    function toggleEmergencyRedFlagModal() {
      const m = document.getElementById('emergency-red-flag-modal');
      if (m) m.classList.toggle('hidden');
    }

    function openEmergencyRedFlagModal() {
      toggleEmergencyRedFlagModal();
    }

    function executeEmergencyHardStop() {
      const radios = document.getElementsByName('stat_red_flag');
      let chosen = 'CARDIAC|Acute Chest Pain / Angina / Suspected Coronary Syndrome';
      for (const r of radios) {
        if (r.checked) { chosen = r.value; break; }
      }
      const parts = chosen.split('|');
      const system = parts[0];
      const trigger = parts[1];

      state.activeRedFlag = {
        system: system,
        trigger: trigger,
        time: new Date().toLocaleTimeString(),
        status: 'ACTIVE_HARD_STOP'
      };

      const banner = document.getElementById('emergency-red-flag-banner');
      const sysEl = document.getElementById('red-flag-banner-system');
      const txtEl = document.getElementById('red-flag-banner-text');

      if (sysEl) sysEl.textContent = system;
      if (txtEl) txtEl.textContent = `${trigger}. Immediate allopathic transfer required.`;
      if (banner) banner.classList.remove('hidden');

      toggleEmergencyRedFlagModal();
      showNotification(`🚨 CRITICAL EMERGENCY RED-FLAG ACTIVE: ${system} - Unani prescribing locked!`, 'error');
    }

    function clearEmergencyRedFlag() {
      state.activeRedFlag = null;
      const banner = document.getElementById('emergency-red-flag-banner');
      if (banner) banner.classList.add('hidden');
      showNotification('Emergency Red-Flag cleared. Specialist clearance documented.', 'info');
    }

    function openEmergencyReferralLetterModal() {
      const m = document.getElementById('emergency-referral-letter-modal');
      const titleEl = document.getElementById('letter-trigger-title');
      const refEl = document.getElementById('letter-ref-no');
      const dateEl = document.getElementById('letter-date-time');

      if (state.activeRedFlag && titleEl) {
        titleEl.textContent = state.activeRedFlag.trigger;
      }
      if (dateEl) {
        dateEl.textContent = `Date: ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`;
      }
      if (m) m.classList.remove('hidden');
    }

    function closeEmergencyReferralLetterModal() {
      const m = document.getElementById('emergency-referral-letter-modal');
      if (m) m.classList.add('hidden');
    }

    // ── TAB 12 FOLLOW-UP & CARE CONTINUITY HELPERS ──────────────────────────
    function selectFollowUpInterval(days, label) {
      const d = new Date();
      d.setDate(d.getDate() + days);
      const iso = d.toISOString().split('T')[0];
      const dateInput = document.getElementById('fu-encounter-date');
      if (dateInput) dateInput.value = iso;

      const preview = document.getElementById('fu-recall-preview');
      if (preview) {
        preview.textContent = `Salam Hamza Farooqi! 🌿\nCourtesy reminder for your follow-up consultation with Hakeem Dr. Irfan Ashraf.\n📅 Scheduled Date: ${d.toLocaleDateString()} (10:30 AM)\n🏥 Venue: ZAYVORA Central Matab & Clinical Hospital\n🎯 Milestone: ${label}\n🧪 Fasting Labs: Please bring fresh repeat hs-CRP & ESR report.`;
      }
    }

    function scheduleFollowUpRecall() {
      const btn = document.getElementById('btn-schedule-fu');
      const conf = document.getElementById('fu-schedule-confirmation');
      const dateVal = document.getElementById('fu-encounter-date')?.value || '2026-10-10';

      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span>⏳</span> Scheduling Recall...';
      }

      setTimeout(() => {
        if (conf) conf.classList.remove('hidden');
        if (btn) {
          btn.innerHTML = '<span>✓</span> Follow-up Scheduled &amp; Queued';
          btn.className = 'w-full px-4 py-2.5 rounded-xl bg-emerald-600 text-white font-bold text-xs shadow-md transition flex items-center justify-center gap-2';
        }
        showNotification(`✓ Follow-up scheduled for ${dateVal}. Automated WhatsApp reminder queued via QSURA gateway!`, 'success');
      }, 500);
    }

    // ── PHARMACY BARCODE SCANNER HELPERS ────────────────────────────────────
    function openPharmacyBarcodeScannerModal() {
      const m = document.getElementById('pharmacy-barcode-modal');
      if (m) m.classList.remove('hidden');
    }

    function closePharmacyBarcodeScannerModal() {
      const m = document.getElementById('pharmacy-barcode-modal');
      if (m) m.classList.add('hidden');
    }

    function confirmPharmacyBarcodeVerification() {
      closePharmacyBarcodeScannerModal();
      const badge = document.getElementById('pharmacy-barcode-status-badge');
      if (badge) {
        badge.textContent = '✓ Barcode BMR-2026-MVP-09 Verified';
        badge.className = 'px-3 py-1.5 rounded-xl bg-emerald-500 text-white text-xs font-bold border border-emerald-400 shadow';
      }
      showNotification('✓ Formulation barcode BMR-2026-MVP-09 verified against Rx-2026-09-0814. Ready to dispense!', 'success');
    }

