"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";

interface PracticumCase {
  id: string;
  patientInitials: string;
  clinicalTrack: string;
  mizajAssessment: string;
  axisIdentification: string;
  severityClassification: string;
  phaseProtocol: string;
  productStack: string;
  labMonitoringPlan: string;
  predictedOutcome: string;
  status: "ACCEPTED" | "REJECTED";
  score: number;
}

const SAMPLE_CASES: PracticumCase[] = [
  {
    id: "CASE-01",
    patientInitials: "A.S. (34M)",
    clinicalTrack: "Male Infertility",
    mizajAssessment: "Balghami dominant (16/18), Sauda overlay (12/18). Barid-Ratab with cold extremities.",
    axisIdentification: "Liver-Testicular Axis (Primary) + Gut-Liver Axis (Secondary). Baseline ALT 54, Total T 287.",
    severityClassification: "Grade 2 Moderate oligospermia (3.2M/mL, motility 14%, DFI 44%).",
    phaseProtocol: "Phase 1: LiverPrime Core (4 wks) -> Phase 2: ManiVital Pro + CoQ10 300mg (12 wks) -> Phase 3: Taper.",
    productStack: "LiverPrime Core 2 caps BD, ManiVital Pro 4 caps BD, CoQ10 Ubiquinol 300mg, Zinc 30mg, Selenium 200mcg.",
    labMonitoringPlan: "SGPT at 4 weeks. Semen analysis at 12 weeks (74-day spermatogenesis cycle).",
    predictedOutcome: "+40-60% motility improvement and DFI reduction <30% at 12 weeks.",
    status: "ACCEPTED",
    score: 95
  },
  {
    id: "CASE-02",
    patientInitials: "S.R. (29F)",
    clinicalTrack: "PCOS / Female Fertility",
    mizajAssessment: "Balghami-IR (17/18). Soft adiposity, cold preference, history of sluggish digestion.",
    axisIdentification: "Gut-Ovarian (Primary) + Liver-Pancreas (Secondary). LH:FSH 3.5:1, Fasting Insulin 28.4.",
    severityClassification: "Grade 2 Moderate PCOS with anovulatory cycles (6 months amenorrhoea).",
    phaseProtocol: "Phase 1: Triphala 3g + Methi 2g + Chiraita 1g (4 wks) -> Phase 2: OvaSync + MetaboCore Elite (12 wks).",
    productStack: "OvaSync (Myo-Inositol 2g + Vitex), MetaboCore Elite (Berberine 1g BD), D3 4000 IU.",
    labMonitoringPlan: "LH:FSH and fasting insulin at 8 weeks. AMH trend and pelvic USG at 12 weeks.",
    predictedOutcome: "Restoration of natural ovulatory cycle within 90 days with LH:FSH moving towards 1.5:1.",
    status: "ACCEPTED",
    score: 100
  }
];

