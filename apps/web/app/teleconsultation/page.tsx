import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export const metadata = {
  title: "Encrypted Virtual Care & Teleconsultation | ZAYVORA Health™",
  description: "End-to-end encrypted telehealth consultations with statutory NCISM-registered Unani clinicians and senior Tabeebs under DPDP Act 2023 standards.",
};

export default function TeleconsultationPage() {
  const steps = [
    {
      num: "01",
      title: "Comprehensive Digital Intake",
      desc: "Complete your structured health history, dietary patterns, sleep timing, and upload any recent pathology reports securely.",
      icon: "clipboard"
    },
    {
      num: "02",
      title: "1-on-1 Encrypted Video Consult",
      desc: "30-minute clinical session with an NCISM-registered consultant Tabeeb for constitutional temperament assessment (Mizaj) and symptom mapping.",
      icon: "video"
    },
    {
      num: "03",
      title: "Digital Nuskha & Clinical Twin",
      desc: "Receive a personalized electronic prescription anchored with a 21 CFR Part 11 digital cryptographic seal, dietary directives, and anupan guidelines.",
      icon: "file-text"
    },
    {
      num: "04",
      title: "Cleanroom Dispensary Delivery",
      desc: "Standardized herbal formulations dispatched under validated FEFO batch tracking directly from our GMP facility to your residence.",
      icon: "hospital"
    }
  ];

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Encrypted Virtual Health OS"
        title="Institutional Teleconsultation & Virtual Care"
        subtitle="Consult senior consultant Tabeebs from the privacy of your home through secure WebRTC video, compliant with DPDP Act 2023 and the Telemedicine Practice Guidelines of India."
        breadcrumbs={[{ label: "Virtual Consultation" }]}
        primaryCta={{ label: "Book Virtual Appointment", href: "/contact?type=teleconsult" }}
        secondaryCta={{ label: "Meet Clinical Faculty", href: "/doctors" }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">
        
        {/* Step-by-Step Care Flow */}
        <section className="space-y-8">
          <div className="text-center max-w-2xl mx-auto space-y-2">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Seamless Continuity</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A]">How Virtual Clinical Care Works</h2>
            <p className="text-xs sm:text-sm text-slate-500">From digital intake to cleanroom formulation delivery at your doorstep</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {steps.map((s, idx) => (
              <div
                key={idx}
                className="bg-white rounded-3xl border border-slate-200/90 p-6 shadow-sm flex flex-col justify-between space-y-4"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xl font-mono font-extrabold text-emerald-800">{s.num}</span>
                    <div className="w-10 h-10 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-800">
                      <HealthcareIcon name={s.icon} className="w-5 h-5 text-emerald-700" />
                    </div>
                  </div>
                  <h3 className="font-bold text-[#0F172A] text-sm leading-snug">{s.title}</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">{s.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Security & Privacy Standards */}
        <section className="bg-white rounded-3xl border border-slate-200/90 p-8 sm:p-10 shadow-sm space-y-6">
          <div className="border-b border-slate-100 pb-4">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Statutory Privacy Firewalls</span>
            <h3 className="text-xl font-bold text-[#0F172A] mt-1">DPDP Act 2023 & Clinical Telemedicine Compliance</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-600">
            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <div className="flex items-center gap-2 text-emerald-800">
                <HealthcareIcon name="lock" className="w-5 h-5 text-emerald-700" />
                <span className="font-bold text-sm text-[#0F172A]">End-to-End Encryption</span>
              </div>
              <p className="leading-relaxed">Peer-to-peer WebRTC video feeds with AES-256 encryption. Audio and video streams are strictly ephemeral and never stored on cloud servers.</p>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <div className="flex items-center gap-2 text-teal-800">
                <HealthcareIcon name="shield-check" className="w-5 h-5 text-teal-700" />
                <span className="font-bold text-sm text-[#0F172A]">NCISM Registered Clinicians</span>
              </div>
              <p className="leading-relaxed">Every attending practitioner holds statutory registration under the NCISM Act 2020 and adheres to official Telemedicine Practice Guidelines.</p>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <div className="flex items-center gap-2 text-amber-800">
                <HealthcareIcon name="file-text" className="w-5 h-5 text-amber-700" />
                <span className="font-bold text-sm text-[#0F172A]">Tamper-Proof Prescriptions</span>
              </div>
              <p className="leading-relaxed">All digital Nuskha prescriptions are anchored with 21 CFR Part 11 electronic signatures and a cryptographic SHA-256 verification hash.</p>
            </div>
          </div>
        </section>

        {/* CTA Banner */}
        <div className="rounded-3xl bg-gradient-to-br from-[#1B4332] to-[#2D6A4F] text-white p-8 sm:p-10 shadow-md flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="space-y-2 max-w-xl">
            <h3 className="text-2xl font-bold">Ready to consult a senior Unani clinician?</h3>
            <p className="text-xs sm:text-sm text-emerald-100/90 leading-relaxed">
              Appointments are available Monday to Saturday. Receive a comprehensive constitutional appraisal and customized treatment regimen.
            </p>
          </div>
          <Link
            href="/contact?type=teleconsult"
            className="shrink-0 px-8 py-3.5 rounded-2xl bg-white text-[#1B4332] hover:bg-slate-100 font-bold text-xs shadow-sm transition"
          >
            Schedule Consultation
          </Link>
        </div>

      </div>
    </PublicWebsiteShell>
  );
}
