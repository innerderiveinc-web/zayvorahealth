"""
ZAYVORA Health OS™ - Comprehensive Pharmacopoeia & Single Drugs Reference
Reference: ZAYVORA Pharmacopoeia Parts 1 (A-M) & 2 (N-Z),
Dr. Irfan Ashraf, BUMS (Ajmal Khan Tibbiya College, AMU).

Codifies 50+ classical Unani single drugs (Mufradat) and modern bioactives:
  - Classical Unani Parameters: Mizaj (Kaifiyyat & Darjat 1-4), Classical Afaal
  - Tadbir (Purification/Processing requirements)
  - Modern Pharmacodynamics & Mechanism of Action
  - Formulation Role, Musleh (Corrective), and Products Used In
"""

from typing import Dict, Any, List, Optional

MONOGRAPHS: Dict[str, Dict[str, Any]] = {
    # ==================== PART 1: A - M ====================
    "AJWAIN_DESI": {
        "key": "AJWAIN_DESI",
        "unani_name": "Ajwain Desi (اجوائن دیسی)",
        "botanical_name": "Trachyspermum ammi L.",
        "english_name": "Carom Seeds / Bishop's Weed",
        "family": "Apiaceae",
        "part_used": "Seeds (Tukhm)",
        "mizaj": {"heat": 3, "dryness": 2, "description": "Har 3, Yabis 2 (Hot in 3rd degree, Dry in 2nd degree)"},
        "afaal": ["Hazim (Digestive)", "Daf-e-Nafakh (Carminative)", "Mufattih-e-Sudad (Deobstruent)", "Muhallil-e-Warama (Anti-inflammatory)", "Muqawwi-e-Meda (Stomach strengthener)", "Mudir-e-Baul (Diuretic)"],
        "pharmacodynamics": "Thymol (35-60%) inhibits L-type Ca2+ channels in intestinal smooth muscle; carminative surface tension reduction; antimicrobial and Nrf2 hepatoprotective.",
        "why_essential": "Digestive catalyst in complex formulas. Warming and drying nature counters heavy, moist nutritive herbs (Salab, Musli).",
        "products_used_in": ["GutBalance", "MetaboBurn-M", "MetaReset", "ZV-F-02"],
        "tadbir": "None required; clean and dry storage"
    },
    "AKHROT_MAGHZ": {
        "key": "AKHROT_MAGHZ",
        "unani_name": "Akhrot Maghz (اخروٹ مغز)",
        "botanical_name": "Juglans regia L.",
        "english_name": "Walnut Kernel",
        "family": "Juglandaceae",
        "part_used": "Kernel (Maghz)",
        "mizaj": {"heat": 2, "moisture": 1, "description": "Har 2, Ratab 1 (Hot in 2nd degree, Moist in 1st degree)"},
        "afaal": ["Muqawwi-e-Dimagh (Brain tonic)", "Muqawwi-e-Aasab (Nerve strengthener)", "Muqawwi-e-Baah (Aphrodisiac)", "Muwalid-e-Mani (Spermatogenic)", "Mufarrih (Exhilarant)"],
        "pharmacodynamics": "Rich in ALA omega-3 fatty acids, polyphenols, and vitamin E; protects neurons from oxidative stress; improves sperm membrane lipid architecture.",
        "why_essential": "Simultaneously strengthens the Brain-Genital axis (Dimagh to Azae Tanasul); calms performance anxiety while supporting nerve conduction.",
        "products_used_in": ["NightOne X", "Qurs-e-Taqwiyat-e-Mani PRO", "Men Daily"],
        "tadbir": "Fresh cold-press or unheated kernel"
    },
    "AMLA": {
        "key": "AMLA",
        "unani_name": "Amla (آملہ)",
        "botanical_name": "Emblica officinalis Gaertn. / Phyllanthus emblica L.",
        "english_name": "Indian Gooseberry",
        "family": "Phyllanthaceae",
        "part_used": "Fruit (dried)",
        "mizaj": {"cold": 1, "dryness": 2, "description": "Barid 1, Yabis 2 (Cold in 1st degree, Dry in 2nd degree)"},
        "afaal": ["Muqawwi-e-Dimagh", "Muqawwi-e-Qalb", "Muqawwi-e-Meda", "Daf-e-Hararat (Heat reducer)", "Muhallil-e-Warama", "Qabiz (Astringent)", "Musleh (Universal corrective)"],
        "pharmacodynamics": "Richest natural ascorbic acid source (450-900 mg/100g) plus emblicanin A & B; protects sperm DNA from oxidative fragmentation; Nrf2 inducer.",
        "why_essential": "Mandatory universal thermal Musleh for hot-dry agents (Guggul, Aqarqarha). Shields sperm DNA from testicular heat stress.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "ThyroMet-W", "OvaBalance PRO", "JointEase PRO"],
        "tadbir": "Seed removed; dried deseeded pericarp powdered"
    },
    "AQARQARHA": {
        "key": "AQARQARHA",
        "unani_name": "Aqarqarha (عاقرقرحا)",
        "botanical_name": "Anacyclus pyrethrum DC.",
        "english_name": "Pellitory Root",
        "family": "Asteraceae",
        "part_used": "Root (Beekh)",
        "mizaj": {"heat": 4, "dryness": 3, "description": "Har 4, Yabis 3 (Hot in 4th degree, Dry in 3rd degree - Highest Thermal Intensity)"},
        "afaal": ["Muhrik-e-Baah (Potent aphrodisiac stimulant)", "Muqawwi-e-Aasab", "Muharrik-e-Dimagh", "Jallab (Attracts blood flow / Vasodilator)"],
        "pharmacodynamics": "Alkamides (pellitorine) stimulate TRPV1/TRPA1 channels, inducing endothelial nitric oxide synthase (eNOS) and cavernosal blood flow.",
        "why_essential": "Most potent natural cavernosal vasodilator in Unani. Absolute ceiling of 200mg/day; mandatory pairing with Tabasheer and Sandal Safaid.",
        "products_used_in": ["NightOne X", "Qurs-e-Taqwiyat-e-Mani PRO (Barid Mizaj only)"],
        "tadbir": "Ethanolic extraction (60%) standardized to pellitorine; strict thermal correction mandatory"
    },
    "ARJUNA": {
        "key": "ARJUNA",
        "unani_name": "Arjuna (ارجن)",
        "botanical_name": "Terminalia arjuna (Roxb.) Wight & Arn.",
        "english_name": "Arjuna Bark",
        "family": "Combretaceae",
        "part_used": "Bark (Post)",
        "mizaj": {"cold": 1, "dryness": 2, "description": "Barid 1, Yabis 2 (Cold in 1st degree, Dry in 2nd degree)"},
        "afaal": ["Muqawwi-e-Qalb (Cardiotonic)", "Qabiz (Astringent)", "Habis-e-Dam (Hemostatic)", "Daf-e-Dard-e-Qalb", "Musakkin"],
        "pharmacodynamics": "Arjunolic acid and arjunosides improve myocardial calcium handling and contractility without digitalis-like toxicity; upregulates endothelial nitric oxide.",
        "why_essential": "Cardiovascular anchor for hypertensive and stress-cardiac presentations; prevents performance-related palpitations.",
        "products_used_in": ["CardioCalm", "NightOne X", "Men Daily"],
        "tadbir": "Standardized to minimum 1% arjunosides by HPLC"
    },
    "ASGANDH": {
        "key": "ASGANDH",
        "unani_name": "Asgandh Nagauri (اسگند ناگوری)",
        "botanical_name": "Withania somnifera (L.) Dunal",
        "english_name": "Ashwagandha / Indian Ginseng",
        "family": "Solanaceae",
        "part_used": "Root (Beekh)",
        "mizaj": {"heat": 2, "dryness": 2, "description": "Har 2, Yabis 2 (Hot in 2nd degree, Dry in 2nd degree)"},
        "afaal": ["Muqawwi-e-Badani", "Muqawwi-e-Aasab", "Muqawwi-e-Baah", "Muwalid-e-Mani", "Musakkin-e-Aasab", "Mufarrih"],
        "pharmacodynamics": "Withanolides (withaferin A, withanolide A) downregulate hypothalamic CRH, reducing cortisol by 14-32%; upregulates hippocampal BDNF; Leydig 17b-HSD stimulation.",
        "why_essential": "Master adaptogen and HPA-HPG axis stabilizer. Rebuilds hippocampal glucocorticoid receptors damaged by chronic cortisol.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "Sleep+Stress PRO", "ThyroMet-W", "OvaBalance PRO"],
        "tadbir": "Nagori root standardized to minimum 5% withanolides (KSM-66 spec)"
    },
    "BADAM_MAGHZ": {
        "key": "BADAM_MAGHZ",
        "unani_name": "Badam Maghz Shirin (بادام مغز شیریں)",
        "botanical_name": "Prunus dulcis / Prunus amygdalus",
        "english_name": "Sweet Almond Kernel",
        "family": "Rosaceae",
        "part_used": "Kernel (Maghz)",
        "mizaj": {"heat": 1, "moisture": 2, "description": "Har 1, Ratab 2 (Hot in 1st degree, Moist in 2nd degree)"},
        "afaal": ["Muqawwi-e-Dimagh", "Muqawwi-e-Basar", "Muqawwi-e-Mani", "Mulayyin", "Ballistik (Nutritive)"],
        "pharmacodynamics": "High alpha-tocopherol, monounsaturated fats, and magnesium; provides lipid membrane substrate for myelin and spermatozoa.",
        "why_essential": "Represents Madda-e-Mani (raw semen substrate) without generating inflammatory heat; nourishing lipid carrier.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "Men Daily", "Women Daily"],
        "tadbir": "Sweet variety only (bitter Prunus amygdalus var. amara prohibited due to amygdalin cyanide risk)"
    },
    "BEHMAN_SAFAID": {
        "key": "BEHMAN_SAFAID",
        "unani_name": "Behman Safaid (بہمن سفید)",
        "botanical_name": "Centaurea behen L.",
        "english_name": "White Behmen Root",
        "family": "Asteraceae",
        "part_used": "Root (Beekh)",
        "mizaj": {"heat": 1, "moisture": 2, "description": "Har 1, Ratab 2 (Hot in 1st degree, Moist in 2nd degree)"},
        "afaal": ["Muqawwi-e-Baah", "Muqawwi-e-Azae Tanasul", "Muwalid-e-Mani", "Mubarrid", "Mufattih"],
        "pharmacodynamics": "Sesquiterpene lactones support testicular basement membrane and Sertoli cell nutrition; enhances hepatic cholesterol delivery to Leydig cells.",
        "why_essential": "Primary structural Muwalid-e-Mani herb providing the cellular matrix for spermatogenesis in severe oligospermia.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "NightOne X"],
        "tadbir": "4:1 concentrated root extract"
    },
    "BEHMAN_SURKH": {
        "key": "BEHMAN_SURKH",
        "unani_name": "Behman Surkh (بہمن سرخ)",
        "botanical_name": "Salvia haematodes Wall.",
        "english_name": "Red Behmen Root",
        "family": "Lamiaceae",
        "part_used": "Root (Beekh)",
        "mizaj": {"heat": 1, "moisture": 2, "description": "Har 1, Ratab 2 (Hot in 1st degree, Moist in 2nd degree)"},
        "afaal": ["Muqawwi-e-Qalb", "Muqawwi-e-Baah", "Muqawwi-e-Mani", "Mufarrih", "Ballistik"],
        "pharmacodynamics": "Cardiotonic polyphenols and salvianolic acid derivatives improve genital microvascular perfusion and reduce cardiac fatigue.",
        "why_essential": "Paired 1:1 with Behman Safaid to create perfect thermal balance and reinforce the heart-gonadal connection.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "NightOne X"],
        "tadbir": "4:1 concentrated root extract"
    },
    "BEEJ_KAUNCH": {
        "key": "BEEJ_KAUNCH",
        "unani_name": "Beej Kaunch (بیج کانچ)",
        "botanical_name": "Mucuna pruriens (L.) DC.",
        "english_name": "Cowhage / Velvet Bean",
        "family": "Fabaceae",
        "part_used": "Seeds (Beej)",
        "mizaj": {"heat": 2, "moisture": 1, "description": "Har 2, Ratab 1 (Hot in 2nd degree, Moist in 1st degree)"},
        "afaal": ["Muqawwi-e-Baah", "Muwalid-e-Mani", "Muqawwi-e-Aasab", "Mufarrih", "Ballistik"],
        "pharmacodynamics": "Contains 4-7% natural L-DOPA; crosses blood-brain barrier to synthesize dopamine; inhibits pituitary prolactin release, freeing testosterone synthesis.",
        "why_essential": "Addresses the neurochemical basis of libido (dopaminergic drive) rather than simple vascular arousal; proven sperm count multiplier.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "NightOne X", "Men Daily"],
        "tadbir": "Seed coat removed (peeled) to eliminate irritating trichomes"
    },
    "BHRINGRAJ": {
        "key": "BHRINGRAJ",
        "unani_name": "Bhringraj (بھرنگراج)",
        "botanical_name": "Eclipta alba (L.) Hassk.",
        "english_name": "False Daisy",
        "family": "Asteraceae",
        "part_used": "Whole plant (aerial parts)",
        "mizaj": {"cold": 1, "moisture": 1, "description": "Barid 1, Ratab 1 (Cold in 1st degree, Moist in 1st degree)"},
        "afaal": ["Munbit-e-Sha'r (Hair growth promoter)", "Daf-e-Tasaqqut-e-Sha'r", "Muqawwi-e-Sha'r", "Muswid-e-Sha'r", "Muqawwi-e-Kabid"],
        "pharmacodynamics": "Wedelolactone competitively inhibits 5-alpha reductase type II in hair follicle dermal papilla; promotes anagen phase transition comparable to Minoxidil 2%.",
        "why_essential": "Gold standard for androgenetic and telogen alopecia; simultaneously cleanses hepatic metabolic waste affecting follicular health.",
        "products_used_in": ["HairRevive System", "Roghan Bhringraj"],
        "tadbir": "Standardized to minimum 0.5% wedelolactone by HPLC"
    },
    "BRAHMI": {
        "key": "BRAHMI",
        "unani_name": "Brahmi (برہمی)",
        "botanical_name": "Bacopa monnieri (L.) Wettst.",
        "english_name": "Water Hyssop / Bacopa",
        "family": "Plantaginaceae",
        "part_used": "Whole plant (aerial parts)",
        "mizaj": {"cold": 1, "moisture": 1, "description": "Barid 1, Ratab 1 (Cold in 1st degree, Moist in 1st degree)"},
        "afaal": ["Muqawwi-e-Dimagh", "Muqawwi-e-Hafiza (Memory enhancer)", "Musakkin", "Daf-e-Waswasa (Anti-anxiety)", "Mubarrid"],
        "pharmacodynamics": "Bacosides A & B upregulate hippocampal BDNF and NGF expression; reversible AChE inhibition; antioxidant neuroprotection via Nrf2.",
        "why_essential": "Builds structural neural reserve and synaptic density over 8-12 weeks; non-sedating cognitive and anxiolytic stabilizer.",
        "products_used_in": ["NeuroClear", "Sleep+Stress PRO", "ThyroMet-W"],
        "tadbir": "Standardized to minimum 20% bacosides (must not be confused with Centella asiatica)"
    },
    "FILFIL_SIYAH": {
        "key": "FILFIL_SIYAH",
        "unani_name": "Filfil Siyah (فلفل سیاہ)",
        "botanical_name": "Piper nigrum L.",
        "english_name": "Black Pepper",
        "family": "Piperaceae",
        "part_used": "Dried fruit (peppercorn)",
        "mizaj": {"heat": 3, "dryness": 2, "description": "Har 3, Yabis 2 (Hot in 3rd degree, Dry in 2nd degree)"},
        "afaal": ["Hazim", "Mufattih", "Muhallil", "Muharrik", "Daf-e-Balgham", "Jallab (Bioavailability catalyst)"],
        "pharmacodynamics": "Piperine (5-10%) reversibly inhibits hepatic CYP3A4 and intestinal P-glycoprotein; increases curcumin absorption by 2,000% and withanolides by 40%.",
        "why_essential": "Universal bioavailability enhancer in the 80/20 formula architecture. Maximum dose ceiling 20mg/day.",
        "products_used_in": ["ViriMax-M", "ThyroMet-W", "JointEase PRO", "LivClear PRO", "MetaReset"],
        "tadbir": "Fine grinding; standardized to 5-10% piperine"
    },
    "GILOY": {
        "key": "GILOY",
        "unani_name": "Giloy / Gilo (گلو)",
        "botanical_name": "Tinospora cordifolia (Willd.) Miers",
        "english_name": "Heart-leaved Moonseed / Guduchi",
        "family": "Menispermaceae",
        "part_used": "Stem (Saaq)",
        "mizaj": {"heat": 1, "dryness": 1, "description": "Har 1, Yabis 1 (Hot in 1st degree, Dry in 1st degree - near Mutadil)"},
        "afaal": ["Muqawwi-e-Tabiyat", "Daf-e-Humma (Anti-pyretic)", "Muhallil-e-Warama", "Muqawwi-e-Kabid", "Hazim"],
        "pharmacodynamics": "Cordifolioside and tinosporaside modulate macrophage phagocytosis and normalize Th1/Th2 balance; reduces Anti-TPO antibodies in Hashimoto's.",
        "why_essential": "Premier immunomodulator that supports Tabiyat without overstimulating autoimmune flares.",
        "products_used_in": ["ImmunoGuard", "ThyroMet-W (Hashimoto overlay)", "OvaBalance PRO"],
        "tadbir": "Aqueous starch extraction (Sat-e-Gilo)"
    },
    "GOKHRU": {
        "key": "GOKHRU",
        "unani_name": "Gokhru (گوکھرو)",
        "botanical_name": "Tribulus terrestris L.",
        "english_name": "Puncture Vine / Small Caltrops",
        "family": "Zygophyllaceae",
        "part_used": "Fruit (Tukhm)",
        "mizaj": {"heat": 1, "moisture": 1, "description": "Har 1, Ratab 1 (Hot in 1st degree, Moist in 1st degree)"},
        "afaal": ["Mudirr-e-Baul (Diuretic)", "Mufattit-e-Hisat (Stone disintegrator)", "Muqawwi-e-Baah", "Muqawwi-e-Azae Tanasul"],
        "pharmacodynamics": "Protodioscin increases pituitary LH pulsatility, stimulating endogenous testosterone; potassium-sparing aquaretic flushing urinary micro-calculi.",
        "why_essential": "Dual-action urogenital bridge: simultaneously addresses renal stone formation and testicular androgen output.",
        "products_used_in": ["StoneGuard", "Qurs-e-Taqwiyat-e-Mani PRO", "Men Daily"],
        "tadbir": "Standardized to minimum 40% saponins"
    },
    "GUGGUL": {
        "key": "GUGGUL",
        "unani_name": "Guggul Shuddh (گگل شدہ)",
        "botanical_name": "Commiphora wightii / Commiphora mukul",
        "english_name": "Indian Bdellium",
        "family": "Burseraceae",
        "part_used": "Purified oleo-gum resin (Samaghe Maghsool)",
        "mizaj": {"heat": 2, "dryness": 2, "description": "Har 2, Yabis 2 (Hot in 2nd degree, Dry in 2nd degree)"},
        "afaal": ["Muhallil-e-Shahm (Fat dissolver)", "Muhallil-e-Warama", "Mufattih-e-Sudad", "Muqawwi-e-Ghudad (Glandular/Thyroid tonic)"],
        "pharmacodynamics": "E- and Z-guggulsterones act as FXR antagonists and PPAR-alpha/gamma agonists; upregulates hepatic deiodinase (T4 to T3); inhibits NF-kB.",
        "why_essential": "Premier metabolic and thyroid resolvent for Balgham accumulation, insulin resistance, and PCOS.",
        "products_used_in": ["ThyroMet-W", "OvaBalance PRO", "MetaReset", "JointEase PRO"],
        "tadbir": "MANDATORY Shuddhi: 12-hour Triphala decoction soak, filtration of insoluble irritant resin acids, concentration <60°C"
    },
    "GULNAAR": {
        "key": "GULNAAR",
        "unani_name": "Gulnaar (گلنار)",
        "botanical_name": "Punica granatum L. (flower)",
        "english_name": "Pomegranate Flower",
        "family": "Lythraceae",
        "part_used": "Dried flower (Gul)",
        "mizaj": {"cold": 2, "dryness": 2, "description": "Barid 2, Yabis 2 (Cold in 2nd degree, Dry in 2nd degree)"},
        "afaal": ["Qabiz (Astringent)", "Habis-e-Dam (Hemostatic)", "Muqawwi-e-Meda", "Hifz-e-Mani (Semen preserver)"],
        "pharmacodynamics": "High punicalagins and gallic acid exert astringent vasoconstriction; reduces seminal viscosity and excessive seminal emission.",
        "why_essential": "Embodies Hifz-e-Mani: ensures proper retention and consistency of newly generated semen without overheating.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "FemCare-L"],
        "tadbir": "Shade dried intact petals"
    },
    "GURMAR": {
        "key": "GURMAR",
        "unani_name": "Gurmar Booti (گرمار بوٹی)",
        "botanical_name": "Gymnema sylvestre (Retz.) R. Br.",
        "english_name": "Sugar Destroyer",
        "family": "Apocynaceae",
        "part_used": "Leaves (Barg)",
        "mizaj": {"heat": 1, "dryness": 2, "description": "Har 1, Yabis 2 (Hot in 1st degree, Dry in 2nd degree)"},
        "afaal": ["Daf-e-Ziabetus (Anti-diabetic)", "Qabiz-e-Quwwa", "Mudhhib-e-Sukkar (Sugar eliminator)"],
        "pharmacodynamics": "Gymnemic acids competitively bind taste receptors on tongue and SGLT-1 intestinal transporters; regenerates pancreatic beta cells.",
        "why_essential": "Eliminates behavioral sugar cravings and reduces intestinal glucose absorption in pre-diabetes and metabolic syndrome.",
        "products_used_in": ["MetaReset", "Sugar Care", "MetaboBurn-M"],
        "tadbir": "Standardized to minimum 25% gymnemic acids by HPLC"
    },
    "HALDI": {
        "key": "HALDI",
        "unani_name": "Haldi / Zard Choob (ہلدی / زرد چوب)",
        "botanical_name": "Curcuma longa L.",
        "english_name": "Turmeric",
        "family": "Zingiberaceae",
        "part_used": "Rhizome",
        "mizaj": {"heat": 2, "dryness": 2, "description": "Har 2, Yabis 2 (Hot in 2nd degree, Dry in 2nd degree)"},
        "afaal": ["Muhallil-e-Warama (Anti-inflammatory)", "Daf-e-Tashannuj", "Muqawwi-e-Kabid", "Musaffi-e-Dam", "Jaali (Cleansing)"],
        "pharmacodynamics": "Curcuminoids inhibit NF-kB, COX-2, and 5-LOX; potent Nrf2 antioxidant activator. Requires piperine or phytosome delivery.",
        "why_essential": "Universal anti-inflammatory anchor for joints, NAFLD, and systemic inflammation.",
        "products_used_in": ["JointEase PRO", "LivClear PRO", "ImmunoGuard"],
        "tadbir": "Phytosome (Meriva) formulation or co-administration with Piperine mandatory"
    },
    "JATAMANSI": {
        "key": "JATAMANSI",
        "unani_name": "Jatamansi / Sumbul-ut-Teeb (جٹامانسی)",
        "botanical_name": "Nardostachys jatamansi (D.Don) DC.",
        "english_name": "Spikenard",
        "family": "Caprifoliaceae",
        "part_used": "Rhizome / Root",
        "mizaj": {"heat": 1, "dryness": 2, "description": "Har 1, Yabis 2 (Hot in 1st degree, Dry in 2nd degree - mild warming)"},
        "afaal": ["Musakkin-e-Dimagh", "Munawwim (Sleep inducer)", "Muqawwi-e-Qalb", "Daf-e-Khafqan (Palpitations)", "Muhallil-e-Sauda"],
        "pharmacodynamics": "Jatamansone and nardosinone act as positive allosteric modulators at GABA-A receptors; reversible MAO-A inhibition; reduces nocturnal cortisol.",
        "why_essential": "Primary non-habit-forming sleep and neuro-calming agent; enables safe benzodiazepine and zolpidem tapering.",
        "products_used_in": ["Sleep+Stress PRO", "NeuroCalm-S", "NightOne X"],
        "tadbir": "CITES Appendix II compliant sourcing; standardized to 0.8% nardosinone"
    },
    "JAMUN_BEEJ": {
        "key": "JAMUN_BEEJ",
        "unani_name": "Jamun Beej (جامن بیج)",
        "botanical_name": "Syzygium cumini (L.) Skeels",
        "english_name": "Java Plum Seed",
        "family": "Myrtaceae",
        "part_used": "Seed kernel (Tukhm Maghz)",
        "mizaj": {"cold": 2, "dryness": 2, "description": "Barid 2, Yabis 2 (Cold in 2nd degree, Dry in 2nd degree)"},
        "afaal": ["Daf-e-Ziabetus", "Qabiz", "Habis-e-Ishaal", "Daf-e-Atash (Thirst quencher)"],
        "pharmacodynamics": "Jamboline and ellagic acid inhibit alpha-glucosidase, retarding starch-to-glucose conversion; reduces diabetic oxidative stress.",
        "why_essential": "King of anti-diabetic seeds in Unani medicine; cooling nature balances hot diabetic metabolic patterns.",
        "products_used_in": ["MetaReset", "Sugar Care"],
        "tadbir": "Dried seed kernel finely pulverized to 100 mesh"
    },
    "KARELA": {
        "key": "KARELA",
        "unani_name": "Karela (کریلا)",
        "botanical_name": "Momordica charantia L.",
        "english_name": "Bitter Gourd / Bitter Melon",
        "family": "Cucurbitaceae",
        "part_used": "Fruit (dried)",
        "mizaj": {"cold": 2, "dryness": 2, "description": "Barid 2, Yabis 2 (Cold in 2nd degree, Dry in 2nd degree)"},
        "afaal": ["Daf-e-Ziabetus", "Musaffi-e-Dam", "Muqawwi-e-Meda", "Muhallil-e-Warama"],
        "pharmacodynamics": "Charantin, vicine, and polypeptide-p function as plant-based insulin mimetics; stimulates GLUT4 translocation and glycogen synthesis.",
        "why_essential": "Powerful postprandial glucose regulator; bitter principles stimulate digestive secretion without heating.",
        "products_used_in": ["MetaReset", "Sugar Care"],
        "tadbir": "Thin sliced fruit shade-dried and powdered"
    },
    "KULTHI": {
        "key": "KULTHI",
        "unani_name": "Kulthi Dal (کلتھی دال)",
        "botanical_name": "Macrotyloma uniflorum (Lam.) Verdc.",
        "english_name": "Horse Gram",
        "family": "Fabaceae",
        "part_used": "Seeds (Dal/Tukhm)",
        "mizaj": {"heat": 2, "dryness": 2, "description": "Har 2, Yabis 2 (Hot in 2nd degree, Dry in 2nd degree)"},
        "afaal": ["Mufattit-e-Hisat (Primary stone breaker)", "Mudirr-e-Baul", "Muhallil", "Daf-e-Warm-e-Kulyah"],
        "pharmacodynamics": "Potent inhibitor of calcium oxalate crystal nucleation and growth; high phenolic content reduces Tamm-Horsfall protein aggregation.",
        "why_essential": "Gold standard classical lithotropic agent; single most effective herb for calcium oxalate metaphylaxis.",
        "products_used_in": ["StoneGuard", "UroClear"],
        "tadbir": "20g boiled in 500mL water to 300mL decoction (Joshanda)"
    },
    "LODHRA": {
        "key": "LODHRA",
        "unani_name": "Lodhra (لودھرا)",
        "botanical_name": "Symplocos racemosa Roxb.",
        "english_name": "Lodh Tree Bark",
        "family": "Symplocaceae",
        "part_used": "Bark (Post)",
        "mizaj": {"cold": 2, "dryness": 2, "description": "Barid 2, Yabis 2 (Cold in 2nd degree, Dry in 2nd degree)"},
        "afaal": ["Qabiz", "Habis-e-Sail-ur-Reham (Stops leucorrhoea)", "Muqawwi-e-Reham (Uterine tonic)", "Mudirr-e-Tams"],
        "pharmacodynamics": "Symposide and loturine restore healthy ovarian estrogen/progesterone balance; astringent action tones relaxed pelvic and uterine tissue.",
        "why_essential": "Premier female uterine tonic for leucorrhoea, menorrhagia, and pelvic tissue relaxation.",
        "products_used_in": ["FemCare-L", "WomanVitality", "ThyroMet-W"],
        "tadbir": "Dried stem bark extraction"
    },
    "METHI": {
        "key": "METHI",
        "unani_name": "Methi Dana (میتھی دانا)",
        "botanical_name": "Trigonella foenum-graecum L.",
        "english_name": "Fenugreek Seeds",
        "family": "Fabaceae",
        "part_used": "Seeds (Tukhm)",
        "mizaj": {"heat": 2, "dryness": 1, "description": "Har 2, Yabis 1 (Hot in 2nd degree, Dry in 1st degree)"},
        "afaal": ["Muqawwi-e-Baah", "Daf-e-Ziabetus", "Muhallil-e-Warama", "Mulayyin", "Mujaffif"],
        "pharmacodynamics": "4-hydroxyisoleucine stimulates glucose-dependent insulin secretion; galactomannan soluble fibre blunts glucose & LPS intestinal absorption.",
        "why_essential": "Dual metabolic-hormonal keystone: upregulates hepatic SHBG, lowers free androgens in PCOS, and sensitizes insulin receptors.",
        "products_used_in": ["OvaBalance PRO", "MetaReset", "ThyroMet-W", "ZV-F-02"],
        "tadbir": "Mild roasting shifts Mizaj slightly towards Yabis for Balgham patients; standardized to 50% 4-HI"
    },
    "MULETHI": {
        "key": "MULETHI",
        "unani_name": "Mulethi / Aslus-Soos (ملٹھی / اصل السوس)",
        "botanical_name": "Glycyrrhiza glabra L.",
        "english_name": "Licorice Root",
        "family": "Fabaceae",
        "part_used": "Root (Beekh)",
        "mizaj": {"heat": 1, "moisture": 2, "description": "Har 1, Ratab 2 (Hot in 1st degree, Moist in 2nd degree - soothing)"},
        "afaal": ["Mulayyin-e-Sadr (Chest expectorant)", "Daf-e-Suaal (Cough suppressant)", "Muqawwi-e-Meda", "Mufarrih", "Mubarrid"],
        "pharmacodynamics": "Glycyrrhizin inhibits 11-beta-HSD, prolonging endogenous cortisol half-life in adrenal exhaustion; mucoprotective prostaglandin stimulation.",
        "why_essential": "Respiratory mucosal demulcent and HPA adrenal burnout supporter; soothing corrector in harsh formulas.",
        "products_used_in": ["LungClear", "ImmunoGuard", "CardioCalm"],
        "tadbir": "DGL (deglycyrrhizinated) form used where hypertension or sodium retention is a concern"
    },
    "MUSLI_SAFED": {
        "key": "MUSLI_SAFED",
        "unani_name": "Musli Safed (موصلی سفید)",
        "botanical_name": "Chlorophytum borivilianum Santapau & R.R. Fern.",
        "english_name": "White Musli",
        "family": "Asparagaceae",
        "part_used": "Root tubers (Beekh)",
        "mizaj": {"heat": 1, "moisture": 2, "description": "Har 1, Ratab 2 (Hot in 1st degree, Moist in 2nd degree)"},
        "afaal": ["Muqawwi-e-Baah Shadeed", "Muwalid-e-Mani", "Muqawwi-e-Mani", "Ballistik", "Muqawwi-e-Badani"],
        "pharmacodynamics": "Borivilianosides and steroidal saponins enhance testosterone synthesis and spermatogenesis; increases semen volume and sperm count.",
        "why_essential": "King of aphrodisiac nutritive herbs (Ballistik); builds reproductive tissue without causing heat or dryness.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "NightOne X", "Men Daily"],
        "tadbir": "Peeled dried tubers; fine pulverization"
    },

    # ==================== PART 2: N - Z ====================
    "PIPPALI": {
        "key": "PIPPALI",
        "unani_name": "Pippali / Filfil Daraz (فلفل دراز)",
        "botanical_name": "Piper longum L.",
        "english_name": "Long Pepper",
        "family": "Piperaceae",
        "part_used": "Dried fruit spikes",
        "mizaj": {"heat": 3, "dryness": 2, "description": "Har 3, Yabis 2 (Hot in 3rd degree, Dry in 2nd degree)"},
        "afaal": ["Hazim", "Muhallil", "Mufattih", "Munaffis", "Muhrik"],
        "pharmacodynamics": "High piperine and piperlongumine content; thermogenic beta-3 agonist; reverses multi-drug resistance by inhibiting P-glycoprotein.",
        "why_essential": "Drives deep tissue penetration and bioavailability for metabolic formulas.",
        "products_used_in": ["NightOne X", "MetaboBurn-M", "ViriMax-M"],
        "tadbir": "Coarse to fine grinding under cool temperature"
    },
    "PODINA": {
        "key": "PODINA",
        "unani_name": "Podina Khushk (پودینہ خشک)",
        "botanical_name": "Mentha arvensis / Mentha piperita",
        "english_name": "Dried Mint / Peppermint",
        "family": "Lamiaceae",
        "part_used": "Leaves",
        "mizaj": {"heat": 2, "moisture": 2, "description": "Har 2, Ratab 2 (Hot in 2nd degree, Moist in 2nd degree)"},
        "afaal": ["Hazim", "Daf-e-Riyah", "Mufattih", "Muhallil"],
        "pharmacodynamics": "Menthol inhibits L-type voltage-gated calcium channels in intestinal smooth muscle, producing rapid antispasmodic action.",
        "why_essential": "Rome IV-endorsed first-line natural intervention for IBS bloating and visceral hypersensitivity.",
        "products_used_in": ["GutBalance", "GutEase-IBS", "MetaboBurn-M"],
        "tadbir": "Enteric encapsulation for lower bowel delivery"
    },
    "PUNARNAVA": {
        "key": "PUNARNAVA",
        "unani_name": "Punarnava (پُنرنوا)",
        "botanical_name": "Boerhavia diffusa L.",
        "english_name": "Spreading Hogweed",
        "family": "Nyctaginaceae",
        "part_used": "Whole plant / Root",
        "mizaj": {"heat": 1, "dryness": 1, "description": "Har 1, Yabis 1 (Hot in 1st degree, Dry in 1st degree)"},
        "afaal": ["Mudirr-e-Baul (Diuretic)", "Muhallil", "Muqawwi-e-Jigar", "Mubarrid"],
        "pharmacodynamics": "Boeravinones and punarnavine inhibit Na+/K+-ATPase pump; promotes natriuresis without potassium wasting; anti-fibrotic hepatoprotection.",
        "why_essential": "Resolves myxoedema and facial puffiness in hypothyroidism and clears peritoneal/ovarian edema in PCOS.",
        "products_used_in": ["ThyroMet-W", "StoneGuard", "OvaBalance PRO", "LivClear PRO"],
        "tadbir": "Standardized to 2.5% boeravinones"
    },
    "SALAB_MISRI": {
        "key": "SALAB_MISRI",
        "unani_name": "Salab Misri (ثعلب مصری)",
        "botanical_name": "Orchis mascula / Eulophia campestris",
        "english_name": "Salep Orchid Tuber",
        "family": "Orchidaceae",
        "part_used": "Dried tubers",
        "mizaj": {"heat": 2, "moisture": 2, "description": "Har 2, Ratab 2 (Hot in 2nd degree, Moist in 2nd degree - thermally balanced)"},
        "afaal": ["Muqawwi-e-Mani", "Muwalid-e-Mani", "Ballistik", "Ghizai (Nutritive substrate)"],
        "pharmacodynamics": "Glucomannans (40-50%) and orchinol provide direct nutritional substrate for Sertoli and Leydig cells; increases semen volume and density.",
        "why_essential": "The single most important classical Unani reproductive tonic (Mughadhi foundation for sperm generation).",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "NightOne X", "Fertility Formula-M"],
        "tadbir": "Tuber dried and pulverized to fine mesh; stored <15% humidity"
    },
    "SANDAL_SAFAID": {
        "key": "SANDAL_SAFAID",
        "unani_name": "Sandal Safaid (صندل سفید)",
        "botanical_name": "Santalum album L.",
        "english_name": "White Sandalwood",
        "family": "Santalaceae",
        "part_used": "Heartwood",
        "mizaj": {"cold": 2, "dryness": 2, "description": "Barid 2, Yabis 2 (Cold in 2nd degree, Dry in 2nd degree)"},
        "afaal": ["Qabiz", "Mubarrid (Cooling)", "Musakkin", "Mufarrih-e-Qalb"],
        "pharmacodynamics": "Alpha-santalol acts as a 5-HT1A partial agonist and central nervous system sedative; reduces cardiac palpitations and Hararat.",
        "why_essential": "Essential cooling corrector for nervous palpitations and formula overheating; protects cardiac tissue.",
        "products_used_in": ["CardioCalm", "NightOne X", "StoneGuard"],
        "tadbir": "Fine wood powder or cold water infusion"
    },
    "SANG_E_YAHUD": {
        "key": "SANG_E_YAHUD",
        "unani_name": "Sang-e-Yahud (سنگ یہود)",
        "botanical_name": "Lapis Judaicus (Purified Fossil Encrinite / Calcium Phosphate)",
        "english_name": "Jew's Stone",
        "family": "Mineral",
        "part_used": "Purified calcined mineral",
        "mizaj": {"cold": 3, "dryness": 3, "description": "Barid 3, Yabis 3 (Cold in 3rd degree, Dry in 3rd degree)"},
        "afaal": ["Mufattit-e-Hisat (Stone-breaker)", "Mudirr-e-Baul", "Muhallil"],
        "pharmacodynamics": "Competitively substitutes for oxalate in calcium crystal lattices; shifts urinary pH to inhibit calcium oxalate aggregation.",
        "why_essential": "Premier classical mineral lithotriptic for disintegrating renal calculi.",
        "products_used_in": ["StoneGuard", "UroClear"],
        "tadbir": "MANDATORY Tadbir: 40-day oxidation, trituration in Kulthi decoction until completely non-gritty"
    },
    "SAUNF": {
        "key": "SAUNF",
        "unani_name": "Saunf / Badiyan (سونف / بادیان)",
        "botanical_name": "Foeniculum vulgare Mill.",
        "english_name": "Fennel Seed",
        "family": "Apiaceae",
        "part_used": "Seeds (Tukhm)",
        "mizaj": {"heat": 2, "moisture": 2, "description": "Har 2, Ratab 2 (Hot in 2nd degree, Moist in 2nd degree)"},
        "afaal": ["Hazim", "Daf-e-Riyah", "Mulayyin", "Muhallil", "Mufarrih"],
        "pharmacodynamics": "Trans-anethole relaxes intestinal smooth muscle via Ca2+ channel modulation; mild estrogenic displacement on thyroid-binding globulin.",
        "why_essential": "Digestive Musleh that prevents bloating in high-dose botanical protocols; improves GI transit.",
        "products_used_in": ["ThyroMet-W", "GutBalance", "MetaboBurn-M"],
        "tadbir": "Pharmaceutical-grade essential oil or fresh coarse seed powder"
    },
    "SHATAVARI": {
        "key": "SHATAVARI",
        "unani_name": "Shatavari / Satawar (ستاّور)",
        "botanical_name": "Asparagus racemosus Willd.",
        "english_name": "100-Root Asparagus",
        "family": "Asparagaceae",
        "part_used": "Root tubers",
        "mizaj": {"cold": 1, "moisture": 3, "description": "Barid 1, Ratab 3 (Cold in 1st degree, Moist in 3rd degree - highly nutritive)"},
        "afaal": ["Muqawwi-e-Reham (Uterine tonic)", "Ghizai", "Mulayyin", "Muqawwi-e-Baah Niswan", "Mudir-e-Laban"],
        "pharmacodynamics": "Shatavarin I-IV modulate estrogen receptors alpha & beta; soothes inflamed ovarian stroma; improves LH:FSH ratio.",
        "why_essential": "Foundational female reproductive trophorestorative; nourishes follicular maturation without androgen spikes.",
        "products_used_in": ["OvaBalance PRO", "WomanVitality", "Women Daily"],
        "tadbir": "Standardized to minimum 20% saponins"
    },
    "SHILAJIT": {
        "key": "SHILAJIT",
        "unani_name": "Shilajit / Salajeet (سلاجیت)",
        "botanical_name": "Asphaltum punjabianum",
        "english_name": "Purified Mineral Pitch",
        "family": "Mineral-Organic Complex",
        "part_used": "Purified exudate",
        "mizaj": {"heat": 2, "dryness": 2, "description": "Har 2, Yabis 2 (Hot in 2nd degree, Dry in 2nd degree)"},
        "afaal": ["Muqawwi-e-Badani", "Rasayan", "Muqawwi-e-Mani", "Muqawwi-e-Quwwa"],
        "pharmacodynamics": "Fulvic acid (60-80%) chelates essential minerals and transports them across mitochondrial membranes; boosts Complex I-III ATP production.",
        "why_essential": "Mitochondrial spark plug for asthenozoospermia and chronic fatigue; synergizes with CoQ10.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "Men Daily", "Stamina Builder"],
        "tadbir": "MANDATORY Shodhana: Aqueous dissolution, filtration, heavy metal chelation to <3 ppm total (Pb, Hg, As, Cd)"
    },
    "TABASHEER": {
        "key": "TABASHEER",
        "unani_name": "Tabasheer / Banslochan (طباشیر)",
        "botanical_name": "Bambusa arundinacea (Retz.) Willd.",
        "english_name": "Bamboo Silica Manna",
        "family": "Poaceae",
        "part_used": "Siliceous concretion inside bamboo stems",
        "mizaj": {"cold": 3, "dryness": 3, "description": "Barid 3, Yabis 3 (Cold in 3rd degree, Dry in 3rd degree)"},
        "afaal": ["Muhaffiz-e-Mani (Semen guardian)", "Mubarrid (Cooling)", "Qabiz", "Muqawwi-e-Qalb"],
        "pharmacodynamics": "Biogenic silica (SiO2 70-90%) with high thermal conductivity; dissipates scrotal heat and shields mitochondrial DNA from hydroxyl radicals.",
        "why_essential": "The ultimate thermal buffer against testicular hyperthermia (laptop heat, sitting) and oxidative sperm DNA fragmentation.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "ThyroMet-W", "JointEase PRO"],
        "tadbir": "Triple water washing, drying at 40°C, sieving to 80 mesh; XRF verification of SiO2 >80%"
    },
    "ZAFRAN": {
        "key": "ZAFRAN",
        "unani_name": "Zafran / Kesar (زعفران)",
        "botanical_name": "Crocus sativus L.",
        "english_name": "Saffron Stigma",
        "family": "Iridaceae",
        "part_used": "Dried stigmas",
        "mizaj": {"heat": 2, "dryness": 1, "description": "Har 2, Yabis 1 (Hot in 2nd degree, Dry in 1st degree)"},
        "afaal": ["Mufarrih-e-Qalb (Supreme exhilarant)", "Muqawwi-e-Dimagh", "Muqawwi-e-Baah", "Muhrik"],
        "pharmacodynamics": "Crocin and safranal inhibit serotonin and dopamine reuptake; stimulates cavernosal eNOS; improves IIEF scores and mood.",
        "why_essential": "Dual-action dopamine sexual motivator and antidepressant; micro-dosed at 10-30mg daily for safe efficacy.",
        "products_used_in": ["NightOne X", "Sleep+Stress PRO", "CardioCalm"],
        "tadbir": "ISO 3632 Grade 1 certified stigmas only; HPLC authentication for crocin >3.5%"
    },

    # ==================== MODERN NUTRACEUTICALS ====================
    "COQ10": {
        "key": "COQ10",
        "unani_name": "Jauhar-e-Hayat (Mitochondrial Coenzyme Q10)",
        "botanical_name": "Ubiquinol / Ubiquinone",
        "english_name": "Coenzyme Q10",
        "family": "Nutraceutical Bioactive",
        "part_used": "Fermented crystalline ubiquinol",
        "mizaj": {"heat": 1, "moisture": 1, "description": "Har 1, Ratab 1 (Warm-Moist / Anabolic energy equivalent)"},
        "afaal": ["Muqawwi-e-Quwwa (Energy tonic)", "Muhaffiz-e-Mani (Mitochondrial antioxidant)"],
        "pharmacodynamics": "Essential cofactor in electron transport chain Complex I & II; drives ATP generation for sperm flagellar motility; lipid peroxyl radical scavenger.",
        "why_essential": "Reverses asthenozoospermia (low sperm motility); synergistic with Shilajit and L-Carnitine.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "CardioCalm", "LivClear PRO"],
        "tadbir": "Ubiquinol reduced form preferred; administer with dietary fat"
    },
    "L_CITRULLINE": {
        "key": "L_CITRULLINE",
        "unani_name": "Muharrak-e-Dam (Citrulline Malate)",
        "botanical_name": "L-Citrulline Malate",
        "english_name": "L-Citrulline",
        "family": "Amino Acid Precursor",
        "part_used": "Pharmaceutical grade powder",
        "mizaj": {"heat": 2, "moisture": 1, "description": "Har 2, Ratab 1 (Hot in 2nd degree, Moist in 1st degree)"},
        "afaal": ["Muhrik (Stimulant)", "Muqawwi-e-Mani (Vascular enhancer)"],
        "pharmacodynamics": "Bypasses hepatic arginase to convert to L-arginine in kidneys; activates endothelial NOS to produce nitric oxide, dilating cavernosal smooth muscle.",
        "why_essential": "Rapid-onset non-pharmaceutical erectile blood flow enhancer; onset within 30-60 minutes.",
        "products_used_in": ["NightOne X"],
        "tadbir": "99% pure synthetic or fermented L-citrulline"
    },
    "L_CARNITINE": {
        "key": "L_CARNITINE",
        "unani_name": "Hamal-e-Taqat (Carnitine Shuttle)",
        "botanical_name": "L-Carnitine L-Tartrate / Acetyl-L-Carnitine",
        "english_name": "L-Carnitine",
        "family": "Amino Acid Derivative",
        "part_used": "Pure crystalline powder",
        "mizaj": {"heat": 1, "dryness": 1, "description": "Har 1, Yabis 1 (Warm-Dry / Metabolic activation)"},
        "afaal": ["Muqawwi-e-Quwwa", "Muwalid-e-Taqat"],
        "pharmacodynamics": "Shuttles long-chain fatty acids across inner mitochondrial membrane for beta-oxidation; fuels sperm flagellar locomotion.",
        "why_essential": "Direct nutritional substrate for sperm forward progression; reverses asthenozoospermia.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "Fertility Formula-M"],
        "tadbir": "L-tartrate salt form for high bioavailability"
    },
    "SELENIUM": {
        "key": "SELENIUM",
        "unani_name": "Jauhar-e-Qalai (Organic Selenium)",
        "botanical_name": "L-Selenomethionine",
        "english_name": "Selenium",
        "family": "Trace Mineral Bioactive",
        "part_used": "Organic yeast-bound or chelated selenium",
        "mizaj": {"heat": 1, "dryness": 1, "description": "Har 1, Yabis 1 (Warm-Dry)"},
        "afaal": ["Muqawwi (Cellular protector)", "Muhaffiz-e-Mani"],
        "pharmacodynamics": "Essential cofactor for GPx4 (glutathione peroxidase 4) which protects sperm mitochondrial sheath from lipid peroxidation; iodothyronine deiodinase cofactor.",
        "why_essential": "Prevents sperm DNA fragmentation (DFI reduction) and reduces Anti-TPO antibodies in Hashimoto's.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "ThyroMet-W"],
        "tadbir": "L-selenomethionine form only; do not exceed 400 mcg/day"
    },
    "ZINC_BISGLYCINATE": {
        "key": "ZINC_BISGLYCINATE",
        "unani_name": "Jauhar-e-Faulad (Zinc Chelate)",
        "botanical_name": "Zinc Bisglycinate Chelate",
        "english_name": "Zinc Bisglycinate",
        "family": "Chelated Mineral",
        "part_used": "Amino acid chelate",
        "mizaj": {"heat": 2, "dryness": 2, "description": "Har 2, Yabis 2 (Warm-Dry)"},
        "afaal": ["Muqawwi-e-Mani", "Muqawwi-e-Tabiyat"],
        "pharmacodynamics": "Inhibits aromatase enzyme (converts excess testosterone to estradiol); structural cofactor in RNA polymerase for Sertoli sperm division; prostate antibacterial.",
        "why_essential": "Reverses hypogonadism and teratospermia (poor sperm morphology); bisglycinate offers 90% absorption vs 25% for zinc sulphate.",
        "products_used_in": ["Qurs-e-Taqwiyat-e-Mani PRO", "OvaBalance PRO", "ImmunoGuard", "Men Daily"],
        "tadbir": "Fully reacted bisglycinate chelate; dose 15-30mg elemental zinc"
    }
}


def get_all_monographs() -> List[Dict[str, Any]]:
    return list(MONOGRAPHS.values())


def get_monograph(key: str) -> Optional[Dict[str, Any]]:
    return MONOGRAPHS.get(key.upper())


get_monograph_by_key = get_monograph


def search_monographs(query: str) -> List[Dict[str, Any]]:
    q = query.lower()
    results = []
    for m in MONOGRAPHS.values():
        if (
            q in m["key"].lower()
            or q in m.get("unani_name", "").lower()
            or q in m.get("botanical_name", "").lower()
            or q in m.get("english_name", "").lower()
            or q in m.get("pharmacodynamics", "").lower()
            or q in m.get("why_essential", "").lower()
            or any(q in af.lower() for af in m.get("afaal", []))
        ):
            results.append(m)
    return results
