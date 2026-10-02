import sys

# Load current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original index.html length: {len(content)}")
