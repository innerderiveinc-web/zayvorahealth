"use client";

import React, { useState } from "react";
import Link from "next/link";
import { PlatformHeader } from "@/components/PlatformHeader";

interface LabTestItem {
  id: string;
  sampleId: string;
  batchLot: string;
  productName: string;
  testType: "HEAVY_METALS" | "MICROBIAL" | "AFLATOXIN" | "HPTLC" | "MUDABBAR_DETOX";
  instrument: string;
  analyst: string;
  dateTested: string;
  status: "PASSED" | "FAILED" | "IN_ANALYSIS";
  measuredValues: string;
  specification: string;
}

const LAB_TESTS: LabTestItem[] = [
  {
    id: "LAB-2026-0881",
    sampleId: "SMP-0814-A",
    batchLot: "LOT-2026-0814",
    productName: "Majun Suranjan Classical Formulation",
    testType: "HEAVY_METALS",
    instrument: "PerkinElmer NexION ICP-MS",
    analyst: "A. Farooqi (QC-Analyst)",
    dateTested: "2026-08-12",
    status: "PASSED",
    measuredValues: "Pb: 0.12 ppm, Cd: 0.02 ppm, As: 0.04 ppm, Hg: <0.01 ppm",
    specification: "Pb < 10 ppm, Cd < 0.3 ppm, As < 3 ppm, Hg < 1 ppm (UPI Vol. IV)",
  },
  {
    id: "LAB-2026-0882",
    sampleId: "SMP-0814-B",
    batchLot: "LOT-2026-0814",
    productName: "Majun Suranjan Classical Formulation",
    testType: "MICROBIAL",
    instrument: "Automated Colony Counter (Symbiosis)",
    analyst: "S. Fatima (Microbiologist)",
    dateTested: "2026-08-13",
    status: "PASSED",
    measuredValues: "TAMC: 1.2x10^2 CFU/g, TYMC: <10 CFU/g, E.coli: Absent",
    specification: "TAMC < 10^5 CFU/g, TYMC < 10^3 CFU/g, Pathogens: Absent",
  },
  {
    id: "LAB-2026-0883",
    sampleId: "SMP-0814-C",
    batchLot: "LOT-2026-0814",
    productName: "Majun Suranjan Classical Formulation",
    testType: "HPTLC",
    instrument: "CAMAG Automatic TLC Sampler 4",
    analyst: "Dr. N. Hashmi (Spectroscopy Lead)",
    dateTested: "2026-08-13",
    status: "PASSED",
    measuredValues: "Rf profile matching Colchicum luteum UPI standard, concordance 99.2%",
    specification: "Concordance >= 95% with reference chromatogram",
  },
  {
    id: "LAB-2026-0901",
    sampleId: "SMP-0910-A",
    batchLot: "LOT-2026-0910",
    productName: "Suranjan Talkh Mudabbar Purified Batch",
    testType: "MUDABBAR_DETOX",
    instrument: "Waters ACQUITY Premier HPLC-UV",
    analyst: "Dr. N. Hashmi (Spectroscopy Lead)",
    dateTested: "2026-09-12",
    status: "IN_ANALYSIS",
    measuredValues: "Post-steeping alkaloid extraction in progress (Cycle 2 of 3)",
    specification: "Schedule E(1) alkaloid reduction > 45% (Safe therapeutic index)",
  },
  {
    id: "LAB-2026-0905",
    sampleId: "SMP-0902-A",
    batchLot: "LOT-2026-0902",
    productName: "Safoof-e-Ziabetes",
    testType: "AFLATOXIN",
    instrument: "Shimadzu LC-MS/MS 8060",
    analyst: "A. Farooqi (QC-Analyst)",
    dateTested: "2026-09-01",
    status: "PASSED",
    measuredValues: "B1: <0.1 ppb, Total (B1+B2+G1+G2): <0.5 ppb",
    specification: "B1 < 2 ppb, Total Aflatoxins < 5 ppb",
  },
];

