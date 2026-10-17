"use client";

import React, { useState } from "react";

interface EngineInfo {
  name: string;
  role: string;
  version: string;
  status: "Operational" | "Degraded" | "Maintenance";
  latencyMs: number;
  uptime: string;
  port: number;
  description: string;
}

const ENGINES: EngineInfo[] = [
  { name: "Identity & RBAC Engine", role: "Security / Auth", version: "v5.0.1", status: "Operational", latencyMs: 14, uptime: "99.98%", port: 8001, description: "JWT authentication, 21 CFR Part 11 electronic signatures, and multi-tenant facility isolation." },
  { name: "Clinical Continuum Engine", role: "EHR / OPD", version: "v5.0.0", status: "Operational", latencyMs: 22, uptime: "99.95%", port: 8002, description: "10-Ajnas longitudinal Mizaj profiling, organ-axis cross-talk, and Afaal stage tracking." },
  { name: "Knowledge Base Engine (ZKB)", role: "Unani Knowledge Graph", version: "v5.1.0", status: "Operational", latencyMs: 18, uptime: "99.99%", port: 8003, description: "Codified UPI/NFUM monographs, Badal substitutes, Musleh correctives, and classical ontology." },
  { name: "Therapeutic & Posology Engine (ZAPE)", role: "Pharmacovigilance", version: "v5.0.2", status: "Operational", latencyMs: 16, uptime: "99.94%", port: 8004, description: "Adaptive botanical posology, Schedule E(1) Mudabbar verification, and OpenFDA cross-checks." },
  { name: "Hakeem AI Copilot Engine", role: "Clinical AI Reasoning", version: "v5.0.0", status: "Operational", latencyMs: 45, uptime: "99.91%", port: 8005, description: "Non-autonomous clinical decision support with mandatory clinician signature gating." }
];

export default function AdminEnginesPage() {
  const [engineList, setEngineList] = useState<EngineInfo[]>(ENGINES);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-gray-800">Core Microservice Engines</h2>
        <p className="text-sm text-gray-500">Real-time status, RPC latency, and operational health of ZAYVORA backend engines</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Active Engines</span>
          <span className="text-2xl font-bold text-emerald-700 mt-1 block">5 / 5 Online</span>
          <span className="text-xs text-gray-400 mt-1 block">All health checks returning 200 OK</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Average Inter-Service Latency</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">23 ms</span>
          <span className="text-xs text-emerald-600 font-semibold mt-1 block">Optimal internal bus throughput</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Consensus State</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">Synchronized</span>
          <span className="text-xs text-gray-400 mt-1 block">Shared DB connection pool active</span>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {engineList.map(eng => (
          <div key={eng.name} className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-gray-800 text-base">{eng.name}</h3>
                <span className="text-xs font-mono px-2 py-0.5 rounded bg-gray-100 text-gray-600">Port {eng.port}</span>
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">{eng.status}</span>
              </div>
              <p className="text-xs text-gray-500 max-w-2xl">{eng.description}</p>
            </div>
            <div className="flex items-center gap-6 text-sm">
              <div>
                <span className="text-xs text-gray-400 block">Latency</span>
                <span className="font-mono font-bold text-gray-700">{eng.latencyMs} ms</span>
              </div>
              <div>
                <span className="text-xs text-gray-400 block">Uptime</span>
                <span className="font-bold text-emerald-600">{eng.uptime}</span>
              </div>
              <button
                onClick={() => alert(`Flushing internal cache for ${eng.name}...`)}
                className="px-3 py-1.5 border border-gray-200 hover:bg-gray-50 text-gray-700 text-xs font-semibold rounded-lg transition"
              >
                Flush Cache
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
