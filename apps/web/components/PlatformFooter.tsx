"use client";

import React, { useState } from "react";
import Link from "next/link";

export function PlatformFooter() {
  const [lang, setLang] = useState<"EN" | "HI" | "UR">("EN");
  const [darkMode, setDarkMode] = useState(true);
  const year = new Date().getFullYear();

  const links = {
    Platform: [
      { label: "About ZAYVORA", href: "/website/about" },
      { label: "ZAYVORA Matab™", href: "/website/matab" },
      { label: "Hakeem Sahab AI™", href: "/website/care-system" },
      { label: "Health Programs", href: "/website/programs" },
      { label: "Herbal Products", href: "/website/herbals" },
      { label: "Knowledge Centre", href: "/website/knowledge-centre" },
    ],
    "For Patients": [
      { label: "Book Consultation", href: "/website/book" },
      { label: "Find Doctors", href: "/website/doctors" },
      { label: "Teleconsultation", href: "/website/teleconsultation" },
      { label: "Our Clinics", href: "/website/clinics" },
      { label: "Conditions Treated", href: "/website/conditions" },
      { label: "Patient Login", href: "/patient/login" },
    ],
    "For Professionals": [
      { label: "Partner with Us", href: "/website/partner" },
      { label: "Research Academy", href: "/website/academy" },
      { label: "Careers", href: "/website/careers" },
      { label: "Blog", href: "/website/blog" },
      { label: "Contact", href: "/website/contact" },
    ],
    Legal: [
      { label: "Privacy Policy", href: "/website/privacy" },
      { label: "Terms of Service", href: "/website/terms" },
      { label: "Medical Disclaimer", href: "/website/medical-disclaimer" },
      { label: "Accessibility (WCAG 2.1 AA)", href: "/website/accessibility" },
      { label: "Refund Policy", href: "/website/refund-policy" },
    ],
  };

  return (
    <footer className="bg-[var(--bg-surface)] border-t border-[var(--border-default)] mt-auto text-xs text-[var(--text-muted)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {/* Brand & Main Grid */}
        <div className="flex flex-col lg:flex-row justify-between gap-8 mb-8">
          <div className="max-w-xs space-y-3">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#2D6A4F] to-[#1B4332] flex items-center justify-center text-white font-bold text-sm shadow-md">
                Z
              </div>
              <div>
                <span className="font-bold text-[var(--text-primary)] text-sm tracking-tight block">
                  ZAYVORA Health OS™
                </span>
                <span className="text-[10px] text-[#64748B]">
                  Codified Greco-Arab Wisdom · Level 4 Clinical AI Governance
                </span>
              </div>
            </div>
            <p className="text-[11px] text-[var(--text-muted)] leading-relaxed">
              Ancient Wisdom. Modern Science. Intelligent Care.
            </p>
            <p className="text-[10px] text-[#64748B] leading-relaxed">
              ZAYVORA Health OS™ is a pre-staging / pilot candidate system.
              All AI outputs enforce safe_to_lock=False requiring human clinician review.
            </p>

            {/* Badges */}
            <div className="flex flex-wrap gap-1.5 pt-1">
              <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono text-[10px] border border-emerald-500/20">
                🌿 Unani
              </span>
              <span className="px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 font-mono text-[10px] border border-blue-500/20">
                Evidence-Aware Care
              </span>
              <span className="px-2.5 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-[10px] font-mono font-bold">
                Electronic Signatures
              </span>
            </div>
          </div>

          {/* Link Columns */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 lg:gap-8">
            {Object.entries(links).map(([section, items]) => (
              <div key={section}>
                <h3 className="text-[11px] font-bold text-[var(--text-primary)] uppercase tracking-wider mb-2.5">
                  {section}
                </h3>
                <ul className="space-y-1.5">
                  {items.map((link) => (
                    <li key={link.href}>
                      <Link
                        href={link.href}
                        className="text-[11px] text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* Controls Bar: Language + Theme + Status */}
        <div className="border-t border-[var(--border-default)] pt-4 pb-4 flex flex-wrap items-center justify-between gap-4 text-[11px]">
          <div className="flex items-center gap-3">
            {/* System Status Pill */}
            <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-[var(--bg-elevated)] border border-[var(--border-default)]">
              <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
              <span className="font-semibold text-amber-400">Status:</span>
              <span className="text-[var(--text-primary)]">Pre-staging / Pilot Candidate</span>
            </div>

            <Link href="/admin/health" className="text-[var(--text-muted)] hover:text-white transition-colors">
              Engine Observability (25)
            </Link>
          </div>

          <div className="flex items-center gap-3">
            {/* Language Selector */}
            <div className="flex items-center bg-[var(--bg-base)] rounded-lg border border-[var(--border-default)] p-0.5">
              {(["EN", "HI", "UR"] as const).map((l) => (
                <button
                  key={l}
                  onClick={() => setLang(l)}
                  className={`px-2 py-0.5 rounded text-[10px] font-bold transition-colors ${
                    lang === l ? "bg-[var(--bg-elevated)] text-[#2DD4BF]" : "text-[var(--text-muted)] hover:text-white"
                  }`}
                >
                  {l === "EN" ? "EN" : l === "HI" ? "HI" : "UR"}
                </button>
              ))}
            </div>

            {/* Dark Mode Toggle */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              title="Toggle theme"
              aria-label="Toggle theme"
              className="p-1.5 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm hover:border-[var(--primary)] transition-colors"
            >
              {darkMode ? "🌙" : "☀️"}
            </button>
          </div>
        </div>

        {/* Legal & Trademark Statement */}
        <div className="border-t border-[var(--border-default)] pt-4 flex flex-col sm:flex-row items-center justify-between gap-2 text-[10px] text-[#64748B]">
          <p>
            © {year} ZAYVORA Health™. All rights reserved.
            ZAYVORA Health OS™, ZAYVORA Matab™, Hakeem Sahab AI™, ZAYVORA Knowledge Intelligence™,
            ZAYVORA Health Products™ and ZAYVORA Research & Manufacturing™ are registered trademarks.
          </p>
          <div className="flex items-center gap-2">
            <span>Schedule E(1) Mudabbar Verified</span>
            <span>·</span>
            <span>WCAG 2.1 AA</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
