export type RegulatoryCategory =
  | "Clinic-Prescribed Unani Formulation"
  | "Retail Wellness Unani Formulation"
  | "AYUSH-Licensed Botanical Preparation"
  | "FSSAI Dietary & Nutraceutical Supplement";

export interface ProductItem {
  id: string;
  name: string;
  category: string;
  regulatoryCategory: RegulatoryCategory;
  price: number;
  currency: string;
  size: string;
  rating: number;
  reviewCount: number;
  inStock: boolean;
  stockCount: number;
  consultBeforeUseRequired: boolean;
  canBuyDirectly: boolean;
  safetyNotice: string;
  intendedUse: string;
  shortDescription: string;
  fullOverview: string;
  activeIngredients: {
    commonName: string;
    botanicalName: string;
    partUsed: string;
    assayStandard: string;
  }[];
  suggestedUsage: {
    dose: string;
    timing: string;
    anupanVehicle: string;
    durationNotes: string;
  };
  warnings: string[];
  contraindications: string[];
  interactionWarning: string;
  batchInfo: {
    lotNumber: string;
    manufacturingDate: string;
    expiryDate: string;
    heavyMetalsTested: boolean;
    leadPpm: string;
    arsenicPpm: string;
    certificateHash: string;
  };
  manufacturer: {
    name: string;
    facility: string;
    gmpLicense: string;
  };
  faqs: { question: string; answer: string }[];
}

