with open('index.html') as f:
    text = f.read()

idx = text.find('website:')
print(text[idx:idx+800])
