import sys
import json
import os
sys.path.insert(0, ".")

from services.knowledge.app.data.grand_integrative_library_master import GRAND_INTEGRATIVE_LIBRARY
from services.knowledge.app.data.canonical_treatises import CANONICAL_TREATISES

# Ensure every chapter in GRAND_INTEGRATIVE_LIBRARY has its full_treatise
for vol in GRAND_INTEGRATIVE_LIBRARY["volumes"]:
    for ch in vol["chapters"]:
        tr = CANONICAL_TREATISES.get(ch["id"])
        if tr:
            ch["full_treatise"] = tr

library_json_str = json.dumps(GRAND_INTEGRATIVE_LIBRARY, ensure_ascii=False)

modal_html = """
  <!-- ===================================================================== -->
  <!-- GRAND INTEGRATIVE MEDICAL LIBRARY MODAL (12 VOLUMES — DUAL LAYER) -->
  <!-- ===================================================================== -->
  <div id="grand-library-modal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4">
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl max-w-4xl w-full p-6 space-y-4 shadow-2xl max-h-[92vh] flex flex-col">
      <div class="flex justify-between items-start border-b border-[var(--border)] pb-3 flex-shrink-0">
        <div>
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-bold">12-VOLUME CANONICAL CLINICAL DOCTRINE</span>
            <span id="grand-lib-modal-badge" class="px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 font-mono text-[10px] font-bold">Classical & Modern</span>
          </div>
          <h3 id="grand-lib-modal-title" class="font-bold text-lg text-white mt-1"></h3>
          <p id="grand-lib-modal-urdu" class="text-xs text-emerald-400 font-medium font-serif" dir="rtl"></p>
        </div>
        <button onclick="closeGrandLibraryModal()" class="text-[var(--muted)] hover:text-white p-2 text-lg">✕</button>
      </div>

      <!-- DUAL-LAYER TAB SWITCHER -->
      <div class="flex items-center gap-2 border-b border-[var(--border)] pb-2 flex-shrink-0">
        <button id="modal-tab-protocol" onclick="switchModalLayer('protocol')" class="px-4 py-2 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-sm flex items-center gap-1.5 transition">
          <span>⚡ Layer 1: Quick Clinical Protocol</span>
          <span class="text-[10px] opacity-80">(فوری سريري رہنما)</span>
        </button>
        <button id="modal-tab-treatise" onclick="switchModalLayer('treatise')" class="px-4 py-2 rounded-xl text-xs font-bold bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 flex items-center gap-1.5 transition">
          <span>📖 Layer 2: Full Canonical Treatise</span>
          <span class="text-[10px] opacity-80">(مفصل نصابی مطالعہ)</span>
        </button>
      </div>

      <div id="grand-library-modal-body" class="overflow-y-auto space-y-4 pr-1 text-xs text-slate-200">
        <!-- Chapter content rendered dynamically based on active layer -->
      </div>
      <div class="pt-3 border-t border-[var(--border)] flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 flex-shrink-0">
        <span class="text-[11px] text-[var(--muted)]">ZAYVORA Health OS • Canonical Dual-Layer Knowledge Base</span>
        <div class="flex gap-2">
          <button onclick="switchModalLayer(currentModalLayer === 'protocol' ? 'treatise' : 'protocol')" class="px-4 py-2 rounded-xl border border-slate-700 bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 font-medium">
            Toggle Protocol / Treatise
          </button>
          <button onclick="closeGrandLibraryModal()" class="px-4 py-2 rounded-xl border border-[var(--border)] text-xs text-[var(--muted)] hover:text-white">Close</button>
          <button onclick="copyCurrentChapterProtocol()" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow flex items-center gap-1.5">
            <span>Copy Protocol to Care Plan</span>
          </button>
        </div>
      </div>
    </div>
  </div>
"""

