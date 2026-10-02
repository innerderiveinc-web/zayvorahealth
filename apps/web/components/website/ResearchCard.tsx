import React from "react";
import Link from "next/link";
import { ResearchItem } from "@/lib/data/types";

interface ResearchCardProps {
  item: ResearchItem;
}

export function ResearchCard({ item }: ResearchCardProps) {
  return (
    <div className="rounded-2xl bg-[#0D1527] border border-[#1E293B] hover:border-[#6366F1]/50 p-6 sm:p-8 flex flex-col justify-between transition-all duration-200">
      <div>
        <div className="flex items-center justify-between gap-2 mb-3">
          <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-[#1E293B] text-[#94A3B8] border border-[#334155]">
            {item.categoryLabel}
          </span>
          <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-[#3B82F6]/20 text-[#60A5FA] border border-[#3B82F6]/30">
            {item.evidenceGrade}
          </span>
        </div>

        <h3 className="text-lg font-bold text-white leading-snug">
          {item.title}
        </h3>

        <p className="mt-3 text-sm text-[#94A3B8] leading-relaxed">
          {item.summary}
        </p>

        <div className="mt-4 space-y-2 text-xs">
          <div className="p-3 rounded-xl bg-[#0A0F1D] border border-[#1E293B]">
            <p className="font-semibold text-[#CBD5E1]">Methodology:</p>
            <p className="text-[#94A3B8] mt-0.5">{item.methodology}</p>
          </div>
          <div className="p-3 rounded-xl bg-[#0F766E]/10 border border-[#0D9488]/20">
            <p className="font-semibold text-[#5EEAD4]">Clinical Significance:</p>
            <p className="text-[#CCFBF1] mt-0.5">{item.significance}</p>
          </div>
        </div>
      </div>

      <div className="mt-6 pt-4 border-t border-[#1E293B] flex items-center justify-between">
        <span className="text-xs font-medium text-[#64748B]">
          Status: <strong className="text-[#CBD5E1]">{item.status}</strong>
        </span>
        <Link
          href={item.href}
          className="text-xs font-semibold text-[#818CF8] hover:text-white flex items-center gap-1 transition"
        >
          <span>Read Protocol</span>
          <span>→</span>
        </Link>
      </div>
    </div>
  );
}
