// ZAYVORA Master Clinical Protocols (P-01 to P-21)
// Source: ZAYVORA Master Clinical System (Dr. Irfan Ashraf)

export interface ProtocolPhaseProduct {
  name: string;
  dose: string;
  timing: string;
  rationale?: string;
}

export interface ProtocolPhase {
  title: string;
  duration_days: number | string;
  products: ProtocolPhaseProduct[];
  diet?: string;
  monitoring?: string;
  exercise?: string;
  investigation?: string;
}

export interface ProtocolProductStack {
  core: string[];
  support: string[];
  modulator: string[];
}

export interface MasterProtocol {
  id: string;
  name: string;
  category: string;
  primary_axis: string;
  secondary_axis?: string;
  indication: string;
  phase1: ProtocolPhase;
  phase2: ProtocolPhase;
  phase3: ProtocolPhase;
  product_stack: ProtocolProductStack;
  lab_monitoring: string[];
  clinical_warnings: string[];
  protocol_kit_id: string;
  protocol_kit_name: string;
  kit_price_range: string;
}

export const MASTER_PROTOCOLS: MasterProtocol[] = [
  {
    "id": "P-01",
    "name": "Type 2 Diabetes Protocol",
    "category": "METABOLIC",
    "primary_axis": "Jigar-Banas",
    "secondary_axis": "Meda-Hazm",
    "indication": "FBS >126; HbA1c >6.5%; Post-prandial >200; Metabolic syndrome with glucose dysregulation",
    "phase1": {
      "title": "Jigar Reset + Gut Axis",
      "duration_days": 30,
      "products": [
        {
          "name": "HepaClear",
          "dose": "4 caps/day",
          "timing": "AM empty + PM",
          "rationale": "Hepatic fat clearance, AMPK steatosis reversal, Kupffer anti-inflammation"
        },
        {
          "name": "GutEase-IBS",
          "dose": "4 caps/day",
          "timing": "pre-meal",
          "rationale": "Gut microbiome reset (dysbiosis drives insulin resistance)"
        }
      ],
      "diet": "Remove refined carbs, increase fibre; fasting window 14-10 hours; stop all processed sugar, maida, refined oil."
    },
    "phase2": {
      "title": "Glucose Control",
      "duration_days": 90,
      "products": [
        {
          "name": "DiabEase",
          "dose": "4 caps/day",
          "timing": "Pre-meal (lunch+dinner)",
          "rationale": "Berberine 600mg/day AMPK + Jamun alpha-glucosidase + Gurmar beta-cell regeneration"
        },
        {
          "name": "HepaClear",
          "dose": "2 caps/day",
          "timing": "maintenance",
          "rationale": "Hepato-metabolic maintenance"
        },
        {
          "name": "MindBalance",
          "dose": "2 caps/day",
          "timing": "bedtime",
          "rationale": "Cortisol-driven glucose dysregulation correction"
        }
      ],
      "monitoring": "FBS monitoring every 2 weeks; HbA1c at 90 days."
    },
    "phase3": {
      "title": "Long-term Maintenance",
      "duration_days": "Ongoing",
      "products": [
        {
          "name": "Sugar Care",
          "dose": "4 caps/day",
          "timing": "Pre-meal",
          "rationale": "Lower dose glucose maintenance"
        },
        {
          "name": "Men Daily / Women Daily",
          "dose": "2 caps/day",
          "timing": "AM with food",
          "rationale": "Daily micronutrient support"
        },
        {
          "name": "HepaClear",
          "dose": "1 cap/day",
          "timing": "daily",
          "rationale": "Long-term NAFLD maintenance"
        }
      ],
      "monitoring": "Annual: LFT, lipid panel, HbA1c, VitD3, serum zinc."
    },
    "product_stack": {
      "core": [
        "DiabEase",
        "HepaClear"
      ],
      "support": [
        "MindBalance",
        "GutEase-IBS"
      ],
      "modulator": [
        "Sugar Care"
      ]
    },
    "lab_monitoring": [
      "FBS (2-weekly Phase 2)",
      "HbA1c (90 days)",
      "PP Glucose (90 days)",
      "LFT (0, 90 days)",
      "Lipid panel (90 days)",
      "Serum Insulin + HOMA-IR (0, 90 days)",
      "Vitamin D3 (baseline)"
    ],
    "clinical_warnings": [
      "NEVER replace prescribed antidiabetics.",
      "Monitor for hypoglycaemia especially if on sulphonylureas or insulin.",
      "Berberine + Metformin = additive \u2014 physician monitoring for lactic acidosis risk.",
      "Adjust Metformin dose only under physician supervision."
    ],
    "protocol_kit_id": "K-01",
    "protocol_kit_name": "DIABETES CONTROL KIT",
    "kit_price_range": "Rs. 3,800 - Rs. 5,500/month"
  },
  {
    "id": "P-02",
    "name": "Obesity & Metabolic Syndrome Protocol",
    "category": "METABOLIC",
    "primary_axis": "Jigar-Dam",
    "secondary_axis": "Meda-Amaa",
    "indication": "BMI >25; Waist >90cm(M)/>80cm(F); Metabolic syndrome (HTN+DM+Dyslipidemia+Obesity)",
    "phase1": {
      "title": "Liver + Gut Detox",
      "duration_days": 30,
      "products": [
        {
          "name": "HepaClear",
          "dose": "4 caps/day",
          "timing": "AM empty + PM",
          "rationale": "NAFLD reversal is prerequisite for weight loss"
        },
        {
          "name": "GutEase-IBS",
          "dose": "4 caps/day",
          "timing": "pre-meal",
          "rationale": "Gut microbiome reset; L-Glutamine sealing leaky gut"
        },
        {
          "name": "LipidClear",
          "dose": "1 cap/day",
          "timing": "morning with 250ml water",
          "rationale": "Initiate lipid normalisation"
        }
      ],
      "diet": "Caloric deficit: 500 kcal below TDEE; Mediterranean-style diet; 16:8 IF."
    },
    "phase2": {
      "title": "Active Fat Mobilisation",
      "duration_days": 60,
      "products": [
        {
          "name": "MetaboBurn-M",
          "dose": "4 caps/day",
          "timing": "Pre-meal (3 times daily)",
          "rationale": "Green Coffee AMPK + Garcinia HCA lipogenesis block + Guggul FXR thermogenesis"
        },
        {
          "name": "HepaClear",
          "dose": "2 caps/day",
          "timing": "maintenance",
          "rationale": "Hepatic support"
        },
        {
          "name": "LipidClear",
          "dose": "2 caps/day",
          "timing": "full dose with water",
          "rationale": "Bile binding and lipid reduction"
        },
        {
          "name": "MindBalance",
          "dose": "1-2 caps/day",
          "timing": "bedtime",
          "rationale": "Cortisol-driven abdominal obesity control"
        }
      ],
      "exercise": "30 min brisk walk 5x/week minimum."
    },
    "phase3": {
      "title": "Weight Maintenance",
      "duration_days": "Ongoing",
      "products": [
        {
          "name": "MetaboBurn-M",
          "dose": "2 caps/day",
          "timing": "morning",
          "rationale": "Half dose maintenance"
        },
        {
          "name": "HepaClear",
          "dose": "1 cap/day",
          "timing": "daily",
          "rationale": "Hepatic maintenance"
        },
        {
          "name": "Sugar Care",
          "dose": "2 caps/day",
          "timing": "as needed",
          "rationale": "If metabolic syndrome persists"
        }
      ],
      "monitoring": "Quarterly: lipid panel, FBS, LFT, waist circumference."
    },
    "product_stack": {
      "core": [
        "MetaboBurn-M",
        "HepaClear",
        "LipidClear"
      ],
      "support": [
        "GutEase-IBS",
        "MindBalance"
      ],
      "modulator": [
        "Sugar Care"
      ]
    },
    "lab_monitoring": [
      "Weight + waist (monthly)",
      "Fasting lipid panel (45-day)",
      "FBS + HOMA-IR (0, 90)",
      "LFT (0, 90)",
      "BMI trend"
    ],
    "clinical_warnings": [
      "MetaboBurn-M is adjunct to caloric restriction \u2014 not standalone.",
      "Isabgol: 250ml water per dose mandatory.",
      "Monitor TSH at baseline (Guggul thyroid effect)."
    ],
    "protocol_kit_id": "K-02",
    "protocol_kit_name": "METABOLIC BURN KIT",
    "kit_price_range": "Rs. 4,000 - Rs. 6,000/month"
  },
  {
    "id": "P-03",
    "name": "Dyslipidaemia & Lipid Management Protocol",
    "category": "METABOLIC",
    "primary_axis": "Jigar-Dam",
    "secondary_axis": "Qalb-Uroq",
    "indication": "LDL >130; TG >150; HDL <40(M)/<50(F); Combined dyslipidemia; Statin-intolerant patients",
    "phase1": {
      "title": "Hepatic Reset",
      "duration_days": 30,
      "products": [
        {
          "name": "HepaClear",
          "dose": "4 caps/day",
          "timing": "AM empty + PM",
          "rationale": "Liver dysfunction drives dyslipidemia"
        },
        {
          "name": "DiabEase",
          "dose": "2 caps/day",
          "timing": "if T2DM comorbid",
          "rationale": "Insulin resistance drives VLDL output"
        }
      ],
      "diet": "Remove trans fats, increase soluble fibre (Isabgol), omega-3 foods."
    },
    "phase2": {
      "title": "Active Lipid Management",
      "duration_days": 90,
      "products": [
        {
          "name": "LipidClear",
          "dose": "2 caps/day",
          "timing": "Empty stomach (AM+PM) with 250ml water",
          "rationale": "Guggul FXR+thyroid + Berberine PCSK9-like + Isabgol bile-binding + Artichoke Cynarin"
        },
        {
          "name": "HepaClear",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "Hepatic clearance continuation"
        },
        {
          "name": "CardioGuard",
          "dose": "1-2 caps/day",
          "timing": "daily",
          "rationale": "If IHD or CVD risk present"
        }
      ],
      "monitoring": "MANDATORY: 250ml water with LipidClear each dose."
    },
    "phase3": {
      "title": "Maintenance",
      "duration_days": "Ongoing",
      "products": [
        {
          "name": "LipidClear",
          "dose": "1-2 caps/day",
          "timing": "daily",
          "rationale": "Long-term lipid maintenance"
        }
      ],
      "monitoring": "Annual lipid panel; LFT check."
    },
    "product_stack": {
      "core": [
        "LipidClear",
        "HepaClear"
      ],
      "support": [
        "CardioGuard",
        "DiabEase"
      ],
      "modulator": [
        "MetaboBurn-M"
      ]
    },
    "lab_monitoring": [
      "Fasting lipid panel (0, 45, 90)",
      "LFT (0, 90)",
      "TSH (baseline and 90 days)",
      "FBS if DM comorbid"
    ],
    "clinical_warnings": [
      "LipidClear: 250ml water per dose mandatory (Isabgol obstruction risk).",
      "Monitor TSH \u2014 Guggul activates thyroid receptor.",
      "Continue statin if prescribed \u2014 additive lipid lowering."
    ],
    "protocol_kit_id": "K-03",
    "protocol_kit_name": "LIPID MANAGEMENT KIT",
    "kit_price_range": "Rs. 3,500 - Rs. 5,000/month"
  },
  {
    "id": "P-04",
    "name": "Hypertension Management Protocol",
    "category": "CARDIO",
    "primary_axis": "Qalb-Uroq",
    "secondary_axis": "Dimagh-Kulya",
    "indication": "BP 130-179/80-109; Stage 1 or Stage 2 HTN; Adjunct to antihypertensives; White-coat HTN",
    "phase1": {
      "title": "Sympathetic Calming",
      "duration_days": 30,
      "products": [
        {
          "name": "HyperCalm",
          "dose": "4 caps/day",
          "timing": "AM before food + PM before dinner",
          "rationale": "Sarpagandha sympatholysis + Arjun 200mg PDE + CoQ10 endothelial support"
        },
        {
          "name": "MindBalance",
          "dose": "3 caps/day",
          "timing": "1 AM + 2 bedtime",
          "rationale": "HPA-cortisol driven HTN; GABA calming"
        },
        {
          "name": "Sleep+Stress",
          "dose": "2 caps/day",
          "timing": "bedtime",
          "rationale": "Sleep quality critical for BP normalisation"
        }
      ],
      "monitoring": "Monitor BP at home twice daily; log every reading."
    },
    "phase2": {
      "title": "Cardiovascular Reinforcement",
      "duration_days": 60,
      "products": [
        {
          "name": "HyperCalm",
          "dose": "4 caps/day",
          "timing": "AM+PM",
          "rationale": "Continued BP modulation"
        },
        {
          "name": "CardioGuard",
          "dose": "2 caps/day",
          "timing": "AM warm milk + PM",
          "rationale": "Arjun cardiotonic + Nattokinase + CoQ10 endothelial + Shilajit"
        },
        {
          "name": "LipidClear",
          "dose": "2 caps/day",
          "timing": "if dyslipidemia present",
          "rationale": "Atherosclerotic BP reduction"
        }
      ],
      "diet": "DASH diet; sodium <2g/day; increase potassium foods; quit tobacco."
    },
    "phase3": {
      "title": "Long-term Cardiac Protection",
      "duration_days": "Ongoing",
      "products": [
        {
          "name": "CardioGuard",
          "dose": "2 caps/day",
          "timing": "maintenance",
          "rationale": "Vascular elasticity and endothelial support"
        },
        {
          "name": "HyperCalm",
          "dose": "2-4 caps/day",
          "timing": "ongoing Rx",
          "rationale": "AYUSH prescription"
        }
      ],
      "monitoring": "Cardiologist review every 3-6 months; NEVER stop allopathic antihypertensives without clearance."
    },
    "product_stack": {
      "core": [
        "HyperCalm",
        "CardioGuard"
      ],
      "support": [
        "MindBalance",
        "LipidClear"
      ],
      "modulator": [
        "Sleep+Stress"
      ]
    },
    "lab_monitoring": [
      "BP home monitoring daily",
      "ECG (0, 90 days)",
      "RFTs (0, 90)",
      "Serum electrolytes (90 days)",
      "Lipid panel (0, 90)",
      "Echocardiogram (annual)"
    ],
    "clinical_warnings": [
      "HyperCalm is PRESCRIPTION ONLY (Schedule E1 Sarpagandha).",
      "NEVER stop allopathic BP medications.",
      "BP monitoring 2x daily mandatory.",
      "If BP >180/110, immediate emergency cardiologist referral."
    ],
    "protocol_kit_id": "K-04",
    "protocol_kit_name": "BLOOD PRESSURE KIT",
    "kit_price_range": "Rs. 4,500 - Rs. 7,000/month"
  },
  {
    "id": "P-05",
    "name": "Cardiac Support & IHD Protocol",
    "category": "CARDIO",
    "primary_axis": "Qalb-Dam-Uroq-Azam",
    "secondary_axis": "Jigar-Meda",
    "indication": "IHD/angina (stable); Post-MI cardiac rehabilitation; High CVD risk; Dyslipidemia + cardiac risk",
    "phase1": {
      "title": "Cardiac Foundation",
      "duration_days": 45,
      "products": [
        {
          "name": "CardioGuard",
          "dose": "2 caps/day",
          "timing": "AM warm milk + PM",
          "rationale": "Arjun 480mg/day PDE + CoQ10 80mg + Shilajit + Nattokinase fibrinolytic"
        },
        {
          "name": "LipidClear",
          "dose": "2 caps/day",
          "timing": "empty stomach",
          "rationale": "LDL plaque management"
        },
        {
          "name": "HepaClear",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "Hepatic protection of lipid metabolism"
        }
      ]
    },
    "phase2": {
      "title": "Full Cardiac Protocol",
      "duration_days": 90,
      "products": [
        {
          "name": "CardioGuard",
          "dose": "4 caps/day",
          "timing": "intensive",
          "rationale": "Full myocardial and mitochondrial support"
        },
        {
          "name": "HyperCalm",
          "dose": "2 caps/day",
          "timing": "if hypertensive",
          "rationale": "Blood pressure reduction"
        },
        {
          "name": "MindBalance",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "Cardiac anxiety is common post-MI"
        },
        {
          "name": "LipidClear",
          "dose": "2 caps/day",
          "timing": "continued",
          "rationale": "Plaque stabilisation"
        }
      ],
      "monitoring": "INR monitoring if on warfarin (Nattokinase mild anticoagulant synergy)."
    },
    "phase3": {
      "title": "Lifelong Cardiac Maintenance",
      "duration_days": "Lifelong",
      "products": [
        {
          "name": "CardioGuard",
          "dose": "2 caps/day",
          "timing": "standard dose",
          "rationale": "Lifelong protective cardiotonic"
        }
      ],
      "monitoring": "Annual: ECG, ECHO, lipid panel, RFTs; Cardiologist supervision mandatory."
    },
    "product_stack": {
      "core": [
        "CardioGuard",
        "LipidClear"
      ],
      "support": [
        "HyperCalm",
        "MindBalance"
      ],
      "modulator": [
        "HepaClear"
      ]
    },
    "lab_monitoring": [
      "ECG (0, 90 days)",
      "ECHO (annual)",
      "Lipid panel (0, 45, 90)",
      "LFT (0, 90)",
      "INR if on warfarin",
      "Troponin/BNP if symptomatic"
    ],
    "clinical_warnings": [
      "CONTINUE ALL CARDIAC MEDICATIONS \u2014 never substitute.",
      "If on warfarin: INR monitoring (Nattokinase mild fibrinolytic synergy).",
      "Cardiologist supervision mandatory for IHD patients.",
      "Emergency symptoms (chest pain, dyspnoea): immediate hospital transfer."
    ],
    "protocol_kit_id": "K-05",
    "protocol_kit_name": "CARDIAC PROTECTION KIT",
    "kit_price_range": "Rs. 5,500 - Rs. 8,000/month"
  },
  {
    "id": "P-06",
    "name": "Stress & Anxiety Protocol",
    "category": "NEURO",
    "primary_axis": "Dimagh-Qalb",
    "secondary_axis": "Jigar",
    "indication": "GAD; Work stress; Burnout; HPA dysregulation; Cortisol excess; Chronic anxiety; Psychosomatic symptoms",
    "phase1": {
      "title": "HPA Axis Reset",
      "duration_days": 30,
      "products": [
        {
          "name": "MindBalance",
          "dose": "3 caps/day",
          "timing": "1 AM + 2 bedtime",
          "rationale": "Ashwagandha cortisol -27% + Zafran SSRI + L-Theanine"
        },
        {
          "name": "Sleep+Stress",
          "dose": "3 caps/day",
          "timing": "1 AM + 2 bedtime",
          "rationale": "Phosphatidylserine cortisol blunting + Mg Glycinate GABA"
        }
      ],
      "lifestyle": "Morning: avoid caffeine in first 2 hours; 10-min sunlight exposure; Evening: no screens 1 hour before bed."
    },
    "phase2": {
      "title": "Neurochemical Rebalancing",
      "duration_days": 60,
      "products": [
        {
          "name": "MindBalance",
          "dose": "3 caps/day",
          "timing": "continued",
          "rationale": "Brahmi GABA-B + Jatamansi MAO-B + Unnab GABA-A"
        },
        {
          "name": "HepaClear",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "If stress-related fatty liver signs (elevated ALT)"
        }
      ],
      "exercise": "30-min walk daily (lowers cortisol); digital detox evenings."
    },
    "phase3": {
      "title": "Long-term Resilience",
      "duration_days": "Ongoing",
      "products": [
        {
          "name": "MindBalance",
          "dose": "2 caps/day",
          "timing": "maintenance",
          "rationale": "Neuro-HPA reserve preservation"
        },
        {
          "name": "Sleep+Stress",
          "dose": "1-2 caps/day",
          "timing": "as needed",
          "rationale": "PRN sleep support"
        }
      ],
      "monitoring": "PHQ-9 + GAD-7 monthly \u2014 do not discontinue abruptly."
    },
    "product_stack": {
      "core": [
        "MindBalance",
        "Sleep+Stress"
      ],
      "support": [
        "HepaClear"
      ]
    },
    "lab_monitoring": [
      "PHQ-9 + GAD-7 monthly",
      "Cortisol AM (0, 90 days)",
      "TSH (anxiety mimics thyroid)",
      "Vitamin D3 (deficiency = anxiety)",
      "CBC (rule out anaemia)"
    ],
    "clinical_warnings": [
      "Do not replace prescribed psychiatric medications.",
      "Do not abruptly stop after 3+ months (gradual taper).",
      "If suicidal ideation present: immediate psychiatric referral.",
      "Ashwagandha: avoid in thyroid conditions on medication."
    ],
    "protocol_kit_id": "K-06",
    "protocol_kit_name": "STRESS-ANXIETY KIT",
    "kit_price_range": "Rs. 2,500 - Rs. 3,800/month"
  },
  {
    "id": "P-07",
    "name": "Insomnia & Sleep Disorder Protocol",
    "category": "NEURO",
    "primary_axis": "Dimagh-Qalb",
    "secondary_axis": "Aasab",
    "indication": "Insomnia; Sleep latency >30 min; Non-restorative sleep; Circadian disruption; Post-COVID insomnia",
    "phase1": {
      "title": "Sleep Architecture Reset",
      "duration_days": 30,
      "products": [
        {
          "name": "Sleep+Stress",
          "dose": "3 caps/day",
          "timing": "1 AM (circadian anchor) + 2 caps 30 min bedtime",
          "rationale": "Mg Glycinate + Jatamansi + Valeriana GABA restoration"
        },
        {
          "name": "MindBalance",
          "dose": "1 cap/day",
          "timing": "bedtime",
          "rationale": "If anxiety-driven insomnia"
        }
      ],
      "hygiene": "Fixed wake time (7 days including weekends); no naps; dark+cool room; eliminate caffeine after 12 PM."
    },
    "phase2": {
      "title": "Deep Sleep Restoration",
      "duration_days": 60,
      "products": [
        {
          "name": "Sleep+Stress",
          "dose": "3 caps/day",
          "timing": "continued full dose",
          "rationale": "Neurochemical sleep maintenance"
        },
        {
          "name": "MindBalance",
          "dose": "2 caps/day",
          "timing": "bedtime",
          "rationale": "Stress/anxiety overlay"
        },
        {
          "name": "HepaClear",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "If liver dysfunction contributing to sleep waking"
        }
      ]
    },
    "phase3": {
      "title": "Maintenance",
      "duration_days": "3-6 months then taper",
      "products": [
        {
          "name": "Sleep+Stress",
          "dose": "1-2 caps/day",
          "timing": "bedtime",
          "rationale": "Gradual taper \u2014 not abrupt discontinuation"
        }
      ],
      "monitoring": "PSG (polysomnography) if sleep apnoea suspected."
    },
    "product_stack": {
      "core": [
        "Sleep+Stress",
        "MindBalance"
      ],
      "support": [
        "HepaClear"
      ]
    },
    "lab_monitoring": [
      "Sleep diary (2 weeks baseline)",
      "Cortisol AM (if >20mcg/dL = HPA disruption)",
      "TSH (hypothyroid = insomnia)",
      "Ferritin (RLS component)",
      "VitD3"
    ],
    "clinical_warnings": [
      "Do not replace prescribed sleep medications immediately \u2014 gradual transition.",
      "Rule out sleep apnoea (PSG if snoring + daytime sleepiness).",
      "Jatamansi MAO-B inhibitor: caution with dopaminergic drugs."
    ],
    "protocol_kit_id": "K-07",
    "protocol_kit_name": "SLEEP RESTORE KIT",
    "kit_price_range": "Rs. 2,200 - Rs. 3,500/month"
  },
  {
    "id": "P-08",
    "name": "Asthma & Allergic Respiratory Protocol",
    "category": "RESPIRATORY",
    "primary_axis": "Riya-Sadr",
    "secondary_axis": "Tabiyat",
    "indication": "Allergic asthma; COPD; Chronic bronchitis; Seasonal allergic rhinitis; Post-viral respiratory weakness",
    "phase1": {
      "title": "Mucociliary Restoration",
      "duration_days": 30,
      "products": [
        {
          "name": "LungEase",
          "dose": "4 caps/day",
          "timing": "2 AM + 2 bedtime",
          "rationale": "NAC mucolytic + Mulethi Glycyrrhizin + Kalonji TQ 5-LOX"
        },
        {
          "name": "Immunity",
          "dose": "4 caps/day",
          "timing": "2+2",
          "rationale": "Elderberry antiviral + Beta-Glucan innate + Gilo T-cell"
        }
      ],
      "vehicle": "Warm Arq-e-Mulethi with honey; avoid known allergens; indoor air purifier."
    },
    "phase2": {
      "title": "Anti-inflammatory + Antiviral Layer",
      "duration_days": 60,
      "products": [
        {
          "name": "LungEase",
          "dose": "4 caps/day",
          "timing": "continued",
          "rationale": "Tulsi COX-2 antiviral + Banafsha expectorant + Selenium GPx lung"
        },
        {
          "name": "Immunity",
          "dose": "4 caps/day",
          "timing": "continued",
          "rationale": "Adaptive immunity reinforcement"
        },
        {
          "name": "MindBalance",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "If stress-triggered bronchospasm"
        }
      ],
      "warning": "Continue prescribed inhalers \u2014 NEVER stop bronchodilators."
    },
    "phase3": {
      "title": "Seasonal Prevention",
      "duration_days": "Ongoing monsoon + winter",
      "products": [
        {
          "name": "LungEase",
          "dose": "2-4 caps/day",
          "timing": "dose by season",
          "rationale": "Seasonal mucosal defence"
        },
        {
          "name": "Immunity",
          "dose": "2 caps/day",
          "timing": "year-round",
          "rationale": "Preventive immunity"
        }
      ],
      "monitoring": "FEV1/FVC spirometry at 3 and 6 months."
    },
    "product_stack": {
      "core": [
        "LungEase",
        "Immunity"
      ],
      "support": [
        "MindBalance"
      ]
    },
    "lab_monitoring": [
      "Spirometry FEV1/FVC (0, 90 days)",
      "IgE total (0, 90)",
      "Eosinophil count",
      "Chest X-ray if COPD"
    ],
    "clinical_warnings": [
      "NEVER stop prescribed inhalers (bronchodilators are life-saving).",
      "LungEase is ADJUNCT to inhalers \u2014 not replacement.",
      "If acute attack: use reliever inhaler; do not rely on supplements in emergencies.",
      "Mulethi long-term: monitor BP in hypertensive patients."
    ],
    "protocol_kit_id": "K-08",
    "protocol_kit_name": "RESPIRATORY CARE KIT",
    "kit_price_range": "Rs. 2,800 - Rs. 4,000/month"
  },
  {
    "id": "P-09",
    "name": "Joint Pain & Arthritis Protocol",
    "category": "JOINTS",
    "primary_axis": "Mafasil-Dam",
    "secondary_axis": "Jigar-Meda",
    "indication": "OA knee/hip; RA (adjunct); Gout (uric acid); Sports injuries; Inflammatory arthropathy",
    "phase1": {
      "title": "Inflammatory Cascade Block",
      "duration_days": 30,
      "products": [
        {
          "name": "JointFree",
          "dose": "4 caps/day",
          "timing": "with food (AM+PM)",
          "rationale": "AKBA 5-LOX + Curcumin COX-2/NF-kB + Ashwagandha NF-kB (3 pathways)"
        },
        {
          "name": "HepaClear",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "If systemic inflammation (elevated CRP, ALT)"
        },
        {
          "name": "UroClear",
          "dose": "6 caps/day",
          "timing": "in gout",
          "rationale": "Uricosuric effect + Potassium Citrate"
        }
      ],
      "physical": "RICE protocol for acute joints; warm compress for chronic."
    },
    "phase2": {
      "title": "Cartilage Protection + Repair",
      "duration_days": 60,
      "products": [
        {
          "name": "JointFree",
          "dose": "4 caps/day",
          "timing": "continued",
          "rationale": "UC-II collagen 4th mechanism + Sandal Safaid TRPV1 analgesic"
        },
        {
          "name": "Immunity",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "Systemic anti-inflammatory via Beta-Glucan + Quercetin"
        }
      ],
      "diet": "Anti-inflammatory (turmeric milk, omega-3 fish, no nightshades for RA); Physiotherapy mandatory."
    },
    "phase3": {
      "title": "Maintenance & Prevention",
      "duration_days": "Ongoing",
      "products": [
        {
          "name": "JointFree",
          "dose": "2 caps/day",
          "timing": "maintenance",
          "rationale": "Cartilage preservation and joint mobility"
        }
      ],
      "monitoring": "Annual: uric acid (gout); CRP; X-ray; Body weight management."
    },
    "product_stack": {
      "core": [
        "JointFree"
      ],
      "support": [
        "HepaClear",
        "Immunity",
        "UroClear"
      ]
    },
    "lab_monitoring": [
      "CRP + ESR (0, 45, 90)",
      "Uric acid (gout)",
      "RF + anti-CCP (RA)",
      "WOMAC score (0, 90)",
      "X-ray joint (0, 6 months)"
    ],
    "clinical_warnings": [
      "JointFree with food (Curcumin+UC-II absorption).",
      "AKBA: Boswellia most adulterated botanical \u2014 verify HPLC certificate.",
      "For RA: JointFree is adjunct to DMARDs; do not stop DMARDs."
    ],
    "protocol_kit_id": "K-09",
    "protocol_kit_name": "JOINT CARE KIT",
    "kit_price_range": "Rs. 3,000 - Rs. 4,500/month"
  },
  {
    "id": "P-10",
    "name": "Erectile Dysfunction Protocol",
    "category": "MALE",
    "primary_axis": "Khusyatain-Uroq-Aasab-Dimagh",
    "secondary_axis": "Jigar",
    "indication": "ED: vasculogenic (60-70%); psychogenic (20-30%); Mixed; Metabolic ED; Performance anxiety",
    "phase1": {
      "title": "Root Cause Assessment + Neurochemical Reset",
      "duration_days": 30,
      "products": [
        {
          "name": "VigorX-ED",
          "dose": "4 caps PRN",
          "timing": "60 min before activity",
          "rationale": "Assess vascular response"
        },
        {
          "name": "MindBalance",
          "dose": "3 caps/day",
          "timing": "daily",
          "rationale": "Psychogenic ED #1 cause India <45 yrs; Zafran SSRI + Ashwagandha HPA"
        },
        {
          "name": "TestoVital Classic",
          "dose": "4 caps/day",
          "timing": "if low T documented",
          "rationale": "Androgenic priming"
        }
      ],
      "diagnostics": "Doppler if vasculogenic suspected; Testosterone + Prolactin + PSA baseline."
    },
    "phase2": {
      "title": "Chronic Restoration Protocol",
      "duration_days": 90,
      "products": [
        {
          "name": "VigorX-ED",
          "dose": "8 caps/day",
          "timing": "4+4 chronic",
          "rationale": "Citrulline+L-Arg 1760mg/day NO + Tongkat Ali + Shilajit 480mg + Warq Tila"
        },
        {
          "name": "TestoVital Classic",
          "dose": "8 caps/day",
          "timing": "4 AM fasting + 4 PM",
          "rationale": "Triple HPG axis restoration"
        },
        {
          "name": "MindBalance",
          "dose": "3 caps/day",
          "timing": "continued",
          "rationale": "Anticipatory anxiety suppression"
        }
      ],
      "lifestyle": "No tobacco, no alcohol (both destroy endothelial NO production)."
    },
    "phase3": {
      "title": "Maintenance",
      "duration_days": "Ongoing",
      "products": [
        {
          "name": "VigorX-ED",
          "dose": "PRN",
          "timing": "as needed",
          "rationale": "On-demand vascular support"
        },
        {
          "name": "TestoVital Classic",
          "dose": "4 caps/day",
          "timing": "maintenance",
          "rationale": "HPG axis maintenance"
        }
      ],
      "monitoring": "Annual: Testosterone + PSA + lipid panel."
    },
    "product_stack": {
      "core": [
        "VigorX-ED",
        "TestoVital Classic"
      ],
      "support": [
        "MindBalance"
      ],
      "modulator": [
        "Night-One X Classic (PRN acute)"
      ]
    },
    "lab_monitoring": [
      "Testosterone (total+free)",
      "Prolactin",
      "LH+FSH",
      "PSA",
      "Fasting glucose+HOMA-IR",
      "Lipid panel",
      "Blood pressure"
    ],
    "clinical_warnings": [
      "Prescription-only (Poshida Amraz \u2014 AYUSH Rx).",
      "Rule out prostate pathology (PSA before prescribing).",
      "No alcohol + tobacco (most common iatrogenic ED cause).",
      "If on PDE5 inhibitors: inform prescriber before combining (additive vasodilation)."
    ],
    "protocol_kit_id": "K-10",
    "protocol_kit_name": "ED RESTORE KIT (Rx)",
    "kit_price_range": "Rs. 6,000 - Rs. 9,000/month"
  },
  {
    "id": "P-11",
    "name": "Male Infertility Protocol",
    "category": "MALE",
    "primary_axis": "Khusyatain-Dam",
    "secondary_axis": "Jigar-Dimagh",
    "indication": "Oligospermia (<15M/mL); Asthenospermia (<32% motility); Teratospermia; High DFI; Idiopathic male infertility",
    "phase1": {
      "title": "Antioxidant + Testicular Environment",
      "duration_days": 30,
      "products": [
        {
          "name": "FertiMax-M",
          "dose": "8 caps/day",
          "timing": "4+4",
          "rationale": "CoQ10 480mg/day Cochrane + Lycopene testicular + Selenium GPx-5 + Ashwagandha"
        },
        {
          "name": "SemenGuard",
          "dose": "4 caps/day",
          "timing": "if high DFI",
          "rationale": "Jatamansi neural axis + Post Akhrot DHA omega-3 + CoQ10"
        }
      ],
      "lifestyle": "Remove: smoking (most damaging to sperm), alcohol, hot tubs, tight clothing; Baseline WHO 6th semen analysis + DFI."
    },
    "phase2": {
      "title": "Spermatogenesis Support",
      "duration_days": 60,
      "products": [
        {
          "name": "Fertility PRO",
          "dose": "5 caps/day",
          "timing": "2+1+2",
          "rationale": "Ashwagandha +167% sperm + Kaunch anti-prolactin + CoQ10 + Zinc"
        },
        {
          "name": "FertiMax-M",
          "dose": "8 caps/day",
          "timing": "continued",
          "rationale": "Antioxidant protection"
        },
        {
          "name": "TestoVital Classic",
          "dose": "4 caps/day",
          "timing": "if testosterone deficient",
          "rationale": "Leydig steroidogenesis support"
        }
      ],
      "guideline": "Zinc-rich foods; Vit D sunlight; sleep 7-8 hours (90% testosterone secreted during sleep)."
    },
    "phase3": {
      "title": "Semen Analysis + Optimisation",
      "duration_days": "90-day checkpoint",
      "products": [
        {
          "name": "Fertility Moderate",
          "dose": "4 caps/day",
          "timing": "maintenance",
          "rationale": "Ongoing spermatogenic maintenance"
        }
      ],
      "monitoring": "Repeat WHO semen analysis at 90 days; if improvement: continue 90 more days before IUI/IVF; both partners evaluated."
    },
    "product_stack": {
      "core": [
        "Fertility PRO",
        "FertiMax-M"
      ],
      "support": [
        "SemenGuard",
        "TestoVital Classic"
      ]
    },
    "lab_monitoring": [
      "WHO 6th semen analysis (0, 45, 90)",
      "DFI \u2014 DNA fragmentation index",
      "ROS assay semen",
      "FSH+LH+T+Prolactin+Estradiol (0, 90)",
      "Testicular Doppler if varicocele suspected",
      "Karyotype if severe (<5M/mL)"
    ],
    "clinical_warnings": [
      "90 days = ONE spermatogenesis cycle minimum.",
      "Both partners must be evaluated simultaneously.",
      "Varicocele: surgical correction if grade 2-3 before supplementation.",
      "If azoospermia: specialist evaluation first."
    ],
    "protocol_kit_id": "K-11",
    "protocol_kit_name": "MALE FERTILITY KIT",
    "kit_price_range": "Rs. 7,000 - Rs. 10,000/month"
  },
  {
    "id": "P-12",
    "name": "Low Testosterone & Hypogonadism Protocol",
    "category": "MALE",
    "primary_axis": "Khusyatain-Jigar-HPG",
    "secondary_axis": "Dimagh-Kuli",
    "indication": "Total T <300 ng/dL; Free T low; LH+FSH low (secondary hypogonadism); Age-related testosterone decline",
    "phase1": {
      "title": "HPG Axis Assessment + Initiation",
      "duration_days": 30,
      "products": [
        {
          "name": "TestoVital Classic",
          "dose": "8 caps/day",
          "timing": "4 AM fasting + 4 PM",
          "rationale": "Ashwagandha HPG + Tongkat Ali SHBG + Shilajit 520mg + Warq Tila"
        },
        {
          "name": "VitD3",
          "dose": "4000 IU/day",
          "timing": "morning",
          "rationale": "Deficiency alone causes -20-30% T"
        }
      ],
      "lifestyle": "Night sleep optimisation (90% testosterone secreted during deep sleep); Baseline full panel."
    },
    "phase2": {
      "title": "Full HPG Restoration",
      "duration_days": 90,
      "products": [
        {
          "name": "TestoVital Classic",
          "dose": "8 caps/day",
          "timing": "continued",
          "rationale": "Full HPG stimulation"
        },
        {
          "name": "Fertility PRO",
          "dose": "4 caps/day",
          "timing": "daily",
          "rationale": "Kaunch L-DOPA LH pulsatile stimulation"
        },
        {
          "name": "Men Daily",
          "dose": "2 caps/day",
          "timing": "with food",
          "rationale": "Daily zinc + VitD3 + CoQ10 maintenance"
        }
      ],
      "exercise": "Resistance training: compound exercises 3x/week; remove alcohol, chronic stress, sleep deprivation."
    },
    "phase3": {
      "title": "Monitoring + Maintenance",
      "duration_days": "Ongoing",
      "products": [
        {
          "name": "TestoVital Classic",
          "dose": "4 caps/day",
          "timing": "maintenance",
          "rationale": "Endogenous testosterone maintenance"
        }
      ],
      "monitoring": "Annual: T+LH+FSH; DEXA if osteopenia suspected; NEVER use exogenous testosterone without specialist."
    },
    "product_stack": {
      "core": [
        "TestoVital Classic",
        "Men Daily"
      ],
      "support": [
        "Fertility PRO",
        "MindBalance"
      ]
    },
    "lab_monitoring": [
      "Total T + Free T (0, 90 days AM 8-10 AM)",
      "LH + FSH",
      "SHBG",
      "Prolactin",
      "VitD3",
      "Cortisol",
      "DEXA (if >45 yrs or severe)"
    ],
    "clinical_warnings": [
      "NEVER use exogenous testosterone without specialist \u2014 permanently suppresses HPG.",
      "Testosterone RCT effects appear at 90 days minimum.",
      "If Prolactin >25: refer for MRI pituitary before TestoVital."
    ],
    "protocol_kit_id": "K-12",
    "protocol_kit_name": "TESTOSTERONE RESTORE KIT",
    "kit_price_range": "Rs. 5,000 - Rs. 7,500/month"
  },
  {
    "id": "P-13",
    "name": "Prostate Health Protocol (BPH / LUTS)",
    "category": "MALE",
    "primary_axis": "Ghudda-Mithana",
    "secondary_axis": "Kulya",
    "indication": "BPH; LUTS (urinary frequency, urgency, weak stream); PSA elevation (benign); Prostatitis (chronic)",
    "phase1": {
      "title": "Baseline + Inflammation Control",
      "duration_days": 30,
      "products": [
        {
          "name": "ProstaGuard",
          "dose": "6 caps/day",
          "timing": "2+2+2",
          "rationale": "Pumpkin Seed 5-AR + AKBA 5-LOX + Lycopene + Curcumin NF-kB"
        },
        {
          "name": "UroClear",
          "dose": "4 caps/day",
          "timing": "daily",
          "rationale": "Diuretic relief + Potassium Citrate urinary pH"
        }
      ],
      "mandate": "MANDATORY: PSA test before prescribing (rule out prostate cancer); IPSS score at baseline."
    },
    "phase2": {
      "title": "Active BPH Management",
      "duration_days": 90,
      "products": [
        {
          "name": "ProstaGuard",
          "dose": "6 caps/day",
          "timing": "continued",
          "rationale": "Prostatic anti-proliferative maintenance"
        },
        {
          "name": "Men Daily",
          "dose": "2 caps/day",
          "timing": "with food",
          "rationale": "Zinc and VitD3 for prostate health"
        }
      ],
      "lifestyle": "Diet: lycopene-rich foods (tomatoes, watermelon); reduce red meat, dairy fat; Pelvic floor exercises (Kegel) daily."
    },
    "phase3": {
      "title": "Monitoring + Maintenance",
      "duration_days": "Ongoing",
      "products": [
        {
          "name": "ProstaGuard",
          "dose": "4 caps/day",
          "timing": "maintenance",
          "rationale": "Long-term IPSS control"
        }
      ],
      "monitoring": "PSA every 6 months mandatory; Uroflowmetry annually; Urologist review annually."
    },
    "product_stack": {
      "core": [
        "ProstaGuard",
        "UroClear"
      ],
      "support": [
        "Men Daily"
      ]
    },
    "lab_monitoring": [
      "PSA (MANDATORY \u2014 0 and 6 months)",
      "IPSS score (0, 90)",
      "Uroflowmetry (0, 90)",
      "Serum creatinine",
      "Urinalysis",
      "Prostate-specific ultrasound"
    ],
    "clinical_warnings": [
      "PSA MONITORING MANDATORY \u2014 rule out prostate cancer before any prescribing.",
      "If PSA >4: urology referral mandatory.",
      "Urologist supervision required."
    ],
    "protocol_kit_id": "K-13",
    "protocol_kit_name": "PROSTATE HEALTH KIT",
    "kit_price_range": "Rs. 3,500 - Rs. 5,000/month"
  },
  {
    "id": "P-14",
    "name": "PCOS Protocol",
    "category": "FEMALE",
    "primary_axis": "Mabaysim-Jigar-Insulin",
    "secondary_axis": "Dimagh-Kuli",
    "indication": "PCOS (Rotterdam criteria); Insulin-resistant PCOS; Lean PCOS; PCOS-related infertility",
    "phase1": {
      "title": "Insulin Resistance Root Correction",
      "duration_days": 30,
      "products": [
        {
          "name": "HepaClear",
          "dose": "4 caps/day",
          "timing": "AM empty + PM",
          "rationale": "Gut-liver-insulin axis reset; 80% PCOS = insulin resistance root"
        },
        {
          "name": "CycloCare-PCOS",
          "dose": "10 caps/day",
          "timing": "5+5",
          "rationale": "Myo+DCI Inositol 40:1 + Gurmar insulin + Dalchini MHCP"
        }
      ],
      "diet": "Low GI (<55 GI foods); Mediterranean; 16:8 fasting optional; Exercise: HIIT 3x/week."
    },
    "phase2": {
      "title": "Hormonal Axis Correction",
      "duration_days": 90,
      "products": [
        {
          "name": "CycloCare-PCOS",
          "dose": "10 caps/day",
          "timing": "continued",
          "rationale": "Gokshura LH surge (67-78% ovulation RCT) + Shatavari FSH/LH + Zafran anti-androgenic"
        },
        {
          "name": "MindBalance",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "HPA-adrenal androgen excess"
        },
        {
          "name": "FertiliWomen",
          "dose": "8 caps/day",
          "timing": "if fertility goal",
          "rationale": "CoQ10 480mg/day oocyte + 5-MTHF"
        }
      ],
      "contraindication": "CONTRAINDICATED IN PREGNANCY: Zafran emmenagogue."
    },
    "phase3": {
      "title": "Cycle Regularisation Maintenance",
      "duration_days": "3-6 months",
      "products": [
        {
          "name": "CycloCare-PCOS",
          "dose": "4-6 caps/day",
          "timing": "maintenance",
          "rationale": "Cycle maintenance"
        },
        {
          "name": "Women Daily",
          "dose": "2 caps/day",
          "timing": "with food",
          "rationale": "Micronutrient maintenance"
        }
      ],
      "monitoring": "Menstrual cycle diary tracking; LH+FSH+AMH+Testosterone+HOMA-IR 3-monthly; Repeat pelvic USG at 6 months."
    },
    "product_stack": {
      "core": [
        "CycloCare-PCOS",
        "HepaClear"
      ],
      "support": [
        "MindBalance",
        "FertiliWomen"
      ],
      "modulator": [
        "Women Daily"
      ]
    },
    "lab_monitoring": [
      "LH+FSH ratio (LH>2:1 FSH = PCOS marker)",
      "AMH (ovarian reserve)",
      "Total T+SHBG+FAI",
      "HOMA-IR+fasting insulin",
      "TSH (thyroid comorbid)",
      "Pelvic USG (0, 6 months)"
    ],
    "clinical_warnings": [
      "CONTRAINDICATED IN PREGNANCY \u2014 Zafran emmenagogue; confirm negative pregnancy test before prescribing.",
      "PCOS + insulin resistance: lifestyle intervention equally important as supplements.",
      "If fertility goal: gynaecologist co-management mandatory."
    ],
    "protocol_kit_id": "K-14",
    "protocol_kit_name": "PCOS KIT",
    "kit_price_range": "Rs. 4,500 - Rs. 6,500/month"
  },
  {
    "id": "P-15",
    "name": "Leucorrhoea Protocol",
    "category": "FEMALE",
    "primary_axis": "Reham-Jigar",
    "secondary_axis": "Tabiyat",
    "indication": "Leucorrhoea (Sayalan-ul-Reham); BV; vaginal Candidiasis; Recurrent vaginal infections; Trichomonas (adjunct)",
    "phase1": {
      "title": "Antimicrobial + Astringent",
      "duration_days": 30,
      "products": [
        {
          "name": "LeucoClear",
          "dose": "8 caps/day",
          "timing": "2+2+2+2",
          "rationale": "L. acidophilus 3B CFU + Mochras tannin astringent + Gulnaar Punicalagin anti-Candida"
        },
        {
          "name": "FemCare-L",
          "dose": "4 caps/day",
          "timing": "2+2",
          "rationale": "Neem Nimbin antibacterial + Shatavari uterine tonic + Iron Bisglycinate"
        }
      ],
      "hygiene": "Maintain vaginal hygiene: pH-balanced wash only; no douching; Continue prescribed antifungal/antibacterial if active infection."
    },
    "phase2": {
      "title": "Microbiome Restoration",
      "duration_days": 60,
      "products": [
        {
          "name": "LeucoClear",
          "dose": "8 caps/day",
          "timing": "continued",
          "rationale": "L. acidophilus establishes vaginal Lactobacillus dominance"
        },
        {
          "name": "Women Daily",
          "dose": "2 caps/day",
          "timing": "with food",
          "rationale": "Nutritional support; iron+B12+VitD3"
        }
      ],
      "monitoring": "pH test strips: aim for vaginal pH <4.5; anaemia correction."
    },
    "phase3": {
      "title": "Prevention",
      "duration_days": "3-6 months",
      "products": [
        {
          "name": "LeucoClear",
          "dose": "4 caps/day",
          "timing": "maintenance",
          "rationale": "Flora preservation"
        },
        {
          "name": "Women Daily",
          "dose": "2 caps/day",
          "timing": "ongoing",
          "rationale": "Nutritional foundation"
        }
      ],
      "monitoring": "HVS culture at 3 months to confirm microbiome normalisation."
    },
    "product_stack": {
      "core": [
        "LeucoClear",
        "FemCare-L"
      ],
      "support": [
        "Women Daily"
      ],
      "modulator": [
        "HepaClear"
      ]
    },
    "lab_monitoring": [
      "HVS culture+sensitivity (0, 90)",
      "Vaginal pH (weekly self-monitoring)",
      "Haemoglobin+ferritin",
      "Blood glucose (diabetes increases infection risk)"
    ],
    "clinical_warnings": [
      "Active Candida or BV: complete prescribed course first; LeucoClear is adjunct.",
      "Refrigerated storage mandatory for probiotic viability."
    ],
    "protocol_kit_id": "K-15",
    "protocol_kit_name": "LEUCORRHOEA KIT",
    "kit_price_range": "Rs. 3,500 - Rs. 5,000/month"
  },
  {
    "id": "P-16",
    "name": "Menstrual Health Protocol (Dysmenorrhoea / Menorrhagia)",
    "category": "FEMALE",
    "primary_axis": "Reham-Dam",
    "secondary_axis": "Dimagh-Kuli",
    "indication": "Primary dysmenorrhoea; Menorrhagia; Irregular cycles; Luteal phase defect; PMS/PMDD",
    "phase1": {
      "title": "Hormonal Balance",
      "duration_days": 30,
      "products": [
        {
          "name": "UterTone",
          "dose": "6 caps/day",
          "timing": "2+2+2",
          "rationale": "Vitex Chasteberry prolactin reduction (6 RCTs PMS)"
        },
        {
          "name": "FemCare-L",
          "dose": "4 caps/day",
          "timing": "2+2",
          "rationale": "Shatavari uterine tonic + Iron Bisglycinate (menorrhagia anaemia)"
        }
      ],
      "regimen": "Day 1-5 (menstrual): hot water bottle, ginger tea, light movement; Day 15-28 (luteal): Vitex acts on prolactin reduction in this phase."
    },
    "phase2": {
      "title": "Cycle Regularisation",
      "duration_days": 60,
      "products": [
        {
          "name": "UterTone",
          "dose": "6 caps/day",
          "timing": "continued + 5-MTHF",
          "rationale": "Methylation for endometrial repair"
        },
        {
          "name": "MindBalance",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "HPA-adrenal driven cycle disruption; PMDD component"
        },
        {
          "name": "HepaClear",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "Hepatic oestrogen metabolism (impaired liver = oestrogen dominance)"
        }
      ],
      "diet": "Omega-3 foods: salmon, flaxseed (PGE2 reduction = less dysmenorrhoea)."
    },
    "phase3": {
      "title": "Maintenance",
      "duration_days": "3-6 months",
      "products": [
        {
          "name": "UterTone",
          "dose": "2-4 caps/day",
          "timing": "maintenance",
          "rationale": "Luteal phase support"
        },
        {
          "name": "Women Daily",
          "dose": "2 caps/day",
          "timing": "ongoing",
          "rationale": "Nutritional support"
        }
      ],
      "monitoring": "Serum progesterone day 21 monitoring; if endometriosis suspected: gynaecologist ultrasound."
    },
    "product_stack": {
      "core": [
        "UterTone",
        "FemCare-L"
      ],
      "support": [
        "MindBalance",
        "HepaClear"
      ],
      "modulator": [
        "Women Daily"
      ]
    },
    "lab_monitoring": [
      "Serum progesterone (day 21)",
      "Prolactin",
      "FSH+LH (day 2-3)",
      "Haemoglobin+ferritin",
      "TSH",
      "Pelvic USG (endometriosis, fibroid)"
    ],
    "clinical_warnings": [
      "PHYSICIAN MONITORING MANDATORY for UterTone.",
      "Not for use in pregnancy (Zafran emmenagogue in UterTone).",
      "If menorrhagia >80mL/cycle: gynaecologist mandatory.",
      "Vitex: may interact with dopamine antagonists; inform prescriber."
    ],
    "protocol_kit_id": "K-16",
    "protocol_kit_name": "CYCLE CARE KIT",
    "kit_price_range": "Rs. 3,200 - Rs. 4,800/month"
  },
  {
    "id": "P-17",
    "name": "Menopause Management Protocol",
    "category": "FEMALE",
    "primary_axis": "Mabaysim-Qalb-Azam",
    "secondary_axis": "Dimagh-Aasab",
    "indication": "Perimenopause; Natural menopause; Surgical menopause; Hot flushes; Post-menopausal bone loss",
    "phase1": {
      "title": "Vasomotor Symptom Control",
      "duration_days": 45,
      "products": [
        {
          "name": "MenoPease",
          "dose": "10 caps/day",
          "timing": "5+5 with food",
          "rationale": "Cimicifuga 150mg/day 5-HT7 (Cochrane hot flush RCTs) + Pueraria Miroestrol ER-beta"
        },
        {
          "name": "Women Daily",
          "dose": "2 caps/day",
          "timing": "with food",
          "rationale": "Calcium + VitD3 + iron + B12 foundational"
        },
        {
          "name": "MindBalance",
          "dose": "2 caps/day",
          "timing": "bedtime",
          "rationale": "Menopausal mood disruption; Ashwagandha HPA"
        }
      ]
    },
    "phase2": {
      "title": "Bone + Cardiovascular Protection",
      "duration_days": 90,
      "products": [
        {
          "name": "MenoPease",
          "dose": "10 caps/day",
          "timing": "continued",
          "rationale": "Coral Calcium + VitD3 + Shallaki AKBA anti-osteoclast bone stack"
        },
        {
          "name": "CardioGuard",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "Post-menopausal CVD risk doubles; CoQ10+Shilajit+Arjun cardiac"
        },
        {
          "name": "LipidClear",
          "dose": "2 caps/day",
          "timing": "if lipid abnormality",
          "rationale": "Post-menopausal LDL rise is common"
        }
      ],
      "exercise": "Weight-bearing exercise: walking + strength 4x/week (bone density)."
    },
    "phase3": {
      "title": "Lifelong Maintenance",
      "duration_days": "Lifelong",
      "products": [
        {
          "name": "MenoPease",
          "dose": "4-6 caps/day",
          "timing": "maintenance",
          "rationale": "Endocrine balance"
        },
        {
          "name": "Women Daily",
          "dose": "2 caps/day",
          "timing": "ongoing",
          "rationale": "Bone mineral support"
        }
      ],
      "monitoring": "DEXA bone density at 1 year and every 2 years; Continue HRT if prescribed \u2014 MenoPease is adjunct."
    },
    "product_stack": {
      "core": [
        "MenoPease",
        "Women Daily"
      ],
      "support": [
        "CardioGuard",
        "MindBalance",
        "LipidClear"
      ]
    },
    "lab_monitoring": [
      "FSH+LH+E2 (menopausal status)",
      "DEXA (0, 12 months)",
      "Lipid panel (0, 6 months)",
      "Blood pressure",
      "TSH",
      "Calcium+VitD3"
    ],
    "clinical_warnings": [
      "MenoPease is ADJUNCT to HRT \u2014 never substitute without gynaecologist.",
      "Pueraria mirifica: potent phytoestrogen \u2014 gynaecologist supervision.",
      "Cimicifuga: 150mg/day (FSSAI compliant dose)."
    ],
    "protocol_kit_id": "K-17",
    "protocol_kit_name": "MENOPAUSE KIT",
    "kit_price_range": "Rs. 4,500 - Rs. 7,000/month"
  },
  {
    "id": "P-18",
    "name": "Female Fertility Protocol",
    "category": "FEMALE",
    "primary_axis": "Mabaysim-Reham-Hormoni",
    "secondary_axis": "Jigar-Meda",
    "indication": "Unexplained infertility; PCOS-infertility; Poor oocyte quality; Recurrent implantation failure; IVF support",
    "phase1": {
      "title": "Hormonal Baseline + Oocyte Quality",
      "duration_days": 30,
      "products": [
        {
          "name": "FertiliWomen",
          "dose": "8 caps/day",
          "timing": "4+4",
          "rationale": "CoQ10 480mg/day oocyte mitochondrial + Gokshura LH surge + 5-MTHF"
        },
        {
          "name": "CycloCare-PCOS",
          "dose": "10 caps/day",
          "timing": "if PCOS infertility",
          "rationale": "Myo+DCI 40:1 + Gokshura + Gurmar insulin"
        },
        {
          "name": "HepaClear",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "Hepatic oestrogen metabolism"
        }
      ],
      "diagnostics": "Baseline: AMH, AFC, FSH, LH, E2, prolactin, TSH, HOMA-IR; at least 2 cycles before conception attempt."
    },
    "phase2": {
      "title": "Cycle Support + Endometrial Preparation",
      "duration_days": 90,
      "products": [
        {
          "name": "FertiliWomen",
          "dose": "8 caps/day",
          "timing": "continued",
          "rationale": "Shatavari endometrial thickening + Zafran uterine blood flow"
        },
        {
          "name": "UterTone",
          "dose": "4 caps/day",
          "timing": "luteal phase",
          "rationale": "Vitex progesterone support + 5-MTHF endometrial DNA"
        },
        {
          "name": "MindBalance",
          "dose": "2 caps/day",
          "timing": "bedtime",
          "rationale": "Fertility anxiety (cortisol impairs FSH sensitivity)"
        }
      ],
      "mandate": "Both partners evaluated simultaneously."
    },
    "phase3": {
      "title": "IVF/IUI Support (if ART)",
      "duration_days": "During stimulation",
      "products": [
        {
          "name": "FertiliWomen",
          "dose": "8 caps/day",
          "timing": "through stimulation phase",
          "rationale": "CoQ10 oocyte protection"
        }
      ],
      "critical_rule": "Stop Zafran-containing products on confirmed pregnancy; continue 5-MTHF + CoQ10 + Shatavari through first trimester (gynaecologist approval)."
    },
    "product_stack": {
      "core": [
        "FertiliWomen",
        "CycloCare-PCOS"
      ],
      "support": [
        "UterTone",
        "MindBalance",
        "HepaClear"
      ],
      "modulator": [
        "Women Daily"
      ]
    },
    "lab_monitoring": [
      "AMH+AFC (ovarian reserve)",
      "FSH+LH+E2 (day 2-3)",
      "Progesterone (day 21)",
      "Prolactin+TSH+Insulin",
      "Both partner: semen analysis",
      "Pelvic USG (antral follicle count)"
    ],
    "clinical_warnings": [
      "GYNAECOLOGIST MONITORING MANDATORY.",
      "Stop Zafran products on confirmed pregnancy.",
      "Both partners must be evaluated \u2014 50% infertility is male factor.",
      "IVF: inform reproductive endocrinologist of all supplements before stimulation."
    ],
    "protocol_kit_id": "K-18",
    "protocol_kit_name": "FEMALE FERTILITY KIT",
    "kit_price_range": "Rs. 6,000 - Rs. 9,000/month"
  },
  {
    "id": "P-19",
    "name": "Immunity & Infection Prevention Protocol",
    "category": "GENERAL",
    "primary_axis": "Tabiyat",
    "secondary_axis": "Riya-Sadr",
    "indication": "Recurrent infections; Seasonal flu; Post-viral fatigue; Immunodeficiency; COVID-19 prevention",
    "phase1": {
      "title": "Innate Immunity Priming",
      "duration_days": 30,
      "products": [
        {
          "name": "Immunity",
          "dose": "4 caps/day",
          "timing": "2+2",
          "rationale": "Elderberry neuraminidase + Beta-Glucan Dectin-1 macrophage + Gilo T-cell + Kalonji TQ"
        },
        {
          "name": "LungEase",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "Respiratory mucociliary barrier (first line of defence)"
        }
      ],
      "check": "Vitamin D3 check (VD3 deficiency = #1 immune vulnerability in India)."
    },
    "phase2": {
      "title": "Adaptive Immunity + Antiviral",
      "duration_days": 60,
      "products": [
        {
          "name": "Immunity",
          "dose": "4 caps/day",
          "timing": "continued full dose",
          "rationale": "Tulsi COX-2 antiviral + Zinc ionophore + Ashwagandha T-cell modulation"
        },
        {
          "name": "LungEase",
          "dose": "2 caps/day",
          "timing": "continued",
          "rationale": "NAC mucolytic + Selenium GPx lung"
        },
        {
          "name": "HepaClear",
          "dose": "2 caps/day",
          "timing": "if liver impaired",
          "rationale": "Immune-liver connection"
        }
      ],
      "lifestyle": "Sleep 7-8 hours (NK cell activity declines 70% with sleep deprivation)."
    },
    "phase3": {
      "title": "Seasonal Maintenance",
      "duration_days": "Year-round / seasonal peaks",
      "products": [
        {
          "name": "Immunity",
          "dose": "2 caps/day",
          "timing": "maintenance; 4 in flu season",
          "rationale": "Ongoing immune surveillance"
        }
      ],
      "monitoring": "Annual CBC; continue vaccinations."
    },
    "product_stack": {
      "core": [
        "Immunity",
        "LungEase"
      ],
      "support": [
        "HepaClear"
      ]
    },
    "lab_monitoring": [
      "CBC with differential (0, 90)",
      "IgE total (allergy component)",
      "VitD3 (baseline)",
      "TSH (thyroid immune link)"
    ],
    "clinical_warnings": [
      "Not a vaccine substitute.",
      "Continue prescribed immunosuppressants if applicable.",
      "Active infection: continue antibiotics; Immunity is adjunct prevention."
    ],
    "protocol_kit_id": "K-19",
    "protocol_kit_name": "IMMUNITY SHIELD KIT",
    "kit_price_range": "Rs. 2,500 - Rs. 3,500/month"
  },
  {
    "id": "P-20",
    "name": "IBS & Gut Health Protocol",
    "category": "GENERAL",
    "primary_axis": "Meda-Amaa",
    "secondary_axis": "Jigar",
    "indication": "IBS (all subtypes); Chronic constipation; Dysbiosis; Leaky gut; Post-antibiotic gut damage; SIBO",
    "phase1": {
      "title": "Gut Barrier Repair",
      "duration_days": 30,
      "products": [
        {
          "name": "GutEase-IBS",
          "dose": "6 caps/day",
          "timing": "2+2+2 pre-meal",
          "rationale": "L-Glutamine tight junctions + Peppermint beads enteric smooth muscle + Synbiotic 5B CFU"
        },
        {
          "name": "HepaClear",
          "dose": "4 caps/day",
          "timing": "AM empty + PM",
          "rationale": "Gut-liver axis restoration; Kaasni inulin prebiotic"
        }
      ],
      "mandate": "Isabgol with 250ml water (MANDATORY each dose); Remove FODMAPs, refined sugar, alcohol (IBS triggers)."
    },
    "phase2": {
      "title": "Microbiome Diversification",
      "duration_days": 60,
      "products": [
        {
          "name": "GutEase-IBS",
          "dose": "6 caps/day",
          "timing": "continued",
          "rationale": "Kaasni inulin feeds Bifidobacterium; Probiotic 5B CFU re-colonises"
        },
        {
          "name": "MindBalance",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "Gut-brain axis (IBS has 50% psychiatric comorbidity)"
        }
      ],
      "diet": "Fermented foods: yoghurt, kefir, fermented vegetables; identify personal trigger foods (food diary)."
    },
    "phase3": {
      "title": "Maintenance + Prevention",
      "duration_days": "Ongoing",
      "products": [
        {
          "name": "GutEase-IBS",
          "dose": "3 caps/day",
          "timing": "maintenance",
          "rationale": "Gut mucosal stability"
        }
      ],
      "monitoring": "Bristol stool scale monthly self-monitoring; IBS-SSS score at 3 and 6 months."
    },
    "product_stack": {
      "core": [
        "GutEase-IBS",
        "HepaClear"
      ],
      "support": [
        "MindBalance"
      ]
    },
    "lab_monitoring": [
      "Colonoscopy (rule out IBD \u2014 mandatory before supplement prescribing)",
      "IBS-SSS score (0, 90)",
      "Stool culture (rule out SIBO)",
      "Lactulose/mannitol ratio (leaky gut)"
    ],
    "clinical_warnings": [
      "Rule out IBD (Crohns, UC) before prescribing \u2014 colonoscopy mandatory.",
      "GutEase is NOT for IBD management.",
      "250ml water per dose with Isabgol \u2014 obstruction risk without water.",
      "Peppermint: enteric-coated beads only; do NOT open capsule."
    ],
    "protocol_kit_id": "K-20",
    "protocol_kit_name": "GUT RESTORE KIT",
    "kit_price_range": "Rs. 3,000 - Rs. 4,500/month"
  },
  {
    "id": "P-21",
    "name": "Hair Loss Protocol",
    "category": "GENERAL",
    "primary_axis": "Shaar-Jigar-Dimagh",
    "secondary_axis": "Mabaysim",
    "indication": "Androgenic alopecia (male+female); Telogen effluvium; Stress-related hair loss; PCOS-related hair loss",
    "phase1": {
      "title": "Root Cause Investigation + Foundation",
      "duration_days": 30,
      "products": [
        {
          "name": "HairRoot-X",
          "dose": "4 caps/day",
          "timing": "2+2 with food",
          "rationale": "Bhringraj Wedelolactone 2% Wnt pathway + Pumpkin Seed 5-AR + Zinc DHT block"
        },
        {
          "name": "MindBalance",
          "dose": "2 caps/day",
          "timing": "daily",
          "rationale": "Telogen effluvium is often stress-triggered cortisol elevation"
        }
      ],
      "diagnostics": "Rule out: hypothyroid (TSH), iron deficiency (ferritin <50), VitD3 deficiency; Baseline trichoscopy."
    },
    "phase2": {
      "title": "DHT Block + Follicle Activation",
      "duration_days": 90,
      "products": [
        {
          "name": "HairRoot-X",
          "dose": "4 caps/day",
          "timing": "continued",
          "rationale": "Biotin 5mg + Selenium follicle GPx + Bhringraj Wnt stem cell activation"
        },
        {
          "name": "Women Daily / Men Daily",
          "dose": "2 caps/day",
          "timing": "with food",
          "rationale": "Daily micronutrient base"
        },
        {
          "name": "HepaClear",
          "dose": "2 caps/day",
          "timing": "if elevated ALT",
          "rationale": "NAFLD drives androgen excess in female AGA"
        },
        {
          "name": "CycloCare-PCOS",
          "dose": "10 caps/day",
          "timing": "if PCOS-related AGA",
          "rationale": "Insulin-androgen axis correction in females"
        }
      ]
    },
    "phase3": {
      "title": "Long-term Maintenance",
      "duration_days": "6-12 months",
      "products": [
        {
          "name": "HairRoot-X",
          "dose": "2 caps/day",
          "timing": "maintenance",
          "rationale": "Follicle density preservation"
        }
      ],
      "routine": "Trichoscopy at 3 and 6 months; Scalp massage daily (5 min) \u2014 VEGF stimulation proven in RCT."
    },
    "product_stack": {
      "core": [
        "HairRoot-X"
      ],
      "support": [
        "MindBalance",
        "HepaClear"
      ],
      "modulator": [
        "CycloCare-PCOS (female PCOS-AGA)",
        "Women Daily / Men Daily"
      ]
    },
    "lab_monitoring": [
      "TSH (hypothyroid AGA)",
      "Ferritin+serum iron (iron-deficiency AGA)",
      "VitD3",
      "DHEAS+T+SHBG (androgenic)",
      "Trichoscopy (0, 3, 6 months)"
    ],
    "clinical_warnings": [
      "Minimum 6 months for meaningful hair cycle response.",
      "Rule out alopecia areata (autoimmune) and tinea capitis (fungal) before prescribing.",
      "Bhringraj: Wedelolactone >2% mandatory \u2014 unstandardised has zero efficacy."
    ],
    "protocol_kit_id": "K-21",
    "protocol_kit_name": "HAIR RESTORE KIT",
    "kit_price_range": "Rs. 2,800 - Rs. 4,000/month"
  }
];

export function getProtocolById(id: string): MasterProtocol | undefined {
  return MASTER_PROTOCOLS.find((p) => p.id.toUpperCase() === id.toUpperCase());
}

export function getProtocolsByCategory(category: string): MasterProtocol[] {
  if (category === "ALL") return MASTER_PROTOCOLS;
  return MASTER_PROTOCOLS.filter((p) => p.category.toUpperCase() === category.toUpperCase());
}