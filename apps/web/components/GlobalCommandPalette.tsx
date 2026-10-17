"use client";

import React, { useState, useEffect, useRef } from "react";
import { searchApi, type SearchResultItem } from "@/lib/searchApi";

interface GlobalCommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onNavigate: (tab: string) => void;
}

export function GlobalCommandPalette({
  isOpen,
  onClose,
  onNavigate,
}: GlobalCommandPaletteProps) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResultItem[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // Focus input when opened
  useEffect(() => {
    if (isOpen) {
      setQuery("");
      setSelectedIndex(0);
      loadInitialResults();
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [isOpen]);

  const loadInitialResults = async () => {
    setIsLoading(true);
    try {
      const items = await searchApi.omniSearch("");
      setResults(items);
    } catch {
      // ignore
    } finally {
      setIsLoading(false);
    }
  };

  // Live search debounced
  useEffect(() => {
    if (!isOpen) return;
    const timer = setTimeout(async () => {
      setIsLoading(true);
      try {
        const items = await searchApi.omniSearch(query);
        setResults(items);
        setSelectedIndex(0);
      } catch {
        // ignore
      } finally {
        setIsLoading(false);
      }
    }, 150);

    return () => clearTimeout(timer);
  }, [query, isOpen]);

  // Keyboard navigation inside modal
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") {
      onClose();
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1 < results.length ? prev + 1 : 0));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 >= 0 ? prev - 1 : results.length - 1));
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (results[selectedIndex]) {
        handleSelectItem(results[selectedIndex]);
      }
    }
  };

  const handleSelectItem = (item: SearchResultItem) => {
    onNavigate(item.route);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 bg-black/75 backdrop-blur-xs flex items-start justify-center pt-20 p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700/80 rounded-2xl max-w-2xl w-full shadow-2xl overflow-hidden flex flex-col"
        onClick={(e) => e.stopPropagation()}
        onKeyDown={handleKeyDown}
      >
        {/* Search Input Bar */}
        <div className="flex items-center px-4 py-3.5 border-b border-slate-800 bg-slate-950">
          <span className="text-slate-400 text-lg mr-3">🔍</span>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type a command or search herbs, formulations, Amraz, or ICD-11..."
            className="w-full bg-transparent text-slate-100 placeholder-slate-500 text-sm focus:outline-none font-sans"
          />
          {query && (
            <button
              onClick={() => setQuery("")}
              className="text-slate-500 hover:text-slate-300 text-xs px-2 py-0.5"
            >
              Clear
            </button>
          )}
          <kbd className="hidden sm:inline-block ml-2 px-2 py-0.5 text-[10px] font-mono text-slate-400 bg-slate-800 border border-slate-700 rounded">
            ESC
          </kbd>
        </div>

        {/* Results List */}
        <div className="max-h-96 overflow-y-auto p-2 space-y-1">
          {isLoading && (
            <div className="py-6 text-center text-xs text-slate-500">
              Searching across ZAYVORA Knowledge & Clinical Graph...
            </div>
          )}

          {!isLoading && results.length === 0 && (
            <div className="py-8 text-center text-xs text-slate-500">
              No matching clinical entities found for "{query}".
            </div>
          )}

          {!isLoading &&
            results.map((item, index) => {
              const isSelected = index === selectedIndex;
              return (
                <div
                  key={item.id}
                  onClick={() => handleSelectItem(item)}
                  onMouseEnter={() => setSelectedIndex(index)}
                  className={`flex items-center justify-between p-2.5 rounded-xl cursor-pointer transition ${
                    isSelected
                      ? "bg-slate-800 text-white"
                      : "text-slate-300 hover:bg-slate-800/50"
                  }`}
                >
                  <div className="flex items-center gap-3 overflow-hidden">
                    <span className="text-base">
                      {item.category === "navigation" && "⚡"}
                      {item.category === "mufradat" && "🌿"}
                      {item.category === "murakkabat" && "🏺"}
                      {item.category === "amraz" && "🩺"}
                      {item.category === "tadbeer" && "🩹"}
                    </span>
                    <div className="truncate">
                      <div className="font-semibold text-xs tracking-wide truncate">
                        {item.title}
                      </div>
                      <div className="text-[11px] text-slate-400 truncate mt-0.5">
                        {item.subtitle}
                      </div>
                    </div>
                  </div>

                  {item.badge && (
                    <span
                      className={`ml-3 px-2 py-0.5 rounded text-[10px] font-mono whitespace-nowrap font-medium ${
                        item.badge.includes("E(1)")
                          ? "bg-red-500/20 text-red-400 border border-red-500/30"
                          : item.badge === "Shortcut"
                          ? "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                          : "bg-slate-800 text-slate-400 border border-slate-700"
                      }`}
                    >
                      {item.badge}
                    </span>
                  )}
                </div>
              );
            })}
        </div>

        {/* Footer info */}
        <div className="px-4 py-2 border-t border-slate-800 bg-slate-950/80 flex items-center justify-between text-[11px] text-slate-500 font-mono">
          <div className="flex items-center gap-2">
            <span>Navigate: <kbd className="px-1 py-0.5 bg-slate-800 rounded">↑</kbd> <kbd className="px-1 py-0.5 bg-slate-800 rounded">↓</kbd></span>
            <span>Select: <kbd className="px-1 py-0.5 bg-slate-800 rounded">↵</kbd></span>
          </div>
          <span>ZAYVORA Omni-Search 2035</span>
        </div>
      </div>
    </div>
  );
}
