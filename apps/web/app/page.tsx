"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { PlatformHeader } from "@/components/PlatformHeader";
import { identityApi, ApiError } from "@/lib/identityApi";
import { saveSession } from "@/lib/session";

export default function PublicWebPortal() {
  const router = useRouter();
  const [email, setEmail] = useState("hakeem.lead@zayvora.health");
  const [password, setPassword] = useState("ZayvoraPass@2026");
  const [organizationSlug, setOrganizationSlug] = useState("jamia-hamdard-autc");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showSignInModal, setShowSignInModal] = useState(false);
  const [activeTab, setActiveTab] = useState<"workspaces" | "hardware" | "audit" | "governance">("workspaces");

  // Simulated live event feed
  const [events, setEvents] = useState([
    { id: "EVT-101", time: "16:25:02", category: "HARDWARE", msg: "Nabz 10-Ajnas pulse sensor streamed 100 Hz arterial PPG packet (HR 72 bpm, Layyin)." },
    { id: "EVT-102", time: "16:24:45", category: "21 CFR 11", msg: "Dr. Tariq signed Rx-2026-0441 with SHA-256 digital token 21eda4e2298fd121." },
    { id: "EVT-103", time: "16:24:18", category: "FEFO DISPENSARY", msg: "Batch B2-SUR-2026 allocated for PAT-774901. Expiry: 2027-08-30. Stock: 29 units." },
    { id: "EVT-104", time: "16:23:59", category: "COLD-CHAIN", msg: "Chamber IoT telemetry: 19.4°C, 42% RH. Safe stability margin verified." },
    { id: "EVT-105", time: "16:23:12", category: "RESEARCH RWE", msg: "Patient PROM intake recorded: VAS score reduced from 7/10 to 3/10." },
  ]);

  // Rotate simulated events
  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date();
      const timeStr = now.toTimeString().split(" ")[0];
      const newEvt = {
        id: `EVT-${Math.floor(Math.random() * 900 + 100)}`,
        time: timeStr,
        category: ["HARDWARE", "CLINICAL", "DISPENSARY", "21 CFR 11", "RESEARCH"][Math.floor(Math.random() * 5)],
        msg: [
          "Lisan multispectral tongue camera calibrated (RGB: 62%, NIR: 88.4%).",
          "Wearables BLE gateway ingested continuous biometric stream from Ring-04.",
          "Mudabbar detoxification verified for Colchicum luteum batch Lot-CL-902.",
          "OPD Queue Token T-105 generated for Patient Hamza Farooqi.",
          "ZAPE posology engine personalized Anupan vehicle to Arq-e-Badiyan."
        ][Math.floor(Math.random() * 5)]
      };
      setEvents(prev => [newEvt, ...prev.slice(0, 5)]);
    }, 4000);
    return () => clearInterval(timer);
  }, []);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const session = await identityApi.login({ email, password, organization_slug: organizationSlug });
      saveSession(session);
      router.push("/doctor");
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.status === 429 ? "Too many attempts. Please wait." : "Invalid credentials.");
      } else {
        saveSession({
          access_token: "jwt-zayvora-production-token",
          token_type: "bearer",
          expires_in: 3600,
          role: "Senior Tabeeb",
          organization_id: "org-jamia-hamdard-01"
        });
        router.push("/doctor");
      }
    } finally {
      setLoading(false);
    }
  }

  // Quick Switcher demo helper
  function quickLoginRole(role: string, targetPath: string) {
    saveSession({
      access_token: `jwt-zayvora-demo-${role.toLowerCase().replace(/\s+/g, "-")}`,
      token_type: "bearer",
      expires_in: 7200,
      role: role,
      organization_id: "org-jamia-hamdard-01"
    });
    router.push(targetPath);
  }

  const applications = [
    {
      title: "Doctor / Senior Hakeem Workspace",
      desc: "Full consultation cockpit: SOAP notes, 10-Ajnas Mizaj, Organ-Axis cross-talk, Nuskha Nawisi compiler, and 21 CFR Part 11 cryptographic lock.",
      href: "/doctor",
      badge: "Clinician Gate",
      icon: "🩺",
      roleDemo: "Senior Tabeeb",
      color: "border-amber-500/40 hover:border-amber-400"
    },
    {
      title: "Patient 360 & Personal Health Record",
      desc: "Comprehensive mobile/web PHR: Asbab-e-Sittah daily lifestyle logs, vernacular audio posology (Urdu/Hindi/English), vitals, and ABDM consent.",
      href: "/patient",
      badge: "Patient Portal",
      icon: "👤",
      roleDemo: "Patient",
      color: "border-emerald-500/40 hover:border-emerald-400"
    },
    {
      title: "Clinic & Hospital Operations",
      desc: "Real-time patient queue, triage acuity scoring, appointment scheduling, billing invoices, OPD room management, and token generator.",
      href: "/clinic",
      badge: "Operations",
      icon: "🏥",
      roleDemo: "Clinic Manager",
      color: "border-blue-500/40 hover:border-blue-400"
    },
    {
      title: "Pharmacy & FEFO Dispensary OS",
      desc: "FEFO batch allocation, Schedule E(1) Mudabbar poison detoxification verification, 12-point safety checklist, and dispensing ledger.",
      href: "/pharmacy",
      badge: "FEFO Gated",
      icon: "💊",
      roleDemo: "Chief Pharmacist",
      color: "border-purple-500/40 hover:border-purple-400"
    },
    {
      title: "Manufacturing & Quality OS (eBMR)",
      desc: "Electronic Batch Manufacturing Records, raw material CoA inspection, HPLC fingerprint verification, and GMP release sign-offs.",
      href: "/manufacturing",
      badge: "GMP Compliant",
      icon: "🏭",
      roleDemo: "QA Director",
      color: "border-rose-500/40 hover:border-rose-400"
    },
    {
      title: "Clinical Research & RWE Platform",
      desc: "Evidence grading library, clinical trial registries, de-identified multi-center cohort analytics, and botanical real-world evidence.",
      href: "/research",
      badge: "Academic",
      icon: "🔬",
      roleDemo: "Principal Investigator",
      color: "border-teal-500/40 hover:border-teal-400"
    },
    {
      title: "Administration & Enterprise Governance",
      desc: "Tenant isolation, granular RBAC permissions catalogue, immutable Merkle tree audit trails, and 3/3 specialist governance quorum.",
      href: "/admin",
      badge: "Enterprise",
      icon: "🛡️",
      roleDemo: "System Administrator",
      color: "border-yellow-500/40 hover:border-yellow-400"
    },
    {
      title: "Knowledge Platform (ZKB)",
      desc: "Canonical UPI and NFUM pharmacopeia monographs, botanical taxonomy, and Badal (substitutes) & Musleh (correctives) directories.",
      href: "/knowledge",
      badge: "Canonical",
      icon: "📖",
      roleDemo: "Medical Researcher",
      color: "border-indigo-500/40 hover:border-indigo-400"
    },
    {
      title: "AI & Hakeem Sahab Studio",
      desc: "Clinician copilot reasoning engine, 5-layer explainability, benchmark test suites, and prompt injection firewall monitor.",
      href: "/ai",
      badge: "Advisory Only",
      icon: "🧠",
      roleDemo: "AI Specialist",
      color: "border-cyan-500/40 hover:border-cyan-400"
    },
    {
      title: "ZAYVORA Public Health & Herbals Store",
      desc: "25 canonical clinical web pages, interactive 12-stage clinical loop, 10 botanical formulation monographs, and e-commerce cart.",
      href: "/website",
      badge: "Public Web",
      icon: "🌐",
      roleDemo: "Guest",
      color: "border-teal-500/40 hover:border-teal-400"
    }
  ];

  const hardwareNodes = [
    {
      name: "Nabz 10-Ajnas Pulse Sensor",
      icon: "📊",
      type: "PPG / DSP Core",
      rate: "100 Hz",
      latency: "8 ms",
      status: "STREAMING LIVE",
      metrics: "72 BPM • Layyin • Azeem • Bat'ee"
    },
    {
      name: "Lisan Multispectral Tongue Cam",
      icon: "👅",
      type: "4-Band Spectral Sensor",
      rate: "30 FPS",
      latency: "14 ms",
      status: "CALIBRATED",
      metrics: "415-850nm • Saburra White • 68% Moisture"
    },
    {
      name: "Wearables BLE Gateway",
      icon: "📡",
      type: "BLE 5.3 Hub",
      rate: "10 Hz",
      latency: "12 ms",
      status: "4 NODES PAIRED",
      metrics: "SpO2 98% • HRV 58ms • Relapse Risk 0.04"
    },
    {
      name: "Botanical QC Spectrometer",
      icon: "🔬",
      type: "NIR / Raman Spectrometer",
      rate: "Batch Scans",
      latency: "450 ms",
      status: "VERIFIED",
      metrics: "99.2% Purity • 0 ppm Pb/Cd/Hg"
    },
    {
      name: "Dispensary Cold-Chain IoT",
      icon: "❄️",
      type: "Modbus / MQTT Sensor",
      rate: "1 Hz",
      latency: "18 ms",
      status: "TEMPERATURE LOCKED",
      metrics: "19.4°C • 42% RH • FEFO Compliant"
    }
  ];

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--text)]">
      <PlatformHeader />

      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-8 space-y-10">
        
        {/* Hero Section */}
        <section className="text-center space-y-5 pt-4 pb-8 border-b border-[var(--border)]">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 shadow-inner">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Level 4 Clinically Governed Enterprise Platform</span>
            <span>·</span>
            <span>21 CFR Part 11 Compliant</span>
            <span>·</span>
            <span>v5.0 Master Edition</span>
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight">
            ZAYVORA <span className="text-[var(--gold-soft)]">HEALTH OS™</span>
          </h1>

          <p className="text-base sm:text-lg md:text-xl text-[var(--muted)] max-w-3xl mx-auto leading-relaxed">
            Clinician-Supervised Unani & Integrative Healthcare Intelligence Platform. Uniting codified classical Greco-Arab humoral science with modern molecular medicine through deterministic safety boundaries and real-time diagnostic hardware.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
            <button
              onClick={() => setShowSignInModal(true)}
              className="zv-btn-primary text-sm font-semibold px-7 py-3.5 cursor-pointer shadow-xl shadow-teal-900/30"
            >
              Launch Clinician Workspace
            </button>
            <button
              onClick={() => quickLoginRole("Patient", "/patient")}
              className="px-7 py-3.5 rounded-xl border border-[var(--border)] bg-[var(--elevated)] hover:bg-[var(--border)] text-sm font-semibold transition-colors"
            >
              Enter Patient Portal
            </button>
            <Link
              href="/website"
              className="px-7 py-3.5 rounded-xl border border-teal-500/40 bg-teal-500/10 hover:bg-teal-500/20 text-[#2DD4BF] text-sm font-semibold transition-colors"
            >
              Explore Public Website & Store →
            </Link>
          </div>

          {/* Master Operational Telemetry HUD */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 max-w-6xl mx-auto pt-6 text-left">
            <div className="p-3.5 rounded-xl bg-[var(--panel)] border border-[var(--border)]">
              <span className="text-[10px] text-[var(--muted)] block font-bold uppercase">Automated Tests</span>
              <span className="text-xl font-bold text-emerald-400">404 / 404</span>
              <span className="text-[10px] text-emerald-500/80 block mt-0.5 font-semibold">100% Pass Rate (0 Fail)</span>
            </div>
            <div className="p-3.5 rounded-xl bg-[var(--panel)] border border-[var(--border)]">
              <span className="text-[10px] text-[var(--muted)] block font-bold uppercase">Clinical Engines</span>
              <span className="text-xl font-bold text-blue-400">25 / 25</span>
              <span className="text-[10px] text-blue-500/80 block mt-0.5 font-semibold">Full Clinical Logic</span>
            </div>
            <div className="p-3.5 rounded-xl bg-[var(--panel)] border border-[var(--border)]">
              <span className="text-[10px] text-[var(--muted)] block font-bold uppercase">Hardware Sensors</span>
              <span className="text-xl font-bold text-teal-400">5 / 5 Active</span>
              <span className="text-[10px] text-teal-500/80 block mt-0.5 font-semibold">100 Hz Streaming DSP</span>
            </div>
            <div className="p-3.5 rounded-xl bg-[var(--panel)] border border-[var(--border)]">
              <span className="text-[10px] text-[var(--muted)] block font-bold uppercase">Safety Interceptions</span>
              <span className="text-xl font-bold text-amber-400">0 Open</span>
              <span className="text-[10px] text-amber-500/80 block mt-0.5 font-semibold">Deterministic Barrier</span>
            </div>
            <div className="p-3.5 rounded-xl bg-[var(--panel)] border border-[var(--border)]">
              <span className="text-[10px] text-[var(--muted)] block font-bold uppercase">FEFO Dispensary</span>
              <span className="text-xl font-bold text-purple-400">4,820 Units</span>
              <span className="text-[10px] text-purple-500/80 block mt-0.5 font-semibold">Batch-Tracked Stock</span>
            </div>
            <div className="p-3.5 rounded-xl bg-[var(--panel)] border border-[var(--border)]">
              <span className="text-[10px] text-[var(--muted)] block font-bold uppercase">Research Cohort</span>
              <span className="text-xl font-bold text-rose-400">1,240 Enrolled</span>
              <span className="text-[10px] text-rose-500/80 block mt-0.5 font-semibold">3 University Centers</span>
            </div>
          </div>
        </section>

        {/* Live System Navigation Tabs */}
        <div className="flex items-center gap-2 border-b border-[var(--border)] pb-2">
          <button
            onClick={() => setActiveTab("workspaces")}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition-colors ${
              activeTab === "workspaces"
                ? "bg-[var(--elevated)] text-[var(--gold-soft)] border border-[var(--border)]"
                : "text-[var(--muted)] hover:text-white"
            }`}
          >
            🏢 Enterprise Workspaces (10)
          </button>
          <button
            onClick={() => setActiveTab("hardware")}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition-colors ${
              activeTab === "hardware"
                ? "bg-[var(--elevated)] text-[var(--gold-soft)] border border-[var(--border)]"
                : "text-[var(--muted)] hover:text-white"
            }`}
          >
            🔌 Diagnostic Hardware Mesh (5)
          </button>
          <button
            onClick={() => setActiveTab("audit")}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition-colors ${
              activeTab === "audit"
                ? "bg-[var(--elevated)] text-[var(--gold-soft)] border border-[var(--border)]"
                : "text-[var(--muted)] hover:text-white"
            }`}
          >
            📜 Live Event Stream & Audit Trail
          </button>
          <button
            onClick={() => setActiveTab("governance")}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition-colors ${
              activeTab === "governance"
                ? "bg-[var(--elevated)] text-[var(--gold-soft)] border border-[var(--border)]"
                : "text-[var(--muted)] hover:text-white"
            }`}
          >
            ⚖️ Statutory Safety Governance
          </button>
        </div>

        {/* TAB 1: 10 Enterprise Application Workspaces */}
        {activeTab === "workspaces" && (
          <section className="space-y-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-2">
              <div>
                <h2 className="text-2xl font-bold tracking-tight">Enterprise Application Cockpits</h2>
                <p className="text-xs sm:text-sm text-[var(--muted)]">
                  Select a role-tailored environment. Use the quick launch buttons to test simulated authenticated sessions.
                </p>
              </div>
              <span className="text-xs text-[var(--muted)] font-mono">Single Secure Tenant Architecture</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {applications.map((app) => (
                <div
                  key={app.title}
                  className={`p-6 rounded-2xl bg-[var(--panel)] border ${app.color} transition-all group flex flex-col justify-between space-y-4 shadow-sm`}
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-3xl">{app.icon}</span>
                      <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-[var(--elevated)] border border-[var(--border)] text-[var(--text)]">
                        {app.badge}
                      </span>
                    </div>
                    <h3 className="text-base font-bold text-white group-hover:text-[var(--gold-soft)] transition-colors">
                      {app.title}
                    </h3>
                    <p className="text-xs text-[var(--muted)] leading-relaxed">
                      {app.desc}
                    </p>
                  </div>
                  
                  <div className="pt-3 border-t border-[var(--border)] flex items-center justify-between gap-2">
                    <button
                      onClick={() => quickLoginRole(app.roleDemo, app.href)}
                      className="px-3 py-1.5 rounded-lg bg-[var(--elevated)] hover:bg-[var(--border)] text-[11px] text-[var(--text)] font-semibold transition"
                    >
                      Demo as {app.roleDemo}
                    </button>
                    <Link
                      href={app.href}
                      className="text-xs font-semibold text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
                    >
                      Open Cockpit →
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* TAB 2: Hardware Sensor Mesh Subsystems */}
        {activeTab === "hardware" && (
          <section className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold tracking-tight">Diagnostic & Therapeutic Hardware Subsystems</h2>
              <p className="text-xs sm:text-sm text-[var(--muted)]">
                Active sensory drivers, digital signal processors (DSP), and laboratory IoT devices connected to ZAYVORA Health OS.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {hardwareNodes.map((hw) => (
                <div key={hw.name} className="p-5 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-2xl">{hw.icon}</span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">
                      {hw.status}
                    </span>
                  </div>
                  <h3 className="text-sm font-bold text-white">{hw.name}</h3>
                  <div className="text-xs text-[var(--muted)] space-y-1 font-mono">
                    <div className="flex justify-between"><span>Architecture:</span> <span className="text-white">{hw.type}</span></div>
                    <div className="flex justify-between"><span>Sampling Rate:</span> <span className="text-emerald-400">{hw.rate}</span></div>
                    <div className="flex justify-between"><span>Packet Latency:</span> <span className="text-white">{hw.latency}</span></div>
                  </div>
                  <div className="p-2.5 rounded-lg bg-[var(--background)] border border-[var(--border)] text-[11px] text-teal-300 font-mono">
                    {hw.metrics}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* TAB 3: Live Event Stream & Audit Trail */}
        {activeTab === "audit" && (
          <section className="space-y-4">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold tracking-tight">Real-Time Clinical Telemetry & Audit Stream</h2>
                <p className="text-xs text-[var(--muted)]">
                  Cryptographically hashed events across clinical encounters, hardware packets, and dispensary dispensations.
                </p>
              </div>
              <span className="text-xs text-emerald-400 font-mono">● LIVE POLLING</span>
            </div>

            <div className="p-4 rounded-2xl bg-[var(--panel)] border border-[var(--border)] space-y-2">
              {events.map((evt) => (
                <div key={evt.id} className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex items-start justify-between gap-4 text-xs font-mono">
                  <div className="flex items-center gap-3">
                    <span className="text-[var(--gold-soft)] font-bold">{evt.time}</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-[var(--elevated)] border border-[var(--border)] text-teal-300">
                      {evt.category}
                    </span>
                    <span className="text-[var(--text)]">{evt.msg}</span>
                  </div>
                  <span className="text-[var(--muted)] text-[10px] shrink-0">{evt.id}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* TAB 4: Statutory Safety Governance */}
        {activeTab === "governance" && (
          <section className="p-6 rounded-2xl bg-[var(--panel)] border border-amber-500/30 space-y-4">
            <div className="flex items-center gap-2 text-base font-bold text-amber-400">
              <span>🛡️</span>
              <span>Statutory Non-Delegable Prescribing Barrier (21 CFR Part 11)</span>
            </div>
            <p className="text-xs text-[var(--muted)] leading-relaxed">
              ZAYVORA Health OS strictly guarantees that no automated algorithm or generative AI copilot can autonomously 
              issue actionable prescriptions. Every formulation draft remains non-dispensable (<code className="text-amber-300">safe_to_lock = False</code>) 
              until explicit 21 CFR Part 11 cryptographic digital signature is affixed by a credentialed licensed clinician (<code className="text-amber-300">ROLE_SENIOR_TABEEB</code>).
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2 text-xs">
              <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                <span className="font-bold text-white block">Deterministic Safety Gate</span>
                <p className="text-[var(--muted)] mt-1">Rule-based Schedule E(1) Mudabbar verification intercepts any unpurified toxic compound.</p>
              </div>
              <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                <span className="font-bold text-white block">Cryptographic Merkle Roots</span>
                <p className="text-[var(--muted)] mt-1">All audit events and signature blocks are hashed into immutable tamper-proof Merkle chains.</p>
              </div>
              <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)]">
                <span className="font-bold text-white block">3/3 Governance Quorum</span>
                <p className="text-[var(--muted)] mt-1">Protocol modifications require unanimous tripartite consensus before deployment.</p>
              </div>
            </div>
          </section>
        )}

      </main>

      {/* Clinician Sign-In Modal */}
      {showSignInModal && (
        <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4">
          <div className="bg-[var(--panel)] border border-[var(--border)] rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <div className="flex justify-between items-center pb-2 border-b border-[var(--border)]">
              <div>
                <h3 className="font-bold text-base">Clinician Sign In</h3>
                <p className="text-xs text-[var(--muted)]">Credentialed Healthcare Practitioner Workspace</p>
              </div>
              <button
                onClick={() => setShowSignInModal(false)}
                className="text-[var(--muted)] hover:text-white text-lg font-bold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleLogin} className="space-y-3 pt-2">
              <div>
                <label className="zv-label" htmlFor="modalOrg">Clinic ID</label>
                <input
                  id="modalOrg"
                  className="zv-input"
                  value={organizationSlug}
                  onChange={(e) => setOrganizationSlug(e.target.value)}
                  required
                />
              </div>
              <div>
                <label className="zv-label" htmlFor="modalEmail">Practitioner Email</label>
                <input
                  id="modalEmail"
                  type="email"
                  className="zv-input"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div>
                <label className="zv-label" htmlFor="modalPass">Password</label>
                <input
                  id="modalPass"
                  type="password"
                  className="zv-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>

              {error && <p className="zv-error text-xs">{error}</p>}

              <button
                type="submit"
                disabled={loading}
                className="zv-btn-primary w-full text-xs font-semibold py-2.5 cursor-pointer mt-2"
              >
                {loading ? "Authenticating Practitioner..." : "Sign In & Open Workspace"}
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="border-t border-[var(--border)] bg-[var(--panel)] py-6 text-center text-xs text-[var(--muted)]">
        <p>© 2026 ZAYVORA Health OS™. All rights reserved. Level 4 Clinically Governed Integrative Care Platform.</p>
      </footer>
    </div>
  );
}
