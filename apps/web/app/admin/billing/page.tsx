"use client";

import React, { useState } from "react";

interface Transaction {
  id: string;
  patientName: string;
  type: "OPD Consultation" | "Pharmacy Dispense" | "Regimenal Therapy" | "Enterprise License";
  amount: number;
  status: "Paid" | "Pending" | "Refunded";
  date: string;
  gateway: "Stripe" | "UPI" | "Cash / POS";
}

const INITIAL_TRANSACTIONS: Transaction[] = [
  { id: "TXN-9021", patientName: "Hamza Farooqi", type: "OPD Consultation", amount: 800, status: "Paid", date: "2026-09-14 10:45", gateway: "UPI" },
  { id: "TXN-9022", patientName: "Ayesha Siddiqui", type: "Pharmacy Dispense", amount: 2340, status: "Paid", date: "2026-09-14 11:20", gateway: "Stripe" },
  { id: "TXN-9023", patientName: "Mohammad Zubair", type: "Regimenal Therapy", amount: 1500, status: "Pending", date: "2026-09-14 12:10", gateway: "UPI" },
  { id: "TXN-9024", patientName: "ZAYVORA Hyderabad Matab", type: "Enterprise License", amount: 45000, status: "Paid", date: "2026-09-13 16:30", gateway: "Stripe" },
  { id: "TXN-9025", patientName: "Farhana Begum", type: "Pharmacy Dispense", amount: 1120, status: "Paid", date: "2026-09-13 14:15", gateway: "Cash / POS" }
];

export default function AdminBillingPage() {
  const [txns, setTxns] = useState<Transaction[]>(INITIAL_TRANSACTIONS);
  const [filter, setFilter] = useState("");

  const filtered = txns.filter(t => 
    t.patientName.toLowerCase().includes(filter.toLowerCase()) ||
    t.id.toLowerCase().includes(filter.toLowerCase()) ||
    t.type.toLowerCase().includes(filter.toLowerCase())
  );

  const totalRevenue = txns.filter(t => t.status === "Paid").reduce((acc, curr) => acc + curr.amount, 0);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Financial Management & Billing</h2>
          <p className="text-sm text-gray-500">Real-time OPD revenue, pharmacy transactions, and subscription settlements</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={() => alert("Exporting financial ledger as CSV...")}
            className="px-4 py-2 bg-[#2D6A4F] hover:bg-[#1B4332] text-white rounded-lg text-sm font-semibold transition shadow-sm"
          >
            ⬇ Export Financial Ledger
          </button>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Total Revenue (MTD)</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">₹{totalRevenue.toLocaleString()}</span>
          <span className="text-xs text-emerald-600 font-semibold mt-1 block">↑ 18.4% vs last month</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Pending Settlements</span>
          <span className="text-2xl font-bold text-amber-600 mt-1 block">₹1,500</span>
          <span className="text-xs text-gray-400 mt-1 block">1 transaction awaiting gateway callback</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Active Payment Gateways</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">Stripe & UPI</span>
          <span className="text-xs text-emerald-600 font-semibold mt-1 block">All webhooks operational (200 OK)</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Average Basket Value</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">₹1,740</span>
          <span className="text-xs text-gray-400 mt-1 block">Consultation + FEFO Dispense</span>
        </div>
      </div>

      {/* Transactions Table */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden space-y-4 p-5">
        <div className="flex justify-between items-center">
          <h3 className="font-bold text-gray-800 text-base">Recent Financial Transactions</h3>
          <input
            type="text"
            placeholder="Search transaction or patient..."
            value={filter}
            onChange={e => setFilter(e.target.value)}
            className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#2D6A4F]"
          />
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-gray-50 border-b border-gray-100 text-xs font-semibold text-gray-500 uppercase">
              <tr>
                <th className="px-4 py-3">Txn ID</th>
                <th className="px-4 py-3">Patient / Entity</th>
                <th className="px-4 py-3">Revenue Stream</th>
                <th className="px-4 py-3">Amount</th>
                <th className="px-4 py-3">Gateway</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filtered.map(t => (
                <tr key={t.id} className="hover:bg-gray-50/50">
                  <td className="px-4 py-3 font-mono font-bold text-gray-700">{t.id}</td>
                  <td className="px-4 py-3 font-medium text-gray-800">{t.patientName}</td>
                  <td className="px-4 py-3 text-gray-600">{t.type}</td>
                  <td className="px-4 py-3 font-bold text-gray-900">₹{t.amount.toLocaleString()}</td>
                  <td className="px-4 py-3 text-gray-500">{t.gateway}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                      t.status === "Paid" ? "bg-emerald-50 text-emerald-700 border border-emerald-200" :
                      t.status === "Pending" ? "bg-amber-50 text-amber-700 border border-amber-200" : "bg-rose-50 text-rose-700 border border-rose-200"
                    }`}>
                      {t.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-500 font-mono text-xs">{t.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
