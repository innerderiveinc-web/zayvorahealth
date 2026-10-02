export interface DoctorProfile {
  id: string;
  name: string;
  salutation: string;
  designation: string;
  degrees: string;
  regNumber: string;
  experienceYears: number;
  hospitalAffiliation: string;
  areasOfFocus: string[];
  languages: string[];
  consultationFee: number;
  availableDays: string;
  clinicTimings: string;
  inClinicAvailable: boolean;
  onlineAvailable: boolean;
  rating?: number;
  reviewCount?: number;
  consultationStatus: string;
  avatarInitials: string;
  bio: string;
  clinicalApproach: string;
  educationAndCredentials: string[];
  publishedWorks: string[];
}

export const CLINICAL_TEAM: DoctorProfile[] = [
  {
    id: "dr-irfan-ashraf",
    name: "Hakeem Dr. Irfan Ashraf",
    salutation: "Hakeem Dr.",
    designation: "Founder, Chairman & Chief Medical Architect",
    degrees: "BUMS (Unani, AKTC AMU)",
    regNumber: "Official State Board Registration (Updating)",
    experienceYears: 18,
    hospitalAffiliation: "ZAYVORA Matab™ Central Care Centre",
    areasOfFocus: [
      "Musculoskeletal Disorders (Waja-ul-Mafasil)",
      "Male Infertility & Andrology",
      "Classical 10-Ajnas Pulse (Nabz) Diagnostics",
      "Complex Chronic Humoral Dyscrasias"
    ],
    languages: ["English", "Urdu", "Hindi"],
    consultationFee: 1200,
    availableDays: "Monday to Friday",
    clinicTimings: "09:30 AM – 02:00 PM IST",
    inClinicAvailable: true,
    onlineAvailable: true,
    consultationStatus: "Accepting Consultations",
    avatarInitials: "IA",
    bio: "Hakeem Dr. Irfan Ashraf is the Founder and Chief Medical Architect of ZAYVORA Health. A graduate of the historic Ajmal Khan Tibbiya College, Aligarh Muslim University, Dr. Ashraf integrates classical pulse evaluation with modern synovial and metabolic diagnostics to formulate individualized clinical management and stabilization protocols.",
    clinicalApproach: "My practice is anchored in the restoration of the patient's innate healing faculty (Tabi'at). Before any medicine is prescribed, we must identify the root humoral disturbance (Su-e-Mizaj) and correct dietary infractions (Parhez). Therapeutics are applied sequentially through the classical 4-stage Afaal cascade.",
    educationAndCredentials: [
      "Bachelor of Unani Medicine & Surgery (BUMS) — Ajmal Khan Tibbiya College, Aligarh Muslim University (Batch 2002 — Passed 2007)",
      "Registered Unani Medical Practitioner (RUMP)",
      "Founder & Chief Medical Architect, ZAYVORA Health OS"
    ],
    publishedWorks: [
      "Clinical Efficacy of Colchicum luteum (Mudabbar) in Osteoarthritis: A Randomized Controlled Trial (2023)",
      "Longitudinal Evaluation of 10-Ajnas Nabz Waveform Profiles in Metabolic Syndromes (2021)",
      "Safety and Standardization of Schedule E(1) Classical Formulations (2024)"
    ]
  },
  {
    id: "dr-tariq-mansoor",
    name: "Prof. Dr. Tariq Mansoor",
    salutation: "Prof. Dr.",
    designation: "Senior Consultant Tabeeb & Integrative Medicine Director",
    degrees: "BUMS, MD (Kulliyat), NCISM Certified",
    regNumber: "NCISM-BUMS-2008-0881",
    experienceYears: 18,
    hospitalAffiliation: "ZAYVORA Matab™ Central Care Centre",
    areasOfFocus: [
      "Metabolic Syndrome & Insulin Resistance",
      "Hepatic Axis & Fatty Liver Support (Su-e-Mizaj Kabid)",
      "Preventive Lifestyle Medicine (Asbab-e-Sittah)",
      "Integrative Digital Telehealth Care"
    ],
    languages: ["English", "Hindi", "Urdu"],
    consultationFee: 950,
    availableDays: "Monday to Saturday",
    clinicTimings: "11:00 AM – 05:00 PM IST",
    inClinicAvailable: true,
    onlineAvailable: true,
    consultationStatus: "Accepting Consultations",
    avatarInitials: "TM",
    bio: "Prof. Dr. Tariq Mansoor directs clinical informatics and integrative care pathways at ZAYVORA Health. He is dedicated to making authentic Unani medicine accessible, measurable, and continuous through structured clinical models and biomarker-correlated care plans.",
    clinicalApproach: "We bridge ancient constitutional temperaments with contemporary molecular omics. By tracking gut-liver cross-talk and sleep architecture, we help patients resolve metabolic stagnation and stabilize humoral balance before permanent organ damage ensues.",
    educationAndCredentials: [
      "BUMS — Faculty of Medicine (Unani), Premier Statutory University, New Delhi",
      "MD (Kulliyat - Principles of Medicine) — Aligarh Muslim University (AMU)",
      "Fellow, Academy of Integrative Health & Medicine (AIHM)",
      "Certified Clinical Scribe & Telemedicine Specialist"
    ],
    publishedWorks: [
      "Biomarker Signatures of Su-e-Mizaj Barid in Type 2 Diabetes (2022)",
      "Impact of Circadian Dietetics (Ilaj bil-Ghiza) on Non-Alcoholic Fatty Liver (2024)"
    ]
  },
  {
    id: "dr-fatima-zahra",
    name: "Dr. Fatima Zahra",
    salutation: "Dr.",
    designation: "Consultant Physician & Women's Health Specialist",
    degrees: "BUMS, MS (Ilmul Qabalat wa Amraz-e-Niswan)",
    regNumber: "NCISM-BUMS-2015-4421",
    experienceYears: 12,
    hospitalAffiliation: "ZAYVORA Matab™ Central Care Centre",
    areasOfFocus: [
      "PCOS & Anovulatory Cycle Management",
      "Female Pelvic Congestion & Dysmenorrhea",
      "Post-Partum Rejuvenation (Nafas Care)",
      "Hormonal Acne & Hirsutism Support"
    ],
    languages: ["English", "Hindi", "Urdu"],
    consultationFee: 900,
    availableDays: "Tuesday, Thursday, Saturday",
    clinicTimings: "10:00 AM – 03:00 PM IST",
    inClinicAvailable: true,
    onlineAvailable: true,
    consultationStatus: "Accepting Consultations",
    avatarInitials: "FZ",
    bio: "Dr. Fatima Zahra is an empathetic and rigorous women's health specialist. She combines classical pelvic fomentation (Abzen) and uterine herbal tonics with modern ultrasound monitoring to guide women through natural hormonal restoration without synthetic hormone side effects.",
    clinicalApproach: "Female physiology requires compassionate listening and phase-synchronized nutrition. We address pelvic circulation and liver hormone detoxification simultaneously to restore natural rhythmic ovulation.",
    educationAndCredentials: [
      "BUMS — Government Nizamia Tibbi College, Hyderabad",
      "MS (Obstetrics & Gynecology in Unani Medicine) — NIUM Bangalore",
      "Advanced Certification in Reproductive Ultrasonography"
    ],
    publishedWorks: [
      "Evaluation of Saraca asoca and Aloe barbadensis in Oligomenorrhea (2023)",
      "Integrative Dietary Interventions for Hyperandrogenism in PCOS (2025)"
    ]
  },
  {
    id: "dr-zainab-husseini",
    name: "Dr. Zainab Al-Husseini",
    salutation: "Dr.",
    designation: "Senior Research Clinician & Pharmacognosy Lead",
    degrees: "BUMS, PhD (Ilmul Advia - Pharmacology)",
    regNumber: "NCISM-BUMS-2013-1890",
    experienceYears: 14,
    hospitalAffiliation: "ZAYVORA Matab™ Central Care Centre",
    areasOfFocus: [
      "Gut-Brain Axis & Nervous Dyspepsia (Zoaf-e-Meda)",
      "Heavy Metal Purification Verification (Mudabbar Protocols)",
      "Pharmacopoeial Quality Assurance & HPLC Assays",
      "Irritable Bowel Syndrome (IBS) Protocols"
    ],
    languages: ["English", "Arabic", "Urdu"],
    consultationFee: 1000,
    availableDays: "Monday, Wednesday, Friday",
    clinicTimings: "01:00 PM – 06:00 PM IST",
    inClinicAvailable: true,
    onlineAvailable: true,
    consultationStatus: "Accepting Consultations",
    avatarInitials: "ZH",
    bio: "Dr. Zainab Al-Husseini oversees formulation quality, botanical standardization, and gastrointestinal care pathways. She works closely with analytical testing laboratories to ensure every herbal formulation is free of adulterants and compliant with international safety standards.",
    clinicalApproach: "The gut is the primary gatekeeper of human vitality. When digestion is restored and mucosal inflammation calmed, systemic recovery accelerates naturally.",
    educationAndCredentials: [
      "BUMS — Faculty of Medicine (Unani), Statutory Ayurvedic & Unani Medical College",
      "PhD in Ilmul Advia (Unani Pharmacology) — Central Research Institute, New Delhi",
      "Lead Auditor, Good Manufacturing Practices (GMP) for AYUSH Formulations"
    ],
    publishedWorks: [
      "Analytical Validation of Mudabbar Detoxification in Colchicum and Nux-vomica (2022)",
      "Microbiome Modulation by Kasni and Chicoric Acid Derivatives (2024)"
    ]
  }
];
