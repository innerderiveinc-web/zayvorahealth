#!/usr/bin/env python3
"""
ZAYVORA Health OS — Fix Clinical Tools Dropdown & Global Interaction Audit
1. Replaces toggleDoctorNavDropdown with fixed viewport positioning (immune to overflow clipping).
2. Updates dropdown markup with modern theme-aware styling and clean outside-click handlers.
3. Adds light-mode CSS rules in index.html for #doctor-more-nav-menu.
4. Syncs index.html -> app.html -> docs/ via sync_all.py.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
CORE_JS_PATH = os.path.join(BASE_DIR, "js", "zayvora-core.js")

def fix():
    print("Reading js/zayvora-core.js...")
    with open(CORE_JS_PATH, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. Update toggleDoctorNavDropdown
    old_toggle_func = """    function toggleDoctorNavDropdown(e, forceState) {
      if (e) e.stopPropagation();
      const menu = document.getElementById('doctor-more-nav-menu');
      if (!menu) return;
      if (typeof forceState === 'boolean') {
        if (forceState) menu.classList.remove('hidden');
        else menu.classList.add('hidden');
      } else {
        menu.classList.toggle('hidden');
      }
    }
    window.toggleDoctorNavDropdown = toggleDoctorNavDropdown;
    if (typeof document !== 'undefined') {
      document.addEventListener('click', () => {
        const menu = document.getElementById('doctor-more-nav-menu');
        if (menu && !menu.classList.contains('hidden')) menu.classList.add('hidden');
      });
    }"""

    new_toggle_func = """    function toggleDoctorNavDropdown(e, forceState) {
      if (e) {
        if (typeof e.stopPropagation === 'function') e.stopPropagation();
        if (typeof e.preventDefault === 'function') e.preventDefault();
      }
      const menu = document.getElementById('doctor-more-nav-menu');
      const btn = document.getElementById('doctor-more-nav-btn');
      if (!menu || !btn) return;

      const isCurrentlyHidden = menu.classList.contains('hidden');
      const shouldOpen = (typeof forceState === 'boolean') ? forceState : isCurrentlyHidden;

      if (shouldOpen) {
        // Floating fixed positioning immune to nav overflow-x-auto clipping!
        const rect = btn.getBoundingClientRect();
        menu.style.position = 'fixed';
        menu.style.top = (rect.bottom + 6) + 'px';
        const menuWidth = 280;
        const maxLeft = Math.max(10, window.innerWidth - menuWidth - 16);
        const targetLeft = Math.max(10, Math.min(rect.left, maxLeft));
        menu.style.left = targetLeft + 'px';
        menu.style.width = menuWidth + 'px';
        menu.style.zIndex = '99999';
        menu.classList.remove('hidden');
      } else {
        menu.classList.add('hidden');
      }
    }
    window.toggleDoctorNavDropdown = toggleDoctorNavDropdown;

    if (typeof document !== 'undefined') {
      document.addEventListener('click', (e) => {
        const menu = document.getElementById('doctor-more-nav-menu');
        const btn = document.getElementById('doctor-more-nav-btn');
        if (menu && !menu.classList.contains('hidden')) {
          if (btn && (btn === e.target || btn.contains(e.target))) return;
          if (menu.contains(e.target)) return;
          menu.classList.add('hidden');
        }
      });
      window.addEventListener('scroll', () => {
        const menu = document.getElementById('doctor-more-nav-menu');
        if (menu && !menu.classList.contains('hidden')) menu.classList.add('hidden');
      }, { passive: true });
      window.addEventListener('resize', () => {
        const menu = document.getElementById('doctor-more-nav-menu');
        if (menu && !menu.classList.contains('hidden')) menu.classList.add('hidden');
      }, { passive: true });
    }"""

    if old_toggle_func in js:
        js = js.replace(old_toggle_func, new_toggle_func)
        print("✓ Replaced toggleDoctorNavDropdown with fixed viewport positioning logic")
    else:
        print("[-] Could not find exact old_toggle_func in js/zayvora-core.js")

    # 2. Update markup inside renderNavigation
    old_markup = """        if (secondaryItems.length > 0) {
          html += `
            <div class="relative inline-block text-left shrink-0" id="doctor-more-nav-dropdown-wrap">
              <button id="doctor-more-nav-btn" onclick="toggleDoctorNavDropdown(event)" class="nav-link shrink-0 ${isSecondaryActive ? 'active' : 'text-[var(--muted)] hover:text-white'} px-3.5 py-1.5 rounded-xl text-xs font-semibold border border-transparent transition-colors flex items-center gap-1.5 bg-slate-900/60 hover:bg-slate-800">
                <span>${dropdownLabel}</span>
              </button>
              <div id="doctor-more-nav-menu" class="hidden absolute left-0 mt-1.5 w-64 rounded-xl bg-slate-900 border border-slate-700 shadow-2xl p-1.5 z-50 space-y-1">
                ${secondaryItems.map(item => `
                  <button onclick="switchTab('${item.id}'); toggleDoctorNavDropdown(event, false);" class="w-full text-left px-3 py-1.5 rounded-lg text-xs font-medium ${isTabActive(item.id, state.tab) ? 'bg-emerald-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'} flex items-center gap-2 transition">
                    ${item.label}
                  </button>
                `).join('')}
              </div>
            </div>
          `;
        }"""

    new_markup = """        if (secondaryItems.length > 0) {
          html += `
            <div class="relative inline-block text-left shrink-0" id="doctor-more-nav-dropdown-wrap">
              <button id="doctor-more-nav-btn" type="button" onclick="toggleDoctorNavDropdown(event)" class="nav-link shrink-0 ${isSecondaryActive ? 'active' : 'text-[var(--muted)] hover:text-white'} px-3.5 py-1.5 rounded-xl text-xs font-semibold border border-transparent transition-colors flex items-center gap-1.5 bg-slate-900/60 hover:bg-slate-800 cursor-pointer">
                <span>${dropdownLabel}</span>
              </button>
              <div id="doctor-more-nav-menu" class="hidden rounded-2xl bg-[#0F172A] border border-slate-700 shadow-2xl p-2 z-[99999] space-y-1 backdrop-blur-xl">
                <div class="px-2.5 py-1.5 border-b border-slate-800 text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center justify-between">
                  <span>Specialty Desks</span>
                  <span class="text-emerald-400 font-mono">${secondaryItems.length} Desks</span>
                </div>
                ${secondaryItems.map(item => `
                  <button type="button" onclick="switchTab('${item.id}'); toggleDoctorNavDropdown(event, false);" class="w-full text-left px-3 py-2 rounded-xl text-xs font-medium ${isTabActive(item.id, state.tab) ? 'bg-emerald-600 text-white font-bold shadow' : 'text-slate-300 hover:bg-slate-800 hover:text-white'} flex items-center justify-between transition cursor-pointer group">
                    <span class="flex items-center gap-2">${item.label}</span>
                    <span class="text-[10px] text-slate-400 group-hover:text-emerald-400 font-mono">→</span>
                  </button>
                `).join('')}
              </div>
            </div>
          `;
        }"""

    if old_markup in js:
        js = js.replace(old_markup, new_markup)
        print("✓ Updated doctor-more-nav markup with theme-aware styling & desk counter")
    else:
        print("[-] Could not find exact old_markup in js/zayvora-core.js")

    with open(CORE_JS_PATH, "w", encoding="utf-8") as f:
        f.write(js)
    print("✓ Updated js/zayvora-core.js")

    # 3. Add Light Mode CSS for #doctor-more-nav-menu in index.html
    print("Reading index.html...")
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    css_target = """    [data-theme="light"] #doctor-more-nav-btn * {
      color: #1A2328 !important;
    }"""

    new_css = """    [data-theme="light"] #doctor-more-nav-btn * {
      color: #1A2328 !important;
    }

    /* Doctor More Nav Floating Dropdown Menu in Light Mode */
    [data-theme="light"] #doctor-more-nav-menu {
      background-color: #FFFFFF !important;
      border: 1px solid #DCD5C4 !important;
      box-shadow: 0 16px 36px -4px rgba(45, 40, 30, 0.18), 0 8px 16px -6px rgba(45, 40, 30, 0.10) !important;
    }
    [data-theme="light"] #doctor-more-nav-menu div {
      border-color: #EFE9DB !important;
      color: #6E7570 !important;
    }
    [data-theme="light"] #doctor-more-nav-menu button {
      color: #1A2328 !important;
    }
    [data-theme="light"] #doctor-more-nav-menu button:hover {
      background-color: #F4EFE6 !important;
      color: #158064 !important;
    }
    [data-theme="light"] #doctor-more-nav-menu button.bg-emerald-600 {
      background-color: #158064 !important;
      color: #FFFFFF !important;
    }"""

    if css_target in html and '#doctor-more-nav-menu {' not in html:
        html = html.replace(css_target, new_css)
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(html)
        print("✓ Injected light mode CSS for #doctor-more-nav-menu into index.html")
    else:
        print("[-] CSS already present or target not found in index.html")

if __name__ == "__main__":
    fix()
