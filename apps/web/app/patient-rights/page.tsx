import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export const metadata = {
  title: "Patient Rights & Clinical Consents | ZAYVORA Health™",
  description: "Statutory patient rights, clinical informed consent, health data privacy under DPDP Act 2023, and institutional grievance access.",
};

export default function PatientRightsPage() {
  const rights = [
    {
      title: "Right to Informed Clinical Consent",
      desc: "You are entitled to a full explanation of your constitutional temperament (Mizaj), the proposed treatment cascade, expected timelines, dietary restrictions (Parhez), and potential detoxification reactions before initiating any care protocol."
    },
    {
      title: "Right to Complete Health Record Access",
      desc: "You retain full ownership of your Personal Health Record (PHR). All clinical SOAP notes, pulse waveform recordings, digital prescriptions, and laboratory reports are accessible via the Patient Portal at zero administrative fee."
    },
    {
      title: "Right to Data Privacy & Non-Commercialization",
      desc: "Under the Digital Personal Data Protection (DPDP) Act 2023, your diagnostic history and consultations are end-to-end encrypted. We will never share or sell your clinical data to insurers, data aggregators, or marketing firms."
    },
    {
      title: "Right to Botanical Formulation Transparency",
      desc: "You have the right to know every ingredient in any dispensed formulation, its classical pharmacopoeial origin (UPI/NFUM), batch testing Certificate of Analysis (CoA), and Mudabbar purification status."
    }
  ];

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Patient-Centered Healthcare"
        title="Patient Rights & Clinical Consents"
        subtitle="Our statutory charter guaranteeing dignity, informed decision-making, health data sovereignty, and ethical care delivery under Indian law."
        breadcrumbs={[{ label: "Patient Rights" }]}
      />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8">
        <div className="bg-white rounded-3xl border border-slate-200/90 p-8 sm:p-10 shadow-sm space-y-6">
          <div className="border-b border-slate-100 pb-4">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Ethical Charter</span>
            <h2 className="text-xl font-bold text-[#0F172A] mt-1">ZAYVORA Patient Bill of Rights</h2>
          </div>

          <div className="space-y-6">
            {rights.map((r, idx) => (
              <div key={idx} className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
                <div className="flex items-center gap-2">
                  <HealthcareIcon name="check" className="w-4 h-4 text-emerald-700 shrink-0" />
                  <h3 className="font-bold text-sm text-[#0F172A]">{r.title}</h3>
                </div>
                <p className="text-xs sm:text-sm text-slate-600 leading-relaxed pl-6">{r.desc}</p>
              </div>
            ))}
          </div>

          <div className="pt-6 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Charter Review: Annual • Statutory NCISM Compliance</span>
            <Link href="/grievance" className="text-emerald-800 font-bold hover:underline">
              File a Care Concern or Grievance →
            </Link>
          </div>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}
