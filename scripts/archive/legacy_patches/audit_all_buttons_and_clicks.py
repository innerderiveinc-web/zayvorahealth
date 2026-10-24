import os
import re
import sys

def audit_buttons_and_clicks():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_file = os.path.join(base_dir, "index.html")
    core_js_file = os.path.join(base_dir, "js", "zayvora-core.js")
    ext_js_file = os.path.join(base_dir, "js", "zayvora-extensions.js")

    with open(index_file, "r", encoding="utf-8") as f:
        index_content = f.read()

    core_content = ""
    if os.path.exists(core_js_file):
        with open(core_js_file, "r", encoding="utf-8") as f:
            core_content = f.read()

    ext_content = ""
    if os.path.exists(ext_js_file):
        with open(ext_js_file, "r", encoding="utf-8") as f:
            ext_content = f.read()

    all_code = index_content + "\n" + core_content + "\n" + ext_content

    # 1. Collect all defined functions
    # Matches: function fnName(, const fnName = function(, const fnName = (, window.fnName = 
    func_defs = set()
    for m in re.finditer(r'(?:function\s+([a-zA-Z0-9_$]+)\s*\(|const\s+([a-zA-Z0-9_$]+)\s*=\s*(?:function|\()|let\s+([a-zA-Z0-9_$]+)\s*=\s*(?:function|\()|var\s+([a-zA-Z0-9_$]+)\s*=\s*(?:function|\()|window\.([a-zA-Z0-9_$]+)\s*=)', all_code):
        name = m.group(1) or m.group(2) or m.group(3) or m.group(4) or m.group(5)
        if name:
            func_defs.add(name)

    # Standard browser functions
    standard_builtins = {
        'print', 'alert', 'confirm', 'prompt', 'open', 'close', 'scroll',
        'scrollTo', 'scrollBy', 'focus', 'blur', 'history', 'location',
        'event', 'console', 'eval', 'parseInt', 'parseFloat', 'setTimeout',
        'clearTimeout', 'setInterval', 'clearInterval'
    }

    # 2. Extract all onclick handlers from index_content, core_content, and ext_content
    # We look for onclick="...", onclick='...', onclick=`...`
    onclick_pattern = re.compile(r'onclick=([\'"])(.*?)\1', re.IGNORECASE)
    
    found_clicks = []
    for match in onclick_pattern.finditer(index_content):
        found_clicks.append(("index.html", match.group(2).strip()))
    for match in onclick_pattern.finditer(core_content):
        found_clicks.append(("zayvora-core.js", match.group(2).strip()))
    for match in onclick_pattern.finditer(ext_content):
        found_clicks.append(("zayvora-extensions.js", match.group(2).strip()))

    print(f"Total onclick handlers detected: {len(found_clicks)}")

    # 3. Analyze each onclick handler
    unresolved_calls = []
    empty_handlers = []
    inline_js_count = 0

    for file_source, code in found_clicks:
        if not code or code == "#" or code == "javascript:void(0)" or code == ";":
            empty_handlers.append((file_source, code))
            continue

        # Extract primary function calls e.g. "myFunc(123)", "window.print()", "this.classList.toggle('x')"
        # Split by semicolons or commas
        statements = [s.strip() for s in code.split(';') if s.strip()]
        for stmt in statements:
            # Check if it starts with an identifier followed by (
            call_match = re.match(r'^(?:window\.)?([a-zA-Z0-9_$]+)\s*\(', stmt)
            if call_match:
                fn_name = call_match.group(1)
                if fn_name not in standard_builtins and fn_name not in func_defs:
                    unresolved_calls.append((file_source, fn_name, stmt))
            elif stmt.startswith("this.") or stmt.startswith("event.") or stmt.startswith("document.") or "=" in stmt:
                # Direct inline DOM manipulation or variable assignment
                inline_js_count += 1
            else:
                # Could be a function call inside ternary or condition
                sub_calls = re.findall(r'([a-zA-Z0-9_$]+)\s*\(', stmt)
                for fn_name in sub_calls:
                    if fn_name not in standard_builtins and fn_name not in func_defs and fn_name not in ('if', 'for', 'while', 'switch', 'catch', 'function'):
                        unresolved_calls.append((file_source, fn_name, stmt))

    # 4. Check all document.getElementById calls in JS against defined IDs
    # Extract all IDs in index.html and in template strings
    id_pattern = re.compile(r'id=[\'"]([a-zA-Z0-9_\-]+)[\'"]', re.IGNORECASE)
    defined_ids = set()
    for m in id_pattern.finditer(all_code):
        defined_ids.add(m.group(1))

    # Extract all getElementById calls
    get_el_pattern = re.compile(r'getElementById\([\'"]([a-zA-Z0-9_\-]+)[\'"]\)')
    get_el_calls = set()
    missing_ids = set()
    for m in get_el_pattern.finditer(all_code):
        el_id = m.group(1)
        get_el_calls.add(el_id)
        if el_id not in defined_ids:
            missing_ids.add(el_id)

    print(f"Total defined functions: {len(func_defs)}")
    print(f"Total defined DOM IDs: {len(defined_ids)}")
    print(f"Total getElementById calls: {len(get_el_calls)}")
    print("=" * 60)

    if empty_handlers:
        print(f"\n[!] EMPTY OR DUMMY ONCLICK HANDLERS FOUND ({len(empty_handlers)}):")
        for src, h in set(empty_handlers):
            print(f"  - In {src}: '{h}'")
    else:
        print("\n[✓] ZERO empty/dummy onclick handlers.")

    if unresolved_calls:
        # Deduplicate
        unique_unresolved = {}
        for src, fn, stmt in unresolved_calls:
            unique_unresolved[fn] = (src, stmt)
        print(f"\n[!] POTENTIALLY UNRESOLVED FUNCTION CALLS ({len(unique_unresolved)}):")
        for fn, (src, stmt) in sorted(unique_unresolved.items()):
            print(f"  - Function '{fn}' called in {src}: `{stmt}`")
    else:
        print("[✓] ALL button and onclick function calls are resolved and defined.")

    if missing_ids:
        print(f"\n[!] getElementById CALLS WITH NO MATCHING ID IN CODE ({len(missing_ids)}):")
        for mid in sorted(missing_ids):
            print(f"  - Target ID: '{mid}'")
    else:
        print("[✓] ALL getElementById calls target valid, existing IDs.")

    print("\n" + "=" * 60)
    print("Audit Complete.")

if __name__ == "__main__":
    audit_buttons_and_clicks()
