"use client";

import React, { useState } from "react";
import {
  multimodalApi,
  type LabExtractionResult,
  type PhysicalSignsResult,
} from "@/lib/multimodalApi";

interface MultimodalLabCockpitProps {
  token: string;
  patientId: string;
  patientName: string;
}

const SAMPLE_LAB_PRESETS = [
  {
    label: "Niqras / Gout with Renal Impairment",
    text: `CLINICAL BIOCHEMISTRY REPORT
Patient: Sample Patient, Age: 54, Male
------------------------------------------------
Serum Uric Acid: 9.4 mg/dL (Ref: 3.5 - 7.2)
Serum Creatinine: 1.8 mg/dL (Ref: 0.6 - 1.2)
Fasting Blood Glucose: 104 mg/dL (Ref: 70 - 99)
Total Bilirubin: 0.9 mg/dL (Ref: 0.2 - 1.2)
ESR: 38 mm/hr (Ref: 0 - 20)
hs-CRP: 4.2 mg/L (Ref: 0.0 - 1.0)`,
  },
  {
    label: "Diabesity & Metabolic Cold Dysregulation",
    text: `ENDOCRINE & METABOLIC PANEL
Patient: Sample Patient, Age: 48, Female
------------------------------------------------
Fasting Blood Glucose: 182 mg/dL (Ref: 70 - 99)
HbA1c: 8.8 % (Ref: 4.0 - 5.6)
Serum Creatinine: 0.9 mg/dL (Ref: 0.6 - 1.2)
Serum Uric Acid: 5.2 mg/dL (Ref: 3.5 - 7.2)
hs-CRP: 2.8 mg/L (Ref: 0.0 - 1.0)`,
  },
  {
    label: "Hepatobiliary Safrawi Heat & Yarqan",
    text: `HEPATIC FUNCTION PANEL
Patient: Sample Patient, Age: 39, Male
------------------------------------------------
Total Bilirubin: 3.6 mg/dL (Ref: 0.2 - 1.2)
ALT (SGPT): 128 U/L (Ref: 7 - 56)
AST (SGOT): 96 U/L (Ref: 10 - 40)
Serum Creatinine: 0.8 mg/dL (Ref: 0.6 - 1.2)
ESR: 24 mm/hr (Ref: 0 - 20)`,
  },
];

