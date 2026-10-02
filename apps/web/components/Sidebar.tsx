"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export type UserRole =
  | "doctor"
  | "patient"
  | "receptionist"
  | "pharmacy"
  | "admin"
  | "manufacturing"
  | "research"
  | "knowledge"
  | "nurse"
  | "website";

interface NavItem {
  id: string;
  label: string;
  icon: string;
  href: string;
  badge?: string;
  roles: UserRole[];
}

const NAV_ITEMS: NavItem[] = [
  // ── Patient Navigation (Master Prompt 5 canonical surfaces)
  { id: "pt-health",       label: "My Health",     icon: "👤", href: "/patient?tab=health",   roles: ["patient"] },
  { id: "pt-care",         label: "My Care",       icon: "🩺", href: "/patient?tab=care",     roles: ["patient"] },
  { id: "pt-plan",         label: "My Plan",       icon: "📜", href: "/patient?tab=plan",     roles: ["patient"] },
  { id: "pt-practice",     label: "My Practice",   icon: "🌿", href: "/patient?tab=practice", roles: ["patient"] },
  { id: "pt-progress",     label: "My Progress",   icon: "📈", href: "/patient?tab=progress", roles: ["patient"] },

  // ── Clinician Navigation (Master Prompt 7 canonical surfaces)
  { id: "dr-desk",         label: "Clinical Desk",          icon: "🩺", href: "/doctor",                   roles: ["doctor"] },
  { id: "dr-p360",         label: "Patient 360",            icon: "👥", href: "/doctor/patients",          roles: ["doctor"] },
  { id: "dr-care-plans",   label: "Care Plans",             icon: "📋", href: "/doctor?tab=treatment",     roles: ["doctor"] },
  { id: "dr-formulations", label: "Formulations (Nuskha)",  icon: "📜", href: "/doctor/nuskha",            roles: ["doctor"] },
  { id: "dr-hakeem",       label: "Hakeem Sahab Copilot",   icon: "🤖", href: "/doctor/hakeem-sahab",      roles: ["doctor"] },
  { id: "dr-pharm-dx",     label: "Pharmacy & Diagnostics", icon: "🔬", href: "/doctor?tab=investigations",roles: ["doctor"] },
  { id: "dr-outcomes",     label: "Outcomes & Follow-up",   icon: "📈", href: "/doctor/follow-ups",        roles: ["doctor"] },

  // ── Reception Navigation (Canonical 4 items)
  { id: "rec-today",       label: "Reception Desk",icon: "🏥", href: "/reception",           roles: ["receptionist"] },
  { id: "rec-appts",       label: "Appointments", icon: "📅", href: "/receptionist/appointments", roles: ["receptionist"] },
  { id: "rec-queue",       label: "Token Queue",  icon: "📋", href: "/receptionist/queue",  roles: ["receptionist"] },
  { id: "rec-patients",    label: "Patient Intake",icon: "👥", href: "/receptionist?tab=register", roles: ["receptionist"] },

  // ── Pharmacy Navigation (Canonical 4 items)
  { id: "ph-rx",           label: "Prescriptions (FEFO)", icon: "📜", href: "/pharmacy",            roles: ["pharmacy"] },
  { id: "ph-dispense",     label: "Dispensing Desk",      icon: "💊", href: "/pharmacy/dispensing", roles: ["pharmacy"] },
  { id: "ph-inventory",    label: "Dispensary Inventory", icon: "📦", href: "/pharmacy/inventory",  roles: ["pharmacy"] },
  { id: "ph-catalog",      label: "Canonical Catalog 16", icon: "🌿", href: "/pharmacy/catalog-16", roles: ["pharmacy"] },

  // ── Nurse Navigation (Canonical 4 items)
  { id: "nr-station",      label: "Nurse Station", icon: "🏥", href: "/nurse",              roles: ["nurse"] },
  { id: "nr-queue",        label: "OPD Queue",     icon: "📋", href: "/doctor/queue",       roles: ["nurse"] },
  { id: "nr-patients",     label: "Inpatient Beds",icon: "👥", href: "/patient",            roles: ["nurse"] },
  { id: "nr-messages",     label: "Messages",      icon: "💬", href: "/messages",           roles: ["nurse"] },

  // ── Manufacturing Navigation
  { id: "mfg-ebmr",        label: "eBMR Production", icon: "🏭", href: "/manufacturing",         roles: ["manufacturing"] },
  { id: "mfg-batches",     label: "Batch Records",   icon: "📦", href: "/manufacturing/batches", roles: ["manufacturing"] },
  { id: "mfg-lab",         label: "QC Analytical Lab",icon: "🔬", href: "/manufacturing/lab",     roles: ["manufacturing"] },
  { id: "mfg-inventory",   label: "Inventory Sync",  icon: "🌿", href: "/pharmacy/inventory",   roles: ["manufacturing"] },

  // ── Research Navigation (Master Prompt 5 canonical surfaces)
  { id: "res-workspace",   label: "Research Workspace",   icon: "📑", href: "/research/workspace",              roles: ["research"] },
  { id: "res-evidence",    label: "Evidence (RWE)",        icon: "🔬", href: "/research/evidence",               roles: ["research"] },
  { id: "res-experiments", label: "Experiments & Trials",  icon: "📊", href: "/research/clinical-research",      roles: ["research"] },
  { id: "res-validation",  label: "Validation Audit",      icon: "🏛️", href: "/research/knowledge-validation",   roles: ["research"] },
  { id: "res-memory",      label: "Scientific Memory",     icon: "🌐", href: "/research/knowledge-intelligence", roles: ["research"] },

  // ── Administration (Master Prompt: Global Control Plane)
  { id: "adm-control",     label: "ZAYVORA Control Plane", icon: "🛡️", href: "/admin",               roles: ["admin"] },
  { id: "adm-users",       label: "Identity & RBAC",       icon: "👥", href: "/admin/users",         roles: ["admin"] },
  { id: "adm-health",      label: "System Health & Safety",icon: "🏥", href: "/admin/health",        roles: ["admin"] },
  { id: "adm-audit",       label: "Part 11 Audit Logs",    icon: "📋", href: "/admin/audit",         roles: ["admin"] },
  { id: "adm-config",      label: "Platform Configuration",icon: "⚙️", href: "/settings",            roles: ["admin"] },
];

