import React from "react";
import Link from "next/link";

export default function DoctorProfilePage({ params }: { params: { slug: string } }) {
  return (
    <div className="min-h-screen bg-[var(--bg-base)]">
      <nav className="border-b border-[var(--border-default)] px-6 py-4 flex items-center justify-between max-w-7xl mx-auto">
        <Link href="/website" className="font-bold text-[var(--text-primary)] text-lg">ZAYVORA Health™</Link>
        <Link href="/website/doctors" className="text-sm text-[var(--text-muted)] hover:text-[var(--text-primary)]">← Our Doctors</Link>
      </nav>
      <main className="max-w-3xl mx-auto px-6 py-12">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 rounded-full bg-[var(--primary-light)] flex items-center justify-center text-2xl">👨‍⚕️</div>
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)] capitalize">{params.slug.replace(/-/g," ")}</h1>
            <p className="text-sm text-[var(--text-muted)]">Hakeem · ZAYVORA Matab™</p>
          </div>
        </div>
        <Link href="/patient/book" className="zv-btn-primary px-6 py-3 inline-flex">Book with This Doctor</Link>
      </main>
    </div>
  );
}
