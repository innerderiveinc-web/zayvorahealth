import React from "react";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";

export const metadata = {
  title: "ZAYVORA Health™ — Modern Unani Integrative Healthcare System",
  description: "Ancient Wisdom. Modern Science. Intelligent Care. Classical Unani Medicine integrated with contemporary biomedical intelligence, organ-axis clinical framework, and 21 CFR Part 11 governance.",
};

export default function WebsiteLayout({ children }: { children: React.ReactNode }) {
  return (
    <PublicWebsiteShell>
      {children}
    </PublicWebsiteShell>
  );
}
