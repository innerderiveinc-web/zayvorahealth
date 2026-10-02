import sys
sys.path.insert(0, ".")
import json
from services.knowledge.app.data.grand_integrative_library_master import GRAND_INTEGRATIVE_LIBRARY

library_json_str = json.dumps(GRAND_INTEGRATIVE_LIBRARY, ensure_ascii=False)

modal_html = """
  <!-- ===================================================================== -->
  <!-- GRAND INTEGRATIVE MEDICAL LIBRARY MODAL (12 VOLUMES) -->
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
      <div id="grand-library-modal-body" class="overflow-y-auto space-y-4 pr-1 text-xs text-slate-200">
        <!-- Chapter content rendered dynamically -->
      </div>
      <div class="pt-3 border-t border-[var(--border)] flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 flex-shrink-0">
        <span class="text-[11px] text-[var(--muted)]">ZAYVORA Health OS • Canonical Medical Knowledge Base</span>
        <div class="flex gap-2">
          <button onclick="closeGrandLibraryModal()" class="px-4 py-2 rounded-xl border border-[var(--border)] text-xs text-[var(--muted)] hover:text-white">Close</button>
          <button onclick="copyCurrentChapterProtocol()" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow flex items-center gap-1.5">
            <span>Copy Protocol to Care Plan</span>
          </button>
        </div>
      </div>
    </div>
  </div>
"""

