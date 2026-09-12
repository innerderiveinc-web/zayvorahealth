"use client";

import React from "react";
import Link from "next/link";

export default function ClinicsPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">Find a ZAYVORA Clinic</h1>
        <p className="text-sm text-[#94A3B8]">Locate Certified Matabs and Partner Healthcare Facilities</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-4">
    <div className="flex gap-3">
      <input placeholder="Enter city, pin code, or locality..." className="flex-1 px-4 py-2.5 rounded-xl bg-[#0F172A] border border-[#334155] text-white text-xs" />
      <button className="px-5 py-2.5 rounded-xl bg-[#0D9488] text-white font-bold text-xs">Search Clinics</button>
    </div>
    <div className="p-4 bg-[#0F172A] rounded-xl border border-[#334155] space-y-2">
      <div className="flex justify-between items-center">
        <h4 className="font-bold text-white text-sm">Central Integrative Clinical Facility (FAC-CENTRAL)</h4>
        <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-[10px]">Active OPD</span>
      </div>
      <p className="text-[#94A3B8]">14 Outpatient Consultations Today • Lead: Hakim Dr. Tariq Mansoor • Central Dispensary Onsite</p>
      <Link href="/website/book" className="text-emerald-400 font-bold hover:underline inline-block mt-1">Book at this Facility →</Link>
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
