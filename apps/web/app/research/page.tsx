"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";

interface ClinicalStudy {
  id: string;
  protocolNumber: string;
  title: string;
  leadInvestigator: string;
  institute: string;
  targetEnrollment: number;
  currentEnrollment: number;
  phase: string;
  status: "ACTIVE_ENROLLMENT" | "ANALYSIS" | "COMPLETED";
}

const STUDIES: ClinicalStudy[] = [
  {
    id: "ST-01",
    protocolNumber: "ZCT-2026-001",
    title: "Therapeutic Concordance of Majun Suranjan with Mudabbar Detoxification in Knee Osteoarthritis",
    leadInvestigator: "Dr. K. Saxena",
    institute: "National Institute of Integrative Medicine",
    targetEnrollment: 120,
    currentEnrollment: 94,
    phase: "Phase IV RWE",
    status: "ACTIVE_ENROLLMENT",
  },
  {
    id: "ST-02",
    protocolNumber: "ZCT-2026-002",
    title: "Multi-Center Prospective Cohort on Safoof-e-Ziabetes in New-Onset Type 2 Diabetes",
    leadInvestigator: "Hakim Dr. Tariq Mansoor",
    institute: "Central Clinical Facility",
    targetEnrollment: 80,
    currentEnrollment: 80,
    phase: "Observational Cohort",
    status: "ANALYSIS",
  },
];

