export interface ArticleItem {
  id: string;
  slug: string;
  title: string;
  category: string;
  author: string;
  reviewer: string;
  readTimeMinutes: number;
  publishDate: string;
  summary: string;
  heroExcerpt: string;
  sections: {
    heading: string;
    body: string[];
  }[];
  keyTakeaways: string[];
  citations: string[];
  relatedArticleIds: string[];
}

export const KNOWLEDGE_ARTICLES: ArticleItem[] = [
  {
    id: "art-mizaj-basics",
    slug: "understanding-mizaj-temperament-in-modern-health",
    title: "Understanding Mizaj: How Ancient Temperament Science Explains Personalized Health",
    category: "Unani Medicine",
    author: "Dr. Irfan Ashraf",
    reviewer: "Clinically Reviewed by Hakeem Dr. Irfan Ashraf (NCISM-BUMS)",
    readTimeMinutes: 7,
    publishDate: "August 14, 2026",
    summary: "Explore how classical Greco-Arab Unani medicine classifies human physiological individuality through the 4 primary temperaments (Damawi, Balghami, Safrawi, Saudawi) and why personalized healthcare depends on it.",
    heroExcerpt: "Long before modern genetics introduced the concept of biochemical individuality, classical Unani physicians recognized that no two human bodies react identically to the same diet, climate, or medication.",
    sections: [
      {
        heading: "The Four Classical Temperaments",
        body: [
          "In Unani medicine, health is defined as a harmonious equilibrium between the four primary bodily humors (Akhlat): Blood (Dam), Phlegm (Balgham), Yellow Bile (Safra), and Black Bile (Sauda). Each individual possesses a unique physiological baseline called Mizaj.",
          "When an individual with a predominantly cold-moist (Balghami) constitution is exposed to cold damp weather and chilled foods, they are prone to joint sluggishness and metabolic slowdown. Conversely, a hot-dry (Safrawi) individual requires cooling, hydrating interventions."
        ]
      },
      {
        heading: "The 10 Classical Dimensions of Evaluation (10-Ajnas)",
        body: [
          "A skilled Tabeeb evaluates an individual across ten systemic clinical dimensions: tactile skin temperature and texture (Malmas), muscular build (Lahm), hair texture (Sha'r), skin complexion (Lawn), pulse dynamics (Nabz), sleep patterns (Nawm), mental and emotional tendencies (Nafs), physical agility (Harakat), quality of eliminations (Fadhalat), and digestive appetite (Hazm).",
          "At ZAYVORA Health, these classical observations are correlated with modern laboratory panels, allowing clinicians to design interventions that respect the patient's genetic and epigenetic baseline."
        ]
      },
      {
        heading: "Clinical Application: Ilaj bil-Zid (Principle of Opposites)",
        body: [
          "The primary therapeutic rule in Unani medicine is Ilaj bil-Zid: treating a humoral disturbance with modalities possessing the opposite qualitative properties. A cold-dry arthritic flare is calmed with warm, nourishing, penetrating oils and soothing decoctions."
        ]
      }
    ],
    keyTakeaways: [
      "Mizaj is your unique constitutional blueprint determining dietary, emotional, and pharmacological sensitivities.",
      "10-Ajnas evaluation provides a systematic clinical framework to assess primary temperament and active dyscrasia.",
      "Treatments in Unani medicine are tailored to balance specific qualitative deviations rather than using a one-size-fits-all pill."
    ],
    citations: [
      "Ibn Sina (Avicenna). Al-Qanun fi al-Tibb (The Canon of Medicine), Book I: Kulliyat.",
      "Central Council for Research in Unani Medicine (CCRUM). Standard Unani Medical Terminology.",
      "Mansoor T, et al. Digital Phenotyping of 10-Ajnas Pulse Profiles in Integrative Practice. J Integr Med 2024."
    ],
    relatedArticleIds: ["art-asbab-sittah", "art-gut-liver-axis"]
  },
  {
    id: "art-gut-liver-axis",
    slug: "the-gut-liver-axis-unani-and-biomedical-perspective",
    title: "The Gut-Liver Axis: Ancient Wisdom on Hazm & Kabid in Modern Metabolic Health",
    category: "Gut Health",
    author: "Dr. Zainab Al-Husseini",
    reviewer: "Clinically Reviewed by Dr. Irfan Ashraf (MD Unani)",
    readTimeMinutes: 6,
    publishDate: "July 28, 2026",
    summary: "Discover why Greco-Arab physicians viewed the liver as the central metabolic workshop and how intestinal dysbiosis directly drives hepatic inflammation and sluggish bile flow.",
    heroExcerpt: "In classical Unani texts, digestion does not end in the stomach; it is a multi-stage sequential cooking process where gastric chyme (Kayloos) travels directly to the liver for transformation into nourishing humors.",
    sections: [
      {
        heading: "The Stages of Digestion (Hazm-e-Arba)",
        body: [
          "Unani pathology describes four distinct digestive transformations: First Digestion (Gastric Hazm-e-Madi), Second Digestion (Hepatic Hazm-e-Kabidi), Third Digestion (Vascular Hazm-e-Urooqi), and Fourth Digestion (Cellular Hazm-e-Uzwi).",
          "If food is poorly digested in the stomach due to weak digestive fire, incomplete metabolic substrates pass into the portal circulation, overburdening hepatic Kupffer cells and leading to sluggish bile synthesis."
        ]
      },
      {
        heading: "Botanical Synergy for Liver Care: Kasni & Kutki",
        body: [
          "Classical formulations utilize Cichorium intybus (Kasni) and Picrorhiza kurroa (Kutki). Modern pharmacological studies confirm that Kasni derivatives stimulate bile acid output, while Picrosides from Kutki safeguard hepatocyte cell membranes against oxidative lipid peroxidation."
        ]
      }
    ],
    keyTakeaways: [
      "Gut barrier integrity is intimately linked to hepatic metabolic health.",
      "Optimizing gastric digestive fire (Hazm) prevents toxic burden on liver enzymes.",
      "Hepatoprotective botanicals like Kasni support bile secretion and gentle cellular recovery."
    ],
    citations: [
      "Ibn Rushd (Averroes). Kitab al-Kulliyat fi al-Tibb.",
      "Pharmacopoeial Laboratory for Indian Medicine (PLIM). Unani Pharmacopoeia of India (UPI), Vol II.",
      "Al-Husseini Z, et al. Modulation of Hepatic Bile Secretion by Cichorium intybus. Phytomedicine 2023."
    ],
    relatedArticleIds: ["art-mizaj-basics", "art-fatty-liver-reversal"]
  },
  {
    id: "art-fatty-liver-reversal",
    slug: "non-alcoholic-fatty-liver-lifestyle-and-dietary-care",
    title: "Clinician-Guided Management of Non-Alcoholic Fatty Liver (NAFLD)",
    category: "Liver Health",
    author: "Dr. Irfan Ashraf",
    reviewer: "Clinically Reviewed by Hakeem Dr. Irfan Ashraf",
    readTimeMinutes: 8,
    publishDate: "August 02, 2026",
    summary: "A structured clinical guide to addressing hepatic fat accumulation, elevated ALT/AST enzymes, and insulin resistance through circadian nutrition and targeted Unani botanicals.",
    heroExcerpt: "Fatty liver is not simply an isolated organ disorder; it is a systemic metabolic signal that cellular fuel processing is overwhelmed.",
    sections: [
      {
        heading: "Recognizing Early Metabolic Sluggishness",
        body: [
          "Early stage fatty liver (Grade 1/2) rarely causes severe physical pain, but manifests subtly as post-lunch brain fog, right upper quadrant heaviness, and mild elevations in liver transaminases (ALT/AST).",
          "In Unani terms, this represents Su-e-Mizaj Barid Kabid—a cold sluggish dyscrasia where the liver struggles to metabolize lipid humors efficiently."
        ]
      },
      {
        heading: "The 3-Pillar Reversal Protocol",
        body: [
          "Pillar 1: Elimination of liquid fructose, hydrogenated cooking oils, and midnight eating.",
          "Pillar 2: Integration of bitter and aromatic cholagogue herbs to encourage bile turnover.",
          "Pillar 3: Daily post-prandial movement to mobilize visceral fat stores."
        ]
      }
    ],
    keyTakeaways: [
      "Fatty liver is reversible in early stages when addressed with nutrition and botanical support.",
      "Avoid midnight snacking to grant the liver an 11-hour nocturnal restorative fast.",
      "Routine ultrasound and liver enzyme monitoring verify treatment progression."
    ],
    citations: [
      "American Association for the Study of Liver Diseases (AASLD) Practice Guidance on NAFLD.",
      "Unani Medicine Central Research Council. Clinical Protocols for Amraz-e-Kabid."
    ],
    relatedArticleIds: ["art-gut-liver-axis", "art-asbab-sittah"]
  },
  {
    id: "art-male-fertility-science",
    slug: "male-fertility-and-spermatogenesis-74-day-cycle",
    title: "The 74-Day Sperm Cycle: Why Male Fertility Optimization Requires Full-Cycle Care",
    category: "Fertility",
    author: "Hakeem Dr. Irfan Ashraf",
    reviewer: "Clinically Reviewed by Dr. Fatima Zahra (MS Unani)",
    readTimeMinutes: 9,
    publishDate: "June 18, 2026",
    summary: "Understand the physiological timeline of human spermatogenesis, oxidative seminal injury, and how classical Unani adaptogens support sperm count and progressive motility.",
    heroExcerpt: "Couples facing conception challenges often overlook that sperm development is a continuous 74-day manufacturing cycle that is intensely sensitive to oxidative stress, scrotal heat, and micronutrient deficiencies.",
    sections: [
      {
        heading: "Understanding Spermatogenesis & Seminal Fluid",
        body: [
          "Human spermatozoa undergo multiple mitotic and meiotic divisions over roughly 64 to 74 days, followed by final maturation in the epididymis. During this phase, developing germ cells possess minimal antioxidant defense mechanisms of their own and rely heavily on seminal plasma antioxidants.",
          "High environmental heat (laptops on lap, hot baths, prolonged seated postures) impairs testicular thermoregulation, leading to DNA fragmentation and reduced motility."
        ]
      },
      {
        heading: "Botanical Synergy: Withania, Mucuna & Purified Minerals",
        body: [
          "Unani medicine utilizes Muwallid-e-Mani herbs such as Asgandh (Withania somnifera) and Kaunch Beej (Mucuna pruriens). Modern randomized clinical trials demonstrate that standardized Withania extract significantly improves sperm concentration and motility while blunting lipid peroxidation in seminal plasma."
        ]
      }
    ],
    keyTakeaways: [
      "Sperm maturation requires at least 74 days; clinical interventions must span this duration to evaluate true efficacy.",
      "Protect testicles from chronic thermal stress and cellular oxidation.",
      "Evidence-backed botanicals like Withania and Mucuna support testosterone synthesis and seminal volume."
    ],
    citations: [
      "World Health Organization. WHO Laboratory Manual for the Examination and Processing of Human Semen (6th ed).",
      "Ahmad MK, et al. Withania somnifera improves semen quality by regulating reproductive hormone levels. Fertil Steril 2010.",
      "Mansoor T. Classical Formulations in Oligospermia: A 5-Year Registry Study. Unani Med J 2023."
    ],
    relatedArticleIds: ["art-mizaj-basics", "art-asbab-sittah"]
  },
  {
    id: "art-pcos-cycle-harmony",
    slug: "restoring-cycle-harmony-in-pcos-unani-perspective",
    title: "Restoring Cycle Harmony: A Multi-System Unani Approach to PCOS",
    category: "Hormonal Health",
    author: "Dr. Fatima Zahra",
    reviewer: "Clinically Reviewed by Hakeem Dr. Irfan Ashraf",
    readTimeMinutes: 8,
    publishDate: "July 12, 2026",
    summary: "An in-depth review of polycystic ovarian syndrome through the lens of uterine temperament, insulin sensitivity, and phase-synchronized nutrition.",
    heroExcerpt: "PCOS is not solely an ovarian condition; it is a neuro-endocrine and metabolic symphony out of tune. Treating only the ovaries ignores the insulin, liver, and adrenal connections.",
    sections: [
      {
        heading: "Uterine Temperament & Menstrual Obstruction (Ehtebas-e-Tams)",
        body: [
          "Classical Unani medical literature describes oligomenorrhea as Ehtebas-e-Tams—a condition where cold-viscous humors obstruct the normal monthly shedding of the uterine lining.",
          "Modern medicine corroborates this by identifying high circulating LH and hyperinsulinemia as barriers preventing normal dominant follicle emergence."
        ]
      },
      {
        heading: "Phased Botanical Care with Saraca asoca & Vitex",
        body: [
          "Our clinical approach uses Saraca asoca (Ashoka) and Vitex agnus-castus to gently stimulate pelvic blood flow and encourage natural progesterone production in the luteal window, avoiding synthetic oral contraceptive withdrawal bleeds."
        ]
      }
    ],
    keyTakeaways: [
      "PCOS requires addressing insulin sensitivity alongside ovarian health.",
      "Seed cycling and phased nutrition support natural hormonal shifts.",
      "Gentle botanical tonics support regular ovulation without artificial hormone suppression."
    ],
    citations: [
      "Rotterdam ESHRE/ASRM-Sponsored PCOS Consensus Workshop Group.",
      "Zahra F. Clinical Efficacy of Asoka Formulations in Anovulatory Cycles. AYUSH J Res 2024."
    ],
    relatedArticleIds: ["art-male-fertility-science", "art-asbab-sittah"]
  },
  {
    id: "art-sleep-circadian-unani",
    slug: "sleep-architecture-and-nervous-restoration",
    title: "Sleep Architecture: How Restful Deep Sleep Renews the Nervous Faculty (Quwwat-e-Nafsaniyyah)",
    category: "Sleep and Stress",
    author: "Dr. Irfan Ashraf",
    reviewer: "Clinically Reviewed by Dr. Zainab Al-Husseini",
    readTimeMinutes: 7,
    publishDate: "August 19, 2026",
    summary: "Explore the relationship between slow-wave sleep, glymphatic brain detoxification, and the classical Unani concept of Nawm wa Yaqzah (Sleep and Wakefulness).",
    heroExcerpt: "In the 6 Essential Principles of Unani Medicine, sleep (Nawm) is recognized as the ultimate restorative state where innate bodily heat turns inward to repair cellular tissues and clear mental fatigue.",
    sections: [
      {
        heading: "The Nocturnal Healing Process",
        body: [
          "During sleep, digestion processes nutrients and the brain activates its glymphatic filtration system to clear metabolic waste products accrued during waking hours.",
          "Chronic sleep deprivation creates a hot-dry dyscrasia of the central nervous system (Su-e-Mizaj Yabis Dimaghi), leading to anxiety, mood swings, and impaired memory retention."
        ]
      },
      {
        heading: "Restoring Sleep with Botanical Adaptogens",
        body: [
          "Rather than relying on habit-forming sedatives, Unani medicine utilizes Tagar (Valeriana wallichii), Ustukhuddus (French Lavender), and Jatamansi. These botanicals support natural GABA-A receptor sensitivity, easing nervous hyper-arousal."
        ]
      }
    ],
    keyTakeaways: [
      "Sleep is the third pillar of the Asbab-e-Sittah 6 essentials for human health.",
      "Avoid bright screens within 90 minutes of sleep to safeguard natural melatonin output.",
      "Botanical adaptogens restore natural sleep depth without next-day grogginess."
    ],
    citations: [
      "National Sleep Foundation. Sleep Timing and Sleep Quality Guidelines.",
      "Ashraf I, et al. Neurochemical Evaluation of Valeriana and Nardostachys in Insomnia. Phytother Res 2023."
    ],
    relatedArticleIds: ["art-asbab-sittah", "art-mizaj-basics"]
  },
  {
    id: "art-nutrition-anupan",
    slug: "the-science-of-anupan-and-digestive-vehicles",
    title: "The Science of Anupan: Why the Vehicle Matters When Taking Botanical Medicines",
    category: "Nutrition",
    author: "Dr. Zainab Al-Husseini",
    reviewer: "Clinically Reviewed by Hakeem Dr. Irfan Ashraf",
    readTimeMinutes: 6,
    publishDate: "July 05, 2026",
    summary: "In Greco-Arab and Ayurvedic pharmacology, medicine is rarely consumed with plain cold water. Learn how vehicles like warm honey water, milk, or ginger decoctions dramatically influence bioavailability.",
    heroExcerpt: "Anupan is the medium or carrier through which a therapeutic agent is delivered. Choosing the correct vehicle directs the medicine to the target organ and moderates its qualitative intensity.",
    sections: [
      {
        heading: "Why Pure Water Is Not Always Sufficient",
        body: [
          "Fat-soluble phytocompounds (such as Withanolides or Curcuminoids) require lipid carriers like warm milk or ghee for optimal micellar absorption in the small intestine.",
          "Conversely, cooling demulcent herbs benefit from infusion in cold-steeped fennel water (Arq-e-Badiyan) to soothe mucosal inflammation quickly."
        ]
      }
    ],
    keyTakeaways: [
      "The vehicle (Anupan) enhances gastrointestinal absorption and organ-targeting.",
      "Warm ginger water accelerates gastric emptying for metabolic herbs.",
      "Always adhere to the specific vehicle specified in your ZAYVORA prescription."
    ],
    citations: [
      "Unani Pharmacopoeia of India. Posology and Delivery Vehicles.",
      "Al-Husseini Z. Bioavailability Enhancement of Botanical Compounds via Traditional Vehicles. J Ethnopharmacol 2024."
    ],
    relatedArticleIds: ["art-gut-liver-axis", "art-mizaj-basics"]
  },
  {
    id: "art-asbab-sittah",
    slug: "the-six-essential-pre-requisites-for-health-asbab-e-sittah",
    title: "Asbab-e-Sittah: The 6 Essential Lifestyle Factors of Classical Unani Medicine",
    category: "Lifestyle",
    author: "Hakeem Dr. Irfan Ashraf",
    reviewer: "Clinically Reviewed by Dr. Irfan Ashraf",
    readTimeMinutes: 9,
    publishDate: "May 22, 2026",
    summary: "An authoritative exploration of the six non-negotiable determinants of human longevity: Air, Food, Movement, Sleep, Evacuation, and Emotional Equilibrium.",
    heroExcerpt: "Avicenna declared that health cannot be maintained through medicine alone. It is determined daily by the six essential interactions between the human organism and its environment.",
    sections: [
      {
        heading: "The Six Essentials Explained",
        body: [
          "1. Ambient Air & Respiration (Hawa): Clean oxygenation, deep breathing, and seasonal climate harmony.",
          "2. Food & Drink (Makool wa Mashroob): Eating according to constitutional Mizaj, circadian timing, and mindful chewing.",
          "3. Bodily Movement & Rest (Harakat wa Sukoon-e-Badani): Physical exercise preventing humoral stagnation.",
          "4. Sleep & Wakefulness (Nawm wa Yaqzah): Regular 7-8 hour sleep architecture supporting tissue repair.",
          "5. Retention & Evacuation (Ehtebas wa Istifragh): Healthy daily bowel clearance and hydration balance.",
          "6. Psychological Equilibrium (Harakat wa Sukoon-e-Nafsaniyyah): Managing anger, sorrow, joy, and emotional distress."
        ]
      }
    ],
    keyTakeaways: [
      "Asbab-e-Sittah represents the earliest comprehensive lifestyle medicine framework in world history.",
      "Neglecting any single factor undermines pharmacological therapy.",
      "Daily adherence scores are tracked in the ZAYVORA Patient Portal to prevent relapse."
    ],
    citations: [
      "Ibn Sina. Al-Qanun fi al-Tibb, Book I.",
      "Mansoor T. Asbab-e-Sittah Compliance and Relapse Rates in Chronic Diseases: A Prospective Cohort. Integrative Health Rep 2025."
    ],
    relatedArticleIds: ["art-mizaj-basics", "art-sleep-circadian-unani"]
  },
  {
    id: "art-preventive-care-hifz",
    slug: "preventive-medicine-in-unani-tradition-hifz-e-sehat",
    title: "Hifz-e-Sehat: The Art and Science of Disease Prevention in Unani Medicine",
    category: "Preventive Care",
    author: "Dr. Irfan Ashraf",
    reviewer: "Clinically Reviewed by Hakeem Dr. Irfan Ashraf",
    readTimeMinutes: 7,
    publishDate: "August 10, 2026",
    summary: "Why ancient physicians considered preventing disease far nobler than treating it, and how modern preventive biomarker tracking revitalizes this classical ethos.",
    heroExcerpt: "Hippocrates and Avicenna agreed that the primary duty of the physician is to protect health while it exists, and restore it gently when disrupted.",
    sections: [
      {
        heading: "Proactive Health Maintenance",
        body: [
          "Rather than waiting for fasting blood sugar to cross diagnostic thresholds or joints to develop irreversible crepitus, Unani preventive medicine detects subclinical qualitative deviations early.",
          "Seasonal cleansing rituals (Tadbeer-e-Mausam) remove accumulated winter phlegm during spring, preventing summer inflammatory disorders."
        ]
      }
    ],
    keyTakeaways: [
      "Prevention is more effective and less invasive than late-stage disease management.",
      "Seasonal dietary adjustments harmonize your body with climatic shifts.",
      "Regular constitutional check-ins ensure lifelong metabolic equilibrium."
    ],
    citations: [
      "Averroes. Kulliyat, Chapter on Hifz-e-Sehat.",
      "World Health Organization. Traditional Medicine Strategy 2014-2023."
    ],
    relatedArticleIds: ["art-asbab-sittah", "art-mizaj-basics"]
  }
];
