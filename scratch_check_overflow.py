with open('index.html') as f:
    text = f.read()

import re

# Check all classes with overflow or height in the static HTML
body_idx = text.find('<body')
script_idx = text.find('// ===== THEME MANAGEMENT =====')
static_html = text[body_idx:script_idx]

for line in static_html.splitlines():
    if any(k in line for k in ['overflow-hidden', 'overflow-y-hidden', 'h-screen', 'max-h-screen', 'fixed inset-0']):
        print("Static HTML:", line.strip()[:100])

