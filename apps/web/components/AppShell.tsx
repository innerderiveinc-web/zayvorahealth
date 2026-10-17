"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { PlatformHeader } from "@/components/PlatformHeader";
import { PlatformFooter } from "@/components/PlatformFooter";
import { Sidebar, UserRole } from "@/components/Sidebar";
import { AuthService, UserSession } from "@/lib/services/authService";
import { useAuth } from "@/lib/hooks/useAuth";

export type { UserRole };

interface AppShellProps {
  children: React.ReactNode;
  activeRole?: UserRole;
  currentFacility?: string;
}

export function AppShell({ 
  children, 
  activeRole = "doctor",
  currentFacility = "ZAYVORA Matab™ — Central Care Centre"
}: AppShellProps) {
  const pathname = usePathname();
  const { logout } = useAuth();
  const [role, setRole] = useState<UserRole>(activeRole);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [session, setSession] = useState<UserSession | null>(null);

  useEffect(() => {
    setSession(AuthService.getSession());
  }, []);

  useEffect(() => {
    if (pathname.startsWith("/doctor")) setRole("doctor");
    else if (pathname.startsWith("/patient")) setRole("patient");
    else if (pathname.startsWith("/reception") || pathname.startsWith("/receptionist") || pathname.startsWith("/clinic")) setRole("receptionist");
    else if (pathname.startsWith("/pharmacy")) setRole("pharmacy");
    else if (pathname.startsWith("/research")) setRole("research");
    else if (pathname.startsWith("/admin")) setRole("admin");
    else if (pathname.startsWith("/nurse")) setRole("nurse");
    else if (pathname.startsWith("/manufacturing")) setRole("manufacturing");
    else if (pathname.startsWith("/enterprise")) setRole("admin");
    else if (pathname.startsWith("/knowledge") || pathname.startsWith("/herbals")) setRole("knowledge");
    else if (pathname.startsWith("/website")) setRole("website");
  }, [pathname]);

  // Dedicated Patient Shell (Oracle Health / Mayo Mobile-First Model)
  if (role === "patient" || pathname.startsWith("/patient")) {
    return (
      <div className="min-h-screen flex flex-col bg-[#0A0F1D] text-slate-100 pb-20 md:pb-0">
        {/* Patient Minimal Top Bar */}
        <header className="border-b border-slate-800 bg-[#0F172A]/95 backdrop-blur-md sticky top-0 z-40 px-4 py-3">
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <Link href="/patient" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-emerald-950/60 border border-emerald-500/40 flex items-center justify-center p-1">
                <img src="/zayvora-logo.png" alt="ZAYVORA" className="w-full h-full object-contain" onError={(e) => { (e.target as HTMLElement).style.display = "none"; }} />
              </div>
              <div>
                <span className="font-extrabold text-sm text-white tracking-tight">ZAYVORA</span>
                <span className="text-[10px] text-emerald-400 font-medium block">My Health Portal</span>
              </div>
            </Link>

            <div className="flex items-center gap-3">
              <span className="text-xs text-slate-300 font-medium hidden sm:inline">
                Good day, <strong className="text-white">{session?.user?.fullName ? session.user.fullName.split(' ')[0] : "Patient"}</strong>
              </span>
              <button className="p-2 rounded-xl bg-slate-800 border border-slate-700 hover:border-emerald-500 text-sm relative transition" title="Patient Notifications">
                🔔
                <span className="absolute -top-1 -right-1 w-3.5 h-3.5 rounded-full bg-emerald-500 text-white font-bold text-[8px] flex items-center justify-center">
                  1
                </span>
              </button>
              <Link href="/patient?tab=profile" className="w-7 h-7 rounded-full bg-emerald-700 text-white font-bold text-xs flex items-center justify-center shadow-sm" title={session?.user?.fullName || "Patient Profile"}>
                {session?.user?.fullName ? session.user.fullName.split(' ').map((n: string) => n[0]).join('').substring(0, 2).toUpperCase() : "PT"}
              </Link>
              <button
                onClick={logout}
                className="text-xs text-slate-400 hover:text-red-400 transition px-2 py-1 rounded-lg border border-slate-700 hover:border-red-500"
                title="Sign Out"
              >
                ⏻
              </button>
            </div>
          </div>
        </header>

        {/* Patient Portal Workspace Body */}
        <main className="flex-1 max-w-4xl w-full mx-auto p-4 sm:p-6">
          {children}
        </main>

        {/* Patient Bottom Navigation Bar (Mobile / Sticky) */}
        <nav className="fixed bottom-0 left-0 right-0 z-50 bg-[#0F172A]/95 backdrop-blur-md border-t border-slate-800 py-2 px-6">
          <div className="max-w-md mx-auto flex justify-between items-center text-xs">
            <Link href="/patient" className="flex flex-col items-center gap-0.5 text-emerald-400 font-semibold">
              <span className="text-base">🏠</span>
              <span className="text-[10px]">Home</span>
            </Link>
            <Link href="/patient?tab=treatment-plans" className="flex flex-col items-center gap-0.5 text-slate-400 hover:text-white transition">
              <span className="text-base">🌿</span>
              <span className="text-[10px]">Care</span>
            </Link>
            <Link href="/patient?tab=reports" className="flex flex-col items-center gap-0.5 text-slate-400 hover:text-white transition">
              <span className="text-base">📊</span>
              <span className="text-[10px]">Health</span>
            </Link>
            <Link href="/patient?tab=messages" className="flex flex-col items-center gap-0.5 text-slate-400 hover:text-white transition">
              <span className="text-base">💬</span>
              <span className="text-[10px]">Messages</span>
            </Link>
            <Link href="/patient?tab=profile" className="flex flex-col items-center gap-0.5 text-slate-400 hover:text-white transition">
              <span className="text-base">👤</span>
              <span className="text-[10px]">Me</span>
            </Link>
          </div>
        </nav>
      </div>
    );
  }

  // Clinician & Operational OS Shell
  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--text)]">
      {/* Universal Enterprise Clinician Header */}
      <PlatformHeader />

      {/* Main Layout (Role-Aware Sidebar + Workspace) */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* Role-Aware Left Sidebar */}
        <Sidebar
          role={role}
          collapsed={sidebarCollapsed}
          onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
        />

        {/* Workspace Body */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 bg-[var(--background)]">
          {children}
        </main>
      </div>

      {/* Universal Enterprise Footer */}
      <PlatformFooter />
    </div>
  );
}
