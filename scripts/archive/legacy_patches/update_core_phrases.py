with open('js/zayvora-core.js', 'r', encoding='utf-8') as f:
    cz = f.read()

replacements = [
    (
        '<!-- CARE INTELLIGENCE 2.0: AI CARE ORCHESTRATOR & CONTINUUM GAPS -->',
        '<!-- CARE INTELLIGENCE 2.0: CLINICAL CARE ORCHESTRATOR & CONTINUUM GAPS -->'
    ),
    (
        'data-pipeline="12-Stage Knowledge Governance & AI Promotion Pipeline">12-Stage Clinical Knowledge Governance & Evidence Review Process',
        'data-pipeline="12-Stage Knowledge Governance & Formulary Validation Pipeline">12-Stage Clinical Knowledge Governance & Evidence Review Process'
    ),
    (
        '<span class="px-2 py-1 rounded bg-purple-500/30 text-purple-200 border border-purple-500/50 font-bold whitespace-nowrap">12. AI Available</span>',
        '<span class="px-2 py-1 rounded bg-purple-500/30 text-purple-200 border border-purple-500/50 font-bold whitespace-nowrap">12. Formulary Verified</span>'
    ),
    (
        '// SINGLE DOCTOR CONSULTATION WORKSPACE (13 CANONICAL TABS + 5-LAYER AI)',
        '// SINGLE DOCTOR CONSULTATION WORKSPACE (13 CANONICAL TABS + 5-LAYER CLINICAL DECISION SUPPORT)'
    ),
    (
        '// Automatically trigger Hakeem Sahab™ AI Nuskha drafting based on diagnosis',
        '// Automatically trigger Hakeem Sahab™ Nuskha drafting based on diagnosis'
    ),
    (
        '// UNIFIED CLINICAL NARRATIVE PARSER & AI SYNTHESIS ENGINE',
        '// UNIFIED CLINICAL NARRATIVE PARSER & CLINICAL SYNTHESIS ENGINE'
    ),
    (
        '<!-- AI PROPOSED CLINICIAN REVIEW BANNER -->',
        '<!-- CLINICAL FORMULATION REVIEW BANNER -->'
    ),
    (
        '// SMART AI CLINICAL SCRIBE (DICTATE RX)',
        '// AMBIENT CLINICAL SCRIBE (DICTATE RX)'
    ),
    (
        '<!-- HAKEEM SAHAB AI DECISION SUPPORT CARD -->',
        '<!-- HAKEEM SAHAB™ CLINICAL DECISION SUPPORT CARD -->'
    ),
    (
        '<!-- 5-LAYER HAKEEM SAHAB AI COPILOT DRAWER -->',
        '<!-- 5-LAYER HAKEEM SAHAB™ CLINICAL DECISION ADVISOR DRAWER -->'
    ),
    (
        'AI generates clinical recommendations only. Prescribing and clinical lockdown authority resides exclusively with the licensed clinician under Medical Council regulations and 21 CFR Part 11.',
        'Hakeem Sahab™ provides clinical decision recommendations only. Prescribing and clinical lockdown authority resides exclusively with the licensed clinician under Medical Council regulations and 21 CFR Part 11.'
    ),
    (
        '// ── MULTIMODAL LISAN (TONGUE) & FACIAL MIZAJ AI SCANNER ─────────────────',
        '// ── MULTIMODAL LISAN (TONGUE) & FACIAL MIZAJ CLINICAL SCANNER ───────────'
    ),
    (
        'Statutory Multidisciplinary Gate: AI proposals must pass sequential human scientist, pharmacologist, and clinician review before commercial formulation or clinical trial deployment.',
        'Statutory Multidisciplinary Gate: Formulary proposals must pass sequential human scientist, pharmacologist, and clinician review before commercial formulation or clinical trial deployment.'
    ),
    (
        'Non-delegable clinician discretion barrier. AI never issues autonomous treatment orders; all prescriptions require cryptographic biometric or PIN signature by a licensed Tabeeb.',
        'Non-delegable clinician discretion barrier. System never issues autonomous treatment orders; all prescriptions require cryptographic biometric or PIN signature by a licensed Tabeeb.'
    ),
    (
        '<span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Assistive AI CDSS (Zero Autonomous Rx)</span>',
        '<span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">Assistive Clinical CDSS (Zero Autonomous Rx)</span>'
    ),
    (
        'fusing centuries of empirical healing with modern biochemistry, AI safety firewalls, and AYUSH-GMP manufacturing.',
        'fusing centuries of empirical healing with modern biochemistry, clinical safety firewalls, and AYUSH-GMP manufacturing.'
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
        '<h1 class="text-3xl font-extrabold text-white">Clinical &amp; AI Ethics Charter</h1>',
        '<h1 class="text-3xl font-extrabold text-white">Clinical Ethics &amp; Governance Charter</h1>'
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
        '// 6. Live Hakeem Sahab AI Copilot',
        '// 6. Live Hakeem Sahab™ Clinical Decision Advisor'
    ),
    (
        '// Live AI Telemetry & Offline Readiness Inspector',
        '// Live Clinical CDSS Telemetry & Offline Readiness Inspector'
    ),
    (
        '// Strictly hide AI badge on public website / patient view!',
        '// Strictly hide CDSS badge on public website / patient view!'
    ),
    (
        '// Contextual Live AI Badge (Doctor consultation & Research desks only)',
        '// Contextual Live Clinical Decision Badge (Doctor consultation & Research desks only)'
    )
]

applied = 0
for t, r in replacements:
    if t in cz:
        cz = cz.replace(t, r)
        applied += 1
    else:
        print(f"Skipped (not found): {t[:60]}")

with open('js/zayvora-core.js', 'w', encoding='utf-8') as f:
    f.write(cz)

print(f"js/zayvora-core.js updated with {applied} replacements!")
