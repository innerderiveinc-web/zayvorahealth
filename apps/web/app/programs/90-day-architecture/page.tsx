"use client";

import React, { useState, useEffect } from "react";
import { PlatformHeader } from "@/components/PlatformHeader";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

interface ProgramTier {
  tier_name: string;
  tier_code: string;
  price_range_inr: number[];
  product_line: string;
  formula_packs: string;
  diet_plan: string;
  follow_ups: string;
  lab_support: string;
  documentation: string;
  target_segment: string;
}

export default function ProgramArchitecturePage() {
  const [tierSpecs, setTierSpecs] = useState<Record<string, ProgramTier>>({});
  const [programPricing, setProgramPricing] = useState<Record<string, any>>({});
  const [selectedProgram, setSelectedProgram] = useState<string>("FEMALE_FERTILITY");
  const [loading, setLoading] = useState<boolean>(true);

  // Revenue simulator states
  const [basicCount, setBasicCount] = useState<number>(20);
  const [advancedCount, setAdvancedCount] = useState<number>(15);
  const [signatureCount, setSignatureCount] = useState<number>(5);

  useEffect(() => {
    fetchPackages();
  }, []);

  async function fetchPackages() {
    try {
      setLoading(true);
      const res = await fetch(`${API}/api/v1/knowledge/programs/packages`);
      if (res.ok) {
        const data = await res.json();
        setTierSpecs(data.tier_specs || {});
        setProgramPricing(data.program_pricing || {});
      }
    } catch (err) {
      console.error("Failed to load program packages:", err);
    } finally {
      setLoading(false);
    }
  }

  const activeProg = programPricing[selectedProgram] || {};
  const currentPricing = activeProg.pricing || {};

  // Calculator
  const totalMonthlyRev = (basicCount * 10000) + (advancedCount * 22000) + (signatureCount * 40000);
  const totalAnnualRev = totalMonthlyRev * 12;

  return (
    <div className="min-h-screen bg-[#FAFAF7] text-[#1A1A1A]">
      <PlatformHeader />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-2 text-xs text-gray-500 uppercase tracking-wider mb-2">
            <span>Clinical Architecture</span>
            <span>&gt;</span>
            <span className="text-[#2D6A4F] font-semibold">90-Day Clinical Programs</span>
          </div>
          <h1 className="text-3xl font-bold text-[#1B4332] font-serif">
            90-Day Clinical Program Architecture & Value-Stacking
          </h1>
          <p className="text-sm text-gray-600 mt-1 max-w-4xl">
            Reference: Master Clinical System (Dr. Irfan Ashraf, BUMS). Transitioning healthcare from single product sales to structured 90-day biologically grounded care continuum packages.
          </p>
        </div>

        {/* Biological Rationale Callout */}
        <div className="bg-[#2D6A4F]/10 border border-[#2D6A4F]/30 rounded-xl p-5 mb-8">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">🧬</span>
            <div>
              <h3 className="text-sm font-bold text-[#1B4332] uppercase tracking-wider">
                Why 90 Days? The Biological Timeline
              </h3>
              <p className="text-xs text-gray-700 mt-0.5">
                Human spermatogenesis requires <strong>74 days</strong>. Follicular recruitment & ovulation stabilization requires <strong>3 menstrual cycles</strong>. Hepatic enzyme normalisation and HbA1c shifts require <strong>12 weeks</strong>. The 90-day duration is biological, not arbitrary.
              </p>
            </div>
          </div>
        </div>

        {/* Condition Selector Tabs */}
        <div className="bg-white border border-gray-200 rounded-xl p-3 shadow-sm mb-8 flex flex-wrap gap-2">
          {Object.keys(programPricing).map((code) => {
            const isSelected = selectedProgram === code;
            return (
              <button
                key={code}
                onClick={() => setSelectedProgram(code)}
                className={`px-3.5 py-2 text-xs font-semibold rounded-lg transition-all ${
                  isSelected
                    ? "bg-[#2D6A4F] text-white shadow"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                {programPricing[code]?.program_title?.split("—")[0] || code.replace("_", " ")}
              </button>
            );
          })}
        </div>

        {/* 3-Tier Value Stacking Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {/* Basic */}
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Tier 1</span>
                <span className="bg-gray-100 text-gray-700 text-[10px] font-semibold px-2 py-0.5 rounded">Mass Premium</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mt-1">Basic Program</h3>
              <div className="mt-4 pb-4 border-b">
                <span className="text-3xl font-extrabold text-[#1B4332]">₹{(currentPricing.BASIC || 10000).toLocaleString()}</span>
                <span className="text-xs text-gray-500 block mt-0.5">Full 90-day course (Core Line)</span>
              </div>

              <ul className="mt-4 space-y-2.5 text-xs text-gray-600">
                <li className="flex items-start">
                  <span className="text-emerald-600 mr-2 font-bold">✓</span>
                  <span><strong>Formulation:</strong> Core Line (500mg, 3 months supply)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-emerald-600 mr-2 font-bold">✓</span>
                  <span><strong>Diet:</strong> Standardized Unani Mizaj PDF Chart</span>
                </li>
                <li className="flex items-start">
                  <span className="text-emerald-600 mr-2 font-bold">✓</span>
                  <span><strong>Support:</strong> Weekly WhatsApp adherence check-ins</span>
                </li>
                <li className="flex items-start">
                  <span className="text-emerald-600 mr-2 font-bold">✓</span>
                  <span><strong>Tracking:</strong> Digital Health Tracking Sheet</span>
                </li>
              </ul>
            </div>
            <div className="mt-6 pt-4 border-t">
              <span className="text-[11px] text-gray-400 block text-center">Best for mild/early-stage prevention</span>
            </div>
          </div>

          {/* Advanced */}
          <div className="bg-white border-2 border-[#2D6A4F] rounded-2xl p-6 shadow-md relative flex flex-col justify-between">
            <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-[#2D6A4F] text-white text-[10px] font-bold px-3 py-0.5 rounded-full uppercase tracking-wider">
              Most Prescribed
            </div>
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-[#2D6A4F] uppercase tracking-wider">Tier 2</span>
                <span className="bg-emerald-100 text-[#2D6A4F] text-[10px] font-semibold px-2 py-0.5 rounded">Serious Patients</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mt-1">Advanced Program</h3>
              <div className="mt-4 pb-4 border-b">
                <span className="text-3xl font-extrabold text-[#1B4332]">₹{(currentPricing.ADVANCED || 22000).toLocaleString()}</span>
                <span className="text-xs text-gray-500 block mt-0.5">Full 90-day structured clinical continuum</span>
              </div>

              <ul className="mt-4 space-y-2.5 text-xs text-gray-700">
                <li className="flex items-start">
                  <span className="text-emerald-600 mr-2 font-bold">✓</span>
                  <span><strong>Formulation:</strong> Core Line + 1 Phase Add-on Modulator</span>
                </li>
                <li className="flex items-start">
                  <span className="text-emerald-600 mr-2 font-bold">✓</span>
                  <span><strong>Diet:</strong> Personalized Functional Diet based on Z-MAI</span>
                </li>
                <li className="flex items-start">
                  <span className="text-emerald-600 mr-2 font-bold">✓</span>
                  <span><strong>Doctor Visits:</strong> 3 Formal Consultations (Day 0, 30, 90)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-emerald-600 mr-2 font-bold">✓</span>
                  <span><strong>Biomarkers:</strong> Pre & Post Lab Review by Physician</span>
                </li>
                <li className="flex items-start">
                  <span className="text-emerald-600 mr-2 font-bold">✓</span>
                  <span><strong>Reporting:</strong> Monthly Objective Progress Reports</span>
                </li>
              </ul>
            </div>
            <div className="mt-6 pt-4 border-t">
              <span className="text-[11px] text-[#2D6A4F] font-semibold block text-center">Comprehensive doctor-guided recovery</span>
            </div>
          </div>

          {/* Signature Elite */}
          <div className="bg-gradient-to-b from-amber-50/50 to-white border border-amber-300 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-amber-700 uppercase tracking-wider">Tier 3</span>
                <span className="bg-amber-100 text-amber-900 text-[10px] font-semibold px-2 py-0.5 rounded">Signature Transformation</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mt-1">Signature Elite</h3>
              <div className="mt-4 pb-4 border-b">
                <span className="text-3xl font-extrabold text-amber-900">₹{(currentPricing.SIGNATURE_ELITE || 42000).toLocaleString()}</span>
                <span className="text-xs text-gray-500 block mt-0.5">High-density clinical-grade care</span>
              </div>

              <ul className="mt-4 space-y-2.5 text-xs text-gray-700">
                <li className="flex items-start">
                  <span className="text-amber-600 mr-2 font-bold">✓</span>
                  <span><strong>Formulation:</strong> Clinical Elite Line (700mg) + 2 Add-ons</span>
                </li>
                <li className="flex items-start">
                  <span className="text-amber-600 mr-2 font-bold">✓</span>
                  <span><strong>Extracts:</strong> Standardized HPLC extracts & chelated minerals</span>
                </li>
                <li className="flex items-start">
                  <span className="text-amber-600 mr-2 font-bold">✓</span>
                  <span><strong>Doctor Access:</strong> Direct Doctor Line + Bi-weekly check-ins</span>
                </li>
                <li className="flex items-start">
                  <span className="text-amber-600 mr-2 font-bold">✓</span>
                  <span><strong>Biomarkers:</strong> Full 360 Mapping (Day 0, Day 45, Day 90)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-amber-600 mr-2 font-bold">✓</span>
                  <span><strong>Dossier:</strong> Hardcover Printed Clinical Protocol & Twin</span>
                </li>
              </ul>
            </div>
            <div className="mt-6 pt-4 border-t">
              <span className="text-[11px] text-amber-800 font-semibold block text-center">Maximum potency for severe cases</span>
            </div>
          </div>
        </div>

        {/* Clinic Revenue Projection Simulator */}
        <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
          <div className="border-b pb-4 mb-6">
            <h2 className="text-xl font-bold text-[#1B4332] font-serif">Clinic Revenue Projection Engine</h2>
            <p className="text-xs text-gray-500 mt-0.5">
              Simulate monthly and annual revenue based on the 20/15/5 program mix per clinic.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-gray-50 p-4 rounded-xl border">
              <label className="text-xs font-bold text-gray-700 block mb-1">Basic Programs (₹10,000 avg)</label>
              <input
                type="number"
                value={basicCount}
                onChange={(e) => setBasicCount(parseInt(e.target.value) || 0)}
                className="w-full text-lg font-bold text-gray-900 px-3 py-1.5 border rounded bg-white"
              />
              <span className="text-[11px] text-gray-500 block mt-1">Monthly: ₹{(basicCount * 10000).toLocaleString()}</span>
            </div>

            <div className="bg-emerald-50 p-4 rounded-xl border border-emerald-100">
              <label className="text-xs font-bold text-[#1B4332] block mb-1">Advanced Programs (₹22,000 avg)</label>
              <input
                type="number"
                value={advancedCount}
                onChange={(e) => setAdvancedCount(parseInt(e.target.value) || 0)}
                className="w-full text-lg font-bold text-gray-900 px-3 py-1.5 border rounded bg-white"
              />
              <span className="text-[11px] text-gray-500 block mt-1">Monthly: ₹{(advancedCount * 22000).toLocaleString()}</span>
            </div>

            <div className="bg-amber-50 p-4 rounded-xl border border-amber-100">
              <label className="text-xs font-bold text-amber-900 block mb-1">Signature Elite (₹40,000 avg)</label>
              <input
                type="number"
                value={signatureCount}
                onChange={(e) => setSignatureCount(parseInt(e.target.value) || 0)}
                className="w-full text-lg font-bold text-gray-900 px-3 py-1.5 border rounded bg-white"
              />
              <span className="text-[11px] text-gray-500 block mt-1">Monthly: ₹{(signatureCount * 40000).toLocaleString()}</span>
            </div>
          </div>

          <div className="bg-[#1B4332] text-white rounded-xl p-5 flex flex-wrap items-center justify-between gap-4">
            <div>
              <span className="text-xs text-emerald-200 uppercase tracking-wider block">Total Monthly Projected Revenue</span>
              <span className="text-3xl font-extrabold">₹{totalMonthlyRev.toLocaleString()}</span>
            </div>
            <div className="text-right">
              <span className="text-xs text-emerald-200 uppercase tracking-wider block">Single Clinic Annual Potential</span>
              <span className="text-2xl font-bold">₹{round(totalAnnualRev / 100000, 1)} Lakhs</span>
              <span className="text-xs text-emerald-300 block mt-0.5">3 Clinics: ₹{round((totalAnnualRev * 3) / 10000000, 2)} Crores</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function round(val: number, dec: number) {
  return Number(val.toFixed(dec));
}
