"use client";

import React, { useState } from "react";
import Link from "next/link";
import { CLINICAL_TEAM, DoctorProfile } from "@/lib/cms/doctorsData";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export default function DoctorsPage() {
  const [selectedFocus, setSelectedFocus] = useState<string>("All");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedDoctor, setSelectedDoctor] = useState<DoctorProfile | null>(null);

  const focusAreas = [
    { id: "All", label: "All Specializations" },
    { id: "Musculoskeletal", label: "Musculoskeletal & Joints (Waja-ul-Mafasil)" },
    { id: "Metabolic & Liver", label: "Metabolic & Hepatic Axis" },
    { id: "Women's Health", label: "Women's Health (Niswan)" },
    { id: "Pharmacology & Gut", label: "Pharmacology & Gastrointestinal" }
  ];

  const filteredDoctors = CLINICAL_TEAM.filter((doc) => {
    // Focus filter
    let matchesFocus = true;
    if (selectedFocus === "Musculoskeletal") {
      matchesFocus = doc.areasOfFocus.some((f) => f.includes("Musculoskeletal"));
    } else if (selectedFocus === "Metabolic & Liver") {
      matchesFocus = doc.areasOfFocus.some((f) => f.includes("Metabolic") || f.includes("Hepatic"));
    } else if (selectedFocus === "Women's Health") {
      matchesFocus = doc.areasOfFocus.some((f) => f.includes("Women") || f.includes("PCOS"));
    } else if (selectedFocus === "Pharmacology & Gut") {
      matchesFocus = doc.areasOfFocus.some((f) => f.includes("Gut") || f.includes("Pharmacology"));
    }

    // Search query
    const query = searchQuery.toLowerCase().trim();
    let matchesSearch = true;
    if (query) {
      matchesSearch =
        doc.name.toLowerCase().includes(query) ||
        doc.designation.toLowerCase().includes(query) ||
        doc.degrees.toLowerCase().includes(query) ||
        doc.areasOfFocus.some((f) => f.toLowerCase().includes(query)) ||
        doc.bio.toLowerCase().includes(query);
    }

    return matchesFocus && matchesSearch;
  });

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Statutory Clinical Registry"
        title="Institutional Faculty & Licensed Tabeebs"
        subtitle="Senior clinical faculty holding statutory registration under the NCISM Act 2020 with combined decades of premier hospital leadership, integrating classical Greco-Arab Unani pulse diagnostics with contemporary pathology and multi-organ monitoring."
        breadcrumbs={[{ label: "Clinical Faculty & Doctors" }]}
        primaryCta={{ label: "Schedule Consultation", href: "/contact" }}
        secondaryCta={{ label: "Clinical Philosophy", href: "/about" }}
      />

      <div className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-10">
        
        {/* Filter and Search Bar */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm space-y-5">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-[#0F172A]">Filter Clinical Faculty</h2>
              <p className="text-xs text-slate-500">Search by name, clinical subspecialty, or therapeutic focus</p>
            </div>
            
            {/* Search Input */}
            <div className="relative w-full md:w-80">
              <input
                type="text"
                placeholder="Search clinician, condition, or term..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-slate-50 border border-slate-200 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-emerald-600 focus:bg-white transition"
              />
              <HealthcareIcon name="search" className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            </div>
          </div>

          {/* Specialization Filter Pills */}
          <div className="flex flex-wrap gap-2 pt-2 border-t border-slate-100">
            {focusAreas.map((area) => (
              <button
                key={area.id}
                onClick={() => setSelectedFocus(area.id)}
                className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                  selectedFocus === area.id
                    ? "bg-[#1B4332] text-white shadow-sm"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200/70 hover:text-slate-900"
                }`}
              >
                {area.label}
              </button>
            ))}
          </div>
        </div>

        {/* Results Count Banner */}
        <div className="flex items-center justify-between px-2 text-xs text-slate-500">
          <span>
            Showing <strong className="text-slate-800">{filteredDoctors.length}</strong> statutory registered practitioners
          </span>
          <div className="inline-flex items-center gap-1.5 text-emerald-800 font-medium">
            <HealthcareIcon name="shield-check" className="w-4 h-4 text-emerald-600" />
            <span>All practitioners verified under NCISM Act 2020</span>
          </div>
        </div>

        {/* Doctors Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {filteredDoctors.map((doc) => (
            <div
              key={doc.id}
              className="rounded-3xl bg-white border border-slate-200/90 p-7 shadow-sm hover:shadow-md hover:border-emerald-600/40 transition-all flex flex-col justify-between space-y-6"
            >
              <div className="space-y-5">
                {/* Header Profile Area */}
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#1B4332] to-[#2D6A4F] text-white font-extrabold flex items-center justify-center text-xl shadow-md shrink-0">
                      {doc.avatarInitials}
                    </div>
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <h3 className="font-bold text-[#0F172A] text-lg">{doc.name}</h3>
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-50 border border-emerald-200 text-[10px] font-bold text-emerald-800">
                          <HealthcareIcon name="shield-check" className="w-3 h-3 text-emerald-700" />
                          <span>NCISM Verified</span>
                        </span>
                      </div>
                      <p className="text-xs text-emerald-700 font-medium mt-0.5">{doc.designation}</p>
                      <p className="text-[11px] text-slate-500 font-mono mt-0.5">
                        {doc.regNumber} • {doc.degrees}
                      </p>
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <span className="inline-flex items-center gap-1.5 text-[11px] font-semibold text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                      {doc.consultationStatus || "Accepting Consultations"}
                    </span>
                    <span className="text-[10px] text-slate-500 block mt-1 font-mono">{doc.experienceYears}+ Years Clinical Exp</span>
                  </div>
                </div>

                {/* Biography excerpt */}
                <p className="text-xs text-slate-600 leading-relaxed">{doc.bio}</p>

                {/* Clinical Details Box */}
                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2.5 text-xs">
                  <div className="flex items-center gap-2">
                    <HealthcareIcon name="hospital" className="w-4 h-4 text-slate-500 shrink-0" />
                    <div>
                      <span className="text-[10px] font-bold uppercase text-slate-400 block tracking-wider">Facility Affiliation</span>
                      <span className="text-slate-800 font-medium text-[11px]">{doc.hospitalAffiliation}</span>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-3 pt-1 border-t border-slate-200/60">
                    <div className="flex items-center gap-2">
                      <HealthcareIcon name="clock" className="w-4 h-4 text-slate-500 shrink-0" />
                      <div>
                        <span className="text-[10px] font-bold text-slate-400 block">OPD Hours:</span>
                        <span className="text-slate-800 font-medium text-[11px]">{doc.clinicTimings}</span>
                      </div>
                    </div>
                    <div>
                      <span className="text-[10px] font-bold text-slate-400 block">Languages:</span>
                      <span className="text-slate-800 font-medium text-[11px]">{doc.languages.join(", ")}</span>
                    </div>
                  </div>
                </div>

                {/* Areas of Focus */}
                <div className="space-y-1.5">
                  <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Areas of Specialization:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {doc.areasOfFocus.map((focus, idx) => (
                      <span key={idx} className="text-[10px] px-2.5 py-1 rounded-lg bg-emerald-50 text-[#1B4332] border border-emerald-200/60 font-medium">
                        {focus}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Card Footer Actions */}
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between gap-3">
                <button
                  type="button"
                  onClick={() => setSelectedDoctor(doc)}
                  className="w-1/2 text-center py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-xs font-semibold text-slate-800 transition"
                >
                  View Full Credentials
                </button>
                <Link
                  href={`/contact?doctor=${doc.id}`}
                  className="w-1/2 text-center py-2.5 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-xs font-bold text-white shadow-sm transition"
                >
                  Book Consultation
                </Link>
              </div>
            </div>
          ))}
        </div>

        {/* Institutional Governance Callout */}
        <div className="rounded-3xl bg-white border border-slate-200/90 p-8 shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex items-start gap-3.5">
              <div className="p-2.5 rounded-xl bg-emerald-50 text-[#1B4332] shrink-0 border border-emerald-200">
                <HealthcareIcon name="shield-check" className="w-5 h-5" />
              </div>
              <div>
                <h4 className="font-bold text-sm text-[#0F172A]">NCISM Act 2020 Compliance</h4>
                <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                  Every practicing physician holds statutory registration with verified post-graduate qualifications in Unani medicine.
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3.5">
              <div className="p-2.5 rounded-xl bg-teal-50 text-[#2D6A4F] shrink-0 border border-teal-200">
                <HealthcareIcon name="lock" className="w-5 h-5" />
              </div>
              <div>
                <h4 className="font-bold text-sm text-[#0F172A]">DPDP Act 2023 Confidentiality</h4>
                <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                  Patient clinical consultations, electronic health records, and prescription communications are end-to-end encrypted.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3.5">
              <div className="p-2.5 rounded-xl bg-amber-50 text-amber-800 shrink-0 border border-amber-200">
                <HealthcareIcon name="pill" className="w-5 h-5" />
              </div>
              <div>
                <h4 className="font-bold text-sm text-[#0F172A]">Schedule E(1) Safety Assurance</h4>
                <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                  All potent classical formulations require documented Mudabbar detoxification certificates before pharmacy dispensing.
                </p>
              </div>
            </div>
          </div>
        </div>

      </div>

      {/* Doctor Full Credentials Modal */}
      {selectedDoctor && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fadeIn">
          <div className="bg-white rounded-3xl border border-slate-200 shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 space-y-6">
            
            <div className="flex items-start justify-between border-b border-slate-100 pb-5">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-2xl bg-[#1B4332] text-white font-extrabold flex items-center justify-center text-2xl shadow-md">
                  {selectedDoctor.avatarInitials}
                </div>
                <div>
                  <h3 className="text-xl font-bold text-[#0F172A]">{selectedDoctor.name}</h3>
                  <p className="text-xs text-emerald-700 font-medium">{selectedDoctor.designation}</p>
                  <p className="text-xs text-slate-500 font-mono mt-0.5">{selectedDoctor.regNumber} • {selectedDoctor.degrees}</p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setSelectedDoctor(null)}
                className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition"
              >
                <HealthcareIcon name="x" className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4 text-xs">
              <div>
                <h4 className="font-bold text-[#0F172A] uppercase tracking-wider text-[11px] mb-1.5">Clinical Approach & Philosophy</h4>
                <p className="text-slate-600 leading-relaxed italic bg-slate-50 p-3.5 rounded-2xl border border-slate-200/80">
                  "{selectedDoctor.clinicalApproach}"
                </p>
              </div>

              <div>
                <h4 className="font-bold text-[#0F172A] uppercase tracking-wider text-[11px] mb-2">Statutory Credentials & Education</h4>
                <ul className="space-y-1.5">
                  {selectedDoctor.educationAndCredentials.map((edu, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-slate-700">
                      <HealthcareIcon name="check" className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                      <span>{edu}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {selectedDoctor.publishedWorks && selectedDoctor.publishedWorks.length > 0 && (
                <div>
                  <h4 className="font-bold text-[#0F172A] uppercase tracking-wider text-[11px] mb-2">Peer-Reviewed Publications & Clinical Studies</h4>
                  <ul className="space-y-1.5">
                    {selectedDoctor.publishedWorks.map((pub, idx) => (
                      <li key={idx} className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/70 text-slate-700 flex items-start gap-2">
                        <HealthcareIcon name="file-text" className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
                        <span>{pub}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="pt-4 border-t border-slate-100 flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={() => setSelectedDoctor(null)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition"
              >
                Close
              </button>
              <Link
                href={`/contact?doctor=${selectedDoctor.id}`}
                className="px-6 py-2.5 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-xs font-bold text-white shadow-sm transition"
              >
                Schedule Consultation
              </Link>
            </div>

          </div>
        </div>
      )}

    </PublicWebsiteShell>
  );
}
