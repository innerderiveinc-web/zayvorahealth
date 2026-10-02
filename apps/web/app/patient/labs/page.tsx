"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";

interface LabTest {
  name: string;
  result: string;
  unit: string;
  referenceRange: string;
  status: "Normal" | "Abnormal" | "Borderline";
  category: string;
  date: string;
  doctor: string;
}

const LAB_TESTS: LabTest[] = [
  { name: "Fasting Blood Glucose", result: "118", unit: "mg/dL", referenceRange: "70 – 99", status: "Borderline", category: "Metabolic Panel", date: "2026-09-10", doctor: "Hakeem Dr. Irfan Ashraf" },
  { name: "HbA1c (Glycated Hemoglobin)", result: "6.8", unit: "%", referenceRange: "< 5.7", status: "Borderline", category: "Metabolic Panel", date: "2026-09-10", doctor: "Hakeem Dr. Irfan Ashraf" },
  { name: "Erythrocyte Sedimentation Rate (ESR)", result: "24", unit: "mm/hr", referenceRange: "0 – 15", status: "Abnormal", category: "Inflammatory Markers", date: "2026-09-10", doctor: "Hakeem Dr. Irfan Ashraf" },
  { name: "C-Reactive Protein (High Sensitivity)", result: "4.2", unit: "mg/L", referenceRange: "< 1.0", status: "Abnormal", category: "Inflammatory Markers", date: "2026-09-10", doctor: "Hakeem Dr. Irfan Ashraf" },
  { name: "Serum Uric Acid", result: "5.8", unit: "mg/dL", referenceRange: "3.5 – 7.2", status: "Normal", category: "Renal & Joint Profile", date: "2026-09-10", doctor: "Hakeem Dr. Irfan Ashraf" },
  { name: "Serum Calcium", result: "9.4", unit: "mg/dL", referenceRange: "8.5 – 10.5", status: "Normal", category: "Bone & Joint Health", date: "2026-09-10", doctor: "Hakeem Dr. Irfan Ashraf" },
  { name: "Serum Alanine Aminotransferase (ALT)", result: "26", unit: "U/L", referenceRange: "7 – 56", status: "Normal", category: "Hepatic Panel", date: "2026-09-10", doctor: "Hakeem Dr. Irfan Ashraf" }
];

export default function PatientLabsPage() {
  const [tests, setTests] = useState<LabTest[]>(LAB_TESTS);
  const [filter, setFilter] = useState("All");

  const filtered = filter === "All" ? tests : tests.filter(t => t.category === filter);

  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">🧪 Diagnostic Laboratory Results</h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              Biochemical panels cross-referenced with your Su-e-Mizaj Barid Balghami humoral profile
            </p>
          </div>
          <button 
            onClick={() => alert("Downloading comprehensive laboratory report PDF with physician sign-off...")}
            className="px-4 py-2 bg-[#2D6A4F] hover:bg-[#1B4332] text-white rounded-xl text-sm font-semibold transition shadow-sm"
          >
            ⬇ Download Complete PDF
          </button>
        </div>

        {/* Categories Bar */}
        <div className="flex gap-2 overflow-x-auto pb-1">
          {["All", "Metabolic Panel", "Inflammatory Markers", "Renal & Joint Profile", "Hepatic Panel"].map(c => (
            <button
              key={c}
              onClick={() => setFilter(c)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                filter === c ? "bg-[#2D6A4F] text-white" : "bg-[var(--card)] text-[var(--text-muted)] border border-[var(--border)] hover:text-white"
              }`}
            >
              {c}
            </button>
          ))}
        </div>

        {/* Results List */}
        <div className="bg-[var(--card)] rounded-2xl border border-[var(--border)] overflow-hidden divide-y divide-[var(--border)]">
          {filtered.map(t => (
            <div key={t.name} className="p-5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 hover:bg-white/5 transition">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <h3 className="font-bold text-white text-base">{t.name}</h3>
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                    t.status === "Normal" ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30" :
                    t.status === "Borderline" ? "bg-amber-500/20 text-amber-400 border border-amber-500/30" :
                    "bg-rose-500/20 text-rose-400 border border-rose-500/30"
                  }`}>
                    {t.status}
                  </span>
                </div>
                <p className="text-xs text-[var(--text-muted)]">
                  Reference Range: <strong className="text-slate-300">{t.referenceRange} {t.unit}</strong> • Category: {t.category} • Ordered by: {t.doctor}
                </p>
              </div>

              <div className="text-right">
                <div className="text-2xl font-bold font-mono text-white">
                  {t.result} <span className="text-sm text-[var(--text-muted)] font-normal">{t.unit}</span>
                </div>
                <span className="text-xs text-[var(--text-muted)]">Verified on {t.date}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
