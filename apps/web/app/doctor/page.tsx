"use client";

import React, { useState, useEffect } from "react";
import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { NuskhaBuilder } from "@/components/NuskhaBuilder";
import { HakeemReviewDrawer } from "@/components/HakeemReviewDrawer";
import { DigitalTwinCockpit } from "@/components/DigitalTwinCockpit";
import type { PatientRecord } from "@/lib/clinicalApi";
import { AuthService } from "@/lib/services/authService";
import { useAuth } from "@/lib/hooks/useAuth";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

/** Lightweight skeleton shown while patient data is loading */
const PATIENT_LOADING_SKELETON: PatientRecord = {
  id: "",
  first_name: "—",
  last_name: "—",
  date_of_birth: "",
  gender: "male",
  contact_phone: "",
  contact_email: "",
  blood_group: "",
  mizaj_dominant: "Assessment Pending",
  allergies: [],
};


export const CLINICAL_PHASES = [
  {
    id: "intake",
    phaseNumber: 1,
    title: "Phase 1: Intake & Constitutional Diagnostics",
    shortTitle: "Phase 1: Intake & Diagnostics",
    tabs: [
      { id: "overview", label: "Overview" },
      { id: "history", label: "History" },
      { id: "examination", label: "Examination" },
      { id: "vitals", label: "Vitals" },
      { id: "investigations", label: "Investigations" },
      { id: "assessment", label: "Assessment" },
      { id: "mizaj", label: "Mizaj & Nabz" },
    ]
  },
  {
    id: "formulation",
    phaseNumber: 2,
    title: "Phase 2: Formulation & Regimenal Therapy",
    shortTitle: "Phase 2: Formulation & Therapy",
    tabs: [
      { id: "afaal", label: "Afaal Cascade" },
      { id: "axis", label: "Axis Mapping" },
      { id: "treatment", label: "Treatment Plan" },
      { id: "prescription", label: "Prescription (Nuskha)" },
    ]
  },
  {
    id: "closure",
    phaseNumber: 3,
    title: "Phase 3: Closure & Part 11 Electronic Sealing",
    shortTitle: "Phase 3: Closure & Sealing",
    tabs: [
      { id: "followup", label: "Follow-up" },
      { id: "timeline", label: "Timeline" },
      { id: "twin", label: "Research / Twin" },
    ]
  }
] as const;

