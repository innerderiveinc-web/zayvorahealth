"use client";

import React, { useState, useEffect } from "react";
import { AppShell } from "@/components/AppShell";
import { AuthService } from "@/lib/services/authService";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

interface HerbItem {
  herb: string;
  dose: string;
  form: string;
  frequency: string;
}

interface PrescriptionRecord {
  id: string;
  order_number: string;
  mrn: string;
  patient_name: string;
  doctor_name: string;
  doctor_reg: string;
  items_json: string;
  dietary_advice?: string;
  regimenal_advice?: string;
  signature_hash: string;
  status: string;
  facility_id: string;
  created_at: string;
}

const COMMON_HERBS = [
  { name: "Ashwagandha (Withania somnifera)", defaultDose: "3g", defaultForm: "Safoof" },
  { name: "Brahmi (Bacopa monnieri)", defaultDose: "2g", defaultForm: "Safoof" },
  { name: "Asl-us-Soos (Glycyrrhiza glabra)", defaultDose: "2g", defaultForm: "Joshanda" },
  { name: "Ustukhuddus (Lavandula stoechas)", defaultDose: "5g", defaultForm: "Arq" },
  { name: "Gaozaban (Borago officinalis)", defaultDose: "3g", defaultForm: "Khamira" },
  { name: "Senna Makki (Cassia angustifolia)", defaultDose: "1g", defaultForm: "Safoof" }
];

