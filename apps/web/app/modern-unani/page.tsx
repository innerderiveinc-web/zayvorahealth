import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export const metadata = {
  title: "Unani Medicine Foundations & Contemporary Science | ZAYVORA Health™",
  description: "Explore the scientific foundations of Greco-Arab Unani medicine (Tibb-e-Unani): Mizaj, Akhlat, Asbab-e-Sittah, and evidence-based analytical standardisation.",
};

export default function ModernUnaniPage() {
  const pillars = [
    {
      title: "Mizaj (Constitutional Temperament)",
      desc: "The unique biochemical and physiological equilibrium of an individual, categorised through Damawi (sanguine), Balghami (phlegmatic), Safrawi (choleric), and Saudawi (melancholic) states."
    },
    {
      title: "Akhlat (Four Humors)",
      desc: "The fluids circulating within the body (Dam/Blood, Balgham/Phlegm, Safra/Yellow Bile, Sauda/Black Bile) that sustain cellular nutrition, immune defence, and organ integrity."
    },
    {
      title: "Tabi'at (Innate Healing Intelligence)",
      desc: "The internal physiological self-regulatory mechanism of the human body. The clinician's primary task is to empower Tabi'at rather than replace it."
    },
    {
      title: "Asbab-e-Sittah Zarooriyyah (6 Health Essentials)",
      desc: "The six environmental and lifestyle determinants that determine homeostasis: ambient air, diet, physical activity, sleep, evacuation/retention, and psychological equilibrium."
    }
  ];

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Classical Canon & Modern Science"
        title="Unani Medicine Foundations"
        subtitle="Uniting two millennia of clinical Greco-Arab humoral physiology with contemporary molecular diagnostics, analytical phytochemistry, and clinician-governed informatics."
        breadcrumbs={[{ label: "Unani Medicine Foundations" }]}
        primaryCta={{ label: "Explore Health Library", href: "/health-library" }}
        secondaryCta={{ label: "Consult Senior Tabeeb", href: "/contact" }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">
        
        {/* Core Philosophy Section */}
        <section className="bg-white rounded-3xl border border-slate-200/90 p-8 sm:p-10 shadow-sm space-y-6">
          <div className="max-w-3xl space-y-3">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Philosophical Doctrine</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A]">A Systemic Science of Individualized Equilibrium</h2>
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              Unani medicine (Tibb-e-Unani) is a comprehensive medical system originating from Hippocrates, Galen, and codified by Ibn Sina (Avicenna) in *The Canon of Medicine* (Al-Qanun fi al-Tibb). In statutory Indian healthcare, it is recognized under the National Commission for Indian System of Medicine (NCISM) Act 2020.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-slate-100">
            {pillars.map((p, idx) => (
              <div key={idx} className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
                <div className="flex items-center gap-2">
                  <HealthcareIcon name="shield-check" className="w-4 h-4 text-emerald-700" />
                  <h3 className="font-bold text-sm text-[#0F172A]">{p.title}</h3>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">{p.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* The 4-Stage Afaal Cascade */}
        <section className="space-y-8">
          <div className="text-center max-w-2xl mx-auto space-y-2">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Therapeutic Logic</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A]">The 4-Stage Afaal Clinical Cascade</h2>
            <p className="text-xs sm:text-sm text-slate-500">Unani therapeutics are never applied haphazardly; treatments proceed through sequential physiological stages:</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-white rounded-3xl border border-slate-200/90 p-6 shadow-sm space-y-3">
              <span className="text-2xl font-mono font-extrabold text-emerald-800">01</span>
              <h3 className="font-bold text-sm text-[#0F172A]">Tanqiya (Humoral Cleansing)</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Eliminating morbid matter (Madda Fasida) through targeted purgatives (Mushil), diuresis (Idrar), or therapeutic cupping (Hijama).
              </p>
            </div>

            <div className="bg-white rounded-3xl border border-slate-200/90 p-6 shadow-sm space-y-3">
              <span className="text-2xl font-mono font-extrabold text-emerald-800">02</span>
              <h3 className="font-bold text-sm text-[#0F172A]">Tahleel (Resolution of Inflammation)</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Resolving local congestion, synovial effusions, or mucosal stagnation with anti-inflammatory Mudabbar botanical formulations.
              </p>
            </div>

            <div className="bg-white rounded-3xl border border-slate-200/90 p-6 shadow-sm space-y-3">
              <span className="text-2xl font-mono font-extrabold text-emerald-800">03</span>
              <h3 className="font-bold text-sm text-[#0F172A]">Taqwiyat (Organ Tonification)</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Strengthening principal organs (Heart, Brain, Liver) with specialized adaptogens and nutritional compounds (Muqawwiyat).
              </p>
            </div>

            <div className="bg-white rounded-3xl border border-slate-200/90 p-6 shadow-sm space-y-3">
              <span className="text-2xl font-mono font-extrabold text-emerald-800">04</span>
              <h3 className="font-bold text-sm text-[#0F172A]">Hifz (Longitudinal Maintenance)</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Preserving constitutional equilibrium through personalized dietary regimens (Parhez) and lifestyle hygiene (Hifzan-e-Sehat).
              </p>
            </div>
          </div>
        </section>

        {/* Contemporary Analytical Standardisation */}
        <section className="bg-white rounded-3xl border border-slate-200/90 p-8 sm:p-10 shadow-sm space-y-6">
          <div className="border-b border-slate-100 pb-4">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Phytochemical Integrity</span>
            <h3 className="text-xl font-bold text-[#0F172A] mt-1">Bridging Classical Codification with Modern Analytical Sciences</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-600">
            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <div className="flex items-center gap-2 text-emerald-800">
                <HealthcareIcon name="flask" className="w-5 h-5 text-emerald-700" />
                <span className="font-bold text-sm text-[#0F172A]">HPTLC Fingerprinting</span>
              </div>
              <p className="leading-relaxed">Every botanical lot is fingerprinted for active phytocompounds (such as colchicine in Colchicum luteum or withanolides in Withania somnifera).</p>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <div className="flex items-center gap-2 text-teal-800">
                <HealthcareIcon name="shield-check" className="w-5 h-5 text-teal-700" />
                <span className="font-bold text-sm text-[#0F172A]">Schedule E(1) Mudabbar</span>
              </div>
              <p className="leading-relaxed">Potent classical botanical substances undergo statutory detox regimens verified through laboratory Certificate of Analysis (CoA) before pharmacy dispensing.</p>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <div className="flex items-center gap-2 text-amber-800">
                <HealthcareIcon name="activity" className="w-5 h-5 text-amber-700" />
                <span className="font-bold text-sm text-[#0F172A]">Dual Diagnostics</span>
              </div>
              <p className="leading-relaxed">Clinical evaluations correlate classical 10-Ajnas pulse (Nabz) and tongue (Lisan) inspection with modern inflammatory markers (hs-CRP, ESR) and metabolic panels.</p>
            </div>
          </div>
        </section>

      </div>
    </PublicWebsiteShell>
  );
}
