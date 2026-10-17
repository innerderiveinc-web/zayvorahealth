"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";

interface Invoice {
  id: string;
  invoiceNo: string;
  patientName: string;
  mrn: string;
  service: string;
  amount: number;
  mode: "UPI" | "Cash" | "Card" | "ABDM Insurance";
  status: "PAID" | "PENDING" | "REFUNDED";
  date: string;
  gstAmount: number;
}

const INITIAL_INVOICES: Invoice[] = [
  {
    id: "inv-1",
    invoiceNo: "INV-2026-8801",
    patientName: "Hamza Farooqi",
    mrn: "MRN-2026-0814",
    service: "OPD Consultation + Mudabbar Nuskha Dispense",
    amount: 1450,
    mode: "UPI",
    status: "PAID",
    date: "Today, 10:45 AM",
    gstAmount: 78,
  },
  {
    id: "inv-2",
    invoiceNo: "INV-2026-8802",
    patientName: "Ayesha Siddiqui",
    mrn: "MRN-2026-0921",
    service: "Telemedicine Video Consultation (Specialist Tabeeb)",
    amount: 800,
    mode: "UPI",
    status: "PAID",
    date: "Today, 11:20 AM",
    gstAmount: 0,
  },
  {
    id: "inv-3",
    invoiceNo: "INV-2026-8803",
    patientName: "Bilal Ahmad",
    mrn: "MRN-2026-0744",
    service: "Hepatic Priming Compound + Comprehensive Metabolic Lab",
    amount: 2850,
    mode: "Card",
    status: "PAID",
    date: "Today, 09:30 AM",
    gstAmount: 180,
  },
  {
    id: "inv-4",
    invoiceNo: "INV-2026-8804",
    patientName: "Fatima Noor",
    mrn: "MRN-2026-1032",
    service: "NeuroCalmX Restorative Formulation (60 Capsules)",
    amount: 1200,
    mode: "Cash",
    status: "PAID",
    date: "Yesterday, 04:15 PM",
    gstAmount: 144,
  },
  {
    id: "inv-5",
    invoiceNo: "INV-2026-8805",
    patientName: "Zubair Khan",
    mrn: "MRN-2026-0612",
    service: "Regimenal Hijama Therapy (Wet Cupping Stage 1)",
    amount: 1500,
    mode: "UPI",
    status: "PENDING",
    date: "Today, 11:50 AM",
    gstAmount: 0,
  },
];

