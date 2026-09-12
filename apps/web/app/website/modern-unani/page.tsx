"use client";

import React from "react";
import Link from "next/link";

export default function Modern_UnaniPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">Modern Unani Care System</h1>
        <p className="text-sm text-[#94A3B8]">Bridging Classical Codification with Digital Informatics</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-4">
    <h2 className="text-lg font-bold text-white">How Modern Unani Differs from Folk Herbalism</h2>
    <p>
      Modern Unani is not folk remedies or random plant mixtures. It is a systematic, codified clinical science governed by statutory pharmacopoeias (Unani Pharmacopoeia of India, NFUM) and modern analytical chemistry:
    </p>
    <ul className="space-y-2 list-disc pl-5">
      <li><strong>HPTLC / HPLC Fingerprinting:</strong> Every botanical lot is chemically fingerprinted for active phytocompounds (e.g. colchicine in Suranjan, withanolides in Asgandh).</li>
      <li><strong>Standardized Mudabbar Detoxification:</strong> Schedule E(1) toxic herbs undergo classical detox regimens verified by analytical Certificate of Analysis (CoA).</li>
      <li><strong>Dual Diagnostics:</strong> Clinical encounters correlate classical *Nabz* (pulse) and *Lisan* (tongue) findings with modern hs-CRP, ESR, HbA1c, and radiologic imaging.</li>
    </ul>
  </div>

      </div>

      <div className="pt-8 border-t border-[#334155] flex justify-between items-center">
        <Link href="/website" className="text-xs font-semibold text-[#94A3B8] hover:text-white">
          ← Back to Home
        </Link>
        <Link href="/website/book" className="px-5 py-2 rounded-xl bg-[#0D9488] text-white font-bold hover:bg-[#14B8A6]">
          Book Consultation →
        </Link>
      </div>
    </div>
  );
}
