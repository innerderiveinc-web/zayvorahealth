"use client";

import React from "react";
import { PublicHeader } from "@/components/PublicHeader";
import { PublicFooter } from "@/components/PublicFooter";
import { CookieConsentBanner } from "@/components/CookieConsentBanner";

export function PublicWebsiteShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col bg-[#FAFAF7] text-[#0F172A] antialiased selection:bg-[#2D6A4F] selection:text-white">
      <PublicHeader />
      <main className="flex-1">
        {children}
      </main>
      <PublicFooter />
      <CookieConsentBanner />
    </div>
  );
}
