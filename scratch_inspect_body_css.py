with open('index.html') as f:
    text = f.read()

idx_style = text.find('<style')
idx_style_end = text.find('</style>', idx_style)
style_content = text[idx_style:idx_style_end]

lines = style_content.splitlines()
print("\n".join(lines[120:160]))
