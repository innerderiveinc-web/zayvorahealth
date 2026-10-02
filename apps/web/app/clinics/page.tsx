import React from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export const metadata = {
  title: "Clinical Facilities & Matabs | ZAYVORA Health™",
  description: "Locate certified ZAYVORA Matab™ clinical facilities, outpatient departments, and specialized regimenal therapy (Ilaj bil-Tadbeer) centers.",
};

const CLINIC_FACILITIES = [
  {
    id: "FAC-CENTRAL-DELHI",
    name: "ZAYVORA Matab™ Central Care Centre",
    city: "New Delhi",
    address: "Block B, Institutional Area, Near Okhla Phase III, New Delhi - 110020",
    phone: "+91 97738 82657",
    hours: "Mon – Sat: 09:00 AM – 06:00 PM IST",
    clinicalDirector: "Hakeem Dr. Irfan Ashraf (Chief Medical Officer)",
    features: [
      "10-Ajnas Arterial Pulse Diagnostic Laboratory",
      "Ilaj bil-Tadbeer Regimenal Suite (Hijama, Dalk, Abzen)",
      "Automated FEFO Botanical Dispensary & Cold-Chain",
      "On-site Biochemical & Synovial Pathology Collection"
    ],
    status: "Active OPD"
  },
  {
    id: "FAC-MUMBAI-REGIONAL",
    name: "ZAYVORA Matab™ Western Regional Centre",
    city: "Mumbai",
    address: "Healthcare Pavilion, Bandra Kurla Complex (BKC), Mumbai, Maharashtra - 400051",
    phone: "+91 22 4890 1200",
    hours: "Mon – Fri: 09:30 AM – 05:30 PM IST",
    clinicalDirector: "Dr. Fatima Zahra (Consultant Physician)",
    features: [
      "Women's Health & Pelvic Circulation Care (Amraz-e-Niswan)",
      "Metabolic Syndrome & Circadian Dietetics (Ilaj bil-Ghiza)",
      "Schedule E(1) Mudabbar Dispensary Counter",
      "Teleconsultation & Remote Patient Triage Studio"
    ],
    status: "Active OPD"
  },
  {
    id: "FAC-HYDERABAD-SOUTH",
    name: "ZAYVORA Matab™ Southern Regional Facility",
    city: "Hyderabad",
    address: "Life Sciences District, Gachibowli, Hyderabad, Telangana - 500032",
    phone: "+91 40 6789 3300",
    hours: "Tue – Sun: 09:00 AM – 05:00 PM IST",
    clinicalDirector: "Dr. Zainab Al-Husseini (Pharmacognosy & GI Lead)",
    features: [
      "Gastrointestinal & Gut-Brain Axis Specialty (Zoaf-e-Meda)",
      "Botanical Standardisation & HPLC Assay Laboratory",
      "Psoriasis & Autoimmune Skin Care Protocol Suite",
      "Emergency Triage & Ambulatory Referrals"
    ],
    status: "Active OPD"
  }
];

export default function ClinicsPage() {
  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="Physical Care Network"
        title="ZAYVORA Matab™ Clinical Facilities"
        subtitle="Explore our certified outpatient healthcare complexes, specialized regimenal therapy suites, and accredited cleanroom dispensaries across India."
        breadcrumbs={[{ label: "Care Centers & Matabs" }]}
        primaryCta={{ label: "Book Facility OPD Slot", href: "/contact" }}
        secondaryCta={{ label: "Meet Clinical Faculty", href: "/doctors" }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
        
        {/* Network Standards Callout */}
        <div className="bg-white rounded-3xl border border-slate-200/90 p-8 shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-600">
            <div className="flex items-start gap-3.5">
              <div className="w-10 h-10 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-800 shrink-0">
                <HealthcareIcon name="hospital" className="w-5 h-5 text-emerald-700" />
              </div>
              <div>
                <h4 className="font-bold text-sm text-[#0F172A]">Standardized Regimenal Suites</h4>
                <p className="mt-1 leading-relaxed text-slate-500">
                  Dedicated sterile chambers for classical Ilaj bil-Tadbeer procedures (wet and dry cupping, therapeutic massage, steam fomentation).
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3.5">
              <div className="w-10 h-10 rounded-2xl bg-teal-50 border border-teal-200 flex items-center justify-center text-[#2D6A4F] shrink-0">
                <HealthcareIcon name="pill" className="w-5 h-5 text-[#2D6A4F]" />
              </div>
              <div>
                <h4 className="font-bold text-sm text-[#0F172A]">On-Site Cleanroom Dispensaries</h4>
                <p className="mt-1 leading-relaxed text-slate-500">
                  Formulations dispensed under strict FEFO protocols with Schedule E(1) Mudabbar detoxification certificates.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3.5">
              <div className="w-10 h-10 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-700 shrink-0">
                <HealthcareIcon name="shield-check" className="w-5 h-5 text-slate-600" />
              </div>
              <div>
                <h4 className="font-bold text-sm text-[#0F172A]">Federated Health Record</h4>
                <p className="mt-1 leading-relaxed text-slate-500">
                  Seamless care continuum between in-person Matab appointments and digital follow-ups across all centers.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Facilities List */}
        <div className="space-y-8">
          {CLINIC_FACILITIES.map((facility) => (
            <div
              key={facility.id}
              className="bg-white rounded-3xl border border-slate-200/90 p-7 sm:p-8 shadow-sm hover:shadow-md hover:border-emerald-600/40 transition space-y-6"
            >
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-100 pb-5">
                <div>
                  <div className="flex items-center gap-2.5 flex-wrap">
                    <h3 className="text-xl font-bold text-[#0F172A]">{facility.name}</h3>
                    <span className="px-2.5 py-0.5 rounded-full bg-emerald-50 text-[#1B4332] border border-emerald-200 font-bold text-[10px]">
                      {facility.status}
                    </span>
                  </div>
                  <p className="text-xs text-emerald-700 font-medium mt-1">Lead: {facility.clinicalDirector}</p>
                </div>
                <span className="text-xs font-mono text-slate-400 bg-slate-50 px-3 py-1 rounded-xl border border-slate-200">
                  {facility.id}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
                <div className="space-y-1">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">Location & Address</span>
                  <p className="text-slate-700 leading-relaxed font-medium">{facility.address}</p>
                </div>

                <div className="space-y-1">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">Operating Hours & Contact</span>
                  <p className="text-slate-700">{facility.hours}</p>
                  <p className="text-emerald-700 font-bold mt-0.5">{facility.phone}</p>
                </div>

                <div className="space-y-1.5">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">Facility Specializations</span>
                  <ul className="space-y-1">
                    {facility.features.map((feat, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-slate-600">
                        <HealthcareIcon name="check" className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                        <span className="text-[11px]">{feat}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="pt-4 border-t border-slate-100 flex items-center justify-end gap-4">
                <Link
                  href={`/contact?facility=${facility.id}`}
                  className="px-6 py-2.5 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white text-xs font-bold shadow-sm transition"
                >
                  Reserve OPD Consultation
                </Link>
              </div>
            </div>
          ))}
        </div>

      </div>
    </PublicWebsiteShell>
  );
}
