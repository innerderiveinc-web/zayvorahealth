"use client";

import React, { useState } from "react";
import Link from "next/link";

const PRODUCTS = [
  { id: "manivital-pro", name: "ManiVital Pro", category: "Fertility", price: "₹1,450", chiefDrug: "Withania somnifera & Mucuna pruriens", indication: "Spermatogenic vitality & reproductive vigor", mudabbar: false, sku: "ZY-FERT-001" },
  { id: "ovasync", name: "OvaSync", category: "Fertility", price: "₹1,380", chiefDrug: "Asparagus racemosus & Saraca asoca", indication: "Ovarian cycle harmonization & follicular health", mudabbar: false, sku: "ZY-FERT-002" },
  { id: "qurs-taqwiyat-mani", name: "Qurs-e-Taqwiyat-e-Mani", category: "Fertility", price: "₹980", chiefDrug: "Salep & Behman Surkh", indication: "Classical seminal viscosity & reproductive tone", mudabbar: false, sku: "ZY-FERT-003" },
  { id: "metabocore-elite", name: "MetaboCore Elite", category: "Metabolic", price: "₹1,250", chiefDrug: "Gymnema sylvestre & Momordica charantia", indication: "Glucose metabolism & insulin sensitivity", mudabbar: false, sku: "ZY-META-001" },
  { id: "thyromet-axis", name: "ThyroMet Axis", category: "Metabolic", price: "₹1,350", chiefDrug: "Commiphora mukul & Bauhinia variegata", indication: "Thyroid-metabolic optimization", mudabbar: false, sku: "ZY-META-002" },
  { id: "liverprime-core", name: "LiverPrime Core", category: "Liver & Gut", price: "₹1,150", chiefDrug: "Picrorhiza kurroa & Cichorium intybus", indication: "Hepatobiliary protection & bile flow regulation", mudabbar: false, sku: "ZY-LIV-001" },
  { id: "neurocalmx", name: "NeuroCalmX", category: "Calm & Sleep", price: "₹1,200", chiefDrug: "Bacopa monnieri & Convolvulus pluricaulis", indication: "GABAergic calm & stress resilience", mudabbar: false, sku: "ZY-CALM-001" },
  { id: "nightone-x", name: "NightOne X", category: "Calm & Sleep", price: "₹1,320", chiefDrug: "Valeriana wallichii & Nardostachys jatamansi", indication: "Circadian rhythm restoration & restorative deep sleep", mudabbar: false, sku: "ZY-CALM-002" },
  { id: "sleep-stress", name: "Sleep Stress Harmonizer", category: "Calm & Sleep", price: "₹1,180", chiefDrug: "Withania somnifera & Matricaria chamomilla", indication: "Nocturnal cortisol normalization", mudabbar: false, sku: "ZY-CALM-003" },
  { id: "men-daily", name: "Men Daily Adaptogen", category: "Daily", price: "₹1,280", chiefDrug: "Tribulus terrestris & Asphaltum (Shilajit)", indication: "Daily micronutrient & vital adaptogen tonic", mudabbar: false, sku: "ZY-DAY-001" },
];

export default function HerbalsPage() {
  const [activeCategory, setActiveCategory] = useState("All");

  const filtered = activeCategory === "All" ? PRODUCTS : PRODUCTS.filter(p => p.category === activeCategory);

  return (
    <div className="max-w-7xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Herbals & Formulations</span>
          <h1 className="text-3xl md:text-4xl font-extrabold text-white mt-1">Product Portfolio & Botanical Store</h1>
          <p className="text-sm text-[#94A3B8]">10 Codified Classical & Proprietary AYUSH Formulations with Full CoA Batch Traceability.</p>
        </div>
        <Link href="/website/cart" className="px-5 py-2.5 rounded-xl bg-[#0D9488] text-white font-bold hover:bg-[#14B8A6] flex items-center gap-2">
          🛒 View Cart & Orders
        </Link>
      </div>

      {/* Category Pills */}
      <div className="flex flex-wrap gap-2">
        {["All", "Fertility", "Metabolic", "Liver & Gut", "Calm & Sleep", "Daily"].map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold transition ${activeCategory === cat ? "bg-[#0D9488] text-white" : "bg-[#1E293B] text-[#94A3B8] hover:text-white border border-[#334155]"}`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Product Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map((product) => (
          <div key={product.id} className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] flex flex-col justify-between space-y-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#0D9488]/20 text-[#2DD4BF] font-bold">
                  {product.category}
                </span>
                <span className="text-base font-bold text-white">{product.price}</span>
              </div>
              <h3 className="text-lg font-bold text-white">{product.name}</h3>
              <p className="text-[#94A3B8]">{product.indication}</p>
              <div className="pt-2 border-t border-[#334155] text-[11px] text-[#64748B]">
                <strong className="text-white">Chief Actives:</strong> {product.chiefDrug}
              </div>
            </div>

            <div className="pt-3 border-t border-[#334155] flex items-center justify-between">
              <Link href={`/website/product?id=${product.id}`} className="text-xs font-semibold text-[#2DD4BF] hover:underline">
                Clinical Monograph →
              </Link>
              <Link href={`/website/cart?add=${product.id}`} className="px-4 py-2 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold text-xs">
                + Add to Cart
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
