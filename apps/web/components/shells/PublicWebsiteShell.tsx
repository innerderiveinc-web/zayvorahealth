"use client";

import React from "react";
import Link from "next/link";

export function PublicWebsiteShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col bg-[#0A0F1D] text-[#F8FAFC]">
      {/* Public Top Announcement */}
      <div className="bg-[#0D9488]/15 border-b border-[#0D9488]/30 px-4 py-2 text-center text-xs text-[#2DD4BF]">
        <span>✨ Ancient Wisdom. Modern Science. Intelligent Care. </span>
        <Link href="/website/book" className="underline font-bold hover:text-white ml-2">Book a Consult →</Link>
      </div>

      {/* Public Main Navigation Header */}
      <header className="bg-[#0F172A] border-b border-[#334155] px-6 py-4 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link href="/website" className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-[#0D9488] flex items-center justify-center font-bold text-white text-xl shadow-lg">
              Z
            </div>
            <div>
              <span className="font-bold tracking-tight text-white text-lg block">ZAYVORA Health™</span>
              <span className="text-[10px] text-[#2DD4BF] font-semibold tracking-wider block">MODERN UNANI CARE SYSTEM</span>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-6 text-xs font-semibold text-[#94A3B8]">
            <Link href="/website/philosophy" className="hover:text-white transition">Clinical Philosophy</Link>
            <Link href="/website/services" className="hover:text-white transition">Clinical Services</Link>
            <Link href="/website/conditions" className="hover:text-white transition">Conditions</Link>
            <Link href="/website/matab" className="hover:text-white transition">ZAYVORA Matab</Link>
            <Link href="/website/doctors" className="hover:text-white transition">Practitioners</Link>
            <Link href="/website/herbals" className="text-[#2DD4BF] hover:text-emerald-300 transition flex items-center gap-1">
              🌿 ZAYVORA Herbals
            </Link>
            <Link href="/website/research" className="hover:text-white transition">Research & Evidence</Link>
          </nav>

          <div className="flex items-center gap-3">
            <Link href="/doctor" className="px-3.5 py-1.5 rounded-lg border border-[#334155] text-xs font-semibold text-[#94A3B8] hover:text-white hover:bg-[#1E293B] transition">
              Health OS Login
            </Link>
            <Link href="/website/book" className="px-4 py-1.5 rounded-lg bg-[#0D9488] text-white text-xs font-bold hover:bg-[#14B8A6] shadow-md transition">
              Book Consultation
            </Link>
          </div>
        </div>
      </header>

      {/* Main Page Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Public Footer */}
      <footer className="bg-[#0F172A] border-t border-[#334155] py-12 px-6 text-xs text-[#94A3B8]">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-5 gap-8">
          <div className="md:col-span-2 space-y-3">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-[#0D9488] flex items-center justify-center font-bold text-white">
                Z
              </div>
              <span className="font-bold text-white text-base">ZAYVORA Health™</span>
            </div>
            <p className="text-[#64748B] max-w-sm leading-relaxed">
              ZAYVORA Health OS combines classical Unani Greco-Arab medical science with modern biomedical diagnostics, organ-axis clinical intelligence, and evidence-based personalized care.
            </p>
            <p className="text-[11px] text-[#475569]">
              © 2026 ZAYVORA Health Inc. All statutory clinical governance and 21 CFR Part 11 protocols enforced.
            </p>
          </div>

          <div className="space-y-2">
            <span className="font-bold text-white block uppercase tracking-wider text-[11px]">Clinical Services</span>
            <ul className="space-y-1.5">
              <li><Link href="/website/services" className="hover:text-white">Integrative OPD</Link></li>
              <li><Link href="/website/matab" className="hover:text-white">ZAYVORA Matab Clinics</Link></li>
              <li><Link href="/website/conditions" className="hover:text-white">Metabolic & Endocrine</Link></li>
              <li><Link href="/website/conditions" className="hover:text-white">Musculoskeletal (Mafasil)</Link></li>
              <li><Link href="/website/programs" className="hover:text-white">Preventive Hifz Programs</Link></li>
            </ul>
          </div>

          <div className="space-y-2">
            <span className="font-bold text-white block uppercase tracking-wider text-[11px]">Herbals & Store</span>
            <ul className="space-y-1.5">
              <li><Link href="/website/herbals" className="hover:text-white">Product Portfolio</Link></li>
              <li><Link href="/website/herbals?cat=fertility" className="hover:text-white">Fertility Formulations</Link></li>
              <li><Link href="/website/herbals?cat=metabolic" className="hover:text-white">Metabolic Support</Link></li>
              <li><Link href="/website/herbals?cat=liver" className="hover:text-white">Liver & Gut Axis</Link></li>
              <li><Link href="/website/cart" className="hover:text-white">My Cart & Orders</Link></li>
            </ul>
          </div>

          <div className="space-y-2">
            <span className="font-bold text-white block uppercase tracking-wider text-[11px]">Institutional & Legal</span>
            <ul className="space-y-1.5">
              <li><Link href="/website/about" className="hover:text-white">About ZAYVORA</Link></li>
              <li><Link href="/website/research" className="hover:text-white">Research & Evidence</Link></li>
              <li><Link href="/website/privacy" className="hover:text-white">Privacy Policy</Link></li>
              <li><Link href="/website/terms" className="hover:text-white">Terms of Care</Link></li>
              <li><Link href="/website/shipping-refunds" className="hover:text-white">Shipping & Refunds</Link></li>
            </ul>
          </div>
        </div>
      </footer>
    </div>
  );
}
