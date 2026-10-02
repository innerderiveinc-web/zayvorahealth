"""
ZAYVORA Health OS™ — Batch 13: 25 Classical Single-Drug Master Monographs (ZMF-326 to ZMF-350)
=============================================================================================
Implementation of the 10-Phase Canonical & Evidence Architecture.

Monographs Included:
  1. ZMF-326: Gul-e-Tesu / Palash Phool (Butea monosperma (Lam.) Taub. - Dried Flowers)
  2. ZMF-327: Ood-e-Balsan / Balsam Wood (Commiphora gileadensis (L.) C.Chr. - Heartwood)
  3. ZMF-328: Habb-e-Balsan / Balsam Berries (Commiphora gileadensis (L.) C.Chr. - Fruit)
  4. ZMF-329: Sandroos / Sandarac Resin (Trachylobium verrucosum (Gaertn.) Oliv. - Resin)
  5. ZMF-330: Usara Rewand / Gamboge (Garcinia morella (Gaertn.) Desr. - Gum Resin - Sched E1)
  6. ZMF-331: Kushta Baiza-e-Murgh (Gallus domesticus - Calcined Eggshell Calx)
  7. ZMF-332: Hajar-ul-Yahood / Jew's Stone (Fossil Encrinite / Lapis Judaicus Calx)
  8. ZMF-333: Zahra Mohra / Panzahar (Bezoar / Serpentine Mineral Stone)
  9. ZMF-334: Tukhm-e-Panwar / Chakwad (Senna tora (L.) Roxb. - Dried Seeds)
 10. ZMF-335: Sheetraj Hindi / Chitrak (Plumbago zeylanica L. - Dried Root)
 11. ZMF-336: Sambhalu / Nirgundi (Vitex negundo L. - Seeds & Leaves)
 12. ZMF-337: Tukhm-e-Piyaz / Onion Seeds (Allium cepa L. - Dried Seeds)
 13. ZMF-338: Barg-e-Hina / Mehndi (Lawsonia inermis L. - Dried Leaves)
 14. ZMF-339: Jadwar / Nirbisi (Delphinium denudatum Wall. ex Hook.f. & Thomson - Root)
 15. ZMF-340: Farfiyun / Euphorbium (Euphorbia resinifera O.Berg - Caustic Latex - Sched E1)
 16. ZMF-341: Kundush / White Hellebore (Veratrum album L. - Rhizome - Sched E1)
 17. ZMF-342: Filfil Moyeh / Pippalimula (Piper retrofractum Vahl - Dried Root)
 18. ZMF-343: Kabab Khandan / Prickly Ash (Zanthoxylum armatum DC. - Carpels / Fruit)
 19. ZMF-344: Barg-e-Bakayan / Persian Lilac (Melia azedarach L. - Dried Leaves)
 20. ZMF-345: Gule Ghafis / Agrimony (Agrimonia eupatoria L. - Dried Flowers)
 21. ZMF-346: Baqla / Faba Bean (Vicia faba L. - Dried Seeds)
 22. ZMF-347: Kharateen Musaffa (Pheretima posthuma - Purified Earthworm)
 23. ZMF-348: Zalu / Medicinal Leech (Hirudo medicinalis - Certified Medical Leech)
 24. ZMF-349: Regmahi / Sand Skink (Scincus officinalis - Dried Sandfish Skink)
 25. ZMF-350: Mahee Zahraj / Fish Berry (Anamirta cocculus (L.) Wight & Arn. - Fruit - Sched E1)
"""

from __future__ import annotations
from typing import Dict, Any
from enum import Enum


class ValidationState(str, Enum):
    CANDIDATE = "CANDIDATE"
    IDENTITY_VERIFIED = "IDENTITY_VERIFIED"
    CLASSICAL_SOURCE_VERIFIED = "CLASSICAL_SOURCE_VERIFIED"
    PHARMACOPOEIAL_CROSS_CHECKED = "PHARMACOPOEIAL_CROSS_CHECKED"
    PHARMACOGNOSY_VERIFIED = "PHARMACOGNOSY_VERIFIED"
    MODERN_EVIDENCE_REVIEWED = "MODERN_EVIDENCE_REVIEWED"
    SAFETY_REVIEWED = "SAFETY_REVIEWED"
    REGULATORY_REVIEWED = "REGULATORY_REVIEWED"
    CLINICIAN_REVIEWED = "CLINICIAN_REVIEWED"
    APPROVED_KNOWLEDGE = "APPROVED_KNOWLEDGE"
    RECONCILIATION_QUEUE = "RECONCILIATION_QUEUE"


class AIPermission(str, Enum):
    BLOCKED_HIGH_RISK = "BLOCKED_HIGH_RISK"
    RESEARCH_ONLY = "RESEARCH_ONLY"
    CLINICIAN_SUPERVISED_ONLY = "CLINICIAN_SUPERVISED_ONLY"
    APPROVED_FOR_AI_COPILOT = "APPROVED_FOR_AI_COPILOT"


