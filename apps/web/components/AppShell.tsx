"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

export type UserRole = 
  | "doctor"
  | "patient"
  | "clinic"
  | "pharmacy"
  | "research"
  | "admin";

interface RoleConfig {
  id: UserRole;
  label: string;
  userName: string;
  title: string;
  defaultPath: string;
  allowedNav: { label: string; href: string; icon: string }[];
}

const ROLES: Record<UserRole, RoleConfig> = {
  doctor: {
    id: "doctor",
    label: "Doctor / Senior Tabeeb",
    userName: "Hakim Dr. Tariq Mansoor",
    title: "Senior Tabeeb (CCIM-BUMS-2004-9841)",
    defaultPath: "/doctor",
    allowedNav: [
      { label: "Consultation Cockpit", href: "/doctor", icon: "🩺" },
      { label: "Patient 360", href: "/patient", icon: "👤" },
      { label: "Knowledge Monograph", href: "/knowledge", icon: "📖" },
      { label: "Research Cohorts", href: "/research", icon: "🔬" },
    ],
  },
  patient: {
    id: "patient",
    label: "Patient Portal",
    userName: "Hamza Farooqi",
    title: "MRN-2026-0814 • Balghami",
    defaultPath: "/patient",
    allowedNav: [
      { label: "My Health 360", href: "/patient", icon: "👤" },
      { label: "Care Plans & Nuskha", href: "/patient?tab=prescriptions", icon: "💊" },
      { label: "Lifestyle (Asbab Sittah)", href: "/patient?tab=lifestyle", icon: "🌿" },
      { label: "Book Appointment", href: "/patient?tab=appointments", icon: "📅" },
    ],
  },
  clinic: {
    id: "clinic",
    label: "Clinic Receptionist / Admin",
    userName: "Sana Khan",
    title: "OPD Operations Desk Lead",
    defaultPath: "/clinic",
    allowedNav: [
      { label: "Live OPD Queue", href: "/clinic", icon: "📋" },
      { label: "Walk-in Registration", href: "/clinic?tab=register", icon: "📝" },
      { label: "Doctor Availability", href: "/clinic?tab=roster", icon: "🩺" },
      { label: "Billing & Invoicing", href: "/clinic?tab=billing", icon: "💳" },
    ],
  },
  pharmacy: {
    id: "pharmacy",
    label: "Clinical Pharmacist",
    userName: "Zainab Ali",
    title: "Chief Dispensary Pharmacist",
    defaultPath: "/pharmacy",
    allowedNav: [
      { label: "Dispensary Queue", href: "/pharmacy", icon: "💊" },
      { label: "FEFO Inventory", href: "/pharmacy?tab=fefo", icon: "📦" },
      { label: "Schedule E(1) Mudabbar", href: "/pharmacy?tab=mudabbar", icon: "🛡️" },
      { label: "Stock Movement", href: "/pharmacy?tab=stock", icon: "📊" },
    ],
  },
  research: {
    id: "research",
    label: "Clinical Researcher",
    userName: "Dr. K. Saxena",
    title: "Principal Clinical Investigator",
    defaultPath: "/research",
    allowedNav: [
      { label: "Clinical Trials Registry", href: "/research", icon: "🔬" },
      { label: "RWE Patient Cohorts", href: "/research?tab=cohorts", icon: "👥" },
      { label: "Adverse Events (WHO-UMC)", href: "/research?tab=adr", icon: "⚠️" },
      { label: "Protocol Designer", href: "/research?tab=protocols", icon: "📑" },
    ],
  },
  admin: {
    id: "admin",
    label: "Platform Administrator",
    userName: "Admin Console",
    title: "IT Governance & Security",
    defaultPath: "/admin",
    allowedNav: [
      { label: "Facility Management", href: "/admin", icon: "🏥" },
      { label: "21 CFR Part 11 Merkle Ledger", href: "/admin?tab=merkle", icon: "🔒" },
      { label: "RBAC & Permissions", href: "/admin?tab=rbac", icon: "🛡️" },
      { label: "Safety Firewall Rules", href: "/admin?tab=firewall", icon: "⚙️" },
    ],
  },
};

interface AppShellProps {
  children: React.ReactNode;
  activeRole?: UserRole;
  currentFacility?: string;
}

