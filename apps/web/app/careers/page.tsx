import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";

export const metadata = {
  title: "Careers at ZAYVORA Health™ | Clinical & Technology Roles",
  description: "Join ZAYVORA Health™ in advancing the future of integrative medicine, AI safety, botanical pharmacology, and healthcare software architecture.",
};

export default function CareersPage() {
  const openings = [
    {
      title: "Senior Consultant Tabeeb / Integrative Physician",
      division: "Clinical Directorate",
      type: "Full-Time (New Delhi)",
      description: "Leading patient consultations, 10-Ajnas pulse diagnosis, and supervising individualized Nuskha formulations at ZAYVORA Matab™.",
      requirements: ["BUMS / MD in Unani Medicine", "Min 5 years clinical OPD experience", "Familiarity with digital EHR platforms"]
    },
    {
      title: "Clinical AI Safety & Knowledge Engineer",
      division: "Informatics & AI",
      type: "Full-Time / Hybrid",
      description: "Curating classical Unani medical taxonomies, fine-tuning retrieval graphs, and building guardrail evaluators for Hakeem Sahab AI™.",
      requirements: ["Background in Health Informatics or Computational Linguistics", "Experience with Neo4j / vector search", "Understanding of traditional medical concepts"]
    },
    {
      title: "Lead Cleanroom QC Pharmacist",
      division: "Research & Manufacturing",
      type: "Full-Time (Okhla Cleanroom Facility)",
      description: "Overseeing AYUSH-GMP batch documentation, HPTLC raw botanical fingerprinting, and Mudabbar detoxification compliance.",
      requirements: ["B.Pharm / M.Pharm (Ayurveda/Unani/Pharmacognosy)", "Experience with 21 CFR Part 11 electronic batch records", "Min 3 years cleanroom QC experience"]
    }
  ];

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Join Our Team"
        title="Careers at ZAYVORA Health™"
        subtitle="Shape the next generation of evidence-based traditional medicine, clinician-centered AI, and enterprise healthcare software."
        breadcrumbs={[{ label: "Careers" }]}
        primaryCta={{ label: "View Open Positions", href: "#positions" }}
        secondaryCta={{ label: "About Our Culture", href: "/about" }}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-16">
        <section className="text-center max-w-3xl mx-auto">
          <span className="text-xs font-bold uppercase tracking-wider text-[#0D9488]">Why Work at ZAYVORA</span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-2">
            Where Ancient Wisdom Meets Cutting-Edge Engineering
          </h2>
          <p className="mt-4 text-[#94A3B8] text-sm leading-relaxed">
            At ZAYVORA, we bring together clinical tabeebs, clinical trial researchers, software engineers, and botanical chemists. We offer a high-impact mission, competitive compensation, continuing medical education support, and comprehensive health coverage.
          </p>
        </section>

        <section id="positions" className="space-y-6">
          <h3 className="text-xl font-bold text-white mb-6">Current Openings</h3>
          <div className="grid grid-cols-1 gap-6">
            {openings.map((job, idx) => (
              <div key={idx} className="p-6 sm:p-8 rounded-2xl bg-[#0D1527] border border-[#1E293B] hover:border-[#0D9488]/40 transition flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div>
                  <div className="flex flex-wrap items-center gap-3 mb-2">
                    <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-[#1E293B] text-[#5EEAD4] border border-[#334155]">
                      {job.division}
                    </span>
                    <span className="text-xs text-[#94A3B8]">{job.type}</span>
                  </div>
                  <h4 className="text-lg font-bold text-white">{job.title}</h4>
                  <p className="text-xs sm:text-sm text-[#94A3B8] mt-2 max-w-2xl">{job.description}</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {job.requirements.map((req, rIdx) => (
                      <span key={rIdx} className="text-[11px] px-2 py-0.5 rounded bg-[#0A0F1D] text-[#CBD5E1] border border-[#1E293B]">
                        • {req}
                      </span>
                    ))}
                  </div>
                </div>
                <Link
                  href="/contact"
                  className="px-5 py-2.5 rounded-xl bg-[#0D9488] hover:bg-[#0F766E] text-white font-bold text-xs shadow-md shrink-0 text-center transition"
                >
                  Apply Now →
                </Link>
              </div>
            ))}
          </div>
        </section>

        <section className="p-8 rounded-3xl bg-[#0A0F1D] border border-[#1E293B] text-center max-w-2xl mx-auto">
          <h3 className="text-lg font-bold text-white">Don't See Your Role?</h3>
          <p className="mt-2 text-xs text-[#94A3B8] leading-relaxed">
            We are always looking for exceptional medical minds, healthcare software architects, and clinical researchers. Send your CV and portfolio directly to <strong className="text-white">careers@zayvorahealth.com</strong>.
          </p>
        </section>
      </div>
    </PublicWebsiteShell>
  );
}
