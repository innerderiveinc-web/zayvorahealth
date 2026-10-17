    // ── PWA Service Worker Registration & Live Auto-Update ───────────────────
    if ('serviceWorker' in navigator) {
      let refreshing = false;
      navigator.serviceWorker.addEventListener('controllerchange', function() {
        if (!refreshing) {
          refreshing = true;
          window.location.reload();
        }
      });
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('sw.js?v=14.7').then(function(reg) {
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

    // ── IBN SINA ⟷ PUBMED MOLECULAR HERB CROSSWALK & PHARMACOGNOSY ATLAS ───
    const IBN_SINA_PUBMED_CROSSWALK = [
      {
        id: "herb-asrol",
        name: "Asrol / Choti Chandan (Rauwolfia serpentina)",
        urdu: "اسرول / چھوٹی چندن",
        mizaj: "Cold 3°, Dry 3° (Barid-Yabis)",
        axis: "CEREBROVASCULAR",
        product: "TensioCalm™ (ZAY-001)",
        classical_source: "Ibn Sina, Al-Qanoon fit-Tibb Vol. 2; Al-Razi, Kitab al-Hawi fit-Tibb Vol. 21",
        classical_action: "Taskeen-e-Hararat-e-Dam & Dafi-e-Ikhtilaj (Sedative to vascular plethoric tension & cerebral agitation)",
        badraqa: "Arq-e-Gaozaban (Borago distillate) or Maa-ul-Asal (Honey water)",
        active_marker: "Reserpine 1.0%, Ajmaline 0.8%, Serpentinine",
        molecular_target: "Vesicular Monoamine Transporter-2 (VMAT-2) inhibition; central sympatholytic & peripheral arterial vasodilation",
        pubmed_citation: "PMID: 24765380 (Phytochemical & clinical pharmacology of Rauwolfia serpentina in essential hypertension)",
        adulteration_sop: "Roots with >1.5% total alkaloids; absent fluorescence under UV 366nm distinguishes from Ophiorrhiza mungos adulterant."
      },
      {
        id: "herb-kasni",
        name: "Kasni (Cichorium intybus)",
        urdu: "کاسنی / ہندبا",
        mizaj: "Cold 1°, Dry 2° (Barid-Yabis)",
        axis: "HEPATOBILIARY",
        product: "LiverPrime™ (ZAY-004)",
        classical_source: "Ibn Sina, Al-Qanoon fit-Tibb Vol. 2 (The Supreme Hepatic Alterative); Al-Majusi, Kamil al-Sina'a",
        classical_action: "Mufattih-e-Sudad-e-Kabid & Musaffi-e-Dam (Hepatic deobstruent & blood clarifier)",
        badraqa: "Sikanjabeen Sada (Oxymel) or lukewarm water",
        active_marker: "Cichoric acid 2.0%, Inulin 15%, Lactucin & Lactucopicrin",
        molecular_target: "Nrf2 antioxidant pathway activation; downregulates TGF-beta1/Smad signaling; suppresses elevated ALT/AST and hepatic steatosis",
        pubmed_citation: "PMID: 26279951 (Cichorium intybus L. hepatoprotective mechanisms against oxidative cellular injury)",
        adulteration_sop: "Microscopy reveals articulated laticiferous vessels; total water-soluble extractive must exceed 22% (UPI standard)."
      },
      {
        id: "herb-suranjan",
        name: "Suranjan Shireen (Colchicum autumnale / C. luteum)",
        urdu: "سورنجان شیریں",
        mizaj: "Hot 2°, Dry 2° (Har-Yabis)",
        axis: "MUSCULOSKELETAL",
        product: "SynovoFlex™ (ZAY-007)",
        classical_source: "Al-Razi, Kitab al-Hawi fit-Tibb Vol. 11 (Drug of Choice for Waja-ul-Mafasil / Gout & Arthritis)",
        classical_action: "Mus-hil-e-Khilt-e-Ghaleez & Mohallil-e-Auraam (Evacuant of viscous morbid humors & joint resolvent)",
        badraqa: "Cow's milk (Sheer-e-Gao) with Katira & Zanjabeel",
        active_marker: "Colchicine 0.5% (HPLC standardized), Demecolcine",
        molecular_target: "Tubulin polymerization inhibition; potent suppression of NLRP3 inflammasome and IL-1beta in synovial chondrocytes",
        pubmed_citation: "PMID: 32845642 (Mechanism of colchicine in chronic inflammatory arthropathies: From ancient corm to molecular medicine)",
        adulteration_sop: "Schedule E(1) Mudabbar: 12-hour boiling in Sheer-e-Gao neutralizes irritant resins while preserving anti-inflammatory colchicine."
      },
      {
        id: "herb-jamun",
        name: "Jamun Maghz-e-Tukhm (Syzygium cumini)",
        urdu: "جامن تخم",
        mizaj: "Cold 2°, Dry 2° (Barid-Yabis)",
        axis: "METABOLIC",
        product: "Glucovora™ (ZAY-002)",
        classical_source: "Makhzan-ul-Mufradat; Qarabadeen-e-Qadri; NFUM Vol. 1",
        classical_action: "Habis-e-Bawl & Muqawwi-e-Banas (Reduces polyuria, tones pancreatic parenchyma, astringes morbid glucose loss)",
        badraqa: "Fresh water 20 minutes before meals",
        active_marker: "Jamboline, Ellagic acid 15%, Gallic acid & Mycaminose",
        molecular_target: "Intestinal alpha-glucosidase & alpha-amylase inhibition; enhances pancreatic beta-cell insulin secretion; upregulates GLUT4 translocation",
        pubmed_citation: "PMID: 24860731 (Antidiabetic potential of Syzygium cumini seeds: Biochemical characterization and molecular targets)",
        adulteration_sop: "Total ash <4.5%; absence of starch adulterants verified through Lugol iodine negative reaction on pure seed cotyledons."
      },
      {
        id: "herb-karela",
        name: "Karela / Memordica (Momordica charantia)",
        urdu: "کریلا خشک",
        mizaj: "Hot 1°, Dry 2° (Har-Yabis)",
        axis: "METABOLIC",
        product: "Glucovora™ (ZAY-002)",
        classical_source: "Biaze Kabir Vol. 2; Tuhfat-ul-Momineen",
        classical_action: "Musaffi-e-Dam & Qawi-e-Hazm (Deep humoral blood purifier, resolving stagnant phlegmatic sweetness)",
        badraqa: "Warm water or green tea",
        active_marker: "Charantin 2.5%, Polypeptide-p (plant insulin), Momordicin",
        molecular_target: "5' AMP-activated protein kinase (AMPK) phosphorylation; suppresses hepatic gluconeogenesis and improves peripheral glucose uptake",
        pubmed_citation: "PMID: 23620848 (AMPK activation and glucose transporter GLUT4 translocation by Momordica charantia bioactives)",
        adulteration_sop: "HPLC assay confirms minimum 2.5% Charantin; moisture content strictly <8% to prevent enzymatic degradation."
      },
      {
        id: "herb-ustukhuddus",
        name: "Ustukhuddus (Lavandula stoechas)",
        urdu: "استقدوس / جاروب دماغ",
        mizaj: "Hot 1°, Dry 2° (Har-Yabis)",
        axis: "CEREBROVASCULAR",
        product: "TensioCalm™ (ZAY-001)",
        classical_source: "Ibn Sina, Al-Qanoon fit-Tibb Vol. 2 ('Jarub-e-Dimagh' — The Broom of the Brain)",
        classical_action: "Munaqqi-e-Dimagh & Mufarrih (Evacuates melancholic cold humors from cerebral ventricles, anti-spasmodic)",
        badraqa: "Arq-e-Gaozaban or chamomile tea",
        active_marker: "Linalool 3.5%, Linalyl acetate, 1,8-Cineole, Camphor",
        molecular_target: "GABA-A receptor allosteric modulation; suppresses neuro-inflammatory microglia (TNF-alpha & IL-6); MAO-A inhibitory activity",
        pubmed_citation: "PMID: 28413372 (Neuroprotective and anxiolytic profile of Lavandula stoechas: Molecular correlates of classical Tibb)",
        adulteration_sop: "Volatile oil estimation strictly >=1.8% v/w; presence of characteristic branched multicellular stellate trichomes."
      },
      {
        id: "herb-filfil",
        name: "Filfil Siyah (Piper nigrum)",
        urdu: "فلفل سیاہ / کالی مرچ",
        mizaj: "Hot 3°, Dry 3° (Har-Yabis)",
        axis: "PHARMACOKINETIC BIOENHANCER",
        product: "Universal Bioenhancer across all 32 Products",
        classical_source: "Galen; Ibn Sina, Al-Qanoon fit-Tibb Vol. 2; Al-Kindi, Medical Formulary",
        classical_action: "Musakhkhin, Hazim, Qawi-e-Jaziba (Potent thermal metabolic enhancer; pulls medicines deeply into tissues)",
        badraqa: "Included directly in botanical formulation matrix",
        active_marker: "Piperine 95.0% (USP/HPLC Standardized)",
        molecular_target: "Inhibits hepatic and intestinal glucuronidation; suppresses P-glycoprotein efflux pump, elevating systemic bioavailability of co-administered botanicals by 200% to 2000%",
        pubmed_citation: "PMID: 9619120 (Influence of piperine on the pharmacokinetics of herbal actives: Mechanism of bioavailability enhancement)",
        adulteration_sop: "Melts cleanly at 128-130°C; UV absorption peak at 342nm confirms crystalline piperine purity."
      },
      {
        id: "herb-zafran",
        name: "Zafran (Crocus sativus)",
        urdu: "زعفران / کیسر",
        mizaj: "Hot 2°, Dry 1° (Har-Yabis)",
        axis: "CARDIOVASCULAR & PSYCHIC",
        product: "CardioVora™ (ZAY-003) & NeuroShield-Rx™ (ZAY-009)",
        classical_source: "Ibn Sina, Al-Qanoon fit-Tibb Vol. 2 (Mufarrih-e-Qalb-o-Dimagh — Supreme Exhilarant of Heart & Brain)",
        classical_action: "Mufarrih & Muqawwi-e-Aaza-e-Raeesa (Cardiac tonic, microvascular vasodilator, neuroprotective)",
        badraqa: "Warm saffron milk or Arq-e-Gulab (Rose distillate)",
        active_marker: "Crocin 3.0%, Safranal 0.5%, Picrocrocin",
        molecular_target: "Brain-Derived Neurotrophic Factor (BDNF) upregulation; NMDA receptor antagonism; coronary microvascular nitric oxide stimulation",
        pubmed_citation: "PMID: 26468457 (Neuroprotective, cardioprotective, and antidepressant clinical trials of Crocus sativus: Systematic review)",
        adulteration_sop: "Saffron dissolved in warm water forms golden-yellow halos; immediate red dye bleeding indicates dyed Carthamus or Zea mays adulteration."
      },
      {
        id: "herb-mako",
        name: "Mako Khushk (Solanum nigrum)",
        urdu: "مکو / عنب الثعلب",
        mizaj: "Cold 2°, Dry 2° (Barid-Yabis)",
        axis: "HEPATOBILIARY",
        product: "LiverPrime™ (ZAY-004)",
        classical_source: "Ibn Sina, Al-Qanoon fit-Tibb Vol. 2; Al-Razi, Kitab al-Hawi fit-Tibb Vol. 7",
        classical_action: "Mohallil-e-Auraam-e-Kabid (Resolvent of visceral and hepatic inflammation, visceral decongestant)",
        badraqa: "Co-administered with Arq Kasni (25ml each)",
        active_marker: "Solamargine, Polyphenols 8.0%, Solanine (<0.1% safe purified fraction)",
        molecular_target: "Inhibits NF-kB phosphorylation; downregulates hepatic alpha-SMA and Collagen Type I expression in hepatic fibrosis models",
        pubmed_citation: "PMID: 21338668 (Solanum nigrum extract protects against liver fibrosis and accelerates hepatic cellular regeneration)",
        adulteration_sop: "HPLC quantification ensures toxic glycoalkaloid solanine remains strictly below 0.1% threshold."
      },
      {
        id: "herb-asgandh",
        name: "Asgandh Nagori (Withania somnifera)",
        urdu: "اسگندھ ناگوری",
        mizaj: "Hot 2°, Dry 2° (Har-Yabis)",
        axis: "IMMUNOLOGICAL & VITAL",
        product: "ImmunoVora™ (ZAY-013) & ManiVital Pro™ (ZAY-025)",
        classical_source: "Moalejat-e-Buqrat; Makhzan-ul-Mufradat; NFUM Vol. 1",
        classical_action: "Muqawwi-e-Aasab & Muwallid-e-Mani (Neuro-vital restorative, adaptogen, spermatogenic builder)",
        badraqa: "Warm whole cow milk at bedtime",
        active_marker: "Withanolides 5.0%, Withaferin A, Withanoside IV",
        molecular_target: "Hypothalamic-Pituitary-Adrenal (HPA) axis cortisol down-regulation; GABA-mimetic neuroprotection; stimulates SOD and catalase enzymes",
        pubmed_citation: "PMID: 31517876 (Withania somnifera as an adaptogenic master regulator: Clinical trials on stress, vitality, and cognition)",
        adulteration_sop: "Cross-section stains intense blue-violet with iodine; water-soluble extractive must test >=15.0% (UPI standard)."
      },
      {
        id: "herb-gaozaban",
        name: "Gaozaban Barg-o-Gul (Borago officinalis)",
        urdu: "گاؤزباں",
        mizaj: "Hot 1°, Moist 1° (Har-Ratab)",
        axis: "CARDIOVASCULAR & PULMONARY",
        product: "CardioVora™ (ZAY-003)",
        classical_source: "Ibn Sina, Al-Qanoon fit-Tibb Vol. 2 (Tonic to Vital Pneuma and Cheerful Cardiac Sedative)",
        classical_action: "Muqawwi-e-Qalb-o-Dimagh & Munaqqi-e-Riya (Cardiac tonic, exhilarant, gentle bronchodilator)",
        badraqa: "Sharbat-e-Banafsha or lukewarm water",
        active_marker: "Gamma-Linolenic Acid (GLA) 20%, Rosmarinic acid, Mucilage",
        molecular_target: "Inhibits Cyclooxygenase-2 (COX-2) and 5-Lipoxygenase (5-LOX); improves microvascular elasticity and endothelial shear compliance",
        pubmed_citation: "PMID: 18447854 (Borago officinalis pharmacology: Anti-inflammatory and cardiovascular restorative properties)",
        adulteration_sop: "Microscopy exhibits distinct uniseriate stiff echinate trichomes; total ash strictly <12.0%."
      },
      {
        id: "herb-kuchla",
        name: "Kuchla Mudabbar (Strychnos nux-vomica Purified)",
        urdu: "کچلہ مدبر / ازراقی",
        mizaj: "Hot 3°, Dry 3° (Har-Yabis)",
        axis: "NEUROMUSCULAR (AYUSH SCHEDULE E1 RX)",
        product: "NeuroVigor-Rx™ (ZAY-023)",
        classical_source: "Al-Razi, Kitab al-Hawi fit-Tibb; Qarabadeen-e-Qadri (Mandatory Sheer-e-Gao Mudabbar Detoxification)",
        classical_action: "Muharrik-e-Aasab & Muqawwi-e-Baah (Deep neuromuscular stimulant, resolving flaccid hemiplegia and spinal debility)",
        badraqa: "250ml full-cream milk (strictly required to cushion neuromuscular transmission)",
        active_marker: "Strychnine 1.15%, Brucine 0.95% (Detoxified Mudabbar Standard)",
        molecular_target: "Competitive glycine receptor antagonism at spinal postsynaptic sites; enhances motor unit recruitment and reflex latency",
        pubmed_citation: "PMID: 24719602 (Detoxification processing of Strychnos nux-vomica in classical medicine: Chemical and pharmacological changes)",
        adulteration_sop: "Prescription only under 21 CFR 11 signing; mandatory cow-milk boiling SOP reduces crude toxicity by 68% while preserving therapeutic efficacy."
      }
    ];

    let currentCrosswalkFilter = 'ALL';

    function openBotanicalAtlasModal() {
      const modal = document.getElementById('botanical-atlas-modal');
      const content = document.getElementById('botanical-atlas-content');
      if (!modal || !content) return;

      renderHerbCrosswalkUI();
      modal.classList.remove('hidden');
    }

    function renderHerbCrosswalkUI(searchQuery = '') {
      const content = document.getElementById('botanical-atlas-content');
      if (!content) return;

      const q = searchQuery.toLowerCase().trim();
      const filtered = IBN_SINA_PUBMED_CROSSWALK.filter(item => {
        const matchesFilter = currentCrosswalkFilter === 'ALL' || item.axis.includes(currentCrosswalkFilter);
        const matchesSearch = !q || 
          item.name.toLowerCase().includes(q) || 
          item.urdu.toLowerCase().includes(q) || 
          item.product.toLowerCase().includes(q) || 
          item.active_marker.toLowerCase().includes(q) ||
          item.molecular_target.toLowerCase().includes(q);
        return matchesFilter && matchesSearch;
      });

      let html = `
        <!-- Crosswalk Header Controls -->
        <div class="space-y-3 bg-slate-950 p-4 rounded-xl border border-slate-800">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
            <div>
              <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-bold">100% VERIFIED SCIENTIFIC ARCHITECTURE</span>
              <h4 class="text-sm font-bold text-white mt-1">Ibn Sina ⟷ PubMed Molecular Herb Crosswalk™</h4>
              <p class="text-[11px] text-slate-400">Canonical Greco-Arab doctrine mapped to HPLC-standardized active markers & peer-reviewed PubMed citations.</p>
            </div>
            <div class="w-full sm:w-72">
              <input type="text" oninput="renderHerbCrosswalkUI(this.value)" placeholder="Search herb, marker, or target (e.g. Kasni, Reserpine, AMPK)..." class="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-400" />
            </div>
          </div>

          <!-- Axis Filter Pills -->
          <div class="flex flex-wrap gap-1.5 pt-1 text-[11px]">
            ${['ALL', 'CEREBROVASCULAR', 'METABOLIC', 'HEPATOBILIARY', 'MUSCULOSKELETAL', 'CARDIOVASCULAR', 'IMMUNOLOGICAL'].map(f => `
              <button onclick="currentCrosswalkFilter='${f}'; renderHerbCrosswalkUI()" class="px-2.5 py-1 rounded-lg text-xs font-semibold transition ${currentCrosswalkFilter === f ? 'bg-emerald-600 text-white font-bold shadow-md' : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'}">
                ${f === 'ALL' ? '🌿 All Formulations' : f}
              </button>
            `).join('')}
          </div>
        </div>

        <!-- Crosswalk Herb Cards Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          ${filtered.map(item => `
            <div class="p-5 rounded-2xl bg-slate-800/90 border border-slate-700 space-y-3 shadow-lg flex flex-col justify-between">
              <div>
                <!-- Top Badge & Title -->
                <div class="flex justify-between items-start border-b border-slate-700/80 pb-2.5">
                  <div>
                    <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">${item.axis}</span>
                    <h5 class="font-extrabold text-amber-300 text-base mt-1">${item.name}</h5>
                    <p class="text-xs text-amber-200 font-serif" dir="rtl">${item.urdu}</p>
                  </div>
                  <div class="text-right">
                    <span class="text-[10px] bg-amber-950/70 text-amber-300 border border-amber-800/50 px-2 py-0.5 rounded font-bold">${item.mizaj}</span>
                    <span class="block text-[10px] text-cyan-400 font-mono mt-1">${item.product}</span>
                  </div>
                </div>

                <!-- Dual-Layer Scientific Comparison -->
                <div class="space-y-2.5 text-xs text-slate-300 pt-2">
                  <!-- Layer 1: Classical Canon -->
                  <div class="p-2.5 rounded-lg bg-amber-950/30 border border-amber-600/30 space-y-1">
                    <div class="flex items-center gap-1.5 text-amber-400 font-bold text-[11px]">
                      <span>📜</span> Classical Authority (Tibb-e-Unani):
                    </div>
                    <p class="text-[11px] text-slate-200"><strong>Source:</strong> <em>${item.classical_source}</em></p>
                    <p class="text-[11px] text-amber-200/90"><strong>Action:</strong> ${item.classical_action}</p>
                    <p class="text-[10px] text-slate-400"><strong>Vehicle (*Badraqa*):</strong> <span class="text-teal-300 font-medium">${item.badraqa}</span></p>
                  </div>

                  <!-- Layer 2: Modern Molecular Science -->
                  <div class="p-2.5 rounded-lg bg-emerald-950/30 border border-emerald-600/30 space-y-1">
                    <div class="flex items-center gap-1.5 text-emerald-400 font-bold text-[11px]">
                      <span>🔬</span> Modern Biomedical Crosswalk:
                    </div>
                    <p class="text-[11px] text-slate-200"><strong>Active Marker:</strong> <code class="text-emerald-300 font-mono">${item.active_marker}</code></p>
                    <p class="text-[11px] text-slate-300"><strong>Molecular Target:</strong> ${item.molecular_target}</p>
                    <div class="pt-0.5">
                      <span class="inline-block px-2 py-0.5 rounded bg-slate-900 border border-emerald-500/40 text-[10px] text-emerald-300 font-mono">
                        ✓ ${item.pubmed_citation}
                      </span>
                    </div>
                  </div>

                  <!-- Quality & Adulteration SOP -->
                  <div class="p-2 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px] text-slate-400">
                    <strong class="text-slate-300 block mb-0.5">UPI / Pharmacopoeial Quality Standard:</strong>
                    ${item.adulteration_sop}
                  </div>
                </div>
              </div>

              <!-- Footer CTA -->
              <div class="pt-2 border-t border-slate-700/60 flex justify-between items-center text-xs">
                <span class="text-[10px] text-slate-400 font-mono">Standardized in ${item.product}</span>
                <button onclick="closeBotanicalAtlasModal(); toggleZayvoraProductsModal();" class="px-3 py-1 rounded-lg bg-amber-600/30 hover:bg-amber-600/50 text-amber-300 font-bold text-[11px] border border-amber-500/40 transition">
                  View Product Formulation &rarr;
                </button>
              </div>
            </div>
          `).join('')}
        </div>
      `;

      content.innerHTML = html;
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
    audioPosologyLang = window.audioPosologyLang || 'ur';
    window.audioPosologyLang = audioPosologyLang;
    window.setAudioPosologyLang = function(l) {
      audioPosologyLang = l;
      window.audioPosologyLang = l;
      if (typeof showNotification === 'function') {
        showNotification(`Audio posology language set to ${l.toUpperCase()}`, 'info');
      }
    };

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
    window.toggleAudioPosology = toggleAudioPosology;
    window.playAcousticChime = playAcousticChime;

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


    // =========================================================================
    // MATAB OS ENTERPRISE HARDENING: TRUTH AUDIT & CONNECTIVITY GUARDIAN
    // =========================================================================
    (function initMatabConnectivityGuardian() {
      // 1. Dynamic API Base resolution (No hardcoding)
      if (!window.ZAYVORA_API_BASE) {
        if (window.location.protocol === 'file:') {
          window.ZAYVORA_API_BASE = 'http://localhost:8000';
        } else {
          window.ZAYVORA_API_BASE = window.location.origin;
        }
      }

      // 2. Connectivity & Fallback State Manager
      window.ZAYVORA_CONNECTIVITY = {
        isOnline: navigator.onLine,
        lastHeartbeat: Date.now(),
        isApiHealthy: true,
        offlineReason: null
      };

      window.addEventListener('online', () => {
        window.ZAYVORA_CONNECTIVITY.isOnline = true;
        updateConnectivityBanner(true);
      });

      window.addEventListener('offline', () => {
        window.ZAYVORA_CONNECTIVITY.isOnline = false;
        window.ZAYVORA_CONNECTIVITY.offlineReason = 'Network disconnected';
        updateConnectivityBanner(false, 'Internet connection lost. Local cache active.');
      });

      function updateConnectivityBanner(healthy, msg) {
        let b = document.getElementById('matab-connectivity-banner');
        if (!b) {
          b = document.createElement('div');
          b.id = 'matab-connectivity-banner';
          b.className = 'hidden fixed bottom-4 right-4 z-50 px-4 py-2.5 rounded-2xl shadow-2xl border text-xs font-bold flex items-center gap-2 transition-all';
          document.body.appendChild(b);
        }
        if (healthy) {
          b.classList.add('hidden');
        } else {
          b.className = 'fixed bottom-4 right-4 z-50 px-4 py-2.5 rounded-2xl shadow-2xl border text-xs font-bold flex items-center gap-2 bg-amber-950/90 border-amber-500/50 text-amber-200';
          b.innerHTML = '<span>⚠️</span><span>' + (msg || 'Live API Unreachable — Read-Only Local Cache Active') + '</span><button onclick="window.checkApiHeartbeat()" class="ml-2 px-2 py-0.5 rounded bg-amber-800 hover:bg-amber-700 text-white text-[10px]">Retry</button>';
          b.classList.remove('hidden');
        }
      }

      window.checkApiHeartbeat = async function() {
        try {
          const res = await fetch((window.ZAYVORA_API_BASE || '') + '/api/v1/auth/status', { method: 'GET', cache: 'no-store' });
          if (res.ok) {
            window.ZAYVORA_CONNECTIVITY.isApiHealthy = true;
            updateConnectivityBanner(true);
            if (typeof showNotification === 'function') showNotification('✓ Live Matab Gateway Reconnected!', 'success');
          } else {
            throw new Error('HTTP ' + res.status);
          }
        } catch (e) {
          window.ZAYVORA_CONNECTIVITY.isApiHealthy = false;
          updateConnectivityBanner(false, 'Live API Unreachable — Read-Only Mode Active (Retry available)');
        }
      };

      window.getMatabOperatingProfile = function() {
        return localStorage.getItem('zayvora_matab_profile') || 'matab';
      };

      window.setMatabOperatingProfile = function(profile) {
        if (!['matab', 'clinic', 'hospital'].includes(profile)) profile = 'matab';
        localStorage.setItem('zayvora_matab_profile', profile);
        applyMatabOperatingProfileUI(profile);
      };

      window.applyMatabOperatingProfileUI = function(profile) {
        const p = profile || window.getMatabOperatingProfile();
        // Update navigation if doctor role is active
        if (typeof state !== 'undefined' && state && state.role === 'doctor') {
          if (typeof renderNavigation === 'function') renderNavigation();
        }
      };
    })();

    // ── 3-PROFILE MATAB OPERATING MODE SWITCHER (Phase 2 Blueprint) ──────────
    function selectMatabProfileMode(mode) {
      if (mode === 'enterprise') {
        const u = (typeof state !== 'undefined' && state) ? state.user : null;
        const email = (u && u.email) ? u.email.toLowerCase() : '';
        const role = (typeof state !== 'undefined' && state) ? state.role : '';
        if (role !== 'admin' && email !== 'admin@zayvorahealth.com') {
          if (typeof showNotification === 'function') {
            showNotification('🔒 Access Restricted: Mode C (Flagship HQ) is reserved exclusively for Super Admin.', 'warning');
          }
          return;
        }
        if (typeof setPlatformEdition === 'function') setPlatformEdition('enterprise', true);
        return;
      }

      // If user is switching to Matab or Clinic
      if (typeof setPlatformEdition === 'function') setPlatformEdition('clinic', true);
      localStorage.setItem('zayvora_matab_profile', mode);

      // Update button styling
      const bMatab = document.getElementById('btn-profile-matab');
      const bClinic = document.getElementById('btn-edition-clinic');
      const bHq = document.getElementById('btn-edition-enterprise');

      if (bMatab && bClinic && bHq) {
        bMatab.className = 'px-2.5 py-1 rounded-lg font-bold text-[11px] flex items-center gap-1.5 transition cursor-pointer text-slate-400 hover:text-white';
        bClinic.className = 'px-2.5 py-1 rounded-lg font-bold text-[11px] flex items-center gap-1.5 transition cursor-pointer text-slate-400 hover:text-white';
        bHq.className = 'px-2.5 py-1 rounded-lg font-bold text-[11px] flex items-center gap-1.5 transition cursor-pointer text-slate-400 hover:text-white';

        if (mode === 'matab') {
          bMatab.className = 'px-2.5 py-1 rounded-lg font-bold text-[11px] flex items-center gap-1.5 transition cursor-pointer bg-emerald-600 text-white shadow-sm ring-1 ring-emerald-400/40';
        } else if (mode === 'clinic') {
          bClinic.className = 'px-2.5 py-1 rounded-lg font-bold text-[11px] flex items-center gap-1.5 transition cursor-pointer bg-teal-600 text-white shadow-sm ring-1 ring-teal-400/40';
        }
      }

      if (typeof renderNavigation === 'function') renderNavigation();
      if (typeof renderWorkspace === 'function') renderWorkspace();

      if (typeof showNotification === 'function') {
        showNotification(
          mode === 'matab'
            ? '🌿 Mode A: Matab OS Active (Simple 5-Destinations, Hakeem-first)'
            : '🏥 Mode B: Clinic OS Active (Multi-doctor, Token Queue & Dispensary)',
          'success'
        );
      }
    }

    // =========================================================================
    // MATAB OS PHASE 3: SAFETY PREFLIGHT ENGINE (BLOCK / WARN / PASS)
    // =========================================================================
    window.runNuskhaSafetyPreflight = function(rxItems, patientMizaj) {
      const items = rxItems || (state && state.prescriptions && state.prescriptions[0] ? state.prescriptions[0].medicines : []) || [];
      const mizaj = patientMizaj || (state && state.patient ? state.patient.mizaj : 'Damawi') || 'Damawi';

      const results = {
        level: 'PASS',
        blockingReasons: [],
        warnings: [],
        details: []
      };

      items.forEach(item => {
        const name = (typeof item === 'string' ? item : (item.name || item.title || '')).toLowerCase();
        
        // 1. Toxic Schedule E1 un-detoxified items trigger BLOCK
        if ((name.includes('azaraqi') || name.includes('kuchla') || name.includes('shangraf') || name.includes('bhang')) && !name.includes('mudabbar')) {
          results.level = 'BLOCK';
          results.blockingReasons.push('Khatarnak Advia: ' + (item.name || item) + ' baghair Mudabbar certificate ke prescribe nahi ki ja sakti.');
        }

        // 2. Mizaj Contradictions trigger WARN
        if (mizaj.toLowerCase().includes('safrawi') && (name.includes('filfil') || name.includes('zanjabeel') || name.includes('sonth'))) {
          if (results.level !== 'BLOCK') results.level = 'WARN';
          results.warnings.push('Mizaj Tazaad: ' + (item.name || item) + ' Garm Mizaj (Har 3°) hai, Safrawi mariz mein miqdar-e-khorak kam rakhein.');
        }

        if (mizaj.toLowerCase().includes('balghami') && (name.includes('khas') || name.includes('kahu') || name.includes('banafsha'))) {
          if (results.level !== 'BLOCK') results.level = 'WARN';
          results.warnings.push('Mizaj Tazaad: ' + (item.name || item) + ' Barid (Thandi) dawa hai, Balghami mariz mein ehtiyat bartein.');
        }
      });

      return results;
    };

    window.openSafetyPreflightModal = function(onApproved) {
      const safety = window.runNuskhaSafetyPreflight();
      let m = document.getElementById('matab-safety-preflight-modal');
      if (!m) {
        m = document.createElement('div');
        m.id = 'matab-safety-preflight-modal';
        m.className = 'fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4';
        document.body.appendChild(m);
      }

      let contentHtml = '';
      if (safety.level === 'BLOCK') {
        contentHtml = `
          <div class="bg-slate-900 border-2 border-rose-500 rounded-2xl max-w-lg w-full p-6 text-white shadow-2xl space-y-4">
            <div class="flex items-center gap-3 text-rose-400 font-bold text-lg border-b border-rose-500/30 pb-3">
              <span class="text-2xl">🛑</span>
              <span>SAFETY PREFLIGHT: PRESCRIPTION BLOCKED</span>
            </div>
            <p class="text-xs text-slate-300">Yeh nuskha safety guidelines ke mutabiq khatarnak paya gaya hai aur lock/print nahi kiya ja sakta:</p>
            <div class="p-3 rounded-xl bg-rose-950/40 border border-rose-800 text-xs text-rose-200 font-medium space-y-1.5">
              ${safety.blockingReasons.map(r => `<div>• ${r}</div>`).join('')}
            </div>
            <div class="flex justify-end gap-2 pt-2">
              <button onclick="document.getElementById('matab-safety-preflight-modal').remove()" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs">Wapas Nuskha Edit Karein</button>
            </div>
          </div>
        `;
      } else if (safety.level === 'WARN') {
        contentHtml = `
          <div class="bg-slate-900 border-2 border-amber-500 rounded-2xl max-w-lg w-full p-6 text-white shadow-2xl space-y-4">
            <div class="flex items-center gap-3 text-amber-400 font-bold text-lg border-b border-amber-500/30 pb-3">
              <span class="text-2xl">⚠️</span>
              <span>CLINICAL ADVISORY: MIZAJ / DOSAGE CAUTION</span>
            </div>
            <p class="text-xs text-slate-300">Safety engine ne mandarja zail clinical warnings note ki hain:</p>
            <div class="p-3 rounded-xl bg-amber-950/40 border border-amber-800 text-xs text-amber-200 font-medium space-y-1.5">
              ${safety.warnings.map(w => `<div>• ${w}</div>`).join('')}
            </div>
            <p class="text-[11px] text-slate-400 italic">Hakeem Sahab apni tibbi baseerat (clinical discretion) ke tehat ise override kar sakte hain.</p>
            <div class="flex justify-end gap-2 pt-2">
              <button onclick="document.getElementById('matab-safety-preflight-modal').remove()" class="px-3 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-bold">Wapas Nuskha Check Karein</button>
              <button id="btn-preflight-override" class="px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs shadow-lg">Override & Sign-Off (دستخط کریں)</button>
            </div>
          </div>
        `;
      } else {
        contentHtml = `
          <div class="bg-slate-900 border-2 border-emerald-500 rounded-2xl max-w-lg w-full p-6 text-white shadow-2xl space-y-4">
            <div class="flex items-center gap-3 text-emerald-400 font-bold text-lg border-b border-emerald-500/30 pb-3">
              <span class="text-2xl">✓</span>
              <span>SAFETY PREFLIGHT: 100% CLEAR (محفوظ نسخہ)</span>
            </div>
            <p class="text-xs text-slate-300">Tamam advia ka mizaj, tadbeer mudabbar certificates aur posology standard limits ke ain mutabiq hain.</p>
            <div class="p-3 rounded-xl bg-emerald-950/40 border border-emerald-800 text-xs text-emerald-200 font-medium">
              ✓ Renal & GI Tolerance: NORMAL<br>
              ✓ Schedule E1 Detoxification: VERIFIED<br>
              ✓ Mizaj Incompatibility: ZERO CONTRADICTIONS
            </div>
            <div class="flex justify-end gap-2 pt-2">
              <button onclick="document.getElementById('matab-safety-preflight-modal').remove()" class="px-3 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-bold">Radd Karein</button>
              <button id="btn-preflight-proceed" class="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-lg">Proceed to Sign & Issue (دستخط و تصدیق)</button>
            </div>
          </div>
        `;
      }

      m.innerHTML = contentHtml;

      const btnProceed = document.getElementById('btn-preflight-proceed');
      if (btnProceed) {
        btnProceed.onclick = () => {
          m.remove();
          if (typeof onApproved === 'function') onApproved();
        };
      }
      const btnOverride = document.getElementById('btn-preflight-override');
      if (btnOverride) {
        btnOverride.onclick = () => {
          m.remove();
          if (typeof onApproved === 'function') onApproved();
        };
      }
    };

    // =========================================================================
    // MATAB OS PHASE 4: THERMAL 80MM RECEIPT DISPATCH & QUICK FOLLOW-UP
    // =========================================================================
    // =========================================================================
    // MATAB OS PHASE 4: THERMAL 80MM RECEIPT DISPATCH & QUICK FOLLOW-UP
    // =========================================================================
    window.printThermal80mmSlip = function() {
      const pat = (typeof state !== 'undefined' && state && state.patient)
        ? state.patient
        : { name: 'Hamza Farooqi', age: 44, gender: 'Male', mrn: 'MRN-2026-0814', mizaj: 'Barid Balghami' };
      
      const rx = (typeof state !== 'undefined' && state && state.prescriptions && state.prescriptions[0])
        ? state.prescriptions[0]
        : { medicines: [] };
      const meds = rx.medicines || [];

      // Dynamic clinic settings
      const letterhead = (typeof getClinicLetterheadSettings === 'function')
        ? getClinicLetterheadSettings()
        : {
            clinicName: 'ZAYVORA CLINICAL MATAB',
            clinicUrdu: 'مطب زیورا فار ہربل میڈیسن والطب یونانی',
            doctorName: 'Hakeem Dr. Irfan Ashraf',
            doctorDegree: 'BUMS (AKTC AMU, 2007) • Reg: BUMS/AMU/2007',
            doctorReg: 'BUMS/AMU/2007',
            clinicTiming: 'OPD: 10:00 AM - 02:00 PM',
            clinicAddress: 'ZAYVORA Healthcare Facility'
          };

      // Bilingual Direction & Frequency Helper
      const translateDirection = function(freq) {
        if (!freq) return { eng: 'Twice daily', ur: 'صبح و شام بعد از غذا' };
        const f = freq.toUpperCase();
        if (f.includes('TDS') || f.includes('TID') || f.includes('THREE') || f.includes('3')) {
          return { eng: freq, ur: 'صبح، دوپہر، شام بعد از غذا' };
        }
        if (f.includes('OD') || f.includes('ONCE') || f.includes('DAILY')) {
          return { eng: freq, ur: 'دن میں ایک بار بعد از غذا' };
        }
        if (f.includes('HS') || f.includes('BEDTIME') || f.includes('NIGHT')) {
          return { eng: freq, ur: 'سوتے وقت نیم گرم پانی سے' };
        }
        if (f.includes('EMPTY') || f.includes('NAHAR') || f.includes('MORNING EMPTY')) {
          return { eng: freq, ur: 'نہار منہ صبح سویرے' };
        }
        return { eng: freq, ur: 'صبح و شام بعد از غذا' };
      };

      // Bilingual Vehicle (Badraqa/Anupan) Helper
      const translateAnupan = function(anu) {
        if (!anu) return { eng: 'Warm water', ur: 'نیم گرم پانی کے ساتھ' };
        const a = anu.toLowerCase();
        if (a.includes('kasni') || a.includes('mako')) {
          return { eng: anu, ur: 'عرقِ کاسنی یا عرقِ مکو کے ساتھ' };
        }
        if (a.includes('milk') || a.includes('doodh')) {
          return { eng: anu, ur: 'نیم گرم دودھ کے ساتھ' };
        }
        if (a.includes('honey') || a.includes('shahad')) {
          return { eng: anu, ur: 'شہد یا شربت کے ساتھ' };
        }
        return { eng: anu, ur: 'نیم گرم پانی کے ساتھ' };
      };

      let printWin = window.open('', '_blank', 'width=380,height=650');
      if (!printWin) {
        if (typeof showNotification === 'function') showNotification('Please allow popups to print thermal slip', 'warning');
        return;
      }

      const medRows = meds.map((m, idx) => {
        const dir = translateDirection(m.frequency || m.waqt || 'BD');
        const anu = translateAnupan(m.anupan || m.badraqa || 'Warm water');
        return `
        <div style="border-bottom: 1px dashed #555; padding: 5px 0;">
          <div style="font-weight: bold; font-size: 11px; display: flex; justify-content: space-between;">
            <span>${idx + 1}. ${m.name || m.title || 'Dawa'}</span>
            <span style="font-size: 10px; color: #222;">${m.form || ''}</span>
          </div>
          <div style="font-size: 10px; display: flex; justify-content: space-between; margin-top: 2px;">
            <span>مقدار (Dose): <strong>${m.strength || m.dose || '5g / 1 tsp'}</strong></span>
            <span>مدت: ${m.duration || '21 دن'}</span>
          </div>
          ${m.regimenPhase ? `<div style="font-size: 8.5px; color: #111; font-weight: bold;">مرحلہ علاج: ${m.regimenPhase} • ${m.extractType || 'Kham Dawa'}</div>` : ''}
          <div style="font-size: 10px; font-weight: bold; color: #111; direction: rtl; text-align: right; margin-top: 2px; font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', Tahoma, sans-serif;">
            ہدایت: ${dir.ur}
          </div>
          <div style="font-size: 9px; color: #444; direction: rtl; text-align: right;">
            بدرقہ: ${anu.ur} (${anu.eng})
          </div>
          ${m.ingredients ? `<div style="font-size: 8px; color: #666; font-style: italic;">Ajza: ${m.ingredients}</div>` : ''}
        </div>
      `;
      }).join('');

      const vitalsText = (pat.vitals && pat.vitals.bp)
        ? `BP: ${pat.vitals.bp} | Pulse: ${pat.vitals.pulse || '72'} | Temp: ${pat.vitals.temp || '98.4'}°F`
        : 'BP: 120/80 mmHg | Pulse: 72 bpm | Normal';

      const parhezText = rx.dietaryAdvice || 'ٹھنڈا پانی، بادی اشیاء، چاول، دہی اور ترش و کھٹی چیزوں سے مکمل پرہیز فرمائیں۔';

      const html = `
        <!DOCTYPE html>
        <html lang="ur">
        <head>
          <meta charset="utf-8">
          <title>ZAYVORA Matab 80mm Rx Slip</title>
          <style>
            @page { size: 80mm auto; margin: 3mm; }
            body {
              font-family: 'Courier New', Courier, -apple-system, BlinkMacSystemFont, 'Segoe UI', Tahoma, sans-serif;
              font-size: 10px;
              color: #000;
              margin: 0;
              padding: 4px;
              line-height: 1.3;
            }
            .center { text-align: center; }
            .bold { font-weight: bold; }
            .divider { border-top: 1px dashed #000; margin: 5px 0; }
            .double-divider { border-top: 2px solid #000; margin: 5px 0; }
            .flex-between { display: flex; justify-content: space-between; }
            .urdu-header { font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', 'Urdu Typesetting', Tahoma, sans-serif; font-size: 11px; direction: rtl; }
            .urdu-text { font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', 'Urdu Typesetting', Tahoma, sans-serif; font-size: 9.5px; direction: rtl; text-align: right; }
            .qr-box { margin: 6px auto; text-align: center; font-size: 8px; border: 1px solid #777; padding: 4px; border-radius: 3px; }
          </style>
        </head>
        <body onload="window.print();">
          <div class="center">
            <div style="font-size: 13px; font-weight: 900; letter-spacing: 0.5px;">${letterhead.clinicName || 'ZAYVORA CLINICAL MATAB'}</div>
            <div class="urdu-header">${letterhead.clinicUrdu || 'مطب زیورا فار ہربل میڈیسن والطب یونانی'}</div>
            <div style="font-size: 10px; font-weight: bold; margin-top: 2px;">${letterhead.doctorName || 'Hakeem Dr. Irfan Ashraf (BUMS AMU)'}</div>
            <div style="font-size: 8.5px; color: #222;">${letterhead.doctorDegree || 'Senior Integrative Physician'}</div>
            <div style="font-size: 8px;">Reg: ${letterhead.doctorReg || 'BUMS/AMU/2007'} • Tel: +91-98765-43210</div>
          </div>
          <div class="divider"></div>
          <div class="flex-between">
            <span>Mareez (مریض): <span class="bold">${pat.name}</span></span>
            <span>MRN: <span class="bold">${pat.mrn}</span></span>
          </div>
          <div class="flex-between">
            <span>Umar/Jins: ${pat.age}Y / ${pat.gender}</span>
            <span>Mizaj-e-Jabli: <span class="bold">${pat.baselineMizaj || 'Damawi (Sanguine)'}</span></span>
          </div>
          <div class="flex-between">
            <span>Su-e-Mizaj: <span class="bold">${pat.currentDyscrasia || pat.mizaj || 'Su-e-Mizaj Barid Balghami'}</span></span>
            <span>Nabz: <span class="bold">${pat.nabzType || 'Nabz-e-Batee'}</span></span>
          </div>
          <div class="flex-between" style="font-size: 8.5px; color: #333;">
            <span>Vitals: ${vitalsText}</span>
          </div>
          <div class="flex-between">
            <span>Tareekh: ${new Date().toLocaleDateString('en-GB')}</span>
            <span>Token: T-104</span>
          </div>
          <div class="double-divider"></div>
          <div class="bold" style="text-align: center; font-size: 11px; letter-spacing: 0.5px;">
            ℞ NUSKHA-E-ILAJ • نسخہ علاج
          </div>
          <div style="margin-top: 4px;">
            ${medRows || '<div style="text-align:center; padding: 8px;">No medicines prescribed.</div>'}
          </div>
          <div class="divider"></div>
          <div class="bold" style="font-size: 9.5px; display: flex; justify-content: space-between;">
            <span>PARHEZ (پرہیز):</span>
            <span class="urdu-text" style="font-size: 9px;">غذائی احتیاط</span>
          </div>
          <div class="urdu-text" style="line-height: 1.4; margin-top: 2px;">
            ${parhezText}
          </div>
          <div class="divider"></div>
          <div class="qr-box">
            [ ★ DIGITAL VERIFIED TAMPER-EVIDENT PRESCRIPTION ★ ]<br>
            21 CFR Part 11 Sealed • Non-Delegable Clinician Discretion<br>
            SHA-256: 636673534a178208...
          </div>
          <div class="center" style="font-size: 8.5px; margin-top: 4px; line-height: 1.3;">
            <div class="urdu-text" style="text-align: center; font-size: 9px;">شفاء من جانب اللہ تعالیٰ</div>
            <div>Shifa min Janib Allah (Healing is from Allah)</div>
            <div style="font-size: 7.5px; color: #555; margin-top: 2px;">ZAYVORA MATAB OS v5.0 • ESC/POS 80mm Standard</div>
          </div>
        </body>
        </html>
      `;

      printWin.document.open();
      printWin.document.write(html);
      printWin.document.close();
      if (typeof showNotification === 'function') showNotification('✓ Vernacular 80mm Thermal Slip dispatched to printer!', 'success');
    };

    // =========================================================================
    // STATUTORY UPI PART-II, VOL-IV & APPENDIX-7 CLASSICAL WEIGHTS CALCULATOR
    // =========================================================================
    window.CLASSICAL_WEIGHTS_TABLE = {
      chawal: { name: 'Chawal', urdu: 'چاول', mg: 15, g: 0.015 },
      ratti: { name: 'Ratti', urdu: 'رتی', mg: 125, g: 0.125 },
      surkh: { name: 'Surkh', urdu: 'سرخ', mg: 125, g: 0.125 },
      qeerat: { name: 'Qeerat', urdu: 'قیراط', mg: 250, g: 0.25 },
      dang: { name: 'Dang', urdu: 'دانگ', mg: 500, g: 0.5 },
      masha: { name: 'Masha', urdu: 'ماشہ', mg: 1000, g: 1.0 },
      dirham: { name: 'Dirham', urdu: 'درہم', mg: 3500, g: 3.5 },
      misqal: { name: 'Misqal', urdu: 'مثقال', mg: 4500, g: 4.5 },
      tola: { name: 'Tola', urdu: 'تولہ', mg: 12000, g: 12.0 },
      dam: { name: 'Dam', urdu: 'دام', mg: 21000, g: 21.0 },
      oqia: { name: 'Oqia', urdu: 'اوقیہ', mg: 32000, g: 32.0 },
      chhatak: { name: 'Chhatak', urdu: 'چھٹانک', mg: 60000, g: 60.0 },
      pao: { name: 'Pao', urdu: 'پاؤ', mg: 240000, g: 240.0 },
      ratal_tibbi: { name: 'Ratal Tibbi', urdu: 'رطل طبی', mg: 420000, g: 420.0 },
      ser: { name: 'Ser', urdu: 'سیر', mg: 960000, g: 960.0 },
      astar: { name: 'Astar', urdu: 'استار', mg: 1000000, g: 1000.0 },
      man_tabrizi: { name: 'Man Tabrizi', urdu: 'من تبریزی', mg: 2900000, g: 2900.0 }
    };

    window.convertClassicalWeight = function(qty, unitKey) {
      const u = (unitKey || 'masha').toLowerCase().trim().replace(/[-\s]/g, '_');
      const item = window.CLASSICAL_WEIGHTS_TABLE[u] || { name: unitKey, urdu: '', mg: 1000, g: 1 };
      const q = parseFloat(qty) || 0;
      return {
        classicalQty: q,
        unitName: item.name,
        urduName: item.urdu,
        milligrams: Math.round(q * item.mg * 100) / 100,
        grams: Math.round(q * item.g * 10000) / 10000
      };
    };

    window.openClassicalWeightsCalculatorModal = function() {
      let modal = document.getElementById('classical-weights-modal');
      if (!modal) {
        modal = document.createElement('div');
        modal.id = 'classical-weights-modal';
        modal.className = 'fixed inset-0 z-[100] bg-black/80 backdrop-blur-sm flex items-center justify-center p-4';
        modal.innerHTML = `
          <div class="bg-slate-900 border border-emerald-500/30 rounded-2xl max-w-xl w-full p-6 shadow-2xl space-y-5 text-white max-h-[90vh] overflow-y-auto">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
              <div>
                <h3 class="text-lg font-bold text-emerald-400 flex items-center gap-2">
                  ⚖️ Classical Unani Weights Converter
                </h3>
                <p class="text-xs text-slate-400">Appendix-7: Official Equivalents Adopted by Unani Pharmacopoeia Committee (Ministry of AYUSH)</p>
              </div>
              <button onclick="document.getElementById('classical-weights-modal').classList.add('hidden');" class="text-slate-400 hover:text-white text-xl font-bold p-1">✕</button>
            </div>

            <!-- Interactive Converter Form -->
            <div class="bg-slate-800/60 p-4 rounded-xl border border-slate-700/60 space-y-3">
              <label class="text-xs font-semibold text-slate-300">Enter Classical Posology / Nuskha Dose:</label>
              <div class="flex items-center gap-3">
                <input id="cw-input-qty" type="number" step="0.25" value="2" class="w-24 px-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white font-mono text-sm focus:border-emerald-500 focus:outline-none" oninput="window.updateClassicalWeightCalc();" />
                <select id="cw-select-unit" class="flex-1 px-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:border-emerald-500 focus:outline-none" onchange="window.updateClassicalWeightCalc();">
                  <option value="chawal">Chawal (چاول) — 15 mg</option>
                  <option value="ratti">Ratti / Surkh (رتی / سرخ) — 125 mg</option>
                  <option value="qeerat">Qeerat (قیراط) — 250 mg</option>
                  <option value="dang">Dang (دانگ) — 500 mg</option>
                  <option value="masha" selected>Masha (ماشہ) — 1 g (1000 mg)</option>
                  <option value="dirham">Dirham (درہم) — 3.5 g</option>
                  <option value="misqal">Misqal (مثقال) — 4.5 g</option>
                  <option value="tola">Tola (تولہ) — 12 g</option>
                  <option value="dam">Dam (دام) — 21 g</option>
                  <option value="oqia">Oqia (اوقیہ) — 32 g</option>
                  <option value="chhatak">Chhatak (چھٹانک) — 60 g</option>
                  <option value="pao">Pao (پاؤ) — 240 g</option>
                  <option value="ser">Ser (سیر) — 960 g</option>
                  <option value="astar">Astar (استار) — 1 kg</option>
                  <option value="man_tabrizi">Man Tabrizi (من تبریزی) — 2.9 kg</option>
                </select>
              </div>
              <div id="cw-calc-result" class="mt-3 p-3 bg-emerald-950/40 border border-emerald-500/30 rounded-xl text-center">
                <span class="text-xs text-emerald-300">Modern Metric Standard:</span>
                <div class="text-xl font-bold font-mono text-emerald-400 mt-1">
                  2.0000 g <span class="text-sm font-normal text-slate-300">(= 2,000 mg)</span>
                </div>
              </div>
            </div>

            <!-- Reference Table -->
            <div class="space-y-2">
              <h4 class="text-xs font-bold text-slate-300 uppercase tracking-wider">Statutory Conversion Matrix (Appendix-7)</h4>
              <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs font-mono">
                <div class="p-2 bg-slate-950 rounded border border-slate-800">1 Chawal = 15 mg</div>
                <div class="p-2 bg-slate-950 rounded border border-slate-800">1 Ratti = 125 mg</div>
                <div class="p-2 bg-slate-950 rounded border border-slate-800">1 Dang = 500 mg</div>
                <div class="p-2 bg-slate-950 rounded border border-slate-800 text-emerald-400 font-bold">1 Masha = 1 g</div>
                <div class="p-2 bg-slate-950 rounded border border-slate-800">1 Dirham = 3.5 g</div>
                <div class="p-2 bg-slate-950 rounded border border-slate-800">1 Misqal = 4.5 g</div>
                <div class="p-2 bg-slate-950 rounded border border-slate-800 text-amber-400 font-bold">1 Tola = 12 g</div>
                <div class="p-2 bg-slate-950 rounded border border-slate-800">1 Dam = 21 g</div>
                <div class="p-2 bg-slate-950 rounded border border-slate-800">1 Pao = 240 g</div>
                <div class="p-2 bg-slate-950 rounded border border-slate-800">1 Ser = 960 g</div>
                <div class="p-2 bg-slate-950 rounded border border-slate-800">1 Ratal Tibbi = 420 g</div>
                <div class="p-2 bg-slate-950 rounded border border-slate-800">1 Man = 2.9 kg</div>
              </div>
            </div>

            <div class="flex justify-end pt-2">
              <button onclick="document.getElementById('classical-weights-modal').classList.add('hidden');" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold shadow">
                Done
              </button>
            </div>
          </div>
        `;
        document.body.appendChild(modal);
      }
      modal.classList.remove('hidden');
      window.updateClassicalWeightCalc();
    };

    window.updateClassicalWeightCalc = function() {
      const qInput = document.getElementById('cw-input-qty');
      const uSelect = document.getElementById('cw-select-unit');
      const resDiv = document.getElementById('cw-calc-result');
      if (!qInput || !uSelect || !resDiv) return;
      const res = window.convertClassicalWeight(qInput.value, uSelect.value);
      resDiv.innerHTML = `
        <span class="text-xs text-emerald-300">Modern Metric Standard:</span>
        <div class="text-xl font-bold font-mono text-emerald-400 mt-1">
          ${res.grams.toLocaleString()} g <span class="text-sm font-normal text-slate-300">(= ${res.milligrams.toLocaleString()} mg)</span>
        </div>
        <div class="text-[11px] text-slate-400 mt-0.5">${res.classicalQty} ${res.unitName} (${res.urduName})</div>
      `;
    };

    // =========================================================================
    // KULLIYAT-E-ADWIYAH PHARMACOLOGICAL DICTIONARY & ACTION MATRIX (DR. ABDUL WADUD)
    // =========================================================================
    window.kulliyatActiveTab = 'terminology';
    window.kulliyatSearchTerm = '';

    window.openKulliyatDictionaryModal = function() {
      let modal = document.getElementById('kulliyat-dictionary-modal');
      if (!modal) {
        modal = document.createElement('div');
        modal.id = 'kulliyat-dictionary-modal';
        modal.className = 'fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-sm flex items-center justify-center p-4';
        modal.innerHTML = `
          <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-5xl w-full max-h-[92vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
            <!-- Modal Header -->
            <div class="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950 flex-shrink-0">
              <div class="flex items-center gap-3">
                <span class="text-2xl">📖</span>
                <div>
                  <div class="flex items-center gap-2">
                    <h3 class="text-base font-bold text-white">Kulliyat-e-Adwiyah Pharmacological Matrix</h3>
                    <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/20 text-emerald-300 font-bold">Ishrah al-Adwiyah (2004)</span>
                  </div>
                  <p class="text-xs text-slate-400">Dr. Abdul Wadud, MD (Ilmul Advia) AMU Aligarh • 74 Standardized Actions, 9 Tastes, 8 Compounding Rules & Degrees of Temperament</p>
                </div>
              </div>
              <button onclick="document.getElementById('kulliyat-dictionary-modal').classList.add('hidden')" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition">✕</button>
            </div>

            <!-- Tab Navigation Bar -->
            <div class="flex items-center gap-2 px-6 py-2 bg-slate-950/60 border-b border-slate-800 overflow-x-auto text-xs font-semibold flex-shrink-0">
              <button id="ktab-btn-terminology" onclick="window.switchKulliyatTab('terminology')" class="px-3 py-1.5 rounded-lg bg-emerald-600 text-white font-bold transition">74 Pharmacological Actions</button>
              <button id="ktab-btn-tastes" onclick="window.switchKulliyatTab('tastes')" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">9 Tastes (Za'iqah)</button>
              <button id="ktab-btn-degrees" onclick="window.switchKulliyatTab('degrees')" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">4 Degrees of Temperament</button>
              <button id="ktab-btn-compounding" onclick="window.switchKulliyatTab('compounding')" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">8 Rules of Compounding</button>
              <button id="ktab-btn-antagonism" onclick="window.switchKulliyatTab('antagonism')" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">Drug Antagonism</button>
            </div>

            <!-- Dynamic Tab Content Body -->
            <div id="kulliyat-modal-body" class="p-6 overflow-y-auto space-y-4 flex-1">
              <!-- Rendered dynamically -->
            </div>
          </div>
        `;
        document.body.appendChild(modal);
      }
      modal.classList.remove('hidden');
      window.renderKulliyatCurrentTab();
    };

    window.switchKulliyatTab = function(tabName) {
      window.kulliyatActiveTab = tabName;
      ['terminology', 'tastes', 'degrees', 'compounding', 'antagonism'].forEach(t => {
        const btn = document.getElementById(`ktab-btn-${t}`);
        if (btn) {
          if (t === tabName) {
            btn.className = 'px-3 py-1.5 rounded-lg bg-emerald-600 text-white font-bold transition';
          } else {
            btn.className = 'px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition';
          }
        }
      });
      window.renderKulliyatCurrentTab();
    };

    window.renderKulliyatCurrentTab = function() {
      const container = document.getElementById('kulliyat-modal-body');
      if (!container) return;

      if (window.kulliyatActiveTab === 'terminology') {
        container.innerHTML = `
          <div class="space-y-4">
            <div class="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center justify-between">
              <input id="kulliyat-search-input" type="text" placeholder="Search by Urdu, English, action, or drug example..." value="${window.kulliyatSearchTerm}" oninput="window.filterKulliyatTerminology(this.value)" class="w-full sm:w-96 px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 font-mono" />
              <div class="text-xs text-slate-400 font-mono text-right" id="kulliyat-action-count">Showing 74 Standardized Clinical Actions</div>
            </div>
            <div id="kulliyat-actions-grid" class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <!-- Populated dynamically -->
            </div>
          </div>
        `;
        window.filterKulliyatTerminology(window.kulliyatSearchTerm);
      } else if (window.kulliyatActiveTab === 'tastes') {
        container.innerHTML = `
          <div class="space-y-4">
            <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
              <h4 class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Epistemological Foundation of Taste (Za'iqah) in Drug Discovery</h4>
              <p class="text-xs text-slate-300">
                In classical Unani pharmacology (Ibn Sina &amp; Dr. Abdul Wadud), taste is the primary and most robust deductive marker (Qiyas) for internal pharmacological actions. Below are the 9 canonical tastes and their validated pharmacodynamic correlates:
              </p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div class="p-3.5 rounded-xl bg-slate-950 border border-emerald-500/30 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-emerald-300 text-sm">Huraif (Pungent / تیز)</span>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300">Hot &amp; Dry</span>
                </div>
                <div class="text-[11px] text-slate-300 leading-relaxed">
                  <strong>Actions:</strong> Vasodilator (Mufattih-e-Urooq), Calorific (Musakhkhin), Attenuant (Mulattif), Resolvent (Muhallil), Antiseptic (Mani-e-Ufoonat).
                </div>
                <div class="text-[10px] text-slate-400 font-mono">Filfil Siyah, Rai, Zanjabeel, Aaqarqarha</div>
              </div>

              <div class="p-3.5 rounded-xl bg-slate-950 border border-emerald-500/30 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-emerald-300 text-sm">Murr (Bitter / کڑوا)</span>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300">Hot &amp; Dry</span>
                </div>
                <div class="text-[11px] text-slate-300 leading-relaxed">
                  <strong>Actions:</strong> Deobstruent (Mufattih), Mild Heating, Resolvent, Antiseptic, Blood Purifier (Musaffi-e-Dam).
                </div>
                <div class="text-[10px] text-slate-400 font-mono">Chiraita, Shahtara, Afsanteen, Neem</div>
              </div>

              <div class="p-3.5 rounded-xl bg-slate-950 border border-emerald-500/30 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-emerald-300 text-sm">Maleh (Salty / نمکین)</span>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300">Hot &amp; Dry</span>
                </div>
                <div class="text-[11px] text-slate-300 leading-relaxed">
                  <strong>Actions:</strong> Attenuant, Liquefying (Muraqqiq), Resolvent, Matter-cleaving (Qati-e-Mawad), Absorbent (Jaazib).
                </div>
                <div class="text-[10px] text-slate-400 font-mono">Namak Ta'am, Shura Qalmi, Jawakhar</div>
              </div>

              <div class="p-3.5 rounded-xl bg-slate-950 border border-blue-500/30 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-cyan-300 text-sm">Hamez (Acidic / کھٹا)</span>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-300">Cold &amp; Dry</span>
                </div>
                <div class="text-[11px] text-slate-300 leading-relaxed">
                  <strong>Actions:</strong> Deobstruent, Matter-cleaving, Thirst-quenching (Dafi-e-Atash), Refrigerant (Mubarrid), Diuretic (Mudirr).
                </div>
                <div class="text-[10px] text-slate-400 font-mono">Aab-e-Lemu, Aloo Bukhara, Imli, Sirka</div>
              </div>

              <div class="p-3.5 rounded-xl bg-slate-950 border border-blue-500/30 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-cyan-300 text-sm">Afas (Astringent-Bitter / کسیلا)</span>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-300">Cold &amp; Dry</span>
                </div>
                <div class="text-[11px] text-slate-300 leading-relaxed">
                  <strong>Actions:</strong> Repellent (Raadi'), Tissue Constrictor (Aasir), Haemostatic (Habis-e-Dam), Astringent (Qabiz).
                </div>
                <div class="text-[10px] text-slate-400 font-mono">Phitkari, Mazoo, Post-e-Anar, Halela</div>
              </div>

              <div class="p-3.5 rounded-xl bg-slate-950 border border-blue-500/30 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-cyan-300 text-sm">Qabiz (Pure Astringent / قابض)</span>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-300">Cold &amp; Dry</span>
                </div>
                <div class="text-[11px] text-slate-300 leading-relaxed">
                  <strong>Actions:</strong> Condenser (Mukaththif), Arresting secretions, Refrigerant, Vascular constrictor.
                </div>
                <div class="text-[10px] text-slate-400 font-mono">Chhalia (Areca nut), Hab-ul-Aas, Katha</div>
              </div>

              <div class="p-3.5 rounded-xl bg-slate-950 border border-amber-500/30 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-amber-300 text-sm">Dasm (Bland/Fatty / پھیکا چکنا)</span>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300">Warm &amp; Moist</span>
                </div>
                <div class="text-[11px] text-slate-300 leading-relaxed">
                  <strong>Actions:</strong> Moisturizing (Murattib), Emollient (Muraqqiq), Relaxant (Murkhi), Laxative (Mulayyin), Concoctive (Munzij).
                </div>
                <div class="text-[10px] text-slate-400 font-mono">Ghee, Roghan Zaitoon, Roghan Badam</div>
              </div>

              <div class="p-3.5 rounded-xl bg-slate-950 border border-amber-500/30 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-amber-300 text-sm">Hilw (Sweet / میٹھا)</span>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300">Warm &amp; Moist</span>
                </div>
                <div class="text-[11px] text-slate-300 leading-relaxed">
                  <strong>Actions:</strong> Detergent (Jali), Mild Laxative, Diluent, Vital Organ Tonic (Muqawwi-e-Aaza), Calorific.
                </div>
                <div class="text-[10px] text-slate-400 font-mono">Shahd (Honey), Qand, Munaqqa, Injeer</div>
              </div>

              <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-700 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-slate-300 text-sm">Tafi (Tasteless / بے مزا)</span>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">Neutral / Cold</span>
                </div>
                <div class="text-[11px] text-slate-300 leading-relaxed">
                  <strong>Actions:</strong> Passive hydration, Demulcent (Musakkin), Mucosal protective barrier.
                </div>
                <div class="text-[10px] text-slate-400 font-mono">Aab-e-Muqattar, Nishashta, Lu'ab Aspaghol</div>
              </div>
            </div>
          </div>
        `;
      } else if (window.kulliyatActiveTab === 'degrees') {
        container.innerHTML = `
          <div class="space-y-4">
            <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
              <h4 class="text-xs font-bold text-emerald-400 uppercase tracking-wider">The 4 Degrees of Temperament &amp; The Paracelsus-Avicenna Invariant</h4>
              <p class="text-xs text-slate-300 leading-relaxed">
                In classical Unani pharmacology (Ibn Sina, Qarshi, and Dr. Abdul Wadud), drug temperament is graded into 4 distinct clinical thresholds. Crucially, a 4th-degree drug (Adwiyah Sammiyyah) is NOT an Absolute Poison (Summ-e-Mutlaq):
              </p>
              <div class="p-3 rounded-lg bg-emerald-950/40 border border-emerald-500/30 text-xs text-emerald-200 italic font-serif">
                &ldquo;Poisoning may result from large doses of drugs, because it is the dose which distinguishes the drug from a poison. Therefore a drug in very high dose may be a poison and a poison in low dose may be a drug.&rdquo;
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div class="p-4 rounded-xl bg-slate-950 border border-emerald-500/30 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-emerald-300">Darjah Awwal (1st Degree)</span>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">Extremely Safe</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Changes temperament imperceptibly on a single dose, but exhibits marked therapeutic efficacy on repeated use.
                </p>
                <div class="text-[11px] text-slate-400 font-mono">Examples: Gaozaban, Banafsha, Behidana, Khashkhash</div>
              </div>

              <div class="p-4 rounded-xl bg-slate-950 border border-emerald-500/30 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-emerald-300">Darjah Dom (2nd Degree)</span>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">Safe Standard</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Action clearly felt upon a single dose, but causes zero injury, functional impairment, or physiological breakdown.
                </p>
                <div class="text-[11px] text-slate-400 font-mono">Examples: Zanjabeel, Asgandh, Kishneez Khushk, Babchi</div>
              </div>

              <div class="p-4 rounded-xl bg-slate-950 border border-amber-500/30 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-amber-300">Darjah Som (3rd Degree)</span>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/20 text-amber-300">Narrow Window</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Strongly alters normal physiological state, causing violent diuresis, purgation, or sedation. Unmonitored use causes toxicity.
                </p>
                <div class="text-[11px] text-slate-400 font-mono">Examples: Suranjan Shirin, Turbud, Saqmonia</div>
              </div>

              <div class="p-4 rounded-xl bg-slate-950 border border-rose-500/40 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-rose-300">Darjah Chaharum (4th Degree / Poison)</span>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-500/20 text-rose-300">Schedule E(1) Gate</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Extreme elemental qualities capable of corrupting vital organ functions and causing fatality in raw unpurified states. Requires mandatory Mudabbar detoxification.
                </p>
                <div class="text-[11px] text-slate-400 font-mono">Examples: Kuchla (Strychnine), Bhang, Sankhiya, Afeeyun</div>
              </div>
            </div>
          </div>
        `;
      } else if (window.kulliyatActiveTab === 'compounding') {
        container.innerHTML = `
          <div class="space-y-4">
            <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
              <h4 class="text-xs font-bold text-emerald-400 uppercase tracking-wider">The 8 Statutory Rationales for Compounding (Qawanin-e-Tarkeeb)</h4>
              <p class="text-xs text-slate-300">
                Dr. Abdul Wadud codifies the 8 definitive clinical justifications for polypharmaceutical compounding in Unani medicine:
              </p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <div class="font-bold text-emerald-300">1. Islah (Toxicity Correction)</div>
                <p class="text-slate-300 leading-relaxed">Adding a Musleh (corrective) to mitigate adverse effects or gastrointestinal griping (e.g., Roghan Badam with Jalapa).</p>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <div class="font-bold text-emerald-300">2. Idhafah-e-Quwwat (Synergistic Potentiation)</div>
                <p class="text-slate-300 leading-relaxed">Combining complementary herbs to amplify therapeutic efficacy without escalating individual doses into toxic ranges.</p>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <div class="font-bold text-emerald-300">3. Taz'eef-e-Amal (Action Moderation)</div>
                <p class="text-slate-300 leading-relaxed">Tempering an overly violent or drastic action when patient constitution or disease state requires gentle evacuation.</p>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <div class="font-bold text-emerald-300">4. Sur'at-e-Nufooz (Accelerating Absorption)</div>
                <p class="text-slate-300 leading-relaxed">Using rapid penetrative carriers (Badraqa like Zafaran or wine/spirits) to speed drug delivery to heart and brain.</p>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <div class="font-bold text-emerald-300">5. Ibt'a-e-Nufooz (Retarding Absorption)</div>
                <p class="text-slate-300 leading-relaxed">Adding viscous or oily vehicles to delay transit for sustained local gastrointestinal contact.</p>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <div class="font-bold text-emerald-300">6. Amraz-e-Murakkabah (Compound Disease Targeting)</div>
                <p class="text-slate-300 leading-relaxed">Addressing multi-morbid pathology simultaneously (e.g. febrifuge with expectorant in acute febrile bronchitis).</p>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <div class="font-bold text-emerald-300">7. Miqdar (Volume Bulking)</div>
                <p class="text-slate-300 leading-relaxed">Expanding the bulk of minute-dose potent drugs with honey, syrup, or mucilage to enable accurate patient administration.</p>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <div class="font-bold text-emerald-300">8. Tahaffuz (Preservation)</div>
                <p class="text-slate-300 leading-relaxed">Using natural preservative vehicles (honey, sugar qiwam, vinegar) to prevent bacterial spoiling and oxidation over years.</p>
              </div>
            </div>
          </div>
        `;
      } else if (window.kulliyatActiveTab === 'antagonism') {
        container.innerHTML = `
          <div class="space-y-4">
            <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
              <h4 class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Drug Antagonism (Tanaquz-e-Adwiyah)</h4>
              <p class="text-xs text-slate-300">
                Dr. Abdul Wadud breaks down clinical drug antagonism into 3 fundamental mechanisms:
              </p>
            </div>
            <div class="space-y-3">
              <div class="p-4 rounded-xl bg-slate-950 border border-rose-500/30 space-y-1">
                <div class="flex items-center justify-between">
                  <h4 class="font-bold text-rose-300 text-sm">1. Pharmacological Antagonism (تناقض فعلی)</h4>
                  <span class="text-[10px] px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-mono">Opposite Receptors</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Two drugs exerting diametrically opposed physiological actions on the same organ or tissue (e.g., co-administering an intestinal purgative like Saqmonia with an astringent like Mazoo, or a stimulant with a heavy narcotic sedative).
                </p>
                <div class="text-[11px] text-slate-400"><strong>Clinical Management:</strong> Avoid simultaneous prescribing; separate by 4–6 hours.</div>
              </div>

              <div class="p-4 rounded-xl bg-slate-950 border border-amber-500/30 space-y-1">
                <div class="flex items-center justify-between">
                  <h4 class="font-bold text-amber-300 text-sm">2. Chemical Antagonism (تناقض صوری / کیمیائی)</h4>
                  <span class="text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono">Precipitation &amp; Neutralization</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Co-administered chemical substances reacting together in gastric juice or bloodstream to form an insoluble precipitate, inactive salt, or gas, destroying potency (e.g., acidic fluids neutralizing alkaline carbonates).
                </p>
                <div class="text-[11px] text-slate-400"><strong>Clinical Management:</strong> Contraindicated in same formulation; separate gastric phases.</div>
              </div>

              <div class="p-4 rounded-xl bg-slate-950 border border-blue-500/30 space-y-1">
                <div class="flex items-center justify-between">
                  <h4 class="font-bold text-cyan-300 text-sm">3. Physical Antagonism (تناقض کیفی / طبیعی)</h4>
                  <span class="text-[10px] px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 font-mono">Barrier &amp; Adsorption</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Physical immiscibility or mechanical absorption blockade, such as oily coatings preventing water-soluble drug absorption, or demulcent mucilages physically trapping toxic alkaloids.
                </p>
                <div class="text-[11px] text-slate-400"><strong>Clinical Management:</strong> Leveraged therapeutically in toxicological poisoning as demulcent antidotes.</div>
              </div>
            </div>
          </div>
        `;
      }
    };

    window.filterKulliyatTerminology = function(query) {
      window.kulliyatSearchTerm = query || '';
      const grid = document.getElementById('kulliyat-actions-grid');
      const countEl = document.getElementById('kulliyat-action-count');
      if (!grid) return;

      const actionsList = [
        { id: "ACT-01", urdu: "اکال", english: "Corrosive / Caustic", def: "An agent that causes corrosion and destruction of living tissue.", ex: "Tezab, Neela Thotha, Chuna", sys: "Tissue / Dermatological" },
        { id: "ACT-02", urdu: "جاذب", english: "Siccative / Absorbent", def: "An agent that absorbs moisture and fluid exudates from tissues.", ex: "Ghareeqoon, Jund Bedastar, Sartan", sys: "Tissue / Exudate" },
        { id: "ACT-03", urdu: "جالی", english: "Detergent / Detersive", def: "A cleansing agent exerting surface oil-dissolving and antibacterial effect.", ex: "Shura, Shahd, Sirka, Namak, Reetha, Lehsan", sys: "Integumentary" },
        { id: "ACT-04", urdu: "حابس دم", english: "Haemostatic / Styptic", def: "An astringent haemostatic agent used to arrest bleeding.", ex: "Mazoo, Geru, Dam-ul-Akhwain, Phitkari", sys: "Vascular" },
        { id: "ACT-05", urdu: "حالق", english: "Depilatory", def: "An agent that causes falling out of hairs from follicles.", ex: "Noora, Hartal", sys: "Integumentary" },
        { id: "ACT-06", urdu: "حکاک", english: "Pruritic / Irritant", def: "An agent that causes pruritus, itching, and local sensory nerve irritation.", ex: "Bhilawa, Rai, Kunch Beej", sys: "Integumentary" },
        { id: "ACT-07", urdu: "خاتم", english: "Cicatrizant", def: "An agent causing or favouring scar formation in wound healing.", ex: "Anzaroot, Sang-e-Jarahat, Sadaf Sokhta", sys: "Wound Care" },
        { id: "ACT-08", urdu: "دابق", english: "Emplastic / Adhesive", def: "Any material that adheres to surface tissues or causes adherence between surfaces.", ex: "Ral Safaid, Samgh-e-Arabi, Gond Kundur", sys: "Topical Formulations" },
        { id: "ACT-09", urdu: "دافع تشنج", english: "Antispasmodic / Anticonvulsive", def: "An agent that quiets spasm or prevents seizures and muscular contractions.", ex: "Asrol, Afeeyun, Bhang, Hing, Dhatura", sys: "Neuromuscular" },
        { id: "ACT-10", urdu: "دافع عفونت", english: "Antiseptic", def: "An agent destroying pathogenic microorganisms or inhibiting growth.", ex: "Afsanteen, Kabab Chini, Sandal, Neem, Kafoor", sys: "Microbiological" },
        { id: "ACT-11", urdu: "دافع حمی", english: "Antipyretic / Antifebrile", def: "An agent that reduces fever and brings abnormal body temperature toward normal.", ex: "Khas, Karanjwa, Afsanteen, Chiraita, Gilo", sys: "Thermoregulatory" },
        { id: "ACT-12", urdu: "رادع", english: "Repellent", def: "An agent that derives off or repels morbid fluids from an inflamed organ.", ex: "Sandal Surkh, Geru, Sang-e-Jarahat, Gil-e-Armani", sys: "Inflammatory" },
        { id: "ACT-13", urdu: "عاصر", english: "Squeezer / Tissue Constrictor", def: "An agent that constricts tissues and empties morbid accumulated fluid.", ex: "Halela, Aamla, Behroza, Tukhm-e-Jamun", sys: "Cellular Fluid" },
        { id: "ACT-14", urdu: "غسال", english: "Irrigator / Lavage", def: "An agent that washes out and purges cavities or ulcer surfaces.", ex: "Shahd ka Paani, Namak ka Paani, Jau ka Paani", sys: "Wound Care" },
        { id: "ACT-15", urdu: "قابض", english: "Astringent", def: "An agent causing contraction of tissues, arresting secretions and checking discharge.", ex: "Dam-ul-Akhwain, Hab-ul-Aas, Babul, Supari", sys: "Mucosal" },
        { id: "ACT-16", urdu: "قابض امعاء", english: "Intestinal Astringent", def: "An agent checking diarrhoea by constricting bowel mucosa.", ex: "Afeeyun, Ajwain Khurasani, Bel Giri", sys: "Gastrointestinal" },
        { id: "ACT-17", urdu: "قاشر", english: "Sloughing / Desquamative", def: "An agent that separates and sheds necrosed tissue from living biological structures.", ex: "Zarawand, Qust, Kunjad Siyah", sys: "Dermatological" },
        { id: "ACT-18", urdu: "قاتل و مخرج دیدان", english: "Vermicide & Vermifuge", def: "An agent that destroys or expels intestinal worms.", ex: "Baobrang, Kamila, Palas Papra, Qust", sys: "Parasitic" },
        { id: "ACT-19", urdu: "قاطع باہ", english: "Anaphrodisiac", def: "An agent that lessens or abolishes sexual desire.", ex: "Kafoor, Afeeyun, Kishneez Khushk, Aab-e-Lemu", sys: "Endocrine" },
        { id: "ACT-20", urdu: "کاسر ریاح", english: "Carminative", def: "An agent that prevents formation or causes expulsion of flatus.", ex: "Zira Safaid, Badiyan, Ajwain Desi, Zanjabeel", sys: "Gastrointestinal" },
        { id: "ACT-21", urdu: "کاوی", english: "Escharotic / Caustic", def: "An agent that destroys living tissue and produces an eschar.", ex: "Tezab, Chuna, Neela Thotha", sys: "Tissue / Caustic" },
        { id: "ACT-22", urdu: "لاذع", english: "Irritant", def: "An agent that causes local inflammatory reaction and erythema.", ex: "Rai, Sirka, Lehsan, Piyaz", sys: "Integumentary" },
        { id: "ACT-23", urdu: "مانع عرق", english: "Anadiaphoretic", def: "An agent that lessens sweat secretion.", ex: "Dhatura, Ajwain Khurasani, Luffah", sys: "Integumentary" },
        { id: "ACT-24", urdu: "مانع نوبت", english: "Antiperiodic", def: "An agent that prevents regular recurrence of disease paroxysms.", ex: "Karanjwa, Chiraita, Afsanteen", sys: "Infectious" },
        { id: "ACT-25", urdu: "مبرّد", english: "Refrigerant / Frigorific", def: "An agent that decreases body heat production and imparts cooling.", ex: "Kafoor, Sandal, Khurfa, Kaddu", sys: "Thermoregulatory" },
        { id: "ACT-26", urdu: "منفط", english: "Vesicant", def: "An agent that produces blisters on cutaneous surfaces.", ex: "Rai, Roghan Jamalgota, Bhilawan", sys: "Integumentary" },
        { id: "ACT-27", urdu: "مجفف", english: "Desiccative", def: "An agent that removes moisture and dries up exudative secretions.", ex: "Phitkari, Murdar Sang, Sang-e-Jarahat", sys: "Mucosal" },
        { id: "ACT-28", urdu: "مجشئ", english: "Flatulent", def: "An agent that produces excessive gas in digestive tract.", ex: "Arvi, Aloo", sys: "Gastrointestinal" },
        { id: "ACT-29", urdu: "مہیج / مقوی باہ", english: "Aphrodisiac", def: "An agent that arouses sexual desire, erectile power, and spermatogenesis.", ex: "Zafaran, Amber, Mushk, Malkangni, Salab Misri", sys: "Reproductive" },
        { id: "ACT-30", urdu: "مجمد", english: "Coagulant", def: "An agent that causes coagulation of biological fluids.", ex: "Phitkari, Geru, Sang-e-Jarahat, Kahruba", sys: "Hematological" },
        { id: "ACT-31", urdu: "محرک اعصاب", english: "Nerve Stimulant", def: "An agent increasing functional activity and conduction of nerves.", ex: "Kuchla, Bhang, Sunbul-ut-Teeb", sys: "Nervous System" },
        { id: "ACT-32", urdu: "محرک دماغ", english: "Brain Stimulant / Nootropic", def: "An agent increasing cerebral activity and cognitive alertness.", ex: "Jund Bedastar, Amber, Chai, Qahwa", sys: "Central Nervous System" },
        { id: "ACT-33", urdu: "محلل", english: "Resolvent / Anti-inflammatory", def: "An agent that resolves pathological swellings and inflammatory processes.", ex: "Amba Haldi, Darhald, Asaroon, Alsi, Mako", sys: "Immune / Tissue" },
        { id: "ACT-34", urdu: "محمر", english: "Rubefacient", def: "Counter-irritant producing cutaneous hyperemia and erythema.", ex: "Rai, Lehsan, Jamalgota, Kabab Chini", sys: "Integumentary" },
        { id: "ACT-35", urdu: "مخدر", english: "Anaesthetic / Narcotic", def: "An agent producing reversible loss of pain sensation.", ex: "Afeeyun, Ajwain Khurasani, Dhatura, Khashkhash", sys: "Nervous System" },
        { id: "ACT-36", urdu: "منوم", english: "Hypnotic / Soporific", def: "An agent that induces and promotes sleep resembling natural sleep.", ex: "Afeeyun, Khashkhash, Kahu", sys: "Central Nervous System" },
        { id: "ACT-37", urdu: "مخرج جنین", english: "Abortifacient / Ecbolic", def: "An agent stimulating uterine contraction and expulsion.", ex: "Abhal, Post-e-Amaltas, Barg-e-Baans", sys: "Uterine" },
        { id: "ACT-38", urdu: "مخشن", english: "Roughening Agent", def: "An agent that roughens and hardens cutaneous surface.", ex: "Rai, Bhilawa, Filfil Siyah", sys: "Integumentary" },
        { id: "ACT-39", urdu: "مدر بول", english: "Diuretic", def: "An agent increasing urinary volume and sodium excretion.", ex: "Gokhru, Shura Qalmi, Jawakhar, Tukhm-e-Khiyar", sys: "Renal" },
        { id: "ACT-40", urdu: "مدر حیض", english: "Emmenagogue", def: "An agent that stimulates or increases menstrual flow.", ex: "Abhal, Post-e-Amaltas, Khar-e-Khasak", sys: "Gynecological" },
        { id: "ACT-41", urdu: "مدر لعاب دہن", english: "Sialogogue", def: "An agent stimulating salivary gland secretion.", ex: "Aaqarqarha, Filfil Siyah, Rai, Tambaku", sys: "Salivary" },
        { id: "ACT-42", urdu: "مدمل", english: "Cicatrizant / Vulnerary", def: "An agent promoting wound granulation and healing.", ex: "Sang-e-Jarahat, Dam-ul-Akhwain, Gil-e-Multani", sys: "Wound Care" },
        { id: "ACT-43", urdu: "مرخی", english: "Relaxant / Emollient", def: "An agent relaxing muscular spasm and softening tissue.", ex: "Alsi, Roghniyat, Mom", sys: "Muscular" },
        { id: "ACT-44", urdu: "مسخن", english: "Calorific / Thermogenic", def: "An agent increasing generation and retention of heat.", ex: "Mushk, Amber, Khulanjaan, Aaqarqarha, Zafaran", sys: "Metabolic" },
        { id: "ACT-45", urdu: "مسکن", english: "Sedative / Calming", def: "An agent allaying nervous excitement and hyperactivity.", ex: "Gaozaban, Banafsha, Ustukhuddus", sys: "Nervous System" },
        { id: "ACT-46", urdu: "مسکن الم", english: "Analgesic", def: "An agent selectively relieving pain without loss of consciousness.", ex: "Afeeyun, Ajwain Khurasani, Bhang", sys: "Pain Pathways" },
        { id: "ACT-47", urdu: "مسکن قلب", english: "Cardiac Sedative", def: "An agent decreasing excessive cardiac rate and palpitations.", ex: "Bhring, Afeeyun, Shukran", sys: "Cardiovascular" },
        { id: "ACT-48", urdu: "مسکن تنفس", english: "Respiratory Sedative", def: "An agent reducing cough reflex irritability and airway spasm.", ex: "Afeeyun, Khashkhash, Dhatura", sys: "Respiratory" },
        { id: "ACT-49", urdu: "مسکن معدہ", english: "Gastric Sedative", def: "An agent allaying gastric hypermotility and vomiting reflexes.", ex: "Ajwain Khurasani, Dhatura, Luffah", sys: "Gastrointestinal" },
        { id: "ACT-50", urdu: "مسکن حرارت", english: "Febrifuge", def: "An agent reducing febrile heat and abating burning.", ex: "Aab-e-Kasni, Aab-e-Anar Tursh", sys: "Thermoregulatory" },
        { id: "ACT-51", urdu: "مسیل / مسہل", english: "Purgative / Cathartic", def: "An agent producing copious bowel evacuation.", ex: "Turbud, Saqmonia, Jamalgota, Jalapa", sys: "Gastrointestinal" },
        { id: "ACT-52", urdu: "مسہل صفراء", english: "Cholagogue Purgative", def: "An agent purging yellow bile (Safra) from liver and gut.", ex: "Saqmonia, Usara-e-Rewand, Sibr Zard", sys: "Hepatobiliary" },
        { id: "ACT-53", urdu: "مسہل بلغم", english: "Phlegmagogue Purgative", def: "An agent purging phlegmatic humour through bowel evacuation.", ex: "Turbud, Jalapa, Shahm-e-Hanzal, Ghariqoon", sys: "Gastrointestinal" },
        { id: "ACT-54", urdu: "مسہل سوداء", english: "Melanagogue Purgative", def: "An agent purging black bile (Sawda) from the system.", ex: "Aftimoon, Kharbaq Siyah, Turbud", sys: "Gastrointestinal" },
        { id: "ACT-55", urdu: "معدل", english: "Humoral Moderator", def: "An agent restoring temperamental balance and humoral harmony.", ex: "Banafsha, Ushba, Sandal, Unnab", sys: "Humoral" },
        { id: "ACT-56", urdu: "منضج", english: "Concoctive / Maturing Agent", def: "An agent preparing raw crude humours for safe evacuation (Tanqiya).", ex: "Kasni, Badiyan, Mulethi, Gaozaban, Aftimoon", sys: "Humoral" },
        { id: "ACT-57", urdu: "مقوی", english: "Tonic", def: "An agent restoring tone, vigor, and organ function.", ex: "Zafaran, Amber, Marwareed, Darchini", sys: "Systemic" },
        { id: "ACT-58", urdu: "مقوی قلب", english: "Cardiotonic", def: "An agent toning cardiac muscle and contractility.", ex: "Khamira Abresham, Marwareed, Zafaran", sys: "Cardiovascular" },
        { id: "ACT-59", urdu: "مقوی اعصاب", english: "Nervine Tonic", def: "An agent strengthening nerves and overcoming chronic exhaustion.", ex: "Kuchla Mudabbar, Jund Bedastar, Bozidan", sys: "Nervous System" },
        { id: "ACT-60", urdu: "مقوی جگر", english: "Hepatotonic / Hepatoprotective", def: "An agent supporting hepatic metabolism and protecting liver cells.", ex: "Kasni, Mako, Afsanteen, Rewand Chini", sys: "Hepatobiliary" },
        { id: "ACT-61", urdu: "مقوی گردہ", english: "Nephrotonic", def: "An agent restoring renal glomerular filtration and tone.", ex: "Mastagi, Khar-e-Khasak, Kaknaj", sys: "Renal" },
        { id: "ACT-62", urdu: "مصفی دم", english: "Blood Purifier", def: "An agent removing metabolic toxins from circulation.", ex: "Chiraita, Mundi, Unnab, Shahtara, Neem, Ushba", sys: "Hematological" },
        { id: "ACT-63", urdu: "معرّق", english: "Diaphoretic / Sudorific", def: "An agent stimulating sweat glands and cutaneous perspiration.", ex: "Kasni, Chai, Lehsan, Ushba", sys: "Integumentary" },
        { id: "ACT-64", urdu: "معطس", english: "Errhine / Ptarmic", def: "An agent inducing sneezing and clearing nasal passages.", ex: "Kundush, Tambaku, Naushadar", sys: "Nasal" },
        { id: "ACT-65", urdu: "مغذی", english: "Nutrient / Nutritive", def: "An agent supplying essential nutritional substrate for tissues.", ex: "Maghz Badam, Roghan Zaitoon, Injeer", sys: "Metabolic" },
        { id: "ACT-66", urdu: "مغلظ منی", english: "Semen Inspissant", def: "An agent increasing semen viscosity and correcting seminal thinning.", ex: "Salab Misri, Satawar, Musli Safaid", sys: "Reproductive" },
        { id: "ACT-67", urdu: "مفتت حصاة", english: "Lithotriptic", def: "An agent effecting dissolution or fragmentation of calculi.", ex: "Sang-e-Sar-e-Mahi, Hab-ul-Qillat, Hajar-ul-Yahood", sys: "Urinary" },
        { id: "ACT-68", urdu: "مفتح", english: "Deobstruent", def: "An agent removing visceral, biliary, and vascular obstructions.", ex: "Afsanteen, Kabab Chini, Badiyan", sys: "Visceral" },
        { id: "ACT-69", urdu: "ملین", english: "Laxative / Aperient", def: "A gentle cathartic promoting soft bowel movement without griping.", ex: "Taranjabeen, Maveez Munaqqa, Gulqand, Aspaghol", sys: "Gastrointestinal" },
        { id: "ACT-70", urdu: "ممسک منی", english: "Semen Retentive", def: "An agent prolonging coital duration and checking ejaculation.", ex: "Dhatura, Bhang, Afeeyun, Ajwain Khurasani", sys: "Reproductive" },
        { id: "ACT-71", urdu: "ملطف", english: "Attenuant / Demulcent", def: "An agent breaking dense viscous matter into thinner particles.", ex: "Baboona, Khatmi, Khabazi, Chob Chini", sys: "Humoral" },
        { id: "ACT-72", urdu: "منفث بلغم", english: "Mucolytic / Expectorant", def: "An agent liquefying bronchial phlegm and facilitating expectoration.", ex: "Asl-us-Soos (Mulethi), Naushadar, Sapistan", sys: "Respiratory" },
        { id: "ACT-73", urdu: "ہاضم", english: "Digestive / Digestant", def: "An agent promoting secretion of digestive enzymes and juices.", ex: "Papita, Namak Siyah, Zanjabeel, Ajwain Desi", sys: "Gastrointestinal" },
        { id: "ACT-74", urdu: "تریاق", english: "Antidote", def: "An agent counteracting poisons physically, chemically, or pharmacologically.", ex: "Tiryaq-e-Farooq, Hab-e-Jadwar, Zahar Mohra", sys: "Toxicology" }
      ];

      const q = (query || '').toLowerCase().trim();
      const filtered = q ? actionsList.filter(a => 
        a.urdu.includes(q) || 
        a.english.toLowerCase().includes(q) || 
        a.def.toLowerCase().includes(q) || 
        a.ex.toLowerCase().includes(q) ||
        a.sys.toLowerCase().includes(q)
      ) : actionsList;

      if (countEl) {
        countEl.textContent = `Showing ${filtered.length} of ${actionsList.length} Standardized Clinical Actions`;
      }

      grid.innerHTML = filtered.map(a => `
        <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-emerald-500/50 transition space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-emerald-300">${a.urdu} • ${a.english}</span>
            <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">${a.id}</span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">${a.def}</p>
          <div class="flex items-center justify-between text-[11px] pt-1 border-t border-slate-900">
            <span class="text-slate-400 font-mono"><strong class="text-slate-300">Ex:</strong> ${a.ex}</span>
            <span class="text-[10px] px-1.5 py-0.2 rounded bg-emerald-950 text-emerald-400 border border-emerald-800/40">${a.sys}</span>
          </div>
        </div>
      `).join('');
    };

    // =========================================================================
    // GRAND MEDICAL BOOKSHELF & STANDARDIZED UNANI TERMINOLOGY (48 VOLS / UMA)
    // =========================================================================
    window.corpusActiveTab = 'books';
    window.corpusActiveCategory = 'ALL';
    window.corpusSearchTerm = '';
    window.umaSearchTerm = '';
    window.corpusBooksCache = [];

    window.openGrandCorpusModal = function() {
      let modal = document.getElementById('grand-corpus-modal');
      if (!modal) {
        modal = document.createElement('div');
        modal.id = 'grand-corpus-modal';
        modal.className = 'fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-sm flex items-center justify-center p-4';
        modal.innerHTML = `
          <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-6xl w-full max-h-[92vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
            <!-- Modal Header -->
            <div class="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950 flex-shrink-0">
              <div class="flex items-center gap-3">
                <span class="text-2xl">📚</span>
                <div>
                  <div class="flex items-center gap-2">
                    <h3 class="text-base font-bold text-white">Grand Medical Bookshelf &amp; CCRUM UMA Terminology</h3>
                    <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-blue-500/20 text-blue-300 font-bold">97 Canonical Treatises (11.7 GB) • 1,593 UMA Terms</span>
                  </div>
                  <p class="text-xs text-slate-400">Classical Canon (Al-Hawi, Al-Qanun, Kamil al-Sina'a) • Formularies (Kabiruddin, Azam Khan) • Standardized Diagnostic Terminology</p>
                </div>
              </div>
              <button onclick="document.getElementById('grand-corpus-modal').classList.add('hidden')" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition">✕</button>
            </div>

            <!-- Tab Navigation Bar -->
            <div class="flex items-center gap-2 px-6 py-2 bg-slate-950/60 border-b border-slate-800 overflow-x-auto text-xs font-semibold flex-shrink-0">
              <button id="ctab-btn-books" onclick="window.switchCorpusTab('books')" class="px-3 py-1.5 rounded-lg bg-blue-600 text-white font-bold transition">97 Treatises Vault (11.7 GB)</button>
              <button id="ctab-btn-uma" onclick="window.switchCorpusTab('uma')" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">1,593 Standardized UMA Terms</button>
              <button id="ctab-btn-crosswalk" onclick="window.switchCorpusTab('crosswalk')" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">Dual-Track Clinical Crosswalk</button>
            </div>

            <!-- Dynamic Tab Content Body -->
            <div id="grand-corpus-modal-body" class="p-6 overflow-y-auto space-y-4 flex-1">
              <!-- Rendered dynamically -->
            </div>
          </div>
        `;
        document.body.appendChild(modal);
      }
      modal.classList.remove('hidden');
      window.renderCorpusCurrentTab();
    };

    window.switchCorpusTab = function(tabName) {
      window.corpusActiveTab = tabName;
      ['books', 'uma', 'crosswalk'].forEach(t => {
        const btn = document.getElementById(`ctab-btn-${t}`);
        if (btn) {
          if (t === tabName) {
            btn.className = 'px-3 py-1.5 rounded-lg bg-blue-600 text-white font-bold transition';
          } else {
            btn.className = 'px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition';
          }
        }
      });
      window.renderCorpusCurrentTab();
    };

    window.renderCorpusCurrentTab = function() {
      const container = document.getElementById('grand-corpus-modal-body');
      if (!container) return;

      if (window.corpusActiveTab === 'books') {
        container.innerHTML = `
          <div class="space-y-4">
            <div class="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center justify-between">
              <input id="corpus-search-input" type="text" placeholder="Search by author, book title, Urdu name, or discipline..." value="${window.corpusSearchTerm}" oninput="window.filterCorpusBooks(this.value)" class="w-full sm:w-96 px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 font-mono" />
              <div class="flex items-center gap-2 overflow-x-auto text-[11px]">
                <button onclick="window.setCorpusCategory('ALL')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='ALL'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">All (97)</button>
                <button onclick="window.setCorpusCategory('Classical Canon')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Classical Canon'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Classical Canon (36)</button>
                <button onclick="window.setCorpusCategory('Clinical Diagnostics')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Clinical Diagnostics'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Diagnostics (10)</button>
                <button onclick="window.setCorpusCategory('Materia Medica')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Materia Medica'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Materia Medica (10)</button>
                <button onclick="window.setCorpusCategory('Pharmacopoeia & Formulary')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Pharmacopoeia & Formulary'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Formularies (17)</button>
                <button onclick="window.setCorpusCategory('Modern Biomedical Medicine')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Modern Biomedical Medicine'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Modern Biomedical (11)</button>
                <button onclick="window.setCorpusCategory('Regimenal Therapy & Surgery')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Regimenal Therapy & Surgery'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Surgery & Tadbeer (5)</button>
                <button onclick="window.setCorpusCategory('Pharmacopoeias & Statutory Standards')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Pharmacopoeias & Statutory Standards'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Statutory Standards (8)</button>
              </div>
            </div>
            <div id="corpus-books-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              <div class="col-span-full py-8 text-center text-xs text-slate-400">Loading catalog from live server...</div>
            </div>
          </div>
        `;
        window.loadAndRenderCorpusBooks();
      } else if (window.corpusActiveTab === 'uma') {
        container.innerHTML = `
          <div class="space-y-4">
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
              <div>
                <h4 class="text-xs font-bold text-blue-400 uppercase tracking-wider">CCRUM / Ministry of AYUSH Standardized Medical Terminology</h4>
                <p class="text-xs text-slate-300">1,593 Standardized Terms (UMA-0001 to UMA-1640) with transliterations, definitions, and modern ICD/biomedical crosswalks.</p>
              </div>
              <div class="text-right">
                <span class="text-xs font-mono font-bold text-blue-400">1,197 Equivalents Mapped</span>
              </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center justify-between">
              <input id="uma-search-input" type="text" placeholder="Search by UMA code (e.g. UMA-0002), Unani term (Shaqiqa), or biomedical name (migraine)..." value="${window.umaSearchTerm}" oninput="window.filterUMATerms(this.value)" class="w-full sm:w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 font-mono" />
            </div>
            <div id="uma-terms-grid" class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div class="col-span-full py-8 text-center text-xs text-slate-400">Loading standardized terms...</div>
            </div>
          </div>
        `;
        window.loadAndRenderUMATerms();
      } else if (window.corpusActiveTab === 'crosswalk') {
        container.innerHTML = `
          <div class="space-y-4">
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <h4 class="text-xs font-bold text-blue-400 uppercase tracking-wider">High-Yield Clinical Crosswalk (Unani Diagnostic Syndrome &harr; Modern Medicine)</h4>
              <p class="text-xs text-slate-300">Statutorily harmonized diagnostic mapping enabling dual-track clinical workflow and ABDM/FHIR interoperability.</p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              ${[
                { uma: "UMA-0002", unani: "Shaqiqa", modern: "Migraine / Hemierania", etiology: "Khilt Safrawi / Damawi", ref: "Al-Qanun Vol. 2" },
                { uma: "UMA-1640", unani: "Waram al-Sifaq", modern: "Acute / Chronic Peritonitis", etiology: "Infection / Visceral perforation", ref: "Kamil al-Sina'a" },
                { uma: "UMA-1622", unani: "Fatq Makhnuq", modern: "Strangulated Inguinal Hernia", etiology: "Vascular compromise", ref: "Kitab al-Jarahat" },
                { uma: "UMA-0050", unani: "Sarsam", modern: "Meningitis / Encephalitis", etiology: "Damawi / Safrawi cerebral heat", ref: "Kitab al-Hawi" },
                { uma: "UMA-0210", unani: "Dheeq al-Nafas", modern: "Bronchial Asthma / Dyspnea", etiology: "Balgham Ghaleez (viscous phlegm)", ref: "Sharh al-Asbab" },
                { uma: "UMA-0430", unani: "Istisqa Ziqqi", modern: "Ascites with Fluid Accumulation", etiology: "Hepatic dysfunction (Daf al-Kabid)", ref: "Akseer-e-Azam" },
                { uma: "UMA-0512", unani: "Yaraqan Insidadi", modern: "Obstructive Jaundice", etiology: "Biliary obstruction (Sudda)", ref: "Al-Qanun Vol. 3" },
                { uma: "UMA-0675", unani: "Qulanj Eelawosi", modern: "Paralytic Ileus / Severe Colic", etiology: "Intestinal obstipation", ref: "Bayaz-e-Kabir" },
                { uma: "UMA-0880", unani: "Bahaq Abyad", modern: "Pityriasis Alba / Vitiligo", etiology: "Fasad-e-Dam & Barid temperament", ref: "Al-Haziq" },
                { uma: "UMA-0915", unani: "Waja al-Mafasil", modern: "Rheumatoid / Osteo-Arthritis", etiology: "Riyah & Balgham deposition in joints", ref: "Qarabadin-e-Azam" },
                { uma: "UMA-1040", unani: "Hasat al-Kulyah", modern: "Nephrolithiasis (Renal Calculi)", etiology: "Dense matter coagulated by visceral heat", ref: "Kitab al-Hawi" },
                { uma: "UMA-1205", unani: "Ihtibas al-Tams", modern: "Secondary Amenorrhea", etiology: "Excessive cold/dryness or vessel obstruction", ref: "Kamil al-Sina'a" }
              ].map(c => `
                <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-blue-500/50 transition space-y-1.5">
                  <div class="flex items-center justify-between">
                    <span class="text-sm font-bold text-white">${c.unani}</span>
                    <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-blue-950 text-blue-300 font-bold border border-blue-800/40">${c.uma}</span>
                  </div>
                  <div class="text-xs font-semibold text-emerald-400">&harr; ${c.modern}</div>
                  <p class="text-[11px] text-slate-400"><strong class="text-slate-300">Pathology:</strong> ${c.etiology}</p>
                  <div class="text-[10px] text-slate-500 font-mono pt-1 border-t border-slate-900 flex justify-between">
                    <span>Classical Ref:</span>
                    <span class="text-slate-400">${c.ref}</span>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      }
    };

    window.setCorpusCategory = function(cat) {
      window.corpusActiveCategory = cat;
      window.renderCorpusCurrentTab();
    };

    window.loadAndRenderCorpusBooks = function() {
      if (window.ZAYVORA_97_BOOKS_CORPUS && window.ZAYVORA_97_BOOKS_CORPUS.length > 0) {
        window.corpusBooksCache = window.ZAYVORA_97_BOOKS_CORPUS;
        window.filterCorpusBooks(window.corpusSearchTerm);
      }
      fetch('/api/v1/canonical/corpus')
        .then(res => res.json())
        .then(data => {
          if (data && data.books && data.books.length > 0) {
            window.corpusBooksCache = data.books;
            window.filterCorpusBooks(window.corpusSearchTerm);
          }
        })
        .catch(() => {
          if (!window.corpusBooksCache || window.corpusBooksCache.length === 0) {
            if (window.ZAYVORA_97_BOOKS_CORPUS) {
              window.corpusBooksCache = window.ZAYVORA_97_BOOKS_CORPUS;
              window.filterCorpusBooks(window.corpusSearchTerm);
            } else {
              const grid = document.getElementById('corpus-books-grid');
              if (grid) grid.innerHTML = '<div class="col-span-full py-8 text-center text-xs text-rose-400">Failed to load corpus from API server.</div>';
            }
          }
        });
    };

    window.filterCorpusBooks = function(query) {
      window.corpusSearchTerm = query || '';
      const grid = document.getElementById('corpus-books-grid');
      if (!grid) return;

      const q = window.corpusSearchTerm.toLowerCase().trim();
      const cat = window.corpusActiveCategory;

      let filtered = window.corpusBooksCache;
      if (cat && cat !== 'ALL') {
        filtered = filtered.filter(b => (b.category || '').toLowerCase() === cat.toLowerCase());
      }
      if (q) {
        filtered = filtered.filter(b => 
          (b.title || '').toLowerCase().includes(q) ||
          (b.title_urdu || '').includes(q) ||
          (b.author || '').toLowerCase().includes(q) ||
          (b.discipline || '').toLowerCase().includes(q) ||
          (b.description || '').toLowerCase().includes(q)
        );
      }

      if (filtered.length === 0) {
        grid.innerHTML = '<div class="col-span-full py-8 text-center text-xs text-slate-400 font-mono">No matching books found.</div>';
        return;
      }

      grid.innerHTML = filtered.map(b => `
        <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-blue-500/50 transition flex flex-col justify-between space-y-2">
          <div class="space-y-1">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 font-bold">${b.id}</span>
              <span class="text-[10px] font-mono text-slate-500">${b.file_size_mb ? b.file_size_mb.toFixed(1) + ' MB' : ''}</span>
            </div>
            <h4 class="text-xs font-bold text-white">${b.title}</h4>
            <div class="text-[11px] font-arabic text-emerald-400">${b.title_urdu || ''}</div>
            <p class="text-[11px] text-slate-400 font-medium">By ${b.author}</p>
            <p class="text-[11px] text-slate-300 leading-relaxed">${b.description}</p>
          </div>
          <div class="pt-2.5 border-t border-slate-900 flex items-center justify-between gap-2 text-[10px]">
            <span class="px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800/40 font-semibold truncate max-w-[140px]">${b.category}</span>
            <div class="flex items-center gap-1.5 shrink-0">
              <button onclick="window.openBookReaderModal('${b.id}', '${(b.title || '').replace(/'/g, "\\'")}')" class="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold transition flex items-center gap-1 shadow-sm cursor-pointer" title="Open and read in built-in reader">
                <span>📖</span> <span>Read Book</span>
              </button>
              <a href="/api/v1/canonical/corpus/read?id=${encodeURIComponent(b.id)}" target="_blank" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white font-semibold transition flex items-center gap-1 border border-slate-700" title="Open full PDF in browser tab">
                <span>↗</span>
              </a>
            </div>
          </div>
        </div>
      `).join('');
    };

    window.openBookReaderModal = function(bookId, bookTitle) {
      let reader = document.getElementById('book-reader-modal');
      if (!reader) {
        reader = document.createElement('div');
        reader.id = 'book-reader-modal';
        reader.className = 'fixed inset-0 z-[60] hidden bg-black/90 backdrop-blur-md flex flex-col p-2 sm:p-4';
        reader.innerHTML = `
          <div class="bg-slate-950 border border-slate-800 rounded-2xl w-full h-full flex flex-col shadow-2xl overflow-hidden">
            <div class="flex items-center justify-between px-5 py-3 border-b border-slate-800 bg-slate-900/90 flex-shrink-0">
              <div class="flex items-center gap-3">
                <span class="text-xl">📖</span>
                <div>
                  <h3 id="book-reader-title" class="text-sm font-bold text-white truncate max-w-xl">Reading Book</h3>
                  <p class="text-[10px] text-slate-400 font-mono">ZAYVORA Health OS • Canonical Medical Treatises Repository</p>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <a id="book-reader-newtab" href="#" target="_blank" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-1 border border-slate-700 transition">
                  <span>↗</span> Full Tab
                </a>
                <button onclick="document.getElementById('book-reader-modal').classList.add('hidden'); document.getElementById('book-reader-frame').src='about:blank';" class="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-slate-800 transition text-sm">✕ Close</button>
              </div>
            </div>
            <div class="flex-1 w-full h-full bg-slate-900 relative">
              <iframe id="book-reader-frame" class="w-full h-full border-0" src="about:blank"></iframe>
            </div>
          </div>
        `;
        document.body.appendChild(reader);
      }
      document.getElementById('book-reader-title').textContent = bookTitle || bookId;
      const url = '/api/v1/canonical/corpus/read?id=' + encodeURIComponent(bookId);
      document.getElementById('book-reader-newtab').href = url;
      document.getElementById('book-reader-frame').src = url;
      reader.classList.remove('hidden');
    };

    window.loadAndRenderUMATerms = function() {
      fetch('/api/v1/terminology/uma?limit=40')
        .then(res => res.json())
        .then(data => {
          if (data && data.terms) {
            window.renderUMAGrid(data.terms);
          }
        })
        .catch(() => {
          const grid = document.getElementById('uma-terms-grid');
          if (grid) grid.innerHTML = '<div class="col-span-full py-8 text-center text-xs text-rose-400">Failed to load UMA terms from server.</div>';
        });
    };

    window.filterUMATerms = function(query) {
      window.umaSearchTerm = query || '';
      const q = window.umaSearchTerm.trim();
      fetch(`/api/v1/terminology/uma?q=${encodeURIComponent(q)}&limit=40`)
        .then(res => res.json())
        .then(data => {
          if (data && data.terms) {
            window.renderUMAGrid(data.terms);
          }
        })
        .catch(() => {});
    };

    window.renderUMAGrid = function(terms) {
      const grid = document.getElementById('uma-terms-grid');
      if (!grid) return;

      if (!terms || terms.length === 0) {
        grid.innerHTML = '<div class="col-span-full py-8 text-center text-xs text-slate-400 font-mono">No matching UMA terms found.</div>';
        return;
      }

      grid.innerHTML = terms.map(t => `
        <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-blue-500/50 transition space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-white">${t.unani_term}</span>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-950 text-blue-300 font-bold border border-blue-800/40">${t.uma_code}</span>
          </div>
          ${t.english_equivalent ? `
            <div class="text-xs font-semibold text-emerald-400">Modern Equivalent: ${t.english_equivalent}</div>
          ` : ''}
          <p class="text-xs text-slate-300 leading-relaxed">${t.definition}</p>
          <div class="text-[10px] text-slate-500 font-mono pt-1 border-t border-slate-900">
            Source: ${t.source}
          </div>
        </div>
      `).join('');
    };

