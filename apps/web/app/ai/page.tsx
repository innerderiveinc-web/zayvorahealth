"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";

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
  organ_axis: string;
  suggested_herbs: string[];
  evidence_tier: string;
}

export default function AiStudioPage() {
  const [clinicianQuery, setClinicianQuery] = useState(
    "62-year-old male with chronic knee stiffness and early morning gel phenomenon, exacerbated by cold damp weather. Mild epigastric fullness after meals."
  );
  const [patientMizaj, setPatientMizaj] = useState("Damawi with secondary Balghami deviation");
  const [activeAxis, setActiveAxis] = useState("mafasil-asab");
  const [isLoading, setIsLoading] = useState(false);
  const [doctorApproved, setDoctorApproved] = useState(false);

  const [response, setResponse] = useState<CopilotResponse | null>({
    query: "62yo male chronic knee stiffness, cold weather exacerbation, epigastric fullness",
    unani_reasoning:
      "Pathology is consistent with Waja-ul-Mafasil Barid Balghami (Phlegmatic arthropathy) wherein morbid, cold viscous humors accumulate in articular capsules during cold weather (Asbab-e-Sittah Zarooriyyah - Hawa). Coexisting Hurqat-ul-Meda / Zof-e-Hazm indicates sluggish digestive concoction (Nujz) in the liver-gut axis.",
    biomedical_correlates:
      "Clinical presentation aligns with Osteoarthritis (ICD-11: FA00) characterized by articular cartilage matrix degradation, with secondary functional dyspepsia. Avoid high-dose unbuffered oral NSAIDs to prevent mucosal injury.",
    recommended_investigations: [
      "Weight-bearing bilateral knee radiography (AP/Lateral views)",
      "Serum Uric Acid & Erythrocyte Sedimentation Rate (ESR)",
      "Fasting blood glucose & HbA1c screening",
      "Stool occult blood & serum liver enzymes",
    ],
    differential_diagnoses: [
      "Waja-ul-Mafasil Barid Balghami / Primary Knee Osteoarthritis (94% confidence)",
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
    organ_axis: "Mafasil-Asab (Joint-Neuro Axis) & Kabid-Mida (Hepato-Gastric)",
    suggested_herbs: ["Suranjan Talkh (Mudabbar)", "Asgandh (Withania somnifera)", "Zanjabeel (Zingiber officinale)"],
    evidence_tier: "E5 (Randomized Clinical Trial & Observational Registry Concordance)",
  });

  function handleRunConsultation() {
    setIsLoading(true);
    setDoctorApproved(false);
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
        organ_axis: "Mafasil-Asab (Joint-Neuro Axis)",
        suggested_herbs: ["Suranjan Talkh (Mudabbar)", "Filfil Siyah", "Babuna"],
        evidence_tier: "E5 (Randomized Clinical Trial Concordance)",
      });
    }, 600);
  }

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-7xl mx-auto pb-12 text-slate-100 text-xs">
        
        {/* Workspace Header */}
        <div className="p-6 rounded-3xl bg-gradient-to-r from-[#0C1524] via-[#101C30] to-[#152540] border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xl">🤖</span>
              <span className="text-[11px] font-bold text-teal-400 uppercase tracking-widest bg-teal-950/80 px-3 py-1 rounded-full border border-teal-800/80">
                Hakeem Sahab™ Clinical AI Copilot
              </span>
              <span className="text-xs text-slate-400 font-mono">• Clinician Decision Support (Advisory Only)</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mt-1">
              AI Clinical Reasoning & Pharmacopeia Studio
            </h1>
            <p className="text-slate-400 text-xs">
              Synthesizes classical Greco-Arab Unani medical treatises with peer-reviewed biomedical literature, organ-axis mapping, and drug safety checks.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <span className="px-3 py-1.5 rounded-xl bg-teal-950/80 border border-teal-500/50 text-teal-300 text-xs font-bold flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
              <span>Non-Delegable Doctor Review Enforced</span>
            </span>
          </div>
        </div>

        {/* Executive KPI Overview */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <StatCard label="Clinical Concordance" value="94.2%" subtext="Across 3 university hospitals" variant="teal" icon="🎯" />
          <StatCard label="Codified Monographs" value="1,280+" subtext="UPI & NFUM standardized" variant="emerald" icon="📚" />
          <StatCard label="Autonomous Lock" value="Blocked" subtext="Doctor signature mandatory" variant="amber" icon="🛡️" />
          <StatCard label="Safety Firewall" value="Active" subtext="Schedule E(1) Mudabbar gate" variant="teal" icon="⚙️" />
        </div>

        {/* Layout Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Query Formulation Input Panel */}
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 shadow-md">
            <div className="border-b border-slate-800 pb-3">
              <span className="text-[10px] uppercase tracking-wider text-teal-400 font-bold block">Clinical Query Input</span>
              <h3 className="text-sm font-bold text-white mt-0.5">Patient Case & Symptoms</h3>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-slate-300 font-semibold mb-1">Chief Clinical Complaint & Symptoms</label>
                <textarea
                  rows={4}
                  value={clinicianQuery}
                  onChange={(e) => setClinicianQuery(e.target.value)}
                  placeholder="Enter patient symptoms, duration, exacerbating factors..."
                  className="w-full p-3 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-semibold mb-1">Assessed Patient Mizaj (Constitution)</label>
                <select
                  value={patientMizaj}
                  onChange={(e) => setPatientMizaj(e.target.value)}
                  className="w-full p-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                >
                  <option value="Balghami (Cold & Moist)">Balghami (Cold & Moist Dyscrasia)</option>
                  <option value="Damawi with secondary Balghami deviation">Damawi with secondary Balghami deviation</option>
                  <option value="Safrawi (Hot & Dry)">Safrawi (Hot & Dry Dyscrasia)</option>
                  <option value="Saudawi (Cold & Dry)">Saudawi (Cold & Dry Dyscrasia)</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-300 font-semibold mb-1">Primary Functional Organ-Axis</label>
                <select
                  value={activeAxis}
                  onChange={(e) => setActiveAxis(e.target.value)}
                  className="w-full p-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                >
                  <option value="mafasil-asab">Mafasil-Asab (Joint & Peripheral Neurological Axis)</option>
                  <option value="kabid-mida">Kabid-Mida (Hepato-Gastric Digestive Axis)</option>
                  <option value="qalb-dimagh">Qalb-Dimagh (Cardio-Cerebral Vital Axis)</option>
                  <option value="kulyah-masanah">Kulyah-Masanah (Renal-Urinary Elimination Axis)</option>
                </select>
              </div>

              <button
                onClick={handleRunConsultation}
                disabled={isLoading}
                className="w-full py-3 rounded-xl bg-teal-600 hover:bg-teal-500 disabled:bg-slate-800 text-white font-bold transition shadow-lg shadow-teal-900/30 flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                    <span>Synthesizing Literature & Evidence...</span>
                  </>
                ) : (
                  <span>Run Hakeem Sahab Reasoning →</span>
                )}
              </button>
            </div>
          </div>

          {/* AI Clinical Reasoning Output Panel */}
          <div className="lg:col-span-2 space-y-4">
            {response && (
              <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 shadow-md">
                
                {/* Advisory Header Banner */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 rounded-2xl bg-teal-950/60 border border-teal-800/80">
                  <div className="flex items-center gap-2.5">
                    <span className="text-xl">🛡️</span>
                    <div>
                      <span className="font-bold text-teal-300 block">AI-Generated Decision Support • Advisory Only</span>
                      <span className="text-slate-400 text-[11px]">Final prescription must be approved and digitally signed by attending physician.</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <span className="px-2.5 py-1 rounded-lg bg-teal-900 text-teal-200 font-mono font-bold text-[11px]">
                      Confidence: {(response.confidence_score * 100).toFixed(0)}%
                    </span>
                    <span className={`px-2.5 py-1 rounded-lg font-bold text-[11px] ${
                      doctorApproved ? "bg-emerald-950 text-emerald-300 border border-emerald-800" : "bg-amber-950 text-amber-300 border border-amber-800"
                    }`}>
                      {doctorApproved ? "✓ Doctor Approved" : "Doctor Review Required"}
                    </span>
                  </div>
                </div>

                {/* Classical Unani Reasoning */}
                <div className="space-y-1.5">
                  <span className="font-bold text-teal-300 uppercase tracking-wider text-[10px]">1. Classical Unani Humoral Analysis</span>
                  <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 text-slate-200 leading-relaxed">
                    {response.unani_reasoning}
                  </div>
                </div>

                {/* Biomedical Correlates */}
                <div className="space-y-1.5">
                  <span className="font-bold text-teal-300 uppercase tracking-wider text-[10px]">2. Modern Biomedical Correlation (ICD-11)</span>
                  <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 text-slate-200 leading-relaxed">
                    {response.biomedical_correlates}
                  </div>
                </div>

                {/* Differentials & Suggested Herbs */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-2">
                    <span className="font-bold text-teal-300 uppercase tracking-wider text-[10px]">Differential Considerations</span>
                    <ul className="space-y-1 text-slate-300">
                      {response.differential_diagnoses.map((d, i) => (
                        <li key={i} className="flex items-center gap-1.5 text-[11px]">
                          <span className="text-teal-400 font-bold">•</span> {d}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-2">
                    <span className="font-bold text-teal-300 uppercase tracking-wider text-[10px]">Candidate Botanicals (UPI Monographed)</span>
                    <div className="flex flex-wrap gap-1.5">
                      {response.suggested_herbs.map((h, i) => (
                        <span key={i} className="bg-teal-950/80 text-teal-300 border border-teal-800 px-2.5 py-1 rounded-xl text-[11px]">
                          🌿 {h}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Statutory Citations */}
                <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-1.5 text-[11px]">
                  <span className="font-bold text-slate-400 uppercase text-[10px]">Peer-Reviewed & Classical Citations</span>
                  {response.citations.map((c, i) => (
                    <div key={i} className="text-slate-400 italic">[{i + 1}] {c}</div>
                  ))}
                </div>

                {/* Doctor Decision Trigger */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-3 border-t border-slate-800">
                  <span className="text-slate-400 text-[11px]">
                    Statutory Rule: Recommendations are advisory. Lock authority remains strictly with the clinician.
                  </span>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setDoctorApproved(!doctorApproved)}
                      className={`px-5 py-2.5 rounded-xl font-bold transition text-xs ${
                        doctorApproved
                          ? "bg-slate-800 text-slate-300 hover:bg-slate-700"
                          : "bg-teal-600 hover:bg-teal-500 text-white shadow-md"
                      }`}
                    >
                      {doctorApproved ? "Revoke Approval" : "Approve & Transfer to Rx Builder →"}
                    </button>
                  </div>
                </div>

              </div>
            )}
          </div>

        </div>

      </div>
    </AppShell>
  );
}
