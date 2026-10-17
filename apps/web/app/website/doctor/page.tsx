"use client";

import React from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { CLINICAL_TEAM } from "@/lib/cms/doctorsData";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export default function DoctorProfilePage() {
  const searchParams = useSearchParams();
  const docId = searchParams.get("id") || "dr-irfan-ashraf";

  const doctor = CLINICAL_TEAM.find((d) => d.id === docId) || CLINICAL_TEAM[0];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-12 space-y-10">
      
      {/* Breadcrumbs */}
      <div className="flex items-center gap-2 text-xs text-slate-500">
        <Link href="/" className="hover:text-slate-900">Home</Link>
        <span>/</span>
        <Link href="/doctors" className="hover:text-slate-900">Clinical Team</Link>
        <span>/</span>
        <span className="text-slate-900 font-semibold">{doctor.name}</span>
      </div>

      {/* Main Profile Presentation Header */}
      <div className="rounded-3xl bg-white border border-slate-200/90 shadow-sm p-8 sm:p-10 space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 border-b border-slate-100 pb-6">
          <div className="flex items-center gap-5">
            <div className="w-20 h-20 rounded-2xl bg-[#1B4332] text-white font-extrabold flex items-center justify-center text-2xl shadow-md">
              {doctor.avatarInitials}
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2 flex-wrap">
                <h1 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A]">{doctor.name}</h1>
                <span className="inline-flex items-center gap-1 text-xs px-2.5 py-0.5 rounded-full bg-emerald-50 text-[#1B4332] border border-emerald-200 font-semibold">
                  <HealthcareIcon name="shield-check" className="w-3.5 h-3.5 text-emerald-700" />
                  <span>NCISM Act 2020 Registered</span>
                </span>
              </div>
              <p className="text-xs text-emerald-700 font-semibold">{doctor.designation}</p>
              <p className="text-xs text-slate-500 font-mono">{doctor.degrees} • {doctor.regNumber}</p>
            </div>
          </div>

          <div className="text-left sm:text-right space-y-1">
            <span className="text-2xl font-bold text-[#0F172A] font-mono">₹{doctor.consultationFee}</span>
            <span className="text-[11px] text-slate-500 block">Initial Comprehensive Clinical Evaluation</span>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/70">
            <span className="text-[10px] text-slate-400 block font-medium">Experience</span>
            <span className="font-bold text-slate-800 text-sm">{doctor.experienceYears} Years Clinical</span>
          </div>
          <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/70">
            <span className="text-[10px] text-slate-400 block font-medium">Rating</span>
            <span className="font-bold text-amber-800 text-sm">★ {doctor.rating} ({doctor.reviewCount} reviews)</span>
          </div>
          <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/70">
            <span className="text-[10px] text-slate-400 block font-medium">Available Days</span>
            <span className="font-bold text-slate-800 text-sm">{doctor.availableDays}</span>
          </div>
          <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/70">
            <span className="text-[10px] text-slate-400 block font-medium">Languages</span>
            <span className="font-bold text-slate-800 text-sm">{doctor.languages.join(", ")}</span>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-4 pt-2">
          <Link
            href={`/contact?doctor=${doctor.id}`}
            className="px-6 py-3 rounded-2xl bg-[#1B4332] text-white font-bold text-xs hover:bg-[#2D6A4F] shadow-sm transition"
          >
            Schedule Consultation with {doctor.name}
          </Link>
          <Link
            href="/contact"
            className="px-6 py-3 rounded-2xl bg-slate-100 border border-slate-200 text-slate-700 font-semibold text-xs hover:bg-slate-200 transition"
          >
            Inquire Facility Timings
          </Link>
        </div>
      </div>

      {/* Clinical Philosophy & Bio */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
        <div className="md:col-span-7 space-y-6">
          <div className="p-6 rounded-3xl bg-white border border-slate-200/90 shadow-sm space-y-3">
            <h3 className="text-base font-bold text-[#0F172A]">Physician Bio & Background</h3>
            <p className="text-xs text-slate-600 leading-relaxed">{doctor.bio}</p>
          </div>

          <div className="p-6 rounded-3xl bg-white border border-slate-200/90 shadow-sm space-y-3">
            <h3 className="text-base font-bold text-[#0F172A]">Clinical Approach</h3>
            <p className="text-xs text-slate-600 leading-relaxed italic bg-slate-50 p-4 rounded-2xl border border-slate-200/70">
              "{doctor.clinicalApproach}"
            </p>
          </div>
        </div>

        <div className="md:col-span-5 space-y-6">
          {/* Areas of Focus */}
          <div className="p-6 rounded-3xl bg-white border border-slate-200/90 shadow-sm space-y-3">
            <h3 className="text-base font-bold text-[#0F172A]">Specialized Areas of Focus</h3>
            <ul className="space-y-2 text-xs text-slate-700">
              {doctor.areasOfFocus.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <HealthcareIcon name="check" className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Academic Credentials */}
          <div className="p-6 rounded-3xl bg-white border border-slate-200/90 shadow-sm space-y-3">
            <h3 className="text-base font-bold text-[#0F172A]">Education & Credentials</h3>
            <ul className="space-y-2 text-xs text-slate-600">
              {doctor.educationAndCredentials.map((edu, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <HealthcareIcon name="shield-check" className="w-3.5 h-3.5 text-slate-400 shrink-0 mt-0.5" />
                  <span>{edu}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Published Research */}
      {doctor.publishedWorks && doctor.publishedWorks.length > 0 && (
        <div className="p-6 rounded-3xl bg-white border border-slate-200/90 shadow-sm space-y-3 text-xs">
          <h3 className="text-base font-bold text-[#0F172A]">Peer-Reviewed Publications & Clinical Studies</h3>
          <ul className="space-y-2 text-slate-700">
            {doctor.publishedWorks.map((pub, idx) => (
              <li key={idx} className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/70 flex items-start gap-2.5">
                <HealthcareIcon name="file-text" className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
                <span>{pub}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Bottom Nav */}
      <div className="pt-4 flex items-center justify-between">
        <Link href="/doctors" className="text-xs font-semibold text-slate-500 hover:text-slate-900 transition">
          ← Back to All Practitioners
        </Link>
        <Link
          href={`/contact?doctor=${doctor.id}`}
          className="px-6 py-3 rounded-2xl bg-[#1B4332] text-white font-bold text-xs hover:bg-[#2D6A4F] shadow-sm transition"
        >
          Book Consultation
        </Link>
      </div>

    </div>
  );
}
