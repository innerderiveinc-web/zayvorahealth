import React from "react";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";

export const metadata = {
  title: "ZAYVORA Health™ — Modern Unani Integrative Healthcare System",
  description: "Ancient Wisdom. Modern Science. Intelligent Care. Classical Unani Medicine integrated with contemporary biomedical intelligence, organ-axis clinical framework, and 21 CFR Part 11 governance.",
};

export default function WebsiteLayout({ children }: { children: React.ReactNode }) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "MedicalOrganization",
    "name": "ZAYVORA Health™",
    "alternateName": ["ZAYVORA Matab™", "ZAYVORA Health OS™"],
    "url": "https://www.zayvorahealth.com",
    "logo": "https://www.zayvorahealth.com/logo.png",
    "description": "Ancient Wisdom. Modern Science. Intelligent Care. Classical Unani Medicine integrated with contemporary biomedical intelligence, organ-axis clinical framework, and Hakeem Sahab AI™ clinical reasoning.",
    "telephone": "+91-97738-82657",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "ZAYVORA Health Complex, Central Care Wing",
      "addressLocality": "New Delhi",
      "postalCode": "110062",
      "addressCountry": "IN"
    },
    "medicalSpecialty": [
      "https://schema.org/TraditionalChineseOrAyurvedic",
      "Integrative Unani Medicine",
      "Holistic Metabolic Health",
      "Endocrine and Reproductive Wellness"
    ],
    "availableService": [
      {
        "@type": "MedicalProcedure",
        "name": "10-Ajnas Mizaj Assessment",
        "description": "Comprehensive constitutional temperament evaluation"
      },
      {
        "@type": "MedicalProcedure",
        "name": "Matab Clinical Consultation",
        "description": "In-clinic and teleconsultation care led by licensed senior tabeebs"
      }
    ]
  };

  return (
    <PublicWebsiteShell>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      {children}
    </PublicWebsiteShell>
  );
}
