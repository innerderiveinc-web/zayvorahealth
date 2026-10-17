"use client";

import React from "react";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";

const CLINICS = [
  { name: "ZAYVORA Healthcare System - Central Hospital", type: "Flagship Hospital & Research Complex", address: "ZAYVORA Health Boulevard, Institutional Area, New Delhi 110062", phone: "+91 97738 82657", timing: "Open 24/7 • OPD: 8:00 AM – 8:00 PM" },
  { name: "ZAYVORA Matab™ Charminar Heritage Center", type: "Specialized Unani Matab & Pharmacy", address: "Heritage Health Quarter, Near Charminar, Hyderabad 500002", phone: "+91 97738 82657", timing: "OPD: 9:00 AM – 7:00 PM" },
  { name: "ZAYVORA Integrative Care Center", type: "Clinical Matab & Telemedicine Hub", address: "Koramangala 4th Block, 80 Feet Road, Bengaluru 560034", phone: "+91 97738 82657", timing: "OPD: 9:30 AM – 6:30 PM" },
  { name: "ZAYVORA Himalayan Herbal Center", type: "High-Altitude Botanical Dispensary", address: "Residency Road, Srinagar, Jammu & Kashmir 190001", phone: "+91 97738 82657", timing: "OPD: 10:00 AM – 5:00 PM" }
];

export default function PatientClinicsPage() {
  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">🏥 Hospital Facilities & Matab Network</h1>
          <p className="text-sm text-[var(--text-muted)] mt-1">
            ZAYVORA accredited hospital centers, specialized Matabs, and regimenal therapy suites
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {CLINICS.map(c => (
            <div key={c.name} className="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-3">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-bold text-white text-base">{c.name}</h3>
                  <span className="text-xs text-emerald-400 font-semibold block mt-0.5">{c.type}</span>
                </div>
                <span className="text-xs font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Active</span>
              </div>
              <p className="text-xs text-[var(--text-muted)] leading-relaxed">📍 {c.address}</p>
              <div className="pt-2 border-t border-[var(--border)] flex justify-between items-center text-xs">
                <a href={`tel:${c.phone}`} className="text-slate-300 font-mono hover:text-emerald-400">📞 {c.phone}</a>
                <span className="text-[var(--text-muted)]">{c.timing}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
