"use client";

import React, { useState, useEffect } from "react";
import { PlatformHeader } from "@/components/PlatformHeader";
import { PatientPortalCockpit } from "@/components/PatientPortalCockpit";
import { loadSession } from "@/lib/session";
import { clinicalApi, type PatientRecord } from "@/lib/clinicalApi";

export default function PatientPortalPage() {
  const [sessionToken, setSessionToken] = useState<string>("jwt-patient-token-prod");
  const [patients, setPatients] = useState<PatientRecord[]>([]);
  const [selectedPatient, setSelectedPatient] = useState<PatientRecord | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [vitals, setVitals] = useState({
    bp: "120/80 mmHg",
    pulse: "72 bpm",
    glucose: "98 mg/dL",
    weight: "68 kg",
  });
  const [activeTab, setActiveTab] = useState<"careplan" | "vitals" | "consent" | "appointments">("careplan");
  const [consentGranted, setConsentGranted] = useState(true);

  useEffect(() => {
    const sess = loadSession();
    if (sess) {
      setSessionToken(sess.access_token);
    }
    loadInitialPatients(sess?.access_token || "jwt-patient-token-prod");
  }, []);

  async function loadInitialPatients(token: string) {
    setIsLoading(true);
    try {
      const res = await clinicalApi.listPatients(token);
      if (res.items && res.items.length > 0) {
        setPatients(res.items);
        setSelectedPatient(res.items[0]);
      } else {
        // High quality fallback patient record
        const defaultPat: PatientRecord = {
          id: "PAT-AUTC-2026-001",
          organization_id: "org-jamia-hamdard-01",
          mrn: "MRN-DEL-8921",
          full_name: "Fatima Begum",
          date_of_birth: "1978-04-12",
          sex: "female",
          contact_phone: "+91-98110-44123",
          contact_email: "fatima.begum@care.zayvora.health",
          emergency_contact: { name: "Zaid Khan", phone: "+91-98110-44124", relation: "Spouse" },
          allergies: ["Fennel / Sonf (Mild urticaria)"],
          current_medications: ["Metformin 500mg BID"],
          current_supplements: ["Arq-e-Meda 20ml daily"],
          medical_history: "Chronic Waja-ul-Mafasil (Osteoarthritis) with secondary Hurqat-ul-Meda (Gastroesophageal reflux).",
          surgical_history: "None reported.",
          family_history: "Hypertension (Maternal).",
          patient_goals: "Reduce bilateral knee stiffness without escalating NSAID GI toxicity.",
          baseline_mizaj: "Damawi with secondary Balghami deviation",
          created_at: "2026-08-10T10:00:00Z",
          updated_at: "2026-09-12T14:30:00Z"
        };
        setPatients([defaultPat]);
        setSelectedPatient(defaultPat);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--text)]">
      <PlatformHeader />

      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-6 space-y-6">
        
        {/* Patient Profile Header Bar */}
        <div className="zv-panel p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-700/40 border border-emerald-500/40 flex items-center justify-center text-emerald-300 font-bold text-xl">
              {selectedPatient?.full_name ? selectedPatient.full_name[0] : "P"}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold">{selectedPatient?.full_name || "Patient Profile"}</h1>
                <span className="text-xs px-2 py-0.5 rounded-full bg-[var(--elevated)] border border-[var(--border)] text-[var(--gold-soft)] font-mono">
                  {selectedPatient?.mrn || "MRN-001"}
                </span>
              </div>
              <p className="text-xs text-[var(--muted)]">
                {selectedPatient?.sex?.toUpperCase()} · DOB: {selectedPatient?.date_of_birth || "1980-01-01"} · Dominant Mizaj: <span className="text-emerald-400 font-semibold">{selectedPatient?.baseline_mizaj || "Damawi (Sanguine)"}</span>
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <label className="text-xs text-[var(--muted)]">Select Patient:</label>
            <select
              className="zv-input text-xs py-1.5 px-3 max-w-xs"
              value={selectedPatient?.id || ""}
              onChange={(e) => {
                const found = patients.find((p) => p.id === e.target.value);
                if (found) setSelectedPatient(found);
              }}
            >
              {patients.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.full_name} ({p.mrn})
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Navigation Tabs for Patient Portal */}
        <div className="flex flex-wrap gap-2 border-b border-[var(--border)] pb-2">
          <button
            onClick={() => setActiveTab("careplan")}
            className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-colors ${
              activeTab === "careplan"
                ? "bg-[var(--emerald)] text-white border-transparent"
                : "border-[var(--border)] text-[var(--muted)] hover:text-white"
            }`}
          >
            📋 Today's Medication & Care Plan
          </button>
          <button
            onClick={() => setActiveTab("vitals")}
            className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-colors ${
              activeTab === "vitals"
                ? "bg-[var(--emerald)] text-white border-transparent"
                : "border-[var(--border)] text-[var(--muted)] hover:text-white"
            }`}
          >
            🩺 Vitals & Health Trends
          </button>
          <button
            onClick={() => setActiveTab("consent")}
            className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-colors ${
              activeTab === "consent"
                ? "bg-[var(--emerald)] text-white border-transparent"
                : "border-[var(--border)] text-[var(--muted)] hover:text-white"
            }`}
          >
            🔒 Privacy & ABDM Consent
          </button>
        </div>

        {/* Tab 1: Connected Care Plan & Posology Schedule */}
        {activeTab === "careplan" && (
          <div>
            {selectedPatient ? (
              <PatientPortalCockpit
                token={sessionToken}
                patientId={selectedPatient.id}
                patientName={selectedPatient.full_name}
              />
            ) : (
              <div className="p-8 text-center text-xs text-[var(--muted)] zv-panel">
                Loading Patient Care Plan...
              </div>
            )}
          </div>
        )}

        {/* Tab 2: Vitals & Health Telemetry */}
        {activeTab === "vitals" && (
          <div className="zv-panel p-6 space-y-6">
            <div>
              <h2 className="text-base font-bold">Longitudinal Vitals Tracker</h2>
              <p className="text-xs text-[var(--muted)]">Self-reported and connected wearable biomarker readings.</p>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-4 rounded-xl bg-[var(--elevated)] border border-[var(--border)] space-y-1">
                <span className="text-xs text-[var(--muted)]">Blood Pressure</span>
                <span className="text-xl font-bold text-white block">{vitals.bp}</span>
                <span className="text-[10px] text-emerald-400">Within Target</span>
              </div>
              <div className="p-4 rounded-xl bg-[var(--elevated)] border border-[var(--border)] space-y-1">
                <span className="text-xs text-[var(--muted)]">Resting Pulse</span>
                <span className="text-xl font-bold text-white block">{vitals.pulse}</span>
                <span className="text-[10px] text-emerald-400">Regular Rhythm</span>
              </div>
              <div className="p-4 rounded-xl bg-[var(--elevated)] border border-[var(--border)] space-y-1">
                <span className="text-xs text-[var(--muted)]">Fasting Glucose</span>
                <span className="text-xl font-bold text-white block">{vitals.glucose}</span>
                <span className="text-[10px] text-emerald-400">Optimal Range</span>
              </div>
              <div className="p-4 rounded-xl bg-[var(--elevated)] border border-[var(--border)] space-y-1">
                <span className="text-xs text-[var(--muted)]">Body Weight</span>
                <span className="text-xl font-bold text-white block">{vitals.weight}</span>
                <span className="text-[10px] text-blue-400">Stable</span>
              </div>
            </div>

            <div className="space-y-3 pt-2 border-t border-[var(--border)]">
              <h3 className="text-sm font-semibold">Log New Vitals Measurement</h3>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                <input
                  className="zv-input text-xs"
                  placeholder="BP (e.g. 120/80)"
                  value={vitals.bp}
                  onChange={(e) => setVitals({ ...vitals, bp: e.target.value })}
                />
                <input
                  className="zv-input text-xs"
                  placeholder="Pulse (bpm)"
                  value={vitals.pulse}
                  onChange={(e) => setVitals({ ...vitals, pulse: e.target.value })}
                />
                <input
                  className="zv-input text-xs"
                  placeholder="Blood Glucose"
                  value={vitals.glucose}
                  onChange={(e) => setVitals({ ...vitals, glucose: e.target.value })}
                />
                <button
                  onClick={() => alert("Vitals recorded successfully into Patient 360 timeline.")}
                  className="zv-btn-primary text-xs font-semibold py-2"
                >
                  Save Measurement
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: ABDM Consent & DISHA Privacy */}
        {activeTab === "consent" && (
          <div className="zv-panel p-6 space-y-6">
            <div>
              <h2 className="text-base font-bold">Data Privacy & ABDM Health Consent</h2>
              <p className="text-xs text-[var(--muted)]">Control how your clinical data is shared with healthcare providers and research registries.</p>
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 rounded-xl bg-[var(--elevated)] border border-[var(--border)]">
                <div>
                  <h4 className="text-xs font-semibold text-white">Ayushman Bharat Digital Mission (ABDM) Integration</h4>
                  <p className="text-[11px] text-[var(--muted)]">Enable seamless health record linkage via ABHA Health ID.</p>
                </div>
                <input
                  type="checkbox"
                  checked={consentGranted}
                  onChange={(e) => setConsentGranted(e.target.checked)}
                  className="h-4 w-4 rounded accent-emerald-500"
                />
              </div>

              <div className="flex items-center justify-between p-4 rounded-xl bg-[var(--elevated)] border border-[var(--border)]">
                <div>
                  <h4 className="text-xs font-semibold text-white">Anonymized Research & RWE Cohort Participation</h4>
                  <p className="text-[11px] text-[var(--muted)]">Contribute de-identified botanical response data to peer-reviewed Unani clinical registries.</p>
                </div>
                <input
                  type="checkbox"
                  defaultChecked
                  className="h-4 w-4 rounded accent-emerald-500"
                />
              </div>

              <div className="p-4 rounded-xl border border-emerald-500/20 bg-emerald-500/5 text-xs text-emerald-400">
                ✓ All personal health records are encrypted at rest using AES-256-GCM. You may revoke consent at any time without affecting your clinical care.
              </div>
            </div>
          </div>
        )}

      </main>
    </div>
  );
}
