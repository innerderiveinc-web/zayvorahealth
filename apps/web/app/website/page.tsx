"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { HEALTH_PROGRAMS } from "@/lib/cms/programsData";
import { PRODUCTS_CATALOG, RegulatoryCategory } from "@/lib/cms/productsData";
import { CLINICAL_TEAM } from "@/lib/cms/doctorsData";
import { KNOWLEDGE_ARTICLES } from "@/lib/cms/articlesData";
import { FAQS_DATA } from "@/lib/cms/faqsData";

export default function ZayvoraHealthHomepage() {
  // Waveform canvas ref
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Filter states
  const [selectedProgramCategory, setSelectedProgramCategory] = useState<string>("All");
  const [selectedProductCategory, setSelectedProductCategory] = useState<RegulatoryCategory | "All">("All");
  const [openFaqId, setOpenFaqId] = useState<string | null>("faq-1");
  const [activeConcern, setActiveConcern] = useState<string | null>(null);

  // Animated Nabz Waveform Simulation
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;
    let t = 0;

    const renderWave = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Grid background
      ctx.strokeStyle = "rgba(13, 148, 136, 0.1)";
      ctx.lineWidth = 1;
      for (let x = 0; x < canvas.width; x += 20) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
      }
      for (let y = 0; y < canvas.height; y += 20) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
      }

      // Waveform line
      ctx.strokeStyle = "#2DD4BF";
      ctx.lineWidth = 2.5;
      ctx.beginPath();

      const centerY = canvas.height / 2;
      for (let x = 0; x < canvas.width; x++) {
        // Compound arterial PPG wave with dicrotic notch
        const wave1 = Math.sin((x + t) * 0.04) * 20;
        const wave2 = Math.sin((x + t) * 0.08) * 8;
        const dicrotic = Math.exp(-Math.pow(((x + t) % 120) - 60, 2) / 200) * 18;
        const y = centerY + wave1 + wave2 - dicrotic;
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      t += 1.5;
      animationFrameId = requestAnimationFrame(renderWave);
    };

    renderWave();
    return () => cancelAnimationFrame(animationFrameId);
  }, []);

  const healthConcerns = [
    {
      id: "male-fertility",
      title: "Male Fertility & Reproductive Health",
      desc: "Evidence-informed 74-day spermatogenesis support addressing sperm count, progressive motility, and seminal oxidative protection.",
      icon: "🧬",
      href: "/website/programs"
    },
    {
      id: "female-hormones",
      title: "Female Hormonal Health & PCOS",
      desc: "Gentle pelvic circulation and ovarian harmony protocols for cycle regularity, dysmenorrhea, and hormonal balance.",
      icon: "🌸",
      href: "/website/programs"
    },
    {
      id: "gut-ibs",
      title: "Gut & IBS Support",
      desc: "Rebuilding gastric digestive warmth (Hazm) to relieve chronic abdominal bloating, post-meal heaviness, and erratic transit.",
      icon: "🍃",
      href: "/website/programs"
    },
    {
      id: "liver-metabolic",
      title: "Liver & Metabolic Health",
      desc: "Targeted hepatic decongestion (Kabid) and circadian nutrition supporting insulin sensitivity and fatty infiltration reduction.",
      icon: "🔬",
      href: "/website/programs"
    },
    {
      id: "thyroid-endocrine",
      title: "Thyroid & Hormonal Health",
      desc: "Nutritional support for sluggish glandular temperament (Su-e-Mizaj Barid), cold intolerance, and peripheral energy conversion.",
      icon: "⚡",
      href: "/website/programs"
    },
    {
      id: "stress-sleep",
      title: "Stress, Anxiety & Sleep Support",
      desc: "Nervous faculty tonification (Taskeen-e-Asab) using non-habit-forming adaptogens to support restorative deep sleep architecture.",
      icon: "🌙",
      href: "/website/programs"
    },
    {
      id: "weight-metabolism",
      title: "Weight & Metabolic Management",
      desc: "Restoring innate metabolic heat (Hararat-e-Ghariziyyah) through circadian meal timing and gentle thermogenic botanicals.",
      icon: "⚖️",
      href: "/website/programs"
    },
    {
      id: "skin-hair",
      title: "Skin & Hair Wellness",
      desc: "Clearing internal humoral impurities (Fasad-e-Dam) to support radiant dermal clarity and nourish hair root vitality.",
      icon: "✨",
      href: "/website/programs"
    },
    {
      id: "respiratory",
      title: "Respiratory Wellness",
      desc: "Clearing phlegmatic mucosal accumulation (Balgham) from pulmonary pathways through gentle expectorant fomentations.",
      icon: "🌬️",
      href: "/website/programs"
    },
    {
      id: "vitality",
      title: "General Vitality & Resilience",
      desc: "Comprehensive preventive tonification (Hifz-e-Sehat) enhancing the body's self-healing faculty (Tabi'at) across all seasons.",
      icon: "🌿",
      href: "/website/programs"
    },
  ];

  const filteredPrograms = selectedProgramCategory === "All"
    ? HEALTH_PROGRAMS.slice(0, 6)
    : HEALTH_PROGRAMS.filter(p => p.category === selectedProgramCategory);

  const filteredProducts = selectedProductCategory === "All"
    ? PRODUCTS_CATALOG
    : PRODUCTS_CATALOG.filter(p => p.regulatoryCategory === selectedProductCategory);

  return (
    <div className="space-y-20 pb-20 text-[#CBD5E1]">

      {/* ========================================================================= */}
      {/* SECTION 1 — HERO                                                          */}
      {/* ========================================================================= */}
      <section className="relative pt-12 pb-16 px-4 sm:px-6 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          <div className="lg:col-span-7 space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#0D5C46]/20 border border-[#0D9488]/40 text-[#2DD4BF] text-xs font-semibold">
              <span>🌿</span>
              <span>Modern Unani Care System • Jamia Hamdard AUTC Facility</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white tracking-tight leading-[1.15]">
              Modern Unani Care for Your <span className="text-[#2DD4BF]">Complete Health Journey</span>
            </h1>

            <p className="text-base sm:text-lg text-[#94A3B8] leading-relaxed max-w-2xl">
              Classical Unani wisdom, modern clinical understanding, and personalized care — brought together through the ZAYVORA Health System.
            </p>

            {/* CTAs */}
            <div className="flex flex-wrap items-center gap-4 pt-2">
              <Link
                href="/website/book"
                className="px-6 py-3.5 rounded-2xl bg-[#0D9488] text-white font-bold text-sm hover:bg-[#0F766E] shadow-xl hover:shadow-[#0D9488]/20 transition flex items-center gap-2"
              >
                <span>📅</span>
                <span>Book a Consultation</span>
              </Link>
              <Link
                href="/website/programs"
                className="px-6 py-3.5 rounded-2xl bg-[#1E293B] border border-[#334155] text-white font-semibold text-sm hover:bg-[#334155] hover:border-[#0D9488] transition"
              >
                Explore Health Programs
              </Link>
              <Link
                href="/patient/login"
                className="px-5 py-3.5 rounded-2xl text-[#94A3B8] hover:text-white text-sm font-semibold transition"
              >
                Patient Login →
              </Link>
            </div>

            {/* 4 Trust Points */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-6 border-t border-[#1E293B]">
              <div className="space-y-0.5">
                <span className="text-white font-bold text-sm block">Personalized Care</span>
                <span className="text-[11px] text-[#64748B] block">10-Ajnas Mizaj profiling</span>
              </div>
              <div className="space-y-0.5">
                <span className="text-white font-bold text-sm block">Clinician-Guided</span>
                <span className="text-[11px] text-[#64748B] block">Supervised by senior Tabeebs</span>
              </div>
              <div className="space-y-0.5">
                <span className="text-white font-bold text-sm block">Evidence-Informed</span>
                <span className="text-[11px] text-[#64748B] block">Standardized HPLC assays</span>
              </div>
              <div className="space-y-0.5">
                <span className="text-white font-bold text-sm block">Secure Experience</span>
                <span className="text-[11px] text-[#64748B] block">HIPAA & ABDM compliant</span>
              </div>
            </div>
          </div>

          {/* Hero Visual: Physiological Diagnostic & Telemetry Card */}
          <div className="lg:col-span-5 space-y-4">
            <div className="rounded-3xl bg-gradient-to-br from-[#0F172A] to-[#1E293B] border border-[#334155] p-6 shadow-2xl space-y-5">
              <div className="flex items-center justify-between border-b border-[#334155] pb-3">
                <div className="flex items-center gap-2.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-[#2DD4BF] animate-pulse"></span>
                  <span className="font-bold text-white text-xs">Arterial Pulse (Nabz) Waveform Simulation</span>
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#0D9488]/20 text-[#2DD4BF]">100 Hz DSP</span>
              </div>

              {/* Canvas Waveform */}
              <div className="rounded-2xl bg-[#070B14] border border-[#1E293B] p-2 overflow-hidden shadow-inner">
                <canvas ref={canvasRef} width={420} height={130} className="w-full h-28 block" />
              </div>

              {/* Real-time Physiological Vitals Grid */}
              <div className="grid grid-cols-3 gap-2.5 text-xs text-center">
                <div className="p-3 rounded-xl bg-[#0A0F1D] border border-[#334155]">
                  <span className="text-[10px] text-[#64748B] block">Heart Rate</span>
                  <span className="font-bold text-white text-base">72 <span className="text-[10px] text-[#94A3B8]">BPM</span></span>
                </div>
                <div className="p-3 rounded-xl bg-[#0A0F1D] border border-[#334155]">
                  <span className="text-[10px] text-[#64748B] block">Dominant Mizaj</span>
                  <span className="font-bold text-[#2DD4BF] text-sm">Balghami</span>
                </div>
                <div className="p-3 rounded-xl bg-[#0A0F1D] border border-[#334155]">
                  <span className="text-[10px] text-[#64748B] block">Cold-Chain FEFO</span>
                  <span className="font-bold text-amber-400 text-sm">19.4°C</span>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[#0D9488]/10 border border-[#0D9488]/30 flex items-center justify-between text-xs">
                <span className="text-white font-medium">Non-invasive clinical assessment</span>
                <Link href="/website/book" className="text-[#2DD4BF] font-bold hover:underline text-[11px]">
                  Schedule Assessment →
                </Link>
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* ========================================================================= */}
      {/* SECTION 2 — INTRODUCTION                                                  */}
      {/* ========================================================================= */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="rounded-3xl bg-[#0F172A] border border-[#334155] p-8 sm:p-12 space-y-8">
          <div className="max-w-3xl space-y-4">
            <span className="text-[11px] font-bold text-[#0D9488] uppercase tracking-wider block">Introduction to ZAYVORA</span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              A Living Synthesis of Classical Wisdom & Contemporary Medical Science
            </h2>
            <p className="text-sm sm:text-base text-[#94A3B8] leading-relaxed">
              ZAYVORA Health was established to bridge a profound divide in healthcare: while modern medicine excels in emergency triage and acute interventions, millions of individuals struggle with chronic, multi-system disorders that standard symptomatic therapies fail to resolve.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4 border-t border-[#1E293B]">
            <div className="space-y-2">
              <h3 className="font-bold text-white text-base flex items-center gap-2">
                <span className="text-lg">🏛️</span> Why We Exist
              </h3>
              <p className="text-xs text-[#94A3B8] leading-relaxed">
                To transform traditional Unani Tibb into an evidence-based, clinically governed science with verified botanical compounds and measurable biomarker outcomes.
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-bold text-white text-base flex items-center gap-2">
                <span className="text-lg">👥</span> Who It Is For
              </h3>
              <p className="text-xs text-[#94A3B8] leading-relaxed">
                Individuals navigating persistent metabolic slowdown, hormonal imbalances, chronic joint discomfort, and stress burnout seeking root-cause restoration.
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-bold text-white text-base flex items-center gap-2">
                <span className="text-lg">⚙️</span> How It Combines Care
              </h3>
              <p className="text-xs text-[#94A3B8] leading-relaxed">
                We integrate classical 10-Ajnas pulse evaluation and Asbab-e-Sittah lifestyle factors with laboratory chemistry and clinician-guided digital health tracking.
              </p>
            </div>
          </div>

          <div className="pt-2 flex justify-start">
            <Link
              href="/website/about"
              className="px-5 py-2.5 rounded-xl bg-[#1E293B] border border-[#334155] text-white font-semibold text-xs hover:border-[#0D9488] transition inline-flex items-center gap-2"
            >
              <span>Discover ZAYVORA</span>
              <span>→</span>
            </Link>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* SECTION 3 — HEALTH CONCERNS                                               */}
      {/* ========================================================================= */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 space-y-8">
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <span className="text-[11px] font-bold text-[#0D9488] uppercase tracking-wider block">Areas of Specialization</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Clinician-Guided Health Concerns We Address
          </h2>
          <p className="text-xs sm:text-sm text-[#94A3B8]">
            Care pathways designed around physiological organ axes, constitutional humors, and evidence-informed botanical protocols.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {healthConcerns.map((c) => (
            <div
              key={c.id}
              className="p-5 rounded-2xl bg-[#0F172A] border border-[#334155] hover:border-[#0D9488] transition duration-200 flex flex-col justify-between space-y-4 group"
            >
              <div className="space-y-2.5">
                <span className="text-2xl block p-2.5 rounded-xl bg-[#1E293B] w-fit border border-[#334155]">
                  {c.icon}
                </span>
                <h4 className="font-bold text-white text-sm group-hover:text-[#2DD4BF] transition leading-snug">
                  {c.title}
                </h4>
                <p className="text-[11px] text-[#94A3B8] leading-relaxed">
                  {c.desc}
                </p>
              </div>

              <Link
                href={c.href}
                className="pt-2 border-t border-[#1E293B] text-[11px] font-bold text-[#0D9488] hover:text-white transition flex items-center justify-between"
              >
                <span>View Pathway</span>
                <span>→</span>
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* ========================================================================= */}
      {/* SECTION 4 — ZAYVORA CARE SYSTEM                                           */}
      {/* ========================================================================= */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 space-y-10">
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <span className="text-[11px] font-bold text-[#0D9488] uppercase tracking-wider block">The Continuum of Care</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            The ZAYVORA 7-Step Care Journey
          </h2>
          <p className="text-xs sm:text-sm text-[#94A3B8]">
            From your first assessment to long-term health preservation, every step is deliberate, measured, and clinician-supervised.
          </p>
        </div>

        {/* Visual Process Diagram */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-7 gap-3">
          {[
            { step: "01", title: "Patient Assessment", sub: "Intake symptom survey and digital registration" },
            { step: "02", title: "Health History", sub: "Review of prior reports, labs, and medications" },
            { step: "03", title: "Mizaj Mapping", sub: "10-Ajnas constitutional temperament evaluation" },
            { step: "04", title: "Clinical Evaluation", sub: "Video or in-clinic consult with registered Tabeeb" },
            { step: "05", title: "Care Plan", sub: "Personalized 4-phase sequential protocol" },
            { step: "06", title: "Lifestyle Guidance", sub: "Asbab-e-Sittah nutrition, sleep & movement" },
            { step: "07", title: "Follow-up & Review", sub: "Bi-weekly milestone audits and progress scores" },
          ].map((s, idx) => (
            <div
              key={idx}
              className="p-4 rounded-2xl bg-[#0F172A] border border-[#334155] space-y-2 relative group hover:border-[#0D9488] transition"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-extrabold text-[#0D9488] px-2 py-0.5 rounded bg-[#0D9488]/10">
                  {s.step}
                </span>
                {idx < 6 && (
                  <span className="hidden lg:inline text-xs text-[#334155] font-bold">→</span>
                )}
              </div>
              <h5 className="font-bold text-white text-xs leading-snug">{s.title}</h5>
              <p className="text-[10px] text-[#64748B] leading-normal">{s.sub}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ========================================================================= */}
      {/* SECTION 5 — FEATURED HEALTH PROGRAMS                                      */}
      {/* ========================================================================= */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 space-y-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="space-y-2">
            <span className="text-[11px] font-bold text-[#0D9488] uppercase tracking-wider block">Structured Clinical Programs</span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              Featured Health Reversal Programs
            </h2>
            <p className="text-xs sm:text-sm text-[#94A3B8]">
              Multi-week clinician-supervised care programs targeting chronic constitutional dyscrasias.
            </p>
          </div>

          {/* Program Category Filters */}
          <div className="flex flex-wrap gap-2 text-xs font-semibold">
            {["All", "Men's Health", "Women's Health", "Metabolic Health", "Gut & Liver", "Stress & Sleep", "General Wellness"].map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedProgramCategory(cat)}
                className={`px-3.5 py-1.5 rounded-xl border transition ${
                  selectedProgramCategory === cat
                    ? "bg-[#0D9488] border-[#0D9488] text-white"
                    : "bg-[#0F172A] border-[#334155] text-[#94A3B8] hover:text-white"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {filteredPrograms.map((p) => (
            <div
              key={p.id}
              className="rounded-3xl bg-[#0F172A] border border-[#334155] p-6 space-y-5 hover:border-[#0D9488] transition flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-[#0D9488]/20 text-[#2DD4BF] font-mono">
                    {p.duration}
                  </span>
                  <span className="text-[10px] text-[#64748B] font-semibold">{p.category}</span>
                </div>

                <h3 className="text-lg font-bold text-white">{p.title}</h3>
                <p className="text-xs text-[#94A3B8] leading-relaxed">{p.shortDescription}</p>

                <div className="space-y-1.5 pt-2 border-t border-[#1E293B]">
                  <span className="text-[10px] font-bold text-white uppercase block">What is included:</span>
                  <ul className="space-y-1 text-[11px] text-[#64748B]">
                    {p.inclusions.slice(0, 3).map((inc, i) => (
                      <li key={i} className="flex items-start gap-1.5">
                        <span className="text-[#0D9488]">✓</span>
                        <span>{inc}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="pt-4 border-t border-[#1E293B] flex items-center justify-between gap-3">
                <Link
                  href={`/website/program?id=${p.id}`}
                  className="px-4 py-2 rounded-xl bg-[#1E293B] text-xs font-semibold text-white hover:bg-[#334155] transition"
                >
                  View Details
                </Link>
                <Link
                  href="/website/book"
                  className="px-4 py-2 rounded-xl bg-[#0D9488] text-xs font-bold text-white hover:bg-[#0F766E] shadow-sm transition"
                >
                  Book Consult
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ========================================================================= */}
      {/* SECTION 6 — FEATURED PRODUCTS (REGULATORY CATEGORIZED)                    */}
      {/* ========================================================================= */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 space-y-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400 text-[11px] font-bold">
              <span>🛡️</span> Statutory Regulatory Traceability
            </div>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              Standardized Botanical Formulations
            </h2>
            <p className="text-xs sm:text-sm text-[#94A3B8]">
              Formulated in GMP cleanrooms, authenticated via HPLC assays, and verified under Schedule E(1) Mudabbar standards.
            </p>
          </div>

          {/* Regulatory Category Filter */}
          <div className="flex flex-wrap gap-2 text-xs font-semibold">
            {(["All", "Clinic-Prescribed Unani Formulation", "AYUSH-Licensed Botanical Preparation", "FSSAI Dietary & Nutraceutical Supplement"] as const).map((rc) => (
              <button
                key={rc}
                onClick={() => setSelectedProductCategory(rc)}
                className={`px-3 py-1.5 rounded-xl border text-[11px] transition ${
                  selectedProductCategory === rc
                    ? "bg-[#0D9488] border-[#0D9488] text-white"
                    : "bg-[#0F172A] border-[#334155] text-[#94A3B8] hover:text-white"
                }`}
              >
                {rc === "All" ? "All Formulations" : rc.replace(" Preparation", "").replace(" Formulation", "")}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {filteredProducts.slice(0, 8).map((prod) => (
            <div
              key={prod.id}
              className="rounded-3xl bg-[#0F172A] border border-[#334155] p-5 space-y-4 hover:border-[#0D9488] transition flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex justify-between items-start gap-2">
                  <span className="text-[9px] font-bold px-2 py-0.5 rounded bg-[#1E293B] border border-[#334155] text-[#94A3B8] uppercase">
                    {prod.regulatoryCategory === "Clinic-Prescribed Unani Formulation" ? "Rx Only" : "AYUSH"}
                  </span>
                  <span className="text-sm font-bold text-white font-mono">{prod.currency}{prod.price}</span>
                </div>

                <h4 className="font-bold text-white text-base leading-snug">{prod.name}</h4>
                <p className="text-[11px] text-[#94A3B8] line-clamp-2 leading-relaxed">{prod.intendedUse}</p>

                <div className="p-2.5 rounded-xl bg-[#0A0F1D] border border-[#1E293B] space-y-1 text-[10px]">
                  <span className="text-[#64748B] block">Batch: <strong className="text-white font-mono">{prod.batchInfo.lotNumber}</strong></span>
                  <span className="text-[#64748B] block">Heavy Metals: <strong className="text-emerald-400">Passed (&lt;0.05 ppm)</strong></span>
                </div>
              </div>

              <div className="space-y-2 pt-3 border-t border-[#1E293B]">
                <div className="flex items-center justify-between text-[11px]">
                  <Link href={`/website/product?id=${prod.id}`} className="text-[#0D9488] font-bold hover:underline">
                    View Monograph →
                  </Link>
                  {prod.consultBeforeUseRequired ? (
                    <span className="text-amber-400 font-semibold text-[10px]">Consult Required</span>
                  ) : (
                    <span className="text-emerald-400 font-semibold text-[10px]">OTC Available</span>
                  )}
                </div>

                {prod.canBuyDirectly ? (
                  <Link
                    href={`/website/product?id=${prod.id}`}
                    className="w-full text-center block py-2 rounded-xl bg-[#1E293B] hover:bg-[#334155] border border-[#334155] text-white text-xs font-semibold transition"
                  >
                    View & Order
                  </Link>
                ) : (
                  <Link
                    href="/website/book"
                    className="w-full text-center block py-2 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/40 text-amber-300 text-xs font-bold transition"
                  >
                    Consult for Prescription
                  </Link>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="text-center pt-2">
          <Link
            href="/website/herbals"
            className="px-6 py-3 rounded-2xl bg-[#1E293B] border border-[#334155] text-white font-semibold text-xs hover:border-[#0D9488] transition inline-flex items-center gap-2"
          >
            <span>Explore Complete 10-Formulation Portfolio</span>
            <span>→</span>
          </Link>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* SECTION 7 — HOW CONSULTATION WORKS                                        */}
      {/* ========================================================================= */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 space-y-10">
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <span className="text-[11px] font-bold text-[#0D9488] uppercase tracking-wider block">Seamless Clinical Experience</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            How a ZAYVORA Consultation Works
          </h2>
          <p className="text-xs sm:text-sm text-[#94A3B8]">
            Whether consulting online via secure video room or visiting our hospital OPD in New Delhi.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {[
            { num: "1", title: "Book Consultation", desc: "Select preferred physician, date, and mode (Online or In-Clinic)." },
            { num: "2", title: "Share Health History", desc: "Complete brief symptom questionnaire and upload prior lab reports." },
            { num: "3", title: "Clinical Assessment", desc: "Comprehensive 10-Ajnas evaluation and organ-axis functional analysis." },
            { num: "4", title: "Personalized Care Plan", desc: "Sequential 4-phase nutrition, lifestyle directives, and herbal guidance." },
            { num: "5", title: "Follow-up & Tracking", desc: "Regular check-ins via Patient Portal with digital dose reminders." },
          ].map((c) => (
            <div key={c.num} className="p-5 rounded-2xl bg-[#0F172A] border border-[#334155] space-y-3">
              <span className="w-8 h-8 rounded-full bg-[#0D9488]/20 border border-[#0D9488]/40 text-[#2DD4BF] font-extrabold text-xs flex items-center justify-center">
                {c.num}
              </span>
              <h4 className="font-bold text-white text-sm">{c.title}</h4>
              <p className="text-xs text-[#94A3B8] leading-relaxed">{c.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ========================================================================= */}
      {/* SECTION 8 — CLINICAL TEAM                                                 */}
      {/* ========================================================================= */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 space-y-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="space-y-2">
            <span className="text-[11px] font-bold text-[#0D9488] uppercase tracking-wider block">Clinical Faculty</span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              Our Certified Practitioners & Tabeebs
            </h2>
            <p className="text-xs sm:text-sm text-[#94A3B8]">
              All practitioners hold statutory CCIM/BUMS credentials with extensive clinical experience at academic teaching hospitals.
            </p>
          </div>
          <Link href="/website/doctors" className="text-xs font-bold text-[#0D9488] hover:text-white transition">
            View All Clinical Faculty →
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {CLINICAL_TEAM.map((doc) => (
            <div
              key={doc.id}
              className="rounded-3xl bg-[#0F172A] border border-[#334155] p-5 space-y-4 hover:border-[#0D9488] transition flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-2xl bg-[#0D9488] text-white font-bold flex items-center justify-center text-base shadow-md">
                    {doc.avatarInitials}
                  </div>
                  <div>
                    <h4 className="font-bold text-white text-sm">{doc.name}</h4>
                    <span className="text-[10px] text-[#2DD4BF] font-mono block">{doc.regNumber}</span>
                  </div>
                </div>

                <p className="text-[11px] text-[#94A3B8] leading-snug">{doc.designation}</p>

                <div className="space-y-1 pt-2 border-t border-[#1E293B] text-[11px]">
                  <span className="text-[10px] font-bold text-white uppercase block">Focus:</span>
                  <p className="text-[#64748B] text-[10px] leading-tight">{doc.areasOfFocus.slice(0, 2).join(" • ")}</p>
                </div>
              </div>

              <div className="space-y-2 pt-3 border-t border-[#1E293B]">
                <div className="flex justify-between items-center text-[10px] text-[#64748B]">
                  <span>Experience: <strong className="text-white">{doc.experienceYears} Years</strong></span>
                  <span>{doc.languages.join(", ")}</span>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <Link
                    href={`/website/doctor?id=${doc.id}`}
                    className="w-full text-center py-2 rounded-xl bg-[#1E293B] text-[11px] font-semibold text-white hover:bg-[#334155] transition"
                  >
                    Profile
                  </Link>
                  <Link
                    href="/website/book"
                    className="w-full text-center py-2 rounded-xl bg-[#0D9488] text-[11px] font-bold text-white hover:bg-[#0F766E] transition"
                  >
                    Book
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ========================================================================= */}
      {/* SECTION 9 — KNOWLEDGE CENTER                                              */}
      {/* ========================================================================= */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 space-y-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="space-y-2">
            <span className="text-[11px] font-bold text-[#0D9488] uppercase tracking-wider block">Evidence & Education</span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              Clinical Insights & Unani Science
            </h2>
            <p className="text-xs sm:text-sm text-[#94A3B8]">
              Clinician-reviewed articles connecting classical manuscripts with modern laboratory biology.
            </p>
          </div>
          <Link href="/website/knowledge-centre" className="text-xs font-bold text-[#0D9488] hover:text-white transition">
            Explore All 9 Categories →
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {KNOWLEDGE_ARTICLES.slice(0, 3).map((art) => (
            <div
              key={art.id}
              className="rounded-3xl bg-[#0F172A] border border-[#334155] p-6 space-y-4 hover:border-[#0D9488] transition flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex justify-between items-center text-[10px]">
                  <span className="font-bold px-2 py-0.5 rounded bg-[#1E293B] text-[#2DD4BF]">{art.category}</span>
                  <span className="text-[#64748B]">{art.readTimeMinutes} min read</span>
                </div>

                <h3 className="font-bold text-white text-base leading-snug">{art.title}</h3>
                <p className="text-xs text-[#94A3B8] leading-relaxed line-clamp-3">{art.summary}</p>
              </div>

              <div className="pt-4 border-t border-[#1E293B] flex items-center justify-between">
                <span className="text-[10px] text-[#64748B]">{art.author}</span>
                <Link href={`/website/article?id=${art.id}`} className="text-xs font-bold text-[#0D9488] hover:underline">
                  Read Article →
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ========================================================================= */}
      {/* SECTION 10 — TRUST AND SAFETY                                             */}
      {/* ========================================================================= */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="rounded-3xl bg-gradient-to-r from-[#0F172A] via-[#131F37] to-[#0F172A] border border-[#334155] p-8 sm:p-12 space-y-8">
          <div className="max-w-3xl space-y-3">
            <span className="text-[11px] font-bold text-[#0D9488] uppercase tracking-wider block">Governance & Ethics</span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              Patient Trust, Privacy & Clinical Safety
            </h2>
            <p className="text-xs sm:text-sm text-[#94A3B8]">
              We adhere strictly to statutory AYUSH regulations, patient data isolation, and verified medical transparency.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="space-y-2">
              <span className="text-xl block">🔒</span>
              <h4 className="font-bold text-white text-sm">Patient Privacy</h4>
              <p className="text-xs text-[#94A3B8]">
                Protected health information (PHI) is compartmentalized under HIPAA and Indian ABDM digital health standards.
              </p>
            </div>
            <div className="space-y-2">
              <span className="text-xl block">🩺</span>
              <h4 className="font-bold text-white text-sm">Clinician Supervision</h4>
              <p className="text-xs text-[#94A3B8]">
                No autonomous AI prescriptions. All care pathways require non-delegable sign-off from a registered Tabeeb.
              </p>
            </div>
            <div className="space-y-2">
              <span className="text-xl block">🧪</span>
              <h4 className="font-bold text-white text-sm">Lab Tested Purity</h4>
              <p className="text-xs text-[#94A3B8]">
                Heavy metals ICP-MS screened below 0.05 ppm with authentic pharmacopoeial batch certificates of analysis.
              </p>
            </div>
            <div className="space-y-2">
              <span className="text-xl block">📜</span>
              <h4 className="font-bold text-white text-sm">Medical Disclaimer</h4>
              <p className="text-xs text-[#94A3B8]">
                Transparent non-guaranteed clinical guidance. Emergency cases are immediately triaged to hospital facilities.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* SECTION 11 — FAQ ACCORDION                                                */}
      {/* ========================================================================= */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 space-y-8">
        <div className="text-center space-y-3">
          <span className="text-[11px] font-bold text-[#0D9488] uppercase tracking-wider block">Frequently Asked Questions</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Clear Answers to Common Clinical Questions
          </h2>
        </div>

        <div className="space-y-3">
          {FAQS_DATA.map((faq) => {
            const isOpen = openFaqId === faq.id;
            return (
              <div
                key={faq.id}
                className="rounded-2xl bg-[#0F172A] border border-[#334155] overflow-hidden transition"
              >
                <button
                  onClick={() => setOpenFaqId(isOpen ? null : faq.id)}
                  className="w-full text-left p-5 flex items-center justify-between gap-4 font-bold text-white text-sm hover:text-[#2DD4BF] transition"
                >
                  <span>{faq.question}</span>
                  <span className="text-base text-[#0D9488] shrink-0">{isOpen ? "−" : "+"}</span>
                </button>
                {isOpen && (
                  <div className="px-5 pb-5 text-xs text-[#94A3B8] leading-relaxed border-t border-[#1E293B] pt-3 animate-fade-in">
                    {faq.answer}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* ========================================================================= */}
      {/* SECTION 12 — FINAL CTA                                                    */}
      {/* ========================================================================= */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="rounded-3xl bg-gradient-to-br from-[#0D5C46] to-[#0A2E23] p-10 sm:p-14 text-center space-y-6 shadow-2xl">
          <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight max-w-2xl mx-auto">
            Start Your Personalized Health Journey
          </h2>
          <p className="text-sm sm:text-base text-[#E6F4EA] max-w-xl mx-auto leading-relaxed">
            Schedule an online or in-clinic evaluation with senior Unani clinicians at Jamia Hamdard AUTC - Main Hospital.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
            <Link
              href="/website/book"
              className="px-7 py-3.5 rounded-2xl bg-white text-[#0D5C46] font-bold text-sm hover:bg-[#F8FAFC] shadow-lg transition"
            >
              Book Consultation
            </Link>
            <Link
              href="/website/contact"
              className="px-7 py-3.5 rounded-2xl bg-[#07241B] border border-[#0D9488]/50 text-white font-semibold text-sm hover:bg-[#051A14] transition"
            >
              Contact ZAYVORA
            </Link>
            <Link
              href="/patient/login"
              className="px-6 py-3.5 rounded-2xl text-[#A7F3D0] hover:text-white text-sm font-semibold transition"
            >
              Patient Login →
            </Link>
          </div>
        </div>
      </section>

    </div>
  );
}
