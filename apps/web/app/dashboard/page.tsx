"use client";

import React, { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import type { TokenResponse } from "@/lib/identityApi";
import { clearSession, loadSession } from "@/lib/session";
import {
  clinicalApi,
  type PatientRecord,
  type TimelineEvent,
  type MizajAssessmentRecord,
  type DifferentialDiagnosis,
} from "@/lib/clinicalApi";
import { therapeuticApi, type TadbeerPlanOut, type NuskhaDraftOut } from "@/lib/therapeuticApi";
import { knowledgeApi, type MufradMonograph, type ScheduleE1Substance } from "@/lib/knowledgeApi";
import { PatientTimeline } from "@/components/PatientTimeline";
import { NuskhaBuilder } from "@/components/NuskhaBuilder";
import { HakeemReviewDrawer } from "@/components/HakeemReviewDrawer";
import { MizajAssessmentModal } from "@/components/MizajAssessmentModal";
import { DigitalTwinCockpit } from "@/components/DigitalTwinCockpit";
import { AmbientScribeGovernanceCockpit } from "@/components/AmbientScribeGovernanceCockpit";
import { MultimodalLabCockpit } from "@/components/MultimodalLabCockpit";
import { GovernanceBoardCockpit } from "@/components/GovernanceBoardCockpit";
import { PatientPortalCockpit } from "@/components/PatientPortalCockpit";
import { TaskPipelineCockpit } from "@/components/TaskPipelineCockpit";
import { GlobalCommandPalette } from "@/components/GlobalCommandPalette";

type ActiveTab =
  | "timeline"
  | "nuskha"
  | "tadbeer"
  | "pharmacopoeia"
  | "digital_twin"
  | "ambient_scribe"
  | "multimodal_lab"
  | "governance_board"
  | "patient_portal"
  | "task_pipelines";


const TADBEER_REGIMENS = [
  { name: "Hijama (Wet / Dry Cupping)", category: "regimen", indication: "Local blood stasis, Tanqiya-e-Dam" },
  { name: "Fasd (Venesection)", category: "regimen", indication: "Ghalba-e-Dam (blood plethora)" },
  { name: "Dalak (Therapeutic Massage)", category: "massage", indication: "Rikhavat, muscular rigidity" },
  { name: "Hammam (Therapeutic Bathing)", category: "bathing", indication: "Su-e-Mizaj Yabis, relaxation" },
  { name: "Qai (Therapeutic Emesis)", category: "regimen", indication: "Tanqiya of upper GI corrupt humors" },
  { name: "Ishaal (Therapeutic Purgation)", category: "regimen", indication: "Istifragh of morbid humors via gut" },
  { name: "Huqna (Enema)", category: "regimen", indication: "Colonic evacuation, Qoolanj" },
  { name: "Natool (Irrigation / Douching)", category: "regimen", indication: "Local cephalic or articular heat" },
];

export default function ClinicDeskDashboard() {
  const router = useRouter();
  const [session, setSession] = useState<TokenResponse | null>(null);
  const [checked, setChecked] = useState(false);

  // Active Tab
  const [activeTab, setActiveTab] = useState<ActiveTab>("timeline");

  // Patients state
  const [patients, setPatients] = useState<PatientRecord[]>([]);
  const [selectedPatient, setSelectedPatient] = useState<PatientRecord | null>(null);
  const [isLoadingPatients, setIsLoadingPatients] = useState(true);
  const [patientSearch, setPatientSearch] = useState("");

  // Timeline state
  const [timelineEvents, setTimelineEvents] = useState<TimelineEvent[]>([]);
  const [isLoadingTimeline, setIsLoadingTimeline] = useState(false);

  // Tadbeer state
  const [tadbeerPlans, setTadbeerPlans] = useState<TadbeerPlanOut[]>([]);
  const [isLoadingTadbeer, setIsLoadingTadbeer] = useState(false);
  const [showAddTadbeerModal, setShowAddTadbeerModal] = useState(false);
  const [newTadbeerName, setNewTadbeerName] = useState(TADBEER_REGIMENS[0].name);
  const [newTadbeerIndication, setNewTadbeerIndication] = useState(TADBEER_REGIMENS[0].indication);
  const [newTadbeerFrequency, setNewTadbeerFrequency] = useState("Weekly for 3 sessions");
  const [newTadbeerDuration, setNewTadbeerDuration] = useState("20 minutes per session");
  const [newTadbeerCategory, setNewTadbeerCategory] = useState<
    "regimen" | "rest" | "physical_activity" | "massage" | "bathing" | "other"
  >("regimen");
  const [isSubmittingTadbeer, setIsSubmittingTadbeer] = useState(false);

  // Pharmacopoeia state
  const [upiMonographs, setUpiMonographs] = useState<MufradMonograph[]>([]);
  const [scheduleE1List, setScheduleE1List] = useState<ScheduleE1Substance[]>([]);
  const [pharmaSearch, setPharmaSearch] = useState("");
  const [isLoadingPharma, setIsLoadingPharma] = useState(false);

  // Hakeem Drawer state
  const [isHakeemDrawerOpen, setIsHakeemDrawerOpen] = useState(false);

  // Mizaj & Diagnostic State
  const [mizajAssessment, setMizajAssessment] = useState<MizajAssessmentRecord | null>(null);
  const [showMizajModal, setShowMizajModal] = useState(false);
  const [differentials, setDifferentials] = useState<DifferentialDiagnosis[]>([]);
  const [diffComplaint, setDiffComplaint] = useState("");
  const [isEvaluatingDiff, setIsEvaluatingDiff] = useState(false);

  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);

  // Global Cmd+K keyboard shortcut listener
  useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setIsCommandPaletteOpen((prev) => !prev);
      }
    };
    window.addEventListener("keydown", handleGlobalKeyDown);
    return () => window.removeEventListener("keydown", handleGlobalKeyDown);
  }, []);

  // Load session
  useEffect(() => {
    const existing = loadSession();
    if (!existing) {
      router.push("/");
      return;
    }
    setSession(existing);
    setChecked(true);
  }, [router]);

  // Fetch patients once session is verified
  const loadPatients = useCallback(async () => {
    if (!session) return;
    try {
      setIsLoadingPatients(true);
      const res = await clinicalApi.listPatients(session.access_token);
      setPatients(res || []);
      if (res && res.length > 0 && !selectedPatient) {
        setSelectedPatient(res[0]);
      }
    } catch {
      // ignore
    } finally {
      setIsLoadingPatients(false);
    }
  }, [session, selectedPatient]);

  useEffect(() => {
    if (session) {
      loadPatients();
    }
  }, [session, loadPatients]);

  // Load patient timeline and tadbeer when selectedPatient changes
  useEffect(() => {
    if (!session || !selectedPatient) return;

    // Load timeline
    setIsLoadingTimeline(true);
    clinicalApi
      .getTimeline(session.access_token, selectedPatient.id)
      .then((events) => setTimelineEvents(events || []))
      .catch(() => setTimelineEvents([]))
      .finally(() => setIsLoadingTimeline(false));

    // Load Tadbeer plans
    setIsLoadingTadbeer(true);
    therapeuticApi
      .listTadbeerPlansForPatient(session.access_token, selectedPatient.id)
      .then((plans) => setTadbeerPlans(plans || []))
      .catch(() => setTadbeerPlans([]))
      .finally(() => setIsLoadingTadbeer(false));

    // Load latest Mizaj assessment
    clinicalApi
      .getLatestMizajAssessment(session.access_token, selectedPatient.id)
      .then((rec) => setMizajAssessment(rec))
      .catch(() => setMizajAssessment(null));
  }, [session, selectedPatient]);

  // Load Pharmacopoeia when tab is selected
  useEffect(() => {
    if (activeTab === "pharmacopoeia" && session && upiMonographs.length === 0) {
      setIsLoadingPharma(true);
      Promise.all([
        knowledgeApi.listMonographs(session.access_token),
        knowledgeApi.listScheduleE1(session.access_token),
      ])
        .then(([monos, e1]) => {
          setUpiMonographs(monos || []);
          setScheduleE1List(e1 || []);
        })
        .catch(() => {})
        .finally(() => setIsLoadingPharma(false));
    }
  }, [activeTab, session, upiMonographs.length]);

  if (!checked || !session) return null;

  function handleLogout() {
    clearSession();
    router.push("/");
  }

  // Create Tadbeer Plan
  const handleCreateTadbeer = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session || !selectedPatient) return;
    try {
      setIsSubmittingTadbeer(true);
      const res = await therapeuticApi.createTadbeerPlan(session.access_token, {
        patient_id: selectedPatient.id,
        encounter_id: "00000000-0000-0000-0000-000000000000",
        name: newTadbeerName,
        category: newTadbeerCategory,
        indication: newTadbeerIndication,
        frequency: newTadbeerFrequency,
        duration: newTadbeerDuration,
        patient_safety_context: {
          pregnancy_status: selectedPatient.pregnancy_status,
          comorbidities: selectedPatient.comorbidities,
        },
      });
      setTadbeerPlans((prev) => [res, ...prev]);
      setShowAddTadbeerModal(false);
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : "Failed to create Tadbeer plan");
    } finally {
      setIsSubmittingTadbeer(false);
    }
  };

  // Evaluate Differential Diagnoses
  const handleEvaluateDifferential = async (complaintText?: string) => {
    const query = complaintText !== undefined ? complaintText : diffComplaint;
    if (!session || !query.trim()) return;
    try {
      setIsEvaluatingDiff(true);
      if (complaintText !== undefined) {
        setDiffComplaint(complaintText);
      }
      const res = await clinicalApi.getDifferentialDiagnoses(session.access_token, query);
      setDifferentials(res || []);
    } catch {
      setDifferentials([]);
    } finally {
      setIsEvaluatingDiff(false);
    }
  };

  // Filtered patients
  const filteredPatients = patients.filter((p) => {
    const q = patientSearch.toLowerCase();
    return (
      p.first_name.toLowerCase().includes(q) ||
      p.last_name.toLowerCase().includes(q) ||
      p.mrn.toLowerCase().includes(q)
    );
  });

  // Calculate selected patient age
  const patientAge = selectedPatient?.date_of_birth
    ? Math.abs(
        new Date(
          Date.now() - new Date(selectedPatient.date_of_birth).getTime()
        ).getUTCFullYear() - 1970
      )
    : 30;

  return (
    <div className="min-h-screen flex flex-col bg-[#0b0f0d] text-[#ece8dd]">
      {/* Screen Reader Live Region (WCAG 2.1 AA) */}
      <div
        id="zv-a11y-announcer"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        Active Tab: {activeTab}. Selected Patient: {selectedPatient ? `${selectedPatient.first_name} ${selectedPatient.last_name}` : "None"}.
      </div>

      {/* Top Navigation Bar */}
      <header className="px-6 py-3.5 border-b border-[#24302a] bg-[#121712] flex items-center justify-between sticky top-0 z-30 shadow-md">
        <div className="flex items-center gap-4">
          <div>
            <h1 className="zv-brand-title text-lg leading-tight font-serif">ZAYVORA HEALTH™</h1>
            <p className="text-[11px] text-[#8a9490] font-sans">
              Clinic Desk 2.0 · {session.organization.name}
            </p>
          </div>
          <span className="hidden sm:inline-block h-5 w-px bg-[#24302a]" />
          <div className="hidden sm:flex items-center gap-2 text-xs text-[#8a9490]">
            <span>Clinician:</span>
            <strong className="text-[#ece8dd] font-medium">{session.user.full_name}</strong>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setIsCommandPaletteOpen(true)}
            className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-[#1a231d] border border-[#2ea87f]/40 text-[#ece8dd] hover:border-[#2ea87f] shadow cursor-pointer transition"
          >
            <span>🔍 Search</span>
            <kbd className="text-[10px] font-mono px-1.5 py-0.5 bg-[#0e1310] text-[#8a9490] rounded border border-[#24302a]">
              ⌘K
            </kbd>
          </button>

          {selectedPatient && (
            <button
              onClick={() => setIsHakeemDrawerOpen(true)}
              className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-linear-to-r from-[#1f6f54] to-[#2ea87f] text-[#06120c] hover:brightness-110 shadow cursor-pointer transition"
            >
              <span>✨ Hakeem Sahab™ AI</span>
            </button>
          )}
          <button
            onClick={handleLogout}
            className="text-xs text-[#8a9490] hover:text-white px-2.5 py-1 rounded cursor-pointer"
          >
            Sign out
          </button>
        </div>
      </header>

      {/* Main Workspace Layout (Sidebar + Workbench) */}
      <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
        {/* Left Sidebar: Patients Queue */}
        <aside className="w-full md:w-80 border-r border-[#24302a] bg-[#0e1310] flex flex-col shrink-0">
          <div className="p-4 border-b border-[#24302a]">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold uppercase text-[#8a9490] font-mono">
                Patients EMR Queue
              </span>
              <span className="text-xs font-mono text-[#c9a24b]">{patients.length} active</span>
            </div>
            <input
              type="text"
              value={patientSearch}
              onChange={(e) => setPatientSearch(e.target.value)}
              placeholder="Search by MRN or Name..."
              className="zv-input text-xs"
            />
          </div>

          <div className="flex-1 overflow-y-auto p-2 space-y-1.5">
            {isLoadingPatients ? (
              <div className="p-4 text-center text-xs text-[#8a9490]">Loading patients...</div>
            ) : filteredPatients.length === 0 ? (
              <div className="p-4 text-center text-xs text-[#8a9490]">No patients found.</div>
            ) : (
              filteredPatients.map((p) => {
                const isSelected = selectedPatient?.id === p.id;
                return (
                  <div
                    key={p.id}
                    onClick={() => setSelectedPatient(p)}
                    className={`p-3 rounded-lg cursor-pointer transition border text-xs ${
                      isSelected
                        ? "bg-[#171d17] border-[#2ea87f] shadow-xs"
                        : "bg-[#121712] border-[#24302a]/70 hover:border-[#8a9490]/50"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-sm text-[#ece8dd]">
                        {p.first_name} {p.last_name}
                      </span>
                      <span className="font-mono text-[11px] text-[#c9a24b]">{p.mrn}</span>
                    </div>
                    <div className="flex items-center gap-2 mt-1 text-[11px] text-[#8a9490]">
                      <span className="capitalize">{p.gender}</span>
                      <span>·</span>
                      <span>Status: {p.pregnancy_status}</span>
                    </div>
                    {p.comorbidities && p.comorbidities.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-2">
                        {p.comorbidities.map((c, i) => (
                          <span
                            key={i}
                            className="text-[10px] px-1.5 py-0.2 rounded bg-amber-950/40 text-amber-300 border border-amber-800/40"
                          >
                            {c}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </aside>

        {/* Center Workbench */}
        <main className="flex-1 flex flex-col overflow-y-auto bg-[#0b0f0d]">
          {selectedPatient ? (
            <div className="flex-1 flex flex-col p-6 max-w-6xl w-full mx-auto space-y-6">
              {/* Patient 360 Banner */}
              <div className="zv-panel p-5 flex flex-wrap items-center justify-between gap-4 border border-[#24302a]">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-full bg-[#1f6f54]/30 border border-[#2ea87f] flex items-center justify-center text-lg font-serif font-bold text-[#2ea87f]">
                    {selectedPatient.first_name[0]}
                    {selectedPatient.last_name[0]}
                  </div>
                  <div>
                    <h2 className="text-lg font-bold text-[#ece8dd]">
                      {selectedPatient.first_name} {selectedPatient.last_name}
                    </h2>
                    <div className="flex flex-wrap items-center gap-3 text-xs text-[#8a9490] mt-0.5">
                      <span className="font-mono text-[#c9a24b]">MRN: {selectedPatient.mrn}</span>
                      <span>·</span>
                      <span>Age: {patientAge} yrs</span>
                      <span>·</span>
                      <span className="capitalize">Gender: {selectedPatient.gender}</span>
                      <span>·</span>
                      <span className="text-amber-300">
                        Pregnancy: {selectedPatient.pregnancy_status}
                      </span>
                      <span>·</span>
                      <span className={mizajAssessment ? "text-[#e3c884] font-medium" : "text-[#8a9490]"}>
                        Mizaj: {mizajAssessment ? `${mizajAssessment.primary_temperament} (${mizajAssessment.su_e_mizaj})` : "Pending Evaluation"}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setShowMizajModal(true)}
                    className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-[#171d17] hover:bg-[#c9a24b]/20 border border-[#c9a24b] text-[#e3c884] cursor-pointer transition"
                  >
                    ⚖️ 10-Ajnas Mizaj
                  </button>
                  <button
                    onClick={() => setIsHakeemDrawerOpen(true)}
                    className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-[#171d17] hover:bg-[#1f6f54]/40 border border-[#2ea87f] text-[#2ea87f] cursor-pointer transition"
                  >
                    Clinical AI Consultation →
                  </button>
                </div>
              </div>

              {/* Workbench Tabs */}
              <div className="flex border-b border-[#24302a] gap-2">
                <button
                  onClick={() => setActiveTab("timeline")}
                  className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition cursor-pointer ${
                    activeTab === "timeline"
                      ? "border-[#2ea87f] text-[#2ea87f]"
                      : "border-transparent text-[#8a9490] hover:text-[#ece8dd]"
                  }`}
                >
                  Longitudinal Timeline ({timelineEvents.length})
                </button>
                <button
                  onClick={() => setActiveTab("nuskha")}
                  className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition cursor-pointer ${
                    activeTab === "nuskha"
                      ? "border-[#2ea87f] text-[#2ea87f]"
                      : "border-transparent text-[#8a9490] hover:text-[#ece8dd]"
                  }`}
                >
                  Nuskha Nawisi Studio (Formulations)
                </button>
                <button
                  onClick={() => setActiveTab("tadbeer")}
                  className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition cursor-pointer ${
                    activeTab === "tadbeer"
                      ? "border-[#2ea87f] text-[#2ea87f]"
                      : "border-transparent text-[#8a9490] hover:text-[#ece8dd]"
                  }`}
                >
                  Ilaj-bit-Tadbeer (Regimens {tadbeerPlans.length})
                </button>
                <button
                  onClick={() => setActiveTab("pharmacopoeia")}
                  className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition cursor-pointer ${
                    activeTab === "pharmacopoeia"
                      ? "border-[#2ea87f] text-[#2ea87f]"
                      : "border-transparent text-[#8a9490] hover:text-[#ece8dd]"
                  }`}
                >
                  UPI Pharmacopoeia Reference
                </button>
                <button
                  onClick={() => setActiveTab("digital_twin")}
                  className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition cursor-pointer ${
                    activeTab === "digital_twin"
                      ? "border-[#2ea87f] text-[#2ea87f]"
                      : "border-transparent text-[#8a9490] hover:text-[#ece8dd]"
                  }`}
                >
                  🧬 Clinical Digital Twin (12 Axes)
                </button>
                <button
                  onClick={() => setActiveTab("ambient_scribe")}
                  className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition cursor-pointer ${
                    activeTab === "ambient_scribe"
                      ? "border-[#2ea87f] text-[#2ea87f]"
                      : "border-transparent text-[#8a9490] hover:text-[#ece8dd]"
                  }`}
                >
                  🎙️ Ambient Scribe & 21 CFR Part 11
                </button>
                <button
                  onClick={() => setActiveTab("multimodal_lab")}
                  className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition cursor-pointer ${
                    activeTab === "multimodal_lab"
                      ? "border-[#2ea87f] text-[#2ea87f]"
                      : "border-transparent text-[#8a9490] hover:text-[#ece8dd]"
                  }`}
                >
                  🧪 Multimodal Lab & Signs
                </button>
                <button
                  onClick={() => setActiveTab("patient_portal")}
                  className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition cursor-pointer ${
                    activeTab === "patient_portal"
                      ? "border-[#2ea87f] text-[#2ea87f]"
                      : "border-transparent text-[#8a9490] hover:text-[#ece8dd]"
                  }`}
                >
                  📱 Patient App 2.0
                </button>
                <button
                  onClick={() => setActiveTab("governance_board")}
                  className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition cursor-pointer ${
                    activeTab === "governance_board"
                      ? "border-[#2ea87f] text-[#2ea87f]"
                      : "border-transparent text-[#8a9490] hover:text-[#ece8dd]"
                  }`}
                >
                  🏛️ Governance Board
                </button>
                <button
                  onClick={() => setActiveTab("task_pipelines")}
                  className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition cursor-pointer ${
                    activeTab === "task_pipelines"
                      ? "border-[#2ea87f] text-[#2ea87f]"
                      : "border-transparent text-[#8a9490] hover:text-[#ece8dd]"
                  }`}
                >
                  ⚡ Tasks &amp; Workers
                </button>
              </div>


              {/* Tab 1: Timeline & Diagnostic Differential */}
              {activeTab === "timeline" && (
                <div className="space-y-6">
                  {/* Differential Diagnosis Engine Card */}
                  <div className="zv-panel p-5 space-y-4 border border-[#24302a]">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                      <div>
                        <h3 className="text-sm font-semibold text-[#e3c884] font-serif flex items-center gap-2">
                          <span>🔍 Integrative Differential Engine</span>
                          <span className="text-[10px] font-mono font-normal px-2 py-0.5 rounded bg-[#1f6f54]/20 text-[#2ea87f] border border-[#2ea87f]/40">
                            ICD-11 &amp; Unani Amraz
                          </span>
                        </h3>
                        <p className="text-xs text-[#8a9490] mt-0.5">
                          Cross-map chief complaints to classical Unani nosology (*Amraz* &amp; *Su-e-Mizaj*), WHO ICD-11, and triage red flags.
                        </p>
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={diffComplaint}
                        onChange={(e) => setDiffComplaint(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter") {
                            e.preventDefault();
                            handleEvaluateDifferential();
                          }
                        }}
                        placeholder="Enter chief complaint (e.g. joint pain and swelling, dyspepsia, asthma, headache)..."
                        className="zv-input text-xs flex-1"
                      />
                      <button
                        type="button"
                        onClick={() => handleEvaluateDifferential()}
                        disabled={isEvaluatingDiff || !diffComplaint.trim()}
                        className="zv-btn-primary text-xs px-4 cursor-pointer disabled:opacity-50"
                      >
                        {isEvaluatingDiff ? "Evaluating..." : "Differential"}
                      </button>
                    </div>

                    {/* Quick suggestion chips */}
                    <div className="flex flex-wrap items-center gap-1.5 text-[11px] text-[#8a9490]">
                      <span>Quick presets:</span>
                      {[
                        "Joint pain and swelling",
                        "Dyspepsia and epigastric burning",
                        "Asthma and breathlessness",
                        "Severe headache and dizziness",
                        "Chronic diarrhea with mucus",
                      ].map((preset) => (
                        <button
                          key={preset}
                          type="button"
                          onClick={() => handleEvaluateDifferential(preset)}
                          className="px-2 py-0.5 rounded bg-[#121712] hover:bg-[#1a231d] border border-[#24302a] text-[#c9a24b] text-[10px] cursor-pointer transition"
                        >
                          {preset}
                        </button>
                      ))}
                    </div>

                    {/* Differential Results */}
                    {differentials.length > 0 && (
                      <div className="space-y-3 pt-2 border-t border-[#24302a]">
                        <div className="text-xs font-semibold text-[#ece8dd] flex items-center justify-between">
                          <span>Differential Diagnoses Found ({differentials.length})</span>
                          <button
                            type="button"
                            onClick={() => setDifferentials([])}
                            className="text-[10px] text-[#8a9490] hover:text-[#ece8dd] cursor-pointer"
                          >
                            Clear Results
                          </button>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {differentials.map((d) => (
                            <div
                              key={d.id}
                              className="p-3.5 rounded-lg bg-[#121712] border border-[#24302a] space-y-2 text-xs"
                            >
                              <div className="flex justify-between items-start gap-2">
                                <div>
                                  <span className="font-semibold text-sm text-[#e3c884]">
                                    {d.unani_diagnosis}
                                  </span>
                                  <div className="text-[11px] text-[#2ea87f] font-mono">
                                    ICD-11: {d.icd11_code} · {d.icd11_title}
                                  </div>
                                </div>
                                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#c9a24b]/20 text-[#e3c884] border border-[#c9a24b]/40 shrink-0">
                                  {d.su_e_mizaj_association}
                                </span>
                              </div>

                              <p className="text-[11px] text-[#8a9490] italic">
                                {d.unani_concept}
                              </p>

                              {/* Red flags */}
                              {d.red_flags && d.red_flags.length > 0 && (
                                <div className="p-2 rounded bg-red-950/40 border border-red-800/60 text-[10px] text-red-300 space-y-0.5">
                                  <span className="font-bold flex items-center gap-1 text-red-400">
                                    🚨 Red Flag Statutory Warning:
                                  </span>
                                  <ul className="list-disc list-inside space-y-0.5">
                                    {d.red_flags.map((rf, idx) => (
                                      <li key={idx}>{rf}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}

                              {/* Investigations */}
                              {d.recommended_investigations && d.recommended_investigations.length > 0 && (
                                <div className="text-[10px] text-[#8a9490] pt-1 border-t border-[#24302a]/60">
                                  <strong className="text-[#ece8dd]">Recommended Investigations:</strong>{" "}
                                  {d.recommended_investigations.join("; ")}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Longitudinal History */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h3 className="text-sm font-semibold text-[#e3c884] font-serif">
                        Longitudinal Clinical History &amp; Prescriptions
                      </h3>
                      <span className="text-xs font-mono text-[#8a9490]">
                        {timelineEvents.length} Recorded Encounters
                      </span>
                    </div>
                    <PatientTimeline
                      events={timelineEvents}
                      loading={isLoadingTimeline}
                    />
                  </div>
                </div>
              )}

              {/* Tab 2: Nuskha Builder */}
              {activeTab === "nuskha" && (
                <NuskhaBuilder
                  token={session.access_token}
                  patient={selectedPatient}
                  onDraftCreated={(_draft: NuskhaDraftOut) => {
                    // Refresh timeline if needed
                    clinicalApi
                      .getTimeline(session.access_token, selectedPatient.id)
                      .then((events) => setTimelineEvents(events || []));
                  }}
                />
              )}

              {/* Tab 3: Tadbeer Plans */}
              {activeTab === "tadbeer" && (
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-sm font-semibold text-[#e3c884] font-serif">
                        Regimenal Therapy (Ilaj-bit-Tadbeer) Protocols
                      </h3>
                      <p className="text-xs text-[#8a9490]">
                        Classical evacuation (Istifragh) and retention (Ihtibas) regimens governed by safety guardrails.
                      </p>
                    </div>
                    <button
                      onClick={() => setShowAddTadbeerModal(true)}
                      className="zv-btn-primary text-xs cursor-pointer"
                    >
                      + Prescribe Tadbeer Regimen
                    </button>
                  </div>

                  {isLoadingTadbeer ? (
                    <div className="text-center py-8 text-xs text-[#8a9490]">Loading regimens...</div>
                  ) : tadbeerPlans.length === 0 ? (
                    <div className="zv-panel p-8 text-center text-xs text-[#8a9490]">
                      No active Tadbeer regimens prescribed for this patient. Click &ldquo;+ Prescribe Tadbeer Regimen&rdquo; to add Hijama, Fasd, Hammam, etc.
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {tadbeerPlans.map((plan) => (
                        <div key={plan.id} className="zv-panel p-4 space-y-2 text-xs">
                          <div className="flex justify-between items-start">
                            <h4 className="font-semibold text-sm text-[#ece8dd]">{plan.name}</h4>
                            <span
                              className={`text-[10px] font-mono px-2 py-0.5 rounded border ${
                                plan.safety_verdict === "SAFE_TO_CONSIDER"
                                  ? "bg-emerald-950/60 text-emerald-400 border-emerald-700"
                                  : plan.safety_verdict === "CAUTION"
                                  ? "bg-amber-950/60 text-amber-400 border-amber-700"
                                  : "bg-red-950/60 text-red-400 border-red-700"
                              }`}
                            >
                              {plan.safety_verdict}
                            </span>
                          </div>
                          <div className="text-[#8a9490]">
                            <strong>Indication:</strong> {plan.indication}
                          </div>
                          <div className="text-[#8a9490]">
                            <strong>Frequency:</strong> {plan.frequency} · <strong>Duration:</strong> {plan.duration}
                          </div>
                          {plan.contraindications && (
                            <div className="text-[11px] text-amber-300/90 pt-1 border-t border-[#24302a]">
                              Contraindications: {plan.contraindications}
                            </div>
                          )}
                          {plan.safety_reasons && plan.safety_reasons.length > 0 && (
                            <div className="text-[11px] text-red-300 pt-1 border-t border-[#24302a]">
                              Safety Alerts: {plan.safety_reasons.join("; ")}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Tab 4: UPI Pharmacopoeia Directory */}
              {activeTab === "pharmacopoeia" && (
                <div className="space-y-6">
                  <div className="zv-panel p-4">
                    <h3 className="text-sm font-semibold text-[#e3c884] font-serif mb-1">
                      Unani Pharmacopoeia of India (UPI) &amp; Schedule E(1) Statutory Reference
                    </h3>
                    <p className="text-xs text-[#8a9490] mb-3">
                      Official classical monographs with Mizaj degrees, botanical verification, statutory dose limits, and Mudabbar protocols.
                    </p>
                    <input
                      type="text"
                      value={pharmaSearch}
                      onChange={(e) => setPharmaSearch(e.target.value)}
                      placeholder="Search UPI monographs (e.g. Asgand, Suranjan, Kuchla, Zanjabeel)..."
                      className="zv-input text-xs"
                    />
                  </div>

                  {isLoadingPharma ? (
                    <div className="text-center py-8 text-xs text-[#8a9490]">Loading UPI database...</div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {upiMonographs
                        .filter(
                          (m) =>
                            m.name.toLowerCase().includes(pharmaSearch.toLowerCase()) ||
                            m.botanical_name.toLowerCase().includes(pharmaSearch.toLowerCase())
                        )
                        .map((mono) => (
                          <div key={mono.id} className="zv-panel p-4 space-y-2 text-xs">
                            <div className="flex justify-between items-baseline">
                              <div>
                                <span className="font-semibold text-sm text-[#ece8dd]">{mono.name}</span>
                                <span className="text-xs text-[#8a9490] italic ml-1.5">
                                  ({mono.botanical_name})
                                </span>
                              </div>
                              <span className="text-xs font-mono text-[#c9a24b]">
                                {mono.mizaj?.temperament || "Mutadil"}
                              </span>
                            </div>

                            {mono.is_schedule_e1 && (
                              <div className="text-[11px] font-mono px-2 py-0.5 rounded bg-red-950/60 text-red-400 border border-red-800">
                                ⚠️ Schedule E(1) Statutory Poison — Mandatory Mudabbar Required
                              </div>
                            )}

                            <div className="text-[#8a9490] text-[11px]">
                              <strong>Af&apos;al (Actions):</strong> {(mono.afal || []).join(", ")}
                            </div>
                            <div className="text-[#8a9490] text-[11px]">
                              <strong>Musleh (Corrective):</strong> {mono.musleh} · <strong>Badal:</strong> {mono.badal}
                            </div>
                            <div className="text-[#8a9490] text-[11px]">
                              <strong>UPI Standard Dose:</strong> {mono.dose}
                            </div>
                          </div>
                        ))}
                    </div>
                  )}
                </div>
              )}

              {/* Tab 5: Clinical Digital Twin */}
              {activeTab === "digital_twin" && (
                <DigitalTwinCockpit
                  token={session.access_token}
                  patientId={selectedPatient.id}
                  patientName={`${selectedPatient.first_name} ${selectedPatient.last_name}`}
                />
              )}

              {/* Tab 6: Ambient Clinical Scribe & 21 CFR Part 11 */}
              {activeTab === "ambient_scribe" && (
                <AmbientScribeGovernanceCockpit
                  token={session.access_token}
                  patientId={selectedPatient.id}
                  patientName={`${selectedPatient.first_name} ${selectedPatient.last_name}`}
                />
              )}

              {/* Tab 7: Multimodal AI Lab & Physical Signs */}
              {activeTab === "multimodal_lab" && (
                <MultimodalLabCockpit
                  token={session.access_token}
                  patientId={selectedPatient.id}
                  patientName={`${selectedPatient.first_name} ${selectedPatient.last_name}`}
                />
              )}

              {/* Tab 8: Patient App 2.0 & Adherence */}
              {activeTab === "patient_portal" && (
                <PatientPortalCockpit
                  token={session.access_token}
                  patientId={selectedPatient.id}
                  patientName={`${selectedPatient.first_name} ${selectedPatient.last_name}`}
                />
              )}

              {/* Tab 9: Clinical Governance Board */}
              {activeTab === "governance_board" && (
                <GovernanceBoardCockpit token={session.access_token} />
              )}

              {/* Tab 10: Task Queue & ABDM Streaming Workers */}
              {activeTab === "task_pipelines" && (
                <TaskPipelineCockpit token={session.access_token} />
              )}
            </div>
          ) : (

            <div className="flex-1 flex items-center justify-center p-8 text-center">
              <div className="zv-panel p-8 max-w-md">
                <p className="text-sm font-medium text-[#ece8dd]">No patient selected</p>
                <p className="text-xs text-[#8a9490] mt-1">
                  Select a patient from the EMR queue on the left to review their longitudinal record, draft formulations, or run Hakeem Sahab AI consultations.
                </p>
              </div>
            </div>
          )}
        </main>
      </div>

      {/* Add Tadbeer Regimen Modal */}
      {showAddTadbeerModal && selectedPatient && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="zv-panel p-6 max-w-md w-full space-y-4 border border-[#2ea87f]">
            <h3 className="text-base font-serif text-[#e3c884] font-semibold">
              Prescribe Ilaj-bit-Tadbeer Regimen
            </h3>
            <form onSubmit={handleCreateTadbeer} className="space-y-3 text-xs">
              <div>
                <label className="zv-label">Regimen Modality</label>
                <select
                  value={newTadbeerName}
                  onChange={(e) => {
                    setNewTadbeerName(e.target.value);
                    const found = TADBEER_REGIMENS.find((r) => r.name === e.target.value);
                    if (found) {
                      setNewTadbeerIndication(found.indication);
                      setNewTadbeerCategory(
                        found.category as
                          | "regimen"
                          | "rest"
                          | "physical_activity"
                          | "massage"
                          | "bathing"
                          | "other"
                      );
                    }
                  }}
                  className="zv-input text-xs cursor-pointer"
                >
                  {TADBEER_REGIMENS.map((r) => (
                    <option key={r.name} value={r.name} className="bg-[#121712]">
                      {r.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="zv-label">Classical Indication</label>
                <input
                  type="text"
                  value={newTadbeerIndication}
                  onChange={(e) => setNewTadbeerIndication(e.target.value)}
                  className="zv-input text-xs"
                />
              </div>

              <div>
                <label className="zv-label">Frequency</label>
                <input
                  type="text"
                  value={newTadbeerFrequency}
                  onChange={(e) => setNewTadbeerFrequency(e.target.value)}
                  className="zv-input text-xs"
                />
              </div>

              <div>
                <label className="zv-label">Duration / Session</label>
                <input
                  type="text"
                  value={newTadbeerDuration}
                  onChange={(e) => setNewTadbeerDuration(e.target.value)}
                  className="zv-input text-xs"
                />
              </div>

              <div className="flex justify-end gap-3 pt-3">
                <button
                  type="button"
                  onClick={() => setShowAddTadbeerModal(false)}
                  className="px-4 py-2 rounded text-xs text-[#8a9490] hover:text-white cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmittingTadbeer}
                  className="zv-btn-primary text-xs cursor-pointer disabled:opacity-50"
                >
                  {isSubmittingTadbeer ? "Evaluating..." : "Evaluate & Prescribe"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Hakeem Sahab Drawer */}
      {selectedPatient && (
        <HakeemReviewDrawer
          token={session.access_token}
          patient={selectedPatient}
          isOpen={isHakeemDrawerOpen}
          onClose={() => setIsHakeemDrawerOpen(false)}
          onConvertToNuskha={(_consultation) => {
            setIsHakeemDrawerOpen(false);
            setActiveTab("nuskha");
          }}
        />
      )}

      {/* 10-Ajnas Mizaj Assessment Modal */}
      {selectedPatient && showMizajModal && (
        <MizajAssessmentModal
          token={session.access_token}
          patientId={selectedPatient.id}
          patientName={`${selectedPatient.first_name} ${selectedPatient.last_name}`}
          isOpen={showMizajModal}
          onClose={() => setShowMizajModal(false)}
          onSaved={(assessment) => {
            setMizajAssessment(assessment);
          }}
        />
      )}

      {/* Global Command Palette (Cmd+K) */}
      <GlobalCommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        onNavigate={(route) => setActiveTab(route as ActiveTab)}
      />
    </div>
  );
}
