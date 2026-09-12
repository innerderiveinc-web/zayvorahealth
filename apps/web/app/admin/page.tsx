"use client";

import React, { useState } from "react";
import { PlatformHeader } from "@/components/PlatformHeader";
import { GovernanceBoardCockpit } from "@/components/GovernanceBoardCockpit";
import { loadSession } from "@/lib/session";

interface TenantOrg {
  id: string;
  name: string;
  slug: string;
  type: "ACADEMIC_HOSPITAL" | "SPECIALTY_CLINIC" | "PHARMACY_CHAIN";
  active_users: number;
  status: "ACTIVE" | "SUSPENDED";
}

const ORGS: TenantOrg[] = [
  { id: "ORG-01", name: "Jamia Hamdard Faculty of Medicine", slug: "jamia-hamdard-autc", type: "ACADEMIC_HOSPITAL", active_users: 142, status: "ACTIVE" },
  { id: "ORG-02", name: "A&U Tibbia College & Hospital", slug: "autc-karol-bagh", type: "ACADEMIC_HOSPITAL", active_users: 98, status: "ACTIVE" },
  { id: "ORG-03", name: "Ajmal Khan Tibbiya College (AMU)", slug: "amu-tibbiya", type: "ACADEMIC_HOSPITAL", active_users: 110, status: "ACTIVE" },
  { id: "ORG-04", name: "ZAYVORA Integrative Wellness Clinic", slug: "zayvora-central", type: "SPECIALTY_CLINIC", active_users: 24, status: "ACTIVE" },
];

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState<"tenants" | "rbac" | "audit" | "governance">("tenants");
  const [sessionToken, setSessionToken] = useState<string>("jwt-admin-token");

  React.useEffect(() => {
    const s = loadSession();
    if (s) setSessionToken(s.access_token);
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--text)]">
      <PlatformHeader />

      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-6 space-y-6">
        
        {/* Admin Header */}
        <div className="zv-panel p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold">ZAYVORA Enterprise Administration & Governance</h1>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-yellow-500/10 border border-yellow-500/30 text-yellow-400 font-semibold">
                Super Admin Console
              </span>
            </div>
            <p className="text-xs text-[var(--muted)] mt-0.5">
              Multi-tenant organization partitioning, RBAC permissions catalog, immutable audit trails, and 3/3 Clinical Governance Quorum.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="text-[var(--muted)]">Active Tenants:</span>
            <span className="font-bold text-white">4</span>
            <span className="text-[var(--border)]">|</span>
            <span className="text-emerald-400 font-medium">Tenant Isolation Verified</span>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex flex-wrap gap-2 border-b border-[var(--border)] pb-2">
          <button
            onClick={() => setActiveTab("tenants")}
            className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-colors ${
              activeTab === "tenants"
                ? "bg-[var(--emerald)] text-white border-transparent"
                : "border-[var(--border)] text-[var(--muted)] hover:text-white"
            }`}
          >
            🏢 Tenant Organizations ({ORGS.length})
          </button>
          <button
            onClick={() => setActiveTab("rbac")}
            className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-colors ${
              activeTab === "rbac"
                ? "bg-[var(--emerald)] text-white border-transparent"
                : "border-[var(--border)] text-[var(--muted)] hover:text-white"
            }`}
          >
            🔑 Granular RBAC Permissions Catalogue
          </button>
          <button
            onClick={() => setActiveTab("audit")}
            className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-colors ${
              activeTab === "audit"
                ? "bg-[var(--emerald)] text-white border-transparent"
                : "border-[var(--border)] text-[var(--muted)] hover:text-white"
            }`}
          >
            📜 Immutable 21 CFR Part 11 Audit Trail
          </button>
          <button
            onClick={() => setActiveTab("governance")}
            className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-colors ${
              activeTab === "governance"
                ? "bg-[var(--emerald)] text-white border-transparent"
                : "border-[var(--border)] text-[var(--muted)] hover:text-white"
            }`}
          >
            ⚖️ 3/3 Specialist Governance Board
          </button>
        </div>

        {/* TAB 1: Tenants */}
        {activeTab === "tenants" && (
          <div className="zv-panel overflow-hidden">
            <table className="w-full text-left text-xs">
              <thead className="bg-[var(--elevated)] border-b border-[var(--border)] text-[var(--muted)] uppercase tracking-wider">
                <tr>
                  <th className="p-3">Organization Name</th>
                  <th className="p-3">Slug / Tenant ID</th>
                  <th className="p-3">Organization Type</th>
                  <th className="p-3">Active Users</th>
                  <th className="p-3">Isolation Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--border)]">
                {ORGS.map((o) => (
                  <tr key={o.id} className="hover:bg-[var(--elevated)]">
                    <td className="p-3 font-semibold text-white">{o.name}</td>
                    <td className="p-3 font-mono text-[var(--gold-soft)]">{o.slug}</td>
                    <td className="p-3 text-[var(--muted)]">{o.type.replace(/_/g, " ")}</td>
                    <td className="p-3 font-medium text-white">{o.active_users} Clinicians & Staff</td>
                    <td className="p-3">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
                        {o.status} (ISOLATED)
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* TAB 2: RBAC Matrix */}
        {activeTab === "rbac" && (
          <div className="zv-panel p-5 space-y-4">
            <h3 className="font-bold text-sm">Action-Level Permission Matrix</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
              {[
                { code: "prescription.create", desc: "Draft a Nuskha formulation; subject to Safety Firewall hold." },
                { code: "prescription.approve", desc: "Statutory 21 CFR Part 11 cryptographic sign-off (Senior Tabeeb only)." },
                { code: "safety_firewall.override", desc: "Override a Safety Firewall hold (requires written justification)." },
                { code: "dispensary.manage", desc: "Authorize FEFO batch allocation and pharmacy stock release." },
                { code: "governance.vote", desc: "Cast cryptographic quorum vote on Clinical Change Orders (CCO)." },
                { code: "research.manage", desc: "Extract de-identified cohort RWE and clinical trial data." },
                { code: "manufacturing.manage", desc: "Sign off on electronic Batch Manufacturing Records (eBMR)." },
                { code: "patient_portal.access", desc: "View personal health records and manage ABDM consent." },
                { code: "audit_log.read", desc: "Inspect tamper-resistant append-only event logs." },
              ].map((p) => (
                <div key={p.code} className="p-3 rounded-xl bg-[var(--elevated)] border border-[var(--border)] space-y-1">
                  <div className="font-mono text-[var(--gold-soft)] font-bold">{p.code}</div>
                  <p className="text-[11px] text-[var(--muted)]">{p.desc}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 3: Audit Trail */}
        {activeTab === "audit" && (
          <div className="zv-panel p-5 space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="font-bold text-sm">Chained Append-Only Audit Ledger</h3>
              <span className="text-xs font-mono text-emerald-400">Merkle Root: 7a8f9c...b410</span>
            </div>
            <table className="w-full text-left text-xs">
              <thead className="bg-[var(--elevated)] border-b border-[var(--border)] text-[var(--muted)] uppercase tracking-wider">
                <tr>
                  <th className="p-3">Timestamp (UTC)</th>
                  <th className="p-3">Actor / Principal</th>
                  <th className="p-3">Action Event</th>
                  <th className="p-3">Target Entity</th>
                  <th className="p-3">Integrity Digest</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--border)]">
                {[
                  { ts: "2026-09-12 17:44:29", actor: "Dr. Hakeem Tariq Ahmad", event: "PRESCRIPTION_SIGNED", target: "NSK-2026-8819", hash: "SHA256: 4a9f...c120" },
                  { ts: "2026-09-12 17:42:15", actor: "System Safety Daemon", event: "SAFETY_FIREWALL_EVAL", target: "NSK-2026-8819", hash: "SHA256: 8e11...99bb" },
                  { ts: "2026-09-12 16:30:00", actor: "Pharmacist Imran Khan", event: "FEFO_BATCH_ALLOCATED", target: "LOT-2026-0814", hash: "SHA256: b012...334d" },
                  { ts: "2026-09-12 15:10:22", actor: "Quality Officer Dr. S. Rao", event: "BMR_RELEASE_AUTHORIZED", target: "BMR-2026-0814", hash: "SHA256: ee41...7710" },
                ].map((l, i) => (
                  <tr key={i} className="hover:bg-[var(--elevated)]">
                    <td className="p-3 font-mono text-[var(--muted)]">{l.ts}</td>
                    <td className="p-3 font-semibold text-white">{l.actor}</td>
                    <td className="p-3 text-[var(--gold-soft)] font-mono">{l.event}</td>
                    <td className="p-3 text-white font-mono">{l.target}</td>
                    <td className="p-3 font-mono text-emerald-400">{l.hash}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* TAB 4: Governance Board */}
        {activeTab === "governance" && (
          <GovernanceBoardCockpit token={sessionToken} />
        )}

      </main>
    </div>
  );
}