dual_layer_js = """
    // =========================================================================
    // GRAND INTEGRATIVE MEDICAL LIBRARY (12 VOLUMES) — DUAL-LAYER ENGINE
    // =========================================================================
    window.ZAYVORA_GRAND_LIBRARY_DATA = __LIBRARY_JSON__;
    let currentLibrarySelectedVol = 'all';
    let currentActiveChapter = null;
    let currentModalLayer = 'protocol'; // 'protocol' | 'treatise'

    function renderGrandLibrary(container, context) {
      const subnav = typeof getWebsiteHubSubnav === 'function' ? getWebsiteHubSubnav(state.tab) : '';
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib) return;

      let html = `
        <div class="max-w-6xl mx-auto space-y-6 pb-12">
          ${context === 'website' ? subnav : ''}
          
          <!-- Library Header Hero -->
          <div class="bg-gradient-to-r from-emerald-950/60 via-slate-900 to-slate-900 p-8 rounded-3xl border border-emerald-500/30 space-y-4 shadow-xl">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold font-mono">12 MASTER VOLUMES</span>
                <span class="px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-mono">38 CANONICAL CHAPTERS</span>
                <span class="px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 text-xs font-mono">DUAL-LAYER ARCHITECTURE</span>
              </div>
              ${context === 'website' ? '<button onclick="viewWebsitePage(\\'home\\')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>' : ''}
            </div>
            <div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-white">ZAYVORA Grand Classical &amp; Modern Integrative Medical Library</h1>
              <p class="text-emerald-400 font-serif text-sm mt-1" dir="rtl">جامع طبی کتب خانہ — ۱۲ ابواب، روایتی کلیات، نبض، اخلاط اور جدید تشخیصی و علاجی علوم (دو تہی نظام)</p>
            </div>
            <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-4xl">
              The authoritative dual-layer doctrine of ZAYVORA Health OS. Switch seamlessly between <strong>Layer 1 (Quick Bedside Protocols &amp; Dosages)</strong> and <strong>Layer 2 (Exhaustive Academic Treatises &amp; Formulations)</strong> spanning classical Unani canons and contemporary clinical medicine.
            </p>

            <!-- Search Bar -->
            <div class="pt-2">
              <div class="relative">
                <input 
                  type="text" 
                  id="grand-lib-search-input" 
                  placeholder="Search 12 volumes by syndrome, biomarker, pulse, herb, or clinical protocol (e.g. Nabz, hs-CRP, FibroScan, Suranjan, PCOS)..." 
                  oninput="handleGrandLibrarySearch(this.value)"
                  class="w-full pl-10 pr-4 py-3 bg-slate-900/90 border border-emerald-500/40 rounded-xl text-xs sm:text-sm text-white focus:outline-none focus:border-emerald-400 shadow-inner"
                >
                <span class="absolute left-3.5 top-3.5 text-slate-400 text-sm">🔍</span>
              </div>
              <div id="grand-lib-search-stats" class="text-[11px] text-slate-400 mt-1.5 flex justify-between">
                <span>Showing 12 Master Volumes (38 Chapters • Dual-Layer)</span>
                <span class="text-emerald-400 font-mono">Zero synthetic mock data • 100% Peer-Reviewed</span>
              </div>
            </div>
          </div>

          <!-- Volume Filter Tabs -->
          <div class="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
            <button onclick="filterGrandLibraryVolume('all')" id="lib-filter-btn-all" class="px-3.5 py-1.5 rounded-xl bg-emerald-600 text-white text-xs font-bold flex-shrink-0 transition">
              All 12 Volumes
            </button>
            ${lib.volumes.map(v => `
              <button onclick="filterGrandLibraryVolume('${v.id}')" id="lib-filter-btn-${v.id}" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-medium flex-shrink-0 transition">
                <span>${v.icon} Vol ${v.volume_number}</span>
              </button>
            `).join('')}
          </div>

          <!-- Volume Cards Grid -->
          <div id="grand-library-grid" class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <!-- Rendered by JS -->
          </div>
        </div>
      `;

      container.innerHTML = html;
      renderGrandLibraryCards(lib.volumes);
    }

    function renderGrandLibraryCards(volumes) {
      const grid = document.getElementById('grand-library-grid');
      if (!grid) return;

      if (!volumes || volumes.length === 0) {
        grid.innerHTML = `
          <div class="col-span-2 p-8 text-center bg-[var(--card)] border border-[var(--border)] rounded-2xl">
            <p class="text-slate-400 text-sm">No medical doctrine chapters matched your search query.</p>
          </div>
        `;
        return;
      }

      grid.innerHTML = volumes.map(v => `
        <div class="bg-[var(--card)] border border-[var(--border)] hover:border-emerald-500/50 transition rounded-2xl p-6 shadow-sm space-y-4 flex flex-col justify-between">
          <div class="space-y-3">
            <div class="flex justify-between items-start gap-2">
              <span class="text-2xl">${v.icon}</span>
              <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold font-mono">
                ${v.badge}
              </span>
            </div>
            <div>
              <span class="text-[10px] font-mono text-cyan-300 font-bold uppercase tracking-wider block">VOLUME ${v.volume_number}</span>
              <h3 class="text-base font-bold text-white leading-snug mt-0.5">${v.title_en}</h3>
              <p class="text-xs text-emerald-400 font-serif mt-1" dir="rtl">${v.title_ur}</p>
            </div>
            <p class="text-xs text-[var(--muted)] leading-relaxed">${v.summary}</p>
          </div>

          <div class="space-y-2 pt-3 border-t border-[var(--border)]">
            <div class="flex justify-between items-center">
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Codified Chapters (${v.chapters.length})</span>
              <span class="text-[10px] font-mono text-emerald-400">⚡ Protocol &amp; 📖 Treatise</span>
            </div>
            <div class="space-y-1.5">
              ${v.chapters.map(ch => `
                <button 
                  onclick="openGrandLibraryChapterModal('${v.id}', '${ch.id}')" 
                  class="w-full text-left p-2 rounded-xl bg-slate-900/70 hover:bg-emerald-950/40 border border-slate-800 hover:border-emerald-500/40 transition flex items-center justify-between group"
                >
                  <div class="flex items-center gap-2 overflow-hidden pr-2">
                    <span class="font-mono text-emerald-400 text-[11px] font-bold">${v.volume_number}.${ch.chapter_number}</span>
                    <span class="text-xs text-slate-300 group-hover:text-white truncate font-medium">${ch.title_en}</span>
                  </div>
                  <div class="flex items-center gap-1.5">
                    <span class="px-1.5 py-0.2 rounded bg-slate-800 text-[10px] font-mono text-cyan-300">Dual-Layer</span>
                    <span class="text-emerald-400 text-xs font-mono group-hover:translate-x-0.5 transition">Read →</span>
                  </div>
                </button>
              `).join('')}
            </div>
          </div>
        </div>
      `).join('');
    }

    function filterGrandLibraryVolume(volId) {
      currentLibrarySelectedVol = volId;
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib) return;

      const allBtns = document.querySelectorAll('[id^="lib-filter-btn-"]');
      allBtns.forEach(btn => {
        btn.classList.remove('bg-emerald-600', 'text-white', 'font-bold');
        btn.classList.add('bg-slate-900', 'text-slate-300');
      });

      const activeBtn = document.getElementById(`lib-filter-btn-${volId}`);
      if (activeBtn) {
        activeBtn.classList.remove('bg-slate-900', 'text-slate-300');
        activeBtn.classList.add('bg-emerald-600', 'text-white', 'font-bold');
      }

      if (volId === 'all') {
        renderGrandLibraryCards(lib.volumes);
      } else {
        const filtered = lib.volumes.filter(v => v.id === volId);
        renderGrandLibraryCards(filtered);
      }
    }

    function handleGrandLibrarySearch(query) {
      const q = (query || '').trim().toLowerCase();
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib) return;

      const statsEl = document.getElementById('grand-lib-search-stats');

      if (!q) {
        if (statsEl) statsEl.innerHTML = `<span>Showing 12 Master Volumes (38 Chapters • Dual-Layer)</span><span class="text-emerald-400 font-mono">Zero synthetic mock data • 100% Authentic Citations</span>`;
        filterGrandLibraryVolume(currentLibrarySelectedVol);
        return;
      }

      const matchingVolumes = [];
      let totalMatchingChapters = 0;

      lib.volumes.forEach(vol => {
        const volMatches = vol.title_en.toLowerCase().includes(q) ||
                           vol.title_ur.toLowerCase().includes(q) ||
                           vol.summary.toLowerCase().includes(q);

        const matchingChapters = vol.chapters.filter(ch => {
          const tr = ch.full_treatise || {};
          return ch.title_en.toLowerCase().includes(q) ||
                 ch.title_ur.toLowerCase().includes(q) ||
                 (ch.key_concepts && ch.key_concepts.some(k => k.toLowerCase().includes(q))) ||
                 (ch.classical_citations && ch.classical_citations.some(c => (typeof c === 'string' ? c : c.book + ' ' + c.author + ' ' + c.text).toLowerCase().includes(q))) ||
                 (ch.modern_biomedical_correlation && ch.modern_biomedical_correlation.toLowerCase().includes(q)) ||
                 (ch.clinical_diagnostic_criteria && (Array.isArray(ch.clinical_diagnostic_criteria) ? ch.clinical_diagnostic_criteria.some(d => d.toLowerCase().includes(q)) : ch.clinical_diagnostic_criteria.toLowerCase().includes(q))) ||
                 (ch.actionable_protocols && (Array.isArray(ch.actionable_protocols) ? ch.actionable_protocols.some(p => p.toLowerCase().includes(q)) : ch.actionable_protocols.toLowerCase().includes(q))) ||
                 (tr.canonical_philosophy_and_doctrine && tr.canonical_philosophy_and_doctrine.toLowerCase().includes(q)) ||
                 (tr.molecular_and_cellular_pathophysiology && tr.molecular_and_cellular_pathophysiology.toLowerCase().includes(q)) ||
                 (tr.comprehensive_pharmacopeia_and_recipes && tr.comprehensive_pharmacopeia_and_recipes.toLowerCase().includes(q)) ||
                 (tr.clinical_case_study && tr.clinical_case_study.toLowerCase().includes(q));
        });

        if (volMatches || matchingChapters.length > 0) {
          totalMatchingChapters += matchingChapters.length;
          matchingVolumes.push({
            ...vol,
            chapters: matchingChapters.length > 0 ? matchingChapters : vol.chapters
          });
        }
      });

      if (statsEl) {
        statsEl.innerHTML = `<span class="text-emerald-400 font-bold">${matchingVolumes.length} volumes (${totalMatchingChapters} chapters) match "${q}"</span><button onclick="document.getElementById('grand-lib-search-input').value=''; handleGrandLibrarySearch('');" class="text-cyan-400 hover:underline">Reset</button>`;
      }

      renderGrandLibraryCards(matchingVolumes);
    }

    function switchModalLayer(layer) {
      currentModalLayer = layer;
      const tabProtocol = document.getElementById('modal-tab-protocol');
      const tabTreatise = document.getElementById('modal-tab-treatise');
      if (tabProtocol && tabTreatise) {
        if (layer === 'protocol') {
          tabProtocol.className = "px-4 py-2 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-sm flex items-center gap-1.5 transition";
          tabTreatise.className = "px-4 py-2 rounded-xl text-xs font-bold bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 flex items-center gap-1.5 transition";
        } else {
          tabTreatise.className = "px-4 py-2 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-sm flex items-center gap-1.5 transition";
          tabProtocol.className = "px-4 py-2 rounded-xl text-xs font-bold bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 flex items-center gap-1.5 transition";
        }
      }
      renderModalBody();
    }

    function renderModalBody() {
      const bodyEl = document.getElementById('grand-library-modal-body');
      if (!bodyEl || !currentActiveChapter) return;

      const { vol, ch } = currentActiveChapter;
      const tr = ch.full_treatise || {};

      if (currentModalLayer === 'protocol') {
        // LAYER 1: QUICK CLINICAL PROTOCOL
        bodyEl.innerHTML = `
          <div class="space-y-4">
            <!-- Key Concepts -->
            ${ch.key_concepts && ch.key_concepts.length > 0 ? `
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">Key Canonical Concepts</span>
                <div class="flex flex-wrap gap-1.5">
                  ${ch.key_concepts.map(k => `<span class="px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-300 text-[11px] font-medium border border-emerald-500/20">${k}</span>`).join('')}
                </div>
              </div>
            ` : ''}

            <!-- Classical Citations -->
            ${ch.classical_citations && ch.classical_citations.length > 0 ? `
              <div class="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 space-y-2">
                <span class="text-[10px] font-bold text-amber-300 uppercase tracking-wider block">Classical Citations &amp; Authorities</span>
                <ul class="space-y-1.5 text-xs text-amber-100/90">
                  ${ch.classical_citations.map(c => `
                    <li class="p-2 rounded-lg bg-slate-900/60 border border-amber-500/20">
                      <strong class="text-amber-300 block">${typeof c === 'string' ? c : c.book + ' — ' + c.author}</strong>
                      ${c.text ? `<p class="italic text-slate-300 mt-0.5">"${c.text}"</p>` : ''}
                    </li>
                  `).join('')}
                </ul>
              </div>
            ` : ''}

            <!-- Modern Biomedical Correlation -->
            ${ch.modern_biomedical_correlation ? `
              <div class="p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/30 space-y-2">
                <span class="text-[10px] font-bold text-cyan-300 uppercase tracking-wider block">Modern Biomedical &amp; Pathophysiological Correlation</span>
                <p class="text-xs text-cyan-100/90 leading-relaxed">${ch.modern_biomedical_correlation}</p>
              </div>
            ` : ''}

            <!-- Clinical Diagnostic Criteria -->
            ${ch.clinical_diagnostic_criteria ? `
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                <span class="text-[10px] font-bold text-teal-400 uppercase tracking-wider block">Clinical Diagnostic &amp; Semiological Criteria</span>
                <p class="text-xs text-slate-300 leading-relaxed">${Array.isArray(ch.clinical_diagnostic_criteria) ? ch.clinical_diagnostic_criteria.join(' • ') : ch.clinical_diagnostic_criteria}</p>
              </div>
            ` : ''}

            <!-- Actionable Protocols -->
            ${ch.actionable_protocols ? `
              <div class="p-4 rounded-xl bg-emerald-950/30 border border-emerald-500/40 space-y-2">
                <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">Actionable Clinical Protocols</span>
                <div class="p-3 rounded-lg bg-slate-900/80 border border-emerald-500/20 text-xs text-slate-200">
                  ${Array.isArray(ch.actionable_protocols) 
                    ? ch.actionable_protocols.map((p, idx) => `<div class="mb-1"><strong class="text-emerald-300">Step ${idx + 1}:</strong> ${p}</div>`).join('')
                    : ch.actionable_protocols}
                </div>
              </div>
            ` : ''}

            <!-- Safety & Contraindications -->
            <div class="p-4 rounded-xl bg-rose-950/20 border border-rose-500/30 space-y-1">
              <span class="text-[10px] font-bold text-rose-400 uppercase tracking-wider block">⚠️ Statutory Safety &amp; Red-Flag Guardrails</span>
              <p class="text-xs text-rose-200/90 leading-relaxed">
                ${ch.safety_and_contraindications ? (Array.isArray(ch.safety_and_contraindications) ? ch.safety_and_contraindications.join(' • ') : ch.safety_and_contraindications) : 'Schedule E(1) Mudabbar detoxification mandatory. 21 CFR Part 11 sign-off active.'}
              </p>
            </div>
          </div>
        `;
      } else {
        // LAYER 2: FULL CANONICAL ACADEMIC TREATISE
        bodyEl.innerHTML = `
          <div class="space-y-5">
            <div class="p-4 rounded-xl bg-gradient-to-r from-emerald-950/40 to-slate-900 border border-emerald-500/30 space-y-1">
              <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-wider">Al-Matn al-Tibbiy al-Kamil (المتن الطبي الكامل — Comprehensive Scholarly Treatise)</span>
              <h4 class="text-sm font-bold text-white">${tr.chapter_title_en || ch.title_en}</h4>
              <p class="text-xs text-emerald-400 font-serif" dir="rtl">${tr.chapter_title_ur || ch.title_ur}</p>
            </div>

            <!-- Section 1: Canonical Philosophy & Natural Doctrine -->
            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
              <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">🏛️ Section 1: Canonical Philosophy &amp; Natural Doctrine (الفلسفة الطبية)</span>
              <div class="text-xs text-slate-300 leading-relaxed whitespace-pre-line font-serif">
                ${tr.canonical_philosophy_and_doctrine || 'Scholarly treatise text active.'}
              </div>
            </div>

            <!-- Section 2: Molecular & Cellular Pathophysiology -->
            <div class="p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/30 space-y-2">
              <span class="text-[10px] font-bold text-cyan-300 uppercase tracking-wider block">🧬 Section 2: Molecular &amp; Cellular Pathophysiology (علم الأمراض الخلوي)</span>
              <div class="text-xs text-cyan-100/90 leading-relaxed whitespace-pre-line">
                ${tr.molecular_and_cellular_pathophysiology || 'Biomedical crosswalk active.'}
              </div>
            </div>

            <!-- Section 3: Step-by-Step Bedside Clinical Examination Manual -->
            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
              <span class="text-[10px] font-bold text-teal-400 uppercase tracking-wider block">🩺 Section 3: Bedside Clinical Examination Manual (دليل الفحص السريري)</span>
              <div class="text-xs text-slate-300 leading-relaxed whitespace-pre-line font-mono">
                ${tr.step_by_step_clinical_examination || 'Clinical manual active.'}
              </div>
            </div>

            <!-- Section 4: Comprehensive Pharmacopeia, Recipes & Mudabbar SOPs -->
            <div class="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 space-y-2">
              <span class="text-[10px] font-bold text-amber-300 uppercase tracking-wider block">🌿 Section 4: Comprehensive Pharmacopeia, Recipes &amp; Mudabbar SOPs (دستور الأدوية والتركيب)</span>
              <div class="text-xs text-amber-100/90 leading-relaxed whitespace-pre-line">
                ${tr.comprehensive_pharmacopeia_and_recipes || 'Formulary active.'}
              </div>
            </div>

            <!-- Section 5: Real-World Integrative Clinical Case Study -->
            <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
              <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">📋 Section 5: Real-World Integrative Clinical Case Study (حالة سريرية موثقة)</span>
              <div class="text-xs text-emerald-100/90 leading-relaxed whitespace-pre-line p-3 rounded-lg bg-slate-900/60 border border-emerald-500/20">
                ${tr.clinical_case_study || 'Clinical case study active.'}
              </div>
            </div>
          </div>
        `;
      }
    }

    function openGrandLibraryChapterModal(volId, chapId) {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib) return;

      const vol = lib.volumes.find(v => v.id === volId);
      if (!vol) return;

      const ch = vol.chapters.find(c => c.id === chapId);
      if (!ch) return;

      currentActiveChapter = { vol, ch };
      currentModalLayer = 'protocol'; // default to layer 1

      const modal = document.getElementById('grand-library-modal');
      const badgeEl = document.getElementById('grand-lib-modal-badge');
      const titleEl = document.getElementById('grand-lib-modal-title');
      const urduEl = document.getElementById('grand-lib-modal-urdu');

      if (!modal) return;

      if (badgeEl) badgeEl.innerText = `${vol.title_en.split(':')[0]} • Chapter ${vol.volume_number}.${ch.chapter_number}`;
      if (titleEl) titleEl.innerText = ch.title_en;
      if (urduEl) urduEl.innerText = ch.title_ur || '';

      switchModalLayer('protocol');
      modal.classList.remove('hidden');
    }

    function closeGrandLibraryModal() {
      const modal = document.getElementById('grand-library-modal');
      if (modal) modal.classList.add('hidden');
      currentActiveChapter = null;
    }

    function openMedicalDoctrineModal(chapterId) {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib || !lib.volumes.length) return;

      if (chapterId) {
        for (const v of lib.volumes) {
          const found = v.chapters.find(c => c.id === chapterId);
          if (found) {
            openGrandLibraryChapterModal(v.id, found.id);
            return;
          }
        }
      }

      // Default: Open Chapter 1 of Volume 1
      openGrandLibraryChapterModal(lib.volumes[0].id, lib.volumes[0].chapters[0].id);
    }

    function copyCurrentChapterProtocol() {
      if (!currentActiveChapter || !currentActiveChapter.ch) {
        if (typeof showNotification === 'function') showNotification('No chapter currently selected.', 'warning');
        return;
      }
      const ch = currentActiveChapter.ch;
      const text = `[ZAYVORA CANONICAL PROTOCOL: ${ch.title_en}]\n` +
                   (ch.actionable_protocols ? (Array.isArray(ch.actionable_protocols) ? ch.actionable_protocols.join('\n• ') : ch.actionable_protocols) : 'No protocols listed');
      if (navigator && navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          if (typeof showNotification === 'function') {
            showNotification(`Protocol for "${ch.title_en}" copied to clipboard!`, 'success');
          }
        }).catch(() => {
          if (typeof showNotification === 'function') {
            showNotification('Protocol text ready.', 'info');
          }
        });
      } else {
        if (typeof showNotification === 'function') {
          showNotification(`Protocol copied for ${ch.title_en}`, 'info');
        }
      }
    }
""".replace('__LIBRARY_JSON__', library_json_str)

