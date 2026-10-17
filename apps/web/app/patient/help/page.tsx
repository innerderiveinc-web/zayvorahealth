"use client";

import React from "react";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";

export default function PatientHelpPage() {
  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">❓ Patient Help & Clinical Concierge</h1>
          <p className="text-sm text-[var(--text-muted)] mt-1">
            Frequently asked questions, emergency clinical protocols, and direct care concierge
          </p>
        </div>

        {/* Emergency Card */}
        <div className="bg-rose-950/30 border border-rose-500/40 p-5 rounded-2xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div className="space-y-1">
            <span className="text-xs font-bold text-rose-400 uppercase tracking-wider">🚨 Emergency Clinical Support</span>
            <h3 className="text-lg font-bold text-white">Experiencing Acute Chest Pain or Severe Distress?</h3>
            <p className="text-xs text-rose-200/80">
              Do not use this app for acute emergencies. Call emergency services immediately or contact our 24/7 hospital casualty desk.
            </p>
          </div>
          <a
            href="tel:+919773882657"
            className="px-5 py-2.5 bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs rounded-xl shadow transition whitespace-nowrap"
          >
            📞 Emergency: +91 97738 82657
          </a>
        </div>

        {/* FAQs */}
        <div className="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
          <h3 className="font-bold text-white text-base">Frequently Asked Questions</h3>
          
          <div className="space-y-3 text-xs">
            <div className="p-4 rounded-xl bg-slate-900/60 border border-[var(--border)] space-y-1.5">
              <h4 className="font-bold text-emerald-400">What is Su-e-Mizaj and how does it relate to my diagnosis?</h4>
              <p className="text-[var(--text-muted)] leading-relaxed">
                In Greco-Arab medicine, health is defined by equilibrium (Mizaj-e-Adil). Su-e-Mizaj represents a humoral deviation (Barid Balghami = cold-phlegmatic). We treat this deviation through the 4-stage Afaal cascade to restore systemic harmony.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-900/60 border border-[var(--border)] space-y-1.5">
              <h4 className="font-bold text-emerald-400">Why do Unani medicines require specific vehicles (Anupan)?</h4>
              <p className="text-[var(--text-muted)] leading-relaxed">
                Vehicles like warm water, fennel infusion, or milk enhance botanical bioavailability and act as natural correctives (Musleh) to protect the gastric mucosa.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-900/60 border border-[var(--border)] space-y-1.5">
              <h4 className="font-bold text-emerald-400">Are my digital prescriptions accepted at external pharmacies?</h4>
              <p className="text-[var(--text-muted)] leading-relaxed">
                Yes. Every prescription generated in ZAYVORA Health OS is cryptographically signed under 21 CFR Part 11 and contains a verified QR code linked to the Central Clinical Registry.
              </p>
            </div>
          </div>
        </div>

        {/* Contact Form Box */}
        <div className="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
          <h3 className="font-bold text-white text-base">Submit a Non-Urgent Query to Hospital Concierge</h3>
          <form onSubmit={e => { e.preventDefault(); alert("Inquiry submitted. Our concierge will contact you at +91 97738 82657."); }} className="space-y-3 text-xs">
            <textarea
              placeholder="Describe your question or scheduling inquiry..."
              rows={3}
              className="w-full bg-slate-800 border border-[var(--border)] rounded-xl p-3 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
            ></textarea>
            <button
              type="submit"
              className="px-5 py-2.5 bg-[#2D6A4F] hover:bg-[#1B4332] text-white font-bold text-xs rounded-xl shadow transition"
            >
              Submit Clinical Inquiry
            </button>
          </form>
        </div>
      </div>
    </AppShell>
  );
}
