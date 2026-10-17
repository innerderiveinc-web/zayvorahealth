"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";

interface ConsultationState {
  step: number;
  timeRemaining: number;
  timerActive: boolean;
  // Step 1: Visual (0-30s)
  bodyHabitus: string;
  tongueColor: string;
  tongueCoating: string;
  initialMizaj: string;
  // Step 2: Chief Complaint (30-90s)
  chiefComplaint: string;
  emotionalTone: string;
  // Step 3: Nabz (90-150s)
  pulseRate: string;
  pulseDepth: string;
  pulseStrength: string;
  pulseTexture: string;
  // Step 4: Asbab-e-Sitta (150-210s)
  sleepHours: number;
  bowelHabit: string;
  exerciseMins: number;
  stressLevel: string;
  // Step 5: Labs & Axis (210-270s)
  sgpt: number;
  hsCrp: number;
  tsh: number;
  fastingInsulin: number;
  primaryAxis: string;
  dominantKhilt: string;
  // Step 6: UDC & Rx (270-300s)
  afaalPhase: string;
  selectedProtocol: string;
  deliveryTrack: string;
}

const STEP_TITLES = [
  "1. Visual Profiling (0–30s)",
  "2. Chief Complaint (30–90s)",
  "3. Radial Pulse / Nabz (90–150s)",
  "4. Asbab-e-Sitta Scan (150–210s)",
  "5. Lab Review & Axis Mapping (210–270s)",
  "6. UDC Code & Prescribing (270–300s)"
];

