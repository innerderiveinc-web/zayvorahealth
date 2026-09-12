"use client";

import React, { useState } from "react";
import { PlatformHeader } from "@/components/PlatformHeader";

interface BmrRecord {
  id: string;
  product_name: string;
  batch_lot: string;
  batch_size: string;
  manufacturing_date: string;
  expiry_date: string;
  current_stage: "RAW_MATERIAL_QC" | "MUDABBAR_DETOX" | "COMPOUNDING" | "PACKAGING" | "QA_RELEASED";
  heavy_metals_pass: boolean;
  microbial_limits_pass: boolean;
  hplc_fingerprint_verified: boolean;
  qa_officer_signed: boolean;
}

const INITIAL_BMR: BmrRecord[] = [
  {
    id: "BMR-2026-0814",
    product_name: "Majun Suranjan Classical Formulation",
    batch_lot: "LOT-2026-0814",
    batch_size: "250 kg",
    manufacturing_date: "2026-08-14",
    expiry_date: "2028-08-14",
    current_stage: "QA_RELEASED",
    heavy_metals_pass: true,
    microbial_limits_pass: true,
    hplc_fingerprint_verified: true,
    qa_officer_signed: true,
  },
  {
    id: "BMR-2026-0902",
    product_name: "Safoof-e-Ziabetes",
    batch_lot: "LOT-2026-0902",
    batch_size: "150 kg",
    manufacturing_date: "2026-09-02",
    expiry_date: "2028-09-02",
    current_stage: "COMPOUNDING",
    heavy_metals_pass: true,
    microbial_limits_pass: true,
    hplc_fingerprint_verified: true,
    qa_officer_signed: false,
  },
  {
    id: "BMR-2026-0910",
    product_name: "Suranjan Talkh Mudabbar Purified Batch",
    batch_lot: "LOT-2026-0910",
    batch_size: "50 kg",
    manufacturing_date: "2026-09-10",
    expiry_date: "2028-09-10",
    current_stage: "MUDABBAR_DETOX",
    heavy_metals_pass: true,
    microbial_limits_pass: false,
    hplc_fingerprint_verified: false,
    qa_officer_signed: false,
  },
];

