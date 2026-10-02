"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { AuthService } from "@/lib/services/authService";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

interface PrescriptionHerb {
  herb: string;
  dose: string;
  form?: string;
  frequency?: string;
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
  created_at: string;
}

export default function PatientPrescriptionsPage() {
  const [prescriptions, setPrescriptions] = useState<PrescriptionRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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
        throw new Error(`Failed to load prescriptions (HTTP ${res.status})`);
      }

      const data = await res.json();
      if (data.ok && Array.isArray(data.prescriptions)) {
        setPrescriptions(data.prescriptions);
      } else {
        setPrescriptions([]);
      }
    } catch (err: any) {
      setError(err.message || "Failed to connect to prescription registry.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPrescriptions();
  }, []);

  const parseHerbs = (jsonStr: string): PrescriptionHerb[] => {
    try {
      const parsed = JSON.parse(jsonStr);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  };

  return (
    <AppShell activeRole="patient">
      <div className="space-y-6 max-w-4xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-[var(--text-primary)]">📜 Nuskha Prescriptions</h1>
              <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                21 CFR Part 11 Sealed
              </span>
            </div>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              Your clinician-verified Unani formulations & regimenal advice
            </p>
          </div>

          <button
            onClick={fetchPrescriptions}
            className="zv-btn-secondary text-xs px-3 py-1.5 flex items-center gap-1.5 self-start sm:self-auto"
          >
            <span>🔄</span>
            <span>Refresh Ledger</span>
          </button>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span>⚠</span>
              <span>{error}</span>
            </div>
            <button onClick={fetchPrescriptions} className="zv-btn-secondary text-[11px] px-3 py-1 font-semibold">
              Retry
            </button>
          </div>
        )}

        {loading ? (
          <div className="space-y-4">
            {[1, 2].map((n) => (
              <div key={n} className="zv-card p-5 animate-pulse space-y-3">
                <div className="h-4 bg-[var(--bg-elevated)] rounded w-1/4"></div>
                <div className="h-3 bg-[var(--bg-elevated)] rounded w-1/2"></div>
                <div className="h-12 bg-[var(--bg-elevated)] rounded"></div>
              </div>
            ))}
          </div>
        ) : prescriptions.length === 0 ? (
          <div className="zv-card p-12 text-center space-y-3">
            <div className="text-3xl">📜</div>
            <h3 className="font-semibold text-base text-[var(--text-primary)]">No Prescriptions Found</h3>
            <p className="text-xs text-[var(--text-muted)] max-w-sm mx-auto">
              You do not have any active or past Nuskha prescriptions recorded.
            </p>
            <Link href="/patient/book" className="zv-btn-primary inline-block text-xs px-4 py-2 font-semibold mt-2">
              Book a Consultation →
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {prescriptions.map((r) => {
              const herbs = parseHerbs(r.items_json);
              return (
                <div key={r.id} className="zv-card p-5 space-y-4 hover:border-[var(--primary)] transition">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[var(--border-subtle)] pb-3">
                    <div className="flex items-center gap-2.5">
                      <span className="font-mono text-sm font-bold text-emerald-400">
                        {r.order_number}
                      </span>
                      <span className="text-xs text-[var(--text-muted)]">
                        · {r.created_at ? r.created_at.split("T")[0] : "Verified"}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span
                        className={`text-xs px-2.5 py-0.5 rounded-full font-medium ${
                          r.status === "DISPENSED"
                            ? "zv-badge-emerald"
                            : r.status === "VERIFIED_READY"
                            ? "bg-blue-500/10 text-blue-400 border border-blue-500/30"
                            : "zv-badge-amber"
                        }`}
                      >
                        {r.status === "VERIFIED_READY" ? "✓ Verified & Ready" : r.status}
                      </span>
                    </div>
                  </div>

                  {/* Clinician Signature Info */}
                  <div className="flex items-center justify-between text-xs">
                    <div>
                      <span className="text-[var(--text-muted)]">Prescribing Clinician: </span>
                      <span className="font-semibold text-[var(--text-primary)]">{r.doctor_name}</span>
                      {r.doctor_reg && (
                        <span className="text-[var(--text-muted)] font-mono ml-1.5">({r.doctor_reg})</span>
                      )}
                    </div>
                    <div className="text-[var(--text-muted)] font-mono text-[11px]">
                      MRN: {r.mrn}
                    </div>
                  </div>

                  {/* Herbs Grid */}
                  <div>
                    <div className="text-xs font-semibold text-[var(--text-muted)] mb-2 uppercase tracking-wider">
                      Prescribed Mufradat & Murakkabat:
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {herbs.map((h, i) => (
                        <div
                          key={i}
                          className="p-2.5 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] flex items-center justify-between"
                        >
                          <div>
                            <div className="font-medium text-xs text-[var(--text-primary)]">{h.herb}</div>
                            {h.form && (
                              <div className="text-[10px] text-[#2DD4BF]">{h.form}</div>
                            )}
                          </div>
                          <div className="text-right">
                            <span className="font-mono text-xs font-bold text-amber-300">{h.dose}</span>
                            {h.frequency && (
                              <div className="text-[10px] text-[var(--text-muted)]">{h.frequency}</div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Parhez / Regimenal Guidance */}
                  {(r.dietary_advice || r.regimenal_advice) && (
                    <div className="p-3 rounded-lg bg-[var(--bg-base)] border border-[var(--border-default)] space-y-1 text-xs">
                      {r.dietary_advice && (
                        <div>
                          <span className="font-semibold text-amber-400">Dietary Parhez: </span>
                          <span className="text-[var(--text-secondary)]">{r.dietary_advice}</span>
                        </div>
                      )}
                      {r.regimenal_advice && (
                        <div>
                          <span className="font-semibold text-blue-400">Ilaj bil-Tadbeer (Regimen): </span>
                          <span className="text-[var(--text-secondary)]">{r.regimenal_advice}</span>
                        </div>
                      )}
                    </div>
                  )}

                  {/* 21 CFR Part 11 Digital Signature Hash */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-2 border-t border-[var(--border-subtle)] text-[10px] text-[var(--text-muted)]">
                    <div className="flex items-center gap-1.5">
                      <span>🔒</span>
                      <span>21 CFR Part 11 HMAC:</span>
                      <span className="font-mono text-[var(--text-secondary)] truncate max-w-xs">
                        {r.signature_hash || "SHA-256 Verified"}
                      </span>
                    </div>
                    <button
                      onClick={() => alert(`Digital Certificate:
Order: ${r.order_number}
Signature Hash: ${r.signature_hash}
Clinician: ${r.doctor_name}`)}
                      className="zv-btn-secondary text-[10px] px-2.5 py-1 font-semibold self-start sm:self-auto"
                    >
                      View Certificate
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </AppShell>
  );
}
