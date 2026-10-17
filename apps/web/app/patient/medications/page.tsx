"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";

interface Medication {
  name: string;
  dosage: string;
  timing: string;
  vehicle: string;
  schedule: string;
  remainingDays: number;
  status: "Active" | "Completed" | "Refill Needed";
}

const MEDICATIONS: Medication[] = [
  { name: "Majun Suranjan (Mudabbar)", dosage: "5g (1 tsp)", timing: "Twice daily after breakfast and dinner", vehicle: "Lukewarm water or fennel seed infusion", schedule: "Days 1 – 30", remainingDays: 16, status: "Active" },
  { name: "Raughan-e-Balsan", dosage: "Gentle local application (3-5 ml)", timing: "At bedtime on affected knee joints", vehicle: "Warm fomentation (Natool) recommended beforehand", schedule: "Nightly", remainingDays: 22, status: "Active" },
  { name: "Hab-e-Suranjan Forte", dosage: "1 tablet", timing: "Once daily after lunch", vehicle: "Plain water", schedule: "Days 15 – 45", remainingDays: 30, status: "Active" }
];

export default function PatientMedicationsPage() {
  const [meds, setMeds] = useState<Medication[]>(MEDICATIONS);

  const requestRefill = (name: string) => {
    alert(`Refill request for ${name} submitted to ZAYVORA Central Dispensary. Pharmacist Zainab Ali notified.`);
  };

  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">💊 Active Prescriptions & Herbal Posology</h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              FEFO batch-verified Unani formulations prescribed by Hakeem Dr. Irfan Ashraf
            </p>
          </div>
          <button 
            onClick={() => alert("Playing vernacluar audio dosage guidance (Urdu/Hindi)...")}
            className="px-4 py-2 bg-emerald-600/20 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-600/30 text-sm font-semibold rounded-xl transition flex items-center gap-2"
          >
            <span>🔊</span> Listen to Vernacular Audio Posology
          </button>
        </div>

        <div className="space-y-4">
          {meds.map(m => (
            <div key={m.name} className="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <h3 className="font-bold text-white text-base">{m.name}</h3>
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    {m.status}
                  </span>
                  <span className="text-xs text-[var(--text-muted)] font-mono">({m.remainingDays} days remaining)</span>
                </div>
                <div className="text-xs text-[var(--text-muted)] space-y-0.5">
                  <p><strong className="text-slate-200">Dose:</strong> {m.dosage} • <strong className="text-slate-200">Timing:</strong> {m.timing}</p>
                  <p><strong className="text-teal-400">Anupan (Vehicle):</strong> {m.vehicle}</p>
                  <p><strong className="text-slate-200">Schedule:</strong> {m.schedule}</p>
                </div>
              </div>

              <button
                onClick={() => requestRefill(m.name)}
                className="px-4 py-2 bg-[#2D6A4F] hover:bg-[#1B4332] text-white font-semibold text-xs rounded-xl shadow transition"
              >
                Request Refill 🔄
              </button>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
