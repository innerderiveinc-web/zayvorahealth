"use client";

import React, { useState } from "react";
import Link from "next/link";
import { CLINICAL_TEAM } from "@/lib/cms/doctorsData";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export default function DoctorsPage() {
  const [selectedFocus, setSelectedFocus] = useState<string>("All");

  const focusAreas = [
    "All",
    "Musculoskeletal",
    "Metabolic & Liver",
    "Women's Health",
    "Pharmacology & Gut"
  ];

  const filteredDoctors = CLINICAL_TEAM.filter((doc) => {
    if (selectedFocus === "All") return true;
    if (selectedFocus === "Musculoskeletal") return doc.areasOfFocus.some(f => f.includes("Musculoskeletal"));
    if (selectedFocus === "Metabolic & Liver") return doc.areasOfFocus.some(f => f.includes("Metabolic") || f.includes("Hepatic"));
    if (selectedFocus === "Women's Health") return doc.areasOfFocus.some(f => f.includes("Women") || f.includes("PCOS"));
    if (selectedFocus === "Pharmacology & Gut") return doc.areasOfFocus.some(f => f.includes("Gut") || f.includes("Pharmacology"));
    return true;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12 space-y-10">
      
      {/* Header */}
      <div className="border-b border-slate-200 pb-8 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-[#1B4332] text-xs font-bold">
          <HealthcareIcon name="stethoscope" className="w-4 h-4 text-emerald-700" />
          <span>Central Clinical Faculty & Registered Practitioners</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-[#0F172A] tracking-tight">
          Licensed Practitioners & Tabeebs
        </h1>
        <p className="text-sm text-slate-600 max-w-3xl leading-relaxed">
          Our senior clinical faculty hold statutory NCISM Act 2020 registration with decades of combined clinical leadership at premier academic hospitals, blending classical pulse diagnostics with modern laboratory medicine.
        </p>
      </div>

      {/* Focus Area Filter */}
      <div className="flex flex-wrap gap-2 p-4 rounded-2xl bg-white border border-slate-200 shadow-sm">
        <span className="text-xs font-bold text-slate-500 flex items-center pr-2">Filter Specialization:</span>
        {focusAreas.map((focus) => (
          <button
            key={focus}
            onClick={() => setSelectedFocus(focus)}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition ${
              selectedFocus === focus
                ? "bg-[#1B4332] text-white shadow-sm"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900"
            }`}
          >
            {focus}
          </button>
        ))}
      </div>

      {/* Doctors Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {filteredDoctors.map((doc) => (
          <div
            key={doc.id}
            className="rounded-3xl bg-white border border-slate-200/90 p-7 space-y-5 shadow-sm hover:shadow-md hover:border-emerald-600/40 transition flex flex-col justify-between"
          >
            <div className="space-y-4">
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-center gap-3.5">
                  <div className="w-14 h-14 rounded-2xl bg-[#1B4332] text-white font-extrabold flex items-center justify-center text-xl shadow-md">
                    {doc.avatarInitials}
                  </div>
                  <div>
                    <h3 className="font-extrabold text-[#0F172A] text-lg">{doc.name}</h3>
                    <span className="text-xs text-emerald-700 font-mono font-medium block">{doc.regNumber}</span>
                    <span className="text-[11px] text-slate-500 block">{doc.degrees}</span>
                  </div>
                </div>
                <span className="text-xs font-bold text-amber-800 bg-amber-50 px-2.5 py-1 rounded-lg border border-amber-200">
                  ★ {doc.rating}
                </span>
              </div>

              <p className="text-xs text-slate-600 leading-relaxed">{doc.bio}</p>

              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2 text-xs">
                <div>
                  <span className="text-[10px] font-bold text-slate-500 uppercase block tracking-wider">Hospital Affiliation:</span>
                  <span className="text-slate-700 text-[11px]">{doc.hospitalAffiliation}</span>
                </div>
                <div className="grid grid-cols-2 gap-2 pt-1 border-t border-slate-200/60">
                  <div>
                    <span className="text-[10px] font-bold text-slate-400 block">OPD Hours:</span>
                    <span className="text-slate-800 text-[11px]">{doc.clinicTimings}</span>
                  </div>
                  <div>
                    <span className="text-[10px] font-bold text-slate-400 block">Languages:</span>
                    <span className="text-slate-800 text-[11px]">{doc.languages.join(", ")}</span>
                  </div>
                </div>
              </div>

              <div className="space-y-1">
                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Areas of Focus:</span>
                <div className="flex flex-wrap gap-1.5">
                  {doc.areasOfFocus.map((f, idx) => (
                    <span key={idx} className="text-[10px] px-2.5 py-0.5 rounded-lg bg-emerald-50 text-[#1B4332] border border-emerald-200 font-medium">
                      {f}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Card Footer Actions */}
            <div className="pt-4 border-t border-slate-100 flex items-center justify-between gap-3">
              <Link
                href={`/website/doctor?id=${doc.id}`}
                className="w-1/2 text-center py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-xs font-semibold text-slate-800 transition"
              >
                View Profile & Credentials
              </Link>
              <Link
                href={`/website/book?doctor=${doc.id}`}
                className="w-1/2 text-center py-2.5 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-xs font-bold text-white shadow-sm transition"
              >
                Book Consultation
              </Link>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
