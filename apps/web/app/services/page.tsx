import React from "react";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { ServiceCard } from "@/components/website/ServiceCard";
import { servicesData } from "@/lib/data/services";

export const metadata = {
  title: "Clinical & Digital Healthcare Services",
  description: "Explore the 7 core healthcare services provided by ZAYVORA Health OS™, spanning clinical Matab care, Hakeem Sahab AI, digital health EHR, cleanroom manufacturing, and research.",
};

export default function ServicesOverviewPage() {
  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Enterprise Healthcare Ecosystem"
        title="Comprehensive Clinical & Technological Services"
        subtitle="Bridging classical bedside Unani care with contemporary digital health, pharmaceutical manufacturing, and real-world evidence research."
        breadcrumbs={[{ label: "Services" }]}
        primaryCta={{ label: "Consult a Tabeeb", href: "/contact" }}
        secondaryCta={{ label: "View Products", href: "/products" }}
      />

      <section className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {servicesData.map((service) => (
            <ServiceCard key={service.id} service={service} />
          ))}
        </div>
      </section>
    </PublicWebsiteShell>
  );
}
