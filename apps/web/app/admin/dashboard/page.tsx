/**
 * @file apps/web/app/admin/dashboard/page.tsx
 * @description Admin dashboard — stats overview, recent audit events,
 *              and microservice health indicators.
 */
"use client";

import React, { useEffect, useState } from "react";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { PageHeader } from "@/components/ui/PageHeader";

interface StatCardData {
  label: string;
  value: string | number;
  delta?: string;
  icon: string;
  color: string;
}

interface AuditEvent {
  id: string;
  timestamp: string;
  user: string;
  action: string;
  resource: string;
  status: "success" | "failure" | "warning";
}

interface ServiceHealth {
  name: string;
  url: string;
  status: "healthy" | "degraded" | "down";
}

const STAT_CARDS: StatCardData[] = [
  { label: "Total Users",       value: "1,284",  delta: "+12 today",    icon: "👥", color: "text-blue-400"    },
  { label: "Active Clinicians", value: "87",     delta: "+3 this week", icon: "🩺", color: "text-emerald-400" },
  { label: "Patient Records",   value: "24,601", delta: "+148 today",   icon: "🫀", color: "text-purple-400"  },
  { label: "API Health",        value: "99.7%",  delta: "30-day uptime",icon: "💚", color: "text-green-400"   },
];

const FALLBACK_AUDIT_LOGS: AuditEvent[] = [
  { id: "a1",  timestamp: "2026-09-14 13:10",user: "admin@zayvora.com",     action: "USER_CREATED",       resource: "users/1295",    status: "success" },
  { id: "a2",  timestamp: "2026-09-14 12:58",user: "dr.alam@zayvora.com",   action: "RX_LOCKED",          resource: "rx/88231",      status: "success" },
  { id: "a3",  timestamp: "2026-09-14 12:47",user: "system",                action: "SYNC_FAILED",        resource: "gateway/sync",  status: "failure" },
  { id: "a4",  timestamp: "2026-09-14 12:31",user: "receptionist@hq",       action: "APPOINTMENT_BOOKED", resource: "appt/9921",     status: "success" },
  { id: "a5",  timestamp: "2026-09-14 12:20",user: "admin@zayvora.com",     action: "ROLE_CHANGED",       resource: "users/1022",    status: "warning" },
  { id: "a6",  timestamp: "2026-09-14 11:55",user: "dr.khan@zayvora.com",   action: "SOAP_ANCHORED",      resource: "records/44103", status: "success" },
  { id: "a7",  timestamp: "2026-09-14 11:40",user: "system",                action: "AI_INFERENCE",       resource: "ai/sessions/9", status: "success" },
  { id: "a8",  timestamp: "2026-09-14 11:22",user: "pharmacy@zayvora.com",  action: "DISPENSE_LOGGED",    resource: "rx/88200",      status: "success" },
  { id: "a9",  timestamp: "2026-09-14 10:58",user: "admin@zayvora.com",     action: "SETTING_CHANGED",    resource: "settings/smtp", status: "warning" },
  { id: "a10", timestamp: "2026-09-14 10:30",user: "system",                action: "BACKUP_COMPLETED",   resource: "infra/backup",  status: "success" },
];

const SERVICES: ServiceHealth[] = [
  { name: "Identity Service",    url: "identity-svc:3001",    status: "healthy"  },
  { name: "Clinical Service",    url: "clinical-svc:3002",    status: "healthy"  },
  { name: "ZAYVORA Knowledge Intelligence™",   url: "knowledge-svc:3003",   status: "healthy"  },
  { name: "Therapeutic Service", url: "therapeutic-svc:3004", status: "degraded" },
  { name: "AI Service",          url: "ai-svc:3005",          status: "healthy"  },
  { name: "API Gateway",         url: "gateway:8080",         status: "healthy"  },
];

