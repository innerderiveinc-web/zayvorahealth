import React from "react";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { ContactForm } from "@/components/website/ContactForm";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { siteConfig } from "@/lib/data/siteConfig";

export const metadata = {
  title: "Contact ZAYVORA Health™ | Central Care Centre & Matab Inquiries",
  description: "Get in touch with ZAYVORA Health™ for clinical appointments, teleconsultation inquiries, cleanroom formulation partnerships, or clinical trial collaborations.",
};

export default function ContactPage() {
  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Direct Communication"
        title="Contact ZAYVORA Health™"
        subtitle="Connect with our clinical care desk, attending Tabeebs, cleanroom manufacturing team, or research informatics coordinators."
        breadcrumbs={[{ label: "Contact Us" }]}
      />

      <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
          
          {/* Left Column: Direct Contact & Facility Details */}
          <div className="space-y-6">
            <div className="p-7 rounded-3xl bg-white border border-slate-200/90 shadow-sm space-y-3">
              <div className="flex items-center gap-2">
                <HealthcareIcon name="hospital" className="w-5 h-5 text-emerald-700" />
                <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">Central Healthcare Complex</span>
              </div>
              <h3 className="text-lg font-bold text-[#0F172A]">{siteConfig.address.facility}</h3>
              <p className="text-xs text-emerald-700 font-medium">{siteConfig.address.wing}</p>
              <p className="text-xs text-slate-600 leading-relaxed pt-1">
                {siteConfig.address.street}<br />
                {siteConfig.address.city}, {siteConfig.address.state} - {siteConfig.address.postalCode}<br />
                {siteConfig.address.country}
              </p>
            </div>

            <div className="p-7 rounded-3xl bg-white border border-slate-200/90 shadow-sm space-y-4">
              <div className="flex items-center gap-2">
                <HealthcareIcon name="phone" className="w-5 h-5 text-teal-700" />
                <span className="text-[11px] font-bold uppercase tracking-wider text-[#2D6A4F]">Direct Clinical Helpline</span>
              </div>
              
              <div>
                <p className="text-xs text-slate-400 font-medium">Toll-Free Patient Helpline:</p>
                <p className="text-base font-extrabold text-[#0F172A] mt-0.5">{siteConfig.contact.helpline}</p>
              </div>

              <div>
                <p className="text-xs text-slate-400 font-medium">OPD Appointment Desk:</p>
                <p className="text-sm font-bold text-slate-800 mt-0.5">{siteConfig.contact.opdPhone}</p>
              </div>

              <div className="pt-2 border-t border-slate-100">
                <p className="text-xs text-slate-400 font-medium">General & Clinical Email:</p>
                <a href={`mailto:${siteConfig.contact.email}`} className="text-xs font-semibold text-emerald-700 hover:underline block mt-0.5">
                  {siteConfig.contact.email}
                </a>
              </div>

              <div>
                <p className="text-xs text-slate-400 font-medium">Patient Support Desk:</p>
                <a href={`mailto:${siteConfig.contact.supportEmail}`} className="text-xs font-semibold text-emerald-700 hover:underline block mt-0.5">
                  {siteConfig.contact.supportEmail}
                </a>
              </div>
            </div>

            <div className="p-7 rounded-3xl bg-white border border-slate-200/90 shadow-sm space-y-3">
              <div className="flex items-center gap-2">
                <HealthcareIcon name="clock" className="w-5 h-5 text-amber-700" />
                <span className="text-[11px] font-bold uppercase tracking-wider text-amber-800">OPD Clinic Hours</span>
              </div>
              <div className="space-y-2 text-xs text-slate-600">
                <div className="flex justify-between border-b border-slate-100 pb-1.5">
                  <span>Monday – Friday:</span>
                  <strong className="text-slate-900">09:00 AM – 06:00 PM</strong>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-1.5">
                  <span>Saturday:</span>
                  <strong className="text-slate-900">09:00 AM – 02:00 PM</strong>
                </div>
                <div className="flex justify-between">
                  <span>Sunday & Holidays:</span>
                  <strong className="text-red-700">Closed (Teleconsult On-Call)</strong>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Interactive Contact & Inquiry Form */}
          <div className="lg:col-span-2">
            <ContactForm />
          </div>

        </div>
      </div>
    </PublicWebsiteShell>
  );
}
