with open('js/modules/02-clinical-workspace.js', 'r', encoding='utf-8') as f:
    c = f.read()

replacements = [
    (
        'data-pipeline="12-Stage Knowledge Governance & AI Promotion Pipeline">12-Stage Clinical Knowledge Governance & Evidence Review Process',
        'data-pipeline="12-Stage Knowledge Governance & Formulary Validation Pipeline">12-Stage Clinical Knowledge Governance & Evidence Review Process'
    ),
    (
        'showNotification(`✨ Hakeem Sahab™ AI proposed formulation for "${diagText}". Clinician review required before finalizing.`, \'info\');',
        'showNotification(`✨ Hakeem Sahab™ formulated prescription for "${diagText}". Attending physician review and signature required.`, \'info\');'
    ),
    (
        '<span class="text-[10px] text-purple-200 block mt-0.5">AI suggests. Clinician decides. Doctor analyzes &amp; holds sole finalization authority.</span>',
        '<span class="text-[10px] text-purple-200 block mt-0.5">Clinical Decision Support. Attending physician analyzes &amp; holds sole finalization authority.</span>'
    ),
    (
        'AI generates clinical recommendations only. Prescribing and clinical lockdown authority resides exclusively with the licensed clinician under Medical Council regulations and 21 CFR Part 11.',
        'Hakeem Sahab™ provides clinical decision recommendations only. Prescribing and clinical lockdown authority resides exclusively with the licensed clinician under Medical Council regulations and 21 CFR Part 11.'
    ),
    (
        '<span class="text-[11px] text-purple-200 block mt-0.5">Automated draft proposed from patient intake data (Su-e-Mizaj Barid Balghami + hs-CRP 4.8 mg/L + Knee Joint stiffness). Review &amp; doctor verification required.</span>',
        '<span class="text-[11px] text-purple-200 block mt-0.5">Evidence-grounded draft synthesized from patient intake data (Su-e-Mizaj Barid Balghami + hs-CRP 4.8 mg/L + Knee Joint stiffness). Review &amp; doctor verification required.</span>'
    ),
    (
        'Statutory Multidisciplinary Gate: AI proposals must pass sequential human scientist, pharmacologist, and clinician review before commercial formulation or clinical trial deployment.',
        'Statutory Multidisciplinary Gate: Formulary proposals must pass sequential human scientist, pharmacologist, and clinician review before commercial formulation or clinical trial deployment.'
    )
]

for t, r in replacements:
    assert t in c, f'Missing: {t}'
    c = c.replace(t, r)

with open('js/modules/02-clinical-workspace.js', 'w', encoding='utf-8') as f:
    f.write(c)

print('js/modules/02-clinical-workspace.js updated successfully!')
