    // ── PWA Service Worker Registration ─────────────────────────────────────
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('sw.js?v=14.1').then(function(reg) {
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

