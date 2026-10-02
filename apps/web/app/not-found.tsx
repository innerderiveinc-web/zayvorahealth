"use client";

import React from "react";
import Link from "next/link";
import { siteConfig } from "@/lib/data/siteConfig";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-[#070D18] flex flex-col justify-center items-center px-4 py-16 text-slate-100 text-center relative overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-[#0D9488]/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10 max-w-lg mx-auto space-y-6">
        <div className="w-20 h-20 mx-auto rounded-3xl bg-[#0D1527] border border-[#1E293B] flex items-center justify-center text-3xl shadow-xl">
          🔍
        </div>

        <div className="space-y-2">
          <span className="text-xs font-mono font-bold text-[#5EEAD4] tracking-widest uppercase">
            Error 404 • Resource Not Located
          </span>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Page Not Found
          </h1>
          <p className="text-xs sm:text-sm text-[#94A3B8] leading-relaxed">
            The clinical service, product monograph, or resource you are looking for does not exist or has been moved to a new route.
          </p>
        </div>

        <div className="flex flex-wrap justify-center gap-3 pt-2">
          <Link
            href="/"
            className="px-6 py-3 rounded-xl bg-[#0D9488] hover:bg-[#0F766E] text-white font-bold text-xs shadow-lg transition"
          >
            Return to Homepage →
          </Link>
          <Link
            href="/services"
            className="px-6 py-3 rounded-xl bg-[#1E293B] hover:bg-[#334155] text-[#CBD5E1] font-semibold text-xs border border-[#334155] transition"
          >
            Explore Services
          </Link>
          <Link
            href="/contact"
            className="px-6 py-3 rounded-xl bg-[#1E293B] hover:bg-[#334155] text-[#CBD5E1] font-semibold text-xs border border-[#334155] transition"
          >
            Contact Care Desk
          </Link>
        </div>

        <div className="pt-8 border-t border-[#1E293B] text-[11px] text-[#64748B]">
          Need clinical assistance? Call our care helpline: <strong className="text-[#CBD5E1]">{siteConfig.contact.helpline}</strong>
        </div>
      </div>
    </div>
  );
}
