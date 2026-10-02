"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";

export default function TelemedicineRoomPage() {
  const [inCall, setInCall] = useState(true);
  const [micMuted, setMicMuted] = useState(false);
  const [videoOff, setVideoOff] = useState(false);
  const [screenSharing, setScreenSharing] = useState(false);
  const [activePatient, setActivePatient] = useState({
    name: "Ayesha Siddiqui",
    mrn: "MRN-2026-0921",
    ageGender: "36 / Female",
    mizaj: "Har Safrawi (Hot & Dry)",
    chiefComplaint: "PCOS, delayed menses, persistent fatigue & acne",
    bp: "118/76 mmHg",
    pulse: "78 bpm (Nabz-e-Sari)",
    activeProtocol: "OvaSync Botanical Hormonal Reset",
  });

  const [aiSuggestions, setAiSuggestions] = useState([
    "Su-e-Mizaj Safrawi detected: Prioritize cooling liver priming (Burudat-e-Kabid) before heating emmenagogues.",
    "Prescription Recommendation: Arq-e-Kasni (25ml) + Majun Dabeed-ul-Ward (5g) post-prandial.",
    "Regimenal Therapy: Cold Natool over hepatic region and gentle foot reflexology."
  ]);

  const [transcript, setTranscript] = useState([
    { speaker: "Dr. Irfan", time: "11:15:02", text: "Assalamu Alaikum Ayesha. Can you hear and see me clearly?" },
    { speaker: "Ayesha", time: "11:15:08", text: "Wa Alaikum Assalam Doctor Sahab. Yes, loud and clear." },
    { speaker: "Dr. Irfan", time: "11:15:15", text: "How has your energy level been over the last 10 days since starting the warm water infusion protocol?" },
    { speaker: "Ayesha", time: "11:15:24", text: "The lethargy in the afternoon has improved significantly, but I noticed mild acidity when taking the seeds on an empty stomach." },
  ]);

  const [scribeNote, setScribeNote] = useState("");
  const [statusNotice, setStatusNotice] = useState<string | null>(null);

  const handleEndCall = () => {
    setInCall(false);
    setStatusNotice("Teleconsultation session ended. Clinical encounter notes preserved.");
  };

  const handleRestartCall = () => {
    setInCall(true);
    setStatusNotice("Connected to encrypted WebRTC stream (Latency: 28ms • Loss: 0.0%).");
    setTimeout(() => setStatusNotice(null), 3000);
  };

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-4 max-w-7xl mx-auto">
        
        {/* Top Control Bar */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-3">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-teal-500/15 border border-teal-500/30 flex items-center justify-center text-teal-400 font-bold">
              📹
            </div>
            <div>
              <h1 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
                Telemedicine Consultation Suite
                <span className="px-2 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-[10px] font-mono font-bold flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                  WebRTC Live
                </span>
              </h1>
              <p className="text-[11px] text-[var(--muted)]">
                Secure WebRTC video with real-time Ambient Scribe and Hakeem Sahab AI clinical reasoning.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="px-2.5 py-1 rounded-xl bg-slate-900 border border-slate-800 text-[10px] font-mono text-slate-400">
              ABDM Room: TEL-2026-0921
            </span>
            <Link
              href="/doctor/nuskha"
              className="px-3 py-1.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition flex items-center gap-1"
            >
              <span>📝</span> Issue Digital Rx
            </Link>
          </div>
        </div>

        {statusNotice && (
          <div className="p-3 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-300 text-xs flex items-center justify-between animate-fadeIn">
            <span>{statusNotice}</span>
            <button onClick={() => setStatusNotice(null)} className="text-slate-400 hover:text-white">✕</button>
          </div>
        )}

        {/* Teleconsultation Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 items-start">
          
          {/* Main Video Stage (7 cols) */}
          <div className="lg:col-span-7 space-y-3">
            
            {/* Video Viewport Container */}
            <div className="relative rounded-3xl overflow-hidden bg-slate-950 border border-slate-800 aspect-video shadow-2xl flex items-center justify-center">
              {inCall ? (
                <>
                  {/* Remote Patient Video Stream Simulation */}
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-900 to-slate-950 flex items-center justify-center">
                    <div className="text-center space-y-3">
                      <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-teal-600 to-emerald-500 text-white font-extrabold text-2xl flex items-center justify-center mx-auto shadow-xl ring-4 ring-teal-500/20">
                        AS
                      </div>
                      <div>
                        <h3 className="text-sm font-bold text-white">{activePatient.name}</h3>
                        <p className="text-[11px] text-teal-300 font-mono">Audio & HD Video Streaming (720p 30fps)</p>
                      </div>
                    </div>
                  </div>

                  {/* Patient Info Overlay */}
                  <div className="absolute top-4 left-4 flex items-center gap-2 bg-slate-900/80 backdrop-blur-md px-3 py-1.5 rounded-xl border border-slate-700 text-xs">
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span className="font-bold text-white">{activePatient.name}</span>
                    <span className="text-[10px] text-slate-400 font-mono">({activePatient.mrn})</span>
                  </div>

                  {/* Network Quality Badge */}
                  <div className="absolute top-4 right-4 bg-slate-900/80 backdrop-blur-md px-2.5 py-1 rounded-xl border border-slate-700 text-[10px] font-mono text-emerald-400 flex items-center gap-1">
                    📶 44ms · 0% loss
                  </div>

                  {/* Doctor Self-Preview PiP (Picture in Picture) */}
                  <div className="absolute bottom-4 right-4 w-36 h-24 rounded-2xl overflow-hidden bg-slate-800 border-2 border-slate-700 shadow-xl flex items-center justify-center">
                    {videoOff ? (
                      <span className="text-[10px] text-slate-400">Camera Off</span>
                    ) : (
                      <div className="text-center">
                        <div className="w-8 h-8 rounded-full bg-teal-600 text-white font-bold text-xs flex items-center justify-center mx-auto mb-1">
                          Dr
                        </div>
                        <span className="text-[9px] font-bold text-white block">Dr. Irfan (You)</span>
                      </div>
                    )}
                  </div>
                </>
              ) : (
                <div className="text-center p-8 space-y-3">
                  <div className="text-4xl">📴</div>
                  <h3 className="text-sm font-bold text-white">Call Disconnected</h3>
                  <p className="text-xs text-slate-400 max-w-sm">
                    The teleconsultation has completed. Prescriptions and encounter notes have been saved to ABDM repository.
                  </p>
                  <button
                    onClick={handleRestartCall}
                    className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs transition"
                  >
                    Reconnect Telemedicine Call
                  </button>
                </div>
              )}
            </div>

            {/* In-Call Controls Bar */}
            {inCall && (
              <div className="p-3 rounded-2xl bg-[var(--panel)] border border-[var(--border)] flex flex-wrap items-center justify-center gap-3">
                <button
                  onClick={() => setMicMuted(!micMuted)}
                  className={`px-4 py-2 rounded-xl font-bold text-xs flex items-center gap-1.5 transition ${
                    micMuted
                      ? "bg-rose-600 text-white"
                      : "bg-[var(--elevated)] hover:bg-[var(--border)] text-white"
                  }`}
                >
                  <span>{micMuted ? "🔇 Unmute Mic" : "🎙️ Mute Mic"}</span>
                </button>

                <button
                  onClick={() => setVideoOff(!videoOff)}
                  className={`px-4 py-2 rounded-xl font-bold text-xs flex items-center gap-1.5 transition ${
                    videoOff
                      ? "bg-rose-600 text-white"
                      : "bg-[var(--elevated)] hover:bg-[var(--border)] text-white"
                  }`}
                >
                  <span>{videoOff ? "📷 Start Video" : "📹 Stop Video"}</span>
                </button>

                <button
                  onClick={() => setScreenSharing(!screenSharing)}
                  className={`px-4 py-2 rounded-xl font-bold text-xs flex items-center gap-1.5 transition ${
                    screenSharing
                      ? "bg-teal-600 text-white"
                      : "bg-[var(--elevated)] hover:bg-[var(--border)] text-white"
                  }`}
                >
                  <span>🖥️ {screenSharing ? "Stop Share" : "Share Screen"}</span>
                </button>

                <button
                  onClick={handleEndCall}
                  className="px-5 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs flex items-center gap-1.5 shadow-sm transition"
                >
                  <span>📞 End Call</span>
                </button>
              </div>
            )}

            {/* Live Transcript & Ambient Scribe */}
            <div className="p-4 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-3">
              <div className="flex items-center justify-between border-b border-[var(--border)] pb-2">
                <h3 className="text-xs font-bold text-white flex items-center gap-1.5">
                  <span>🎙️</span> Ambient Scribe Speech-to-Text
                  <span className="px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-400 text-[9px] font-mono">
                    Streaming
                  </span>
                </h3>
                <span className="text-[10px] text-[var(--muted)]">Biomedical English + Urdu/Hindi</span>
              </div>

              <div className="space-y-2 max-h-40 overflow-y-auto text-xs">
                {transcript.map((item, idx) => (
                  <div key={idx} className="p-2 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                    <div className="flex justify-between items-center mb-0.5 text-[10px]">
                      <span className="font-bold text-teal-300">{item.speaker}</span>
                      <span className="text-[var(--muted)]">{item.time}</span>
                    </div>
                    <p className="text-slate-300 leading-snug">{item.text}</p>
                  </div>
                ))}
              </div>
            </div>

          </div>

          {/* Right Panel: Patient Health 360 & AI Clinical Reasoning (5 cols) */}
          <div className="lg:col-span-5 space-y-4">
            
            {/* Patient Snapshot Card */}
            <div className="p-4 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-3">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-sm font-bold text-white">{activePatient.name}</h3>
                  <span className="text-[11px] text-[var(--muted)]">{activePatient.ageGender}</span>
                </div>
                <span className="text-[10px] font-mono text-teal-300 bg-slate-900 px-2 py-0.5 rounded border border-slate-700">
                  {activePatient.mrn}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px]">
                <div className="p-2 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span className="text-[var(--muted)] block text-[10px]">Mizaj Diagnosis</span>
                  <span className="font-bold text-emerald-400">{activePatient.mizaj}</span>
                </div>
                <div className="p-2 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                  <span className="text-[var(--muted)] block text-[10px]">Baseline Vitals</span>
                  <span className="font-bold text-white">{activePatient.bp} • {activePatient.pulse}</span>
                </div>
              </div>

              <div className="p-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-xs space-y-1">
                <span className="text-[10px] text-[var(--muted)] block font-bold uppercase">Chief Complaint</span>
                <p className="text-slate-300">{activePatient.chiefComplaint}</p>
              </div>

              <div className="flex gap-2 text-xs">
                <Link
                  href="/doctor/patients"
                  className="flex-1 py-1.5 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-center text-slate-300 font-semibold border border-[var(--border)] transition"
                >
                  Full EMR Profile →
                </Link>
                <Link
                  href="/doctor/organ-axis"
                  className="flex-1 py-1.5 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-center text-teal-300 font-semibold border border-[var(--border)] transition"
                >
                  Organ-Axis Score →
                </Link>
              </div>
            </div>

            {/* Hakeem Sahab AI Live Clinical Reasoning Drawer */}
            <div className="p-4 rounded-2xl bg-gradient-to-br from-teal-950/40 via-slate-900 to-slate-950 border border-teal-800/40 space-y-3 shadow-lg">
              <div className="flex items-center justify-between border-b border-teal-800/30 pb-2">
                <h3 className="text-xs font-bold text-teal-300 flex items-center gap-1.5">
                  <span>🤖</span> Hakeem Sahab AI™ Copilot
                </h3>
                <span className="px-1.5 py-0.2 rounded bg-teal-500/20 text-teal-300 text-[9px] font-mono">
                  Advisory Only
                </span>
              </div>

              <div className="space-y-2 text-xs">
                {aiSuggestions.map((sug, idx) => (
                  <div
                    key={idx}
                    className="p-2.5 rounded-xl bg-slate-900/80 border border-teal-700/30 text-slate-300 flex items-start gap-2"
                  >
                    <span className="text-teal-400 font-bold shrink-0">•</span>
                    <p className="leading-snug">{sug}</p>
                  </div>
                ))}
              </div>

              <div className="pt-2 border-t border-teal-800/30 flex gap-2 text-xs">
                <Link
                  href="/doctor/hakeem-sahab"
                  className="flex-1 py-1.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-center transition"
                >
                  Open Full AI Studio
                </Link>
                <Link
                  href="/doctor/nuskha"
                  className="flex-1 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-teal-300 font-bold text-center border border-teal-700/40 transition"
                >
                  Import to Nuskha
                </Link>
              </div>
            </div>

            {/* Quick Scribe Clinical Note */}
            <div className="p-4 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-2">
              <h3 className="text-xs font-bold text-white flex items-center justify-between">
                <span>📝 Teleconsultation Encounter Summary</span>
                <span className="text-[10px] text-[var(--muted)]">21 CFR Part 11</span>
              </h3>
              <textarea
                rows={3}
                placeholder="Type clinician notes: assessment, advice given, next follow-up interval..."
                value={scribeNote}
                onChange={(e) => setScribeNote(e.target.value)}
                className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-xs text-white placeholder-[var(--muted)] focus:outline-none focus:border-teal-500"
              />
              <button
                onClick={() => {
                  setStatusNotice("Clinical encounter note signed and anchored to Merkle ledger.");
                  setTimeout(() => setStatusNotice(null), 3000);
                }}
                className="w-full py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition"
              >
                Sign & Save Encounter Notes
              </button>
            </div>

          </div>

        </div>

      </div>
    </AppShell>
  );
}
