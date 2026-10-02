import { SiteConfig } from "./types";

export const siteConfig: SiteConfig = {
  name: "ZAYVORA Health™",
  platformName: "ZAYVORA Health OS™",
  tagline: "Ancient Wisdom. Modern Science. Intelligent Care.",
  description: "ZAYVORA Health OS™ is an enterprise-grade, AI-native healthcare operating system integrating classical Unani Medicine, 10-Ajnas Mizaj intelligence, 6-Vector Organ-Axis reasoning, and contemporary biomedical informatics with strict 21 CFR Part 11 and human clinical governance.",
  logo: "/zayvora-logo.png",
  favicon: "/favicon.ico",
  address: {
    facility: "ZAYVORA Healthcare System - Central Hospital",
    wing: "Integrative Clinical Facility & Formulation Cleanroom",
    street: "ZAYVORA Healthcare Complex, Institutional Area",
    city: "New Delhi",
    state: "Delhi",
    postalCode: "110062",
    country: "India"
  },
  contact: {
    helpline: "+91 97738 82657",
    opdPhone: "+91 97738 82657",
    email: "contact@zayvorahealth.com",
    supportEmail: "care@zayvorahealth.com",
    pressEmail: "press@zayvorahealth.com"
  },
  socialLinks: [
    { platform: "LinkedIn", url: "https://linkedin.com/company/zayvora-health" },
    { platform: "X (Twitter)", url: "https://x.com/zayvorahealth" },
    { platform: "GitHub", url: "https://github.com/zayvora-health" }
  ],
  legalLinks: [
    { label: "Privacy Policy", href: "/privacy-policy" },
    { label: "Terms & Conditions", href: "/terms-and-conditions" },
    { label: "Medical Disclaimer", href: "/medical-disclaimer" }
  ],
  primaryCta: {
    label: "Explore Services",
    href: "/services"
  },
  secondaryCta: {
    label: "Clinical Login",
    href: "/login"
  },
  medicalDisclaimer: "ZAYVORA Health OS™ provides clinical decision support tools for licensed medical practitioners. It does not replace independent professional medical judgment, clinical diagnosis, or individualized treatment plans. Patients should always consult a licensed healthcare provider before initiating any new therapy.",
  copyright: `© ${new Date().getFullYear()} ZAYVORA Health™. All rights reserved. Proprietary Healthcare Operating System.`
};
