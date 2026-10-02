'use client';

import React, { useEffect, useState, useCallback } from 'react';

const SERVICES = [
  { name: 'identity', port: 8001, label: 'Identity Service' },
  { name: 'clinical', port: 8002, label: 'Clinical Service' },
  { name: 'knowledge', port: 8003, label: 'ZAYVORA Knowledge Intelligence™' },
  { name: 'therapeutic', port: 8004, label: 'Therapeutic Service' },
  { name: 'ai', port: 8005, label: 'AI Service' },
  { name: 'gateway', port: 8000, label: 'API Gateway' },
];

const GATEWAY = process.env.NEXT_PUBLIC_GATEWAY_URL || 'http://localhost:8000';

interface SvcHealth {
  name: string; label: string; status: 'healthy' | 'unhealthy' | 'checking';
  latency: number | null; lastChecked: Date | null; details?: string;
}

export default function SystemHealthPage() {
  const [services, setServices] = useState<SvcHealth[]>(
    SERVICES.map(s => ({ ...s, status: 'checking', latency: null, lastChecked: null }))
  );

  const checkAll = useCallback(async () => {
    setServices(prev => prev.map(s => ({ ...s, status: 'checking' })));
    const updated = await Promise.all(
      SERVICES.map(async (svc) => {
        const start = Date.now();
        try {
          const res = await fetch(`${GATEWAY}/api/${svc.name}/health`, {
            signal: AbortSignal.timeout(4000),
          });
          const latency = Date.now() - start;
          let details = '';
          try { const d = await res.json(); details = d.status || ''; } catch {}
          return { ...svc, status: res.ok ? 'healthy' : 'unhealthy', latency, lastChecked: new Date(), details } as SvcHealth;
        } catch (err) {
          return { ...svc, status: 'unhealthy', latency: Date.now() - start, lastChecked: new Date(), details: 'Unreachable' } as SvcHealth;
        }
      })
    );
    setServices(updated);
  }, []);

  useEffect(() => { checkAll(); const id = setInterval(checkAll, 30000); return () => clearInterval(id); }, [checkAll]);

  const healthy = services.filter(s => s.status === 'healthy').length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-800">System Health</h2>
          <p className="text-sm text-gray-500 mt-1">{healthy}/{SERVICES.length} services healthy · Auto-refreshes every 30s</p>
        </div>
        <button onClick={checkAll} className="px-4 py-2 bg-[#2D6A4F] text-white rounded-lg text-sm font-medium hover:bg-[#1B4332] transition-colors">
          🔄 Check Now
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {services.map((svc) => (
          <div key={svc.name} className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="font-semibold text-gray-800">{svc.label}</h3>
                <p className="text-xs text-gray-400 mt-0.5">/{svc.name}</p>
              </div>
              <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                svc.status === 'healthy' ? 'bg-green-100 text-green-700' :
                svc.status === 'unhealthy' ? 'bg-red-100 text-red-700' :
                'bg-gray-100 text-gray-500'
              }`}>
                {svc.status === 'checking' ? '⏳ Checking' : svc.status === 'healthy' ? '✅ Healthy' : '❌ Down'}
              </span>
            </div>
            <div className="mt-4 space-y-1">
              <p className="text-sm text-gray-500">Response: <span className="font-medium text-gray-700">{svc.latency != null ? `${svc.latency}ms` : '—'}</span></p>
              <p className="text-sm text-gray-500">Last check: <span className="font-medium text-gray-700">{svc.lastChecked ? svc.lastChecked.toLocaleTimeString() : '—'}</span></p>
              {svc.details && <p className="text-xs text-gray-400 mt-1">{svc.details}</p>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
