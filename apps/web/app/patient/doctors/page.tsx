"use client";

import React from "react";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";

const DOCTORS = [
  { name: "Hakeem Dr. Irfan Ashraf", degree: "BUMS (AKTC, AMU Aligarh)", specialty: "Moalajat (Internal Medicine) & Waja-ul-Mafasil", facility: "ZAYVORA Healthcare System - Central Hospital", room: "OPD Room 204", timing: "Mon – Fri: 9:00 AM – 2:00 PM" },
  { name: "Dr. Aisha Siddiqui", degree: "BUMS, MD (Tahaffuzi wa Samaji Tibb)", specialty: "Preventive Medicine & Mizaj-e-Adil Lifestyle", facility: "ZAYVORA Healthcare System - Central Hospital", room: "OPD Room 108", timing: "Tue – Sat: 10:00 AM – 3:00 PM" },
  { name: "Hakim Syed M. Akhtar", degree: "BUMS, MD (Ilaj bil-Tadbeer)", specialty: "Regimenal Therapy, Hijama & Musculoskeletal Rehabilitation", facility: "ZAYVORA Matab™ Specialized Therapy Suite", room: "Regimenal Suite 3", timing: "Mon – Thu: 11:00 AM – 4:00 PM" }
];

export default function PatientDoctorsPage() {
  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">🩺 Attending Clinicians & Faculty Directory</h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              Board-certified Senior Tabeebs and integrative medicine specialists
            </p>
          </div>
          <Link
            href="/patient/book"
            className="px-4 py-2 bg-[#2D6A4F] hover:bg-[#1B4332] text-white rounded-xl text-xs font-bold transition shadow-sm"
          >
            + Book Consultation
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {DOCTORS.map(d => (
            <div key={d.name} className="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] flex flex-col justify-between space-y-4">
              <div className="space-y-2">
                <div className="w-12 h-12 rounded-full bg-emerald-950/60 border border-emerald-500/40 flex items-center justify-center text-xl">
                  👨‍⚕️
                </div>
                <div>
                  <h3 className="font-bold text-white text-base">{d.name}</h3>
                  <span className="text-xs text-emerald-400 font-semibold block">{d.degree}</span>
                </div>
                <p className="text-xs text-[var(--text-muted)]">{d.specialty}</p>
                <div className="pt-2 border-t border-[var(--border)] text-[11px] text-slate-300 space-y-0.5">
                  <p>📍 {d.facility}</p>
                  <p>🚪 {d.room}</p>
                  <p>⏰ {d.timing}</p>
                </div>
              </div>

              <Link
                href="/patient/book"
                className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-emerald-400 font-bold text-xs rounded-xl border border-[var(--border)] text-center transition block"
              >
                Schedule Appointment →
              </Link>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