export default function PracticumDashboardPage() {
  const [cases, setCases] = useState<PracticumCase[]>(SAMPLE_CASES);
  const [showNewModal, setShowNewModal] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);

  // Form State
  const [track, setTrack] = useState("Male Infertility");
  const [initials, setInitials] = useState("");
  const [mizaj, setMizaj] = useState("");
  const [axis, setAxis] = useState("");
  const [severity, setSeverity] = useState("");
  const [phaseProto, setPhaseProto] = useState("");
  const [products, setProducts] = useState("");
  const [labs, setLabs] = useState("");
  const [outcome, setOutcome] = useState("");

  const handleSubmitCase = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Strict Table 6.2 Validation
    const missingFatal: string[] = [];
    if (!mizaj.trim()) missingFatal.push("Element 1: Mizaj Assessment");
    if (!axis.trim()) missingFatal.push("Element 2: Axis Identification");
    if (!phaseProto.trim()) missingFatal.push("Element 4: Phase Protocol");

    if (missingFatal.length > 0) {
      alert(`Case REJECTED! Missing mandatory elements:\n${missingFatal.join("\n")}\nPer Section 6.5, missing Elements 1, 2, or 4 cause outright rejection.`);
      return;
    }

    let calculatedScore = 100;
    if (!severity.trim()) calculatedScore -= 5;
    if (!products.trim()) calculatedScore -= 10;
    if (!labs.trim()) calculatedScore -= 5;
    if (!outcome.trim()) calculatedScore -= 5;

    const newCase: PracticumCase = {
      id: `CASE-0${cases.length + 1}`,
      patientInitials: initials || "Anonymous Patient",
      clinicalTrack: track,
      mizajAssessment: mizaj,
      axisIdentification: axis,
      severityClassification: severity,
      phaseProtocol: phaseProto,
      productStack: products,
      labMonitoringPlan: labs,
      predictedOutcome: outcome,
      status: "ACCEPTED",
      score: calculatedScore
    };

    setCases([...cases, newCase]);
    setShowNewModal(false);
    setNotice(`Case ${newCase.id} successfully validated and registered! Score: ${calculatedScore}/100.`);
    setTimeout(() => setNotice(null), 5000);

    // Reset
    setInitials("");
    setMizaj("");
    setAxis("");
    setSeverity("");
    setPhaseProto("");
    setProducts("");
    setLabs("");
    setOutcome("");
  };

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-7xl mx-auto pb-16">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-2xl">🎓</span>
              <h1 className="text-xl font-bold text-white tracking-tight">
                CP-AFUM Practicum Case Registry
              </h1>
              <span className="px-2.5 py-0.5 rounded-full bg-teal-500/15 border border-teal-500/30 text-teal-300 text-xs font-mono font-bold">
                20 Supervised Cases
              </span>
            </div>
            <p className="text-xs text-[var(--muted)] mt-1">
              Module 6 Portfolio: Documenting clinical reasoning across all 7 mandatory case elements for Dr. Irfan Ashraf certification.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowNewModal(true)}
              className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shadow-md transition flex items-center gap-1.5"
            >
              <span>➕ Submit New Case</span>
            </button>
            <Link
              href="/academy/cp-afum"
              className="px-3.5 py-2 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-teal-300 font-semibold text-xs border border-[var(--border)] transition"
            >
              📚 LMS Curriculum →
            </Link>
          </div>
        </div>

        {notice && (
          <div className="p-3.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs flex items-center justify-between shadow-md animate-fadeIn">
            <span>✓ {notice}</span>
            <button onClick={() => setNotice(null)} className="text-slate-400 hover:text-white font-bold ml-4">✕</button>
          </div>
        )}

        {/* 20-Case Portfolio Progress Tracker */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          {[
            { track: "Male Infertility", target: 5, current: cases.filter(c => c.clinicalTrack === "Male Infertility").length },
            { track: "PCOS / Fertility", target: 5, current: cases.filter(c => c.clinicalTrack.includes("PCOS")).length },
            { track: "T2DM / Metabolic", target: 4, current: cases.filter(c => c.clinicalTrack.includes("Metabolic")).length },
            { track: "Thyroid Axis", target: 3, current: cases.filter(c => c.clinicalTrack.includes("Thyroid")).length },
            { track: "Anxiety / Stress", target: 3, current: cases.filter(c => c.clinicalTrack.includes("Anxiety")).length },
          ].map((item, idx) => (
            <div key={idx} className="p-3.5 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-1.5 shadow-sm">
              <div className="flex justify-between text-[11px] text-slate-400">
                <span>{item.track}</span>
                <span className="font-mono font-bold text-white">{item.current}/{item.target}</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <div
                  className="bg-teal-500 h-full rounded-full transition-all"
                  style={{ width: `${Math.min((item.current / item.target) * 100, 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Viva Voce Gate Card */}
        <div className="p-4 rounded-2xl bg-gradient-to-r from-amber-950/30 via-slate-900 to-teal-950/30 border border-amber-500/30 text-xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
              <span>⚖️</span> Week 24 Final Clinical Viva Requirements
            </span>
            <span className="px-2 py-0.5 rounded bg-amber-900/40 text-amber-300 font-mono text-[10px]">
              20-Min Oral Exam
            </span>
          </div>
          <p className="text-slate-300 leading-relaxed">
            Candidates must present 2 randomly selected cases from this portfolio to <strong>Dr. Irfan Ashraf</strong>. Must defend: (1) Mizaj assessment rationale, (2) Axis mapping with lab proof, (3) 8 Phase trigger rules application, (4) Mandatory Red Flag exclusion. <em>No viva clearance = No CP-AFUM certificate.</em>
          </p>
        </div>

        {/* Registered Cases Table */}
        <div className="p-5 rounded-3xl bg-[var(--panel)] border border-[var(--border)] shadow-xl space-y-4">
          <div className="flex justify-between items-center px-1">
            <h3 className="text-sm font-bold text-white">Registered Practicum Cases ({cases.length})</h3>
            <span className="text-xs text-teal-400 font-mono">Passing Grade: ≥70% Average</span>
          </div>

          <div className="space-y-3">
            {cases.map((c) => (
              <div key={c.id} className="p-4 rounded-2xl bg-[var(--background)] border border-slate-800 space-y-3">
                <div className="flex justify-between items-start">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded-md bg-teal-950/60 border border-teal-700/40 text-teal-300 font-mono text-xs font-bold">
                      {c.id}
                    </span>
                    <span className="text-sm font-bold text-white">{c.patientInitials}</span>
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300 font-medium">
                      {c.clinicalTrack}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-950/40 border border-emerald-700/40 px-2 py-0.5 rounded">
                      Score: {c.score}/100
                    </span>
                    <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-bold">
                      {c.status}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] text-slate-300">
                  <div className="p-2.5 rounded-xl bg-[var(--panel)] border border-slate-800/80">
                    <strong className="text-teal-400 block text-[10px] uppercase">1. Mizaj Assessment</strong>
                    {c.mizajAssessment}
                  </div>
                  <div className="p-2.5 rounded-xl bg-[var(--panel)] border border-slate-800/80">
                    <strong className="text-teal-400 block text-[10px] uppercase">2. Axis & Lab Evidence</strong>
                    {c.axisIdentification}
                  </div>
                  <div className="p-2.5 rounded-xl bg-[var(--panel)] border border-slate-800/80">
                    <strong className="text-amber-400 block text-[10px] uppercase">4. 3-Phase Protocol</strong>
                    {c.phaseProtocol}
                  </div>
                  <div className="p-2.5 rounded-xl bg-[var(--panel)] border border-slate-800/80">
                    <strong className="text-cyan-400 block text-[10px] uppercase">6. Monitoring & Outcome</strong>
                    {c.predictedOutcome}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Modal for Case Submission */}
        {showNewModal && (
          <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-xs flex items-center justify-center p-4">
            <div className="bg-[var(--panel)] border border-teal-500/40 rounded-3xl max-w-2xl w-full p-6 space-y-4 max-h-[90vh] overflow-y-auto shadow-2xl">
              <div className="flex justify-between items-center border-b border-[var(--border)] pb-3">
                <h3 className="text-base font-bold text-white">Log Practicum Case (7 Mandatory Elements)</h3>
                <button onClick={() => setShowNewModal(false)} className="text-slate-400 hover:text-white font-bold">✕</button>
              </div>

              <form onSubmit={handleSubmitCase} className="space-y-3 text-xs">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="text-[11px] font-bold text-slate-300 block mb-1">Patient Initials / Age</label>
                    <input
                      required
                      value={initials}
                      onChange={(e) => setInitials(e.target.value)}
                      placeholder="e.g. M.K. (36M)"
                      className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                    />
                  </div>
                  <div>
                    <label className="text-[11px] font-bold text-slate-300 block mb-1">Clinical Track</label>
                    <select
                      value={track}
                      onChange={(e) => setTrack(e.target.value)}
                      className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                    >
                      <option>Male Infertility</option>
                      <option>PCOS / Female Fertility</option>
                      <option>Type 2 Diabetes / Metabolic</option>
                      <option>Thyroid (Hypo + Subclinical)</option>
                      <option>Anxiety / Stress / IBS</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="text-[11px] font-bold text-teal-300 block mb-1">
                    1. Mizaj Assessment (FATAL: Missing = Case Rejected)
                  </label>
                  <textarea
                    required
                    rows={2}
                    value={mizaj}
                    onChange={(e) => setMizaj(e.target.value)}
                    placeholder="Document dominant Mizaj, 8-domain scoring rationale, and Mixed Mizaj notes..."
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  />
                </div>

                <div>
                  <label className="text-[11px] font-bold text-teal-300 block mb-1">
                    2. Axis Identification (FATAL: Missing = Case Rejected)
                  </label>
                  <textarea
                    required
                    rows={2}
                    value={axis}
                    onChange={(e) => setAxis(e.target.value)}
                    placeholder="Document primary axis, secondary axis, and supporting lab values with collection dates..."
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  />
                </div>

                <div>
                  <label className="text-[11px] font-bold text-slate-300 block mb-1">
                    3. Severity Classification (-5 marks if missing)
                  </label>
                  <input
                    value={severity}
                    onChange={(e) => setSeverity(e.target.value)}
                    placeholder="e.g. Grade 2 Moderate (HOMA-IR 3.4, SGPT 52)"
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  />
                </div>

                <div>
                  <label className="text-[11px] font-bold text-teal-300 block mb-1">
                    4. Phase Protocol (FATAL: Missing = Case Rejected)
                  </label>
                  <textarea
                    required
                    rows={2}
                    value={phaseProto}
                    onChange={(e) => setPhaseProto(e.target.value)}
                    placeholder="Phase 1 (duration/rationale) + Phase 2 (hero product) + Phase 3 (taper)..."
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  />
                </div>

                <div>
                  <label className="text-[11px] font-bold text-slate-300 block mb-1">
                    5. Product Stack with Mizaj Adjustments (-10 marks if missing)
                  </label>
                  <input
                    value={products}
                    onChange={(e) => setProducts(e.target.value)}
                    placeholder="Document specific products, exact milligrams, and thermal dose adjustments..."
                    className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="text-[11px] font-bold text-slate-300 block mb-1">
                      6. Lab Monitoring Plan (-5 marks)
                    </label>
                    <input
                      value={labs}
                      onChange={(e) => setLabs(e.target.value)}
                      placeholder="Labs at Week 4, 8, 12..."
                      className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                    />
                  </div>
                  <div>
                    <label className="text-[11px] font-bold text-slate-300 block mb-1">
                      7. Predicted 12-Week Outcome (-5 marks)
                    </label>
                    <input
                      value={outcome}
                      onChange={(e) => setOutcome(e.target.value)}
                      placeholder="Expected lab & clinical target..."
                      className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl p-2.5 text-white"
                    />
                  </div>
                </div>

                <div className="pt-3 flex justify-end gap-2 border-t border-[var(--border)]">
                  <button
                    type="button"
                    onClick={() => setShowNewModal(false)}
                    className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 font-medium text-xs"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shadow-md"
                  >
                    Submit for Validation
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
