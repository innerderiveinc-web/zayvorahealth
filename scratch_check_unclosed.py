with open('index.html') as f:
    text = f.read()

import re

# Remove scripts and styles first so we only check HTML structure
no_scripts = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', text, flags=re.DOTALL)
no_styles = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', no_scripts, flags=re.DOTALL)

# Self-closing tags in HTML5
void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

stack = []
tag_pattern = re.compile(r'<\s*(/)?\s*([a-zA-Z0-9\-]+)([^>]*)>')

for m in tag_pattern.finditer(no_styles):
    is_closing, tag, attrs = m.groups()
    tag = tag.lower()
    if tag in void_tags or attrs.endswith('/'):
        continue
    
    if not is_closing:
        stack.append((tag, m.start()))
    else:
        # Looking for matching opening tag
        found = False
        for i in range(len(stack)-1, -1, -1):
            if stack[i][0] == tag:
                stack = stack[:i] # pop up to this tag
                found = True
                break
        if not found:
            print(f"Unmatched closing tag: </{tag}> at pos {m.start()}")

print(f"Remaining unclosed tags at end: {len(stack)}")
for tag, pos in stack:
    print(f" - Unclosed <{tag}> opened at {pos}: {no_styles[pos:pos+60].replace(chr(10), ' ')}")

