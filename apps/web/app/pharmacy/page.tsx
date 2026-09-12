"use client";

import React, { useState } from "react";
import { PlatformHeader } from "@/components/PlatformHeader";

interface BatchItem {
  id: string;
  medication_name: string;
  formulation_type: string;
  batch_number: string;
  manufacturer: string;
  expiry_date: string;
  available_quantity: number;
  unit: string;
  is_schedule_e1: boolean;
  mudabbar_certified: boolean;
  certificate_number: string;
  qc_release_status: "released" | "quarantined" | "pending_testing";
}

const INITIAL_BATCHES: BatchItem[] = [
  {
    id: "B-101",
    medication_name: "Suranjan Shireen Pulvis",
    formulation_type: "Safoof (Powder)",
    batch_number: "LOT-2026-0814",
    manufacturer: "Hamdard Laboratories",
    expiry_date: "2027-08-30",
    available_quantity: 450,
    unit: "grams",
    is_schedule_e1: false,
    mudabbar_certified: true,
    certificate_number: "MUD-2026-9912",
    qc_release_status: "released",
  },
  {
    id: "B-102",
    medication_name: "Suranjan Talkh (Colchicum luteum)",
    formulation_type: "Mufrad Crude",
    batch_number: "LOT-2026-0720",
    manufacturer: "Dehlvi Remedies",
    expiry_date: "2027-04-15",
    available_quantity: 210,
    unit: "grams",
    is_schedule_e1: true,
    mudabbar_certified: true,
    certificate_number: "MUD-CERT-SHA256-VALIDATED",
    qc_release_status: "released",
  },
  {
    id: "B-103",
    medication_name: "Kuchla Mudabbar (Strychnos nux-vomica)",
    formulation_type: "Processed Seeds",
    batch_number: "LOT-2026-0511",
    manufacturer: "Cipzer Ayush Pharma",
    expiry_date: "2026-11-20",
    available_quantity: 120,
    unit: "grams",
    is_schedule_e1: true,
    mudabbar_certified: false,
    certificate_number: "PENDING_ASSAY",
    qc_release_status: "quarantined",
  },
  {
    id: "B-104",
    medication_name: "Majun Suranjan",
    formulation_type: "Majun (Confection)",
    batch_number: "LOT-2026-0612",
    manufacturer: "Hamdard Laboratories",
    expiry_date: "2027-06-15",
    available_quantity: 35,
    unit: "jars (125g)",
    is_schedule_e1: false,
    mudabbar_certified: true,
    certificate_number: "MUD-2026-4419",
    qc_release_status: "released",
  },
];

