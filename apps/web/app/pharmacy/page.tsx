"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";

interface PrescriptionOrder {
  id: string;
  orderNumber: string;
  patientName: string;
  mrn: string;
  doctorName: string;
  doctorReg: string;
  items: {
    name: string;
    dose: string;
    isScheduleE1: boolean;
    mudabbarRequired: boolean;
    batchNumber: string;
    expiryDate: string;
    mudabbarCert: string | null;
  }[];
  signatureHash: string;
  status: "PENDING_VERIFICATION" | "VERIFIED_READY" | "DISPENSED";
}

const INITIAL_ORDERS: PrescriptionOrder[] = [
  {
    id: "ORD-9011",
    orderNumber: "RX-2026-0441",
    patientName: "Hamza Farooqi",
    mrn: "MRN-2026-0814",
    doctorName: "Hakim Dr. Tariq Mansoor",
    doctorReg: "CCIM-BUMS-2004-9841",
    items: [
      {
        name: "Majun Suranjan",
        dose: "5g twice daily • 14 days",
        isScheduleE1: true,
        mudabbarRequired: true,
        batchNumber: "MS-2026-LOT4",
        expiryDate: "2027-08-30",
        mudabbarCert: "SHA256:7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b",
      },
      {
        name: "Raughan-e-Balsan",
        dose: "Local application nocte • 14 days",
        isScheduleE1: false,
        mudabbarRequired: false,
        batchNumber: "RB-2026-LOT1",
        expiryDate: "2028-01-15",
        mudabbarCert: null,
      },
    ],
    signatureHash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    status: "PENDING_VERIFICATION",
  },
  {
    id: "ORD-9012",
    orderNumber: "RX-2026-0442",
    patientName: "Aisha Siddiqui",
    mrn: "MRN-2026-0815",
    doctorName: "Hakim Dr. Tariq Mansoor",
    doctorReg: "CCIM-BUMS-2004-9841",
    items: [
      {
        name: "Jawarish Kamuni Kabir",
        dose: "5g after meals • 10 days",
        isScheduleE1: false,
        mudabbarRequired: false,
        batchNumber: "JK-2026-LOT9",
        expiryDate: "2027-12-01",
        mudabbarCert: null,
      },
    ],
    signatureHash: "8f4b29c91a03e147b2c9d01248a0f9b3e217c49b01538a7c29b0134f59c14820",
    status: "PENDING_VERIFICATION",
  },
];

