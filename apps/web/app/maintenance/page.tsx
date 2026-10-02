"use client";

import React from "react";
import Link from "next/link";

export default function MaintenancePage() {
  return (
    <div className="min-h-screen bg-[#070D18] flex flex-col justify-center items-center px-4 py-16 text-slate-100 text-center relative overflow-hidden">
      <div className="relative z-10 max-w-lg mx-auto space-y-6">
        <div className="w-20 h-20 mx-auto rounded-3xl bg-slate-900 border border-teal-500/40 flex items-center justify-center text-3xl shadow-xl">
          ⚙️
        </div>

        <div className="space-y-2">
          <span className="text-xs font-mono font-bold text-teal-400 tracking-widest uppercase bg-teal-950 px-3 py-1 rounded-full border border-teal-800">
            Scheduled Maintenance
          </span>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            System Upgrading
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
            ZAYVORA Health OS is undergoing routine clinical registry and database synchronization. Full services will resume shortly.
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 space-y-1">
          <div>Estimated Time to Service: <strong>15 Minutes</strong></div>
          <div className="text-slate-400">Emergency OPD Desk remains active: +91 97738 82657</div>
        </div>

        <div className="pt-4">
          <Link
            href="/website"
            className="inline-block px-6 py-3 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shadow-lg transition"
          >
            Check Platform Status →
          </Link>
        </div>
      </div>
    </div>
  );
}
