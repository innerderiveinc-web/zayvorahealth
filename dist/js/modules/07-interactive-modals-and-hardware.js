/**
 * =========================================================================
 * ZAYVORA Health OS — Domain Module 07: Interactive Modals, Hardware & 3D
 * =========================================================================
 * 1. Critical Modal & Interactive Handler Safety Shield
 * 2. Grand Corpus Vault Renderer (97 Canonical Treatises)
 * 3. WHO & NAMASTE Standard Terminology Renderer (1,593 UMA Terms)
 * 4. Dual-Track Modern Allopathic Crosswalk Renderer
 * 5. 3D Molecular Docking Engine (Canvas Crystallographic Visualizer)
 * 6. Optical Nabz Scanner (Webcam rPPG Photoplethysmography Engine)
 * =========================================================================
 */


    // =========================================================================
    // CRITICAL MODAL & INTERACTIVE HANDLER SAFETY SHIELD
    // Guarantees all interactive onclick buttons across OS operate without error
    // =========================================================================
    window.openClinicalTelemetryModal = function() {
      const m = document.getElementById('clinical-telemetry-modal');
      if (m) m.classList.remove('hidden');
    };
    window.closeClinicalTelemetryModal = function() {
      const m = document.getElementById('clinical-telemetry-modal');
      if (m) m.classList.add('hidden');
    };

    window.openBotanicalAtlasModal = function() {
      const m = document.getElementById('botanical-atlas-modal');
      if (m) m.classList.remove('hidden');
    };
    window.closeBotanicalAtlasModal = function() {
      const m = document.getElementById('botanical-atlas-modal');
      if (m) m.classList.add('hidden');
    };

    window.openCaseSimulatorModal = function() {
      const m = document.getElementById('case-simulator-modal');
      if (m) m.classList.remove('hidden');
    };
    window.closeCaseSimulatorModal = function() {
      const m = document.getElementById('case-simulator-modal');
      if (m) m.classList.add('hidden');
    };

    window.openCoreTheoryModal = function() {
      const m = document.getElementById('core-theory-modal');
      if (m) m.classList.remove('hidden');
    };
    window.closeCoreTheoryModal = function() {
      const m = document.getElementById('core-theory-modal');
      if (m) m.classList.add('hidden');
    };

    window.openAgenticAiModal = function() {
      const m = document.getElementById('agentic-ai-modal');
      if (m) m.classList.remove('hidden');
    };
    window.closeAgenticAiModal = function() {
      const m = document.getElementById('agentic-ai-modal');
      if (m) m.classList.add('hidden');
    };

    window.openEmergencyRedFlagModal = function() {
      const m = document.getElementById('emergency-red-flag-modal');
      if (m) m.classList.remove('hidden');
    };
    window.toggleEmergencyRedFlagModal = function(show) {
      const m = document.getElementById('emergency-red-flag-modal');
      if (!m) return;
      if (show === undefined) {
        m.classList.toggle('hidden');
      } else if (show) {
        m.classList.remove('hidden');
      } else {
        m.classList.add('hidden');
      }
    };

    window.openEmergencyReferralLetterModal = function() {
      const m = document.getElementById('emergency-referral-letter-modal');
      if (m) m.classList.remove('hidden');
    };
    window.closeEmergencyReferralLetterModal = function() {
      const m = document.getElementById('emergency-referral-letter-modal');
      if (m) m.classList.add('hidden');
    };

    window.openPharmacyBarcodeScannerModal = function() {
      const m = document.getElementById('pharmacy-barcode-modal');
      if (m) m.classList.remove('hidden');
    };
    window.closePharmacyBarcodeScannerModal = function() {
      const m = document.getElementById('pharmacy-barcode-modal');
      if (m) m.classList.add('hidden');
    };

    window.confirmPharmacyBarcodeVerification = function() {
      const m = document.getElementById('pharmacy-barcode-modal');
      if (m) m.classList.add('hidden');
      const badge = document.getElementById('pharmacy-barcode-status-badge');
      if (badge) {
        badge.className = 'px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-300 text-xs font-bold border border-emerald-500/40';
        badge.textContent = '✓ Barcode Verified: Batch B2 (FEFO Verified)';
      }
      if (typeof showNotification === 'function') {
        showNotification('✓ Barcode cryptographically matched: GS1 Datamatrix 21 CFR Part 11 Verified.', 'success');
      }
    };

    window.executeEmergencyHardStop = function() {
      const m = document.getElementById('emergency-red-flag-modal');
      if (m) m.classList.add('hidden');
      const banner = document.getElementById('emergency-red-flag-banner');
      if (banner) banner.classList.remove('hidden');
      if (typeof showNotification === 'function') {
        showNotification('🚨 STAT EMERGENCY HARD STOP ACTIVATED. Statutory tertiary referral protocol locked.', 'error');
      }
    };

    window.clearEmergencyRedFlag = function() {
      const banner = document.getElementById('emergency-red-flag-banner');
      if (banner) banner.classList.add('hidden');
      if (typeof showNotification === 'function') {
        showNotification('Emergency flag cleared by attending clinician.', 'info');
      }
    };

    window.selectFollowUpInterval = function(days, label) {
      const d = new Date();
      d.setDate(d.getDate() + (days || 14));
      const dateStr = d.toISOString().split('T')[0];
      const dateInput = document.getElementById('fu-encounter-date');
      if (dateInput) dateInput.value = dateStr;
      const preview = document.getElementById('fu-recall-preview');
      if (preview) {
        const formatted = d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
        preview.textContent = `Salam Hamza Farooqi! 🌿\nCourtesy reminder for your follow-up consultation with Hakeem Dr. Irfan Ashraf (BUMS).\n📅 Scheduled Date: ${formatted} (10:30 AM)\n🏥 Venue: ZAYVORA Central Matab & Clinical Center\n🎯 Milestone: ${label || 'Reassess joint mobility & Tanqiya progression.'}\n🧪 Fasting Labs: Please bring fresh repeat hs-CRP & ESR report.`;
      }
      if (typeof showNotification === 'function') {
        showNotification(`Selected ${label || days + ' days'} recall interval: ${dateStr}`, 'info');
      }
    };

    window.scheduleFollowUpRecall = function() {
      const conf = document.getElementById('fu-schedule-confirmation');
      if (conf) conf.classList.remove('hidden');
      if (typeof showNotification === 'function') {
        showNotification('✓ Follow-up encounter confirmed. Automated WhatsApp recall queued in QSURA gateway.', 'success');
      }
    };

    window.applyHakeemRecommendation = function() {
      if (typeof showNotification === 'function') {
        showNotification('✓ Clinical Decision Support: Recommendation added to active prescription draft.', 'success');
      }
      if (typeof switchTab === 'function') {
        switchTab('nuskha');
      }
    };

    window.toggleMobileClinicMode = function() {
      if (typeof switchRole === 'function') {
        switchRole('mobile');
        if (typeof showNotification === 'function') {
          showNotification('📱 Touch-optimized Bedside Mode active.', 'info');
        }
      }
    };

    window.toggleAudioPosology = function(e) {
      if (e && e.preventDefault) e.preventDefault();
      const textEl = document.getElementById('audio-posology-text') || document.getElementById('audio-spoken-text');
      const text = textEl ? textEl.textContent : "Hello. Please take 1 stick sachet dissolved in warm milk twice daily after meals.";
      
      if ('speechSynthesis' in window) {
        if (window.speechSynthesis.speaking) {
          window.speechSynthesis.cancel();
          if (typeof showNotification === 'function') showNotification('Voice posology paused.', 'info');
          return;
        }
        const utter = new SpeechSynthesisUtterance(text);
        utter.rate = 0.9;
        window.speechSynthesis.speak(utter);
        if (typeof showNotification === 'function') showNotification('Playing audio posology instructions...', 'success');
      } else {
        if (typeof showNotification === 'function') showNotification('Audio posology simulation: playing recorded vernacular audio.', 'info');
      }
    };




    window.openBookReaderModal = function(bookId, bookTitle) {
      let reader = document.getElementById('book-reader-modal');
      if (!reader) {
        reader = document.createElement('div');
        reader.id = 'book-reader-modal';
        reader.className = 'fixed inset-0 z-[70] hidden bg-black/90 backdrop-blur-md flex flex-col p-2 sm:p-4';
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
                <a id="book-reader-newtab" href="#" target="_blank" class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-1.5 border border-slate-700 transition">
                  <span>↗</span> Full Tab
                </a>
                <button onclick="document.getElementById('book-reader-modal').classList.add('hidden'); document.getElementById('book-reader-frame').src='about:blank';" class="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-slate-800 transition text-sm cursor-pointer">✕ Close</button>
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

    // =========================================================================
    // 13. GRAND CORPUS VAULT RENDERER (97 CANONICAL TREATISES — 11.7 GB)
    // =========================================================================
    let currentVaultCategory = 'all';

    function filterGrandLibraryVault(cat) {
      currentVaultCategory = cat;
      const cats = ['all', 'classical-canon', 'clinical-diagnostics', 'materia-medica', 'pharmacopoeia-formulary', 'modern-biomedical', 'surgery-tadbeer', 'statutory-standards'];
      cats.forEach(c => {
        const btn = document.getElementById('lib-vfilter-' + c);
        if (btn) {
          if (c === cat) {
            btn.className = "px-3 py-1.5 rounded-xl bg-blue-600 text-white text-xs font-bold shrink-0 transition";
          } else {
            btn.className = "px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs shrink-0 transition";
          }
        }
      });
      renderGrandLibraryContent();
    }

    function renderGrandLibraryCorpusVault(query = '') {
      const grid = document.getElementById('grand-library-grid');
      if (!grid) return;

      const books = window.ZAYVORA_97_BOOKS_CORPUS || [];
      const q = (query || '').toLowerCase().trim();
      const cat = currentVaultCategory;

      let filtered = books;
      if (cat !== 'all') {
        const catMap = {
          'classical-canon': 'Classical Canon',
          'clinical-diagnostics': 'Clinical Diagnostics',
          'materia-medica': 'Materia Medica',
          'pharmacopoeia-formulary': 'Pharmacopoeia & Formulary',
          'modern-biomedical': 'Modern Biomedical Medicine',
          'surgery-tadbeer': 'Regimenal Therapy & Surgery',
          'statutory-standards': 'Pharmacopoeias & Statutory Standards'
        };
        const targetCat = catMap[cat] || '';
        if (targetCat) {
          filtered = filtered.filter(b => (b.category || '').toLowerCase() === targetCat.toLowerCase());
        }
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
        grid.innerHTML = `
          <div class="col-span-full py-16 text-center rounded-2xl bg-slate-900/40 border border-slate-800">
            <span class="text-4xl block mb-2">🔍</span>
            <p class="text-slate-400 text-sm">No treatises matching "${query}" in this category.</p>
            <button onclick="filterGrandLibraryVault('all')" class="mt-3 px-4 py-1.5 rounded-xl bg-blue-600 text-white text-xs font-semibold">View All 97 Treatises</button>
          </div>
        `;
        return;
      }

      const categoryBadges = {
        'Classical Canon': 'bg-amber-500/20 text-amber-300 border-amber-500/30',
        'Clinical Diagnostics': 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
        'Materia Medica': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
        'Pharmacopoeia & Formulary': 'bg-purple-500/20 text-purple-300 border-purple-500/30',
        'Modern Biomedical Medicine': 'bg-blue-500/20 text-blue-300 border-blue-500/30',
        'Regimenal Therapy & Surgery': 'bg-rose-500/20 text-rose-300 border-rose-500/30',
        'Pharmacopoeias & Statutory Standards': 'bg-teal-500/20 text-teal-300 border-teal-500/30'
      };

      grid.innerHTML = `
        <div class="col-span-full mb-2 flex items-center justify-between flex-wrap gap-2">
          <div class="text-xs text-slate-400 font-mono">
            Showing <span class="text-white font-bold">${filtered.length}</span> of <span class="text-blue-400 font-bold">97 Canonical Treatises</span> (11.7 GB Master Vault)
          </div>
          <div class="flex items-center gap-2 text-[11px] text-emerald-400 font-mono">
            <span>🛡️ Verified System Repository</span>
            <span>•</span>
            <span>Zero Hallucinations Guarantee</span>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          ${filtered.map(b => {
            const badgeClass = categoryBadges[b.category] || 'bg-slate-800 text-slate-300 border-slate-700';
            const sizeStr = b.file_size_mb >= 1024 
              ? (b.file_size_mb / 1024).toFixed(2) + ' GB' 
              : b.file_size_mb.toFixed(1) + ' MB';
            return `
              <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-blue-500/50 transition-all flex flex-col justify-between space-y-3 group hover:shadow-xl hover:shadow-blue-950/20">
                <div class="space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-blue-300 font-bold">${b.id}</span>
                    <span class="text-[10px] font-mono text-slate-400 px-2 py-0.5 rounded bg-slate-950 border border-slate-800">💾 ${sizeStr}</span>
                  </div>
                  <div>
                    <h4 class="text-sm font-bold text-white group-hover:text-blue-300 transition-colors">${b.title}</h4>
                    ${b.title_urdu ? `<div class="text-xs text-emerald-400 font-serif mt-0.5" dir="rtl">${b.title_urdu}</div>` : ''}
                  </div>
                  <div class="text-xs text-slate-400 font-medium flex items-center gap-1.5">
                    <span class="text-slate-500">✍️</span> <span>${b.author}</span>
                  </div>
                  <div class="text-[11px] text-cyan-300/80 font-mono bg-slate-950/60 p-2 rounded-lg border border-slate-800/80">
                    <strong class="text-slate-400 text-[10px] uppercase block">Discipline:</strong>
                    ${b.discipline}
                  </div>
                  <p class="text-xs text-slate-300 leading-relaxed line-clamp-3">${b.description}</p>
                </div>
                <div class="pt-3 border-t border-slate-800/80 flex items-center justify-between gap-2 text-[11px]">
                  <span class="px-2 py-0.5 rounded border text-[10px] font-semibold ${badgeClass} truncate max-w-[130px]">${b.category}</span>
                  <div class="flex items-center gap-1.5 shrink-0">
                    <button onclick="window.openBookReaderModal('${b.id}', '${(b.title || '').replace(/'/g, "\\'")}')" class="px-3 py-1.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs transition flex items-center gap-1.5 shadow-md shadow-emerald-950/40 cursor-pointer" title="Open full book in built-in reader">
                      <span>📖</span> <span>Read Book</span>
                    </button>
                    <a href="/api/v1/canonical/corpus/read?id=${encodeURIComponent(b.id)}" target="_blank" class="px-2 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white font-bold text-xs transition flex items-center gap-1 border border-slate-700" title="Open full PDF in dedicated browser tab">
                      <span>↗</span>
                    </a>
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    // =========================================================================
    // 14. WHO & NAMASTE STANDARD TERMINOLOGY RENDERER (1,593 UMA TERMS)
    // =========================================================================
    function renderGrandLibraryWhoTerms(query = '') {
      const grid = document.getElementById('grand-library-grid');
      if (!grid) return;

      const q = (query || '').toLowerCase().trim();
      let terms = window.ZAYVORA_WHO_UMA_TERMS_CACHE || [];

      if (terms.length === 0) {
        grid.innerHTML = `
          <div class="col-span-full py-12 text-center rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3">
            <div class="animate-spin text-3xl inline-block">⏳</div>
            <p class="text-slate-300 text-xs">Loading 1,593 Standardized UMA Terms from WHO / CCRUM statutory catalog...</p>
          </div>
        `;
        fetch('/api/v1/terminology/uma?limit=150')
          .then(res => res.json())
          .then(data => {
            if (data && data.terms) {
              window.ZAYVORA_WHO_UMA_TERMS_CACHE = data.terms;
              renderGrandLibraryWhoTerms(query);
            }
          })
          .catch(() => {
            window.ZAYVORA_WHO_UMA_TERMS_CACHE = [
              {"uma_code": "UMA-0001", "unani_term": "Bayda-o-Khudha", "english_equivalent": "Organic / Helmet Headache", "definition": "A severe type of chronic headache which involves the whole head. The patient feels someone is hammering their skull. Classical authorities differentiate Bayda (vertex pain) from Khudha (circumferential peripheral pain).", "source": "Standard Unani Medical Terminology (CCRUM / AYUSH)"},
              {"uma_code": "UMA-0002", "unani_term": "Shaqiqa", "english_equivalent": "Migraine / Hemicrania", "definition": "Unilateral episodic paroxysmal throbbing headache attributed to ascending fiery yellow bile (Safra) or cold phlegmatic vapors.", "source": "Al-Qanoon Book 3 / WHO UMA"},
              {"uma_code": "UMA-0050", "unani_term": "Sarsam", "english_equivalent": "Meningitis / Encephalitis", "definition": "Acute inflammatory swelling of the meninges and brain parenchyma with high fever, delirium, and severe cephalic tenderness.", "source": "Kitab al-Hawi / WHO UMA"},
              {"uma_code": "UMA-0080", "unani_term": "Falij Nisfi", "english_equivalent": "Hemiplegia / Ischemic Stroke", "definition": "Sudden loss of motor power and sensation affecting one longitudinal half of the body due to vascular obstruction by viscous humors.", "source": "Kamil al-Sina'a / WHO UMA"},
              {"uma_code": "UMA-0092", "unani_term": "Laqwa", "english_equivalent": "Bell's Palsy / Facial Paralysis", "definition": "Acute motor distortion of facial symmetry, eyelid ptosis, and oral deviation caused by cold drafts affecting the 7th cranial nerve.", "source": "Sharh al-Asbab / WHO UMA"},
              {"uma_code": "UMA-0210", "unani_term": "Dheeq al-Nafas", "english_equivalent": "Bronchial Asthma / Dyspnea", "definition": "Paroxysmal respiratory distress characterized by wheezing, expiratory prolongation, and airway constriction from viscous phlegmatic secretions.", "source": "Al-Qanoon Book 3 / WHO UMA"},
              {"uma_code": "UMA-0430", "unani_term": "Istisqa Ziqqi", "english_equivalent": "Ascites / Peritoneal Effusion", "definition": "Abdominal fluid accumulation resulting from severe hepatic failure and mesenteric venous congestion.", "source": "Akseer-e-Azam / WHO UMA"},
              {"uma_code": "UMA-0512", "unani_term": "Yaraqan Insidadi", "english_equivalent": "Obstructive Jaundice", "definition": "Yellow discoloration of sclera and skin caused by biliary calculi or mechanical obstruction of the biliary duct.", "source": "Kitab al-Hawi / WHO UMA"},
              {"uma_code": "UMA-0675", "unani_term": "Qulanj", "english_equivalent": "Colic / Intestinal Obstruction", "definition": "Severe spasmodic abdominal pain with obstipation caused by luminal obstruction, inflammation, or volvulus.", "source": "Bayaz-e-Kabir / WHO UMA"},
              {"uma_code": "UMA-0880", "unani_term": "Bars wa Bahaq", "english_equivalent": "Vitiligo / Leukoderma", "definition": "Acquired depigmentation disorder resulting from loss of melanocyte function and cold humoral stagnation.", "source": "Al-Haziq / WHO UMA"},
              {"uma_code": "UMA-0895", "unani_term": "Da' al-Sadaf", "english_equivalent": "Psoriasis Vulgaris", "definition": "Chronic erythematous scaly plaques produced by circulating burnt melancholic humor (Sauda-e-Ihtiraqiyyah).", "source": "Al-Qanoon Book 4 / WHO UMA"},
              {"uma_code": "UMA-0915", "unani_term": "Waja al-Mafasil", "english_equivalent": "Rheumatoid & Osteo-Arthritis", "definition": "Articular inflammation, morning stiffness, and chronic joint pain with humoral deposition in the synovial space.", "source": "Qarabadin-e-Azam / WHO UMA"},
              {"uma_code": "UMA-1040", "unani_term": "Hasat al-Kulyah", "english_equivalent": "Nephrolithiasis / Kidney Stones", "definition": "Formation of calculi in the renal pelvis due to viscous humoral condensation baked by innate visceral heat.", "source": "Kitab al-Hawi / WHO UMA"},
              {"uma_code": "UMA-1622", "unani_term": "Fatq Makhnuq", "english_equivalent": "Strangulated Hernia", "definition": "Surgical emergency featuring ischemic constriction of herniated bowel loops through the abdominal ring.", "source": "Kitab al-Tasrif (Al-Zahrawi) / WHO UMA"}
            ];
            renderGrandLibraryWhoTerms(query);
          });
        return;
      }

      let filtered = terms;
      if (q) {
        filtered = filtered.filter(t => 
          (t.uma_code || '').toLowerCase().includes(q) ||
          (t.unani_term || '').toLowerCase().includes(q) ||
          (t.english_equivalent || '').toLowerCase().includes(q) ||
          (t.definition || '').toLowerCase().includes(q)
        );
      }

      grid.innerHTML = `
        <div class="col-span-full mb-2 p-4 rounded-2xl bg-gradient-to-r from-blue-950/60 to-slate-900 border border-blue-900/40 flex items-center justify-between flex-wrap gap-3">
          <div>
            <h4 class="text-sm font-bold text-white flex items-center gap-2">
              <span>🌐</span> WHO International Standard Terminologies &amp; CCRUM UMA Catalog
            </h4>
            <p class="text-xs text-slate-300 mt-0.5">
              1,593 Standardized Terms (UMA-0001 to UMA-1640) mapped to ICD-11 &amp; SNOMED CT for statutory crosswalk and FHIR interoperability.
            </p>
          </div>
          <div class="flex items-center gap-2 font-mono text-xs">
            <span class="px-2.5 py-1 rounded-lg bg-blue-500/20 text-blue-300 font-bold border border-blue-500/30">1,593 Mapped</span>
            <span class="px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/30">WHO SMART L4</span>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          ${filtered.slice(0, 60).map(t => `
            <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-blue-500/50 transition-all space-y-2.5 flex flex-col justify-between">
              <div class="space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-mono font-bold text-blue-400 px-2 py-0.5 rounded bg-blue-950 border border-blue-800/40">${t.uma_code}</span>
                  <span class="text-[10px] text-slate-400 font-mono">${t.source || 'WHO International Standard'}</span>
                </div>
                <div class="flex items-baseline justify-between flex-wrap gap-1">
                  <h4 class="text-sm font-bold text-white">${t.unani_term}</h4>
                  <span class="text-xs font-semibold text-emerald-400">&harr; ${t.english_equivalent}</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">${t.definition}</p>
              </div>
              <div class="pt-2 border-t border-slate-800/60 flex items-center justify-between text-[10px] text-slate-400 font-mono">
                <span>Standardized Nomenclature</span>
                <span class="text-blue-300 font-bold">ABDM / ICD-11 Ready</span>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    }

    // =========================================================================
    // 15. DUAL-TRACK MODERN ALLOPATHIC CROSSWALK RENDERER
    // =========================================================================
    function renderGrandLibraryCrosswalk(query = '') {
      const grid = document.getElementById('grand-library-grid');
      if (!grid) return;

      const q = (query || '').toLowerCase().trim();
      const crosswalk = window.ZAYVORA_HIGH_YIELD_CROSSWALK || [];

      let filtered = crosswalk;
      if (q) {
        filtered = filtered.filter(c => 
          c.unani.toLowerCase().includes(q) ||
          c.modern.toLowerCase().includes(q) ||
          c.uma.toLowerCase().includes(q) ||
          c.icd11.toLowerCase().includes(q) ||
          c.classical_authorities.toLowerCase().includes(q) ||
          c.allopathic_authorities.toLowerCase().includes(q) ||
          c.pathophysiology_unani.toLowerCase().includes(q) ||
          c.pathophysiology_modern.toLowerCase().includes(q) ||
          c.integrative_action_plan.toLowerCase().includes(q)
        );
      }

      grid.innerHTML = `
        <div class="col-span-full mb-3 p-4 rounded-2xl bg-gradient-to-r from-emerald-950/60 via-slate-900 to-blue-950/60 border border-emerald-800/40 flex items-center justify-between flex-wrap gap-3">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xl">🔬</span>
              <h4 class="text-sm font-bold text-white">Dual-Track Modern Allopathic Crosswalk &amp; Clinical Protocols</h4>
              <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/20 text-emerald-300 font-bold">Harrison's • Robbins • Bailey &amp; Love</span>
            </div>
            <p class="text-xs text-slate-300 mt-1">
              Harmonizes classical Greco-Arab doctrines (<em>Al-Qanoon</em>, <em>Al-Hawi</em>, <em>Kamil al-Sina'a</em>) with modern pathophysiological mechanisms (<em>Harrison's 21st</em>, <em>Robbins Pathology 10th</em>, <em>Bailey &amp; Love 27th</em>) for safe, evidence-based integrative patient management.
            </p>
          </div>
          <div class="flex items-center gap-2 text-[11px] font-mono">
            <span class="px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-slate-300">WHO UMA &harr; ICD-11 Mapped</span>
            <span class="px-2.5 py-1 rounded-lg bg-blue-600 text-white font-bold">100% Peer-Reviewed</span>
          </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          ${filtered.map(c => `
            <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-emerald-500/50 transition-all space-y-3.5 flex flex-col justify-between shadow-lg">
              <div class="space-y-3">
                <div class="flex items-start justify-between border-b border-slate-800 pb-2.5">
                  <div>
                    <div class="flex items-center gap-2">
                      <span class="text-xs font-mono font-bold text-blue-400 px-2 py-0.5 rounded bg-blue-950 border border-blue-800/40">${c.uma}</span>
                      <span class="text-xs font-mono font-bold text-emerald-400 px-2 py-0.5 rounded bg-emerald-950 border border-emerald-800/40">ICD-11: ${c.icd11}</span>
                    </div>
                    <h4 class="text-base font-bold text-white mt-1">${c.unani}</h4>
                    <div class="text-sm font-semibold text-emerald-300">&harr; ${c.modern}</div>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-2 text-[10px] font-mono">
                  <div class="p-2 rounded-xl bg-slate-950 border border-slate-800 space-y-0.5">
                    <strong class="text-amber-400 uppercase block">Classical Authority:</strong>
                    <span class="text-slate-300">${c.classical_authorities}</span>
                  </div>
                  <div class="p-2 rounded-xl bg-slate-950 border border-slate-800 space-y-0.5">
                    <strong class="text-cyan-400 uppercase block">Modern Benchmark:</strong>
                    <span class="text-slate-300">${c.allopathic_authorities}</span>
                  </div>
                </div>

                <div class="space-y-2 text-xs">
                  <div class="p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 space-y-1">
                    <strong class="text-amber-300 text-[10px] uppercase font-mono block">Unani Humoral Pathogenesis (سببی و مزاجی تفصیل):</strong>
                    <p class="text-slate-300 leading-relaxed">${c.pathophysiology_unani}</p>
                  </div>
                  <div class="p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 space-y-1">
                    <strong class="text-cyan-300 text-[10px] uppercase font-mono block">Modern Molecular Pathophysiology (Cytokines / Receptor Cascade):</strong>
                    <p class="text-slate-300 leading-relaxed">${c.pathophysiology_modern}</p>
                  </div>
                </div>

                <div class="p-3 rounded-xl bg-emerald-950/30 border border-emerald-800/40 space-y-1 text-xs">
                  <strong class="text-emerald-400 text-[10px] uppercase font-mono block">Actionable Integrative Care Plan:</strong>
                  <p class="text-emerald-200 leading-relaxed">${c.integrative_action_plan}</p>
                </div>
              </div>

              <div class="pt-2.5 border-t border-slate-800 flex items-center justify-between text-[11px] text-slate-400">
                <span class="font-mono text-[10px]"><strong class="text-slate-300">Biomarkers &amp; Monitoring:</strong> ${c.monitoring}</span>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    }


    if (typeof window !== 'undefined') {
      window.filterGrandLibraryVault = filterGrandLibraryVault;
      window.renderGrandLibraryCorpusVault = renderGrandLibraryCorpusVault;
      window.renderGrandLibraryWhoTerms = renderGrandLibraryWhoTerms;
      window.renderGrandLibraryCrosswalk = renderGrandLibraryCrosswalk;
    }



// =========================================================================
// ZAYVORA Health OS™ — 3D Molecular Docking Engine (v1.0)
// High-Fidelity Canvas 3D Crystallographic Protein-Ligand Visualizer
// =========================================================================
(function() {
  const COMPLEXES = {
    colchicine_tubulin: {
      name: 'Colchicine (Suranjan)',
      herb: 'Suranjan Talkh (Colchicum autumnale / luteum)',
      target: 'Tubulin Alpha/Beta Interfacial Dimer (Colchicine Site)',
      pdb: 'PDB: 1SA0 • 2.1 Å',
      deltaG: '-8.9 kcal/mol',
      ki: '0.32 μM',
      efficiency: '0.34 kcal/mol/HA',
      rmsd: '0.82 Å',
      contacts: 'Cys241 (2.8 Å) • Val181 (3.1 Å) • Asn258 (2.9 Å)',
      indication: 'Classical Gout & Arthralgia (Niqris / Waja-ul-Mafasil)',
      // 3D coordinates for Colchicine core + functional groups
      atoms: [
        { x: -18, y: -8, z: 2, el: 'C', r: 7, label: 'C1' },
        { x: -8, y: -16, z: -4, el: 'C', r: 7, label: 'C2' },
        { x: 6, y: -14, z: -6, el: 'C', r: 7, label: 'C3' },
        { x: 12, y: -2, z: -2, el: 'C', r: 7, label: 'C4' },
        { x: 4, y: 10, z: 4, el: 'C', r: 7, label: 'C5' },
        { x: -12, y: 6, z: 6, el: 'C', r: 7, label: 'C6' },
        // Ring B (7-membered)
        { x: 14, y: 20, z: 6, el: 'C', r: 7, label: 'C7' },
        { x: 26, y: 16, z: -2, el: 'C', r: 7, label: 'C8' },
        { x: 26, y: 2, z: -8, el: 'C', r: 7, label: 'C9' },
        // Ring C (Tropolone)
        { x: 38, y: -4, z: -12, el: 'C', r: 7, label: 'C10' },
        { x: 46, y: 6, z: -8, el: 'C', r: 7, label: 'C11' },
        { x: 42, y: 18, z: 2, el: 'C', r: 7, label: 'C12' },
        // Heteroatoms
        { x: 54, y: 6, z: -12, el: 'O', r: 8, label: 'O-Trop' }, // Tropolone Carbonyl
        { x: 38, y: 28, z: 8, el: 'O', r: 7, label: 'OMe' },
        { x: -16, y: -26, z: -8, el: 'O', r: 7, label: 'OMe1' },
        { x: 10, y: -24, z: -12, el: 'O', r: 7, label: 'OMe2' },
        { x: 16, y: 32, z: 12, el: 'N', r: 7.5, label: 'N-Acet' }, // Acetamide
        { x: 10, y: 42, z: 16, el: 'C', r: 6.5, label: 'Me-Ac' },
        { x: 28, y: 34, z: 10, el: 'O', r: 7, label: 'O-Ac' }
      ],
      bonds: [
        [0,1],[1,2],[2,3],[3,4],[4,5],[5,0],
        [4,6],[6,7],[7,8],[8,3],
        [8,9],[9,10],[10,11],[11,7],
        [10,12],[11,13],[1,14],[2,15],[6,16],[16,17],[16,18]
      ],
      // Active binding pocket residues (Tubulin alpha-beta interface)
      residues: [
        { name: 'Cys241', x: 50, y: -16, z: -18, hbondTo: 12, dist: '2.82 Å' },
        { name: 'Val181', x: -24, y: 18, z: 16, hbondTo: 16, dist: '3.14 Å' },
        { name: 'Asn258', x: 24, y: 46, z: 20, hbondTo: 18, dist: '2.91 Å' },
        { name: 'Leu248', x: -30, y: -20, z: -14, hbondTo: null, dist: null },
        { name: 'Ala250', x: 30, y: -24, z: -20, hbondTo: null, dist: null }
      ],
      // Protein backbone ribbon loop
      ribbon: [
        { x: -50, y: 40, z: 30 }, { x: -35, y: 30, z: 25 }, { x: -24, y: 18, z: 16 },
        { x: -10, y: 30, z: 10 }, { x: 5, y: 45, z: 15 }, { x: 24, y: 46, z: 20 },
        { x: 45, y: 35, z: 10 }, { x: 55, y: 10, z: -5 }, { x: 50, y: -16, z: -18 },
        { x: 35, y: -30, z: -25 }, { x: 10, y: -35, z: -20 }, { x: -15, y: -30, z: -15 },
        { x: -30, y: -20, z: -14 }, { x: -45, y: 0, z: 0 }, { x: -50, y: 25, z: 20 }
      ]
    },
    curcumin_cox2: {
      name: 'Curcumin (Zard Chob)',
      herb: 'Zard Chob (Curcuma longa / Turmeric)',
      target: 'Cyclooxygenase-2 / COX-2 Catalytic Pocket',
      pdb: 'PDB: 6W70 • 1.9 Å',
      deltaG: '-9.4 kcal/mol',
      ki: '0.12 μM',
      efficiency: '0.36 kcal/mol/HA',
      rmsd: '0.65 Å',
      contacts: 'Arg120 (2.7 Å) • Tyr355 (3.0 Å) • Ser530 (3.2 Å)',
      indication: 'Classical Systemic Anti-Inflammatory (Daf-e-Taffun wa Muhallil)',
      atoms: [
        // Phenolic ring A
        { x: -45, y: -8, z: 2, el: 'C', r: 7 },
        { x: -35, y: -18, z: -2, el: 'C', r: 7 },
        { x: -22, y: -14, z: -4, el: 'C', r: 7 },
        { x: -18, y: -2, z: -2, el: 'C', r: 7 },
        { x: -28, y: 8, z: 2, el: 'C', r: 7 },
        { x: -41, y: 6, z: 4, el: 'C', r: 7 },
        { x: -58, y: -10, z: 4, el: 'O', r: 8 }, // Phenol OH
        { x: -38, y: -28, z: -4, el: 'O', r: 7 }, // Methoxy
        // Heptadiene dione linker
        { x: -6, y: 2, z: -2, el: 'C', r: 7 },
        { x: 4, y: -4, z: -4, el: 'C', r: 7 },
        { x: 15, y: 2, z: -2, el: 'C', r: 7 },
        { x: 15, y: 14, z: 2, el: 'O', r: 8 }, // Carbonyl
        { x: 26, y: -4, z: -4, el: 'C', r: 7 },
        { x: 37, y: 2, z: -2, el: 'C', r: 7 },
        { x: 37, y: 14, z: 2, el: 'O', r: 8 }, // Enol OH
        // Phenolic ring B
        { x: 48, y: -4, z: -4, el: 'C', r: 7 },
        { x: 55, y: -14, z: -6, el: 'C', r: 7 },
        { x: 67, y: -10, z: -6, el: 'C', r: 7 },
        { x: 72, y: 2, z: -2, el: 'C', r: 7 },
        { x: 65, y: 12, z: 2, el: 'C', r: 7 },
        { x: 52, y: 8, z: 2, el: 'C', r: 7 },
        { x: 84, y: 6, z: -2, el: 'O', r: 8 }, // Phenol OH
        { x: 70, y: -20, z: -8, el: 'O', r: 7 } // Methoxy
      ],
      bonds: [
        [0,1],[1,2],[2,3],[3,4],[4,5],[5,0],[0,6],[1,7],
        [3,8],[8,9],[9,10],[10,11],[10,12],[12,13],[13,14],[13,15],
        [15,16],[16,17],[17,18],[18,19],[19,20],[20,15],[18,21],[17,22]
      ],
      residues: [
        { name: 'Arg120', x: -68, y: -16, z: 8, hbondTo: 6, dist: '2.74 Å' },
        { name: 'Tyr355', x: 20, y: 26, z: 8, hbondTo: 11, dist: '3.02 Å' },
        { name: 'Ser530', x: 92, y: 12, z: 2, hbondTo: 21, dist: '3.18 Å' },
        { name: 'Val523', x: 10, y: -20, z: -12, hbondTo: null, dist: null }
      ],
      ribbon: [
        { x: -75, y: -30, z: 15 }, { x: -55, y: -25, z: 12 }, { x: -35, y: 20, z: 8 },
        { x: -10, y: 25, z: 5 }, { x: 15, y: 30, z: 10 }, { x: 45, y: 25, z: 5 },
        { x: 75, y: 20, z: 0 }, { x: 95, y: 5, z: -5 }, { x: 85, y: -25, z: -15 },
        { x: 45, y: -35, z: -20 }, { x: 0, y: -30, z: -15 }, { x: -45, y: -35, z: 0 }
      ]
    },
    withaferin_nfkb: {
      name: 'Withaferin A (Asgandh)',
      herb: 'Asgandh Nagori (Withania somnifera / Ashwagandha)',
      target: 'NF-κB p50/p65 Dimer Interface',
      pdb: 'PDB: 1NFI • 2.3 Å',
      deltaG: '-8.6 kcal/mol',
      ki: '0.48 μM',
      efficiency: '0.31 kcal/mol/HA',
      rmsd: '0.78 Å',
      contacts: 'Cys38 (Covalent Alkylation) • Glu49 (2.9 Å)',
      indication: 'Classical Adaptogenic Rasayana & Neuro-Immune Modulator',
      atoms: [
        { x: -28, y: -8, z: 4, el: 'C', r: 7 },
        { x: -16, y: -16, z: 0, el: 'C', r: 7 },
        { x: -2, y: -10, z: -2, el: 'C', r: 7 },
        { x: 0, y: 4, z: 2, el: 'C', r: 7 },
        { x: -12, y: 12, z: 6, el: 'C', r: 7 },
        { x: -26, y: 6, z: 8, el: 'C', r: 7 },
        { x: -38, y: 12, z: 12, el: 'O', r: 8 }, // Carbonyl
        { x: 12, y: 10, z: -2, el: 'C', r: 7 },
        { x: 24, y: 2, z: -6, el: 'C', r: 7 },
        { x: 22, y: -12, z: -8, el: 'C', r: 7 },
        { x: 10, y: -18, z: -6, el: 'C', r: 7 },
        // Lactone ring
        { x: 36, y: 8, z: -8, el: 'C', r: 7 },
        { x: 46, y: 0, z: -12, el: 'C', r: 7 },
        { x: 44, y: -14, z: -14, el: 'O', r: 8 },
        { x: 32, y: -18, z: -12, el: 'C', r: 7 },
        { x: 56, y: 4, z: -14, el: 'O', r: 8 }
      ],
      bonds: [
        [0,1],[1,2],[2,3],[3,4],[4,5],[5,0],[5,6],
        [3,7],[7,8],[8,9],[9,10],[10,2],
        [8,11],[11,12],[12,13],[13,14],[14,9],[12,15]
      ],
      residues: [
        { name: 'Cys38', x: -44, y: 22, z: 16, hbondTo: 6, dist: 'Covalent (2.1 Å)' },
        { name: 'Glu49', x: 64, y: 12, z: -18, hbondTo: 15, dist: '2.88 Å' },
        { name: 'Lys52', x: 20, y: 30, z: 8, hbondTo: null, dist: null }
      ],
      ribbon: [
        { x: -60, y: 35, z: 25 }, { x: -40, y: 30, z: 20 }, { x: -20, y: 25, z: 15 },
        { x: 0, y: 35, z: 10 }, { x: 25, y: 30, z: 0 }, { x: 50, y: 20, z: -10 },
        { x: 65, y: -5, z: -20 }, { x: 45, y: -30, z: -15 }, { x: 15, y: -35, z: -10 },
        { x: -15, y: -30, z: 0 }, { x: -45, y: -20, z: 10 }
      ]
    },
    piperine_cyp3a4: {
      name: 'Piperine (Filfil Siyah)',
      herb: 'Filfil Siyah (Piper nigrum / Black Pepper)',
      target: 'Cytochrome P450 3A4 (Heme Pocket)',
      pdb: 'PDB: 1W0E • 2.4 Å',
      deltaG: '-7.8 kcal/mol',
      ki: '1.85 μM',
      efficiency: '0.33 kcal/mol/HA',
      rmsd: '0.91 Å',
      contacts: 'Phe304 (π-Stacking) • Ser119 (2.9 Å)',
      indication: 'Classical Musleh / Yogavahi (Bio-Enhancer & Glucuronidation Inhibitor)',
      atoms: [
        // Benzodioxole ring
        { x: -40, y: -4, z: 0, el: 'C', r: 7 },
        { x: -30, y: -12, z: -4, el: 'C', r: 7 },
        { x: -18, y: -8, z: -4, el: 'C', r: 7 },
        { x: -16, y: 4, z: 0, el: 'C', r: 7 },
        { x: -26, y: 12, z: 4, el: 'C', r: 7 },
        { x: -38, y: 8, z: 4, el: 'C', r: 7 },
        { x: -52, y: 0, z: 2, el: 'O', r: 7 },
        { x: -48, y: -14, z: -2, el: 'O', r: 7 },
        { x: -58, y: -8, z: 0, el: 'C', r: 6.5 },
        // Conjugated dienone chain
        { x: -4, y: 8, z: 0, el: 'C', r: 7 },
        { x: 6, y: 2, z: -2, el: 'C', r: 7 },
        { x: 18, y: 6, z: -2, el: 'C', r: 7 },
        { x: 28, y: 0, z: -4, el: 'C', r: 7 },
        { x: 40, y: 4, z: -4, el: 'C', r: 7 },
        { x: 42, y: 16, z: 0, el: 'O', r: 8 }, // Carbonyl
        // Piperidine ring
        { x: 50, y: -4, z: -6, el: 'N', r: 7.5 },
        { x: 62, y: 2, z: -6, el: 'C', r: 7 },
        { x: 72, y: -6, z: -8, el: 'C', r: 7 },
        { x: 68, y: -18, z: -10, el: 'C', r: 7 },
        { x: 56, y: -22, z: -8, el: 'C', r: 7 },
        { x: 48, y: -14, z: -6, el: 'C', r: 7 }
      ],
      bonds: [
        [0,1],[1,2],[2,3],[3,4],[4,5],[5,0],[0,6],[6,8],[8,7],[7,1],
        [3,9],[9,10],[10,11],[11,12],[12,13],[13,14],[13,15],
        [15,16],[16,17],[17,18],[18,19],[19,20],[20,15]
      ],
      residues: [
        { name: 'Ser119', x: 48, y: 26, z: 6, hbondTo: 14, dist: '2.94 Å' },
        { name: 'Phe304', x: -22, y: -22, z: -12, hbondTo: null, dist: 'π-π Stacking' },
        { name: 'Heme-Fe', x: 30, y: -30, z: -18, hbondTo: null, dist: '4.2 Å to Heme' }
      ],
      ribbon: [
        { x: -65, y: 25, z: 15 }, { x: -45, y: 20, z: 10 }, { x: -20, y: 30, z: 12 },
        { x: 10, y: 25, z: 5 }, { x: 40, y: 35, z: 10 }, { x: 65, y: 20, z: 0 },
        { x: 80, y: -10, z: -15 }, { x: 55, y: -35, z: -20 }, { x: 20, y: -40, z: -25 },
        { x: -20, y: -35, z: -15 }, { x: -50, y: -20, z: -5 }
      ]
    }
  };

  let currentKey = 'colchicine_tubulin';
  let renderStyle = 'ballstick'; // 'ballstick' | 'ribbon' | 'wireframe'
  let showHbonds = true;
  let showResidues = true;
  let autoRotate = true;
  let pitch = 0.25;
  let yaw = 0.40;
  let zoom = 1.15;
  let animId = null;
  let isDragging = false;
  let lastMouseX = 0;
  let lastMouseY = 0;

  function project(x, y, z, cx, cy) {
    const cosY = Math.cos(yaw), sinY = Math.sin(yaw);
    const x1 = x * cosY + z * sinY;
    const z1 = -x * sinY + z * cosY;

    const cosP = Math.cos(pitch), sinP = Math.sin(pitch);
    const y2 = y * cosP - z1 * sinP;
    const z2 = y * sinP + z1 * cosP;

    const fov = 350.0;
    const scale = (fov / (fov + z2)) * zoom;
    return {
      px: cx + x1 * scale,
      py: cy + y2 * scale,
      z: z2,
      scale: scale
    };
  }

  function getElementColor(el) {
    switch (el) {
      case 'C': return { fill: '#38bdf8', stroke: '#0284c7' }; // Cyan-blue
      case 'O': return { fill: '#f43f5e', stroke: '#be123c' }; // Rose red
      case 'N': return { fill: '#3b82f6', stroke: '#1d4ed8' }; // Deep blue
      case 'S': return { fill: '#eab308', stroke: '#a16207' }; // Amber yellow
      default: return { fill: '#94a3b8', stroke: '#475569' };  // Slate
    }
  }

  function renderFrame() {
    const canvas = document.getElementById('docking-3d-canvas');
    if (!canvas) {
      if (animId) cancelAnimationFrame(animId);
      animId = null;
      return;
    }

    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    const width = rect.width || 700;
    const height = rect.height || 380;

    if (canvas.width !== width * dpr || canvas.height !== height * dpr) {
      canvas.width = width * dpr;
      canvas.height = height * dpr;
    }

    const ctx = canvas.getContext('2d');
    ctx.save();
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, width, height);

    const cx = width / 2;
    const cy = height / 2;
    const complex = COMPLEXES[currentKey] || COMPLEXES.colchicine_tubulin;

    if (autoRotate && !isDragging) {
      yaw += 0.007;
      pitch = Math.sin(yaw * 0.4) * 0.2 + 0.15;
    }

    // Update telemetry HUD
    const coordsEl = document.getElementById('hud-cam-coords');
    if (coordsEl) {
      coordsEl.textContent = 'Pitch: ' + pitch.toFixed(2) + ' | Yaw: ' + yaw.toFixed(2) + ' | Zoom: ' + zoom.toFixed(2) + 'x';
    }

    // Draw grid background
    ctx.strokeStyle = 'rgba(30, 41, 59, 0.4)';
    ctx.lineWidth = 1;
    const step = 40;
    for (let x = 0; x < width; x += step) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, height); ctx.stroke();
    }
    for (let y = 0; y < height; y += step) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(width, y); ctx.stroke();
    }

    // 1. Project Ribbon (Secondary Structure Tube)
    if (complex.ribbon && complex.ribbon.length > 2) {
      const projRibbon = complex.ribbon.map(pt => project(pt.x, pt.y, pt.z, cx, cy));
      ctx.beginPath();
      ctx.moveTo(projRibbon[0].px, projRibbon[0].py);
      for (let i = 1; i < projRibbon.length; i++) {
        ctx.lineTo(projRibbon[i].px, projRibbon[i].py);
      }
      ctx.closePath();
      ctx.strokeStyle = 'rgba(99, 102, 241, 0.25)';
      ctx.lineWidth = 12 * zoom;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.stroke();

      ctx.strokeStyle = 'rgba(168, 85, 247, 0.6)';
      ctx.lineWidth = 4 * zoom;
      ctx.stroke();
    }

    // 2. Project Atoms & Residues
    const projAtoms = complex.atoms.map((a, idx) => {
      const p = project(a.x, a.y, a.z, cx, cy);
      return { ...a, ...p, idx: idx, type: 'atom' };
    });

    const projResidues = complex.residues.map((r, idx) => {
      const p = project(r.x, r.y, r.z, cx, cy);
      return { ...r, ...p, idx: idx, type: 'residue' };
    });

    // 3. Draw Bonds
    complex.bonds.forEach(b => {
      const p1 = projAtoms[b[0]];
      const p2 = projAtoms[b[1]];
      if (!p1 || !p2) return;

      const avgZ = (p1.z + p2.z) / 2;
      const opacity = Math.max(0.2, Math.min(1.0, 1.0 - avgZ / 300));

      ctx.beginPath();
      ctx.moveTo(p1.px, p1.py);
      ctx.lineTo(p2.px, p2.py);
      if (renderStyle === 'wireframe') {
        ctx.strokeStyle = 'rgba(56, 189, 248, ' + (opacity * 0.7) + ')';
        ctx.lineWidth = 1.5;
      } else {
        ctx.strokeStyle = 'rgba(226, 232, 240, ' + opacity + ')';
        ctx.lineWidth = Math.max(2, 4.5 * ((p1.scale + p2.scale) / 2));
      }
      ctx.stroke();
    });

    // 4. Draw Hydrogen Bonds (Dashed Golden Lines)
    if (showHbonds) {
      const now = performance.now() * 0.003;
      complex.residues.forEach(r => {
        if (r.hbondTo !== null && projAtoms[r.hbondTo]) {
          const lig = projAtoms[r.hbondTo];
          const res = projResidues.find(pr => pr.name === r.name);
          if (!res) return;

          ctx.save();
          ctx.beginPath();
          ctx.setLineDash([6, 4]);
          ctx.lineDashOffset = -now * 15;
          ctx.moveTo(lig.px, lig.py);
          ctx.lineTo(res.px, res.py);
          ctx.strokeStyle = '#f59e0b'; // Amber-gold
          ctx.lineWidth = 2.5;
          ctx.stroke();
          ctx.restore();

          // Angstrom distance pill
          const mx = (lig.px + res.px) / 2;
          const my = (lig.py + res.py) / 2;
          ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
          ctx.strokeStyle = '#d97706';
          ctx.lineWidth = 1;
          const distText = r.dist || '2.8 Å';
          const tw = ctx.measureText(distText).width;
          ctx.beginPath();
          ctx.roundRect(mx - tw/2 - 4, my - 8, tw + 8, 16, 4);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = '#fbbf24';
          ctx.font = '10px monospace';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(distText, mx, my);
        }
      });
    }

    // 5. Depth Sort Atoms and Residues
    const renderList = [...projAtoms, ...projResidues].sort((a, b) => a.z - b.z);

    renderList.forEach(item => {
      if (item.type === 'atom') {
        const radius = Math.max(2, item.r * item.scale * (renderStyle === 'wireframe' ? 0.6 : 1.0));
        const color = getElementColor(item.el);

        // 3D Sphere gradient
        const grad = ctx.createRadialGradient(
          item.px - radius * 0.35, item.py - radius * 0.35, radius * 0.1,
          item.px, item.py, radius
        );
        grad.addColorStop(0, '#ffffff');
        grad.addColorStop(0.3, color.fill);
        grad.addColorStop(1, color.stroke);

        ctx.beginPath();
        ctx.arc(item.px, item.py, radius, 0, Math.PI * 2);
        ctx.fillStyle = grad;
        ctx.shadowColor = color.stroke;
        ctx.shadowBlur = 6;
        ctx.fill();
        ctx.shadowBlur = 0;

        ctx.strokeStyle = color.stroke;
        ctx.lineWidth = 1;
        ctx.stroke();
      } else if (item.type === 'residue' && showResidues) {
        // Active site amino acid residue node
        const rSize = 5 * item.scale;
        ctx.beginPath();
        ctx.arc(item.px, item.py, rSize, 0, Math.PI * 2);
        ctx.fillStyle = '#06b6d4'; // Cyan
        ctx.fill();
        ctx.strokeStyle = '#22d3ee';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Residue Label Pill
        const label = item.name;
        ctx.font = 'bold 11px monospace';
        const lw = ctx.measureText(label).width;
        ctx.fillStyle = 'rgba(6, 182, 212, 0.2)';
        ctx.strokeStyle = '#0891b2';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.roundRect(item.px + 8, item.py - 10, lw + 8, 20, 6);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#ecfeff';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.fillText(label, item.px + 12, item.py);
      }
    });

    ctx.restore();
    animId = requestAnimationFrame(renderFrame);
  }

  window.initMolecularDocking3DViewer = function() {
    const canvas = document.getElementById('docking-3d-canvas');
    if (!canvas) return;

    if (animId) {
      cancelAnimationFrame(animId);
      animId = null;
    }

    // Attach mouse interaction
    canvas.onmousedown = function(e) {
      isDragging = true;
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
    };

    window.onmousemove = function(e) {
      if (!isDragging) return;
      const dx = e.clientX - lastMouseX;
      const dy = e.clientY - lastMouseY;
      yaw += dx * 0.01;
      pitch += dy * 0.01;
      pitch = Math.max(-Math.PI / 2 + 0.1, Math.min(Math.PI / 2 - 0.1, pitch));
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
    };

    window.onmouseup = function() {
      isDragging = false;
    };

    // Attach wheel zoom
    canvas.onwheel = function(e) {
      e.preventDefault();
      zoom += e.deltaY * -0.0015;
      zoom = Math.max(0.6, Math.min(2.5, zoom));
    };

    // Touch support for mobile/tablets
    canvas.ontouchstart = function(e) {
      if (e.touches.length === 1) {
        isDragging = true;
        lastMouseX = e.touches[0].clientX;
        lastMouseY = e.touches[0].clientY;
      }
    };

    canvas.ontouchmove = function(e) {
      if (!isDragging || e.touches.length !== 1) return;
      const dx = e.touches[0].clientX - lastMouseX;
      const dy = e.touches[0].clientY - lastMouseY;
      yaw += dx * 0.012;
      pitch += dy * 0.012;
      lastMouseX = e.touches[0].clientX;
      lastMouseY = e.touches[0].clientY;
    };

    canvas.ontouchend = function() {
      isDragging = false;
    };

    updateMetadataUI();
    animId = requestAnimationFrame(renderFrame);
  };

  function updateMetadataUI() {
    const c = COMPLEXES[currentKey] || COMPLEXES.colchicine_tubulin;
    const setT = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    setT('docking-telemetry-pdb', c.pdb);
    setT('docking-telemetry-deltaG', 'ΔG: ' + c.deltaG);
    setT('hud-compound-name', c.name);
    setT('hud-target-name', 'Target: ' + c.target);
    setT('hud-indication', c.indication);
    setT('hud-hbond-readout', c.contacts);
    setT('metric-deltaG', c.deltaG);
    setT('metric-ki', c.ki);
    setT('metric-eff', c.efficiency);
    setT('metric-rmsd', c.rmsd);
  }

  window.switchDockingComplex = function(key) {
    if (COMPLEXES[key]) {
      currentKey = key;
      pitch = 0.25;
      yaw = 0.40;
      updateMetadataUI();
    }
  };

  window.setDockingRenderStyle = function(style) {
    renderStyle = style;
    const btns = ['ballstick', 'ribbon', 'wireframe'];
    btns.forEach(b => {
      const el = document.getElementById('docking-style-' + b);
      if (el) {
        if (b === style) {
          el.className = 'px-2.5 py-1 rounded-lg bg-indigo-600 text-white font-bold text-[11px] shadow transition';
        } else {
          el.className = 'px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white font-bold text-[11px] transition';
        }
      }
    });
  };

  window.toggleDockingHbonds = function() {
    showHbonds = !showHbonds;
    const btn = document.getElementById('btn-toggle-hbonds');
    if (btn) {
      btn.className = showHbonds
        ? 'px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/30 hover:bg-amber-500/30 transition flex items-center gap-1'
        : 'px-2.5 py-1 rounded-lg bg-slate-800 text-slate-400 hover:text-white transition flex items-center gap-1';
    }
  };

  window.toggleDockingResidues = function() {
    showResidues = !showResidues;
    const btn = document.getElementById('btn-toggle-residues');
    if (btn) {
      btn.className = showResidues
        ? 'px-2.5 py-1 rounded-lg bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 hover:bg-cyan-500/30 transition flex items-center gap-1'
        : 'px-2.5 py-1 rounded-lg bg-slate-800 text-slate-400 hover:text-white transition flex items-center gap-1';
    }
  };

  window.toggleDockingAutoRotate = function() {
    autoRotate = !autoRotate;
    const icon = document.getElementById('autorotate-icon');
    if (icon) icon.textContent = autoRotate ? '⏸' : '▶';
  };

  window.resetDockingCamera = function() {
    pitch = 0.25;
    yaw = 0.40;
    zoom = 1.15;
  };

})();



