"use client";

import React, { useState } from "react";

export default function RegimenTherapiesPage() {
  const [mizaj, setMizaj] = useState("Bard-Ratab");
  const [condition, setCondition] = useState("Type 2 Diabetes Mellitus");
  const [hasCvd, setHasCvd] = useState(false);
  const [isPregnant, setIsPregnant] = useState(false);
  const [neuropathy, setNeuropathy] = useState(false);

  // Hijama safety inputs
  const [plt, setPlt] = useState(250000);
  const [hb, setHb] = useState(13.5);
  const [isAnticoag, setIsAnticoag] = useState(false);

  const [hammamRes, setHammamRes] = useState<any>(null);
  const [contrastRes, setContrastRes] = useState<any>(null);
  const [hijamaRes, setHijamaRes] = useState<any>(null);

  const handleGenerateRegimen = async () => {
    try {
      const [hRes, cRes, hijRes] = await Promise.all([
        fetch("/api/v1/therapeutic/regimen/hammam", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ mizaj, condition, has_cvd_history: hasCvd, is_pregnant: isPregnant, neuropathy_present: neuropathy })
        }).then(r => r.json()),
        fetch("/api/v1/therapeutic/regimen/contrast-shower", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ mizaj, is_raynauds: false })
        }).then(r => r.json()),
        fetch("/api/v1/therapeutic/regimen/hijama-safety", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ platelet_count: plt, hemoglobin_g_dl: hb, is_anticoagulated: isAnticoag, is_pregnant: isPregnant, active_infection_at_site: false })
        }).then(r => r.json())
      ]);

      if (hRes.ok) setHammamRes(hRes.hammam_protocol);
      if (cRes.ok) setContrastRes(cRes.contrast_shower);
      if (hijRes.ok) setHijamaRes(hijRes.safety_check);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="min-h-screen bg-[#FAFAF7] p-8 text-neutral-900 font-sans">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="border-b border-neutral-200 pb-4">
          <span className="text-xs font-bold uppercase tracking-widest text-[#2D6A4F] bg-emerald-50 px-2.5 py-1 rounded">
            ZAYVORA Health OS™ · Regimental Therapies (Ilaj bil Tadbeer)
          </span>
          <h1 className="text-3xl font-serif font-bold text-neutral-900 mt-2">
            Hammam, Hydrotherapy & Cupping Safety Protocol
          </h1>
          <p className="text-sm text-neutral-600 mt-1">
            Reference: Chapters 9, 10, 11 & 12 · Thermoregulation, HSP70 Induction, and Vascular Compliance
          </p>
        </div>

        {/* Setup Parameters */}
        <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-xs font-semibold text-neutral-600 uppercase mb-1">Mizaj</label>
            <select
              value={mizaj}
              onChange={(e) => setMizaj(e.target.value)}
              className="w-full border rounded p-2 text-sm bg-neutral-50"
            >
              <option value="Harr-Yabis">Harr-Yabis (Hot-Dry)</option>
              <option value="Harr-Ratab">Harr-Ratab (Hot-Wet)</option>
              <option value="Bard-Ratab">Bard-Ratab (Cold-Wet)</option>
              <option value="Bard-Yabis">Bard-Yabis (Cold-Dry)</option>
              <option value="Mutadil">Mutadil (Balanced)</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-semibold text-neutral-600 uppercase mb-1">Condition</label>
            <input
              type="text"
              value={condition}
              onChange={(e) => setCondition(e.target.value)}
              className="w-full border rounded p-2 text-sm"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-neutral-600 uppercase mb-1">Platelets (/mcL)</label>
            <input
              type="number"
              value={plt}
              onChange={(e) => setPlt(parseInt(e.target.value))}
              className="w-full border rounded p-2 text-sm"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-neutral-600 uppercase mb-1">Hemoglobin (g/dL)</label>
            <input
              type="number"
              step="0.1"
              value={hb}
              onChange={(e) => setHb(parseFloat(e.target.value))}
              className="w-full border rounded p-2 text-sm"
            />
          </div>

          <div className="md:col-span-4 flex flex-wrap gap-6 pt-2 border-t text-sm">
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={hasCvd} onChange={(e) => setHasCvd(e.target.checked)} />
              <span>Prior Cardiovascular Disease History</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={isPregnant} onChange={(e) => setIsPregnant(e.target.checked)} />
              <span>Pregnant</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={neuropathy} onChange={(e) => setNeuropathy(e.target.checked)} />
              <span>Severe Peripheral Neuropathy</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={isAnticoag} onChange={(e) => setIsAnticoag(e.target.checked)} />
              <span>Active Anticoagulant Therapy</span>
            </label>
          </div>

          <div className="md:col-span-4 pt-2">
            <button
              onClick={handleGenerateRegimen}
              className="bg-[#2D6A4F] hover:bg-[#1B4332] text-white font-medium py-2 px-6 rounded-lg text-sm shadow transition-colors"
            >
              Verify Safety & Prescribe Regimen
            </button>
          </div>
        </div>

        {/* Results Panels */}
        {hammamRes && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Hammam Sequence */}
            <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-3">
              <h2 className="text-base font-serif font-bold text-[#1B4332] border-b pb-2">
                Hammam 3-Phase Thermoregulation Protocol
              </h2>
              {hammamRes.eligible ? (
                <div className="space-y-3 text-sm">
                  <p className="text-neutral-600 text-xs">{hammamRes.therapeutic_objective}</p>
                  <div className="space-y-2">
                    {hammamRes.sequence.map((seq: any) => (
                      <div key={seq.phase} className="p-2.5 bg-neutral-50 rounded border border-neutral-200">
                        <div className="flex justify-between font-bold text-xs text-neutral-800">
                          <span>{seq.chamber}</span>
                          <span>{seq.target_temp_c}°C · {seq.duration_min} min</span>
                        </div>
                        <p className="text-xs text-neutral-600 mt-0.5">{seq.action}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="p-4 bg-red-50 text-red-900 border border-red-200 rounded text-sm">
                  {hammamRes.reason}
                </div>
              )}
            </div>

            {/* Hijama Safety Gate */}
            <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-3">
              <h2 className="text-base font-serif font-bold text-[#1B4332] border-b pb-2">
                Hijama (Wet Cupping) Safety Verification Gate
              </h2>
              {hijamaRes && (
                <div className="text-sm space-y-3">
                  <div className={`p-3 rounded-lg border font-bold text-xs ${hijamaRes.cleared ? "bg-emerald-50 border-emerald-200 text-emerald-950" : "bg-red-50 border-red-200 text-red-950"}`}>
                    {hijamaRes.decision}
                  </div>
                  {hijamaRes.cleared ? (
                    <div className="space-y-2 text-xs text-neutral-700">
                      <p><strong>Max Safe Extraction Volume:</strong> {hijamaRes.max_extraction_volume_ml} mL</p>
                      <p><strong>Depth:</strong> {hijamaRes.protocol_specifications.incision_depth}</p>
                      <p><strong>Equipment:</strong> {hijamaRes.protocol_specifications.equipment}</p>
                    </div>
                  ) : (
                    <ul className="list-disc list-inside text-xs text-red-700 space-y-1">
                      {hijamaRes.reasons.map((r: string, idx: number) => (
                        <li key={idx}>{r}</li>
                      ))}
                    </ul>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
