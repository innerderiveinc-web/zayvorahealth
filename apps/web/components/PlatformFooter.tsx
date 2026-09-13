"use client";

import React, { useState } from "react";
import Link from "next/link";

export function PlatformFooter() {
  const [lang, setLang] = useState<"EN" | "HI" | "UR">("EN");
  const [darkMode, setDarkMode] = useState(true);

  return (
    <footer className="w-full border-t border-[var(--border)] bg-[var(--panel)] text-xs text-[var(--muted)] py-6 px-4 md:px-8 mt-auto">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        
        {/* Footer Left */}
        <div className="text-center md:text-left space-y-1">
          <div className="flex items-center justify-center md:justify-start gap-2">
            <span className="font-bold text-white text-sm">ZAYVORA Health OS™</span>
            <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono text-[10px] border border-emerald-500/20">
              v1.0.0
            </span>
          </div>
          <p className="text-[11px] text-[var(--muted)]">
            © 2026 ZAYVORA Health. Modern Unani Care System.
          </p>
          <p className="text-[10px] text-[#64748B]">
            Codified Greco-Arab Wisdom + Level 4 Clinical AI Governance
          </p>
        </div>

        {/* Footer Center Links */}
        <div className="flex flex-wrap items-center justify-center gap-x-4 gap-y-2 text-[11px]">
          <Link href="/website/about" className="hover:text-white transition-colors">About ZAYVORA</Link>
          <span className="text-[#334155]">•</span>
          <Link href="/website/faqs" className="hover:text-white transition-colors">Help Center</Link>
          <span className="text-[#334155]">•</span>
          <Link href="/knowledge" className="hover:text-white transition-colors">Documentation</Link>
          <span className="text-[#334155]">•</span>
          <Link href="/website/contact" className="hover:text-white transition-colors">Contact Support</Link>
          <span className="text-[#334155]">•</span>
          <Link href="/website/privacy" className="hover:text-white transition-colors">Privacy Policy</Link>
          <span className="text-[#334155]">•</span>
          <Link href="/website/terms" className="hover:text-white transition-colors">Terms of Service</Link>
          <span className="text-[#334155]">•</span>
          <Link href="/admin" className="hover:text-white transition-colors">Data Protection</Link>
          <span className="text-[#334155]">•</span>
          <span className="text-emerald-400/80 font-semibold cursor-default">Accessibility (WCAG 2.1 AA)</span>
        </div>

        {/* Footer Right */}
        <div className="flex flex-col sm:flex-row items-center gap-4 text-[11px]">
          {/* System Status Pill */}
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-[var(--elevated)] border border-[var(--border)]">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="font-semibold text-emerald-400">System Status:</span>
            <span className="text-white">Operational</span>
          </div>

          {/* Language Selector */}
          <div className="flex items-center bg-[var(--background)] rounded-lg border border-[var(--border)] p-0.5">
            <button
              onClick={() => setLang("EN")}
              className={`px-2 py-0.5 rounded text-[10px] font-bold transition-colors ${
                lang === "EN" ? "bg-[var(--elevated)] text-[#2DD4BF]" : "text-[var(--muted)] hover:text-white"
              }`}
            >
              EN
            </button>
            <button
              onClick={() => setLang("HI")}
              className={`px-2 py-0.5 rounded text-[10px] font-bold transition-colors ${
                lang === "HI" ? "bg-[var(--elevated)] text-[#2DD4BF]" : "text-[var(--muted)] hover:text-white"
              }`}
            >
              हिन्दी
            </button>
            <button
              onClick={() => setLang("UR")}
              className={`px-2 py-0.5 rounded text-[10px] font-bold transition-colors ${
                lang === "UR" ? "bg-[var(--elevated)] text-[#2DD4BF]" : "text-[var(--muted)] hover:text-white"
              }`}
            >
              اردو
            </button>
          </div>

          {/* Dark Mode Toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            title="Toggle theme"
            className="p-1.5 rounded-lg bg-[var(--elevated)] border border-[var(--border)] text-sm hover:border-[var(--gold-soft)] transition-colors"
          >
            {darkMode ? "🌙" : "☀️"}
          </button>

          {/* Secure Platform Badge */}
          <span className="px-2.5 py-1 rounded-md bg-amber-500/10 border border-amber-500/30 text-amber-300 text-[10px] font-mono font-bold whitespace-nowrap">
            🔒 21 CFR Part 11
          </span>
        </div>

      </div>
    </footer>
  );
}