export default function PharmacyPage() {
  const [batches, setBatches] = useState<BatchItem[]>(INITIAL_BATCHES);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterType, setFilterType] = useState("ALL");
  const [selectedBatch, setSelectedBatch] = useState<BatchItem | null>(INITIAL_BATCHES[0]);
  const [dispensePrescriptionId, setDispensePrescriptionId] = useState("NSK-2026-8819");
  const [dispenseResult, setDispenseResult] = useState<string | null>(null);
  const [isDispensing, setIsDispensing] = useState(false);

  const filteredBatches = batches.filter((b) => {
    const matchesSearch =
      b.medication_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      b.batch_number.toLowerCase().includes(searchQuery.toLowerCase()) ||
      b.manufacturer.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter =
      filterType === "ALL" ||
      (filterType === "SCHEDULE_E1" && b.is_schedule_e1) ||
      (filterType === "QUARANTINED" && b.qc_release_status === "quarantined");
    return matchesSearch && matchesFilter;
  });

  function handleDispense() {
    setIsDispensing(true);
    setDispenseResult(null);
    setTimeout(() => {
      setIsDispensing(false);
      if (selectedBatch?.is_schedule_e1 && !selectedBatch.mudabbar_certified) {
        setDispenseResult(
          "❌ DISPENSE BLOCKED: Schedule E(1) botanical lacks validated Mudabbar Detoxification Certificate. Statutory safety violation."
        );
      } else {
        setDispenseResult(
          `✓ DISPENSED SUCCESS: Batch ${selectedBatch?.batch_number} allocated to prescription ${dispensePrescriptionId} under FEFO priority.`
        );
        // Decrease stock
        if (selectedBatch) {
          setBatches(
            batches.map((b) =>
              b.id === selectedBatch.id
                ? { ...b, available_quantity: Math.max(0, b.available_quantity - 10) }
                : b
            )
          );
        }
      }
    }, 600);
  }

  function handleQuarantine(batchId: string) {
    setBatches(
      batches.map((b) =>
        b.id === batchId ? { ...b, qc_release_status: "quarantined" } : b
      )
    );
    alert(`Batch ${batchId} has been immediately quarantined. Dispensing locked across all clinics.`);
  }

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--text)]">
      <PlatformHeader />

      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-6 space-y-6">
        
        {/* Pharmacy Top Control Bar */}
        <div className="zv-panel p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold">ZAYVORA Pharmacy OS™ & FEFO Dispensing</h1>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-400 font-semibold">
                Central Dispensary
              </span>
            </div>
            <p className="text-xs text-[var(--muted)] mt-0.5">
              Automated First-Expired, First-Out batch allocation with statutory Schedule E(1) Mudabbar verification.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="text-[var(--muted)]">Active Batches:</span>
            <span className="font-bold text-white">{batches.length}</span>
            <span className="text-[var(--border)]">|</span>
            <span className="text-red-400 font-medium">1 Quarantined</span>
          </div>
        </div>

        {/* Layout Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Main Batch Inventory Table */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex flex-col sm:flex-row gap-3 justify-between items-center">
              <input
                type="text"
                placeholder="Search medication, LOT number, maker..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="zv-input text-xs max-w-sm"
              />
              <div className="flex items-center gap-2">
                <label className="text-xs text-[var(--muted)]">Filter:</label>
                <select
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                  className="zv-input text-xs py-1.5 px-3"
                >
                  <option value="ALL">All Batches</option>
                  <option value="SCHEDULE_E1">Schedule E(1) Only</option>
                  <option value="QUARANTINED">Quarantined Only</option>
                </select>
              </div>
            </div>

            <div className="zv-panel overflow-hidden">
              <table className="w-full text-left text-xs">
                <thead className="bg-[var(--elevated)] border-b border-[var(--border)] text-[var(--muted)] uppercase tracking-wider">
                  <tr>
                    <th className="p-3">Medication / Form</th>
                    <th className="p-3">Batch / LOT</th>
                    <th className="p-3">FEFO Expiry</th>
                    <th className="p-3">Stock Level</th>
                    <th className="p-3">Classification</th>
                    <th className="p-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border)]">
                  {filteredBatches.map((b) => (
                    <tr
                      key={b.id}
                      onClick={() => setSelectedBatch(b)}
                      className={`hover:bg-[var(--elevated)] cursor-pointer transition-colors ${
                        selectedBatch?.id === b.id ? "bg-[var(--elevated)]" : ""
                      }`}
                    >
                      <td className="p-3 font-medium">
                        <div className="text-white font-semibold">{b.medication_name}</div>
                        <div className="text-[11px] text-[var(--muted)]">{b.formulation_type} · {b.manufacturer}</div>
                      </td>
                      <td className="p-3 font-mono text-[var(--gold-soft)]">{b.batch_number}</td>
                      <td className="p-3 text-[var(--muted)]">{b.expiry_date}</td>
                      <td className="p-3 font-semibold text-white">
                        {b.available_quantity} {b.unit}
                      </td>
                      <td className="p-3">
                        {b.is_schedule_e1 ? (
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-red-500/20 text-red-400 border border-red-500/40">
                            Schedule E(1)
                          </span>
                        ) : (
                          <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
                            Standard Unani
                          </span>
                        )}
                      </td>
                      <td className="p-3">
                        <span
                          className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                            b.qc_release_status === "released"
                              ? "bg-emerald-500/20 text-emerald-400"
                              : "bg-red-500/20 text-red-400"
                          }`}
                        >
                          {b.qc_release_status.toUpperCase()}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Batch Dispense & Mudabbar Gate Control */}
          <div className="zv-panel p-5 space-y-4">
            <div className="border-b border-[var(--border)] pb-3">
              <span className="text-[10px] uppercase tracking-wider text-[var(--muted)] block">Dispensary Gate</span>
              <h3 className="text-base font-bold text-white">{selectedBatch?.medication_name}</h3>
              <span className="text-xs font-mono text-[var(--gold-soft)]">{selectedBatch?.batch_number}</span>
            </div>

            <div className="space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <span className="text-[var(--muted)] block">Current Available</span>
                  <span className="text-white font-semibold">{selectedBatch?.available_quantity} {selectedBatch?.unit}</span>
                </div>
                <div>
                  <span className="text-[var(--muted)] block">Expiration Window</span>
                  <span className="text-amber-400 font-semibold">{selectedBatch?.expiry_date}</span>
                </div>
              </div>

              {/* Schedule E1 Mudabbar Verification Card */}
              {selectedBatch?.is_schedule_e1 && (
                <div className={`p-3.5 rounded-xl border ${
                  selectedBatch.mudabbar_certified
                    ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-300"
                    : "bg-red-500/10 border-red-500/30 text-red-300"
                } space-y-1.5`}>
                  <div className="flex items-center gap-1.5 font-bold text-xs">
                    <span>{selectedBatch.mudabbar_certified ? "🛡️" : "⚠️"}</span>
                    <span>Schedule E(1) Detoxification Status</span>
                  </div>
                  <p className="text-[11px] leading-snug">
                    {selectedBatch.mudabbar_certified
                      ? `Detoxification Certificate Validated: ${selectedBatch.certificate_number}`
                      : "Lacks authorized Mudabbar purification assay. Dispense forbidden by statutory law."}
                  </p>
                </div>
              )}

              <div className="pt-2 border-t border-[var(--border)] space-y-2">
                <label className="text-[var(--muted)] block">Prescription ID for Dispensing</label>
                <input
                  className="zv-input text-xs"
                  value={dispensePrescriptionId}
                  onChange={(e) => setDispensePrescriptionId(e.target.value)}
                  placeholder="NSK-2026-XXXX"
                />
              </div>

              <div className="pt-2 flex flex-col gap-2">
                <button
                  onClick={handleDispense}
                  disabled={isDispensing || selectedBatch?.qc_release_status === "quarantined"}
                  className="zv-btn-primary text-xs font-semibold py-2.5 cursor-pointer disabled:opacity-50"
                >
                  {isDispensing ? "Verifying FEFO & Dispensing..." : "Fulfill & Dispense Batch"}
                </button>
                <button
                  onClick={() => selectedBatch && handleQuarantine(selectedBatch.id)}
                  className="px-3 py-2 rounded-lg border border-red-500/40 text-red-400 hover:bg-red-500/10 text-xs font-semibold cursor-pointer"
                >
                  Quarantine Entire Batch
                </button>
              </div>

              {dispenseResult && (
                <div className={`p-3 rounded-lg text-xs leading-relaxed ${
                  dispenseResult.startsWith("✓")
                    ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30"
                    : "bg-red-500/10 text-red-400 border border-red-500/30"
                }`}>
                  {dispenseResult}
                </div>
              )}
            </div>
          </div>

        </div>

      </main>
    </div>
  );
}
