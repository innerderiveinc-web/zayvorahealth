"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";

export default function PracticeAnalyticsPage() {
  const [timeRange, setTimeRange] = useState<"7D" | "30D" | "90D" | "1Y">("30D");
  const [exportNotice, setExportNotice] = useState<string | null>(null);

  const handleExport = (format: "PDF" | "CSV") => {
    setExportNotice(`Generating ${format} clinical audit & performance report...`);
    setTimeout(() => setExportNotice(null), 3000);
  };

  const mizajDistribution = [
    { label: "Barid Balghami (Cold & Moist)", count: 474, percent: 38, color: "bg-cyan-500", note: "Predominant in Arthralgia & Chronic Rhinitis" },
    { label: "Har Safrawi (Hot & Dry)", count: 349, percent: 28, color: "bg-amber-500", note: "Common in Dyspepsia, Dermatitis & Insomnia" },
    { label: "Har Damawi (Hot & Moist)", count: 275, percent: 22, color: "bg-rose-500", note: "Hypertension, Cephalalgia & Gout" },
    { label: "Barid Sawdawi (Cold & Dry)", count: 150, percent: 12, color: "bg-purple-500", note: "Chronic Melancholia, IBS & Fibrosis" },
  ];

  const topIndications = [
    { name: "Osteoarthritis / Waja'-ul-Mafasil", cases: 312, resolutionRate: "91.2%", avgWeeks: 7.2 },
    { name: "NAFLD & Hepatic Dyscrasia", cases: 248, resolutionRate: "88.6%", avgWeeks: 8.5 },
    { name: "PCOS & Anovulatory Cycles", cases: 194, resolutionRate: "85.4%", avgWeeks: 10.1 },
    { name: "Chronic Tension Cephalalgia", cases: 165, resolutionRate: "94.0%", avgWeeks: 4.0 },
    { name: "Type-2 Metabolic Syndrome", cases: 142, resolutionRate: "83.1%", avgWeeks: 12.0 },
  ];

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-7xl mx-auto">
        
        {/* Top Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-4">
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
              <span>📈</span> Clinical & Practice Analytics Intelligence
              <span className="px-2 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold">
                Real-Time RWE
              </span>
            </h1>
            <p className="text-xs text-[var(--muted)] mt-1">
              Patient population epidemiology, temperament (Mizaj) cohorts, treatment outcome concordance, and clinical velocity.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            {/* Time Filter */}
            <div className="flex items-center bg-[var(--panel)] p-0.5 rounded-xl border border-[var(--border)]">
              {(["7D", "30D", "90D", "1Y"] as const).map((r) => (
                <button
                  key={r}
                  onClick={() => setTimeRange(r)}
                  className={`px-2.5 py-1 rounded-lg font-semibold transition ${
                    timeRange === r
                      ? "bg-teal-600 text-white shadow-xs"
                      : "text-[var(--muted)] hover:text-white"
                  }`}
                >
                  {r}
                </button>
              ))}
            </div>

            <button
              onClick={() => handleExport("PDF")}
              className="px-3 py-1.5 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] border border-[var(--border)] text-slate-300 hover:text-white font-medium transition"
            >
              Export PDF 📥
            </button>
            <button
              onClick={() => handleExport("CSV")}
              className="px-3 py-1.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition"
            >
              Export CSV 📊
            </button>
          </div>
        </div>

        {exportNotice && (
          <div className="p-3 rounded-xl bg-teal-500/15 border border-teal-500/30 text-teal-300 text-xs flex items-center justify-between animate-fadeIn">
            <span>✓ {exportNotice}</span>
            <button onClick={() => setExportNotice(null)} className="text-slate-400 hover:text-white">✕</button>
          </div>
        )}

        {/* 4 High-Impact KPI Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-1">
            <span className="text-[11px] text-[var(--muted)] block font-medium">Total Registered EMR Profiles</span>
            <div className="text-2xl font-mono font-extrabold text-white">1,248</div>
            <span className="text-[10px] text-emerald-400 font-medium">↑ +14.2% active patient growth</span>
          </div>

          <div className="p-4 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-1">
            <span className="text-[11px] text-[var(--muted)] block font-medium">Clinical Concordance Rate</span>
            <div className="text-2xl font-mono font-extrabold text-teal-300">88.4%</div>
            <span className="text-[10px] text-slate-400">Validated against double-blind pilot criteria</span>
          </div>

          <div className="p-4 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-1">
            <span className="text-[11px] text-[var(--muted)] block font-medium">Teleconsultation Ratio</span>
            <div className="text-2xl font-mono font-extrabold text-purple-300">38% / 62%</div>
            <span className="text-[10px] text-slate-400">38% WebRTC Virtual • 62% In-Person OPD</span>
          </div>

          <div className="p-4 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-1">
            <span className="text-[11px] text-[var(--muted)] block font-medium">Mean Time to Symptom Relief</span>
            <div className="text-2xl font-mono font-extrabold text-amber-300">6.4 Wks</div>
            <span className="text-[10px] text-emerald-400">1.8 weeks faster with 4-stage Afaal cascade</span>
          </div>
        </div>

        {/* Two Columns: Mizaj Cohort & Clinical Indication Concordance */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          {/* Mizaj Demographics (6 cols) */}
          <div className="lg:col-span-6 p-5 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-4">
            <div className="flex justify-between items-center border-b border-[var(--border)] pb-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <span>🌿</span> Patient Population Temperament (Mizaj) Breakdown
              </h3>
              <span className="text-[10px] text-[var(--muted)]">N = 1,248</span>
            </div>

            <div className="space-y-3.5">
              {mizajDistribution.map((m, idx) => (
                <div key={idx} className="space-y-1">
                  <div className="flex justify-between items-center text-xs">
                    <span className="font-bold text-white">{m.label}</span>
                    <span className="font-mono text-slate-300">{m.count} ({m.percent}%)</span>
                  </div>
                  <div className="w-full h-2.5 rounded-full bg-slate-900 overflow-hidden">
                    <div className={`h-full ${m.color} rounded-full`} style={{ width: `${m.percent}%` }}></div>
                  </div>
                  <span className="text-[10px] text-[var(--muted)] block">{m.note}</span>
                </div>
              ))}
            </div>

            <div className="pt-2 border-t border-[var(--border)] flex justify-between items-center text-xs">
              <Link href="/doctor/mizaj" className="text-teal-400 font-bold hover:underline">
                Open Mizaj 10-Ajnas Assessment Engine →
              </Link>
            </div>
          </div>

          {/* Top Indications & Recovery (6 cols) */}
          <div className="lg:col-span-6 p-5 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-4">
            <div className="flex justify-between items-center border-b border-[var(--border)] pb-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <span>🩺</span> Top Indications & Therapeutic Outcome Concordance
              </h3>
              <span className="text-[10px] text-emerald-400 font-bold">AYUSH Standard</span>
            </div>

            <div className="space-y-3">
              {topIndications.map((ind, idx) => (
                <div key={idx} className="p-3 rounded-2xl bg-[var(--background)] border border-[var(--border)] flex items-center justify-between gap-3 text-xs">
                  <div className="space-y-0.5">
                    <div className="font-bold text-white">{ind.name}</div>
                    <span className="text-[10px] text-[var(--muted)]">{ind.cases} Enrolled • Avg {ind.avgWeeks} wks to remission</span>
                  </div>
                  <div className="text-right">
                    <span className="text-xs font-mono font-bold text-emerald-400 block">{ind.resolutionRate}</span>
                    <span className="text-[9px] text-[var(--muted)]">Resolution</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="pt-2 border-t border-[var(--border)] flex justify-between items-center text-xs">
              <Link href="/research/analytics" className="text-teal-400 font-bold hover:underline">
                View Longitudinal Research Cloud Analytics →
              </Link>
            </div>
          </div>

        </div>

      </div>
    </AppShell>
  );
}
