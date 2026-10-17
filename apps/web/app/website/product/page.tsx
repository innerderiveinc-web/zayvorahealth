"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { PRODUCTS_CATALOG } from "@/lib/cms/productsData";

// Canonical Monograph Index
const MONOGRAPH_KEYS = [
  "manivital-pro",
  "ovasync",
  "qurs-taqwiyat-mani",
  "metabocore-elite",
  "thyromet-axis",
  "liverprime-core",
  "neurocalmx",
  "nightone-x",
  "sleep-stress",
  "men-daily"
];

export default function ProductDetailPage() {
  const searchParams = useSearchParams();
  const prodId = searchParams.get("id") || "manivital-pro";

  const product = PRODUCTS_CATALOG.find(p => p.id === prodId) || PRODUCTS_CATALOG[0];
  const [addedNotice, setAddedNotice] = useState(false);

  const handleAddToCart = () => {
    setAddedNotice(true);
    setTimeout(() => setAddedNotice(false), 3000);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-12 space-y-10 text-[#CBD5E1]">
      
      {/* Breadcrumbs */}
      <div className="flex items-center gap-2 text-xs text-[#64748B]">
        <Link href="/website" className="hover:text-white">Home</Link>
        <span>/</span>
        <Link href="/website/herbals" className="hover:text-white">Formulations</Link>
        <span>/</span>
        <span className="text-white font-medium">{product.name}</span>
      </div>

      {/* Main Product Presentation Card */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-8 p-8 rounded-3xl bg-[#0F172A] border border-[#334155]">
        
        {/* Left Visual Presentation */}
        <div className="md:col-span-5 space-y-4">
          <div className="aspect-square rounded-2xl bg-[#0A0F1D] border border-[#1E293B] flex flex-col items-center justify-center p-8 text-center space-y-3 shadow-inner">
            <span className="text-6xl">🌿</span>
            <span className="font-bold text-white text-lg">{product.name}</span>
            <span className="text-xs text-[#2DD4BF] font-mono">{product.regulatoryCategory}</span>
          </div>

          <div className="p-4 rounded-2xl bg-[#0A0F1D] border border-[#1E293B] space-y-2 text-[11px]">
            <span className="font-bold text-white uppercase tracking-wider block">Analytical Certification:</span>
            <div className="text-[#94A3B8] space-y-1">
              <div>Batch Lot: <strong className="text-white font-mono">{product.batchInfo.lotNumber}</strong></div>
              <div>Lead Content: <strong className="text-emerald-400">{product.batchInfo.leadPpm}</strong></div>
              <div>Arsenic Content: <strong className="text-emerald-400">{product.batchInfo.arsenicPpm}</strong></div>
              <div className="text-[10px] text-[#64748B] font-mono truncate">SHA256: {product.batchInfo.certificateHash}</div>
            </div>
          </div>
        </div>

        {/* Right Product Information */}
        <div className="md:col-span-7 space-y-5">
          <div className="space-y-1">
            <span className="text-xs font-semibold text-[#0D9488] uppercase tracking-wider">{product.category}</span>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white">{product.name}</h1>
            <span className="text-xs text-[#64748B]">{product.size}</span>
          </div>

          <div className="flex items-center gap-4">
            <span className="text-2xl font-extrabold text-white font-mono">{product.currency}{product.price}</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-semibold">
              ✓ In Stock ({product.stockCount} units available)
            </span>
          </div>

          <p className="text-xs text-[#94A3B8] leading-relaxed">{product.fullOverview}</p>

          {/* Prominent Mandatory Safety Notice */}
          <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs leading-snug">
            <strong>Safety Notice:</strong> {product.safetyNotice}
          </div>

          {/* Actions */}
          <div className="pt-4 border-t border-[#1E293B] space-y-3">
            {product.canBuyDirectly ? (
              <div className="flex gap-3">
                <Link
                  href={`/website/cart?add=${product.id}`}
                  className="w-full text-center py-3.5 rounded-2xl bg-[#0D9488] hover:bg-[#0F766E] text-white font-bold text-xs shadow-md transition"
                >
                  Buy Now — {product.currency}{product.price}
                </Link>
                <Link
                  href="/website/book"
                  className="w-full text-center py-3.5 rounded-2xl bg-[#1E293B] hover:bg-[#334155] border border-[#334155] text-white font-semibold text-xs transition"
                >
                  Consult Before Use
                </Link>
              </div>
            ) : (
              <div className="space-y-2">
                <Link
                  href="/website/book"
                  className="w-full block text-center py-3.5 rounded-2xl bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/40 text-amber-300 font-bold text-xs shadow-md transition"
                >
                  Book Doctor Consultation to Prescribe
                </Link>
                <p className="text-[10px] text-[#64748B] text-center">
                  This Schedule E(1) compound requires statutory clinician evaluation and 21 CFR Part 11 digital locking.
                </p>
              </div>
            )}
          </div>
        </div>

      </div>

      {/* Active Ingredients Table */}
      <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-4">
        <h3 className="text-lg font-bold text-white">Active Botanical Ingredients</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-[#94A3B8]">
            <thead className="border-b border-[#1E293B] text-white uppercase text-[10px]">
              <tr>
                <th className="py-2.5 px-3">Common Unani Name</th>
                <th className="py-2.5 px-3">Botanical / Latin Name</th>
                <th className="py-2.5 px-3">Part Used</th>
                <th className="py-2.5 px-3">HPLC Assay Standard</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]">
              {product.activeIngredients.map((ing, idx) => (
                <tr key={idx} className="hover:bg-[#1E293B]/50">
                  <td className="py-2.5 px-3 font-semibold text-white">{ing.commonName}</td>
                  <td className="py-2.5 px-3 italic">{ing.botanicalName}</td>
                  <td className="py-2.5 px-3">{ing.partUsed}</td>
                  <td className="py-2.5 px-3 text-[#2DD4BF] font-mono">{ing.assayStandard}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Suggested Usage & Contraindications */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-3 text-xs">
          <h4 className="font-bold text-white text-base">Suggested Clinical Posology</h4>
          <div className="space-y-1 text-[#94A3B8]">
            <p><strong>Dose:</strong> {product.suggestedUsage.dose}</p>
            <p><strong>Timing:</strong> {product.suggestedUsage.timing}</p>
            <p><strong>Vehicle (Anupan):</strong> {product.suggestedUsage.anupanVehicle}</p>
            <p className="text-[11px] text-[#64748B] pt-1">{product.suggestedUsage.durationNotes}</p>
          </div>
        </div>

        <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-3 text-xs">
          <h4 className="font-bold text-white text-base">Safety Warnings & Contraindications</h4>
          <div className="space-y-2 text-[#94A3B8]">
            <div>
              <strong className="text-amber-400 block">Contraindicated in:</strong>
              <ul className="list-disc list-inside text-[11px] text-[#64748B]">
                {product.contraindications.map((c, i) => (
                  <li key={i}>{c}</li>
                ))}
              </ul>
            </div>
            <p className="text-[11px] text-[#64748B] pt-1">
              <strong>Drug Interactions:</strong> {product.interactionWarning}
            </p>
          </div>
        </div>
      </div>

      {/* Manufacturer Information */}
      <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-2 text-xs">
        <h4 className="font-bold text-white text-sm">Manufacturer & Statutory Quality Assurance</h4>
        <div className="text-[#94A3B8] text-[11px] space-y-0.5">
          <p><strong>Manufactured By:</strong> {product.manufacturer.name}</p>
          <p><strong>Facility:</strong> {product.manufacturer.facility}</p>
          <p><strong>License Number:</strong> {product.manufacturer.gmpLicense}</p>
        </div>
      </div>

    </div>
  );
}
