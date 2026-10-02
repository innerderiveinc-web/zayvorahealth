with open('index.html') as f:
    text = f.read()

pos = 131358
print(text[pos-200:pos+300])
