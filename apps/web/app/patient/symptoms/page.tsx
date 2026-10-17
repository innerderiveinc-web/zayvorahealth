"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";

export default function PatientSymptomsPage() {
  const [temp, setTemp] = useState<"hot" | "cold">("cold");
  const [moisture, setMoisture] = useState<"moist" | "dry">("moist");
  const [jointPain, setJointPain] = useState(true);
  const [heaviness, setHeaviness] = useState(true);

  const calculatedMizaj = temp === "cold" && moisture === "moist" ? "Barid Balghami (Cold-Phlegmatic)" :
                          temp === "hot" && moisture === "moist" ? "Damawi (Sanguine)" :
                          temp === "hot" && moisture === "dry" ? "Safrawi (Choleric)" : "Sawdawi (Melancholic)";

  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">🩺 Interactive Symptom & Mizaj Self-Check</h1>
          <p className="text-sm text-[var(--text-muted)] mt-1">
            Preliminary assessment to guide clinical triage and appointment scheduling
          </p>
        </div>

        <div className="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-5">
          <h3 className="font-bold text-white text-base">1. Constitutional Thermal & Moisture Tendencies</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="p-4 rounded-xl bg-slate-900/60 border border-[var(--border)] space-y-2">
              <span className="text-emerald-400 font-bold block">Thermal Sensitivity</span>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => setTemp("cold")}
                  className={`flex-1 py-2 rounded-lg font-bold transition ${temp === "cold" ? "bg-emerald-600 text-white" : "bg-slate-800 text-slate-300"}`}
                >
                  ❄️ Feel Cold Easily
                </button>
                <button
                  type="button"
                  onClick={() => setTemp("hot")}
                  className={`flex-1 py-2 rounded-lg font-bold transition ${temp === "hot" ? "bg-emerald-600 text-white" : "bg-slate-800 text-slate-300"}`}
                >
                  🔥 Feel Warm / Hot Easily
                </button>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-900/60 border border-[var(--border)] space-y-2">
              <span className="text-emerald-400 font-bold block">Moisture & Skin Tendency</span>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => setMoisture("moist")}
                  className={`flex-1 py-2 rounded-lg font-bold transition ${moisture === "moist" ? "bg-emerald-600 text-white" : "bg-slate-800 text-slate-300"}`}
                >
                  💧 Moist / Hydrated
                </button>
                <button
                  type="button"
                  onClick={() => setMoisture("dry")}
                  className={`flex-1 py-2 rounded-lg font-bold transition ${moisture === "dry" ? "bg-emerald-600 text-white" : "bg-slate-800 text-slate-300"}`}
                >
                  🍂 Dry / Rough
                </button>
              </div>
            </div>
          </div>

          <h3 className="font-bold text-white text-base pt-2">2. Active Presenting Complaints</h3>
          <div className="space-y-2 text-xs">
            <label className="flex items-center gap-2 text-slate-300 cursor-pointer">
              <input type="checkbox" checked={jointPain} onChange={e => setJointPain(e.target.checked)} className="w-4 h-4 accent-emerald-500" />
              Joint stiffness or throbbing pain aggravated in cold or rainy weather
            </label>
            <label className="flex items-center gap-2 text-slate-300 cursor-pointer">
              <input type="checkbox" checked={heaviness} onChange={e => setHeaviness(e.target.checked)} className="w-4 h-4 accent-emerald-500" />
              Post-prandial sluggishness, heaviness in limbs, or excess mucus secretion
            </label>
          </div>

          <div className="p-5 rounded-xl bg-slate-900 border border-emerald-500/40 space-y-3">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
              <div>
                <span className="text-xs text-[var(--text-muted)]">Calculated Humoral Tendency:</span>
                <h4 className="text-lg font-bold text-emerald-400">{calculatedMizaj}</h4>
              </div>
              <Link
                href="/patient/book"
                className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow transition"
              >
                Book Formal 10-Ajnas Evaluation →
              </Link>
            </div>
            <p className="text-xs text-[var(--text-muted)]">
              Recommendation: In-person consultation with Hakeem Dr. Irfan Ashraf for pulse (Nabz) and tongue (Lisan) multispectral diagnostic verification.
            </p>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