export default function FiveMinuteConsultationPage() {
  const [state, setState] = useState<ConsultationState>({
    step: 0,
    timeRemaining: 300,
    timerActive: false,
    bodyHabitus: "Balghami (Rounded/Soft)",
    tongueColor: "Pale with thick white coating",
    tongueCoating: "Thick White",
    initialMizaj: "Balghami-Sawdawi",
    chiefComplaint: "Primary fatigue, weight gain, irregular cycles and morning sluggishness.",
    emotionalTone: "Exhausted / Low Affect",
    pulseRate: "Slow (<60 bpm)",
    pulseDepth: "Deep (Ghareeqi)",
    pulseStrength: "Weak / Soft (Za'eef)",
    pulseTexture: "Laayin (Soft / Mucous)",
    sleepHours: 6,
    bowelHabit: "Constipation (sluggish transit)",
    exerciseMins: 15,
    stressLevel: "High (Chronic Occupational)",
    sgpt: 52,
    hsCrp: 3.4,
    tsh: 3.8,
    fastingInsulin: 14,
    primaryAxis: "Gut-Ovarian",
    dominantKhilt: "Balgham Ghalib",
    afaalPhase: "Phase 1 (Tanqiya)",
    selectedProtocol: "PC-01 (PCOS / Ovulatory)",
    deliveryTrack: "Track 2 (GMP Hero: OvaSync + LiverPrime)"
  });

  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    let interval: any = null;
    if (state.timerActive && state.timeRemaining > 0) {
      interval = setInterval(() => {
        setState((prev) => ({ ...prev, timeRemaining: prev.timeRemaining - 1 }));
      }, 1000);
    } else if (state.timeRemaining === 0) {
      setState((prev) => ({ ...prev, timerActive: false }));
    }
    return () => clearInterval(interval);
  }, [state.timerActive, state.timeRemaining]);

  const toggleTimer = () => {
    setState((prev) => ({ ...prev, timerActive: !prev.timerActive }));
  };

  const resetTimer = () => {
    setState((prev) => ({ ...prev, timeRemaining: 300, timerActive: false }));
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  };

  const udcCode = `${state.initialMizaj} — ${state.dominantKhilt} — ${state.primaryAxis} — ${state.afaalPhase}`;

  // Non-negotiable Lab Triggers Check
  const isPhase1Mandatory = state.sgpt > 45 || state.hsCrp > 3.0;
  const isThyroidTriggered = state.tsh > 2.5;
  const isIrTriggered = state.fastingInsulin > 10;
  const isSafravi = state.initialMizaj.toLowerCase().includes("safra");

  const handleCompleteConsultation = () => {
    setNotice(`Encounter completed! UDC [${udcCode}] logged with Phase 1 LiverPrime Core mandatory mandate.`);
    setTimeout(() => setNotice(null), 5000);
  };

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-7xl mx-auto pb-16">
        {/* Top Bar with Timer */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-[var(--border)] pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-2xl">⏱️</span>
              <h1 className="text-xl font-bold text-white tracking-tight">
                5-Minute Diagnostic Engine Console
              </h1>
              <span className="px-2.5 py-0.5 rounded-full bg-teal-500/15 border border-teal-500/30 text-teal-300 text-xs font-mono font-bold">
                CP-AFUM Standard
              </span>
            </div>
            <p className="text-xs text-[var(--muted)] mt-1">
              Structured clinical workflow: Visual $\to$ Complaint $\to$ Nabz $\to$ Asbab $\to$ Labs $\to$ UDC & Prescription.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-2xl bg-slate-900 border border-slate-700 shadow-inner">
              <span className="text-xs text-slate-400 font-medium">Clock:</span>
              <span className={`text-sm font-mono font-bold ${state.timeRemaining < 60 ? "text-rose-400 animate-pulse" : "text-emerald-400"}`}>
                {formatTime(state.timeRemaining)}
              </span>
            </div>
            <button
              onClick={toggleTimer}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition shadow-xs ${
                state.timerActive
                  ? "bg-amber-600 hover:bg-amber-500 text-white"
                  : "bg-teal-600 hover:bg-teal-500 text-white"
              }`}
            >
              {state.timerActive ? "⏸ Pause" : "▶ Start 5-Min"}
            </button>
            <button
              onClick={resetTimer}
              className="px-2.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition"
            >
              🔄 Reset
            </button>
          </div>
        </div>

        {notice && (
          <div className="p-3.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs flex items-center justify-between shadow-md animate-fadeIn">
            <span>✓ {notice}</span>
            <button onClick={() => setNotice(null)} className="text-slate-400 hover:text-white font-bold ml-4">✕</button>
          </div>
        )}

        {/* Live Generated UDC Header Card */}
        <div className="p-4 rounded-2xl bg-gradient-to-r from-teal-950/40 via-slate-900 to-indigo-950/40 border border-teal-500/40 shadow-lg space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-[11px] font-bold text-teal-400 uppercase tracking-wider">
              Live Unani Diagnosis Code (UDC)
            </span>
            <span className="text-[10px] text-slate-400 font-mono">Chapter 5 Format</span>
          </div>
          <div className="p-3 rounded-xl bg-black/40 border border-teal-500/30 font-mono text-sm sm:text-base font-bold text-teal-200 break-words">
            {udcCode}
          </div>
          <div className="flex flex-wrap items-center gap-2 pt-1 text-[11px] text-slate-300">
            {isPhase1Mandatory && (
              <span className="px-2 py-0.5 rounded bg-rose-950/50 border border-rose-700/40 text-rose-300 font-bold">
                ⚠️ Rule 1: Phase 1 (LiverPrime Core) MANDATORY (SGPT {state.sgpt} / CRP {state.hsCrp})
              </span>
            )}
            {isSafravi && (
              <span className="px-2 py-0.5 rounded bg-amber-950/50 border border-amber-700/40 text-amber-300 font-bold">
                🔥 Safravi Rule: Reduce Heating Herbs 25-30%
              </span>
            )}
            {isThyroidTriggered && (
              <span className="px-2 py-0.5 rounded bg-cyan-950/50 border border-cyan-700/40 text-cyan-300 font-bold">
                🦋 Rule 3: ThyroMet Axis Triggered (TSH {state.tsh} &gt; 2.5)
              </span>
            )}
            {isIrTriggered && (
              <span className="px-2 py-0.5 rounded bg-indigo-950/50 border border-indigo-700/40 text-indigo-300 font-bold">
                ⚡ Rule 4: Stage 1 Insulin Resistance (Insulin {state.fastingInsulin} &gt; 10)
              </span>
            )}
          </div>
        </div>

        {/* 6-Step Consultation Navigator */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 text-xs">
          {STEP_TITLES.map((title, idx) => (
            <button
              key={idx}
              onClick={() => setState((prev) => ({ ...prev, step: idx }))}
              className={`p-2.5 rounded-xl border text-left font-medium transition ${
                state.step === idx
                  ? "bg-teal-600 border-teal-500 text-white font-bold shadow-xs"
                  : "bg-[var(--panel)] border-[var(--border)] text-[var(--muted)] hover:text-white"
              }`}
            >
              {title}
            </button>
          ))}
        </div>

        {/* Step-Specific Interactive Workspace */}
        <div className="p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] shadow-xl space-y-6">
          {/* Step 1: Visual */}
          {state.step === 0 && (
            <div className="space-y-4 animate-fadeIn">
              <div className="border-b border-[var(--border)] pb-2">
                <h3 className="text-base font-bold text-white">Step 1: Visual Profiling (0–30 Seconds)</h3>
                <p className="text-xs text-[var(--muted)]">Observe body habitus, facial complexion, and tongue coating as patient enters.</p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Body Habitus (Mizaj Proxy)</label>
                  <select
                    value={state.bodyHabitus}
                    onChange={(e) => setState({ ...state, bodyHabitus: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white focus:border-teal-500"
                  >
                    <option>Balghami (Rounded/Soft, slower movements)</option>
                    <option>Safravi (Lean, angular, sharp features)</option>
                    <option>Damvi (Muscular, robust, athletic build)</option>
                    <option>Saudavi (Thin, dry, narrow frame, nervous energy)</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Tongue Inspection (Coating & Moisture)</label>
                  <select
                    value={state.tongueColor}
                    onChange={(e) => setState({ ...state, tongueColor: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white focus:border-teal-500"
                  >
                    <option>Pale with thick white coating (Balgham excess)</option>
                    <option>Red with thin yellow coating (Safra heat/acidity)</option>
                    <option>Dark-tipped with dry coating (Sauda oxidative)</option>
                    <option>Pink, well-perfused, thin white (Dam/balanced)</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Working Mizaj Hypothesis</label>
                  <select
                    value={state.initialMizaj}
                    onChange={(e) => setState({ ...state, initialMizaj: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-teal-300 font-bold focus:border-teal-500"
                  >
                    <option>Balghami-Sawdawi</option>
                    <option>Balghami</option>
                    <option>Safravi</option>
                    <option>Safravi-Saudavi</option>
                    <option>Damvi</option>
                    <option>Damvi-Balghami</option>
                    <option>Saudavi</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Chief Complaint */}
          {state.step === 1 && (
            <div className="space-y-4 animate-fadeIn">
              <div className="border-b border-[var(--border)] pb-2">
                <h3 className="text-base font-bold text-white">Step 2: Chief Complaint (30–90 Seconds)</h3>
                <p className="text-xs text-[var(--muted)]">Single open question: &apos;Tell me what is troubling you most.&apos; Listen without interrupting for 60 seconds.</p>
              </div>
              <div className="space-y-3 text-xs">
                <div>
                  <label className="text-[11px] font-bold text-slate-300 block mb-1">Patient Narrative / Complaint</label>
                  <textarea
                    rows={3}
                    value={state.chiefComplaint}
                    onChange={(e) => setState({ ...state, chiefComplaint: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-3 text-white focus:border-teal-500"
                    placeholder="Document verbatim chief complaint..."
                  />
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="text-[11px] font-bold text-slate-300">Emotional Tone & Speech Pace</label>
                    <select
                      value={state.emotionalTone}
                      onChange={(e) => setState({ ...state, emotionalTone: e.target.value })}
                      className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                    >
                      <option>Exhausted / Low Affect (Balghami-Saudavi)</option>
                      <option>Sharp, irritable, hurried (Safravi)</option>
                      <option>Anxious, ruminative, overthinking (Saudavi)</option>
                      <option>Expressive, warm, communicative (Damvi)</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Step 3: Nabz */}
          {state.step === 2 && (
            <div className="space-y-4 animate-fadeIn">
              <div className="border-b border-[var(--border)] pb-2">
                <h3 className="text-base font-bold text-white">Step 3: Radial Pulse Examination / Nabz (90–150 Seconds)</h3>
                <p className="text-xs text-[var(--muted)]">Right wrist, 3-finger placement: Assess rate, depth, strength, and texture.</p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 text-xs">
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Rate (Miqdar)</label>
                  <select
                    value={state.pulseRate}
                    onChange={(e) => setState({ ...state, pulseRate: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  >
                    <option>Slow (&lt;60 bpm — Balgham)</option>
                    <option>Rapid (80-90+ bpm — Safra)</option>
                    <option>Variable / Irregular (Sauda)</option>
                    <option>Full / Normal (70-75 bpm — Dam)</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Depth (Ghareeqi vs Sa&apos;ati)</label>
                  <select
                    value={state.pulseDepth}
                    onChange={(e) => setState({ ...state, pulseDepth: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  >
                    <option>Deep / Sunken (Ghareeqi — Parasympathetic)</option>
                    <option>Superficial / High (Sa&apos;ati — Sympathetic)</option>
                    <option>Moderate balanced depth</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Strength (Quwwat)</label>
                  <select
                    value={state.pulseStrength}
                    onChange={(e) => setState({ ...state, pulseStrength: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  >
                    <option>Weak / Soft (Za&apos;eef)</option>
                    <option>Full / Bounding (Qawi)</option>
                    <option>Wiry / Taut (Mustawi)</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Texture (Imtidad / Wave)</label>
                  <select
                    value={state.pulseTexture}
                    onChange={(e) => setState({ ...state, pulseTexture: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  >
                    <option>Laayin (Soft / Mucous / Balgham)</option>
                    <option>Khashun (Rough / Vascular inflammation)</option>
                    <option>Zalaaq (Slippery / Insulin resistance)</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Step 4: Asbab Scan */}
          {state.step === 3 && (
            <div className="space-y-4 animate-fadeIn">
              <div className="border-b border-[var(--border)] pb-2">
                <h3 className="text-base font-bold text-white">Step 4: Asbab-e-Sitta Rapid Scan (150–210 Seconds)</h3>
                <p className="text-xs text-[var(--muted)]">Rapid check of the 6 essentials: sleep, evacuation, movement, and stress.</p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 text-xs">
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Sleep (Naum wa Yaqzah)</label>
                  <input
                    type="number"
                    value={state.sleepHours}
                    onChange={(e) => setState({ ...state, sleepHours: Number(e.target.value) })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                    placeholder="Hours/night"
                  />
                  <span className="text-[10px] text-slate-400">Optimal: 7-8h before midnight</span>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Bowel (Ihtibas wa Istifragh)</label>
                  <select
                    value={state.bowelHabit}
                    onChange={(e) => setState({ ...state, bowelHabit: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  >
                    <option>Constipation (sluggish transit)</option>
                    <option>Loose / Irritable / Acidic</option>
                    <option>Normal daily complete evacuation</option>
                    <option>Alternating constipation/diarrhea</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Riyazat (Daily Movement)</label>
                  <input
                    type="number"
                    value={state.exerciseMins}
                    onChange={(e) => setState({ ...state, exerciseMins: Number(e.target.value) })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                    placeholder="Mins/day"
                  />
                  <span className="text-[10px] text-slate-400">Target: 30-45 mins moderate</span>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Stress (Harakat-e-Nafsani)</label>
                  <select
                    value={state.stressLevel}
                    onChange={(e) => setState({ ...state, stressLevel: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  >
                    <option>High (Chronic Occupational / HPA loop)</option>
                    <option>Moderate</option>
                    <option>Low / Managed</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Step 5: Labs & Axis */}
          {state.step === 4 && (
            <div className="space-y-4 animate-fadeIn">
              <div className="border-b border-[var(--border)] pb-2">
                <h3 className="text-base font-bold text-white">Step 5: Lab Review & Axis Mapping (210–270 Seconds)</h3>
                <p className="text-xs text-[var(--muted)]">Map objective laboratory biomarkers directly to functional organ axes.</p>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">SGPT / ALT (U/L)</label>
                  <input
                    type="number"
                    value={state.sgpt}
                    onChange={(e) => setState({ ...state, sgpt: Number(e.target.value) })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  />
                  <span className="text-[10px] text-teal-400">&gt;45 mandates Phase 1</span>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">hs-CRP (mg/L)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={state.hsCrp}
                    onChange={(e) => setState({ ...state, hsCrp: Number(e.target.value) })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  />
                  <span className="text-[10px] text-teal-400">&gt;3.0 mandates Phase 1</span>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">TSH (mIU/L)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={state.tsh}
                    onChange={(e) => setState({ ...state, tsh: Number(e.target.value) })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  />
                  <span className="text-[10px] text-cyan-400">&gt;2.5 = Subclinical</span>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Fasting Insulin (uIU/mL)</label>
                  <input
                    type="number"
                    value={state.fastingInsulin}
                    onChange={(e) => setState({ ...state, fastingInsulin: Number(e.target.value) })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  />
                  <span className="text-[10px] text-indigo-400">&gt;10 = Stage 1 IR</span>
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs pt-2">
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Primary Organ-Axis</label>
                  <select
                    value={state.primaryAxis}
                    onChange={(e) => setState({ ...state, primaryAxis: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-teal-300 font-bold"
                  >
                    <option>Gut-Ovarian (Quwwat-e-Tanasul F / PCOS)</option>
                    <option>Liver-Testicular (Quwwat-e-Tanasul M / Infertility)</option>
                    <option>Liver-Pancreas (Metabolic / Diabetes)</option>
                    <option>Gut-Liver (Hepatic / Detox)</option>
                    <option>Thyroid-Neuro (Tihal-Ghudad)</option>
                    <option>HPA Axis (Dimagh-Qalb / Burnout)</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Dominant Morbid Khilt</label>
                  <select
                    value={state.dominantKhilt}
                    onChange={(e) => setState({ ...state, dominantKhilt: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-emerald-300 font-bold"
                  >
                    <option>Balgham Ghalib</option>
                    <option>Safra Ghalib</option>
                    <option>Sauda Ghalib</option>
                    <option>Dam Ghalib</option>
                    <option>Balgham/Sauda Ghalib</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Step 6: UDC & Rx */}
          {state.step === 5 && (
            <div className="space-y-4 animate-fadeIn">
              <div className="border-b border-[var(--border)] pb-2">
                <h3 className="text-base font-bold text-white">Step 6: UDC Finalization & Prescription (270–300 Seconds)</h3>
                <p className="text-xs text-[var(--muted)]">Generate codified UDC, assign Afaal phase, choose delivery track, and issue prescription.</p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Afaal Phase Assignment</label>
                  <select
                    value={state.afaalPhase}
                    onChange={(e) => setState({ ...state, afaalPhase: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  >
                    <option>Phase 1 (Tanqiya)</option>
                    <option>Phase 2 (Tahleel)</option>
                    <option>Phase 3 (Taqwiyaat)</option>
                    <option>Phase 4 (Hifz)</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Clinical Protocol</label>
                  <select
                    value={state.selectedProtocol}
                    onChange={(e) => setState({ ...state, selectedProtocol: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  >
                    <option>PC-01 (PCOS / Ovulatory Dysfunction)</option>
                    <option>MF-01 (Male Reproductive / Infertility)</option>
                    <option>WM-01 (Metabolic Syndrome / NAFLD)</option>
                    <option>NE-01 (Stress / Insomnia / Burnout)</option>
                    <option>TG-01 (Thyroid / Subclinical Hypothyroid)</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[11px] font-bold text-slate-300">Delivery Track</label>
                  <select
                    value={state.deliveryTrack}
                    onChange={(e) => setState({ ...state, deliveryTrack: e.target.value })}
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  >
                    <option>Track 2 (GMP Hero: OvaSync + LiverPrime)</option>
                    <option>Track 1 (Matab Custom Nuskha Compounding)</option>
                    <option>Hybrid Dual-Track (Matab Acute + GMP Taper)</option>
                  </select>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-4 flex flex-col sm:flex-row gap-3 items-center justify-between border-t border-[var(--border)]">
                <span className="text-xs text-slate-400">
                  Ready to lock encounter and transmit prescription to pharmacy.
                </span>
                <div className="flex items-center gap-2">
                  <button
                    onClick={handleCompleteConsultation}
                    className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shadow-md transition flex items-center gap-2"
                  >
                    <span>🔒 Lock UDC & Sign Rx</span>
                  </button>
                  <Link
                    href="/doctor/practicum"
                    className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs transition"
                  >
                    📑 Log as Practicum Case →
                  </Link>
                </div>
              </div>
            </div>
          )}

          {/* Navigation Controls */}
          <div className="flex justify-between items-center pt-2 border-t border-[var(--border)] text-xs">
            <button
              disabled={state.step === 0}
              onClick={() => setState((prev) => ({ ...prev, step: Math.max(prev.step - 1, 0) }))}
              className={`px-3 py-1.5 rounded-lg border transition ${
                state.step === 0 ? "opacity-40 cursor-not-allowed" : "hover:bg-[var(--elevated)] text-slate-300"
              }`}
            >
              ← Previous Step
            </button>
            <span className="text-slate-400 font-mono">
              Step {state.step + 1} of {STEP_TITLES.length}
            </span>
            <button
              disabled={state.step === STEP_TITLES.length - 1}
              onClick={() => setState((prev) => ({ ...prev, step: Math.min(prev.step + 1, STEP_TITLES.length - 1) }))}
              className={`px-3 py-1.5 rounded-lg border transition ${
                state.step === STEP_TITLES.length - 1 ? "opacity-40 cursor-not-allowed" : "hover:bg-[var(--elevated)] text-slate-300"
              }`}
            >
              Next Step →
            </button>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
