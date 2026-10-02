"use client";

import React from "react";
import Link from "next/link";

export default function CareSystemPage() {
  const pillars = [
    {
      num: "01",
      title: "10-Ajnas Longitudinal Mizaj Engine",
      badge: "Classical Foundation",
      color: "border-teal-500 text-teal-400",
      desc: "Every human being possesses a unique constitutional temperament (Mizaj: Damawi, Safrawi, Balghami, or Sawdawi). Our clinical system assesses 10 classical physiological parameters (Ajnas al-Ashrah) including skin tactile quality (Malmas), muscular build (Lahm wa Shahm), hair texture (Sha'ar), complexions (Lawn), sleep patterns (Nawm wa Yaqzah), pulse attributes (Nabz), and mental acuity.",
      points: [
        "Dynamic recalculation of humoral deviations",
        "Individualized baseline calibration per patient",
        "Longitudinal tracking across changing seasons and life stages",
      ]
    },
    {
      num: "02",
      title: "Dual Tashkhees (Integrative Diagnostics)",
      badge: "Biomedical Convergence",
      color: "border-blue-500 text-blue-400",
      desc: "ZAYVORA harmonizes classical Unani bedside observation with cutting-edge modern diagnostics. High-frequency digital tactile pulse wave analysis (Nabz) and acoustic voice biomarkers are correlated directly with biochemical lab panels (hs-CRP, HbA1c, fasting lipids, hepatic enzymes).",
      points: [
        "Multimodal lab ingestion with FHIR R4 interoperability",
        "Humoral dyscrasia correlation with systemic inflammation",
        "Continuous digital twin tracking physiological organ reserves",
      ]
    },
    {
      num: "03",
      title: "4-Stage Afaal Treatment Cascade",
      badge: "Therapeutic Architecture",
      color: "border-purple-500 text-purple-400",
      desc: "Rather than applying blanket symptom suppression, ZAYVORA Matab™ clinicians adhere to the classical sequential protocol of treatment: Tanqiya (Humoral Evacuation & Detoxification) → Tahleel (Metabolic Resolution) → Taqwiyaat (Targeted Organ Strengthening) → Hifz (Health Preservation & Relapse Prevention).",
      points: [
        "Stage gating prevents premature tonification of congested organs",
        "Strict adherence to classical posology and Mudabbar processing",
        "Dynamic phase transition monitored via objective clinical biomarkers",
      ]
    },
    {
      num: "04",
      title: "Hakeem Sahab AI™ & Electronic Governance",
      badge: "Safety & Intelligence",
      color: "border-amber-500 text-amber-400",
      desc: "Clinical decision-making is reinforced by Hakeem Sahab AI™—a 5-layer clinical reasoning engine operating under immutable safety invariants. Every prescription is checked against Schedule E(1) toxic botanicals, drug-herb interactions (OpenFDA), and locked with 21 CFR Part 11 cryptographic electronic signatures.",
      points: [
        "Mandatory human-in-the-loop: safe_to_lock=False invariant",
        "Tamper-evident Merkle tree audit trail across all encounters",
        "Automated FEFO batch allocation with cold-chain dispensary fulfillment",
      ]
    }
  ];

  return (
    <div className="max-w-6xl mx-auto px-6 py-12 space-y-12 text-xs text-[#CBD5E1]">
      {/* Header */}
      <div className="border-b border-[#334155] pb-8 space-y-3">
        <div className="flex items-center gap-2">
          <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ Architecture</span>
          <span className="text-slate-600">•</span>
          <span className="text-[11px] text-slate-400">Clinical Framework</span>
        </div>
        <h1 className="text-3xl md:text-5xl font-extrabold text-white tracking-tight">
          The ZAYVORA Care System™
        </h1>
        <p className="text-base text-[#94A3B8] max-w-3xl leading-relaxed">
          Ancient Wisdom. Modern Science. Intelligent Care. An institutional, full-stack operating system unifying classical Greco-Arabic Unani Tibb with contemporary molecular medicine and verifiable clinical safety.
        </p>
      </div>

      {/* Clinical Workflow Visual Strip */}
      <div className="bg-[#0F172A] border border-[#334155] rounded-3xl p-6 sm:p-8 space-y-6">
        <h2 className="text-base font-bold text-white uppercase tracking-wider text-teal-400">
          Integrated Clinical Workflow Cycle
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-[#1E293B]/70 p-4 rounded-2xl border border-slate-700/60 space-y-2">
            <span className="text-xs font-bold text-teal-400">Phase I: Intake</span>
            <h3 className="font-bold text-white text-sm">10-Ajnas Assessment</h3>
            <p className="text-[11px] text-slate-400">Tactile pulse, tongue diagnosis, constitutional questionnaire &amp; digital intake.</p>
          </div>
          <div className="bg-[#1E293B]/70 p-4 rounded-2xl border border-slate-700/60 space-y-2">
            <span className="text-xs font-bold text-blue-400">Phase II: Diagnostics</span>
            <h3 className="font-bold text-white text-sm">Dual Tashkhees</h3>
            <p className="text-[11px] text-slate-400">Laboratory biomarkers + digital organ axis evaluation and digital twin generation.</p>
          </div>
          <div className="bg-[#1E293B]/70 p-4 rounded-2xl border border-slate-700/60 space-y-2">
            <span className="text-xs font-bold text-purple-400">Phase III: Protocol</span>
            <h3 className="font-bold text-white text-sm">4-Stage Afaal Cascade</h3>
            <p className="text-[11px] text-slate-400">Targeted evacuation, resolution, organ tonification, and wellness preservation.</p>
          </div>
          <div className="bg-[#1E293B]/70 p-4 rounded-2xl border border-slate-700/60 space-y-2">
            <span className="text-xs font-bold text-amber-400">Phase IV: Posology</span>
            <h3 className="font-bold text-white text-sm">FEFO Dispensary</h3>
            <p className="text-[11px] text-slate-400">Standardized compounds, QR batch tracking, and multi-lingual voice posology.</p>
          </div>
        </div>
      </div>

      {/* Deep-Dive Pillars */}
      <div className="space-y-6">
        <h2 className="text-xl font-bold text-white">Four Foundational Pillars of Intelligent Care</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {pillars.map((p) => (
            <div
              key={p.num}
              className={`p-6 rounded-3xl bg-[#1E293B] border border-[#334155] border-t-4 ${p.color} space-y-4 shadow-lg`}
            >
              <div className="flex justify-between items-start">
                <span className="text-2xl font-black text-slate-600">{p.num}</span>
                <span className="px-3 py-1 rounded-full bg-slate-900 border border-slate-700 text-[10px] font-bold uppercase tracking-wider text-slate-300">
                  {p.badge}
                </span>
              </div>
              <h3 className="text-lg font-bold text-white">{p.title}</h3>
              <p className="leading-relaxed text-[#94A3B8]">{p.desc}</p>
              <div className="pt-2 border-t border-slate-800 space-y-1.5">
                {p.points.map((pt, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-[11px] text-slate-300">
                    <span className="text-teal-400">✓</span>
                    <span>{pt}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Navigation Footer Actions */}
      <div className="pt-8 border-t border-[#334155] flex flex-col sm:flex-row justify-between items-center gap-4">
        <Link href="/website" className="text-xs font-semibold text-[#94A3B8] hover:text-white transition">
          ← Back to ZAYVORA Overview
        </Link>
        <div className="flex items-center gap-3">
          <Link
            href="/website/care-journey"
            className="px-4 py-2 rounded-xl bg-slate-800 text-slate-200 font-bold hover:bg-slate-700 border border-slate-600 transition"
          >
            View Patient Journey →
          </Link>
          <Link
            href="/website/book"
            className="px-5 py-2 rounded-xl bg-[#0D9488] text-white font-bold hover:bg-[#14B8A6] shadow-lg transition"
          >
            Book Clinical Consultation →
          </Link>
        </div>
      </div>
    </div>
  );
}
