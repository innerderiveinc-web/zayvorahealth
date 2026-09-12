"use client";

import React from "react";
import Link from "next/link";

export default function BookPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">Book Integrative Consultation</h1>
        <p className="text-sm text-[#94A3B8]">Schedule In-Person or Tele-Health Clinical Encounter</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-4">
    <form className="space-y-4" onSubmit={(e) => { e.preventDefault(); alert("Appointment booked successfully! Token T-104 assigned."); }}>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-[#94A3B8] mb-1">Full Name</label>
          <input defaultValue="Hamza Farooqi" className="w-full px-3 py-2 rounded-lg bg-[#0F172A] border border-[#334155] text-white" required />
        </div>
        <div>
          <label className="block text-[#94A3B8] mb-1">Contact Phone</label>
          <input defaultValue="+91-9876543210" className="w-full px-3 py-2 rounded-lg bg-[#0F172A] border border-[#334155] text-white" required />
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-[#94A3B8] mb-1">Select Specialty / Condition</label>
          <select className="w-full px-3 py-2 rounded-lg bg-[#0F172A] border border-[#334155] text-white">
            <option>Waja-ul-Mafasil (Joint & Knee Pain)</option>
            <option>Metabolic & Diabetes Care</option>
            <option>Liver & Gastrointestinal</option>
            <option>Reproductive Health & Fertility</option>
            <option>Chronic Fatigue & Stress</option>
          </select>
        </div>
        <div>
          <label className="block text-[#94A3B8] mb-1">Preferred Date</label>
          <input type="date" defaultValue="2026-09-15" className="w-full px-3 py-2 rounded-lg bg-[#0F172A] border border-[#334155] text-white" />
        </div>
      </div>
      <div>
        <label className="block text-[#94A3B8] mb-1">Chief Symptoms & Notes</label>
        <textarea rows={3} defaultValue="Bilateral knee aching and morning stiffness for past 3 weeks." className="w-full p-3 rounded-lg bg-[#0F172A] border border-[#334155] text-white" />
      </div>
      <button type="submit" className="w-full py-3 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold text-sm transition">
        Confirm Appointment & Generate Queue Token
      </button>
    </form>
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
