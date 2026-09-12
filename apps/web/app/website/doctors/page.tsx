"use client";

import React from "react";
import Link from "next/link";

export default function DoctorsPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">Licensed Practitioners & Tabeebs</h1>
        <p className="text-sm text-[#94A3B8]">Senior Faculty, Unani Physicians, and Researchers</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
      <div className="flex items-center gap-3">
        <div className="w-12 h-12 rounded-full bg-[#0D9488] flex items-center justify-center font-bold text-white text-base">TM</div>
        <div>
          <h3 className="font-bold text-white text-base">Hakim Dr. Tariq Mansoor</h3>
          <span className="text-[11px] text-[#2DD4BF] font-mono">CCIM-BUMS-2004-9841</span>
        </div>
      </div>
      <p className="text-[#94A3B8]">Senior Tabeeb with 22 years of clinical experience in Waja-ul-Mafasil, metabolic dyscrasia, and complex Nuskha formulation.</p>
      <Link href="/website/book" className="text-emerald-400 font-bold hover:underline inline-block text-xs">Book with Dr. Mansoor →</Link>
    </div>
    <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
      <div className="flex items-center gap-3">
        <div className="w-12 h-12 rounded-full bg-purple-600 flex items-center justify-center font-bold text-white text-base">AP</div>
        <div>
          <h3 className="font-bold text-white text-base">Dr. Asma Parveen</h3>
          <span className="text-[11px] text-purple-400 font-mono">CCIM-BUMS-2011-5420</span>
        </div>
      </div>
      <p className="text-[#94A3B8]">Specialist in female reproductive vitality (*Niswan*), ovarian reserve regulation, and Asbab Sittah lifestyle optimization.</p>
      <Link href="/website/book" className="text-purple-400 font-bold hover:underline inline-block text-xs">Book with Dr. Parveen →</Link>
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