export function MultimodalLabCockpit({
  token,
  patientId,
  patientName,
}: MultimodalLabCockpitProps) {
  const [labText, setLabText] = useState(SAMPLE_LAB_PRESETS[0].text);
  const [isExtracting, setIsExtracting] = useState(false);
  const [labResult, setLabResult] = useState<LabExtractionResult | null>(null);

  // Physical signs state
  const [tongueNotes, setTongueNotes] = useState("Thick yellow coat with prominent dry fissured surface (Asfar Yabis)");
  const [skinNotes, setSkinNotes] = useState("Depigmented porcelain-white macules on extensor forearms (Bars / Vitiligo)");
  const [isAnalyzingSigns, setIsAnalyzingSigns] = useState(false);
  const [signsResult, setSignsResult] = useState<PhysicalSignsResult | null>(null);

  const handleExtractLab = async () => {
    setIsExtracting(true);
    try {
      const res = await multimodalApi.extractLabReport(token, {
        text: labText,
        patient_age: 54,
        patient_gender: "M",
      });
      setLabResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsExtracting(false);
    }
  };

  const handleAnalyzeSigns = async () => {
    setIsAnalyzingSigns(true);
    try {
      const res = await multimodalApi.analyzePhysicalSigns(token, {
        tongue_notes: tongueNotes,
        skin_notes: skinNotes,
      });
      setSignsResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsAnalyzingSigns(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="zv-panel p-5 bg-[#121712] border border-[#24302a] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xl">🧪</span>
            <h2 className="text-base font-serif font-semibold text-[#e3c884]">
              Multimodal Clinical Lab & Physical Signs Extractor
            </h2>
            <span className="px-2 py-0.5 text-[10px] font-mono rounded-full bg-[#182a1d] text-[#2ea87f] border border-[#2ea87f]/40">
              Horizon 3 AI Runtime
            </span>
          </div>
          <p className="text-xs text-[#8a9490] mt-1">
            Standardized LOINC extraction, CKD-EPI renal safety scaling, and Unani humoral synthesis for{" "}
            <span className="text-[#ece8dd] font-medium">{patientName}</span>.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-2.5 py-1 text-xs font-mono font-semibold rounded bg-[#2e1919] text-[#e06c75] border border-[#e06c75]/40">
            safe_to_lock: FALSE
          </span>
          <span className="px-2.5 py-1 text-xs font-mono rounded bg-[#18231d] text-[#e3c884] border border-[#e3c884]/40">
            LOINC 2.77 + UPI Compliant
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Section 1: Laboratory Report Extractor */}
        <div className="zv-panel p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-[#ece8dd] flex items-center gap-2">
              <span>📋</span> Laboratory Text & LOINC Ingestion
            </h3>
            <span className="text-[10px] text-[#8a9490]">Dual-Evidence Invariant</span>
          </div>

          <div className="flex flex-wrap gap-2">
            {SAMPLE_LAB_PRESETS.map((preset, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => setLabText(preset.text)}
                className="px-2.5 py-1 text-[11px] rounded bg-[#1a231d] text-[#8a9490] hover:text-[#e3c884] hover:bg-[#202b24] border border-[#24302a] transition cursor-pointer"
              >
                {preset.label}
              </button>
            ))}
          </div>

          <textarea
            value={labText}
            onChange={(e) => setLabText(e.target.value)}
            rows={8}
            className="zv-input font-mono text-xs w-full bg-[#0d120e] text-[#ece8dd]"
            placeholder="Paste raw laboratory report text or enter clinical observations..."
          />

          <button
            onClick={handleExtractLab}
            disabled={isExtracting}
            className="zv-btn-primary w-full py-2 text-xs font-semibold flex items-center justify-center gap-2"
          >
            {isExtracting ? (
              <span>Extracting LOINC Analytes...</span>
            ) : (
              <>
                <span>⚡ Run Multimodal Structured Extraction</span>
              </>
            )}
          </button>
        </div>

        {/* Section 2: Physical Signs Semiotic Analyzer */}
        <div className="zv-panel p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-[#ece8dd] flex items-center gap-2">
              <span>👅</span> Classical Physical Signs (Alamat-e-Amraz)
            </h3>
            <span className="text-[10px] text-[#8a9490]">Tongue & Dermatological</span>
          </div>

          <div className="space-y-3">
            <div>
              <label className="zv-label">Tongue Inspection (Sabagh & Rutoobat)</label>
              <input
                type="text"
                value={tongueNotes}
                onChange={(e) => setTongueNotes(e.target.value)}
                className="zv-input text-xs"
                placeholder="e.g. Yellow thick dry coat (Asfar Yabis)..."
              />
            </div>

            <div>
              <label className="zv-label">Cutaneous Lesion Notes (Amraz-e-Jildiyyah)</label>
              <input
                type="text"
                value={skinNotes}
                onChange={(e) => setSkinNotes(e.target.value)}
                className="zv-input text-xs"
                placeholder="e.g. Vitiligo / Bars, Qooba, Bahaq Aswad..."
              />
            </div>
          </div>

          <button
            onClick={handleAnalyzeSigns}
            disabled={isAnalyzingSigns}
            className="w-full py-2 px-4 text-xs font-semibold rounded bg-[#1f3326] text-[#2ea87f] hover:bg-[#284433] border border-[#2ea87f]/40 transition cursor-pointer"
          >
            {isAnalyzingSigns ? "Classifying Semiotics..." : "🔍 Analyze Physical Signs & Tadbeer"}
          </button>
        </div>
      </div>

      {/* Lab Results Display */}
      {labResult && (
        <div className="space-y-6">
          {/* Renal Safety Alert Banner */}
          {labResult.renal_safety && (
            <div
              className={`p-4 rounded-lg border flex flex-col md:flex-row items-start md:items-center justify-between gap-3 ${
                labResult.renal_safety.requires_dose_adjustment
                  ? "bg-[#331c17] border-[#e06c75] text-[#f5a7a7]"
                  : "bg-[#142619] border-[#2ea87f] text-[#9be3b5]"
              }`}
            >
              <div>
                <div className="flex items-center gap-2 font-bold text-sm">
                  <span>⚠️</span>
                  <span>Renal Safety Posology Assessment: {labResult.renal_safety.renal_stage}</span>
                  <span className="text-xs font-mono font-normal">
                    (eGFR: {labResult.renal_safety.egfr_value} mL/min/1.73m²)
                  </span>
                </div>
                <p className="text-xs mt-1 text-[#ece8dd]">
                  {labResult.renal_safety.safety_advisory}
                </p>
                {labResult.renal_safety.contraindicated_herbs.length > 0 && (
                  <p className="text-[11px] text-[#e06c75] mt-1 font-semibold">
                    Contraindicated Herbs: {labResult.renal_safety.contraindicated_herbs.join(", ")}
                  </p>
                )}
              </div>

              <div className="text-right">
                <span className="text-xs uppercase tracking-wide block text-[#8a9490]">Recommended Dose Scaling</span>
                <span className="text-lg font-mono font-bold text-[#e3c884]">
                  {Math.round(labResult.renal_safety.recommended_dose_scaling_factor * 100)}%
                </span>
              </div>
            </div>
          )}

          {/* Analytes & Humoral Synthesis Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Analytes List (2 Cols) */}
            <div className="lg:col-span-2 zv-panel p-5 space-y-3">
              <h4 className="text-xs font-serif font-semibold text-[#e3c884] uppercase tracking-wider">
                Extracted LOINC Analytes & Physiological Interpretations ({labResult.analytes.length})
              </h4>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs border-collapse">
                  <thead>
                    <tr className="border-b border-[#24302a] text-[#8a9490]">
                      <th className="py-2 px-2">Analyte</th>
                      <th className="py-2 px-2">LOINC</th>
                      <th className="py-2 px-2">Value</th>
                      <th className="py-2 px-2">Reference</th>
                      <th className="py-2 px-2">Status</th>
                      <th className="py-2 px-2">Unani Humoral Correlation</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#1e2922]">
                    {labResult.analytes.map((a, i) => (
                      <tr key={i} className="hover:bg-[#162018] transition">
                        <td className="py-2.5 px-2 font-medium text-[#ece8dd]">{a.analyte_name}</td>
                        <td className="py-2.5 px-2 font-mono text-[11px] text-[#8a9490]">{a.loinc_code}</td>
                        <td className="py-2.5 px-2 font-mono font-bold text-[#e3c884]">
                          {a.measured_value} {a.unit}
                        </td>
                        <td className="py-2.5 px-2 text-[#8a9490] text-[11px]">{a.reference_range}</td>
                        <td className="py-2.5 px-2">
                          <span
                            className={`px-2 py-0.5 text-[10px] font-semibold rounded ${
                              a.interpretation === "NORMAL"
                                ? "bg-[#182a1d] text-[#2ea87f]"
                                : a.interpretation.includes("CRITICAL")
                                ? "bg-[#451616] text-[#e06c75] font-bold"
                                : "bg-[#332815] text-[#e3c884]"
                            }`}
                          >
                            {a.interpretation}
                          </span>
                        </td>
                        <td className="py-2.5 px-2 text-[#9ba39f] text-[11px] max-w-xs">
                          {a.unani_humoral_correlation}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Humoral Synthesis (1 Col) */}
            <div className="zv-panel p-5 space-y-4 bg-[#141b15] border border-[#2ea87f]/30">
              <h4 className="text-xs font-serif font-semibold text-[#e3c884] uppercase tracking-wider flex items-center gap-2">
                <span>🌿</span> Unani Humoral Synthesis
              </h4>

              <div className="space-y-3 text-xs">
                <div>
                  <span className="text-[#8a9490] block text-[11px]">Dominant Humor Burden:</span>
                  <span className="text-sm font-semibold text-[#2ea87f]">
                    {labResult.humoral_synthesis.dominant_humor_burden}
                  </span>
                </div>

                <div>
                  <span className="text-[#8a9490] block text-[11px]">Inflammatory Status:</span>
                  <span className="text-xs font-medium text-[#e3c884]">
                    {labResult.humoral_synthesis.inflammatory_status}
                  </span>
                </div>

                <div>
                  <span className="text-[#8a9490] block text-[11px]">Pathological Entities Correlated:</span>
                  <ul className="list-disc list-inside text-[#ece8dd] space-y-1 mt-1">
                    {labResult.humoral_synthesis.pathological_entities.map((p, i) => (
                      <li key={i}>{p}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <span className="text-[#8a9490] block text-[11px]">Organ Axes Implicated:</span>
                  <div className="flex flex-wrap gap-1.5 mt-1">
                    {labResult.humoral_synthesis.organ_axes_implicated.map((axis, i) => (
                      <span key={i} className="px-2 py-0.5 rounded text-[10px] bg-[#1a2920] text-[#ece8dd]">
                        {axis}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="p-3 bg-[#111712] rounded border border-[#24302a] text-[11px] text-[#8a9490]">
                  {labResult.humoral_synthesis.synthesis_notes}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Physical Signs Results Display */}
      {signsResult && (
        <div className="zv-panel p-5 space-y-4 border border-[#e3c884]/40 bg-[#141b15]">
          <h4 className="text-xs font-serif font-semibold text-[#e3c884] uppercase tracking-wider flex items-center gap-2">
            <span>👁️</span> Physical Signs Semiotic Synthesis & Recommended Tadbeer
          </h4>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            {signsResult.tongue_finding && (
              <div className="p-4 bg-[#111712] rounded border border-[#24302a] space-y-2">
                <span className="text-[11px] font-semibold text-[#e3c884]">👅 Tongue Findings (Lisan):</span>
                <p className="text-[#ece8dd]">
                  <strong className="text-[#8a9490]">Coating:</strong> {signsResult.tongue_finding.coating_color} |{" "}
                  <strong className="text-[#8a9490]">Moisture:</strong> {signsResult.tongue_finding.moisture}
                </p>
                <p className="text-[#2ea87f]">
                  <strong>Humoral Inference:</strong> {signsResult.tongue_finding.humoral_inference}
                </p>
              </div>
            )}

            {signsResult.skin_finding && (
              <div className="p-4 bg-[#111712] rounded border border-[#24302a] space-y-2">
                <span className="text-[11px] font-semibold text-[#e3c884]">🧴 Cutaneous Signs (Jild):</span>
                <p className="text-[#ece8dd]">
                  <strong className="text-[#8a9490]">Entity:</strong> {signsResult.skin_finding.lesion_type}
                </p>
                <p className="text-[#9ba39f] text-[11px]">{signsResult.skin_finding.pathophysiology}</p>
              </div>
            )}
          </div>

          {signsResult.suggested_tadbeer.length > 0 && (
            <div className="p-3 bg-[#111712] rounded border border-[#2ea87f]/30">
              <span className="text-[11px] font-semibold text-[#2ea87f] block mb-1">
                Suggested Regimenal Therapies (Ilaj-bit-Tadbeer):
              </span>
              <div className="flex flex-wrap gap-2">
                {signsResult.suggested_tadbeer.map((t, idx) => (
                  <span
                    key={idx}
                    className="px-2.5 py-1 text-xs rounded bg-[#182a1d] text-[#ece8dd] border border-[#2ea87f]/40 font-medium"
                  >
                    ✦ {t}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
