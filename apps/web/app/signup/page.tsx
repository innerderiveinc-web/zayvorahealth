"use client";

import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";

export default function SignupHubPage() {
  const pathways = [
    {
      title: "Patient Health Account",
      subtitle: "My ZAYVORA™ Personal Health Record",
      icon: "🌿",
      description:
        "Create your individual health record, access active Unani prescriptions, track regimenal therapy (Tadbeer), and book clinical consultations.",
      actionLabel: "Create Patient Account →",
      href: "/patient/register",
      badge: "Instant ABDM Access",
      badgeColor: "bg-teal-950 text-teal-300 border-teal-800"
    },
    {
      title: "Unani Clinician / Tabeeb",
      subtitle: "NCISM Credentialing & Prescribing Privileges",
      icon: "🩺",
      description:
        "8-step statutory credential verification for BUMS / MD Unani practitioners. Grants access to Clinical Thread™, Hakeem Sahab AI copilot, and 21 CFR Part 11 digital prescribing.",
      actionLabel: "Apply for Clinician Credential →",
      href: "/clinician/apply",
      badge: "Statutory NCISM Review",
      badgeColor: "bg-emerald-950 text-emerald-300 border-emerald-800"
    },
    {
      title: "Hospital, Matab or Clinic",
      subtitle: "Enterprise Healthcare OS Tenancy",
      icon: "🏥",
      description:
        "Onboard your healthcare institution. Multi-room OPD queue management, dispensary FEFO inventory, cold-chain monitoring, and multi-facility compliance.",
      actionLabel: "Institutional Partnership Application →",
      href: "/organization/apply",
      badge: "Enterprise Tenancy",
      badgeColor: "bg-indigo-950 text-indigo-300 border-indigo-800"
    }
  ];

  return (
    <PublicWebsiteShell>
      <div className="min-h-[85vh] py-16 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto flex flex-col justify-center">
        <div className="text-center mb-12 space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-teal-400 text-xs font-mono">
            <span>🛡️ Unified Identity & Onboarding</span>
            <span>•</span>
            <span>Zero Unvetted Clinical Access</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Welcome to ZAYVORA Health OS™
          </h1>
          <p className="text-sm text-slate-400 max-w-xl mx-auto">
            Select your registration pathway. In accordance with Indian digital health governance and the NCISM Act 2020, professional clinical privileges require verified statutory review.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {pathways.map((p, i) => (
            <div
              key={i}
              className="rounded-3xl bg-[#0D1527] border border-slate-800 p-6 flex flex-col justify-between hover:border-teal-500/50 transition duration-200 shadow-xl group"
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-700/60 flex items-center justify-center text-2xl group-hover:scale-105 transition">
                    {p.icon}
                  </div>
                  <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-medium border ${p.badgeColor}`}>
                    {p.badge}
                  </span>
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white group-hover:text-teal-400 transition">
                    {p.title}
                  </h3>
                  <p className="text-xs text-teal-400/80 font-mono mt-0.5">
                    {p.subtitle}
                  </p>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  {p.description}
                </p>
              </div>

              <div className="pt-6">
                <Link
                  href={p.href}
                  className="w-full py-2.5 px-4 rounded-xl bg-slate-900 hover:bg-teal-600 text-teal-300 hover:text-white border border-slate-700 hover:border-teal-500 text-xs font-bold text-center block transition duration-200 shadow-sm"
                >
                  {p.actionLabel}
                </Link>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 text-center text-xs text-slate-400 space-y-2">
          <p>
            Already have an active account or institutional login?{" "}
            <Link href="/login" className="text-teal-400 font-bold hover:underline">
              Sign In to ZAYVORA Health OS™ →
            </Link>
          </p>
          <div className="flex items-center justify-center gap-4 text-[11px] text-slate-500 pt-2">
            <Link href="/patient/login" className="hover:text-slate-300">My ZAYVORA™ (Patient Portal)</Link>
            <span>•</span>
            <Link href="/doctor/login" className="hover:text-slate-300">Clinician OPD Desk</Link>
            <span>•</span>
            <Link href="/medical-disclaimer" className="hover:text-slate-300">Statutory Notice</Link>
          </div>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}
