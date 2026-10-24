#!/usr/bin/env python3
"""
ZAYVORA Health OS — Master Book & Treatise Compiler (Publication Edition)
========================================================================
Compiles the comprehensive, publication-grade 12-Volume medical textbook:
"THE ZAYVORA DOCTRINE: The Principles & Practice of Computational Integrative Medicine & Health OS"
(قانونِ زیورا: علم الطب، جدید مالیکیولر فارماکولوجی اور کلینیکل ہیلتھ آپریٹنگ سسٹم کا جامع انسائیکلوپیڈیا)

Outputs:
  - docs/THE_ZAYVORA_DOCTRINE_MASTER_BOOK.md (Full Academic Markdown)
  - docs/THE_ZAYVORA_DOCTRINE_MASTER_BOOK.html (Publication-Ready Interactive Hardcover eBook)
"""

import sys
import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services.knowledge.app.data.canonical_treatises import CANONICAL_TREATISES
from services.knowledge.app.data.murakkabat_50_classical_formulary import CLASSICAL_MURAKKABAT_50
from services.live_api_server import get_db

VOLUME_METADATA = {
    "vol-01": {
        "title_en": "Volume I: Kulliyat-e-Tibb & Biophysical Homeostasis",
        "title_ur": "جلد اول: کلیاتِ طب، ارکان، اخلاط اور حیاتیاتی فعلیات",
        "desc": "The foundational biophysics of Greco-Arab medicine: Arkan (Elements), Akhlat (Humors), Mizaj (Temperament), and Quwa & Afaal (Physiological Faculties) mapped to modern cellular thermodynamics, entropy, and allostatic load."
    },
    "vol-02": {
        "title_en": "Volume II: Asbab-e-Sittah Zarooriyyah (Lifestyle Determinants)",
        "title_ur": "جلد دوم: اسبابِ ستہ ضروریہ اور ماحولیاتی لائف اسٹائل میڈیسن",
        "desc": "Chrono-nutrition, atmospheric aeration, physical exercise bioenergetics, sleep architecture, coction/retention dynamics, and psychoneuroimmunology."
    },
    "vol-03": {
        "title_en": "Volume III: Classical Clinical Semiology & Diagnostics",
        "title_ur": "جلد سوم: علم النبض، قارورہ اور لسان — کلاسیکل طبی تشخیص",
        "desc": "The 10 Ajnas of arterial pulse waveforms, physical urine sediment stratification (Qaroorah), and tongue mucosal semiology."
    },
    "vol-04": {
        "title_en": "Volume IV: Laboratory Biomarkers & Clinical Chemistry",
        "title_ur": "جلد چہارم: کلینیکل لیبارٹری بائیو مارکرز اور مالیکیولر پینلز",
        "desc": "Harmonization of hs-CRP, ESR, cytokines, HbA1c, lipid sub-fractionation, and hepatorenal panels with humoral dyscrasias."
    },
    "vol-05": {
        "title_en": "Volume V: Diagnostic Imaging & Structural Phenotyping",
        "title_ur": "جلد پنجم: تشخیصی ریڈیولوجی اور اسٹرکچرل فینوٹائپنگ",
        "desc": "X-Ray, MRI, FibroScan, and Doppler ultrasound concordance in degenerative, inflammatory, and oncological pathologies."
    },
    "vol-06": {
        "title_en": "Volume VI: Hazm-e-Awwal & Gastrointestinal Metagenomics",
        "title_ur": "جلد ششم: ہضمِ اول اور گٹ مائیکروبائیوم میٹاجینومکس",
        "desc": "The gastrointestinal tract as the primary humoral coction factory, short-chain fatty acids (SCFAs), dysbiosis, and epigenetic host modulation."
    },
    "vol-07": {
        "title_en": "Volume VII: Digital Telemetry, Wearables & Computer Vision",
        "title_ur": "جلد ہفتم: ڈیجیٹل ٹیلی میٹری، ویئرایبلز اور کمپیوٹر ویژن",
        "desc": "Continuous Glucose Monitoring (CGM), Heart Rate Variability (HRV), photoplethysmography pulse wave decomposition, and smartphone facial/tongue diagnostic vision."
    },
    "vol-08": {
        "title_en": "Volume VIII: Master Botanical Pharmacopoeia & Toxicology",
        "title_ur": "جلد ہشتم: جامع نباتاتی فارماکوپیا اور سموم کی سائنسی شدھی",
        "desc": "Over 1,280 codified monographs, statutory Schedule E(1) Mudabbar detoxification SOPs, and Badal/Musleh substitution dynamics."
    },
    "vol-09": {
        "title_en": "Volume IX: The Four Canonical Therapeutic Modalities",
        "title_ur": "جلد نہم: چاروں ارکانِ علاج — غذا، تدبیر، دوا اور جراحت",
        "desc": "Ilaj bil Ghiza, the 16 regimenal therapies (Hijama, Fasd, Dalk, Hammam, Tareeq), Ilaj bil Dawa, and minor surgical intervention (Ilaj bil Yad)."
    },
    "vol-10": {
        "title_en": "Volume X: Integrative Neuropsychiatry & Psychosomatic Medicine",
        "title_ur": "جلد دہم: امراضِ نفسیات، مالیخولیا اور صوفیانہ اعصابی علاج",
        "desc": "Classical Melancholia, anxiety, and obsessive disorders mapped to neuro-inflammation, vagus nerve stimulation, and adaptogenic botanicals."
    },
    "vol-11": {
        "title_en": "Volume XI: Specialized Clinical Medicine (Gynecology, Pediatrics & Geriatrics)",
        "title_ur": "جلد یازدہم: خصوصی طبی شعبہ جات — نسواں، اطفال، اور مشائخ",
        "desc": "PCOS, infertility, hormonal dysregulation, pediatric growth and immune vigor, and geriatric degenerative longevity protocols."
    },
    "vol-12": {
        "title_en": "Volume XII: Drug Safety, Regulatory Compliance & Health OS",
        "title_ur": "جلد دوازدہم: ادویاتی حفاظت، قانونی تقاضے اور ہیلتھ آپریٹنگ سسٹم",
        "desc": "CYP450 herb-drug interaction matrix, 21 CFR Part 11 cryptographic Merkle ledger, Fast Matab clinical ergonomics, and WHO/ABDM federation standards."
    }
}

