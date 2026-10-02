import React from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { servicesData } from "@/lib/data/services";

export const metadata = {
  title: "Pharmacy & Dispensary OS | ZAYVORA Health™",
  description: "First-Expired-First-Out (FEFO) dispensing, batch traceability, and Schedule E(1) Mudabbar detoxification controls.",
};

export default function PharmacyServicePage() {
  const service = servicesData.find(s => s.slug === "pharmacy");
  if (!service) notFound();

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Dispensary OS"
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
            <h2 className="text-2xl font-bold text-white mt-2">Botanical Pharmacy Safety</h2>
            <p className="mt-4 text-[#94A3B8] text-sm leading-relaxed">{service.fullDescription}</p>
          </div>

          <div className="p-8 rounded-2xl bg-[#0D1527] border border-[#1E293B]">
            <span className="text-xs font-bold uppercase tracking-wider text-[#F59E0B]">The Challenge</span>
            <h2 className="text-2xl font-bold text-white mt-2">Problem We Solve</h2>
            <p className="mt-4 text-[#94A3B8] text-sm leading-relaxed">{service.problemSolved}</p>
          </div>
        </section>

        <section className="p-8 rounded-2xl bg-[#0D1527] border border-[#1E293B]">
          <span className="text-xs font-bold uppercase tracking-wider text-[#5EEAD4]">Dispensary Features</span>
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
          <span className="text-xs font-bold uppercase tracking-wider text-[#38BDF8]">Fulfillment Protocol</span>
          <h2 className="text-2xl font-bold text-white mt-2 mb-6">FEFO Dispensing Journey</h2>
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
          <section className="p-6 rounded-2xl bg-[#7F1D1D]/10 border border-[#DC2626]/30">
            <span className="text-xs font-bold uppercase tracking-wider text-red-400">Mudabbar Verification Gate</span>
            <p className="mt-2 text-sm text-[#FCA5A5] leading-relaxed">{service.safetyConsiderations}</p>
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
          <Link href="/products" className="px-6 py-2.5 rounded-xl bg-[#0D9488] hover:bg-[#0F766E] text-white font-bold text-xs shadow-md transition">
            Browse Botanical Formulations →
          </Link>
        </section>
      </div>
    </PublicWebsiteShell>
  );
}
