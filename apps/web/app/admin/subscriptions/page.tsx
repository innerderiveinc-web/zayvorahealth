"use client";

import React from "react";

export default function AdminSubscriptionsPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Enterprise Licensure & Facility Quotas</h2>
          <p className="text-sm text-gray-500">Multi-facility clinical seats, hospital tiers, and API subscription allocations</p>
        </div>
        <button 
          onClick={() => alert("Licensing wizard opened for new hospital onboarding.")}
          className="px-4 py-2 bg-[#2D6A4F] hover:bg-[#1B4332] text-white text-sm font-semibold rounded-lg shadow-sm transition"
        >
          + Issue New License
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Active Hospital Facilities</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">4 Complexes</span>
          <span className="text-xs text-emerald-600 font-semibold mt-1 block">Delhi, Hyderabad, Bengaluru, Srinagar</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Clinician Seats Licensed</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">48 / 60 Seats</span>
          <span className="text-xs text-gray-400 mt-1 block">12 seats available for faculty expansion</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">License Model</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">Enterprise Hospital</span>
          <span className="text-xs text-emerald-600 font-semibold mt-1 block">Includes 21 CFR 11 & ABDM Gateway</span>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 space-y-4">
        <h3 className="font-bold text-gray-800 text-base">Registered Facility Licenses</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-gray-50 border-b border-gray-100 text-xs font-semibold text-gray-500 uppercase">
              <tr>
                <th className="px-4 py-3">Facility ID</th>
                <th className="px-4 py-3">Hospital / Matab Name</th>
                <th className="px-4 py-3">Location</th>
                <th className="px-4 py-3">Clinician Seats</th>
                <th className="px-4 py-3">Tier</th>
                <th className="px-4 py-3">Renewal Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              <tr className="hover:bg-gray-50/50">
                <td className="px-4 py-3 font-mono font-bold text-gray-700">FAC-HQ-01</td>
                <td className="px-4 py-3 font-semibold text-gray-800">ZAYVORA Healthcare System - Central Hospital</td>
                <td className="px-4 py-3 text-gray-600">New Delhi Institutional Area</td>
                <td className="px-4 py-3 font-medium text-gray-900">24 Seats</td>
                <td className="px-4 py-3"><span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 font-bold text-xs">Enterprise Flagship</span></td>
                <td className="px-4 py-3 text-gray-500 font-mono text-xs">2027-09-30</td>
              </tr>
              <tr className="hover:bg-gray-50/50">
                <td className="px-4 py-3 font-mono font-bold text-gray-700">FAC-HYD-02</td>
                <td className="px-4 py-3 font-semibold text-gray-800">ZAYVORA Matab™ Specialized Regional Center</td>
                <td className="px-4 py-3 text-gray-600">Hyderabad Charminar Heritage Area</td>
                <td className="px-4 py-3 font-medium text-gray-900">12 Seats</td>
                <td className="px-4 py-3"><span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-bold text-xs">Clinical Matab</span></td>
                <td className="px-4 py-3 text-gray-500 font-mono text-xs">2027-08-15</td>
              </tr>
              <tr className="hover:bg-gray-50/50">
                <td className="px-4 py-3 font-mono font-bold text-gray-700">FAC-BLR-03</td>
                <td className="px-4 py-3 font-semibold text-gray-800">ZAYVORA Integrative Care Center</td>
                <td className="px-4 py-3 text-gray-600">Bengaluru Koramangala Medical Hub</td>
                <td className="px-4 py-3 font-medium text-gray-900">8 Seats</td>
                <td className="px-4 py-3"><span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-bold text-xs">Clinical Matab</span></td>
                <td className="px-4 py-3 text-gray-500 font-mono text-xs">2027-07-01</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
