"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";

export default function PatientLifestylePage() {
  const [airScore, setAirScore] = useState(80);
  const [dietScore, setDietScore] = useState(75);
  const [movementScore, setMovementScore] = useState(70);
  const [sleepScore, setSleepScore] = useState(85);
  const [evacuationScore, setEvacuationScore] = useState(90);
  const [mentalScore, setMentalScore] = useState(75);

  const avgMeezan = Math.round((airScore + dietScore + movementScore + sleepScore + evacuationScore + mentalScore) / 6);

  const handleSave = () => {
    alert("Asbab-e-Sittah daily lifestyle log updated! Your Meezan-e-Sehat score is " + avgMeezan + "/100.");
  };

  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">🌿 Asbab-e-Sittah Essential Regimen Tracker</h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              The 6 Classical Life Essentials for restoring innate equilibrium (Mizaj-e-Adil)
            </p>
          </div>
          <div className="flex items-center gap-2 bg-[var(--card)] px-4 py-2 rounded-xl border border-[var(--border)]">
            <span className="text-xs text-[var(--text-muted)]">Today's Meezan Score:</span>
            <span className="text-xl font-bold text-emerald-400 font-mono">{avgMeezan}/100</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* 1. Hawa */}
          <div className="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-3">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <span className="text-xl">🌬️</span>
                <h3 className="font-bold text-white text-base">1. Hawa-e-Muheet (Air & Breathing)</h3>
              </div>
              <span className="font-mono font-bold text-emerald-400 text-sm">{airScore}%</span>
            </div>
            <p className="text-xs text-[var(--text-muted)]">Daily morning deep breathing (Tanaffus-e-Amīq) in well-ventilated natural air.</p>
            <input type="range" min="40" max="100" value={airScore} onChange={e => setAirScore(Number(e.target.value))} className="w-full accent-emerald-500" />
          </div>

          {/* 2. Makool wa Mashroob */}
          <div className="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-3">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <span className="text-xl">🍲</span>
                <h3 className="font-bold text-white text-base">2. Makool wa Mashroob (Diet & Drink)</h3>
              </div>
              <span className="font-mono font-bold text-emerald-400 text-sm">{dietScore}%</span>
            </div>
            <p className="text-xs text-[var(--text-muted)]">Avoiding chilled water and phlegm-inducing dairy. Drinking warm ginger-cumin decoction.</p>
            <input type="range" min="40" max="100" value={dietScore} onChange={e => setDietScore(Number(e.target.value))} className="w-full accent-emerald-500" />
          </div>

          {/* 3. Harakat wa Sukoon Badani */}
          <div className="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-3">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <span className="text-xl">🚶</span>
                <h3 className="font-bold text-white text-base">3. Harakat Badani (Movement & Rest)</h3>
              </div>
              <span className="font-mono font-bold text-emerald-400 text-sm">{movementScore}%</span>
            </div>
            <p className="text-xs text-[var(--text-muted)]">25 minutes gentle walking on level ground. Avoiding deep squats during acute knee inflammation.</p>
            <input type="range" min="40" max="100" value={movementScore} onChange={e => setMovementScore(Number(e.target.value))} className="w-full accent-emerald-500" />
          </div>

          {/* 4. Nawm wa Yaqzah */}
          <div className="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-3">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <span className="text-xl">🌙</span>
                <h3 className="font-bold text-white text-base">4. Nawm wa Yaqzah (Sleep & Wakefulness)</h3>
              </div>
              <span className="font-mono font-bold text-emerald-400 text-sm">{sleepScore}%</span>
            </div>
            <p className="text-xs text-[var(--text-muted)]">7.5 hours uninterrupted restful sleep. In bed by 10:30 PM to optimize hepatic restorative phase.</p>
            <input type="range" min="40" max="100" value={sleepScore} onChange={e => setSleepScore(Number(e.target.value))} className="w-full accent-emerald-500" />
          </div>

          {/* 5. Ehtibas wa Istifragh */}
          <div className="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-3">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <span className="text-xl">💧</span>
                <h3 className="font-bold text-white text-base">5. Ehtibas wa Istifragh (Evacuation)</h3>
              </div>
              <span className="font-mono font-bold text-emerald-400 text-sm">{evacuationScore}%</span>
            </div>
            <p className="text-xs text-[var(--text-muted)]">Regular bowel clearance and adequate hydration. Tanqiya detox schedule adhered to.</p>
            <input type="range" min="40" max="100" value={evacuationScore} onChange={e => setEvacuationScore(Number(e.target.value))} className="w-full accent-emerald-500" />
          </div>

          {/* 6. Harakat wa Sukoon Nafsani */}
          <div className="bg-[var(--card)] p-5 rounded-2xl border border-[var(--border)] space-y-3">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <span className="text-xl">🧘</span>
                <h3 className="font-bold text-white text-base">6. Harakat Nafsani (Mental Equilibrium)</h3>
              </div>
              <span className="font-mono font-bold text-emerald-400 text-sm">{mentalScore}%</span>
            </div>
            <p className="text-xs text-[var(--text-muted)]">15 minutes mindfulness, evening calm, and avoiding emotional stress spikes.</p>
            <input type="range" min="40" max="100" value={mentalScore} onChange={e => setMentalScore(Number(e.target.value))} className="w-full accent-emerald-500" />
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button 
            onClick={handleSave}
            className="px-6 py-3 bg-[#2D6A4F] hover:bg-[#1B4332] text-white font-bold text-sm rounded-xl shadow-md transition"
          >
            ✓ Save Today's Lifestyle Log
          </button>
        </div>
      </div>
    </AppShell>
  );
}
