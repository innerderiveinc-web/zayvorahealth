"use client";

import React from "react";
import Link from "next/link";

export default function RefundPolicyPage() {
  return (
    <div className="min-h-screen bg-[#0A101D] text-slate-100 py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-10">
        
        <div className="border-b border-slate-800 pb-6 space-y-3">
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <Link href="/website" className="hover:text-teal-400 transition">ZAYVORA Health</Link>
            <span>/</span>
            <span className="text-teal-400 font-medium">Consumer Rights</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Cancellation & Refund Policy
          </h1>
          <p className="text-xs text-slate-400 font-mono">
            Governed under Consumer Protection (E-Commerce) Rules 2020 • Last Updated: September 2026
          </p>
        </div>

        <div className="space-y-8 text-xs sm:text-sm text-slate-300 leading-relaxed">
          
          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">1. Clinical Consultation Cancellations</h2>
            <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 space-y-2 text-xs">
              <div className="flex items-center justify-between text-slate-200">
                <span className="font-semibold">Cancellation &gt; 4 hours before slot:</span>
                <span className="text-emerald-400 font-bold">100% Full Refund</span>
              </div>
              <div className="flex items-center justify-between text-slate-200">
                <span className="font-semibold">Cancellation within 4 hours:</span>
                <span className="text-teal-300 font-bold">Free Reschedule or 80% Refund</span>
              </div>
              <div className="flex items-center justify-between text-slate-200">
                <span className="font-semibold">Clinician Unavailability / Emergency Reschedule:</span>
                <span className="text-emerald-400 font-bold">100% Refund + Priority Next Slot</span>
              </div>
            </div>
            <p>
              Refunds for online consultation fees are credited back to the original source method (UPI, Debit/Credit Card, Net Banking) within 3 to 5 business days.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">2. Herbal Medicines & Dispensary Orders</h2>
            <p>
              Under Drug Safety & AYUSH Good Distribution Guidelines, medicines once opened cannot be accepted for return due to hygiene and environmental contamination protocols. However, you are eligible for an immediate full refund or replacement under the following conditions:
            </p>
            <ul className="list-disc pl-5 space-y-2 text-slate-300">
              <li>Packaging arrives damaged, broken, or with broken security seal.</li>
              <li>Incorrect batch or formulation received compared to the digital prescription.</li>
              <li>Product delivered past the indicated shelf life / expiry date.</li>
            </ul>
            <p>
              To request a dispensary return, email <strong>dispensary@zayvora.com</strong> with unboxing photos within 48 hours of delivery.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-bold text-white">3. Mode & Processing Timeline</h2>
            <p>
              Approved refunds are processed via our automated payment gateway within 24 hours of claim approval and typically reflect in your bank account within 3 to 5 banking days depending on your bank's clearing cycle.
            </p>
          </section>

        </div>

        <div className="pt-8 border-t border-slate-800 flex justify-between items-center text-xs">
          <Link href="/website" className="text-teal-400 hover:underline">
            ← Return to Homepage
          </Link>
          <Link href="/website/contact" className="text-slate-400 hover:text-white transition">
            Contact Support Desk →
          </Link>
        </div>

      </div>
    </div>
  );
}
