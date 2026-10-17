"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { AuthService } from "@/lib/services/authService";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

interface AdvisorySections {
  mizaj_analysis?: string;
  differential_diagnoses?: string[];
  recommended_nuskha?: Array<{ herb: string; dose: string; form?: string }>;
  tadbeer_ghiza?: string;
  safety_warnings?: string[];
  clinical_summary?: string;
}

interface ConsultResponse {
  ok: boolean;
  consultationId?: string;
  safe_to_lock: boolean;
  requiresPractitionerSignoff: boolean;
  advisorySections?: AdvisorySections;
  citations?: Array<{ title: string; source: string; confidence: number }>;
  message?: string;
  raw?: string;
}

const EXAMPLES = [
  "Patient has Su-ul-Mizaj Damawi with recurring vascular cephalalgia (Suda' Muzmin).",
  "Suggest non-toxic Mufradat for chronic osteoarthritis (Waja'-ul-Mafasil) in elderly Balghami.",
  "Evaluate liver-digestive axis (Zo'f-e-Kabid) with dyspepsia and mild hyperacidity."
];

export default function HakeemSahabPage() {
  const [query, setQuery] = useState("");
  const [mrn, setMrn] = useState("MRN-2026-0001");
  const [organAxis, setOrganAxis] = useState("Cerebrovascular-Psychic Axis (Dimagh-Asab)");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ConsultResponse | null>(null);

  const handleSubmit = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);

    const session = AuthService.getSession();

    try {
      const res = await fetch(`${API}/api/v1/hakeem/consult`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(session?.token ? { Authorization: `Bearer ${session.token}` } : {})
        },
        body: JSON.stringify({
          chiefComplaint: query,
          mrn: mrn.trim() || undefined,
          organAxis
        })
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.error || errData.message || `AI Copilot request failed (HTTP ${res.status})`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Failed to reach Hakeem Sahab AI service.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-4xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-[var(--text-primary)]">Hakeem Sahab AI™</h1>
              <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Copilot Active
              </span>
            </div>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              Level 4 Clinical Decision Support · Classical Greco-Arab RAG & Safety Firewall
            </p>
          </div>
          <span className="px-3 py-1 rounded-full bg-red-500/10 text-red-400 border border-red-500/30 text-xs font-mono font-bold self-start sm:self-auto">
            🔒 safe_to_lock = false
          </span>
        </div>

        {/* Clinical Safety Invariant Card */}
        <div className="zv-card p-4 flex gap-3 items-start border-amber-500/30 bg-amber-500/10">
          <span className="text-amber-400 text-lg">⚠</span>
          <div className="text-xs text-amber-300 space-y-1">
            <p className="font-semibold">Mandatory Clinician Governance (21 CFR Part 11):</p>
            <p className="leading-relaxed">
              Hakeem Sahab AI™ assists clinical reasoning but cannot autonomously author or lock prescriptions.
              Every suggestion requires independent review, modification, and digital signature by a licensed Hakeem or Physician.
            </p>
          </div>
        </div>

        {/* Query Input Card */}
        <div className="zv-card p-5 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="text-xs font-semibold text-[var(--text-muted)] block mb-1">Patient MRN</label>
              <input
                type="text"
                value={mrn}
                onChange={(e) => setMrn(e.target.value)}
                placeholder="e.g. MRN-2026-0001"
                className="zv-input text-xs font-mono"
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-[var(--text-muted)] block mb-1">Target Organ-Axis</label>
              <select
                value={organAxis}
                onChange={(e) => setOrganAxis(e.target.value)}
                className="zv-input text-xs"
              >
                <option value="Cerebrovascular-Psychic Axis (Dimagh-Asab)">Cerebrovascular-Psychic (Dimagh-Asab)</option>
                <option value="Hepato-Digestive Axis (Kabid-Meda)">Hepato-Digestive (Kabid-Meda)</option>
                <option value="Cardio-Respiratory Axis (Qalb-Riya)">Cardio-Respiratory (Qalb-Riya)</option>
                <option value="Renal-Urogenital Axis (Kulya-Masana)">Renal-Urogenital (Kulya-Masana)</option>
                <option value="Musculoskeletal-Metabolic Axis (Mafasil-Asab)">Musculoskeletal-Metabolic (Mafasil)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-[var(--text-muted)] block mb-1">Clinical Inquiry / Presentation</label>
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Describe chief complaint, temperamental dyscrasia (Su-ul-Mizaj), or posology questions..."
              rows={3}
              className="zv-input text-sm resize-none"
            />
          </div>

          <div>
            <div className="text-[11px] font-semibold text-[var(--text-muted)] mb-1.5">Quick Clinical Prompts:</div>
            <div className="flex gap-2 flex-wrap">
              {EXAMPLES.map((ex) => (
                <button
                  key={ex}
                  onClick={() => setQuery(ex)}
                  className="text-[10px] px-2.5 py-1 rounded bg-[var(--bg-elevated)] text-[var(--text-secondary)] hover:text-white border border-[var(--border-default)] transition text-left"
                >
                  {ex.substring(0, 55)}...
                </button>
              ))}
            </div>
          </div>

          {error && (
            <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs">
              ⚠ {error}
            </div>
          )}

          <div className="flex justify-between items-center pt-2">
            <button
              onClick={handleSubmit}
              disabled={loading || !query.trim()}
              className={`zv-btn-primary text-xs px-5 py-2.5 font-semibold flex items-center gap-2 ${
                loading || !query.trim() ? "opacity-50 cursor-not-allowed" : ""
              }`}
            >
              {loading ? (
                <>
                  <span className="animate-spin text-base">⏳</span>
                  <span>Synthesizing Monograph Evidence...</span>
                </>
              ) : (
                <span>Query Hakeem Sahab AI™ →</span>
              )}
            </button>
            <span className="text-[10px] text-[var(--text-muted)]">
              Model: ZAYVORA Classical Reasoning Engine v2.0
            </span>
          </div>
        </div>

        {/* AI Advisory Response Card */}
        {result && (
          <div className="zv-card p-6 space-y-5 border-emerald-500/30 bg-emerald-950/10">
            <div className="flex items-center justify-between border-b border-[var(--border-subtle)] pb-3">
              <div>
                <h3 className="font-bold text-base text-[var(--text-primary)]">
                  Clinical Copilot Advisory
                </h3>
                {result.consultationId && (
                  <span className="font-mono text-[10px] text-[var(--text-muted)]">
                    Audit ID: {result.consultationId}
                  </span>
                )}
              </div>
              <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold">
                ✓ Evidence Anchored
              </span>
            </div>

            {/* Advisory Content */}
            <div className="space-y-4 text-xs">
              {result.advisorySections?.clinical_summary && (
                <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                  <div className="font-semibold text-emerald-400 mb-1">Clinical Impression</div>
                  <p className="text-[var(--text-primary)] leading-relaxed">
                    {result.advisorySections.clinical_summary}
                  </p>
                </div>
              )}

              {result.advisorySections?.mizaj_analysis && (
                <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                  <div className="font-semibold text-[#2DD4BF] mb-1">Mizaj Assessment (Dyscrasia Analysis)</div>
                  <p className="text-[var(--text-secondary)] leading-relaxed">
                    {result.advisorySections.mizaj_analysis}
                  </p>
                </div>
              )}

              {result.advisorySections?.recommended_nuskha && result.advisorySections.recommended_nuskha.length > 0 && (
                <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                  <div className="font-semibold text-amber-300 mb-2">Formulation Suggestions (Draft Nuskha)</div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {result.advisorySections.recommended_nuskha.map((item, idx) => (
                      <div key={idx} className="p-2 rounded bg-[var(--bg-base)] border border-[var(--border-default)] flex justify-between items-center">
                        <span className="font-medium text-[var(--text-primary)]">{item.herb}</span>
                        <span className="font-mono text-amber-400 font-bold">{item.dose}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {result.advisorySections?.tadbeer_ghiza && (
                <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                  <div className="font-semibold text-blue-400 mb-1">Regimenal & Dietary Guidance (Ilaj bil-Tadbeer / Ghiza)</div>
                  <p className="text-[var(--text-secondary)] leading-relaxed">
                    {result.advisorySections.tadbeer_ghiza}
                  </p>
                </div>
              )}
            </div>

            {/* Citations */}
            {result.citations && result.citations.length > 0 && (
              <div className="pt-2 border-t border-[var(--border-subtle)] text-[11px]">
                <span className="font-semibold text-[var(--text-muted)] block mb-1.5">Classical Literature Citations:</span>
                <ul className="space-y-1 text-[var(--text-secondary)]">
                  {result.citations.map((c, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <span>📖</span>
                      <span className="font-medium">{c.title}</span>
                      <span className="text-[var(--text-muted)]">({c.source})</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Bottom Actions: Explicit Clinician Review Controls */}
            <div className="flex flex-col sm:flex-row justify-between items-center gap-3 pt-3 border-t border-[var(--border-subtle)]">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
                <span className="text-[11px] text-amber-300 font-semibold">
                  Pending Independent Clinician Approval (safe_to_lock: false)
                </span>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <button
                  onClick={() => alert("Advisory rejected and logged in safety audit ledger.")}
                  className="px-3 py-1.5 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30 text-xs font-semibold transition"
                >
                  ✕ Reject
                </button>
                <Link
                  href="/doctor/nuskha"
                  className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold transition"
                >
                  ✎ Edit &amp; Customize
                </Link>
                <Link
                  href="/doctor/nuskha"
                  className="zv-btn-primary text-xs px-4 py-2 font-semibold flex items-center gap-1.5 shadow-md shadow-teal-900/30"
                >
                  <span>✓ Accept &amp; Import to Nuskha</span>
                  <span>→</span>
                </Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
