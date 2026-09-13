"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";
import { CANONICAL_PRODUCTS, ProductItem } from "@/lib/cms/productsData";

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
    doctorName: "Prof. (Dr.) Mansoor Alam",
    doctorReg: "CCIM-U-1988-0412",
    items: [
      {
        name: "Majun Suranjan (Mudabbar)",
        dose: "5g twice daily with lukewarm water • 14 days",
        isScheduleE1: true,
        mudabbarRequired: true,
        batchNumber: "MS-2026-LOT4",
        expiryDate: "2027-08-30",
        mudabbarCert: "SHA256:7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b",
      },
      {
        name: "Roghan-e-Balsan",
        dose: "Local gentle application nocte • 14 days",
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
    patientName: "Ayesha Siddiqui",
    mrn: "MRN-2026-0815",
    doctorName: "Dr. Aisha Siddiqui",
    doctorReg: "CCIM-U-2004-1892",
    items: [
      {
        name: "Jawarish Shahi",
        dose: "5g post-prandial • 10 days",
        isScheduleE1: false,
        mudabbarRequired: false,
        batchNumber: "JS-2026-LOT9",
        expiryDate: "2027-12-01",
        mudabbarCert: null,
      },
      {
        name: "Sharbat Bazoori Motadil",
        dose: "20ml with warm water morning • 15 days",
        isScheduleE1: false,
        mudabbarRequired: false,
        batchNumber: "SB-2026-LOT3",
        expiryDate: "2028-03-20",
        mudabbarCert: null,
      }
    ],
    signatureHash: "8f4b29c91a03e147b2c9d01248a0f9b3e217c49b01538a7c29b0134f59c14820",
    status: "PENDING_VERIFICATION",
  },
];

interface InventoryBatch {
  id: string;
  name: string;
  category: "CLINIC_UNANI" | "RETAIL_UNANI" | "AYUSH_PROPRIETARY" | "FSSAI_SUPPLEMENT";
  batchNumber: string;
  expiryDate: string;
  stockQty: number;
  minThreshold: number;
  isScheduleE1: boolean;
  mudabbarStatus: "CERTIFIED" | "NOT_APPLICABLE";
  storage: "Ambient Dry" | "Cold-Chain (15-25°C)" | "Refrigerated (2-8°C)";
}

const INVENTORY_ITEMS: InventoryBatch[] = [
  // 1. Clinic-Prescribed Formulations
  { id: "INV-01", name: "Majun Suranjan (Mudabbar)", category: "CLINIC_UNANI", batchNumber: "MS-2026-LOT4", expiryDate: "2027-08-30", stockQty: 29, minThreshold: 50, isScheduleE1: true, mudabbarStatus: "CERTIFIED", storage: "Cold-Chain (15-25°C)" },
  { id: "INV-02", name: "Safoof-e-Mubarrid", category: "CLINIC_UNANI", batchNumber: "SM-2026-LOT2", expiryDate: "2027-11-15", stockQty: 85, minThreshold: 30, isScheduleE1: false, mudabbarStatus: "NOT_APPLICABLE", storage: "Ambient Dry" },
  { id: "INV-03", name: "Habb-e-Suranjan Forte", category: "CLINIC_UNANI", batchNumber: "HSF-2026-LOT1", expiryDate: "2027-06-30", stockQty: 42, minThreshold: 40, isScheduleE1: true, mudabbarStatus: "CERTIFIED", storage: "Cold-Chain (15-25°C)" },
  
  // 2. Classical Retail Formulations
  { id: "INV-04", name: "Roghan-e-Balsan", category: "RETAIL_UNANI", batchNumber: "RB-2026-LOT1", expiryDate: "2028-01-15", stockQty: 120, minThreshold: 40, isScheduleE1: false, mudabbarStatus: "NOT_APPLICABLE", storage: "Ambient Dry" },
  { id: "INV-05", name: "Sharbat Bazoori Motadil", category: "RETAIL_UNANI", batchNumber: "SB-2026-LOT3", expiryDate: "2028-03-20", stockQty: 160, minThreshold: 50, isScheduleE1: false, mudabbarStatus: "NOT_APPLICABLE", storage: "Ambient Dry" },
  { id: "INV-06", name: "Khamira Gaozaban Ambari", category: "RETAIL_UNANI", batchNumber: "KG-2026-LOT5", expiryDate: "2027-09-10", stockQty: 74, minThreshold: 30, isScheduleE1: false, mudabbarStatus: "NOT_APPLICABLE", storage: "Ambient Dry" },

  // 3. AYUSH Proprietary Formulations
  { id: "INV-07", name: "Arthronix Joint Ease", category: "AYUSH_PROPRIETARY", batchNumber: "ARTH-2026-LOT8", expiryDate: "2028-02-28", stockQty: 195, minThreshold: 60, isScheduleE1: false, mudabbarStatus: "NOT_APPLICABLE", storage: "Ambient Dry" },
  { id: "INV-08", name: "MetaboCore Elite", category: "AYUSH_PROPRIETARY", batchNumber: "MCE-2026-LOT2", expiryDate: "2027-10-15", stockQty: 110, minThreshold: 40, isScheduleE1: false, mudabbarStatus: "NOT_APPLICABLE", storage: "Ambient Dry" },

  // 4. FSSAI Dietary Supplements
  { id: "INV-09", name: "ManiVital Pro", category: "FSSAI_SUPPLEMENT", batchNumber: "MVP-2026-LOT4", expiryDate: "2028-04-10", stockQty: 142, minThreshold: 50, isScheduleE1: false, mudabbarStatus: "NOT_APPLICABLE", storage: "Ambient Dry" },
  { id: "INV-10", name: "Pure Himalayan Shilajit Gold", category: "FSSAI_SUPPLEMENT", batchNumber: "SHIL-2026-LOT1", expiryDate: "2028-06-01", stockQty: 88, minThreshold: 35, isScheduleE1: false, mudabbarStatus: "NOT_APPLICABLE", storage: "Ambient Dry" },
];

