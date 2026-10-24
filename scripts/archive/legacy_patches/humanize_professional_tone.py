#!/usr/bin/env python3
"""
scripts/humanize_professional_tone.py

Replaces robotic AI hype terms across the entire OS with dignified, authentic,
and human-centric clinical healthcare terminology.

Examples of transformations:
- "🤖 Clinical AI Copilot" -> "🩺 Clinical Decision Support (CDSS)"
- "🎙️ Yad-dasht (AI Voice Clinical Notes)" -> "🔪 Ilaj bil Yad (Procedural & Manual)"
- "AI Copilot & LLM" -> "Clinical Decision Support (CDS)"
- "Hakeem Sahab AI Copilot Engine" -> "Clinical Decision Support Engine (CDSS)"
- "AI differential diagnosis" -> "clinical differential diagnosis and pharmacopoeial cross-checks"
- "Autonomous AI prescription (HARD BLOCKED)" -> "Automated prescription without physician review (STRICTLY PROHIBITED)"
- "HARD-BLOCKED FROM AI COPILOT" -> "RESERVED STRICTLY FOR LICENSED TABEEB"
- Tooltips, modal labels, and system banners aligned with professional medical standards.
"""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path("/Users/irfanashraf/Downloads/zayvora-platform-phase0-4")

def update_zayvora_core():
    core_path = ROOT / "js" / "zayvora-core.js"
    text = core_path.read_text(encoding="utf-8")

    # 1. Update getDoctorNavItems labels
    text = text.replace(
        "{ id: 'assistant', label: '🤖 Clinical AI Copilot' }",
        "{ id: 'assistant', label: '🩺 Clinical Decision Support (CDSS)' }"
    )
    text = text.replace(
        "{ id: 'yad', label: '🎙️ Yad-dasht (AI Voice Clinical Notes)' }",
        "{ id: 'yad', label: '🔪 Ilaj bil Yad (Procedural & Manual)' }"
    )

    # 2. Update tooltips and settings button titles
    text = text.replace(
        'title="Configure Master Practice, Doctor, AI & Backup Settings"',
        'title="Master System Settings (Clinic, Clinical CDS, Doctor, Backup)"'
    )
    text = text.replace(
        'title="Master System Settings (Clinic, AI, Doctor, Backup)"',
        'title="Master System Settings (Clinic, Clinical CDS, Doctor, Backup)"'
    )

    # 3. Update contraindication / safety strings in grand corpus
    text = text.replace(
        '"Autonomous AI prescription (HARD BLOCKED)"',
        '"Automated prescribing without in-person physician evaluation (STRICTLY PROHIBITED)"'
    )
    text = text.replace(
        'HARD-BLOCKED FROM AI AUTONOMOUS COPILOT',
        'MANDATORY IN-PERSON CLINICIAN SUPERVISION (NO AUTOMATED DISPENSING)'
    )
    text = text.replace(
        'HARD-BLOCKED FROM AI COPILOT',
        'RESERVED STRICTLY FOR ATTENDING TABEEB'
    )
    text = text.replace(
        'Hard-blocked for automated AI prescription',
        'Strictly prohibited from automated dispensing without physician review'
    )
    text = text.replace(
        'Contraindicated for direct AI prescription',
        'Contraindicated for automated dispensing without clinician evaluation'
    )
    text = text.replace(
        'STRICTLY BLOCKED FROM AUTOMATED AI PRESCRIBING',
        'STRICTLY RESERVED FOR IN-PERSON LICENSED TABEEB ONLY'
    )

    # 4. Update Assistant tab in renderDoctorApp
    text = text.replace(
        'onclick="insertAiRecommendationToPlan()" class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg shadow">\n                      + Insert to Active Encounter Plan',
        'onclick="insertAiRecommendationToPlan()" class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg shadow">\n                      + Adopt Clinical Recommendation into Encounter Plan'
    )

    core_path.write_text(text, encoding="utf-8")
    print("✓ Updated js/zayvora-core.js with human clinical terminology")

