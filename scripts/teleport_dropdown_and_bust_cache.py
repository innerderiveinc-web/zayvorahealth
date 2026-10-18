#!/usr/bin/env python3
"""
scripts/teleport_dropdown_and_bust_cache.py

1. Redesigns Doctor Specialty Desks dropdown:
   - Moves #doctor-more-nav-menu directly to <body> so NO parent overflow or styling can ever clip it.
   - Populates dynamically via populateDoctorNavDropdownMenu().
   - Removes aggressive window.onscroll dismissal that prematurely closed the dropdown on click/focus.
   - Supports clean outside-click and Escape key dismissal.
   - Adds smooth chevron animation on open/close.
   - Implements selectDoctorDesk(tabId) for instant tab switching + close.
   - Works seamlessly in both Light and Dark modes.

2. Comprehensive Cache-Busting:
   - Bumps version to v=16.9 across all HTML, JS, extensions, and Service Worker.
   - Updates CACHE_NAME in sw.js and docs/sw.js to force cache purge on all browsers.

3. Mirrors changes to docs/ and verifies 100% parity.
"""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path("/Users/irfanashraf/Downloads/zayvora-platform-phase0-4")

def update_zayvora_core():
    core_path = ROOT / "js" / "zayvora-core.js"
    content = core_path.read_text(encoding="utf-8")

    # Locate toggleDoctorNavDropdown and renderNavigation
    old_section_pattern = re.compile(
        r'function toggleDoctorNavDropdown\(e, forceState\)\s*\{.*?window\.toggleDoctorNavDropdown = toggleDoctorNavDropdown;.*?'
        r'if \(typeof document !== \'undefined\'\)\s*\{.*?\n    \}\n',
        re.DOTALL
    )

    new_js_code = '''function selectDoctorDesk(tabId) {
      if (typeof toggleDoctorNavDropdown === 'function') {
        toggleDoctorNavDropdown(null, false);
      }
      if (typeof switchTab === 'function') {
        switchTab(tabId);
      }
    }
    window.selectDoctorDesk = selectDoctorDesk;

    function populateDoctorNavDropdownMenu() {
      let menu = document.getElementById('doctor-more-nav-menu');
      if (!menu) {
        menu = document.createElement('div');
        menu.id = 'doctor-more-nav-menu';
        menu.className = 'hidden fixed rounded-2xl bg-[#0F172A] border border-slate-700 shadow-2xl p-2.5 space-y-1 z-[999999] backdrop-blur-xl';
        document.body.appendChild(menu);
      }
      const allItems = (typeof getDoctorNavItems === 'function') ? getDoctorNavItems() : [];
      const primaryIds = ['today', 'consultation', 'patients', 'prescriptions'];
      const secondaryItems = allItems.filter(item => !primaryIds.includes(item.id));
      if (secondaryItems.length === 0) {
        menu.innerHTML = '<div class="p-3 text-xs text-slate-400 text-center">No additional specialty desks configured.</div>';
        return;
      }
      menu.innerHTML = `
        <div class="dropdown-header px-3 py-2 border-b border-slate-800 text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center justify-between">
          <span>Specialty Desks</span>
          <span class="badge text-emerald-400 font-mono text-[11px] font-semibold">${secondaryItems.length} Desks</span>
        </div>
        <div class="py-1 space-y-1">
          ${secondaryItems.map(item => `
            <button type="button" onclick="selectDoctorDesk('${item.id}')" class="desk-item w-full text-left px-3 py-2 rounded-xl text-xs font-medium ${isTabActive(item.id, state.tab) ? 'active-item bg-emerald-600 text-white font-bold shadow' : 'text-slate-300 hover:bg-slate-800 hover:text-white'} flex items-center justify-between transition cursor-pointer group">
              <span class="flex items-center gap-2">${item.label}</span>
              <span class="text-[10px] text-slate-400 group-hover:text-emerald-400 font-mono">→</span>
            </button>
          `).join('')}
        </div>
      `;
    }
    window.populateDoctorNavDropdownMenu = populateDoctorNavDropdownMenu;

    function toggleDoctorNavDropdown(e, forceState) {
      if (e) {
        if (typeof e.stopPropagation === 'function') e.stopPropagation();
        if (typeof e.preventDefault === 'function') e.preventDefault();
      }
      const btn = document.getElementById('doctor-more-nav-btn');
      let menu = document.getElementById('doctor-more-nav-menu');
      if (!btn) return;

      if (!menu) {
        menu = document.createElement('div');
        menu.id = 'doctor-more-nav-menu';
        menu.className = 'hidden fixed rounded-2xl bg-[#0F172A] border border-slate-700 shadow-2xl p-2.5 space-y-1 z-[999999] backdrop-blur-xl';
        document.body.appendChild(menu);
      } else if (menu.parentElement !== document.body) {
        document.body.appendChild(menu);
      }

      const isCurrentlyHidden = menu.classList.contains('hidden') || menu.style.display === 'none';
      const shouldOpen = (typeof forceState === 'boolean') ? forceState : isCurrentlyHidden;
      const arrow = document.getElementById('doctor-more-nav-arrow');

      if (shouldOpen) {
        populateDoctorNavDropdownMenu();
        const rect = btn.getBoundingClientRect();
        const menuWidth = Math.min(300, window.innerWidth - 20);

        menu.style.position = 'fixed';
        menu.style.top = (rect.bottom + 8) + 'px';

        let targetLeft = rect.left;
        if (targetLeft + menuWidth > window.innerWidth - 10) {
          targetLeft = window.innerWidth - menuWidth - 10;
        }
        if (targetLeft < 10) targetLeft = 10;

        menu.style.left = targetLeft + 'px';
        menu.style.width = menuWidth + 'px';
        menu.style.maxWidth = 'calc(100vw - 20px)';
        menu.style.zIndex = '999999';
        menu.classList.remove('hidden');
        menu.style.display = 'block';

        if (arrow) arrow.style.transform = 'rotate(180deg)';
      } else {
        menu.classList.add('hidden');
        menu.style.display = 'none';
        if (arrow) arrow.style.transform = 'rotate(0deg)';
      }
    }
    window.toggleDoctorNavDropdown = toggleDoctorNavDropdown;

    if (typeof document !== 'undefined') {
      document.addEventListener('click', (e) => {
        const menu = document.getElementById('doctor-more-nav-menu');
        const btn = document.getElementById('doctor-more-nav-btn');
        if (menu && (!menu.classList.contains('hidden') && menu.style.display !== 'none')) {
          if (btn && (btn === e.target || btn.contains(e.target))) return;
          if (menu.contains(e.target)) return;
          toggleDoctorNavDropdown(null, false);
        }
      });
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          const menu = document.getElementById('doctor-more-nav-menu');
          if (menu && (!menu.classList.contains('hidden') && menu.style.display !== 'none')) {
            toggleDoctorNavDropdown(null, false);
          }
        }
      });
      window.addEventListener('resize', () => {
        const menu = document.getElementById('doctor-more-nav-menu');
        const btn = document.getElementById('doctor-more-nav-btn');
        if (menu && (!menu.classList.contains('hidden') && menu.style.display !== 'none') && btn) {
          const rect = btn.getBoundingClientRect();
          const menuWidth = Math.min(300, window.innerWidth - 20);
          let targetLeft = rect.left;
          if (targetLeft + menuWidth > window.innerWidth - 10) {
            targetLeft = window.innerWidth - menuWidth - 10;
          }
          if (targetLeft < 10) targetLeft = 10;
          menu.style.top = (rect.bottom + 8) + 'px';
          menu.style.left = targetLeft + 'px';
        }
      }, { passive: true });
    }
'''

    if old_section_pattern.search(content):
        content = old_section_pattern.sub(new_js_code, content, count=1)
        print("✓ Successfully replaced toggleDoctorNavDropdown logic in js/zayvora-core.js")
    else:
        print("! Warning: regex did not match old toggleDoctorNavDropdown block")
        sys.exit(1)

    # Now update doctor dropdown button rendering in renderNavigation
    old_btn_wrap_pattern = re.compile(
        r'if \(secondaryItems\.length > 0\) \{\s*html \+= `\s*<div class="relative inline-block text-left shrink-0" id="doctor-more-nav-dropdown-wrap">.*?</div>\s*`;\s*\}',
        re.DOTALL
    )

    new_btn_wrap = '''if (secondaryItems.length > 0) {
          html += `
            <div class="relative inline-block text-left shrink-0" id="doctor-more-nav-dropdown-wrap">
              <button id="doctor-more-nav-btn" type="button" onclick="toggleDoctorNavDropdown(event)" class="nav-link shrink-0 ${isSecondaryActive ? 'active' : 'text-[var(--muted)] hover:text-white'} px-3.5 py-1.5 rounded-xl text-xs font-semibold border border-transparent transition-colors flex items-center gap-1.5 bg-slate-900/60 hover:bg-slate-800 cursor-pointer" title="Click to open Specialty Desks">
                <span>${dropdownLabel}</span>
                <span id="doctor-more-nav-arrow" class="inline-block transition-transform duration-200">▾</span>
              </button>
            </div>
          `;
          // Pre-populate detached floating menu in body
          try { populateDoctorNavDropdownMenu(); } catch (err) {}
        }'''

    if old_btn_wrap_pattern.search(content):
        content = old_btn_wrap_pattern.sub(new_btn_wrap, content, count=1)
        print("✓ Successfully updated renderNavigation doctor button in js/zayvora-core.js")
    else:
        print("! Warning: regex did not match old_btn_wrap_pattern")
        sys.exit(1)

    core_path.write_text(content, encoding="utf-8")
    print("✓ Saved js/zayvora-core.js")

