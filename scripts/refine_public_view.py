#!/usr/bin/env python3
"""
scripts/refine_public_view.py

Refines public view before sign-in:
1. Hides edition switcher (#edition-mode-switcher) on the public website.
2. Hides Grand Bookshelf button (#header-bookshelf-btn) on public website, showing only for authenticated clinicians.
3. Clears password auto-fill in prefillLogin() so plaintext passwords are never injected into password field.
4. Syncs index.html, app.html, js/zayvora-core.js, sw.js to docs/ and root.
"""

import re
from pathlib import Path

ROOT = Path("/Users/irfanashraf/Downloads/zayvora-platform-phase0-4")

def update_html(filepath: Path):
    content = filepath.read_text(encoding="utf-8")

    # 1. Add id="edition-mode-switcher" and ensure it is hidden by default
    content = re.sub(
        r'<div class="hidden sm:flex items-center bg-slate-900/90 border border-slate-700/80 rounded-xl p-0\.5 shadow-sm shrink-0">\s*<button id="btn-edition-clinic"',
        '<div id="edition-mode-switcher" class="hidden items-center bg-slate-900/90 border border-slate-700/80 rounded-xl p-0.5 shadow-sm shrink-0">\n          <button id="btn-edition-clinic"',
        content
    )

    # 2. Make header-bookshelf-btn hidden by default (no md:flex initially)
    content = re.sub(
        r'<button id="header-bookshelf-btn" onclick="openGrandCorpusModal\(\)" class="[^"]*"',
        '<button id="header-bookshelf-btn" onclick="openGrandCorpusModal()" class="hidden bg-slate-900 border border-blue-500/40 hover:border-blue-400 text-blue-300 hover:text-white font-bold text-xs rounded-xl px-2.5 py-1.5 focus:outline-none cursor-pointer transition shadow-sm items-center gap-1.5 shrink-0"',
        content
    )

    # 3. Ensure header-diagnostic-btn is hidden by default
    content = re.sub(
        r'<button id="header-diagnostic-btn" onclick="toggleGlobalToolsModal\(true\)" class="[^"]*"',
        '<button id="header-diagnostic-btn" onclick="toggleGlobalToolsModal(true)" class="hidden bg-slate-900 border border-emerald-500/40 hover:border-emerald-400 text-emerald-300 hover:text-white font-bold text-xs rounded-xl px-2.5 py-1.5 focus:outline-none cursor-pointer transition shadow-sm items-center gap-1.5 shrink-0"',
        content
    )

    # 4. Version cache bump to 17.2
    content = re.sub(r'zayvora-core\.js\?v=[\d\.]+', 'zayvora-core.js?v=17.2', content)
    content = re.sub(r'zayvora-extensions\.js\?v=[\d\.]+', 'zayvora-extensions.js?v=17.2', content)

    filepath.write_text(content, encoding="utf-8")
    print(f"✓ Updated {filepath.relative_to(ROOT)}")

def update_core_js():
    core_path = ROOT / "js" / "zayvora-core.js"
    content = core_path.read_text(encoding="utf-8")

    # 1. Update prefillLogin to NOT fill password
    old_prefill_target = """      const emailInput = document.getElementById('login-input-email');
      const passInput = document.getElementById('login-input-password');
      if (emailInput) emailInput.value = p.email;
      if (passInput) {
        passInput.value = p.pass || 'doctor123';
        passInput.focus();
      }"""

    new_prefill_target = """      const emailInput = document.getElementById('login-input-email');
      const passInput = document.getElementById('login-input-password');
      if (emailInput) emailInput.value = p.email;
      if (passInput) {
        passInput.value = '';
        passInput.placeholder = 'Enter password for ' + (p.label || p.name);
        passInput.focus();
      }"""

    if old_prefill_target in content:
        content = content.replace(old_prefill_target, new_prefill_target)
        print("✓ Updated prefillLogin() to clear password field")
    else:
        print("! Note: old_prefill_target not found in zayvora-core.js")

    # 2. Add header-bookshelf-btn control inside updateAuthHeaderUI
    old_auth_ui = """      // Contextual Header Diagnostic Launcher (Hidden from header to prevent clutter; accessible in Today tray)
      const diagBtn = document.getElementById('header-diagnostic-btn');
      if (diagBtn) {
        if (isSuperAdmin) {
          diagBtn.classList.remove('hidden');
          diagBtn.classList.add('flex');
        } else {
          diagBtn.classList.add('hidden');
          diagBtn.classList.remove('flex');
        }
      }"""

    new_auth_ui = """      // Contextual Header Diagnostic Launcher (Hidden from header to prevent clutter; accessible in Today tray)
      const diagBtn = document.getElementById('header-diagnostic-btn');
      if (diagBtn) {
        if (isSuperAdmin && state.role !== 'website') {
          diagBtn.classList.remove('hidden');
          diagBtn.classList.add('flex');
        } else {
          diagBtn.classList.add('hidden');
          diagBtn.classList.remove('flex');
        }
      }

      // Grand Medical Bookshelf (Available for Clinicians & Researchers inside OS, hidden on public website)
      const bookshelfBtn = document.getElementById('header-bookshelf-btn');
      if (bookshelfBtn) {
        if (state.role !== 'website' && state.currentUser) {
          bookshelfBtn.classList.remove('hidden');
          bookshelfBtn.classList.add('flex');
        } else {
          bookshelfBtn.classList.add('hidden');
          bookshelfBtn.classList.remove('flex');
        }
      }"""

    if old_auth_ui in content:
        content = content.replace(old_auth_ui, new_auth_ui)
        print("✓ Updated updateAuthHeaderUI() with bookshelf and diagnostic visibility guards")
    else:
        print("! Note: old_auth_ui not found in zayvora-core.js")

    core_path.write_text(content, encoding="utf-8")
    print(f"✓ Saved updated {core_path.relative_to(ROOT)}")

def sync_docs():
    docs_dir = ROOT / "docs"
    # sync index.html, app.html, sw.js, js/
    for fn in ["index.html", "app.html", "sw.js"]:
        src = ROOT / fn
        dst = docs_dir / fn
        if src.exists():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"✓ Synced {fn} to docs/")

    for fn in ["zayvora-core.js", "zayvora-extensions.js"]:
        src = ROOT / "js" / fn
        dst = docs_dir / "js" / fn
        if src.exists():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"✓ Synced js/{fn} to docs/js/")

if __name__ == "__main__":
    update_html(ROOT / "index.html")
    update_html(ROOT / "app.html")
    update_core_js()
    sync_docs()
    print("=== Refine Public View Completed Successfully ===")
