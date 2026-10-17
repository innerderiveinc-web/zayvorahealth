"use client";

import React from "react";
import Link from "next/link";

export default function Care_JourneyPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">Patient Care Journey</h1>
        <p className="text-sm text-[#94A3B8]">From 10-Ajnas Assessment to Long-Term Health Preservation</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="space-y-4">
    <div className="p-4 rounded-xl bg-[#1E293B] border-l-4 border-[#0D9488] space-y-1">
      <span className="font-bold text-white block">Step 1: Intake & 10-Ajnas Longitudinal Mizaj Evaluation</span>
      <p className="text-[#94A3B8]">Detailed assessment of skin tactile touch (*Malmas*), build, pulse (*Nabz*), sleep, and mental temperament.</p>
    </div>
    <div className="p-4 rounded-xl bg-[#1E293B] border-l-4 border-blue-500 space-y-1">
      <span className="font-bold text-white block">Step 2: Dual Tashkhees (Classical + Biomedical Assessment)</span>
      <p className="text-[#94A3B8]">Correlating Unani humoral dyscrasia with hs-CRP, CBC, ESR, and radiographic imaging.</p>
    </div>
    <div className="p-4 rounded-xl bg-[#1E293B] border-l-4 border-purple-500 space-y-1">
      <span className="font-bold text-white block">Step 3: 4-Stage Afaal Protocol & Digital Prescription</span>
      <p className="text-[#94A3B8]">Sequential progression (*Tanqiya* $\rightarrow$ *Tahleel* $\rightarrow$ *Taqwiyaat* $\rightarrow$ *Hifz*) sealed with 21 CFR Part 11 signature.</p>
    </div>
    <div className="p-4 rounded-xl bg-[#1E293B] border-l-4 border-amber-500 space-y-1">
      <span className="font-bold text-white block">Step 4: FEFO Dispensary Delivery & Mobile Audio Posology</span>
      <p className="text-[#94A3B8]">Verified Mudabbar compounds dispatched with vernacular voice instructions in Urdu, Hindi, and English.</p>
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
