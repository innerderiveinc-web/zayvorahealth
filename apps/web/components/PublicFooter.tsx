"use client";

import React, { useState } from "react";
import Link from "next/link";

export function PublicFooter() {
  const [lang, setLang] = useState<"EN" | "HI" | "UR">("EN");

  return (
    <footer className="bg-[#070B14] border-t border-[#1E293B] text-xs text-[#94A3B8]">
      {/* Upper Footer Columns */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-14">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 lg:gap-10">
          
          {/* COLUMN 1: ZAYVORA */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-[#0D9488]/20 border border-[#0D9488]/40 flex items-center justify-center p-0.5">
                <img src="/zayvora-logo.png" alt="ZAYVORA" className="w-full h-full object-contain" onError={(e) => { (e.target as HTMLElement).style.display = "none"; }} />
              </div>
              <span className="font-bold text-white text-base tracking-tight">ZAYVORA Health™</span>
            </div>
            <p className="text-[11px] text-[#64748B] leading-relaxed">
              Modern Unani Care System combining classical Greco-Arab medical science with contemporary clinical diagnostics, personalized constitutional assessment, and clinician-supervised care pathways.
            </p>
            <div className="space-y-1.5 pt-1">
              <span className="text-[10px] font-bold text-white uppercase tracking-wider block">Organization</span>
              <ul className="space-y-1 text-[11px]">
                <li><Link href="/website/about" className="hover:text-white transition">About ZAYVORA</Link></li>
                <li><Link href="/website/philosophy" className="hover:text-white transition">Our Philosophy</Link></li>
                <li><Link href="/website/doctors" className="hover:text-white transition">Clinical Team</Link></li>
                <li><Link href="/website/contact" className="hover:text-white transition">Contact Us</Link></li>
                <li><Link href="/website/careers" className="hover:text-white transition">Careers</Link></li>
              </ul>
            </div>
          </div>

          {/* COLUMN 2: CARE */}
          <div className="space-y-3">
            <span className="font-bold text-white uppercase tracking-wider text-[11px] block">
              Clinical Care
            </span>
            <ul className="space-y-2 text-[11px]">
              <li><Link href="/website/programs" className="hover:text-white transition">Health Programs</Link></li>
              <li><Link href="/website/book" className="hover:text-white transition text-[#2DD4BF] font-semibold">Book Consultation</Link></li>
              <li><Link href="/patient/login" className="hover:text-white transition">Patient Login</Link></li>
              <li><Link href="/website/care-journey" className="hover:text-white transition">Consultation Process</Link></li>
              <li><Link href="/website/services" className="hover:text-white transition">Follow-up Care</Link></li>
              <li><Link href="/website/faqs" className="hover:text-white transition">Frequently Asked Questions</Link></li>
            </ul>
          </div>

          {/* COLUMN 3: PRODUCTS */}
          <div className="space-y-3">
            <span className="font-bold text-white uppercase tracking-wider text-[11px] block">
              Formulations & Store
            </span>
            <ul className="space-y-2 text-[11px]">
              <li><Link href="/website/herbals" className="hover:text-white transition">All Products</Link></li>
              <li><Link href="/website/product?id=manivital-pro" className="hover:text-white transition">Male Reproductive Wellness</Link></li>
              <li><Link href="/website/product?id=ovasync" className="hover:text-white transition">Female Hormonal Balance</Link></li>
              <li><Link href="/website/product?id=metabocore-elite" className="hover:text-white transition">Metabolic Support</Link></li>
              <li><Link href="/website/product?id=liverprime-core" className="hover:text-white transition">Gut & Liver Support</Link></li>
              <li><Link href="/website/product?id=nightone-x" className="hover:text-white transition">Sleep & Stress Support</Link></li>
            </ul>
          </div>

          {/* COLUMN 4: RESOURCES */}
          <div className="space-y-3">
            <span className="font-bold text-white uppercase tracking-wider text-[11px] block">
              Knowledge & Insights
            </span>
            <ul className="space-y-2 text-[11px]">
              <li><Link href="/website/knowledge-centre" className="hover:text-white transition">Knowledge Center</Link></li>
              <li><Link href="/website/blog" className="hover:text-white transition">Health Articles</Link></li>
              <li><Link href="/website/modern-unani" className="hover:text-white transition">Unani Education</Link></li>
              <li><Link href="/website/research" className="hover:text-white transition">Clinical Insights & Trials</Link></li>
              <li><Link href="/patient" className="hover:text-white transition">Patient Resources</Link></li>
            </ul>
          </div>

          {/* COLUMN 5: LEGAL & GOVERNANCE */}
          <div className="space-y-3">
            <span className="font-bold text-white uppercase tracking-wider text-[11px] block">
              Legal & Trust
            </span>
            <ul className="space-y-2 text-[11px]">
              <li><Link href="/website/privacy" className="hover:text-white transition">Privacy Policy</Link></li>
              <li><Link href="/website/terms" className="hover:text-white transition">Terms of Service</Link></li>
              <li><Link href="/website/medical-disclaimer" className="hover:text-white transition">Medical Disclaimer</Link></li>
              <li><Link href="/website/refund-policy" className="hover:text-white transition">Refund Policy</Link></li>
              <li><Link href="/website/shipping-policy" className="hover:text-white transition">Shipping Policy</Link></li>
              <li><Link href="/admin" className="hover:text-white transition">Data Protection (HIPAA & ABDM)</Link></li>
              <li><Link href="/website/accessibility" className="hover:text-white transition">Accessibility Statement</Link></li>
            </ul>
          </div>

        </div>

        {/* CLINICAL CONTACT & LOCATION BLOCK */}
        <div className="mt-12 pt-8 border-t border-[#1E293B] grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="space-y-1">
            <span className="text-[11px] font-bold text-white uppercase tracking-wider block">Central Hospital Facility</span>
            <p className="text-[11px] text-[#64748B] leading-relaxed">
              Jamia Hamdard AUTC - Main Hospital<br />
              Mehrauli - Badarpur Rd, Near Batra Hospital, Hamdard Nagar<br />
              New Delhi, Delhi 110062, India
            </p>
          </div>
          <div className="space-y-1">
            <span className="text-[11px] font-bold text-white uppercase tracking-wider block">Care Coordination & Appointments</span>
            <p className="text-[11px] text-[#64748B]">
              <strong>Helpline:</strong> +91 11 2605 9688<br />
              <strong>WhatsApp Support:</strong> +91 98110 44219<br />
              <strong>Patient Care Email:</strong> care@zayvora.com
            </p>
          </div>
          <div className="space-y-1">
            <span className="text-[11px] font-bold text-white uppercase tracking-wider block">OPD & Dispensary Timings</span>
            <p className="text-[11px] text-[#64748B]">
              <strong>Monday – Saturday:</strong> 09:00 AM – 06:00 PM IST<br />
              <strong>Sunday:</strong> Closed (Emergency Triage Only)<br />
              <strong>Dispensary:</strong> 24/7 Automated FEFO Batch Dispatch
            </p>
          </div>
        </div>

        {/* STATUTORY MEDICAL DISCLAIMER NOTICE */}
        <div className="mt-8 p-4 rounded-2xl bg-[#0D1527] border border-[#1E293B] text-[11px] text-[#64748B] leading-relaxed">
          <strong className="text-[#94A3B8] block mb-1">Important Medical Disclaimer:</strong>
          The information, health programs, and botanical formulations provided on this website are for educational and personalized supportive health management under qualified clinical supervision. They are not intended as an autonomous substitute for acute emergency medical care. Consult a licensed physician or registered Tabeeb before initiating any new health program or changing medications.
        </div>

        {/* BOTTOM COPYRIGHT & COMPLIANCE BAR */}
        <div className="mt-8 pt-6 border-t border-[#1E293B] flex flex-col md:flex-row items-center justify-between gap-4 text-[11px] text-[#64748B]">
          <div className="flex flex-wrap items-center gap-3">
            <span>© 2026 ZAYVORA Health. All rights reserved.</span>
            <span>•</span>
            <span className="text-[#0D9488] font-semibold">Modern Unani Care System</span>
            <span>•</span>
            <span>Website Version 5.0.0</span>
          </div>

          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5 text-emerald-400 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              All Systems Operational
            </span>
            <div className="flex items-center bg-[#0F172A] rounded-lg border border-[#334155] p-0.5 text-[10px] font-bold">
              {(["EN", "HI", "UR"] as const).map((l) => (
                <button
                  key={l}
                  onClick={() => setLang(l)}
                  className={`px-2 py-0.5 rounded transition ${
                    lang === l ? "bg-[#0D9488] text-white" : "text-[#94A3B8] hover:text-white"
                  }`}
                >
                  {l}
                </button>
              ))}
            </div>
          </div>
        </div>

      </div>
    </footer>
  );
}