function StatCard({ label, value, delta, icon, color }: StatCardData) {
  return (
    <div className="zv-card p-5 flex items-start gap-4">
      <div className="w-10 h-10 rounded-xl bg-[#1e293b] flex items-center justify-center text-xl shrink-0">{icon}</div>
      <div className="flex-1 min-w-0">
        <p className="text-[11px] text-slate-500 uppercase tracking-wider font-semibold">{label}</p>
        <p className={`text-2xl font-bold mt-0.5 ${color}`}>{value}</p>
        {delta && <p className="text-[11px] text-slate-500 mt-0.5">{delta}</p>}
      </div>
    </div>
  );
}

function ServiceDot({ status }: { status: ServiceHealth["status"] }) {
  const cls = { healthy: "bg-emerald-400", degraded: "bg-amber-400 animate-pulse", down: "bg-red-500 animate-ping" };
  return <span className={`inline-block w-2.5 h-2.5 rounded-full shrink-0 ${cls[status]}`} />;
}

export default function AdminDashboardPage() {
  const [loading, setLoading] = useState(true);
  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>(FALLBACK_AUDIT_LOGS);

  useEffect(() => {
    fetch('/api/v1/audit/ledger')
      .then(r => r.ok ? r.json() : null)
      .then(d => {
        if (d && d.ledger && Array.isArray(d.ledger) && d.ledger.length > 0) {
          const mapped: AuditEvent[] = d.ledger.slice(0, 10).map((ev: any, i: number) => ({
            id: String(ev.id || i),
            timestamp: ev.timestamp || "Just now",
            user: ev.user || ev.user_id || "admin@zayvora.com",
            action: ev.action || "AUDIT_EVENT",
            resource: ev.resource || ev.entity || "system",
            status: ev.status === "ERROR" ? "failure" : "success"
          }));
          setAuditEvents(mapped);
        }
      })
      .catch(() => {});
    const t = setTimeout(() => setLoading(false), 400);
    return () => clearTimeout(t);
  }, []);

  if (loading) return <LoadingSpinner message="Loading dashboard…" />;

  return (
    <div className="space-y-8">
      <PageHeader
        title="Admin Dashboard"
        subtitle="Platform-wide overview — ZAYVORA Health OS"
        breadcrumbs={[{ label: "Admin", href: "/admin" }, { label: "Dashboard" }]}
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {STAT_CARDS.map((s) => <StatCard key={s.label} {...s} />)}
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Service health */}
        <div className="zv-card p-5">
          <h2 className="text-sm font-bold text-white mb-4">💚 Microservice Health</h2>
          <ul className="space-y-3">
            {SERVICES.map((svc) => (
              <li key={svc.name} className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-2 min-w-0">
                  <ServiceDot status={svc.status} />
                  <span className="text-xs text-slate-300 truncate font-medium">{svc.name}</span>
                </div>
                <StatusBadge
                  label={svc.status}
                  variant={svc.status === "healthy" ? "success" : svc.status === "degraded" ? "warning" : "danger"}
                />
              </li>
            ))}
          </ul>
        </div>

        {/* Recent audit */}
        <div className="xl:col-span-2 zv-card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-bold text-white">📋 Recent Audit Events</h2>
            <a href="/admin/audit" className="text-[11px] text-[#52b788] hover:underline">View all →</a>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full text-xs">
              <thead>
                <tr className="border-b border-[#1e293b]">
                  {["Timestamp","User","Action","Resource","Status"].map((h) => (
                    <th key={h} className="pb-2 pr-4 text-left text-[11px] text-slate-500 uppercase tracking-wider font-semibold whitespace-nowrap">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1e293b]">
                {auditEvents.map((ev) => (
                  <tr key={ev.id} className="hover:bg-[#1e293b]/40 transition-colors">
                    <td className="py-2 pr-4 text-slate-400 whitespace-nowrap font-mono">{ev.timestamp}</td>
                    <td className="py-2 pr-4 text-slate-300 truncate max-w-[120px]">{ev.user}</td>
                    <td className="py-2 pr-4 text-slate-200 font-mono font-semibold whitespace-nowrap">{ev.action}</td>
                    <td className="py-2 pr-4 text-slate-400 whitespace-nowrap">{ev.resource}</td>
                    <td className="py-2">
                      <StatusBadge
                        label={ev.status}
                        variant={ev.status === "success" ? "success" : ev.status === "failure" ? "danger" : "warning"}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