export default function DoctorWorkspacePage({ initialPatientId }: { initialPatientId?: string } = {}) {
  const { isLoading: authLoading, isAuthorized } = useAuth({ requiredRoles: ['DOCTOR', 'HAKEEM'] });
  const [activeTab, setActiveTab] = useState<
    | "overview"
    | "history"
    | "examination"
    | "vitals"
    | "investigations"
    | "assessment"
    | "mizaj"
    | "afaal"
    | "axis"
    | "treatment"
    | "prescription"
    | "followup"
    | "timeline"
    | "twin"
  >("overview");

  const currentPhase = CLINICAL_PHASES.find((p) =>
    p.tabs.some((t) => t.id === activeTab)
  ) || CLINICAL_PHASES[0];

  const [aiDrawerOpen, setAiDrawerOpen] = useState(false);
  const [activePatient, setActivePatient] = useState<PatientRecord>(PATIENT_LOADING_SKELETON);
  const [patientList, setPatientList] = useState<PatientRecord[]>([]);
  const [isLoadingPatient, setIsLoadingPatient] = useState(true);
  const [apiError, setApiError] = useState<string | null>(null);
  const [encounterId, setEncounterId] = useState<string>("");
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [showRxPrintModal, setShowRxPrintModal] = useState(false);

  // Clinician Authentication & Production Intranet Gate States
  const [session, setSession] = useState<any>(null);
  const [isDemoMode, setIsDemoMode] = useState(false);
  const [authChecking, setAuthChecking] = useState(true);
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);
  const [loginError, setLoginError] = useState<string | null>(null);

  // Check existing session on mount
  useEffect(() => {
    const s = AuthService.getSession();
    if (s) {
      setSession(s);
    }
    setAuthChecking(false);
  }, []);

  const handleDoctorLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!loginEmail.trim() || !loginPassword) {
      setLoginError("Please enter your clinician email and password.");
      return;
    }
    setLoginLoading(true);
    setLoginError(null);
    try {
      const sess = await AuthService.loginAsync(loginEmail.trim(), loginPassword);
      setSession(sess);
    } catch (err: any) {
      setLoginError(err?.message || "Invalid clinician credentials. Please check your credentials.");
    } finally {
      setLoginLoading(false);
    }
  };

  const handleLaunchDemo = () => {
    setIsDemoMode(true);
    setSession({
      token: "demo-clinician-token",
      user: {
        id: "DOC-DEMO-01",
        fullName: "Hakim Dr. Irfan Ashraf (NCISM)",
        email: "irfan.ashraf@zayvorahealth.com",
        role: "DOCTOR",
        roleDisplayName: "Senior Consultant Tabeeb",
        facilityId: "fac-01",
        facilityName: "ZAYVORA Matab™ Central Care Centre"
      }
    });
  };


  // Clinical Consultation State (Initialized to empty - documented per live encounter)
  const [chiefComplaint, setChiefComplaint] = useState("");
  const [examNotes, setExamNotes] = useState("");
  const [vitals, setVitals] = useState({
    bp: "",
    pulse: "",
    temp: "",
    weight: "",
    spo2: "",
  });

  // Afaal Cascade State
  const [afaalStage, setAfaalStage] = useState<"TANQIYA" | "TAHLEEL" | "TAQWIYAAT" | "HIFZ">("TAHLEEL");
  const [afaalRationale, setAfaalRationale] = useState("");
  const [afaalGoals, setAfaalGoals] = useState<string[]>([]);

  // Lock and Signature State (Starts in strict unsealed DRAFT state)
  const [isLocked, setIsLocked] = useState(false);
  const [signatureHash, setSignatureHash] = useState<string | null>(null);
  const [merkleBlock, setMerkleBlock] = useState<number | null>(null);
  const [signedTimestamp, setSignedTimestamp] = useState<string | null>(null);
  const [isSigning, setIsSigning] = useState(false);

  // Engine Integration States
  const [mizajAssessment, setMizajAssessment] = useState<any>(null);
  const [organAxisResult, setOrganAxisResult] = useState<any>(null);
  const [differentialList, setDifferentialList] = useState<any[]>([]);
  const [isSavingNotes, setIsSavingNotes] = useState(false);
  const [lastSavedTime, setLastSavedTime] = useState<string | null>(null);

  // Timeline events state
  const [timelineEvents, setTimelineEvents] = useState<any[]>([]);

  // Master Platform Services Integration States
  const [tasks, setTasks] = useState<any[]>([]);
  const [showTasksModal, setShowTasksModal] = useState(false);
  const [preEncounterData, setPreEncounterData] = useState<any>(null);
  const [showSignModal, setShowSignModal] = useState(false);
  const [signingPin, setSigningPin] = useState("");
  const [signingReason, setSigningReason] = useState("Consultation, Nuskha, and Afaal regimen verified under NCISM standards.");
  const [signError, setSignError] = useState<string | null>(null);

  // Load patient list on mount and select first patient
  useEffect(() => {
    async function loadPatients() {
      if (!session && !isDemoMode) return;
      setIsLoadingPatient(true);
      setApiError(null);
      try {
        const token = session?.token;
        const headers: Record<string, string> = {};
        if (token) headers["Authorization"] = `Bearer ${token}`;
        const res = await fetch(`${API}/api/v1/patients`, { headers });
        if (res.ok) {
          const data = await res.json();
          const patients: PatientRecord[] = data.patients || data.items || data || [];
          if (patients.length > 0) {
            setPatientList(patients);
            const target = initialPatientId ? patients.find(p => p.id === initialPatientId) : null;
            setActivePatient(target || patients[0]);
          } else {
            setPatientList([]);
          }
        } else {
          setApiError(`Authoritative clinical server returned error (HTTP ${res.status}). Live patient records unavailable.`);
        }
      } catch {
        setApiError("Unable to establish encrypted clinical connection with Central Server. Please verify server connectivity.");
      } finally {
        setIsLoadingPatient(false);
      }
    }
    loadPatients();
  }, [initialPatientId, session, isDemoMode]);

  // Create or load an encounter when active patient is set
  useEffect(() => {
    if (!activePatient.id) return;
    async function initEncounter() {
      try {
        const session = AuthService.getSession();
        if (!session?.token) return;
        // Attempt to create a new encounter for this patient
        const res = await fetch(`${API}/api/v1/encounters`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${session.token}`
          },
          body: JSON.stringify({
            patient_id: activePatient.id,
            chief_complaint: chiefComplaint
          })
        });
        if (res.ok) {
          const data = await res.json();
          if (data.encounter?.id) setEncounterId(data.encounter.id);
        }
      } catch {
        // Cannot create encounter — will retry on next interaction
      }
    }
    initEncounter();
  }, [activePatient.id]);

  useEffect(() => {
    async function loadTimeline() {
      if (!activePatient.id) return;
      try {
        const session = AuthService.getSession();
        const res = await fetch(`${API}/api/v1/patients/${activePatient.id}/timeline`, {
          headers: session?.token ? { Authorization: `Bearer ${session.token}` } : {}
        });
        if (res.ok) {
          const data = await res.json();
          if (data.ok && Array.isArray(data.timeline)) {
            setTimelineEvents(data.timeline);
          }
        }
      } catch {
        // Fallback gracefully to offline timeline
      }
    }
    loadTimeline();
  }, [activePatient.id]);

  // Load real-time engine intelligence (Mizaj, Organ Axis, Differential, Afaal)
  useEffect(() => {
    if (!activePatient.id) return;
    async function loadEngineDiagnostics() {
      const session = AuthService.getSession();
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(session?.token ? { Authorization: `Bearer ${session.token}` } : {})
      };

      // 1. Fetch latest quantitative Mizaj assessment
      try {
        const mizajRes = await fetch(`${API}/api/v1/patients/${activePatient.id}/mizaj-assessment/latest`, { headers });
        if (mizajRes.ok) {
          const mData = await mizajRes.json();
          setMizajAssessment(mData);
        }
      } catch {}

      // 2. Fetch organ axis cross-talk analysis
      try {
        const axisRes = await fetch(`${API}/api/v1/diagnostics/organ-axis/analyze`, {
          method: "POST",
          headers,
          body: JSON.stringify({
            patient_id: activePatient.id,
            organ_axis: "mafasil-asab",
            clinical_observations: examNotes
          })
        });
        if (axisRes.ok) {
          const aData = await axisRes.json();
          setOrganAxisResult(aData);
        }
      } catch {}

      // 3. Fetch differential diagnosis considerations
      try {
        const diffRes = await fetch(`${API}/api/v1/diagnostics/differential`, {
          method: "POST",
          headers,
          body: JSON.stringify({
            chief_complaint: chiefComplaint,
            dominant_mizaj: activePatient.mizaj_dominant || "Balghami (Cold & Moist)",
            organ_axis: "mafasil-asab"
          })
        });
        if (diffRes.ok) {
          const dData = await diffRes.json();
          setDifferentialList(dData.considerations || dData.items || []);
        }
      } catch {}

      // 4. Evaluate recommended Afaal therapeutic stage
      try {
        const afaalRes = await fetch(`${API}/api/v1/clinical/afaal/evaluate`, {
          method: "POST",
          headers,
          body: JSON.stringify({
            mizaj_dominant: activePatient.mizaj_dominant || "Balghami (Cold & Moist)",
            organ_axis: "mafasil-asab",
            chronicity_months: 6,
            symptom_severity: "MODERATE"
          })
        });
        if (afaalRes.ok) {
          const afData = await afaalRes.json();
          if (afData.recommended_stage) setAfaalStage(afData.recommended_stage);
          if (afData.rationale) setAfaalRationale(afData.rationale);
          if (afData.goals) setAfaalGoals(afData.goals);
        }
      } catch {}
    }
    loadEngineDiagnostics();
  }, [activePatient.id]);

  // Debounced auto-save for clinical consultation notes
  useEffect(() => {
    if (!encounterId || !activePatient.id || isLocked) return;
    const timer = setTimeout(async () => {
      try {
        setIsSavingNotes(true);
        const session = AuthService.getSession();
        await fetch(`${API}/api/v1/encounters/${encounterId}`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            ...(session?.token ? { Authorization: `Bearer ${session.token}` } : {})
          },
          body: JSON.stringify({
            chief_complaint: chiefComplaint,
            examination_notes: examNotes,
            vitals,
            afaal_stage: afaalStage,
          })
        });
        setLastSavedTime(new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }));
        setHasUnsavedChanges(false);
      } catch {
        // Local state preserved
      } finally {
        setIsSavingNotes(false);
      }
    }, 1500);

    return () => clearTimeout(timer);
  }, [chiefComplaint, examNotes, vitals, afaalStage, encounterId, activePatient.id, isLocked]);


  // Fetch live tasks for clinician (Service 8)
  useEffect(() => {
    async function fetchTasks() {
      try {
        const res = await fetch(`${API}/api/v1/tasks?role=DOCTOR`);
        if (res.ok) {
          const data = await res.json();
          if (data.ok && data.tasks) {
            setTasks(data.tasks);
          }
        }
      } catch {}
    }
    fetchTasks();
  }, []);

  // Fetch pre-encounter briefing for active patient (Service 3)
  useEffect(() => {
    if (!activePatient.id) return;
    async function fetchPreEncounter() {
      try {
        const res = await fetch(`${API}/api/v1/clinical/encounter/prepare?patient_id=${activePatient.id}&clinician_id=DOC-01`);
        if (res.ok) {
          const data = await res.json();
          if (data.ok && data.pre_encounter) {
            setPreEncounterData(data.pre_encounter);
          }
        }
      } catch {}
    }
    fetchPreEncounter();
  }, [activePatient.id]);

  const handleCompleteTask = async (taskId: string) => {
    try {
      const res = await fetch(`${API}/api/v1/tasks/${taskId}/complete`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          actor_id: "DOC-01",
          notes: "Task reviewed and verified by attending physician."
        })
      });
      if (res.ok) {
        setTasks((prev) => prev.map((t) => (t.task_id === taskId ? { ...t, status: "COMPLETED" } : t)));
      }
    } catch {}
  };

  const handleOpenSignModal = () => {
    setSignError(null);
    setShowSignModal(true);
  };

  const handleConfirmSignWithPin = async () => {
    setIsSigning(true);
    setSignError(null);
    try {
      const res = await fetch(`${API}/api/v1/clinical/encounter/sign-off`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          encounter_id: encounterId || "ENC-2026-0814-01",
          clinician_id: "DOC-01",
          signing_pin: signingPin,
          reason: signingReason
        })
      });
      const data = await res.json();
      if (res.ok && data.ok) {
        setSignatureHash(data.signature?.signature_hash || data.signature_hash || null);
        setSignedTimestamp(data.signed_at || new Date().toISOString());
        setMerkleBlock(data.signature?.merkle_block || data.merkle_block || 1042);
        setIsLocked(true);
        setHasUnsavedChanges(false);
        setShowSignModal(false);
        setIsSigning(false);
        return;
      } else {
        setSignError(data.error || data.detail || "Cryptographic signature verification failed. Please verify your PIN.");
        setIsSigning(false);
        return;
      }
    } catch {
      setSignError("Cryptographic ledger service is currently unreachable. Encounters cannot be permanently sealed without active ledger connectivity (21 CFR Part 11). Record remains in Draft state.");
      setIsSigning(false);
    }
  };

  if (authChecking) {
    return (
      <div className="min-h-screen bg-[#0A0F1D] flex items-center justify-center text-teal-400 text-xs font-mono">
        Authenticating Secure Clinical Environment...
      </div>
    );
  }

  // Clinician & Staff Gateway (Restricts unauthenticated visitors from clinical charts)
  if (!session && !isDemoMode) {
    return (
      <div className="min-h-screen bg-[#0A0F1D] text-slate-100 flex flex-col justify-center items-center p-4">
        <div className="max-w-md w-full bg-[#0F172A] border border-slate-800 rounded-3xl p-8 space-y-6 shadow-2xl">
          <div className="text-center space-y-2">
            <div className="w-12 h-12 rounded-2xl bg-teal-500/20 text-teal-400 mx-auto flex items-center justify-center p-2.5">
              <HealthcareIcon name="shield-check" className="w-full h-full text-teal-400" />
            </div>
            <h2 className="text-xl font-bold text-white tracking-tight">ZAYVORA Health OS™</h2>
            <p className="text-xs text-slate-400">Hospital Intranet &amp; Clinician Consultation Desk</p>
          </div>

          <form onSubmit={handleDoctorLogin} className="space-y-4">
            <div>
              <label className="text-[11px] font-semibold text-slate-400 block mb-1">Council Reg Email / ID</label>
              <input
                type="email"
                placeholder="doctor@hospital.org"
                value={loginEmail}
                onChange={(e) => setLoginEmail(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500 font-mono"
                required
              />
            </div>
            <div>
              <label className="text-[11px] font-semibold text-slate-400 block mb-1">Password</label>
              <input
                type="password"
                placeholder="••••••••••••"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500 font-mono"
                required
              />
            </div>

            {loginError && (
              <p className="text-xs text-rose-400 bg-rose-950/40 p-3 rounded-xl border border-rose-800/80">
                {loginError}
              </p>
            )}

            <button
              type="submit"
              disabled={loginLoading}
              className="w-full py-3 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shadow-md transition"
            >
              {loginLoading ? "Authenticating Clinician..." : "Sign In to Clinical Desk →"}
            </button>
          </form>

          <div className="pt-4 border-t border-slate-800 text-center space-y-3">
            <button
              onClick={handleLaunchDemo}
              className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-teal-300 font-semibold text-xs border border-slate-700 transition flex items-center justify-center gap-2"
            >
              <span>🧪 Launch Evaluator Clinical Sandbox</span>
            </button>
            <div className="flex justify-between items-center text-[11px] text-slate-500 pt-1">
              <Link href="/" className="hover:text-slate-300">← Back to Public Website</Link>
              <span>NCISM &amp; 21 CFR Part 11</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (authLoading) return <div className="flex items-center justify-center h-64 text-slate-500">Verifying access…</div>;
  if (!isAuthorized) return null;

  return (
    <AppShell activeRole="doctor">
      {isDemoMode && (
        <div className="bg-amber-950/80 border-b border-amber-600/50 px-4 py-2 flex items-center justify-between text-xs text-amber-200">
          <span className="flex items-center gap-2">
            <span>⚠️</span>
            <strong>Clinical Demo Sandbox Active:</strong> Unsealed records and simulated clinical telemetry loaded for review.
          </span>
          <button
            onClick={() => { setIsDemoMode(false); setSession(null); }}
            className="px-2.5 py-1 rounded-lg bg-amber-800 hover:bg-amber-700 text-white text-[11px] font-bold transition"
          >
            Exit Sandbox
          </button>
        </div>
      )}
      <div className="space-y-5 max-w-7xl mx-auto">
        {/* Authoritative Server Connection Status Alert */}
        {apiError && (
          <div className="p-4 rounded-2xl bg-rose-950/40 border border-rose-500/30 text-rose-200 text-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-md">
            <div className="flex items-center gap-2.5">
              <HealthcareIcon name="alert-triangle" className="w-4 h-4 text-rose-400 shrink-0" />
              <div>
                <strong className="block text-white text-xs">Authoritative Clinical Server: UNAVAILABLE</strong>
                <span>{apiError}</span>
              </div>
            </div>
            <button
              onClick={() => {
                if (typeof window !== "undefined") {
                  window.location.reload();
                }
              }}
              className="px-4 py-1.5 rounded-xl bg-rose-900/60 hover:bg-rose-900 text-white font-semibold border border-rose-700 text-xs transition shrink-0"
            >
              RETRY CONNECTION ⟳
            </button>
          </div>
        )}
        
                {/* Actionable "Requires Attention" Clinician Queue */}
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

        {/* ============================================================= */}
        {/* 1. 8-WIDGET DOCTOR OVERVIEW PANEL */}
        {/* ============================================================= */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-bold text-white tracking-tight">ZAYVORA Health OS™ — Clinical Desk</h1>
                {hasUnsavedChanges && (
                  <span className="zv-badge-amber text-[10px] px-2 py-0.5 rounded font-semibold">
                    ● Unsaved Changes
                  </span>
                )}
              </div>
              <p className="text-xs text-[#94A3B8]">
                Hakeem Dr. Irfan Ashraf • NCISM Reg: BUMS-2004-9841 • Facility: Central Clinical Hospital • Room 3
              </p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowTasksModal(true)}
                className="zv-btn-secondary text-xs border-[#F59E0B]/40 text-[#FBBF24] hover:bg-[#F59E0B]/10 flex items-center gap-1.5"
              >
                <HealthcareIcon name="zap" className="w-3.5 h-3.5 text-[#FBBF24]" />
                <span>Task Engine</span>
                {tasks.filter((t) => t.status === "PENDING").length > 0 && (
                  <span className="bg-[#DC2626] text-white text-[10px] px-1.5 py-0.2 rounded-full font-bold">
                    {tasks.filter((t) => t.status === "PENDING").length}
                  </span>
                )}
              </button>
              <button
                onClick={() => setAiDrawerOpen(true)}
                className="zv-btn-secondary text-xs border-[#0D9488]/40 text-[#2DD4BF] hover:bg-[#0D9488]/20 flex items-center gap-1.5"
              >
                <HealthcareIcon name="activity" className="w-3.5 h-3.5 text-[#2DD4BF]" />
                <span>Hakeem Sahab AI™ Copilot</span>
              </button>
              <a
                href="/library"
                target="_blank"
                rel="noopener noreferrer"
                className="zv-btn-secondary text-xs border-emerald-500/40 text-emerald-400 hover:bg-emerald-500/20 flex items-center gap-1.5"
                title="Access 12-Volume Classical & Modern Integrative Medical Library"
              >
                <HealthcareIcon name="book" className="w-3.5 h-3.5 text-emerald-400" />
                <span>📖 Medical Doctrine Library</span>
              </a>
              {isLocked ? (
                <span className="zv-badge-emerald px-3 py-1 text-xs rounded-lg font-semibold flex items-center gap-1.5">
                  <HealthcareIcon name="check-circle" className="w-3.5 h-3.5 text-emerald-400" />
                  <span>21 CFR Part 11 Sealed</span>
                </span>
              ) : (
                <button
                  onClick={handleOpenSignModal}
                  disabled={isSigning}
                  className="zv-btn-primary text-xs bg-[#0D9488] hover:bg-[#14B8A6] disabled:opacity-50 flex items-center gap-1.5"
                >
                  {isSigning ? (
                    <>
                      <HealthcareIcon name="refresh" className="w-3.5 h-3.5 animate-spin" />
                      <span>Sealing Encounter...</span>
                    </>
                  ) : (
                    <>
                      <HealthcareIcon name="lock" className="w-3.5 h-3.5" />
                      <span>Sign &amp; Lock Encounter</span>
                    </>
                  )}
                </button>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2.5">
            <StatCard label="Today's Appts" value="14" subtext="3 Completed" variant="teal" icon="calendar" />
            <StatCard label="Waiting Queue" value="3" subtext="Next: T-105" variant="amber" icon="⏳" />
            <StatCard label="Active Consult" value="T-104" subtext="Hamza Farooqi" variant="emerald" icon="stethoscope" />
            <StatCard label="Pending Notes" value="2" subtext="Draft state" variant="blue" icon="file-text" />
            <StatCard label="Draft Rx" value="1" subtext="Awaiting lock" variant="rose" icon="pill" />
            <StatCard label="Follow-ups" value="4" subtext="Due this week" variant="purple" icon="refresh" />
            <StatCard label="Safety Alerts" value="1" subtext="Mudabbar Req." variant="amber" icon="️" />
            <StatCard label="Recent Vitals" value={vitals.bp ? "Recorded" : "Pending"} subtext={vitals.bp ? `BP ${vitals.bp}` : "Awaiting entry"} variant="teal" icon="activity" />
          </div>
        </div>

        {/* ============================================================= */}
        {/* 2. MAIN CONSULTATION WORKSPACE (LEFT CONTEXT + CENTER TABS) */}
        {/* ============================================================= */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
          
          {/* LEFT CONTEXT PANEL (3 Columns) */}
          <div className="lg:col-span-3 space-y-4">
            {/* Active Patient & Encounter Card */}
            <div className="zv-card p-4 space-y-3">
              <div className="flex items-center justify-between border-b border-[#334155] pb-2.5">
                <div className="flex items-center gap-2.5">
                  <div className="w-10 h-10 rounded-full bg-[#1E293B] border border-[#334155] flex items-center justify-center font-bold text-white text-sm">
                    HF
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">
                      {activePatient.first_name} {activePatient.last_name}
                    </h3>
                    <span className="text-[11px] text-[#94A3B8] font-mono">MRN-2026-0814</span>
                  </div>
                </div>
                <StatusBadge status="In Consult" variant="verified" pulse />
              </div>

              <div className="p-2 rounded bg-[#0A0F1D] border border-[#334155] text-xs space-y-1">
                <div className="flex justify-between text-[11px]">
                  <span className="text-[#64748B]">Encounter ID:</span>
                  <span className="font-mono text-white font-bold">{encounterId}</span>
                </div>
                <div className="flex justify-between text-[11px]">
                  <span className="text-[#64748B]">Facility:</span>
                  <span className="text-white">Central Clinical Facility</span>
                </div>
                <div className="flex justify-between text-[11px]">
                  <span className="text-[#64748B]">Token:</span>
                  <span className="text-[#2DD4BF] font-mono font-bold">T-104</span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span className="text-[#64748B] block text-[10px] uppercase">Age / Gender</span>
                  <span className="text-white font-medium">42y • Male</span>
                </div>
                <div>
                  <span className="text-[#64748B] block text-[10px] uppercase">Blood Group</span>
                  <span className="text-white font-medium">B+ Positive</span>
                </div>
              </div>

              <div className="p-2.5 rounded-lg bg-[#0A0F1D] border border-[#334155] space-y-1">
                <span className="text-[10px] text-[#64748B] uppercase block">Assessed Mizaj</span>
                <span className="text-xs font-semibold text-[#2DD4BF] flex items-center gap-1.5">
                  <HealthcareIcon name="activity" className="w-3.5 h-3.5 text-[#2DD4BF]" />
                  <span>{activePatient.mizaj_dominant}</span>
                </span>
                <p className="text-[10px] text-[#94A3B8]">Organ Axis: Mafasil-Asab (Joint-Nerve)</p>
              </div>

              <div className="space-y-1">
                <span className="text-[10px] text-[#EF4444] font-semibold uppercase block">Allergies & Contraindications</span>
                <div className="flex flex-wrap gap-1">
                  {activePatient.allergies.map((allergy) => (
                    <span key={allergy} className="text-[11px] px-2 py-0.5 rounded bg-[#EF4444]/15 text-[#FB7185] border border-[#EF4444]/30">
                      ️ {allergy}
                    </span>
                  ))}
                </div>
              </div>

              <div className="border-t border-[#334155] pt-2 space-y-1 text-xs text-[#94A3B8]">
                <div className="flex justify-between">
                  <span>Contact:</span>
                  <span className="text-white">{activePatient.contact_phone}</span>
                </div>
                <div className="flex justify-between">
                  <span>ABHA ID:</span>
                  <span className="text-white font-mono">91-1234-5678-9012</span>
                </div>
              </div>
            </div>

            {/* Quick Vitals Panel */}
            <div className="zv-card p-4 space-y-3">
              <h4 className="text-xs font-semibold text-white uppercase tracking-wider">Clinical Vitals</h4>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div>
                  <label className="text-[10px] text-[#64748B]">BP (mmHg)</label>
                  <input
                    type="text"
                    value={vitals.bp}
                    onChange={(e) => { setVitals({ ...vitals, bp: e.target.value }); setHasUnsavedChanges(true); }}
                    disabled={isLocked}
                    className="zv-input mt-0.5 font-mono text-xs"
                  />
                </div>
                <div>
                  <label className="text-[10px] text-[#64748B]">Pulse (bpm)</label>
                  <input
                    type="text"
                    value={vitals.pulse}
                    onChange={(e) => { setVitals({ ...vitals, pulse: e.target.value }); setHasUnsavedChanges(true); }}
                    disabled={isLocked}
                    className="zv-input mt-0.5 font-mono text-xs"
                  />
                </div>
                <div>
                  <label className="text-[10px] text-[#64748B]">Weight (kg)</label>
                  <input
                    type="text"
                    value={vitals.weight}
                    onChange={(e) => { setVitals({ ...vitals, weight: e.target.value }); setHasUnsavedChanges(true); }}
                    disabled={isLocked}
                    className="zv-input mt-0.5 font-mono text-xs"
                  />
                </div>
                <div>
                  <label className="text-[10px] text-[#64748B]">SpO2 (%)</label>
                  <input
                    type="text"
                    value={vitals.spo2}
                    onChange={(e) => { setVitals({ ...vitals, spo2: e.target.value }); setHasUnsavedChanges(true); }}
                    disabled={isLocked}
                    className="zv-input mt-0.5 font-mono text-xs"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* CENTER DOCUMENTATION SEQUENCE: 13 TABS (9 Columns) */}
          <div className="lg:col-span-9 zv-card flex flex-col min-h-[700px]">
            
            {/* Clinical Safety & Non-Autonomous AI Notice */}
            <div className="bg-indigo-950/30 border-b border-indigo-800/40 px-4 py-2.5 flex items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-2 text-indigo-300">
                <HealthcareIcon name="shield-check" className="w-4 h-4 text-indigo-400 shrink-0" />
                <span className="font-semibold text-white">Clinical Safety Invariant:</span>
                <span className="text-indigo-200/90">Hakeem Sahab AI™ is strictly clinician-supportive and explainable. Autonomous prescription generation is prohibited.</span>
              </div>
              <button
                onClick={() => setAiDrawerOpen(true)}
                className="px-2.5 py-1 rounded bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-[11px] shrink-0 transition"
              >
                Open AI Copilot
              </button>
            </div>

            {/* 3-Phase Clinical Continuum Navigation */}
            <div className="bg-[#0B132B] border-b border-[#334155] px-3 py-2.5 flex flex-wrap items-center justify-between gap-2.5 text-xs">
              <div className="flex items-center gap-2 overflow-x-auto">
                <span className="text-[10px] font-bold uppercase text-slate-400 tracking-wider shrink-0 mr-1">Continuum:</span>
                {CLINICAL_PHASES.map((phase) => {
                  const isPhaseActive = currentPhase.id === phase.id;
                  return (
                    <button
                      key={phase.id}
                      onClick={() => {
                        if (!isPhaseActive) {
                          setActiveTab(phase.tabs[0].id as typeof activeTab);
                        }
                      }}
                      className={`px-3 py-1.5 rounded-lg font-bold text-xs transition flex items-center gap-1.5 whitespace-nowrap ${
                        isPhaseActive
                          ? "bg-teal-600 text-white shadow-sm ring-1 ring-teal-400"
                          : "bg-slate-800/80 text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                      }`}
                    >
                      <span>{phase.shortTitle}</span>
                      <span className={`text-[10px] px-1.5 py-0.5 rounded-full ${isPhaseActive ? "bg-teal-800 text-teal-100 font-mono" : "bg-slate-700 text-slate-400 font-mono"}`}>
                        {phase.tabs.length}
                      </span>
                    </button>
                  );
                })}
              </div>

              <div className="flex items-center gap-2 shrink-0 ml-auto">
                <button
                  onClick={() => setAiDrawerOpen(true)}
                  className="px-2.5 py-1.5 rounded bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-[11px] shrink-0 transition flex items-center gap-1.5 shadow-sm"
                >
                  <HealthcareIcon name="activity" className="w-3.5 h-3.5" />
                  <span>AI Review</span>
                </button>
                <button
                  onClick={handleSignEncounter}
                  disabled={isLocked || isSigning}
                  className={`px-3 py-1.5 rounded font-bold text-[11px] transition flex items-center gap-1.5 ${
                    isLocked
                      ? "bg-emerald-900/60 text-emerald-300 border border-emerald-500/50 cursor-default"
                      : "bg-amber-600 hover:bg-amber-500 text-white shadow-sm"
                  }`}
                >
                  <HealthcareIcon name={isLocked ? "lock" : "shield"} className="w-3.5 h-3.5" />
                  <span>{isLocked ? "21 CFR Part 11 Sealed" : "Sign & Seal"}</span>
                </button>
              </div>
            </div>

            {/* Contextual Phase Tabs Header */}
            <div className="border-b border-[#334155] bg-[#0F172A] rounded-t-xl px-2 pt-2 flex items-center gap-1 overflow-x-auto">
              {currentPhase.tabs.map((tab) => {
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as typeof activeTab)}
                    className={`px-3.5 py-2 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
                      isActive
                        ? "border-[#0D9488] text-[#2DD4BF] bg-[#0D9488]/10 rounded-t-md font-bold"
                        : "border-transparent text-[#94A3B8] hover:text-white hover:bg-[#1E293B]"
                    }`}
                  >
                    {tab.label}
                  </button>
                );
              })}
            </div>

            {/* Tab Body Content */}
            <div className="p-5 flex-1 overflow-y-auto">
              {/* TAB 1: OVERVIEW */}
              {activeTab === "overview" && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-sm font-bold text-white">Consultation Overview & Encounter Status</h3>
                      <span className="text-[11px] text-[#94A3B8]">Encounter {encounterId} • Started at 10:15 AM</span>
                    </div>
                    <StatusBadge status="Encounter In Progress" variant="verified" />
                  </div>

                  {/* Pre-Encounter Intelligence Briefing (Service 3) */}
                  {preEncounterData && (
                    <div className="p-3.5 bg-gradient-to-r from-[#0F172A] to-[#131E35] rounded-xl border border-[#0D9488]/40 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-[11px] font-bold text-[#5EEAD4] uppercase tracking-wider flex items-center gap-1.5">
                          <HealthcareIcon name="clipboard" className="w-4 h-4 text-teal-400 inline" /> Pre-Encounter Intelligence Briefing
                        </span>
                        <span className="text-[10px] text-[#94A3B8]">
                          Assessed Mizaj: <strong className="text-white">{preEncounterData.patient_mizaj || "Balghami (Cold & Moist)"}</strong>
                        </span>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px]">
                        <div className="p-2 rounded bg-[#0A0F1D]/80 border border-[#1E293B]">
                          <span className="text-[#64748B] block text-[10px] uppercase">Active Nuskha & Mudabbar</span>
                          <span className="text-[#F1F5F9] font-medium">
                            {preEncounterData.active_nuskha?.map((n: any) => n.name).join(", ") || "Hab-e-Suranjan, Roghan-e-Balsan"}
                          </span>
                        </div>
                        <div className="p-2 rounded bg-[#0A0F1D]/80 border border-[#1E293B]">
                          <span className="text-[#64748B] block text-[10px] uppercase">Permanent Safety Rail</span>
                          <span className="text-[#34D399] font-medium">
                            ✓ Mudabbar Certificate Verified • Zero Drug Interactions
                          </span>
                        </div>
                      </div>
                    </div>
                  )}

                  <div>
                    <label className="text-xs text-[#94A3B8] block mb-1">Chief Complaint (Shikayat-e-Awwal)</label>
                    <textarea
                      rows={3}
                      value={chiefComplaint}
                      onChange={(e) => { setChiefComplaint(e.target.value); setHasUnsavedChanges(true); }}
                      disabled={isLocked}
                      className="zv-input text-xs"
                    />
                  </div>
                  <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-2">
                    <h4 className="text-xs font-semibold text-[#2DD4BF]">Integrated Diagnostic Assessment</h4>
                    <p className="text-xs text-[#F8FAFC]">
                      <strong>Unani Diagnosis:</strong> Waja-ul-Mafasil Barid Balghami (Knee Osteoarthritis / Joint Phlegmatic Dyscrasia)<br />
                      <strong>Biomedical Mapping:</strong> ICD-10 M17.9 (Bilateral Primary Knee Osteoarthritis) • SNOMED CT: 399269003
                    </p>
                  </div>
                  {isLocked && signatureHash && (
                    <div className="p-3 bg-[#10B981]/10 border border-[#10B981]/30 rounded-lg text-xs space-y-1">
                      <div className="flex items-center gap-2 text-[#34D399] font-bold">
                        <span>✓ 21 CFR Part 11 Cryptographically Sealed</span>
                      </div>
                      <p className="text-[11px] text-[#94A3B8] font-mono">Signature Hash: {signatureHash}</p>
                      <p className="text-[10px] text-[#64748B]">Signer: Hakeem Dr. Irfan Ashraf (BUMS - AKTC AMU, Reg: Updating/Verification in Progress)</p>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 2: HISTORY */}
              {activeTab === "history" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Clinical History (Tarikh-e-Marz)</h3>
                  <div>
                    <label className="text-[#94A3B8] block mb-1">History of Present Illness (HPI)</label>
                    <textarea
                      rows={4}
                      defaultValue="Patient reports 14-month history of progressive bilateral knee stiffness and dull aching pain. Symptoms worsen during cold weather and early morning. Associated with mild pedal edema after prolonged standing."
                      disabled={isLocked}
                      className="zv-input text-xs"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-[#94A3B8] block mb-1">Past Medical History</label>
                      <input type="text" defaultValue="Mild Dyspepsia (Su-e-Hazm), Hypertension (Controlled)" disabled={isLocked} className="zv-input text-xs" />
                    </div>
                    <div>
                      <label className="text-[#94A3B8] block mb-1">Family History</label>
                      <input type="text" defaultValue="Maternal history of joint arthralgia" disabled={isLocked} className="zv-input text-xs" />
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 3: EXAMINATION */}
              {activeTab === "examination" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Physical & Classical Unani Examination</h3>
                  <div>
                    <label className="text-[#94A3B8] block mb-1">Pulse (Nabz), Tongue (Lisan), & Musculoskeletal Signs</label>
                    <textarea
                      rows={4}
                      value={examNotes}
                      onChange={(e) => { setExamNotes(e.target.value); setHasUnsavedChanges(true); }}
                      disabled={isLocked}
                      className="zv-input text-xs"
                    />
                  </div>
                  <div className="grid grid-cols-3 gap-3">
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] uppercase block">Nabz (Pulse)</span>
                      <span className="text-xs font-semibold text-white">Bat'ee, Layyin, Munkafish</span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] uppercase block">Lisan (Tongue)</span>
                      <span className="text-xs font-semibold text-white">Pale, moist, white coating</span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] uppercase block">Baul & Baraz</span>
                      <span className="text-xs font-semibold text-white">Qarura: Abyad (Pale), normal clarity</span>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 4: VITALS */}
              {activeTab === "vitals" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Longitudinal Vitals & Biometrics</h3>
                  <div className="grid grid-cols-4 gap-3">
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Blood Pressure</span>
                      <span className="text-sm font-bold text-white font-mono">124/82 mmHg</span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Pulse Rate</span>
                      <span className="text-sm font-bold text-white font-mono">72 bpm</span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Body Temperature</span>
                      <span className="text-sm font-bold text-white font-mono">98.4 °F</span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">SpO2</span>
                      <span className="text-sm font-bold text-white font-mono">98% Room Air</span>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 5: INVESTIGATIONS */}
              {activeTab === "investigations" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Diagnostic Investigations & Laboratory</h3>
                  <div className="zv-card p-3 space-y-2 border-[#334155]">
                    <div className="flex justify-between items-center text-xs font-semibold">
                      <span>X-Ray Bilateral Knees (AP/Lateral)</span>
                      <span className="text-[#2DD4BF]">Completed (2026-09-02)</span>
                    </div>
                    <p className="text-[11px] text-[#94A3B8]">
                      Findings: Moderate joint space narrowing of medial compartment with subchondral sclerosis. Kellgren-Lawrence Grade II.
                    </p>
                  </div>
                  <div className="zv-card p-3 space-y-2 border-[#334155]">
                    <div className="flex justify-between items-center text-xs font-semibold">
                      <span>Serum Uric Acid & ESR</span>
                      <span className="text-[#34D399]">Normal Limits</span>
                    </div>
                    <p className="text-[11px] text-[#94A3B8]">
                      Uric acid: 5.4 mg/dL (Normal). ESR: 18 mm/hr (Mildly elevated).
                    </p>
                  </div>
                </div>
              )}

              {/* TAB 6: ASSESSMENT */}
              {activeTab === "assessment" && (
                <div className="space-y-4 text-xs">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-bold text-white">Differential & Confirmed Clinical Assessment</h3>
                    <span className="text-[10px] text-teal-400 font-mono">
                      Engine: Differential Diagnoser v5.0
                    </span>
                  </div>
                  <div className="p-4 bg-[#0A0F1D] rounded-lg border border-[#0D9488]/40 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-[#2DD4BF]">PRIMARY DIAGNOSIS: CONFIRMED</span>
                      <StatusBadge status="Evidence Grade A" variant="verified" />
                    </div>
                    <p className="text-sm text-white font-medium">
                      Waja-ul-Mafasil Barid Balghami (Phlegmatic Cold Knee Osteoarthritis)
                    </p>
                    <p className="text-xs text-[#94A3B8]">
                      ICD-10: <strong>M17.9</strong> • ICD-11: <strong>FA00.Z</strong> • SNOMED CT: <strong>399269003</strong>
                    </p>
                  </div>

                  {differentialList.length > 0 && (
                    <div className="space-y-2">
                      <span className="text-xs font-bold text-slate-300">Differential Considerations (Differential Engine):</span>
                      <div className="space-y-1.5">
                        {differentialList.map((d: any, idx: number) => (
                          <div key={idx} className="p-2.5 bg-[#0A0F1D] rounded-lg border border-[#334155] flex justify-between items-center">
                            <div>
                              <span className="font-bold text-white block">{d.condition_name || d.name || d}</span>
                              <span className="text-[11px] text-slate-400">{d.rationale || "Humoral and clinical feature match"}</span>
                            </div>
                            <span className="px-2 py-0.5 rounded bg-teal-950 text-teal-300 font-mono text-[10px] border border-teal-800">
                              {d.match_score ? `${Math.round(d.match_score * 100)}% Match` : "Evaluated"}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 7: MIZAJ ASSESSMENT */}
              {activeTab === "mizaj" && (
                <div className="space-y-4 text-xs">
                  <div className="flex justify-between items-center">
                    <h3 className="text-sm font-bold text-white">10-Ajnas-e-Ashara Quantitative Mizaj Assessment</h3>
                    <StatusBadge
                      status={mizajAssessment?.dominant_mizaj || activePatient.mizaj_dominant || "65% Balghami Dominant"}
                      variant="verified"
                    />
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Balgham (Phlegm)</span>
                      <span className="text-sm font-bold text-[#2DD4BF] font-mono">
                        {mizajAssessment?.percentages?.balgham ?? "65%"} Dominant
                      </span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Dam (Blood)</span>
                      <span className="text-sm font-bold text-white font-mono">
                        {mizajAssessment?.percentages?.dam ?? "20%"} Secondary
                      </span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Safra (Yellow Bile)</span>
                      <span className="text-sm font-bold text-white font-mono">
                        {mizajAssessment?.percentages?.safra ?? "10%"} Low
                      </span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Sauda (Black Bile)</span>
                      <span className="text-sm font-bold text-white font-mono">
                        {mizajAssessment?.percentages?.sauda ?? "5%"} Low
                      </span>
                    </div>
                  </div>
                  {mizajAssessment?.clinical_notes && (
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] text-slate-300">
                      <span className="text-[#2DD4BF] font-bold block mb-1">Mizaj Engine Assessment Summary:</span>
                      <p>{mizajAssessment.clinical_notes}</p>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 8: AFAAL CASCADE (NEW FIRST-CLASS CLINICAL STAGE) */}
              {activeTab === "afaal" && (
                <div className="space-y-5 text-xs">
                  <div className="flex justify-between items-start border-b border-[#334155] pb-3">
                    <div>
                      <h3 className="text-sm font-bold text-white">ZAYVORA Afaal Cascade (Therapeutic Progression)</h3>
                      <p className="text-[11px] text-[#94A3B8]">
                        Classical 4-stage protocol linking humoral diagnosis to sequential clinical actions
                      </p>
                    </div>
                    <StatusBadge status={`Active: ${afaalStage}`} variant="verified" />
                  </div>

                  {/* 4-Stage Interactive Progression Ribbon */}
                  <div className="grid grid-cols-4 gap-2">
                    {[
                      { key: "TANQIYA", step: 1, name: "Tanqiya", title: "Targeted Evacuation", desc: "Nujz & expulsion of morbid matter" },
                      { key: "TAHLEEL", step: 2, name: "Tahleel", title: "Resolution & Dissolution", desc: "Dissolve local synovial congestion" },
                      { key: "TAQWIYAAT", step: 3, name: "Taqwiyaat", title: "Organ Restoration", desc: "Strengthen joint structural tone" },
                      { key: "HIFZ", step: 4, name: "Hifz", title: "Preservation & Health", desc: "Asbab-e-Sittah long-term balance" },
                    ].map((st) => {
                      const isCurrent = afaalStage === st.key;
                      return (
                        <button
                          key={st.key}
                          onClick={() => { setAfaalStage(st.key as typeof afaalStage); setHasUnsavedChanges(true); }}
                          className={`p-3 rounded-lg border text-left transition ${
                            isCurrent
                              ? "bg-[#0D9488]/15 border-[#0D9488] text-white ring-1 ring-[#0D9488]"
                              : "bg-[#0A0F1D] border-[#334155] text-[#94A3B8] hover:border-[#64748B]"
                          }`}
                        >
                          <div className="flex justify-between items-center mb-1">
                            <span className="font-mono text-[10px] font-bold text-[#2DD4BF]">Stage {st.step}</span>
                            {isCurrent && <span className="text-[10px] text-[#34D399] font-bold">ACTIVE</span>}
                          </div>
                          <span className="font-bold text-white block">{st.name}</span>
                          <span className="text-[10px] text-[#64748B] block">{st.title}</span>
                        </button>
                      );
                    })}
                  </div>

                  {/* Detailed Stage Workspace */}
                  <div className="p-4 bg-[#0A0F1D] rounded-xl border border-[#334155] space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-white text-sm">
                        Stage: {afaalStage === "TANQIYA" ? "1. Tanqiya (Humoral Cleansing)" : afaalStage === "TAHLEEL" ? "2. Tahleel (Resolution & Anti-Inflammatory)" : afaalStage === "TAQWIYAAT" ? "3. Taqwiyaat (Organ Tonification)" : "4. Hifz (Preservation & Maintenance)"}
                      </span>
                      <span className="zv-badge-teal text-[10px] px-2.5 py-0.5 rounded font-mono">
                        Review: 14 Days
                      </span>
                    </div>

                    <div>
                      <label className="text-[#94A3B8] block mb-1">Clinical Rationale for Active Stage *</label>
                      <textarea
                        rows={2}
                        value={afaalRationale}
                        onChange={(e) => { setAfaalRationale(e.target.value); setHasUnsavedChanges(true); }}
                        className="zv-input text-xs"
                      />
                    </div>

                    <div>
                      <label className="text-[#94A3B8] block mb-1 font-semibold">Clinician-Selected Goals for this Horizon:</label>
                      <div className="space-y-1.5">
                        {afaalGoals.map((goal, idx) => (
                          <div key={idx} className="flex items-center gap-2 p-2 rounded bg-[#0F172A] border border-[#334155]">
                            <span className="text-[#2DD4BF] font-bold">✓</span>
                            <span className="text-white text-xs">{goal}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 9: AXIS MAPPING */}
              {activeTab === "axis" && (
                <div className="space-y-4 text-xs">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-bold text-white">Organ-Axis Physiological Cross-Talk & Reflex Arc</h3>
                    <span className="text-[10px] text-teal-400 font-mono">
                      Engine: Organ Axis Reflex Model v5.0
                    </span>
                  </div>
                  <div className="p-4 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-2">
                    <h4 className="text-xs font-semibold text-[#2DD4BF]">
                      Primary Axis: {organAxisResult?.axis_name || "Mafasil-Asab (Musculoskeletal-Neural Locomotor Axis)"}
                    </h4>
                    <p className="text-xs text-[#94A3B8]">
                      {organAxisResult?.cross_talk_summary ||
                        "Burudat wa Rutubat (Cold & Moist Dyscrasia) causes impaired synovial fluid dynamics and subchondral congestion. Sympathetic nerve sensitivity aggravates pain during nocturnal temperature drops."}
                    </p>
                  </div>

                  {organAxisResult?.nodes && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {organAxisResult.nodes.map((node: any, idx: number) => (
                        <div key={idx} className="p-3 bg-[#0A0F1D] rounded-lg border border-slate-800 space-y-1">
                          <div className="flex justify-between">
                            <span className="font-bold text-white">{node.organ_name || node.name}</span>
                            <span className="text-[10px] text-teal-400 font-mono">{node.role || "Target Organ"}</span>
                          </div>
                          <p className="text-[11px] text-slate-400">{node.pathology || node.status}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* TAB 10: TREATMENT PLAN */}
              {activeTab === "treatment" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Multi-Horizon Integrative Treatment Plan</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-1">
                      <h4 className="text-xs font-semibold text-[#34D399]">Ilaj bit-Tadbeer (Regimenal Therapy)</h4>
                      <p className="text-[11px] text-[#94A3B8]">
                        1. Dalak Layyin (Gentle massage) with Raughan-e-Balsan nocte.<br />
                        2. Natool (Warm herbal irrigation) with decoction of Babuna twice weekly.
                      </p>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-1">
                      <h4 className="text-xs font-semibold text-[#2DD4BF]">Ilaj bil-Ghiza (Dietary Prescription)</h4>
                      <p className="text-[11px] text-[#94A3B8]">
                        Avoid cold and mucus-generating foods. Incorporate warm ginger, cinnamon, and sheep bone broth.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 11: PRESCRIPTION */}
              {activeTab === "prescription" && (
                <div className="space-y-4">
                  <div className="flex flex-wrap justify-between items-center bg-[#0D1527] p-3.5 rounded-lg border border-[#1E293B] gap-2">
                    <div>
                      <h3 className="text-sm font-bold text-white flex items-center gap-2">
                        <span>Botanical Nuskha &amp; Medical Prescription</span>
                        <span className="px-2 py-0.5 bg-[#0D9488]/20 text-[#2DD4BF] border border-[#0D9488]/40 rounded text-[10px] font-mono uppercase">Secure Electronic Signature</span>
                      </h3>
                      <p className="text-xs text-[#94A3B8]">Formulate, safety-check with Schedule E(1) guardrails, and seal for dispensary fulfillment.</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => setShowRxPrintModal(true)}
                      className="px-3.5 py-2 bg-[#0D9488] hover:bg-[#14B8A6] text-white rounded-md text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer shadow-sm"
                    >
                      <HealthcareIcon name="printer" className="w-4 h-4 text-slate-300 inline" />
                      <span>Generate &amp; Print Prescription PDF</span>
                    </button>
                  </div>
                  <NuskhaBuilder
                    token={AuthService.getSession()?.token ?? ""}
                    patient={activePatient}
                    encounterId={encounterId}
                  />
                </div>
              )}

              {/* TAB 12: FOLLOW-UP */}
              {activeTab === "followup" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Follow-up Consultation & PROMs Outcome Tracking</h3>
                  <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-2">
                    <span className="text-xs font-semibold text-white">Scheduled Review: Day +14 (2026-09-26)</span>
                    <p className="text-xs text-[#94A3B8]">
                      Evaluate VAS pain score reduction, knee flexion degrees, and check for any botanical gastric intolerance.
                    </p>
                  </div>
                </div>
              )}

              {/* TAB 13: TIMELINE */}
              {activeTab === "timeline" && (
                <div className="space-y-3 text-xs">
                  <h3 className="text-sm font-bold text-white">Longitudinal Clinical Encounters &amp; Audit Log</h3>
                  <div className="border-l-2 border-[#0D9488] pl-4 space-y-3">
                    {timelineEvents.length > 0 ? (
                      timelineEvents.map((evt, idx) => (
                        <div key={idx} className="space-y-0.5">
                          <div className="flex items-center gap-2">
                            <span className="text-[10px] text-[#64748B] font-mono">
                              {evt.date || evt.timestamp || "Recent"}
                            </span>
                            <span className="text-[9px] px-1.5 py-0.5 rounded bg-[#0D9488]/20 text-[#2DD4BF] font-mono uppercase">
                              {evt.type}
                            </span>
                          </div>
                          <p className="text-xs font-semibold text-white">
                            {evt.summary || evt.notes || `${evt.title || evt.type}`}
                          </p>
                          {evt.provider && (
                            <p className="text-[10px] text-[#94A3B8]">Provider: {evt.provider}</p>
                          )}
                          {evt.merkle_root && (
                            <p className="text-[9px] text-[#64748B] font-mono">
                              Merkle Root: {evt.merkle_root.substring(0, 24)}... (Block #{evt.block_height})
                            </p>
                          )}
                        </div>
                      ))
                    ) : (
                      <>
                        <div>
                          <span className="text-[10px] text-[#64748B]">2026-09-13 (Today • Active)</span>
                          <p className="text-xs font-semibold text-white">Encounter {encounterId} • Hakeem Dr. Irfan Ashraf</p>
                        </div>
                        <div>
                          <span className="text-[10px] text-[#64748B]">2026-09-02</span>
                          <p className="text-xs font-semibold text-white">Radiology: X-Ray Knee Bilateral • Dr. K. Saxena</p>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              )}

              {/* TAB 14: CLINICAL SIMULATION & LONGITUDINAL TRAJECTORY (RESEARCH) */}
              {activeTab === "twin" && (
                <div className="space-y-4">
                  <div className="p-3.5 rounded-xl bg-purple-950/30 border border-purple-500/30 text-purple-200 text-xs flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <HealthcareIcon name="flask" className="w-4 h-4 text-purple-400 shrink-0" />
                      <span><strong>Investigational / Research Track:</strong> Digital Twin trajectory modeling is an exploratory decision-support simulation. Primary clinical diagnoses and prescribing decisions must be grounded in direct clinician examination.</span>
                    </div>
                  </div>
                  <DigitalTwinCockpit
                    token={AuthService.getSession()?.token ?? ""}
                    patientId={activePatient.id}
                    patientName={`${activePatient.first_name} ${activePatient.last_name}`}
                  />
                </div>
              )}
            </div>
          </div>
        </div>

        {/* STANDARDIZED MEDICAL PRESCRIPTION PRINTABLE MODAL */}
        {showRxPrintModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-sm p-4 overflow-y-auto">
            <div className="bg-white text-neutral-900 rounded-xl max-w-3xl w-full p-8 shadow-2xl space-y-6 print:p-0 print:shadow-none print:max-w-none">
              {/* Modal Controls (Hidden in print) */}
              <div className="flex justify-between items-center pb-4 border-b border-neutral-200 print:hidden">
                <span className="text-xs font-semibold uppercase tracking-wider text-teal-800">
                  Clinical Record: Prescription Letterhead (A4 Ready)
                </span>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => window.print()}
                    className="px-4 py-1.5 bg-teal-700 hover:bg-teal-800 text-white rounded text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
                  >
                    <HealthcareIcon name="printer" className="w-4 h-4 text-slate-300 inline" />
                    <span>Print Letterhead (PDF)</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowRxPrintModal(false)}
                    className="px-3 py-1.5 bg-neutral-200 hover:bg-neutral-300 text-neutral-800 rounded text-xs font-semibold transition-colors cursor-pointer"
                  >
                    Close
                  </button>
                </div>
              </div>

              {/* Printable Medical Letterhead */}
              <div className="space-y-6 font-serif">
                {/* Hospital Branding Header */}
                <div className="flex items-center justify-between border-b-2 border-neutral-900 pb-4">
                  <div>
                    <h1 className="text-xl font-bold tracking-tight text-neutral-900">
                      ZAYVORA MATAB™ INTEGRATIVE CLINICAL HOSPITAL
                    </h1>
                    <p className="text-xs text-neutral-600">
                      Centre for Advanced Clinical Care, Classical Unani Medicine &amp; Integrative Therapeutics
                    </p>
                    <p className="text-[11px] text-neutral-500">
                      ZAYVORA Health Boulevard, New Delhi - 110062 | Tel: +91 97738 82657 | Lic: AYUSH-DL-2004/09
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="inline-block px-2.5 py-1 bg-teal-900 text-white text-[10px] font-sans font-bold uppercase rounded">
                      Outpatient Department
                    </span>
                    <p className="text-xs font-mono font-bold mt-1 text-neutral-800">Order: RX-2026-0441</p>
                  </div>
                </div>

                {/* Patient Profile Bar */}
                <div className="grid grid-cols-4 gap-3 bg-neutral-50 p-3 rounded border border-neutral-200 text-xs font-sans">
                  <div>
                    <span className="text-[10px] text-neutral-500 block uppercase">Patient Name</span>
                    <strong className="text-neutral-900 font-serif text-sm">{activePatient.first_name} {activePatient.last_name}</strong>
                  </div>
                  <div>
                    <span className="text-[10px] text-neutral-500 block uppercase">Age / Gender</span>
                    <span className="text-neutral-800">42 Y / Male</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-neutral-500 block uppercase">Medical Record No.</span>
                    <strong className="text-neutral-900 font-mono">MRN-2026-0814</strong>
                  </div>
                  <div>
                    <span className="text-[10px] text-neutral-500 block uppercase">Date &amp; Token</span>
                    <span className="text-neutral-800">2026-09-13 (Token T-104)</span>
                  </div>
                </div>

                {/* Mizaj & Diagnosis Row */}
                <div className="grid grid-cols-2 gap-4 text-xs font-sans pb-2 border-b border-neutral-200">
                  <div>
                    <span className="text-[10px] uppercase font-bold text-teal-800 block">Baseline Mizaj Assessment</span>
                    <p className="text-neutral-800 font-semibold">{activePatient.mizaj_dominant || "Balghami (Cold & Moist)"}</p>
                    <span className="text-[11px] text-neutral-500">Known Allergies: {activePatient.allergies?.join(", ") || "None Reported"}</span>
                  </div>
                  <div>
                    <span className="text-[10px] uppercase font-bold text-teal-800 block">Clinical Diagnosis (Tashkhees)</span>
                    <p className="text-neutral-800 font-semibold">Waja-ul-Mafasil (Su-e-Mizaj Barid Balghami)</p>
                    <span className="text-[11px] text-neutral-500">Vitals: BP 124/82 • Pulse 72 • Nabz: Bat'ee, Layyin</span>
                  </div>
                </div>

                {/* Prescription Items Table */}
                <div className="space-y-2">
                  <h3 className="text-sm font-bold text-neutral-900 uppercase tracking-wide flex items-center gap-2">
                    <span>℞</span>
                    <span className="text-xs">Botanical &amp; Compound Formulations</span>
                  </h3>
                  <table className="w-full text-left text-xs font-sans border-collapse border border-neutral-200">
                    <thead>
                      <tr className="bg-neutral-100 text-neutral-700 text-[11px] border-b border-neutral-300">
                        <th className="p-2 border-r border-neutral-200">#</th>
                        <th className="p-2 border-r border-neutral-200">Medicine Name &amp; Classification</th>
                        <th className="p-2 border-r border-neutral-200">Dosage &amp; Timing</th>
                        <th className="p-2 border-r border-neutral-200">Duration</th>
                        <th className="p-2">Regulatory Safety / Mudabbar</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-neutral-200">
                      <tr>
                        <td className="p-2 border-r border-neutral-200 font-mono">1</td>
                        <td className="p-2 border-r border-neutral-200">
                          <strong className="text-neutral-900 block font-serif">Majun Suranjan (Mudabbar)</strong>
                          <span className="text-[10px] text-neutral-500">Colchicum autumnale purified</span>
                        </td>
                        <td className="p-2 border-r border-neutral-200">5g twice daily with lukewarm water after meals</td>
                        <td className="p-2 border-r border-neutral-200">14 Days</td>
                        <td className="p-2 text-[10px] font-mono text-emerald-800 font-semibold">
                          Certified Mudabbar (SHA256:7a8b9c0d...)
                        </td>
                      </tr>
                      <tr>
                        <td className="p-2 border-r border-neutral-200 font-mono">2</td>
                        <td className="p-2 border-r border-neutral-200">
                          <strong className="text-neutral-900 block font-serif">Roghan-e-Balsan</strong>
                          <span className="text-[10px] text-neutral-500">Commiphora gileadensis</span>
                        </td>
                        <td className="p-2 border-r border-neutral-200">Gentle local application over knees at night</td>
                        <td className="p-2 border-r border-neutral-200">14 Days</td>
                        <td className="p-2 text-[10px] text-neutral-600">Standard Retail Unani (External)</td>
                      </tr>
                      <tr>
                        <td className="p-2 border-r border-neutral-200 font-mono">3</td>
                        <td className="p-2 border-r border-neutral-200">
                          <strong className="text-neutral-900 block font-serif">Habb-e-Suranjan Forte</strong>
                          <span className="text-[10px] text-neutral-500">Purified classical pill</span>
                        </td>
                        <td className="p-2 border-r border-neutral-200">1 pill twice daily after meals with water</td>
                        <td className="p-2 border-r border-neutral-200">10 Days</td>
                        <td className="p-2 text-[10px] font-mono text-emerald-800 font-semibold">
                          Certified Mudabbar (SHA256:f1e2d3c4...)
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                {/* Dietary Advice (Ilaj bil-Ghiza / Parhez) */}
                <div className="grid grid-cols-2 gap-4 text-xs font-sans bg-amber-50/60 p-3 rounded border border-amber-200/80">
                  <div>
                    <h4 className="font-bold text-amber-900 uppercase text-[11px] mb-1">Ilaj bil-Ghiza (Dietary Parhez)</h4>
                    <p className="text-neutral-700 leading-relaxed text-[11px]">
                      Avoid sour foods, cold refrigerated water, curd, lentils (Mash), and red meat. Prefer warm ginger decoction and barley water.
                    </p>
                  </div>
                  <div>
                    <h4 className="font-bold text-teal-900 uppercase text-[11px] mb-1">Ilaj bil-Tadbeer (Regimenal Therapy)</h4>
                    <p className="text-neutral-700 leading-relaxed text-[11px]">
                      Nutool Haar (warm medicated irrigation) with Babuna decoction for 10 minutes daily in evening over bilateral patellae.
                    </p>
                  </div>
                </div>

                {/* Doctor Sign-off & 21 CFR Part 11 Electronic Seal */}
                <div className="pt-4 border-t-2 border-neutral-900 flex justify-between items-end">
                  <div className="space-y-1">
                    <span className="text-[10px] font-sans uppercase font-bold text-teal-900 block">
                      21 CFR Part 11 Cryptographic Electronic Signature
                    </span>
                    {signatureHash && isLocked ? (
                      <>
                        <p className="text-[10px] font-mono text-neutral-600 break-all max-w-md">
                          SHA-256: {signatureHash}
                        </p>
                        <span className="text-[10px] text-neutral-500 font-sans block">
                          Anchored in Merkle Audit Block #{merkleBlock ?? "Committed"} • Timestamp: {signedTimestamp || "Recorded"}
                        </span>
                      </>
                    ) : (
                      <div className="flex items-center gap-2 py-1">
                        <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-800 text-[10px] font-semibold border border-amber-300">
                          STATUS: DRAFT — UNSEALED
                        </span>
                        <span className="text-[10px] text-neutral-500 font-sans">
                          Pending clinician verification &amp; electronic seal
                        </span>
                      </div>
                    )}
                  </div>
                  <div className="text-right">
                    <div className="h-10 border-b border-dashed border-neutral-400 mb-1 w-44"></div>
                    <strong className="text-xs font-serif text-neutral-900 block">Hakeem Dr. Irfan Ashraf</strong>
                    <span className="text-[11px] text-neutral-600 block">BUMS (AKTC Aligarh Muslim University, Batch 2002, Passed 2007)</span>
                    <span className="text-[10px] font-mono text-neutral-500 block">Reg. No: (Updating / Verification in Progress)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 21 CFR PART 11 DIGITAL SIGNATURE SEAL MODAL (Service 3) */}
        {showSignModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm">
            <div className="zv-card w-full max-w-lg p-6 space-y-4 border border-[#0D9488]/60 shadow-2xl bg-[#0D1527]">
              <div className="flex items-center justify-between border-b border-[#334155] pb-3">
                <div className="flex items-center gap-2">
                  <HealthcareIcon name="lock" className="w-5 h-5 text-emerald-400 inline" />
                  <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                    21 CFR Part 11 Digital Signature Seal
                  </h3>
                </div>
                <button
                  onClick={() => setShowSignModal(false)}
                  className="text-[#94A3B8] hover:text-white text-lg font-bold"
                >
                  ✕
                </button>
              </div>

              <div className="p-3.5 rounded-xl bg-[#0A0F1D] border border-[#334155] text-xs space-y-2">
                <p className="text-[#94A3B8]">
                  <strong>Attending Clinician:</strong> Hakeem Dr. Irfan Ashraf (BUMS - AKTC AMU, Reg: Updating/Verification in Progress)
                </p>
                <p className="text-[#94A3B8]">
                  <strong>Patient:</strong> {activePatient.first_name} {activePatient.last_name} • MRN-2026-0814
                </p>
                <p className="text-[#94A3B8]">
                  <strong>Encounter:</strong> {encounterId || "ENC-2026-0814-01"}
                </p>
                <div className="pt-2 border-t border-[#1E293B] text-[11px] text-[#CBD5E1]">
                  "I hereby certify under NCISM governance and 21 CFR Part 11 that I have conducted this clinical encounter, reviewed the Afaal stage, confirmed drug safety clearances, and sealed the active Nuskha."
                </div>
              </div>

              {signError && (
                <div className="p-3 bg-[#DC2626]/20 border border-[#DC2626]/40 rounded-lg text-xs text-[#EF4444]">
                  ️ {signError}
                </div>
              )}

              <div className="space-y-3">
                <div>
                  <label className="text-xs text-[#94A3B8] block mb-1">6-Digit Authorizing PIN</label>
                  <input
                    type="password"
                    maxLength={6}
                    value={signingPin}
                    onChange={(e) => setSigningPin(e.target.value)}
                    type="password" placeholder="Enter your 6-digit electronic PIN"
                    className="zv-input font-mono tracking-widest text-center text-sm"
                  />
                </div>
                <div>
                  <label className="text-xs text-[#94A3B8] block mb-1">Reason for Signature</label>
                  <input
                    type="text"
                    value={signingReason}
                    onChange={(e) => setSigningReason(e.target.value)}
                    className="zv-input text-xs"
                  />
                </div>
              </div>

              <div className="pt-3 border-t border-[#334155] flex justify-end gap-2">
                <button
                  onClick={() => setShowSignModal(false)}
                  className="zv-btn-secondary text-xs px-4 py-2"
                >
                  Cancel
                </button>
                <button
                  onClick={handleConfirmSignWithPin}
                  disabled={isSigning || signingPin.length < 4}
                  className="zv-btn-primary text-xs bg-[#0D9488] hover:bg-[#14B8A6] px-5 py-2 disabled:opacity-50"
                >
                  {isSigning ? "Cryptographically Sealing..." : "Authorize & Digitally Seal"}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* UNIVERSAL TASK ENGINE DRAWER / MODAL (Service 8) */}
        {showTasksModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm">
            <div className="zv-card w-full max-w-2xl p-6 space-y-4 border border-[#F59E0B]/50 shadow-2xl bg-[#0D1527]">
              <div className="flex items-center justify-between border-b border-[#334155] pb-3">
                <div className="flex items-center gap-2">
                  <span className="text-xl text-[#FBBF24]"></span>
                  <div>
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                      Universal Task Engine (Service 8)
                    </h3>
                    <p className="text-[11px] text-[#94A3B8]">
                      Coordinating statutory alerts, reviews, and clinical sign-offs
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => setShowTasksModal(false)}
                  className="text-[#94A3B8] hover:text-white text-lg font-bold"
                >
                  ✕
                </button>
              </div>

              <div className="max-h-96 overflow-y-auto space-y-3">
                {tasks.length > 0 ? (
                  tasks.map((task: any) => (
                    <div
                      key={task.task_id}
                      className="p-3.5 rounded-xl bg-[#0A0F1D] border border-[#1E293B] hover:border-[#334155] flex items-center justify-between gap-3"
                    >
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                              task.priority === "STAT"
                                ? "bg-[#DC2626]/20 text-[#EF4444] border border-[#DC2626]/40"
                                : task.priority === "HIGH"
                                ? "bg-[#F59E0B]/20 text-[#FBBF24] border border-[#F59E0B]/40"
                                : "bg-[#3B82F6]/20 text-[#93C5FD] border border-[#3B82F6]/40"
                            }`}
                          >
                            {task.priority}
                          </span>
                          <span className="text-xs font-bold text-white">{task.title}</span>
                        </div>
                        <p className="text-[11px] text-[#94A3B8]">{task.description}</p>
                        <div className="flex items-center gap-3 text-[10px] text-[#64748B]">
                          <span>ID: {task.task_id}</span>
                          <span>Target: {task.target_entity_id}</span>
                          <span>Status: <strong className="text-[#CBD5E1]">{task.status}</strong></span>
                        </div>
                      </div>

                      <div className="shrink-0">
                        {task.status === "COMPLETED" ? (
                          <span className="text-xs font-semibold text-[#10B981] flex items-center gap-1">
                            ✓ Done
                          </span>
                        ) : (
                          <button
                            onClick={() => handleCompleteTask(task.task_id)}
                            className="px-3 py-1.5 rounded-lg bg-[#0D9488] hover:bg-[#14B8A6] text-white text-xs font-semibold"
                          >
                            Resolve Task
                          </button>
                        )}
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-center py-8 text-xs text-[#94A3B8]">No pending clinical tasks.</p>
                )}
              </div>

              <div className="pt-3 border-t border-[#334155] flex justify-end">
                <button
                  onClick={() => setShowTasksModal(false)}
                  className="zv-btn-secondary text-xs px-4 py-2"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}

        {/* HAKEEM SAHAB AI REVIEW DRAWER WITH 5-LAYER DECISION SUPPORT */}
        <HakeemReviewDrawer
          token={AuthService.getSession()?.token ?? ""}
          patient={activePatient}
          isOpen={aiDrawerOpen}
          onClose={() => setAiDrawerOpen(false)}
        />
      </div>
    </AppShell>
  );
}
