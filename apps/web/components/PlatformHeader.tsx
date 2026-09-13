"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { clearSession, loadSession, saveSession } from "@/lib/session";
import type { TokenResponse } from "@/lib/identityApi";

export function PlatformHeader() {
  const pathname = usePathname();
  const router = useRouter();
  const [session, setSession] = useState<TokenResponse | null>(null);

  // Header Interactive States
  const [showSearchModal, setShowSearchModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfileDropdown, setShowProfileDropdown] = useState(false);
  const [showRoleSwitcher, setShowRoleSwitcher] = useState(false);
  const [lang, setLang] = useState<"EN" | "HI" | "UR">("EN");
  const [darkMode, setDarkMode] = useState(true);

  // Global search mock index
  const searchItems = [
    { type: "Patient", title: "Hamza Farooqi (MRN-2026-0814)", sub: "Age 44 • Male • Balghami • Active Afaal: Tanqiya", href: "/doctor" },
    { type: "Patient", title: "Ayesha Siddiqui (MRN-2026-0921)", sub: "Age 36 • Female • Safrawi • PCOS & Insulin Resistance", href: "/doctor" },
    { type: "Prescription", title: "RX-2026-0441 (Hamza Farooqi)", sub: "Suranjan Talkh + Kateera • 21 CFR Part 11 Locked", href: "/pharmacy" },
    { type: "Protocol", title: "Mafasil Reversal Protocol (Waja-ul-Mafasil)", sub: "4-Stage Afaal Cascade: Tanqiya, Tahleel, Taqwiyaat, Hifz", href: "/clinical" },
    { type: "Protocol", title: "Metabolic Reset 90 (Su-e-Mizaj Barid)", sub: "Dietary Anupan + MetaboCore Elite + Picrorhiza", href: "/clinical" },
    { type: "Medicine", title: "Habb-e-Suranjan Forte (Schedule E-1 Mudabbar)", sub: "Batch B2-2026 • Stock: 29 • Expiry: 2027-08-30", href: "/pharmacy" },
    { type: "Medicine", title: "ManiVital Pro (Withania + Mucuna)", sub: "Batch MVP-901 • Stock: 142 • HPLC Assay > 2.5%", href: "/website/product?id=manivital-pro" },
  ];

  const filteredSearch = searchQuery.trim() === ""
    ? searchItems.slice(0, 5)
    : searchItems.filter(item =>
        item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.sub.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.type.toLowerCase().includes(searchQuery.toLowerCase())
      );

  useEffect(() => {
    setSession(loadSession());
  }, []);

  function handleSignOut() {
    clearSession();
    setShowProfileDropdown(false);
    router.push("/");
  }

  function handleSwitchRole(role: string, targetPath: string) {
    saveSession({
      access_token: `jwt-zayvora-role-${role.toLowerCase().replace(/\s+/g, "-")}`,
      token_type: "bearer",
      expires_in: 7200,
      role: role,
      organization_id: "org-jamia-hamdard-01"
    });
    setSession(loadSession());
    setShowRoleSwitcher(false);
    setShowProfileDropdown(false);
    router.push(targetPath);
  }

  const notifications = [
    { id: 1, type: "Clinical", title: "Drug Interaction Warning", desc: "Potential synergistic depression with sedative botanicals.", priority: "Critical", time: "10m ago" },
    { id: 2, type: "Appointment", title: "New OPD Check-In", desc: "Hamza Farooqi (Token T-104) is waiting in Room 3.", priority: "High", time: "15m ago" },
    { id: 3, type: "Pharmacy", title: "FEFO Batch Allocated", desc: "Batch B2-SURANJAN dispensed under 21 CFR Part 11 sign-off.", priority: "Normal", time: "32m ago" },
  ];

  return (
    <header className="border-b border-[var(--border)] bg-[var(--panel)] sticky top-0 z-40 px-4 py-2 text-[var(--text)]">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        
        {/* Brand & Clinic Identity */}
        <div className="flex items-center gap-3 shrink-0">
          <Link href="/dashboard" className="flex items-center gap-2.5 group">
            {/* Official Logo */}
            <div className="w-9 h-9 rounded-xl bg-[var(--background)] border border-[var(--border)] flex items-center justify-center p-1 shadow-sm overflow-hidden group-hover:border-[#2DD4BF] transition-colors">
              <img
                src="/zayvora-logo.png"
                alt="ZAYVORA Logo"
                className="w-full h-full object-contain"
                onError={(e) => {
                  // Fallback letter if image not yet loaded
                  (e.target as HTMLElement).style.display = "none";
                }}
              />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-extrabold tracking-tight text-base zv-brand-title block leading-none">
                  ZAYVORA
                </span>
                <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
                  HEALTH OS
                </span>
              </div>
              <span className="text-[10px] text-[var(--muted)] block font-medium mt-0.5 truncate max-w-[200px] sm:max-w-[280px]">
                🏥 Jamia Hamdard AUTC - Main Hospital
              </span>
            </div>
          </Link>
        </div>

        {/* Live Hardware IoT Sensors Telemetry */}
        <div className="hidden xl:flex items-center gap-2 text-[10px]">
          <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-medium flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            Nabz: 100Hz
          </span>
          <span className="px-2 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 font-medium flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
            Lisan Cam
          </span>
          <span className="px-2 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 font-medium flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
            19.4°C (FEFO)
          </span>
        </div>

        {/* Global Search Bar Trigger */}
        <div className="flex-1 max-w-md hidden md:block">
          <button
            onClick={() => setShowSearchModal(true)}
            className="w-full flex items-center justify-between px-3.5 py-1.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-xs text-[var(--muted)] hover:border-[#2DD4BF] transition-all"
          >
            <span className="flex items-center gap-2">
              <span>🔍</span>
              <span>Search Patient, Rx, Protocol, Medicine...</span>
            </span>
            <kbd className="px-1.5 py-0.5 rounded bg-[var(--elevated)] border border-[var(--border)] text-[10px] font-mono">
              ⌘K
            </kbd>
          </button>
        </div>

        {/* Top Header Actions */}
        <div className="flex items-center gap-2 sm:gap-3">
          
          {/* Global Search Icon for Mobile */}
          <button
            onClick={() => setShowSearchModal(true)}
            className="md:hidden p-2 rounded-lg bg-[var(--elevated)] border border-[var(--border)] text-sm"
          >
            🔍
          </button>

          {/* Notifications Bell with Counter */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="p-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] hover:border-[#2DD4BF] text-sm relative transition"
              title="Notifications"
            >
              🔔
              <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-rose-500 text-white font-bold text-[9px] flex items-center justify-center">
                3
              </span>
            </button>

            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 rounded-2xl bg-[var(--panel)] border border-[var(--border)] shadow-2xl p-4 space-y-3 z-50">
                <div className="flex items-center justify-between border-b border-[var(--border)] pb-2">
                  <span className="font-bold text-xs text-white">Clinical & System Alerts (3)</span>
                  <button onClick={() => setShowNotifications(false)} className="text-xs text-[var(--muted)] hover:text-white">✕</button>
                </div>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {notifications.map(n => (
                    <div key={n.id} className="p-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-xs space-y-1">
                      <div className="flex justify-between items-center">
                        <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-rose-500/20 text-rose-300">{n.priority}</span>
                        <span className="text-[10px] text-[var(--muted)]">{n.time}</span>
                      </div>
                      <h5 className="font-bold text-white text-xs">{n.title}</h5>
                      <p className="text-[11px] text-[var(--muted)] leading-snug">{n.desc}</p>
                    </div>
                  ))}
                </div>
                <div className="pt-2 border-t border-[var(--border)] flex justify-between text-[11px]">
                  <Link href="/notifications" className="text-emerald-400 font-bold hover:underline">View All Notifications →</Link>
                  <button onClick={() => setShowNotifications(false)} className="text-[var(--muted)] hover:text-white">Clear</button>
                </div>
              </div>
            )}
          </div>

          {/* Messages */}
          <Link
            href="/messages"
            className="p-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] hover:border-[#2DD4BF] text-sm text-[var(--muted)] hover:text-white transition"
            title="Messages & Care Team"
          >
            💬
          </Link>

          {/* Help & Support */}
          <Link
            href="/website/faqs"
            className="hidden sm:flex p-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] hover:border-[#2DD4BF] text-sm text-[var(--muted)] hover:text-white transition"
            title="Help Center"
          >
            ❓
          </Link>

          {/* Language Selector */}
          <div className="flex items-center bg-[var(--background)] rounded-xl border border-[var(--border)] p-0.5 text-[10px] font-bold">
            {(["EN", "HI", "UR"] as const).map(l => (
              <button
                key={l}
                onClick={() => setLang(l)}
                className={`px-2 py-1 rounded-lg transition ${
                  lang === l ? "bg-[var(--elevated)] text-[#2DD4BF] shadow-xs" : "text-[var(--muted)] hover:text-white"
                }`}
              >
                {l}
              </button>
            ))}
          </div>

          {/* Dark Mode Toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="p-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-xs hover:border-[var(--gold-soft)] transition"
            title="Toggle theme"
          >
            {darkMode ? "🌙" : "☀️"}
          </button>

          {/* Role Badge & User Profile Dropdown */}
          <div className="relative">
            <button
              onClick={() => setShowProfileDropdown(!showProfileDropdown)}
              className="flex items-center gap-2 p-1.5 pl-2.5 rounded-xl bg-[var(--elevated)] border border-[var(--border)] hover:border-[#2DD4BF] transition"
            >
              <span className="text-xs font-bold text-white hidden sm:inline">Dr. Irfan</span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400">
                {session?.role || "Doctor"}
              </span>
              <div className="w-6 h-6 rounded-full bg-teal-600 text-white font-bold text-xs flex items-center justify-center">
                I
              </div>
            </button>

            {showProfileDropdown && (
              <div className="absolute right-0 mt-2 w-64 rounded-2xl bg-[var(--panel)] border border-[var(--border)] shadow-2xl p-3 space-y-2 z-50 text-xs">
                <div className="px-3 py-2 border-b border-[var(--border)] space-y-0.5">
                  <div className="font-bold text-white">Dr. Irfan Ashraf</div>
                  <div className="text-[11px] text-[var(--muted)]">Senior Tabeeb • CCIM-BUMS</div>
                  <div className="text-[10px] font-mono text-emerald-400">Jamia Hamdard AUTC</div>
                </div>

                <div className="py-1 space-y-0.5 text-[11px]">
                  <Link href="/doctor" onClick={() => setShowProfileDropdown(false)} className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white">
                    <span>👤</span> My Profile
                  </Link>
                  <Link href="/settings" onClick={() => setShowProfileDropdown(false)} className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white">
                    <span>⚙️</span> Account Settings
                  </Link>
                  <Link href="/clinic" onClick={() => setShowProfileDropdown(false)} className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white">
                    <span>🏥</span> Clinic Settings
                  </Link>
                  <Link href="/admin" onClick={() => setShowProfileDropdown(false)} className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white">
                    <span>🛡️</span> Security & Compliance
                  </Link>
                  <Link href="/admin" onClick={() => setShowProfileDropdown(false)} className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white">
                    <span>📜</span> Activity Logs (Merkle)
                  </Link>
                  <button
                    onClick={() => setShowRoleSwitcher(!showRoleSwitcher)}
                    className="w-full text-left flex items-center justify-between px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-teal-300 font-semibold"
                  >
                    <span className="flex items-center gap-2.5">
                      <span>🔄</span> Switch Role
                    </span>
                    <span>→</span>
                  </button>
                </div>

                {showRoleSwitcher && (
                  <div className="p-2 rounded-xl bg-[var(--background)] border border-[var(--border)] space-y-1">
                    <span className="text-[10px] font-bold text-[var(--muted)] uppercase block px-1">Select Persona</span>
                    <button onClick={() => handleSwitchRole("Doctor", "/doctor")} className="w-full text-left px-2 py-1 rounded hover:bg-[var(--elevated)] text-[11px] text-white">
                      🩺 Doctor (Clinical Suite)
                    </button>
                    <button onClick={() => handleSwitchRole("Admin", "/admin")} className="w-full text-left px-2 py-1 rounded hover:bg-[var(--elevated)] text-[11px] text-white">
                      🛡️ Admin (Governance)
                    </button>
                    <button onClick={() => handleSwitchRole("Patient", "/patient")} className="w-full text-left px-2 py-1 rounded hover:bg-[var(--elevated)] text-[11px] text-white">
                      👤 Patient (PHR Portal)
                    </button>
                    <button onClick={() => handleSwitchRole("Pharmacist", "/pharmacy")} className="w-full text-left px-2 py-1 rounded hover:bg-[var(--elevated)] text-[11px] text-white">
                      💊 Pharmacist (Dispensary)
                    </button>
                    <button onClick={() => handleSwitchRole("Receptionist", "/clinic")} className="w-full text-left px-2 py-1 rounded hover:bg-[var(--elevated)] text-[11px] text-white">
                      🏥 Receptionist (Queue OPD)
                    </button>
                  </div>
                )}

                <div className="pt-2 border-t border-[var(--border)]">
                  <button
                    onClick={handleSignOut}
                    className="w-full text-left flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-rose-400 hover:bg-rose-500/10 font-bold text-[11px]"
                  >
                    <span>🚪</span> Logout
                  </button>
                </div>
              </div>
            )}
          </div>

        </div>

      </div>

      {/* Global Search Modal */}
      {showSearchModal && (
        <div className="fixed inset-0 z-50 bg-black/80 flex items-start justify-center pt-20 p-4">
          <div className="bg-[var(--panel)] border border-[var(--border)] rounded-2xl max-w-xl w-full p-4 space-y-4 shadow-2xl">
            <div className="flex items-center gap-3 border-b border-[var(--border)] pb-3">
              <span className="text-base">🔍</span>
              <input
                autoFocus
                placeholder="Search patients, prescriptions, protocols, medicines..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-transparent text-sm text-white focus:outline-none"
              />
              <button
                onClick={() => setShowSearchModal(false)}
                className="text-xs text-[var(--muted)] hover:text-white px-2 py-1 rounded bg-[var(--elevated)]"
              >
                ESC
              </button>
            </div>

            <div className="space-y-1.5 max-h-80 overflow-y-auto">
              <span className="text-[10px] font-bold text-[var(--muted)] uppercase px-2">Clinical Results ({filteredSearch.length})</span>
              {filteredSearch.map((item, idx) => (
                <Link
                  key={idx}
                  href={item.href}
                  onClick={() => setShowSearchModal(false)}
                  className="p-3 rounded-xl hover:bg-[var(--elevated)] border border-transparent hover:border-[var(--border)] flex items-start justify-between gap-3 text-xs block transition"
                >
                  <div className="space-y-0.5">
                    <div className="flex items-center gap-2">
                      <span className="px-1.5 py-0.2 rounded bg-teal-500/20 text-teal-300 font-mono text-[9px] font-bold">{item.type}</span>
                      <span className="font-bold text-white">{item.title}</span>
                    </div>
                    <p className="text-[11px] text-[var(--muted)]">{item.sub}</p>
                  </div>
                  <span className="text-[var(--muted)] text-[10px] font-semibold">Open →</span>
                </Link>
              ))}
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
