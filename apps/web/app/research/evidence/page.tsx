import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { ResearchCard } from "@/components/website/ResearchCard";
import { researchData } from "@/lib/data/research";

export const metadata = {
  title: "Biomedical Evidence & Pharmacovigilance | ZAYVORA Health™",
  description: "Real-world evidence surveillance, analytical Mudabbar detoxification characterization, and continuous adverse drug reaction monitoring.",
};

export default function EvidenceCategoryPage() {
  const categoryStudies = researchData.filter(r => r.category === "evidence");

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Biomedical Evidence"
        title="Evidence Engine & Pharmacovigilance"
        subtitle="Analytical quantification of botanical mechanisms, Mudabbar processing safety profiles, and algorithmic surveillance of Schedule E(1) traditional medicines."
        breadcrumbs={[
          { label: "Research", href: "/research" },
          { label: "Evidence" }
        ]}
        primaryCta={{ label: "View Mudabbar Research", href: "/research/evidence" }}
        secondaryCta={{ label: "Research Hub", href: "/research" }}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {categoryStudies.map((item) => (
            <ResearchCard key={item.id} item={item} />
          ))}
        </div>

        <div className="p-6 rounded-2xl bg-[#0D1527] border border-[#1E293B] text-xs text-[#94A3B8] leading-relaxed">
          <strong className="text-white block mb-1">Continuous Safety Surveillance:</strong>
          Our pharmacovigilance surveillance monitors patient encounters algorithms in real time. Suspected adverse drug reactions trigger automated clinical duty alerts and mandatory follow-up liver/renal biomarker assessments.
        </div>

        <div className="flex items-center justify-between pt-8 border-t border-[#1E293B]">
          <Link href="/research/knowledge-intelligence" className="text-xs font-semibold text-[#5EEAD4] hover:underline">
            Next: Knowledge Intelligence (ZKB) →
          </Link>
          <Link href="/research" className="text-xs font-semibold text-[#94A3B8] hover:text-white">
            ← Back to Research Overview
          </Link>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}
