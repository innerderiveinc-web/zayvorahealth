"use client";

import React, { useState } from "react";
import Link from "next/link";
import { PlatformHeader } from "@/components/PlatformHeader";

interface BatchItem {
  id: string;
  lotNumber: string;
  productName: string;
  form: "Majun" | "Safoof" | "Khamira" | "Arq" | "Kushta" | "Habb";
  plannedQuantity: string;
  actualYield: string;
  startDate: string;
  completionDate: string;
  status: "IN_PROGRESS" | "QA_HOLD" | "RELEASED" | "ARCHIVED";
  leadOperator: string;
  qaLead: string;
  mudabbarCertified: boolean;
  hash21Cfr: string;
}

const BATCHES_DATA: BatchItem[] = [
  {
    id: "BMR-2026-0814",
    lotNumber: "LOT-2026-0814",
    productName: "Majun Suranjan Classical Formulation",
    form: "Majun",
    plannedQuantity: "250 kg",
    actualYield: "248.6 kg (99.4%)",
    startDate: "2026-08-01",
    completionDate: "2026-08-14",
    status: "RELEASED",
    leadOperator: "T. Qureshi (OP-104)",
    qaLead: "Dr. A. Siddiqui (QA-7821)",
    mudabbarCertified: true,
    hash21Cfr: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  },
  {
    id: "BMR-2026-0902",
    lotNumber: "LOT-2026-0902",
    productName: "Safoof-e-Ziabetes",
    form: "Safoof",
    plannedQuantity: "150 kg",
    actualYield: "149.1 kg (99.4%)",
    startDate: "2026-08-28",
    completionDate: "2026-09-02",
    status: "IN_PROGRESS",
    leadOperator: "K. Khan (OP-209)",
    qaLead: "Dr. S. Parveen (QA-4412)",
    mudabbarCertified: true,
    hash21Cfr: "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
  },
  {
    id: "BMR-2026-0910",
    lotNumber: "LOT-2026-0910",
    productName: "Suranjan Talkh Mudabbar Purified Batch",
    form: "Habb",
    plannedQuantity: "50 kg",
    actualYield: "Pending Mudabbar",
    startDate: "2026-09-05",
    completionDate: "2026-09-18",
    status: "QA_HOLD",
    leadOperator: "M. Ansari (OP-312)",
    qaLead: "Dr. A. Siddiqui (QA-7821)",
    mudabbarCertified: false,
    hash21Cfr: "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
  },
  {
    id: "BMR-2026-0705",
    lotNumber: "LOT-2026-0705",
    productName: "Khamira Gaozaban Ambari Jawaharwala",
    form: "Khamira",
    plannedQuantity: "100 kg",
    actualYield: "98.2 kg (98.2%)",
    startDate: "2026-06-25",
    completionDate: "2026-07-05",
    status: "ARCHIVED",
    leadOperator: "T. Qureshi (OP-104)",
    qaLead: "Dr. S. Parveen (QA-4412)",
    mudabbarCertified: true,
    hash21Cfr: "3a4b5c6d7e8f90123456789abcdef0123456789abcdef0123456789abcdef012",
  },
];

