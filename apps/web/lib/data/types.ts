export interface SiteConfig {
  name: string;
  platformName: string;
  tagline: string;
  description: string;
  logo: string;
  favicon: string;
  address: {
    facility: string;
    wing: string;
    street: string;
    city: string;
    state: string;
    postalCode: string;
    country: string;
  };
  contact: {
    helpline: string;
    opdPhone: string;
    email: string;
    supportEmail: string;
    pressEmail: string;
  };
  socialLinks: {
    platform: string;
    url: string;
  }[];
  legalLinks: {
    label: string;
    href: string;
  }[];
  primaryCta: {
    label: string;
    href: string;
  };
  secondaryCta: {
    label: string;
    href: string;
  };
  medicalDisclaimer: string;
  copyright: string;
}

export interface NavigationDropdownItem {
  title: string;
  description: string;
  href: string;
  badge?: string;
  icon?: string;
}

export interface NavigationItem {
  label: string;
  href: string;
  dropdown?: NavigationDropdownItem[];
}

export interface ServiceItem {
  id: string;
  name: string;
  slug: string;
  shortDescription: string;
  fullDescription: string;
  problemSolved: string;
  capabilities: string[];
  userGroups: string[];
  workflow: string[];
  safetyConsiderations?: string;
  relatedModules: string[];
  relatedServices: { name: string; href: string }[];
  ctaLabel: string;
  ctaHref: string;
  icon: string;
  badge?: string;
}

export interface ProductItem {
  id: string;
  name: string;
  category: "unani-care" | "herbal-products" | "nutraceuticals";
  categoryLabel: string;
  tagline: string;
  description: string;
  intendedUse: string;
  keyIngredients: string[];
  dosageGuidelines: string;
  qualityStandards: string[];
  safetyNotes: string;
  regulatoryPositioning: string;
  availabilityStatus: "Available" | "Under Clinical Review" | "Coming Soon" | "Authorized Clinics Only";
  price?: string;
  volume?: string;
  badge?: string;
}

export interface ResearchItem {
  id: string;
  title: string;
  category: "clinical-research" | "evidence" | "knowledge-intelligence";
  categoryLabel: string;
  summary: string;
  methodology: string;
  significance: string;
  evidenceGrade: "Grade A" | "Grade B" | "Grade C" | "Observational / RWE";
  leadInvestigator?: string;
  status: "Active Trial" | "Published Cohort" | "Continuous Surveillance" | "Peer Review";
  href: string;
}

export interface TeamMember {
  id: string;
  name: string;
  role: string;
  division: "Clinical" | "Research" | "Informatics & AI" | "Operations";
  degrees: string;
  bio: string;
  specialization: string[];
  experience: string;
}

export interface FaqItem {
  id: string;
  category: "General" | "Clinical Care" | "AI & Technology" | "Products" | "Research & Safety";
  question: string;
  answer: string;
}

export interface LegalPageData {
  title: string;
  lastUpdated: string;
  version: string;
  sections: {
    heading: string;
    content: string[];
  }[];
}
