"use client";

import React from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { HEALTH_PROGRAMS } from "@/lib/cms/programsData";

export default function ProgramDetailPage() {
  const searchParams = useSearchParams();
  const programId = searchParams.get("id") || "metabolic-care";

  const program = HEALTH_PROGRAMS.find(p => p.id === programId) || HEALTH_PROGRAMS[0];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-12 space-y-12 text-[#CBD5E1]">
      
      {/* Breadcrumbs */}
      <div className="flex items-center gap-2 text-xs text-[#64748B]">
        <Link href="/website" className="hover:text-white">Home</Link>
        <span>/</span>
        <Link href="/website/programs" className="hover:text-white">Health Programs</Link>
        <span>/</span>
        <span className="text-white font-medium">{program.title}</span>
      </div>

      {/* Program Hero */}
      <div className="rounded-3xl bg-gradient-to-br from-[#0F172A] to-[#1E293B] border border-[#334155] p-8 sm:p-10 space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <span className="px-3 py-1 rounded-full bg-[#0D9488]/20 border border-[#0D9488]/40 text-[#2DD4BF] text-xs font-mono font-bold">
            {program.duration} Program
          </span>
          <span className="text-xs text-[#94A3B8] font-semibold">{program.category}</span>
        </div>

        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">{program.title}</h1>
        <p className="text-base text-[#94A3B8] leading-relaxed">{program.overview}</p>

        <div className="flex flex-wrap items-center gap-4 pt-4 border-t border-[#334155]">
          <Link
            href="/website/book"
            className="px-6 py-3 rounded-2xl bg-[#0D9488] text-white font-bold text-xs hover:bg-[#0F766E] shadow-md transition"
          >
            Book Assessment Consultation
          </Link>
          <Link
            href="/website/contact"
            className="px-6 py-3 rounded-2xl bg-[#1E293B] border border-[#334155] text-white font-semibold text-xs hover:bg-[#334155] transition"
          >
            Inquire with Patient Care Team
          </Link>
        </div>
      </div>

      {/* Who May Benefit & Key Benefits */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <span>👥</span> Who May Benefit
          </h3>
          <ul className="space-y-2 text-xs text-[#94A3B8]">
            {program.suitableAudience.map((item, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-[#0D9488] font-bold">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <span>✨</span> Program Key Goals
          </h3>
          <ul className="space-y-2 text-xs text-[#94A3B8]">
            {program.keyBenefits.map((item, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-emerald-400 font-bold">✓</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Sequential Program Phases (Afaal Protocol) */}
      <div className="space-y-6">
        <div>
          <span className="text-[11px] font-bold text-[#0D9488] uppercase tracking-wider block">Care Pathway</span>
          <h2 className="text-2xl font-bold text-white">Sequential Program Phases</h2>
          <p className="text-xs text-[#94A3B8]">Grounded in the classical Unani 4-stage therapeutic cascade.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {program.phases.map((phase) => (
            <div key={phase.stageNumber} className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-[#1E293B] text-[#2DD4BF]">
                  Phase {phase.stageNumber}: {phase.unaniName}
                </span>
                <span className="text-[10px] text-[#64748B] font-mono">{phase.durationDays} Days</span>
              </div>
              <h4 className="font-bold text-white text-base">{phase.title}</h4>
              <p className="text-xs text-[#94A3B8] leading-relaxed">{phase.focus}</p>
              <div className="pt-2 border-t border-[#1E293B] space-y-1">
                <span className="text-[10px] font-bold text-white uppercase block">Key Modalities:</span>
                <ul className="text-[11px] text-[#64748B] space-y-0.5">
                  {phase.modalities.map((m, idx) => (
                    <li key={idx}>• {m}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Lifestyle Guidance (Asbab-e-Sittah) */}
      <div className="p-8 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-6">
        <div>
          <span className="text-[11px] font-bold text-[#0D9488] uppercase tracking-wider block">Daily Self-Care</span>
          <h2 className="text-xl font-bold text-white">Lifestyle Guidance (Asbab-e-Sittah)</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-[#94A3B8]">
          <div className="space-y-2">
            <h5 className="font-bold text-white flex items-center gap-1.5">
              <span>🍲</span> Dietary Directives
            </h5>
            <ul className="space-y-1.5 text-[11px]">
              {program.lifestyleGuidance.dietary.map((d, idx) => (
                <li key={idx}>• {d}</li>
              ))}
            </ul>
          </div>
          <div className="space-y-2">
            <h5 className="font-bold text-white flex items-center gap-1.5">
              <span>🚶</span> Movement & Physical Activity
            </h5>
            <ul className="space-y-1.5 text-[11px]">
              {program.lifestyleGuidance.activity.map((a, idx) => (
                <li key={idx}>• {a}</li>
              ))}
            </ul>
          </div>
          <div className="space-y-2">
            <h5 className="font-bold text-white flex items-center gap-1.5">
              <span>🌙</span> Restorative Sleep Architecture
            </h5>
            <ul className="space-y-1.5 text-[11px]">
              {program.lifestyleGuidance.sleep.map((s, idx) => (
                <li key={idx}>• {s}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Safety & Follow-up Notice */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-2 text-xs">
          <h4 className="font-bold text-white flex items-center gap-1.5">
            <span>🛡️</span> Safety & Medical Supervision
          </h4>
          <p className="text-[#94A3B8] leading-relaxed">{program.safetyInformation}</p>
        </div>
        <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-2 text-xs">
          <h4 className="font-bold text-white flex items-center gap-1.5">
            <span>📅</span> Follow-up & Monitoring Cadence
          </h4>
          <p className="text-[#94A3B8] leading-relaxed">{program.followUpProcess}</p>
        </div>
      </div>

      {/* Program FAQs */}
      {program.faqs && program.faqs.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-bold text-white">Program Questions</h3>
          <div className="space-y-3">
            {program.faqs.map((faq, idx) => (
              <div key={idx} className="p-5 rounded-2xl bg-[#0F172A] border border-[#334155] space-y-1.5 text-xs">
                <h5 className="font-bold text-white">{faq.question}</h5>
                <p className="text-[#94A3B8] leading-relaxed">{faq.answer}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Final Medical Disclaimer Box */}
      <div className="p-4 rounded-2xl bg-[#0A0F1D] border border-[#1E293B] text-[11px] text-[#64748B] leading-relaxed">
        <strong>Statutory Notice:</strong> This health program is designed for supportive chronic wellness management. It does not replace emergency medical treatment. Individual outcomes vary based on adherence, baseline constitution, and medical history.
      </div>

      {/* Bottom Action Bar */}
      <div className="pt-4 flex items-center justify-between">
        <Link href="/website/programs" className="text-xs font-semibold text-[#94A3B8] hover:text-white">
          ← Back to All Health Programs
        </Link>
        <Link
          href="/website/book"
          className="px-6 py-3 rounded-2xl bg-[#0D9488] text-white font-bold text-xs hover:bg-[#0F766E] shadow-md transition"
        >
          Book Consultation for This Program
        </Link>
      </div>

    </div>
  );
}