export function AppShell({ 
  children, 
  activeRole = "doctor",
  currentFacility = "Central Integrative Clinical Facility"
}: AppShellProps) {
  const pathname = usePathname();
  const router = useRouter();
  const [role, setRole] = useState<UserRole>(activeRole);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    // Detect role from path
    if (pathname.startsWith("/doctor")) setRole("doctor");
    else if (pathname.startsWith("/patient")) setRole("patient");
    else if (pathname.startsWith("/clinic")) setRole("clinic");
    else if (pathname.startsWith("/pharmacy")) setRole("pharmacy");
    else if (pathname.startsWith("/research")) setRole("research");
    else if (pathname.startsWith("/admin")) setRole("admin");
  }, [pathname]);

  const currentRoleConfig = ROLES[role] || ROLES.doctor;

  const handleRoleChange = (newRole: UserRole) => {
    setRole(newRole);
    router.push(ROLES[newRole].defaultPath);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#0A0F1D] text-[#F8FAFC]">
      {/* ================================================================= */}
      {/* ENTERPRISE TOP HEADER */}
      {/* ================================================================= */}
      <header className="bg-[#0F172A] border-b border-[#334155] px-4 py-2.5 sticky top-0 z-40">
        <div className="flex items-center justify-between gap-4">
          
          {/* Brand & Facility Info */}
          <div className="flex items-center gap-3">
            <button 
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-1.5 rounded-lg hover:bg-[#1E293B] text-[#94A3B8] transition"
              aria-label="Toggle Navigation"
            >
              ☰
            </button>
            <div className="w-8 h-8 rounded-lg bg-[#0D9488] flex items-center justify-center font-bold text-white text-lg">
              Z
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold tracking-tight text-white text-sm md:text-base">ZAYVORA Health OS™</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded font-semibold bg-[#0D9488]/20 text-[#2DD4BF] border border-[#0D9488]/30">
                  Enterprise v5.0
                </span>
              </div>
              <p className="text-[11px] text-[#94A3B8] hidden sm:block">{currentFacility}</p>
            </div>
          </div>

          {/* Role Switcher & User Profile Context */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 bg-[#0A0F1D] px-2.5 py-1.5 rounded-lg border border-[#334155]">
              <span className="text-[11px] text-[#94A3B8] hidden md:inline">Workspace:</span>
              <select
                value={role}
                onChange={(e) => handleRoleChange(e.target.value as UserRole)}
                className="bg-transparent text-xs font-semibold text-[#2DD4BF] focus:outline-none cursor-pointer"
              >
                {Object.values(ROLES).map((r) => (
                  <option key={r.id} value={r.id} className="bg-[#0F172A] text-white">
                    {r.label}
                  </option>
                ))}
              </select>
            </div>

            {/* User Details */}
            <div className="hidden lg:flex flex-col text-right">
              <span className="text-xs font-medium text-white">{currentRoleConfig.userName}</span>
              <span className="text-[10px] text-[#94A3B8]">{currentRoleConfig.title}</span>
            </div>

            {/* Status Ping */}
            <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-[#1E293B] border border-[#334155] text-[11px] text-[#34D399]">
              <span className="w-2 h-2 rounded-full bg-[#10B981] animate-pulse"></span>
              <span className="hidden sm:inline">Systems Live</span>
            </div>
          </div>
        </div>
      </header>

      {/* ================================================================= */}
      {/* MAIN LAYOUT (SIDEBAR + CONTENT) */}
      {/* ================================================================= */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* Contextual Left Sidebar */}
        <aside 
          className={`bg-[#0F172A] border-r border-[#334155] flex flex-col transition-all duration-200 ${
            sidebarOpen ? "w-60" : "w-16"
          }`}
        >
          {/* Navigation Links */}
          <nav className="p-2 space-y-1 flex-1 overflow-y-auto">
            <div className="px-2 py-1.5 text-[10px] font-semibold tracking-wider text-[#64748B] uppercase">
              {sidebarOpen ? currentRoleConfig.label : "NAV"}
            </div>
            {currentRoleConfig.allowedNav.map((item) => {
              const isActive = pathname === item.href.split("?")[0];
              return (
                <Link
                  key={item.label}
                  href={item.href}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium transition ${
                    isActive 
                      ? "bg-[#0D9488]/15 text-[#2DD4BF] border border-[#0D9488]/30" 
                      : "text-[#94A3B8] hover:bg-[#1E293B] hover:text-white"
                  }`}
                >
                  <span className="text-sm">{item.icon}</span>
                  {sidebarOpen && <span>{item.label}</span>}
                </Link>
              );
            })}
          </nav>

          {/* Quick Security & Integrity Status */}
          {sidebarOpen && (
            <div className="p-3 border-t border-[#334155] bg-[#0A0F1D]/50 text-[11px] text-[#94A3B8] space-y-1">
              <div className="flex items-center justify-between">
                <span>21 CFR Part 11:</span>
                <span className="text-[#34D399] font-medium">Secured</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Schedule E(1):</span>
                <span className="text-[#2DD4BF] font-medium">Gate Active</span>
              </div>
            </div>
          )}
        </aside>

        {/* Dynamic Page Workspace */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 bg-[#0A0F1D]">
          {children}
        </main>
      </div>
    </div>
  );
}
