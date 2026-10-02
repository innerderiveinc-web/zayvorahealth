"use client";

import React, { useState } from "react";

export default function ZAPEConsolePage() {
  const [mizaj, setMizaj] = useState("Bard-Ratab");
  const [fbg, setFbg] = useState(115);
  const [hba1c, setHba1c] = useState(6.8);
  const [fastingInsulin, setFastingInsulin] = useState(18);
  const [sbp, setSbp] = useState(135);
  const [dbp, setDbp] = useState(88);
  const [hsCrp, setHsCrp] = useState(2.8);
  const [pss10, setPss10] = useState(18);
  const [bmi, setBmi] = useState(29.5);

  const [decisionSupport, setDecisionSupport] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleEvaluate = async () => {
    setLoading(true);
    try {
      const payload = {
        patient_id: "PAT-DEMO-001",
        mizaj,
        bmi,
        pss_10: pss10,
        sbp,
        dbp,
        fbg,
        hba1c,
        fasting_insulin: fastingInsulin,
        hs_crp: hsCrp,
        symptoms: ["fatigue", "bloating", "morning sluggishness"]
      };

      const res = await fetch("/api/v1/clinical/zape/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.ok) {
        setDecisionSupport(data.zape_decision_support);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FAFAF7] p-8 text-neutral-900 font-sans">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="border-b border-neutral-200 pb-4">
          <div className="flex items-center justify-between">
            <div>
              <span className="text-xs font-bold uppercase tracking-widest text-[#2D6A4F] bg-emerald-50 px-2.5 py-1 rounded">
                ZAYVORA Health OS™ · Global Edition (2026)
              </span>
              <h1 className="text-3xl font-serif font-bold text-neutral-900 mt-2">
                ZAPE — AI Personalisation Engine Console
              </h1>
              <p className="text-sm text-neutral-600 mt-1">
                4-Layer Clinical Decision Support: Ingestion → 6-Axis Scoring → Mizaj Moderation → Protocol Synthesis
              </p>
            </div>
            <div className="text-right">
              <span className="inline-block px-3 py-1 bg-amber-50 text-amber-800 text-xs font-medium border border-amber-200 rounded">
                SaMD Class IIa · Clinician-in-the-Loop Required
              </span>
            </div>
          </div>
        </div>

        {/* Grid Input + Output */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Controls */}
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
            <h2 className="text-lg font-serif font-bold text-[#1B4332] border-b pb-2">
              Patient Phenotypic Data
            </h2>

            <div>
              <label className="block text-xs font-semibold text-neutral-600 uppercase mb-1">
                Constitutional Mizaj
              </label>
              <select
                value={mizaj}
                onChange={(e) => setMizaj(e.target.value)}
                className="w-full border border-neutral-300 rounded-md p-2 text-sm bg-neutral-50"
              >
                <option value="Harr-Yabis">Harr-Yabis (Hot-Dry / Safrawi)</option>
                <option value="Harr-Ratab">Harr-Ratab (Hot-Wet / Damawi)</option>
                <option value="Bard-Ratab">Bard-Ratab (Cold-Wet / Balghami)</option>
                <option value="Bard-Yabis">Bard-Yabis (Cold-Dry / Sawdawi)</option>
                <option value="Mutadil">Mutadil (Balanced / Temperate)</option>
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-neutral-500">BMI</label>
                <input
                  type="number"
                  step="0.1"
                  value={bmi}
                  onChange={(e) => setBmi(parseFloat(e.target.value))}
                  className="w-full border rounded p-1.5 text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500">PSS-10 Stress</label>
                <input
                  type="number"
                  value={pss10}
                  onChange={(e) => setPss10(parseInt(e.target.value))}
                  className="w-full border rounded p-1.5 text-sm"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-neutral-500">Systolic BP</label>
                <input
                  type="number"
                  value={sbp}
                  onChange={(e) => setSbp(parseInt(e.target.value))}
                  className="w-full border rounded p-1.5 text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500">Diastolic BP</label>
                <input
                  type="number"
                  value={dbp}
                  onChange={(e) => setDbp(parseInt(e.target.value))}
                  className="w-full border rounded p-1.5 text-sm"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-neutral-500">HbA1c (%)</label>
                <input
                  type="number"
                  step="0.1"
                  value={hba1c}
                  onChange={(e) => setHba1c(parseFloat(e.target.value))}
                  className="w-full border rounded p-1.5 text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500">FBG (mg/dL)</label>
                <input
                  type="number"
                  value={fbg}
                  onChange={(e) => setFbg(parseFloat(e.target.value))}
                  className="w-full border rounded p-1.5 text-sm"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-neutral-500">Fast. Insulin (µIU/mL)</label>
                <input
                  type="number"
                  step="0.1"
                  value={fastingInsulin}
                  onChange={(e) => setFastingInsulin(parseFloat(e.target.value))}
                  className="w-full border rounded p-1.5 text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500">hs-CRP (mg/L)</label>
                <input
                  type="number"
                  step="0.1"
                  value={hsCrp}
                  onChange={(e) => setHsCrp(parseFloat(e.target.value))}
                  className="w-full border rounded p-1.5 text-sm"
                />
              </div>
            </div>

            <button
              onClick={handleEvaluate}
              disabled={loading}
              className="w-full bg-[#2D6A4F] hover:bg-[#1B4332] text-white font-medium py-2.5 rounded-lg transition-colors text-sm shadow"
            >
              {loading ? "Computing 4-Layer ZAPE Synthesis..." : "Run ZAPE Personalisation Synthesis"}
            </button>
          </div>

          {/* Results Display */}
          <div className="lg:col-span-2 space-y-6">
            {!decisionSupport ? (
              <div className="bg-white p-12 rounded-xl border border-dashed border-neutral-300 text-center text-neutral-500">
                <p className="text-base font-serif">Run synthesis to generate ZAPE multi-axis assessment and tiered protocols.</p>
              </div>
            ) : (
              <div className="space-y-6">
                {/* 6-Axis Overview */}
                <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm">
                  <h3 className="text-base font-serif font-bold text-neutral-900 border-b pb-2 mb-4">
                    Layer 2: Six-Axis Disease Model Activation
                  </h3>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                    {Object.entries(decisionSupport.axis_activations).map(([axis, data]: any) => (
                      <div
                        key={axis}
                        className={`p-3 rounded-lg border ${
                          data.severity === "Severe"
                            ? "bg-red-50 border-red-200 text-red-950"
                            : data.severity === "Moderate"
                            ? "bg-amber-50 border-amber-200 text-amber-950"
                            : "bg-emerald-50 border-emerald-200 text-emerald-950"
                        }`}
                      >
                        <div className="text-xs font-bold uppercase">{axis}</div>
                        <div className="text-xl font-bold mt-1">{data.score} / 100</div>
                        <div className="text-xs font-medium mt-0.5">{data.severity}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Layer 3: Constitutional Guidance */}
                <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm">
                  <h3 className="text-base font-serif font-bold text-neutral-900 border-b pb-2 mb-3">
                    Layer 3: Constitutional Mizaj Moderation ({decisionSupport.mizaj})
                  </h3>
                  <div className="text-sm space-y-2">
                    <p><strong className="text-neutral-700">Qualities:</strong> {decisionSupport.constitutional_modifiers.qualities}</p>
                    <p><strong className="text-neutral-700">Dietary Principle:</strong> {decisionSupport.constitutional_modifiers.dietary_orientation.principle}</p>
                    <p><strong className="text-neutral-700">Dalak Manual Style:</strong> {decisionSupport.constitutional_modifiers.regimental_orientation.dalak_style}</p>
                  </div>
                </div>

                {/* Layer 4: 4-Tier Recommendations */}
                <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
                  <h3 className="text-base font-serif font-bold text-neutral-900 border-b pb-2">
                    Layer 4: Actionable 4-Tier Clinical Interventions
                  </h3>

                  <div className="space-y-3 text-sm">
                    <div className="p-3 bg-neutral-50 rounded-lg border border-neutral-200">
                      <span className="font-bold text-[#2D6A4F] text-xs uppercase block">Tier 1 — Lifestyle Foundation</span>
                      <p className="mt-1 text-neutral-700">{decisionSupport.recommendations.tier_1_lifestyle.stress_management}</p>
                      <p className="text-neutral-600 text-xs mt-1">{decisionSupport.recommendations.tier_1_lifestyle.sleep_target}</p>
                    </div>

                    <div className="p-3 bg-neutral-50 rounded-lg border border-neutral-200">
                      <span className="font-bold text-[#2D6A4F] text-xs uppercase block">Tier 2 — Evidence-Based Botanicals</span>
                      <ul className="list-disc list-inside mt-1 text-neutral-700 space-y-1">
                        {decisionSupport.recommendations.tier_2_botanicals.map((b: any, idx: number) => (
                          <li key={idx}>
                            <strong>{b.botanical}</strong> ({b.dose}) — <span className="text-xs text-neutral-500">[{b.evidence_level}] {b.mechanism}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="p-3 bg-neutral-50 rounded-lg border border-neutral-200">
                      <span className="font-bold text-[#2D6A4F] text-xs uppercase block">Tier 3 — Pharmacotherapy Safety Flags</span>
                      <ul className="list-disc list-inside mt-1 text-neutral-700 space-y-1">
                        {decisionSupport.recommendations.tier_3_pharmacotherapy.indications_flagged.map((f: string, idx: number) => (
                          <li key={idx} className="text-neutral-800">{f}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="p-3 bg-neutral-50 rounded-lg border border-neutral-200">
                      <span className="font-bold text-[#2D6A4F] text-xs uppercase block">Tier 4 — Regimental Modalities</span>
                      <p className="mt-1 text-neutral-700"><strong>Dalak:</strong> {decisionSupport.recommendations.tier_4_regimental.dalak}</p>
                      <p className="text-neutral-700 mt-1"><strong>Hijama:</strong> {decisionSupport.recommendations.tier_4_regimental.hijama_evaluation.eligible ? "Eligible" : "Not Recommended"} — {decisionSupport.recommendations.tier_4_regimental.hijama_evaluation.protocol || decisionSupport.recommendations.tier_4_regimental.hijama_evaluation.reason}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
