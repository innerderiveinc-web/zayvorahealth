import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export const metadata = {
  title: "ZAYVORA Clinical Academy™ | Post-Graduate Fellowships & CME",
  description: "Advanced clinical fellowship curricula, continuing medical education, and clinical decision support practicums for NCISM-registered Unani clinicians.",
};

export default function AcademyPage() {
  const programs = [
    {
      code: "CP-AFUM",
      title: "Certified Practitioner in Applied Foundations of Unani Medicine",
      duration: "24 Weeks (96 Hours + 20 Supervised Clinical Cases)",
      credentials: "Open to BUMS / MD (Unani) Graduates & Statutory Registrants",
      desc: "An intensive fellowship bridging classical 10-Ajnas pulse evaluation, organ-axis systems biology, and contemporary functional pathology.",
      href: "/academy/cp-afum"
    },
    {
      code: "AFUF",
      title: "Advanced Fellowship in Unani Formulations & Cleanroom QA",
      duration: "16 Weeks (Applied Pharmacognosy & HPLC Benchwork)",
      credentials: "Post-Graduate Pharmacologists & Clinical Tabeebs",
      desc: "Specialized training in Schedule E(1) Mudabbar detoxification, analytical validation, batch manufacturing records (eBMR), and 21 CFR Part 11 audit trails.",
      href: "/academy/cp-afum"
    },
    {
      code: "CME-TADBEER",
      title: "Clinical Masterclass in Regimenal Therapy (Ilaj bil-Tadbeer)",
      duration: "8 Weeks (Sterile Procedural Certification)",
      credentials: "Registered Tabeebs & Integrative Physical Therapists",
      desc: "Hands-on certification in sterile Hijama (cupping), specialized Dalk (medical friction), Abzen (pelvic hydrotherapy), and therapeutic thermal regimes.",
      href: "/academy/cp-afum"
    }
  ];

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Post-Graduate Medical Education"
        title="ZAYVORA Clinical Academy™"
        subtitle="Elevating the global standard of Greco-Arab Unani medicine through rigorous postgraduate curriculum, clinical decision support practicums, and evidence-grounded fellowships."
        breadcrumbs={[{ label: "Clinical Academy" }]}
        primaryCta={{ label: "View CP-AFUM Curriculum", href: "/academy/cp-afum" }}
        secondaryCta={{ label: "Admissions Inquiry", href: "/contact?type=academy" }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">
        
        {/* Core Fellowship Overview */}
        <section className="space-y-8">
          <div className="text-center max-w-2xl mx-auto space-y-2">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Accredited Fellowships</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A]">Post-Graduate Clinical Curricula</h2>
            <p className="text-xs sm:text-sm text-slate-500">Designed for licensed clinicians seeking mastery in evidence-correlated Unani healthcare</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {programs.map((prog, idx) => (
              <div
                key={idx}
                className="bg-white rounded-3xl border border-slate-200/90 p-7 shadow-sm hover:shadow-md hover:border-emerald-600/40 transition flex flex-col justify-between space-y-6"
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="px-3 py-1 rounded-full bg-emerald-50 text-[#1B4332] border border-emerald-200 font-mono font-bold text-xs">
                      {prog.code}
                    </span>
                    <span className="text-[11px] text-slate-400 font-medium">{prog.duration}</span>
                  </div>

                  <h3 className="text-lg font-bold text-[#0F172A] leading-snug">{prog.title}</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">{prog.desc}</p>

                  <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/70 text-xs">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Eligibility:</span>
                    <p className="text-slate-700 text-[11px]">{prog.credentials}</p>
                  </div>
                </div>

                <div className="pt-4 border-t border-slate-100 flex items-center justify-between gap-3">
                  <Link
                    href={prog.href}
                    className="w-full text-center py-2.5 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white text-xs font-bold shadow-sm transition"
                  >
                    Examine Curriculum Modules
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Clinical Practicum & Scribe Standards */}
        <section className="bg-white rounded-3xl border border-slate-200/90 p-8 sm:p-10 shadow-sm space-y-6">
          <div className="border-b border-slate-100 pb-4">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Practicum Environment</span>
            <h3 className="text-xl font-bold text-[#0F172A] mt-1">Supervised Real-World Clinical Decision Support (CDS)</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-600">
            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <div className="flex items-center gap-2 text-emerald-800">
                <HealthcareIcon name="academic" className="w-5 h-5 text-emerald-700" />
                <span className="font-bold text-sm text-[#0F172A]">20 Supervised Case Audits</span>
              </div>
              <p className="leading-relaxed">Fellows manage 20 longitudinal clinical cases under direct senior consultant Tabeeb supervision with mandatory EMR documentation.</p>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <div className="flex items-center gap-2 text-teal-800">
                <HealthcareIcon name="shield-check" className="w-5 h-5 text-teal-700" />
                <span className="font-bold text-sm text-[#0F172A]">Red-Flag Referral Triage</span>
              </div>
              <p className="leading-relaxed">Rigorous training in emergency boundaries, drug-herb interactions, and acute biomedical referral criteria.</p>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <div className="flex items-center gap-2 text-amber-800">
                <HealthcareIcon name="clipboard" className="w-5 h-5 text-amber-700" />
                <span className="font-bold text-sm text-[#0F172A]">Viva Voce & Board Exam</span>
              </div>
              <p className="leading-relaxed">Candidates complete a comprehensive oral case defense before statutory external examiners prior to fellowship conferral.</p>
            </div>
          </div>
        </section>

      </div>
    </PublicWebsiteShell>
  );
}
