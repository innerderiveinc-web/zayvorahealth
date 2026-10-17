import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { ResearchCard } from "@/components/website/ResearchCard";
import { researchData } from "@/lib/data/research";

export const metadata = {
  title: "Research & Evidence Ecosystem | ZAYVORA Health™",
  description: "Explore our clinical research trials, real-world evidence studies, and the ZAYVORA Knowledge Base (ZKB) ontological intelligence layer.",
};

export default function ResearchOverviewPage() {
  const clinicalResearch = researchData.filter(r => r.category === "clinical-research");
  const evidenceStudies = researchData.filter(r => r.category === "evidence");
  const knowledgeIntelligence = researchData.filter(r => r.category === "knowledge-intelligence");

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Evidence-Based Traditional Medicine"
        title="Scientific Inquiry & Real-World Validation"
        subtitle="Empirical Unani wisdom subjected to GCP clinical trials, real-world evidence surveillance, and ontological knowledge graph representation."
        breadcrumbs={[{ label: "Research" }]}
        primaryCta={{ label: "Research Collaboration", href: "/contact" }}
        secondaryCta={{ label: "Knowledge Intelligence", href: "/research/knowledge-intelligence" }}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-20">
        {/* Research Category Navigation */}
        <div className="flex flex-wrap items-center justify-center gap-4 border-b border-[#1E293B] pb-8">
          <Link
            href="/research/clinical-research"
            className="px-5 py-2.5 rounded-xl bg-[#0D1527] hover:bg-[#1E293B] border border-[#334155] text-white text-xs font-semibold flex items-center gap-2 transition"
          >
            <span>📊</span>
            <span>Clinical Research ({clinicalResearch.length})</span>
          </Link>
          <Link
            href="/research/evidence"
            className="px-5 py-2.5 rounded-xl bg-[#0D1527] hover:bg-[#1E293B] border border-[#334155] text-white text-xs font-semibold flex items-center gap-2 transition"
          >
            <span>📑</span>
            <span>Biomedical Evidence ({evidenceStudies.length})</span>
          </Link>
          <Link
            href="/research/knowledge-intelligence"
            className="px-5 py-2.5 rounded-xl bg-[#0D1527] hover:bg-[#1E293B] border border-[#334155] text-white text-xs font-semibold flex items-center gap-2 transition"
          >
            <span>🌐</span>
            <span>Knowledge Intelligence ({knowledgeIntelligence.length})</span>
          </Link>
        </div>

        {/* 1. Clinical Research Section */}
        <section>
          <div className="flex items-center justify-between mb-8">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-[#3B82F6]">Prospective Trials</span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-1">Clinical Research Studies</h2>
              <p className="text-sm text-[#94A3B8] mt-1">GCP-compliant trials evaluating Unani therapeutic regimens.</p>
            </div>
            <Link href="/research/clinical-research" className="text-xs font-semibold text-[#60A5FA] hover:underline hidden sm:inline">
              View All Clinical Studies →
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {clinicalResearch.map(r => <ResearchCard key={r.id} item={r} />)}
          </div>
        </section>

        {/* 2. Evidence & Surveillance Section */}
        <section>
          <div className="flex items-center justify-between mb-8">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-[#10B981]">Real-World Surveillance</span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-1">Biomedical Evidence & Pharmacovigilance</h2>
              <p className="text-sm text-[#94A3B8] mt-1">Analytical Mudabbar characterization and continuous ADR surveillance.</p>
            </div>
            <Link href="/research/evidence" className="text-xs font-semibold text-[#34D399] hover:underline hidden sm:inline">
              View All Evidence Protocols →
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {evidenceStudies.map(r => <ResearchCard key={r.id} item={r} />)}
          </div>
        </section>

        {/* 3. Knowledge Intelligence Section */}
        <section>
          <div className="flex items-center justify-between mb-8">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-[#A855F7]">Ontological AI Core</span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-1">Knowledge Intelligence (ZKB)</h2>
              <p className="text-sm text-[#94A3B8] mt-1">Multi-hop graph retrieval and historical manuscript OCR digitization.</p>
            </div>
            <Link href="/research/knowledge-intelligence" className="text-xs font-semibold text-[#C084FC] hover:underline hidden sm:inline">
              View Knowledge Architecture →
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {knowledgeIntelligence.map(r => <ResearchCard key={r.id} item={r} />)}
          </div>
        </section>

        {/* Institutional Collaboration Banner */}
        <section className="p-8 rounded-3xl bg-[#0D1527] border border-[#0D9488]/40 flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <h3 className="text-xl font-bold text-white">Participate in Clinical Research</h3>
            <p className="text-xs text-[#94A3B8] mt-1 max-w-xl leading-relaxed">
              We collaborate with accredited university medical centers, research institutes, and clinical investigators to advance evidence-based traditional medicine under formal Institutional Review Board (IRB) ethics oversight.
            </p>
          </div>
          <Link
            href="/contact"
            className="px-6 py-3 rounded-xl bg-[#0D9488] hover:bg-[#0F766E] text-white font-bold text-xs shadow-md shrink-0 transition"
          >
            Submit Research Proposal →
          </Link>
        </section>
      </div>
    </PublicWebsiteShell>
  );
}
