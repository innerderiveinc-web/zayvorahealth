"use client";

import React from "react";

export default function AdminCompliancePage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-gray-800">Regulatory Compliance & Quality Assurance</h2>
        <p className="text-sm text-gray-500">Statutory AYUSH Schedule T GMP standards, NABH Matab SOP guidelines, DPDP privacy controls, and Schedule E(1) oversight</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">AYUSH Schedule T GMP</span>
          <span className="text-2xl font-bold text-emerald-700 mt-1 block">Compliant (A+)</span>
          <span className="text-xs text-gray-400 mt-1 block">BMR/BPR digital sign-off verified</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Schedule E(1) Mudabbar</span>
          <span className="text-2xl font-bold text-emerald-700 mt-1 block">100% Detoxified</span>
          <span className="text-xs text-gray-400 mt-1 block">Zero unpurified toxic botanical release</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">ABDM M1-M3 Architecture</span>
          <span className="text-2xl font-bold text-emerald-700 mt-1 block">Ready (Sandbox)</span>
          <span className="text-xs text-gray-400 mt-1 block">NHA FHIR sandbox schema integrated</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">DSMB Academic Review</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">Quorum 3/3</span>
          <span className="text-xs text-gray-400 mt-1 block">Independent governance active</span>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm space-y-4">
        <h3 className="font-bold text-gray-800 text-base">Mandatory Statutory Registers</h3>
        <div className="divide-y divide-gray-100 text-sm">
          <div className="py-3.5 flex justify-between items-center">
            <div>
              <span className="font-semibold text-gray-800 block">Schedule E(1) Botanical Poison Processing Log (Mudabbar)</span>
              <span className="text-xs text-gray-500">Tracks purification batches of Strychnos nux-vomica (Azaraqi) and Colchicum autumnale (Suranjan)</span>
            </div>
            <button 
              onClick={() => alert("Generating Schedule E(1) Statutory Audit PDF...")}
              className="px-3 py-1.5 border border-[#2D6A4F] text-[#2D6A4F] hover:bg-[#2D6A4F] hover:text-white rounded-lg text-xs font-semibold transition"
            >
              Download Register ↗
            </button>
          </div>
          <div className="py-3.5 flex justify-between items-center">
            <div>
              <span className="font-semibold text-gray-800 block">21 CFR Part 11 Electronic Signature Audit Trail</span>
              <span className="text-xs text-gray-500">Cryptographically links every locked prescription to clinician biometric or secure PIN</span>
            </div>
            <button 
              onClick={() => alert("Generating 21 CFR Part 11 Audit Trail Export...")}
              className="px-3 py-1.5 border border-[#2D6A4F] text-[#2D6A4F] hover:bg-[#2D6A4F] hover:text-white rounded-lg text-xs font-semibold transition"
            >
              Download Register ↗
            </button>
          </div>
          <div className="py-3.5 flex justify-between items-center">
            <div>
              <span className="font-semibold text-gray-800 block">Dispensary Cold-Chain Continuous Temperature Log</span>
              <span className="text-xs text-gray-500">IoT sensor records for botanical distillates (Arqiyat) and medicated oils (Raughaniyat)</span>
            </div>
            <button 
              onClick={() => alert("Generating Cold-Chain IoT Compliance Log...")}
              className="px-3 py-1.5 border border-[#2D6A4F] text-[#2D6A4F] hover:bg-[#2D6A4F] hover:text-white rounded-lg text-xs font-semibold transition"
            >
              Download Register ↗
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
