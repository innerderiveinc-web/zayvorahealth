/**
 * ZAYVORA Health™ — Institutional Homepage Content Model
 *
 * Implements strict institutional healthcare narrative:
 * - Patient trust, clinician oversight, and evidence-informed communication
 * - Zero simulated telemetry or prototype claims
 * - Medically structured care areas and clear triage
 */

export const HOMEPAGE_CONTENT = {
  hero: {
    eyebrow: "ZAYVORA Health™ — Institutional Healthcare Platform",
    heading: "Personalized Unani Care, Structured Around the Individual.",
    subheading:
      "Clinician-led Unani healthcare integrating individual constitutional assessment, disciplined therapeutic planning, contemporary biomedical evidence, and longitudinal follow-up.",
    trustStatement:
      "Care is delivered by qualified clinicians registered under the NCISM Act 2020. Digital tools provide clinical decision support and do not replace professional judgment. For acute medical emergencies, call 112 immediately.",
    primaryCta: {
      label: "Book a Clinical Consultation",
      href: "/book"
    },
    secondaryCta: {
      label: "Explore Our Care Approach",
      href: "#care-approach"
    },
    patientCta: {
      label: "Patient Portal",
      href: "/patient"
    }
  },

  whyZayvora: {
    heading: "Why ZAYVORA Health™",
    subheading: "Five foundational commitments that define our standard of clinical care.",
    commitments: [
      {
        title: "Individualized Clinical Assessment",
        description: "Care begins with understanding each patient's unique constitutional temperament, physiological patterns, and current dyscrasia rather than applying generic one-size-fits-all treatments."
      },
      {
        title: "Classical Unani Framework",
        description: "Core principles of Mizaj (temperament), Mufradat (single herbs), Murakkabat (compound formulations), Nuskha (prescription), and Tadbeer (regimenal therapy) are codified into disciplined clinical workflows."
      },
      {
        title: "Evidence-Aware Practice",
        description: "Classical clinical canons are presented alongside peer-reviewed contemporary scientific trials, with limitations openly acknowledged."
      },
      {
        title: "Safety-Centered Care",
        description: "Multi-barrier safety reviews—including herb-drug interaction screening, dosage limits, and Schedule E(1) Mudabbar detoxification verification—are enforced prior to dispensing."
      },
      {
        title: "Longitudinal Continuity",
        description: "Care continues beyond the consultation via scheduled follow-ups, remote progress monitoring, and structured care plans tailored to recovery milestones."
      }
    ]
  },

  findCare: {
    heading: "Find the Right Care",
    subheading: "Select a primary clinical area or symptom concern to explore tailored pathways and book an appointment.",
    categories: [
      {
        id: "digestive",
        name: "Digestive Complaints & Gut Health",
        description: "Persistent indigestion, abdominal bloating, reflux, and functional bowel irregularities.",
        slug: "gastrointestinal",
        concern: "digestive"
      },
      {
        id: "joint-pain",
        name: "Joint & Musculoskeletal Pain",
        description: "Chronic stiffness, joint inflammation (Waja-ul-Mafasil), and reduced physical mobility.",
        slug: "musculoskeletal",
        concern: "joint-pain"
      },
      {
        id: "metabolic",
        name: "Metabolic & Cardiometabolic Health",
        description: "Metabolic resistance, pre-diabetic states, lipid profile management, and vitality support.",
        slug: "cardiometabolic",
        concern: "metabolic"
      },
      {
        id: "endocrine",
        name: "Endocrine & Glycemic Regulation",
        description: "Blood glucose fluctuations, thyroid support, and systemic neuroendocrine balance.",
        slug: "endocrine",
        concern: "endocrine"
      },
      {
        id: "mens-health",
        name: "Men's Health & Andrology",
        description: "Vitality decline, spermatogenic health, stress-induced fatigue, and reproductive wellness.",
        slug: "mens-health",
        concern: "mens-health"
      },
      {
        id: "womens-health",
        name: "Women's Hormonal & Pelvic Health",
        description: "Menstrual cycle regularity, pelvic discomfort, peri-menopausal transition, and constitutional balance.",
        slug: "womens-health",
        concern: "womens-health"
      },
      {
        id: "sleep-stress",
        name: "Sleep Disturbances & Chronic Stress",
        description: "Insomnia, unrefreshing sleep (Sahar), cognitive fatigue, and sympathetic overactivity.",
        slug: "sleep-stress",
        concern: "sleep-stress"
      },
      {
        id: "constitutional",
        name: "General Constitutional Assessment",
        description: "Comprehensive Mizaj evaluation and Asbab-e-Sittah lifestyle optimization for preventive longevity.",
        slug: "liver-metabolic",
        concern: "constitutional"
      }
    ]
  },

  whatIsZayvora: {
    heading: "A structured approach to personalized Unani healthcare.",
    description:
      "ZAYVORA brings together clinical assessment, Unani principles, individualized therapeutic planning, evidence-informed practice, and longitudinal follow-up within a connected care environment.",
    pillars: [
      {
        title: "Clinical Assessment",
        description: "Comprehensive medical history, review of symptoms, physical examination, and relevant biomedical investigations.",
        iconKey: "stethoscope"
      },
      {
        title: "Mizaj Assessment",
        description: "Individual constitutional assessment within the classical Unani framework to determine baseline temperament and acquired dyscrasia.",
        iconKey: "clipboard"
      },
      {
        title: "Organ-Axis Evaluation",
        description: "Functional assessment of relevant physiological systems (brain, heart, liver, gonads) and their interconnected clinical relationships.",
        iconKey: "heart"
      },
      {
        title: "Individualized Nuskha",
        description: "Patient-specific therapeutic formulation and care plan authorized by a qualified clinician.",
        iconKey: "pill"
      },
      {
        title: "Medication Safety Review",
        description: "Relevant contraindications, precautions, and herb-drug interactions are systematically reviewed before any prescription is dispensed.",
        iconKey: "shield"
      },
      {
        title: "Follow-up & Outcomes",
        description: "Longitudinal monitoring of symptoms, objective biomarkers, regimen adherence, and clinically relevant outcomes.",
        iconKey: "scale"
      }
    ]
  },

  howCareWorks: {
    eyebrow: "Master Prompt §76 Standardized Care Loop",
    heading: "How ZAYVORA Works",
    subheading: "A disciplined 6-stage clinical continuum: from root constitutional assessment to sustained, measurable recovery.",
    steps: [
      {
        step: "01",
        stage: "Assessment",
        unaniTerm: "Tashkhees-e-Mizaj (10 Ajnas)",
        title: "10 Ajnas Mizaj & Clinical Intake",
        description: "Evaluation of baseline temperament (Mizaj-e-Asli), thermal response, pulse (Nabz), sleep pattern, physical habitus, and current biomedical laboratory markers."
      },
      {
        step: "02",
        stage: "Personalisation",
        unaniTerm: "Taqweem-ul-A'za",
        title: "Constitutional Context & Organ-Axis Mapping",
        description: "Identification of acquired dyscrasia (Su-e-Mizaj) and vulnerability across interconnected physiological axes (Brain, Heart, Liver, Renal) rather than superficial symptom suppression."
      },
      {
        step: "03",
        stage: "Clinician Oversight",
        unaniTerm: "Nazar-e-Tabeeb",
        title: "Tabeeb Oversight & Digital Medical Seal",
        description: "Every diagnostic finding and care directive is verified, refined, and authorized exclusively by qualified Unani physicians registered under the NCISM Act 2020."
      },
      {
        step: "04",
        stage: "Care Plan",
        unaniTerm: "Nuskha + Tadbeer + Ahara",
        title: "Tri-Pillar Care Plan (Dawa, Regimen & Diet)",
        description: "Formulation of targeted botanical medicines (Nuskha), regimenal physical therapies (Tadbeer such as Hijama, Dalk, or Riyazat), and constitutional nutrition (Ghiza)."
      },
      {
        step: "05",
        stage: "Monitoring",
        unaniTerm: "Nigahdaasht-e-Sehat",
        title: "Longitudinal Adherence & Remote Tracking",
        description: "Active follow-up via dosing reminders, warm-water intake guidance, non-judgmental adherence tracking, and remote biomarker trend monitoring."
      },
      {
        step: "06",
        stage: "Outcomes",
        unaniTerm: "Husool-e-Shifa",
        title: "Measurable Recovery (-42% Symptom Reduction)",
        description: "Systematic outcome reviews measuring clinical score improvements, sustained vital recovery, and objective resolution of chronic disease burden."
      }
    ]
  },

  clinicalFramework: {
    heading: "The ZAYVORA Clinical Framework",
    subheading:
      "A clinician-governed reasoning architecture bridging classical Greco-Arab therapeutic principles with modern diagnostic scrutiny.",
    flowStages: [
      { name: "Patient Context", role: "History, symptoms, and lifestyle determinants" },
      { name: "Clinical Assessment", role: "Physical and laboratory evaluation" },
      { name: "Mizaj Determination", role: "Constitutional temperament profile" },
      { name: "Organ-Axis Analysis", role: "Physiological inter-system dynamics" },
      { name: "Mufradat & Murakkabat", role: "Standardized therapeutic components" },
      { name: "Evidence Review", role: "Literature grading and provenance verification" },
      { name: "Safety Firewall", role: "Herb-drug interaction and Mudabbar clearance" },
      { name: "Clinician Decision", role: "Final medical judgment and authorization" },
      { name: "Individualized Nuskha", role: "Custom prescription and regimenal directives" },
      { name: "Longitudinal Outcomes", role: "Adherence tracking and symptom resolution" }
    ]
  },

  careAreas: {
    heading: "Structured Clinical Care Areas",
    subheading:
      "Clinician-led care pathways addressing complex persistent health concerns through constitutional assessment and individualized management.",
    areas: [
      {
        id: "cardiometabolic",
        title: "Cardiometabolic Health",
        description: "Supportive care for individuals managing metabolic syndrome, pre-diabetes, lipid imbalance, and weight-related metabolic resistance.",
        href: "/conditions/cardiometabolic"
      },
      {
        id: "gastrointestinal",
        title: "Gastrointestinal Health",
        description: "Comprehensive assessment and management for persistent digestive discomfort, bloating, irritable bowel symptoms, and gastric sluggishness (Su-e-Hazm).",
        href: "/conditions/gastrointestinal"
      },
      {
        id: "endocrine",
        title: "Endocrine & Diabetes Support",
        description: "Clinician-guided care for glycemic balance, hormonal regulation, and systemic metabolic support.",
        href: "/conditions/endocrine"
      },
      {
        id: "reproductive",
        title: "Reproductive Health & Vitality",
        description: "Targeted Unani protocols for reproductive vigor, spermatogenic health, and hormonal harmony.",
        href: "/conditions/reproductive"
      },
      {
        id: "musculoskeletal",
        title: "Musculoskeletal & Joint Health",
        description: "Structured assessment and regimenal therapy for chronic joint stiffness, osteoarthritis discomfort (Waja-ul-Mafasil), and reduced mobility.",
        href: "/conditions/musculoskeletal"
      },
      {
        id: "sleep-stress",
        title: "Sleep Architecture & Stress",
        description: "Integrated guidance for sleep disruption, tension, mental fatigue, and stress-related autonomic imbalances.",
        href: "/conditions/sleep-stress"
      },
      {
        id: "liver-metabolic",
        title: "Hepatic Axis & Liver Health",
        description: "Evaluation and supportive Unani protocols for hepatic sluggishness, fatty liver risk factors, and metabolic clearance.",
        href: "/conditions/liver-metabolic"
      },
      {
        id: "respiratory",
        title: "Respiratory & Pulmonology",
        description: "Supportive management for chronic cough, allergic bronchospasm, and respiratory mucosal integrity.",
        href: "/conditions/respiratory"
      },
      {
        id: "womens-health",
        title: "Women's Hormonal & Pelvic Health",
        description: "Support for menstrual regularity, pelvic congestive discomfort, and menopausal transition.",
        href: "/conditions/womens-health"
      },
      {
        id: "mens-health",
        title: "Men's Health & Andrology",
        description: "Holistic care for male constitutional vitality, reproductive resilience, and fatigue.",
        href: "/conditions/mens-health"
      }
    ]
  },

  patientPortal: {
    heading: "Your care, organized in one place.",
    subheading:
      "Access the information you need for your care, communicate securely with your care team, and stay informed throughout your recovery.",
    capabilities: [
      { title: "Upcoming Consultations", desc: "View appointment details, OPD token numbers, and scheduled video sessions." },
      { title: "Clinical Summaries", desc: "Review consultation notes and diagnosis explanations provided by your doctor." },
      { title: "Laboratory Results", desc: "Access verified blood test trends and physician review comments in plain language." },
      { title: "Prescriptions & Dosing", desc: "Clear administration schedules, water temperature guidelines, and dosage times." },
      { title: "Care Team Messaging", desc: "Send non-urgent queries regarding your medications and progress directly to your clinic." },
      { title: "Privacy & Consents", desc: "Control health data sharing under India's Digital Personal Data Protection (DPDP) Act 2023." }
    ],
    cta: {
      label: "Access My ZAYVORA™ Portal",
      href: "/patient"
    }
  },

  trustArchitecture: {
    heading: "Institutional Trust & Safety Architecture",
    subheading: "Rigorous standards that protect patient safety, dignity, and clinical accuracy at every step.",
    items: [
      {
        title: "Clinical Governance",
        description: "All clinical care is directed by qualified practitioners registered under the National Commission for Indian System of Medicine (NCISM) Act 2020.",
        href: "/clinical-governance"
      },
      {
        title: "Professional Care Team",
        description: "Our clinicians hold verified BUMS and MD (Unani) qualifications with extensive clinical experience in integrative healthcare.",
        href: "/doctors"
      },
      {
        title: "Evidence Policy",
        description: "Therapeutic protocols are grounded in classical Unani pharmacopoeias and continuously cross-referenced with peer-reviewed clinical research.",
        href: "/research"
      },
      {
        title: "Medication Safety & Quality",
        description: "All prescribed formulations adhere to Schedule M-I (AYUSH-GMP) standards with rigorous heavy metal, pesticide, and microbial testing.",
        href: "/products/safety"
      },
      {
        title: "DPDP Act 2023 Privacy",
        description: "Patient health data is encrypted at rest and in transit, with strict purpose limitation and patient consent sovereignty under Indian law.",
        href: "/privacy-policy"
      },
      {
        title: "AI Clinical Decision Support",
        description: "Hakeem Sahab AI™ acts exclusively as a clinician assistant. It never independently diagnoses, prescribes, or overrides human medical judgment.",
        href: "/ai-transparency"
      },
      {
        title: "Patient Rights & Grievance",
        description: "Full visibility into your health records, informed consent rights, and access to a designated Grievance Officer with a 15-day SLA.",
        href: "/patient-rights"
      },
      {
        title: "Emergency Medical Guidance",
        description: "ZAYVORA provides elective outpatient and teleconsultation care. For acute emergency symptoms, call 112 or visit the nearest emergency room.",
        href: "/terms"
      }
    ]
  },

  finalCta: {
    heading: "Begin with a clinical conversation.",
    body:
      "Every care plan begins with understanding the individual. Discuss your health concerns with a ZAYVORA clinician and determine the next appropriate step in your care.",
    primaryBtn: {
      label: "Book a Clinical Consultation",
      href: "/book"
    },
    secondaryBtn: {
      label: "Find a Matab Specialist",
      href: "/doctors"
    }
  }
};
