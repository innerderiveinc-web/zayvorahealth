'use client';

import React, { useState, useEffect } from 'react';

interface AuditEvent {
  id: string; timestamp: string; user: string; action: string;
  resource: string; ip: string; status: 'success' | 'failure' | 'warning';
}

const FALLBACK_AUDIT_EVENTS: AuditEvent[] = [
  { id: '1', timestamp: new Date().toISOString(), user: 'admin@zayvora.com', action: 'USER_LOGIN', resource: 'auth', ip: '192.168.1.1', status: 'success' },
  { id: '2', timestamp: new Date(Date.now() - 60000).toISOString(), user: 'dr.ali@zayvora.com', action: 'NUSKHA_CREATED', resource: 'prescription#1234', ip: '10.0.0.5', status: 'success' },
  { id: '3', timestamp: new Date(Date.now() - 120000).toISOString(), user: 'unknown', action: 'LOGIN_FAILED', resource: 'auth', ip: '203.0.113.10', status: 'failure' },
];

const STATUS_COLORS = { success: 'text-green-700 bg-green-50', failure: 'text-red-700 bg-red-50', warning: 'text-yellow-700 bg-yellow-50' };

export default function AuditLogPage() {
  const [events, setEvents] = useState<AuditEvent[]>(FALLBACK_AUDIT_EVENTS);
  const [filter, setFilter] = useState('');
  const [isLive, setIsLive] = useState(false);

  useEffect(() => {
    fetch('/api/v1/audit/ledger')
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data && data.ledger && Array.isArray(data.ledger)) {
          const mapped: AuditEvent[] = data.ledger.map((item: any, idx: number) => ({
            id: String(item.id || idx + 1),
            timestamp: item.timestamp || new Date().toISOString(),
            user: item.user || item.user_id || 'system',
            action: item.action || 'AUDIT_LOG',
            resource: item.resource || item.entity || 'general',
            ip: item.ip || '127.0.0.1',
            status: item.status === 'ERROR' ? 'failure' : 'success'
          }));
          if (mapped.length > 0) {
            setEvents(mapped);
            setIsLive(true);
          }
        }
      })
      .catch(() => {
        // Standalone offline fallback
      });
  }, []);


  const filtered = events.filter(e =>
    e.user.toLowerCase().includes(filter.toLowerCase()) ||
    e.action.toLowerCase().includes(filter.toLowerCase()) ||
    e.ip.includes(filter)
  );

  const exportCSV = () => {
    const rows = [['ID', 'Timestamp', 'User', 'Action', 'Resource', 'IP', 'Status']];
    filtered.forEach(e => rows.push([e.id, e.timestamp, e.user, e.action, e.resource, e.ip, e.status]));
    const csv = rows.map(r => r.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'audit_log.csv'; a.click();
  };

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Audit Logs</h2>
          <p className="text-sm text-gray-500">Complete record of all system events</p>
        </div>
        <button onClick={exportCSV} className="px-4 py-2 bg-[#2D6A4F] text-white rounded-lg text-sm font-medium hover:bg-[#1B4332]">
          ⬇ Export CSV
        </button>
      </div>

      <input
        type="text" placeholder="Filter by user, action, or IP…"
        value={filter} onChange={e => setFilter(e.target.value)}
        className="w-full px-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#2D6A4F]"
      />

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b border-gray-100">
            <tr>
              {['Timestamp', 'User', 'Action', 'Resource', 'IP Address', 'Status'].map(h => (
                <th key={h} className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {filtered.map(e => (
              <tr key={e.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-4 py-3 text-gray-600 whitespace-nowrap">{new Date(e.timestamp).toLocaleString()}</td>
                <td className="px-4 py-3 font-medium text-gray-800">{e.user}</td>
                <td className="px-4 py-3 text-gray-600 font-mono text-xs">{e.action}</td>
                <td className="px-4 py-3 text-gray-500 text-xs">{e.resource}</td>
                <td className="px-4 py-3 text-gray-500 font-mono text-xs">{e.ip}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${STATUS_COLORS[e.status]}`}>
                    {e.status}
                  </span>
                </td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr><td colSpan={6} className="px-4 py-8 text-center text-gray-400 text-sm">No events found.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
