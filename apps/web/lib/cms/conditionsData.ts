/**
 * ZAYVORA Health™ — Canonical Conditions & Care Pathways Data Model
 *
 * Implements 10 core healthcare areas with standardized clinical layout:
 * - Overview & Pathology
 * - Common Symptoms & Signs
 * - Contributing Factors (Humoral & Biomedical Etiology)
 * - Red Flags & Urgent Care Triage (Emergency Call 112)
 * - ZAYVORA Clinical Assessment (Mizaj, Nabz, Biomarkers)
 * - Treatment Approach (4-Stage Afaal, Ghiza, Tadbeer, Dawa)
 * - Follow-up Schedule & Monitoring
 * - Evidence Base & Limitations
 * - FAQs & Scientific Citations
 */

export interface ConditionDetail {
  slug: string;
  title: string;
  unaniTerm: string;
  subtitle: string;
  category: string;
  duration: string;
  overview: string;
  symptoms: string[];
  contributingFactors: string[];
  redFlags: string[];
  assessment: {
    mizajEvaluation: string;
    physicalExamination: string;
    laboratoryInvestigations: string[];
  };
  treatmentApproach: {
    stage1: { name: string; description: string };
    stage2: { name: string; description: string };
    stage3: { name: string; description: string };
    stage4: { name: string; description: string };
    dietaryDirectives: string[];
    regimenalTherapies: string[];
  };
  followUp: {
    schedule: string;
    biomarkersTracked: string[];
  };
  evidenceAndLimitations: {
    summary: string;
    limitations: string;
    citations: string[];
  };
  faqs: { question: string; answer: string }[];
}

