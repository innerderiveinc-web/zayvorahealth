"use client";

import React from "react";
import { AppShell } from "@/components/AppShell";

export function PharmacistShell({ children }: { children: React.ReactNode }) {
  return (
    <AppShell activeRole="pharmacy" currentFacility="Central Dispensary & Mudabbar Compound Lab">
      {children}
    </AppShell>
  );
}
