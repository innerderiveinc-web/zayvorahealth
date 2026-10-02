with open('index.html') as f:
    text = f.read()

idx = text.find('const roleNavs =')
print(text[idx:idx+1500])
