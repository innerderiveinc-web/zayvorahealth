"use client";

import React from "react";
import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-[#070D18] flex flex-col justify-center items-center px-4 py-16 text-slate-100 text-center relative overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-teal-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="relative z-10 max-w-lg mx-auto space-y-6">
        <div className="w-20 h-20 mx-auto rounded-3xl bg-slate-900 border border-slate-800 flex items-center justify-center text-3xl shadow-xl">
          🔍
        </div>

        <div className="space-y-2">
          <span className="text-xs font-mono font-bold text-teal-400 tracking-widest uppercase">
            Error 404 • Resource Not Found
          </span>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Clinical Page Not Located
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
            The medical page, monograph, or patient resource you are searching for might have been moved, updated, or does not exist.
          </p>
        </div>

        <div className="flex flex-wrap justify-center gap-3 pt-2">
          <Link
            href="/website"
            className="px-6 py-3 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shadow-lg shadow-teal-900/30 transition"
          >
            Return to Homepage →
          </Link>
          <Link
            href="/website/book"
            className="px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs border border-slate-700 transition"
          >
            Book Consultation
          </Link>
          <Link
            href="/patient"
            className="px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs border border-slate-700 transition"
          >
            Patient Portal
          </Link>
        </div>

        <div className="pt-8 border-t border-slate-800/80 text-[11px] text-slate-500">
          Need clinical assistance? Call our hospital helpline: <strong className="text-slate-400">+91 11 2605 9000</strong>
        </div>
      </div>
    </div>
  );
}
