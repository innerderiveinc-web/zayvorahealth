"use client";

import React from "react";
import Link from "next/link";

export default function ServicesPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">Clinical Services & Specialties</h1>
        <p className="text-sm text-[#94A3B8]">Integrated In-Clinic and Virtual Care Delivery</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
    <div className="p-5 rounded-xl bg-[#1E293B] border border-[#334155] space-y-2">
      <h3 className="font-bold text-white text-sm">Integrative Outpatient Consultation</h3>
      <p className="text-[#94A3B8]">Comprehensive 45-minute clinical evaluation, 10-Ajnas Mizaj profiling, pulse examination, and dual biomedical diagnostic synthesis.</p>
    </div>
    <div className="p-5 rounded-xl bg-[#1E293B] border border-[#334155] space-y-2">
      <h3 className="font-bold text-white text-sm">Ilaj bil-Tadbeer (Regimenal Unit)</h3>
      <p className="text-[#94A3B8]">Supervised clinical regimens including Hijama (Cupping), Natool (Herbal irrigation), Zimad (Poultice), and Dalak Layyin (Therapeutic massage).</p>
    </div>
    <div className="p-5 rounded-xl bg-[#1E293B] border border-[#334155] space-y-2">
      <h3 className="font-bold text-white text-sm">Personalized Nuskha Dispensing</h3>
      <p className="text-[#94A3B8]">Custom compound compounding at our certified dispensary, sealed with 21 CFR Part 11 digital signatures and FEFO batch allocation.</p>
    </div>
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