export default function NuskhaPage() {
  const [prescriptions, setPrescriptions] = useState<PrescriptionRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showComposer, setShowComposer] = useState(false);

  // Composer Form State
  const [patientName, setPatientName] = useState("Ahmad Khan");
  const [mrn, setMrn] = useState("MRN-2026-0001");
  const [herbs, setHerbs] = useState<HerbItem[]>([
    { herb: "Ashwagandha (Withania somnifera)", dose: "3g", form: "Safoof", frequency: "BD" },
    { herb: "Brahmi (Bacopa monnieri)", dose: "2g", form: "Safoof", frequency: "BD" }
  ]);
  const [dietaryAdvice, setDietaryAdvice] = useState("Avoid cold fluids and heavy red meat. Consume lukewarm infusions.");
  const [regimenalAdvice, setRegimenalAdvice] = useState("Daily morning walk (30 min) and mild foot massage with Roghan-e-Banafsha.");

  const fetchPrescriptions = async () => {
    setLoading(true);
    setError(null);
    const session = AuthService.getSession();

    try {
      const res = await fetch(`${API}/api/v1/prescriptions`, {
        headers: {
          ...(session?.token ? { Authorization: `Bearer ${session.token}` } : {})
        }
      });

      if (!res.ok) {
        throw new Error(`Failed to load prescription ledger (HTTP ${res.status})`);
      }

      const data = await res.json();
      if (data.ok && Array.isArray(data.prescriptions)) {
        setPrescriptions(data.prescriptions);
      } else {
        setPrescriptions([]);
      }
    } catch (err: any) {
      setError(err.message || "Failed to reach prescription registry.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPrescriptions();
  }, []);

  const addHerb = (h: { name: string; defaultDose: string; defaultForm: string }) => {
    setHerbs([...herbs, { herb: h.name, dose: h.defaultDose, form: h.defaultForm, frequency: "BD" }]);
  };

  const removeHerb = (index: number) => {
    setHerbs(herbs.filter((_, i) => i !== index));
  };

  const handleCreatePrescription = async () => {
    if (herbs.length === 0) {
      alert("Please include at least one herb or formulation.");
      return;
    }

    setSubmitting(true);
    setError(null);
    const session = AuthService.getSession();

    const payload = {
      patientName,
      mrn,
      doctorName: session?.user?.fullName || "Hakeem Dr. Irfan Ashraf",
      doctorReg: session?.user?.regNumber || "Updating / Verification in Progress",
      items: herbs,
      dietaryAdvice,
      regimenalAdvice,
      facilityId: session?.user?.facilityId || "FAC-HQ-01"
    };

    try {
      const res = await fetch(`${API}/api/v1/prescriptions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(session?.token ? { Authorization: `Bearer ${session.token}` } : {})
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        throw new Error(errJson.error || "Failed to author prescription.");
      }

      setShowComposer(false);
      await fetchPrescriptions();
    } catch (err: any) {
      setError(err.message || "Prescription submission failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-6xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-[var(--text-primary)]">Nuskha Authoring & Ledger</h1>
              <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                21 CFR Part 11 Digital Signatures
              </span>
            </div>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              Author, digitally sign, and audit classical Unani formulations
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button onClick={fetchPrescriptions} className="zv-btn-secondary text-xs px-3 py-2">
              🔄 Refresh
            </button>
            <button
              onClick={() => setShowComposer(!showComposer)}
              className="zv-btn-primary text-xs px-4 py-2 font-semibold"
            >
              {showComposer ? "✕ Close Composer" : "+ Author New Nuskha"}
            </button>
          </div>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs flex justify-between items-center">
            <span>⚠ {error}</span>
            <button onClick={() => setError(null)} className="text-red-400 font-bold hover:text-white">✕</button>
          </div>
        )}

        {/* Composer Drawer / Card */}
        {showComposer && (
          <div className="zv-card p-6 space-y-5 border-emerald-500/40 bg-emerald-950/10">
            <div className="flex items-center justify-between border-b border-[var(--border-subtle)] pb-3">
              <div>
                <h2 className="font-semibold text-base text-[var(--text-primary)]">New Nuskha Formulation</h2>
                <p className="text-xs text-[var(--text-muted)]">Authoring for patient encounter</p>
              </div>
              <span className="px-2.5 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/30 text-[11px] font-bold">
                Pending Clinician Signature
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-semibold text-[var(--text-muted)] block mb-1">Patient Name</label>
                <input
                  value={patientName}
                  onChange={(e) => setPatientName(e.target.value)}
                  className="zv-input text-xs"
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-[var(--text-muted)] block mb-1">Medical Record Number (MRN)</label>
                <input
                  value={mrn}
                  onChange={(e) => setMrn(e.target.value)}
                  className="zv-input text-xs font-mono"
                />
              </div>
            </div>

            {/* Herb Selection */}
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="text-xs font-semibold text-[var(--text-muted)]">Prescribed Herbs & Murakkabat</label>
                <span className="text-[11px] text-[var(--text-muted)]">{herbs.length} items added</span>
              </div>

              {/* Quick Add Herb Badges */}
              <div className="flex gap-2 flex-wrap mb-3">
                {COMMON_HERBS.map((h) => (
                  <button
                    key={h.name}
                    onClick={() => addHerb(h)}
                    className="text-[10px] px-2.5 py-1 rounded-full bg-[var(--bg-elevated)] border border-[var(--border-default)] text-[var(--text-secondary)] hover:text-white hover:border-[var(--primary)] transition"
                  >
                    + {h.name.split(" ")[0]}
                  </button>
                ))}
              </div>

              {/* Herbs List Table */}
              <div className="space-y-2">
                {herbs.map((item, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs"
                  >
                    <span className="font-semibold text-[var(--text-primary)] flex-1">{item.herb}</span>
                    <div className="flex items-center gap-2">
                      <input
                        value={item.dose}
                        onChange={(e) => {
                          const updated = [...herbs];
                          updated[idx].dose = e.target.value;
                          setHerbs(updated);
                        }}
                        className="zv-input py-1 px-2 text-xs w-20 text-center font-mono"
                        placeholder="Dose"
                      />
                      <input
                        value={item.form}
                        onChange={(e) => {
                          const updated = [...herbs];
                          updated[idx].form = e.target.value;
                          setHerbs(updated);
                        }}
                        className="zv-input py-1 px-2 text-xs w-24 text-center"
                        placeholder="Form"
                      />
                      <input
                        value={item.frequency}
                        onChange={(e) => {
                          const updated = [...herbs];
                          updated[idx].frequency = e.target.value;
                          setHerbs(updated);
                        }}
                        className="zv-input py-1 px-2 text-xs w-20 text-center"
                        placeholder="Freq"
                      />
                      <button
                        onClick={() => removeHerb(idx)}
                        className="text-red-400 hover:text-red-300 px-2 py-1"
                        title="Remove herb"
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Dietary & Regimenal Advice */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-semibold text-[var(--text-muted)] block mb-1">Dietary Parhez (Ghiza)</label>
                <textarea
                  rows={2}
                  value={dietaryAdvice}
                  onChange={(e) => setDietaryAdvice(e.target.value)}
                  className="zv-input text-xs"
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-[var(--text-muted)] block mb-1">Ilaj bil-Tadbeer (Regimen)</label>
                <textarea
                  rows={2}
                  value={regimenalAdvice}
                  onChange={(e) => setRegimenalAdvice(e.target.value)}
                  className="zv-input text-xs"
                />
              </div>
            </div>

            {/* Actions */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-3 border-t border-[var(--border-subtle)]">
              <span className="text-[11px] text-amber-400">
                🔒 Cryptographic SHA-256 HMAC digital signature will be generated on confirmation.
              </span>
              <div className="flex gap-2">
                <button
                  disabled={submitting}
                  onClick={handleCreatePrescription}
                  className="zv-btn-primary text-xs px-5 py-2 font-semibold flex items-center gap-2"
                >
                  {submitting ? "Sealing Prescription..." : "Sign & Lock Prescription (21 CFR Part 11) ✓"}
                </button>
                <button
                  disabled={submitting}
                  onClick={() => setShowComposer(false)}
                  className="zv-btn-secondary text-xs px-4 py-2"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Existing Prescriptions Ledger */}
        <div className="zv-card overflow-hidden">
          {loading ? (
            <div className="p-8 text-center space-y-3">
              <div className="animate-spin text-2xl">⏳</div>
              <p className="text-xs text-[var(--text-muted)]">Loading Nuskha registry...</p>
            </div>
          ) : prescriptions.length === 0 ? (
            <div className="p-12 text-center space-y-3">
              <div className="text-3xl">📜</div>
              <h3 className="font-semibold text-base text-[var(--text-primary)]">Prescription Ledger Empty</h3>
              <p className="text-xs text-[var(--text-muted)] max-w-sm mx-auto">
                No prescriptions have been recorded yet. Click &ldquo;+ Author New Nuskha&rdquo; to begin.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="border-b border-[var(--border-default)] bg-[var(--bg-elevated)]">
                  <tr className="text-left text-[var(--text-muted)] text-xs font-semibold">
                    <th className="px-4 py-3">Order Number</th>
                    <th className="px-4 py-3">Patient & MRN</th>
                    <th className="px-4 py-3">Prescribing Doctor</th>
                    <th className="px-4 py-3">Status</th>
                    <th className="px-4 py-3">21 CFR Part 11 HMAC</th>
                    <th className="px-4 py-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border-subtle)]">
                  {prescriptions.map((n) => (
                    <tr key={n.id} className="hover:bg-[var(--bg-elevated)] transition">
                      <td className="px-4 py-3 font-mono text-xs font-bold text-emerald-400">
                        {n.order_number}
                      </td>
                      <td className="px-4 py-3">
                        <div className="font-semibold text-sm text-[var(--text-primary)]">{n.patient_name}</div>
                        <div className="text-[11px] font-mono text-[var(--text-muted)]">{n.mrn}</div>
                      </td>
                      <td className="px-4 py-3 text-xs text-[var(--text-muted)]">
                        <div className="font-medium text-[var(--text-primary)]">{n.doctor_name}</div>
                        <div className="text-[10px] text-[var(--text-secondary)]">{n.doctor_reg}</div>
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={`text-xs px-2.5 py-0.5 rounded-full font-medium ${
                            n.status === "DISPENSED"
                              ? "zv-badge-emerald"
                              : n.status === "VERIFIED_READY"
                              ? "bg-blue-500/10 text-blue-400 border border-blue-500/30"
                              : "zv-badge-amber"
                          }`}
                        >
                          {n.status}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-mono text-[10px] text-[var(--text-muted)] max-w-xs truncate">
                        {n.signature_hash}
                      </td>
                      <td className="px-4 py-3 text-right">
                        <button
                          onClick={() => alert(`Prescription Order: ${n.order_number}
Signature Hash: ${n.signature_hash}
Doctor: ${n.doctor_name}
Status: ${n.status}`)}
                          className="zv-btn-secondary text-xs px-3 py-1 font-semibold"
                        >
                          Audit Hash
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}
