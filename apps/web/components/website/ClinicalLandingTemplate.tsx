"use client";

import React, { useState } from "react";
import Link from "next/link";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export interface ClinicalReference {
  title: string;
  source: string;
  year?: string;
  doiOrUrl?: string;
  type: "classical" | "contemporary";
}

export interface FaqItem {
  question: string;
  answer: string;
}

export interface ClinicalSpecialtyData {
  slug: string;
  name: string;
  classicalNomenclature: string;
  badge: string;
  shortSummary: string;
  fullOverview: string;
  targetAudience: string[];
  symptoms: string[];
  clinicalApproach: {
    title: string;
    description: string;
  }[];
  unaniFramework: {
    mizajImpact: string;
    organAxis: string;
    humoralPathology: string;
    asbabConsiderations: string[];
  };
  biomedicalCorroboration: {
    biomarkers: string[];
    monitoring: string;
    integrativeSafety: string;
  };
  consultationIncludes: string[];
  redFlagSafety: {
    emergencySymptoms: string[];
    exclusionCriteria: string[];
    advisory: string;
  };
  clinicianTeam: {
    name: string;
    role: string;
    regNumber: string;
    qualification: string;
  }[];
  faqs: FaqItem[];
  references: ClinicalReference[];
  governance: {
    author: string;
    authorRole: string;
    reviewer: string;
    reviewerRegNumber: string;
    lastReviewed: string;
    version: string;
    nextAuditDue: string;
  };
}

