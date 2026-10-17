"use client";

import React from "react";
import Link from "next/link";

export default function Shipping_RefundsPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">Dispensary Courier & Refund Policy</h1>
        <p className="text-sm text-[#94A3B8]">FEFO Temperature-Controlled Fulfillment</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-4">
    <p>Prescribed compounds and ZAYVORA Herbals are dispatched via temperature-controlled courier within 24 hours of verified pharmacist sign-off. Unopened, tamper-sealed botanicals may be returned within 14 days.</p>
  </div>

      </div>

      <div className="pt-8 border-t border-[#334155] flex justify-between items-center">
        <Link href="/website" className="text-xs font-semibold text-[#94A3B8] hover:text-white">
          ← Back to Home
        </Link>
        <Link href="/contact" className="px-5 py-2 rounded-xl bg-[#0D9488] text-white font-bold hover:bg-[#14B8A6]">
          Book Consultation →
        </Link>
      </div>
    </div>
  );
}