def update_html_files():
    html_files = [ROOT / "index.html", ROOT / "app.html"]
    for path in html_files:
        text = path.read_text(encoding="utf-8")

        # 1. Bump version
        text = re.sub(r'zayvora-core\.js\?v=[\d\.]+', 'zayvora-core.js?v=17.1', text)
        text = re.sub(r'zayvora-extensions\.js\?v=[\d\.]+', 'zayvora-extensions.js?v=17.1', text)

        # 2. Humanize Settings Modal
        text = text.replace(
            '<span>🧠</span> <span>AI Copilot &amp; LLM</span>',
            '<span>🧠</span> <span>Clinical Decision Support (CDS)</span>'
        )
        text = text.replace(
            'Centralized Practice Configuration • Prescriber Stationery, AI Engine, Regional Currency &amp; Encryption',
            'Centralized Practice Configuration • Prescriber Stationery, Clinical Decision Support (CDS), Regional Currency &amp; Compliance'
        )
        text = text.replace(
            '<!-- 4. AI COPILOT & LLM ENGINE TAB -->',
            '<!-- 4. CLINICAL DECISION SUPPORT & KNOWLEDGE ENGINE TAB -->'
        )
        text = text.replace(
            '<span>🧠</span> <strong>Hakeem Sahab AI Copilot Engine:</strong> Powered by Google Gemini 2.0 Flash for Clinical Decision Support.',
            '<span>🧠</span> <strong>Clinical Decision Support Engine (CDSS):</strong> Integrated medical evidence synthesis, classical literature cross-checks, and differential diagnosis.'
        )
        text = text.replace(
            'Google Gemini API Key (Clinical CDS)',
            'Google Gemini API Key (Clinical Knowledge Gateway)'
        )
        text = text.replace(
            'Forwarded via SSL to live API server for AI differential diagnosis.',
            'Forwarded via SSL to live API server for clinical differential diagnosis and classical pharmacopoeial cross-checks.'
        )
        text = text.replace(
            '<!-- MODAL: SMART VOICE & TEXT PRESCRIPTION PARSER (FAST MATAB AI)         -->',
            '<!-- MODAL: SMART VOICE & TEXT PRESCRIPTION PARSER (FAST MATAB CDS)        -->'
        )
        text = text.replace(
            'Hakeem Sahab™ AI Copilot',
            'Hakeem Sahab™ Clinical Protocol Advisor'
        )

        path.write_text(text, encoding="utf-8")
        print(f"✓ Updated {path.name} with professional clinical terminology and bumped to v=17.1")

def update_sw_and_extensions():
    # 1. sw.js
    sw_file = ROOT / "sw.js"
    sw_code = sw_file.read_text(encoding="utf-8")
    sw_code = re.sub(r"const CACHE_NAME = 'zayvora-health-os-v[\d\.]+-live';", "const CACHE_NAME = 'zayvora-health-os-v17.1-live';", sw_code)
    sw_file.write_text(sw_code, encoding="utf-8")
    print("✓ Updated sw.js CACHE_NAME to v17.1-live")

    # 2. js/zayvora-extensions.js
    ext_file = ROOT / "js" / "zayvora-extensions.js"
    ext_code = ext_file.read_text(encoding="utf-8")
    ext_code = re.sub(r"sw\.js\?v=[\d\.]+", "sw.js?v=17.1", ext_code)
    ext_file.write_text(ext_code, encoding="utf-8")
    print("✓ Updated js/zayvora-extensions.js sw registration to v17.1")

def sync_to_docs():
    shutil.copy2(ROOT / "index.html", ROOT / "docs" / "index.html")
    shutil.copy2(ROOT / "app.html", ROOT / "docs" / "app.html")
    shutil.copy2(ROOT / "sw.js", ROOT / "docs" / "sw.js")
    shutil.copy2(ROOT / "js" / "zayvora-core.js", ROOT / "docs" / "js" / "zayvora-core.js")
    shutil.copy2(ROOT / "js" / "zayvora-extensions.js", ROOT / "docs" / "js" / "zayvora-extensions.js")
    print("✓ Synchronized 100% of files to docs/")

if __name__ == "__main__":
    update_zayvora_core()
    update_html_files()
    update_sw_and_extensions()
    sync_to_docs()
    print("=== Professional Tone Humanization Complete! ===")
