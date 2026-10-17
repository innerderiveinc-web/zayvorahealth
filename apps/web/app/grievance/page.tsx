import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export const metadata = {
  title: "Grievance Redressal & Patient Advocacy | ZAYVORA Health™",
  description: "Statutory grievance redressal mechanism, clinical concern filing, DPDP Act 2023 data officer, and escalation protocols.",
};

export default function GrievancePage() {
  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Statutory Accountability"
        title="Grievance Redressal & Patient Advocacy"
        subtitle="Every patient concern, clinical inquiry, or data privacy request is handled with strict confidentiality, structured SLAs, and direct oversight by our Clinical Ethics Board."
        breadcrumbs={[{ label: "Grievance Redressal" }]}
      />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8">
        <div className="bg-white rounded-3xl border border-slate-200/90 p-8 sm:p-10 shadow-sm space-y-6">
          
          <div className="space-y-3">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Prompt Resolution</span>
            <h2 className="text-xl font-bold text-[#0F172A]">Statutory Redressal Commitment</h2>
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              In accordance with the Consumer Protection (E-Commerce) Rules 2020, the Telemedicine Practice Guidelines, and the Digital Personal Data Protection (DPDP) Act 2023, ZAYVORA Health™ provides an expedited grievance redressal mechanism. All formal grievances are acknowledged within 24 hours and addressed within 15 business days.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-4">
            <h3 className="text-sm font-bold text-[#0F172A] uppercase tracking-wider">Designated Grievance & Data Protection Officer</h3>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <span className="text-slate-400 block font-medium">Officer Name:</span>
                <strong className="text-slate-900 text-sm">Dr. N. K. Siddiqui</strong>
                <span className="text-[11px] text-slate-500 block">Senior Clinical Ombudsman & Ethics Lead</span>
              </div>

              <div>
                <span className="text-slate-400 block font-medium">Direct Grievance Email:</span>
                <a href="mailto:grievance@zayvorahealth.com" className="text-emerald-700 font-bold hover:underline">
                  grievance@zayvorahealth.com
                </a>
                <span className="text-[11px] text-slate-500 block">Confidential / Priority Routing</span>
              </div>

              <div>
                <span className="text-slate-400 block font-medium">Helpline Telephone:</span>
                <span className="text-slate-900 font-semibold">+91 97738 82657 (Ext. 402)</span>
              </div>

              <div>
                <span className="text-slate-400 block font-medium">Physical Address:</span>
                <span className="text-slate-700">Ombudsman Office, ZAYVORA Health Complex, Okhla Phase III, New Delhi - 110020</span>
              </div>
            </div>
          </div>

          <div className="space-y-3 pt-2">
            <h3 className="text-sm font-bold text-[#0F172A]">Grievance Escalation Process</h3>
            <ol className="space-y-2 text-xs text-slate-600 list-decimal pl-5">
              <li><strong>Step 1: Filing:</strong> Submit your concern via email to grievance@zayvorahealth.com or through the contact form with category "Grievance".</li>
              <li><strong>Step 2: Acknowledgment:</strong> A unique ticket tracking number is issued within 24 hours with an assigned clinical investigator.</li>
              <li><strong>Step 3: Clinical Review:</strong> If related to clinical consultation or prescription posology, the matter is reviewed by an independent senior tabeeb not involved in the original encounter.</li>
              <li><strong>Step 4: Formal Resolution:</strong> A written resolution notice is provided to the patient within 15 business days.</li>
            </ol>
          </div>

          <div className="pt-6 border-t border-slate-100 flex items-center justify-between text-xs">
            <Link href="/contact" className="text-emerald-800 font-bold hover:underline">
              Submit Direct Inquiry Online →
            </Link>
            <Link href="/patient-rights" className="text-slate-500 hover:text-slate-900">
              Review Patient Bill of Rights
            </Link>
          </div>

        </div>
      </div>
    </PublicWebsiteShell>
  );
}
