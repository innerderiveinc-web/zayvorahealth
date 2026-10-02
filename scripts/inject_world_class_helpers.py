import re

helpers_code = '''
    let activeOrganAxis = 0;
    let opdTokenCounter = 105;
    let pulseAnimFrame = null;
    let pulseOffset = 0;

    const organAxesList = [
      {
        id: "dimagh-meda",
        name: "Dimagh-Meda Axis (Brain-Gut Axis)",
        element: "Psychosomatic & Enteric Neuropathy",
        icon: "🧠 ⇄ 🫄",
        rootCause: "Mental stress and emotional agitation (Su-e-Mizaj Nafsani) lead to gastric hypomotility and cold mucosal dysbiosis (Buroodat-e-Meda).",
        markers: "Vagus nerve tone, Cortisol, Secretory IgA, Gut microbiome diversity.",
        dualTrack: "Ilaj bil Nafsiyat (psychotherapy & breathwork) + Jawarish Kamuni (carminative digestant) + Chamomile/Gaozaban infusion.",
        successRate: "92.4% symptomatic attenuation within 21 days."
      },
      {
        id: "qalb-kabid",
        name: "Qalb-Kabid Axis (Cardio-Hepatic Axis)",
        element: "Hemodynamic & Metabolic Vitality",
        icon: "🫀 ⇄ 🫁",
        rootCause: "Hepatic congestion (Sudda-e-Kabid) impairs innate heat (Hararat-e-Ghariziyyah), placing secondary hemodynamic strain on cardiovascular output.",
        markers: "hs-CRP, Lipid subfractions, SGOT/SGPT, Arterial elasticity index.",
        dualTrack: "Dawa-ul-Misk Motadil (cardioprotective electuary) + Arq Kasni (hepatic decongestant) + Cold-pressed olive oil.",
        successRate: "89.1% lipid & metabolic normalization at 60 days."
      },
      {
        id: "kabid-mafasil",
        name: "Kabid-Mafasil Axis (Hepatic-Joint Phlegmatic Axis)",
        element: "Phlegmatic Exudate & Synovial Clearance",
        icon: "🫁 ⇄ 🦵",
        rootCause: "Sluggish hepatic metabolism allows cold, viscous phlegm (Balgham-e-Ghaleez) to precipitate in synovial microspaces, causing arthritis (Waja-ul-Mafasil).",
        markers: "Uric acid, ESR, Synovial fluid viscosity, IL-6 inflammatory cytokines.",
        dualTrack: "Majun Suranjan (Mudabbar Schedule E1) + Hijama Bila Shart (dry cupping) + Local Raughan-e-Balsan fomentation.",
        successRate: "94.6% joint stiffness reduction at 28 days."
      },
      {
        id: "kulyah-masana",
        name: "Kulyah-Masana Axis (Renal-Bladder Axis)",
        element: "Fluid Filtration & Humoral Excretion",
        icon: "🫘 ⇄ 💧",
        rootCause: "Weakness of retention or expulsion faculty (Quwwat-e-Dafi\\'ah) in renal parenchyma, causing metabolic gravel and fluid retention.",
        markers: "eGFR, Serum creatinine, Urine microalbumin, Urinary pH.",
        dualTrack: "Sharbat Bazoori Motadil (alkalizing diuretic) + Kushta Hajr-ul-Yahud + Hydration with barley water (Maa-ul-Sha\\'eer).",
        successRate: "96.2% stone clearance & filtration enhancement."
      }
    ];

    const mizajDetailsMap = {
      "Balghami": {
        title: "Balghami (Cold & Moist / Phlegmatic)",
        element: "Water (Maa) • Phlegm (Balgham)",
        physique: "Broad shoulders, tendency toward fluid retention, pale cool skin, soft tissue structure.",
        temperamentDesc: "Calm, deliberate, patient, reflective, peaceful, with higher requirement for restorative sleep.",
        organVulnerabilities: "Phlegmatic joint arthritis (Waja-ul-Mafasil), respiratory catarrh, sluggish metabolism, lymphatic congestion.",
        dietaryPrescription: "Warm and dry dietary regimen (Ilaj bil Ghiza). Include ginger, garlic, cloves, black pepper, honey water infusion, and lean proteins. Strictly avoid iced drinks, chilled curds, heavy lentils, and raw cucumbers.",
        regimenalTherapy: "Dry cupping (Hijama Bila Shart), hot sand fomentation (Nutool), and invigorating morning walk (Riyazat).",
        recommendedFormula: "Majun Suranjan (Mudabbar) + Arq Mako"
      },
      "Damawi": {
        title: "Damawi (Hot & Moist / Sanguine)",
        element: "Air (Hawa) • Blood (Dam)",
        physique: "Muscular, robust vascular build, ruddy complexion, warm skin, prominent veins.",
        temperamentDesc: "Enthusiastic, optimistic, communicative, energetic, highly adaptable, full pulse.",
        organVulnerabilities: "Cardiovascular hypertension, arterial plethora (Imtila), epistaxis, acute inflammatory headaches.",
        dietaryPrescription: "Cooling and purifying dietary regimen. Include pomegranate, sour apples, fresh coriander, barley water (Maa-ul-Sha\\'eer), and mint. Limit excessive red meats, pungent spices, and refined sugar.",
        regimenalTherapy: "Venesection (Fasd) or wet cupping (Hijama bil Shart) to release excess vascular pressure.",
        recommendedFormula: "Sharbat Bazoori Motadil + Dawa-ul-Misk"
      },
      "Safrawi": {
        title: "Safrawi (Hot & Dry / Choleric)",
        element: "Fire (Nar) • Yellow Bile (Safra)",
        physique: "Lean, athletic, sharp facial features, yellowish tint, warm dry skin, rapid reflexes.",
        temperamentDesc: "Determined, ambitious, quick-witted, intense, focused, easily irritated under hunger or dehydration.",
        organVulnerabilities: "Gastric hyperacidity, acid reflux, biliary hyperactivity, skin rash/dermatitis, hepatic heat.",
        dietaryPrescription: "Moistening and cooling dietetics. Include tamarind, cucumber, bottle gourd, rose syrup (Sharbat Gulab), and ispaghol. Strictly avoid deep-fried foods, mustard, chili, and tobacco.",
        regimenalTherapy: "Lukewarm medicated baths (Hammam), cold fomentation, peaceful contemplative rest.",
        recommendedFormula: "Sikanjabeen Sada + Itrifal Kishneezi"
      },
      "Sawdawi": {
        title: "Sawdawi (Cold & Dry / Melancholic)",
        element: "Earth (Arz) • Black Bile (Sauda)",
        physique: "Slender, prominent bone landmarks, dry cool skin, dark complexion, delicate frame.",
        temperamentDesc: "Analytical, profound thinker, detail-oriented, cautious, introspective, light restless sleeper.",
        organVulnerabilities: "Splenic congestion, chronic constipation, melancholy, insomnia, localized arthralgia.",
        dietaryPrescription: "Warm, nourishing and moistening dietetics. Include sweet almond oil, fresh cow milk, seedless black raisins, figs, and mutton broth with saffron. Avoid stale foods, brinjal, beef, and cabbage.",
        regimenalTherapy: "Gentle oil massage (Dalk Layyin) with Roghan Badam, warm herbal steam bath, music therapy (Nafsiyat).",
        recommendedFormula: "Khamira Gaozaban Ambari + Majun Najah"
      }
    };

    function setOrganAxis(idx) {
      activeOrganAxis = idx;
      renderWebsiteApp(document.getElementById('workspace-container'));
    }

    function generateInstantOpdToken() {
      const nameInput = document.getElementById('opd-patient-name');
      const clinicSelect = document.getElementById('opd-clinic-select');
      const name = (nameInput && nameInput.value.trim()) || "Visitor";
      const clinic = (clinicSelect && clinicSelect.value) || "ZAYVORA Central Hospital";
      
      opdTokenCounter++;
      const token = "T-" + opdTokenCounter;
      
      const tokenCard = document.getElementById('opd-token-result');
      if (tokenCard) {
        tokenCard.classList.remove('hidden');
        tokenCard.innerHTML = `
          <div class="p-5 rounded-2xl bg-gradient-to-r from-emerald-950/90 via-slate-900 to-teal-950/90 border border-emerald-500/50 space-y-3 text-xs">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-emerald-500/30 pb-3">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">🎫</span>
                <div>
                  <div class="font-bold text-white text-sm">OPD Queue Token Issued Successfully</div>
                  <div class="text-[10px] text-emerald-400 font-mono">${clinic} • Consultation Ready</div>
                </div>
              </div>
              <span class="px-3.5 py-1.5 bg-emerald-500/20 text-emerald-300 font-mono font-extrabold text-base rounded-xl border border-emerald-500/40">
                ${token}
              </span>
            </div>
            <div class="grid grid-cols-3 gap-2.5 text-center text-[11px]">
              <div class="p-2.5 rounded-xl bg-slate-900/90 border border-slate-800">
                <span class="text-slate-400 block text-[10px]">Patient</span>
                <strong class="text-white">${name}</strong>
              </div>
              <div class="p-2.5 rounded-xl bg-slate-900/90 border border-slate-800">
                <span class="text-slate-400 block text-[10px]">Estimated Wait</span>
                <strong class="text-emerald-400">10 - 15 Mins</strong>
              </div>
              <div class="p-2.5 rounded-xl bg-slate-900/90 border border-slate-800">
                <span class="text-slate-400 block text-[10px]">Consultation Chamber</span>
                <strong class="text-teal-300">Room 204 (OPD Desk)</strong>
              </div>
            </div>
            <div class="flex flex-col sm:flex-row justify-between items-center gap-2 pt-1 text-[10px] text-slate-300">
              <span class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Live dispatch confirmed via QSURA SMS bridge.</span>
              <button onclick="switchRole(\\'doctor\\'); switchTab(\\'today\\');" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl shadow-lg transition">
                Enter Doctor Consultation Cockpit →
              </button>
            </div>
          </div>
        `;
      }
      showNotification(`Token ${token} issued for ${name} at ${clinic}. Admitted to Room 204.`, 'success');
    }

    function initWebsiteWaveform() {
      const canvas = document.getElementById('preview-pulse-canvas');
      if (!canvas || !canvas.getContext) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      if (pulseAnimFrame) {
        cancelAnimationFrame(pulseAnimFrame);
      }

      function drawPulse() {
        if (!document.getElementById('preview-pulse-canvas')) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw telemetry grid
        ctx.strokeStyle = '#1E293B';
        ctx.lineWidth = 1;
        for (let x = 0; x < canvas.width; x += 25) {
          ctx.beginPath();
          ctx.moveTo(x, 0);
          ctx.lineTo(x, canvas.height);
          ctx.stroke();
        }
        for (let y = 0; y < canvas.height; y += 20) {
          ctx.beginPath();
          ctx.moveTo(0, y);
          ctx.lineTo(canvas.width, y);
          ctx.stroke();
        }

        // Draw physiological arterial PPG wave
        ctx.strokeStyle = '#10B981';
        ctx.lineWidth = 2.5;
        ctx.shadowBlur = 8;
        ctx.shadowColor = '#10B981';
        ctx.beginPath();

        const w = canvas.width;
        const h = canvas.height;
        const mid = h / 2;

        for (let x = 0; x < w; x++) {
          const t = (x + pulseOffset) % 120;
          let y = mid;
          if (t < 25) {
            y = mid - Math.sin((t / 25) * Math.PI) * 26;
          } else if (t < 40) {
            y = mid - 8 + Math.sin(((t - 25) / 15) * Math.PI) * 5;
          } else if (t < 55) {
            y = mid - 12 + Math.sin(((t - 40) / 15) * Math.PI) * 7;
          } else {
            const decay = (t - 55) / 65;
            y = mid - 5 + decay * 5;
          }

          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
        ctx.shadowBlur = 0;

        pulseOffset = (pulseOffset + 1.2) % 120;
        pulseAnimFrame = requestAnimationFrame(drawPulse);
      }

      drawPulse();
    }
'''

for filepath in ['index.html', 'docs/index.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'const organAxesList = [' not in html:
        html = html.replace("    function renderWebsiteApp(container) {", helpers_code + "\n    function renderWebsiteApp(container) {")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

print("Injected helpers into index.html and docs/index.html.")
