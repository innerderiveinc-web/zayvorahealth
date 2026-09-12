"use client";

import React from "react";
import Link from "next/link";

export default function ResearchPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">Research & Evidence Platform</h1>
        <p className="text-sm text-[#94A3B8]">Clinical Trials, Observational RWE, and Botanical Science</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-4">
    <h2 className="text-lg font-bold text-white">Evidence-Based Integrative Healthcare</h2>
    <p>
      ZAYVORA's academic research platform connects university medical centers, clinical investigator networks, and de-identified real-world evidence (RWE) registries to validate classical Greco-Arab therapeutic interventions.
    </p>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
      <div className="p-4 bg-[#0F172A] rounded-xl border border-[#334155]">
        <span className="font-bold text-white block">Study ZCT-2026-001</span>
        <p className="text-[#94A3B8] text-[11px] mt-1">Multi-center randomized concordance trial of 4-stage Afaal Cascade in Grade II Knee Osteoarthritis (94 enrolled subjects).</p>
      </div>
      <div className="p-4 bg-[#0F172A] rounded-xl border border-[#334155]">
        <span className="font-bold text-white block">WHO-UMC Pharmacovigilance</span>
        <p className="text-[#94A3B8] text-[11px] mt-1">ICH E2B electronic safety and adverse drug reaction reporting pipeline maintaining statutory compliance.</p>
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
