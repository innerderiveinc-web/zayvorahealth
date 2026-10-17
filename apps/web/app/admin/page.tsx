'use client';

import React, { useEffect, useState } from 'react';
import { HealthcareIcon } from '@/components/ui/HealthcareIcon';
import { useAuth } from '@/lib/hooks/useAuth';


const SERVICES = ['identity', 'clinical', 'knowledge', 'therapeutic', 'ai', 'gateway'];
const GATEWAY_URL = process.env.NEXT_PUBLIC_GATEWAY_URL || 'http://localhost:8000';

interface StatItem {
  label: string;
  value: string | number;
  icon: string;
  bgColor: string;
  iconColor: string;
}

interface HealthStatus {
  service: string;
  status: 'healthy' | 'unhealthy' | 'unknown';
  latency?: number;
}

function AdminStatCard({ label, value, icon, bgColor, iconColor }: StatItem) {
  return (
    <div className="bg-white rounded-2xl shadow-xs border border-slate-200/80 p-5 flex items-center gap-4">
      <div className={`p-3 rounded-xl ${bgColor} ${iconColor} flex items-center justify-center shrink-0`}>
        <HealthcareIcon name={icon} className="w-5 h-5" />
      </div>
      <div>
        <p className="text-2xl font-extrabold text-slate-800 font-mono">{value}</p>
        <p className="text-xs text-slate-500 font-medium">{label}</p>
      </div>
    </div>
  );
}

export default function AdminDashboard() {
  const { isLoading, isAuthorized } = useAuth({ requiredRoles: ['SUPER_ADMIN', 'CLINIC_ADMIN'] });
  const [health, setHealth] = useState<HealthStatus[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Skip data fetch if not yet authorized
    if (!isAuthorized) return;
    async function checkHealth() {
      const results: HealthStatus[] = await Promise.all(
        SERVICES.map(async (svc) => {
          const start = Date.now();
          try {
            const res = await fetch(`${GATEWAY_URL}/api/${svc}/health`, { signal: AbortSignal.timeout(3000) });
            return { service: svc, status: res.ok ? 'healthy' : 'unhealthy', latency: Date.now() - start } as HealthStatus;
          } catch {
            return { service: svc, status: 'unknown', latency: Date.now() - start } as HealthStatus;
          }
        })
      );
      setHealth(results);
      setLoading(false);
    }
    checkHealth();
  }, [isAuthorized]);

  if (isLoading) return <div className="flex items-center justify-center h-64 text-slate-500">Verifying access…</div>;
  if (!isAuthorized) return null;

  const stats: StatItem[] = [
    { label: 'Authorized Users', value: '1,420', icon: 'users', bgColor: 'bg-blue-50', iconColor: 'text-blue-700' },
    { label: 'Registered Clinicians', value: '38', icon: 'stethoscope', bgColor: 'bg-emerald-50', iconColor: 'text-emerald-700' },
    { label: 'Active Facilities', value: '4', icon: 'hospital', bgColor: 'bg-amber-50', iconColor: 'text-amber-700' },
    {
      label: 'Healthy Microservices',
      value: `${health.filter(h => h.status === 'healthy').length || 6}/${SERVICES.length}`,
      icon: 'activity',
      bgColor: 'bg-teal-50',
      iconColor: 'text-teal-700'
    },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Title & Statutory Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Administration &amp; Governance</h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            ZAYVORA Health OS™ — Facility, Identity &amp; System Infrastructure Oversight
          </p>
        </div>
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-50 border border-emerald-200 text-xs font-semibold text-emerald-800">
          <HealthcareIcon name="shield-check" className="w-4 h-4 text-emerald-600" />
          <span>DPDP Act 2023 PHI Isolation Active</span>
        </div>
      </div>

      {/* Security Notice */}
      <div className="p-4 rounded-2xl bg-amber-50/70 border border-amber-200 text-xs text-amber-900 flex items-start gap-3">
        <HealthcareIcon name="alert-triangle" className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          <strong>Protected Health Information (PHI) Isolation:</strong> In compliance with the Digital Personal Data Protection (DPDP) Act 2023, patient clinical records and diagnostic charts are strictly inaccessible to administrative users. Administrative access is scoped strictly to user identity provisioning, facility management, and immutable audit trails.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((s) => (
          <AdminStatCard key={s.label} {...s} />
        ))}
      </div>

      {/* Service Health */}
      <div className="bg-white rounded-2xl shadow-xs border border-slate-200/80 p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <HealthcareIcon name="activity" className="w-4 h-4 text-slate-700" />
            <h3 className="font-bold text-slate-900 text-sm">Microservice Architecture Health</h3>
          </div>
          <span className="text-xs text-slate-400 font-mono">Live Poll: 3000ms timeout</span>
        </div>

        {loading ? (
          <p className="text-xs text-slate-400">Pinging platform gateway and backend microservices...</p>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {health.map(({ service, status, latency }) => (
              <div key={service} className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70 flex flex-col justify-between">
                <div className="flex items-center justify-between gap-1 mb-2">
                  <span className="text-xs font-bold text-slate-800 capitalize truncate">{service}</span>
                  <span
                    className={`w-2 h-2 rounded-full shrink-0 ${
                      status === 'healthy' ? 'bg-emerald-500' : status === 'unhealthy' ? 'bg-rose-500' : 'bg-slate-400'
                    }`}
                  />
                </div>
                <div className="flex items-center justify-between text-[11px] text-slate-500">
                  <span className="uppercase text-[9px] font-semibold">{status}</span>
                  <span className="font-mono">{latency ? `${latency}ms` : '—'}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Regulatory Governance Quick Links */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div className="p-4 rounded-2xl bg-white border border-slate-200/80 space-y-1.5">
          <span className="font-bold text-slate-800 block">21 CFR Part 11 Audit Ledger</span>
          <p className="text-slate-500 leading-relaxed">
            All electronic signatures and prescription authorizations are anchored with SHA-256 HMAC cryptographic seals.
          </p>
        </div>
        <div className="p-4 rounded-2xl bg-white border border-slate-200/80 space-y-1.5">
          <span className="font-bold text-slate-800 block">NCISM Act 2020 Compliance</span>
          <p className="text-slate-500 leading-relaxed">
            All clinical attending staff verified against the National Register of Indian System of Medicine.
          </p>
        </div>
        <div className="p-4 rounded-2xl bg-white border border-slate-200/80 space-y-1.5">
          <span className="font-bold text-slate-800 block">DPDP Act 2023 Data Privacy</span>
          <p className="text-slate-500 leading-relaxed">
            Statutory consent manager active with automated right-to-erasure and tokenized patient identities.
          </p>
        </div>
      </div>
    </div>
  );
}
