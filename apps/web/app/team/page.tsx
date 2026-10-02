import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { TeamCard } from "@/components/website/TeamCard";
import { teamData } from "@/lib/data/team";

export const metadata = {
  title: "Clinical Leadership & Scientific Team | ZAYVORA Health™",
  description: "Meet the senior Tabeebs, physician-scientists, pharmacognosists, and informatics engineers leading ZAYVORA Health™.",
};

export default function TeamPage() {
  const clinicalTeam = teamData.filter(m => m.division === "Clinical");
  const scientificTeam = teamData.filter(m => m.division !== "Clinical");

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Clinical Leadership"
        title="Distinguished Clinicians & Scientists"
        subtitle="Our multidisciplinary panel combines accredited Unani medical scholars, biomedical pharmacologists, and healthcare informatics engineers."
        breadcrumbs={[{ label: "Team" }]}
        primaryCta={{ label: "Consult Attending Tabeeb", href: "/contact" }}
        secondaryCta={{ label: "Explore Research", href: "/research" }}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-16">
        {/* Clinical Leadership */}
        <section>
          <div className="mb-8">
            <span className="text-xs font-bold uppercase tracking-wider text-[#0D9488]">Clinical Directorate</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-1">Attending Tabeebs & Physicians</h2>
            <p className="text-sm text-[#94A3B8] mt-1">Licensed clinicians leading patient consultations and regimenal care at ZAYVORA Matab™.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {clinicalTeam.map(member => <TeamCard key={member.id} member={member} />)}
          </div>
        </section>

        {/* Scientific & Technical Leadership */}
        <section>
          <div className="mb-8">
            <span className="text-xs font-bold uppercase tracking-wider text-[#6366F1]">Scientific & Systems Team</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-1">Research & Clinical Informatics</h2>
            <p className="text-sm text-[#94A3B8] mt-1">Engineers, pharmacognosists, and safety leads governing the ZAYVORA Health OS™ platform.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {scientificTeam.map(member => <TeamCard key={member.id} member={member} />)}
          </div>
        </section>

        {/* Clinical Governance Pledge */}
        <section className="p-8 rounded-3xl bg-[#0D1527] border border-[#1E293B] text-center max-w-3xl mx-auto">
          <span className="text-xs font-bold uppercase tracking-wider text-[#5EEAD4]">Ethical Governance</span>
          <h3 className="text-xl font-bold text-white mt-2">100% Clinician-Supervised Healthcare</h3>
          <p className="mt-3 text-xs sm:text-sm text-[#94A3B8] leading-relaxed">
            Every clinical protocol, formulation recipe, and AI suggestion in the ZAYVORA ecosystem is governed by licensed medical practitioners holding accredited degrees from recognized statutory universities.
          </p>
          <div className="mt-6">
            <Link
              href="/contact"
              className="px-6 py-2.5 rounded-xl bg-[#0D9488] hover:bg-[#0F766E] text-white font-bold text-xs shadow-md transition inline-block"
            >
              Book Consultation with Clinical Team →
            </Link>
          </div>
        </section>
      </div>
    </PublicWebsiteShell>
  );
}
