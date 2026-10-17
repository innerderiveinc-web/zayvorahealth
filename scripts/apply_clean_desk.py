import re

def install():
    desk_start = '<div class="grid grid-cols-1 lg:grid-cols-12 gap-5">'
    desk_end = '<!-- DYNAMIC EMERGENCY RED-FLAG BANNER -->'

    with open('scripts/install_clean_desk.py', 'r') as f:
        script_content = f.read()

    # Extract clean_desk_html
    m_clean = re.search(r'clean_desk_html = \"\"\"(.*?)\"\"\"', script_content, re.DOTALL)
    if not m_clean:
        print('Failed to extract clean_desk_html')
        return
    clean_html = m_clean.group(1)

    for fp in ['js/zayvora-core.js', 'js/modules/02-clinical-workspace.js']:
        with open(fp, 'r') as f:
            c = f.read()

        s_pos = c.find(desk_start)
        e_pos = c.find(desk_end, s_pos)

        if s_pos != -1 and e_pos != -1:
            c_new = c[:s_pos] + clean_html + "\n\n          " + c[e_pos:]
            with open(fp, 'w') as f:
                f.write(c_new)
            print(f'[✓] Clean desk installed into {fp} (s={s_pos}, e={e_pos})')
        else:
            print(f'[!] Could not locate boundaries in {fp}: s={s_pos}, e={e_pos}')

if __name__ == '__main__':
    install()
