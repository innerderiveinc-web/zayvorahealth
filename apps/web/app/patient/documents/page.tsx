"use client";

import React from "react";
import { AppShell } from "@/components/AppShell";

const DOCUMENTS = [
  { name: "Signed Electronic Prescription (21 CFR Part 11)", type: "PDF", size: "240 KB", date: "2026-09-12", docId: "RX-2026-0441", signedBy: "Hakeem Dr. Irfan Ashraf" },
  { name: "Knee Joint X-Ray (Bilateral AP/Lateral)", type: "DICOM / PNG", size: "8.4 MB", date: "2026-09-08", docId: "RAD-2026-1049", signedBy: "Dr. Farooq Radiology" },
  { name: "Comprehensive Metabolic & Inflammatory Panel", type: "PDF", size: "180 KB", date: "2026-09-10", docId: "LAB-2026-5501", signedBy: "Central Pathology Lab" },
  { name: "Baseline 10-Ajnas Pulse Waveform Report", type: "PDF", size: "512 KB", date: "2026-09-12", docId: "DSP-2026-0129", signedBy: "ZAYVORA Clinical IoT" }
];

export default function PatientDocumentsPage() {
  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">📁 Clinical Health Records & Documents</h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              Digitally signed medical records, radiology imaging, and laboratory certificates
            </p>
          </div>
          <button 
            onClick={() => alert("Document upload dialog opened. Select local PDF or DICOM scan...")}
            className="px-4 py-2 bg-[#2D6A4F] hover:bg-[#1B4332] text-white rounded-xl text-sm font-semibold transition shadow-sm"
          >
            + Upload External Document
          </button>
        </div>

        <div className="bg-[var(--card)] rounded-2xl border border-[var(--border)] divide-y divide-[var(--border)] overflow-hidden">
          {DOCUMENTS.map(d => (
            <div key={d.docId} className="p-5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 hover:bg-white/5 transition">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-base">📄</span>
                  <h3 className="font-bold text-white text-sm">{d.name}</h3>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-[var(--border)]">{d.type}</span>
                </div>
                <p className="text-xs text-[var(--text-muted)]">
                  Document ID: <span className="font-mono text-slate-300">{d.docId}</span> • Issuer: {d.signedBy} • Size: {d.size}
                </p>
              </div>

              <div className="flex items-center gap-3">
                <span className="text-xs text-[var(--text-muted)] font-mono">{d.date}</span>
                <button
                  onClick={() => alert(`Downloading verified document ${d.docId}...`)}
                  className="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-emerald-400 font-semibold text-xs rounded-lg border border-[var(--border)] transition"
                >
                  Download ⬇
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
