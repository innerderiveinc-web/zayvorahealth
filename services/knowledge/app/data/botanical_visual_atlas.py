"""
ZAYVORA Health OS™ — Botanical Visual Atlas & Morphological Identification Keys
================================================================================
Master Pharmacognosy & Botanical Identification Repository.
Conforms with:
  - Unani Pharmacopoeia of India (UPI) Parts I & II
  - WHO Guidelines on Good Agricultural and Collection Practices (GACP)
  - Ayurvedic & Unani Quality Standards for Raw Botanical Drugs

Provides macroscopic diagnostic characters, organoleptic markers, microscopic
powder histology, and authentic adulteration detection SOPs for raw herb authentication.
"""

from typing import Dict, Any, List, Optional

BOTANICAL_ATLAS: List[Dict[str, Any]] = [
    {
        "id": "bva-01-asgandh",
        "canonical_name": "Asgandh",
        "botanical_name": "Withania somnifera (L.) Dunal",
        "family": "Solanaceae",
        "vernacular_names": {
            "urdu": "اسگندھ ناگوری",
            "arabic": "سم الفراخ / العباب",
            "hindi": "अश्वगंधा",
            "english": "Winter Cherry / Indian Ginseng"
        },
        "mizaj": "Hot 2°, Dry 2° (Garm 2°, Khushk 2°)",
        "plant_part_used": "Dried mature root (Bikh-e-Asgandh)",
        "classical_authorities": ["Al-Qanoon fit-Tibb", "Khazain-ul-Advia", "UPI Part-I Vol. I"],
        "macroscopic_diagnostic_keys": {
            "dimensions": "Length: 10 to 20 cm, Diameter: 6 to 18 mm",
            "external_morphology": "Straight, cylindrical, unbranched or sparsely branched roots tapering downwards. Exterior surface light brown to creamy grey with fine longitudinal wrinkles.",
            "fracture_texture": "Short, starchy, brittle fracture; cleanly breaks with minimal fibrous splintering.",
            "cross_section_appearance": "Light cream starchy central core; prominent narrow dark cambium ring separating the cortex from the stelar cylinder."
        },
        "organoleptic_profile": {
            "odor": "Strong characteristic pungent horse-like odor ('Ashwa-gandha'), markedly intensified on pulverization.",
            "taste": "Bitter, mucilaginous, followed by a slight lingering acrid tongue sensation."
        },
        "microscopic_diagnostic_markers": [
            "Abundant simple and compound starch grains (5-18 μm) with distinct centric hilum.",
            "Microsphenoidal (sandy) and prismatic calcium oxalate crystals embedded in cortical parenchyma.",
            "Lignified xylem vessels with reticulate and scalariform pit thickenings.",
            "Cork cells composed of 4-6 layers of tabular, suberized brown polygonal cells."
        ],
        "adulteration_detection_sops": [
            {
                "adulterant": "Roots of Withania coagulans (Paneer Dodi) or Physalis minima",
                "detection_method": "Macroscopic Inspection: W. coagulans roots are deeply grooved, significantly lighter in weight, and lack the clean starchy fracture.",
                "chemical_spot_test": "Iodine Reagent: True Asgandh cross-section turns immediate deep blue-violet due to high amylaceous starch content. Woodier substitutes exhibit faint or negative staining."
            },
            {
                "adulterant": "Spent / Extracted Root Powder",
                "detection_method": "Water Soluble Extractive: UPI standard mandates not less than 15.0% w/w water-soluble extractive. Exhausted roots yield <6.0%."
            }
        ],
        "detoxification_and_safety": {
            "is_schedule_e1": False,
            "mudabbar_required": False,
            "purification_sop": "Clean thoroughly of sand and soil, peel outer periderm if aged, soak in milk (Doodh mein Josh) for pediatric tonics.",
            "musleh": "Katira (Astragalus gummifer) and Cow's Milk",
            "badal": "Bahman Safaid / Salab Misri"
        }
    },
    {
        "id": "bva-02-suranjan",
        "canonical_name": "Suranjan Shireen",
        "botanical_name": "Colchicum autumnale L. / Colchicum luteum Baker",
        "family": "Colchicaceae / Liliaceae",
        "vernacular_names": {
            "urdu": "سورنجان شیریں",
            "arabic": "سورنجان حلو",
            "hindi": "सुरंजन मीठी",
            "english": "Sweet Meadow Saffron / Colchicum Corm"
        },
        "mizaj": "Hot 2°, Dry 2° (Sweet) / Hot 3°, Dry 3° (Bitter/Talkh)",
        "plant_part_used": "Dried corm (Ganth / Beekh)",
        "classical_authorities": ["Kitab al-Hawi fit-Tibb", "Kamil al-Sina'a", "Khazain-ul-Advia", "UPI Part-I Vol. II"],
        "macroscopic_diagnostic_keys": {
            "dimensions": "Length: 2 to 4.5 cm, Width: 1.5 to 3 cm, Thickness: 8 to 15 mm",
            "external_morphology": "Ovate, flattened on one side with a distinct longitudinal groove. Yellowish-white to light buff exterior, smooth or slightly wrinkled.",
            "fracture_texture": "Short, chalky, highly amylaceous fracture; easily pulverized into a white dust.",
            "cross_section_appearance": "Dense, solid, homogeneous milky white flesh; vascular bundles scattered as tiny pin-point yellowish dots."
        },
        "organoleptic_profile": {
            "odor": "Virtually odorless when dry; faint starchy aroma when moist.",
            "taste": "Suranjan Shireen is bland, mildly sweetish, then mucilaginous. (Note: Suranjan Talkh is intensely bitter and acrid)."
        },
        "microscopic_diagnostic_markers": [
            "Parenchyma densely packed with compound starch grains (2 to 4 components) with triangular or stellate hila.",
            "Complete absence of calcium oxalate raphides (differentiates from squill and arum adulterants).",
            "Spiral and annular vessel elements with thin non-lignified walls."
        ],
        "adulteration_detection_sops": [
            {
                "adulterant": "Suranjan Talkh (Bitter toxic corms) substituted for Sweet Suranjan",
                "detection_method": "Organoleptic Test: Tiny speck on tongue tip yields immediate fierce bitter taste if bitter variety; sweet variety is completely devoid of bitterness.",
                "chemical_spot_test": "Concentrated Sulphuric Acid (H2SO4): Produces a transient intense yellow turning orange-red color reaction indicating colchicine alkaloid presence."
            },
            {
                "adulterant": "Arisaema propinquum (Snake Lily / Habb-ul-Ghul) corms",
                "detection_method": "Microscopy: Arisaema contains needle-shaped raphides of calcium oxalate which induce fierce throat stinging; true Colchicum possesses ZERO raphides."
            }
        ],
        "detoxification_and_safety": {
            "is_schedule_e1": True,
            "mudabbar_required": True,
            "purification_sop": "Suranjan Talkh MUST be soaked in Sheer-e-Gao (fresh cow's milk) for 24 hours, boiled gently until milk is absorbed, then shade-dried. This reduces toxic colchicine excess while retaining therapeutic colchicosides.",
            "musleh": "Katira (Astragalus gummifer) & Zanjabeel (Zingiber officinale)",
            "badal": "Bozidan (Pyrethrum indicum) / Asgandh"
        }
    },
    {
        "id": "bva-03-zanjabeel",
        "canonical_name": "Zanjabeel",
        "botanical_name": "Zingiber officinale Roscoe",
        "family": "Zingiberaceae",
        "vernacular_names": {
            "urdu": "زنجبیل / سونٹھ",
            "arabic": "زنجبيل",
            "hindi": "सोंठ / अदरक",
            "english": "Dried Ginger"
        },
        "mizaj": "Hot 3°, Dry 2° (Garm 3°, Khushk 2°)",
        "plant_part_used": "Dried rhizome (Sonth)",
        "classical_authorities": ["Al-Qanoon fit-Tibb", "Kitab al-Hawi", "UPI Part-I Vol. I"],
        "macroscopic_diagnostic_keys": {
            "dimensions": "Length: 5 to 15 cm, Width: 1.5 to 3 cm laterally compressed",
            "external_morphology": "Laterally flattened, palmately branched 'hands' or 'fingers'. Pale buff to light golden-brown surface with longitudinal striations and ring-like scars of cataphylls.",
            "fracture_texture": "Fibrous, short, displaying protruding fibro-vascular bundles.",
            "cross_section_appearance": "Prominent yellow-brown endodermis separating the wide cortical zone from the large central stele; abundant glistening oleoresin droplets."
        },
        "organoleptic_profile": {
            "odor": "Strongly aromatic, agreeable, warm spicy scent.",
            "taste": "Fiercely pungent, heating, salivary-stimulating."
        },
        "microscopic_diagnostic_markers": [
            "Sac-shaped, flattened oval starch grains (12-50 μm) with eccentric beak-like hilum.",
            "Abundant golden-yellow, suberized oleoresin cells containing gingerols and shogaols.",
            "Non-lignified septate fibers with slit-like oblique pits."
        ],
        "adulteration_detection_sops": [
            {
                "adulterant": "Exhausted / Solvent-Extracted Ginger",
                "detection_method": "Water-Soluble Ash: UPI standard mandates minimum 1.7% w/w water-soluble ash. Exhausted ginger drops below 0.8%.",
                "chemical_spot_test": "Alcohol Extractive Test: Genuine dry ginger yields not less than 4.5% w/w alcohol-soluble extractive with pungent aroma."
            },
            {
                "adulterant": "Bleached with excess Calcium Sulphate (Chuna)",
                "detection_method": "Total Ash & Acid-Insoluble Ash: Chalk-coated ginger exhibits total ash >8.0% (standard max: 6.0%) and effervesces violently with dilute Hydrochloric Acid (HCl)."
            }
        ],
        "detoxification_and_safety": {
            "is_schedule_e1": False,
            "mudabbar_required": False,
            "purification_sop": "Wash thoroughly, scrape off epidermal chalk layers if limed, dry at 40°C.",
            "musleh": "Samagh-e-Arabi (Gum Acacia) and Roghan-e-Badam (Almond Oil)",
            "badal": "Filfil Daraz (Piper retrofractum / longum)"
        }
    },
    {
        "id": "bva-04-filfil-siyah",
        "canonical_name": "Filfil Siyah",
        "botanical_name": "Piper nigrum L.",
        "family": "Piperaceae",
        "vernacular_names": {
            "urdu": "فلفل سیاہ / کالی مرچ",
            "arabic": "فلفل أسود",
            "hindi": "काली मिर्च",
            "english": "Black Pepper"
        },
        "mizaj": "Hot 3°, Dry 3° (Garm 3°, Khushk 3°)",
        "plant_part_used": "Dried unripe globose drupe",
        "classical_authorities": ["Al-Qanoon fit-Tibb", "Khazain-ul-Advia", "UPI Part-I Vol. I"],
        "macroscopic_diagnostic_keys": {
            "dimensions": "Diameter: 3.5 to 6 mm sub-globular berry",
            "external_morphology": "Heavily reticulated, coarsely wrinkled pericarp, dark brownish-black to jet black. Minute apical remnant of stigma.",
            "fracture_texture": "Hard, crustaceous outer pericarp with a whitish, starchy, hollow perisperm center.",
            "cross_section_appearance": "Thin dark pericarp surrounding a light grayish-white perisperm with a central air cavity."
        },
        "organoleptic_profile": {
            "odor": "Characteristic sharp aromatic spicy fragrance.",
            "taste": "Intensely biting, fiery, persistent piperine pungency."
        },
        "microscopic_diagnostic_markers": [
            "Pericarp stone cells: Isodiametric sclereids with horseshoe-shaped secondary lumen wall thickenings.",
            "Minute polyhedral starch grains (2-6 μm) packed compactly into perisperm cells.",
            "Hypodermal oil cells containing piperine crystals and essential oil."
        ],
        "adulteration_detection_sops": [
            {
                "adulterant": "Carica papaya seeds (Dried Papaya Seeds)",
                "detection_method": "Water Flotation Assay: Papaya seeds float on surface water; heavy genuine whole black peppercorns sink promptly to the bottom.",
                "microscopic_test": "Papaya seeds contain distinct epidermal hairs and large oil globules without horseshoe sclereids."
            },
            {
                "adulterant": "Mineral Oil Glazing / Kerosene wash for gloss",
                "detection_method": "Fluorescence Analysis: Under UV light (366 nm), mineral oil-glazed berries emit strong bluish-violet fluorescence; untreated berries are dark."
            }
        ],
        "detoxification_and_safety": {
            "is_schedule_e1": False,
            "mudabbar_required": False,
            "purification_sop": "Manual winnowing to remove dust and light stalks.",
            "musleh": "Samagh-e-Arabi & Roghan-e-Banafsha",
            "badal": "Zanjabeel / Filfil Safaid"
        }
    },
    {
        "id": "bva-05-ustukhuddus",
        "canonical_name": "Ustukhuddus",
        "botanical_name": "Lavandula stoechas L.",
        "family": "Lamiaceae",
        "vernacular_names": {
            "urdu": "استقدوس / جاروبِ دماغ",
            "arabic": "أستحودس / مكنسة الدماغ",
            "hindi": "उस्तुखुद्दूस",
            "english": "French Lavender / Arabian Lavender"
        },
        "mizaj": "Hot 1°, Dry 2° (Garm 1°, Khushk 2°)",
        "plant_part_used": "Dried flowering inflorescence and floral spikes",
        "classical_authorities": ["Al-Qanoon fit-Tibb", "Kitab al-Hawi", "Bayaz-e-Kabir", "UPI Part-I Vol. II"],
        "macroscopic_diagnostic_keys": {
            "dimensions": "Spike length: 2 to 4 cm, Width: 1 to 1.5 cm",
            "external_morphology": "Dense quadrangular spike surmounted by a tuft of showy, sterile, purple-violet membranous bracts (coma). Flowers small, dark purple.",
            "fracture_texture": "Brittle, crumbly florets detaching easily from the central rachis.",
            "cross_section_appearance": "Hairy calyx with 13-15 distinct longitudinal rib veins; glandular dots on surface."
        },
        "organoleptic_profile": {
            "odor": "Strongly balsamic, camphoraceous, relaxing lavender aroma.",
            "taste": "Bitter, slightly camphoraceous, pleasantly astringent."
        },
        "microscopic_diagnostic_markers": [
            "Biate branched and stellate non-glandular trichomes covering calyx.",
            "Capitate glandular hairs with unicellular stalks and 8-celled radiating heads (lamiaceous glands).",
            "Pollen grains: Hexacolpate, sub-spheroidal (30-40 μm) with smooth exine."
        ],
        "adulteration_detection_sops": [
            {
                "adulterant": "Spent Lavandula angustifolia flowers",
                "detection_method": "Volatile Oil Assay: Genuine Lavandula stoechas yields not less than 0.8% v/w volatile oil rich in camphor, fenchone, and cineole.",
                "morphological_check": "Presence of the terminal showy purple coma bracts is pathognomonic for L. stoechas; absent in common L. angustifolia."
            }
        ],
        "detoxification_and_safety": {
            "is_schedule_e1": False,
            "mudabbar_required": False,
            "purification_sop": "Remove non-floral stems and sandy soil through sieve #20.",
            "musleh": "Sikanjabeen Motadil & Sharbat-e-Bazoori",
            "badal": "Aftimoon (Cuscuta reflexa) / Badiyan"
        }
    },
    {
        "id": "bva-06-babchi",
        "canonical_name": "Babchi",
        "botanical_name": "Psoralea corylifolia L. (Cullen corylifolium)",
        "family": "Fabaceae",
        "vernacular_names": {
            "urdu": "بابچی",
            "arabic": "لبلاب / بابچی",
            "hindi": "बाकुची / बावची",
            "english": "Psoralea Seeds / Purple Fleabane"
        },
        "mizaj": "Hot 2°, Dry 2° (Garm 2°, Khushk 2°)",
        "plant_part_used": "Dried ripe seeds / fruits",
        "classical_authorities": ["Khazain-ul-Advia", "UPI Part-I Vol. I", "NFUM Part-I"],
        "macroscopic_diagnostic_keys": {
            "dimensions": "Length: 3.5 to 5 mm, Breadth: 2 to 3 mm",
            "external_morphology": "Oblong, flattened, kidney-shaped or sub-reniform achene. Exterior dark chocolate brown to brownish-black with prominent pitted reticulations.",
            "fracture_texture": "Hard seed coat; cotyledons oily, light yellowish-white.",
            "cross_section_appearance": "Thin adherent pericarp, distinct campylotropous seed with two large fleshy oily cotyledons."
        },
        "organoleptic_profile": {
            "odor": "Distinctive, aromatic, somewhat disagreeable balsamic odor.",
            "taste": "Bitter, pungent, acrid, leaving an oily warmth in the pharynx."
        },
        "microscopic_diagnostic_markers": [
            "Palisade-like sclerenchymatous layer of radially elongated cells in seed coat (Malpighian cells).",
            "Large secretory reservoirs containing brownish oleoresinous furanocoumarins (psoralen, isopsoralen).",
            "Aleurone grains and micro-globules of fixed oil in endosperm cells."
        ],
        "adulteration_detection_sops": [
            {
                "adulterant": "Seeds of Abutilon indicum (Kanghi)",
                "detection_method": "Microscopic & Morphology: Abutilon seeds are heart-shaped with fine stellate hairs; Babchi is reniform, glabrous, and pitted.",
                "chemical_test": "TLC/HPTLC profiling for Psoralen marker: Genuine Babchi exhibits prominent fluorescent blue band under 366 nm corresponding to psoralen."
            }
        ],
        "detoxification_and_safety": {
            "is_schedule_e1": False,
            "mudabbar_required": True,
            "purification_sop": "Babchi is steep-purified by maceration in fresh ginger juice (Aab-e-Zanjabeel) or butter-milk (Chhachh) for 3 days with daily fluid change to prevent cutaneous blistering.",
            "musleh": "Roghan-e-Banafsha & Cow's Ghee",
            "badal": "Chaksu (Cassia absus)"
        }
    },
    {
        "id": "bva-07-rewand-chini",
        "canonical_name": "Rewand Chini",
        "botanical_name": "Rheum emodi Wall. / Rheum webbianum Royle",
        "family": "Polygonaceae",
        "vernacular_names": {
            "urdu": "ریوند چینی / ریوند ختائی",
            "arabic": "راوند صيني",
            "hindi": "रेवंद चीनी",
            "english": "Indian Rhubarb / Himalayan Rhubarb"
        },
        "mizaj": "Hot 2°, Dry 2° (Garm 2°, Khushk 2°)",
        "plant_part_used": "Dried rhizome and root",
        "classical_authorities": ["Al-Qanoon fit-Tibb", "Kitab al-Hawi", "UPI Part-I Vol. III"],
        "macroscopic_diagnostic_keys": {
            "dimensions": "Pieces: 2 to 10 cm length, 1 to 5 cm diameter cylindrical or barrel-shaped",
            "external_morphology": "Compact, heavy pieces, peeled or unpeeled. Exterior yellowish-brown with distinct longitudinal dark reticulations ('star spots').",
            "fracture_texture": "Granular, uneven fracture; surfaces show alternating white parenchyma rays and orange-red medullary rays.",
            "cross_section_appearance": "Distinct anomalous cambial rings forming 'star spots' (stellate vascular bundles) in the central pith."
        },
        "organoleptic_profile": {
            "odor": "Characteristic aromatic, earthy, pleasantly sub-acidic aroma.",
            "taste": "Bitter, astringent, gritty between the teeth due to calcium oxalate."
        },
        "microscopic_diagnostic_markers": [
            "Enormous rosette aggregates of calcium oxalate (50-140 μm) throughout parenchyma.",
            "Medullary rays containing bright yellow anthraquinone glycoside granules (emodin, rhein).",
            "Reticulate vessels up to 150 μm wide."
        ],
        "adulteration_detection_sops": [
            {
                "adulterant": "Rumex nepalensis roots",
                "detection_method": "Borntrager's Test for Hydroxyanthraquinones: Powder shaken with ether; addition of dilute ammonia produces immediate cherry-red coloration in aqueous layer.",
                "fluorescence_test": "True Rhubarb powder under UV (366 nm) exhibits deep velvety brown to orange fluorescence; rhapontic rhubarb emits fierce blue fluorescence."
            }
        ],
        "detoxification_and_safety": {
            "is_schedule_e1": False,
            "mudabbar_required": False,
            "purification_sop": "Wash, scrape off black rind, dry at 45°C.",
            "musleh": "Samagh-e-Arabi & Gul-e-Surkh",
            "badal": "Zard Chob (Turmeric) / Afsanteen"
        }
    },
    {
        "id": "bva-08-zafran",
        "canonical_name": "Zafran",
        "botanical_name": "Crocus sativus L.",
        "family": "Iridaceae",
        "vernacular_names": {
            "urdu": "زعفران / کیسر",
            "arabic": "زعفران",
            "hindi": "केसर",
            "english": "Saffron"
        },
        "mizaj": "Hot 2°, Dry 1° (Garm 2°, Khushk 1°)",
        "plant_part_used": "Dried trifid stigmas and top of style",
        "classical_authorities": ["Al-Qanoon fit-Tibb", "Kamil al-Sina'a", "UPI Part-I Vol. I"],
        "macroscopic_diagnostic_keys": {
            "dimensions": "Length: 20 to 35 mm tubular flaring stigmas",
            "external_morphology": "Three dark crimson-red trumpet-shaped stigmas attached to a short pale yellow style. Upper end flared, notched and slit.",
            "fracture_texture": "Flexible when moist; brittle when dry; stains skin intensely golden-yellow when rubbed with water.",
            "cross_section_appearance": "Unicellular tubular papillae on the stigma rim."
        },
        "organoleptic_profile": {
            "odor": "Powerfully sweet, intoxicating, honey-like, floral saffron scent.",
            "taste": "Warm, pungent, pleasantly bitter."
        },
        "microscopic_diagnostic_markers": [
            "Conical, finger-like epidermal papillae (50-120 μm) on the upper margin of the stigma.",
            "Rare spherical pollen grains (80-120 μm) with smooth exine.",
            "Elongated thin-walled parenchyma containing crocin and crocetin carotenoids."
        ],
        "adulteration_detection_sops": [
            {
                "adulterant": "Dyed corn silk, safflower (Carthamus tinctorius), shredded meat fibers",
                "detection_method": "Water Imbibition Assay: Drop authentic stigma in warm water. Genuine saffron slowly releases brilliant clear golden-yellow halos without expanding into floral petals. Stigma remains intact and red for hours. Dyed corn silk immediately releases red dye and turns pale grey.",
                "chemical_test": "Concentrated Sulphuric Acid: A single genuine stigma dropped into a drop of H2SO4 turns immediate deep blue, quickly shifting to purple and reddish-brown."
            }
        ],
        "detoxification_and_safety": {
            "is_schedule_e1": False,
            "mudabbar_required": False,
            "purification_sop": "Triturate gently with rose water (Arq Gulab) in porcelain mortar before compounding.",
            "musleh": "Sikanjabeen & Tukhm-e-Kahu",
            "badal": "Qust Shireen / Sumbul-ut-Teeb"
        }
    },
    {
        "id": "bva-09-kasni",
        "canonical_name": "Tukhm-e-Kasni",
        "botanical_name": "Cichorium intybus L.",
        "family": "Asteraceae",
        "vernacular_names": {
            "urdu": "تخمِ کاسنی",
            "arabic": "بزر الهندباء",
            "hindi": "कासनी के बीज",
            "english": "Chicory Seeds / Achenes"
        },
        "mizaj": "Cold 1°, Dry 1° (Barid 1°, Yabis 1°)",
        "plant_part_used": "Dried achenes (seeds)",
        "classical_authorities": ["Al-Qanoon fit-Tibb", "Kitab al-Hawi", "UPI Part-I Vol. II"],
        "macroscopic_diagnostic_keys": {
            "dimensions": "Length: 2 to 3 mm, Width: 1 to 1.5 mm",
            "external_morphology": "Small, angled, wedge-shaped (turbinate) achenes, 4-5 ribbed, pale brown to greyish-black with crown of short paleaceous pappus scales at apex.",
            "fracture_texture": "Crisp, oily fracture.",
            "cross_section_appearance": "Outer pericarp with brown pigment layer; two oily cotyledons."
        },
        "organoleptic_profile": {
            "odor": "Mild, herbaceous, characteristic scent.",
            "taste": "Pleasantly bitter, mucilaginous."
        },
        "microscopic_diagnostic_markers": [
            "Pappus composed of narrow, unicellular scales.",
            "Sclerenchymatous pericarp fibers arranged longitudinally.",
            "Endosperm containing aleurone grains and inulin crystals (soluble in warm water)."
        ],
        "adulteration_detection_sops": [
            {
                "adulterant": "Seeds of Lactuca serriola (Wild Lettuce)",
                "detection_method": "Morphology: Chicory achenes have a crown of short scales; wild lettuce achenes possess a long slender beak with fine capillary hairs.",
                "quality_metric": "Foreign Organic Matter: Not more than 2% w/w."
            }
        ],
        "detoxification_and_safety": {
            "is_schedule_e1": False,
            "mudabbar_required": False,
            "purification_sop": "Winnow to clear chaff, wash in cold water.",
            "musleh": "Sharbat-e-Bazoori & Shakar Safaid",
            "badal": "Tukhm-e-Kahu / Tukhm-e-Kasoos"
        }
    },
    {
        "id": "bva-10-badiyan",
        "canonical_name": "Badiyan",
        "botanical_name": "Foeniculum vulgare Mill.",
        "family": "Apiaceae",
        "vernacular_names": {
            "urdu": "بادیان / سونف",
            "arabic": "رازيانج",
            "hindi": "सौंफ",
            "english": "Fennel Fruit"
        },
        "mizaj": "Hot 2°, Dry 1° (Garm 2°, Khushk 1°)",
        "plant_part_used": "Dried ripe cremocarp fruit",
        "classical_authorities": ["Al-Qanoon fit-Tibb", "Khazain-ul-Advia", "UPI Part-I Vol. I"],
        "macroscopic_diagnostic_keys": {
            "dimensions": "Length: 5 to 10 mm, Width: 2 to 4 mm",
            "external_morphology": "Oblong, slightly curved cremocarp, greenish-brown to yellowish-green. Five prominent, straight, pale prominent primary ridges on each mericarp; crowned by a small stylopod.",
            "fracture_texture": "Readily splits along the commissure into two curved mericarps.",
            "cross_section_appearance": "Five ribs with vascular bundles, four wide brown vallecular vittae (oil channels) on dorsal side and two on commissural side."
        },
        "organoleptic_profile": {
            "odor": "Intensely sweet, fragrant, anise-like anethole aroma.",
            "taste": "Sweet, aromatic, warm, followed by a cooling camphoric sensation."
        },
        "microscopic_diagnostic_markers": [
            "Mesocarp characterized by 'parquetry' arrangement of endocarp cells (groups of narrow parallel cells).",
            "Brown, schizogenous vittae filled with essential oil containing trans-anethole and fenchone.",
            "Abundant micro-rosette crystals of calcium oxalate in endosperm."
        ],
        "adulteration_detection_sops": [
            {
                "adulterant": "Exhausted Fennel artificially dyed with Malachite Green",
                "detection_method": "Color Stripping Test: Rub fruits on moist filter paper. Artificially colored fruits release immediate blue-green dye; natural fennel yields zero dye.",
                "volatile_oil_metric": "Minimum 1.4% v/w volatile oil required by UPI standards."
            }
        ],
        "detoxification_and_safety": {
            "is_schedule_e1": False,
            "mudabbar_required": False,
            "purification_sop": "Manual separation from stalks and pedicels.",
            "musleh": "Kishneez Khushk (Coriander) & Sandal Safaid",
            "badal": "Anisoon (Pimpinella anisum)"
        }
    },
    {
        "id": "bva-11-gul-e-surkh",
        "canonical_name": "Gul-e-Surkh",
        "botanical_name": "Rosa damascena Mill.",
        "family": "Rosaceae",
        "vernacular_names": {
            "urdu": "گلِ سرخ / دیسی گلاب",
            "arabic": "ورد أحمر",
            "hindi": "गुलाब के फूल",
            "english": "Damask Rose Petals"
        },
        "mizaj": "Cold 1°, Dry 2° (Barid 1°, Yabis 2°)",
        "plant_part_used": "Dried petals",
        "classical_authorities": ["Al-Qanoon fit-Tibb", "Kitab al-Hawi", "UPI Part-I Vol. I"],
        "macroscopic_diagnostic_keys": {
            "dimensions": "Length: 15 to 30 mm obovate petals",
            "external_morphology": "Broadly obovate, velvety petals with emarginate apex and cuneate base. Deep pinkish-red to purple, becoming purplish-brown on storage.",
            "fracture_texture": "Thin, papery, delicate, easily pulverized.",
            "cross_section_appearance": "Epidermal cells with wavy anticlinal walls and prominent velvety papillae."
        },
        "organoleptic_profile": {
            "odor": "Delightfully fragrant, uplifting, characteristic damascena rose aroma.",
            "taste": "Sweetish, slightly bitter, cooling, highly astringent."
        },
        "microscopic_diagnostic_markers": [
            "Upper epidermis shows pronounced velvety conical papillae.",
            "Abundant pollen grains (25-35 μm) with 3 pores and striate exine.",
            "Parenchyma packed with anthocyanin pigments and rosette crystals of calcium oxalate."
        ],
        "adulteration_detection_sops": [
            {
                "adulterant": "Hibiscus petals or artificially perfumed wild rose petals",
                "detection_method": "Microscopy: Hibiscus exhibits large mucilage cavities and large spiny pollen grains (120 μm); Rosa damascena pollen is small (30 μm) with NO spines.",
                "chemical_check": "Natural rose anthocyanin turns red in acidic pH and green in alkaline pH."
            }
        ],
        "detoxification_and_safety": {
            "is_schedule_e1": False,
            "mudabbar_required": False,
            "purification_sop": "Shade drying in well-ventilated dark rooms to preserve volatile geraniol and citronellol.",
            "musleh": "Anisoon & Marzanjosh",
            "badal": "Gul-e-Nilofar (Nymphaea alba)"
        }
    },
    {
        "id": "bva-12-darchini",
        "canonical_name": "Darchini",
        "botanical_name": "Cinnamomum verum J. Presl (Cinnamomum zeylanicum)",
        "family": "Lauraceae",
        "vernacular_names": {
            "urdu": "دارچینی",
            "arabic": "دارصيني / قرفة",
            "hindi": "दालचीनी",
            "english": "True Ceylon Cinnamon"
        },
        "mizaj": "Hot 2°, Dry 2° (Garm 2°, Khushk 2°)",
        "plant_part_used": "Dried inner bark of shoots freed from cork",
        "classical_authorities": ["Al-Qanoon fit-Tibb", "Khazain-ul-Advia", "UPI Part-I Vol. I"],
        "macroscopic_diagnostic_keys": {
            "dimensions": "Quills: Up to 1 meter long, 0.5 mm thick paper-thin compound quills",
            "external_morphology": "Compound quills (multiple inner barks nested tightly inside one another). Exterior yellowish-brown, smooth with faint wavy longitudinal lines.",
            "fracture_texture": "Short, clean, splintery fracture.",
            "cross_section_appearance": "Extremely thin bark (<0.8 mm); absence of cork and primary cortex."
        },
        "organoleptic_profile": {
            "odor": "Fragrant, delicate, warmly aromatic cinnamaldehyde scent.",
            "taste": "Warm, sweet, highly agreeable, pungent without harsh astringency."
        },
        "microscopic_diagnostic_markers": [
            "Continuous pericyclic ring of 3-4 layers of stone cells with thickened U-shaped walls.",
            "Acicular (needle-like) micro-crystals of calcium oxalate in phloem parenchyma.",
            "Volatile oil cells and mucilage cavities in phloem."
        ],
        "adulteration_detection_sops": [
            {
                "adulterant": "Cinnamomum cassia (Chinese Cassia Bark)",
                "detection_method": "Thickness & Texture: Cassia bark is thick (1.5 to 3.0 mm), single-quilled, coarse, and contains thick grey cork. True Ceylon cinnamon is paper-thin (<0.8 mm) multi-layered compound quill.",
                "chemical_iodine_test": "Boil 1g powder in 10ml water, cool, add 2 drops dilute Iodine reagent. Cassia turns immediate deep blue (high starch); True Ceylon Cinnamon yields only a faint pale greenish-blue reaction."
            }
        ],
        "detoxification_and_safety": {
            "is_schedule_e1": False,
            "mudabbar_required": False,
            "purification_sop": "Scrape and select inner quills.",
            "musleh": "Tukhm-e-Kahu & Samagh-e-Arabi",
            "badal": "Taj Qalmi (Cassia) / Qaranfal"
        }
    }
]

def get_all_botanical_atlas() -> List[Dict[str, Any]]:
    """Returns complete list of botanical monographs in the visual atlas."""
    return BOTANICAL_ATLAS

def get_botanical_by_id(herb_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a specific botanical monograph by ID or name."""
    hid = (herb_id or "").strip().lower()
    for item in BOTANICAL_ATLAS:
        if (
            item["id"].lower() == hid
            or item["canonical_name"].lower() == hid
            or item["botanical_name"].lower().startswith(hid)
        ):
            return item
    return None
