import React from "react";
import Link from "next/link";

export default function HerbalDetailPage({ params }: { params: { slug: string } }) {
  return (
    <div className="min-h-screen bg-[var(--bg-base)]">
      <nav className="border-b border-[var(--border-default)] px-6 py-4 flex items-center justify-between max-w-7xl mx-auto">
        <Link href="/website" className="font-bold text-[var(--text-primary)] text-lg">ZAYVORA Health™</Link>
        <Link href="/website/herbals" className="text-sm text-[var(--text-muted)] hover:text-[var(--text-primary)]">← Herbals</Link>
      </nav>
      <main className="max-w-3xl mx-auto px-6 py-12">
        <div className="text-xs text-[var(--text-muted)] mb-6 font-mono">/herbals/{params.slug}</div>
        <h1 className="text-3xl font-bold text-[var(--text-primary)] mb-4 capitalize">{params.slug.replace(/-/g," ")}</h1>
        <div className="zv-card p-4 mb-6 flex gap-3 items-start border-amber-500/30 bg-amber-500/10">
          <span className="text-amber-400">⚠</span>
          <p className="text-xs text-amber-300">
            This herbal product information is for educational purposes only. 
            Consult a qualified Hakeem or physician before use.
            ZAYVORA Health Products™ does not make therapeutic claims without clinical substantiation.
          </p>
        </div>
        <p className="text-[var(--text-muted)] text-sm">
          Full product details including ingredients, dosage, and safety profile are being developed under ZAYVORA Health Products™ Phase 2.
        </p>
      </main>
    </div>
  );
}
