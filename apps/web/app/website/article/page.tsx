"use client";

import React from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { KNOWLEDGE_ARTICLES } from "@/lib/cms/articlesData";

export default function ArticleDetailPage() {
  const searchParams = useSearchParams();
  const artId = searchParams.get("id") || "art-mizaj-basics";

  const article = KNOWLEDGE_ARTICLES.find(a => a.id === artId) || KNOWLEDGE_ARTICLES[0];

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12 space-y-10 text-[#CBD5E1]">
      
      {/* Breadcrumbs */}
      <div className="flex items-center gap-2 text-xs text-[#64748B]">
        <Link href="/website" className="hover:text-white">Home</Link>
        <span>/</span>
        <Link href="/website/knowledge-centre" className="hover:text-white">Knowledge Center</Link>
        <span>/</span>
        <span className="text-white font-medium truncate">{article.title}</span>
      </div>

      {/* Article Header */}
      <div className="space-y-4 border-b border-[#1E293B] pb-8">
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <span className="px-3 py-1 rounded-full bg-[#0D9488]/20 text-[#2DD4BF] font-bold">
            {article.category}
          </span>
          <span className="text-[#64748B]">•</span>
          <span className="text-[#94A3B8]">{article.readTimeMinutes} min read</span>
          <span className="text-[#64748B]">•</span>
          <span className="text-[#94A3B8]">Published: {article.publishDate}</span>
        </div>

        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
          {article.title}
        </h1>

        <p className="text-base text-[#94A3B8] leading-relaxed italic border-l-2 border-[#0D9488] pl-4">
          "{article.heroExcerpt}"
        </p>

        <div className="p-3 rounded-xl bg-[#0F172A] border border-[#334155] flex flex-col sm:flex-row sm:items-center justify-between text-xs gap-2">
          <div>Author: <strong className="text-white">{article.author}</strong></div>
          <div className="text-emerald-400 font-medium">✓ {article.reviewer}</div>
        </div>
      </div>

      {/* Article Body Sections */}
      <div className="space-y-8 text-sm leading-relaxed text-[#CBD5E1]">
        {article.sections.map((sec, idx) => (
          <div key={idx} className="space-y-3">
            <h2 className="text-xl font-bold text-white tracking-tight">{sec.heading}</h2>
            {sec.body.map((p, pIdx) => (
              <p key={pIdx} className="text-[#94A3B8] leading-relaxed">{p}</p>
            ))}
          </div>
        ))}
      </div>

      {/* Key Clinical Takeaways */}
      <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-3">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <span>💡</span> Key Clinical Takeaways
        </h3>
        <ul className="space-y-2 text-xs text-[#94A3B8]">
          {article.keyTakeaways.map((takeaway, idx) => (
            <li key={idx} className="flex items-start gap-2">
              <span className="text-[#0D9488] font-bold">✓</span>
              <span>{takeaway}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Classical & Biomedical Citations */}
      <div className="p-6 rounded-3xl bg-[#0A0F1D] border border-[#1E293B] space-y-2 text-xs text-[#64748B]">
        <h4 className="font-bold text-white uppercase tracking-wider text-[11px]">References & Citations:</h4>
        <ul className="space-y-1 text-[11px]">
          {article.citations.map((cit, idx) => (
            <li key={idx}>[{idx + 1}] {cit}</li>
          ))}
        </ul>
      </div>

      {/* Bottom Nav */}
      <div className="pt-6 border-t border-[#1E293B] flex items-center justify-between">
        <Link href="/website/knowledge-centre" className="text-xs font-semibold text-[#94A3B8] hover:text-white">
          ← Back to Knowledge Center
        </Link>
        <Link
          href="/website/book"
          className="px-5 py-2.5 rounded-xl bg-[#0D9488] text-white font-bold text-xs hover:bg-[#0F766E] shadow-sm transition"
        >
          Discuss with a Clinician
        </Link>
      </div>

    </div>
  );
}
