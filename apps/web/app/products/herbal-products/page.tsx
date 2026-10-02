import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { ProductCard } from "@/components/website/ProductCard";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { productsData } from "@/lib/data/products";

export const metadata = {
  title: "Standardized Herbal Products | ZAYVORA Health Products™",
  description: "Standardized active botanical extracts, HPLC-quantified compounds, and customized herbal remedies.",
};

export default function HerbalProductsCategoryPage() {
  const categoryProducts = productsData.filter((p) => p.category === "herbal-products");

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Active Botanical Extracts"
        title="Standardized Herbal Products"
        subtitle="Botanical compounds engineered with quantified bioactive marker fractions, modern bioavailability enhancers, and zero synthetic fillers."
        breadcrumbs={[
          { label: "Products", href: "/products" },
          { label: "Herbal Products" }
        ]}
        primaryCta={{ label: "Consult Tabeeb", href: "/contact" }}
        secondaryCta={{ label: "All Product Categories", href: "/products" }}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {categoryProducts.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>

        <div className="p-7 rounded-3xl bg-white border border-slate-200/90 shadow-sm text-xs text-slate-600 leading-relaxed space-y-1.5">
          <div className="flex items-center gap-2 text-teal-800">
            <HealthcareIcon name="flask" className="w-5 h-5 text-teal-700" />
            <strong className="text-sm text-[#0F172A]">Standardized Potency Assays</strong>
          </div>
          <p>
            Every herbal product batch is tested via High-Performance Liquid Chromatography (HPLC) to guarantee certified active marker levels (e.g., 5% withanolides, 10% L-DOPA) for predictable clinical efficacy.
          </p>
        </div>

        <div className="flex items-center justify-between pt-8 border-t border-slate-200 text-xs">
          <Link href="/products" className="font-semibold text-slate-500 hover:text-slate-900">
            ← Back to Products Overview
          </Link>
          <Link href="/products/nutraceuticals" className="font-bold text-teal-800 hover:text-teal-950 flex items-center gap-1">
            <span>Next: Functional Nutraceuticals</span>
            <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}
