"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { clearSession, loadSession } from "@/lib/auth";
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
  const [selectedFacility, setSelectedFacility] = useState("New Delhi Central Matab & Hospital");

  // Facilities list
  const facilities = [
    "New Delhi Central Matab & Hospital",
    "Lucknow Matab & Research Complex",
    "Hyderabad Integrative Care Centre",
    "Bengaluru Wellness & Clinical Matab",
    "Srinagar Botanical Medicine Institute",
  ];

  // Dynamic search categories
  const searchCategories = [
    { type: "Patient Search", title: "Search Master Patient Index (MPI)", sub: "Lookup active patient files by Name, ABHA ID, or MRN", href: "/doctor" },
    { type: "Formulation Index", title: "Codified Pharmacopoeia (UPI / NFUM)", sub: "250+ Botanical monographs, HPLC active markers, and safety limits", href: "/knowledge" },
    { type: "Prescription Registry", title: "Digital Prescription Ledger", sub: "21 CFR Part 11 signed prescriptions and dispensing status", href: "/pharmacy" },
    { type: "Clinical Protocols", title: "Afaal & Regimenal Protocols", sub: "16 Tadbeer modalities, 4-stage cascade, and dietetics", href: "/doctor" },
    { type: "Inventory & Batch", title: "Dispensary & Cold-Chain Stock", sub: "FEFO batch allocations and Schedule E(1) Mudabbar verification", href: "/pharmacy" },
  ];

  const filteredSearch = searchQuery.trim() === ""
    ? searchCategories
    : searchCategories.filter(item =>
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
    router.replace("/login");
  }

  const notifications = [
    { id: 1, type: "Clinical Safety", title: "Drug-Herb Interaction Caution", desc: "Potential synergistic metabolic inhibition with sedative botanicals.", priority: "Critical", time: "8m ago" },
    { id: 2, type: "OPD Triage", title: "Patient Checked In", desc: "Next scheduled outpatient token waiting in Consultation Room 2.", priority: "High", time: "14m ago" },
    { id: 3, type: "Dispensary", title: "FEFO Batch Allocated", desc: "Batch released under electronic signature and CoA verification.", priority: "Normal", time: "28m ago" },
  ];

  return (
    <header className="border-b border-[var(--border)] bg-[var(--panel)] sticky top-0 z-40 px-4 py-2 text-[var(--text)]">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        
        {/* Brand & Executive Identity */}
        <div className="flex items-center gap-3 shrink-0">
          <Link href="/doctor" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-[var(--background)] border border-[var(--border)] flex items-center justify-center p-1 shadow-sm overflow-hidden group-hover:border-emerald-500 transition-colors">
              <img
                src="/zayvora-logo.png"
                alt="ZAYVORA Logo"
                className="w-full h-full object-contain"
                onError={(e) => {
                  (e.target as HTMLElement).style.display = "none";
                }}
              />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-extrabold tracking-tight text-base text-white block leading-none">
                  ZAYVORA
                </span>
                <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
                  HEALTH OS™
                </span>
              </div>
              <span className="text-[10px] text-[var(--muted)] block font-medium mt-0.5 truncate max-w-[220px] sm:max-w-[320px]">
                🏥 {selectedFacility}
              </span>
            </div>
          </Link>
        </div>

        {/* Hardware Integration Architecture Status */}
        <div className="hidden xl:flex items-center gap-2 text-[10px]">
          <span className="px-2.5 py-0.5 rounded-full bg-slate-800/80 border border-slate-700/80 text-slate-300 font-medium flex items-center gap-1.5" title="Hardware Integration Architecture - Awaiting physical device telemetry verification">
            <span className="w-1.5 h-1.5 rounded-full bg-slate-500"></span>
            Hardware Integration Architecture
          </span>
          <span className="px-2 py-0.5 rounded-full bg-slate-800/60 border border-slate-700/70 text-slate-400 font-mono text-[10px]" title="Zero real physical devices currently connected">
            Connected Devices: 0
          </span>
        </div>

        {/* Global Search Bar Trigger (⌘K) */}
        <div className="flex-1 max-w-md hidden md:block">
          <button
            onClick={() => setShowSearchModal(true)}
            className="w-full flex items-center justify-between px-3.5 py-1.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-xs text-[var(--muted)] hover:border-emerald-500/60 transition-all"
          >
            <span className="flex items-center gap-2">
              <span>🔍</span>
              <span>Search Patient, MRN, Nuskha, Mufradat, Knowledge...</span>
            </span>
            <kbd className="px-1.5 py-0.5 rounded bg-[var(--elevated)] border border-[var(--border)] text-[10px] font-mono">
              ⌘K
            </kbd>
          </button>
        </div>

        {/* Header Right Actions: Facility, Alerts, Tasks, Profile */}
        <div className="flex items-center gap-2 sm:gap-3">
          
          {/* Facility Selector */}
          <div className="hidden lg:flex items-center gap-1.5 text-xs">
            <select
              value={selectedFacility}
              onChange={(e) => setSelectedFacility(e.target.value)}
              aria-label="Select clinical facility"
              className="bg-[var(--background)] border border-[var(--border)] text-[11px] font-medium text-slate-300 rounded-lg px-2.5 py-1 focus:outline-none focus:border-emerald-500 cursor-pointer"
            >
              {facilities.map((fac, idx) => (
                <option key={idx} value={fac} className="bg-[#0F172A] text-slate-200">
                  📍 {fac}
                </option>
              ))}
            </select>
          </div>

          {/* Global Search Icon for Mobile */}
          <button
            onClick={() => setShowSearchModal(true)}
            className="md:hidden p-2 rounded-lg bg-[var(--elevated)] border border-[var(--border)] text-sm"
          >
            🔍
          </button>

          {/* Pending Clinical Tasks */}
          <Link
            href="/doctor"
            className="hidden sm:flex items-center gap-1 px-2.5 py-1 rounded-xl bg-[var(--elevated)] border border-[var(--border)] hover:border-emerald-500/40 text-xs text-slate-300 transition"
            title="Clinical Tasks"
          >
            <span>📋</span>
            <span className="font-semibold text-[11px]">Tasks</span>
            <span className="ml-0.5 px-1.5 py-0.2 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-bold">
              3
            </span>
          </Link>

          {/* Notifications Bell with Counter */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="p-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] hover:border-emerald-500/40 text-sm relative transition"
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
                  <span className="font-bold text-xs text-white">Clinical &amp; System Alerts (3)</span>
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
              </div>
            )}
          </div>

          {/* Clinician User Profile Dropdown */}
          <div className="relative">
            <button
              onClick={() => setShowProfileDropdown(!showProfileDropdown)}
              className="flex items-center gap-2 p-1.5 rounded-xl hover:bg-[var(--elevated)] border border-transparent hover:border-[var(--border)] transition"
            >
              <div className="w-7 h-7 rounded-full bg-emerald-600 text-white font-bold text-xs flex items-center justify-center shadow-sm">
                IA
              </div>
              <span className="text-xs font-semibold text-white hidden sm:inline">
                Dr. Irfan Ashraf ▾
              </span>
            </button>

            {showProfileDropdown && (
              <div className="absolute right-0 mt-2 w-72 rounded-2xl bg-[var(--panel)] border border-[var(--border)] shadow-2xl p-3 space-y-2 z-50 text-xs">
                <div className="px-3 py-2 border-b border-[var(--border)] space-y-0.5">
                  <div className="font-bold text-white">
                    {session?.user?.fullName || "Hakeem Dr. Irfan Ashraf"}
                  </div>
                  <div className="text-[11px] text-emerald-400 font-medium">
                    {session?.user?.role === "SUPER_ADMIN" || !session?.user?.role
                      ? "Founder, Chairman & Chief Architect"
                      : session?.user?.role}
                  </div>
                  <div className="text-[10px] text-[var(--muted)]">
                    {session?.user?.role === "SUPER_ADMIN" || !session?.user?.role
                      ? "Senior Tabeeb · BUMS (Unani Medicine)"
                      : session?.user?.email || "ZAYVORA Health OS™"}
                  </div>
                </div>

                <div className="py-1 space-y-0.5 text-[11px]">
                  {(!session?.user?.role || session?.user?.role === "SUPER_ADMIN" || session?.user?.role === "CLINIC_ADMIN") ? (
                    <>
                      <div className="px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
                        <span>👑</span> Master Switcher (God View)
                      </div>
                      <Link href="/doctor" onClick={() => setShowProfileDropdown(false)} className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white">
                        <span>🩺</span> Clinical Desk™ (OPD)
                      </Link>
                      <Link href="/nurse" onClick={() => setShowProfileDropdown(false)} className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white">
                        <span>🏥</span> Nurse Station (Ward/Vitals)
                      </Link>
                      <Link href="/receptionist" onClick={() => setShowProfileDropdown(false)} className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white">
                        <span>📋</span> Reception &amp; Token Queue
                      </Link>
                      <Link href="/pharmacy" onClick={() => setShowProfileDropdown(false)} className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white">
                        <span>💊</span> Dispensary &amp; FEFO Inventory
                      </Link>
                      <Link href="/manufacturing" onClick={() => setShowProfileDropdown(false)} className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white">
                        <span>🏭</span> Manufacturing Lab &amp; eBMR
                      </Link>
                      <Link href="/research/workspace" onClick={() => setShowProfileDropdown(false)} className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white">
                        <span>🔬</span> Clinical Trials &amp; RWE
                      </Link>
                      <Link href="/patient" onClick={() => setShowProfileDropdown(false)} className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white">
                        <span>👤</span> Patient Portal View
                      </Link>
                      <Link href="/admin" onClick={() => setShowProfileDropdown(false)} className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white">
                        <span>🛡️</span> Governance &amp; Audit Logs
                      </Link>
                    </>
                  ) : (
                    <Link
                      href={
                        session?.user?.role === "DOCTOR" || session?.user?.role === "HAKEEM" ? "/doctor" :
                        session?.user?.role === "NURSE" || session?.user?.role === "NURSE_COORDINATOR" ? "/nurse" :
                        session?.user?.role === "PHARMACIST" ? "/pharmacy" :
                        session?.user?.role === "RECEPTIONIST" ? "/receptionist" :
                        session?.user?.role === "RESEARCHER" ? "/research/workspace" :
                        session?.user?.role === "MANUFACTURING_HEAD" ? "/manufacturing" :
                        "/patient"
                      }
                      onClick={() => setShowProfileDropdown(false)}
                      className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg hover:bg-[var(--elevated)] text-white font-medium"
                    >
                      <span>⚡</span> Open My Assigned Desk
                    </Link>
                  )}
                </div>

                <div className="pt-2 border-t border-[var(--border)]">
                  <button
                    onClick={handleSignOut}
                    className="w-full text-left flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-rose-400 hover:bg-rose-500/10 font-bold text-[11px]"
                  >
                    <span>🚪</span> Sign Out
                  </button>
                </div>
              </div>
            )}
          </div>

        </div>

      </div>

      {/* Global Search Modal (⌘K) */}
      {showSearchModal && (
        <div className="fixed inset-0 z-50 bg-black/80 flex items-start justify-center pt-20 p-4">
          <div className="bg-[var(--panel)] border border-[var(--border)] rounded-2xl max-w-xl w-full p-4 space-y-4 shadow-2xl">
            <div className="flex items-center gap-3 border-b border-[var(--border)] pb-3">
              <span className="text-base">🔍</span>
              <input
                autoFocus
                placeholder="Search patients, MRN, Nuskha, Mufradat, knowledge..."
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
              <span className="text-[10px] font-bold text-[var(--muted)] uppercase px-2">Clinical Indexes</span>
              {filteredSearch.map((item, idx) => (
                <Link
                  key={idx}
                  href={item.href}
                  onClick={() => setShowSearchModal(false)}
                  className="p-3 rounded-xl hover:bg-[var(--elevated)] border border-transparent hover:border-[var(--border)] flex items-start justify-between gap-3 text-xs block transition"
                >
                  <div className="space-y-0.5">
                    <div className="flex items-center gap-2">
                      <span className="px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-300 font-mono text-[9px] font-bold">{item.type}</span>
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
