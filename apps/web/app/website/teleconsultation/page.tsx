import React from "react";
import Link from "next/link";

export default function TeleconsultationPage() {
  return (
    <div className="min-h-screen bg-[var(--bg-base)]">
      {/* Navigation placeholder */}
      <nav className="border-b border-[var(--border-default)] px-6 py-4 flex items-center justify-between max-w-7xl mx-auto">
        <Link href="/website" className="font-bold text-[var(--text-primary)] text-lg">ZAYVORA Health™</Link>
        <Link href="/patient/book" className="zv-btn-primary text-sm px-4 py-2">Book Consultation</Link>
      </nav>
      <main className="max-w-4xl mx-auto px-6 py-16 text-center">
        <div className="text-6xl mb-6">📱</div>
        <h1 className="text-4xl font-bold text-[var(--text-primary)] mb-4">Teleconsultation</h1>
        <p className="text-lg text-[var(--text-muted)] mb-8 max-w-2xl mx-auto">Book a video or voice consultation with a ZAYVORA Hakeem</p>
        <div className="flex gap-4 justify-center">
          <Link href="/patient/book" className="zv-btn-primary px-6 py-3">Book a Consultation</Link>
          <Link href="/website/about" className="zv-btn-secondary px-6 py-3">Learn More</Link>
        </div>
      </main>
    </div>
  );
}
