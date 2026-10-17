import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { ProductCard } from "@/components/website/ProductCard";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { productsData } from "@/lib/data/products";

export const metadata = {
  title: "Classical Unani Care Formulations | ZAYVORA Health Products™",
  description: "Classical Majoon, Khamira, and Itrifal compound formulations prepared according to ancient Greco-Arab and Unani pharmacopoeia standards.",
};

export default function UnaniCareCategoryPage() {
  const categoryProducts = productsData.filter((p) => p.category === "unani-care");

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Classical Unani Care"
        title="Authentic Unani Compound Formulations"
        subtitle="Master formulations crafted from classical treatises (Qarabadin-e-Kabir, Bayaz-e-Kabir) using certified botanical extracts and traditional honey/sugar vehicles."
        breadcrumbs={[
          { label: "Products", href: "/products" },
          { label: "Unani Care" }
        ]}
        primaryCta={{ label: "Consult Attending Tabeeb", href: "/contact" }}
        secondaryCta={{ label: "All Product Categories", href: "/products" }}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {categoryProducts.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>

        {/* Regulatory note */}
        <div className="p-7 rounded-3xl bg-white border border-slate-200/90 shadow-sm text-xs text-slate-600 leading-relaxed space-y-1.5">
          <div className="flex items-center gap-2 text-emerald-800">
            <HealthcareIcon name="shield-check" className="w-5 h-5 text-emerald-700" />
            <strong className="text-sm text-[#0F172A]">Classical Formulation Standards</strong>
          </div>
          <p>
            Classical Unani medicines are formulated strictly according to the National Pharmacopoeia of India and authoritative classical canons. Dispensing is governed under clinician supervision to ensure accurate posology and constitutional compatibility.
          </p>
        </div>

        {/* Category Navigation */}
        <div className="flex items-center justify-between pt-8 border-t border-slate-200 text-xs">
          <Link href="/products" className="font-semibold text-slate-500 hover:text-slate-900">
            ← Back to Products Overview
          </Link>
          <Link href="/products/herbal-products" className="font-bold text-emerald-800 hover:text-emerald-950 flex items-center gap-1">
            <span>Next: Standardized Herbal Products</span>
            <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}
