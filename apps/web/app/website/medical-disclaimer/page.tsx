"use client";

import React from "react";
import Link from "next/link";

export default function MedicalDisclaimerPage() {
  return (
    <div className="min-h-screen bg-[#0A101D] text-slate-100 py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-10">
        
        {/* Header */}
        <div className="border-b border-slate-800 pb-6 space-y-3">
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <Link href="/website" className="hover:text-teal-400 transition">ZAYVORA Health</Link>
            <span>/</span>
            <span className="text-teal-400 font-medium">Statutory Governance</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Medical & Clinical Disclaimer
          </h1>
          <p className="text-xs text-slate-400 font-mono">
            Last Updated: September 2026 • Statutory Compliance: AYUSH / NCISM / DPDP Act 2023
          </p>
        </div>

        {/* Content Body */}
        <div className="space-y-8 text-xs sm:text-sm text-slate-300 leading-relaxed">
          
          <div className="p-6 rounded-2xl bg-amber-950/30 border border-amber-800/60 text-amber-200 space-y-2">
            <h2 className="font-bold text-base flex items-center gap-2">
              <span>⚠️</span> Emergency Notice
            </h2>
            <p className="text-xs leading-relaxed text-amber-200/90">
              The services and content provided by ZAYVORA Health are <strong>not designed for acute medical emergencies</strong>. If you are experiencing chest pain, severe breathlessness, traumatic physical injury, sudden weakness or numbness, or any life-threatening symptoms, please immediately call national emergency number <strong>112</strong> or proceed to the nearest multi-specialty emergency trauma hospital.
            </p>
          </div>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">1. Nature of Medical Information</h2>
            <p>
              The articles, monographs, clinical program descriptions, video materials, and drug information published across ZAYVORA Health digital properties (including our website, mobile application, and educational portals) are intended strictly for educational, informational, and reference purposes. They are based upon classical Unani pharmacopeia (including the Unani Pharmacopoeia of India - UPI and National Formulary of Unani Medicine - NFUM) combined with contemporary peer-reviewed clinical research.
            </p>
            <p>
              No material on this platform is intended to substitute for direct clinical examination, individualized pulse (Nabz) diagnosis, physical palpatory assessment, or supervised prescription by a licensed practitioner of medicine.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">2. Clinician-Supervised Encounters</h2>
            <p>
              Consultations conducted through ZAYVORA Health (both in-person at Jamia Hamdard AUTC hospital OPD and through encrypted teleconsultation) are provided by qualified clinicians registered with the Central Council of Indian Medicine (CCIM) / National Commission for Indian System of Medicine (NCISM) or State AYUSH Councils.
            </p>
            <p>
              Recommendations, therapeutic regimens (Ilaj-bit-Tadbeer), and classical herbal dispensations are customized based on comprehensive personal assessment (Mizaj temperament, Su-e-Mizaj dystechnia, Asbab-e-Sittah lifestyle determinants, and concurrent biomedical laboratory reports). Self-medication or altering prescribed pharmaceutical dosages without attending clinician supervision is strictly advised against.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">3. Botanical Quality & Regulatory Approvals</h2>
            <p>
              All Unani proprietary and classical formulations showcased on ZAYVORA Health are manufactured in Good Manufacturing Practice (GMP) certified facilities licensed under Rule 158B of the Drugs & Cosmetics Act, 1940. Botanical ingredients undergo rigorous thin-layer chromatography (HPTLC), pesticide residue screening, aflatoxin validation, and heavy metal testing adhering to AYUSH safety standards.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">4. No Warranty of Outcome</h2>
            <p>
              Biological response to classical therapeutic regimens varies significantly across individual constitutional temperaments (Damawi, Balghami, Safrawi, Saudawi) and chronicity of conditions. While our clinical outcomes are validated in observational cohorts, ZAYVORA Health makes no claims of guaranteed cure or rapid symptomatic reversal.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">5. Contact & Clinical Oversight</h2>
            <p>
              For clinical governance queries or feedback regarding medical content, contact the ZAYVORA Clinical Governance Secretariat at:
            </p>
            <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-1 text-xs">
              <div className="text-white font-bold">Office of Clinical Affairs — ZAYVORA Health</div>
              <div className="text-slate-400">Jamia Hamdard AUTC - Main Hospital Campus, Hamdard Nagar, New Delhi - 110062</div>
              <div className="text-teal-400">Email: governance@zayvora.com • Tele-Desk: +91 11 2605 9000</div>
            </div>
          </section>

        </div>

        {/* Back Link */}
        <div className="pt-8 border-t border-slate-800 flex justify-between items-center text-xs">
          <Link href="/website" className="text-teal-400 hover:underline">
            ← Return to Homepage
          </Link>
          <Link href="/website/book" className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition">
            Book Consultation →
          </Link>
        </div>

      </div>
    </div>
  );
}