export default function PharmacyWorkspacePage() {
  const [activeTab, setActiveTab] = useState<"queue" | "inventory" | "fefo" | "mudabbar">("queue");
  const [orders, setOrders] = useState<PrescriptionOrder[]>(INITIAL_ORDERS);
  const [selectedOrder, setSelectedOrder] = useState<PrescriptionOrder | null>(null);

  // 12-Step Dispensing Verification Checklist Modal
  const [isVerifying, setIsVerifying] = useState(false);
  const [checklist, setChecklist] = useState({
    step1_auth_rx: false,
    step2_patient_id: false,
    step3_rx_content: false,
    step4_medicine_match: false,
    step5_batch_fefo: false,
    step6_expiry_valid: false,
    step7_stock_sufficient: false,
    step8_mudabbar_gate: false,
    step9_pharmacist_auth: false,
    step10_merkle_record: false,
    step11_patient_posology: false,
    step12_inventory_decrement: false,
  });

  const handleStartDispense = (order: PrescriptionOrder) => {
    setSelectedOrder(order);
    setChecklist({
      step1_auth_rx: true,
      step2_patient_id: true,
      step3_rx_content: true,
      step4_medicine_match: true,
      step5_batch_fefo: true,
      step6_expiry_valid: true,
      step7_stock_sufficient: true,
      step8_mudabbar_gate: order.items.every(i => !i.mudabbarRequired || i.mudabbarCert !== null),
      step9_pharmacist_auth: false,
      step10_merkle_record: false,
      step11_patient_posology: false,
      step12_inventory_decrement: false,
    });
    setIsVerifying(true);
  };

  const handleConfirmDispense = () => {
    if (!selectedOrder) return;
    setOrders(orders.map(o => o.id === selectedOrder.id ? { ...o, status: "DISPENSED" } : o));
    setIsVerifying(false);
    setSelectedOrder(null);
  };

  return (
    <AppShell activeRole="pharmacy">
      <div className="space-y-5 max-w-7xl mx-auto">
        
        {/* Workspace Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight">Clinical Pharmacy OS & Dispensary</h1>
            <p className="text-xs text-[#94A3B8]">
              Central Dispensary Unit • Pharmacist Zainab Ali • Schedule E(1) Gate Active
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="zv-badge-teal px-3 py-1 rounded-lg text-xs font-semibold flex items-center gap-1.5">
              🛡️ FEFO Prioritized & Mudabbar Enforced
            </span>
          </div>
        </div>

        {/* Pharmacy Executive Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <StatCard label="Pending Dispense" value={orders.filter(o => o.status === "PENDING_VERIFICATION").length} subtext="Awaiting verification" variant="amber" icon="⏳" />
          <StatCard label="Dispensed Today" value={orders.filter(o => o.status === "DISPENSED").length + 14} subtext="100% verified" variant="emerald" icon="✓" />
          <StatCard label="Schedule E(1) Lots" value="2 Lots" subtext="Suranjan Talkh (Mudabbar)" variant="teal" icon="🛡️" />
          <StatCard label="FEFO Near Expiry" value="0 Batches" subtext="No expired stock" variant="teal" icon="📦" />
        </div>

        {/* Tab Navigation */}
        <div className="border-b border-[#334155] flex gap-2">
          {[
            { id: "queue", label: "Prescription Dispensing Queue", icon: "💊" },
            { id: "fefo", label: "FEFO Batch Inventory", icon: "📦" },
            { id: "mudabbar", label: "Schedule E(1) Mudabbar Gate", icon: "🛡️" },
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

        {/* TAB 1: DISPENSING QUEUE */}
        {activeTab === "queue" && (
          <div className="zv-card overflow-hidden">
            <div className="p-4 border-b border-[#334155] bg-[#0F172A] flex justify-between items-center">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider">Authorized Prescriptions Ready for Dispensing</h3>
              <span className="text-[11px] text-[#94A3B8]">Cryptographically signed via 21 CFR Part 11</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-[#0A0F1D] text-[#94A3B8] border-b border-[#334155]">
                  <tr>
                    <th className="p-3">Order / Rx ID</th>
                    <th className="p-3">Patient Name / MRN</th>
                    <th className="p-3">Prescribing Physician</th>
                    <th className="p-3">Medications & Batches</th>
                    <th className="p-3">Safety Status</th>
                    <th className="p-3">Order Status</th>
                    <th className="p-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#334155]">
                  {orders.map((order) => (
                    <tr key={order.id} className="hover:bg-[#1E293B]/50 transition">
                      <td className="p-3 font-mono font-bold text-white">{order.orderNumber}</td>
                      <td className="p-3">
                        <span className="font-semibold text-white block">{order.patientName}</span>
                        <span className="text-[11px] text-[#94A3B8] font-mono">{order.mrn}</span>
                      </td>
                      <td className="p-3">
                        <span className="text-white font-medium block">{order.doctorName}</span>
                        <span className="text-[10px] text-[#94A3B8]">{order.doctorReg}</span>
                      </td>
                      <td className="p-3 space-y-1">
                        {order.items.map((it) => (
                          <div key={it.name} className="flex items-center gap-1.5">
                            <span className="text-white">{it.name}</span>
                            <span className="font-mono text-[10px] text-[#2DD4BF]">({it.batchNumber})</span>
                            {it.isScheduleE1 && (
                              <span className="text-[9px] px-1 py-0.5 rounded bg-[#F59E0B]/20 text-[#FBBF24]">E(1)</span>
                            )}
                          </div>
                        ))}
                      </td>
                      <td className="p-3">
                        {order.items.some(i => i.isScheduleE1) ? (
                          <span className="text-[11px] font-semibold text-[#34D399] flex items-center gap-1">
                            ✓ Mudabbar Certified
                          </span>
                        ) : (
                          <span className="text-[11px] text-[#94A3B8]">Standard Safety</span>
                        )}
                      </td>
                      <td className="p-3">
                        <StatusBadge
                          status={order.status.replace("_", " ")}
                          variant={order.status === "DISPENSED" ? "verified" : "pending"}
                        />
                      </td>
                      <td className="p-3 text-right">
                        {order.status === "PENDING_VERIFICATION" ? (
                          <button
                            onClick={() => handleStartDispense(order)}
                            className="zv-btn-primary text-xs py-1 px-3 bg-[#0D9488]"
                          >
                            12-Step Dispense
                          </button>
                        ) : (
                          <span className="text-[11px] text-[#34D399] font-medium">✓ Completed</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* TAB 2: FEFO BATCH INVENTORY */}
        {activeTab === "fefo" && (
          <div className="zv-card p-5 space-y-4 text-xs">
            <h3 className="text-sm font-bold text-white">First Expiry, First Out (FEFO) Inventory Allocation</h3>
            <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-1">
              <span className="font-bold text-[#2DD4BF]">Batch MS-2026-LOT4 • Majun Suranjan (Mudabbar)</span>
              <p className="text-[#94A3B8]">Available: 450g • Expiry: 2027-08-30 (Allocated first according to FEFO algorithm)</p>
            </div>
            <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-1">
              <span className="font-bold text-[#2DD4BF]">Batch RB-2026-LOT1 • Raughan-e-Balsan</span>
              <p className="text-[#94A3B8]">Available: 320ml • Expiry: 2028-01-15</p>
            </div>
          </div>
        )}

        {/* TAB 3: MUDABBAR GATE */}
        {activeTab === "mudabbar" && (
          <div className="zv-card p-5 space-y-4 text-xs">
            <div className="flex justify-between items-center border-b border-[#334155] pb-3">
              <div>
                <h3 className="text-sm font-bold text-white">Schedule E(1) Botanical Detoxification (Mudabbar) Gate</h3>
                <span className="text-[#94A3B8]">Statutory compliance under Drugs and Cosmetics Act (Ayush Rule 170)</span>
              </div>
              <StatusBadge status="Gate Active" variant="verified" />
            </div>
            <p className="text-[#F8FAFC]">
              Any compound formulated with crude poisonous botanicals (Colchicum / Strychnos) requires an authenticated laboratory purification certificate before release.
            </p>
            <div className="p-4 bg-[#0A0F1D] rounded-lg border border-[#10B981]/40 space-y-2">
              <span className="font-bold text-[#34D399]">Certificate: MUD-CERT-SHA256-VALIDATED</span>
              <p className="text-[#94A3B8]">
                Batch: MS-2026-LOT4 • Detoxification Method: Shodhan / Mudabbar in Cow's Milk & Almond Oil (classical Bayaz-e-Kabir protocol) • Residual Toxicity: &lt;0.01%
              </p>
            </div>
          </div>
        )}

        {/* ============================================================= */}
        {/* 12-STEP DISPENSING VERIFICATION MODAL */}
        {/* ============================================================= */}
        {isVerifying && selectedOrder && (
          <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="zv-card w-full max-w-xl p-5 space-y-4 max-h-[90vh] overflow-y-auto border-[#0D9488]">
              <div className="flex items-center justify-between border-b border-[#334155] pb-3">
                <div>
                  <h3 className="text-sm font-bold text-white">12-Step Pharmacist Dispensing Verification</h3>
                  <span className="text-[11px] text-[#94A3B8]">Rx: {selectedOrder.orderNumber} • Patient: {selectedOrder.patientName}</span>
                </div>
                <button onClick={() => setIsVerifying(false)} className="text-[#94A3B8] hover:text-white">✕</button>
              </div>

              <div className="space-y-2 text-xs">
                {[
                  { key: "step1_auth_rx", label: "1. Receive & verify authorized prescription" },
                  { key: "step2_patient_id", label: "2. Confirm patient identity & MRN match" },
                  { key: "step3_rx_content", label: "3. Verify prescription signature & 21 CFR Part 11 hash" },
                  { key: "step4_medicine_match", label: "4. Cross-check medicine formulation & dosage" },
                  { key: "step5_batch_fefo", label: "5. Verify FEFO batch allocation priority" },
                  { key: "step6_expiry_valid", label: "6. Check physical batch expiration date" },
                  { key: "step7_stock_sufficient", label: "7. Verify dispensary shelf stock availability" },
                  { key: "step8_mudabbar_gate", label: "8. Schedule E(1) Mudabbar Certificate Verified" },
                  { key: "step9_pharmacist_auth", label: "9. Pharmacist license authorization & pin" },
                  { key: "step10_merkle_record", label: "10. Anchor dispense leaf into Merkle ledger" },
                  { key: "step11_patient_posology", label: "11. Print vernacular posology instructions" },
                  { key: "step12_inventory_decrement", label: "12. Atomically decrement inventory count" },
                ].map((step) => (
                  <label key={step.key} className="flex items-center gap-2 p-2 rounded bg-[#0A0F1D] border border-[#334155] cursor-pointer">
                    <input
                      type="checkbox"
                      checked={checklist[step.key as keyof typeof checklist]}
                      onChange={(e) => setChecklist({ ...checklist, [step.key]: e.target.checked })}
                      className="accent-[#0D9488]"
                    />
                    <span className="text-white font-medium">{step.label}</span>
                  </label>
                ))}
              </div>

              <div className="flex justify-end gap-2 pt-2 border-t border-[#334155]">
                <button onClick={() => setIsVerifying(false)} className="zv-btn-secondary text-xs">
                  Cancel
                </button>
                <button
                  onClick={handleConfirmDispense}
                  disabled={!Object.values(checklist).every(Boolean)}
                  className="zv-btn-primary text-xs bg-[#0D9488]"
                >
                  Confirm & Dispense Medication
                </button>
              </div>
            </div>
          </div>
        )}

      </div>
    </AppShell>
  );
}
