"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";

interface TenantFacility {
  id: string;
  name: string;
  code: string;
  type: "HOSPITAL" | "CLINIC" | "RESEARCH_INSTITUTE";
  activePractitioners: number;
  status: "ACTIVE" | "MAINTENANCE";
}

const FACILITIES: TenantFacility[] = [
  {
    id: "FAC-HQ-01",
    name: "National Institute of Integrative Medicine (Central Facility)",
    code: "NIIM-DELHI",
    type: "HOSPITAL",
    activePractitioners: 18,
    status: "ACTIVE",
  },
  {
    id: "FAC-HQ-02",
    name: "Jamia Hamdard Faculty of Unani Medicine Clinical Center",
    code: "JH-UNANI-01",
    type: "HOSPITAL",
    activePractitioners: 12,
    status: "ACTIVE",
  },
];

interface MerkleBlock {
  blockNumber: number;
  timestamp: string;
  leafHash: string;
  merkleRoot: string;
  eventType: string;
  signer: string;
  status: "ANCHORED";
}

const MERKLE_LOGS: MerkleBlock[] = [
  {
    blockNumber: 44102,
    timestamp: "2026-09-12T17:30:00Z",
    leafHash: "731f5cf53472e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495",
    merkleRoot: "a8b3d6e99b9bc060fb3591c27a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b",
    eventType: "PRESCRIPTION_LOCKED",
    signer: "Hakim Dr. Tariq Mansoor (CCIM-BUMS-2004-9841)",
    status: "ANCHORED",
  },
  {
    blockNumber: 44101,
    timestamp: "2026-09-12T17:15:22Z",
    leafHash: "8f4b29c91a03e147b2c9d01248a0f9b3e217c49b01538a7c29b0134f59c14820",
    merkleRoot: "c060fb3591c2a8b3d6e99b9b7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b",
    eventType: "CLINICAL_SOAP_ANCHORED",
    signer: "Hakim Dr. Tariq Mansoor (CCIM-BUMS-2004-9841)",
    status: "ANCHORED",
  },
  {
    blockNumber: 44100,
    timestamp: "2026-09-12T16:50:11Z",
    leafHash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    merkleRoot: "d9e8f7a6b5c4d3e2f1a0b9c8d7c060fb3591c2a8b3d6e99b9b7a8b9c0d1e2f3a",
    eventType: "MUDABBAR_CERTIFICATE_VERIFIED",
    signer: "Pharmacist Zainab Ali (PB-PHARM-2015-8812)",
    status: "ANCHORED",
  },
];