export default function PharmacyWorkspacePage() {
  const [activeTab, setActiveTab] = useState<"queue" | "inventory" | "orders" | "search">("queue");
  const [regulatoryFilter, setRegulatoryFilter] = useState<"ALL" | "CLINIC_UNANI" | "RETAIL_UNANI" | "AYUSH_PROPRIETARY" | "FSSAI_SUPPLEMENT">("ALL");
  const [orders, setOrders] = useState<PrescriptionOrder[]>(INITIAL_ORDERS);
  const [selectedOrder, setSelectedOrder] = useState<PrescriptionOrder | null>(null);
  const [inventory] = useState<InventoryBatch[]>(INVENTORY_ITEMS);
  const [searchQuery, setSearchQuery] = useState("");

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
      step9_pharmacist_auth: true,
      step10_merkle_record: true,
      step11_patient_posology: true,
      step12_inventory_decrement: true,
    });
    setIsVerifying(true);
  };

  const handleConfirmDispense = () => {
    if (!selectedOrder) return;
    setOrders(orders.map(o => o.id === selectedOrder.id ? { ...o, status: "DISPENSED" } : o));
    setIsVerifying(false);
    setSelectedOrder(null);
  };

  // Filtered inventory items
  const filteredInventory = inventory.filter(item => {
    const matchesReg = regulatoryFilter === "ALL" || item.category === regulatoryFilter;
    const matchesSearch = searchQuery === "" ||
      item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.batchNumber.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesReg && matchesSearch;
  });

  return (
    <AppShell activeRole="pharmacy">
      <div className="space-y-6 max-w-7xl mx-auto pb-12 text-slate-100 text-xs">
        
        {/* Pharmacy Workspace Header */}
        <div className="p-6 rounded-3xl bg-gradient-to-r from-[#0C1524] via-[#101C30] to-[#152540] border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xl">💊</span>
              <span className="text-[11px] font-bold text-teal-400 uppercase tracking-widest bg-teal-950/80 px-3 py-1 rounded-full border border-teal-800/80">
                Central Dispensary Operations
              </span>
              <span className="text-xs text-slate-400 font-mono">• Chief Pharmacist: Zainab Ali (PB-PHARM-2015-8812)</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mt-1">
              Clinical Pharmacy & Regulatory Inventory OS
            </h1>
            <p className="text-slate-400 text-xs">
              Strict 4-tier regulatory categorization, FEFO batch allocation, Schedule E(1) Mudabbar verification, and 12-step dispense checklists.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <span className="px-3 py-1.5 rounded-xl bg-teal-950/80 border border-teal-500/50 text-teal-300 text-xs font-bold flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
              <span>Mudabbar Safety Gate: ACTIVE</span>
            </span>
          </div>
        </div>

        {/* Executive Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <StatCard label="Pending Prescriptions" value={orders.filter(o => o.status === "PENDING_VERIFICATION").length} subtext="Awaiting verification" variant="amber" icon="⏳" />
          <StatCard label="Dispensed Today" value={orders.filter(o => o.status === "DISPENSED").length + 18} subtext="100% FEFO allocated" variant="emerald" icon="✓" />
          <StatCard label="Schedule E(1) Lots" value="2 Batches" subtext="Mudabbar verified" variant="teal" icon="🛡️" />
          <StatCard label="Cold-Chain Stability" value="19.4°C" subtext="Safe storage margin" variant="teal" icon="❄️" />
        </div>

        {/* Tab Navigation */}
        <div className="border-b border-slate-800 flex gap-2">
          {[
            { id: "queue", label: "Prescription Dispensing Queue", icon: "📋" },
            { id: "inventory", label: "4-Tier Regulatory Inventory", icon: "📦" },
            { id: "orders", label: "Purchase Orders & Restock", icon: "🚚" },
            { id: "search", label: "Medicine Search & History", icon: "🔍" },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold rounded-xl transition ${
                activeTab === tab.id
                  ? "bg-teal-950/80 text-teal-300 border border-teal-600/50 shadow-sm"
                  : "text-slate-400 hover:text-white hover:bg-slate-800/40"
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* TAB 1: DISPENSING QUEUE */}
        {activeTab === "queue" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in">
            <div className="border-b border-slate-800 pb-3 flex justify-between items-center">
              <div>
                <h3 className="text-sm font-bold text-white">Active Electronic Prescriptions</h3>
                <p className="text-slate-400 text-[11px]">21 CFR Part 11 signed by attending clinicians, awaiting dispensing verification.</p>
              </div>
              <span className="text-amber-400 font-semibold">{orders.filter(o => o.status === "PENDING_VERIFICATION").length} Orders Awaiting Action</span>
            </div>

            <div className="space-y-4">
              {orders.map(order => (
                <div key={order.id} className="p-5 bg-slate-900/90 rounded-2xl border border-slate-800 space-y-3">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-teal-400 font-bold">{order.orderNumber}</span>
                        <span className="text-slate-600">•</span>
                        <span className="font-bold text-white">{order.patientName}</span>
                        <span className="text-slate-400 font-mono">({order.mrn})</span>
                      </div>
                      <p className="text-slate-400 text-[11px]">Prescribed by {order.doctorName} • {order.doctorReg}</p>
                    </div>
                    <StatusBadge
                      status={order.status === "DISPENSED" ? "Dispensed & Closed" : "Pending Verification"}
                      variant={order.status === "DISPENSED" ? "verified" : "warning"}
                    />
                  </div>

                  <div className="space-y-2">
                    <span className="text-slate-400 font-semibold uppercase text-[10px] block">Prescribed Medicines & Safety Gates:</span>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {order.items.map((item, idx) => (
                        <div key={idx} className="p-3 bg-slate-950/80 rounded-xl border border-slate-800 flex justify-between items-start">
                          <div>
                            <div className="font-bold text-white">{item.name}</div>
                            <div className="text-[11px] text-slate-400">{item.dose}</div>
                            <div className="text-[10px] text-slate-500 font-mono mt-1">Batch: {item.batchNumber} • Exp: {item.expiryDate}</div>
                          </div>
                          {item.isScheduleE1 && (
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-950 text-amber-300 border border-amber-800">
                              Schedule E(1) Mudabbar
                            </span>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="flex justify-between items-center pt-2 border-t border-slate-800">
                    <div className="font-mono text-[10px] text-slate-500 truncate max-w-sm">
                      Doctor Signature Hash: {order.signatureHash}
                    </div>
                    {order.status === "PENDING_VERIFICATION" ? (
                      <button
                        onClick={() => handleStartDispense(order)}
                        className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition shadow-md"
                      >
                        Start 12-Step Dispensing Verification →
                      </button>
                    ) : (
                      <button
                        onClick={() => alert(`Printing Dispense Certificate & Posology Labels for ${order.orderNumber}`)}
                        className="px-4 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-teal-300 font-semibold border border-slate-700"
                      >
                        Print Dispense Labels 🏷️
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 2: 4-TIER REGULATORY INVENTORY */}
        {activeTab === "inventory" && (
          <div className="space-y-4 animate-fade-in">
            
            {/* Regulatory Filter Pills */}
            <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex items-center gap-1.5 flex-wrap">
                <span className="text-slate-400 font-semibold mr-1">Regulatory Category:</span>
                {[
                  { id: "ALL", label: "All Formulations" },
                  { id: "CLINIC_UNANI", label: "1. Clinic-Prescribed Unani" },
                  { id: "RETAIL_UNANI", label: "2. Classical Retail Unani" },
                  { id: "AYUSH_PROPRIETARY", label: "3. AYUSH Proprietary" },
                  { id: "FSSAI_SUPPLEMENT", label: "4. FSSAI Supplements" },
                ].map(cat => (
                  <button
                    key={cat.id}
                    onClick={() => setRegulatoryFilter(cat.id as any)}
                    className={`px-3 py-1.5 rounded-xl font-semibold transition text-[11px] ${
                      regulatoryFilter === cat.id
                        ? "bg-teal-600 text-white shadow-sm"
                        : "bg-slate-800 text-slate-400 hover:text-white"
                    }`}
                  >
                    {cat.label}
                  </button>
                ))}
              </div>

              <div className="flex items-center gap-2 max-w-xs w-full bg-slate-950 p-2 rounded-xl border border-slate-800">
                <span>🔍</span>
                <input
                  type="text"
                  placeholder="Search batch or formulation..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-transparent text-white focus:outline-none text-xs"
                />
              </div>
            </div>

            {/* Regulatory Notice */}
            <div className="p-3.5 rounded-2xl bg-teal-950/40 border border-teal-800/60 text-teal-300 text-[11px] leading-relaxed">
              <strong>Regulatory Integrity Guarantee:</strong> Categories are strictly compartmentalized under AYUSH Rule 158B and Drugs & Cosmetics Act, 1940. Clinic-Prescribed formulations require verified clinician digital signatures before FEFO allocation.
            </div>

            {/* Inventory Table */}
            <div className="bg-[#0F172A] border border-slate-800 rounded-3xl overflow-hidden shadow-lg">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-slate-900/90 border-b border-slate-800 text-slate-400 font-semibold text-[11px]">
                      <th className="p-4">Formulation Name</th>
                      <th className="p-4">Regulatory Category</th>
                      <th className="p-4">Batch Lot & Expiry</th>
                      <th className="p-4">Stock Qty</th>
                      <th className="p-4">Storage Spec</th>
                      <th className="p-4">Safety Status</th>
                      <th className="p-4 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 text-slate-200">
                    {filteredInventory.map(item => (
                      <tr key={item.id} className="hover:bg-slate-800/30 transition">
                        <td className="p-4">
                          <div className="font-bold text-white text-xs">{item.name}</div>
                          <span className="text-[10px] text-slate-500 font-mono">{item.id}</span>
                        </td>
                        <td className="p-4">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            item.category === "CLINIC_UNANI"
                              ? "bg-purple-950 text-purple-300 border border-purple-800"
                              : item.category === "RETAIL_UNANI"
                              ? "bg-teal-950 text-teal-300 border border-teal-800"
                              : item.category === "AYUSH_PROPRIETARY"
                              ? "bg-blue-950 text-blue-300 border border-blue-800"
                              : "bg-emerald-950 text-emerald-300 border border-emerald-800"
                          }`}>
                            {item.category.replace("_", " ")}
                          </span>
                        </td>
                        <td className="p-4">
                          <div className="font-mono text-white text-[11px]">{item.batchNumber}</div>
                          <div className="text-[10px] text-slate-400">Exp: {item.expiryDate}</div>
                        </td>
                        <td className="p-4">
                          <span className={`font-mono font-bold ${item.stockQty <= item.minThreshold ? "text-amber-400" : "text-white"}`}>
                            {item.stockQty} Units
                          </span>
                          {item.stockQty <= item.minThreshold && (
                            <span className="block text-[9px] text-amber-400 font-semibold">Low Stock</span>
                          )}
                        </td>
                        <td className="p-4 text-slate-300">
                          {item.storage}
                        </td>
                        <td className="p-4">
                          {item.isScheduleE1 ? (
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950 text-emerald-300 border border-emerald-800">
                              ✓ Mudabbar Certified
                            </span>
                          ) : (
                            <span className="text-slate-500 text-[11px]">Standard Non-E(1)</span>
                          )}
                        </td>
                        <td className="p-4 text-right">
                          <button
                            onClick={() => alert(`Creating Purchase Reorder for ${item.name} (${item.batchNumber})`)}
                            className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-teal-300 text-[11px] border border-slate-700 font-medium"
                          >
                            + Reorder
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: PURCHASE ORDERS & RESTOCK */}
        {activeTab === "orders" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in">
            <div className="border-b border-slate-800 pb-3 flex justify-between items-center">
              <div>
                <h3 className="text-sm font-bold text-white">Botanical Purchase Orders & Restock Pipeline</h3>
                <p className="text-slate-400 text-[11px]">Procurement from Jamia Hamdard Certified AYUSH-GMP Botanical Pharmacy Facility.</p>
              </div>
              <button onClick={() => alert("Creating new purchase order...")} className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold">
                + New Purchase Order
              </button>
            </div>

            <div className="space-y-3">
              {[
                { po: "PO-2026-081", item: "Suranjan Talkh Raw Botanical Extract (Mudabbar Grade)", qty: "50 kg", supplier: "Hamdard Laboratories GMP Unit", status: "In Transit", arrival: "Sep 15" },
                { po: "PO-2026-080", item: "Balsamodendron Mukul Purified Gum Resin (Guggulu)", qty: "25 kg", supplier: "AUTC Central Processing Facility", status: "Received & QA Cleared", arrival: "Sep 11" }
              ].map((po, idx) => (
                <div key={idx} className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 flex justify-between items-center">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-teal-400 font-bold">{po.po}</span>
                      <span className="text-slate-600">•</span>
                      <span className="font-bold text-white">{po.item}</span>
                    </div>
                    <p className="text-slate-400 text-[11px]">Supplier: {po.supplier} • Quantity: {po.qty}</p>
                  </div>
                  <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2.5 py-1 rounded-full text-[10px] font-bold">
                    {po.status} (ETA {po.arrival})
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 4: MEDICINE SEARCH & HISTORY */}
        {activeTab === "search" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in">
            <div className="border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">Patient Medication Dispensation History</h3>
              <p className="text-slate-400 text-[11px]">Lookup past dispensations by MRN to ensure no duplicate or cross-reacting botanicals.</p>
            </div>

            <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-2">
              <div className="flex justify-between items-center">
                <span className="font-bold text-white">Hamza Farooqi (MRN-2026-0814)</span>
                <span className="text-slate-400 font-mono">Last Dispense: Sep 02, 2026</span>
              </div>
              <p className="text-slate-300 text-[11px]">
                Dispensed: Majun Suranjan (180g, Lot MS-2026-LOT4) + Roghan-e-Balsan (100ml). Adherence compliance reported at 85%.
              </p>
            </div>
          </div>
        )}

        {/* 12-STEP DISPENSING VERIFICATION MODAL */}
        {isVerifying && selectedOrder && (
          <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-[#0F172A] border border-slate-700 rounded-3xl p-6 max-w-xl w-full space-y-4 shadow-2xl">
              <div className="flex justify-between items-center border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <span className="text-teal-400 text-base">🛡️</span>
                  <h3 className="text-sm font-bold text-white">12-Step Pharmacist Dispensing Verification Gate</h3>
                </div>
                <button onClick={() => setIsVerifying(false)} className="text-slate-400 hover:text-white text-lg">✕</button>
              </div>

              <div className="space-y-2 bg-slate-900/80 p-3.5 rounded-2xl border border-slate-800">
                <div className="font-bold text-white">{selectedOrder.orderNumber} — {selectedOrder.patientName}</div>
                <div className="text-[11px] text-slate-400">Prescribed by {selectedOrder.doctorName}</div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px]">
                {[
                  { key: "step1_auth_rx", label: "1. Authentic Prescription" },
                  { key: "step2_patient_id", label: "2. Patient MRN Verified" },
                  { key: "step3_rx_content", label: "3. Drug Strength Checked" },
                  { key: "step4_medicine_match", label: "4. Botanical Formula Match" },
                  { key: "step5_batch_fefo", label: "5. FEFO Batch Allocated" },
                  { key: "step6_expiry_valid", label: "6. Expiry Margin > 180d" },
                  { key: "step7_stock_sufficient", label: "7. Stock Qty Confirmed" },
                  { key: "step8_mudabbar_gate", label: "8. Mudabbar Cert Valid" },
                  { key: "step9_pharmacist_auth", label: "9. Pharmacist Signature" },
                  { key: "step10_merkle_record", label: "10. Merkle Leaf Hashed" },
                  { key: "step11_patient_posology", label: "11. Vernacular Posology" },
                  { key: "step12_inventory_decrement", label: "12. Inventory Deducted" },
                ].map((s) => (
                  <label key={s.key} className="flex items-center gap-2 p-2 bg-slate-950 rounded-xl border border-slate-800/80 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={(checklist as any)[s.key]}
                      onChange={(e) => setChecklist({ ...checklist, [s.key]: e.target.checked })}
                      className="rounded border-slate-700 text-teal-600 focus:ring-teal-500 h-4 w-4"
                    />
                    <span className="text-slate-200">{s.label}</span>
                  </label>
                ))}
              </div>

              <div className="flex gap-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsVerifying(false)}
                  className="flex-1 py-2.5 rounded-xl bg-slate-800 text-slate-300 font-semibold hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleConfirmDispense}
                  className="flex-1 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold"
                >
                  Confirm & Seal Dispense ✓
                </button>
              </div>
            </div>
          </div>
        )}

      </div>
    </AppShell>
  );
}
