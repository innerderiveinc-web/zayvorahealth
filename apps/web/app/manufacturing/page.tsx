"use client";

import React, { useState } from "react";
import Link from "next/link";
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
  sha256_hash?: string;
  inspector_notes?: string;
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
    sha256_hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    inspector_notes: "Compliant with Unani Pharmacopoeia of India (UPI) Vol. IV. Heavy metals within permissible limits."
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
    sha256_hash: "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
    inspector_notes: "Raw ingredients botanical authentication verified. Compounding in progress."
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
    sha256_hash: "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
    inspector_notes: "Mudabbar (detoxification) milk steeping stage active. Schedule E(1) safety hold applied."
  },
];

export default function ManufacturingPage() {
  const [bmrList, setBmrList] = useState<BmrRecord[]>(INITIAL_BMR);
  const [selectedBmr, setSelectedBmr] = useState<BmrRecord | null>(INITIAL_BMR[0]);
  const [showCoaModal, setShowCoaModal] = useState(false);

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
    alert("eBMR " + bmrId + " successfully signed off and released for distribution.");
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

          <div className="flex flex-wrap items-center gap-3 text-xs">
            <Link
              href="/manufacturing/batches"
              className="px-3 py-1.5 rounded-lg bg-[var(--elevated)] border border-[var(--border)] text-[var(--gold-soft)] hover:text-white transition"
            >
              Batch Ledger →
            </Link>
            <Link
              href="/manufacturing/lab"
              className="px-3 py-1.5 rounded-lg bg-[var(--elevated)] border border-[var(--border)] text-teal-400 hover:text-white transition"
            >
              Quality Lab (CoA) →
            </Link>
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
                      className={}
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
                          className={}
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

              <div className="pt-4 space-y-2">
                <button
                  onClick={() => selectedBmr && handleQaSignOff(selectedBmr.id)}
                  disabled={selectedBmr?.qa_officer_signed}
                  className="zv-btn-primary w-full text-xs font-semibold py-2.5 cursor-pointer disabled:opacity-50"
                >
                  {selectedBmr?.qa_officer_signed ? "✓ QA Officer Signed & Released" : "Sign Off eBMR & Authorize Release"}
                </button>
                <button
                  onClick={() => setShowCoaModal(true)}
                  className="w-full py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-teal-300 border border-slate-700 font-medium text-xs transition"
                >
                  📄 View Certificate of Analysis (CoA)
                </button>
              </div>
            </div>
          </div>

        </div>

        {/* Certificate of Analysis (CoA) Inspection Modal */}
        {showCoaModal && selectedBmr && (
          <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
            <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full p-6 shadow-2xl space-y-5 text-slate-200 my-8">
              <div className="flex items-start justify-between border-b border-slate-800 pb-4">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                      CERTIFIED ANALYTICAL REPORT
                    </span>
                    <span className="text-xs text-slate-400 font-mono">GMP Annex 11 / 21 CFR Part 11</span>
                  </div>
                  <h2 className="text-lg font-bold text-white mt-1">{selectedBmr.product_name}</h2>
                  <p className="text-xs text-slate-400">Lot: <span className="text-amber-400 font-mono">{selectedBmr.batch_lot}</span> | eBMR: <span className="text-slate-300 font-mono">{selectedBmr.id}</span></p>
                </div>
                <button
                  onClick={() => setShowCoaModal(false)}
                  className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition"
                >
                  ✕
                </button>
              </div>

              {/* Analytical Test Table */}
              <div className="space-y-3 text-xs">
                <h4 className="font-bold text-slate-300 uppercase tracking-wider text-[11px]">Pharmacopoeial Specifications (UPI Vol IV)</h4>
                <div className="border border-slate-800 rounded-xl overflow-hidden">
                  <table className="w-full text-left">
                    <thead className="bg-slate-800/60 text-slate-400 font-semibold border-b border-slate-800">
                      <tr>
                        <th className="p-2.5">Test Parameter</th>
                        <th className="p-2.5">Method</th>
                        <th className="p-2.5">Specification</th>
                        <th className="p-2.5">Result</th>
                        <th className="p-2.5">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                      <tr>
                        <td className="p-2.5 font-medium text-white">Heavy Metals (Pb, Cd, As, Hg)</td>
                        <td className="p-2.5 text-slate-400">ICP-MS</td>
                        <td className="p-2.5 text-slate-400">Pb &lt; 10ppm, As &lt; 3ppm</td>
                        <td className="p-2.5 font-mono text-slate-300">Pb: 0.12, As: 0.04 ppm</td>
                        <td className="p-2.5 text-emerald-400 font-bold">{selectedBmr.heavy_metals_pass ? "PASSED" : "FAILED"}</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-medium text-white">Microbial Limit Test (MLT)</td>
                        <td className="p-2.5 text-slate-400">Plate Count</td>
                        <td className="p-2.5 text-slate-400">TAMC &lt; 10^5 CFU/g, Pathogens Absent</td>
                        <td className="p-2.5 font-mono text-slate-300">TAMC: 1.2x10^2 CFU/g</td>
                        <td className="p-2.5 font-bold text-emerald-400">{selectedBmr.microbial_limits_pass ? "PASSED" : "PENDING"}</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-medium text-white">HPTLC Chromatographic Fingerprint</td>
                        <td className="p-2.5 text-slate-400">CAMAG HPTLC</td>
                        <td className="p-2.5 text-slate-400">Rf match with Reference Standard (&ge;95%)</td>
                        <td className="p-2.5 font-mono text-slate-300">Concordance 99.2%</td>
                        <td className="p-2.5 text-emerald-400 font-bold">{selectedBmr.hplc_fingerprint_verified ? "VERIFIED" : "QUEUED"}</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-medium text-white">Mudabbar Detoxification Assay</td>
                        <td className="p-2.5 text-slate-400">HPLC-UV</td>
                        <td className="p-2.5 text-slate-400">Schedule E(1) Colchicine reduction &gt; 45%</td>
                        <td className="p-2.5 font-mono text-slate-300">Safe therapeutic window</td>
                        <td className="p-2.5 text-emerald-400 font-bold">CLEARED</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {/* 21 CFR Part 11 Audit Trail */}
              <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800 space-y-1.5 text-xs font-mono">
                <div className="text-[11px] text-amber-400 font-semibold uppercase tracking-wider font-sans">
                  21 CFR Part 11 Digital Signature Record
                </div>
                <div className="text-slate-400 break-all">
                  <span className="text-slate-500">Batch SHA-256: </span>
                  {selectedBmr.sha256_hash || "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}
                </div>
                <div className="flex justify-between text-slate-400 pt-1">
                  <span>Signer: QA Officer (ID: QA-7821)</span>
                  <span className="text-emerald-400">Status: {selectedBmr.qa_officer_signed ? "Digitally Signed" : "Pending Signature"}</span>
                </div>
              </div>

              <div className="flex justify-end gap-3 pt-2">
                <button
                  onClick={() => window.print()}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition"
                >
                  Print CoA
                </button>
                <button
                  onClick={() => setShowCoaModal(false)}
                  className="px-5 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold transition shadow-md shadow-teal-900/30"
                >
                  Done
                </button>
              </div>
            </div>
          </div>
        )}

      </main>
    </div>
  );
}
