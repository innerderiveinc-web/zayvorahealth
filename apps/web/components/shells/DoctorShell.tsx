"use client";

import React from "react";
import { AppShell } from "@/components/AppShell";

export function DoctorShell({ children }: { children: React.ReactNode }) {
  return (
    <AppShell activeRole="doctor" currentFacility="Central Integrative Clinical Facility — Room 3">
      {children}
    </AppShell>
  );
}
