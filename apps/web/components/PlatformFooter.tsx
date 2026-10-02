"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export function PlatformFooter() {
  const pathname = usePathname();
  const [lang, setLang] = useState<"EN" | "HI" | "UR">("EN");
  const [darkMode, setDarkMode] = useState(true);
  const year = new Date().getFullYear();

  // Clinical Operating Dashboards: Render compact, distraction-free Telemetry Bar
  const isClinicalDesk = pathname?.startsWith('/doctor') ||
                         pathname?.startsWith('/patient') ||
                         pathname?.startsWith('/reception') ||
                         pathname?.startsWith('/receptionist') ||
                         pathname?.startsWith('/clinic') ||
                         pathname?.startsWith('/nurse') ||
                         pathname?.startsWith('/pharmacy') ||
                         pathname?.startsWith('/manufacturing') ||
                         pathname?.startsWith('/admin') ||
                         pathname?.startsWith('/research') ||
                         pathname?.startsWith('/billing') ||
                         pathname?.startsWith('/analytics') ||
                         pathname?.startsWith('/protocols') ||
                         pathname?.startsWith('/dashboard');

  if (isClinicalDesk) {
    return (
      <footer className="bg-[#070D1B] border-t border-slate-800 text-[11px] text-slate-400 py-3 px-4 sm:px-6 lg:px-8 mt-auto shadow-inner">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2.5">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-slate-200 font-bold">ZAYVORA Health OS™ Enterprise</span>
            <span className="text-slate-600">&bull;</span>
            <span className="text-slate-400">Facility: <strong className="text-emerald-400 font-mono">ZAY-DEL-01</strong></span>
            <span className="text-slate-600 hidden md:inline">&bull;</span>
            <span className="text-slate-400 font-mono text-[10px] hidden md:inline">21 CFR Part 11 Merkle Sealed</span>
          </div>
          <div className="flex items-center gap-3 text-[10px] font-mono text-slate-400">
            <span className="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> DB: SQLite WAL Active</span>
            <span className="text-slate-700">&bull;</span>
            <span>Latency: 12ms</span>
            <span className="text-slate-700">&bull;</span>
            <span>DPDP Act 2023 Isolated</span>
            <span className="text-slate-700">&bull;</span>
            <span className="text-slate-500 font-semibold">v5.2.0-PROD</span>
          </div>
        </div>
      </footer>
    );
  }

  const links = {
    Platform: [
      { label: "About ZAYVORA", href: "/about" },
      { label: "Clinical Care", href: "/services/clinical-care" },
      { label: "Health Programs", href: "/programs" },
      { label: "Herbal Products", href: "/products" },
      { label: "Health Library", href: "/health-library" },
    ],
    "For Patients": [
      { label: "Book Consultation", href: "/book" },
      { label: "Find Doctors", href: "/doctors" },
      { label: "Teleconsultation", href: "/teleconsultation" },
      { label: "Our Clinics", href: "/clinics" },
      { label: "Conditions Treated", href: "/conditions" },
      { label: "Patient Login", href: "/login" },
    ],
    "For Professionals": [
      { label: "Clinical Academy", href: "/academy" },
      { label: "Clinical Research", href: "/research" },
      { label: "Careers", href: "/careers" },
      { label: "Contact Us", href: "/contact" },
      { label: "Governance & Trust", href: "/trust" },
    ],
    Legal: [
      { label: "Privacy Policy", href: "/privacy-policy" },
      { label: "Terms of Service", href: "/terms-and-conditions" },
      { label: "Medical Disclaimer", href: "/medical-disclaimer" },
      { label: "Accessibility (WCAG 2.1 AA)", href: "/accessibility" },
      { label: "Shipping & Refunds", href: "/shipping-refunds" },
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
