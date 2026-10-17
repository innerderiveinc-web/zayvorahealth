import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { ProductCard } from "@/components/website/ProductCard";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { productsData } from "@/lib/data/products";

export const metadata = {
  title: "ZAYVORA Health Products™ | Botanical Formulations & Quality Standards",
  description: "Explore classical Unani medicines, standardized herbal extracts, and functional nutraceuticals prepared in AYUSH-GMP certified cleanrooms.",
};

export default function ProductsOverviewPage() {
  const unaniProducts = productsData.filter((p) => p.category === "unani-care");
  const herbalProducts = productsData.filter((p) => p.category === "herbal-products");
  const nutraceuticals = productsData.filter((p) => p.category === "nutraceuticals");

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Botanical Pharmacy & Cleanroom"
        title="Standardized Botanical Formulations"
        subtitle="Prepared under strict AYUSH-GMP and 21 CFR Part 11 cleanroom standards, free from synthetic adulterants and verified via HPTLC and heavy metal screening."
        breadcrumbs={[{ label: "Products" }]}
        primaryCta={{ label: "Consult Tabeeb for Prescriptions", href: "/contact" }}
        secondaryCta={{ label: "Dispensary Standards", href: "/services/pharmacy" }}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-16">
        
        {/* Category Jump Navigation */}
        <div className="flex flex-wrap items-center justify-center gap-4 bg-white p-4 rounded-3xl border border-slate-200/90 shadow-sm">
          <Link
            href="/products/unani-care"
            className="px-5 py-3 rounded-2xl bg-emerald-50 hover:bg-emerald-100 text-[#1B4332] text-xs font-bold flex items-center gap-2.5 transition border border-emerald-200/60"
          >
            <HealthcareIcon name="pill" className="w-4 h-4 text-emerald-700" />
            <span>Classical Unani Formulations ({unaniProducts.length})</span>
          </Link>
          <Link
            href="/products/herbal-products"
            className="px-5 py-3 rounded-2xl bg-teal-50 hover:bg-teal-100 text-[#2D6A4F] text-xs font-bold flex items-center gap-2.5 transition border border-teal-200/60"
          >
            <HealthcareIcon name="leaf" className="w-4 h-4 text-[#2D6A4F]" />
            <span>Standardized Herbal Products ({herbalProducts.length})</span>
          </Link>
          <Link
            href="/products/nutraceuticals"
            className="px-5 py-3 rounded-2xl bg-amber-50 hover:bg-amber-100 text-amber-900 text-xs font-bold flex items-center gap-2.5 transition border border-amber-200/60"
          >
            <HealthcareIcon name="flask" className="w-4 h-4 text-amber-700" />
            <span>Functional Nutraceuticals ({nutraceuticals.length})</span>
          </Link>
        </div>

        {/* 1. Classical Unani Care */}
        <section className="space-y-6">
          <div className="flex items-center justify-between border-b border-slate-200 pb-4">
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Qarabadin Canon Standard</span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] mt-1">Classical Unani Formulations</h2>
              <p className="text-xs sm:text-sm text-slate-500 mt-1">Authentic Majoon, Khamira, Safoof, and Itrifal compound formulations.</p>
            </div>
            <Link href="/products/unani-care" className="text-xs font-bold text-emerald-800 hover:text-emerald-950 flex items-center gap-1.5 hidden sm:flex">
              <span>View All Unani Formulations</span>
              <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {unaniProducts.map((p) => <ProductCard key={p.id} product={p} />)}
          </div>
        </section>

        {/* 2. Standardized Herbal Products */}
        <section className="space-y-6">
          <div className="flex items-center justify-between border-b border-slate-200 pb-4">
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-[#2D6A4F]">Active Botanical Extracts</span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] mt-1">Standardized Herbal Products</h2>
              <p className="text-xs sm:text-sm text-slate-500 mt-1">HPLC-quantified botanical active fractions, distillates, and targeted tinctures.</p>
            </div>
            <Link href="/products/herbal-products" className="text-xs font-bold text-teal-800 hover:text-teal-950 flex items-center gap-1.5 hidden sm:flex">
              <span>View All Herbal Products</span>
              <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {herbalProducts.map((p) => <ProductCard key={p.id} product={p} />)}
          </div>
        </section>

        {/* 3. Functional Nutraceuticals */}
        <section className="space-y-6">
          <div className="flex items-center justify-between border-b border-slate-200 pb-4">
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-amber-800">Metabolic & Adaptogenic Support</span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] mt-1">Functional Nutraceuticals</h2>
              <p className="text-xs sm:text-sm text-slate-500 mt-1">Bioavailable mineral complexes, nootropics, and cellular antioxidant blends.</p>
            </div>
            <Link href="/products/nutraceuticals" className="text-xs font-bold text-amber-900 hover:text-amber-950 flex items-center gap-1.5 hidden sm:flex">
              <span>View All Nutraceuticals</span>
              <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {nutraceuticals.map((p) => <ProductCard key={p.id} product={p} />)}
          </div>
        </section>

        {/* Quality Philosophy Callout */}
        <section className="p-8 rounded-3xl bg-white border border-slate-200/90 shadow-sm grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-600">
          <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
            <div className="flex items-center gap-2 text-emerald-800">
              <HealthcareIcon name="shield-check" className="w-5 h-5 text-emerald-700" />
              <span className="font-bold text-sm text-[#0F172A]">Mudabbar Detoxification</span>
            </div>
            <p className="leading-relaxed">Every batch of Suranjan, Azaraqi, and classical mineral calx undergoes verified pharmacopoeial Mudabbar processing prior to dispensing.</p>
          </div>
          
          <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
            <div className="flex items-center gap-2 text-teal-800">
              <HealthcareIcon name="flask" className="w-5 h-5 text-teal-700" />
              <span className="font-bold text-sm text-[#0F172A]">ICP-MS Heavy Metal Screen</span>
            </div>
            <p className="leading-relaxed">Screened via Inductively Coupled Plasma Mass Spectrometry (ICP-MS) to certify zero toxic lead, mercury, arsenic, or cadmium adulteration.</p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
            <div className="flex items-center gap-2 text-amber-800">
              <HealthcareIcon name="lock" className="w-5 h-5 text-amber-700" />
              <span className="font-bold text-sm text-[#0F172A]">21 CFR Part 11 eBMR</span>
            </div>
            <p className="leading-relaxed">Every manufacturing step is electronically logged with dual technician sign-off and tamper-evident cryptographic audit ledger entries.</p>
          </div>
        </section>

      </div>
    </PublicWebsiteShell>
  );
}
