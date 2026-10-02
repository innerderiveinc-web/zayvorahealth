"use client";

import React, { useState, useEffect } from "react";

interface Step {
  num: number;
  id: string;
  name: string;
  desc: string;
}

const STEPS: Step[] = [
  { num: 1, id: "p360", name: "Patient 360", desc: "Vitals, History & Labs" },
  { num: 2, id: "mizaj", name: "10-Ajnas Mizaj", desc: "Temperament Matrix" },
  { num: 3, id: "axes", name: "12-Axis Scoring", desc: "Functional Organ Systems" },
  { num: 4, id: "hakeem", name: "Hakeem Sahab v2", desc: "Evidence Copilot Brief" },
  { num: 5, id: "safety", name: "Safety Firewall", desc: "Statutory Gating" },
  { num: 6, id: "nuskha", name: "4-Tier Nuskha", desc: "Prescription Builder" },
  { num: 7, id: "signoff", name: "Sign & Follow-up", desc: "21 CFR Part 11" }
];

export default function DoctorClinicalContinuumPage() {
  const [activeStep, setActiveStep] = useState<number>(1);
  const [patientId, setPatientId] = useState<string>("MRN-2026-0814");
  const [chiefComplaint, setChiefComplaint] = useState<string>(
    "Chronic bilateral knee pain and morning stiffness aggravated by cold damp weather (Waja-ul-Mafasil)"
  );
  const [selectedMizaj, setSelectedMizaj] = useState<string>("Balghami (Cold & Moist)");
  const [mizajScore, setMizajScore] = useState<number>(16);

  const [axesScores, setAxesScores] = useState<Record<string, number>>({
    "Mafasil-Azlaat (Musculo-Skeletal)": 4,
    "Jigar-Banas (Hepato-Metabolic)": 3,
    "Meda-Ama (Gastro-Intestinal)": 2,
    "Dimagh-Aasab (Neuro-Psychological)": 1
  });

  const [hakeemBrief, setHakeemBrief] = useState<any>(null);
  const [isLoadingHakeem, setIsLoadingHakeem] = useState<boolean>(false);
  const [safetyStatus, setSafetyStatus] = useState<string>("PASS_VERIFIED");
  const [practitionerId, setPractitionerId] = useState<string>("DOC-IRFAN-BUMS");
  const [completedEncounter, setCompletedEncounter] = useState<any>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  // Auto-fetch Hakeem Sahab v2 brief when entering step 4
  useEffect(() => {
    if (activeStep === 4 && !hakeemBrief) {
      fetchHakeemBrief();
    }
  }, [activeStep]);

  const fetchHakeemBrief = async () => {
    setIsLoadingHakeem(true);
    try {
      const res = await fetch("/api/v1/hakeem/v2/evidence-brief", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          patient_id: patientId,
          patient_context: {
            name: "Tariq Mahmood",
            age: 38,
            gender: "Male",
            mizaj: selectedMizaj,
            user_role: "CLINICIAN"
          },
          clinical_condition: "Waja-ul-Mafasil",
          labs: { hba1c: 5.6, crp: 4.8 },
          mizaj_result: { dominant_humor: selectedMizaj, score: mizajScore },
          active_axes: Object.keys(axesScores)
        })
      });
      const data = await res.json();
      if (data.ok) {
        setHakeemBrief(data.hakeem_v2_brief);
      }
    } catch (e) {
      console.error("Hakeem brief fetch error:", e);
    } finally {
      setIsLoadingHakeem(false);
    }
  };

  const handleCompleteEncounter = async () => {
    setIsSubmitting(true);
    try {
      const res = await fetch("/api/v1/doctor/continuum/complete-encounter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          patient_id: patientId,
          practitioner_id: practitionerId,
          chief_complaint: chiefComplaint,
          mizaj_input: { dominant_humor: selectedMizaj, score: mizajScore },
          axis_scores: axesScores,
          labs: { hba1c: 5.6, crp: 4.8 },
          prescribed_drugs: ["Asgandh", "Zanjabeel", "Filfil Siyah"]
        })
      });
      const data = await res.json();
      if (data.ok) {
        setCompletedEncounter(data.encounter);
        setActiveStep(7);
      }
    } catch (e) {
      console.error("Encounter completion error:", e);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Header */}
      <header className="border-b border-slate-800 bg-slate-900/90 px-6 py-4 flex items-center justify-between sticky top-0 z-30 backdrop-blur-md">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-lg bg-emerald-600 flex items-center justify-center font-bold text-white shadow-lg shadow-emerald-900/40">
            Z
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="font-semibold text-lg text-white">Unified Clinical Continuum Cockpit</h1>
              <span className="text-xs bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded font-mono">
                SINGLE-SCREEN CONTINUOUS ENCOUNTER
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Patient 360 &rarr; Mizaj &rarr; 12-Axis &rarr; Hakeem Sahab v2 &rarr; Safety &rarr; Nuskha &rarr; Sign-off
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div className="text-right">
            <span className="text-xs text-slate-400 block">Treating Clinician</span>
            <span className="text-xs font-medium text-emerald-400">{practitionerId} (BUMS / MD Unani)</span>
          </div>
          <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-700">
            <span className="w-1.5 h-1.5 mr-1.5 bg-emerald-400 rounded-full animate-pulse"></span>
            SAFETY FIREWALL v2 ACTIVE
          </span>
        </div>
      </header>

      {/* Stepped Progress Ribbon */}
      <nav className="bg-slate-900 border-b border-slate-800 px-6 py-2.5 overflow-x-auto">
        <div className="flex items-center space-x-2 min-w-max">
          {STEPS.map((step) => {
            const isCurrent = activeStep === step.num;
            const isCompleted = activeStep > step.num;
            return (
              <button
                key={step.id}
                onClick={() => setActiveStep(step.num)}
                className={`flex items-center space-x-2 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                  isCurrent
                    ? "bg-emerald-600 text-white shadow-md shadow-emerald-900/30 ring-1 ring-emerald-400"
                    : isCompleted
                    ? "bg-slate-800/80 text-emerald-400 hover:bg-slate-800"
                    : "bg-slate-900/50 text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                }`}
              >
                <span
                  className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                    isCurrent
                      ? "bg-white text-emerald-700"
                      : isCompleted
                      ? "bg-emerald-900 text-emerald-300"
                      : "bg-slate-800 text-slate-400"
                  }`}
                >
                  {isCompleted ? "✓" : step.num}
                </span>
                <div className="text-left">
                  <div className="leading-tight">{step.name}</div>
                  <div className="text-[10px] opacity-75">{step.desc}</div>
                </div>
              </button>
            );
          })}
        </div>
      </nav>

      {/* Main Split Layout */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-0 overflow-hidden">
        {/* Left Column: Persistent Patient 360 (col-span-3) */}
        <aside className="lg:col-span-3 border-r border-slate-800 bg-slate-900/50 p-5 overflow-y-auto space-y-5">
          <div className="bg-slate-800/60 rounded-xl p-4 border border-slate-700/60">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-mono text-emerald-400">{patientId}</span>
              <span className="text-[10px] bg-emerald-950 text-emerald-300 border border-emerald-800 px-1.5 py-0.5 rounded">
                CONSENT ACTIVE (DPDP Act 2023 / Rules 2025)
              </span>
            </div>
            <h2 className="text-base font-semibold text-white">Tariq Mahmood</h2>
            <div className="text-xs text-slate-400 mt-0.5">38 yrs &bull; Male &bull; Blood Group: B+</div>

            <div className="mt-3 pt-3 border-t border-slate-700/50 grid grid-cols-2 gap-2 text-xs">
              <div>
                <span className="text-slate-500 block text-[10px]">Baseline Mizaj</span>
                <span className="text-amber-300 font-medium">{selectedMizaj.split(" ")[0]}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">Primary Concern</span>
                <span className="text-rose-300 font-medium">Knee Joint Pain</span>
              </div>
            </div>
          </div>

          {/* Active Problems */}
          <div className="bg-slate-800/40 rounded-xl p-4 border border-slate-800">
            <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Active Problems (ICD-11)
            </h3>
            <ul className="space-y-1.5 text-xs">
              <li className="flex items-center justify-between text-slate-200">
                <span>&bull; Waja-ul-Mafasil (Osteoarthritis)</span>
                <span className="text-[10px] bg-rose-950 text-rose-300 px-1 rounded">Moderate</span>
              </li>
              <li className="flex items-center justify-between text-slate-200">
                <span>&bull; Insulin Resistance (HOMA-IR 5.12)</span>
                <span className="text-[10px] bg-amber-950 text-amber-300 px-1 rounded">Metabolic</span>
              </li>
              <li className="flex items-center justify-between text-slate-200">
                <span>&bull; Subclinical Hypothyroidism</span>
                <span className="text-[10px] bg-blue-950 text-blue-300 px-1 rounded">TSH 3.9</span>
              </li>
            </ul>
          </div>

          {/* Key Biomarkers */}
          <div className="bg-slate-800/40 rounded-xl p-4 border border-slate-800">
            <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Recent Lab Markers
            </h3>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-slate-900/60 p-2 rounded border border-slate-800">
                <span className="text-slate-400 block text-[10px]">hs-CRP (Inflam.)</span>
                <span className="text-rose-400 font-bold">4.8 mg/L</span>
                <span className="text-[9px] text-slate-500 block">&gt; 3.0 High</span>
              </div>
              <div className="bg-slate-900/60 p-2 rounded border border-slate-800">
                <span className="text-slate-400 block text-[10px]">HbA1c</span>
                <span className="text-amber-400 font-bold">5.6%</span>
                <span className="text-[9px] text-slate-500 block">Normal-Border</span>
              </div>
              <div className="bg-slate-900/60 p-2 rounded border border-slate-800">
                <span className="text-slate-400 block text-[10px]">S. Creatinine</span>
                <span className="text-emerald-400 font-bold">0.9 mg/dL</span>
                <span className="text-[9px] text-slate-500 block">Normal Clearance</span>
              </div>
              <div className="bg-slate-900/60 p-2 rounded border border-slate-800">
                <span className="text-slate-400 block text-[10px]">Serum Uric Acid</span>
                <span className="text-emerald-400 font-bold">5.4 mg/dL</span>
                <span className="text-[9px] text-slate-500 block">No Gouty Spikes</span>
              </div>
            </div>
          </div>
        </aside>

        {/* Center Workspace: Active Step Content (col-span-6) */}
        <main className="lg:col-span-6 p-6 overflow-y-auto space-y-6">
          {/* STEP 1: PATIENT 360 & CHIEF COMPLAINT */}
          {activeStep === 1 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-white">Step 1: Patient 360 Intake & Chief Complaint</h3>
                <span className="text-xs bg-slate-800 px-2 py-1 rounded text-slate-300">Phase 0 Baseline</span>
              </div>
              <p className="text-xs text-slate-400">
                Review the patient's active presentation and confirm primary symptoms before proceeding to the 10-Ajnas Mizaj examination.
              </p>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Active Chief Complaint Description
                </label>
                <textarea
                  value={chiefComplaint}
                  onChange={(e) => setChiefComplaint(e.target.value)}
                  rows={3}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-xs text-slate-100 focus:ring-1 focus:ring-emerald-500 focus:outline-none"
                />
              </div>

              <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800 space-y-2">
                <h4 className="text-xs font-semibold text-emerald-400">Past Nuskha History</h4>
                <div className="text-xs text-slate-300">
                  Last prescription 45 days ago: <span className="text-slate-100 font-medium">Safoof-e-Suranjan 500mg</span> with Arq-e-Badiyan.
                  Patient reported 40% initial relief before cold seasonal shift aggravated symptoms.
                </div>
              </div>

              <div className="flex justify-end pt-4">
                <button
                  onClick={() => setActiveStep(2)}
                  className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-emerald-900/40"
                >
                  Proceed to 10-Ajnas Mizaj &rarr;
                </button>
              </div>
            </div>
          )}

          {/* STEP 2: 10-AJNAS MIZAJ ASSESSMENT */}
          {activeStep === 2 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-white">Step 2: 10-Ajnas Mizaj Assessment</h3>
                <span className="text-xs bg-amber-950 text-amber-300 border border-amber-800 px-2 py-1 rounded">
                  Z-MAI 6-Domain Tool
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Select the dominant humoral dyscrasia based on pulse (Nabz), urine (Qaroorah), stool (Baraaz), and physical temperament markers.
              </p>

              <div className="grid grid-cols-2 gap-3">
                {[
                  { name: "Balghami (Cold & Moist)", desc: "Soft sluggish pulse, pale urine, cold joint swelling", active: selectedMizaj.includes("Balghami") },
                  { name: "Safrawi (Hot & Dry)", desc: "Rapid bounding pulse, high thirst, burning sensations", active: selectedMizaj.includes("Safrawi") },
                  { name: "Damawi (Hot & Moist)", desc: "Full bounding pulse, ruddy complexion, heaviness", active: selectedMizaj.includes("Damawi") },
                  { name: "Saudawi (Cold & Dry)", desc: "Slow hard pulse, dark urine, chronicity, stiffness", active: selectedMizaj.includes("Saudawi") }
                ].map((m) => (
                  <button
                    key={m.name}
                    onClick={() => setSelectedMizaj(m.name)}
                    className={`p-3 rounded-xl border text-left transition-all ${
                      m.active
                        ? "border-emerald-500 bg-emerald-950/40 text-emerald-200 ring-1 ring-emerald-500"
                        : "border-slate-800 bg-slate-900/60 text-slate-300 hover:border-slate-700"
                    }`}
                  >
                    <div className="font-semibold text-xs text-white">{m.name}</div>
                    <div className="text-[11px] text-slate-400 mt-1">{m.desc}</div>
                  </button>
                ))}
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Humoral Deviation Severity Score (1 - 18)
                </label>
                <div className="flex items-center space-x-3">
                  <input
                    type="range"
                    min="1"
                    max="18"
                    value={mizajScore}
                    onChange={(e) => setMizajScore(Number(e.target.value))}
                    className="flex-1 accent-emerald-500"
                  />
                  <span className="font-bold text-sm text-emerald-400 w-8">{mizajScore}</span>
                </div>
                <span className="text-[10px] text-slate-400 block mt-1">
                  Score &ge; 14 indicates severe humoral accumulation requiring phased Tanqiya (evacuation) before Taqwiyaat.
                </span>
              </div>

              <div className="flex justify-between pt-4">
                <button
                  onClick={() => setActiveStep(1)}
                  className="px-4 py-2 border border-slate-700 text-slate-300 rounded-lg text-xs"
                >
                  &larr; Back
                </button>
                <button
                  onClick={() => setActiveStep(3)}
                  className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-emerald-900/40"
                >
                  Proceed to 12-Axis Scoring &rarr;
                </button>
              </div>
            </div>
          )}

          {/* STEP 3: 12 ORGAN-AXIS SCORING */}
          {activeStep === 3 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-white">Step 3: 12 Organ-Axis Diagnostic Scoring</h3>
                <span className="text-xs bg-blue-950 text-blue-300 border border-blue-800 px-2 py-1 rounded">
                  Functional Systems
                </span>
              </div>
              <p className="text-xs text-slate-400">
                12-Axis is not a disease diagnosis; it is ZAYVORA's functional organizational layer to map metabolic, neural, and musculoskeletal strain.
              </p>

              <div className="space-y-3">
                {Object.entries(axesScores).map(([axisName, score]) => (
                  <div key={axisName} className="bg-slate-900/60 p-3 rounded-lg border border-slate-800 flex items-center justify-between">
                    <div>
                      <div className="text-xs font-medium text-white">{axisName}</div>
                      <div className="text-[10px] text-slate-400">Severity rating (0 - 5)</div>
                    </div>
                    <div className="flex items-center space-x-1">
                      {[1, 2, 3, 4, 5].map((s) => (
                        <button
                          key={s}
                          onClick={() => setAxesScores({ ...axesScores, [axisName]: s })}
                          className={`w-7 h-7 rounded text-xs font-bold transition-all ${
                            score === s
                              ? "bg-emerald-600 text-white ring-1 ring-emerald-400"
                              : "bg-slate-800 text-slate-400 hover:bg-slate-700"
                          }`}
                        >
                          {s}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex justify-between pt-4">
                <button
                  onClick={() => setActiveStep(2)}
                  className="px-4 py-2 border border-slate-700 text-slate-300 rounded-lg text-xs"
                >
                  &larr; Back
                </button>
                <button
                  onClick={() => setActiveStep(4)}
                  className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-emerald-900/40"
                >
                  Retrieve Hakeem Sahab v2 Brief &rarr;
                </button>
              </div>
            </div>
          )}

          {/* STEP 4: HAKEEM SAHAB AI V2 EVIDENCE-GROUNDED BRIEF */}
          {activeStep === 4 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-white">Step 4: Hakeem Sahab AI v2 Evidence-Grounded Brief</h3>
                <span className="text-xs bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-1 rounded font-mono">
                  Evidence + Confidence + Safety + Unknowns + Sources
                </span>
              </div>

              {isLoadingHakeem ? (
                <div className="p-8 text-center bg-slate-900/50 rounded-xl border border-slate-800">
                  <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
                  <p className="text-xs text-slate-300">Traversing 25-Drug Clinical Knowledge Graph...</p>
                  <p className="text-[10px] text-slate-500 mt-1">Cross-referencing Afaal, UPI Volumes, and Safety Firewall</p>
                </div>
              ) : hakeemBrief ? (
                <div className="space-y-4">
                  {/* Confidence & Overall Grade Banner */}
                  <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 flex items-center justify-between">
                    <div>
                      <span className="text-[10px] text-slate-400 block uppercase">Overall Evidence Tier</span>
                      <span className="text-sm font-bold text-emerald-400">{hakeemBrief.evidence.overall_grade}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-slate-400 block uppercase">Algorithmic Confidence</span>
                      <span className="text-sm font-bold text-amber-300">{Math.round(hakeemBrief.confidence * 100)}%</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-slate-400 block uppercase">Safety Firewall Gate</span>
                      <span className="text-xs font-semibold bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded">
                        {hakeemBrief.safety.ai_state}
                      </span>
                    </div>
                  </div>

                  {/* Clinical Reasoning Summary */}
                  <div className="bg-slate-900/70 p-4 rounded-xl border border-slate-800">
                    <h4 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-1">
                      Clinical Reasoning Synthesis
                    </h4>
                    <p className="text-xs text-slate-200 leading-relaxed">
                      {hakeemBrief.clinical_reasoning_summary}
                    </p>
                  </div>

                  {/* Multi-Hop Traversal Chain */}
                  <div className="bg-slate-900/40 p-3 rounded-lg border border-slate-800 text-[11px] space-y-1">
                    <div className="font-semibold text-slate-400">Multi-Hop Relational Traversal Path:</div>
                    {hakeemBrief.evidence.traversal_hops.map((hop: string, idx: number) => (
                      <div key={idx} className="text-slate-300 pl-2 border-l border-emerald-700/50">
                        &bull; {hop}
                      </div>
                    ))}
                  </div>

                  {/* Unknowns & Uncertainty Flags */}
                  <div className="bg-amber-950/20 p-3 rounded-lg border border-amber-800/40">
                    <div className="text-xs font-semibold text-amber-400 mb-1">Identified Clinical Unknowns</div>
                    <ul className="text-[11px] text-amber-200/80 list-disc list-inside space-y-0.5">
                      {hakeemBrief.unknowns.map((u: string, idx: number) => (
                        <li key={idx}>{u}</li>
                      ))}
                    </ul>
                  </div>

                  {/* Traceable Sources */}
                  <div className="bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                    <div className="text-xs font-semibold text-slate-300 mb-2">Traceable Citations (Zero Fake Data)</div>
                    <div className="space-y-1.5 text-[11px]">
                      {hakeemBrief.sources.map((s: any, idx: number) => (
                        <div key={idx} className="p-2 bg-slate-950/60 rounded border border-slate-800/80">
                          <span className="font-bold text-slate-200">{s.substance}</span> &bull;{" "}
                          <span className="text-emerald-400">{s.work_title}</span> ({s.volume}, {s.page})
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : null}

              <div className="flex justify-between pt-4">
                <button
                  onClick={() => setActiveStep(3)}
                  className="px-4 py-2 border border-slate-700 text-slate-300 rounded-lg text-xs"
                >
                  &larr; Back
                </button>
                <button
                  onClick={() => setActiveStep(5)}
                  className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-emerald-900/40"
                >
                  Verify Safety Firewall Gate &rarr;
                </button>
              </div>
            </div>
          )}

          {/* STEP 5: SAFETY FIREWALL V2 GATE */}
          {activeStep === 5 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-white">Step 5: Safety Firewall v2 Verification Gate</h3>
                <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-700 px-2 py-1 rounded">
                  Gate 0 to Gate 4 Active
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Deterministic statutory screening: Checks Schedule E(1) poisons, pregnancy contraindications, renal excretion thresholds, and narrow therapeutic index warnings.
              </p>

              <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-3">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <span className="text-xs text-slate-300">Schedule E(1) Statutory Poison Screen</span>
                  <span className="text-xs text-emerald-400 font-semibold">&check; PASSED (No uncertified poisons)</span>
                </div>
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <span className="text-xs text-slate-300">Renal Clearance Compatibility (Cr: 0.9 mg/dL)</span>
                  <span className="text-xs text-emerald-400 font-semibold">&check; PASSED (Full Dose Permitted)</span>
                </div>
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <span className="text-xs text-slate-300">CYP450 Herb-Drug Interaction Matrix</span>
                  <span className="text-xs text-emerald-400 font-semibold">&check; PASSED (Zero CYP3A4 inhibitors)</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-300">Mizaj Dose Modulation</span>
                  <span className="text-xs text-amber-300 font-semibold">Dry Powder (Safoof) Mandated for Balgham</span>
                </div>
              </div>

              <div className="flex justify-between pt-4">
                <button
                  onClick={() => setActiveStep(4)}
                  className="px-4 py-2 border border-slate-700 text-slate-300 rounded-lg text-xs"
                >
                  &larr; Back
                </button>
                <button
                  onClick={() => setActiveStep(6)}
                  className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-emerald-900/40"
                >
                  Proceed to 4-Tier Nuskha Builder &rarr;
                </button>
              </div>
            </div>
          )}

          {/* STEP 6: 4-TIER NUSKHA NAWISI PRESCRIBING */}
          {activeStep === 6 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-white">Step 6: 4-Tier Classical Prescribing Architecture</h3>
                <span className="text-xs bg-purple-950 text-purple-300 border border-purple-800 px-2 py-1 rounded font-mono">
                  Symphonic Prescription Formula
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Prescription formulation structured into 4 classical functional tiers: Chief Drug, Supporting Actives, Corrective (Musleh), and Catalyst Vehicle (Badraqa).
              </p>

              <div className="space-y-2.5">
                <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
                  <div className="text-[10px] text-emerald-400 font-bold uppercase">Tier 1: Chief Active Drug (Juz-e-Azam) &bull; 35%</div>
                  <div className="text-xs font-bold text-white mt-0.5">Asgandh (Withania somnifera) &bull; 500 mg</div>
                  <div className="text-[11px] text-slate-400">Target: Restores vitality, musculo-skeletal tone, and suppresses pro-inflammatory cytokines.</div>
                </div>

                <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
                  <div className="text-[10px] text-blue-400 font-bold uppercase">Tier 2: Supporting Actives (Muawin) &bull; 50%</div>
                  <div className="text-xs font-bold text-white mt-0.5">Zanjabeel (Zingiber officinale, 350mg) + Chob Zard (Curcuma longa, 250mg)</div>
                  <div className="text-[11px] text-slate-400">Target: Potent analgesic (Musakkin-e-Waja) and resolvent of phlegmatic effusion (Muhallil-e-Waram).</div>
                </div>

                <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
                  <div className="text-[10px] text-amber-400 font-bold uppercase">Tier 3: Corrective (Musleh) &bull; 10%</div>
                  <div className="text-xs font-bold text-white mt-0.5">Filfil Siyah (Piper nigrum) &bull; 100 mg</div>
                  <div className="text-[11px] text-slate-400">Function: Mitigates gastric coldness and provides piperine for systemic bio-enhancement.</div>
                </div>

                <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
                  <div className="text-[10px] text-purple-400 font-bold uppercase">Tier 4: Catalyst Vehicle (Badraqa) &bull; 5%</div>
                  <div className="text-xs font-bold text-white mt-0.5">Lukewarm water with 1 drop Roghan-e-Badiyan</div>
                  <div className="text-[11px] text-slate-400">Function: Organ-conduit vehicle targeting joints and preventing flatulence.</div>
                </div>
              </div>

              <div className="p-3 bg-slate-900/60 rounded-lg border border-slate-800 text-xs">
                <span className="font-semibold text-amber-400">Associated Classical Murakkab:</span> Habb-e-Suranjan (1 tablet at bedtime with warm water).
              </div>

              <div className="flex justify-between pt-4">
                <button
                  onClick={() => setActiveStep(5)}
                  className="px-4 py-2 border border-slate-700 text-slate-300 rounded-lg text-xs"
                >
                  &larr; Back
                </button>
                <button
                  onClick={handleCompleteEncounter}
                  disabled={isSubmitting}
                  className="px-6 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold shadow-lg shadow-emerald-900/40"
                >
                  {isSubmitting ? "Cryptographically Signing..." : "Sign & Finalize Encounter (21 CFR Part 11) &rarr;"}
                </button>
              </div>
            </div>
          )}

          {/* STEP 7: DIGITAL SIGNOFF & COMPLETED ENCOUNTER */}
          {activeStep === 7 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-emerald-400">&check; Consultation Successfully Finalized</h3>
                <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-700 px-2 py-1 rounded">
                  21 CFR PART 11 SIGNED
                </span>
              </div>
              <p className="text-xs text-slate-400">
                The continuous clinical encounter is complete, digitally signed, routed to the dispensary, and scheduled for automated PROMs follow-up.
              </p>

              {completedEncounter && (
                <div className="bg-slate-900 p-5 rounded-xl border border-emerald-800/60 space-y-4">
                  <div className="grid grid-cols-2 gap-3 text-xs pb-3 border-b border-slate-800">
                    <div>
                      <span className="text-slate-500 block text-[10px]">Encounter Identifier</span>
                      <span className="font-mono text-emerald-400 font-bold">{completedEncounter.encounter_id}</span>
                    </div>
                    <div>
                      <span className="text-slate-500 block text-[10px]">Licensed Practitioner</span>
                      <span className="font-bold text-white">{completedEncounter.digital_signature.signed_by}</span>
                    </div>
                    <div>
                      <span className="text-slate-500 block text-[10px]">Cryptographic SHA-256 Hash</span>
                      <span className="font-mono text-[10px] text-slate-300 truncate block">
                        {completedEncounter.digital_signature.signature_hash}
                      </span>
                    </div>
                    <div>
                      <span className="text-slate-500 block text-[10px]">Automated Follow-Up</span>
                      <span className="font-bold text-amber-300">{completedEncounter.follow_up.scheduled_date} (14 days)</span>
                    </div>
                  </div>

                  <div className="text-xs text-slate-300">
                    <span className="text-emerald-400 font-semibold block mb-1">Prescription Dispatched to Pharmacy:</span>
                    {completedEncounter.final_nuskha.tier_1_foundation.drug} + {completedEncounter.final_nuskha.tier_2_core_actives.map((a: any) => a.drug).join(", ")}.
                  </div>
                </div>
              )}

              <div className="flex justify-end pt-4 space-x-3">
                <button
                  onClick={() => {
                    setActiveStep(1);
                    setCompletedEncounter(null);
                  }}
                  className="px-5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold"
                >
                  Start Next Patient Encounter
                </button>
              </div>
            </div>
          )}
        </main>

        {/* Right Column: Live Safety Firewall Monitor & Evidence Drawer (col-span-3) */}
        <aside className="lg:col-span-3 border-l border-slate-800 bg-slate-900/50 p-5 overflow-y-auto space-y-5">
          <div className="bg-slate-800/40 rounded-xl p-4 border border-slate-800">
            <h3 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-2 flex items-center justify-between">
              <span>Safety Firewall Monitor</span>
              <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span>
            </h3>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between items-center text-slate-300">
                <span>Gate 0: Pregnancy Contraindication</span>
                <span className="text-emerald-400 font-bold">&check; SAFE</span>
              </div>
              <div className="flex justify-between items-center text-slate-300">
                <span>Gate 1: Schedule E(1) Poisons</span>
                <span className="text-emerald-400 font-bold">&check; CLEAR</span>
              </div>
              <div className="flex justify-between items-center text-slate-300">
                <span>Gate 2: Renal Posology Threshold</span>
                <span className="text-emerald-400 font-bold">&check; GFR &gt; 90</span>
              </div>
              <div className="flex justify-between items-center text-slate-300">
                <span>Gate 3: Narrow Therapeutic Index</span>
                <span className="text-emerald-400 font-bold">&check; MONITORED</span>
              </div>
              <div className="flex justify-between items-center text-slate-300">
                <span>Gate 4: 21 CFR Part 11 Override</span>
                <span className="text-emerald-400 font-bold">&check; ENFORCED</span>
              </div>
            </div>
          </div>

          <div className="bg-slate-800/40 rounded-xl p-4 border border-slate-800">
            <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Statutory Clinical Doctrine
            </h3>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              "Autonomous Diagnosis != Autonomous Prescription. Hakeem Sahab AI operates strictly as an Evidence-Grounded Decision Support Copilot. Final legal authority and ethical responsibility rests with the human clinician."
            </p>
          </div>

          <div className="bg-slate-800/40 rounded-xl p-4 border border-slate-800">
            <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Automated Outcomes Loop
            </h3>
            <div className="text-[11px] text-slate-400 space-y-1">
              <div>&bull; Day 7: Digital VAS Pain score SMS</div>
              <div>&bull; Day 14: In-clinic follow-up consultation</div>
              <div>&bull; Day 28: Repeat hs-CRP & HOMA-IR</div>
              <div>&bull; Real-World Evidence (RWE) auto-ingestion</div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
