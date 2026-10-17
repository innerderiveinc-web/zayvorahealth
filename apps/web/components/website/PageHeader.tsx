import React from "react";
import Link from "next/link";

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface PageHeaderProps {
  badge?: string;
  title: string;
  subtitle: string;
  breadcrumbs?: BreadcrumbItem[];
  primaryCta?: { label: string; href: string };
  secondaryCta?: { label: string; href: string };
}

export function PageHeader({
  badge,
  title,
  subtitle,
  breadcrumbs = [],
  primaryCta,
  secondaryCta
}: PageHeaderProps) {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-[#0A0F1D] via-[#0D1527] to-[#0A0F1D] border-b border-[#1E293B] pt-12 pb-16 px-4 sm:px-6 lg:px-8">
      {/* Background Decorative Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-full overflow-hidden pointer-events-none -z-10">
        <div className="absolute -top-24 left-1/4 w-96 h-96 bg-[#0D9488]/10 rounded-full blur-3xl" />
        <div className="absolute top-10 right-1/4 w-80 h-80 bg-[#2D6A4F]/15 rounded-full blur-3xl" />
      </div>

      <div className="max-w-7xl mx-auto">
        {/* Breadcrumbs */}
        {breadcrumbs.length > 0 && (
          <nav aria-label="Breadcrumb" className="mb-6 flex items-center space-x-2 text-xs font-medium text-[#94A3B8]">
            <Link href="/" className="hover:text-white transition">
              Home
            </Link>
            {breadcrumbs.map((crumb, idx) => (
              <React.Fragment key={idx}>
                <span className="text-[#64748B]">/</span>
                {crumb.href ? (
                  <Link href={crumb.href} className="hover:text-white transition">
                    {crumb.label}
                  </Link>
                ) : (
                  <span className="text-[#E2E8F0] font-semibold">{crumb.label}</span>
                )}
              </React.Fragment>
            ))}
          </nav>
        )}

        {/* Badge */}
        {badge && (
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#0F766E]/20 border border-[#0D9488]/40 text-[#5EEAD4] text-xs font-bold uppercase tracking-wider mb-4">
            <span className="w-2 h-2 rounded-full bg-[#14B8A6] animate-pulse" />
            {badge}
          </div>
        )}

        {/* Title & Subtitle */}
        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white tracking-tight max-w-4xl leading-tight">
          {title}
        </h1>
        <p className="mt-4 text-base sm:text-lg lg:text-xl text-[#94A3B8] max-w-3xl leading-relaxed">
          {subtitle}
        </p>

        {/* Action Buttons */}
        {(primaryCta || secondaryCta) && (
          <div className="mt-8 flex flex-wrap items-center gap-4">
            {primaryCta && (
              <Link
                href={primaryCta.href}
                className="px-6 py-3 rounded-xl bg-gradient-to-r from-[#0D9488] to-[#2D6A4F] text-white font-semibold text-sm shadow-md hover:brightness-110 transition flex items-center gap-2"
              >
                {primaryCta.label}
                <span>→</span>
              </Link>
            )}
            {secondaryCta && (
              <Link
                href={secondaryCta.href}
                className="px-6 py-3 rounded-xl bg-[#1E293B]/80 hover:bg-[#334155] border border-[#475569] text-[#E2E8F0] font-semibold text-sm transition"
              >
                {secondaryCta.label}
              </Link>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
