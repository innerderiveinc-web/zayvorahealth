"use client";

import React from "react";
import Link from "next/link";

export default function AccessibilityStatementPage() {
  return (
    <div className="min-h-screen bg-[#0A101D] text-slate-100 py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-10">
        
        <div className="border-b border-slate-800 pb-6 space-y-3">
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <Link href="/website" className="hover:text-teal-400 transition">ZAYVORA Health</Link>
            <span>/</span>
            <span className="text-teal-400 font-medium">Digital Inclusion</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Accessibility Statement (WCAG 2.1 AA)
          </h1>
          <p className="text-xs text-slate-400 font-mono">
            Commitment to Universal Healthcare Access • Last Updated: September 2026
          </p>
        </div>

        <div className="space-y-8 text-xs sm:text-sm text-slate-300 leading-relaxed">
          
          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">1. Our Commitment to Universal Healthcare</h2>
            <p>
              ZAYVORA Health is dedicated to ensuring that digital health information, appointment scheduling, and patient portal access are accessible to everyone, including individuals with visual, motor, auditory, cognitive, or language impairments.
            </p>
            <p>
              We continuously evaluate our digital interfaces against the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA criteria established by the World Wide Web Consortium (W3C).
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">2. Accessible Features Implemented</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-1 text-xs">
                <span className="font-bold text-teal-400 block">High Contrast & Screen Modes</span>
                <p className="text-slate-300">Minimum 4.5:1 text-to-background contrast ratio across dark and light palettes.</p>
              </div>
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-1 text-xs">
                <span className="font-bold text-teal-400 block">Keyboard Navigability</span>
                <p className="text-slate-300">Complete keyboard navigation support, skip-to-content anchors, and clear focus rings.</p>
              </div>
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-1 text-xs">
                <span className="font-bold text-teal-400 block">Vernacular Voice Medication</span>
                <p className="text-slate-300">Voice-guided dosage instructions in Urdu, Hindi, and English for low-literacy accessibility.</p>
              </div>
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-1 text-xs">
                <span className="font-bold text-teal-400 block">Screen Reader Tags & ARIA</span>
                <p className="text-slate-300">Semantic HTML5 landmarks, descriptive alt text on clinical imagery, and ARIA live regions.</p>
              </div>
            </div>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">3. Feedback & Contact</h2>
            <p>
              If you experience any accessibility barriers while browsing ZAYVORA Health or using our Patient Portal, please contact our Digital Inclusion Desk:
            </p>
            <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 text-xs text-slate-300 space-y-1">
              <div>Email: <strong>accessibility@zayvora.com</strong></div>
              <div>Phone: <strong>+91 97738 82657 (Ext 404)</strong></div>
            </div>
          </section>

        </div>

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
