"use client";

import React from "react";
import Link from "next/link";
import { INSTITUTIONAL_FOOTER_NAVIGATION } from "@/lib/cms/website/navigationData";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { siteConfig } from "@/lib/data/siteConfig";

export function PublicFooter() {
  return (
    <footer className="bg-[#11231B] text-[#D8F3DC] border-t border-[#1B4332] text-xs">
      {/* Emergency Advisory Callout Ribbon */}
      <div className="bg-[#1B4332] border-b border-[#2D6A4F] py-3 px-4">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2 text-center sm:text-left text-xs text-[#E8F5E9]">
          <div className="flex items-center gap-2">
            <HealthcareIcon name="alert" className="w-4 h-4 text-[#FBBF24] shrink-0" />
            <span>
              <strong>Emergency Medical Advisory:</strong> In the event of severe chest pain, acute dyspnea, or signs of stroke, immediately dial <strong className="text-white underline">112 (National Emergency)</strong>.
            </span>
          </div>
          <Link href="/teleconsultation" className="text-[#A7F3D0] hover:text-white font-semibold underline shrink-0">
            Emergency Guidelines →
          </Link>
        </div>
      </div>

      {/* Main Footer Navigation Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-14">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
          
          {/* Column 1: Organization */}
          <div className="col-span-2 md:col-span-3 lg:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-white/10 border border-white/20 flex items-center justify-center p-1.5">
                <img
                  src={siteConfig.logo}
                  alt={siteConfig.name}
                  className="w-full h-full object-contain"
                  onError={(e) => { (e.target as HTMLElement).style.display = "none"; }}
                />
              </div>
              <span className="font-extrabold text-white text-base tracking-tight">ZAYVORA Health™</span>
            </div>
            <p className="text-xs text-[#95D5B2] leading-relaxed max-w-sm">
              Clinician-led integrative Unani healthcare platform combining classical humoral assessment, individualized Nuskha formulations, contemporary biomedical scrutiny, and longitudinal patient follow-up.
            </p>
            <div className="space-y-1 text-[11px] text-[#74C69D] pt-2">
              <p>Registered Clinical Facility: <span className="text-white font-medium">{siteConfig.address.facility}</span></p>
              <p>Helpline: <strong className="text-white">{siteConfig.contact.helpline}</strong></p>
              <p>Email: <span className="text-white">{siteConfig.contact.email}</span></p>
            </div>
          </div>

          {/* Column 2: Clinical Care */}
          <div className="space-y-3">
            <h4 className="font-bold text-white uppercase tracking-wider text-[11px]">
              Clinical Care
            </h4>
            <ul className="space-y-2 text-xs">
              {INSTITUTIONAL_FOOTER_NAVIGATION.care.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="text-[#95D5B2] hover:text-white transition">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 3: Health Resources */}
          <div className="space-y-3">
            <h4 className="font-bold text-white uppercase tracking-wider text-[11px]">
              Health & Products
            </h4>
            <ul className="space-y-2 text-xs">
              {INSTITUTIONAL_FOOTER_NAVIGATION.health.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="text-[#95D5B2] hover:text-white transition">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 4: Evidence & Research */}
          <div className="space-y-3">
            <h4 className="font-bold text-white uppercase tracking-wider text-[11px]">
              Evidence & Academy
            </h4>
            <ul className="space-y-2 text-xs">
              {INSTITUTIONAL_FOOTER_NAVIGATION.research.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="text-[#95D5B2] hover:text-white transition">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 5: Patient Rights & Legal */}
          <div className="space-y-3">
            <h4 className="font-bold text-white uppercase tracking-wider text-[11px]">
              Patient Rights & Legal
            </h4>
            <ul className="space-y-2 text-xs">
              {INSTITUTIONAL_FOOTER_NAVIGATION.patientInfo.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="text-[#95D5B2] hover:text-white transition">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

        </div>
      </div>

      {/* Statutory Disclaimers & Copyright Sub-Footer */}
      <div className="border-t border-[#1B4332] bg-[#0B1711] py-6 px-4">
        <div className="max-w-7xl mx-auto space-y-4">
          <p className="text-[11px] text-[#74C69D] leading-relaxed">
            <strong className="text-white font-semibold">Statutory Governance Disclosure:</strong> ZAYVORA Health™ operates in strict compliance with the National Commission for Indian System of Medicine (NCISM) Act, 2020 and the Digital Personal Data Protection (DPDP) Act, 2023. Consultation assessments, individualized prescriptions (Nuskha), and treatment approvals are conducted exclusively by verified, licensed practitioners. Hakeem Sahab AI™ functions solely as a clinician decision-support system and does not independently prescribe or diagnose.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] text-[#52B788] pt-2 border-t border-[#1B4332]/60">
            <div>
              © 2026 ZAYVORA Health Systems Private Limited. All rights reserved.
            </div>
            <div className="flex items-center gap-4">
              <Link href="/accessibility" className="hover:text-white transition">WCAG 2.2 AA Accessibility</Link>
              <span>•</span>
              <Link href="/privacy-policy" className="hover:text-white transition">DPDP 2023 Compliant</Link>
              <span>•</span>
              <Link href="/medical-disclaimer" className="hover:text-white transition">NCISM Framework</Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
