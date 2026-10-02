"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";

const SEMESTERS_DATA = [
  {
    id: 1,
    title: "Semester 1: Foundations (Weeks 1–6)",
    lectures: "36 Lectures (Pure Theory)",
    modules: [
      {
        num: "Module 1",
        title: "Mizaj & Temperament Science (L01–L12)",
        focus: "Humoral theory, 4 primary qualities as physiological forces, 8-domain Mizaj Assessment Form, Table 1.3 Dose Adjustment Matrix, Thermal herb pairing."
      },
      {
        num: "Module 2",
        title: "Organ-Axis Systems Biology (L13–L24)",
        focus: "6 Organ Axes (Gut-Liver, Liver-Pancreas, Gut-Ovarian, Liver-Testicular, Thyroid-Neuro, HPA), cascade failures, 5 Axis Priority Rules."
      },
      {
        num: "Module 3",
        title: "Clinical Diagnostics & Lab Integration (L25–L36)",
        focus: "Functional vs standard ranges, 5 Non-Negotiable Lab Trigger Rules, HOMA-IR, TG/HDL ratio, Semen Analysis WHO 6th ed vs ZAYVORA optimal."
      }
    ]
  },
  {
    id: 2,
    title: "Semester 2: Therapeutic Architecture (Weeks 7–16)",
    lectures: "40 Lectures (Applied Theory)",
    modules: [
      {
        num: "Module 4",
        title: "Phase-Based Therapeutic Model (L37–L44)",
        focus: "3-Phase Model (Stabilization, Axis Correction, Consolidation), Table 4.1 Phase Trigger Rules (R1–R8), Phase 1/2/3 exit criteria."
      },
      {
        num: "Module 5",
        title: "Therapeutic Formulation Science (L45–L52)",
        focus: "Kaifiyat & Khawas, 4 key standardization targets, 6 Core GMP Hero products, Table 5.1 Herb-Drug Interactions, Forbidden formulation list."
      }
    ]
  },
  {
    id: 3,
    title: "Semester 3: Clinical Practicum & Case Mastery (Weeks 17–24)",
    lectures: "20 Lectures + 20 Supervised Cases",
    modules: [
      {
        num: "Module 6",
        title: "Clinical Practicum & Case Mastery (L53–L90+)",
        focus: "20 Supervised Clinical Cases across 5 tracks, Table 6.2 7 Mandatory Elements, Table 6.1 Red Flag Referrals, Z-ACIP EMR, 20-min Viva Voce."
      }
    ]
  }
];

