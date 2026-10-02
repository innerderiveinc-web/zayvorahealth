with open('index.html') as f:
    text = f.read()

idx = text.find('function renderNavigation(')
print(text[idx:idx+1500])
