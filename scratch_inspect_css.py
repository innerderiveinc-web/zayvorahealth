with open('index.html') as f:
    text = f.read()

idx_style = text.find('<style')
idx_style_end = text.find('</style>', idx_style)
print(text[idx_style:idx_style+2500])
