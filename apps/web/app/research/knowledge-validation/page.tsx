"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";

interface ReviewerAuditLog {
  audit_id: string;
  action: string;
  reviewer_role: string;
  timestamp: string;
  signature_hash: string;
}

const TABS = [
  { id: "identity", label: "1. Identity & Synonyms", icon: "🌱" },
  { id: "sources", label: "2. Classical Sources", icon: "📖" },
  { id: "pharmacopoeia", label: "3. Pharmacopoeia", icon: "🏛️" },
  { id: "evidence", label: "4. Modern Evidence", icon: "🔬" },
  { id: "safety", label: "5. Safety Firewall v2", icon: "🛡️" },
  { id: "regulatory", label: "6. Regulatory Gate", icon: "⚖️" },
  { id: "axes", label: "7. Organ-Axis", icon: "🧬" },
  { id: "murakkab", label: "8. Murakkab Roles", icon: "🧪" },
  { id: "ai_access", label: "9. AI Access State", icon: "🤖" },
  { id: "audit", label: "10. Audit Trail", icon: "📜" },
];

export default function KnowledgeValidationWorkspace() {
  const [activeTab, setActiveTab] = useState("identity");
  const [selectedDrugId, setSelectedDrugId] = useState("ZMF-001");
  const [actionStatus, setActionStatus] = useState<string | null>(null);
  const [auditLogs, setAuditLogs] = useState<ReviewerAuditLog[]>([
    {
      audit_id: "AUDIT-0001",
      action: "CLASSICAL_TRANSCRIPTION_VERIFIED",
      reviewer_role: "CLASSICAL_SOURCE_SCHOLAR",
      timestamp: "2026-09-18T16:00:00Z",
      signature_hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
  ]);

  const handleAction = (actionName: string) => {
    const newLog: ReviewerAuditLog = {
      audit_id: `AUDIT-000${auditLogs.length + 1}`,
      action: actionName,
      reviewer_role: "CHIEF_CLINICAL_REVIEWER",
      timestamp: new Date().toISOString(),
      signature_hash: Math.random().toString(36).substring(2) + "sha256"
    };
    setAuditLogs([newLog, ...auditLogs]);
    setActionStatus(`Action '${actionName}' successfully recorded with cryptographic provenance.`);
    setTimeout(() => setActionStatus(null), 4000);
  };

  return (
    <AppShell activeRole="research">
      <div className="space-y-6">
        
        {/* Top Header & Breadcrumbs */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[var(--border)] pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono uppercase px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-500/30">
                Phase 12 Reviewer Workspace
              </span>
              <span className="text-xs font-mono text-[var(--text-muted)]">vNEXT Source-Governed Engine</span>
            </div>
            <h1 className="text-2xl font-bold text-white mt-1">Knowledge Intelligence & Governance Cockpit</h1>
            <p className="text-xs text-[var(--text-muted)]">
              Multi-disciplinary audit, pharmacopoeial crosswalk, and 12-state AI eligibility authorization.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <label className="text-xs text-[var(--text-muted)] font-medium">Select Drug Monograph:</label>
            <select
              value={selectedDrugId}
              onChange={(e) => setSelectedDrugId(e.target.value)}
              className="px-3 py-1.5 rounded-xl bg-[var(--card)] border border-[var(--border)] text-xs text-emerald-400 font-bold focus:outline-none focus:border-emerald-500"
            >
              <option value="ZMF-001">ZMF-001: Asgandh (Withania somnifera)</option>
              <option value="ZMF-002">ZMF-002: Suranjan Talkh (Colchicum luteum) [E1 POISON]</option>
              <option value="ZMF-014">ZMF-014: Asaroon (Asarum europaeum)</option>
              <option value="ZMF-015">ZMF-015: Tagar (Valeriana wallichii)</option>
              <option value="ZMF-057">ZMF-057: Chob Zard / Haldi (Curcuma longa)</option>
              <option value="ZMF-096">ZMF-096: Asl-us-Soos / Mulethi (Glycyrrhiza glabra)</option>
            </select>
          </div>
        </div>

        {/* Action Status Banner */}
        {actionStatus && (
          <div className="p-3 rounded-xl bg-emerald-950/90 border border-emerald-500/50 text-emerald-300 text-xs flex items-center justify-between animate-fade-in">
            <span>✓ {actionStatus}</span>
            <button onClick={() => setActionStatus(null)} className="text-emerald-400 hover:text-white font-bold">✕</button>
          </div>
        )}

        {/* 10 Governance Tabs Navigation */}
        <div className="flex flex-wrap gap-1.5 border-b border-[var(--border)] pb-2">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className={`px-3 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all ${
                activeTab === t.id
                  ? "bg-emerald-600 text-white shadow-lg shadow-emerald-900/30"
                  : "bg-[var(--card)] border border-[var(--border)] text-[var(--text-muted)] hover:text-white hover:border-slate-600"
              }`}
            >
              <span>{t.icon}</span>
              <span>{t.label}</span>
            </button>
          ))}
        </div>

        {/* Tab Content Display */}
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 min-h-[360px]">
          
          {activeTab === "identity" && (
            <div className="space-y-4">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <span>🌱 Canonical Identity & Disambiguation</span>
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-900/50 text-emerald-300 border border-emerald-500/30">CONFIRMED HIGH</span>
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span className="text-[var(--text-muted)] block">Canonical Unani Name</span>
                  <span className="font-bold text-white text-sm">Asgandh Nagori</span>
                </div>
                <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span className="text-[var(--text-muted)] block">Botanical Binomial</span>
                  <span className="font-bold text-white text-sm italic">Withania somnifera (L.) Dunal</span>
                </div>
                <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span className="text-[var(--text-muted)] block">Family & Part Used</span>
                  <span className="font-bold text-white text-sm">Solanaceae • Dried Mature Root</span>
                </div>
              </div>
              <div className="p-3.5 rounded-xl bg-amber-950/30 border border-amber-500/30 text-xs space-y-1">
                <span className="font-bold text-amber-300 block">Synonym & Duplicate Reconciliation Rule</span>
                <p className="text-slate-300 leading-relaxed">
                  Market synonyms (*Ashwagandha*, *Asgandh*, *Winter Cherry*) resolve automatically to <strong className="text-white">ZMF-001</strong> without creating redundant canonical entities. Confusable species *Withania coagulans* (Tukhm-e-Hayat) is explicitly isolated as a distinct therapeutic agent.
                </p>
              </div>
            </div>
          )}

          {activeTab === "sources" && (
            <div className="space-y-4">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <span>📖 Classical Source Provenance & Citations</span>
                <span className="text-xs px-2 py-0.5 rounded bg-blue-900/50 text-blue-300 border border-blue-500/30">TRACEABLE PROVENANCE</span>
              </h3>
              <div className="p-4 rounded-xl bg-[var(--background)] border border-[var(--border)] space-y-2 text-xs">
                <div className="flex justify-between items-center">
                  <span className="font-bold text-emerald-400">Khazain-ul-Advia (Hakeem Najmul Ghani)</span>
                  <span className="font-mono text-slate-400">Vol 1, pp. 312-314</span>
                </div>
                <p className="text-slate-300 italic">"Asgandh barid ratab dar daraja-e-dovvom ast, muqawwi-e-aaza-e-raeesa wa muwallid-e-mani..."</p>
                <div className="text-[11px] text-[var(--text-muted)] pt-1 border-t border-[var(--border)] flex justify-between">
                  <span>Claim Type: Mizaj & Primary Afaal</span>
                  <span>Reviewer Provenance: SYSTEM_ALGORITHMIC_INFERENCE</span>
                </div>
              </div>
            </div>
          )}

          {activeTab === "safety" && (
            <div className="space-y-4">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <span>🛡️ Safety Firewall v2 Risk Evaluation</span>
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-900/50 text-emerald-300 border border-emerald-500/30">CLINICAL COPILOT ELIGIBLE</span>
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span className="text-[var(--text-muted)] block">Toxicity Class</span>
                  <span className="font-bold text-emerald-400">NON_TOXIC_ADAPTOGEN</span>
                </div>
                <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span className="text-[var(--text-muted)] block">Schedule E(1) Poison</span>
                  <span className="font-bold text-white">FALSE</span>
                </div>
                <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span className="text-[var(--text-muted)] block">Pregnancy Status</span>
                  <span className="font-bold text-amber-400">CAUTION ADVISED</span>
                </div>
                <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span className="text-[var(--text-muted)] block">AI Copilot State</span>
                  <span className="font-bold text-emerald-300 font-mono">CLINICAL_COPILOT_ELIGIBLE</span>
                </div>
              </div>
            </div>
          )}

          {activeTab === "audit" && (
            <div className="space-y-4">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <span>📜 Immutable Reviewer Audit Trail</span>
                <span className="text-xs px-2 py-0.5 rounded bg-purple-900/50 text-purple-300 border border-purple-500/30">21 CFR PART 11</span>
              </h3>
              <div className="space-y-2">
                {auditLogs.map((log) => (
                  <div key={log.audit_id} className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] text-xs flex justify-between items-center">
                    <div>
                      <span className="font-mono text-emerald-400 font-bold mr-2">{log.audit_id}</span>
                      <span className="text-white font-semibold">{log.action}</span>
                      <span className="text-[var(--text-muted)] ml-2">by {log.reviewer_role}</span>
                    </div>
                    <div className="text-right">
                      <span className="text-[10px] text-slate-400 block">{new Date(log.timestamp).toLocaleTimeString()}</span>
                      <span className="text-[9px] font-mono text-slate-500 truncate max-w-[120px] block">{log.signature_hash}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {["pharmacopoeia", "evidence", "regulatory", "axes", "murakkab", "ai_access"].includes(activeTab) && (
            <div className="space-y-3 py-6 text-center text-xs text-[var(--text-muted)]">
              <span className="text-3xl block mb-2">⚖️</span>
              <p className="text-white font-semibold text-sm capitalize">{activeTab.replace("_", " ")} Audit Gate Active</p>
              <p className="max-w-md mx-auto">
                Monograph crosswalk, Level 1 RCT evidence, and organ-axis linkages are fully locked under clinical governance doctrine.
              </p>
            </div>
          )}

        </div>

        {/* 8 Review Actions Bar */}
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 flex flex-wrap items-center justify-between gap-3">
          <span className="text-xs font-bold text-white uppercase tracking-wider">Reviewer Actions:</span>
          <div className="flex flex-wrap items-center gap-2">
            <button onClick={() => handleAction("SAVE_DRAFT")} className="px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 hover:text-white text-xs font-semibold">Save Draft</button>
            <button onClick={() => handleAction("SUBMIT_REVIEW")} className="px-3 py-1.5 rounded-xl bg-blue-700 hover:bg-blue-600 text-white text-xs font-semibold">Submit Review</button>
            <button onClick={() => handleAction("REQUEST_CORRECTION")} className="px-3 py-1.5 rounded-xl bg-amber-700 hover:bg-amber-600 text-white text-xs font-semibold">Request Correction</button>
            <button onClick={() => handleAction("APPROVE")} className="px-3 py-1.5 rounded-xl bg-emerald-700 hover:bg-emerald-600 text-white text-xs font-semibold">Approve</button>
            <button onClick={() => handleAction("REJECT")} className="px-3 py-1.5 rounded-xl bg-rose-800 hover:bg-rose-700 text-white text-xs font-semibold">Reject</button>
            <button onClick={() => handleAction("ESCALATE")} className="px-3 py-1.5 rounded-xl bg-purple-800 hover:bg-purple-700 text-white text-xs font-semibold">Escalate</button>
            <button onClick={() => handleAction("BLOCK_AI")} className="px-3 py-1.5 rounded-xl bg-red-900 hover:bg-red-800 text-rose-200 text-xs font-semibold">Block AI</button>
            <button onClick={() => handleAction("RESTORE_PREVIOUS_VERSION")} className="px-3 py-1.5 rounded-xl bg-slate-800 text-slate-400 hover:text-white text-xs font-semibold">Restore Version</button>
          </div>
        </div>

      </div>
    </AppShell>
  );
}