export const CONDITIONS_DATA: Record<string, ConditionDetail> = {
  "cardiometabolic": {
    slug: "cardiometabolic",
    title: "Cardiometabolic Health",
    unaniTerm: "Su-e-Mizaj Damawi wa Qalb",
    subtitle: "Integrative management of metabolic syndrome, lipid dysregulation, and vascular endothelium support.",
    category: "Cardiovascular & Metabolic",
    duration: "12 to 24 Weeks",
    overview: "Cardiometabolic health addresses the triad of central adiposity, dyslipidemia, and endothelial stiffness. In the Unani framework, this is conceptualized as an accumulation of thick, sluggish humors (Ghaleez Akhlat) impairing tissue perfusion and overburdening the cardiovascular axis (Qalb wa Urooq).",
    symptoms: [
      "Persistent post-prandial heaviness and fatigue",
      "Elevated waist-to-hip circumference ratio",
      "Borderline elevated systolic or diastolic arterial pressure",
      "Exertional shortness of breath without acute distress",
      "Dyslipidemic lipid panels (elevated triglycerides, low HDL)"
    ],
    contributingFactors: [
      "Circadian disruption and late-night heavy meals (Takhleel-e-Harkat)",
      "Hepatic metabolic sluggishness (Buroodat-e-Kabid)",
      "Sedentary lifestyle leading to reduced innate heat (Istirkha-e-Hararat Ghareezia)",
      "Chronic sympathetic stress elevating cortisol and vascular resistance"
    ],
    redFlags: [
      "Acute crushing chest pressure radiating to left arm, jaw, or back — Call 112 immediately",
      "Sudden shortness of breath accompanied by cold diaphoresis",
      "Acute unilateral neurological weakness or facial drooping",
      "Severe resting systolic blood pressure exceeding 180 mmHg"
    ],
    assessment: {
      mizajEvaluation: "Evaluation of baseline temperament (Mizaj-e-Asli) and identification of Damawi (sanguineous) or Balghami (phlegmatic) acquired dyscrasia.",
      physicalExamination: "10-Ajnas pulse assessment (Nabz) evaluating arterial vessel elasticity, fullness, and wave velocity; body composition analysis.",
      laboratoryInvestigations: [
        "Fasting Lipid Profile (Total Cholesterol, LDL-C, HDL-C, Triglycerides, ApoB)",
        "Fasting Blood Glucose and HbA1c",
        "High-Sensitivity C-Reactive Protein (hs-CRP)",
        "Serum Homocysteine and Liver Function Tests (SGOT, SGPT)"
      ]
    },
    treatmentApproach: {
      stage1: {
        name: "Tanqiya (Humoral Clearance)",
        description: "Mild hepatic de-obstruent and circulatory decoctions to decongest microvasculature."
      },
      stage2: {
        name: "Tahleel (Metabolic Dispersion)",
        description: "Standardized herbal formulations (e.g. Allium sativum, Commiphora mukul) targeting serum lipid clearance."
      },
      stage3: {
        name: "Taqwiyat (Cardiac & Vascular Tonification)",
        description: "Cardiotonic compound preparations (Khamira Marwareed, Arq-e-Gulab) supporting endothelial elasticity."
      },
      stage4: {
        name: "Hifz-e-Sehat (Longitudinal Preservation)",
        description: "Permanent circadian routine, aerobic exercise pacing, and Mediterranean-Unani dietary maintenance."
      },
      dietaryDirectives: [
        "Strict reduction of refined hydrogenated oils and high-fructose confections",
        "Incorporation of bitter gourds, pomegranate juice, garlic cloves, and unrefined olive oil",
        "Adherence to a 12-hour overnight digestive rest window"
      ],
      regimenalTherapies: [
        "Riyazat (Prescribed moderate aerobic exercise 30 minutes daily)",
        "Dalk (Therapeutic circulatory massage with specialized herbal oils)",
        "Hammam (Controlled thermal therapy to enhance peripheral perspiration)"
      ]
    },
    followUp: {
      schedule: "Bi-weekly clinical reviews for the first 6 weeks, transitioning to monthly evaluations thereafter.",
      biomarkersTracked: ["Fasting Lipid Panel at Week 8 and Week 16", "Serial Blood Pressure Logs", "Waist Circumference", "HOMA-IR Insulin Resistance Score"]
    },
    evidenceAndLimitations: {
      summary: "Clinical trials on standardized Commiphora mukul and Allium sativum formulations have demonstrated statistically significant reductions in serum triglycerides and LDL oxidation markers when paired with lifestyle modifications.",
      limitations: "Unani botanical therapeutics are supportive and integrative. Patients on prescription statins or antihypertensives must continue their medication under primary cardiology supervision.",
      citations: [
        "Urizar NL, et al. A natural product that lowers cholesterol as an antagonist ligand for FXR. Science. 2002;296(5573):1703-1706.",
        "Ried K, et al. Effect of garlic on blood pressure: a systematic review and meta-analysis. BMC Cardiovasc Disord. 2008;8:13."
      ]
    },
    faqs: [
      {
        question: "Can ZAYVORA replace my prescription blood pressure or cholesterol medication?",
        answer: "No. ZAYVORA care plans work collaboratively with conventional care. Medication titration is strictly performed by your treating physician based on objective laboratory outcomes."
      },
      {
        question: "How long before metabolic improvements are reflected in blood tests?",
        answer: "Initial glycemic and lipid profile shifts typically register between 6 to 12 weeks of consistent dietary adherence and botanical regimen."
      }
    ]
  },

  "gastrointestinal": {
    slug: "gastrointestinal",
    title: "Gastrointestinal & Gut-Brain Axis",
    unaniTerm: "Zoaf-e-Meda wa Su-e-Hazm",
    subtitle: "Evidence-informed protocols for functional dyspepsia, bloating, chronic constipation, and irritable bowel manifestations.",
    category: "Gastroenterology",
    duration: "6 to 16 Weeks",
    overview: "Gastrointestinal disorders often stem from impaired gastric innate heat (Buroodat-e-Meda), abnormal digestive secretions, and gut-brain dysregulation. The Unani system views digestion (Hazm) as a sequential 4-stage metabolic process beginning in the stomach and concluding at cellular assimilation.",
    symptoms: [
      "Post-prandial gastric fullness, bloating, and early satiety",
      "Epigastric burning, acid reflux, or water brash",
      "Irregular bowel habits alternating between constipation and loose stools",
      "Persistent abdominal cramping relieved by defecation",
      "Coated tongue with altered taste perception"
    ],
    contributingFactors: [
      "Irregular meal timing and rapid eating (Takhleel-e-Ghiza)",
      "Cold, heavy, or ultra-processed dietary intake damping digestive enzymes",
      "Visceral hyperalgesia and psychosomatic tension (Fikr wa Tashweesh)",
      "Dysbiosis secondary to recurrent antimicrobial usage"
    ],
    redFlags: [
      "Unexplained rapid unintentional weight loss",
      "Persistent hematemesis (vomiting blood) or melena (black tarry stools) — Call 112 immediately",
      "Progressive difficulty swallowing (dysphagia) or painful swallowing",
      "Severe persistent nocturnal abdominal pain"
    ],
    assessment: {
      mizajEvaluation: "Assessment of gastric and hepatic temperament; distinguishing between warm-dry hyperchlorhydria and cold-moist hypochlorhydria.",
      physicalExamination: "Abdominal palpation for epigastric tenderness, hepatomegaly, and tympanites; detailed tongue examination (Saburrah/coating).",
      laboratoryInvestigations: [
        "Complete Blood Count (CBC) and Erythrocyte Sedimentation Rate (ESR)",
        "Stool Routine, Microscopy, and Occult Blood (FOBT)",
        "Helicobacter pylori Antigen or Breath Test",
        "Serum Tissue Transglutaminase (tTG-IgA) for Celiac screening"
      ]
    },
    treatmentApproach: {
      stage1: {
        name: "Tanqiya (Gastric Cleansing)",
        description: "Gentle elimination of fermentative mucosal residue using standardized herbal decoctions."
      },
      stage2: {
        name: "Ta'deel (Humoral Normalization)",
        description: "Restoring digestive temperamental balance with Jawarish Kamuni and carminative preparations."
      },
      stage3: {
        name: "Taqwiyat-e-Meda (Gastric Tonification)",
        description: "Strengthening gastric mucosal integrity with Emblica officinalis (Amla) and Terminalia chebula (Haritaki)."
      },
      stage4: {
        name: "Hifz-e-Sehat (Gut Barrier Maintenance)",
        description: "Establishing prebiotic dietary rhythms and stress reduction protocols."
      },
      dietaryDirectives: [
        "Warm, freshly prepared, easily digestible meals (Latafat-e-Ghiza)",
        "Strict avoidance of iced drinks, carbonate beverages, and deep-fried items",
        "Incorporation of fennel, cumin, ginger, and stewed quince"
      ],
      regimenalTherapies: [
        "Nutool (Warm herbal fomentation over the epigastrium)",
        "Takmeed (Warm dry compress to relieve abdominal spasticity)",
        "Light ambulation post-prandially; avoid recumbency within 2 hours of eating"
      ]
    },
    followUp: {
      schedule: "Weekly virtual check-in for the first 4 weeks, followed by bi-weekly assessments.",
      biomarkersTracked: ["Gastrointestinal Symptom Rating Scale (GSRS)", "Bristol Stool Chart Records", "Weekly Bloating Severity Score"]
    },
    evidenceAndLimitations: {
      summary: "Clinical evaluations of classical Greco-Arab carminative confections (Jawarish formulations) demonstrate marked acceleration of gastric emptying and reduction of post-prandial distress in functional dyspepsia cohorts.",
      limitations: "Organic pathologies including inflammatory bowel disease (Crohn's, Ulcerative Colitis) and active peptic ulcers require combined gastroenterology management.",
      citations: [
        "Rahimi R, et al. A review of the role of Unani medicines in gastrointestinal disorders. Phytother Res. 2010;24(10):1423-1430.",
        "Talley NJ, et al. Functional dyspepsia: advances in diagnosis and management. Gut. 2017;66(6):1153-1164."
      ]
    },
    faqs: [
      {
        question: "How does Unani medicine approach chronic bloating differently?",
        answer: "Unani medicine evaluates bloating as impaired enzymatic digestion (Zoaf-e-Hazm) and excessive gas formation (Riyah-e-Ghaleeza) resulting from cold gastric dyscrasia, treating the root motility rather than just providing antacids."
      },
      {
        question: "Can I take these herbal formulations alongside my prescription PPIs?",
        answer: "In many cases yes, but dosing is carefully staggered by your ZAYVORA clinician to prevent absorption interference."
      }
    ]
  },

  "endocrine": {
    slug: "endocrine",
    title: "Endocrine & Diabetes Support",
    unaniTerm: "Ziabetes Shakari wa Zoaf-e-Ghudud",
    subtitle: "Specialized clinical protocols for glycemic stabilization, insulin sensitivity, and endocrine balance.",
    category: "Endocrinology",
    duration: "12 to 24 Weeks",
    overview: "Endocrine dysregulation, particularly type 2 diabetes, involves hepatic glucose overproduction and peripheral receptor insensitivity. Classical Unani nosology identifies this as Ziabetes Shakari, originating from renal and hepatic cold-dry or cold-moist dyscrasia leading to inability of tissues to retain and utilize vital metabolic substrates.",
    symptoms: [
      "Excessive thirst (Atash-e-Mufrit) and frequent nocturnal urination",
      "Unexplained physical fatigue and mental lethargy",
      "Delayed healing of minor abrasions and skin pricks",
      "Tingling, numbness, or burning sensation in feet (peripheral neuropathy)",
      "Recurrent cutaneous fungal or bacterial infections"
    ],
    contributingFactors: [
      "Excessive intake of refined carbohydrates and sedentary behavior",
      "Hepatic fatty accumulation impairing gluconeogenesis regulation",
      "Loss of intrinsic metabolic heat and cellular vigor",
      "Long-term elevated stress hormones triggering gluconeogenic spikes"
    ],
    redFlags: [
      "Fasting blood glucose above 300 mg/dL with nausea or fruity breath odor (DKA/HHS) — Call 112 immediately",
      "Acute confusion, slurred speech, or profound shakiness (hypoglycemia below 54 mg/dL)",
      "Non-healing foot ulcers with erythema, warmth, or foul-smelling discharge",
      "Sudden blurry vision or visual field loss"
    ],
    assessment: {
      mizajEvaluation: "Detailed determination of systemic and organ-specific Mizaj, particularly renal and hepatic temperaments.",
      physicalExamination: "Peripheral sensation testing using monofilament, pedal pulse palpation, and retinal examination referral check.",
      laboratoryInvestigations: [
        "Fasting and Post-Prandial Plasma Glucose",
        "Glycated Hemoglobin (HbA1c)",
        "Fasting Insulin and C-Peptide Levels",
        "Urine Albumin-to-Creatinine Ratio (uACR) and Serum Creatinine"
      ]
    },
    treatmentApproach: {
      stage1: {
        name: "Tahzeeb-e-Ghiza (Dietary Synchronization)",
        description: "Immediate elimination of high-glycemic glycemic spikes and implementation of low-insulinemic food order."
      },
      stage2: {
        name: "Ta'deel-e-Kabid (Hepatic Modulation)",
        description: "Formulations containing Gymnema sylvestre (Gurmar), Syzygium cumini (Jamun), and Cichorium intybus (Kasni)."
      },
      stage3: {
        name: "Taqwiyat-e-A'za (End-Organ Protection)",
        description: "Renoprotective and neuroprotective compound preparations safeguarding microcirculation."
      },
      stage4: {
        name: "Istiqrar (Metabolic Homeostasis)",
        description: "Structured physical conditioning and maintenance dosing to sustain glycemic stability."
      },
      dietaryDirectives: [
        "Priority consumption of complex whole grains (barley, finger millet) over white flour and rice",
        "Daily inclusion of bitter greens (methi leaves, karela) and cinnamon water",
        "Structured meal cadence with minimum 4 hours between daytime meals"
      ],
      regimenalTherapies: [
        "Riyazat-e-Mu'tadilah (Brisk walking 40 minutes daily post-meal)",
        "Dalk-e-Qawi (Vigorous dry friction massage of extremities to stimulate peripheral circulation)",
        "Takmeed (Warm fomentation over the renal and lumbar region)"
      ]
    },
    followUp: {
      schedule: "Weekly digital glucose review with clinician consultations at Week 4, 8, 12, and 24.",
      biomarkersTracked: ["Continuous or SMBG Glucose Trends", "HbA1c at 12 and 24 Weeks", "uACR Screening", "Serum Lipid Profile"]
    },
    evidenceAndLimitations: {
      summary: "Modern pharmacological trials have substantiated the insulin-sensitizing and pancreatic beta-cell supportive properties of Gymnema sylvestre gymnemic acids and Momordica charantia polypeptides.",
      limitations: "Type 1 Diabetes Mellitus requires lifelong insulin therapy; ZAYVORA care plans do not substitute for insulin in insulin-dependent states.",
      citations: [
        "Baskaran K, et al. Antidiabetic effect of a leaf extract from Gymnema sylvestre in non-insulin-dependent diabetes mellitus patients. J Ethnopharmacol. 1990;30(3):295-305.",
        "Grover JK, et al. Medicinal plants of India with anti-diabetic potential. J Ethnopharmacol. 2002;81(1):81-100."
      ]
    },
    faqs: [
      {
        question: "Can these Unani medicines be taken alongside Metformin or Glimepiride?",
        answer: "Yes. Our clinicians routinely co-manage patients on oral antidiabetic agents, monitoring blood glucose closely to prevent hypoglycemia as sensitivity improves."
      },
      {
        question: "Is complete diabetes reversal guaranteed?",
        answer: "No ethical clinical institution guarantees disease reversal. However, significant reductions in HbA1c, improved insulin sensitivity, and reduced pharmaceutical dependency are frequently achieved."
      }
    ]
  },

  "reproductive": {
    slug: "reproductive",
    title: "Reproductive Health & Vitality",
    unaniTerm: "Amraz-e-Tanasul wa Zoaf-e-Bah",
    subtitle: "Clinician-governed holistic care for male and female reproductive resilience, vitality, and hormonal health.",
    category: "Reproductive Medicine",
    duration: "8 to 16 Weeks",
    overview: "Reproductive health in Unani medicine is intimately tied to the integrity of the three principal organs (A'za-e-Ra'eesah: brain, heart, liver) and the testicular/ovarian axes. When chronic exhaustion, stress, or humoral dyscrasia impair reproductive tissue nourishment (Mani and Dam-e-Hayz), vitality decline manifests.",
    symptoms: [
      "Loss of physical stamina, reproductive fatigue, and reduced vigor",
      "Seminal fluid thinning and suboptimal spermatogenic parameters",
      "Stress-induced performance apprehension and fatigue",
      "Neurovegetative exhaustion and low morning vitality"
    ],
    contributingFactors: [
      "Excessive nocturnal screen usage disrupting pineal-gonadal signaling",
      "Psychological stress depleting vital nervous tone (Zoaf-e-Aasab)",
      "Sedentary habits and pelvic stagnation (Ihtebas)",
      "Nutritional insufficiencies lacking adequate zinc, selenium, and essential lipids"
    ],
    redFlags: [
      "Sudden severe testicular pain with swelling (suspected torsion) — Call 112 immediately",
      "Painless testicular lump or firm induration requiring urgent oncologic workup",
      "Gross hematuria (blood in urine) or purulent urethral discharge",
      "Persistent priapism lasting longer than 4 hours"
    ],
    assessment: {
      mizajEvaluation: "Evaluation of Hararat-e-Ghareezia (innate metabolic heat) and determination of dry-cold or hot-dry genital organ dyscrasia.",
      physicalExamination: "Focused systemic exam assessing secondary sexual characteristics, peripheral reflexes, and thyroid palpation.",
      laboratoryInvestigations: [
        "Total and Free Serum Testosterone, SHBG, and LH/FSH",
        "Semen Analysis (WHO 6th Edition criteria for concentration, motility, morphology)",
        "Serum Prolactin and Thyroid Stimulating Hormone (TSH)",
        "Fasting Cortisol and DHEA-S"
      ]
    },
    treatmentApproach: {
      stage1: {
        name: "Tahdiyat-e-Aasab (Nervous System Calming)",
        description: "Reducing central sympathetic tone and anxiety with Withania somnifera (Asgandh) and Centella asiatica."
      },
      stage2: {
        name: "Taghziya-e-Mani (Nutritive Seminal Enrichment)",
        description: "Administering classical Mughalliz-e-Mani and Muqawwi-e-Bah botanical-mineral formulations."
      },
      stage3: {
        name: "Taqwiyat-e-A'za-e-Ra'eesah (Principal Organ Fortification)",
        description: "Cardiovascular and hepatic tonics ensuring optimal nitric oxide release and hormonal clearance."
      },
      stage4: {
        name: "Hifz-e-Quwat (Vitality Preservation)",
        description: "Sustainable sleep hygiene and regenerative exercise protocols."
      },
      dietaryDirectives: [
        "Inclusion of soaked almonds, walnuts, pine nuts, and pumpkin seeds",
        "Grass-fed dairy, honey, saffron infusion, and pomegranate reduction",
        "Elimination of nicotine, excess caffeine, and heavy late-night dinners"
      ],
      regimenalTherapies: [
        "Natool (Herbal cooling irrigation over the scalp to reduce nervous excitability)",
        "Dalk (Therapeutic spinal friction massage with revitalizing oils)",
        "Pelvic floor strengthening and diaphragmatic breathing routines"
      ]
    },
    followUp: {
      schedule: "Consultations at Week 2, 6, 12, and 16 with digital adherence tracking.",
      biomarkersTracked: ["International Index of Erectile Function (IIEF-5)", "Repeat Semen Analysis at Week 12", "Serum Total Testosterone at Week 16"]
    },
    evidenceAndLimitations: {
      summary: "Double-blind randomized trials on Withania somnifera and Mucuna pruriens have established significant increases in sperm concentration, motility, and salivary testosterone alongside marked cortisol reductions.",
      limitations: "Anatomical defects (severe varicocele Grade III, obstructive azoospermia) necessitate surgical evaluation.",
      citations: [
        "Ahmad MK, et al. Withania somnifera improves semen quality by regulating reproductive hormone levels. Fertil Steril. 2010;94(3):989-996.",
        "Shukla KK, et al. Mucuna pruriens improves male fertility by its action on the hypothalamus-pituitary-gonadal axis. Fertil Steril. 2009;92(4):1334-1340."
      ]
    },
    faqs: [
      {
        question: "Are these formulations safe for long-term use?",
        answer: "Yes. All ZAYVORA reproductive formulations undergo strict heavy-metal and microbial testing, and contain no synthetic PDE-5 inhibitors or banned adulterants."
      },
      {
        question: "How soon can I expect improvements in vitality and energy?",
        answer: "Most patients report improved sleep quality and reduced nervous fatigue within 2 to 3 weeks, with reproductive parameters demonstrating measurable changes over 8 to 12 weeks."
      }
    ]
  },

  "musculoskeletal": {
    slug: "musculoskeletal",
    title: "Musculoskeletal & Joint Health",
    unaniTerm: "Waja-ul-Mafasil wa Niqris",
    subtitle: "Clinical pathways for osteoarthritis, cervical/lumbar spondylosis, gouty arthralgia, and synovial inflammation.",
    category: "Rheumatology & Orthopedics",
    duration: "8 to 20 Weeks",
    overview: "Joint disorders in Unani medicine (Waja-ul-Mafasil) are understood as the accumulation of cold, viscous humoral waste (Khilt-e-Balgham or Sauda) in the articular cartilage and synovial cavities, obstructing local blood flow and leading to degeneration and pain.",
    symptoms: [
      "Joint stiffness, especially pronounced during cold mornings or after rest",
      "Crepitus, dull ache, and localized joint tenderness on weight-bearing",
      "Reduced range of motion in knees, hips, or cervical spine",
      "Episodic joint swelling without active erythema or fever",
      "Associated muscular spasm in paraspinal or quadriceps musculature"
    ],
    contributingFactors: [
      "Exposure to cold-damp environments (Buroodat wa Rutoobat)",
      "Age-related loss of synovial natural moisture (Rutoobat-e-Ghareezia)",
      "Poor alignment, past traumatic joint injury, or repetitive mechanical strain",
      "Elevated serum uric acid crystallizing within articular tissues"
    ],
    redFlags: [
      "Hot, acutely swollen, erythematous single joint with high-grade fever (Septic Arthritis) — Call 112 immediately",
      "Rapid-onset weakness in lower limbs with loss of bladder or bowel control (Cauda Equina Syndrome)",
      "Recent severe trauma with joint deformity or inability to bear any weight",
      "Unremitting night pain unrelated to movement"
    ],
    assessment: {
      mizajEvaluation: "Evaluation of joint temperament; distinguishing between warm inflammatory arthralgia (Damawi/Safrawi) and cold degenerative osteoarthritis (Balghami/Saudawi).",
      physicalExamination: "Articular range of motion, ligamentous stability testing, palpation for effusions, and gait evaluation.",
      laboratoryInvestigations: [
        "Serum Uric Acid and Rheumatoid Factor (RF)",
        "Anti-Cyclic Citrullinated Peptide (Anti-CCP)",
        "Erythrocyte Sedimentation Rate (ESR) and C-Reactive Protein (CRP)",
        "Weight-Bearing Bilateral Radiographs (X-rays) of affected joints"
      ]
    },
    treatmentApproach: {
      stage1: {
        name: "Tanqiya-e-Mawad (Articular Humoral Evacuation)",
        description: "Evacuation of cold-viscous humor using purified Colchicum autumnale (Suranjan Mudabbar) and gentle purgatives."
      },
      stage2: {
        name: "Tahleel-e-Waram (Anti-inflammatory Resolution)",
        description: "Administering Boswellia serrata (Kundur) and Commiphora mukul (Guggulu) to resolve peri-articular edema."
      },
      stage3: {
        name: "Taqwiyat-e-Mafasil (Joint Cartilage Tonification)",
        description: "Mineral-rich marine calces (Kushta Sadaf) supporting subchondral bone density."
      },
      stage4: {
        name: "Hifz-e-Harkat (Mobility Preservation)",
        description: "Low-impact rehabilitation, functional kinesiology, and joint protection guidance."
      },
      dietaryDirectives: [
        "Elimination of excessive cold, sour foods (yogurt at night, citrus excesses) and purine-dense organ meats",
        "Inclusion of ginger, turmeric, black pepper, garlic, and bone broths",
        "Adequate hydration with warm herbal infusions"
      ],
      regimenalTherapies: [
        "Natool (Continuous warm herbal decoction irrigation over the affected joints)",
        "Zimad (Topical therapeutic poultices with anti-inflammatory herbal pastes)",
        "Dalk-e-Layyin (Gentle therapeutic oil massage with Roghan-e-Suranjan or Roghan-e-Balsan)"
      ]
    },
    followUp: {
      schedule: "Consultations every 3 weeks with functional movement score monitoring.",
      biomarkersTracked: ["WOMAC Osteoarthritis Index", "Visual Analog Scale (VAS) for Pain", "Serum ESR / hs-CRP Levels at Week 12"]
    },
    evidenceAndLimitations: {
      summary: "Boswellia serrata and Colchicum autumnale possess well-documented 5-LOX inhibitory and microtubule-stabilizing mechanisms that significantly alleviate joint pain and improve physical function in clinical trials.",
      limitations: "End-stage tricompartmental osteoarthritis (Kellgren-Lawrence Grade IV) with complete joint space loss may ultimately necessitate orthopedic joint replacement.",
      citations: [
        "Sengupta K, et al. A double blind, randomized, placebo controlled study of the efficacy and safety of 5-Loxin for treatment of osteoarthritis. Arthritis Res Ther. 2008;10(4):R85.",
        "Al-Snafi AE. Chemical constituents and pharmacological activities of Colchicum autumnale. IOSR J Pharm. 2018;8(9):44-50."
      ]
    },
    faqs: [
      {
        question: "Is Suranjan (Colchicum) safe to take for joints?",
        answer: "In its raw state Colchicum contains potent alkaloids. At ZAYVORA, all Suranjan preparations strictly undergo statutory Schedule E(1) Mudabbar purification (repeated milk boiling and detoxification) to ensure safety and clinical efficacy."
      },
      {
        question: "Can these therapies help with chronic lower back pain?",
        answer: "Yes. Spondylosis and lumbar muscular spasms respond exceptionally well to our combination of oral Boswellia formulations and targeted Natool (herbal oil fomentation)."
      }
    ]
  },

  "sleep-stress": {
    slug: "sleep-stress",
    title: "Sleep Architecture & Stress",
    unaniTerm: "Sahar wa Fikr wa Zoaf-e-Dimagh",
    subtitle: "Comprehensive neuro-regulative therapy for chronic insomnia, sympathetic hyperarousal, and mental exhaustion.",
    category: "Neurology & Integrative Psychiatry",
    duration: "6 to 12 Weeks",
    overview: "Sleep disorders (Sahar) and mental tension (Fikr) in Unani clinical philosophy stem from excessive dryness and heat in the cerebral parenchyma (Yubusat wa Hararat-e-Dimagh). When mental agitation drains cerebral moistures, restorative delta-wave sleep is disrupted.",
    symptoms: [
      "Prolonged sleep onset latency exceeding 45 minutes",
      "Frequent nocturnal awakenings with racing thoughts",
      "Unrefreshing morning sleep accompanied by daytime brain fog",
      "Chronic irritability, sensory hypersensitivity, and physical tension",
      "Tension-type headaches centered around temples or vertex"
    ],
    contributingFactors: [
      "Circadian disruption from evening blue-light exposure (Tashweesh-e-Basari)",
      "Overactive cognitive rumination and unresolved emotional strain",
      "Excessive consumption of caffeinated or stimulant substances",
      "Decline in natural cerebral soothing moisture (Rutoobat-e-Dimagh)"
    ],
    redFlags: [
      "Active suicidal ideation or intent to harm oneself — Call 112 or Tele-MANAS (14416) immediately",
      "Sudden severe explosive headache unlike any previously experienced ('Thunderclap')",
      "Acute psychotic episode, hallucinations, or severe disorientation",
      "Associated new-onset seizures or focal motor deficits"
    ],
    assessment: {
      mizajEvaluation: "Evaluation of cerebral and cardiac temperament; assessing dry-hot versus dry-cold cerebral dyscrasia.",
      physicalExamination: "Neurological cranial nerve screening, pupillary light reflex check, temporal artery palpation, and resting pulse rate.",
      laboratoryInvestigations: [
        "Thyroid Function Tests (Free T3, Free T4, TSH)",
        "Serum Morning Cortisol and 24-Hour Urine Catecholamines (if indicated)",
        "Serum Vitamin B12 and Vitamin D3 (25-OH)",
        "Complete Iron Panel (Serum Ferritin, Transferrin Saturation)"
      ]
    },
    treatmentApproach: {
      stage1: {
        name: "Tarleeb-e-Dimagh (Cerebral Moistening)",
        description: "Administering brain-moistening botanical confections containing Prunus amygdalus and Lactuca sativa."
      },
      stage2: {
        name: "Taskeen-e-Aasab (Nervous Sedation)",
        description: "Utilizing Valeriana wallichii (Asarun) and Nardostachys jatamansi to promote GABAergic inhibitory tone."
      },
      stage3: {
        name: "Taqwiyat-e-Qalb wa Dimagh (Neuro-Cardiac Fortification)",
        description: "Cardioneuro-tonics (Khamira Gaozaban Ambari) stabilizing autonomic emotional swings."
      },
      stage4: {
        name: "Istiqrar-e-Naum (Sleep Homeostasis)",
        description: "Permanent circadian entrainment, morning sunlight exposure, and evening temperature modulation."
      },
      dietaryDirectives: [
        "Warm milk infused with crushed almonds, cardamoms, and a pinch of nutmeg before bedtime",
        "Fresh gourd soups, lettuce, pumpkin seeds, and ripe sweet apples",
        "Strict cessation of caffeine and nicotine intake past 2:00 PM"
      ],
      regimenalTherapies: [
        "Nutool (Slow, warm rhythmic irrigation of sesame or pumpkin seed oil over the forehead/vertex)",
        "Shamoom (Aromatic inhalation of Rosa damascena and Nymphaea alba essences)",
        "Tadheen (Gentle scalp massage with cooling botanical oils before sleep)"
      ]
    },
    followUp: {
      schedule: "Weekly virtual check-in for 4 weeks, transitioning to bi-weekly reviews.",
      biomarkersTracked: ["Pittsburgh Sleep Quality Index (PSQI)", "Generalized Anxiety Disorder 7-item (GAD-7) Scale", "Sleep Latency Logs"]
    },
    evidenceAndLimitations: {
      summary: "Randomized double-blind studies have shown that standardized extracts of Nardostachys jatamansi and Valeriana wallichii modulate central GABA-A receptor complexes, reducing sleep latency without inducing next-morning sedation.",
      limitations: "Severe clinical major depressive disorder with psychotic features or bipolar mania requires immediate psychiatric care and psychopharmacology.",
      citations: [
        "Salter S, et al. Treating primary insomnia - the efficacy of valerian and hops. Aust Fam Physician. 2010;39(6):433-437.",
        "Rao VS, et al. Neuropharmacological activities of Nardostachys jatamansi. J Ethnopharmacol. 2005;98(1-2):191-196."
      ]
    },
    faqs: [
      {
        question: "Are ZAYVORA sleep formulations habit-forming like benzodiazepines?",
        answer: "No. Our botanical formulations act as adaptogens and neuro-tonics, nourishing cerebral pathways rather than inducing chemical dependence or daytime withdrawal grogginess."
      },
      {
        question: "How does Nutool therapy help sleep?",
        answer: "Nutool (continuous rhythmic oil streaming onto the forehead) stimulates cutaneous mechanoreceptors, triggering profound parasympathetic activation and slowing alpha rhythms."
      }
    ]
  },

  "liver-metabolic": {
    slug: "liver-metabolic",
    title: "Hepatic Axis & Liver Health",
    unaniTerm: "Zoaf-e-Kabid wa Su-e-Qinya",
    subtitle: "Evidence-based protocols for non-alcoholic fatty liver disease (NAFLD), elevated transaminases, and sluggish hepatic clearance.",
    category: "Hepatology",
    duration: "12 to 24 Weeks",
    overview: "The liver (Kabid) is hailed in Unani medicine as the central laboratory of the body, responsible for second digestion (Hazm-e-Kabidi) and the generation of the four humors. Sluggish hepatic metabolism allows toxic metabolic byproducts (Fuzlaat) to stagnate in tissue microenvironments.",
    symptoms: [
      "Persistent right upper quadrant dull fullness or heaviness",
      "Chronic daytime lethargy and unrefreshing rest",
      "Sallow, dull complexion with mild scleral icteric tint",
      "Intolerance to fatty or heavily seasoned foods",
      "Mild pruritus and post-prandial nausea"
    ],
    contributingFactors: [
      "Excessive consumption of refined carbohydrates, trans-fats, and alcohol",
      "Visceral insulin resistance driving free fatty acid overflow into hepatocytes",
      "Accumulation of cold-viscous humor (Khilt-e-Balgham) obstructing hepatic sinusoids",
      "Chronic pharmaceutical polypharmacy taxing Phase I & II liver detoxification pathways"
    ],
    redFlags: [
      "Overt jaundice (bright yellow sclera and skin) accompanied by dark cola-colored urine",
      "Abdominal distension with shifting dullness (Ascites) or gross bilateral pedal edema",
      "Hematemesis (vomiting blood) or altered mental status (Hepatic Encephalopathy) — Call 112 immediately",
      "Severe acute right upper quadrant pain radiating to right shoulder with high fever"
    ],
    assessment: {
      mizajEvaluation: "Determination of hepatic Mizaj (Har/Barid/Yabis/Ratab); identifying hot inflammatory versus cold congested hepatomegaly.",
      physicalExamination: "Abdominal examination for hepatosplenomegaly, hepatic tenderness, palmar erythema, and spider angiomas.",
      laboratoryInvestigations: [
        "Comprehensive Liver Function Tests (Total/Direct Bilirubin, SGOT, SGPT, ALP, GGT, Total Protein, Albumin)",
        "Viral Hepatitis Serologies (HBsAg, Anti-HCV)",
        "Abdominal Ultrasonography evaluating liver echogenicity and steatosis grade",
        "FibroScan (Transient Elastography) assessing liver stiffness"
      ]
    },
    treatmentApproach: {
      stage1: {
        name: "Fatah-e-Sudad (De-obstruent Clearance)",
        description: "Opening intra-hepatic sinusoidal channels with Cichorium intybus (Kasni) and Solanum nigrum (Mako)."
      },
      stage2: {
        name: "Tanqiya-e-Mawad (Biliary Cleansing)",
        description: "Gentle stimulation of bile flow and elimination of stagnated biliary sludges."
      },
      stage3: {
        name: "Taqwiyat-e-Kabid (Hepatocyte Regeneration)",
        description: "Administering Silymarin-rich botanicals and classical Dawa-ul-Kurkum formulations."
      },
      stage4: {
        name: "Hifz-e-Istehala (Metabolic Preservation)",
        description: "Long-term dietary liver protection and regular biochemical surveillance."
      },
      dietaryDirectives: [
        "Daily incorporation of Kasni (chicory) leaf decoction, radish, beetroot, and artichoke",
        "Complete elimination of ultra-processed palm oils, deep-fried snacks, and alcoholic beverages",
        "Evening meal completed at least 3.5 hours before sleep"
      ],
      regimenalTherapies: [
        "Takmeed (Warm herbal compress over the hepatic region)",
        "Riyazat-e-Khafeefa (Light brisk walking to stimulate splanchnic blood flow)",
        "Hammam (Controlled sauna to encourage toxin elimination through the skin)"
      ]
    },
    followUp: {
      schedule: "Bi-weekly consultations for 8 weeks, followed by monthly reviews.",
      biomarkersTracked: ["Liver Enzymes (SGPT, SGOT, GGT) at Week 6, 12, and 24", "Repeat Abdominal Ultrasound or FibroScan at Month 6", "Fasting Lipid Profile"]
    },
    evidenceAndLimitations: {
      summary: "Cichorium intybus and Solanum nigrum (the foundational herbs of classical Arq Kasni and Arq Mako) demonstrate significant antioxidant, anti-inflammatory, and hepatoprotective efficacy, reducing transaminase leakage in NAFLD clinical trials.",
      limitations: "Decompensated cirrhosis, portal hypertension, and acute fulminant viral hepatitis require immediate inpatient hepatology and critical care.",
      citations: [
        "Ahmed B, et al. Antihepatotoxic activity of Cichorium intybus. J Ethnopharmacol. 2003;87(2-3):237-240.",
        "Raju K, et al. Antihepatotoxic activity of Solanum nigrum against carbon tetrachloride induced liver damage. Biol Pharm Bull. 2003;26(11):1618-1619."
      ]
    },
    faqs: [
      {
        question: "Can Unani medicine reverse Grade 1 or Grade 2 Fatty Liver?",
        answer: "Yes. Grade 1 and 2 hepatic steatosis show excellent reversibility when ZAYVORA de-obstruent botanicals (Kasni, Mako) are combined with strict dietary glycemic control and weight reduction."
      },
      {
        question: "How are ZAYVORA liver tonics monitored for safety?",
        answer: "Every formulation is analyzed for heavy metals (lead, arsenic, mercury, cadmium) via ICP-MS, and regular serial LFT blood tests ensure complete safety and therapeutic progress."
      }
    ]
  },

  "respiratory": {
    slug: "respiratory",
    title: "Respiratory & Pulmonology",
    unaniTerm: "Amraz-e-Tanaffus wa Zeequn Nafas",
    subtitle: "Targeted clinical protocols for bronchial asthma, allergic rhinitis, chronic bronchitis, and respiratory mucosal integrity.",
    category: "Pulmonology",
    duration: "6 to 16 Weeks",
    overview: "Respiratory conditions in Unani doctrine (Amraz-e-Tanaffus) arise from the descent of cold catarrhal phlegm (Nuzla) into the bronchial tree, causing bronchospasm, mucosal swelling, and airway obstruction (Zeequn Nafas).",
    symptoms: [
      "Recurrent episodes of wheezing, chest tightness, and dyspnea",
      "Persistent productive cough with viscous white or clear sputum",
      "Paroxysmal sneezing, nasal congestion, and post-nasal drip",
      "Exertional breathlessness exacerbated by cold air or dampness",
      "Nocturnal coughing spells interrupting sleep"
    ],
    contributingFactors: [
      "Environmental allergen and particulate air pollution exposure (Ghubar)",
      "Systemic Balghami (phlegmatic) dyscrasia weakening pulmonary tone",
      "Cold-damp climate exposure without adequate respiratory protection",
      "Underlying gastroesophageal reflux irritating respiratory vagal receptors"
    ],
    redFlags: [
      "Acute severe respiratory distress with inability to speak in complete sentences — Call 112 immediately",
      "Central cyanosis (bluish coloration of lips or tongue)",
      "Hemoptysis (coughing up fresh blood)",
      "Accessory muscle retractions (sternocleidomastoid indrawing) during quiet breathing"
    ],
    assessment: {
      mizajEvaluation: "Evaluation of pulmonary and cerebral Mizaj; distinguishing between hot-inflammatory and cold-phlegmatic bronchospasm.",
      physicalExamination: "Chest auscultation for wheezing, rhonchi, or crepitations; examination of nasal turbinates for allergic polyps.",
      laboratoryInvestigations: [
        "Complete Blood Count with Absolute Eosinophil Count (AEC)",
        "Serum Total Immunoglobulin E (IgE)",
        "Spirometry (FEV1, FVC, FEV1/FVC ratio with bronchodilator reversibility)",
        "Chest Radiograph (PA View) to rule out consolidation or active infection"
      ]
    },
    treatmentApproach: {
      stage1: {
        name: "Inzaj-e-Balgham (Mucolytic Maturation)",
        description: "Liquefying thick pulmonary catarrh using Adhatoda vasica (Arusa) and Glycyrrhiza glabra (Asl-us-Soos)."
      },
      stage2: {
        name: "Ikhraj-e-Balgham (Expectorant Evacuation)",
        description: "Clearing bronchial tree through natural bronchodilatory herbal decoctions (La'ooq formulations)."
      },
      stage3: {
        name: "Taqwiyat-e-Riya (Pulmonary Fortification)",
        description: "Strengthening bronchial mucosal defense and tonifying the diaphragm."
      },
      stage4: {
        name: "Hifz-e-Majra (Airway Preservation)",
        description: "Seasonal allergy prophylactic regimens and respiratory breathing exercises."
      },
      dietaryDirectives: [
        "Warm broths flavored with black pepper, cloves, basil leaves, and ginger",
        "Strict avoidance of refrigerated items, ice creams, cold yogurt, and deep-fried snacks",
        "Daily sipping of lukewarm water infused with honey and licorice"
      ],
      regimenalTherapies: [
        "Bukhoor (Medicated herbal steam inhalation with Eucalyptus and Thymus serpyllum)",
        "Takmeed (Warm dry fomentation over the anterior and posterior chest wall)",
        "Habs-e-Nafas (Gentle guided pranayama and diaphragmatic expansion exercises)"
      ]
    },
    followUp: {
      schedule: "Weekly follow-up during acute stabilization; monthly reviews for maintenance.",
      biomarkersTracked: ["Peak Expiratory Flow Rate (PEFR) Diaries", "Asthma Control Test (ACT) Score", "Serial Absolute Eosinophil Count"]
    },
    evidenceAndLimitations: {
      summary: "Vasicine alkaloids from Adhatoda vasica exert potent bronchodilatory, mucolytic, and anti-allergic actions, comparable to mild beta-2 agonists in clinical trials.",
      limitations: "Status asthmaticus and severe hypoxemic respiratory failure require emergency hospital admission, supplemental oxygen, and nebulized bronchodilators.",
      citations: [
        "Atal CK. Chemistry and pharmacology of vasicine: a new oxytocic and abortifacient. Indian Drugs. 1980;17:371-374.",
        "Gupta OP, et al. Neuromuscular blocking activity of vasicine and its analogues. Indian J Exp Biol. 1977;15:107-110."
      ]
    },
    faqs: [
      {
        question: "Can I stop using my steroid inhaler while taking ZAYVORA medicines?",
        answer: "No. Never discontinue prescribed inhalers abruptly. As pulmonary resistance improves, your pulmonologist will supervise any safe step-down of inhalation therapies."
      },
      {
        question: "How does herbal steam inhalation (Bukhoor) help?",
        answer: "Bukhoor delivers volatile terpene fractions directly to the bronchial mucosa, thinning thick tenaceous mucus and soothing hyper-reactive airway spasms."
      }
    ]
  },

  "womens-health": {
    slug: "womens-health",
    title: "Women's Hormonal & Pelvic Health",
    unaniTerm: "Amraz-e-Niswan wa Ihtebas-e-Tams",
    subtitle: "Compassionate, clinician-guided care for PCOS, menstrual irregularities, dysmenorrhea, and menopausal wellness.",
    category: "Gynecology & Women's Health",
    duration: "12 to 24 Weeks",
    overview: "In classical Unani gynecology (Amraz-e-Niswan), female hormonal balance depends on the unhindered flow of vital fluids and optimal uterine temperament (Mizaj-e-Rehm). Chronic pelvic congestion, emotional strain, or cold humoral accumulations lead to menstrual irregularity and anovulation.",
    symptoms: [
      "Oligomenorrhea (delayed cycles) or amenorrhea (absent menstruation)",
      "Severe spasmodic dysmenorrhea (pelvic cramping) during menses",
      "Persistent cystic acne, hirsutism, and androgenic alopecia",
      "Pelvic fullness, chronic fatigue, and pre-menstrual mood disturbances",
      "Perimenopausal vasomotor hot flashes and night sweats"
    ],
    contributingFactors: [
      "Pelvic venous congestion and cold uterine dyscrasia (Buroodat-e-Rehm)",
      "Hyperinsulinemia driving ovarian theca-cell androgen synthesis",
      "Chronic emotional distress elevating prolactin and suppressing LH pulsatility",
      "Sedentary desk work impairing pelvic microcirculation"
    ],
    redFlags: [
      "Acute severe lower quadrant pelvic pain with fainting (suspected ectopic pregnancy/ovarian torsion) — Call 112 immediately",
      "Sudden heavy vaginal hemorrhage soaking more than 2 pads per hour for over 2 consecutive hours",
      "Post-menopausal vaginal bleeding of any volume requiring urgent endometrial evaluation",
      "High fever accompanied by purulent vaginal discharge and pelvic peritonitis"
    ],
    assessment: {
      mizajEvaluation: "Evaluation of uterine and systemic Mizaj; identifying whether pelvic stasis is rooted in Balghami coldness or Saudawi obstruction.",
      physicalExamination: "Abdominal palpation for uterine/adnexal masses, thyroid examination, and clinical scoring of hirsutism (Ferriman-Gallwey scale).",
      laboratoryInvestigations: [
        "Day 2–3 Serum Hormonal Profile (FSH, LH, Estradiol, Total Testosterone, DHEA-S, Prolactin)",
        "Fasting Insulin and Homeostatic Model Assessment (HOMA-IR)",
        "Thyroid Panel (TSH, Free T4)",
        "Pelvic Ultrasonography (Transabdominal/TVS) assessing ovarian morphology and endometrial thickness"
      ]
    },
    treatmentApproach: {
      stage1: {
        name: "Tahleel-e-Warm-e-Rehm (Pelvic Decongestion)",
        description: "Clearing uterine micro-congestions with Saraca asoca (Ashoka) and Foeniculum vulgare (Saunf)."
      },
      stage2: {
        name: "Idrar-e-Tams (Menstrual Flow Harmonization)",
        description: "Promoting natural rhythmic follicular maturation and regularizing menstrual cycle cadence."
      },
      stage3: {
        name: "Taqwiyat-e-Rehm (Uterine Tonification)",
        description: "Nourishing ovarian reserve and reproductive tissues with Majun Supari Pak and natural calces."
      },
      stage4: {
        name: "Hifz-e-Dawra (Cycle Regularity Maintenance)",
        description: "Phase-aligned dietary seeding, circadian stabilization, and continuous lifestyle guidance."
      },
      dietaryDirectives: [
        "Inclusion of sesame seeds, flaxseeds, methi seeds, and fresh pomegranate juice",
        "Minimization of dairy foods, commercial poultry, and high-glycemic refined flour",
        "Drinking warm infusion of ajwain and jaggery during pre-menstrual days"
      ],
      regimenalTherapies: [
        "Abzen (Warm sitz bath with decoctions of chamomile, rose petals, and alum)",
        "Takmeed (Warm herbal compress over the lower hypogastrium)",
        "Riyazat (Specific pelvic-opening asanas and daily brisk walking)"
      ]
    },
    followUp: {
      schedule: "Consultation aligned with menstrual cycle phases (every 4 weeks).",
      biomarkersTracked: ["Menstrual Diary Logs (Cycle Length, Bleeding Days)", "Basal Body Temperature Tracking", "Repeat Pelvic Ultrasound at Month 6"]
    },
    evidenceAndLimitations: {
      summary: "Clinical trials on standardized Saraca asoca, Symplocos racemosa, and Aloe barbadensis formulations show significant recovery of ovulatory cycles and reduction in LH:FSH ratios in women with PCOS.",
      limitations: "Complex structural anomalies (large submucosal fibroids > 5cm, complex ovarian cysts with solid components) require gynecological surgical evaluation.",
      citations: [
        "Priya G, et al. A review of Saraca asoca for gynecological disorders. Int J Pharm Sci Res. 2012;3(9):3040-3047.",
        "Kaur S, et al. Plant-derived bioactive compounds for polycystic ovary syndrome. Phytother Res. 2021;35(4):1858-1875."
      ]
    },
    faqs: [
      {
        question: "Can ZAYVORA help restore periods in PCOS without birth control pills?",
        answer: "Yes. Our focus is addressing the root insulin resistance and uterine dyscrasia to restore spontaneous ovulation naturally, rather than inducing artificial withdrawal bleeds."
      },
      {
        question: "Are these treatments safe if I am planning pregnancy?",
        answer: "Certain herbs are safe for preconception tonification, while others are emmenagogues contraindicated in pregnancy. Your ZAYVORA clinician strictly customizes prescriptions based on your conception timeline."
      }
    ]
  },

  "mens-health": {
    slug: "mens-health",
    title: "Men's Health & Andrology",
    unaniTerm: "Amraz-e-Rijal wa Zoaf-e-A'da-e-Tanasul",
    subtitle: "Integrative clinical care for male hormonal resilience, vitality, prostate health, and physical endurance.",
    category: "Andrology & Urology",
    duration: "8 to 16 Weeks",
    overview: "Men's health in Unani doctrine centers around preserving Hararat-e-Ghareezia (vital innate warmth) and the hormonal feedback loop between the brain, liver, and testes. When physical and mental exhaustion drains systemic reserves, andrological debility ensues.",
    symptoms: [
      "Progressive decline in physical stamina and morning vitality",
      "Stress-related reproductive fatigue and performance apprehension",
      "Nocturnal micturition frequency and weak urinary stream (mild BPH signs)",
      "Loss of lean muscle mass with increasing visceral adiposity",
      "Persistent mental fatigue and low drive"
    ],
    contributingFactors: [
      "Chronic occupational burnout and elevated cortisol depleting gonadotropins",
      "Lack of restorative deep sleep and late-night digital exposure",
      "Pelvic congestion from prolonged sedentary seated posture",
      "Nutritional deficits lacking key phytonutrients and micro-minerals"
    ],
    redFlags: [
      "Acute urinary retention (inability to pass urine with excruciating suprapubic pain) — Call 112 immediately",
      "Gross painless hematuria (blood in urine) requiring immediate urological workup",
      "Sudden onset severe scrotal pain with nausea (testicular torsion)",
      "Rapidly rising PSA or hard irregular prostate nodule on palpation"
    ],
    assessment: {
      mizajEvaluation: "Determination of baseline constitutional temperament and evaluation of cold-dry genital organ dyscrasia.",
      physicalExamination: "Digital rectal examination (DRE) referral review, blood pressure check, and waist-to-height ratio assessment.",
      laboratoryInvestigations: [
        "Serum Total & Free Testosterone, SHBG, and LH",
        "Serum Prostate-Specific Antigen (Total and Free PSA)",
        "Metabolic Panel (Fasting Glucose, Lipid Profile, LFT)",
        "Uroflowmetry and Post-Void Residual Urine Ultrasound (if lower urinary tract symptoms exist)"
      ]
    },
    treatmentApproach: {
      stage1: {
        name: "Mu'addil-e-Aasab (Nervous System Calibration)",
        description: "Reducing sympathetic overdrive with Withania somnifera and Tribulus terrestris (Gokhru)."
      },
      stage2: {
        name: "Mughalliz-e-Mani (Vitality Tonification)",
        description: "Administering classical restorative confections (Laboob Kabeer, Majun Salab) to rebuild stamina."
      },
      stage3: {
        name: "Taqwiyat-e-Masana (Prostate & Bladder Support)",
        description: "Supporting prostate microcirculation with Cucurbita pepo (pumpkin seed) and Serenoa repens."
      },
      stage4: {
        name: "Hifz-e-Quwat (Endurance Preservation)",
        description: "Progressive resistance training guidelines and sustained stress resilience protocols."
      },
      dietaryDirectives: [
        "Daily raw pumpkin seeds, soaked almonds, walnuts, and pomegranate juice",
        "Adequate lean protein, leafy greens, garlic, and cold-pressed sesame oil",
        "Elimination of excessive alcohol, smoking, and refined fried foods"
      ],
      regimenalTherapies: [
        "Dalk (Therapeutic full-body friction massage with strengthening oils)",
        "Natool (Herbal decanted oil streaming to soothe lumbar nerve roots)",
        "Pelvic floor conditioning and regular interval physical training"
      ]
    },
    followUp: {
      schedule: "Consultations at Week 2, 6, 10, and 16 with digital outcome tracking.",
      biomarkersTracked: ["Aging Males' Symptoms (AMS) Score", "International Prostate Symptom Score (IPSS)", "Serum Testosterone at Week 16"]
    },
    evidenceAndLimitations: {
      summary: "Clinical trials on Tribulus terrestris and Withania somnifera demonstrate significant improvements in male vitality scores, lean body mass, and subjective well-being.",
      limitations: "Severe anatomical prostate enlargement with severe bladder outflow obstruction requires conventional urological intervention.",
      citations: [
        "Santos CA, et al. Tribulus terrestris versus placebo in the treatment of erectile dysfunction. Actas Urol Esp. 2014;38(4):244-248.",
        "Wankhede S, et al. Examining the effect of Withania somnifera on muscle strength and recovery. J Int Soc Sports Nutr. 2015;12:43."
      ]
    },
    faqs: [
      {
        question: "Does ZAYVORA use any synthetic hormones or steroids?",
        answer: "Absolutely not. All formulations are 100% botanical and natural mineral preparations validated under Schedule M-I AYUSH-GMP standards."
      },
      {
        question: "Can these therapies help with early prostate enlargement (BPH)?",
        answer: "Yes. In early to moderate BPH, our specialized phytotherapeutic protocols help reduce inflammation and improve urinary flow mechanics."
      }
    ]
  }
};
