"use client";

import React, { useState } from "react";
import Link from "next/link";
import { KNOWLEDGE_ARTICLES } from "@/lib/cms/articlesData";

export default function KnowledgeCentrePage() {
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [searchQuery, setSearchQuery] = useState("");

  const categories = [
    "All",
    "Unani Medicine",
    "Gut Health",
    "Liver Health",
    "Fertility",
    "Hormonal Health",
    "Sleep and Stress",
    "Nutrition",
    "Lifestyle",
    "Preventive Care"
  ];

  const filteredArticles = KNOWLEDGE_ARTICLES.filter((art) => {
    const matchesCategory = selectedCategory === "All" || art.category === selectedCategory;
    const matchesSearch = searchQuery.trim() === "" ||
      art.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      art.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
      art.author.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12 space-y-10 text-[#CBD5E1]">
      
      {/* Header */}
      <div className="border-b border-[#1E293B] pb-8 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold">
          <span>📚</span> Peer-Reviewed Unani Medical Repository
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Clinical Knowledge Center
        </h1>
        <p className="text-sm text-[#94A3B8] max-w-3xl leading-relaxed">
          Clinician-reviewed educational monographs, constitutional science explanations, and lifestyle guides bridging classical Greco-Arab manuscripts with contemporary cellular biology.
        </p>
      </div>

      {/* Category Pills & Search Toolbar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 rounded-2xl bg-[#0F172A] border border-[#334155]">
        <div className="flex flex-wrap gap-2">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition ${
                selectedCategory === cat
                  ? "bg-[#0D9488] text-white"
                  : "bg-[#1E293B] text-[#94A3B8] hover:text-white"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        <div className="relative w-full md:w-64">
          <span className="absolute left-3 top-2.5 text-xs text-[#64748B]">🔍</span>
          <input
            placeholder="Search articles & authors..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-8 pr-4 py-2 rounded-xl bg-[#1E293B] border border-[#334155] text-xs text-white placeholder-[#64748B] focus:outline-none focus:border-[#0D9488]"
          />
        </div>
      </div>

      {/* Articles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredArticles.map((art) => (
          <div
            key={art.id}
            className="rounded-3xl bg-[#0F172A] border border-[#334155] p-6 space-y-4 hover:border-[#0D9488] transition flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex justify-between items-center text-[10px]">
                <span className="font-bold px-2.5 py-0.5 rounded-full bg-[#1E293B] text-[#2DD4BF] border border-[#334155]">
                  {art.category}
                </span>
                <span className="text-[#64748B] font-mono">{art.readTimeMinutes} min read</span>
              </div>

              <h3 className="text-lg font-bold text-white leading-snug hover:text-[#2DD4BF] transition">
                <Link href={`/website/article?id=${art.id}`}>
                  {art.title}
                </Link>
              </h3>

              <p className="text-xs text-[#94A3B8] leading-relaxed line-clamp-3">{art.summary}</p>
            </div>

            <div className="pt-4 border-t border-[#1E293B] space-y-2">
              <div className="text-[11px] text-[#64748B] flex items-center justify-between">
                <span>By {art.author}</span>
                <span>{art.publishDate}</span>
              </div>
              <div className="flex items-center justify-between pt-1">
                <span className="text-[10px] text-emerald-400 font-medium">✓ Clinically Reviewed</span>
                <Link
                  href={`/website/article?id=${art.id}`}
                  className="text-xs font-bold text-[#0D9488] hover:text-white transition"
                >
                  Read Article →
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
