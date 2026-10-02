with open('index.html') as f:
    text = f.read()

idx = text.find('id="site-footer-directory"')
print("Length from site-footer-directory to end:", len(text) - idx)
# Print after closing </footer> of site-footer-directory
idx_close = text.find('</footer>', idx)
print("After site-footer-directory close:")
print(text[idx_close:idx_close+1500])
