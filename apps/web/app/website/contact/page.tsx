"use client";

import React from "react";
import Link from "next/link";

export default function ContactPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">Contact ZAYVORA Health</h1>
        <p className="text-sm text-[#94A3B8]">Clinics, Inquiries, and Emergency Coordination</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-4">
      <h3 className="font-bold text-white text-base">Clinical Headquarters</h3>
      <p className="text-[#94A3B8]">ZAYVORA Health Systems Inc.<br />Medical Enclave, Central Integrative Wing<br />New Delhi, 110001, India</p>
      <div className="space-y-1 text-[#CBD5E1]">
        <p><strong>Clinical OPD Helpline:</strong> +91 11 4982 0000</p>
        <p><strong>Dispensary Inquiries:</strong> pharmacy@zayvora.health</p>
        <p><strong>Clinical Research:</strong> trials@zayvora.health</p>
      </div>
    </div>
    <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-4">
      <h3 className="font-bold text-white text-base">Send Clinical Inquiry</h3>
      <form className="space-y-3" onSubmit={(e) => { e.preventDefault(); alert("Inquiry transmitted to clinical triage."); }}>
        <input placeholder="Your Name" className="w-full px-3 py-2 rounded-lg bg-[#0F172A] border border-[#334155] text-white" required />
        <input placeholder="Email or Phone" className="w-full px-3 py-2 rounded-lg bg-[#0F172A] border border-[#334155] text-white" required />
        <textarea rows={3} placeholder="Inquiry details..." className="w-full p-3 rounded-lg bg-[#0F172A] border border-[#334155] text-white" required />
        <button type="submit" className="w-full py-2.5 rounded-xl bg-[#0D9488] text-white font-bold">Transmit Inquiry</button>
      </form>
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
