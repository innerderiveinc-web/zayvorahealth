import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { termsConditionsData } from "@/lib/data/legal";

export const metadata = {
  title: "Terms and Conditions | ZAYVORA Health™",
  description: "Terms and conditions governing clinical consultations, teleconsultations, electronic health records, and the ZAYVORA Health OS™ platform.",
};

export default function TermsConditionsPage() {
  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Legal & Terms"
        title={termsConditionsData.title}
        subtitle="Terms of use governing clinical care services, electronic pharmacy fulfillment, and access to the ZAYVORA digital ecosystem."
        breadcrumbs={[{ label: "Terms & Conditions" }]}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto space-y-12">
        <div className="flex items-center justify-between text-xs text-[#64748B] border-b border-[#1E293B] pb-4">
          <span>Effective Date: <strong className="text-[#CBD5E1]">{termsConditionsData.lastUpdated}</strong></span>
          <span>Version: <strong className="text-[#CBD5E1]">{termsConditionsData.version}</strong></span>
        </div>

        <div className="space-y-10">
          {termsConditionsData.sections.map((sec, idx) => (
            <div key={idx} className="space-y-3">
              <h2 className="text-xl font-bold text-white tracking-tight">{sec.heading}</h2>
              {sec.content.map((p, pIdx) => (
                <p key={pIdx} className="text-sm text-[#94A3B8] leading-relaxed">
                  {p}
                </p>
              ))}
            </div>
          ))}
        </div>

        <div className="pt-8 border-t border-[#1E293B] flex items-center justify-between text-xs">
          <Link href="/privacy-policy" className="text-[#5EEAD4] hover:underline font-semibold">
            ← View Privacy Policy
          </Link>
          <Link href="/contact" className="text-[#94A3B8] hover:text-white">
            Legal Inquiries
          </Link>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}
