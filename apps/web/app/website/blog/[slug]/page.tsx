import React from "react";
import Link from "next/link";

export default function BlogArticlePage({ params }: { params: { slug: string } }) {
  return (
    <div className="min-h-screen bg-[var(--bg-base)]">
      <nav className="border-b border-[var(--border-default)] px-6 py-4 flex items-center justify-between max-w-7xl mx-auto">
        <Link href="/website" className="font-bold text-[var(--text-primary)] text-lg">ZAYVORA Health™</Link>
        <Link href="/website/blog" className="text-sm text-[var(--text-muted)] hover:text-[var(--text-primary)]">← Blog</Link>
      </nav>
      <main className="max-w-3xl mx-auto px-6 py-12">
        <div className="text-xs text-[var(--text-muted)] mb-6 font-mono">/blog/{params.slug}</div>
        <h1 className="text-3xl font-bold text-[var(--text-primary)] mb-4">Article: {params.slug}</h1>
        <p className="text-[var(--text-muted)] text-sm">
          This blog article page is part of ZAYVORA Health OS™ Phase 2 content system.
          Full CMS integration is planned for the next development phase.
        </p>
      </main>
    </div>
  );
}
