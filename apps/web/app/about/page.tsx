import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export const metadata = {
  title: "About ZAYVORA Health™ — Institutional Mission, Vision & Clinical Leadership",
  description: "Learn about ZAYVORA Health™, our mission to integrate classical Unani Medicine with contemporary biomedical science, and our clinician-led digital healthcare operating system.",
};

export default function AboutPage() {
  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Institutional Overview"
        title="Pioneering the Future of Integrative Medicine"
        subtitle="Uniting classical Greco-Arab medical science with contemporary diagnostic intelligence, clinician-governed technology, and rigorous patient safety."
        breadcrumbs={[{ label: "About Us" }]}
        primaryCta={{ label: "Meet Clinical Faculty", href: "/team" }}
        secondaryCta={{ label: "Explore Clinical Care", href: "/services/clinical-care" }}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-20">
        {/* THE ZAYVORA THEORY AT A GLANCE (30-SECOND & 2-MINUTE EXPOSITION) */}
        <section className="p-8 sm:p-12 rounded-3xl bg-slate-900 border border-slate-800 text-white shadow-xl relative overflow-hidden">
          <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-600/10 rounded-full blur-3xl pointer-events-none" />
          <div className="max-w-4xl space-y-6 relative z-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-500/30 text-xs font-semibold text-emerald-300">
              <span>💡 THE UNIFIED DOCTRINE AT A GLANCE</span>
            </div>

            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-white tracking-tight leading-tight">
              What is ZAYVORA Health? The Core Theory
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
              <div className="p-6 rounded-2xl bg-white/5 border border-white/10 space-y-3">
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 block">
                  The 30-Second Public Synthesis
                </span>
                <p className="text-sm text-slate-200 leading-relaxed">
                  ZAYVORA is a clinician-governed clinical operating platform that bridges <strong>1,000 years of root-cause Greco-Arab healing (Tibb-e-Unani)</strong> with <strong>21st-century diagnostic science and clinical decision support</strong>. Where conventional medicine focuses on symptom management, and traditional systems historically lacked digital documentation and safety gates, ZAYVORA unifies both: structuring constitutional assessment (Mizaj), correlating objective laboratory hematology and imaging, and delivering individualized, evidence-informed botanical therapies.
                </p>
              </div>

              <div className="p-6 rounded-2xl bg-white/5 border border-white/10 space-y-3">
                <span className="text-xs font-bold uppercase tracking-wider text-teal-400 block">
                  The 2-Minute Clinical & Institutional Thesis
                </span>
                <p className="text-sm text-slate-200 leading-relaxed">
                  Under the doctrine of <strong>Integrative Precision Medicine (IPM)</strong>, ZAYVORA eliminates the reductionist monotherapy trap. Classical humoral dynamics (<em>Akhlat</em>) map directly to cellular biofluids and microvascular shear; constitutional typing (<em>Mizaj</em>) correlates with metabolic phenotyping, mitochondrial bioenergetics, and GLUT4 translocation; and the 6 Essentials (<em>Asbab-e-Sitta</em>) align with circadian chronobiology, sleep architecture, and gut metagenomics.
                </p>
              </div>
            </div>

            <div className="pt-4 flex flex-wrap items-center gap-4 border-t border-white/10 text-xs">
              <span className="text-slate-400 font-medium">Explore the Operational System:</span>
              <Link
                href="/library"
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl transition shadow-sm flex items-center gap-1.5"
              >
                <span>📖</span> 12-Volume Canonical Library
              </Link>
              <Link
                href="/simulator"
                className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-xl transition shadow-sm flex items-center gap-1.5"
              >
                <span>🎓</span> Clinical Case Simulator
              </Link>
              <Link
                href="/doctor"
                className="px-4 py-2 bg-white/10 hover:bg-white/20 text-white font-semibold rounded-xl transition flex items-center gap-1.5"
              >
                <span>🩺</span> Doctor Consultation Desk
              </Link>
            </div>
          </div>
        </section>

        {/* MISSION & VISION */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch">
          <div className="p-8 sm:p-10 rounded-3xl bg-white border border-slate-200/80 shadow-sm flex flex-col justify-between space-y-6">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-xs font-bold uppercase tracking-wider text-[#1B4332] mb-4">
                <HealthcareIcon name="shield-check" className="w-3.5 h-3.5 text-emerald-700" />
                <span>Our Mission</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-[#0F172A]">Restoring Constitutional Balance & Human Vitality</h2>
              <p className="mt-4 text-slate-700 text-sm sm:text-base leading-relaxed">
                To deliver compassionate, individualized, and scientifically validated healthcare by revitalizing classical Unani medicine through contemporary clinical diagnostics, standardized botanical pharmaceuticals, and clinician-governed clinical informatics.
              </p>
            </div>
            <div className="pt-4 border-t border-slate-100 flex items-center gap-3 text-xs text-slate-500">
              <HealthcareIcon name="check" className="w-4 h-4 text-emerald-600 shrink-0" />
              <span>Patient-centered care rooted in classical humoral physiology.</span>
            </div>
          </div>

          <div className="p-8 sm:p-10 rounded-3xl bg-white border border-slate-200/80 shadow-sm flex flex-col justify-between space-y-6">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-50 border border-teal-200 text-xs font-bold uppercase tracking-wider text-[#2D6A4F] mb-4">
                <HealthcareIcon name="activity" className="w-3.5 h-3.5 text-[#2D6A4F]" />
                <span>Our Vision</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-[#0F172A]">A Global Standard for Integrative Healthcare</h2>
              <p className="mt-4 text-slate-700 text-sm sm:text-base leading-relaxed">
                To establish ZAYVORA as the world's preeminent institutional healthcare ecosystem—where constitutional etiology, organ-axis reasoning, and biomedical diagnostics converge to resolve complex chronic illnesses without avoidable pharmaceutical toxicities.
              </p>
            </div>
            <div className="pt-4 border-t border-slate-100 flex items-center gap-3 text-xs text-slate-500">
              <HealthcareIcon name="check" className="w-4 h-4 text-[#2D6A4F] shrink-0" />
              <span>Statutory compliance under NCISM Act 2020 and DPDP Act 2023.</span>
            </div>
          </div>
        </section>

        {/* FOUNDER & CLINICAL ARCHITECT SPOTLIGHT */}
        <section className="rounded-3xl bg-gradient-to-br from-[#1B4332] via-[#2D6A4F] to-[#0F172A] text-white p-8 sm:p-12 lg:p-16 shadow-lg">
          <div className="max-w-4xl space-y-6">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 border border-white/20 text-xs font-semibold text-emerald-200">
              <HealthcareIcon name="academic" className="w-4 h-4 text-emerald-300" />
              <span>Founding Leadership & Architecture</span>
            </div>

            <h2 className="text-3xl sm:text-4xl font-extrabold text-white leading-tight">
              Clinician-Led Innovation Under Hakeem Dr. Irfan Ashraf
            </h2>

            <p className="text-sm sm:text-base text-emerald-100/90 leading-relaxed">
              ZAYVORA was conceived and architected by <strong>Hakeem Dr. Irfan Ashraf</strong> (Founder, Chairman & Chief Medical Architect), a senior clinician dedicated to translating traditional wisdom into verifiable medical outcomes.
            </p>

            <p className="text-sm sm:text-base text-emerald-100/90 leading-relaxed">
              Recognizing that traditional medicine often suffered from fragmented record-keeping, variable botanical potency, and lack of diagnostic corroboration, Dr. Ashraf spearheaded the engineering of <strong>ZAYVORA Health OS™</strong>. The operating system bridges 10-Ajnas pulse and constitutional staging (Mizaj) with contemporary clinical pathology, cryptographically sealed medical records (21 CFR Part 11), and safe, explainable artificial intelligence.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-6 border-t border-white/10 text-xs">
              <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                <span className="block text-emerald-300 font-bold text-sm">NCISM Registered</span>
                <span className="text-emerald-100/70 text-[11px] mt-1 block">Reg Number: BUMS-2004-9841</span>
              </div>
              <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                <span className="block text-emerald-300 font-bold text-sm">Clinical Canon</span>
                <span className="text-emerald-100/70 text-[11px] mt-1 block">Al-Qanun fi al-Tibb & Classical Manuscripts</span>
              </div>
              <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                <span className="block text-emerald-300 font-bold text-sm">Regulatory Integrity</span>
                <span className="text-emerald-100/70 text-[11px] mt-1 block">Zero Unverified Claims & Absolute Transparency</span>
              </div>
            </div>
          </div>
        </section>

        {/* FOUR PILLARS */}
        <section className="space-y-8">
          <div className="text-center max-w-3xl mx-auto space-y-2">
            <span className="text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">Clinical Philosophy</span>
            <h2 className="text-3xl font-extrabold text-[#0F172A]">The Four Pillars of ZAYVORA Care</h2>
            <p className="text-sm text-slate-600">
              Bridging centuries of empirical healing with the highest standards of modern clinical scrutiny.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="p-6 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-3">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-[#1B4332] flex items-center justify-center">
                <HealthcareIcon name="leaf" className="w-5 h-5 text-[#1B4332]" />
              </div>
              <h3 className="text-base font-bold text-[#0F172A]">1. Classical Unani Core</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Rooted in the humoral etiology of Ibn Sina (Avicenna) and Al-Razi. We assess constitutional Mizaj and restore Hararat-e-Ghariziya (vital innate heat).
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-3">
              <div className="w-10 h-10 rounded-xl bg-teal-50 text-[#2D6A4F] flex items-center justify-center">
                <HealthcareIcon name="flask" className="w-5 h-5 text-[#2D6A4F]" />
              </div>
              <h3 className="text-base font-bold text-[#0F172A]">2. Biomedical Integration</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Every traditional diagnosis is corroborated with contemporary biomarkers: complete metabolic panels, hormonal assays, and imaging diagnostics.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-3">
              <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-800 flex items-center justify-center">
                <HealthcareIcon name="shield-check" className="w-5 h-5 text-amber-700" />
              </div>
              <h3 className="text-base font-bold text-[#0F172A]">3. Patient Safety Mandate</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Mandatory Schedule E(1) Mudabbar (purification) verification, emergency red-flag exclusion protocols, and 21 CFR Part 11 digital signatures.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-3">
              <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-800 flex items-center justify-center">
                <HealthcareIcon name="stethoscope" className="w-5 h-5 text-blue-700" />
              </div>
              <h3 className="text-base font-bold text-[#0F172A]">4. Governed AI Copilot</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Hakeem Sahab AI™ assists with literature retrieval while enforcing strict safety guardrails; attending physicians retain 100% decision authority.
              </p>
            </div>
          </div>
        </section>

        {/* SYSTEM ARCHITECTURE */}
        <section className="p-8 sm:p-10 rounded-3xl bg-white border border-slate-200/80 shadow-sm space-y-6">
          <div className="max-w-3xl space-y-2">
            <span className="text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">Digital Infrastructure</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A]">The ZAYVORA Health OS™ Platform</h2>
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              ZAYVORA Health OS™ is our proprietary enterprise healthcare operating system built from the ground up to support holistic clinical workflows. Designed with zero vendor lock-in, it securely manages multi-clinic tenancy, 10-Ajnas pulse capture, digital twin trajectories, and GMP cleanroom pharmaceutical manufacturing.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <HealthcareIcon name="hospital" className="w-4 h-4 text-[#2D6A4F]" />
                Clinical Matab Desk
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                OPD queues, SOAP notes, 10-Ajnas diagnostic workbench, organ-axis dynamic radar, and 21 CFR Part 11 cryptographic sealing.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <HealthcareIcon name="library" className="w-4 h-4 text-[#2D6A4F]" />
                Knowledge & Clinical AI
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Dense-vector + Neo4j ontological graph (ZKB) powering Hakeem Sahab AI™ point-of-care decision support with verified UPI citations.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <HealthcareIcon name="pill" className="w-4 h-4 text-[#2D6A4F]" />
                Dispensary & Cleanroom
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                First-Expired-First-Out (FEFO) dispensing, eBMR batch manufacturing records, and cold-chain environmental surveillance.
              </p>
            </div>
          </div>
        </section>

        {/* INSTITUTIONAL CALL TO ACTION */}
        <section className="p-8 sm:p-12 rounded-3xl bg-[#FAF9F5] border border-[#DDD6C1] text-center space-y-6">
          <div className="max-w-2xl mx-auto space-y-2">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A]">Experience Clinician-Led Holistic Care</h2>
            <p className="text-xs sm:text-sm text-slate-600">
              Schedule an in-person or telehealth consultation with our NCISM-registered faculty at ZAYVORA Matab™.
            </p>
          </div>

          <div className="flex flex-wrap justify-center gap-4 pt-2">
            <Link
              href="/booking"
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white font-bold text-xs shadow-md transition"
            >
              <HealthcareIcon name="calendar" className="w-4 h-4 text-white" />
              <span>Book Consultation</span>
            </Link>
            <Link
              href="/contact"
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-white hover:bg-slate-50 border border-slate-300 text-slate-800 font-bold text-xs transition"
            >
              <HealthcareIcon name="phone" className="w-4 h-4 text-slate-700" />
              <span>Contact Admissions</span>
            </Link>
          </div>
        </section>

        {/* CLINICAL GOVERNANCE AUDIT METADATA */}
        <section className="p-5 rounded-2xl bg-slate-100 border border-slate-200 text-xs text-slate-600 flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <strong className="text-slate-800">Organizational Governance:</strong> ZAYVORA Health Systems Private Limited • Registered under the Companies Act 2013 • Governed under the NCISM Act 2020.
          </div>
          <div className="text-[11px] text-slate-500">
            Last Content Audit: September 2026 • Document Ref: ZAY-GOV-2026-A1
          </div>
        </section>
      </div>
    </PublicWebsiteShell>
  );
}
