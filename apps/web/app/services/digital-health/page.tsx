import React from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { servicesData } from "@/lib/data/services";

export const metadata = {
  title: "Digital Health & EHR Interoperability | ZAYVORA Health™",
  description: "Enterprise electronic health records, longitudinal patient timelines, and ABDM/FHIR R4 compliant interoperability.",
};

export default function DigitalHealthServicePage() {
  const service = servicesData.find(s => s.slug === "digital-health");
  if (!service) notFound();

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Enterprise Architecture"
        title={service.name}
        subtitle={service.shortDescription}
        breadcrumbs={[
          { label: "Services", href: "/services" },
          { label: service.name }
        ]}
        primaryCta={{ label: service.ctaLabel, href: service.ctaHref }}
        secondaryCta={{ label: "View All Services", href: "/services" }}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-16">
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          <div className="p-8 rounded-2xl bg-[#0D1527] border border-[#1E293B]">
            <span className="text-xs font-bold uppercase tracking-wider text-[#0D9488]">Overview</span>
            <h2 className="text-2xl font-bold text-white mt-2">Interoperable Digital Infrastructure</h2>
            <p className="mt-4 text-[#94A3B8] text-sm leading-relaxed">{service.fullDescription}</p>
          </div>

          <div className="p-8 rounded-2xl bg-[#0D1527] border border-[#1E293B]">
            <span className="text-xs font-bold uppercase tracking-wider text-[#F59E0B]">The Challenge</span>
            <h2 className="text-2xl font-bold text-white mt-2">Problem We Solve</h2>
            <p className="mt-4 text-[#94A3B8] text-sm leading-relaxed">{service.problemSolved}</p>
          </div>
        </section>

        <section className="p-8 rounded-2xl bg-[#0D1527] border border-[#1E293B]">
          <span className="text-xs font-bold uppercase tracking-wider text-[#5EEAD4]">EHR Features</span>
          <h2 className="text-2xl font-bold text-white mt-2 mb-6">Core Capabilities</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {service.capabilities.map((cap, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-[#0A0F1D] border border-[#1E293B] flex items-start gap-3">
                <span className="text-[#10B981] font-bold text-lg">✓</span>
                <span className="text-sm text-[#E2E8F0]">{cap}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="p-8 rounded-2xl bg-[#0D1527] border border-[#1E293B]">
          <span className="text-xs font-bold uppercase tracking-wider text-[#38BDF8]">Data Lifecycle</span>
          <h2 className="text-2xl font-bold text-white mt-2 mb-6">Patient Health Data Flow</h2>
          <div className="space-y-3">
            {service.workflow.map((step, idx) => (
              <div key={idx} className="flex items-center gap-4 p-3.5 rounded-xl bg-[#0A0F1D] border border-[#1E293B]">
                <span className="w-8 h-8 rounded-lg bg-[#0D9488]/20 border border-[#0D9488] text-[#5EEAD4] font-bold text-xs flex items-center justify-center shrink-0">
                  {idx + 1}
                </span>
                <span className="text-sm text-[#CBD5E1] font-medium">{step}</span>
              </div>
            ))}
          </div>
        </section>

        {service.safetyConsiderations && (
          <section className="p-6 rounded-2xl bg-[#0A0F1D] border border-[#334155]">
            <span className="text-xs font-bold uppercase tracking-wider text-[#38BDF8]">Security & Privacy</span>
            <p className="mt-2 text-sm text-[#94A3B8] leading-relaxed">{service.safetyConsiderations}</p>
          </section>
        )}

        <section className="pt-8 border-t border-[#1E293B] flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-xs text-[#64748B] font-semibold uppercase">Related Services:</span>
            {service.relatedServices.map((rel, idx) => (
              <Link key={idx} href={rel.href} className="text-xs px-3 py-1 rounded-lg bg-[#1E293B] text-[#5EEAD4] hover:bg-[#334155] transition">
                {rel.name} →
              </Link>
            ))}
          </div>
          <Link href="/about" className="px-6 py-2.5 rounded-xl bg-[#0D9488] hover:bg-[#0F766E] text-white font-bold text-xs shadow-md transition">
            Learn More About Health OS →
          </Link>
        </section>
      </div>
    </PublicWebsiteShell>
  );
}
