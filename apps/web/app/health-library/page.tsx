"use client";

import React, { useState, useMemo } from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { HEALTH_LIBRARY_ARTICLES } from "@/lib/data/healthLibrary";

const CATEGORIES = [
  "All",
  "Conditions",
  "Symptoms",
  "Tests",
  "Treatments",
  "Lifestyle",
  "Unani Concepts",
  "Patient Guides"
] as const;

export default function HealthLibraryIndexPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [searchQuery, setSearchQuery] = useState<string>("");

  const filteredArticles = useMemo(() => {
    return HEALTH_LIBRARY_ARTICLES.filter((article) => {
      const matchesCategory =
        selectedCategory === "All" || article.category === selectedCategory;
      const q = searchQuery.toLowerCase().trim();
      const matchesSearch =
        !q ||
        article.title.toLowerCase().includes(q) ||
        article.summary.toLowerCase().includes(q) ||
        article.clinicalReviewer.name.toLowerCase().includes(q);
      return matchesCategory && matchesSearch;
    });
  }, [selectedCategory, searchQuery]);

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Evidence-Based Health Library"
        title="Authoritative Health Knowledge & Classical Wisdom"
        subtitle="Clinician-reviewed medical guidance conforming strictly to NHS Digital editorial principles and NCISM Act 2020 clinical governance standards."
        breadcrumbs={[{ label: "Health Library" }]}
        primaryCta={{ label: "Explore Clinical Monograms", href: "#articles" }}
        secondaryCta={{ label: "Schedule Consultation", href: "/contact" }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
        
        {/* Emergency Medical Safety Banner */}
        <div className="rounded-3xl bg-red-50 border border-red-200 p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-5 shadow-sm">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-2xl bg-red-100 border border-red-300 flex items-center justify-center text-red-700 shrink-0">
              <HealthcareIcon name="alert-triangle" className="w-6 h-6 text-red-600" />
            </div>
            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <h3 className="text-red-900 font-bold text-base tracking-wide">
                  Emergency Medical Guidance
                </h3>
                <span className="text-[10px] font-bold bg-red-600 text-white px-2 py-0.5 rounded-full uppercase tracking-wider">
                  STAT Protocol
                </span>
              </div>
              <p className="text-red-800 text-xs sm:text-sm mt-1 leading-relaxed max-w-3xl">
                The ZAYVORA Health Library is for educational and constitutional wellness guidance. If you experience acute chest pain, sudden breathlessness, signs of stroke, or severe bleeding, immediately call <strong className="text-red-900 font-bold underline">112 (National Emergency)</strong> or go to the nearest hospital casualty department.
              </p>
            </div>
          </div>
          <Link
            href="/contact"
            className="shrink-0 px-5 py-2.5 bg-red-700 hover:bg-red-800 text-white font-semibold text-xs rounded-xl transition shadow-sm"
          >
            Emergency Advice
          </Link>
        </div>

        {/* Editorial Trust & NCISM Certification Bar */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 rounded-3xl bg-white border border-slate-200/90 shadow-sm flex items-start gap-4">
            <div className="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-[#1B4332] shrink-0">
              <HealthcareIcon name="stethoscope" className="w-6 h-6 text-emerald-700" />
            </div>
            <div>
              <p className="text-sm font-bold text-[#0F172A]">Board-Certified Clinicians</p>
              <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                Every monograph is vetted and signed off by an NCISM-registered consultant tabeeb.
              </p>
            </div>
          </div>

          <div className="p-6 rounded-3xl bg-white border border-slate-200/90 shadow-sm flex items-start gap-4">
            <div className="w-12 h-12 rounded-2xl bg-teal-50 border border-teal-200 flex items-center justify-center text-[#2D6A4F] shrink-0">
              <HealthcareIcon name="book" className="w-6 h-6 text-[#2D6A4F]" />
            </div>
            <div>
              <p className="text-sm font-bold text-[#0F172A]">Dual-Origin Provenance</p>
              <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                Synthesizes classical pharmacopoeias (Al-Qanun, UPI) with contemporary peer-reviewed RCTs.
              </p>
            </div>
          </div>

          <div className="p-6 rounded-3xl bg-white border border-slate-200/90 shadow-sm flex items-start gap-4">
            <div className="w-12 h-12 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-700 shrink-0">
              <HealthcareIcon name="scale" className="w-6 h-6 text-slate-600" />
            </div>
            <div>
              <p className="text-sm font-bold text-[#0F172A]">Editorial Independence</p>
              <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                Zero commercial bias. Strictly compliant with NHS Digital information quality benchmarks.
              </p>
            </div>
          </div>
        </div>

        {/* Search & Category Filter Controls */}
        <div id="articles" className="bg-white rounded-3xl border border-slate-200/90 p-6 shadow-sm space-y-5">
          <div className="flex flex-col sm:flex-row gap-4 justify-between items-center">
            {/* Search Input */}
            <div className="w-full sm:w-96 relative">
              <input
                type="text"
                placeholder="Search conditions, symptoms, or remedies..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400 text-xs focus:outline-none focus:border-emerald-600 focus:bg-white transition"
              />
              <HealthcareIcon name="search" className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            </div>

            {/* Results Count */}
            <span className="text-xs font-medium text-slate-500 self-end sm:self-center">
              Showing <strong className="text-slate-900">{filteredArticles.length}</strong> certified monographs
            </span>
          </div>

          {/* Category Tabs */}
          <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none pt-2 border-t border-slate-100">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
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

        {/* Article Grid */}
        {filteredArticles.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredArticles.map((article) => (
              <article
                key={article.slug}
                className="rounded-3xl bg-white border border-slate-200/90 hover:border-emerald-600/40 p-6 flex flex-col justify-between shadow-sm hover:shadow-md transition-all space-y-6"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-[#1B4332] border border-emerald-200">
                      {article.category}
                    </span>
                    <span className="text-[11px] text-slate-400 font-medium flex items-center gap-1">
                      <HealthcareIcon name="clock" className="w-3.5 h-3.5 text-slate-400" />
                      <span>{article.readingTimeMinutes} min read</span>
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-[#0F172A] mb-2 leading-snug line-clamp-2">
                    {article.title}
                  </h3>

                  <p className="text-xs text-slate-600 leading-relaxed line-clamp-3">
                    {article.summary}
                  </p>
                </div>

                <div className="pt-4 border-t border-slate-100">
                  {/* Clinical Reviewer Badge */}
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-8 h-8 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-[10px] font-bold text-[#1B4332]">
                      MD
                    </div>
                    <div className="text-[11px] leading-tight">
                      <p className="text-slate-900 font-semibold">Reviewed by {article.clinicalReviewer.name}</p>
                      <p className="text-slate-400 text-[10px] font-mono">NCISM: {article.clinicalReviewer.ncismRegNumber}</p>
                    </div>
                  </div>

                  <Link
                    href={`/health-library/${article.slug}`}
                    className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-slate-100 hover:bg-[#1B4332] hover:text-white text-slate-800 text-xs font-semibold transition"
                  >
                    <span>Read Full Clinical Monograph</span>
                    <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </article>
            ))}
          </div>
        ) : (
          <div className="py-16 text-center rounded-3xl bg-white border border-slate-200/90 shadow-sm p-8">
            <HealthcareIcon name="book" className="w-10 h-10 text-slate-400 mx-auto mb-3" />
            <p className="text-base font-bold text-[#0F172A]">No clinical monographs found</p>
            <p className="text-xs text-slate-500 mt-1">Try modifying your search keywords or switching category filters.</p>
            <button
              onClick={() => {
                setSelectedCategory("All");
                setSearchQuery("");
              }}
              className="mt-4 px-5 py-2 rounded-xl bg-[#1B4332] text-white text-xs font-semibold hover:bg-[#2D6A4F] transition"
            >
              Reset Search & Filters
            </button>
          </div>
        )}

      </div>
    </PublicWebsiteShell>
  );
}