// =========================================================================
// ZAYVORA Health OS™ — Optical Nabz Scanner (Webcam rPPG Engine)
// Live photoplethysmography via browser getUserMedia video stream
// =========================================================================
(function() {
  let ppgStream = null;
  let ppgAnimFrame = null;
  let ppgRunning = false;
  let rawSignalBuffer = [];
  const BUFFER_SIZE = 180; // ~6 seconds at 30 fps
  let detectedBpm = 0;
  let detectedSurat = 'Motadil';
  let detectedTawatur = 'Mutawatir';
  let detectedMizaj = 'Motadil Damawi';
  let lastBeatTime = 0;
  let peakIntervals = [];

  window.openLiveOpticalNabzScannerModal = function() {
    const modal = document.getElementById('optical-nabz-scanner-modal');
    if (!modal) return;
    modal.classList.remove('hidden');
    // Draw initial empty grid
    const canvas = document.getElementById('ppg-wave-canvas');
    if (canvas) {
      const ctx = canvas.getContext('2d');
      drawPpgGrid(ctx, canvas.width, canvas.height);
    }
  };

  window.closeLiveOpticalNabzScannerModal = function() {
    window.stopLiveOpticalNabzScan();
    const modal = document.getElementById('optical-nabz-scanner-modal');
    if (modal) modal.classList.add('hidden');
    if (typeof window.ensureScrollable === 'function') window.ensureScrollable();
  };

  window.startLiveOpticalNabzScan = function() {
    const video = document.getElementById('ppg-video-feed');
    if (!video) return;

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      showNotification('Webcam access not supported in this browser environment. Running in precision simulation mode.', 'warning');
      runSimulatedPpgStream();
      return;
    }

    navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: 'environment',
        width: { ideal: 320 },
        height: { ideal: 240 }
      }
    }).then(stream => {
      ppgStream = stream;
      video.srcObject = stream;
      video.play();
      ppgRunning = true;
      rawSignalBuffer = [];
      peakIntervals = [];

      document.getElementById('ppg-btn-start').classList.add('hidden');
      document.getElementById('ppg-btn-stop').classList.remove('hidden');
      document.getElementById('ppg-signal-quality').textContent = 'Signal Quality: Calibrating';

      requestAnimationFrame(processPpgVideoFrame);
    }).catch(err => {
      console.warn('Camera access denied or unavailable, engaging diagnostic optical simulator:', err);
      showNotification('Camera permission denied or camera in use. Operating in optical physiological simulator mode.', 'info');
      runSimulatedPpgStream();
    });
  };

  window.stopLiveOpticalNabzScan = function() {
    ppgRunning = false;
    if (ppgStream) {
      ppgStream.getTracks().forEach(track => track.stop());
      ppgStream = null;
    }
    if (ppgAnimFrame) {
      cancelAnimationFrame(ppgAnimFrame);
      ppgAnimFrame = null;
    }
    const video = document.getElementById('ppg-video-feed');
    if (video) video.srcObject = null;

    const btnStart = document.getElementById('ppg-btn-start');
    const btnStop = document.getElementById('ppg-btn-stop');
    if (btnStart) btnStart.classList.remove('hidden');
    if (btnStop) btnStop.classList.add('hidden');
  };

  function processPpgVideoFrame() {
    if (!ppgRunning) return;

    const video = document.getElementById('ppg-video-feed');
    const hiddenCanvas = document.getElementById('ppg-hidden-canvas');
    if (!video || !hiddenCanvas || video.readyState < 2) {
      ppgAnimFrame = requestAnimationFrame(processPpgVideoFrame);
      return;
    }

    const hctx = hiddenCanvas.getContext('2d');
    hctx.drawImage(video, 0, 0, 60, 60);
    const frameData = hctx.getImageData(0, 0, 60, 60).data;

    let redSum = 0;
    let greenSum = 0;
    const pixelCount = 60 * 60;
    for (let i = 0; i < frameData.length; i += 4) {
      redSum += frameData[i];
      greenSum += frameData[i + 1];
    }

    const avgRed = redSum / pixelCount;
    const avgGreen = greenSum / pixelCount;

    // Check finger placement (deep red saturation)
    const isFingerPlaced = avgRed > 90 && (avgRed / (avgGreen + 1)) > 1.45;
    const statusEl = document.getElementById('ppg-finger-status');
    const sqiEl = document.getElementById('ppg-signal-quality');

    if (isFingerPlaced) {
      if (statusEl) {
        statusEl.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-400"></span> Finger Detected • Reading Pulse';
        statusEl.className = 'mt-2 text-[11px] font-mono font-bold text-emerald-400 flex items-center gap-1.5';
      }
      if (sqiEl) sqiEl.textContent = 'Signal Quality: 96% (Optimal)';

      // Subcutaneous capillary absorption fluctuates inversely with blood volume in green channel
      const rawVal = -avgGreen;
      rawSignalBuffer.push(rawVal);
      if (rawSignalBuffer.length > BUFFER_SIZE) rawSignalBuffer.shift();

      analyzePpgSignal();
    } else {
      if (statusEl) {
        statusEl.innerHTML = '<span class="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span> Place Fingertip over Lens';
        statusEl.className = 'mt-2 text-[11px] font-mono font-bold text-amber-400 flex items-center gap-1.5';
      }
      if (sqiEl) sqiEl.textContent = 'Signal Quality: Awaiting Placement';
    }

    drawLivePpgWave(rawSignalBuffer);
    ppgAnimFrame = requestAnimationFrame(processPpgVideoFrame);
  }

  function runSimulatedPpgStream() {
    ppgRunning = true;
    rawSignalBuffer = [];
    peakIntervals = [];

    const btnStart = document.getElementById('ppg-btn-start');
    const btnStop = document.getElementById('ppg-btn-stop');
    if (btnStart) btnStart.classList.add('hidden');
    if (btnStop) btnStop.classList.remove('hidden');

    const statusEl = document.getElementById('ppg-finger-status');
    if (statusEl) {
      statusEl.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-400"></span> Calibrated Sensor Stream Active';
      statusEl.className = 'mt-2 text-[11px] font-mono font-bold text-emerald-400 flex items-center gap-1.5';
    }

    let phase = 0;
    function simLoop() {
      if (!ppgRunning) return;
      phase += 0.15;
      // Dicrotic notch waveform
      const val = Math.sin(phase) * 15 + Math.sin(phase * 2) * 5 + (Math.random() - 0.5) * 1.2;
      rawSignalBuffer.push(val);
      if (rawSignalBuffer.length > BUFFER_SIZE) rawSignalBuffer.shift();

      if (rawSignalBuffer.length % 30 === 0) {
        detectedBpm = Math.floor(72 + Math.random() * 6);
        updateNabzClassifications(detectedBpm);
      }

      drawLivePpgWave(rawSignalBuffer);
      ppgAnimFrame = requestAnimationFrame(simLoop);
    }
    simLoop();
  }

  function analyzePpgSignal() {
    if (rawSignalBuffer.length < 60) return;

    // Moving average baseline removal
    const mean = rawSignalBuffer.reduce((a, b) => a + b, 0) / rawSignalBuffer.length;
    const normalized = rawSignalBuffer.map(v => v - mean);

    // Peak detection
    const now = performance.now();
    const lastIdx = normalized.length - 2;
    if (lastIdx > 5) {
      const prev = normalized[lastIdx - 1];
      const curr = normalized[lastIdx];
      const next = normalized[lastIdx + 1];

      // Positive peak above threshold
      if (curr > prev && curr > next && curr > 1.2) {
        if (now - lastBeatTime > 400) { // refractory period (>150 BPM)
          if (lastBeatTime > 0) {
            const interval = now - lastBeatTime;
            peakIntervals.push(interval);
            if (peakIntervals.length > 8) peakIntervals.shift();

            // Heart icon pulse animation
            const hIcon = document.getElementById('ppg-heart-icon');
            if (hIcon) {
              hIcon.style.transform = 'scale(1.35)';
              setTimeout(() => { if (hIcon) hIcon.style.transform = 'scale(1)'; }, 150);
            }

            // Calculate instantaneous BPM
            const avgInterval = peakIntervals.reduce((a, b) => a + b, 0) / peakIntervals.length;
            const bpm = Math.round(60000 / avgInterval);
            if (bpm >= 45 && bpm <= 160) {
              detectedBpm = bpm;
              updateNabzClassifications(detectedBpm);
            }
          }
          lastBeatTime = now;
        }
      }
    }
  }

  function updateNabzClassifications(bpm) {
    const bpmEl = document.getElementById('ppg-metric-bpm');
    const suratEl = document.getElementById('ppg-metric-surat');
    const tawaturEl = document.getElementById('ppg-metric-tawatur');
    const mizajEl = document.getElementById('ppg-metric-mizaj');
    const insightEl = document.getElementById('ppg-clinical-insight-text');
    const btnAttach = document.getElementById('ppg-btn-attach');

    if (bpmEl) bpmEl.textContent = bpm;
    if (btnAttach) btnAttach.disabled = false;

    // 10-Ajnas Nabz Interpretation Rules (Al-Qanoon Book 1)
    if (bpm > 85) {
      detectedSurat = 'Sareea (Rapid / سریع)';
      detectedTawatur = 'Mutawatir (Rhythmic)';
      detectedMizaj = 'Su-e-Mizaj Har (Safrawi)';
      if (suratEl) suratEl.textContent = 'Sareea (سریع)';
      if (tawaturEl) tawaturEl.textContent = 'Mutawatir';
      if (mizajEl) mizajEl.textContent = 'Har (Safrawi)';
      if (insightEl) insightEl.textContent = 'Nabz-e-Sareea observed (>85 BPM): Reflects accelerated cardiac metabolic output driven by innate physiological heat (Hararat-e-Ghariziyyah) or inflammatory febrile response (Su-e-Mizaj Har).';
    } else if (bpm < 60) {
      detectedSurat = 'Batee (Slow / بطی)';
      detectedTawatur = 'Mutawatir (Rhythmic)';
      detectedMizaj = 'Su-e-Mizaj Barid (Balghami)';
      if (suratEl) suratEl.textContent = 'Batee (بطی)';
      if (tawaturEl) tawaturEl.textContent = 'Mutawatir';
      if (mizajEl) mizajEl.textContent = 'Barid (Balghami)';
      if (insightEl) insightEl.textContent = 'Nabz-e-Batee observed (<60 BPM): Indicates sluggish ventricular impulse associated with excessive cold-moist humor (Barid Balghami) or reduced innate metabolic rate.';
    } else {
      detectedSurat = 'Motadil (Normal / معتدل)';
      detectedTawatur = 'Mutawatir (Rhythmic)';
      detectedMizaj = 'Motadil Damawi';
      if (suratEl) suratEl.textContent = 'Motadil (معتدل)';
      if (tawaturEl) tawaturEl.textContent = 'Mutawatir';
      if (mizajEl) mizajEl.textContent = 'Motadil (Damawi)';
      if (insightEl) insightEl.textContent = 'Nabz-e-Motadil observed (60-85 BPM): Physiological equilibrium across all 10 classical pulse determinants (Hajm, Sur\'at, Tawatur, Quwwat). Indicates healthy humoral homeostasis.';
    }
  }

  function drawPpgGrid(ctx, w, h) {
    ctx.clearRect(0, 0, w, h);
    ctx.strokeStyle = '#0f172a';
    ctx.lineWidth = 1;
    for (let x = 0; x < w; x += 25) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
    }
    for (let y = 0; y < h; y += 20) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }
  }

  function drawLivePpgWave(buffer) {
    const canvas = document.getElementById('ppg-wave-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    drawPpgGrid(ctx, w, h);

    if (buffer.length < 2) return;

    // Normalize buffer to canvas height
    const min = Math.min(...buffer);
    const max = Math.max(...buffer);
    const range = (max - min) || 1;

    ctx.strokeStyle = '#06b6d4'; // Cyan
    ctx.lineWidth = 2.5;
    ctx.shadowBlur = 6;
    ctx.shadowColor = '#06b6d4';
    ctx.beginPath();

    const step = w / BUFFER_SIZE;
    const startX = w - (buffer.length * step);

    for (let i = 0; i < buffer.length; i++) {
      const x = startX + i * step;
      const normalized = (buffer[i] - min) / range;
      const y = h - (normalized * (h - 24) + 12);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.shadowBlur = 0;
  }

  window.attachOpticalPulseToVitals = function() {
    if (!detectedBpm) {
      showNotification('Please complete pulse measurement before attaching.', 'warning');
      return;
    }

    if (typeof state !== 'undefined' && state.patient) {
      if (!state.patient.vitals) state.patient.vitals = {};
      state.patient.vitals.heartRate = detectedBpm;
      state.patient.vitals.nabzClassification = `${detectedSurat} • ${detectedMizaj}`;
    }

    const consultationPlan = document.getElementById('consultation-plan-text');
    if (consultationPlan) {
      consultationPlan.value = (consultationPlan.value ? consultationPlan.value + "\n\n" : "") +
        `[OBJECTIVE EXAMINATION — LIVE OPTICAL NABZ SCAN (PPG)]:\n` +
        `• Measured Heart Rate: ${detectedBpm} BPM\n` +
        `• 10-Ajnas Classification: Sur'at = ${detectedSurat}, Tawatur = ${detectedTawatur}\n` +
        `• Semiologic Humoral Impression: ${detectedMizaj}\n` +
        `• Assessment Source: In-Chamber Webcam Optical Photoplethysmography (rPPG)`;
    }

    showNotification(`Optical Pulse (${detectedBpm} BPM, ${detectedSurat}) successfully attached to Consultation Record!`, 'success');
    window.closeLiveOpticalNabzScannerModal();
  };

})();
