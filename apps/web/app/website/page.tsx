"use client";

import React from "react";
import Link from "next/link";

export default function PublicHomePage() {
  const careAreas = [
    { name: "Metabolic & Endocrine Disorders", desc: "Su-e-Mizaj Barid Balghami management, insulin sensitivity, lipid dyscrasia.", icon: "⚡" },
    { name: "Musculoskeletal & Joint Care (Mafasil)", desc: "Osteoarthritis, rheumatoid arthralgia, synovial fluid restoration with Ilaj bil-Tadbeer.", icon: "🦴" },
    { name: "Liver & Gastrointestinal Axis", desc: "Hepatobiliary stasis, dyspepsia, fatty liver, gut microbiome humoral balance.", icon: "🌿" },
    { name: "Reproductive Vitality & Fertility", desc: "Male spermatogenic renewal and female follicular equilibrium via targeted Muqawwiyat.", icon: "👶" },
    { name: "Neuro-Psychiatric & Sleep Disorders", desc: "Chronic stress adaptation, GABAergic modulation, and circadian restorative sleep.", icon: "🧠" },
    { name: "Preventive Health & Hifz-e-Sehat", desc: "Asbab-e-Sittah الضرورية adherence for lifelong systemic wellness and immunity.", icon: "🛡️" },
  ];

  const coreProducts = [
    { id: "manivital-pro", name: "ManiVital Pro", category: "Fertility", price: "₹1,450", desc: "Targeted Shukra & male reproductive vitality formulation with Withania somnifera and Mucuna pruriens." },
    { id: "ovasync", name: "OvaSync", category: "Fertility", price: "₹1,380", desc: "Ovarian reserve and hormonal rhythm balancer with standardized Asparagus racemosus extract." },
    { id: "metabocore-elite", name: "MetaboCore Elite", category: "Metabolic", price: "₹1,250", desc: "Potent metabolic regulator featuring Gymnema sylvestre and Berberis aristata." },
    { id: "liverprime-core", name: "LiverPrime Core", category: "Liver & Gut", price: "₹1,150", desc: "Hepatoprotective and bile-regulating compound backed by classical Unani pharmacopoeia." },
    { id: "neurocalmx", name: "NeuroCalmX", category: "Calm & Sleep", price: "₹1,200", desc: "Nootropic stress modulator and adaptogenic nerve tonic with Convolvulus pluricaulis." },
    { id: "nightone-x", name: "NightOne X", category: "Calm & Sleep", price: "₹1,320", desc: "Restorative deep sleep confection enriched with Valeriana wallichii and Nardostachys." },
  ];

  return (
    <div className="space-y-16 pb-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 border-b border-[#334155] bg-gradient-to-b from-[#0F172A] to-[#0A0F1D]">
        <div className="max-w-7xl mx-auto px-6 text-center space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#0D9488]/15 border border-[#0D9488]/30 text-[#2DD4BF] text-xs font-semibold">
            <span>✨ Classical Greco-Arab Science + Modern Biomedical Intelligence</span>
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight">
            Ancient Wisdom. Modern Science. <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#2DD4BF] to-[#14B8A6]">Intelligent Care.</span>
          </h1>
          <p className="text-base md:text-lg text-[#94A3B8] max-w-2xl mx-auto leading-relaxed">
            ZAYVORA Health OS™ unites 1,000 years of codified Unani medicine with state-of-the-art clinical AI, longitudinal Mizaj profiling, organ-axis cross-talk, and 21 CFR Part 11 medical governance.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
            <Link href="/website/book" className="px-6 py-3 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold text-sm shadow-xl transition">
              Book Integrative Consultation
            </Link>
            <Link href="/website/philosophy" className="px-6 py-3 rounded-xl border border-[#334155] hover:bg-[#1E293B] text-white font-semibold text-sm transition">
              Explore Clinical Philosophy →
            </Link>
          </div>
        </div>
      </section>

      {/* 4-Stage Clinical Paradigm */}
      <section className="max-w-7xl mx-auto px-6 space-y-8">
        <div className="text-center space-y-2">
          <span className="text-xs font-bold text-[#2DD4BF] tracking-wider uppercase">Clinical Protocol</span>
          <h2 className="text-2xl md:text-3xl font-bold text-white">The ZAYVORA Afaal Cascade</h2>
          <p className="text-xs md:text-sm text-[#94A3B8] max-w-xl mx-auto">
            Unlike superficial symptom suppression, our clinical continuum restores innate vitality (*Tabi'at*) through four structured, evidence-guided phases:
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
          <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
            <span className="text-xs font-mono font-bold text-emerald-400">STAGE 01</span>
            <h3 className="text-base font-bold text-white">Tanqiya</h3>
            <span className="text-[11px] text-[#2DD4BF] block font-semibold">Humoral Cleansing & Detoxification</span>
            <p className="text-xs text-[#94A3B8] leading-relaxed">
              Targeted elimination of accumulated cold, phlegmatic, or bilious morbid matter (*Mawad-e-Fasida*) through concoctive Munzaj pharmacotherapy and gentle cupping (*Hijama*).
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
            <span className="text-xs font-mono font-bold text-blue-400">STAGE 02</span>
            <h3 className="text-base font-bold text-white">Tahleel</h3>
            <span className="text-[11px] text-blue-400 block font-semibold">Resolution of Inflammation</span>
            <p className="text-xs text-[#94A3B8] leading-relaxed">
              Dissolution of deep-seated peri-articular exudates and microvascular stasis via medicated warm fomentations (*Natool*), poultices (*Zimad*), and classical resolvents.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
            <span className="text-xs font-mono font-bold text-purple-400">STAGE 03</span>
            <h3 className="text-base font-bold text-white">Taqwiyaat</h3>
            <span className="text-[11px] text-purple-400 block font-semibold">Organ & Tissue Restoration</span>
            <p className="text-xs text-[#94A3B8] leading-relaxed">
              Strengthening weakened target organs and neural pathways (*Muqawwiyat-e-A'za*) to rebuild functional resilience and prevent recurrent pathological deposition.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
            <span className="text-xs font-mono font-bold text-amber-400">STAGE 04</span>
            <h3 className="text-base font-bold text-white">Hifz</h3>
            <span className="text-[11px] text-amber-400 block font-semibold">Long-Term Preservation</span>
            <p className="text-xs text-[#94A3B8] leading-relaxed">
              Preserving innate physiological equilibrium through personalized dietetics (*Ilaj bil-Ghiza*) and strict adherence to the Six Essential Lifestyle Precepts (*Asbab-e-Sittah*).
            </p>
          </div>
        </div>
      </section>

      {/* Clinical Care Areas */}
      <section className="max-w-7xl mx-auto px-6 space-y-8">
        <div className="text-center space-y-2">
          <span className="text-xs font-bold text-[#2DD4BF] tracking-wider uppercase">Comprehensive Care</span>
          <h2 className="text-2xl md:text-3xl font-bold text-white">Specialized Clinical Care Areas</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {careAreas.map((area, i) => (
            <div key={i} className="p-6 rounded-2xl bg-[#0F172A] border border-[#334155] hover:border-[#0D9488]/50 transition space-y-3">
              <span className="text-3xl">{area.icon}</span>
              <h3 className="text-base font-bold text-white">{area.name}</h3>
              <p className="text-xs text-[#94A3B8] leading-relaxed">{area.desc}</p>
              <Link href="/website/conditions" className="text-xs font-bold text-[#2DD4BF] hover:text-white inline-flex items-center gap-1">
                Learn Clinical Protocol →
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* Featured ZAYVORA Herbals */}
      <section className="max-w-7xl mx-auto px-6 space-y-8">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-[#334155] pb-4">
          <div>
            <span className="text-xs font-bold text-[#2DD4BF] tracking-wider uppercase">Codified Botanical Formulations</span>
            <h2 className="text-2xl md:text-3xl font-bold text-white">ZAYVORA Herbals Portfolio</h2>
            <p className="text-xs text-[#94A3B8] mt-1">GMP manufactured, CoA verified, Mudabbar purified classical & proprietary compounds.</p>
          </div>
          <Link href="/website/herbals" className="px-4 py-2 rounded-xl border border-[#334155] text-xs font-bold text-[#2DD4BF] hover:text-white hover:bg-[#1E293B]">
            View All 10 Formulations →
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {coreProducts.map((p) => (
            <div key={p.id} className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3 flex flex-col justify-between">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] px-2 py-0.5 rounded font-mono font-semibold bg-[#0D9488]/20 text-[#2DD4BF]">
                    {p.category}
                  </span>
                  <span className="text-sm font-bold text-white">{p.price}</span>
                </div>
                <h4 className="text-base font-bold text-white">{p.name}</h4>
                <p className="text-xs text-[#94A3B8] leading-relaxed">{p.desc}</p>
              </div>
              <div className="pt-3 border-t border-[#334155] flex items-center justify-between">
                <Link href={`/website/product?id=${p.id}`} className="text-xs font-semibold text-[#94A3B8] hover:text-white">
                  View Monographs
                </Link>
                <Link href={`/website/cart?add=${p.id}`} className="px-3.5 py-1.5 rounded-lg bg-[#0D9488] text-white text-xs font-bold hover:bg-[#14B8A6]">
                  + Add to Cart
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-6">
        <div className="p-8 md:p-12 rounded-3xl bg-gradient-to-r from-[#0D9488]/20 via-[#1E293B] to-[#0F172A] border border-[#0D9488]/30 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="space-y-2">
            <h3 className="text-2xl font-bold text-white">Experience Modern Evidence-Based Unani Care</h3>
            <p className="text-xs md:text-sm text-[#94A3B8] max-w-xl">
              Consult with licensed senior tabeebs, receive personalized 10-Ajnas Mizaj profiling, and benefit from organ-axis therapeutic formulations.
            </p>
          </div>
          <Link href="/website/book" className="px-8 py-3.5 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold text-sm shadow-xl whitespace-nowrap">
            Schedule Appointment Now
          </Link>
        </div>
      </section>
    </div>
  );
}
