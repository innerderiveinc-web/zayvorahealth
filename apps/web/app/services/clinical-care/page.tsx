import React from "react";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { ClinicalLandingTemplate, ClinicalSpecialtyData } from "@/components/website/ClinicalLandingTemplate";

export const metadata = {
  title: "Clinical Care & Matab Consultation | ZAYVORA Health™",
  description: "Individualized Unani Matab care combining 10-Ajnas constitutional assessment with organ-axis clinical mapping and 21 CFR Part 11 electronic prescriptions.",
};

const clinicalCareData: ClinicalSpecialtyData = {
  slug: "clinical-care",
  name: "Integrative Clinical Matab & Constitutional Medicine",
  classicalNomenclature: "Tibb-e-Unani Clinical Canon",
  badge: "Primary Outpatient Clinical Service",
  shortSummary: "Individualized Unani Matab care combining classical 10-Ajnas constitutional assessment (Mizaj) with contemporary biomarker mapping, organ-axis surveillance, and clinician-verified electronic prescriptions.",
  fullOverview: `ZAYVORA Matab™ delivers patient-centered, clinician-governed healthcare rooted in the foundational principles of Greco-Arab (Unani) medicine, unified with contemporary diagnostic intelligence.

Rather than merely suppressing isolated peripheral symptoms, our clinical practice evaluates each patient's inherent constitutional temperament (Mizaj-e-Asli) versus their acquired pathological deviation (Su-e-Mizaj). Through rigorous multi-dimensional examination—spanning ten classical clinical criteria (Al-Ajnas al-Ashra), organ-axis cross-talk, and corroborating modern laboratory panels—our attending clinicians formulate targeted, stage-wise therapeutic interventions.

Every consultation adheres to the statutory standards of the National Commission for Indian System of Medicine (NCISM) Act 2020. Prescriptions are cryptographically signed using 21 CFR Part 11 compliant digital signatures, and all dispensed classical botanicals undergo strict Schedule E(1) Mudabbar (pharmaceutical purification) verification.`,
  targetAudience: [
    "Individuals with chronic functional or metabolic disorders unresponsive to mono-target therapies.",
    "Patients presenting with musculoskeletal, digestive, or inflammatory dysfunctions seeking constitutional rebalancing.",
    "Those experiencing fatigue, metabolic syndrome, or psychosomatic imbalances (Ilaj bil Nafsiyat).",
    "Individuals needing structured dietary (Ilaj bil Ghiza) and regimenal (Ilaj bil Tadbeer) guidance alongside clinical care.",
    "Patients seeking physician-governed, non-toxic integrative management with laboratory safety monitoring."
  ],
  symptoms: [
    "Chronic joint stiffness, migratory arthralgia, and cold-predominant muscular aches (Waja al-Mafasil).",
    "Functional gastrointestinal distress, chronic dyspepsia, gastric sluggishness, and altered bowel habits (Zo'f-e-Meda).",
    "Metabolic sluggishness, insulin resistance, unexplained fatigue, and impaired vitality (Zo'f-e-A'za-e-Ra'eesa).",
    "Chronic stress, insomnia, mental fatigue, and autonomic dysregulation (Amraz-e-Nafsaniyah).",
    "Recurrent seasonal allergies, respiratory vulnerability, and immune dysregulation."
  ],
  clinicalApproach: [
    {
      title: "1. 10-Ajnas Pulse & Mizaj Staging",
      description: "Comprehensive physical and constitutional examination evaluating pulse volume, rate, rhythm, skin texture, complexion, and body habitus."
    },
    {
      title: "2. Organ-Axis Cross-Talk Mapping",
      description: "Evaluating interconnected organ systems (Brain-Heart-Liver-Kidney-Gut-Immune) to locate the primary seat of humoral dyscrasia."
    },
    {
      title: "3. Corroborative Laboratory Verification",
      description: "Review of complete blood counts, hepatic and renal panels, metabolic biomarkers, and inflammatory indices to validate clinical impressions."
    },
    {
      title: "4. Individualized Nuskha & Regimen",
      description: "Tailored botanical formulation authoring, dietetics (Ilaj bil Ghiza), and regimenal therapy scheduling, cryptographically signed by the attending Tabeeb."
    }
  ],
  unaniFramework: {
    mizajImpact: "Identifies whether the disease state stems from Barid (Cold), Yabis (Dry), Haar (Hot), or Ratab (Moist) constitutional imbalance.",
    organAxis: "Primary focus on A'za-e-Ra'eesa (Principal Vital Organs: Brain, Heart, Liver) and their functional axes with kidneys, stomach, and nervous system.",
    humoralPathology: "Assesses qualitative or quantitative corruption of the four primary bodily humors: Dam (Blood), Balgham (Phlegm), Safra (Yellow Bile), and Sauda (Black Bile).",
    asbabConsiderations: [
      "Hawa-e-Muheet (Ambient air quality, temperature, and seasonal adaptation)",
      "Makool wa Mashroob (Constitutional dietary intake, digestive timing, and hydration)",
      "Harkat wa Sukoon-e-Badani (Physical movement, muscular exertion, and sedentary load)",
      "Harkat wa Sukoon-e-Nafsani (Emotional equilibrium, stress, anxiety, and mental rest)",
      "Naum wa Yaqza (Sleep-wake architecture and circadian rhythm restoration)",
      "Ehtibas wa Istifragh (Therapeutic retention of essential fluids and elimination of metabolic wastes)"
    ]
  },
  biomedicalCorroboration: {
    biomarkers: [
      "hs-CRP / ESR (Inflammatory status)",
      "HbA1c & Fasting Glucose (Metabolic balance)",
      "Liver Function Tests (ALT, AST, Bilirubin)",
      "Kidney Function Tests (Serum Creatinine, eGFR)",
      "Lipid Profile (Total Cholesterol, Triglycerides, HDL)",
      "Thyroid Stimulating Hormone (TSH)"
    ],
    monitoring: "Routine repeat biomarker tracking at 30, 60, and 90-day intervals to verify biochemical normalization and safety.",
    integrativeSafety: "Automated screening for pharmaceutical-botanical interactions; safe posology thresholds calibrated against standard pharmacopoeias (UPI / NFUM)."
  },
  consultationIncludes: [
    "45-minute comprehensive clinical assessment with an NCISM-registered senior Tabeeb.",
    "Classical 10-Ajnas pulse and constitutional Mizaj diagnosis.",
    "Review and clinical synthesis of prior medical records, lab reports, and imaging.",
    "21 CFR Part 11 compliant digitally signed electronic prescription (Nuskha).",
    "Individualized dietary guideline chart tailored to constitutional temperament.",
    "Regimenal therapy (Ilaj bil-Tadbeer) recommendations (Hijamah, Dalk, Hammam where indicated).",
    "Direct encrypted messaging with your clinical care team via My ZAYVORA™ portal.",
    "Automated laboratory test requisition and follow-up scheduling."
  ],
  redFlagSafety: {
    emergencySymptoms: [
      "Acute, crushing retrosternal chest pain radiating to left arm or jaw.",
      "Sudden unilateral facial drooping, arm weakness, or slurred speech (acute stroke signs).",
      "Severe, abrupt shortness of breath or acute oxygen saturation drop (< 92%).",
      "Massive gastrointestinal bleeding, hematemesis, or acute rigid abdomen.",
      "High unremitting fever accompanied by neck stiffness or altered consciousness."
    ],
    exclusionCriteria: [
      "Acute surgical emergencies requiring immediate operative intervention.",
      "Severe decompensated diabetic ketoacidosis or hyperosmolar hyperglycemic state.",
      "Active oncological crises or acute septic shock.",
      "Unstable cardiac arrhythmias requiring continuous ICU cardiac telemetry."
    ],
    advisory: "ZAYVORA Matab provides specialized ambulatory and chronic disease management. We do not provide acute trauma, intensive care, or emergency room resuscitation services. In severe life-threatening emergencies, patients must immediately proceed to the nearest emergency hospital."
  },
  clinicianTeam: [
    {
      name: "Hakeem Dr. Irfan Ashraf",
      role: "Founder, Chairman & Chief Medical Architect",
      regNumber: "NCISM Reg: BUMS-2004-9841",
      qualification: "BUMS (Gold Medalist), MD (Unani), Specialist in Constitutional Internal Medicine"
    },
    {
      name: "Dr. Aaminah Qureshi",
      role: "Consultant Physician & Metabolic Medicine Lead",
      regNumber: "NCISM Reg: BUMS-2012-4412",
      qualification: "BUMS, MD (Kulliyat wa Ilaj-bil-Adviya), Fellowship in Integrative Endocrinology"
    }
  ],
  faqs: [
    {
      question: "How does a ZAYVORA Matab consultation differ from a standard clinic visit?",
      answer: "A standard clinical consultation often addresses only an isolated presenting symptom with mono-target drugs. At ZAYVORA, our physicians evaluate your constitutional temperament (Mizaj), your dietary-lifestyle stressors (Asbab-e-Sitta), and organ-axis dynamics alongside modern laboratory diagnostics, providing a root-cause, restorative treatment protocol."
    },
    {
      question: "Are your medications safe and tested for toxicity?",
      answer: "Yes. Every botanical formula prescribed at ZAYVORA is sourced from GMP-certified facilities and tested for heavy metals, microbial limits, and pesticide residues. Schedule E(1) botanicals undergo mandatory classical Mudabbar (purification) processes verified by laboratory certificates of analysis before dispensing."
    },
    {
      question: "Can I take ZAYVORA medicines alongside my conventional allopathic prescriptions?",
      answer: "Yes, under physician supervision. Our attending clinicians review all your ongoing medications and use automated drug-herb interaction checks to ensure complete safety, preventing adverse overlaps or metabolic interference."
    },
    {
      question: "What is an electronic prescription seal under 21 CFR Part 11?",
      answer: "It is a legally binding, cryptographic digital seal with dual-factor authentication (PIN and clinician credentials) ensuring that your medical prescription cannot be modified, tampered with, or duplicated once approved by the licensed physician."
    }
  ],
  references: [
    {
      title: "Al-Qanun fi al-Tibb (The Canon of Medicine) — Book 1: General Principles & Mizaj",
      source: "Ibn Sina (Avicenna), Classical Canon",
      type: "classical"
    },
    {
      title: "Kitab al-Kulliyat (General Principles of Medicine)",
      source: "Ibn Rushd (Averroes), Classical Canon",
      type: "classical"
    },
    {
      title: "Unani Pharmacopoeia of India (UPI) — Parts I & II",
      source: "Ministry of AYUSH, Government of India",
      year: "2016",
      type: "contemporary"
    },
    {
      title: "National Commission for Indian System of Medicine (NCISM) Professional Conduct Standards",
      source: "Gazette of India, Extraordinary",
      year: "2020",
      type: "contemporary"
    }
  ],
  governance: {
    author: "Clinical Architecture Board",
    authorRole: "Integrative Internal Medicine Division",
    reviewer: "Hakeem Dr. Irfan Ashraf",
    reviewerRegNumber: "BUMS-2004-9841",
    lastReviewed: "15 September 2026",
    version: "2.4.0",
    nextAuditDue: "15 March 2027"
  }
};

export default function ClinicalCareServicePage() {
  return (
    <PublicWebsiteShell>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <ClinicalLandingTemplate data={clinicalCareData} />
      </div>
    </PublicWebsiteShell>
  );
}
