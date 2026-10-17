"use client";

import React, { useState, useEffect } from "react";
import { PlatformHeader } from "@/components/PlatformHeader";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

export default function HealthCrisesEducationPage() {
  const [modules, setModules] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<string>("three-crises");

  // HOMA-IR calculator states
  const [fastingGlucose, setFastingGlucose] = useState<number>(95);
  const [fastingInsulin, setFastingInsulin] = useState<number>(14);

  // Breathing Pacer state
  const [breathingActive, setBreathingActive] = useState<boolean>(false);
  const [breathPhase, setBreathPhase] = useState<"Inhale" | "Hold" | "Exhale">("Inhale");
  const [breathCounter, setBreathCounter] = useState<number>(4);

  useEffect(() => {
    fetchModules();
  }, []);

  useEffect(() => {
    let timer: any;
    if (breathingActive) {
      timer = setInterval(() => {
        setBreathCounter((prev) => {
          if (prev <= 1) {
            if (breathPhase === "Inhale") {
              setBreathPhase("Hold");
              return 7;
            } else if (breathPhase === "Hold") {
              setBreathPhase("Exhale");
              return 8;
            } else {
              setBreathPhase("Inhale");
              return 4;
            }
          }
          return prev - 1;
        });
      }, 1000);
    } else {
      setBreathPhase("Inhale");
      setBreathCounter(4);
    }
    return () => clearInterval(timer);
  }, [breathingActive, breathPhase]);

  async function fetchModules() {
    try {
      const res = await fetch(`${API}/api/v1/patient/education/modules`);
      if (res.ok) {
        const data = await res.json();
        setModules(data.modules || []);
      }
    } catch (err) {
      console.error("Failed to load education modules:", err);
    }
  }

  const homaIr = Number(((fastingGlucose * fastingInsulin) / 405).toFixed(2));
  let homaStatus = "Optimal Insulin Sensitivity";
  let homaBadgeClass = "bg-green-100 text-green-800 border-green-200";
  if (homaIr >= 2.0 && homaIr < 3.5) {
    homaStatus = "Early Insulin Resistance (Borderline Metabolic Imbalance)";
    homaBadgeClass = "bg-amber-100 text-amber-800 border-amber-200";
  } else if (homaIr >= 3.5) {
    homaStatus = "Significant Insulin Resistance (Root of PCOS & Fatty Liver)";
    homaBadgeClass = "bg-red-100 text-red-800 border-red-200";
  }

  return (
    <div className="min-h-screen bg-[#FAFAF7] text-[#1A1A1A]">
      <PlatformHeader />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb & Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-2 text-xs text-gray-500 uppercase tracking-wider mb-2">
            <span>Patient & Family Guide</span>
            <span>&gt;</span>
            <span className="text-[#2D6A4F] font-semibold">Health Literacy</span>
          </div>
          <h1 className="text-3xl font-bold text-[#1B4332] font-serif">
            Understanding Your Health Through Unani Precision
          </h1>
          <p className="text-sm text-gray-600 mt-1 max-w-4xl">
            Reference: <em>Understanding Your Health Through the Lens of Unani Medicine</em> by Dr. Irfan Ashraf, BUMS. Clear explanations for patients who are tired of being told their blood tests are "normal" while they feel anything but.
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex border-b border-gray-200 mb-8 space-x-8">
          <button
            onClick={() => setActiveTab("three-crises")}
            className={`pb-4 text-sm font-bold border-b-2 transition-colors ${
              activeTab === "three-crises"
                ? "border-[#2D6A4F] text-[#2D6A4F]"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            The Three Health Crises
          </button>
          <button
            onClick={() => setActiveTab("thyroid-trap")}
            className={`pb-4 text-sm font-bold border-b-2 transition-colors ${
              activeTab === "thyroid-trap"
                ? "border-[#2D6A4F] text-[#2D6A4F]"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            The TSH vs Free T3 Trap
          </button>
          <button
            onClick={() => setActiveTab("homa-ir")}
            className={`pb-4 text-sm font-bold border-b-2 transition-colors ${
              activeTab === "homa-ir"
                ? "border-[#2D6A4F] text-[#2D6A4F]"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            HOMA-IR Calculator
          </button>
          <button
            onClick={() => setActiveTab("vagal-breathing")}
            className={`pb-4 text-sm font-bold border-b-2 transition-colors ${
              activeTab === "vagal-breathing"
                ? "border-[#2D6A4F] text-[#2D6A4F]"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            4-7-8 Vagal Breathing Pacer
          </button>
        </div>

        {/* Tab 1: Three Crises */}
        {activeTab === "three-crises" && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Crisis 1 */}
              <div className="bg-white border rounded-2xl p-6 shadow-sm">
                <div className="text-3xl mb-3">🚹</div>
                <h3 className="text-lg font-bold text-[#1B4332]">The Male Reproductive Crisis</h3>
                <p className="text-xs text-red-700 font-semibold mt-1">
                  &gt;50% sperm count drop in 50 years.
                </p>
                <p className="text-xs text-gray-600 mt-2">
                  Young men in their late 20s and 30s are now routinely diagnosed with clinically low testosterone due to sustained cortisol spikes, midnight sleep disruption, and environmental endocrine disruptors.
                </p>
                <div className="mt-4 pt-3 border-t text-[11px] text-gray-500">
                  <strong>Biological Timeline:</strong> 74 days for spermatogenesis. Requires a 90-day restorative cycle.
                </div>
              </div>

              {/* Crisis 2 */}
              <div className="bg-white border rounded-2xl p-6 shadow-sm">
                <div className="text-3xl mb-3">🚺</div>
                <h3 className="text-lg font-bold text-[#1B4332]">The Female Metabolic Chaos</h3>
                <p className="text-xs text-amber-700 font-semibold mt-1">
                  1 in 5 Indian women affected by PCOS.
                </p>
                <p className="text-xs text-gray-600 mt-2">
                  The oral contraceptive pill masks symptoms with synthetic hormones while underlying insulin resistance, elevated theca androgens, and thyroid auto-antibodies continue to damage metabolic health.
                </p>
                <div className="mt-4 pt-3 border-t text-[11px] text-gray-500">
                  <strong>Biological Timeline:</strong> Requires 3 full ovulatory cycles for follicular and insulin reset.
                </div>
              </div>

              {/* Crisis 3 */}
              <div className="bg-white border rounded-2xl p-6 shadow-sm">
                <div className="text-3xl mb-3">🏙️</div>
                <h3 className="text-lg font-bold text-[#1B4332]">The Urban Lifestyle Epidemic</h3>
                <p className="text-xs text-purple-700 font-semibold mt-1">
                  25-30% of urban adults have NAFLD.
                </p>
                <p className="text-xs text-gray-600 mt-2">
                  Knowledge economy workers face a mismatch: 10 hours of sitting, artificial light at midnight, ultra-processed seed oils, and unremitting low-grade stress driving fatty liver and chronic adrenal burnout.
                </p>
                <div className="mt-4 pt-3 border-t text-[11px] text-gray-500">
                  <strong>Biological Timeline:</strong> Grade I-II fatty change is 100% reversible in 12-16 weeks.
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: Thyroid Trap */}
        {activeTab === "thyroid-trap" && (
          <div className="bg-white border rounded-2xl p-8 shadow-sm max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold text-[#1B4332] font-serif mb-2">
              The TSH vs Free T3 Trap: Why Normal Labs Still Leave You Tired
            </h2>
            <p className="text-xs text-gray-600 mb-6">
              Many patients with severe fatigue, cold intolerance, hair loss, and weight gain are told their thyroid is normal after a simple TSH test. Here is why:
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-5">
                <span className="text-xs font-bold text-amber-800 uppercase block mb-1">TSH (The Pituitary Signal)</span>
                <p className="text-xs text-amber-900">
                  TSH is NOT a thyroid hormone. It is a signal from the brain asking the thyroid to work. Checking TSH alone tells you what the pituitary is asking—not what your cells are actually receiving.
                </p>
              </div>

              <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-5">
                <span className="text-xs font-bold text-[#2D6A4F] uppercase block mb-1">Free T3 (The Cellular Engine)</span>
                <p className="text-xs text-emerald-900">
                  Free T3 is the active hormone that enters mitochondria and drives your basal metabolic rate. <strong>60% of T4 to T3 conversion occurs in the LIVER</strong>. When the liver is fatty or stressed, Free T3 drops while TSH stays normal!
                </p>
              </div>
            </div>

            <div className="border-t pt-4">
              <h4 className="text-xs font-bold text-gray-700 uppercase mb-3">Optimal Functional Ranges vs Standard Lab Ranges</h4>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="border-b text-gray-500">
                      <th className="py-2">Biomarker</th>
                      <th>Standard Normal Range</th>
                      <th>ZAYVORA Functional Optimal</th>
                      <th>Clinical Significance</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y text-gray-700">
                    <tr>
                      <td className="py-2.5 font-bold">TSH</td>
                      <td>0.5 – 4.5 mIU/L</td>
                      <td className="font-semibold text-emerald-700">1.0 – 2.0 mIU/L</td>
                      <td>TSH &gt;2.5 indicates early subclinical hypothyroid stress</td>
                    </tr>
                    <tr>
                      <td className="py-2.5 font-bold">Free T3</td>
                      <td>2.0 – 4.4 pg/mL</td>
                      <td className="font-semibold text-emerald-700">3.2 – 4.0 pg/mL</td>
                      <td>Values &lt;3.0 produce cellular fatigue even if TSH is normal</td>
                    </tr>
                    <tr>
                      <td className="py-2.5 font-bold">Free T4</td>
                      <td>0.8 – 1.8 ng/dL</td>
                      <td className="font-semibold text-emerald-700">1.1 – 1.4 ng/dL</td>
                      <td>Reflects clean storage availability without receptor saturation</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: HOMA-IR Calculator */}
        {activeTab === "homa-ir" && (
          <div className="bg-white border rounded-2xl p-8 shadow-sm max-w-3xl mx-auto">
            <h2 className="text-2xl font-bold text-[#1B4332] font-serif mb-2">
              HOMA-IR Insulin Resistance Calculator
            </h2>
            <p className="text-xs text-gray-600 mb-6">
              Fasting blood sugar can remain completely normal for 10-15 years while fasting insulin climbs. Calculate your true insulin resistance score:
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="text-xs font-bold text-gray-700 block mb-1">
                  Fasting Blood Glucose (mg/dL)
                </label>
                <input
                  type="number"
                  value={fastingGlucose}
                  onChange={(e) => setFastingGlucose(parseFloat(e.target.value) || 0)}
                  className="w-full text-base font-bold px-3 py-2 border rounded-lg"
                />
                <span className="text-[10px] text-gray-400">Optimal: 70 – 85 mg/dL</span>
              </div>

              <div>
                <label className="text-xs font-bold text-gray-700 block mb-1">
                  Fasting Serum Insulin (uIU/mL)
                </label>
                <input
                  type="number"
                  value={fastingInsulin}
                  onChange={(e) => setFastingInsulin(parseFloat(e.target.value) || 0)}
                  className="w-full text-base font-bold px-3 py-2 border rounded-lg"
                />
                <span className="text-[10px] text-gray-400">Optimal: &lt;8 uIU/mL</span>
              </div>
            </div>

            {/* Result Box */}
            <div className="bg-[#FAFAF7] border rounded-xl p-5 mb-6 text-center">
              <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block">Your Calculated HOMA-IR Score</span>
              <div className="text-4xl font-extrabold text-[#1B4332] my-2">{homaIr}</div>
              <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold border ${homaBadgeClass}`}>
                {homaStatus}
              </span>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-xs text-blue-900">
              <strong>Good News:</strong> Insulin resistance is among the most reversible metabolic conditions in medicine. Consistent implementation of low-glycemic food swaps, a 15-minute post-meal walk, and Tanqiya botanicals (Gurmar, Jamun, Daruhaldi) can normalize insulin sensitivity within 4–12 weeks.
            </div>
          </div>
        )}

        {/* Tab 4: 4-7-8 Breathing Pacer */}
        {activeTab === "vagal-breathing" && (
          <div className="bg-white border rounded-2xl p-8 shadow-sm max-w-xl mx-auto text-center">
            <h2 className="text-2xl font-bold text-[#1B4332] font-serif mb-2">
              4-7-8 Diaphragmatic Vagal Reset
            </h2>
            <p className="text-xs text-gray-600 mb-8">
              Prolonged exhalation directly stimulates the cardiac vagus nerve, slowing heart rate and rapidly reducing circulating cortisol. Ten minutes daily shifts autonomic tone within 4 days.
            </p>

            <div className="relative w-48 h-48 mx-auto flex items-center justify-center mb-8">
              <div
                className={`w-full h-full rounded-full transition-all duration-1000 flex flex-col items-center justify-center border-4 ${
                  breathPhase === "Inhale"
                    ? "border-emerald-500 bg-emerald-50 scale-105"
                    : breathPhase === "Hold"
                    ? "border-amber-500 bg-amber-50 scale-100"
                    : "border-blue-500 bg-blue-50 scale-95"
                }`}
              >
                <span className="text-sm font-bold uppercase text-gray-600 tracking-wider">
                  {breathPhase}
                </span>
                <span className="text-4xl font-extrabold text-[#1B4332] mt-1">
                  {breathCounter}s
                </span>
              </div>
            </div>

            <button
              onClick={() => setBreathingActive(!breathingActive)}
              className={`px-8 py-3 text-sm font-bold rounded-xl shadow transition-colors ${
                breathingActive
                  ? "bg-red-600 text-white hover:bg-red-700"
                  : "bg-[#2D6A4F] text-white hover:bg-[#1B4332]"
              }`}
            >
              {breathingActive ? "Stop Breathing Exercise" : "Start 4-7-8 Session"}
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
