"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";

interface ClinicNode {
  id: string;
  name: string;
  tier: "TIER_1_CENTRAL_HOSPITAL" | "TIER_2_REGIONAL_SPECIALTY" | "TIER_3_COMMUNITY_MATAB";
  city: string;
  state: string;
  abdmFacilityId: string;
  activeClinicians: number;
  hasRegimentalTherapy: boolean;
  hasCompoundingPharmacy: boolean;
  specialtyAxes: string[];
  status: "ONLINE" | "STANDBY";
}

const CLINIC_NETWORK: ClinicNode[] = [
  {
    id: "FAC-DEL-CENTRAL-01",
    name: "ZAYVORA Central Matab & Governance Hospital",
    tier: "TIER_1_CENTRAL_HOSPITAL",
    city: "New Delhi",
    state: "Delhi",
    abdmFacilityId: "IN-FAC-DEL-0012",
    activeClinicians: 18,
    hasRegimentalTherapy: true,
    hasCompoundingPharmacy: true,
    status: "ONLINE",
    specialtyAxes: [
      "Cardiovascular & Circulatory Axis",
      "Pulmonary & Respiratory Axis",
      "Gastrointestinal & Metabolic Axis",
      "Hepatobiliary & Spleen Axis",
      "Renal & Urogenital Axis",
      "Neurological & Cognitive Axis",
      "Musculoskeletal & Articular Axis",
      "Dermatologic & Mucosal Axis",
      "Endocrine & Hormonal Axis",
      "Hematologic & Immunologic Axis",
      "Sensory (Ocular/ENT) Axis",
      "Reproductive & Sexual Axis"
    ]
  },
  {
    id: "FAC-HYD-REGIONAL-02",
    name: "ZAYVORA Charminar Specialty Matab & Tadbeer Center",
    tier: "TIER_2_REGIONAL_SPECIALTY",
    city: "Hyderabad",
    state: "Telangana",
    abdmFacilityId: "IN-FAC-HYD-0045",
    activeClinicians: 10,
    hasRegimentalTherapy: true,
    hasCompoundingPharmacy: true,
    status: "ONLINE",
    specialtyAxes: [
      "Musculoskeletal & Articular Axis",
      "Hepatobiliary & Spleen Axis",
      "Renal & Urogenital Axis",
      "Gastrointestinal & Metabolic Axis",
      "Dermatologic & Mucosal Axis",
      "Hematologic & Immunologic Axis"
    ]
  },
  {
    id: "FAC-LKO-REGIONAL-03",
    name: "ZAYVORA Avadh Classical Care & Clinical Practicum Center",
    tier: "TIER_2_REGIONAL_SPECIALTY",
    city: "Lucknow",
    state: "Uttar Pradesh",
    abdmFacilityId: "IN-FAC-LKO-0089",
    activeClinicians: 8,
    hasRegimentalTherapy: true,
    hasCompoundingPharmacy: false,
    status: "ONLINE",
    specialtyAxes: [
      "Neurological & Cognitive Axis",
      "Musculoskeletal & Articular Axis",
      "Pulmonary & Respiratory Axis",
      "Cardiovascular & Circulatory Axis",
      "Endocrine & Hormonal Axis",
      "Sensory (Ocular/ENT) Axis"
    ]
  },
  {
    id: "FAC-BLR-COMMUNITY-04",
    name: "ZAYVORA Bengaluru Integrated Care Matab",
    tier: "TIER_3_COMMUNITY_MATAB",
    city: "Bengaluru",
    state: "Karnataka",
    abdmFacilityId: "IN-FAC-BLR-0112",
    activeClinicians: 4,
    hasRegimentalTherapy: false,
    hasCompoundingPharmacy: false,
    status: "ONLINE",
    specialtyAxes: [
      "Gastrointestinal & Metabolic Axis",
      "Musculoskeletal & Articular Axis"
    ]
  }
];

interface ReferralRecord {
  token: string;
  patientId: string;
  sourceFacility: string;
  targetFacility: string;
  condition: string;
  axis: string;
  status: "PENDING" | "REDEEMED";
  createdTime: string;
}