export default function ManufacturingLabPage() {
  const [tests, setTests] = useState<LabTestItem[]>(LAB_TESTS);
  const [selectedType, setSelectedType] = useState<string>("ALL");

  const filtered = tests.filter((t) => selectedType === "ALL" || t.testType === selectedType);

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--text)]">
      <PlatformHeader />

      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-6 space-y-6">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-xs text-[var(--muted)]">
          <Link href="/manufacturing" className="hover:text-white transition">
            ← Back to Manufacturing OS
          </Link>
          <span>/</span>
          <span className="text-white font-medium">QC Analytical Laboratory</span>
        </div>

        {/* Header */}
        <div className="zv-panel p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-white">ZAYVORA QC Analytical Laboratory</h1>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-teal-500/10 border border-teal-500/30 text-teal-300 font-semibold">
                NABL / ISO 17025 Accreditations
              </span>
            </div>
            <p className="text-xs text-[var(--muted)] mt-1">
              Unani Pharmacopoeia of India (UPI) botanical assays, Heavy Metal ICP-MS, Microbial Limits & Mudabbar safety verification.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/manufacturing/batches"
              className="px-4 py-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-xs text-white hover:border-teal-500 transition"
            >
              ← View Batch Ledger
            </Link>
          </div>
        </div>

        {/* Assay Metrics Overview Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="zv-panel p-4 space-y-1">
            <span className="text-[10px] uppercase text-[var(--muted)] font-semibold">ICP-MS Heavy Metals</span>
            <div className="text-lg font-bold text-emerald-400">100% Passed</div>
            <p className="text-[11px] text-[var(--muted)]">Lead, Cadmium, Arsenic, Mercury</p>
          </div>
          <div className="zv-panel p-4 space-y-1">
            <span className="text-[10px] uppercase text-[var(--muted)] font-semibold">Microbial Purity</span>
            <div className="text-lg font-bold text-emerald-400">Zero Contamination</div>
            <p className="text-[11px] text-[var(--muted)]">Pathogen-free plate counts</p>
          </div>
          <div className="zv-panel p-4 space-y-1">
            <span className="text-[10px] uppercase text-[var(--muted)] font-semibold">Mudabbar Safety Holds</span>
            <div className="text-lg font-bold text-amber-400">1 Batch Steeping</div>
            <p className="text-[11px] text-[var(--muted)]">Schedule E(1) detoxification</p>
          </div>
          <div className="zv-panel p-4 space-y-1">
            <span className="text-[10px] uppercase text-[var(--muted)] font-semibold">HPTLC Botanical Authenticity</span>
            <div className="text-lg font-bold text-teal-300">99.2% Avg Match</div>
            <p className="text-[11px] text-[var(--muted)]">CAMAG Scanner 4 profiles</p>
          </div>
        </div>

        {/* Filter bar */}
        <div className="flex flex-wrap items-center gap-2">
          {["ALL", "HEAVY_METALS", "MICROBIAL", "HPTLC", "MUDABBAR_DETOX", "AFLATOXIN"].map((type) => (
            <button
              key={type}
              onClick={() => setSelectedType(type)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition ${
                selectedType === type
                  ? "bg-teal-500/20 text-teal-300 border-teal-500/40"
                  : "bg-[var(--elevated)] text-[var(--muted)] border-[var(--border)] hover:text-white"
              }`}
            >
              {type.replace(/_/g, " ")}
            </button>
          ))}
        </div>

        {/* Laboratory Test Records Table */}
        <div className="zv-panel overflow-hidden">
          <table className="w-full text-left text-xs">
            <thead className="bg-[var(--elevated)] border-b border-[var(--border)] text-[var(--muted)] uppercase tracking-wider">
              <tr>
                <th className="p-3">Sample / Assay ID</th>
                <th className="p-3">Product & Batch</th>
                <th className="p-3">Assay Type & Instrument</th>
                <th className="p-3">Analyst</th>
                <th className="p-3">Results & Specification</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--border)]">
              {filtered.map((test) => (
                <tr key={test.id} className="hover:bg-[var(--elevated)] transition">
                  <td className="p-3 font-mono">
                    <div className="text-white font-bold">{test.id}</div>
                    <div className="text-[11px] text-[var(--gold-soft)]">{test.sampleId}</div>
                  </td>
                  <td className="p-3">
                    <div className="text-white font-medium">{test.productName}</div>
                    <div className="text-[11px] font-mono text-[var(--muted)]">{test.batchLot}</div>
                  </td>
                  <td className="p-3">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-[var(--elevated)] border border-[var(--border)] text-teal-300">
                      {test.testType.replace(/_/g, " ")}
                    </span>
                    <div className="text-[11px] text-[var(--muted)] mt-1">{test.instrument}</div>
                  </td>
                  <td className="p-3 text-[var(--muted)]">
                    <div>{test.analyst}</div>
                    <div className="text-[10px] font-mono">{test.dateTested}</div>
                  </td>
                  <td className="p-3 max-w-sm">
                    <div className="text-white font-mono text-[11px]">{test.measuredValues}</div>
                    <div className="text-[10px] text-[var(--muted)] mt-0.5">Spec: {test.specification}</div>
                  </td>
                  <td className="p-3">
                    <span
                      className={`text-[10px] font-bold px-2.5 py-1 rounded-full ${
                        test.status === "PASSED"
                          ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40"
                          : test.status === "FAILED"
                          ? "bg-rose-500/20 text-rose-400 border border-rose-500/40"
                          : "bg-amber-500/20 text-amber-400 border border-amber-500/40"
                      }`}
                    >
                      {test.status}
                    </span>
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
