import React from "react";
import Link from "next/link";

export default function ProgramDetailPage({ params }: { params: { slug: string } }) {
  return (
    <div className="min-h-screen bg-[var(--bg-base)]">
      <nav className="border-b border-[var(--border-default)] px-6 py-4 flex items-center justify-between max-w-7xl mx-auto">
        <Link href="/website" className="font-bold text-[var(--text-primary)] text-lg">ZAYVORA Health™</Link>
        <Link href="/website/programs" className="text-sm text-[var(--text-muted)] hover:text-[var(--text-primary)]">← Programs</Link>
      </nav>
      <main className="max-w-3xl mx-auto px-6 py-12">
        <div className="text-xs text-[var(--text-muted)] mb-6 font-mono">/programs/{params.slug}</div>
        <h1 className="text-3xl font-bold text-[var(--text-primary)] mb-4 capitalize">{params.slug.replace(/-/g," ")} Program</h1>
        <p className="text-[var(--text-muted)] text-sm mb-6">
          Full program details are being developed as part of ZAYVORA Health Products™ Phase 2.
        </p>
        <Link href="/patient/book" className="zv-btn-primary px-6 py-3 inline-flex">Book Consultation</Link>
      </main>
    </div>
  );
}
