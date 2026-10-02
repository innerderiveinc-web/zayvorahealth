with open('index.html') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'localStorage\.', text)]
print(f"Total localStorage accesses: {len(matches)}")
unprotected = []
for pos in matches:
    # Check if inside a try block within the preceding 300 chars
    preceding = text[max(0, pos-400):pos]
    # Check if 'try {' appears after the last 'function' or '{'
    snippet = text[pos-20:pos+80].replace('\n', ' ')
    # Look for try before this line
    lines_before = preceding.splitlines()[-5:]
    has_try = any('try' in l for l in lines_before)
    if not has_try:
        unprotected.append((pos, snippet))

print(f"Potentially unprotected localStorage calls: {len(unprotected)}")
for pos, s in unprotected[:15]:
    print(f" - at {pos}: {s}")
