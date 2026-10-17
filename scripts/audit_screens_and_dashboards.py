import re
import os
import glob

def audit_platform():
    core_path = "js/zayvora-core.js"
    with open(core_path, "r", encoding="utf-8") as f:
        core = f.read()

    print("=" * 70)
    print("ZAYVORA HEALTH OS — COMPREHENSIVE SCREEN & DASHBOARD AUDIT")
    print("=" * 70)

    # 1. Check all role workspaces and tabs
    role_navs_match = re.search(r'const roleNavs\s*=\s*(\{.*?\n\s*\};)', core, re.DOTALL)
    if not role_navs_match:
        print("[-] Could not find roleNavs")
        return

    roles_code = role_navs_match.group(1)
    roles = re.findall(r'(\w+):\s*\[(.*?)\]', roles_code, re.DOTALL)
    
    total_screens = 0
    role_tab_map = {}
    for r, tabs_block in roles:
        tab_ids = re.findall(r"id:\s*'([^']+)'", tabs_block)
        role_tab_map[r] = tab_ids
        total_screens += len(tab_ids)

    print(f"Total Roles Configured: {len(role_tab_map)}")
    print(f"Total Screens / Tabs Configured in Navigation: {total_screens}")
    print("-" * 70)

    # 2. Check implementation of each role workspace
    gaps = []
    hardcoded_mocks = []
    
    for r, tabs in role_tab_map.items():
        renderer_name = f"render{r.capitalize()}App"
        # Search for renderer function
        pattern = r'function\s+' + renderer_name + r'\s*\([^)]*\)\s*\{(.*?)(?=\n\s*(?:function\s+render\w+App|function\s+[a-zA-Z0-9_]+\s*\(|\/\*\*\s*GRAND|$))'
        m = re.search(pattern, core, re.DOTALL)
        
        implemented_tabs = []
        if m:
            body = m.group(1)
            # Find which tabs are handled
            implemented_tabs = re.findall(r"(?:state\.tab|activeTab|currentTab|tab)\s*===\s*'([^']+)'", body)
            # Also catch switch cases
            implemented_tabs += re.findall(r"case\s+'([^']+)':", body)
            implemented_tabs = list(set(implemented_tabs))
            
            # Check for dummy/mock names
            if "Hamza Farooqi" in body:
                hardcoded_mocks.append((r, "Hamza Farooqi hardcoded in table/view"))
            if "MRN-2026-0814" in body:
                hardcoded_mocks.append((r, "MRN-2026-0814 hardcoded in table/view"))
            if "₹1,250" in body or "₹ 1,250" in body or "₹1250" in body:
                hardcoded_mocks.append((r, "Hardcoded dummy revenue / invoice ₹1,250"))
            if "94 subjects" in body or "ZCT-2026-001" in body:
                hardcoded_mocks.append((r, "Hardcoded research study numbers"))

            # Check if any tab defined in navigation is missing from renderer
            missing = [t for t in tabs if t not in implemented_tabs]
            if missing:
                gaps.append((r, f"Missing tab handlers in {renderer_name}: {missing}"))
        else:
            # Check if function exists at all
            if f"function {renderer_name}" not in core:
                gaps.append((r, f"Renderer {renderer_name} NOT DEFINED in js/zayvora-core.js"))
            else:
                gaps.append((r, f"Renderer {renderer_name} found but body parsing failed"))

        print(f"Role: {r.upper():<14} | Configured: {len(tabs):<2} tabs | Implemented: {len(implemented_tabs):<2} tabs")

    print("\n" + "=" * 70)
    print("IDENTIFIED GAPS & DEFICIENCIES")
    print("=" * 70)
    
    print("\n[A] NAVIGATION VS RENDERER MISMATCHES (Tabs defined but not rendered):")
    for r, g in gaps:
        print(f"  ❌ {r}: {g}")
        
    print("\n[B] HARDCODED / DUMMY DATA FOUND IN VIEWS (Clean Slate Inconsistency):")
    for r, h in hardcoded_mocks:
        print(f"  ⚠️  {r}: {h}")

    # 3. Check Live API integration across core
    print("\n[C] LIVE API CALLS IN WORKSPACES:")
    api_calls = re.findall(r'fetch\([\"\'`](/api/v1/[^\"\'`?]+)', core)
    unique_apis = sorted(set(api_calls))
    print(f"  Total API endpoints hooked up via fetch(): {len(unique_apis)}")
    for ep in unique_apis:
        print(f"    ✓ {ep}")

    # 4. Modals and Global Engines Check
    print("\n[D] MODALS & POPUP WORKSPACES:")
    with open("index.html") as f:
        html = f.read()
    modals = re.findall(r'id=\"([a-zA-Z0-9_\-]+modal)\"', html)
    print(f"  Total Modal Engines in index.html: {len(modals)}")
    for mod in sorted(modals):
        has_opener = f"toggle{mod.replace('-modal','').replace('-','').capitalize()}" in core or f"open{mod.replace('-modal','').replace('-','').capitalize()}" in core or mod in core
        print(f"    • {mod:<35} | Integrated in JS: {'YES' if has_opener else 'CHECK'}")

if __name__ == "__main__":
    audit_platform()