export default function ResearchWorkspacePage() {
  const [activeTab, setActiveTab] = useState<"trials" | "cohorts" | "adr" | "protocols">("trials");
  const [studies] = useState<ClinicalStudy[]>(STUDIES);

  // WHO-UMC ADR Form
  const [adrPatient, setAdrPatient] = useState("PAT-774901 (Hamza Farooqi)");
  const [adrDrug, setAdrDrug] = useState("Majun Suranjan");
  const [adrReaction, setAdrReaction] = useState("Mild transient nausea after first dose");
  const [adrSeverity, setAdrSeverity] = useState("MILD");
  const [adrSuccess, setAdrSuccess] = useState<string | null>(null);

  const handleReportAdr = (e: React.FormEvent) => {
    e.preventDefault();
    setAdrSuccess("Adverse Drug Reaction successfully filed under WHO-UMC / ICH E2B guidelines (Ref: ADR-2026-0912-01)");
    setTimeout(() => setAdrSuccess(null), 5000);
  };

  return (
    <AppShell activeRole="research">
      <div className="space-y-5 max-w-7xl mx-auto">
        
        {/* Workspace Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight">Clinical Research Cloud & Pharmacovigilance</h1>
            <p className="text-xs text-[#94A3B8]">
              Dr. K. Saxena • Principal Clinical Investigator • ICH E2B & RWE Compliant
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="zv-badge-purple px-3 py-1 rounded-lg text-xs font-semibold">
              🔬 GCP / ICMR Ethical Standards
            </span>
          </div>
        </div>

        {/* Research Executive Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <StatCard label="Active Trials" value={studies.length} subtext="2 Institutional studies" variant="purple" icon="🔬" />
          <StatCard label="Enrolled Subjects" value="174" subtext="Across all cohorts" variant="teal" icon="👥" />
          <StatCard label="ADRs Reported" value="1" subtext="WHO-UMC Causality Verified" variant="amber" icon="⚠️" />
          <StatCard label="Data Completeness" value="99.4%" subtext="PROMs & Biomarkers" variant="emerald" icon="📊" />
        </div>

        {/* Tab Navigation */}
        <div className="border-b border-[#334155] flex gap-2">
          {[
            { id: "trials", label: "Active Clinical Trials", icon: "🔬" },
            { id: "cohorts", label: "RWE Patient Cohorts", icon: "👥" },
            { id: "adr", label: "Adverse Events (WHO-UMC)", icon: "⚠️" },
            { id: "protocols", label: "Study Protocols", icon: "📑" },
          ].map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as typeof activeTab)}
                className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold border-b-2 transition ${
                  isActive
                    ? "border-[#8B5CF6] text-[#C084FC] bg-[#8B5CF6]/10 rounded-t-lg"
                    : "border-transparent text-[#94A3B8] hover:text-white"
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* TAB 1: ACTIVE CLINICAL TRIALS */}
        {activeTab === "trials" && (
          <div className="zv-card overflow-hidden">
            <div className="p-4 border-b border-[#334155] bg-[#0F172A] flex justify-between items-center">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider">Clinical Trial Protocols & Enrollment</h3>
              <span className="text-[11px] text-[#94A3B8]">CTRI Registered</span>
            </div>
            <div className="divide-y divide-[#334155]">
              {studies.map((st) => (
                <div key={st.id} className="p-4 hover:bg-[#1E293B]/50 transition space-y-2 text-xs">
                  <div className="flex justify-between items-start">
                    <div>
                      <span className="font-mono text-[#C084FC] font-bold block">{st.protocolNumber}</span>
                      <h4 className="text-sm font-bold text-white">{st.title}</h4>
                      <p className="text-[11px] text-[#94A3B8] mt-0.5">
                        PI: {st.leadInvestigator} • {st.institute} • {st.phase}
                      </p>
                    </div>
                    <StatusBadge
                      status={st.status.replace("_", " ")}
                      variant={st.status === "ACTIVE_ENROLLMENT" ? "verified" : "research"}
                    />
                  </div>
                  <div className="flex items-center justify-between pt-2 text-[#94A3B8] text-[11px]">
                    <span>Enrollment: <strong className="text-white">{st.currentEnrollment} / {st.targetEnrollment}</strong> subjects ({Math.round((st.currentEnrollment/st.targetEnrollment)*100)}%)</span>
                    <button className="zv-btn-secondary text-xs py-1 px-3">View Cohort Dataset</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 2: RWE COHORTS */}
        {activeTab === "cohorts" && (
          <div className="zv-card p-5 space-y-4 text-xs">
            <h3 className="text-sm font-bold text-white">Real-World Evidence (RWE) Observational Cohorts</h3>
            <div className="p-4 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-2">
              <span className="font-bold text-[#2DD4BF]">Cohort A: Waja-ul-Mafasil Barid Balghami Longitudinal Study</span>
              <p className="text-[#94A3B8]">
                94 subjects receiving standardized Majun Suranjan (Mudabbar) + Raughan-e-Balsan with bi-weekly WOMAC osteoarthritis score tracking.
              </p>
              <div className="flex gap-4 pt-2 text-[11px] text-[#94A3B8]">
                <span>Mean Pain Reduction: <strong className="text-[#34D399]">-68%</strong></span>
                <span>Adverse Event Rate: <strong className="text-white">1.06%</strong></span>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: WHO-UMC ADR FORM */}
        {activeTab === "adr" && (
          <div className="zv-card p-5 max-w-2xl mx-auto space-y-4 text-xs">
            <div>
              <h3 className="text-sm font-bold text-white">WHO-UMC & ICH E2B Adverse Drug Reaction (ADR) Intake</h3>
              <p className="text-xs text-[#94A3B8] mt-0.5">Submit suspected adverse botanical reaction directly to pharmacovigilance registry</p>
            </div>

            {adrSuccess && (
              <div className="p-3 bg-[#10B981]/15 border border-[#10B981]/30 rounded-lg text-xs text-[#34D399] font-semibold">
                ✓ {adrSuccess}
              </div>
            )}

            <form onSubmit={handleReportAdr} className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[#94A3B8] block mb-1">Patient Subject *</label>
                  <input
                    type="text"
                    required
                    value={adrPatient}
                    onChange={(e) => setAdrPatient(e.target.value)}
                    className="zv-input"
                  />
                </div>
                <div>
                  <label className="text-[#94A3B8] block mb-1">Suspected Medicine *</label>
                  <input
                    type="text"
                    required
                    value={adrDrug}
                    onChange={(e) => setAdrDrug(e.target.value)}
                    className="zv-input"
                  />
                </div>
              </div>

              <div>
                <label className="text-[#94A3B8] block mb-1">Observed Adverse Event / Symptoms *</label>
                <textarea
                  rows={3}
                  required
                  value={adrReaction}
                  onChange={(e) => setAdrReaction(e.target.value)}
                  className="zv-input"
                />
              </div>

              <div>
                <label className="text-[#94A3B8] block mb-1">Reaction Severity</label>
                <select
                  value={adrSeverity}
                  onChange={(e) => setAdrSeverity(e.target.value)}
                  className="zv-input bg-[#0F172A]"
                >
                  <option value="MILD">Mild (No intervention required)</option>
                  <option value="MODERATE">Moderate (Dose adjustment required)</option>
                  <option value="SEVERE">Severe (Hospitalization / Discontinuation)</option>
                </select>
              </div>

              <button
                type="submit"
                className="zv-btn-primary w-full py-2 bg-[#8B5CF6] hover:bg-[#7C3AED] font-bold"
              >
                Submit ICH E2B Pharmacovigilance Report
              </button>
            </form>
          </div>
        )}

        {/* TAB 4: PROTOCOLS */}
        {activeTab === "protocols" && (
          <div className="zv-card p-5 space-y-3 text-xs">
            <h3 className="text-sm font-bold text-white">Registered Study Protocols</h3>
            <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] flex justify-between items-center">
              <div>
                <span className="font-bold text-white">ZCT-2026-001-Protocol-V2.pdf</span>
                <span className="text-[10px] text-[#64748B] block">Approved by Institutional Ethics Committee (IEC)</span>
              </div>
              <button className="zv-btn-secondary py-1 px-3">Download Protocol</button>
            </div>
          </div>
        )}

      </div>
    </AppShell>
  );
}
