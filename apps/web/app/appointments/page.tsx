"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";

export default function AppointmentsRedirectPage() {
  const router = useRouter();

  useEffect(() => {
    router.replace("/book");
  }, [router]);

  return (
    <PublicWebsiteShell>
      <div className="min-h-[60vh] flex flex-col items-center justify-center text-center p-8 bg-[#FAFAF7]">
        <div className="w-12 h-12 rounded-2xl bg-[#E8F5E9] flex items-center justify-center text-[#1B4332] mb-3">
          <HealthcareIcon name="calendar" className="w-6 h-6 text-[#2D6A4F]" />
        </div>
        <h2 className="text-xl font-bold text-[#0F172A] mb-1">Redirecting to Booking Gateway</h2>
        <p className="text-xs text-[#64748B] max-w-sm mb-4">
          Routing you to the canonical clinical appointment booking gateway at <code className="text-[#1B4332]">/book</code>...
        </p>
        <Link
          href="/book"
          className="px-5 py-2.5 rounded-xl bg-[#1B4332] text-white text-xs font-semibold hover:bg-[#2D6A4F] transition"
        >
          Click here to continue
        </Link>
      </div>
    </PublicWebsiteShell>
  );
}