def generate_markdown_book():
    print("Compiling Master Academic Markdown Treatise...")
    lines = []
    
    # Title Page
    lines.append("# THE ZAYVORA DOCTRINE")
    lines.append("## The Principles & Practice of Computational Integrative Medicine and Health OS")
    lines.append("### قانونِ زیورا: علم الطب، جدید مالیکیولر فارماکولوجی اور کلینیکل ہیلتھ آپریٹنگ سسٹم کا جامع انسائیکلوپیڈیا\n")
    lines.append("**Author & Chief Clinical Architect:** Hakeem Dr. Irfan Ashraf (BUMS, Aligarh Muslim University, Batch 2002 — Passed 2007)")
    lines.append("**Academic & Alma Mater Affiliation:** Ajmal Khan Tibbiya College, Aligarh Muslim University (AMU), Batch of 2002 (Graduated 2007) • ZAYVORA Integrative Healthcare & Research Centre Consortium")
    lines.append("**Edition:** Definitive First Edition — September 2026")
    lines.append("**Statutory Legal Registry:** Facility ID: ZAY-DEL-01 • Reg. No: (Updating / Verification in Progress) • NABH Matab SOP • Architected for compliance with US FDA 21 CFR Part 11")
    lines.append("**International Standard Book Number (ISBN):** Provisional / Registration In Progress (Raja Rammohun Roy National Agency for ISBN, Ministry of Education, New Delhi)\n")
    lines.append("---\n")

    lines.append("### Statutory Medical Ethics & Educational Vignette Disclosure")
    lines.append("> **LEGAL & REGULATORY NOTICE:** In compliance with the **Drugs and Magic Remedies (Objectionable Advertisements) Act, 1954**, the National Commission for Indian System of Medicine (NCISM) professional conduct standards, and medical academic conventions:")
    lines.append("> 1. **Educational Illustrative Models:** All patient vignettes and clinical cases detailed in Section §5 across the 12 volumes are de-identified illustrative composite cases synthesized from observational clinical registries, classic Unani semiology patterns, and published peer-reviewed cohort studies (*e.g., Ambiye et al. 2013, Terteit et al. 2010*). They serve exclusively as pedagogical training instruments and clinical decision-support logic demonstrations for licensed healthcare practitioners.")
    lines.append("> 2. **No Guaranteed Therapeutic Claims:** Greco-Arab / Unani medicine recognizes that biological and humoral responses vary fundamentally according to each patient's innate constitutional temperament (*Mizaj-e-Asli*), disease chronicity, environmental factors (*Asbab-e-Sittah Zarooriyyah*), and regimen adherence. No outcome presented herein guarantees or implies an unconditional cure or therapeutic result.")
    lines.append("> 3. **Classical Textual Editions:** Classical Greco-Arab citations referenced throughout this treatise from Ibn Sina's *Al-Qanun fi al-Tibb* and Al-Razi's *Kitab al-Hawi* reference the canonical editions published by the Institute of History of Medicine and Medical Research (Jamia Hamdard, New Delhi, 1993) and the Central Council for Research in Unani Medicine (CCRUM, Ministry of AYUSH, Govt. of India, 2007).\n")
    lines.append("---\n")

    # Front Matter: Dedication & Epigraph
    lines.append("## Dedication & Epigraph\n")
    lines.append("> *\"Medicine is the science by which we learn the various states of the human body, in health, when not in health, the means by which health is likely to be lost, and, when lost, is likely to be restored to health.\"*\n")
    lines.append("> — **Ibn Sina (Avicenna)**, *Al-Qanun fi al-Tibb* (The Canon of Medicine), Book I, 1025 CE (Jamia Hamdard 1993 Critical Edition)\n")
    lines.append("\n")
    lines.append("> *\"The constancy of the internal environment (Milieu Intérieur) is the condition for free and independent life.\"*\n")
    lines.append("> — **Claude Bernard**, *An Introduction to the Study of Experimental Medicine*, 1865 CE\n")
    lines.append("\n")
    lines.append("Dedicated to the venerable Hakims, Tabibs, and clinical scholars across millennia whose observational genius decoded the humors of nature, and to the modern biomedical scientists building the molecular bridges that unite traditional wisdom with computational rigor.\n")
    lines.append("---\n")

    # Author's Preface
    lines.append("## Author's Preface\n")
    lines.append("### By Hakeem Dr. Irfan Ashraf (BUMS, Aligarh Muslim University, Batch 2002 — Passed 2007)\n")
    lines.append("Entering the revered halls of **Ajmal Khan Tibbiya College, Aligarh Muslim University (AMU)** as part of the **Batch of 2002**, and graduating with my Bachelor of Unani Medicine & Surgery (BUMS) in **2007** from this historic cradle founded under the luminous vision of Masih-ul-Mulk Hakeem Ajmal Khan, my clinical journey has been animated by a singular resolve: to elevate the venerable wisdom of classical Greco-Arab medicine into a mathematically precise, verifiable, and technologically advanced computational architecture.\n")
    lines.append("For centuries, the classical medical doctrine of Unani Medicine (*Tibb-e-Unani*) has been treated by conventional allopathic medicine as either an archaic historical curiosity or an unquantifiable empirical tradition. Conversely, contemporary biomedicine has increasingly fragmented human physiology into isolated molecular targets, frequently losing sight of the systemic, whole-organism balance that determines chronic wellness and disease recovery.\n")
    lines.append("The **ZAYVORA Doctrine** was born out of an imperative clinical need: to create a unified scientific grammar where the qualitative genius of Greco-Arab humoral physiology (*Arkan, Mizaj, Akhlat, A'za-e-Ra'isah*) meets the quantitative precision of systems biology, network pharmacology, and real-time clinical computation.\n")
    lines.append("This treatise is not merely a theoretical exposition. It is the architectural blueprint of an operational Clinical Health Operating System (ZAYVORA Health OS) designed to sit at the elbow of the practicing physician, safeguarding patient safety, accelerating diagnosis through the 60-Second Fast Matab™ framework, and proving with mathematical and biochemical clarity that ancient therapeutics possess profound modern mechanisms.\n")
    lines.append("---\n")

    # Table of Contents
    lines.append("## Complete Table of Contents\n")
    for vid, vmeta in sorted(VOLUME_METADATA.items()):
        lines.append(f"### {vmeta['title_en']}")
        lines.append(f"*{vmeta['title_ur']}*\n")
        lines.append(f"_{vmeta['desc']}_\n")
        v_chs = [t for t in CANONICAL_TREATISES.values() if t.get("volume_id") == vid]
        for ch in v_chs:
            lines.append(f"- **Chapter {ch['chapter_id']}**: {ch['chapter_title_en']} ({ch['chapter_title_ur']})")
        lines.append("")

    lines.append("### Appendices")
    lines.append("- **Appendix A**: The 59 Canonical Classical Murakkabat Formulary (NFUM & Bayaz-e-Kabir)")
    lines.append("- **Appendix B**: The 60-Second Fast Matab™ Clinical Workflow Manual & Bilingual Prescription SOP")
    lines.append("- **Appendix C**: Master Herb-Drug Interaction (HDI) Safety & CYP450 Clearance Matrix\n")
    lines.append("---\n")

    # Populate Volumes & Chapters
    for vid, vmeta in sorted(VOLUME_METADATA.items()):
        lines.append(f"# {vmeta['title_en']}")
        lines.append(f"## {vmeta['title_ur']}\n")
        lines.append(f"> **Volume Synopsis:** {vmeta['desc']}\n\n")

        v_chs = [t for t in CANONICAL_TREATISES.values() if t.get("volume_id") == vid]
        for ch in v_chs:
            lines.append(f"## Chapter {ch['chapter_id'].split('-')[1]}.{ch['chapter_id'].split('-')[2]}: {ch['chapter_title_en']}")
            lines.append(f"### {ch['chapter_title_ur']}\n")

            lines.append("#### §1. Classical Philosophy & Canonical Doctrine")
            lines.append(ch.get("canonical_philosophy_and_doctrine", "").strip() + "\n")

            lines.append("#### §2. Molecular & Cellular Pathophysiology")
            lines.append(ch.get("molecular_and_cellular_pathophysiology", "").strip() + "\n")

            lines.append("#### §3. Step-by-Step Clinical Examination Protocol")
            lines.append(ch.get("step_by_step_clinical_examination", "").strip() + "\n")

            lines.append("#### §4. Comprehensive Pharmacopoeia & Recipes")
            lines.append(ch.get("comprehensive_pharmacopeia_and_recipes", "").strip() + "\n")

            lines.append("#### §5. Documented Clinical Case Study (Pedagogical Composite Model)")
            lines.append(ch.get("clinical_case_study", "").strip() + "\n")

            lines.append("---\n")

    # Appendices
    lines.append("# Appendix A: The 59 Canonical Classical Murakkabat Formulary")
    lines.append("## ضمیمہ الف: قرابادینِ زیورا — ۵۹ معیاری کلاسیکل مرکبات کا مکمل نسخہ جات انسائیکلوپیڈیا\n")
    lines.append("Standardized formulations from the National Formulary of Unani Medicine (NFUM) and Bayaz-e-Kabir, mapped to 12 organ-axes, key active constituents, dose, and clinical indications.\n")

    for i, m in enumerate(CLASSICAL_MURAKKABAT_50, 1):
        lines.append(f"### {i}. {m['name']} ({m.get('urdu_name', '')})")
        lines.append(f"- **Category:** {m.get('category')} | **Classical Source:** {m.get('classical_source')}")
        lines.append(f"- **Classical Indication:** {m.get('classical_indication')}")
        lines.append(f"- **Chief Ingredients:** {', '.join(m.get('chief_ingredients', [])) if isinstance(m.get('chief_ingredients'), list) else m.get('chief_ingredients')}")
        lines.append(f"- **Posology & Vehicle (Badraqa):** {m.get('dose')}")
        lines.append(f"- **Molecular Mechanism:** {m.get('mechanism_of_action', 'Anti-inflammatory and humoral balancing action.')}\n")

    lines.append("# Appendix B: The 60-Second Fast Matab™ Clinical Workflow Manual")
    lines.append("## ضمیمہ ب: کلینیکل گائیڈ — ۶۰ سیکنڈ فاسٹ مطب موڈ اور مریض کی نسخہ پرچی\n")
    lines.append("Detailed operational guidelines for managing 60–80 patients per day in high-throughput outpatient departments while guaranteeing 100% adherence to multi-scale safety invariants and bilingual patient compliance.\n")

    out_md = os.path.join(BASE_DIR, "docs", "THE_ZAYVORA_DOCTRINE_MASTER_BOOK.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ Generated Markdown: {out_md} ({os.path.getsize(out_md)} bytes)")
    return out_md

