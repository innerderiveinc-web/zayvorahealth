"use client";

import React from "react";
import { AppShell } from "@/components/AppShell";

export function EnterpriseOwnerShell({ children }: { children: React.ReactNode }) {
  return (
    <AppShell activeRole="enterprise" currentFacility="Enterprise Multi-Facility Network Headquarters">
      {children}
    </AppShell>
  );
}
