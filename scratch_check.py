with open('index.html') as f:
    text = f.read()

idx = text.find('function renderWebsiteApp(')
idx_end = text.find('function renderHerbalsApp(', idx)
website_func = text[idx:idx_end]

import re
matches = [m.start() for m in re.finditer(r'container\.innerHTML\s*=', website_func)]
for i, pos in enumerate(matches):
    # Find next return
    ret_pos = website_func.find('return;', pos)
    next_pos = matches[i+1] if i+1 < len(matches) else len(website_func)
    has_ret = ret_pos != -1 and ret_pos < next_pos
    print(f"Assignment {i}: has_return={has_ret} (ret_pos={ret_pos}, next_pos={next_pos})")
