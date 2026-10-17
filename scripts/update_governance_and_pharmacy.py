with open('js/modules/03-governance-admin.js', 'r', encoding='utf-8') as f:
    c3 = f.read()

gov_replacements = [
    (
        'Non-delegable clinician discretion barrier. AI never issues autonomous treatment orders; all prescriptions require cryptographic biometric or PIN signature by a licensed Tabeeb.',
        'Non-delegable clinician discretion barrier. System never issues autonomous treatment orders; all prescriptions require cryptographic biometric or PIN signature by a licensed Tabeeb.'
    ),
    (
        'All proprietary algorithms, clinical decision support logic (Hakeem Sahab AI™), 10-Ajnas scoring models',
        'All proprietary algorithms, clinical decision support logic (Hakeem Sahab™ CDSS), 10-Ajnas scoring models'
    ),
    (
        '<span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Assistive AI CDSS (Zero Autonomous Rx)</span>',
        '<span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Assistive Clinical CDSS (Zero Autonomous Rx)</span>'
    ),
    (
        'Role &amp; Boundaries of Clinical AI (Hakeem Sahab AI™)',
        'Role &amp; Boundaries of Clinical Decision Support (Hakeem Sahab™ CDSS)'
    ),
    (
        '<strong>Hakeem Sahab AI™</strong> operates strictly as an assistive Clinical Decision Support System (CDSS) for certified medical practitioners:',
        '<strong>Hakeem Sahab™ CDSS</strong> operates strictly as an assistive Clinical Decision Support System (CDSS) for certified medical practitioners:'
    ),
    (
        '<li><strong>Zero Autonomous Prescribing:</strong> The AI system possesses zero legal, diagnostic, or prescribing authority.',
        '<li><strong>Zero Autonomous Prescribing:</strong> The clinical decision support system possesses zero legal, diagnostic, or prescribing authority.'
    ),
    (
        '<li><strong>Reference Only:</strong> AI outputs represent synthesized literature cross-talk',
        '<li><strong>Reference Only:</strong> Clinical CDSS outputs represent synthesized literature cross-talk'
    ),
    (
        'review Hakeem Sahab™ AI differential suggestions, and execute',
        'review Hakeem Sahab™ differential suggestions, and execute'
    ),
    (
        'We are building the future of codified Greco-Arab medicine—fusing centuries of empirical healing with modern biochemistry, AI safety firewalls, and AYUSH-GMP manufacturing.',
        'We are building the future of codified Greco-Arab medicine—fusing centuries of empirical healing with modern biochemistry, clinical safety firewalls, and AYUSH-GMP manufacturing.'
    ),
    (
        '<p class="text-xs text-slate-400">Practitioners retain complete diagnostic authority. AI serves as clinician-in-the-loop decision support, never replacing human clinical judgment.</p>',
        '<p class="text-xs text-slate-400">Practitioners retain complete diagnostic authority. Decision support serves as clinician-in-the-loop guidance, never replacing human clinical judgment.</p>'
    ),
    (
        '// TAB: CLINICAL & AI GOVERNANCE ETHICS CHARTER',
        '// TAB: CLINICAL & DECISION GOVERNANCE ETHICS CHARTER'
    ),
    (
        'desc: "Under statutory NCISM and medical board ethics, the AI engine (Hakeem Sahab™) is strictly prohibited from generating, modifying, or dispensing therapeutic prescriptions autonomously. All clinical recommendations are non-binding differential advisories."',
        'desc: "Under statutory NCISM and medical board ethics, the decision support engine (Hakeem Sahab™) is strictly prohibited from generating, modifying, or dispensing therapeutic prescriptions autonomously. All clinical recommendations are non-binding differential advisories."'
    ),
    (
        '<h1 class="text-3xl font-extrabold text-white">Clinical &amp; AI Ethics Charter</h1>',
        '<h1 class="text-3xl font-extrabold text-white">Clinical Ethics &amp; Governance Charter</h1>'
    ),
    (
        'desc: "Full-spectrum integrative healthcare services unifying 10-Ajnas pulse evaluation, clinical decision support AI, ambient scribe, and certified manufacturing."',
        'desc: "Full-spectrum integrative healthcare services unifying 10-Ajnas pulse evaluation, clinical decision support system, ambient scribe, and certified manufacturing."'
    ),
    (
        '<span class="block mt-1 font-bold text-emerald-300">AI assists. Evidence informs. Clinicians decide.</span>',
        '<span class="block mt-1 font-bold text-emerald-300">Evidence informs. Guidelines assist. Clinicians decide.</span>'
    ),
    (
        'Patient 360, OPD consultation, Clinical Copilot advisory, posology adjustments, and signed electronic prescription workflows.',
        'Patient 360, OPD consultation, Clinical Decision Advisory, posology adjustments, and signed electronic prescription workflows.'
    ),
    (
        'In-clinic matab care, tele-consultation, and AI clinical decision support',
        'In-clinic matab care, tele-consultation, and clinical decision support'
    ),
    (
        'electronic health records, and clinician-governed AI.',
        'electronic health records, and clinician-governed decision intelligence.'
    )
]

for t, r in gov_replacements:
    assert t in c3, f'Missing in 03-governance-admin: {t}'
    c3 = c3.replace(t, r)

with open('js/modules/03-governance-admin.js', 'w', encoding='utf-8') as f:
    f.write(c3)

print('js/modules/03-governance-admin.js updated successfully!')


with open('js/modules/04-pharmacy-dispensary.js', 'r', encoding='utf-8') as f:
    c4 = f.read()

pharm_replacements = [
    (
        '// Global clinical copilot & queue helpers',
        '// Global clinical decision advisory & queue helpers'
    ),
    (
        '[HAKEEM SAHAB AI RECOMMENDATION]',
        '[HAKEEM SAHAB™ CLINICAL RECOMMENDATION]'
    ),
    (
        "showNotification('Hakeem Sahab AI recommendation inserted into Active Encounter Care Plan.', 'success');",
        "showNotification('Hakeem Sahab™ clinical recommendation inserted into Active Encounter Care Plan.', 'success');"
    ),
    (
        '// 6. Live Hakeem Sahab AI Copilot',
        '// 6. Live Hakeem Sahab™ Clinical Decision Advisor'
    )
]

for t, r in pharm_replacements:
    assert t in c4, f'Missing in 04-pharmacy-dispensary: {t}'
    c4 = c4.replace(t, r)

with open('js/modules/04-pharmacy-dispensary.js', 'w', encoding='utf-8') as f:
    f.write(c4)

print('js/modules/04-pharmacy-dispensary.js updated successfully!')
