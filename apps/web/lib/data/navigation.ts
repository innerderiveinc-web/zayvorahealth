import { NavigationItem } from "./types";

export const headerNavigation: NavigationItem[] = [
  {
    label: "Home",
    href: "/"
  },
  {
    label: "About Us",
    href: "/about"
  },
  {
    label: "Services",
    href: "/services",
    dropdown: [
      {
        title: "Clinical Care",
        description: "10-Ajnas Mizaj diagnostics & individualized Unani Matab care plans.",
        href: "/services/clinical-care",
        icon: "🩺",
        badge: "Core Matab"
      },
      {
        title: "AI Healthcare",
        description: "Hakeem Sahab AI™ clinician copilot with evidence verification.",
        href: "/services/ai-healthcare",
        icon: "🧠",
        badge: "AI Copilot"
      },
      {
        title: "Digital Health",
        description: "Comprehensive EHR, patient timelines, and digital twin trajectories.",
        href: "/services/digital-health",
        icon: "💻"
      },
      {
        title: "Research",
        description: "Real-world evidence (RWE), cohort analytics, and clinical research cloud.",
        href: "/services/research",
        icon: "🔬"
      },
      {
        title: "Pharmacy",
        description: "FEFO dispensing, botanical batch tracking, and Schedule E(1) Mudabbar gates.",
        href: "/services/pharmacy",
        icon: "💊"
      },
      {
        title: "Manufacturing",
        description: "AYUSH-GMP compliant cleanroom formulation OS and 21 CFR Part 11 eBMR.",
        href: "/services/manufacturing",
        icon: "⚙️"
      },
      {
        title: "Healthcare Communication",
        description: "Secure telemedicine, QSURA omnichannel alerts, and encrypted messaging.",
        href: "/services/healthcare-communication",
        icon: "📡"
      }
    ]
  },
  {
    label: "Care Programs",
    href: "/programs"
  },
  {
    label: "Doctors",
    href: "/doctors"
  },
  {
    label: "Research",
    href: "/research",
    dropdown: [
      {
        title: "Clinical Research",
        description: "Multi-center clinical trials, IRB protocols, and concordance analytics.",
        href: "/research/clinical-research",
        icon: "📊"
      },
      {
        title: "Evidence",
        description: "Biomedical evidence engine, literature grading, and pharmacovigilance.",
        href: "/research/evidence",
        icon: "📑"
      },
      {
        title: "Knowledge Intelligence",
        description: "Governed classical Unani knowledge graph and hybrid RAG semantic search.",
        href: "/research/knowledge-intelligence",
        icon: "🌐"
      }
    ]
  },
  {
    label: "Knowledge Centre",
    href: "/knowledge-centre"
  },
  {
    label: "Products",
    href: "/products",
    dropdown: [
      {
        title: "Unani Care",
        description: "Classical single (Mufradat) and compound (Murakkabat) botanical formulations.",
        href: "/products/unani-care",
        icon: "🌿",
        badge: "Classical"
      },
      {
        title: "Herbal Products",
        description: "Standardized active botanical extracts and customized herbal compounds.",
        href: "/products/herbal-products",
        icon: "🌱"
      },
      {
        title: "Nutraceuticals",
        description: "Evidence-graded functional botanical tonics and metabolic support.",
        href: "/products/nutraceuticals",
        icon: "✨"
      }
    ]
  },
  {
    label: "Contact",
    href: "/contact"
  }
];

export const footerNavigation = {
  company: [
    { label: "About ZAYVORA", href: "/about" },
    { label: "Clinical Team", href: "/doctors" },
    { label: "Careers", href: "/careers" },
    { label: "Contact Us", href: "/contact" }
  ],
  services: [
    { label: "Clinical Care", href: "/services/clinical-care" },
    { label: "AI Healthcare", href: "/services/ai-healthcare" },
    { label: "Digital Health", href: "/services/digital-health" },
    { label: "Clinical Research", href: "/services/research" },
    { label: "Pharmacy & Dispensary", href: "/services/pharmacy" },
    { label: "Manufacturing OS", href: "/services/manufacturing" },
    { label: "Teleconsultation", href: "/telemedicine" }
  ],
  programs: [
    { label: "All Care Programs", href: "/programs" },
    { label: "Male Fertility (74-Day)", href: "/programs" },
    { label: "Female Hormonal Balance", href: "/programs" },
    { label: "Gut & IBS Restoration", href: "/programs" },
    { label: "Metabolic & Liver Support", href: "/programs" }
  ],
  products: [
    { label: "Unani Care", href: "/products/unani-care" },
    { label: "Herbal Products", href: "/products/herbal-products" },
    { label: "Nutraceuticals", href: "/products/nutraceuticals" }
  ],
  resources: [
    { label: "FAQ", href: "/faq" },
    { label: "Knowledge Centre", href: "/knowledge-centre" },
    { label: "Clinical Research", href: "/research/clinical-research" },
    { label: "Evidence Engine", href: "/research/evidence" }
  ],
  legal: [
    { label: "Privacy Policy", href: "/privacy-policy" },
    { label: "Terms & Conditions", href: "/terms-and-conditions" },
    { label: "Medical Disclaimer", href: "/medical-disclaimer" },
    { label: "Shipping & Refund Policy", href: "/shipping-refunds" },
    { label: "Accessibility", href: "/accessibility" }
  ]
};

