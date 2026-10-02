import React from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { CONDITIONS_DATA, ConditionDetail } from "@/lib/cms/conditionsData";

interface ConditionPageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return Object.keys(CONDITIONS_DATA).map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: ConditionPageProps) {
  const { slug } = await params;
  const condition = CONDITIONS_DATA[slug];

  if (!condition) {
    return { title: "Condition Not Found | ZAYVORA Health™" };
  }

  return {
    title: `${condition.title} (${condition.unaniTerm}) | Clinical Care Pathway | ZAYVORA Health™`,
    description: condition.subtitle,
  };
}

export default async function ConditionDetailPage({ params }: ConditionPageProps) {
  const { slug } = await params;
  const condition: ConditionDetail | undefined = CONDITIONS_DATA[slug];

  if (!condition) {
    notFound();
  }

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge={condition.category}
        title={condition.title}
        subtitle={`${condition.subtitle} Protocol Duration: ${condition.duration}.`}
        breadcrumbs={[
          { label: "Conditions", href: "/conditions" },
          { label: condition.title }
        ]}
        primaryCta={{
          label: "Book Clinical Consultation",
          href: `/book?condition=${condition.slug}`
        }}
        secondaryCta={{
          label: "Find a Matab Specialist",
          href: "/doctors"
        }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
        
        {/* ── 1. EMERGENCY RED FLAG BOX ─────────────────────────────────── */}
        <div className="p-6 rounded-3xl bg-[#FEF2F2] border border-[#FCA5A5] flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="w-10 h-10 rounded-2xl bg-[#DC2626] text-white flex items-center justify-center shrink-0">
              <HealthcareIcon name="alert-triangle" className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-[#991B1B]">Emergency Medical Guidance</h3>
              <p className="text-xs text-[#B91C1C] mt-1 leading-relaxed max-w-3xl">
                ZAYVORA provides scheduled outpatient and teleconsultation care. If you or someone with you experiences any of the red-flag symptoms below, seek emergency emergency care immediately:
              </p>
              <ul className="mt-2 space-y-1 text-xs text-[#7F1D1D] list-disc list-inside">
                {condition.redFlags.map((flag, idx) => (
                  <li key={idx}><strong>{flag}</strong></li>
                ))}
              </ul>
            </div>
          </div>
          <div className="shrink-0 self-stretch md:self-auto flex items-center justify-center">
            <span className="px-4 py-2 rounded-xl bg-[#DC2626] text-white font-bold text-xs">
              Emergency: Call 112
            </span>
          </div>
        </div>

        {/* ── 2. OVERVIEW & HUMORAL PATHOLOGY ───────────────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-8 space-y-6">
            <div className="bg-white rounded-3xl border border-[#E2E8F0] p-8 shadow-sm space-y-4">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E8F5E9] text-xs font-semibold text-[#1B4332]">
                <HealthcareIcon name="shield-check" className="w-4 h-4 text-[#2D6A4F]" />
                <span>Classical Unani Nosology: {condition.unaniTerm}</span>
              </div>
              <h2 className="text-xl sm:text-2xl font-extrabold text-[#0F172A]">Clinical Overview</h2>
              <p className="text-sm text-[#475569] leading-relaxed">
                {condition.overview}
              </p>
            </div>

            {/* Symptoms & Contributing Factors */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white rounded-3xl border border-[#E2E8F0] p-6 shadow-sm space-y-4">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-xl bg-[#E8F5E9] flex items-center justify-center text-[#1B4332]">
                    <HealthcareIcon name="clipboard" className="w-4 h-4" />
                  </div>
                  <h3 className="text-sm font-bold text-[#0F172A]">Common Clinical Symptoms</h3>
                </div>
                <ul className="space-y-2 text-xs text-[#475569]">
                  {condition.symptoms.map((sym, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <HealthcareIcon name="check" className="w-3.5 h-3.5 text-[#2D6A4F] shrink-0 mt-0.5" />
                      <span>{sym}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-white rounded-3xl border border-[#E2E8F0] p-6 shadow-sm space-y-4">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-xl bg-[#E8F5E9] flex items-center justify-center text-[#1B4332]">
                    <HealthcareIcon name="activity" className="w-4 h-4" />
                  </div>
                  <h3 className="text-sm font-bold text-[#0F172A]">Contributing Factors</h3>
                </div>
                <ul className="space-y-2 text-xs text-[#475569]">
                  {condition.contributingFactors.map((fac, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <HealthcareIcon name="arrow-right" className="w-3.5 h-3.5 text-[#2D6A4F] shrink-0 mt-0.5" />
                      <span>{fac}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Right Column: Quick Care Summary */}
          <div className="lg:col-span-4 space-y-6">
            <div className="bg-[#FAFAF7] rounded-3xl border border-[#E2E8F0] p-6 space-y-5">
              <h3 className="text-sm font-bold text-[#0F172A] border-b border-[#E2E8F0] pb-3">
                Pathway At A Glance
              </h3>

              <div className="space-y-3 text-xs">
                <div>
                  <span className="text-[#64748B] block text-[11px]">Primary Category</span>
                  <span className="font-semibold text-[#0F172A]">{condition.category}</span>
                </div>

                <div>
                  <span className="text-[#64748B] block text-[11px]">Expected Protocol Timeline</span>
                  <span className="font-semibold text-[#0F172A]">{condition.duration}</span>
                </div>

                <div>
                  <span className="text-[#64748B] block text-[11px]">Consultation Delivery</span>
                  <span className="font-semibold text-[#0F172A]">In-Clinic Matab™ or Encrypted Video</span>
                </div>

                <div>
                  <span className="text-[#64748B] block text-[11px]">Clinical Governance</span>
                  <span className="font-semibold text-[#1B4332]">NCISM Registered Unani Physician</span>
                </div>
              </div>

              <div className="pt-2">
                <Link
                  href={`/book?condition=${condition.slug}`}
                  className="w-full py-3 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white font-semibold text-xs transition shadow-sm flex items-center justify-center gap-2"
                >
                  <HealthcareIcon name="calendar" className="w-4 h-4 text-white" />
                  <span>Schedule Consultation</span>
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* ── 3. ZAYVORA CLINICAL ASSESSMENT ────────────────────────────── */}
        <div className="bg-white rounded-3xl border border-[#E2E8F0] p-8 shadow-sm space-y-6">
          <div className="max-w-2xl space-y-1">
            <span className="text-xs font-bold uppercase tracking-wider text-[#2D6A4F]">
              Comprehensive Workup
            </span>
            <h2 className="text-xl sm:text-2xl font-extrabold text-[#0F172A]">
              What Your ZAYVORA Clinician Evaluates
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-5 rounded-2xl bg-[#FAFAF7] border border-[#E2E8F0] space-y-2">
              <div className="w-8 h-8 rounded-lg bg-[#E8F5E9] flex items-center justify-center text-[#1B4332]">
                <HealthcareIcon name="clipboard" className="w-4 h-4" />
              </div>
              <h4 className="text-xs font-bold text-[#0F172A]">Constitutional Mizaj Staging</h4>
              <p className="text-xs text-[#64748B] leading-relaxed">
                {condition.assessment.mizajEvaluation}
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-[#FAFAF7] border border-[#E2E8F0] space-y-2">
              <div className="w-8 h-8 rounded-lg bg-[#E8F5E9] flex items-center justify-center text-[#1B4332]">
                <HealthcareIcon name="stethoscope" className="w-4 h-4" />
              </div>
              <h4 className="text-xs font-bold text-[#0F172A]">Physical &amp; Nabz Examination</h4>
              <p className="text-xs text-[#64748B] leading-relaxed">
                {condition.assessment.physicalExamination}
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-[#FAFAF7] border border-[#E2E8F0] space-y-2">
              <div className="w-8 h-8 rounded-lg bg-[#E8F5E9] flex items-center justify-center text-[#1B4332]">
                <HealthcareIcon name="heart-pulse" className="w-4 h-4" />
              </div>
              <h4 className="text-xs font-bold text-[#0F172A]">Biomedical Investigations</h4>
              <ul className="text-xs text-[#64748B] space-y-1">
                {condition.assessment.laboratoryInvestigations.map((inv, idx) => (
                  <li key={idx}>- {inv}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* ── 4. 4-STAGE AFAAL TREATMENT CASCADE ────────────────────────── */}
        <div className="bg-[#1B4332] text-white rounded-3xl p-8 sm:p-10 shadow-lg space-y-8">
          <div className="max-w-2xl space-y-1">
            <span className="text-xs font-bold uppercase tracking-wider text-[#A7F3D0]">
              Sequential Therapeutic Methodology
            </span>
            <h2 className="text-xl sm:text-2xl font-extrabold text-white">
              The 4-Stage Afaal Treatment Cascade
            </h2>
            <p className="text-xs text-[#D8F3DC]">
              Disciplined progression ensuring toxins and morbid humors are evacuated before restorative tonics are administered.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-5 rounded-2xl bg-white/10 border border-white/20 space-y-2">
              <span className="text-[10px] font-mono font-bold text-[#A7F3D0]">STAGE 01</span>
              <h4 className="text-xs font-bold text-white">{condition.treatmentApproach.stage1.name}</h4>
              <p className="text-[11px] text-[#B7E4C7] leading-relaxed">
                {condition.treatmentApproach.stage1.description}
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-white/10 border border-white/20 space-y-2">
              <span className="text-[10px] font-mono font-bold text-[#A7F3D0]">STAGE 02</span>
              <h4 className="text-xs font-bold text-white">{condition.treatmentApproach.stage2.name}</h4>
              <p className="text-[11px] text-[#B7E4C7] leading-relaxed">
                {condition.treatmentApproach.stage2.description}
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-white/10 border border-white/20 space-y-2">
              <span className="text-[10px] font-mono font-bold text-[#A7F3D0]">STAGE 03</span>
              <h4 className="text-xs font-bold text-white">{condition.treatmentApproach.stage3.name}</h4>
              <p className="text-[11px] text-[#B7E4C7] leading-relaxed">
                {condition.treatmentApproach.stage3.description}
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-white/10 border border-white/20 space-y-2">
              <span className="text-[10px] font-mono font-bold text-[#A7F3D0]">STAGE 04</span>
              <h4 className="text-xs font-bold text-white">{condition.treatmentApproach.stage4.name}</h4>
              <p className="text-[11px] text-[#B7E4C7] leading-relaxed">
                {condition.treatmentApproach.stage4.description}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-white/20 text-xs">
            <div className="space-y-2">
              <h4 className="font-bold text-[#A7F3D0] uppercase tracking-wider text-[11px]">
                Dietetic Directives (Ilaj bil-Ghiza)
              </h4>
              <ul className="space-y-1.5 text-[#D8F3DC]">
                {condition.treatmentApproach.dietaryDirectives.map((d, idx) => (
                  <li key={idx}>- {d}</li>
                ))}
              </ul>
            </div>

            <div className="space-y-2">
              <h4 className="font-bold text-[#A7F3D0] uppercase tracking-wider text-[11px]">
                Regimenal Therapies (Ilaj bil-Tadbeer)
              </h4>
              <ul className="space-y-1.5 text-[#D8F3DC]">
                {condition.treatmentApproach.regimenalTherapies.map((r, idx) => (
                  <li key={idx}>- {r}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* ── 5. FOLLOW-UP & MONITORING ─────────────────────────────────── */}
        <div className="bg-white rounded-3xl border border-[#E2E8F0] p-8 shadow-sm space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-[#E8F5E9] flex items-center justify-center text-[#1B4332]">
              <HealthcareIcon name="scale" className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-[#0F172A]">Follow-up Schedule &amp; Outcome Monitoring</h3>
              <p className="text-xs text-[#64748B]">{condition.followUp.schedule}</p>
            </div>
          </div>

          <div className="pt-2">
            <h4 className="text-xs font-bold text-[#0F172A] mb-2">Tracked Clinical Biomarkers:</h4>
            <div className="flex flex-wrap gap-2">
              {condition.followUp.biomarkersTracked.map((b, idx) => (
                <span key={idx} className="px-3 py-1 rounded-full text-xs font-semibold bg-[#FAFAF7] border border-[#E2E8F0] text-[#334155]">
                  {b}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* ── 6. EVIDENCE & LIMITATIONS ─────────────────────────────────── */}
        <div className="bg-[#FAFAF7] rounded-3xl border border-[#E2E8F0] p-8 space-y-4">
          <div className="flex items-center gap-2">
            <HealthcareIcon name="shield-check" className="w-5 h-5 text-[#2D6A4F]" />
            <h3 className="text-base font-bold text-[#0F172A]">Scientific Evidence Base &amp; Acknowledged Limitations</h3>
          </div>

          <p className="text-xs sm:text-sm text-[#475569] leading-relaxed">
            {condition.evidenceAndLimitations.summary}
          </p>

          <div className="p-4 rounded-2xl bg-white border border-[#E2E8F0] text-xs text-[#64748B] space-y-1">
            <strong>Clinical Boundary:</strong>
            <p>{condition.evidenceAndLimitations.limitations}</p>
          </div>

          <div className="pt-2">
            <h4 className="text-xs font-bold text-[#0F172A] mb-2">Selected Peer-Reviewed Literature Citations:</h4>
            <ul className="text-[11px] text-[#64748B] space-y-1 font-mono">
              {condition.evidenceAndLimitations.citations.map((cit, idx) => (
                <li key={idx}>[{idx + 1}] {cit}</li>
              ))}
            </ul>
          </div>
        </div>

        {/* ── 7. FAQS ───────────────────────────────────────────────────── */}
        <div className="bg-white rounded-3xl border border-[#E2E8F0] p-8 shadow-sm space-y-4">
          <h3 className="text-lg font-bold text-[#0F172A]">Frequently Asked Clinical Questions</h3>
          <div className="space-y-4">
            {condition.faqs.map((faq, idx) => (
              <div key={idx} className="p-4 rounded-2xl bg-[#FAFAF7] border border-[#E2E8F0] space-y-1.5">
                <h4 className="text-xs font-bold text-[#0F172A]">{faq.question}</h4>
                <p className="text-xs text-[#64748B] leading-relaxed">{faq.answer}</p>
              </div>
            ))}
          </div>
        </div>

        {/* ── 8. DIRECT CLINICAL BOOKING CTA ─────────────────────────────── */}
        <div className="p-8 sm:p-12 rounded-3xl bg-[#1B4332] text-white text-center space-y-4">
          <h3 className="text-2xl sm:text-3xl font-extrabold text-white">
            Begin Your Care for {condition.title}
          </h3>
          <p className="text-xs sm:text-sm text-[#D8F3DC] max-w-xl mx-auto leading-relaxed">
            Consult with a qualified Unani physician registered under the NCISM Act 2020. Receive an individualized clinical evaluation and comprehensive care plan.
          </p>
          <div className="pt-2 flex flex-wrap items-center justify-center gap-3">
            <Link
              href={`/book?condition=${condition.slug}`}
              className="px-6 py-3 rounded-xl bg-white text-[#1B4332] font-semibold text-xs hover:bg-[#F8FAFC] transition shadow-sm"
            >
              Book Clinical Consultation
            </Link>
            <Link
              href="/doctors"
              className="px-6 py-3 rounded-xl bg-[#2D6A4F] text-white font-semibold text-xs hover:bg-[#40916C] transition"
            >
              View Specialized Clinicians
            </Link>
          </div>
        </div>

      </div>
    </PublicWebsiteShell>
  );
}
