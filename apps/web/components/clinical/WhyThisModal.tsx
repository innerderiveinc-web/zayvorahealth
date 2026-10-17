"use client";

import React from "react";

export interface WhyThisExplanation {
  itemId: string;
  itemTitle: string;
  category: "NUSKHA" | "TADBEER" | "AHARA" | "INVESTIGATION" | "CDS_RECOMMENDATION";
  clinicalRationale: string;
  classicalAuthority: {
    sourceText: string;
    chapterVolume: string;
    formulationPrinciple: string;
  };
  evidenceLevel: "E0" | "E1" | "E2" | "E3" | "E4" | "E5" | "E6";
  evidenceDescription: string;
  mizajConcordance: {
    targetMizaj: string;
    formulationMizaj: string;
    mechanismOfCorrection: string;
  };
  muslehBalancing: {
    muslehAgent: string;
    correctiveAction: string;
  };
  badraqaConduit: {
    vehicle: string;
    organDeliveryRole: string;
  };
  safetyBoundaries: {
    scheduleE1Status: boolean;
    maximumDailyDose: string;
    knownContraindications: string[];
    monitoringRequirements: string[];
  };
  governanceMetadata: {
    zkbVersion: string;
    zfieVersion: string;
    lastVerifiedDate: string;
    verifiedBy: string;
  };
}

interface WhyThisModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: WhyThisExplanation | null;
}