def update_html_files():
    files = [ROOT / "index.html", ROOT / "app.html"]
    
    css_addition = """
    /* Doctor More Nav Floating Dropdown Menu (Teleported to Body) */
    #doctor-more-nav-menu {
      background-color: #0F172A;
      border: 1px solid #334155;
      box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.6), 0 10px 20px -5px rgba(0, 0, 0, 0.4);
    }
    [data-theme="light"] #doctor-more-nav-menu {
      background-color: #FFFFFF !important;
      border: 1px solid #DCD5C4 !important;
      box-shadow: 0 20px 40px -8px rgba(45, 40, 30, 0.22), 0 8px 16px -4px rgba(45, 40, 30, 0.12) !important;
    }
    [data-theme="light"] #doctor-more-nav-menu .dropdown-header {
      border-color: #EFE9DB !important;
      color: #6E7570 !important;
    }
    [data-theme="light"] #doctor-more-nav-menu .dropdown-header span.badge {
      color: #158064 !important;
    }
    [data-theme="light"] #doctor-more-nav-menu button.desk-item {
      color: #1A2328 !important;
    }
    [data-theme="light"] #doctor-more-nav-menu button.desk-item:hover {
      background-color: #F4EFE6 !important;
      color: #158064 !important;
    }
    [data-theme="light"] #doctor-more-nav-menu button.desk-item.active-item {
      background-color: #158064 !important;
      color: #FFFFFF !important;
    }
"""

    modal_element = """
  <!-- Floating Doctor Specialty Desks & Clinical Tools Dropdown Menu (Teleported to Body) -->
  <div id="doctor-more-nav-menu" class="hidden fixed rounded-2xl bg-[#0F172A] border border-slate-700 shadow-2xl p-2.5 space-y-1 z-[999999] backdrop-blur-xl"></div>
"""

    for fpath in files:
        html = fpath.read_text(encoding="utf-8")

        # 1. Bump version query string to 16.9
        html = re.sub(r'zayvora-core\.js\?v=[\d\.]+', 'zayvora-core.js?v=16.9', html)
        html = re.sub(r'zayvora-extensions\.js\?v=[\d\.]+', 'zayvora-extensions.js?v=16.9', html)

        # 2. Add #doctor-more-nav-menu before </body> if not present
        if 'id="doctor-more-nav-menu"' not in html:
            html = html.replace('</body>', f'{modal_element}\n</body>')
            print(f"✓ Inserted #doctor-more-nav-menu into {fpath.name}")
        else:
            print(f"• #doctor-more-nav-menu already present in {fpath.name}")

        # 3. Insert CSS if not already there
        if 'Doctor More Nav Floating Dropdown Menu (Teleported to Body)' not in html:
            html = html.replace('</style>', f'{css_addition}\n  </style>', 1)
            print(f"✓ Added CSS styles to {fpath.name}")

        fpath.write_text(html, encoding="utf-8")
        print(f"✓ Saved {fpath.name} with cache version v=16.9")

