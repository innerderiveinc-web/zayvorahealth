"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { PlatformHeader } from "@/components/PlatformHeader";
import { PlatformFooter } from "@/components/PlatformFooter";

export type UserRole = 
  | "doctor"
  | "patient"
  | "clinic"
  | "receptionist"
  | "pharmacy"
  | "research"
  | "admin"
  | "manufacturing"
  | "enterprise"
  | "website"
  | "herbals";

interface AppShellProps {
  children: React.ReactNode;
  activeRole?: UserRole;
  currentFacility?: string;
}

export function AppShell({ 
  children, 
  activeRole = "doctor",
  currentFacility = "Jamia Hamdard AUTC - Main Hospital"
}: AppShellProps) {
  const pathname = usePathname();
  const router = useRouter();
  const [role, setRole] = useState<UserRole>(activeRole);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  useEffect(() => {
    if (pathname.startsWith("/doctor")) setRole("doctor");
    else if (pathname.startsWith("/patient")) setRole("patient");
    else if (pathname.startsWith("/receptionist")) setRole("receptionist");
    else if (pathname.startsWith("/clinic")) setRole("clinic");
    else if (pathname.startsWith("/pharmacy")) setRole("pharmacy");
    else if (pathname.startsWith("/research")) setRole("research");
    else if (pathname.startsWith("/admin")) setRole("admin");
    else if (pathname.startsWith("/manufacturing")) setRole("manufacturing");
    else if (pathname.startsWith("/website/herbals") || pathname.startsWith("/website/cart")) setRole("herbals");
    else if (pathname.startsWith("/website")) setRole("website");
  }, [pathname]);

  const menuItems = [
    { id: "dashboard", label: "Dashboard", icon: "📊", href: "/dashboard" },
    { id: "patients", label: "Patients", icon: "👥", href: "/patient" },
    { id: "reception", label: "Reception / Queue", icon: "🏥", href: "/receptionist" },
    { id: "appointments", label: "Appointments", icon: "📅", href: "/clinic" },
    { id: "clinical", label: "Clinical Workspace", icon: "🩺", href: "/doctor" },
    { id: "ai_doctor", label: "AI Doctor — Hakeem Sahab", icon: "🤖", href: "/ai" },
    { id: "protocols", label: "ZAYVORA Protocols", icon: "📑", href: "/dashboard" },
    { id: "prescriptions", label: "Prescriptions", icon: "📝", href: "/doctor" },
    { id: "pharmacy", label: "Medicines / Pharmacy", icon: "💊", href: "/pharmacy" },
    { id: "diagnostics", label: "Diagnostics / Reports", icon: "🧪", href: "/dashboard" },
    { id: "treatment_plans", label: "Treatment Plans", icon: "🌿", href: "/dashboard" },
    { id: "followups", label: "Follow-ups", icon: "🔄", href: "/clinic" },
    { id: "telemedicine", label: "Telemedicine", icon: "📱", href: "/website" },
    { id: "billing", label: "Billing & Payments", icon: "💳", href: "/clinic" },
    { id: "analytics", label: "Analytics", icon: "📈", href: "/research" },
    { id: "knowledge", label: "Knowledge Base", icon: "📚", href: "/knowledge" },
    { id: "messages", label: "Messages", icon: "💬", href: "/dashboard" },
    { id: "notifications", label: "Notifications", icon: "🔔", href: "/dashboard" },
    { id: "settings", label: "Settings", icon: "⚙️", href: "/admin" },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--text)]">
      {/* Universal SaaS Header */}
      <PlatformHeader />

      {/* Main Layout (Sidebar + Workspace) */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* Collapsible Left Sidebar */}
        <aside
          className={`bg-[var(--panel)] border-r border-[var(--border)] flex flex-col transition-all duration-200 shrink-0 ${
            sidebarCollapsed ? "w-16" : "w-60"
          } hidden md:flex`}
        >
          <div className="p-3 border-b border-[var(--border)] flex items-center justify-between">
            {!sidebarCollapsed && (
              <span className="text-[10px] font-bold text-[var(--muted)] uppercase tracking-wider">
                Menu
              </span>
            )}
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="p-1 rounded-lg hover:bg-[var(--elevated)] text-[var(--muted)] hover:text-white transition"
              title="Toggle sidebar"
            >
              {sidebarCollapsed ? "▶" : "◀"}
            </button>
          </div>

          <nav className="p-2 space-y-0.5 flex-1 overflow-y-auto">
            {menuItems.map((item) => {
              const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname?.startsWith(item.href));
              return (
                <Link
                  key={item.id}
                  href={item.href}
                  className={`flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium transition ${
                    isActive
                      ? "bg-[#0D9488]/20 text-[#2DD4BF] border border-[#0D9488]/30 font-semibold"
                      : "text-[var(--muted)] hover:bg-[var(--elevated)] hover:text-white"
                  }`}
                  title={item.label}
                >
                  <span className="text-base shrink-0">{item.icon}</span>
                  {!sidebarCollapsed && <span className="truncate">{item.label}</span>}
                </Link>
              );
            })}
          </nav>

          {/* Bottom Sidebar Links */}
          <div className="p-2 border-t border-[var(--border)] bg-[var(--background)] space-y-0.5 text-xs">
            <Link href="/website/faqs" className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-[var(--muted)] hover:text-white">
              <span>❓</span> {!sidebarCollapsed && <span>Help Center</span>}
            </Link>
            <Link href="/knowledge" className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-[var(--muted)] hover:text-white">
              <span>📖</span> {!sidebarCollapsed && <span>Documentation</span>}
            </Link>
            <Link href="/admin" className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-[var(--muted)] hover:text-white">
              <span>🟢</span> {!sidebarCollapsed && <span>System Status</span>}
            </Link>
            <Link href="/website/contact" className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-[var(--muted)] hover:text-white">
              <span>📞</span> {!sidebarCollapsed && <span>Contact Support</span>}
            </Link>
          </div>
        </aside>

        {/* Workspace Body */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 bg-[var(--background)]">
          {children}
        </main>
      </div>

      {/* Universal SaaS Footer */}
      <PlatformFooter />
    </div>
  );
}