export default function CpAfumAcademyPage() {
  const [activeTab, setActiveTab] = useState(1);

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-7xl mx-auto pb-16">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-2xl">🏛️</span>
              <h1 className="text-xl font-bold text-white tracking-tight">
                ZAYVORA Institute of Axis-Based Functional Unani Medicine
              </h1>
              <span className="px-2.5 py-0.5 rounded-full bg-teal-500/15 border border-teal-500/30 text-teal-300 text-xs font-mono font-bold">
                CP-AFUM Certification
              </span>
            </div>
            <p className="text-xs text-[var(--muted)] mt-1">
              Academic Director: Dr. Irfan Ashraf | 24 Weeks • 96 Core Lectures • 6 Modules • 20 Supervised Cases
            </p>
          </div>

          <div className="flex items-center gap-2">
            <Link
              href="/doctor/consultation"
              className="px-3.5 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shadow-md transition"
            >
              ⏱️ 5-Min Consultation Console →
            </Link>
            <Link
              href="/doctor/practicum"
              className="px-3.5 py-2 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-teal-300 font-semibold text-xs border border-[var(--border)] transition"
            >
              📑 Practicum Portfolio →
            </Link>
          </div>
        </div>

        {/* 4 Core Standardization Targets Banner */}
        <div className="p-4 rounded-2xl bg-gradient-to-r from-teal-950/40 via-slate-900 to-indigo-950/40 border border-teal-500/30 shadow-md">
          <span className="text-[10px] font-bold text-teal-400 uppercase tracking-wider block mb-2">
            ★ Non-Negotiable Active Standardisation Targets (Exam Critical)
          </span>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div className="p-2.5 rounded-xl bg-black/40 border border-slate-800">
              <span className="text-slate-400 text-[10px] block">Withanolides</span>
              <strong className="text-teal-300 text-sm">≥ 5.0% (HPLC)</strong>
              <span className="text-[10px] text-slate-500 block">ManiVital Pro / NeuroCalmX</span>
            </div>
            <div className="p-2.5 rounded-xl bg-black/40 border border-slate-800">
              <span className="text-slate-400 text-[10px] block">Silymarin</span>
              <strong className="text-emerald-300 text-sm">70 – 80%</strong>
              <span className="text-[10px] text-slate-500 block">LiverPrime Core (Phase 1)</span>
            </div>
            <div className="p-2.5 rounded-xl bg-black/40 border border-slate-800">
              <span className="text-slate-400 text-[10px] block">Berberine HCl</span>
              <strong className="text-cyan-300 text-sm">≥ 95.0%</strong>
              <span className="text-[10px] text-slate-500 block">MetaboCore Elite (AMPK)</span>
            </div>
            <div className="p-2.5 rounded-xl bg-black/40 border border-slate-800">
              <span className="text-slate-400 text-[10px] block">Valerenic Acid</span>
              <strong className="text-indigo-300 text-sm">0.8%</strong>
              <span className="text-[10px] text-slate-500 block">NeuroCalmX (GABA-A)</span>
            </div>
          </div>
        </div>

        {/* Semester Tabs */}
        <div className="flex gap-2 border-b border-[var(--border)] pb-2 text-xs">
          {SEMESTERS_DATA.map((sem) => (
            <button
              key={sem.id}
              onClick={() => setActiveTab(sem.id)}
              className={`px-4 py-2 rounded-xl font-bold transition ${
                activeTab === sem.id
                  ? "bg-teal-600 text-white shadow-xs"
                  : "bg-[var(--panel)] text-[var(--muted)] hover:text-white"
              }`}
            >
              {sem.title}
            </button>
          ))}
        </div>

        {/* Active Semester Modules */}
        <div className="space-y-4">
          {SEMESTERS_DATA.find((s) => s.id === activeTab)?.modules.map((mod, idx) => (
            <div key={idx} className="p-5 rounded-3xl bg-[var(--panel)] border border-[var(--border)] shadow-md space-y-2">
              <div className="flex justify-between items-center">
                <span className="px-2.5 py-0.5 rounded-md bg-slate-800 text-teal-400 font-mono text-xs font-bold">
                  {mod.num}
                </span>
                <span className="text-xs text-slate-400 font-mono">Curriculum Module</span>
              </div>
              <h3 className="text-base font-bold text-white">{mod.title}</h3>
              <p className="text-xs text-slate-300 leading-relaxed">{mod.focus}</p>
            </div>
          ))}
        </div>

        {/* 5 Non-Negotiable Lab Trigger Rules Summary */}
        <div className="p-5 rounded-3xl bg-slate-900/80 border border-slate-800 space-y-3">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <span>🔬</span> The 5 Non-Negotiable Lab Trigger Rules (Memorise All)
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
            <div className="p-3 rounded-2xl bg-[var(--panel)] border border-rose-800/30">
              <strong className="text-rose-300 block mb-1">1. SGPT (ALT) &gt; 45 U/L</strong>
              <p className="text-slate-300 text-[11px]">Phase 1 (LiverPrime Core) mandatory before any axis correction. No exceptions.</p>
            </div>
            <div className="p-3 rounded-2xl bg-[var(--panel)] border border-rose-800/30">
              <strong className="text-rose-300 block mb-1">2. hs-CRP &gt; 3.0 mg/L</strong>
              <p className="text-slate-300 text-[11px]">Systemic inflammation blocks receptor sensitivity for herbal actives. Phase 1 mandatory.</p>
            </div>
            <div className="p-3 rounded-2xl bg-[var(--panel)] border border-cyan-800/30">
              <strong className="text-cyan-300 block mb-1">3. TSH &gt; 2.5 mIU/L (Symptomatic)</strong>
              <p className="text-slate-300 text-[11px]">Subclinical hypothyroid — initiate ThyroMet Axis protocol immediately (no watchful waiting).</p>
            </div>
            <div className="p-3 rounded-2xl bg-[var(--panel)] border border-indigo-800/30">
              <strong className="text-indigo-300 block mb-1">4. Fasting Insulin &gt; 10 uIU/mL</strong>
              <p className="text-slate-300 text-[11px]">Early Stage 1 Insulin Resistance detected before HbA1c elevation — MetaboCore Elite.</p>
            </div>
            <div className="p-3 rounded-2xl bg-[var(--panel)] border border-amber-800/30">
              <strong className="text-amber-300 block mb-1">5. SGPT &gt; 100 or Anti-TPO &gt; 300</strong>
              <p className="text-slate-300 text-[11px]">Specialist referral mandatory (Hepatology / Endocrinology). ZAYVORA as adjunct only.</p>
            </div>
            <div className="p-3 rounded-2xl bg-[var(--panel)] border border-teal-800/30">
              <strong className="text-teal-300 block mb-1">Safravi Mizaj Rule</strong>
              <p className="text-slate-300 text-[11px]">Reduce ALL heating herbs by 25–30% across ALL phases. SGPT check every 4 weeks.</p>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