export default function AdminWorkspacePage() {
  const [activeTab, setActiveTab] = useState<"facilities" | "merkle" | "rbac" | "firewall">("facilities");
  const [facilities] = useState<TenantFacility[]>(FACILITIES);
  const [merkleLogs] = useState<MerkleBlock[]>(MERKLE_LOGS);

  return (
    <AppShell activeRole="admin">
      <div className="space-y-5 max-w-7xl mx-auto">
        
        {/* Workspace Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight">Enterprise IT Administration & Governance</h1>
            <p className="text-xs text-[#94A3B8]">
              Platform Administrator Console • 21 CFR Part 11 Merkle Ledger • Multi-Tenant Partitioning
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="zv-badge-emerald px-3 py-1 rounded-lg text-xs font-semibold">
              ✓ Merkle Root Validated
            </span>
          </div>
        </div>

        {/* Admin Executive Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <StatCard label="Active Facilities" value="2" subtext="Hospitals & Institutes" variant="teal" icon="🏥" />
          <StatCard label="Anchored Blocks" value="44,102" subtext="21 CFR Part 11 leaves" variant="emerald" icon="🔒" />
          <StatCard label="Active Clinicians" value="30" subtext="Verified registrations" variant="blue" icon="🩺" />
          <StatCard label="Firewall Rule State" value="Enforced" subtext="Schedule E(1) block active" variant="teal" icon="🛡️" />
        </div>

        {/* Tab Navigation */}
        <div className="border-b border-[#334155] flex gap-2">
          {[
            { id: "facilities", label: "Facilities & Tenants", icon: "🏥" },
            { id: "merkle", label: "21 CFR Part 11 Merkle Ledger", icon: "🔒" },
            { id: "rbac", label: "RBAC Permissions Matrix", icon: "🛡️" },
            { id: "firewall", label: "Safety Firewall Rules", icon: "⚙️" },
          ].map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as typeof activeTab)}
                className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold border-b-2 transition ${
                  isActive
                    ? "border-[#0D9488] text-[#2DD4BF] bg-[#0D9488]/10 rounded-t-lg"
                    : "border-transparent text-[#94A3B8] hover:text-white"
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* TAB 1: FACILITIES */}
        {activeTab === "facilities" && (
          <div className="zv-card overflow-hidden">
            <div className="p-4 border-b border-[#334155] bg-[#0F172A] flex justify-between items-center">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider">Registered Healthcare Facilities</h3>
              <button className="zv-btn-primary text-xs py-1 px-3 bg-[#0D9488]">+ Add Facility</button>
            </div>
            <div className="divide-y divide-[#334155]">
              {facilities.map((fac) => (
                <div key={fac.id} className="p-4 hover:bg-[#1E293B]/50 transition flex justify-between items-center text-xs">
                  <div>
                    <span className="font-bold text-white block text-sm">{fac.name}</span>
                    <span className="text-[11px] text-[#94A3B8] font-mono">Code: {fac.code} • Type: {fac.type}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-[#2DD4BF] font-semibold">{fac.activePractitioners} Practitioners</span>
                    <StatusBadge status={fac.status} variant="verified" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 2: MERKLE LEDGER */}
        {activeTab === "merkle" && (
          <div className="zv-card overflow-hidden">
            <div className="p-4 border-b border-[#334155] bg-[#0F172A] flex justify-between items-center">
              <div>
                <h3 className="text-xs font-bold text-white uppercase tracking-wider">21 CFR Part 11 Merkle Signature Explorer</h3>
                <p className="text-[11px] text-[#94A3B8]">Immutable cryptographic root securing all clinical notes and prescription seals</p>
              </div>
              <span className="zv-badge-teal px-2 py-0.5 rounded text-[10px] font-mono">
                Root: a8b3d6...5a6b
              </span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-[#0A0F1D] text-[#94A3B8] border-b border-[#334155]">
                  <tr>
                    <th className="p-3">Block #</th>
                    <th className="p-3">Timestamp</th>
                    <th className="p-3">Event Type</th>
                    <th className="p-3">Leaf Hash (SHA-256)</th>
                    <th className="p-3">Authorized Signer</th>
                    <th className="p-3 text-right">Integrity</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#334155]">
                  {merkleLogs.map((log) => (
                    <tr key={log.blockNumber} className="hover:bg-[#1E293B]/50 transition">
                      <td className="p-3 font-mono text-[#2DD4BF] font-bold">#{log.blockNumber}</td>
                      <td className="p-3 text-[#94A3B8] font-mono">{log.timestamp}</td>
                      <td className="p-3 font-semibold text-white">{log.eventType}</td>
                      <td className="p-3 font-mono text-[10px] text-[#94A3B8] max-w-[200px] truncate">{log.leafHash}</td>
                      <td className="p-3 text-white text-[11px]">{log.signer}</td>
                      <td className="p-3 text-right">
                        <StatusBadge status="Anchored" variant="verified" />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* TAB 3: RBAC MATRIX */}
        {activeTab === "rbac" && (
          <div className="zv-card p-5 space-y-3 text-xs">
            <h3 className="text-sm font-bold text-white">Granular Role-Based Access Control (RBAC)</h3>
            <p className="text-[#94A3B8]">
              Enforces the principle of least privilege across all 6 roles. Clinicians retain non-delegable prescribing rights; patients are strictly isolated.
            </p>
            <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-1">
              <span className="font-bold text-[#2DD4BF]">Full policy documented in:</span>
              <p className="font-mono text-[#94A3B8]">/docs/V5_ROLE_PERMISSIONS.md</p>
            </div>
          </div>
        )}

        {/* TAB 4: SAFETY FIREWALL */}
        {activeTab === "firewall" && (
          <div className="zv-card p-5 space-y-4 text-xs">
            <h3 className="text-sm font-bold text-white">Therapeutic Safety Firewall Rules</h3>
            <div className="p-4 bg-[#0A0F1D] rounded-lg border border-[#10B981]/40 space-y-2">
              <span className="font-bold text-[#34D399]">RULE-E1-001: Schedule E(1) Mudabbar Detoxification Gate</span>
              <p className="text-[#94A3B8]">
                Statutory block on unpurified toxic botanicals (*Suranjan*, *Kuchla*, *Aconite*). Any prescription containing these botanicals without an attached cryptographic Mudabbar certificate hash is unconditionally held.
              </p>
            </div>
            <div className="p-4 bg-[#0A0F1D] rounded-lg border border-[#0D9488]/40 space-y-2">
              <span className="font-bold text-[#2DD4BF]">RULE-AI-002: Non-Delegable Prescribing Barrier</span>
              <p className="text-[#94A3B8]">
                Artificial Intelligence models (Hakeem Sahab) cannot issue approved or signed prescriptions. `safe_to_lock = False` is enforced by default until manually reviewed and sealed by a verified human clinician.
              </p>
            </div>
          </div>
        )}

      </div>
    </AppShell>
  );
}
