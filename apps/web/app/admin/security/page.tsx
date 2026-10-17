"use client";

import React, { useState } from "react";

export default function AdminSecurityPage() {
  const [mfaEnforced, setMfaEnforced] = useState(true);
  const [sessionTimeout, setSessionTimeout] = useState(15);
  const [maxLoginAttempts, setMaxLoginAttempts] = useState(5);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-gray-800">Clinical Security & 21 CFR Part 11 Governance</h2>
        <p className="text-sm text-gray-500">Cryptographic digital key management, audit trail immutability, and statutory authentication controls</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">21 CFR Part 11 Signatures</span>
          <span className="text-2xl font-bold text-emerald-700 mt-1 block">Strict Enforced</span>
          <span className="text-xs text-gray-400 mt-1 block">HMAC-SHA256 signature gating active</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Transport Layer</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">TLS 1.3 Strict</span>
          <span className="text-xs text-emerald-600 font-semibold mt-1 block">HSTS max-age 31536000</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">PHI Encryption</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">AES-256-GCM</span>
          <span className="text-xs text-gray-400 mt-1 block">Field-level DB encryption enabled</span>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm space-y-5">
        <h3 className="font-bold text-gray-800 text-base">Authentication & Policy Controls</h3>
        
        <div className="divide-y divide-gray-100">
          <div className="py-4 flex justify-between items-center">
            <div>
              <span className="font-semibold text-gray-800 text-sm block">Enforce Multi-Factor Authentication (MFA)</span>
              <span className="text-xs text-gray-500">Mandate TOTP authenticator app verification for all clinicians and admins</span>
            </div>
            <input 
              type="checkbox" 
              checked={mfaEnforced} 
              onChange={e => setMfaEnforced(e.target.checked)}
              className="w-5 h-5 text-[#2D6A4F] rounded border-gray-300 focus:ring-[#2D6A4F]"
            />
          </div>

          <div className="py-4 flex justify-between items-center">
            <div>
              <span className="font-semibold text-gray-800 text-sm block">Inactivity Session Lockout (Minutes)</span>
              <span className="text-xs text-gray-500">Automatically locks doctor screen during unattended examinations</span>
            </div>
            <select 
              value={sessionTimeout} 
              onChange={e => setSessionTimeout(Number(e.target.value))}
              className="border border-gray-200 rounded-lg text-sm px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-[#2D6A4F]"
            >
              <option value={5}>5 Minutes</option>
              <option value={15}>15 Minutes (Clinical Security Standard)</option>
              <option value={30}>30 Minutes</option>
            </select>
          </div>

          <div className="py-4 flex justify-between items-center">
            <div>
              <span className="font-semibold text-gray-800 text-sm block">Failed Login Lockout Threshold</span>
              <span className="text-xs text-gray-500">Temporary account lockout after consecutive failed attempts</span>
            </div>
            <select 
              value={maxLoginAttempts} 
              onChange={e => setMaxLoginAttempts(Number(e.target.value))}
              className="border border-gray-200 rounded-lg text-sm px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-[#2D6A4F]"
            >
              <option value={3}>3 Attempts</option>
              <option value={5}>5 Attempts (Recommended)</option>
              <option value={10}>10 Attempts</option>
            </select>
          </div>
        </div>

        <div className="pt-2 flex justify-end">
          <button 
            onClick={() => alert("Security configuration policies saved successfully!")}
            className="px-5 py-2.5 bg-[#2D6A4F] hover:bg-[#1B4332] text-white font-semibold text-sm rounded-lg shadow-sm transition"
          >
            Save Security Policies
          </button>
        </div>
      </div>
    </div>
  );
}
