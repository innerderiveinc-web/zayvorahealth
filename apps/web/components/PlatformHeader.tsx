"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { clearSession, loadSession } from "@/lib/session";
import type { TokenResponse } from "@/lib/identityApi";

export function PlatformHeader() {
  const pathname = usePathname();
  const router = useRouter();
  const [session, setSession] = useState<TokenResponse | null>(null);

  useEffect(() => {
    setSession(loadSession());
  }, []);

  function handleSignOut() {
    clearSession();
    router.push("/");
  }

  const workspaces = [
    { label: "Public", href: "/", icon: "🌐" },
    { label: "Website (25p)", href: "/website", icon: "🏛️" },
    { label: "Herbals Store", href: "/website/herbals", icon: "🌿" },
    { label: "Patient", href: "/patient", icon: "👤" },
    { label: "Doctor", href: "/doctor", icon: "🩺" },
    { label: "Clinic", href: "/clinic", icon: "🏥" },
    { label: "Pharmacy", href: "/pharmacy", icon: "💊" },
    { label: "Research", href: "/research", icon: "🔬" },
    { label: "Manufacturing", href: "/manufacturing", icon: "🏭" },
    { label: "Admin", href: "/admin", icon: "🛡️" },
    { label: "Knowledge", href: "/knowledge", icon: "📖" },
    { label: "AI Copilot", href: "/ai", icon: "🧠" },
  ];

  return (
    <header className="border-b border-[var(--border)] bg-[var(--panel)] sticky top-0 z-40 px-4 py-2.5">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
        
        {/* Brand & Philosophy */}
        <div className="flex items-center gap-3">
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 rounded-lg bg-[var(--emerald)] flex items-center justify-center text-white font-bold text-base shadow-sm group-hover:opacity-90">
              Z
            </div>
            <div>
              <span className="font-bold tracking-tight text-base zv-brand-title block leading-none">
                ZAYVORA HEALTH OS™
              </span>
              <span className="text-[10px] text-[var(--muted)] block tracking-wider uppercase">
                Ancient Wisdom · Modern Science · Intelligent Care
              </span>
            </div>
          </Link>
          <span className="hidden sm:inline-block text-[10px] font-semibold px-2 py-0.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400">
            v5.0-Enterprise
          </span>
        </div>

        {/* Global Workspace Navigation */}
        <nav className="flex items-center gap-1 overflow-x-auto py-1 max-w-full">
          {workspaces.map((ws) => {
            const isActive = pathname === ws.href || (ws.href !== "/" && pathname?.startsWith(ws.href));
            return (
              <Link
                key={ws.href}
                href={ws.href}
                className={`px-2.5 py-1 rounded-md text-xs font-medium transition-colors flex items-center gap-1.5 whitespace-nowrap ${
                  isActive
                    ? "bg-[var(--emerald)] text-white shadow-xs font-semibold"
                    : "text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--elevated)]"
                }`}
              >
                <span>{ws.icon}</span>
                <span>{ws.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Live Hardware Telemetry Indicators */}
        <div className="hidden lg:flex items-center gap-2 text-[10px] bg-[var(--elevated)] px-2.5 py-1 rounded-lg border border-[var(--border)]">
          <span className="flex items-center gap-1 text-emerald-400 font-semibold" title="PPG Pulse Sensor Streaming at 100Hz">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            🩺 Nabz: 100Hz
          </span>
          <span className="text-[var(--border)]">|</span>
          <span className="flex items-center gap-1 text-teal-300 font-semibold" title="Multispectral Lisan Camera Ready">
            👅 Lisan Cam
          </span>
          <span className="text-[var(--border)]">|</span>
          <span className="flex items-center gap-1 text-cyan-300 font-semibold" title="Dispensary Cold-Chain Temperature">
            🌡️ 19.4°C (FEFO)
          </span>
        </div>

        {/* User Session & Status */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 text-xs text-[var(--muted)]">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="hidden md:inline">Live Mesh</span>
          </div>

          {session ? (
            <div className="flex items-center gap-2">
              <span className="text-xs font-medium text-[var(--gold-soft)] bg-[var(--elevated)] px-2.5 py-1 rounded border border-[var(--border)]">
                {session.role || "Clinician"}
              </span>
              <button
                onClick={handleSignOut}
                className="text-xs px-2 py-1 rounded hover:bg-[var(--elevated)] text-[var(--muted)] hover:text-white"
              >
                Sign Out
              </button>
            </div>
          ) : (
            <Link
              href="/signup"
              className="text-xs font-semibold px-3 py-1 rounded bg-[var(--elevated)] hover:bg-[var(--border)] text-[var(--text)] border border-[var(--border)]"
            >
              Sign In
            </Link>
          )}
        </div>

      </div>
    </header>
  );
}
