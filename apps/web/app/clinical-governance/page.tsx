import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export const metadata = {
  title: "Clinical Governance & Statutory Oversight | ZAYVORA Health™",
  description: "Learn about ZAYVORA Health™ clinical governance: NCISM Act 2020 statutory standards, non-delegable physician oversight, AI safety boundaries, and 21 CFR Part 11 audit trails.",
};

export default function ClinicalGovernancePage() {
  const pillars = [
    {
      title: "100% Clinician-Governed Practice",
      desc: "Every clinical decision, Nuskha prescription, and therapeutic milestone is personally authored and signed by an NCISM-registered physician. No algorithm or non-clinical personnel can override physician discretion.",
      icon: "stethoscope"
    },
    {
      title: "Non-Delegable AI Decision Support",
      desc: "Artificial intelligence systems within ZAYVORA Health OS operate strictly as advisory clinical decision support (CDS). Automated prescribing, diagnosis without human clinician review, and black-box recommendations are strictly prohibited.",
      icon: "shield-check"
    },
    {
      title: "Schedule E(1) Mudabbar Gate",
      desc: "Formulations containing potent botanical or mineral calces are locked behind a mandatory Mudabbar detoxification certificate barrier. The pharmacy cannot dispense Schedule E(1) drugs without verified batch certificates.",
      icon: "pill"
    },
    {
      title: "21 CFR Part 11 Cryptographic Audits",
      desc: "All clinical notes, posology changes, and dispensations are anchored in a tamper-evident SHA-256 Merkle ledger with dual-factor clinician authentication, ensuring full statutory defensibility.",
      icon: "lock"
    }
  ];

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Quality & Patient Safety"
        title="Clinical Governance & Statutory Standards"
        subtitle="Our clinician-led framework ensures uncompromising patient safety, regulatory compliance under the NCISM Act 2020, and evidence-grounded therapeutic accountability."
        breadcrumbs={[{ label: "Clinical Governance" }]}
        primaryCta={{ label: "Meet Clinical Faculty", href: "/doctors" }}
        secondaryCta={{ label: "Contact Governance Board", href: "/contact" }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">
        
        {/* Core Pillars */}
        <section className="space-y-8">
          <div className="text-center max-w-2xl mx-auto space-y-2">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Four Invariant Pillars</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A]">Institutional Safety Architecture</h2>
            <p className="text-xs sm:text-sm text-slate-500">How ZAYVORA enforces medical safety at every layer of clinical encounter and pharmacy operation</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {pillars.map((p, idx) => (
              <div
                key={idx}
                className="bg-white rounded-3xl border border-slate-200/90 p-8 shadow-sm space-y-4"
              >
                <div className="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-800">
                  <HealthcareIcon name={p.icon} className="w-6 h-6 text-emerald-700" />
                </div>
                <h3 className="text-lg font-bold text-[#0F172A]">{p.title}</h3>
                <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">{p.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Regulatory Authorities */}
        <section className="bg-white rounded-3xl border border-slate-200/90 p-8 sm:p-10 shadow-sm space-y-6">
          <div className="border-b border-slate-100 pb-4">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Statutory Bodies</span>
            <h3 className="text-xl font-bold text-[#0F172A] mt-1">Regulatory Alignment & Clinical Credentials</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-600">
            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <span className="font-bold text-sm text-[#0F172A] block">NCISM Act 2020</span>
              <p className="leading-relaxed">National Commission for Indian System of Medicine governs the registration, ethical conduct, and clinical licensing of all practicing Tabeebs on the platform.</p>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <span className="font-bold text-sm text-[#0F172A] block">Drugs & Cosmetics Act 1940</span>
              <p className="leading-relaxed">All Unani pharmacopoeial preparations are manufactured in certified AYUSH-GMP cleanroom environments conforming to UPI and NFUM monograph specifications.</p>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <span className="font-bold text-sm text-[#0F172A] block">DPDP Act 2023</span>
              <p className="leading-relaxed">Digital Personal Data Protection Act safeguards every patient consultation, electronic medical record, and diagnostic imaging upload with end-to-end encryption.</p>
            </div>
          </div>
        </section>

      </div>
    </PublicWebsiteShell>
  );
}