def generate_html_ebook():
    print("Compiling Modern Interactive Hardcover HTML eBook...")
    
    # Calculate word count and page estimate
    total_words = 0
    for t in CANONICAL_TREATISES.values():
        total_words += sum(len(str(v).split()) for v in t.values())
    total_words += len(CLASSICAL_MURAKKABAT_50) * 120 + 3500
    est_pages = int(total_words / 260)  # Standard academic book layout: ~260 words/page with tables and callouts

    html = f"""<!DOCTYPE html>
<html lang="en" class="theme-ivory">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>THE ZAYVORA DOCTRINE — Master Medical Treatise &amp; Textbook</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Cinzel:wght@600;700;900&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;0,6..72,700;1,6..72,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <style>
    /* =========================================================================
       CSS VARIABLES & THREE LUXURY PUBLICATION THEMES
       ========================================================================= */
    :root {{
      --font-body: 'Newsreader', Georgia, serif;
      --font-display: 'Cinzel', serif;
      --font-sans: 'Plus Jakarta Sans', sans-serif;
      --font-urdu: 'Amiri', serif;
      --font-mono: 'JetBrains Mono', monospace;
      --base-font-size: 16.5px;
      --line-height: 1.8;
    }}

    /* THEME 1: IVORY LIBRARY (Default High-End Physical Book) */
    html.theme-ivory {{
      --bg-page: #fbf9f5;
      --bg-surface: #ffffff;
      --bg-card: #fdfcf9;
      --bg-inset: #f3efe6;
      --border: #e2d9c8;
      --border-subtle: #ede6d8;
      --text: #1c1a17;
      --text-muted: #665f54;
      --text-dim: #8c8273;
      --primary: #0f5132;
      --primary-tint: #e8f5e9;
      --accent: #b45309;
      --accent-tint: #fef3c7;
      --shadow: 0 10px 30px rgba(0,0,0,0.06);
      --cover-grad: radial-gradient(circle at center, #1b382b 0%, #0d1e16 100%);
      --header-bg: rgba(251, 249, 245, 0.94);
    }}

    /* THEME 2: OBSIDIAN DARK (Deep Modern Scholar Mode) */
    html.theme-obsidian {{
      --bg-page: #0a0e17;
      --bg-surface: #101622;
      --bg-card: #131b2a;
      --bg-inset: #0e1420;
      --border: #222f46;
      --border-subtle: #192334;
      --text: #f0f4fc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --primary: #10b981;
      --primary-tint: rgba(16, 185, 129, 0.15);
      --accent: #f59e0b;
      --accent-tint: rgba(245, 158, 11, 0.15);
      --shadow: 0 15px 35px rgba(0,0,0,0.6);
      --cover-grad: radial-gradient(circle at center, #13241b 0%, #090d14 70%);
      --header-bg: rgba(10, 14, 23, 0.94);
    }}

    /* THEME 3: SEPIA PARCHMENT (Classical Manuscript Mode) */
    html.theme-sepia {{
      --bg-page: #f4ebd9;
      --bg-surface: #faeedb;
      --bg-card: #fdf3e2;
      --bg-inset: #ebdcc0;
      --border: #d4be9b;
      --border-subtle: #decbb0;
      --text: #2c2217;
      --text-muted: #735e47;
      --text-dim: #99836a;
      --primary: #2d5a27;
      --primary-tint: rgba(45, 90, 39, 0.12);
      --accent: #8f3f0e;
      --accent-tint: rgba(143, 63, 14, 0.12);
      --shadow: 0 10px 25px rgba(60,40,15,0.08);
      --cover-grad: radial-gradient(circle at center, #352516 0%, #1d140b 100%);
      --header-bg: rgba(244, 235, 217, 0.94);
    }}

    /* Global Resets */
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg-page);
      color: var(--text);
      font-family: var(--font-body);
      font-size: var(--base-font-size);
      line-height: var(--line-height);
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
      transition: background-color 0.3s ease, color 0.3s ease;
    }}

    /* Reading Progress Bar */
    #progress-bar {{
      position: fixed;
      top: 0;
      left: 0;
      height: 4px;
      background: linear-gradient(90deg, var(--primary), var(--accent));
      width: 0%;
      z-index: 1000;
      transition: width 0.1s ease;
    }}

    /* Top Navigation Studio Bar */
    .studio-bar {{
      position: sticky;
      top: 0;
      z-index: 900;
      background: var(--header-bg);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      padding: 10px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }}
    .brand-title {{
      font-family: var(--font-display);
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 1px;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .brand-badge {{
      display: inline-block;
      font-family: var(--font-sans);
      font-size: 10px;
      padding: 2px 8px;
      border-radius: 9999px;
      background: var(--primary-tint);
      color: var(--primary);
      font-weight: 700;
    }}
    .studio-controls {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .search-input {{
      padding: 6px 12px 6px 32px;
      border-radius: 20px;
      border: 1px solid var(--border);
      background: var(--bg-surface);
      color: var(--text);
      font-family: var(--font-sans);
      font-size: 12px;
      outline: none;
      width: 180px;
      transition: all 0.2s ease;
    }}
    .search-input:focus {{
      width: 260px;
      border-color: var(--primary);
    }}
    .search-wrapper {{
      position: relative;
    }}
    .search-icon {{
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 11px;
      color: var(--text-dim);
      pointer-events: none;
    }}
    .ctrl-btn {{
      padding: 6px 12px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--bg-surface);
      color: var(--text);
      font-family: var(--font-sans);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .ctrl-btn:hover {{
      border-color: var(--primary);
      background: var(--primary-tint);
      color: var(--primary);
    }}
    .ctrl-btn.active {{
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
    }}

    /* Main Container */
    .book-wrapper {{
      max-width: 960px;
      margin: 0 auto;
      padding: 50px 24px 100px 24px;
    }}

    /* Hardcover Book Dust Jacket */
    .book-jacket {{
      background: var(--cover-grad);
      color: #ffffff;
      border-radius: 20px;
      padding: 90px 40px;
      text-align: center;
      position: relative;
      border: 3px solid #b89146;
      box-shadow: 0 30px 60px rgba(0,0,0,0.5);
      margin-bottom: 70px;
      overflow: hidden;
    }}
    .book-jacket::before {{
      content: "";
      position: absolute;
      inset: 12px;
      border: 1px solid rgba(212, 175, 55, 0.4);
      border-radius: 12px;
      pointer-events: none;
    }}
    .book-jacket::after {{
      content: "";
      position: absolute;
      inset: 18px;
      border: 1px dashed rgba(212, 175, 55, 0.25);
      border-radius: 8px;
      pointer-events: none;
    }}
    .gold-crest {{
      width: 70px;
      height: 70px;
      margin: 0 auto 20px auto;
      border-radius: 50%;
      border: 2px solid #d4af37;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 32px;
      background: rgba(0,0,0,0.3);
      box-shadow: 0 0 25px rgba(212, 175, 55, 0.3);
    }}
    .jacket-tag {{
      display: inline-block;
      font-family: var(--font-sans);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: #d4af37;
      margin-bottom: 15px;
    }}
    .jacket-title {{
      font-family: var(--font-display);
      font-size: 52px;
      font-weight: 900;
      letter-spacing: 2px;
      line-height: 1.15;
      margin-bottom: 12px;
      color: #ffffff;
      text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }}
    .jacket-subtitle {{
      font-family: var(--font-sans);
      font-size: 18px;
      font-weight: 400;
      color: #f1ebd8;
      max-width: 680px;
      margin: 0 auto 20px auto;
      line-height: 1.5;
    }}
    .jacket-urdu-title {{
      font-family: var(--font-urdu);
      font-size: 36px;
      direction: rtl;
      color: #e5cf98;
      margin-bottom: 35px;
    }}
    .jacket-author-block {{
      border-top: 1px solid rgba(212, 175, 55, 0.3);
      padding-top: 30px;
      margin-top: 30px;
    }}
    .jacket-author {{
      font-family: var(--font-sans);
      font-size: 20px;
      font-weight: 700;
      color: #ffffff;
    }}
    .jacket-creds {{
      font-family: var(--font-sans);
      font-size: 13px;
      color: #d1d5db;
      margin-top: 4px;
    }}
    .jacket-edition {{
      font-family: var(--font-mono);
      font-size: 11px;
      color: #d4af37;
      margin-top: 12px;
      letter-spacing: 1px;
    }}

    /* Book Meta Bar */
    .book-stat-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 20px;
      margin-bottom: 50px;
      box-shadow: var(--shadow);
    }}
    .stat-box {{
      text-align: center;
      border-right: 1px solid var(--border-subtle);
    }}
    .stat-box:last-child {{ border-right: none; }}
    .stat-val {{
      font-family: var(--font-sans);
      font-size: 22px;
      font-weight: 800;
      color: var(--primary);
    }}
    .stat-lbl {{
      font-family: var(--font-sans);
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-top: 2px;
    }}

    /* Front Matter Editorial Pages */
    .front-matter {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 44px;
      margin-bottom: 60px;
      box-shadow: var(--shadow);
    }}
    .front-heading {{
      font-family: var(--font-display);
      font-size: 24px;
      font-weight: 700;
      color: var(--text);
      border-bottom: 2px solid var(--primary);
      padding-bottom: 10px;
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }}
    .epigraph-box {{
      font-style: italic;
      border-left: 4px solid var(--accent);
      padding: 16px 24px;
      background: var(--accent-tint);
      border-radius: 0 12px 12px 0;
      margin: 24px 0;
      color: var(--text);
    }}
    .epigraph-cite {{
      display: block;
      font-style: normal;
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 700;
      margin-top: 8px;
      color: var(--accent);
    }}

    /* Table of Contents Grid */
    .toc-container {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 40px;
      margin-bottom: 60px;
      box-shadow: var(--shadow);
    }}
    .toc-title {{
      font-family: var(--font-display);
      font-size: 26px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 24px;
      border-bottom: 2px solid var(--primary);
      padding-bottom: 8px;
    }}
    .toc-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }}
    .toc-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 16px;
      text-decoration: none;
      color: var(--text);
      display: block;
      transition: all 0.2s ease;
    }}
    .toc-card:hover {{
      border-color: var(--primary);
      background: var(--primary-tint);
      transform: translateY(-2px);
    }}
    .toc-vol-no {{
      font-family: var(--font-sans);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--primary);
    }}
    .toc-vol-name {{
      font-family: var(--font-display);
      font-size: 14.5px;
      font-weight: 700;
      margin: 4px 0;
      color: var(--text);
    }}
    .toc-vol-ur {{
      font-family: var(--font-urdu);
      font-size: 16px;
      color: var(--text-dim);
      direction: rtl;
    }}

    /* Volume Banner */
    .volume-banner {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-left: 8px solid var(--primary);
      border-radius: 14px;
      padding: 30px;
      margin: 70px 0 35px 0;
      box-shadow: var(--shadow);
      page-break-before: always;
    }}
    .vol-badge {{
      font-family: var(--font-sans);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: var(--primary);
    }}
    .vol-title-en {{
      font-family: var(--font-display);
      font-size: 28px;
      font-weight: 700;
      color: var(--text);
      margin: 6px 0;
    }}
    .vol-title-ur {{
      font-family: var(--font-urdu);
      font-size: 24px;
      color: var(--accent);
      direction: rtl;
      margin-bottom: 12px;
    }}
    .vol-desc {{
      font-size: 14.5px;
      color: var(--text-muted);
      line-height: 1.6;
    }}

    /* Treatise / Chapter Card */
    .chapter-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 40px;
      margin-bottom: 45px;
      box-shadow: var(--shadow);
      position: relative;
    }}
    .chapter-header {{
      border-bottom: 1px solid var(--border);
      padding-bottom: 20px;
      margin-bottom: 30px;
    }}
    .chapter-meta {{
      font-family: var(--font-sans);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--primary);
      margin-bottom: 6px;
    }}
    .chapter-title-en {{
      font-family: var(--font-display);
      font-size: 25px;
      font-weight: 700;
      color: var(--text);
      line-height: 1.3;
    }}
    .chapter-title-ur {{
      font-family: var(--font-urdu);
      font-size: 26px;
      color: var(--accent);
      direction: rtl;
      margin-top: 6px;
    }}

    /* Editorial Sections */
    .section-module {{
      margin-bottom: 32px;
    }}
    .section-tag {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-sans);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: var(--accent);
      background: var(--accent-tint);
      padding: 4px 12px;
      border-radius: 6px;
      margin-bottom: 14px;
    }}
    .prose-text {{
      font-size: var(--base-font-size);
      line-height: var(--line-height);
      color: var(--text);
      white-space: pre-line;
    }}
    .prose-text strong {{
      color: var(--text);
      font-weight: 700;
    }}

    /* Drop Cap for Editorial Polish */
    .drop-cap::first-letter {{
      font-family: var(--font-display);
      font-size: 3.4em;
      float: left;
      line-height: 0.85;
      margin-right: 10px;
      margin-top: 4px;
      color: var(--primary);
      font-weight: 700;
    }}

    /* Callout Boxes */
    .callout-pearl {{
      background: var(--accent-tint);
      border-left: 4px solid var(--accent);
      border-radius: 0 12px 12px 0;
      padding: 18px 24px;
      margin: 24px 0;
    }}
    .callout-molecular {{
      background: var(--primary-tint);
      border-left: 4px solid var(--primary);
      border-radius: 0 12px 12px 0;
      padding: 18px 24px;
      margin: 24px 0;
    }}
    .callout-title {{
      font-family: var(--font-sans);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 6px;
    }}

    /* Appendix Murakkabat Grid */
    .formulary-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 16px;
      margin-top: 20px;
    }}
    .form-item {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 16px;
    }}
    .form-item-name {{
      font-family: var(--font-sans);
      font-weight: 700;
      font-size: 14.5px;
      color: var(--text);
    }}
    .form-item-ur {{
      font-family: var(--font-urdu);
      font-size: 17px;
      color: var(--primary);
      margin-left: 8px;
    }}

    /* Floating Table of Contents Drawer */
    #toc-drawer {{
      position: fixed;
      right: -360px;
      top: 55px;
      bottom: 0;
      width: 360px;
      background: var(--bg-surface);
      border-left: 1px solid var(--border);
      box-shadow: -10px 0 30px rgba(0,0,0,0.15);
      z-index: 850;
      overflow-y: auto;
      padding: 24px;
      transition: right 0.3s ease;
    }}
    #toc-drawer.open {{
      right: 0;
    }}
    .drawer-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
    }}

    /* =========================================================================
       PRINT & PDF BOOK BINDING OPTIMIZATIONS (@media print)
       ========================================================================= */
    @page {{
      size: A4;
      margin: 25mm 20mm 25mm 20mm;
      @bottom-center {{
        content: "Page " counter(page);
        font-family: 'Newsreader', Georgia, serif;
        font-size: 9pt;
        color: #334155;
      }}
      @top-center {{
        content: "THE ZAYVORA DOCTRINE &bull; Master Medical Treatise";
        font-family: 'Cinzel', serif;
        font-size: 8pt;
        color: #475569;
        letter-spacing: 1px;
      }}
    }}
    @media print {{
      :root, html, body {{
        --bg-page: #ffffff !important;
        --bg-surface: #ffffff !important;
        --bg-card: #ffffff !important;
        --bg-inset: #f8fafc !important;
        --border: #cbd5e1 !important;
        --border-subtle: #e2e8f0 !important;
        --text: #0f172a !important;
        --text-muted: #334155 !important;
        --text-dim: #475569 !important;
        --primary: #065f46 !important;
        --primary-tint: #ecfdf5 !important;
        --accent: #92400e !important;
        --accent-tint: #fffbeb !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-size: 10.5pt !important;
        line-height: 1.6 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }}
      * {{
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        text-shadow: none !important;
      }}
      #progress-bar, .studio-bar, #toc-drawer, .search-wrapper {{
        display: none !important;
      }}
      .book-wrapper {{
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
      }}

      /* 1. Dust Jacket (Cover Page) */
      .book-jacket {{
        background: #0d281e !important;
        color: #ffffff !important;
        border: 4px solid #b45309 !important;
        box-shadow: none !important;
        padding: 80px 30px !important;
        page-break-after: always !important;
        break-after: page !important;
        margin-bottom: 0 !important;
      }}
      .book-jacket * {{
        color: #ffffff !important;
      }}
      .book-jacket .gold-crest {{
        border-color: #f59e0b !important;
        color: #f59e0b !important;
        box-shadow: none !important;
        background: rgba(0,0,0,0.3) !important;
      }}
      .book-jacket .jacket-tag {{
        color: #fbbf24 !important;
      }}
      .book-jacket .jacket-title {{
        color: #ffffff !important;
      }}
      .book-jacket .jacket-subtitle {{
        color: #f1f5f9 !important;
      }}
      .book-jacket .jacket-urdu-title {{
        color: #fef3c7 !important;
      }}
      .book-jacket .jacket-author {{
        color: #ffffff !important;
      }}
      .book-jacket .jacket-creds {{
        color: #e2e8f0 !important;
      }}
      .book-jacket .jacket-edition {{
        color: #fcd34d !important;
      }}
      .book-jacket::before, .book-jacket::after {{
        border-color: rgba(251, 191, 36, 0.5) !important;
      }}

      /* 2. Stats Grid */
      .book-stat-grid {{
        background: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
        page-break-inside: avoid !important;
        margin-top: 20px !important;
        margin-bottom: 25px !important;
      }}
      .stat-val {{
        color: #065f46 !important;
      }}
      .stat-lbl {{
        color: #475569 !important;
      }}

      /* 3. Front Matter & Cards */
      .front-matter {{
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: none !important;
        page-break-inside: avoid !important;
        margin-bottom: 25px !important;
      }}
      .front-heading {{
        color: #0f172a !important;
        border-bottom-color: #065f46 !important;
      }}
      .front-matter p, .front-matter div, .front-matter span {{
        color: #1e293b !important;
      }}
      .epigraph-box {{
        background: #fffbeb !important;
        border-left: 4px solid #b45309 !important;
        color: #1e293b !important;
      }}
      .epigraph-cite {{
        color: #92400e !important;
      }}

      /* 4. Table of Contents */
      .toc-container {{
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: none !important;
        page-break-after: always !important;
        break-after: page !important;
      }}
      .toc-title {{
        color: #0f172a !important;
        border-bottom-color: #065f46 !important;
      }}
      .toc-card {{
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        color: #0f172a !important;
      }}
      .toc-vol-no {{
        color: #065f46 !important;
      }}
      .toc-vol-name {{
        color: #0f172a !important;
      }}
      .toc-vol-ur {{
        color: #92400e !important;
      }}

      /* 5. Volume Banners */
      .volume-banner {{
        background: #f0fdf4 !important;
        border: 1px solid #cbd5e1 !important;
        border-left: 8px solid #065f46 !important;
        page-break-before: always !important;
        break-before: page !important;
        page-break-inside: avoid !important;
        margin-top: 0 !important;
        margin-bottom: 25px !important;
      }}
      .vol-badge {{
        color: #065f46 !important;
      }}
      .vol-title-en {{
        color: #042f2e !important;
      }}
      .vol-title-ur {{
        color: #92400e !important;
      }}
      .vol-desc {{
        color: #334155 !important;
      }}

      /* 6. Chapter Cards */
      .chapter-card {{
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: none !important;
        page-break-inside: avoid !important;
        margin-bottom: 25px !important;
      }}
      .chapter-header {{
        border-bottom-color: #e2e8f0 !important;
      }}
      .chapter-meta {{
        color: #065f46 !important;
      }}
      .chapter-title-en {{
        color: #0f172a !important;
      }}
      .chapter-title-ur {{
        color: #92400e !important;
      }}

      /* 7. Section Tags & Prose */
      .section-tag {{
        background: #fffbeb !important;
        border: 1px solid #fde68a !important;
        color: #92400e !important;
      }}
      .prose-text {{
        color: #1e293b !important;
      }}
      .prose-text strong {{
        color: #0f172a !important;
      }}
      .drop-cap::first-letter {{
        color: #065f46 !important;
      }}

      /* 8. Callout Boxes */
      .callout-pearl {{
        background: #fffbeb !important;
        border-left: 4px solid #b45309 !important;
        color: #1e293b !important;
      }}
      .callout-molecular {{
        background: #f0fdf4 !important;
        border-left: 4px solid #059669 !important;
        color: #1e293b !important;
      }}
      .callout-title {{
        color: #0f172a !important;
      }}

      /* 9. Formulary Grid & Items */
      .form-item {{
        background: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
        page-break-inside: avoid !important;
      }}
      .form-item-name {{
        color: #0f172a !important;
      }}
      .form-item-ur {{
        color: #065f46 !important;
      }}
      .form-item p {{
        color: #334155 !important;
      }}

      a {{
        text-decoration: none !important;
        color: #065f46 !important;
      }}
    }}
  </style>
</head>
<body>

  <!-- Reading Progress Bar -->
  <div id="progress-bar"></div>

  <!-- Studio Quick Action Bar -->
  <header class="studio-bar">
    <div class="brand-title">
      <span>🌿</span>
      <span>THE ZAYVORA DOCTRINE</span>
      <span class="brand-badge">EST. {est_pages} PAGES &bull; 12 VOLUMES</span>
    </div>

    <div class="search-wrapper">
      <span class="search-icon">🔍</span>
      <input type="text" id="bookSearch" class="search-input" placeholder="Search herbs, organs, pulse..." onkeyup="filterBookContent()">
    </div>

    <div class="studio-controls">
      <!-- Theme Switcher -->
      <button class="ctrl-btn" onclick="setBookTheme('theme-ivory')" title="Library Ivory Paper">📖 Ivory</button>
      <button class="ctrl-btn" onclick="setBookTheme('theme-obsidian')" title="Obsidian Dark Mode">🌌 Dark</button>
      <button class="ctrl-btn" onclick="setBookTheme('theme-sepia')" title="Sepia Parchment">📜 Sepia</button>

      <!-- Font Sizer -->
      <button class="ctrl-btn" onclick="adjustFontSize(-1)" title="Decrease Font">A-</button>
      <button class="ctrl-btn" onclick="adjustFontSize(1)" title="Increase Font">A+</button>

      <!-- Drawer Toggle -->
      <button class="ctrl-btn" onclick="toggleTocDrawer()" title="Table of Contents">📑 Chapters</button>

      <!-- Print to PDF -->
      <button class="ctrl-btn active" onclick="prepareAndPrintBook()" title="Print Hardcover PDF">🖨️ Print / Save PDF</button>
    </div>
  </header>

  <!-- Slide-out Table of Contents Drawer -->
  <aside id="toc-drawer">
    <div class="drawer-header">
      <strong style="font-family: var(--font-display); font-size: 15px;">Table of Contents</strong>
      <button onclick="toggleTocDrawer()" style="background:none; border:none; cursor:pointer; font-size: 16px;">✕</button>
    </div>
    <div style="display: flex; flex-direction: column; gap: 8px;">
"""

    for vid, vmeta in sorted(VOLUME_METADATA.items()):
        html += f"""
      <a href="#{vid}" onclick="toggleTocDrawer()" style="font-family: var(--font-sans); font-size: 12.5px; text-decoration: none; color: var(--text); padding: 6px 10px; border-radius: 6px; background: var(--bg-card); border: 1px solid var(--border-subtle);">
        <strong style="color: var(--primary);">{vmeta['title_en'].split(':')[0]}:</strong> {vmeta['title_en'].split(':')[1] if ':' in vmeta['title_en'] else vmeta['title_en']}
      </a>
"""

    html += f"""
      <a href="#appendix-a" onclick="toggleTocDrawer()" style="font-family: var(--font-sans); font-size: 12.5px; text-decoration: none; color: var(--text); padding: 6px 10px; border-radius: 6px; background: var(--bg-card); border: 1px solid var(--border-subtle);">
        <strong style="color: var(--accent);">Appendix A:</strong> 59 Murakkabat Formulary
      </a>
      <a href="#appendix-b" onclick="toggleTocDrawer()" style="font-family: var(--font-sans); font-size: 12.5px; text-decoration: none; color: var(--text); padding: 6px 10px; border-radius: 6px; background: var(--bg-card); border: 1px solid var(--border-subtle);">
        <strong style="color: var(--accent);">Appendix B:</strong> 60-Sec Fast Matab™ Manual
      </a>
    </div>
  </aside>

  <!-- Book Main Wrapper -->
  <main class="book-wrapper">

    <!-- Hardcover Book Dust Jacket -->
    <section class="book-jacket">
      <div class="gold-crest">⚕️</div>
      <span class="jacket-tag">DEFINITIVE ACADEMIC MEDICAL TEXTBOOK</span>
      <h1 class="jacket-title">The ZAYVORA Doctrine</h1>
      <p class="jacket-subtitle">The Principles &amp; Practice of Computational Integrative Medicine &amp; Health OS</p>
      <div class="jacket-urdu-title">قانونِ زیورا: علم الطب، جدید مالیکیولر فارماکولوجی اور کلینیکل ہیلتھ آپریٹنگ سسٹم</div>

      <div class="jacket-author-block">
        <div class="jacket-author">Hakeem Dr. Irfan Ashraf (BUMS)</div>
        <div class="jacket-creds">Bachelor of Unani Medicine &amp; Surgery (Ajmal Khan Tibbiya College, Aligarh Muslim University &bull; Batch 2002, Passed 2007) &bull; Chief Clinical Architect &bull; ZAYVORA Health OS Consortium</div>
        <div class="jacket-edition">ALIGARH MUSLIM UNIVERSITY ALUMNUS (BATCH 2002 – PASSED 2007) &bull; ISBN: REGISTRATION IN PROGRESS &bull; NEW DELHI &bull; LONDON</div>
      </div>
    </section>

    <!-- Book Metrics Quick Bar -->
    <section class="book-stat-grid">
      <div class="stat-box">
        <div class="stat-val">12</div>
        <div class="stat-lbl">Curated Volumes</div>
      </div>
      <div class="stat-box">
        <div class="stat-val">38</div>
        <div class="stat-lbl">Clinical Treatises</div>
      </div>
      <div class="stat-box">
        <div class="stat-val">59</div>
        <div class="stat-lbl">Classical Formulas</div>
      </div>
      <div class="stat-box">
        <div class="stat-val">~{est_pages}</div>
        <div class="stat-lbl">Standard Book Pages</div>
      </div>
    </section>

    <!-- Front Matter: Half-Title, CIP & Legal -->
    <section class="front-matter">
      <div class="front-heading">
        <span>Cataloging &amp; Statutory Legal Registry</span>
        <span style="font-size: 11px; font-family: var(--font-mono); color: var(--text-dim);">CIP-DATA-2026</span>
      </div>

      <div style="font-family: var(--font-mono); font-size: 12px; line-height: 1.7; color: var(--text-muted); background: var(--bg-inset); padding: 18px; border-radius: 8px; margin-bottom: 24px;">
        Title: The ZAYVORA Doctrine: Principles &amp; Practice of Computational Integrative Medicine and Health OS<br>
        Author: Ashraf, Irfan, Hakeem Dr. [BUMS, Ajmal Khan Tibbiya College, Aligarh Muslim University (Batch 2002, Passed 2007)]<br>
        Alma Mater: Ajmal Khan Tibbiya College, Aligarh Muslim University (AMU), Batch 2002 – Passed 2007<br>
        Publisher: ZAYVORA Academic Publishing Press, New Delhi &bull; London<br>
        Classification: Integrative Medicine &bull; Greco-Arab / Unani Systems Biology &bull; Computational Phytopharmacology<br>
        Statutory Compliance: Facility ID: ZAY-DEL-01 &bull; Reg. No: (Updating / Verification in Progress) &bull; NABH Matab SOP &bull; US FDA Title 21 CFR Part 11 Compliant<br>
        ISBN: Provisional / Registration In Progress (Raja Rammohun Roy National Agency for ISBN, Ministry of Education, Govt. of India)
      </div>

      <div class="epigraph-box" style="border-left-color: #059669; background: rgba(5, 150, 105, 0.08); font-style: normal; font-size: 12.5px; line-height: 1.6;">
        <strong style="color: #047857; text-transform: uppercase; letter-spacing: 0.5px; font-size: 11px; display: block; margin-bottom: 6px;">Statutory Medical Ethics &amp; Educational Vignette Disclosure</strong>
        In compliance with the <strong>Drugs and Magic Remedies (Objectionable Advertisements) Act, 1954</strong> and NCISM professional standards: All clinical cases detailed in Section §5 are de-identified illustrative composite cases synthesized from observational clinical registries, classic Unani semiology patterns, and published peer-reviewed cohort studies (e.g., Ambiye et al. 2013, Terteit et al. 2010) as pedagogical decision-support demonstrations. Biological and humoral responses vary based on individual constitutional temperament (Mizaj-e-Asli), chronicity, and regimen compliance; no outcome presented guarantees or implies an unconditional cure. Classical Greco-Arab citations reference the critical editions published by Jamia Hamdard (1993) and CCRUM (Ministry of AYUSH, 2007).
      </div>

      <div class="epigraph-box">
        "Medicine is the science by which we learn the various states of the human body, in health, when not in health, the means by which health is likely to be lost, and, when lost, is likely to be restored to health."
        <span class="epigraph-cite">— Ibn Sina (Avicenna), Al-Qanun fi al-Tibb (The Canon of Medicine), Book I, 1025 CE (Jamia Hamdard 1993 Critical Edition)</span>
      </div>

      <div class="epigraph-box">
        "The constancy of the internal environment (Milieu Intérieur) is the condition for free and independent life."
        <span class="epigraph-cite">— Claude Bernard, An Introduction to the Study of Experimental Medicine, 1865 CE</span>
      </div>
    </section>

    <!-- Front Matter: Author's Preface -->
    <section class="front-matter">
      <div class="front-heading">
        <span>Author's Preface &amp; Clinical Manifesto</span>
        <span style="font-size: 12px; font-family: var(--font-sans); color: var(--primary);">Hakeem Dr. Irfan Ashraf (BUMS)</span>
      </div>

      <p class="drop-cap" style="margin-bottom: 16px;">
        For centuries, the classical medical doctrine of Unani Medicine (Tibb-e-Unani) has been treated by conventional allopathic medicine as either an archaic historical curiosity or an unquantifiable empirical tradition. Conversely, contemporary biomedicine has increasingly fragmented human physiology into isolated molecular targets, frequently losing sight of the systemic, whole-organism balance that determines chronic wellness and disease recovery.
      </p>

      <p style="margin-bottom: 16px;">
        The <strong>ZAYVORA Doctrine</strong> was born out of an imperative clinical need: to create a unified scientific grammar where the qualitative genius of Greco-Arab humoral physiology (<em>Arkan, Mizaj, Akhlat, A'za-e-Ra'isah</em>) meets the quantitative precision of systems biology, network pharmacology, and real-time clinical computation.
      </p>

      <p style="margin-bottom: 16px;">
        This treatise is not merely a theoretical exposition. It is the architectural blueprint of an operational Clinical Health Operating System (ZAYVORA Health OS) designed to sit at the elbow of the practicing physician, safeguarding patient safety, accelerating diagnosis through the <strong>60-Second Fast Matab™ framework</strong>, and proving with mathematical and biochemical clarity that ancient therapeutics possess profound modern mechanisms.
      </p>

      <div class="callout-pearl">
        <div class="callout-title" style="color: var(--accent);">💎 Hakim's Clinical Invariant</div>
        Every biological organism is an open thermodynamic system governed by <em>Tabi'at</em> (the innate self-regulating healing force). The clinician's supreme duty is not to force chemical perturbation upon the body, but to assist <em>Tabi'at</em> through <em>Ilaj bil-Zidd</em> (treatment by contraries) and targeted cellular nutrition.
      </div>
    </section>

    <!-- Table of Contents -->
    <section class="toc-container" id="toc">
      <div class="toc-title">12-Volume Master Academic Curriculum</div>
      <div class="toc-grid">
"""

    for vid, vmeta in sorted(VOLUME_METADATA.items()):
        html += f"""
        <a href="#{vid}" class="toc-card">
          <div class="toc-vol-no">{vmeta['title_en'].split(':')[0]}</div>
          <div class="toc-vol-name">{vmeta['title_en'].split(':')[1] if ':' in vmeta['title_en'] else vmeta['title_en']}</div>
          <div class="toc-vol-ur">{vmeta['title_ur']}</div>
        </a>
"""

    html += """
      </div>
    </section>
"""

    # Populate Volumes & Treatises
    for vid, vmeta in sorted(VOLUME_METADATA.items()):
        html += f"""
    <!-- {vid.upper()} -->
    <section class="volume-banner" id="{vid}">
      <span class="vol-badge">{vid.upper()} &bull; CURRICULAR MONOGRAPH</span>
      <h2 class="vol-title-en">{vmeta['title_en']}</h2>
      <div class="vol-title-ur">{vmeta['title_ur']}</div>
      <p class="vol-desc">{vmeta['desc']}</p>
    </section>
"""

        v_chs = [t for t in CANONICAL_TREATISES.values() if t.get("volume_id") == vid]
        for ch in v_chs:
            ch_num = f"Chapter {ch['chapter_id'].split('-')[1]}.{ch['chapter_id'].split('-')[2]}"
            html += f"""
    <article class="chapter-card" id="{ch['chapter_id']}">
      <div class="chapter-header">
        <div class="chapter-meta">{ch_num} &bull; Clinical Doctrine</div>
        <h3 class="chapter-title-en">{ch['chapter_title_en']}</h3>
        <div class="chapter-title-ur">{ch['chapter_title_ur']}</div>
      </div>

      <div class="section-module">
        <div class="section-tag"><span>🏛️</span> §1. Classical Philosophy &amp; Canonical Doctrine</div>
        <div class="prose-text">{ch.get('canonical_philosophy_and_doctrine', '').strip()}</div>
      </div>

      <div class="section-module">
        <div class="section-tag" style="color: var(--primary); background: var(--primary-tint);"><span>🧬</span> §2. Molecular &amp; Cellular Pathophysiology</div>
        <div class="prose-text">{ch.get('molecular_and_cellular_pathophysiology', '').strip()}</div>
      </div>

      <div class="section-module">
        <div class="section-tag"><span>🩺</span> §3. Step-by-Step Clinical Examination Protocol</div>
        <div class="prose-text">{ch.get('step_by_step_clinical_examination', '').strip()}</div>
      </div>

      <div class="section-module">
        <div class="section-tag" style="color: var(--primary); background: var(--primary-tint);"><span>🌿</span> §4. Comprehensive Pharmacopoeia &amp; Recipes</div>
        <div class="prose-text">{ch.get('comprehensive_pharmacopeia_and_recipes', '').strip()}</div>
      </div>

      <div class="section-module">
        <div class="section-tag"><span>📋</span> §5. Documented Clinical Case Study (Pedagogical Composite Model)</div>
        <div class="prose-text">{ch.get('clinical_case_study', '').strip()}</div>
      </div>
    </article>
"""

    # Appendix A
    html += """
    <!-- APPENDIX A -->
    <section class="volume-banner" id="appendix-a">
      <span class="vol-badge">APPENDIX A &bull; STANDARD FORMULARY</span>
      <h2 class="vol-title-en">Appendix A: The 59 Canonical Classical Murakkabat Formulary</h2>
      <div class="vol-title-ur">ضمیمہ الف: قرابادینِ زیورا — ۵۹ معیاری کلاسیکل مرکبات کا مکمل نسخہ جات انسائیکلوپیڈیا</div>
      <p class="vol-desc">Standardized from the National Formulary of Unani Medicine (NFUM) and Bayaz-e-Kabir, mapped to 12 organ-axes, chief botanical constituents, posology, and molecular mechanisms.</p>
    </section>

    <div class="chapter-card">
      <div class="formulary-grid">
"""

    for i, m in enumerate(CLASSICAL_MURAKKABAT_50, 1):
        html += f"""
        <div class="form-item">
          <div>
            <span class="form-item-name">{i}. {m['name']}</span>
            <span class="form-item-ur">{m.get('urdu_name', '')}</span>
          </div>
          <div style="font-family: var(--font-sans); font-size: 11px; color: var(--accent); margin: 4px 0;">{m.get('category')} &bull; {m.get('classical_source')}</div>
          <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 6px;"><strong>Indication:</strong> {m.get('classical_indication')}</p>
          <div style="font-family: var(--font-mono); font-size: 11px; color: var(--primary);">Dose: {m.get('dose')}</div>
        </div>
"""

    # Appendix B
    html += """
      </div>
    </div>

    <!-- APPENDIX B -->
    <section class="volume-banner" id="appendix-b">
      <span class="vol-badge">APPENDIX B &bull; CLINICAL SOP MANUAL</span>
      <h2 class="vol-title-en">Appendix B: The 60-Second Fast Matab™ Clinical Workflow Manual</h2>
      <div class="vol-title-ur">ضمیمہ ب: کلینیکل گائیڈ — ۶۰ سیکنڈ فاسٹ مطب موڈ اور مریض کی نسخہ پرچی</div>
      <p class="vol-desc">Operational standard operating procedure (SOP) for high-throughput ambulatory OPD clinics, 10-Ajnas pulse capture, and bilingual prescription slip generation.</p>
    </section>

    <div class="chapter-card">
      <div class="section-module">
        <div class="section-tag"><span>⚡</span> High-Throughput Ambulatory Matab SOP</div>
        <div class="prose-text">
          In high-volume ambulatory clinical practice, clinicians require rapid cognitive synthesis without sacrificing multi-scale safety invariants. The ZAYVORA Fast Matab™ mode executes in four instantaneous steps:

          1. <strong>Chief Complaint Clustering</strong>: Single-click selection of the primary pathological axis (Waja-ul-Mafasil, Su-e-Hazm, Suda-e-Muzmin, Ziabetus Shakari, Zof-e-Bah).
          2. <strong>Classical Tashkhees Quick Drawer</strong>: Immediate assessment of the 10 Ajnas of Pulse (Harakat: Batee/Saree, Miqdar: Azeem/Saghir, Qawam: Layyin/Sulb), Tongue mucosal coating (Balghami/Safrawi/Sawdawi), and Qaroora urine density.
          3. <strong>Automated Ilaj bil-Zidd Equilibrium</strong>: Real-time evaluation of the net temperamental vector of candidate botanical formulations against the patient's pathological dystemperament.
          4. <strong>Bilingual Visual Slip Generation</strong>: Cryptographically commits the 21 CFR Part 11 SHA-256 seal and renders the patient-facing slip with morning, noon, and night visual glyphs and dietary Parhez, dispatched directly to WhatsApp.
        </div>
      </div>
    </div>

  </main>

  <!-- Interactive Reader JavaScript -->
  <script>
    // 1. Reading Progress Bar
    window.addEventListener('scroll', () => {
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrolled = (window.scrollY / docHeight) * 100;
      document.getElementById('progress-bar').style.width = scrolled + '%';
    });

    // 2. Theme Switching
    function setBookTheme(themeName) {
      document.documentElement.className = themeName;
      localStorage.setItem('zayvora_book_theme', themeName);
    }
    const savedTheme = localStorage.getItem('zayvora_book_theme');
    if (savedTheme) { document.documentElement.className = savedTheme; }

    // 3. Dynamic Font Resizing
    let currentFontSize = 16.5;
    function adjustFontSize(delta) {
      currentFontSize = Math.min(Math.max(currentFontSize + delta, 13), 22);
      document.documentElement.style.setProperty('--base-font-size', currentFontSize + 'px');
    }

    // 4. Drawer Toggle
    function toggleTocDrawer() {
      document.getElementById('toc-drawer').classList.toggle('open');
    }

    // 5. In-Book Search Filter
    function filterBookContent() {
      const q = document.getElementById('bookSearch').value.toLowerCase().trim();
      const chapters = document.querySelectorAll('.chapter-card');
      if (!q) {
        chapters.forEach(c => c.style.display = 'block');
        return;
      }
      chapters.forEach(c => {
        const text = c.innerText.toLowerCase();
        if (text.includes(q)) {
          c.style.display = 'block';
        } else {
          c.style.display = 'none';
        }
      });
    }

    // 6. Print PDF Preparation (Forces high-contrast Ivory layout for crystal-clear PDF)
    function prepareAndPrintBook() {
      const currentTheme = document.documentElement.className;
      document.documentElement.className = 'theme-ivory';
      setTimeout(() => {
        window.print();
        setTimeout(() => {
          document.documentElement.className = currentTheme;
        }, 1200);
      }, 50);
    }
  </script>

</body>
</html>
"""

    out_html = os.path.join(BASE_DIR, "docs", "THE_ZAYVORA_DOCTRINE_MASTER_BOOK.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Generated Modern Hardcover eBook: {out_html} ({os.path.getsize(out_html)} bytes)")
    return out_html

def main():
    print("=" * 80)
    print(" ZAYVORA HEALTH OS — MASTER BOOK COMPILATION (PUBLICATION EDITION)")
    print("=" * 80)
    md_file = generate_markdown_book()
    html_file = generate_html_ebook()
    print("=" * 80)
    print(" COMPILATION COMPLETE: Publication-grade Markdown and eBook are ready!")
    print(f"  - Markdown: file://{md_file}")
    print(f"  - Modern Interactive eBook: file://{html_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()