export default function BillingManagementPage() {
  const [invoices, setInvoices] = useState<Invoice[]>(INITIAL_INVOICES);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterStatus, setFilterStatus] = useState<"ALL" | "PAID" | "PENDING">("ALL");
  const [showNewModal, setShowNewModal] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);

  // Form states
  const [patientName, setPatientName] = useState("");
  const [mrn, setMrn] = useState("");
  const [serviceName, setServiceName] = useState("OPD Consultation (Room 3)");
  const [amount, setAmount] = useState("800");
  const [payMode, setPayMode] = useState<"UPI" | "Cash" | "Card">("UPI");

  const handleCreateBill = (e: React.FormEvent) => {
    e.preventDefault();
    if (!patientName.trim()) return;

    const numAmount = parseFloat(amount) || 800;
    const newInv: Invoice = {
      id: "inv-" + Date.now(),
      invoiceNo: `INV-2026-${Math.floor(1000 + Math.random() * 9000)}`,
      patientName: patientName.trim(),
      mrn: mrn.trim() || `MRN-2026-${Math.floor(1000 + Math.random() * 9000)}`,
      service: serviceName,
      amount: numAmount,
      mode: payMode,
      status: "PAID",
      date: "Just now",
      gstAmount: Math.round(numAmount * 0.05),
    };

    setInvoices((prev) => [newInv, ...prev]);
    setShowNewModal(false);
    setPatientName("");
    setMrn("");
    setNotice(`Invoice ${newInv.invoiceNo} issued for ₹${numAmount} and receipt generated.`);
    setTimeout(() => setNotice(null), 3500);
  };

  const handleDownloadReceipt = (invNo: string) => {
    setNotice(`Downloading official GST Tax Invoice & Receipt: ${invNo}...`);
    setTimeout(() => setNotice(null), 3000);
  };

  const filteredInvoices = invoices.filter((inv) => {
    const matchStatus = filterStatus === "ALL" || inv.status === filterStatus;
    const matchSearch =
      inv.patientName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      inv.invoiceNo.toLowerCase().includes(searchQuery.toLowerCase()) ||
      inv.mrn.toLowerCase().includes(searchQuery.toLowerCase()) ||
      inv.service.toLowerCase().includes(searchQuery.toLowerCase());
    return matchStatus && matchSearch;
  });

  const totalCollected = invoices
    .filter((i) => i.status === "PAID")
    .reduce((acc, curr) => acc + curr.amount, 0);

  const pendingAmount = invoices
    .filter((i) => i.status === "PENDING")
    .reduce((acc, curr) => acc + curr.amount, 0);

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-7xl mx-auto">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-4">
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
              <span>💳</span> Billing, Payments & Accounts Management
              <span className="px-2 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold">
                GST Ready
              </span>
            </h1>
            <p className="text-xs text-[var(--muted)] mt-1">
              OPD consultation ticketing, dispensary botanical sales, regimenal therapy packages, and GST invoices.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <button
              onClick={() => setShowNewModal(true)}
              className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition flex items-center gap-1.5 shadow-sm"
            >
              <span>+ Create Bill / Receipt</span>
            </button>
          </div>
        </div>

        {notice && (
          <div className="p-3 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs flex items-center justify-between animate-fadeIn">
            <span>✓ {notice}</span>
            <button onClick={() => setNotice(null)} className="text-slate-400 hover:text-white">✕</button>
          </div>
        )}

        {/* 4 KPI Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-1">
            <span className="text-[11px] text-[var(--muted)] block font-medium">Total Collections Today</span>
            <div className="text-2xl font-mono font-extrabold text-white">₹{totalCollected.toLocaleString()}</div>
            <span className="text-[10px] text-emerald-400 font-medium">↑ +18.2% vs 7-day average</span>
          </div>

          <div className="p-4 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-1">
            <span className="text-[11px] text-[var(--muted)] block font-medium">Pending Uncollected Dues</span>
            <div className="text-2xl font-mono font-extrabold text-amber-400">₹{pendingAmount.toLocaleString()}</div>
            <span className="text-[10px] text-slate-400">1 patient awaiting dispensary checkout</span>
          </div>

          <div className="p-4 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-1">
            <span className="text-[11px] text-[var(--muted)] block font-medium">Dispensary Herbal Volume</span>
            <div className="text-2xl font-mono font-extrabold text-teal-300">₹38,400</div>
            <span className="text-[10px] text-teal-400">Mudabbar formulations & Arqiyat</span>
          </div>

          <div className="p-4 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-1">
            <span className="text-[11px] text-[var(--muted)] block font-medium">Payment Gateway Health</span>
            <div className="text-sm font-bold text-emerald-400 flex items-center gap-1.5 pt-1">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              Razorpay UPI & Cards Active
            </div>
            <span className="text-[10px] text-[var(--muted)]">99.98% uptime · Instant settlement</span>
          </div>
        </div>

        {/* Filter Bar */}
        <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
          <div className="flex items-center gap-1.5 p-1 bg-[var(--panel)] border border-[var(--border)] rounded-2xl text-xs">
            {(["ALL", "PAID", "PENDING"] as const).map((st) => (
              <button
                key={st}
                onClick={() => setFilterStatus(st)}
                className={`px-3 py-1.5 rounded-xl font-medium transition ${
                  filterStatus === st
                    ? "bg-teal-600 text-white font-semibold shadow-xs"
                    : "text-[var(--muted)] hover:text-white"
                }`}
              >
                {st === "ALL" ? "All Invoices" : st}
              </button>
            ))}
          </div>

          <div className="w-full sm:w-72">
            <input
              type="text"
              placeholder="Search invoice #, patient, MRN..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-[var(--panel)] border border-[var(--border)] rounded-xl px-3.5 py-2 text-xs text-white placeholder-[var(--muted)] focus:outline-none focus:border-teal-500"
            />
          </div>
        </div>

        {/* Invoices Table */}
        <div className="rounded-2xl bg-[var(--panel)] border border-[var(--border)] overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-[var(--border)] bg-[var(--background)] text-[var(--muted)] font-semibold text-[11px]">
                  <th className="p-3.5 pl-4">Invoice #</th>
                  <th className="p-3.5">Date / Time</th>
                  <th className="p-3.5">Patient Details</th>
                  <th className="p-3.5">Service Description</th>
                  <th className="p-3.5">Mode</th>
                  <th className="p-3.5 text-right">Amount (₹)</th>
                  <th className="p-3.5 text-center">Status</th>
                  <th className="p-3.5 pr-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--border)]">
                {filteredInvoices.map((inv) => (
                  <tr key={inv.id} className="hover:bg-[var(--elevated)]/50 transition">
                    <td className="p-3.5 pl-4 font-mono font-bold text-teal-300">
                      {inv.invoiceNo}
                    </td>
                    <td className="p-3.5 text-[var(--muted)] text-[11px]">
                      {inv.date}
                    </td>
                    <td className="p-3.5">
                      <div className="font-bold text-white">{inv.patientName}</div>
                      <span className="text-[10px] font-mono text-[var(--muted)]">{inv.mrn}</span>
                    </td>
                    <td className="p-3.5 text-slate-300 max-w-xs truncate">
                      {inv.service}
                    </td>
                    <td className="p-3.5">
                      <span className="px-2 py-0.5 rounded-lg bg-[var(--background)] border border-[var(--border)] text-[10px] font-mono text-slate-300">
                        {inv.mode}
                      </span>
                    </td>
                    <td className="p-3.5 text-right font-mono font-bold text-white text-sm">
                      ₹{inv.amount.toLocaleString()}
                    </td>
                    <td className="p-3.5 text-center">
                      <span
                        className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                          inv.status === "PAID"
                            ? "bg-emerald-500/15 text-emerald-400 border-emerald-500/30"
                            : "bg-amber-500/15 text-amber-300 border-amber-500/30"
                        }`}
                      >
                        {inv.status}
                      </span>
                    </td>
                    <td className="p-3.5 pr-4 text-right">
                      <button
                        onClick={() => handleDownloadReceipt(inv.invoiceNo)}
                        className="px-2.5 py-1 rounded-lg bg-[var(--elevated)] hover:bg-[var(--border)] text-teal-300 hover:text-white border border-[var(--border)] text-[11px] font-semibold transition"
                      >
                        Receipt 📥
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Modal: New Invoice Creation */}
        {showNewModal && (
          <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4">
            <div className="bg-[var(--panel)] border border-[var(--border)] rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl text-xs">
              <div className="flex justify-between items-center border-b border-[var(--border)] pb-3">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <span>💳</span> Generate New OPD / Dispensary Invoice
                </h3>
                <button
                  onClick={() => setShowNewModal(false)}
                  className="text-slate-400 hover:text-white text-base"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleCreateBill} className="space-y-3">
                <div>
                  <label className="block text-[var(--muted)] font-semibold mb-1">Patient Full Name</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Hamza Farooqi"
                    value={patientName}
                    onChange={(e) => setPatientName(e.target.value)}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-teal-500"
                  />
                </div>

                <div>
                  <label className="block text-[var(--muted)] font-semibold mb-1">Medical Record Number (MRN)</label>
                  <input
                    type="text"
                    placeholder="MRN-2026-XXXX (Optional)"
                    value={mrn}
                    onChange={(e) => setMrn(e.target.value)}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl px-3 py-2 text-xs text-white font-mono focus:outline-none focus:border-teal-500"
                  />
                </div>

                <div>
                  <label className="block text-[var(--muted)] font-semibold mb-1">Clinical Service</label>
                  <select
                    value={serviceName}
                    onChange={(e) => setServiceName(e.target.value)}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-teal-500 cursor-pointer"
                  >
                    <option value="OPD Consultation (Room 3)">OPD Consultation (Specialist Tabeeb) — ₹800</option>
                    <option value="Telemedicine Virtual Consultation">Telemedicine Virtual Consultation — ₹800</option>
                    <option value="Hijama Regimenal Therapy (Wet Cupping)">Hijama Regimenal Therapy (Wet Cupping) — ₹1,500</option>
                    <option value="Botanical Dispensary Compound">Botanical Dispensary Compound (Mudabbar) — ₹1,450</option>
                    <option value="Full Comprehensive Metabolic Lab Panel">Full Comprehensive Metabolic Lab Panel — ₹2,850</option>
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-[var(--muted)] font-semibold mb-1">Total Fee (₹)</label>
                    <input
                      type="number"
                      required
                      value={amount}
                      onChange={(e) => setAmount(e.target.value)}
                      className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl px-3 py-2 text-xs text-white font-mono focus:outline-none focus:border-teal-500"
                    />
                  </div>
                  <div>
                    <label className="block text-[var(--muted)] font-semibold mb-1">Payment Method</label>
                    <select
                      value={payMode}
                      onChange={(e) => setPayMode(e.target.value as any)}
                      className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-teal-500 cursor-pointer"
                    >
                      <option value="UPI">UPI / QR Code</option>
                      <option value="Cash">Cash (Counter)</option>
                      <option value="Card">Debit / Credit Card</option>
                    </select>
                  </div>
                </div>

                <div className="pt-2 flex gap-2">
                  <button
                    type="button"
                    onClick={() => setShowNewModal(false)}
                    className="flex-1 py-2.5 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-slate-300 font-semibold hover:bg-[var(--border)] transition"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold shadow-sm transition"
                  >
                    Generate & Print Bill
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

      </div>
    </AppShell>
  );
}
