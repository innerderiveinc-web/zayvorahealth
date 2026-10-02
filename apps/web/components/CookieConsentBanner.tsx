"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";

const COOKIE_STORAGE_KEY = "zayvora_cookie_consent_v1";

export function CookieConsentBanner() {
  const [isVisible, setIsVisible] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    try {
      const stored = localStorage.getItem(COOKIE_STORAGE_KEY);
      if (!stored) {
        setIsVisible(true);
      }
    } catch {
      // LocalStorage access restricted
    }
  }, []);

  const handleAcceptAll = () => {
    try {
      localStorage.setItem(
        COOKIE_STORAGE_KEY,
        JSON.stringify({
          essential: true,
          analytics: true,
          preferences: true,
          timestamp: new Date().toISOString(),
        })
      );
    } catch {}
    setIsVisible(false);
  };

  const handleEssentialOnly = () => {
    try {
      localStorage.setItem(
        COOKIE_STORAGE_KEY,
        JSON.stringify({
          essential: true,
          analytics: false,
          preferences: false,
          timestamp: new Date().toISOString(),
        })
      );
    } catch {}
    setIsVisible(false);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-0 inset-x-0 z-50 p-4 sm:p-6 bg-[#0A0F1D]/95 backdrop-blur-md border-t border-[#334155] shadow-2xl animate-fade-in text-xs text-[#CBD5E1]">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="space-y-1.5 max-w-3xl">
          <div className="flex items-center gap-2">
            <span className="text-emerald-400 font-bold text-sm"><HealthcareIcon name="shield" size={16} className="inline mr-1" /> Clinical Privacy &amp; Data Protection</span>
            <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-teal-950 border border-teal-700 text-teal-300">
              DPDP Act 2023 &amp; ABDM Compliant
            </span>
          </div>
          <p className="text-slate-300 leading-relaxed text-[11px] sm:text-xs">
            ZAYVORA Health OS™ uses essential operational cookies to maintain your secure clinical session, authenticate consultations, and preserve DPDP Act 2023 / ABDM encrypted healthcare records. Optional anonymized telemetry helps optimize clinical decision support latency.
          </p>
          {showDetails && (
            <div className="pt-2 text-[11px] text-slate-400 space-y-1">
              <p>• <strong>Strictly Essential:</strong> JWT session tokens, tamper-evident audit verification, CSRF defense.</p>
              <p>• <strong>Clinical Telemetry:</strong> Microservice latency tracking and high-resolution pulse waveform telemetry.</p>
              <p>
                Read our full legal disclosures in our{" "}
                <Link href="/website/privacy" className="text-teal-400 underline hover:text-teal-300">
                  Privacy Policy
                </Link>{" "}
                and{" "}
                <Link href="/website/terms" className="text-teal-400 underline hover:text-teal-300">
                  Terms of Clinical Use
                </Link>.
              </p>
            </div>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-2.5 w-full md:w-auto shrink-0">
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium transition text-[11px]"
          >
            {showDetails ? "Hide Details" : "Preferences"}
          </button>
          <button
            onClick={handleEssentialOnly}
            className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 hover:bg-slate-800 text-white font-semibold transition text-[11px]"
          >
            Essential Only
          </button>
          <button
            onClick={handleAcceptAll}
            className="px-5 py-2 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold shadow-md transition text-[11px]"
          >
            Accept All Cookies
          </button>
        </div>
      </div>
    </div>
  );
}
