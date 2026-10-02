/**
 * ZAYVORA Health™ — Institutional Navigation Architecture
 *
 * Conforming strictly to institutional healthcare standard:
 * 5 authoritative primary pillars with clear clinical pathways.
 * Zero text emojis; uses semantic SVG icon keys.
 */

export interface NavSubItem {
  title: string;
  description: string;
  href: string;
  iconKey: "stethoscope" | "clipboard" | "heart" | "video" | "users" | "hospital" | "pill" | "leaf" | "flask" | "shield" | "book" | "library" | "scale" | "academic" | "building" | "phone";
  badge?: string;
}

export interface NavMainItem {
  label: string;
  href: string;
  dropdown?: NavSubItem[];
}

export const INSTITUTIONAL_HEADER_NAVIGATION: NavMainItem[] = [
  {
    label: "Care",
    href: "/services/clinical-care",
    dropdown: [
      {
        title: "Clinical Care",
        description: "Comprehensive history, constitutional assessment, and personalized care planning.",
        href: "/services/clinical-care",
        iconKey: "stethoscope",
        badge: "Core Service"
      },
      {
        title: "Care Programs",
        description: "Structured clinician-guided programs for metabolic, digestive, and musculoskeletal care.",
        href: "/programs",
        iconKey: "clipboard"
      },
      {
        title: "Health Conditions",
        description: "Clinical information and care options for common persistent health complaints.",
        href: "/conditions",
        iconKey: "heart"
      },
      {
        title: "Virtual Consultation",
        description: "Encrypted video consultations with certified Unani physicians.",
        href: "/teleconsultation",
        iconKey: "video"
      }
    ]
  },
  {
    label: "ZAYVORA Matab",
    href: "/doctors",
    dropdown: [
      {
        title: "Specialists & Clinicians",
        description: "Meet board-certified Unani physicians registered under the NCISM Act 2020.",
        href: "/doctors",
        iconKey: "users"
      },
      {
        title: "Care Centers & Matabs",
        description: "Explore our in-person clinical facilities and specialized regimenal suites.",
        href: "/clinics",
        iconKey: "hospital"
      }
    ]
  },
  {
    label: "Health Products",
    href: "/products",
    dropdown: [
      {
        title: "Classical Unani Formulations",
        description: "Standardized pharmacopoeial preparations (Majun, Jawarish, Kushta, Roghan).",
        href: "/products/unani-care",
        iconKey: "pill"
      },
      {
        title: "Herbal Products",
        description: "Active botanical single-ingredient and compound formulations.",
        href: "/products/herbal-products",
        iconKey: "leaf"
      },
      {
        title: "Botanical Nutraceuticals",
        description: "Nutritional supplements developed according to traditional humoral principles.",
        href: "/products/nutraceuticals",
        iconKey: "flask"
      },
      {
        title: "Product Quality & Safety",
        description: "GMP standards, testing protocols, and Schedule E(1) purification procedures.",
        href: "/products/safety",
        iconKey: "shield"
      }
    ]
  },
  {
    label: "Knowledge",
    href: "/health-library",
    dropdown: [
      {
        title: "Grand Integrative Medical Library",
        description: "Authoritative 12-Volume encyclopedia spanning Classical Tibb, Modern Biomarkers, Radio-Diagnostics, and Epigenetics.",
        href: "/library",
        iconKey: "library",
        badge: "12 Volumes"
      },
      {
        title: "Health Library",
        description: "Clinician-reviewed medical guidance conforming to NHS Digital editorial standards.",
        href: "/health-library",
        iconKey: "library",
        badge: "Verified"
      },
      {
        title: "Unani Medicine Foundations",
        description: "Educational guide to Mizaj, Asbab-e-Sitta, and humoral physiology.",
        href: "/modern-unani",
        iconKey: "book"
      },
      {
        title: "Evidence & Research Dossiers",
        description: "Transparent grading of clinical trials, observational data, and limitations.",
        href: "/research/evidence",
        iconKey: "scale"
      },
      {
        title: "Clinical Academy",
        description: "Professional continuing education and post-graduate fellowship resources.",
        href: "/academy",
        iconKey: "academic"
      }
    ]
  },
  {
    label: "About",
    href: "/about",
    dropdown: [
      {
        title: "About ZAYVORA",
        description: "Our organizational mission, leadership, and clinical philosophy.",
        href: "/about",
        iconKey: "building"
      },
      {
        title: "Trust & Safety Centre",
        description: "Unified governance, patient rights, safety standards, and DPDP privacy.",
        href: "/trust",
        iconKey: "shield",
        badge: "Charter"
      },
      {
        title: "Clinical Governance",
        description: "Physician oversight standards, ethical bounds, and safety firewalls.",
        href: "/clinical-governance",
        iconKey: "shield"
      },
      {
        title: "Contact & Assistance",
        description: "Care helpline, clinic directions, and institutional inquiries.",
        href: "/contact",
        iconKey: "phone"
      }
    ]
  }
];

export const INSTITUTIONAL_FOOTER_NAVIGATION = {
  care: [
    { label: "Clinical Care", href: "/services/clinical-care" },
    { label: "Care Programs", href: "/programs" },
    { label: "Virtual Consultation", href: "/teleconsultation" },
    { label: "Our Clinicians", href: "/doctors" },
    { label: "Matab Facilities", href: "/clinics" }
  ],
  health: [
    { label: "Health Conditions", href: "/conditions" },
    { label: "Health Library", href: "/health-library" },
    { label: "My ZAYVORA™ Patient Portal", href: "/patient" },
    { label: "Medicines & Products", href: "/products" },
    { label: "Product Safety Standards", href: "/products/safety" }
  ],
  research: [
    { label: "Clinical Evidence Dossiers", href: "/research/evidence" },
    { label: "Observational Cohorts (RWE)", href: "/research/clinical-research" },
    { label: "Knowledge Intelligence", href: "/research/knowledge-intelligence" },
    { label: "Clinical Academy", href: "/academy" }
  ],
  about: [
    { label: "About ZAYVORA Health", href: "/about" },
    { label: "Trust & Safety Centre", href: "/trust" },
    { label: "Clinical Governance", href: "/clinical-governance" },
    { label: "AI Transparency", href: "/ai-transparency" },
    { label: "Contact Us", href: "/contact" }
  ],
  patientInfo: [
    { label: "Trust & Safety", href: "/trust" },
    { label: "Medical Disclaimer", href: "/medical-disclaimer" },
    { label: "Privacy Policy (DPDP Act)", href: "/privacy-policy" },
    { label: "Terms of Service", href: "/terms" },
    { label: "Patient Rights & Consents", href: "/patient-rights" },
    { label: "Accessibility Statement", href: "/accessibility" },
    { label: "Grievance Redressal", href: "/grievance" }
  ]
};
