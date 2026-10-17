import { ServiceItem } from "./types";

export const servicesData: ServiceItem[] = [
  {
    id: "clinical-care",
    name: "Clinical Care",
    slug: "clinical-care",
    shortDescription: "Individualized Unani Matab care combining 10-Ajnas constitutional assessment with organ-axis clinical mapping.",
    fullDescription: "ZAYVORA Matab™ delivers patient-centered, clinician-governed healthcare. Attending Hakeems leverage our integrated diagnostic workbench to assess constitutional Mizaj across 10 classical axes (Nabz, Baul, Baraz, etc.), cross-examine biomedical lab panels, and formulate holistic therapeutic regimens.",
    problemSolved: "Eliminates fragmented, trial-and-error treatments by anchoring clinical decisions in constitutional Mizaj etiology combined with organ-axis cross-talk analysis.",
    capabilities: [
      "10-Ajnas Constitutional Mizaj evaluation & dynamic scoring",
      "6-Vector Organ-Axis radar (Brain, Heart, Liver, Kidney, Gut, Immune)",
      "Longitudinal Patient 360 timeline & digital twin trajectory simulation",
      "Ilaj bil-Tadbeer (regimenal therapy) and Ilaj bil-Ghiza (dietary therapy) planning",
      "21 CFR Part 11 cryptographic encounter sealing with SHA-256 HMAC digital signatures"
    ],
    userGroups: ["Attending Tabeebs / Doctors", "Clinical Fellows", "OPD Nurses", "Care Coordinators"],
    workflow: [
      "Patient check-in & vital signs capture",
      "10-Ajnas Mizaj examination & symptomatic intake",
      "Organ-Axis imbalance mapping & differential analysis",
      "Individualized Nuskha formulation & regimen configuration",
      "Clinician electronic review & cryptographic prescription signature"
    ],
    safetyConsiderations: "All therapeutic recommendations are subject to clinician verification; emergency red-flag symptoms immediately trigger acute hospital referral protocols.",
    relatedModules: ["Mizaj Diagnostics", "Organ-Axis Radar", "Nuskha Compiler", "21 CFR Part 11 Signatures"],
    relatedServices: [
      { name: "AI Healthcare", href: "/services/ai-healthcare" },
      { name: "Pharmacy & Dispensary", href: "/services/pharmacy" }
    ],
    ctaLabel: "Consult a Tabeeb",
    ctaHref: "/contact",
    icon: "🩺",
    badge: "Core Matab Care"
  },
  {
    id: "ai-healthcare",
    name: "AI Healthcare",
    slug: "ai-healthcare",
    shortDescription: "Hakeem Sahab AI™ clinical copilot providing evidence-graded decision support with strict safety guardrails.",
    fullDescription: "Hakeem Sahab AI™ operates strictly as a clinician copilot, synthesising classical Unani pharmacopoeia with modern PubMed/Medline evidence. Designed with zero autonomous prescribing capability, every suggestion enforces safe_to_lock=False until reviewed and sealed by a human clinician.",
    problemSolved: "Synthesizes thousands of classical formulation manuscripts and modern pharmacological interactions into real-time, evidence-cited clinical advisories at the point of care.",
    capabilities: [
      "Hybrid dense-vector & Neo4j knowledge graph RAG retrieval",
      "Real-time Schedule E(1) toxic herb Mudabbar detoxification checking",
      "Drug-herb interaction & contraindication screening",
      "Structured clinical rationale with classical and modern citations",
      "Zero-hallucination safety firewall with multi-layer prompt defense"
    ],
    userGroups: ["Senior Hakeems", "Consultant Physicians", "Clinical Pharmacists", "Research Scholars"],
    workflow: [
      "Clinician queries patient presentation or differential diagnostic dilemma",
      "Hybrid RAG retrieves validated Unani texts and biomedical evidence",
      "Safety firewall screens for posology limits and contraindicated substances",
      "Advisory presented in structured drawer with confidence scores and citations",
      "Clinician accepts, modifies, or rejects advisory prior to prescription lock"
    ],
    safetyConsiderations: "Hakeem Sahab AI™ never independently diagnoses, prescribes, or signs prescriptions. All recommendations carry safe_to_lock=False.",
    relatedModules: ["Hakeem Sahab Engine", "Safety Firewall", "Hybrid RAG", "Knowledge Graph"],
    relatedServices: [
      { name: "Clinical Care", href: "/services/clinical-care" },
      { name: "Knowledge Intelligence", href: "/research/knowledge-intelligence" }
    ],
    ctaLabel: "Explore AI Safety Governance",
    ctaHref: "/research/knowledge-intelligence",
    icon: "🧠",
    badge: "Clinician Copilot"
  },
  {
    id: "digital-health",
    name: "Digital Health",
    slug: "digital-health",
    shortDescription: "Enterprise EHR, patient health records, longitudinal timelines, and ABDM/FHIR R4 interoperability.",
    fullDescription: "ZAYVORA Health OS™ provides an interoperable digital infrastructure engineered for healthcare networks. Featuring longitudinal health timelines, digital twin symptom trajectory tracking, and native ABDM/FHIR R4 connectors, patient records flow securely across clinical, laboratory, and pharmacy touchpoints.",
    problemSolved: "Bridges the gap between traditional holistic clinical observations and modern electronic health data standards without data loss.",
    capabilities: [
      "FHIR R4 Observation, Condition, and MedicationRequest normalization",
      "ABDM ABHA integration architecture for health ID linkage",
      "Longitudinal Patient 360 view with multi-visit symptom trajectory modeling",
      "Role-based access control (RBAC) across 7 discrete clinical & administrative tiers",
      "Automated disaster recovery backups and immutable cryptographic audit logging"
    ],
    userGroups: ["Clinic Administrators", "Medical Records Officers", "Chief Medical Officers", "Patients"],
    workflow: [
      "Patient demographic and ABHA record registration",
      "Continuous health data capture across clinical encounters",
      "Automated FHIR bundle generation and secure cloud sync",
      "Longitudinal health trend visualization for patient and clinician"
    ],
    safetyConsiderations: "Data is encrypted in transit (TLS 1.3) and at rest (AES-256) with strict organization and clinic-level multi-tenant isolation.",
    relatedModules: ["ABDM/FHIR Client", "Patient 360", "Audit Ledger", "Tenancy Manager"],
    relatedServices: [
      { name: "Clinical Care", href: "/services/clinical-care" },
      { name: "Healthcare Communication", href: "/services/healthcare-communication" }
    ],
    ctaLabel: "View Platform Architecture",
    ctaHref: "/about",
    icon: "💻"
  },
  {
    id: "research",
    name: "Research & Evidence Cloud",
    slug: "research",
    shortDescription: "De-identified clinical research cloud, cohort analytics, and real-world evidence (RWE) generation.",
    fullDescription: "The ZAYVORA Research Cloud empowers clinical investigators and academic institutions to generate rigorous real-world evidence on Unani therapeutics. Utilizing automated cohort extraction, validated PROM/PREM scoring, and adverse event surveillance, our platform bridges ancient empirical knowledge with clinical trials.",
    problemSolved: "Solves the empirical validation challenge in traditional medicine by providing standardized, GCP-compliant trial data capture and real-world outcome analytics.",
    capabilities: [
      "De-identified clinical cohort analytics with differential filtering",
      "Real-World Evidence (RWE) outcome tracking & symptom resolution curves",
      "Institutional Review Board (IRB) trial protocol registry & tracking",
      "Automated pharmacovigilance and adverse drug reaction (ADR) detection",
      "Biomedical literature concordance analysis and evidence grading"
    ],
    userGroups: ["Clinical Trial Investigators", "Epidemiologists", "Academic Faculty", "Pharmacovigilance Officers"],
    workflow: [
      "Study protocol registration and cohort inclusion criteria configuration",
      "Anonymized clinical outcome and biomarker aggregation",
      "Concordance and efficacy statistical modeling",
      "Publication-grade trial reporting and regulatory dossier generation"
    ],
    safetyConsiderations: "All research cohorts strictly utilize de-identified data complying with clinical trial governance and data protection frameworks.",
    relatedModules: ["Research Cloud", "RWE Engine", "Pharmacovigilance", "Evidence Registry"],
    relatedServices: [
      { name: "Clinical Research", href: "/research/clinical-research" },
      { name: "Evidence Engine", href: "/research/evidence" }
    ],
    ctaLabel: "Explore Research Studies",
    ctaHref: "/research",
    icon: "🔬"
  },
  {
    id: "pharmacy",
    name: "Pharmacy & Dispensary OS",
    slug: "pharmacy",
    shortDescription: "First-Expired-First-Out (FEFO) dispensing, batch traceability, and Schedule E(1) detoxification safety controls.",
    fullDescription: "ZAYVORA Dispensary OS transforms botanical pharmacy operations with pharmaceutical-grade safety controls. Prescriptions flow directly from clinician encounter locks to dispensary queues, where pharmacists verify active batch numbers, expiry dates, and Mudabbar processing certificates prior to dispensing.",
    problemSolved: "Prevents dispensing errors, halts expired or degraded botanical medicines, and enforces verification for restricted traditional formulations.",
    capabilities: [
      "First-Expired-First-Out (FEFO) automated stock batch allocation",
      "Schedule E(1) Mudabbar detoxification certificate enforcement gate",
      "Real-time pharmacy inventory tracking and automated reorder alerts",
      "Automated dosage, anupan (vehicle), and parhez (dietary restrictions) label printing",
      "Cryptographic dispensing verification linked to patient encounter ledger"
    ],
    userGroups: ["Chief Pharmacists", "Dispensary Staff", "Store Incharges", "Quality Controllers"],
    workflow: [
      "Electronic prescription reception from signed clinician encounter",
      "Batch selection according to FEFO algorithm and expiry limits",
      "Verification of Mudabbar certificate for restricted botanicals",
      "Physical dispensing, patient counseling, and cryptographic record lock"
    ],
    safetyConsiderations: "Dispensary software automatically blocks dispensing if a batch is expired or if required Mudabbar certification is missing.",
    relatedModules: ["FEFO Dispensary", "Batch Tracker", "Schedule E1 Gate", "Inventory Manager"],
    relatedServices: [
      { name: "Manufacturing OS", href: "/services/manufacturing" },
      { name: "Unani Care Products", href: "/products/unani-care" }
    ],
    ctaLabel: "Review Dispensary Standards",
    ctaHref: "/products",
    icon: "💊"
  },
  {
    id: "manufacturing",
    name: "Manufacturing & Formulation OS",
    slug: "manufacturing",
    shortDescription: "AYUSH-GMP compliant formulation management, cleanroom IoT telemetry, and 21 CFR Part 11 eBMR.",
    fullDescription: "Engineered for high-integrity botanical processing, ZAYVORA Research & Manufacturing™ Cleanroom OS digitizes master formula records, raw material botanical verification, cleanroom environmental monitoring (temperature, humidity, differential pressure), and automated Certificate of Analysis (CoA) generation.",
    problemSolved: "Eliminates batch variation, contamination risks, and documentation lapses in traditional herbal and Unani pharmaceutical manufacturing.",
    capabilities: [
      "Electronic Batch Manufacturing Records (eBMR) with step-by-step signoffs",
      "Botanical raw material pharmacopoeial authentication & supplier tracking",
      "Cleanroom IoT sensor integration (temperature, RH, particle count telemetry)",
      "In-process Quality Control (IPQC) checkpoints and stability testing logs",
      "Digital Certificate of Analysis (CoA) generation with release authority signoff"
    ],
    userGroups: ["Plant Managers", "Production Chemists", "Quality Assurance Heads", "Regulatory Auditors"],
    workflow: [
      "Master formula selection and raw material lot allocation",
      "Cleanroom preparation and environmental parameter verification",
      "Stepwise execution with dual operator and QA signoff",
      "Finished goods testing, stability verification, and formal release approval"
    ],
    safetyConsiderations: "Batches cannot be released for clinical dispensing without passing QA microbiological, heavy metal, and potency thresholds.",
    relatedModules: ["Manufacturing OS", "eBMR Engine", "QC Inspector", "Cleanroom Telemetry"],
    relatedServices: [
      { name: "Pharmacy OS", href: "/services/pharmacy" },
      { name: "Herbal Products", href: "/products/herbal-products" }
    ],
    ctaLabel: "Discover Manufacturing Standards",
    ctaHref: "/contact",
    icon: "⚙️"
  },
  {
    id: "healthcare-communication",
    name: "Healthcare Communication",
    slug: "healthcare-communication",
    shortDescription: "Encrypted teleconsultation, patient portal communications, and QSURA omnichannel care notifications.",
    fullDescription: "ZAYVORA Healthcare Communication connects patients, care coordinators, and tabeebs across encrypted digital touchpoints. Utilizing the QSURA communications layer, patients receive timely appointment confirmations, dosage reminders, lifestyle adherence nudges, and secure teleconsultation links.",
    problemSolved: "Reduces patient no-shows, enhances treatment adherence, and provides secure remote clinical consultations for distance patients.",
    capabilities: [
      "End-to-end encrypted video teleconsultation room with shared clinical notes",
      "QSURA omnichannel messaging (SMS, Email, Push Notifications)",
      "Automated appointment booking confirmations & token status notifications",
      "Medication adherence nudges with customized anupan instructions",
      "Secure patient-doctor asynchronous messaging with care team escalation"
    ],
    userGroups: ["Tele-Tabeebs", "Care Coordinators", "Front Desk Receptionists", "Patients & Caregivers"],
    workflow: [
      "Appointment booking triggers automated confirmation via SMS/Email",
      "Day-of consultation reminder with live virtual waiting room link",
      "Secure video encounter conducted directly inside clinician workbench",
      "Post-consultation prescription and follow-up guidance delivered to patient app"
    ],
    safetyConsiderations: "All communications maintain strict DPDP Act 2023 and ABDM privacy guardrails; sensitive diagnostic reports require authenticated portal login.",
    relatedModules: ["QSURA Engine", "TeleConsult Room", "Notification Gateway", "Queue Manager"],
    relatedServices: [
      { name: "Clinical Care", href: "/services/clinical-care" },
      { name: "Digital Health", href: "/services/digital-health" }
    ],
    ctaLabel: "Book a Teleconsultation",
    ctaHref: "/contact",
    icon: "📡"
  }
];
