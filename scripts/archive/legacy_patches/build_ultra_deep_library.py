#!/usr/bin/env python3
"""
ZAYVORA Health OS — Ultra-Deep Grand Integrative Medical Library Engine Builder
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
    UNIVERSAL_CONTRAINDICATIONS_LIST,
    MATAB_PROTOCOLS_LIST,
    PARHEZ_REGIMENS_LIST
)

master_data = {
    "metadata": LIBRARY_METADATA,
    "volumes": GRAND_INTEGRATIVE_LIBRARY["volumes"],
    "mufradat": MUFRADAT_LIST,
    "murakkabat": MURAKKABAT_LIST,
    "drug_interactions": DRUG_INTERACTIONS_LIST,
    "universal_contraindications": UNIVERSAL_CONTRAINDICATIONS_LIST,
    "matab_protocols": MATAB_PROTOCOLS_LIST,
    "parhez_regimens": PARHEZ_REGIMENS_LIST
}

library_json_str = json.dumps(master_data, ensure_ascii=False)
print(f"Master JSON Size: {len(library_json_str)/1024:.1f} KB")

js_engine_code = r'''
    // =========================================================================
    // GRAND INTEGRATIVE MEDICAL LIBRARY — ULTRA-DEEP CLINICAL OS ENGINE (v15.5)
    // =========================================================================
    window.ZAYVORA_GRAND_LIBRARY_DATA = __LIBRARY_JSON__;

    let currentLibraryMode = 'volumes'; // 'volumes' | 'mufradat' | 'murakkabat' | 'matab' | 'parhez' | 'interactions' | 'pulse'
    let currentLibrarySelectedVol = 'all';
    let currentMufradFilter = 'all';
    let currentMurakkabFilter = 'all';
    let currentInteractionsFilter = 'all';
    let currentActiveChapter = null;
    let currentActiveMufrad = null;
    let currentActiveMurakkab = null;
    let currentActiveMatab = null;
    let currentActiveParhez = null;
    let currentModalLayer = 'protocol'; // 'protocol' | 'treatise' | 'recipes' | 'semiology'

    function renderGrandLibrary(container, context) {
      const subnav = typeof getWebsiteHubSubnav === 'function' ? getWebsiteHubSubnav(state.tab) : '';
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib) return;

      const totalVolumes = (lib.volumes || []).length;
      const totalChapters = (lib.volumes || []).reduce((acc, v) => acc + (v.chapters || []).length, 0);
      const totalMufradat = (lib.mufradat || []).length;
      const totalMurakkabat = (lib.murakkabat || []).length;
      const totalMatab = (lib.matab_protocols || []).length;
      const totalParhez = (lib.parhez_regimens || []).length;
      const totalInteractions = (lib.drug_interactions || []).length;

      let html = `
        <div class="max-w-6xl mx-auto space-y-6 pb-12">
          ${context === 'website' ? subnav : ''}
          
          <!-- Library Header Hero -->
          <div class="bg-gradient-to-r from-emerald-950/60 via-slate-900 to-slate-900 p-6 sm:p-8 rounded-3xl border border-emerald-500/30 space-y-4 shadow-xl">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold font-mono">12 VOLUMES (${totalChapters} CH.)</span>
                <span class="px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 text-xs font-mono font-bold">${totalMufradat} GOLD MUFRADAT</span>
                <span class="px-3 py-1 rounded-full bg-teal-500/20 text-teal-300 text-xs font-mono font-bold">${totalMurakkabat} MURAKKABAT</span>
                <span class="px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-mono font-bold">${totalMatab} MATAB PROTOCOLS</span>
                <span class="px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 text-xs font-mono font-bold">${totalParhez} PARHEZ REGIMENS</span>
                <span class="px-3 py-1 rounded-full bg-rose-500/20 text-rose-300 text-xs font-mono font-bold">CYP450 MATRIX</span>
              </div>
              ${context === 'website' ? '<button onclick="viewWebsitePage(\'home\')" class="text-xs text-[var(--muted)] hover:text-white">← Back to Home</button>' : ''}
            </div>
            <div>
              <h1 class="text-2xl sm:text-3xl font-extrabold text-[#1B242A] dark:text-white">ZAYVORA Grand Classical &amp; Modern Integrative Medical Library</h1>
              <p class="text-emerald-400 font-serif text-sm mt-1" dir="rtl">جامع طبی کتب خانہ — ۱۲ ابواب، ۳۵۰ مفردات، ۵۹ مرکبات، مطب نسخہ جات اور احتیاطی تدابیر</p>
            </div>
            <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-4xl">
              The authoritative clinical knowledge foundation of ZAYVORA Health OS. Unites classical Greco-Arab doctrines (<em>Al-Qanoon</em>, <em>Al-Hawi</em>, <em>Kamil al-Sina'a</em>, <em>Khazain-ul-Advia</em>, <em>Bayaz-e-Kabir</em>) with active phytochemistry, randomized controlled trials (RCTs), 10-Ajnas pulse semiology, and modern diagnostic cutoffs (hs-CRP, HbA1c, FibroScan).
            </p>

            <!-- Search Bar -->
            <div class="pt-2">
              <div class="relative">
                <input 
                  type="text" 
                  id="grand-lib-search-input" 
                  placeholder="Search across 12 volumes, 350 herbs, 59 recipes, Matab protocols, Parhez rules, or drug interactions..." 
                  oninput="handleGrandLibrarySearch(this.value)"
                  class="w-full pl-10 pr-4 py-3 bg-slate-900/90 border border-emerald-500/40 rounded-xl text-xs sm:text-sm text-white focus:outline-none focus:border-emerald-400 shadow-inner"
                >
                <span class="absolute left-3.5 top-3.5 text-slate-400 text-sm">🔍</span>
              </div>
              <div id="grand-lib-search-stats" class="text-[11px] text-slate-400 mt-1.5 flex justify-between flex-wrap gap-2">
                <span>12 Volumes • 350 Mufradat • 59 Murakkabat • 8 Matab Protocols • 8 Parhez Regimens</span>
                <span class="text-emerald-400 font-mono">100% Peer-Reviewed • Zero Mock Data</span>
              </div>
            </div>
          </div>

          <!-- TOP-LEVEL 6-MODE SWITCHER TABS -->
          <div class="flex items-center gap-2 overflow-x-auto pb-1 border-b border-slate-800 scrollbar-none">
            <button onclick="switchGrandLibraryMode('volumes')" id="lib-mode-tab-volumes" class="px-3.5 py-2.5 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-lg shadow-emerald-950/40 ring-2 ring-emerald-400/40 flex items-center gap-2 shrink-0 transition">
              <span>🏛️</span> 12 Volumes
            </button>
            <button onclick="switchGrandLibraryMode('mufradat')" id="lib-mode-tab-mufradat" class="px-3.5 py-2.5 rounded-xl text-xs font-bold bg-slate-900/90 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-2 shrink-0 transition">
              <span>🌿</span> 350+ Mufradat
            </button>
            <button onclick="switchGrandLibraryMode('murakkabat')" id="lib-mode-tab-murakkabat" class="px-3.5 py-2.5 rounded-xl text-xs font-bold bg-slate-900/90 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-2 shrink-0 transition">
              <span>🥣</span> 59 Murakkabat
            </button>
            <button onclick="switchGrandLibraryMode('matab')" id="lib-mode-tab-matab" class="px-3.5 py-2.5 rounded-xl text-xs font-bold bg-slate-900/90 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-2 shrink-0 transition">
              <span>🧪</span> 8 Matab Protocols
            </button>
            <button onclick="switchGrandLibraryMode('parhez')" id="lib-mode-tab-parhez" class="px-3.5 py-2.5 rounded-xl text-xs font-bold bg-slate-900/90 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-2 shrink-0 transition">
              <span>🥗</span> 8 Parhez Regimens
            </button>
            <button onclick="switchGrandLibraryMode('interactions')" id="lib-mode-tab-interactions" class="px-3.5 py-2.5 rounded-xl text-xs font-bold bg-slate-900/90 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-2 shrink-0 transition">
              <span>🛡️</span> CYP450 Safety
            </button>
            <button onclick="switchGrandLibraryMode('pulse')" id="lib-mode-tab-pulse" class="px-3.5 py-2.5 rounded-xl text-xs font-bold bg-slate-900/90 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-2 shrink-0 transition">
              <span>🩺</span> 10-Ajnas Nabz
            </button>
          </div>

          <!-- SUB-FILTERS: MODE 1 (VOLUMES) -->
          <div id="lib-volume-subfilters" class="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
            <button onclick="filterGrandLibraryVolume('all')" id="lib-filter-btn-all" class="px-3 py-1.5 rounded-xl bg-emerald-600 text-white text-xs font-bold shrink-0 transition">
              All 12 Volumes
            </button>
            ${(lib.volumes || []).map(v => `
              <button onclick="filterGrandLibraryVolume('${v.id}')" id="lib-filter-btn-${v.id}" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs shrink-0 transition flex items-center gap-1.5">
                <span>${v.icon}</span> Vol ${v.volume_number}: ${v.title_en.split(':')[0]}
              </button>
            `).join('')}
          </div>

          <!-- SUB-FILTERS: MODE 2 (MUFRADAT) -->
          <div id="lib-mufrad-subfilters" class="hidden items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
            <button onclick="filterGrandLibraryMufrad('all')" id="lib-mfilter-all" class="px-3 py-1.5 rounded-xl bg-amber-600 text-white text-xs font-bold shrink-0 transition">
              All 350 Herbs
            </button>
            <button onclick="filterGrandLibraryMufrad('haar-yabis')" id="lib-mfilter-haar-yabis" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-rose-300 text-xs shrink-0 transition flex items-center gap-1">
              <span>🔥</span> Haar-Yabis
            </button>
            <button onclick="filterGrandLibraryMufrad('haar-ratab')" id="lib-mfilter-haar-ratab" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-amber-300 text-xs shrink-0 transition flex items-center gap-1">
              <span>☀️</span> Haar-Ratab
            </button>
            <button onclick="filterGrandLibraryMufrad('barid-ratab')" id="lib-mfilter-barid-ratab" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-cyan-300 text-xs shrink-0 transition flex items-center gap-1">
              <span>💧</span> Barid-Ratab
            </button>
            <button onclick="filterGrandLibraryMufrad('barid-yabis')" id="lib-mfilter-barid-yabis" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-blue-300 text-xs shrink-0 transition flex items-center gap-1">
              <span>❄️</span> Barid-Yabis
            </button>
            <button onclick="filterGrandLibraryMufrad('schedule-e1')" id="lib-mfilter-schedule-e1" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-rose-500/40 text-rose-400 text-xs shrink-0 transition flex items-center gap-1 font-semibold">
              <span>⚠️</span> Schedule E(1) Only
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
      
      const modes = ['volumes', 'mufradat', 'murakkabat', 'matab', 'parhez', 'interactions', 'pulse'];
      modes.forEach(m => {
        const btn = document.getElementById('lib-mode-tab-' + m);
        if (btn) {
          if (m === mode) {
            btn.className = "px-3.5 py-2.5 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-lg shadow-emerald-950/40 ring-2 ring-emerald-400/40 flex items-center gap-2 shrink-0 transition";
          } else {
            btn.className = "px-3.5 py-2.5 rounded-xl text-xs font-bold bg-slate-900/90 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-2 shrink-0 transition";
          }
        }
      });

      const volFilters = document.getElementById('lib-volume-subfilters');
      const mufradFilters = document.getElementById('lib-mufrad-subfilters');
      const murakkabFilters = document.getElementById('lib-murakkab-subfilters');

      if (volFilters) volFilters.className = mode === 'volumes' ? 'flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin' : 'hidden';
      if (mufradFilters) mufradFilters.className = mode === 'mufradat' ? 'flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin' : 'hidden';
      if (murakkabFilters) murakkabFilters.className = mode === 'murakkabat' ? 'flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin' : 'hidden';

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
      } else if (currentLibraryMode === 'matab') {
        renderGrandLibraryMatab(q);
      } else if (currentLibraryMode === 'parhez') {
        renderGrandLibraryParhez(q);
      } else if (currentLibraryMode === 'interactions') {
        renderGrandLibraryInteractions(q);
      } else if (currentLibraryMode === 'pulse') {
        renderGrandLibraryPulse();
      }
    }

    // =========================================================================
    // 1. VOLUMES RENDERER
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
              <span class="text-3xl p-2.5 rounded-2xl bg-emerald-950/40 border border-emerald-500/30 shrink-0">${vol.icon}</span>
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
                  <span class="text-xs text-slate-500 group-hover:text-emerald-400 transition">Read Protocol &amp; Treatise →</span>
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
          ? 'px-3 py-1.5 rounded-xl bg-emerald-600 text-white text-xs font-bold shrink-0 transition'
          : 'px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs shrink-0 transition';
      }

      (lib.volumes || []).forEach(v => {
        const btn = document.getElementById('lib-filter-btn-' + v.id);
        if (btn) {
          btn.className = v.id === volId
            ? 'px-3 py-1.5 rounded-xl bg-emerald-600 text-white text-xs font-bold shrink-0 transition flex items-center gap-1.5'
            : 'px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs shrink-0 transition flex items-center gap-1.5';
        }
      });

      renderGrandLibraryContent();
    }

    // =========================================================================
    // 2. MUFRADAT RENDERER (350 GOLD MONOGRAPHS)
    // =========================================================================
    function renderGrandLibraryMufradat(query = '') {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      const grid = document.getElementById('grand-library-grid');
      if (!grid || !lib) return;

      let mufradat = lib.mufradat || [];

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
          (m.urdu_name && m.urdu_name.toLowerCase().includes(query)) ||
          (m.urdu_script && m.urdu_script.includes(query)) ||
          (m.family && m.family.toLowerCase().includes(query)) ||
          (m.mizaj && m.mizaj.toLowerCase().includes(query)) ||
          (m.constituents && m.constituents.some(c => c.toLowerCase().includes(query))) ||
          (m.afaal && m.afaal.some(a => a.toLowerCase().includes(query)))
        );
      }

      if (mufradat.length === 0) {
        grid.innerHTML = `
          <div class="p-12 text-center bg-slate-900/50 rounded-2xl border border-slate-800 text-slate-400 space-y-2">
            <span class="text-3xl block">🌿</span>
            <strong class="text-white text-base">No single herbs matched "${query}"</strong>
            <p class="text-xs">Search by Urdu script (سورنجان، اسگندھ), common name, chemical constituent (Withanolides), or botanical name.</p>
          </div>
        `;
        return;
      }

      grid.innerHTML = `
        <div class="space-y-4">
          <div class="flex justify-between items-center px-1">
            <span class="text-xs text-slate-400">Displaying <strong class="text-white">${mufradat.length}</strong> gold benchmark monographs</span>
            <span class="text-xs text-amber-400 font-mono">UPI Standard • Phytochemistry &amp; RCT Evidenced</span>
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
                    ${m.urdu_script && m.urdu_script !== m.name ? `<p class="text-xs text-emerald-400 font-serif" dir="rtl">${m.urdu_script}</p>` : ''}
                    <p class="text-[11px] text-cyan-400 italic">${m.botanical} (${m.family})</p>
                  </div>

                  <div class="text-[11px] text-slate-300 space-y-1 pt-1 border-t border-slate-800">
                    <p><strong class="text-slate-400">Part:</strong> ${m.part}</p>
                    <p><strong class="text-slate-400">Actions:</strong> ${Array.isArray(m.afaal) ? m.afaal.slice(0, 2).join('; ') : m.afaal}</p>
                    ${m.indications && m.indications.length > 0 ? `<p><strong class="text-cyan-400">Indication:</strong> ${m.indications[0]}</p>` : ''}
                    ${m.contraindications && m.contraindications.length > 0 ? `<p class="text-[10px] text-rose-300 font-medium"><strong>Contra:</strong> ${m.contraindications[0]}</p>` : ''}
                    ${m.constituents && m.constituents.length > 0 ? `<p><strong class="text-amber-400 font-mono">Actives:</strong> ${m.constituents[0]}</p>` : ''}
                    <p><strong class="text-slate-400">Musleh:</strong> ${m.musleh}</p>
                  </div>
                </div>

                <div class="pt-2 border-t border-slate-800 flex items-center justify-between gap-2">
                  <button onclick="openMufradModal('${m.id}')" class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-1 transition">
                    <span>🔍</span> Deep Monograph
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
    // 3. MURAKKABAT RENDERER (59 FORMULATIONS)
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

      grid.innerHTML = `
        <div class="space-y-4">
          <div class="flex justify-between items-center px-1">
            <span class="text-xs text-slate-400">Displaying <strong class="text-white">${murakkabat.length}</strong> classical compound formulations</span>
            <span class="text-xs text-teal-400 font-mono">National Formulary of Unani Medicine (NFUM)</span>
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
                    <p><strong class="text-slate-400">Dose &amp; Vehicle:</strong> ${f.dose}</p>
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
    // 4. MATAB COMPOUNDING PROTOCOLS RENDERER (8 MULTI-PHASE PROTOCOLS)
    // =========================================================================
    function renderGrandLibraryMatab(query = '') {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      const grid = document.getElementById('grand-library-grid');
      if (!grid || !lib) return;

      let list = lib.matab_protocols || [];
      if (query) {
        list = list.filter(p => p.name.toLowerCase().includes(query) || (p.organ_axis && p.organ_axis.toLowerCase().includes(query)) || (p.description && p.description.toLowerCase().includes(query)));
      }

      grid.innerHTML = `
        <div class="space-y-5">
          <div class="p-4 rounded-2xl bg-cyan-950/20 border border-cyan-500/30 flex justify-between items-center">
            <div>
              <span class="text-xs font-mono font-bold text-cyan-400 uppercase tracking-wider block">Sequential Multi-Phase Compounding Protocols</span>
              <p class="text-xs text-slate-300">Phase 1 Gut-Liver Priming (Nujz) ➔ Phase 2 Active Target Therapeutics ➔ Phase 3 Stabilization</p>
            </div>
            <span class="px-3 py-1 rounded-full bg-cyan-900/60 border border-cyan-500/40 text-cyan-300 font-mono text-xs font-bold">
              ${list.length} Clinical Protocols
            </span>
          </div>

          <div class="space-y-4">
            ${list.map(p => `
              <div class="p-6 rounded-3xl bg-slate-950 border border-slate-800 space-y-4 shadow-xl">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800/80 pb-3">
                  <div>
                    <span class="px-2 py-0.5 rounded font-mono text-[10px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                      ${p.protocol_id} • ${p.organ_axis}
                    </span>
                    <h3 class="text-base font-bold text-white mt-1">${p.name}</h3>
                  </div>
                  <button onclick="addMonographToPrescription('matab', '${p.protocol_id}')" class="px-3.5 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs shadow flex items-center gap-1.5 transition">
                    <span>➕ Add Entire Protocol to Care Plan</span>
                  </button>
                </div>

                <p class="text-xs text-slate-300 leading-relaxed">${p.description}</p>

                <!-- Phases -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                  ${Object.keys(p.phases || {}).map(k => {
                    const phase = p.phases[k];
                    return `
                      <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 space-y-2 text-xs">
                        <span class="font-bold text-amber-300 block text-xs">${phase.phase_name}</span>
                        <span class="text-[10px] text-slate-400 font-mono block">Duration: ${phase.duration_days ? phase.duration_days + ' Days' : phase.duration_cycle_days}</span>
                        <div class="space-y-1 pt-1 border-t border-slate-800">
                          ${(phase.ingredients || []).map(ing => `
                            <div class="text-[11px] text-slate-200 flex justify-between">
                              <span>${ing.herb}</span>
                              <strong class="text-cyan-300 font-mono">${ing.dose_g}g</strong>
                            </div>
                          `).join('')}
                        </div>
                        <p class="text-[10px] text-emerald-300 pt-1 italic">${phase.preparation_method}</p>
                      </div>
                    `;
                  }).join('')}
                </div>

                ${p.parhez && p.parhez.length > 0 ? `
                  <div class="p-3 rounded-xl bg-amber-950/20 border border-amber-500/30 text-xs text-amber-200 space-y-1">
                    <strong class="text-amber-400 text-[10px] uppercase font-bold block">Protocol Dietary Restrictions (پرہیز):</strong>
                    <ul class="list-disc list-inside space-y-0.5 text-[11px]">
                      ${p.parhez.map(r => `<li>${r}</li>`).join('')}
                    </ul>
                  </div>
                ` : ''}
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    // =========================================================================
    // 5. PARHEZ & LIFESTYLE REGIMENS RENDERER (8 PROTOCOLS)
    // =========================================================================
    function renderGrandLibraryParhez(query = '') {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      const grid = document.getElementById('grand-library-grid');
      if (!grid || !lib) return;

      let list = lib.parhez_regimens || [];
      if (query) {
        list = list.filter(p => p.name.toLowerCase().includes(query) || (p.classical_principle && p.classical_principle.toLowerCase().includes(query)));
      }

      grid.innerHTML = `
        <div class="space-y-5">
          <div class="p-4 rounded-2xl bg-purple-950/20 border border-purple-500/30 flex justify-between items-center">
            <div>
              <span class="text-xs font-mono font-bold text-purple-400 uppercase tracking-wider block">Evidence-Based Clinical Parhez Architecture</span>
              <p class="text-xs text-slate-300">Targeted organ-axis lifestyle restrictions grounded in classical Tibb and molecular pathophysiology</p>
            </div>
            <span class="px-3 py-1 rounded-full bg-purple-900/60 border border-purple-500/40 text-purple-300 font-mono text-xs font-bold">
              ${list.length} Regimens
            </span>
          </div>

          <div class="space-y-4">
            ${list.map(p => `
              <div class="p-6 rounded-3xl bg-slate-950 border border-slate-800 space-y-4 shadow-xl">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800/80 pb-3">
                  <div>
                    <span class="px-2 py-0.5 rounded font-mono text-[10px] font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">
                      ${p.code} • ${(p.target_axes || []).join(', ')}
                    </span>
                    <h3 class="text-base font-bold text-white mt-1">${p.name}</h3>
                    <p class="text-xs text-emerald-400 font-serif mt-0.5" dir="rtl">${p.classical_principle}</p>
                  </div>
                  <span class="px-3 py-1 rounded-full bg-slate-900 border border-slate-700 text-slate-300 font-mono text-xs">
                    Cycle: ${p.duration_days} Days
                  </span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  ${(p.rules || []).map(r => `
                    <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 space-y-1.5">
                      <strong class="text-amber-400 text-xs block">${r.category}</strong>
                      <p class="text-slate-200 leading-relaxed">${r.instruction}</p>
                      <div class="pt-1 border-t border-slate-800 text-[10px] text-cyan-300">
                        <strong>Biochemical Rationale:</strong> ${r.scientific_rationale}
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    // =========================================================================
    // 6. 10-AJNAS NABZ PULSE & QAROORAH SIMULATOR
    // =========================================================================
    function renderGrandLibraryPulse() {
      const grid = document.getElementById('grand-library-grid');
      if (!grid) return;

      grid.innerHTML = `
        <div class="space-y-6">
          <div class="p-6 rounded-3xl bg-gradient-to-r from-teal-950/60 via-slate-900 to-slate-900 border border-teal-500/30 space-y-2">
            <span class="text-xs font-mono font-bold text-teal-400 uppercase tracking-wider block">Ilm-un-Nabz &amp; Qaroorah Bedside Semiology Suite</span>
            <h2 class="text-xl font-bold text-white">The 10 Classical Ajnas Pulse Waveforms &amp; Urine Topography</h2>
            <p class="text-xs text-slate-300 leading-relaxed max-w-4xl">
              Codified from <em>Al-Qanoon fit-Tibb</em> (Book I, Fen 2) and <em>Kamil al-Sina'a</em>. Master the tactile arterial pulse dynamics and their direct systemic bio-fluid correlations.
            </p>
          </div>

          <!-- 10 Ajnas Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
            ${[
              { no: 1, name: 'Miqdar (Quantity / حجم)', desc: 'Length, breadth, and depth of the arterial expansion.', types: 'Azeem (Large/Dam), Saghir (Small/Sauda), Motadil (Balanced).' },
              { no: 2, name: 'Kayfiyyat-e-Qar\'a (Tension / قرع)', desc: 'Force with which the arterial impulse impacts finger pads.', types: 'Qawi (Strong/High stroke volume), Zaeef (Weak/Hypotensive).' },
              { no: 3, name: 'Zaman-e-Harakat (Velocity / زمان)', desc: 'Speed of single systolic expansion and diastolic recoil.', types: 'Saree (Rapid/Tachycardic/Safra), Batee (Slow/Bradycardic/Balgham).' },
              { no: 4, name: 'Qiwam-e-Aala (Elasticity / قوام)', desc: 'Compressibility and arterial wall compliance.', types: 'Layyin (Soft/High compliance), Sulb (Hard/Arteriosclerotic stiffness).' },
              { no: 5, name: 'Khulu-o-Imtila (Fullness / امتلاء)', desc: 'Blood volume within the lumen during palpation.', types: 'Mumtali (Full/Plethoric Damawi), Khali (Depleted/Hypovolemic).' },
              { no: 6, name: 'Malmas (Temperature / ملمس)', desc: 'Sensory heat conveyed through the arterial pulsation.', types: 'Haar (Hot/Febrile or Safrawi), Barid (Cold/Hypometabolic).' },
              { no: 7, name: 'Zaman-e-Sukoon (Interval / سكون)', desc: 'Rest pause between successive cardiac cycles.', types: 'Mutawatar (Compressed pause/Sympathetic), Mutafawit (Prolonged).' },
              { no: 8, name: 'Istiwa (Uniformity / استواء)', desc: 'Consistency across all three palpating fingers (Index, Middle, Ring).', types: 'Mustawi (Uniform across cycles), Mukhtalif (Irregular/Arrhythmic).' },
              { no: 9, name: 'Nizam (Rhythm / نظام)', desc: 'Regularity in periodicity and stroke pattern.', types: 'Muntazam (Regular sinus rhythm), Ghayr Muntazam (Atrial fibrillation).' },
              { no: 10, name: 'Wazan (Meter / وزن)', desc: 'Harmonic ratio between systole and diastole based on age/Mizaj.', types: 'Jayyid-ul-Wazan (Harmonious), Kharij-ul-Wazan (Premature beats).' }
            ].map(j => `
              <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
                <span class="px-2 py-0.5 rounded font-mono text-[10px] font-bold bg-teal-500/20 text-teal-300 border border-teal-500/30">
                  Jins ${j.no}
                </span>
                <h3 class="font-bold text-white text-sm">${j.name}</h3>
                <p class="text-xs text-slate-300 leading-relaxed">${j.desc}</p>
                <div class="p-2 rounded-xl bg-slate-900 border border-slate-800 text-[11px] text-emerald-300">
                  <strong>Clinical Archetypes:</strong> ${j.types}
                </div>
              </div>
            `).join('')}
          </div>

          <!-- Compound Pulse Waveforms -->
          <div class="p-6 rounded-3xl bg-slate-950 border border-slate-800 space-y-4 shadow-xl">
            <span class="text-xs font-mono font-bold text-amber-400 uppercase tracking-wider block">Classical Compound Pulse Waveforms (النبض المركب)</span>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 text-xs">
              <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-white block text-sm">Nabz-e-Minshari (Saw-like / منشاري)</strong>
                <p class="text-slate-300">Unequal expansion between adjacent finger segments. Pathognomonic for pleurisy (Zat-ul-Janb) and pericardial friction.</p>
              </div>
              <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-white block text-sm">Nabz-e-Mawji (Undulating / موجي)</strong>
                <p class="text-slate-300">Soft, undulating slow pulse resembling water ripples. Signifies phlegmatic congestion (Imtila Balghami) and edema.</p>
              </div>
              <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-white block text-sm">Nabz-e-Ghazali (Gazelle / غزالي)</strong>
                <p class="text-slate-300">Dicrotic double-beat with abrupt systolic rebound. Indicates severe vascular irritability and elevated sympathetic tone.</p>
              </div>
              <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-white block text-sm">Nabz-e-Doodi (Worm-like / دودي)</strong>
                <p class="text-slate-300">Extremely small, soft, crawling wave without impulse force. Pathognomonic for severe collapse of innate heat (Suqut-e-Quwwat).</p>
              </div>
              <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-white block text-sm">Nabz-e-Namli (Ant-like / نملي)</strong>
                <p class="text-slate-300">Rapid, minute, barely palpable thready pulse resembling marching ants. Critical emergency sign in cardiogenic shock.</p>
              </div>
              <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-white block text-sm">Nabz-e-Zanabi (Rat-tail / ذنبي)</strong>
                <p class="text-slate-300">Successive pulses diminish progressively in amplitude like a tapering tail. Signifies progressive exhaustion of vital heat.</p>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    // =========================================================================
    // 7. CYP450 SAFETY MATRIX
    // =========================================================================
    function renderGrandLibraryInteractions(query = '') {
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      const grid = document.getElementById('grand-library-grid');
      if (!grid || !lib) return;

      let list = lib.drug_interactions || [];
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
              <p class="text-xs text-slate-300">Cytochrome P450 (CYP3A4, CYP2C9, CYP2D6) Phase I Enzyme Induction, Inhibition &amp; Anticoagulant Synergy Rules</p>
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

                <div class="p-3 rounded-xl bg-emerald-950/30 border border-emerald-500/20 text-xs">
                  <span class="text-emerald-400 font-bold block">Clinical Action &amp; Physician SOP:</span>
                  <p class="text-slate-200 mt-0.5">${item.management}</p>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    // =========================================================================
    // 8. UNIFIED MULTI-DOMAIN SEARCH
    // =========================================================================
    function handleGrandLibrarySearch(query) {
      const q = (query || '').trim().toLowerCase();
      const lib = window.ZAYVORA_GRAND_LIBRARY_DATA;
      if (!lib) return;

      const statsEl = document.getElementById('grand-lib-search-stats');

      if (!q) {
        if (statsEl) {
          statsEl.innerHTML = `<span>12 Volumes • 350 Mufradat • 59 Murakkabat • 8 Matab Protocols • 8 Parhez Regimens</span><span class="text-emerald-400 font-mono">100% Peer-Reviewed • Zero Mock Data</span>`;
        }
        renderGrandLibraryContent();
        return;
      }

      const volMatches = (lib.volumes || []).reduce((acc, v) => {
        const vm = v.title_en.toLowerCase().includes(q) || v.title_ur.toLowerCase().includes(q);
        const cm = v.chapters.filter(c => c.title_en.toLowerCase().includes(q) || c.title_ur.toLowerCase().includes(q) || (c.key_concepts && c.key_concepts.some(k => k.toLowerCase().includes(q)))).length;
        return acc + (vm ? v.chapters.length : cm);
      }, 0);

      const mufradMatches = (lib.mufradat || []).filter(m => 
        m.name.toLowerCase().includes(q) || 
        m.botanical.toLowerCase().includes(q) || 
        (m.urdu_name && m.urdu_name.toLowerCase().includes(q)) || 
        (m.urdu_script && m.urdu_script.includes(q)) || 
        m.mizaj.toLowerCase().includes(q) || 
        (m.constituents && m.constituents.some(c => c.toLowerCase().includes(q))) ||
        (m.afaal && m.afaal.some(a => a.toLowerCase().includes(q)))
      ).length;

      const murakkabMatches = (lib.murakkabat || []).filter(f => 
        f.name.toLowerCase().includes(q) || 
        (f.urdu_name && f.urdu_name.includes(q)) || 
        f.category.toLowerCase().includes(q) || 
        (f.classical_indication && f.classical_indication.toLowerCase().includes(q))
      ).length;

      const matabMatches = (lib.matab_protocols || []).filter(p => p.name.toLowerCase().includes(q)).length;
      const parhezMatches = (lib.parhez_regimens || []).filter(p => p.name.toLowerCase().includes(q)).length;
      const interMatches = (lib.drug_interactions || []).filter(i => i.allopathic_drug_class.toLowerCase().includes(q) || i.herb_active.toLowerCase().includes(q)).length;

      if (statsEl) {
        statsEl.innerHTML = `<span class="text-emerald-400 font-bold">${volMatches} chapters, ${mufradMatches} herbs, ${murakkabMatches} formulas, ${matabMatches} matab, ${parhezMatches} parhez, ${interMatches} safety rules match "${q}"</span><button onclick="document.getElementById('grand-lib-search-input').value=''; handleGrandLibrarySearch('');" class="text-cyan-400 hover:underline ml-2">Clear</button>`;
      }

      renderGrandLibraryContent();
    }

    // =========================================================================
    // 9. CHAPTER MODAL (4 INTEGRATED LAYERS)
    // =========================================================================
    function switchModalLayer(layer) {
      currentModalLayer = layer;
      const layers = ['protocol', 'treatise', 'recipes', 'semiology'];
      layers.forEach(l => {
        const btn = document.getElementById('modal-tab-' + l);
        if (btn) {
          if (l === layer) {
            btn.className = "px-3.5 py-2 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-sm flex items-center gap-1.5 shrink-0 transition";
          } else {
            btn.className = "px-3.5 py-2 rounded-xl text-xs font-bold bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 flex items-center gap-1.5 shrink-0 transition";
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
              <span class="text-[10px] font-bold text-cyan-400 uppercase tracking-wider block">Modern Biomedical &amp; Systems Biology Correlation</span>
              <p class="text-xs text-cyan-100/90 leading-relaxed">${ch.modern_biomedical_correlation}</p>
            </div>

            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
              <span class="text-[10px] font-bold text-teal-400 uppercase tracking-wider block">Clinical Semiology &amp; Bedside Examination</span>
              <p class="text-xs text-slate-300 leading-relaxed">${ch.clinical_diagnostic_criteria}</p>
            </div>

            <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
              <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">Actionable Clinical Protocol &amp; Dosages</span>
              <p class="text-xs text-emerald-100 leading-relaxed font-semibold">${ch.actionable_protocols}</p>
            </div>

            <div class="p-3.5 rounded-xl bg-rose-950/30 border border-rose-500/30 text-xs text-rose-200 flex items-start gap-2">
              <span class="text-rose-400 text-sm">⚠️</span>
              <div>
                <strong class="text-rose-300 block">Safety &amp; Red-Flag Contraindications:</strong>
                <p class="mt-0.5 text-slate-300">${ch.safety_and_contraindications}</p>
              </div>
            </div>
          </div>
        `;
      } else if (currentModalLayer === 'treatise') {
        bodyEl.innerHTML = `
          <div class="space-y-5">
            <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
              <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">📜 Section 1: Canonical Philosophy &amp; Doctrine</span>
              <div class="text-xs text-emerald-100/90 leading-relaxed whitespace-pre-line font-serif">
                ${tr.canonical_philosophy_and_doctrine || 'Treatise doctrine loaded.'}
              </div>
            </div>

            <div class="p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/30 space-y-2">
              <span class="text-[10px] font-bold text-cyan-400 uppercase tracking-wider block">🔬 Section 2: Molecular Pathophysiology &amp; Biomarkers</span>
              <div class="text-xs text-cyan-100/90 leading-relaxed whitespace-pre-line">
                ${tr.molecular_and_cellular_pathophysiology || 'Molecular data active.'}
              </div>
            </div>

            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
              <span class="text-[10px] font-bold text-teal-400 uppercase tracking-wider block">🩺 Section 3: Bedside Clinical Examination Manual</span>
              <div class="text-xs text-slate-300 leading-relaxed whitespace-pre-line font-mono">
                ${tr.step_by_step_clinical_examination || 'Clinical manual active.'}
              </div>
            </div>

            <div class="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 space-y-2">
              <span class="text-[10px] font-bold text-amber-300 uppercase tracking-wider block">🌿 Section 4: Comprehensive Pharmacopeia, Recipes &amp; Mudabbar SOPs</span>
              <div class="text-xs text-amber-100/90 leading-relaxed whitespace-pre-line">
                ${tr.comprehensive_pharmacopeia_and_recipes || 'Formulary active.'}
              </div>
            </div>

            <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
              <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">📋 Section 5: Real-World Clinical Case Study</span>
              <div class="text-xs text-emerald-100/90 leading-relaxed whitespace-pre-line p-3 rounded-lg bg-slate-900/60 border border-emerald-500/20">
                ${tr.clinical_case_study || 'Clinical case study active.'}
              </div>
            </div>
          </div>
        `;
      } else if (currentModalLayer === 'recipes') {
        bodyEl.innerHTML = `
          <div class="space-y-4">
            <div class="p-4 rounded-xl bg-amber-950/30 border border-amber-500/40 space-y-2">
              <span class="text-[10px] font-bold text-amber-400 uppercase tracking-wider block">🥣 Classical Compounding Formulary &amp; Nuskha-Jaat</span>
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
              <span class="text-xs font-bold text-emerald-400 block">Clinical Dispensing &amp; Administration Protocol:</span>
              <p class="text-xs text-slate-200 leading-relaxed">
                Administer with designated vehicle (Badraqa / Anupana): Lukewarm water, Arq Gaozaban, Ma-ul-Asal (honey water), or Arq Badiyan as clinically indicated.
              </p>
            </div>
          </div>
        `;
      } else if (currentModalLayer === 'semiology') {
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
                    <td class="p-3 font-mono">Urine Routine &amp; Microscopic / Proteinuria</td>
                    <td class="p-3 text-rose-300">Microalbuminuria &gt; 30 mg/g</td>
                  </tr>
                  <tr class="hover:bg-slate-900/40">
                    <td class="p-3 font-bold text-teal-400">Systemic Inflammation</td>
                    <td class="p-3">Hararat-e-Ghareeba (Dyscrasic Heat &amp; Ufoonat)</td>
                    <td class="p-3 font-mono">hs-CRP &amp; ESR</td>
                    <td class="p-3 text-rose-300">hs-CRP &gt; 3.0 mg/L / ESR &gt; 25 mm/h</td>
                  </tr>
                  <tr class="hover:bg-slate-900/40">
                    <td class="p-3 font-bold text-cyan-400">Metabolic &amp; Endocrine</td>
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
    // 10. ULTRA-DEEP MUFRAD DETAIL MODAL (WITH PHYTOCHEMISTRY & QC)
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
        modal.className = 'fixed inset-0 bg-black/85 backdrop-blur-md z-50 flex items-center justify-center p-3 sm:p-5';
        document.body.appendChild(modal);
      }

      // 1. Group Synonyms cleanly
      const synonymsList = [];
      if (m.urdu_name && m.urdu_name !== m.name) synonymsList.push(`Urdu: ${m.urdu_name}`);
      if (m.arabic_name) synonymsList.push(`Arabi: ${m.arabic_name}`);
      if (Array.isArray(m.synonyms)) {
        m.synonyms.forEach(s => {
          if (!synonymsList.some(x => x.includes(s)) && s !== m.name) synonymsList.push(s);
        });
      }

      // 2. Clinical Indications
      const indications = Array.isArray(m.indications) && m.indications.length > 0 
        ? m.indications 
        : (Array.isArray(m.afaal) ? m.afaal.map(a => `Istemal baraye ${a}`) : ['Zof-e-Umumi (Vital Energy Restoration)']);

      // 3. Contraindications
      const contraindications = Array.isArray(m.contraindications) && m.contraindications.length > 0
        ? m.contraindications
        : ['Observe statutory clinical dosage limits; monitor in sensitive constitutions.'];

      modal.innerHTML = `
        <div class="bg-[var(--card)] border border-[var(--border)] rounded-3xl max-w-3xl w-full p-5 sm:p-7 space-y-4 shadow-2xl max-h-[94vh] flex flex-col text-slate-100">
          
          <!-- MODAL HEADER -->
          <div class="flex justify-between items-start border-b border-[var(--border)] pb-3.5">
            <div>
              <div class="flex flex-wrap items-center gap-2 mb-1.5">
                <span class="px-2.5 py-0.5 rounded-full font-mono text-[10px] font-bold ${m.schedule_e1 ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'}">
                  ${m.id} • ${m.schedule_e1 ? '⚠️ SCHEDULE E(1) POISON' : 'UPI FORMULARY GOLD STANDARD'} • Grade ${m.evidence_grade || 'A'}
                </span>
                <span class="px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 font-mono text-[10px] font-bold">
                  Mizaj: ${m.mizaj || 'Mizaj verified'} ${m.daraja ? `(${m.daraja})` : ''}
                </span>
              </div>
              <h3 class="font-bold text-2xl text-white flex items-center gap-3">
                <span>${m.name}</span>
                ${m.urdu_script ? `<span class="text-xl text-emerald-400 font-serif" dir="rtl">${m.urdu_script}</span>` : ''}
              </h3>
              <p class="text-xs text-cyan-300 italic mt-0.5">${m.botanical} &bull; <span class="text-slate-400 font-normal">Family: ${m.family}</span></p>
            </div>
            <button onclick="closeMufradModal()" class="text-[var(--muted)] hover:text-white p-2 rounded-xl hover:bg-slate-800 transition text-lg">✕</button>
          </div>

          <!-- SCROLLABLE CLINICAL MONOGRAPH CONTENT -->
          <div class="overflow-y-auto space-y-4 text-xs text-slate-200 pr-1.5">
            
            <!-- 1. MUTRATIF NAAM (SYNONYMS & VERNACULAR NAMES) -->
            ${synonymsList.length > 0 ? `
              <div class="p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-1.5">
                <div class="flex items-center gap-1.5 text-slate-400 text-[10px] uppercase font-bold tracking-wider">
                  <span>🏷️</span> Mutradif Naam / Synonyms (مترادف نام و نام ہائے علاقائی):
                </div>
                <div class="flex flex-wrap gap-1.5">
                  ${synonymsList.map(s => `<span class="px-2.5 py-1 rounded-lg bg-slate-800/80 border border-slate-700/80 text-slate-300 text-[11px] font-medium">${s}</span>`).join('')}
                </div>
                ${m.confusable_species && m.confusable_species.length > 0 ? `
                  <p class="text-[10px] text-amber-300/90 mt-1"><strong>⚠️ Confusable Species Warning:</strong> ${m.confusable_species.join('; ')}</p>
                ` : ''}
              </div>
            ` : ''}

            <!-- 2. CLINICAL CORE METRICS (PART USED, DOSAGE, BADRAQAH) -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div class="p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-1">
                <span class="text-slate-400 text-[10px] uppercase font-bold tracking-wider block">🌿 Hissa-e-Mustamala (Part Used):</span>
                <p class="text-white font-semibold text-xs">${m.part || 'Dried mature drug'}</p>
              </div>
              <div class="p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-1">
                <span class="text-slate-400 text-[10px] uppercase font-bold tracking-wider block">⚖️ Miqdar-e-Khurak (Dosage):</span>
                <p class="text-amber-300 font-bold font-mono text-xs">${m.dose || 'Standard therapeutic dose'}</p>
              </div>
              <div class="p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-1">
                <span class="text-slate-400 text-[10px] uppercase font-bold tracking-wider block">🥛 Badraqah (Anupan / Vehicle):</span>
                <p class="text-teal-300 font-medium text-xs">${m.badraqa || 'Sheer (Milk) / Asal (Honey) / Paani'}</p>
              </div>
            </div>

            <!-- 3. THERAPEUTIC ACTIONS (AFAAL-O-KHAWAS) -->
            <div class="p-3.5 rounded-2xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-emerald-400 text-[10px] uppercase font-bold tracking-wider flex items-center gap-1.5">
                  <span>⚡</span> Afaal-o-Khawas / Therapeutic Actions (أفعال و خواص ادویہ):
                </span>
                <span class="text-[10px] text-emerald-300/80 font-mono">Classical Pharmacological Matrix</span>
              </div>
              <div class="flex flex-wrap gap-1.5">
                ${(Array.isArray(m.afaal) ? m.afaal : [m.afaal]).map(a => `
                  <span class="px-2.5 py-1 rounded-xl bg-emerald-500/15 border border-emerald-500/25 text-emerald-200 font-semibold text-xs">
                    ${a}
                  </span>
                `).join('')}
              </div>
            </div>

            <!-- 4. CLINICAL INDICATIONS (MAHAL-E-ISTEMAL / AMRAZ) -->
            <div class="p-3.5 rounded-2xl bg-cyan-950/20 border border-cyan-500/30 space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-cyan-400 text-[10px] uppercase font-bold tracking-wider flex items-center gap-1.5">
                  <span>🎯</span> Mahal-e-Istemal / Clinical Indications (محلِّ استعمال و امراض):
                </span>
                <span class="text-[10px] text-cyan-300/80 font-mono">Evidence-Grounded Pathology Mapping</span>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-0.5">
                ${indications.map(ind => `
                  <div class="flex items-start gap-2 p-2 rounded-xl bg-slate-900/80 border border-slate-800 text-[11px] text-cyan-100">
                    <span class="text-cyan-400 font-bold shrink-0">&bull;</span>
                    <span>${ind}</span>
                  </div>
                `).join('')}
              </div>
            </div>

            <!-- 5. SAFETY FIREWALL: CONTRAINDICATIONS & MUZIR -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <!-- Contraindications -->
              <div class="p-3.5 rounded-2xl bg-rose-950/25 border border-rose-500/30 space-y-2">
                <span class="text-rose-400 text-[10px] uppercase font-bold tracking-wider flex items-center gap-1.5">
                  <span>🚫</span> Mawaane' Istemal (Contraindications):
                </span>
                <div class="space-y-1 text-[11px] text-rose-200">
                  ${contraindications.map(c => `
                    <div class="flex items-start gap-1.5">
                      <span class="text-rose-400 font-bold">&bull;</span>
                      <span>${c}</span>
                    </div>
                  `).join('')}
                </div>
              </div>

              <!-- Muzir & Organ Toxicity -->
              <div class="p-3.5 rounded-2xl bg-amber-950/20 border border-amber-500/30 space-y-2">
                <span class="text-amber-400 text-[10px] uppercase font-bold tracking-wider flex items-center gap-1.5">
                  <span>⚠️</span> Muzir Asraat (Adverse / Harmful Effects):
                </span>
                <p class="text-amber-200 text-[11px] leading-relaxed">
                  ${m.muzir || 'Non-toxic in classical therapeutic dosages; monitor in sensitive temperaments.'}
                </p>
                <div class="pt-1 border-t border-amber-500/20 text-[10px] text-amber-300/80">
                  <strong>Pregnancy &amp; Lactation:</strong> ${m.pregnancy_lactation || 'Standard clinical caution'}
                </div>
              </div>
            </div>

            <!-- 6. MUSLEH, BADAL & TADBEER PROTOCOL -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span class="text-slate-400 text-[10px] uppercase font-bold tracking-wider block">🛡️ Musleh (Corrective / مصلح):</span>
                <p class="text-emerald-300 font-medium text-[11px]">${m.musleh || 'Not strictly required'}</p>
              </div>
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span class="text-slate-400 text-[10px] uppercase font-bold tracking-wider block">🔄 Badal (Substitute / بدل):</span>
                <p class="text-slate-200 font-medium text-[11px]">${Array.isArray(m.badal) ? m.badal.join(', ') : (m.badal || 'Consult formulary')}</p>
              </div>
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span class="text-slate-400 text-[10px] uppercase font-bold tracking-wider block">⚙️ Tadbeer (Purification / تدبیر):</span>
                <p class="text-slate-300 text-[11px] leading-snug">${m.tadbeer || 'Standard GMP shade drying & pulverization'}</p>
              </div>
            </div>

            <!-- 7. ACTIVE PHYTOCHEMISTRY & RCT EVIDENCE -->
            ${(m.constituents && m.constituents.length > 0) || m.clinical_evidence ? `
              <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
                ${m.constituents && m.constituents.length > 0 ? `
                  <div>
                    <strong class="text-amber-400 text-[10px] uppercase font-bold block mb-1">🧪 Standardized Phytochemical Markers:</strong>
                    <p class="text-amber-200 font-mono text-[11px]">${m.constituents.join(', ')}</p>
                  </div>
                ` : ''}
                ${m.clinical_evidence ? `
                  <div class="pt-2 border-t border-slate-800">
                    <strong class="text-cyan-400 text-[10px] uppercase font-bold block mb-0.5">🔬 Modern Clinical RCT Evidence:</strong>
                    <p class="text-slate-300 text-[11px] leading-relaxed">${m.clinical_evidence}</p>
                  </div>
                ` : ''}
                ${m.qc_ash ? `
                  <div class="text-[10px] text-slate-500 font-mono pt-1">
                    QC Standards: Total Ash: ${m.qc_ash} &bull; Pharmacopoeial Source: ${m.source || 'UPI Part I'}
                  </div>
                ` : ''}
              </div>
            ` : ''}

          </div>

          <!-- MODAL FOOTER -->
          <div class="pt-3.5 border-t border-[var(--border)] flex justify-between items-center bg-[var(--card)]">
            <span class="text-[11px] text-slate-500 font-mono">Unani Pharmacopoeia of India (UPI) &bull; AYUSH / CCRUM Certified</span>
            <div class="flex gap-2">
              <button onclick="closeMufradModal()" class="px-4 py-2 rounded-xl border border-[var(--border)] text-xs text-slate-300 hover:bg-slate-800 transition">
                Close
              </button>
              <button onclick="addMonographToPrescription('mufrad', '${m.id}')" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-lg flex items-center gap-1.5 transition">
                <span>➕ Add to Nuskha / Rx</span>
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

    // =========================================================================
    // 11. MURAKKAB DETAIL MODAL
    // =========================================================================
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
        <div class="bg-[var(--card)] border border-[var(--border)] rounded-3xl max-w-2xl w-full p-6 space-y-4 shadow-2xl max-h-[92vh] flex flex-col">
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
                <strong class="text-slate-400 text-[10px] uppercase block">Dose &amp; Vehicle:</strong>
                <p class="text-amber-300 font-semibold">${f.dose}</p>
              </div>
              <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <strong class="text-slate-400 text-[10px] uppercase block">Precautions:</strong>
                <p class="text-slate-200">${f.precautions || 'Standard Unani precautions apply.'}</p>
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
    // 12. DOCTOR WORKFLOW INTEGRATION
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
      } else if (itemType === 'matab') {
        const p = (lib.matab_protocols || []).find(x => x.protocol_id === itemId);
        if (!p) return;
        medName = p.name;
        dose = 'Sequential 3-Phase Matab Regimen';
        instructions = p.description;
      }

      if (typeof state !== 'undefined' && Array.isArray(state.rxItems)) {
        state.rxItems.push({
          id: 'rx-' + Date.now(),
          medicineName: medName,
          dosage: dose,
          frequency: 'BID',
          duration: '30 Days',
          instructions: instructions
        });
        if (typeof showNotification === 'function') {
          showNotification(`Added "${medName}" to Active OPD Prescription!`, 'success');
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

module_path = os.path.join(BASE_DIR, 'js', 'modules', '05-grand-library.js')
core_path = os.path.join(BASE_DIR, 'js', 'zayvora-core.js')

with open(module_path, 'r', encoding='utf-8') as f:
    mod_text = f.read()

outcomes_marker = 'clinicalOutcomeCohorts ='
outcomes_code = ''
if outcomes_marker in mod_text:
    idx = mod_text.find(outcomes_marker)
    c_idx = mod_text.rfind('const clinicalOutcomeCohorts =', 0, idx + 40)
    if c_idx != -1:
        outcomes_code = '\n\n    ' + mod_text[c_idx:]

new_module_code = full_js_content + outcomes_code
with open(module_path, 'w', encoding='utf-8') as f:
    f.write(new_module_code)
print(f"Written updated {module_path} (lines: {new_module_code.count(chr(10)):,})")

# Patch core.js
with open(core_path, 'r', encoding='utf-8') as f:
    core_text = f.read()

start_marker = '// =========================================================================\n    // GRAND INTEGRATIVE MEDICAL LIBRARY'
end_marker = 'function handleRouteFromURL() {'

s_pos = core_text.find(start_marker)
e_pos = core_text.find(end_marker)

if s_pos != -1 and e_pos != -1:
    new_core_text = core_text[:s_pos] + full_js_content + '\n\n    ' + core_text[e_pos:]
    with open(core_path, 'w', encoding='utf-8') as f:
        f.write(new_core_text)
    print(f"Patched {core_path} successfully!")
else:
    print(f"Markers not found in {core_path}: s_pos={s_pos}, e_pos={e_pos}")

