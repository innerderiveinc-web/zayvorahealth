"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export function PublicHeader() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchModalOpen, setSearchModalOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [lang, setLang] = useState<"EN" | "HI" | "UR">("EN");
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setSearchModalOpen(true);
      }
      if (e.key === "Escape") {
        setSearchModalOpen(false);
        setMobileMenuOpen(false);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const navLinks = [
    { label: "Home", href: "/website" },
    { label: "About", href: "/website/about" },
    { label: "Our Care System", href: "/website/care-journey" },
    { label: "Health Programs", href: "/website/programs" },
    { label: "Products", href: "/website/herbals" },
    { label: "Knowledge Center", href: "/website/knowledge-centre" },
    { label: "Clinical Team", href: "/website/doctors" },
    { label: "Contact", href: "/website/contact" },
  ];

  const searchIndex = [
    { title: "Metabolic Care & Endocrine Balance", sub: "12-16 Week Clinical Program", href: "/website/programs" },
    { title: "Male Fertility & Semen Health", sub: "74-Day Spermatogenesis Protocol", href: "/website/programs" },
    { title: "Female Hormonal Health & PCOS", sub: "Uterine Harmony & Ovary Wellness", href: "/website/programs" },
    { title: "ManiVital Pro (Withania & Mucuna)", sub: "Standardized Botanical Compound", href: "/website/product?id=manivital-pro" },
    { title: "OvaSync Botanical Complex", sub: "Women's Endocrine Formulation", href: "/website/product?id=ovasync" },
    { title: "Hakim Dr. Tariq Mansoor", sub: "Chief Medical Officer • CCIM-BUMS", href: "/website/doctors" },
    { title: "Understanding Mizaj (Temperament)", sub: "Clinical Knowledge Article", href: "/website/knowledge-centre" },
  ];

  const filteredResults = searchQuery.trim() === ""
    ? searchIndex.slice(0, 5)
    : searchIndex.filter(item =>
        item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.sub.toLowerCase().includes(searchQuery.toLowerCase())
      );

  return (
    <>
      {/* Top Clinical Announcement Bar */}
      <div className="bg-[#0D5C46] text-[#E6F4EA] px-4 py-2 text-xs font-medium text-center border-b border-[#0F766E]/40">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
          <span className="hidden sm:inline">🏥 Jamia Hamdard AUTC - Main Hospital • Integrative Clinical Facility</span>
          <div className="mx-auto sm:mx-0 flex items-center gap-3">
            <span className="text-white font-semibold">Care Helpline: +91 11 2605 9688</span>
            <span className="text-[#A7F3D0]">•</span>
            <Link href="/website/book" className="underline font-bold text-white hover:text-[#99F6E4] transition">
              Book a Consultation →
            </Link>
          </div>
        </div>
      </div>

      {/* Main Sticky Header */}
      <header
        className={`sticky top-0 z-40 transition-all duration-200 border-b ${
          isScrolled
            ? "bg-[#0A0F1D]/95 backdrop-blur-md border-[#334155] shadow-lg py-3"
            : "bg-[#0A0F1D] border-[#1E293B] py-4"
        }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 flex items-center justify-between gap-4">
          
          {/* Brand Logo & Name */}
          <Link href="/website" className="flex items-center gap-3 group shrink-0">
            <div className="w-10 h-10 rounded-xl bg-white/5 border border-[#334155] flex items-center justify-center p-1 shadow-sm group-hover:border-[#0D9488] transition overflow-hidden">
              <img
                src="/zayvora-logo.png"
                alt="ZAYVORA Health Logo"
                className="w-full h-full object-contain"
                onError={(e) => {
                  (e.target as HTMLElement).style.display = "none";
                }}
              />
            </div>
            <div>
              <span className="font-extrabold text-white text-lg tracking-tight block leading-tight">
                ZAYVORA <span className="text-[#0D9488] font-semibold text-base">Health</span>
              </span>
              <span className="text-[10px] text-[#94A3B8] font-medium tracking-wider block uppercase">
                Modern Unani Care System
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden xl:flex items-center gap-6 text-xs font-semibold text-[#94A3B8]">
            {navLinks.map((link) => {
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`transition hover:text-white py-1 relative ${
                    isActive ? "text-[#2DD4BF] font-bold" : ""
                  }`}
                >
                  {link.label}
                  {isActive && (
                    <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#0D9488] rounded-full" />
                  )}
                </Link>
              );
            })}
          </nav>

          {/* Right Header Actions */}
          <div className="flex items-center gap-2.5 sm:gap-3">
            
            {/* Search Trigger */}
            <button
              onClick={() => setSearchModalOpen(true)}
              className="px-3 py-1.5 rounded-xl bg-[#0F172A] border border-[#334155] text-xs text-[#94A3B8] hover:text-white hover:border-[#0D9488] flex items-center gap-2 transition focus:outline-none focus:ring-2 focus:ring-[#0D9488]"
              title="Search website (Cmd+K)"
            >
              <span>🔍</span>
              <span className="hidden md:inline">Search...</span>
              <kbd className="hidden lg:inline-block px-1.5 py-0.5 rounded bg-[#1E293B] border border-[#334155] text-[10px] font-mono text-[#64748B]">
                ⌘K
              </kbd>
            </button>

            {/* Language Switcher */}
            <div className="hidden sm:flex items-center bg-[#0F172A] rounded-xl border border-[#334155] p-0.5 text-[10px] font-bold">
              {(["EN", "HI", "UR"] as const).map((l) => (
                <button
                  key={l}
                  onClick={() => setLang(l)}
                  className={`px-2 py-1 rounded-lg transition ${
                    lang === l
                      ? "bg-[#0D9488] text-white shadow-xs"
                      : "text-[#94A3B8] hover:text-white"
                  }`}
                >
                  {l}
                </button>
              ))}
            </div>

            {/* Patient Portal Login */}
            <Link
              href="/patient/login"
              className="hidden sm:inline-flex px-3.5 py-2 rounded-xl border border-[#334155] text-xs font-semibold text-[#CBD5E1] hover:text-white hover:bg-[#1E293B] transition"
            >
              Patient Login
            </Link>

            {/* Primary Action: Book Consultation */}
            <Link
              href="/website/book"
              className="px-4 py-2 rounded-xl bg-[#0D9488] text-white text-xs font-bold hover:bg-[#0F766E] shadow-md transition focus:outline-none focus:ring-2 focus:ring-[#0D9488] focus:ring-offset-2 focus:ring-offset-[#0A0F1D]"
            >
              Book Consultation
            </Link>

            {/* Mobile Hamburger Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="xl:hidden p-2 rounded-xl bg-[#0F172A] border border-[#334155] text-white hover:border-[#0D9488] transition"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? "✕" : "☰"}
            </button>

          </div>

        </div>

        {/* Mobile Navigation Drawer */}
        {mobileMenuOpen && (
          <div className="xl:hidden fixed inset-0 top-[110px] z-50 bg-[#0A0F1D]/95 backdrop-blur-xl border-t border-[#334155] p-6 overflow-y-auto space-y-6 animate-fade-in">
            <div className="space-y-2">
              <span className="text-[10px] font-bold text-[#64748B] uppercase tracking-wider block">Menu</span>
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className="block px-4 py-3 rounded-xl hover:bg-[#1E293B] text-sm font-semibold text-white transition border border-transparent hover:border-[#334155]"
                >
                  {link.label}
                </Link>
              ))}
            </div>

            <div className="pt-4 border-t border-[#334155] space-y-3">
              <span className="text-[10px] font-bold text-[#64748B] uppercase tracking-wider block">Patient Access</span>
              <div className="grid grid-cols-2 gap-3">
                <Link
                  href="/patient/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-full text-center px-4 py-3 rounded-xl border border-[#334155] text-xs font-bold text-white bg-[#0F172A]"
                >
                  Patient Login
                </Link>
                <Link
                  href="/patient/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-full text-center px-4 py-3 rounded-xl bg-[#0D9488]/20 border border-[#0D9488]/40 text-xs font-bold text-[#2DD4BF]"
                >
                  Register
                </Link>
              </div>
              <Link
                href="/website/book"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full block text-center px-4 py-3 rounded-xl bg-[#0D9488] text-white text-sm font-bold shadow-md"
              >
                Book a Consultation
              </Link>
            </div>

            <div className="pt-4 border-t border-[#334155] flex items-center justify-between text-xs text-[#94A3B8]">
              <span>Language:</span>
              <div className="flex gap-1">
                {(["EN", "HI", "UR"] as const).map((l) => (
                  <button
                    key={l}
                    onClick={() => setLang(l)}
                    className={`px-3 py-1 rounded-lg text-xs font-bold ${
                      lang === l ? "bg-[#0D9488] text-white" : "bg-[#1E293B] text-[#94A3B8]"
                    }`}
                  >
                    {l}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </header>

      {/* Global Search Modal */}
      {searchModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-start justify-center pt-24 p-4">
          <div className="bg-[#0F172A] border border-[#334155] rounded-3xl max-w-xl w-full p-5 space-y-4 shadow-2xl animate-scale-up">
            <div className="flex items-center gap-3 border-b border-[#334155] pb-3">
              <span className="text-lg">🔍</span>
              <input
                autoFocus
                placeholder="Search programs, formulations, doctors, health articles..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-transparent text-sm text-white focus:outline-none placeholder-[#64748B]"
              />
              <button
                onClick={() => setSearchModalOpen(false)}
                className="text-xs text-[#94A3B8] hover:text-white px-2 py-1 rounded bg-[#1E293B]"
              >
                ESC
              </button>
            </div>

            <div className="space-y-2 max-h-72 overflow-y-auto">
              <span className="text-[10px] font-bold text-[#64748B] uppercase px-1">
                Search Results ({filteredResults.length})
              </span>
              {filteredResults.map((item, idx) => (
                <Link
                  key={idx}
                  href={item.href}
                  onClick={() => setSearchModalOpen(false)}
                  className="p-3 rounded-2xl hover:bg-[#1E293B] border border-transparent hover:border-[#334155] flex items-center justify-between text-xs transition block"
                >
                  <div>
                    <h5 className="font-bold text-white text-sm">{item.title}</h5>
                    <p className="text-[11px] text-[#94A3B8]">{item.sub}</p>
                  </div>
                  <span className="text-[#0D9488] font-bold">Open →</span>
                </Link>
              ))}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
