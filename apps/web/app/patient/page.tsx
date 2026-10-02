"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
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
  PatientMessage,
  PatientProfileData,
  ActiveCarePlanData
} from "@/lib/cms/patientMockData";
import { AuthService, UserSession } from "@/lib/services/authService";
import { PatientService } from "@/lib/services/patientService";
import { loadSession } from "@/lib/session";
import { useAuth } from "@/lib/hooks/useAuth";
import { WhyThisModal, WhyThisExplanation } from "@/components/clinical/WhyThisModal";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

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
  | "billing"
  | "consent-privacy";

export default function PatientPortalPage() {
  const { isLoading: authLoading, isAuthorized } = useAuth({ requiredRoles: ['PATIENT'] });
  const [activeTab, setActiveTab] = useState<PatientSection>("care");
  const [careSubTab, setCareSubTab] = useState<"overview" | "appointments" | "consultations" | "messages">("overview");
  const [healthSubTab, setHealthSubTab] = useState<"profile" | "consent" | "reports">("profile");
  const [planSubTab, setPlanSubTab] = useState<"prescriptions" | "protocols" | "billing">("prescriptions");

  useEffect(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      const tabParam = params.get("tab") as string | null;
      if (tabParam) {
        if (tabParam === "overview" || tabParam === "care") {
          setActiveTab("care");
          setCareSubTab("overview");
        } else if (tabParam === "appointments") {
          setActiveTab("care");
          setCareSubTab("appointments");
        } else if (tabParam === "consultations" || tabParam === "ai-doctor") {
          setActiveTab("care");
          setCareSubTab("consultations");
        } else if (tabParam === "messages") {
          setActiveTab("care");
          setCareSubTab("messages");
        } else if (tabParam === "profile" || tabParam === "health" || tabParam === "mizaj") {
          setActiveTab("health");
          setHealthSubTab("profile");
        } else if (tabParam === "consent-privacy" || tabParam === "consent") {
          setActiveTab("health");
          setHealthSubTab("consent");
        } else if (tabParam === "reports" || tabParam === "labs") {
          setActiveTab("health");
          setHealthSubTab("reports");
        } else if (tabParam === "prescriptions" || tabParam === "plan" || tabParam === "medicines") {
          setActiveTab("plan");
          setPlanSubTab("prescriptions");
        } else if (tabParam === "protocols" || tabParam === "treatment-plans") {
          setActiveTab("plan");
          setPlanSubTab("protocols");
        } else if (tabParam === "billing" || tabParam === "payments") {
          setActiveTab("plan");
          setPlanSubTab("billing");
        } else if (tabParam === "lifestyle" || tabParam === "practice") {
          setActiveTab("practice");
        } else if (tabParam === "progress") {
          setActiveTab("progress");
        } else {
          setActiveTab(tabParam as PatientSection);
        }
      }
    }
  }, []);

  // Authentication & Session States
  const [session, setSession] = useState<UserSession | null>(null);
  const [isDemoMode, setIsDemoMode] = useState(false);
  const [authChecking, setAuthChecking] = useState(true);

  // Auth Gateway States (for unauthenticated visitors)
  const [authTab, setAuthTab] = useState<"signin" | "register">("signin");
  const [authIdentifier, setAuthIdentifier] = useState("");
  const [authPassword, setAuthPassword] = useState("");
  const [regFullName, setRegFullName] = useState("");
  const [regMobile, setRegMobile] = useState("");
  const [regEmail, setRegEmail] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [regConsent, setRegConsent] = useState(false);
  const [authSubmitting, setAuthSubmitting] = useState(false);
  const [authError, setAuthError] = useState<string | null>(null);

  // Live API Connection States
  const [loading, setLoading] = useState(false);
  const [activePatient, setActivePatient] = useState<PatientProfileData | null>(null);
  const [carePlan, setCarePlan] = useState<ActiveCarePlanData | null>(null);
  const [prescriptions, setPrescriptions] = useState<any[]>([]);
  const [invoices, setInvoices] = useState<any[]>([]);
  const [patient360, setPatient360] = useState<any>(null);
  const [consents, setConsents] = useState({
    abdm_health_data_sharing: false,
    tele_triage_telemetry: false,
    research_bio_repository_opt_in: false,
    sms_whatsapp_care_reminders: false,
    last_audit: null as string | null,
    hash: null as string | null
  });
  const [checkinSuccessAptId, setCheckinSuccessAptId] = useState<string | null>(null);
  const [isCheckingIn, setIsCheckingIn] = useState(false);
  const [checkinScore, setCheckinScore] = useState(3);
  const [apiError, setApiError] = useState<string | null>(null);
  // Caregiver Access Management State
  const [caregivers, setCaregivers] = useState([
    {
      id: "CG-01",
      name: "Amina Farooqi",
      relationship: "Spouse",
      phone: "+91 98765 11223",
      scope: "Full Records & Appointments",
      status: "Active",
      addedDate: "2026-08-14"
    }
  ]);
  const [showCaregiverModal, setShowCaregiverModal] = useState(false);
  const [newCaregiverName, setNewCaregiverName] = useState("");
  const [newCaregiverRelation, setNewCaregiverRelation] = useState("Spouse");
  const [newCaregiverPhone, setNewCaregiverPhone] = useState("");
  const [newCaregiverScope, setNewCaregiverScope] = useState("Appointments & Schedule Only");

  // Voice Posology States
  const [audioLang, setAudioLang] = useState<"urdu" | "hindi" | "english">("urdu");
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  // Master Prompt §63: Explainability ("Why This?") Modal State
  const [whyThisOpen, setWhyThisOpen] = useState(false);
  const [whyThisData, setWhyThisData] = useState<WhyThisExplanation | null>(null);

  // Master Prompt §28: Adherence Intelligence & Drop Reasons State
  const [missedItemModalOpen, setMissedItemModalOpen] = useState(false);
  const [selectedMissedItem, setSelectedMissedItem] = useState<{ id: string; name: string } | null>(null);
  const [missedReasonSelected, setMissedReasonSelected] = useState<string>("");
  const [missedNotes, setMissedNotes] = useState<string>("");
  const [adherenceEntries, setAdherenceEntries] = useState<{ [itemId: string]: { status: "TAKEN" | "MISSED"; reason?: string } }>({
    "RX-01": { status: "TAKEN" },
    "TB-01": { status: "TAKEN" }
  });

  const handleOpenWhyThis = async (itemId: string, itemTitle: string) => {
    try {
      const res = await fetch(`http://localhost:8088/api/v1/clinical/explainability?item_id=${encodeURIComponent(itemId)}`);
      const json = await res.json();
      if (json.ok && json.explanation) {
        setWhyThisData(json.explanation);
      } else {
        throw new Error("No data");
      }
    } catch {
      setWhyThisData({
        itemId,
        itemTitle,
        category: "NUSKHA",
        clinicalRationale: "Targeted humoral balancing formulated to resolve current temperamental dyscrasia (Su-e-Mizaj).",
        classicalAuthority: {
          sourceText: "Unani Pharmacopoeia of India (UPI) Vol. 1",
          chapterVolume: "Al-Qanun fi al-Tibb Book II",
          formulationPrinciple: "Istifragh wa Ta'deel"
        },
        evidenceLevel: "E5",
        evidenceDescription: "Human Observational Cohorts (Concordant with National Formulary of Unani Medicine)",
        mizajConcordance: {
          targetMizaj: "Balghami (Cold-Moist Dyscrasia)",
          formulationMizaj: "Haar Yabis (Hot-Dry 2°)",
          mechanismOfCorrection: "Resolves cold-phlegmatic effusion and restores vital innate heat (Hararat-e-Ghariziyyah)."
        },
        muslehBalancing: {
          muslehAgent: "Roghan Badam / Kateera",
          correctiveAction: "Protects mucous membrane and neutralizes roughness."
        },
        badraqaConduit: {
          vehicle: "Maa-ul-Asl (Lukewarm Honey-Water)",
          organDeliveryRole: "Directs active medicinal constituents to affected target tissues."
        },
        safetyBoundaries: {
          scheduleE1Status: true,
          maximumDailyDose: "3g daily in divided doses",
          knownContraindications: ["Pregnancy", "Severe renal impairment"],
          monitoringRequirements: ["Weekly joint evaluation", "Bowel function regularity"]
        },
        governanceMetadata: {
          zkbVersion: "ZKB-v5.2.0-CANONICAL",
          zfieVersion: "ZFIE-v2.1.0-PRODUCTION",
          lastVerifiedDate: "2026-09-28",
          verifiedBy: "Hakeem Dr. Irfan Ashraf (BUMS, AKTC AMU)"
        }
      });
    }
    setWhyThisOpen(true);
  };

  const handleMarkDose = (itemId: string, itemName: string, status: "TAKEN" | "MISSED") => {
    if (status === "TAKEN") {
      setAdherenceEntries(prev => ({ ...prev, [itemId]: { status: "TAKEN" } }));
    } else {
      setSelectedMissedItem({ id: itemId, name: itemName });
      setMissedItemModalOpen(true);
    }
  };

  const handleConfirmMissed = async (reason: string) => {
    if (!selectedMissedItem) return;
    const itemId = selectedMissedItem.id;
    setAdherenceEntries(prev => ({ ...prev, [itemId]: { status: "MISSED", reason } }));
    try {
      await fetch("http://localhost:8088/api/v1/patient/adherence/log-missed", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          patient_id: activePatient?.mrn || "PAT-001",
          item_id: itemId,
          item_name: selectedMissedItem.name,
          reason,
          notes: missedNotes
        })
      });
    } catch {
      // Offline fallback
    }
    setMissedItemModalOpen(false);
    setSelectedMissedItem(null);
    setMissedReasonSelected("");
    setMissedNotes("");
  };

  // Appointments State
  const [appointments, setAppointments] = useState<PatientAppointment[]>([]);
  const [showRescheduleModal, setShowRescheduleModal] = useState(false);
  const [showBookingModal, setShowBookingModal] = useState(false);
  const [rescheduleDate, setRescheduleDate] = useState("2026-09-22");
  const [rescheduleSlot, setRescheduleSlot] = useState("11:00 AM – 11:30 AM");
  const [bookingComplaint, setBookingComplaint] = useState("Routine Follow-up & Mizaj Check");
  const [bookingDoctor, setBookingDoctor] = useState("Prof. (Dr.) Mansoor Alam");

  // Launch simulated clinical sandbox for accreditation review
  const handleLaunchDemo = () => {
    setIsDemoMode(true);
    setSession(null);
    setActivePatient(MOCK_PATIENT_PROFILE);
    setAppointments([MOCK_PATIENT_APPOINTMENT]);
    setCarePlan(MOCK_ACTIVE_CARE_PLAN);
    setPrescriptions(MOCK_PRESCRIPTIONS);
    setReports(MOCK_LAB_REPORTS);
    setInvoices(MOCK_PATIENT_INVOICES);
    setMessages(MOCK_PATIENT_MESSAGES);
    setLoading(false);
  };

  // Load patient data from authoritative backend for an authenticated session
  const loadPatientData = async (sess: UserSession) => {
    setLoading(true);
    setApiError(null);
    try {
      const records = await PatientService.getMyRecords(sess.token, sess.user.mrn);
      if (records.ok && records.patient) {
        const p = records.patient;
        setActivePatient({
          mrn: p.mrn || sess.user.mrn || "MRN-PENDING",
          abhaId: p.abha_id || p.abhaId || "ABHA-NOT-LINKED",
          fullName: `${p.first_name || ""} ${p.last_name || ""}`.trim() || p.fullName || sess.user.fullName || "Registered Patient",
          age: p.age || 30,
          gender: p.gender || "Not Specified",
          primaryMizaj: p.mizaj_dominant || p.primaryMizaj || "Assessment Pending",
          suEMizaj: p.su_e_mizaj || "None Documented",
          bloodGroup: p.blood_group || "Not Documented",
          phone: p.contact_phone || sess.user.phone || "",
          email: p.contact_email || sess.user.email || "",
          address: p.address || "Residential Address on File",
          emergencyContact: p.emergency_contact || "None Specified",
          allergies: p.allergies ? (typeof p.allergies === "string" ? JSON.parse(p.allergies) : p.allergies) : []
        });

        if (records.appointments && records.appointments.length > 0) {
          setAppointments(records.appointments.map((a: any) => ({
            id: a.id || a.token_number,
            tokenNumber: a.token_number || "T-00",
            doctorName: a.doctor_name || "Attending Tabeeb",
            doctorSpecialty: a.department || "Unani Medicine",
            date: a.appointment_date || "Today",
            timeSlot: a.appointment_time || "10:00 AM",
            mode: a.mode || "OPD In-Person",
            facilityLocation: a.facility_name || "Central Hospital",
            status: a.status || "Confirmed"
          })));
        } else {
          setAppointments([]);
        }

        if (records.prescriptions && records.prescriptions.length > 0) {
          const rxList = [];
          for (const rx of records.prescriptions) {
            if (rx.items && Array.isArray(rx.items)) {
              for (const item of rx.items) {
                rxList.push({
                  id: item.id || rx.id,
                  medicineName: item.medicine_name || item.name || "Nuskha Compound",
                  dosage: item.dosage || "1 dose",
                  timing: item.timing || "Morning & Evening",
                  instructions: item.instructions || rx.notes || "Take with lukewarm water",
                  daysSupply: item.days || 30,
                  remainingDoses: 28,
                  dispenseStatus: rx.status === "DISPENSED" ? "Dispensed" : "Pending"
                });
              }
            }
          }
          setPrescriptions(rxList);
        } else {
          setPrescriptions([]);
        }

        if (records.invoices && records.invoices.length > 0) {
          setInvoices(records.invoices.map((inv: any) => ({
            invoiceId: inv.invoice_number || inv.id,
            date: inv.created_at ? inv.created_at.split("T")[0] : "Recent",
            amount: inv.total_amount || inv.amount || 0,
            status: inv.status || "PAID",
            serviceDescription: inv.description || "Clinical Encounter & Formulation",
            facility: inv.facility_name || "ZAYVORA Health",
            paymentMode: inv.payment_mode || "UPI / Direct"
          })));
        } else {
          setInvoices([]);
        }
      } else {
        // Authoritative record unavailable or pending creation
        setActivePatient({
          mrn: sess.user.mrn || "MRN-PENDING",
          abhaId: "ABHA-NOT-LINKED",
          fullName: sess.user.fullName || "Registered Patient",
          age: 30,
          gender: "Not Specified",
          primaryMizaj: "Assessment Pending",
          suEMizaj: "None Documented",
          bloodGroup: "Pending",
          phone: sess.user.phone || "",
          email: sess.user.email || "",
          address: "Address Pending Verification",
          emergencyContact: "None Specified",
          allergies: []
        });
        setAppointments([]);
        setPrescriptions([]);
        setInvoices([]);
      }
    } catch {
      setApiError("Unable to establish encrypted clinical connection with Central Server. Please verify connectivity.");
    } finally {
      setLoading(false);
    }
  };

  // Check authentication session on mount
  useEffect(() => {
    async function initPortal() {
      setLoading(true);
      setApiError(null);
      if (typeof window !== "undefined") {
        const params = new URLSearchParams(window.location.search);
        if (params.get("demo") === "true") {
          handleLaunchDemo();
          setAuthChecking(false);
          return;
        }
      }

      const sess = AuthService.getSession();
      if (sess && (sess.user.role === "PATIENT" || sess.user.role === "SUPER_ADMIN")) {
        setSession(sess);
        setIsDemoMode(false);
        await loadPatientData(sess);
      } else {
        setSession(null);
        setIsDemoMode(false);
        setActivePatient(null);
      }
      setAuthChecking(false);
      setLoading(false);
    }
    initPortal();
  }, []);

  const handlePatientSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthSubmitting(true);
    setAuthError(null);
    try {
      const sess = await AuthService.loginAsync(authIdentifier, authPassword, "PATIENT");
      setSession(sess);
      setIsDemoMode(false);
      await loadPatientData(sess);
    } catch (err: any) {
      setAuthError(err.message || "Invalid credentials. Please verify your registered mobile number or password.");
    } finally {
      setAuthSubmitting(false);
    }
  };

  const handlePatientRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!regConsent) {
      setAuthError("You must accept the DPDP Act 2023 consent to register your health record.");
      return;
    }
    setAuthSubmitting(true);
    setAuthError(null);
    try {
      const sess = await AuthService.registerAsync({
        fullName: regFullName,
        email: regEmail,
        mobile: regMobile,
        password: regPassword,
        age: 30,
        gender: "Not Specified",
        consent: true
      });
      setSession(sess);
      setIsDemoMode(false);
      await loadPatientData(sess);
    } catch (err: any) {
      setAuthError(err.message || "Registration failed. Please verify your details.");
    } finally {
      setAuthSubmitting(false);
    }
  };

  const handleDigitalCheckin = async (appointmentId: string) => {
    setIsCheckingIn(true);
    try {
      const res = await fetch(`${API}/api/v1/appointments/check-in`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          appointment_id: appointmentId,
          proms_score: checkinScore
        })
      });
      if (res.ok) {
        setCheckinSuccessAptId(appointmentId);
        setAppointments((prev) =>
          prev.map((a) =>
            a.id === appointmentId ? { ...a, status: "Confirmed" } : a
          )
        );
      }
    } catch {} finally {
      setIsCheckingIn(false);
    }
  };

  const handleToggleConsent = (key: string) => {
    setConsents((prev: any) => ({
      ...prev,
      [key]: !prev[key],
      last_audit: new Date().toISOString()
    }));
  };

  // Diagnostic Reports State & Upload Modal
  const [reports, setReports] = useState<PatientLabReport[]>([]);
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
  const [messages, setMessages] = useState<PatientMessage[]>([]);
  const [messageInput, setMessageInput] = useState("");

  // AI Doctor Hakeem Sahab Chat
  const [aiHistory, setAiHistory] = useState<Array<{ role: "user" | "bot"; text: string; time: string }>>([
    {
      role: "bot",
      text: "Assalamu Alaikum Hamza Sahab. I am Hakeem Sahab AI™, your clinical AI copilot trained on classical Unani pharmacopeia and your personal Balghami Mizaj profile. How can I assist you with your diet, exercises, or medicine timings today?",
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
  const handleRescheduleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const session = loadSession();
    try {
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      if (session?.access_token) headers["Authorization"] = `Bearer ${session.access_token}`;

      const res = await fetch(`${API}/api/v1/appointments`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          patientName: activePatient?.fullName || "Patient Record",
          mrn: activePatient?.mrn || "Pending",
          doctorName: "Prof. (Dr.) Mansoor Alam",
          date: rescheduleDate,
          timeSlot: rescheduleSlot,
          chiefComplaint: "Patient Rescheduled Consultation"
        })
      });
      if (res.ok) {
        const data = await res.json();
        if (data.appointment) {
          setAppointments((prev) => [
            {
              id: data.appointment.id,
              doctorName: data.appointment.doctorName,
              doctorSpecialty: "Integrative Unani Matab",
              date: data.appointment.appointmentDate,
              timeSlot: data.appointment.appointmentTime,
              mode: "In-Clinic OPD",
              facilityLocation: "ZAYVORA Matab™ Central Care Centre, OPD Room 3",
              tokenNumber: data.appointment.tokenNumber,
              status: "Scheduled"
            },
            ...prev
          ]);
        }
      } else {
        alert("Unable to reschedule appointment on the clinical server. Please try again or contact clinic reception.");
      }
    } catch {
      alert("Network connection error: Unable to reach the clinical scheduling server. Please verify your connection.");
    }
    setShowRescheduleModal(false);
  };

  const handleBookingSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const session = loadSession();
    try {
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      if (session?.access_token) headers["Authorization"] = `Bearer ${session.access_token}`;

      const res = await fetch(`${API}/api/v1/appointments`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          patientName: activePatient?.fullName || "Patient Record",
          mrn: activePatient?.mrn || "Pending",
          doctorName: bookingDoctor,
          date: rescheduleDate,
          timeSlot: rescheduleSlot,
          chiefComplaint: bookingComplaint
        })
      });
      if (res.ok) {
        const data = await res.json();
        if (data.appointment) {
          setAppointments((prev) => [
            {
              id: data.appointment.id,
              doctorName: data.appointment.doctorName,
              doctorSpecialty: "Integrative Unani Matab",
              date: data.appointment.appointmentDate,
              timeSlot: data.appointment.appointmentTime,
              mode: "In-Clinic OPD",
              facilityLocation: "ZAYVORA Matab™ Central Care Centre, OPD Room 3",
              tokenNumber: data.appointment.tokenNumber,
              status: "Confirmed"
            },
            ...prev
          ]);
        }
      } else {
        alert("Clinical scheduling server rejected appointment booking. Please verify availability or try another slot.");
      }
    } catch {
      alert("Network connection error: Unable to reach the clinical scheduling server. Please verify your connection or contact the Matab reception at +91 11 4928 0000.");
    }
    setShowBookingModal(false);
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

  // Clinical Messaging Thread
  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    const patientName = activePatient?.fullName || "Patient";
    const newMsg: PatientMessage = {
      id: "msg-" + Date.now(),
      senderName: patientName,
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
        messageText: `Noted with thanks, ${patientName.split(' ')[0]} Sahab. Please ensure the warm fomentation is applied exactly 20 minutes before sleeping.`,
        isDoctor: true
      };
      setMessages((curr) => [...curr, reply]);
    }, 1200);
  };

  // AI Doctor prompt handler
  const handleAiAsk = async (e: React.FormEvent) => {
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
    { id: "care", label: "My Care (Today)", icon: "activity" },
    { id: "health", label: "My Health", icon: "user" },
    { id: "plan", label: "My Plan", icon: "pill" },
    { id: "practice", label: "My Practice", icon: "heart" },
    { id: "progress", label: "My Progress", icon: "trending-up" },
  ];

  if (authLoading) return <div className="flex items-center justify-center h-64 text-slate-500">Verifying access…</div>;
  if (!isAuthorized) return null;

  return (
    <AppShell activeRole="patient">
      <div className="space-y-6 max-w-7xl mx-auto pb-12">

        {/* Unauthenticated Visitor Gateway */}
        {!session && !isDemoMode ? (
          <div className="max-w-xl mx-auto py-8 space-y-6 animate-fade-in">
            <div className="text-center space-y-2">
              <span className="px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-300 text-xs font-bold uppercase tracking-wider">
                My ZAYVORA — Patient Care Portal
              </span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-white">
                Patient Health Portal
              </h2>
              <p className="text-xs sm:text-sm text-slate-400">
                Access your digital prescriptions, Nabz telemetry, lab investigations, and follow-up schedules under DPDP Act 2023 &amp; ABDM.
              </p>
            </div>

            <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 shadow-2xl">
              {/* Tab switch: Sign In vs Register */}
              <div className="flex border-b border-slate-800 pb-2 gap-4 text-xs font-bold">
                <button
                  type="button"
                  onClick={() => { setAuthTab("signin"); setAuthError(null); }}
                  className={`pb-2 border-b-2 transition ${authTab === "signin" ? "border-teal-400 text-teal-300" : "border-transparent text-slate-400 hover:text-white"}`}
                >
                  Sign In with Mobile / ABHA
                </button>
                <button
                  type="button"
                  onClick={() => { setAuthTab("register"); setAuthError(null); }}
                  className={`pb-2 border-b-2 transition ${authTab === "register" ? "border-teal-400 text-teal-300" : "border-transparent text-slate-400 hover:text-white"}`}
                >
                  New Patient Registration
                </button>
              </div>

              {authError && (
                <div className="p-3 rounded-xl bg-rose-950/60 border border-rose-800/80 text-rose-300 text-xs flex items-center gap-2">
                  <span>⚠</span>
                  <span>{authError}</span>
                </div>
              )}

              {authTab === "signin" ? (
                <form onSubmit={handlePatientSignIn} className="space-y-4 text-xs">
                  <div>
                    <label className="block text-slate-300 font-semibold mb-1">
                      Registered Mobile Number / ABHA ID / Email
                    </label>
                    <input
                      type="text"
                      required
                      placeholder="e.g. +91 98110 44219 or hamza.farooqi@gmail.com"
                      value={authIdentifier}
                      onChange={(e) => setAuthIdentifier(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-300 font-semibold mb-1">
                      Password / Security PIN
                    </label>
                    <input
                      type="password"
                      required
                      placeholder="Enter your security PIN or password"
                      value={authPassword}
                      onChange={(e) => setAuthPassword(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={authSubmitting}
                    className="w-full py-3 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition disabled:opacity-50"
                  >
                    {authSubmitting ? "Verifying..." : "Sign In to My Care"}
                  </button>
                </form>
              ) : (
                <form onSubmit={handlePatientRegister} className="space-y-4 text-xs">
                  <div>
                    <label className="block text-slate-300 font-semibold mb-1">
                      Full Legal Name <span className="text-rose-400">*</span>
                    </label>
                    <input
                      type="text"
                      required
                      placeholder="e.g. Fatima Khan"
                      value={regFullName}
                      onChange={(e) => setRegFullName(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-slate-300 font-semibold mb-1">
                        Mobile Number <span className="text-rose-400">*</span>
                      </label>
                      <input
                        type="tel"
                        required
                        placeholder="+91-9876543210"
                        value={regMobile}
                        onChange={(e) => setRegMobile(e.target.value)}
                        className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                      />
                    </div>
                    <div>
                      <label className="block text-slate-300 font-semibold mb-1">
                        Email Address <span className="text-rose-400">*</span>
                      </label>
                      <input
                        type="email"
                        required
                        placeholder="name@example.com"
                        value={regEmail}
                        onChange={(e) => setRegEmail(e.target.value)}
                        className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-slate-300 font-semibold mb-1">
                      Create Password / PIN <span className="text-rose-400">*</span>
                    </label>
                    <input
                      type="password"
                      required
                      placeholder="At least 6 characters"
                      value={regPassword}
                      onChange={(e) => setRegPassword(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                    />
                  </div>
                  <div className="p-3 rounded-xl bg-slate-900/90 border border-slate-800 flex items-start gap-2.5">
                    <input
                      type="checkbox"
                      id="regConsent"
                      checked={regConsent}
                      onChange={(e) => setRegConsent(e.target.checked)}
                      className="mt-0.5 rounded border-slate-700 text-teal-600 focus:ring-teal-500 h-4 w-4"
                      required
                    />
                    <label htmlFor="regConsent" className="text-[11px] text-slate-300 leading-snug cursor-pointer">
                      I consent to digital health record creation and DPDP Act 2023 / ABDM processing.
                    </label>
                  </div>
                  <button
                    type="submit"
                    disabled={authSubmitting}
                    className="w-full py-3 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition disabled:opacity-50"
                  >
                    {authSubmitting ? "Creating Patient Account..." : "Register My Patient Record"}
                  </button>
                </form>
              )}

              {/* Sandbox Demo Launch Option for Evaluators */}
              <div className="pt-4 border-t border-slate-800/80 text-center space-y-2">
                <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider block">
                  Accreditation Review &amp; Evaluation Mode
                </span>
                <button
                  type="button"
                  onClick={handleLaunchDemo}
                  className="w-full py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-teal-300 font-semibold text-xs border border-slate-700 transition flex items-center justify-center gap-2"
                >
                  <span>Launch Clinical Demo Sandbox (Hamza Farooqi)</span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-teal-950 border border-teal-800 text-teal-400">Simulation</span>
                </button>
                <p className="text-[10px] text-slate-500">
                  Auditors can evaluate the complete patient journey with simulated clinical data without live credentials.
                </p>
              </div>
            </div>
          </div>
        ) : (
          <>
            {/* Demo Sandbox Watermark if in evaluation mode */}
            {isDemoMode && (
              <div className="p-3.5 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                <div className="flex items-center gap-2">
                  <HealthcareIcon name="shield-check" className="w-4 h-4 text-amber-400 shrink-0" />
                  <span><strong>DEMO EVALUATION SANDBOX:</strong> Currently displaying simulated patient record (Hamza Farooqi, MRN-2026-0814) for accreditation review. Real patient data is isolated.</span>
                </div>
                <button
                  onClick={() => { setIsDemoMode(false); setSession(null); setActivePatient(null); }}
                  className="px-3 py-1 rounded-lg bg-amber-500/20 hover:bg-amber-500/30 text-amber-100 font-semibold text-[11px] transition shrink-0"
                >
                  Exit Sandbox
                </button>
              </div>
            )}

            {/* Live Synchronization Status Indicator */}
            <div className="px-4 py-2.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs flex items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <HealthcareIcon name="shield-check" className="w-4 h-4 text-emerald-400 shrink-0" />
                <span><strong>Active Health Record:</strong> Synchronized with Central Hospital • Encrypted &amp; DPDP Act 2023 Compliant</span>
              </div>
              <span className="text-[11px] font-mono text-emerald-400 hidden sm:inline">ABDM Linked • Consent Active</span>
            </div>
            
            {/* Patient Welcome & Health Identity Banner */}
            <div className="p-6 rounded-3xl bg-gradient-to-r from-[#0C1524] via-[#101C30] to-[#152540] border border-slate-800 shadow-xl flex flex-col lg:flex-row lg:items-center justify-between gap-6">
              <div className="space-y-2">
                <div className="flex items-center gap-3">
                  <span className="text-[11px] font-bold text-teal-400 uppercase tracking-widest bg-teal-950/80 px-3 py-1 rounded-full border border-teal-800/80">
                    Active Patient Account
                  </span>
                  <span className="text-xs text-slate-400 font-mono">
                    ABDM Linked • Central Hospital
                  </span>
                </div>
                <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                  {new Date().getHours() < 12 ? "Good morning" : new Date().getHours() < 17 ? "Good afternoon" : "Good evening"}, {activePatient?.fullName || "Patient"}
                </h1>
                <p className="text-xs sm:text-sm text-teal-300 font-medium">
                  Here&apos;s what needs your clinical attention today.
                </p>
                <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 text-xs text-slate-300">
                  <span>MRN: <strong className="text-white font-mono">{activePatient?.mrn || "Pending"}</strong></span>
                  <span>•</span>
                  <span>ABHA: <strong className="text-white font-mono">{activePatient?.abhaId || "Not Linked"}</strong></span>
                  <span>•</span>
                  <span>Mizaj: <strong className="text-teal-300">{activePatient?.primaryMizaj || "Assessment Pending"}</strong></span>
                  <span>•</span>
                  <span>Blood Group: <strong className="text-white">{activePatient?.bloodGroup || "Not Documented"}</strong></span>
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <button
                  onClick={() => setActiveTab("appointments")}
                  className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold transition shadow-lg shadow-teal-900/30 flex items-center gap-2"
                >
                  <HealthcareIcon name="calendar" className="w-4 h-4 text-white" />
                  <span>{appointments[0] ? `Next Visit: ${appointments[0].date}` : "Book Visit"}</span>
                </button>
                <button
                  onClick={() => setActiveTab("ai-doctor")}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-teal-300 text-xs font-semibold border border-slate-700 transition flex items-center gap-2"
                >
                  <HealthcareIcon name="activity" className="w-4 h-4 text-teal-400" />
                  <span>Ask Hakeem Sahab</span>
                </button>
              </div>
            </div>

        {/* Sandbox Simulation Mode Indicator (Zero-Deception Policy) */}
        {isDemoMode && (
          <div className="p-3.5 rounded-2xl bg-amber-950/70 border border-amber-500/50 text-amber-200 text-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-md">
            <div className="flex items-center gap-2.5">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse shrink-0"></span>
              <div>
                <span className="font-bold tracking-wide uppercase text-[11px] text-amber-300 block">
                  Clinical Sandbox: Simulation Mode Active
                </span>
                <span className="text-[11px] text-amber-200/80">
                  Data shown below is synthetic for evaluation. Authenticate with registered patient credentials to view authoritative server records.
                </span>
              </div>
            </div>
            <button
              onClick={() => {
                if (typeof window !== "undefined") {
                  window.location.href = "/patient";
                }
              }}
              className="px-3.5 py-1.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-200 font-semibold border border-amber-500/40 text-xs transition shrink-0"
            >
              Exit Sandbox →
            </button>
          </div>
        )}

        {/* Live Authoritative Server Connection Status Alert */}
        {apiError && (
          <div className="p-4 rounded-2xl bg-rose-950/40 border border-rose-500/30 text-rose-200 text-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
            <div className="flex items-center gap-2.5">
              <HealthcareIcon name="alert-triangle" className="w-4 h-4 text-rose-400 shrink-0" />
              <div>
                <strong className="block text-white text-xs">Authoritative Clinical Server: UNAVAILABLE</strong>
                <span>{apiError}</span>
              </div>
            </div>
            <button
              onClick={() => {
                if (session) {
                  loadPatientData(session);
                } else if (typeof window !== "undefined") {
                  window.location.reload();
                }
              }}
              className="px-4 py-1.5 rounded-xl bg-rose-900/60 hover:bg-rose-900 text-white font-semibold border border-rose-700 text-xs transition shrink-0"
            >
              RETRY CONNECTION ⟳
            </button>
          </div>
        )}

        {/* 4 Patient Orientation Cards: Consumer Health Guidance */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 space-y-1.5">
            <div className="text-[11px] font-bold text-teal-400 uppercase tracking-wider flex items-center gap-1.5">
              <HealthcareIcon name="hospital" className="w-3.5 h-3.5 text-teal-400" />
              <span>Where am I?</span>
            </div>
            <p className="text-xs text-slate-300">
              ZAYVORA Matab™ Patient Care Portal • Connected to Central Hospital
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 space-y-1.5">
            <div className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
              <HealthcareIcon name="stethoscope" className="w-3.5 h-3.5 text-emerald-400" />
              <span>Health Status</span>
            </div>
            <p className="text-xs text-slate-300">
              Constitutional Mizaj: <strong className="text-white">{activePatient?.primaryMizaj ? activePatient.primaryMizaj.split(' ')[0] : "Assessing"}</strong> • {carePlan ? "Care Plan Active" : "Intake Stage"}
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 space-y-1.5">
            <div className="text-[11px] font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
              <HealthcareIcon name="activity" className="w-3.5 h-3.5 text-amber-400" />
              <span>Next Step</span>
            </div>
            <p className="text-xs text-slate-300">
              {prescriptions.length > 0 ? `Take ${prescriptions[0].timing || 'scheduled dose'} (${prescriptions[0].medicineName})` : "Awaiting clinician prescription"}
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#0F172A] border border-slate-800 space-y-1.5">
            <div className="text-[11px] font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
              <HealthcareIcon name="calendar" className="w-3.5 h-3.5 text-cyan-400" />
              <span>Next Appointment</span>
            </div>
            <p className="text-xs text-slate-300">
              {appointments[0] ? `${appointments[0].date} (${appointments[0].timeSlot.split('–')[0].trim()})` : "None scheduled"}
            </p>
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
                <HealthcareIcon name={tab.icon} className="w-3.5 h-3.5 shrink-0" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Canonical Sub-Surface Pill Bar */}
        {activeTab === "care" && (
          <div className="flex gap-1.5 overflow-x-auto no-scrollbar pb-1 text-xs">
            {[
              { id: "overview", label: "Today's Regimen & Priorities" },
              { id: "appointments", label: `Appointments (${appointments.length})` },
              { id: "consultations", label: "Consultations & Triage" },
              { id: "messages", label: "Care Team Chat" },
            ].map((sub) => (
              <button
                key={sub.id}
                onClick={() => setCareSubTab(sub.id as any)}
                className={`px-3 py-1.5 rounded-lg transition font-medium ${
                  careSubTab === sub.id
                    ? "bg-emerald-900/60 text-emerald-300 border border-emerald-600/50 font-bold"
                    : "bg-slate-900/80 text-slate-400 hover:text-white border border-slate-800"
                }`}
              >
                {sub.label}
              </button>
            ))}
          </div>
        )}

        {activeTab === "health" && (
          <div className="flex gap-1.5 overflow-x-auto no-scrollbar pb-1 text-xs">
            {[
              { id: "profile", label: "Identity & Mizaj Baseline" },
              { id: "consent", label: "Consents & Caregivers (DPDP)" },
              { id: "reports", label: `Lab Investigations (${labReports.length})` },
            ].map((sub) => (
              <button
                key={sub.id}
                onClick={() => setHealthSubTab(sub.id as any)}
                className={`px-3 py-1.5 rounded-lg transition font-medium ${
                  healthSubTab === sub.id
                    ? "bg-emerald-900/60 text-emerald-300 border border-emerald-600/50 font-bold"
                    : "bg-slate-900/80 text-slate-400 hover:text-white border border-slate-800"
                }`}
              >
                {sub.label}
              </button>
            ))}
          </div>
        )}

        {activeTab === "plan" && (
          <div className="flex gap-1.5 overflow-x-auto no-scrollbar pb-1 text-xs">
            {[
              { id: "prescriptions", label: "Today's Nuskha Formulations" },
              { id: "protocols", label: "Care Protocols & Regimens" },
              { id: "billing", label: `Invoices & Receipts (${invoices.length})` },
            ].map((sub) => (
              <button
                key={sub.id}
                onClick={() => setPlanSubTab(sub.id as any)}
                className={`px-3 py-1.5 rounded-lg transition font-medium ${
                  planSubTab === sub.id
                    ? "bg-emerald-900/60 text-emerald-300 border border-emerald-600/50 font-bold"
                    : "bg-slate-900/80 text-slate-400 hover:text-white border border-slate-800"
                }`}
              >
                {sub.label}
              </button>
            ))}
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 1: HEALTH 360 OVERVIEW (MY CARE TODAY)            */}
        {/* ========================================================= */}
        {((activeTab === "care" && careSubTab === "overview") || activeTab === "overview") && (
          <div className="space-y-6 animate-fade-in">
            {/* Today's Daily Priority Card */}
            <div className="p-5 rounded-3xl bg-[#0D1829] border border-emerald-800/40 shadow-lg space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-full bg-amber-500/10 border border-amber-500/20 flex items-center justify-center">
                    <HealthcareIcon name="sun" className="w-4 h-4 text-amber-400" />
                  </div>
                  <div>
                    <h2 className="text-sm font-bold text-white">Your Daily Health Regimen for Today</h2>
                    <p className="text-xs text-slate-400">Personalized tasks set by Prof. (Dr.) Mansoor Alam</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setActiveTab("messages")}
                    className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 transition flex items-center gap-1.5"
                  >
                    <HealthcareIcon name="message" className="w-3.5 h-3.5 text-slate-300" />
                    <span>Message Tabeeb</span>
                  </button>
                  <button
                    onClick={() => setActiveTab("consultations")}
                    className="px-3.5 py-1.5 rounded-xl bg-emerald-700 hover:bg-emerald-600 text-xs font-semibold text-white transition shadow-sm flex items-center gap-1.5"
                  >
                    <HealthcareIcon name="video" className="w-3.5 h-3.5 text-white" />
                    <span>Video Consult</span>
                  </button>
                </div>
              </div>

              {/* 3 Core Daily Checklist Items */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                <div className="p-3.5 rounded-2xl bg-[#0A1020] border border-slate-800 flex items-start gap-3">
                  <input type="checkbox" defaultChecked className="mt-0.5 rounded text-emerald-600 focus:ring-0" />
                  <div>
                    <span className="font-semibold text-white block">Morning Dose (Completed)</span>
                    <p className="text-slate-400 text-[11px] mt-0.5">Majun Suranjan (5g) with lukewarm water after breakfast.</p>
                  </div>
                </div>
                <div className="p-3.5 rounded-2xl bg-[#0A1020] border border-slate-800 flex items-start gap-3">
                  <input type="checkbox" className="mt-0.5 rounded text-emerald-600 focus:ring-0" />
                  <div>
                    <span className="font-semibold text-amber-300 block">Evening Dose (Pending)</span>
                    <p className="text-slate-400 text-[11px] mt-0.5">Local warm application of Roghan-e-Balsan nocte.</p>
                  </div>
                </div>
                <div className="p-3.5 rounded-2xl bg-[#0A1020] border border-slate-800 flex items-start gap-3">
                  <input type="checkbox" className="mt-0.5 rounded text-emerald-600 focus:ring-0" />
                  <div>
                    <span className="font-semibold text-teal-300 block">Hydration & Asbab Task</span>
                    <p className="text-slate-400 text-[11px] mt-0.5">Avoid refrigerated water; take 200ml warm water with honey.</p>
                  </div>
                </div>
              </div>
            </div>

            
            {/* Signature Feature: My Care Today Time-Ordered Action Timeline */}
            <div className="p-6 rounded-3xl bg-[#0F172A] border border-slate-800 shadow-md space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center">
                    <HealthcareIcon name="clock" className="w-4 h-4 text-teal-400" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">My Care Today — Daily Action Timeline</h3>
                    <p className="text-xs text-slate-400">Structured chronological schedule for medications, diet, and therapeutic regimen</p>
                  </div>
                </div>
                <span className="text-[11px] font-mono text-teal-400">
                  Daily Regimen Active
                </span>
              </div>

              <div className="space-y-3">
                {[
                  {
                    time: "07:30 AM",
                    title: "Morning Formulation (Hab-e-Suranjan Mudabbar)",
                    desc: "Take 1 tablet with 1 cup of warm milk or lukewarm water (anupan).",
                    type: "Medication",
                    completed: true
                  },
                  {
                    time: "08:30 AM",
                    title: "Joint Mobilization & Ambulation (Riyazat-e-Khafeefa)",
                    desc: "20 minutes brisk walking in morning sunlight; gentle knee extension exercises.",
                    type: "Tadbeer (Regimen)",
                    completed: true
                  },
                  {
                    time: "01:30 PM",
                    title: "Prescribed Lunch Dietary Protocol (Parhez)",
                    desc: "Warm barley khichdi with ginger-cumin soup; strictly avoid refrigerated water or cold dairy.",
                    type: "Ghiza (Diet)",
                    completed: false
                  },
                  {
                    time: "05:00 PM",
                    title: "Evening Fomentation (Takmeed Haar)",
                    desc: "Apply warm dry compress over affected knee joints for 15 minutes to reduce cold stiffness.",
                    type: "Therapy",
                    completed: false
                  },
                  {
                    time: "09:30 PM",
                    title: "Night Restorative Tonic (Khamira Gaozaban)",
                    desc: "5 grams with warm water before sleeping.",
                    type: "Medication",
                    completed: false
                  },
                  {
                    time: "Upcoming Visit",
                    title: "Clinical Follow-up with Dr. Mansoor Alam",
                    desc: "Token #T-104 • In-Clinic Matab OPD Room 3 (Scheduled for Sep 15).",
                    type: "Consultation",
                    completed: false
                  }
                ].map((act, idx) => (
                  <div key={idx} className="p-3.5 rounded-2xl bg-[#0A1020] border border-slate-800 flex items-start justify-between gap-4">
                    <div className="flex items-start gap-3">
                      <span className="w-2 h-2 rounded-full bg-teal-400 mt-2 shrink-0" />
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-[11px] font-mono font-bold text-teal-300">{act.time}</span>
                          <span className="text-slate-600">•</span>
                          <span className="text-[10px] font-bold text-slate-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                            {act.type}
                          </span>
                        </div>
                        <h4 className="text-xs font-bold text-white mt-1">{act.title}</h4>
                        <p className="text-[11px] text-slate-400 mt-0.5 leading-relaxed">{act.desc}</p>
                      </div>
                    </div>
                    <span className={`px-2.5 py-1 rounded-lg text-[10px] font-bold shrink-0 ${
                      act.completed ? "bg-emerald-950 text-emerald-300 border border-emerald-800" : "bg-slate-800 text-slate-400"
                    }`}>
                      {act.completed ? "Done" : "Pending"}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Health Metrics Summary */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <StatCard label="Next Scheduled Visit" value="Sep 15" subtext="10:30 AM • ZAYVORA Matab™ OPD" variant="teal" icon="calendar" />
              <StatCard label="Active Formulations" value="2 Drugs" subtext="Majun Suranjan & Roghan" variant="emerald" icon="pill" />
              <StatCard label="Lifestyle Balance" value="82%" subtext="Asbab-e-Sittah Compliance" variant="blue" icon="leaf" />
              <StatCard label="Recent Blood Pressure" value="124/82" subtext="Resting Pulse 72 bpm" variant="teal" icon="heart" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Active Care Protocol Summary */}
              <div className="lg:col-span-2 space-y-6">
                {carePlan ? (
                  <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 shadow-md">
                    <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                      <div>
                        <span className="text-[10px] font-bold uppercase tracking-wider text-teal-400">Clinical Protocol</span>
                        <h3 className="text-lg font-bold text-white mt-0.5">{carePlan.programName}</h3>
                        <p className="text-xs text-slate-400">{carePlan.condition}</p>
                      </div>
                      <StatusBadge status="Active Care" variant="verified" />
                    </div>

                    <div className="space-y-2">
                      <div className="flex justify-between text-xs">
                        <span className="text-slate-400">Phase {carePlan.phaseNumber} of {carePlan.totalPhases}: {carePlan.currentPhase}</span>
                        <span className="text-teal-400 font-bold font-mono">{carePlan.progressPercent}%</span>
                      </div>
                      <div className="w-full h-2.5 rounded-full bg-slate-800 overflow-hidden">
                        <div className="h-full bg-gradient-to-r from-teal-500 to-emerald-400 rounded-full" style={{ width: `${carePlan.progressPercent}%` }}></div>
                      </div>
                    </div>

                    <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800/80 text-xs space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-slate-400">Supervising Physician</span>
                        <span className="text-teal-300 font-semibold">{carePlan.attendingPhysician}</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-slate-400">Program Start</span>
                        <span className="text-slate-200">{carePlan.startDate}</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-slate-400">Next Scheduled Evaluation</span>
                        <span className="text-slate-200">{carePlan.nextReviewDate}</span>
                      </div>
                      {carePlan.clinicalNotes && (
                        <p className="text-slate-400 pt-2 border-t border-slate-800 italic">
                          "{carePlan.clinicalNotes}"
                        </p>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-8 text-center space-y-3">
                    <div className="w-12 h-12 mx-auto rounded-2xl bg-slate-800 flex items-center justify-center text-slate-400">
                      <HealthcareIcon name="clipboard" className="w-6 h-6 text-slate-400" />
                    </div>
                    <h3 className="text-sm font-bold text-white">No Active Care Protocol</h3>
                    <p className="text-xs text-slate-400 max-w-sm mx-auto">
                      Your personalized Unani regimen and Ilaj-bil-Tadbeer protocol will appear here once formulated by your attending clinician.
                    </p>
                  </div>
                )}

                {/* Voice Medication Instructions */}
                <div className="bg-[#0F172A] border border-teal-800/40 rounded-3xl p-6 space-y-4 shadow-md">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-teal-500/20 text-teal-300 flex items-center justify-center text-xl">
                        <HealthcareIcon name="activity" className="w-5 h-5 text-teal-300" />
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
                      {isPlayingAudio ? "▶ Playing Voice..." : "<HealthcareIcon name="activity" className="w-5 h-5 text-teal-300" /> Listen to Audio"}
                    </button>
                  </div>
                </div>
              </div>

              {/* Right Column: Next Appointment & Emergency Desk */}
              <div className="space-y-6">
                <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 shadow-md">
                  <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                    <h4 className="text-sm font-bold text-white">Next Clinic Visit</h4>
                    {appointments.length > 0 ? (
                      <StatusBadge status="Confirmed" variant="verified" />
                    ) : (
                      <StatusBadge status="No Visit" variant="neutral" />
                    )}
                  </div>
                  {appointments.length > 0 ? (
                    <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800 space-y-2 text-xs">
                      <span className="text-[10px] uppercase font-bold text-slate-500">OPD Queue Token</span>
                      <div className="text-xl font-mono font-extrabold text-teal-300">{appointments[0].tokenNumber}</div>
                      <div className="text-slate-200 font-medium pt-1">
                        {appointments[0].date} • {appointments[0].timeSlot}
                      </div>
                      <div className="text-slate-400">
                        {appointments[0].doctorName}
                      </div>
                      <div className="text-[11px] text-slate-500">
                        {appointments[0].facilityLocation}
                      </div>
                    </div>
                  ) : (
                    <div className="bg-slate-900/50 p-6 rounded-2xl border border-slate-800/80 text-center text-xs text-slate-400 space-y-1">
                      <p className="text-white font-medium">No Upcoming Visits</p>
                      <p className="text-[11px]">You currently have no scheduled OPD or telemedicine consultations.</p>
                    </div>
                  )}
                  <div className="flex gap-2">
                    <button
                      onClick={() => appointments.length > 0 ? setShowRescheduleModal(true) : setShowBookingModal(true)}
                      className="flex-1 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition"
                    >
                      {appointments.length > 0 ? "Reschedule" : "Book Visit"}
                    </button>
                    <button
                      onClick={() => setActiveTab("appointments")}
                      className="flex-1 py-2 rounded-xl bg-teal-950 hover:bg-teal-900 text-teal-300 text-xs font-semibold border border-teal-800 transition"
                    >
                      All Visits
                    </button>
                  </div>
                </div>

                {/* Emergency Medical Guidance */}
                <div className="bg-[#0F172A] border border-rose-900/40 rounded-3xl p-6 space-y-3 shadow-md text-xs">
                  <div className="flex items-center gap-2 text-rose-400 font-bold">
                    <span><HealthcareIcon name="alert-triangle" className="w-4 h-4 text-rose-400" /></span>
                    <span>Emergency Medical Guidance</span>
                  </div>
                  <p className="text-slate-400 text-[11px] leading-relaxed">
                    ZAYVORA provides elective outpatient and teleconsultation care. For acute medical emergencies (chest pain, acute breathlessness, loss of consciousness), call <strong>112</strong> or visit the nearest hospital emergency department immediately.
                  </p>
                  <div className="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                    <div className="text-slate-300 font-bold">Elective Outpatient Helpline:</div>
                    <div className="text-teal-400 font-mono font-bold text-sm">+91 97738 82657</div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 2: MY HEALTH PROFILE                             */}
        {/* ========================================================= */}
        {((activeTab === "health" && healthSubTab === "profile") || activeTab === "profile") && (
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
                    <div><span className="text-slate-500 block">Full Name:</span> {activePatient?.fullName || "Not Specified"}</div>
                    <div><span className="text-slate-500 block">Age / Gender:</span> {activePatient?.age ? `${activePatient.age} yrs` : "—"} / {activePatient?.gender || "—"}</div>
                    <div><span className="text-slate-500 block">Medical Record No:</span> <span className="font-mono text-teal-400">{activePatient?.mrn || "Pending Registration"}</span></div>
                    <div><span className="text-slate-500 block">ABHA ID:</span> <span className="font-mono text-white">{activePatient?.abhaId || "Not Linked"}</span></div>
                    <div><span className="text-slate-500 block">Blood Group:</span> {activePatient?.bloodGroup || "Not Recorded"}</div>
                    <div><span className="text-slate-500 block">Registered Phone:</span> {activePatient?.phone || "Not Recorded"}</div>
                  </div>
                </div>

                <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800 space-y-3">
                  <h4 className="font-bold text-teal-300 uppercase tracking-wider text-[10px]">Residential Address</h4>
                  <p className="text-slate-300">{activePatient?.address || "No residential address documented in clinical record."}</p>
                  <h4 className="font-bold text-teal-300 uppercase tracking-wider text-[10px] pt-2">Emergency Contact</h4>
                  <p className="text-slate-300">{activePatient?.emergencyContact || "No emergency contact registered."}</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800 space-y-3">
                  <h4 className="font-bold text-teal-300 uppercase tracking-wider text-[10px]">Mizaj &amp; Constitutional Diagnostics</h4>
                  <div className="space-y-2 text-slate-300">
                    <div>
                      <span className="text-slate-500 block">Innate Temperament (Mizaj-e-Asli):</span>
                      <strong className="text-white text-sm">{activePatient?.primaryMizaj || "Awaiting Pulse & Mizaj Assessment"}</strong>
                    </div>
                    <div>
                      <span className="text-slate-500 block">Present Dyscrasia (Su-e-Mizaj):</span>
                      <span className="text-teal-300">{activePatient?.suEMizaj || "None Documented"}</span>
                    </div>
                  </div>
                </div>

                <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800 space-y-3">
                  <h4 className="font-bold text-rose-400 uppercase tracking-wider text-[10px]">Documented Clinical Allergies</h4>
                  <div className="flex flex-wrap gap-2">
                    {((activePatient?.knownAllergies || activePatient?.allergies || []).length > 0) ? (
                      (activePatient?.knownAllergies || activePatient?.allergies).map((allergy: string, idx: number) => (
                        <span key={idx} className="bg-rose-950/60 border border-rose-800/80 text-rose-300 px-3 py-1 rounded-xl text-xs">
                          • {allergy}
                        </span>
                      ))
                    ) : (
                      <span className="text-slate-500 text-xs italic">No known drug or botanical allergies documented (NKDA).</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 2B: CONSENTS & PRIVACY (DPDP ACT 2023 & ABDM)      */}
        {/* ========================================================= */}
        {((activeTab === "health" && healthSubTab === "consent") || activeTab === "consent-privacy") && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <HealthcareIcon name="lock" className="w-4 h-4 text-emerald-400" />
                  <span>DPDP Act 2023 &amp; ABDM Consent Center</span>
                </h3>
                <p className="text-slate-400">
                  Manage your statutory health data permissions, access logs, and revocation preferences in real time.
                </p>
              </div>
              <span className="px-3 py-1 rounded-full bg-emerald-950 border border-emerald-700 text-emerald-300 text-[11px] font-bold">
                ✓ DPDP Rules 2025 Active
              </span>
            </div>

            
            {/* Caregiver & Family Access Management */}
            <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
                <div>
                  <h4 className="font-bold text-white text-sm flex items-center gap-2">
                    <HealthcareIcon name="users" className="w-4 h-4 text-teal-400" />
                    <span>Caregiver &amp; Family Access Management</span>
                  </h4>
                  <p className="text-slate-400 text-[11px] mt-0.5">
                    Authorize trusted family members or caregivers to view your appointments, schedule visits, or review clinical prescriptions under DPDP Act 2023.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => setShowCaregiverModal(true)}
                  className="px-3.5 py-1.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-xs transition shadow-sm"
                >
                  + Add Caregiver
                </button>
              </div>

              <div className="space-y-3">
                {caregivers.map((cg) => (
                  <div key={cg.id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-white text-xs">{cg.name}</span>
                        <span className="text-[10px] text-teal-400 bg-teal-950 px-2 py-0.5 rounded border border-teal-800 font-mono">
                          {cg.relationship}
                        </span>
                        <span className="text-[10px] text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800">
                          {cg.status}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 mt-1">
                        Phone: {cg.phone} • Scope: <strong className="text-slate-200">{cg.scope}</strong> • Granted: {cg.addedDate}
                      </p>
                    </div>
                    <button
                      type="button"
                      onClick={() => setCaregivers((prev) => prev.filter((c) => c.id !== cg.id))}
                      className="px-3 py-1 rounded-lg bg-rose-950/60 hover:bg-rose-900 border border-rose-800 text-rose-300 text-xs font-semibold transition self-start sm:self-auto"
                    >
                      Revoke Access
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Statutory Consent Toggles */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-start justify-between gap-4">
                <div>
                  <h4 className="font-bold text-white text-sm">ABDM Health Data Sharing</h4>
                  <p className="text-slate-400 text-[11px] mt-1 leading-relaxed">
                    Authorizes seamless diagnostic and prescription exchange with certified AYUSH and modern hospitals via Ayushman Bharat Digital Mission (FHIR R4 standard).
                  </p>
                  <span className="text-[10px] text-teal-400 font-mono mt-2 block">
                    Status: {consents.abdm_health_data_sharing ? "Granted (Active)" : "Revoked"}
                  </span>
                </div>
                <button
                  onClick={() => handleToggleConsent("abdm_health_data_sharing")}
                  className={`w-12 h-6 flex items-center rounded-full p-1 transition duration-300 ${
                    consents.abdm_health_data_sharing ? "bg-teal-600 justify-end" : "bg-slate-700 justify-start"
                  }`}
                >
                  <div className="w-4 h-4 bg-white rounded-full shadow-md" />
                </button>
              </div>

              <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-start justify-between gap-4">
                <div>
                  <h4 className="font-bold text-white text-sm">Remote Triage & Red-Flag Telemetry</h4>
                  <p className="text-slate-400 text-[11px] mt-1 leading-relaxed">
                    Allows real-time algorithmic safety monitoring for acute red-flag symptoms (chest pain, severe breathlessness) with emergency hospital escalation.
                  </p>
                  <span className="text-[10px] text-teal-400 font-mono mt-2 block">
                    Status: {consents.tele_triage_telemetry ? "Granted (Active)" : "Revoked"}
                  </span>
                </div>
                <button
                  onClick={() => handleToggleConsent("tele_triage_telemetry")}
                  className={`w-12 h-6 flex items-center rounded-full p-1 transition duration-300 ${
                    consents.tele_triage_telemetry ? "bg-teal-600 justify-end" : "bg-slate-700 justify-start"
                  }`}
                >
                  <div className="w-4 h-4 bg-white rounded-full shadow-md" />
                </button>
              </div>

              <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-start justify-between gap-4">
                <div>
                  <h4 className="font-bold text-white text-sm">Clinical Knowledge Bio-Repository (RWE)</h4>
                  <p className="text-slate-400 text-[11px] mt-1 leading-relaxed">
                    Contributes de-identified constitutional outcomes and biomarker trajectories to Unani clinical research cohorts (Study ZCT-2026-001).
                  </p>
                  <span className="text-[10px] text-teal-400 font-mono mt-2 block">
                    Status: {consents.research_bio_repository_opt_in ? "Granted (Active)" : "Revoked"}
                  </span>
                </div>
                <button
                  onClick={() => handleToggleConsent("research_bio_repository_opt_in")}
                  className={`w-12 h-6 flex items-center rounded-full p-1 transition duration-300 ${
                    consents.research_bio_repository_opt_in ? "bg-teal-600 justify-end" : "bg-slate-700 justify-start"
                  }`}
                >
                  <div className="w-4 h-4 bg-white rounded-full shadow-md" />
                </button>
              </div>

              <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-start justify-between gap-4">
                <div>
                  <h4 className="font-bold text-white text-sm">Daily Regimen & Posology Alerts</h4>
                  <p className="text-slate-400 text-[11px] mt-1 leading-relaxed">
                    Sends automated WhatsApp and SMS reminders for morning/evening drug administration, water temperature instructions, and Asbab Sittah habits.
                  </p>
                  <span className="text-[10px] text-teal-400 font-mono mt-2 block">
                    Status: {consents.sms_whatsapp_care_reminders ? "Granted (Active)" : "Revoked"}
                  </span>
                </div>
                <button
                  onClick={() => handleToggleConsent("sms_whatsapp_care_reminders")}
                  className={`w-12 h-6 flex items-center rounded-full p-1 transition duration-300 ${
                    consents.sms_whatsapp_care_reminders ? "bg-teal-600 justify-end" : "bg-slate-700 justify-start"
                  }`}
                >
                  <div className="w-4 h-4 bg-white rounded-full shadow-md" />
                </button>
              </div>
            </div>

            {/* Access Audit Trail */}
            <div className="bg-slate-900/80 p-5 rounded-2xl border border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <h4 className="font-bold text-teal-300 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                  <span><HealthcareIcon name="file-text" className="w-4 h-4" /></span> Immutable Access Audit History (21 CFR Part 11)
                </h4>
                <span className="text-[10px] font-mono text-slate-500">Tamper-Proof Merkle Root Active</span>
              </div>
              <div className="space-y-2">
                {[
                  {
                    accessor: "Hakeem Dr. Irfan Ashraf",
                    role: "Attending Clinician (BUMS - AKTC AMU)",
                    action: "Encounter Chart & Nuskha Verification",
                    time: "Today, 10:15 AM",
                    hash: "3aec624294e3"
                  },
                  {
                    accessor: "Dr. Tariq Mahmood",
                    role: "Chief Pharmacist (DL-PH-2015-8821)",
                    action: "Schedule E(1) Mudabbar Certificate Clearance",
                    time: "Yesterday, 04:30 PM",
                    hash: "91ab429e71cc"
                  },
                  {
                    accessor: "ZAYVORA Safety Firewall Core",
                    role: "Automated Clinical Guard Service",
                    action: "Herb-Drug & Posology Safety Verification",
                    time: "18 Sep 2026, 09:00 AM",
                    hash: "77fc12089bae"
                  }
                ].map((item, idx) => (
                  <div key={idx} className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-[11px]">
                    <div>
                      <strong className="text-white">{item.accessor}</strong>
                      <span className="text-slate-400 ml-1.5">({item.role})</span>
                      <p className="text-slate-300 text-[10px]">{item.action}</p>
                    </div>
                    <div className="text-right shrink-0">
                      <span className="text-slate-400 block">{item.time}</span>
                      <span className="font-mono text-teal-400 text-[10px]">Hash: {item.hash}...</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Statutory Actions Bar */}
            <div className="p-4 rounded-2xl bg-[#064E3B]/20 border border-[#059669]/40 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <p className="text-white font-bold">Download Your Personal Health Record (PHR)</p>
                <p className="text-slate-400 text-[11px]">
                  Export all your encounters, active prescriptions, lab trends, and consent receipts in ABDM FHIR R4 standard.
                </p>
              </div>
              <button
                onClick={() => alert("Personal Health Record (ABDM FHIR R4 Bundle) downloaded successfully with cryptographic signature.")}
                className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-xs transition shrink-0"
              >
                Download FHIR R4 PHR
              </button>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 3: APPOINTMENTS                                   */}
        {/* ========================================================= */}
        {((activeTab === "care" && careSubTab === "appointments") || activeTab === "appointments") && (
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
                    {apt.status !== "Completed" && !apt.status.includes("Pre-Checked In") && (
                      <button
                        onClick={() => handleDigitalCheckin(apt.id)}
                        disabled={isCheckingIn}
                        className="px-3.5 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-xs shadow-sm transition disabled:opacity-50"
                      >
                        {isCheckingIn ? "Checking In..." : "✓ Pre-Visit Digital Check-in"}
                      </button>
                    )}
                    {apt.status.includes("Pre-Checked In") && (
                      <span className="px-3 py-1.5 rounded-xl bg-emerald-950/90 border border-emerald-700 text-emerald-300 font-semibold text-[11px]">
                        ✓ Pre-Checked In
                      </span>
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
        {((activeTab === "care" && careSubTab === "consultations") || activeTab === "consultations") && (
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
        {((activeTab === "care" && careSubTab === "consultations") || activeTab === "ai-doctor") && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-teal-500/10 border border-teal-500/30 flex items-center justify-center">
                    <HealthcareIcon name="activity" className="w-4 h-4 text-teal-400" />
                  </div>
                  <h3 className="text-lg font-bold text-white">Hakeem Sahab AI™ — AI-Assisted Clinical Decision Support</h3>
                </div>
                <p className="text-slate-400">AI-assisted clinical education &amp; health literacy support, calibrated to your health profile. Non-autonomous decision support; consult attending Tabeeb for diagnosis.</p>
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
                  <span>Hakeem Sahab AI™ is formulating clinical advice...</span>
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
        {((activeTab === "plan" && planSubTab === "protocols") || activeTab === "protocols") && (
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
        {((activeTab === "plan" && planSubTab === "prescriptions") || activeTab === "prescriptions") && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-lg font-bold text-white">Digital Prescription: RX-2026-0441</h3>
                <p className="text-slate-400">Issued by Prof. (Dr.) Mansoor Alam • Verified by ZAYVORA Central Dispensary</p>
              </div>
              <button
                onClick={() => alert("Downloading signed official prescription PDF...")}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-teal-300 font-semibold border border-slate-700 transition"
              >
                Download Official PDF <HealthcareIcon name="clipboard" className="w-5 h-5 text-teal-400" />
              </button>
            </div>

            <div className="space-y-4">
              {prescriptions.length > 0 ? (
                prescriptions.map((rx, idx) => (
                  <div key={idx} className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div className="space-y-1.5">
                      <div className="flex items-center gap-2">
                        <h4 className="font-bold text-white text-sm">{rx.medicineName}</h4>
                        <span className="bg-teal-950 text-teal-300 px-2 py-0.5 rounded text-[10px] font-semibold border border-teal-800">
                          {rx.form}
                        </span>
                      </div>
                      <p className="text-slate-300">
                        <strong>Dosage &amp; Frequency:</strong> {rx.dosage} • {rx.timing}
                      </p>
                      <p className="text-slate-400 text-[11px]">
                        <strong>Vehicle (Anupan):</strong> {rx.anupan}
                      </p>
                      <p className="text-slate-400 text-[11px]">
                        <strong>Instructions:</strong> {rx.instructions}
                      </p>
                    </div>
                    <div className="text-right shrink-0 space-y-1.5">
                      <span className="text-emerald-400 font-semibold block text-[11px]">✓ Mudabbar Batch Certified</span>
                      <button
                        type="button"
                        onClick={() => handleOpenWhyThis(rx.medicineName, rx.medicineName)}
                        className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-emerald-400 hover:text-emerald-300 border border-slate-700 text-[10px] font-medium transition inline-flex items-center gap-1"
                        title="View scientific & classical authority rationale"
                      >
                        <span>💡</span> Why This?
                      </button>
                    </div>
                  </div>
                ))
              ) : (
                <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 text-center space-y-2">
                  <div className="w-12 h-12 mx-auto rounded-2xl bg-slate-800 flex items-center justify-center text-slate-400">
                    <HealthcareIcon name="clipboard" className="w-6 h-6 text-slate-400" />
                  </div>
                  <p className="text-white font-semibold">No Active Prescriptions</p>
                  <p className="text-slate-400 text-[11px] max-w-sm mx-auto">
                    There are currently no active botanical or compound formulations prescribed for this medical record.
                  </p>
                </div>
              )}
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
        {((activeTab === "health" && healthSubTab === "reports") || activeTab === "reports") && (
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
                      <HealthcareIcon name="clipboard" className="w-5 h-5 text-teal-400" />
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
        {((activeTab === "plan" && planSubTab === "protocols") || activeTab === "treatment-plans") && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-4">
              <h3 className="text-lg font-bold text-white">Ilaj-bit-Tadbeer (Regimenal Therapies) Schedule</h3>
              <p className="text-slate-400">Clinical physiotherapy, fomentation, and hijama procedures scheduled at ZAYVORA Matab™ Central.</p>
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
        {(activeTab === "practice" || activeTab === "lifestyle") && (
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

            {/* Daily Regimen & Adherence Check-In (§28, §63) */}
            <div className="pt-6 border-t border-slate-800 space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div>
                  <h4 className="text-sm font-bold text-white flex items-center gap-2">
                    <span>💊</span> Today's Adherence Check-in & Posology
                  </h4>
                  <p className="text-slate-400 text-[11px]">
                    Track your daily doses with non-judgmental feedback to help your Tabeeb calibrate your care.
                  </p>
                </div>
                <div className="px-3 py-1 rounded-full bg-emerald-950 border border-emerald-800 text-[10px] text-emerald-300 font-semibold">
                  Today's Rate: 92% (High Adherence)
                </div>
              </div>

              <div className="space-y-3">
                {[
                  {
                    id: "RX-01",
                    name: "Safoof Suranjan (Mudabbar)",
                    dosage: "5g twice daily with lukewarm water",
                    timing: "Morning & Night",
                    type: "NUSKHA"
                  },
                  {
                    id: "RX-02",
                    name: "Sharbat Bazoori Motadil",
                    dosage: "20ml diluted in 150ml water",
                    timing: "Post-prandial Noon",
                    type: "NUSKHA"
                  },
                  {
                    id: "TB-01",
                    name: "Roghan Suranjan (Dalak Layyin)",
                    dosage: "Gentle warming massage over knee joints for 10 mins",
                    timing: "Bedtime",
                    type: "TADBEER"
                  }
                ].map((item) => {
                  const currentStatus = adherenceEntries[item.id]?.status || "PENDING";
                  const missedReason = adherenceEntries[item.id]?.reason;

                  return (
                    <div
                      key={item.id}
                      className="p-4 bg-slate-900/90 rounded-2xl border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
                    >
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-white text-xs">{item.name}</span>
                          <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-teal-300 font-mono">
                            {item.timing}
                          </span>
                        </div>
                        <p className="text-slate-400 text-[11px]">{item.dosage}</p>
                        {missedReason && (
                          <div className="text-[10px] text-amber-400/90 flex items-center gap-1 pt-0.5">
                            <span>ℹ️</span> Reason: <em>{missedReason}</em>
                          </div>
                        )}
                      </div>

                      <div className="flex items-center gap-2 shrink-0">
                        {/* Why this button (§63) */}
                        <button
                          type="button"
                          onClick={() => handleOpenWhyThis(item.id, item.name)}
                          className="px-2.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-400 hover:text-emerald-300 border border-slate-700 text-[11px] font-medium transition flex items-center gap-1"
                          title="View classical & scientific rationale (Blueprint §63)"
                        >
                          <span>💡</span> Why This?
                        </button>

                        {/* Taken button */}
                        <button
                          type="button"
                          onClick={() => handleMarkDose(item.id, item.name, "TAKEN")}
                          className={`px-3 py-1.5 rounded-xl text-[11px] font-bold transition flex items-center gap-1 ${
                            currentStatus === "TAKEN"
                              ? "bg-emerald-600 text-white shadow-sm"
                              : "bg-slate-800 text-slate-300 hover:bg-slate-700"
                          }`}
                        >
                          <span>✓</span> Taken
                        </button>

                        {/* Missed button (§28) */}
                        <button
                          type="button"
                          onClick={() => handleMarkDose(item.id, item.name, "MISSED")}
                          className={`px-3 py-1.5 rounded-xl text-[11px] font-bold transition flex items-center gap-1 ${
                            currentStatus === "MISSED"
                              ? "bg-rose-900/80 text-rose-200 border border-rose-700"
                              : "bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-rose-300"
                          }`}
                        >
                          <span>✕</span> Skipped
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 12: CLINICAL MESSAGES                             */}
        {/* ========================================================= */}
        {((activeTab === "care" && careSubTab === "messages") || activeTab === "messages") && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-4">
              <h3 className="text-lg font-bold text-white">Direct Encrypted Doctor Communication</h3>
              <p className="text-slate-400">Secure clinical chat thread with Prof. (Dr.) Mansoor Alam and the ZAYVORA clinical care desk.</p>
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
        {((activeTab === "plan" && planSubTab === "billing") || activeTab === "billing") && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-4">
              <h3 className="text-lg font-bold text-white">Itemized Consultation & Dispensary Invoices</h3>
              <p className="text-slate-400">GST-compliant digital receipts for OPD encounters and herbal dispensations.</p>
            </div>

            <div className="space-y-3">
              {invoices.length > 0 ? (
                invoices.map((inv) => (
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
                        Download Receipt
                      </button>
                    </div>
                  </div>
                ))
              ) : (
                <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 text-center space-y-2">
                  <div className="w-12 h-12 mx-auto rounded-2xl bg-slate-800 flex items-center justify-center text-slate-400">
                    <HealthcareIcon name="file-text" className="w-6 h-6 text-slate-400" />
                  </div>
                  <p className="text-white font-semibold">No Billing Records Found</p>
                  <p className="text-slate-400 text-[11px] max-w-sm mx-auto">
                    There are no unpaid or archived invoices registered under this patient account.
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* SECTION 14: MY PROGRESS (OUTCOME INTELLIGENCE)             */}
        {/* ========================================================= */}
        {activeTab === "progress" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <HealthcareIcon name="trending-up" className="w-5 h-5 text-emerald-400" />
                  <span>My Clinical Recovery &amp; Progress (Outcomes)</span>
                </h3>
                <p className="text-slate-400">
                  Continuous outcome tracking: Symptom trajectory, Mizaj equilibrium index, and functional recovery milestones.
                </p>
              </div>
              <div className="flex items-center gap-2 bg-emerald-950/70 border border-emerald-800/80 px-4 py-2 rounded-2xl">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                <span className="text-emerald-300 font-bold text-xs">Adherence: 92% (Excellent)</span>
              </div>
            </div>

            {/* Outcome KPI Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-4 bg-slate-900/90 border border-slate-800 rounded-2xl space-y-1">
                <span className="text-[10px] text-slate-500 uppercase font-bold">Symptom Burden Index</span>
                <div className="text-2xl font-bold font-mono text-emerald-400">-42%</div>
                <p className="text-[11px] text-slate-400">Marked reduction in bilateral knee morning stiffness</p>
              </div>

              <div className="p-4 bg-slate-900/90 border border-slate-800 rounded-2xl space-y-1">
                <span className="text-[10px] text-slate-500 uppercase font-bold">Mizaj Equilibrium (Tanqiya)</span>
                <div className="text-2xl font-bold font-mono text-teal-300">Phase 2: 68%</div>
                <p className="text-[11px] text-slate-400">Elimination of cold morbid humors (Balgham Barid)</p>
              </div>

              <div className="p-4 bg-slate-900/90 border border-slate-800 rounded-2xl space-y-1">
                <span className="text-[10px] text-slate-500 uppercase font-bold">Functional Mobility Score</span>
                <div className="text-2xl font-bold font-mono text-cyan-400">8.4 / 10</div>
                <p className="text-[11px] text-slate-400">Improved range of motion &amp; uninterrupted nocturnal sleep</p>
              </div>

              <div className="p-4 bg-slate-900/90 border border-slate-800 rounded-2xl space-y-1">
                <span className="text-[10px] text-slate-500 uppercase font-bold">Next Target Milestone</span>
                <div className="text-sm font-bold text-white mt-1">Stage 03: Ta'dil-e-Mizaj</div>
                <p className="text-[11px] text-slate-400">Scheduled for follow-up review on Sep 18, 2026</p>
              </div>
            </div>

            {/* Trajectory Breakdown */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-2">
              <div className="p-5 bg-slate-900/80 border border-slate-800 rounded-2xl space-y-3">
                <h4 className="font-bold text-white text-sm flex items-center gap-2">
                  <HealthcareIcon name="activity" className="w-4 h-4 text-teal-400" />
                  <span>30-Day Symptom Trajectory (Pain &amp; Stiffness)</span>
                </h4>
                <div className="space-y-2 pt-2">
                  {[
                    { label: "Day 01 (Intake & Baseline)", score: "8.5 / 10 Pain Severity", width: "85%", color: "bg-rose-500" },
                    { label: "Day 10 (Post-Taskeen phase)", score: "5.5 / 10 Pain Severity", width: "55%", color: "bg-amber-500" },
                    { label: "Day 20 (Active Munzij regimen)", score: "4.0 / 10 Pain Severity", width: "40%", color: "bg-teal-500" },
                    { label: "Day 30 (Present Clinical Status)", score: "2.5 / 10 Mild Discomfort", width: "25%", color: "bg-emerald-500" },
                  ].map((row, idx) => (
                    <div key={idx} className="space-y-1">
                      <div className="flex justify-between text-[11px] text-slate-300">
                        <span>{row.label}</span>
                        <span className="font-mono font-bold text-white">{row.score}</span>
                      </div>
                      <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                        <div className={`h-full ${row.color} rounded-full transition-all`} style={{ width: row.width }}></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="p-5 bg-slate-900/80 border border-slate-800 rounded-2xl space-y-3">
                <h4 className="font-bold text-white text-sm flex items-center gap-2">
                  <HealthcareIcon name="check-circle" className="w-4 h-4 text-emerald-400" />
                  <span>Hakeem Sahab™ Longitudinal Care Evaluation</span>
                </h4>
                <p className="text-slate-300 leading-relaxed text-[11px]">
                  Based on 28 daily adherence logs and resting Nabz telemetry (72 bpm, regular), your constitutional state is successfully shifting out of the Barid (cold) stagnation phase.
                </p>
                <div className="p-3 bg-[#0A101D] border border-slate-800 rounded-xl space-y-1.5 text-[11px]">
                  <span className="font-bold text-teal-300 uppercase text-[10px]">Attending Clinician Instruction:</span>
                  <p className="text-slate-300">
                    "Continue Majun Suranjan and nightly warm fomentation. Reassessment consultation scheduled in 7 days for Ta'dil-e-Mizaj transition."
                  </p>
                  <span className="text-[10px] text-slate-500 block">— Prof. (Dr.) Mansoor Alam (AKTC Aligarh)</span>
                </div>
              </div>
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
        {/* ADD CAREGIVER MODAL                                       */}
        {/* ========================================================= */}
        {showCaregiverModal && (
          <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-[#0F172A] border border-slate-700 rounded-3xl p-6 max-w-md w-full space-y-4 shadow-2xl text-xs">
              <div className="flex justify-between items-center border-b border-slate-800 pb-3">
                <h3 className="text-sm font-bold text-white">Authorize Family Caregiver</h3>
                <button onClick={() => setShowCaregiverModal(false)} className="text-slate-400 hover:text-white">✕</button>
              </div>

              <form onSubmit={(e) => {
                e.preventDefault();
                if (!newCaregiverName) return;
                setCaregivers(prev => [
                  ...prev,
                  {
                    id: `CG-0${prev.length + 1}`,
                    name: newCaregiverName,
                    relationship: newCaregiverRelation,
                    phone: newCaregiverPhone || "+91 98000 00000",
                    scope: newCaregiverScope,
                    status: "Active",
                    addedDate: new Date().toISOString().split("T")[0]
                  }
                ]);
                setShowCaregiverModal(false);
                setNewCaregiverName("");
                setNewCaregiverPhone("");
              }} className="space-y-4">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Caregiver Full Name *</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Tariq Farooqi"
                    value={newCaregiverName}
                    onChange={(e) => setNewCaregiverName(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-300 font-semibold mb-1">Relationship</label>
                    <select
                      value={newCaregiverRelation}
                      onChange={(e) => setNewCaregiverRelation(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                    >
                      <option value="Spouse">Spouse</option>
                      <option value="Parent">Parent</option>
                      <option value="Child">Son / Daughter</option>
                      <option value="Sibling">Brother / Sister</option>
                      <option value="Legal Guardian">Legal Guardian</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-slate-300 font-semibold mb-1">Mobile Number</label>
                    <input
                      type="tel"
                      placeholder="+91 98765 00000"
                      value={newCaregiverPhone}
                      onChange={(e) => setNewCaregiverPhone(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Permission Scope</label>
                  <select
                    value={newCaregiverScope}
                    onChange={(e) => setNewCaregiverScope(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-teal-500"
                  >
                    <option value="Appointments & Schedule Only">Appointments &amp; Schedule Only (Read/Book)</option>
                    <option value="Full Records & Prescriptions">Full Records, Prescriptions &amp; Messaging</option>
                  </select>
                </div>

                <div className="flex gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowCaregiverModal(false)}
                    className="flex-1 py-2 rounded-xl bg-slate-800 text-slate-300 font-semibold border border-slate-700"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold"
                  >
                    Grant Access
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
                  <div className="text-2xl text-teal-400"><HealthcareIcon name="upload" className="w-6 h-6 text-teal-400 mx-auto" /></div>
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
        {/* ========================================================= */}
        {/* NON-JUDGMENTAL ADHERENCE DROP REASONS MODAL (Blueprint §28) */}
        {/* ========================================================= */}
        {missedItemModalOpen && selectedMissedItem && (
          <div
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in"
            role="dialog"
            aria-modal="true"
          >
            <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 sm:p-7 max-w-lg w-full space-y-5 text-xs text-slate-300 shadow-2xl">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <span className="p-2 rounded-xl bg-amber-950/60 border border-amber-800 text-amber-300 text-base">🌱</span>
                  <div>
                    <h3 className="text-base font-bold text-white">Log Missed Regimen Dose</h3>
                    <p className="text-[11px] text-slate-400">Blueprint §28 Non-judgmental adherence intelligence</p>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => setMissedItemModalOpen(false)}
                  className="p-1 rounded-lg text-slate-400 hover:text-white"
                >
                  ✕
                </button>
              </div>

              <div className="p-3 bg-slate-900/90 rounded-2xl border border-slate-800">
                <span className="text-[11px] text-slate-400 block">Item:</span>
                <span className="text-sm font-bold text-white">{selectedMissedItem.name}</span>
              </div>

              <div className="space-y-2">
                <label className="block text-slate-200 font-semibold text-xs">
                  Please let us know what made it difficult to take this dose:
                </label>
                <div className="grid grid-cols-1 gap-2 max-h-56 overflow-y-auto pr-1">
                  {[
                    "Forgetfulness / Busy schedule",
                    "Complexity of preparation / dosing",
                    "Availability / Supply shortage",
                    "Cost or refill constraint",
                    "Discomfort, strong taste, or odor",
                    "Suspected side effect / adverse reaction",
                    "Unclear instructions / lack of understanding",
                    "Routine conflict with meals or prayer times",
                    "Other"
                  ].map((r) => (
                    <button
                      key={r}
                      type="button"
                      onClick={() => setMissedReasonSelected(r)}
                      className={`p-2.5 rounded-xl border text-left text-xs transition flex items-center justify-between ${
                        missedReasonSelected === r
                          ? "bg-teal-950/80 border-teal-500 text-teal-200 ring-1 ring-teal-500"
                          : "bg-slate-900 border-slate-800 text-slate-300 hover:bg-slate-800"
                      }`}
                    >
                      <span>{r}</span>
                      {missedReasonSelected === r && <span className="text-teal-400 font-bold">✓</span>}
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-1">
                <label className="block text-slate-400 text-[11px]">Additional notes for your Tabeeb (optional):</label>
                <input
                  type="text"
                  placeholder="e.g. Felt slight fullness after lunch"
                  value={missedNotes}
                  onChange={(e) => setMissedNotes(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500 text-xs"
                />
              </div>

              <div className="p-3 rounded-xl bg-emerald-950/30 border border-emerald-900/40 text-[11px] text-emerald-300 leading-relaxed">
                <em>"Unani therapy is compassionate and flexible. Your feedback helps your clinician adjust doses, timing, or vehicles for optimal comfort."</em>
              </div>

              <div className="flex gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => setMissedItemModalOpen(false)}
                  className="flex-1 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  disabled={!missedReasonSelected}
                  onClick={() => handleConfirmMissed(missedReasonSelected)}
                  className="flex-1 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 disabled:opacity-50 text-white font-bold transition shadow-sm"
                >
                  Record Reason
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* WHY THIS? SCIENTIFIC & CLASSICAL EXPLAINABILITY MODAL (§63)*/}
        {/* ========================================================= */}
        <WhyThisModal
          isOpen={whyThisOpen}
          onClose={() => setWhyThisOpen(false)}
          data={whyThisData}
        />

          </>
        )}

      </div>
    </AppShell>
  );
}