export function WhyThisModal({ isOpen, onClose, data }: WhyThisModalProps) {
  if (!isOpen || !data) return null;

  const evidenceLevelBadgeColor = {
    E0: "bg-gray-100 text-gray-700 border-gray-300",
    E1: "bg-blue-50 text-blue-700 border-blue-200",
    E2: "bg-indigo-50 text-indigo-700 border-indigo-200",
    E3: "bg-purple-50 text-purple-700 border-purple-200",
    E4: "bg-amber-50 text-amber-700 border-amber-200",
    E5: "bg-emerald-50 text-emerald-700 border-emerald-300",
    E6: "bg-green-100 text-green-800 border-green-400 font-bold",
  }[data.evidenceLevel] || "bg-gray-100 text-gray-700 border-gray-300";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in"
      role="dialog"
      aria-modal="true"
      aria-labelledby="why-this-title"
    >
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] flex flex-col border border-emerald-900/10 overflow-hidden">
        {/* Header */}
        <div className="p-5 bg-gradient-to-r from-emerald-900 to-[#1B4332] text-white flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <span className="p-2 rounded-xl bg-white/10 text-emerald-300 text-lg">💡</span>
            <div>
              <div className="text-xs font-semibold tracking-wider uppercase text-emerald-200">
                Scientific & Classical Explainability • Master Blueprint §63
              </div>
              <h2 id="why-this-title" className="text-lg font-bold text-white">
                Why this recommendation?
              </h2>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-emerald-200 hover:text-white hover:bg-white/10 transition"
            aria-label="Close explainability modal"
          >
            ✕
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-sm text-gray-700">
          {/* Target Item Header */}
          <div className="flex items-center justify-between p-3.5 rounded-xl bg-emerald-50/70 border border-emerald-100">
            <div>
              <div className="text-xs uppercase tracking-wider font-semibold text-emerald-800">
                {data.category.replace("_", " ")}
              </div>
              <div className="text-base font-bold text-emerald-950">{data.itemTitle}</div>
            </div>
            <div className={`px-2.5 py-1 rounded-full text-xs border ${evidenceLevelBadgeColor}`}>
              Evidence: {data.evidenceLevel} ({data.evidenceDescription})
            </div>
          </div>

          {/* 1. Clinical Rationale */}
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-1.5 flex items-center gap-1.5">
              <span>🩺</span> Clinical Rationale & Objective
            </h3>
            <p className="p-3 bg-gray-50 rounded-xl border border-gray-200/80 leading-relaxed text-gray-800">
              {data.clinicalRationale}
            </p>
          </div>

          {/* 2. Classical Unani Authority & Canon */}
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-1.5 flex items-center gap-1.5">
              <span>📜</span> Classical Textual Authority (Canonical Canon)
            </h3>
            <div className="p-3 bg-amber-50/60 rounded-xl border border-amber-200/70 space-y-1 text-xs text-amber-950">
              <div><strong className="font-semibold">Source Text:</strong> {data.classicalAuthority.sourceText} ({data.classicalAuthority.chapterVolume})</div>
              <div><strong className="font-semibold">Therapeutic Principle:</strong> {data.classicalAuthority.formulationPrinciple}</div>
            </div>
          </div>

          {/* 3. Mizaj Concordance & Humoral Correction */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="p-3 bg-blue-50/60 rounded-xl border border-blue-200/70 space-y-1 text-xs text-blue-950">
              <div className="font-bold text-blue-900 mb-1 flex items-center gap-1">
                <span>⚖️</span> Mizaj Concordance
              </div>
              <div><strong>Target Dyscrasia:</strong> {data.mizajConcordance.targetMizaj}</div>
              <div><strong>Item Temperament:</strong> {data.mizajConcordance.formulationMizaj}</div>
              <div className="text-[11px] text-blue-800 pt-1 leading-snug">{data.mizajConcordance.mechanismOfCorrection}</div>
            </div>

            {/* 4. Musleh & Badraqa Integration */}
            <div className="p-3 bg-emerald-50/60 rounded-xl border border-emerald-200/70 space-y-1 text-xs text-emerald-950">
              <div className="font-bold text-emerald-900 mb-1 flex items-center gap-1">
                <span>🛡️</span> Musleh & Badraqa Balance
              </div>
              <div><strong>Musleh (Corrective):</strong> {data.muslehBalancing.muslehAgent} ({data.muslehBalancing.correctiveAction})</div>
              <div><strong>Badraqa (Conduit):</strong> {data.badraqaConduit.vehicle} ({data.badraqaConduit.organDeliveryRole})</div>
            </div>
          </div>

          {/* 5. Safety Boundaries & Guardrails */}
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-1.5 flex items-center gap-1.5">
              <span>⚠️</span> Safety Guardrails & Monitoring Constraints
            </h3>
            <div className="p-3 bg-rose-50/50 rounded-xl border border-rose-200/70 text-xs space-y-1 text-rose-950">
              <div className="flex items-center gap-2">
                <strong>Schedule E(1) Poison Status:</strong>
                <span className={data.safetyBoundaries.scheduleE1Status ? "font-bold text-rose-700" : "text-emerald-700"}>
                  {data.safetyBoundaries.scheduleE1Status ? "YES — Mudabbar (Detoxification) Required" : "NO — Standard Botanical Monograph"}
                </span>
              </div>
              <div><strong>Maximum Single/Daily Dose:</strong> {data.safetyBoundaries.maximumDailyDose}</div>
              <div><strong>Contraindications:</strong> {data.safetyBoundaries.knownContraindications.join(", ")}</div>
              <div><strong>Monitoring:</strong> {data.safetyBoundaries.monitoringRequirements.join("; ")}</div>
            </div>
          </div>

          {/* 6. Scientific Traceability & Audit Metadata */}
          <div className="pt-2 border-t border-gray-200 flex flex-wrap items-center justify-between text-[11px] text-gray-500">
            <div>Knowledge Base: <strong>{data.governanceMetadata.zkbVersion}</strong> | ZFIE: <strong>{data.governanceMetadata.zfieVersion}</strong></div>
            <div>Verified By: <strong>{data.governanceMetadata.verifiedBy}</strong> on {data.governanceMetadata.lastVerifiedDate}</div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="p-4 bg-gray-50 border-t border-gray-200 flex items-center justify-between">
          <span className="text-xs text-gray-500 italic">
            ZAYVORA Clinical Governance • Explainable Medical Intelligence
          </span>
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-emerald-800 hover:bg-emerald-900 text-white font-medium text-xs shadow-sm transition"
          >
            Understood & Close
          </button>
        </div>
      </div>
    </div>
  );
}