js_code = """
    // =========================================================================
    // GRAND INTEGRATIVE MEDICAL LIBRARY (12 VOLUMES) ENGINE
    // =========================================================================
    window.ZAYVORA_GRAND_LIBRARY_DATA = __LIBRARY_JSON__;
    let currentLibrarySelectedVol = 'all';
    let currentActiveChapter = null;

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
                <span class="px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 text-xs font-mono">CLASSICAL &amp; MODERN</span>
              </div>
              ${context === 'website' ? '<button onclick="viewWebsitePage(\\'home\\')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>' : ''}
            </div>
            <div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-white">ZAYVORA Grand Classical &amp; Modern Integrative Medical Library</h1>
              <p class="text-emerald-400 font-serif text-sm mt-1" dir="rtl">جامع طبی کتب خانہ — ۱۲ ابواب، روایتی کلیات، نبض، اخلاط اور جدید تشخیصی و علاجی علوم</p>
            </div>
            <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-4xl">
              The institutional theoretical and clinical doctrine of ZAYVORA Health OS. Unites Avicennian foundations (Kulliyat, 10-Ajnas Nabz, Asbab-e-Sitta, 4-Pillar Therapeutics, 1,280+ UPI monographs, Schedule E(1) Mudabbar detox) with modern clinical medicine (hs-CRP, HbA1c, Radio-Diagnostics, Ultrasound, FibroScan, Gut Metagenomics, IoT Wearables, and 21 CFR Part 11 Electronic Sealing).
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
                <span>Showing 12 Master Volumes (38 Chapters)</span>
                <span class="text-emerald-400 font-mono">Zero synthetic mock data • 100% Authentic Citations</span>
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
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Codified Chapters (${v.chapters.length})</span>
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
                  <span class="text-emerald-400 text-xs font-mono group-hover:translate-x-0.5 transition">Read →</span>
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
        if (statsEl) statsEl.innerHTML = `<span>Showing 12 Master Volumes (38 Chapters)</span><span class="text-emerald-400 font-mono">Zero synthetic mock data • 100% Authentic Citations</span>`;
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
          return ch.title_en.toLowerCase().includes(q) ||
                 ch.title_ur.toLowerCase().includes(q) ||
                 (ch.key_concepts && ch.key_concepts.some(k => k.toLowerCase().includes(q))) ||
                 (ch.classical_citations && ch.classical_citations.some(c => c.toLowerCase().includes(q))) ||
                 (ch.modern_biomedical_correlation && ch.modern_biomedical_correlation.toLowerCase().includes(q)) ||
                 (ch.clinical_diagnostic_criteria && ch.clinical_diagnostic_criteria.some(d => d.toLowerCase().includes(q))) ||
                 (ch.actionable_protocols && ch.actionable_protocols.some(p => p.toLowerCase().includes(q))) ||
                 (ch.safety_and_contraindications && ch.safety_and_contraindications.some(s => s.toLowerCase().includes(q)));
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

    function openGrandLibraryChapterModal(volId, chapId) {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib) return;

      const vol = lib.volumes.find(v => v.id === volId);
      if (!vol) return;

      const ch = vol.chapters.find(c => c.id === chapId);
      if (!ch) return;

      currentActiveChapter = { vol, ch };

      const modal = document.getElementById('grand-library-modal');
      const badgeEl = document.getElementById('grand-lib-modal-badge');
      const titleEl = document.getElementById('grand-lib-modal-title');
      const urduEl = document.getElementById('grand-lib-modal-urdu');
      const bodyEl = document.getElementById('grand-lib-modal-body');

      if (!modal || !bodyEl) return;

      badgeEl.innerText = `${vol.title_en.split(':')[0]} • Chapter ${vol.volume_number}.${ch.chapter_number}`;
      titleEl.innerText = ch.title_en;
      urduEl.innerText = ch.title_ur || '';

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
              <ul class="space-y-1.5 text-xs text-amber-100/90 list-disc list-inside">
                ${ch.classical_citations.map(c => `<li><span class="font-medium">${c}</span></li>`).join('')}
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
          ${ch.clinical_diagnostic_criteria && ch.clinical_diagnostic_criteria.length > 0 ? `
            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
              <span class="text-[10px] font-bold text-teal-400 uppercase tracking-wider block">Clinical Diagnostic &amp; Semiological Criteria</span>
              <ul class="space-y-1.5 text-xs text-slate-300 list-disc list-inside">
                ${ch.clinical_diagnostic_criteria.map(d => `<li>${d}</li>`).join('')}
              </ul>
            </div>
          ` : ''}

          <!-- Actionable Protocols -->
          ${ch.actionable_protocols && ch.actionable_protocols.length > 0 ? `
            <div class="p-4 rounded-xl bg-emerald-950/30 border border-emerald-500/40 space-y-2">
              <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">Actionable Clinical Protocols</span>
              <div class="space-y-2">
                ${ch.actionable_protocols.map((p, idx) => `
                  <div class="p-2.5 rounded-lg bg-slate-900/80 border border-emerald-500/20 text-xs text-slate-200">
                    <strong class="text-emerald-300 block mb-1">Protocol Step ${idx + 1}:</strong>
                    <span>${p}</span>
                  </div>
                `).join('')}}
              </div>
            </div>
          ` : ''}

          <!-- Safety, Contraindications & Red Flags -->
          ${ch.safety_and_contraindications && ch.safety_and_contraindications.length > 0 ? `
            <div class="p-4 rounded-xl bg-rose-950/20 border border-rose-500/30 space-y-2">
              <span class="text-[10px] font-bold text-rose-400 uppercase tracking-wider block">Safety Guardrails, Contraindications &amp; Red-Flags</span>
              <ul class="space-y-1 text-xs text-rose-200/90 list-disc list-inside">
                ${ch.safety_and_contraindications.map(s => `<li>${s}</li>`).join('')}
              </ul>
            </div>
          ` : ''}
        </div>
      `;

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
                   (ch.actionable_protocols ? ch.actionable_protocols.join('\n• ') : 'No protocols listed');
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
    print(f"Patching {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert Modal Markup if not present
    if 'id="grand-library-modal"' not in content:
        target = '<!-- CLIENT-SIDE APPLICATION DATA & LOGIC -->'
        if target in content:
            content = content.replace(target, modal_html + '\n  ' + target)
            print("  [✓] Inserted grand-library-modal markup.")

    # 2. Insert Doctor Desk Header Button if not present
    doc_btn_pattern = 'onclick="toggleHakeemDrawer(true)"'
    if doc_btn_pattern in content and 'openMedicalDoctrineModal()' not in content:
        idx = content.find(doc_btn_pattern)
        end_btn_idx = content.find('</button>', idx)
        if end_btn_idx != -1:
            insertion = """
              <button onclick="openMedicalDoctrineModal()" class="px-3.5 py-2 rounded-xl bg-emerald-600/20 border border-emerald-500/40 text-emerald-300 text-xs font-bold hover:bg-emerald-600/30 flex items-center gap-1.5 transition" title="12-Volume Classical & Modern Integrative Medical Library">
                <svg class="w-4 h-4 inline-block text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg> 📖 Medical Doctrine Library
              </button>"""
            content = content[:end_btn_idx + 9] + insertion + content[end_btn_idx + 9:]
            print("  [✓] Inserted Medical Doctrine Library button in doctor header.")

    # 3. Insert JS Logic & Data if not present
    if 'window.ZAYVORA_GRAND_LIBRARY_DATA' not in content:
        target_js = 'function initializeApp() {'
        if target_js in content:
            content = content.replace(target_js, js_code + '\n    ' + target_js)
            print("  [✓] Inserted Grand Library engine JS logic.")

    # 4. Update state.tab === 'knowledge' in renderWebsiteApp
    old_website_knowledge_pattern = 'if (state.tab === \'knowledge\') {\n        container.innerHTML = `\n          <div class="max-w-5xl mx-auto space-y-8 pb-12">'
    
    if old_website_knowledge_pattern in content:
        idx = content.find(old_website_knowledge_pattern)
        end_return_idx = content.find('return;\n      }', idx)
        if end_return_idx != -1:
            replacement = """if (state.tab === 'knowledge') {
        renderGrandLibrary(container, 'website');
        return;
      }"""
            content = content[:idx] + replacement + content[end_return_idx + 15:]
            print("  [✓] Replaced renderWebsiteApp knowledge tab with renderGrandLibrary.")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully patched {filepath}!")

patch_file('/Users/irfanashraf/Downloads/zayvora-platform-phase0-4/index.html')
patch_file('/Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/index.html')
print("ALL FILES PATCHED SUCCESSFULLY!")
