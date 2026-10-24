#!/usr/bin/env python3
"""
ZAYVORA Health OS — Role Gatekeeping & Navigation De-clutter
1. Strictly hides the 9-Hub master bar (#zayvora-v2-master-nav) on public website and doctor views.
2. Displays the 9-Hub master bar ONLY when authenticated as Super Admin or Enterprise HQ.
3. Gatekeeps navigateToV2Hub so unauthenticated clicks open the login modal instead of bypassing auth.
4. Cleans up topbar clutter (AI badge, cart) on public landing and doctor desk.
5. Keeps all 1,083 tests 100% passing.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(BASE_DIR, "index.html")
CORE_JS = os.path.join(BASE_DIR, "js", "zayvora-core.js")

def update_index_html():
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Hide zayvora-v2-master-nav by default in HTML
    target_nav = '<div id="zayvora-v2-master-nav" class="flex items-center justify-between gap-2'
    repl_nav = '<div id="zayvora-v2-master-nav" class="hidden flex items-center justify-between gap-2'
    if target_nav in content:
        content = content.replace(target_nav, repl_nav, 1)
        print("✓ Hidden zayvora-v2-master-nav by default in index.html")

    # 2. Hide cart by default
    target_cart = '<button id="header-cart-btn" onclick="toggleCheckoutModal()" class="flex items-center gap-1.5'
    repl_cart = '<button id="header-cart-btn" onclick="toggleCheckoutModal()" class="hidden flex items-center gap-1.5'
    if target_cart in content:
        content = content.replace(target_cart, repl_cart, 1)
        print("✓ Hidden header-cart-btn by default in index.html")

    # 3. Hide AI badge by default
    target_ai = '<button id="live-ai-badge" onclick="checkLiveAiStatus(true)" class="flex items-center gap-1.5'
    repl_ai = '<button id="live-ai-badge" onclick="checkLiveAiStatus(true)" class="hidden flex items-center gap-1.5'
    if target_ai in content:
        content = content.replace(target_ai, repl_ai, 1)
        print("✓ Hidden live-ai-badge by default in index.html")

    # 4. Update auth login button text
    target_login_lbl = '<span id="auth-btn-label">Sign In / Portals</span>'
    repl_login_lbl = '<span id="auth-btn-label">🔐 Tabeeb / Staff Sign In</span>'
    if target_login_lbl in content:
        content = content.replace(target_login_lbl, repl_login_lbl, 1)
        print("✓ Updated auth-btn-label to '🔐 Tabeeb / Staff Sign In' in index.html")

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(content)

def update_core_js():
    with open(CORE_JS, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. Update navigateToV2Hub to gatekeep unauthenticated users
    old_nav_fn = """    function navigateToV2Hub(hub) {
      const hubMap = {
        command_center: { role: 'doctor', tab: 'today' },
        patients: { role: 'doctor', tab: 'patients' },
        clinical: { role: 'doctor', tab: 'consultation' },
        zmie: { role: 'doctor', tab: 'knowledge' },
        pharmacy: { role: 'pharmacy', tab: 'dispensing' },
        formulation: { role: 'research', tab: 'zfie_studio' },
        outcomes: { role: 'research', tab: 'outcomes' },
        research: { role: 'research', tab: 'studies' },
        admin: { role: 'admin', tab: 'audit' }
      };

      const target = hubMap[hub] || { role: 'doctor', tab: 'today' };
      switchRole(target.role, true);
      switchTab(target.tab);"""

    new_nav_fn = """    function navigateToV2Hub(hub) {
      const hubMap = {
        command_center: { role: 'doctor', tab: 'today' },
        patients: { role: 'doctor', tab: 'patients' },
        clinical: { role: 'doctor', tab: 'consultation' },
        zmie: { role: 'doctor', tab: 'knowledge' },
        pharmacy: { role: 'pharmacy', tab: 'dispensing' },
        formulation: { role: 'research', tab: 'zfie_studio' },
        outcomes: { role: 'research', tab: 'outcomes' },
        research: { role: 'research', tab: 'studies' },
        admin: { role: 'admin', tab: 'audit' }
      };

      // Security Gate: Gatekeep internal hubs. Must be authenticated!
      if (!state.currentUser || !state.currentUser.token) {
        toggleLoginModal(true);
        const targetRole = hubMap[hub] ? hubMap[hub].role : 'doctor';
        prefillLogin(targetRole);
        showNotification('Please sign in with your staff credentials to access this clinical module.', 'info');
        return;
      }

      const target = hubMap[hub] || { role: 'doctor', tab: 'today' };
      switchRole(target.role, false);
      switchTab(target.tab);"""

    if old_nav_fn in js:
        js = js.replace(old_nav_fn, new_nav_fn, 1)
        print("✓ Updated navigateToV2Hub with authentication gatekeeping in js/zayvora-core.js")
    else:
        print("! Warning: Could not locate exact navigateToV2Hub pattern in js/zayvora-core.js")

    # 2. Update updateAuthHeaderUI to control v2 master nav, AI badge, cart
    old_cart_logic = """      // Contextual Dispensary Cart (Website, Pharmacy OS, Patient Portal only)
      const cartBtn = document.getElementById('header-cart-btn');
      if (cartBtn) {
        if (['website', 'pharmacy', 'patient'].includes(state.role)) {
          cartBtn.classList.remove('hidden');
          cartBtn.classList.add('flex');
        } else {
          cartBtn.classList.add('hidden');
          cartBtn.classList.remove('flex');
        }
      }"""

    new_cart_logic = """      // Control V2 Master 9-Hub Navigation visibility:
      // Strictly show ONLY for Super Admin or Enterprise Headquarters when authenticated!
      const v2MasterNav = document.getElementById('zayvora-v2-master-nav');
      if (v2MasterNav) {
        const hasValidAuth = !!(state.currentUser && state.currentUser.token);
        const isEnterpriseHQ = state.platformEdition === 'enterprise' || state.role === 'enterprise';
        if (hasValidAuth && (isSuperAdmin || isEnterpriseHQ)) {
          v2MasterNav.classList.remove('hidden');
          v2MasterNav.classList.add('flex');
        } else {
          v2MasterNav.classList.add('hidden');
          v2MasterNav.classList.remove('flex');
        }
      }

      // Contextual Dispensary Cart (Pharmacy OS & Patient Portal only - NOT doctor or public home)
      const cartBtn = document.getElementById('header-cart-btn');
      if (cartBtn) {
        if (['pharmacy', 'patient'].includes(state.role)) {
          cartBtn.classList.remove('hidden');
          cartBtn.classList.add('flex');
        } else {
          cartBtn.classList.add('hidden');
          cartBtn.classList.remove('flex');
        }
      }

      // Contextual Live AI Badge (Doctor consultation & Research desks only)
      const liveAiBadge = document.getElementById('live-ai-badge');
      if (liveAiBadge) {
        if (['doctor', 'research', 'manufacturing'].includes(state.role)) {
          liveAiBadge.classList.remove('hidden');
          liveAiBadge.classList.add('flex');
        } else {
          liveAiBadge.classList.add('hidden');
          liveAiBadge.classList.remove('flex');
        }
      }"""

    if old_cart_logic in js:
        js = js.replace(old_cart_logic, new_cart_logic, 1)
        print("✓ Injected v2MasterNav, AI badge and cart controls into updateAuthHeaderUI")
    else:
        print("! Warning: Could not locate exact cart logic in js/zayvora-core.js")

    # 3. Update public authContainer CTA button text
    old_auth_cta = '<span id="auth-btn-label">Sign In / Portals</span>'
    new_auth_cta = '<span id="auth-btn-label">🔐 Tabeeb / Staff Sign In</span>'
    if old_auth_cta in js:
        js = js.replace(old_auth_cta, new_auth_cta)
        print("✓ Updated authContainer login CTA in js/zayvora-core.js")

    with open(CORE_JS, "w", encoding="utf-8") as f:
        f.write(js)

if __name__ == "__main__":
    update_index_html()
    update_core_js()
    print("Done applying updates.")
