"use client";

import React from "react";
import Link from "next/link";

export default function PhilosophyPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 space-y-2">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Health OS™ v5.0</span>
        <h1 className="text-3xl md:text-4xl font-extrabold text-white">Our Clinical Philosophy</h1>
        <p className="text-sm text-[#94A3B8]">The Classical Foundations of Unani Greco-Arab Medicine</p>
      </div>

      <div className="space-y-6 leading-relaxed">
        
  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
      <h3 className="text-base font-bold text-emerald-400">1. Tabi'at (The Innate Healer)</h3>
      <p>
        The central premise of Unani medicine is *Tabi'at* — the body's innate self-preservative intelligence. Clinicians do not force synthetic suppression; we remove humoral blockages so the innate vital power can restore physiological equilibrium.
      </p>
    </div>
    <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
      <h3 className="text-base font-bold text-blue-400">2. Akhlat (Humoral Equilibrium)</h3>
      <p>
        Health is the harmonious balance of the four primary humors: *Dam* (Blood), *Balgham* (Phlegm), *Safra* (Yellow Bile), and *Sauda* (Black Bile). Pathology arises when humors undergo qualitative dyscrasia (*Su-e-Mizaj*) or abnormal retention.
      </p>
    </div>
    <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
      <h3 className="text-base font-bold text-purple-400">3. Organ-Axis Cross-Talk</h3>
      <p>
        Organs never suffer in isolation. ZAYVORA maps dynamic multi-organ interactions, such as the *Mafasil-Asab* (Joint-Nerve) axis linked to the *Meda-Amaa* (Gastrointestinal) axis, addressing root systemic drivers.
      </p>
    </div>
    <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
      <h3 className="text-base font-bold text-amber-400">4. Asbab-e-Sittah (Lifestyle Determinants)</h3>
      <p>
        True health requires regulation of the Six Essential Precepts: Ambient Air, Diet & Water, Physical Exercise & Rest, Sleep & Wakefulness, Evacuation & Retention, and Emotional State.
      </p>
    </div>
  </div>

      </div>

      <div className="pt-8 border-t border-[#334155] flex justify-between items-center">
        <Link href="/website" className="text-xs font-semibold text-[#94A3B8] hover:text-white">
          ← Back to Home
        </Link>
        <Link href="/website/book" className="px-5 py-2 rounded-xl bg-[#0D9488] text-white font-bold hover:bg-[#14B8A6]">
          Book Consultation →
        </Link>
      </div>
    </div>
  );
}
