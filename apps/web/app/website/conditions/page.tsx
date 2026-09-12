"use client";

import React from "react";
import Link from "next/link";

export default function ConditionsPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">Conditions & Care Areas</h1>
        <p className="text-sm text-[#94A3B8]">Evidence-Guided Clinical Pathways</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="space-y-4">
    <p>Our clinical protocols are codified across 6 core therapeutic areas:</p>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="p-4 rounded-xl bg-[#1E293B] border border-[#334155]">
        <h4 className="font-bold text-emerald-400">Waja-ul-Mafasil (Joint Osteoarthritis)</h4>
        <p className="text-[#94A3B8] mt-1">4-Stage Afaal Cascade: Tanqiya $\rightarrow$ Tahleel with Majun Suranjan Mudabbar $\rightarrow$ Taqwiyaat $\rightarrow$ Hifz.</p>
      </div>
      <div className="p-4 rounded-xl bg-[#1E293B] border border-[#334155]">
        <h4 className="font-bold text-blue-400">Ziabetes & Dyskrasia (Metabolic Disorders)</h4>
        <p className="text-[#94A3B8] mt-1">Insulin sensitizing Tadbeer, Safoof-e-Ziabetes, hepatic enzyme regulation, and low-glycemic dietary parhez.</p>
      </div>
      <div className="p-4 rounded-xl bg-[#1E293B] border border-[#334155]">
        <h4 className="font-bold text-purple-400">Su-e-Hazm & Kabid (Gastro-Hepatic Axis)</h4>
        <p className="text-[#94A3B8] mt-1">Hepatoprotective confections, gastric tone restoration (*Muqawwi-e-Meda*), and gut dysbiosis cleansing.</p>
      </div>
      <div className="p-4 rounded-xl bg-[#1E293B] border border-[#334155]">
        <h4 className="font-bold text-amber-400">Zof-e-Bah & Uqr (Fertility & Vitality)</h4>
        <p className="text-[#94A3B8] mt-1">Male and female reproductive axis tonification, semen viscosity optimization (*Mughalliz-e-Mani*), hormonal balance.</p>
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