interface SidebarProps {
  role?: UserRole;
  collapsed?: boolean;
  onToggle?: () => void;
}

export function Sidebar({ role = "doctor", collapsed = false, onToggle }: SidebarProps) {
  const pathname = usePathname();

  const visibleItems = NAV_ITEMS.filter((item) => item.roles.includes(role));

  const roleTitle = {
    doctor: "Clinician Cockpit",
    patient: "Patient Portal",
    receptionist: "Reception Desk",
    pharmacy: "Pharmacy OS",
    admin: "Admin Console",
    manufacturing: "Manufacturing OS",
    research: "Research Cloud",
    knowledge: "Knowledge Centre",
    nurse: "Nurse Station",
    website: "Public Portal",
  }[role] || "Workspace";

  return (
    <aside
      className={`bg-[var(--bg-surface)] border-r border-[var(--border-default)] flex flex-col transition-all duration-200 shrink-0 ${
        collapsed ? "w-16" : "w-60"
      } hidden md:flex`}
      aria-label={`${roleTitle} Navigation`}
    >
      {/* Header */}
      <div className="p-3 border-b border-[var(--border-default)] flex items-center justify-between min-h-[48px]">
        {!collapsed && (
          <span className="text-[11px] font-bold text-emerald-500 uppercase tracking-wider">
            {roleTitle}
          </span>
        )}
        <button
          type="button"
          onClick={onToggle}
          className="p-1.5 rounded-lg hover:bg-[var(--bg-elevated)] text-[var(--text-muted)] hover:text-[var(--text-primary)] transition ml-auto focus:outline-none focus:ring-2 focus:ring-emerald-500"
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? "▶" : "◀"}
        </button>
      </div>

      {/* Navigation */}
      <nav className="p-2 space-y-1 flex-1 overflow-y-auto" aria-label="Workspace navigation">
        {visibleItems.map((item) => {
          const isActive =
            pathname === item.href ||
            (item.href !== "/patient" && item.href !== "/doctor" && item.href !== "/admin" && pathname?.startsWith(item.href));

          return (
            <Link
              key={item.id}
              href={item.href}
              aria-current={isActive ? "page" : undefined}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                isActive
                  ? "bg-emerald-950/50 text-emerald-400 border border-emerald-500/40 font-semibold shadow-sm"
                  : "text-[var(--text-secondary)] hover:bg-[var(--bg-elevated)] hover:text-[var(--text-primary)]"
              }`}
              title={collapsed ? item.label : undefined}
            >
              <span className="text-base shrink-0 select-none">{item.icon}</span>
              {!collapsed && <span className="truncate">{item.label}</span>}
              {!collapsed && item.badge && (
                <span className="ml-auto text-[10px] bg-emerald-600 text-white px-2 py-0.5 rounded-full font-bold">
                  {item.badge}
                </span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Footer Support Links */}
      <div className="p-2 border-t border-[var(--border-default)] space-y-0.5 text-xs">
        <Link
          href="/faq"
          className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-elevated)] transition"
        >
          <span>❓</span>
          {!collapsed && <span>Help & Support</span>}
        </Link>
        <Link
          href="/admin/health"
          className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-elevated)] transition"
        >
          <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block ml-1 mr-0.5"></span>
          {!collapsed && <span>System Status</span>}
        </Link>
      </div>
    </aside>
  );
}