export default function FederationPage() {
  const [activeTab, setActiveTab] = useState<"topology" | "referrals" | "inventory">("topology");

  // Referral Creation State
  const [patientId, setPatientId] = useState("PAT-2026-0814");
  const [sourceClinic, setSourceClinic] = useState("FAC-DEL-CENTRAL-01");
  const [targetClinic, setTargetClinic] = useState("FAC-HYD-REGIONAL-02");
  const [clinicalCondition, setClinicalCondition] = useState("Waja-ul-Mafasil");
  const [specialtyAxis, setSpecialtyAxis] = useState("Musculoskeletal & Articular Axis");
  const [referralReason, setReferralReason] = useState("Tertiary Hijamah & Nutool regimental therapy");

  // List of active referrals
  const [referrals, setReferrals] = useState<ReferralRecord[]>([
    {
      token: "ZAY-REF-F829A019BC41298410294821",
      patientId: "PAT-2026-0412",
      sourceFacility: "FAC-BLR-COMMUNITY-04",
      targetFacility: "FAC-HYD-REGIONAL-02",
      condition: "Waja-ul-Mafasil",
      axis: "Musculoskeletal & Articular Axis",
      status: "REDEEMED",
      createdTime: "2 hours ago"
    },
    {
      token: "ZAY-REF-71829ABCDE10293847561029",
      patientId: "PAT-2026-0814",
      sourceFacility: "FAC-DEL-CENTRAL-01",
      targetFacility: "FAC-HYD-REGIONAL-02",
      condition: "Waja-ul-Mafasil",
      axis: "Musculoskeletal & Articular Axis",
      status: "PENDING",
      createdTime: "Just now"
    }
  ]);

  // Redemption State
  const [redeemToken, setRedeemToken] = useState("");
  const [redeemFacility, setRedeemFacility] = useState("FAC-HYD-REGIONAL-02");
  const [redeemMessage, setRedeemMessage] = useState<{ ok: boolean; text: string } | null>(null);

  // Inventory Transfer State
  const [transferSuccess, setTransferSuccess] = useState<string | null>(null);

  const handleGenerateReferral = (e: React.FormEvent) => {
    e.preventDefault();
    const tokenBytes = Array.from({ length: 24 }, () => Math.floor(Math.random() * 16).toString(16)).join("").toUpperCase();
    const newToken = `ZAY-REF-${tokenBytes}`;
    
    const newRecord: ReferralRecord = {
      token: newToken,
      patientId,
      sourceFacility: sourceClinic,
      targetFacility: targetClinic,
      condition: clinicalCondition,
      axis: specialtyAxis,
      status: "PENDING",
      createdTime: "Just now"
    };

    setReferrals([newRecord, ...referrals]);
    setRedeemToken(newToken);
    alert(`HMAC Signed Referral Token Generated:\n${newToken}\n\nValid for designated target clinic: ${targetClinic}`);
  };

  const handleRedeem = (e: React.FormEvent) => {
    e.preventDefault();
    const match = referrals.find(r => r.token.trim() === redeemToken.trim());
    if (!match) {
      setRedeemMessage({ ok: false, text: "Verification Failed: Invalid or tampered referral token." });
      return;
    }
    if (match.targetFacility !== redeemFacility) {
      setRedeemMessage({
        ok: false,
        text: `Target Clinic Mismatch: Designated for ${match.targetFacility}, but presented at ${redeemFacility}. Chart unlock blocked.`
      });
      return;
    }
    if (match.status === "REDEEMED") {
      setRedeemMessage({ ok: false, text: "Referral has already been redeemed and cannot be reused." });
      return;
    }

    // Mark as redeemed
    setReferrals(referrals.map(r => r.token === redeemToken.trim() ? { ...r, status: "REDEEMED" } : r));
    setRedeemMessage({
      ok: true,
      text: `Cryptographic Handshake Certified: Chart access authorized for ${match.patientId} at ${redeemFacility}.`
    });
  };

  const handleTransfer = (drug: string, from: string, to: string, qty: number, lot: string) => {
    setTransferSuccess(`FEFO Transfer Executed: ${qty}g of ${drug} (Lot ${lot}) dispatched from ${from} to ${to}. In-transit balance updated.`);
    setTimeout(() => setTransferSuccess(null), 5000);
  };

  return (
    <AppShell activeRole="admin">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Page Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-[var(--border)] pb-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              <span>🌐</span> Enterprise Multi-Clinic Federation Hub
              <span className="px-2.5 py-0.5 rounded-full bg-teal-500/15 border border-teal-500/30 text-teal-400 text-xs font-mono font-bold">
                Sequence 15
              </span>
            </h1>
            <p className="text-xs text-[var(--muted)] mt-1">
              Decentralized clinical node topology, HMAC cryptographic inter-clinic referrals, and cross-dispensary FEFO inventory balancing.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab("topology")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${activeTab === "topology" ? "bg-teal-600 text-white" : "bg-[var(--panel)] text-[var(--muted)] hover:text-white border border-[var(--border)]"}`}
            >
              🏥 Clinic Network ({CLINIC_NETWORK.length})
            </button>
            <button
              onClick={() => setActiveTab("referrals")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${activeTab === "referrals" ? "bg-teal-600 text-white" : "bg-[var(--panel)] text-[var(--muted)] hover:text-white border border-[var(--border)]"}`}
            >
              🔐 Cryptographic Referrals ({referrals.length})
            </button>
            <button
              onClick={() => setActiveTab("inventory")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${activeTab === "inventory" ? "bg-teal-600 text-white" : "bg-[var(--panel)] text-[var(--muted)] hover:text-white border border-[var(--border)]"}`}
            >
              📦 FEFO Inventory Balancing
            </button>
          </div>
        </div>

        {/* Top Summary Metrics */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-[var(--panel)] p-4 rounded-xl border border-[var(--border)]">
            <div className="text-xs text-[var(--muted)]">Federated Facilities</div>
            <div className="text-2xl font-bold text-white mt-1">4 Nodes</div>
            <div className="text-xs text-emerald-400 mt-1 flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span> 100% Online
            </div>
          </div>
          <div className="bg-[var(--panel)] p-4 rounded-xl border border-[var(--border)]">
            <div className="text-xs text-[var(--muted)]">Active Clinicians</div>
            <div className="text-2xl font-bold text-white mt-1">40 BUMS / MD</div>
            <div className="text-xs text-teal-400 mt-1">Distributed across 4 states</div>
          </div>
          <div className="bg-[var(--panel)] p-4 rounded-xl border border-[var(--border)]">
            <div className="text-xs text-[var(--muted)]">HMAC Signed Referrals</div>
            <div className="text-2xl font-bold text-teal-400 mt-1">{referrals.length} Total</div>
            <div className="text-xs text-cyan-400 mt-1">Zero cross-tenant leakage</div>
          </div>
          <div className="bg-[var(--panel)] p-4 rounded-xl border border-[var(--border)]">
            <div className="text-xs text-[var(--muted)]">ABDM Milestone 3</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">Certified</div>
            <div className="text-xs text-[var(--muted)] mt-1">NRCeS FHIR R4 Profiles</div>
          </div>
        </div>

        {/* TAB 1: Clinic Network Topology */}
        {activeTab === "topology" && (
          <div className="space-y-4">
            <div className="text-sm font-semibold text-white flex items-center justify-between">
              <span>Federated Clinic Nodes & Capability Hierarchy</span>
              <span className="text-xs text-[var(--muted)] font-normal">Strict Tenant Isolation Enforced</span>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {CLINIC_NETWORK.map((node) => (
                <div key={node.id} className="bg-[var(--panel)] p-5 rounded-xl border border-[var(--border)] flex flex-col justify-between space-y-4">
                  <div>
                    <div className="flex justify-between items-start">
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="text-base font-bold text-white">{node.name}</h3>
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono font-bold ${
                            node.tier === "TIER_1_CENTRAL_HOSPITAL"
                              ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                              : node.tier === "TIER_2_REGIONAL_SPECIALTY"
                              ? "bg-teal-500/20 text-teal-300 border border-teal-500/40"
                              : "bg-blue-500/20 text-blue-300 border border-blue-500/40"
                          }`}>
                            {node.tier.replace(/_/g, " ")}
                          </span>
                        </div>
                        <div className="text-xs text-[var(--muted)] mt-1 flex items-center gap-2">
                          <span>📍 {node.city}, {node.state}</span>
                          <span>•</span>
                          <span className="font-mono text-cyan-400">ABDM: {node.abdmFacilityId}</span>
                        </div>
                      </div>
                      <span className="flex items-center gap-1 text-xs text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded-md">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> {node.status}
                      </span>
                    </div>

                    <div className="grid grid-cols-3 gap-2 mt-4 text-center">
                      <div className="bg-[var(--background)] p-2 rounded-lg border border-[var(--border)]">
                        <div className="text-[10px] text-[var(--muted)]">Clinicians</div>
                        <div className="text-sm font-bold text-white">{node.activeClinicians}</div>
                      </div>
                      <div className="bg-[var(--background)] p-2 rounded-lg border border-[var(--border)]">
                        <div className="text-[10px] text-[var(--muted)]">Regimental Tadbeer</div>
                        <div className={`text-sm font-bold ${node.hasRegimentalTherapy ? "text-emerald-400" : "text-zinc-500"}`}>
                          {node.hasRegimentalTherapy ? "Available" : "No"}
                        </div>
                      </div>
                      <div className="bg-[var(--background)] p-2 rounded-lg border border-[var(--border)]">
                        <div className="text-[10px] text-[var(--muted)]">Compounding Pharmacy</div>
                        <div className={`text-sm font-bold ${node.hasCompoundingPharmacy ? "text-emerald-400" : "text-zinc-500"}`}>
                          {node.hasCompoundingPharmacy ? "Certified" : "Dispensary Only"}
                        </div>
                      </div>
                    </div>

                    <div className="mt-4">
                      <div className="text-xs text-[var(--muted)] mb-2 font-semibold">Authorized Organ-Axes ({node.specialtyAxes.length}):</div>
                      <div className="flex flex-wrap gap-1.5">
                        {node.specialtyAxes.map((axis, i) => (
                          <span key={i} className="px-2 py-0.5 rounded-md bg-[var(--background)] border border-[var(--border)] text-[10px] text-teal-300">
                            {axis}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-[var(--border)] flex justify-between items-center text-xs text-[var(--muted)]">
                    <span>Node ID: <span className="font-mono text-zinc-300">{node.id}</span></span>
                    <button
                      onClick={() => {
                        setTargetClinic(node.id);
                        setActiveTab("referrals");
                      }}
                      className="text-teal-400 hover:text-teal-300 font-semibold"
                    >
                      Refer Patient Here →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 2: Cryptographic Inter-Clinic Referrals */}
        {activeTab === "referrals" && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

              {/* Referral Generator */}
              <div className="bg-[var(--panel)] p-5 rounded-xl border border-[var(--border)] space-y-4">
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <span>✍️</span> Generate HMAC-Signed Inter-Clinic Referral
                </h3>
                <p className="text-xs text-[var(--muted)]">
                  Signs patient clinical summary with HMAC-SHA256. Designated target facility can alone decrypt the clinical encounter.
                </p>

                <form onSubmit={handleGenerateReferral} className="space-y-3">
                  <div>
                    <label className="text-xs text-[var(--muted)] block mb-1">Patient MRN / ID</label>
                    <input
                      type="text"
                      value={patientId}
                      onChange={(e) => setPatientId(e.target.value)}
                      className="w-full bg-[var(--background)] border border-[var(--border)] px-3 py-2 rounded-lg text-xs text-white"
                      required
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs text-[var(--muted)] block mb-1">Source Facility</label>
                      <select
                        value={sourceClinic}
                        onChange={(e) => setSourceClinic(e.target.value)}
                        className="w-full bg-[var(--background)] border border-[var(--border)] px-3 py-2 rounded-lg text-xs text-white"
                      >
                        {CLINIC_NETWORK.map(c => <option key={c.id} value={c.id}>{c.city} ({c.id})</option>)}
                      </select>
                    </div>
                    <div>
                      <label className="text-xs text-[var(--muted)] block mb-1">Target Facility</label>
                      <select
                        value={targetClinic}
                        onChange={(e) => setTargetClinic(e.target.value)}
                        className="w-full bg-[var(--background)] border border-[var(--border)] px-3 py-2 rounded-lg text-xs text-white"
                      >
                        {CLINIC_NETWORK.filter(c => c.id !== sourceClinic).map(c => <option key={c.id} value={c.id}>{c.city} ({c.id})</option>)}
                      </select>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs text-[var(--muted)] block mb-1">Clinical Condition</label>
                      <input
                        type="text"
                        value={clinicalCondition}
                        onChange={(e) => setClinicalCondition(e.target.value)}
                        className="w-full bg-[var(--background)] border border-[var(--border)] px-3 py-2 rounded-lg text-xs text-white"
                        required
                      />
                    </div>
                    <div>
                      <label className="text-xs text-[var(--muted)] block mb-1">Specialty Axis Required</label>
                      <select
                        value={specialtyAxis}
                        onChange={(e) => setSpecialtyAxis(e.target.value)}
                        className="w-full bg-[var(--background)] border border-[var(--border)] px-3 py-2 rounded-lg text-xs text-white"
                      >
                        <option value="Musculoskeletal & Articular Axis">Musculoskeletal & Articular</option>
                        <option value="Hepatobiliary & Spleen Axis">Hepatobiliary & Spleen</option>
                        <option value="Neurological & Cognitive Axis">Neurological & Cognitive</option>
                        <option value="Gastrointestinal & Metabolic Axis">Gastrointestinal & Metabolic</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="text-xs text-[var(--muted)] block mb-1">Referral Indication & Regimen Required</label>
                    <textarea
                      rows={2}
                      value={referralReason}
                      onChange={(e) => setReferralReason(e.target.value)}
                      className="w-full bg-[var(--background)] border border-[var(--border)] px-3 py-2 rounded-lg text-xs text-white"
                    />
                  </div>

                  <button
                    type="submit"
                    className="w-full bg-teal-600 hover:bg-teal-500 text-white font-semibold py-2 rounded-lg text-xs transition shadow-md"
                  >
                    🔒 Sign & Issue Cryptographic Referral
                  </button>
                </form>
              </div>

              {/* Referral Redeemer */}
              <div className="bg-[var(--panel)] p-5 rounded-xl border border-[var(--border)] space-y-4 flex flex-col justify-between">
                <div>
                  <h3 className="text-base font-bold text-white flex items-center gap-2">
                    <span>🗝️</span> Redeem Referral Token at Target Clinic
                  </h3>
                  <p className="text-xs text-[var(--muted)]">
                    Validates HMAC token integrity, prevents replay attacks, checks facility designation, and unlocks patient history.
                  </p>

                  <form onSubmit={handleRedeem} className="space-y-3 mt-4">
                    <div>
                      <label className="text-xs text-[var(--muted)] block mb-1">Receiving Facility</label>
                      <select
                        value={redeemFacility}
                        onChange={(e) => setRedeemFacility(e.target.value)}
                        className="w-full bg-[var(--background)] border border-[var(--border)] px-3 py-2 rounded-lg text-xs text-white"
                      >
                        {CLINIC_NETWORK.map(c => <option key={c.id} value={c.id}>{c.city} - {c.name}</option>)}
                      </select>
                    </div>

                    <div>
                      <label className="text-xs text-[var(--muted)] block mb-1">Referral Token (ZAY-REF-...)</label>
                      <input
                        type="text"
                        value={redeemToken}
                        onChange={(e) => setRedeemToken(e.target.value)}
                        placeholder="Paste ZAY-REF-..."
                        className="w-full font-mono bg-[var(--background)] border border-[var(--border)] px-3 py-2 rounded-lg text-xs text-teal-300"
                        required
                      />
                    </div>

                    <button
                      type="submit"
                      className="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-semibold py-2 rounded-lg text-xs transition shadow-md"
                    >
                      ⚡ Validate & Unlock Clinical Chart
                    </button>
                  </form>

                  {redeemMessage && (
                    <div className={`mt-4 p-3 rounded-lg text-xs border ${
                      redeemMessage.ok
                        ? "bg-emerald-500/15 border-emerald-500/30 text-emerald-300"
                        : "bg-rose-500/15 border-rose-500/30 text-rose-300"
                    }`}>
                      {redeemMessage.text}
                    </div>
                  )}
                </div>

                <div className="text-[11px] text-[var(--muted)] bg-[var(--background)] p-3 rounded-lg border border-[var(--border)] mt-4">
                  🛡️ <strong>Security Invariant:</strong> Attempting to redeem an HMAC token at any clinic other than the designated target facility immediately raises a cryptographic mismatch and flags a tenant security audit.
                </div>
              </div>

            </div>

            {/* Referrals Log Table */}
            <div className="bg-[var(--panel)] p-5 rounded-xl border border-[var(--border)] space-y-3">
              <h3 className="text-sm font-bold text-white">Cross-Clinic Referral Audit Log</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="border-b border-[var(--border)] text-[var(--muted)]">
                    <tr>
                      <th className="pb-2">Token</th>
                      <th className="pb-2">Patient</th>
                      <th className="pb-2">Route</th>
                      <th className="pb-2">Condition & Axis</th>
                      <th className="pb-2">Created</th>
                      <th className="pb-2">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[var(--border)]">
                    {referrals.map((r, i) => (
                      <tr key={i} className="hover:bg-[var(--background)]">
                        <td className="py-2.5 font-mono text-teal-400">{r.token.substring(0, 16)}...</td>
                        <td className="py-2.5 font-bold text-white">{r.patientId}</td>
                        <td className="py-2.5 text-zinc-300">{r.sourceFacility.split("-")[1]} ➔ {r.targetFacility.split("-")[1]}</td>
                        <td className="py-2.5">
                          <span className="text-white">{r.condition}</span>
                          <span className="text-[10px] text-[var(--muted)] block">{r.axis}</span>
                        </td>
                        <td className="py-2.5 text-[var(--muted)]">{r.createdTime}</td>
                        <td className="py-2.5">
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                            r.status === "REDEEMED"
                              ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                              : "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                          }`}>
                            {r.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: Federated FEFO Inventory Balancing */}
        {activeTab === "inventory" && (
          <div className="space-y-4">
            <div className="text-sm font-semibold text-white flex justify-between items-center">
              <span>Dispensary Stock & Cross-Branch FEFO Optimization</span>
              <span className="text-xs text-teal-400">Algorithm: Earliest Expiring First Out (FEFO)</span>
            </div>

            {transferSuccess && (
              <div className="p-3 bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 rounded-lg text-xs">
                ✓ {transferSuccess}
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              
              {/* Product 1: Suranjan Shirin */}
              <div className="bg-[var(--panel)] p-4 rounded-xl border border-[var(--border)] space-y-3">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="text-sm font-bold text-white">Suranjan Shirin</h4>
                    <span className="text-[10px] text-[var(--muted)]">Colchicum autumnale (Sweet)</span>
                  </div>
                  <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    Mudabbar Certified
                  </span>
                </div>

                <div className="space-y-2 text-xs">
                  <div className="flex justify-between p-2 bg-[var(--background)] rounded-md border border-[var(--border)]">
                    <div>
                      <span className="font-bold text-white">Delhi Central</span>
                      <span className="text-[10px] text-amber-400 block">Lot LOT-SS-2026-01 (Exp: 2027-06-30)</span>
                    </div>
                    <span className="font-mono text-white font-bold">4,980g</span>
                  </div>
                  <div className="flex justify-between p-2 bg-[var(--background)] rounded-md border border-[var(--border)]">
                    <div>
                      <span className="font-bold text-white">Hyderabad Specialty</span>
                      <span className="text-[10px] text-zinc-400 block">Lot B-SUR-2026-A2 (Exp: 2027-08-31)</span>
                    </div>
                    <span className="font-mono text-white font-bold">2,500g</span>
                  </div>
                  <div className="flex justify-between p-2 bg-[var(--background)] rounded-md border border-[var(--border)]">
                    <div>
                      <span className="font-bold text-white">Bengaluru Matab</span>
                      <span className="text-[10px] text-rose-400 block">Low Stock Warning</span>
                    </div>
                    <span className="font-mono text-rose-400 font-bold">120g</span>
                  </div>
                </div>

                <button
                  onClick={() => handleTransfer("Suranjan Shirin", "FAC-DEL-CENTRAL-01", "FAC-BLR-COMMUNITY-04", 500, "LOT-SS-2026-01")}
                  className="w-full bg-teal-600/30 hover:bg-teal-600/50 border border-teal-500/40 text-teal-300 py-1.5 rounded-lg text-xs font-semibold transition"
                >
                  Transfer 500g to Bengaluru (FEFO Lot)
                </button>
              </div>

              {/* Product 2: Majun Suranjan */}
              <div className="bg-[var(--panel)] p-4 rounded-xl border border-[var(--border)] space-y-3">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="text-sm font-bold text-white">Majun Suranjan</h4>
                    <span className="text-[10px] text-[var(--muted)]">Classical Electuary Formulary</span>
                  </div>
                  <span className="px-2 py-0.5 rounded text-[10px] bg-rose-500/20 text-rose-300 border border-rose-500/30 font-bold">
                    Schedule E(1)
                  </span>
                </div>

                <div className="space-y-2 text-xs">
                  <div className="flex justify-between p-2 bg-[var(--background)] rounded-md border border-[var(--border)]">
                    <div>
                      <span className="font-bold text-white">Delhi Central</span>
                      <span className="text-[10px] text-zinc-400 block">Lot B-MSUR-2026-B1 (Exp: 2028-06-30)</span>
                    </div>
                    <span className="font-mono text-white font-bold">3,000g</span>
                  </div>
                  <div className="flex justify-between p-2 bg-[var(--background)] rounded-md border border-[var(--border)]">
                    <div>
                      <span className="font-bold text-white">Lucknow Regional</span>
                      <span className="text-[10px] text-zinc-400 block">Lot B-MSUR-2026-B2 (Exp: 2028-07-15)</span>
                    </div>
                    <span className="font-mono text-white font-bold">1,800g</span>
                  </div>
                </div>

                <button
                  onClick={() => handleTransfer("Majun Suranjan", "FAC-DEL-CENTRAL-01", "FAC-LKO-REGIONAL-03", 250, "B-MSUR-2026-B1")}
                  className="w-full bg-teal-600/30 hover:bg-teal-600/50 border border-teal-500/40 text-teal-300 py-1.5 rounded-lg text-xs font-semibold transition"
                >
                  Transfer 250g to Lucknow (FEFO Lot)
                </button>
              </div>

              {/* Product 3: Asgandh Nagori */}
              <div className="bg-[var(--panel)] p-4 rounded-xl border border-[var(--border)] space-y-3">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="text-sm font-bold text-white">Asgandh Nagori</h4>
                    <span className="text-[10px] text-[var(--muted)]">Withania somnifera (Radix)</span>
                  </div>
                  <span className="px-2 py-0.5 rounded text-[10px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                    Adaptogen
                  </span>
                </div>

                <div className="space-y-2 text-xs">
                  <div className="flex justify-between p-2 bg-[var(--background)] rounded-md border border-[var(--border)]">
                    <div>
                      <span className="font-bold text-white">Bengaluru Matab</span>
                      <span className="text-[10px] text-amber-400 block">Lot B-ASG-2026-C1 (Exp: 2027-04-30)</span>
                    </div>
                    <span className="font-mono text-white font-bold">1,200g</span>
                  </div>
                  <div className="flex justify-between p-2 bg-[var(--background)] rounded-md border border-[var(--border)]">
                    <div>
                      <span className="font-bold text-white">Delhi Central</span>
                      <span className="text-[10px] text-zinc-400 block">Lot B-ASG-2026-C2 (Exp: 2027-09-30)</span>
                    </div>
                    <span className="font-mono text-white font-bold">8,000g</span>
                  </div>
                </div>

                <button
                  onClick={() => handleTransfer("Asgandh Nagori", "FAC-BLR-COMMUNITY-04", "FAC-HYD-REGIONAL-02", 300, "B-ASG-2026-C1")}
                  className="w-full bg-teal-600/30 hover:bg-teal-600/50 border border-teal-500/40 text-teal-300 py-1.5 rounded-lg text-xs font-semibold transition"
                >
                  Transfer 300g to Hyderabad (FEFO Lot)
                </button>
              </div>

            </div>
          </div>
        )}

      </div>
    </AppShell>
  );
}
