"use client";

import React from "react";
import Link from "next/link";

export default function MatabPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">ZAYVORA Matab Clinics</h1>
        <p className="text-sm text-[#94A3B8]">Institutional Network of Integrated Healthcare Centres</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-4">
    <h2 className="text-lg font-bold text-white">Experience the Modern Matab</h2>
    <p>
      The classical Unani consultation room (*Matab*) is re-imagined as a modern, digital healthcare clinic equipped with acoustic ambient scribing, spectral quality validation labs, electronic vitals monitors, and an in-house FEFO herbal dispensary.
    </p>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
      <div className="p-4 bg-[#0F172A] rounded-xl border border-[#334155]">
        <span className="text-white font-bold block">Matab New Delhi Central</span>
        <span className="text-[#94A3B8] block text-[11px]">Connaught Place, Barakhamba Road</span>
        <span className="text-emerald-400 font-semibold block text-[10px] mt-2">● 4 Doctors on Roster</span>
      </div>
      <div className="p-4 bg-[#0F172A] rounded-xl border border-[#334155]">
        <span className="text-white font-bold block">Matab Jamia Hamdard Campus</span>
        <span className="text-[#94A3B8] block text-[11px]">Academic Integrative OPD Wing</span>
        <span className="text-emerald-400 font-semibold block text-[10px] mt-2">● Clinical Research Center</span>
      </div>
      <div className="p-4 bg-[#0F172A] rounded-xl border border-[#334155]">
        <span className="text-white font-bold block">Matab Mumbai South</span>
        <span className="text-[#94A3B8] block text-[11px]">Nariman Point Medical Hub</span>
        <span className="text-emerald-400 font-semibold block text-[10px] mt-2">● Virtual & In-Person OPD</span>
      </div>
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
