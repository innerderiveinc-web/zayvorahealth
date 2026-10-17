export interface HealthProgram {
  id: string;
  title: string;
  category: "Men's Health" | "Women's Health" | "Metabolic Health" | "Gut & Liver" | "Stress & Sleep" | "General Wellness";
  shortDescription: string;
  duration: string;
  suitableAudience: string[];
  keyBenefits: string[];
  inclusions: string[];
  overview: string;
  assessmentProcess: string[];
  phases: {
    stageNumber: number;
    title: string;
    unaniName: string;
    durationDays: number;
    focus: string;
    modalities: string[];
  }[];
  lifestyleGuidance: {
    dietary: string[];
    activity: string[];
    sleep: string[];
  };
  followUpProcess: string;
  safetyInformation: string;
  faqs: { question: string; answer: string }[];
}

export const HEALTH_PROGRAMS: HealthProgram[] = [
  {
    id: "metabolic-care",
    title: "Metabolic Care & Endocrine Balance",
    category: "Metabolic Health",
    shortDescription: "Personalized care pathway targeting insulin sensitivity, liver lipid handling, and sluggish metabolic temperament (Su-e-Mizaj Barid).",
    duration: "12 to 16 Weeks",
    suitableAudience: [
      "Individuals experiencing insulin resistance or metabolic slowdown",
      "Those with pre-diabetes seeking non-invasive dietary and botanical support",
      "Patients managing abdominal weight gain and sluggish digestion",
      "Individuals with cold-moist dyscrasia affecting metabolic vitality"
    ],
    keyBenefits: [
      "Targeted optimization of cellular energy and carbohydrate handling",
      "Restoration of natural digestive warmth (Hararat-e-Ghariziyyah)",
      "Reduction in post-meal fatigue and persistent brain fog",
      "Structured dietary rhythms aligned with circadian biology"
    ],
    inclusions: [
      "Initial 10-Ajnas constitutional temperament evaluation",
      "Biomarker correlation (HbA1c, fasting insulin, lipid profile)",
      "Personalized 4-phase therapeutic nutrition protocol",
      "Doctor-curated botanical support regimen",
      "Bi-weekly telehealth follow-ups and progress tracking",
      "Continuous lifestyle & sleep coaching"
    ],
    overview: "The Metabolic Care Program addresses chronic metabolic deceleration through the combined principles of Unani medicine and modern metabolic science. Rather than viewing metabolism solely through calorie expenditure, this program evaluates the innate metabolic heat (Hararat-e-Ghariziyyah) and liver-gut-pancreas cross-talk.",
    assessmentProcess: [
      "Detailed metabolic and endocrine health history review",
      "Evaluation of primary Mizaj (temperament) and current dyscrasia",
      "Review of recent metabolic lab panels (Lipids, HbA1c, LFT)",
      "Dietary recall analysis and digestive fire (Quwwat-e-Hazima) assessment"
    ],
    phases: [
      {
        stageNumber: 1,
        title: "Humoral Cleansing",
        unaniName: "Tanqiya",
        durationDays: 14,
        focus: "Clearing accumulated metabolic residues (Balgham-e-Fasid) and decongesting hepatic pathways.",
        modalities: ["Gentle bitter aperients", "Digestive infusions (Zanjabeel & Zeera)", "Warm water regimen"]
      },
      {
        stageNumber: 2,
        title: "Metabolic Activation",
        unaniName: "Tahleel",
        durationDays: 28,
        focus: "Stimulating cellular thermogenesis and restoring insulin receptor sensitivity.",
        modalities: ["MetaboCore botanical synergy", "Targeted post-meal walks", "Low-glycemic culinary spices"]
      },
      {
        stageNumber: 3,
        title: "Organ Tonification",
        unaniName: "Taqwiyaat",
        durationDays: 28,
        focus: "Nourishing hepatic parenchyma and balancing endocrine signaling pathways.",
        modalities: ["Kalonji & Gudmar botanical extracts", "Mizaj-specific protein balancing", "Sleep stabilization"]
      },
      {
        stageNumber: 4,
        title: "Equilibrium Preservation",
        unaniName: "Hifz",
        durationDays: 42,
        focus: "Long-term lifestyle and dietary habits to maintain stable blood sugar and vitality.",
        modalities: ["Asbab-e-Sittah self-care guidelines", "Monthly maintenance check-ins", "Sustainable nutritional routine"]
      }
    ],
    lifestyleGuidance: {
      dietary: [
        "Prioritize warm, light meals cooked with digestive spices (cumin, fenugreek, ginger)",
        "Strictly avoid chilled, sweetened beverages and refined carbohydrates",
        "Conclude dinner at least 3 hours prior to sleep"
      ],
      activity: [
        "15-minute brisk walk following main meals to blunt glucose excursions",
        "30 minutes of low-impact aerobic activity 4 times per week"
      ],
      sleep: [
        "Maintain consistent sleep-wake timing between 10:00 PM and 6:30 AM",
        "Dark, quiet sleep environment to support nighttime hormonal rhythm"
      ]
    },
    followUpProcess: "Scheduled consultations occur at Day 14, Day 42, Day 70, and completion at Day 112. Patients log weekly fasting readings and digestive comfort scores via the ZAYVORA Patient Portal.",
    safetyInformation: "This program is clinician-supervised. Patients on prescription hypoglycemic medications will have their doses monitored in coordination with their primary prescribing physician to prevent hypoglycemia.",
    faqs: [
      {
        question: "Can this program replace my current diabetes medication?",
        answer: "No. ZAYVORA programs are complementary and clinician-guided. We work alongside your existing medical management, and any medication modifications must be approved by your treating physician."
      },
      {
        question: "Is this program suitable for gestational diabetes?",
        answer: "No. Pregnant women require specialized obstetric protocols and are referred to hospital-based maternal care."
      }
    ]
  },
  {
    id: "male-fertility-care",
    title: "Male Fertility & Reproductive Health",
    category: "Men's Health",
    shortDescription: "Evidence-informed protocol supporting sperm count, motility, morphology, and seminal fluid vitality (Quwwat-e-Bah).",
    duration: "12 to 14 Weeks",
    suitableAudience: [
      "Men seeking to optimize semen parameters prior to conception",
      "Couples navigating delayed conception seeking male factor support",
      "Men managing low vitality, fatigue, and stress-related reproductive strain",
      "Individuals recovering from oxidative stress and environmental toxic exposure"
    ],
    keyBenefits: [
      "Support for healthy spermatogenesis during the 74-day sperm cycle",
      "Protection against seminal oxidative damage with potent botanical antioxidants",
      "Optimization of testicular microcirculation and endocrine tone",
      "Enhanced physical stamina and restorative deep sleep"
    ],
    inclusions: [
      "Comprehensive semen analysis report review and history mapping",
      "Personalized 3-stage reproductive care pathway",
      "Prescription-grade standardized botanical compounds (Withania, Mucuna, Safed Musli)",
      "Dietary micro-nutrient and zinc-rich nutritional plan",
      "Monthly semen parameter reviews and clinical oversight"
    ],
    overview: "Spermatogenesis requires approximately 74 days. The ZAYVORA Male Fertility Care Program provides full-cycle support addressing the underlying nutritional, vascular, and humoral factors that determine sperm health, concentration, and progressive motility.",
    assessmentProcess: [
      "Comprehensive semen analysis (WHO 6th edition criteria)",
      "Assessment of reproductive heat balance and testicular thermoregulation",
      "Review of occupational exposures, heat, and chemical stressors",
      "Stress and adrenal axis evaluation"
    ],
    phases: [
      {
        stageNumber: 1,
        title: "Oxidative Decongestion",
        unaniName: "Tanqiya",
        durationDays: 14,
        focus: "Clearing systemic metabolic waste and minimizing seminal oxidative stress.",
        modalities: ["Antioxidant herbal infusions", "Elimination of heat-generating foods", "Cold-hip bath guidance"]
      },
      {
        stageNumber: 2,
        title: "Nutritive Spermatogenesis",
        unaniName: "Taqwiyaat",
        durationDays: 56,
        focus: "Providing deep nutrient substrates for developing sperm cells throughout their 74-day maturation.",
        modalities: ["ManiVital Pro standardized formulation", "Qurs-e-Kushta-e-Qalai (where indicated)", "Nutritive nuts & seeds regimen"]
      },
      {
        stageNumber: 3,
        title: "Maturity & Preservation",
        unaniName: "Hifz",
        durationDays: 28,
        focus: "Stabilizing seminal morphology and preparing for optimal conception timing.",
        modalities: ["Follow-up semen analysis", "Lifestyle pacing protocol", "Stress reduction practices"]
      }
    ],
    lifestyleGuidance: {
      dietary: [
        "Incorporate raw walnuts, pumpkin seeds, soaked almonds, and pomegranate juice",
        "Avoid tobacco, alcohol, and excessive caffeine which impair motility",
        "Minimize consumption of processed, high-sodium foods"
      ],
      activity: [
        "Moderate aerobic exercise; avoid prolonged cycling or tight athletic gear",
        "Maintain scrotal coolness by avoiding saunas, hot tubs, and laptop on lap"
      ],
      sleep: [
        "Aim for 8 hours of uninterrupted sleep to support peak morning testosterone synthesis"
      ]
    },
    followUpProcess: "A baseline semen test is logged at week 0, followed by mid-protocol check-in at week 6, and a repeat semen analysis at week 12.",
    safetyInformation: "Formulations used are free of synthetic hormones and heavy metal adulteration. All classical minerals are purified strictly via Mudabbar pharmacopoeial protocols.",
    faqs: [
      {
        question: "How long before we see improvements in sperm tests?",
        answer: "Because sperm development takes about 74 days, measurable changes in semen analysis are typically evaluated after 10 to 12 weeks of consistent care."
      },
      {
        question: "Are these formulations safe for long-term use?",
        answer: "Yes, our botanicals are adapted for cycle-based usage under clinician supervision."
      }
    ]
  },
  {
    id: "female-hormonal-care",
    title: "Female Hormonal Health & Ovarian Wellness",
    category: "Women's Health",
    shortDescription: "Gentle, non-invasive support for cycle regularity, PCOS management, pelvic comfort, and reproductive vitality.",
    duration: "12 to 20 Weeks",
    suitableAudience: [
      "Women with irregular cycles, delayed periods, or anovulatory patterns",
      "Those navigating PCOS, androgen excess, or facial hair/acne concerns",
      "Women experiencing intense pre-menstrual mood changes and cramping",
      "Women planning for pregnancy seeking natural cycle harmonization"
    ],
    keyBenefits: [
      "Supports healthy hypothalamic-pituitary-ovarian (HPO) axis signaling",
      "Assists in clearing pelvic congestion and restoring healthy menstrual flow",
      "Nutritional modulation of insulin sensitivity in PCOS phenotypes",
      "Gentle botanical tonification of uterine musculature (Reham)"
    ],
    inclusions: [
      "Menstrual cycle history and symptom tracking audit",
      "Pelvic ultrasound and hormonal lab review (LH/FSH, AMH, Prolactin)",
      "Phased dietary regimen tailored to follicular and luteal phases",
      "Clinician-supervised Unani herbal formulation (OvaSync synergy)",
      "Monthly telehealth evaluation during post-menses window"
    ],
    overview: "Female hormonal health is viewed in Unani medicine through the lens of uterine temperament (Mizaj-e-Reham) and unobstructed menstrual cleansing (Ehtebas-e-Tams). The program combines phase-specific nutrition with classical botanicals like Saraca asoca, Aloe barbadensis, and Vitex agnus-castus.",
    assessmentProcess: [
      "Detailed cycle log analysis over previous 6 months",
      "Assessment of uterine temperament (Barid / Yabis vs Har / Ratab)",
      "Thyroid, prolactin, and fasting insulin correlation",
      "Pelvic pain and dysmenorrhea intensity scoring"
    ],
    phases: [
      {
        stageNumber: 1,
        title: "Pelvic Decongestion",
        unaniName: "Tanqiya",
        durationDays: 21,
        focus: "Clearing accumulated phlegmatic barriers and supporting gentle pelvic circulation.",
        modalities: ["Emmenagogue botanical teas", "Warm sesame oil lower abdomen compress", "Inflammation-reducing dietary shift"]
      },
      {
        stageNumber: 2,
        title: "Follicular Harmonization",
        unaniName: "Tahleel",
        durationDays: 42,
        focus: "Encouraging regular follicular recruitment and insulin receptor responsiveness.",
        modalities: ["OvaSync botanical blend", "Seed cycling protocol", "Resistance-based muscle activation"]
      },
      {
        stageNumber: 3,
        title: "Uterine Nourishment",
        unaniName: "Taqwiyaat",
        durationDays: 28,
        focus: "Strengthening endometrium and supporting optimal progesterone output.",
        modalities: ["Ashoka and Shatavari restorative syrups", "Stress-reducing breathwork", "Iron and folate dense nutrition"]
      }
    ],
    lifestyleGuidance: {
      dietary: [
        "Follicular phase: Incorporate flaxseeds, pumpkin seeds, and leafy greens",
        "Luteal phase: Add sunflower and sesame seeds, root vegetables, and warm bone broths",
        "Eliminate refined vegetable oils and excess dairy during active congestion"
      ],
      activity: [
        "Dynamic yoga and walking during follicular phase; restorative stretching during menses"
      ],
      sleep: [
        "Prioritize deep sleep during the pre-menstrual week to ease emotional irritability"
      ]
    },
    followUpProcess: "Review appointments are synchronized with the first week after menses to evaluate flow duration, color, clot formation, and symptom changes.",
    safetyInformation: "Not recommended during active pregnancy. If pregnancy occurs while on the program, formulations are immediately paused and transitioned to prenatal care.",
    faqs: [
      {
        question: "Can this program cure PCOS?",
        answer: "PCOS is a chronic metabolic-endocrine condition. This program does not claim a permanent cure, but provides clinical management to restore ovulation, ease symptoms, and support cycle regularity."
      }
    ]
  },
  {
    id: "gut-liver-care",
    title: "Gut & Liver Axis (Hazm & Kabid Support)",
    category: "Gut & Liver",
    shortDescription: "Integrative restorative protocol for sluggish liver, fatty infiltration grade I/II, chronic acidity, bloating, and IBS.",
    duration: "8 to 12 Weeks",
    suitableAudience: [
      "Individuals with non-alcoholic fatty liver changes on ultrasound",
      "Those suffering from chronic bloating, indigestion, or erratic bowel habits (IBS)",
      "Patients recovering from prolonged antibiotic use or sluggish bile flow",
      "Individuals with elevated liver enzymes (SGOT/SGPT) needing lifestyle guidance"
    ],
    keyBenefits: [
      "Enhancement of hepatic detoxifying capacity and bile synthesis",
      "Soothes gastric mucosa and eases acid reflux sensations",
      "Harmonizes intestinal microbiome and reduces abdominal distension",
      "Improves overall nutrient assimilation and energy levels"
    ],
    inclusions: [
      "Liver ultrasound review and hepatic panel assessment",
      "Gastric digestive fire (Quwwat-e-Hazima) categorization",
      "LiverPrime Core botanical extract protocol (Picrorhiza, Kasni, Giloy)",
      "Anti-inflammatory digestive diet plan",
      "Progress tracking for bloating, stool consistency, and energy"
    ],
    overview: "In classical Unani pathology, the liver (Kabid) is the central laboratory of the body where all four humors (Akhlat) are formed. Poor gastric digestion produces imperfect chyme (Kayloos), placing immense burden on the liver. This program simultaneously repairs the gut barrier and decongests hepatic tissue.",
    assessmentProcess: [
      "Assessment of tongue coating (Lisan) and bitter taste in mouth",
      "Review of liver ultrasound, AST, ALT, GGT, and lipid profiles",
      "Mapping of bowel transit time and Bristol Stool Scale logging",
      "Screening for food intolerances and medication histories"
    ],
    phases: [
      {
        stageNumber: 1,
        title: "Biliary Decongestion",
        unaniName: "Tanqiya",
        durationDays: 14,
        focus: "Promoting healthy bile flow and clearing mucosal sluggishness.",
        modalities: ["Kasni (Cichorium intybus) decoctions", "Warm fennel water", "Light cooked diet"]
      },
      {
        stageNumber: 2,
        title: "Hepatoprotective Regeneration",
        unaniName: "Tahleel",
        durationDays: 28,
        focus: "Supporting liver enzyme normalization and membrane stabilization.",
        modalities: ["LiverPrime Core botanical capsules", "Milk thistle & Kutki synergy", "Anti-inflammatory dietary protocol"]
      },
      {
        stageNumber: 3,
        title: "Digestive Equilibrium",
        unaniName: "Taqwiyaat",
        durationDays: 28,
        focus: "Strengthening gastric tone and establishing long-term microbiome stability.",
        modalities: ["Jawarish-style digestive confection", "Fermented probiotic foods", "Circadian meal timing"]
      }
    ],
    lifestyleGuidance: {
      dietary: [
        "Include bitter greens (dandelion, fenugreek leaves), beetroot, and lemon water",
        "Strictly avoid deep-fried foods, hydrogenated oils, alcohol, and refined sugar",
        "Chew food thoroughly; drink liquids between meals rather than with meals"
      ],
      activity: [
        "Daily 30-minute brisk walk to encourage bile ejection and visceral mobility"
      ],
      sleep: [
        "Avoid eating after 8:00 PM to give the liver undisturbed nocturnal rejuvenation"
      ]
    },
    followUpProcess: "LFT lab tests are reassessed at week 8 to monitor enzyme trajectories alongside clinician review.",
    safetyInformation: "Patients with acute viral hepatitis, gallstone impaction, or cirrhosis require immediate in-person hepatology evaluation and are excluded from self-guided programs.",
    faqs: [
      {
        question: "How does Kasni (chicory) help the liver?",
        answer: "Kasni is a premier Unani hepatoprotective herb recognized for stimulating bile secretion, easing liver congestion, and mitigating mild hepatic inflammation."
      }
    ]
  },
  {
    id: "stress-sleep-care",
    title: "Stress, Anxiety & Sleep Care (Asab & Dimagh)",
    category: "Stress & Sleep",
    shortDescription: "Holistic protocol calming hyperactive nervous tension, adrenal burnout, mental fatigue, and sleep maintenance insomnia.",
    duration: "6 to 10 Weeks",
    suitableAudience: [
      "Working professionals experiencing chronic mental fatigue and burnout",
      "Individuals suffering from racing thoughts at night and frequent awakenings",
      "Those with tension headaches, muscular tightness, and nervous indigestion",
      "Patients seeking non-habit-forming, natural botanical sleep support"
    ],
    keyBenefits: [
      "Calms nervous excitability (Taskeen-e-Asab) without daytime grogginess",
      "Promotes deep restorative slow-wave sleep architecture",
      "Supports healthy evening cortisol decline and melatonin secretion",
      "Improves daytime focus, emotional equilibrium, and cognitive stamina"
    ],
    inclusions: [
      "Sleep architecture audit (latency, awakenings, daytime alertness)",
      "Brain and nervous temperament (Mizaj-e-Dimagh) assessment",
      "NeuroCalm-X botanical synergy (Brahmi, Ustukhuddus, Jatamansi)",
      "Classical Unani head massage (Natool/Tadbeer) guidance",
      "Sleep hygiene and nervous system regulation workbook"
    ],
    overview: "Mental stress and sleep disruption are viewed in Unani medicine as dry-hot or dry-cold dyscrasias of the brain (Su-e-Mizaj Dimaghi). Our protocol provides soothing moisture and gentle warmth (Tarteeb wa Taskeen) to the nervous system through evidence-backed adaptogens and evening rituals.",
    assessmentProcess: [
      "Pittsburgh Sleep Quality Index (PSQI) evaluation",
      "Screening for physiological causes (iron deficiency, thyroid, sleep apnea)",
      "Mapping daily caffeine, screen time, and work stressors",
      "Evaluation of emotional temperament (Nafs) and somatic anxiety signs"
    ],
    phases: [
      {
        stageNumber: 1,
        title: "Sensory Calming",
        unaniName: "Taskeen",
        durationDays: 14,
        focus: "Down-regulating sympathetic nervous fight-or-flight dominance.",
        modalities: ["Ustukhuddus (French Lavender) evening infusion", "Digital screen curfew at 9 PM", "Gentle scalp oiling (Roghan-e-Kahu)"]
      },
      {
        stageNumber: 2,
        title: "Neuro-Nutritive Tonification",
        unaniName: "Taqwiyaat",
        durationDays: 28,
        focus: "Replenishing neurochemical reserves and improving sleep depth.",
        modalities: ["NeuroCalm-X formulation", "Ashwagandha with warm almond milk", "Diaphragmatic breathwork"]
      },
      {
        stageNumber: 3,
        title: "Circadian Anchoring",
        unaniName: "Hifz",
        durationDays: 14,
        focus: "Solidifying robust 24-hour circadian rhythmicity and stress resilience.",
        modalities: ["Morning sunlight exposure within 30 minutes of waking", "Sustained lifestyle rituals"]
      }
    ],
    lifestyleGuidance: {
      dietary: [
        "Include warm milk with nutmeg, soaked almonds, pumpkin seeds, and dates",
        "Zero caffeine intake after 1:00 PM",
        "Avoid heavy meals right before bedtime"
      ],
      activity: [
        "Gentle evening walking, gentle yoga, and avoiding intense nighttime workouts"
      ],
      sleep: [
        "Bedroom kept cool (18°C–20°C), dark, and free of blue light screens"
      ]
    },
    followUpProcess: "Weekly digital sleep logs submitted through the portal; clinician reviews at weeks 2, 6, and 10.",
    safetyInformation: "Our formulations are 100% free of benzodiazepines, sedatives, or synthetic melatonin. Safe and non-habit forming.",
    faqs: [
      {
        question: "Will I feel groggy the next morning?",
        answer: "No. The botanicals support your natural GABAergic and parasympathetic systems rather than forcing artificial sedation."
      }
    ]
  },
  {
    id: "general-vitality",
    title: "General Vitality & Rejuvenation (Hifz-e-Sehat)",
    category: "General Wellness",
    shortDescription: "Classical preventive regimen enhancing innate immune resilience (Tabi'at), cellular longevity, and vital energy.",
    duration: "8 to 12 Weeks",
    suitableAudience: [
      "Healthy adults seeking preventive health maintenance and vitality",
      "Individuals recovering from seasonal illness or physical fatigue",
      "Older adults wishing to maintain joint, digestive, and cognitive vigor",
      "Anyone seeking a structured seasonal routine (Tadbeer-e-Mausam)"
    ],
    keyBenefits: [
      "Strengthens innate healing faculty (Tabi'at-e-Mudabbira-e-Badan)",
      "Enhances cellular resilience against environmental and seasonal stressors",
      "Optimizes gastrointestinal assimilation of vital micronutrients",
      "Promotes sustained daytime stamina and clear mental acuity"
    ],
    inclusions: [
      "Preventive 10-Ajnas constitutional health audit",
      "Seasonal health regimen (Tadbeer-e-Mausam) customized to climate",
      "Daily botanical tonic (Khamira / Arq synergy)",
      "Asbab-e-Sittah 6 Essential Lifestyle Factors personal guide",
      "Quarterly preventive doctor consultation"
    ],
    overview: "Preventive medicine (Hifz-e-Sehat) is the crown jewel of Unani clinical philosophy. Rather than waiting for disease manifestation, this program fortifies the internal physician within the body—Tabi'at—through balanced nutrition, seasonal adaptations, and classical rasayana tonics.",
    assessmentProcess: [
      "Evaluation of constitutional baseline and seasonal vulnerabilities",
      "Routine preventive metabolic and immune blood check review",
      "Analysis of daily energy curves and recovery rates"
    ],
    phases: [
      {
        stageNumber: 1,
        title: "Harmonization",
        unaniName: "Ta'deel",
        durationDays: 14,
        focus: "Normalizing mild humoral imbalances before they manifest as disease.",
        modalities: ["Seasonal digestive infusions", "Gentle dietary reset"]
      },
      {
        stageNumber: 2,
        title: "Vital Force Tonification",
        unaniName: "Taqwiyaat",
        durationDays: 42,
        focus: "Nourishing vital organs (Heart, Brain, Liver) with adaptogenic confections.",
        modalities: ["Men's / Women's Daily Vitality synergy", "Antioxidant botanical elixirs"]
      },
      {
        stageNumber: 3,
        title: "Long-term Maintenance",
        unaniName: "Hifz",
        durationDays: 28,
        focus: "Sustaining radiant well-being throughout changing seasons.",
        modalities: ["Asbab-e-Sittah daily routine", "Preventive tracking"]
      }
    ],
    lifestyleGuidance: {
      dietary: [
        "Eat seasonally and locally; respect constitutional affinities",
        "Eat when truly hungry and stop before complete fullness"
      ],
      activity: [
        "Regular, joyful movement aligned with your natural build and age"
      ],
      sleep: [
        "7 to 8 hours of restorative sleep aligned with natural daylight cycles"
      ]
    },
    followUpProcess: "Quarterly review with a certified Tabeeb for seasonal regimen adjustment.",
    safetyInformation: "Suitable for general adult use. Not intended for the treatment of acute medical emergencies.",
    faqs: [
      {
        question: "What does Tabi'at mean in Unani medicine?",
        answer: "Tabi'at refers to the body's innate self-regulating and self-healing intelligence. In modern terms, it encompasses immune homeostasis, physiological repair, and autonomic balance."
      }
    ]
  }
];
