"use client";

import React from "react";
import Link from "next/link";

export default function PortfolioPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">ZAYVORA Herbals Product Portfolio</h1>
        <p className="text-sm text-[#94A3B8]">Clinical Rationale and Evidence Classification</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-4">
    <p>The ZAYVORA Herbals Portfolio represents the golden standard of modern Unani phytomedicine:</p>
    <ul className="space-y-2 list-disc pl-5">
      <li><strong>ManiVital Pro:</strong> Male reproductive vitality formulation (Withania somnifera, Mucuna pruriens).</li>
      <li><strong>OvaSync:</strong> Ovarian rhythm and female vitality balancer (Asparagus racemosus).</li>
      <li><strong>Qurs-e-Taqwiyat-e-Mani:</strong> Classical seminal viscosity and reproductive tone formula.</li>
      <li><strong>MetaboCore Elite:</strong> Metabolic syndrome and glycemic regulator (Gymnema, Momordica).</li>
      <li><strong>ThyroMet Axis:</strong> Thyroid-metabolic optimization compound (Commiphora mukul).</li>
      <li><strong>LiverPrime Core:</strong> Hepatoprotective & bile flow regulator (Picrorhiza kurroa).</li>
      <li><strong>NeuroCalmX:</strong> GABAergic calm & mental resilience confection (Bacopa monnieri).</li>
      <li><strong>NightOne X:</strong> Circadian deep sleep restorer (Valeriana wallichii).</li>
      <li><strong>Sleep Stress Harmonizer:</strong> Nocturnal cortisol balancing formula.</li>
      <li><strong>Men Daily:</strong> Daily vitality micronutrient & adaptogenic tonic.</li>
    </ul>
    <Link href="/website/herbals" className="inline-block mt-3 px-5 py-2 rounded-xl bg-[#0D9488] text-white font-bold">
      Browse All Formulations in Store →
    </Link>
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
