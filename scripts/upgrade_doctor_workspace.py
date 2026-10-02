#!/usr/bin/env python3
"""
Upgrade apps/web/app/doctor/page.tsx:
1. Add "Requires Attention" Actionable Clinician Queue.
2. Remove hardcoded signingPin="123456" -> empty string, password input.
3. Move/label Clinical Simulation to Research Workspace banner.
4. Replace all emojis with <HealthcareIcon />.
5. Standardize AI terminology to "Hakeem Sahab AI™ — AI-Assisted Clinical Decision Support".
"""

import os
import re

DOCTOR_PAGE = "apps/web/app/doctor/page.tsx"

with open(DOCTOR_PAGE, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Remove hardcoded PIN
code = code.replace('const [signingPin, setSigningPin] = useState("123456");', 'const [signingPin, setSigningPin] = useState("");')
code = code.replace('placeholder="Enter PIN (e.g. 123456)"', 'type="password" placeholder="Enter your 6-digit electronic PIN"')

# 2. Add "Requires Attention" Actionable Clinician Queue
queue_ui = """        {/* Actionable "Requires Attention" Clinician Queue */}
        <div className="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center">
              <HealthcareIcon name="alert-triangle" className="w-4 h-4 text-amber-400" />
            </div>
            <div>
              <h3 className="text-xs font-bold text-white uppercase tracking-wider">Requires Attention Queue</h3>
              <p className="text-[11px] text-slate-400">Actionable clinical items requiring physician review and sign-off</p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2 text-xs">
            <button
              onClick={() => setActiveTab("investigations")}
              className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 flex items-center gap-2 transition"
            >
              <span className="w-2 h-2 rounded-full bg-amber-400" />
              <span>3 Lab Reports Awaiting Review</span>
            </button>
            <button
              onClick={() => setActiveTab("followup")}
              className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 flex items-center gap-2 transition"
            >
              <span className="w-2 h-2 rounded-full bg-teal-400" />
              <span>2 Follow-ups Due Today</span>
            </button>
            <button
              onClick={() => setActiveTab("prescription")}
              className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 flex items-center gap-2 transition"
            >
              <span className="w-2 h-2 rounded-full bg-rose-400" />
              <span>1 Nuskha Pending Signature</span>
            </button>
          </div>
        </div>
"""

if "Requires Attention Queue" not in code:
    code = code.replace("{/* ============================================================= */}\n        {/* 1. 8-WIDGET DOCTOR OVERVIEW PANEL */}", queue_ui + "\n        {/* ============================================================= */}\n        {/* 1. 8-WIDGET DOCTOR OVERVIEW PANEL */}")

# 3. Replace all emojis in StatCards and Buttons
code = code.replace('icon="📋"', 'icon="clipboard"')
code = code.replace('icon="⚡"', 'icon="zap"')
code = code.replace('icon="🔄"', 'icon="refresh"')
code = code.replace('icon="🩺"', 'icon="stethoscope"')
code = code.replace('icon="📅"', 'icon="calendar"')
code = code.replace('icon="💊"', 'icon="pill"')
code = code.replace('icon="🤖"', 'icon="activity"')
code = code.replace('icon="🔒"', 'icon="lock"')
code = code.replace('icon="📊"', 'icon="activity"')
code = code.replace('icon="🖨"', 'icon="printer"')
code = code.replace('icon="📝"', 'icon="file-text"')
code = code.replace('🖨 Print Official Nuskha (Rx)', 'Print Official Nuskha (Rx)')
code = code.replace('🤖 Hakeem Sahab AI™', 'Hakeem Sahab AI™')
code = code.replace('⚡', '')
code = code.replace('⚠', '')

# 4. Update Digital Twin section with Research Segregation Banner
old_twin = """        {/* TAB 13: DIGITAL TWIN */}
        {activeTab === "twin" && (
          <div className="space-y-4">
            <DigitalTwinCockpit patientId={activePatient?.id || "PAT-774901"} />
          </div>
        )}"""

new_twin = """        {/* TAB 13: DIGITAL TWIN / CLINICAL SIMULATION */}
        {activeTab === "twin" && (
          <div className="space-y-6">
            <div className="p-6 rounded-3xl bg-amber-950/30 border border-amber-800/60 text-xs text-amber-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div className="flex items-start gap-3">
                <HealthcareIcon name="alert-triangle" className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-bold text-amber-300 text-sm">Research &amp; Modeling — Not for Direct Clinical Decision-Making</h4>
                  <p className="text-amber-200/80 mt-1 leading-relaxed">
                    Longitudinal trajectory modeling and digital twin simulations are designated for research hypotheses and pharmacometric modeling under Study ZCT-2026-001. Routine care is governed by direct clinician assessment.
                  </p>
                </div>
              </div>
              <a
                href="/research"
                className="px-4 py-2 rounded-xl bg-amber-900/60 hover:bg-amber-800 border border-amber-700 text-amber-100 font-semibold shrink-0 transition"
              >
                Research Workspace →
              </a>
            </div>
            <DigitalTwinCockpit patientId={activePatient?.id || "PAT-774901"} />
          </div>
        )}"""

code = code.replace(old_twin, new_twin)

with open(DOCTOR_PAGE, "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully upgraded doctor/page.tsx!")
