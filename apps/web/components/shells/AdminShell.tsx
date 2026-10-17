"use client";

import React from "react";
import { AppShell } from "@/components/AppShell";

export function AdminShell({ children }: { children: React.ReactNode }) {
  return (
    <AppShell activeRole="admin" currentFacility="ZAYVORA System Administration & 21 CFR 11 Governance">
      {children}
    </AppShell>
  );
}
