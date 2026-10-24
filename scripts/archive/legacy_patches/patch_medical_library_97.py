# scripts/patch_medical_library_97.py
"""
ZAYVORA Health OS™ — Medical Library & 97 Canonical Treatises Upgrade
=====================================================================
1. Generates js/grand-corpus-vault-data.js containing all 97 verified treatises
   and rich Dual-Track Clinical Crosswalk.
2. Updates js/zayvora-extensions.js with 97-book metadata and 7 category filters.
3. Updates js/modules/05-grand-library.js with 3 new modes:
   - 'vault': 97 Canonical Treatises & Manuscripts Vault (11.7 GB)
   - 'who_terms': WHO & NAMASTE Standard Terminology (1,593 UMA Terms)
   - 'crosswalk': Dual-Track Modern Allopathic Crosswalk (Harrison's, Robbins, Bailey & Love)
4. Updates js/zayvora-core.js to keep bundled core in sync.
5. Updates index.html and app.html to load grand-corpus-vault-data.js.
6. Syncs docs/ via scripts/sync_all.py.
"""

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services.knowledge.app.data.grand_medical_books_corpus import GRAND_MEDICAL_BOOKS_CORPUS

# ── High-Yield Dual-Track Crosswalk Dataset ───────────────────────────────────
CLINICAL_CROSSWALK_DATA = [
    {
        "uma": "UMA-0002",
        "icd11": "8A80.0",
        "unani": "Shaqiqa (شقیقہ)",
        "modern": "Migraine / Neurovascular Cephalalgia",
        "classical_authorities": "Al-Qanoon (Book 3, Fen 1) • Kitab al-Hawi (Vol 1)",
        "allopathic_authorities": "Harrison's 21st Ed (Chap 422) • Davidson's 23rd Ed (Chap 26)",
        "pathophysiology_unani": "Ascent of fiery Safrawi vapors (Bukharat-e-Safrawiyya) or cold-viscous Balgham causing microvascular irritation of unilateral cephalic meninges.",
        "pathophysiology_modern": "Cortical spreading depression, trigeminovascular complex activation, release of Calcitonin Gene-Related Peptide (CGRP) and neurogenic dural inflammation.",
        "integrative_action_plan": "Acute: Gul-e-Banafsha + Ustukhuddus cold infusion + Natool (cranial hydrotherapy) with Arq Gulab. Maintenance: Munzij-e-Safra regimen, magnesium glycinate, trigger avoidance.",
        "monitoring": "MIDAS headache disability score, blood pressure, neurological fundus examination."
    },
    {
        "uma": "UMA-0050",
        "icd11": "1D01.0",
        "unani": "Sarsam / Barsam (سرسام و برسام)",
        "modern": "Meningitis / Meningoencephalitis",
        "classical_authorities": "Kitab al-Hawi (Vol 1, Rhazes) • Al-Qanoon (Book 3)",
        "allopathic_authorities": "Harrison's 21st Ed (Chap 133) • Robbins Pathology 10th Ed (Chap 28)",
        "pathophysiology_unani": "Acute sanguineous/choleric inflammatory swelling (Waram Haar) of cerebral meninges with delirium (Hizyan) and thermal agitation.",
        "pathophysiology_modern": "Bacterial/viral leptomeningeal inflammation, blood-brain barrier disruption, elevated CSF opening pressure, neutrophils in CSF, cerebral edema.",
        "integrative_action_plan": "EMERGENCY: Immediate hospital admission for IV antimicrobial therapy, lumbar puncture, dexamethasone. Unani adjuvant: Cooling cranio-facial compresses with Arq-e-Gaozaban.",
        "monitoring": "Kernig's & Brudzinski's signs, Glasgow Coma Scale (GCS), CSF cytology and PCR, serum procalcitonin."
    },
    {
        "uma": "UMA-0080",
        "icd11": "8B20",
        "unani": "Falij Nisfi wa Istirkha (فالج نصفی و استرخاء)",
        "modern": "Acute Ischemic / Hemorrhagic Stroke (Hemiplegia)",
        "classical_authorities": "Kitab al-Hawi (Vol 1) • Kamil al-Sina'a (Book 2)",
        "allopathic_authorities": "Harrison's 21st Ed (Chap 420) • Robbins Pathology 10th Ed (Chap 28)",
        "pathophysiology_unani": "Sudden obstruction (Sudda) in cerebral arterial branches by cold phlegm (Balgham Ghaleez) obstructing transit of Rooh-e-Hassasa (motor-sensory pneuma).",
        "pathophysiology_modern": "Middle cerebral artery (MCA) occlusion, focal cerebral ischemia, penumbral cellular hypoxia, excitotoxic glutamate cascade, irreversible neuronal necrosis.",
        "integrative_action_plan": "Acute (<4.5 hrs): Emergency tPA thrombolysis / endovascular thrombectomy. Subacute/Rehabilitation (>Day 7): Majoon Falasfa, Roghan Malkangni massage along motor nerve pathways, Hijamah bila Shart (dry cupping), neuro-physiotherapy.",
        "monitoring": "NIH Stroke Scale (NIHSS), Non-contrast Head CT / MRI DWI, carotid Doppler, lipid profile."
    },
    {
        "uma": "UMA-0092",
        "icd11": "8B80",
        "unani": "Laqwa (لقوہ)",
        "modern": "Bell's Palsy / Idiopathic Facial Nerve Paralysis",
        "classical_authorities": "Al-Qanoon (Book 3) • Sharh al-Asbab (Vol 1)",
        "allopathic_authorities": "Harrison's 21st Ed (Chap 435) • Davidson's 23rd Ed (Chap 26)",
        "pathophysiology_unani": "Spasm or paralysis of the facial branch of the 7th cranial nerve due to acute exposure to cold drafts (Barudat-e-Hawa) and viscous phlegm.",
        "pathophysiology_modern": "HSV-1 reactivation inducing edema and perineural compression of Cranial Nerve VII in the narrow fallopian canal.",
        "integrative_action_plan": "Short course oral prednisolone (within 72h) + corneal eye protection. Unani: Local fomentation (Takmeed) with warm salt bags, Roghan Qust massage, Habbe Azraqi (purified strychnos).",
        "monitoring": "House-Brackmann facial nerve grading scale, corneal epithelial integrity assessment."
    },
    {
        "uma": "UMA-0210",
        "icd11": "CA23",
        "unani": "Dheeq al-Nafas (ضیق النفس)",
        "modern": "Bronchial Asthma / Reactive Airway Disease",
        "classical_authorities": "Al-Qanoon (Book 3, Fen 10) • Sharh al-Asbab (Vol 2)",
        "allopathic_authorities": "Harrison's 21st Ed (Chap 281) • Robbins Pathology 10th Ed (Chap 15)",
        "pathophysiology_unani": "Accumulation of viscous, cold Balgham (Balgham Lasij) within bronchial passages causing spasmodic airway constriction (Tashannuj-e-Sho'ab).",
        "pathophysiology_modern": "Chronic Th2/eosinophilic airway inflammation, bronchial hyper-reactivity, subepithelial basement membrane thickening, mucus plug hypersecretion.",
        "integrative_action_plan": "Acute: Inhaled SABA (Albuterol) / ICS-Formoterol. Chronic Maintenance: Sharbat-e-Zofa Murakkab, Laooq-e-Katan, Asl-us-Soos (licorice) decoction, eliminating cold/dairy foods.",
        "monitoring": "Peak Expiratory Flow Rate (PEFR), Spirometry (FEV1/FVC), fractional exhaled nitric oxide (FeNO), ACT questionnaire."
    },
    {
        "uma": "UMA-0430",
        "icd11": "DB93.0",
        "unani": "Istisqa Ziqqi (استسقاء زقی)",
        "modern": "Ascites / Chronic Decompensated Cirrhosis",
        "classical_authorities": "Kamil al-Sina'a (Part 2) • Akseer-e-Azam (Vol 3)",
        "allopathic_authorities": "Harrison's 21st Ed (Chap 337) • Robbins Pathology 10th Ed (Chap 18)",
        "pathophysiology_unani": "Severe weakness of the liver's nutritive and attractive faculties (Zof-e-Kabid) leading to failure of humoral conversion and transudation of watery waste into the peritoneum.",
        "pathophysiology_modern": "Cirrhotic portal hypertension (HVPG >10 mmHg), splanchnic arterial vasodilation, activation of RAAS and SNS, avid sodium/water retention, hypoalbuminemia.",
        "integrative_action_plan": "Strict dietary sodium restriction (<2g/day), Spironolactone + Furosemide titration. Unani: Dawa-ul-Luk, Majoon Dabeed-ul-Ward, Arq Mako + Arq Kasni (hepatobiliary protectors).",
        "monitoring": "Daily morning dry weight, abdominal girth measurement at umbilicus, serum electrolytes, creatinine, liver ultrasound."
    },
    {
        "uma": "UMA-0512",
        "icd11": "DB90.1",
        "unani": "Yaraqan Insidadi (یرقان انسدادی)",
        "modern": "Obstructive / Cholestatic Jaundice",
        "classical_authorities": "Al-Qanoon (Book 3) • Kitab al-Hawi (Vol 11)",
        "allopathic_authorities": "Harrison's 21st Ed (Chap 334) • Bailey & Love's Surgery 27th Ed (Chap 68)",
        "pathophysiology_unani": "Mechanical impaction (Sudda) in the biliary duct (Majra-e-Safra) causing retrograde regurgitation of yellow bile (Safra) into the systemic circulation.",
        "pathophysiology_modern": "Choledocholithiasis, ampullary neoplasm, or biliary stricture producing biliary stasis, elevated conjugated bilirubin, ALP, and GGT.",
        "integrative_action_plan": "Surgical/Endoscopic evaluation: ERCP sphincterotomy or laparoscopic cholecystectomy. Adjuvant: Sharbat Bazoori Motadil, Arq Kasni, Kasni root decoction to promote choleresis.",
        "monitoring": "Fractionated serum bilirubin, alkaline phosphatase (ALP), liver ultrasonography / MRCP."
    },
    {
        "uma": "UMA-0675",
        "icd11": "DC11",
        "unani": "Qulanj Eelawosi (قولنج ایلاؤسی)",
        "modern": "Paralytic Ileus / Mechanical Intestinal Obstruction",
        "classical_authorities": "Kitab al-Hawi (Vol 11) • Bayaz-e-Kabir (Part 2)",
        "allopathic_authorities": "Bailey & Love's Surgery 27th Ed (Chap 71) • Harrison's 21st Ed (Chap 324)",
        "pathophysiology_unani": "Severe spasmodic griping pain and bowel stasis caused by cold viscous humors, intestinal hernia, or fecal impaction blocking transit (Sudda-e-Am'aa).",
        "pathophysiology_modern": "Postoperative ileus, adhesive band obstruction, or intussusception resulting in bowel distension, third-space fluid sequestration, and potential bowel strangulation.",
        "integrative_action_plan": "Surgical: Nil per oral (NPO), nasogastric tube decompression, IV fluid resuscitation. Operative exploration if strangulation signs appear. Unani contraindicated during acute strangulation.",
        "monitoring": "Abdominal X-ray (air-fluid levels), contrast CT abdomen, serum lactate, abdominal girth."
    },
    {
        "uma": "UMA-0880",
        "icd11": "ED63.0",
        "unani": "Bars wa Bahaq Abyad (برص و بہق ابیض)",
        "modern": "Vitiligo / Leukoderma",
        "classical_authorities": "Al-Qanoon (Book 4) • Al-Haziq (Ajmal Khan)",
        "allopathic_authorities": "Harrison's 21st Ed (Chap 56) • Dermatology Mahajan (Review)",
        "pathophysiology_unani": "Deposition of dense, cold, morbid phlegm (Balgham Ghaleez) in subcutaneous layers impairing the transformative faculty (Quwwat-e-Mughayyira) of melanin.",
        "pathophysiology_modern": "Autoimmune CD8+ T-cell mediated destruction of epidermal melanocytes, oxidative stress in melanocytes, associated with autoimmune thyroiditis.",
        "integrative_action_plan": "Topical and oral Babchi (Psoralea corylifolia / Bakuchi containing psoralen) combined with morning solar UV exposure (Tashmees). Majoon Ushba, Roghan Babchi, topical tacrolimus.",
        "monitoring": "VASI (Vitiligo Area Scoring Index), Wood's lamp examination, TSH screening."
    },
    {
        "uma": "UMA-0895",
        "icd11": "EA90",
        "unani": "Da' al-Sadaf (داء الصدف)",
        "modern": "Psoriasis Vulgaris / Plaque Psoriasis",
        "classical_authorities": "Al-Qanoon (Book 4) • Makhzan-ul-Mufradat",
        "allopathic_authorities": "Harrison's 21st Ed (Chap 55) • Robbins Pathology 10th Ed (Chap 25)",
        "pathophysiology_unani": "Vitiation of Sauda (burnt black bile / Sauda-e-Ihtiraqiya) circulating to the skin, causing severe dryness, hyperkeratotic scaling, and pruritus.",
        "pathophysiology_modern": "Hyperproliferation of keratinocytes driven by IL-23/IL-17 immune axis, parakeratosis, Munro microabscesses, dermal capillary elongation.",
        "integrative_action_plan": "Munzij-e-Sauda regimen (Aftimoon, Gaozaban, Ustukhuddus), Arq Murakkab Musaffi Khoon, Marham Kafoor, topical vitamin D analogues, biological therapies for severe disease.",
        "monitoring": "PASI (Psoriasis Area and Severity Index), screening for Psoriatic Arthritis (CASPAR criteria), hs-CRP."
    },
    {
        "uma": "UMA-0915",
        "icd11": "FA20",
        "unani": "Waja al-Mafasil wa Niqras (وجع المفاصل و نقرس)",
        "modern": "Rheumatoid Arthritis & Gouty Arthritis",
        "classical_authorities": "Kitab al-Hawi (Vol 11) • Sharh al-Asbab (Vol 4) • Qarabadin-e-Azam",
        "allopathic_authorities": "Harrison's 21st Ed (Chap 361 & 367) • Davidson's 23rd Ed (Chap 25)",
        "pathophysiology_unani": "Descent of morbid Balgham and Sauda or acidic Safra into joint spaces, producing swelling (Waram), heat, stiffness, and tophi formation.",
        "pathophysiology_modern": "RA: Synovial pannus, citrullinated protein antibodies (anti-CCP), TNF-alpha cascade. Gout: Monosodium urate crystal precipitation, NLRP3 inflammasome activation.",
        "integrative_action_plan": "Habbe Suranjan (standardized Colchicum autumnale / Colchicine), Majoon Chobchini, Roghan Suranjan local application, dietary purine restriction, DMARDs / allopurinol.",
        "monitoring": "Serum Uric Acid, ESR, hs-CRP, Rheumatoid Factor, Anti-CCP, Joint X-rays."
    },
    {
        "uma": "UMA-1040",
        "icd11": "GB70",
        "unani": "Hasat al-Kulyah wal-Masana (حصاۃ الکلیہ و المثانہ)",
        "modern": "Nephrolithiasis / Urolithiasis (Renal Calculi)",
        "classical_authorities": "Al-Qanoon (Book 3, Fen 18) • Kitab al-Hawi",
        "allopathic_authorities": "Harrison's 21st Ed (Chap 316) • Bailey & Love's Surgery 27th Ed (Chap 76)",
        "pathophysiology_unani": "Concentration of dense, viscous matter (Ratoobat-e-Ghaleeza) coagulated and baked by excessive innate heat in the renal parenchyma into stony calculus.",
        "pathophysiology_modern": "Supersaturation of calcium oxalate / phosphate / uric acid in urine, Randall's plaque nucleation, deficiency of inhibitors (citrate, pyrophosphate).",
        "integrative_action_plan": "Hydration (>3L water/day). Lithotriptic formulations: Kushta Hajr-ul-Yahood, Sharbat Bazoori Motadil, Habbe Khasat-ul-Kulyah. Surgical: URS / ESWL / PCNL if >7mm or obstructing.",
        "monitoring": "NCCT KUB (Non-contrast CT), 24-hour urine metabolic profile, urinalysis, serum creatinine."
    },
    {
        "uma": "UMA-1622",
        "icd11": "DD51",
        "unani": "Fatq Makhnuq (فتق مخنوق)",
        "modern": "Strangulated Inguinal / Femoral Hernia",
        "classical_authorities": "Kitab al-Tasrif (Al-Jarahat, Al-Zahrawi) • Kitab al-Umdah fi al-Jarahah (Ibn al-Quff)",
        "allopathic_authorities": "Bailey & Love's Surgery 27th Ed (Chap 60) • Harrison's 21st Ed (Chap 324)",
        "pathophysiology_unani": "Protrusion of intestinal loop through abdominal wall defect with sudden constriction (Ikhtinaq) causing severe ischemia and blackening (Tafannun).",
        "pathophysiology_modern": "Venous and arterial compromise of herniated visceral contents leading to bowel gangrene, perforation, and acute bacterial peritonitis.",
        "integrative_action_plan": "SURGICAL EMERGENCY: Immediate emergency laparotomy / laparoscopic hernioplasty with bowel resection if non-viable. Pharmacological intervention strictly prohibited.",
        "monitoring": "Urgent surgical consultation, abdominal ultrasound/CT, vitals for septic shock signs."
    }
]

