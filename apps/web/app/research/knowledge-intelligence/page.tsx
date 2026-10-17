import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { ResearchCard } from "@/components/website/ResearchCard";
import { researchData } from "@/lib/data/research";

export const metadata = {
  title: "ZAYVORA Knowledge Intelligence™ | Ontological Graph & Classical OCR",
  description: "Explore the ZAYVORA Knowledge Base (ZKB), combining multi-hop Neo4j knowledge graphs with Bio-BERT embeddings and historical manuscript OCR pipelines.",
};

export default function KnowledgeIntelligenceCategoryPage() {
  const categoryStudies = researchData.filter(r => r.category === "knowledge-intelligence");

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Ontological Knowledge Layer"
        title="Knowledge Intelligence & Ontological Graphs"
        subtitle="Unifying classical Arabic, Persian, and Urdu Unani pharmacopoeia with modern biomedical vocabularies (SNOMED CT, MeSH, ICD-11) through graph retrieval."
        breadcrumbs={[
          { label: "Research", href: "/research" },
          { label: "Knowledge Intelligence" }
        ]}
        primaryCta={{ label: "Explore Hakeem Sahab AI", href: "/services/ai-healthcare" }}
        secondaryCta={{ label: "Research Hub", href: "/research" }}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {categoryStudies.map((item) => (
            <ResearchCard key={item.id} item={item} />
          ))}
        </div>

        <div className="p-6 rounded-2xl bg-[#0D1527] border border-[#1E293B] text-xs text-[#94A3B8] leading-relaxed">
          <strong className="text-white block mb-1">Peer-Reviewed Knowledge Governance:</strong>
          Every entity, botanical synonym, and therapeutic property in the ZAYVORA Knowledge Base (ZKB) is reviewed and certified by a formal Clinical Governance Board quorum prior to ingestion into the live AI retrieval index.
        </div>

        <div className="flex items-center justify-between pt-8 border-t border-[#1E293B]">
          <Link href="/research/clinical-research" className="text-xs font-semibold text-[#5EEAD4] hover:underline">
            ← Back to Clinical Research Protocols
          </Link>
          <Link href="/research" className="text-xs font-semibold text-[#94A3B8] hover:text-white">
            ← Back to Research Overview
          </Link>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}