export function ClinicalLandingTemplate({ data }: { data: ClinicalSpecialtyData }) {
  const [openFaq, setOpenFaq] = useState<number | null>(0);

  return (
    <div className="space-y-16 py-8">
      {/* 1. HERO BANNER */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-[#1B4332] via-[#2D6A4F] to-[#0F172A] text-white p-8 sm:p-12 lg:p-16 shadow-xl">
        <div className="max-w-4xl space-y-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 border border-white/20 backdrop-blur-sm text-xs font-semibold text-emerald-200">
            <HealthcareIcon name="shield-check" className="w-4 h-4 text-emerald-300" />
            <span>{data.badge}</span>
            <span className="opacity-40">•</span>
            <span className="text-xs font-medium text-emerald-200">{data.classicalNomenclature}</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
            {data.name}
          </h1>

          <p className="text-base sm:text-lg text-emerald-100/90 leading-relaxed max-w-3xl">
            {data.shortSummary}
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-2">
            <Link
              href="/booking"
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-sm shadow-md transition transform active:scale-95"
            >
              <HealthcareIcon name="calendar" className="w-4 h-4 text-slate-950" />
              <span>Book Clinical Consultation</span>
            </Link>
            <Link
              href="/team"
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-white/10 hover:bg-white/20 border border-white/30 text-white font-semibold text-sm backdrop-blur-sm transition"
            >
              <HealthcareIcon name="users" className="w-4 h-4 text-white" />
              <span>Meet the Faculty</span>
            </Link>
          </div>

          <div className="pt-6 border-t border-white/10 grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
            <div>
              <span className="block text-emerald-300/80 uppercase font-bold tracking-wider text-[10px]">Framework</span>
              <span className="font-semibold text-white">10-Ajnas Pulse & Mizaj</span>
            </div>
            <div>
              <span className="block text-emerald-300/80 uppercase font-bold tracking-wider text-[10px]">Verification</span>
              <span className="font-semibold text-white">21 CFR Part 11 Digital Seal</span>
            </div>
            <div>
              <span className="block text-emerald-300/80 uppercase font-bold tracking-wider text-[10px]">Practitioners</span>
              <span className="font-semibold text-white">NCISM Act 2020 Registered</span>
            </div>
            <div>
              <span className="block text-emerald-300/80 uppercase font-bold tracking-wider text-[10px]">Data Protection</span>
              <span className="font-semibold text-white">DPDP Act 2023 Compliant</span>
            </div>
          </div>
        </div>
      </section>

      {/* 2. CLINICAL OVERVIEW */}
      <section className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <div className="lg:col-span-8 p-8 rounded-3xl bg-white border border-slate-200/80 shadow-sm space-y-4">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
            <HealthcareIcon name="stethoscope" className="w-4 h-4 text-[#2D6A4F]" />
            <span>Clinical Overview</span>
          </div>
          <h2 className="text-2xl font-bold text-[#0F172A]">Understanding the Condition & Etiology</h2>
          <p className="text-sm sm:text-base text-slate-700 leading-relaxed whitespace-pre-line">
            {data.fullOverview}
          </p>
        </div>

        <div className="lg:col-span-4 p-6 rounded-3xl bg-[#F4F6F0] border border-[#E2E8D8] space-y-4">
          <h3 className="text-sm font-bold uppercase tracking-wider text-[#1B4332] flex items-center gap-2">
            <HealthcareIcon name="shield-check" className="w-4 h-4 text-[#2D6A4F]" />
            Clinical Assurance
          </h3>
          <ul className="text-xs text-slate-700 space-y-2.5">
            <li className="flex items-start gap-2">
              <HealthcareIcon name="check" className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
              <span>Evidence-based classical Unani formulation protocols.</span>
            </li>
            <li className="flex items-start gap-2">
              <HealthcareIcon name="check" className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
              <span>Schedule E(1) Mudabbar verification mandatory for safe dispensing.</span>
            </li>
            <li className="flex items-start gap-2">
              <HealthcareIcon name="check" className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
              <span>Continuous cross-referencing with contemporary clinical biomarkers.</span>
            </li>
            <li className="flex items-start gap-2">
              <HealthcareIcon name="check" className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
              <span>Zero unverified cure guarantees; strictly individualized holistic management.</span>
            </li>
          </ul>
        </div>
      </section>

      {/* 3 & 4: WHO MAY BENEFIT & SYMPTOMS */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="p-8 rounded-3xl bg-white border border-slate-200/80 shadow-sm space-y-4">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#1B4332]">
            <HealthcareIcon name="users" className="w-4 h-4 text-[#2D6A4F]" />
            <span>Candidate Profile</span>
          </div>
          <h2 className="text-xl font-bold text-[#0F172A]">Who May Benefit From This Care</h2>
          <div className="space-y-2.5 pt-2">
            {data.targetAudience.map((item, idx) => (
              <div key={idx} className="flex items-start gap-3 p-3 rounded-xl bg-slate-50 border border-slate-100 text-xs text-slate-800">
                <HealthcareIcon name="check-circle" className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span className="leading-relaxed">{item}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="p-8 rounded-3xl bg-white border border-slate-200/80 shadow-sm space-y-4">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-amber-800">
            <HealthcareIcon name="alert-triangle" className="w-4 h-4 text-amber-600" />
            <span>Clinical Indicators</span>
          </div>
          <h2 className="text-xl font-bold text-[#0F172A]">Symptoms & Manifestations Addressed</h2>
          <div className="space-y-2.5 pt-2">
            {data.symptoms.map((symptom, idx) => (
              <div key={idx} className="flex items-start gap-3 p-3 rounded-xl bg-amber-50/60 border border-amber-100 text-xs text-slate-800">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0" />
                <span className="leading-relaxed">{symptom}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 5. CLINICAL APPROACH */}
      <section className="p-8 sm:p-10 rounded-3xl bg-white border border-slate-200/80 shadow-sm space-y-6">
        <div className="max-w-2xl">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
            <HealthcareIcon name="activity" className="w-4 h-4 text-[#2D6A4F]" />
            <span>Methodology</span>
          </div>
          <h2 className="text-2xl font-bold text-[#0F172A] mt-1">Our Integrated Clinical Approach</h2>
          <p className="text-xs sm:text-sm text-slate-600 mt-2">
            Every patient trajectory is structured through rigorous diagnostic staging and individualized therapeutic modulation.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {data.clinicalApproach.map((step, idx) => (
            <div key={idx} className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2 flex flex-col justify-between">
              <div>
                <span className="w-7 h-7 rounded-lg bg-[#2D6A4F] text-white font-bold text-xs flex items-center justify-center mb-3">
                  {idx + 1}
                </span>
                <h3 className="text-sm font-bold text-slate-900">{step.title}</h3>
                <p className="text-xs text-slate-600 mt-2 leading-relaxed">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 6 & 7: UNANI FRAMEWORK & BIOMEDICAL CORROBORATION */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="p-8 rounded-3xl bg-[#FAF9F5] border border-[#E6E2D3] shadow-sm space-y-5">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#1B4332]">
            <HealthcareIcon name="book" className="w-4 h-4 text-[#2D6A4F]" />
            <span>Classical Canon</span>
          </div>
          <h2 className="text-xl font-bold text-[#0F172A]">Unani Pathophysiological Framework</h2>
          
          <div className="space-y-3 text-xs">
            <div className="p-3.5 rounded-xl bg-white border border-[#DDD6C1]">
              <span className="font-bold text-slate-900 block mb-1">Mizaj Assessment:</span>
              <p className="text-slate-700 leading-relaxed">{data.unaniFramework.mizajImpact}</p>
            </div>
            <div className="p-3.5 rounded-xl bg-white border border-[#DDD6C1]">
              <span className="font-bold text-slate-900 block mb-1">Organ Axis Involved:</span>
              <p className="text-slate-700 leading-relaxed">{data.unaniFramework.organAxis}</p>
            </div>
            <div className="p-3.5 rounded-xl bg-white border border-[#DDD6C1]">
              <span className="font-bold text-slate-900 block mb-1">Humoral Pathology (Su-e-Mizaj):</span>
              <p className="text-slate-700 leading-relaxed">{data.unaniFramework.humoralPathology}</p>
            </div>
            <div className="p-3.5 rounded-xl bg-white border border-[#DDD6C1]">
              <span className="font-bold text-slate-900 block mb-1">Essential Regimen Factors (Asbab-e-Sitta):</span>
              <ul className="list-disc list-inside space-y-1 text-slate-700 mt-1">
                {data.unaniFramework.asbabConsiderations.map((asbab, idx) => (
                  <li key={idx}>{asbab}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="p-8 rounded-3xl bg-white border border-slate-200/80 shadow-sm space-y-5">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
            <HealthcareIcon name="flask" className="w-4 h-4 text-[#2D6A4F]" />
            <span>Modern Science</span>
          </div>
          <h2 className="text-xl font-bold text-[#0F172A]">Contemporary Biomedical Corroboration</h2>

          <div className="space-y-3 text-xs">
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="font-bold text-slate-900 block mb-1">Corroborating Biomarkers:</span>
              <div className="flex flex-wrap gap-1.5 mt-2">
                {data.biomedicalCorroboration.biomarkers.map((bm, idx) => (
                  <span key={idx} className="px-2.5 py-1 rounded-md bg-white border border-slate-200 text-slate-800 font-mono text-[11px]">
                    {bm}
                  </span>
                ))}
              </div>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="font-bold text-slate-900 block mb-1">Longitudinal Surveillance:</span>
              <p className="text-slate-700 leading-relaxed">{data.biomedicalCorroboration.monitoring}</p>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="font-bold text-slate-900 block mb-1">Integrative Pharmacological Safety:</span>
              <p className="text-slate-700 leading-relaxed">{data.biomedicalCorroboration.integrativeSafety}</p>
            </div>
          </div>
        </div>
      </section>

      {/* 8. WHAT CONSULTATION INCLUDES */}
      <section className="p-8 sm:p-10 rounded-3xl bg-gradient-to-br from-[#FAFAF7] to-[#EEF2E6] border border-[#D5DEC4] space-y-6">
        <div className="max-w-2xl">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#1B4332]">
            <HealthcareIcon name="clipboard" className="w-4 h-4 text-[#2D6A4F]" />
            <span>Care Delivery</span>
          </div>
          <h2 className="text-2xl font-bold text-[#0F172A] mt-1">What Your Clinical Encounter Includes</h2>
          <p className="text-xs sm:text-sm text-slate-600 mt-2">
            ZAYVORA consultations are thorough, unhurried, and documented under 21 CFR Part 11 electronic records standards.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.consultationIncludes.map((item, idx) => (
            <div key={idx} className="p-4 rounded-2xl bg-white border border-slate-200/80 shadow-xs flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0 mt-0.5">
                <HealthcareIcon name="check" className="w-3.5 h-3.5" />
              </div>
              <span className="text-xs text-slate-800 font-medium leading-relaxed">{item}</span>
            </div>
          ))}
        </div>
      </section>

      {/* 9. RED-FLAG SAFETY & CONTRAINDICATIONS */}
      <section className="p-6 sm:p-8 rounded-3xl bg-rose-50/70 border border-rose-200/80 space-y-4">
        <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-rose-800">
          <HealthcareIcon name="alert-triangle" className="w-4 h-4 text-rose-600" />
          <span>Clinical Safety Protocol</span>
        </div>
        <h2 className="text-xl font-bold text-rose-950">Emergency Exclusion Criteria & Red-Flag Warnings</h2>
        <p className="text-xs sm:text-sm text-rose-900 leading-relaxed">
          {data.redFlagSafety.advisory}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          <div className="p-4 rounded-2xl bg-white/90 border border-rose-200 text-xs space-y-2">
            <span className="font-bold text-rose-900 block">Immediate Emergency Red Flags (Seek Emergency Hospital Care):</span>
            <ul className="list-disc list-inside space-y-1 text-rose-800">
              {data.redFlagSafety.emergencySymptoms.map((sym, idx) => (
                <li key={idx}>{sym}</li>
              ))}
            </ul>
          </div>
          <div className="p-4 rounded-2xl bg-white/90 border border-rose-200 text-xs space-y-2">
            <span className="font-bold text-rose-900 block">Relative Exclusion for Outpatient Unani Care:</span>
            <ul className="list-disc list-inside space-y-1 text-rose-800">
              {data.redFlagSafety.exclusionCriteria.map((crit, idx) => (
                <li key={idx}>{crit}</li>
              ))}
            </ul>
          </div>
        </div>

        <div className="p-3 rounded-xl bg-rose-100/70 border border-rose-300 text-rose-950 text-xs font-semibold flex items-center justify-between gap-4">
          <span>In case of severe acute chest pain, sudden paralysis, or severe respiratory distress:</span>
          <span className="px-3 py-1 rounded bg-rose-600 text-white font-bold shrink-0">Dial 112 Immediately</span>
        </div>
      </section>

      {/* 10. CLINICAL TEAM */}
      <section className="p-8 rounded-3xl bg-white border border-slate-200/80 shadow-sm space-y-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
            <HealthcareIcon name="academic" className="w-4 h-4 text-[#2D6A4F]" />
            <span>Practicing Faculty</span>
          </div>
          <h2 className="text-2xl font-bold text-[#0F172A] mt-1">Led by Registered Clinicians</h2>
          <p className="text-xs sm:text-sm text-slate-600 mt-2">
            All ZAYVORA attending physicians hold verified qualifications recognized under the National Commission for Indian System of Medicine (NCISM) Act 2020.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {data.clinicianTeam.map((doc, idx) => (
            <div key={idx} className="p-5 rounded-2xl bg-slate-50 border border-slate-200 flex items-start gap-4">
              <div className="w-12 h-12 rounded-xl bg-[#2D6A4F] text-white flex items-center justify-center font-bold text-base shrink-0">
                {doc.name.split(" ").map(w => w[0]).filter(Boolean).slice(0, 2).join("")}
              </div>
              <div className="space-y-1 text-xs">
                <h3 className="text-sm font-bold text-slate-900">{doc.name}</h3>
                <p className="text-slate-600 font-medium">{doc.role}</p>
                <div className="pt-1 flex flex-wrap gap-2 text-[11px] text-slate-500">
                  <span className="px-2 py-0.5 rounded bg-white border border-slate-200 font-mono">
                    {doc.regNumber}
                  </span>
                  <span className="px-2 py-0.5 rounded bg-white border border-slate-200">
                    {doc.qualification}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 11. STRUCTURED FAQS */}
      <section className="p-8 rounded-3xl bg-white border border-slate-200/80 shadow-sm space-y-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#1B4332]">
            <HealthcareIcon name="message" className="w-4 h-4 text-[#2D6A4F]" />
            <span>Informed Consent</span>
          </div>
          <h2 className="text-2xl font-bold text-[#0F172A] mt-1">Frequently Asked Questions</h2>
        </div>

        <div className="space-y-3">
          {data.faqs.map((faq, idx) => {
            const isOpen = openFaq === idx;
            return (
              <div key={idx} className="border border-slate-200 rounded-2xl overflow-hidden transition">
                <button
                  onClick={() => setOpenFaq(isOpen ? null : idx)}
                  className="w-full text-left px-5 py-4 bg-slate-50 hover:bg-slate-100/80 flex items-center justify-between gap-4 text-xs sm:text-sm font-bold text-slate-900"
                >
                  <span>{faq.question}</span>
                  <HealthcareIcon
                    name={isOpen ? "chevron-down" : "chevron-right"}
                    className="w-4 h-4 text-slate-500 shrink-0 transition-transform"
                  />
                </button>
                {isOpen && (
                  <div className="px-5 py-4 bg-white text-xs sm:text-sm text-slate-700 leading-relaxed border-t border-slate-200">
                    {faq.answer}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* 12. EVIDENCE & LITERATURE REFERENCES */}
      <section className="p-8 rounded-3xl bg-[#FAF9F5] border border-[#E6E2D3] shadow-sm space-y-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
            <HealthcareIcon name="library" className="w-4 h-4 text-[#2D6A4F]" />
            <span>Scholarly Provenance</span>
          </div>
          <h2 className="text-xl font-bold text-[#0F172A] mt-1">Classical Canon & Indexed Research References</h2>
        </div>

        <div className="space-y-2.5">
          {data.references.map((ref, idx) => (
            <div key={idx} className="p-3.5 rounded-xl bg-white border border-[#DDD6C1] text-xs flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <span className={`inline-block px-2 py-0.5 rounded text-[10px] font-bold uppercase mr-2 ${
                  ref.type === "classical" ? "bg-amber-100 text-amber-800" : "bg-teal-100 text-teal-800"
                }`}>
                  {ref.type}
                </span>
                <span className="font-semibold text-slate-900">{ref.title}</span>
                <span className="text-slate-500 text-[11px] block sm:inline sm:ml-2">({ref.source}{ref.year ? `, ${ref.year}` : ""})</span>
              </div>
              {ref.doiOrUrl && (
                <span className="text-emerald-700 font-mono text-[10px] shrink-0">{ref.doiOrUrl}</span>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* 13. EDITORIAL GOVERNANCE BLOCK */}
      <section className="p-6 rounded-2xl bg-slate-100 border border-slate-200 text-xs text-slate-600 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-slate-800 font-semibold">
            <HealthcareIcon name="shield" className="w-4 h-4 text-emerald-700" />
            <span>Clinical Editorial Governance</span>
            <span className="px-2 py-0.2 rounded bg-emerald-100 text-emerald-800 font-mono text-[10px]">v{data.governance.version}</span>
          </div>
          <p className="text-[11px] text-slate-500">
            Author: {data.governance.author} ({data.governance.authorRole}) • Senior Reviewer: {data.governance.reviewer} (NCISM Reg: {data.governance.reviewerRegNumber})
          </p>
        </div>
        <div className="text-[11px] text-slate-500 md:text-right shrink-0">
          <div>Last Clinical Audit: <strong className="text-slate-700">{data.governance.lastReviewed}</strong></div>
          <div>Next Mandatory Audit: <strong className="text-slate-700">{data.governance.nextAuditDue}</strong></div>
        </div>
      </section>
    </div>
  );
}
