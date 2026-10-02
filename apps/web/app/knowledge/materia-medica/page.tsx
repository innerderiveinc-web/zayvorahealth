"use client";

import React, { useState, useEffect } from "react";
import { PlatformHeader } from "@/components/PlatformHeader";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

interface Monograph {
  key: string;
  name: string;
  botanical_name?: string;
  family?: string;
  part_used?: string;
  mizaj_primary: string;
  mizaj: {
    heat: number;
    cold: number;
    dryness: number;
    moisture: number;
  };
  afaal: string[];
  modern_pharmacodynamics: string;
  why_essential: string;
  products_used_in: string[];
  requires_musleh?: boolean;
  musleh?: string;
  requires_tadbir?: boolean;
  tadbir_rules?: string;
  form?: string;
  clinical_benefits?: string[];
}

export default function MateriaMedicaPage() {
  const [monographs, setMonographs] = useState<Monograph[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedQuality, setSelectedQuality] = useState<string>("ALL");
  const [selectedDarja, setSelectedDarja] = useState<string>("ALL");
  const [selectedDrug, setSelectedDrug] = useState<Monograph | null>(null);

  // Safety checker simulator
  const [simulatorFormula, setSimulatorFormula] = useState<string>("AQARQARHA, ASGANDH, HALDI, PIPERINE");
  const [auditResult, setAuditResult] = useState<any>(null);
  const [auditing, setAuditing] = useState(false);

  useEffect(() => {
    fetchMonographs();
  }, []);

  async function fetchMonographs() {
    try {
      setLoading(true);
      const res = await fetch(`${API}/api/v1/knowledge/materia-medica/all`);
      if (res.ok) {
        const data = await res.json();
        setMonographs(data.monographs || []);
      }
    } catch (err) {
      console.error("Failed to load materia medica:", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleAuditFormula() {
    try {
      setAuditing(true);
      const items = simulatorFormula
        .split(",")
        .map((s) => ({ key: s.trim().toUpperCase().replace(/\s+/g, "_"), weight_g: 1.0 }))
        .filter((i) => i.key.length > 0);

      const res = await fetch(`${API}/api/v1/therapeutic/formula/audit-safety`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredients: items }),
      });
      if (res.ok) {
        const data = await res.json();
        setAuditResult(data.audit);
      }
    } catch (err) {
      console.error("Audit failed:", err);
    } finally {
      setAuditing(false);
    }
  }

  const filteredMonographs = monographs.filter((m) => {
    const q = searchQuery.toLowerCase();
    const matchesSearch =
      !searchQuery ||
      m.name.toLowerCase().includes(q) ||
      (m.botanical_name && m.botanical_name.toLowerCase().includes(q)) ||
      m.afaal.some((a) => a.toLowerCase().includes(q)) ||
      m.why_essential.toLowerCase().includes(q);

    let matchesQuality = true;
    if (selectedQuality === "HEAT") matchesQuality = (m.mizaj?.heat || 0) > 0;
    if (selectedQuality === "COLD") matchesQuality = (m.mizaj?.cold || 0) > 0;
    if (selectedQuality === "DRY") matchesQuality = (m.mizaj?.dryness || 0) > 0;
    if (selectedQuality === "MOIST") matchesQuality = (m.mizaj?.moisture || 0) > 0;

    let matchesDarja = true;
    if (selectedDarja !== "ALL") {
      const d = parseInt(selectedDarja, 10);
      matchesDarja =
        m.mizaj?.heat === d ||
        m.mizaj?.cold === d ||
        m.mizaj?.dryness === d ||
        m.mizaj?.moisture === d;
    }

    return matchesSearch && matchesQuality && matchesDarja;
  });

  return (
    <div className="min-h-screen bg-[#FAFAF7] text-[#1A1A1A]">
      <PlatformHeader />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb & Header */}
        <div className="mb-6">
          <div className="flex items-center space-x-2 text-xs text-gray-500 uppercase tracking-wider mb-2">
            <span>Clinical Knowledge</span>
            <span>&gt;</span>
            <span className="text-[#2D6A4F] font-semibold">ZAYVORA Pharmacopoeia</span>
          </div>
          <h1 className="text-3xl font-bold text-[#1B4332] font-serif">
            ZAYVORA Pharmacopoeia: Classical Single Drugs & Modern Bioactives
          </h1>
          <p className="text-sm text-gray-600 mt-1 max-w-4xl">
            Author: Dr. Irfan Ashraf, BUMS. Complete botanical, mineral (*Mufradat*), and nutraceutical reference with classical *Mizaj* thermal gradations (1° to 4°), classical *Afaal*, molecular pharmacodynamics, mandatory *Musleh* correctives, and *Tadbir* purification benchmarks.
          </p>
        </div>

        {/* Top Control Bar & Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white border border-[#2D6A4F]/20 rounded-xl p-4 shadow-sm">
            <span className="text-xs font-semibold text-gray-500 uppercase">Total Cataloged Drugs</span>
            <div className="text-2xl font-bold text-[#2D6A4F] mt-1">{monographs.length} Agents</div>
            <span className="text-xs text-gray-400">Herbal, Mineral, Bioactive</span>
          </div>
          <div className="bg-white border border-amber-200 rounded-xl p-4 shadow-sm">
            <span className="text-xs font-semibold text-amber-700 uppercase">Potent 3° & 4° Agents</span>
            <div className="text-2xl font-bold text-amber-800 mt-1">
              {monographs.filter((m) => (m.mizaj?.heat >= 3 || m.mizaj?.cold >= 3)).length} Agents
            </div>
            <span className="text-xs text-amber-600">Requires Musleh counter-balance</span>
          </div>
          <div className="bg-white border border-blue-200 rounded-xl p-4 shadow-sm">
            <span className="text-xs font-semibold text-blue-700 uppercase">Mineral / Tadbir Bound</span>
            <div className="text-2xl font-bold text-blue-800 mt-1">
              {monographs.filter((m) => m.requires_tadbir).length} Formulations
            </div>
            <span className="text-xs text-blue-600">Strict Shuddhi & heavy-metal gates</span>
          </div>
          <div className="bg-white border border-purple-200 rounded-xl p-4 shadow-sm">
            <span className="text-xs font-semibold text-purple-700 uppercase">Modern Bioactives</span>
            <div className="text-2xl font-bold text-purple-800 mt-1">
              {monographs.filter((m) => !m.botanical_name || m.botanical_name.includes("Bioactive")).length} Actives
            </div>
            <span className="text-xs text-purple-600">Mitochondrial & NO Cascades</span>
          </div>
        </div>

        {/* Filter & Search Toolbar */}
        <div className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm mb-6 flex flex-wrap items-center gap-4">
          <div className="flex-1 min-w-[240px]">
            <input
              type="text"
              placeholder="Search classical name, botanical name, afaal (e.g. Muqawwi, Curcumin, Amla)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2D6A4F]"
            />
          </div>

          <div className="flex items-center space-x-2">
            <span className="text-xs font-semibold text-gray-500 uppercase">Quality:</span>
            {["ALL", "HEAT", "COLD", "DRY", "MOIST"].map((qual) => (
              <button
                key={qual}
                onClick={() => setSelectedQuality(qual)}
                className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                  selectedQuality === qual
                    ? "bg-[#2D6A4F] text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                {qual === "HEAT" ? "Har (Hot)" : qual === "COLD" ? "Barid (Cold)" : qual === "DRY" ? "Yabis (Dry)" : qual === "MOIST" ? "Ratab (Moist)" : "All"}
              </button>
            ))}
          </div>

          <div className="flex items-center space-x-2">
            <span className="text-xs font-semibold text-gray-500 uppercase">Darja (Degree):</span>
            {["ALL", "1", "2", "3", "4"].map((d) => (
              <button
                key={d}
                onClick={() => setSelectedDarja(d)}
                className={`px-2.5 py-1.5 text-xs font-medium rounded-md transition-colors ${
                  selectedDarja === d
                    ? "bg-[#1B4332] text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                {d === "ALL" ? "All" : `${d}°`}
              </button>
            ))}
          </div>
        </div>

        {/* Main Content Layout: Grid + Monograph Drawer + Simulator */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left 2 Cols: Cards */}
          <div className="lg:col-span-2 space-y-4">
            {loading ? (
              <div className="bg-white border rounded-xl p-12 text-center text-gray-500">
                Loading ZAYVORA Pharmacopoeia monographs...
              </div>
            ) : filteredMonographs.length === 0 ? (
              <div className="bg-white border rounded-xl p-12 text-center text-gray-500">
                No single drugs match the current filters.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filteredMonographs.map((item) => {
                  const isHighDegree = (item.mizaj?.heat >= 3 || item.mizaj?.cold >= 3);
                  return (
                    <div
                      key={item.key}
                      onClick={() => setSelectedDrug(item)}
                      className={`bg-white border rounded-xl p-4 cursor-pointer transition-all hover:shadow-md ${
                        selectedDrug?.key === item.key
                          ? "border-[#2D6A4F] ring-2 ring-[#2D6A4F]/20"
                          : "border-gray-200 hover:border-gray-300"
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="font-bold text-[#1B4332] text-base">{item.name}</h3>
                          <p className="text-xs italic text-gray-500">{item.botanical_name || item.family || "Modern Active"}</p>
                        </div>
                        <span
                          className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${
                            isHighDegree
                              ? "bg-red-100 text-red-800 border border-red-200"
                              : "bg-emerald-100 text-[#2D6A4F]"
                          }`}
                        >
                          {item.mizaj_primary}
                        </span>
                      </div>

                      <div className="mt-3 flex flex-wrap gap-1">
                        {item.afaal?.slice(0, 3).map((af, idx) => (
                          <span
                            key={idx}
                            className="bg-gray-100 text-gray-700 text-[10px] px-2 py-0.5 rounded"
                          >
                            {af}
                          </span>
                        ))}
                      </div>

                      <p className="mt-2 text-xs text-gray-600 line-clamp-2">
                        {item.why_essential}
                      </p>

                      <div className="mt-3 pt-2 border-t border-gray-100 flex items-center justify-between text-[11px] text-gray-500">
                        <span>Used in: {item.products_used_in?.length || 0} Products</span>
                        {item.requires_musleh && (
                          <span className="text-amber-600 font-semibold text-[10px]">⚠️ Musleh Required</span>
                        )}
                        {item.requires_tadbir && (
                          <span className="text-blue-600 font-semibold text-[10px]">⚖️ Tadbir Compliant</span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Right Col: Drug Detail Drawer or Safety Simulator */}
          <div className="space-y-6">
            {/* Selected Drug Details */}
            {selectedDrug ? (
              <div className="bg-white border border-[#2D6A4F]/30 rounded-xl p-5 shadow-sm sticky top-6">
                <div className="flex items-start justify-between border-b pb-3">
                  <div>
                    <h2 className="text-xl font-bold text-[#1B4332] font-serif">{selectedDrug.name}</h2>
                    <p className="text-xs italic text-gray-500">{selectedDrug.botanical_name}</p>
                    <p className="text-[11px] text-gray-400">Family: {selectedDrug.family || "N/A"} | Part: {selectedDrug.part_used || "Standardized Form"}</p>
                  </div>
                  <button
                    onClick={() => setSelectedDrug(null)}
                    className="text-xs text-gray-400 hover:text-gray-600"
                  >
                    ✕ Close
                  </button>
                </div>

                {/* Mizaj Matrix */}
                <div className="mt-4 bg-[#FAFAF7] border border-gray-200 rounded-lg p-3">
                  <span className="text-xs font-bold text-gray-600 uppercase tracking-wider block mb-2">
                    Mizaj (Temperamental Degrees)
                  </span>
                  <div className="grid grid-cols-4 gap-2 text-center text-xs">
                    <div className="bg-red-50 p-2 rounded border border-red-100">
                      <span className="text-red-700 block font-semibold">Heat (Harr)</span>
                      <span className="text-sm font-bold text-red-900">{selectedDrug.mizaj?.heat || 0}°</span>
                    </div>
                    <div className="bg-blue-50 p-2 rounded border border-blue-100">
                      <span className="text-blue-700 block font-semibold">Cold (Barid)</span>
                      <span className="text-sm font-bold text-blue-900">{selectedDrug.mizaj?.cold || 0}°</span>
                    </div>
                    <div className="bg-amber-50 p-2 rounded border border-amber-100">
                      <span className="text-amber-700 block font-semibold">Dry (Yabis)</span>
                      <span className="text-sm font-bold text-amber-900">{selectedDrug.mizaj?.dryness || 0}°</span>
                    </div>
                    <div className="bg-teal-50 p-2 rounded border border-teal-100">
                      <span className="text-teal-700 block font-semibold">Moist (Ratab)</span>
                      <span className="text-sm font-bold text-teal-900">{selectedDrug.mizaj?.moisture || 0}°</span>
                    </div>
                  </div>
                </div>

                {/* Classical Afaal */}
                <div className="mt-4">
                  <span className="text-xs font-bold text-gray-600 uppercase tracking-wider block mb-1">
                    Classical Afaal (Therapeutic Actions)
                  </span>
                  <div className="flex flex-wrap gap-1">
                    {selectedDrug.afaal?.map((af, idx) => (
                      <span key={idx} className="bg-emerald-50 text-[#2D6A4F] text-xs px-2 py-0.5 rounded border border-emerald-100">
                        {af}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Modern Biochemistry */}
                <div className="mt-4">
                  <span className="text-xs font-bold text-gray-600 uppercase tracking-wider block mb-1">
                    Modern Pharmacodynamics & Biochemistry
                  </span>
                  <p className="text-xs text-gray-700 bg-gray-50 p-2 rounded border border-gray-200">
                    {selectedDrug.modern_pharmacodynamics}
                  </p>
                </div>

                {/* Musleh / Corrective */}
                {selectedDrug.musleh && (
                  <div className="mt-4 bg-amber-50 border border-amber-200 rounded-lg p-3">
                    <span className="text-xs font-bold text-amber-800 uppercase block mb-1">
                      Mandatory Musleh (Corrective Agent)
                    </span>
                    <p className="text-xs text-amber-900">{selectedDrug.musleh}</p>
                  </div>
                )}

                {/* Tadbir Protocol */}
                {selectedDrug.tadbir_rules && (
                  <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-3">
                    <span className="text-xs font-bold text-blue-800 uppercase block mb-1">
                      Tadbir (Purification / Shuddhi Benchmark)
                    </span>
                    <p className="text-xs text-blue-900">{selectedDrug.tadbir_rules}</p>
                  </div>
                )}

                {/* Products Used In */}
                <div className="mt-4 pt-3 border-t">
                  <span className="text-xs font-bold text-gray-600 uppercase tracking-wider block mb-2">
                    ZAYVORA Formulations & Products
                  </span>
                  <div className="flex flex-wrap gap-1">
                    {selectedDrug.products_used_in?.map((p, idx) => (
                      <span key={idx} className="bg-gray-100 text-gray-800 text-[11px] px-2 py-0.5 rounded font-mono">
                        {p}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
                <h3 className="font-bold text-[#1B4332] text-sm uppercase tracking-wider mb-2">
                  Select a Drug for Clinical Monograph
                </h3>
                <p className="text-xs text-gray-500">
                  Click any of the {monographs.length} monographs on the left to view complete Unani *Mizaj* gradations, *Afaal*, receptor dynamics, and compounding rules.
                </p>
              </div>
            )}

            {/* Formula Safety Checker Simulator */}
            <div className="bg-white border border-[#2D6A4F]/20 rounded-xl p-5 shadow-sm">
              <h3 className="font-bold text-[#1B4332] text-sm uppercase tracking-wider mb-2 flex items-center justify-between">
                <span>Formula Thermal & Safety Auditor</span>
                <span className="text-[10px] bg-emerald-100 text-[#2D6A4F] px-2 py-0.5 rounded font-semibold">Live Engine</span>
              </h3>
              <p className="text-xs text-gray-600 mb-3">
                Test any polypharmacy compound for thermal balance, mandatory Musleh pairing, and Shuddhi verification:
              </p>

              <div className="space-y-3">
                <div>
                  <label className="text-[11px] font-semibold text-gray-500 uppercase block mb-1">
                    Formula Ingredients (Comma Separated Keys)
                  </label>
                  <input
                    type="text"
                    value={simulatorFormula}
                    onChange={(e) => setSimulatorFormula(e.target.value)}
                    className="w-full px-3 py-2 text-xs border border-gray-300 rounded font-mono focus:outline-none focus:ring-2 focus:ring-[#2D6A4F]"
                  />
                  <span className="text-[10px] text-gray-400">
                    Try entering: AQARQARHA (missing Tabasheer will trigger safety violation!)
                  </span>
                </div>

                <button
                  onClick={handleAuditFormula}
                  disabled={auditing}
                  className="w-full bg-[#2D6A4F] hover:bg-[#1B4332] text-white text-xs font-semibold py-2 px-4 rounded transition-colors"
                >
                  {auditing ? "Auditing Formula..." : "Audit Safety & Thermal Index"}
                </button>

                {auditResult && (
                  <div className="mt-4 pt-3 border-t space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-bold text-gray-600">Decision:</span>
                      <span
                        className={`font-bold px-2 py-0.5 rounded text-[11px] ${
                          auditResult.formula_cleared
                            ? "bg-green-100 text-green-800 border border-green-200"
                            : "bg-red-100 text-red-800 border border-red-200"
                        }`}
                      >
                        {auditResult.decision}
                      </span>
                    </div>

                    {auditResult.thermal_audit && (
                      <div className="bg-[#FAFAF7] p-2 rounded text-xs border">
                        <div className="text-[11px] text-gray-500">Thermal Balance:</div>
                        <div className="font-bold text-gray-800">{auditResult.thermal_audit.classified_formula_mizaj}</div>
                        <div className="text-[10px] text-gray-500">
                          Heat Index: {auditResult.thermal_audit.net_thermal_index} | Moisture Index: {auditResult.thermal_audit.net_moisture_index}
                        </div>
                      </div>
                    )}

                    {auditResult.violations?.length > 0 && (
                      <div className="bg-red-50 border border-red-200 p-2 rounded text-xs text-red-800 space-y-1">
                        <span className="font-bold block">Safety Violations:</span>
                        {auditResult.violations.map((v: string, i: number) => (
                          <div key={i} className="text-[11px]">⚠️ {v}</div>
                        ))}
                      </div>
                    )}

                    {auditResult.synergies_detected?.length > 0 && (
                      <div className="bg-emerald-50 border border-emerald-200 p-2 rounded text-xs text-emerald-800 space-y-1">
                        <span className="font-bold block">Detected Synergies:</span>
                        {auditResult.synergies_detected.map((s: string, i: number) => (
                          <div key={i} className="text-[11px]">✨ {s}</div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
