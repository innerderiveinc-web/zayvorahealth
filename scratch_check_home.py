with open('index.html') as f:
    text = f.read()

idx = text.find('function renderWebsiteApp(')
idx_end = text.find('function renderHerbalsApp(', idx)
website_func = text[idx:idx_end]

home_html = website_func[150039:227952]

import re
# Find all HTML comments or major section headers
comments = re.findall(r'<!--\s*=+\s*([^-]+?)\s*=+-->', home_html)
print("Sections in Home Page:")
for c in comments:
    print(" -", c.strip())

# Check for unclosed tags or syntax issues in home_html
tags = re.findall(r'<(/?[a-zA-Z0-9]+)', home_html)
counts = {}
for t in tags:
    is_closing = t.startswith('/')
    name = t[1:] if is_closing else t
    if name in ['div', 'section', 'main', 'p', 'span', 'button', 'a']:
        counts[name] = counts.get(name, 0) + (-1 if is_closing else 1)

print("\nTag balance in Home Page (0 means perfectly balanced):")
for k, v in counts.items():
    print(f" {k}: {v}")