export default function ManufacturingPage() {
  const [bmrList, setBmrList] = useState<BmrRecord[]>(INITIAL_BMR);
  const [selectedBmr, setSelectedBmr] = useState<BmrRecord | null>(INITIAL_BMR[0]);

  function handleQaSignOff(bmrId: string) {
    if (!selectedBmr?.heavy_metals_pass || !selectedBmr?.microbial_limits_pass) {
      alert("Cannot sign off: Analytical CoA tests must pass before QA release.");
      return;
    }
    setBmrList(
      bmrList.map((b) =>
        b.id === bmrId ? { ...b, qa_officer_signed: true, current_stage: "QA_RELEASED" } : b
      )
    );
    if (selectedBmr) {
      setSelectedBmr({ ...selectedBmr, qa_officer_signed: true, current_stage: "QA_RELEASED" });
    }
    alert(`eBMR ${bmrId} successfully signed off and released for distribution.`);
  }

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--text)]">
      <PlatformHeader />

      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-6 space-y-6">
        
        {/* Manufacturing Header */}
        <div className="zv-panel p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold">ZAYVORA Manufacturing OS & eBMR</h1>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-rose-500/10 border border-rose-500/30 text-rose-400 font-semibold">
                GMP Certified Facility
              </span>
            </div>
            <p className="text-xs text-[var(--muted)] mt-0.5">
              Electronic Batch Manufacturing Records (eBMR), analytical CoA verification, and Mudabbar purification logs.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="text-[var(--muted)]">Active Production Lots:</span>
            <span className="font-bold text-white">{bmrList.length}</span>
            <span className="text-[var(--border)]">|</span>
            <span className="text-emerald-400 font-medium">GMP Annex 11 Compliant</span>
          </div>
        </div>

        {/* Layout Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Main eBMR Table */}
          <div className="lg:col-span-2 space-y-4">
            <div className="zv-panel overflow-hidden">
              <table className="w-full text-left text-xs">
                <thead className="bg-[var(--elevated)] border-b border-[var(--border)] text-[var(--muted)] uppercase tracking-wider">
                  <tr>
                    <th className="p-3">Product / eBMR ID</th>
                    <th className="p-3">Batch / Lot</th>
                    <th className="p-3">Batch Size</th>
                    <th className="p-3">Current Stage</th>
                    <th className="p-3">QA Release</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border)]">
                  {bmrList.map((b) => (
                    <tr
                      key={b.id}
                      onClick={() => setSelectedBmr(b)}
                      className={`hover:bg-[var(--elevated)] cursor-pointer transition-colors ${
                        selectedBmr?.id === b.id ? "bg-[var(--elevated)]" : ""
                      }`}
                    >
                      <td className="p-3 font-medium">
                        <div className="text-white font-semibold">{b.product_name}</div>
                        <div className="text-[11px] text-[var(--gold-soft)] font-mono">{b.id}</div>
                      </td>
                      <td className="p-3 font-mono text-white">{b.batch_lot}</td>
                      <td className="p-3 text-[var(--muted)]">{b.batch_size}</td>
                      <td className="p-3">
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[var(--elevated)] border border-[var(--border)] text-white">
                          {b.current_stage.replace(/_/g, " ")}
                        </span>
                      </td>
                      <td className="p-3">
                        <span
                          className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                            b.qa_officer_signed
                              ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40"
                              : "bg-amber-500/20 text-amber-400 border border-amber-500/40"
                          }`}
                        >
                          {b.qa_officer_signed ? "RELEASED" : "IN PROCESS"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* eBMR Detail & Analytical Assay Sign-off Panel */}
          <div className="zv-panel p-5 space-y-4">
            <div className="border-b border-[var(--border)] pb-3">
              <span className="text-[10px] uppercase tracking-wider text-[var(--muted)] block">Batch Manufacturing Record</span>
              <h3 className="text-base font-bold text-white">{selectedBmr?.product_name}</h3>
              <span className="text-xs font-mono text-[var(--gold-soft)]">{selectedBmr?.batch_lot}</span>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <span className="text-[var(--muted)] block">Manufacturing Window</span>
                <span className="text-white font-medium">{selectedBmr?.manufacturing_date} → {selectedBmr?.expiry_date}</span>
              </div>

              {/* Analytical CoA Checklist */}
              <div className="pt-2 border-t border-[var(--border)] space-y-2">
                <span className="text-[var(--muted)] font-bold block">Analytical CoA Inspection (UPI Standards)</span>
                
                <div className="flex items-center justify-between p-2 rounded-lg bg-[var(--elevated)] border border-[var(--border)]">
                  <span>Heavy Metals (Lead, Cadmium, Arsenic)</span>
                  <span className={selectedBmr?.heavy_metals_pass ? "text-emerald-400 font-bold" : "text-red-400 font-bold"}>
                    {selectedBmr?.heavy_metals_pass ? "✓ PASS" : "❌ FAIL"}
                  </span>
                </div>

                <div className="flex items-center justify-between p-2 rounded-lg bg-[var(--elevated)] border border-[var(--border)]">
                  <span>Microbial Limits & Aflatoxin</span>
                  <span className={selectedBmr?.microbial_limits_pass ? "text-emerald-400 font-bold" : "text-amber-400 font-bold"}>
                    {selectedBmr?.microbial_limits_pass ? "✓ PASS" : "⏳ TESTING"}
                  </span>
                </div>

                <div className="flex items-center justify-between p-2 rounded-lg bg-[var(--elevated)] border border-[var(--border)]">
                  <span>HPTLC Fingerprint Concordance</span>
                  <span className={selectedBmr?.hplc_fingerprint_verified ? "text-emerald-400 font-bold" : "text-amber-400 font-bold"}>
                    {selectedBmr?.hplc_fingerprint_verified ? "✓ 99.2% MATCH" : "⏳ IN QUEUE"}
                  </span>
                </div>
              </div>

              <div className="pt-4">
                <button
                  onClick={() => selectedBmr && handleQaSignOff(selectedBmr.id)}
                  disabled={selectedBmr?.qa_officer_signed}
                  className="zv-btn-primary w-full text-xs font-semibold py-2.5 cursor-pointer disabled:opacity-50"
                >
                  {selectedBmr?.qa_officer_signed ? "✓ QA Officer Signed & Released" : "Sign Off eBMR & Authorize Release"}
                </button>
              </div>
            </div>
          </div>

        </div>

      </main>
    </div>
  );
}
