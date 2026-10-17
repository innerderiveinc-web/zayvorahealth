"use client";
import React from "react";
import { AppShell } from "@/components/AppShell";

const ROLES = [
  { name:"Super Admin",      users:2,  perms:["*"],                          desc:"Full platform access" },
  { name:"Doctor",           users:8,  perms:["clinical:read","clinical:write","nuskha:sign"], desc:"Clinical workspace" },
  { name:"Receptionist",     users:5,  perms:["reception:read","appointments:write"],          desc:"Queue and booking" },
  { name:"Pharmacist",       users:3,  perms:["pharmacy:read","dispensing:write"],             desc:"Dispensing and inventory" },
  { name:"Research Analyst", users:4,  perms:["research:read","cohorts:read"],                 desc:"Read-only research access" },
  { name:"Manufacturing",    users:3,  perms:["manufacturing:read","qc:write"],                desc:"QC and eBMR" },
  { name:"Patient",          users:247,perms:["patient:own"],                                 desc:"Patient self-service portal" },
];

export default function AdminRolesPage() {
  return (
    <AppShell activeRole="admin">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">🔐 Roles & Permissions</h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">RBAC matrix · ZAYVORA Health OS™</p>
          </div>
          <button className="zv-btn-primary text-sm px-4 py-2">+ Create Role</button>
        </div>
        <div className="space-y-3">
          {ROLES.map(r => (
            <div key={r.name} className="zv-card p-4 flex items-center gap-4">
              <div className="w-10 h-10 rounded-lg bg-[var(--primary-light)] flex items-center justify-center text-lg">🔐</div>
              <div className="flex-1">
                <div className="font-semibold text-sm text-[var(--text-primary)]">{r.name}</div>
                <div className="text-xs text-[var(--text-muted)] mt-0.5">{r.desc} · {r.users} users</div>
                <div className="flex gap-1 flex-wrap mt-1">
                  {r.perms.map(p => <span key={p} className="text-[10px] px-1.5 py-0.5 rounded bg-[var(--bg-elevated)] text-[var(--text-muted)] font-mono">{p}</span>)}
                </div>
              </div>
              <button className="zv-btn-secondary text-xs px-3 py-1.5">Edit</button>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
