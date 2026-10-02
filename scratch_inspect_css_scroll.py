with open('index.html') as f:
    text = f.read()

idx_style = text.find('<style')
idx_style_end = text.find('</style>', idx_style)
style_content = text[idx_style:idx_style_end]

lines = style_content.splitlines()
for i, line in enumerate(lines):
    if any(k in line.lower() for k in ['html', 'body', 'scroll', 'overflow', 'height', 'max-height']):
        print(f"L{i}: {line.strip()}")
