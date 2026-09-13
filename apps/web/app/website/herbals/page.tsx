"use client";

import React, { useState } from "react";
import Link from "next/link";
import { PRODUCTS_CATALOG, RegulatoryCategory } from "@/lib/cms/productsData";

// Canonical Portfolio Index
const CANONICAL_HERBALS_CATALOG = [
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

export default function ProductsHerbalsPage() {
  const [selectedCategory, setSelectedCategory] = useState<RegulatoryCategory | "All">("All");
  const [searchQuery, setSearchQuery] = useState("");

  const regulatoryCategories: (RegulatoryCategory | "All")[] = [
    "All",
    "Clinic-Prescribed Unani Formulation",
    "AYUSH-Licensed Botanical Preparation",
    "Retail Wellness Unani Formulation",
    "FSSAI Dietary & Nutraceutical Supplement"
  ];

  const filteredProducts = PRODUCTS_CATALOG.filter((prod) => {
    const matchesCategory = selectedCategory === "All" || prod.regulatoryCategory === selectedCategory;
    const matchesSearch = searchQuery.trim() === "" ||
      prod.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      prod.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      prod.intendedUse.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12 space-y-10 text-[#CBD5E1]">
      
      {/* Header */}
      <div className="border-b border-[#1E293B] pb-8 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold">
          <span>🌿</span> Pharmacopoeial Purity & HPLC Standardized
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          ZAYVORA Standardized Formulations
        </h1>
        <p className="text-sm text-[#94A3B8] max-w-3xl leading-relaxed">
          Statutory Unani botanical preparations manufactured under strict GMP conditions at the Jamia Hamdard AUTC cleanroom facility. Separated cleanly into clinical prescription formulations, classical retail preparations, and licensed nutraceuticals.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 rounded-2xl bg-[#0F172A] border border-[#334155]">
        <div className="flex flex-wrap gap-2">
          {regulatoryCategories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition ${
                selectedCategory === cat
                  ? "bg-[#0D9488] text-white"
                  : "bg-[#1E293B] text-[#94A3B8] hover:text-white"
              }`}
            >
              {cat === "All" ? "All Formulations" : cat.replace(" Preparation", "").replace(" Formulation", "")}
            </button>
          ))}
        </div>

        <div className="relative w-full md:w-64">
          <span className="absolute left-3 top-2.5 text-xs text-[#64748B]">🔍</span>
          <input
            placeholder="Search active herbs or products..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-8 pr-4 py-2 rounded-xl bg-[#1E293B] border border-[#334155] text-xs text-white placeholder-[#64748B] focus:outline-none focus:border-[#0D9488]"
          />
        </div>
      </div>

      {/* Regulatory Notice Banner */}
      <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs leading-relaxed flex items-center gap-3">
        <span className="text-lg shrink-0">⚠️</span>
        <div>
          <strong>Statutory Compliance Notice:</strong> Formulations marked as <span className="font-bold underline">Clinic-Prescribed</span> contain potent or mineral extracts purified via Mudabbar protocols and require physician review before dispensing under 21 CFR Part 11 regulations.
        </div>
      </div>

      {/* Product Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProducts.map((prod) => (
          <div
            key={prod.id}
            className="rounded-3xl bg-[#0F172A] border border-[#334155] p-6 space-y-5 hover:border-[#0D9488] transition flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded ${
                  prod.consultBeforeUseRequired
                    ? "bg-amber-500/20 text-amber-300 border border-amber-500/30"
                    : "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                }`}>
                  {prod.consultBeforeUseRequired ? "Prescription Only" : "Direct Order Available"}
                </span>
                <span className="text-sm font-extrabold text-white font-mono">{prod.currency}{prod.price}</span>
              </div>

              <div>
                <span className="text-[10px] text-[#64748B] font-semibold block">{prod.category}</span>
                <h3 className="text-lg font-bold text-white leading-snug mt-0.5">{prod.name}</h3>
              </div>

              <p className="text-xs text-[#94A3B8] leading-relaxed line-clamp-2">{prod.shortDescription}</p>

              <div className="p-3 rounded-2xl bg-[#0A0F1D] border border-[#1E293B] space-y-1 text-[11px]">
                <div className="flex justify-between text-[#94A3B8]">
                  <span>Batch:</span>
                  <span className="font-mono text-white">{prod.batchInfo.lotNumber}</span>
                </div>
                <div className="flex justify-between text-[#94A3B8]">
                  <span>Lead & Arsenic:</span>
                  <span className="text-emerald-400 font-semibold">{prod.batchInfo.leadPpm}</span>
                </div>
              </div>
            </div>

            <div className="pt-4 border-t border-[#1E293B] space-y-2">
              <div className="flex items-center justify-between text-[11px]">
                <span className="text-[#64748B]">{prod.size}</span>
                <span className="text-emerald-400 font-semibold">✓ In Stock ({prod.stockCount})</span>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <Link
                  href={`/website/product?id=${prod.id}`}
                  className="w-full text-center py-2.5 rounded-xl bg-[#1E293B] hover:bg-[#334155] text-xs font-semibold text-white transition"
                >
                  Monograph
                </Link>
                {prod.canBuyDirectly ? (
                  <Link
                    href={`/website/cart?add=${prod.id}`}
                    className="w-full text-center py-2.5 rounded-xl bg-[#0D9488] hover:bg-[#0F766E] text-xs font-bold text-white shadow-sm transition"
                  >
                    Add to Cart
                  </Link>
                ) : (
                  <Link
                    href="/website/book"
                    className="w-full text-center py-2.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/40 text-xs font-bold text-amber-300 transition"
                  >
                    Consult Doctor
                  </Link>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
