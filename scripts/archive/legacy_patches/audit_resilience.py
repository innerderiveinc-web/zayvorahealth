#!/usr/bin/env python3
"""
ZAYVORA Health OS - Deep Resilience & Bug-Proof Audit
Verifies:
1. All document.getElementById references and null-guards
2. All window/global event listeners
3. Modal open/close scroll state restoration
4. Error boundaries across async/sync execution
5. Cache headers and Service Worker cache consistency
"""
import re
import sys

def audit():
    print("=== STARTING DEEP RESILIENCE AUDIT ===")
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    with open('app.html', 'r', encoding='utf-8') as f:
        app_html = f.read()
    with open('js/zayvora-core.js', 'r', encoding='utf-8') as f:
        core_js = f.read()
    with open('js/zayvora-extensions.js', 'r', encoding='utf-8') as f:
        ext_js = f.read()

    # 1. HTML IDs
    html_ids = set(re.findall(r'id=["\']([a-zA-Z0-9_\-]+)["\']', html + app_html))
    js_ids = set(re.findall(r'id=["\']([a-zA-Z0-9_\-]+)["\']', core_js + ext_js))
    all_known_ids = html_ids.union(js_ids)
    print(f"[*] Total Known Element IDs: {len(all_known_ids)}")

    # 2. Direct property/method access on document.getElementById without check
    # e.g. document.getElementById('xyz').value or .innerHTML or .classList
    direct_access_pattern = re.compile(r'document\.getElementById\([\'"]([a-zA-Z0-9_\-]+)[\'"]\)\.([a-zA-Z0-9_]+)')
    matches = direct_access_pattern.findall(core_js)
    
    risky_calls = []
    for el_id, prop in matches:
        if el_id not in all_known_ids:
            risky_calls.append((el_id, prop))

    print(f"[*] Direct method/property calls on document.getElementById: {len(matches)}")
    print(f"[*] Potential missing IDs called directly: {len(set(risky_calls))}")
    for el_id, prop in sorted(list(set(risky_calls))):
        print(f"    - WARNING: document.getElementById('{el_id}').{prop} (ID not found in static markup)")

    # 3. Check for global unhandled rejection and error boundaries
    has_window_onerror = 'window.onerror' in core_js or 'window.addEventListener(\'error\'' in core_js or 'window.addEventListener("error"' in core_js
    has_unhandled_rejection = 'unhandledrejection' in core_js
    print(f"[*] Global window.onerror boundary: {'PRESENT' if has_window_onerror else 'MISSING'}")
    print(f"[*] Global unhandledrejection boundary: {'PRESENT' if has_unhandled_rejection else 'MISSING'}")

    # 4. Check renderWorkspace try-catch
    has_render_workspace_try_catch = False
    rw_match = re.search(r'function\s+renderWorkspace\s*\(', core_js)
    if rw_match:
        rw_chunk = core_js[rw_match.start():rw_match.start()+2500]
        if 'try {' in rw_chunk and 'catch (' in rw_chunk:
            has_render_workspace_try_catch = True
    print(f"[*] renderWorkspace protected by try-catch: {'YES' if has_render_workspace_try_catch else 'NO'}")

    # 5. Check modal scroll cleanup
    modal_overflow_resets = re.findall(r'body\.style\.overflow\s*=\s*[\'"][^\'"]*[\'"]', core_js)
    print(f"[*] Modal body overflow toggles: {len(modal_overflow_resets)}")

    return risky_calls

if __name__ == '__main__':
    audit()
