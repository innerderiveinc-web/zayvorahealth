"use client";

import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export default function AiTransparencyPage() {
  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Clinical Governance & Accountability"
        title="AI Transparency & Decision Support Charter"
        subtitle="An open, accountable disclosure of how Hakeem Sahab AI™ assists clinicians, adheres to classical evidence, and enforces non-delegable human medical judgment."
        breadcrumbs={[{ label: "AI Transparency" }]}
        primaryCta={{ label: "Book a Clinical Consultation", href: "/book" }}
        secondaryCta={{ label: "Clinical Governance Charter", href: "/clinical-governance" }}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto space-y-12">
        
        {/* Core Principles Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 rounded-3xl bg-white border border-[#E2E8F0] shadow-sm space-y-3">
            <div className="w-10 h-10 rounded-2xl bg-[#E8F5E9] border border-[#C8E6C9] flex items-center justify-center text-[#1B4332]">
              <HealthcareIcon name="stethoscope" className="w-5 h-5 text-[#2D6A4F]" />
            </div>
            <h3 className="font-bold text-[#0F172A] text-base">Human in the Loop</h3>
            <p className="text-xs text-[#64748B] leading-relaxed">
              Zero autonomous prescribing. Every diagnostic assessment, formulation choice, and care plan must be reviewed and authorized by an NCISM-registered physician.
            </p>
          </div>

          <div className="p-6 rounded-3xl bg-white border border-[#E2E8F0] shadow-sm space-y-3">
            <div className="w-10 h-10 rounded-2xl bg-[#E8F5E9] border border-[#C8E6C9] flex items-center justify-center text-[#1B4332]">
              <HealthcareIcon name="clipboard" className="w-5 h-5 text-[#2D6A4F]" />
            </div>
            <h3 className="font-bold text-[#0F172A] text-base">Classical &amp; Empirical Grounding</h3>
            <p className="text-xs text-[#64748B] leading-relaxed">
              Synthesized directly from verified canonical texts: <em>Al-Qanun fi al-Tibb</em>, <em>Kitab al-Kulliyat</em>, and the <em>Unani Pharmacopoeia of India (UPI)</em> cross-referenced with PubMed trials.
            </p>
          </div>

          <div className="p-6 rounded-3xl bg-white border border-[#E2E8F0] shadow-sm space-y-3">
            <div className="w-10 h-10 rounded-2xl bg-[#E8F5E9] border border-[#C8E6C9] flex items-center justify-center text-[#1B4332]">
              <HealthcareIcon name="shield-check" className="w-5 h-5 text-[#2D6A4F]" />
            </div>
            <h3 className="font-bold text-[#0F172A] text-base">Visible Safety Firewalls</h3>
            <p className="text-xs text-[#64748B] leading-relaxed">
              Real-time multi-barrier screening for herb-drug interactions (CYP450 enzymes), pregnancy contraindications, and Schedule E(1) Mudabbar purification clearance.
            </p>
          </div>
        </div>

        {/* Detailed Sections */}
        <div className="bg-white rounded-3xl border border-[#E2E8F0] p-8 sm:p-10 shadow-sm space-y-10 text-xs sm:text-sm text-[#475569] leading-relaxed">
          
          <section className="space-y-3">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E8F5E9] text-xs font-semibold text-[#1B4332]">
              <span>Section 01</span>
            </div>
            <h2 className="text-xl font-extrabold text-[#0F172A] tracking-tight">
              What Hakeem Sahab AI™ Does
            </h2>
            <p>
              Hakeem Sahab AI™ operates exclusively as an assistive <strong>Clinical Decision Support System (CDSS)</strong> for registered practitioners of Greco-Arab Unani medicine. It processes structured clinical intake data—including presenting symptoms, vitals, quantitative 10-Ajnas pulse characteristics, and laboratory findings—and evaluates them against standardized pharmacopeial rules.
            </p>
            <p>
              The system assists the clinician by:
            </p>
            <ul className="list-disc pl-5 space-y-1.5 text-[#64748B]">
              <li>Highlighting potential humoral dyscrasias (<em>Su-e-Mizaj</em>) and organ-axis dynamics (such as the <em>Dimagh-Meda</em> brain-gut axis).</li>
              <li>Surfacing classical formulation templates from the Unani Pharmacopoeia of India (UPI).</li>
              <li>Screening proposed botanicals against confirmed patient allergies and active allopathic medications.</li>
              <li>Calculating objective risk scores to assist clinical triage.</li>
            </ul>
          </section>

          <section className="space-y-3 pt-6 border-t border-[#F1F5F9]">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#FEF2F2] text-xs font-semibold text-[#991B1B]">
              <span>Section 02</span>
            </div>
            <h2 className="text-xl font-extrabold text-[#0F172A] tracking-tight">
              What Hakeem Sahab AI™ Cannot and Will Not Do
            </h2>
            <div className="p-4 rounded-2xl bg-[#FAFAF7] border border-[#E2E8F0] space-y-2">
              <ul className="list-disc pl-5 space-y-2 text-[#64748B]">
                <li><strong>No Autonomous Prescribing:</strong> The system cannot generate, finalize, or dispense a prescription without active clinician manual review and electronic signature authentication.</li>
                <li><strong>No Independent Diagnosis:</strong> The model cannot establish an authoritative diagnosis. Diagnostic determination is reserved exclusively for licensed human clinicians.</li>
                <li><strong>No Emergency Triage Overrides:</strong> When emergency red flags (e.g. acute chest pressure, sudden hemoptysis, severe respiratory distress) are detected, elective AI suggestions are automatically suppressed, and the user is directed to call <strong>112</strong> immediately.</li>
                <li><strong>No Opaque Predictions:</strong> Every recommendation provides verbatim citations from canonical medical monographs and published scientific literature.</li>
              </ul>
            </div>
          </section>

          <section className="space-y-3 pt-6 border-t border-[#F1F5F9]">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E8F5E9] text-xs font-semibold text-[#1B4332]">
              <span>Section 03</span>
            </div>
            <h2 className="text-xl font-extrabold text-[#0F172A] tracking-tight">
              Sources of Medical &amp; Pharmacological Knowledge
            </h2>
            <p>
              The underlying knowledge graphs of Hakeem Sahab AI™ are built upon authoritative, primary-source medical literature:
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-xs">
              <div className="p-3.5 rounded-xl bg-[#FAFAF7] border border-[#E2E8F0] space-y-1">
                <span className="font-bold text-[#0F172A] block">Classical Canons</span>
                <p className="text-[#64748B]">Al-Qanun fi al-Tibb (Avicenna), Kitab al-Kulliyat (Averroes), Kitab al-Hawi (Rhazes), and Kamil al-Sina&apos;ah.</p>
              </div>
              <div className="p-3.5 rounded-xl bg-[#FAFAF7] border border-[#E2E8F0] space-y-1">
                <span className="font-bold text-[#0F172A] block">Statutory Pharmacopoeias</span>
                <p className="text-[#64748B]">National Formulary of Unani Medicine (NFUM) and the Unani Pharmacopoeia of India (UPI Parts I–VI).</p>
              </div>
              <div className="p-3.5 rounded-xl bg-[#FAFAF7] border border-[#E2E8F0] space-y-1">
                <span className="font-bold text-[#0F172A] block">Contemporary Biomedical Evidence</span>
                <p className="text-[#64748B]">Peer-reviewed phytotherapy journals, in-vivo pharmacokinetic trials, and toxicology studies.</p>
              </div>
              <div className="p-3.5 rounded-xl bg-[#FAFAF7] border border-[#E2E8F0] space-y-1">
                <span className="font-bold text-[#0F172A] block">Herb-Drug Interaction Data</span>
                <p className="text-[#64748B]">Cytochrome P450 inhibition profiles and clinical polypharmacy registries.</p>
              </div>
            </div>
          </section>

          <section className="space-y-3 pt-6 border-t border-[#F1F5F9]">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E8F5E9] text-xs font-semibold text-[#1B4332]">
              <span>Section 04</span>
            </div>
            <h2 className="text-xl font-extrabold text-[#0F172A] tracking-tight">
              Representation of Algorithmic Uncertainty
            </h2>
            <p>
              When clinical intake contains atypical symptom presentations, rare co-morbidities, or conflicting laboratory markers, the model calculates an <strong>Epistemic Uncertainty Metric</strong>. If uncertainty exceeds pre-set clinical boundaries (e.g. &gt; 0.15), the system explicitly refuses to guess and instead prompts the doctor to request senior clinical quorum review or order targeted laboratory diagnostics.
            </p>
          </section>

          <section className="space-y-3 pt-6 border-t border-[#F1F5F9]">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E8F5E9] text-xs font-semibold text-[#1B4332]">
              <span>Section 05</span>
            </div>
            <h2 className="text-xl font-extrabold text-[#0F172A] tracking-tight">
              Auditability &amp; Regulatory Compliance
            </h2>
            <p>
              In full adherence to <strong>Section 35 of the NCISM Act 2020</strong> and India&apos;s <strong>Digital Personal Data Protection (DPDP) Act 2023</strong>:
            </p>
            <ul className="list-disc pl-5 space-y-1.5 text-[#64748B]">
              <li>All clinician decisions, model prompts, and overrides are recorded in an immutable cryptographic Merkle ledger.</li>
              <li>Electronic signatures require active practitioner authentication and are sealed with SHA-256 integrity hashes.</li>
              <li>Patient health information is purpose-restricted and never utilized for unauthorized commercial model training.</li>
            </ul>
          </section>

        </div>

        {/* Navigation & Incident Reporting Link */}
        <div className="pt-6 border-t border-[#E2E8F0] flex flex-col sm:flex-row justify-between items-center gap-4 text-xs">
          <Link href="/" className="text-[#1B4332] font-bold hover:underline flex items-center gap-1">
            <HealthcareIcon name="arrow-left" className="w-3.5 h-3.5" />
            <span>Return to Institutional Homepage</span>
          </Link>
          <div className="flex items-center gap-4 text-[#64748B]">
            <Link href="/grievance" className="hover:text-[#0F172A] transition">
              Report an AI Concern / Grievance
            </Link>
            <span>•</span>
            <Link href="/medical-disclaimer" className="hover:text-[#0F172A] transition">
              Medical Disclaimer
            </Link>
          </div>
        </div>

      </div>
    </PublicWebsiteShell>
  );
}
