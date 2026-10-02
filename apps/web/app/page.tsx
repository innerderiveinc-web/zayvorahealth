"use client";

import React, { useState } from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { HOMEPAGE_CONTENT } from "@/lib/cms/website/homepage";
import { CLINICAL_TEAM } from "@/lib/cms/doctorsData";
import { HEALTH_LIBRARY_ARTICLES } from "@/lib/data/healthLibrary";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export default function ZayvoraHealthHomepage() {
  const [selectedConcern, setSelectedConcern] = useState<string>("all");
  const [activeCareStep, setActiveCareStep] = useState<number>(0);
  const [mizajQuestionStep, setMizajQuestionStep] = useState<number>(0);
  const [mizajAnswers, setMizajAnswers] = useState<{ thermal?: string; digestion?: string; sleep?: string }>({});
  const [mizajResult, setMizajResult] = useState<{
    mizaj: string;
    english: string;
    qualities: string;
    description: string;
    asbabTips: string;
  } | null>(null);

  const calculateMizaj = (answers: { thermal?: string; digestion?: string; sleep?: string }) => {
    const { thermal, digestion } = answers;
    if (thermal === "warm" && digestion === "active") {
      return {
        mizaj: "Safrawi (صفراوی)",
        english: "Bilious / Choleric (Hot & Dry)",
        qualities: "High metabolic drive, warm extremities, alert responsiveness.",
        description: "Predominance of yellow bile (Safra). Prone to acidity, restlessness, and heat intolerance under excessive exertion.",
        asbabTips: "Prioritize cooling, hydrating nutrition (Aab-e-Anar, cucumber, barley water) and avoid late-night sleep deprivation."
      };
    } else if (thermal === "warm" && digestion === "moderate") {
      return {
        mizaj: "Damawi (دموی)",
        english: "Sanguine (Hot & Moist)",
        qualities: "Robust vitality, florid complexion, strong muscular habitus.",
        description: "Predominance of blood (Dam). Excellent constitutional resilience, but requires monitoring for metabolic congestion and plethora.",
        asbabTips: "Engage in regular physical exertion (Riyazat) and maintain balanced, non-excessive caloric intake."
      };
    } else if (thermal === "cold" && digestion === "slow") {
      return {
        mizaj: "Balghami (بلغمی)",
        english: "Phlegmatic (Cold & Moist)",
        qualities: "Calm demeanor, cooler skin tone, heavier sleep architecture.",
        description: "Predominance of phlegm (Balgham). Tendency towards fluid retention, sluggish metabolism, and morning sluggishness.",
        asbabTips: "Incorporate warming spices (Zanjabeel/Ginger, Darchini/Cinnamon) and avoid cold/heavy dairy in the evening."
      };
    } else {
      return {
        mizaj: "Sawdawi (سوداوی)",
        english: "Melancholic (Cold & Dry)",
        qualities: "Analytical mind, slender build, sensitivity to erratic schedules.",
        description: "Predominance of black bile (Sawda). Tendency towards dry skin, anxious rumination, and light or fragmented sleep.",
        asbabTips: "Follow calming oil massage (Dalk), deeply nourishing moist foods (Roghan-e-Badam, milk, dates), and fixed bedtime hours."
      };
    }
  };

  const handleMizajOption = (key: "thermal" | "digestion" | "sleep", val: string) => {
    const updated = { ...mizajAnswers, [key]: val };
    setMizajAnswers(updated);
    if (mizajQuestionStep < 2) {
      setMizajQuestionStep(mizajQuestionStep + 1);
    } else {
      const res = calculateMizaj(updated);
      setMizajResult(res);
      setMizajQuestionStep(3);
    }
  };

  const resetMizajTeaser = () => {
    setMizajQuestionStep(0);
    setMizajAnswers({});
    setMizajResult(null);
  };

  const filteredCareCategories =
    selectedConcern === "all"
      ? HOMEPAGE_CONTENT.findCare.categories
      : HOMEPAGE_CONTENT.findCare.categories.filter((cat) => cat.concern === selectedConcern);

  return (
    <PublicWebsiteShell>
      {/* ── 1. INSTITUTIONAL HERO SECTION ─────────────────────────────── */}
      <section className="relative overflow-hidden bg-gradient-to-b from-[#FAFAF7] via-white to-[#F4F6F0] py-16 sm:py-24 border-b border-[#E2E8F0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            
            {/* Left Column: Heading & Core Clinical Access */}
            <div className="lg:col-span-7 space-y-6">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E8F5E9] border border-[#C8E6C9] text-xs font-semibold text-[#1B4332]">
                <HealthcareIcon name="shield-check" className="w-4 h-4 text-[#2D6A4F]" />
                <span>{HOMEPAGE_CONTENT.hero.eyebrow}</span>
              </div>

              <h1 className="text-3xl sm:text-5xl lg:text-5xl font-extrabold text-[#0F172A] tracking-tight leading-[1.15]">
                {HOMEPAGE_CONTENT.hero.heading}
              </h1>

              <p className="text-base sm:text-lg text-[#475569] leading-relaxed max-w-2xl font-normal">
                {HOMEPAGE_CONTENT.hero.subheading}
              </p>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center gap-3 pt-2">
                <Link
                  href={HOMEPAGE_CONTENT.hero.primaryCta.href}
                  className="px-6 py-3.5 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white font-semibold text-sm shadow-sm hover:shadow transition duration-150 flex items-center gap-2"
                >
                  <HealthcareIcon name="calendar" className="w-4 h-4 text-[#A7F3D0]" />
                  <span>{HOMEPAGE_CONTENT.hero.primaryCta.label}</span>
                </Link>

                <Link
                  href={HOMEPAGE_CONTENT.hero.secondaryCta.href}
                  className="px-5 py-3.5 rounded-xl bg-white hover:bg-[#F8FAFC] text-[#1B4332] font-semibold text-sm border border-[#CBD5E1] transition shadow-sm"
                >
                  {HOMEPAGE_CONTENT.hero.secondaryCta.label}
                </Link>

                <Link
                  href={HOMEPAGE_CONTENT.hero.patientCta.href}
                  className="px-4 py-3.5 rounded-xl text-[#334155] hover:text-[#1B4332] font-semibold text-sm flex items-center gap-1.5 transition"
                >
                  <HealthcareIcon name="lock" className="w-4 h-4 text-[#2D6A4F]" />
                  <span>{HOMEPAGE_CONTENT.hero.patientCta.label}</span>
                </Link>
              </div>

              {/* Clinical Trust & Emergency Guidance */}
              <div className="pt-4 border-t border-[#E2E8F0] max-w-xl space-y-2">
                <p className="text-xs text-[#64748B] leading-relaxed flex items-start gap-2">
                  <HealthcareIcon name="shield-check" className="w-4 h-4 text-[#2D6A4F] shrink-0 mt-0.5" />
                  <span>{HOMEPAGE_CONTENT.hero.trustStatement}</span>
                </p>
              </div>
            </div>

            {/* Right Column: Restrained Institutional Visual Card */}
            <div className="lg:col-span-5">
              <div className="rounded-3xl bg-white border border-[#E2E8F0] p-6 shadow-xl space-y-5">
                <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-11 h-11 rounded-2xl bg-[#E8F5E9] flex items-center justify-center text-[#1B4332]">
                      <HealthcareIcon name="stethoscope" className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-[#0F172A]">Individualized Consultation</h3>
                      <p className="text-xs text-[#64748B]">ZAYVORA Matab™ Clinical Model</p>
                    </div>
                  </div>
                  <span className="px-2.5 py-1 rounded-full text-[11px] font-bold bg-[#E8F5E9] text-[#1B4332]">
                    NCISM Governed
                  </span>
                </div>

                <div className="space-y-3 text-xs">
                  <div className="p-3.5 rounded-2xl bg-[#F8FAFC] border border-[#E2E8F0] space-y-1">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-[#1B4332] block">
                      Constitutional Evaluation
                    </span>
                    <p className="text-[#334155]">
                      Mizaj-e-Asli (baseline temperament) determination and Su-e-Mizaj (acquired dyscrasia) staging within classical Unani medicine.
                    </p>
                  </div>

                  <div className="p-3.5 rounded-2xl bg-[#F8FAFC] border border-[#E2E8F0] space-y-1">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-[#1B4332] block">
                      Individualized Nuskha & Diet
                    </span>
                    <p className="text-[#334155]">
                      Standardized botanical formulations aligned with Asbab-e-Sitta lifestyle and dietary directives.
                    </p>
                  </div>

                  <div className="p-3.5 rounded-2xl bg-[#F8FAFC] border border-[#E2E8F0] space-y-1">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-[#1B4332] block">
                      Medication Safety Review
                    </span>
                    <p className="text-[#334155]">
                      Relevant contraindications, precautions, and herb-drug interactions are systematically reviewed prior to dispensing.
                    </p>
                  </div>
                </div>

                <div className="pt-2">
                  <Link
                    href="/book"
                    className="w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white text-xs font-semibold transition"
                  >
                    <span>Schedule Clinical Consultation</span>
                    <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* ── 2. WHY ZAYVORA? BRAND COMMITMENTS ─────────────────────────── */}
      <section className="py-16 sm:py-20 bg-white border-b border-[#E2E8F0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mb-12">
            <span className="text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
              Clinical Philosophy
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] mt-2">
              {HOMEPAGE_CONTENT.whyZayvora.heading}
            </h2>
            <p className="text-sm sm:text-base text-[#475569] mt-2 leading-relaxed">
              {HOMEPAGE_CONTENT.whyZayvora.subheading}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {HOMEPAGE_CONTENT.whyZayvora.commitments.map((item, idx) => (
              <div
                key={idx}
                className="p-6 rounded-2xl bg-[#FAFAF7] border border-[#E2E8F0] hover:border-[#CBD5E1] transition space-y-3"
              >
                <div className="w-10 h-10 rounded-xl bg-[#E8F5E9] flex items-center justify-center text-[#1B4332] font-mono text-sm font-bold">
                  0{idx + 1}
                </div>
                <h3 className="text-base font-bold text-[#0F172A]">{item.title}</h3>
                <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed">
                  {item.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── 3. FIND THE RIGHT CARE DISCOVERY MODULE ────────────────────── */}
      <section className="py-16 sm:py-20 bg-[#F4F6F0] border-b border-[#E2E8F0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mb-10">
            <span className="text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
              Clinical Navigation
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] mt-2">
              {HOMEPAGE_CONTENT.findCare.heading}
            </h2>
            <p className="text-sm sm:text-base text-[#475569] mt-2 leading-relaxed">
              {HOMEPAGE_CONTENT.findCare.subheading}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {filteredCareCategories.map((cat) => (
              <div
                key={cat.id}
                className="p-6 rounded-2xl bg-white border border-[#E2E8F0] hover:border-[#CBD5E1] transition shadow-sm flex flex-col justify-between"
              >
                <div className="space-y-2.5">
                  <div className="w-10 h-10 rounded-xl bg-[#E8F5E9] flex items-center justify-center text-[#1B4332]">
                    <HealthcareIcon name="heart-pulse" className="w-5 h-5" />
                  </div>
                  <h3 className="text-sm font-bold text-[#0F172A]">{cat.name}</h3>
                  <p className="text-xs text-[#64748B] leading-relaxed">
                    {cat.description}
                  </p>
                </div>
                <div className="pt-4 mt-4 border-t border-[#F1F5F9] flex items-center justify-between">
                  <Link
                    href={`/conditions/${cat.slug}`}
                    className="text-xs font-semibold text-[#1B4332] hover:text-[#2D6A4F] flex items-center gap-1"
                  >
                    <span>Condition Guide</span>
                    <HealthcareIcon name="arrow-right" className="w-3 h-3" />
                  </Link>
                  <Link
                    href={`/book?concern=${cat.concern}`}
                    className="px-2.5 py-1 rounded-lg bg-[#E8F5E9] text-[#1B4332] hover:bg-[#1B4332] hover:text-white transition text-xs font-bold"
                  >
                    Book Care
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── 4. WHAT IS ZAYVORA SECTION ─────────────────────────────────── */}
      <section id="care-approach" className="py-16 sm:py-20 bg-white border-b border-[#E2E8F0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mb-12">
            <span className="text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
              Integrative Methodology
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] mt-2">
              {HOMEPAGE_CONTENT.whatIsZayvora.heading}
            </h2>
            <p className="text-sm sm:text-base text-[#475569] mt-3 leading-relaxed">
              {HOMEPAGE_CONTENT.whatIsZayvora.description}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {HOMEPAGE_CONTENT.whatIsZayvora.pillars.map((pillar, idx) => (
              <div
                key={idx}
                className="p-6 rounded-2xl bg-[#FAFAF7] border border-[#E2E8F0] hover:border-[#CBD5E1] transition space-y-3"
              >
                <div className="w-10 h-10 rounded-xl bg-[#E8F5E9] flex items-center justify-center text-[#1B4332]">
                  <HealthcareIcon name={pillar.iconKey} className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-[#0F172A]">{pillar.title}</h3>
                <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed">
                  {pillar.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── 5. HOW CARE WORKS (MASTER PROMPT §76: 6-STEP CARE CONTINUUM) ─── */}
      <section className="py-16 sm:py-24 bg-[#FAFAF7] border-b border-[#E2E8F0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* Section Header */}
          <div className="text-center max-w-3xl mx-auto mb-12">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E8F5E9] border border-[#C8E6C9] text-xs font-semibold text-[#1B4332] mb-3">
              <HealthcareIcon name="shield-check" className="w-3.5 h-3.5 text-[#2D6A4F]" />
              <span>{HOMEPAGE_CONTENT.howCareWorks.eyebrow}</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-[#0F172A] tracking-tight">
              {HOMEPAGE_CONTENT.howCareWorks.heading}
            </h2>
            <p className="text-sm sm:text-base text-[#64748B] mt-3 leading-relaxed">
              {HOMEPAGE_CONTENT.howCareWorks.subheading}
            </p>
          </div>

          {/* Interactive Stepper Navigation Bar */}
          <div className="hidden lg:grid grid-cols-6 gap-2 p-2 bg-white rounded-2xl border border-[#E2E8F0] shadow-sm mb-8">
            {HOMEPAGE_CONTENT.howCareWorks.steps.map((st, idx) => {
              const isActive = activeCareStep === idx;
              return (
                <button
                  key={st.step}
                  onClick={() => setActiveCareStep(idx)}
                  className={`p-3 rounded-xl text-left transition-all duration-200 flex flex-col justify-between ${
                    isActive
                      ? "bg-[#1B4332] text-white shadow-md shadow-[#1B4332]/20"
                      : "hover:bg-[#F8FAFC] text-[#334155]"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className={`text-[10px] font-mono font-bold ${isActive ? "text-[#A7F3D0]" : "text-[#2D6A4F]"}`}>
                      {st.step}
                    </span>
                    <span className={`text-[9px] uppercase tracking-wider font-semibold px-1.5 py-0.5 rounded ${
                      isActive ? "bg-white/20 text-white" : "bg-[#E8F5E9] text-[#1B4332]"
                    }`}>
                      {st.stage}
                    </span>
                  </div>
                  <p className={`text-xs font-bold mt-2 truncate ${isActive ? "text-white" : "text-[#0F172A]"}`}>
                    {st.title}
                  </p>
                </button>
              );
            })}
          </div>

          {/* Active Step Highlighted Detail Panel */}
          {HOMEPAGE_CONTENT.howCareWorks.steps[activeCareStep] && (
            <div className="mb-12 p-6 sm:p-8 rounded-3xl bg-white border border-[#CBD5E1] shadow-lg relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-[#2D6A4F] via-[#52B788] to-[#1B4332]" />
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
                <div className="lg:col-span-8 space-y-3">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="px-2.5 py-1 rounded-full text-xs font-mono font-bold bg-[#E8F5E9] text-[#1B4332]">
                      STAGE {HOMEPAGE_CONTENT.howCareWorks.steps[activeCareStep].step}
                    </span>
                    <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-[#F1F5F9] text-[#475569]">
                      {HOMEPAGE_CONTENT.howCareWorks.steps[activeCareStep].stage}
                    </span>
                    <span className="text-xs font-serif italic text-[#2D6A4F] font-semibold bg-[#E8F5E9]/50 px-2 py-0.5 rounded">
                      {HOMEPAGE_CONTENT.howCareWorks.steps[activeCareStep].unaniTerm}
                    </span>
                  </div>
                  <h3 className="text-xl sm:text-2xl font-extrabold text-[#0F172A]">
                    {HOMEPAGE_CONTENT.howCareWorks.steps[activeCareStep].title}
                  </h3>
                  <p className="text-sm text-[#475569] leading-relaxed">
                    {HOMEPAGE_CONTENT.howCareWorks.steps[activeCareStep].description}
                  </p>
                </div>
                <div className="lg:col-span-4 flex flex-col sm:flex-row lg:flex-col gap-3 justify-center items-stretch lg:items-end">
                  <Link
                    href="/book"
                    className="px-5 py-3 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white text-xs font-semibold text-center transition flex items-center justify-center gap-2 shadow-sm"
                  >
                    <span>Book Clinical Consultation</span>
                    <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
                  </Link>
                  <Link
                    href="/patient"
                    className="px-5 py-3 rounded-xl bg-[#F8FAFC] hover:bg-[#F1F5F9] text-[#1B4332] border border-[#CBD5E1] text-xs font-semibold text-center transition"
                  >
                    <span>Explore Patient Portal</span>
                  </Link>
                </div>
              </div>
            </div>
          )}

          {/* All 6 Steps Grid (Mobile & Desktop Full Overview) */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {HOMEPAGE_CONTENT.howCareWorks.steps.map((st, idx) => {
              const isSelected = activeCareStep === idx;
              return (
                <div
                  key={st.step}
                  onClick={() => setActiveCareStep(idx)}
                  className={`p-6 rounded-2xl cursor-pointer transition-all duration-200 border relative flex flex-col justify-between ${
                    isSelected
                      ? "bg-white border-[#2D6A4F] ring-2 ring-[#2D6A4F]/20 shadow-md"
                      : "bg-white border-[#E2E8F0] hover:border-[#CBD5E1] shadow-sm"
                  }`}
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-xl font-black text-[#2D6A4F]">
                        {st.step}
                      </span>
                      <span className="text-[11px] font-semibold text-[#1B4332] bg-[#E8F5E9] px-2 py-0.5 rounded-full">
                        {st.stage}
                      </span>
                    </div>
                    <div className="text-[11px] font-serif italic text-[#2D6A4F]">
                      {st.unaniTerm}
                    </div>
                    <h3 className="text-base font-bold text-[#0F172A] leading-snug">
                      {st.title}
                    </h3>
                    <p className="text-xs text-[#64748B] leading-relaxed">
                      {st.description}
                    </p>
                  </div>

                  <div className="pt-4 mt-4 border-t border-[#F1F5F9] flex items-center justify-between text-[11px]">
                    <span className="text-[#64748B]">Clinical Deliverable</span>
                    <span className="font-semibold text-[#2D6A4F] flex items-center gap-1">
                      <span>View details</span>
                      <HealthcareIcon name="arrow-right" className="w-3 h-3" />
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* ── 5B. INTERACTIVE MIZAJ TENDENCY PREVIEW TEASER ─────────────── */}
          <div className="mt-16 bg-white rounded-3xl border border-[#CBD5E1] p-6 sm:p-10 shadow-lg">
            <div className="max-w-3xl mx-auto">
              <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-4 mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-2xl bg-[#E8F5E9] flex items-center justify-center text-[#1B4332]">
                    <HealthcareIcon name="leaf" className="w-5 h-5 text-[#2D6A4F]" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-[#0F172A]">
                      Discover Your Constitutional Mizaj Tendency
                    </h3>
                    <p className="text-xs text-[#64748B]">
                      A 45-second educational preview based on classical Greco-Arab Unani physiology.
                    </p>
                  </div>
                </div>
                <span className="hidden sm:inline-block px-2.5 py-1 rounded-full text-[11px] font-bold bg-[#E8F5E9] text-[#1B4332]">
                  Educational Screener
                </span>
              </div>

              {/* Step 1: Thermal Question */}
              {mizajQuestionStep === 0 && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between text-xs font-semibold text-[#64748B]">
                    <span>QUESTION 1 OF 3</span>
                    <span>Thermal Sensitivity</span>
                  </div>
                  <p className="text-sm sm:text-base font-bold text-[#0F172A]">
                    How does your body typically respond to temperature and seasonal changes?
                  </p>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
                    <button
                      onClick={() => handleMizajOption("thermal", "warm")}
                      className="p-4 rounded-xl border border-[#E2E8F0] hover:border-[#2D6A4F] hover:bg-[#F8FAFC] text-left transition space-y-1"
                    >
                      <p className="text-xs font-bold text-[#0F172A]">Hot / Warm Tolerance Low</p>
                      <p className="text-[11px] text-[#64748B]">I feel heated easily, prefer cool breeze, crave cold drinks.</p>
                    </button>
                    <button
                      onClick={() => handleMizajOption("thermal", "cold")}
                      className="p-4 rounded-xl border border-[#E2E8F0] hover:border-[#2D6A4F] hover:bg-[#F8FAFC] text-left transition space-y-1"
                    >
                      <p className="text-xs font-bold text-[#0F172A]">Cold Sensitivity</p>
                      <p className="text-[11px] text-[#64748B]">Hands/feet get cold easily, prefer sunshine, warm beverages.</p>
                    </button>
                    <button
                      onClick={() => handleMizajOption("thermal", "moderate")}
                      className="p-4 rounded-xl border border-[#E2E8F0] hover:border-[#2D6A4F] hover:bg-[#F8FAFC] text-left transition space-y-1"
                    >
                      <p className="text-xs font-bold text-[#0F172A]">Balanced Adaptation</p>
                      <p className="text-[11px] text-[#64748B]">Tolerate both heat and cold comfortably without distress.</p>
                    </button>
                  </div>
                </div>
              )}

              {/* Step 2: Digestion & Energy */}
              {mizajQuestionStep === 1 && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between text-xs font-semibold text-[#64748B]">
                    <span>QUESTION 2 OF 3</span>
                    <span>Metabolism & Digestion</span>
                  </div>
                  <p className="text-sm sm:text-base font-bold text-[#0F172A]">
                    How would you describe your hunger, digestion rate, and physical vitality?
                  </p>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
                    <button
                      onClick={() => handleMizajOption("digestion", "active")}
                      className="p-4 rounded-xl border border-[#E2E8F0] hover:border-[#2D6A4F] hover:bg-[#F8FAFC] text-left transition space-y-1"
                    >
                      <p className="text-xs font-bold text-[#0F172A]">Quick & Sharp</p>
                      <p className="text-[11px] text-[#64748B]">Frequent strong appetite, rapid digestion, high burning rate.</p>
                    </button>
                    <button
                      onClick={() => handleMizajOption("digestion", "moderate")}
                      className="p-4 rounded-xl border border-[#E2E8F0] hover:border-[#2D6A4F] hover:bg-[#F8FAFC] text-left transition space-y-1"
                    >
                      <p className="text-xs font-bold text-[#0F172A]">Regular & Robust</p>
                      <p className="text-[11px] text-[#64748B]">Consistent appetite at regular hours, steady stamina.</p>
                    </button>
                    <button
                      onClick={() => handleMizajOption("digestion", "slow")}
                      className="p-4 rounded-xl border border-[#E2E8F0] hover:border-[#2D6A4F] hover:bg-[#F8FAFC] text-left transition space-y-1"
                    >
                      <p className="text-xs font-bold text-[#0F172A]">Sluggish & Heavy</p>
                      <p className="text-[11px] text-[#64748B]">Slow transit, feeling full for hours, tendency to retain water.</p>
                    </button>
                  </div>
                </div>
              )}

              {/* Step 3: Sleep & Mind */}
              {mizajQuestionStep === 2 && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between text-xs font-semibold text-[#64748B]">
                    <span>QUESTION 3 OF 3</span>
                    <span>Sleep & Nervous Rhythm</span>
                  </div>
                  <p className="text-sm sm:text-base font-bold text-[#0F172A]">
                    What is your prevailing sleep pattern and emotional recovery rhythm?
                  </p>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
                    <button
                      onClick={() => handleMizajOption("sleep", "deep")}
                      className="p-4 rounded-xl border border-[#E2E8F0] hover:border-[#2D6A4F] hover:bg-[#F8FAFC] text-left transition space-y-1"
                    >
                      <p className="text-xs font-bold text-[#0F172A]">Deep & Prolonged</p>
                      <p className="text-[11px] text-[#64748B]">Heavy restorative sleep, peaceful mind, slow to wake.</p>
                    </button>
                    <button
                      onClick={() => handleMizajOption("sleep", "balanced")}
                      className="p-4 rounded-xl border border-[#E2E8F0] hover:border-[#2D6A4F] hover:bg-[#F8FAFC] text-left transition space-y-1"
                    >
                      <p className="text-xs font-bold text-[#0F172A]">Refreshing & Moderate</p>
                      <p className="text-[11px] text-[#64748B]">6-7 hours sufficient, wake up alert with clear focus.</p>
                    </button>
                    <button
                      onClick={() => handleMizajOption("sleep", "light")}
                      className="p-4 rounded-xl border border-[#E2E8F0] hover:border-[#2D6A4F] hover:bg-[#F8FAFC] text-left transition space-y-1"
                    >
                      <p className="text-xs font-bold text-[#0F172A]">Light & Interrupted</p>
                      <p className="text-[11px] text-[#64748B]">Easily startled awake, active thoughts, occasional restless nights.</p>
                    </button>
                  </div>
                </div>
              )}

              {/* Result State */}
              {mizajQuestionStep === 3 && mizajResult && (
                <div className="space-y-5 animate-fadeIn">
                  <div className="p-5 rounded-2xl bg-[#E8F5E9]/60 border border-[#A7F3D0] space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-mono font-bold text-[#1B4332]">PRELIMINARY TENDENCY</span>
                      <span className="text-xs font-bold text-[#2D6A4F]">{mizajResult.english}</span>
                    </div>
                    <h4 className="text-xl font-extrabold text-[#0F172A]">
                      {mizajResult.mizaj}
                    </h4>
                    <p className="text-xs font-medium text-[#1B4332]">
                      {mizajResult.qualities}
                    </p>
                    <p className="text-xs text-[#334155] leading-relaxed pt-1">
                      {mizajResult.description}
                    </p>
                    <div className="pt-2 border-t border-[#A7F3D0]/60">
                      <span className="text-[11px] font-bold text-[#1B4332] block">Asbab-e-Sittah Lifestyle Focus:</span>
                      <p className="text-[11px] text-[#334155]">{mizajResult.asbabTips}</p>
                    </div>
                  </div>

                  <div className="p-3.5 rounded-xl bg-[#F8FAFC] border border-[#E2E8F0] flex items-start gap-2 text-xs text-[#64748B]">
                    <HealthcareIcon name="shield-check" className="w-4 h-4 text-[#2D6A4F] shrink-0 mt-0.5" />
                    <span>
                      <strong>Clinical Notice:</strong> This preview is educational. A definitive Unani diagnosis requires clinical examination of pulse (Nabz), urine (Baul), and physical habitus (Ajnas-e-Ashara) by a licensed practitioner under NCISM guidelines.
                    </span>
                  </div>

                  <div className="flex flex-wrap items-center gap-3 pt-1">
                    <Link
                      href="/book"
                      className="px-6 py-3 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white text-xs font-semibold flex items-center gap-2 shadow-sm transition"
                    >
                      <HealthcareIcon name="calendar" className="w-3.5 h-3.5 text-[#A7F3D0]" />
                      <span>Book Formal Assessment with Clinician</span>
                    </Link>
                    <button
                      onClick={resetMizajTeaser}
                      className="px-4 py-3 rounded-xl bg-white hover:bg-[#F8FAFC] text-[#334155] border border-[#CBD5E1] text-xs font-semibold transition"
                    >
                      Retake Screener
                    </button>
                  </div>
                </div>
              )}

            </div>
          </div>

        </div>
      </section>

      {/* ── 6. SIGNATURE ZAYVORA CLINICAL FRAMEWORK FLOW ────────────────── */}
      <section className="py-16 sm:py-20 bg-[#1B4332] text-white border-b border-[#2D6A4F]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mb-12">
            <span className="text-xs font-bold uppercase tracking-wider text-[#A7F3D0]">
              Signature Clinical Architecture
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-2">
              {HOMEPAGE_CONTENT.clinicalFramework.heading}
            </h2>
            <p className="text-sm text-[#D8F3DC] mt-2">
              {HOMEPAGE_CONTENT.clinicalFramework.subheading}
            </p>
          </div>

          {/* Horizontal Linear Clinical Thread Flow */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
            {HOMEPAGE_CONTENT.clinicalFramework.flowStages.map((stage, idx) => (
              <div
                key={idx}
                className="p-4 rounded-2xl bg-white/10 border border-white/20 space-y-2 backdrop-blur-sm"
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono text-[#A7F3D0] font-bold">STAGE 0{idx + 1}</span>
                  <HealthcareIcon name="check" className="w-3.5 h-3.5 text-[#52B788]" />
                </div>
                <h4 className="text-xs font-bold text-white leading-snug">{stage.name}</h4>
                <p className="text-[11px] text-[#B7E4C7] leading-relaxed">{stage.role}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── 7. STRUCTURED CLINICAL CARE AREAS ──────────────────────────── */}
      <section className="py-16 sm:py-20 bg-white border-b border-[#E2E8F0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mb-10">
            <span className="text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
              Clinical Specialties
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] mt-2">
              {HOMEPAGE_CONTENT.careAreas.heading}
            </h2>
            <p className="text-sm text-[#64748B] mt-2">
              {HOMEPAGE_CONTENT.careAreas.subheading}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {HOMEPAGE_CONTENT.careAreas.areas.map((area) => (
              <div
                key={area.id}
                className="p-6 rounded-2xl bg-[#FAFAF7] border border-[#E2E8F0] hover:border-[#CBD5E1] transition flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="w-9 h-9 rounded-xl bg-[#E8F5E9] flex items-center justify-center text-[#1B4332]">
                    <HealthcareIcon name="heart-pulse" className="w-4 h-4" />
                  </div>
                  <h3 className="text-base font-bold text-[#0F172A]">{area.title}</h3>
                  <p className="text-xs text-[#64748B] leading-relaxed">
                    {area.description}
                  </p>
                </div>
                <div className="pt-4 mt-4 border-t border-[#E2E8F0]">
                  <Link
                    href={area.href}
                    className="text-xs font-semibold text-[#1B4332] hover:text-[#2D6A4F] flex items-center gap-1"
                  >
                    <span>View Care Pathway</span>
                    <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── 8. PATIENT PORTAL SPOTLIGHT (MY ZAYVORA™) ──────────────────── */}
      <section className="py-16 sm:py-20 bg-[#F4F6F0] border-b border-[#E2E8F0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
            
            <div className="lg:col-span-6 space-y-5">
              <span className="text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
                Digital Care Continuity
              </span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A]">
                {HOMEPAGE_CONTENT.patientPortal.heading}
              </h2>
              <p className="text-sm text-[#64748B] leading-relaxed">
                {HOMEPAGE_CONTENT.patientPortal.subheading}
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                {HOMEPAGE_CONTENT.patientPortal.capabilities.map((cap, idx) => (
                  <div key={idx} className="p-3.5 rounded-xl bg-white border border-[#E2E8F0] space-y-1">
                    <h4 className="text-xs font-bold text-[#0F172A]">{cap.title}</h4>
                    <p className="text-[11px] text-[#64748B] leading-snug">{cap.desc}</p>
                  </div>
                ))}
              </div>

              <div className="pt-2">
                <Link
                  href={HOMEPAGE_CONTENT.patientPortal.cta.href}
                  className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white font-semibold text-xs transition shadow-sm"
                >
                  <HealthcareIcon name="lock" className="w-4 h-4 text-[#A7F3D0]" />
                  <span>{HOMEPAGE_CONTENT.patientPortal.cta.label}</span>
                </Link>
              </div>
            </div>

            <div className="lg:col-span-6">
              <div className="p-6 rounded-3xl bg-white border border-[#E2E8F0] shadow-lg space-y-4">
                <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-3">
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-full bg-[#E8F5E9] flex items-center justify-center font-bold text-xs text-[#1B4332]">
                      PT
                    </div>
                    <div>
                      <p className="text-xs font-bold text-[#0F172A]">My ZAYVORA™ Health Portal</p>
                      <p className="text-[10px] text-[#64748B]">Personal Health Record</p>
                    </div>
                  </div>
                  <span className="text-[10px] font-bold bg-[#E8F5E9] text-[#1B4332] px-2 py-0.5 rounded-md">
                    DPDP Act 2023 Encrypted
                  </span>
                </div>

                <div className="space-y-2.5 text-xs">
                  <div className="p-3 rounded-xl bg-[#FAFAF7] border border-[#E2E8F0] flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-[#0F172A]">Next Scheduled Appointment</p>
                      <p className="text-[11px] text-[#64748B]">Consultation with Dr. Mansoor Alam</p>
                    </div>
                    <span className="text-[11px] font-mono font-bold text-[#1B4332]">Token #T-104</span>
                  </div>

                  <div className="p-3 rounded-xl bg-[#FAFAF7] border border-[#E2E8F0] flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-[#0F172A]">Active Prescription (Nuskha)</p>
                      <p className="text-[11px] text-[#64748B]">Hab-e-Suranjan & Roghan-e-Balsan</p>
                    </div>
                    <span className="text-[10px] font-semibold text-[#2D6A4F] bg-[#E8F5E9] px-2 py-0.5 rounded-md">
                      Verified Safety Review
                    </span>
                  </div>

                  <div className="p-3 rounded-xl bg-[#FAFAF7] border border-[#E2E8F0] flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-[#0F172A]">Recent Lab Diagnostic Review</p>
                      <p className="text-[11px] text-[#64748B]">Serum Uric Acid: 6.8 mg/dL (Normal Range)</p>
                    </div>
                    <span className="text-[10px] font-semibold text-[#2D6A4F]">Physician Reviewed</span>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* ── 9. INSTITUTIONAL TRUST & SAFETY ARCHITECTURE ───────────────── */}
      <section className="py-16 sm:py-20 bg-white border-b border-[#E2E8F0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mb-12">
            <span className="text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
              Institutional Governance
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] mt-2">
              {HOMEPAGE_CONTENT.trustArchitecture.heading}
            </h2>
            <p className="text-sm sm:text-base text-[#64748B] mt-2">
              {HOMEPAGE_CONTENT.trustArchitecture.subheading}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {HOMEPAGE_CONTENT.trustArchitecture.items.map((item, idx) => (
              <div
                key={idx}
                className="p-6 rounded-2xl bg-[#FAFAF7] border border-[#E2E8F0] hover:border-[#CBD5E1] transition flex flex-col justify-between"
              >
                <div className="space-y-2.5">
                  <div className="w-8 h-8 rounded-lg bg-[#E8F5E9] flex items-center justify-center text-[#1B4332]">
                    <HealthcareIcon name="shield-check" className="w-4 h-4 text-[#2D6A4F]" />
                  </div>
                  <h4 className="text-sm font-bold text-[#0F172A]">{item.title}</h4>
                  <p className="text-xs text-[#64748B] leading-relaxed">{item.description}</p>
                </div>
                <div className="pt-3 mt-3 border-t border-[#E2E8F0]">
                  <Link
                    href={item.href}
                    className="text-xs font-semibold text-[#1B4332] hover:text-[#2D6A4F] flex items-center gap-1"
                  >
                    <span>Read Policy</span>
                    <HealthcareIcon name="arrow-right" className="w-3 h-3" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── 10. CLINICAL TEAM PREVIEW ───────────────────────────────────── */}
      <section className="py-16 sm:py-20 bg-[#FAFAF7] border-b border-[#E2E8F0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-10">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
                Medical Leadership
              </span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] mt-2">
                Meet the Clinicians Behind Your Care
              </h2>
            </div>
            <Link
              href="/doctors"
              className="text-xs font-semibold text-[#1B4332] hover:text-[#2D6A4F] flex items-center gap-1 self-start sm:self-auto"
            >
              <span>View All Clinicians</span>
              <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {CLINICAL_TEAM.slice(0, 3).map((doc) => (
              <div
                key={doc.id}
                className="p-6 rounded-2xl bg-white border border-[#E2E8F0] space-y-4 shadow-sm"
              >
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-2xl bg-[#E8F5E9] flex items-center justify-center text-sm font-bold text-[#1B4332]">
                    MD
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-[#0F172A]">{doc.name}</h4>
                    <p className="text-[11px] text-[#64748B]">{doc.qualifications}</p>
                  </div>
                </div>

                <div className="text-xs text-[#475569] space-y-1 border-t border-[#F1F5F9] pt-3">
                  <p><strong>Department:</strong> {doc.specialty}</p>
                  <p><strong>Experience:</strong> {doc.experienceYears} Years Clinical Practice</p>
                  <p className="text-[11px] text-[#64748B] font-mono">Council Reg: {doc.registrationNumber}</p>
                </div>

                <div className="pt-2">
                  <Link
                    href={`/book?doctor=${doc.id}`}
                    className="w-full flex items-center justify-center gap-1.5 py-2 rounded-xl bg-[#F8FAFC] hover:bg-[#E8F5E9] text-[#1B4332] text-xs font-semibold border border-[#E2E8F0] transition"
                  >
                    <span>Book Consultation</span>
                    <HealthcareIcon name="arrow-right" className="w-3 h-3" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── 11. HEALTH LIBRARY SPOTLIGHT ────────────────────────────────── */}
      <section className="py-16 sm:py-20 bg-white border-b border-[#E2E8F0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-10">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
                Evidence-Based Articles
              </span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] mt-2">
                Clinician-Reviewed Health Library
              </h2>
            </div>
            <Link
              href="/health-library"
              className="text-xs font-semibold text-[#1B4332] hover:text-[#2D6A4F] flex items-center gap-1 self-start sm:self-auto"
            >
              <span>Explore All Articles</span>
              <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {HEALTH_LIBRARY_ARTICLES.slice(0, 3).map((art) => (
              <div
                key={art.slug}
                className="p-6 rounded-2xl bg-[#FAFAF7] border border-[#E2E8F0] flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#E8F5E9] text-[#1B4332]">
                    {art.category}
                  </span>
                  <h3 className="text-base font-bold text-[#0F172A] leading-snug">{art.title}</h3>
                  <p className="text-xs text-[#64748B] line-clamp-3 leading-relaxed">
                    {art.summary}
                  </p>
                </div>

                <div className="pt-4 mt-4 border-t border-[#E2E8F0] flex items-center justify-between text-xs">
                  <span className="text-[#64748B] text-[11px] flex items-center gap-1">
                    <HealthcareIcon name="clock" className="w-3.5 h-3.5 text-[#64748B]" />
                    <span>{art.readingTimeMinutes} min read</span>
                  </span>
                  <Link
                    href={`/health-library/${art.slug}`}
                    className="font-bold text-[#1B4332] hover:text-[#2D6A4F] flex items-center gap-1"
                  >
                    <span>Read</span>
                    <HealthcareIcon name="arrow-right" className="w-3 h-3" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── 12. FINAL CLINICAL CONSULTATION CTA ─────────────────────────── */}
      <section className="py-16 sm:py-24 bg-[#1B4332] text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            {HOMEPAGE_CONTENT.finalCta.heading}
          </h2>
          <p className="text-base text-[#D8F3DC] max-w-2xl mx-auto leading-relaxed">
            {HOMEPAGE_CONTENT.finalCta.body}
          </p>

          <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
            <Link
              href={HOMEPAGE_CONTENT.finalCta.primaryBtn.href}
              className="px-6 py-3.5 rounded-xl bg-white hover:bg-[#F8FAFC] text-[#1B4332] font-semibold text-sm shadow-sm transition"
            >
              {HOMEPAGE_CONTENT.finalCta.primaryBtn.label}
            </Link>
            <Link
              href={HOMEPAGE_CONTENT.finalCta.secondaryBtn.href}
              className="px-6 py-3.5 rounded-xl bg-[#2D6A4F] hover:bg-[#40916C] text-white font-semibold text-sm transition"
            >
              {HOMEPAGE_CONTENT.finalCta.secondaryBtn.label}
            </Link>
          </div>
        </div>
      </section>
    </PublicWebsiteShell>
  );
}
