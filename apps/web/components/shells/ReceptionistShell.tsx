"use client";

import React from "react";
import { AppShell } from "@/components/AppShell";

export function ReceptionistShell({ children }: { children: React.ReactNode }) {
  return (
    <AppShell activeRole="clinic" currentFacility="OPD Intake & Triage Desk — Counter 1">
      {children}
    </AppShell>
  );
}
