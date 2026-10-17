"use client";

import React from "react";
import Link from "next/link";

export default function BlogPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">Clinical Articles & Health Insights</h1>
        <p className="text-sm text-[#94A3B8]">Written by Licensed Senior Tabeebs and Medical Scientists</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="space-y-4">
    <div className="p-5 rounded-xl bg-[#1E293B] border border-[#334155] space-y-2">
      <span className="text-[10px] text-emerald-400 font-mono">SEPTEMBER 10, 2026 • CLINICAL PROTOCOL</span>
      <h3 className="font-bold text-white text-base">The Science of Mudabbar: Detoxification Chemistry of Toxic Botanical Alkaloids</h3>
      <p className="text-[#94A3B8]">How classical boiling in milk and sour wine resolves colchicine toxicity in Colchicum luteum without blunting anti-inflammatory efficacy.</p>
    </div>
    <div className="p-5 rounded-xl bg-[#1E293B] border border-[#334155] space-y-2">
      <span className="text-[10px] text-blue-400 font-mono">AUGUST 28, 2026 • RESEARCH REVIEW</span>
      <h3 className="font-bold text-white text-base">Organ-Axis Cross-Talk: The Gut-Joint Reflex in Balghami Arthralgia</h3>
      <p className="text-[#94A3B8]">Analyzing how cold dyscrasia in the gastric mucosa alters synovial fluid viscosity and prompts micro-crystallization.</p>
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
