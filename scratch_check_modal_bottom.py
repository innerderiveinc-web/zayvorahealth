with open('index.html') as f:
    text = f.read()

idx = text.rfind('<footer id="clinical-os-footer"')
idx2 = text.find('id="bilingual-prescription-slip-modal"')
print("Prescription slip modal position relative to footer:", idx2 - idx)
print(text[idx2-100:idx2+400])
