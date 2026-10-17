import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { CONDITIONS_DATA } from "@/lib/cms/conditionsData";

export const metadata = {
  title: "Health Conditions & Clinical Care Pathways | ZAYVORA Health™",
  description: "Evidence-guided clinical pathways for 10 core healthcare areas under classical Unani humoral medicine and modern diagnostic monitoring.",
};

export default function ConditionsHubPage() {
  const conditionsList = Object.values(CONDITIONS_DATA);

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Evidence-Guided Clinical Care Pathways"
        title="Health Conditions & Therapeutic Protocols"
        subtitle="Specialized clinical care pathways combining classical 4-stage humoral resolution (Tanqiya, Tahleel, Taqwiyat, Hifz) with modern biomedical laboratory monitoring."
        breadcrumbs={[{ label: "Conditions" }]}
        primaryCta={{ label: "Book a Clinical Consultation", href: "/book" }}
        secondaryCta={{ label: "Explore Health Library", href: "/health-library" }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
        
        {/* Clinical Framework Callout */}
        <div className="bg-white rounded-3xl border border-[#E2E8F0] p-8 shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-[#475569]">
            <div className="flex items-start gap-3.5">
              <div className="w-10 h-10 rounded-2xl bg-[#E8F5E9] border border-[#C8E6C9] flex items-center justify-center text-[#1B4332] shrink-0">
                <HealthcareIcon name="shield-check" className="w-5 h-5 text-[#2D6A4F]" />
              </div>
              <div>
                <h4 className="font-bold text-sm text-[#0F172A]">Individualized Etiology</h4>
                <p className="mt-1 leading-relaxed text-[#64748B]">
                  Every treatment protocol begins by diagnosing the root humoral imbalance (Su-e-Mizaj) rather than merely suppressing surface symptoms.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3.5">
              <div className="w-10 h-10 rounded-2xl bg-[#E8F5E9] border border-[#C8E6C9] flex items-center justify-center text-[#1B4332] shrink-0">
                <HealthcareIcon name="activity" className="w-5 h-5 text-[#2D6A4F]" />
              </div>
              <div>
                <h4 className="font-bold text-sm text-[#0F172A]">Sequential 4-Stage Afaal</h4>
                <p className="mt-1 leading-relaxed text-[#64748B]">
                  Therapeutics follow classical physiological logic: Tanqiya (Evacuation) → Tahleel (Resolution) → Taqwiyat (Tonification) → Hifz (Preservation).
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3.5">
              <div className="w-10 h-10 rounded-2xl bg-[#E8F5E9] border border-[#C8E6C9] flex items-center justify-center text-[#1B4332] shrink-0">
                <HealthcareIcon name="scale" className="w-5 h-5 text-[#2D6A4F]" />
              </div>
              <div>
                <h4 className="font-bold text-sm text-[#0F172A]">NCISM Governed Safety</h4>
                <p className="mt-1 leading-relaxed text-[#64748B]">
                  Protocols are authorized by registered BUMS/MD Unani clinicians with mandatory herb-drug interaction screening.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* 10 Canonical Condition Cards */}
        <div className="space-y-6">
          <div className="flex items-end justify-between">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
                10 Core Clinical Domains
              </span>
              <h2 className="text-2xl font-extrabold text-[#0F172A] mt-1">
                Explore Condition Pathways
              </h2>
            </div>
            <span className="text-xs font-mono text-[#64748B]">
              10 Pathways Codified
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {conditionsList.map((cond) => (
              <div
                key={cond.slug}
                className="bg-white rounded-3xl border border-[#E2E8F0] p-6 shadow-sm hover:border-[#CBD5E1] transition flex flex-col justify-between space-y-4"
              >
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <span className="text-[11px] font-mono text-[#2D6A4F] font-bold uppercase tracking-wider">
                        {cond.category}
                      </span>
                      <h3 className="text-lg font-bold text-[#0F172A] mt-0.5">
                        {cond.title}
                      </h3>
                      <p className="text-xs font-semibold text-[#64748B] italic">
                        Unani Term: {cond.unaniTerm}
                      </p>
                    </div>
                    <span className="px-2.5 py-1 rounded-full text-[11px] font-bold bg-[#FAFAF7] border border-[#E2E8F0] text-[#334155] shrink-0">
                      {cond.duration}
                    </span>
                  </div>

                  <p className="text-xs text-[#475569] leading-relaxed line-clamp-3">
                    {cond.overview}
                  </p>

                  <div className="pt-2 border-t border-[#F1F5F9] space-y-1">
                    <span className="text-[11px] font-bold text-[#0F172A] block">Common Indicators:</span>
                    <p className="text-xs text-[#64748B] line-clamp-2">
                      {cond.symptoms.slice(0, 3).join(" • ")}
                    </p>
                  </div>
                </div>

                <div className="pt-3 border-t border-[#F1F5F9] flex items-center justify-between">
                  <Link
                    href={`/conditions/${cond.slug}`}
                    className="text-xs font-bold text-[#1B4332] hover:text-[#2D6A4F] flex items-center gap-1.5"
                  >
                    <span>Read Complete Pathway</span>
                    <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
                  </Link>

                  <Link
                    href={`/book?condition=${cond.slug}`}
                    className="px-3.5 py-1.5 rounded-xl bg-[#E8F5E9] hover:bg-[#1B4332] text-[#1B4332] hover:text-white text-xs font-bold transition shadow-sm"
                  >
                    Book Care
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Bottom Consultation CTA */}
        <div className="bg-[#FAFAF7] rounded-3xl border border-[#E2E8F0] p-8 text-center space-y-4">
          <h3 className="text-xl font-bold text-[#0F172A]">
            Have a Specific Health Concern Not Listed Here?
          </h3>
          <p className="text-xs sm:text-sm text-[#64748B] max-w-xl mx-auto leading-relaxed">
            Our clinicians provide comprehensive constitutional assessments for a wide range of complex, chronic, and multisystem concerns.
          </p>
          <div className="pt-2">
            <Link
              href="/book"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#1B4332] text-white font-semibold text-xs hover:bg-[#2D6A4F] transition shadow-sm"
            >
              <HealthcareIcon name="calendar" className="w-4 h-4 text-[#A7F3D0]" />
              <span>Schedule General Assessment</span>
            </Link>
          </div>
        </div>

      </div>
    </PublicWebsiteShell>
  );
}
