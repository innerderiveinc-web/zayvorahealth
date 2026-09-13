"use client";

import React from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { CLINICAL_TEAM } from "@/lib/cms/doctorsData";

export default function DoctorProfilePage() {
  const searchParams = useSearchParams();
  const docId = searchParams.get("id") || "dr-tariq-mansoor";

  const doctor = CLINICAL_TEAM.find(d => d.id === docId) || CLINICAL_TEAM[0];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-12 space-y-10 text-[#CBD5E1]">
      
      {/* Breadcrumbs */}
      <div className="flex items-center gap-2 text-xs text-[#64748B]">
        <Link href="/website" className="hover:text-white">Home</Link>
        <span>/</span>
        <Link href="/website/doctors" className="hover:text-white">Clinical Team</Link>
        <span>/</span>
        <span className="text-white font-medium">{doctor.name}</span>
      </div>

      {/* Main Profile Presentation Header */}
      <div className="rounded-3xl bg-gradient-to-br from-[#0F172A] to-[#1E293B] border border-[#334155] p-8 sm:p-10 space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 border-b border-[#334155] pb-6">
          <div className="flex items-center gap-5">
            <div className="w-20 h-20 rounded-3xl bg-[#0D9488] text-white font-extrabold flex items-center justify-center text-3xl shadow-xl">
              {doctor.avatarInitials}
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <h1 className="text-2xl sm:text-3xl font-extrabold text-white">{doctor.name}</h1>
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-semibold">
                  Verified CCIM
                </span>
              </div>
              <p className="text-xs text-[#2DD4BF] font-mono">{doctor.designation}</p>
              <p className="text-xs text-[#94A3B8]">{doctor.degrees} • {doctor.regNumber}</p>
            </div>
          </div>

          <div className="text-right sm:text-right space-y-1">
            <span className="text-xl font-bold text-white font-mono">₹{doctor.consultationFee}</span>
            <span className="text-[11px] text-[#64748B] block">Initial Comprehensive Evaluation</span>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div className="p-3.5 rounded-2xl bg-[#0A0F1D] border border-[#1E293B]">
            <span className="text-[10px] text-[#64748B] block">Experience</span>
            <span className="font-bold text-white text-sm">{doctor.experienceYears} Years Clinical</span>
          </div>
          <div className="p-3.5 rounded-2xl bg-[#0A0F1D] border border-[#1E293B]">
            <span className="text-[10px] text-[#64748B] block">Rating</span>
            <span className="font-bold text-amber-400 text-sm">★ {doctor.rating} ({doctor.reviewCount})</span>
          </div>
          <div className="p-3.5 rounded-2xl bg-[#0A0F1D] border border-[#1E293B]">
            <span className="text-[10px] text-[#64748B] block">Available Days</span>
            <span className="font-bold text-white text-sm">{doctor.availableDays}</span>
          </div>
          <div className="p-3.5 rounded-2xl bg-[#0A0F1D] border border-[#1E293B]">
            <span className="text-[10px] text-[#64748B] block">Languages</span>
            <span className="font-bold text-white text-sm">{doctor.languages.join(", ")}</span>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-4 pt-2">
          <Link
            href={`/website/book?doctor=${doctor.id}`}
            className="px-6 py-3 rounded-2xl bg-[#0D9488] text-white font-bold text-xs hover:bg-[#0F766E] shadow-md transition"
          >
            Book Consultation with {doctor.name}
          </Link>
          <Link
            href="/website/contact"
            className="px-6 py-3 rounded-2xl bg-[#1E293B] border border-[#334155] text-white font-semibold text-xs hover:bg-[#334155] transition"
          >
            Inquire Facility Timings
          </Link>
        </div>
      </div>

      {/* Clinical Philosophy & Bio */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
        <div className="md:col-span-7 space-y-6">
          <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-3">
            <h3 className="text-base font-bold text-white">Physician Bio & Background</h3>
            <p className="text-xs text-[#94A3B8] leading-relaxed">{doctor.bio}</p>
          </div>

          <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-3">
            <h3 className="text-base font-bold text-white">Clinical Approach</h3>
            <p className="text-xs text-[#94A3B8] leading-relaxed italic">"{doctor.clinicalApproach}"</p>
          </div>
        </div>

        <div className="md:col-span-5 space-y-6">
          {/* Areas of Focus */}
          <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-3">
            <h3 className="text-base font-bold text-white">Specialized Areas of Focus</h3>
            <ul className="space-y-1.5 text-xs text-[#94A3B8]">
              {doctor.areasOfFocus.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-[#0D9488] font-bold">✓</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Academic Credentials */}
          <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-3">
            <h3 className="text-base font-bold text-white">Education & Credentials</h3>
            <ul className="space-y-1.5 text-xs text-[#64748B]">
              {doctor.educationAndCredentials.map((edu, idx) => (
                <li key={idx} className="flex items-start gap-1.5">
                  <span className="text-white">•</span>
                  <span>{edu}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Published Research */}
      {doctor.publishedWorks && doctor.publishedWorks.length > 0 && (
        <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-3 text-xs">
          <h3 className="text-base font-bold text-white">Peer-Reviewed Publications & Clinical Studies</h3>
          <ul className="space-y-2 text-[#94A3B8]">
            {doctor.publishedWorks.map((pub, idx) => (
              <li key={idx} className="p-3 rounded-2xl bg-[#0A0F1D] border border-[#1E293B]">
                📄 {pub}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Bottom Nav */}
      <div className="pt-4 flex items-center justify-between">
        <Link href="/website/doctors" className="text-xs font-semibold text-[#94A3B8] hover:text-white">
          ← Back to All Practitioners
        </Link>
        <Link
          href={`/website/book?doctor=${doctor.id}`}
          className="px-6 py-3 rounded-2xl bg-[#0D9488] text-white font-bold text-xs hover:bg-[#0F766E] shadow-md transition"
        >
          Book Consultation
        </Link>
      </div>

    </div>
  );
}