export default function ManufacturingBatchesPage() {
  const [filter, setFilter] = useState<string>("ALL");
  const [search, setSearch] = useState<string>("");

  const filtered = BATCHES_DATA.filter((b) => {
    const matchesFilter = filter === "ALL" || b.status === filter;
    const matchesSearch =
      b.productName.toLowerCase().includes(search.toLowerCase()) ||
      b.lotNumber.toLowerCase().includes(search.toLowerCase()) ||
      b.id.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--text)]">
      <PlatformHeader />

      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-6 space-y-6">
        {/* Navigation Breadcrumb */}
        <div className="flex items-center gap-2 text-xs text-[var(--muted)]">
          <Link href="/manufacturing" className="hover:text-white transition">
            ← Back to Manufacturing OS
          </Link>
          <span>/</span>
          <span className="text-white font-medium">Batch Manufacturing Ledger</span>
        </div>

        {/* Header Panel */}
        <div className="zv-panel p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-white">eBMR Batch Production Ledger</h1>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-semibold">
                GMP Annex 11 / 21 CFR Part 11
              </span>
            </div>
            <p className="text-xs text-[var(--muted)] mt-1">
              End-to-end lineage, Mudabbar detoxification compliance, and immutable cryptographic sign-off hashes.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/manufacturing/lab"
              className="px-4 py-2 rounded-xl bg-teal-600/20 text-teal-300 border border-teal-500/30 text-xs font-semibold hover:bg-teal-600/30 transition"
            >
              Quality Lab Testing (CoA) →
            </Link>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
          <div className="flex items-center gap-2">
            {["ALL", "RELEASED", "IN_PROGRESS", "QA_HOLD", "ARCHIVED"].map((s) => (
              <button
                key={s}
                onClick={() => setFilter(s)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition ${
                  filter === s
                    ? "bg-[var(--gold-soft)]/20 text-[var(--gold-soft)] border-[var(--gold-soft)]/40"
                    : "bg-[var(--elevated)] text-[var(--muted)] border-[var(--border)] hover:text-white"
                }`}
              >
                {s.replace(/_/g, " ")}
              </button>
            ))}
          </div>

          <input
            type="text"
            placeholder="Search lot, eBMR ID, formulation..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="px-3.5 py-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-xs text-white placeholder-[var(--muted)] w-full sm:w-72 focus:outline-none focus:border-teal-500"
          />
        </div>

        {/* Batches Table */}
        <div className="zv-panel overflow-hidden">
          <table className="w-full text-left text-xs">
            <thead className="bg-[var(--elevated)] border-b border-[var(--border)] text-[var(--muted)] uppercase tracking-wider">
              <tr>
                <th className="p-3">eBMR ID / Lot Number</th>
                <th className="p-3">Product / Dosage Form</th>
                <th className="p-3">Batch Size & Yield</th>
                <th className="p-3">Dates (Start → End)</th>
                <th className="p-3">Mudabbar Status</th>
                <th className="p-3">Status</th>
                <th className="p-3">Audit Hash (21 CFR)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--border)]">
              {filtered.map((batch) => (
                <tr key={batch.id} className="hover:bg-[var(--elevated)] transition">
                  <td className="p-3 font-mono">
                    <div className="text-white font-bold">{batch.id}</div>
                    <div className="text-[11px] text-[var(--gold-soft)]">{batch.lotNumber}</div>
                  </td>
                  <td className="p-3">
                    <div className="text-white font-medium">{batch.productName}</div>
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-[var(--elevated)] border border-[var(--border)] text-slate-300">
                      {batch.form}
                    </span>
                  </td>
                  <td className="p-3">
                    <div className="text-slate-200 font-medium">{batch.actualYield}</div>
                    <div className="text-[10px] text-[var(--muted)]">Plan: {batch.plannedQuantity}</div>
                  </td>
                  <td className="p-3 text-[var(--muted)] font-mono">
                    {batch.startDate} → {batch.completionDate}
                  </td>
                  <td className="p-3">
                    {batch.mudabbarCertified ? (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                        ✓ CERTIFIED
                      </span>
                    ) : (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30">
                        ⏳ IN PROCESS
                      </span>
                    )}
                  </td>
                  <td className="p-3">
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        batch.status === "RELEASED"
                          ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40"
                          : batch.status === "QA_HOLD"
                          ? "bg-rose-500/20 text-rose-400 border border-rose-500/40"
                          : batch.status === "IN_PROGRESS"
                          ? "bg-amber-500/20 text-amber-400 border border-amber-500/40"
                          : "bg-slate-700 text-slate-300 border border-slate-600"
                      }`}
                    >
                      {batch.status.replace(/_/g, " ")}
                    </span>
                  </td>
                  <td className="p-3 font-mono text-[10px] text-[var(--muted)] max-w-xs truncate" title={batch.hash21Cfr}>
                    {batch.hash21Cfr.slice(0, 16)}...
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
