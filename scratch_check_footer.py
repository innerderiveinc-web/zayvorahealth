with open('index.html') as f:
    text = f.read()

idx = text.rfind('<footer')
print(text[idx:])
