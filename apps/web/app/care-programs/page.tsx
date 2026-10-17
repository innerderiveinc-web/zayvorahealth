"use client";

import React, { useState } from "react";
import Link from "next/link";
import { HEALTH_PROGRAMS } from "@/lib/cms/programsData";

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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12 space-y-10 text-[#CBD5E1]">
      
      {/* Header */}
      <div className="border-b border-[#1E293B] pb-8 space-y-3">
        <span className="text-[11px] font-bold text-[#0D9488] uppercase tracking-wider block">
          Clinician-Guided Care Pathways
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          ZAYVORA Health Programs
        </h1>
        <p className="text-sm text-[#94A3B8] max-w-3xl leading-relaxed">
          Multi-week structured clinical care programs designed to restore constitutional humoral equilibrium (Mizaj) and physiological organ-axis health under direct physician supervision.
        </p>
      </div>

      {/* Search & Category Filter Toolbar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 rounded-2xl bg-[#0F172A] border border-[#334155]">
        {/* Category Pills */}
        <div className="flex flex-wrap gap-2">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition ${
                selectedCategory === cat
                  ? "bg-[#0D9488] text-white shadow-sm"
                  : "bg-[#1E293B] text-[#94A3B8] hover:text-white"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Search Input */}
        <div className="relative w-full md:w-72">
          <span className="absolute left-3 top-2.5 text-xs text-[#64748B]">🔍</span>
          <input
            placeholder="Search symptoms or programs..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-8 pr-4 py-2 rounded-xl bg-[#1E293B] border border-[#334155] text-xs text-white placeholder-[#64748B] focus:outline-none focus:border-[#0D9488]"
          />
        </div>
      </div>

      {/* Program Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredPrograms.map((prog) => (
          <div
            key={prog.id}
            className="rounded-3xl bg-[#0F172A] border border-[#334155] p-6 space-y-5 hover:border-[#0D9488] transition flex flex-col justify-between"
          >
            <div className="space-y-4">
              <div className="flex justify-between items-center text-[10px]">
                <span className="px-2.5 py-1 rounded-full bg-[#0D9488]/20 text-[#2DD4BF] font-mono font-bold">
                  {prog.duration}
                </span>
                <span className="text-[#64748B] font-semibold">{prog.category}</span>
              </div>

              <h2 className="text-xl font-bold text-white leading-snug">{prog.title}</h2>
              <p className="text-xs text-[#94A3B8] leading-relaxed">{prog.shortDescription}</p>

              {/* Who may benefit */}
              <div className="space-y-1.5 pt-3 border-t border-[#1E293B]">
                <span className="text-[10px] font-bold text-white uppercase tracking-wider block">
                  Who May Benefit:
                </span>
                <ul className="space-y-1 text-[11px] text-[#94A3B8]">
                  {prog.suitableAudience.slice(0, 2).map((item, idx) => (
                    <li key={idx} className="flex items-start gap-1.5">
                      <span className="text-[#0D9488]">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Inclusions */}
              <div className="space-y-1.5 pt-3 border-t border-[#1E293B]">
                <span className="text-[10px] font-bold text-white uppercase tracking-wider block">
                  What Is Included:
                </span>
                <ul className="space-y-1 text-[11px] text-[#64748B]">
                  {prog.inclusions.slice(0, 3).map((item, idx) => (
                    <li key={idx} className="flex items-start gap-1.5">
                      <span className="text-emerald-400">✓</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Actions */}
            <div className="pt-5 border-t border-[#1E293B] flex items-center justify-between gap-3">
              <Link
                href={`/website/program?id=${prog.id}`}
                className="w-1/2 text-center py-2.5 rounded-xl bg-[#1E293B] text-xs font-semibold text-white hover:bg-[#334155] transition"
              >
                View Details
              </Link>
              <Link
                href="/contact"
                className="w-1/2 text-center py-2.5 rounded-xl bg-[#0D9488] text-xs font-bold text-white hover:bg-[#0F766E] shadow-sm transition"
              >
                Book Consult
              </Link>
            </div>
          </div>
        ))}
      </div>

      {filteredPrograms.length === 0 && (
        <div className="text-center py-16 p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-3">
          <span className="text-3xl block">🔍</span>
          <h3 className="text-base font-bold text-white">No Programs Found</h3>
          <p className="text-xs text-[#94A3B8]">No health programs match your search query. Try choosing another category.</p>
          <button
            onClick={() => { setSelectedCategory("All"); setSearchQuery(""); }}
            className="px-4 py-2 rounded-xl bg-[#0D9488] text-white text-xs font-bold"
          >
            Reset Filters
          </button>
        </div>
      )}

    </div>
  );
}
