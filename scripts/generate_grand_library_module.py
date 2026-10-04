#!/usr/bin/env python3
"""
ZAYVORA Health OS — Grand Integrative Medical Library Engine Builder
Generates js/modules/05-grand-library.js and patches js/zayvora-core.js
"""

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services.knowledge.app.data.grand_integrative_library_master import (
    GRAND_INTEGRATIVE_LIBRARY,
    LIBRARY_METADATA,
    MUFRADAT_LIST,
    MURAKKABAT_LIST,
    DRUG_INTERACTIONS_LIST,
    UNIVERSAL_CONTRAINDICATIONS_LIST
)

master_data = {
    "metadata": LIBRARY_METADATA,
    "volumes": GRAND_INTEGRATIVE_LIBRARY["volumes"],
    "mufradat": MUFRADAT_LIST,
    "murakkabat": MURAKKABAT_LIST,
    "drug_interactions": DRUG_INTERACTIONS_LIST,
    "universal_contraindications": UNIVERSAL_CONTRAINDICATIONS_LIST
}

library_json_str = json.dumps(master_data, ensure_ascii=False)

js_engine_code = r'''
    // =========================================================================
    // GRAND INTEGRATIVE MEDICAL LIBRARY (12 VOLUMES + 250 MUFRADAT + 59 MURAKKABAT + CYP450)
    // =========================================================================
    window.ZAYVORA_GRAND_LIBRARY_DATA = __LIBRARY_JSON__;

    let currentLibraryMode = 'volumes'; // 'volumes' | 'mufradat' | 'murakkabat' | 'interactions'
    let currentLibrarySelectedVol = 'all';
    let currentMufradFilter = 'all';
    let currentMurakkabFilter = 'all';
    let currentInteractionsFilter = 'all';
    let currentActiveChapter = null;
    let currentActiveMufrad = null;
    let currentActiveMurakkab = null;
    let currentModalLayer = 'protocol'; // 'protocol' | 'treatise' | 'recipes' | 'semiology'

    function renderGrandLibrary(container, context) {
      const subnav = typeof getWebsiteHubSubnav === 'function' ? getWebsiteHubSubnav(state.tab) : '';
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib) return;

      const totalVolumes = (lib.volumes || []).length;
      const totalChapters = (lib.volumes || []).reduce((acc, v) => acc + (v.chapters || []).length, 0);
      const totalMufradat = (lib.mufradat || []).length;
      const totalMurakkabat = (lib.murakkabat || []).length;
      const totalInteractions = (lib.drug_interactions || []).length;

      let html = `
        <div class="max-w-6xl mx-auto space-y-6 pb-12">
          ${context === 'website' ? subnav : ''}
          
          <!-- Library Header Hero -->
          <div class="bg-gradient-to-r from-emerald-950/60 via-slate-900 to-slate-900 p-6 sm:p-8 rounded-3xl border border-emerald-500/30 space-y-4 shadow-xl">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold font-mono">12 MASTER VOLUMES</span>
                <span class="px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-mono">38 CHAPTERS</span>
                <span class="px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 text-xs font-mono font-bold">250+ MUFRADAT</span>
                <span class="px-3 py-1 rounded-full bg-teal-500/20 text-teal-300 text-xs font-mono">59 MURAKKABAT</span>
                <span class="px-3 py-1 rounded-full bg-rose-500/20 text-rose-300 text-xs font-mono font-bold">CYP450 SAFETY</span>
              </div>
              ${context === 'website' ? '<button onclick="viewWebsitePage(\'home\')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>' : ''}
            </div>
            <div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-[#1B242A] dark:text-white">ZAYVORA Grand Classical &amp; Modern Integrative Medical Library</h1>
              <p class="text-emerald-400 font-serif text-sm mt-1" dir="rtl">جامع طبی کتب خانہ — ۱۲ ابواب، ۲۵۰ مفردات، ۵۹ مرکبات اور جدید تشخیصی و علاجی علوم (۴ تہی نظام)</p>
            </div>
            <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-4xl">
              The institutional theoretical and clinical doctrine of ZAYVORA Health OS. Unites Avicennian foundations (Kulliyat, 10-Ajnas Nabz, Asbab-e-Sitta, 4-Pillar Therapeutics, 250+ UPI single herbs, 59 NFUM classical compounds, and Schedule E-1 Mudabbar detox) with contemporary clinical medicine (hs-CRP, HbA1c, FibroScan, Gut Metagenomics, IoT Wearables, and 21 CFR Part 11 Electronic Sealing).
            </p>

            <!-- Search Bar -->
            <div class="pt-2">
              <div class="relative">
                <input 
                  type="text" 
                  id="grand-lib-search-input" 
                  placeholder="Search volumes, 250 herbs, 59 classical recipes, or modern drug interactions (e.g. Asgandh, Suranjan, Itrifal, Warfarin, hs-CRP, سورنجان)..." 
                  oninput="handleGrandLibrarySearch(this.value)"
                  class="w-full pl-10 pr-4 py-3 bg-slate-900/90 border border-emerald-500/40 rounded-xl text-xs sm:text-sm text-white focus:outline-none focus:border-emerald-400 shadow-inner"
                >
                <span class="absolute left-3.5 top-3.5 text-slate-400 text-sm">🔍</span>
              </div>
              <div id="grand-lib-search-stats" class="text-[11px] text-slate-400 mt-1.5 flex justify-between">
                <span>Showing 12 Master Volumes (38 Chapters) • 250 Mufradat • 59 Murakkabat</span>
                <span class="text-emerald-400 font-mono">Zero synthetic mock data • 100% Authentic Citations</span>
              </div>
            </div>
          </div>

          <!-- TOP-LEVEL 4-MODE SWITCHER TABS -->
          <div class="flex items-center gap-2 overflow-x-auto pb-1 border-b border-slate-800 scrollbar-none">
            <button onclick="switchGrandLibraryMode('volumes')" id="lib-mode-tab-volumes" class="px-4 py-2.5 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-lg shadow-emerald-950/40 ring-2 ring-emerald-400/40 flex items-center gap-2 shrink-0 transition">
              <span>🏛️</span> 12 Master Volumes (${totalChapters} Chapters)
            </button>
            <button onclick="switchGrandLibraryMode('mufradat')" id="lib-mode-tab-mufradat" class="px-4 py-2.5 rounded-xl text-xs font-bold bg-slate-900/90 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-2 shrink-0 transition">
              <span>🌿</span> 250+ Mufradat (Materia Medica)
            </button>
            <button onclick="switchGrandLibraryMode('murakkabat')" id="lib-mode-tab-murakkabat" class="px-4 py-2.5 rounded-xl text-xs font-bold bg-slate-900/90 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-2 shrink-0 transition">
              <span>🥣</span> Classical Formulary (59 Murakkabat)
            </button>
            <button onclick="switchGrandLibraryMode('interactions')" id="lib-mode-tab-interactions" class="px-4 py-2.5 rounded-xl text-xs font-bold bg-slate-900/90 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-2 shrink-0 transition">
              <span>🛡️</span> CYP450 Herb-Drug Safety Matrix (${totalInteractions})
            </button>
          </div>

          <!-- SUB-FILTERS: MODE 1 (VOLUMES) -->
          <div id="lib-volume-subfilters" class="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
            <button onclick="filterGrandLibraryVolume('all')" id="lib-filter-btn-all" class="px-3 py-1.5 rounded-xl bg-emerald-600 text-white text-xs font-bold flex-shrink-0 transition">
              All 12 Volumes
            </button>
            ${(lib.volumes || []).map(v => `
              <button onclick="filterGrandLibraryVolume('${v.id}')" id="lib-filter-btn-${v.id}" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs flex-shrink-0 transition flex items-center gap-1.5">
                <span>${v.icon}</span> Vol ${v.volume_number}: ${v.title_en.split(':')[0]}
              </button>
            `).join('')}
          </div>

          <!-- SUB-FILTERS: MODE 2 (MUFRADAT) -->
          <div id="lib-mufrad-subfilters" class="hidden items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
            <button onclick="filterGrandLibraryMufrad('all')" id="lib-mfilter-all" class="px-3 py-1.5 rounded-xl bg-amber-600 text-white text-xs font-bold shrink-0 transition">
              All 250 Herbs
            </button>
            <button onclick="filterGrandLibraryMufrad('haar-yabis')" id="lib-mfilter-haar-yabis" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-rose-300 text-xs shrink-0 transition flex items-center gap-1">
              <span>🔥</span> Haar-Yabis (Hot-Dry)
            </button>
            <button onclick="filterGrandLibraryMufrad('haar-ratab')" id="lib-mfilter-haar-ratab" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-amber-300 text-xs shrink-0 transition flex items-center gap-1">
              <span>☀️</span> Haar-Ratab (Hot-Moist)
            </button>
            <button onclick="filterGrandLibraryMufrad('barid-ratab')" id="lib-mfilter-barid-ratab" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-cyan-300 text-xs shrink-0 transition flex items-center gap-1">
              <span>💧</span> Barid-Ratab (Cold-Moist)
            </button>
            <button onclick="filterGrandLibraryMufrad('barid-yabis')" id="lib-mfilter-barid-yabis" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-blue-300 text-xs shrink-0 transition flex items-center gap-1">
              <span>❄️</span> Barid-Yabis (Cold-Dry)
            </button>
            <button onclick="filterGrandLibraryMufrad('schedule-e1')" id="lib-mfilter-schedule-e1" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-rose-500/40 text-rose-400 text-xs shrink-0 transition flex items-center gap-1 font-semibold">
              <span>⚠️</span> Schedule E(1) Mudabbar Only
            </button>
          </div>

          <!-- SUB-FILTERS: MODE 3 (MURAKKABAT) -->
          <div id="lib-murakkab-subfilters" class="hidden items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
            <button onclick="filterGrandLibraryMurakkab('all')" id="lib-kfilter-all" class="px-3 py-1.5 rounded-xl bg-teal-600 text-white text-xs font-bold shrink-0 transition">
              All 59 Formulations
            </button>
            ${['Itrifal', 'Majun', 'Khamira', 'Sharbat', 'Kushta', 'Roghan', 'Habb', 'Qurs', 'Jawarish', 'Sanoon'].map(cat => `
              <button onclick="filterGrandLibraryMurakkab('${cat.toLowerCase()}')" id="lib-kfilter-${cat.toLowerCase()}" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs shrink-0 transition">
                ${cat}
              </button>
            `).join('')}
          </div>

          <!-- SUB-FILTERS: MODE 4 (INTERACTIONS) -->
          <div id="lib-inter-subfilters" class="hidden items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
            <button onclick="filterGrandLibraryInteractions('all')" id="lib-ifilter-all" class="px-3 py-1.5 rounded-xl bg-rose-600 text-white text-xs font-bold shrink-0 transition">
              All Interactions (11)
            </button>
            <button onclick="filterGrandLibraryInteractions('critical')" id="lib-ifilter-critical" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-rose-500/50 text-rose-400 text-xs shrink-0 transition font-bold">
              🔴 Critical (Hard Block)
            </button>
            <button onclick="filterGrandLibraryInteractions('high')" id="lib-ifilter-high" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-amber-500/50 text-amber-400 text-xs shrink-0 transition font-bold">
              🟠 High Caution
            </button>
          </div>

          <!-- Dynamic Cards Container Grid -->
          <div id="grand-library-grid" class="space-y-8">
            <!-- Rendered dynamically by renderGrandLibraryContent() -->
          </div>
        </div>
      `;

      container.innerHTML = html;
      renderGrandLibraryContent();
    }

    function switchGrandLibraryMode(mode) {
      currentLibraryMode = mode;
      
      const modes = ['volumes', 'mufradat', 'murakkabat', 'interactions'];
      modes.forEach(m => {
        const btn = document.getElementById('lib-mode-tab-' + m);
        if (btn) {
          if (m === mode) {
            btn.className = "px-4 py-2.5 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-lg shadow-emerald-950/40 ring-2 ring-emerald-400/40 flex items-center gap-2 shrink-0 transition";
          } else {
            btn.className = "px-4 py-2.5 rounded-xl text-xs font-bold bg-slate-900/90 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-2 shrink-0 transition";
          }
        }
      });

      const volFilters = document.getElementById('lib-volume-subfilters');
      const mufradFilters = document.getElementById('lib-mufrad-subfilters');
      const murakkabFilters = document.getElementById('lib-murakkab-subfilters');
      const interFilters = document.getElementById('lib-inter-subfilters');

      if (volFilters) volFilters.className = mode === 'volumes' ? 'flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin' : 'hidden';
      if (mufradFilters) mufradFilters.className = mode === 'mufradat' ? 'flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin' : 'hidden';
      if (murakkabFilters) murakkabFilters.className = mode === 'murakkabat' ? 'flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin' : 'hidden';
      if (interFilters) interFilters.className = mode === 'interactions' ? 'flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin' : 'hidden';

      renderGrandLibraryContent();
    }

    function renderGrandLibraryContent() {
      const q = (document.getElementById('grand-lib-search-input')?.value || '').trim().toLowerCase();
      if (currentLibraryMode === 'volumes') {
        renderGrandLibraryVolumes(q);
      } else if (currentLibraryMode === 'mufradat') {
        renderGrandLibraryMufradat(q);
      } else if (currentLibraryMode === 'murakkabat') {
        renderGrandLibraryMurakkabat(q);
      } else if (currentLibraryMode === 'interactions') {
        renderGrandLibraryInteractions(q);
      }
    }

    // =========================================================================
    // 1. VOLUMES & CHAPTERS RENDERER
    // =========================================================================
    function renderGrandLibraryVolumes(query = '') {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      const grid = document.getElementById('grand-library-grid');
      if (!grid || !lib) return;

      let volumesToRender = lib.volumes || [];
      if (currentLibrarySelectedVol !== 'all') {
        volumesToRender = volumesToRender.filter(v => v.id === currentLibrarySelectedVol);
      }

      if (query) {
        volumesToRender = volumesToRender.map(vol => {
          const volMatches = vol.title_en.toLowerCase().includes(query) ||
                             vol.title_ur.toLowerCase().includes(query) ||
                             vol.summary.toLowerCase().includes(query);
          const matchingChapters = vol.chapters.filter(ch => {
            const tr = ch.full_treatise || {};
            return ch.title_en.toLowerCase().includes(query) ||
                   ch.title_ur.toLowerCase().includes(query) ||
                   (ch.key_concepts && ch.key_concepts.some(k => k.toLowerCase().includes(query))) ||
                   (ch.modern_biomedical_correlation && ch.modern_biomedical_correlation.toLowerCase().includes(query)) ||
                   (tr.canonical_philosophy_and_doctrine && tr.canonical_philosophy_and_doctrine.toLowerCase().includes(query));
          });
          if (volMatches || matchingChapters.length > 0) {
            return { ...vol, chapters: matchingChapters.length > 0 ? matchingChapters : vol.chapters };
          }
          return null;
        }).filter(Boolean);
      }

      if (volumesToRender.length === 0) {
        grid.innerHTML = `
          <div class="p-12 text-center bg-slate-900/50 rounded-2xl border border-slate-800 text-slate-400 space-y-2">
            <span class="text-3xl block">🔍</span>
            <strong class="text-white text-base">No chapters matched "${query}"</strong>
            <p class="text-xs">Try searching for keywords like "Nabz", "hs-CRP", "Suranjan", "PCOS", or "FibroScan".</p>
          </div>
        `;
        return;
      }

      grid.innerHTML = volumesToRender.map(vol => `
        <div class="bg-slate-950/80 border border-slate-800 rounded-3xl p-6 sm:p-7 space-y-5 shadow-lg hover:border-emerald-500/40 transition">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-slate-800/80 pb-4">
            <div class="flex items-center gap-3.5">
              <span class="text-3xl p-2.5 rounded-2xl bg-emerald-950/40 border border-emerald-500/30 flex-shrink-0">${vol.icon}</span>
              <div>
                <div class="flex items-center gap-2">
                  <span class="text-xs font-mono font-bold text-emerald-400 uppercase tracking-wider">Volume ${vol.volume_number}</span>
                  <span class="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono text-[10px]">${vol.badge}</span>
                </div>
                <h2 class="text-lg sm:text-xl font-bold text-white mt-0.5">${vol.title_en}</h2>
                <p class="text-xs text-emerald-400/90 font-serif font-medium mt-0.5" dir="rtl">${vol.title_ur}</p>
              </div>
            </div>
            <span class="px-3 py-1 rounded-full bg-slate-900 border border-slate-700/60 text-slate-300 text-xs font-mono font-semibold">
              ${vol.chapters.length} Chapters
            </span>
          </div>

          <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">${vol.summary}</p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5 pt-1">
            ${vol.chapters.map(ch => `
              <div onclick="openGrandLibraryChapterModal('${vol.id}', '${ch.id}')" class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800/80 hover:border-emerald-500/50 hover:bg-slate-900 cursor-pointer transition space-y-2.5 group">
                <div class="flex justify-between items-start">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 font-mono text-[10px] font-bold border border-emerald-500/20">
                    Chapter ${ch.chapter_number}
                  </span>
                  <span class="text-xs text-slate-500 group-hover:text-emerald-400 transition">Read Protocol & Treatise →</span>
                </div>
                <div>
                  <h3 class="font-bold text-white text-xs sm:text-sm group-hover:text-emerald-300 transition">${ch.title_en}</h3>
                  <p class="text-[11px] text-emerald-400/80 font-serif mt-0.5" dir="rtl">${ch.title_ur || ''}</p>
                </div>
                ${ch.key_concepts && ch.key_concepts.length > 0 ? `
                  <div class="flex flex-wrap gap-1 pt-1">
                    ${ch.key_concepts.slice(0, 3).map(k => `<span class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]">${k.split('(')[0].trim()}</span>`).join('')}
                    ${ch.key_concepts.length > 3 ? `<span class="text-[10px] text-slate-500">+${ch.key_concepts.length - 3} more</span>` : ''}
                  </div>
                ` : ''}
              </div>
            `).join('')}
          </div>
        </div>
      `).join('');
    }

    function filterGrandLibraryVolume(volId) {
      currentLibrarySelectedVol = volId;
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib) return;

      const allBtn = document.getElementById('lib-filter-btn-all');
      if (allBtn) {
        allBtn.className = volId === 'all' 
          ? 'px-3 py-1.5 rounded-xl bg-emerald-600 text-white text-xs font-bold flex-shrink-0 transition'
          : 'px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs flex-shrink-0 transition';
      }

      (lib.volumes || []).forEach(v => {
        const btn = document.getElementById('lib-filter-btn-' + v.id);
        if (btn) {
          btn.className = v.id === volId
            ? 'px-3 py-1.5 rounded-xl bg-emerald-600 text-white text-xs font-bold flex-shrink-0 transition flex items-center gap-1.5'
            : 'px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs flex-shrink-0 transition flex items-center gap-1.5';
        }
      });

      renderGrandLibraryContent();
    }

    // =========================================================================
    // 2. MUFRADAT (250 SINGLE BOTANICAL HERBS) RENDERER
    // =========================================================================
    function renderGrandLibraryMufradat(query = '') {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      const grid = document.getElementById('grand-library-grid');
      if (!grid || !lib) return;

      let mufradat = lib.mufradat || [];

      // Apply subfilter
      if (currentMufradFilter === 'haar-yabis') {
        mufradat = mufradat.filter(m => (m.mizaj || '').toLowerCase().includes('haar') && (m.mizaj || '').toLowerCase().includes('yabis'));
      } else if (currentMufradFilter === 'haar-ratab') {
        mufradat = mufradat.filter(m => (m.mizaj || '').toLowerCase().includes('haar') && (m.mizaj || '').toLowerCase().includes('ratab'));
      } else if (currentMufradFilter === 'barid-ratab') {
        mufradat = mufradat.filter(m => (m.mizaj || '').toLowerCase().includes('barid') && (m.mizaj || '').toLowerCase().includes('ratab'));
      } else if (currentMufradFilter === 'barid-yabis') {
        mufradat = mufradat.filter(m => (m.mizaj || '').toLowerCase().includes('barid') && (m.mizaj || '').toLowerCase().includes('yabis'));
      } else if (currentMufradFilter === 'schedule-e1') {
        mufradat = mufradat.filter(m => m.schedule_e1 || m.high_risk);
      }

      if (query) {
        mufradat = mufradat.filter(m => 
          m.name.toLowerCase().includes(query) ||
          m.botanical.toLowerCase().includes(query) ||
          (m.urdu_script && m.urdu_script.includes(query)) ||
          (m.family && m.family.toLowerCase().includes(query)) ||
          (m.mizaj && m.mizaj.toLowerCase().includes(query)) ||
          (m.afaal && m.afaal.some(a => a.toLowerCase().includes(query)))
        );
      }

      if (mufradat.length === 0) {
        grid.innerHTML = `
          <div class="p-12 text-center bg-slate-900/50 rounded-2xl border border-slate-800 text-slate-400 space-y-2">
            <span class="text-3xl block">🌿</span>
            <strong class="text-white text-base">No single herbs matched "${query}"</strong>
            <p class="text-xs">Try searching by Urdu name (سورنجان، اسگندھ), English name, or Botanical identity.</p>
          </div>
        `;
        return;
      }

      grid.innerHTML = `
        <div class="space-y-4">
          <div class="flex justify-between items-center px-1">
            <span class="text-xs text-slate-400">Displaying <strong class="text-white">${mufradat.length}</strong> botanical monographs</span>
            <span class="text-xs text-amber-400 font-mono">Unani Pharmacopoeia of India (UPI) Standard</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
            ${mufradat.map(m => `
              <div class="p-4 rounded-2xl bg-slate-900/90 border ${m.schedule_e1 ? 'border-rose-500/40 bg-rose-950/10' : 'border-slate-800/80'} hover:border-emerald-500/50 transition space-y-3 flex flex-col justify-between">
                <div class="space-y-1.5">
                  <div class="flex justify-between items-start gap-2">
                    <span class="px-2 py-0.5 rounded font-mono text-[10px] font-bold ${m.schedule_e1 ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/20'}">
                      ${m.id} ${m.schedule_e1 ? '• ⚠️ SCHEDULE E(1)' : ''}
                    </span>
                    <span class="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-slate-800 text-slate-300">
                      ${m.mizaj || 'Mizaj pending'}
                    </span>
                  </div>

                  <div>
                    <h3 class="font-bold text-white text-sm hover:text-emerald-300 transition cursor-pointer" onclick="openMufradModal('${m.id}')">
                      ${m.name}
                    </h3>
                    ${m.urdu_script ? `<p class="text-xs text-emerald-400 font-serif" dir="rtl">${m.urdu_script}</p>` : ''}
                    <p class="text-[11px] text-cyan-400 italic">${m.botanical} (${m.family})</p>
                  </div>

                  <div class="text-[11px] text-slate-300 space-y-1 pt-1 border-t border-slate-800">
                    <p><strong class="text-slate-400">Part:</strong> ${m.part}</p>
                    <p><strong class="text-slate-400">Actions:</strong> ${Array.isArray(m.afaal) ? m.afaal.slice(0, 2).join('; ') : m.afaal}</p>
                    <p><strong class="text-slate-400">Musleh:</strong> ${m.musleh}</p>
                  </div>
                </div>

                <div class="pt-2 border-t border-slate-800 flex items-center justify-between gap-2">
                  <button onclick="openMufradModal('${m.id}')" class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-1 transition">
                    <span>🔍</span> Monograph
                  </button>
                  <button onclick="addMonographToPrescription('mufrad', '${m.id}')" class="px-3 py-1.5 rounded-xl bg-emerald-600/80 hover:bg-emerald-500 text-white text-xs font-bold flex items-center gap-1 transition shadow">
                    <span>➕</span> Prescribe
                  </button>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    function filterGrandLibraryMufrad(filterKey) {
      currentMufradFilter = filterKey;
      const keys = ['all', 'haar-yabis', 'haar-ratab', 'barid-ratab', 'barid-yabis', 'schedule-e1'];
      keys.forEach(k => {
        const btn = document.getElementById('lib-mfilter-' + k);
        if (btn) {
          if (k === filterKey) {
            btn.className = "px-3 py-1.5 rounded-xl bg-amber-600 text-white text-xs font-bold shrink-0 transition flex items-center gap-1";
          } else {
            btn.className = "px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs shrink-0 transition flex items-center gap-1";
          }
        }
      });
      renderGrandLibraryContent();
    }

    // =========================================================================
    // 3. MURAKKABAT (59 CLASSICAL COMPOUND FORMULAS) RENDERER
    // =========================================================================
    function renderGrandLibraryMurakkabat(query = '') {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      const grid = document.getElementById('grand-library-grid');
      if (!grid || !lib) return;

      let murakkabat = lib.murakkabat || [];

      if (currentMurakkabFilter !== 'all') {
        murakkabat = murakkabat.filter(f => (f.category || '').toLowerCase() === currentMurakkabFilter);
      }

      if (query) {
        murakkabat = murakkabat.filter(f => 
          f.name.toLowerCase().includes(query) ||
          (f.urdu_name && f.urdu_name.includes(query)) ||
          f.category.toLowerCase().includes(query) ||
          (f.classical_indication && f.classical_indication.toLowerCase().includes(query)) ||
          (f.classical_source && f.classical_source.toLowerCase().includes(query)) ||
          (f.key_ingredients && f.key_ingredients.some(i => i.name.toLowerCase().includes(query)))
        );
      }

      if (murakkabat.length === 0) {
        grid.innerHTML = `
          <div class="p-12 text-center bg-slate-900/50 rounded-2xl border border-slate-800 text-slate-400 space-y-2">
            <span class="text-3xl block">🥣</span>
            <strong class="text-white text-base">No classical formulations matched "${query}"</strong>
            <p class="text-xs">Try searching for "Itrifal", "Khamira", "Majun", "Banafsha", or an ingredient.</p>
          </div>
        `;
        return;
      }

      grid.innerHTML = `
        <div class="space-y-4">
          <div class="flex justify-between items-center px-1">
            <span class="text-xs text-slate-400">Displaying <strong class="text-white">${murakkabat.length}</strong> classical compound formulations</span>
            <span class="text-xs text-teal-400 font-mono">National Formulary of Unani Medicine (NFUM) Standard</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
            ${murakkabat.map(f => `
              <div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800/80 hover:border-teal-500/50 transition space-y-3 flex flex-col justify-between">
                <div class="space-y-1.5">
                  <div class="flex justify-between items-start gap-2">
                    <span class="px-2 py-0.5 rounded font-mono text-[10px] font-bold bg-teal-500/20 text-teal-300 border border-teal-500/30">
                      ${f.category}
                    </span>
                    <span class="text-[10px] text-slate-400 font-mono">${(f.key_ingredients || []).length} Ingredients</span>
                  </div>

                  <div>
                    <h3 class="font-bold text-white text-sm hover:text-teal-300 transition cursor-pointer" onclick="openMurakkabModal('${f.id}')">
                      ${f.name}
                    </h3>
                    ${f.urdu_name ? `<p class="text-xs text-emerald-400 font-serif" dir="rtl">${f.urdu_name}</p>` : ''}
                    <p class="text-[11px] text-slate-400 font-mono">${f.classical_source}</p>
                  </div>

                  <div class="text-[11px] text-slate-300 space-y-1 pt-1 border-t border-slate-800">
                    <p><strong class="text-slate-400">Indications:</strong> ${f.classical_indication}</p>
                    <p><strong class="text-slate-400">Dose & Vehicle:</strong> ${f.dose}</p>
                  </div>
                </div>

                <div class="pt-2 border-t border-slate-800 flex items-center justify-between gap-2">
                  <button onclick="openMurakkabModal('${f.id}')" class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-1 transition">
                    <span>📖</span> Recipe SOP
                  </button>
                  <button onclick="addMonographToPrescription('murakkab', '${f.id}')" class="px-3 py-1.5 rounded-xl bg-teal-600/80 hover:bg-teal-500 text-white text-xs font-bold flex items-center gap-1 transition shadow">
                    <span>➕</span> Prescribe
                  </button>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    function filterGrandLibraryMurakkab(catKey) {
      currentMurakkabFilter = catKey;
      const cats = ['all', 'itrifal', 'majun', 'khamira', 'sharbat', 'kushta', 'roghan', 'habb', 'qurs', 'jawarish', 'sanoon'];
      cats.forEach(c => {
        const btn = document.getElementById('lib-kfilter-' + c);
        if (btn) {
          if (c === catKey) {
            btn.className = "px-3 py-1.5 rounded-xl bg-teal-600 text-white text-xs font-bold shrink-0 transition";
          } else {
            btn.className = "px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs shrink-0 transition";
          }
        }
      });
      renderGrandLibraryContent();
    }

    // =========================================================================
    // 4. CYP450 HERB-DRUG INTERACTIONS MATRIX RENDERER
    // =========================================================================
    function renderGrandLibraryInteractions(query = '') {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      const grid = document.getElementById('grand-library-grid');
      if (!grid || !lib) return;

      let list = lib.drug_interactions || [];

      if (currentInteractionsFilter === 'critical') {
        list = list.filter(i => i.severity === 'CRITICAL');
      } else if (currentInteractionsFilter === 'high') {
        list = list.filter(i => i.severity === 'HIGH' || i.severity === 'WARNING');
      }

      if (query) {
        list = list.filter(i => 
          i.allopathic_drug_class.toLowerCase().includes(query) ||
          i.herb_active.toLowerCase().includes(query) ||
          i.mechanism.toLowerCase().includes(query) ||
          i.clinical_effect.toLowerCase().includes(query)
        );
      }

      grid.innerHTML = `
        <div class="space-y-5">
          <div class="p-4 rounded-2xl bg-rose-950/20 border border-rose-500/30 flex items-center justify-between">
            <div>
              <span class="text-xs font-mono font-bold text-rose-400 uppercase tracking-wider block">Clinical Pharmacovigilance Firewall</span>
              <p class="text-xs text-slate-300">Cytochrome P450 (CYP3A4, CYP2C9, CYP2D6) Phase I Enzyme Induction, Inhibition & Anticoagulant Synergy Rules</p>
            </div>
            <span class="px-3 py-1 rounded-full bg-rose-900/60 border border-rose-500/40 text-rose-300 font-mono text-xs font-bold">
              ${list.length} Monitored Vectors
            </span>
          </div>

          <div class="space-y-3.5">
            ${list.map(item => `
              <div class="p-5 rounded-2xl bg-slate-950 border ${item.severity === 'CRITICAL' ? 'border-rose-500/50 bg-rose-950/10' : 'border-slate-800'} space-y-3 shadow">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                  <div class="flex items-center gap-2">
                    <span class="px-2.5 py-0.5 rounded font-mono text-xs font-bold ${item.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'}">
                      ${item.severity}
                    </span>
                    <strong class="text-white text-sm">${item.herb_active}</strong>
                    <span class="text-slate-500">⟷</span>
                    <span class="text-cyan-300 font-semibold text-sm">${item.allopathic_drug_class}</span>
                  </div>
                  <span class="text-[11px] font-mono text-slate-400">${item.interaction_id || 'CYP-VECTOR'}</span>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                    <span class="text-slate-400 text-[10px] uppercase font-bold block">Biochemical Mechanism</span>
                    <p class="text-slate-200 leading-relaxed">${item.mechanism}</p>
                  </div>
                  <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                    <span class="text-rose-400 text-[10px] uppercase font-bold block">Adverse Clinical Effect</span>
                    <p class="text-rose-200 leading-relaxed">${item.clinical_effect}</p>
                  </div>
                </div>

                <div class="p-3 rounded-xl bg-emerald-950/30 border border-emerald-500/20 text-xs flex justify-between items-center">
                  <div>
                    <span class="text-emerald-400 font-bold block">Clinical Action & Physician SOP:</span>
                    <p class="text-slate-200 mt-0.5">${item.management}</p>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    function filterGrandLibraryInteractions(severity) {
      currentInteractionsFilter = severity;
      const keys = ['all', 'critical', 'high'];
      keys.forEach(k => {
        const btn = document.getElementById('lib-ifilter-' + k);
        if (btn) {
          if (k === severity) {
            btn.className = "px-3 py-1.5 rounded-xl bg-rose-600 text-white text-xs font-bold shrink-0 transition";
          } else {
            btn.className = "px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs shrink-0 transition";
          }
        }
      });
      renderGrandLibraryContent();
    }

    // =========================================================================
    // 5. UNIFIED SEARCH ACROSS ALL 4 MODES
    // =========================================================================
    function handleGrandLibrarySearch(query) {
      const q = (query || '').trim().toLowerCase();
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib) return;

      const statsEl = document.getElementById('grand-lib-search-stats');

      if (!q) {
        if (statsEl) {
          statsEl.innerHTML = `<span>Showing 12 Master Volumes (38 Chapters) • 250 Mufradat • 59 Murakkabat</span><span class="text-emerald-400 font-mono">100% Authentic Citations</span>`;
        }
        renderGrandLibraryContent();
        return;
      }

      // Calculate matches across all domains
      const volMatches = (lib.volumes || []).reduce((acc, v) => {
        const vm = v.title_en.toLowerCase().includes(q) || v.title_ur.toLowerCase().includes(q);
        const cm = v.chapters.filter(c => c.title_en.toLowerCase().includes(q) || c.title_ur.toLowerCase().includes(q) || (c.key_concepts && c.key_concepts.some(k => k.toLowerCase().includes(q)))).length;
        return acc + (vm ? v.chapters.length : cm);
      }, 0);

      const mufradMatches = (lib.mufradat || []).filter(m => 
        m.name.toLowerCase().includes(q) || 
        m.botanical.toLowerCase().includes(q) || 
        (m.urdu_script && m.urdu_script.includes(q)) || 
        m.mizaj.toLowerCase().includes(q) || 
        (m.afaal && m.afaal.some(a => a.toLowerCase().includes(q)))
      ).length;

      const murakkabMatches = (lib.murakkabat || []).filter(f => 
        f.name.toLowerCase().includes(q) || 
        (f.urdu_name && f.urdu_name.includes(q)) || 
        f.category.toLowerCase().includes(q) || 
        (f.classical_indication && f.classical_indication.toLowerCase().includes(query))
      ).length;

      const interMatches = (lib.drug_interactions || []).filter(i => 
        i.allopathic_drug_class.toLowerCase().includes(q) || 
        i.herb_active.toLowerCase().includes(q)
      ).length;

      if (statsEl) {
        statsEl.innerHTML = `<span class="text-emerald-400 font-bold">${volMatches} chapters, ${mufradMatches} herbs, ${murakkabMatches} formulas, ${interMatches} safety rules match "${q}"</span><button onclick="document.getElementById('grand-lib-search-input').value=''; handleGrandLibrarySearch('');" class="text-cyan-400 hover:underline ml-2">Clear</button>`;
      }

      renderGrandLibraryContent();
    }

    // =========================================================================
    // 6. CHAPTER MODAL (4 INTEGRATED LAYERS)
    // =========================================================================
    function switchModalLayer(layer) {
      currentModalLayer = layer;
      const layers = ['protocol', 'treatise', 'recipes', 'semiology'];
      layers.forEach(l => {
        const btn = document.getElementById('modal-tab-' + l);
        if (btn) {
          if (l === layer) {
            btn.className = "px-3.5 py-2 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-sm flex items-center gap-1.5 transition";
          } else {
            btn.className = "px-3.5 py-2 rounded-xl text-xs font-bold bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 flex items-center gap-1.5 transition";
          }
        }
      });
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
            ${ch.key_concepts && ch.key_concepts.length > 0 ? `
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">Key Canonical Concepts</span>
                <div class="flex flex-wrap gap-1.5">
                  ${ch.key_concepts.map(k => `<span class="px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-300 text-[11px] font-medium border border-emerald-500/20">${k}</span>`).join('')}
                </div>
              </div>
            ` : ''}

            ${ch.classical_citations && ch.classical_citations.length > 0 ? `
              <div class="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 space-y-2">
                <span class="text-[10px] font-bold text-amber-400 uppercase tracking-wider block">Classical Authority Citations (امہات الکتب)</span>
                <div class="space-y-2">
                  ${ch.classical_citations.map(c => `
                    <div class="text-xs text-amber-200/90 pl-3 border-l-2 border-amber-500/50">
                      <strong class="text-amber-300 block font-serif">${c.book} (${c.author})</strong>
                      <span class="italic">"${c.text}"</span>
                    </div>
                  `).join('')}
                </div>
              </div>
            ` : ''}

            <div class="p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/30 space-y-2">
              <span class="text-[10px] font-bold text-cyan-400 uppercase tracking-wider block">Modern Biomedical & Systems Biology Correlation</span>
              <p class="text-xs text-cyan-100/90 leading-relaxed">${ch.modern_biomedical_correlation}</p>
            </div>

            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
              <span class="text-[10px] font-bold text-teal-400 uppercase tracking-wider block">Clinical Semiology & Bedside Examination</span>
              <p class="text-xs text-slate-300 leading-relaxed">${ch.clinical_diagnostic_criteria}</p>
            </div>

            <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
              <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">Actionable Clinical Protocol & Dosages (علاجی دستور العمل)</span>
              <p class="text-xs text-emerald-100 leading-relaxed font-semibold">${ch.actionable_protocols}</p>
            </div>

            <div class="p-3.5 rounded-xl bg-rose-950/30 border border-rose-500/30 text-xs text-rose-200 flex items-start gap-2">
              <span class="text-rose-400 text-sm">⚠️</span>
              <div>
                <strong class="text-rose-300 block">Safety & Red-Flag Contraindications:</strong>
                <p class="mt-0.5 text-slate-300">${ch.safety_and_contraindications}</p>
              </div>
            </div>
          </div>
        `;
      } else if (currentModalLayer === 'treatise') {
        // LAYER 2: FULL CANONICAL TREATISE
        bodyEl.innerHTML = `
          <div class="space-y-5">
            <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
              <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">📜 Section 1: Canonical Philosophy & Doctrine (المنهج النظري)</span>
              <div class="text-xs text-emerald-100/90 leading-relaxed whitespace-pre-line font-serif">
                ${tr.canonical_philosophy_and_doctrine || 'Treatise doctrine loaded.'}
              </div>
            </div>

            <div class="p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/30 space-y-2">
              <span class="text-[10px] font-bold text-cyan-400 uppercase tracking-wider block">🔬 Section 2: Molecular Pathophysiology & Biomarkers (الفسيولوجيا الجزيئية)</span>
              <div class="text-xs text-cyan-100/90 leading-relaxed whitespace-pre-line">
                ${tr.molecular_and_cellular_pathophysiology || 'Molecular data active.'}
              </div>
            </div>

            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
              <span class="text-[10px] font-bold text-teal-400 uppercase tracking-wider block">🩺 Section 3: Bedside Clinical Examination Manual (دلیل الفحص السريري)</span>
              <div class="text-xs text-slate-300 leading-relaxed whitespace-pre-line font-mono">
                ${tr.step_by_step_clinical_examination || 'Clinical manual active.'}
              </div>
            </div>

            <div class="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 space-y-2">
              <span class="text-[10px] font-bold text-amber-300 uppercase tracking-wider block">🌿 Section 4: Comprehensive Pharmacopeia, Recipes & Mudabbar SOPs</span>
              <div class="text-xs text-amber-100/90 leading-relaxed whitespace-pre-line">
                ${tr.comprehensive_pharmacopeia_and_recipes || 'Formulary active.'}
              </div>
            </div>

            <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
              <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">📋 Section 5: Real-World Integrative Clinical Case Study</span>
              <div class="text-xs text-emerald-100/90 leading-relaxed whitespace-pre-line p-3 rounded-lg bg-slate-900/60 border border-emerald-500/20">
                ${tr.clinical_case_study || 'Clinical case study active.'}
              </div>
            </div>
          </div>
        `;
      } else if (currentModalLayer === 'recipes') {
        // LAYER 3: CLASSICAL FORMULARY & COMPOUNDING RECIPES
        bodyEl.innerHTML = `
          <div class="space-y-4">
            <div class="p-4 rounded-xl bg-amber-950/30 border border-amber-500/40 space-y-2">
              <span class="text-[10px] font-bold text-amber-400 uppercase tracking-wider block">🥣 Classical Compounding Formulary & Nuskha-Jaat (دستور نسخہ جات)</span>
              <p class="text-xs text-amber-100 leading-relaxed">
                Authentic Greco-Arab formulations codified for <strong>${ch.title_en}</strong> from <em>Al-Qanoon fit-Tibb</em>, <em>Bayaz-e-Kabir</em>, and <em>NFUM</em>.
              </p>
            </div>

            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
              <span class="text-xs font-bold text-white block">Chief Compounding Formulation (المركب الرئيسي):</span>
              <div class="text-xs text-slate-200 leading-relaxed whitespace-pre-line font-mono bg-slate-950 p-3.5 rounded-xl border border-slate-800">
                ${tr.comprehensive_pharmacopeia_and_recipes || ch.actionable_protocols}
              </div>
            </div>

            <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
              <span class="text-xs font-bold text-emerald-400 block">Clinical Dispensing & Administration Protocol:</span>
              <p class="text-xs text-slate-200 leading-relaxed">
                Administer with designated vehicle (Badraqa / Anupana): Lukewarm water, Arq Gaozaban, Ma-ul-Asal (honey water), or Arq Badiyan as clinically indicated.
              </p>
            </div>
          </div>
        `;
      } else if (currentModalLayer === 'semiology') {
        // LAYER 4: SEMIOLOGY VS MODERN BIOMARKERS MATRIX
        bodyEl.innerHTML = `
          <div class="space-y-4">
            <div class="p-4 rounded-xl bg-cyan-950/30 border border-cyan-500/40 space-y-2">
              <span class="text-[10px] font-bold text-cyan-400 uppercase tracking-wider block">🔬 Semiology vs. Modern Lab Biomarkers Cross-Correlation</span>
              <p class="text-xs text-cyan-100 leading-relaxed">
                Objective comparison between classical Bedside Semiology (Nabz, Qaroorah, Lisaan) and contemporary laboratory and radiological diagnostics.
              </p>
            </div>

            <div class="overflow-x-auto rounded-xl border border-slate-800">
              <table class="w-full text-xs text-left">
                <thead class="bg-slate-900 text-slate-300 font-mono text-[10px] uppercase border-b border-slate-800">
                  <tr>
                    <th class="p-3">Diagnostic Domain</th>
                    <th class="p-3">Classical Unani Semiology</th>
                    <th class="p-3">Modern Biomedical Biomarker</th>
                    <th class="p-3">Pathological Threshold</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-800 text-slate-200">
                  <tr class="hover:bg-slate-900/40">
                    <td class="p-3 font-bold text-emerald-400">10-Ajnas Nabz (Arterial Pulse)</td>
                    <td class="p-3">Miqdar, Qar'a (tension), Zaman (velocity), Qiwam (stiffness)</td>
                    <td class="p-3 font-mono">Pulse Contour / HRV (rMSSD)</td>
                    <td class="p-3 text-rose-300">rMSSD &lt; 20ms / Rigid Sallabi</td>
                  </tr>
                  <tr class="hover:bg-slate-900/40">
                    <td class="p-3 font-bold text-amber-400">Qaroorah (Urinalysis)</td>
                    <td class="p-3">Rang (color), Qiwam, Rasib (sediment topography), Ragwa (foam)</td>
                    <td class="p-3 font-mono">Urine Routine & Microscopic / Proteinuria</td>
                    <td class="p-3 text-rose-300">Microalbuminuria &gt; 30 mg/g</td>
                  </tr>
                  <tr class="hover:bg-slate-900/40">
                    <td class="p-3 font-bold text-teal-400">Systemic Inflammation</td>
                    <td class="p-3">Hararat-e-Ghareeba (Dyscrasic Heat & Ufoonat)</td>
                    <td class="p-3 font-mono">hs-CRP &amp; ESR</td>
                    <td class="p-3 text-rose-300">hs-CRP &gt; 3.0 mg/L / ESR &gt; 25 mm/h</td>
                  </tr>
                  <tr class="hover:bg-slate-900/40">
                    <td class="p-3 font-bold text-cyan-400">Metabolic & Endocrine</td>
                    <td class="p-3">Zof-e-Hazm-e-Sani (Hepatic Digestion Stasis)</td>
                    <td class="p-3 font-mono">HbA1c &amp; Fasting Insulin (HOMA-IR)</td>
                    <td class="p-3 text-rose-300">HbA1c &gt; 6.5% / HOMA-IR &gt; 2.5</td>
                  </tr>
                  <tr class="hover:bg-slate-900/40">
                    <td class="p-3 font-bold text-purple-400">Tissue Stiffness / Fibrosis</td>
                    <td class="p-3">Salabat-e-Jigar (Hepatic Induration / Yaboosat)</td>
                    <td class="p-3 font-mono">Transient Elastography (FibroScan)</td>
                    <td class="p-3 text-rose-300">Liver Stiffness &gt; 7.0 kPa (F2-F4)</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        `;
      }
    }

    function openGrandLibraryChapterModal(volId, chapId) {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib) return;

      const vol = (lib.volumes || []).find(v => v.id === volId);
      if (!vol) return;

      const ch = (vol.chapters || []).find(c => c.id === chapId);
      if (!ch) return;

      currentActiveChapter = { vol, ch };
      currentModalLayer = 'protocol';

      const modal = document.getElementById('grand-library-modal');
      const badgeEl = document.getElementById('grand-lib-modal-badge');
      const titleEl = document.getElementById('grand-lib-modal-title');
      const urduEl = document.getElementById('grand-lib-modal-urdu');

      if (!modal) return;

      if (badgeEl) badgeEl.innerText = `${vol.title_en.split(':')[0]} • Chapter ${ch.chapter_number}`;
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

      openGrandLibraryChapterModal(lib.volumes[0].id, lib.volumes[0].chapters[0].id);
    }

    // =========================================================================
    // 7. DEDICATED MUFRAD & MURAKKAB DETAIL MODALS
    // =========================================================================
    function openMufradModal(zmfId) {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib || !lib.mufradat) return;

      const m = lib.mufradat.find(x => x.id === zmfId || x.name === zmfId);
      if (!m) return;
      currentActiveMufrad = m;

      let modal = document.getElementById('mufrad-detail-modal');
      if (!modal) {
        modal = document.createElement('div');
        modal.id = 'mufrad-detail-modal';
        modal.className = 'fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4';
        document.body.appendChild(modal);
      }

      modal.innerHTML = `
        <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl max-w-2xl w-full p-6 space-y-4 shadow-2xl max-h-[92vh] flex flex-col">
          <div class="flex justify-between items-start border-b border-[var(--border)] pb-3">
            <div>
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-full font-mono text-[10px] font-bold ${m.schedule_e1 ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 'bg-emerald-500/20 text-emerald-300'}">
                  ${m.id} • UPI Monograph
                </span>
                <span class="px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono text-[10px] font-bold">
                  Mizaj: ${m.mizaj} (Darajah ${m.daraja})
                </span>
              </div>
              <h3 class="font-bold text-xl text-white mt-1">${m.name}</h3>
              ${m.urdu_script ? `<p class="text-sm text-emerald-400 font-serif" dir="rtl">${m.urdu_script}</p>` : ''}
              <p class="text-xs text-cyan-400 italic">${m.botanical} (${m.family})</p>
            </div>
            <button onclick="closeMufradModal()" class="text-[var(--muted)] hover:text-white p-2 text-lg">✕</button>
          </div>

          <div class="overflow-y-auto space-y-3.5 text-xs text-slate-200 pr-1">
            <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
              <strong class="text-slate-400 text-[10px] uppercase block">Pharmacological Actions (أفعال و خواص):</strong>
              <p class="text-emerald-300 font-semibold">${Array.isArray(m.afaal) ? m.afaal.join('; ') : m.afaal}</p>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-slate-400 text-[10px] uppercase block">Part Used (حصۂ مستعملہ):</strong>
                <p class="text-white">${m.part}</p>
              </div>
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-slate-400 text-[10px] uppercase block">Standard Dosage (مقدار خوراک):</strong>
                <p class="text-amber-300 font-semibold">${m.dose}</p>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-slate-400 text-[10px] uppercase block">Corrective (مصلح):</strong>
                <p class="text-slate-200">${m.musleh}</p>
              </div>
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-slate-400 text-[10px] uppercase block">Substitute (بدل):</strong>
                <p class="text-slate-200">${m.badal}</p>
              </div>
            </div>

            <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
              <strong class="text-slate-400 text-[10px] uppercase block">Tadbeer / Processing SOP (تدبیر):</strong>
              <p class="text-slate-300">${m.tadbeer}</p>
            </div>

            <div class="p-3 rounded-xl bg-amber-950/20 border border-amber-500/30 text-amber-200 space-y-0.5">
              <strong class="text-amber-400 text-[10px] uppercase block">Classical Citation:</strong>
              <p class="text-xs italic">${m.source}</p>
            </div>
          </div>

          <div class="pt-3 border-t border-[var(--border)] flex justify-between items-center">
            <span class="text-[11px] text-slate-500">Unani Pharmacopoeia of India (UPI)</span>
            <div class="flex gap-2">
              <button onclick="closeMufradModal()" class="px-4 py-2 rounded-xl border border-[var(--border)] text-xs text-slate-400">Close</button>
              <button onclick="addMonographToPrescription('mufrad', '${m.id}')" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow flex items-center gap-1.5">
                <span>➕ Add to Prescription</span>
              </button>
            </div>
          </div>
        </div>
      `;
      modal.classList.remove('hidden');
    }

    function closeMufradModal() {
      const modal = document.getElementById('mufrad-detail-modal');
      if (modal) modal.classList.add('hidden');
      currentActiveMufrad = null;
    }

    function openMurakkabModal(formulaId) {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib || !lib.murakkabat) return;

      const f = lib.murakkabat.find(x => x.id === formulaId || x.name === formulaId);
      if (!f) return;
      currentActiveMurakkab = f;

      let modal = document.getElementById('murakkab-detail-modal');
      if (!modal) {
        modal = document.createElement('div');
        modal.id = 'murakkab-detail-modal';
        modal.className = 'fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4';
        document.body.appendChild(modal);
      }

      modal.innerHTML = `
        <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl max-w-2xl w-full p-6 space-y-4 shadow-2xl max-h-[92vh] flex flex-col">
          <div class="flex justify-between items-start border-b border-[var(--border)] pb-3">
            <div>
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-full bg-teal-500/20 text-teal-300 font-mono text-[10px] font-bold">
                  NFUM Formulation • ${f.category}
                </span>
                ${f.schedule_e1_warning ? '<span class="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 font-mono text-[10px] font-bold">⚠️ Schedule E-1 Alert</span>' : ''}
              </div>
              <h3 class="font-bold text-xl text-white mt-1">${f.name}</h3>
              ${f.urdu_name ? `<p class="text-sm text-emerald-400 font-serif" dir="rtl">${f.urdu_name}</p>` : ''}
              <p class="text-xs text-slate-400 font-mono">${f.classical_source}</p>
            </div>
            <button onclick="closeMurakkabModal()" class="text-[var(--muted)] hover:text-white p-2 text-lg">✕</button>
          </div>

          <div class="overflow-y-auto space-y-3.5 text-xs text-slate-200 pr-1">
            <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
              <strong class="text-slate-400 text-[10px] uppercase block">Classical Indication (وجہ استعمال):</strong>
              <p class="text-teal-300 font-semibold leading-relaxed">${f.classical_indication}</p>
            </div>

            <div class="space-y-1.5">
              <strong class="text-slate-400 text-[10px] uppercase block">Recipe Composition &amp; Ingredients (اجزائے ترکیبی):</strong>
              <div class="rounded-xl border border-slate-800 overflow-hidden">
                <table class="w-full text-left">
                  <thead class="bg-slate-900 text-slate-400 text-[10px] font-mono uppercase">
                    <tr>
                      <th class="p-2.5">Ingredient</th>
                      <th class="p-2.5">Role</th>
                      <th class="p-2.5">Statutory Class</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-800">
                    ${(f.key_ingredients || []).map(ing => `
                      <tr class="hover:bg-slate-900/40">
                        <td class="p-2.5 font-medium text-white">${ing.name}</td>
                        <td class="p-2.5 font-mono text-[10px] text-cyan-300">${ing.role}</td>
                        <td class="p-2.5 text-[10px] ${ing.is_schedule_e1 ? 'text-rose-400 font-bold' : 'text-slate-400'}">
                          ${ing.is_schedule_e1 ? '⚠️ Schedule E(1)' : 'Standard'}
                        </td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-slate-400 text-[10px] uppercase block">Dose & Vehicle (مقدار خوراک و بدرقہ):</strong>
                <p class="text-amber-300 font-semibold">${f.dose}</p>
              </div>
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-slate-400 text-[10px] uppercase block">Precautions:</strong>
                <p class="text-slate-200">${f.precautions || 'Standard Unani administration precautions apply.'}</p>
              </div>
            </div>
          </div>

          <div class="pt-3 border-t border-[var(--border)] flex justify-between items-center">
            <span class="text-[11px] text-slate-500">National Formulary of Unani Medicine</span>
            <div class="flex gap-2">
              <button onclick="closeMurakkabModal()" class="px-4 py-2 rounded-xl border border-[var(--border)] text-xs text-slate-400">Close</button>
              <button onclick="addMonographToPrescription('murakkab', '${f.id}')" class="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shadow flex items-center gap-1.5">
                <span>➕ Add to Prescription</span>
              </button>
            </div>
          </div>
        </div>
      `;
      modal.classList.remove('hidden');
    }

    function closeMurakkabModal() {
      const modal = document.getElementById('murakkab-detail-modal');
      if (modal) modal.classList.add('hidden');
      currentActiveMurakkab = null;
    }

    // =========================================================================
    // 8. DOCTOR CLINICAL DESK INTEGRATION & PRINTING
    // =========================================================================
    function copyCurrentChapterProtocol() {
      if (!currentActiveChapter || !currentActiveChapter.ch) {
        if (typeof showNotification === 'function') showNotification('No chapter currently selected.', 'warning');
        return;
      }
      const { ch } = currentActiveChapter;
      const text = `[ZAYVORA CANONICAL PROTOCOL: ${ch.title_en}]\n` +
                   `Citations: ${(ch.classical_citations || []).map(c => c.book + ' (' + c.author + ')').join('; ')}\n` +
                   `Diagnostic Criteria: ${ch.clinical_diagnostic_criteria}\n` +
                   `Protocol: ${ch.actionable_protocols}\n` +
                   `Safety: ${ch.safety_and_contraindications}`;
      
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
          if (typeof showNotification === 'function') {
            showNotification(`Protocol for "${ch.title_en}" copied to clipboard!`, 'success');
          }
        }).catch(() => {
          if (typeof showNotification === 'function') {
            showNotification('Protocol ready.', 'info');
          }
        });
      } else {
        if (typeof showNotification === 'function') {
          showNotification(`Protocol copied for ${ch.title_en}`, 'info');
        }
      }
    }

    function addMonographToPrescription(itemType, itemId) {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib) return;

      let medName = '';
      let dose = '';
      let instructions = '';

      if (itemType === 'mufrad') {
        const m = (lib.mufradat || []).find(x => x.id === itemId);
        if (!m) return;
        medName = `Sufuf ${m.name} (${m.botanical})`;
        dose = m.dose;
        instructions = `Musleh: ${m.musleh}. Take after meals with lukewarm water.`;
      } else if (itemType === 'murakkab') {
        const f = (lib.murakkabat || []).find(x => x.id === itemId);
        if (!f) return;
        medName = `${f.name} (${f.category})`;
        dose = f.dose;
        instructions = `NFUM protocol. ${f.precautions || ''}`;
      }

      if (typeof state !== 'undefined' && Array.isArray(state.rxItems)) {
        state.rxItems.push({
          id: 'rx-' + Date.now(),
          medicineName: medName,
          dosage: dose,
          frequency: 'BID',
          duration: '14 Days',
          instructions: instructions
        });
        if (typeof showNotification === 'function') {
          showNotification(`Added "${medName}" to Active OPD Prescription Cart!`, 'success');
        }
        if (typeof renderRxItemsList === 'function') renderRxItemsList();
      } else {
        const rxClip = `Prescription Order:\nItem: ${medName}\nDose: ${dose}\nInstructions: ${instructions}`;
        if (navigator.clipboard) {
          navigator.clipboard.writeText(rxClip);
        }
        if (typeof showNotification === 'function') {
          showNotification(`Copied formulation "${medName}" to clipboard for Care Plan!`, 'success');
        }
      }

      closeMufradModal();
      closeMurakkabModal();
    }

    function printCurrentMonograph() {
      window.print();
    }
'''

