"use client";

import React, { useState } from "react";
import Link from "next/link";

export default function ProductDetailPage() {
  const [selectedLot, setSelectedLot] = useState("LOT-2026-0814");

  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">Botanical Monograph & CoA</span>
          <h1 className="text-3xl font-extrabold text-white mt-1">ManiVital Pro</h1>
          <p className="text-sm text-[#94A3B8]">Targeted Male Reproductive Vitality Formulation • SKU: ZY-FERT-001</p>
        </div>
        <div className="text-right">
          <span className="text-2xl font-bold text-white block">₹ 1,450</span>
          <span className="text-[10px] text-emerald-400 font-semibold block">In Stock • FEFO Priority Released</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
            <h3 className="text-sm font-bold text-white">Clinical Indications & Classical Action</h3>
            <p>
              Indicated for male reproductive fatigue (*Zof-e-Bah*), seminal thinning (*Riqqat-e-Mani*), and constitutional exhaustion (*Zof-e-Aam*). Formulated under the principles of Ibn Rushd's *Kitab al-Kulliyat* to enhance innate vitality (*Quwwat-e-Bahiyah*) without provoking secondary heat.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
            <h3 className="text-sm font-bold text-white">Standardized Botanical Actives</h3>
            <ul className="space-y-1.5 list-disc pl-5 text-[#94A3B8]">
              <li><strong>Withania somnifera (Asgandh):</strong> Standardized to 5.0% Withanolides (HPLC verified).</li>
              <li><strong>Mucuna pruriens (Kunch):</strong> Standardized to 15.0% L-DOPA.</li>
              <li><strong>Asphaltum punjabianum (Shilajit):</strong> Purified Shodhit extract with 50% Fulvic Acid.</li>
              <li><strong>Chlorophytum borivilianum (Safed Musli):</strong> 20% Saponins.</li>
            </ul>
          </div>

          <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
            <h3 className="text-sm font-bold text-white">Posology & Administration</h3>
            <p>
              Take 5g (one level metric teaspoon) twice daily after breakfast and dinner with 200ml lukewarm milk (*Sheer-e-Gao*) or warm water. Avoid cold and sour foods during active regimen.
            </p>
          </div>
        </div>

        {/* Batch CoA Card */}
        <div className="space-y-4">
          <div className="p-5 rounded-2xl bg-[#0F172A] border border-[#334155] space-y-3">
            <span className="text-xs font-bold text-white block">Analytical CoA Verification</span>
            <div className="space-y-1.5 text-[11px]">
              <div className="flex justify-between">
                <span className="text-[#94A3B8]">Batch No:</span>
                <span className="font-mono text-white">{selectedLot}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94A3B8]">Mfg Date:</span>
                <span className="text-white">August 2026</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94A3B8]">Expiry Date:</span>
                <span className="text-white">July 2028</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94A3B8]">Heavy Metals:</span>
                <span className="text-emerald-400 font-bold">Passed (ICP-MS)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94A3B8]">Microbial Limit:</span>
                <span className="text-emerald-400 font-bold">Passed (USP 61/62)</span>
              </div>
            </div>
            <Link href="/website/cart?add=manivital-pro" className="w-full py-3 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold text-center block text-xs mt-3">
              Add to Cart (₹ 1,450)
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
