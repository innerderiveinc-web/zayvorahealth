#!/usr/bin/env python3
"""
ZAYVORA Health OS — Patch Qarabadeen (59 Items) and Products (32 Items) into zayvora-core.js
"""

import json
import os

CORE_JS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "js", "zayvora-core.js"))
INDEX_HTML = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "index.html"))

with open('/tmp/qarabadeen_59.json') as f:
    qarabadeen_59 = json.load(f)

with open('/tmp/products_32.json') as f:
    products_32 = json.load(f)

with open(CORE_JS, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace QARABADEEN_CATALOG
q_start = content.find("const QARABADEEN_CATALOG = [")
q_end = content.find("];", q_start)

if q_start != -1 and q_end != -1:
    qarabadeen_js_str = "const QARABADEEN_CATALOG = " + json.dumps(qarabadeen_59, indent=2) + ";"
    content = content[:q_start] + qarabadeen_js_str + content[q_end+2:]
    print("[✓] Replaced QARABADEEN_CATALOG with 59 classical items.")
else:
    print("[-] Could not find QARABADEEN_CATALOG in zayvora-core.js")

# 2. Replace const ZAYVORA_PRODUCTS_32 = ZAYVORA_PRODUCTS_16;
target_str = "const ZAYVORA_PRODUCTS_32 = ZAYVORA_PRODUCTS_16;"
if target_str in content:
    prods_32_str = "const ZAYVORA_PRODUCTS_32 = " + json.dumps(products_32, indent=2) + ";"
    content = content.replace(target_str, prods_32_str, 1)
    print("[✓] Replaced ZAYVORA_PRODUCTS_32 with full 32 sovereign formulations.")
else:
    print("[-] Could not find target ZAYVORA_PRODUCTS_32 assignment")

# 3. Enhance renderQarabadeenCatalog to show Urdu name and Classical Source Badge
old_render_part = """              <strong class="text-white text-sm">${it.name}</strong>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">${it.category}</span>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">${it.axis} Axis</span>
            </div>"""

new_render_part = """              <strong class="text-white text-sm">${it.name}</strong>
              ${it.urdu_name ? `<span class="text-xs font-bold text-amber-300 font-serif mr-1">${it.urdu_name}</span>` : ''}
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">${it.category}</span>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">${it.axis} Axis</span>
              ${it.source ? `<span class="text-[10px] font-mono px-2 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-500/30">📖 ${it.source}</span>` : ''}
            </div>"""

if old_render_part in content:
    content = content.replace(old_render_part, new_render_part, 1)
    print("[✓] Enhanced renderQarabadeenCatalog with Urdu name and Classical Source Badge.")
else:
    print("[!] Warning: old_render_part pattern not found in zayvora-core.js")

with open(CORE_JS, 'w', encoding='utf-8') as f:
    f.write(content)

print("[✓] Successfully saved updated js/zayvora-core.js")

# 4. In index.html, add Noto Nastaliq Urdu font and Amiri
with open(INDEX_HTML, 'r', encoding='utf-8') as f:
    html_content = f.read()

font_tag = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Noto+Nastaliq+Urdu:wght@400;700&display=swap" rel="stylesheet">"""

if "Noto+Nastaliq+Urdu" not in html_content:
    head_tag = "<meta charset=\"UTF-8\">"
    html_content = html_content.replace(head_tag, head_tag + "\n" + font_tag, 1)
    print("[✓] Added Noto Nastaliq Urdu and Amiri Google Fonts to index.html.")

# Add Urdu typography helper class in style tag
urdu_css = """    .urdu-font {
      font-family: 'Noto Nastaliq Urdu', 'Amiri', serif !important;
      direction: rtl;
    }"""

if ".urdu-font" not in html_content:
    style_end = "</style>"
    html_content = html_content.replace(style_end, urdu_css + "\n  " + style_end, 1)
    print("[✓] Added .urdu-font CSS class to index.html.")

with open(INDEX_HTML, 'w', encoding='utf-8') as f:
    html_content = f.write(html_content)

print("[✓] Finished all patches!")
