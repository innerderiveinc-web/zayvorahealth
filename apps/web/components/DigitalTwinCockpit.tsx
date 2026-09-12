"use client";

import React, { useState, useEffect } from "react";
import {
  clinicalApi,
  type DigitalTwinState,
  type DigitalTwinSimulationResponse,
  type DigitalTwinTrajectoryResponse,
} from "@/lib/clinicalApi";

interface DigitalTwinCockpitProps {
  token: string;
  patientId: string;
  patientName: string;
}

export function DigitalTwinCockpit({ token, patientId, patientName }: DigitalTwinCockpitProps) {
  const [twin, setTwin] = useState<DigitalTwinState | null>(null);
  const [trajectory, setTrajectory] = useState<DigitalTwinTrajectoryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Simulation controls
  const [dominantHumor, setDominantHumor] = useState("Dam");
  const [simWeeks, setSimWeeks] = useState(8);
  const [simResult, setSimResult] = useState<DigitalTwinSimulationResponse | null>(null);
  const [isSimulating, setIsSimulating] = useState(false);

  // FHIR Export state
  const [fhirJson, setFhirJson] = useState<string | null>(null);
  const [isExportingFhir, setIsExportingFhir] = useState(false);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      setError(null);
      try {
        const [twinData, trajData] = await Promise.all([
          clinicalApi.getDigitalTwin(token, patientId),
          clinicalApi.getDigitalTwinTrajectory(token, patientId).catch(() => ({
            trajectory_available: false,
            clinical_trend: "Single Evaluation",
          })),
        ]);
        setTwin(twinData);
        setTrajectory(trajData);
      } catch (err: any) {
        setError(err.message || "Failed to load Clinical Digital Twin");
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [token, patientId]);

  const handleSimulate = async () => {
    setIsSimulating(true);
    try {
      const res = await clinicalApi.simulateDigitalTwinTrajectory(token, patientId, {
        dominant_humor: dominantHumor,
        weeks: simWeeks,
        treatment_modalities: ["Ilaj bil-Dawa", "Ilaj bil-Tadbeer", "Ilaj bil-Ghiza"],
      });
      setSimResult(res);
    } catch (err: any) {
      alert(`Simulation failed: ${err.message}`);
    } finally {
      setIsSimulating(false);
    }
  };

  const handleExportFhir = async () => {
    setIsExportingFhir(true);
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000"}/api/v1/interop/patients/${patientId}/fhir/op-consult`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (!res.ok) throw new Error("Failed to export ABDM FHIR bundle");
      const data = await res.json();
      setFhirJson(JSON.stringify(data, null, 2));
    } catch (err: any) {
      alert(`FHIR Export Error: ${err.message}`);
    } finally {
      setIsExportingFhir(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 text-center" style={{ color: "var(--muted)" }}>
        <div className="inline-block animate-spin w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full mb-3" />
        <p className="text-sm">Synthesizing Clinical Digital Twin & Organ Axes...</p>
      </div>
    );
  }

  if (error || !twin) {
    return (
      <div className="p-6 rounded-lg bg-red-950/30 border border-red-800/50 text-red-400">
        <p className="font-semibold text-sm">Error Loading Digital Twin</p>
        <p className="text-xs mt-1">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header & Vitality Score */}
      <div className="zv-panel p-5 flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
            <h2 className="text-lg font-bold text-slate-100">
              Clinical Digital Twin: <span className="text-emerald-400">{patientName}</span>
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Dynamic Computational Physiological State Vector across 12 Canonical Organ Axes & Humoral Trajectory
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-xs text-slate-400">Overall Vitality Index</div>
            <div className="text-2xl font-extrabold text-emerald-400">
              {(twin.overall_vitality_index * 100).toFixed(0)}%
            </div>
          </div>
          <button
            onClick={handleExportFhir}
            disabled={isExportingFhir}
            className="px-3 py-2 text-xs font-semibold rounded-md border border-cyan-500/40 text-cyan-300 bg-cyan-950/40 hover:bg-cyan-900/50 transition-colors"
          >
            {isExportingFhir ? "Exporting..." : "📋 ABDM FHIR R4 Bundle"}
          </button>
        </div>
      </div>

      {/* Top Grid: Mizaj Trajectory & Quwa Faculties */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Card 1: Mizaj Equilibrium & Drift */}
        <div className="zv-panel p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <h3 className="text-sm font-semibold text-slate-200">Humoral Mizaj State & Drift</h3>
            <span className="px-2 py-0.5 text-xs rounded bg-slate-800 text-slate-300 font-mono">
              {twin.mizaj_state.clinical_status}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="p-3 rounded bg-slate-900/60 border border-slate-800">
              <span className="text-xs text-slate-400">Primary Temperament</span>
              <p className="text-base font-bold text-amber-400 mt-0.5">
                {twin.mizaj_state.primary_temperament}
              </p>
            </div>
            <div className="p-3 rounded bg-slate-900/60 border border-slate-800">
              <span className="text-xs text-slate-400">Drift Magnitude</span>
              <p className="text-base font-bold text-slate-200 mt-0.5">
                {twin.mizaj_state.drift_magnitude} Δ
              </p>
            </div>
          </div>

          <div className="p-3 rounded bg-slate-900/40 border border-slate-800/80 text-xs text-slate-300">
            <span className="font-semibold text-emerald-400">Longitudinal Velocity: </span>
            {trajectory?.clinical_trend || "Single Evaluation"}
            {trajectory?.net_drift_delta !== undefined && (
              <span className="text-slate-400 ml-1">
                (Net Change: {trajectory.net_drift_delta > 0 ? "+" : ""}
                {trajectory.net_drift_delta})
              </span>
            )}
          </div>
        </div>

        {/* Card 2: Quwa (Vital Faculties) */}
        <div className="zv-panel p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <h3 className="text-sm font-semibold text-slate-200">Four Classical Faculties (Quwa)</h3>
            <span className="text-xs text-emerald-400 font-mono">
              Tabi'at Reserve: {(twin.quwa_faculties.tabiat_homeostatic_reserve * 100).toFixed(0)}%
            </span>
          </div>

          <div className="space-y-3">
            {[
              {
                name: "Quwwat-e-Tabi'iyyah (Nutritive / Hepatic)",
                val: twin.quwa_faculties.quwwat_tabi_iyyah,
                desc: "Governs digestion, assimilation, and blood manufacture",
              },
              {
                name: "Quwwat-e-Hayawaniyyah (Vital / Cardio-Pulmonary)",
                val: twin.quwa_faculties.quwwat_hayawaniyyah,
                desc: "Governs arterial pulsation, innate heat, and breath",
              },
              {
                name: "Quwwat-e-Nafsaniyyah (Psychic / Neuro-Cognitive)",
                val: twin.quwa_faculties.quwwat_nafsaniyyah,
                desc: "Governs sensation, voluntary motion, and cognition",
              },
            ].map((q) => (
              <div key={q.name} className="space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-300">{q.name}</span>
                  <span className="font-mono text-slate-400">{(q.val * 100).toFixed(0)}%</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${
                      q.val >= 0.8 ? "bg-emerald-500" : q.val >= 0.6 ? "bg-amber-500" : "bg-red-500"
                    }`}
                    style={{ width: `${q.val * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Organ Axis Integrity Matrix */}
      <div className="zv-panel p-5 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
          <h3 className="text-sm font-semibold text-slate-200">
            12 Canonical Organ Axis Homeostasis Matrix
          </h3>
          <span className="text-xs text-slate-400">Scores $\ge$ 80% indicate resilient homeostasis</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
          {Object.entries(twin.organ_axis_integrity).map(([axis, score]) => {
            const pct = (score * 100).toFixed(0);
            const isGood = score >= 0.8;
            const isMid = score >= 0.5 && score < 0.8;
            return (
              <div
                key={axis}
                className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex flex-col justify-between"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-300 capitalize">
                    {axis.replace("-", " ")}
                  </span>
                  <span
                    className={`text-xs font-bold font-mono ${
                      isGood ? "text-emerald-400" : isMid ? "text-amber-400" : "text-red-400"
                    }`}
                  >
                    {pct}%
                  </span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                  <div
                    className={`h-full rounded-full ${
                      isGood ? "bg-emerald-500" : isMid ? "bg-amber-500" : "bg-red-500"
                    }`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Interactive Simulation Panel */}
      <div className="zv-panel p-5 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
          <div>
            <h3 className="text-sm font-semibold text-slate-200">
              Treatment Trajectory Simulation Engine
            </h3>
            <p className="text-xs text-slate-400">
              Simulates multi-week physiological response, Nujz (concoction) schedule, and axis recovery
            </p>
          </div>
          <div className="flex items-center gap-2">
            <select
              value={dominantHumor}
              onChange={(e) => setDominantHumor(e.target.value)}
              className="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-700 rounded text-slate-200"
            >
              <option value="Dam">Dam (Sanguine - 4d Nujz)</option>
              <option value="Safra">Safra (Biliary - 8d Nujz)</option>
              <option value="Balgham">Balgham (Phlegmatic - 18d Nujz)</option>
              <option value="Sauda">Sauda (Melancholic - 35d Nujz)</option>
            </select>
            <select
              value={simWeeks}
              onChange={(e) => setSimWeeks(Number(e.target.value))}
              className="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-700 rounded text-slate-200"
            >
              <option value={4}>4 Weeks</option>
              <option value={8}>8 Weeks</option>
              <option value={12}>12 Weeks</option>
            </select>
            <button
              onClick={handleSimulate}
              disabled={isSimulating}
              className="px-3.5 py-1.5 text-xs font-semibold rounded bg-emerald-600 hover:bg-emerald-500 text-white transition-colors"
            >
              {isSimulating ? "Simulating..." : "Run Simulation"}
            </button>
          </div>
        </div>

        {simResult && (
          <div className="space-y-3 pt-2">
            <div className="p-3 rounded bg-emerald-950/30 border border-emerald-800/40 text-xs text-emerald-300">
              <span className="font-bold">Concoction Protocol: </span>
              {simResult.simulation_metadata.concoction_protocol.phase} (Estimated:{" "}
              {simResult.simulation_metadata.concoction_protocol.days} days)
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
              {simResult.projected_milestones.map((m) => (
                <div
                  key={m.week}
                  className="p-3 rounded bg-slate-900 border border-slate-800 space-y-1 text-xs"
                >
                  <div className="flex justify-between items-center text-slate-300 font-semibold">
                    <span>Week {m.week} Milestone</span>
                    <span className="text-emerald-400 font-mono">
                      {(m.projected_mean_organ_integrity * 100).toFixed(0)}%
                    </span>
                  </div>
                  <p className="text-slate-400 text-[11px]">{m.phase_description}</p>
                  <div className="text-[10px] mt-1 font-semibold">
                    {m.nujz_milestone_achieved ? (
                      <span className="text-emerald-400">✓ Nujz Concoction Achieved</span>
                    ) : (
                      <span className="text-amber-400">⏳ Concoction Pending</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* FHIR Bundle Modal Preview if clicked */}
      {fhirJson && (
        <div className="zv-panel p-5 space-y-3 border-cyan-800/60">
          <div className="flex justify-between items-center">
            <h4 className="text-xs font-bold text-cyan-400">
              ABDM HL7 FHIR R4 OPConsultRecord Document Bundle
            </h4>
            <button
              onClick={() => setFhirJson(null)}
              className="text-xs text-slate-400 hover:text-white"
            >
              ✕ Close Preview
            </button>
          </div>
          <pre className="p-3 rounded bg-slate-950 text-cyan-200 text-xs font-mono max-h-64 overflow-auto border border-slate-800">
            {fhirJson}
          </pre>
        </div>
      )}
    </div>
  );
}
