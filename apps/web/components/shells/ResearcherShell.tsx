"use client";

import React from "react";
import { AppShell } from "@/components/AppShell";

export function ResearcherShell({ children }: { children: React.ReactNode }) {
  return (
    <AppShell activeRole="research" currentFacility="Clinical Research & Observational RWE Division">
      {children}
    </AppShell>
  );
}
