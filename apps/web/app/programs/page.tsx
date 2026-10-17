"use client";

import React, { useState } from "react";
import Link from "next/link";
import { HEALTH_PROGRAMS } from "@/lib/cms/programsData";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export default function ProgramsListingPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [searchQuery, setSearchQuery] = useState<string>("");

  const categories = [
    "All",
    "Men's Health",
    "Women's Health",
    "Metabolic Health",
    "Gut & Liver",
    "Stress & Sleep",
    "General Wellness"
  ];

  const filteredPrograms = HEALTH_PROGRAMS.filter((prog) => {
    const matchesCategory = selectedCategory === "All" || prog.category === selectedCategory;
    const matchesSearch = searchQuery.trim() === "" ||
      prog.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      prog.shortDescription.toLowerCase().includes(searchQuery.toLowerCase()) ||
      prog.suitableAudience.some(a => a.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Clinician-Guided Care Pathways"
        title="Structured Clinical Health Programs"
        subtitle="Multi-week therapeutic pathways designed to restore constitutional humoral balance (Mizaj) and organ-axis equilibrium under direct senior clinician supervision."
        breadcrumbs={[{ label: "Care Programs" }]}
        primaryCta={{ label: "Consult Clinical Coordinator", href: "/contact" }}
        secondaryCta={{ label: "Clinical Philosophy", href: "/about" }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
        
        {/* Search & Category Filter Toolbar */}
        <div className="bg-white rounded-3xl border border-slate-200/90 p-6 shadow-sm space-y-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-base font-bold text-[#0F172A]">Filter Clinical Programs</h2>
              <p className="text-xs text-slate-500">Explore multi-week care protocols tailored to your health profile</p>
            </div>

            {/* Search Input */}
            <div className="relative w-full md:w-80">
              <input
                placeholder="Search symptoms or programs..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-slate-50 border border-slate-200 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-emerald-600 focus:bg-white transition"
              />
              <HealthcareIcon name="search" className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            </div>
          </div>

          {/* Category Pills */}
          <div className="flex flex-wrap gap-2 pt-2 border-t border-slate-100">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-2 rounded-xl text-xs font-semibold transition ${
                  selectedCategory === cat
                    ? "bg-[#1B4332] text-white shadow-sm"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Results Banner */}
        <div className="flex items-center justify-between px-2 text-xs text-slate-500">
          <span>
            Showing <strong className="text-slate-900">{filteredPrograms.length}</strong> clinician-supervised care programs
          </span>
          <span className="text-emerald-800 font-medium">All programs supervised by NCISM Act 2020 registered clinicians</span>
        </div>

        {/* Program Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredPrograms.map((prog) => (
            <div
              key={prog.id}
              className="rounded-3xl bg-white border border-slate-200/90 p-7 shadow-sm hover:shadow-md hover:border-emerald-600/40 transition flex flex-col justify-between space-y-6"
            >
              <div className="space-y-4">
                <div className="flex justify-between items-center text-xs">
                  <span className="px-3 py-1 rounded-full bg-emerald-50 text-[#1B4332] border border-emerald-200 font-bold text-[11px]">
                    {prog.duration}
                  </span>
                  <span className="text-slate-400 font-medium text-[11px]">{prog.category}</span>
                </div>

                <h3 className="text-xl font-bold text-[#0F172A] leading-snug">{prog.title}</h3>
                <p className="text-xs text-slate-600 leading-relaxed">{prog.shortDescription}</p>

                {/* Who may benefit */}
                <div className="space-y-1.5 pt-3 border-t border-slate-100">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                    Target Indications:
                  </span>
                  <ul className="space-y-1 text-xs text-slate-700">
                    {prog.suitableAudience.slice(0, 2).map((item, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <HealthcareIcon name="check" className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Inclusions */}
                <div className="space-y-1.5 pt-3 border-t border-slate-100">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                    Protocol Inclusions:
                  </span>
                  <ul className="space-y-1 text-xs text-slate-500">
                    {prog.inclusions.slice(0, 3).map((item, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-slate-300 mt-1.5 shrink-0" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Actions */}
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between gap-3">
                <Link
                  href={`/contact?program=${encodeURIComponent(prog.title)}`}
                  className="w-full text-center py-2.5 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-xs font-bold text-white shadow-sm transition"
                >
                  Inquire Program Details
                </Link>
              </div>
            </div>
          ))}
        </div>

        {filteredPrograms.length === 0 && (
          <div className="text-center py-16 p-8 rounded-3xl bg-white border border-slate-200/90 shadow-sm space-y-3">
            <HealthcareIcon name="search" className="w-10 h-10 text-slate-300 mx-auto" />
            <h3 className="text-base font-bold text-[#0F172A]">No Programs Found</h3>
            <p className="text-xs text-slate-500">No health programs match your search query. Try choosing another category.</p>
            <div className="pt-2">
              <button
                onClick={() => { setSelectedCategory("All"); setSearchQuery(""); }}
                className="px-5 py-2.5 rounded-xl bg-[#1B4332] text-white text-xs font-bold hover:bg-[#2D6A4F] transition"
              >
                Reset Search Filters
              </button>
            </div>
          </div>
        )}

      </div>
    </PublicWebsiteShell>
  );
}
