import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { ProductCard } from "@/components/website/ProductCard";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { productsData } from "@/lib/data/products";

export const metadata = {
  title: "Functional Botanical Nutraceuticals | ZAYVORA Health Products™",
  description: "Evidence-graded functional botanical tonics, metabolic adaptogens, and cognitive nootropics.",
};

export default function NutraceuticalsCategoryPage() {
  const categoryProducts = productsData.filter((p) => p.category === "nutraceuticals");

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Metabolic Adaptogens"
        title="Functional Botanical Nutraceuticals"
        subtitle="Bridging dietary lifestyle supplementation with targeted botanical bioactives to support neuro-cognitive health, metabolic balance, and cellular defense."
        breadcrumbs={[
          { label: "Products", href: "/products" },
          { label: "Nutraceuticals" }
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
          <div className="flex items-center gap-2 text-amber-800">
            <HealthcareIcon name="shield-check" className="w-5 h-5 text-amber-700" />
            <strong className="text-sm text-[#0F172A]">Nutraceutical Safety Standard</strong>
          </div>
          <p>
            Nutraceutical formulations are prepared in cleanrooms to support specific organ systems and physiological resilience. They are accompanied by batch Certificates of Analysis and nutritional profiling.
          </p>
        </div>

        <div className="flex items-center justify-between pt-8 border-t border-slate-200 text-xs">
          <Link href="/products/unani-care" className="font-semibold text-slate-500 hover:text-slate-900">
            ← Back to Classical Unani Care
          </Link>
          <Link href="/products" className="font-bold text-amber-900 hover:text-amber-950 flex items-center gap-1">
            <span>Back to Products Overview</span>
            <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}
