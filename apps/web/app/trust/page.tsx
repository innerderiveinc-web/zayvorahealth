"use client";

import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export default function TrustAndSafetyCentrePage() {
  const TRUST_SECTIONS = [
    {
      id: "clinical-governance",
      title: "Clinical Governance & NCISM Compliance",
      subtitle: "Qualified, registered practitioners with continuous peer oversight",
      icon: "stethoscope",
      description:
        "Every patient interaction, diagnosis, and prescription is authorized by clinicians holding recognized BUMS or MD (Unani) qualifications registered under the National Commission for Indian System of Medicine (NCISM) Act 2020. Prescriptions are cryptographically signed under 21 CFR Part 11 electronic signature standards.",
      highlights: [
        "100% NCISM-Registered Clinicians",
        "Mandatory Peer Quorum Review for Complex Cases",
        "Cryptographic SHA-256 Prescription Sealing"
      ],
      link: "/clinical-governance",
      linkText: "Read Governance Charter"
    },
    {
      id: "ai-ethics",
      title: "AI Clinical Decision Support Ethics",
      subtitle: "Human clinician oversight; zero autonomous medical practice",
      icon: "activity",
      description:
        "Hakeem Sahab AI™ operates exclusively as an assistive decision support copilot. It evaluates pharmacopeial monographs, scans for herb-drug interactions, and calculates epistemic uncertainty. It is strictly barred from independently issuing prescriptions or formulating final diagnoses.",
      highlights: [
        "Non-Autonomous Prescribing Barrier",
        "Transparent Monograph & Trial Citations",
        "Strict Out-of-Bounds Emergency Triage"
      ],
      link: "/ai-transparency",
      linkText: "Review AI Transparency Disclosure"
    },
    {
      id: "patient-privacy",
      title: "Patient Privacy & DPDP Act 2023",
      subtitle: "Data sovereignty, purpose limitation, and cryptographic security",
      icon: "lock",
      description:
        "Patient health records and biometric data are governed under India's statutory Digital Personal Data Protection (DPDP) Act 2023. Data is encrypted in transit and at rest, and will never be monetized, sold, or shared with third-party advertisers.",
      highlights: [
        "DPDP Act 2023 Statutory Consent Architecture",
        "Ayushman Bharat Digital Mission (ABDM) Integration",
        "Granular Patient Revocation Rights"
      ],
      link: "/privacy-policy",
      linkText: "View Privacy Policy"
    },
    {
      id: "medication-safety",
      title: "Botanical Quality & Medication Safety",
      subtitle: "Schedule M-I (AYUSH-GMP) manufacturing and heavy-metal testing",
      icon: "shield-check",
      description:
        "All prescribed Unani formulations are produced in ISO Class 7 pharmaceutical cleanrooms adhering strictly to Schedule M-I (AYUSH-GMP). Every batch undergoes mandatory Inductively Coupled Plasma Mass Spectrometry (ICP-MS) testing for heavy metals and Schedule E(1) Mudabbar detoxification.",
      highlights: [
        "Schedule M-I Cleanroom Compliance",
        "ICP-MS Heavy Metal & Aflatoxin Screening",
        "Statutory Mudabbar Detoxification Gate"
      ],
      link: "/products/safety",
      linkText: "Explore Quality & Safety Standards"
    },
    {
      id: "evidence-policy",
      title: "Evidence Policy & Intellectual Honesty",
      subtitle: "Grounded in traditional canons; cross-referenced with modern trials",
      icon: "clipboard",
      description:
        "We balance profound respect for classical Greco-Arab medical treatises with contemporary scientific rigor. Therapeutic claims are explicitly categorized by evidence tier, and therapeutic boundaries are openly communicated to patients.",
      highlights: [
        "4-Tier Systematic Evidence Grading",
        "Open Documentation of Clinical Boundaries",
        "Active Clinical Cohort Research (Study ZCT-2026-001)"
      ],
      link: "/research",
      linkText: "View Research & Evidence Policy"
    },
    {
      id: "patient-rights",
      title: "Patient Rights & Informed Consent",
      subtitle: "Dignified, collaborative healthcare centered on patient autonomy",
      icon: "heart",
      description:
        "Patients have the fundamental right to clear explanations of their constitutional assessment, transparent treatment rationales, full visibility into their electronic health records, and the unconditional right to seek a second clinical opinion.",
      highlights: [
        "Comprehensive Patient Charter",
        "Informed Consent on All Modalities",
        "Complete Health Record Portability"
      ],
      link: "/patient-rights",
      linkText: "Read Patient Rights Charter"
    },
    {
      id: "grievance-redressal",
      title: "Grievance Redressal & Ombudsman",
      subtitle: "Designated institutional officer with statutory 15-day resolution SLA",
      icon: "scale",
      description:
        "If you have any concern regarding clinical care, patient dignity, billing transparency, or data privacy, you may submit a formal complaint to our designated Grievance Redressal Officer. All formal complaints are investigated within 15 business days.",
      highlights: [
        "Designated Statutory Ombudsman",
        "Enforceable 15-Day Resolution SLA",
        "Transparent Audit & Escalation Pathway"
      ],
      link: "/grievance",
      linkText: "Access Grievance Redressal Desk"
    },
    {
      id: "emergency-guidance",
      title: "Emergency Medical Guidance",
      subtitle: "Elective outpatient scope; clear emergency referral protocols",
      icon: "alert-triangle",
      description:
        "ZAYVORA Health™ operates elective outpatient clinics and teleconsultation care. We do not operate an acute emergency casualty ward. Patients experiencing acute chest pain, sudden breathlessness, severe neurological symptoms, or major physical trauma must call 112 or visit the nearest hospital emergency department.",
      highlights: [
        "Elective Outpatient Scope Clarification",
        "Immediate Red-Flag Triage Lockouts",
        "Emergency Referral Hotline: Call 112"
      ],
      link: "/terms",
      linkText: "Review Terms & Triage Scope"
    }
  ];

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Trust, Safety & Governance"
        title="ZAYVORA Trust & Safety Centre"
        subtitle="Our comprehensive institutional framework safeguarding clinical excellence, patient privacy, pharmaceutical safety, and ethical healthcare delivery."
        breadcrumbs={[{ label: "Trust & Safety" }]}
        primaryCta={{ label: "Book a Clinical Consultation", href: "/book" }}
        secondaryCta={{ label: "Meet Our Care Team", href: "/doctors" }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14 space-y-14">
        
        {/* Institutional Pledge Callout */}
        <div className="p-8 rounded-3xl bg-white border border-[#E2E8F0] shadow-sm">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            <div className="lg:col-span-8 space-y-3">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E8F5E9] text-xs font-semibold text-[#1B4332]">
                <HealthcareIcon name="shield-check" className="w-4 h-4 text-[#2D6A4F]" />
                <span>Our Institutional Commitment</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] tracking-tight">
                Healthcare Built on Transparency, Not Jargon.
              </h2>
              <p className="text-sm text-[#475569] leading-relaxed">
                At ZAYVORA Health™, trust is not an afterthought or a marketing badge. It is codified into every layer of our organization—from statutory compliance under the NCISM Act 2020 and DPDP Act 2023 to our multi-barrier pharmaceutical cleanroom testing and strict human clinician oversight.
              </p>
            </div>

            <div className="lg:col-span-4 p-6 rounded-2xl bg-[#FAFAF7] border border-[#E2E8F0] space-y-3 text-xs">
              <span className="font-bold text-[#0F172A] block uppercase tracking-wider text-[11px]">
                Statutory Accreditations
              </span>
              <ul className="space-y-2 text-[#64748B]">
                <li className="flex items-center gap-2">
                  <HealthcareIcon name="check" className="w-3.5 h-3.5 text-[#2D6A4F] shrink-0" />
                  <span>NCISM Act 2020 Registered Tabeebs</span>
                </li>
                <li className="flex items-center gap-2">
                  <HealthcareIcon name="check" className="w-3.5 h-3.5 text-[#2D6A4F] shrink-0" />
                  <span>DPDP Act 2023 Statutory Privacy</span>
                </li>
                <li className="flex items-center gap-2">
                  <HealthcareIcon name="check" className="w-3.5 h-3.5 text-[#2D6A4F] shrink-0" />
                  <span>Schedule M-I (AYUSH-GMP) Cleanrooms</span>
                </li>
                <li className="flex items-center gap-2">
                  <HealthcareIcon name="check" className="w-3.5 h-3.5 text-[#2D6A4F] shrink-0" />
                  <span>21 CFR Part 11 Electronic Signatures</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* 8 Detailed Trust Pillars Grid */}
        <div className="space-y-6">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
              Pillars of Accountability
            </span>
            <h2 className="text-2xl font-extrabold text-[#0F172A] mt-1">
              Explore Our Governance &amp; Safety Standards
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {TRUST_SECTIONS.map((sec) => (
              <div
                key={sec.id}
                className="p-7 rounded-3xl bg-white border border-[#E2E8F0] shadow-sm hover:border-[#CBD5E1] transition flex flex-col justify-between space-y-5"
              >
                <div className="space-y-3">
                  <div className="flex items-start gap-4">
                    <div className="w-11 h-11 rounded-2xl bg-[#E8F5E9] border border-[#C8E6C9] flex items-center justify-center text-[#1B4332] shrink-0">
                      <HealthcareIcon name={sec.icon} className="w-5 h-5 text-[#2D6A4F]" />
                    </div>
                    <div>
                      <h3 className="text-base font-bold text-[#0F172A]">{sec.title}</h3>
                      <p className="text-xs text-[#64748B] font-medium mt-0.5">{sec.subtitle}</p>
                    </div>
                  </div>

                  <p className="text-xs sm:text-sm text-[#475569] leading-relaxed">
                    {sec.description}
                  </p>

                  <div className="pt-2 border-t border-[#F1F5F9] space-y-1.5">
                    {sec.highlights.map((h, idx) => (
                      <div key={idx} className="flex items-center gap-2 text-xs text-[#334155]">
                        <HealthcareIcon name="shield-check" className="w-3.5 h-3.5 text-[#2D6A4F] shrink-0" />
                        <span>{h}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="pt-3 border-t border-[#F1F5F9]">
                  <Link
                    href={sec.link}
                    className="text-xs font-bold text-[#1B4332] hover:text-[#2D6A4F] inline-flex items-center gap-1.5 transition"
                  >
                    <span>{sec.linkText}</span>
                    <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Emergency Medical Guidance Banner */}
        <div className="p-8 rounded-3xl bg-[#FEF2F2] border border-[#FCA5A5] flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-2xl bg-[#DC2626] text-white flex items-center justify-center shrink-0">
              <HealthcareIcon name="alert-triangle" className="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 className="text-base font-bold text-[#991B1B]">
                Medical Emergency Protocol Notice
              </h3>
              <p className="text-xs sm:text-sm text-[#B91C1C] mt-1 leading-relaxed max-w-2xl">
                ZAYVORA Health™ delivers planned, elective outpatient consultations and teleconsultation care. If you are experiencing acute medical emergencies—such as acute chest pain, severe difficulty breathing, sudden paralysis, or major physical trauma—please immediately call <strong>112</strong> or visit the nearest emergency casualty department.
              </p>
            </div>
          </div>
          <div className="shrink-0">
            <span className="px-5 py-2.5 rounded-xl bg-[#DC2626] text-white font-bold text-xs shadow-sm">
              Emergency Services: Call 112
            </span>
          </div>
        </div>

        {/* Clinical Contact & Consultation CTA */}
        <div className="p-8 sm:p-12 rounded-3xl bg-[#1B4332] text-white text-center space-y-4">
          <h3 className="text-2xl sm:text-3xl font-extrabold text-white">
            Have Questions for Our Medical Directorate?
          </h3>
          <p className="text-xs sm:text-sm text-[#D8F3DC] max-w-xl mx-auto leading-relaxed">
            Our clinical coordinators are available to answer your questions regarding care pathways, doctor credentials, and safety standards.
          </p>
          <div className="pt-2 flex flex-wrap items-center justify-center gap-3">
            <Link
              href="/contact"
              className="px-6 py-3 rounded-xl bg-white text-[#1B4332] font-semibold text-xs hover:bg-[#F8FAFC] transition shadow-sm"
            >
              Contact Care Desk
            </Link>
            <Link
              href="/book"
              className="px-6 py-3 rounded-xl bg-[#2D6A4F] text-white font-semibold text-xs hover:bg-[#40916C] transition"
            >
              Book Clinical Consultation
            </Link>
          </div>
        </div>

      </div>
    </PublicWebsiteShell>
  );
}