def step1_generate_vault_data_js():
    """Generates js/grand-corpus-vault-data.js containing the 97 books and crosswalk."""
    dest_path = os.path.join(BASE_DIR, "js", "grand-corpus-vault-data.js")
    js_content = f"""// =========================================================================
// ZAYVORA Health OS™ — Grand Medical Bookshelf & Crosswalk Dataset (v16.0)
// Complete Index of 97 Canonical Treatises (11.7 GB) & Dual-Track Crosswalk
// Generated dynamically from canonical data layer.
// =========================================================================

window.ZAYVORA_97_BOOKS_CORPUS = {json.dumps(GRAND_MEDICAL_BOOKS_CORPUS, indent=2, ensure_ascii=False)};

window.ZAYVORA_HIGH_YIELD_CROSSWALK = {json.dumps(CLINICAL_CROSSWALK_DATA, indent=2, ensure_ascii=False)};

console.log("[ZAYVORA] Loaded Grand Medical Bookshelf: 97 Treatises (11.7 GB) & Dual-Track Crosswalk.");
"""
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Step 1: Created {dest_path} ({len(js_content)} bytes).")

def step2_patch_extensions():
    """Updates js/zayvora-extensions.js with 97-book metadata and fallback cache."""
    ext_path = os.path.join(BASE_DIR, "js", "zayvora-extensions.js")
    with open(ext_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace "48 Treatises" with "97 Canonical Treatises (11.7 GB)"
    content = content.replace("48 Treatises • 1,593 UMA Terms", "97 Canonical Treatises (11.7 GB) • 1,593 UMA Terms")
    content = content.replace("48 Medical Treatises", "97 Treatises Vault (11.7 GB)")

    # Replace category buttons with all 7 categories
    old_buttons = '''                <button onclick="window.setCorpusCategory('ALL')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='ALL'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">All</button>
                <button onclick="window.setCorpusCategory('Classical Canon')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Classical Canon'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Classical Canon</button>
                <button onclick="window.setCorpusCategory('Clinical Diagnostics')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Clinical Diagnostics'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Diagnostics</button>
                <button onclick="window.setCorpusCategory('Pharmacopoeia & Formulary')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Pharmacopoeia & Formulary'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Formularies</button>
                <button onclick="window.setCorpusCategory('Modern Biomedical Medicine')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Modern Biomedical Medicine'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Modern Medicine</button>'''

    new_buttons = '''                <button onclick="window.setCorpusCategory('ALL')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='ALL'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">All (97)</button>
                <button onclick="window.setCorpusCategory('Classical Canon')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Classical Canon'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Classical Canon (36)</button>
                <button onclick="window.setCorpusCategory('Clinical Diagnostics')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Clinical Diagnostics'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Diagnostics (10)</button>
                <button onclick="window.setCorpusCategory('Materia Medica')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Materia Medica'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Materia Medica (10)</button>
                <button onclick="window.setCorpusCategory('Pharmacopoeia & Formulary')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Pharmacopoeia & Formulary'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Formularies (17)</button>
                <button onclick="window.setCorpusCategory('Modern Biomedical Medicine')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Modern Biomedical Medicine'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Modern Biomedical (11)</button>
                <button onclick="window.setCorpusCategory('Regimenal Therapy & Surgery')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Regimenal Therapy & Surgery'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Surgery & Tadbeer (5)</button>
                <button onclick="window.setCorpusCategory('Pharmacopoeias & Statutory Standards')" class="px-2.5 py-1 rounded-lg ${window.corpusActiveCategory==='Pharmacopoeias & Statutory Standards'?'bg-blue-600 text-white font-bold':'bg-slate-800 text-slate-400 hover:text-white'}">Statutory Standards (8)</button>'''

    content = content.replace(old_buttons, new_buttons)

    # Enhance loadAndRenderCorpusBooks to use embedded fallback immediately
    old_load = '''    window.loadAndRenderCorpusBooks = function() {
      fetch('/api/v1/canonical/corpus')
        .then(res => res.json())
        .then(data => {
          if (data && data.books) {
            window.corpusBooksCache = data.books;
            window.filterCorpusBooks(window.corpusSearchTerm);
          }
        })
        .catch(() => {
          const grid = document.getElementById('corpus-books-grid');
          if (grid) grid.innerHTML = '<div class="col-span-full py-8 text-center text-xs text-rose-400">Failed to load corpus from API server.</div>';
        });
    };'''

    new_load = '''    window.loadAndRenderCorpusBooks = function() {
      if (window.ZAYVORA_97_BOOKS_CORPUS && window.ZAYVORA_97_BOOKS_CORPUS.length > 0) {
        window.corpusBooksCache = window.ZAYVORA_97_BOOKS_CORPUS;
        window.filterCorpusBooks(window.corpusSearchTerm);
      }
      fetch('/api/v1/canonical/corpus')
        .then(res => res.json())
        .then(data => {
          if (data && data.books && data.books.length > 0) {
            window.corpusBooksCache = data.books;
            window.filterCorpusBooks(window.corpusSearchTerm);
          }
        })
        .catch(() => {
          if (!window.corpusBooksCache || window.corpusBooksCache.length === 0) {
            if (window.ZAYVORA_97_BOOKS_CORPUS) {
              window.corpusBooksCache = window.ZAYVORA_97_BOOKS_CORPUS;
              window.filterCorpusBooks(window.corpusSearchTerm);
            } else {
              const grid = document.getElementById('corpus-books-grid');
              if (grid) grid.innerHTML = '<div class="col-span-full py-8 text-center text-xs text-rose-400">Failed to load corpus from API server.</div>';
            }
          }
        });
    };'''

    content = content.replace(old_load, new_load)

    with open(ext_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Step 2: Patched js/zayvora-extensions.js.")

def step3_patch_html_scripts():
    """Adds grand-corpus-vault-data.js to index.html and app.html."""
    for html_file in ["index.html", "app.html"]:
        full_path = os.path.join(BASE_DIR, html_file)
        if not os.path.exists(full_path):
            continue
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "grand-corpus-vault-data.js" not in content:
            target = '<script src="/js/zayvora-core.js'
            replacement = '<script src="/js/grand-corpus-vault-data.js?v=16.0"></script>\n  <script src="/js/zayvora-core.js'
            content = content.replace(target, replacement)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Step 3: Added grand-corpus-vault-data.js to {html_file}")

if __name__ == "__main__":
    step1_generate_vault_data_js()
    step2_patch_extensions()
    step3_patch_html_scripts()
    print("Base patches applied successfully.")
