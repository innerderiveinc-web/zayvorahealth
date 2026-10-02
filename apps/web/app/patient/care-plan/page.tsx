"use client";

import React from "react";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";

export default function PatientCarePlanPage() {
  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">📋 4-Stage Afaal Clinical Roadmap</h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              Personalized therapeutic cascade for Knee Osteoarthritis (Waja-ul-Mafasil Barid Balghami)
            </p>
          </div>
          <span className="px-3 py-1.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-bold">
            Encounter ENC-2026-0814 • Active Stage: TANQIYA
          </span>
        </div>

        {/* 4 Stages Stepper */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-5 rounded-2xl bg-gradient-to-b from-emerald-950/40 to-slate-900 border-2 border-emerald-500 space-y-2 relative">
            <span className="text-[10px] font-mono font-bold text-emerald-400 uppercase">STAGE 1 • CURRENT</span>
            <h3 className="text-lg font-bold text-white">Tanqiya (Cleansing)</h3>
            <span className="text-xs text-emerald-300 block font-semibold">Days 1 – 14</span>
            <p className="text-xs text-[var(--text-muted)] leading-relaxed">
              Concoction (Inzaj) and gentle evacuation of accumulated cold-phlegmatic humors.
            </p>
            <div className="pt-2 text-[11px] text-emerald-400 font-medium">
              ✓ Munzij-e-Balgham decoction<br />
              ✓ Wet Cupping (Hijama) on Day 10
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] opacity-70 space-y-2">
            <span className="text-[10px] font-mono font-bold text-slate-400 uppercase">STAGE 2 • UPCOMING</span>
            <h3 className="text-lg font-bold text-white">Tahleel (Resolution)</h3>
            <span className="text-xs text-blue-300 block font-semibold">Days 15 – 30</span>
            <p className="text-xs text-[var(--text-muted)] leading-relaxed">
              Dissolution of peri-articular stiffness and warm medicated fomentation.
            </p>
            <div className="pt-2 text-[11px] text-blue-400 font-medium">
              • Natool herbal irrigation<br />
              • Raughan-e-Balsan local massage
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] opacity-50 space-y-2">
            <span className="text-[10px] font-mono font-bold text-slate-400 uppercase">STAGE 3 • PLANNED</span>
            <h3 className="text-lg font-bold text-white">Taqwiyaat (Restoration)</h3>
            <span className="text-xs text-purple-300 block font-semibold">Days 31 – 60</span>
            <p className="text-xs text-[var(--text-muted)] leading-relaxed">
              Cartilage structural replenishment and neural vitality reinforcement.
            </p>
            <div className="pt-2 text-[11px] text-purple-400 font-medium">
              • Hab-e-Suranjan Forte<br />
              • Muqawwi-e-Aasab tonic
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-[var(--card)] border border-[var(--border)] opacity-40 space-y-2">
            <span className="text-[10px] font-mono font-bold text-slate-400 uppercase">STAGE 4 • LIFELONG</span>
            <h3 className="text-lg font-bold text-white">Hifz (Preservation)</h3>
            <span className="text-xs text-amber-300 block font-semibold">Post-Treatment</span>
            <p className="text-xs text-[var(--text-muted)] leading-relaxed">
              Seasonal dietary adherence and long-term joint homeostasis.
            </p>
            <div className="pt-2 text-[11px] text-amber-400 font-medium">
              • Asbab-e-Sittah tracking<br />
              • Quarterly clinical check-in
            </div>
          </div>
        </div>

        {/* Clinical Orders Box */}
        <div className="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
          <h3 className="font-bold text-white text-base">Attending Tabeeb's Specific Instructions</h3>
          <div className="p-4 rounded-xl bg-slate-900/80 border border-[var(--border)] text-xs text-slate-300 space-y-2 leading-relaxed">
            <p><strong className="text-white">Dietary Directives (Parhez):</strong> Strictly avoid refrigerated water, ice, yogurt, and flatulent lentils (Mash/Urad dal) during the Tanqiya stage. Favor warm mutton broth with black pepper, saffron, and ginger.</p>
            <p><strong className="text-white">Physical Activity:</strong> Avoid squatting or prolonged standing. Perform isometric quadriceps contraction exercises twice daily for 10 minutes.</p>
            <p><strong className="text-white">Next OPD Evaluation:</strong> September 24, 2026 at ZAYVORA Healthcare System - Central Hospital, Room 204 with Hakeem Dr. Irfan Ashraf.</p>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
