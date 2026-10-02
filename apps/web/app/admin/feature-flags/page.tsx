"use client";

import React, { useState } from "react";

interface FeatureFlag {
  key: string;
  name: string;
  category: "Clinical Safety" | "EHR Features" | "Pharmacy & Store" | "AI Capabilities";
  description: string;
  enabled: boolean;
}

const INITIAL_FLAGS: FeatureFlag[] = [
  { key: "CLINICAL_AI_COPILOT", name: "Hakeem Sahab AI Copilot", category: "AI Capabilities", description: "Enables real-time UPI knowledge graph traversal and Su-e-Mizaj differential recommendations.", enabled: true },
  { key: "STRICT_21CFR11_SIGNING", name: "Strict 21 CFR Part 11 Electronic Signature", category: "Clinical Safety", description: "Mandates clinician cryptographic PIN sign-off before any prescription can be locked or dispensed.", enabled: true },
  { key: "FEFO_AUTO_DEDUCT", name: "Automated FEFO Stock Depletion", category: "Pharmacy & Store", description: "Deducts dispensary stock automatically from earliest-expiring batch upon doctor signature.", enabled: true },
  { key: "ABDM_SYNC_GATEWAY", name: "ABDM Health Locker Interoperability", category: "EHR Features", description: "Permits sharing of encrypted FHIR clinical artifacts to patient Ayushman Bharat health account.", enabled: true },
  { key: "VERNACULAR_VOICE_POSOLOGY", name: "Multilingual Vernacular Audio Posology", category: "Pharmacy & Store", description: "Synthesizes Hindi/Urdu audio instructions for elderly and non-literate patients.", enabled: true }
];

export default function AdminFeatureFlagsPage() {
  const [flags, setFlags] = useState<FeatureFlag[]>(INITIAL_FLAGS);

  const toggleFlag = (key: string) => {
    setFlags(flags.map(f => f.key === key ? { ...f, enabled: !f.enabled } : f));
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Clinical Feature Flags & Runtime Toggles</h2>
          <p className="text-sm text-gray-500">Safely control high-impact clinical, AI, and pharmacy capabilities without redeploying</p>
        </div>
        <button 
          onClick={() => alert("Feature flag changes deployed across all clusters!")}
          className="px-4 py-2 bg-[#2D6A4F] hover:bg-[#1B4332] text-white text-sm font-semibold rounded-lg shadow-sm transition"
        >
          Save & Sync Flags
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm divide-y divide-gray-100">
        {flags.map(f => (
          <div key={f.key} className="p-5 flex items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="font-bold text-gray-800 text-sm">{f.name}</span>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-gray-100 text-gray-600">{f.key}</span>
                <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200">{f.category}</span>
              </div>
              <p className="text-xs text-gray-500">{f.description}</p>
            </div>
            <button
              onClick={() => toggleFlag(f.key)}
              className={`px-4 py-1.5 rounded-full text-xs font-bold transition ${
                f.enabled ? "bg-emerald-600 text-white shadow-sm" : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              }`}
            >
              {f.enabled ? "ENABLED" : "DISABLED"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
