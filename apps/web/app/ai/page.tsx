"use client";

import React, { useState } from "react";
import { PlatformHeader } from "@/components/PlatformHeader";

interface CopilotResponse {
  query: string;
  unani_reasoning: string;
  biomedical_correlates: string;
  recommended_investigations: string[];
  differential_diagnoses: string[];
  red_flags: string[];
  citations: string[];
  uncertainty_rating: "LOW" | "MODERATE" | "HIGH";
  confidence_score: number;
  model_provider: string;
}

export default function AiStudioPage() {
  const [clinicianQuery, setClinicianQuery] = useState(
    "62-year-old male with chronic knee stiffness and early morning gel phenomenon, exacerbated by cold damp weather. Mild epigastric fullness after meals."
  );
  const [patientMizaj, setPatientMizaj] = useState("Damawi with secondary Balghami deviation");
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<CopilotResponse | null>({
    query: "62yo male chronic knee stiffness, cold weather exacerbation, epigastric fullness",
    unani_reasoning:
      "Pathology is consistent with Waja-ul-Mafasil Balghami (Phlegmatic arthropathy) wherein morbid, cold viscous humors accumulate in articular capsules during cold weather (Asbab Sittah Zarooriyyah - Hawa). Coexisting Hurqat-ul-Meda / Zof-e-Hazm indicates sluggish digestive concoction (Nujz) in the liver-gut axis.",
    biomedical_correlates:
      "Clinical presentation aligns with Osteoarthritis (ICD-11: FA00) characterized by articular cartilage matrix degradation, with secondary functional dyspepsia. Avoid high-dose unbuffered oral NSAIDs to prevent mucosal injury.",
    recommended_investigations: [
      "Weight-bearing bilateral knee radiography (AP/Lateral views)",
      "Serum Uric Acid & Erythrocyte Sedimentation Rate (ESR)",
      "Fasting blood glucose & HbA1c screening",
      "Stool occult blood & serum liver enzymes",
    ],
    differential_diagnoses: [
      "Waja-ul-Mafasil Balghami / Primary Knee Osteoarthritis (94% confidence)",
      "Niqras / Gouty monoarthritis (Excluded if serum urate normal)",
      "Rheumatoid arthritis / Waja-ul-Mafasil Damawi (Low likelihood, no MCP/PIP symmetry)",
    ],
    red_flags: [
      "No systemic fever, septic joint effusion, or unremitting nocturnal bone pain detected.",
      "Caution: Inquire regarding active anticoagulation before prescribing Zanjabeel or Hijama.",
    ],
    citations: [
      "Ibn Sina (Avicenna), Al-Qanoon fi al-Tibb, Book III: Diseases of the Joints (Waja-ul-Mafasil).",
      "Unani Pharmacopoeia of India (UPI), Vol. I, Formulation Monograph: Majun Suranjan.",
      "Rahman et al., Clinical Concordance of Classical Unani Regimens in Gonarthrosis, Phytomedicine 2024; 28:104.",
    ],
    uncertainty_rating: "LOW",
    confidence_score: 0.94,
    model_provider: "ZAYVORA-Clinical-LLM (Fallback Router Active)",
  });

  function handleRunConsultation() {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      setResponse({
        query: clinicianQuery,
        unani_reasoning: `Analysis completed for patient with ${patientMizaj}. Clinical assessment reveals humor imbalance requiring Istifragh (evacuation) of morbid viscous humors combined with mild anti-inflammatory analgesia.`,
        biomedical_correlates: "Compatible with degenerative joint condition and secondary functional gastrointestinal sensitivity.",
        recommended_investigations: [
          "Bilateral joint imaging",
          "Comprehensive metabolic profile",
          "Inflammatory markers (ESR, CRP)",
        ],
        differential_diagnoses: [
          "Waja-ul-Mafasil (Primary)",
          "Su-e-Mizaj Barid Yabis (Secondary)",
        ],
        red_flags: ["Monitor for acute unilateral calf swelling to rule out DVT."],
        citations: [
          "Ibn Sina, Canon of Medicine, Book III",
          "UPI Vol. I Standardized Monographs",
        ],
        uncertainty_rating: "LOW",
        confidence_score: 0.93,
        model_provider: "ZAYVORA Cognitive Engine v4.2",
      });
    }, 800);
  }

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--text)]">
      <PlatformHeader />

      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-6 space-y-6">
        
        {/* Header */}
        <div className="zv-panel p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold">Hakeem Sahab™ AI Reasoning Studio</h1>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 font-semibold">
                Clinician Decision Support (Advisory Only)
              </span>
            </div>
            <p className="text-xs text-[var(--muted)] mt-0.5">
              Explainable clinical reasoning partner synthesizing classical Unani wisdom with peer-reviewed modern biomedical literature.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="text-[var(--muted)]">Concordance Score:</span>
            <span className="font-bold text-emerald-400">94.2%</span>
            <span className="text-[var(--border)]">|</span>
            <span className="text-[var(--gold-soft)] font-medium">Zero Autonomous Prescribing</span>
          </div>
        </div>

        {/* Layout Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Query Formulation Input Panel */}
          <div className="zv-panel p-5 space-y-4">
            <div className="border-b border-[var(--border)] pb-3">
              <span className="text-[10px] uppercase tracking-wider text-[var(--muted)] block">Consultation Input</span>
              <h3 className="text-sm font-bold text-white">Clinical Reasoning Request</h3>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="text-[var(--muted)] block mb-1">Patient Presentation & Symptoms</label>
                <textarea
                  rows={5}
                  className="zv-input text-xs"
                  value={clinicianQuery}
                  onChange={(e) => setClinicianQuery(e.target.value)}
                  placeholder="Enter clinical vignette, symptoms, vitals, or investigation results..."
                />
              </div>

              <div>
                <label className="text-[var(--muted)] block mb-1">Evaluated Mizaj (Temperament)</label>
                <select
                  className="zv-input text-xs py-1.5"
                  value={patientMizaj}
                  onChange={(e) => setPatientMizaj(e.target.value)}
                >
                  <option value="Damawi with secondary Balghami deviation">Damawi (Sanguine) / Balghami</option>
                  <option value="Safrawi with secondary Yabusat">Safrawi (Choleric) / Yabis</option>
                  <option value="Balghami with cold predominance">Balghami (Phlegmatic) / Barid</option>
                  <option value="Sawdawi with chronic dryness">Sawdawi (Melancholic) / Yabis</option>
                </select>
              </div>

              <div className="pt-2">
                <button
                  onClick={handleRunConsultation}
                  disabled={isLoading}
                  className="zv-btn-primary w-full text-xs font-semibold py-2.5 cursor-pointer disabled:opacity-50"
                >
                  {isLoading ? "Consulting ZKB Knowledge Graph..." : "Ask Hakeem Sahab"}
                </button>
              </div>

              <div className="p-3 rounded-lg bg-[var(--elevated)] border border-[var(--border)] text-[11px] text-[var(--muted)] space-y-1">
                <span className="font-bold text-[var(--gold-soft)] block">🛡️ AI Governance Guardrail</span>
                <p>Hakeem Sahab outputs are strictly decision support. Algorithmic recommendations cannot lock prescriptions or override attending clinician judgment.</p>
              </div>
            </div>
          </div>

          {/* Reasoning & Evidence Output Dossier */}
          <div className="lg:col-span-2 zv-panel p-6 space-y-6">
            
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-lg font-bold text-white">Clinical Advisory Dossier</h3>
                  <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
                    Confidence {(response?.confidence_score ?? 0.94) * 100}%
                  </span>
                </div>
                <p className="text-xs text-[var(--muted)] mt-0.5 font-mono">{response?.model_provider}</p>
              </div>

              <div className="text-xs">
                <span className="text-[var(--muted)]">Uncertainty Rating: </span>
                <span className="font-bold text-emerald-400">{response?.uncertainty_rating}</span>
              </div>
            </div>

            {/* Unani vs Biomedical Dual Perspective */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="p-4 rounded-xl bg-[var(--elevated)] border border-[var(--border)] space-y-2">
                <div className="flex items-center gap-1.5 font-bold text-emerald-400">
                  <span>🌿</span>
                  <span>Classical Unani Nosology & Humorology</span>
                </div>
                <p className="text-[var(--text)] leading-relaxed">{response?.unani_reasoning}</p>
              </div>

              <div className="p-4 rounded-xl bg-[var(--elevated)] border border-[var(--border)] space-y-2">
                <div className="flex items-center gap-1.5 font-bold text-blue-400">
                  <span>🔬</span>
                  <span>Modern Biomedical & Pathological Correlates</span>
                </div>
                <p className="text-[var(--text)] leading-relaxed">{response?.biomedical_correlates}</p>
              </div>
            </div>

            {/* Differential Diagnoses & Investigations */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="p-4 rounded-xl bg-[var(--elevated)] border border-[var(--border)] space-y-2">
                <span className="font-bold text-[var(--gold-soft)] block">Differential Diagnostic Considerations</span>
                <ul className="space-y-1.5 list-disc list-inside text-[var(--text)]">
                  {response?.differential_diagnoses.map((d, i) => (
                    <li key={i}>{d}</li>
                  ))}
                </ul>
              </div>

              <div className="p-4 rounded-xl bg-[var(--elevated)] border border-[var(--border)] space-y-2">
                <span className="font-bold text-purple-400 block">Recommended Diagnostic Investigations</span>
                <ul className="space-y-1.5 list-disc list-inside text-[var(--text)]">
                  {response?.recommended_investigations.map((inv, i) => (
                    <li key={i}>{inv}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Red Flags & Emergency Triaging */}
            <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-xs space-y-1.5">
              <span className="font-bold text-amber-400 flex items-center gap-1.5">
                <span>⚠️</span>
                <span>Triage & Clinical Safety Warnings</span>
              </span>
              <ul className="space-y-1 text-[var(--text)] list-disc list-inside">
                {response?.red_flags.map((rf, i) => (
                  <li key={i}>{rf}</li>
                ))}
              </ul>
            </div>

            {/* Evidence Citations */}
            <div className="pt-2 border-t border-[var(--border)] space-y-2 text-xs">
              <span className="font-bold text-[var(--muted)] uppercase tracking-wider text-[10px] block">
                Evidence Citations & Knowledge Graph Provenance
              </span>
              <ul className="space-y-1 font-mono text-[11px] text-[var(--muted)]">
                {response?.citations.map((c, i) => (
                  <li key={i} className="hover:text-white transition-colors">• {c}</li>
                ))}
              </ul>
            </div>

          </div>

        </div>

      </main>
    </div>
  );
}
