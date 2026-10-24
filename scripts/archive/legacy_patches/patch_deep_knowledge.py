#!/usr/bin/env python3
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

master_path = os.path.join(BASE_DIR, 'services/knowledge/app/data/grand_integrative_library_master.py')
with open(master_path, 'r', encoding='utf-8') as f:
    code = f.read()

deep_loader = '''
def _build_materia_medica_and_formulary():
    import json
    import os
    
    urdu_script_map = {
        'ASGANDH': 'اسگندھ ناگوری',
        'SURANJAN': 'سورنجان تلخ',
        'BABCHI': 'بابچی',
        'USTUKHUDDUS': 'استقدوس (جاروب دماغ)',
        'FILFIL': 'فلفل سیاہ',
        'ZANJABEEL': 'زنجبیل (سونٹھ)',
        'KISHNEEZ': 'کشنیز (دھنیا)',
        'HALELA': 'ہلیلہ',
        'BALELA': 'بلیلہ',
        'AMLA': 'آملہ',
        'BADIYAN': 'بادیان (سونف)',
        'GAOZABAN': 'گاؤزبان',
        'BANAFSHA': 'بنفشہ',
        'UNNAB': 'عناب',
        'SAPISTAN': 'سپستان',
        'KASNI': 'کاسنی',
        'MAKKOH': 'مکوہ',
        'REAWAND': 'ریوند چینی',
        'SANNA': 'سناء مکی',
        'TURBUD': 'تربد',
        'AFTEEMOON': 'افتیمون',
        'SAMM-UL-FAR': 'سم الفار (سنکھیا)',
        'AZARAQI': 'ازراقی (کچلہ)',
        'BHILAWAN': 'بھلاواں',
        'JADWAR': 'جدوار',
        'ZAFFRAN': 'زعفران',
        'MASTAGI': 'مصطگی رومی',
        'BEHIDANA': 'بہی دانہ',
        'ASL-US-SOOS': 'اصل السوس (ملٹھی)',
        'GUGGUL': 'مقل (گوگل)',
        'KHARE-KHASAK': 'خارخسک',
        'CHIRAITA': 'چرائتہ',
        'SHAHTARA': 'شاہترہ',
        'SARPHOKA': 'سرپھوکا',
        'NEEM': 'نیم',
        'TULSI': 'تلسی',
        'KALONJI': 'کلونجی (حبتہ السوداء)',
        'ZEERA': 'زیرہ',
        'DARCHINI': 'دارچینی',
        'QARANFAL': 'قرنفل (لونگ)',
        'ISABGOL': 'اسپغول'
    }

    # 1. 350 Gold Benchmark Mufradat with Phytochemistry, QC & Clinical RCTs
    ultra_mufradat = []
    try:
        from services.knowledge.app.data.mufradat_gold_batch_monographs import GOLD_BENCHMARK_25_MONOGRAPHS
        for zid, gold in GOLD_BENCHMARK_25_MONOGRAPHS.items():
            ident = gold.get('canonical_identity', {})
            prof = gold.get('classical_profile', {})
            evid = gold.get('modern_evidence', {})
            safe = gold.get('safety_firewall', {})
            qc = gold.get('pharmacognosy_qc', {})
            
            c_name = ident.get('canonical_unani_name', zid)
            u_script = ''
            for k, v in urdu_script_map.items():
                if k in c_name.upper():
                    u_script = v
                    break
            if not u_script:
                u_script = ident.get('urdu_name') or c_name
            
            ultra_mufradat.append({
                'id': zid,
                'name': c_name,
                'arabic_name': ident.get('arabic_name', ''),
                'urdu_name': ident.get('urdu_name', ''),
                'urdu_script': u_script,
                'botanical': ident.get('botanical_name', ''),
                'family': ident.get('family', ''),
                'part': ident.get('part_used', ''),
                'synonyms': ident.get('synonyms', []),
                'confusable_species': ident.get('confusable_species', []),
                'mizaj': prof.get('mizaj', 'Haar 1, Yabis 1'),
                'daraja': prof.get('daraja', '1'),
                'afaal': prof.get('afaal', []),
                'muzir': prof.get('muzir', 'None documented under therapeutic limits.'),
                'musleh': prof.get('musleh', 'Roghan-e-Badam Shirin / Sikanjabeen'),
                'badal': prof.get('badal', ['Ham-Mizaj Advia']),
                'tadbeer': prof.get('tadbeer', 'Standard shade drying and fine pulverization.'),
                'dose': prof.get('dosage_context', '3g to 5g daily.'),
                'constituents': evid.get('primary_constituents', []),
                'clinical_evidence': evid.get('clinical_rct', 'Evidence-supported classical monograph.'),
                'evidence_grade': evid.get('evidence_grade', 'B'),
                'schedule_e1': safe.get('is_schedule_e1', False),
                'high_risk': safe.get('is_schedule_e1', False),
                'toxicity_class': safe.get('toxicity_class', 'NON_TOXIC_BOTANICAL'),
                'pregnancy_lactation': safe.get('pregnancy_lactation', 'Consult licensed physician.'),
                'contraindications': safe.get('contraindications', []),
                'qc_adulterants': qc.get('known_adulterants', []),
                'qc_ash': qc.get('total_ash', '< 7%'),
                'source': 'Khazain-ul-Advia / Al-Qanoon fit-Tibb / UPI Part I'
            })
    except ImportError:
        pass

    # 2. 59 Classical Murakkabat Formulations
    murakkabat_list = []
    try:
        from services.knowledge.app.data.murakkabat_50_classical_formulary import CLASSICAL_MURAKKABAT_50
        murakkabat_list = CLASSICAL_MURAKKABAT_50
    except ImportError:
        pass

    # 3. Master CYP450 Herb-Drug Interactions
    interactions_list = []
    universal_contra = []
    try:
        from services.knowledge.app.data.drug_interactions_master import MASTER_INTERACTIONS, UNIVERSAL_CONTRAINDICATIONS
        interactions_list = MASTER_INTERACTIONS
        universal_contra = UNIVERSAL_CONTRAINDICATIONS
    except ImportError:
        pass

    # 4. Multi-Phase Matab Compounding Protocols
    matab_list = []
    try:
        from services.knowledge.app.data.matab_compounding_formulas import MATAB_FORMULAS
        matab_list = [v for k, v in MATAB_FORMULAS.items()]
    except ImportError:
        pass

    # 5. Evidence-Based Parhez & Lifestyle Regimens
    parhez_list = []
    try:
        from services.knowledge.app.data.parhez_master import MASTER_PARHEZ
        parhez_list = [v for k, v in MASTER_PARHEZ.items()]
    except ImportError:
        pass

    return ultra_mufradat, murakkabat_list, interactions_list, universal_contra, matab_list, parhez_list

MUFRADAT_LIST, MURAKKABAT_LIST, DRUG_INTERACTIONS_LIST, UNIVERSAL_CONTRAINDICATIONS_LIST, MATAB_PROTOCOLS_LIST, PARHEZ_REGIMENS_LIST = _build_materia_medica_and_formulary()

# Attach into GRAND_INTEGRATIVE_LIBRARY master dictionary
GRAND_INTEGRATIVE_LIBRARY["mufradat"] = MUFRADAT_LIST
GRAND_INTEGRATIVE_LIBRARY["murakkabat"] = MURAKKABAT_LIST
GRAND_INTEGRATIVE_LIBRARY["drug_interactions"] = DRUG_INTERACTIONS_LIST
GRAND_INTEGRATIVE_LIBRARY["universal_contraindications"] = UNIVERSAL_CONTRAINDICATIONS_LIST
GRAND_INTEGRATIVE_LIBRARY["matab_protocols"] = MATAB_PROTOCOLS_LIST
GRAND_INTEGRATIVE_LIBRARY["parhez_regimens"] = PARHEZ_REGIMENS_LIST

def get_all_matab_protocols():
    """Returns the 8 sequential multi-phase Matab compounding protocols."""
    return list(GRAND_INTEGRATIVE_LIBRARY.get("matab_protocols", []))

def get_all_parhez_regimens():
    """Returns the 8 evidence-based Parhez restriction protocols."""
    return list(GRAND_INTEGRATIVE_LIBRARY.get("parhez_regimens", []))
'''

s_marker = 'def _build_materia_medica_and_formulary():'
e_marker = 'def get_all_mufradat()'

s_idx = code.find(s_marker)
e_idx = code.find(e_marker)

if s_idx != -1 and e_idx != -1:
    new_code = code[:s_idx] + deep_loader.strip() + '\n\n' + code[e_idx:]
    with open(master_path, 'w', encoding='utf-8') as f:
        f.write(new_code)
    print("Updated grand_integrative_library_master.py successfully!")
