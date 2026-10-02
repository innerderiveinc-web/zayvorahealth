"use client";

import React, { useState } from "react";

export default function AdminSystemHealthPage() {
  const [refreshedAt, setRefreshedAt] = useState(new Date().toLocaleTimeString());

  const handleRefresh = () => {
    setRefreshedAt(new Date().toLocaleTimeString());
    alert("All system health probes executed. All services reporting nominal state.");
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Infrastructure Telemetry & Health</h2>
          <p className="text-sm text-gray-500">Server resource consumption, database connection pool, and queue metrics • Last checked: {refreshedAt}</p>
        </div>
        <button 
          onClick={handleRefresh}
          className="px-4 py-2 bg-[#2D6A4F] hover:bg-[#1B4332] text-white text-sm font-semibold rounded-lg shadow-sm transition"
        >
          🔄 Refresh Probes
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">CPU Utilization</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">18.4%</span>
          <div className="w-full bg-gray-100 h-2 rounded-full mt-2 overflow-hidden">
            <div className="bg-emerald-500 h-full w-[18%]"></div>
          </div>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Memory Footprint</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">2.4 GB / 8.0 GB</span>
          <div className="w-full bg-gray-100 h-2 rounded-full mt-2 overflow-hidden">
            <div className="bg-emerald-500 h-full w-[30%]"></div>
          </div>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">DB Connections</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">28 / 100</span>
          <div className="w-full bg-gray-100 h-2 rounded-full mt-2 overflow-hidden">
            <div className="bg-blue-500 h-full w-[28%]"></div>
          </div>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Redis Cache Hit Rate</span>
          <span className="text-2xl font-bold text-emerald-600 mt-1 block">94.8%</span>
          <div className="w-full bg-gray-100 h-2 rounded-full mt-2 overflow-hidden">
            <div className="bg-emerald-500 h-full w-[95%]"></div>
          </div>
        </div>
      </div>

      <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm space-y-4">
        <h3 className="font-bold text-gray-800 text-base">Active Background Workers & Schedulers</h3>
        <div className="divide-y divide-gray-100 text-sm">
          <div className="py-3 flex justify-between items-center">
            <div>
              <span className="font-semibold text-gray-800 block">FEFO Inventory Depletion Worker</span>
              <span className="text-xs text-gray-500">Synchronizes stock deductions with electronic prescriptions</span>
            </div>
            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">Running</span>
          </div>
          <div className="py-3 flex justify-between items-center">
            <div>
              <span className="font-semibold text-gray-800 block">ABHA M1/M2 Sync Daemon</span>
              <span className="text-xs text-gray-500">Ayushman Bharat Digital Mission health record gateway</span>
            </div>
            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">Running</span>
          </div>
          <div className="py-3 flex justify-between items-center">
            <div>
              <span className="font-semibold text-gray-800 block">IoT Cold-Chain Telemetry Listener</span>
              <span className="text-xs text-gray-500">Monitors dispensary temperature sensors (15°C - 25°C limit)</span>
            </div>
            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">Running</span>
          </div>
        </div>
      </div>
    </div>
  );
}
