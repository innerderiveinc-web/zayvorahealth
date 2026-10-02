/**
 * @file PageHeader.tsx
 * @description Page title + breadcrumb component for admin and clinical pages.
 */
"use client";

import React from "react";
import Link from "next/link";

export interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface PageHeaderProps {
  /** Main page title */
  title: string;
  /** Optional subtitle / description */
  subtitle?: string;
  /** Breadcrumb trail – last item is the current page */
  breadcrumbs?: BreadcrumbItem[];
  /** Optional action slot (e.g., a button row) */
  actions?: React.ReactNode;
}

/**
 * PageHeader – consistent top-of-page title block with breadcrumb nav.
 */
export function PageHeader({
  title,
  subtitle,
  breadcrumbs,
  actions,
}: PageHeaderProps) {
  return (
    <div className="mb-6 flex flex-col gap-1 sm:flex-row sm:items-start sm:justify-between">
      <div>
        {/* Breadcrumbs */}
        {breadcrumbs && breadcrumbs.length > 0 && (
          <nav aria-label="Breadcrumb" className="mb-1">
            <ol className="flex flex-wrap items-center gap-1 text-[11px] text-slate-500">
              {breadcrumbs.map((crumb, idx) => {
                const isLast = idx === breadcrumbs.length - 1;
                return (
                  <li key={idx} className="flex items-center gap-1">
                    {idx > 0 && <span aria-hidden="true">/</span>}
                    {crumb.href && !isLast ? (
                      <Link
                        href={crumb.href}
                        className="hover:text-[#2D6A4F] transition-colors"
                      >
                        {crumb.label}
                      </Link>
                    ) : (
                      <span
                        className={isLast ? "text-slate-300 font-medium" : ""}
                        aria-current={isLast ? "page" : undefined}
                      >
                        {crumb.label}
                      </span>
                    )}
                  </li>
                );
              })}
            </ol>
          </nav>
        )}

        {/* Title */}
        <h1 className="text-xl font-bold text-white tracking-tight">
          {title}
        </h1>

        {/* Subtitle */}
        {subtitle && (
          <p className="mt-0.5 text-xs text-slate-400">{subtitle}</p>
        )}
      </div>

      {/* Action slot */}
      {actions && (
        <div className="flex items-center gap-2 mt-3 sm:mt-0 flex-shrink-0">
          {actions}
        </div>
      )}
    </div>
  );
}
