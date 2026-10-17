"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";

export default function PatientTeleconsultationPage() {
  const [micOn, setMicOn] = useState(true);
  const [camOn, setCamOn] = useState(true);
  const [inCall, setInCall] = useState(false);

  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">🎥 HD Clinical Tele-Consultation Room</h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              End-to-End Encrypted WebRTC consultation with your Senior Tabeeb • ABDM Compliant
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="text-xs text-emerald-400 font-semibold">Physician Online: Hakeem Dr. Irfan Ashraf</span>
          </div>
        </div>

        {/* Video Canvas Container */}
        <div className="bg-slate-950 rounded-2xl border border-[var(--border)] overflow-hidden shadow-2xl relative min-h-[420px] flex flex-col items-center justify-center p-6 text-center">
          {!inCall ? (
            <div className="space-y-4 max-w-md">
              <div className="w-20 h-20 rounded-full bg-emerald-950/60 border border-emerald-500/40 text-emerald-400 flex items-center justify-center text-3xl mx-auto shadow-inner">
                🩺
              </div>
              <h2 className="text-xl font-bold text-white">Ready to Join Tele-OPD Consultation?</h2>
              <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                You are connecting with Hakeem Dr. Irfan Ashraf. Your vitals, 10-Ajnas pulse records, and recent lab tests are securely synced into the doctor's cockpit.
              </p>
              <button
                onClick={() => setInCall(true)}
                className="px-8 py-3.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm rounded-xl shadow-lg transition"
              >
                Join Consultation Room
              </button>
            </div>
          ) : (
            <div className="w-full h-full flex flex-col justify-between items-center py-6 space-y-6">
              <div className="flex justify-between items-center w-full px-4 text-xs">
                <span className="px-3 py-1 rounded-full bg-rose-500/20 text-rose-400 border border-rose-500/30 font-bold font-mono">
                  🔴 LIVE 00:04:18
                </span>
                <span className="text-slate-400 font-mono">ABDM Session Token: SEC-ENC-2026-904</span>
              </div>

              <div className="w-32 h-32 rounded-full bg-emerald-900/40 border-2 border-emerald-400 flex items-center justify-center text-5xl shadow-xl">
                👨‍⚕️
              </div>
              <div className="text-center space-y-1">
                <h3 className="text-lg font-bold text-white">Hakeem Dr. Irfan Ashraf</h3>
                <p className="text-xs text-emerald-400 font-medium">Senior Tabeeb • ZAYVORA Central Hospital</p>
                <p className="text-xs text-slate-400">Audio & Video Stream: 1080p 60fps (Encrypted)</p>
              </div>

              {/* Controls */}
              <div className="flex items-center gap-4">
                <button
                  onClick={() => setMicOn(!micOn)}
                  className={`p-3.5 rounded-full text-lg shadow-md transition ${micOn ? "bg-slate-800 text-white hover:bg-slate-700" : "bg-rose-600 text-white"}`}
                >
                  {micOn ? "🎤" : "🔇"}
                </button>
                <button
                  onClick={() => setCamOn(!camOn)}
                  className={`p-3.5 rounded-full text-lg shadow-md transition ${camOn ? "bg-slate-800 text-white hover:bg-slate-700" : "bg-rose-600 text-white"}`}
                >
                  {camOn ? "📹" : "🚫"}
                </button>
                <button
                  onClick={() => setInCall(false)}
                  className="px-6 py-3.5 bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs rounded-full shadow-lg transition"
                >
                  Leave Call
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}