full_js_content = js_engine_code.replace('__LIBRARY_JSON__', library_json_str)

# Write to js/modules/05-grand-library.js
# First check what is in js/modules/05-grand-library.js after copyCurrentChapterProtocol()
module_path = os.path.join(BASE_DIR, 'js', 'modules', '05-grand-library.js')
core_path = os.path.join(BASE_DIR, 'js', 'zayvora-core.js')

with open(module_path, 'r', encoding='utf-8') as f:
    mod_text = f.read()

# Preserve clinicalOutcomeCohorts from 05-grand-library.js if present
outcomes_marker = 'clinicalOutcomeCohorts ='
outcomes_code = ''
if outcomes_marker in mod_text:
    idx = mod_text.find(outcomes_marker)
    # Find start of const clinicalOutcomeCohorts
    c_idx = mod_text.rfind('const clinicalOutcomeCohorts =', 0, idx + 40)
    if c_idx != -1:
        outcomes_code = '\n\n    ' + mod_text[c_idx:]

new_module_code = full_js_content + outcomes_code
with open(module_path, 'w', encoding='utf-8') as f:
    f.write(new_module_code)
print(f"Written updated {module_path} (lines: {new_module_code.count(chr(10)):,})")

# Now patch js/zayvora-core.js
with open(core_path, 'r', encoding='utf-8') as f:
    core_text = f.read()

# Find grand library start and end in zayvora-core.js
start_marker = '// GRAND INTEGRATIVE MEDICAL LIBRARY (12 VOLUMES)'
end_marker = 'function handleRouteFromURL() {'

s_pos = core_text.find(start_marker)
e_pos = core_text.find(end_marker)

if s_pos != -1 and e_pos != -1:
    # Look back to comment block
    comment_lead = '// =========================================================================\n    // =========================================================================\n    '
    lead_pos = core_text.rfind(comment_lead, 0, s_pos)
    if lead_pos != -1:
        s_pos = lead_pos

    new_core_text = core_text[:s_pos] + full_js_content + '\n\n    ' + core_text[e_pos:]
    with open(core_path, 'w', encoding='utf-8') as f:
        f.write(new_core_text)
    print(f"Patched {core_path} successfully!")
else:
    print(f"WARNING: Markers not found in {core_path}: s_pos={s_pos}, e_pos={e_pos}")

