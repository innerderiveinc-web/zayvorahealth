import re

# Test all tab definitions against our planned renderers
roles_tabs = {
    'patient': ['home', 'appointments', 'health', 'treatment', 'medicines', 'reports', 'messages', 'profile'],
    'doctor': ['today', 'patients', 'consultation', 'prescriptions', 'followups', 'assistant', 'knowledge', 'profile'],
    'clinic': ['overview', 'appointments', 'patients', 'queue', 'doctors', 'billing', 'settings'],
    'pharmacy': ['dispensing', 'inventory', 'detox', 'orders'],
    'research': ['studies', 'outcomes', 'adverse'],
    'admin': ['organizations', 'users', 'audit', 'safety', 'engines'],
    'enterprise': ['overview', 'facilities', 'financials', 'governance', 'expansion'],
    'manufacturing': ['batches', 'testing', 'mudabbar', 'coa'],
    'herbals': ['catalog', 'cart', 'monographs', 'fefo'],
    'mobile': ['simulator', 'audio_posology', 'asbab_sittah', 'companion'],
    'hardware': ['nabz', 'lisan', 'wearables', 'nir', 'coldchain'],
    'website': ['home', 'about', 'services', 'products', 'research', 'philosophy', 'care_journey', 'clinics', 'doctors', 'knowledge', 'faqs', 'contact', 'pages25']
}

total_tabs = sum(len(tabs) for tabs in roles_tabs.values())
print(f"Total role-tab combinations to verify: {total_tabs}")