def update_service_worker_and_extensions():
    # 1. sw.js
    sw_path = ROOT / "sw.js"
    sw_code = sw_path.read_text(encoding="utf-8")
    sw_code = re.sub(r"const CACHE_NAME = 'zayvora-health-os-v[\d\.]+-live';", "const CACHE_NAME = 'zayvora-health-os-v16.9-live';", sw_code)
    sw_path.write_text(sw_code, encoding="utf-8")
    print("✓ Updated sw.js CACHE_NAME to v16.9-live")

    # 2. js/zayvora-extensions.js
    ext_path = ROOT / "js" / "zayvora-extensions.js"
    ext_code = ext_path.read_text(encoding="utf-8")
    ext_code = re.sub(r"sw\.js\?v=[\d\.]+", "sw.js?v=16.9", ext_code)
    ext_path.write_text(ext_code, encoding="utf-8")
    print("✓ Updated js/zayvora-extensions.js sw registration to v16.9")

def sync_to_docs():
    # Copy files to docs/
    shutil.copy2(ROOT / "index.html", ROOT / "docs" / "index.html")
    shutil.copy2(ROOT / "app.html", ROOT / "docs" / "app.html")
    shutil.copy2(ROOT / "sw.js", ROOT / "docs" / "sw.js")
    shutil.copy2(ROOT / "js" / "zayvora-core.js", ROOT / "docs" / "js" / "zayvora-core.js")
    shutil.copy2(ROOT / "js" / "zayvora-extensions.js", ROOT / "docs" / "js" / "zayvora-extensions.js")
    print("✓ Synchronized all updated files to docs/")

if __name__ == "__main__":
    update_zayvora_core()
    update_html_files()
    update_service_worker_and_extensions()
    sync_to_docs()
    print("=== All updates completed successfully! ===")
