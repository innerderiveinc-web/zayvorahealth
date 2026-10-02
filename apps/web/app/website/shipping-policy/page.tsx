"use client";

import React from "react";
import Link from "next/link";

export default function ShippingPolicyPage() {
  return (
    <div className="min-h-screen bg-[#0A101D] text-slate-100 py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-10">
        
        <div className="border-b border-slate-800 pb-6 space-y-3">
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <Link href="/website" className="hover:text-teal-400 transition">ZAYVORA Health</Link>
            <span>/</span>
            <span className="text-teal-400 font-medium">Logistics & Supply</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Shipping & Dispensary Delivery Policy
          </h1>
          <p className="text-xs text-slate-400 font-mono">
            AYUSH Cold-Chain Standards • Last Updated: September 2026
          </p>
        </div>

        <div className="space-y-8 text-xs sm:text-sm text-slate-300 leading-relaxed">
          
          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">1. Dispensary Fulfillment & Dispatch</h2>
            <p>
              Prescriptions approved by ZAYVORA Health clinicians are verified and dispensed directly from our centralized central hospital pharmacy at ZAYVORA Central Pharmacy, New Delhi. Formulations requiring fresh preparation (Mudabbar detoxification, bespoke Safoof blending) are dispatched within 24 hours of physician lock.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">2. Shipping Durations & Coverage</h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-1 text-xs">
                <span className="font-bold text-teal-400 block">Delhi NCR & Metros</span>
                <p className="text-white font-semibold">24 to 48 Hours</p>
                <p className="text-[11px] text-slate-400">Priority expedited cold-chain dispatch.</p>
              </div>
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-1 text-xs">
                <span className="font-bold text-teal-400 block">Tier 1 & Tier 2 Cities</span>
                <p className="text-white font-semibold">2 to 4 Business Days</p>
                <p className="text-[11px] text-slate-400">Direct courier with live airway tracking.</p>
              </div>
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-1 text-xs">
                <span className="font-bold text-teal-400 block">Rest of India / Remote</span>
                <p className="text-white font-semibold">4 to 7 Business Days</p>
                <p className="text-[11px] text-slate-400">Insulated protective packaging.</p>
              </div>
            </div>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">3. Cold-Chain & Tamper-Evident Packaging</h2>
            <p>
              Herbal syrups, roghaniyat (oils), and fermented formulations (Khamiras) are packed in multi-layered, temperature-buffered containers to ensure active phytochemical integrity remains unaffected during transit across extreme weather conditions.
            </p>
          </section>

        </div>

        <div className="pt-8 border-t border-slate-800 flex justify-between items-center text-xs">
          <Link href="/website" className="text-teal-400 hover:underline">
            ← Return to Homepage
          </Link>
          <Link href="/website/herbals" className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition">
            Explore Botanical Formulations →
          </Link>
        </div>

      </div>
    </div>
  );
}
