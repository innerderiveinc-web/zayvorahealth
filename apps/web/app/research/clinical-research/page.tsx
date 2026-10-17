import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { ResearchCard } from "@/components/website/ResearchCard";
import { researchData } from "@/lib/data/research";

export const metadata = {
  title: "Clinical Research & Trials | ZAYVORA Health™",
  description: "Prospective clinical trials, observational study protocols, and clinical concordance evaluations in Unani medicine.",
};

export default function ClinicalResearchCategoryPage() {
  const categoryStudies = researchData.filter(r => r.category === "clinical-research");

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Prospective Trials"
        title="Clinical Research Protocols & Trials"
        subtitle="Empirical Unani therapeutic protocols evaluated across multi-center outpatient trials with standardized diagnostic biomarkers and GCP governance."
        breadcrumbs={[
          { label: "Research", href: "/research" },
          { label: "Clinical Research" }
        ]}
        primaryCta={{ label: "Research Inquiries", href: "/contact" }}
        secondaryCta={{ label: "Research Hub", href: "/research" }}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {categoryStudies.map((item) => (
            <ResearchCard key={item.id} item={item} />
          ))}
        </div>

        <div className="p-6 rounded-2xl bg-[#0D1527] border border-[#1E293B] text-xs text-[#94A3B8] leading-relaxed">
          <strong className="text-white block mb-1">Good Clinical Practice (GCP) Standards:</strong>
          All ZAYVORA clinical trials operate with prior Institutional Review Board (IRB) ethical clearance and voluntary informed patient consent. Trial data is monitored under independent Data and Safety Monitoring Boards (DSMB).
        </div>

        <div className="flex items-center justify-between pt-8 border-t border-[#1E293B]">
          <Link href="/research/evidence" className="text-xs font-semibold text-[#5EEAD4] hover:underline">
            Next: Biomedical Evidence & Pharmacovigilance →
          </Link>
          <Link href="/research" className="text-xs font-semibold text-[#94A3B8] hover:text-white">
            ← Back to Research Overview
          </Link>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}
