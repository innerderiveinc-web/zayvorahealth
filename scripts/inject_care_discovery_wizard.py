with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = '<!-- Live Diagnostic Hardware Telemetry Bar -->'
replacement = """<!-- Guided Care Discovery Wizard ("What Brings You Here?") -->
          <div id="care-discovery-wizard"></div>

          <!-- Live Diagnostic Hardware Telemetry Bar -->"""

if 'id="care-discovery-wizard"' not in html:
    html = html.replace(target, replacement, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Successfully injected care-discovery-wizard into index.html and docs/index.html")
else:
    print("care-discovery-wizard already in html")
