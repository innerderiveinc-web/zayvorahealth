"use client";

import React from "react";
import { AppShell } from "@/components/AppShell";

export function PatientShell({ children }: { children: React.ReactNode }) {
  return (
    <AppShell activeRole="patient" currentFacility="ZAYVORA Patient 360 Portal">
      {children}
    </AppShell>
  );
}
