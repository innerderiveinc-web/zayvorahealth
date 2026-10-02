import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { privacyPolicyData } from "@/lib/data/legal";

export const metadata = {
  title: "Privacy Policy | ZAYVORA Health™",
  description: "ZAYVORA Health™ privacy policy detailing personal health data protection, DPDP and ABDM compliance, encryption, and patient confidentiality.",
};

export default function PrivacyPolicyPage() {
  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Legal & Privacy"
        title={privacyPolicyData.title}
        subtitle="Our commitment to safeguarding patient confidentiality, protected health information (PHI), and cryptographic electronic records."
        breadcrumbs={[{ label: "Privacy Policy" }]}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto space-y-12">
        <div className="flex items-center justify-between text-xs text-[#64748B] border-b border-[#1E293B] pb-4">
          <span>Effective Date: <strong className="text-[#CBD5E1]">{privacyPolicyData.lastUpdated}</strong></span>
          <span>Version: <strong className="text-[#CBD5E1]">{privacyPolicyData.version}</strong></span>
        </div>

        <div className="space-y-10">
          {privacyPolicyData.sections.map((sec, idx) => (
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
          <Link href="/terms-and-conditions" className="text-[#5EEAD4] hover:underline font-semibold">
            View Terms and Conditions →
          </Link>
          <Link href="/contact" className="text-[#94A3B8] hover:text-white">
            Contact Data Protection Officer
          </Link>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}
