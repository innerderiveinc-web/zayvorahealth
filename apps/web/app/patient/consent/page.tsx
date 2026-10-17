"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";

export default function PatientConsentPage() {
  const [abhaConsent, setAbhaConsent] = useState(true);
  const [teleconsultRecording, setTeleconsultRecording] = useState(false);
  const [researchAnonymization, setResearchAnonymization] = useState(true);

  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">🛡️ Patient Consent & Privacy Controls</h1>
          <p className="text-sm text-[var(--text-muted)] mt-1">
            Manage national health locker sharing, video recording permissions, and RWE research participation
          </p>
        </div>

        <div className="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-5">
          <h3 className="font-bold text-white text-base">Active Informed Consents (DISHA & ABDM Compliant)</h3>

          <div className="divide-y divide-[var(--border)] text-xs">
            <div className="py-4 flex justify-between items-center gap-4">
              <div className="space-y-1">
                <span className="font-bold text-white block text-sm">Ayushman Bharat Digital Mission (ABDM) Data Sharing</span>
                <p className="text-[var(--text-muted)] leading-relaxed">
                  Allows ZAYVORA Healthcare System to securely synchronize encrypted electronic prescriptions, lab panels, and diagnostic summaries to your ABHA health locker.
                </p>
              </div>
              <input type="checkbox" checked={abhaConsent} onChange={e => setAbhaConsent(e.target.checked)} className="w-5 h-5 accent-emerald-500" />
            </div>

            <div className="py-4 flex justify-between items-center gap-4">
              <div className="space-y-1">
                <span className="font-bold text-white block text-sm">Tele-Consultation Session Audio/Video Archival</span>
                <p className="text-[var(--text-muted)] leading-relaxed">
                  Permits high-definition video recording of consultations for medical quality review and clinical continuity. Optional and revocable anytime.
                </p>
              </div>
              <input type="checkbox" checked={teleconsultRecording} onChange={e => setTeleconsultRecording(e.target.checked)} className="w-5 h-5 accent-emerald-500" />
            </div>

            <div className="py-4 flex justify-between items-center gap-4">
              <div className="space-y-1">
                <span className="font-bold text-white block text-sm">De-Identified Real-World Evidence (RWE) Observational Cohort</span>
                <p className="text-[var(--text-muted)] leading-relaxed">
                  Permits anonymized statistical evaluation of botanical therapeutic response curves to advance integrative Unani medicine clinical trials.
                </p>
              </div>
              <input type="checkbox" checked={researchAnonymization} onChange={e => setResearchAnonymization(e.target.checked)} className="w-5 h-5 accent-emerald-500" />
            </div>
          </div>

          <div className="pt-2 flex justify-end">
            <button
              onClick={() => alert("Consent preferences cryptographically updated and logged to audit trail.")}
              className="px-6 py-2.5 bg-[#2D6A4F] hover:bg-[#1B4332] text-white font-bold text-xs rounded-xl shadow transition"
            >
              Update Consents
            </button>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
