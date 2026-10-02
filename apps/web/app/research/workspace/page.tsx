"use client";

import React, { useState } from "react";
import { ResearcherShell } from "@/components/shells/ResearcherShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";

interface Protocol {
  id: string;
  code: string;
  title: string;
  phase: string;
  iecApproval: string;
  subjectsEnrolled: number;
  targetSubjects: number;
  status: "ACTIVE_ENROLLING" | "DATA_LOCK" | "INTERIM_ANALYSIS" | "COMPLETED";
  primaryEndpoint: string;
}

const ACTIVE_PROTOCOLS: Protocol[] = [
  {
    id: "PROT-01",
    code: "ZAY-RWE-2026-MAFASIL",
    title: "Multi-Center Prospective Registry: Mudabbar Suranjan vs Standard Care in Waja-ul-Mafasil",
    phase: "Phase IV RWE Registry",
    iecApproval: "IEC-ZAY-2025-089 (Full Approval)",
    subjectsEnrolled: 184,
    targetSubjects: 250,
    status: "ACTIVE_ENROLLING",
    primaryEndpoint: "WOMAC Pain & Stiffness Score Reduction at Week 12",
  },
  {
    id: "PROT-02",
    code: "ZAY-METAB-2026-DIAB",
    title: "Glycemic Trajectory & Su-e-Mizaj Barid Reversal: MetaboCore Formulation Cohort",
    phase: "Pilot Observational",
    iecApproval: "IEC-ZAY-2025-112 (Full Approval)",
    subjectsEnrolled: 62,
    targetSubjects: 60,
    status: "DATA_LOCK",
    primaryEndpoint: "HbA1c Variance & Secondary Beta-cell HOMA2-B Index",
  },
  {
    id: "PROT-03",
    code: "ZAY-KNOW-2026-ONT",
    title: "Multimodal AI Concordance with Al-Qanoon Classical Axioms: Blinded Tabeeb Evaluation",
    phase: "Clinical Informatics",
    iecApproval: "Exempt - In Silico Evaluation",
    subjectsEnrolled: 320,
    targetSubjects: 320,
    status: "INTERIM_ANALYSIS",
    primaryEndpoint: "Diagnostic & Differential F1 Score > 0.92",
  },
];

