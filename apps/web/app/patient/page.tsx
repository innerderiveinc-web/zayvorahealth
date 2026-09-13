"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";
import {
  MOCK_PATIENT_PROFILE,
  MOCK_PATIENT_APPOINTMENT,
  MOCK_ACTIVE_CARE_PLAN,
  MOCK_PRESCRIPTIONS,
  MOCK_LAB_REPORTS,
  MOCK_PATIENT_MESSAGES,
  MOCK_PATIENT_INVOICES,
  PatientAppointment,
  PatientLabReport,
  PatientMessage
} from "@/lib/cms/patientMockData";

type PatientSection =
  | "overview"
  | "profile"
  | "appointments"
  | "consultations"
  | "ai-doctor"
  | "protocols"
  | "prescriptions"
  | "medicines"
  | "reports"
  | "treatment-plans"
  | "lifestyle"
  | "messages"
  | "billing";

export default function PatientPortalPage() {
  const [activeTab, setActiveTab] = useState<PatientSection>("overview");

  // Voice Posology States
  const [audioLang, setAudioLang] = useState<"urdu" | "hindi" | "english">("urdu");
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  // Appointments State
  const [appointments, setAppointments] = useState<PatientAppointment[]>([
    MOCK_PATIENT_APPOINTMENT,
    {
      id: "APT-2026-0792",
      doctorName: "Dr. Aisha Siddiqui",
      doctorSpecialty: "Tahaffuzi wa Samaji Tibb (Preventive Medicine)",
      date: "2026-08-10",
      timeSlot: "11:30 AM – 12:00 PM",
      mode: "In-Clinic OPD",
      facilityLocation: "Jamia Hamdard AUTC - Main Hospital, OPD Room 2",
      tokenNumber: "T-089",
      status: "Completed"
    }
  ]);
  const [showRescheduleModal, setShowRescheduleModal] = useState(false);
  const [rescheduleDate, setRescheduleDate] = useState("2026-09-22");
  const [rescheduleSlot, setRescheduleSlot] = useState("11:00 AM – 11:30 AM");

  // Diagnostic Reports State & Upload Modal
  const [reports, setReports] = useState<PatientLabReport[]>(MOCK_LAB_REPORTS);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [newReportTitle, setNewReportTitle] = useState("");
  const [newReportLab, setNewReportLab] = useState("Dr. Lal PathLabs, Okhla");

  // Asbab Sittah Lifestyle Tracker
  const [asbabScores, setAsbabScores] = useState({
    air: 4,       // Hawa-e-Muheet: Fresh morning air & deep breathing
    diet: 4,      // Makool wa Mashroob: Warm, light, anti-phlegmatic diet
    movement: 3,  // Harkat wa Sukun Badani: Joint mobility exercises
    sleep: 4,     // Nawm wa Yaqza: 7-8 hours restorative sleep
    retention: 4, // Ihtibas wa Istifragh: Normal metabolic elimination
    mental: 5     // Harkat wa Sukun Nafsani: Emotional calm & prayer/meditation
  });

  // Clinical Messaging Thread
  const [messages, setMessages] = useState<PatientMessage[]>(MOCK_PATIENT_MESSAGES);
  const [messageInput, setMessageInput] = useState("");

  // AI Doctor Hakeem Sahab Chat
  const [aiHistory, setAiHistory] = useState<Array<{ role: "user" | "bot"; text: string; time: string }>>([
    {
      role: "bot",
      text: "Assalamu Alaikum Hamza Sahab. I am Hakeem Sahab, your clinical AI assistant trained on classical Unani pharmacopeia and your personal Balghami Mizaj profile. How can I assist you with your diet, exercises, or medicine timings today?",
      time: "10:00 AM"
    }
  ]);
  const [aiPrompt, setAiPrompt] = useState("");
  const [aiResponding, setAiResponding] = useState(false);

  // Posology audio playback simulation
  const handlePlayPosologyAudio = () => {
    setIsPlayingAudio(true);
    setTimeout(() => {
      setIsPlayingAudio(false);
    }, 3500);
  };

  // Appointment Actions
  const handleRescheduleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setAppointments((prev) =>
      prev.map((apt) =>
        apt.id === MOCK_PATIENT_APPOINTMENT.id
          ? { ...apt, date: rescheduleDate, timeSlot: rescheduleSlot, status: "Rescheduled" }
          : apt
      )
    );
    setShowRescheduleModal(false);
  };

  const handleCancelAppointment = (aptId: string) => {
    if (confirm("Are you sure you wish to cancel this scheduled consultation? Our clinical desk will be notified.")) {
      setAppointments((prev) => prev.filter((a) => a.id !== aptId));
    }
  };

  // Report Upload Action
  const handleReportUpload = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newReportTitle.trim()) return;
    const newEntry: PatientLabReport = {
      id: "RPT-2026-" + Math.floor(1000 + Math.random() * 9000),
      title: newReportTitle,
      testDate: new Date().toISOString().split("T")[0],
      labName: newReportLab,
      status: "Pending Review",
      fileSize: "1.4 MB",
      downloadUrl: "#"
    };
    setReports([newEntry, ...reports]);
    setNewReportTitle("");
    setShowUploadModal(false);
  };

  // Chat Send Action
  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!messageInput.trim()) return;
    const newMsg: PatientMessage = {
      id: "msg-" + Date.now(),
      senderName: MOCK_PATIENT_PROFILE.fullName,
      senderRole: "Patient",
      timestamp: "Just now",
      messageText: messageInput,
      isDoctor: false
    };
    setMessages([...messages, newMsg]);
    setMessageInput("");

    // Simulated clinical desk response
    setTimeout(() => {
      const reply: PatientMessage = {
        id: "msg-" + (Date.now() + 1),
        senderName: "Prof. (Dr.) Mansoor Alam",
        senderRole: "Attending Senior Tabeeb",
        timestamp: "Just now",
        messageText: "Noted with thanks, Hamza Sahab. Please ensure the warm fomentation is applied exactly 20 minutes before sleeping.",
        isDoctor: true
      };
      setMessages((curr) => [...curr, reply]);
    }, 1200);
  };

  // AI Doctor prompt handler
  const handleAiAsk = (e: React.FormEvent) => {
    e.preventDefault();
    if (!aiPrompt.trim()) return;
    const userQ = aiPrompt;
    const userTime = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    setAiHistory((prev) => [...prev, { role: "user", text: userQ, time: userTime }]);
    setAiPrompt("");
    setAiResponding(true);

    setTimeout(() => {
      let botAnswer = "";
      const lower = userQ.toLowerCase();
      if (lower.includes("food") || lower.includes("diet") || lower.includes("parhez")) {
        botAnswer = "For your Balghami (Cold & Moist) temperament, favor warm digestive spices like zanjabeel (ginger), darchini (cinnamon), and roasted cumin. Avoid cold curd at night, chilled drinks, and heavy white flour dishes to keep phlegmatic accumulation minimal.";
      } else if (lower.includes("suranjan") || lower.includes("majun") || lower.includes("medicine")) {
        botAnswer = "Majun Suranjan should be taken exactly 5g (one metric teaspoon) morning and evening after food with lukewarm water. Remember never to take it with ice water, as cold liquid hampers its digestive transformation (Hazm-e-Uzw).";
      } else if (lower.includes("exercise") || lower.includes("pain") || lower.includes("knee")) {
        botAnswer = "Perform gentle isometric knee strengthening and non-weight-bearing flexion. If you feel morning stiffness, apply warm Roghan-e-Balsan with mild strokes before moving.";
      } else {
        botAnswer = "Your clinical regime is focused on Taskeen-e-Alam (pain mitigation) and Ta'dil-e-Mizaj (temperamental rebalancing). Continue following your prescribed Asbab Sittah lifestyle habits and consult Dr. Mansoor during your next appointment on Sep 15.";
      }

      setAiHistory((prev) => [
        ...prev,
        {
          role: "bot",
          text: botAnswer,
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
        }
      ]);
      setAiResponding(false);
    }, 800);
  };

  const navTabs: Array<{ id: PatientSection; label: string; icon: string }> = [
    { id: "overview", label: "Health 360", icon: "👤" },
    { id: "profile", label: "My Profile", icon: "📋" },
    { id: "appointments", label: "Appointments", icon: "📅" },
    { id: "consultations", label: "Clinical Encounters", icon: "🩺" },
    { id: "ai-doctor", label: "Hakeem Sahab AI", icon: "🤖" },
    { id: "protocols", label: "Care Protocols", icon: "📑" },
    { id: "prescriptions", label: "Prescriptions", icon: "📝" },
    { id: "medicines", label: "Medicines & Dawa", icon: "💊" },
    { id: "reports", label: "Lab Reports", icon: "🧪" },
    { id: "treatment-plans", label: "Regimenal Therapies", icon: "🌿" },
    { id: "lifestyle", label: "Asbab-e-Sittah", icon: "🧘" },
    { id: "messages", label: "Doctor Messages", icon: "💬" },
    { id: "billing", label: "Invoices & Billing", icon: "💳" }
  ];

  return (
    <AppShell activeRole="patient">
      <div className="space-y-6 max-w-7xl mx-auto pb-12">
        
        {/* Patient Welcome & Health Identity Banner */}
        <div className="p-6 rounded-3xl bg-gradient-to-r from-[#0C1524] via-[#101C30] to-[#152540] border border-slate-800 shadow-xl flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-3">
              <span className="text-[11px] font-bold text-teal-400 uppercase tracking-widest bg-teal-950/80 px-3 py-1 rounded-full border border-teal-800/80">
                Active Patient Account
              </span>
              <span className="text-xs text-slate-400 font-mono">
                ABDM Linked • DPDP 2023 Verified
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Hamza Farooqi
            </h1>
            <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 text-xs text-slate-300">
              <span>MRN: <strong className="text-white font-mono">{MOCK_PATIENT_PROFILE.mrn}</strong></span>
              <span>•</span>
              <span>ABHA: <strong className="text-white font-mono">{MOCK_PATIENT_PROFILE.abhaId}</strong></span>
              <span>•</span>
              <span>Mizaj: <strong className="text-teal-300">{MOCK_PATIENT_PROFILE.primaryMizaj}</strong></span>
              <span>•</span>
              <span>Blood Group: <strong className="text-white">{MOCK_PATIENT_PROFILE.bloodGroup}</strong></span>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={() => setActiveTab("appointments")}
              className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold transition shadow-lg shadow-teal-900/30 flex items-center gap-2"
            >
              <span>📅</span> Next Visit: Sep 15 (10:30 AM)
            </button>
            <button
              onClick={() => setActiveTab("ai-doctor")}
              className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-teal-300 text-xs font-semibold border border-slate-700 transition flex items-center gap-2"
            >
              <span>🤖</span> Ask Hakeem Sahab
            </button>
          </div>
        </div>

        {/* 13-Section Horizontal Navigation Bar */}
        <div className="border-b border-slate-800 overflow-x-auto no-scrollbar flex gap-1 pb-1">
          {navTabs.map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-3.5 py-2.5 text-xs font-semibold whitespace-nowrap transition-all rounded-xl ${
                  isActive
                    ? "bg-teal-950/80 text-teal-300 border border-teal-600/50 shadow-sm"
                    : "text-slate-400 hover:text-white hover:bg-slate-800/40"
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* ========================================================= */}
        {/* SECTION 1: HEALTH 360 OVERVIEW                            */}
        {/* ========================================================= */}
        {activeTab === "overview" && (
          <div className="space-y-6 animate-fade-in">
            {/* Health Metrics Summary */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <StatCard label="Next Scheduled Visit" value="Sep 15" subtext="10:30 AM • Jamia Hamdard OPD" variant="teal" icon="📅" />
              <StatCard label="Active Formulations" value="2 Drugs" subtext="Majun Suranjan & Roghan" variant="emerald" icon="💊" />
              <StatCard label="Lifestyle Balance" value="82%" subtext="Asbab-e-Sittah Compliance" variant="blue" icon="🌿" />
              <StatCard label="Recent Blood Pressure" value="124/82" subtext="Resting Pulse 72 bpm" variant="teal" icon="❤️" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Active Care Protocol Summary */}
              <div className="lg:col-span-2 space-y-6">
                <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 shadow-md">
                  <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                    <div>
                      <span className="text-[10px] font-bold uppercase tracking-wider text-teal-400">Clinical Protocol</span>
                      <h3 className="text-lg font-bold text-white mt-0.5">{MOCK_ACTIVE_CARE_PLAN.programName}</h3>
                      <p className="text-xs text-slate-400">{MOCK_ACTIVE_CARE_PLAN.condition}</p>
                    </div>
                    <StatusBadge status="Active Care" variant="verified" />
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-400">Phase {MOCK_ACTIVE_CARE_PLAN.phaseNumber} of {MOCK_ACTIVE_CARE_PLAN.totalPhases}: {MOCK_ACTIVE_CARE_PLAN.currentPhase}</span>
                      <span className="text-teal-400 font-bold font-mono">{MOCK_ACTIVE_CARE_PLAN.progressPercent}%</span>
                    </div>
                    <div className="w-full h-2.5 rounded-full bg-slate-800 overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-teal-500 to-emerald-400 rounded-full" style={{ width: `${MOCK_ACTIVE_CARE_PLAN.progressPercent}%` }}></div>
                    </div>
                  </div>

                  <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800/80 text-xs space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">Supervising Physician</span>
                      <span className="text-teal-300 font-semibold">{MOCK_ACTIVE_CARE_PLAN.attendingPhysician}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">Program Start</span>
                      <span className="text-slate-200">{MOCK_ACTIVE_CARE_PLAN.startDate}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">Next Scheduled Evaluation</span>
                      <span className="text-slate-200">{MOCK_ACTIVE_CARE_PLAN.nextReviewDate}</span>
                    </div>
                    <p className="text-slate-400 pt-2 border-t border-slate-800 italic">
                      "{MOCK_ACTIVE_CARE_PLAN.clinicalNotes}"
                    </p>
                  </div>
                </div>

                {/* Voice Medication Instructions */}
                <div className="bg-[#0F172A] border border-teal-800/40 rounded-3xl p-6 space-y-4 shadow-md">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-teal-500/20 text-teal-300 flex items-center justify-center text-xl">
                        🔊
                      </div>
                      <div>
                        <h4 className="text-sm font-bold text-white">Vernacular Voice Medication Guide</h4>
                        <p className="text-xs text-slate-400">Clear audio posology instructions spoken in your mother tongue</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-1.5 bg-slate-900 p-1 rounded-xl border border-slate-800">
                      {(["urdu", "hindi", "english"] as const).map((lang) => (
                        <button
                          key={lang}
                          onClick={() => setAudioLang(lang)}
                          className={`px-3 py-1 rounded-lg text-xs font-semibold capitalize transition ${
                            audioLang === lang
                              ? "bg-teal-600 text-white shadow-sm"
                              : "text-slate-400 hover:text-white"
                          }`}
                        >
                          {lang}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="bg-slate-900/90 rounded-2xl p-4 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div className="text-xs text-slate-300 leading-relaxed">
                      {audioLang === "urdu" && "Majun Suranjan subah aur sham 5 gram neem garam pani ke sath lein. Roghan-e-Balsan rat ko ghutne par halke hath se malish karein."}
                      {audioLang === "hindi" && "Majun Suranjan subah aur shaam 5 gram gungune paani ke saath lein. Roghan-e-Balsan raat ko ghutne par halke haath se lagayein."}
                      {audioLang === "english" && "Take Majun Suranjan 5 grams twice daily with lukewarm water after meals. Gently massage Roghan-e-Balsan onto the knee joint at bedtime."}
                    </div>
                    <button
                      onClick={handlePlayPosologyAudio}
                      disabled={isPlayingAudio}
                      className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 disabled:bg-slate-800 disabled:text-slate-500 text-white text-xs font-bold transition whitespace-nowrap flex items-center gap-2 self-start sm:self-center"
                    >
                      {isPlayingAudio ? "▶ Playing Voice..." : "🔊 Listen to Audio"}
                    </button>
                  </div>
                </div>
              </div>

              {/* Right Column: Next Appointment & Emergency Desk */}
              <div className="space-y-6">
                <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 shadow-md">
                  <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                    <h4 className="text-sm font-bold text-white">Next Clinic Visit</h4>
                    <StatusBadge status="Confirmed" variant="verified" />
                  </div>
                  <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800 space-y-2 text-xs">
                    <span className="text-[10px] uppercase font-bold text-slate-500">OPD Queue Token</span>
                    <div className="text-xl font-mono font-extrabold text-teal-300">{MOCK_PATIENT_APPOINTMENT.tokenNumber}</div>
                    <div className="text-slate-200 font-medium pt-1">
                      {MOCK_PATIENT_APPOINTMENT.date} • {MOCK_PATIENT_APPOINTMENT.timeSlot}
                    </div>
                    <div className="text-slate-400">
                      {MOCK_PATIENT_APPOINTMENT.doctorName}
                    </div>
                    <div className="text-[11px] text-slate-500">
                      {MOCK_PATIENT_APPOINTMENT.facilityLocation}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setShowRescheduleModal(true)}
                      className="flex-1 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition"
                    >
                      Reschedule
                    </button>
                    <button
                      onClick={() => setActiveTab("appointments")}
                      className="flex-1 py-2 rounded-xl bg-teal-950 hover:bg-teal-900 text-teal-300 text-xs font-semibold border border-teal-800 transition"
                    >
                      All Visits
                    </button>
                  </div>
                </div>

                {/* Emergency Hospital Contact */}
                <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-3 shadow-md text-xs">
                  <div className="flex items-center gap-2 text-rose-400 font-bold">
                    <span>🚨</span>
                    <span>24/7 Clinical Emergency Desk</span>
                  </div>
                  <p className="text-slate-400 text-[11px]">
                    For sudden acute distress, contact the AUTC emergency hospital triage or call 112 immediately.
                  </p>
                  <div className="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <div className="text-slate-300 font-bold">Jamia Hamdard Emergency Wing:</div>
                    <div className="text-teal-400 font-mono font-bold text-sm">+91 11 2605 9000</div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 2: MY HEALTH PROFILE                             */}
        {/* ========================================================= */}
        {activeTab === "profile" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-4">
              <h3 className="text-lg font-bold text-white">Patient Clinical Identity & Demographics</h3>
              <p className="text-slate-400">Official medical record details registered under Ayushman Bharat Digital Mission (ABDM).</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800 space-y-3">
                  <h4 className="font-bold text-teal-300 uppercase tracking-wider text-[10px]">Demographic Profile</h4>
                  <div className="grid grid-cols-2 gap-2 text-slate-300">
                    <div><span className="text-slate-500 block">Full Name:</span> {MOCK_PATIENT_PROFILE.fullName}</div>
                    <div><span className="text-slate-500 block">Age / Gender:</span> {MOCK_PATIENT_PROFILE.age} yrs / {MOCK_PATIENT_PROFILE.gender}</div>
                    <div><span className="text-slate-500 block">Medical Record No:</span> <span className="font-mono text-teal-400">{MOCK_PATIENT_PROFILE.mrn}</span></div>
                    <div><span className="text-slate-500 block">ABHA ID:</span> <span className="font-mono text-white">{MOCK_PATIENT_PROFILE.abhaId}</span></div>
                    <div><span className="text-slate-500 block">Blood Group:</span> {MOCK_PATIENT_PROFILE.bloodGroup}</div>
                    <div><span className="text-slate-500 block">Registered Phone:</span> {MOCK_PATIENT_PROFILE.phone}</div>
                  </div>
                </div>

                <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800 space-y-3">
                  <h4 className="font-bold text-teal-300 uppercase tracking-wider text-[10px]">Residential Address</h4>
                  <p className="text-slate-300">{MOCK_PATIENT_PROFILE.address}</p>
                  <h4 className="font-bold text-teal-300 uppercase tracking-wider text-[10px] pt-2">Emergency Contact</h4>
                  <p className="text-slate-300">{MOCK_PATIENT_PROFILE.emergencyContact}</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800 space-y-3">
                  <h4 className="font-bold text-teal-300 uppercase tracking-wider text-[10px]">Mizaj & Constitutional Diagnostics</h4>
                  <div className="space-y-2 text-slate-300">
                    <div>
                      <span className="text-slate-500 block">Innate Temperament (Mizaj-e-Asli):</span>
                      <strong className="text-white text-sm">{MOCK_PATIENT_PROFILE.primaryMizaj}</strong>
                    </div>
                    <div>
                      <span className="text-slate-500 block">Present Dyscrasia (Su-e-Mizaj):</span>
                      <span className="text-rose-300">{MOCK_PATIENT_PROFILE.suEMizaj}</span>
                    </div>
                  </div>
                </div>

                <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800 space-y-3">
                  <h4 className="font-bold text-rose-400 uppercase tracking-wider text-[10px]">Documented Clinical Allergies</h4>
                  <div className="flex flex-wrap gap-2">
                    {MOCK_PATIENT_PROFILE.allergies.map((allergy, idx) => (
                      <span key={idx} className="bg-rose-950/60 border border-rose-800/80 text-rose-300 px-3 py-1 rounded-xl text-xs">
                        ⚠ {allergy}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 3: APPOINTMENTS                                   */}
        {/* ========================================================= */}
        {activeTab === "appointments" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-lg font-bold text-white">Consultation Visits & Tokens</h3>
                <p className="text-slate-400">Track your in-person hospital OPD encounters and scheduled teleconsultations.</p>
              </div>
              <Link
                href="/website/book"
                className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shadow-md transition self-start sm:self-center"
              >
                + Schedule New Consultation
              </Link>
            </div>

            <div className="space-y-4">
              {appointments.map((apt) => (
                <div key={apt.id} className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2.5">
                      <span className="font-mono text-teal-400 font-bold">{apt.tokenNumber}</span>
                      <span className="text-slate-600">•</span>
                      <span className="font-bold text-white text-sm">{apt.date} at {apt.timeSlot}</span>
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                        apt.status === "Confirmed" ? "bg-emerald-950 text-emerald-300 border border-emerald-800" : "bg-slate-800 text-slate-400"
                      }`}>
                        {apt.status}
                      </span>
                    </div>
                    <div className="text-slate-200 font-medium">{apt.doctorName} — <span className="text-slate-400 font-normal">{apt.doctorSpecialty}</span></div>
                    <div className="text-slate-400 text-[11px]">{apt.mode} • {apt.facilityLocation}</div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    {apt.mode === "Video Consultation" && (
                      <button className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition">
                        Join Teleconsultation Room
                      </button>
                    )}
                    <button
                      onClick={() => setShowRescheduleModal(true)}
                      className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold border border-slate-700 transition"
                    >
                      Reschedule
                    </button>
                    <button
                      onClick={() => handleCancelAppointment(apt.id)}
                      className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-rose-950 text-slate-400 hover:text-rose-300 font-semibold border border-slate-700 transition"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 4: CLINICAL ENCOUNTERS / WORKSPACE                */}
        {/* ========================================================= */}
        {activeTab === "consultations" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-4">
              <h3 className="text-lg font-bold text-white">Clinical Encounters & Doctor Notes</h3>
              <p className="text-slate-400">Formal clinical summaries signed by registered Unani faculty.</p>
            </div>

            <div className="space-y-4">
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                  <div>
                    <span className="text-teal-400 font-mono text-[11px]">Encounter #ENC-2026-0814</span>
                    <h4 className="text-sm font-bold text-white mt-0.5">Comprehensive Intake & Nabz Palpation</h4>
                    <span className="text-slate-400 text-[11px]">Attending: Prof. (Dr.) Mansoor Alam • Date: Sep 02, 2026</span>
                  </div>
                  <StatusBadge status="Doctor Signed" variant="verified" />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <span className="text-slate-500 uppercase font-bold text-[10px]">Chief Complaint & History</span>
                    <p className="text-slate-300 leading-relaxed">
                      Patient presented with bilateral knee stiffness, worse in mornings and damp winter conditions. Local swelling with mild crepitus. No acute inflammatory erythema.
                    </p>
                  </div>

                  <div className="space-y-2">
                    <span className="text-slate-500 uppercase font-bold text-[10px]">Physical Nabz Examination</span>
                    <p className="text-slate-300 leading-relaxed">
                      Nabz is <em>Bati</em> (slow) and <em>Layyin</em> (soft), consistent with excessive Balgham accumulation in the joints. Tongue showed thick white coating and moist borders.
                    </p>
                  </div>
                </div>

                <div className="p-3 bg-[#0A0F1D] rounded-xl border border-slate-800 text-slate-300 space-y-1">
                  <span className="text-teal-300 font-bold block text-[10px] uppercase">Plan of Management (Tadbeer)</span>
                  <p>
                    1. Majun Suranjan 5g twice daily with lukewarm water. 2. Warm fomentation (Nutool Haar) with decoction of Babuna and Ikleel-ul-Malik. 3. Avoid yogurt, chilled drinks, and heavy starches at dinner.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 5: AI DOCTOR HAKEEM SAHAB COMPANION               */}
        {/* ========================================================= */}
        {activeTab === "ai-doctor" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xl">🤖</span>
                  <h3 className="text-lg font-bold text-white">AI Doctor — Hakeem Sahab</h3>
                </div>
                <p className="text-slate-400">24/7 Unani Clinical Intelligence trained on classical medical texts and calibrated to your Balghami Mizaj.</p>
              </div>
              <div className="flex items-center gap-2 bg-slate-900 px-3 py-1 rounded-full border border-slate-800 text-[11px] text-teal-400">
                <span className="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
                <span>Active Knowledge Engine</span>
              </div>
            </div>

            {/* Chat Box Display */}
            <div className="bg-[#0A101D] rounded-2xl border border-slate-800 p-4 h-96 overflow-y-auto space-y-4">
              {aiHistory.map((item, idx) => (
                <div
                  key={idx}
                  className={`flex flex-col ${item.role === "user" ? "items-end" : "items-start"}`}
                >
                  <div
                    className={`max-w-xl p-3.5 rounded-2xl text-xs leading-relaxed ${
                      item.role === "user"
                        ? "bg-teal-600 text-white rounded-tr-none"
                        : "bg-slate-900 text-slate-200 border border-slate-800 rounded-tl-none"
                    }`}
                  >
                    {item.text}
                  </div>
                  <span className="text-[10px] text-slate-500 mt-1 px-1">{item.time}</span>
                </div>
              ))}
              {aiResponding && (
                <div className="flex items-center gap-2 text-slate-400 text-xs">
                  <span className="w-3 h-3 border-2 border-teal-400 border-t-transparent rounded-full animate-spin"></span>
                  <span>Hakeem Sahab is formulating clinical advice...</span>
                </div>
              )}
            </div>

            {/* Prompt Form */}
            <form onSubmit={handleAiAsk} className="flex gap-2">
              <input
                type="text"
                value={aiPrompt}
                onChange={(e) => setAiPrompt(e.target.value)}
                placeholder="Ask about diet, medicine dosage, morning joint stiffness..."
                className="flex-1 px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500 text-xs"
              />
              <button
                type="submit"
                disabled={aiResponding}
                className="px-6 py-3 rounded-xl bg-teal-600 hover:bg-teal-500 disabled:bg-slate-800 text-white font-bold transition flex items-center gap-2"
              >
                Send Question →
              </button>
            </form>

            <div className="flex flex-wrap gap-2 text-[11px] text-slate-400">
              <span className="text-slate-500">Suggested queries:</span>
              <button
                onClick={() => setAiPrompt("What foods should I avoid with Balghami Mizaj?")}
                className="bg-slate-900 hover:bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-800 text-teal-400 transition"
              >
                What foods should I avoid?
              </button>
              <button
                onClick={() => setAiPrompt("How should I take Majun Suranjan?")}
                className="bg-slate-900 hover:bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-800 text-teal-400 transition"
              >
                How to take Majun Suranjan?
              </button>
              <button
                onClick={() => setAiPrompt("Can I do morning walks with knee stiffness?")}
                className="bg-slate-900 hover:bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-800 text-teal-400 transition"
              >
                Morning walk guidelines
              </button>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 6: ZAYVORA PROTOCOLS                              */}
        {/* ========================================================= */}
        {activeTab === "protocols" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-4">
              <h3 className="text-lg font-bold text-white">4-Phase Integrative Protocol Schedule</h3>
              <p className="text-slate-400">Evidence-based Unani therapeutic pathway for Waja-ul-Mafasil Barid Balghami.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {[
                { phase: 1, name: "Taskeen-e-Alam", action: "Acute Pain Mitigation", status: "Completed", desc: "Local analgesic Roghan application and initial anti-inflammatory Safoof." },
                { phase: 2, name: "Tanqiya-e-Mawad", action: "Morbid Matter Elimination", status: "In Progress", desc: "Gentle Munzij-e-Balgham herbs followed by Mushil to expel cold humors." },
                { phase: 3, name: "Ta'dil-e-Mizaj", action: "Temperamental Normalization", status: "Upcoming", desc: "Rebalancing dietetics and constitutional restoration." },
                { phase: 4, name: "Taqwiyat-e-Mafasil", action: "Cartilage & Joint Fortification", status: "Upcoming", desc: "Long-term tonic therapy and regimenal maintenance." }
              ].map((p) => (
                <div
                  key={p.phase}
                  className={`p-5 rounded-2xl border space-y-3 ${
                    p.status === "Completed"
                      ? "bg-emerald-950/20 border-emerald-500/40 text-slate-200"
                      : p.status === "In Progress"
                      ? "bg-teal-950/40 border-teal-500 text-white ring-1 ring-teal-500/50"
                      : "bg-slate-900/60 border-slate-800 text-slate-400"
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <span className="font-mono text-teal-400 font-bold text-[10px]">STAGE 0{p.phase}</span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      p.status === "Completed" ? "bg-emerald-950 text-emerald-300" : p.status === "In Progress" ? "bg-teal-950 text-teal-300" : "bg-slate-800 text-slate-500"
                    }`}>
                      {p.status}
                    </span>
                  </div>
                  <h4 className="font-bold text-sm text-white">{p.name}</h4>
                  <div className="text-teal-300 font-medium text-[11px]">{p.action}</div>
                  <p className="text-[11px] text-slate-400 leading-relaxed">{p.desc}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 7: PRESCRIPTIONS                                  */}
        {/* ========================================================= */}
        {activeTab === "prescriptions" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-lg font-bold text-white">Digital Prescription: RX-2026-0441</h3>
                <p className="text-slate-400">Issued by Prof. (Dr.) Mansoor Alam • Verified by Jamia Hamdard Central Dispensary</p>
              </div>
              <button
                onClick={() => alert("Downloading signed official prescription PDF...")}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-teal-300 font-semibold border border-slate-700 transition"
              >
                Download Official PDF 📄
              </button>
            </div>

            <div className="space-y-4">
              {MOCK_PRESCRIPTIONS.map((rx, idx) => (
                <div key={idx} className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2">
                      <h4 className="font-bold text-white text-sm">{rx.medicineName}</h4>
                      <span className="bg-teal-950 text-teal-300 px-2 py-0.5 rounded text-[10px] font-semibold border border-teal-800">
                        {rx.form}
                      </span>
                    </div>
                    <p className="text-slate-300">
                      <strong>Dosage & Frequency:</strong> {rx.dosage} • {rx.timing}
                    </p>
                    <p className="text-slate-400 text-[11px]">
                      <strong>Vehicle (Anupan):</strong> {rx.anupan}
                    </p>
                    <p className="text-slate-400 text-[11px]">
                      <strong>Instructions:</strong> {rx.instructions}
                    </p>
                  </div>
                  <div className="text-right shrink-0">
                    <span className="text-emerald-400 font-semibold block text-[11px]">✓ Mudabbar Batch Certified</span>
                    <span className="text-slate-500 text-[10px]">Dispensed: Sep 12, 2026</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 8: MEDICINES & PHARMACY                           */}
        {/* ========================================================= */}
        {activeTab === "medicines" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-4">
              <h3 className="text-lg font-bold text-white">Active Formulations & Posology Schedule</h3>
              <p className="text-slate-400">Real-time medication adherence tracking and pharmaceutical monographs.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-bold text-white text-sm">Majun Suranjan (Mudabbar)</h4>
                    <span className="text-teal-400 text-[11px]">Suranjan Shirin + Asgandh + Zanjabeel</span>
                  </div>
                  <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded text-[10px] font-bold">
                    In Stock (180g)
                  </span>
                </div>
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800/80 space-y-1 text-slate-300">
                  <div><strong>Daily Regimen:</strong> 5g twice daily with lukewarm water</div>
                  <div><strong>Batch Lot:</strong> MS-2026-LOT4 (Ayush GMP)</div>
                  <div><strong>Adherence:</strong> 12 of 14 doses taken this week</div>
                </div>
              </div>

              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-bold text-white text-sm">Roghan-e-Balsan (Joint Oil)</h4>
                    <span className="text-teal-400 text-[11px]">Classical Balsamodendron extract in pure sesame base</span>
                  </div>
                  <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded text-[10px] font-bold">
                    In Stock (100ml)
                  </span>
                </div>
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800/80 space-y-1 text-slate-300">
                  <div><strong>Daily Regimen:</strong> Gentle circular massage onto knee at night</div>
                  <div><strong>Batch Lot:</strong> RB-2026-LOT2 (Ayush GMP)</div>
                  <div><strong>Adherence:</strong> 7 of 7 night applications completed</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 9: DIAGNOSTICS / REPORTS                          */}
        {/* ========================================================= */}
        {activeTab === "reports" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-lg font-bold text-white">Diagnostic Laboratory Reports & Imaging</h3>
                <p className="text-slate-400">Access verified pathology, biochemistry, and radiological records.</p>
              </div>
              <button
                onClick={() => setShowUploadModal(true)}
                className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition shadow-md self-start sm:self-center"
              >
                + Upload New Lab Report
              </button>
            </div>

            <div className="space-y-3">
              {reports.map((rpt) => (
                <div key={rpt.id} className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-slate-800 text-teal-400 flex items-center justify-center text-lg">
                      📄
                    </div>
                    <div>
                      <h4 className="font-bold text-white text-sm">{rpt.title}</h4>
                      <p className="text-slate-400 text-[11px]">{rpt.labName} • Date: {rpt.testDate} • {rpt.fileSize}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                      rpt.status === "Verified" ? "bg-emerald-950 text-emerald-300 border border-emerald-800" : "bg-amber-950 text-amber-300 border border-amber-800"
                    }`}>
                      {rpt.status}
                    </span>
                    <button
                      onClick={() => alert(`Downloading diagnostic report: ${rpt.title}`)}
                      className="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold border border-slate-700 transition"
                    >
                      Download PDF
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 10: TREATMENT PLANS (REGIMENAL THERAPIES)         */}
        {/* ========================================================= */}
        {activeTab === "treatment-plans" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-4">
              <h3 className="text-lg font-bold text-white">Ilaj-bit-Tadbeer (Regimenal Therapies) Schedule</h3>
              <p className="text-slate-400">Clinical physiotherapy, fomentation, and hijama procedures scheduled at Jamia Hamdard AUTC.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="font-bold text-teal-400">Nutool Haar</span>
                  <span className="text-emerald-400 text-[10px] font-semibold">Scheduled</span>
                </div>
                <h4 className="text-white font-bold text-sm">Warm Decoction Irrigation</h4>
                <p className="text-slate-400 text-[11px] leading-relaxed">
                  Local pouring of warm anti-inflammatory herbal decoctions (Babuna + Gul-e-Surkh) over knee joint for 15 minutes.
                </p>
                <div className="text-[11px] text-slate-300 pt-2 border-t border-slate-800">
                  Next Session: <strong>Sep 16, 11:30 AM</strong>
                </div>
              </div>

              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="font-bold text-teal-400">Dalk Layyin</span>
                  <span className="text-emerald-400 text-[10px] font-semibold">Active Daily</span>
                </div>
                <h4 className="text-white font-bold text-sm">Gentle Therapeutic Massage</h4>
                <p className="text-slate-400 text-[11px] leading-relaxed">
                  Centripetal strokes with warm Roghan to stimulate blood circulation and enhance synovial fluid movement.
                </p>
                <div className="text-[11px] text-slate-300 pt-2 border-t border-slate-800">
                  Frequency: <strong>Nightly before bed</strong>
                </div>
              </div>

              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="font-bold text-teal-400">Hijama Nariyya</span>
                  <span className="text-slate-500 text-[10px]">Phase 3 Evaluation</span>
                </div>
                <h4 className="text-white font-bold text-sm">Warm Dry Fire Cupping</h4>
                <p className="text-slate-400 text-[11px] leading-relaxed">
                  Applied to peri-articular points to evacuate deep-seated cold humors following Tanqiya phase completion.
                </p>
                <div className="text-[11px] text-slate-300 pt-2 border-t border-slate-800">
                  Planned for: <strong>Oct 05, 2026</strong>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 11: ASBAB-E-SITTAH LIFESTYLE TRACKER             */}
        {/* ========================================================= */}
        {activeTab === "lifestyle" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-4">
              <h3 className="text-lg font-bold text-white">Asbab-e-Sittah Zaruriyyah (6 Essential Lifestyle Determinants)</h3>
              <p className="text-slate-400">Daily interactive self-assessment based on classical Unani physiological equilibrium.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                { key: "air", title: "1. Hawa-e-Muheet (Ambient Air & Breathing)", desc: "Fresh morning air ventilation, avoiding damp cold rooms", val: asbabScores.air },
                { key: "diet", title: "2. Makool wa Mashroob (Diet & Hydration)", desc: "Warm soups, herbal infusions, strict avoidance of chilled foods", val: asbabScores.diet },
                { key: "movement", title: "3. Harkat wa Sukun Badani (Physical Exercise)", desc: "20 minutes gentle knee range of motion and brisk walking", val: asbabScores.movement },
                { key: "sleep", title: "4. Nawm wa Yaqza (Sleep & Rest)", desc: "7-8 hours restful nocturnal sleep without late-night screens", val: asbabScores.sleep },
                { key: "retention", title: "5. Ihtibas wa Istifragh (Retention & Elimination)", desc: "Healthy digestion, daily bowel movements, adequate hydration", val: asbabScores.retention },
                { key: "mental", title: "6. Harkat wa Sukun Nafsani (Emotional Balance)", desc: "Low mental anxiety, mindfulness, calm temperamental demeanor", val: asbabScores.mental }
              ].map((item) => (
                <div key={item.key} className="p-4 bg-slate-900/90 rounded-2xl border border-slate-800 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-white">{item.title}</span>
                    <span className="text-teal-300 font-bold font-mono text-sm">{item.val} / 5</span>
                  </div>
                  <p className="text-slate-400 text-[11px]">{item.desc}</p>
                  <div className="flex gap-2 pt-2">
                    {[1, 2, 3, 4, 5].map((score) => (
                      <button
                        key={score}
                        onClick={() => setAsbabScores({ ...asbabScores, [item.key]: score })}
                        className={`w-8 h-8 rounded-xl font-bold text-xs transition ${
                          item.val === score
                            ? "bg-teal-600 text-white shadow-sm"
                            : "bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white"
                        }`}
                      >
                        {score}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 12: CLINICAL MESSAGES                             */}
        {/* ========================================================= */}
        {activeTab === "messages" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-4">
              <h3 className="text-lg font-bold text-white">Direct Encrypted Doctor Communication</h3>
              <p className="text-slate-400">Secure clinical chat thread with Prof. (Dr.) Mansoor Alam and the AUTC care desk.</p>
            </div>

            <div className="bg-[#0A101D] rounded-2xl border border-slate-800 p-4 h-96 overflow-y-auto space-y-4">
              {messages.map((m) => (
                <div
                  key={m.id}
                  className={`flex flex-col ${m.isDoctor ? "items-start" : "items-end"}`}
                >
                  <div className="flex items-center gap-1.5 mb-1 px-1">
                    <span className="font-bold text-white text-[11px]">{m.senderName}</span>
                    <span className="text-[10px] text-teal-400">({m.senderRole})</span>
                    <span className="text-[10px] text-slate-500">• {m.timestamp}</span>
                  </div>
                  <div
                    className={`max-w-xl p-3.5 rounded-2xl text-xs leading-relaxed ${
                      m.isDoctor
                        ? "bg-slate-900 text-slate-200 border border-slate-800 rounded-tl-none"
                        : "bg-teal-600 text-white rounded-tr-none"
                    }`}
                  >
                    {m.messageText}
                  </div>
                </div>
              ))}
            </div>

            <form onSubmit={handleSendMessage} className="flex gap-2">
              <input
                type="text"
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
                placeholder="Type your message to Dr. Mansoor..."
                className="flex-1 px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500 text-xs"
              />
              <button
                type="submit"
                className="px-6 py-3 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition"
              >
                Send Message →
              </button>
            </form>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 13: BILLING & INVOICES                            */}
        {/* ========================================================= */}
        {activeTab === "billing" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-4">
              <h3 className="text-lg font-bold text-white">Itemized Consultation & Dispensary Invoices</h3>
              <p className="text-slate-400">GST-compliant digital receipts for OPD encounters and herbal dispensations.</p>
            </div>

            <div className="space-y-3">
              {MOCK_PATIENT_INVOICES.map((inv) => (
                <div key={inv.invoiceId} className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-teal-400 font-bold">{inv.invoiceId}</span>
                      <span className="text-slate-600">•</span>
                      <span className="text-slate-400">{inv.date}</span>
                      <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded text-[10px] font-bold">
                        {inv.status}
                      </span>
                    </div>
                    <h4 className="font-bold text-white text-sm">{inv.serviceDescription}</h4>
                    <p className="text-slate-400 text-[11px]">Payment Mode: {inv.paymentMode} • Receipt: {inv.receiptNumber}</p>
                  </div>

                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <span className="text-[10px] text-slate-500 block">Total Amount</span>
                      <span className="text-base font-mono font-bold text-white">₹{inv.amount.toLocaleString()}</span>
                    </div>
                    <button
                      onClick={() => alert(`Downloading GST receipt for ${inv.invoiceId}`)}
                      className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-teal-300 font-semibold border border-slate-700 transition"
                    >
                      Receipt 📥
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* RESCHEDULE APPOINTMENT MODAL                              */}
        {/* ========================================================= */}
        {showRescheduleModal && (
          <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-[#0F172A] border border-slate-700 rounded-3xl p-6 max-w-md w-full space-y-4 shadow-2xl text-xs">
              <div className="flex justify-between items-center border-b border-slate-800 pb-3">
                <h3 className="text-sm font-bold text-white">Reschedule Clinic Visit</h3>
                <button
                  onClick={() => setShowRescheduleModal(false)}
                  className="text-slate-400 hover:text-white text-lg"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleRescheduleSubmit} className="space-y-4">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">New Date</label>
                  <input
                    type="date"
                    min="2026-09-16"
                    value={rescheduleDate}
                    onChange={(e) => setRescheduleDate(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">New Time Slot</label>
                  <select
                    value={rescheduleSlot}
                    onChange={(e) => setRescheduleSlot(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                  >
                    <option value="09:30 AM – 10:00 AM">09:30 AM – 10:00 AM</option>
                    <option value="10:30 AM – 11:00 AM">10:30 AM – 11:00 AM</option>
                    <option value="11:00 AM – 11:30 AM">11:00 AM – 11:30 AM</option>
                    <option value="02:30 PM – 03:00 PM">02:30 PM – 03:00 PM</option>
                    <option value="03:30 PM – 04:00 PM">03:30 PM – 04:00 PM</option>
                  </select>
                </div>

                <div className="flex gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowRescheduleModal(false)}
                    className="flex-1 py-2.5 rounded-xl bg-slate-800 text-slate-300 font-semibold border border-slate-700 hover:bg-slate-700"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold"
                  >
                    Confirm Slot
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* UPLOAD REPORT MODAL                                       */}
        {/* ========================================================= */}
        {showUploadModal && (
          <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-[#0F172A] border border-slate-700 rounded-3xl p-6 max-w-md w-full space-y-4 shadow-2xl text-xs">
              <div className="flex justify-between items-center border-b border-slate-800 pb-3">
                <h3 className="text-sm font-bold text-white">Upload Diagnostic Lab Report</h3>
                <button
                  onClick={() => setShowUploadModal(false)}
                  className="text-slate-400 hover:text-white text-lg"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleReportUpload} className="space-y-4">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Test Name / Description</label>
                  <input
                    type="text"
                    placeholder="e.g. Serum Uric Acid & Kidney Function Panel"
                    value={newReportTitle}
                    onChange={(e) => setNewReportTitle(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Diagnostic Laboratory</label>
                  <input
                    type="text"
                    placeholder="e.g. Dr. Lal PathLabs or SRL Diagnostics"
                    value={newReportLab}
                    onChange={(e) => setNewReportLab(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                    required
                  />
                </div>

                <div className="p-6 border-2 border-dashed border-slate-700 rounded-2xl text-center space-y-2 bg-slate-950/60">
                  <div className="text-2xl text-teal-400">📤</div>
                  <div className="text-slate-300 font-semibold">Drop your PDF, DICOM, or JPG file here</div>
                  <div className="text-slate-500 text-[10px]">Maximum file size: 25MB • ABDM Encrypted</div>
                </div>

                <div className="flex gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowUploadModal(false)}
                    className="flex-1 py-2.5 rounded-xl bg-slate-800 text-slate-300 font-semibold border border-slate-700 hover:bg-slate-700"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold"
                  >
                    Submit Report
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
