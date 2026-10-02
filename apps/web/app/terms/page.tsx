import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export const metadata = {
  title: "Terms of Clinical Service | ZAYVORA Health™",
  description: "Statutory terms of clinical service, telehealth consent, electronic prescription boundaries, and patient rights under NCISM Act 2020 and DPDP Act 2023.",
};

export default function TermsPage() {
  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Statutory Legal Agreement"
        title="Terms of Clinical Service"
        subtitle="Operational, clinical governance, and telemedicine service terms governing patient encounters, teleconsultations, and pharmaceutical dispensations."
        breadcrumbs={[{ label: "Terms of Service" }]}
      />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8 text-xs sm:text-sm text-slate-700 leading-relaxed">
        
        <div className="bg-white rounded-3xl border border-slate-200/90 p-8 sm:p-10 shadow-sm space-y-6">
          
          <section className="space-y-3">
            <h2 className="text-lg font-bold text-[#0F172A] flex items-center gap-2">
              <HealthcareIcon name="shield-check" className="w-5 h-5 text-emerald-700" />
              <span>1. Clinician Governance & Prescribing Discretion</span>
            </h2>
            <p>
              All consultations, examinations, and prescriptions (Nuskha) provided via ZAYVORA Health™ are conducted exclusively by licensed Unani practitioners registered under the National Commission for Indian System of Medicine (NCISM) Act 2020. Every prescription requires the independent clinical discretion and non-delegable electronic signature of the attending Tabeeb in compliance with 21 CFR Part 11 and the Information Technology Act 2000.
            </p>
          </section>

          <section className="space-y-3 border-t border-slate-100 pt-6">
            <h2 className="text-lg font-bold text-[#0F172A] flex items-center gap-2">
              <HealthcareIcon name="alert-triangle" className="w-5 h-5 text-red-600" />
              <span>2. Emergency Medical Boundaries</span>
            </h2>
            <p>
              ZAYVORA Health™ teleconsultation services are designed strictly for chronic disease management, constitutional optimization, and elective outpatient follow-up. <strong>They are not intended for acute medical emergencies.</strong> If you experience severe chest pain, shortness of breath, sudden neurological deficits, or uncontrolled trauma, you must immediately contact national emergency services at 112 or visit the nearest hospital casualty unit.
            </p>
          </section>

          <section className="space-y-3 border-t border-slate-100 pt-6">
            <h2 className="text-lg font-bold text-[#0F172A] flex items-center gap-2">
              <HealthcareIcon name="lock" className="w-5 h-5 text-teal-700" />
              <span>3. Digital Privacy & Health Data Rights (DPDP Act 2023)</span>
            </h2>
            <p>
              All personal health records, diagnostic uploads, and clinical encounter notes are protected in accordance with the Digital Personal Data Protection (DPDP) Act 2023. Patient data is encrypted in transit and at rest. We never sell, rent, or monetize sensitive personal health information to third-party advertisers or insurance brokers without statutory court orders.
            </p>
          </section>

          <section className="space-y-3 border-t border-slate-100 pt-6">
            <h2 className="text-lg font-bold text-[#0F172A] flex items-center gap-2">
              <HealthcareIcon name="pill" className="w-5 h-5 text-amber-700" />
              <span>4. Dispensary & Schedule E(1) Mudabbar Compliance</span>
            </h2>
            <p>
              Formulations containing potent botanical or mineral substances (Schedule E(1) of the Drugs and Cosmetics Act 1940) require explicit Mudabbar purification verification prior to dispensing. ZAYVORA cleanroom facilities adhere to Good Manufacturing Practice (GMP) standards.
            </p>
          </section>

          <div className="pt-6 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Last Updated: September 2026 • Version 5.2</span>
            <Link href="/contact" className="text-emerald-800 font-bold hover:underline">
              Questions? Contact Legal & Grievance Desk
            </Link>
          </div>

        </div>

      </div>
    </PublicWebsiteShell>
  );
}