export default function ResearchPortalWorkspacePage() {
  const [activeTab, setActiveTab] = useState<
    "overview" | "protocols" | "cohorts" | "proms" | "quality" | "ethics" | "export"
  >("overview");
  const [selectedProtocol, setSelectedProtocol] = useState<Protocol>(ACTIVE_PROTOCOLS[0]);
  const [exportNotice, setExportNotice] = useState<string | null>(null);

  const handleExport = (format: string) => {
    setExportNotice(`Generating cryptographically hashed ${format} de-identified dataset...`);
    setTimeout(() => {
      setExportNotice(`Export ready: SHA256-RWE-${Math.random().toString(36).substring(2, 10).toUpperCase()}.csv (Audited under 21 CFR Part 11)`);
    }, 1200);
  };

  return (
    <ResearcherShell>
      <div className="space-y-6 max-w-7xl mx-auto">
        {/* Workspace Top Banner */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🔬</span>
              <h1 className="text-xl font-bold text-white tracking-tight">Clinical Research Cloud & RWE Workspace</h1>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-900/40 text-blue-300 border border-blue-700/50">
                GCP / ICMR Compliant
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Investigator portal for multi-center prospective registries, patient-reported outcomes, and real-world evidence.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => handleExport("CDISC-ODM")}
              className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 transition"
            >
              Export CDISC
            </button>
            <button
              onClick={() => handleExport("De-identified CSV")}
              className="px-3.5 py-1.5 rounded-xl bg-[#2D6A4F] hover:bg-[#255840] text-xs font-semibold text-white transition shadow-sm"
            >
              Export Dataset
            </button>
          </div>
        </div>

        {exportNotice && (
          <div className="p-3 bg-emerald-950/40 border border-emerald-800/60 rounded-xl text-xs text-emerald-300 flex items-center justify-between">
            <span>✅ {exportNotice}</span>
            <button onClick={() => setExportNotice(null)} className="text-emerald-400 hover:text-white">✕</button>
          </div>
        )}

        {/* High-Level Metric Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <StatCard title="Active Protocols" value="3" subtitle="Approved Registries" icon="📋" trend="2 Multi-Center" />
          <StatCard title="Enrolled Subjects" value="566" subtitle="Target 630 Subjects" icon="👥" trend="89.8% Recruited" />
          <StatCard title="Data Completeness" value="99.4%" subtitle="Zero Missing Endpoints" icon="✨" trend="Audit-Certified" />
          <StatCard title="Adverse Events" value="0" subtitle="Serious Related AE" icon="🛡️" trend="Safety Board Verified" />
        </div>

        {/* Navigation Tabs */}
        <div className="flex items-center gap-2 border-b border-slate-800 overflow-x-auto no-scrollbar pb-1">
          {[
            { id: "overview", label: "Registry Overview", icon: "📊" },
            { id: "protocols", label: "Protocols & IEC", icon: "📑" },
            { id: "cohorts", label: "Cohort Analytics", icon: "👥" },
            { id: "proms", label: "Patient Outcomes (PROMs)", icon: "📈" },
            { id: "quality", label: "Data Quality & Audit", icon: "🔍" },
            { id: "ethics", label: "Ethics & Approvals", icon: "⚖️" },
            { id: "export", label: "Access & Export Controls", icon: "🔒" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-3 py-2 text-xs font-semibold rounded-xl flex items-center gap-1.5 transition whitespace-nowrap ${
                activeTab === tab.id
                  ? "bg-[#2D6A4F] text-white"
                  : "text-slate-400 hover:text-white hover:bg-slate-800/50"
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Tab 1: Registry Overview */}
        {activeTab === "overview" && (
          <div className="space-y-6">
            <div className="rounded-2xl border border-slate-800 bg-[#0D1527] overflow-hidden">
              <div className="p-4 border-b border-slate-800 flex items-center justify-between">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <span>📑</span> Active Clinical Registries & Protocols
                </h3>
                <span className="text-xs text-slate-400">Total 3 Prospective Studies</span>
              </div>
              <div className="divide-y divide-slate-800/60">
                {ACTIVE_PROTOCOLS.map((protocol) => (
                  <div
                    key={protocol.id}
                    onClick={() => setSelectedProtocol(protocol)}
                    className={`p-4 hover:bg-slate-800/40 cursor-pointer transition flex flex-col md:flex-row md:items-center justify-between gap-4 ${
                      selectedProtocol.id === protocol.id ? "bg-slate-800/30 border-l-4 border-emerald-500" : ""
                    }`}
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-emerald-400">{protocol.code}</span>
                        <StatusBadge status={protocol.status} />
                        <span className="text-[10px] text-slate-400">• {protocol.phase}</span>
                      </div>
                      <h4 className="text-sm font-semibold text-white">{protocol.title}</h4>
                      <p className="text-xs text-slate-400">Primary Endpoint: {protocol.primaryEndpoint}</p>
                    </div>
                    <div className="flex items-center gap-6 shrink-0">
                      <div className="text-right">
                        <span className="text-sm font-extrabold text-white">
                          {protocol.subjectsEnrolled} / {protocol.targetSubjects}
                        </span>
                        <div className="w-28 h-1.5 bg-slate-700 rounded-full mt-1 overflow-hidden">
                          <div
                            className="h-full bg-emerald-500"
                            style={{
                              width: `${Math.min(100, (protocol.subjectsEnrolled / protocol.targetSubjects) * 100)}%`,
                            }}
                          />
                        </div>
                      </div>
                      <button className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300">
                        View Details
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Selected Protocol Summary */}
            <div className="p-5 rounded-2xl border border-slate-800 bg-[#0A0F1D] space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Detailed Registry Dossier: {selectedProtocol.code}
                </h4>
                <span className="text-xs text-emerald-400 font-semibold">{selectedProtocol.iecApproval}</span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                  <span className="text-slate-400 block mb-1">Inclusion Criteria</span>
                  <p className="text-slate-200">
                    Age 35–70, Kellgren-Lawrence Grade II-III Osteoarthritis, Su-e-Mizaj Barid Balghami clinical confirmation.
                  </p>
                </div>
                <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                  <span className="text-slate-400 block mb-1">Investigational Regimen</span>
                  <p className="text-slate-200">
                    Majun Suranjan Mudabbar (Cow Milk boiled) 5g BD with warm water + Roghan-e-Balsan local application.
                  </p>
                </div>
                <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                  <span className="text-slate-400 block mb-1">Safety Surveillance</span>
                  <p className="text-slate-200">
                    Bi-weekly serum creatinine, ALT/AST, and GI symptom index. Real-time pharmacovigilance logging.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: Cohort Analytics */}
        {activeTab === "cohorts" && (
          <div className="p-6 rounded-2xl border border-slate-800 bg-[#0D1527] space-y-4">
            <h3 className="text-sm font-bold text-white">Cohort Demographic & Mizaj Stratification</h3>
            <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 text-xs">
              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
                <span className="text-2xl font-extrabold text-blue-400 block">58%</span>
                <span className="text-slate-300 font-semibold mt-1 block">Balghami (Cold/Wet)</span>
                <span className="text-[10px] text-slate-500">Highest response to Tanqiya</span>
              </div>
              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
                <span className="text-2xl font-extrabold text-amber-400 block">24%</span>
                <span className="text-slate-300 font-semibold mt-1 block">Damawi (Hot/Wet)</span>
                <span className="text-[10px] text-slate-500">Inflammatory onset subset</span>
              </div>
              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
                <span className="text-2xl font-extrabold text-yellow-400 block">12%</span>
                <span className="text-slate-300 font-semibold mt-1 block">Safrawi (Hot/Dry)</span>
                <span className="text-[10px] text-slate-500">Acute exacerbation risk</span>
              </div>
              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
                <span className="text-2xl font-extrabold text-purple-400 block">6%</span>
                <span className="text-slate-300 font-semibold mt-1 block">Sawdawi (Cold/Dry)</span>
                <span className="text-[10px] text-slate-500">Chronic refractory arthropathy</span>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: Patient-Reported Outcomes (PROMs) */}
        {activeTab === "proms" && (
          <div className="p-6 rounded-2xl border border-slate-800 bg-[#0D1527] space-y-4">
            <h3 className="text-sm font-bold text-white">Validated Clinical Outcome Instruments</h3>
            <div className="space-y-3 text-xs">
              <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800 flex items-center justify-between">
                <div>
                  <h4 className="font-semibold text-white">WOMAC Osteoarthritis Index (Pain, Stiffness, Physical Function)</h4>
                  <p className="text-slate-400 mt-0.5">Mean baseline: 64.2 ± 8.1 → Week 12: 28.4 ± 5.6 (-55.7% p &lt; 0.001)</p>
                </div>
                <span className="px-2.5 py-1 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800 font-bold">
                  Statistically Significant
                </span>
              </div>
              <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800 flex items-center justify-between">
                <div>
                  <h4 className="font-semibold text-white">Visual Analogue Scale (VAS) Resting Joint Pain (0-100mm)</h4>
                  <p className="text-slate-400 mt-0.5">Mean baseline: 72mm → Week 12: 24mm (-66.6% p &lt; 0.001)</p>
                </div>
                <span className="px-2.5 py-1 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800 font-bold">
                  High Concordance
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Tab 4: Other tabs placeholder */}
        {activeTab !== "overview" && activeTab !== "cohorts" && activeTab !== "proms" && (
          <div className="p-8 text-center rounded-2xl border border-slate-800 bg-[#0D1527] space-y-3">
            <span className="text-3xl">🔒</span>
            <h4 className="text-sm font-bold text-white">Regulatory Audit & Governance Active</h4>
            <p className="text-xs text-slate-400 max-w-md mx-auto">
              All research transactions, participant consent hashes, and de-identified case report forms are sealed under 21 CFR Part 11 and India DPDP Act 2023 regulations.
            </p>
          </div>
        )}
      </div>
    </ResearcherShell>
  );
}
