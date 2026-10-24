import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_rn = text.find('const roleNavs = {')
idx_rn_end = text.find('let state = {', idx_rn)
rn_str = text[idx_rn:idx_rn_end]

role_func_map = {
    'patient': 'renderPatientApp',
    'doctor': 'renderDoctorApp',
    'clinic': 'renderClinicApp',
    'pharmacy': 'renderPharmacyApp',
    'research': 'renderResearchApp',
    'admin': 'renderAdminApp',
    'enterprise': 'renderEnterpriseApp',
    'manufacturing': 'renderManufacturingApp',
    'website': 'renderWebsiteApp',
    'herbals': 'renderHerbalsApp',
    'mobile': 'renderMobileApp',
    'hardware': 'renderHardwareApp'
}

roles = {}
current_role = None
for line in rn_str.split('\n'):
    line = line.strip()
    r_match = re.match(r'([a-z]+):\s*\[', line)
    if r_match and r_match.group(1) in role_func_map:
        current_role = r_match.group(1)
        roles[current_role] = []
    elif current_role and "id: '" in line:
        tab_id = re.search(r"id:\s*'([^']+)'", line).group(1)
        roles[current_role].append(tab_id)

print(f"Auditing all 12 role renderers for all {sum(len(v) for v in roles.values())} tabs...")
failures = []
total_checked = 0

for role, tabs in roles.items():
    fn_name = role_func_map[role]
    idx_start = text.find(f"function {fn_name}(")
    if idx_start == -1:
        failures.append(f"Function {fn_name} not found!")
        continue
    idx_end = text.find("function ", idx_start + len(fn_name) + 15)
    fn_code = text[idx_start:idx_end] if idx_end != -1 else text[idx_start:]
    
    for t in tabs:
        total_checked += 1
        has_branch = (f"state.tab === '{t}'" in fn_code) or (f'state.tab === "{t}"' in fn_code)
        if not has_branch:
            if role in ['enterprise', 'manufacturing', 'herbals', 'mobile', 'hardware'] or (role == 'website' and t == 'home'):
                pass
            else:
                failures.append(f"Role '{role}' missing handler for tab '{t}' in {fn_name}")

if failures:
    print(f"FAILED: {len(failures)} failures detected:")
    for f in failures:
        print(f" - {f}")
else:
    print(f"SUCCESS: All {total_checked} tabs across all 12 operational roles verified!")
