"use client";

import React, { useState, useEffect } from "react";

export default function TwelveAxesCockpitPage() {
  const [patientMap, setPatientMap] = useState<any>(null);
  const [aiDraft, setAiDraft] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [doctorApproved, setDoctorApproved] = useState(false);

  // Sample patient data to evaluate
  const [patientData, setPatientData] = useState({
    patient_id: "MRN-2026-0814",
    mizaj: "Bard-Ratab",
    axes: {
      AXIS_01: { symptoms_score: 55, history_score: 40, investigations_score: 60, lifestyle_score: 50, clinician_assessment: 60 },
      AXIS_02: { symptoms_score: 70, history_score: 65, investigations_score: 75, lifestyle_score: 60, clinician_assessment: 70 },
      AXIS_03: { symptoms_score: 45, history_score: 30, investigations_score: 40, lifestyle_score: 40, clinician_assessment: 40 },
      AXIS_04: { symptoms_score: 60, history_score: 50, investigations_score: 65, lifestyle_score: 45, clinician_assessment: 60 },
      AXIS_06: { symptoms_score: 65, history_score: 50, investigations_score: 50, lifestyle_score: 70, clinician_assessment: 60 },
      AXIS_07: { symptoms_score: 40, history_score: 30, investigations_score: 35, lifestyle_score: 40, clinician_assessment: 35 }
    }
  });

  const load12AxisMap = async () => {
    setLoading(true);
    try {
      const [mapRes, draftRes] = await Promise.all([
        fetch("/api/v1/clinical/axes-12/patient-map", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ patient_data: patientData })
        }).then(r => r.json()),
        fetch("/api/v1/clinical/axes-12/ai-draft", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            reported_symptoms: ["bloating", "constipation", "fatigue"],
            biomarkers: { fbg: 112, hba1c: 6.3 },
            mizaj: "Bard-Ratab"
          })
        }).then(r => r.json())
      ]);

      if (mapRes.ok) setPatientMap(mapRes.patient_360_map);
      if (draftRes.ok) setAiDraft(draftRes.hakeem_sahab_draft);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load12AxisMap();
  }, []);

  return (
    <div className="min-h-screen bg-[#FAFAF7] p-8 text-neutral-900 font-sans">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header with Mandatory Label */}
        <div className="border-b border-neutral-200 pb-4">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2">
            <div>
              <span className="text-xs font-bold uppercase tracking-widest text-[#2D6A4F] bg-emerald-50 px-2.5 py-1 rounded">
                ZAYVORA Health OS™ · Clinical Intelligence
              </span>
              <h1 className="text-3xl font-serif font-bold text-neutral-900 mt-2">
                12 Organ-Axis Health Map (Patient 360)
              </h1>
              <p className="text-xs text-neutral-500 mt-1 max-w-2xl">
                ZAYVORA 12-Axis Clinical Intelligence Framework™ — Proposed Proprietary Clinical Architecture; advisory decision-support layer, not a replacement for clinician-validated diagnosis.
              </p>
            </div>
            <div className="text-right">
              <div className="inline-block px-3 py-1.5 bg-neutral-100 border border-neutral-300 rounded text-xs font-medium text-neutral-700">
                Patient: <span className="font-bold text-neutral-900">{patientData.patient_id}</span> | Mizaj: <span className="font-bold text-[#2D6A4F]">{patientData.mizaj}</span>
              </div>
            </div>
          </div>
        </div>

        {/* 12-Axis Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {patientMap?.axes?.map((ax: any) => {
            const isHigh = ax.status === "High Concern";
            const isMod = ax.status === "Moderate Concern";
            const isLow = ax.status === "Low Concern";
            const isRed = ax.status === "Red Flag";

            return (
              <div
                key={ax.axis_id}
                className={`p-4 rounded-xl border transition-all ${
                  isRed
                    ? "bg-red-50 border-red-300 text-red-950"
                    : isHigh
                    ? "bg-amber-50 border-amber-300 text-amber-950"
                    : isMod
                    ? "bg-yellow-50/50 border-yellow-200 text-yellow-950"
                    : isLow
                    ? "bg-emerald-50/50 border-emerald-200 text-emerald-950"
                    : "bg-white border-neutral-200 text-neutral-500"
                }`}
              >
                <div className="flex justify-between items-start">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-neutral-500">
                    {ax.axis_id}
                  </span>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                      isRed
                        ? "bg-red-200 text-red-900"
                        : isHigh
                        ? "bg-amber-200 text-amber-900"
                        : isMod
                        ? "bg-yellow-200 text-yellow-900"
                        : isLow
                        ? "bg-emerald-200 text-emerald-900"
                        : "bg-neutral-100 text-neutral-600"
                    }`}
                  >
                    {ax.status}
                  </span>
                </div>

                <h3 className="font-serif font-bold text-sm mt-2 text-neutral-900">{ax.axis_name}</h3>
                <div className="text-2xl font-bold mt-1 text-neutral-800">
                  {ax.activity_index > 0 ? ax.activity_index : "—"}
                  {ax.activity_index > 0 && <span className="text-xs font-normal text-neutral-500"> / 100</span>}
                </div>
                <p className="text-xs text-neutral-600 mt-1">{ax.ui_meaning}</p>

                {ax.foundational_core_links?.length > 0 && (
                  <div className="mt-3 pt-2 border-t border-neutral-200/60 flex flex-wrap gap-1">
                    {ax.foundational_core_links.map((link: string, idx: number) => (
                      <span key={idx} className="text-[9px] bg-white border px-1.5 py-0.5 rounded text-neutral-600 font-mono">
                        {link}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Hakeem Sahab AI Draft & Clinician Signoff Box */}
        {aiDraft && (
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <div>
                <span className="text-xs font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded">
                  Hakeem Sahab AI Copilot
                </span>
                <h2 className="text-lg font-serif font-bold text-neutral-900 mt-1">
                  Advisory Clinical Pattern Summary (Draft)
                </h2>
              </div>
              <div>
                <span className="text-xs font-mono text-amber-800 bg-amber-50 border border-amber-200 px-2.5 py-1 rounded">
                  {doctorApproved ? "✓ Clinician Signed & Validated" : "Pending Clinician Approval"}
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div className="space-y-2">
                <h4 className="font-bold text-xs uppercase tracking-wider text-neutral-600">Possible Relevant Axes</h4>
                <ul className="list-disc list-inside space-y-1 text-neutral-800">
                  {aiDraft.possible_relevant_axes.map((ax: any, idx: number) => (
                    <li key={idx}>
                      <strong>{ax.axis}</strong>: {ax.recommendation}
                    </li>
                  ))}
                </ul>

                <h4 className="font-bold text-xs uppercase tracking-wider text-neutral-600 pt-2">Supporting Observations</h4>
                <ul className="list-disc list-inside space-y-1 text-neutral-700">
                  {aiDraft.supporting_observations.map((obs: string, idx: number) => (
                    <li key={idx}>{obs}</li>
                  ))}
                </ul>
              </div>

              <div className="space-y-2">
                <h4 className="font-bold text-xs uppercase tracking-wider text-neutral-600">Missing Information Needed</h4>
                <ul className="list-disc list-inside space-y-1 text-amber-900 bg-amber-50/60 p-3 rounded-lg border border-amber-200">
                  {aiDraft.missing_information.map((info: string, idx: number) => (
                    <li key={idx}>{info}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Approval Footer */}
            <div className="pt-4 border-t flex items-center justify-between">
              <p className="text-xs text-neutral-500 max-w-xl">
                {aiDraft.advisory_notice}
              </p>
              <button
                onClick={() => setDoctorApproved(!doctorApproved)}
                className={`px-5 py-2 rounded-lg text-sm font-medium transition-colors shadow ${
                  doctorApproved
                    ? "bg-neutral-800 text-white hover:bg-neutral-900"
                    : "bg-[#2D6A4F] text-white hover:bg-[#1B4332]"
                }`}
              >
                {doctorApproved ? "Revoke Signoff" : "Doctor Review & Approve Care Plan"}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
