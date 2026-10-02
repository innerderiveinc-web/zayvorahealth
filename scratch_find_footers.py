with open('index.html') as f:
    text = f.read()

import re
for m in re.finditer(r'<footer[^>]*>', text):
    print(f"Footer at {m.start()}: {m.group(0)}")
