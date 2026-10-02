with open('index.html') as f:
    text = f.read()

idx = text.find('function switchTab(')
print(text[idx:idx+800])
