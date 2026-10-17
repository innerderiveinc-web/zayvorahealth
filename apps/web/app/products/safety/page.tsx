import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export const metadata = {
  title: "Product Quality, Cleanroom Standards & Safety | ZAYVORA Health™",
  description: "Learn about ZAYVORA cleanroom pharmaceutical standards: AYUSH-GMP, Schedule E(1) Mudabbar detoxification, ICP-MS heavy metal limits, and HPTLC testing.",
};

export default function ProductSafetyPage() {
  const safetyTests = [
    {
      title: "ICP-MS Heavy Metal Screening",
      desc: "Every finished lot is tested via Inductively Coupled Plasma Mass Spectrometry to guarantee toxic elements (Lead, Mercury, Arsenic, Cadmium) are strictly below WHO/AYUSH limits.",
      icon: "flask"
    },
    {
      title: "HPTLC Fingerprint Verification",
      desc: "High-Performance Thin-Layer Chromatography verifies the botanical identity and quantifies target active chemical markers (e.g. colchicine, withanolides, glycyrrhizin).",
      icon: "clipboard"
    },
    {
      title: "Microbial & Aflatoxin Assay",
      desc: "Comprehensive bioburden analysis testing for total aerobic microbial count, yeast and molds, E. coli, Salmonella, and B1/B2/G1/G2 aflatoxins.",
      icon: "shield-check"
    },
    {
      title: "Schedule E(1) Mudabbar Gate",
      desc: "Classical poisonous botanicals (Suranjan, Kuchla) undergo documented detoxification cycles in cleanroom chambers before incorporation into complex compounds.",
      icon: "pill"
    }
  ];

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Pharmaceutical Rigor"
        title="Botanical Quality & Cleanroom Safety"
        subtitle="Every classical formulation and botanical extract is manufactured in ISO Class 7 cleanrooms adhering strictly to Schedule M-I (AYUSH GMP) and 21 CFR Part 11 electronic batch records."
        breadcrumbs={[
          { label: "Products", href: "/products" },
          { label: "Product Safety Standards" }
        ]}
        primaryCta={{ label: "View Botanical Formulations", href: "/products" }}
        secondaryCta={{ label: "Inquire Quality Assurance", href: "/contact" }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">
        
        {/* Safety Assays Grid */}
        <section className="space-y-8">
          <div className="text-center max-w-2xl mx-auto space-y-2">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Analytical Verification</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A]">Batch Testing & Pharmacopoeial Benchmarks</h2>
            <p className="text-xs sm:text-sm text-slate-500">Zero tolerance for adulteration, synthetic fortification, or toxic residual solvents</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {safetyTests.map((t, idx) => (
              <div
                key={idx}
                className="bg-white rounded-3xl border border-slate-200/90 p-8 shadow-sm space-y-4"
              >
                <div className="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-800">
                  <HealthcareIcon name={t.icon} className="w-6 h-6 text-emerald-700" />
                </div>
                <h3 className="text-lg font-bold text-[#0F172A]">{t.title}</h3>
                <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">{t.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* 21 CFR Part 11 eBMR */}
        <section className="bg-white rounded-3xl border border-slate-200/90 p-8 sm:p-10 shadow-sm space-y-6">
          <div className="border-b border-slate-100 pb-4">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Cleanroom Telemetry</span>
            <h3 className="text-xl font-bold text-[#0F172A] mt-1">21 CFR Part 11 Electronic Batch Manufacturing Records (eBMR)</h3>
          </div>

          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed max-w-4xl">
            Our cleanroom processing suites log real-time differential pressure, relative humidity (35–50%), and temperature (18–22°C) via calibrated IoT sensor nodes. Every compounding stage requires dual technician biometric or cryptographic token sign-off, creating an immutable audit trail from raw botanical arrival to patient dispensation.
          </p>

          <div className="pt-4 flex items-center justify-between border-t border-slate-100 text-xs">
            <span className="text-slate-500">Conforming to UPI Vol I–VI and NFUM Part I–VI specifications.</span>
            <Link href="/products" className="text-emerald-800 font-bold hover:underline">
              Explore Certified Formulations →
            </Link>
          </div>
        </section>

      </div>
    </PublicWebsiteShell>
  );
}
