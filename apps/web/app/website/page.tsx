"use client";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export default function ZayvoraHealthLegacyRedirect() {
  const router = useRouter();

  useEffect(() => {
    router.replace("/");
  }, [router]);

  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center text-center p-8 bg-[#FAFAF7]">
      <div className="w-16 h-16 rounded-2xl bg-[#E8F5E9] border border-[#C8E6C9] flex items-center justify-center text-[#1B4332] mb-4 shadow-sm">
        <HealthcareIcon name="shield-check" className="w-8 h-8 text-[#2D6A4F]" />
      </div>
      <h1 className="text-2xl font-bold text-[#0F172A] mb-2">Redirecting to ZAYVORA Health™</h1>
      <p className="text-[#475569] max-w-md mb-6 text-sm leading-relaxed">
        The public web experience is consolidated at the root institutional portal. Redirecting you automatically...
      </p>
      <Link
        href="/"
        className="px-6 py-3 rounded-xl bg-[#1B4332] text-white font-semibold text-sm hover:bg-[#2D6A4F] transition shadow-sm inline-flex items-center gap-2"
      >
        <span>Continue to Institutional Homepage</span>
        <HealthcareIcon name="arrow-right" className="w-4 h-4 text-white" />
      </Link>
    </div>
  );
}