export const PRODUCTS_CATALOG: ProductItem[] = [
  {
    id: "manivital-pro",
    name: "ManiVital Pro (Withania & Mucuna)",
    category: "Men's Reproductive Health",
    regulatoryCategory: "AYUSH-Licensed Botanical Preparation",
    price: 1450,
    currency: "₹",
    size: "60 Veg Capsules",
    rating: 4.9,
    reviewCount: 124,
    inStock: true,
    stockCount: 142,
    consultBeforeUseRequired: false,
    canBuyDirectly: true,
    safetyNotice: "Use only as directed. Consult a qualified healthcare professional when required.",
    intendedUse: "Nutritional support for healthy sperm count, motility, seminal fluid volume, and male reproductive stamina.",
    shortDescription: "High-potency synergy of Withania somnifera and Mucuna pruriens standardized for withanolides and L-Dopa.",
    fullOverview: "ManiVital Pro brings together premier Greco-Arab spermatogenic botanicals (Muwallid-e-Mani) validated by modern analytical HPLC assays. Standardized to contain >2.5% Withanolides and >15% natural L-Dopa, it safeguards developing spermatozoa from seminal oxidative stress.",
    activeIngredients: [
      { commonName: "Asgandh Nagori", botanicalName: "Withania somnifera", partUsed: "Root Extract", assayStandard: "Withanolides > 2.5% HPLC" },
      { commonName: "Kaunch Beej", botanicalName: "Mucuna pruriens", partUsed: "Seed Extract", assayStandard: "L-Dopa > 15% HPLC" },
      { commonName: "Safed Musli", botanicalName: "Chlorophytum borivilianum", partUsed: "Tuber Extract", assayStandard: "Saponins > 40%" },
      { commonName: "Gokhru Khurd", botanicalName: "Tribulus terrestris", partUsed: "Fruit Extract", assayStandard: "Protodioscin > 20%" }
    ],
    suggestedUsage: {
      dose: "1 capsule twice daily",
      timing: "30 minutes post-breakfast and post-dinner",
      anupanVehicle: "Warm milk or lukewarm water",
      durationNotes: "Recommended minimum course: 90 days (aligning with spermatogenesis cycle)."
    },
    warnings: [
      "Do not exceed recommended daily dosage.",
      "Store in a cool, dry place away from direct sunlight (15°C–25°C)."
    ],
    contraindications: [
      "Acute febrile disorders (Humma-e-Hadda)",
      "Severe untreated hypertension without clinician supervision"
    ],
    interactionWarning: "Caution if concurrently taking dopamine agonists or MAO inhibitors due to natural L-Dopa content.",
    batchInfo: {
      lotNumber: "LOT-MVP-2026-09",
      manufacturingDate: "2026-08-10",
      expiryDate: "2028-07-31",
      heavyMetalsTested: true,
      leadPpm: "< 0.02 ppm",
      arsenicPpm: "< 0.01 ppm",
      certificateHash: "9f82ab410cd8321e9014b2e88a31c0e819b52a417c80"
    },
    manufacturer: {
      name: "ZAYVORA Health Products™",
      facility: "ZAYVORA Research & Manufacturing™ GMP Cleanroom",
      gmpLicense: "AYUSH-DL-GMP-2024-081"
    },
    faqs: [
      {
        question: "Can this be taken alongside a general multivitamin?",
        answer: "Yes. ManiVital Pro works synergetically with dietary micronutrients like Zinc and Selenium."
      }
    ]
  },
  {
    id: "ovasync",
    name: "OvaSync Botanical Complex",
    category: "Women's Hormonal Health",
    regulatoryCategory: "AYUSH-Licensed Botanical Preparation",
    price: 1380,
    currency: "₹",
    size: "60 Veg Capsules",
    rating: 4.8,
    reviewCount: 98,
    inStock: true,
    stockCount: 88,
    consultBeforeUseRequired: false,
    canBuyDirectly: true,
    safetyNotice: "Use only as directed. Consult a qualified healthcare professional when required.",
    intendedUse: "Supports regular menstrual cycle cadence, ovarian follicular maturation, and healthy pelvic circulation.",
    shortDescription: "Synergistic botanical blend of Saraca asoca, Aloe barbadensis, and Vitex agnus-castus for female endocrine balance.",
    fullOverview: "OvaSync is scientifically crafted to tonify uterine musculature (Muqawwi-e-Reham) and encourage rhythmic follicular development. It assists in mitigating estrogen-progesterone disequilibrium without synthetic hormones.",
    activeIngredients: [
      { commonName: "Ashoka Bark", botanicalName: "Saraca asoca", partUsed: "Stem Bark Extract", assayStandard: "Tannins > 8% w/w" },
      { commonName: "Gheekwar", botanicalName: "Aloe barbadensis", partUsed: "Leaf Gel Extract", assayStandard: "Aloin < 1 ppm (Non-laxative)" },
      { commonName: "Sambhalu", botanicalName: "Vitex agnus-castus", partUsed: "Berry Extract", assayStandard: "Agnuside > 0.5% HPLC" },
      { commonName: "Lodhra", botanicalName: "Symplocos racemosa", partUsed: "Bark Extract", assayStandard: "Total Alkaloids > 2%" }
    ],
    suggestedUsage: {
      dose: "1 capsule twice daily",
      timing: "Morning and evening with meals",
      anupanVehicle: "Lukewarm water",
      durationNotes: "Continue for 3 to 6 consecutive cycles; pause during active menstrual flow days 1-3 if directed."
    },
    warnings: [
      "Discontinue immediately upon confirmed pregnancy.",
      "Keep out of reach of children."
    ],
    contraindications: [
      "Active pregnancy",
      "Estrogen-dependent neoplastic conditions"
    ],
    interactionWarning: "Consult clinician if taking oral contraceptive pills or hormone replacement therapy.",
    batchInfo: {
      lotNumber: "LOT-OVA-2026-04",
      manufacturingDate: "2026-07-15",
      expiryDate: "2028-06-30",
      heavyMetalsTested: true,
      leadPpm: "< 0.01 ppm",
      arsenicPpm: "< 0.01 ppm",
      certificateHash: "b41c098e98da8711e5a201c890f12d4a7c18b049e771"
    },
    manufacturer: {
      name: "ZAYVORA Health Products™",
      facility: "ZAYVORA Research & Manufacturing™ GMP Cleanroom",
      gmpLicense: "AYUSH-DL-GMP-2024-081"
    },
    faqs: [
      {
        question: "Can I take OvaSync if I have PCOS?",
        answer: "Yes, OvaSync is formulated to support cycle regularity in women with PCOS when combined with balanced dietary habits."
      }
    ]
  },
  {
    id: "qurs-taqwiyat-mani",
    name: "Qurs Taqwiyat-e-Mani (Mudabbar Formulation)",
    category: "Men's Reproductive Health",
    regulatoryCategory: "Clinic-Prescribed Unani Formulation",
    price: 1650,
    currency: "₹",
    size: "120 Tablets",
    rating: 4.9,
    reviewCount: 64,
    inStock: true,
    stockCount: 35,
    consultBeforeUseRequired: true,
    canBuyDirectly: false,
    safetyNotice: "STATUTORY PRESCRIPTION DRUG: Schedule E(1) Mudabbar Verified. Requires clinical consultation before dispensing.",
    intendedUse: "Deep seminal tonification and viscous stabilization for oligospermia and asthenozoospermia under physician care.",
    shortDescription: "Classical Unani compound tablet incorporating purified calces (Kushta Qalai Mudabbar) and Salab Misri.",
    fullOverview: "Qurs Taqwiyat-e-Mani is an authentic Unani Pharmacopoeial compound formulated under strict 21 CFR Part 11 and Mudabbar detoxification standards. Indicated for severe seminal depletion (Riqqat-e-Mani) and low vitality.",
    activeIngredients: [
      { commonName: "Salab Misri", botanicalName: "Orchis latifolia", partUsed: "Tuber", assayStandard: "Mucilage > 45%" },
      { commonName: "Kushta Qalai (Mudabbar)", botanicalName: "Purified Stannum", partUsed: "Calcined Calx", assayStandard: "Elemental Sn validated via ICP-MS" },
      { commonName: "Tadree Zard", botanicalName: "Cheiranthus cheiri", partUsed: "Seed", assayStandard: "Glucosides > 3%" },
      { commonName: "Gond Kateera", botanicalName: "Astragalus gummifer", partUsed: "Exudate Gum", assayStandard: "NFUM Standard Monograph" }
    ],
    suggestedUsage: {
      dose: "2 tablets twice daily",
      timing: "Morning fasting and bedtime with warm milk",
      anupanVehicle: "Warm cow milk with 2 crushed green cardamoms",
      durationNotes: "Strictly as prescribed by a licensed Tabeeb (40 to 60 days)."
    },
    warnings: [
      "Prescription-only medicine. Do not self-prescribe.",
      "Must be stored in airtight container protected from moisture."
    ],
    contraindications: [
      "Severe renal impairment (eGFR < 30 mL/min)",
      "Acute hepatic dysfunction"
    ],
    interactionWarning: "Take at least 2 hours apart from synthetic antibiotic medications.",
    batchInfo: {
      lotNumber: "LOT-QTM-2026-B1",
      manufacturingDate: "2026-08-01",
      expiryDate: "2029-07-31",
      heavyMetalsTested: true,
      leadPpm: "< 0.05 ppm (Compliant with UPI limit)",
      arsenicPpm: "< 0.05 ppm",
      certificateHash: "72a819b0f4a83e091176b50912c982310f8819a071c3"
    },
    manufacturer: {
      name: "ZAYVORA Central Dispensary & Matab",
      facility: "ZAYVORA Research & Manufacturing™ Certified Cleanroom",
      gmpLicense: "AYUSH-UNANI-MFR-2025-01"
    },
    faqs: [
      {
        question: "Why does this formulation require a doctor's consultation?",
        answer: "Because it contains purified classical calces (Kushta), statutory AYUSH regulations and ZAYVORA safety protocols mandate clinician oversight to verify dosing and baseline renal clearance."
      }
    ]
  },
  {
    id: "metabocore-elite",
    name: "MetaboCore Elite Herbal Extract",
    category: "Metabolic & Blood Sugar",
    regulatoryCategory: "AYUSH-Licensed Botanical Preparation",
    price: 1250,
    currency: "₹",
    size: "60 Veg Capsules",
    rating: 4.7,
    reviewCount: 112,
    inStock: true,
    stockCount: 95,
    consultBeforeUseRequired: false,
    canBuyDirectly: true,
    safetyNotice: "Use only as directed. Consult a qualified healthcare professional when required.",
    intendedUse: "Supports healthy post-prandial glucose metabolism, insulin sensitivity, and reduction of sugar cravings.",
    shortDescription: "Standardized dual extract of Gymnema sylvestre (Gurmar) and Cinnamomum verum with Momordica charantia.",
    fullOverview: "MetaboCore Elite assists the body's natural peripheral glucose uptake and modulates alpha-glucosidase activity in the digestive tract. Designed to assist those experiencing metabolic lethargy and post-meal energy slumps.",
    activeIngredients: [
      { commonName: "Gurmar Buti", botanicalName: "Gymnema sylvestre", partUsed: "Leaf Extract", assayStandard: "Gymnemic Acids > 25% HPLC" },
      { commonName: "Dalchini Ceylon", botanicalName: "Cinnamomum verum", partUsed: "Bark Extract", assayStandard: "Polyphenols > 10% (Low coumarin)" },
      { commonName: "Karela", botanicalName: "Momordica charantia", partUsed: "Fruit Extract", assayStandard: "Charantin > 5%" },
      { commonName: "Jamun Beej", botanicalName: "Syzygium cumini", partUsed: "Seed Extract", assayStandard: "Ellagic Acid > 4%" }
    ],
    suggestedUsage: {
      dose: "1 capsule 15 minutes before lunch and dinner",
      timing: "Pre-prandial (before meals)",
      anupanVehicle: "Warm water",
      durationNotes: "Can be used continuously for 12 to 24 weeks with dietary tracking."
    },
    warnings: [
      "Monitor blood glucose levels regularly if taking antidiabetic pharmaceuticals.",
      "Not a substitute for emergency insulin in Type 1 diabetes."
    ],
    contraindications: [
      "Hypoglycemia episodes",
      "Severe liver failure"
    ],
    interactionWarning: "May exert additive hypoglycemic effect with Metformin or Sulfonylureas.",
    batchInfo: {
      lotNumber: "LOT-MET-2026-03",
      manufacturingDate: "2026-06-20",
      expiryDate: "2028-05-31",
      heavyMetalsTested: true,
      leadPpm: "< 0.01 ppm",
      arsenicPpm: "< 0.01 ppm",
      certificateHash: "11a8b0c9e887a123f809a412b77a09d8172c9183490b"
    },
    manufacturer: {
      name: "ZAYVORA Health Products™",
      facility: "ZAYVORA Research & Manufacturing™ GMP Cleanroom",
      gmpLicense: "AYUSH-DL-GMP-2024-081"
    },
    faqs: [
      {
        question: "How quickly does Gurmar reduce sugar cravings?",
        answer: "Gymnemic acids interact with lingual sweet taste receptors within days, reducing the palatability of high-sugar snacks."
      }
    ]
  },
  {
    id: "thyromet-axis",
    name: "ThyroMet Axis Botanical Support",
    category: "Thyroid & Hormonal Health",
    regulatoryCategory: "AYUSH-Licensed Botanical Preparation",
    price: 1320,
    currency: "₹",
    size: "60 Veg Capsules",
    rating: 4.8,
    reviewCount: 76,
    inStock: true,
    stockCount: 62,
    consultBeforeUseRequired: false,
    canBuyDirectly: true,
    safetyNotice: "Use only as directed. Consult a qualified healthcare professional when required.",
    intendedUse: "Supports healthy peripheral thyroid hormone conversion (T4 to T3), adrenal resilience, and metabolic warmth.",
    shortDescription: "Synergistic botanical formulation of Commiphora mukul (Guggulu), Bacopa monnieri, and Bauhinia variegata.",
    fullOverview: "ThyroMet Axis addresses the sluggish glandular temperament associated with subclinical hypothyroid states and cold dyscrasia. Standardized Guggulsterones enhance cellular metabolic tone and peripheral heat generation.",
    activeIngredients: [
      { commonName: "Shuddha Guggulu", botanicalName: "Commiphora mukul", partUsed: "Purified Gum Resin", assayStandard: "Guggulsterones E & Z > 2.5%" },
      { commonName: "Kanchnar Bark", botanicalName: "Bauhinia variegata", partUsed: "Bark Extract", assayStandard: "Total Flavonoids > 5%" },
      { commonName: "Brahmi", botanicalName: "Bacopa monnieri", partUsed: "Whole Herb Extract", assayStandard: "Bacosides > 20% HPLC" },
      { commonName: "Pippali", botanicalName: "Piper longum", partUsed: "Fruit Extract", assayStandard: "Piperine > 95% (Bioavailability enhancer)" }
    ],
    suggestedUsage: {
      dose: "1 capsule twice daily",
      timing: "After meals morning and evening",
      anupanVehicle: "Warm ginger water or plain warm water",
      durationNotes: "Recommended evaluation cycle: 90 days alongside baseline TSH/T4 checks."
    },
    warnings: [
      "Do not take if diagnosed with hyperthyroidism or Graves disease.",
      "Not recommended during pregnancy or breastfeeding without physician consent."
    ],
    contraindications: [
      "Hyperthyroid states / Thyrotoxicosis",
      "Bleeding disorders (mild antiplatelet properties of Guggulu)"
    ],
    interactionWarning: "Take at least 4 hours apart from synthetic Levothyroxine medication to avoid absorption competition.",
    batchInfo: {
      lotNumber: "LOT-THY-2026-02",
      manufacturingDate: "2026-07-02",
      expiryDate: "2028-06-30",
      heavyMetalsTested: true,
      leadPpm: "< 0.02 ppm",
      arsenicPpm: "< 0.01 ppm",
      certificateHash: "c098e721a980b1278912c98a0b7612c80918237190ad"
    },
    manufacturer: {
      name: "ZAYVORA Health Products™",
      facility: "ZAYVORA Research & Manufacturing™ GMP Cleanroom",
      gmpLicense: "AYUSH-DL-GMP-2024-081"
    },
    faqs: [
      {
        question: "Can I stop my thyroid medication with this product?",
        answer: "Never discontinue prescription thyroid hormone replacements without consulting your endocrinologist. ThyroMet Axis serves as supportive nutritional therapy."
      }
    ]
  },
  {
    id: "liverprime-core",
    name: "LiverPrime Core Hepatoprotective Formula",
    category: "Gut & Liver",
    regulatoryCategory: "AYUSH-Licensed Botanical Preparation",
    price: 1190,
    currency: "₹",
    size: "60 Veg Capsules",
    rating: 4.9,
    reviewCount: 145,
    inStock: true,
    stockCount: 110,
    consultBeforeUseRequired: false,
    canBuyDirectly: true,
    safetyNotice: "Use only as directed. Consult a qualified healthcare professional when required.",
    intendedUse: "Supports healthy liver parenchymal regeneration, bile flow, and protection against lipid accumulation.",
    shortDescription: "Dual-action Unani hepatoprotective combining Cichorium intybus (Kasni), Picrorhiza kurroa (Kutki), and Tinospora.",
    fullOverview: "LiverPrime Core is formulated according to classical Greco-Arab liver tonics (Muqawwi-e-Kabid). It facilitates phase I and II hepatic biotransformation pathways, promoting healthy liver enzyme balance.",
    activeIngredients: [
      { commonName: "Kasni Beej", botanicalName: "Cichorium intybus", partUsed: "Seed Extract", assayStandard: "Cichoriin & Inulin standardized" },
      { commonName: "Kutki", botanicalName: "Picrorhiza kurroa", partUsed: "Rhizome Extract", assayStandard: "Kutkin (Picroside I & II) > 8% HPLC" },
      { commonName: "Gilo (Sat Gilo)", botanicalName: "Tinospora cordifolia", partUsed: "Aqueous Starch", assayStandard: "Bitters > 3%" },
      { commonName: "Makoh", botanicalName: "Solanum nigrum", partUsed: "Fruit Extract", assayStandard: "Solasodine > 1%" }
    ],
    suggestedUsage: {
      dose: "1 capsule twice daily before meals",
      timing: "Morning and night with water",
      anupanVehicle: "Warm water or light herbal tea",
      durationNotes: "8 to 12 weeks course followed by maintenance regimen."
    },
    warnings: [
      "Discontinue if experiencing acute watery diarrhea.",
      "Not intended for the treatment of active gallstone impaction."
    ],
    contraindications: [
      "Obstructive jaundice due to bile duct stones",
      "End-stage hepatic encephalopathy"
    ],
    interactionWarning: "No known major drug interactions. Well tolerated alongside conventional care.",
    batchInfo: {
      lotNumber: "LOT-LIV-2026-08",
      manufacturingDate: "2026-08-05",
      expiryDate: "2028-07-31",
      heavyMetalsTested: true,
      leadPpm: "< 0.01 ppm",
      arsenicPpm: "< 0.01 ppm",
      certificateHash: "88a912b70cd981a2719a0b871239c098a1290812739a"
    },
    manufacturer: {
      name: "ZAYVORA Health Products™",
      facility: "ZAYVORA Research & Manufacturing™ GMP Cleanroom",
      gmpLicense: "AYUSH-DL-GMP-2024-081"
    },
    faqs: [
      {
        question: "Is this product beneficial for fatty liver Grade 1?",
        answer: "Yes, the lipotropic and antioxidant action of Kasni and Kutki has been extensively researched for reducing hepatic fat accumulation when combined with dietary improvements."
      }
    ]
  },
  {
    id: "neurocalmx",
    name: "NeuroCalm-X Adaptogenic Stress Formula",
    category: "Stress & Sleep Support",
    regulatoryCategory: "AYUSH-Licensed Botanical Preparation",
    price: 1290,
    currency: "₹",
    size: "60 Veg Capsules",
    rating: 4.8,
    reviewCount: 89,
    inStock: true,
    stockCount: 74,
    consultBeforeUseRequired: false,
    canBuyDirectly: true,
    safetyNotice: "Use only as directed. Consult a qualified healthcare professional when required.",
    intendedUse: "Calms nervous tension, relieves work-related mental exhaustion, and supports daytime cognitive focus.",
    shortDescription: "Calming synergy of Nardostachys jatamansi, Lavandula stoechas (Ustukhuddus), and Centella asiatica (Brahmi).",
    fullOverview: "NeuroCalm-X soothes the excited nervous temperament (Hararat-e-Dimagh) without causing daytime sedation. It harmonizes cortisol rhythms and supports neurotransmitter resilience in chronically stressed individuals.",
    activeIngredients: [
      { commonName: "Jatamansi", botanicalName: "Nardostachys jatamansi", partUsed: "Rhizome Extract", assayStandard: "Jatamansone > 1.5% GC-MS" },
      { commonName: "Ustukhuddus", botanicalName: "Lavandula stoechas", partUsed: "Flower Extract", assayStandard: "Total Terpenes > 3%" },
      { commonName: "Brahmi Buti", botanicalName: "Centella asiatica", partUsed: "Whole Plant Extract", assayStandard: "Asiaticosides > 10%" },
      { commonName: "Shankhpushpi", botanicalName: "Convolvulus pluricaulis", partUsed: "Aerial Parts", assayStandard: "Alkaloids > 2%" }
    ],
    suggestedUsage: {
      dose: "1 capsule in the morning and 1 capsule in late afternoon",
      timing: "After meals",
      anupanVehicle: "Water or warm herbal infusion",
      durationNotes: "Safe for continuous use up to 12 weeks."
    },
    warnings: [
      "Non-drowsy, but avoid operating heavy machinery if unusually sensitive.",
      "Keep in a cool and dry location away from children."
    ],
    contraindications: [
      "Severe clinical depression without psychiatric co-management",
      "Co-administration with general anesthesia within 48 hours"
    ],
    interactionWarning: "May potentiate the sedative effects of barbiturates or benzodiazepines.",
    batchInfo: {
      lotNumber: "LOT-NCX-2026-05",
      manufacturingDate: "2026-07-20",
      expiryDate: "2028-06-30",
      heavyMetalsTested: true,
      leadPpm: "< 0.01 ppm",
      arsenicPpm: "< 0.01 ppm",
      certificateHash: "67a80b192837190a98b01298c71289301982b7190281"
    },
    manufacturer: {
      name: "ZAYVORA Health Products™",
      facility: "ZAYVORA Research & Manufacturing™ GMP Cleanroom",
      gmpLicense: "AYUSH-DL-GMP-2024-081"
    },
    faqs: [
      {
        question: "Will this cause dependency?",
        answer: "No. NeuroCalm-X contains only non-habit-forming botanical adaptogens that support your own physiological regulation."
      }
    ]
  },
  {
    id: "nightone-x",
    name: "NightOne-X Restorative Sleep Synergy",
    category: "Stress & Sleep Support",
    regulatoryCategory: "AYUSH-Licensed Botanical Preparation",
    price: 1350,
    currency: "₹",
    size: "60 Veg Capsules",
    rating: 4.9,
    reviewCount: 134,
    inStock: true,
    stockCount: 82,
    consultBeforeUseRequired: false,
    canBuyDirectly: true,
    safetyNotice: "Use only as directed. Consult a qualified healthcare professional when required.",
    intendedUse: "Promotes restful onset of sleep, eases nighttime tossing, and supports deep slow-wave restorative sleep.",
    shortDescription: "Bedtime botanical extract of Valeriana wallichii (Tagar), Withania somnifera, and Myristica fragrans.",
    fullOverview: "Formulated to alleviate nocturnal restlessness and restore cold-moist restorative tranquility (Ratab-e-Dimagh) to the brain. Free of synthetic hormones like melatonin, it allows for refreshing morning awakenings without sleep hangover.",
    activeIngredients: [
      { commonName: "Tagar Asaroon", botanicalName: "Valeriana wallichii", partUsed: "Rhizome Extract", assayStandard: "Valerenic Acid > 0.8% HPLC" },
      { commonName: "Asgandh", botanicalName: "Withania somnifera", partUsed: "Root Extract", assayStandard: "Withanolides > 2.5%" },
      { commonName: "Jaiphal", botanicalName: "Myristica fragrans", partUsed: "Kernel Extract", assayStandard: "Volatile Oil > 5%" },
      { commonName: "Kahu Beej", botanicalName: "Lactuca sativa", partUsed: "Seed Extract", assayStandard: "Lactucarium markers" }
    ],
    suggestedUsage: {
      dose: "1 to 2 capsules 45 minutes prior to bedtime",
      timing: "Nighttime before sleep",
      anupanVehicle: "Warm milk or chamomile infusion",
      durationNotes: "Can be taken nightly for 4 to 8 weeks to re-establish sleep rhythm."
    },
    warnings: [
      "Do not drive or operate machinery following consumption.",
      "Strictly adult use only (18+)."
    ],
    contraindications: [
      "Obstructive sleep apnea without CPAP therapy",
      "Concurrent high-dose sedative medications"
    ],
    interactionWarning: "Avoid alcohol consumption while taking NightOne-X.",
    batchInfo: {
      lotNumber: "LOT-NOX-2026-06",
      manufacturingDate: "2026-07-28",
      expiryDate: "2028-06-30",
      heavyMetalsTested: true,
      leadPpm: "< 0.01 ppm",
      arsenicPpm: "< 0.01 ppm",
      certificateHash: "55a9182b0918237c891273901b87192a871239b01982"
    },
    manufacturer: {
      name: "ZAYVORA Health Products™",
      facility: "ZAYVORA Research & Manufacturing™ GMP Cleanroom",
      gmpLicense: "AYUSH-DL-GMP-2024-081"
    },
    faqs: [
      {
        question: "Does this product contain melatonin?",
        answer: "No. NightOne-X is 100% botanical and does not contain synthetic melatonin, allowing your pineal gland to maintain its natural secretion."
      }
    ]
  },
  {
    id: "sleep-stress",
    name: "ZAYVORA Sleep & Stress Calming Tea Elixir",
    category: "Stress & Sleep Support",
    regulatoryCategory: "Retail Wellness Unani Formulation",
    price: 690,
    currency: "₹",
    size: "100g Loose Herbal Infusion",
    rating: 4.7,
    reviewCount: 52,
    inStock: true,
    stockCount: 160,
    consultBeforeUseRequired: false,
    canBuyDirectly: true,
    safetyNotice: "Use only as directed. Consult a qualified healthcare professional when required.",
    intendedUse: "Gentle bedtime beverage promoting evening wind-down, sensory relaxation, and digestive ease.",
    shortDescription: "Aromatic herbal blend of Chamomile, Ustukhuddus, Gul-e-Surkh (Damask Rose), and cardamom.",
    fullOverview: "A soothing evening tea blend created to replace caffeinated beverages in the late afternoon and evening. Its aromatic essential oils provide gentle olfactory calming and reduce somatic tension.",
    activeIngredients: [
      { commonName: "Babuna Phool", botanicalName: "Matricaria chamomilla", partUsed: "Flower Heads", assayStandard: "Apigenin-rich botanical standard" },
      { commonName: "Gul-e-Surkh", botanicalName: "Rosa damascena", partUsed: "Dried Rose Petals", assayStandard: "Pharmacopoeial Grade" },
      { commonName: "Badiyan", botanicalName: "Foeniculum vulgare", partUsed: "Seeds", assayStandard: "Volatile oil > 2%" },
      { commonName: "Ilaichi Sabz", botanicalName: "Elettaria cardamomum", partUsed: "Pods", assayStandard: "Essential oil rich" }
    ],
    suggestedUsage: {
      dose: "1 teaspoon steeped in 200ml freshly boiled water for 5 minutes",
      timing: "Evening around 8:00 PM",
      anupanVehicle: "Warm infusion; optionally sweetened with raw organic honey",
      durationNotes: "Daily beverage suitable for indefinite enjoyment."
    },
    warnings: [
      "Do not boil the herbs vigorously; steep covered to preserve essential aromatics."
    ],
    contraindications: [
      "Known severe allergy to Asteraceae family plants (ragweed/chamomile)"
    ],
    interactionWarning: "None reported.",
    batchInfo: {
      lotNumber: "LOT-TEA-2026-01",
      manufacturingDate: "2026-08-12",
      expiryDate: "2027-08-11",
      heavyMetalsTested: true,
      leadPpm: "< 0.01 ppm",
      arsenicPpm: "< 0.01 ppm",
      certificateHash: "44b0918237c891273901b87192a871239b0198277182"
    },
    manufacturer: {
      name: "ZAYVORA Health Products™",
      facility: "ZAYVORA Research & Manufacturing™ GMP Cleanroom",
      gmpLicense: "AYUSH-DL-GMP-2024-081"
    },
    faqs: [
      {
        question: "Can children drink this tea?",
        answer: "Yes, children over 6 years old can enjoy a mild cup with honey to help soothe evening restlessness."
      }
    ]
  },
  {
    id: "men-daily",
    name: "Men's Daily Vitality & Stamina Complex",
    category: "General Wellness",
    regulatoryCategory: "FSSAI Dietary & Nutraceutical Supplement",
    price: 1150,
    currency: "₹",
    size: "60 Tablets",
    rating: 4.8,
    reviewCount: 167,
    inStock: true,
    stockCount: 125,
    consultBeforeUseRequired: false,
    canBuyDirectly: true,
    safetyNotice: "Use only as directed. Consult a qualified healthcare professional when required.",
    intendedUse: "Daily micronutrient and botanical support for physical vigor, immune resilience, and joint mobility.",
    shortDescription: "Comprehensive multi-nutrient tablet infused with Shilajit, Gokshura, Zinc, and Vitamin D3.",
    fullOverview: "A modern dietary supplement bridging classical rejuvenators (Muqawwiyat-e-Aam) with essential modern micronutrients. Formulated to sustain peak cellular energy production throughout demanding workdays.",
    activeIngredients: [
      { commonName: "Shodhit Shilajit", botanicalName: "Asphaltum punjabianum", partUsed: "Purified Exudate", assayStandard: "Fulvic Acid > 50%" },
      { commonName: "Gokhru", botanicalName: "Tribulus terrestris", partUsed: "Fruit Extract", assayStandard: "Saponins > 40%" },
      { commonName: "Zinc Bisglycinate", botanicalName: "Chelated Mineral", partUsed: "Micronutrient", assayStandard: "12mg elemental Zinc (100% RDA)" },
      { commonName: "Vitamin D3 (Vegan)", botanicalName: "Lichen Extract", partUsed: "Micronutrient", assayStandard: "1000 IU (100% RDA)" }
    ],
    suggestedUsage: {
      dose: "1 tablet daily with breakfast",
      timing: "Morning with meal",
      anupanVehicle: "Water",
      durationNotes: "Daily nutritional foundation suitable for ongoing long-term use."
    },
    warnings: [
      "Do not take on an empty stomach to avoid minor mineral nausea.",
      "Keep bottle tightly capped in dry room temperature."
    ],
    contraindications: [
      "Hemochromatosis (iron overload disorder)",
      "Hypercalcemia"
    ],
    interactionWarning: "Take 2 hours apart from thyroid medications or fluoroquinolone antibiotics.",
    batchInfo: {
      lotNumber: "LOT-MDV-2026-11",
      manufacturingDate: "2026-08-01",
      expiryDate: "2028-07-31",
      heavyMetalsTested: true,
      leadPpm: "< 0.01 ppm",
      arsenicPpm: "< 0.01 ppm",
      certificateHash: "33c0918237c891273901b87192a871239b0198266281"
    },
    manufacturer: {
      name: "ZAYVORA Health Products™",
      facility: "ZAYVORA Research & Manufacturing™ GMP Cleanroom",
      gmpLicense: "FSSAI-LIC-100240110098"
    },
    faqs: [
      {
        question: "Can I take this if I exercise heavily?",
        answer: "Yes, the chelated zinc and Shilajit fulvic acid support post-exercise muscular recovery and cellular hydration."
      }
    ]
  }
];
