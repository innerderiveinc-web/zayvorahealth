import re

with open("docs/index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the existing renderWebsiteApp function with our comprehensive multi-page implementation
pattern = r"function renderWebsiteApp\(container\)\s*\{.*?\n\s*\}\s*\n\s*// ===+[\r\n\s]*// ZAYVORA HERBALS"
match = re.search(pattern, text, flags=re.DOTALL)
if not match:
    print("! Could not find renderWebsiteApp boundary by regex, trying line split")
    # Find start and end by markers
    start_marker = "function renderWebsiteApp(container) {"
    end_marker = "// ZAYVORA HERBALS 10-PRODUCT PORTFOLIO & CART WORKSPACE"
    start_pos = text.find(start_marker)
    end_pos = text.find(end_marker)
    print("start_pos:", start_pos, "end_pos:", end_pos)
else:
    print("✓ Found renderWebsiteApp match!")

