"use client";

import React from "react";
import { AppShell } from "@/components/AppShell";

const INVOICES = [
  { id: "INV-2026-0814", description: "Outpatient Consultation (Hakeem Dr. Irfan Ashraf)", amount: 800, date: "2026-09-12", status: "Paid", method: "UPI" },
  { id: "INV-2026-0815", description: "Unani Formulations (Majun Suranjan + Raughan-e-Balsan)", amount: 1420, date: "2026-09-12", status: "Paid", method: "Debit Card (Stripe)" },
  { id: "INV-2026-0792", description: "Diagnostic Laboratory Panel (Metabolic + Inflammatory)", amount: 1200, date: "2026-09-10", status: "Paid", method: "UPI" }
];

export default function PatientPaymentsPage() {
  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">💳 Billing & Payment Receipts</h1>
          <p className="text-sm text-[var(--text-muted)] mt-1">
            Official receipts for clinic consultations, pharmacy dispensary orders, and lab investigations
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)]">
            <span className="text-xs text-[var(--text-muted)] block">Total Settled</span>
            <span className="text-2xl font-bold text-white mt-1 block">₹3,420</span>
            <span className="text-xs text-emerald-400 mt-1 block">✓ Zero outstanding copays</span>
          </div>
          <div className="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)]">
            <span className="text-xs text-[var(--text-muted)] block">Linked Insurance / TPA</span>
            <span className="text-2xl font-bold text-white mt-1 block">Star Health AYUSH</span>
            <span className="text-xs text-[var(--text-muted)] mt-1 block">Cashless OPD claims supported</span>
          </div>
          <div className="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)]">
            <span className="text-xs text-[var(--text-muted)] block">Payment Gateway</span>
            <span className="text-2xl font-bold text-white mt-1 block">Stripe & UPI</span>
            <span className="text-xs text-emerald-400 mt-1 block">100% PCI-DSS compliant</span>
          </div>
        </div>

        <div className="bg-[var(--card)] rounded-2xl border border-[var(--border)] divide-y divide-[var(--border)] overflow-hidden">
          {INVOICES.map(inv => (
            <div key={inv.id} className="p-5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 hover:bg-white/5 transition">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono font-bold text-emerald-400 text-sm">{inv.id}</span>
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    {inv.status}
                  </span>
                </div>
                <h3 className="font-bold text-white text-sm mt-1">{inv.description}</h3>
                <p className="text-xs text-[var(--text-muted)]">Settled via {inv.method} on {inv.date}</p>
              </div>

              <div className="flex items-center gap-4">
                <span className="text-lg font-bold font-mono text-white">₹{inv.amount.toLocaleString()}</span>
                <button
                  onClick={() => alert(`Downloading statutory tax invoice ${inv.id}...`)}
                  className="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-[var(--border)] transition"
                >
                  Download Invoice 📄
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
