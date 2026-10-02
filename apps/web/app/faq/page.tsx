import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { FaqAccordion } from "@/components/website/FaqAccordion";
import { faqsData } from "@/lib/data/faqs";

export const metadata = {
  title: "Frequently Asked Questions | ZAYVORA Health™",
  description: "Find answers regarding ZAYVORA Matab consultations, constitutional Mizaj, Hakeem Sahab AI safety guardrails, and botanical formulation standards.",
};

export default function FaqPage() {
  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Clinical Knowledge Hub"
        title="Frequently Asked Questions"
        subtitle="Transparent answers regarding our clinical Unani care model, diagnostic methods, AI safety governance, and botanical pharmaceutical quality."
        breadcrumbs={[{ label: "FAQ" }]}
        primaryCta={{ label: "Contact Clinical Team", href: "/contact" }}
        secondaryCta={{ label: "Explore Clinical Care", href: "/services/clinical-care" }}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-16">
        <FaqAccordion items={faqsData} showCategoryFilter={true} />

        {/* Still have questions callout */}
        <section className="p-8 rounded-3xl bg-[#0D1527] border border-[#1E293B] text-center max-w-2xl mx-auto">
          <h3 className="text-xl font-bold text-white">Still Have Clinical Questions?</h3>
          <p className="mt-2 text-xs text-[#94A3B8] leading-relaxed">
            Our clinical duty tabeebs and care coordinators are available to answer your inquiries regarding treatment protocols, dietary guidelines, or teleconsultations.
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-4">
            <Link
              href="/contact"
              className="px-6 py-2.5 rounded-xl bg-[#0D9488] hover:bg-[#0F766E] text-white font-bold text-xs shadow-md transition"
            >
              Submit an Inquiry →
            </Link>
            <a
              href="tel:+919773882657"
              className="px-6 py-2.5 rounded-xl bg-[#1E293B] hover:bg-[#334155] border border-[#334155] text-[#CBD5E1] font-bold text-xs transition"
            >
              Call Helpline: +91 97738 82657
            </a>
          </div>
        </section>
      </div>
    </PublicWebsiteShell>
  );
}
