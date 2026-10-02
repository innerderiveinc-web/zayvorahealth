'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { HealthcareIcon } from '@/components/ui/HealthcareIcon';

const NAV_ITEMS = [
  { href: '/admin', label: 'Governance Overview', icon: 'home' },
  { href: '/admin/users', label: 'Identity & Access', icon: 'users' },
  { href: '/admin/organizations', label: 'Facilities & Tenants', icon: 'hospital' },
  { href: '/admin/ai', label: 'AI Evaluation Lab', icon: 'activity' },
  { href: '/admin/audit', label: 'Audit Logs (Part 11)', icon: 'clipboard' },
  { href: '/admin/health', label: 'System Health', icon: 'shield-check' },
  { href: '/admin/settings', label: 'System Settings', icon: 'settings' },
];

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const handleLogout = () => {
    localStorage.removeItem('zayvora_token');
    router.push('/login');
  };

  return (
    <div className="flex h-screen bg-[#FAFAF7] font-sans">
      {/* Sidebar */}
      <aside
        className={`${sidebarOpen ? 'w-64' : 'w-16'} bg-[#2D6A4F] text-white flex flex-col transition-all duration-200 shadow-lg`}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-4 py-5 border-b border-[#1B4332]">
          <HealthcareIcon name="leaf" className="w-6 h-6 text-emerald-300 shrink-0" />
          {sidebarOpen && (
            <div>
              <p className="font-bold text-sm leading-tight tracking-wider">ZAYVORA</p>
              <p className="text-xs text-green-200">Governance Console</p>
            </div>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="ml-auto text-green-200 hover:text-white p-1 rounded hover:bg-[#1B4332]"
            aria-label="Toggle Sidebar"
          >
            <HealthcareIcon name={sidebarOpen ? "chevron-left" : "chevron-right"} className="w-4 h-4" />
          </button>
        </div>

        {/* Nav */}
        <nav className="flex-1 py-4 overflow-y-auto">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href || (item.href !== '/admin' && pathname?.startsWith(item.href));
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-4 py-3 text-sm font-medium transition-colors ${
                  isActive ? 'bg-[#1B4332] text-white' : 'text-green-100 hover:bg-[#1B4332] hover:text-white'
                }`}
              >
                <HealthcareIcon name={item.icon} className="w-4 h-4 shrink-0" />
                {sidebarOpen && <span>{item.label}</span>}
              </Link>
            );
          })}
        </nav>

        {/* Bottom */}
        <div className="p-4 border-t border-[#1B4332]">
          {sidebarOpen ? (
            <div className="flex items-center justify-between text-xs text-green-200">
              <span className="truncate">Admin Portal</span>
              <button
                onClick={handleLogout}
                className="text-red-300 hover:text-white font-medium"
              >
                Sign out
              </button>
            </div>
          ) : (
            <button
              onClick={handleLogout}
              className="text-xs text-red-300 hover:text-white flex justify-center w-full"
              title="Sign out"
            >
              <HealthcareIcon name="lock" className="w-4 h-4" />
            </button>
          )}
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 shadow-sm">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
              Governance &amp; Oversight Console
            </span>
          </div>
          <div className="flex items-center gap-4 text-sm text-gray-600">
            <span className="flex items-center gap-1.5 text-xs text-slate-500">
              <HealthcareIcon name="shield-check" className="w-4 h-4 text-emerald-600" />
              <span>DPDP 2023 Isolated Console</span>
            </span>
            <span className="w-8 h-8 rounded-full bg-[#2D6A4F] text-white flex items-center justify-center font-bold text-xs">
              AD
            </span>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
