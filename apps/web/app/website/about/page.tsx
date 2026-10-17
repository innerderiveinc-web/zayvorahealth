"use client";

import React from "react";
import Link from "next/link";

export default function AboutPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">About ZAYVORA Health™</h1>
        <p className="text-sm text-[#94A3B8]">Ancient Wisdom. Modern Science. Intelligent Care.</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-4">
    <h2 className="text-lg font-bold text-white">Our Institutional Mission</h2>
    <p>
      ZAYVORA Health is an enterprise clinical operating system and integrative healthcare network dedicated to transforming traditional Unani Tibb into an evidence-based, digitally governed modern healthcare science.
    </p>
    <p>
      Grounded in the fundamental works of Avicenna (*Ibn Sina*) and Averroes (*Ibn Rushd*), ZAYVORA integrates 10-Ajnas longitudinal temperament (*Mizaj*) profiling, the 4-stage therapeutic cascade (*Afaal*), and physiological organ-axis cross-talk with contemporary clinical chemistry, FHIR R4 interoperability, and 21 CFR Part 11 cryptographic governance.
    </p>
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
