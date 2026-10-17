"use client";

import React, { useState, useEffect } from "react";

export default function Catalog16Page() {
  const [products, setProducts] = useState<any[]>([]);
  const [selectedTrack, setSelectedTrack] = useState<string>("ALL");
  const [selectedProduct, setSelectedProduct] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/v1/therapeutic/products-16/all")
      .then(r => r.json())
      .then(data => {
        if (data.ok) {
          setProducts(data.products);
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const filtered = selectedTrack === "ALL" 
    ? products 
    : products.filter(p => p.regulatory_track.includes(selectedTrack));

  return (
    <div className="min-h-screen bg-[#FAFAF7] p-8 text-neutral-900 font-sans">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="border-b border-neutral-200 pb-4">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2">
            <div>
              <span className="text-xs font-bold uppercase tracking-widest text-[#2D6A4F] bg-emerald-50 px-2.5 py-1 rounded">
                ZAYVORA Health OS™ · Volume II Pharmacopoeia
              </span>
              <h1 className="text-3xl font-serif font-bold text-neutral-900 mt-2">
                16 Core Standardized Product Matrix
              </h1>
              <p className="text-xs text-neutral-500 mt-1">
                Dual-Track Architecture: AYUSH Track A (Schedule T GMP) & FSSAI Track B (Nutraceutical)
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setSelectedTrack("ALL")}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border ${
                  selectedTrack === "ALL" ? "bg-[#2D6A4F] text-white border-[#2D6A4F]" : "bg-white text-neutral-700"
                }`}
              >
                All 16 Products
              </button>
              <button
                onClick={() => setSelectedTrack("AYUSH")}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border ${
                  selectedTrack === "AYUSH" ? "bg-[#2D6A4F] text-white border-[#2D6A4F]" : "bg-white text-neutral-700"
                }`}
              >
                AYUSH Track A
              </button>
              <button
                onClick={() => setSelectedTrack("FSSAI")}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border ${
                  selectedTrack === "FSSAI" ? "bg-[#2D6A4F] text-white border-[#2D6A4F]" : "bg-white text-neutral-700"
                }`}
              >
                FSSAI Track B
              </button>
            </div>
          </div>
        </div>

        {/* 16-Product Grid */}
        {loading ? (
          <div className="text-center py-12 text-neutral-400 font-serif">Loading 16 Core Product Matrix...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filtered.map((prod) => {
              const isAyush = prod.regulatory_track.includes("AYUSH");
              return (
                <div
                  key={prod.product_id}
                  onClick={() => setSelectedProduct(prod)}
                  className="bg-white p-5 rounded-xl border border-neutral-200 shadow-sm hover:border-[#2D6A4F] hover:shadow-md cursor-pointer transition-all flex flex-col justify-between"
                >
                  <div>
                    <div className="flex justify-between items-start gap-1">
                      <span className="text-[10px] font-mono font-bold text-neutral-400">
                        {prod.internal_code}
                      </span>
                      <span
                        className={`text-[9px] font-bold px-2 py-0.5 rounded border ${
                          isAyush
                            ? "bg-emerald-50 text-emerald-800 border-emerald-200"
                            : "bg-blue-50 text-blue-800 border-blue-200"
                        }`}
                      >
                        {isAyush ? "AYUSH Track A" : "FSSAI Track B"}
                      </span>
                    </div>

                    <h3 className="font-serif font-bold text-base text-neutral-900 mt-2 line-clamp-2">
                      {prod.name}
                    </h3>
                    <p className="text-xs text-[#2D6A4F] font-medium mt-0.5">
                      {prod.clinical_axis}
                    </p>

                    <div className="mt-3 text-xs bg-neutral-50 p-2.5 rounded border border-neutral-100 text-neutral-600 space-y-1">
                      <div><strong className="text-neutral-700">Parent Nuskha:</strong> {prod.parent_nuskha_code}</div>
                      <div className="italic text-[11px] truncate">{prod.parent_nuskha_name}</div>
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-neutral-100 flex items-center justify-between">
                    <span className="text-xs text-neutral-500">{prod.dosage_form}</span>
                    <span className="font-bold text-sm text-neutral-900">₹{prod.mrp_target_inr}</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Product Detail Modal */}
        {selectedProduct && (
          <div className="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl max-w-2xl w-full p-6 space-y-4 shadow-xl max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-start border-b pb-3">
                <div>
                  <span className="text-xs font-bold text-[#2D6A4F] bg-emerald-50 px-2 py-0.5 rounded">
                    {selectedProduct.regulatory_track}
                  </span>
                  <h2 className="text-xl font-serif font-bold text-neutral-900 mt-1">
                    {selectedProduct.name}
                  </h2>
                  <p className="text-xs text-neutral-500">
                    Parent Classical Formula: <strong className="text-neutral-800">{selectedProduct.parent_nuskha_name} ({selectedProduct.parent_nuskha_code})</strong>
                  </p>
                </div>
                <button
                  onClick={() => setSelectedProduct(null)}
                  className="text-neutral-400 hover:text-neutral-800 text-xl font-bold px-2"
                >
                  ✕
                </button>
              </div>

              {/* Composition Breakdown: 80% Classical Core + 20% Modern Layer */}
              <div className="space-y-3 text-xs">
                <div className="p-3 bg-neutral-50 rounded-lg border border-neutral-200">
                  <h4 className="font-bold uppercase tracking-wider text-[#1B4332] mb-1.5">
                    Classical Core (80% Therapeutic Action)
                  </h4>
                  <ul className="space-y-1">
                    {selectedProduct.classical_core_80.map((c: any, idx: number) => (
                      <li key={idx} className="flex justify-between text-neutral-700">
                        <span><strong>{c.ingredient}</strong> ({c.standardisation})</span>
                        <span className="font-mono text-neutral-900 font-medium">{c.mg_per_cap} mg</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="p-3 bg-blue-50/50 rounded-lg border border-blue-200">
                  <h4 className="font-bold uppercase tracking-wider text-blue-900 mb-1.5">
                    Modern Bioactive Layer (20% Mechanistic Gap Fillers)
                  </h4>
                  <ul className="space-y-1">
                    {selectedProduct.modern_layer_20.map((m: any, idx: number) => (
                      <li key={idx} className="flex justify-between text-neutral-700">
                        <span><strong>{m.ingredient}</strong> <span className="text-neutral-500 text-[10px]">({m.purpose})</span></span>
                        <span className="font-mono text-neutral-900 font-medium">{m.mg_per_cap ? `${m.mg_per_cap} mg` : (m.mcg_per_cap ? `${m.mcg_per_cap} mcg` : `${m.IU_per_cap} IU`)}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="space-y-2 pt-2 border-t">
                  <div>
                    <strong className="text-neutral-800">Prescription Dose:</strong>
                    <p className="text-neutral-600 mt-0.5">{selectedProduct.daily_dose}</p>
                  </div>
                  <div>
                    <strong className="text-emerald-800">Permitted Structure-Function Claim (Green Zone):</strong>
                    <p className="text-emerald-900 bg-emerald-50 p-2 rounded border border-emerald-200 mt-0.5">
                      {selectedProduct.permitted_claim_green_zone}
                    </p>
                  </div>
                  <div>
                    <strong className="text-red-800">Prohibited Curative Claim (Red Zone - DMR Act 1954):</strong>
                    <p className="text-red-900 bg-red-50 p-2 rounded border border-red-200 mt-0.5">
                      {selectedProduct.prohibited_claim_red_zone}
                    </p>
                  </div>
                </div>
              </div>

              <div className="pt-2 border-t flex justify-between items-center text-xs">
                <span className="font-bold text-neutral-800 text-sm">MRP: ₹{selectedProduct.mrp_target_inr}</span>
                <button
                  onClick={() => setSelectedProduct(null)}
                  className="bg-[#2D6A4F] text-white px-4 py-1.5 rounded-lg hover:bg-[#1B4332]"
                >
                  Close Specification
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
