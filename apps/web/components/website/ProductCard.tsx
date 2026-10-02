import React from "react";
import Link from "next/link";
import { ProductItem } from "@/lib/data/types";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

interface ProductCardProps {
  product: ProductItem;
}

export function ProductCard({ product }: ProductCardProps) {
  return (
    <div className="group rounded-3xl bg-white border border-slate-200/90 hover:border-emerald-600/40 p-6 flex flex-col justify-between shadow-sm hover:shadow-md transition-all duration-200 space-y-5">
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
            {product.categoryLabel}
          </span>
          {product.badge && (
            <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-800 border border-amber-200">
              {product.badge}
            </span>
          )}
        </div>

        <h3 className="text-lg font-bold text-[#0F172A] group-hover:text-emerald-800 transition">
          {product.name}
        </h3>
        
        <p className="text-xs italic text-emerald-700 font-medium">
          {product.tagline}
        </p>

        <p className="text-xs text-slate-600 leading-relaxed line-clamp-3">
          {product.description}
        </p>

        <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/70">
          <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Key Actives / Botanical Fractions</p>
          <p className="text-xs text-slate-800 font-medium truncate">
            {product.keyIngredients.join(" • ")}
          </p>
        </div>

        <div className="text-[11px] text-slate-500">
          <span className="font-semibold text-slate-700">Standards: </span>
          {product.qualityStandards.slice(0, 2).join(" • ")}
        </div>
      </div>

      <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
        <div>
          {product.price ? (
            <div className="flex items-baseline gap-1.5">
              <span className="text-lg font-extrabold text-[#0F172A]">{product.price}</span>
              {product.volume && <span className="text-xs text-slate-400">/ {product.volume}</span>}
            </div>
          ) : (
            <span className="text-xs text-slate-500 font-medium">{product.availabilityStatus}</span>
          )}
        </div>

        <Link
          href={`/products/${product.category}`}
          className="px-4 py-2 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white text-xs font-bold shadow-sm transition flex items-center gap-1.5"
        >
          <span>View Details</span>
          <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
}