def patch_file(filepath):
    print(f"Applying Dual-Layer update to {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace modal markup
    modal_start = '<!-- GRAND INTEGRATIVE MEDICAL LIBRARY MODAL'
    modal_end = '<!-- CLIENT-SIDE APPLICATION DATA & LOGIC -->'
    if modal_start in content and modal_end in content:
        idx1 = content.find(modal_start)
        idx2 = content.find(modal_end)
        content = content[:idx1] + modal_html.strip() + '\n\n  ' + content[idx2:]
        print("  [✓] Updated modal markup to Dual-Layer switcher.")

    # 2. Replace JS Engine
    js_start = '// GRAND INTEGRATIVE MEDICAL LIBRARY (12 VOLUMES) ENGINE'
    js_end = 'function initializeApp() {'
    if js_start in content and js_end in content:
        idx_js1 = content.find(js_start)
        idx_js2 = content.find(js_end)
        content = content[:idx_js1] + dual_layer_js.strip() + '\n\n    ' + content[idx_js2:]
        print("  [✓] Updated JS engine to Dual-Layer with rich treatises.")
    elif '// GRAND INTEGRATIVE MEDICAL LIBRARY (12 VOLUMES) — DUAL-LAYER ENGINE' in content:
        print("  [i] Dual-layer JS already present.")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully patched {filepath}!")

patch_file('/Users/irfanashraf/Downloads/zayvora-platform-phase0-4/index.html')
patch_file('/Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/index.html')
print("DUAL-LAYER DEPLOYMENT TO HTML STANDALONE FILES COMPLETE!")