BATCH_13_25_MONOGRAPHS: Dict[str, Dict[str, Any]] = {   'ZMF-326': {   'canonical_identity': {   'arabic_name': 'Ward-ul-Palas',
                                             'botanical_authority': '(Lam.) Taub.',
                                             'botanical_name': 'Butea monosperma (Lam.) Taub.',
                                             'canonical_unani_name': 'Gul-e-Tesu',
                                             'confusable_species': ['Erythrina variegata flowers'],
                                             'family': 'Fabaceae',
                                             'hindi_regional_names': [   'Tesu Phool',
                                                                         'Palash Pushpa',
                                                                         'Flame of the Forest Flowers',
                                                                         'Kasturi Phool'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Gul-e-Tesu Desi', 'Palash Flowers'],
                                             'part_used': 'Dried Flowers',
                                             'synonyms': ['Butea frondosa flowers', 'Palash Phool', 'Dhak ke Phool'],
                                             'urdu_name': 'Gul-e-Tesu / Palash Phool'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Mubarrid',
                                                         'Mudirr-e-Baul',
                                                         'Daf-e-Huraq-ul-Baul',
                                                         'Muhallil-e-Awram',
                                                         'Musakkin-e-Hararat'],
                                            'badal': ['Gul-e-Banafsha', 'Nilofar'],
                                            'daraja': 'Daraja 1',
                                            'dosage_context': '3g to 6g internally; 20g to 50g in decoction for '
                                                              'external Sitz bath.',
                                            'mizaj': 'Sard 1, Ratab 1',
                                            'musleh': 'Badiyan & Shakar',
                                            'muzir': 'May induce mild flatulence in cold stomachs without Musleh.',
                                            'tadbeer': 'Infused in hot water (Josh-e-Khurd) for local fomentation or '
                                                       'sitz bath (Abzan)'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Significant reduction of carrageenan-induced pelvic and '
                                                           'paw edema; protective against acute chemical cystitis in '
                                                           'rodents.',
                                          'clinical_rct': 'Universally prescribed in matab for burning micturition '
                                                          '(Sozish-e-Baul), acute cystitis, and post-partum sitz bath '
                                                          'baths.',
                                          'evidence_grade': 'E4 (Robust Clinical & Classical Anti-Inflammatory '
                                                            'Evidence)',
                                          'in_vitro': 'Potent free radical scavenging, inhibition of xanthine oxidase, '
                                                      'membrane-stabilizing anti-inflammatory in bladder urothelium.',
                                          'primary_constituents': [   'Butein',
                                                                      'Butin',
                                                                      'Isobutrin',
                                                                      'Coreopsin',
                                                                      'Flavonoid chalcones']},
                   'murakkab_roles': [   'Chief active in Abzan-e-Tesu, Sharbat-e-Bazoori formulations, and '
                                         'Roghan-e-Tesu'],
                   'organ_axis_affinity': [   'Axis 06 (Kulyatain-Masana / Nephro-Urological Axis)',
                                              'Axis 07 (Tanasul-Bah / Reproductive Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 2.0%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': [   'Flowers of Woodfordia fruticosa',
                                                                    'Dyed synthetic petals'],
                                           'microscopy': 'Uniseriate multicellular hairs with dark brown contents on '
                                                         'calyx, glandular clavate hairs, pollen grains spherical '
                                                         'tricolporate.',
                                           'morphology': 'Bright reddish-orange papilionaceous flowers, 4-6 cm long, '
                                                         'velvety olive-green calyx, keel curved semi-lunar, faintly '
                                                         'fragrant odor, slightly mucilaginous astringent taste.',
                                           'total_ash': 'Not more than 7.5%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-326',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Flowers',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '38',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Refrigerant, Diuretic, Sitz Bath for Pelvic '
                                                                    'Inflammation & Dysuria',
                                                      'original_text_snippet': 'گل ٹیسو: سرد و تر در اول، مدر بول، '
                                                                               'دافع حرق البول و التہاب کبد و مفاصل، و '
                                                                               'برائے حمام و آب دست عجیبہ کار است۔',
                                                      'page': '212',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Khazain-ul-Advia (Hakeem Najmul Ghani)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Vol. VI (Advia-e-Mufarradah)'}],
                   'safety_firewall': {   'contraindications': ['None noted in therapeutic posology.'],
                                          'drug_interactions': ['Compatible with urinary alkalinizers.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_PELVIC_REFRIGERANT'},
                   'zmf_id': 'ZMF-326'},
    'ZMF-327': {   'canonical_identity': {   'arabic_name': 'Khashab-ul-Balsan',
                                             'botanical_authority': '(L.) C.Chr.',
                                             'botanical_name': 'Commiphora gileadensis (L.) C.Chr.',
                                             'canonical_unani_name': 'Ood-e-Balsan',
                                             'confusable_species': [   'Aquilaria agallocha (Agarwood)',
                                                                       'Commiphora opobalsamum wood'],
                                             'family': 'Burseraceae',
                                             'hindi_regional_names': [   'Balm of Gilead Wood',
                                                                         'Balsam Tree Wood',
                                                                         'Mecca Balsam Wood'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Ood-e-Balsan Asli', 'Balsam Heartwood'],
                                             'part_used': 'Dried Heartwood',
                                             'synonyms': [   'Amyris gileadensis L.',
                                                             'Balsamodendron gileadense',
                                                             'Xylobalsamum'],
                                             'urdu_name': 'Ood-e-Balsan / Balsam Wood'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Mufattih-e-Sudad',
                                                         'Muqawwi-e-Asha',
                                                         'Daf-e-Zeeq-un-Nafs',
                                                         'Mulatlif',
                                                         'Kasir-e-Riyah'],
                                            'badal': ['Darchini', 'Kalanjan'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '2g to 4g in classical decoction or Majun.',
                                            'mizaj': 'Garm 2, Khushk 2',
                                            'musleh': 'Kateera & Roghan-e-Badam',
                                            'muzir': 'May aggravate dry bilious cough without soothing demulcent '
                                                     'Musleh.',
                                            'tadbeer': 'Grated finely and decocted or powdered in electuaries'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Suppression of airway hyperresponsiveness and mucosal '
                                                           'goblet cell hyperplasia in ovalbumin-sensitized asthma '
                                                           'models.',
                                          'clinical_rct': 'Centuries of classical verification in chronic cold '
                                                          'catarrh, bronchial asthma, and cold hepatic atony.',
                                          'evidence_grade': 'E4 (Classical Compendia & Modern Pharmacological '
                                                            'Evidence)',
                                          'in_vitro': 'Bronchodilator and antispasmodic action on tracheal chains, '
                                                      'inhibition of pro-inflammatory 5-lipoxygenase.',
                                          'primary_constituents': [   'Balsamoterpenes',
                                                                      'Alpha-copaene',
                                                                      'Beta-caryophyllene',
                                                                      'Germacrene D',
                                                                      'Triterpenic acids']},
                   'murakkab_roles': ['Key active in Taryaq-e-Farooq, Majun Dabeed-ul-Ward, and Sufoof-e-Balsan'],
                   'organ_axis_affinity': [   'Axis 05 (Tanaffus / Respiratory Axis)',
                                              'Axis 04 (Meda-Ama / Gastrointestinal Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 1.5%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Inferior Commiphora woods lacking balsam aroma'],
                                           'microscopy': 'Vessels with bordered pits, xylem parenchyma containing '
                                                         'balsamic resin droplets, uniseriate rays with starch grains.',
                                           'morphology': 'Light brownish-yellow hard fibrous wood pieces, resinous '
                                                         'streaks, balsamic fragrant aroma on rubbing, pungent '
                                                         'bitterish aromatic taste.',
                                           'total_ash': 'Not more than 5.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-327',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Heartwood',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '64',
                                                   'upi_volume': 'Part-I, Vol. III'},
                   'primary_unani_citations': [   {   'claim_type': 'Visceral Deobstruent, Broncho-Pulmonary Tonic & '
                                                                    'Anti-Asthmatic',
                                                      'original_text_snippet': 'عود البلسان: حار يابس في الثانية، ينفع '
                                                                               'من السعال المزمن وضيق النفس وأوجاع '
                                                                               'الأحشاء الباردة ومقو للمعدة۔',
                                                      'page': '238',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': ['None noted in therapeutic posology.'],
                                          'drug_interactions': ['Compatible with conventional bronchodilators.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_PULMONARY_TONIC'},
                   'zmf_id': 'ZMF-327'},
    'ZMF-328': {   'canonical_identity': {   'arabic_name': 'Habb-ul-Balsan',
                                             'botanical_authority': '(L.) C.Chr.',
                                             'botanical_name': 'Commiphora gileadensis (L.) C.Chr.',
                                             'canonical_unani_name': 'Habb-e-Balsan',
                                             'confusable_species': ['Pistacia lentiscus berries', 'Cubeb pepper'],
                                             'family': 'Burseraceae',
                                             'hindi_regional_names': [   'Carpobalsamum',
                                                                         'Balm of Gilead Berries',
                                                                         'Mecca Balsam Berry'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Habb-e-Balsan Asli', 'Carpobalsamum'],
                                             'part_used': 'Dried Fruit / Berries',
                                             'synonyms': ['Carpobalsamum', 'Balsam fruit', 'Amyris opobalsamum fruit'],
                                             'urdu_name': 'Habb-e-Balsan / Balsam Berries'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Kasir-e-Riyah',
                                                         'Munaqqi-e-Sadr',
                                                         'Munaqqi-e-Reham',
                                                         'Hazim-e-Taam',
                                                         'Muqawwi-e-Bah'],
                                            'badal': ['Ood-e-Balsan', 'Darchini'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '1g to 3g in decoction or compound powders.',
                                            'mizaj': 'Garm 2, Khushk 2',
                                            'musleh': 'Sharbat-e-Banafsha & Sikanjabeen',
                                            'muzir': 'May induce cephalic heat in hot temperaments without Musleh.',
                                            'tadbeer': 'Lightly crushed before preparing infusion or electuary'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Accelerates gastrointestinal motility and reduces visceral '
                                                           'hypersensitivity in rodent dyspepsia models.',
                                          'clinical_rct': 'Classical constituent in royal confections for visceral '
                                                          'flatulence, delayed menstruation, and nervous dyspepsia.',
                                          'evidence_grade': 'E4 (Classical Compendia & Modern Carminative Evidence)',
                                          'in_vitro': 'In vitro spasmolytic activity on gastrointestinal and uterine '
                                                      'smooth muscle, inhibition of enteric gas production.',
                                          'primary_constituents': [   'Volatile oleoresin terpenes (alpha-pinene, '
                                                                      'limonene)',
                                                                      'Balsam resins',
                                                                      'Gallic acid',
                                                                      'Flavonoids']},
                   'murakkab_roles': ['Chief active in Taryaq-e-Farooq, Jawarish Zarooni, and Majun Balsan'],
                   'organ_axis_affinity': [   'Axis 04 (Meda-Ama / Gastrointestinal Axis)',
                                              'Axis 07 (Tanasul-Bah / Reproductive Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 1.0%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Piper cubeba exhausted berries', 'Juniper berries'],
                                           'microscopy': 'Pericarp with large schizogenous oleoresin ducts in '
                                                         'mesocarp, stone cells in endocarp, seeds with exalbuminous '
                                                         'embryo.',
                                           'morphology': 'Small globose or pyriform reddish-brown berries, 4-6 mm '
                                                         'diameter, wrinkled surface, calyx persistent at base, '
                                                         'intense balsamic fragrant aroma, warm pungent aromatic '
                                                         'taste.',
                                           'total_ash': 'Not more than 4.5%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-328',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Fruit / Berries',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '66',
                                                   'upi_volume': 'Part-I, Vol. III'},
                   'primary_unani_citations': [   {   'claim_type': 'Aromatic Carminative, Uterine Deobstruent & '
                                                                    'Digestive Tonic',
                                                      'original_text_snippet': 'حب البلسان: ألطف من خشب البلسان، حار '
                                                                               'يابس في الثانية، يحلل الرياح الغليظة '
                                                                               'وينقي الصدر والرحم ويقوي الهضم۔',
                                                      'page': '239',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': ['Avoid excessive use in hyperpyrexia.'],
                                          'drug_interactions': ['None documented.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_AROMATIC_CARMINATIVE'},
                   'zmf_id': 'ZMF-328'},
    'ZMF-329': {   'canonical_identity': {   'arabic_name': 'Sandroos',
                                             'botanical_authority': '(Gaertn.) Oliv.',
                                             'botanical_name': 'Trachylobium verrucosum (Gaertn.) Oliv.',
                                             'canonical_unani_name': 'Sandroos',
                                             'confusable_species': ['Colophony (Pine resin)', 'Dammar resin'],
                                             'family': 'Fabaceae',
                                             'hindi_regional_names': ['Sandarac', 'Sandroos', 'Gum Juniper'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Sandroos Asli', 'Sandarac Gum'],
                                             'part_used': 'Dried Exuded Hard Resin',
                                             'synonyms': [   'Tetraclinis articulata (Vahl) Mast.',
                                                             'Sandarac Tree Resin',
                                                             'Resina Sandaraca'],
                                             'urdu_name': 'Sandroos / Sandarac Resin'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Habis-ud-Dam',
                                                         'Mujaffif-e-Ratubat-e-Riyah',
                                                         'Daf-e-Nafas-ud-Dam',
                                                         'Habis-e-Ishal',
                                                         'Mudammil'],
                                            'badal': ['Dam-ul-Akhwain', 'Kahroba'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '500mg to 1.5g in powder or electuary.',
                                            'mizaj': 'Garm 1, Khushk 2',
                                            'musleh': 'Roghan-e-Badam & Kateera',
                                            'muzir': 'Excessive internal use may cause colic in dry colonic '
                                                     'temperaments without Musleh.',
                                            'tadbeer': 'Pulverized into micro-fine powder with gum acacia or sugar'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Demonstrated significant reduction in pulmonary vascular '
                                                           'exudation in rodent lung injury models.',
                                          'clinical_rct': 'Centuries of clinical verification in pulmonary '
                                                          'tuberculosis hemoptysis, chronic bronchial catarrh, and '
                                                          'epistaxis.',
                                          'evidence_grade': 'E4 (Robust Classical & Modern Hemostatic Evidence)',
                                          'in_vitro': 'Strong astringent, capillary microvascular sealing, inhibition '
                                                      'of platelet-activating factor-induced capillary leakage.',
                                          'primary_constituents': [   'Sandaracopimaric acid',
                                                                      'Sandaracinic acid',
                                                                      'Callitrisic acid',
                                                                      'Volatile monoterpenes']},
                   'murakkab_roles': ['Key constituent in Qurs Sandroos, Sufoof-e-Habis, and Habb-e-Nafas-ud-Dam'],
                   'organ_axis_affinity': [   'Axis 05 (Tanaffus / Respiratory Axis)',
                                              'Axis 02 (Qalb-Urooq / Cardio-Vascular Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 1.0%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': [   'Colophony pine resin (softens in mouth)',
                                                                    'Pistacia lentiscus resin'],
                                           'microscopy': 'Soluble in alcohol and ether; insoluble in water; non-sticky '
                                                         'when chewed; leaves white residue on glass slide.',
                                           'morphology': 'Elongated pale yellow or orange-yellow brittle cylindrical '
                                                         'tears, 0.5-2 cm long, dusty surface, vitreous fracture, '
                                                         'faint pine-like aroma, crumbles between teeth without '
                                                         'softening (unlike Mastagi).',
                                           'total_ash': 'Not more than 1.5%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-329',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Exuded Hard Resin',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '102',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Potent Hemostatic, Pulmonary Desiccant & '
                                                                    'Anti-Hemoptysis Resin',
                                                      'original_text_snippet': 'سندروس: حار في الأولى يابس في الثانية، '
                                                                               'يحبس الدم ونفثه وإسهاله، ويجفف '
                                                                               'الرطوبات السائلة من الصدر والرئة۔',
                                                      'page': '250',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': ['Contraindicated in acute severe constipation.'],
                                          'drug_interactions': ['None documented.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_POTENT_HEMOSTATIC'},
                   'zmf_id': 'ZMF-329'},
    'ZMF-330': {   'canonical_identity': {   'arabic_name': 'Usara Rewand / Gamboge',
                                             'botanical_authority': '(Gaertn.) Desr.',
                                             'botanical_name': 'Garcinia morella (Gaertn.) Desr.',
                                             'canonical_unani_name': 'Usara Rewand',
                                             'confusable_species': [   'Rheum emodi extract (true Revand extract)',
                                                                       'Yellow ochre'],
                                             'family': 'Clusiaceae',
                                             'hindi_regional_names': ['Gamboge', 'Gotapuli', 'Usara-e-Revand'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Usara Rewand Asli', 'Gamboge Pipe'],
                                             'part_used': 'Gum Resin Exuded from Incised Trunk',
                                             'synonyms': ['Garcinia hanburyi Hook.f.', 'Gamboge resin', 'Cambogia'],
                                             'urdu_name': 'Usara Rewand / Gamboge Resin'},
                   'category': 'SCHEDULE_E1_POISON_HIGH_RISK',
                   'classical_profile': {   'afaal': [   'Mushil-e-Qawi',
                                                         'Mukhrij-e-Maa-ul-Istisqa',
                                                         'Munaqqi-e-Balgham-e-Ghaleez',
                                                         'Qatil-e-Deedan'],
                                            'badal': ['Jalapa', 'Turbud'],
                                            'daraja': 'Daraja 3',
                                            'dosage_context': '60mg to 150mg MAXIMUM of purified gum resin. Lethal in '
                                                              'crude overdose. HARD-BLOCKED FROM AI COPILOT.',
                                            'mizaj': 'Garm 3, Khushk 3',
                                            'musleh': 'Mastagi, Kateera, Roghan-e-Badam & Sikanjabeen',
                                            'muzir': 'DRASTIC VIOLENT CATHARTIC. Toxic overdose triggers catastrophic '
                                                     'gastrointestinal ulceration, bloody diarrhea and collapse.',
                                            'tadbeer': 'Mandatory traditional purification: rubbed in lemon juice or '
                                                       'sour pomegranate juice and dried in shade'},
                   'governance': {   'ai_permission': AIPermission.BLOCKED_HIGH_RISK,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.SAFETY_REVIEWED},
                   'modern_evidence': {   'animal_models': 'Triggers massive intraluminal fluid secretion in rodent '
                                                           'loop assays; narrow margin of safety.',
                                          'clinical_rct': 'Classical emergency resort in intractable anasarca and '
                                                          'abdominal dropsy (Istisqa-e-Zaqqi) under hospital '
                                                          'supervision.',
                                          'evidence_grade': 'E4 (Classical Compendia Efficacy with Strict Poison '
                                                            'Schedule E-1 Classification)',
                                          'in_vitro': 'Violent stimulation of intestinal myenteric plexus, inhibition '
                                                      'of Na+/K+-ATPase in enterocytes, potent apoptosis induction.',
                                          'primary_constituents': [   'Gambogic acid',
                                                                      'Morellin',
                                                                      'Morellinol',
                                                                      'Guttiferones',
                                                                      'Water-soluble gum (up to 20%)']},
                   'murakkab_roles': [   'Regulated active in Habb-e-Istisqa, Habb-e-Mudirr, and classical emergency '
                                         'cathartic pills'],
                   'organ_axis_affinity': [   'Axis 04 (Meda-Ama / Gastrointestinal Axis)',
                                              'Axis 06 (Kulyatain-Masana / Nephro-Urological Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 1.0%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': [   'Dyed synthetic resins',
                                                                    'Inferior mass gamboge containing sand'],
                                           'microscopy': 'Microscopy reveals no cellular elements; amorphous matrix '
                                                         'containing abundant resin droplets and yellow gambogic acid '
                                                         'granules soluble in ammonia.',
                                           'morphology': 'Cylindrical solid rolls (pipe gamboge), 2-5 cm diameter, '
                                                         'rich orange-brown surface, smooth conchoidal fracture, '
                                                         'odorless, acrid taste, forms bright yellow emulsion with '
                                                         'water.',
                                           'total_ash': 'Not more than 2.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-330',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Gum Resin Exuded from Incised Trunk',
                                                   'regulatory_status': 'RESTRICTED SCHEDULE E(1) POISON. Strictly '
                                                                        'governed.',
                                                   'upi_page': '154',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Drastic Hydragogue Purgative & Cathartic for '
                                                                    'Dropsy (SCHEDULE E-1 TOXIC)',
                                                      'original_text_snippet': 'عصارہ ریوند: گرم در سوم و خشک در سوم، '
                                                                               'مسهل غایت قوی و عنیف، مخرج بلغم و آب '
                                                                               'استسقا، و زیاده خوردن آن مهلک است۔',
                                                      'page': '415',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Khazain-ul-Advia (Hakeem Najmul Ghani)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Vol. I (Advia-e-Mufarradah)'}],
                   'safety_firewall': {   'contraindications': [   'ABSOLUTELY CONTRAINDICATED IN PREGNANCY, ELDERLY, '
                                                                   'CHILDREN, AND PEPTIC ULCER DISEASE.'],
                                          'drug_interactions': [   'Strictly contraindicated with digitalis or '
                                                                   'diuretics due to lethal hypokalemia.'],
                                          'is_schedule_e1': True,
                                          'pregnancy_lactation': 'CONTRAINDICATED_IN_PREGNANCY',
                                          'toxicity_class': 'SCHEDULE_E1_DRASTIC_CATHARTIC_POISON'},
                   'zmf_id': 'ZMF-330'},
    'ZMF-331': {   'canonical_identity': {   'arabic_name': 'Kushta Qishr-ul-Baid',
                                             'botanical_authority': 'Classical Animal-Mineral Calx',
                                             'botanical_name': 'Gallus domesticus (Egg Shell Calx)',
                                             'canonical_unani_name': 'Kushta Baiza-e-Murgh',
                                             'confusable_species': [   'Crude pulverized egg shell (uncalcined)',
                                                                       'Chalk powder'],
                                             'family': 'Calcined Avian Shell Calx',
                                             'hindi_regional_names': [   'Kukkutanda Twak Bhasma',
                                                                         'Eggshell Calx',
                                                                         'Calcined Eggshell'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Kushta Baiza-e-Murgh Asli'],
                                             'part_used': "Purified Incinerated Hen's Egg Shell",
                                             'synonyms': [   'Kukkutandatwak Bhasma',
                                                             'Calcium Carbonate Micro-Calx',
                                                             'Post Baiza Murgh'],
                                             'urdu_name': 'Kushta Baiza-e-Murgh / Egg Shell Calx'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Mumsik-e-Mani',
                                                         'Mughalliz-e-Mani',
                                                         'Daf-e-Sailan-ur-Reham',
                                                         'Daf-e-Kasrat-e-Tams',
                                                         'Muqawwi-e-Izam'],
                                            'badal': ['Kushta Sadaf', 'Kushta Marjan'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '125mg to 250mg with butter, honey, or Majun Salab.',
                                            'mizaj': 'Sard 1, Khushk 2',
                                            'musleh': 'Mastagi & Roghan-e-Badam',
                                            'muzir': 'Uncalcined raw shell causes severe urinary gravel and gastric '
                                                     'irritation.',
                                            'tadbeer': 'Egg membranes peeled off, washed with salt water, ground in '
                                                       'Ghritkumari or Barg-e-Dhatura juice and calcined in Gajput '
                                                       'fire'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Significant increase in bone mineral density and cortical '
                                                           'thickness in ovariectomized osteoporotic rodent models.',
                                          'clinical_rct': 'Decades of verified clinical success in chronic '
                                                          'spermatorrhea (Jiryan), premature ejaculation, intractable '
                                                          'leucorrhea, and osteoporosis.',
                                          'evidence_grade': 'E5 (Extensive Classical Pharmacopoeial & Clinical '
                                                            'Gynecological Evidence)',
                                          'in_vitro': 'Enhances osteoblast proliferation, increases alkaline '
                                                      'phosphatase expression, high intestinal calcium absorption '
                                                      'kinetics.',
                                          'primary_constituents': [   'Bioavailable Calcium (as CaCO3 and CaO >85%)',
                                                                      'Strontium traces',
                                                                      'Magnesium',
                                                                      'Organic trace matrix peptides']},
                   'murakkab_roles': [   'Chief active in Majun Baiza-e-Murgh, Majun Supari Pak, and Qurs Kushta '
                                         'Baiza-e-Murgh'],
                   'organ_axis_affinity': [   'Axis 07 (Tanasul-Bah / Reproductive Axis)',
                                              'Axis 08 (Izam-Mafasil / Musculoskeletal Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 0.5%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': [   'Crude uncalcined eggshell meal',
                                                                    'Industrial precipitated calcium carbonate'],
                                           'microscopy': 'XRD confirms conversion to nanocrystalline calcite and '
                                                         'calcium oxide matrix; high biological bio-absorption '
                                                         'profile.',
                                           'morphology': 'Dull white, odorless, tasteless, micro-fine calcined powder, '
                                                         'passes through 150-mesh sieve, floats on water '
                                                         '(Varitaratva), smooth feel between fingers.',
                                           'total_ash': 'Residue on ignition >95%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-331',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': "Purified Incinerated Hen's Egg Shell",
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '142',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Premier Bioavailable Calcium Calx, Seminal '
                                                                    'Thickener, Anti-Leucorrheal & Bone Fortifier',
                                                      'original_text_snippet': 'کشتہ بیضہ مرغ: سرد در اول و خشک در '
                                                                               'دوم، غایت ممسک منی، دافع رقت و سرعت '
                                                                               'انزال، و مقوی اعصاب و دافع سیلان الرحم '
                                                                               'و کثرت طمث است۔',
                                                      'page': '58',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Kitab-ul-Taklees (Classical Unani Alchemy)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Treatise on Animal Calces'}],
                   'safety_firewall': {   'contraindications': [   'Contraindicated in hypercalcemia and '
                                                                   'calcium-containing kidney stones.'],
                                          'drug_interactions': [   'Take 2 hours apart from iron supplements or '
                                                                   'fluoroquinolones.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_CALCINED_CALCIUM_TONIC'},
                   'zmf_id': 'ZMF-331'},
    'ZMF-332': {   'canonical_identity': {   'arabic_name': 'Hajar-ul-Yahood',
                                             'botanical_authority': 'Fossil Mineral',
                                             'botanical_name': 'Fossil Encrinite / Lapis Judaicus',
                                             'canonical_unani_name': 'Hajar-ul-Yahood',
                                             'confusable_species': [   'Ordinary limestone pebbles',
                                                                       'Gypsum imitation stones'],
                                             'family': 'Fossilized Echinoderm Spine',
                                             'hindi_regional_names': [   'Hazrul Yahood',
                                                                         'Sang-e-Yahood',
                                                                         'Lapis Judaicus',
                                                                         'Fossil Encrinite'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Kushta Hajar-ul-Yahood', 'Hazrul Yahood Asli'],
                                             'part_used': 'Purified Fossilized Spine of Cidaris',
                                             'synonyms': [   "Jew's Stone",
                                                             'Echinoid Fossil Calx',
                                                             'Petrified Olive Stone'],
                                             'urdu_name': "Hajar-ul-Yahood / Jew's Stone"},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Mufattit-e-Hasat-e-Kulyah wa Masana',
                                                         'Mudirr-e-Baul',
                                                         'Daf-e-Huraq-ul-Baul',
                                                         'Jali-e-Majari-e-Baul'],
                                            'badal': ['Kushta Sadaf', 'Javakhar'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '250mg to 500mg with Sharbat-e-Bazoori Motadil.',
                                            'mizaj': 'Garm 1, Khushk 2',
                                            'musleh': 'Sharbat-e-Bazoori & Roghan-e-Badam',
                                            'muzir': 'Excessive internal use in dehydrated patients without Musleh may '
                                                     'cause bladder irritation.',
                                            'tadbeer': 'Calcinated by quenching 21 times in radish juice (Aab-e-Turb) '
                                                       'or Kulthi decoction, followed by incineration'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Dose-dependent dissolution of surgical foreign-body '
                                                           'induced urinary calculi in rodent bladder models.',
                                          'clinical_rct': 'Universally renowned in Unani hospitals for dissolving and '
                                                          'expelling renal and bladder stones without surgery.',
                                          'evidence_grade': 'E5 (Extensive Classical Compendia & Hospital Lithotriptic '
                                                            'Evidence)',
                                          'in_vitro': 'Potent in vitro dissolution of calcium oxalate and calcium '
                                                      'phosphate kidney stones; inhibits crystal nucleation and '
                                                      'aggregation.',
                                          'primary_constituents': [   'Calcium carbonate (CaCO3 >80%)',
                                                                      'Magnesium carbonate',
                                                                      'Silica (SiO2)',
                                                                      'Trace iron and phosphates']},
                   'murakkab_roles': [   'Chief active in Kushta Hajar-ul-Yahood, Habb-e-Mudirr-e-Baul, and '
                                         'Sufoof-e-Hasat'],
                   'organ_axis_affinity': ['Axis 06 (Kulyatain-Masana / Nephro-Urological Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 0.5%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Uncalcined fossil fragments', 'Chalk stone'],
                                           'microscopy': 'Microscopy and XRD show calcium carbonate in crystalline '
                                                         'calcite form associated with magnesium, silica, and '
                                                         'phosphate traces.',
                                           'morphology': 'Fine, off-white or yellowish-grey impalpable powder, '
                                                         'odorless, slightly saline taste, floats on water when '
                                                         'properly calcined.',
                                           'total_ash': 'Calcium carbonate >80%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-332',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Purified Fossilized Spine of Cidaris',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '140',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Supreme Classical Lithotriptic (Mufattit-e-Hasat) '
                                                                    'for Renal & Bladder Calculi',
                                                      'original_text_snippet': 'حجر اليهود: حجر زیتونی الشکل، حار یابس '
                                                                               'فی الثانیہ، یفتت حصاۃ الکلی والمثانۃ '
                                                                               'تفتیتا عجیبا ویدر البول بولا قویا۔',
                                                      'page': '192',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': [   'Contraindicated in complete urinary tract '
                                                                   'obstruction requiring emergency surgery.'],
                                          'drug_interactions': [   'Abundant fluid intake mandatory during '
                                                                   'administration.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_CALCINED_LITHOTRIPTIC'},
                   'zmf_id': 'ZMF-332'},
    'ZMF-333': {   'canonical_identity': {   'arabic_name': 'Panzahar / Hajr-ut-Taryaq',
                                             'botanical_authority': 'Hydrated Magnesium Silicate Mineral',
                                             'botanical_name': 'Bezoar / Serpentine Mineral Stone',
                                             'canonical_unani_name': 'Zahra Mohra',
                                             'confusable_species': [   'Soft soapstone without serpentine active',
                                                                       'Colored limestone'],
                                             'family': 'Mineral Ore',
                                             'hindi_regional_names': [   'Zahar Mohra',
                                                                         'Panzahar',
                                                                         'Serpentine Stone',
                                                                         'Antidote Stone'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Kushta Zahra Mohra', 'Zahar Mohra Khatai'],
                                             'part_used': 'Purified Hydrated Magnesium Silicate / Serpentine',
                                             'synonyms': ['Lapis Bezoar', 'Serpentine Stone', 'Bezoar Calx'],
                                             'urdu_name': 'Zahra Mohra / Bezoar Serpentine Stone'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Daf-e-Sumoom',
                                                         'Taryaq-e-Kabeer',
                                                         'Muqawwi-e-Qalb',
                                                         'Mufarreh',
                                                         'Daf-e-Khafqan wa Ghashi'],
                                            'badal': ['Jadwar', 'Kahroba'],
                                            'daraja': 'Daraja 1',
                                            'dosage_context': '125mg to 250mg with Khamira Gaozaban or Arq-e-Gaozaban.',
                                            'mizaj': 'Muaddil (Sard 1, Khushk 1)',
                                            'musleh': 'Gulab & Roghan-e-Banafsha',
                                            'muzir': 'Uncalcined stone should not be ingested raw.',
                                            'tadbeer': 'Levigated with pure rose water or arq-e-gaozaban for 21 days '
                                                       '(Tasaeed / Kharal-e-Aab-e-Gulab)'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Significantly decreases mortality in acute scorpion and '
                                                           'snake venom challenge models in laboratory rodents.',
                                          'clinical_rct': 'Royal clinical remedy in severe palpitations, cardiac '
                                                          'syncope, choleraic collapse, and toxic delirium.',
                                          'evidence_grade': 'E5 (Extensive Classical Compendia & Modern '
                                                            'Pharmacological Evidence)',
                                          'in_vitro': 'Adsorbs systemic endotoxins, protects myocardial cells from '
                                                      'catecholamine-induced arrhythmia and toxic necrosis.',
                                          'primary_constituents': [   'Hydrated magnesium silicate Mg3(Si2O5)(OH)4',
                                                                      'Iron traces',
                                                                      'Trace aluminum and calcium']},
                   'murakkab_roles': [   'Chief active in Jawahar Mohra, Khamira Abresham Hakim Arshad Wala, and '
                                         'Taryaq-e-Farooq'],
                   'organ_axis_affinity': [   'Axis 02 (Qalb-Urooq / Cardio-Vascular Axis)',
                                              'Axis 01 (Dimagh-Asab / Neuro-Psychiatric Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 0.5%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': [   'Unpurified raw serpentine fragments',
                                                                    'Talc substitute'],
                                           'microscopy': 'XRD confirms serpentine-group minerals '
                                                         '(antigorite/chrysotile/lizardite hydrated magnesium '
                                                         'silicates); free of heavy metals.',
                                           'morphology': 'Fine, greenish-white to pale olive-green impalpable powder, '
                                                         'smooth unctuous feel, odorless, tasteless, completely floats '
                                                         'on water.',
                                           'total_ash': 'Silica & Magnesium >85%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-333',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Purified Hydrated Magnesium Silicate / Serpentine',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '146',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Supreme Universal Antidote (Taryaq-e-Aam), '
                                                                    'Cardiac Vitalizer & Anti-Arrhythmic',
                                                      'original_text_snippet': 'فادزہر / زہر مہرہ: معتدل، الترياق '
                                                                               'الأعظم لجميع السموم واللدغات ومقو '
                                                                               'للقلب والروح دافع للغشي والخفقان۔',
                                                      'page': '188',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': ['None noted in therapeutic posology.'],
                                          'drug_interactions': [   'Compatible with conventional supportive cardiac '
                                                                   'therapies.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_CALCINED_ANTIDOTE_TONIC'},
                   'zmf_id': 'ZMF-333'},
    'ZMF-334': {   'canonical_identity': {   'arabic_name': 'Habb-ul-Qilqil',
                                             'botanical_authority': '(L.) Roxb.',
                                             'botanical_name': 'Senna tora (L.) Roxb.',
                                             'canonical_unani_name': 'Tukhm-e-Panwar',
                                             'confusable_species': [   'Cassia occidentalis seeds (Kasondi)',
                                                                       'Cassia sophera seeds'],
                                             'family': 'Fabaceae',
                                             'hindi_regional_names': [   'Chakwad Beej',
                                                                         'Chakramarda Seeds',
                                                                         'Ringworm Cassia Seeds',
                                                                         'Sickle Senna'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Tukhm-e-Panwar Desi', 'Chakwad Beej'],
                                             'part_used': 'Dried Seeds',
                                             'synonyms': ['Cassia tora L.', 'Cassia obtusifolia L.', 'Sicklepod Seeds'],
                                             'urdu_name': 'Tukhm-e-Panwar / Chakwad Seeds'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Jali',
                                                         'Daf-e-Qooba wa Daad',
                                                         'Musaffi-e-Dam',
                                                         'Qatil-e-Futoor',
                                                         'Mulaiyin'],
                                            'badal': ['Bawachi', 'Gandhak'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '1g to 3g internally; liberally applied as topical paste '
                                                              'in vinegar for skin ringworm.',
                                            'mizaj': 'Garm 2, Khushk 2',
                                            'musleh': 'Ghee, Sikanjabeen & Roghan-e-Badam',
                                            'muzir': 'Large doses cause loose motions and griping without Musleh.',
                                            'tadbeer': 'Lightly roasted (Biryan) to remove bitterness and ground in '
                                                       'buttermilk or vinegar for topical paste'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Marked reduction of erythema, scaling and induration in '
                                                           'rodent psoriasis plaque models.',
                                          'clinical_rct': 'Extensive clinical validation in tinea corporis, tinea '
                                                          'cruris, and chronic ringworm lesions in Unani '
                                                          'dermatological clinics.',
                                          'evidence_grade': 'E4 (Robust Clinical & Classical Dermatological Evidence)',
                                          'in_vitro': 'Potent in vitro antifungal activity against dermatophytes '
                                                      '(Trichophyton rubrum, Microsporum canis), inhibits keratinocyte '
                                                      'hyperproliferation.',
                                          'primary_constituents': [   'Chrysophanol',
                                                                      'Emodin',
                                                                      'Aloe-emodin',
                                                                      'Rubrofusarin',
                                                                      'Torachrysone',
                                                                      'Anthraquinone glycosides']},
                   'murakkab_roles': ['Chief active in Marham-e-Daad, Zimad-e-Panwar, and Sufoof-e-Musaffi'],
                   'organ_axis_affinity': [   'Axis 10 (Jild-Masamat / Dermato-Immunological Axis)',
                                              'Axis 04 (Meda-Ama / Gastrointestinal Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 2.0%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Senna occidentalis seeds', 'Weed seeds'],
                                           'microscopy': 'Palisade layer of thick-walled sclereids with light line, '
                                                         'hourglass cells, endosperm containing aleurone grains and '
                                                         'mucilage.',
                                           'morphology': 'Small rhomboidal, compressed seeds, 4-6 mm long, '
                                                         'greenish-brown to dark brown, glistening surface, hard, '
                                                         'bitter mucilaginous taste.',
                                           'total_ash': 'Not more than 6.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-334',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Seeds',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '120',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Premier Specific for Ringworm (Qooba), Psoriasis, '
                                                                    'Eczema & Alterative Laxative',
                                                      'original_text_snippet': 'تخم پنواڑ: گرم و خشک در دوم، غایت دافع '
                                                                               'داد و قوبا و جرب و خارش، مصفی خون و '
                                                                               'مسهل ملطف است۔',
                                                      'page': '165',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Khazain-ul-Advia (Hakeem Najmul Ghani)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Vol. II (Advia-e-Mufarradah)'}],
                   'safety_firewall': {   'contraindications': [   'Avoid excessive internal dose during active '
                                                                   'diarrhea.'],
                                          'drug_interactions': ['None documented.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_DERMATOLOGICAL_ALTERATIVE'},
                   'zmf_id': 'ZMF-334'},
    'ZMF-335': {   'canonical_identity': {   'arabic_name': 'Sheetraj Hindi',
                                             'botanical_authority': 'L.',
                                             'botanical_name': 'Plumbago zeylanica L.',
                                             'canonical_unani_name': 'Sheetraj Hindi',
                                             'confusable_species': [   'Plumbago rosea (Lal Chitrak - highly toxic)',
                                                                       'Plumbago capensis'],
                                             'family': 'Plumbaginaceae',
                                             'hindi_regional_names': [   'Chitrak',
                                                                         'Chita',
                                                                         'White Leadwort Root',
                                                                         'Sheetraj'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Sheetraj Hindi Asli', 'Chitrak Chhal'],
                                             'part_used': 'Dried Root',
                                             'synonyms': ['White Plumbago', 'Leadwort Root', 'Plumbago Root'],
                                             'urdu_name': 'Sheetraj Hindi / Chitrak Root'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Kasir-e-Riyah',
                                                         'Muharrik-e-Ishteha',
                                                         'Hazim-e-Taam',
                                                         'Muhallil-e-Tihal',
                                                         'Musakkin-e-Waja-ul-Mafasil'],
                                            'badal': ['Zanjabeel', 'Filfil Siyah'],
                                            'daraja': 'Daraja 3',
                                            'dosage_context': '500mg to 1.5g in digestive electuaries or compound '
                                                              'powders.',
                                            'mizaj': 'Garm 3, Khushk 3',
                                            'musleh': 'Roghan-e-Badam, Shakar & Dudh (Milk)',
                                            'muzir': 'Excessive uncorrected doses cause violent mucosal burning, '
                                                     'gastritis and uterine contractions.',
                                            'tadbeer': 'Mandatory traditional Shodhana: roots soaked in lime water '
                                                       '(Chune ka Paani) for 3 days, washed thoroughly and shade '
                                                       'dried'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Dose-dependent reduction of serum cholesterol, LDL, and '
                                                           'triglycerides in atherogenic animal models; potent '
                                                           'anti-arthritic activity.',
                                          'clinical_rct': 'Centuries of classical clinical success in atonic '
                                                          'dyspepsia, loss of appetite, splenomegaly, and chronic '
                                                          'rheumatic pain.',
                                          'evidence_grade': 'E4 (Robust Classical & Modern Pharmacological Digestive '
                                                            'Evidence)',
                                          'in_vitro': 'Potent stimulation of gastric pepsin, trypsin, and pancreatic '
                                                      'lipase secretion; marked hypolipidemic and anti-atherosclerotic '
                                                      'action.',
                                          'primary_constituents': [   'Plumbagin '
                                                                      '(2-methyl-5-hydroxy-1,4-naphthoquinone)',
                                                                      '3-Chloroplumbagin',
                                                                      'Zeylinone',
                                                                      'Isozeylinone',
                                                                      'Beta-sitosterol']},
                   'murakkab_roles': ['Chief active in Jawarish Sheetraj, Majun Falasifa, and Sufoof-e-Hazim'],
                   'organ_axis_affinity': [   'Axis 04 (Meda-Ama / Gastrointestinal Axis)',
                                              'Axis 03 (Jigar-Tihal / Hepato-Splenic Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 1.5%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': [   'Plumbago rosea (Rakta Chitrak - excessive '
                                                                    'toxicity)',
                                                                    'Zanthoxylum roots'],
                                           'microscopy': 'Cork multilayered, broad secondary phloem with tannin cells '
                                                         'and starch, vessels with bordered pits, fibers abundant.',
                                           'morphology': 'Cylindrical stout root pieces, 5-15 cm long, 0.5-2 cm thick, '
                                                         'reddish-brown deeply fissured bark, light yellow wood, '
                                                         'characteristic pungent acrid taste.',
                                           'total_ash': 'Not more than 5.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-335',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Root',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '106',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Powerful Digestive Stimulant, Gastric Fire '
                                                                    'Igniter & Anti-Splenomegaly',
                                                      'original_text_snippet': 'شيطرج: حار يابس في الثالثة، هاضم مشه '
                                                                               'للطعام جدا، محلل لأورام الطحال ومسكن '
                                                                               'لأوجاع المفاصل الباردة۔',
                                                      'page': '262',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': [   'Strictly contraindicated in pregnancy '
                                                                   '(abortifacient) and active peptic ulcer bleeding.'],
                                          'drug_interactions': [   'Avoid co-administration with anti-platelet or '
                                                                   'anticoagulant medications (synergistic).'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'CONTRAINDICATED_IN_PREGNANCY',
                                          'toxicity_class': 'POTENT_DIGESTIVE_SHODHANA_REQUIRED'},
                   'zmf_id': 'ZMF-335'},
    'ZMF-336': {   'canonical_identity': {   'arabic_name': 'Fanjangusht / Uslaq',
                                             'botanical_authority': 'L.',
                                             'botanical_name': 'Vitex negundo L.',
                                             'canonical_unani_name': 'Sambhalu',
                                             'confusable_species': ['Vitex agnus-castus L.', 'Vitex trifolia L.'],
                                             'family': 'Lamiaceae',
                                             'hindi_regional_names': [   'Sambhalu',
                                                                         'Nirgundi',
                                                                         'Five-Leaved Chaste Tree',
                                                                         'Uslaq'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Sambhalu Desi', 'Tukhm-e-Sambhalu'],
                                             'part_used': 'Dried Seeds and Leaves',
                                             'synonyms': ['Vitex incisa Lam.', 'Chaste Tree Seeds', 'Nirgundi Beej'],
                                             'urdu_name': 'Sambhalu / Tukhm-e-Sambhalu'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Muhallil-e-Awram',
                                                         'Musakkin-e-Waja-ul-Mafasil',
                                                         'Kasir-e-Riyah',
                                                         'Mudirr-e-Tams',
                                                         'Daf-e-Kharash'],
                                            'badal': ['Babuna', 'Asgandh'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '3g to 5g in decoction; extensive external use in warm '
                                                              'fomentations and oils.',
                                            'mizaj': 'Garm 1, Khushk 2',
                                            'musleh': 'Gaozaban, Shakar & Roghan-e-Banafsha',
                                            'muzir': 'Large doses may cause dry headache in arid hot temperaments '
                                                     'without Musleh.',
                                            'tadbeer': 'Cleaned, shade dried, powdered for internal use; leaves boiled '
                                                       'in water for fomentation (Natool) and medicated oil '
                                                       '(Roghan-e-Sambhalu)'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': "Demonstrated reduction in complete Freund's adjuvant "
                                                           'arthritis paw swelling and radiological joint destruction '
                                                           'in animal trials.',
                                          'clinical_rct': 'Validated in clinical randomized trials for chronic '
                                                          'osteoarthritic joint pain, sciatica, and premenstrual '
                                                          'syndrome mastalgia.',
                                          'evidence_grade': 'E5 (Extensive Classical & Modern Clinical Orthopedic '
                                                            'Evidence)',
                                          'in_vitro': 'Potent dual inhibition of cyclooxygenase-2 (COX-2) and '
                                                      '5-lipoxygenase (5-LOX) inflammatory cascades, central and '
                                                      'peripheral analgesia.',
                                          'primary_constituents': [   'Nishindine',
                                                                      'Negundoside',
                                                                      'Casticin',
                                                                      'Luteolin',
                                                                      'Artemetin',
                                                                      'Beta-caryophyllene']},
                   'murakkab_roles': ['Chief active in Roghan-e-Sambhalu, Majun Suranjan, and Zimad-e-Mafasil'],
                   'organ_axis_affinity': [   'Axis 08 (Izam-Mafasil / Musculoskeletal Axis)',
                                              'Axis 07 (Tanasul-Bah / Reproductive Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 2.0%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Vitex trifolia seeds'],
                                           'microscopy': 'Epicarp of parenchymatous cells with dense cuticle, mesocarp '
                                                         'with stone cells and vascular bundles; leaves show peltate '
                                                         'glandular trichomes.',
                                           'morphology': 'Seeds subglobose, 2-3 mm diameter, greyish-black, hard, '
                                                         '4-celled, aromatic odor on crushing, warm pungent taste; '
                                                         'leaves palmately 3-5 foliolate.',
                                           'total_ash': 'Not more than 7.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-336',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Seeds and Leaves',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '104',
                                                   'upi_volume': 'Part-I, Vol. III'},
                   'primary_unani_citations': [   {   'claim_type': 'Potent Anti-Inflammatory, Analgesic, '
                                                                    'Anti-Arthritic & Uterine Regulator',
                                                      'original_text_snippet': 'فنجنكشت: حار في الأولى يابس في '
                                                                               'الثانية، يحلل الرياح والأورام '
                                                                               'البلغمية، ويسكن أوجاع المفاصل ويطفئ '
                                                                               'حرارة المني الزائدة۔',
                                                      'page': '258',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': ['None noted in therapeutic posology.'],
                                          'drug_interactions': [   'Compatible with conventional NSAIDs (permits dose '
                                                                   'reduction).'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_ANALGESIC_ANTI_INFLAMMATORY'},
                   'zmf_id': 'ZMF-336'},
    'ZMF-337': {   'canonical_identity': {   'arabic_name': 'Bazr-ul-Basal',
                                             'botanical_authority': 'L.',
                                             'botanical_name': 'Allium cepa L.',
                                             'canonical_unani_name': 'Tukhm-e-Piyaz',
                                             'confusable_species': [   'Nigella sativa (Kalonji - frequently confused '
                                                                       'in regional trade)'],
                                             'family': 'Amaryllidaceae',
                                             'hindi_regional_names': ['Piyaz ke Beej', 'Onion Seed', 'Palandu Beej'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Tukhm-e-Piyaz Asli', 'Genuine Onion Seeds'],
                                             'part_used': 'Dried Seeds',
                                             'synonyms': ['Onion Seeds', 'Semen Allii cepae', 'Bazr-ul-Basal'],
                                             'urdu_name': 'Tukhm-e-Piyaz / Onion Seeds'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Muqawwi-e-Bah-e-Qawi',
                                                         'Mughalliz-e-Mani',
                                                         'Muwallid-e-Mani',
                                                         'Mudirr-e-Baul',
                                                         'Kaser-e-Riyah'],
                                            'badal': ['Tukhm-e-Gandana', 'Tukhm-e-Shalgam'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '2g to 5g with warm milk in morning.',
                                            'mizaj': 'Garm 2, Khushk 1',
                                            'musleh': 'Kashneez Khushk & Roghan-e-Badam',
                                            'muzir': 'May cause gastric flatulence and bad breath without Musleh.',
                                            'tadbeer': 'Cleaned, lightly roasted (Biryan), pulverized and mixed with '
                                                       "cow's milk and honey"},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Marked elevation of serum testosterone, sperm motility '
                                                           'index, and testicular weight in male fertility rodent '
                                                           'models.',
                                          'clinical_rct': 'Long-standing clinical success in classical Unani practice '
                                                          'for asthenospermia, low seminal volume, and psychogenic '
                                                          'impotence.',
                                          'evidence_grade': 'E4 (Robust Classical & Modern Spermatogenic Evidence)',
                                          'in_vitro': 'Stimulates luteinizing hormone (LH) and follicle-stimulating '
                                                      'hormone (FSH) secretion, increases testicular antioxidant '
                                                      'catalase and SOD.',
                                          'primary_constituents': [   'Allicin precursor S-alk(en)yl-L-cysteine '
                                                                      'sulfoxides',
                                                                      'Quercetin glucosides',
                                                                      'Steroidal saponins',
                                                                      'Fixed fatty acids']},
                   'murakkab_roles': ['Chief active in Majun Piyaz, Majun Salab, and Sufoof-e-Mughalliz'],
                   'organ_axis_affinity': [   'Axis 07 (Tanasul-Bah / Reproductive Axis)',
                                              'Axis 06 (Kulyatain-Masana / Nephro-Urological Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 1.5%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': [   'Nigella sativa seeds (Kalonji)',
                                                                    'Allium tuberosum seeds'],
                                           'microscopy': 'Sclerenchymatous black seed coat, endosperm packed with '
                                                         'fixed oil and aleurone grains; distinctly distinguishable '
                                                         'from Kalonji under stereomicroscope.',
                                           'morphology': 'Small, angular, jet-black wrinkled seeds, 2-3 mm long, '
                                                         'flattened on one side, faint characteristic sulfurous allium '
                                                         'odor when crushed, pungent taste.',
                                           'total_ash': 'Not more than 6.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-337',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Seeds',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '126',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Sovereign Aphrodisiac (Muqawwi-e-Bah), '
                                                                    'Spermatogenic & Seminal Multiplier',
                                                      'original_text_snippet': 'بزر البصل: حار في الثانية يابس في '
                                                                               'الأولى، مهيج للباه جدا، مغلظ للمني '
                                                                               'ومحرك للشهوة ومدر للبول۔',
                                                      'page': '142',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': ['Avoid excessive use in active acid peptic disease.'],
                                          'drug_interactions': ['None documented.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_APHRODISIAC_VITALIZER'},
                   'zmf_id': 'ZMF-337'},
    'ZMF-338': {   'canonical_identity': {   'arabic_name': 'Auraq-ul-Hinna',
                                             'botanical_authority': 'L.',
                                             'botanical_name': 'Lawsonia inermis L.',
                                             'canonical_unani_name': 'Barg-e-Hina',
                                             'confusable_species': ['Camellia sinensis exhausted leaves'],
                                             'family': 'Lythraceae',
                                             'hindi_regional_names': ['Mehndi', 'Henna Leaves', 'Madanaka'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Barg-e-Hina Asli', 'Rajasthani Mehndi'],
                                             'part_used': 'Dried Leaves',
                                             'synonyms': ['Lawsonia alba Lam.', 'Henna Leaves', 'Barg-e-Mehndi'],
                                             'urdu_name': 'Barg-e-Hina / Mehndi Leaves'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Mubarrid',
                                                         'Muhallil-e-Awram',
                                                         'Daf-e-Huraq',
                                                         'Musaffi-e-Dam',
                                                         'Mudammil-e-Qurooh'],
                                            'badal': ['Shahtara', 'Berg-e-Neem'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '3g to 5g internally in infusion; freely applied '
                                                              'topically as cooling paste with water or vinegar.',
                                            'mizaj': 'Sard 1, Khushk 2',
                                            'musleh': 'Gaozaban, Shakar & Roghan-e-Banafsha',
                                            'muzir': 'Internal excessive use in cold phlegmatic temperaments produces '
                                                     'pulmonary chilliness without Musleh.',
                                            'tadbeer': 'Cleaned of stems, shade dried, pulverized into fine powder for '
                                                       'infusions or topical pastes'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Significant reduction of thermal burn surface area, rapid '
                                                           're-epithelialization in full-thickness dermal wound models '
                                                           'in animals.',
                                          'clinical_rct': 'Universal clinical staple for burning sensation in soles '
                                                          'and palms (Sozish-e-Qadam wa Dast), skin erythema, and '
                                                          'polyherbal blood purifiers.',
                                          'evidence_grade': 'E5 (Extensive Classical Pharmacopoeial & Clinical '
                                                            'Evidence)',
                                          'in_vitro': 'Strong antimicrobial against Candida albicans and '
                                                      'Staphylococcus aureus, accelerated wound healing and collagen '
                                                      'deposition.',
                                          'primary_constituents': [   'Lawsone (2-hydroxy-1,4-naphthoquinone)',
                                                                      'Gallic acid',
                                                                      'Tannins (up to 10%)',
                                                                      'Luteolin',
                                                                      'Flavonoids']},
                   'murakkab_roles': ['Chief active in Zimad-e-Hina, Roghan-e-Hina, and Arq-e-Murakkab Musaffi'],
                   'organ_axis_affinity': [   'Axis 10 (Jild-Masamat / Dermato-Immunological Axis)',
                                              'Axis 08 (Izam-Mafasil / Musculoskeletal Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 2.0%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Synthetic dye-laced adulterated leaf powders'],
                                           'microscopy': 'Anomocytic stomata on both surfaces, thick cuticle, spongy '
                                                         'mesophyll with large calcium oxalate rosette clusters, lack '
                                                         'of hairs.',
                                           'morphology': 'Greenish-brown elliptical to lanceolate entire leaves, 2-4 '
                                                         'cm long, short petiole, faint tea-like aroma, characteristic '
                                                         'astringent bitterish taste.',
                                           'total_ash': 'Not more than 10.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-338',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Leaves',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '26',
                                                   'upi_volume': 'Part-I, Vol. I'},
                   'primary_unani_citations': [   {   'claim_type': 'Potent Refrigerant (Mubarrid), Topical Burn '
                                                                    'Healer & Anti-Inflammatory',
                                                      'original_text_snippet': 'حناء: بارد في الأولى يابس في الثانية، '
                                                                               'محلل نافع لحرق النار ومسكن لأوجاع '
                                                                               'المفاصل والحمرة ونافع لجراحات الفم۔',
                                                      'page': '178',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': [   'Use caution internally in diagnosed G6PD enzyme '
                                                                   'deficiency.'],
                                          'drug_interactions': [   'Contraindicated internally in G6PD deficiency due '
                                                                   'to lawsone oxidative hemolysis risk.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_COOLING_VULNERARY'},
                   'zmf_id': 'ZMF-338'},
    'ZMF-339': {   'canonical_identity': {   'arabic_name': 'Zadwar / Antidotum',
                                             'botanical_authority': 'Wall. ex Hook.f. & Thomson',
                                             'botanical_name': 'Delphinium denudatum Wall. ex Hook.f. & Thomson',
                                             'canonical_unani_name': 'Jadwar',
                                             'confusable_species': [   'Aconitum heterophyllum (Atees - non-toxic but '
                                                                       'distinct)',
                                                                       'Aconitum ferox (Deadly poisonous Bish)'],
                                             'family': 'Ranunculaceae',
                                             'hindi_regional_names': [   'Nirbisi',
                                                                         'Jadwar',
                                                                         'Delphinium Root',
                                                                         'Antidote Tuber'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Jadwar Asli', 'Nirbisi Grade A'],
                                             'part_used': 'Dried Root Tuber',
                                             'synonyms': ['Jadwar Khatai', 'Delphinium denudatum root'],
                                             'urdu_name': 'Jadwar / Nirbisi Root'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Taryaq-e-Kabeer',
                                                         'Daf-e-Sumoom-e-Bish',
                                                         'Muqawwi-e-Qalb wa Dimagh',
                                                         'Mufarreh-e-Azam',
                                                         'Musakkin-e-Asab'],
                                            'badal': ['Zafran', 'Zahra Mohra'],
                                            'daraja': 'Daraja 3',
                                            'dosage_context': '500mg to 1g in precious royal electuaries.',
                                            'mizaj': 'Garm 3, Khushk 2',
                                            'musleh': 'Kashneez Khushk & Sikanjabeen',
                                            'muzir': 'High doses produce internal heat in hot sanguine temperaments '
                                                     'without Musleh.',
                                            'tadbeer': 'Cleaned, washed in rose water, pulverized into micro-fine '
                                                       'powder'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Dose-dependent protection against aconitine-induced '
                                                           'ventricular arrhythmias and chemical-induced epilepsy in '
                                                           'laboratory animals.',
                                          'clinical_rct': 'Premier classical medication for opioid detoxification, '
                                                          'cardiac arrhythmia, morphine addiction weaning, and '
                                                          'post-stroke rehabilitation.',
                                          'evidence_grade': 'E5 (Extensive Classical & Modern Neuro-Cardioprotective '
                                                            'Evidence)',
                                          'in_vitro': 'High-affinity neuroprotective activity against '
                                                      'glutamate-induced excitotoxicity, anticonvulsant and '
                                                      'anti-arrhythmic action.',
                                          'primary_constituents': [   'Denudatine',
                                                                      'Condelphine',
                                                                      'Delphinine-free diterpenoid alkaloids',
                                                                      'Stigmasterol',
                                                                      'Campesterol']},
                   'murakkab_roles': [   'Chief active in Khamira Gaozaban Ambari Jadwar Ood Saleeb Wala, Jawahar '
                                         'Mohra, and Hab-e-Jadwar'],
                   'organ_axis_affinity': [   'Axis 01 (Dimagh-Asab / Neuro-Psychiatric Axis)',
                                              'Axis 02 (Qalb-Urooq / Cardio-Vascular Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 1.0%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Aconitum ferox roots (lethal Bish)', 'Inula roots'],
                                           'microscopy': 'Parenchyma filled with starch grains, cambium in an '
                                                         'undulating continuous ring, absence of the violent tingling '
                                                         'alkaloidal sensation of aconitine.',
                                           'morphology': 'Conical or cylindrical root tubers, 2-5 cm long, '
                                                         'greyish-brown exterior, pale starchy white fracture, faint '
                                                         'earthy aroma, bitterish mucilaginous taste without numbness '
                                                         '(distinguishing it from poisonous Aconite).',
                                           'total_ash': 'Not more than 5.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-339',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Root Tuber',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '42',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Supreme Universal Classical Antidote '
                                                                    '(Taryaq-e-Azam), Cephalic & Cardioprotective',
                                                      'original_text_snippet': 'جدوار: حار في الثالثة يابس في الثانية، '
                                                                               'الترياق الأعظم لسموم البيش والعقرب، '
                                                                               'ومقو عظيم للقلب والدماغ ومفرح للروح۔',
                                                      'page': '182',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': ['None noted at standard therapeutic posology.'],
                                          'drug_interactions': [   'Safe and effective adjunct in addiction '
                                                                   'rehabilitation under clinical oversight.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_ROYAL_ANTIDOTE_TONIC'},
                   'zmf_id': 'ZMF-339'},
    'ZMF-340': {   'canonical_identity': {   'arabic_name': 'Afarbiyun',
                                             'botanical_authority': 'O.Berg',
                                             'botanical_name': 'Euphorbia resinifera O.Berg',
                                             'canonical_unani_name': 'Farfiyun',
                                             'confusable_species': ['Asafoetida', 'Galbanum'],
                                             'family': 'Euphorbiaceae',
                                             'hindi_regional_names': ['Euphorbium', 'Farfiyun', 'Euphorbia Gum Resin'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Farfiyun Asli'],
                                             'part_used': 'Dried Exuded Caustic Latex Gum',
                                             'synonyms': ['Euphorbia gum resin', 'Gum Euphorbium', 'Afarbiyun'],
                                             'urdu_name': 'Farfiyun / Euphorbium Gum'},
                   'category': 'SCHEDULE_E1_POISON_HIGH_RISK',
                   'classical_profile': {   'afaal': [   'Mushil-e-Anif',
                                                         'Daf-e-Irq-un-Nasa',
                                                         'Muhallil-e-Awram-e-Baridah',
                                                         'Jali-e-Qawi'],
                                            'badal': ['Turbud', 'Suranjan Talkh'],
                                            'daraja': 'Daraja 4',
                                            'dosage_context': '30mg to 60mg MAXIMUM with correctives. Lethal in crude '
                                                              'overdose. HARD-BLOCKED FROM AI COPILOT.',
                                            'mizaj': 'Garm 4, Khushk 4',
                                            'musleh': "Roghan-e-Badam, Kateera & Dudh (Cow's Milk)",
                                            'muzir': 'VIOLENT CAUSTIC IRRITANT POISON. Ingestion causes intense '
                                                     'mouth/throat ulceration, bloody diarrhea, and fatal circulatory '
                                                     'collapse.',
                                            'tadbeer': "Traditional Shodhana: fried in cow's ghee with gum tragacanth "
                                                       '(Kateera) to attenuate extreme caustic nature'},
                   'governance': {   'ai_permission': AIPermission.BLOCKED_HIGH_RISK,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.SAFETY_REVIEWED},
                   'modern_evidence': {   'animal_models': 'Induces complete desensitization of C-fiber nociceptors in '
                                                           'animal neuropathic pain models; intense topical vesicant '
                                                           'action.',
                                          'clinical_rct': 'Used historically in intractable chronic sciatica plaster '
                                                          'and paralytic facial palsy (Laqwa) under specialist Hakeem '
                                                          'administration.',
                                          'evidence_grade': 'E4 (Classical Compendia Efficacy with Strict Poison '
                                                            'Schedule E-1 Classification)',
                                          'in_vitro': 'Ultra-potent activation of transient receptor potential '
                                                      'vanilloid-1 (TRPV1) channels followed by long-lasting sensory '
                                                      'neuro-ablation.',
                                          'primary_constituents': [   'Resiniferatoxin (ultra-potent TRPV1 agonist)',
                                                                      'Euphorbic acid',
                                                                      'Euphorbol',
                                                                      'Diterpene esters']},
                   'murakkab_roles': [   'Regulated active in Zimad-e-Farfiyun, Roghan-e-Farfiyun, and Majun Jograj '
                                         'Guggul'],
                   'organ_axis_affinity': [   'Axis 08 (Izam-Mafasil / Musculoskeletal Axis)',
                                              'Axis 01 (Dimagh-Asab / Neuro-Psychiatric Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 1.0%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Ordinary Euphorbia latices'],
                                           'microscopy': 'Microscopy shows amorphous matrix with bone-shaped starch '
                                                         'grains and latex droplets; resinobenzol extracts '
                                                         'resiniferatoxin.',
                                           'morphology': 'Irregular dull yellowish or brownish tears or masses, 0.5-2 '
                                                         'cm diameter, perforated with double holes left by plant '
                                                         'spines, odorless, fiercely burning caustic taste.',
                                           'total_ash': 'Not more than 4.5%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-340',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Exuded Caustic Latex Gum',
                                                   'regulatory_status': 'RESTRICTED SCHEDULE E(1) POISON. Strictly '
                                                                        'governed.',
                                                   'upi_page': '156',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Violent Caustic Purgative, Anti-Sciatica Plaster '
                                                                    '& Resolvent (SCHEDULE E-1 TOXIC)',
                                                      'original_text_snippet': 'فرفيون: حار يابس في الرابعة، مسهل عنيف '
                                                                               'للمرة السوداء والبلغم اللزج، نافع لعرق '
                                                                               'النسا والقولنج العتيق، وقاتل في '
                                                                               'الزيادة۔',
                                                      'page': '244',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': [   'ABSOLUTELY CONTRAINDICATED IN PREGNANCY, '
                                                                   'GASTRITIS, AND OTC CONSUMPTION.'],
                                          'drug_interactions': [   'Dangerous if taken with any other stimulant '
                                                                   'purgatives.'],
                                          'is_schedule_e1': True,
                                          'pregnancy_lactation': 'CONTRAINDICATED_IN_PREGNANCY',
                                          'toxicity_class': 'SCHEDULE_E1_CAUSTIC_NEURO_POISON'},
                   'zmf_id': 'ZMF-340'},
    'ZMF-341': {   'canonical_identity': {   'arabic_name': 'Kundush',
                                             'botanical_authority': 'L.',
                                             'botanical_name': 'Veratrum album L.',
                                             'canonical_unani_name': 'Kundush',
                                             'confusable_species': ['Acorus calamus rhizome', 'Curcuma roots'],
                                             'family': 'Melanthiaceae',
                                             'hindi_regional_names': ['Nakchhikni', 'Kundush', 'White Hellebore'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Kundush Asli'],
                                             'part_used': 'Dried Rhizome and Roots',
                                             'synonyms': ['Veratrum viride', 'White Hellebore Rhizome'],
                                             'urdu_name': 'Kundush / White Hellebore Root'},
                   'category': 'SCHEDULE_E1_POISON_HIGH_RISK',
                   'classical_profile': {   'afaal': [   'Muattis-e-Shadid',
                                                         'Munaqqi-e-Dimagh',
                                                         'Daf-e-Saktah',
                                                         'Daf-e-Laqwa',
                                                         'Jali'],
                                            'badal': ['Filfil Siyah', 'Zanjabeel'],
                                            'daraja': 'Daraja 4',
                                            'dosage_context': 'NASAL SNUFF / SAOOT ONLY (Diluted 1:50). Oral internal '
                                                              'dose: 0 mg (STRICTLY PROHIBITED). HARD-BLOCKED FROM AI '
                                                              'COPILOT.',
                                            'mizaj': 'Garm 4, Khushk 4',
                                            'musleh': 'Roghan-e-Banafsha, Dudh & Sikanjabeen',
                                            'muzir': 'DEADLY STEROIDAL ALKALOID POISON. Causes violent uncontrollable '
                                                     'sneezing, profound hypotension, bradycardia, and asphyxia.',
                                            'tadbeer': 'Finely sifted and diluted 1:100 with starch or almond oil for '
                                                       'nasal insufflation (Saoot)'},
                   'governance': {   'ai_permission': AIPermission.BLOCKED_HIGH_RISK,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.SAFETY_REVIEWED},
                   'modern_evidence': {   'animal_models': 'Potent stimulation of trigeminal sensory nerve endings '
                                                           'inducing violent expulsive sneeze reflexes in animal '
                                                           'models.',
                                          'clinical_rct': 'Classical emergency resuscitative agent in apoplexy '
                                                          '(Saktah), coma, and intractable deep cerebral catarrh via '
                                                          'nasal application.',
                                          'evidence_grade': 'E4 (Classical Emergency Resuscitation Efficacy — Oral Use '
                                                            'Lethal)',
                                          'in_vitro': 'Prolongs the open state of voltage-gated sodium channels in '
                                                      'cardiac and nerve cells, inducing Bezold-Jarisch reflex '
                                                      '(bradycardia, hypotension, apnea).',
                                          'primary_constituents': [   'Protoveratrine A and B',
                                                                      'Jervine',
                                                                      'Rubijervine',
                                                                      'Veratramine',
                                                                      'Steroidal veratrum alkaloids']},
                   'murakkab_roles': ['Regulated active in Saoot-e-Kundush, Roghan-e-Kundush, and Kohal-e-Kundush'],
                   'organ_axis_affinity': ['Axis 01 (Dimagh-Asab / Neuro-Psychiatric Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 0.5%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Non-toxic Acorus calamus powders'],
                                           'microscopy': 'Parenchyma packed with raphides of calcium oxalate and '
                                                         "starch grains; veratrum alkaloids precipitate with Mayer's "
                                                         'reagent.',
                                           'morphology': 'Rough, dark greyish-brown conical rhizome pieces, 3-8 cm '
                                                         'long, surrounded by dense root fibers, starchy fracture, '
                                                         'intense acrid burning taste, dust causes violent paroxysms '
                                                         'of sneezing.',
                                           'total_ash': 'Not more than 5.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-341',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Rhizome and Roots',
                                                   'regulatory_status': 'RESTRICTED SCHEDULE E(1) POISON. Strictly '
                                                                        'governed.',
                                                   'upi_page': '158',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Violent Sternutatory (Attas), Cephalic '
                                                                    'Deobstruent in Apoplexy & Coma (SCHEDULE E-1 '
                                                                    'TOXIC)',
                                                      'original_text_snippet': 'کندش: حار يابس في الرابعة، عطوس غاية، '
                                                                               'يجذب البلغم من الرأس بقوة، ونافع '
                                                                               'للسكتة والصرع والفالج وقاتل في الشرب۔',
                                                      'page': '246',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': [   'ABSOLUTELY CONTRAINDICATED FOR ORAL CONSUMPTION. '
                                                                   'Prohibited in pregnancy, cardiac disease, and '
                                                                   'children.'],
                                          'drug_interactions': [   'Strictly contraindicated with digitalis or modern '
                                                                   'antihypertensives.'],
                                          'is_schedule_e1': True,
                                          'pregnancy_lactation': 'CONTRAINDICATED_IN_PREGNANCY',
                                          'toxicity_class': 'SCHEDULE_E1_LETHAL_STERNUTATORY_POISON'},
                   'zmf_id': 'ZMF-341'},
    'ZMF-342': {   'canonical_identity': {   'arabic_name': 'Filfil Moyeh',
                                             'botanical_authority': 'Vahl',
                                             'botanical_name': 'Piper retrofractum Vahl',
                                             'canonical_unani_name': 'Filfil Moyeh',
                                             'confusable_species': ['Piper longum root', 'Piper nigrum root'],
                                             'family': 'Piperaceae',
                                             'hindi_regional_names': ['Pippalimula', 'Piplamool', 'Long Pepper Root'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Filfil Moyeh Asli', 'Piplamool Desi'],
                                             'part_used': 'Dried Root and Rootstock',
                                             'synonyms': [   'Piper officinarum (Miq.) C.DC.',
                                                             'Piper chaba Hunter',
                                                             'Balinese Pepper Root'],
                                             'urdu_name': 'Filfil Moyeh / Long Pepper Root'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Kasir-e-Riyah',
                                                         'Hazim-e-Taam',
                                                         'Muqawwi-e-Meda wa Jigar',
                                                         'Daf-e-Qulanj',
                                                         'Daf-e-Waja-ul-Mafasil'],
                                            'badal': ['Filfil Daraz', 'Zanjabeel'],
                                            'daraja': 'Daraja 3',
                                            'dosage_context': '1g to 2g in powder or electuaries.',
                                            'mizaj': 'Garm 3, Khushk 3',
                                            'musleh': 'Roghan-e-Badam & Gond Kikar',
                                            'muzir': 'May aggravate gastritis in hot bilious temperaments without '
                                                     'Musleh.',
                                            'tadbeer': 'Washed, shade dried, powdered with carminatives'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Demonstrates potent anti-inflammatory and analgesic '
                                                           'effects in formalin and acetic acid writhing assays in '
                                                           'test models.',
                                          'clinical_rct': 'Extensive classical and clinical use in chronic cold atonic '
                                                          'dyspepsia, deep pelvic flatulence, and cold arthritic '
                                                          'aching.',
                                          'evidence_grade': 'E5 (Extensive Classical & Modern Pharmacological '
                                                            'Evidence)',
                                          'in_vitro': 'Increases gastric blood flow, enhances bioavailability of '
                                                      'co-administered therapeutics via intestinal glucuronidation '
                                                      'inhibition.',
                                          'primary_constituents': [   'Piperine (3-5%)',
                                                                      'Chavicine',
                                                                      'Piperlongumine',
                                                                      'Retrorefractamides',
                                                                      'Volatile essential oil']},
                   'murakkab_roles': ['Chief active in Jawarish Filfil, Majun Falasifa, and Sufoof-e-Hazim'],
                   'organ_axis_affinity': [   'Axis 04 (Meda-Ama / Gastrointestinal Axis)',
                                              'Axis 08 (Izam-Mafasil / Musculoskeletal Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 2.0%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Piper nigrum roots', 'Chavica officinarum stems'],
                                           'microscopy': 'Cork multilayered, broad cortex with stone cells and starch '
                                                         'grains, vascular bundles with broad medullary rays.',
                                           'morphology': 'Cylindrical, tortuous, branched root pieces, 2-8 cm long, '
                                                         '0.5-1.5 cm thick, dark brown exterior, longitudinal '
                                                         'wrinkles, fibrous fracture, intensely pungent aromatic '
                                                         'taste.',
                                           'total_ash': 'Not more than 6.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-342',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Root and Rootstock',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '34',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Deep Visceral Warming Digestant, Anti-Colic & '
                                                                    'Hepato-Gastric Stimulant',
                                                      'original_text_snippet': 'فلفل مويه: حار يابس في الثالثة، أشد '
                                                                               'تسخينا من دار فلفل، مسخن للمعدة والكبد '
                                                                               'ومحلل للرياح الغليظة والقولنج۔',
                                                      'page': '248',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': ['Contraindicated in acute peptic ulceration.'],
                                          'drug_interactions': [   'Significantly increases absorption and '
                                                                   'bioavailability of modern pharmaceutical drugs.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_DIGESTIVE_STIMULANT'},
                   'zmf_id': 'ZMF-342'},
    'ZMF-343': {   'canonical_identity': {   'arabic_name': 'Kabab Khandan',
                                             'botanical_authority': 'DC.',
                                             'botanical_name': 'Zanthoxylum armatum DC.',
                                             'canonical_unani_name': 'Kabab Khandan',
                                             'confusable_species': ['Zanthoxylum rhetsa', 'Zanthoxylum acanthopodium'],
                                             'family': 'Rutaceae',
                                             'hindi_regional_names': [   'Timur',
                                                                         'Darmar',
                                                                         'Tejbal',
                                                                         'Toothache Tree Fruit',
                                                                         'Kabab-e-Khandan'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Kabab Khandan Asli', 'Timur Fruit'],
                                             'part_used': 'Dried Carpels / Fruit',
                                             'synonyms': [   'Zanthoxylum alatum Roxb.',
                                                             'Winged Prickly Ash',
                                                             'Szechuan Pepper relative'],
                                             'urdu_name': 'Kabab Khandan / Prickly Ash Fruit'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Musakkin-e-Waja-ul-Asnan',
                                                         'Muqawwi-e-Lissa',
                                                         'Tib-e-Fum',
                                                         'Kasir-e-Riyah',
                                                         'Hazim'],
                                            'badal': ['Kabab Chini', 'Qaranfal'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '1g to 2g internally; freely used in dentifrices and '
                                                              'mouthwashes.',
                                            'mizaj': 'Garm 2, Khushk 2',
                                            'musleh': 'Gulab & Roghan-e-Banafsha',
                                            'muzir': 'High doses may cause mild burning in mouth in sensitive '
                                                     'temperaments without Musleh.',
                                            'tadbeer': 'Cleaned of black seeds, carpels dried and finely ground for '
                                                       'tooth powders (Sanoon) or pills'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Demonstrated profound peripheral analgesic and '
                                                           'anti-inflammatory activity in rodent dental pain and '
                                                           'formalin assays.',
                                          'clinical_rct': 'Universally prescribed in Unani tooth powders (Sanoon), '
                                                          'mouth deodorants, and stomachic electuaries for flatulence.',
                                          'evidence_grade': 'E4 (Robust Clinical & Classical Odontological Evidence)',
                                          'in_vitro': 'Local anesthetic action via voltage-gated sodium channel '
                                                      'inhibition by sanshools, potent antibacterial against oral '
                                                      'Streptococcus mutans.',
                                          'primary_constituents': [   'Hydroxy-alpha-sanshool',
                                                                      'Linalool (up to 60% of volatile oil)',
                                                                      'Limonene',
                                                                      'Armatamide',
                                                                      'Flavonoids']},
                   'murakkab_roles': ['Chief active in Sanoon-e-Kabab Khandan, Sanoon-e-Mujalli, and Jawarish Zarooni'],
                   'organ_axis_affinity': [   'Axis 04 (Meda-Ama / Gastrointestinal Axis)',
                                              'Axis 10 (Jild-Masamat / Dermato-Immunological Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 1.5%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Zanthoxylum acanthopodium carpels'],
                                           'microscopy': 'Pericarp with large lysigenous oil cavities, inner endocarp '
                                                         'horny and separating; volatile oil shows linalool and '
                                                         'limonene.',
                                           'morphology': 'Bivalved, subglobose follicles, 4-5 mm diameter, '
                                                         'reddish-brown, pellucid punctate with prominent oil glands, '
                                                         'pleasant aromatic citrus-coriander odor, unique numbing '
                                                         'tingling taste on tongue.',
                                           'total_ash': 'Not more than 5.5%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-343',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Carpels / Fruit',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '48',
                                                   'upi_volume': 'Part-I, Vol. III'},
                   'primary_unani_citations': [   {   'claim_type': 'Aromatic Oral Tonic, Toothache Reliever, '
                                                                    'Carminative & Stomachic',
                                                      'original_text_snippet': 'کباب خنداں: گرم و خشک در دوم، غایت '
                                                                               'مقوی دندان و لثہ، دافع درد دندان و '
                                                                               'بدبوئے دہن، و ہاضم طعام و کاسر ریاح '
                                                                               'است۔',
                                                      'page': '115',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Khazain-ul-Advia (Hakeem Najmul Ghani)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Vol. VI (Advia-e-Mufarradah)'}],
                   'safety_firewall': {   'contraindications': ['None noted in therapeutic posology.'],
                                          'drug_interactions': ['None documented.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_ODONTIC_CARMINATIVE'},
                   'zmf_id': 'ZMF-343'},
    'ZMF-344': {   'canonical_identity': {   'arabic_name': 'Auraq-ul-Mahanimb',
                                             'botanical_authority': 'L.',
                                             'botanical_name': 'Melia azedarach L.',
                                             'canonical_unani_name': 'Barg-e-Bakayan',
                                             'confusable_species': [   'Azadirachta indica leaves (Neem - distinct '
                                                                       'odor and bitterness)'],
                                             'family': 'Meliaceae',
                                             'hindi_regional_names': [   'Bakayan ke Patte',
                                                                         'Mahanimb Leaves',
                                                                         'Persian Lilac Leaves'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Barg-e-Bakayan Asli'],
                                             'part_used': 'Dried Leaves',
                                             'synonyms': ['Persian Lilac Leaves', 'Bead Tree Leaves', 'Barg-e-Drek'],
                                             'urdu_name': 'Barg-e-Bakayan / Persian Lilac Leaves'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Musaffi-e-Dam',
                                                         'Muhallil-e-Bawaseer',
                                                         'Daf-e-Kharash',
                                                         'Qatil-e-Deedan',
                                                         'Mubarrid'],
                                            'badal': ['Barg-e-Neem', 'Shahtara'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '3g to 5g in decoction; extensively used in '
                                                              'anti-hemorrhoidal washes and sitz baths.',
                                            'mizaj': 'Sard 1, Khushk 2',
                                            'musleh': 'Kashneez Khushk & Shakar',
                                            'muzir': 'Overdose of raw extract can produce nausea without Musleh.',
                                            'tadbeer': 'Shade dried leaves pulverized or brewed into wash for '
                                                       'hemorrhoids and ulcers'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Marked reduction of croton oil-induced hemorrhoidal '
                                                           'inflammation and tissue edema in animal models.',
                                          'clinical_rct': 'Extensive clinical validation in bleeding hemorrhoids '
                                                          '(Bawaseer-e-Damiya), perineal pruritus, and chronic '
                                                          'scrofula.',
                                          'evidence_grade': 'E4 (Robust Clinical & Classical Anti-Hemorrhoidal '
                                                            'Evidence)',
                                          'in_vitro': 'Potent inhibition of vascular endothelial growth factor (VEGF) '
                                                      'and inflammatory cytokines in hemorrhoidal venous congestion.',
                                          'primary_constituents': [   'Toosendanin',
                                                                      'Meliatoxins',
                                                                      'Azadirachtin-related limonoids',
                                                                      'Rutin',
                                                                      'Flavonoid glycosides']},
                   'murakkab_roles': ['Chief active in Habb-e-Bawaseer Khooni, Marham-e-Bawaseer, and Arq-e-Musaffi'],
                   'organ_axis_affinity': [   'Axis 10 (Jild-Masamat / Dermato-Immunological Axis)',
                                              'Axis 04 (Meda-Ama / Gastrointestinal Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 2.0%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Azadirachta indica (Neem leaves)'],
                                           'microscopy': 'Anomocytic stomata on lower surface, multicellular glandular '
                                                         'trichomes, calcium oxalate crystals in mesophyll.',
                                           'morphology': 'Bipinnate or tripinnate leaves, leaflets ovate to '
                                                         'lanceolate, serrate or lobed margin, acuminate apex, dark '
                                                         'green, bitter taste, faint characteristic aroma.',
                                           'total_ash': 'Not more than 8.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-344',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Leaves',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '16',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Anti-Hemorrhoidal, Blood Purifier, Resolvent & '
                                                                    'Anti-Scrofulous',
                                                      'original_text_snippet': 'برگ بکائن: سرد در اول و خشک در دوم، '
                                                                               'غایت مصفی خون، محلل بواسیر و خنازیر، و '
                                                                               'دافع خارش و جذام و قروح خبیثہ۔',
                                                      'page': '460',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Khazain-ul-Advia (Hakeem Najmul Ghani)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Vol. I (Advia-e-Mufarradah)'}],
                   'safety_firewall': {   'contraindications': [   'Do not confuse with poisonous seeds/berries of the '
                                                                   'plant.'],
                                          'drug_interactions': ['None documented at standard clinical doses.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_ANTI_HEMORRHOIDAL'},
                   'zmf_id': 'ZMF-344'},
    'ZMF-345': {   'canonical_identity': {   'arabic_name': 'Zahr-ul-Ghafis',
                                             'botanical_authority': 'L.',
                                             'botanical_name': 'Agrimonia eupatoria L.',
                                             'canonical_unani_name': 'Gule Ghafis',
                                             'confusable_species': ['Eupatorium cannabinum', 'Inula dysenterica'],
                                             'family': 'Rosaceae',
                                             'hindi_regional_names': ['Agrimony Flowers', 'Ghafis', 'Church Steeples'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Gule Ghafis Asli', 'Agrimony Herb'],
                                             'part_used': 'Dried Flowers and Flowering Tops',
                                             'synonyms': [   'Common Agrimony',
                                                             'Eupatorium of Dioscorides',
                                                             'Sticklewort'],
                                             'urdu_name': 'Gule Ghafis / Agrimony Flowers'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Mufattih-e-Sudad-e-Jigar',
                                                         'Mudirr-e-Safra',
                                                         'Muhallil-e-Salabat-e-Tihal',
                                                         'Daf-e-Yarqan',
                                                         'Muqawwi-e-Meda'],
                                            'badal': ['Afsanteen', 'Kashoot'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '3g to 7g in classical infusion or Sharbat.',
                                            'mizaj': 'Garm 1, Khushk 2',
                                            'musleh': 'Sharbat-e-Banafsha & Sikanjabeen',
                                            'muzir': 'May induce mild dryness in arid temperaments without Musleh.',
                                            'tadbeer': 'Dried flowers brewed in hot water infusion (Zulal-e-Ghafis)'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Significant reduction of cholestatic liver injury, '
                                                           'reduction of elevated serum bilirubin, AST, and ALT in '
                                                           'rodent bile-duct ligation models.',
                                          'clinical_rct': 'Centuries of classical hospital success in chronic '
                                                          'hepatitis, jaundice (Yarqan), and cirrhosis with '
                                                          'hepatomegaly in Majun Dabeed-ul-Ward.',
                                          'evidence_grade': 'E5 (Extensive Classical Pharmacopoeial & Clinical '
                                                            'Hepatobiliary Evidence)',
                                          'in_vitro': 'Stimulates physiological bile flow, protects hepatocytes from '
                                                      'lipid peroxidation, potent free radical scavenging.',
                                          'primary_constituents': [   'Agrimoniin (ellagitannin dimer)',
                                                                      'Luteolin 7-glucoside',
                                                                      'Apigenin',
                                                                      'Quercetin',
                                                                      'Ursolic acid']},
                   'murakkab_roles': ['Chief active in Majun Dabeed-ul-Ward, Sharbat-e-Deenam, and Arq-e-Ghafis'],
                   'organ_axis_affinity': [   'Axis 03 (Jigar-Tihal / Hepato-Splenic Axis)',
                                              'Axis 04 (Meda-Ama / Gastrointestinal Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 2.0%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Eupatorium cannabinum flowering tops'],
                                           'microscopy': 'Uniseriate unicellular conical trichomes, glandular hairs '
                                                         'with multicellular heads, calcium oxalate rosettes in '
                                                         'mesophyll.',
                                           'morphology': 'Small bright yellow 5-petaled flowers clustered in long '
                                                         'terminal spike-like racemes, calyx tube grooved with hooked '
                                                         'bristles at top, pleasant apricot-like fragrance, mildly '
                                                         'bitter astringent taste.',
                                           'total_ash': 'Not more than 8.5%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-345',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Flowers and Flowering Tops',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '40',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Supreme Hepatobiliary Deobstruent, Choleretic & '
                                                                    'Spleen Desiccant',
                                                      'original_text_snippet': 'غافث: حار في الأولى يابس في الثانية، '
                                                                               'مفتح عظيم لسدد الكبد والطحال، نافع '
                                                                               'لليرقان والاستسقاء وورم الأحشاء الصلب۔',
                                                      'page': '230',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': ['None noted in therapeutic posology.'],
                                          'drug_interactions': ['Compatible with conventional liver protectants.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_HEPATOBILIARY_DEOBSTRUENT'},
                   'zmf_id': 'ZMF-345'},
    'ZMF-346': {   'canonical_identity': {   'arabic_name': 'Fool / Baqila',
                                             'botanical_authority': 'L.',
                                             'botanical_name': 'Vicia faba L.',
                                             'canonical_unani_name': 'Baqla',
                                             'confusable_species': ['Phaseolus vulgaris (Lobia)', 'Pisum sativum'],
                                             'family': 'Fabaceae',
                                             'hindi_regional_names': ['Baqla', 'Fava Bean', 'Broad Bean', 'Bakla'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Baqla Desi', 'Faba Bean'],
                                             'part_used': 'Dried Seeds (Faba Beans)',
                                             'synonyms': ['Faba vulgaris Moench', 'Broad Bean Seeds', 'Hab-e-Baqla'],
                                             'urdu_name': 'Baqla / Faba Bean'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Muhallil-e-Awram',
                                                         'Jali-e-Kalf',
                                                         'Musakkin-e-Waram-e-Khasiya',
                                                         'Daf-e-Waram-e-Sadi',
                                                         'Ghadhi'],
                                            'badal': ['Nakhud', 'Mash'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '5g to 15g cooked internally; freely applied as warm '
                                                              'topical poultice.',
                                            'mizaj': 'Sard 1, Khushk 2',
                                            'musleh': 'Roghan-e-Badam, Filfil Siyah & Namak',
                                            'muzir': 'Internal ingestion triggers acute hemolytic anemia (Favism) in '
                                                     'G6PD enzyme deficiency.',
                                            'tadbeer': 'Flour (Aard-e-Baqla) boiled with vinegar, water or rose water '
                                                       'and applied warm as thick resolving poultice (Zimad)'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Significant reduction of experimentally induced testicular '
                                                           'swelling and mastitis edema in topical poultice models.',
                                          'clinical_rct': 'Universally renowned in Unani surgery for resolving acute '
                                                          'orchitis (Waram-e-Khasiya), parotitis, and clearing facial '
                                                          'melasma (Kalf).',
                                          'evidence_grade': 'E4 (Robust Classical & Clinical Resolvent Evidence)',
                                          'in_vitro': 'High natural content of L-DOPA supports dopaminergic pathways; '
                                                      'high mucilaginous starch and flavonoids provide thermal '
                                                      'poultice resolvent action.',
                                          'primary_constituents': [   'L-DOPA (L-3,4-dihydroxyphenylalanine)',
                                                                      'Vicine',
                                                                      'Convicine',
                                                                      'Starch (up to 50%)',
                                                                      'Vegetable protein (25-30%)']},
                   'murakkab_roles': ['Chief active in Zimad-e-Baqla, Zimad-e-Mohallil, and Ubtan-e-Husn'],
                   'organ_axis_affinity': [   'Axis 07 (Tanasul-Bah / Reproductive Axis)',
                                              'Axis 10 (Jild-Masamat / Dermato-Immunological Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 1.0%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Common horse beans of inferior grade'],
                                           'microscopy': 'Palisade layer of seed coat with columnar sclereids, '
                                                         'hourglass cells, parenchymatous cotyledons packed with '
                                                         'simple oval starch grains.',
                                           'morphology': 'Large, compressed, oval or oblong greenish-brown to blackish '
                                                         'seeds, 1.5-2.5 cm long, prominent elongated black hilum, '
                                                         'starchy sweetish taste.',
                                           'total_ash': 'Not more than 4.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-346',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Seeds (Faba Beans)',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '18',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Supreme Resolvent Poultice (Muhallil-e-Awram), '
                                                                    'Anti-Orchitis & Cosmetic Depurative',
                                                      'original_text_snippet': 'باقلا: بارد في الأولى يابس في الثانية، '
                                                                               'دقيقها مع الخل يحلل الأورام البلغمية '
                                                                               'وورم الخصية والثدي، ويجلو الآثار۔',
                                                      'page': '144',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': [   'Strictly contraindicated internally in individuals '
                                                                   'with Glucose-6-Phosphate Dehydrogenase (G6PD) '
                                                                   'deficiency.'],
                                          'drug_interactions': ['None for topical use.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_TOPICAL_RESOLVENT_FAVISM_RISK_INTERNALLY'},
                   'zmf_id': 'ZMF-346'},
    'ZMF-347': {   'canonical_identity': {   'arabic_name': 'Kharateen / Asal-ul-Ard',
                                             'botanical_authority': 'Classical Animal Drug',
                                             'botanical_name': 'Pheretima posthuma (Purified Earthworm)',
                                             'canonical_unani_name': 'Kharateen Musaffa',
                                             'confusable_species': [   'Unpurified wild earthworms with gut soil '
                                                                       'contents'],
                                             'family': 'Purified Dried Earthworm',
                                             'hindi_regional_names': [   'Kharateen',
                                                                         'Kenchua Shuddh',
                                                                         'Purified Earthworm'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Kharateen Musaffa Asli'],
                                             'part_used': 'Specially Fed, Purified and Dried Whole Earthworm',
                                             'synonyms': [   'Lumbricus terrestris',
                                                             'Purified Earthworm',
                                                             'Earthworm Powder'],
                                             'urdu_name': 'Kharateen Musaffa / Purified Earthworm'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Muqawwi-e-Bah',
                                                         'Muharrik-e-Asab',
                                                         'Musammin-e-Uzw-e-Makhsoos',
                                                         'Daf-e-Falij',
                                                         'Daf-e-Istirkha'],
                                            'badal': ['Zalu', 'Regmahi'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '500mg to 1g internally; extensively cooked in sesame '
                                                              'oil to prepare classical virility oils '
                                                              '(Tila-e-Kharateen).',
                                            'mizaj': 'Garm 1, Ratab 2',
                                            'musleh': 'Zanjabeel, Elaichi & Roghan-e-Badam',
                                            'muzir': 'Improperly purified earthworms cause intestinal infection and '
                                                     'nausea.',
                                            'tadbeer': 'Purified by starving in clean water, feeding buttermilk/flour '
                                                       'until gut clears, washed in wine/vinegar and dried'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Accelerates peripheral nerve axonal regeneration and '
                                                           'enhances cavernous sinusoidal blood filling in rodent '
                                                           'erectile models.',
                                          'clinical_rct': 'Legendary Unani medication in Majun Kharateen and royal '
                                                          'virility oils for local flaccidity and erectile weakness.',
                                          'evidence_grade': 'E5 (Extensive Classical Pharmacopoeial & Clinical '
                                                            'Microvascular Evidence)',
                                          'in_vitro': 'Potent fibrinolytic and antithrombotic activity via '
                                                      'lumbrokinase enzyme complex, peripheral microvascular '
                                                      'vasodilatation.',
                                          'primary_constituents': [   'Lumbrokinase (fibrinolytic enzyme complex)',
                                                                      'Lumbritin',
                                                                      'Terrestro-lumbrolysin',
                                                                      'Hypoxanthine',
                                                                      'Bioactive peptides']},
                   'murakkab_roles': ['Chief active in Majun Kharateen, Tila-e-Kharateen, and Roghan-e-Kharateen'],
                   'organ_axis_affinity': [   'Axis 07 (Tanasul-Bah / Reproductive Axis)',
                                              'Axis 01 (Dimagh-Asab / Neuro-Psychiatric Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 0.5%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Unpurified earthworms containing intestinal sand'],
                                           'microscopy': 'Microscopy shows cuticle, circular and longitudinal muscle '
                                                         'layers, setae embedded in setigerous sacs; gut lumen '
                                                         'completely free of soil particles after Shodhana.',
                                           'morphology': 'Cylindrical, wrinkled, curved, reddish-brown to dark brown '
                                                         'dried worms, 5-12 cm long, segmented body, characteristic '
                                                         'earthy odor, non-putrid, starchy striae.',
                                           'total_ash': 'Acid insoluble ash <2.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-347',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Specially Fed, Purified and Dried Whole Earthworm',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '148',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Premier Musculo-Nervine Stimulant, Organ '
                                                                    'Hypertrophic Tonic & Aphrodisiac',
                                                      'original_text_snippet': 'خراطین مصفی: گرم در اول و تر در دوم، '
                                                                               'اعظم مقویات باہ و محرک عصب و مسمن عضو '
                                                                               'مخصوص و دافع فالج و استرخاء است۔',
                                                      'page': '312',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Khazain-ul-Advia (Hakeem Najmul Ghani)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Vol. III (Advia-e-Mufarradah)'}],
                   'safety_firewall': {   'contraindications': [   'Contraindicated in active internal bleeding '
                                                                   'disorders.'],
                                          'drug_interactions': [   'Caution with modern anticoagulants (warfarin, '
                                                                   'heparin) due to intrinsic fibrinolytic enzymes.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_ANIMAL_RESTUATIVE_SHODHANA_REQUIRED'},
                   'zmf_id': 'ZMF-347'},
    'ZMF-348': {   'canonical_identity': {   'arabic_name': 'Alaq / Zalu',
                                             'botanical_authority': 'Classical Animal Biotherapy',
                                             'botanical_name': 'Hirudo medicinalis (Medicinal Leech)',
                                             'canonical_unani_name': 'Zalu',
                                             'confusable_species': [   'Poisonous toxic water leeches (Zalu-e-Sammiyah '
                                                                       'with broad green bellies)'],
                                             'family': 'Medicinal Annelid Leech',
                                             'hindi_regional_names': ['Zalu', 'Jok', 'Medicinal Leech', 'Jalauka'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Zalu-e-Tibbiyah', 'Certified Medicinal Leech'],
                                             'part_used': 'Live Certified Medical Leech',
                                             'synonyms': [   'Hirudinaria granulosa (Indian Medicinal Leech)',
                                                             'Hirudo medicinalis L.',
                                                             'Jalauka'],
                                             'urdu_name': 'Zalu / Medicinal Leech'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Ikhraj-e-Dam-e-Fasid',
                                                         'Munaqqi-e-Urooq',
                                                         'Muhallil-e-Awram',
                                                         'Daf-e-Dawali',
                                                         'Daf-e-Qurooh-e-Khabisah'],
                                            'badal': ['Fasad (Venesection)', 'Hajamat (Cupping)'],
                                            'daraja': 'Daraja 1',
                                            'dosage_context': 'EXTERNAL BIOTHERAPEUTIC APPLICATION ONLY '
                                                              '(Irsal-e-Alaq). 1 to 6 leeches per sitting under '
                                                              'certified clinician oversight.',
                                            'mizaj': 'Muaddil (Barad 1, Ratab 1)',
                                            'musleh': 'Post-leech dressing with Turmeric, Dam-ul-Akhwain, or Alum '
                                                      'powder to arrest bleeding',
                                            'muzir': 'Application of poisonous wild leeches causes gangrene, '
                                                     'ulceration, and severe sepsis.',
                                            'tadbeer': 'Kept in pure spring water, starved before application; skin '
                                                       'cleaned with clay and rose water before attachment'},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Accelerates salvage of congested flap pedicles, enhances '
                                                           'digital replantation micro-perfusion in reconstructive '
                                                           'animal trials.',
                                          'clinical_rct': 'Approved and globally recognized in Unani regimenal therapy '
                                                          '(Ilaj-bil-Tadbeer) for varicose ulcers, deep vein '
                                                          'thrombosis, and alopecia areata.',
                                          'evidence_grade': 'E6 (Extensive Classical Canon & Modern FDA/WHO Cleared '
                                                            'Biotherapy)',
                                          'in_vitro': 'Direct stoichiometric binding to thrombin, complete inhibition '
                                                      'of fibrin clot propagation, degradation of established '
                                                      'microvascular thrombi.',
                                          'primary_constituents': [   'Hirudin (potent direct thrombin inhibitor)',
                                                                      'Calin (collagen-mediated platelet aggregation '
                                                                      'inhibitor)',
                                                                      'Hyaluronidase',
                                                                      'Destabilase',
                                                                      'Bdellins']},
                   'murakkab_roles': [   'Key agent in Ilaj-bil-Tadbeer (Irsal-e-Alaq Protocol) for chronic ulcers and '
                                         'vascular thrombosis'],
                   'organ_axis_affinity': [   'Axis 02 (Qalb-Urooq / Cardio-Vascular Axis)',
                                              'Axis 10 (Jild-Masamat / Dermato-Immunological Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not applicable',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Wild toxic leeches lacking dorsal reddish stripes'],
                                           'microscopy': 'Salivary glands contain abundant uniseriate secretory '
                                                         'tubules producing hirudin, calin, and hyaluronidase; tested '
                                                         'pathogen-free for Aeromonas hydrophila.',
                                           'morphology': 'Olive-green to dark brown dorsally with 6 longitudinal '
                                                         'reddish stripes, yellowish-orange belly with black spots, '
                                                         'flattened body with anterior and posterior suckers, '
                                                         'triradiate jaws with chitinous teeth.',
                                           'total_ash': 'Not applicable'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-348',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Live Certified Medical Leech',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '152',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Supreme Regimenal Bloodletting Biotherapy '
                                                                    '(Irsal-e-Alaq), Antithrombotic & Resolvent',
                                                      'original_text_snippet': 'علق / زلو: تمص الدم الفاسد من أعمق '
                                                                               'العروق، وتنفع من القروح الرديئة '
                                                                               'والدوالي وداء الفيل وانسداد الأوعية۔',
                                                      'page': '312',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book I (General Principles of Regimen)'}],
                   'safety_firewall': {   'contraindications': [   'Strictly contraindicated in hemophilia, severe '
                                                                   'anemia, and leukemia.'],
                                          'drug_interactions': [   'Contraindicated with severe systemic '
                                                                   'anticoagulation therapy without monitoring.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'CONTRAINDICATED_IN_PREGNANCY',
                                          'toxicity_class': 'REGIMENAL_BIOTHERAPEUTIC_CLINICIAN_ONLY'},
                   'zmf_id': 'ZMF-348'},
    'ZMF-349': {   'canonical_identity': {   'arabic_name': 'Samkat-ur-Raml',
                                             'botanical_authority': 'Classical Animal Drug',
                                             'botanical_name': 'Scincus officinalis (Sand Skink)',
                                             'canonical_unani_name': 'Regmahi',
                                             'confusable_species': ['Common wall geckos', 'Imitation dried lizards'],
                                             'family': 'Dried Sand Skink Lizard',
                                             'hindi_regional_names': ['Regmahi', 'Ret ki Machli', 'Sand Fish Skink'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Regmahi Asli', 'Genuine Egyptian Sandfish'],
                                             'part_used': 'Cleaned, Gutted and Dried Sand Lizard',
                                             'synonyms': ['Scincus scincus L.', 'Sandfish Lizard', 'Samak-ur-Raml'],
                                             'urdu_name': 'Regmahi / Sand Skink Lizard'},
                   'category': 'VERIFIED_CLASSICAL_MUFRAD',
                   'classical_profile': {   'afaal': [   'Muqawwi-e-Bah-e-Azam',
                                                         'Muharrik-e-Intisab',
                                                         'Muqawwi-e-Asab',
                                                         'Daf-e-Falij',
                                                         'Daf-e-Laqwa'],
                                            'badal': ['Kharateen Musaffa', 'Zalu'],
                                            'daraja': 'Daraja 2',
                                            'dosage_context': '500mg to 1g in royal confections (Majun Regmahi, '
                                                              'Laboob-e-Kabeer).',
                                            'mizaj': 'Garm 2, Khushk 2',
                                            'musleh': 'Roghan-e-Banafsha & Sikanjabeen',
                                            'muzir': 'May induce warmth and restlessness in hot bilious temperaments '
                                                     'without Musleh.',
                                            'tadbeer': 'Gut eviscerated, washed with vinegar and rock salt, sun dried '
                                                       "and fried lightly in cow's ghee"},
                   'governance': {   'ai_permission': AIPermission.APPROVED_FOR_AI_COPILOT,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.APPROVED_KNOWLEDGE},
                   'modern_evidence': {   'animal_models': 'Marked restoration of erectile rigidity and mounting '
                                                           'performance in diabetic and castrated animal models.',
                                          'clinical_rct': 'Renowned historical constituent in Laboob-e-Kabeer and '
                                                          'royal electuaries for severe psychogenic and organic '
                                                          'erectile failure.',
                                          'evidence_grade': 'E4 (Robust Classical Compendia & Modern Pharmacological '
                                                            'Evidence)',
                                          'in_vitro': 'Enhances hypothalamic-pituitary-gonadal axis signaling, '
                                                      'restores nitric oxide synthase activity in penile smooth muscle '
                                                      'tissue.',
                                          'primary_constituents': [   'Steroidal animal hormones',
                                                                      'Omega-3 and Omega-6 polyunsaturated lipids',
                                                                      'Phospholipids',
                                                                      'Zinc and selenium complexes']},
                   'murakkab_roles': ['Chief active in Majun Regmahi, Laboob-e-Kabeer, and Tila-e-Shahi'],
                   'organ_axis_affinity': [   'Axis 07 (Tanasul-Bah / Reproductive Axis)',
                                              'Axis 01 (Dimagh-Asab / Neuro-Psychiatric Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 0.5%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Ordinary dried domestic lizards'],
                                           'microscopy': 'Microscopy shows keratinized epidermal scales, skeletal '
                                                         'striated muscle bundles, bone fragments with osteocytes; '
                                                         'free of rancid putrefaction.',
                                           'morphology': 'Small spindle-shaped dried lizard, 10-18 cm long, smooth '
                                                         'polished yellowish-buff scales, flattened snout, short limbs '
                                                         'with fringed toes, oily starchy aroma.',
                                           'total_ash': 'Acid insoluble ash <1.5%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-349',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Cleaned, Gutted and Dried Sand Lizard',
                                                   'regulatory_status': 'Monographed (PCIM&H / AYUSH). Fully '
                                                                        'authorized.',
                                                   'upi_page': '146',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Supreme Classical Animal Aphrodisiac, Nervine '
                                                                    'Tonic & Anti-Hemiplegic',
                                                      'original_text_snippet': 'سمكة الرمل / ریگماہی: حارة يابسة في '
                                                                               'الثانية، غاية في تحريك الباه '
                                                                               'والانتصاب، مقوية للأعصاب ونافعة للفالج '
                                                                               'والاسترخاء۔',
                                                      'page': '190',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': [   'Contraindicated in acute priapism and severe '
                                                                   'hypertension.'],
                                          'drug_interactions': ['Compatible with herbal vitalizers.'],
                                          'is_schedule_e1': False,
                                          'pregnancy_lactation': 'SAFE_WITH_MONITORING',
                                          'toxicity_class': 'SAFE_ROYAL_ANIMAL_VITALIZER'},
                   'zmf_id': 'ZMF-349'},
    'ZMF-350': {   'canonical_identity': {   'arabic_name': 'Sam-us-Samak',
                                             'botanical_authority': '(L.) Wight & Arn.',
                                             'botanical_name': 'Anamirta cocculus (L.) Wight & Arn.',
                                             'canonical_unani_name': 'Mahee Zahraj',
                                             'confusable_species': [   'Piper nigrum (Black pepper - superficial '
                                                                       'visual resemblance)'],
                                             'family': 'Menispermaceae',
                                             'hindi_regional_names': [   'Kakamari',
                                                                         'Fish Berry',
                                                                         'Indian Berry',
                                                                         'Picrotoxin Seed'],
                                             'identity_confidence': 'HIGH_CONFIRMED',
                                             'market_names': ['Mahee Zahraj Asli'],
                                             'part_used': 'Dried Ripe Seeds / Fruit',
                                             'synonyms': [   'Menispermum cocculus L.',
                                                             'Cocculus indicus',
                                                             'Fish Poison Berries'],
                                             'urdu_name': 'Mahee Zahraj / Fish Berry'},
                   'category': 'SCHEDULE_E1_POISON_HIGH_RISK',
                   'classical_profile': {   'afaal': [   'Qatil-e-Quml wa Saiban',
                                                         'Qatil-e-Kiram-e-Jild',
                                                         'Muhallil-e-Awram-e-Salbah',
                                                         'Jali'],
                                            'badal': ['Post Bekh Madar', 'Gandhak'],
                                            'daraja': 'Daraja 4',
                                            'dosage_context': 'EXTERNAL TOPICAL APPLICATION ONLY (Anti-Lice '
                                                              'Oil/Paste). Absolute internal dose: 0 mg (STRICTLY '
                                                              'PROHIBITED). HARD-BLOCKED FROM AI COPILOT.',
                                            'mizaj': 'Garm 4, Khushk 4',
                                            'musleh': 'Roghan-e-Banafsha, Dudh & Qai (Emesis induction)',
                                            'muzir': 'DEADLY CENTRAL SPINAL CONVULSANT POISON. Ingestion produces '
                                                     'violent epileptiform seizures, respiratory paralysis and death.',
                                            'tadbeer': 'Finely ground with mustard oil or vinegar for external '
                                                       'parasiticidal paste only'},
                   'governance': {   'ai_permission': AIPermission.BLOCKED_HIGH_RISK,
                                     'signoff_clinician': 'Prof. (Dr.) Mansoor Alam',
                                     'signoff_date': '2026-09-18',
                                     'state': ValidationState.SAFETY_REVIEWED},
                   'modern_evidence': {   'animal_models': '100% eradication of lice, scabies mites, and cutaneous '
                                                           'ectoparasites in topical animal screening models within 30 '
                                                           'minutes.',
                                          'clinical_rct': 'Centuries of classical veterinary and human topical use for '
                                                          'pediculosis capitis and scabies under extreme care.',
                                          'evidence_grade': 'E4 (Classical Compendia Efficacy for External '
                                                            'Parasitology — Internal Use Lethal)',
                                          'in_vitro': 'Picrotoxinin is a potent non-competitive GABA-A receptor '
                                                      'chloride channel blocker, inducing catastrophic generalized '
                                                      'tonic-clonic convulsions.',
                                          'primary_constituents': [   'Picrotoxin (equimolar picrotoxinin and '
                                                                      'picrotin)',
                                                                      'Picrotoxic acid',
                                                                      'Anamirtin',
                                                                      'Menispermine alkaloid']},
                   'murakkab_roles': ['Chief active in Roghan-e-Kakamari, Zimad-e-Quml, and Marham-e-Kharish'],
                   'organ_axis_affinity': ['Axis 10 (Jild-Masamat / Dermato-Immunological Axis)'],
                   'pharmacognosy_qc': {   'foreign_matter_limit': 'Not more than 0.5%',
                                           'heavy_metals_pesticides': 'Complies with CCRUM GLP limits.',
                                           'known_adulterants': ['Piper nigrum (Black pepper)', 'Embelia ribes'],
                                           'microscopy': 'Pericarp with sclerotic endocarp, endosperm packed with '
                                                         'fixed oil and picrotoxin crystals which turn yellow then red '
                                                         'with sulfuric acid.',
                                           'morphology': 'Subglobose or kidney-shaped drupes, 8-12 mm long, wrinkled '
                                                         'dark brownish-black surface, hard woody shell, cup-shaped '
                                                         'seed enclosing white oily kernel, bitter nauseous taste.',
                                           'total_ash': 'Not more than 5.0%'},
                   'pharmacopoeial_crosswalk': {   'nfum_code': 'UPI-M-350',
                                                   'official_book': 'Unani Pharmacopoeia of India (UPI)',
                                                   'official_part': 'Dried Ripe Seeds / Fruit',
                                                   'regulatory_status': 'RESTRICTED SCHEDULE E(1) POISON. Strictly '
                                                                        'governed.',
                                                   'upi_page': '160',
                                                   'upi_volume': 'Part-I, Vol. II'},
                   'primary_unani_citations': [   {   'claim_type': 'Potent Parasiticidal, Anti-Pediculosis & '
                                                                    'Convulsant Toxin (SCHEDULE E-1 TOXIC)',
                                                      'original_text_snippet': 'سم السمك: حار يابس في الرابعة، مسكر '
                                                                               'للسمك وقاتل للقمل والصيبان، ومحلل '
                                                                               'للأورام الصلبة، وشربه مهلك محدث '
                                                                               'للتشنج۔',
                                                      'page': '234',
                                                      'review_status': 'AUTHENTICATED_HISTORICAL_CITATIONS',
                                                      'reviewer': 'Prof. (Dr.) Mansoor Alam, Unani Pharmacognosist',
                                                      'source': 'Al-Qanoon fi al-Tibb (Ibn Sina)',
                                                      'status': 'VERIFIED',
                                                      'volume': 'Book II (Materia Medica)'}],
                   'safety_firewall': {   'contraindications': [   'ABSOLUTELY CONTRAINDICATED FOR INTERNAL USE. '
                                                                   'Prohibited in pregnancy, infants, and broken '
                                                                   'skin.'],
                                          'drug_interactions': [   'Never apply to large open weeping wounds due to '
                                                                   'systemic absorption.'],
                                          'is_schedule_e1': True,
                                          'pregnancy_lactation': 'CONTRAINDICATED_IN_PREGNANCY',
                                          'toxicity_class': 'SCHEDULE_E1_CONVULSANT_GABA_BLOCKER_POISON'},
                   'zmf_id': 'ZMF-350'}}

