"use client";

import React, { useState } from "react";
import { FaqItem } from "@/lib/data/types";

interface FaqAccordionProps {
  items: FaqItem[];
  showCategoryFilter?: boolean;
}

export function FaqAccordion({ items, showCategoryFilter = true }: FaqAccordionProps) {
  const [openId, setOpenId] = useState<string | null>(items[0]?.id || null);
  const [selectedCategory, setSelectedCategory] = useState<string>("All");

  const categories = ["All", ...Array.from(new Set(items.map(item => item.category)))];

  const filteredItems = selectedCategory === "All"
    ? items
    : items.filter(item => item.category === selectedCategory);

  return (
    <div className="w-full">
      {/* Category filter pills */}
      {showCategoryFilter && (
        <div className="flex flex-wrap gap-2 mb-8 justify-center">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-4 py-2 rounded-full text-xs font-semibold transition ${
                selectedCategory === cat
                  ? "bg-[#0D9488] text-white shadow-md"
                  : "bg-[#1E293B] text-[#94A3B8] hover:bg-[#334155] hover:text-white"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      )}

      {/* Accordion List */}
      <div className="space-y-4 max-w-3xl mx-auto">
        {filteredItems.map((item) => {
          const isOpen = openId === item.id;
          return (
            <div
              key={item.id}
              className="rounded-2xl bg-[#0D1527] border border-[#1E293B] overflow-hidden transition-all"
            >
              <button
                type="button"
                onClick={() => setOpenId(isOpen ? null : item.id)}
                className="w-full p-5 sm:p-6 text-left flex items-center justify-between gap-4 focus:outline-none focus:ring-2 focus:ring-[#0D9488]"
                aria-expanded={isOpen}
              >
                <div className="flex items-center gap-3">
                  <span className="text-xs font-semibold px-2 py-0.5 rounded bg-[#1E293B] text-[#64748B]">
                    {item.category}
                  </span>
                  <span className="text-base sm:text-lg font-bold text-white">
                    {item.question}
                  </span>
                </div>
                <span className="text-xl font-bold text-[#5EEAD4] shrink-0 transition-transform">
                  {isOpen ? "−" : "+"}
                </span>
              </button>

              {isOpen && (
                <div className="px-5 pb-5 sm:px-6 sm:pb-6 text-sm sm:text-base text-[#94A3B8] leading-relaxed border-t border-[#1E293B] pt-4">
                  {item.answer}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
